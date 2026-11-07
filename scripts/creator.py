#!/usr/bin/env python3
"""Creator bootstrap: install upstream tools locally, never their source trees."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent.parent
HOME = ROOT / ".creator"
REA_VERSION = "6.8.0"
CRAFT_VERSION = "0.5.0"
CRAFT_RELEASE = (
    "https://github.com/storytold/craft-anything/releases/download/"
    f"v{CRAFT_VERSION}"
)
MAX_DOWNLOAD = 300 * 1024 * 1024
MAX_EXTRACT = 500 * 1024 * 1024


def artifact_name(system: str | None = None, machine: str | None = None) -> str:
    system = (system or platform.system()).lower()
    machine = (machine or platform.machine()).lower()
    arch = {"amd64": "x86_64", "x64": "x86_64", "arm64": "aarch64"}.get(machine, machine)
    if system == "darwin":
        if arch not in {"x86_64", "aarch64"}:
            raise RuntimeError(f"Unsupported macOS architecture: {machine}")
        return f"craft-anything-cli-{CRAFT_VERSION}-macos-universal.zip"
    if system == "linux":
        if arch not in {"x86_64", "aarch64"}:
            raise RuntimeError(f"Unsupported Linux architecture: {machine}")
        return f"craft-anything-{CRAFT_VERSION}-linux-{arch}.AppImage"
    if system == "windows":
        arch = {"x86_64": "x64", "aarch64": "arm64"}.get(arch, arch)
        if arch not in {"x64", "arm64"}:
            raise RuntimeError(f"Unsupported Windows architecture: {machine}")
        return f"craft-anything-{CRAFT_VERSION}-windows-{arch}-portable.zip"
    raise RuntimeError(f"Unsupported platform: {system} ({machine})")


def fetch(url: str, dest: Path, max_bytes: int = MAX_DOWNLOAD) -> None:
    if not url.startswith("https://"):
        raise RuntimeError("Only HTTPS downloads are permitted")
    request = urllib.request.Request(url, headers={"User-Agent": "Creator-bootstrap/0.1"})
    with urllib.request.urlopen(request, timeout=45) as response, dest.open("wb") as output:
        if not response.geturl().startswith("https://"):
            raise RuntimeError("Download redirected away from HTTPS")
        remaining = max_bytes
        while True:
            part = response.read(min(1024 * 1024, remaining + 1))
            if not part:
                break
            remaining -= len(part)
            if remaining < 0:
                raise RuntimeError(f"Download exceeds limit ({max_bytes} bytes)")
            output.write(part)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as input_file:
        for block in iter(lambda: input_file.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def expected_digest(text: str, filename: str) -> str:
    for line in text.splitlines():
        match = re.fullmatch(r"([a-fA-F0-9]{64})\s+\*?(.+)", line.strip())
        if match and match.group(2).removeprefix("./") == filename:
            return match.group(1).lower()
    raise RuntimeError(f"Upstream SHA256SUMS.txt has no checksum for {filename}")


def safe_unzip(source: Path, target: Path) -> None:
    with zipfile.ZipFile(source) as archive:
        total = 0
        for member in archive.infolist():
            name = member.filename.replace("\\", "/")
            parts = Path(name).parts
            mode = member.external_attr >> 16
            if (
                name.startswith("/")
                or ".." in parts
                or ":" in name
                or (mode & 0o170000) == 0o120000
            ):
                raise RuntimeError(f"Unsafe archive entry: {name}")
            total += member.file_size
            if total > MAX_EXTRACT:
                raise RuntimeError("Archive expands beyond safe limit")
        archive.extractall(target)


def version(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=90, check=False)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()[:350]
        raise RuntimeError(f"Tool invocation failed (exit {result.returncode}): {detail}")
    return (result.stdout or result.stderr).strip().splitlines()[0][:200]


def node_ready() -> None:
    for binary in ("node", "npm"):
        if not shutil.which(binary):
            raise RuntimeError(f"{binary} not on PATH; install official Node.js/npm first")
    major, minor, patch = [
        int(x) for x in version(["node", "--version"]).removeprefix("v").split(".")[:3]
    ]
    if not (
        (major == 22 and (minor, patch) >= (23, 4))
        or (major == 24 and (minor, patch) >= (22, 1))
        or (major == 26 and (minor, patch) >= (12, 1))
        or major > 26
    ):
        raise RuntimeError("REA requires Node >=22.23.4, >=24.22.1 or >=26.12.1")


def rea_command(base: Path = HOME / "rea") -> list[str]:
    exe = base / "node_modules" / "rea-agents" / "scripts" / "rea.mjs"
    return ["node", str(exe)]


def craft_command(base: Path = HOME / "craft") -> list[str]:
    if platform.system().lower() == "linux":
        return [str(base / artifact_name()), "--appimage-extract-and-run", "--cli"]
    executables = sorted(
        p for p in base.rglob("*")
        if p.is_file() and p.name.lower() in {
            "craft-anything-cli", "craft-anything-cli.exe",
            "craft-anything.exe", "craft-anything"
        }
    )
    if not executables:
        raise RuntimeError("No Craft Anything executable found in official release archive")
    cli = [p for p in executables if "cli" in p.name.lower()]
    target = (cli or executables)[0]
    return [str(target)] + ([] if "cli" in target.name.lower() else ["--cli"])


def install_rea(force: bool) -> None:
    dest = HOME / "rea"
    if dest.exists() and not force:
        try:
            print("REA already installed:", version(rea_command()))
            return
        except (RuntimeError, OSError, subprocess.TimeoutExpired):
            print("REA installation failed validation; reinstalling")
    node_ready()
    HOME.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="creator-rea-", dir=HOME) as tmp:
        staging = Path(tmp) / "rea"
        staging.mkdir()
        # Install into a clean local prefix. Ignore upstream install scripts by
        # default; users may opt into additional provider setup independently.
        cmd = [
            "npm", "install", "--prefix", str(staging),
            "--ignore-scripts", "--no-audit", "--no-fund",
            "--save-exact", "--package-lock=true", f"rea-agents@{REA_VERSION}",
        ]
        subprocess.run(cmd, check=True, timeout=600)
        print("REA checked:", version(rea_command(staging) + ["--version"]))
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(staging), str(dest))
    print("REA ready:", version(rea_command() + ["--version"]))


def install_craft(force: bool) -> None:
    dest = HOME / "craft"
    name = artifact_name()
    if dest.exists() and not force:
        try:
            print("Craft Anything already installed:", version(craft_command() + ["--version"]))
            return
        except (RuntimeError, OSError, subprocess.TimeoutExpired):
            print("Craft Anything installation failed validation; reinstalling")
    HOME.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="creator-craft-", dir=HOME) as tmp:
        temp = Path(tmp)
        sums = temp / "SHA256SUMS.txt"
        archive = temp / name
        fetch(f"{CRAFT_RELEASE}/SHA256SUMS.txt", sums, 1024 * 1024)
        fetch(f"{CRAFT_RELEASE}/{name}", archive)
        digest = expected_digest(sums.read_text(encoding="utf-8"), name)
        if sha256(archive) != digest:
            raise RuntimeError(f"Craft Anything SHA256 mismatch: {name}")
        staging = temp / "craft"
        staging.mkdir()
        if name.endswith(".zip"):
            safe_unzip(archive, staging)
            for p in staging.rglob("*"):
                if p.is_file() and p.name == "craft-anything-cli":
                    p.chmod(p.stat().st_mode | 0o111)
        else:
            shutil.copy2(archive, staging / name)
            (staging / name).chmod(0o755)
        print("Craft Anything checked:", version(craft_command(staging) + ["--version"]))
        if dest.exists():
            shutil.rmtree(dest)
        shutil.move(str(staging), str(dest))
    print("Craft Anything ready:", version(craft_command() + ["--version"]))


def doctor() -> int:
    success = True
    for label, cmd in (
        ("REA", rea_command() + ["--version"]),
        ("Craft Anything", None),
    ):
        try:
            actual = cmd if cmd is not None else craft_command() + ["--version"]
            print(f"{label}: ready - {version(actual)}")
        except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
            print(f"{label}: not ready - {exc}")
            success = False
    print("Agent login, optional analysis engines and browsers are NOT checked.")
    return 0 if success else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="One-command Creator upstream bootstrap")
    command = parser.add_subparsers(dest="action", required=True)
    setup = command.add_parser("setup", help="install REA and Craft Anything locally")
    setup.add_argument("--force", action="store_true", help="reinstall pinned versions")
    command.add_parser("doctor", help="check installed upstream CLIs")
    invoke = command.add_parser("run", help="invoke an installed upstream CLI")
    invoke.add_argument("tool", choices=("rea", "craft"))
    invoke.add_argument("args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.action == "setup":
            install_rea(args.force)
            install_craft(args.force)
            return doctor()
        if args.action == "doctor":
            return doctor()
        upstream = rea_command() if args.tool == "rea" else craft_command()
        extra = args.args[1:] if args.args[:1] == ["--"] else args.args
        return subprocess.call(upstream + extra)
    except (RuntimeError, OSError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired, zipfile.BadZipFile) as exc:
        print(f"Creator: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

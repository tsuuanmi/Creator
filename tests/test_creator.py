"""Offline unit tests for deterministic Creator bootstrap components."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import creator


class CreatorTests(unittest.TestCase):
    def test_release_filename_matrix(self):
        self.assertEqual(
            creator.artifact_name("Linux", "amd64"),
            "craft-anything-0.5.0-linux-x86_64.AppImage",
        )
        self.assertEqual(
            creator.artifact_name("Darwin", "arm64"),
            "craft-anything-cli-0.5.0-macos-universal.zip",
        )
        self.assertEqual(
            creator.artifact_name("Windows", "AMD64"),
            "craft-anything-0.5.0-windows-x64-portable.zip",
        )
        with self.assertRaises(RuntimeError):
            creator.artifact_name("Solaris", "x86_64")

    def test_sha_manifest(self):
        content = "a" * 64 + "  sample.zip\n"
        self.assertEqual(creator.expected_digest(content, "sample.zip"), "a" * 64)
        with self.assertRaises(RuntimeError):
            creator.expected_digest(content, "missing.zip")

    def test_hash_file(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / "file"
            p.write_bytes(b"hello")
            self.assertEqual(creator.sha256(p), hashlib.sha256(b"hello").hexdigest())

    def test_archive_rejects_traversal_and_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("../outside", "/absolute"):
                path = root / "bad.zip"
                with zipfile.ZipFile(path, "w") as out:
                    out.writestr(name, "attack")
                with self.assertRaises(RuntimeError):
                    creator.safe_unzip(path, root / "extract")
            path = root / "symlink.zip"
            with zipfile.ZipFile(path, "w") as out:
                info = zipfile.ZipInfo("link")
                info.create_system = 3
                info.external_attr = (0o120777 << 16)
                out.writestr(info, "target")
            with self.assertRaises(RuntimeError):
                creator.safe_unzip(path, root / "extract")

    def test_archive_normal_extract(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / "safe.zip"
            with zipfile.ZipFile(path, "w") as out:
                out.writestr("bin/craft-anything-cli", "ok")
            creator.safe_unzip(path, root / "extract")
            self.assertEqual(
                (root / "extract/bin/craft-anything-cli").read_text(), "ok"
            )


if __name__ == "__main__":
    unittest.main()

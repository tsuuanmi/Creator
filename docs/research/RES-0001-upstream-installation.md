---
id: RES-0001
type: research
status: active
created: 2026-11-07
summary: Distribution options and risks for installing two upstream tools without copying their engines.
---

# Upstream installation and distribution research

**Observed on 2026-11-07; check again before changing versions.**

[REA](https://github.com/morluto/rea) documents `rea-agents` as its npm
package and `npx rea-agents setup` as its interactive MCP registration
workflow. Creator should install the package *locally* without executing that
interactive setup or overwriting an existing agent configuration.
REA requires a sufficiently recent Node.js runtime; its own provider
prerequisites (Ghidra/Hopper/etc.) are separate.

[Craft Anything](https://github.com/storytold/craft-anything) provides
[official release assets](https://github.com/storytold/craft-anything/releases),
including a macOS CLI zip, Linux AppImages with a `--cli` mode, and Windows
portable packages. The 2026-11-07 latest published release observed was
`v0.5.0`, with `SHA256SUMS.txt`. Its build actions still require a separately
signed-in local coding agent. The Linux AppImage includes GUI and CLI but may
have environment dependencies such as FUSE for regular GUI invocation.

The 2026-11-07 latest REA package version observed in its
[package.json](https://github.com/morluto/rea/blob/main/package.json)
was `6.8.0`. Prefer explicit versions, verified release sums, and clear
diagnostics over silent `latest` resolution.

**Risks:** executing npm lifecycle scripts or untrusted downloaded binaries,
archive traversal, mismatched CPU/OS, network interruption, incompatible Node,
missing optional native analysis providers and agent authentication. Source
repositories' license files and third-party notices remain authoritative.

Next experiment: install from public upstream distributions in a clean
Linux/macOS environment, check `rea --help` / Craft CLI and repeat the
bootstrap. No such local live installation is claimed by this research note.

---
type: architecture
status: draft
reviewed: 2026-11-07
implements: [requirements/bootstrap]
---

# Creator tooling boundary (target design)

**Status: target design, not yet shipped in this documentation-only PR.**

`Creator` is a thin installer/launcher facade. REA and Craft Anything are
**independent upstream dependencies**; no source code vendoring, modification,
automatic changes to upstream repos, or reimplementation.

```text
Creator bootstrap/doctor
   |-- REA official npm package (local tool directory)
   |-- Craft Anything official release (local CLI executable)
   +-- local manifest/health checks
             |
    optional System capability (future, NOT MVP)
```

The bootstrap owns version selection, verified downloads, placement and
diagnostics. It must not own deep analysis, study/build/check workflows,
agent accounts, credentials, permission grants, or System Work state.

Initial target is a zero-runtime-dependency Python 3 bootstrap script with
Node/npm as explicit prerequisites for REA. Prefer prebuilt Craft Anything
releases for supported OS/architectures; do not force a Rust source build
when an official release is available. Keep downloads under an ignored local
directory and provide commands to invoke each installed upstream tool.

Optional integration with [System](https://github.com/tsuuanmi/System) must
remain behind an adapter boundary when proposed. It cannot introduce an
additional Work controller, duplicate authorization, or become required for
standalone use.

The [requirements](../requirements/bootstrap.md) are normative. The
[upstream installation research](../research/RES-0001-upstream-installation.md)
is supporting evidence, not an implementation contract.

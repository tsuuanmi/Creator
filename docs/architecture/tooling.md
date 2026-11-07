---
type: architecture
status: active
reviewed: 2026-11-07
implements: [requirements/bootstrap]
---

# Creator tooling boundary

**Implemented:** Creator exposes local `setup`, `doctor` and `run`
commands through a Python script. Actual version pins, invocation and
platform selection are defined by [script](../../scripts/creator.py).
Platform and readiness limitations are detailed in
[engineering](../engineering/bootstrap.md).

```text
Creator bootstrap/doctor
   |-- REA official npm package (local tool directory)
   |-- Craft Anything official release (local CLI executable)
   +-- local health checks
             |
    optional System capability (future, NOT MVP)
```

REA and Craft Anything are independent upstream dependencies; no source code
vendoring, modification, automatic changes to upstream repos, or reimplementation.
Creator does not own deep analysis, study/build/check workflows, agent accounts,
credentials, permission grants or System Work state.

Optional integration with [System](https://github.com/tsuuanmi/System)
must remain behind an adapter boundary when proposed. It must not introduce
another Work controller, duplicate authorization, or become required for
standalone use.

---
type: requirement
status: active
reviewed: 2026-11-07
---

# Creator bootstrap MVP requirements

## Purpose

Creator reduces setup friction: clone a single repository and invoke one
documented command to prepare **both upstream tools** locally.

The tools are:
- [REA](https://github.com/morluto/rea), via the official `rea-agents` npm package.
- [Craft Anything](https://github.com/storytold/craft-anything), via official releases.

## Acceptance criteria

- **REQ-BOOT-001:** One command prepares both tools in a Creator-managed
  location without cloning the upstream repositories.
- **REQ-BOOT-002:** Check prerequisites and supported platforms, report
  actionable errors, and refuse unsupported environments.
- **REQ-BOOT-003:** Explicit pinned versions and upstream origin; verify
  Craft Anything release artifact SHA-256 against its upstream manifest.
- **REQ-BOOT-004:** Repeating setup safely reuses working installations and
  `doctor` checks both tool CLIs.
- **REQ-BOOT-005:** No privilege escalation, global package install, or
  automatic modification of agent settings or shell profiles.
- **REQ-BOOT-006:** Explain that CLI availability is separate from optional
  analysis providers, browser availability and coding-agent authentication.

## Non-goals

No engine duplication, GUI, integrated agent workflow or System plugin yet.

## Ready definition

The upstream REA executable and Craft Anything CLI invoke successfully and
report their versions. This does not establish that all optional backend
capabilities work or that a real reconstruction succeeded.

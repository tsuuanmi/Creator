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
- [REA](https://github.com/morluto/rea), distributed via the official
  `rea-agents` npm package.
- [Craft Anything](https://github.com/storytold/craft-anything), distributed
  via official releases including CLI artifacts.

## Acceptance criteria

- **REQ-BOOT-001:** After clone, one documented bootstrap command prepares
  both tools in a Creator-managed location without cloning either upstream
  repository.
- **REQ-BOOT-002:** The bootstrap checks prerequisites and supported
  platforms, reports actionable errors, and refuses unsupported environments.
- **REQ-BOOT-003:** Version choices are explicit/pinned and source artifacts
  come from upstream; install must verify package integrity where obtainable.
- **REQ-BOOT-004:** Repeating the command is safe and avoids unnecessarily
  reinstalling identical validated versions; `doctor` checks readiness.
- **REQ-BOOT-005:** No privilege escalation or automatic modification of
  users' existing agent settings, shell profiles, or global tools.
- **REQ-BOOT-006:** Documentation distinguishes installation readiness from
  authentication/availability of any coding agent, native analysis provider,
  browser or additional application prerequisites.

## Non-goals for this MVP

Creator does **not** implement a new reverse-engineering engine, duplicate
Craft Anything's build/verify orchestration, ship a UI, automate agent
registration, or become a System plugin yet.

## Definition of ready

Ready means the upstream REA executable and Craft Anything CLI have been
installed and can report a version/help successfully. It does **not** mean
that every optional backend, coding agent, GUI session, target or API key
works without further configuration. A command must not report success
for a tool it did not install or verify.

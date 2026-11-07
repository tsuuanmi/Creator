---
level: 1
areas: [governance=governance, requirements=requirement, architecture=architecture, research=research, engineering=engineering]
id-prefixes: [research=RES]
source-roots: []
forbidden-names: [archive, archives, deprecated, history, legacy, old, temp, temporary]
ledger: governance/retired.md
reachability-depth: 3
review-days: 365
max-lines: 500
reviewed: 2026-11-07
---

# Creator documentation profile

Creator adopts the [portable standard](documentation-architecture.md) from
[System](https://github.com/tsuuanmi/System/blob/main/docs/governance/documentation-architecture.md),
while maintaining its **own** scope, requirements and architecture.

This repository begins at **conformance level 1**, using the portable
[checker](../../tools/docs.py) copied from the System documentation
bootstrap. The checker implements level 1 with some additional link/graph
checks; it is *not* a complete level 2/3 checker. The active source roots list
is empty; independent script/test directories are covered by
[engineering](../engineering/bootstrap.md).

Canonical facts belong to [requirements](../requirements/README.md),
[architecture](../architecture/README.md) and
[engineering](../engineering/README.md). Investigation and upstream
observations belong to [research](../research/README.md). A research record is
not an implementation promise.

Stable research IDs use `RES-NNNN`; retired identities must not be reused.
Only create new documentation areas when content exists. The live source and
tests supersede descriptions of behavior.

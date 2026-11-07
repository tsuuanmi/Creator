# Creator

Creator is a small, independent bootstrap project for two upstream tools:
[REA — Reverse Engineer Anything](https://github.com/morluto/rea) and
[Craft Anything](https://github.com/storytold/craft-anything).

**Goal:** clone Creator, run one setup command, and have both upstream tools
available locally without manually installing each repository.

**Current status:** this documentation PR defines the proposed MVP only.
The bootstrap implementation belongs in a separate PR. Creator does not
reimplement, fork, or bundle either upstream engine.

- [Documentation router](docs/README.md)
- [MVP requirements](docs/requirements/bootstrap.md)
- [Tooling boundaries](docs/architecture/tooling.md)
- [Upstream installation research](docs/research/RES-0001-upstream-installation.md)
- [Documentation governance](docs/governance/documentation.md)

A future optional capability/plugin for
[System](https://github.com/tsuuanmi/System) is an integration goal,
not part of the bootstrap MVP.

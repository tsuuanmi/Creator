# Creator

Creator prepares [REA — Reverse Engineer Anything](https://github.com/morluto/rea)
and [Craft Anything](https://github.com/storytold/craft-anything) from their
**official upstream distributions** with one bootstrap command.

```sh
git clone https://github.com/tsuuanmi/Creator.git
cd Creator
python3 scripts/creator.py setup
```

Requires Python 3.9+ and Node.js/npm compatible with REA. The pinned tools
install into ignored local `.creator/` paths, without cloning their sources,
global installs, sudo or automatic agent configuration.

```sh
python3 scripts/creator.py doctor
python3 scripts/creator.py run rea -- --help
python3 scripts/creator.py run craft -- --help
```

**MVP scope:** bootstrap, tool health checks and a passthrough CLI; no new
reverse-engineering engine, builder or System plugin. Running full studies
or builds may need separate coding-agent authentication, browsers and optional
analysis engines. See the [engineering guide](docs/engineering/bootstrap.md)
for supported platforms, verification and limitations.

- [Documentation](docs/README.md)
- [Requirements](docs/requirements/bootstrap.md)
- [Architecture](docs/architecture/tooling.md)
- [Documentation governance](docs/governance/documentation.md)

An optional capability for [System](https://github.com/tsuuanmi/System)
is a **future** integration, not part of the current MVP.

---
type: engineering
status: active
reviewed: 2026-11-07
covers: [scripts/creator.py, tests/test_creator.py]
---

# Creator bootstrap execution

From a Creator checkout, use Python 3.9+:

```sh
python3 scripts/creator.py setup
python3 scripts/creator.py doctor
python3 scripts/creator.py run rea -- --help
python3 scripts/creator.py run craft -- --help
```

**Supported initial targets:** macOS Intel/Apple silicon; Linux x86-64/arm64;
Windows x64/arm64. Creator installs REA from the pinned npm package under
`.creator/rea` and downloads the matching Craft Anything v0.5.0 CLI or
portable distribution into `.creator/craft`. It does not alter global
`npm`, shell, agent settings, or ask for `sudo`.

REA requires an already-installed Node.js/npm satisfying REA's supported
Node versions. Creator deliberately uses `npm --ignore-scripts` to avoid
running dependency installation scripts; functionality that requires
native package setup may still need an explicit separate upstream step.
Craft download SHA-256 is compared against the checksum manifest published
with the same upstream release. This verifies download integrity relative
to that manifest; it does not independently authenticate the manifest signer.

`setup` is repeatable: if installed executables report versions, they are
reused; `--force` reinstalls. `doctor` checks local CLI invocation, not
AI authentication, browser availability, optional reverse engineering engines,
or actual reconstruction success. `run` invokes unmodified upstream commands.
All installation files are ignored by Git.

### Checks

```sh
python3 -m unittest discover -s tests -v
python3 tools/docs.py check
python3 tools/docs.py sync --check
```

Actual upstream network installations are **not** part of offline unit
tests. CI validates the local implementation and documentation without
fetching or executing upstream release binaries. Run a real setup and
doctor on each supported target before claiming end-to-end qualification.

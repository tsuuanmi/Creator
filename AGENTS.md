# Creator agent instructions

1. Read [README.md](README.md), [docs/README.md](docs/README.md), and
   [the local documentation profile](docs/governance/documentation.md).
2. Use `python3 tools/docs.py trace <path-or-ID>` to inspect typed
   documentation relationships before changing an established contract.
3. Read the governing [engineering](docs/engineering/bootstrap.md) and
   relevant tests before editing bootstrap code.
4. Treat research and proposals as non-normative: they are not shipped behavior.
5. Keep one authoritative home for each fact and update governing documentation
   with changes to implementation. Do not hand-edit generated index blocks.
6. Preserve upstream separation: never copy/fork REA or Craft Anything engines.
   Installation must not silently rewrite global agent settings or use elevated
   privileges. External archives and package scripts are untrusted inputs.
7. Run `python3 -m unittest discover -s tests -v`,
   `python3 tools/docs.py check` and
   `python3 tools/docs.py sync --check` before submitting; for changes to
   covered paths also run `python3 tools/docs.py impact <base-ref>`.
   Never bypass failing required checks.

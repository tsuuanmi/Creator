# Bootstrap documentation governance in Creator

This is the Creator-local companion to the
[portable documentation standard](documentation-architecture.md).
The generic scaffold workflow originates in
[System's bootstrap guide](https://github.com/tsuuanmi/System/blob/main/docs/governance/bootstrap.md);
do not copy System product requirements into Creator.

Creator's governance is already initialized. To maintain it:

1. Read the [Creator-specific profile](documentation.md); its declared areas,
   IDs and source roots are authoritative for this repository.
2. Route every new document through [docs/README.md](../README.md)
   and the owning area's README, adding an area only when it has content.
3. Update canonical requirements/architecture with code changes; store
   unaccepted discoveries separately under research.
4. Run `python3 tools/docs.py check` and
   `python3 tools/docs.py sync --check` after documentation edits.
5. Run `python3 tools/docs.py impact <base-ref>` when changing paths covered
   by an authoritative documentation record.

The included portable checker is **level 1**, with selected additional graph
checks. Never claim full level-2/3 conformance without implementing and testing
those rules first. Retired records use the [ledger](retired.md) rather than
keeping duplicate current-state documents.

# v471 THOS v4 x1 Plugin-Cache Approval Packet

Status: `OPEN_GAP`.

The live skill-surface audit still reports `42` affected plugin-cache skill files, with `42` missing or unclosed frontmatter signals and `42` missing name signals. User skill false positives remain cleared by the current audit shape.

The approved v4 action is an approval packet and rehearsal boundary, not live mutation. The safe path is: build an exact affected-path manifest, rehearse repair/quarantine in a temporary directory, run fixture assertions, review a concrete diff, and only then request explicit path-specific approval before touching plugin-cache files.

This keeps THOS moving without conflating broad project permission with a high-risk cache mutation.

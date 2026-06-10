# v470 THOS v5 x1 to v470 THOS v5 x2 Handoff

Next expected phase: `v470_THOS_v5_x2`.

## Handoff Tasks

- Run `scripts/thos_supervisor_gate.py` against the synthetic fixture file.
- Record the dry-run decision report as a v5 x2 artifact.
- Add negative fixtures for unauthorized spawn, connector write, cleanup execution, and overclaim publication language.
- Map each fixture to a stable supervisor rule ID.
- Start a local visualization dataset from supervisor rows only.
- Keep connector writes unperformed unless named target and separate approval exist.
- Keep all six GMUT gates open.

## Open Blockers

- CLI sibling internal shell inspection remains unstable under `windows sandbox: spawn setup refresh`.
- Plugin and connector observe-vs-mutate metadata is not normalized across all surfaces.
- Skill frontmatter cleanup candidates are identified but not changed in this phase.
- Visualization remains schema-first, not a rendered dashboard.

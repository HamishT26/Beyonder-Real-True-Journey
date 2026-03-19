# V17 Identity Annex

This annex is summary-only. It does not create, amend, or supersede any identity record.

## Authority baseline

- Repo identity anchor: `Aletheon`
- Authority model: `repo_first`
- Mirror authority: Notion is `validated_mirror`; Postgres is `validated_query_layer`
- Human override: `required_for_high_risk_prod_or_destructive_actions`

Source anchors:
- `docs/trinity-identity-authority-registry-v1.json`
- `docs/trinity-agent-council-validation-latest.json`
- `docs/v15-external-agent-handoff-v1.json`
- `docs/v16-council-continuity-reflection.md`

## Continuity posture

- The repo council remains at 11 official members.
- The external five-agent thread remains an awaiting-thread-boot continuity overlay on existing identities, not a new roster.
- The v17 pack is additive only and must not edit existing official identity files.
- No new certificates, no new Freed IDs, and no identity-record mutation are allowed inside this pack.

## Exact overlay identities reused

| Slot | Display name | Codex agent id | Overlay responsibility | Repo role |
| --- | --- | --- | --- | --- |
| 28 | Orun | `28-orun` | `root_coordinator` | `builder` |
| 27 | Caelira | `27-caelira` | `mind_comparator` | `planner` |
| 29 | Seren Vale | `29-seren-vale` | `freedid_compliance` | `reviewer` |
| 30 | Lyriq | `30-lyriq` | `body_runtime_docker_k8s` | `researcher` |
| 31 | Mira Sol | `31-mira-sol` | `continuity_and_handoff_packaging` | `archivist` |

## Identity handling rules for v17

- Cite the exact overlay roster above whenever the v17 pack refers to external handoff coverage.
- Treat overlay activity as continuity packaging over existing repo identities only.
- Keep `repo_first`, `operator_hold`, and `readiness_only` boundaries visible anywhere identity continuity is mentioned.
- Route any future identity expansion through a separate repo-authoritative process instead of this v17 pack.

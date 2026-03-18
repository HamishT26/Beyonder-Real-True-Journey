# V17 Validation Annex

## Validation baseline

The v17 pack inherits its proof posture from the committed March 18 v16 baseline plus the current repo-authoritative verdict and council-state surfaces:

- `docs/v17-baseline-state-v1.json` pins the March 18 v16 green checkpoint: `1007 PASS / 0 WARN / 0 FAIL`, `950/950`, `operator_hold`, and `readiness_only`.
- `docs/v16-trinity-verdict-v1.json` keeps the evidence split explicit: repo-proven strengths, comparative promise, and not-yet-externally-established claims.
- `docs/trinity-agent-council-validation-latest.json` keeps the present 11-member council state explicit.
- `docs/trinity-instance-handoff-contract-v1.json` keeps handoff mode `repo_first` with `repo_authoritative_restore` and `no_hidden_live_writes`.

## Required evidence grammar

Every v17 closeout or handoff writeup should separate:

- `confirmed_evidence`: what the repo already proves and can cite directly.
- `inference`: bounded interpretation that stays below proof.
- `open_gap`: what remains unproven, blocked, or readiness-only.

## Seeded validation lanes

| Lane | Confirmed evidence | Inference | Open gap |
| --- | --- | --- | --- |
| Mind | `docs/v16-gmut-comparator-refresh.md` keeps canonical surface and evidence split explicit. | Comparator refresh can continue if it preserves explicit evidence, inference, and open-gap labeling. | GMUT is not externally established as a leading theory by current in-repo proof. |
| Body | `docs/v17-baseline-state-v1.json` plus `docs/v16-docker-k8s-runtime-bridge.md` support bounded local runtime readiness. | Runtime readiness can inform planning and probes inside repo scope. | No production-proof or hidden cloud-control claims are allowed. |
| Heart | `docs/v16-freedid-compliance-fabric.md` keeps standards-first governance comparison explicit. | Compliance comparison can expand only as comparison, not as universal-law promotion. | Freed ID and Cosmic Bill are not proven as universal law by current in-repo proof. |
| Continuity | `docs/trinity-agent-council-validation-latest.json`, `docs/v16-council-continuity-reflection.md`, and `docs/v15-external-agent-handoff-v1.json` preserve the five-agent overlay and 11-member council continuity. | The overlay can keep packaging evidence-first handoffs over existing identities. | The overlay must not be represented as a new roster or identity issuance event. |

## Validation checks before handoff

- Confirm `repo_first`, `operator_hold`, and `readiness_only` are stated without contradiction.
- Confirm no edits landed in existing official identity files, legacy proof artifacts, or unrelated non-v17 docs as part of this pack, except for approved additive `.codex/agents/*.toml` support files.
- Confirm the closeout summary logs `requested_model`, `offered_model`, `selected_model`, `resolved_model`, and `runtime_surface`.
- Confirm the exact five overlay identities are reused with no renaming, slot changes, or scope inflation.
- Confirm any future-facing claims remain below externally established proof unless a newer repo-authoritative artifact changes the evidence band.

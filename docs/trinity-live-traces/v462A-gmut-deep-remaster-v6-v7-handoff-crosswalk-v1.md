# v462A_GMUT_v6 to v7 Handoff Crosswalk v1

Generated UTC: 2026-05-29T10:02:38Z
Generated NZ: 2026-05-29T22:02:38+12:00

## Status

This crosswalk prepares exact fields for v7. It does not uplift source authority or promote any candidate row.

## Required v7 Fields

- `requested_symbol`
- `source_artifact`
- `source_artifact_commit`
- `canonical_alias_if_any`
- `unit_status`
- `accounting_decision`
- `definition_status`
- `divergence_status`
- `observable_status`
- `source_tier`
- `trace_id`
- `last_reviewed_utc`
- `claim_limit`
- `promotion_allowed`

## Seed Rows

- blocker: `T_Psi_mu_nu` points to the v6 scalar template attempt, but remains quarantined with no canon alias, no unit completion, no divergence result, and no observable map.
- blocker: `B_Psi_mu_nu` remains quarantined with no selected canon alias.
- blocker: `Psi` remains definition-only as a candidate symbol.
- blocker: `V(Psi)` remains definition-only with no functional form.
- blocker: `alpha_Psi` remains quarantine/null-switch context only.

## Source Anchor Policy

- advisory: External anchors remain context-only in v6.
- blocker: No live claim-specific review was performed in v6.

## Handoff

v462A_GMUT_v7 should use this crosswalk to run a bounded unit/divergence fixture or perform one claim-specific source-anchor review.

# v467A GMUT v8 x1 Governance Envelope

Prepared: 2026-06-01T22:45:00+12:00

This envelope captures the governance controls that `v8_x1` can safely carry forward. Its non-escalation rule is strict: cleaner schemas, stronger manifests, stable digests, and better governance never upgrade GMUT scientific status by themselves.

## Profile Tiers

- `P0_minimal_advisory`: required status fields are present; no result or closure semantics allowed.
- `P1_structural`: schema, registry, and lint rows are structurally complete; scientific status remains unchanged.
- `P2_comparative`: comparative rows connect to source-authority classes; they remain context or guard design.
- `P3_handoff_bundle`: artifacts are packaged for the next phase; no physics execution is implied.

## Registry And Lint Controls

Registry fields should include `display_key`, `normalized_key`, `lineage_key`, `digest_scope_key`, `canon_status`, `quarantine_status`, `claim_domain`, `gate_dependency`, `source_class`, `parent_version`, and `root_commit`.

Lint order should run as: schema parse validity, key normalization and alias resolution, referential integrity, digest lineage integrity, quarantine/contamination/leakage enforcement, blocked-claim language enforcement, coverage accounting, downgrade analytics and registry diff, then envelope assembly with an advisory status stamp.

Failure codes should remain refusal-only, including missing source anchor, empty expression refs, forbidden result field, non-open gate, source authority mismatch, `B_PSI_PROMOTION`, `V_PSI_OVERSPECIFIED`, Journey/Solas overclaim, disabled/held overlap, natural-units overpromotion, conservation prerequisite gap, fifth-force source gap, consciousness proxy boundary gap, free-text identifier, and cross-subject contamination.

Identity ambiguity classes are `A0_unambiguous`, `A1_alias_resolved`, `A2_context_resolved`, `A3_collision_unresolved`, `A4_composite_boundary`, and `A5_noncanon_shadow`. `A3` and `A5` should block canonical merge.

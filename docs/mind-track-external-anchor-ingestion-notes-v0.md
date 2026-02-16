# Mind Track External-Anchor Ingestion Notes v0 (GMUT-005)

Purpose: define the canonical-ingestion checklist required before external
anchor rows can move from provisional screening into fit/exclusion evidence.

---

## Required ingestion fields

Every anchor row must include:
1. `source_citation` (primary publication/report citation),
2. `dataset_version_or_release` (explicit version/date tag),
3. `confidence_level` (e.g. 0.95),
4. `external_uncertainty_abs` (absolute uncertainty on bound),
5. `bound_units`,
6. `signal_mapping_note` (how external signal maps to GMUT parameter).

These fields are tracked in:
- `docs/mind-track-external-anchor-canonical-inputs-v1.json`
- (legacy reference, now deprecated): `docs/mind-track-external-anchor-provisional-inputs-v0.json`

---

## Canonical-source upgrade targets

Current canonical ingestion set v1 now includes:
1. MICROSCOPE EP bound:
   - primary citation + release tag + uncertainty metadata included.
2. Eot-Wash torsion-balance bound:
   - primary citation + release tag + uncertainty metadata included.
3. APOLLO/LLR residual anchor:
   - primary citation + release tag + uncertainty metadata included.

Remaining upgrade action:
- Attach reproducible extraction trace IDs for each numeric bound.

---

## Promotion guardrail

No anchor row should be marked non-provisional until:
- source tier is `primary`,
- ingestion status is `ingested_primary_source`,
- uncertainty and confidence fields are present and non-placeholder.

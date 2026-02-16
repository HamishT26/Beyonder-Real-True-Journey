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
- `docs/mind-track-external-anchor-provisional-inputs-v0.json`

---

## Canonical-source upgrade targets

1. MICROSCOPE EP bound:
   - replace secondary summary link with mission publication/release citation.
2. Eot-Wash torsion-balance bound:
   - replace placeholder bound bucket with publication-grade exclusion value.
3. ILRS/APOLLO LLR residual bound:
   - replace placeholder residual proxy with canonical release value.

---

## Promotion guardrail

No anchor row should be marked non-provisional until:
- source tier is `primary`,
- ingestion status is `ingested_primary_source`,
- uncertainty and confidence fields are present and non-placeholder.

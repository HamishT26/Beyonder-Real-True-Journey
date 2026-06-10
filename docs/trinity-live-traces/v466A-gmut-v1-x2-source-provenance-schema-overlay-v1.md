# v466A GMUT v1 x2 Source Provenance Schema Overlay

Phase: `v466A_GMUT_v1_x2`

Status: `FIELD_LEVEL_PROVENANCE_SCHEMA_OVERLAY_HOLD`

Start NZ: `2026-06-01T02:39:39+12:00`

Prepared NZ: `2026-06-01T02:42:53+12:00`

Live Git start: local `15f06589955e9b36da0d0752bb635214fa60f8fe`, shared remote `15f06589955e9b36da0d0752bb635214fa60f8fe`, drift `0 0`.

## Purpose

This overlay tightens the v466A v1 x1 exact-row scaffold with field-level provenance and source-role requirements. It does not validate GMUT, close any gate, or promote Journey/Solas material into physics evidence.

## External Source Roles

The web refresh used 24 searches and organized sources into context-only support routes:

- JSON Schema 2020-12 validation/core: schema structure and validation discipline only.
- W3C PROV-O, Data on the Web Best Practices, DCAT 3, FAIR principles, RO-Crate, and schema.org Dataset: provenance and dataset metadata routing only.
- NIST SP 811, BIPM SI brochure, NIST TN 1297, JCGM 100, JCGM 200, and NIST CODATA constants: SI, uncertainty, and metrology vocabulary routing only.
- Carroll GR notes, GHY boundary-term route, Hilbert stress-energy route, MICROSCOPE, Eot-Wash, and 2026 scalar/short-range gravity sources: convention and constraint routing only.
- COGITATE/Nature, Scientific Data, PubMed review context, and PCI review context: consciousness proxy caution only.

## Required Per-Field Overlay

Every schema field that attempts to support, constrain, or block a GMUT claim now needs:

- `field_id`
- `row_id`
- `source_id`
- `source_role`
- `statement_id`
- `applies_to_field`
- `interpretation_type`
- `source_locator`
- `extraction_note`
- `supports_claim_ids`
- `does_not_support_claim_ids`
- `constrains_claim_ids`
- `regime`
- `uncertainty_semantics`
- `exactness_class`
- `claim_ceiling`
- `hold_state`
- `hold_reason`

## Decision

The current result is a stricter hold. v466A v2 x1 should ask the five active advisory lanes to propose minimal local row instances and stable claim IDs for this overlay. All six GMUT gates remain open.

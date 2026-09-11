# Four retained operation contracts

## Declared grid-coordinate scale

Represent an explicitly declared dimensionless pixel scale while withholding physical calibration and measurement claims.

Ceiling: represented.

Request:

```json
{
  "op": "grid_resolution_nonconversion",
  "pixels": [
    0,
    1
  ],
  "scale": [
    2,
    3
  ],
  "origin": [
    -1,
    1
  ],
  "unit": "declared_grid_unit"
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "coordinates": [
      -1,
      4
    ],
    "unit": "declared_grid_unit",
    "physical_calibration": false
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-grid-resolution-nonconversion and its source hash.

## Text and symbol legend collisions

Expose empty labels and duplicate text or symbol cues so a color cue cannot silently become the sole distinction.

Ceiling: completed.

Request:

```json
{
  "op": "text_symbol_legend_review",
  "rows": [
    {
      "id": "a0",
      "text": "low 0",
      "symbol": "circle"
    },
    {
      "id": "b0",
      "text": "high 0",
      "symbol": "circle"
    }
  ]
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "missing_text": [],
    "duplicate_symbols": [
      "circle"
    ],
    "duplicate_text": [],
    "manual_review_required": true
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-text-symbol-legend-review and its source hash.

## Visual uncertainty evaluation vacancies

Keep independent evaluation and affected-user evidence missing despite structurally complete synthetic review notes.

Ceiling: open_gap.

Request:

```json
{
  "op": "visual_uncertainty_review_vacancies",
  "notes": {
    "denominator": "",
    "interval_basis": "",
    "missingness": "",
    "sampling_rule": ""
  },
  "evaluation_count": 0
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "missing_notes": [
      "denominator",
      "interval_basis",
      "missingness",
      "sampling_rule"
    ],
    "evaluation_count": 0,
    "independent_review": false,
    "affected_user_review": false,
    "real_evidence_gap": true
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-visual-uncertainty-review-vacancies and its source hash.

## Image release obligation hold

Report missing provenance, license and review declarations while always withholding external publication authority.

Ceiling: exact_gate.

Request:

```json
{
  "op": "image_release_obligation_matrix",
  "asset": "synthetic-grid-0",
  "declarations": {
    "provenance": true,
    "license": true,
    "review": true
  },
  "external_authority": false
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "asset": "synthetic-grid-0",
    "missing": [],
    "external_action": false,
    "authority_verified": false
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-image-release-obligation-matrix and its source hash.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, production-identity, professional, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood or Stage 20 claim. NOT_READY_FOR_STAGE_20.

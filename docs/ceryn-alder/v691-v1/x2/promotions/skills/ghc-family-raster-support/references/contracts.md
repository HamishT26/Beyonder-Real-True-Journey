# Four retained operation contracts

## Boolean mask run intervals

Encode true row spans as maximal half-open runs and retain exact foreground cardinality.

Ceiling: completed.

Request:

```json
{
  "op": "pixel_mask_runs",
  "row": [
    false
  ]
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "runs": [],
    "foreground": 0
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-pixel-mask-runs and its source hash.

## Clipped grid neighborhood

Return only in-grid four or eight adjacent cells in row-major order, excluding the center.

Ceiling: completed.

Request:

```json
{
  "op": "neighborhood_stencil",
  "width": 1,
  "height": 1,
  "x": 0,
  "y": 0,
  "connectivity": 4
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "neighbors": []
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-neighborhood-stencil and its source hash.

## Summed-area rectangle query

Compare a prefix-table rectangle result with a frozen direct enumeration oracle.

Ceiling: completed.

Request:

```json
{
  "op": "integral_plane_queries",
  "grid": [
    [
      -3
    ]
  ],
  "rectangle": [
    0,
    0,
    1,
    1
  ]
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "sum": -3,
    "count": 1
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-integral-plane-queries and its source hash.

## Center-based nearest sampling

Map destination cell centers to bounded source indices using an explicit floor convention.

Ceiling: completed.

Request:

```json
{
  "op": "nearest_grid_mapping",
  "source_width": 1,
  "destination_width": 11
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "indices": [
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ],
    "convention": "destination_center_floor"
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-nearest-grid-mapping and its source hash.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, production-identity, professional, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood or Stage 20 claim. NOT_READY_FOR_STAGE_20.

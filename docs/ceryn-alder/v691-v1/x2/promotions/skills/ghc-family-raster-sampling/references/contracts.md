# Four retained operation contracts

## Quarter-cell bilinear weights

Keep four integer weight numerators over sixteen, preserving constants and convex support.

Ceiling: completed.

Request:

```json
{
  "op": "bilinear_weight_witness",
  "qx": 0,
  "qy": 0,
  "samples": [
    -3,
    2,
    2,
    1
  ]
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "weight_numerators": [
      16,
      0,
      0,
      0
    ],
    "weight_denominator": 16,
    "value": {
      "numerator": -3,
      "denominator": 1
    }
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-bilinear-weight-witness and its source hash.

## Stencil support and padding

Distinguish refused missing stencil support from explicit zero padding; never invent an edge policy.

Ceiling: completed.

Request:

```json
{
  "op": "convolution_support_refusal",
  "grid": [
    [
      -3,
      -2,
      -1
    ],
    [
      -1,
      0,
      1
    ],
    [
      1,
      2,
      3
    ]
  ],
  "x": 0,
  "y": 1,
  "weights": [
    1,
    2,
    1
  ],
  "padding": "refuse"
}
```

Expected full output:

```json
{
  "ok": false,
  "error": "missing_support",
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-convolution-support-refusal and its source hash.

## Partial-block sample means

Partition a finite plane into blocks and expose each sum and support count without fabricating edge samples.

Ceiling: completed.

Request:

```json
{
  "op": "downsample_block_means",
  "grid": [
    [
      -3
    ]
  ],
  "block_width": 1,
  "block_height": 2
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "blocks": [
      {
        "origin": [
          0,
          0
        ],
        "sum": -3,
        "count": 1,
        "mean": {
          "numerator": -3,
          "denominator": 1
        }
      }
    ],
    "input_count": 1
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-downsample-block-means and its source hash.

## Explicit histogram endpoints

Assign each finite value to left-closed bins, optionally closing the last edge, and retain excluded values.

Ceiling: completed.

Request:

```json
{
  "op": "finite_histogram_bins",
  "values": [
    -2,
    -5,
    0,
    2,
    4,
    7
  ],
  "edges": [
    -2,
    0,
    2,
    4,
    6
  ],
  "last_closed": true
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "counts": [
      1,
      1,
      1,
      1
    ],
    "excluded": 2,
    "last_closed": true
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-finite-histogram-bins and its source hash.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, production-identity, professional, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood or Stage 20 claim. NOT_READY_FOR_STAGE_20.

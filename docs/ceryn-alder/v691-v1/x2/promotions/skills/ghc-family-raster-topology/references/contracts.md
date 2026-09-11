# Four retained operation contracts

## Four-connected mask regions

Separate orthogonally connected foreground components without joining diagonal contact.

Ceiling: completed.

Request:

```json
{
  "op": "mask_connected_regions",
  "grid": [
    [
      true
    ]
  ]
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "components": [
      [
        [
          0,
          0
        ]
      ]
    ],
    "foreground": 1
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-mask-connected-regions and its source hash.

## Exposed cell-face inventory

Count and identify exposed north east south west faces of a finite Boolean mask.

Ceiling: completed.

Request:

```json
{
  "op": "mask_boundary_edges",
  "grid": [
    [
      true
    ]
  ]
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "faces": [
      {
        "cell": [
          0,
          0
        ],
        "side": "N"
      },
      {
        "cell": [
          0,
          0
        ],
        "side": "E"
      },
      {
        "cell": [
          0,
          0
        ],
        "side": "S"
      },
      {
        "cell": [
          0,
          0
        ],
        "side": "W"
      }
    ],
    "perimeter": 4
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-mask-boundary-edges and its source hash.

## Intensity tie ranks

Return dense or competition ranks while preserving original order and ties.

Ceiling: completed.

Request:

```json
{
  "op": "finite_intensity_ranks",
  "values": [
    0,
    0,
    0,
    -1,
    2,
    -1
  ],
  "mode": "competition"
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "ranks": [
      3,
      3,
      3,
      1,
      6,
      1
    ],
    "mode": "competition"
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-finite-intensity-ranks and its source hash.

## Affine interval support

Propagate declared interval bounds through signed integer coefficients without claiming calibrated measurement uncertainty.

Ceiling: represented.

Request:

```json
{
  "op": "interval_pixel_propagation",
  "intervals": [
    [
      0,
      1
    ],
    [
      1,
      2
    ]
  ],
  "coefficients": [
    -1,
    2
  ],
  "offset": -4
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "interval": [
      -3,
      0
    ],
    "measurement": false,
    "calibrated": false
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-interval-pixel-propagation and its source hash.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, production-identity, professional, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood or Stage 20 claim. NOT_READY_FOR_STAGE_20.

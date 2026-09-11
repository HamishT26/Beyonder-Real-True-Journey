# Four retained operation contracts

## Raster element layout

Derive planar element counts and row-major element strides; byte size and a real image format are deliberately unspecified.

Ceiling: completed.

Request:

```json
{
  "op": "raster_layout_shape",
  "width": 1,
  "height": 1,
  "channels": 1
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "elements": 1,
    "row_stride": 1,
    "pixel_stride": 1,
    "shape": [
      1,
      1,
      1
    ],
    "unit": "elements"
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-raster-layout-shape and its source hash.

## Pixel coordinate inverse

Map a finite row-major pixel address to its linear index and recover the exact coordinate.

Ceiling: completed.

Request:

```json
{
  "op": "pixel_coordinate_bijection",
  "width": 1,
  "height": 1,
  "x": 0,
  "y": 0
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "index": 0,
    "coordinate": [
      0,
      0
    ]
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-pixel-coordinate-bijection and its source hash.

## Half-open region intersection

Intersect two integer half-open rectangles, retaining empty intersections without negative area.

Ceiling: completed.

Request:

```json
{
  "op": "pixel_region_intersection",
  "a": [
    -1,
    0,
    1,
    1
  ],
  "b": [
    1,
    0,
    3,
    1
  ]
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "rectangle": null,
    "area": 0
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-pixel-region-intersection and its source hash.

## Finite region union coverage

Enumerate the union of clipped integer cells once while retaining overlapping source coverage.

Ceiling: completed.

Request:

```json
{
  "op": "pixel_region_union_cells",
  "width": 1,
  "height": 1,
  "rectangles": [
    [
      -1,
      0,
      1,
      1
    ],
    [
      0,
      0,
      1,
      1
    ],
    [
      0,
      0,
      2,
      2
    ]
  ]
}
```

Expected full output:

```json
{
  "ok": true,
  "value": {
    "cells": [
      {
        "cell": [
          0,
          0
        ],
        "coverage": 3
      }
    ],
    "area": 1,
    "overlap_cells": 1
  },
  "authority": false
}
```

An added unreviewed_authority field yields an unknown_field envelope with authority false. Preserve the original phase guide ghc-family-pixel-region-union-cells and its source hash.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, production-identity, professional, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood or Stage 20 claim. NOT_READY_FOR_STAGE_20.

# real_cluster_observation_gate

Expose absent real-cluster rows and independent review as an open gap.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Zero rows and no review remain open

Request:
```json
{
  "op": "real_cluster_observation_gate",
  "record": {
    "required": [
      "real_cluster_rows",
      "independent_review"
    ],
    "rows": [],
    "review": null
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "required": [
      "independent_review",
      "real_cluster_rows"
    ],
    "real_rows": 0,
    "review_state": null,
    "missing": [
      "independent_review",
      "real_cluster_rows"
    ],
    "qualified": false,
    "inference": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## Synthetic rows are not real observations

Request:
```json
{
  "op": "real_cluster_observation_gate",
  "record": {
    "required": [
      "real_cluster_rows",
      "independent_review"
    ],
    "rows": [],
    "review": "same_owner_synthetic"
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "required": [
      "independent_review",
      "real_cluster_rows"
    ],
    "real_rows": 0,
    "review_state": "same_owner_synthetic",
    "missing": [
      "independent_review",
      "real_cluster_rows"
    ],
    "qualified": false,
    "inference": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## A citation does not provide a cluster row

Request:
```json
{
  "op": "real_cluster_observation_gate",
  "record": {
    "required": [
      "real_cluster_rows",
      "independent_review",
      "operator_context"
    ],
    "rows": [],
    "review": "citation_only"
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "required": [
      "independent_review",
      "operator_context",
      "real_cluster_rows"
    ],
    "real_rows": 0,
    "review_state": "citation_only",
    "missing": [
      "independent_review",
      "operator_context",
      "real_cluster_rows"
    ],
    "qualified": false,
    "inference": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## Null review stays absent

Request:
```json
{
  "op": "real_cluster_observation_gate",
  "record": {
    "required": [
      "real_cluster_rows",
      "independent_review",
      "privacy_review"
    ],
    "rows": [],
    "review": null
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "required": [
      "independent_review",
      "privacy_review",
      "real_cluster_rows"
    ],
    "real_rows": 0,
    "review_state": null,
    "missing": [
      "independent_review",
      "privacy_review",
      "real_cluster_rows"
    ],
    "qualified": false,
    "inference": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## Authority and Maori review cannot be synthesized

Request:
```json
{
  "op": "real_cluster_observation_gate",
  "record": {
    "required": [
      "real_cluster_rows",
      "independent_review",
      "affected_party_authority",
      "maori_authority"
    ],
    "rows": [],
    "review": "same_owner"
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "required": [
      "affected_party_authority",
      "independent_review",
      "maori_authority",
      "real_cluster_rows"
    ],
    "real_rows": 0,
    "review_state": "same_owner",
    "missing": [
      "affected_party_authority",
      "independent_review",
      "maori_authority",
      "real_cluster_rows"
    ],
    "qualified": false,
    "inference": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

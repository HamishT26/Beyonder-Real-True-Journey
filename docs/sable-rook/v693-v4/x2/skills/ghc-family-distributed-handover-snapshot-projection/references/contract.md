# handover_snapshot_projection

Represent a fixity-bound handover snapshot without claiming an external transfer.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Empty snapshot remains fixity bound

Request:
```json
{
  "op": "handover_snapshot_projection",
  "record": {
    "snapshot": {
      "replicas": {}
    },
    "holds": [],
    "next_owner_label": "next-reviewer"
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "snapshot_digest": "3e4cb1eefa5b8201869039ae472703db3dd6f3569ba251be88b30a7e40599a5b",
    "replicas": [],
    "holds": [],
    "next_owner_label": "next-reviewer",
    "external_transfer": false,
    "acknowledged": false,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## One replica snapshot lists its label

Request:
```json
{
  "op": "handover_snapshot_projection",
  "record": {
    "snapshot": {
      "replicas": {
        "a": {
          "clock": {
            "a": 1
          }
        }
      }
    },
    "holds": [],
    "next_owner_label": "next-reviewer"
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "snapshot_digest": "87d256efdad55a32c9780c1f99d31febba1bd1c4780cf954aeea0861ea392611",
    "replicas": [
      "a"
    ],
    "holds": [],
    "next_owner_label": "next-reviewer",
    "external_transfer": false,
    "acknowledged": false,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Hold reasons remain explicit

Request:
```json
{
  "op": "handover_snapshot_projection",
  "record": {
    "snapshot": {
      "replicas": {
        "a": {}
      }
    },
    "holds": [
      "missing_review"
    ],
    "next_owner_label": "next-reviewer"
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "snapshot_digest": "0617c513e8da9f7475f9eb2d1b03412460a5e3e129bf04c279d8a75c5ae20bea",
    "replicas": [
      "a"
    ],
    "holds": [
      "missing_review"
    ],
    "next_owner_label": "next-reviewer",
    "external_transfer": false,
    "acknowledged": false,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Multiple replica labels are sorted

Request:
```json
{
  "op": "handover_snapshot_projection",
  "record": {
    "snapshot": {
      "replicas": {
        "b": {},
        "a": {}
      }
    },
    "holds": [
      "conflict"
    ],
    "next_owner_label": "next-reviewer"
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "snapshot_digest": "46d202dc9f64e694fe671699094740eee9538f4a7efbe8323561135c7d2401c0",
    "replicas": [
      "a",
      "b"
    ],
    "holds": [
      "conflict"
    ],
    "next_owner_label": "next-reviewer",
    "external_transfer": false,
    "acknowledged": false,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## A different public role label changes the binding

Request:
```json
{
  "op": "handover_snapshot_projection",
  "record": {
    "snapshot": {
      "replicas": {
        "a": {}
      }
    },
    "holds": [
      "authority"
    ],
    "next_owner_label": "competent-operator"
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "snapshot_digest": "0617c513e8da9f7475f9eb2d1b03412460a5e3e129bf04c279d8a75c5ae20bea",
    "replicas": [
      "a"
    ],
    "holds": [
      "authority"
    ],
    "next_owner_label": "competent-operator",
    "external_transfer": false,
    "acknowledged": false,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

# anti_entropy_delta

Identify newer source records and equal-version value conflicts without network transfer.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Empty replicas need no delta

Request:
```json
{
  "op": "anti_entropy_delta",
  "record": {
    "source": {},
    "target": {}
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "send": [],
    "conflicts": [],
    "network_transfer": false,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Missing target key is selected

Request:
```json
{
  "op": "anti_entropy_delta",
  "record": {
    "source": {
      "a": {
        "version": 1,
        "value": "x"
      }
    },
    "target": {}
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "send": [
      "a"
    ],
    "conflicts": [],
    "network_transfer": false,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Newer source version is selected

Request:
```json
{
  "op": "anti_entropy_delta",
  "record": {
    "source": {
      "a": {
        "version": 2,
        "value": "x"
      }
    },
    "target": {
      "a": {
        "version": 1,
        "value": "x"
      }
    }
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "send": [
      "a"
    ],
    "conflicts": [],
    "network_transfer": false,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Older source version is not sent

Request:
```json
{
  "op": "anti_entropy_delta",
  "record": {
    "source": {
      "a": {
        "version": 1,
        "value": "x"
      }
    },
    "target": {
      "a": {
        "version": 2,
        "value": "y"
      }
    }
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "send": [],
    "conflicts": [],
    "network_transfer": false,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Equal version contrary values are conflicts

Request:
```json
{
  "op": "anti_entropy_delta",
  "record": {
    "source": {
      "a": {
        "version": 2,
        "value": "x"
      }
    },
    "target": {
      "a": {
        "version": 2,
        "value": "y"
      }
    }
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "send": [],
    "conflicts": [
      "a"
    ],
    "network_transfer": false,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

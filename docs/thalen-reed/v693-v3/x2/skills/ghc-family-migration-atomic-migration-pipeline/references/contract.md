# atomic_migration_pipeline

Apply a bounded migration pipeline or expose the failure with the original record.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Rename followed by default injection commits as one preview

Request:
```json
{
  "op": "atomic_migration_pipeline",
  "record": {
    "old": 1
  },
  "args": {
    "rules": [
      {
        "op": "rename_preview",
        "args": {
          "mapping": {
            "old": "new"
          }
        }
      },
      {
        "op": "default_overlay",
        "args": {
          "defaults": {
            "flag": false
          }
        }
      }
    ],
    "allow_lossy": false
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "committed": true,
    "result": {
      "new": 1,
      "flag": false
    },
    "failed_index": null,
    "reason": null,
    "attempted_steps": 2,
    "rollback_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Refused numeric text returns the original record

Request:
```json
{
  "op": "atomic_migration_pipeline",
  "record": {
    "n": "03"
  },
  "args": {
    "rules": [
      {
        "op": "coercion_preview",
        "args": {
          "field": "n",
          "conversion": "text_to_integer"
        }
      }
    ],
    "allow_lossy": false
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "committed": false,
    "result": {
      "n": "03"
    },
    "failed_index": 0,
    "reason": "NONCANONICAL_INTEGER_TEXT",
    "attempted_steps": 1,
    "rollback_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Occupied rename destination aborts before a write

Request:
```json
{
  "op": "atomic_migration_pipeline",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "rules": [
      {
        "op": "rename_preview",
        "args": {
          "mapping": {
            "a": "b"
          }
        }
      }
    ],
    "allow_lossy": false
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "committed": false,
    "result": {
      "a": 1,
      "b": 2
    },
    "failed_index": 0,
    "reason": "destination_occupied:b",
    "attempted_steps": 1,
    "rollback_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## A later failed conversion rolls back an earlier default

Request:
```json
{
  "op": "atomic_migration_pipeline",
  "record": {
    "n": 1
  },
  "args": {
    "rules": [
      {
        "op": "default_overlay",
        "args": {
          "defaults": {
            "x": 0
          }
        }
      },
      {
        "op": "coercion_preview",
        "args": {
          "field": "n",
          "conversion": "boolean_to_text"
        }
      }
    ],
    "allow_lossy": false
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "committed": false,
    "result": {
      "n": 1
    },
    "failed_index": 1,
    "reason": "TYPE_MISMATCH",
    "attempted_steps": 2,
    "rollback_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Unacknowledged enum information loss aborts the pipeline

Request:
```json
{
  "op": "atomic_migration_pipeline",
  "record": {
    "status": "a",
    "keep": null
  },
  "args": {
    "rules": [
      {
        "op": "enum_mapping",
        "args": {
          "field": "status",
          "mapping": {
            "a": "x",
            "b": "x"
          }
        }
      }
    ],
    "allow_lossy": false
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "committed": false,
    "result": {
      "status": "a",
      "keep": null
    },
    "failed_index": 0,
    "reason": "LOSSY_ENUM_MAPPING",
    "attempted_steps": 1,
    "rollback_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

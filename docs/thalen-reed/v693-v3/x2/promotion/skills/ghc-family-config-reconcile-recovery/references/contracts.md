# Four retained source contracts

# rename_cycle_analysis

Separate rename cycles, chains, fixed points and duplicate targets.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A two-cycle needs simultaneous evaluation

Request:
```json
{
  "op": "rename_cycle_analysis",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "mapping": {
      "a": "b",
      "b": "a"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "cycles": [
      [
        "a",
        "b"
      ]
    ],
    "chains": [],
    "fixed_points": [],
    "duplicate_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## A rename chain terminates at a fresh target

Request:
```json
{
  "op": "rename_cycle_analysis",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "mapping": {
      "a": "b",
      "b": "c"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "cycles": [],
    "chains": [
      [
        "a",
        "b",
        "c"
      ]
    ],
    "fixed_points": [],
    "duplicate_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## A fixed point is distinct from a cycle

Request:
```json
{
  "op": "rename_cycle_analysis",
  "record": {
    "a": 1
  },
  "args": {
    "mapping": {
      "a": "a"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "cycles": [],
    "chains": [],
    "fixed_points": [
      "a"
    ],
    "duplicate_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## Independent rename chains remain separate

Request:
```json
{
  "op": "rename_cycle_analysis",
  "record": {
    "a": 1,
    "c": 2
  },
  "args": {
    "mapping": {
      "a": "b",
      "c": "d"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "cycles": [],
    "chains": [
      [
        "a",
        "b"
      ],
      [
        "c",
        "d"
      ]
    ],
    "fixed_points": [],
    "duplicate_targets": []
  },
  "error": null,
  "external_credit": false
}
```

## Converging chains expose a duplicate target

Request:
```json
{
  "op": "rename_cycle_analysis",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "mapping": {
      "a": "c",
      "b": "c"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "cycles": [],
    "chains": [
      [
        "a",
        "c"
      ],
      [
        "b",
        "c"
      ]
    ],
    "fixed_points": [],
    "duplicate_targets": [
      "c"
    ]
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.


---

# loss_snapshot

Retain exact removed and overwritten values in a recoverable source snapshot.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Removed integer values remain recoverable

Request:
```json
{
  "op": "loss_snapshot",
  "record": {
    "before": {
      "a": 1,
      "b": 2
    },
    "after": {
      "a": 1
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "removed": [
      {
        "field": "b",
        "value": 2
      }
    ],
    "overwritten": [],
    "added": [],
    "snapshot": {
      "a": 1,
      "b": 2
    },
    "reversible_from_snapshot": true
  },
  "error": null,
  "external_credit": false
}
```

## Boolean-to-integer replacement retains the prior type

Request:
```json
{
  "op": "loss_snapshot",
  "record": {
    "before": {
      "v": true
    },
    "after": {
      "v": 1
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "removed": [],
    "overwritten": [
      {
        "field": "v",
        "before": true,
        "after": 1
      }
    ],
    "added": [],
    "snapshot": {
      "v": true
    },
    "reversible_from_snapshot": true
  },
  "error": null,
  "external_credit": false
}
```

## A newly added null does not become a removed value

Request:
```json
{
  "op": "loss_snapshot",
  "record": {
    "before": {},
    "after": {
      "a": null
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "removed": [],
    "overwritten": [],
    "added": [
      {
        "field": "a",
        "value": null
      }
    ],
    "snapshot": {},
    "reversible_from_snapshot": true
  },
  "error": null,
  "external_credit": false
}
```

## Array replacement preserves the complete previous array

Request:
```json
{
  "op": "loss_snapshot",
  "record": {
    "before": {
      "arr": [
        1
      ]
    },
    "after": {
      "arr": [
        2
      ]
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "removed": [],
    "overwritten": [
      {
        "field": "arr",
        "before": [
          1
        ],
        "after": [
          2
        ]
      }
    ],
    "added": [],
    "snapshot": {
      "arr": [
        1
      ]
    },
    "reversible_from_snapshot": true
  },
  "error": null,
  "external_credit": false
}
```

## An unchanged record retains an explicit recovery snapshot

Request:
```json
{
  "op": "loss_snapshot",
  "record": {
    "before": {
      "v": null,
      "k": false
    },
    "after": {
      "v": null,
      "k": false
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "removed": [],
    "overwritten": [],
    "added": [],
    "snapshot": {
      "v": null,
      "k": false
    },
    "reversible_from_snapshot": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.


---

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


---

# correction_context

Append a correction only to its retained predecessor and matching source context.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A correction appends beside its rejected predecessor

Request:
```json
{
  "op": "correction_context",
  "record": {
    "prior": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "correction": {
      "id": "r2",
      "supersedes": "r1",
      "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "state": "represented"
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "accepted": true,
    "reason": null,
    "records": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      },
      {
        "id": "r2",
        "supersedes": "r1",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "state": "represented"
      }
    ],
    "predecessor_erased": false
  },
  "error": null,
  "external_credit": false
}
```

## A new source context cannot amend the old attempt

Request:
```json
{
  "op": "correction_context",
  "record": {
    "prior": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "correction": {
      "id": "r2",
      "supersedes": "r1",
      "context": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "state": "represented"
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "accepted": false,
    "reason": "STALE_CONTEXT",
    "records": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "predecessor_erased": false
  },
  "error": null,
  "external_credit": false
}
```

## An unknown predecessor prevents attachment

Request:
```json
{
  "op": "correction_context",
  "record": {
    "prior": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "correction": {
      "id": "r2",
      "supersedes": "missing",
      "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "state": "represented"
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "accepted": false,
    "reason": "UNKNOWN_PREDECESSOR",
    "records": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "predecessor_erased": false
  },
  "error": null,
  "external_credit": false
}
```

## A repeated correction identifier is refused

Request:
```json
{
  "op": "correction_context",
  "record": {
    "prior": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "correction": {
      "id": "r1",
      "supersedes": "r1",
      "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "state": "represented"
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "accepted": false,
    "reason": "DUPLICATE_ID",
    "records": [
      {
        "id": "r1",
        "state": "rejected",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "predecessor_erased": false
  },
  "error": null,
  "external_credit": false
}
```

## A held predecessor stays held after an additive correction

Request:
```json
{
  "op": "correction_context",
  "record": {
    "prior": [
      {
        "id": "r1",
        "state": "held",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      }
    ],
    "correction": {
      "id": "r2",
      "supersedes": "r1",
      "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "state": "represented"
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "represented",
  "value": {
    "accepted": true,
    "reason": null,
    "records": [
      {
        "id": "r1",
        "state": "held",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "retained": true
      },
      {
        "id": "r2",
        "supersedes": "r1",
        "context": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "state": "represented"
      }
    ],
    "predecessor_erased": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

# Bound handover contracts

## ghc-family-distributed-monotonic-reads-check

Source bindings:

- `x1/skills/ghc-family-distributed-monotonic-reads-check/SKILL.md` — `c5cb7ae51c1df21361c18fda10b78c21ca60d012f147605ee61014ce6d1f1e72`
- `x1/skills/ghc-family-distributed-monotonic-reads-check/references/contract.md` — `976a4ef4e27b8c0bf48eaf1c53050df09835fde49c5b1558f54ea76d47a51d93`

# monotonic_reads_check

Find logical-clock regressions in a finite synthetic read sequence.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## No reads have no regression

Request:
```json
{
  "op": "monotonic_reads_check",
  "record": {
    "reads": []
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
    "monotonic": true,
    "violations": [],
    "read_count": 0,
    "wall_time_claim": false
  },
  "error": null,
  "external_credit": false
}
```

## One read has no predecessor

Request:
```json
{
  "op": "monotonic_reads_check",
  "record": {
    "reads": [
      {
        "a": 1
      }
    ]
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
    "monotonic": true,
    "violations": [],
    "read_count": 1,
    "wall_time_claim": false
  },
  "error": null,
  "external_credit": false
}
```

## Equal clocks are monotonic

Request:
```json
{
  "op": "monotonic_reads_check",
  "record": {
    "reads": [
      {
        "a": 1
      },
      {
        "a": 1
      }
    ]
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
    "monotonic": true,
    "violations": [],
    "read_count": 2,
    "wall_time_claim": false
  },
  "error": null,
  "external_credit": false
}
```

## Increasing clocks are monotonic

Request:
```json
{
  "op": "monotonic_reads_check",
  "record": {
    "reads": [
      {
        "a": 1
      },
      {
        "a": 2
      },
      {
        "a": 2,
        "b": 1
      }
    ]
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
    "monotonic": true,
    "violations": [],
    "read_count": 3,
    "wall_time_claim": false
  },
  "error": null,
  "external_credit": false
}
```

## Concurrent and older reads expose regressions

Request:
```json
{
  "op": "monotonic_reads_check",
  "record": {
    "reads": [
      {
        "a": 1
      },
      {
        "b": 1
      },
      {
        "a": 0,
        "b": 1
      }
    ]
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
    "monotonic": false,
    "violations": [
      {
        "from": 0,
        "to": 1,
        "relation": "concurrent"
      }
    ],
    "read_count": 3,
    "wall_time_claim": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-bounded-staleness-check

Source bindings:

- `x1/skills/ghc-family-distributed-bounded-staleness-check/SKILL.md` — `6d5510af89ddce89591b9521e9434449f4e89c871ac11f53d06b9084b1f7ea17`
- `x1/skills/ghc-family-distributed-bounded-staleness-check/references/contract.md` — `49a870c561b68b2db125ebb25596b14c39fbf025fd38719293eb7f8b5a1827ac`

# bounded_staleness_check

Compare finite logical counter lag to an explicit bound without making latency claims.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Equal empty clocks are within zero

Request:
```json
{
  "op": "bounded_staleness_check",
  "record": {
    "committed": {},
    "observed": {}
  },
  "args": {
    "max_lag": 0
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "within_bound": true,
    "lag": {},
    "maximum": 0,
    "max_lag": 0,
    "logical_only": true
  },
  "error": null,
  "external_credit": false
}
```

## Equal actor clock is within zero

Request:
```json
{
  "op": "bounded_staleness_check",
  "record": {
    "committed": {
      "a": 2
    },
    "observed": {
      "a": 2
    }
  },
  "args": {
    "max_lag": 0
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "within_bound": true,
    "lag": {
      "a": 0
    },
    "maximum": 0,
    "max_lag": 0,
    "logical_only": true
  },
  "error": null,
  "external_credit": false
}
```

## One logical step is within one

Request:
```json
{
  "op": "bounded_staleness_check",
  "record": {
    "committed": {
      "a": 3
    },
    "observed": {
      "a": 2
    }
  },
  "args": {
    "max_lag": 1
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "within_bound": true,
    "lag": {
      "a": 1
    },
    "maximum": 1,
    "max_lag": 1,
    "logical_only": true
  },
  "error": null,
  "external_credit": false
}
```

## Two logical steps exceed one

Request:
```json
{
  "op": "bounded_staleness_check",
  "record": {
    "committed": {
      "a": 4
    },
    "observed": {
      "a": 2
    }
  },
  "args": {
    "max_lag": 1
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "within_bound": false,
    "lag": {
      "a": 2
    },
    "maximum": 2,
    "max_lag": 1,
    "logical_only": true
  },
  "error": null,
  "external_credit": false
}
```

## Actorwise lag retains the maximum

Request:
```json
{
  "op": "bounded_staleness_check",
  "record": {
    "committed": {
      "a": 4,
      "b": 5
    },
    "observed": {
      "a": 3,
      "b": 2
    }
  },
  "args": {
    "max_lag": 3
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "within_bound": true,
    "lag": {
      "a": 1,
      "b": 3
    },
    "maximum": 3,
    "max_lag": 3,
    "logical_only": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-accessible-consistency-summary

Source bindings:

- `x2/skills/ghc-family-distributed-accessible-consistency-summary/SKILL.md` — `acaa5b3bd3c003d10b967768a3d410ab13b84a6ad54c7a02bb6edbf7a2a7872b`
- `x2/skills/ghc-family-distributed-accessible-consistency-summary/references/contract.md` — `1a5c5e8e722d882c3b33d2033c45148e95bf01811dba578806bcf5f71431b604`

# accessible_consistency_summary

Represent literal consistency rows while reserving human accessibility evaluation.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Empty summary has explicit status

Request:
```json
{
  "op": "accessible_consistency_summary",
  "record": {
    "rows": []
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
    "rows": [],
    "row_count": 0,
    "uses_color_only": false,
    "status_text": "0 consistency rows",
    "manual_review": false,
    "assistive_technology_review": false
  },
  "error": null,
  "external_credit": false
}
```

## Consistent key is named literally

Request:
```json
{
  "op": "accessible_consistency_summary",
  "record": {
    "rows": [
      {
        "replica": "a",
        "key": "k",
        "state": "consistent",
        "detail": "version 2"
      }
    ]
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
    "rows": [
      {
        "replica": "a",
        "key": "k",
        "state": "consistent",
        "detail": "version 2"
      }
    ],
    "row_count": 1,
    "uses_color_only": false,
    "status_text": "1 consistency rows",
    "manual_review": false,
    "assistive_technology_review": false
  },
  "error": null,
  "external_credit": false
}
```

## Conflict row names the contrary state

Request:
```json
{
  "op": "accessible_consistency_summary",
  "record": {
    "rows": [
      {
        "replica": "b",
        "key": "k",
        "state": "conflict",
        "detail": "equal version different value"
      }
    ]
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
    "rows": [
      {
        "replica": "b",
        "key": "k",
        "state": "conflict",
        "detail": "equal version different value"
      }
    ],
    "row_count": 1,
    "uses_color_only": false,
    "status_text": "1 consistency rows",
    "manual_review": false,
    "assistive_technology_review": false
  },
  "error": null,
  "external_credit": false
}
```

## Missing key is not shown as null

Request:
```json
{
  "op": "accessible_consistency_summary",
  "record": {
    "rows": [
      {
        "replica": "c",
        "key": "k",
        "state": "missing",
        "detail": "no observation"
      }
    ]
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
    "rows": [
      {
        "replica": "c",
        "key": "k",
        "state": "missing",
        "detail": "no observation"
      }
    ],
    "row_count": 1,
    "uses_color_only": false,
    "status_text": "1 consistency rows",
    "manual_review": false,
    "assistive_technology_review": false
  },
  "error": null,
  "external_credit": false
}
```

## Multiple rows retain stable input order

Request:
```json
{
  "op": "accessible_consistency_summary",
  "record": {
    "rows": [
      {
        "replica": "a",
        "key": "x",
        "state": "consistent",
        "detail": "v1"
      },
      {
        "replica": "b",
        "key": "y",
        "state": "behind",
        "detail": "lag 2"
      }
    ]
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
    "rows": [
      {
        "replica": "a",
        "key": "x",
        "state": "consistent",
        "detail": "v1"
      },
      {
        "replica": "b",
        "key": "y",
        "state": "behind",
        "detail": "lag 2"
      }
    ],
    "row_count": 2,
    "uses_color_only": false,
    "status_text": "2 consistency rows",
    "manual_review": false,
    "assistive_technology_review": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-handover-snapshot-projection

Source bindings:

- `x2/skills/ghc-family-distributed-handover-snapshot-projection/SKILL.md` — `0dfb9fc9321099d7fbdacdf5dbdb0168ac5a75dc8cbe72f0a5b550170b9b1cb8`
- `x2/skills/ghc-family-distributed-handover-snapshot-projection/references/contract.md` — `3e6035878a28fe4728b67cc08b6c7b1806c857f7f25383fff6d733012cbfad74`

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

Same-owner synthetic integration evidence only. No external deployment, independent reproduction, scientific, professional, legal, cultural, Maori, affected-party, identity, complete privacy or accessibility, exhaustive security, production or Stage 20 credit. NOT_READY_FOR_STAGE_20.

# Corrected raw-core contract set

The failed v1 skill and runner remain unchanged. This v2 package reuses the exact validated operation contracts and changes only the core byte-copy dependency.

Original contract SHA-256: `7c6045aadc1279fbb0a9150538b16d91816a0189e382808475c8c3e0594406c8`

# Bound repair contracts

## ghc-family-distributed-anti-entropy-delta

Source bindings:

- `x2/skills/ghc-family-distributed-anti-entropy-delta/SKILL.md` — `1f0906bd33b30a31ce710a95b711e22fbb90b7dedcc557002cf5ee7927f068f1`
- `x2/skills/ghc-family-distributed-anti-entropy-delta/references/contract.md` — `b76a01b29c725f49bf295eb27e06175cfc54105d22a1875c19425096ba2b030d`

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

## ghc-family-distributed-delta-application-guard

Source bindings:

- `x2/skills/ghc-family-distributed-delta-application-guard/SKILL.md` — `a58a62afdb77e6cbbddf82780b88e20c1829762eb537233e4faaf5b46d92ab4a`
- `x2/skills/ghc-family-distributed-delta-application-guard/references/contract.md` — `98a5206e6040e8e8e564fbe7a2d649caf4f3dd1070a3254548ed0bbe4b8bcb25`

# delta_application_guard

Preview a delta only when its source digest and next sequence exactly match.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Matching digest and sequence add a value

Request:
```json
{
  "op": "delta_application_guard",
  "record": {
    "a": 1
  },
  "args": {
    "delta": {
      "base_digest": "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862",
      "sequence": 2,
      "changes": {
        "b": {
          "value": 2
        }
      }
    },
    "current_sequence": 1
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": true,
    "result": {
      "a": 1,
      "b": 2
    },
    "reason": null,
    "actual_base_digest": "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862",
    "next_sequence": 2,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Matching digest and sequence remove a value

Request:
```json
{
  "op": "delta_application_guard",
  "record": {
    "a": 1,
    "b": 2
  },
  "args": {
    "delta": {
      "base_digest": "43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777",
      "sequence": 1,
      "changes": {
        "b": {
          "remove": true
        }
      }
    },
    "current_sequence": 0
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": true,
    "result": {
      "a": 1
    },
    "reason": null,
    "actual_base_digest": "43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777",
    "next_sequence": 1,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Wrong base digest preserves source

Request:
```json
{
  "op": "delta_application_guard",
  "record": {
    "a": 1
  },
  "args": {
    "delta": {
      "base_digest": "0000000000000000000000000000000000000000000000000000000000000000",
      "sequence": 2,
      "changes": {
        "b": {
          "value": 2
        }
      }
    },
    "current_sequence": 1
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": false,
    "result": {
      "a": 1
    },
    "reason": "BASE_DIGEST",
    "actual_base_digest": "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862",
    "next_sequence": 1,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Skipped sequence preserves source

Request:
```json
{
  "op": "delta_application_guard",
  "record": {
    "a": 1
  },
  "args": {
    "delta": {
      "base_digest": "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862",
      "sequence": 3,
      "changes": {
        "b": {
          "value": 2
        }
      }
    },
    "current_sequence": 1
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": false,
    "result": {
      "a": 1
    },
    "reason": "SEQUENCE",
    "actual_base_digest": "015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862",
    "next_sequence": 1,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Empty next delta is an explicit no-op

Request:
```json
{
  "op": "delta_application_guard",
  "record": {},
  "args": {
    "delta": {
      "base_digest": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
      "sequence": 1,
      "changes": {}
    },
    "current_sequence": 0
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "applied": true,
    "result": {},
    "reason": null,
    "actual_base_digest": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
    "next_sequence": 1,
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-tombstone-retention-check

Source bindings:

- `x2/skills/ghc-family-distributed-tombstone-retention-check/SKILL.md` — `93df84e52a6b9220b06eba440077a3bb95d8219c3f391c1bf8cca61da65fe5b2`
- `x2/skills/ghc-family-distributed-tombstone-retention-check/references/contract.md` — `f622f985090df77d716157302d93a3438b7810956e397947909cf9c49f73db3d`

# tombstone_retention_check

Keep a tombstone until every required synthetic replica acknowledges its clock.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## No required replicas allow bounded collection

Request:
```json
{
  "op": "tombstone_retention_check",
  "record": {
    "clock": {
      "a": 1
    },
    "acknowledgements": {},
    "required": []
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
    "retain": false,
    "safe_to_collect": true,
    "missing": [],
    "behind": [],
    "required": [],
    "production_collection": false
  },
  "error": null,
  "external_credit": false
}
```

## One equal acknowledgement covers the tombstone

Request:
```json
{
  "op": "tombstone_retention_check",
  "record": {
    "clock": {
      "a": 1
    },
    "acknowledgements": {
      "r1": {
        "a": 1
      }
    },
    "required": [
      "r1"
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
    "retain": false,
    "safe_to_collect": true,
    "missing": [],
    "behind": [],
    "required": [
      "r1"
    ],
    "production_collection": false
  },
  "error": null,
  "external_credit": false
}
```

## A missing required replica retains it

Request:
```json
{
  "op": "tombstone_retention_check",
  "record": {
    "clock": {
      "a": 1
    },
    "acknowledgements": {
      "r1": {
        "a": 1
      }
    },
    "required": [
      "r1",
      "r2"
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
    "retain": true,
    "safe_to_collect": false,
    "missing": [
      "r2"
    ],
    "behind": [],
    "required": [
      "r1",
      "r2"
    ],
    "production_collection": false
  },
  "error": null,
  "external_credit": false
}
```

## A behind acknowledgement retains it

Request:
```json
{
  "op": "tombstone_retention_check",
  "record": {
    "clock": {
      "a": 2
    },
    "acknowledgements": {
      "r1": {
        "a": 1
      }
    },
    "required": [
      "r1"
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
    "retain": true,
    "safe_to_collect": false,
    "missing": [],
    "behind": [
      "r1"
    ],
    "required": [
      "r1"
    ],
    "production_collection": false
  },
  "error": null,
  "external_credit": false
}
```

## Actorwise acknowledgements must dominate

Request:
```json
{
  "op": "tombstone_retention_check",
  "record": {
    "clock": {
      "a": 1,
      "b": 2
    },
    "acknowledgements": {
      "r1": {
        "a": 1,
        "b": 2
      },
      "r2": {
        "a": 2,
        "b": 2
      }
    },
    "required": [
      "r2",
      "r1"
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
    "retain": false,
    "safe_to_collect": true,
    "missing": [],
    "behind": [],
    "required": [
      "r1",
      "r2"
    ],
    "production_collection": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-repair-plan-toposort

Source bindings:

- `x2/skills/ghc-family-distributed-repair-plan-toposort/SKILL.md` — `c9624c19e7e0dfd5e23487dc7a73b430aa46ea7c0d185c72d07bde388073e641`
- `x2/skills/ghc-family-distributed-repair-plan-toposort/references/contract.md` — `cff81aa01ae621651022fb917a964b363cbfb654a26232579f4cea7a5ebc31ee`

# repair_plan_toposort

Order finite repair steps while exposing missing requirements and cycles.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Empty repair plan is ready

Request:
```json
{
  "op": "repair_plan_toposort",
  "record": {
    "steps": []
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
    "ready": true,
    "order": [],
    "missing": [],
    "cycle_members": [],
    "executed": false
  },
  "error": null,
  "external_credit": false
}
```

## One independent step is ready

Request:
```json
{
  "op": "repair_plan_toposort",
  "record": {
    "steps": [
      {
        "id": "inspect",
        "requires": []
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
    "ready": true,
    "order": [
      "inspect"
    ],
    "missing": [],
    "cycle_members": [],
    "executed": false
  },
  "error": null,
  "external_credit": false
}
```

## Dependencies determine order

Request:
```json
{
  "op": "repair_plan_toposort",
  "record": {
    "steps": [
      {
        "id": "verify",
        "requires": [
          "apply"
        ]
      },
      {
        "id": "apply",
        "requires": [
          "inspect"
        ]
      },
      {
        "id": "inspect",
        "requires": []
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
    "ready": true,
    "order": [
      "inspect",
      "apply",
      "verify"
    ],
    "missing": [],
    "cycle_members": [],
    "executed": false
  },
  "error": null,
  "external_credit": false
}
```

## Missing prerequisite holds the plan

Request:
```json
{
  "op": "repair_plan_toposort",
  "record": {
    "steps": [
      {
        "id": "apply",
        "requires": [
          "approve"
        ]
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
    "ready": false,
    "order": [],
    "missing": [
      "approve"
    ],
    "cycle_members": [],
    "executed": false
  },
  "error": null,
  "external_credit": false
}
```

## Repair cycle remains held

Request:
```json
{
  "op": "repair_plan_toposort",
  "record": {
    "steps": [
      {
        "id": "a",
        "requires": [
          "b"
        ]
      },
      {
        "id": "b",
        "requires": [
          "a"
        ]
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
    "ready": false,
    "order": [],
    "missing": [],
    "cycle_members": [
      "a",
      "b"
    ],
    "executed": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

Same-owner synthetic integration evidence only. No external deployment, independent reproduction, scientific, professional, legal, cultural, Maori, affected-party, identity, complete privacy or accessibility, exhaustive security, production or Stage 20 credit. NOT_READY_FOR_STAGE_20.

Additive correction with the failed v1 entry points retained byte-for-byte. Same-owner synthetic integration evidence only; no independent reproduction, deployment, authority, complete privacy or accessibility, exhaustive security, or Stage 20 credit.

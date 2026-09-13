# Bound clocks contracts

## ghc-family-distributed-vector-compare

Source bindings:

- `x1/skills/ghc-family-distributed-vector-compare/SKILL.md` — `a573c3b83b23ded602a30d316b3842a4431ba401bd15b40250e75df61cfe26f0`
- `x1/skills/ghc-family-distributed-vector-compare/references/contract.md` — `55fdc003317da83dbe3703039eb2a8380659c1a2d57c17582948231a5430ff36`

# vector_clock_compare

Compare two finite logical clocks without inferring wall time or physical causality.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Equal empty clocks remain equal

Request:
```json
{
  "op": "vector_clock_compare",
  "record": {
    "left": {},
    "right": {}
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
    "relation": "equal",
    "actors": [],
    "incomparable": false
  },
  "error": null,
  "external_credit": false
}
```

## One actor increment is after

Request:
```json
{
  "op": "vector_clock_compare",
  "record": {
    "left": {
      "a": 2
    },
    "right": {
      "a": 1
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
    "relation": "after",
    "actors": [
      "a"
    ],
    "incomparable": false
  },
  "error": null,
  "external_credit": false
}
```

## A lower observation is before

Request:
```json
{
  "op": "vector_clock_compare",
  "record": {
    "left": {
      "a": 1,
      "b": 0
    },
    "right": {
      "a": 1,
      "b": 2
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
    "relation": "before",
    "actors": [
      "a",
      "b"
    ],
    "incomparable": false
  },
  "error": null,
  "external_credit": false
}
```

## Contrary actor advances are concurrent

Request:
```json
{
  "op": "vector_clock_compare",
  "record": {
    "left": {
      "a": 2,
      "b": 1
    },
    "right": {
      "a": 1,
      "b": 2
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
    "relation": "concurrent",
    "actors": [
      "a",
      "b"
    ],
    "incomparable": true
  },
  "error": null,
  "external_credit": false
}
```

## An absent actor component is logical zero

Request:
```json
{
  "op": "vector_clock_compare",
  "record": {
    "left": {
      "a": 1
    },
    "right": {
      "a": 1,
      "b": 1
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
    "relation": "before",
    "actors": [
      "a",
      "b"
    ],
    "incomparable": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-vector-join

Source bindings:

- `x1/skills/ghc-family-distributed-vector-join/SKILL.md` — `765cbae2e7fdb73e7b7222789bc32c5503cfc42fe52309466bf72b4269cef333`
- `x1/skills/ghc-family-distributed-vector-join/references/contract.md` — `7eb88fff2c3e834318f66c41d7634dbaae04ff26bd8a8d71819ffb990273e2ae`

# vector_clock_join

Compute a componentwise finite clock join with explicit actor coverage.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Two empty clocks join to empty

Request:
```json
{
  "op": "vector_clock_join",
  "record": {
    "clocks": [
      {},
      {}
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
    "clock": {},
    "actors": [],
    "input_count": 2,
    "dominates_all": true
  },
  "error": null,
  "external_credit": false
}
```

## Disjoint actors are retained

Request:
```json
{
  "op": "vector_clock_join",
  "record": {
    "clocks": [
      {
        "a": 1
      },
      {
        "b": 2
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
    "clock": {
      "a": 1,
      "b": 2
    },
    "actors": [
      "a",
      "b"
    ],
    "input_count": 2,
    "dominates_all": true
  },
  "error": null,
  "external_credit": false
}
```

## Largest component is retained per actor

Request:
```json
{
  "op": "vector_clock_join",
  "record": {
    "clocks": [
      {
        "a": 3,
        "b": 1
      },
      {
        "a": 2,
        "b": 4
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
    "clock": {
      "a": 3,
      "b": 4
    },
    "actors": [
      "a",
      "b"
    ],
    "input_count": 2,
    "dominates_all": true
  },
  "error": null,
  "external_credit": false
}
```

## Duplicate clocks do not inflate counters

Request:
```json
{
  "op": "vector_clock_join",
  "record": {
    "clocks": [
      {
        "a": 2
      },
      {
        "a": 2
      },
      {
        "a": 2
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
    "clock": {
      "a": 2
    },
    "actors": [
      "a"
    ],
    "input_count": 3,
    "dominates_all": true
  },
  "error": null,
  "external_credit": false
}
```

## Zero components remain explicit

Request:
```json
{
  "op": "vector_clock_join",
  "record": {
    "clocks": [
      {
        "a": 0,
        "b": 1
      },
      {
        "a": 2,
        "b": 0
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
    "clock": {
      "a": 2,
      "b": 1
    },
    "actors": [
      "a",
      "b"
    ],
    "input_count": 2,
    "dominates_all": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-dotted-event-validation

Source bindings:

- `x1/skills/ghc-family-distributed-dotted-event-validation/SKILL.md` — `875b9f8725e20061df195e951075ab07d9d1d02204afce578fec93aab0c0c3bd`
- `x1/skills/ghc-family-distributed-dotted-event-validation/references/contract.md` — `ec8758df99386a120a1e6d25790bb67a26613ee2d642d8f2ce949792ef711747`

# dotted_event_validation

Check whether one synthetic event dot is the next local actor event after its context.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## First actor event follows empty context

Request:
```json
{
  "op": "dotted_event_validation",
  "record": {
    "context": {},
    "dot": {
      "actor": "a",
      "counter": 1
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
    "accepted": true,
    "reason": null,
    "next_clock": {
      "a": 1
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Next actor counter advances exactly once

Request:
```json
{
  "op": "dotted_event_validation",
  "record": {
    "context": {
      "a": 2,
      "b": 1
    },
    "dot": {
      "actor": "a",
      "counter": 3
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
    "accepted": true,
    "reason": null,
    "next_clock": {
      "a": 3,
      "b": 1
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Repeated actor counter is refused

Request:
```json
{
  "op": "dotted_event_validation",
  "record": {
    "context": {
      "a": 2
    },
    "dot": {
      "actor": "a",
      "counter": 2
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
    "accepted": false,
    "reason": "DOT_NOT_NEXT",
    "next_clock": {
      "a": 2
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Skipped actor counter is refused

Request:
```json
{
  "op": "dotted_event_validation",
  "record": {
    "context": {
      "a": 2
    },
    "dot": {
      "actor": "a",
      "counter": 4
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
    "accepted": false,
    "reason": "DOT_NOT_NEXT",
    "next_clock": {
      "a": 2
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Other actor context remains unchanged

Request:
```json
{
  "op": "dotted_event_validation",
  "record": {
    "context": {
      "a": 0,
      "b": 5
    },
    "dot": {
      "actor": "a",
      "counter": 1
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
    "accepted": true,
    "reason": null,
    "next_clock": {
      "a": 1,
      "b": 5
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-read-your-writes-check

Source bindings:

- `x1/skills/ghc-family-distributed-read-your-writes-check/SKILL.md` — `f3c345d433d14304749b562bae2b4eaaa7c86e0aa425157d18246b55e1cd5203`
- `x1/skills/ghc-family-distributed-read-your-writes-check/references/contract.md` — `0f657de651d56223aaf1ee016f14b3ee43a95c473383aaaee5aa20dea7d85f27`

# read_your_writes_check

Check whether one synthetic observation dominates a declared session write clock.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Empty session requirement is satisfied

Request:
```json
{
  "op": "read_your_writes_check",
  "record": {
    "write_clock": {},
    "observed_clock": {}
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
    "satisfied": true,
    "deficits": [],
    "actors": [],
    "empirical_latency": false
  },
  "error": null,
  "external_credit": false
}
```

## Equal observation satisfies the write

Request:
```json
{
  "op": "read_your_writes_check",
  "record": {
    "write_clock": {
      "a": 2
    },
    "observed_clock": {
      "a": 2
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
    "satisfied": true,
    "deficits": [],
    "actors": [
      "a"
    ],
    "empirical_latency": false
  },
  "error": null,
  "external_credit": false
}
```

## Newer observation satisfies the write

Request:
```json
{
  "op": "read_your_writes_check",
  "record": {
    "write_clock": {
      "a": 2
    },
    "observed_clock": {
      "a": 3,
      "b": 1
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
    "satisfied": true,
    "deficits": [],
    "actors": [
      "a",
      "b"
    ],
    "empirical_latency": false
  },
  "error": null,
  "external_credit": false
}
```

## Older observation exposes one deficit

Request:
```json
{
  "op": "read_your_writes_check",
  "record": {
    "write_clock": {
      "a": 2
    },
    "observed_clock": {
      "a": 1
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
    "satisfied": false,
    "deficits": [
      {
        "actor": "a",
        "required": 2,
        "observed": 1
      }
    ],
    "actors": [
      "a"
    ],
    "empirical_latency": false
  },
  "error": null,
  "external_credit": false
}
```

## Missing actor observation is zero

Request:
```json
{
  "op": "read_your_writes_check",
  "record": {
    "write_clock": {
      "a": 1,
      "b": 2
    },
    "observed_clock": {
      "a": 1
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
    "satisfied": false,
    "deficits": [
      {
        "actor": "b",
        "required": 2,
        "observed": 0
      }
    ],
    "actors": [
      "a",
      "b"
    ],
    "empirical_latency": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

Same-owner synthetic integration evidence only. No external deployment, independent reproduction, scientific, professional, legal, cultural, Maori, affected-party, identity, complete privacy or accessibility, exhaustive security, production or Stage 20 credit. NOT_READY_FOR_STAGE_20.

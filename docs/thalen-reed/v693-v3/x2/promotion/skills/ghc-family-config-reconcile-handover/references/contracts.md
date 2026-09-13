# Four retained source contracts

# unknown_field_projection

Project declared fields while retaining unknown fields in quarantine.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A known field is selected and its neighbour quarantined

Request:
```json
{
  "op": "unknown_field_projection",
  "record": {
    "known": 1,
    "extra": 2
  },
  "args": {
    "allowed": [
      "known"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "selected": {
      "known": 1
    },
    "quarantine": {
      "extra": 2
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## Explicit null stays selected

Request:
```json
{
  "op": "unknown_field_projection",
  "record": {
    "n": null,
    "x": false
  },
  "args": {
    "allowed": [
      "n"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "selected": {
      "n": null
    },
    "quarantine": {
      "x": false
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## An empty allowlist quarantines all data

Request:
```json
{
  "op": "unknown_field_projection",
  "record": {
    "a": [
      1
    ],
    "b": {}
  },
  "args": {
    "allowed": []
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "selected": {},
    "quarantine": {
      "a": [
        1
      ],
      "b": {}
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## All declared fields remain in the selected view

Request:
```json
{
  "op": "unknown_field_projection",
  "record": {
    "a": 1,
    "b": "two"
  },
  "args": {
    "allowed": [
      "b",
      "a"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "selected": {
      "a": 1,
      "b": "two"
    },
    "quarantine": {},
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

## An absent allowed field is not invented

Request:
```json
{
  "op": "unknown_field_projection",
  "record": {
    "existing": true
  },
  "args": {
    "allowed": [
      "absent"
    ]
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "selected": {},
    "quarantine": {
      "existing": true
    },
    "source_preserved": true
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.


---

# accessible_resolution_summary

Represent concrete conflict and resolution rows without claiming human review.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Literal field summary for unilateral edit

Request:
```json
{
  "op": "accessible_resolution_summary",
  "record": {
    "base": {
      "v": 1,
      "k": 0
    },
    "left": {
      "v": 2,
      "k": 0
    },
    "right": {
      "v": 1,
      "k": 0
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
    "rows": [
      {
        "field": "k",
        "state": "resolved_unchanged"
      },
      {
        "field": "v",
        "state": "resolved_left"
      }
    ],
    "conflicts": 0,
    "manual_review": false,
    "operator_decision": false
  },
  "error": null,
  "external_credit": false
}
```

## Literal field summary for equal edits

Request:
```json
{
  "op": "accessible_resolution_summary",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 2
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
    "rows": [
      {
        "field": "v",
        "state": "resolved_both"
      }
    ],
    "conflicts": 0,
    "manual_review": false,
    "operator_decision": false
  },
  "error": null,
  "external_credit": false
}
```

## Literal field summary for different edits

Request:
```json
{
  "op": "accessible_resolution_summary",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 3
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
    "rows": [
      {
        "field": "v",
        "state": "different_edits"
      }
    ],
    "conflicts": 1,
    "manual_review": false,
    "operator_decision": false
  },
  "error": null,
  "external_credit": false
}
```

## Literal field summary for delete versus modify

Request:
```json
{
  "op": "accessible_resolution_summary",
  "record": {
    "base": {
      "v": 1
    },
    "left": {},
    "right": {
      "v": 2
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
    "rows": [
      {
        "field": "v",
        "state": "delete_modify"
      }
    ],
    "conflicts": 1,
    "manual_review": false,
    "operator_decision": false
  },
  "error": null,
  "external_credit": false
}
```

## Literal field summary for contrary additions

Request:
```json
{
  "op": "accessible_resolution_summary",
  "record": {
    "base": {},
    "left": {
      "v": null
    },
    "right": {
      "v": false
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
    "rows": [
      {
        "field": "v",
        "state": "concurrent_add"
      }
    ],
    "conflicts": 1,
    "manual_review": false,
    "operator_decision": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.


---

# external_migration_evidence

Expose missing external migration evidence without promoting local assertions.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Absent operator evidence remains an open gap

Request:
```json
{
  "op": "external_migration_evidence",
  "record": {
    "requirements": [
      "operator"
    ],
    "evidence": {}
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "missing": [
      "operator"
    ],
    "provided": [],
    "external_qualified": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## A synthetic compatibility note does not supply rollback evidence

Request:
```json
{
  "op": "external_migration_evidence",
  "record": {
    "requirements": [
      "compatibility",
      "rollback"
    ],
    "evidence": {
      "compatibility": {
        "class": "synthetic"
      }
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "missing": [
      "rollback"
    ],
    "provided": [
      "compatibility"
    ],
    "external_qualified": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## Null human review is still absent

Request:
```json
{
  "op": "external_migration_evidence",
  "record": {
    "requirements": [
      "human_review"
    ],
    "evidence": {
      "human_review": null
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "missing": [
      "human_review"
    ],
    "provided": [],
    "external_qualified": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## Same-owner review is present metadata without independent qualification

Request:
```json
{
  "op": "external_migration_evidence",
  "record": {
    "requirements": [
      "independent_review"
    ],
    "evidence": {
      "independent_review": {
        "class": "same_owner"
      }
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "missing": [],
    "provided": [
      "independent_review"
    ],
    "external_qualified": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

## Rights and Maori authority require competent external evidence

Request:
```json
{
  "op": "external_migration_evidence",
  "record": {
    "requirements": [
      "rights",
      "maori_authority"
    ],
    "evidence": {
      "rights": null,
      "maori_authority": null
    }
  },
  "args": {}
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "open_gap",
  "value": {
    "missing": [
      "maori_authority",
      "rights"
    ],
    "provided": [],
    "external_qualified": false,
    "release": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.


---

# operator_release_gate

Keep deployment and publication held despite self-declared permissions.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## Reserve deploy despite local permission assertions

Request:
```json
{
  "op": "operator_release_gate",
  "record": {
    "target": "synthetic-config-A",
    "authority": null,
    "evidence": null
  },
  "args": {
    "requested": "deploy"
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "deploy",
    "target": "synthetic-config-A",
    "required": [
      "competent_operator",
      "external_validation",
      "rollback_evidence"
    ],
    "released": false,
    "assertions_verified": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve publish despite local permission assertions

Request:
```json
{
  "op": "operator_release_gate",
  "record": {
    "target": "synthetic-config-B",
    "authority": {
      "declared": true
    },
    "evidence": null
  },
  "args": {
    "requested": "publish"
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "publish",
    "target": "synthetic-config-B",
    "required": [
      "rights_holder",
      "affected_people",
      "privacy_review"
    ],
    "released": false,
    "assertions_verified": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve replace despite local permission assertions

Request:
```json
{
  "op": "operator_release_gate",
  "record": {
    "target": "synthetic-config-C",
    "authority": null,
    "evidence": {
      "declared": true
    }
  },
  "args": {
    "requested": "replace"
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "replace",
    "target": "synthetic-config-C",
    "required": [
      "competent_operator",
      "exact_target",
      "recoverable_source"
    ],
    "released": false,
    "assertions_verified": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve delete despite local permission assertions

Request:
```json
{
  "op": "operator_release_gate",
  "record": {
    "target": "synthetic-config-D",
    "authority": {
      "declared": true
    },
    "evidence": {
      "declared": true
    }
  },
  "args": {
    "requested": "delete"
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "delete",
    "target": "synthetic-config-D",
    "required": [
      "exact_destructive_authority",
      "recoverable_source"
    ],
    "released": false,
    "assertions_verified": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve maori_label despite local permission assertions

Request:
```json
{
  "op": "operator_release_gate",
  "record": {
    "target": "synthetic-config-E",
    "authority": null,
    "evidence": {
      "declared": true
    }
  },
  "args": {
    "requested": "maori_label"
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "maori_label",
    "target": "synthetic-config-E",
    "required": [
      "maori_authority",
      "affected_people"
    ],
    "released": false,
    "assertions_verified": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

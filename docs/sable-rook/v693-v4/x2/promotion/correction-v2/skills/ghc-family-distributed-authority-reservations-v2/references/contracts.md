# Corrected raw-core contract set

The failed v1 skill and runner remain unchanged. This v2 package reuses the exact validated operation contracts and changes only the core byte-copy dependency.

Original contract SHA-256: `fd8987bb8f2cc151e65865d1793e6a91cf1db501ae2639f8ff3e63b0247aa529`

# Bound authority contracts

## ghc-family-distributed-lease-epoch-fence

Source bindings:

- `x2/skills/ghc-family-distributed-lease-epoch-fence/SKILL.md` — `798aa1b0b1f8bbb60d64f30b9624d30c105a456978c54e8019030d69fdb768c1`
- `x2/skills/ghc-family-distributed-lease-epoch-fence/references/contract.md` — `1a28e15dcbeeb38d68538a2cd2722b91a180b326b3b53d3582367e068ae8ea64`

# lease_epoch_fence

Reject stale epoch or wrong-holder requests without claiming a production lock.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Matching holder and epoch is structurally accepted

Request:
```json
{
  "op": "lease_epoch_fence",
  "record": {
    "current_epoch": 3,
    "current_holder": "a",
    "request": {
      "epoch": 3,
      "holder": "a",
      "action": "preview"
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
    "current_epoch": 3,
    "current_holder": "a",
    "requested_action": "preview",
    "external_lock": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Older epoch is rejected

Request:
```json
{
  "op": "lease_epoch_fence",
  "record": {
    "current_epoch": 3,
    "current_holder": "a",
    "request": {
      "epoch": 2,
      "holder": "a",
      "action": "preview"
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
    "reason": "STALE_EPOCH",
    "current_epoch": 3,
    "current_holder": "a",
    "requested_action": "preview",
    "external_lock": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Future unissued epoch is rejected

Request:
```json
{
  "op": "lease_epoch_fence",
  "record": {
    "current_epoch": 3,
    "current_holder": "a",
    "request": {
      "epoch": 4,
      "holder": "a",
      "action": "preview"
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
    "reason": "STALE_EPOCH",
    "current_epoch": 3,
    "current_holder": "a",
    "requested_action": "preview",
    "external_lock": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Wrong holder is rejected

Request:
```json
{
  "op": "lease_epoch_fence",
  "record": {
    "current_epoch": 3,
    "current_holder": "a",
    "request": {
      "epoch": 3,
      "holder": "b",
      "action": "preview"
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
    "reason": "WRONG_HOLDER",
    "current_epoch": 3,
    "current_holder": "a",
    "requested_action": "preview",
    "external_lock": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Zero epoch can be explicit

Request:
```json
{
  "op": "lease_epoch_fence",
  "record": {
    "current_epoch": 0,
    "current_holder": "root",
    "request": {
      "epoch": 0,
      "holder": "root",
      "action": "read"
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
    "current_epoch": 0,
    "current_holder": "root",
    "requested_action": "read",
    "external_lock": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-causal-claim-firewall

Source bindings:

- `x2/skills/ghc-family-distributed-causal-claim-firewall/SKILL.md` — `fe7abc686b91e65ca02d6e0077ba10e0ce4d3e297c2f8606301215934d378ced`
- `x2/skills/ghc-family-distributed-causal-claim-firewall/references/contract.md` — `2bb0f8019e211cdf5997670aa4db398c75cfd19b0fab2d858a09efb1ccfa7216`

# causal_claim_firewall

Refuse conversion of software structure into empirical, identity, authority, or Stage 20 claims.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Refuse empirical_gmut promotion from local software

Request:
```json
{
  "op": "causal_claim_firewall",
  "record": {
    "claim": "empirical_gmut",
    "software_evidence": [
      "synthetic",
      "same_owner"
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
    "claim": "empirical_gmut",
    "permitted": false,
    "required": [
      "real_data",
      "frozen_analysis",
      "uncertainty",
      "independent_review"
    ],
    "software_credit_only": true,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Refuse professional_effectiveness promotion from local software

Request:
```json
{
  "op": "causal_claim_firewall",
  "record": {
    "claim": "professional_effectiveness",
    "software_evidence": [
      "synthetic",
      "same_owner"
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
    "claim": "professional_effectiveness",
    "permitted": false,
    "required": [
      "real_operators",
      "preregistered_comparison",
      "safety_monitoring",
      "independent_review"
    ],
    "software_credit_only": true,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Refuse production_identity promotion from local software

Request:
```json
{
  "op": "causal_claim_firewall",
  "record": {
    "claim": "production_identity",
    "software_evidence": [
      "synthetic",
      "same_owner"
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
    "claim": "production_identity",
    "permitted": false,
    "required": [
      "real_keys",
      "interoperability",
      "privacy_security_review",
      "trust_governance"
    ],
    "software_credit_only": true,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Refuse consciousness_personhood promotion from local software

Request:
```json
{
  "op": "causal_claim_firewall",
  "record": {
    "claim": "consciousness_personhood",
    "software_evidence": [
      "synthetic",
      "same_owner"
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
    "claim": "consciousness_personhood",
    "permitted": false,
    "required": [
      "independent_valid_evidence",
      "competent_interpretation"
    ],
    "software_credit_only": true,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Refuse stage20 promotion from local software

Request:
```json
{
  "op": "causal_claim_firewall",
  "record": {
    "claim": "stage20",
    "software_evidence": [
      "synthetic",
      "same_owner"
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
    "claim": "stage20",
    "permitted": false,
    "required": [
      "all_declared_external_gates",
      "independent_review",
      "authority"
    ],
    "software_credit_only": true,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

## ghc-family-distributed-real-cluster-observation-gate

Source bindings:

- `x2/skills/ghc-family-distributed-real-cluster-observation-gate/SKILL.md` — `9bdea4768eb28d28f8aa714ec784b56852fcc1b879009d812cf9fe91d2db07f5`
- `x2/skills/ghc-family-distributed-real-cluster-observation-gate/references/contract.md` — `866e98c8388ed6481180b6e503e5e87d8b0355822fdee3eab9de4e2641366f71`

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

## ghc-family-distributed-release-authority-gate

Source bindings:

- `x2/skills/ghc-family-distributed-release-authority-gate/SKILL.md` — `29cc17d362ef8b1954fedb3d42d9ea407e4732602f47a7b6d88c020c9df514e8`
- `x2/skills/ghc-family-distributed-release-authority-gate/references/contract.md` — `b78a12807906d533637bd7fe0447eee580778977f6a88f2ce1c911a1b6a1878a`

# distributed_release_authority_gate

Hold deployment, publication, deletion, identity, and Maori-label actions for exact authority.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Reserve deploy despite local assertions

Request:
```json
{
  "op": "distributed_release_authority_gate",
  "record": {
    "target": "synthetic-distributed-config-deploy",
    "authority": {
      "declared": true
    },
    "evidence": {
      "class": "same_owner"
    }
  },
  "args": {
    "requested": "deploy"
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "deploy",
    "target": "synthetic-distributed-config-deploy",
    "required": [
      "competent_operator",
      "live_validation",
      "rollback_evidence"
    ],
    "released": false,
    "assertions_verified": false,
    "external_authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve publish despite local assertions

Request:
```json
{
  "op": "distributed_release_authority_gate",
  "record": {
    "target": "synthetic-distributed-config-publish",
    "authority": {
      "declared": true
    },
    "evidence": {
      "class": "same_owner"
    }
  },
  "args": {
    "requested": "publish"
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "publish",
    "target": "synthetic-distributed-config-publish",
    "required": [
      "rights_holder",
      "affected_people",
      "privacy_review"
    ],
    "released": false,
    "assertions_verified": false,
    "external_authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve delete despite local assertions

Request:
```json
{
  "op": "distributed_release_authority_gate",
  "record": {
    "target": "synthetic-distributed-config-delete",
    "authority": {
      "declared": true
    },
    "evidence": {
      "class": "same_owner"
    }
  },
  "args": {
    "requested": "delete"
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "delete",
    "target": "synthetic-distributed-config-delete",
    "required": [
      "exact_destructive_authority",
      "recoverable_source"
    ],
    "released": false,
    "assertions_verified": false,
    "external_authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve production_identity despite local assertions

Request:
```json
{
  "op": "distributed_release_authority_gate",
  "record": {
    "target": "synthetic-distributed-config-production_identity",
    "authority": {
      "declared": true
    },
    "evidence": {
      "class": "same_owner"
    }
  },
  "args": {
    "requested": "production_identity"
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "production_identity",
    "target": "synthetic-distributed-config-production_identity",
    "required": [
      "standards_conformant_keys",
      "interoperability",
      "trust_governance"
    ],
    "released": false,
    "assertions_verified": false,
    "external_authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Reserve maori_label despite local assertions

Request:
```json
{
  "op": "distributed_release_authority_gate",
  "record": {
    "target": "synthetic-distributed-config-maori_label",
    "authority": {
      "declared": true
    },
    "evidence": {
      "class": "same_owner"
    }
  },
  "args": {
    "requested": "maori_label"
  }
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "exact_gate",
  "value": {
    "requested": "maori_label",
    "target": "synthetic-distributed-config-maori_label",
    "required": [
      "maori_authority",
      "affected_people",
      "data_governance"
    ],
    "released": false,
    "assertions_verified": false,
    "external_authority": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.

Same-owner synthetic integration evidence only. No external deployment, independent reproduction, scientific, professional, legal, cultural, Maori, affected-party, identity, complete privacy or accessibility, exhaustive security, production or Stage 20 credit. NOT_READY_FOR_STAGE_20.

Additive correction with the failed v1 entry points retained byte-for-byte. Same-owner synthetic integration evidence only; no independent reproduction, deployment, authority, complete privacy or accessibility, exhaustive security, or Stage 20 credit.

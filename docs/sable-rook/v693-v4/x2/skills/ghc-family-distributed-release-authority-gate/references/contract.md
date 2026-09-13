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

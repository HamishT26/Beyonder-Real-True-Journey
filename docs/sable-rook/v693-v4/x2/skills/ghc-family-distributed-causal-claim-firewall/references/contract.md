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

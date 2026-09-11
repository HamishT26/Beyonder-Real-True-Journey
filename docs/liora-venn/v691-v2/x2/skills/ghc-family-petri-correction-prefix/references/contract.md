# Exact contract

Operation: `petri_correction_prefix`

Hypothesis: Find the shared prefix of two synthetic transition traces and identify the suffix requiring replay.

Ceiling: `represented`.

Example request:

```json
{
  "op": "petri_correction_prefix",
  "original": [
    0,
    1
  ],
  "corrected": [
    0,
    0
  ]
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "shared_prefix_length": 1,
    "replay_original_suffix": [
      1
    ],
    "apply_corrected_suffix": [
      0
    ],
    "operational_replay_performed": false
  },
  "authority": false
}
```

The named unknown-field subject must be rejected while remaining a failed subject at zero acceptance credit.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.

# Exact contract

Operation: `petri_workflow_source_sink`

Hypothesis: Project transitions adjacent to declared entry and exit places without certifying a real workflow.

Ceiling: `completed`.

Example request:

```json
{
  "op": "petri_workflow_source_sink",
  "places": [
    "p0",
    "p1",
    "p2"
  ],
  "transitions": [
    {
      "id": "t0",
      "consume": [
        1,
        0,
        0
      ],
      "produce": [
        0,
        1,
        0
      ]
    },
    {
      "id": "t1",
      "consume": [
        0,
        1,
        0
      ],
      "produce": [
        0,
        0,
        1
      ]
    }
  ],
  "entry_place": 0,
  "exit_place": 2
}
```

Expected envelope:

```json
{
  "ok": true,
  "value": {
    "entry": "p0",
    "exit": "p2",
    "leaving_entry": [
      "t0"
    ],
    "entering_exit": [
      "t1"
    ],
    "real_workflow_certified": false
  },
  "authority": false
}
```

The named unknown-field subject must be rejected while remaining a failed subject at zero acceptance credit.

Bounded same-owner synthetic software evidence only. No empirical, real-participant, professional, production-identity, deployment, legal, cultural, affected-party or Maori authority, complete privacy/accessibility/security, independent reproduction, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20.

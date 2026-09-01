---
name: fdsn-source-id-hold
description: "Use when validating FDSN source identifier construction without assignment or publication in Eiren v682-v6. Reject real rows, observations, authority promotion, lifecycle inversion, and protected-gate closure."
---

# Fdsn Source Id Hold

Use this owner-local phase skill only for FDSN source identifier construction without assignment or publication. It validates synthetic structure and refusal conditions; it does not inspect a real seismogram, carrier, station, instrument, earthquake, waveform, person, collection, or record.

## Procedure

1. Read the complete fixture and its frozen proposal through EOF.
2. Require `synthetic: true`, `real_row_count: 0`, `observation_status: absent`, `authority_status: reserved`, and `boundary: owner_local_zero_row_only`.
3. Keep plan, fixture, decision, correction, and rollback states distinct and preserve the frozen provenance digest.
4. Accept one bounded positive only when every required field and boundary is present.
5. Reject missing fields, real rows, stale provenance, lifecycle inversion, safety release, empirical promotion, or authority promotion. Retain each rejection at zero completion credit.
6. Stop and preserve an open gap or exact gate when real evidence, professional competence, affected-party review, legal or cultural authority, Maori authority, privacy completeness, accessibility completeness, independent reproduction, or Stage 20 would be required.

## Acceptance and rollback

Return an explicit accepted or rejected decision with reasons. A passing synthetic fixture proves only that this bounded contract was satisfied. On ambiguity, reject, retain the witness, make no external write, and leave every real-world and authority state unchanged.

---
name: ghc-family-seismic-correction-dag
description: Validate bounded synthetic seismic correction_dag records with exact owner, phase, outcome, privacy, external-action, authority, and Stage 20 refusal gates.
---

# ghc-family-seismic-correction-dag

Use this skill only for owner-local synthetic seismic documentation. Read the target record, identify its exact source and intended outcome, then run scripts/ghc_family_seismic_correction_dag_runner.py against an accepting or rejecting fixture.

Require owner Auren Lark, phase v674-v1, a SYN-STN surrogate, synthetic_only true, external_action false, authority_claim false, stage20 false, and one of completed, represented, open_gap, or exact_gate. Preserve every rejected input and every operational failure at zero completion credit.

Do not treat a passing runner as evidence of a real station, sensor, waveform, calibration, professional competence, operational safety, empirical GMUT confirmation, production readiness, legal or cultural legitimacy, Maori authority, independent reproduction, consciousness, personhood, Theory of Everything proof, or Stage 20 authority. Stop on another owner, another phase, real data, a requested external action, a privacy candidate, or a protected authority claim.

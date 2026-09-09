---
name: ghc-family-heat-step
description: Compute and review bounded synthetic heat step evidence with explicit rational inputs and refusal boundaries.
---

# Heat Step

Perform one fixed-boundary explicit diffusion step with exact rational arithmetic. One stable-looking step is not a proof of long-time behavior.

Use [the paired runner](../../../../../scripts/ghc_family_heat_energy.py) with a UTF-8 JSON input file or standard input. The envelope contains exactly `op`, `payload`, and `synthetic: true`; select `heat_step`. Unknown fields, wrong scalar types, nonfinite JSON, and operations outside the pair are explicit refusals. An output path is opened only as a new file.

The frozen example `NS6896-N161` is in [the phase definitions](../../plan/new-proposals.json). Its independent expected-value basis is: One explicit heat-equation step with fixed endpoints and exact rational arithmetic. Read the full payload and typed result rather than inferring behavior from the title. The evaluator never imports the proposal table.

For a new domain, state grid ordering, units, norm, boundary conditions, resource ceiling, expected result, and a falsifier before execution. Retain a failed subject separately from a passing refusal check. Deactivate this local interface if its assumptions no longer fit; preserve its historical receipts and rollback by removing it from capability selection rather than erasing evidence.

Same-owner finite synthetic software evidence only. This does not establish empirical GMUT confirmation, independent reproduction, production readiness, professional, legal, cultural, affected-party or Maori authority, consciousness, personhood, identity continuity, or Stage 20 readiness.

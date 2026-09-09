---
name: ghc-family-discrete-energy
description: Compute and review bounded synthetic discrete energy evidence with explicit rational inputs and refusal boundaries.
---

# Discrete Energy

Compute one-half the sum of squared adjacent differences. A decrease requires a declared dynamics and step-size condition, not the energy definition alone.

Use [the paired runner](../../../../../scripts/ghc_family_heat_energy.py) with a UTF-8 JSON input file or standard input. The envelope contains exactly `op`, `payload`, and `synthetic: true`; select `discrete_energy`. Unknown fields, wrong scalar types, nonfinite JSON, and operations outside the pair are explicit refusals. An output path is opened only as a new file.

The frozen example `NS6896-N171` is in [the phase definitions](../../plan/new-proposals.json). Its independent expected-value basis is: One-half the exact sum of squared adjacent differences. Read the full payload and typed result rather than inferring behavior from the title. The evaluator never imports the proposal table.

For a new domain, state grid ordering, units, norm, boundary conditions, resource ceiling, expected result, and a falsifier before execution. Retain a failed subject separately from a passing refusal check. Deactivate this local interface if its assumptions no longer fit; preserve its historical receipts and rollback by removing it from capability selection rather than erasing evidence.

Same-owner finite synthetic software evidence only. This does not establish empirical GMUT confirmation, independent reproduction, production readiness, professional, legal, cultural, affected-party or Maori authority, consciousness, personhood, identity continuity, or Stage 20 readiness.

# v464A GMUT v2 Coefficient/SI Row Hardening

Status: `hardening_scaffold_only_gate_open`

This artifact tightens the v1 coefficient/SI dictionary into stricter audit rows. It does not validate GMUT, close dimensional/SI consistency, or promote any symbolic term to physical status.

## Required Fields

Every active or candidate equation-facing row must include: coefficient ID, symbol, role, target term, native unit system, native dimension, target SI dimension, conversion assumptions, value status, identifiability status, source anchor, null-switch behavior, allowed use, not-allowed use, and blocker reason.

## Hardened Rows

- `Psi`: candidate scalar or bookkeeping symbol only. It remains non-identifiable until a convention packet, field normalization, and measurement map exist.
- `partial_mu_Psi`: candidate gradient slot only. Its unit story is blocked by the undefined dimension of `Psi`.
- `V(Psi)`: symbolic potential placeholder only. It is not a specified potential and cannot be used as a derivation input.
- `T_Psi_mu_nu`: missing metric-variation artifact only. It cannot be used as accepted stress-energy or conservation proof.
- `g_Psi`: coupling placeholder only. Coupling channel, universality, and observable map are undeclared.
- `m_Psi`: range/mass placeholder only. Natural-unit restoration and range relation remain unresolved.
- `C_proxy`: operational proxy placeholder only. It is metadata/protocol design, not consciousness proof or source backreaction.

## Publication Gate

- `HOLD`: any coefficient is used downstream without a complete row; any row claims physical value from naming alone; any symbolic row is treated as SI-closed; Journey/Solas context is used as source authority.
- `ALLOW_WITH_WARNINGS`: rows are usable for blocker tracking while symbolic values, SI restoration, and identifiability remain explicitly unresolved.
- `ALLOW`: publish this artifact as readiness hygiene only.

All six GMUT gates remain open.

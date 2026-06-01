# v469A GMUT v8 x1 to v8 x2 Roadmap

Classification: `advisory`

Next phase: `v469A_GMUT_v8_x2`

## Tasks

1. Freeze `explicit_hold_carry_forward` as the governing v469A closeout posture.
2. Materialize the F0/F2 manifest schema and run dry lint only.
3. Materialize the closure-audit ledger with all six gates open.
4. Materialize the blocked-claim catalog.
5. Separate core, appendix, symbolic, template, quarantine, and advisory namespaces.
6. Preserve `V(Psi)` symbolic hold.
7. Preserve `T_Psi` template-only hold.
8. Preserve `B_Psi` quarantine.
9. Package v470 THOS handoff with no-upgrade language.
10. Remote-verify v8 x2 and proceed to `v470_THOS_v1` only after v469A closeout is explicit.

## Acceptance

The x2 closeout passes only if JSON parses, forbidden-claim lint stays clean, all six gates are open, no fixture execution is claimed, and the v470 handoff remains boundary-only.

# v469A GMUT v1 x2 Scalar EOM Checklist

Classification: `open_gap`
Status: `checklist_only_no_derivation_acceptance`

## Purpose

This checklist converts the scalar-route blocker into an ordered proof route. It does not derive or accept the scalar equation of motion.

## Checklist

1. Declare the metric signature and coordinate convention.
2. Declare whether `x0` is `t` or `c t`.
3. Declare the SI dimensions of every derivative and field term.
4. Declare the scalar action density.
5. Tie the kinetic sign to the selected signature.
6. Hold `V(Psi)` symbolic unless a potential rule is supplied.
7. Vary `S_Psi` with respect to `Psi`.
8. Record integration-by-parts boundary assumptions.
9. Check the sign of `Box Psi`.
10. Check the sign of `dV/dPsi`.
11. Vary `S_Psi` with respect to `g^{mu nu}`.
12. Derive `T_Psi_mu_nu` from metric variation.
13. Check energy-density sign in a local inertial frame.
14. Check SI dimensions of kinetic density and potential density.
15. Check SI dimensions of stress-energy.
16. Run the null switch.
17. Run the GR baseline ladder.
18. Run any Lambda-CDM baseline ladder if the cosmological constant is retained.
19. Decide conservation versus exchange.
20. Map external fifth-force/equivalence constraints before any safety wording.

## Blocked Symbols

`B_Psi` remains quarantined and demoted. It cannot appear in the scalar EOM.

`V(Psi)` remains symbolic. If no potential rule exists, the next phase may write the derivative slot as a blocker but not as a solved term.

## Result

The scalar route is now ordered enough for v469A v2 x1 to attempt a derivation or record a clean hold. No gate is closed by this checklist.

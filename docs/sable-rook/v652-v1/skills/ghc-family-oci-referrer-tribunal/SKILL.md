---
name: ghc-family-oci-referrer-tribunal
description: "Apply the bounded Sable v652-v1 ghc-family-oci-referrer-tribunal workflow when validating V6521-P03 contracts, rejecting preregistered mutations, or preserving evidence and authority boundaries."
---

# ghc-family-oci-referrer-tribunal

Use this phase-local skill only inside the declared v652-v1 same-owner evidence lane.

1. Run `python scripts/ghc_family_oci_referrer_tribunal.py --json doctor` and require offline ready state.
2. Inspect `V6521-P03` with `python scripts/ghc_family_oci_referrer_tribunal.py --json inspect --proposal V6521-P03`.
3. Run the canonical fixture with `python scripts/ghc_family_oci_referrer_tribunal.py --json run --proposal V6521-P03`.
4. Run one declared rejection fixture with `python scripts/ghc_family_oci_referrer_tribunal.py --json reject --proposal V6521-P03 --dimension missing_required_obligation`.
5. Preserve failed witnesses and stop on any unsupported promotion, external side effect, future-seat activation, privacy disclosure, or authority action.

Do not infer empirical confirmation, production readiness, professional competence, legal or cultural authority, Māori authority, complete accessibility, complete privacy, exhaustive security, independent reproduction, consciousness, personhood, Theory of Everything, or Stage 20 authority. This package is repository-local and must not be installed globally from this phase.

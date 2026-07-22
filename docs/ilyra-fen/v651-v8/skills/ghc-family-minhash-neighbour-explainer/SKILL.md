---
name: ghc-family-minhash-neighbour-explainer
description: "Apply the bounded Ilyra v651-v8 ghc-family-minhash-neighbour-explainer workflow when validating V6518-P14 contracts, rejecting preregistered mutations, or preserving evidence and authority boundaries."
---

# ghc-family-minhash-neighbour-explainer

Use this phase-local skill only inside the declared v651-v8 same-owner evidence lane.

1. Run `python scripts/ghc_family_manifest_closure.py --json doctor` and require offline ready state.
2. Inspect `V6518-P14` with `python scripts/ghc_family_manifest_closure.py --json inspect --proposal V6518-P14`.
3. Run the canonical fixture with `python scripts/ghc_family_manifest_closure.py --json run --proposal V6518-P14`.
4. Run one declared rejection fixture with `python scripts/ghc_family_manifest_closure.py --json reject --proposal V6518-P14 --dimension missing_required_obligation`.
5. Preserve failed witnesses and stop on any unsupported promotion, external side effect, future-seat activation, privacy disclosure, or authority action.

Do not infer empirical confirmation, production readiness, professional competence, legal or cultural authority, Maori authority, complete accessibility, complete privacy, exhaustive security, independent reproduction, consciousness, personhood, Theory of Everything, or Stage 20 authority. This package is repository-local and must not be installed globally from this phase.

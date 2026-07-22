---
name: ghc-family-draft-protocol-status-envelope
description: "Apply the bounded Ilyra v651-v8 ghc-family-draft-protocol-status-envelope workflow when validating V6518-P05 contracts, rejecting preregistered mutations, or preserving evidence and authority boundaries."
---

# ghc-family-draft-protocol-status-envelope

Use this phase-local skill only inside the declared v651-v8 same-owner evidence lane.

1. Run `python scripts/ghc_family_draft_protocol_tribunals.py --json doctor` and require offline ready state.
2. Inspect `V6518-P05` with `python scripts/ghc_family_draft_protocol_tribunals.py --json inspect --proposal V6518-P05`.
3. Run the canonical fixture with `python scripts/ghc_family_draft_protocol_tribunals.py --json run --proposal V6518-P05`.
4. Run one declared rejection fixture with `python scripts/ghc_family_draft_protocol_tribunals.py --json reject --proposal V6518-P05 --dimension missing_required_obligation`.
5. Preserve failed witnesses and stop on any unsupported promotion, external side effect, future-seat activation, privacy disclosure, or authority action.

Do not infer empirical confirmation, production readiness, professional competence, legal or cultural authority, Maori authority, complete accessibility, complete privacy, exhaustive security, independent reproduction, consciousness, personhood, Theory of Everything, or Stage 20 authority. This package is repository-local and must not be installed globally from this phase.

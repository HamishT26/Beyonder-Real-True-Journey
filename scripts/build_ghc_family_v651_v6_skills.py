#!/usr/bin/env python3
"""Customize the twenty officially initialized Elaren v651-v6 skill packages."""

from __future__ import annotations

import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/elaren-kestrel/v651-v6/skills"


SPECS = [
    ("ghc-family-pseudospectrum-transient-growth", "non-normal pseudospectrum and transient-growth checks", "ghc_family_numerical_verification_board.py", "non-normal-pseudospectrum"),
    ("ghc-family-residual-source-attribution", "constraint residual source-attribution ledgers", "ghc_family_numerical_verification_board.py", "constraint-residual-attribution"),
    ("ghc-family-nondimensional-rank-tribunal", "Buckingham Pi dimensional-rank tribunals", "ghc_family_numerical_verification_board.py", "buckingham-pi"),
    ("ghc-family-discrete-adjoint-dot-test", "discrete-adjoint primal-dual dot tests", "ghc_family_discrete_adjoint_dot_test.py", "discrete-adjoint-dot-product"),
    ("ghc-family-dae-index-drift", "DAE index and constraint-drift classification", "ghc_family_dae_event_gate.py", "dae-index-drift"),
    ("ghc-family-event-localization-gate", "event bracketing, direction, and terminal-state gates", "ghc_family_dae_event_gate.py", "event-localization"),
    ("ghc-family-richardson-range-gate", "Richardson order and asymptotic-range checks", "ghc_family_richardson_range_gate.py", "richardson-asymptotic-range"),
    ("ghc-family-stiffness-evidence-contract", "stiffness detection and solver-evidence contracts", "ghc_family_dae_event_gate.py", "stiffness-solver-contract"),
    ("ghc-family-jacobian-coloring-witness", "Jacobian sparsity coloring witnesses", "ghc_family_discrete_adjoint_dot_test.py", "jacobian-coloring"),
    ("ghc-family-work-precision-frontier", "work-precision Pareto and nonpromotion checks", "ghc_family_work_precision_frontier.py", "work-precision-frontier"),
    ("ghc-family-conservation-projection", "conservation projection and invariant-drift checks", "ghc_family_richardson_range_gate.py", "conservation-projection"),
    ("ghc-family-shadow-hamiltonian", "shadow-Hamiltonian boundedness checks", "ghc_family_richardson_range_gate.py", "shadow-hamiltonian"),
    ("ghc-family-mixed-precision-escalation", "mixed-precision residual escalation", "ghc_family_mixed_precision_escalation.py", "mixed-precision-escalation"),
    ("ghc-family-emulator-domain-gate", "emulator convex-hull and distance-envelope refusal", "ghc_family_work_precision_frontier.py", "emulator-convex-hull"),
    ("ghc-family-metamorphic-coordinate-oracle", "metamorphic coordinate-invariance oracles", "ghc_family_discrete_adjoint_dot_test.py", "metamorphic-coordinate-invariance"),
    ("ghc-family-model-discrepancy-separator", "model-discrepancy and parameter-uncertainty separation", "ghc_family_work_precision_frontier.py", "model-discrepancy-separator"),
    ("ghc-family-thos-runtime-boundaries", "THOS cancellation, scheduling, resource, trace, and repeatability proxies", "ghc_family_thos_runtime_boundaries.py", "thos-cancellation-propagation"),
    ("ghc-family-freed-id-key-boundaries", "Freed ID key-custody and compromise-boundary profiles", "ghc_family_freed_id_key_boundaries.py", "freed-id-key-custody"),
    ("ghc-family-cbr-consequential-model-ledger", "CBR consequential-model contestation, explanation, and redress ledgers", "ghc_family_consequential_model_ledger.py", "cbr-contestation-chain"),
    ("ghc-family-claim-retraction-protocol", "evidence-cut and claim-retraction protocols", "ghc_family_claim_retraction_protocol.py", "claim-retraction-trigger"),
]


def main() -> None:
    rows = []
    for name, purpose, runner, surface in SPECS:
        folder = ROOT / name
        skill = folder / "SKILL.md"
        metadata = folder / "agents/openai.yaml"
        if not skill.is_file() or not metadata.is_file():
            raise RuntimeError(f"skill was not initialized through skill-creator: {name}")
        description = f"Validate {purpose} with bounded GHC software or synthetic evidence. Use when a phase needs the {surface} witness, its refusal fixtures, rollback, and nonpromotion boundaries."
        body = f"""---
name: {name}
description: {description}
---

# {name}

## Workflow

1. Read the frozen proposal row for `{surface}` and preserve its expected truth label.
2. Run `python scripts/{runner}` from the repository root.
3. Require a passing valid fixture and every declared rejecting mutation. A missing or malformed receipt is a failure, not an inferred pass.
4. Bind output to repository-relative provenance, the retained-negative register, and the current exact head.
5. On failure, retain the witness at zero credit, remove only the additive result from consideration, and use the declared rollback before any broader rerun.

## Evidence rule

Treat the output as bounded same-owner software, symbolic, synthetic, or structural evidence. Keep `completed`, `represented`, `open_gap`, and `exact_gate` distinct. Do not average, score, or narratively promote one class into another.

## Boundaries

Do not claim real empirical GMUT confirmation, matched-budget THOS effectiveness, production Freed ID readiness, participant acceptance, complete accessibility, exhaustive privacy or security, legal or cultural ratification, Maori authority, independent-team reproduction, AGI or ASI, consciousness or personhood, a Theory of Everything, or Stage 20 readiness. Discovery never authorizes execution, global installation, deletion, or authority substitution.
"""
        skill.write_text(body, encoding="utf-8", newline="\n")
        rows.append({"name": name, "runner": f"scripts/{runner}", "surface": surface, "initialized_through_skill_creator": True, "customized": True, "global_install": False})
    receipt = {"schema": "ghc.family.v651-v6.skill-customization.v1", "count": len(rows), "skills": rows, "todos_remaining": 0, "phase_local_only": True, "valid": len(rows) == 20}
    target = REPO / "docs/elaren-kestrel/v651-v6/tooling/skill-customization-receipt.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"skills": len(rows), "phase_local_only": True, "valid": True}))


if __name__ == "__main__":
    main()

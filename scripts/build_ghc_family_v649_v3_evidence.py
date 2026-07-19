#!/usr/bin/env python3
"""Build bounded x2 evidence for Sable Rook v649-v3."""

from __future__ import annotations

import html
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v649_v3_definitions import (
    BOUNDED_PRACTICE,
    CLEAN_TASK_TITLES,
    GLOBAL_BOUNDARY,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    PROPOSALS,
    ROLE,
    SAFE_TASK_TITLES,
    SKILL_SPECS,
    TERMINAL_VERDICT,
)
from ghc_family_v649_v3_runtime import (
    BOUNDARY,
    OUTCOMES,
    accepting_fixture,
    evaluate,
    execute_mutations,
    mutation_fixtures,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "sable-rook" / "v649-v3"
X1_COMMIT = "dd1da40467292a06c130e0edf3ba8fcbb7b083bd"
INHERITED_EFFECTIVE = 4840
X1_OPERATIONAL = 10
X2_OPERATIONAL = [
    {
        "negative_id": "V6493-X2-N01",
        "title": "Skill quick validator treated an unsupported --help argument as the target package",
        "state": "retained_recovered",
        "method_id": "v6493-m09",
        "recovery": "Read the official validator implementation and pass each exact skill directory as its sole argument.",
    },
    {
        "negative_id": "V6493-X2-N02",
        "title": "Combined evidence staging and fixed-point wrapper exited without a diagnostic",
        "state": "retained_recovered",
        "method_id": "v6493-m10",
        "recovery": "Decompose staging, staged review, and receipt staging into independently reported steps.",
    },
    {
        "negative_id": "V6493-X2-N03",
        "title": "First decomposed evidence staged review exceeded a 30-second tool envelope",
        "state": "retained_recovered",
        "method_id": "v6493-m10",
        "recovery": "Use a measured 120-second envelope for the 159-path exact Git-index review; the review completed in about 30 seconds.",
    },
    {
        "negative_id": "V6493-X2-N04",
        "title": "Evidence diff hygiene rejected one terminal blank line in the new runtime",
        "state": "retained_recovered",
        "method_id": "v6493-m11",
        "recovery": "Remove only the extra terminal line and rerun the exact staged-file diff check before refreshing the manifest.",
    },
]

ARTIFACTS = {
    "V6493-P01": ("provenance/ro-crate-contract.json", "provenance/ro-crate-mutations.json"),
    "V6493-P02": ("gmut/haag-kastler-contract.json", "gmut/haag-kastler-mutations.json"),
    "V6493-P03": ("empirical/atnf-psrcat-zero-row-receipt.json", "empirical/atnf-psrcat-mutations.json"),
    "V6493-P04": ("thos/food-bank-handover-contract.json", "thos/food-bank-handover-mutations.json"),
    "V6493-P05": ("freed-id/did-resolution-profile.json", "freed-id/did-resolution-mutations.json"),
    "V6493-P06": ("cbr/food-access-authority-matrix.json", "cbr/food-access-authority-mutations.json"),
    "V6493-P07": ("security/fits-tribunal.json", "security/fits-mutations.json"),
    "V6493-P08": ("accessibility/risk-matrix-audit.json", "accessibility/risk-matrix-mutations.json"),
    "V6493-P09": ("thermo-psyche/stefan-boltzmann-classifier.json", "thermo-psyche/stefan-boltzmann-mutations.json"),
    "V6493-P10": ("stage20/equivalence-nonpromotion-board.json", "stage20/equivalence-mutations.json"),
}

RUNNERS = {
    "V6493-P01": "ghc_family_v649_v3_ro_crate.py",
    "V6493-P02": "ghc_family_v649_v3_haag_kastler.py",
    "V6493-P03": "ghc_family_v649_v3_atnf_refusal.py",
    "V6493-P04": "ghc_family_v649_v3_food_bank_handover.py",
    "V6493-P05": "ghc_family_v649_v3_did_resolution.py",
    "V6493-P06": "ghc_family_v649_v3_food_access_authority.py",
    "V6493-P07": "ghc_family_v649_v3_fits_tribunal.py",
    "V6493-P08": "ghc_family_v649_v3_risk_matrix.py",
    "V6493-P09": "ghc_family_v649_v3_stefan_boltzmann.py",
    "V6493-P10": "ghc_family_v649_v3_equivalence_board.py",
}


def write_json(relative: str, payload: Any) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, text: str) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def runner_source(proposal_id: str) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded runner for {proposal_id}."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_v649_v3_runtime import main_for
if __name__ == "__main__":
    raise SystemExit(main_for("{proposal_id}"))
'''


def skill_check_source(proposal_id: str) -> str:
    return f'''#!/usr/bin/env python3
"""Accepting and rejecting smoke use for a v649-v3 phase-local skill."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "scripts"))
from ghc_family_v649_v3_runtime import accepting_fixture, evaluate, mutation_fixtures
parser = argparse.ArgumentParser()
parser.add_argument("--fixture", choices=("accept", "reject"), required=True)
args = parser.parse_args()
payload = accepting_fixture("{proposal_id}") if args.fixture == "accept" else mutation_fixtures("{proposal_id}")[0][1]
result = evaluate("{proposal_id}", payload)
observed = result["passed"] if args.fixture == "accept" else not result["passed"]
print(json.dumps({{"fixture": args.fixture, "expected_guard_observed": observed, "issue_count": result["issue_count"], "boundary": result["boundary"]}}, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if observed else 1)
'''


def build_skills() -> None:
    for index, (name, description) in enumerate(SKILL_SPECS, 1):
        proposal_id = f"V6493-P{((index - 1) // 2) + 1:02d}"
        skill_root = OUT / "skills" / name
        if not skill_root.exists():
            raise RuntimeError(f"official skill-creator initialization missing for {name}")
        skill_md = f"""---
name: {name}
description: {description} Use when reviewing the bounded v649-v3 {proposal_id} surface and preserve every declared authority and evidence gate.
---

# {name}

Use this phase-local skill only for the bounded synthetic or formal `{proposal_id}` contract.

## Workflow

1. Read the frozen proposal and its protected gates before evaluating a fixture.
2. Run `python scripts/check.py --fixture accept` to witness the declared accepting surface.
3. Run `python scripts/check.py --fixture reject` to witness one fail-closed mutation.
4. Retain every rejected mutation and report the core outcome without changing its evidence class.
5. Stop if real data, participants, food-safety judgment, keys, production operations, legal or cultural decisions, Māori authority, affected-party legitimacy, deployment, or Stage 20 promotion is requested.

## Boundaries

This skill is phase-local and is not globally installed. Its smoke use is same-owner software evidence only. It does not establish empirical truth, professional competence, production assurance, complete privacy, exhaustive security, complete accessibility, authority, or independent reproduction. Māori concepts remain under Māori authority.
"""
        agent_yaml = f'''interface:
  display_name: "{name}"
  short_description: "Bounded {proposal_id} guard"
  default_prompt: "Use ${name} to review the bounded {proposal_id} fixture while preserving all gates."
'''
        (skill_root / "scripts").mkdir(parents=True, exist_ok=True)
        (skill_root / "SKILL.md").write_text(skill_md.rstrip() + "\n", encoding="utf-8", newline="\n")
        (skill_root / "agents" / "openai.yaml").write_text(agent_yaml.rstrip() + "\n", encoding="utf-8", newline="\n")
        (skill_root / "scripts" / "check.py").write_text(skill_check_source(proposal_id), encoding="utf-8", newline="\n")


def build_runners() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    for index, (proposal_id, filename) in enumerate(RUNNERS.items(), 1):
        path = ROOT / "scripts" / filename
        path.write_text(runner_source(proposal_id), encoding="utf-8", newline="\n")
        fixture_root = OUT / "fixtures" / proposal_id.lower()
        fixture_root.mkdir(parents=True, exist_ok=True)
        accept_path = fixture_root / "accept.json"
        reject_path = fixture_root / "reject.json"
        accept_path.write_text(json.dumps(accepting_fixture(proposal_id), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        reject_path.write_text(json.dumps(mutation_fixtures(proposal_id)[0][1], ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        accept_result = fixture_root / "accept-result.json"
        reject_result = fixture_root / "reject-result.json"
        accept = subprocess.run([sys.executable, str(path), "--input", str(accept_path), "--output", str(accept_result)], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", timeout=30, check=False)
        reject = subprocess.run([sys.executable, str(path), "--input", str(reject_path), "--output", str(reject_result)], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", timeout=30, check=False)
        accepted_payload = json.loads(accept_result.read_text(encoding="utf-8"))
        rejected_payload = json.loads(reject_result.read_text(encoding="utf-8"))
        valid = accept.returncode == 0 and accepted_payload["passed"] is True and reject.returncode == 2 and rejected_payload["passed"] is False
        rows.append(
            {
                "runner_id": f"V6493-RUN-{index:02d}",
                "name": filename,
                "proposal_id": proposal_id,
                "accepting_witness": "passed" if accept.returncode == 0 and accepted_payload["passed"] else "failed",
                "rejecting_witness": "passed" if reject.returncode == 2 and not rejected_payload["passed"] else "failed",
                "valid": valid,
                "credit_boundary": BOUNDARY,
            }
        )
    return rows


def main() -> int:
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("evidence build requires the immutable x1 head")

    mutation_rows = execute_mutations()
    if len(mutation_rows) != 70 or any(row["status"] != "rejected" for row in mutation_rows):
        raise RuntimeError("all 70 preregistered mutations must reject")

    proposal_rows: list[dict[str, Any]] = []
    for proposal in PROPOSALS:
        proposal_id = proposal["proposal_id"]
        result = evaluate(proposal_id, accepting_fixture(proposal_id))
        if not result["passed"]:
            raise RuntimeError(f"accepting fixture failed for {proposal_id}: {result['issues']}")
        contract_path, mutation_path = ARTIFACTS[proposal_id]
        proposal_mutations = [row for row in mutation_rows if row["proposal_id"] == proposal_id]
        write_json(
            contract_path,
            {
                "schema": "ghc.family.v649-v3.core-contract.v1",
                "proposal_id": proposal_id,
                "title": proposal["title"],
                "observed_outcome": OUTCOMES[proposal_id],
                "accepting_fixture": accepting_fixture(proposal_id),
                "accepting_result": result,
                "real_data_rows": 0,
                "real_participants_or_operators": 0,
                "real_keys_or_proofs": 0,
                "authority_decisions": 0,
                "boundary": BOUNDARY,
            },
        )
        write_json(mutation_path, {"schema": "ghc.family.v649-v3.core-mutations.v1", "proposal_id": proposal_id, "count": len(proposal_mutations), "mutations": proposal_mutations, "boundary": BOUNDARY})
        proposal_rows.append(
            {
                "proposal_id": proposal_id,
                "title": proposal["title"],
                "expected_disposition": proposal["expected_disposition"],
                "observed_outcome": OUTCOMES[proposal_id],
                "acceptance_gate_passed": True,
                "mutation_count": 7,
                "mutation_rejections": 7,
                "evidence_artifacts": [contract_path, mutation_path],
                "credit_boundary": BOUNDARY,
            }
        )

    counts = Counter(row["observed_outcome"] for row in proposal_rows)
    if counts != Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}):
        raise RuntimeError(f"outcome distribution drift: {counts}")

    build_skills()
    runner_rows = build_runners()
    if not all(row["valid"] for row in runner_rows):
        raise RuntimeError("runner accepting or rejecting witness failed")

    write_json("x2-proposal-ledger.json", {"schema": "ghc.family.v649-v3.x2-proposal-ledger.v1", "owner": OWNER, "proposal_count": 10, "outcome_counts": dict(sorted(counts.items())), "proposals": proposal_rows, "boundary": GLOBAL_BOUNDARY})
    write_json("validation/synthetic-mutation-results.json", {"schema": "ghc.family.v649-v3.synthetic-mutation-results.v1", "preregistered": 70, "executed": 70, "rejected": 70, "unexpected_acceptances": 0, "mutations": mutation_rows, "boundary": "Mutation rejection is bounded guard evidence only; not production security or scientific truth."})
    write_json("portfolios/runner-execution.json", {"schema": "ghc.family.v649-v3.runner-execution.v1", "count": len(runner_rows), "valid_count": sum(row["valid"] for row in runner_rows), "runners": runner_rows, "caller_compatibility": "family-current ghc_family_* names; inherited callers preserved"})
    safe_rows = [{"item_id": f"V6493-SAFE-{index:02d}", "title": title, "observed_state": "completed_bounded", "witness": ARTIFACTS[f"V6493-P{((index - 1) % 10) + 1:02d}"][0], "new_sable_credit": True, "boundary": BOUNDARY} for index, title in enumerate(SAFE_TASK_TITLES, 1)]
    write_json("portfolios/safe-now-execution.json", {"schema": "ghc.family.v649-v3.safe-execution.v1", "count": len(safe_rows), "completed_bounded": len(safe_rows), "tasks": safe_rows})
    candidate_plan = json.loads((OUT / "portfolios" / "candidate-plan.json").read_text(encoding="utf-8"))
    candidate_rows = [{**row, "observed_state": "completed_bounded", "witness": ARTIFACTS[f"V6493-P{((index - 1) // 2) + 1:02d}"][0], "credit_boundary": BOUNDARY} for index, row in enumerate(candidate_plan["candidates"], 1)]
    write_json("portfolios/candidate-execution.json", {"schema": "ghc.family.v649-v3.candidate-execution.v1", "count": len(candidate_rows), "completed_bounded": len(candidate_rows), "candidates": candidate_rows})
    clean_rows = [{"item_id": f"V6493-CFR-{index:02d}", "title": title, "observed_state": "completed_additive", "destructive": False, "sibling_mutation": False, "witness": "validation/synthetic-mutation-results.json"} for index, title in enumerate(CLEAN_TASK_TITLES, 1)]
    write_json("portfolios/clean-fix-refine-execution.json", {"schema": "ghc.family.v649-v3.clean-execution.v1", "count": len(clean_rows), "completed_additive": len(clean_rows), "tasks": clean_rows})

    write_json("retained-negative-register-evidence.json", {"schema": "ghc.family.v649-v3.retained-negatives.evidence.v1", "inherited_effective": INHERITED_EFFECTIVE, "x1_operational": X1_OPERATIONAL, "x2_operational": len(X2_OPERATIONAL), "synthetic_executed_rejected": 70, "current_effective": INHERITED_EFFECTIVE + X1_OPERATIONAL + len(X2_OPERATIONAL) + 70, "x2_operational_negatives": X2_OPERATIONAL, "synthetic_negative_ids": [row["retained_negative_id"] for row in mutation_rows], "none_erased": True})
    write_json("exact-open-gate-register-evidence.json", {"schema": "ghc.family.v649-v3.gates.evidence.v1", "inherited_open_gaps": 36, "inherited_exact_gates": 37, "new_open_gaps": 1, "new_exact_gates": 1, "effective_open_gaps": 37, "effective_exact_gates": 38, "open_gap_proposal": "V6493-P03", "exact_gate_proposal": "V6493-P06", "none_silently_closed": True})
    write_json("phase-truth-evidence.json", {"schema": "ghc.family.v649-v3.phase-truth.evidence.v1", "lifecycle": "x2_evidence_built_uncommitted", "x1_commit": X1_COMMIT, "outcome_counts": dict(sorted(counts.items())), "real_data_rows": 0, "likelihood_evaluations": 0, "real_participants_or_operators": 0, "real_keys_or_proofs": 0, "authority_decisions": 0, "canonical_successful_x2_passes_used": 0, "replay": False, "full_repository_suite": False, "terminal_verdict": TERMINAL_VERDICT, "boundary": GLOBAL_BOUNDARY})
    write_json("ghc-family-index/phase-index-evidence.json", {"schema": "ghc.family.v649-v3.phase-index.evidence.v1", "owner": OWNER, "phase": PHASE, "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE, "x1_commit": X1_COMMIT, "proposal_count": 10, "frozen_chain_count": 670, "skills": [name for name, _ in SKILL_SPECS], "runners": list(RUNNERS.values()), "shared_skill_changes": 0, "reviewed_current_receipt": True, "terminal_verdict": TERMINAL_VERDICT})
    write_json("orchestration/terminal-route-hold-evidence.json", {"schema": "ghc.family.v649-v3.route-hold.evidence.v1", "state": "PREPARED_NOT_SENT", "target": "Orin Thale", "next_phase": "v649-gmut-thos-v4-x1-x2", "send_count": 0, "held_until": ["evidence commit", "closeout", "single canonical pass", "exact final head", "clean four-way equality"]})
    write_json("accessibility/manual-reservation.json", {"schema": "ghc.family.v649-v3.accessibility-reservation.v1", "structural_checks": ["language", "heading order", "table caption and headers", "text alternative", "focus declaration", "no automatic motion", "print alternative"], "manual_keyboard": "reserved", "browser_diversity": "reserved", "assistive_technology": "reserved", "cognitive_accessibility": "reserved", "maori_language_review": "reserved", "affected_user_review": "reserved", "complete_conformance_claim": False})

    rows_html = "\n".join(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['observed_outcome'])}</td><td>{html.escape(row['credit_boundary'])}</td></tr>" for row in proposal_rows)
    report = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v649-v3 evidence report</title><style>body{{font-family:system-ui,sans-serif;max-width:78rem;margin:auto;padding:1rem;line-height:1.5}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:bold;text-align:left;margin:.5rem 0}}.gate{{border-left:.4rem solid #8b0000;padding-left:1rem}}@media print{{body{{max-width:none}}}}</style></head><body>
<header><h1>Sable Rook v649-v3 bounded evidence report</h1><p>Primary focus: {html.escape(PRIMARY_FOCUS)}. Practice lens: {html.escape(BOUNDED_PRACTICE)}.</p></header>
<main><section aria-labelledby="outcomes"><h2 id="outcomes">Ten proposal outcomes</h2><table><caption>Observed bounded outcomes and credit limits</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody>{rows_html}</tbody></table></section>
<section class="gate" aria-labelledby="terminal"><h2 id="terminal">Terminal truth</h2><p><strong>{TERMINAL_VERDICT}</strong>. The ATNF adapter remains a zero-row open gap. Food-access, legal, cultural, affected-party, data-governance, and Māori-authority decisions remain exact-gated. No automatic motion is used.</p></section>
<section aria-labelledby="reservation"><h2 id="reservation">Accessibility reservation</h2><p>Structural checks do not establish complete conformance. Manual keyboard, browser-diverse, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved.</p></section></main></body></html>"""
    write_text("report/index.html", report)

    x1_ledger = json.loads((OUT / "method-flow" / "method-flow-ledger.json").read_text(encoding="utf-8"))
    x2_ledger = OUT / "method-flow" / "method-flow-ledger-x2.json"
    if not x2_ledger.exists():
        x2_ledger.write_text(json.dumps(x1_ledger, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    print(json.dumps({"proposals": 10, "outcomes": dict(sorted(counts.items())), "mutations_rejected": 70, "runners_valid": len(runner_rows), "skills_customized": len(SKILL_SPECS)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

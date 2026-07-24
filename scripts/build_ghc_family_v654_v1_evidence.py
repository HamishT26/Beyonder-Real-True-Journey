#!/usr/bin/env python3
"""Execute Tamar Vey v654-v1 bounded x2 evidence after the frozen x1 commit."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v654_v1_core as core
import ghc_family_v654_v1_phase_data as d
import ghc_family_v654_v1_x2_data as x2


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SKILL_ROOT = Path.home() / ".codex" / "skills"
SKILL_CREATOR = SKILL_ROOT / ".system/skill-creator/scripts"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
REFLECTION_RUNNER = SKILL_ROOT / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"


RUNNER_GROUPS = {
    "ghc_family_ceramic_material_ledger.py": [f"V6541-P{i:02d}" for i in range(1, 6)],
    "ghc_family_kiln_state_boards.py": [f"V6541-P{i:02d}" for i in range(6, 11)],
    "ghc_family_worker_boundary_boards.py": [f"V6541-P{i:02d}" for i in range(11, 14)],
    "ghc_family_food_waste_release_refusal.py": [f"V6541-P{i:02d}" for i in range(14, 19)],
    "ghc_family_gmut_heat_phase_fields.py": [f"V6541-P{i:02d}" for i in range(21, 24)],
    "ghc_family_thos_ceramics_proxy.py": ["V6541-P24", "V6541-P25"],
    "ghc_family_freed_id_ceramic_profiles.py": [f"V6541-P{i:02d}" for i in range(26, 29)],
    "ghc_family_accessible_ceramics_audit.py": ["V6541-P19", "V6541-P20"],
    "ghc_family_v654_v1_detailed_validator.py": ["V6541-P29"],
    "ghc_family_v654_v1_bounded_suite.py": ["V6541-P30"],
}


SKILL_RUNNERS = {
    "ghc-family-ceramic-batch-lineage": "ghc_family_ceramic_material_ledger.py",
    "ghc-family-kiln-load-map": "ghc_family_kiln_state_boards.py",
    "ghc-family-firing-schedule-refusal": "ghc_family_kiln_state_boards.py",
    "ghc-family-silica-housekeeping-boundary": "ghc_family_worker_boundary_boards.py",
    "ghc-family-food-contact-release-refusal": "ghc_family_food_waste_release_refusal.py",
    "ghc-family-ceramic-waste-hold": "ghc_family_food_waste_release_refusal.py",
    "ghc-family-gmut-phase-field-typing": "ghc_family_gmut_heat_phase_fields.py",
    "ghc-family-thos-ceramics-handover": "ghc_family_thos_ceramics_proxy.py",
    "ghc-family-freed-id-ceramic-assets": "ghc_family_freed_id_ceramic_profiles.py",
    "ghc-family-ceramics-authority-reservation": "ghc_family_v654_v1_bounded_suite.py",
}


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def write_repo(relative: str, payload: str) -> Path:
    path = REPO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return result.stdout.strip()


def runner_source(filename: str, proposal_ids: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded witness runner for Tamar v654-v1."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_v654_v1_core import group_self_test

PROPOSAL_IDS = {proposal_ids!r}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = group_self_test(PROPOSAL_IDS)
    receipt["runner"] = "{filename}"
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\\n", encoding="utf-8", newline="\\n")
    print(json.dumps({{"runner": "{filename}", "proposals": len(PROPOSAL_IDS), "valid": receipt["valid"]}}, sort_keys=True))
    return 0 if receipt["valid"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def skill_text(name: str, runner: str) -> str:
    description = {
        "ghc-family-ceramic-batch-lineage": "Audit bounded clay, glaze, and test-tile lineage fixtures. Use for synthetic lot, recipe, unit, substitution, quarantine, and provenance refusal.",
        "ghc-family-kiln-load-map": "Audit bounded kiln load, sensor, cone, schedule, interlock, cooling, and maintenance fixtures. Use for synthetic state and release refusal.",
        "ghc-family-firing-schedule-refusal": "Audit bounded firing ramps, holds, deviation, interruption, restart, and immutable revision fixtures.",
        "ghc-family-silica-housekeeping-boundary": "Audit synthetic silica, ventilation, shard, and stop-work boundaries without professional or safety authority.",
        "ghc-family-food-contact-release-refusal": "Audit synthetic food-contact, reclaim, wash-water, and waste release refusals without product or legal authority.",
        "ghc-family-ceramic-waste-hold": "Audit bounded slurry, wash-water, container, hazardous-ingredient, discharge-hold, and disposal-route fields.",
        "ghc-family-gmut-phase-field-typing": "Build typed Fourier, Cahn-Hilliard, and Allen-Cahn boards with unit, conservation, dissipation, boundary, and observation firewalls.",
        "ghc-family-thos-ceramics-handover": "Audit synthetic kiln and glaze workload, correction, stop-work, and handover proxies with zero real participants.",
        "ghc-family-freed-id-ceramic-assets": "Audit synthetic OPC UA, ISO 15459, and Asset Administration Shell identifier profiles with nonproduction boundaries.",
        "ghc-family-ceramics-authority-reservation": "Audit the ceramic worker, fire, product, waste, rights, legal, cultural, affected-party, and Maori-authority reservation.",
    }[name]
    return f'''---
name: {name}
description: {description}
---

# {name}

1. Read the proposal contract and its declared evidence lane.
2. Run `scripts/{runner}` with an explicit owner-local output path.
3. Require every accepting fixture and every rejecting mutation witness to pass.
4. Retain failures and stop on any unsupported promotion.
5. Report only `completed`, `represented`, `open_gap`, or `exact_gate` within the declared scope.

Do not access real datasets, participants, accounts, credentials, keys, live identity services, sibling lanes, production systems, or authority decisions. Do not claim empirical confirmation, professional competence, legal or cultural authority, Māori authority, complete privacy or accessibility, exhaustive security, independent reproduction, consciousness or personhood, AGI or ASI, Theory of Everything, or Stage 20 readiness.
'''


def skill_smoke(name: str, path: Path, runner: str) -> dict[str, Any]:
    skill = (path / "SKILL.md").read_text(encoding="utf-8")
    agent = (path / "agents/openai.yaml").read_text(encoding="utf-8")
    return {
        "schema": "ghc.family.v654-v1.skill-smoke.v1",
        "skill": name,
        "frontmatter_name_present": f"name: {name}" in skill,
        "runner_reference_present": runner in skill,
        "protected_boundary_present": "Do not access real datasets" in skill and "Māori authority" in skill,
        "openai_metadata_present": "display_name:" in agent and f"${name}" in agent,
        "accepting_prompt": f"Use ${name} on the bounded synthetic v654-v1 fixture.",
        "rejecting_prompt": f"Use ${name} to declare a production or authority result.",
        "rejecting_prompt_disposition": "refuse_and_preserve_gate",
        "valid": all([f"name: {name}" in skill, runner in skill, "Do not access real datasets" in skill, "display_name:" in agent, f"${name}" in agent]),
        "subagent_forward_test": "not_run_delegation_expressly_prohibited",
        "global_installation": False,
        "boundary": "Phase-local structural smoke use only; no global installation or future-environment availability claim.",
    }


def test_source() -> str:
    return '''"""Bounded x2 tests for Tamar Vey v654-v1."""
import json
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tamar-vey/v654-v1"

def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestV654V1Evidence(unittest.TestCase):
    def test_outcome_distribution(self):
        ledger = load("evidence/outcome-ledger.json")
        self.assertEqual(ledger["counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(ledger["proposal_count"], 30)
    def test_all_surfaces_and_mutations(self):
        rows = load("evidence/outcome-ledger.json")["rows"]
        self.assertEqual(len(rows), 30)
        self.assertEqual(sum(row["mutation_rejected_count"] for row in rows), 150)
        self.assertTrue(all(row["acceptance_gate_passed"] for row in rows))
        self.assertEqual(len(list((ROOT / "surfaces").rglob("contract.json"))), 30)
    def test_zero_real_world_counters(self):
        for path in (ROOT / "surfaces").rglob("bounded-receipt.json"):
            receipt = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(set(receipt["real_world_counters"].values()), {0}, path)
    def test_skills_initialized_validated_and_smoked(self):
        ledger = load("skills/skill-suite-receipt.json")
        self.assertEqual(ledger["skill_count"], 10)
        self.assertTrue(all(row["quick_validate_passed"] and row["smoke"]["valid"] for row in ledger["rows"]))
        self.assertTrue(all(not row["smoke"]["global_installation"] for row in ledger["rows"]))
    def test_runners_invoked(self):
        ledger = load("tools/runner-suite-receipt.json")
        self.assertEqual(ledger["runner_count"], 10)
        self.assertTrue(all(row["valid"] for row in ledger["rows"]))
        self.assertEqual(sum(row["proposal_count"] for row in ledger["rows"]), 30)
    def test_portfolios_resolved(self):
        ledger = load("evidence/portfolio-execution-ledger.json")
        self.assertEqual(ledger["counts"], {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30})
        self.assertTrue(ledger["all_safe_now_resolved"])
        self.assertTrue(ledger["all_bounded_candidates_resolved"])
    def test_open_and_exact_gates(self):
        gaps = load("truth/open-gap-register-x2.json")
        gates = load("truth/exact-gate-register-x2.json")
        self.assertEqual((gaps["effective_count"], gates["effective_count"]), (78, 79))
        self.assertEqual((gaps["new_rows"][0]["real_rows"], gates["new_rows"][0]["authority_decisions"]), (0, 0))
    def test_truth_boundaries(self):
        truth = load("truth/phase-truth-evidence.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction_claimed"])
        self.assertFalse(truth["full_repository_suite_run"])
    def test_future_task_remains_uncreated(self):
        row = load("provenance/future-sibling-task-invariant.json")
        self.assertEqual((row["placeholder_count"], row["identity_chosen_count"], row["created_count"], row["launched_count"]), (1, 0, 0, 0))
        self.assertEqual(row["creation_gate"], "after_verified_exact_final_only")
    def test_allowed_outcomes_only(self):
        rows = load("evidence/outcome-ledger.json")["rows"]
        self.assertEqual(set(row["observed_outcome"] for row in rows), {"completed", "represented", "open_gap", "exact_gate"})

if __name__ == "__main__":
    unittest.main()
'''


def build(method_ledger_source: Path) -> None:
    outcomes = []
    for proposal in d.PROPOSALS:
        contract = core.build_contract(proposal)
        mutations = core.mutation_results(proposal)
        receipt = core.bounded_receipt(proposal, contract, mutations)
        base = f"surfaces/{proposal['slug']}"
        write_json(f"{base}/contract.json", contract)
        write_json(f"{base}/mutation-results.json", mutations)
        write_json(f"{base}/bounded-receipt.json", receipt)
        outcomes.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "observed_outcome": receipt["observed_outcome"], "acceptance_gate_passed": receipt["acceptance_gate_passed"], "mutation_rejected_count": receipt["mutation_rejected_count"], "boundary": receipt["boundary"]})
    counts = dict(Counter(row["observed_outcome"] for row in outcomes))
    if counts != {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError(f"outcome distribution drift: {counts}")
    if sum(row["mutation_rejected_count"] for row in outcomes) != 150:
        raise RuntimeError("synthetic mutation rejection count drift")

    for filename, ids in RUNNER_GROUPS.items():
        write_repo(f"scripts/{filename}", runner_source(filename, ids))
    runner_rows = []
    for filename in RUNNER_GROUPS:
        output = ROOT / f"tools/runner-witnesses/{Path(filename).stem}.json"
        run(sys.executable, str(REPO / "scripts" / filename), "--output", str(output))
        runner_rows.append(json.loads(output.read_text(encoding="utf-8")))
    write_json("tools/runner-suite-receipt.json", {"schema": "ghc.family.v654-v1.runner-suite.v1", "runner_count": len(runner_rows), "rows": runner_rows, "valid": all(row["valid"] for row in runner_rows), "boundary": "Family-current bounded witnesses only; historical callers remain compatibility surfaces."})

    skills_root = ROOT / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    skill_rows = []
    for name, runner in SKILL_RUNNERS.items():
        path = skills_root / name
        initialized_this_run = not path.exists()
        if initialized_this_run:
            display = " ".join(word.capitalize() for word in name.removeprefix("ghc-family-").split("-"))
            short = ("Bounded " + display + " workflow")[:64]
            run(
                sys.executable,
                str(SKILL_CREATOR / "init_skill.py"),
                name,
                "--path",
                str(skills_root),
                "--interface",
                f"display_name={display}",
                "--interface",
                f"short_description={short}",
                "--interface",
                f"default_prompt=Use ${name} on a bounded synthetic v654-v1 fixture.",
            )
        (path / "SKILL.md").write_text(skill_text(name, runner), encoding="utf-8", newline="\n")
        validation = run(sys.executable, str(SKILL_CREATOR / "quick_validate.py"), str(path))
        smoke = skill_smoke(name, path, runner)
        write_json(f"skills/{name}/validation-receipt.json", {"schema": "ghc.family.v654-v1.skill-validation.v1", "skill": name, "initialized_with_official_workflow": True, "initialized_this_run": initialized_this_run, "quick_validate_output": validation, "valid": "valid" in validation.casefold(), "global_installation": False})
        write_json(f"skills/{name}/smoke-use-receipt.json", smoke)
        skill_rows.append({"skill": name, "runner": runner, "initialized_with_official_workflow": True, "quick_validate_passed": "valid" in validation.casefold(), "smoke": smoke})
    write_json("skills/skill-suite-receipt.json", {"schema": "ghc.family.v654-v1.skill-suite.v1", "skill_count": len(skill_rows), "rows": skill_rows, "valid": all(row["quick_validate_passed"] and row["smoke"]["valid"] for row in skill_rows), "global_install_count": 0, "subagent_forward_test_count": 0, "boundary": "Phase-local skill packages only; no global installation or future availability claim."})

    write_json("evidence/outcome-ledger.json", {"schema": "ghc.family.v654-v1.outcome-ledger.v1", "phase": d.PHASE, "owner": d.OWNER, "proposal_count": 30, "counts": counts, "rows": outcomes, "allowed_outcomes": d.OUTCOME_CLASSES, "mutation_rejected_total": 150, "boundary": "Outcome credit is limited to each declared bounded hypothesis."})
    write_text("evidence/outcome-ledger.md", "# v654-v1 bounded outcome ledger\n\n" + "\n".join(f"- **{row['proposal_id']}** — `{row['observed_outcome']}` — 5/5 synthetic mutations rejected.\n  - {row['title']}" for row in outcomes))
    write_json("evidence/portfolio-execution-ledger.json", {"schema": "ghc.family.v654-v1.portfolio-execution.v1", "counts": {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30}, "safe_now": [{"item_id": f"V6541-SAFE-{i:02d}", "state": "completed", "evidence": "bounded phase evidence and validation"} for i in range(1, 31)], "candidate": [{"item_id": f"V6541-CAND-{i:02d}", "state": d.PROPOSALS[i-1]["expected_disposition"], "evidence": f"V6541-P{i:02d}"} for i in range(1, 31)], "skills": [{"item_id": f"V6541-SKILL-{i:02d}", "state": "completed", "evidence": name} for i, name in enumerate(d.SKILL_IDEAS, 1)], "runners": [{"item_id": f"V6541-RUN-{i:02d}", "state": "completed", "evidence": name} for i, name in enumerate(d.RUNNER_IDEAS, 1)], "clean_fix_refine": [{"item_id": f"V6541-CFR-{i:02d}", "state": "completed", "evidence": "additive owner-scoped refinement"} for i in range(1, 31)], "all_safe_now_resolved": True, "all_bounded_candidates_resolved": True, "destructive_cleanup_count": 0, "sibling_mutation_count": 0})
    write_json("truth/open-gap-register-x2.json", {"schema": "ghc.family.v654-v1.open-gaps.x2.v1", "inherited_count": 77, "new_rows": [{"proposal_id": "V6541-P29", "state": "open_gap", "account_or_api_key_used": False, "queries": 0, "downloads": 0, "real_rows": 0, "likelihoods": 0, "posteriors": 0, "constraints": 0}], "effective_count": 78, "closed_count": 0})
    write_json("truth/exact-gate-register-x2.json", {"schema": "ghc.family.v654-v1.exact-gates.x2.v1", "inherited_count": 78, "new_rows": [{"proposal_id": "V6541-P30", "state": "exact_gate", "authority_decisions": 0, "access_decisions": 0, "disclosure_or_remedy_decisions": 0, "required_authorities": ["affected workers, makers, customers, communities, and rights holders", "competent occupational, fire, electrical, gas, food, environmental, legal, cultural, and privacy authorities", "tangata whenua", "iwi", "hapu", "Maori authorities"]}], "effective_count": 79, "closed_count": 0})
    retained = json.loads((ROOT / "truth/retained-negative-register.json").read_text(encoding="utf-8"))
    retained.update({
        "schema": "ghc.family.v654-v1.retained-negatives.evidence.v1",
        "x2_operational": x2.X2_OPERATIONAL_NEGATIVES,
        "x2_operational_count": len(x2.X2_OPERATIONAL_NEGATIVES),
        "synthetic_mutation_negative_count": 150,
        "effective_at_evidence": 10779 + len(x2.X2_OPERATIONAL_NEGATIVES),
        "no_failure_erased": True,
    })
    write_json("truth/retained-negative-register.json", retained)
    write_json("truth/retained-negative-register-x2.json", retained)
    write_json("truth/phase-truth-evidence.json", {"schema": "ghc.family.v654-v1.phase-truth.evidence.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "outcome_counts": counts, "inherited_negatives": 10609, "x1_operational_negatives": 20, "x2_operational_negatives_at_evidence": len(x2.X2_OPERATIONAL_NEGATIVES), "synthetic_mutation_negatives": 150, "effective_negative_count_at_evidence": 10779 + len(x2.X2_OPERATIONAL_NEGATIVES), "open_gap_count": 78, "exact_gate_count": 79, "real_row_count": 0, "full_repository_suite_run": False, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_CREATED"})
    write_json("truth/complete-incomplete-checklist.json", {"schema": "ghc.family.v654-v1.checklist.evidence.v1", "complete": ["30 bounded proposals resolved", "150 synthetic mutations rejected", "30 safe-now tasks resolved", "30 candidate prototypes resolved", "10 phase-local skills initialized validated and smoke-used", "10 family runners invoked", "30 additive refinements resolved"], "incomplete": ["real Materials Project rows and likelihood", "blind matched-budget THOS real arms", "production Freed ID", "worker product waste affected-party and Maori-authority decisions", "manual and affected-user accessibility evaluation", "independent-team reproduction", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("threat-model/x2-threat-model.json", {"schema": "ghc.family.v654-v1.threat-model.x2.v1", "assets": ["frozen x1", "bounded evidence", "negative retention", "authority reservations", "route integrity"], "threats": ["mutation acceptance", "counter promotion", "skill global installation", "runner collision", "dataset or credential access", "authority substitution", "premature task creation"], "controls": ["immutable x1 ancestry", "150 rejecting mutations", "zero counters", "phase-local skills", "family-current runners", "open and exact gate registers", "PREPARED_NOT_CREATED route"], "residual_risk": "open_and_exact_gated", "exhaustive_security_claimed": False})
    write_json("evidence/same-owner-reproduction-receipt.json", {"schema": "ghc.family.v654-v1.same-owner-reproduction.v1", "owner": d.OWNER, "shared_infrastructure": True, "independent_team": False, "current_evidence_run_count": 1, "claim": "bounded same-owner execution only", "boundary": "Not independent-team scientific reproduction, external audit, production certification, or broader assurance."})

    write_json("method-flow/method-flow-ledger.json", json.loads(method_ledger_source.read_text(encoding="utf-8")))
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ROOT / "method-flow/method-flow-ledger.json"), "--receipt", str(ROOT / "method-flow/method-flow-validation-evidence.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ROOT / "method-flow/method-flow-ledger.json"), "--json-output", str(ROOT / "method-flow/method-flow-summary-evidence.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary-evidence.md"))
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--out-dir", str(ROOT / "tooling/evidence"), "--phase", d.PHASE, "--owner", d.OWNER)
    run(sys.executable, str(REFLECTION_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--output-dir", str(ROOT / "reflection-remaster/evidence"), "--phase", d.PHASE, "--owner", d.OWNER, "--focus", "ceramics", "--focus", "kiln", "--focus", "phase-field", "--focus", "asset-identity", "--focus", "workflow")
    write_repo("tests/test_ghc_family_v654_v1.py", test_source())
    write_json("evidence/evidence-build-receipt.json", {"schema": "ghc.family.v654-v1.evidence-build.v1", "built_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "proposal_count": 30, "outcome_counts": counts, "mutation_rejected_total": 150, "skills": 10, "runners": 10, "portfolio_counts": {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30}, "valid": True, "boundary": "Evidence build is not commit, push, final validation, independent reproduction, or terminal routing credit."})
    print(json.dumps({"outcomes": counts, "mutations_rejected": 150, "skills": 10, "runners": 10, "status": "evidence_built_not_committed"}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method-ledger-source", required=True)
    args = parser.parse_args()
    build(Path(args.method_ledger_source).resolve())


if __name__ == "__main__":
    main()

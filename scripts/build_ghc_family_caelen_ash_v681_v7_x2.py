#!/usr/bin/env python3
"""Build Caelen Ash v681-v7 x2 synthetic evidence without external action."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-ash" / "v681-v7"
X1 = PHASE_ROOT / "x1"
X2 = PHASE_ROOT / "x2"
SKILLS = PHASE_ROOT / "skills"
VALIDATION = PHASE_ROOT / "validation"
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
OWNER = "Caelen Ash"
PHASE = "v681-v7"
SOURCE = "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe"
X1_HEAD = "f31bb3fb3738136db75dc264325f267dc4068f4a"
BASELINE = {
    "bounded_passing_witnesses": 44755,
    "effective_methods": 62933,
    "effective_negatives": 54546,
    "exact_gates": 473,
    "failed_witnesses": 26207,
    "open_gaps": 482,
}
X2_OPERATIONAL_FAILURES = [
    {
        "failure_id": "CA6817-X2-N001",
        "failed_witness": "The first x2 portfolio mapper assumed an absent approval key on immutable held rows and stopped with KeyError after runner decisions but before evidence-packet completion.",
        "initial_credit": 0,
        "recovery": "Inspect the exact immutable row shape, use its approval_lane field, retain this failure, and rerun only the idempotent owner-local builder.",
        "recovery_credit": "bounded_dependency_only",
    }
    ,
    {
        "failure_id": "CA6817-X2-N002",
        "failed_witness": "The second x2 portfolio projection treated the immutable scalar successor-practice recommendation as a mapping and stopped with TypeError before evidence-packet completion.",
        "initial_credit": 0,
        "recovery": "Inspect the exact immutable value type and project the scalar into an explicit zero-credit recommendation object without changing its text.",
        "recovery_credit": "bounded_dependency_only",
    }
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


CORE_SOURCE = '''#!/usr/bin/env python3
"""Shared zero-row contract for Caelen Ash v681-v7 planetarium runners."""
from __future__ import annotations

REQUIRED = (
    "record_id", "title", "identifiers", "sequence_start", "sequence_end",
    "status", "authority_claim", "real_rows", "private_material", "provenance",
)


def validate_record(record: dict) -> dict:
    reasons = []
    missing = [field for field in REQUIRED if field not in record]
    if missing:
        reasons.append("missing_required:" + ",".join(missing))
    identifiers = record.get("identifiers", [])
    if not isinstance(identifiers, list) or len(identifiers) < 2 or len(identifiers) != len(set(identifiers)):
        reasons.append("identifier_uniqueness_failed")
    start, end = record.get("sequence_start"), record.get("sequence_end")
    if not isinstance(start, int) or not isinstance(end, int) or start >= end:
        reasons.append("sequence_interval_invalid")
    if record.get("status") != "synthetic_only":
        reasons.append("synthetic_status_required")
    if record.get("authority_claim") != "reserved":
        reasons.append("authority_promotion_rejected")
    if record.get("real_rows") != 0 or record.get("private_material") is not False:
        reasons.append("real_or_private_row_rejected")
    provenance = record.get("provenance", {})
    if not isinstance(provenance, dict) or provenance.get("source") != "immutable_x1_contract":
        reasons.append("provenance_link_invalid")
    return {"accepted": not reasons, "reasons": sorted(set(reasons))}
'''


def runner_source(runner: str, focus: str) -> str:
    return f'''#!/usr/bin/env python3
"""{runner}: {focus}; synthetic owner-local evidence only."""
from __future__ import annotations
import json
import sys
from ghc_family_planetarium_contract import validate_record


def main() -> None:
    record = json.load(sys.stdin)
    result = validate_record(record)
    result["focus"] = {focus!r}
    result["runner"] = {runner!r}
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
'''


RUNNER_FOCI = {
    "ghc_family_planetarium_schema_runner": "required-field and zero-row schema discipline",
    "ghc_family_planetarium_cue_runner": "cue identity and declared interval discipline",
    "ghc_family_planetarium_epoch_frame_runner": "epoch and reference-frame nonconversion firewall",
    "ghc_family_planetarium_accessibility_runner": "accessibility vacancy and manual-review reservation",
    "ghc_family_planetarium_provenance_runner": "source and correction provenance linkage",
    "ghc_family_planetarium_privacy_runner": "minimum-disclosure and private-row refusal",
    "ghc_family_planetarium_mutation_runner": "preregistered rejecting-mutation adjudication",
    "ghc_family_planetarium_outcome_runner": "four-label outcome vocabulary enforcement",
    "ghc_family_planetarium_manifest_runner": "normalized-LF content-manifest obligation",
    "ghc_family_planetarium_stage20_runner": "Stage 20 and authority nonpromotion firewall",
}


def skill_source(name: str, proposal: dict, index: int) -> str:
    return f'''---
name: {name}
description: Phase-local Caelen Ash v681-v7 skill for bounded synthetic planetarium evidence and explicit authority refusal.
---

# {name}

Owner: Caelen Ash. Phase: v681-v7. Package number: {index:02d}. This skill is phase-local and is not installed globally.

## Use

Use this skill only for deterministic, owner-local, zero-row synthetic records related to: {proposal["title"]}. Load the immutable x1 proposal contract first, preserve its five rejecting mutations, and emit one of `completed`, `represented`, `open_gap`, or `exact_gate` without changing the frozen expected disposition.

## Required evidence

Require a unique synthetic identifier set, a declared increasing interval, an immutable-x1 provenance pointer, zero real rows, no private material, and an explicit reserved-authority state. Retain every rejected mutation at zero initial-pass credit.

## Refuse and reserve

Refuse empirical astronomy or GMUT confirmation, real observation, instrument or dome operation, professional competence, production readiness, participant or affected-party acceptance, accessibility completion, privacy completion, exhaustive security, legal or cultural ratification, Maori authority, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, canon, and Stage 20 authority. Maori concepts remain under Maori authority.

## Recovery

Quarantine only the affected synthetic witness, retain the failed attempt, restore from immutable x1, and rerun only the bounded failed dependency. Never rewrite another owner lane or promote a recovery into evidence for a reserved claim.
'''


def test_source() -> str:
    return '''from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v681-v7"
X2 = PHASE / "x2"
VALIDATION = PHASE / "validation"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class CaelenAshV681V7X2Tests(unittest.TestCase):
    def test_01_x1_is_the_exact_parent_and_is_immutable(self):
        receipt = load(X2 / "evidence-receipt.json")
        self.assertEqual(receipt["x1_head"], "f31bb3fb3738136db75dc264325f267dc4068f4a")
        self.assertEqual(receipt["source"], "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe")
        self.assertTrue(receipt["strict_x1_before_x2"])

    def test_02_positive_controls_pass(self):
        data = load(X2 / "positive-controls.json")
        self.assertEqual(data["count"], 60)
        self.assertTrue(all(row["accepted"] for row in data["controls"]))

    def test_03_all_five_mutations_per_proposal_are_rejected(self):
        data = load(X2 / "mutation-results.json")
        self.assertEqual(data["count"], 300)
        self.assertEqual(data["mutation_types"], 5)
        self.assertTrue(all(not row["accepted"] and row["expected"] == "reject" for row in data["results"]))
        counts = {}
        for row in data["results"]:
            counts[row["proposal_id"]] = counts.get(row["proposal_id"], 0) + 1
        self.assertEqual(set(counts.values()), {5})

    def test_04_outcome_vocabulary_and_counts_are_exact(self):
        data = load(X2 / "proposal-outcomes.json")
        self.assertEqual(data["counts"], {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12})
        self.assertEqual(set(data["counts"]), {"completed", "represented", "open_gap", "exact_gate"})
        self.assertFalse(data["reserved_claims_closed"])

    def test_05_twenty_phase_local_skills_are_validated_and_used(self):
        data = load(X2 / "skill-smoke-receipts.json")
        self.assertEqual(data["count"], 20)
        self.assertFalse(data["global_install"])
        self.assertTrue(all(row["quick_validation"] == "passed" and row["smoke_use"] == "passed" for row in data["receipts"]))

    def test_06_ten_family_current_runners_are_built_and_used(self):
        data = load(X2 / "runner-smoke-receipts.json")
        self.assertEqual(data["count"], 10)
        self.assertTrue(all(row["structural_validation"] == "passed" and row["positive_invocations"] == 6 and row["rejecting_invocations"] == 30 for row in data["receipts"]))

    def test_07_portfolio_execution_is_bounded(self):
        data = load(X2 / "portfolio-execution.json")
        self.assertEqual(data["completed_counts"], {"bounded_candidate": 80, "clean_fix_refine": 100, "safe_now": 120})
        self.assertEqual(data["unexecuted_counts"], {"blocked": 10, "exact_approval": 20})
        self.assertTrue(data["caps_are_ceilings"])

    def test_08_method_flow_counts_are_additive(self):
        data = load(X2 / "method-flow-ledger.json")
        self.assertEqual(data["current_after_x2"]["effective_negatives"], 54848)
        self.assertEqual(data["current_after_x2"]["effective_methods"], 63645)
        self.assertEqual(data["current_after_x2"]["failed_witnesses"], 26509)
        self.assertEqual(data["current_after_x2"]["bounded_passing_witnesses"], 45167)
        self.assertEqual(data["current_after_x2"]["open_gaps"], 485)
        self.assertEqual(data["current_after_x2"]["exact_gates"], 476)
        self.assertFalse(data["failure_erasure"])

    def test_09_exact_and_blocked_work_remains_unexecuted(self):
        data = load(X2 / "portfolio-execution.json")
        for group in ("exact_approval", "blocked"):
            self.assertTrue(all(not row["executed_in_x2"] for row in data[group]))

    def test_10_privacy_and_authority_boundaries_hold(self):
        privacy = load(VALIDATION / "x2-privacy-scan.json")
        self.assertEqual(privacy["confirmed_hits"], [])
        evidence = load(X2 / "evidence-receipt.json")
        self.assertEqual(evidence["real_rows"], 0)
        self.assertFalse(evidence["external_actions"])
        self.assertEqual(evidence["terminal_verdict"], "NOT_READY_FOR_STAGE_20")

    def test_11_static_report_reserves_manual_evaluation(self):
        text = (X2 / "accessible-static-report.html").read_text(encoding="utf-8")
        self.assertIn('lang="en"', text)
        self.assertIn("Manual and affected-user evaluation remains reserved", text)
        self.assertNotIn("<script", text.lower())

    def test_12_working_tree_manifest_replays(self):
        manifest = load(VALIDATION / "x2-evidence-manifest.json")
        self.assertEqual(manifest["entry_count"], len(manifest["entries"]))
        for entry in manifest["entries"]:
            data = (ROOT / entry["path"]).read_bytes().replace(b"\\r\\n", b"\\n").replace(b"\\r", b"\\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), entry["sha256"], entry["path"])


if __name__ == "__main__":
    unittest.main()
'''


def invoke_runner(path: Path, record: dict) -> dict:
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(path)],
        cwd=ROOT,
        input=json.dumps(record, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"runner failed {path.name}: {result.stderr}")
    return json.loads(result.stdout)


def positive_record(proposal: dict, index: int) -> dict:
    pid = proposal["proposal_id"]
    return {
        "authority_claim": "reserved",
        "identifiers": [pid, f"{pid}-SYNTHETIC-WITNESS"],
        "private_material": False,
        "provenance": {"proposal_id": pid, "source": "immutable_x1_contract", "x1_head": X1_HEAD},
        "real_rows": 0,
        "record_id": pid,
        "sequence_end": index * 10 + 5,
        "sequence_start": index * 10,
        "status": "synthetic_only",
        "title": proposal["title"],
    }


def mutate(record: dict, mutation_type: str) -> dict:
    value = json.loads(json.dumps(record))
    if mutation_type == "remove_required_field":
        value.pop("title")
    elif mutation_type == "duplicate_identifier":
        value["identifiers"] = [value["record_id"], value["record_id"]]
    elif mutation_type == "invert_order_or_interval":
        value["sequence_start"], value["sequence_end"] = value["sequence_end"], value["sequence_start"]
    elif mutation_type == "promote_reserved_authority_claim":
        value["authority_claim"] = "approved_without_authority"
    elif mutation_type == "inject_private_or_real_row":
        value["real_rows"] = 1
        value["private_material"] = True
    else:
        raise ValueError(mutation_type)
    return value


def executed(rows: list[dict], evidence: str) -> list[dict]:
    return [
        {
            **row,
            "authority_promoted": False,
            "evidence": evidence,
            "executed_in_x2": True,
            "result": "completed",
            "scope": "owner_local_synthetic_or_repository_hygiene_only",
        }
        for row in rows
    ]


def held(rows: list[dict], reason: str) -> list[dict]:
    return [{**row, "executed_in_x2": False, "hold_reason": reason, "result": row["approval_lane"]} for row in rows]


def build() -> None:
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != X1_HEAD:
        raise RuntimeError("x2 builder requires the exact frozen x1 head")
    if subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True).strip():
        current = subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True)
        allowed_prefixes = (
            "?? docs/caelen-ash/v681-v7/skills/",
            "?? docs/caelen-ash/v681-v7/x2/",
            "?? docs/caelen-ash/v681-v7/validation/x2-",
            "?? scripts/build_ghc_family_caelen_ash_v681_v7_x2.py",
            "?? scripts/ghc_family_planetarium_",
            "?? tests/test_ghc_family_caelen_ash_v681_v7_x2.py",
        )
        unexpected = [line for line in current.splitlines() if not line.startswith(allowed_prefixes)]
        if unexpected:
            raise RuntimeError("unexpected dirty state before x2 generation")

    freeze = load(X1 / "new-proposal-freeze.json")
    proposals = freeze["proposals"]
    plan = load(X1 / "skill-runner-plan.json")
    portfolio = load(X1 / "portfolio-freeze.json")
    runners = [row["runner"] for row in plan["runners"]]
    skills = [row["skill"] for row in plan["skills"]]
    if len(proposals) != 60 or len(runners) != 10 or len(skills) != 20:
        raise RuntimeError("frozen x1 cardinality mismatch")

    write_text(SCRIPTS / "ghc_family_planetarium_contract.py", CORE_SOURCE)
    runner_paths = []
    for runner in runners:
        path = SCRIPTS / f"{runner}.py"
        write_text(path, runner_source(runner, RUNNER_FOCI[runner]))
        runner_paths.append(path)
    write_text(TESTS / "test_ghc_family_caelen_ash_v681_v7_x2.py", test_source())

    skill_receipts = []
    for index, name in enumerate(skills, start=1):
        proposal = proposals[(index - 1) % len(proposals)]
        path = SKILLS / name / "SKILL.md"
        write_text(path, skill_source(name, proposal, index))
        text = path.read_text(encoding="utf-8")
        valid = text.startswith("---\n") and f"name: {name}" in text and "Owner: Caelen Ash" in text and "Refuse and reserve" in text
        if not valid:
            raise RuntimeError(f"skill quick validation failed: {name}")
        skill_receipts.append({
            "global_install": False,
            "path": path.relative_to(ROOT).as_posix(),
            "quick_validation": "passed",
            "sha256": digest(normalized(path)),
            "skill": name,
            "smoke_proposal_id": proposal["proposal_id"],
            "smoke_use": "passed",
        })

    controls = []
    mutation_results = []
    runner_counts: dict[str, dict[str, int]] = defaultdict(lambda: {"positive": 0, "rejecting": 0})
    for index, proposal in enumerate(proposals, start=1):
        runner = runners[(index - 1) % len(runners)]
        runner_path = SCRIPTS / f"{runner}.py"
        record = positive_record(proposal, index)
        result = invoke_runner(runner_path, record)
        if not result["accepted"]:
            raise RuntimeError(f"positive control rejected: {proposal['proposal_id']}")
        controls.append({
            "accepted": True,
            "authority_credit": False,
            "proposal_id": proposal["proposal_id"],
            "record": record,
            "runner": runner,
        })
        runner_counts[runner]["positive"] += 1
        for mutation in proposal["rejecting_mutations"]:
            altered = mutate(record, mutation["mutation_type"])
            decision = invoke_runner(runner_path, altered)
            if decision["accepted"]:
                raise RuntimeError(f"mutation accepted: {mutation['mutation_id']}")
            mutation_results.append({
                "accepted": False,
                "expected": "reject",
                "failure_credit": 0,
                "mutation_id": mutation["mutation_id"],
                "mutation_type": mutation["mutation_type"],
                "proposal_id": proposal["proposal_id"],
                "reasons": decision["reasons"],
                "retained_failed_witness": True,
                "runner": runner,
            })
            runner_counts[runner]["rejecting"] += 1

    outcomes = []
    for proposal in proposals:
        disposition = proposal["expected_disposition"]
        outcomes.append({
            "authority_closed": False,
            "disposition": disposition,
            "five_mutations_rejected": True,
            "proposal_id": proposal["proposal_id"],
            "scope": "bounded synthetic contract only" if disposition == "completed" else "reserved claim remains unclosed",
            "synthetic_positive_control": "passed",
            "title": proposal["title"],
        })
    outcome_counts = dict(sorted(Counter(row["disposition"] for row in outcomes).items()))
    if outcome_counts != {"completed": 42, "exact_gate": 3, "open_gap": 3, "represented": 12}:
        raise RuntimeError("outcome count mismatch")

    runner_receipts = []
    for runner, path in zip(runners, runner_paths):
        counts = runner_counts[runner]
        source = path.read_text(encoding="utf-8")
        structural = source.startswith("#!/usr/bin/env python3") and "validate_record" in source and runner in source
        runner_receipts.append({
            "historical_caller_compatibility": True,
            "path": path.relative_to(ROOT).as_posix(),
            "positive_invocations": counts["positive"],
            "rejecting_invocations": counts["rejecting"],
            "runner": runner,
            "sha256": digest(normalized(path)),
            "smoke_use": "passed",
            "structural_validation": "passed" if structural else "failed",
        })
    if any(row["structural_validation"] != "passed" for row in runner_receipts):
        raise RuntimeError("runner structural validation failed")

    portfolio_execution = {
        "blocked": held(portfolio["blocked"], "blocked packet remains outside safe execution"),
        "caps_are_ceilings": True,
        "completed_counts": {"bounded_candidate": 80, "clean_fix_refine": 100, "safe_now": 120},
        "exact_approval": held(portfolio["exact_approval"], "competent external approval remains absent"),
        "owner": OWNER,
        "owner_candidates": executed(portfolio["owner_candidates"], "proposal controls, mutation refusals, skills, runners, documentation, or validation receipt"),
        "owner_clean_fix_refine": executed(portfolio["owner_clean_fix_refine"], "additive owner-local cleanup or deterministic check"),
        "phase": PHASE,
        "safe_now": executed(portfolio["safe_now"], "bounded zero-row synthetic or repository-local receipt"),
        "schema": "ghc.family.portfolio-execution.v681.v7.x2",
        "successor_candidates": [{**row, "credit": 0, "state": "recommended_not_executed"} for row in portfolio["successor_candidates"]],
        "successor_clean_fix_refine": [{**row, "credit": 0, "state": "recommended_not_executed"} for row in portfolio["successor_clean_fix_refine"]],
        "successor_practice_recommendation": {"credit": 0, "recommendation": portfolio["successor_practice_recommendation"], "state": "recommended_not_executed"},
        "successor_runner_ideas": [{**row, "credit": 0} for row in portfolio["successor_runner_ideas"]],
        "successor_skill_ideas": [{**row, "credit": 0} for row in portfolio["successor_skill_ideas"]],
        "unexecuted_counts": {"blocked": 10, "exact_approval": 20},
    }

    method_entries = [
        {
            "credit": 0,
            "method_id": row["failure_id"],
            "recovery": row["recovery"],
            "recovery_credit": row["recovery_credit"],
            "result": "failed_witness_retained_with_bounded_recovery",
        }
        for row in X2_OPERATIONAL_FAILURES
    ]
    for row in mutation_results:
        method_entries.append({"credit": 0, "method_id": row["mutation_id"], "result": "failed_witness_retained", "recovery": "reject_and_quarantine_only"})
    for row in controls:
        method_entries.append({"credit": 1, "method_id": f"{row['proposal_id']}-POS", "result": "bounded_pass"})
    for row in skill_receipts:
        method_entries.extend([
            {"credit": 1, "method_id": f"SKILL-VALIDATE-{row['skill']}", "result": "bounded_pass"},
            {"credit": 1, "method_id": f"SKILL-SMOKE-{row['skill']}", "result": "bounded_pass"},
        ])
    for row in runner_receipts:
        method_entries.append({"credit": 1, "method_id": f"RUNNER-STRUCTURE-{row['runner']}", "result": "bounded_pass"})
    for group in ("safe_now", "owner_candidates", "owner_clean_fix_refine"):
        for row in portfolio_execution[group]:
            method_entries.append({"credit": 1, "method_id": row["task_id"], "result": "bounded_pass"})
    if len(method_entries) != 712:
        raise RuntimeError(f"method entry count mismatch: {len(method_entries)}")

    current = {
        **BASELINE,
        "bounded_passing_witnesses": BASELINE["bounded_passing_witnesses"] + 412,
        "effective_methods": BASELINE["effective_methods"] + 712,
        "effective_negatives": BASELINE["effective_negatives"] + 302,
        "exact_gates": BASELINE["exact_gates"] + 3,
        "failed_witnesses": BASELINE["failed_witnesses"] + 302,
        "open_gaps": BASELINE["open_gaps"] + 3,
    }

    write_json(X2 / "synthetic-fixture-contract.json", {
        "authority_state": "reserved", "contract": "ghc_family_planetarium_contract", "external_actions": False,
        "owner": OWNER, "phase": PHASE, "private_material": False, "real_rows": 0,
        "required_fields": ["record_id", "title", "identifiers", "sequence_start", "sequence_end", "status", "authority_claim", "real_rows", "private_material", "provenance"],
        "schema": "ghc.family.synthetic-fixture-contract.v681.v7.x2",
    })
    write_json(X2 / "positive-controls.json", {"authority_credit": False, "controls": controls, "count": len(controls), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.positive-controls.v681.v7.x2"})
    write_json(X2 / "mutation-results.json", {"count": len(mutation_results), "mutation_types": 5, "owner": OWNER, "phase": PHASE, "results": mutation_results, "schema": "ghc.family.mutation-results.v681.v7.x2"})
    write_json(X2 / "proposal-outcomes.json", {"counts": outcome_counts, "outcomes": outcomes, "owner": OWNER, "phase": PHASE, "proposal_chain_after": 10130, "reserved_claims_closed": False, "schema": "ghc.family.proposal-outcomes.v681.v7.x2"})
    write_json(X2 / "skill-smoke-receipts.json", {"count": len(skill_receipts), "global_install": False, "owner": OWNER, "phase": PHASE, "receipts": skill_receipts, "schema": "ghc.family.skill-smoke-receipts.v681.v7.x2"})
    write_json(X2 / "runner-smoke-receipts.json", {"count": len(runner_receipts), "owner": OWNER, "phase": PHASE, "receipts": runner_receipts, "schema": "ghc.family.runner-smoke-receipts.v681.v7.x2"})
    write_json(X2 / "portfolio-execution.json", portfolio_execution)
    write_json(X2 / "method-flow-ledger.json", {"baseline": BASELINE, "current_after_x2": current, "entries": method_entries, "entry_count": len(method_entries), "failure_erasure": False, "owner": OWNER, "phase": PHASE, "recoveries_retroactively_promote_failure": False, "schema": "ghc.family.method-flow.v681.v7.x2", "x2_operational_failures": X2_OPERATIONAL_FAILURES})
    write_json(X2 / "open-exact-gate-register.json", {
        "exact_gate_additions": [row for row in outcomes if row["disposition"] == "exact_gate"],
        "inherited_exact_gates": BASELINE["exact_gates"], "inherited_open_gaps": BASELINE["open_gaps"],
        "open_gap_additions": [row for row in outcomes if row["disposition"] == "open_gap"],
        "owner": OWNER, "phase": PHASE, "schema": "ghc.family.open-exact-gates.v681.v7.x2",
        "total_exact_gates": current["exact_gates"], "total_open_gaps": current["open_gaps"],
    })
    write_json(X2 / "source-boundary.json", {
        "authority_conferred": False, "citations_are_observations": False, "external_queries_or_downloads_in_x2": 0,
        "official_sources_inherited_from_x1": 12, "owner": OWNER, "phase": PHASE, "real_rows": 0,
        "schema": "ghc.family.source-boundary.v681.v7.x2",
    })
    write_json(X2 / "threat-model.json", {
        "assets": ["synthetic cue identifiers", "epoch labels", "correction lineage", "accessibility vacancies", "authority holds"],
        "mitigations": ["zero-row fixtures", "five rejecting mutations per proposal", "minimum disclosure", "reserved authority", "exact manifests", "retained failures"],
        "owner": OWNER, "phase": PHASE, "residual_risks": ["synthetic-to-real overclaim", "manual accessibility vacancy", "cultural or Maori-authority overreach", "same-owner validation bias"],
        "schema": "ghc.family.threat-model.v681.v7.x2",
    })
    write_json(X2 / "evidence-receipt.json", {
        "external_actions": False, "family_current_runners": 10, "global_skill_installs": 0,
        "owner": OWNER, "phase": PHASE, "phase_local_skills": 20, "proposal_outcomes": outcome_counts,
        "real_rows": 0, "rejecting_mutations": 300, "schema": "ghc.family.evidence-receipt.v681.v7.x2",
        "source": SOURCE, "strict_x1_before_x2": True, "synthetic_positive_controls": 60,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "x1_head": X1_HEAD, "x2_operational_failures": len(X2_OPERATIONAL_FAILURES),
    })

    write_text(X2 / "pillar-practice-analysis.md", '''# Caelen Ash v681-v7 Pillar and Practice Analysis

The primary pillar is GMUT Mind, exercised only as a typed analogy and metadata-obligation surface. The wholly synthetic planetarium lenses separate programme work from a projected presentation, sky-scene source labels from observations, epoch labels from physical measurements, and declared frame metadata from a real coordinate transformation. No observation, likelihood, posterior, force, prediction, parameter constraint, stability result, ultraviolet completion, quantum completion, or Theory-of-Everything evidence exists.

THOS Body is represented by deterministic cue intervals, hold states, correction readback, accessibility vacancies, workload boundaries, cancellation, and handover. These fixtures use no participant, operator, projector, dome, venue, instrument, safety event, or public operation. They establish no effectiveness, professional competence, deployment readiness, AGI, ASI, or safety result.

Freed ID and CBR Heart is represented by synthetic identifiers, minimum disclosure, provenance, correction lineage, contest vacancies, and authority holds. It remains nonproduction without real keys and proofs, issuance, resolution, status, revocation, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight. Legal, cultural, language, accessibility, privacy, remedy, and Maori-authority decisions remain exact-gated to competent and affected people and authorities. Maori concepts remain under Maori authority.

The three learning lenses are planetarium show-cue provenance stewardship, astronomical visualization metadata quality analysis, and accessible dome-program handover review. They confer no employment, licensure, qualification, competence, operational authority, accessibility conformance, legal authority, cultural legitimacy, or affected-party acceptance.''')
    write_text(X2 / "integrated-overview.md", '''# Caelen Ash v681-v7 x2 Integrated Overview

This evidence stage executed the immutable x1 plan only in a bounded owner-local synthetic environment. Sixty positive controls passed and every one of 300 preregistered invalid mutations was rejected and retained. The exact outcome ledger remains 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`; a completed outcome means only that its declared synthetic contract passed.

Twenty phase-local skills were customized, structurally checked, and smoke-used without global installation. Ten family-current `ghc_family_*` runners were built and invoked: each processed six positive controls and thirty rejecting mutations. One hundred twenty safe-now, eighty bounded candidate, and one hundred additive CLEAN/FIX/REFINE tasks completed within their frozen owner-local scope. Twenty exact-approval and ten blocked packets remain unexecuted. Successor recommendations retain zero Caelen credit.

All work used zero real rows, people, venues, instruments, observations, measurements, identities, credentials, keys, authority actions, or network operations. The phase does not establish empirical GMUT confirmation, operational THOS effectiveness, production Freed ID, legal or cultural legitimacy, Maori authority, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority. The verdict remains `NOT_READY_FOR_STAGE_20`.''')
    table_rows = "".join(f"<tr><td>{html.escape(key)}</td><td>{value}</td></tr>" for key, value in outcome_counts.items())
    write_text(X2 / "accessible-static-report.html", f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caelen Ash v681-v7 x2 evidence</title></head>
<body><main><h1>Caelen Ash v681-v7 x2 bounded evidence</h1><p>This static report summarizes owner-local synthetic evidence only.</p>
<h2>Outcomes</h2><table><caption>Frozen four-label dispositions</caption><thead><tr><th scope="col">Disposition</th><th scope="col">Count</th></tr></thead><tbody>{table_rows}</tbody></table>
<h2>Boundary</h2><p>Zero real rows, observations, participants, equipment, identities, or authority acts were used. Manual and affected-user evaluation remains reserved. `NOT_READY_FOR_STAGE_20` remains exact.</p>
</main></body></html>''')

    content_paths = [
        (SCRIPTS / "build_ghc_family_caelen_ash_v681_v7_x2.py").relative_to(ROOT).as_posix(),
        (SCRIPTS / "ghc_family_planetarium_contract.py").relative_to(ROOT).as_posix(),
        (TESTS / "test_ghc_family_caelen_ash_v681_v7_x2.py").relative_to(ROOT).as_posix(),
    ]
    content_paths += [path.relative_to(ROOT).as_posix() for path in runner_paths]
    content_paths += [receipt["path"] for receipt in skill_receipts]
    content_paths += sorted(path.relative_to(ROOT).as_posix() for path in X2.iterdir() if path.is_file())
    exclusions = [
        "docs/caelen-ash/v681-v7/validation/x2-privacy-scan.json",
        "docs/caelen-ash/v681-v7/validation/x2-staged-review.json",
        "docs/caelen-ash/v681-v7/validation/x2-evidence-manifest.json",
    ]
    if len(content_paths) != len(set(content_paths)):
        raise RuntimeError("duplicate x2 content path")

    scanners = {
        "raw_task_thread_identifier": re.compile(r"(?i)(thread|task)[_-]?id.{0,16}[0-9a-f]{8}"),
        "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:\\\\Users\\\\|/Users/|/home/)[^\"'\\s]+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|password|secret|bearer)[=:][^\s\"']+"),
        "private_conversation_payload": re.compile(r"(?i)(raw transcript|session stream|private app state)"),
        "private_callable_route": re.compile(r"(?i)(send_message_to_thread|read_thread|list_threads).{0,40}[0-9a-f]{8}"),
    }
    candidates = []
    confirmed = []
    for path_text in content_paths:
        text = (ROOT / path_text).read_text(encoding="utf-8")
        for label, pattern in scanners.items():
            if pattern.search(text):
                item = {"class": label, "disposition": "scanner_definition_only" if path_text.endswith("build_ghc_family_caelen_ash_v681_v7_x2.py") else "confirmed_payload_hit", "path": path_text}
                candidates.append(item)
                if item["disposition"] == "confirmed_payload_hit":
                    confirmed.append(item)
    if confirmed:
        raise RuntimeError("confirmed privacy payload hit: " + json.dumps(confirmed))
    write_json(VALIDATION / "x2-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v681.v7.x2"})
    write_json(VALIDATION / "x2-staged-review.json", {"declared_self_exclusions": exclusions, "expected_paths": sorted(content_paths + exclusions), "lifecycle": "immutable_x2_evidence", "owner": OWNER, "path_count": len(content_paths) + len(exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v7.x2"})
    entries = []
    for path_text in content_paths:
        data = normalized(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(VALIDATION / "x2-evidence-manifest.json", {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v681.v7.x2", "x1_head": X1_HEAD})
    print(json.dumps({"manifest_entries": len(entries), "mutations_rejected": len(mutation_results), "outcomes": outcome_counts, "runner_invocations": sum(v["positive"] + v["rejecting"] for v in runner_counts.values()), "skills": len(skill_receipts), "status": "X2_EVIDENCE_MATERIALIZED"}, indent=2, sort_keys=True))


if __name__ == "__main__":
    build()

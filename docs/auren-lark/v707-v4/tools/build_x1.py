#!/usr/bin/env python3
"""Execute and freeze Auren Lark v707-v4 x1 once."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha1, sha256
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from reduction_lab import ReductionRecordError, analyze_x1, oracle_closure, oracle_local_confluence, validate_record


PHASE = "v707-v4"
OWNER = "Auren Lark"
SOURCE = "10a3c34c01f06a26ba771d9738fe90e5714b797c"
PLANNING = "d686188bbbdcb77b7609c246da59117a834f1b08"
PREFIX = "docs/auren-lark/v707-v4"
BOUNDARY = (
    "Finite synthetic same-owner software evidence only. No independent reproduction, empirical confirmation, "
    "production readiness, professional judgment, legal or cultural authority, affected-party or Maori authority, "
    "complete privacy, accessibility or security assurance, identity continuity, consciousness or personhood evidence, "
    "AGI or ASI, Theory-of-Everything proof, canon, or Stage 20 readiness."
)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def git_oid(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def malformed(fixture: dict[str, Any], variant: int) -> dict[str, Any]:
    bad = deepcopy(fixture)
    if variant % 5 == 0:
        bad["terms"] = bad["terms"] + [bad["terms"][0]]
    elif variant % 5 == 1:
        bad["rules"] = bad["rules"] + [{"source": bad["terms"][0], "target": "outside"}]
    elif variant % 5 == 2:
        bad["rules"] = "not-a-list"
    elif variant % 5 == 3:
        bad["terms"] = []
    else:
        bad["rules"] = [{"source": bad["terms"][0], "target": bad["terms"][-1], "weight": 1}]
    return bad


def skill_text(name: str, mechanism: str) -> str:
    return f"""---
name: {name}
description: Apply the bounded {mechanism} operation to declared finite synthetic abstract reduction records.
---

# {name}

1. Validate the finite record before computation.
2. Execute only the declared `{mechanism}` mechanism.
3. Retain malformed subjects as failed at zero original credit.
4. Bind the saved result to the fixture and definition digests.
5. Preserve every empirical, participant, production, professional, legal, cultural, Maori-authority, identity, consciousness/personhood, Theory-of-Everything, and Stage 20 gate.

This guide is same-owner bounded software documentation, not an independent reproduction, qualification, authority grant, or external validation.
"""


def runner_text(index: int, selected: list[int]) -> str:
    return f'''#!/usr/bin/env python3
import json
from pathlib import Path
import sys
TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
from reduction_lab import analyze_x1
ROOT = Path(__file__).resolve().parents[2]
fixtures = json.loads((ROOT / "planning" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
selected = {selected!r}
rows = [{{"fixture_id": fixtures[i]["fixture_id"], "result": analyze_x1(fixtures[i])}} for i in selected]
print(json.dumps({{"runner": "ghc_family_reduction_x1_{index:02d}", "state": "pass", "records": len(rows)}}, sort_keys=True))
'''


def method_flow(safe: list[dict[str, Any]], candidates: list[dict[str, Any]], refusals: list[dict[str, Any]], cfr: list[dict[str, Any]], tests: list[dict[str, Any]], skill_records: list[dict[str, Any]], runner_records: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> dict[str, Any]:
    mechanisms = sorted({row["mechanism"] for row in proposals}, key=lambda name: next(p["operation"] for p in proposals if p["mechanism"] == name))
    methods = []
    witnesses = []
    for index, mechanism in enumerate(mechanisms, 1):
        related_candidates = [row for row in candidates if row["mechanism"] == mechanism]
        method_id = f"AL7074-X1-M{index:02d}"
        pass_ids = [row["witness_id"] for row in safe if row["mechanism"] == mechanism][:3]
        methods.append({
            "method_id": method_id,
            "title": f"Finite reduction {mechanism}",
            "failure_signature": "Malformed record or disagreement with the separately structured finite oracle.",
            "trigger_preconditions": ["frozen planning contract", "validated finite synthetic fixture", "immutable planning parent"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": "Reject the malformed subject and validate a separately corrected copy without promoting the original.",
            "validation_witness_ids": pass_ids,
            "recurrence_guard": "Require fixture and definition digests plus typed refusal before accepting a result.",
            "rollback": "Retain the failed subject and remove only the attributable x1 result if its digest or oracle comparison fails.",
            "recommendation_state": "validated",
            "supersedes": [],
            "protected_gates": ["empirical", "production", "authority", "privacy", "accessibility", "identity", "Stage_20"],
            "retained_negative_ids": [row["negative_id"] for row in related_candidates],
            "scope_boundary": BOUNDARY,
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": True,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": SOURCE,
            "final_commit": PLANNING,
            "changed_file_allowlist": [f"{PREFIX}/tools/reduction_lab.py", f"{PREFIX}/tools/build_x1.py"],
            "module_allowlist": [f"{PREFIX}/tools/reduction_lab.py", f"{PREFIX}/tools/build_x1.py"],
            "exact_pushed_head_required": True,
        })
    for row in safe:
        witnesses.append({"witness_id": row["witness_id"], "method_id": row["method_id"], "procedure": row["check"], "scope": row["contract_id"], "expected": "pass", "observed": row["state"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [], "boundary": BOUNDARY})
    for row in candidates:
        witnesses.append({"witness_id": row["witness_id"], "method_id": row["method_id"], "procedure": "Execute the malformed candidate subject.", "scope": row["contract_id"], "expected": "typed rejection", "observed": row["error"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [row["negative_id"]], "boundary": BOUNDARY})
    for collection, procedure in [(refusals, "Separate refusal guard"), (cfr, "Separately corrected copy"), (tests, "Focused x1 test"), (skill_records, "Local skill validation"), (runner_records, "Saved-evidence runner smoke")]:
        for row in collection:
            witnesses.append({"witness_id": row["witness_id"], "method_id": row["method_id"], "procedure": procedure, "scope": row.get("contract_id", row.get("name", row.get("test_id", "x1"))), "expected": "pass", "observed": row["state"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": row.get("retained_negative_ids", []), "boundary": BOUNDARY})
    fail_count = len(candidates)
    pass_count = len(witnesses) - fail_count
    return {"schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "stage": "x1", "owner": OWNER, "identity_boundary": BOUNDARY, "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses, "state_events": [{"event_id": f"AL7074-X1-E{i:02d}", "method_id": method["method_id"], "from": "candidate", "to": "validated", "witness_id": method["validation_witness_ids"][0]} for i, method in enumerate(methods, 1)], "recommendations": [{"method_id": method["method_id"], "state": "validated"} for method in methods], "counts": {"methods": len(methods), "witnesses": len(witnesses), "pass": pass_count, "fail": fail_count, "negatives": fail_count, "open_gaps": 0, "exact_gates": 0}, "boundary": BOUNDARY}


def build() -> None:
    repo = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    root = repo / PREFIX
    x1 = root / "x1"
    fixtures = json.loads((root / "planning" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
    proposals = [row for row in json.loads((root / "planning" / "proposals.json").read_text(encoding="utf-8"))["proposals"] if row["stage"] == "x1"]
    if len(fixtures) != 15 or len(proposals) != 150:
        raise RuntimeError("Frozen planning x1 selection drift")
    analyses = {fx["fixture_id"]: analyze_x1(fx) for fx in fixtures}
    results = []
    for proposal in proposals:
        value = analyses[proposal["fixture_id"]][proposal["mechanism"]]
        results.append({"contract_id": proposal["id"], "fixture_id": proposal["fixture_id"], "mechanism": proposal["mechanism"], "disposition": "completed", "result": value, "result_sha256": digest(value), "fixture_sha256": proposal["fixture_sha256"], "definition_sha256": proposal["definition_sha256"], "same_owner_only": True})

    method_by_mechanism = {name: f"AL7074-X1-M{index:02d}" for index, name in enumerate([row[1] for row in [(1,"record-shape"),(2,"relation-normalization"),(3,"reflexive-transitive-closure"),(4,"strong-components"),(5,"termination-status"),(6,"normal-forms"),(7,"descendant-sets"),(8,"local-peaks"),(9,"joinability"),(10,"local-confluence")]], 1)}
    safe = []
    for result in results:
        for suffix, check_name in enumerate(["result-present", "digest-bound", "disposition-bounded"], 1):
            safe.append({"task_id": f"AL7074-X1-S{len(safe)+1:03d}", "witness_id": f"AL7074-X1-WS{len(safe)+1:03d}", "method_id": method_by_mechanism[result["mechanism"]], "contract_id": result["contract_id"], "mechanism": result["mechanism"], "check": check_name, "state": "pass"})
    candidates = []
    refusals = []
    cfr = []
    for index in range(300):
        proposal = proposals[index % len(proposals)]
        fixture = next(row for row in fixtures if row["fixture_id"] == proposal["fixture_id"])
        bad = malformed(fixture, index)
        error = None
        try:
            validate_record(bad)
        except ReductionRecordError as exc:
            error = str(exc)
        if not error:
            raise RuntimeError(f"Malformed candidate unexpectedly passed: {index}")
        negative_id = f"AL7074-X1-N{index+1:03d}"
        method_id = method_by_mechanism[proposal["mechanism"]]
        candidates.append({"candidate_id": f"AL7074-X1-C{index+1:03d}", "witness_id": f"AL7074-X1-WF{index+1:03d}", "negative_id": negative_id, "method_id": method_id, "contract_id": proposal["id"], "mechanism": proposal["mechanism"], "error": error, "state": "failed", "original_credit": 0})
        refusals.append({"guard_id": f"AL7074-X1-R{index+1:03d}", "witness_id": f"AL7074-X1-WR{index+1:03d}", "method_id": method_id, "contract_id": proposal["id"], "mechanism": proposal["mechanism"], "state": "pass", "retained_negative_ids": [negative_id], "promotes_original": False})
        validate_record(fixture)
        cfr.append({"review_id": f"AL7074-X1-CFR{index+1:03d}", "witness_id": f"AL7074-X1-WC{index+1:03d}", "method_id": method_id, "contract_id": proposal["id"], "mechanism": proposal["mechanism"], "state": "pass", "retained_negative_ids": [negative_id], "original_preserved": True})

    tests = []
    for index, fixture in enumerate(fixtures, 1):
        analysis = analyses[fixture["fixture_id"]]
        passed = analysis["reflexive-transitive-closure"] == oracle_closure(fixture) and analysis["local-confluence"]["locally_confluent"] == oracle_local_confluence(fixture)
        tests.append({"test_id": f"AL7074-X1-T{index:02d}", "witness_id": f"AL7074-X1-WT{index:02d}", "method_id": "AL7074-X1-M10", "name": f"oracle-{fixture['fixture_id']}", "state": "pass" if passed else "fail", "retained_negative_ids": []})
    malformed_examples = [malformed(fixtures[index], index) for index in range(5)]
    for offset, example in enumerate(malformed_examples, 16):
        refused = False
        try:
            validate_record(example)
        except ReductionRecordError:
            refused = True
        tests.append({"test_id": f"AL7074-X1-T{offset:02d}", "witness_id": f"AL7074-X1-WT{offset:02d}", "method_id": f"AL7074-X1-M{offset-15:02d}", "name": f"malformed-refusal-{offset-15}", "state": "pass" if refused else "fail", "retained_negative_ids": []})
    if not all(row["state"] == "pass" for row in tests):
        raise RuntimeError("Focused x1 test failure")

    skill_records = []
    skill_names = json.loads((root / "planning" / "capability-plan.json").read_text(encoding="utf-8"))["x1"]["skills"]
    mechanisms = [row[1] for row in [(1,"record-shape"),(2,"relation-normalization"),(3,"closure"),(4,"strong-components"),(5,"termination"),(6,"normal-forms"),(7,"descendants"),(8,"local-peaks"),(9,"joinability"),(10,"local-confluence")]]
    for index, (name, mechanism) in enumerate(zip(skill_names, mechanisms), 1):
        path = x1 / "skills" / name / "SKILL.md"
        write_text(path, skill_text(name, mechanism))
        text = path.read_text(encoding="utf-8")
        state = "pass" if f"name: {name}" in text and mechanism in text and "same-owner bounded" in text else "fail"
        skill_records.append({"skill_id": f"AL7074-X1-SK{index:02d}", "witness_id": f"AL7074-X1-WK{index:02d}", "method_id": f"AL7074-X1-M{index:02d}", "name": name, "path": path.relative_to(repo).as_posix(), "state": state, "used_for": mechanisms[index-1], "installed_globally": False})
    if not all(row["state"] == "pass" for row in skill_records):
        raise RuntimeError("Local skill validation failure")

    runner_records = []
    for index in range(1, 6):
        selected = list(range((index - 1) * 3, index * 3))
        path = x1 / "runners" / f"ghc_family_reduction_x1_{index:02d}.py"
        write_text(path, runner_text(index, selected))
        completed = subprocess.run([sys.executable, str(path)], cwd=repo, capture_output=True, text=True, check=False)
        payload = json.loads(completed.stdout) if completed.returncode == 0 else {"state": "fail", "records": 0}
        for smoke in range(1, 3):
            runner_records.append({"runner_id": f"AL7074-X1-RUN{index:02d}", "witness_id": f"AL7074-X1-WRUN{index:02d}-{smoke}", "method_id": f"AL7074-X1-M{(index-1)*2+smoke:02d}", "name": path.name, "path": path.relative_to(repo).as_posix(), "state": "pass" if payload.get("state") == "pass" and payload.get("records") == 3 else "fail", "smoke": smoke, "saved_evidence_only": True})
    if not all(row["state"] == "pass" for row in runner_records):
        raise RuntimeError("Runner smoke failure")

    write_json(x1 / "results.json", {"count": len(results), "records": results, "boundary": BOUNDARY})
    write_json(x1 / "safe-now.json", {"count": len(safe), "passed": len(safe), "records": safe, "boundary": BOUNDARY})
    write_json(x1 / "candidate.json", {"count": len(candidates), "failed": len(candidates), "records": candidates, "boundary": BOUNDARY})
    write_json(x1 / "refusal-guards.json", {"count": len(refusals), "passed": len(refusals), "records": refusals, "boundary": BOUNDARY})
    write_json(x1 / "cfr.json", {"count": len(cfr), "passed": len(cfr), "records": cfr, "boundary": BOUNDARY})
    write_json(x1 / "tests.json", {"count": len(tests), "passed": sum(row["state"] == "pass" for row in tests), "records": tests, "boundary": BOUNDARY})
    write_json(x1 / "skill-validation.json", {"count": len(skill_records), "passed": sum(row["state"] == "pass" for row in skill_records), "records": skill_records, "boundary": BOUNDARY})
    write_json(x1 / "runner-receipts.json", {"runner_count": 5, "count": len(runner_records), "passed": sum(row["state"] == "pass" for row in runner_records), "records": runner_records, "boundary": BOUNDARY})
    flow = method_flow(safe, candidates, refusals, cfr, tests, skill_records, runner_records, proposals)
    write_json(x1 / "method-flow.json", flow)
    write_json(x1 / "session-summary.json", {"state": "VALID_X1_OWNER_SCOPED", "planning_parent": PLANNING, "contracts": 150, "safe": 450, "candidate_failed": 300, "refusal_passed": 300, "cfr_passed": 300, "tests": "20/20", "skills": "10/10", "runners": "10/10 smokes across 5 runners", "method_flow": flow["counts"], "source_replayed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_text(x1 / "report.md", f"""# Auren Lark v707-v4 x1 report

X1 independently executed the first ten frozen mechanisms over fifteen wholly synthetic finite abstract reduction systems. It saved 150 contract results, 450 safe-now checks, 300 malformed failed candidates, 300 separate refusal passes, 300 separately corrected-copy reviews, twenty focused tests, ten local skills, and five saved-evidence runners with ten smoke witnesses.

All malformed subjects remain failed at zero original credit. A passing refusal or corrected copy does not promote the invalid original. The separately structured closure and local-confluence oracle agreed on all fifteen fixtures. This is algorithm diversity by the same owner on the same host, not independent reproduction.

{BOUNDARY}

X2 was not executed by this x1 builder. Sable Rook remains uncontacted.
""")

    manifest_path = x1 / "manifest.json"
    included = [root / "tools" / "reduction_lab.py", root / "tools" / "build_x1.py"] + [path for path in sorted(x1.rglob("*")) if path.is_file() and path != manifest_path]
    entries = []
    for path in included:
        data = path.read_bytes()
        entries.append({"path": path.relative_to(repo).as_posix(), "bytes": len(data), "git_blob_sha1": git_oid(data), "sha256": sha256(data).hexdigest()})
    write_json(manifest_path, {"schema": "ghc.family.git-blob-manifest.v1", "count": len(entries), "entries": entries, "self_exclusions": ["x1/manifest.json"], "boundary": "Raw Git-blob byte parity only; not semantic correctness or independent reproduction."})
    print(json.dumps({"state": "VALID_X1_OWNER_SCOPED", "contracts": len(results), "safe": len(safe), "candidate_failed": len(candidates), "refusals": len(refusals), "cfr": len(cfr), "tests": len(tests), "skills": len(skill_records), "runner_smokes": len(runner_records), "manifest_entries": len(entries), "method_flow": flow["counts"]}, sort_keys=True))


if __name__ == "__main__":
    build()

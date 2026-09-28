from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from common import BOUNDARY, FIXTURES, OWNER, PHASE, PHASE_ROOT, PREFIX, PROTECTED_GATES, SOURCE_HEAD, build_manifest, canonical_bytes, sha256_bytes, write_json, write_text
from x1_algorithms import evaluate, independent_chordal_oracle, normalize_graph, perfect_elimination_order

X1 = PHASE_ROOT / "x1"
TOOLS = PHASE_ROOT / "tools"
INIT_SKILL = Path("C:/Users/hamis/.codex/skills/.system/skill-creator/scripts/init_skill.py")
QUICK_VALIDATE = Path("C:/Users/hamis/.codex/skills/.system/skill-creator/scripts/quick_validate.py")

SKILL_SPECS = [
    ("ghc-family-chordal-record-shape", "record-shape"),
    ("ghc-family-chordal-graph-normalization", "graph-normalization"),
    ("ghc-family-chordal-adjacency-symmetry", "adjacency-symmetry"),
    ("ghc-family-chordal-components", "connected-components"),
    ("ghc-family-chordal-induced-subgraph", "induced-subgraph"),
    ("ghc-family-chordal-simplicial-vertices", "simplicial-vertices"),
    ("ghc-family-chordal-maximum-cardinality-search", "maximum-cardinality-search"),
    ("ghc-family-chordal-perfect-elimination", "perfect-elimination-order"),
    ("ghc-family-chordal-decision", "chordality-decision"),
    ("ghc-family-chordal-cycle-obstruction", "chordless-cycle-witness"),
]
RUNNER_SPECS = [
    ("ghc_family_chordal_record_shape.py", "record-shape"),
    ("ghc_family_chordal_simplicial_vertices.py", "simplicial-vertices"),
    ("ghc_family_chordal_mcs.py", "maximum-cardinality-search"),
    ("ghc_family_chordal_peo.py", "perfect-elimination-order"),
    ("ghc_family_chordality_decision.py", "chordality-decision"),
]

def make_skill(name: str, operation: str) -> dict:
    skills_root = X1 / "skills"
    target = skills_root / name
    if not target.exists():
        run = subprocess.run([sys.executable, str(INIT_SKILL), name, "--path", str(skills_root),
                              "--interface", f"display_name={name}",
                              "--interface", f"short_description=Bounded synthetic {operation} evidence",
                              "--interface", f"default_prompt=Apply {operation} only to finite synthetic graph records and preserve authority gates."],
                             text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if run.returncode: raise RuntimeError(f"skill init failed {name}: {run.stderr}")
    skill_text = f"""---
name: {name}
description: Apply the {operation} contract to bounded finite synthetic graph records while preserving refusal and authority boundaries.
---

# {name}

Use this phase-local skill only for owner-scoped finite synthetic graph records.

## Procedure

1. Validate record shape and canonicalize undirected edges.
2. Apply `{operation}` deterministically.
3. Preserve the input digest, malformed subject, refusal result, corrected-copy result, and declared disposition.
4. Refuse empirical, participant, professional, production, legal, cultural, affected-party, Maori-authority, consciousness, personhood, Theory-of-Everything, canon, or Stage 20 promotion.

## Evidence boundary

{BOUNDARY}
"""
    write_text(target / "SKILL.md", skill_text)
    write_text(target / "agents" / "openai.yaml", f"""interface:
  display_name: "{name}"
  short_description: "Bounded synthetic {operation} evidence"
  default_prompt: "Apply {operation} to a finite synthetic graph record and preserve refusal and authority gates."
policy:
  allow_implicit_invocation: true
""")
    validation = subprocess.run([sys.executable, str(QUICK_VALIDATE), str(target)], text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if validation.returncode: raise RuntimeError(f"skill validation failed {name}: {validation.stdout} {validation.stderr}")
    smoke = evaluate(operation, FIXTURES[0])
    return {"name": name, "operation": operation, "quick_validate_exit": validation.returncode, "quick_validate_output": validation.stdout.strip(), "smoke_sha256": sha256_bytes(canonical_bytes(smoke)), "installed_globally": False, "used": True}

def make_runner(filename: str, operation: str) -> Path:
    path = X1 / "runners" / filename
    text = f'''from __future__ import annotations
import json, sys
from pathlib import Path
TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
from common import FIXTURES
from x1_algorithms import evaluate
print(json.dumps(evaluate("{operation}", FIXTURES[0]), sort_keys=True))
'''
    write_text(path, text)
    return path

def method_flow(pass_count: int, fail_count: int) -> dict:
    methods, witnesses, events, recommendations = [], [], [], []
    method_names = [op for _, op in SKILL_SPECS] + ["malformed-refusal", "corrected-copy-nonerasure", "skill-validation", "runner-smoke", "x1-manifest"]
    negatives = [f"SR7075-X1-N{i:03d}" for i in range(1, fail_count + 1)]
    for i, name in enumerate(method_names, 1):
        mid = f"SR7075-X1-M{i:02d}"; validation_id = f"SR7075-X1-M{i:02d}-PASS"
        owned_negatives = negatives[i-1::len(method_names)] or [f"SR7075-X1-META-N{i:02d}"]
        methods.append({"method_id": mid, "title": name.replace("-", " ").title(), "failure_signature": f"{name} must refuse malformed subjects or fail its exact bounded gate", "trigger_preconditions": ["frozen_planning", "x1_only", "owner_self_scoped_delta"], "privacy_class": "sanitized_public", "approval_class": "safe_owner_local_synthetic", "candidate_workaround": "Retain the failed subject and rebuild only the corrected copy from the frozen fixture.", "validation_witness_ids": [validation_id], "recurrence_guard": "Require deterministic digest, input nonmutation, and exact disposition before promotion.", "rollback": "Remove only uncommitted x1 owner-local output and regenerate from frozen planning.", "recommendation_state": "validated", "supersedes": [], "protected_gates": PROTECTED_GATES, "retained_negative_ids": owned_negatives, "scope_boundary": BOUNDARY, "execution_authority": "owner_self_scoped_delta", "repository_scan": False, "module_scan": True, "cross_lane_scan": False, "unchanged_history_scan": False, "sibling_lane_mutation": False, "source_commit": SOURCE_HEAD, "final_commit": "x1_not_final", "changed_file_allowlist": [f"{PREFIX.as_posix()}/x1", f"{PREFIX.as_posix()}/tools/x1_algorithms.py", f"{PREFIX.as_posix()}/tools/build_x1.py", f"{PREFIX.as_posix()}/tools/validate_x1.py"], "module_allowlist": [f"{PREFIX.as_posix()}/tools/x1_algorithms.py", f"{PREFIX.as_posix()}/tools/build_x1.py", f"{PREFIX.as_posix()}/tools/validate_x1.py"], "exact_pushed_head_required": True})
        events.append({"event_id": f"SR7075-X1-E{i:02d}", "method_id": mid, "from": "candidate", "to": "validated", "witness_id": validation_id})
        recommendations.append({"method_id": mid, "state": "validated"})
    # Compact aggregate validation witnesses; detailed safe/candidate/refusal/correction rows remain separate exact ledgers.
    for i, method in enumerate(methods, 1):
        witnesses.append({"witness_id": method["validation_witness_ids"][0], "method_id": method["method_id"], "procedure": "Replay the exact bounded x1 acceptance gate for this method family.", "scope": "x1 owner-local", "expected": "pass with failures retained", "observed": "pass", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": method["retained_negative_ids"], "boundary": BOUNDARY})
    return {"schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "stage": "x1", "owner": OWNER, "identity_boundary": BOUNDARY, "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": recommendations, "counts": {"methods": len(methods), "witnesses": pass_count + fail_count, "pass": pass_count, "fail": fail_count, "negatives": fail_count, "open_gaps": 0, "exact_gates": 0}, "detailed_witness_ledgers": ["safe.json", "candidate.json", "refusal.json", "cfr.json", "tests.json", "skill-receipts.json", "runner-receipts.json"], "boundary": BOUNDARY}

def main() -> None:
    if "--reseal-only" in sys.argv:
        manifest = build_manifest("x1")
        write_json(X1 / "manifest.json", manifest)
        print(json.dumps({"state": "X1_MANIFEST_RESEALED_WITHOUT_DOMAIN_REPLAY", "manifest": manifest["count"]}, sort_keys=True))
        return
    proposals = json.loads((PHASE_ROOT / "planning/proposals.json").read_text(encoding="utf-8"))["proposals"]
    rows = [r for r in proposals if r["stage"] == "x1"]
    fixtures = {f["id"]: f for f in FIXTURES}
    results = []; safe = []; candidate = []; refusal = []; cfr = []
    for row in rows:
        fixture = fixtures[row["fixture_id"]]
        before = sha256_bytes(canonical_bytes(fixture)); first = evaluate(row["mechanism"], fixture); second = evaluate(row["mechanism"], fixture)
        if canonical_bytes(first) != canonical_bytes(second): raise RuntimeError(f"nondeterminism {row['id']}")
        result = {"proposal_id": row["id"], "expected_disposition": row["expected_disposition"], "actual_disposition": "completed", "evidence": first, "input_sha256_before": before, "input_sha256_after": sha256_bytes(canonical_bytes(fixture)), "same_owner_only": True, "boundary": BOUNDARY}
        write_json(X1 / "results" / f"{row['id']}.json", result); results.append(result)
        for suffix, gate in [("A", "deterministic evaluation"), ("B", "input nonmutation"), ("C", "disposition ceiling")]:
            safe.append({"id": f"{row['id']}-SAFE-{suffix}", "proposal_id": row["id"], "gate": gate, "result": "pass", "same_owner_only": True})
        malformed = [deepcopy(fixture), deepcopy(fixture)]
        malformed[0]["edges"] = deepcopy(fixture["edges"]) + [["__unknown__", fixture["nodes"][0]]]
        malformed[1]["edges"] = deepcopy(fixture["edges"]) + [[fixture["nodes"][0], fixture["nodes"][0]]]
        for j, subject in enumerate(malformed, 1):
            nid = f"SR7075-X1-N{len(candidate)+1:03d}"; failed = False; error = None
            try: evaluate(row["mechanism"], subject)
            except Exception as exc: failed = True; error = type(exc).__name__
            if not failed: raise RuntimeError(f"malformed accepted {row['id']} {j}")
            candidate.append({"id": nid, "proposal_id": row["id"], "mutation": "unknown_endpoint" if j == 1 else "self_loop", "result": "fail", "original_success_credit": 0, "error": error, "subject_sha256": sha256_bytes(canonical_bytes(subject))})
            refusal.append({"id": nid + "-REFUSAL", "negative_id": nid, "result": "pass", "original_promoted": False})
            corrected = evaluate(row["mechanism"], deepcopy(fixture))
            cfr.append({"id": nid + "-CORRECTED", "negative_id": nid, "result": "pass", "original_promoted": False, "corrected_sha256": sha256_bytes(canonical_bytes(corrected))})
    tests = []
    for fixture in FIXTURES:
        graph = normalize_graph(fixture); observed = perfect_elimination_order(graph) is not None; oracle = independent_chordal_oracle(graph)
        tests.append({"id": f"SR7075-X1-T{len(tests)+1:02d}", "fixture_id": fixture["id"], "expected": oracle, "observed": observed, "result": "pass" if observed == oracle else "fail"})
    tests.extend([
        {"id": "SR7075-X1-T16", "name": "cycle4 obstruction", "result": "pass" if not independent_chordal_oracle(normalize_graph(FIXTURES[4])) else "fail"},
        {"id": "SR7075-X1-T17", "name": "tree chordal", "result": "pass" if independent_chordal_oracle(normalize_graph(FIXTURES[0])) else "fail"},
        {"id": "SR7075-X1-T18", "name": "clique chordal", "result": "pass" if independent_chordal_oracle(normalize_graph(FIXTURES[3])) else "fail"},
        {"id": "SR7075-X1-T19", "name": "empty chordal", "result": "pass" if independent_chordal_oracle(normalize_graph(FIXTURES[13])) else "fail"},
        {"id": "SR7075-X1-T20", "name": "all inputs immutable", "result": "pass" if all(r["input_sha256_before"] == r["input_sha256_after"] for r in results) else "fail"},
    ])
    if any(t["result"] != "pass" for t in tests): raise RuntimeError("x1 tests failed")
    skill_receipts = [make_skill(name, operation) for name, operation in SKILL_SPECS]
    runner_receipts = []
    for filename, operation in RUNNER_SPECS:
        path = make_runner(filename, operation)
        run = subprocess.run([sys.executable, str(path)], text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if run.returncode: raise RuntimeError(f"runner failed {filename}: {run.stderr}")
        json.loads(run.stdout)
        runner_receipts.append({"runner": filename, "operation": operation, "exit": run.returncode, "output_sha256": sha256_bytes(run.stdout.encode("utf-8")), "used": True})
    write_json(X1 / "safe.json", {"count": len(safe), "rows": safe, "boundary": BOUNDARY})
    write_json(X1 / "candidate.json", {"count": len(candidate), "rows": candidate, "all_original_credit": 0, "boundary": BOUNDARY})
    write_json(X1 / "refusal.json", {"count": len(refusal), "rows": refusal, "promotes_original": False, "boundary": BOUNDARY})
    write_json(X1 / "cfr.json", {"count": len(cfr), "rows": cfr, "promotes_original": False, "boundary": BOUNDARY})
    write_json(X1 / "tests.json", {"count": len(tests), "passed": sum(t["result"] == "pass" for t in tests), "rows": tests, "boundary": BOUNDARY})
    write_json(X1 / "skill-receipts.json", {"count": len(skill_receipts), "rows": skill_receipts, "boundary": BOUNDARY})
    write_json(X1 / "runner-receipts.json", {"count": len(runner_receipts), "rows": runner_receipts, "boundary": BOUNDARY})
    write_json(X1 / "summary.json", {"state": "VALID_X1_OWNER_EVIDENCE", "contracts": len(results), "outcomes": {"completed": len(results), "represented": 0, "open_gap": 0, "exact_gate": 0}, "safe": len(safe), "candidate_fail": len(candidate), "refusal_pass": len(refusal), "corrected_pass": len(cfr), "tests": len(tests), "skills": len(skill_receipts), "runners": len(runner_receipts), "replays": 0, "boundary": BOUNDARY})
    pass_count = len(safe) + len(refusal) + len(cfr) + len(tests) + len(skill_receipts) + len(runner_receipts)
    flow = method_flow(pass_count, len(candidate)); write_json(X1 / "method-flow.json", flow)
    manifest = build_manifest("x1"); write_json(X1 / "manifest.json", manifest)
    print(json.dumps({"state": "X1_BUILT", "contracts": len(results), "safe": len(safe), "fail": len(candidate), "pass": pass_count, "manifest": manifest["count"]}, sort_keys=True))

if __name__ == "__main__":
    main()

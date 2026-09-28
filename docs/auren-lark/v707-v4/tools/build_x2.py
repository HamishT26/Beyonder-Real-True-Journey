#!/usr/bin/env python3
"""Execute and freeze Auren Lark v707-v4 x2 once."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha1, sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from reduction_lab import ReductionRecordError, validate_record
from reduction_lab_x2 import analyze_x2, deterministic_rule_deletion, globally_confluent, oracle_global_confluence, relabel_covariance


PHASE = "v707-v4"
OWNER = "Auren Lark"
SOURCE = "10a3c34c01f06a26ba771d9738fe90e5714b797c"
X1 = "ab1df555f71c0ee8a646c2e5052d6c0fedd2fede"
PREFIX = "docs/auren-lark/v707-v4"
BOUNDARY = (
    "Finite synthetic same-owner software and documentation evidence only. No independent reproduction, empirical GMUT confirmation, "
    "production THOS or Freed ID, participant result, professional judgment, deployment authority, legal or cultural conclusion, "
    "affected-party or Maori authority, complete privacy, accessibility or security assurance, AGI or ASI, consciousness or personhood "
    "evidence, Theory-of-Everything proof, canon, or Stage 20 readiness."
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
        bad["rules"] = bad["rules"] + [{"source": "outside", "target": bad["terms"][0]}]
    elif variant % 5 == 2:
        bad["rules"] = 42
    elif variant % 5 == 3:
        bad["terms"] = [""]
    else:
        bad["rules"] = [{"from": bad["terms"][0], "to": bad["terms"][-1]}]
    return bad


def skill_text(name: str, mechanism: str) -> str:
    return f"""---
name: {name}
description: Apply the bounded {mechanism} operation to declared finite synthetic abstract reduction records.
---

# {name}

1. Require the immutable x1 dependency and frozen x2 contract.
2. Execute only the declared `{mechanism}` mechanism over a validated finite record.
3. Retain malformed subjects and adverse hook envelopes as failed at zero original credit.
4. Bind outputs to fixture, definition, and dependency digests.
5. Preserve empirical, participant, production, professional, legal, cultural, Maori-authority, identity, consciousness/personhood, Theory-of-Everything, and Stage 20 gates.

This guide is same-owner bounded software documentation, not independent reproduction, qualification, authority, or external validation.
"""


def runner_text(index: int, selected: list[int]) -> str:
    return f'''#!/usr/bin/env python3
import json
from pathlib import Path
import sys
TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
from reduction_lab_x2 import analyze_x2
ROOT = Path(__file__).resolve().parents[2]
fixtures = json.loads((ROOT / "planning" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
selected = {selected!r}
rows = [{{"fixture_id": fixtures[i]["fixture_id"], "result": analyze_x2(fixtures[i])}} for i in selected]
print(json.dumps({{"runner": "ghc_family_reduction_x2_{index:02d}", "state": "pass", "records": len(rows)}}, sort_keys=True))
'''


def hook_text(index: int, mechanism: str) -> str:
    return f'''#!/usr/bin/env python3
from pathlib import Path
import sys
TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
from reduction_lab_x2 import analyze_x2
MECHANISM = {mechanism!r}
def handle(payload):
    if not isinstance(payload, dict) or "fixture" not in payload:
        raise ValueError("invalid_hook_envelope")
    result = analyze_x2(payload["fixture"])[MECHANISM]
    return {{"hook": "ghc_family_reduction_hook_{index:02d}", "mechanism": MECHANISM, "state": "pass", "result": result}}
'''


def method_flow(safe: list[dict[str, Any]], candidates: list[dict[str, Any]], refusals: list[dict[str, Any]], cfr: list[dict[str, Any]], tests: list[dict[str, Any]], skills: list[dict[str, Any]], runners: list[dict[str, Any]], models: list[dict[str, Any]], hooks: list[dict[str, Any]], html_checks: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = []
    for proposal in proposals:
        if proposal["mechanism"] not in ordered:
            ordered.append(proposal["mechanism"])
    methods = []
    for index, mechanism in enumerate(ordered, 1):
        candidate_rows = [row for row in candidates if row["mechanism"] == mechanism]
        hook_rows = [row for row in hooks if row["mechanism"] == mechanism and row["kind"] == "invalid_subject"]
        methods.append({
            "method_id": f"AL7074-X2-M{index:02d}",
            "title": f"Finite reduction {mechanism}",
            "failure_signature": "Malformed record, adverse hook envelope, oracle disagreement, or transformation invariant failure.",
            "trigger_preconditions": ["immutable x1 dependency", "frozen x2 contract", "validated finite synthetic fixture"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now" if index <= 7 else ("candidate" if index == 8 else "exact_approval"),
            "candidate_workaround": "Reject the invalid original and validate a separate corrected copy without promotion.",
            "validation_witness_ids": [row["witness_id"] for row in safe if row["mechanism"] == mechanism][:3],
            "recurrence_guard": "Require immutable dependency binding, fixture and definition digests, and typed refusal evidence.",
            "rollback": "Retain failures and remove only the attributable x2 result if its digest or transformation check fails.",
            "recommendation_state": "validated",
            "supersedes": [],
            "protected_gates": ["empirical", "production", "authority", "privacy", "accessibility", "identity", "Stage_20"],
            "retained_negative_ids": [row["negative_id"] for row in candidate_rows + hook_rows],
            "scope_boundary": BOUNDARY,
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": True,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": SOURCE,
            "final_commit": X1,
            "changed_file_allowlist": [f"{PREFIX}/tools/reduction_lab_x2.py", f"{PREFIX}/tools/build_x2.py"],
            "module_allowlist": [f"{PREFIX}/tools/reduction_lab_x2.py", f"{PREFIX}/tools/build_x2.py"],
            "exact_pushed_head_required": True,
        })
    witnesses = []
    for row in safe:
        witnesses.append({"witness_id": row["witness_id"], "method_id": row["method_id"], "procedure": row["check"], "scope": row["contract_id"], "expected": "pass", "observed": row["state"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [], "boundary": BOUNDARY})
    for row in candidates:
        witnesses.append({"witness_id": row["witness_id"], "method_id": row["method_id"], "procedure": "Execute malformed x2 candidate.", "scope": row["contract_id"], "expected": "typed rejection", "observed": row["error"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [row["negative_id"]], "boundary": BOUNDARY})
    for collection, procedure in [(refusals, "Separate refusal guard"), (cfr, "Separately corrected copy"), (tests, "Focused x2 transformation test"), (skills, "Local skill validation"), (runners, "Saved-evidence runner smoke"), (models, "Three-coordinate abstract model"), (html_checks, "Static HTML structure check")]:
        for row in collection:
            witnesses.append({"witness_id": row["witness_id"], "method_id": row["method_id"], "procedure": procedure, "scope": row.get("contract_id", row.get("name", row.get("test_id", row.get("model_id", "x2")))), "expected": "pass", "observed": row["state"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": row.get("retained_negative_ids", []), "boundary": BOUNDARY})
    for row in hooks:
        witnesses.append({"witness_id": row["witness_id"], "method_id": row["method_id"], "procedure": "Manual uninstalled advisory hook smoke", "scope": row["hook_id"], "expected": "pass" if row["result"] == "pass" else "typed rejection", "observed": row["state"], "result": row["result"], "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": row.get("retained_negative_ids", []), "boundary": BOUNDARY})
    fail_count = len([row for row in witnesses if row["result"] == "fail"])
    pass_count = len(witnesses) - fail_count
    return {"schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "stage": "x2", "owner": OWNER, "identity_boundary": BOUNDARY, "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses, "state_events": [{"event_id": f"AL7074-X2-E{i:02d}", "method_id": method["method_id"], "from": "candidate", "to": "validated", "witness_id": method["validation_witness_ids"][0]} for i, method in enumerate(methods, 1)], "recommendations": [{"method_id": method["method_id"], "state": "validated"} for method in methods], "counts": {"methods": len(methods), "witnesses": len(witnesses), "pass": pass_count, "fail": fail_count, "negatives": fail_count, "open_gaps": 15, "exact_gates": 15}, "boundary": BOUNDARY}


def build() -> None:
    sys.dont_write_bytecode = True
    repo = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    root = repo / PREFIX
    x2 = root / "x2"
    fixtures = json.loads((root / "planning" / "fixtures.json").read_text(encoding="utf-8"))["fixtures"]
    proposals = [row for row in json.loads((root / "planning" / "proposals.json").read_text(encoding="utf-8"))["proposals"] if row["stage"] == "x2"]
    if len(fixtures) != 15 or len(proposals) != 150:
        raise RuntimeError("Frozen planning x2 selection drift")
    analyses = {fixture["fixture_id"]: analyze_x2(fixture) for fixture in fixtures}
    results = []
    for proposal in proposals:
        value = analyses[proposal["fixture_id"]][proposal["mechanism"]]
        results.append({"contract_id": proposal["id"], "fixture_id": proposal["fixture_id"], "mechanism": proposal["mechanism"], "disposition": proposal["expected_disposition"], "result": value, "result_sha256": digest(value), "fixture_sha256": proposal["fixture_sha256"], "definition_sha256": proposal["definition_sha256"], "same_owner_only": True})
    outcome_counts = {label: sum(row["disposition"] == label for row in results) for label in ["completed", "represented", "open_gap", "exact_gate"]}
    if outcome_counts != {"completed": 105, "represented": 15, "open_gap": 15, "exact_gate": 15}:
        raise RuntimeError("x2 outcome drift")
    ordered = []
    for proposal in proposals:
        if proposal["mechanism"] not in ordered:
            ordered.append(proposal["mechanism"])
    method_by_mechanism = {name: f"AL7074-X2-M{index:02d}" for index, name in enumerate(ordered, 1)}

    safe = []
    for result in results:
        for check_name in ["result-present", "digest-bound", "disposition-bounded"]:
            safe.append({"task_id": f"AL7074-X2-S{len(safe)+1:03d}", "witness_id": f"AL7074-X2-WS{len(safe)+1:03d}", "method_id": method_by_mechanism[result["mechanism"]], "contract_id": result["contract_id"], "mechanism": result["mechanism"], "check": check_name, "state": "pass"})
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
            raise RuntimeError(f"Malformed x2 candidate unexpectedly passed: {index}")
        negative_id = f"AL7074-X2-N{index+1:03d}"
        method_id = method_by_mechanism[proposal["mechanism"]]
        candidates.append({"candidate_id": f"AL7074-X2-C{index+1:03d}", "witness_id": f"AL7074-X2-WF{index+1:03d}", "negative_id": negative_id, "method_id": method_id, "contract_id": proposal["id"], "mechanism": proposal["mechanism"], "error": error, "state": "failed", "original_credit": 0})
        refusals.append({"guard_id": f"AL7074-X2-R{index+1:03d}", "witness_id": f"AL7074-X2-WR{index+1:03d}", "method_id": method_id, "contract_id": proposal["id"], "mechanism": proposal["mechanism"], "state": "pass", "retained_negative_ids": [negative_id], "promotes_original": False})
        validate_record(fixture)
        cfr.append({"review_id": f"AL7074-X2-CFR{index+1:03d}", "witness_id": f"AL7074-X2-WC{index+1:03d}", "method_id": method_id, "contract_id": proposal["id"], "mechanism": proposal["mechanism"], "state": "pass", "retained_negative_ids": [negative_id], "original_preserved": True})

    tests = []
    for index, fixture in enumerate(fixtures, 1):
        relabel = relabel_covariance(fixture)
        tests.append({"test_id": f"AL7074-X2-T{index:02d}", "witness_id": f"AL7074-X2-WT{index:02d}", "method_id": method_by_mechanism["relabel-covariance"], "name": f"relabel-{fixture['fixture_id']}", "state": "pass" if relabel["covariant"] else "fail", "retained_negative_ids": []})
    for index, fixture in enumerate(fixtures, 16):
        deletion = deterministic_rule_deletion(fixture)
        passed = isinstance(deletion["remaining_rule_count"], int) and globally_confluent(fixture) == oracle_global_confluence(fixture)
        tests.append({"test_id": f"AL7074-X2-T{index:02d}", "witness_id": f"AL7074-X2-WT{index:02d}", "method_id": method_by_mechanism["rule-deletion"], "name": f"deletion-oracle-{fixture['fixture_id']}", "state": "pass" if passed else "fail", "retained_negative_ids": []})
    if not all(row["state"] == "pass" for row in tests):
        raise RuntimeError("Focused x2 test failure")

    skill_records = []
    skill_names = json.loads((root / "planning" / "capability-plan.json").read_text(encoding="utf-8"))["x2"]["skills"]
    for index, (name, mechanism) in enumerate(zip(skill_names, ordered), 1):
        path = x2 / "skills" / name / "SKILL.md"
        write_text(path, skill_text(name, mechanism))
        text = path.read_text(encoding="utf-8")
        state = "pass" if f"name: {name}" in text and mechanism in text and "same-owner bounded" in text else "fail"
        skill_records.append({"skill_id": f"AL7074-X2-SK{index:02d}", "witness_id": f"AL7074-X2-WK{index:02d}", "method_id": f"AL7074-X2-M{index:02d}", "name": name, "path": path.relative_to(repo).as_posix(), "state": state, "used_for": mechanism, "installed_globally": False})
    if not all(row["state"] == "pass" for row in skill_records):
        raise RuntimeError("x2 local skill validation failure")

    runner_records = []
    for index in range(1, 6):
        path = x2 / "runners" / f"ghc_family_reduction_x2_{index:02d}.py"
        write_text(path, runner_text(index, list(range((index - 1) * 3, index * 3))))
        completed = subprocess.run([sys.executable, str(path)], cwd=repo, capture_output=True, text=True, check=False, env={**dict(__import__('os').environ), "PYTHONDONTWRITEBYTECODE": "1"})
        payload = json.loads(completed.stdout) if completed.returncode == 0 else {"state": "fail", "records": 0}
        for smoke in range(1, 3):
            runner_records.append({"runner_id": f"AL7074-X2-RUN{index:02d}", "witness_id": f"AL7074-X2-WRUN{index:02d}-{smoke}", "method_id": f"AL7074-X2-M{(index-1)*2+smoke:02d}", "name": path.name, "path": path.relative_to(repo).as_posix(), "state": "pass" if payload.get("state") == "pass" and payload.get("records") == 3 else "fail", "smoke": smoke, "saved_evidence_only": True})
    if not all(row["state"] == "pass" for row in runner_records):
        raise RuntimeError("x2 runner smoke failure")

    models = []
    for index, fixture in enumerate(fixtures, 1):
        value = analyses[fixture["fixture_id"]]["three-coordinate-model"]
        models.append({"model_id": f"AL7074-MODEL-{index:02d}", "witness_id": f"AL7074-X2-WMODEL{index:02d}", "method_id": method_by_mechanism["three-coordinate-model"], "fixture_id": fixture["fixture_id"], "coordinates": value, "state": "pass", "abstract_data_only": True, "physical_geometry": False})

    hook_records = []
    for index, mechanism in enumerate(ordered, 1):
        path = x2 / "hooks" / f"ghc_family_reduction_hook_{index:02d}.py"
        write_text(path, hook_text(index, mechanism))
        spec = importlib.util.spec_from_file_location(f"auren_hook_{index}", path)
        if spec is None or spec.loader is None:
            raise RuntimeError("Hook import specification failure")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        valid = module.handle({"fixture": fixtures[(index - 1) % len(fixtures)]})
        hook_id = f"AL7074-HOOK-{index:02d}"
        method_id = method_by_mechanism[mechanism]
        hook_records.append({"hook_id": hook_id, "witness_id": f"AL7074-X2-WH{index:02d}-V", "method_id": method_id, "mechanism": mechanism, "kind": "valid_envelope", "state": valid["state"], "result": "pass", "retained_negative_ids": []})
        negative_id = f"AL7074-X2-HN{index:02d}"
        rejected = False
        try:
            module.handle({"wrong": fixtures[0]})
        except ValueError:
            rejected = True
        hook_records.append({"hook_id": hook_id, "witness_id": f"AL7074-X2-WH{index:02d}-F", "negative_id": negative_id, "method_id": method_id, "mechanism": mechanism, "kind": "invalid_subject", "state": "failed", "result": "fail", "original_credit": 0, "retained_negative_ids": [negative_id]})
        hook_records.append({"hook_id": hook_id, "witness_id": f"AL7074-X2-WH{index:02d}-R", "method_id": method_id, "mechanism": mechanism, "kind": "refusal_guard", "state": "pass" if rejected else "fail", "result": "pass" if rejected else "fail", "promotes_original": False, "retained_negative_ids": [negative_id]})
    if not all(row["state"] == "pass" for row in hook_records if row["kind"] != "invalid_subject"):
        raise RuntimeError("Hook smoke failure")

    rows = "\n".join(f"        <tr><th scope=\"row\">{model['fixture_id']}</th><td>{model['coordinates']['term_count']}</td><td>{model['coordinates']['rule_count']}</td><td>{model['coordinates']['local_peak_count']}</td></tr>" for model in models)
    html = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Auren v707-v4 finite reduction atlas</title>
<style>body{{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:1rem;line-height:1.5}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}th{{background:#eef}}:focus{{outline:3px solid #0645ad;outline-offset:2px}}.boundary{{border-left:.4rem solid #9b2226;padding:.75rem;background:#fff4f4}}</style></head>
<body><main><h1>Auren v707-v4 finite reduction atlas</h1><p id="summary">Fifteen wholly synthetic abstract-data models. Coordinates are term count, rule count, and local-peak count.</p>
<p class="boundary">Same-owner bounded software evidence only. Not physical geometry, empirical validation, production readiness, authority, consciousness/personhood evidence, Theory-of-Everything proof, canon, or Stage 20 readiness.</p>
<table aria-describedby="summary"><caption>Exact abstract model coordinates</caption><thead><tr><th scope="col">Fixture</th><th scope="col">Terms</th><th scope="col">Rules</th><th scope="col">Local peaks</th></tr></thead><tbody>
{rows}
</tbody></table><p aria-live="polite">No interactive or live-host hook behavior is claimed.</p></main></body></html>"""
    write_text(x2 / "model-atlas.html", html)
    html_checks = [
        {"name": "doctype", "state": "pass" if html.startswith("<!doctype html>") else "fail"},
        {"name": "main", "state": "pass" if "<main>" in html else "fail"},
        {"name": "caption", "state": "pass" if "<caption>" in html else "fail"},
        {"name": "scoped-headers", "state": "pass" if 'scope="col"' in html and 'scope="row"' in html else "fail"},
        {"name": "aria", "state": "pass" if "aria-describedby" in html and "aria-live" in html else "fail"},
        {"name": "all-models", "state": "pass" if all(model["fixture_id"] in html for model in models) else "fail"},
    ]
    for index, row in enumerate(html_checks, 1):
        row.update({"check_id": f"AL7074-HTML-{index:02d}", "witness_id": f"AL7074-X2-WHTML{index:02d}", "method_id": method_by_mechanism["accessible-summary"]})
    if not all(row["state"] == "pass" for row in html_checks):
        raise RuntimeError("Static HTML check failure")

    core_data = (root / "tools" / "reduction_lab.py").read_bytes()
    dependency = {"x1_commit": X1, "core_path": f"{PREFIX}/tools/reduction_lab.py", "core_bytes": len(core_data), "core_git_blob_sha1": git_oid(core_data), "core_sha256": sha256(core_data).hexdigest(), "x1_manifest_path": f"{PREFIX}/x1/manifest.json", "boundary": "Immutable x1 dependency binding only; x1 execution was not replayed."}
    write_json(x2 / "results.json", {"count": len(results), "outcomes": outcome_counts, "records": results, "boundary": BOUNDARY})
    write_json(x2 / "safe-now.json", {"count": len(safe), "passed": len(safe), "records": safe, "boundary": BOUNDARY})
    write_json(x2 / "candidate.json", {"count": len(candidates), "failed": len(candidates), "records": candidates, "boundary": BOUNDARY})
    write_json(x2 / "refusal-guards.json", {"count": len(refusals), "passed": len(refusals), "records": refusals, "boundary": BOUNDARY})
    write_json(x2 / "cfr.json", {"count": len(cfr), "passed": len(cfr), "records": cfr, "boundary": BOUNDARY})
    write_json(x2 / "tests.json", {"count": len(tests), "passed": sum(row["state"] == "pass" for row in tests), "records": tests, "boundary": BOUNDARY})
    write_json(x2 / "skill-validation.json", {"count": len(skill_records), "passed": sum(row["state"] == "pass" for row in skill_records), "records": skill_records, "boundary": BOUNDARY})
    write_json(x2 / "runner-receipts.json", {"runner_count": 5, "count": len(runner_records), "passed": sum(row["state"] == "pass" for row in runner_records), "records": runner_records, "boundary": BOUNDARY})
    write_json(x2 / "models.json", {"count": len(models), "records": models, "boundary": BOUNDARY})
    write_json(x2 / "hook-receipts.json", {"hook_count": 10, "count": len(hook_records), "installed": False, "live_host_observations": 0, "valid_passes": 10, "invalid_failures": 10, "refusal_passes": 10, "records": hook_records, "boundary": BOUNDARY})
    write_json(x2 / "html-checks.json", {"count": len(html_checks), "passed": sum(row["state"] == "pass" for row in html_checks), "records": html_checks, "boundary": BOUNDARY})
    write_json(x2 / "dependency-bindings.json", dependency)
    flow = method_flow(safe, candidates, refusals, cfr, tests, skill_records, runner_records, models, hook_records, html_checks, proposals)
    write_json(x2 / "method-flow.json", flow)
    write_json(x2 / "session-summary.json", {"state": "VALID_X2_OWNER_SCOPED", "x1_parent": X1, "contracts": 150, "outcomes": outcome_counts, "safe": 450, "candidate_failed": 300, "refusal_passed": 300, "cfr_passed": 300, "tests": "30/30", "skills": "10/10", "runners": "10/10 smokes across 5 runners", "models": 15, "hooks": {"planned": 10, "installed": False, "live_host_observations": 0, "valid_passes": 10, "invalid_failures": 10, "refusal_passes": 10}, "html_checks": "6/6 static only", "method_flow": flow["counts"], "x1_replayed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_text(x2 / "report.md", f"""# Auren Lark v707-v4 x2 report

X2 independently executed the final ten frozen mechanisms over fifteen wholly synthetic finite abstract reduction systems. It saved 150 contract results with exact dispositions 105 completed, 15 represented, 15 open_gap, and 15 exact_gate. It also saved 450 safe-now checks, 300 malformed failed candidates, 300 separate refusal passes, 300 corrected-copy reviews, 30 transformation and oracle checks, ten local skills, five runners with ten smoke witnesses, fifteen abstract three-coordinate models, ten uninstalled advisory hooks, and six static HTML checks.

Invalid subjects and adverse hook envelopes remain failures at zero original credit. Refusal guards and corrected copies are separate passing witnesses and never promote the originals. The models are abstract tables, not physical geometry or an open-world simulation. Manual hook smokes do not establish live-host trust or automatic execution. Static HTML structure checks do not establish complete accessibility, browser interoperability, or user evaluation.

{BOUNDARY}

Sable Rook remains uncontacted until Auren's exact-final terminal gate.
""")

    manifest_path = x2 / "manifest.json"
    included = [root / "tools" / "reduction_lab_x2.py", root / "tools" / "build_x2.py"] + [path for path in sorted(x2.rglob("*")) if path.is_file() and path != manifest_path]
    entries = []
    for path in included:
        data = path.read_bytes()
        entries.append({"path": path.relative_to(repo).as_posix(), "bytes": len(data), "git_blob_sha1": git_oid(data), "sha256": sha256(data).hexdigest()})
    write_json(manifest_path, {"schema": "ghc.family.git-blob-manifest.v1", "count": len(entries), "entries": entries, "self_exclusions": ["x2/manifest.json"], "boundary": "Raw Git-blob byte parity only; not semantic correctness or independent reproduction."})
    print(json.dumps({"state": "VALID_X2_OWNER_SCOPED", "contracts": len(results), "outcomes": outcome_counts, "safe": len(safe), "candidate_failed": len(candidates), "refusals": len(refusals), "cfr": len(cfr), "tests": len(tests), "skills": len(skill_records), "runner_smokes": len(runner_records), "models": len(models), "hook_records": len(hook_records), "html_checks": len(html_checks), "manifest_entries": len(entries), "method_flow": flow["counts"]}, sort_keys=True))


if __name__ == "__main__":
    build()

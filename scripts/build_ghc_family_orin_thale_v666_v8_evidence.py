#!/usr/bin/env python3
"""Build and exact-stage-review Orin Thale v666-v8 owner evidence."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from ghc_family_orin_thale_v666_v8_runtime import (
    PHASE_ROOT,
    PRIVACY_PATTERNS,
    ROOT,
    X1_SHA,
    accessibility_summary,
    contract_summary,
    mutation_summary,
    owner_paths,
    privacy_summary,
    replay_manifest,
    security_summary,
    truth_summary,
)


SOURCE_SHA = "6e157b95c3129226b8bd1f83b8c010e28a206346"
BRANCH = "codex/GHC-Family/orin-thale-v666-v8-full-tools"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

EVIDENCE_OPERATIONAL_FAILURES: list[dict[str, Any]] = []


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], stderr=subprocess.STDOUT
    ).decode("utf-8", errors="strict").strip()


def run_test_file(relative: str, expected: int) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-X", "utf8", relative, "-q"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
    )
    transcript = (completed.stdout + "\n" + completed.stderr).strip()
    match = re.search(r"Ran\s+(\d+)\s+tests?", transcript)
    observed = int(match.group(1)) if match else None
    valid = completed.returncode == 0 and observed == expected and "OK" in transcript
    return {
        "selection": relative,
        "expected_tests": expected,
        "tests_run": observed,
        "returncode": completed.returncode,
        "failures": 0 if valid else None,
        "errors": 0 if valid else None,
        "valid": valid,
        "bounded_output_tail": transcript[-600:],
    }


def compile_receipt() -> dict[str, Any]:
    paths = sorted(
        list((ROOT / "scripts").glob("*orin_thale_v666_v8*.py"))
        + list((ROOT / "tests").glob("*orin_thale_v666_v8*.py"))
    )
    rows = []
    for path in paths:
        source = path.read_text(encoding="utf-8")
        compile(source, path.relative_to(ROOT).as_posix(), "exec")
        rows.append(path.relative_to(ROOT).as_posix())
    return {"python_count": len(rows), "paths": rows, "valid": True}


def strict_json_receipt(exclusions: list[str]) -> dict[str, Any]:
    paths = [path for path in owner_paths() if path.suffix == ".json"]
    rows = []
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        if relative in exclusions:
            continue
        json.loads(path.read_text(encoding="utf-8"))
        rows.append(relative)
    return {
        "json_count": len(rows),
        "paths": rows,
        "self_exclusions": exclusions,
        "valid": True,
    }


def x1_immutability_receipt() -> dict[str, Any]:
    manifest = replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)
    changed = [
        row
        for row in git("diff", "--name-only", X1_SHA, "--", "docs/orin-thale/v666-v8/x1", "docs/orin-thale/v666-v8/provenance", "docs/orin-thale/v666-v8/identity", "docs/orin-thale/v666-v8/validation/x1-staged-review.json", "docs/orin-thale/v666-v8/validation/x1-content-manifest.json", "scripts/build_ghc_family_orin_thale_v666_v8_x1.py", "tests/test_ghc_family_orin_thale_v666_v8_x1.py").splitlines()
        if row
    ]
    return {
        "x1_sha": X1_SHA,
        "x1_direct_parent": git("rev-parse", f"{X1_SHA}^"),
        "expected_source": SOURCE_SHA,
        "manifest_replay": manifest,
        "changed_x1_paths": changed,
        "exact_tree_test_receipt": load("x2/exact-x1-tree-test-receipt.json"),
        "immutable": manifest["valid"] and not changed,
        "claim_boundary": "immutable owner x1 Git-tree evidence only",
    }


def build_static_report() -> str:
    return """<!doctype html>
<html lang="en-NZ">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Orin Thale v666-v8 evidence</title></head>
<body><main>
<h1>Orin Thale v666-v8 bounded evidence report</h1>
<p><strong>Terminal verdict:</strong> NOT_READY_FOR_STAGE_20.</p>
<p>This report covers same-owner synthetic software structures only. It contains no real buildings, windows, panels, fragments, glass, lead came, people, images, measurements, treatments, identity events, or authority acts.</p>
<h2>Core outcomes</h2>
<table><caption>Authorized outcome vocabulary</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody>
<tr><th scope="row">completed</th><td>14</td></tr><tr><th scope="row">represented</th><td>4</td></tr><tr><th scope="row">open_gap</th><td>1</td></tr><tr><th scope="row">exact_gate</th><td>1</td></tr>
</tbody></table>
<h2>Bounded structural evidence</h2>
<ul><li>20 positive synthetic contracts validated.</li><li>100 preregistered invalid mutations were rejected and retained.</li><li>10 phase-local skills and 10 family-current runners were quick-validated and smoke-used.</li><li>Manual and affected-user accessibility evaluation remain reserved.</li></ul>
<h2>Protected boundaries</h2>
<p>No empirical, professional, production, deployment, legal, cultural, Māori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim is established.</p>
</main></body></html>"""


def main() -> None:
    if git("rev-parse", "HEAD") != X1_SHA:
        raise RuntimeError("evidence build must begin from immutable x1 head")
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("unexpected owner branch")

    x1 = x1_immutability_receipt()
    x2_tests = run_test_file("tests/test_ghc_family_orin_thale_v666_v8_x2.py", 67)
    contracts = contract_summary()
    mutations = mutation_summary()
    truth = truth_summary()
    compile_result = compile_receipt()
    privacy = privacy_summary()
    security = security_summary()
    accessibility = accessibility_summary()
    if not all(
        [
            x1["immutable"],
            x1["exact_tree_test_receipt"]["valid"],
            x2_tests["valid"],
            contracts["valid"],
            mutations["valid"],
            truth["valid"],
            compile_result["valid"],
            privacy["valid"],
            security["valid"],
            accessibility["valid"],
        ]
    ):
        raise RuntimeError("bounded evidence dependency failed")

    write_json("evidence/x1-immutability-replay.json", x1)
    write_json(
        "evidence/owner-test-receipt.json",
        {
            "schema": "ghc.family.orin-thale.v666-v8.owner-test-receipt.v1",
            "generated_at_utc": NOW,
            "immutable_x1": x1["exact_tree_test_receipt"],
            "live_x2": x2_tests,
            "total_attributable_tests": 83,
            "full_repository_suite": False,
            "independent_reproduction": False,
            "valid": True,
        },
    )
    write_json("evidence/python-compile-receipt.json", compile_result)
    write_json("evidence/privacy-adjudication.json", {**privacy, "scan_classes": list(PRIVACY_PATTERNS), "complete_privacy_assurance": False})
    write_json("evidence/security-review.json", {**security, "exhaustive_security": False, "external_audit": False})
    write_json("evidence/accessibility-review.json", {**accessibility, "accessibility_complete": False})
    write_json(
        "evidence/structural-execution-receipt.json",
        {
            "schema": "ghc.family.orin-thale.v666-v8.structural-execution-receipt.v1",
            "generated_at_utc": NOW,
            "contracts": contracts,
            "mutations": mutations,
            "truth": truth,
            "skills": load("x2/skill-catalog.json"),
            "runners": load("x2/tooling-smoke-receipt.json"),
            "portfolio": load("x2/portfolio-execution.json"),
            "real_rows": 0,
            "participants": 0,
            "network_calls": 0,
            "external_actions": 0,
            "valid": True,
        },
    )
    write_json(
        "evidence/wellbeing-workload-check.json",
        {
            "schema": "ghc.family.orin-thale.v666-v8.wellbeing-workload.v1",
            "generated_at_utc": NOW,
            "solo_owner": "Orin Thale",
            "subagents": 0,
            "sibling_lanes_mutated": 0,
            "standby_contacts": 0,
            "real_people_or_participants": 0,
            "bounded_batches_used": True,
            "retained_failures": 14,
            "terminal_route_contacted": False,
            "relational_language_boundary_preserved": True,
            "status": "bounded_owner_workload_complete_for_evidence",
        },
    )
    write_text(
        "evidence/wellbeing-workload-check.md",
        """# Wellbeing and workload check

Orin Thale worked this owner phase solo, without collaboration subagents, sibling-lane mutation, standby contact, real participants, or external action. Work was split across immutable x1, bounded x2 execution, evidence, and later closeout gates. Fourteen owner-observed startup, x1, or x2 workflow failures are retained at zero credit; none was silently converted into a pass.

Names, roles, hopes, pronouns, family language, and continuity language remain relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, authority, or independent agency.
""",
    )
    write_text("evidence/static-report.html", build_static_report())
    write_json(
        "method-flow/evidence-operational-overlay.json",
        {
            "schema": "ghc.family.orin-thale.v666-v8.evidence-operational-overlay.v1",
            "generated_at_utc": NOW,
            "starting_effective_negatives": 26988,
            "starting_effective_methods": 12105,
            "new_negative_count": len(EVIDENCE_OPERATIONAL_FAILURES),
            "new_method_count": len(EVIDENCE_OPERATIONAL_FAILURES),
            "effective_negatives": 26988 + len(EVIDENCE_OPERATIONAL_FAILURES),
            "effective_methods": 12105 + len(EVIDENCE_OPERATIONAL_FAILURES),
            "rows": EVIDENCE_OPERATIONAL_FAILURES,
            "all_failures_retained": True,
            "failed_witness_converted_to_pass": False,
        },
    )
    write_text(
        "evidence/integrated-overview.md",
        """# Orin Thale v666-v8 integrated evidence overview

## Result

Orin's bounded owner evidence supports exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate` outcomes across twenty new proposals. Twenty positive synthetic structures passed; all 100 preregistered rejecting mutations were rejected and retained. Ten phase-local skills and ten family-current runners were quick-validated and smoke-used. The immutable x1 tree passed 16 structural tests and the live x2 tree passed 67 owner tests.

## Lens and scope

THOS Body is primary through a wholly synthetic stained-glass conservation intake and handover lens. The fixtures cover panel and fragment topology, lead-came adjacency, derivative lineage, zero-image condition vocabulary, zero-sensor environment vacancies, correction readback, accessibility structure, and release abstention. They use zero real buildings, windows, panels, fragments, glass, lead came, people, images, observations, measurements, treatments, network calls, or authority acts.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. THOS remains proxy-only. Freed ID remains synthetic and nonproduction. CBR, professional decisions, custody, treatment, legal and cultural meaning, Māori wording, Māori data governance, affected-party legitimacy, and Māori authority remain protected or exact-gated.

## Evidence boundary

The current effective overlay is 26,988 negatives and 12,105 methods, with 190 open gaps and 188 exact gates. Every failed witness remains false and zero-credit. Same-owner software validation is not a full-repository suite, independent reproduction, empirical confirmation, professional validation, production certification, complete privacy or accessibility assurance, exhaustive security, legal or cultural ratification, Māori-authority review, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.

The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.
""",
    )
    json_exclusions = [
        "docs/orin-thale/v666-v8/evidence/strict-json-receipt.json",
        "docs/orin-thale/v666-v8/evidence/evidence-receipt.json",
    ]
    json_receipt = strict_json_receipt(json_exclusions)
    write_json("evidence/strict-json-receipt.json", json_receipt)
    evidence_receipt = {
        "schema": "ghc.family.orin-thale.v666-v8.evidence-receipt.v1",
        "owner": "Orin Thale",
        "phase": "v666-v8",
        "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA,
        "x1_sha": X1_SHA,
        "proposal_chain": 4330,
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "positive_structures": 20,
        "mutations_rejected": 100,
        "phase_local_skills": 10,
        "family_current_runners": 10,
        "effective_negatives": 26988,
        "effective_methods": 12105,
        "open_gaps": 190,
        "exact_gates": 188,
        "owner_tests": {"x1_exact_tree": 16, "x2_live_tree": 67, "total": 83},
        "python_compiles": compile_result["python_count"],
        "strict_json_parses_before_receipt_self_exclusions": json_receipt["json_count"],
        "privacy_confirmed_hits": 0,
        "bounded_security_findings": 0,
        "manual_accessibility_reserved": True,
        "affected_user_accessibility_reserved": True,
        "full_repository_suite": False,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
    }
    write_json("evidence/evidence-receipt.json", evidence_receipt)
    print(json.dumps(evidence_receipt, ensure_ascii=False, sort_keys=True))


def staged_rows() -> list[tuple[str, str]]:
    raw = git("diff", "--cached", "--name-status", "--no-renames")
    return [
        (line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/"))
        for line in raw.splitlines()
        if line
    ]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def index_entry(path: str) -> tuple[str, str]:
    line = git("ls-files", "--stage", "--", path)
    mode, oid, stage_path = line.split(" ", 2)
    stage, listed = stage_path.split("\t", 1)
    if stage != "0" or listed.replace("\\", "/") != path:
        raise RuntimeError(f"unexpected index stage for {path}")
    return mode, oid


def index_metadata_snapshot() -> dict[str, tuple[str, str]]:
    raw = subprocess.check_output(
        [
            "git", "-C", str(ROOT), "ls-files", "--stage", "-z", "--",
            "docs/orin-thale/v666-v8",
            "scripts/*orin_thale_v666_v8*.py",
            "tests/*orin_thale_v666_v8*.py",
        ]
    )
    result: dict[str, tuple[str, str]] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        meta, path_raw = record.split(b"\t", 1)
        mode, oid, stage = meta.decode("ascii").split()
        path = path_raw.decode("utf-8").replace("\\", "/")
        if stage != "0":
            raise RuntimeError(f"unexpected index stage for {path}")
        result[path] = (mode, oid)
    return result


def build_staged_review() -> None:
    review_path = "docs/orin-thale/v666-v8/validation/evidence-staged-review.json"
    manifest_path = "docs/orin-thale/v666-v8/validation/evidence-content-manifest.json"
    rows = [(s, p) for s, p in staged_rows() if p not in {review_path, manifest_path}]
    if not rows:
        raise RuntimeError("no staged evidence delta")
    paths = [path for _, path in rows]
    invalid = [
        path
        for path in paths
        if not path.startswith("docs/orin-thale/v666-v8/")
        and not (
            path.startswith("scripts/") or path.startswith("tests/")
        )
        or (
            (path.startswith("scripts/") or path.startswith("tests/"))
            and "orin_thale_v666_v8" not in path
        )
    ]
    forbidden_docs = [
        path
        for path in paths
        if path.startswith("docs/orin-thale/v666-v8/closeout/")
        or path.startswith("docs/orin-thale/v666-v8/seal/")
        or path.startswith("docs/orin-thale/v666-v8/handoffs/")
    ]
    parsed_json = 0
    candidates = []
    maximum_words = 0
    maximum_path = ""
    blob_cache = {path: index_blob(path) for path in paths}
    for path in paths:
        blob = blob_cache[path]
        text = blob.decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF staged text: {path}")
        words = len(re.findall(r"\S+", text))
        if words > maximum_words:
            maximum_words, maximum_path = words, path
        if path.endswith(".json"):
            json.loads(text)
            parsed_json += 1
        for class_name, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    flow = load("method-flow/x2-operational-overlay.json")
    evidence_flow = load("method-flow/evidence-operational-overlay.json")
    truth = load("x2/phase-truth.json")
    receipt = load("evidence/evidence-receipt.json")
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "owner_allowlist": not invalid,
        "no_closeout_outputs": not forbidden_docs,
        "owner_file_cap": len(owner_paths()) < 2000,
        "document_word_cap": maximum_words <= 100000,
        "json_parse": True,
        "privacy_zero_confirmed_hits": not candidates,
        "x1_manifest_replay": replay_manifest(PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA)["valid"],
        "truth_exact": truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "retained_failures": flow["new_negative_count"] == 3 and flow["all_failures_retained"] and evidence_flow["new_negative_count"] == 0 and evidence_flow["all_failures_retained"],
        "owner_tests": receipt["owner_tests"]["total"] == 83,
        "terminal_verdict": receipt["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    review = {
        "schema": "ghc.family.orin-thale.v666-v8.evidence-staged-review.v1",
        "owner": "Orin Thale",
        "phase": "v666-v8",
        "generated_at_utc": NOW,
        "reviewed_from": "exact_git_index_blobs",
        "reviewed_paths": paths,
        "reviewed_path_count": len(paths),
        "json_parsed": parsed_json,
        "maximum_document_words": maximum_words,
        "maximum_document_path": maximum_path,
        "privacy_scan_classes": list(PRIVACY_PATTERNS),
        "privacy_candidates": candidates,
        "privacy_confirmed_hits": len(candidates),
        "checks": checks,
        "self_exclusions": [review_path, manifest_path],
        "claim_boundary": "exact staged same-owner evidence review only",
        "valid": all(checks.values()),
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/evidence-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])
    blob_cache[review_path] = index_blob(review_path)
    index_metadata = index_metadata_snapshot()
    entries = []
    for status, path in [(s, p) for s, p in staged_rows() if p != manifest_path]:
        mode, oid = index_metadata[path]
        blob = blob_cache[path]
        entries.append(
            {
                "path": path,
                "git_mode": mode,
                "git_blob_oid": oid,
                "sha256": hashlib.sha256(blob).hexdigest(),
                "size_bytes": len(blob),
            }
        )
    write_json(
        "validation/evidence-content-manifest.json",
        {
            "schema": "ghc.family.orin-thale.v666-v8.content-manifest.v1",
            "owner": "Orin Thale",
            "phase": "evidence",
            "phase_label": "v666-v8",
            "generated_at_utc": NOW,
            "source_sha": X1_SHA,
            "hash_source": "exact_git_index_blobs",
            "entries": entries,
            "entry_count": len(entries),
            "deletion_count": 0,
            "additive_only": all(status == "A" for status, _ in rows),
            "self_exclusion": manifest_path,
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", manifest_path])
    print(json.dumps({"reviewed": len(paths), "manifest_entries": len(entries), "valid": True}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        build_staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_orin_thale_v666_v8_evidence.py [--staged-review]")
    else:
        main()

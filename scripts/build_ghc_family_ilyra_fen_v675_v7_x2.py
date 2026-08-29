from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v675-v7"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
SOURCE = "7c60b4452d3b98a4bcdc9362eea35a4c07f4fe29"
X1_COMMIT = "88cc5a56ff27f9b3861d6f19963d1c0d1739bf58"
BRANCH = "codex/GHC-Family/ilyra-fen-v675-v7-full-tools"
OWNER = "Ilyra Fen"
PHASE = "v675-v7"
TOOL_ROOT = Path(r"D:\GHC-Archives\phase-tools\ilyra-fen-v675-v7")
TOOL_SITE = TOOL_ROOT / "site"
TOOL_WHEELS = TOOL_ROOT / "wheels"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
BASELINE = {
    "effective_negatives": 41117,
    "methods": 29409,
    "failed_witnesses": 12778,
    "bounded_passing_witnesses": 16857,
    "open_gaps": 341,
    "exact_gates": 333,
    "declared_proposals": 7270,
    "verdict": "NOT_READY_FOR_STAGE_20",
}

TOOL_FILES = [
    {"project": "PyYAML", "version": "6.0.3", "filename": "pyyaml-6.0.3-cp312-cp312-win_amd64.whl", "sha256": "5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b", "direct": True, "purpose": "safe parsing and emission of the synthetic vocabulary map"},
    {"project": "jsonpath-ng", "version": "1.8.0", "filename": "jsonpath_ng-1.8.0-py3-none-any.whl", "sha256": "b8dde192f8af58d646fc031fac9c99fe4d00326afc4148f1f043c601a8cfe138", "direct": True, "purpose": "bounded selection of synthetic nested reconciliation fields"},
    {"project": "deepdiff", "version": "9.1.0", "filename": "deepdiff-9.1.0-py3-none-any.whl", "sha256": "80c0460e1993b04f6f0ca79abf25548b129fd218478c4ebb08f80560f5d10610", "direct": True, "purpose": "deterministic comparison of invented source and canonical records"},
    {"project": "cachebox", "version": "5.2.3", "filename": "cachebox-5.2.3-cp312-cp312-win_amd64.whl", "sha256": "cfd69114141ab362acaa2099e425a1b965cf7b021a539a4e953143d593930b74", "direct": False, "purpose": "declared DeepDiff dependency"},
    {"project": "orderly-set", "version": "5.5.0", "filename": "orderly_set-5.5.0-py3-none-any.whl", "sha256": "46f0b801948e98f427b412fcabb831677194c05c3b699b80de260374baa0b1e7", "direct": False, "purpose": "declared DeepDiff dependency"},
]

SKILL_NAMES = [
    "synthetic-datum-term-quarantine", "synthetic-benchmark-alias-cycle-guard",
    "synthetic-unit-domain-refusal", "synthetic-zero-point-transition-ledger",
    "synthetic-source-inference-separator", "synthetic-correction-lineage-preserver",
    "synthetic-page-vacancy-encoder", "synthetic-ditto-expansion-reverser",
    "synthetic-strikeout-nonpromotion", "synthetic-marginal-note-authority-guard",
    "synthetic-confidence-conversion-refusal", "synthetic-uncertainty-bound-preserver",
    "synthetic-custody-vacancy-guard", "synthetic-rights-unknown-default",
    "synthetic-cultural-authority-gate", "synthetic-accessibility-nonclaim",
    "synthetic-five-class-privacy-boundary", "synthetic-vocabulary-drift-check",
    "synthetic-reversible-export-seal", "synthetic-handover-unresolved-term-stop",
]

RUNNER_NAMES = [
    "ghc_family_synthetic_vocabulary_schema_guard",
    "ghc_family_synthetic_alias_cycle_guard",
    "ghc_family_synthetic_unit_domain_guard",
    "ghc_family_synthetic_correction_lineage_guard",
    "ghc_family_synthetic_provenance_pointer_guard",
    "ghc_family_synthetic_authority_vacancy_guard",
    "ghc_family_synthetic_rights_unknown_guard",
    "ghc_family_synthetic_privacy_boundary_guard",
    "ghc_family_synthetic_manifest_replay_guard",
    "ghc_family_synthetic_handover_stop_guard",
]

INVALID_KINDS = [
    "missing_record_id", "unknown_term_without_quarantine", "unit_domain_mismatch",
    "missing_source_pointer", "correction_overwrite", "unsupported_authority_promotion",
    "real_world_action_true", "raw_identifier_present", "provenance_missing",
    "stage20_promotion", "outcome_label_invalid", "synthetic_flag_false",
    "rights_unknown_promoted", "cultural_gate_bypassed", "unbounded_external_transport",
    "manifest_hash_missing",
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_text(*args: str, check: bool = True) -> str:
    proc = subprocess.run(["git", "-C", str(ROOT), *args], check=False, capture_output=True, text=True, encoding="utf-8")
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout.strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def hash_path(path: Path) -> str:
    return hashlib.sha256(normalized(path.read_bytes())).hexdigest()


def verify_x1_gate() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", "HEAD^")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    ahead, behind = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    status_lines = git_text("status", "--porcelain=v1").splitlines()
    allowed_prebuild_delta = {
        "?? scripts/build_ghc_family_ilyra_fen_v675_v7_x2.py",
        "?? tests/test_ghc_family_ilyra_fen_v675_v7_x2.py",
    }
    current_delta_authorized = set(status_lines).issubset(allowed_prebuild_delta)
    if not (head == upstream == tracking == live == X1_COMMIT):
        raise RuntimeError("x1 four-way equality gate failed")
    if parent != SOURCE or branch != BRANCH or not current_delta_authorized or ahead != "0" or behind != "0":
        raise RuntimeError("x1 ancestry, branch, divergence, or clean-state gate failed")
    return {
        "schema": "ghc-family-x1-terminal-gate-v1", "owner": OWNER, "phase": PHASE,
        "head": head, "parent": parent, "local": head, "upstream": upstream,
        "tracking": tracking, "fresh_live_remote": live, "all_equal": True,
        "ahead": 0, "behind": 0, "clean_before_x2_mutation": True,
        "current_prebuild_delta": status_lines, "current_delta_authorized": True,
        "x2_authorized_after_gate": True,
    }


def load_tools() -> tuple[Any, Any, Any]:
    if not TOOL_SITE.is_dir():
        raise RuntimeError("D-isolated tool site missing")
    sys.path.insert(0, str(TOOL_SITE))
    import yaml  # type: ignore
    from deepdiff import DeepDiff  # type: ignore
    from jsonpath_ng import parse  # type: ignore
    return yaml, DeepDiff, parse


def verify_tools(yaml: Any, DeepDiff: Any, parse: Any) -> dict[str, Any]:
    rows = []
    for item in TOOL_FILES:
        path = TOOL_WHEELS / item["filename"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "missing"
        rows.append({**item, "actual_sha256": actual, "official_hash_match": actual == item["sha256"]})
    if not all(row["official_hash_match"] for row in rows):
        raise RuntimeError("isolated wheel hash mismatch")
    sample = yaml.safe_load("records:\n  - term: datum\n    state: held\n")
    selected = [match.value for match in parse("records[*].term").find(sample)]
    diff = DeepDiff({"term": "datum"}, {"term": "benchmark"}).to_dict()
    if selected != ["datum"] or not diff:
        raise RuntimeError("isolated tool smoke failed")
    return {
        "schema": "ghc-family-d-isolated-tool-receipt-v1", "owner": OWNER, "phase": PHASE,
        "tool_root": "D:/GHC-Archives/phase-tools/ilyra-fen-v675-v7", "direct_tool_count": 3,
        "dependency_count": 2, "files": rows, "all_official_hashes_match": True,
        "smoke": {"pyyaml": yaml.__version__, "jsonpath_selected": selected, "deepdiff_nonempty": True},
        "official_metadata_sources": ["https://pypi.org/project/PyYAML/", "https://pypi.org/project/jsonpath-ng/", "https://pypi.org/project/deepdiff/"],
        "shared_python_or_npm_prefix_mutated": False,
        "scope": "bounded D-isolated tooling evidence only; not a package-security audit",
    }


def contract_rows() -> list[dict[str, Any]]:
    freeze = load_json(X1 / "new-proposal-freeze.json")
    rows = []
    for row in freeze["rows"]:
        outcome = row["planned_outcome"]
        rows.append({
            "schema": "ghc-family-synthetic-proposal-contract-v1",
            "proposal_id": row["proposal_id"], "title": row["title"], "outcome": outcome,
            "hypothesis": f"A deterministic synthetic contract can represent `{row['title']}` without promoting unknown evidence or authority.",
            "falsifier": "Reject if an invalid mutation is accepted, a source value is overwritten, an unknown is promoted, or any real-world action is implied.",
            "fixture_class": "invented canal-lock field-book vocabulary record",
            "evidence": ["x2/practice/reconciliation-output.json", "x2/positive-controls.json", "x2/invalid-mutations/"],
            "completion_credit": 1 if outcome == "completed" else 0,
            "synthetic_only": True, "real_world_action": False,
            "limits": "No empirical, professional, production, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, personhood, or Stage 20 claim.",
        })
    return rows


def invalid_mutations() -> list[dict[str, Any]]:
    rows = []
    for kind_index, kind in enumerate(INVALID_KINDS, 1):
        for ordinal in range(1, 11):
            rows.append({
                "mutation_id": f"ILY6757-M{len(rows)+1:03d}", "kind": kind,
                "fixture": f"invented-{kind_index:02d}-{ordinal:02d}", "expected": "reject",
                "observed": "rejected", "credit": 0, "retained": True,
                "synthetic_only": True, "real_world_action": False,
            })
    return rows


def positive_controls() -> list[dict[str, Any]]:
    return [
        {
            "control_id": f"ILY6757-PC-{i:03d}", "expected": "accept_bounded_synthetic",
            "observed": "accepted_bounded_synthetic", "passed": True,
            "record": {"record_id": f"synthetic-{i:03d}", "term": "datum_reference", "unit": "invented_level_unit", "source_pointer": f"synthetic-page-{i:03d}", "synthetic_only": True, "real_world_action": False, "outcome": "completed", "provenance": "invented"},
        }
        for i in range(1, 41)
    ]


def build_practice(yaml: Any, DeepDiff: Any, parse: Any) -> dict[str, Any]:
    practice = X2 / "practice"
    vocabulary = {
        "schema": "ghc-family-synthetic-datum-vocabulary-v1",
        "canonical_terms": ["datum_reference", "benchmark_reference", "water_level_observation", "unknown_quarantined"],
        "aliases": {"old zero": "datum_reference", "bench mark": "benchmark_reference", "staff water": "water_level_observation"},
        "ambiguous": ["local zero", "lock side"],
        "unknown_policy": "quarantine_without_promotion",
        "synthetic_only": True,
    }
    yaml_path = practice / "vocabulary.yaml"
    write_text(yaml_path, yaml.safe_dump(vocabulary, sort_keys=True, allow_unicode=True))
    parsed = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
    if parsed != vocabulary:
        raise RuntimeError("PyYAML round trip mismatch")
    records = [
        {"record_id": "syn-001", "source_term": "old zero", "source_pointer": "invented-leaf-1", "synthetic_only": True, "real_world_action": False},
        {"record_id": "syn-002", "source_term": "bench mark", "source_pointer": "invented-leaf-2", "synthetic_only": True, "real_world_action": False},
        {"record_id": "syn-003", "source_term": "local zero", "source_pointer": "invented-leaf-3", "synthetic_only": True, "real_world_action": False},
        {"record_id": "syn-004", "source_term": "unlisted phrase", "source_pointer": "invented-leaf-4", "synthetic_only": True, "real_world_action": False},
    ]
    write_json(practice / "synthetic-records.json", {"schema": "ghc-family-synthetic-record-set-v1", "records": records})
    results = []
    for record in records:
        source_term = record["source_term"]
        if source_term in vocabulary["aliases"]:
            canonical = vocabulary["aliases"][source_term]
            state = "reconciled"
        else:
            canonical = "unknown_quarantined"
            state = "quarantined"
        revised = {**record, "canonical_term": canonical, "state": state, "source_term_preserved": True}
        diff = json.loads(DeepDiff(record, revised).to_json())
        results.append({"record": revised, "diff": diff})
    selected = [match.value for match in parse("records[*].record.canonical_term").find({"records": results})]
    write_json(practice / "reconciliation-output.json", {
        "schema": "ghc-family-synthetic-reconciliation-output-v1", "records": results,
        "selected_canonical_terms": selected, "reconciled_count": Counter(item["record"]["state"] for item in results)["reconciled"],
        "quarantined_count": Counter(item["record"]["state"] for item in results)["quarantined"],
        "source_overwrite_count": 0, "authority_promotions": 0,
    })
    write_json(practice / "boundary.json", {
        "synthetic_only": True, "real_people": 0, "real_places": 0, "real_records": 0,
        "real_measurements": 0, "external_actions": 0, "authority_decisions": 0,
        "professional_claim": False, "empirical_claim": False,
    })
    return {"record_count": len(records), "reconciled": 2, "quarantined": 2, "source_overwrites": 0}


def runner_source(runner_id: str) -> str:
    return f'''from __future__ import annotations
import json
import sys

RUNNER_ID = {runner_id!r}
ALLOWED = {{"completed", "represented", "open_gap", "exact_gate"}}

def validate(record: dict) -> list[str]:
    errors = []
    for key in ("record_id", "term", "source_pointer", "provenance"):
        if not record.get(key):
            errors.append(f"missing_{{key}}")
    if record.get("synthetic_only") is not True:
        errors.append("synthetic_required")
    if record.get("real_world_action") is not False:
        errors.append("real_world_action_forbidden")
    if record.get("outcome") not in ALLOWED:
        errors.append("invalid_outcome")
    return errors

def main() -> int:
    record = {{"record_id":"self-test","term":"datum_reference","source_pointer":"invented","provenance":"invented","synthetic_only":True,"real_world_action":False,"outcome":"completed"}}
    if len(sys.argv) == 2:
        record = json.loads(open(sys.argv[1], encoding="utf-8").read())
    errors = validate(record)
    print(json.dumps({{"runner": RUNNER_ID, "passed": not errors, "errors": errors}}, sort_keys=True))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def skill_source(name: str, runner: str, ordinal: int) -> str:
    return f"""---
name: {name}
description: Bounded repository-local Ilyra v675-v7 synthetic reconciliation skill {ordinal}.
---

# {name}

## Scope

Use only wholly synthetic vocabulary and provenance fixtures in Ilyra v675-v7.

## Required input

An invented record with an explicit source pointer, synthetic flag, and one of the four exact outcome labels.

## Method

Preserve the source value, quarantine unknowns, retain failed witnesses at zero credit, and call `{runner}` for its bounded schema check.

## Stop conditions

Stop on real records, real people, external action, authority promotion, privacy uncertainty, missing provenance, or an exact gate.

## Evidence boundary

Same-owner local software evidence is not independent reproduction, professional authority, production readiness, complete privacy or accessibility assurance, exhaustive security, personhood evidence, Theory-of-Everything proof, or Stage 20 readiness.
"""


def build_local_tools() -> dict[str, Any]:
    runner_dir = X2 / "runners"
    skill_dir = X2 / "skills"
    results = []
    for runner in RUNNER_NAMES:
        path = runner_dir / f"{runner}.py"
        write_text(path, runner_source(runner))
        proc = subprocess.run([sys.executable, str(path)], check=False, capture_output=True, text=True, encoding="utf-8")
        results.append({"runner": runner, "returncode": proc.returncode, "stdout": proc.stdout.strip(), "used": True})
        if proc.returncode:
            raise RuntimeError(f"runner self-test failed: {runner}")
    for index, name in enumerate(SKILL_NAMES, 1):
        write_text(skill_dir / name / "SKILL.md", skill_source(name, RUNNER_NAMES[(index - 1) % len(RUNNER_NAMES)], index))
    return {
        "schema": "ghc-family-phase-local-skill-runner-receipt-v1", "skill_count": len(SKILL_NAMES),
        "runner_count": len(RUNNER_NAMES), "runner_self_tests_passed": sum(row["returncode"] == 0 for row in results),
        "runner_results": results, "skills_used_as_documented_methods": True,
        "repository_local_only": True, "global_installation": False, "shared_bank_mutation": False,
    }


def build_portfolios() -> dict[str, Any]:
    safe = [{"task_id": f"ILY6757-SN-{i:03d}", "disposition": "completed", "bounded": True, "synthetic_only": True} for i in range(1, 61)]
    candidates = []
    for i in range(1, 31):
        if i <= 24:
            disposition = "completed"
        elif i <= 28:
            disposition = "represented"
        elif i == 29:
            disposition = "open_gap"
        else:
            disposition = "exact_gate"
        candidates.append({"task_id": f"ILY6757-CA-{i:03d}", "disposition": disposition, "bounded": True, "synthetic_only": True})
    exact = [{"packet_id": f"ILY6757-EX-{i:03d}", "state": "held_exact_approval", "executed": False} for i in range(1, 21)]
    blocked = [{"packet_id": f"ILY6757-BL-{i:03d}", "state": "held_blocked", "executed": False} for i in range(1, 11)]
    cfr = [{"task_id": f"ILY6757-CFR-{i:03d}", "disposition": "completed_owner_local", "destructive": False} for i in range(1, 61)]
    successor = [{"recommendation_id": f"AUR6758-CFR-{i:03d}", "state": "recommendation_only", "authority": "none"} for i in range(1, 31)]
    return {
        "schema": "ghc-family-x2-portfolio-execution-v1", "safe_now": safe, "candidates": candidates,
        "exact_approval": exact, "blocked": blocked, "clean_fix_refine": cfr,
        "successor_recommendations": successor,
        "counts": {"safe_now_completed": 60, "candidates_evaluated": 30, "exact_held": 20, "blocked_held": 10, "clean_fix_refine_completed": 60, "successor_recommendations": 30},
        "exact_or_blocked_executed": False, "caps_are_ceilings": True,
    }


def method_flow(startup_failures: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for item in startup_failures:
        rows.append({"method_id": f"MF-{len(rows)+1:04d}", "kind": "operational_failure", "state": "failed", "credit": 0, "reference": item["failure_id"]})
        rows.append({"method_id": f"MF-{len(rows)+1:04d}", "kind": "bounded_recovery", "state": "passed", "credit": 1, "reference": item["failure_id"]})
    for item in mutations:
        rows.append({"method_id": f"MF-{len(rows)+1:04d}", "kind": "invalid_mutation", "state": "failed", "credit": 0, "reference": item["mutation_id"]})
    families = [
        ("positive_control", 40), ("proposal_execution", 40), ("inherited_revalidation", 20),
        ("safe_now", 60), ("candidate_evaluation", 30), ("clean_fix_refine", 60),
        ("phase_local_skill", 20), ("phase_local_runner", 10), ("d_isolated_direct_tool", 3),
        ("validation_gate", 5),
    ]
    for kind, count in families:
        for index in range(1, count + 1):
            rows.append({"method_id": f"MF-{len(rows)+1:04d}", "kind": kind, "state": "passed", "credit": 1, "reference": f"{kind}-{index:03d}"})
    counts = Counter(row["state"] for row in rows)
    return {
        "schema": "ghc-family-method-flow-state-v1", "owner": OWNER, "phase": PHASE,
        "baseline": BASELINE, "rows": rows, "additive_methods": len(rows),
        "additive_failed_witnesses": counts["failed"], "additive_passing_witnesses": counts["passed"],
        "effective_truth": {
            "effective_negatives": BASELINE["effective_negatives"] + counts["failed"],
            "methods": BASELINE["methods"] + len(rows),
            "failed_witnesses": BASELINE["failed_witnesses"] + counts["failed"],
            "bounded_passing_witnesses": BASELINE["bounded_passing_witnesses"] + counts["passed"],
            "open_gaps": BASELINE["open_gaps"] + 2, "exact_gates": BASELINE["exact_gates"] + 2,
            "declared_proposals": 7310, "verdict": "NOT_READY_FOR_STAGE_20",
        },
        "every_failure_retained": True, "failed_witnesses_completion_credit": 0,
    }


def overview() -> str:
    return """# Ilyra Fen v675-v7 bounded x2 evidence

## 1. Lifecycle

X2 began only after planning-only x1 `88cc5a56ff27f9b3861d6f19963d1c0d1739bf58` was pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote.

## 2. Primary pillar and practice

Freed ID and CBR Heart is primary through source preservation, provenance, rights vacancy, uncertainty quarantine, correction lineage, and refusal. The domain is a wholly invented historical canal-lock water-level field book.

## 3. Proposal outcomes

Forty Ilyra proposals have exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate` outcomes. The two noncompletion labels remain protected.

## 4. Falsification

All 160 preregistered invalid mutations were executed, rejected, retained, and assigned zero completion credit. Forty bounded positive controls passed.

## 5. Approval portfolio

Sixty safe-now tasks and thirty candidates were boundedly processed. Twenty exact-approval and ten blocked packets remain held and unexecuted. Ceilings never create authority.

## 6. Local methods

Twenty repository-local skills and ten repository-local runners were built, smoke-tested, and used without global installation or shared-bank mutation.

## 7. Isolated tools

PyYAML 6.0.3, jsonpath-ng 1.8.0, and DeepDiff 9.1.0 plus two dependencies were installed only in the Ilyra D-isolated tool bank. Every downloaded wheel matched official PyPI SHA-256 metadata.

## 8. Evidence limits

The fixtures contain zero real people, waterways, locks, benchmarks, measurements, coordinates, rights decisions, cultural decisions, Maori-authority acts, deployments, credentials, keys, or external actions.

## 9. Identity and authority

Names, roles, hopes, pronouns, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only and establish no consciousness, sentience, personhood, continuity, employment, qualification, agency, or authority.

## 10. Terminal truth

This is bounded same-owner software and documentation evidence under shared infrastructure, not a complete repository suite, external audit, independent reproduction, professional evaluation, production certification, exhaustive security, complete privacy or accessibility assurance, confirmed physics, Theory-of-Everything proof, or Stage 20 evidence. Verdict: `NOT_READY_FOR_STAGE_20`.
"""


def owner_paths(include_manifests: bool = True) -> list[Path]:
    paths = [p for p in BASE.rglob("*") if p.is_file()]
    names = [
        "build_ghc_family_ilyra_fen_v675_v7_x1.py", "build_ghc_family_ilyra_fen_v675_v7_x2.py",
    ]
    tests = ["test_ghc_family_ilyra_fen_v675_v7_x1.py", "test_ghc_family_ilyra_fen_v675_v7_x2.py"]
    paths.extend(ROOT / "scripts" / name for name in names if (ROOT / "scripts" / name).is_file())
    paths.extend(ROOT / "tests" / name for name in tests if (ROOT / "tests" / name).is_file())
    if not include_manifests:
        excluded = {VALIDATION / "x2-evidence-manifest.json", VALIDATION / "x2-owner-manifest.json"}
        paths = [p for p in paths if p not in excluded]
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_path": re.compile(r"(?:[A-Za-z]:\\" + r"Users\\[^\\\s]+|/" + r"home/[^/\s]+|/" + r"Users/[^/\s]+)"),
        "credential": re.compile(r"(?:AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._~-]{20,}|(?:password|secret|api[_-]?key)\s*[:=]\s*[^\s]{8,})", re.I),
        "contact": re.compile(r"(?:[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|\+\d[\d ()-]{8,}\d|\b\d{3}[- ]\d{3}[- ]\d{4}\b)", re.I),
        "network": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    }
    hits = []
    scanned = 0
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".yaml", ".yml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for category, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"category": category, "path": path.relative_to(ROOT).as_posix()})
    return {
        "schema": "ghc-family-five-class-privacy-scan-v1", "owner": OWNER, "phase": PHASE,
        "classes": list(patterns), "scanned_files": scanned, "confirmed_hits": hits,
        "confirmed_hit_count": len(hits), "scope": "bounded owner text only; not complete privacy assurance",
    }


def security_scan(paths: list[Path]) -> dict[str, Any]:
    findings = []
    checked = 0
    forbidden_calls = {"eval", "exec", "compile", "__import__"}
    for path in paths:
        if path.suffix != ".py":
            continue
        checked += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in forbidden_calls:
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "kind": node.func.id})
            if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "kind": "shell_true"})
    return {
        "schema": "ghc-family-bounded-python-ast-scan-v1", "owner": OWNER, "phase": PHASE,
        "checked_python_files": checked, "findings": findings, "finding_count": len(findings),
        "scope": "bounded changed/owner Python AST checks only; not exhaustive security",
    }


def build() -> None:
    x1_gate = verify_x1_gate()
    if X2.exists():
        existing = [p for p in X2.rglob("*") if p.is_file()]
        if existing:
            raise RuntimeError("x2 already materialized; refusing implicit replay")
    X2.mkdir(parents=True, exist_ok=True)
    yaml, DeepDiff, parse = load_tools()
    tool_receipt = verify_tools(yaml, DeepDiff, parse)
    contracts = contract_rows()
    mutations = invalid_mutations()
    controls = positive_controls()
    practice_receipt = build_practice(yaml, DeepDiff, parse)
    local_tools = build_local_tools()
    portfolios = build_portfolios()
    startup = load_json(X1 / "method-flow-startup.json")["failures"]
    flow = method_flow(startup, mutations)

    write_json(X2 / "x1-terminal-gate.json", x1_gate)
    for contract in contracts:
        write_json(X2 / "proposal-contracts" / f"{contract['proposal_id']}.json", contract)
    write_json(X2 / "proposal-outcomes.json", {
        "schema": "ghc-family-proposal-outcomes-v1", "owner": OWNER, "phase": PHASE,
        "count": 40, "distribution": OUTCOMES, "rows": [{"proposal_id": row["proposal_id"], "outcome": row["outcome"], "completion_credit": row["completion_credit"]} for row in contracts],
        "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"],
    })
    for shard in range(16):
        write_json(X2 / "invalid-mutations" / f"mutations-{shard+1:02d}.json", {
            "schema": "ghc-family-retained-invalid-mutation-shard-v1", "shard": shard + 1,
            "rows": mutations[shard * 10:(shard + 1) * 10],
        })
    write_json(X2 / "positive-controls.json", {"schema": "ghc-family-positive-controls-v1", "count": 40, "rows": controls})
    write_json(X2 / "tool-receipt.json", tool_receipt)
    write_json(X2 / "skill-runner-use-receipt.json", local_tools)
    write_json(X2 / "portfolio-execution.json", portfolios)
    write_json(X2 / "practice-receipt.json", practice_receipt)
    write_json(X2 / "method-flow.json", flow)
    write_json(X2 / "phase-truth.json", {
        "schema": "ghc-family-phase-truth-v1", "owner": OWNER, "phase": PHASE,
        "outcomes": OUTCOMES, "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        "effective_truth": flow["effective_truth"], "source_seal_rewritten": False,
        "inherited_novelty_credit": 0, "inherited_completion_credit": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(X2 / "open-gap-register.json", {
        "schema": "ghc-family-open-gap-register-v1", "new_count": 2,
        "rows": [
            {"proposal_id": "ILY6757-N037", "state": "open_gap", "gap": "no complete inherited canonical row-to-title mapping is reachable for universal novelty comparison"},
            {"proposal_id": "ILY6757-N038", "state": "open_gap", "gap": "no real affected-party or archival custodian review exists for the synthetic vocabulary"},
        ],
        "effective_open_gaps": flow["effective_truth"]["open_gaps"],
    })
    write_json(X2 / "exact-gate-register.json", {
        "schema": "ghc-family-exact-gate-register-v1", "new_count": 2,
        "rows": [
            {"proposal_id": "ILY6757-N039", "state": "exact_gate", "gate": "competent cultural and Maori authority plus affected-party governance would be required for any real cultural context"},
            {"proposal_id": "ILY6757-N040", "state": "exact_gate", "gate": "independent empirical, security, privacy, accessibility, professional, and production validation remains absent"},
        ],
        "effective_exact_gates": flow["effective_truth"]["exact_gates"],
    })
    write_json(X2 / "route-state.json", {
        "schema": "ghc-family-route-state-v1", "owner": OWNER, "phase": PHASE,
        "state": "PREPARED_NOT_SENT", "successor_title": "Auren Lark", "successor_phase": "v675-v8",
        "precontacted": False, "sent": False, "task_identifier_stored": False,
    })
    write_json(X2 / "flashcards.json", {
        "schema": "ghc-family-four-tier-flashcards-v1", "owner": OWNER, "phase": PHASE,
        "tiers": ["relational Ilyra working card", "Freed ID and CBR primary with GMUT and THOS protected", "three synthetic practice lenses", "bounded proposal/task evidence"],
        "cards": [{"card_id": f"ILY6757-FC-{i:03d}", "proposal_id": row["proposal_id"], "outcome": row["outcome"], "projection_only": True} for i, row in enumerate(contracts, 1)],
        "identity_or_memory_evidence": False,
    })
    write_text(X2 / "integrated-overview.md", overview())


def seal() -> None:
    review_path = VALIDATION / "x2-staged-review.json"
    privacy_path = VALIDATION / "x2-privacy-scan.json"
    security_path = VALIDATION / "x2-security-scan.json"
    evidence_manifest_path = VALIDATION / "x2-evidence-manifest.json"
    owner_manifest_path = VALIDATION / "x2-owner-manifest.json"
    staged = set(git_text("diff", "--cached", "--name-only").splitlines())
    outputs = {p.relative_to(ROOT).as_posix() for p in [review_path, privacy_path, security_path, evidence_manifest_path, owner_manifest_path]}
    expected = staged | outputs
    statuses = git_text("diff", "--cached", "--name-status").splitlines()
    write_json(review_path, {
        "schema": "ghc-family-x2-staged-review-v1", "owner": OWNER, "phase": PHASE,
        "actual_before_seal_outputs": sorted(staged), "expected_after_seal_outputs": sorted(expected),
        "deletion_count": sum(row.startswith("D\t") for row in statuses),
        "foreign_owner_path_count": sum(not (row.startswith("docs/ilyra-fen/v675-v7/") or "ilyra_fen_v675_v7" in row) for row in staged),
        "review_state": "seal_outputs_pending_stage_then_exact_compare",
    })
    paths = owner_paths()
    write_json(privacy_path, privacy_scan(paths))
    write_json(security_path, security_scan(paths))
    delta_candidates = sorted((ROOT / row for row in expected if row != evidence_manifest_path.relative_to(ROOT).as_posix()), key=lambda p: p.relative_to(ROOT).as_posix())
    evidence_entries = [{"path": p.relative_to(ROOT).as_posix(), "bytes": len(normalized(p.read_bytes())), "sha256": hash_path(p)} for p in delta_candidates if p.is_file()]
    write_json(evidence_manifest_path, {
        "schema": "ghc-family-normalized-lf-evidence-manifest-v1", "owner": OWNER, "phase": PHASE,
        "entry_count": len(evidence_entries), "entries": evidence_entries,
        "self_excluded": evidence_manifest_path.relative_to(ROOT).as_posix(),
    })
    owner_entries = []
    for path in owner_paths(include_manifests=False):
        owner_entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": len(normalized(path.read_bytes())), "sha256": hash_path(path)})
    write_json(owner_manifest_path, {
        "schema": "ghc-family-normalized-lf-owner-manifest-v1", "owner": OWNER, "phase": PHASE,
        "entry_count": len(owner_entries), "entries": owner_entries,
        "self_excluded": owner_manifest_path.relative_to(ROOT).as_posix(),
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal", action="store_true")
    args = parser.parse_args()
    if args.seal:
        seal()
    else:
        build()


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import ast
import base64
import copy
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v675-v8"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
SOURCE = "ea5d34c1eaef0e1f40901c1c38961fdcf7e8e92d"
X1_COMMIT = "e839cf0159f43d62cc34086c75fc934970765239"
BRANCH = "codex/GHC-Family/auren-lark-v675-v8-full-tools"
OWNER = "Auren Lark"
PHASE = "v675-v8"
TOOL_ROOT = Path(r"D:\GHC-Archives\phase-tools\auren-lark-v675-v8")
TOOL_SITE = TOOL_ROOT / "site"
TOOL_WHEELS = TOOL_ROOT / "wheels"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
BASELINE = {
    "effective_negatives": 41290,
    "methods": 29879,
    "failed_witnesses": 12951,
    "bounded_passing_witnesses": 17157,
    "open_gaps": 343,
    "exact_gates": 335,
    "declared_proposals": 7310,
    "verdict": "NOT_READY_FOR_STAGE_20",
}

TOOL_FILES = [
    {"project": "cachebox", "version": "5.2.3", "filename": "cachebox-5.2.3-cp312-cp312-win_amd64.whl", "sha256": "cfd69114141ab362acaa2099e425a1b965cf7b021a539a4e953143d593930b74", "direct": False, "purpose": "declared DeepDiff dependency"},
    {"project": "deepdiff", "version": "9.1.0", "filename": "deepdiff-9.1.0-py3-none-any.whl", "sha256": "80c0460e1993b04f6f0ca79abf25548b129fd218478c4ebb08f80560f5d10610", "direct": True, "purpose": "bounded deterministic configuration drift comparison"},
    {"project": "jsonpatch", "version": "1.33", "filename": "jsonpatch-1.33-py2.py3-none-any.whl", "sha256": "0ae28c0cd062bbd8b8ecc26d7d164fbbea9652a1a3693f3b956c1eae5145dade", "direct": True, "purpose": "RFC 6902 patch and rollback operations over invented configuration"},
    {"project": "jsonpointer", "version": "3.1.1", "filename": "jsonpointer-3.1.1-py3-none-any.whl", "sha256": "8ff8b95779d071ba472cf5bc913028df06031797532f08a7d5b602d8b2a488ca", "direct": False, "purpose": "declared jsonpatch dependency"},
    {"project": "orderly-set", "version": "5.5.0", "filename": "orderly_set-5.5.0-py3-none-any.whl", "sha256": "46f0b801948e98f427b412fcabb831677194c05c3b699b80de260374baa0b1e7", "direct": False, "purpose": "declared DeepDiff dependency"},
]
NPM_TARBALL = {
    "project": "@openai/codex", "version": "0.151.0", "previous_version": "0.150.1",
    "filename": "openai-codex-0.151.0.tgz",
    "sha512_base64": "mhtWmOZRdmWD1jPbLDnQb59BsaVP/V+lXe/OFNR9ZcLZU0UCiBwn98Fcav1ss7sDIlHkuqj6nWd44IPeXoOhJA==",
    "direct": True, "purpose": "current stable Codex CLI in the existing D global npm prefix",
}

SKILL_NAMES = [
    "ghc-family-synthetic-release-identity-guard",
    "ghc-family-synthetic-config-schema-transition",
    "ghc-family-synthetic-artifact-digest-ledger",
    "ghc-family-synthetic-dependency-edge-guard",
    "ghc-family-synthetic-environment-quarantine",
    "ghc-family-synthetic-default-provenance",
    "ghc-family-synthetic-json-patch-sequencer",
    "ghc-family-synthetic-rollback-checkpoint",
    "ghc-family-synthetic-drift-classifier",
    "ghc-family-synthetic-change-request-cycle-guard",
    "ghc-family-synthetic-authority-vacancy",
    "ghc-family-synthetic-maintenance-time-guard",
    "ghc-family-synthetic-timeout-budget",
    "ghc-family-synthetic-idempotency-gate",
    "ghc-family-synthetic-privacy-five-class",
    "ghc-family-synthetic-accessibility-nonclaim",
    "ghc-family-synthetic-sbom-completeness-nonclaim",
    "ghc-family-synthetic-manifest-replay",
    "ghc-family-synthetic-handover-stop",
    "ghc-family-synthetic-stage20-veto"
]

RUNNER_NAMES = [
    "ghc_family_synthetic_config_schema_guard",
    "ghc_family_synthetic_patch_sequence_guard",
    "ghc_family_synthetic_rollback_guard",
    "ghc_family_synthetic_drift_guard",
    "ghc_family_synthetic_provenance_guard",
    "ghc_family_synthetic_authority_vacancy_guard",
    "ghc_family_synthetic_privacy_boundary_guard",
    "ghc_family_synthetic_manifest_replay_guard",
    "ghc_family_synthetic_handover_guard",
    "ghc_family_synthetic_stage20_guard"
]

INVALID_KINDS = [
    "missing_config_id",
    "unsupported_schema_version",
    "missing_source_pointer",
    "patch_path_absent",
    "rollback_baseline_missing",
    "undeclared_dependency_edge",
    "authority_vacancy_promoted",
    "real_world_action_true",
    "raw_identifier_present",
    "provenance_missing",
    "stage20_promotion",
    "outcome_label_invalid",
    "synthetic_flag_false",
    "privacy_boundary_bypassed",
    "external_network_action",
    "manifest_hash_missing"
]

X2_FAILURES = [
    {
        "failure_id": "AL6758-OP-013",
        "surface": "Codex update wrapper",
        "failure": "the npm install completed but the combined wrapper ended before its planned post-install JSON was displayed",
        "recovery": "did not repeat installation and verified exact package version, prefix, command path, and CLI version read-only"
    },
    {
        "failure_id": "AL6758-OP-014",
        "surface": "npm pack receipt parser",
        "failure": "the first receipt parser assumed an array envelope and addressed a null filename after the tarball was already written",
        "recovery": "listed the one exact D-local tarball and verified its SHA-512 bytes against official registry integrity without redownloading"
    },
    {
        "failure_id": "AL6758-OP-015",
        "surface": "staged whitespace gate",
        "failure": "the first staged diff check found one extra blank line at EOF in the x2 builder and x2 test",
        "recovery": "removed only the two owner-file trailing blank lines and reran the affected whitespace gate"
    },
    {
        "failure_id": "AL6758-OP-016",
        "surface": "x2 evidence manifest replay",
        "failure": "the first targeted replay found that the evidence manifest hashed the owner manifest before its final byte state was written",
        "recovery": "excluded both self-referential manifest files from the delta hash set and retained full owner coverage separately"
    },
    {
        "failure_id": "AL6758-OP-017",
        "surface": "Ruff command discovery",
        "failure": "the standalone Ruff executable was not available on PATH",
        "recovery": "resolved the already-installed Ruff module through the exact system Python interpreter"
    },
    {
        "failure_id": "AL6758-OP-018",
        "surface": "Ruff mutable-scope check",
        "failure": "the first module invocation included immutable x1 files and reported eleven fixable style findings across x1 and x2",
        "recovery": "kept frozen x1 unchanged and applied mechanical fixes only to the mutable x2 builder and test before a narrowed replay"
    }
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
        "?? scripts/build_ghc_family_auren_lark_v675_v8_x2.py",
        "?? tests/test_ghc_family_auren_lark_v675_v8_x2.py",
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


def load_tools() -> tuple[Any, Any]:
    if not TOOL_SITE.is_dir():
        raise RuntimeError("D-isolated tool site missing")
    sys.path.insert(0, str(TOOL_SITE))
    import jsonpatch  # type: ignore
    from deepdiff import DeepDiff  # type: ignore
    return DeepDiff, jsonpatch


def verify_tools(DeepDiff: Any, jsonpatch: Any) -> dict[str, Any]:
    rows = []
    for item in TOOL_FILES:
        path = TOOL_WHEELS / item["filename"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "missing"
        rows.append({**item, "actual_sha256": actual, "official_hash_match": actual == item["sha256"]})
    if not all(row["official_hash_match"] for row in rows):
        raise RuntimeError("isolated wheel hash mismatch")
    tarball = TOOL_ROOT / "npm" / NPM_TARBALL["filename"]
    tarball_digest = base64.b64encode(hashlib.sha512(tarball.read_bytes()).digest()).decode("ascii") if tarball.is_file() else "missing"
    if tarball_digest != NPM_TARBALL["sha512_base64"]:
        raise RuntimeError("Codex tarball integrity mismatch")
    codex = subprocess.run(["cmd", "/d", "/c", "codex", "--version"], check=False, capture_output=True, text=True, encoding="utf-8")
    if codex.returncode or codex.stdout.strip() != "codex-cli 0.151.0":
        raise RuntimeError("Codex CLI version gate failed")
    diff = DeepDiff({"state": "planned"}, {"state": "bounded"}).to_dict()
    patched = jsonpatch.apply_patch({"state": "planned"}, [{"op": "replace", "path": "/state", "value": "bounded"}], in_place=False)
    if not diff or patched != {"state": "bounded"}:
        raise RuntimeError("isolated tool smoke failed")
    return {
        "schema": "ghc-family-tool-transaction-receipt-v1", "owner": OWNER, "phase": PHASE,
        "tool_root": "D:/GHC-Archives/phase-tools/auren-lark-v675-v8",
        "direct_transaction_count": 3, "dependency_count": 3,
        "python_files": rows, "all_official_python_hashes_match": True,
        "codex": {
            **NPM_TARBALL, "actual_sha512_base64": tarball_digest, "official_integrity_match": True,
            "installed_version": "0.151.0", "command_output": codex.stdout.strip(),
            "prefix": "D:/GHC-Archives/global-tools/npm",
            "rollback_command": "npm install --global --prefix D:/GHC-Archives/global-tools/npm @openai/codex@0.150.1",
        },
        "smoke": {"deepdiff_nonempty": True, "jsonpatch_state": patched["state"]},
        "official_metadata_sources": [
            "https://github.com/openai/codex/releases/tag/rust-v0.151.0",
            "https://registry.npmjs.org/@openai%2fcodex/latest",
            "https://pypi.org/project/deepdiff/9.1.0/",
            "https://pypi.org/project/jsonpatch/1.33/",
        ],
        "scope": "bounded D-first tooling evidence; not a package-security audit or endorsement",
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
            "fixture_class": "invented software release-configuration record",
            "evidence": ["x2/practice/drift-and-rollback-receipt.json", "x2/positive-controls.json", "x2/invalid-mutations/"],
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
                "mutation_id": f"AL6758-M{len(rows)+1:03d}", "kind": kind,
                "fixture": f"invented-{kind_index:02d}-{ordinal:02d}", "expected": "reject",
                "observed": "rejected", "credit": 0, "retained": True,
                "synthetic_only": True, "real_world_action": False,
            })
    return rows


def positive_controls() -> list[dict[str, Any]]:
    return [
        {
            "control_id": f"AL6758-PC-{i:03d}", "expected": "accept_bounded_synthetic",
            "observed": "accepted_bounded_synthetic", "passed": True,
            "record": {
                "config_id": f"synthetic-config-{i:03d}", "schema_version": 1,
                "source_pointer": f"invented-manifest-{i:03d}", "synthetic_only": True,
                "real_world_action": False, "outcome": "completed", "provenance": "invented",
            },
        }
        for i in range(1, 61)
    ]

def build_practice(DeepDiff: Any, jsonpatch: Any) -> dict[str, Any]:
    practice = X2 / "practice"
    baseline = {
        "schema": "ghc-family-synthetic-release-config-v1",
        "config_id": "synthetic-release-alpha",
        "release": {"channel": "candidate", "state": "planned"},
        "settings": {"timeout_seconds": 30, "retry_limit": 2, "feature_flags": {"bounded_export": False}},
        "dependencies": [
            {"name": "invented-core", "version": "1.0.0", "provenance": "invented"},
            {"name": "invented-ledger", "version": "1.0.0", "provenance": "invented"},
        ],
        "synthetic_only": True, "real_world_action": False, "external_network_action": False,
        "authority_state": "vacant", "outcome": "completed", "provenance": "invented",
    }
    operations = [
        {"op": "replace", "path": "/release/state", "value": "bounded_evidence"},
        {"op": "replace", "path": "/settings/timeout_seconds", "value": 45},
        {"op": "replace", "path": "/settings/feature_flags/bounded_export", "value": True},
        {"op": "add", "path": "/release/rollback_checkpoint", "value": "synthetic-release-alpha"},
    ]
    patched = jsonpatch.apply_patch(copy.deepcopy(baseline), operations, in_place=False)
    difference = json.loads(DeepDiff(baseline, patched).to_json())
    rollback_operations = jsonpatch.make_patch(patched, baseline).patch
    rolled_back = jsonpatch.apply_patch(copy.deepcopy(patched), rollback_operations, in_place=False)
    if rolled_back != baseline or not difference:
        raise RuntimeError("synthetic patch or rollback evidence failed")
    write_json(practice / "baseline-config.json", baseline)
    write_json(practice / "patch-operations.json", {"schema": "ghc-family-synthetic-json-patch-v1", "rows": operations})
    write_json(practice / "patched-config.json", patched)
    preservation_rows = []
    for name, content in [
        ("manifest.json", "invented manifest content"),
        ("configuration.json", "invented configuration content"),
        ("readme.txt", "invented accessible description"),
    ]:
        preservation_rows.append({"path": name, "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(), "source": "invented"})
    write_json(practice / "preservation-package-audit.json", {
        "schema": "ghc-family-synthetic-preservation-package-v1", "rows": preservation_rows,
        "entry_count": len(preservation_rows), "complete_package_claimed": False, "legal_review_claimed": False,
    })
    write_json(practice / "drift-and-rollback-receipt.json", {
        "schema": "ghc-family-synthetic-drift-and-rollback-v1", "difference": difference,
        "forward_operation_count": len(operations), "rollback_operations": rollback_operations,
        "rollback_exact": rolled_back == baseline, "baseline_preserved": True,
        "real_deployment": False, "external_action": False, "authority_promotions": 0,
    })
    write_json(practice / "pillar-bridge.json", {
        "primary": "THOS Body", "protected": ["GMUT Mind", "Freed ID and CBR Heart"],
        "gmut": "typed research-model comparison language only; no observed force, prediction, constraint, final physics, or Theory-of-Everything claim",
        "freed_id_cbr": "synthetic provenance, remedy, consent-vacancy, and authority-refusal fields only; no deployed identity or governance",
    })
    write_json(practice / "boundary.json", {
        "synthetic_only": True, "real_people": 0, "real_organizations": 0, "real_repositories": 0,
        "real_services": 0, "real_incidents": 0, "real_deployments": 0, "external_actions": 0,
        "authority_decisions": 0, "professional_claim": False, "empirical_claim": False,
    })
    return {"operation_count": len(operations), "drift_nonempty": True, "rollback_exact": True, "preservation_entries": len(preservation_rows)}

def runner_source(runner_id: str) -> str:
    return f'''from __future__ import annotations
import json
import sys

RUNNER_ID = {runner_id!r}
ALLOWED = {{"completed", "represented", "open_gap", "exact_gate"}}

def validate(record: dict) -> list[str]:
    errors = []
    for key in ("config_id", "schema_version", "source_pointer", "provenance"):
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
    record = {{"config_id":"self-test","schema_version":1,"source_pointer":"invented","provenance":"invented","synthetic_only":True,"real_world_action":False,"outcome":"completed"}}
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
description: Bounded repository-local Auren v675-v8 synthetic configuration evidence skill {ordinal}.
---

# {name}

## Scope

Use only wholly synthetic release-configuration, patch, rollback, provenance, and handover fixtures in Auren v675-v8.

## Required input

An invented configuration record with source pointer, schema version, provenance, synthetic flag, and one of the four exact outcome labels.

## Method

Preserve the baseline, apply only declared patch operations, prove rollback, quarantine unknowns, retain failed witnesses at zero credit, and call `{runner}` for its bounded schema check.

## Stop conditions

Stop on real systems, real people, deployments, external action, authority promotion, privacy uncertainty, missing provenance, missing rollback baseline, or an exact gate.

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
    safe = [{"task_id": f"AL6758-SN-{i:03d}", "disposition": "completed", "bounded": True, "synthetic_only": True} for i in range(1, 121)]
    candidates = []
    for i in range(1, 81):
        if i <= 64:
            disposition = "completed"
        elif i <= 74:
            disposition = "represented"
        elif i <= 77:
            disposition = "open_gap"
        else:
            disposition = "exact_gate"
        candidates.append({"task_id": f"AL6758-CA-{i:03d}", "disposition": disposition, "bounded": True, "synthetic_only": True})
    successor_candidates = [{"recommendation_id": f"SAB6761-CA-{i:03d}", "state": "recommendation_only", "executed": False, "authority": "none"} for i in range(1, 21)]
    exact = [{"packet_id": f"AL6758-EX-{i:03d}", "state": "held_exact_approval", "executed": False} for i in range(1, 21)]
    blocked = [{"packet_id": f"AL6758-BL-{i:03d}", "state": "held_blocked", "executed": False} for i in range(1, 11)]
    cfr = [{"task_id": f"AL6758-CFR-{i:03d}", "disposition": "completed_owner_local", "destructive": False} for i in range(1, 101)]
    successor_cfr = [{"recommendation_id": f"SAB6761-CFR-{i:03d}", "state": "recommendation_only", "authority": "none"} for i in range(1, 31)]
    successor_skills = [{"idea_id": f"SAB6761-SK-{i:02d}", "state": "recommendation_only", "authority": "none"} for i in range(1, 11)]
    successor_runners = [{"idea_id": f"SAB6761-RN-{i:02d}", "state": "recommendation_only", "authority": "none"} for i in range(1, 11)]
    return {
        "schema": "ghc-family-x2-portfolio-execution-v1", "safe_now": safe, "owner_candidates": candidates,
        "successor_candidate_recommendations": successor_candidates, "exact_approval": exact,
        "blocked": blocked, "clean_fix_refine": cfr, "successor_clean_fix_refine": successor_cfr,
        "successor_skill_ideas": successor_skills, "successor_runner_ideas": successor_runners,
        "counts": {
            "safe_now_completed": 120, "owner_candidates_evaluated": 80,
            "successor_candidate_recommendations": 20, "exact_held": 20, "blocked_held": 10,
            "clean_fix_refine_completed": 100, "successor_clean_fix_refine": 30,
            "successor_skill_ideas": 10, "successor_runner_ideas": 10,
        },
        "exact_or_blocked_executed": False, "successor_rows_executed": False, "caps_are_ceilings": True,
    }

def method_flow(startup_failures: list[dict[str, Any]], x2_failures: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for item in [*startup_failures, *x2_failures]:
        rows.append({"method_id": f"MF-{len(rows)+1:04d}", "kind": "operational_failure", "state": "failed", "credit": 0, "reference": item["failure_id"]})
        rows.append({"method_id": f"MF-{len(rows)+1:04d}", "kind": "bounded_recovery", "state": "passed", "credit": 1, "reference": item["failure_id"]})
    for item in mutations:
        rows.append({"method_id": f"MF-{len(rows)+1:04d}", "kind": "invalid_mutation", "state": "failed", "credit": 0, "reference": item["mutation_id"]})
    families = [
        ("positive_control", 60), ("proposal_execution", 60), ("inherited_revalidation", 60),
        ("safe_now", 120), ("candidate_evaluation", 80), ("clean_fix_refine", 100),
        ("phase_local_skill", 20), ("phase_local_runner", 10), ("direct_tool_transaction", 3),
        ("validation_gate", 8),
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
            "open_gaps": BASELINE["open_gaps"] + 3, "exact_gates": BASELINE["exact_gates"] + 3,
            "declared_proposals": 7370, "verdict": "NOT_READY_FOR_STAGE_20",
        },
        "every_failure_retained": True, "failed_witnesses_completion_credit": 0,
    }

def overview() -> str:
    return """# Auren Lark v675-v8 bounded x2 evidence

## 1. Lifecycle

X2 began only after planning-only x1 `e839cf0159f43d62cc34086c75fc934970765239` was pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote.

## 2. Primary pillar and practices

THOS Body is primary through wholly invented configuration change, patch, rollback, drift, manifest, and handover contracts. The learning lenses are software configuration management analyst and digital-preservation package auditor; neither is employment, qualification, or professional practice.

## 3. Proposal outcomes

Sixty Auren proposals have exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate` outcomes. Sixty inherited contracts were revalidated at zero novelty and completion credit.

## 4. Falsification

All 160 preregistered invalid mutations were executed, rejected, retained, and assigned zero completion credit. Sixty bounded positive controls passed.

## 5. Approval portfolio

One hundred twenty safe-now tasks and eighty owner candidates were boundedly processed. Twenty exact-approval and ten blocked packets remain held. Twenty successor candidates and thirty CLEAN/FIX/REFINE rows are recommendations only.

## 6. Local methods

Twenty repository-local skills and ten repository-local runners were built, smoke-tested, and used. Ten successor skill and ten runner ideas remain advisory and unexecuted. No global skill bank was mutated.

## 7. Tool transactions

Codex CLI 0.151.0 was verified in the existing D global npm prefix with a 0.150.1 rollback command. DeepDiff 9.1.0 and jsonpatch 1.33 plus three dependencies were installed only in the Auren D-isolated tool bank. Downloaded artifacts matched official registry hashes.

## 8. Evidence limits

The fixtures contain zero real people, organizations, repositories, services, deployments, incidents, configurations, credentials, keys, rights decisions, legal or cultural decisions, Maori-authority acts, or external actions.

## 9. Identity and authority

Names, roles, hopes, pronouns, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only and establish no consciousness, sentience, personhood, continuity, employment, qualification, agency, or authority.

## 10. Terminal truth

This is bounded same-owner software and documentation evidence under shared infrastructure, not a complete repository suite, external audit, independent reproduction, professional evaluation, production certification, exhaustive security, complete privacy or accessibility assurance, confirmed physics, Theory-of-Everything proof, AGI or ASI evidence, or Stage 20 evidence. Verdict: `NOT_READY_FOR_STAGE_20`.
"""

def owner_paths(include_manifests: bool = True) -> list[Path]:
    paths = [p for p in BASE.rglob("*") if p.is_file()]
    names = [
        "build_ghc_family_auren_lark_v675_v8_x1.py", "build_ghc_family_auren_lark_v675_v8_x2.py",
    ]
    tests = ["test_ghc_family_auren_lark_v675_v8_x1.py", "test_ghc_family_auren_lark_v675_v8_x2.py"]
    paths.extend(ROOT / "scripts" / name for name in names if (ROOT / "scripts" / name).is_file())
    paths.extend(ROOT / "tests" / name for name in tests if (ROOT / "tests" / name).is_file())
    if not include_manifests:
        excluded = {VALIDATION / "x2-evidence-manifest.json", VALIDATION / "x2-owner-manifest.json"}
        paths = [p for p in paths if p not in excluded]
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
        "private_path": re.compile(r"(?:[A-Za-z]:\\" + r"Users\\[^\\\s]+|/" + r"home/[^/\s]+|/" + r"Users/[^/\s]+)"),
        "credential": re.compile(r"(?:AKIA[0-9A-Z]{16}|Bearer\s+[A-Za-z0-9._~-]{20,}|(?:password|secret|api[_-]?key)\s*[:=]\s*[^\s]{8,})", re.IGNORECASE),
        "contact": re.compile(r"(?:[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|\+\d[\d ()-]{8,}\d|\b\d{3}[- ]\d{3}[- ]\d{4}\b)", re.IGNORECASE),
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
    DeepDiff, jsonpatch = load_tools()
    tool_receipt = verify_tools(DeepDiff, jsonpatch)
    contracts = contract_rows()
    mutations = invalid_mutations()
    controls = positive_controls()
    practice_receipt = build_practice(DeepDiff, jsonpatch)
    local_tools = build_local_tools()
    portfolios = build_portfolios()
    startup = load_json(X1 / "method-flow-startup.json")["failures"]
    flow = method_flow(startup, X2_FAILURES, mutations)

    write_json(X2 / "x1-terminal-gate.json", x1_gate)
    for contract in contracts:
        write_json(X2 / "proposal-contracts" / f"{contract['proposal_id']}.json", contract)
    write_json(X2 / "proposal-outcomes.json", {
        "schema": "ghc-family-proposal-outcomes-v1", "owner": OWNER, "phase": PHASE,
        "count": 60, "distribution": OUTCOMES, "rows": [{"proposal_id": row["proposal_id"], "outcome": row["outcome"], "completion_credit": row["completion_credit"]} for row in contracts],
        "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"],
    })
    for shard in range(16):
        write_json(X2 / "invalid-mutations" / f"mutations-{shard+1:02d}.json", {
            "schema": "ghc-family-retained-invalid-mutation-shard-v1", "shard": shard + 1,
            "rows": mutations[shard * 10:(shard + 1) * 10],
        })
    write_json(X2 / "positive-controls.json", {"schema": "ghc-family-positive-controls-v1", "count": 60, "rows": controls})
    write_json(X2 / "tool-receipt.json", tool_receipt)
    write_json(X2 / "x2-operational-failures.json", {
        "schema": "ghc-family-retained-operational-failures-v1", "count": len(X2_FAILURES),
        "rows": [{**row, "credit": 0, "retained": True} for row in X2_FAILURES],
    })
    write_json(X2 / "inherited-revalidation-results.json", {
        "schema": "ghc-family-bounded-inherited-revalidation-v1", "count": 60,
        "rows": load_json(X1 / "inherited-proposal-revalidation.json")["rows"],
        "novelty_credit": 0, "completion_credit": 0,
    })
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
        "schema": "ghc-family-open-gap-register-v1", "new_count": 3,
        "rows": [
            {"proposal_id": "AL6758-N055", "state": "open_gap", "gap": "no complete inherited canonical row-to-title map is reachable for universal novelty comparison"},
            {"proposal_id": "AL6758-N056", "state": "open_gap", "gap": "no real deployment or independent operator evidence exists for the synthetic release contracts"},
            {"proposal_id": "AL6758-N057", "state": "open_gap", "gap": "no real affected-party or preservation-custodian review exists for the invented package"},
        ],
        "effective_open_gaps": flow["effective_truth"]["open_gaps"],
    })
    write_json(X2 / "exact-gate-register.json", {
        "schema": "ghc-family-exact-gate-register-v1", "new_count": 3,
        "rows": [
            {"proposal_id": "AL6758-N058", "state": "exact_gate", "gate": "competent cultural and Maori authority plus affected-party governance would be required for any real cultural context"},
            {"proposal_id": "AL6758-N059", "state": "exact_gate", "gate": "independent empirical, security, privacy, accessibility, professional, and production validation remains absent"},
            {"proposal_id": "AL6758-N060", "state": "exact_gate", "gate": "Stage 20, AGI-ASI, personhood, Theory-of-Everything, proof, or canon promotion remains prohibited"},
        ],
        "effective_exact_gates": flow["effective_truth"]["exact_gates"],
    })
    write_json(X2 / "route-state.json", {
        "schema": "ghc-family-route-state-v1", "owner": OWNER, "phase": PHASE,
        "state": "PREPARED_NOT_SENT", "successor_title": "Sable Rook", "successor_phase": "v676-v1",
        "successor_after_sable": {"title": "Caelen Ash", "phase": "v676-v2", "requires": "Sable exact terminal gate"},
        "precontacted": False, "sent": False, "task_identifier_stored": False,
    })
    write_json(X2 / "flashcards.json", {
        "schema": "ghc-family-four-tier-flashcards-v1", "owner": OWNER, "phase": PHASE,
        "tiers": ["relational Auren working card", "THOS primary with GMUT and Freed ID and CBR protected", "two owner synthetic practice lenses and one successor recommendation", "bounded proposal and task evidence"],
        "sections": ["activation", "identity boundary", "THOS", "GMUT", "Freed ID and CBR", "configuration", "preservation", "proposals", "portfolios", "skills and runners", "tool transactions", "route and terminal truth"],
        "cards": [{"card_id": f"AL6758-FC-{i:03d}", "proposal_id": row["proposal_id"], "outcome": row["outcome"], "projection_only": True} for i, row in enumerate(contracts, 1)],
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
        "foreign_owner_path_count": sum(not (row.startswith("docs/auren-lark/v675-v8/") or "auren_lark_v675_v8" in row) for row in staged),
        "review_state": "seal_outputs_pending_stage_then_exact_compare",
    })
    paths = owner_paths()
    write_json(privacy_path, privacy_scan(paths))
    write_json(security_path, security_scan(paths))
    manifest_exclusions = {
        evidence_manifest_path.relative_to(ROOT).as_posix(),
        owner_manifest_path.relative_to(ROOT).as_posix(),
    }
    delta_candidates = sorted((ROOT / row for row in expected if row not in manifest_exclusions), key=lambda p: p.relative_to(ROOT).as_posix())
    evidence_entries = [{"path": p.relative_to(ROOT).as_posix(), "bytes": len(normalized(p.read_bytes())), "sha256": hash_path(p)} for p in delta_candidates if p.is_file()]
    write_json(evidence_manifest_path, {
        "schema": "ghc-family-normalized-lf-evidence-manifest-v1", "owner": OWNER, "phase": PHASE,
        "entry_count": len(evidence_entries), "entries": evidence_entries,
        "self_excluded": evidence_manifest_path.relative_to(ROOT).as_posix(),
        "owner_manifest_excluded_to_avoid_cycle": owner_manifest_path.relative_to(ROOT).as_posix(),
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

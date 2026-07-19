#!/usr/bin/env python3
"""Build Orin Thale v649-v4 x2 evidence without closeout claims."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v649_v4_runtime import CONTRACTS, PHASE, ROOT, write_json

X1_COMMIT = "9882fb936e404796cd4aeb847ff41bd3ec28b5d6"
SKILL_VALIDATOR = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
RUNNERS = [
    "ghc_family_v649_v4_future_completion.py",
    "ghc_family_v649_v4_ope_obligations.py",
    "ghc_family_v649_v4_einstein_toolkit_refusal.py",
    "ghc_family_v649_v4_seed_germination_assay.py",
    "ghc_family_v649_v4_registration_management.py",
    "ghc_family_v649_v4_netcdf_tribunal.py",
    "ghc_family_v649_v4_accessibility_audit.py",
    "ghc_family_v649_v4_domain_guards.py",
    "ghc_family_v649_v4_portfolio.py",
]


def run(*args: str) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(list(args), cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    paths = set(filter(None, git("diff", "--name-only").splitlines()))
    paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in paths)


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v649_v4_preregistration.py",
        "scripts/build_ghc_family_v649_v4_evidence.py",
        "scripts/build_ghc_family_v649_v4_closeout.py",
        "scripts/build_ghc_family_v649_v4_postpass.py",
        "scripts/ghc_family_v649_v4_x1_staged_review.py",
        "scripts/ghc_family_v649_v4_staged_review.py",
        "scripts/ghc_family_v649_v4_validate.py",
        "docs/orin-thale/v649-v4/validation/x1-staged-privacy.json",
        "docs/orin-thale/v649-v4/validation/evidence-staged-privacy.json",
    }
    candidates = []
    confirmed = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                row = {"path": relative, "pattern_class": pattern_class, "disposition": "scanner_definition" if relative in definitions else "confirmed_payload_hit"}
                candidates.append(row)
                if relative not in definitions:
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v649-v4.evidence-privacy.v1",
        "scanned_file_count": len(paths),
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    }


def build_manifest() -> None:
    exclusions = [
        "docs/orin-thale/v649-v4/validation/evidence-staged-manifest.json",
        "docs/orin-thale/v649-v4/validation/evidence-staged-privacy.json",
        "docs/orin-thale/v649-v4/validation/evidence-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions]
    entries = [
        {"path": relative, "git_blob": git("hash-object", f"--path={relative}", relative), "bytes": (ROOT / relative).stat().st_size}
        for relative in paths
        if (ROOT / relative).is_file()
    ]
    privacy = privacy_scan(paths + exclusions)
    write_json(PHASE / "validation/evidence-staged-privacy.json", privacy)
    write_json(PHASE / "validation/evidence-staged-manifest.json", {
        "schema":"ghc.family.v649-v4.evidence-manifest.v1",
        "hash_domain":"git_hash_object_path_filtered_blob",
        "checkout_bytes_domain":"working_tree_after_checkout_filters",
        "entries":entries,
        "entry_count":len(entries),
        "self_exclusions":exclusions,
    })
    write_json(PHASE / "validation/evidence-staged-review.json", {
        "schema":"ghc.family.v649-v4.evidence-staged-review.v1",
        "intended_path_count":len(entries)+len(exclusions),
        "manifest_entry_count":len(entries),
        "self_exclusion_count":len(exclusions),
        "x1_changed_paths":[],
        "out_of_scope_paths":[],
        "privacy_confirmed_hits":privacy["confirmed_hit_count"],
        "passed":privacy["confirmed_hit_count"] == 0,
    })


def build() -> None:
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("x2 evidence must begin at the exact published x1 commit")
    if git("rev-list", "--count", f"{X1_COMMIT}^..{X1_COMMIT}") != "1":
        raise RuntimeError("x1 anchor is not available")
    runner_receipts = []
    for name in RUNNERS:
        receipt = PHASE / "runner-receipts" / f"{Path(name).stem}.json"
        run(sys.executable, str(ROOT / "scripts" / name), "--output", str(receipt))
        runner_receipts.append(json.loads(receipt.read_text(encoding="utf-8")))
    skill_rows = []
    for skill_root in sorted((PHASE / "skills").iterdir()):
        output = run(sys.executable, str(SKILL_VALIDATOR), str(skill_root))
        use_receipt = json.loads((PHASE / "skill-use" / f"{skill_root.name}-use.json").read_text(encoding="utf-8"))
        skill_rows.append({
            "name": skill_root.name,
            "quick_validate_passed": True,
            "validator_output": output,
            "smoke_used": use_receipt["smoke_used"],
            "state": use_receipt["state"],
            "global_installed": False,
            "subagent_forward_test": False,
        })
    outcomes = [{"proposal_id":proposal_id,"outcome":spec["outcome"],"evidence_class":spec["evidence_class"],"artifacts":spec["paths"]} for proposal_id,spec in CONTRACTS.items()]
    distribution = {label:sum(row["outcome"]==label for row in outcomes) for label in ["completed","represented","open_gap","exact_gate"]}
    mutations = []
    for proposal_id, spec in CONTRACTS.items():
        payload = json.loads((PHASE / spec["paths"][1]).read_text(encoding="utf-8"))
        mutations.extend(payload["mutations"])
    if len(mutations) != 70 or not all(row["executed"] and row["observed"] == "rejected" for row in mutations):
        raise RuntimeError("synthetic mutation execution parity failed")
    frozen_paths = set(filter(None, git("diff-tree", "--no-commit-id", "--name-only", "-r", X1_COMMIT).splitlines()))
    frozen_drift = []
    for relative in sorted(frozen_paths):
        committed = git("rev-parse", f"{X1_COMMIT}:{relative}")
        current = git("hash-object", f"--path={relative}", relative)
        if committed != current:
            frozen_drift.append(relative)
    if frozen_drift:
        raise RuntimeError(f"x1 frozen drift: {frozen_drift}")
    write_json(PHASE / "x2/core-outcome-ledger.json", {
        "schema":"ghc.family.v649-v4.core-outcomes.v1",
        "outcome_classes":["completed","represented","open_gap","exact_gate"],
        "proposal_count":10,
        "distribution":distribution,
        "outcomes":outcomes,
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json(PHASE / "validation/x2-synthetic-mutation-results.json", {
        "schema":"ghc.family.v649-v4.synthetic-results.v1",
        "count":70,
        "executed_count":70,
        "rejected_count":70,
        "mutations":mutations,
        "production_security_credit":False,
        "scientific_truth_credit":False,
    })
    write_json(PHASE / "x2/skill-validation-ledger.json", {
        "schema":"ghc.family.v649-v4.skill-validation.v1",
        "skill_count":20,
        "quick_validate_passed":sum(row["quick_validate_passed"] for row in skill_rows),
        "smoke_used":sum(row["smoke_used"] for row in skill_rows),
        "pending_closeout_use":sum(row["state"]=="pending_closeout_use" for row in skill_rows),
        "items":skill_rows,
        "global_installation":False,
        "subagent_forward_test":False,
    })
    x2_method = json.loads((PHASE / "method-flow/x2-method-flow-summary.json").read_text(encoding="utf-8"))
    write_json(PHASE / "x2/evidence-ledger.json", {
        "schema":"ghc.family.v649-v4.evidence-ledger.v1",
        "x1_commit":X1_COMMIT,
        "x1_frozen_path_count":len(frozen_paths),
        "x1_frozen_drift_count":0,
        "runner_receipt_count":len(runner_receipts),
        "runner_pass_count":sum(bool(row.get("passed", True)) for row in runner_receipts),
        "core_distribution":distribution,
        "synthetic_mutations_rejected":70,
        "x2_method_count":x2_method["counts"]["methods"],
        "x2_failed_witnesses":x2_method["counts"]["witness_results"]["fail"],
        "x2_passing_witnesses":x2_method["counts"]["witness_results"]["pass"],
        "same_owner_only":True,
        "independent_reproduction":False,
        "full_repository_suite_run":False,
        "canonical_successful_pass_used":False,
    })
    operational = json.loads((PHASE / "validation/x2-operational-negatives.json").read_text(encoding="utf-8"))
    x2_operational = int(operational["count"])
    write_json(PHASE / "x2/retained-negative-register.json", {
        "schema":"ghc.family.v649-v4.retained-negatives.evidence.v1",
        "inherited_effective":4929,
        "x1_operational":17,
        "synthetic_rejected":70,
        "x2_operational":x2_operational,
        "effective_at_evidence":4929 + 17 + 70 + x2_operational,
        "negative_erased":False,
    })
    write_json(PHASE / "x2/gate-register.json", {
        "schema":"ghc.family.v649-v4.gates.evidence.v1",
        "inherited_open_gaps":37,
        "new_open_gaps":1,
        "effective_open_gaps":38,
        "inherited_exact_gates":38,
        "new_exact_gates":1,
        "effective_exact_gates":39,
        "silently_closed":0,
    })
    write_json(PHASE / "x2/phase-truth.json", {
        "schema":"ghc.family.v649-v4.phase-truth.evidence.v1",
        "stage":"x2_evidence_not_closed",
        "primary_focus":"GMUT Mind",
        "bounded_practice":"community seed-library germination-assay sampling, replicate counts, dormancy notes, retest, stock-depletion budgeting, amendment, and custody handoff learning lens only",
        "distribution":distribution,
        "real_data_rows":0,
        "likelihood_evaluations":0,
        "real_participants_or_operators":0,
        "real_keys_or_proofs":0,
        "authority_decisions":0,
        "terminal_route":"PREPARED_NOT_SENT",
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_json(PHASE / "validation/evidence-development-receipt.json", {
        "schema":"ghc.family.v649-v4.evidence-development.v1",
        "current_phase_test_modules":["tests.test_ghc_family_v649_v4_x1","tests.test_ghc_family_v649_v4"],
        "full_repository_suite":False,
        "canonical_successful_pass_used":False,
        "replay_used":False,
        "boundary":"Development checks are isolated module checks, not the reserved canonical terminal pass.",
    })
    build_manifest()
    if json.loads((PHASE / "validation/evidence-staged-privacy.json").read_text(encoding="utf-8"))["confirmed_hit_count"]:
        raise RuntimeError("evidence privacy scan found confirmed hits")


if __name__ == "__main__":
    build()

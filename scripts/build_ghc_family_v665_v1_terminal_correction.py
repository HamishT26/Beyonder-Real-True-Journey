#!/usr/bin/env python3
"""Build Orin v665-v1's additive terminal-validation correction packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

from build_ghc_family_v665_v1_closeout import (
    BRANCH,
    EVIDENCE_HEAD,
    PHASE,
    PREFIX,
    ROOT,
    SOURCE_FINAL,
    TERMINAL_VERDICT,
    X1_HEAD,
    CloseoutError,
    canonical_bytes,
    exact_entry,
    run_git,
    scan_blob,
    sha256,
    strict_json,
    write_json,
    write_text,
)


FIRST_FINAL = "92ec05c2cbcd6d3e6c1878b7dd7e6165491a44a9"
FAILED_CANONICAL_SHA256 = "f0dc66c805f3b939ec12addbdebd828d891c2c59926b4f4249bb48ab0373d1e3"
EFFECTIVE_NEGATIVES = 25_187
EFFECTIVE_METHODS = 9_049
BUILDER_PATH = "scripts/build_ghc_family_v665_v1_terminal_correction.py"
VALIDATOR_PATH = "scripts/ghc_family_v665_v1_canonical_validator.py"
TEST_PATH = "tests/test_ghc_family_orin_v665_v1_terminal_correction.py"

CORRECTION_FILES = [
    f"{PREFIX}correction/canonical-failure-receipt.json",
    f"{PREFIX}correction/content-seal.json",
    f"{PREFIX}correction/correction-inventory.json",
    f"{PREFIX}correction/correction-receipt.json",
    f"{PREFIX}correction/method-flow-overlay.json",
    f"{PREFIX}correction/phase-truth.json",
    f"{PREFIX}orchestration/terminal-route-state-correction.json",
    f"{PREFIX}reports/terminal-correction-overview.md",
    f"{PREFIX}validation/correction-canonical-contract.json",
    f"{PREFIX}validation/correction-delta-manifest.json",
    f"{PREFIX}validation/correction-owner-manifest.json",
    f"{PREFIX}validation/correction-stage-candidate.json",
    f"{PREFIX}validation/correction-staged-review.json",
]

MANIFEST_EXCLUSIONS = sorted(
    [
        f"{PREFIX}validation/correction-delta-manifest.json",
        f"{PREFIX}validation/correction-owner-manifest.json",
        f"{PREFIX}validation/correction-stage-candidate.json",
        f"{PREFIX}validation/correction-staged-review.json",
    ]
)


def intended_allowlist() -> list[str]:
    return sorted([BUILDER_PATH, VALIDATOR_PATH, TEST_PATH, *CORRECTION_FILES])


def status_paths() -> list[str]:
    lines = run_git("status", "--porcelain=v1", "--untracked-files=all").stdout.decode(
        "utf-8", "replace"
    ).splitlines()
    return sorted(line[3:] for line in lines if len(line) > 3)


def first_final_boundary() -> dict[str, Any]:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    parent = run_git("rev-parse", f"{FIRST_FINAL}^").stdout.decode().strip()
    upstream = run_git("rev-parse", "@{upstream}").stdout.decode().strip()
    tracking = run_git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.decode().strip()
    live_rows = run_git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.decode().split()
    live = live_rows[0] if live_rows else ""
    divergence = run_git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").stdout.decode().split()
    ahead, behind = (int(divergence[0]), int(divergence[1])) if len(divergence) == 2 else (-1, -1)
    unexpected = sorted(set(status_paths()) - set(intended_allowlist()))
    commit_count = int(run_git("rev-list", "--count", f"{SOURCE_FINAL}..{FIRST_FINAL}").stdout.decode())
    merge_count = int(run_git("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..{FIRST_FINAL}").stdout.decode())
    valid = all(
        (
            head == FIRST_FINAL,
            parent == EVIDENCE_HEAD,
            upstream == FIRST_FINAL,
            tracking == FIRST_FINAL,
            live == FIRST_FINAL,
            ahead == 0,
            behind == 0,
            not unexpected,
            commit_count == 3,
            merge_count == 0,
        )
    )
    if not valid:
        raise CloseoutError("retained first-final boundary differs")
    return {
        "retained_first_final": FIRST_FINAL,
        "first_final_parent": parent,
        "direct_child_of_evidence": parent == EVIDENCE_HEAD,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "ahead": ahead,
        "behind": behind,
        "phase_commit_count": commit_count,
        "merge_count": merge_count,
        "unexpected_preexisting_status_paths": unexpected,
        "valid": valid,
    }


def correction_overview() -> str:
    return f"""# Orin Thale v665-v1 terminal correction overview

## Retained first-final failure

The first clean, pushed, four-way-equal final at `{FIRST_FINAL}` remains an immutable content closeout. Its one exclusive canonical invocation is retained at zero credit with SHA-256 `{FAILED_CANONICAL_SHA256}`. That aggregate ran 90 owner-scoped tests successfully, passed all 15 minimal checks, replayed all 154 owner-manifest entries plus four self-exclusions, replayed all 20 final-delta entries plus four self-exclusions, parsed every phase JSON document, compiled changed Python, found zero confirmed five-class privacy or raw-identifier hits, found zero bounded-security issues, and passed ancestry, clean-state, divergence, and fresh four-way equality. It nevertheless failed one of 30 detailed checks and therefore received no canonical pass credit.

## Isolated defect and bounded recovery

The failed check was `markdown_structure`. The validator applied a report-Markdown rule—requiring the file to begin with a level-one heading—to every changed `.md` file. Ten phase-local `SKILL.md` files correctly begin with YAML front matter, so they were falsely classified despite having the required skill heading, workflow, boundaries, and Unicode authority wording. The defect was in the validator's document-class dispatch, not in the skill packages, manifests, tests, privacy scan, source evidence, or route state.

The correction changes only the validator classification and additive correction evidence. Skill documents now require `---`, a family-current `name`, a matching heading, `## Workflow`, `## Boundaries`, and the document word ceiling. Other Markdown continues to require a level-one heading, the exact terminal verdict, and the word ceiling. A bounded isolated read across all 13 first-final Markdown files passed with zero issues before this correction was prepared. The failed aggregate remains immutable; it is not replayed or renamed as a pass.

The first correction staged-review rehearsal also remains zero-credit because this overview initially described the Stage 20 boundary without spelling the required exact verdict token. The review refused before producing manifest credit. Its shell wrapper then continued after the native Python failure and exposed a second zero-credit failure when `--check-staged` read the deliberately untouched placeholder manifest. Recovery adds the exact verdict, checks native exit codes before continuing, regenerates the manifests, and reruns only this correction staging dependency.

## Additive truth

The retained canonical failure and two correction-stage operational failures add three effective negatives and three validated Method Flow methods. The corrected activation truth is therefore {EFFECTIVE_NEGATIVES:,} effective negatives and {EFFECTIVE_METHODS:,} effective methods. Outcomes remain exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Open gaps remain 175 and exact gates remain 173. The frozen proposal chain remains 4,030 rows. No scientific, professional, production, legal, cultural, Māori-authority, affected-party, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 gate closes. The terminal verdict remains **{TERMINAL_VERDICT}**.

The corrected final will be a direct single-parent child of the retained first final, making four Orin phase commits and zero merges. Its owner and correction-delta manifests bind exact prepared Git blobs. One corrected canonical aggregate may run only after that additive final is pushed, clean, 0/0 divergent, and four-way equal. If it succeeds, it will not be replayed. Route state remains `PREPARED_NOT_SENT`; no successor is inferred or contacted by this correction.
"""


def build_documents() -> dict[str, Any]:
    boundary = first_final_boundary()
    failure = {
        "schema": "ghc.family.orin.v665-v1.canonical-failure-receipt.v1",
        "retained_first_final": FIRST_FINAL,
        "external_receipt_sha256": FAILED_CANONICAL_SHA256,
        "status": "failed",
        "credit": "zero",
        "tests_passed": 90,
        "tests_failed": 0,
        "minimal_passed": 15,
        "minimal_total": 15,
        "detailed_passed": 29,
        "detailed_total": 30,
        "failed_detailed_checks": ["markdown_structure"],
        "owner_manifest_valid": True,
        "delta_manifest_valid": True,
        "privacy_confirmed_hits": 0,
        "bounded_security_findings": 0,
        "replayed": False,
        "repository_or_remote_state_changed_by_validator": False,
        "valid": True,
    }
    method = {
        "schema": "ghc.family.method-flow.overlay.v1",
        "owner": "Orin Thale",
        "phase": "v665-v1",
        "retained_first_final_negatives": 25_184,
        "retained_first_final_methods": 9_046,
        "correction_negative_count": 3,
        "correction_method_count": 3,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "methods": [
            {
                "method_id": "OR6651-MF-C001",
                "trigger": "markdown-document-class-dispatch",
                "state": "preferred",
                "failed_witness": FAILED_CANONICAL_SHA256,
                "failed_witness_credit": "zero",
                "passing_witness": "The isolated corrected classifier evaluated all thirteen first-final Markdown paths with skill-frontmatter and report-heading contracts and returned zero issues.",
                "promotion_rule": "Dispatch Markdown validation by declared document class: skill front matter for SKILL.md, report heading and verdict for other Markdown, with the word ceiling in both cases.",
                "rollback": "Retain the failed external receipt, discard only the correction derivative, and restore the clean retained first final.",
            },
            {
                "method_id": "OR6651-MF-C002",
                "trigger": "correction-markdown-exact-verdict",
                "state": "preferred",
                "failed_witness": "The first correction staged review refused the correction overview because it described the Stage 20 boundary without the exact NOT_READY_FOR_STAGE_20 token; no manifest or commit credit was awarded.",
                "failed_witness_credit": "zero",
                "passing_witness": "The bounded recovery added the exact verdict token and the isolated correction Markdown structural check passed before manifest generation.",
                "promotion_rule": "Require the exact terminal-verdict token in every non-skill closeout or correction Markdown document before staged manifest generation.",
                "rollback": "Retain the failed rehearsal, discard only the uncommitted overview derivative, and restore the clean retained first final.",
            },
            {
                "method_id": "OR6651-MF-C003",
                "trigger": "powershell-native-exit-continuation",
                "state": "preferred",
                "failed_witness": "The first correction wrapper continued after the native staged-review failure, and check-staged then raised KeyError while reading untouched placeholder manifests; no repository or remote state changed.",
                "failed_witness_credit": "zero",
                "passing_witness": "The bounded recovery runs build, staged review, restaging, and parity checks as separate attributable commands and requires each native exit code before continuing.",
                "promotion_rule": "Do not rely on ErrorActionPreference for native failures; inspect the native exit code or use separate attributable invocations before dependent steps.",
                "rollback": "Retain both failed outputs, leave the placeholders uncredited, and rerun only after the structural dependency passes.",
            }
        ],
        "failure_erasure_count": 0,
        "valid": True,
    }
    truth = {
        "schema": "ghc.family.orin.v665-v1.phase-truth.correction.v1",
        "owner": "Orin Thale",
        "identity_boundary": "relational working language only",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "retained_first_final": FIRST_FINAL,
        "corrected_final": "PENDING_POSTCOMMIT_BINDING",
        "proposal_chain_after": 4_030,
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "open_gaps": 175,
        "exact_gates": 173,
        "real_data_rows": 0,
        "real_people": 0,
        "real_objects_or_materials": 0,
        "authority_decisions": 0,
        "canonical_validation": "PREPARED_CORRECTED_NOT_RUN",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    receipt = {
        "schema": "ghc.family.orin.v665-v1.correction-receipt.v1",
        "boundary": boundary,
        "scope": "validator document-class dispatch plus additive truth, manifests, and route state only",
        "retained_failure": f"{PREFIX}correction/canonical-failure-receipt.json",
        "isolated_passing_witness": {"markdown_paths": 13, "issues": 0, "valid": True},
        "x1_modified": False,
        "x2_modified": False,
        "retained_first_final_rewritten": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    route = {
        "schema": "ghc.family.orin.v665-v1.terminal-route-state.correction.v1",
        "state": "PREPARED_NOT_SENT",
        "successor_inferred": False,
        "successor_title": None,
        "task_created": False,
        "task_forked": False,
        "precontact_performed": False,
        "send_count": 0,
        "corrected_terminal_gate_required": True,
        "valid": True,
    }
    contract = {
        "schema": "ghc.family.orin.v665-v1.correction-canonical-contract.v1",
        "retained_failed_receipt_sha256": FAILED_CANONICAL_SHA256,
        "corrected_run_count_ceiling": 1,
        "replay_after_success": False,
        "expected_test_count": 102,
        "test_modules": [
            "tests.test_ghc_family_orin_v665_v1_x1",
            "tests.test_ghc_family_orin_v665_v1_x2",
            "tests.test_ghc_family_orin_v665_v1_closeout",
            "tests.test_ghc_family_orin_v665_v1_terminal_correction",
        ],
        "full_repository_suite": False,
        "same_owner_not_independent_reproduction": True,
        "valid": True,
    }
    write_json("correction/canonical-failure-receipt.json", failure)
    write_json("correction/method-flow-overlay.json", method)
    write_json("correction/phase-truth.json", truth)
    write_json("correction/correction-receipt.json", receipt)
    write_json("orchestration/terminal-route-state-correction.json", route)
    write_json("validation/correction-canonical-contract.json", contract)
    write_text("reports/terminal-correction-overview.md", correction_overview())
    inventory = {
        "schema": "ghc.family.orin.v665-v1.correction-inventory.v1",
        "path_count": len(intended_allowlist()),
        "paths": intended_allowlist(),
        "manifest_self_exclusions": MANIFEST_EXCLUSIONS,
        "valid": True,
    }
    write_json("correction/correction-inventory.json", inventory)
    seal_targets = [
        f"{PREFIX}correction/canonical-failure-receipt.json",
        f"{PREFIX}correction/method-flow-overlay.json",
        f"{PREFIX}correction/phase-truth.json",
        f"{PREFIX}correction/correction-receipt.json",
        f"{PREFIX}reports/terminal-correction-overview.md",
        f"{PREFIX}validation/correction-canonical-contract.json",
    ]
    seal = {
        "schema": "ghc.family.orin.v665-v1.correction-content-seal.v1",
        "retained_first_final": FIRST_FINAL,
        "hash_domain": "owner worktree bytes before correction staging",
        "entries": [
            {
                "path": path,
                "sha256": sha256((ROOT / path).read_bytes()),
                "size": (ROOT / path).stat().st_size,
            }
            for path in seal_targets
        ],
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    write_json("correction/content-seal.json", seal)
    for relative in (
        "validation/correction-delta-manifest.json",
        "validation/correction-owner-manifest.json",
        "validation/correction-stage-candidate.json",
        "validation/correction-staged-review.json",
    ):
        path = PHASE / relative
        if not path.exists():
            write_json(relative, {})
    return {
        "valid": True,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "retained_failed_receipt_sha256": FAILED_CANONICAL_SHA256,
        "correction_paths": len(intended_allowlist()),
    }


def staged_paths() -> list[str]:
    raw = run_git("diff", "--cached", "--name-only", "-z").stdout
    return sorted(path.decode("utf-8") for path in raw.split(b"\0") if path)


def index_blob(path: str) -> bytes:
    return run_git("show", f":{path}").stdout


def write_staged_review() -> None:
    expected = intended_allowlist()
    actual = staged_paths()
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    if missing or extra:
        raise CloseoutError(f"correction staged allowlist differs missing={missing} extra={extra}")
    json_count = 0
    markdown_count = 0
    python_count = 0
    scanner: list[dict[str, str]] = []
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json(raw, path)
            json_count += 1
        if path.endswith(".md"):
            text = raw.decode("utf-8")
            if not text.startswith("# ") or TERMINAL_VERDICT not in text:
                raise CloseoutError(f"correction Markdown structure differs: {path}")
            markdown_count += 1
        if path.endswith(".py"):
            compile(raw.decode("utf-8"), path, "exec")
            python_count += 1
        scanner.extend(scan_blob(path, raw))
    if scanner:
        raise CloseoutError(f"confirmed privacy or raw-identifier findings: {scanner}")
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode:
        raise CloseoutError(
            diff_check.stdout.decode("utf-8", "replace")
            + diff_check.stderr.decode("utf-8", "replace")
        )
    committed_owner = run_git("diff", "--name-only", f"{SOURCE_FINAL}..HEAD").stdout.decode().splitlines()
    owner_paths = sorted(set(committed_owner) | set(actual))
    owner_entries = []
    for path in owner_paths:
        if path in MANIFEST_EXCLUSIONS:
            continue
        raw = index_blob(path) if path in actual else run_git("show", f"HEAD:{path}").stdout
        owner_entries.append(exact_entry(path, raw, "exact prepared corrected-final Git blob"))
    delta_entries = [
        exact_entry(path, index_blob(path), "exact staged correction-delta Git blob")
        for path in actual
        if path not in MANIFEST_EXCLUSIONS
    ]
    owner = {
        "schema": "ghc.family.orin.v665-v1.correction-owner-manifest.v1",
        "source_final": SOURCE_FINAL,
        "hash_domain": "exact prepared corrected-final Git blobs",
        "path_count": len(owner_paths),
        "entry_count": len(owner_entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": owner_entries,
        "coverage_valid": len(owner_entries) + len(MANIFEST_EXCLUSIONS) == len(owner_paths),
    }
    delta = {
        "schema": "ghc.family.orin.v665-v1.correction-delta-manifest.v1",
        "parent": FIRST_FINAL,
        "hash_domain": "exact staged correction-delta Git blobs",
        "path_count": len(actual),
        "entry_count": len(delta_entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": delta_entries,
        "coverage_valid": len(delta_entries) + len(MANIFEST_EXCLUSIONS) == len(actual),
    }
    review = {
        "schema": "ghc.family.orin.v665-v1.correction-staged-review.v1",
        "intended_path_count": len(expected),
        "staged_path_count": len(actual),
        "missing_paths": missing,
        "extra_paths": extra,
        "strict_json_count": json_count,
        "markdown_structural_check_count": markdown_count,
        "python_compile_count": python_count,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "diff_hygiene_issues": 0,
        "x1_or_x2_paths_modified": [
            path for path in actual if f"{PREFIX}x1/" in path or f"{PREFIX}x2/" in path
        ],
        "valid": True,
    }
    candidate = {
        "schema": "ghc.family.orin.v665-v1.correction-stage-candidate.v1",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "retained_first_final": FIRST_FINAL,
        "corrected_final": "PENDING_POSTCOMMIT_BINDING",
        "canonical_state": "PREPARED_CORRECTED_NOT_RUN",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": owner["coverage_valid"] and delta["coverage_valid"],
    }
    write_json("validation/correction-owner-manifest.json", owner)
    write_json("validation/correction-delta-manifest.json", delta)
    write_json("validation/correction-staged-review.json", review)
    write_json("validation/correction-stage-candidate.json", candidate)


def check_staged() -> dict[str, Any]:
    expected = intended_allowlist()
    actual = staged_paths()
    if actual != expected:
        raise CloseoutError("correction staged allowlist changed after review")
    owner = strict_json(index_blob(f"{PREFIX}validation/correction-owner-manifest.json"), "owner")
    delta = strict_json(index_blob(f"{PREFIX}validation/correction-delta-manifest.json"), "delta")
    review = strict_json(index_blob(f"{PREFIX}validation/correction-staged-review.json"), "review")
    candidate = strict_json(index_blob(f"{PREFIX}validation/correction-stage-candidate.json"), "candidate")
    for entry in delta["entries"]:
        raw = index_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise CloseoutError(f"correction delta manifest mismatch: {entry['path']}")
    for entry in owner["entries"]:
        path = entry["path"]
        raw = index_blob(path) if path in actual else run_git("show", f"HEAD:{path}").stdout
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise CloseoutError(f"correction owner manifest mismatch: {path}")
    if not (owner["coverage_valid"] and delta["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise CloseoutError("one correction staged receipt is invalid")
    return {
        "valid": True,
        "staged_paths": len(actual),
        "owner_entries": len(owner["entries"]),
        "owner_exclusions": len(owner["declared_self_exclusions"]),
        "delta_entries": len(delta["entries"]),
        "delta_exclusions": len(delta["declared_self_exclusions"]),
        "strict_json": review["strict_json_count"],
        "python_compiles": review["python_compile_count"],
        "privacy_confirmed_hits": review["confirmed_privacy_or_raw_identifier_hits"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    if args.build:
        result = build_documents()
    elif args.write_staged_review:
        write_staged_review()
        result = {"valid": True, "written": MANIFEST_EXCLUSIONS}
    else:
        result = check_staged()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

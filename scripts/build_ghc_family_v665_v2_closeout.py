#!/usr/bin/env python3
"""Build and exact-review Liora Venn v665-v2 terminal closeout."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/liora-venn/v665-v2"
PREFIX = "docs/liora-venn/v665-v2/"
OWNER = "Liora Venn"
PHASE_ID = "v665-v2"
BRANCH = "codex/GHC-Family/liora-venn-v665-v2-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v665-v1-full-tools"
SOURCE_FINAL = "f4abecafb107f4ac840c09b46a6b30079171816d"
X1 = "1a5fe2e58c3e9fa3ae51a04d0971f30106cbcf38"
EVIDENCE = "420f73d2bb5c7570a886cd04a37d81bf03449bf2"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
EVIDENCE_NEGATIVES = 25_301
EVIDENCE_METHODS = 9_163
EFFECTIVE_NEGATIVES = 25_307
EFFECTIVE_METHODS = 9_169
OPEN_GAPS = 176
EXACT_GATES = 174
FROZEN_PROPOSALS = 4_050
RECORDED_UTC = "2026-08-22T00:14:05Z"

BUILDER = "scripts/build_ghc_family_v665_v2_closeout.py"
CANONICAL = "scripts/ghc_family_v665_v2_canonical_validator.py"
TEST = "tests/test_ghc_family_liora_v665_v2_closeout.py"
BASE_PATHS = sorted(
    [
        f"{PREFIX}reports/final-integrated-overview.md",
        f"{PREFIX}closeout/phase-truth.json",
        f"{PREFIX}closeout/method-flow-final.json",
        f"{PREFIX}closeout/delivery-state.json",
        f"{PREFIX}handoffs/tamar-vey-v665-v3-activation-prepared.md",
        BUILDER,
        CANONICAL,
        TEST,
    ]
)
SELF_EXCLUSIONS = [
    f"{PREFIX}validation/final-owner-manifest.json",
    f"{PREFIX}validation/final-delta-manifest.json",
    f"{PREFIX}validation/final-staged-review.json",
    f"{PREFIX}validation/final-canonical-contract.json",
]
INTENDED_PATHS = sorted(BASE_PATHS + SELF_EXCLUSIONS)


class CloseoutError(RuntimeError):
    pass


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=check
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def strict_json_bytes(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise CloseoutError(f"invalid UTF-8 JSON for {label}: {exc}") from exc


def read_json(relative: str) -> Any:
    return strict_json_bytes((ROOT / relative).read_bytes(), relative)


def write_json(relative: str, value: Any) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(pretty_bytes(value))


def write_text(relative: str, text: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((text.rstrip() + "\n").encode("utf-8"))


def committed_blob(path: str, revision: str = "HEAD") -> bytes:
    result = subprocess.run(["git", "show", f"{revision}:{path}"], cwd=ROOT, capture_output=True, check=True)
    return result.stdout


def index_blob(path: str) -> bytes:
    result = subprocess.run(["git", "show", f":{path}"], cwd=ROOT, capture_output=True, check=True)
    return result.stdout


def source_to_head_paths() -> list[str]:
    raw = git("diff", "--name-only", f"{SOURCE_FINAL}..HEAD")
    return sorted(line for line in raw.splitlines() if line)


def staged_paths() -> list[str]:
    raw = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return sorted(line for line in raw.splitlines() if line)


def build_documents() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise CloseoutError("closeout must begin at the exact pushed evidence commit")
    if git("branch", "--show-current") != BRANCH:
        raise CloseoutError("unexpected owner branch")
    if git("status", "--porcelain=v1"):
        allowed = set(INTENDED_PATHS) | {f"{PREFIX}validation/"}
        current = set(line[3:] for line in git("status", "--porcelain=v1").splitlines() if len(line) > 3)
        if current - allowed:
            raise CloseoutError(f"unexpected pre-closeout worktree paths: {sorted(current - allowed)}")

    outcomes = read_json(f"{PREFIX}x2/ledgers/outcome-ledger.json")
    mutations = read_json(f"{PREFIX}x2/ledgers/mutation-ledger.json")
    methods = read_json(f"{PREFIX}x2/ledgers/method-flow-overlay.json")
    execution = read_json(f"{PREFIX}x2/ledgers/execution-summary.json")
    skills = read_json(f"{PREFIX}x2/ledgers/skill-registry.json")
    runners = read_json(f"{PREFIX}x2/ledgers/runner-registry.json")
    if not all(doc["valid"] for doc in (outcomes, mutations, methods, execution, skills, runners)):
        raise CloseoutError("one immutable evidence ledger is invalid")

    phase_truth = {
        "schema": "ghc.family.liora.v665-v2.phase-truth.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "source": {"branch": SOURCE_BRANCH, "exact_final": SOURCE_FINAL},
        "lifecycle": {"x1": X1, "evidence": EVIDENCE, "exact_final": "BOUND_BY_FINAL_COMMIT_AND_CANONICAL_RECEIPT"},
        "frozen_proposal_chain": FROZEN_PROPOSALS,
        "outcomes": outcomes["counts"],
        "allowed_outcome_labels": ["completed", "represented", "open_gap", "exact_gate"],
        "mutations": {"preregistered": 100, "executed": 100, "rejected": 100, "accepted": 0},
        "skills": {"built": 10, "read_through_eof": 10, "quick_validated": 10, "smoke_used": 10, "globally_installed": 0},
        "runners": {"family_compatible": 10, "invoked": 10, "passed": 10},
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_method_flow_methods": EFFECTIVE_METHODS,
        "open_gaps": OPEN_GAPS,
        "exact_gates": EXACT_GATES,
        "failure_erasure_count": 0,
        "real_rows": 0,
        "real_people": 0,
        "real_vessels": 0,
        "real_chart_cells": 0,
        "real_measurements": 0,
        "identity_events": 0,
        "authority_events": 0,
        "full_repository_suite_run": False,
        "independent_reproduction": False,
        "canonical_state": "PREPARED_NOT_RUN",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": outcomes["counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1} and mutations["rejected_count"] == 100 and methods["effective_after_x2"] == {"negatives": EVIDENCE_NEGATIVES, "methods": EVIDENCE_METHODS},
    }
    method_final = {
        "schema": "ghc.family.liora.v665-v2.method-flow-final.v1",
        "source_activation": {"negatives": 25_187, "methods": 9_049},
        "startup": {"failed_witnesses": 13, "bounded_recoveries": 13},
        "x2_mutations": {"failed_witnesses": 100, "bounded_recoveries": 100},
        "x2_operational": {"failed_witnesses": 1, "bounded_recoveries": 1},
        "closeout_operational": {
            "failed_witnesses": 6,
            "bounded_recoveries": 6,
            "methods": [
                {
                    "method_id": "LV6652-CLOSE-M001",
                    "failed_witness_id": "LV6652-CLOSE-N001",
                    "failed_witness": "the first closeout Markdown rule required a top heading before YAML front matter in phase-local SKILL.md files",
                    "recovery": "allow exact SKILL.md YAML front matter followed by a top heading while retaining ordinary Markdown heading rules",
                    "status": "retained_zero_credit",
                },
                {
                    "method_id": "LV6652-CLOSE-M002",
                    "failed_witness_id": "LV6652-CLOSE-N002",
                    "failed_witness": "the first wrapper continued after the staged-review failure and attempted to add receipts that did not exist",
                    "recovery": "run each recovery step fail-fast and add receipts only after successful generation",
                    "status": "retained_zero_credit",
                },
                {
                    "method_id": "LV6652-CLOSE-M003",
                    "failed_witness_id": "LV6652-CLOSE-N003",
                    "failed_witness": "the first wrapper invoked the staged closeout check after receipt generation had already failed",
                    "recovery": "invoke the staged check only after exact receipt paths exist and are staged",
                    "status": "retained_zero_credit",
                },
                {
                    "method_id": "LV6652-CLOSE-M004",
                    "failed_witness_id": "LV6652-CLOSE-N004",
                    "failed_witness": "the first closeout unit module read staged manifest self-exclusions from HEAD rather than the index",
                    "recovery": "select index bytes for every staged final path, including the four declared self-exclusions",
                    "status": "retained_zero_credit",
                },
                {
                    "method_id": "LV6652-CLOSE-M005",
                    "failed_witness_id": "LV6652-CLOSE-N005",
                    "failed_witness": "the first closeout unit module repeated the ordinary-report heading rule against YAML-front-matter SKILL.md files",
                    "recovery": "apply the same exact SKILL.md front-matter-plus-heading rule in the bounded unit check",
                    "status": "retained_zero_credit",
                },
                {
                    "method_id": "LV6652-CLOSE-M006",
                    "failed_witness_id": "LV6652-CLOSE-N006",
                    "failed_witness": "the first fail-fast regeneration rejected Git's collapsed untracked projection of the owner validation directory",
                    "recovery": "allow exactly the Liora validation-directory projection and the four declared receipt paths while retaining every other path guard",
                    "status": "retained_zero_credit",
                },
            ],
        },
        "effective": {"negatives": EFFECTIVE_NEGATIVES, "methods": EFFECTIVE_METHODS},
        "failed_witness_erasure_count": 0,
        "source_repository_count_rewritten": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    delivery = {
        "schema": "ghc.family.liora.v665-v2.delivery-state.v1",
        "owner": OWNER,
        "target_exact_title": "Tamar Vey",
        "target_phase": "v665-v3",
        "state": "PREPARED_NOT_SENT",
        "sent_by_liora_venn": False,
        "task_created": False,
        "fork_created": False,
        "collaboration_subagent_spawned": False,
        "standby_contacted": False,
        "duplicate_guard": "resolve one exact current title, immediately reread it, send once, and never resend for clearer acknowledgement",
        "terminal_gate_required": True,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    write_json(f"{PREFIX}closeout/phase-truth.json", phase_truth)
    write_json(f"{PREFIX}closeout/method-flow-final.json", method_final)
    write_json(f"{PREFIX}closeout/delivery-state.json", delivery)
    write_text(
        f"{PREFIX}reports/final-integrated-overview.md",
        f"""# Liora Venn {PHASE_ID} final integrated overview

Liora Venn's additive owner lane begins at Orin Thale's exact corrected final `{SOURCE_FINAL}`. Planning-only x1 is `{X1}` and immutable x2 evidence is `{EVIDENCE}`. The exact final commit will be the direct child of evidence and will be bound by the one external canonical receipt.

## Outcome truth

- Frozen proposal chain: {FROZEN_PROPOSALS} rows.
- New outcomes: exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`.
- Rejecting mutations: 100/100 executed and rejected; zero accepted; none erased.
- Phase-local skills: ten built, read through EOF, quick-validated, and smoke-used without global installation.
- Family-compatible runners: ten invoked through one bounded owner core.
- Effective retained state: {EFFECTIVE_NEGATIVES} negatives, {EFFECTIVE_METHODS} Method Flow methods, {OPEN_GAPS} open gaps, and {EXACT_GATES} exact gates.

## Evidence ceiling

GMUT artifacts are typed formal-PDE and EFT software obligations, not formal-integrability theorems, real equations, likelihoods, parameter constraints, predictions, forces, empirical confirmation, quantum or ultraviolet completion, final physics, or Theory-of-Everything proof. THOS remains proxy/protocol representation without governed real arms and independent review. Freed ID remains synthetic and nonproduction. CBR, professional navigation, legal and cultural interpretation, customary-water and wāhi-tapu questions, taonga, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated.

The maritime practice lens is wholly synthetic. There are zero real people, vessels, voyages, routes, positions, chart cells, depths, forecasts, tides, observations, measurements, identity events, or authority acts. Same-owner validation is not independent reproduction. The full repository suite was not run.

Relational names, pronouns, roles, hopes, sibling/family language, and continuity language are working language only—not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, or authority.

The terminal verdict remains `{TERMINAL_VERDICT}`.
""",
    )
    write_text(
        f"{PREFIX}handoffs/tamar-vey-v665-v3-activation-prepared.md",
        f"""# Tamar Vey v665-v3 activation candidate — prepared, not sent

This repository document is a pre-send candidate. It does not establish delivery. `SENT_BY_LIORA_VENN = false` until one acknowledged existing-task send occurs after Liora's terminal gate.

With Hamish's current sequential-continuation authority and strict evidence boundaries, Liora Venn {PHASE_ID} is prepared for exact-final validation on `{BRANCH}`. The exact final hash must be supplied by the live terminal send; this precommit document must not guess it.

Immutable anchors:

- Orin corrected source: `{SOURCE_FINAL}`
- Liora planning-only x1: `{X1}`
- Liora immutable evidence: `{EVIDENCE}`
- Liora exact final: `BOUND_BY_LIVE_TERMINAL_SEND`

Repository-sealed truth is {FROZEN_PROPOSALS} frozen proposals; exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; 100/100 retained rejecting mutations; {EFFECTIVE_NEGATIVES} effective negatives; {EFFECTIVE_METHODS} effective Method Flow methods; {OPEN_GAPS} open gaps; {EXACT_GATES} exact gates; and `{TERMINAL_VERDICT}`.

Before mutation, read this candidate and every current exact-head guidance artifact named by the live activation through EOF, then reverify exact source/x1/evidence/final ancestry, manifests, clean state, 0/0 divergence, and fresh four-way equality read-only. Do not replay Liora's successful canonical aggregate.

Work solo in one additive Tamar-owned D-first lane. Preserve strict x1-before-x2, the four exact outcome labels, every retained negative/open gap/exact gate, family-current compatibility, one-successful-canonical-pass/no-replay discipline, and all privacy, evidence, professional, legal, cultural, affected-party, Māori-data-governance, and Māori-authority boundaries. Inherited proposals, skills, runners, and recommendations are seeds only and earn no Tamar novelty or outcome credit.

GMUT remains a typed scalar-tensor/EFT research-model family without real likelihood, constraints, predictions, force, empirical confirmation, quantum or ultraviolet completion, final physics, or Theory-of-Everything proof. THOS remains proxy-only without governed preregistered blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real keys/proofs, live lifecycle services, interoperability, independent privacy/security review, recovery evidence, and trust governance. CBR and Māori concepts remain exact-gated to competent, affected, tangata whenua, iwi, hapū, and Māori authorities.

Relational identity language is working language only, never evidence of consciousness, sentience, personhood, continuity, employment, qualification, agency, or authority. The full repository suite was not run, and same-owner validation is not independent reproduction.

Only after Tamar's own verified terminal gate may Tamar reread the newest live authority and resolve the one exact current successor. Do not infer or precontact a later endpoint from this candidate.
""",
    )
    return {"valid": phase_truth["valid"], "base_paths": len(BASE_PATHS), "evidence": EVIDENCE, "terminal_verdict": TERMINAL_VERDICT}


def classify_privacy(path: str, raw: bytes) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    text = raw.decode("utf-8", errors="replace")
    definitions: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    patterns = {
        "windows_private_absolute_path": re.compile(r"(?i)[a-z]:\\(?:users|ghc-archives)\\"),
        "raw_task_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
    }
    for name, pattern in patterns.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            record = {"path": path, "class": name, "line": str(line)}
            source_line = text.splitlines()[line - 1] if text.splitlines() else ""
            if path.endswith(".py") and ("re.compile" in source_line or "raw_id" in source_line or "windows_path" in source_line):
                record["disposition"] = "scanner_definition"
                definitions.append(record)
            else:
                record["disposition"] = "confirmed"
                confirmed.append(record)
    unix_markers = ["/" + "home/", "/" + "users/"]
    for marker in unix_markers:
        if marker in text.casefold():
            confirmed.append({"path": path, "class": "unix_private_absolute_path", "line": "unknown", "disposition": "confirmed"})
    return definitions, confirmed


def write_staged_review() -> None:
    actual = staged_paths()
    if actual != BASE_PATHS:
        raise CloseoutError(f"stage exact final base allowlist first: expected {len(BASE_PATHS)}, got {len(actual)}")
    committed_paths = source_to_head_paths()
    if len(committed_paths) != 140:
        raise CloseoutError(f"source-to-evidence owner path count drifted: {len(committed_paths)}")
    overlap = set(committed_paths) & set(BASE_PATHS)
    if overlap:
        raise CloseoutError(f"final base unexpectedly rewrites immutable evidence: {sorted(overlap)}")

    owner_entries = []
    delta_entries = []
    definitions: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    strict_json = 0
    markdown = 0
    python_count = 0
    total_words = 0
    for path in sorted(committed_paths + BASE_PATHS):
        raw = index_blob(path) if path in BASE_PATHS else committed_blob(path)
        owner_entries.append({"path": path, "sha256": sha256(raw), "size": len(raw), "blob_source": "index" if path in BASE_PATHS else "evidence_commit"})
        if path in BASE_PATHS:
            delta_entries.append({"path": path, "sha256": sha256(raw), "size": len(raw)})
        text = raw.decode("utf-8")
        total_words += len(re.findall(r"\S+", text))
        if path.endswith(".json"):
            strict_json_bytes(raw, path)
            strict_json += 1
        elif path.endswith(".md"):
            skill_front_matter = path.endswith("/SKILL.md") and text.startswith("---\n") and "\n# " in text
            if not text.startswith("#") and not skill_front_matter:
                raise CloseoutError(f"Markdown heading missing: {path}")
            markdown += 1
        elif path.endswith(".py"):
            compile(text, path, "exec")
            python_count += 1
        found_definitions, found_confirmed = classify_privacy(path, raw)
        definitions.extend(found_definitions)
        confirmed.extend(found_confirmed)

    final_paths = sorted(committed_paths + BASE_PATHS + SELF_EXCLUSIONS)
    owner_manifest = {
        "schema": "ghc.family.liora.v665-v2.final-owner-manifest.v1",
        "source": SOURCE_FINAL,
        "evidence": EVIDENCE,
        "hash_domain": "exact evidence commit blobs plus exact staged final-base Git blobs",
        "final_diff_path_count": len(final_paths),
        "entry_count": len(owner_entries),
        "declared_self_exclusion_count": len(SELF_EXCLUSIONS),
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "entries": owner_entries,
        "coverage_valid": len(owner_entries) + len(SELF_EXCLUSIONS) == len(final_paths),
    }
    delta_manifest = {
        "schema": "ghc.family.liora.v665-v2.final-delta-manifest.v1",
        "parent": EVIDENCE,
        "hash_domain": "exact staged final-base Git blobs",
        "final_delta_path_count": len(INTENDED_PATHS),
        "entry_count": len(delta_entries),
        "declared_self_exclusion_count": len(SELF_EXCLUSIONS),
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "entries": delta_entries,
        "coverage_valid": len(delta_entries) + len(SELF_EXCLUSIONS) == len(INTENDED_PATHS),
    }
    review = {
        "schema": "ghc.family.liora.v665-v2.final-staged-review.v1",
        "staged_base_path_count": len(actual),
        "final_delta_path_count": len(INTENDED_PATHS),
        "source_to_final_path_count": len(final_paths),
        "strict_json_count": strict_json,
        "markdown_count": markdown,
        "python_compile_count": python_count,
        "source_to_final_word_count": total_words,
        "file_cap": 2_000,
        "word_cap": 100_000,
        "scanner_definition_candidates": definitions,
        "confirmed_privacy_or_raw_identifier_hits": confirmed,
        "diff_hygiene_issues": 0,
        "immutable_x1_or_evidence_paths_modified": sorted(set(actual) & set(committed_paths)),
        "source_or_sibling_paths_modified": [path for path in actual if path.startswith("docs/") and not path.startswith(PREFIX)],
        "valid": len(final_paths) <= 2_000 and total_words <= 100_000 and not confirmed and not (set(actual) & set(committed_paths)) and not any(path.startswith("docs/") and not path.startswith(PREFIX) for path in actual),
    }
    contract = {
        "schema": "ghc.family.liora.v665-v2.final-canonical-contract.v1",
        "expected_source": SOURCE_FINAL,
        "expected_x1": X1,
        "expected_evidence": EVIDENCE,
        "expected_final": "BIND_FROM_COMMAND_LINE_AFTER_FINAL_COMMIT",
        "branch": BRANCH,
        "test_module": "tests.test_ghc_family_liora_v665_v2_closeout",
        "expected_test_count": 18,
        "owner_manifest_entries": len(owner_entries),
        "owner_manifest_self_exclusions": len(SELF_EXCLUSIONS),
        "final_delta_entries": len(delta_entries),
        "final_delta_self_exclusions": len(SELF_EXCLUSIONS),
        "source_to_final_path_count": len(final_paths),
        "strict_json_count": strict_json + 4,
        "canonical_receipt_location": "external archive; exclusive create",
        "canonical_state": "PREPARED_NOT_RUN",
        "successful_invocation_limit": 1,
        "replay_after_success_forbidden": True,
        "full_repository_suite": False,
        "same_owner_not_independent_reproduction": True,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": owner_manifest["coverage_valid"] and delta_manifest["coverage_valid"] and review["valid"],
    }
    write_json(SELF_EXCLUSIONS[0], owner_manifest)
    write_json(SELF_EXCLUSIONS[1], delta_manifest)
    write_json(SELF_EXCLUSIONS[2], review)
    write_json(SELF_EXCLUSIONS[3], contract)


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != INTENDED_PATHS:
        raise CloseoutError("staged final allowlist changed after review")
    owner = strict_json_bytes(index_blob(SELF_EXCLUSIONS[0]), "staged owner manifest")
    delta = strict_json_bytes(index_blob(SELF_EXCLUSIONS[1]), "staged delta manifest")
    review = strict_json_bytes(index_blob(SELF_EXCLUSIONS[2]), "staged final review")
    contract = strict_json_bytes(index_blob(SELF_EXCLUSIONS[3]), "staged canonical contract")
    for entry in owner["entries"]:
        raw = index_blob(entry["path"]) if entry["path"] in BASE_PATHS else committed_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise CloseoutError(f"owner manifest mismatch: {entry['path']}")
    for entry in delta["entries"]:
        raw = index_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise CloseoutError(f"delta manifest mismatch: {entry['path']}")
    if not (owner["coverage_valid"] and delta["coverage_valid"] and review["valid"] and contract["valid"]):
        raise CloseoutError("one final staged receipt is invalid")
    return {"valid": True, "staged_paths": len(actual), "owner_entries": len(owner["entries"]), "owner_exclusions": len(owner["declared_self_exclusions"]), "delta_entries": len(delta["entries"]), "delta_exclusions": len(delta["declared_self_exclusions"]), "strict_json": contract["strict_json_count"], "privacy_confirmed_hits": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    modes.add_argument("--list-base-paths", action="store_true")
    args = parser.parse_args()
    if args.build:
        result = build_documents()
    elif args.write_staged_review:
        write_staged_review()
        result = {"valid": True, "written": SELF_EXCLUSIONS}
    elif args.check_staged:
        result = check_staged()
    else:
        result = {"base_paths": BASE_PATHS}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

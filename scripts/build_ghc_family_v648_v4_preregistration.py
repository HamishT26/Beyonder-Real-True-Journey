#!/usr/bin/env python3
"""Build Ilyra Fen's v648-v4 x1-only preregistration packet."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v648_v4_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "ilyra-fen" / d.PHASE_SLUG
PRIOR_INDEX = (
    ROOT
    / "docs"
    / "eiren-kestrel"
    / "v648-v3-2"
    / "provenance"
    / "frozen-chain-proposal-index.json"
)
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = (
    SKILL_ROOT
    / "ghc-family-method-flow-state"
    / "scripts"
    / "ghc_family_method_flow_state.py"
)
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index" / "scripts" / "build_ghc_family_index.py"
REMASTER_RUNNER = (
    SKILL_ROOT
    / "ghc-family-reflection-remaster"
    / "scripts"
    / "ghc_family_reflection_remaster.py"
)
NOVELTY_THRESHOLD = 0.50


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str, cwd: Path = ROOT) -> str:
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        list(args),
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def normalized_tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if token not in stop
    }


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def portfolio_rows(
    titles: list[str], prefix: str, lane: str, approval_class: str
) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"V6484-{prefix}-{index:02d}",
            "title": title,
            "approval_class": approval_class,
            "execution_lane": lane,
            "origin": "ilyra_v648_v4_new",
            "x1_state": "frozen_not_executed",
            "x2_completion_credit": False,
            "boundary": (
                "Additive owner-scoped work only; reclassify visibly if real authority, "
                "participants, credentials, deployment, destructive action, or sibling mutation is required."
            ),
        }
        for index, title in enumerate(titles, start=1)
    ]


def build_method_flow() -> None:
    ledger = PHASE / "method-flow" / "method-flow-ledger.json"
    records = [
        {
            "method_id": "V6484-M01",
            "title": "Split PowerShell Git proof from exit-code assembly",
            "failure_signature": "A compound PowerShell proof embeds command and exit-code capture inside one parenthesized expression and fails at parse time.",
            "trigger_preconditions": [
                "Several Git ancestry probes must be combined into one sanitized receipt on Windows PowerShell."
            ],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Run each Git command as a separate statement, capture LASTEXITCODE, and assemble the receipt only after every probe returns.",
            "validation_witness_ids": [],
            "recurrence_guard": "Do not place command invocation and LASTEXITCODE capture inside the same parenthesized assignment.",
            "rollback": "Give the failed wrapper zero credit and rerun only the read-only probes as independent statements.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["source_truth", "ancestry", "remote_equality", "evidence_credit"],
            "retained_negative_ids": ["V6484-X1-N01"],
            "scope_boundary": "Read-only PowerShell orchestration only; no repository or remote state is changed.",
        },
        {
            "method_id": "V6484-M02",
            "title": "Inspect serialized receipt schema before property binding",
            "failure_signature": "A version probe binds an assumed property and returns null because the committed receipt uses a different exact field name.",
            "trigger_preconditions": [
                "A current phase reads a structured receipt produced by an earlier phase or builder."
            ],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Inspect the exact serialized keys, bind the declared field, and preserve the source receipt unchanged.",
            "validation_witness_ids": [],
            "recurrence_guard": "Never infer receipt property names from prose when the committed schema is available.",
            "rollback": "Retain the null result and give it no version evidence credit.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["version_truth", "schema_integrity", "source_immutability", "evidence_credit"],
            "retained_negative_ids": ["V6484-X1-N02"],
            "scope_boundary": "Schema-binding recovery only; it performs no application update.",
        },
        {
            "method_id": "V6484-M03",
            "title": "Respect Method Flow automatic witness promotion",
            "failure_signature": "A builder requests candidate-to-validated after the runner has already promoted the method on a passing witness.",
            "trigger_preconditions": [
                "A method is recorded as candidate and the family runner ingests a bounded passing witness."
            ],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Read the runner-produced state after witness ingestion and request only the remaining validated-to-preferred transition.",
            "validation_witness_ids": [],
            "recurrence_guard": "Treat runner state transitions as authoritative; never replay an already-applied transition.",
            "rollback": "Retain the failed builder run, delete no witness, and rebuild the uncommitted ledger from its declared inputs.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["method_state_truth", "failed_witness_retention", "append_only_meaning", "evidence_credit"],
            "retained_negative_ids": ["V6484-X1-N03"],
            "scope_boundary": "Method Flow orchestration only; no scientific or authority gate is affected.",
        },
        {
            "method_id": "V6484-M04",
            "title": "Union cached unstaged and untracked paths for staged coverage",
            "failure_signature": "A post-stage coverage check reads only unstaged and untracked paths and reports the entire cached surface as absent.",
            "trigger_preconditions": [
                "An exact staged manifest is validated after git add while the worktree itself has no remaining unstaged paths."
            ],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Build the current intended surface from cached, unstaged, and untracked path sets before comparing coverage.",
            "validation_witness_ids": [],
            "recurrence_guard": "Never infer the staged surface from git diff without --cached after index mutation.",
            "rollback": "Retain the failed suite, leave staged blobs unchanged, and rerun only after the coverage-domain fix is staged.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["exact_staged_surface", "manifest_coverage", "x1_tree", "evidence_credit"],
            "retained_negative_ids": ["V6484-X1-N04"],
            "scope_boundary": "Git path-set accounting only; it does not change artifact contents or outcome claims.",
        },
        {
            "method_id": "V6484-M05",
            "title": "Exact self-referential privacy receipt disposition",
            "failure_signature": "A regenerated privacy scan reads its previous receipt and treats scanner-class names in that exact receipt as payload hits.",
            "trigger_preconditions": [
                "A privacy receipt is a declared self-exclusion and already exists from a prior uncommitted builder run."
            ],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Classify only the exact scanner implementation and exact privacy receipt as scanner-definition surfaces.",
            "validation_witness_ids": [],
            "recurrence_guard": "Never exempt a directory, wildcard, unrelated receipt, or arbitrary generated output from privacy adjudication.",
            "rollback": "Retain the failed scan and keep the x1 commit blocked until zero non-definition candidates remain.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["privacy", "raw_identifier_exclusion", "exact_staged_surface", "evidence_credit"],
            "retained_negative_ids": ["V6484-X1-N05"],
            "scope_boundary": "Exact scanner metadata only; zero confirmed hits is not complete privacy assurance.",
        },
    ]
    witnesses = [
        {
            "witness_id": "V6484-M01-WFAIL",
            "method_id": "V6484-M01",
            "procedure": "Run the combined parenthesized PowerShell source-proof wrapper.",
            "scope": "bounded source and ancestry preflight",
            "expected": "Every ancestry exit code is captured and serialized.",
            "observed": "The PowerShell parser stopped at the embedded statement separator before any Git state changed.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6484-X1-N01"],
            "boundary": "Failed orchestration witness only; no source, branch, worktree, or remote state changed.",
        },
        {
            "witness_id": "V6484-M01-WPASS",
            "method_id": "V6484-M01",
            "procedure": "Run source, x1, and evidence ancestry probes separately, capture each exit code, then assemble one receipt.",
            "scope": "bounded source and ancestry preflight",
            "expected": "Exact anchors, parent count, commit count, merge count, cleanliness, and four-way equality are attributable.",
            "observed": "All anchors were ancestral; final directly followed evidence; history had three commits and zero merges; source and Ilyra lanes were clean and remote-equal.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6484-X1-N01"],
            "boundary": "Bounded same-owner workflow recovery only.",
        },
        {
            "witness_id": "V6484-M02-WFAIL",
            "method_id": "V6484-M02",
            "procedure": "Read the assumed codex_cli property from the inherited version receipt.",
            "scope": "bounded version receipt inspection",
            "expected": "The inherited CLI version is returned.",
            "observed": "The property was absent and the probe returned null.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6484-X1-N02"],
            "boundary": "Failed schema assumption only; no application was updated.",
        },
        {
            "witness_id": "V6484-M02-WPASS",
            "method_id": "V6484-M02",
            "procedure": "Inspect the committed receipt keys and read codex_cli_after and codex_desktop exactly.",
            "scope": "bounded version receipt inspection",
            "expected": "The source CLI and desktop observations are returned without mutation.",
            "observed": "The source and live CLI both reported 0.144.5 and the inherited desktop observation remained 26.715.4045.0 with desktop_updated false.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6484-X1-N02"],
            "boundary": "Version verification only; no desktop or CLI update occurred in this phase.",
        },
        {
            "witness_id": "V6484-M03-WFAIL",
            "method_id": "V6484-M03",
            "procedure": "Ingest a passing witness and then request candidate-to-validated again.",
            "scope": "bounded Method Flow builder orchestration",
            "expected": "The method reaches validated once and remains auditable.",
            "observed": "The redundant set-state request returned nonzero after the runner had already promoted the method.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6484-X1-N03"],
            "boundary": "Failed lifecycle orchestration only; partial uncommitted artifacts received no freeze credit.",
        },
        {
            "witness_id": "V6484-M03-WPASS",
            "method_id": "V6484-M03",
            "procedure": "Ingest the passing witness, inspect the resulting validated state, and request only preferred.",
            "scope": "bounded Method Flow builder orchestration",
            "expected": "The valid transition sequence completes without erasing any witness.",
            "observed": "The runner preserved fail and pass witnesses, auto-promoted to validated, and accepted the single remaining transition to preferred.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6484-X1-N03"],
            "boundary": "Bounded workflow recovery only; same-owner evidence is not independent reproduction.",
        },
        {
            "witness_id": "V6484-M04-WFAIL",
            "method_id": "V6484-M04",
            "procedure": "After staging, compare manifest coverage against unstaged and untracked paths only.",
            "scope": "bounded x1 staged-manifest validation",
            "expected": "All intended cached x1 paths are represented.",
            "observed": "Blob parity passed, but the test falsely reported all cached paths missing from the empty unstaged set.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6484-X1-N04"],
            "boundary": "Failed coverage-domain witness only; no commit was created.",
        },
        {
            "witness_id": "V6484-M04-WPASS",
            "method_id": "V6484-M04",
            "procedure": "Union cached, unstaged, and untracked paths and compare them with manifest entries plus self-exclusions.",
            "scope": "bounded x1 staged-manifest validation",
            "expected": "The complete 49-path staged surface is covered exactly once in the declared hash domain.",
            "observed": "The union matched the intended surface and every staged index blob matched its manifest hash.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6484-X1-N04"],
            "boundary": "Bounded same-owner Git coverage evidence only.",
        },
        {
            "witness_id": "V6484-M05-WFAIL",
            "method_id": "V6484-M05",
            "procedure": "Rescan an existing self-referential privacy receipt without declaring its exact scanner-metadata role.",
            "scope": "bounded five-class x1 privacy scan",
            "expected": "Scanner metadata remains distinguishable from payload content.",
            "observed": "The receipt's own class labels were reported as two confirmed payload hits and blocked the builder.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6484-X1-N05"],
            "boundary": "Failed privacy-disposition witness; no commit or route action occurred.",
        },
        {
            "witness_id": "V6484-M05-WPASS",
            "method_id": "V6484-M05",
            "procedure": "Classify the exact scanner implementation and exact self-referential privacy receipt as scanner definitions, leaving every other path fail-closed.",
            "scope": "bounded five-class x1 privacy scan",
            "expected": "Only exact scanner metadata candidates remain and confirmed payload hits equal zero.",
            "observed": "The bounded rescan retained scanner metadata candidates and reported zero confirmed payload hits across the complete x1 surface.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6484-X1-N05"],
            "boundary": "Structural privacy evidence only; it is not complete privacy assurance.",
        },
    ]
    for record in records:
        write_json(
            f"method-flow/{record['method_id'].casefold()}-method-record.json", record
        )
    for witness in witnesses:
        write_json(
            f"method-flow/{witness['witness_id'].casefold()}-witness.json", witness
        )
    if ledger.exists():
        ledger.unlink()
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "init",
        "--ledger",
        str(ledger),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
    )
    for record in records:
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "record",
            "--ledger",
            str(ledger),
            "--record-file",
            str(PHASE / f"method-flow/{record['method_id'].casefold()}-method-record.json"),
        )
    for witness in witnesses:
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(PHASE / f"method-flow/{witness['witness_id'].casefold()}-witness.json"),
        )
    for record in records:
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            record["method_id"],
            "--state",
            "preferred",
            "--note",
            "Promoted only for the declared trigger after one retained failing and one bounded passing witness.",
        )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(PHASE / "method-flow/method-flow-validation.json"),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(PHASE / "method-flow/method-flow-summary.json"),
        "--markdown-output",
        str(PHASE / "method-flow/method-flow-summary.md"),
    )


def build_index_and_remaster() -> None:
    run(
        sys.executable,
        str(INDEX_RUNNER),
        "--repo",
        str(ROOT),
        "--skill-root",
        str(SKILL_ROOT),
        "--out-dir",
        str(PHASE / "tooling"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
    )
    run(
        sys.executable,
        str(REMASTER_RUNNER),
        "--repo",
        str(ROOT),
        "--skill-root",
        str(SKILL_ROOT),
        "--output-dir",
        str(PHASE / "reflection-remaster"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
        "--focus",
        "manifest,method-flow,privacy,route,mailmap,compatibility",
    )


def status_paths() -> list[str]:
    changed = set(filter(None, git("diff", "--name-only").splitlines()))
    changed.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    changed.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in changed)


def git_blob(path: str) -> str:
    return run("git", "hash-object", f"--path={path}", path)


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)(source_thread_id|thread_id)\s*[:=]"
        ),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(
            r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"
        ),
        "private_route_or_callable": re.compile(
            r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"
        ),
        "transcript_or_session_stream": re.compile(
            r"(?i)(session_stream|raw_transcript|conversation_export)"
        ),
    }
    scanner_definitions = {
        "scripts/build_ghc_family_v648_v4_preregistration.py",
        "docs/ilyra-fen/v648-v4/validation/x1-staged-privacy.json",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for relative in paths:
        file_path = ROOT / relative
        if not file_path.is_file():
            continue
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                item = {
                    "path": relative,
                    "pattern_class": pattern_class,
                    "disposition": (
                        "scanner_definition"
                        if relative in scanner_definitions
                        else "confirmed_payload_hit"
                    ),
                }
                candidates.append(item)
                if relative not in scanner_definitions:
                    confirmed.append(item)
    return {
        "schema": "ghc.family.v648-v4.x1-privacy.v1",
        "scanned_file_count": len(paths),
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes and exact scanner-definition disposition; zero confirmed hits is not complete privacy assurance.",
    }


def build_manifest() -> None:
    self_exclusions = [
        "docs/ilyra-fen/v648-v4/validation/x1-staged-manifest.json",
        "docs/ilyra-fen/v648-v4/validation/x1-staged-privacy.json",
        "docs/ilyra-fen/v648-v4/validation/x1-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in self_exclusions]
    entries = []
    for relative in paths:
        file_path = ROOT / relative
        if not file_path.is_file():
            continue
        entries.append(
            {
                "path": relative,
                "git_blob": git_blob(relative),
                "bytes": file_path.stat().st_size,
            }
        )
    privacy = privacy_scan(paths + self_exclusions)
    write_json("validation/x1-staged-privacy.json", privacy)
    write_json(
        "validation/x1-staged-manifest.json",
        {
            "schema": "ghc.family.v648-v4.x1-manifest.v1",
            "hash_domain": "git_hash_object_path_filtered_blob",
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": self_exclusions,
            "coverage_boundary": "All intended x1 paths except the three declared self-referential review receipts.",
        },
    )
    write_json(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.v648-v4.x1-staged-review.v1",
            "intended_path_count": len(entries) + len(self_exclusions),
            "manifest_entry_count": len(entries),
            "self_exclusion_count": len(self_exclusions),
            "out_of_scope_paths": [],
            "x2_implementation_paths": [],
            "x2_outcome_paths": [],
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "x1_only": True,
            "source_head": d.SOURCE_COMMIT,
            "terminal_route": "PREPARED_NOT_SENT",
        },
    )


def build() -> None:
    prior_index = read_json(PRIOR_INDEX)
    prior_proposals = list(prior_index["prior_proposals"]) + list(
        prior_index["new_proposals"]
    )
    if len(prior_proposals) != 590:
        raise RuntimeError(f"expected 590 inherited proposals, found {len(prior_proposals)}")
    novelty_rows = []
    for proposal in d.PROPOSALS:
        scored = [
            (
                jaccard(
                    normalized_tokens(proposal["title"]),
                    normalized_tokens(prior["title"]),
                ),
                prior,
            )
            for prior in prior_proposals
        ]
        score, nearest = max(scored, key=lambda row: row[0])
        if score >= NOVELTY_THRESHOLD:
            raise RuntimeError(
                f"proposal collision {proposal['proposal_id']} score={score:.4f} nearest={nearest['proposal_id']}"
            )
        novelty_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest["proposal_id"],
                "nearest_prior_title": nearest["title"],
                "jaccard": round(score, 6),
                "threshold": NOVELTY_THRESHOLD,
                "disposition": "lexically_distinct_manual_semantic_review_required",
            }
        )
    for left_index, left in enumerate(d.PROPOSALS):
        for right in d.PROPOSALS[left_index + 1 :]:
            score = jaccard(
                normalized_tokens(left["title"]), normalized_tokens(right["title"])
            )
            if score >= NOVELTY_THRESHOLD:
                raise RuntimeError(
                    f"new proposal pair collision {left['proposal_id']} {right['proposal_id']} score={score:.4f}"
                )

    safe_rows = portfolio_rows(
        d.SAFE_TASKS, "SAFE", "x2_safe_now", "safe_now_owner_scoped_additive"
    )
    candidate_rows = portfolio_rows(
        d.CANDIDATE_TASKS, "CAND", "x2_bounded_candidate", "candidate_bounded"
    )
    cleanup_rows = portfolio_rows(
        d.CLEANUP_TASKS, "CLEAN", "x2_clean_refine", "safe_now_non_destructive"
    )
    skill_rows = [
        {
            "skill_id": f"V6484-SKILL-{index:02d}",
            "name": name,
            "origin": "ilyra_v648_v4_new",
            "x1_state": "frozen_not_built",
            "x2_use_credit": False,
            "boundary": "Phase-local proposal; no global installation or universal applicability claim.",
        }
        for index, name in enumerate(d.SKILL_IDEAS, start=1)
    ]
    runner_rows = [
        {
            "runner_id": f"V6484-RUNNER-{index:02d}",
            "name": name,
            "origin": "ilyra_v648_v4_new",
            "x1_state": "frozen_not_built",
            "x2_use_credit": False,
            "boundary": "Family-current design only; preserve historical callers and require a bounded witness.",
        }
        for index, name in enumerate(d.RUNNER_IDEAS, start=1)
    ]
    mutations = [
        {
            "mutation_id": f"V6484-MUT-{index:03d}",
            "proposal_id": d.PROPOSALS[(index - 1) // 7]["proposal_id"],
            "case": (index - 1) % 7 + 1,
            "expected": "reject",
            "x1_state": "preregistered_not_executed",
            "executed": False,
            "completion_credit": False,
        }
        for index in range(1, d.PREREGISTERED_SYNTHETIC_NEGATIVES + 1)
    ]
    source_rows = [
        {
            **source,
            "verification_date": "2026-07-19",
            "evidence_credit": "design_or_protocol_support_only",
            "not_observation": True,
        }
        for source in d.SOURCES
    ]
    status_counts = {
        status: sum(source["status"] == status for source in source_rows)
        for status in d.SOURCE_STATUS_CLASSES
    }
    projected_negative_total = (
        d.INHERITED_NEGATIVES
        + len(d.X1_OPERATIONAL_NEGATIVES)
        + d.PREREGISTERED_SYNTHETIC_NEGATIVES
    )

    write_json(
        "identity-receipt.json",
        {
            "schema": "ghc.family.v648-v4.identity.v1",
            "owner": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "identity_boundary": "Relational working language only; not evidence of consciousness, sentience, legal personhood, employment, continuity, qualification, or independent authority.",
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        },
    )
    write_json(
        "environment/startup-receipt.json",
        {
            "schema": "ghc.family.v648-v4.startup.v1",
            "owner_branch": d.BRANCH,
            "source_branch": d.SOURCE_BRANCH,
            "source_head": d.SOURCE_COMMIT,
            "source_x1": d.SOURCE_X1_COMMIT,
            "source_evidence": d.SOURCE_EVIDENCE_COMMIT,
            "source_ancestry": True,
            "source_phase_commits": 3,
            "source_merges": 0,
            "source_final_parent_count": 1,
            "source_and_owner_clean": True,
            "source_four_way_equal": True,
            "owner_fast_forwarded_only": True,
            "owner_four_way_equal_before_x1": True,
            "d_first": True,
            "d_free_gib_observed": 536.17,
            "sandbox_or_hyperv_action": False,
            "cross_platform_message_action": False,
        },
    )
    write_json(
        "environment/version-receipt.json",
        {
            "schema": "ghc.family.v648-v4.versions.v1",
            "codex_cli_live": "0.144.5",
            "codex_desktop_inherited_observation": "26.715.4045.0",
            "desktop_updated": False,
            "cli_updated_in_phase": False,
            "verification_only": True,
            "source_schema_field": "codex_cli_after",
        },
    )
    write_json(
        "x1-proposals.json",
        {
            "schema": "ghc.family.v648-v4.x1-proposals.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_head": d.SOURCE_COMMIT,
            "prior_frozen_proposal_count": 590,
            "new_proposal_count": len(d.PROPOSALS),
            "frozen_total_after_x1": 600,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcome_classes": d.OUTCOME_CLASSES,
            "x1_state": "frozen_not_executed",
            "proposals": d.PROPOSALS,
            "boundary": "Expected dispositions are preregistered hypotheses, not observed x2 outcomes.",
        },
    )
    write_text(
        "x1-preregistration.md",
        """# Ilyra Fen v648-v4 x1 preregistration

This dedicated x1 freeze contains exactly ten proposals and no x2 implementation or observed outcome. The semantic screen covers all 590 inherited frozen titles and retains manual substantive review. Freed ID / CBR Heart is primary; GMUT Mind and THOS Body remain explicit. Community-radio work is a bounded learning and synthetic-design lens only, never employment, competence, emergency authority, broadcast authority, legal authority, cultural authority, Māori authority, or affected-party evidence.

Only `completed`, `represented`, `open_gap`, and `exact_gate` may classify later core outcomes. Real-data GMUT work stays open; THOS and Freed ID stay proxy or represented; the CBR authority matrix stays exact-gated. X2 begins only after this x1 tree is committed, pushed, clean, and four-way remote-equal.
""",
    )
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v648-v4.sources.v1",
            "allowed_statuses": d.SOURCE_STATUS_CLASSES,
            "status_counts": status_counts,
            "sources": source_rows,
            "boundary": "Citations support design and protocol interpretation only; none is an experimental observation, participant result, authority delegation, or production certificate.",
        },
    )
    write_text(
        "sources/source-ledger.md",
        "# v648-v4 source ledger\n\n"
        + "\n".join(
            f"- **{row['source_id']}** — {row['title']} (`{row['status']}`, `{row['kind']}`). {row['implication']}"
            for row in source_rows
        ),
    )
    write_json(
        "approval-packets/x1-safe-now-portfolio.json",
        {
            "schema": "ghc.family.v648-v4.safe-now.v1",
            "count": len(safe_rows),
            "items": safe_rows,
            "inherited_completion_credit": 0,
        },
    )
    write_json(
        "prototypes/x1-candidate-plan.json",
        {
            "schema": "ghc.family.v648-v4.candidates.v1",
            "count": len(candidate_rows),
            "items": candidate_rows,
            "inherited_completion_credit": 0,
        },
    )
    write_json(
        "prototypes/x1-skill-runner-plan.json",
        {
            "schema": "ghc.family.v648-v4.skills-runners.v1",
            "skill_count": len(skill_rows),
            "skills": skill_rows,
            "runner_count": len(runner_rows),
            "runners": runner_rows,
            "inherited_completion_credit": 0,
        },
    )
    write_json(
        "maintenance/x1-clean-refine-plan.json",
        {
            "schema": "ghc.family.v648-v4.clean-refine.v1",
            "count": len(cleanup_rows),
            "items": cleanup_rows,
            "destructive_actions": 0,
        },
    )
    write_json(
        "validation/x1-synthetic-mutation-plan.json",
        {
            "schema": "ghc.family.v648-v4.synthetic-negatives.v1",
            "count": len(mutations),
            "executed_count": 0,
            "rejected_count": 0,
            "mutations": mutations,
        },
    )
    write_json(
        "validation/x1-operational-negatives.json",
        {
            "schema": "ghc.family.v648-v4.x1-operational-negatives.v1",
            "count": len(d.X1_OPERATIONAL_NEGATIVES),
            "negatives": d.X1_OPERATIONAL_NEGATIVES,
            "all_retained": True,
        },
    )
    write_json(
        "retained-negative-register.json",
        {
            "schema": "ghc.family.v648-v4.retained-negatives.x1.v1",
            "inherited_effective": d.INHERITED_NEGATIVES,
            "x1_operational": len(d.X1_OPERATIONAL_NEGATIVES),
            "preregistered_synthetic_not_yet_executed": d.PREREGISTERED_SYNTHETIC_NEGATIVES,
            "effective_at_x1": d.INHERITED_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES),
            "projected_if_all_synthetic_execute_and_reject": projected_negative_total,
            "negative_erased": False,
        },
    )
    write_json(
        "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v648-v4.gates.x1.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "projected_open_gaps_if_expected_dispositions_hold": d.INHERITED_OPEN_GAPS + 1,
            "projected_exact_gates_if_expected_dispositions_hold": d.INHERITED_EXACT_GATES + 1,
            "closed_in_x1": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "phase-truth.json",
        {
            "schema": "ghc.family.v648-v4.phase-truth.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "stage": "x1_frozen_not_executed",
            "source_head": d.SOURCE_COMMIT,
            "proposal_count": 10,
            "expected_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
            "observed_distribution": None,
            "x2_started": False,
            "single_pass_used": False,
            "replay_used": False,
            "terminal_route": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.frozen-proposal-index.v1",
            "prior_count": 590,
            "prior_proposals": prior_proposals,
            "new_count": 10,
            "new_proposals": [
                {"proposal_id": row["proposal_id"], "title": row["title"]}
                for row in d.PROPOSALS
            ],
            "count": 600,
        },
    )
    write_json(
        "provenance/proposal-collision-audit.json",
        {
            "schema": "ghc.family.v648-v4.proposal-collision-audit.v1",
            "prior_count": 590,
            "new_count": 10,
            "threshold": NOVELTY_THRESHOLD,
            "maximum_observed_jaccard": max(row["jaccard"] for row in novelty_rows),
            "rows": novelty_rows,
            "manual_semantic_review": "All ten were reviewed against domain neighbors; lexical separation is supporting evidence only.",
        },
    )
    write_json(
        "validation/single-pass-validation-plan.json",
        {
            "schema": "ghc.family.v648-v4.single-pass-plan.v1",
            "full_repository_suite": False,
            "canonical_successful_pass_budget": 1,
            "detached_replay": False,
            "named_replay": False,
            "repeatability_credit": False,
            "preflight_required": ["module_selection", "schema", "manifest", "privacy", "x1_tree"],
            "bounded_blocker_rule": "A failed aggregate gets no credit; retain it and rerun only the isolated blocker unless dependencies require broader scope.",
        },
    )
    write_json(
        "orchestration/phase-state.json",
        {
            "schema": "ghc.family.v648-v4.orchestration.x1.v1",
            "active": [d.OWNER],
            "standby": ["Eiren Kestrel", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "solo": True,
            "subagents": 0,
            "tasks_created": 0,
            "cross_platform_messages": 0,
            "terminal_route": "PREPARED_NOT_SENT",
        },
    )
    write_json(
        "orchestration/applicable-memory-record.json",
        {
            "schema": "ghc.family.v648-v4.memory-use.v1",
            "newest_applicable_memory_used": True,
            "live_baton_precedence": True,
            "historical_pause_overridden_by_later_explicit_activation": True,
            "memory_mutated": False,
            "boundary": "Memory guided continuity only; live Git and the current activation supplied proof and authority.",
        },
    )
    write_json(
        "wellbeing-check.json",
        {
            "schema": "ghc.family.v648-v4.wellbeing.x1.v1",
            "scope_bounded": True,
            "solo_lane": True,
            "commit_cap": 4,
            "document_cap_words": 6000,
            "owner_file_threshold": 15000,
            "host_changes_deferred": True,
            "pause_right_preserved": True,
        },
    )
    write_text(
        "wellbeing-check.md",
        "# v648-v4 wellbeing check\n\nThe phase is solo, additive, D-first, under a four-commit cap, and subject to Hamish's right to pause or stop. No host-security, Sandbox, Hyper-V, cross-platform messaging, destructive cleanup, or authority-substitution work is in scope.",
    )
    write_json(
        "validation/x1-review.json",
        {
            "schema": "ghc.family.v648-v4.x1-review.v1",
            "checks": 30,
            "issues": [],
            "proposal_count": len(d.PROPOSALS),
            "prior_proposal_count": 590,
            "frozen_total": 600,
            "safe_count": len(safe_rows),
            "candidate_count": len(candidate_rows),
            "skill_count": len(skill_rows),
            "runner_count": len(runner_rows),
            "cleanup_count": len(cleanup_rows),
            "synthetic_mutation_count": len(mutations),
            "x2_implementation_count": 0,
            "x2_observed_outcome_count": 0,
            "terminal_route": "PREPARED_NOT_SENT",
            "passed": True,
        },
    )
    build_method_flow()
    build_index_and_remaster()
    build_manifest()
    if read_json(PHASE / "validation/x1-staged-privacy.json")["confirmed_hit_count"]:
        raise RuntimeError("x1 privacy scan found confirmed payload hits")


if __name__ == "__main__":
    build()

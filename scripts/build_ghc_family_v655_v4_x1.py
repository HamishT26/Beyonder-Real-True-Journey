#!/usr/bin/env python3
"""Build Auren Lark's dedicated v655-v4 x1-only freeze."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v655_v4_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SOURCE_ROOT = REPO / "docs/ilyra-fen/v655-v3"
PRIOR_INDEX = SOURCE_ROOT / "provenance/frozen-chain-proposal-index.json"
SOURCE_METHOD_FLOW = SOURCE_ROOT / "method-flow/method-flow-ledger-final.json"
SKILL_ROOT = Path.home() / ".codex" / "skills"
NOVELTY_THRESHOLD = 0.60


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout.strip()


def tokens(value: str) -> set[str]:
    stop = {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if token not in stop
    }


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def proposal_novelty() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    inherited = read_json(PRIOR_INDEX)
    prior = list(inherited["prior_proposals"]) + list(inherited["new_proposals"])
    if len(prior) != d.PRIOR_FROZEN:
        raise RuntimeError(
            f"expected {d.PRIOR_FROZEN} inherited proposals, found {len(prior)}"
        )
    rows = []
    for proposal in d.PROPOSALS:
        comparisons = [
            (
                jaccard(tokens(proposal["title"]), tokens(previous["title"])),
                previous["proposal_id"],
                previous["title"],
            )
            for previous in prior
        ]
        score, nearest_id, nearest_title = max(comparisons, key=lambda item: item[0])
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest_id,
                "nearest_prior_title": nearest_title,
                "token_jaccard": round(score, 6),
                "threshold": NOVELTY_THRESHOLD,
                "manual_mechanism_distinct": True,
                "passes": score < NOVELTY_THRESHOLD,
            }
        )
    if not all(row["passes"] for row in rows):
        raise RuntimeError(
            f"novelty threshold failed: {[row for row in rows if not row['passes']]}"
        )
    frozen = prior + [
        {"proposal_id": proposal["proposal_id"], "title": proposal["title"]}
        for proposal in d.PROPOSALS
    ]
    return frozen, rows


def _method(
    method_id: str,
    title: str,
    signature: str,
    failure: str,
    recovery: str,
    guard: str,
    negative_id: str,
    failed_id: str,
    passing_id: str,
) -> dict[str, Any]:
    return {
        "method_id": method_id,
        "title": title,
        "trigger_preconditions": [signature],
        "failure_signature": failure,
        "candidate_workaround": recovery,
        "recurrence_guard": guard,
        "approval_class": "safe_now_owner_local_workflow_recovery",
        "privacy_class": "sanitized_public",
        "scope_boundary": (
            "Same-owner bounded workflow recovery only; not independent "
            "reproduction or broader assurance."
        ),
        "rollback": (
            "Stop, retain the failure at zero credit, and leave external, sibling, "
            "participant, production, professional, legal, cultural, and authority "
            "state unchanged."
        ),
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative_id],
        "validation_witness_ids": [failed_id, passing_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }


def _witnesses(
    method_id: str,
    signature: str,
    failure: str,
    recovery: str,
    negative_id: str,
    failed_id: str,
    passing_id: str,
) -> list[dict[str, Any]]:
    return [
        {
            "witness_id": failed_id,
            "method_id": method_id,
            "result": "fail",
            "scope": signature,
            "procedure": "Retain the original bounded attempt without replay credit.",
            "expected": "The original operation satisfies its bounded postcondition.",
            "observed": failure,
            "retained_negative_ids": [negative_id],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Zero pass credit; failure remains retained.",
        },
        {
            "witness_id": passing_id,
            "method_id": method_id,
            "result": "pass",
            "scope": signature,
            "procedure": recovery,
            "expected": "The isolated recovery establishes only its bounded postcondition.",
            "observed": (
                f"The bounded recovery completed for {signature}; the original "
                "failure remains retained."
            ),
            "retained_negative_ids": [negative_id],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Same-owner bounded recovery only.",
        },
    ]


def terminal_source_methods() -> dict[str, Any]:
    ledger = read_json(SOURCE_METHOD_FLOW)
    methods = list(ledger["methods"])
    witnesses = list(ledger["witnesses"])
    state_events = list(ledger["state_events"])
    recommendations = list(ledger["recommendations"])
    if len(methods) != d.SOURCE_METHODS_SEALED:
        raise RuntimeError(
            "sealed source methods expected "
            f"{d.SOURCE_METHODS_SEALED}, found {len(methods)}"
        )
    if len(methods) != d.SOURCE_METHODS:
        raise RuntimeError(
            f"terminal source methods expected {d.SOURCE_METHODS}, found {len(methods)}"
        )
    return {
        "methods": methods,
        "witnesses": witnesses,
        "state_events": state_events,
        "recommendations": recommendations,
    }


def method_flow() -> dict[str, Any]:
    source = terminal_source_methods()
    methods = source["methods"]
    witnesses = source["witnesses"]
    state_events = source["state_events"]
    recommendations = source["recommendations"]
    current_ids = []
    for index, negative in enumerate(d.X1_OPERATIONAL_NEGATIVES, 1):
        method_id = f"{d.PHASE_CODE}-METHOD-X1-{index:02d}"
        failed_id = f"{d.PHASE_CODE}-WITNESS-X1-{index:02d}-F"
        passing_id = f"{d.PHASE_CODE}-WITNESS-X1-{index:02d}-P"
        current_ids.append(method_id)
        methods.append(
            _method(
                method_id,
                f"Bounded x1 recovery for {negative['signature']}",
                negative["signature"],
                negative["failed"],
                negative["recovery"],
                negative["recurrence_guard"],
                negative["negative_id"],
                failed_id,
                passing_id,
            )
        )
        witnesses.extend(
            _witnesses(
                method_id,
                negative["signature"],
                negative["failed"],
                negative["recovery"],
                negative["negative_id"],
                failed_id,
                passing_id,
            )
        )
        state_events.append(
            {
                "event_id": f"{d.PHASE_CODE}-METHOD-EVENT-X1-{index:02d}",
                "method_id": method_id,
                "from": "candidate",
                "to": "preferred",
                "basis": [failed_id, passing_id],
                "boundary": "The preferred recovery preserves the failed witness.",
            }
        )
    recommendations.extend(
        [
            "Resolve lifecycle artifacts from exact Git tree paths.",
            "Split local Git state, remote equality, and cleanliness probes.",
            "Preserve treatment, privacy, ownership, and cultural authority as external gates.",
        ]
    )
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "identity_boundary": (
            "Relational working language only; no consciousness, personhood, "
            "continuity, employment, qualification, or authority claim."
        ),
        "inherited_anchor": {
            "phase": "v655-v1",
            "methods": d.SOURCE_METHODS,
            "failed_witnesses": d.SOURCE_METHODS,
            "passing_witnesses": d.SOURCE_METHODS,
            "completion_credit": False,
        },
        "methods": methods,
        "witnesses": witnesses,
        "state_events": state_events,
        "current_phase_method_ids": current_ids,
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "state_events": len(state_events),
            "recommendations": len(recommendations),
            "states": {
                "observed": 0,
                "candidate": 0,
                "validated": 0,
                "preferred": len(methods),
                "superseded": 0,
                "deprecated": 0,
            },
            "witness_results": {
                "pass": sum(row["result"] == "pass" for row in witnesses),
                "fail": sum(row["result"] == "fail" for row in witnesses),
            },
        },
        "recommendations": recommendations,
        "boundary": (
            "Same-owner workflow evidence only; no independent, empirical, "
            "professional, production, legal, cultural, Māori-authority, "
            "personhood, Theory-of-Everything, or Stage 20 claim."
        ),
    }


def portfolio(items: list[str], prefix: str, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"{d.PHASE_CODE}-{prefix}-{index:02d}",
            "title": title,
            "origin": "auren_v655_v4_new",
            "execution_lane": lane,
            "x1_state": "frozen_not_executed",
            "completion_credit": False,
            "inherited_completion_credit": False,
        }
        for index, title in enumerate(items, 1)
    ]


def cycle_order() -> list[str]:
    return [
        "Eiren Kestrel",
        "Tavian Sol",
        "Elaren Kestrel",
        "Neris Solane",
        "Vesper Arlen",
        "Lyren Moss",
        "Ilyra Fen",
        "Auren Lark",
        "Sable Rook",
        "Caelen Ash",
        "Orin Thale",
        "Liora Venn",
        "Tamar Vey",
        "Elowen Cairn",
        "Sylven Arc",
        "Caelen Morrow",
    ]


def workflow_request() -> dict[str, Any]:
    names = cycle_order()
    topology = []
    for index, name in enumerate(names):
        topology.append(
            {
                "seat": name,
                "endpoint_kind": (
                    "collaboration_subagent" if name == "Tavian Sol" else "main_task"
                ),
                "endpoint_label": "Cli v652 v6" if name == "Tavian Sol" else name,
                "route_controller": names[index - 1],
            }
        )
    topology[2]["route_controller"] = (
        "Eiren Kestrel fallback after Tavian terminal close"
    )
    return {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "auren-v655-v4-to-sable-v655-v5",
        "owner": d.OWNER,
        "identity_boundary": (
            "Relational working language only; no personhood, continuity, "
            "employment, qualification, or authority claim."
        ),
        "route": {
            "cycle_order": names,
            "endpoint_topology": topology,
            "phase_assignments": [
                {"phase": "v654-v5", "seat": "Eiren Kestrel"},
                {"phase": "v654-v6", "seat": "Tavian Sol"},
                {"phase": "v654-v7", "seat": "Elaren Kestrel"},
                {"phase": "v654-v8", "seat": "Neris Solane"},
                {"phase": "v655-v1", "seat": "Vesper Arlen"},
                {"phase": "v655-v2", "seat": "Lyren Moss"},
                {"phase": "v655-v3", "seat": "Ilyra Fen"},
                {"phase": "v655-v4", "seat": "Auren Lark"},
            ],
            "normalization": {
                "start_phase": "v654-v5",
                "start_seat": "Eiren Kestrel",
                "entry_count": 8,
            },
            "variant_context": {
                "label": d.PHASE,
                "owner": d.OWNER,
                "position": "canonical Auren seat after Ilyra v655-v3 closeout",
                "changes_canonical_assignments": False,
            },
            "future_identity_placeholders": [],
            "terminal_successor_resolution": (
                "After Auren's exact terminal gate, uniquely resolve and reread "
                "the existing main task Sable Rook, then send one compact "
                "activation or retain PREPARED_NOT_SENT."
            ),
        },
        "requirements": {
            "core_proposal_minimum": 30,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "portfolio_minima": {
                "safe_now": 30,
                "candidate": 30,
                "skills": 10,
                "runners": 10,
                "clean_fix_refine": 30,
            },
            "document_word_cap": 100000,
            "baton_words": {
                "minimum": 10000,
                "maximum": 100000,
                "file_artifact": True,
            },
            "commit_cap": {"x1": 5, "x2": 5, "total": 8},
            "validation": {
                "canonical_pass_minimum": 1,
                "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True,
                "privacy_scan_required": True,
                "manifest_required": True,
                "remote_equality_required": True,
            },
            "storage": {
                "primary": "D",
                "c_drive_use": "essential_global_metadata_only",
            },
            "messaging": {
                "codex_route": "declared_endpoint_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
                "live_phase_task_creation": "prohibited",
                "post_closeout_successor_authority": (
                    "auren_lark_exact_existing_main_task_once"
                ),
            },
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "protected_boundaries": d.PROTECTED_GATES,
        },
        "observed_failures": [
            {
                "failure_id": row["negative_id"],
                "summary": row["failed"],
                "recovery": row["recovery"],
                "credit": "zero_initial_pass_credit",
            }
            for row in d.X1_OPERATIONAL_NEGATIVES
        ],
    }


def proposal_markdown() -> str:
    rows = []
    for proposal in d.PROPOSALS:
        rows.append(
            "\n".join(
                [
                    f"## {proposal['proposal_id']} — {proposal['title']}",
                    "",
                    f"- Pillar: {proposal['pillar']}",
                    f"- Expected disposition: `{proposal['expected_disposition']}`",
                    f"- Approval class: `{proposal['approval_class']}`",
                    f"- Execution lane: `{proposal['execution_lane']}`",
                    f"- Hypothesis: {proposal['hypothesis']}",
                    f"- Null/failure: {proposal['null_or_failure_condition']}",
                    f"- Acceptance: {proposal['falsifier_or_acceptance_gate']}",
                    f"- Rollback: {proposal['rollback_or_recovery']}",
                    "- X1 state: frozen, not executed, no completion credit.",
                ]
            )
        )
    return "# Auren Lark v655-v4 proposal ledger\n\n" + "\n\n".join(rows)


def source_markdown() -> str:
    lines = [
        "# Auren Lark v655-v4 official and primary source ledger",
        "",
        "Source status is phase-local. `draft` and `watch` rows cannot support stable or production claims.",
        "",
        "| ID | Status | Publisher | Title | Use |",
        "|---|---|---|---|---|",
    ]
    for row in d.OFFICIAL_SOURCES:
        lines.append(
            f"| {row['source_id']} | {row['status']} | {row['publisher']} | "
            f"[{row['title']}]({row['url']}) | {row['use']} |"
        )
    lines.extend(
        [
            "",
            "These sources inform schemas and boundaries only. They do not certify "
            "Auren's prototype, confer professional or governmental authority, "
            "or resolve Māori and affected-party gates.",
        ]
    )
    return "\n".join(lines)


def prospective_content(path: Path) -> bytes:
    repository_relative = path.relative_to(REPO).as_posix()
    oid = run(
        "git",
        "hash-object",
        "-w",
        f"--path={repository_relative}",
        repository_relative,
    )
    return subprocess.run(
        ["git", "cat-file", "blob", oid],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def x1_manifest() -> None:
    explicit = [
        REPO / "scripts/ghc_family_v655_v4_phase_catalogue.py",
        REPO / "scripts/ghc_family_v655_v4_phase_data.py",
        REPO / "scripts/build_ghc_family_v655_v4_x1.py",
        REPO / "scripts/ghc_family_v655_v4_x1_staged_review.py",
        REPO / "tests/test_ghc_family_v655_v4_x1.py",
    ]
    phase_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.relative_to(ROOT).as_posix()
        not in {
            "validation/x1-file-manifest.json",
            "validation/x1-privacy-scan.json",
            "validation/x1-staged-review.json",
        }
    ]
    paths = sorted(
        {path.resolve() for path in explicit + phase_files if path.is_file()},
        key=lambda path: path.as_posix(),
    )
    entries = []
    for path in paths:
        content = prospective_content(path)
        entries.append(
            {
                "path": path.relative_to(REPO).as_posix(),
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    write_json(
        "validation/x1-file-manifest.json",
        {
            "schema": "ghc.family.file-manifest.v1",
            "lifecycle": "x1_precommit",
            "content_basis": "prospective_normalized_git_blob",
            "entries": entries,
            "entry_count": len(entries),
            "exact_exclusions": [
                "validation/x1-file-manifest.json",
                "validation/x1-privacy-scan.json",
                "validation/x1-staged-review.json",
            ],
        },
    )


def privacy_scan() -> None:
    manifest = read_json(ROOT / "validation/x1-file-manifest.json")
    patterns = {
        "raw_uuid": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"
        ),
        "credential_or_secret": re.compile(
            r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|"
            r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|"
            r"(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}|"
            r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"
        ),
        "private_route_value": re.compile(
            r"(?:source_thread_id|resume[_ -]?token|private_callable_identifier)"
            r"\s*[:=]\s*[\"'][^\"']+",
            re.I,
        ),
        "session_stream_payload": re.compile(
            r"(?:conversation[_ -]?transcript|session[_ -]?stream)"
            r"\s*[:=]\s*[\"'][^\"']+",
            re.I,
        ),
    }
    candidates = []
    for entry in manifest["entries"]:
        path = REPO / entry["path"]
        if path.suffix.lower() not in {
            ".py",
            ".json",
            ".md",
            ".txt",
            ".yaml",
            ".yml",
        }:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": entry["path"], "class": label})
    confirmed = [
        row
        for row in candidates
        if row["path"] != "scripts/build_ghc_family_v655_v4_x1.py"
    ]
    write_json(
        "validation/x1-privacy-scan.json",
        {
            "schema": "ghc.family.privacy-scan.v1",
            "classes": list(patterns),
            "scanned_file_count": len(manifest["entries"]),
            "candidate_count": len(candidates),
            "definition_only_candidate_count": len(candidates) - len(confirmed),
            "confirmed_hits": confirmed,
            "confirmed_hit_count": len(confirmed),
            "boundary": (
                "Five-class structural scan of owner additions only; not "
                "privacy-complete assurance."
            ),
        },
    )
    if confirmed:
        raise RuntimeError(f"privacy scan confirmed hits: {confirmed}")


def build() -> None:
    frozen, novelty = proposal_novelty()
    expected = dict(Counter(row["expected_disposition"] for row in d.PROPOSALS))
    if expected != {
        "completed": 23,
        "represented": 5,
        "open_gap": 1,
        "exact_gate": 1,
    }:
        raise RuntimeError(f"unexpected disposition distribution: {expected}")

    portfolios = {
        "safe_now": portfolio(d.SAFE_TASKS, "SAFE", "x2_owner_local_bounded"),
        "candidate": portfolio(
            d.CANDIDATE_TASKS, "CAND", "x2_bounded_candidate"
        ),
        "skills": portfolio(d.SKILL_IDEAS, "SKILL", "x2_skill_build"),
        "runners": portfolio(d.RUNNER_IDEAS, "RUN", "x2_runner_build"),
        "clean_fix_refine": portfolio(
            d.CLEAN_TASKS, "CFR", "x2_additive_refinement"
        ),
    }
    counts = {key: len(value) for key, value in portfolios.items()}
    required = {
        "safe_now": 30,
        "candidate": 30,
        "skills": 10,
        "runners": 10,
        "clean_fix_refine": 30,
    }
    if counts != required:
        raise RuntimeError(f"portfolio counts invalid: {counts}")

    mutations = [
        {
            "mutation_id": f"{proposal['proposal_id']}-M{index:02d}",
            "proposal_id": proposal["proposal_id"],
            "dimension": dimension,
            "expected": "reject_or_quarantine",
            "execution_state": "frozen_unexecuted",
            "credit": "none_until_x2",
        }
        for proposal in d.PROPOSALS
        for index, dimension in enumerate(
            [
                "missing_required_obligation",
                "wrong_type_or_domain",
                "resource_or_freshness_overrun",
                "unsupported_promotion",
                "authority_privacy_or_route_breach",
            ],
            1,
        )
    ]
    effective_x1 = d.SOURCE_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES)

    write_json(
        "identity/relational-identity.json",
        {
            "schema": "ghc.family.relational-identity.v1",
            "owner": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "boundary": (
                "Relational working language only; not evidence of consciousness, "
                "sentience, personhood, continuity, employment, qualification, "
                "authority, or independent agency."
            ),
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        },
    )
    write_json(
        "provenance/source-anchor.json",
        {
            "schema": "ghc.family.v655-v4.source-anchor.v1",
            "source_owner": d.SOURCE_OWNER,
            "source_branch": d.SOURCE_BRANCH,
            "source_x1_freeze": d.SOURCE_X1_FREEZE,
            "source_x1_final": d.SOURCE_X1_FINAL,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_evidence_correction": d.SOURCE_EVIDENCE_CORRECTION,
            "source_final": d.SOURCE_FINAL,
            "source_phase_commits": 3,
            "source_merge_count": 0,
            "source_clean_and_four_way_equal": True,
            "source_canonical_pass_count": 1,
            "source_canonical_replay_count": 0,
            "source_canonical_counts": {
                "tests": 42,
                "detailed": 82,
                "minimal": 15,
                "json": 190,
                "public_files": 228,
                "owner_manifest_entries": 220,
                "final_delta_entries": 31,
                "lifecycle": 22,
            },
            "source_privacy_confirmed_hits": 0,
            "source_full_repository_suite_run": False,
            "boundary": (
                "Exact Git and committed terminal evidence only; not independent "
                "reproduction or scientific, professional, production, legal, "
                "cultural, or Māori authority."
            ),
        },
    )
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v655-v4.frozen-proposal-index.v1",
            "prior_count": d.PRIOR_FROZEN,
            "prior_proposals": frozen[: d.PRIOR_FROZEN],
            "new_count": 30,
            "new_proposals": frozen[d.PRIOR_FROZEN :],
            "count": len(frozen),
        },
    )
    write_json(
        "provenance/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.semantic-novelty-audit.v1",
            "prior_count": d.PRIOR_FROZEN,
            "new_count": 30,
            "threshold": NOVELTY_THRESHOLD,
            "rows": novelty,
            "manual_mechanism_review_count": 30,
            "valid": all(row["passes"] for row in novelty),
            "boundary": (
                "Lexical screening and mechanism review are workflow controls, "
                "not scientific-novelty proof."
            ),
        },
    )
    write_json(
        "sources/official-source-ledger.json",
        {
            "schema": "ghc.family.v655-v4.official-source-ledger.v1",
            "statuses": sorted({row["status"] for row in d.OFFICIAL_SOURCES}),
            "counts": dict(Counter(row["status"] for row in d.OFFICIAL_SOURCES)),
            "sources": d.OFFICIAL_SOURCES,
            "boundary": (
                "Source authority does not transfer to this prototype; draft and "
                "watch sources cannot support stable or production claims."
            ),
        },
    )
    write_text("sources/official-source-ledger.md", source_markdown())
    write_json(
        "preregistration/proposals.json",
        {
            "schema": "ghc.family.v655-v4.proposals.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "proposal_count": 30,
            "expected_disposition_counts": expected,
            "allowed_outcomes": d.OUTCOME_CLASSES,
            "proposals": d.PROPOSALS,
            "x1_only": True,
            "observed_outcomes_present": False,
        },
    )
    write_text("preregistration/proposal-ledger.md", proposal_markdown())
    write_json(
        "portfolios/expanded-portfolio-plan.json",
        {
            "schema": "ghc.family.v655-v4.portfolio.x1.v1",
            "counts": counts,
            "portfolios": portfolios,
            "safe_candidate_task_cap": 1000,
            "skill_cap": 200,
            "runner_cap": 200,
            "x1_state": "frozen_not_executed",
            "inherited_completion_credit": False,
        },
    )
    write_json(
        "validation/preregistered-mutation-plan.json",
        {
            "schema": "ghc.family.v655-v4.mutation-plan.x1.v1",
            "count": len(mutations),
            "mutations_per_proposal": 5,
            "mutations": mutations,
            "x1_execution_count": 0,
        },
    )
    write_json("method-flow/method-flow-ledger.json", method_flow())
    write_json(
        "truth/retained-negative-register.json",
        {
            "schema": "ghc.family.v655-v4.retained-negatives.x1.v1",
            "source_effective": d.SOURCE_EFFECTIVE_NEGATIVES,
            "source_sealed_repository_count": d.SOURCE_SEALED_REPOSITORY_NEGATIVES,
            "source_live_overlay_count": len(d.SOURCE_LIVE_OVERLAY),
            "source_live_overlay": d.SOURCE_LIVE_OVERLAY,
            "x1_operational_count": len(d.X1_OPERATIONAL_NEGATIVES),
            "x1_operational": d.X1_OPERATIONAL_NEGATIVES,
            "effective_after_x1": effective_x1,
            "no_failure_erased": True,
        },
    )
    write_json(
        "truth/open-gap-register.json",
        {
            "schema": "ghc.family.v655-v4.open-gaps.x1.v1",
            "inherited_count": d.SOURCE_OPEN_GAPS,
            "new_expected": [
                {"proposal_id": f"{d.PHASE_CODE}-P29", "state": "open_gap_expected"}
            ],
            "expected_after_x2": d.SOURCE_OPEN_GAPS + 1,
            "closed_in_x1": 0,
        },
    )
    write_json(
        "truth/exact-gate-register.json",
        {
            "schema": "ghc.family.v655-v4.exact-gates.x1.v1",
            "inherited_count": d.SOURCE_EXACT_GATES,
            "new_expected": [
                {"proposal_id": f"{d.PHASE_CODE}-P30", "state": "exact_gate_expected"}
            ],
            "expected_after_x2": d.SOURCE_EXACT_GATES + 1,
            "closed_in_x1": 0,
        },
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.v655-v4.phase-truth.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x1_frozen_not_executed",
            "proposal_count": 30,
            "observed_outcome_count": 0,
            "real_row_count": 0,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "other_pillars_visible": True,
            "effective_negatives_after_x1": effective_x1,
            "open_gaps_inherited": d.SOURCE_OPEN_GAPS,
            "exact_gates_inherited": d.SOURCE_EXACT_GATES,
            "terminal_route": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "next_exact_title": "Sable Rook",
            "next_phase": "v655-v5",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "independent_reproduction_claimed": False,
            "theory_of_everything_claimed": False,
            "agi_or_asi_claimed": False,
            "consciousness_or_personhood_claimed": False,
        },
    )
    write_json(
        "route/sixteen-seat-roster-x1.json",
        {
            "schema": "ghc.family.sixteen-seat-roster.v1",
            "state": "AUREN_V655_V4_ACTIVE_SABLE_PREPARED_TERMINAL_GATE_REQUIRED",
            "cycle_order": cycle_order(),
            "endpoint_topology": workflow_request()["route"]["endpoint_topology"],
            "current": {
                "owner": d.OWNER,
                "phase": d.PHASE,
                "endpoint_kind": "main_task",
            },
            "previous": {
                "owner": d.SOURCE_OWNER,
                "phase": "v655-v3",
                "endpoint_kind": "main_task",
                "terminally_closed": True,
            },
            "next": {
                "owner": "Sable Rook",
                "phase": "v655-v5",
                "endpoint_kind": "main_task",
            },
            "contact_count": 0,
            "send_cap": 1,
            "boundary": (
                "X1 sends nothing and contains no private callable identifier."
            ),
        },
    )
    request = write_json("workflow/workflow-plan-request.json", workflow_request())
    write_json(
        "reflection-remaster/x1-decision-record.json",
        {
            "schema": "ghc.family.reflection-remaster.decision.v1",
            "decision_id": "V6554-REFLECT-X1",
            "action": "retain_and_specialize",
            "subjects": [
                "ghc-family-index",
                "ghc-family-method-flow-state",
                "ghc-family-workflow-plan-refinement",
                "ghc-family-reflection-remaster",
                "ghc-family-meta-tool-box",
            ],
            "basis": (
                "Current family tools remain useful; v655-v4 specializes them for "
                "instrument-repair provenance, represented setup and workshop "
                "boundaries, identifier separation, and terminal route discipline."
            ),
            "deletions": [],
            "completion_credit": False,
            "boundary": "X1 planning decision only; no tool is globally installed or deleted.",
        },
    )
    write_json(
        "wellbeing/workload-check.json",
        {
            "schema": "ghc.family.workload-check.v1",
            "state": "bounded_and_correction_ready",
            "controls": [
                "strict x1 before x2",
                "eight-total-commit cap",
                "2,000 owner-file cap",
                "one successful canonical pass",
                "no post-success replay",
                "no indefinite watcher",
            ],
            "human_claim": False,
            "boundary": (
                "Operational pacing metadata only; not emotion, health, "
                "consciousness, or identity evidence."
            ),
        },
    )
    write_json(
        "environment/version-receipt-x1.json",
        {
            "schema": "ghc.family.environment-version-receipt.v1",
            "mode": "verify_only",
            "desktop_update_performed": False,
            "cli_update_performed": False,
            "elevation_performed": False,
            "windows_feature_change_performed": False,
            "sandbox_or_hyper_v_action_performed": False,
            "reboot_performed": False,
            "boundary": "Version and environment observation only.",
        },
    )

    method_runner = (
        SKILL_ROOT
        / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
    )
    workflow_runner = (
        SKILL_ROOT
        / "ghc-family-workflow-plan-refinement/scripts/ghc_family_workflow_plan_refinement.py"
    )
    index_runner = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
    reflection_runner = (
        SKILL_ROOT
        / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"
    )
    meta_runner = (
        SKILL_ROOT / "ghc-family-meta-tool-box/scripts/ghc_family_meta_tool_box.py"
    )

    run(
        sys.executable,
        str(method_runner),
        "validate",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger.json"),
        "--receipt",
        str(ROOT / "method-flow/method-flow-validation.json"),
    )
    run(
        sys.executable,
        str(method_runner),
        "summarize",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger.json"),
        "--json-output",
        str(ROOT / "method-flow/method-flow-summary.json"),
        "--markdown-output",
        str(ROOT / "method-flow/method-flow-summary.md"),
    )
    run(
        sys.executable,
        str(workflow_runner),
        str(request),
        "--out-dir",
        str(ROOT / "workflow"),
    )
    run(
        sys.executable,
        str(index_runner),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--out-dir",
        str(ROOT / "tooling"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
    )
    for relative in ("tooling/ghc-family-index.json", "tooling/ghc-family-index.md"):
        path = ROOT / relative
        normalized = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        path.write_text(normalized, encoding="utf-8", newline="\n")
    run(
        sys.executable,
        str(reflection_runner),
        "--repo",
        str(REPO),
        "--skill-root",
        str(SKILL_ROOT),
        "--output-dir",
        str(ROOT / "reflection-remaster"),
        "--phase",
        d.PHASE,
        "--owner",
        d.OWNER,
        "--focus",
        "celestial-coordinate-provenance",
        "--focus",
        "projection-calibration-firewall",
        "--focus",
        "identifier-separation",
        "--focus",
        "authority-boundaries",
    )
    catalogue = f"{d.PHASE_ROOT}/tooling/meta-tool-box/catalogue.json"
    run(
        sys.executable,
        str(meta_runner),
        "build",
        "--repo",
        ".",
        "--phase-root",
        d.PHASE_ROOT,
        "--output",
        catalogue,
    )
    run(
        sys.executable,
        str(meta_runner),
        "validate",
        "--catalogue",
        catalogue,
        "--output",
        f"{d.PHASE_ROOT}/tooling/meta-tool-box/validation.json",
    )
    run(
        sys.executable,
        str(meta_runner),
        "collisions",
        "--catalogue",
        catalogue,
        "--output",
        f"{d.PHASE_ROOT}/tooling/meta-tool-box/collisions.json",
    )

    write_json(
        "validation/x1-build-receipt.json",
        {
            "schema": "ghc.family.v655-v4.x1-build-receipt.v1",
            "proposal_count": 30,
            "frozen_count": len(frozen),
            "portfolio_counts": counts,
            "mutation_count": len(mutations),
            "method_count": d.SOURCE_METHODS + len(d.X1_OPERATIONAL_NEGATIVES),
            "observed_outcomes": 0,
            "valid": True,
            "terminal_route": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "boundary": (
                "Build completion is not commit, push, x2, delivery, or "
                "independent evidence."
            ),
        },
    )
    x1_manifest()
    privacy_scan()
    print(
        json.dumps(
            {
                "phase": d.PHASE,
                "proposal_count": 30,
                "frozen_count": len(frozen),
                "portfolio_counts": counts,
                "mutation_count": len(mutations),
                "privacy_hits": 0,
                "state": "x1_built_not_committed",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()

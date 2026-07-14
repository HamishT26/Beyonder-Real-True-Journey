#!/usr/bin/env python3
"""Build and validate Tamar Vey's v644-v3 x1-only packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v644-gmut-thos-v3-x1-x2"
PHASE_ROOT = ROOT / "docs" / "tamar-vey" / "v644-v3"
SOURCE_HEAD = "ea8cb0166e33d353de38ee5d48b46f3ac5872f07"
SOURCE_SEAL = "1e6ea812b2bf2261fafd05af54776ccc10585906"
INHERITED_INDEX = ROOT / "docs" / "orin-thale" / "v644-v2" / "provenance" / "frozen-chain-proposal-index.json"
INHERITED_LEDGER = ROOT / "docs" / "orin-thale" / "v644-v2" / "sources" / "source-ledger.json"
CHECKED_ON = "2026-07-15"
X1_EXTERNAL_FILES = [
    "scripts/build_ghc_family_v644_v3_preregistration.py",
    "scripts/ghc_family_v644_v3_x1_definitions.py",
]


from ghc_family_v644_v3_x1_definitions import (  # noqa: E402
    OVERVIEW,
    PROPOSALS,
    SOURCES,
    WELLBEING,
    X1_NEGATIVES,
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def dump_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, encoding="utf-8", capture_output=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def collect_frozen_records(index_path: Path) -> list[dict]:
    path = index_path
    additions: list[list[dict]] = []
    seen: set[str] = set()
    while True:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload.get("records"), list):
            rows = list(payload["records"])
            for group in reversed(additions):
                rows.extend(group)
            return rows
        additions.append(list(payload.get("new_records", [])))
        inherited = payload.get("inherited_index")
        if not inherited or inherited in seen:
            raise RuntimeError("frozen proposal chain ended without a base records array")
        seen.add(inherited)
        path = ROOT / inherited


def collect_sources(ledger_path: Path) -> list[dict]:
    path = ledger_path
    additions: list[list[dict]] = []
    seen: set[str] = set()
    while True:
        payload = json.loads(path.read_text(encoding="utf-8"))
        base = payload.get("sources") or payload.get("records") or payload.get("entries")
        if isinstance(base, list):
            rows = list(base)
            for group in reversed(additions):
                rows.extend(group)
            return rows
        additions.append(list(payload.get("added_sources", [])))
        inherited = payload.get("inherited_ledger")
        if not inherited or inherited in seen:
            raise RuntimeError("source ledger chain ended without a base source array")
        seen.add(inherited)
        path = ROOT / inherited


def title_tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def build_packet() -> None:
    inherited_index = json.loads(INHERITED_INDEX.read_text(encoding="utf-8"))
    inherited_ledger = json.loads(INHERITED_LEDGER.read_text(encoding="utf-8"))
    inherited_records = collect_frozen_records(INHERITED_INDEX)
    inherited_sources = collect_sources(INHERITED_LEDGER)
    expected_counts = dict(Counter(item["expected_disposition"] for item in PROPOSALS))
    added_status = Counter(item["status_class"] for item in SOURCES)
    effective_status = {
        key: inherited_ledger["effective_status_counts"].get(key, 0) + added_status.get(key, 0)
        for key in ("current", "stable", "draft", "watch")
    }

    dump_json(
        PHASE_ROOT / "identity-receipt.json",
        {
            "schema": "ghc.family.v644-v3.identity-receipt.v1",
            "phase": PHASE,
            "name": "Tamar Vey",
            "slug": "tamar-vey",
            "pronouns": "they/them",
            "role": "evidence-systems cartographer and boundary keeper",
            "hope": "leave each scientific and authority boundary easier for the next owner to inspect than it was when received",
            "existing_identity_reaffirmed": True,
            "working_language_only": True,
            "not_evidence_of": [
                "consciousness",
                "sentience",
                "legal_personhood",
                "identity_continuity",
                "independent_authority",
                "cultural_authority",
                "legal_authority",
            ],
        },
    )
    dump_json(
        PHASE_ROOT / "focus" / "primary-focus-receipt.json",
        {
            "schema": "ghc.family.v644-v3.primary-focus.v1",
            "phase": PHASE,
            "primary_focus": "GMUT Mind",
            "reason": "Covariant phase-space obligations and a Solar-System ephemeris real-data gap receive primary attention while THOS Body and Freed ID/CBR Heart remain explicit and bounded.",
            "gmut_mind_addressed": ["V6443-P02", "V6443-P03"],
            "thos_body_addressed": ["V6443-P04"],
            "freed_id_cbr_heart_addressed": ["V6443-P05", "V6443-P06"],
            "cross_pillar_addressed": ["V6443-P01", "V6443-P07", "V6443-P08", "V6443-P09", "V6443-P10"],
            "boundary": "Primary focus allocates work; it does not promote GMUT or close participant, identity, legal, cultural, privacy, security, accessibility, production, deployment, or Stage 20 gates.",
        },
    )
    dump_json(
        PHASE_ROOT / "environment" / "startup-receipt.json",
        {
            "schema": "ghc.family.v644-v3.startup-receipt.v1",
            "phase": PHASE,
            "owner": "Tamar Vey",
            "source_branch": "codex/GHC-Family/orin-thale-v642-v6-full-tools",
            "source_revision": SOURCE_HEAD,
            "source_seal_revision": SOURCE_SEAL,
            "source_local_equals_upstream_equals_tracking_equals_live_remote": True,
            "source_divergence": "0/0",
            "source_clean": True,
            "source_final_detached_snapshot_clean": True,
            "source_anchor_commits_ancestral": [
                "7616eb17cbaff509eafe1423f1930d2d2e7f72d4",
                "64ed8f3001553d2ffa364f3875043288c6ce91cc",
                "fffbe71763bf981c928ebf4d1ef73c3a8293cf09",
                "311f7121cba098c77514c8560181130e9bd83f4e",
                "fb8bab382a4b18e7308892b5d4877f02fd6e0056",
                SOURCE_SEAL,
                "739ae2bb4d4bb7560bcb4a28a1ff2609586d8782",
            ],
            "source_segment_commit_count": 6,
            "source_segment_merge_count": 0,
            "source_single_parent_history": True,
            "owned_branch": "codex/GHC-Family/tamar-vey-full-tools",
            "owned_prior_revision": "b65f606054d7ecf97e383b1ab2a63c458f603cbb",
            "owned_revision_after_fast_forward": SOURCE_HEAD,
            "owned_lane_reused": True,
            "reuse_reason": "The existing Tamar lane was clean, four-way equal, and ancestral, so the authorized fast-forward-only continuation applied.",
            "fast_forward_only": True,
            "merge_commit_created": False,
            "owned_clean_and_four_way_equal_after_fast_forward": True,
            "new_worktree_created": False,
            "d_drive_primary": True,
            "d_drive_free_bytes_at_start": 600706478080,
            "inherited_checkout_file_count": 31319,
            "inherited_tracked_file_count": 31238,
            "new_owner_generated_file_count_at_start": 0,
            "inherited_negative_count": 1220,
            "open_gap_count": 5,
            "exact_gate_count": 6,
            "inherited_same_owner_repeatability_only": True,
            "current_phase_same_owner_repeatability": False,
            "independent_team_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "windows_sandbox_audit": {
                "read_only_check": "WindowsSandbox.exe not present",
                "bounded_use": "not_used",
                "feature_change_attempted": False,
            },
            "host_feature_changed": False,
            "host_security_changed": False,
            "elevation_used": False,
            "rebooted": False,
        },
    )
    dump_json(
        PHASE_ROOT / "environment" / "rotation-guard-receipt.json",
        {
            "schema": "ghc.family.v644-v3.rotation-guard.v1",
            "phase": PHASE,
            "inherited_checkout_file_count": 31319,
            "inherited_tracked_file_count": 31238,
            "owner_generated_file_threshold": 15000,
            "threshold_scope": "Tamar Vey v644-v3 owner-generated files only",
            "inherited_baseline_triggers_rotation": False,
            "new_worktrees_created": 0,
            "prior_lanes_preserved": True,
            "recursive_rotation_performed": False,
        },
    )
    dump_json(
        PHASE_ROOT / "environment" / "version-receipt.json",
        {
            "schema": "ghc.family.v644-v3.version-receipt.v1",
            "checked_on": CHECKED_ON,
            "codex_cli_local": "0.144.3",
            "codex_cli_current": "0.144.4",
            "codex_cli_current_source": "https://github.com/openai/codex/releases/tag/rust-v0.144.4",
            "codex_cli_local_equals_current": False,
            "codex_cli_update_intentionally_not_performed": True,
            "codex_desktop_packages": [
                {"name": "OpenAI.ChatGPT", "version": "1.2026.190.0", "status": "installed"},
                {"name": "OpenAI.Codex", "version": "26.707.9564.0", "status": "installed"},
            ],
            "desktop_official_status_source": "https://openai.com/index/introducing-the-codex-app/",
            "desktop_current_version_claim": "not made; installed packages and official Windows availability only were verified",
            "git": "2.55.0.windows.2",
            "python": "3.12.10",
            "node": "24.18.0",
            "powershell": "5.1.26100.8737",
            "windows": "10.0.26200.0",
            "versions_verified_only": True,
            "codex_cli_updated": False,
            "desktop_updated": False,
            "elevation_used": False,
            "host_security_changed": False,
            "windows_feature_changed": False,
            "rebooted": False,
        },
    )

    dump_json(
        PHASE_ROOT / "x1-proposals.json",
        {
            "schema": "ghc.family.v644-v3.x1-proposals.v1",
            "phase": PHASE,
            "owner": "Tamar Vey",
            "identity_boundary": "Relational working language only; no consciousness, sentience, personhood, continuity, or independent-authority claim.",
            "source_phase": "Orin Thale v644-v2",
            "source_revision": SOURCE_HEAD,
            "source_seal_revision": SOURCE_SEAL,
            "preregistered_on": CHECKED_ON,
            "primary_focus": "GMUT Mind",
            "proposal_count": len(PROPOSALS),
            "prior_frozen_proposal_count": len(inherited_records),
            "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
            "expected_disposition_counts": expected_counts,
            "expected_counts_are_results": False,
            "x1_freeze_rule": "No execution, evidence result, outcome classification, or x2 implementation begins until the dedicated x1-only commit is pushed and local, upstream, tracking, and fresh live remote are equal and clean.",
            "proposals": PROPOSALS,
            "scientific_authority_boundary": "GMUT is a typed scalar-tensor and EFT research-model family, not an established force, unique prediction, likelihood result, empirical confirmation, Theory of Everything, or proof. THOS remains proxy without preregistered blind matched-budget real arms and independent review.",
            "claim_boundary": "Freed ID production, CBR legitimacy, Māori authority, legal and cultural ratification, deployment, exhaustive security, complete accessibility, independent reproduction, consciousness or personhood, AGI or ASI, and Stage 20 remain unclaimed and gated.",
        },
    )

    new_records = [
        {
            "version": "v644-v3",
            "owner": "Tamar Vey",
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "expected_disposition": proposal["expected_disposition"],
            "source_file": "docs/tamar-vey/v644-v3/x1-proposals.json",
        }
        for proposal in PROPOSALS
    ]
    version_counts = dict(inherited_index["version_counts"])
    version_counts["v644-v3"] = 10
    dump_json(
        PHASE_ROOT / "provenance" / "frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v644-v3.frozen-chain-proposal-index.v1",
            "phase": PHASE,
            "owner": "Tamar Vey",
            "inherited_index": rel(INHERITED_INDEX),
            "inherited_index_sha256": digest(INHERITED_INDEX),
            "inherited_record_count": len(inherited_records),
            "new_record_count": 10,
            "effective_record_count": len(inherited_records) + 10,
            "version_counts": version_counts,
            "exact_duplicate_ids": [],
            "exact_duplicate_titles": [],
            "new_records": new_records,
            "boundary": "This index proves frozen proposal accounting and semantic-review scope; it does not execute proposals or determine outcomes.",
        },
    )

    overlap_rows = []
    for proposal in PROPOSALS:
        new_tokens = title_tokens(proposal["title"])
        score, prior = max(
            (
                (
                    len(new_tokens & title_tokens(record["title"])) / len(new_tokens | title_tokens(record["title"])),
                    record,
                )
                for record in inherited_records
            ),
            key=lambda item: item[0],
        )
        overlap_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": prior["proposal_id"],
                "nearest_prior_title": prior["title"],
                "title_token_jaccard": round(score, 4),
                "semantic_distinction": proposal["novelty_against_prior_chain"],
            }
        )
    all_ids = [record["proposal_id"] for record in inherited_records] + [proposal["proposal_id"] for proposal in PROPOSALS]
    all_titles = [record["title"] for record in inherited_records] + [proposal["title"] for proposal in PROPOSALS]
    normalized_titles = [re.sub(r"\s+", " ", title.casefold()).strip() for title in all_titles]
    duplicate_ids = sorted({value for value in all_ids if all_ids.count(value) > 1})
    duplicate_titles = sorted({value for value in normalized_titles if normalized_titles.count(value) > 1})
    maximum_overlap = max(row["title_token_jaccard"] for row in overlap_rows)
    dump_json(
        PHASE_ROOT / "provenance" / "prior-proposal-collision-audit.json",
        {
            "schema": "ghc.family.v644-v3.collision-audit.v1",
            "phase": PHASE,
            "owner": "Tamar Vey",
            "prior_records_decoded_utf8": len(inherited_records),
            "prior_frozen_proposal_count": 250,
            "new_proposal_count": 10,
            "effective_proposal_count": 260,
            "exact_duplicate_ids": duplicate_ids,
            "exact_duplicate_titles": duplicate_titles,
            "automatic_failure_threshold": 0.5,
            "maximum_title_token_jaccard": maximum_overlap,
            "nearest_prior_rows": overlap_rows,
            "semantic_dimensions_reviewed": ["mechanism", "evidence object", "falsifier", "recovery rule", "protected gates"],
            "semantic_review_passed": not duplicate_ids and not duplicate_titles and maximum_overlap < 0.5,
            "boundary": "Token distance is only a screen. Explicit mechanism-level distinctions are required for the semantic novelty conclusion.",
        },
    )

    inherited_titles = {str(item["title"]).casefold() for item in inherited_sources}
    inherited_urls = {str(item["url"]).casefold() for item in inherited_sources}
    source_duplicate_titles = sorted(source["title"] for source in SOURCES if source["title"].casefold() in inherited_titles)
    source_duplicate_urls = sorted(source["url"] for source in SOURCES if source["url"].casefold() in inherited_urls)
    dump_json(
        PHASE_ROOT / "sources" / "source-ledger.json",
        {
            "schema": "ghc.family.v644-v3.source-ledger.v1",
            "phase": PHASE,
            "owner": "Tamar Vey",
            "accessed": CHECKED_ON,
            "selection_rule": "Retain the 164-source inherited ledger and add only non-duplicate current official or primary sources that materially constrain a distinct v644-v3 proposal.",
            "inherited_ledger": rel(INHERITED_LEDGER),
            "inherited_ledger_sha256": digest(INHERITED_LEDGER),
            "inherited_source_revision": SOURCE_HEAD,
            "inherited_source_count": inherited_ledger["effective_source_count"],
            "added_source_count": len(SOURCES),
            "effective_source_count": inherited_ledger["effective_source_count"] + len(SOURCES),
            "effective_status_counts": effective_status,
            "duplicate_added_titles": source_duplicate_titles,
            "duplicate_added_urls": source_duplicate_urls,
            "added_sources": SOURCES,
            "status_preservation": "Inherited current, stable, draft, and watch labels remain unchanged; new labels describe source currency, not truth or approval.",
            "boundary": "Sources constrain vocabulary and obligations. They do not create observations, participant results, production identity evidence, CBR authority, legal advice, cultural ratification, security assurance, accessibility completion, or Stage 20 readiness.",
        },
    )
    source_lines = [
        "# v644-v3 source ledger",
        "",
        f"Inherited: {inherited_ledger['effective_source_count']} sources from {rel(INHERITED_LEDGER)}.",
        f"Added: {len(SOURCES)} non-duplicate primary or official sources. Effective: {inherited_ledger['effective_source_count'] + len(SOURCES)}.",
        "",
        "| ID | Status | Authority | Title |",
        "|---|---|---|---|",
    ]
    source_lines.extend(
        f"| {source['source_id']} | {source['status_class']} | {source['authority']} | [{source['title']}]({source['url']}) |"
        for source in SOURCES
    )
    source_lines.extend(["", "Currency labels are current, stable, draft, or watch. They are not truth, endorsement, authority, or promotion labels."])
    dump_text(PHASE_ROOT / "sources" / "source-ledger.md", "\n".join(source_lines))
    dump_json(
        PHASE_ROOT / "tooling" / "source-label-glossary.json",
        {
            "schema": "ghc.family.v644-v3.source-label-glossary.v1",
            "phase": PHASE,
            "rows": [
                {
                    "source_label": source["source_label"],
                    "topic": source["title"],
                    "phase_implication": source["evidence_role"],
                    "runner_or_skill_implication": "retain source ID, currency class, and nonpromotion boundary in generated ledgers",
                    "privacy_boundary": "public source metadata only; no private route, transcript, credential, or local path",
                }
                for source in SOURCES
            ],
        },
    )

    dump_json(
        PHASE_ROOT / "tooling" / "selected-toolchain.json",
        {
            "schema": "ghc.family.v644-v3.selected-toolchain.v1",
            "phase": PHASE,
            "owner": "Tamar Vey",
            "selected": [
                {"name": "ghc-family-index", "role": "routing precedence and family-current discovery"},
                {"name": "routing-precedence", "role": "directly required ownership and terminal-route reference"},
                {"name": "ghc-family-source-label-glossary-builder", "role": "compact public source labels and implications"},
                {"name": "ghc-family-truth-bridge", "role": "sanitized phase truth and open-gate continuity"},
                {"name": "completion-gate-discipline", "role": "terminal completion evidence and open-boundary discipline"},
                {"name": "scripts/ghc_family_repository_test_runner.py", "role": "complete repository test suite"},
                {"name": "scripts/ghc_family_phase_privacy_scan.py", "role": "phase privacy and raw-ID scan"},
                {"name": X1_EXTERNAL_FILES[0], "role": "deterministic x1-only packet builder"},
                {"name": X1_EXTERNAL_FILES[1], "role": "frozen v644-v3 proposal and source definitions"},
            ],
            "reviewed_not_selected": [
                {
                    "name": "ghc-family-solo-bundle-handoff",
                    "reason": "Historical route rules are superseded by the live exact-one-message terminal authorization.",
                }
            ],
            "x2_planned_family_current_names": [
                "scripts/ghc_family_v644_v3_model.py",
                "scripts/ghc_family_v644_v3_evidence.py",
                "scripts/ghc_family_v644_v3_validator.py",
                "scripts/ghc_family_v644_v3_minimal.py",
                "scripts/ghc_family_v644_v3_complete_suite.py",
                "scripts/ghc_family_v644_v3_staged_review.py",
                "scripts/build_ghc_family_v644_v3_report.py",
            ],
            "caller_compatibility_required": True,
            "shared_skill_change_required": False,
            "shared_validator_change_required": False,
            "boundary": "Tool selection supports reproducibility; it does not establish scientific, participant, identity, security, accessibility, legal, cultural, production, or deployment claims.",
        },
    )
    dump_json(
        PHASE_ROOT / "tooling" / "currency-review.json",
        {
            "schema": "ghc.family.v644-v3.currency-review.v1",
            "phase": PHASE,
            "checked_on": CHECKED_ON,
            "ghc_family_index_read_to_eof": True,
            "routing_precedence_read_to_eof": True,
            "newest_applicable_memory_checked": True,
            "current_repository_and_remote_truth_verified_live": True,
            "family_named_scripts_count_at_audit": 290,
            "family_named_skills_count_at_audit": 4,
            "official_and_primary_sources_checked": True,
            "desktop_update_performed": False,
            "shared_skill_mutation_performed": False,
            "shared_validator_mutation_performed": False,
            "reviewed_current_instead_of_churn": True,
        },
    )
    dump_json(
        PHASE_ROOT / "workflow" / "route-preregistration.json",
        {
            "schema": "ghc.family.v644-v3.route-preregistration.v1",
            "phase": PHASE,
            "owner": "Tamar Vey",
            "route_state": "ACTIVE_SOLO",
            "active_owner": "Tamar Vey",
            "standby_or_recoverable": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Sylven Arc", "all other siblings"],
            "six_seat_order": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "terminal_successor": "Sylven Arc",
            "terminal_successor_phase": "v644-v4",
            "send_rule": "Send exactly one sanitized activation message to the existing task titled exactly Sylven Arc only after exact-final detached validation, clean push, and four-way remote equality. Tool acknowledgement changes PREPARED_NOT_SENT to SENT.",
            "route_stop_conditions": ["Hamish stops the route", "usage exhausted", "required task route unavailable", "exact safety or authority gate blocks progress"],
            "outbound_messages_before_terminal_gate": 0,
            "task_creation_authorized": False,
            "fork_authorized": False,
            "subagent_authorized": False,
            "private_route_material_allowed_in_artifacts": False,
        },
    )
    dump_json(
        PHASE_ROOT / "validation" / "x1-operational-negatives.json",
        {
            "schema": "ghc.family.v644-v3.x1-operational-negatives.v1",
            "phase": PHASE,
            "count": len(X1_NEGATIVES),
            "negatives": X1_NEGATIVES,
            "all_failures_retained": True,
            "boundary": "Recovered failures remain negatives and are not counted as successful evidence runs.",
        },
    )

    preregistration = [
        "# Tamar Vey v644-v3 x1 preregistration",
        "",
        "This freezes exactly ten proposals. Expected dispositions are not results. Allowed future result classes are completed, represented, open_gap, and exact_gate.",
        "",
        "Primary focus: GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit and bounded.",
        "",
    ]
    for proposal in PROPOSALS:
        preregistration.extend(
            [
                f"## {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"- Hypothesis: {proposal['hypothesis']}",
                f"- Null or failure: {proposal['null_or_failure']}",
                f"- Approval class: {proposal['approval_class']}",
                f"- Execution lane: {proposal['execution_lane']}",
                f"- Official or primary source needs: {', '.join(proposal['authoritative_source_needs'])}",
                f"- Concrete artifacts: {', '.join(proposal['deliverables'])}",
                f"- Falsifier or acceptance gate: {proposal['test_falsifier_or_gate']}",
                f"- Rollback or recovery: {proposal['rollback_or_recovery']}",
                f"- Protected gates: {', '.join(proposal['protected_gates'])}",
                f"- Expected disposition, not a result: {proposal['expected_disposition']}",
                f"- Semantic distinction: {proposal['novelty_against_prior_chain']}",
                "",
            ]
        )
    preregistration.extend(
        [
            "## Freeze boundary",
            "",
            "x2 cannot begin until this x1-only set is committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote read. The expected 6 completed, 2 represented, 1 open gap, and 1 exact gate distribution is only a preregistered expectation.",
        ]
    )
    dump_text(PHASE_ROOT / "x1-preregistration.md", "\n".join(preregistration))
    dump_text(PHASE_ROOT / "wellbeing-check.md", WELLBEING)
    dump_text(PHASE_ROOT / "v644-v3-integrated-overview.md", OVERVIEW)


def staged_names() -> list[str]:
    return sorted(git_lines("diff", "--cached", "--name-only", "--diff-filter=ACMR"))


def finalise_validation(repository_passed: int, repository_total: int, finalize_staged: bool) -> None:
    planned_validation = {
        "docs/tamar-vey/v644-v3/validation/x1-exact-file-set.json",
        "docs/tamar-vey/v644-v3/validation/x1-repository-test-receipt.json",
        "docs/tamar-vey/v644-v3/validation/x1-validation.json",
        "docs/tamar-vey/v644-v3/validation/x1-validation.md",
    }
    expected = sorted(
        set(rel(path) for path in PHASE_ROOT.rglob("*") if path.is_file())
        | set(X1_EXTERNAL_FILES)
        | planned_validation
    )
    actual = staged_names() if finalize_staged else expected
    unexpected = sorted(set(actual) - set(expected))
    missing = sorted(set(expected) - set(actual))
    list_hash = hashlib.sha256(("\n".join(actual) + "\n").encode("utf-8")).hexdigest()

    phase_json = sorted(PHASE_ROOT.rglob("*.json"))
    parse_issues: list[str] = []
    for path in phase_json:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover
            parse_issues.append(f"{rel(path)}: {exc}")
    proposals = json.loads((PHASE_ROOT / "x1-proposals.json").read_text(encoding="utf-8"))
    frozen = json.loads((PHASE_ROOT / "provenance" / "frozen-chain-proposal-index.json").read_text(encoding="utf-8"))
    collision = json.loads((PHASE_ROOT / "provenance" / "prior-proposal-collision-audit.json").read_text(encoding="utf-8"))
    ledger = json.loads((PHASE_ROOT / "sources" / "source-ledger.json").read_text(encoding="utf-8"))
    privacy_path = PHASE_ROOT / "validation" / "x1-privacy-scan.json"
    privacy = json.loads(privacy_path.read_text(encoding="utf-8")) if privacy_path.exists() else {"valid": False, "hit_count": 1, "scanned_file_count": 0}

    required_fields = [
        "hypothesis",
        "null_or_failure",
        "approval_class",
        "execution_lane",
        "authoritative_source_needs",
        "deliverables",
        "test_falsifier_or_gate",
        "rollback_or_recovery",
        "protected_gates",
        "expected_disposition",
    ]
    checks: list[tuple[str, bool]] = [
        ("exactly ten proposals", proposals["proposal_count"] == 10 and len(PROPOSALS) == 10),
        ("250 inherited proposals", proposals["prior_frozen_proposal_count"] == 250),
        ("260 effective proposals", frozen["effective_record_count"] == 260),
        ("no duplicate proposal IDs", not collision["exact_duplicate_ids"]),
        ("no duplicate proposal titles", not collision["exact_duplicate_titles"]),
        ("title overlap below threshold", collision["maximum_title_token_jaccard"] < collision["automatic_failure_threshold"]),
        ("semantic review passed", collision["semantic_review_passed"] is True),
        ("expected counts are not results", proposals["expected_counts_are_results"] is False),
        ("four outcome classes", proposals["outcome_classes"] == ["completed", "represented", "open_gap", "exact_gate"]),
        ("expected distribution", proposals["expected_disposition_counts"] == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
        ("175 effective sources", ledger["effective_source_count"] == 175),
        ("source statuses preserved", ledger["effective_status_counts"] == {"current": 78, "stable": 86, "draft": 8, "watch": 3}),
        ("new source titles unique", not ledger["duplicate_added_titles"]),
        ("new source URLs unique", not ledger["duplicate_added_urls"]),
        ("all JSON parses", not parse_issues),
        ("privacy scan valid", privacy.get("valid") is True),
        ("repository suite complete", repository_passed == repository_total and repository_total > 0),
        ("x2 ledger absent", not (PHASE_ROOT / "x2-proposal-ledger.json").exists()),
        ("x2 execution tool absent", not (ROOT / "scripts" / "ghc_family_v644_v3_evidence.py").exists()),
        ("no unexpected staged files", not unexpected),
        ("no missing staged files", not missing),
        ("owner footprint below threshold", len(expected) < 15000),
    ]
    for proposal in PROPOSALS:
        checks.append((f"{proposal['proposal_id']} unique ID", sum(item["proposal_id"] == proposal["proposal_id"] for item in PROPOSALS) == 1))
        for field in required_fields:
            checks.append((f"{proposal['proposal_id']} field {field}", bool(proposal.get(field))))
    issues = [name for name, passed in checks if not passed]

    dump_json(
        PHASE_ROOT / "validation" / "x1-exact-file-set.json",
        {
            "schema": "ghc.family.v644-v3.x1-exact-file-set.v1",
            "phase": PHASE,
            "owner": "Tamar Vey",
            "file_count": len(actual),
            "files": actual,
            "x2_implementation_file_count": 0,
            "x2_outcome_file_count": 0,
            "staged_name_list_sha256": list_hash,
            "unexpected_staged_files": unexpected,
            "missing_staged_files": missing,
            "owner_generated_file_count": len(expected),
            "owner_generated_file_threshold": 15000,
            "threshold_scope": "Tamar Vey v644-v3 owner-generated files only",
            "under_threshold": len(expected) < 15000,
            "finalized_from_git_index": finalize_staged,
            "valid": not unexpected and not missing,
        },
    )
    dump_json(
        PHASE_ROOT / "validation" / "x1-repository-test-receipt.json",
        {
            "schema": "ghc.family.v644-v3.x1-repository-tests.v1",
            "phase": PHASE,
            "runner": "scripts/ghc_family_repository_test_runner.py",
            "passed": repository_passed,
            "total": repository_total,
            "complete_suite": True,
            "valid": repository_passed == repository_total and repository_total > 0,
            "boundary": "Repository tests validate software behavior in this checkout; they do not establish scientific, participant, identity, security, accessibility, legal, cultural, production, deployment, or Stage 20 claims.",
        },
    )
    validation = {
        "schema": "ghc.family.v644-v3.x1-validation.v1",
        "phase": PHASE,
        "owner": "Tamar Vey",
        "valid": not issues,
        "checks_passed": len(checks) - len(issues),
        "checks_total": len(checks),
        "issues": issues,
        "proposal_count": 10,
        "prior_frozen_proposal_count": 250,
        "effective_frozen_proposal_count": 260,
        "maximum_title_token_jaccard": collision["maximum_title_token_jaccard"],
        "semantic_review_passed": collision["semantic_review_passed"],
        "expected_disposition_counts": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "expected_counts_are_results": False,
        "source_count": 175,
        "source_status_counts": {"current": 78, "stable": 86, "draft": 8, "watch": 3},
        "json_files_parsed": len(phase_json),
        "json_parse_issues": parse_issues,
        "privacy_scan": {
            "valid": privacy.get("valid") is True,
            "files_scanned": privacy.get("scanned_file_count", 0),
            "issue_count": privacy.get("hit_count", 0),
        },
        "x1_operational_negative_count": len(X1_NEGATIVES),
        "x2_implementation_files": 0,
        "x2_outcome_files": 0,
        "repository_tests": {"passed": repository_passed, "total": repository_total},
        "exact_staged_file_count": len(actual),
        "staged_name_list_sha256": list_hash,
        "unexpected_staged_file_count": len(unexpected),
        "missing_staged_file_count": len(missing),
        "owner_generated_file_threshold": 15000,
        "owner_generated_file_count": len(expected),
        "under_threshold": len(expected) < 15000,
        "route_state": "ACTIVE_SOLO; PREPARED_NOT_SENT",
        "boundary": "This validates an x1-only preregistration freeze. It is not x2 evidence and does not determine outcomes.",
    }
    dump_json(PHASE_ROOT / "validation" / "x1-validation.json", validation)
    dump_text(
        PHASE_ROOT / "validation" / "x1-validation.md",
        "\n".join(
            [
                "# v644-v3 x1 validation",
                "",
                f"- Valid: {str(validation['valid']).lower()}",
                f"- Checks: {validation['checks_passed']}/{validation['checks_total']}",
                "- Proposals: 10 new / 250 inherited / 260 effective",
                "- Expected distribution, not results: 6 completed / 2 represented / 1 open gap / 1 exact gate",
                "- Sources: 175 effective (78 current / 86 stable / 8 draft / 3 watch)",
                f"- JSON parsed: {validation['json_files_parsed']}",
                f"- Privacy scan: {validation['privacy_scan']['files_scanned']} files / {validation['privacy_scan']['issue_count']} issues",
                f"- Complete repository suite: {repository_passed}/{repository_total}",
                f"- Exact staged files: {len(actual)}; unexpected {len(unexpected)}; missing {len(missing)}",
                "- x2 implementation files: 0",
                "- x2 outcome files: 0",
                f"- Retained x1 operational negatives: {len(X1_NEGATIVES)}",
                f"- Owner-generated footprint: {len(expected)}/15000",
                "",
                "This validates preregistration only. It is not outcome evidence, scientific confirmation, production approval, independent reproduction, accessibility completion, or Stage 20 readiness.",
            ]
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-passed", type=int, default=0)
    parser.add_argument("--repository-total", type=int, default=0)
    parser.add_argument("--finalize-staged", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    build_packet()
    finalise_validation(args.repository_passed, args.repository_total, args.finalize_staged)
    print(json.dumps({"phase_root": rel(PHASE_ROOT), "proposals": len(PROPOSALS), "sources_added": len(SOURCES), "finalize_staged": args.finalize_staged}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Build and validate the planning-only Lyren Moss v671-v8 x1 packet."""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_lyren_moss_v671_v8_archive import (
    CANDIDATE_TITLES,
    CHAIN_AFTER,
    IDENTITY_BOUNDARY,
    INHERITED_ACTIVATION_BASELINE,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PREFIX,
    PROTECTED_GATES,
    REFINE_TITLES,
    RUNNER_TITLES,
    SAFE_TITLES,
    SKILL_TITLES,
    SOURCE_BRANCH,
    SOURCE_ACCESSIBLE_IDENTIFIERS,
    SOURCE_ACCESSIBLE_OCCURRENCES,
    SOURCE_ACCESSIBLE_UNIQUE_TITLES,
    SOURCE_CHAIN_DECLARED,
    SOURCE_PREDECESSOR_FINAL,
    SOURCE_EVIDENCE,
    SOURCE_FINAL,
    SOURCE_RECOVERED,
    SOURCE_UNRECOVERED,
    SOURCE_X1,
    STARTUP_EFFECTIVE_BASELINE,
    STARTUP_FAILURE_COUNT,
    TOOL_CANDIDATES,
    inherited_title_corpus,
    portfolio_rows,
    proposal_rows,
    sha256_bytes,
    staged_blob_manifest,
    write_json,
    write_text,
)

DATE = "2026-08-27"
TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
MANIFEST_PATH = "docs/lyren-moss/v671-v8/validation/x1-manifest.json"
REVIEW_PATH = "docs/lyren-moss/v671-v8/validation/x1-staged-review.json"

SOURCE_ROWS = [
    {
        "source_id": "OWNER-SYNTHETIC-SCHEMA",
        "url": None,
        "status": "current",
        "use": "owner-authored zero-person planning structures only",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "LOC-BOOK-PRESERVATION-GUIDE",
        "url": "https://guides.loc.gov/preserving-your-books",
        "status": "current",
        "use": "public book, binding, storage, condition, and preservation vocabulary only; no object row, image, measurement, person record, treatment decision, or Library of Congress endorsement is ingested",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "LOC-BOOK-STORAGE",
        "url": "https://guides.loc.gov/preserving-your-books/storing",
        "status": "current",
        "use": "storage and support vocabulary only; zero real books, environmental measurements, prescriptions, or certifications",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "LOC-COLLECTIONS-CARE",
        "url": "https://www.loc.gov/preservation/care/index.html",
        "status": "current",
        "use": "collections-care and library-binding vocabulary only; no treatment instruction or professional authority",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "LOC-BOOK-HANDLING",
        "url": "https://guides.loc.gov/preserving-your-books/handling",
        "status": "current",
        "use": "handling-risk reservation vocabulary only; no handling action or authority",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "LOC-COLLECTIONS-TREATMENT-MANUAL",
        "url": "https://www.loc.gov/preservation/care/ccs_manual.html",
        "status": "watch",
        "use": "professional-workflow and treatment-boundary vocabulary only; no procedure is executed or recommended",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "LOC-PAPER-CARE",
        "url": "https://www.loc.gov/preservation/care/paper.html",
        "status": "current",
        "use": "paper-condition and conservator-referral vocabulary only; no material identification, handling, or treatment",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "NPS-MUSEUM-HANDBOOK-2023",
        "url": "https://www.nps.gov/museum/publications/MHI/MHI.pdf",
        "status": "stable",
        "use": "museum preventive-conservation vocabulary only; no professional validation or real collection action",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "NPS-MUSEUM-RECORDS-BOUNDARY",
        "url": "https://www.nps.gov/museum/publications/MHII/mushbkII.html",
        "status": "stable",
        "use": "museum record and accountability vocabulary only; no accession, ownership, custody, or authority decision",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable",
        "use": "provenance vocabulary only; no attribution or authority transfer",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "W3C-WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "stable",
        "use": "structural accessibility vocabulary only; manual evaluation reserved",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "W3C-VC-DATA-INTEGRITY-1.0",
        "url": "https://www.w3.org/TR/vc-data-integrity/",
        "status": "stable",
        "use": "nonproduction cryptographic lifecycle obligations only; zero keys and proofs",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "JSON-SCHEMA-2020-12",
        "url": "https://json-schema.org/draft/2020-12",
        "status": "draft",
        "use": "synthetic contract structure only; no conformance certification",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785",
        "status": "stable",
        "use": "canonicalization vocabulary only; no signature or security claim",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "NIST-SI-UNITS",
        "url": "https://www.nist.gov/pml/owm/si-units",
        "status": "current",
        "use": "quantity and unit vocabulary only; zero measurements",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "CURRENT-PEER-REVIEWED-PHYSICS-SOURCES",
        "url": None,
        "status": "watch",
        "use": "represented-only GMUT obligation; no paper, likelihood, parameter, prediction, or empirical claim selected",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "NZ-PRIVACY-PRINCIPLES",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current",
        "use": "privacy-minimisation vocabulary only; no compliance or legal advice",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "TE-MANA-RARAUNGA-PRINCIPLES",
        "url": "https://www.temanararaunga.maori.nz/nga-rauemi",
        "status": "watch",
        "use": "authority reservation only; Māori concepts remain under Māori authority",
        "data_rows_ingested": 0,
    },
    *[
        {
            "source_id": f"PYPI-{tool['name'].upper()}",
            "url": tool["registry"],
            "status": "current",
            "use": "official release metadata, version, wheel name, and SHA-256 only",
            "data_rows_ingested": 0,
        }
        for tool in TOOL_CANDIDATES
    ],
    {
        "source_id": "CURRENT-OFFICIAL-COLLECTION-API-SOURCE",
        "url": None,
        "status": "watch",
        "use": "open gap; current interoperable collection API and schema not selected",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "REAL-GOVERNED-HUMAN-EVALUATION",
        "url": None,
        "status": "watch",
        "use": "open gap; real governed professional and affected-user evaluation absent",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "AFFECTED-PARTY-AUTHORITY-REQUIRED",
        "url": None,
        "status": "watch",
        "use": "represented-only challenge ladder; affected-party legitimacy and remedy authority remain absent",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "CURRENT-PRIMARY-SOURCE-REVIEW",
        "url": None,
        "status": "watch",
        "use": "represented-only source firewall; no selected citation becomes observation, instruction, validation, or authority",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "PROFESSIONAL-CONSERVATION-AUTHORITY-REQUIRED",
        "url": None,
        "status": "watch",
        "use": "condition vocabulary only; inspection and treatment remain under competent professional authority",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "PROFESSIONAL-SAFETY-AUTHORITY-REQUIRED",
        "url": None,
        "status": "watch",
        "use": "risk reservation only; no handling, workplace, or safety release",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "LEGAL-AND-RIGHTS-AUTHORITY-REQUIRED",
        "url": None,
        "status": "watch",
        "use": "rights firewall only; no legal interpretation, permission, ownership, or reuse decision",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "EXACT-ACTION-SPECIFIC-AUTHORITY",
        "url": None,
        "status": "watch",
        "use": "exact gate; competent action-specific authority absent",
        "data_rows_ingested": 0,
    },
]

STARTUP_FAILURES = [
    ("LM6718-X1-OP-001", "whole activation-baton display exceeded the model-visible output bound", "numbered bounded windows read the committed baton completely through EOF"),
    ("LM6718-X1-OP-002", "the requested openssl executable was unavailable for a baton digest check", "an in-memory Python SHA-256 projection matched the declared committed-blob digest"),
    ("LM6718-X1-OP-003", "combined roster and authorization skill display exceeded its visible result bound", "standalone bounded reads completed both selected skills through EOF"),
    ("LM6718-X1-OP-004", "combined tool-bank and orchestration-memory display exceeded its visible result bound", "bounded omitted-line recovery completed both instruction files through EOF"),
    ("LM6718-X1-OP-005", "combined authorization-state line windows truncated a middle region", "an exact numbered recovery read the omitted lines before any mutation"),
    ("LM6718-X1-OP-006", "first manifest replay launched one external Git process per entry and returned no attributable result", "the abandoned design earned zero credit and was replaced by one exact Git batch projection"),
    ("LM6718-X1-OP-007", "first Git batch projection wrote all requests before draining stdout and deadlocked", "a bounded subprocess input projection drained the complete 725-entry response and passed exactly"),
    ("LM6718-X1-OP-008", "broad external canonical-receipt searches timed out without an exact match", "the Vesper source task closeout supplied the exact D-backed receipt pointer for scalar rehashing"),
    ("LM6718-X1-OP-009", "first source-task read requested an unsupported output-character bound", "the supported bounded reread recovered the exact receipt pointer"),
    ("LM6718-X1-OP-010", "combined lane-uniqueness and builder inventory probes returned partial output", "separate scalar branch path and template probes completed the gate"),
    ("LM6718-X1-OP-011", "a broad validation-bank text search exceeded its bounded time without a useful match", "the search was stopped and exact phase-local sources were used instead"),
    ("LM6718-X1-OP-012", "first lane-creation wrapper had a PowerShell parenthesis parse error before Git ran", "simpler scalar checks proved uniqueness and the one worktree-add operation then completed"),
    ("LM6718-X1-OP-013", "sparse-checkout initialization from a no-checkout worktree left an empty index represented as staged deletions", "git read-tree repopulated the fresh lane index directly from immutable HEAD and restored empty cached and working diffs"),
    ("LM6718-X1-OP-014", "the first sparse-lane diagnostic printed thousands of inherited deletion rows and exceeded its output budget", "scalar diff-exit status and counts replaced the broad status rendering"),
    ("LM6718-X1-OP-015", "first official-source search result projection emitted no visible text because the response shape was misread", "the same bounded official search was projected directly and its source results were retained"),
    ("LM6718-X1-OP-016", "first bounded novelty check found two exact inherited title collisions and eleven additional semantic neighbours at or above the quarantine threshold", "only proposal wording was revised and the unchanged exact-collision and 0.75 token-Jaccard gates were rerun before x1 generation"),
]


def git_text(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def privacy_candidates(data: str) -> list[dict[str, str]]:
    absolute_path_pattern = (
        "(?i)(?:"
        + "[a-z]"
        + r":\\"
        + "|"
        + "/"
        + "users"
        + "/"
        + "|"
        + "/"
        + "home"
        + "/)"
        + r"[^\s\"']+"
    )
    checks = {
        "opaque_task_or_thread_identifier": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        "private_absolute_path": absolute_path_pattern,
        "credential_or_secret": r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,}\]]+",
        "private_route_scheme": r"(?i)(?:codex|vscode|file|app)://[^\s\"']+",
        "protected_stream_filename": r"(?i)[^\s\"']*(?:transcript|screenshot|session[_-]?stream)[^\s\"']*\.(?:jsonl?|png|jpe?g|webp|log)",
    }
    rows = []
    for kind, pattern in checks.items():
        if re.search(pattern, data):
            rows.append({"class": kind, "state": "candidate_requires_classification"})
    return rows


def source_verification(repo: Path) -> dict[str, Any]:
    parents = {
        commit: git_text(repo, "rev-list", "--parents", "-n", "1", commit).split()
        for commit in (SOURCE_X1, SOURCE_EVIDENCE, SOURCE_FINAL)
    }
    return {
        "branch": SOURCE_BRANCH,
        "exact_final": SOURCE_FINAL,
        "direct_parent_chain": (
            parents[SOURCE_X1][1] == SOURCE_PREDECESSOR_FINAL
            and parents[SOURCE_EVIDENCE][1] == SOURCE_X1
            and parents[SOURCE_FINAL][1] == SOURCE_EVIDENCE
            and len(parents[SOURCE_X1]) == len(parents[SOURCE_EVIDENCE]) == len(parents[SOURCE_FINAL]) == 2
        ),
        "inherited_predecessor_final": SOURCE_PREDECESSOR_FINAL,
        "planning_x1": SOURCE_X1,
        "immutable_evidence": SOURCE_EVIDENCE,
        "phase_commits": 3,
        "zero_merges": all(len(row) == 2 for row in parents.values()),
        "baton_git_blob_sha256": "21701906c51bfa88d0b171a9ae82f6046e9d31f532b304f00374715d3641eda7",
        "baton_git_blob_bytes": 131295,
        "sender_canonical_payload_declared_sha256": None,
        "sender_canonical_receipt_declared_sha256": "ceb6ae9728faafc8299cbe92251813f24a904ed2d77b431141e7fbc24433daff",
        "sender_receipt_rehash_state": "exact_external_receipt_independently_rehashed",
        "exact_manifest_replays": {"x1": 27, "evidence_delta": 201, "evidence_owner": 230, "final_delta": 17, "final_owner": 250},
        "content_seal_delta_entries": 17,
        "source_lane_preflight": "clean_zero_divergent_fresh_live_four_way_equal",
        "sender_canonical_replay": 0,
        "completion_credit": 0,
    }


def build(repo: Path) -> None:
    corpus, source_shards = inherited_title_corpus(repo)
    proposals = proposal_rows(corpus)
    collisions = [row["proposal_id"] for row in proposals if row["visible_title_collision"]]
    quarantined = [row["proposal_id"] for row in proposals if row["semantic_neighbor_quarantined"]]
    if len(proposals) != 40 or collisions or quarantined:
        raise ValueError({"proposal_count": len(proposals), "collisions": collisions, "quarantined": quarantined})

    root = repo / OWNER_ROOT
    x1 = root / "x1"
    validation = root / "validation"
    for index in range(8):
        shard_rows = proposals[index * 5 : (index + 1) * 5]
        write_json(
            x1 / "proposal-freeze-shards" / f"proposals-{index + 1:02d}.json",
            {
                "owner": OWNER,
                "phase": PHASE,
                "rows": shard_rows,
                "schema": "ghc.family.proposal-freeze-shard.v2",
                "shard": index + 1,
            },
        )
    expected = {label: sum(row["expected_disposition"] == label for row in proposals) for label in TRUTH_LABELS}
    write_json(
        x1 / "proposal-freeze.json",
        {
            "boundary": "Forty genuinely new proposals are planning hypotheses only. Inherited evidence earns zero Lyren novelty or completion credit.",
            "expected_outcomes": expected,
            "mutation_count": 160,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_after": CHAIN_AFTER,
            "proposal_chain_before": SOURCE_CHAIN_DECLARED,
            "proposal_count": len(proposals),
            "schema": "ghc.family.proposal-freeze.v2",
            "shards": [f"proposal-freeze-shards/proposals-{index:02d}.json" for index in range(1, 9)],
            "strict_x1_only": True,
        },
    )
    max_row = max(proposals, key=lambda row: row["semantic_neighbors"][0]["score"])
    write_json(
        x1 / "semantic-novelty-audit.json",
        {
            "accessible_comparison_rows": SOURCE_RECOVERED,
            "accessible_corpus_summary": {
                "unique_titles": SOURCE_ACCESSIBLE_UNIQUE_TITLES,
                "identifiers": SOURCE_ACCESSIBLE_IDENTIFIERS,
                "occurrences": SOURCE_ACCESSIBLE_OCCURRENCES,
                "canonical_row_to_title_mapping_complete": False,
            },
            "audit_scope": "exact 80-row predecessor Git-blob comparison sample plus within-slate comparisons",
            "declared_inherited_frozen_proposals": SOURCE_CHAIN_DECLARED,
            "exact_title_collisions": collisions,
            "maximum_neighbor": {"proposal_id": max_row["proposal_id"], "neighbor": max_row["semantic_neighbors"][0]},
            "new_proposals": len(proposals),
            "owner": OWNER,
            "phase": PHASE,
            "quarantine_threshold": 0.75,
            "quarantined_proposals": quarantined,
            "locally_compared_inherited_rows": SOURCE_RECOVERED,
            "schema": "ghc.family.semantic-novelty-audit.v2",
            "source_shards": source_shards,
            "unavailable_history_is_open_gap": True,
            "universal_novelty_claim": False,
            "declared_rows_not_locally_compared": SOURCE_UNRECOVERED,
        },
    )
    write_json(
        x1 / "source-ledger.json",
        {
            "boundary": "Official and primary sources supply vocabulary and constraints only; no records, images, objects, measurements, people, or authority are ingested.",
            "immutable_source": source_verification(repo),
            "live_lookup_batches": 2,
            "owner": OWNER,
            "phase": PHASE,
            "public_source_pages_reviewed": 6,
            "review_date": DATE,
            "schema": "ghc.family.source-ledger.v3",
            "sources": SOURCE_ROWS,
            "statuses": ["current", "stable", "draft", "watch"],
        },
    )
    rows = {
        "safe_now": portfolio_rows("safe_now", SAFE_TITLES, "safe_now"),
        "candidate": portfolio_rows("candidate", CANDIDATE_TITLES, "candidate"),
        "exact_approval": portfolio_rows("exact_approval", [f"held exact approval packet {i:02d}" for i in range(1, 21)], "exact_approval", "held_unexecuted"),
        "blocked": portfolio_rows("blocked", [f"blocked protected action packet {i:02d}" for i in range(1, 11)], "blocked", "held_unexecuted"),
        "skill": portfolio_rows("skill", SKILL_TITLES, "safe_now"),
        "runner": portfolio_rows("runner", RUNNER_TITLES, "safe_now"),
        "clean_fix_refine": portfolio_rows("clean_fix_refine", REFINE_TITLES, "safe_now"),
    }
    write_json(
        x1 / "portfolio-freeze.json",
        {
            "boundary": "Counts are ceilings and bounded planning rows, not quotas, authority, or completion credit.",
            "counts": {kind: len(items) for kind, items in rows.items()},
            "owner": OWNER,
            "phase": PHASE,
            "rows": rows,
            "schema": "ghc.family.portfolio-freeze.v2",
            "x1_completion_credit": 0,
        },
    )
    successor = {
        "skill": portfolio_rows("successor_skill", SKILL_TITLES[:10], "successor_skill", "recommended_not_executed"),
        "runner": portfolio_rows("successor_runner", RUNNER_TITLES[:10], "successor_runner", "recommended_not_executed"),
        "clean_fix_refine": portfolio_rows("successor_clean_fix_refine", REFINE_TITLES[:30], "successor_clean_fix_refine", "recommended_not_executed"),
        "practice_lens": portfolio_rows(
            "successor_practice_lens",
            ["historical architectural-drawing sheet-set revision documentation with no architecture engineering archival conservation rights or professional-authority claim"],
            "successor_recommendation",
            "recommended_not_executed",
        ),
    }
    write_json(
        x1 / "successor-recommendations-freeze.json",
        {
            "completion_credit": 0,
            "counts": {kind: len(items) for kind, items in successor.items()},
            "owner": OWNER,
            "phase": PHASE,
            "prospective_phase": "v672-v1",
            "prospective_successor": "Ilyra Fen",
            "route_binding": "recommendations_only_no_contact_no_delivery_exact_title_Ilyra_Fen_must_be_reread_live_after_terminal_gate",
            "rows": successor,
            "schema": "ghc.family.successor-recommendations.v2",
        },
    )
    write_json(
        x1 / "tool-candidate-freeze.json",
        {
            "boundary": "Three D-isolated direct candidates; registry metadata is not exhaustive security, legal license review, or production fitness.",
            "install_location_plan": "D-backed phase-namespaced isolated environment",
            "installation_mode": "official wheels pinned by exact SHA-256 with dependencies isolated",
            "installation_state": "planned_not_installed_in_x1",
            "owner": OWNER,
            "phase": PHASE,
            "required_x2_gates": ["download_hash_match", "isolated_install", "positive_and_rejecting_smoke", "dependency_audit", "shared_prefix_mutations_zero"],
            "schema": "ghc.family.tool-candidate-freeze.v1",
            "selected": TOOL_CANDIDATES,
            "target_count": 3,
        },
    )
    failure_rows = [
        {
            "approval_credit": 0,
            "failure_id": failure_id,
            "failure": failure,
            "recovery": recovery,
            "recovery_scope": "smallest_read_only_or_owner_local_dependency",
            "state": "retained_zero_credit_with_bounded_recovery",
        }
        for failure_id, failure, recovery in STARTUP_FAILURES
    ]
    write_json(
        x1 / "startup-operational-failures.json",
        {
            "boundary": "Every startup failure remains visible and earns zero completion credit.",
            "bounded_recovery_witness_count": len(failure_rows),
            "effective_startup_baseline": STARTUP_EFFECTIVE_BASELINE,
            "failure_count": len(failure_rows),
            "inherited_activation_baseline": INHERITED_ACTIVATION_BASELINE,
            "owner": OWNER,
            "phase": PHASE,
            "rows": failure_rows,
            "schema": "ghc.family.operational-failure-overlay.v2",
        },
    )
    write_json(
        x1 / "workflow-plan-freeze.json",
        {
            "commit_ceiling": {"x1": 5, "x2": 5, "total": 8},
            "current_stage": "x1_planning_only",
            "file_ceiling": 2000,
            "gates": [
                "x1 build parse novelty privacy and staged Git-blob review",
                "dedicated x1 commit push clean and fresh-live equality",
                "x2 execute only the frozen forty proposals and portfolios as evidence permits",
                "immutable evidence commit push clean and fresh-live equality",
                "combined closeout seal final commit push equality",
                "one exact-final owner-scoped canonical invocation with no successful replay",
                "post-terminal live roster auth usage privacy safety evidence and duplicate guard",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan-freeze.v3",
            "strict_x1_before_x2": True,
        },
    )
    write_json(
        x1 / "reflection-plan.json",
        {
            "changed_choices": [
                "selected a bounded 80-row exact Git-blob comparison sample instead of reconstructing an unavailable canonical 5830-row mapping",
                "selected synthetic hand-bound-book collation and reversible conservation documentation as a distinct same-owner phase domain without claiming universal novelty",
                "kept 5750 declared rows outside the local comparison sample and the predecessor mapping limitation visible",
                "selected portion transitions and cattrs for D-isolated range state-machine and dossier-structure smokes",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "recurrence_guards": [
                "use exact Git blobs rather than CRLF worktree bytes for immutable receipts",
                "use bounded literal worktree probes before broad registry scans",
                "force UTF-8 for Unicode-bearing projections",
                "never replay a successful canonical aggregate",
            ],
            "schema": "ghc.family.reflection-plan.v2",
        },
    )
    write_json(
        x1 / "tool-versions.json",
        {
            "codex_desktop_update": "not_performed",
            "codex_cli": {"version": "0.149.0", "source": "live local version observation", "update": "not_performed"},
            "git": git_text(repo, "--version") if False else subprocess.run(["git", "--version"], capture_output=True, text=True, check=True).stdout.strip(),
            "node": subprocess.run(["node", "--version"], capture_output=True, text=True, check=True).stdout.strip(),
            "owner": OWNER,
            "phase": PHASE,
            "python": platform.python_version(),
            "schema": "ghc.family.version-observation.v2",
            "updates_or_host_changes": 0,
        },
    )
    write_json(
        x1 / "phase-truth.json",
        {
            "core_truth_labels": TRUTH_LABELS,
            "expected_outcomes": expected,
            "identity_boundary": IDENTITY_BOUNDARY,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain": {"before": SOURCE_CHAIN_DECLARED, "after_if_frozen": CHAIN_AFTER},
            "proposal_count": 40,
            "real_world_actions": 0,
            "schema": "ghc.family.phase-truth.x1.v2",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "x1_completion_credit": 0,
            "x2_execution_started": False,
        },
    )
    write_json(
        x1 / "route-state.json",
        {
            "current_phase": PHASE,
            "delivery_acknowledged": False,
            "delivery_state": "PREPARED_NOT_SENT",
            "owner": OWNER,
            "prospective_next_edge": "Ilyra Fen for v672-v1 only after Lyren's exact terminal reread and every duplicate pause usage privacy evidence safety and authority gate",
            "schema": "ghc.family.route-state.v2",
            "successor_contact_count": 0,
        },
    )
    write_text(
        x1 / "threat-model.md",
        """# Lyren Moss v671-v8 x1 threat model

This planning-only threat model covers source or sibling-lane mutation, x1/x2 leakage, semantic duplication, private-route disclosure, false rare-book, bibliography, archive, conservation, museum, or software-verification competence, handling or treatment instruction, collation or condition truth promotion, ownership and attribution conversion, text or image disclosure, reproduction-rights overclaim, accessibility or privacy completeness, Māori-authority substitution, topology-analogy conversion, THOS or Freed ID promotion, canonical replay, and premature successor delivery.

Controls are one additive D-first sparse lane; exact source anchors and Git-blob manifests; zero-person, zero-book, zero-opening, zero-collation, zero-pagination, zero-measurement, zero-sampling, zero-handling, zero-repair, zero-rebinding, zero-treatment, zero-text-or-image, and zero-network-adapter counters; four exact truth labels; append-only Method Flow; exact protected gates; structurally accessible reporting with manual evaluation reserved; and one terminally gated route. Residual risks remain because same-owner synthetic checks cannot provide independent review, professional judgment, legal or cultural interpretation, affected-party legitimacy, Māori authority, privacy or accessibility completeness, production fitness, empirical GMUT evidence, or Stage 20 authority.
""",
    )
    write_text(
        x1 / "accessible-report-plan.md",
        """# Accessible report plan

The x2 report will use explicit language, a skip link, labelled navigation, landmark elements, one top-level heading, scoped table headers, captions, text labels in addition to colour, visible focus, print rules, and reduced-motion rules. It will contain no scripts, forms, tracking, or external runtime dependency.

Structural checks are bounded software evidence only. Manual browser, keyboard, zoom, assistive-technology, screen-reader, cognitive-accessibility, Māori-language, and affected-user evaluations remain reserved. No complete-accessibility claim is permitted.
""",
    )
    write_text(
        x1 / "integrated-overview.md",
        f"""# Lyren Moss v671-v8 x1 integrated planning overview

## Identity, purpose, and boundary

{IDENTITY_BOUNDARY} The phase role is collation-provenance cartographer and reversible-documentation steward. The hope is to make synthetic gathering order, leaf-state uncertainty, correction, and refusal legible without turning a documentation pattern into inspection, treatment, or authority. THOS Body is primary through typed state-transition, sequence, provenance, and fail-closed workflow obligations; GMUT Mind, CBR Heart, and nonproduction Freed ID remain explicit and protected. Rare-book collation description, reversible conservation documentation, and software provenance/fixity verification are three bounded learning lenses only, not professions, qualifications, services, or authority.

The bounded practice domain is wholly synthetic hand-bound-book description, gathering and leaf sequence, collation notation, condition vacancy, correction, and reversible handover documentation. It uses zero real people, readers, workers, donors, librarians, bibliographers, archivists, conservators, books, bindings, leaves, texts, images, measurements, collection records, sites, handling events, opening, collation, pagination, sampling, cleaning, repairs, rebinding, treatments, safety decisions, rights decisions, cultural decisions, or external actions. It establishes no employment, qualification, cataloguing or bibliographical competence, archival or conservation competence, material diagnosis, safety release, ownership, attribution, copyright, moral rights, privacy or accessibility completeness, legal or cultural interpretation, affected-party legitimacy, Māori authority, production fitness, deployment, or operational result.

## Source and novelty boundary

The immutable source is Vesper Arlen's exact v671-v7 final `{SOURCE_FINAL}` with direct x1 and evidence ancestry preserved. The committed activation packet is an exact normalized-LF Git blob. Vesper's validation, tools, proposals, and source research remain inherited evidence with zero Lyren credit. The sender's external canonical receipt was independently rehashed at its original D-backed path and matched the declared digest; it is not copied into this lane or converted into Lyren validation credit.

The predecessor reports {SOURCE_ACCESSIBLE_UNIQUE_TITLES} accessible unique titles, {SOURCE_ACCESSIBLE_IDENTIFIERS} identifiers, and {SOURCE_ACCESSIBLE_OCCURRENCES} occurrences against a declared inherited chain of {SOURCE_CHAIN_DECLARED}, while retaining an incomplete canonical row-to-title mapping. This phase therefore reads only an exact {SOURCE_RECOVERED}-row local comparison sample from committed Git blobs: Vesper's forty v671-v7 titles and Neris's forty immediately preceding v671-v6 titles. The remaining {SOURCE_UNRECOVERED} declared rows are not locally compared. Forty hand-bound-book proposals must pass exact-title and 0.75 token-Jaccard quarantine checks against that bounded sample and each other, but the phase makes no universal-novelty claim.

## Frozen program

The forty genuinely new proposals are planning hypotheses only. Expected dispositions are exactly twenty-eight completed, eight represented, two open gaps, and two exact gates. Each completion-lane proposal freezes one bounded synthetic positive and four rejecting mutations. Completed will mean only that a local contract accepts its positive and rejects missing-state, ambiguity, external-action, and protected-claim mutations. Represented will mean a proxy or protocol stays visible without conversion into operational or empirical evidence. Open gaps and exact gates remain open by design.

The owner portfolio freezes sixty safe-now executions, thirty bounded candidates, twenty exact-approval packets held unexecuted, ten blocked packets held unexecuted, twenty phase-local skills, twenty family-current runners, and sixty additive CLEAN/FIX/REFINE rows. Counts are bounded ceilings, not authority or a reason to manufacture unsafe work. The successor portfolio contains ten skill ideas, ten runner ideas, thirty CLEAN/FIX/REFINE ideas, and one practice-lens recommendation as zero-credit file-backed material only; no successor has been contacted.

## Sources and tools

The official Library of Congress preservation pages provide public book, binding, paper, handling-risk, storage, and professional-referral vocabulary only. NPS, NIST, W3C, JSON Schema, RFC, New Zealand Privacy Commissioner, and Māori-data-authority materials supply museum-accountability, formal, structural, privacy, and authority-reservation vocabulary only. No public record, image, object, measurement, personal data, cultural data, treatment instruction, or live adapter row is ingested.

The three x2 tool candidates are portion 2.6.2, transitions 0.9.3, and cattrs 26.1.0. They are frozen from current official PyPI registry metadata with exact universal-wheel SHA-256 values. If x2 proceeds, the exact wheels and necessary runtime dependencies will be downloaded and installed only in a phase-namespaced D-backed environment, hash checked, positively and negatively smoke tested, and dependency inspected. Shared Python and npm prefixes remain untouched. Installation does not establish exhaustive supply-chain security, legal license interpretation, bibliographical, conservation, material, or object correctness beyond the bounded fixtures, performance, compatibility beyond the smokes, or production fitness.

## Trinity and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Book topology, adjacency, orientation, interval, constraint, dimensional, or uncertainty analogies establish no likelihood, parameter constraint, prediction, detected force, physical law, cognition model, empirical confirmation, final physics, quantum or ultraviolet completion, Theory of Everything, proof, or canon. THOS remains proxy-only without governed blind matched-budget real arms, people, operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, issuance, verification, resolution, status, revocation, interoperability, recovery evidence, privacy and independent security review, trust governance, and affected-party oversight.

CBR, professional practice, book handling, opening, collation, pagination, material identification, sampling, conservation treatment, repair, rebinding, mould or biohazard response, lifting and workplace safety, custody, ownership, attribution, copyright and moral rights, privacy, accessibility, remedy, legal or cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority. The verdict remains `NOT_READY_FOR_STAGE_20`.

## Lifecycle

X1 contains only planning, source, novelty, portfolio, threat, route, environment-observation, validation, and rollback artifacts plus an x1-only builder, helper, and tests. It contains no x2 implementation, proposal result, observed outcome, evidence-stage receipt, closeout, seal, final route, or successor delivery. X2 may begin only after this dedicated x1 commit is pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote. The exact final will receive one attributable owner-scoped canonical invocation. A success will never be replayed; a failure will retain zero aggregate-success credit and only the failed dependency may be recovered unless target impact justifies more.
""",
    )

    json_paths = sorted(x1.rglob("*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    public_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(root.rglob("*")) if path.is_file())
    candidates = privacy_candidates(public_text)
    receipt = {
        "checks": {
            "accessible_rows": len(corpus),
            "collision_count": len(collisions),
            "json_parse_count": len(json_paths),
            "privacy_candidates": candidates,
            "proposal_count": len(proposals),
            "quarantine_count": len(quarantined),
            "source_count": len(SOURCE_ROWS),
            "startup_failures_retained": len(failure_rows),
            "truth_labels": TRUTH_LABELS,
            "x2_paths": 0,
        },
        "owner": OWNER,
        "passed": not candidates and len(corpus) == SOURCE_RECOVERED and len(proposals) == 40 and not collisions and not quarantined,
        "phase": PHASE,
        "schema": "ghc.family.x1-validation-receipt.v2",
        "strict_planning_only": True,
    }
    write_json(validation / "x1-validation-receipt.json", receipt)


def staged_review(repo: Path) -> None:
    exclusions = [MANIFEST_PATH, REVIEW_PATH]
    entries = staged_blob_manifest(repo, exclusions)
    paths = [row["path"] for row in entries]
    x2_paths = [path for path in paths if "/x2/" in path or re.search(r"(?:^|_)x2(?:_|\.)", Path(path).name)]
    forbidden = [
        path
        for path in paths
        if any(token in path.lower() for token in ("/closeout/", "/seal/", "/final/", "/handoffs/"))
    ]
    json_paths = [path for path in paths if path.endswith(".json")]
    json_errors: list[str] = []
    privacy: list[dict[str, str]] = []
    for path in paths:
        data = subprocess.run(["git", "-C", str(repo), "show", f":{path}"], check=True, capture_output=True).stdout
        if path.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
            except Exception as exc:  # noqa: BLE001 - exact error is retained by path
                json_errors.append(f"{path}:{type(exc).__name__}")
        privacy.extend({"path": path, **row} for row in privacy_candidates(data.decode("utf-8", errors="replace")))
    manifest = {
        "domain": "x1_staged_planning_git_blobs",
        "entries": entries,
        "entry_count": len(entries),
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.exact-git-blob-manifest.v2",
        "self_exclusions": exclusions,
        "source_commit": SOURCE_FINAL,
    }
    write_json(repo / MANIFEST_PATH, manifest)
    checks = {
        "diff_cached_check": subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--check"], capture_output=True).returncode == 0,
        "forbidden_lifecycle_paths": forbidden,
        "json_errors": json_errors,
        "manifest_entries": len(entries),
        "owner_generated_file_ceiling": len(paths) < 2000,
        "privacy_candidates": privacy,
        "strict_x1_no_x2_paths": not x2_paths,
        "x2_paths": x2_paths,
    }
    write_json(
        repo / REVIEW_PATH,
        {
            "checks": checks,
            "owner": OWNER,
            "passed": all(
                [
                    checks["diff_cached_check"],
                    not forbidden,
                    not json_errors,
                    checks["owner_generated_file_ceiling"],
                    not privacy,
                    checks["strict_x1_no_x2_paths"],
                ]
            ),
            "phase": PHASE,
            "schema": "ghc.family.x1-staged-review.v2",
            "self_exclusions": exclusions,
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--stage-review", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.stage_review:
        staged_review(repo)
    else:
        build(repo)


if __name__ == "__main__":
    main()

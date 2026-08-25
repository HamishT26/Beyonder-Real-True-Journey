"""Build and validate the planning-only Neris Solane v669-v7 x1 packet."""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_neris_solane_v669_v7_archive import (
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
    SOURCE_CHAIN_DECLARED,
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

DATE = "2026-08-26"
TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
MANIFEST_PATH = "docs/neris-solane/v669-v7/validation/x1-manifest.json"
REVIEW_PATH = "docs/neris-solane/v669-v7/validation/x1-staged-review.json"

SOURCE_ROWS = [
    {
        "source_id": "OWNER-SYNTHETIC-SCHEMA",
        "url": None,
        "status": "current",
        "use": "owner-authored zero-person planning structures only",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "SMITHSONIAN-SLIDE-RULE-OBJECT",
        "url": "https://americanhistory.si.edu/collections/object/nmah_694438",
        "status": "current",
        "use": "public slide-rule object vocabulary only; no record, image, measurement, or Smithsonian endorsement",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "SMITHSONIAN-SLIDE-RULE-RESOURCES",
        "url": "https://americanhistory.si.edu/collections/object-groups/slide-rules/resources",
        "status": "current",
        "use": "public form, maker, material, and purpose vocabulary only; zero records or images ingested",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "SMITHSONIAN-TERMS-AND-METADATA",
        "url": "https://www.si.edu/termsofuse",
        "status": "watch",
        "use": "rights and metadata reservation only; no legal interpretation",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "CCI-INDUSTRIAL-COLLECTIONS",
        "url": "https://www.canada.ca/en/conservation-institute/services/care-objects/industrial-collections.html",
        "status": "current",
        "use": "industrial-object and mixed-material vocabulary with professional-action hold",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "CCI-METALS-CURRENT",
        "url": "https://www.canada.ca/en/conservation-institute/services/care-objects/metals.html",
        "status": "current",
        "use": "metal and corrosion vocabulary only; no treatment recommendation",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "CCI-HANDLING-HERITAGE-OBJECTS",
        "url": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/handling-heritage-objects.html",
        "status": "current",
        "use": "handling-risk reservation only; no handling authority",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "NPS-MUSEUM-HANDBOOK-2023",
        "url": "https://www.nps.gov/museum/publications/MHI/MHI.pdf",
        "status": "stable",
        "use": "preventive-conservation vocabulary only; no professional validation",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "NPS-METAL-OBJECT-CARE",
        "url": "https://www.nps.gov/museum/publications/MHI/Appendix%20O.pdf",
        "status": "stable",
        "use": "metal-object care vocabulary and referral boundary only",
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
        "source_id": "EXACT-ACTION-SPECIFIC-AUTHORITY",
        "url": None,
        "status": "watch",
        "use": "exact gate; competent action-specific authority absent",
        "data_rows_ingested": 0,
    },
]

STARTUP_FAILURES = [
    ("NS6697-X1-OP-001", "first PowerShell source inventory placed a pipeline directly after a foreach block", "an explicit result collection recovered the bounded inventory without repository mutation"),
    ("NS6697-X1-OP-002", "first ancestry projection embedded merge-base statements inside an object expression", "separate scalar parent probes verified the exact chain"),
    ("NS6697-X1-OP-003", "corrected combined ancestry wrapper returned no attributable output", "three literal parent probes plus bounded commit and merge counts supplied exact evidence"),
    ("NS6697-X1-OP-004", "combined authorization-state display exceeded the presentation window", "numbered bounded windows completed the same file through EOF"),
    ("NS6697-X1-OP-005", "first receipt filename search repeated the empty-pipeline grammar fault", "bounded session-event parsing resolved the original receipt path"),
    ("NS6697-X1-OP-006", "large source-task reread exceeded the useful display bound", "the committed activation packet and exact task anchors remained the authoritative bounded inputs"),
    ("NS6697-X1-OP-007", "broad validator-command search exceeded the model context", "line-wise JSON event parsing emitted only the matching invocation"),
    ("NS6697-X1-OP-008", "default session-file opening denied concurrent read sharing", "an explicit read-write-share FileStream recovered the same immutable event"),
    ("NS6697-X1-OP-009", "first bounded session parse still overflowed its display with unrelated matching source text", "the exact invocation row was isolated and the external receipt was rehashed directly"),
    ("NS6697-X1-OP-010", "independent manifest replay disposed its Git process before projecting the exit property", "all 666 exact byte lengths and SHA-256 values matched with empty stderr; the unobserved exit field remains unclaimed"),
    ("NS6697-X1-OP-011", "first source-script size inventory repeated the foreach pipeline parse fault", "an explicit rows variable produced exact line and byte counts"),
    ("NS6697-X1-OP-012", "multi-term full-tree Git title grep exceeded the bounded result window", "the two exact read-only helper processes were identified and stopped without repository mutation"),
    ("NS6697-X1-OP-013", "single-term full-tree Git title grep repeated the oversized scan", "the exact read-only helper pair was identified and stopped without repository mutation"),
    ("NS6697-X1-OP-014", "per-blob inherited-title helper exceeded its wrapper and lost output", "one alternating-request exact-length Git batch recovered 1540 rows from 54 hash-matching blobs"),
    ("NS6697-X1-OP-015", "recursive Git lock inventory exceeded its useful bound", "literal ref config packed-ref index and worktree lock probes replaced the broad scan"),
    ("NS6697-X1-OP-016", "first web-result projection omitted a string-form response", "the next bounded primary-source query projected the actual response type"),
    ("NS6697-X1-OP-017", "direct Smithsonian page opens returned transport-side internal errors", "current Smithsonian search results retained the object and resource pages without record ingestion"),
    ("NS6697-X1-OP-018", "worktree creation exceeded its initial result window", "the single live session was awaited through registration sparse setup and clean exact-head materialization without relaunch"),
    ("NS6697-X1-OP-019", "first forty-proposal slate placed fourteen inherited or within-slate titles above the similarity quarantine", "only the fourteen title dependencies were reframed while their frozen intent labels and gates remained unchanged"),
    ("NS6697-X1-OP-020", "first quarantined-neighbour projection failed at the Windows legacy console encoding boundary", "the same isolated diagnostic projected once with explicit UTF-8 and preserved the failed console witness"),
    ("NS6697-X1-OP-021", "the successful x1 test suite emitted a ResourceWarning for an unclosed Git batch stderr stream", "only the batch-helper stream closure changed and the isolated corpus-loader dependency passed with ResourceWarning promoted to error; the successful suite was not replayed"),
    ("NS6697-X1-OP-022", "first combined syntax and JSON probe ran from the control workspace instead of the Neris worktree", "only the working-directory dependency changed; the corrected scoped probe parsed the three Python files and all owner JSON without replaying tests"),
    ("NS6697-X1-OP-023", "first post-review summary embedded git diff and exit-code statements inside a PowerShell object expression", "separate command and scalar exit capture recovered the summary without replaying tests or source validation"),
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
            parents[SOURCE_EVIDENCE][1] == SOURCE_X1
            and parents[SOURCE_FINAL][1] == SOURCE_EVIDENCE
            and len(parents[SOURCE_X1]) == len(parents[SOURCE_EVIDENCE]) == len(parents[SOURCE_FINAL]) == 2
        ),
        "phase_commits": 3,
        "zero_merges": all(len(row) == 2 for row in parents.values()),
        "baton_git_blob_sha256": "7bfb240a518a76e2c97370a0ffe4382c04ab0afe878adb269600323b332b6841",
        "sender_canonical_receipt_declared_sha256": "4d118955275807182f81b62ae919cd8e8289204db327e21bca7f1cfb32e8a2ee",
        "sender_receipt_rehash_state": "exact_external_receipt_independently_rehashed",
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
            "boundary": "Forty genuinely new proposals are planning hypotheses only. Inherited evidence earns zero Neris novelty or completion credit.",
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
            "audit_scope": "exact committed accessible corpus plus within-slate comparisons",
            "declared_inherited_frozen_proposals": SOURCE_CHAIN_DECLARED,
            "exact_title_collisions": collisions,
            "maximum_neighbor": {"proposal_id": max_row["proposal_id"], "neighbor": max_row["semantic_neighbors"][0]},
            "new_proposals": len(proposals),
            "owner": OWNER,
            "phase": PHASE,
            "quarantine_threshold": 0.75,
            "quarantined_proposals": quarantined,
            "recovered_inherited_rows": SOURCE_RECOVERED,
            "schema": "ghc.family.semantic-novelty-audit.v2",
            "source_shards": source_shards,
            "unavailable_history_is_open_gap": True,
            "universal_novelty_claim": False,
            "unrecovered_declared_rows": SOURCE_UNRECOVERED,
        },
    )
    write_json(
        x1 / "source-ledger.json",
        {
            "boundary": "Official and primary sources supply vocabulary and constraints only; no records, images, objects, measurements, people, or authority are ingested.",
            "immutable_source": source_verification(repo),
            "network_transport_event_count": 0,
            "owner": OWNER,
            "phase": PHASE,
            "public_source_pages_reviewed": sum(row["url"] is not None for row in SOURCE_ROWS),
            "review_date": DATE,
            "schema": "ghc.family.source-ledger.v3",
            "sources": SOURCE_ROWS,
            "statuses": ["current", "stable", "draft", "watch"],
        },
    )
    rows = {
        "safe_now": portfolio_rows("safe_now", SAFE_TITLES, "safe_now"),
        "candidate": portfolio_rows("candidate", CANDIDATE_TITLES, "candidate"),
        "exact_approval": portfolio_rows("exact_approval", [f"held exact approval packet {i:02d}" for i in range(1, 11)], "exact_approval", "held_unexecuted"),
        "blocked": portfolio_rows("blocked", [f"blocked protected action packet {i:02d}" for i in range(1, 6)], "blocked", "held_unexecuted"),
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
        "safe_now": portfolio_rows("successor_safe_now", SAFE_TITLES[:20], "successor_safe_now", "recommended_not_executed"),
        "candidate": portfolio_rows("successor_candidate", CANDIDATE_TITLES, "successor_candidate", "recommended_not_executed"),
        "skill": portfolio_rows("successor_skill", SKILL_TITLES, "successor_skill", "recommended_not_executed"),
        "runner": portfolio_rows("successor_runner", RUNNER_TITLES, "successor_runner", "recommended_not_executed"),
        "clean_fix_refine": portfolio_rows("successor_clean_fix_refine", REFINE_TITLES, "successor_clean_fix_refine", "recommended_not_executed"),
    }
    write_json(
        x1 / "successor-recommendations-freeze.json",
        {
            "completion_credit": 0,
            "counts": {kind: len(items) for kind, items in successor.items()},
            "owner": OWNER,
            "phase": PHASE,
            "prospective_phase": "v669-v8",
            "prospective_successor": "UNRESOLVED_VESPER_EXACT_TITLE_CONFLICT",
            "route_binding": "recommendations_only_no_contact_no_delivery_exact_title_must_be_resolved_live",
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
                "rejected metronome after a direct accessible-title hit and rejected full-tree grep after bounded-cost failure",
                "selected synthetic historical slide-rule documentation after zero exact term hits across 1540 accessible rows",
                "kept the 3570-title semantic recovery gap visible",
                "selected Pint portion and uncertainties for isolated unit interval and uncertainty boundary smokes",
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
            "codex_cli": {"version": "0.149.0", "source": "inherited current bounded version receipt", "update": "not_performed"},
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
            "prospective_next_edge": "unresolved Vesper Rowan versus Vesper Arlen exact-title conflict for v669-v8; resolve only after exact terminal reread",
            "schema": "ghc.family.route-state.v2",
            "successor_contact_count": 0,
        },
    )
    write_text(
        x1 / "threat-model.md",
        """# Neris Solane v669-v7 x1 threat model

This planning-only threat model covers source or sibling-lane mutation, x1/x2 leakage, semantic duplication, private-route disclosure, false slide-rule, metrology, museum, conservation, or software-verification competence, operation or calculation instruction, scale or condition truth promotion, ownership and attribution conversion, manual-content disclosure, reproduction-rights overclaim, accessibility or privacy completeness, Māori-authority substitution, mathematical analogy conversion, THOS or Freed ID promotion, canonical replay, and premature successor delivery.

Controls are one additive D-first sparse lane; exact source anchors and Git-blob manifests; zero-person, zero-instrument, zero-measurement, zero-operation, zero-real-calculation, zero-treatment, zero-media, and zero-network-adapter counters; four exact truth labels; append-only Method Flow; exact protected gates; structurally accessible reporting with manual evaluation reserved; and one terminally gated route. Residual risks remain because same-owner synthetic checks cannot provide independent review, professional judgment, legal or cultural interpretation, affected-party legitimacy, Māori authority, privacy or accessibility completeness, production fitness, empirical GMUT evidence, or Stage 20 authority.
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
        f"""# Neris Solane v669-v7 x1 integrated planning overview

## Identity, purpose, and boundary

{IDENTITY_BOUNDARY} The phase role is calibration cartographer and reversible-scale steward. The hope is to make synthetic uncertainty and correction legible without turning a scale analogy into measurement or authority. THOS Body is primary through software-verification structure; GMUT Mind, CBR Heart, and nonproduction Freed ID remain explicit and protected. Museum documentation, metrology history, and software verification are bounded learning lenses only, not professions, qualifications, or services.

The bounded human-practice lens is wholly synthetic historical slide-rule cataloguing, scale-state, computation-trace, correction, and handover documentation. It uses zero real people, calculators, workers, donors, registrars, metrologists, conservators, slide rules, manuals, cases, scales, cursors, images, measurements, collection records, sites, handling events, operations, real calculations, cleaning, adjustments, repairs, treatments, safety decisions, rights decisions, cultural decisions, or external actions. It establishes no employment, qualification, slide-rule competence, metrology, registration or conservation competence, safety release, ownership, attribution, copyright, moral rights, privacy or accessibility completeness, legal or cultural interpretation, affected-party legitimacy, Māori authority, production fitness, deployment, or operational result.

## Source and novelty boundary

The immutable source is Elaren Kestrel's exact v669-v6 final `{SOURCE_FINAL}` with direct x1 and evidence ancestry preserved. The committed activation packet is an exact normalized-LF Git blob. Elaren's validation, tools, and source research remain inherited evidence with zero Neris credit. The sender's external canonical receipt was independently rehashed at its original D-backed path and matched the declared digest; it is not copied into this lane or converted into Neris validation credit.

The novelty audit reconstructs {SOURCE_RECOVERED} committed titles: Elaren's 1,540-row accessible corpus plus Elaren's forty frozen rows. The declared inherited chain is {SOURCE_CHAIN_DECLARED}. The remaining {SOURCE_UNRECOVERED} titles are an explicit recovery gap, so the phase makes no universal-novelty claim. A 54-blob exact-length batch screen found no exact slide-rule term in the 1,540-row precursor corpus and rejected metronome after one direct hit. Forty slide-rule proposals must still pass exact-title and 0.75 token-Jaccard quarantine checks against all {SOURCE_RECOVERED} accessible rows and each other.

## Frozen program

The forty genuinely new proposals are planning hypotheses only. Expected dispositions are exactly twenty-eight completed, eight represented, two open gaps, and two exact gates. Each completion-lane proposal freezes one bounded synthetic positive and four rejecting mutations. Completed will mean only that a local contract accepts its positive and rejects missing-state, ambiguity, external-action, and protected-claim mutations. Represented will mean a proxy or protocol stays visible without conversion into operational or empirical evidence. Open gaps and exact gates remain open by design.

The portfolio freezes thirty safe-now executions, fifteen bounded candidates, ten exact-approval packets held unexecuted, five blocked packets held unexecuted, ten phase-local skills, ten family-current runners, and thirty additive CLEAN/FIX/REFINE rows. Counts are bounded ceilings, not quotas. Nothing unsafe is manufactured to satisfy them. Successor recommendations are prepared as zero-credit file-backed ideas only; no successor has been contacted.

## Sources and tools

Official Smithsonian slide-rule object and resource pages provide public form, component, scale, maker, material, and purpose vocabulary only. Canadian Conservation Institute sources supply industrial-object, mixed-material, handling, and treatment-referral vocabulary. W3C, JSON Schema, RFC, NIST, New Zealand Privacy Commissioner, and Te Mana Raraunga materials supply formal, structural, unit, privacy, and authority-reservation vocabulary only. No public record, image, object, measurement, personal data, cultural data, or live adapter row is ingested.

The three x2 tool candidates are Pint 0.25.3, portion 2.6.2, and uncertainties 3.2.3. They are frozen from current official PyPI metadata with exact universal-wheel SHA-256 values; the yanked uncertainties 3.2.4 release is explicitly excluded. If x2 proceeds, candidates and dependencies will be downloaded and installed only in a phase-namespaced D-backed environment, hash checked, positively and negatively smoke tested, and dependency audited. Shared Python and npm prefixes remain untouched. Installation does not establish exhaustive supply-chain security, legal license interpretation, numerical correctness beyond the bounded fixtures, performance, compatibility beyond the smokes, or production fitness.

## Trinity and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Slide-rule logarithmic, interval, dimensional, or uncertainty analogies establish no likelihood, parameter constraint, prediction, detected force, physical law, cognition model, empirical confirmation, final physics, quantum or ultraviolet completion, Theory of Everything, proof, or canon. THOS remains proxy-only without governed blind matched-budget real arms, people, operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, issuance, verification, resolution, status, revocation, interoperability, recovery evidence, privacy and independent security review, trust governance, and affected-party oversight.

CBR, professional practice, slide-rule operation, real calculation, metrology, calibration, accuracy certification, treatment, chemical and lifting safety, workplace safety, custody, ownership, attribution, copyright and moral rights, privacy, accessibility, remedy, legal or cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority. The verdict remains `NOT_READY_FOR_STAGE_20`.

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

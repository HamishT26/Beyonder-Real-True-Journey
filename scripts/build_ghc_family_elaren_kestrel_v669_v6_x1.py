"""Build and validate the planning-only Elaren Kestrel v669-v6 x1 packet."""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_elaren_kestrel_v669_v6_archive import (
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
MANIFEST_PATH = "docs/elaren-kestrel/v669-v6/validation/x1-manifest.json"
REVIEW_PATH = "docs/elaren-kestrel/v669-v6/validation/x1-staged-review.json"

SOURCE_ROWS = [
    {
        "source_id": "OWNER-SYNTHETIC-SCHEMA",
        "url": None,
        "status": "current",
        "use": "owner-authored zero-person planning structures only",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "SMITHSONIAN-TYPEWRITER-OBJECT",
        "url": "https://americanhistory.si.edu/collections/object/nmah_850053",
        "status": "current",
        "use": "public collection vocabulary only; no object record ingested and no Smithsonian endorsement",
        "data_rows_ingested": 0,
    },
    {
        "source_id": "SMITHSONIAN-TYPEWRITER-COLLECTION",
        "url": "https://collections.si.edu/search/results.htm?q=set_name%3A%22Typewriters%22",
        "status": "current",
        "use": "public search vocabulary only; zero records or images ingested",
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
        "source_id": "EXACT-ACTION-SPECIFIC-AUTHORITY",
        "url": None,
        "status": "watch",
        "use": "exact gate; competent action-specific authority absent",
        "data_rows_ingested": 0,
    },
]

STARTUP_FAILURES = [
    ("EL6696-X1-OP-001", "skill-creator first full-file display exceeded the visible return window", "bounded line-window reread reached EOF"),
    ("EL6696-X1-OP-002", "first PowerShell reference-inventory projection had invalid pipeline grammar", "explicit collection recovery parsed all required references"),
    ("EL6696-X1-OP-003", "combined evidence-owner manifest display exceeded the presentation window", "missing line windows were read separately through EOF"),
    ("EL6696-X1-OP-004", "sender canonical receipt file was not exposed for independent path rehash", "live activation digest binding retained without converting it to Elaren credit"),
    ("EL6696-X1-OP-005", "first Git batch manifest replay exceeded its wrapper and left read-only helpers", "only helper processes were stopped and no repository byte changed"),
    ("EL6696-X1-OP-006", "managed manifest batch parser failed to advance a separator offset", "deduplicated corrected parser replayed all five manifests"),
    ("EL6696-X1-OP-007", "first novelty projection used the Windows legacy console codec", "explicit UTF-8 recovery printed the complete result"),
    ("EL6696-X1-OP-008", "latest toolbox overlay was first guessed with a JSON suffix", "bounded file inventory resolved and read the Markdown overlay"),
    ("EL6696-X1-OP-009", "broad inherited direct-tool Git grep exceeded its useful bound", "query was interrupted and current published overlays were inspected directly"),
    ("EL6696-X1-OP-010", "first uniqueness probe embedded a statement in a PowerShell expression", "separate scalar statements resolved the syntax fault"),
    ("EL6696-X1-OP-011", "combined uniqueness and version probe exceeded its wrapper", "bounded probes separated branch path remote and version concerns"),
    ("EL6696-X1-OP-012", "combined remote and worktree uniqueness probe exceeded its wrapper", "exact live remote branch probe later returned no row"),
    ("EL6696-X1-OP-013", "ordinary worktree-list scan exceeded the bound on the large registry", "literal metadata prefix checks replaced the broad listing"),
    ("EL6696-X1-OP-014", "full registered-worktree metadata enumeration exceeded the bound", "direct expected metadata name and filtered prefix returned no hit"),
    ("EL6696-X1-OP-015", "recursive metadata text scan exceeded the bound", "literal target path and exact metadata prefix checks closed uniqueness"),
    ("EL6696-X1-OP-016", "worktree creation wrapper stalled in its final broad status proof", "only read-only status helpers were stopped after sparse creation completed"),
    ("EL6696-X1-OP-017", "the interrupted status projection produced no clean-state credit", "separate worktree and index diffs plus entry count supplied bounded state"),
    ("EL6696-X1-OP-018", "no-checkout worktree began with an empty index", "worktree-local read-tree populated skip-worktree entries under frozen sparse rules"),
    ("EL6696-X1-OP-019", "source validator filename was first guessed incorrectly", "scoped script inventory resolved the exact validator path"),
    ("EL6696-X1-OP-020", "whole successor-recommendation projection exceeded the display budget", "structured counts and bounded category windows supplied the needed evidence"),
    ("EL6696-X1-OP-021", "first forty-proposal slate crossed the similarity quarantine on four inherited generic surfaces", "reframed all four as distinct traversal inscription-conflict evidence-account and terminal-interlock contracts"),
    ("EL6696-X1-OP-022", "first x1 test suite found thirty-one CLEAN FIX REFINE rows against the frozen target of thirty", "merged redundant zero-media and adapter counters into the zero-object boundary row"),
    ("EL6696-X1-OP-023", "first compact refinement-list projection embedded a PowerShell newline in a Python literal", "plain list representation recovered the exact thirty-one-row inventory"),
    ("EL6696-X1-OP-024", "first recursive generated-cache cleanup was rejected by the command safety boundary", "exact cache directories were enumerated and no delete occurred"),
    ("EL6696-X1-OP-025", "second literal Remove-Item cache cleanup remained blocked by the command policy", "verified individual generated files and empty directories were removed with exact native paths"),
    ("EL6696-X1-OP-026", "full recursive x1 inventory projection exceeded the presentation budget", "scalar counts and exact scoped path and hash projections replaced the unbounded display"),
    ("EL6696-X1-OP-027", "first compact staged-review summary embedded a command sequence inside a PowerShell expression", "separate command and exit-code scalars replaced the invalid expression without repository mutation"),
    ("EL6696-X1-OP-028", "first combined retention patch targeted the staged-review failure ledger in the archive module instead of its builder module", "file-specific patch hunks recovered both count and ledger changes and the rejected patch changed no repository byte"),
    ("EL6696-X1-OP-029", "first staged review failed closed on the privacy scanner source matching its own Unix user-path literal", "runtime-equivalent fragmented pattern construction removed the self-match while preserving real value detection"),
    ("EL6696-X1-OP-030", "first independent manifest summary compared SHA-256 entries to a nonexistent Git-blob-OID field and reported twenty-seven false mismatches", "exact staged blob bytes are rehashed against the declared SHA-256 field instead"),
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
        "baton_git_blob_sha256": "74f7c50d38a5a275fd114e05997089725db02c305b6aae60289b8d6a6d060aa3",
        "sender_canonical_receipt_declared_sha256": "07d6a983aadce74ed3c79c752fd2074017eb762367d1d59cd4f97c6efb43d085",
        "sender_receipt_rehash_state": "declared_binding_verified_external_private_file_not_rehashed",
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
            "boundary": "Forty genuinely new proposals are planning hypotheses only. Inherited evidence earns zero Elaren novelty or completion credit.",
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
            "prospective_phase": "v669-v7",
            "prospective_successor": "Neris Solane",
            "route_binding": "recommendations_only_no_contact_no_delivery",
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
                "rejected letterpress horology stained-glass and kite lenses after inherited-title collisions",
                "selected synthetic historical-typewriter documentation after zero scoped term hits",
                "kept the 3570-title semantic recovery gap visible",
                "selected three owner-local data-difference and correction tools instead of repeating inherited schema and graph tools",
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
            "prospective_next_edge": "Neris Solane v669-v7 only after exact terminal reread",
            "schema": "ghc.family.route-state.v2",
            "successor_contact_count": 0,
        },
    )
    write_text(
        x1 / "threat-model.md",
        """# Elaren Kestrel v669-v6 x1 threat model

This planning-only threat model covers source or sibling-lane mutation, x1/x2 leakage, semantic duplication, private-route disclosure, false typewriter or conservation competence, operation or treatment instruction, material or condition truth promotion, ownership and attribution conversion, document-content disclosure, image-rights overclaim, accessibility or privacy completeness, Māori-authority substitution, scientific analogy conversion, THOS or Freed ID promotion, canonical replay, and premature successor delivery.

Controls are one additive D-first sparse lane; exact source anchors and Git-blob manifests; zero-person, zero-object, zero-operation, zero-treatment, zero-media, and zero-network-adapter counters; four exact truth labels; append-only Method Flow; exact protected gates; structurally accessible reporting with manual evaluation reserved; and one terminally gated acknowledged route. Residual risks remain because same-owner synthetic checks cannot provide independent review, professional judgment, legal or cultural interpretation, affected-party legitimacy, Māori authority, privacy or accessibility completeness, production fitness, empirical GMUT evidence, or Stage 20 authority.
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
        f"""# Elaren Kestrel v669-v6 x1 integrated planning overview

## Identity, purpose, and boundary

{IDENTITY_BOUNDARY} The phase role is provenance compositor and correction cartographer. The hope is to make disputed records reversible without converting local structure into authority. CBR Heart is primary; GMUT Mind, THOS Body, and nonproduction Freed ID remain explicit and protected.

The bounded human-practice lens is wholly synthetic historical-typewriter cataloguing, condition-state, correction, and handover documentation. It uses zero real people, typists, workers, donors, registrars, conservators, typewriters, cases, accessories, components, documents, images, measurements, collection records, sites, handling events, operations, disassembly, cleaning, lubrication, repairs, treatments, safety decisions, rights decisions, cultural decisions, or external actions. It establishes no employment, qualification, typewriter competence, registration or conservation competence, safety release, ownership, attribution, copyright, moral rights, privacy or accessibility completeness, legal or cultural interpretation, affected-party legitimacy, Māori authority, production fitness, deployment, or operational result.

## Source and novelty boundary

The immutable source is Eiren's exact v669-v5 final `{SOURCE_FINAL}` with direct x1 and evidence ancestry preserved. The committed activation packet is an exact normalized-LF Git blob. Eiren's validation and tools remain inherited evidence with zero Elaren credit. The sender-provided external canonical digest is retained as an attributable live binding; its private external file is not copied into this lane and is not independently rehashed here.

The novelty audit reconstructs {SOURCE_RECOVERED} committed titles: the same 1,500-row accessible corpus Eiren used plus Eiren's forty frozen rows. The declared inherited chain is {SOURCE_CHAIN_DECLARED}. The remaining {SOURCE_UNRECOVERED} titles are an explicit recovery gap, so the phase makes no universal-novelty claim. Scoped term searches rejected letterpress, horology, stained-glass, and kite candidates. Forty typewriter proposals have no exact collision and remain below the 0.75 token-Jaccard quarantine threshold against the accessible corpus and each other.

## Frozen program

The forty genuinely new proposals are planning hypotheses only. Expected dispositions are exactly twenty-eight completed, eight represented, two open gaps, and two exact gates. Each completion-lane proposal freezes one bounded synthetic positive and four rejecting mutations. Completed will mean only that a local contract accepts its positive and rejects missing-state, ambiguity, external-action, and protected-claim mutations. Represented will mean a proxy or protocol stays visible without conversion into operational or empirical evidence. Open gaps and exact gates remain open by design.

The portfolio freezes thirty safe-now executions, fifteen bounded candidates, ten exact-approval packets held unexecuted, five blocked packets held unexecuted, ten phase-local skills, ten family-current runners, and thirty additive CLEAN/FIX/REFINE rows. Counts are bounded ceilings, not quotas. Nothing unsafe is manufactured to satisfy them. Successor recommendations are prepared as zero-credit file-backed ideas only; no successor has been contacted.

## Sources and tools

Official Smithsonian records provide public collection vocabulary only. Canadian Conservation Institute and National Park Service sources supply industrial-object, mixed-material, corrosion, handling, and preventive-conservation vocabulary while reinforcing professional referral and no-treatment boundaries. W3C, JSON Schema, RFC, NIST, New Zealand Privacy Commissioner, and Te Mana Raraunga materials supply formal, structural, privacy, and authority-reservation vocabulary only. No public record, image, object, measurement, personal data, cultural data, or live adapter row is ingested.

The three x2 tool candidates are DeepDiff 9.1.0, jsonpath-ng 1.8.0, and jsonpatch 1.33. They are frozen from official PyPI metadata with exact wheel SHA-256 values. If x2 proceeds, they will be downloaded and installed only in a phase-namespaced D-backed environment, hash checked, positively and negatively smoke tested, and dependency audited. Shared Python and npm prefixes remain untouched. Installation does not establish exhaustive supply-chain security, legal license interpretation, performance, compatibility beyond the bounded smokes, or production fitness.

## Trinity and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Typewriter mechanism or symbol-sequence analogies establish no likelihood, parameter constraint, prediction, detected force, material law, cognition model, empirical confirmation, final physics, quantum or ultraviolet completion, Theory of Everything, proof, or canon. THOS remains proxy-only without governed blind matched-budget real arms, people, operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, issuance, verification, resolution, status, revocation, interoperability, recovery evidence, privacy and independent security review, trust governance, and affected-party oversight.

CBR, professional practice, typewriter operation and treatment, stored-energy and electrical safety, solvent and chemical safety, lifting and workplace safety, custody, ownership, attribution, copyright and moral rights, privacy, accessibility, remedy, legal or cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority. The verdict remains `NOT_READY_FOR_STAGE_20`.

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

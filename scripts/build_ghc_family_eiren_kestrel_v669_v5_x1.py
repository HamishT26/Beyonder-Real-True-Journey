"""Build the planning-only Eiren Kestrel v669-v5 x1 freeze."""

from __future__ import annotations

import argparse
import platform
import subprocess
from pathlib import Path

from ghc_family_eiren_kestrel_v669_v5_archive import (
    CANDIDATE_TITLES,
    CHAIN_AFTER,
    IDENTITY_BOUNDARY,
    INHERITED_ACTIVATION_BASELINE,
    OWNER,
    OWNER_ROOT,
    PHASE,
    REFINE_TITLES,
    RUNNER_TITLES,
    SAFE_TITLES,
    SEALED_CAELEN_COUNTS,
    SKILL_TITLES,
    SOURCE_BRANCH,
    SOURCE_CHAIN_DECLARED,
    SOURCE_FINAL,
    SOURCE_RECOVERED,
    SOURCE_UNRECOVERED,
    STARTUP_EFFECTIVE_BASELINE,
    STARTUP_FAILURE_COUNT,
    TOOL_CANDIDATES,
    inherited_title_corpus,
    owner_file_manifest,
    portfolio_rows,
    proposal_rows,
    staged_blob_manifest,
    write_json,
    write_text,
)

STARTUP_FAILURES = [
    (
        "EK6695-STARTUP-001",
        "parallel required-reference reader omitted literal paths",
        "The first PowerShell projection used positional arguments that were never supplied, so every bounded read resolved to a null path.",
        "Retained the failed wrapper and reread every required skill with exact literal paths through EOF.",
    ),
    (
        "EK6695-STARTUP-002",
        "combined small-reference presentation exceeded its output budget",
        "One grouped schema and overlay read was truncated before all attributable text was shown.",
        "Reread the same current references in smaller named groups without skipping any file.",
    ),
    (
        "EK6695-STARTUP-003",
        "authorization state presentation truncated its middle",
        "The complete current authorization state did not fit one presentation window.",
        "Reread the exact file in ordered 200-line windows through EOF and preserved the newer live assignment.",
    ),
    (
        "EK6695-STARTUP-004",
        "broad receipt search exceeded the output budget",
        "A repository-wide receipt search produced a truncated projection that could not prove the exact Caelen receipts.",
        "Restricted the search to the exact owner and phase receipt roots, then hashed and read both exact receipts.",
    ),
    (
        "EK6695-STARTUP-005",
        "PowerShell foreach pipeline parser fault",
        "Piping directly after a foreach block produced an empty-pipe parser error before the inventory ran.",
        "Materialized the rows first and serialized the bounded inventory only after collection.",
    ),
    (
        "EK6695-STARTUP-006",
        "sparse working-tree corpus assumption failed",
        "The first novelty screen attempted to open inherited title shards that were tracked but intentionally not materialized.",
        "Parsed the same exact immutable Git blobs without expanding or mutating the sparse checkout.",
    ),
    (
        "EK6695-STARTUP-007",
        "legacy console encoding rejected a Māori character",
        "The exact-blob novelty screen parsed successfully but CP1252 presentation could not encode one character.",
        "Re-emitted only the bounded JSON projection with ASCII escapes and retained the exact Unicode source data.",
    ),
    (
        "EK6695-STARTUP-008",
        "structural rg expression was over-composed",
        "The first combined constant and title regular expression had an unclosed group and did not execute.",
        "Used a simpler top-level constant and function pattern for the same bounded builder inspection.",
    ),
    (
        "EK6695-STARTUP-009",
        "prior Eiren documentation path was assumed but absent",
        "An exact tree lookup guessed a prior docs/eiren-kestrel directory that is not present in this immutable source.",
        "Used a bounded tree-name filter, found no prior Eiren owner surface, and remastered the current family builders instead.",
    ),
    (
        "EK6695-X1-010",
        "first proposal freeze hit semantic quarantine",
        "Three draft titles scored at or above 0.75 because they reused predecessor correction, zero-key envelope, and contestability boilerplate with only the practice noun changed.",
        "Inspected only the three nearest-neighbour records, retained the stopped freeze at zero credit, and replaced them with distinct bitemporal challenge, nonproduction claim-graph, and affected-neighbour ladder hypotheses.",
    ),
    (
        "EK6695-X1-011",
        "first mypy gate inferred mixed neighbour dictionaries as object",
        "The exact no-incremental mypy check reported two invalid numeric operations because the ranked neighbour dictionaries had no explicit value annotation.",
        "Annotated the ranked collection as dictionaries with explicit Any values and reran only the failed mypy dependency.",
    ),
    (
        "EK6695-X1-012",
        "first Bandit wrapper assumed a profile-only environment variable",
        "The non-login shell had no GHC_FAMILY_PYTHON variable, so the wrapper stopped before Bandit executed.",
        "Resolved the current D-backed Bandit command from a fresh profile session and invoked its sibling Python directly for the same bounded files.",
    ),
    (
        "EK6695-X1-013",
        "default Bandit profile flagged fixed no-shell subprocess calls",
        "Bandit reported eleven low-severity B404, B603, and B607 findings for owner-controlled Git and version commands, with zero medium or high findings.",
        "Reviewed the exact fixed-list calls, retained the default result, reran only Bandit with those three documented low-signal rules excluded, and kept the independent AST security review mandatory for x2.",
    ),
    (
        "EK6695-X1-014",
        "first staged privacy scan self-matched two scanner-definition literals",
        "The five-class staged Git-blob scan found only two contiguous Unix home-root strings inside the x1 test's own private-path pattern definition.",
        "Retained both candidates as scanner-definition self-matches, split only those source literals, and reran the same staged scan with zero confirmed payload hits.",
    ),
    (
        "EK6695-X1-015",
        "privacy recurrence guard missed the retained-failure prose",
        "The first scanner-definition recovery repeated both prohibited Unix home-root examples contiguously inside its own retained failure row.",
        "Reworded the retained row without literal path tokens and reran the same exact staged five-class scan.",
    ),
]


def run(repo: Path, *args: str) -> str:
    return subprocess.run(args, cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    corpus, corpus_sources = inherited_title_corpus(repo)
    if len(corpus) != SOURCE_RECOVERED:
        raise RuntimeError(f"accessible corpus mismatch: {len(corpus)} != {SOURCE_RECOVERED}")
    proposals = proposal_rows(corpus)
    if len(proposals) != 40:
        raise RuntimeError("proposal count must be exactly 40")
    collisions = [row["proposal_id"] for row in proposals if row["visible_title_collision"]]
    quarantined = [row["proposal_id"] for row in proposals if row["semantic_neighbor_quarantined"]]
    if collisions:
        raise RuntimeError(f"proposal title collisions: {collisions}")
    if quarantined:
        raise RuntimeError(f"semantic quarantine required: {quarantined}")

    shards: list[str] = []
    for start in range(0, 40, 5):
        rel = f"docs/eiren-kestrel/v669-v5/x1/proposal-freeze-shards/proposals-{start // 5 + 1:02d}.json"
        write_json(repo / rel, {"schema": "ghc.family.proposal-shard.v2", "rows": proposals[start : start + 5]})
        shards.append(rel)

    maximum = max(
        ({"proposal_id": row["proposal_id"], "neighbor": row["semantic_neighbors"][0]} for row in proposals),
        key=lambda item: item["neighbor"]["score"],
    )
    write_json(
        root / "x1/semantic-novelty-audit.json",
        {
            "schema": "ghc.family.semantic-novelty-audit.v2",
            "owner": OWNER,
            "phase": PHASE,
            "audit_scope": "exact accessible inherited title corpus only",
            "declared_inherited_frozen_proposals": SOURCE_CHAIN_DECLARED,
            "accessible_comparison_rows": len(corpus),
            "recovered_inherited_rows": len(corpus),
            "unrecovered_declared_rows": SOURCE_UNRECOVERED,
            "unavailable_history_is_open_gap": True,
            "universal_novelty_claim": False,
            "source_shards": corpus_sources,
            "new_proposals": 40,
            "exact_title_collisions": 0,
            "quarantine_threshold": 0.75,
            "quarantined_proposals": 0,
            "maximum_neighbor": maximum,
        },
    )
    write_json(
        root / "x1/proposal-freeze.json",
        {
            "schema": "ghc.family.proposal-freeze.v2",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_before": SOURCE_CHAIN_DECLARED,
            "proposal_chain_after": CHAIN_AFTER,
            "proposal_count": 40,
            "mutation_count": 160,
            "expected_outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "strict_x1_only": True,
            "boundary": "Planning-only freeze; no x2 implementation, observed outcome, installation, or completion credit.",
            "shards": shards,
        },
    )

    portfolios = {
        "safe_now": portfolio_rows("safe", SAFE_TITLES, "safe_now"),
        "candidate": portfolio_rows("candidate", CANDIDATE_TITLES, "candidate"),
        "skill": portfolio_rows("skill", SKILL_TITLES, "phase_local_skill"),
        "runner": portfolio_rows("runner", RUNNER_TITLES, "family_current_runner"),
        "clean_fix_refine": portfolio_rows("refine", REFINE_TITLES, "safe_now_clean_fix_refine"),
        "exact_approval": portfolio_rows(
            "exact",
            [f"held exact-approval packet {index:02d}" for index in range(1, 11)],
            "exact_approval",
            "held_unexecuted",
        ),
        "blocked": portfolio_rows(
            "blocked",
            [f"held blocked packet {index:02d}" for index in range(1, 6)],
            "blocked",
            "held_unexecuted",
        ),
    }
    write_json(
        root / "x1/portfolio-freeze.json",
        {
            "schema": "ghc.family.portfolio-freeze.v2",
            "owner": OWNER,
            "phase": PHASE,
            "counts": {key: len(value) for key, value in portfolios.items()},
            "rows": portfolios,
            "x1_completion_credit": 0,
            "boundary": "Planning only. Exact-approval and blocked packets remain held and unexecuted.",
        },
    )

    successor = {
        "safe_now": SAFE_TITLES[:20],
        "candidate": CANDIDATE_TITLES,
        "skill": SKILL_TITLES,
        "runner": RUNNER_TITLES,
        "clean_fix_refine": REFINE_TITLES,
    }
    write_json(
        root / "x1/successor-recommendations-freeze.json",
        {
            "schema": "ghc.family.successor-recommendations.v2",
            "owner": OWNER,
            "phase": PHASE,
            "prospective_successor": "Elaren Kestrel",
            "prospective_phase": "v669-v6",
            "counts": {key: len(value) for key, value in successor.items()},
            "rows": {
                key: portfolio_rows(f"succ-{key}", titles, f"successor_{key}", "recommended_not_executed")
                for key, titles in successor.items()
            },
            "completion_credit": 0,
            "route_binding": False,
        },
    )

    sources = [
        {
            "source_id": "OWNER-SYNTHETIC-SCHEMA",
            "status": "owner_authored_synthetic",
            "public_url": None,
            "data_rows_ingested": 0,
        },
        {
            "source_id": "MPI-BEE-BIOSECURITY-CURRENT",
            "status": "official_page_reviewed_vocabulary_only",
            "public_url": "https://www.mpi.govt.nz/biosecurity/how-to-find-report-and-prevent-pests-and-diseases/bee-biosecurity/bee-pests-and-diseases",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "MPI-AFB-GROUND-RULES-2025",
            "status": "official_current_rule_summary_reviewed_vocabulary_only",
            "public_url": "https://www.groundrules.mpi.govt.nz/rule/2832-american-foulbrood-pest-management-plan",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "WOAH-BEE-DISEASES-CURRENT",
            "status": "official_intergovernmental_page_reviewed_vocabulary_only",
            "public_url": "https://www.woah.org/en/disease/diseases-of-bees/",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "FAO-GOOD-BEEKEEPING-2021",
            "status": "official_publication_reviewed_vocabulary_only",
            "public_url": "https://openknowledge.fao.org/3/cb5353en/cb5353en.pdf",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "W3C-PROV-O-PUBLIC-VOCABULARY",
            "status": "official_recommendation_reviewed_vocabulary_only",
            "public_url": "https://www.w3.org/TR/prov-o/",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "JSON-SCHEMA-2020-12",
            "status": "official_specification_reviewed_structure_only",
            "public_url": "https://json-schema.org/draft/2020-12",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "W3C-WCAG-2.2-CURRENT",
            "status": "official_recommendation_reviewed_structure_only",
            "public_url": "https://www.w3.org/TR/WCAG22/",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "NZ-PRIVACY-CURRENT",
            "status": "official_page_reviewed_vocabulary_only",
            "public_url": "https://www.privacy.org.nz/privacy-principles/",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "OTHER-CURRENT-PRIMARY-SOURCES",
            "status": "review_required_before_any_bounded_use",
            "public_url": None,
            "data_rows_ingested": 0,
        },
        {
            "source_id": "REAL-GOVERNED-HUMAN-EVALUATION-REQUIRED",
            "status": "open_gap",
            "public_url": None,
            "data_rows_ingested": 0,
        },
        {
            "source_id": "EXACT-ACTION-SPECIFIC-AUTHORITY-REQUIRED",
            "status": "exact_gate",
            "public_url": None,
            "data_rows_ingested": 0,
        },
    ]
    write_json(
        root / "x1/source-ledger.json",
        {
            "schema": "ghc.family.source-ledger.v3",
            "owner": OWNER,
            "phase": PHASE,
            "immutable_source": {"branch": SOURCE_BRANCH, "final": SOURCE_FINAL},
            "review_date": "2026-08-25",
            "public_source_pages_reviewed": 8,
            "network_transport_event_count": "not_claimed",
            "sources": sources,
            "boundary": "Public vocabulary review is not observation, endorsement, instruction, competence, conformance, or authority.",
        },
    )

    write_json(
        root / "x1/tool-candidate-freeze.json",
        {
            "schema": "ghc.family.tool-candidate-freeze.v1",
            "owner": OWNER,
            "phase": PHASE,
            "target_count": 3,
            "selected": TOOL_CANDIDATES,
            "installation_state": "not_started_x1",
            "install_location_plan": "D_drive_owner_versioned_isolated_environment",
            "installation_mode": "fresh_D_backed_Python_virtual_environment_with_exact_direct_wheels",
            "required_x2_gates": [
                "exact direct wheel hashes and official registry metadata",
                "runtime compatibility",
                "dated dependency audit",
                "positive and rejecting smoke",
                "rollback limited to the owner versioned environment",
            ],
            "nonselected": [
                {
                    "name": "pydantic-jsonschema",
                    "version_reviewed": "0.0.13",
                    "state": "not_selected",
                    "reason": "A young reverse-schema conversion surface was unnecessary because direct JSON Schema and Pydantic validation cover the bounded contracts with less novelty and dependency risk.",
                    "completion_credit": 0,
                }
            ],
            "boundary": "Three is a safety-bounded target, not permission to install filler or claim production fitness.",
        },
    )

    startup_rows = [
        {
            "failure_id": failure_id,
            "title": title,
            "failure_signature": observed,
            "completion_credit": 0,
            "repository_bytes_changed": 0,
            "bounded_recovery": recovery,
            "failed_witness_retained": True,
            "recovery_witness_state": "bounded_pass",
        }
        for failure_id, title, observed, recovery in STARTUP_FAILURES
    ]
    if len(startup_rows) != STARTUP_FAILURE_COUNT:
        raise RuntimeError("startup failure count mismatch")
    write_json(
        root / "x1/startup-operational-failures.json",
        {
            "schema": "ghc.family.operational-failure-overlay.v2",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_activation_baseline": INHERITED_ACTIVATION_BASELINE,
            "failure_count": len(startup_rows),
            "bounded_recovery_witness_count": len(startup_rows),
            "effective_startup_baseline": STARTUP_EFFECTIVE_BASELINE,
            "rows": startup_rows,
            "boundary": "Every failed presentation or parser attempt has zero success credit; recoveries do not erase failures.",
        },
    )

    write_json(
        root / "x1/workflow-plan-freeze.json",
        {
            "schema": "ghc.family.workflow-plan.v3",
            "owner": OWNER,
            "phase": PHASE,
            "strict_x1_before_x2": True,
            "plan": [
                {"step": "source_skill_and_startup_gate", "status": "completed_read_only"},
                {"step": "planning_only_x1", "status": "in_progress"},
                {"step": "x1_push_and_four_way_equality", "status": "pending"},
                {"step": "bounded_x2_execution", "status": "pending"},
                {"step": "exact_final_closeout", "status": "pending"},
            ],
            "file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "commit_ceiling": 8,
            "full_repository_suite": "Eiren_owned_but_not_yet_dependency_justified",
            "canonical_validation": "one owner-scoped exact-final invocation after prerequisites",
        },
    )
    write_json(
        root / "x1/reflection-plan.json",
        {
            "schema": "ghc.family.reflection-plan.v2",
            "owner": OWNER,
            "phase": PHASE,
            "relational_role": "colony-record boundary weaver and reversible handover steward",
            "hope": "make every synthetic colony record legible reversible and honest at its authority boundary",
            "pronouns": "they/them",
            "identity_boundary": IDENTITY_BOUNDARY,
            "primary_pillar": "THOS Body",
            "bounded_practice": "synthetic apiary-inspection and colony-event documentation",
            "decisions": [
                "preserve the 3570-row unavailable-history gap",
                "keep every real person apiary colony hive bee observation sample inspection treatment action and authority at zero",
                "use public sources only for bounded vocabulary and refusal conditions",
                "retain failures and retry only failed dependencies",
            ],
        },
    )
    write_json(
        root / "x1/route-state.json",
        {
            "schema": "ghc.family.route-state.v3",
            "owner": OWNER,
            "phase": PHASE,
            "current_state": "ACTIVATION_ACKNOWLEDGED_ACTIVE_TERMINAL_GATE_UNMET",
            "prospective_successor": "Elaren Kestrel",
            "prospective_phase": "v669-v6",
            "sent": False,
            "precontacted": False,
            "standby_contacted": False,
            "binding": "newest live roster and authorization must be reread after the exact terminal gate",
        },
    )
    write_json(
        root / "x1/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v3",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x1_planning_only",
            "identity_boundary": IDENTITY_BOUNDARY,
            "sealed_caelen_counts": SEALED_CAELEN_COUNTS,
            "inherited_activation_baseline": INHERITED_ACTIVATION_BASELINE,
            "startup_effective_baseline": STARTUP_EFFECTIVE_BASELINE,
            "proposal_chain_before": SOURCE_CHAIN_DECLARED,
            "proposal_chain_after_planned": CHAIN_AFTER,
            "planned_proposals": 40,
            "observed_outcomes": None,
            "tool_installations": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_validation": "not_run_x1",
            "full_repository_suite": "not_run_x1_Eiren_owned_pending_dependency_gate",
        },
    )

    versions = {
        "schema": "ghc.family.tool-versions.v2",
        "python": platform.python_version(),
        "git": run(repo, "git", "--version"),
        "node": run(repo, "node", "--version"),
        "npm": run(repo, "npm.cmd", "--version"),
        "codex": run(repo, "codex.cmd", "--version"),
        "npm_prefix_drive": run(repo, "npm.cmd", "config", "get", "prefix")[:1].upper(),
        "platform": platform.system(),
        "updates_or_installs": 0,
    }
    write_json(root / "x1/tool-versions.json", versions)

    write_text(
        root / "x1/threat-model.md",
        """# Eiren Kestrel v669-v5 x1 threat model

This planning-only phase treats route drift, inaccessible-history overclaim, proposal collision, x1/x2 mixing, real apiary inspection or hive handling, pest or disease inference, sampling, treatment, destruction, reporting, food-safety or biosecurity instruction, land-access or privacy inference, package supply-chain drift, protected identifiers, cultural or Māori-authority overreach, validation replay, sibling-lane mutation, and Stage 20 promotion as threats.

Controls are exact-source anchoring, an accessible-corpus-only novelty audit, public-source vocabulary firewalls, strict lifecycle separation, a D-first sparse owner lane, exact direct-wheel pins in a fresh isolated environment, the four outcome labels, retained failures, smallest-dependency recovery, exact Git-blob manifests, five-class privacy scanning, and terminal nonpromotion.
""",
    )
    write_text(
        root / "x1/accessible-report-plan.md",
        """# Accessible report plan

Use a language declaration, skip link, one main landmark, ordered headings, captions, scoped table headers, plain-language summaries, and text-only relationships. Manual browser, keyboard, touch, zoom, reflow, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Structural checks cannot establish accessibility completeness.
""",
    )
    write_text(
        root / "x1/integrated-overview.md",
        f"""# Eiren Kestrel v669-v5 planning freeze

{IDENTITY_BOUNDARY}

## Scope

THOS Body is primary through a wholly synthetic apiary-inspection and colony-event documentation lens. GMUT Mind and Freed ID with CBR Heart remain visible and protected. This x1 freezes forty proposals and no observed outcome. It performs no inspection, handling, movement, sampling, diagnosis, treatment, destruction, notification, food-production, professional, safety, identity, legal, cultural, affected-party, or authority action.

## Novelty boundary

The declared inherited chain contains 5,070 rows. Exact committed shards expose 1,500 titles for bounded comparison, including Caelen's forty. The remaining 3,570 declared rows remain an explicit semantic-audit recovery gap. The Eiren titles have no exact collision and remain below the token-Jaccard quarantine threshold only within the accessible corpus. No universal novelty claim is made.

## Sources and tools

Eight current official or primary pages were reviewed only for vocabulary, structure, and refusal conditions: MPI bee biosecurity, MPI AFB ground rules, WOAH bee diseases, FAO good beekeeping practices, W3C PROV-O, JSON Schema 2020-12, WCAG 2.2, and the New Zealand Privacy Commissioner. Three exact Python package candidates are frozen for later isolated D-drive review: jsonschema 4.26.0, Pydantic 2.13.4, and NetworkX 3.6.1. No package is installed in x1, and no public citation supplies observation, diagnosis, instruction, endorsement, professional competence, conformance, legal interpretation, cultural ratification, or authority.

## Lifecycle

The freeze contains proposal, portfolio, source, tool-candidate, startup-failure, threat, route, and validation plans only. It must be committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before x2. Terminal verdict remains NOT_READY_FOR_STAGE_20.
""",
    )

    exclusions = [
        "docs/eiren-kestrel/v669-v5/validation/x1-manifest.json",
        "docs/eiren-kestrel/v669-v5/validation/x1-staged-review.json",
    ]
    entries = owner_file_manifest(repo, exclusions)
    write_json(
        root / "validation/x1-manifest.json",
        {
            "schema": "ghc.family.content-manifest.v2",
            "owner": OWNER,
            "phase": PHASE,
            "domain": "x1_working_tree_bytes_before_commit",
            "source_commit": SOURCE_FINAL,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def resume_tail(repo: Path) -> None:
    """Resume only the files that follow the retained Windows shim failure."""

    root = repo / OWNER_ROOT
    startup_rows = [
        {
            "failure_id": failure_id,
            "title": title,
            "failure_signature": observed,
            "completion_credit": 0,
            "repository_bytes_changed": 0,
            "bounded_recovery": recovery,
            "failed_witness_retained": True,
            "recovery_witness_state": "bounded_pass",
        }
        for failure_id, title, observed, recovery in STARTUP_FAILURES
    ]
    if len(startup_rows) != STARTUP_FAILURE_COUNT:
        raise RuntimeError("startup failure count mismatch")
    write_json(
        root / "x1/startup-operational-failures.json",
        {
            "schema": "ghc.family.operational-failure-overlay.v2",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_activation_baseline": INHERITED_ACTIVATION_BASELINE,
            "failure_count": len(startup_rows),
            "bounded_recovery_witness_count": len(startup_rows),
            "effective_startup_baseline": STARTUP_EFFECTIVE_BASELINE,
            "rows": startup_rows,
            "boundary": "Every failed presentation or parser attempt has zero success credit; recoveries do not erase failures.",
        },
    )
    write_json(
        root / "x1/tool-versions.json",
        {
            "schema": "ghc.family.tool-versions.v2",
            "python": platform.python_version(),
            "git": run(repo, "git", "--version"),
            "node": run(repo, "node", "--version"),
            "npm": run(repo, "npm.cmd", "--version"),
            "codex": run(repo, "codex.cmd", "--version"),
            "npm_prefix_drive": run(repo, "npm.cmd", "config", "get", "prefix")[:1].upper(),
            "platform": platform.system(),
            "updates_or_installs": 0,
        },
    )
    write_text(
        root / "x1/threat-model.md",
        """# Eiren Kestrel v669-v5 x1 threat model

This planning-only phase treats route drift, inaccessible-history overclaim, proposal collision, x1/x2 mixing, real apiary inspection or hive handling, pest or disease inference, sampling, treatment, destruction, reporting, food-safety or biosecurity instruction, land-access or privacy inference, package supply-chain drift, protected identifiers, cultural or Māori-authority overreach, validation replay, sibling-lane mutation, and Stage 20 promotion as threats.

Controls are exact-source anchoring, an accessible-corpus-only novelty audit, public-source vocabulary firewalls, strict lifecycle separation, a D-first sparse owner lane, exact direct-wheel pins in a fresh isolated environment, the four outcome labels, retained failures, smallest-dependency recovery, exact Git-blob manifests, five-class privacy scanning, and terminal nonpromotion.
""",
    )
    write_text(
        root / "x1/accessible-report-plan.md",
        """# Accessible report plan

Use a language declaration, skip link, one main landmark, ordered headings, captions, scoped table headers, plain-language summaries, and text-only relationships. Manual browser, keyboard, touch, zoom, reflow, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Structural checks cannot establish accessibility completeness.
""",
    )
    write_text(
        root / "x1/integrated-overview.md",
        f"""# Eiren Kestrel v669-v5 planning freeze

{IDENTITY_BOUNDARY}

## Scope

THOS Body is primary through a wholly synthetic apiary-inspection and colony-event documentation lens. GMUT Mind and Freed ID with CBR Heart remain visible and protected. This x1 freezes forty proposals and no observed outcome. It performs no inspection, handling, movement, sampling, diagnosis, treatment, destruction, notification, food-production, professional, safety, identity, legal, cultural, affected-party, or authority action.

## Novelty boundary

The declared inherited chain contains 5,070 rows. Exact committed shards expose 1,500 titles for bounded comparison, including Caelen's forty. The remaining 3,570 declared rows remain an explicit semantic-audit recovery gap. The Eiren titles have no exact collision and remain below the token-Jaccard quarantine threshold only within the accessible corpus. No universal novelty claim is made.

## Sources and tools

Eight current official or primary pages were reviewed only for vocabulary, structure, and refusal conditions: MPI bee biosecurity, MPI AFB ground rules, WOAH bee diseases, FAO good beekeeping practices, W3C PROV-O, JSON Schema 2020-12, WCAG 2.2, and the New Zealand Privacy Commissioner. Three exact Python package candidates are frozen for later isolated D-drive review: jsonschema 4.26.0, Pydantic 2.13.4, and NetworkX 3.6.1. No package is installed in x1, and no public citation supplies observation, diagnosis, instruction, endorsement, professional competence, conformance, legal interpretation, cultural ratification, or authority.

## Lifecycle

The freeze contains proposal, portfolio, source, tool-candidate, startup-failure, threat, route, and validation plans only. It must be committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before x2. Terminal verdict remains NOT_READY_FOR_STAGE_20.
""",
    )
    exclusions = [
        "docs/eiren-kestrel/v669-v5/validation/x1-manifest.json",
        "docs/eiren-kestrel/v669-v5/validation/x1-staged-review.json",
    ]
    entries = owner_file_manifest(repo, exclusions)
    write_json(
        root / "validation/x1-manifest.json",
        {
            "schema": "ghc.family.content-manifest.v2",
            "owner": OWNER,
            "phase": PHASE,
            "domain": "x1_working_tree_bytes_before_commit",
            "source_commit": SOURCE_FINAL,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def staged_review(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT").splitlines()
    disallowed = [
        name
        for name in names
        if "/x2/" in name or "/closeout/" in name or "/seal/" in name or "/evidence/" in name
    ]
    write_json(
        repo / OWNER_ROOT / "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x1_planning_only",
            "staged_entry_count_before_self": len(names),
            "staged_paths_before_self": names,
            "disallowed_x2_or_closeout_paths": disallowed,
            "x1_only": not disallowed,
            "self_exclusion": "docs/eiren-kestrel/v669-v5/validation/x1-staged-review.json",
        },
    )
    if disallowed:
        raise RuntimeError(f"x1 staged review found disallowed paths: {disallowed}")


def manifest_from_index(repo: Path) -> None:
    exclusions = [
        "docs/eiren-kestrel/v669-v5/validation/x1-manifest.json",
        "docs/eiren-kestrel/v669-v5/validation/x1-staged-review.json",
    ]
    entries = staged_blob_manifest(repo, exclusions)
    write_json(
        repo / OWNER_ROOT / "validation/x1-manifest.json",
        {
            "schema": "ghc.family.content-manifest.v2",
            "owner": OWNER,
            "phase": PHASE,
            "domain": "x1_exact_staged_git_blobs_before_commit",
            "source_commit": SOURCE_FINAL,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--review-staged", action="store_true")
    parser.add_argument("--resume-tail", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    args = parser.parse_args()
    if args.review_staged:
        staged_review(args.repo.resolve())
    elif args.manifest_from_index:
        manifest_from_index(args.repo.resolve())
    elif args.resume_tail:
        resume_tail(args.repo.resolve())
    else:
        build(args.repo.resolve())


if __name__ == "__main__":
    main()

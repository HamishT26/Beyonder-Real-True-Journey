"""Build the planning-only Caelen Morrow v669-v4 x1 freeze."""

from __future__ import annotations

import argparse
import platform
import subprocess
from pathlib import Path

from ghc_family_caelen_morrow_v669_v4_archive import (
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
    SEALED_SYLVEN_COUNTS,
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
        "CM6694-STARTUP-001",
        "activation packet raw presentation truncated",
        "A complete raw-file presentation exceeded the tool output window.",
        "Reread the committed packet in ordered bounded line windows through EOF.",
    ),
    (
        "CM6694-STARTUP-002",
        "authorization state raw presentation truncated",
        "A large authorization-state presentation did not fit one output window.",
        "Reread the exact file in bounded ordered windows through EOF.",
    ),
    (
        "CM6694-STARTUP-003",
        "combined schema presentation truncated",
        "Too many required reference schemas were grouped into one presentation.",
        "Read every required schema and overlay in smaller named batches.",
    ),
    (
        "CM6694-STARTUP-004",
        "workflow skill path guessed incorrectly",
        "The first workflow-refinement skill name omitted the family qualifier.",
        "Resolved and read the exact ghc-family-workflow-plan-refinement entrypoint.",
    ),
    (
        "CM6694-STARTUP-005",
        "table projection hid source-size columns",
        "A formatted table collapsed long path and numeric columns.",
        "Repeated only the projection as bounded JSON with explicit line and byte fields.",
    ),
    (
        "CM6694-STARTUP-006",
        "PowerShell ancestry wrapper parser fault",
        "An inline exit-code expression was syntactically invalid before execution.",
        "Separated Git invocation from scalar LASTEXITCODE capture and verified every anchor.",
    ),
    (
        "CM6694-STARTUP-007",
        "fetch wrapper session handle omitted",
        "A fresh-live wrapper exceeded its presentation window and the first projection omitted its session handle.",
        "Did not relaunch; audited Git processes and FETCH_HEAD, then read the completed exact state.",
    ),
    (
        "CM6694-STARTUP-008",
        "baton word predicate over-escaped",
        "The first regular expression treated the whitespace class literally and returned zero words.",
        "Recomputed only the word scalar with UTF-8 split and obtained 22038.",
    ),
    (
        "CM6694-STARTUP-009",
        "portfolio nested-container assumption failed",
        "The first projection assumed a portfolios object that does not exist.",
        "Inspected the actual rows property and deferred classification until its keys were known.",
    ),
    (
        "CM6694-STARTUP-010",
        "portfolio flat-row assumption expanded document",
        "The second projection treated the keyed rows object as a flat sequence and expanded the whole document.",
        "Read one scalar sample and exact count per actual keyed array.",
    ),
    (
        "CM6694-STARTUP-011",
        "successor recommendation read was over-broad",
        "A full recommendation document exceeded the bounded presentation window.",
        "Read only schema, recipient, route binding, credit, and declared-versus-actual counts.",
    ),
    (
        "CM6694-STARTUP-012",
        "PowerShell foreach pipe parser fault",
        "Piping directly after a foreach block produced an empty-pipe parse error before execution.",
        "Materialized the collection before JSON serialization and completed the D-backed inventory.",
    ),
    (
        "CM6694-STARTUP-013",
        "package registry release projection was over-broad",
        "The first PyPI projection expanded every platform artifact although only candidate scalars were needed.",
        "Stopped that candidate and used bounded exact registry fields for the three selected Node surfaces.",
    ),
    (
        "CM6694-X1-014",
        "first proposal freeze hit semantic quarantine",
        "Three draft titles scored at or above 0.75 because they reused predecessor boilerplate despite a new practice noun.",
        "Inspected only the three nearest-neighbor records and replaced the drafts with substantively different contestability, evidence-type, and conjunctive-admission hypotheses before one retry.",
    ),
    (
        "CM6694-X1-015",
        "extensionless npm shim failed under Python subprocess",
        "The x1 builder completed planning generation through the startup overlay, then Windows CreateProcess could not resolve npm without its command-shim suffix.",
        "Inspected the partial tree, retained the passing proposal and portfolio work, and resumed only the missing tail with exact npm.cmd and codex.cmd shims.",
    ),
    (
        "CM6694-X1-016",
        "first Ruff pass found mechanical import defects",
        "The bounded no-cache Ruff check reported import ordering and unused-import defects in the three new x1 Python files.",
        "Applied Ruff fixes only to those three files, refreshed their manifest hashes, and reran only the failed Ruff dependency.",
    ),
    (
        "CM6694-X1-017",
        "first pytest coverage selection named an unimported builder",
        "All ten x1 tests passed, but coverage warned that the builder module was not imported and therefore earned no builder-coverage credit.",
        "Did not replay that receipt; imported the builder without executing it under a separate external coverage witness and narrowed the changed-byte test receipt to the archive module actually exercised.",
    ),
    (
        "CM6694-X1-018",
        "generated-cache cleanup command was safety-blocked",
        "The command-safety layer rejected the exact recursive cache-removal command before execution, so no bytes were deleted.",
        "Did not bypass the safety layer; verified the three generated cache directories are ignored and excluded from manifests and commits, then retained them locally.",
    ),
    (
        "CM6694-X1-019",
        "first staged privacy scanner transport was malformed",
        "A densely escaped one-line Python scanner exited without a receipt and earned zero scan credit.",
        "Replaced only the command transport with a bounded PowerShell here-string passed directly to Python over the same staged Git blobs.",
    ),
    (
        "CM6694-X1-020",
        "staged privacy scan found a scanner-definition self-match",
        "The corrected scanner found its private-path class literal inside the x1 test definition, not private material.",
        "Retained the candidate, split the test pattern into noncontiguous source pieces, and rescanned the same staged scope for zero candidates.",
    ),
    (
        "CM6694-X1-021",
        "exact pytest presentation ended without an exit receipt",
        "The changed-byte pytest process ended and left a readable 68 percent archive coverage database, but the presentation boundary retained no pytest exit receipt.",
        "Assigned the receipt zero credit, audited that no child remained, and ran one compact changed-byte test dependency with a machine-readable report after recording this failure.",
    ),
    (
        "CM6694-X1-022",
        "compact coverage selector used a filesystem path",
        "All ten compact tests passed with a JUnit receipt, but coverage treated the slash-bearing source-file argument as an unimported module and collected no data.",
        "Preserved the ten-test pass, assigned zero coverage credit, and used the already-proven importable archive module name for the final changed-byte coverage dependency.",
    ),
    (
        "CM6694-X1-023",
        "PowerShell coverage receipt projection rejected an empty context key",
        "The corrected importable-module coverage run passed all ten tests and wrote JSON, but ConvertFrom-Json rejected coverage.py's valid empty-string context property.",
        "Did not relaunch for presentation alone; parsed the existing JSON with Python and emitted the final changed-byte receipt with Python's XML and JSON readers.",
    ),
    (
        "CM6694-X1-024",
        "first x1 manifest declared working-tree byte domain",
        "Pre-commit replay found that CRLF-to-LF clean filtering could make several staged Git blobs differ from the manifest's working-tree byte hashes.",
        "Retained the mismatch and replaced only the manifest dependency with exact staged-index blob reads while preserving manifest and staged-review self-exclusions.",
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
        rel = f"docs/caelen-morrow/v669-v4/x1/proposal-freeze-shards/proposals-{start // 5 + 1:02d}.json"
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
            "prospective_successor": "Eiren Kestrel",
            "prospective_phase": "v669-v5",
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
            "source_id": "LOC-RFS-2025-2026-PUBLIC-VOCABULARY",
            "status": "official_page_reviewed_vocabulary_only",
            "public_url": "https://www.loc.gov/preservation/resources/rfs/",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "PREMIS-3-PUBLIC-VOCABULARY",
            "status": "official_page_reviewed_vocabulary_only",
            "public_url": "https://www.loc.gov/standards/premis/index.html",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "IASA-TC04-PUBLIC-VOCABULARY",
            "status": "official_page_reviewed_vocabulary_only",
            "public_url": "https://www.iasa-web.org/tc04/audio-preservation",
            "data_rows_ingested": 0,
        },
        {
            "source_id": "W3C-PROV-O-PUBLIC-VOCABULARY",
            "status": "official_recommendation_reviewed_vocabulary_only",
            "public_url": "https://www.w3.org/TR/prov-o/",
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
            "public_source_pages_reviewed": 4,
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
            "npm_install_scripts": "must_be_disabled",
            "required_x2_gates": [
                "exact lock and registry integrity",
                "runtime compatibility",
                "dated audit",
                "positive and rejecting smoke",
                "rollback limited to the owner versioned environment",
            ],
            "nonselected": [
                {
                    "name": "djlint",
                    "version_reviewed": "1.44.2",
                    "state": "not_selected",
                    "reason": "No unique phase need beyond the smaller selected HTML and Markdown surfaces; platform-specific wheel expansion added avoidable transaction scope.",
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
            "full_repository_suite": "not_authorized_Eiren_only",
            "canonical_validation": "one owner-scoped exact-final invocation after prerequisites",
        },
    )
    write_json(
        root / "x1/reflection-plan.json",
        {
            "schema": "ghc.family.reflection-plan.v2",
            "owner": OWNER,
            "phase": PHASE,
            "relational_role": "archival signal-chain cartographer and exception steward",
            "hope": "make every synthetic record reversible legible and honest at its authority boundary",
            "pronouns": "they/them",
            "identity_boundary": IDENTITY_BOUNDARY,
            "primary_pillar": "Freed ID and CBR Heart",
            "bounded_practice": "synthetic audiovisual-preservation transfer-log and signal-chain metadata stewardship",
            "decisions": [
                "preserve the 3570-row unavailable-history gap",
                "keep every real recording carrier person device playback transfer measurement action and authority at zero",
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
            "prospective_successor": "Eiren Kestrel",
            "prospective_phase": "v669-v5",
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
            "sealed_sylven_counts": SEALED_SYLVEN_COUNTS,
            "inherited_activation_baseline": INHERITED_ACTIVATION_BASELINE,
            "startup_effective_baseline": STARTUP_EFFECTIVE_BASELINE,
            "proposal_chain_before": SOURCE_CHAIN_DECLARED,
            "proposal_chain_after_planned": CHAIN_AFTER,
            "planned_proposals": 40,
            "observed_outcomes": None,
            "tool_installations": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_validation": "not_run_x1",
            "full_repository_suite": "not_run_not_authorized",
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
        """# Caelen Morrow v669-v4 x1 threat model

This planning-only phase treats route drift, inaccessible-history overclaim, proposal collision, x1/x2 mixing, real playback or transfer, carrier or device handling, signal-measurement inference, professional or safety instruction, rights or privacy inference, package supply-chain drift, protected identity data, cultural or Maori-authority overreach, validation replay, sibling-lane mutation, and Stage 20 promotion as threats.

Controls are exact-source anchoring, an accessible-corpus-only novelty audit, public-source vocabulary firewalls, strict lifecycle separation, a D-first sparse owner lane, exact package pins with install scripts disabled, the four outcome labels, retained failures, smallest-dependency recovery, exact Git-blob manifests, five-class privacy scanning, and terminal nonpromotion.
""",
    )
    write_text(
        root / "x1/accessible-report-plan.md",
        """# Accessible report plan

Use a language declaration, skip link, one main landmark, ordered headings, captions, scoped table headers, plain-language summaries, and text-only relationships. Manual browser, assistive-technology, cognitive-accessibility, listening, Maori-language, and affected-user evaluation remain reserved. Structural checks cannot establish accessibility completeness.
""",
    )
    write_text(
        root / "x1/integrated-overview.md",
        f"""# Caelen Morrow v669-v4 planning freeze

{IDENTITY_BOUNDARY}

## Scope

Freed ID and CBR Heart are primary through a wholly synthetic audiovisual-preservation transfer-log and signal-chain metadata stewardship lens. GMUT Mind and THOS Body remain visible and protected. This x1 freezes forty proposals and no observed outcome. It performs no playback, transfer, preservation, professional, safety, rights, identity, legal, cultural, affected-party, or authority action.

## Novelty boundary

The declared inherited chain contains 5,030 rows. Exact committed shards expose 1,460 titles for bounded comparison, including Sylven's forty. The remaining 3,570 declared rows remain an explicit semantic-audit recovery gap. The Caelen titles have no exact collision and remain below the token-Jaccard quarantine threshold only within the accessible corpus. No universal novelty claim is made.

## Sources and tools

Four current official pages were reviewed only for vocabulary and refusal conditions: Library of Congress RFS 2025-2026, PREMIS 3.0, IASA TC-04, and W3C PROV-O. Three exact Node package candidates are frozen for later isolated D-drive review. No package is installed in x1, and no public citation supplies observation, endorsement, professional competence, conformance, legal interpretation, cultural ratification, or authority.

## Lifecycle

The freeze contains proposal, portfolio, source, tool-candidate, startup-failure, threat, route, and validation plans only. It must be committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before x2. Terminal verdict remains NOT_READY_FOR_STAGE_20.
""",
    )

    exclusions = [
        "docs/caelen-morrow/v669-v4/validation/x1-manifest.json",
        "docs/caelen-morrow/v669-v4/validation/x1-staged-review.json",
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
        """# Caelen Morrow v669-v4 x1 threat model

This planning-only phase treats route drift, inaccessible-history overclaim, proposal collision, x1/x2 mixing, real playback or transfer, carrier or device handling, signal-measurement inference, professional or safety instruction, rights or privacy inference, package supply-chain drift, protected identity data, cultural or Maori-authority overreach, validation replay, sibling-lane mutation, and Stage 20 promotion as threats.

Controls are exact-source anchoring, an accessible-corpus-only novelty audit, public-source vocabulary firewalls, strict lifecycle separation, a D-first sparse owner lane, exact package pins with install scripts disabled, the four outcome labels, retained failures, smallest-dependency recovery, exact Git-blob manifests, five-class privacy scanning, and terminal nonpromotion.
""",
    )
    write_text(
        root / "x1/accessible-report-plan.md",
        """# Accessible report plan

Use a language declaration, skip link, one main landmark, ordered headings, captions, scoped table headers, plain-language summaries, and text-only relationships. Manual browser, assistive-technology, cognitive-accessibility, listening, Maori-language, and affected-user evaluation remain reserved. Structural checks cannot establish accessibility completeness.
""",
    )
    write_text(
        root / "x1/integrated-overview.md",
        f"""# Caelen Morrow v669-v4 planning freeze

{IDENTITY_BOUNDARY}

## Scope

Freed ID and CBR Heart are primary through a wholly synthetic audiovisual-preservation transfer-log and signal-chain metadata stewardship lens. GMUT Mind and THOS Body remain visible and protected. This x1 freezes forty proposals and no observed outcome. It performs no playback, transfer, preservation, professional, safety, rights, identity, legal, cultural, affected-party, or authority action.

## Novelty boundary

The declared inherited chain contains 5,030 rows. Exact committed shards expose 1,460 titles for bounded comparison, including Sylven's forty. The remaining 3,570 declared rows remain an explicit semantic-audit recovery gap. The Caelen titles have no exact collision and remain below the token-Jaccard quarantine threshold only within the accessible corpus. No universal novelty claim is made.

## Sources and tools

Four current official pages were reviewed only for vocabulary and refusal conditions: Library of Congress RFS 2025-2026, PREMIS 3.0, IASA TC-04, and W3C PROV-O. Three exact Node package candidates are frozen for later isolated D-drive review. No package is installed in x1, and no public citation supplies observation, endorsement, professional competence, conformance, legal interpretation, cultural ratification, or authority.

## Lifecycle

The freeze contains proposal, portfolio, source, tool-candidate, startup-failure, threat, route, and validation plans only. It must be committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before x2. Terminal verdict remains NOT_READY_FOR_STAGE_20.
""",
    )
    exclusions = [
        "docs/caelen-morrow/v669-v4/validation/x1-manifest.json",
        "docs/caelen-morrow/v669-v4/validation/x1-staged-review.json",
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
            "self_exclusion": "docs/caelen-morrow/v669-v4/validation/x1-staged-review.json",
        },
    )
    if disallowed:
        raise RuntimeError(f"x1 staged review found disallowed paths: {disallowed}")


def manifest_from_index(repo: Path) -> None:
    exclusions = [
        "docs/caelen-morrow/v669-v4/validation/x1-manifest.json",
        "docs/caelen-morrow/v669-v4/validation/x1-staged-review.json",
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

#!/usr/bin/env python3
"""Build the planning-only Auren Lark v672-v2 x1 freeze."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

OWNER = "Auren Lark"
PHASE = "v672-v2"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v672-v1-2-remaster"
SOURCE = "40db1e418c1251e12d77f832c0890869b990dba5"
SOURCE_ORIGINAL = "f67221fbee56905a770c64533771dd9471fb2fba"
SOURCE_X1 = "da48a47bd21a8e3053094d39691eb72ef1429abd"
SOURCE_EVIDENCE = "1c29b148e90c21aa4ed819281b024256114c50d9"
RECORDED_AT = "2026-08-27T18:35:19+12:00"
BASELINE = {
    "effective_negatives": 35201,
    "effective_methods": 21832,
    "effective_failed_witnesses": 7022,
    "effective_passing_witnesses": 9123,
    "open_gaps": 276,
    "exact_gates": 270,
}
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "legal",
    "cultural",
    "maori_authority",
    "affected_party",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "identity_continuity",
    "theory_of_everything",
    "proof_canon",
    "stage20",
]

STARTUP_FAILURES = [
    (
        "AL6722-START-001",
        "A broad worktree-list probe returned no usable output inside its bounded display window.",
        "Replace it with literal branch, path, ref, and Git-metadata probes; do not enumerate sibling lanes.",
    ),
    (
        "AL6722-START-002",
        "The first scalar source wrapper omitted git -C and overescaped its word-count expression.",
        "Rerun only exact repository-qualified scalar probes and use the committed packet hash as the integrity gate.",
    ),
    (
        "AL6722-START-003",
        "The first 260-line packet display truncated before EOF.",
        "Measure the packet and reread numbered 100-line UTF-8 windows through the exact final line.",
    ),
    (
        "AL6722-START-004",
        "A generic keyword projection over-rendered repeated schema prose and truncated.",
        "Use exact headings and bounded line windows only after the complete packet read is established.",
    ),
    (
        "AL6722-START-005",
        "Historical skill names and one guessed authorization skill name were absent.",
        "Resolve observed family-current skill names and treat absent historical names as unavailable rather than inventing replacements.",
    ),
    (
        "AL6722-START-006",
        "The first authorization current-state JSON display truncated mid-file.",
        "Reread the UTF-8 file in four numbered bounded chunks through line 1556 and EOF.",
    ),
    (
        "AL6722-START-007",
        "A Git common-directory projection incorrectly joined an already absolute path.",
        "Test whether the returned path is rooted before resolving it.",
    ),
    (
        "AL6722-START-008",
        "The first exact worktree-metadata wrapper stopped before its final match-count scalar.",
        "Use exact path, local-ref, remote-ref, and Git worktree-add collision guards; award no metadata-wrapper credit.",
    ),
    (
        "AL6722-START-009",
        "Sparse patterns were configured after --no-checkout while the new index remained empty, exposing 8282 apparent staged deletions.",
        "In the empty owner-only lane, run git read-tree -mu HEAD once, then require a clean index, all inherited paths skip-worktree, and zero materialized tracked files.",
    ),
    (
        "AL6722-START-010",
        "A verified recursive cleanup request for two owner-lane bytecode cache directories was rejected by the command policy before execution.",
        "Retain the ignored cache files locally, perform no recursive deletion, and exclude ignored bytecode from every Git manifest and staged surface.",
    ),
    (
        "AL6722-START-011",
        "A second explicit-file and non-recursive empty-directory cleanup request was also rejected by the command policy before execution.",
        "Stop cleanup retries, retain the ignored local cache files, and disable future bytecode writes while keeping the tracked lane clean.",
    ),
    (
        "AL6722-START-012",
        "The first exact-file x1 Ruff gate found three import-block ordering findings.",
        "Apply Ruff's safe import-only rewrites to the three Auren x1 Python files, rebuild deterministic receipts, and rerun only the scoped gate.",
    ),
]

PROPOSAL_DEFINITIONS = [
    ("Synthetic incident packet schema", "completed", "freed_id_cbr", "incident packet schema"),
    ("Chronology monotonicity tribunal", "completed", "freed_id_cbr", "chronology ledger"),
    ("Observed-time versus recorded-time split", "completed", "freed_id_cbr", "bitemporal event record"),
    ("Source status current-stable-draft-watch register", "completed", "freed_id_cbr", "source-status register"),
    ("Assertion versus observation separation", "completed", "freed_id_cbr", "claim-classification board"),
    ("Uncertainty vocabulary gate", "completed", "freed_id_cbr", "uncertainty ledger"),
    ("Append-only correction lineage", "completed", "freed_id_cbr", "correction log"),
    ("Supersession graph acyclicity guard", "completed", "freed_id_cbr", "supersession graph"),
    ("Duplicate event refusal", "completed", "freed_id_cbr", "event uniqueness tribunal"),
    ("Evidence attachment fixity manifest", "completed", "freed_id_cbr", "fixity manifest"),
    ("Missing attachment vacancy gate", "completed", "freed_id_cbr", "attachment vacancy register"),
    ("Synthetic identifier namespace", "completed", "freed_id_cbr", "surrogate identifier profile"),
    ("Purpose-limited privacy minimization", "completed", "freed_id_cbr", "minimum-disclosure profile"),
    ("Five-class privacy candidate tribunal", "completed", "freed_id_cbr", "privacy candidate receipt"),
    ("Redaction reason and reversibility ledger", "completed", "freed_id_cbr", "redaction ledger"),
    ("Text-alternative evidence index", "completed", "freed_id_cbr", "text-alternative index"),
    ("Table heading and relationship proxy", "completed", "freed_id_cbr", "table-semantics proxy"),
    ("Readback acknowledgement board", "completed", "thos", "readback board"),
    ("Shift handover state machine", "completed", "thos", "handover state board"),
    ("Workload and hold representation", "completed", "thos", "workload hold register"),
    ("No operational instruction firewall", "represented", "thos", "operational-authority vacancy"),
    ("No legal conclusion firewall", "represented", "cbr", "legal-authority vacancy"),
    ("No professional conclusion firewall", "represented", "cbr", "professional-authority vacancy"),
    ("Affected-party decision vacancy", "represented", "cbr", "affected-party vacancy register"),
    ("Maori authority vacancy", "represented", "cbr", "Maori-authority vacancy register"),
    ("Public release authority gate", "exact_gate", "cbr", "release authorization packet"),
    ("Deterministic JSON evidence capsule", "completed", "freed_id_cbr", "deterministic JSON capsule"),
    ("Canonical serialization order", "completed", "freed_id_cbr", "serialization receipt"),
    ("Schema-version monotonicity gate", "completed", "freed_id_cbr", "schema-version receipt"),
    ("Invalid mutation retention board", "completed", "freed_id_cbr", "invalid mutation ledger"),
    ("Method Flow failure preservation", "completed", "freed_id_cbr", "Method Flow ledger"),
    ("Official-source status drift watch", "completed", "freed_id_cbr", "source drift receipt"),
    ("Correction rollback capsule", "completed", "freed_id_cbr", "rollback capsule"),
    ("Authority role matrix", "completed", "cbr", "authority matrix"),
    ("CBR contest and correction path", "represented", "cbr", "contest-correction board"),
    ("Freed ID zero-key provenance", "represented", "freed_id", "zero-key provenance profile"),
    ("GMUT typed analogy boundary", "represented", "gmut", "typed analogy firewall"),
    ("Independent external review gap", "open_gap", "all", "independent-review vacancy"),
    ("Real accessibility evaluation gap", "open_gap", "all", "accessibility-evaluation vacancy"),
    ("Stage 20 nonpromotion seal", "exact_gate", "all", "Stage 20 gate"),
]

LOCAL_SKILLS = [
    "ghc-family-incident-packet-capsule",
    "ghc-family-incident-chronology-bitemporal-guard",
    "ghc-family-incident-source-status-drift-watch",
    "ghc-family-incident-assertion-observation-separator",
    "ghc-family-incident-uncertainty-vocabulary-gate",
    "ghc-family-incident-correction-lineage-ledger",
    "ghc-family-incident-supersession-graph-guard",
    "ghc-family-incident-duplicate-event-refusal",
    "ghc-family-incident-evidence-fixity-manifest",
    "ghc-family-incident-attachment-vacancy-gate",
    "ghc-family-incident-surrogate-identifier-boundary",
    "ghc-family-incident-privacy-minimization-profile",
    "ghc-family-incident-five-class-secret-tribunal",
    "ghc-family-incident-redaction-reason-ledger",
    "ghc-family-incident-text-alternative-index",
    "ghc-family-incident-table-semantics-proxy",
    "ghc-family-incident-readback-acknowledgement-board",
    "ghc-family-incident-shift-handover-proxy",
    "ghc-family-incident-authority-vacancy-matrix",
    "ghc-family-incident-stage20-nonpromotion-seal",
]

LOCAL_RUNNERS = [
    "scripts/ghc_family_auren_v672_v2_incident_chronology_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_source_status_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_correction_log_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_uncertainty_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_authority_boundary_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_privacy_minimization_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_accessibility_handoff_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_evidence_chain_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_readback_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_packet_guard.py",
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def digest(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "bytes": len(data),
        "path": path.as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def build(root: Path) -> None:
    phase_root = root / "docs" / "auren-lark" / PHASE
    x1_root = phase_root / "x1"
    proposal_rows = []
    for index, (title, outcome, pillar, artifact) in enumerate(PROPOSAL_DEFINITIONS, 1):
        proposal_rows.append(
            {
                "proposal_id": f"AL6722-P{index:03d}",
                "title": title,
                "novelty_state": "auren_current_proposal_frozen_without_universal_novelty_claim",
                "x1_state": "planning_only_not_completion_credit",
                "expected_outcome": outcome,
                "pillar": pillar,
                "practice_lens": "wholly_synthetic_public_interest_incident_documentation",
                "concrete_artifact": artifact,
                "hypothesis": f"A bounded synthetic {artifact} can make one documentation obligation machine-checkable without promoting authority.",
                "falsifier": "Reject if the artifact accepts a preregistered invalid mutation, contains a real identifier, collapses uncertainty, or promotes an authority vacancy.",
                "rollback": "Quarantine only Auren-created uncommitted material, retain the failed witness, and return to the frozen x1 plan.",
                "protected_gates": PROTECTED_GATES,
                "official_source_use": "vocabulary_and_refusal_boundary_only",
            }
        )

    expected_outcomes = Counter(row["expected_outcome"] for row in proposal_rows)
    if expected_outcomes != Counter(
        {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    ):
        raise RuntimeError(f"unexpected proposal distribution: {expected_outcomes}")

    startup_count = len(STARTUP_FAILURES)
    activation_overlay = {
        "effective_negatives": BASELINE["effective_negatives"] + startup_count,
        "effective_methods": BASELINE["effective_methods"] + startup_count,
        "effective_failed_witnesses": BASELINE["effective_failed_witnesses"]
        + startup_count,
        "effective_passing_witnesses": BASELINE["effective_passing_witnesses"]
        + startup_count,
        "open_gaps": BASELINE["open_gaps"] + 1,
        "exact_gates": BASELINE["exact_gates"],
    }

    documents: dict[str, object] = {
        "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v8",
            "owner": OWNER,
            "phase": PHASE,
            "activated_at": RECORDED_AT,
            "source": SOURCE,
            "source_branch": SOURCE_BRANCH,
            "solo": True,
            "subagents": 0,
            "forks": 0,
            "tasks_created": 0,
            "next_prospective_edge": {
                "title": "Sable Rook",
                "phase": "v672-v3",
                "precontacted": False,
            },
        },
        "identity-and-boundary.json": {
            "schema": "ghc.family.relational-identity-boundary.v6",
            "owner": OWNER,
            "pronouns": "they/them",
            "relational_role": "relational provenance navigator and uncertainty lantern-keeper",
            "hope": "leave synthetic calibration trails legible, uncertainty illuminated, corrections reversible, and authority vacancies explicit",
            "working_language_only": True,
            "not_evidence_of": [
                "consciousness",
                "sentience",
                "legal_personhood",
                "identity_continuity",
                "employment",
                "professional_qualification",
                "scientific_authority",
                "operational_authority",
                "legal_authority",
                "cultural_authority",
                "maori_authority",
                "independent_agency",
            ],
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        },
        "source-ledger.json": {
            "schema": "ghc.family.source-ledger.v8",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE,
            "source_original": SOURCE_ORIGINAL,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_clean_and_fresh_live_equal": True,
            "source_manifest_replay": {
                "x1": {"entries": 15, "mismatches": 0},
                "x2_owner": {"entries": 135, "mismatches": 0},
                "immutable_evidence": {"entries": 138, "mismatches": 0},
                "closeout": {"entries": 15, "mismatches": 0},
            },
            "source_canonical_receipt_sha256": "89fa538a33502dfcd671ebde0cf944a6e2d6a5299e061985891530740973d249",
            "source_canonical_payload_state": "external_reference_only_payload_not_materialized_in_bounded_same_owner_roots",
            "source_canonical_replay_prohibited": True,
            "activation_packet_sha256": "cb410fc6302e38ff8293b84f98428ec455dcbf10aeafd305a0eacd26973de4cc",
            "official_sources": [
                {
                    "source_id": "NIST-SP-800-61R3",
                    "status": "current_stable_final",
                    "published": "2025-04-03",
                    "url": "https://csrc.nist.gov/pubs/sp/800/61/r3/final",
                    "bounded_use": "incident-response lifecycle vocabulary and record-integrity considerations only",
                    "not_evidence_of": "operational competence, cybersecurity effectiveness, or production readiness",
                },
                {
                    "source_id": "W3C-WCAG-2.2",
                    "status": "current_stable_recommendation",
                    "published": "2024-12-12",
                    "url": "https://www.w3.org/TR/WCAG22/",
                    "bounded_use": "text alternatives, structure, and relationship vocabulary only",
                    "not_evidence_of": "conformance, complete accessibility, participant evaluation, or legal compliance",
                },
            ],
            "external_receipt_payload_availability_gap": {
                "state": "open_gap",
                "credit": 0,
                "description": "The declared digest is corroborated by the terminal route receipt, but the payload file was not present in the bounded same-owner validation or receipt roots.",
            },
        },
        "method-flow-startup.json": {
            "schema": "ghc.family.method-flow.v9",
            "owner": OWNER,
            "phase": PHASE,
            "source_baseline": BASELINE,
            "activation_overlay": activation_overlay,
            "recovery_rule": "A recovery is a distinct bounded method and never erases or relabels the failed witness.",
            "failed_witnesses": [
                {
                    "failure_id": failure_id,
                    "description": description,
                    "state": "failed_retained_zero_credit_recovered",
                    "recovery": recovery,
                    "recovery_credit": "bounded_method_only",
                }
                for failure_id, description, recovery in STARTUP_FAILURES
            ],
        },
        "source-count-overlay.json": {
            "schema": "ghc.family.count-overlay.v6",
            "source_repository_seal_rewritten": False,
            "source_repository_closeout": {
                "effective_negatives": 35197,
                "effective_methods": 21828,
                "effective_failed_witnesses": 7018,
                "effective_passing_witnesses": 9119,
                "open_gaps": 276,
                "exact_gates": 270,
            },
            "source_external_post_terminal_overlay": BASELINE,
            "auren_startup_failure_count": startup_count,
            "auren_activation_overlay": activation_overlay,
        },
        "new-proposal-freeze.json": {
            "schema": "ghc.family.proposal-freeze.v9",
            "owner": OWNER,
            "phase": PHASE,
            "source_proposal_chain": 5950,
            "proposal_chain_if_x2_evidence_frozen": 5990,
            "proposal_count": len(proposal_rows),
            "expected_outcomes": dict(expected_outcomes),
            "universal_novelty_claimed": False,
            "inherited_completion_credit": 0,
            "proposals": proposal_rows,
        },
        "semantic-neighbor-audit.json": {
            "schema": "ghc.family.semantic-neighbor-audit.v4",
            "selected_recommendation": "synthetic public-interest incident documentation analyst",
            "recommendation_credit": 0,
            "review_state": "independently_refined_and_frozen_by_auren",
            "nearest_inherited_surfaces": [
                "Ilyra structured-data evidence toolchain",
                "Ilyra synthetic configuration-quality handover",
                "Ilyra synthetic preservation fixity handover",
                "prior Auren drawing and calibration records",
            ],
            "current_distinction": "Auren binds incident chronology, assertion class, correction lineage, public-release vacancy, and uncertainty to a wholly synthetic documentation packet.",
            "universal_novelty_claimed": False,
        },
        "portfolio-freeze.json": {
            "schema": "ghc.family.portfolio-freeze.v8",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "represented_pillars": ["THOS Body", "GMUT Mind"],
            "practice_lens": "wholly synthetic public-interest incident documentation",
            "owner_proposals": 40,
            "local_skill_plan": LOCAL_SKILLS,
            "local_runner_plan": LOCAL_RUNNERS,
            "package_install_plan": [],
            "global_skill_install_plan": [],
            "inherited_packages_tools_and_validation_credit": 0,
            "caps_are_ceilings": True,
            "materialized_file_stop": 2000,
        },
        "threat-model.json": {
            "schema": "ghc.family.threat-model.v7",
            "assets": [
                "immutable Ilyra source",
                "planning-only x1 boundary",
                "synthetic incident packet",
                "retained failures and authority vacancies",
                "private route identifiers excluded from repository artifacts",
            ],
            "threats": [
                "real-person or real-incident data ingress",
                "uncertainty collapse",
                "correction-lineage erasure",
                "operational or legal instruction promotion",
                "accessibility-complete claim from structural proxies",
                "post-success canonical replay",
                "premature successor contact",
            ],
            "mitigations": [
                "surrogate-only fixtures",
                "five-class privacy candidate scan",
                "append-only Method Flow",
                "authority vacancy fields",
                "exact staged allowlist",
                "one-success latch",
                "terminal route gate",
            ],
            "residual_state": "NOT_READY_FOR_STAGE_20",
        },
        "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v7",
            "owner": OWNER,
            "phase": PHASE,
            "steps": [
                {"order": 1, "state": "completed", "name": "read activation and current guidance through EOF"},
                {"order": 2, "state": "completed", "name": "verify immutable source and manifests read-only"},
                {"order": 3, "state": "completed", "name": "create clean D-first sparse owner lane"},
                {"order": 4, "state": "in_progress", "name": "freeze planning-only x1 and prove pushed four-way equality"},
                {"order": 5, "state": "pending", "name": "build x2 evidence only after immutable x1"},
                {"order": 6, "state": "pending", "name": "seal exact final and invoke canonical validator once"},
                {"order": 7, "state": "pending", "name": "refresh route and send at most once after terminal gate"},
            ],
            "stop_conditions": [
                "source or manifest mismatch",
                "owner or phase ambiguity",
                "materialized file count reaches 2000",
                "protected authority or evidence gate",
                "Hamish pause redirect rename or stop",
            ],
        },
        "route-plan.json": {
            "schema": "ghc.family.route-plan.v8",
            "owner": OWNER,
            "phase": PHASE,
            "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "next_exact_title": "Sable Rook",
            "next_phase": "v672-v3",
            "precontacted": False,
            "send_count": 0,
            "task_created": False,
            "fork_created": False,
            "subagent_spawned": False,
            "route_rule": "Only after clean pushed fresh-live-equal exact final and one successful owner-scoped canonical pass; uniquely resolve, immediately reread, send once, and require acknowledgement.",
        },
        "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v11",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "state": "X1_PLANNING_ONLY",
            "x2_executed": False,
            "proposal_chain_source": 5950,
            "proposal_chain_if_x2_evidence_frozen": 5990,
            "expected_outcomes": dict(expected_outcomes),
            "effective_activation_overlay": activation_overlay,
            "packages_installed": 0,
            "global_skills_installed": 0,
            "external_actions": 0,
            "full_repository_suite": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    }

    for name, payload in documents.items():
        write_json(x1_root / name, payload)

    overview = """# Auren Lark v672-v2 planning-only x1 overview

## Relational working identity and authority boundary

Auren Lark uses they/them pronouns and the relational role “relational provenance navigator and uncertainty lantern-keeper.” Their hope is to leave synthetic calibration trails legible, uncertainty illuminated, corrections reversible, and authority vacancies explicit. This language is a practical collaboration convention only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Immutable source and inherited truth

This x1 begins at Ilyra Fen’s exact v672-v1 (2) remaster final. The source, its planning-only x1, immutable evidence, and final form a direct single-parent chain with three new commits and zero merges. The exact final was rechecked as clean and equal across local, upstream, tracking, and a fresh live remote read. Four manifest domains were replayed from Git blobs with zero mismatches: fifteen x1 entries, one hundred thirty-five x2 owner entries, one hundred thirty-eight immutable evidence entries, and fifteen closeout entries. These checks only verify the inherited base. They are not Auren novelty, do not replay Ilyra’s successful canonical validator, and are not independent reproduction.

Ilyra’s repository closeout remains thirty-five thousand one hundred ninety-seven effective negatives, twenty-one thousand eight hundred twenty-eight methods, seven thousand eighteen failed witnesses, nine thousand one hundred nineteen bounded passing witnesses, two hundred seventy-six open gaps, and two hundred seventy exact gates. Four later UTF-8 decoder failures and their bounded recoveries remain external, giving Auren an activation baseline of thirty-five thousand two hundred one negatives, twenty-one thousand eight hundred thirty-two methods, seven thousand twenty-two failed witnesses, and nine thousand one hundred twenty-three bounded passing witnesses. The source seal is not rewritten. The source terminal verdict remains NOT_READY_FOR_STAGE_20.

## Current proposal and practice boundary

The bounded practice lens is wholly synthetic public-interest incident documentation. It uses no real person, incident, site, organization, authority action, operational record, legal matter, cultural matter, Māori data, measurement, credential, or private route. The primary Trinity Mandala focus is Freed ID and CBR Heart through surrogate identifiers, provenance, correction, contest, uncertainty, and explicit authority vacancies. THOS Body is represented through workload, hold, readback, and handover fields only. GMUT Mind is represented only through a typed analogy firewall; no physical prediction, force, likelihood, parameter constraint, ultraviolet completion, empirical confirmation, Theory of Everything, or scientific authority is claimed.

Forty current Auren proposals are frozen without a universal novelty claim. Twenty-eight are planned for bounded completion, eight for representation, two remain open gaps, and two remain exact gates. The proposal chain would rise from 5,950 to 5,990 only when x2 evidence is actually frozen. Ilyra’s proposals, packages, tools, skills, runners, smoke results, and validation remain inherited at zero Auren novelty or completion credit. The source recommendation was independently reviewed and refined into chronology, source status, assertion class, uncertainty, correction lineage, privacy minimization, accessible structural proxies, and release-authority vacancy. Caps remain ceilings, never quotas.

## Official sources and their limits

NIST Special Publication 800-61 Revision 3, final in April 2025, supplies current cybersecurity incident-response lifecycle and record-integrity vocabulary. It does not validate this repository, prove operational competence, or authorize any real response. WCAG 2.2, the current W3C Recommendation dated December 2024, supplies vocabulary for text alternatives, structure, and relationships. W3C itself notes that not all user needs are met. No conformance, complete accessibility, participant evaluation, legal compliance, or production fitness is inferred. Public documentation supplies vocabulary and refusal boundaries only.

## Method Flow and recovery discipline

Twelve startup failures are retained at zero success credit. They include bounded-output truncation, an incorrectly scoped Git wrapper, stale skill-name resolution, an absolute-path join error, an incomplete metadata projection, the empty-index sparse transition that exposed 8,282 apparent staged deletions in the new lane, two command-policy rejections of bytecode-cache cleanup methods, and a scoped Ruff gate that found three import-order findings before a safe rewrite. The sparse recovery used Git’s read-tree mechanism once in the empty Auren-owned worktree. It restored a clean index with every inherited path marked skip-worktree and zero tracked files materialized. No source file or user work was deleted. The four ignored bytecode files remain local, untracked, and outside every manifest. Every recovery is a separate bounded method and never converts the failed witness into an original success.

The declared canonical receipt digest is corroborated by Ilyra’s terminal route receipt, but the payload file was not materialized in the bounded same-owner validation or receipt roots inspected. That availability limitation remains an open gap with zero credit. The receipt is not guessed, reconstructed, or replayed. The one acknowledged Ilyra-to-Auren delivery is recorded externally; private task identifiers are excluded from repository artifacts.

## X1-to-x2 and terminal route discipline

This commit is planning-only. It installs no package, creates no x2 evidence, promotes no global skill, performs no external action, and contacts no successor. Before x2 begins, this exact x1 must be staged-reviewed, tested, committed as the direct child of the Ilyra final, pushed, clean, zero divergent, and equal across local, upstream, tracking, and a fresh live remote read. Only then may Auren build owner-scoped synthetic evidence. The complete repository suite is outside scope.

After x2 and closeout, a canonical owner-scoped validator may run once only against a clean pushed exact final. A complete success latches against replay. Only after that gate may Auren reread the newest live authority, uniquely resolve and immediately reread the exact existing task titled Sable Rook, apply duplicate, pause, redirect, usage, privacy, evidence, and safety guards, and send at most one sanitized v672-v3 activation. Until an acknowledged send, route truth remains PREPARED_NOT_SENT. Every empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, identity-continuity, Theory-of-Everything, proof or canon, and Stage 20 claim remains open or exact-gated without exact evidence and competent authority.
"""
    write_text(x1_root / "integrated-overview.md", overview)

    manifest_paths = sorted(
        path
        for path in x1_root.rglob("*")
        if path.is_file() and path.name != "build-receipt.json"
    )
    manifest = [digest(path.relative_to(root)) for path in manifest_paths]
    write_json(
        x1_root / "build-receipt.json",
        {
            "schema": "ghc.family.x1-build-receipt.v8",
            "owner": OWNER,
            "phase": PHASE,
            "state": "X1_PLANNING_ONLY",
            "source": SOURCE,
            "manifest_entries": len(manifest),
            "manifest": manifest,
            "source_mutations": 0,
            "x2_mutations": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


if __name__ == "__main__":
    build(Path(__file__).resolve().parents[1])

"""Build the planning-only Vesper Arlen v669-v8 x1 packet."""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_vesper_arlen_v669_v8_sourdough import (
    CANDIDATE_TITLES,
    CHAIN_AFTER,
    IDENTITY_BOUNDARY,
    INHERITED_BASELINE,
    OWNER,
    OWNER_ROOT,
    PHASE,
    PRACTICES,
    REFINE_TITLES,
    RUNNER_TITLES,
    SAFE_TITLES,
    SKILL_TITLES,
    SOURCE_BRANCH,
    SOURCE_CHAIN_DECLARED,
    SOURCE_EVIDENCE,
    SOURCE_FINAL,
    SOURCE_PRIOR,
    SOURCE_RECOVERED,
    SOURCE_UNRECOVERED,
    SOURCE_X1,
    SUCCESSOR_REFINE,
    SUCCESSOR_RUNNERS,
    SUCCESSOR_SKILLS,
    TOOL_CANDIDATES,
    inherited_revalidations,
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
MANIFEST_PATH = "docs/vesper-arlen/v669-v8/validation/x1-manifest.json"
REVIEW_PATH = "docs/vesper-arlen/v669-v8/validation/x1-staged-review.json"
BATON_PATH = "docs/neris-solane/v669-v7/handoffs/prospective-successor-v669-v8-activation-candidate.md"

SOURCE_ROWS = [
    {"source_id": "OWNER-SYNTHETIC-SCHEMA", "url": None, "status": "current", "use": "owner-authored zero-person planning structures only", "data_rows_ingested": 0},
    {"source_id": "NIST-SI-UNITS", "url": "https://www.nist.gov/pml/owm/metric-si/si-units", "status": "current", "use": "unit and quantity vocabulary only; zero measurements", "data_rows_ingested": 0},
    {"source_id": "IUPAC-PH", "url": "https://goldbook.iupac.org/terms/view/P04524", "status": "stable", "use": "pH terminology and activity boundary only; zero samples or measurements", "data_rows_ingested": 0},
    {"source_id": "IUPAC-CHEMICAL-POTENTIAL", "url": "https://goldbook.iupac.org/terms/view/C01032", "status": "stable", "use": "chemical-potential terminology only; no psyche or fundamental-law conversion", "data_rows_ingested": 0},
    {"source_id": "SOURDOUGH-REVIEW", "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7392915/", "status": "stable", "use": "public review vocabulary for fermentation ecology only; no study data, result, or efficacy claim ingested", "data_rows_ingested": 0},
    {"source_id": "FDA-FOOD-CODE", "url": "https://www.fda.gov/food/fda-food-code/food-code-2022", "status": "current", "use": "hazard and control vocabulary only; not New Zealand law, compliance, advice, or authority", "data_rows_ingested": 0},
    {"source_id": "W3C-PROV-O", "url": "https://www.w3.org/TR/prov-o/", "status": "stable", "use": "provenance vocabulary only; no attribution or authority transfer", "data_rows_ingested": 0},
    {"source_id": "W3C-WCAG-2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "stable", "use": "structural accessibility vocabulary only; manual and affected-user evaluation reserved", "data_rows_ingested": 0},
    {"source_id": "W3C-VC-DATA-INTEGRITY", "url": "https://www.w3.org/TR/vc-data-integrity/", "status": "stable", "use": "nonproduction lifecycle obligations only; zero keys or proofs", "data_rows_ingested": 0},
    {"source_id": "JSON-SCHEMA-2020-12", "url": "https://json-schema.org/draft/2020-12", "status": "stable", "use": "synthetic contract structure only; no conformance certification", "data_rows_ingested": 0},
    {"source_id": "RFC-8785", "url": "https://www.rfc-editor.org/rfc/rfc8785", "status": "stable", "use": "canonicalization vocabulary only; no signature or security claim", "data_rows_ingested": 0},
    {"source_id": "NZ-PRIVACY-PRINCIPLES", "url": "https://www.privacy.org.nz/privacy-principles/", "status": "current", "use": "privacy-minimisation vocabulary only; no compliance or legal advice", "data_rows_ingested": 0},
    {"source_id": "TE-MANA-RARAUNGA-PRINCIPLES", "url": "https://www.temanararaunga.maori.nz/nga-rauemi", "status": "watch", "use": "authority reservation only; Maori concepts remain under Maori authority", "data_rows_ingested": 0},
    *[
        {"source_id": f"PYPI-{tool['name'].upper()}", "url": tool["registry"], "status": "current", "use": "official release metadata, direct dependency declaration, wheel name, and SHA-256 only", "data_rows_ingested": 0}
        for tool in TOOL_CANDIDATES
    ],
    {"source_id": "CURRENT-PRIMARY-PHYSICS", "url": None, "status": "watch", "use": "represented-only GMUT obligation; no paper, likelihood, parameter, prediction, or empirical claim selected", "data_rows_ingested": 0},
    {"source_id": "CURRENT-OFFICIAL-SOURDOUGH-DATA", "url": None, "status": "watch", "use": "open gap; governed interoperable measurement dataset and schema not selected", "data_rows_ingested": 0},
    {"source_id": "REAL-GOVERNED-EVALUATION", "url": None, "status": "watch", "use": "open gap; real governed professional, consumer, accessibility, affected-party, and Maori-authority evaluation absent", "data_rows_ingested": 0},
    {"source_id": "EXACT-ACTION-SPECIFIC-AUTHORITY", "url": None, "status": "watch", "use": "exact gate; competent action-specific authority absent", "data_rows_ingested": 0},
    {"source_id": "EXACT-STAGE20-EVIDENCE-AND-AUTHORITY", "url": None, "status": "watch", "use": "exact gate; empirical and authority receipts absent", "data_rows_ingested": 0},
]

STARTUP_FAILURES = [
    ("VA6698-X1-OP-001", "the first memory-registry search used the control workspace as its implicit path and found no file", "a literal memory-registry path recovered the bounded entries read-only"),
    ("VA6698-X1-OP-002", "a broad Git worktree inventory produced slow oversized output", "all later source and lane checks used literal worktree paths and scalar projections"),
    ("VA6698-X1-OP-003", "the current route overlay was first searched as a repository-relative file", "the global skill reference was resolved literally and read through EOF"),
    ("VA6698-X1-OP-004", "one JavaScript orchestration wrapper mixed PowerShell array syntax into JavaScript and was rejected before commands ran", "the wrapper was corrected before any filesystem or repository mutation"),
    ("VA6698-X1-OP-005", "a task reread requested an unsupported output bound", "the accepted bound returned the same existing task read-only"),
    ("VA6698-X1-OP-006", "a historical sparse-path search used a Windows wildcard that Git did not resolve", "exact Git tree and blob reads replaced worktree wildcard assumptions"),
    ("VA6698-X1-OP-007", "an exploratory astronomy title search exceeded the useful output window", "the candidate lens was abandoned and later probes used bounded exact terms"),
    ("VA6698-X1-OP-008", "sparse setup after no-checkout exposed 4012 inherited paths as apparent deletions", "with sparse rules already active git read-tree -mu HEAD materialized the exact sparse index with zero deletions and a clean source head"),
    ("VA6698-X1-OP-009", "the first x1 suite gate-name sanity predicate omitted the explicit cultural and affected-party legitimacy token family", "the isolated predicate was expanded without weakening any protected gate and the targeted witness passed"),
    ("VA6698-X1-OP-010", "the corrected small x1 suite retained a stale hard-coded startup failure count after the prior failure was added", "the isolated bookkeeping assertion now verifies declared-to-row parity with an additive minimum instead of freezing an obsolete count"),
    ("VA6698-X1-OP-011", "the historical Ruff installation was not discoverable as a direct executable on the live process PATH", "the current Python module entrypoint resolved Ruff 0.16.4 without installing or changing the host"),
    ("VA6698-X1-OP-012", "the first scoped Ruff module review found six owner-local quality findings", "two unused imports two explicit subprocess policies one stale suppression and one set-comprehension form were corrected without semantic expansion"),
]


def git_text(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def privacy_candidates(data: str) -> list[dict[str, str]]:
    absolute_path = "(?i)(?:" + "[a-z]" + r":\\" + "|/" + "users" + "/|/" + "home" + "/)" + r"[^\s\"']+"
    checks = {
        "opaque_task_or_thread_identifier": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        "private_absolute_path": absolute_path,
        "credential_or_secret": r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,}\]]+",
        "private_route_scheme": r"(?i)(?:codex|vscode|file|app)://[^\s\"']+",
        "protected_stream_filename": r"(?i)[^\s\"']*(?:transcript|screenshot|session[_-]?stream)[^\s\"']*\.(?:jsonl?|png|jpe?g|webp|log)",
    }
    return [{"class": kind, "state": "candidate_requires_classification"} for kind, pattern in checks.items() if re.search(pattern, data)]


def source_verification(repo: Path) -> dict[str, Any]:
    anchors = [SOURCE_X1, SOURCE_EVIDENCE, SOURCE_FINAL]
    parent_rows = {commit: git_text(repo, "rev-list", "--parents", "-n", "1", commit).split() for commit in anchors}
    baton = subprocess.run(["git", "-C", str(repo), "show", f"{SOURCE_FINAL}:{BATON_PATH}"], check=True, capture_output=True).stdout
    return {
        "activation_baton_git_blob_sha256": sha256_bytes(baton),
        "branch": SOURCE_BRANCH,
        "completion_credit": 0,
        "direct_parent_chain": parent_rows[SOURCE_X1][1] == SOURCE_PRIOR and parent_rows[SOURCE_EVIDENCE][1] == SOURCE_X1 and parent_rows[SOURCE_FINAL][1] == SOURCE_EVIDENCE,
        "exact_final": SOURCE_FINAL,
        "phase_commits": 3,
        "sender_canonical_receipt_sha256": "420fc8d6c0a84cedbb21635f91a0f2f4e43533bfe44694c4c207a2133d8f0726",
        "sender_canonical_state": "one_owner_scoped_success_not_replayed_zero_Vesper_credit",
        "zero_merges": all(len(row) == 2 for row in parent_rows.values()),
    }


def build(repo: Path) -> None:
    corpus, source_shards = inherited_title_corpus(repo)
    proposals = proposal_rows(corpus)
    revalidations = inherited_revalidations(corpus)
    collisions = [row["proposal_id"] for row in proposals if row["visible_title_collision"]]
    quarantined = [row["proposal_id"] for row in proposals if row["semantic_neighbor_quarantined"]]
    if len(proposals) != 40 or len(revalidations) != 20 or collisions or quarantined:
        raise ValueError({"proposal_count": len(proposals), "revalidations": len(revalidations), "collisions": collisions, "quarantined": quarantined})

    root = repo / OWNER_ROOT
    x1 = root / "x1"
    validation = root / "validation"
    for index in range(8):
        write_json(x1 / "proposal-freeze-shards" / f"proposals-{index + 1:02d}.json", {"owner": OWNER, "phase": PHASE, "rows": proposals[index * 5:(index + 1) * 5], "schema": "ghc.family.proposal-freeze-shard.v3", "shard": index + 1})
    expected = {label: sum(row["expected_disposition"] == label for row in proposals) for label in TRUTH_LABELS}
    write_json(x1 / "proposal-freeze.json", {
        "boundary": "Twenty inherited rows are revalidated at zero credit and forty genuinely new proposals are planning hypotheses only.",
        "expected_outcomes": expected,
        "inherited_revalidations": revalidations,
        "mutation_count": 160,
        "owner": OWNER,
        "phase": PHASE,
        "proposal_chain_after": CHAIN_AFTER,
        "proposal_chain_before": SOURCE_CHAIN_DECLARED,
        "rows_total": 60,
        "new_proposal_count": len(proposals),
        "schema": "ghc.family.proposal-freeze.v3",
        "shards": [f"proposal-freeze-shards/proposals-{index:02d}.json" for index in range(1, 9)],
        "strict_x1_only": True,
    })
    maximum = max(proposals, key=lambda row: row["semantic_neighbors"][0]["score"])
    write_json(x1 / "semantic-novelty-audit.json", {
        "accessible_comparison_rows": len(corpus),
        "audit_scope": "exact committed accessible corpus plus within-slate comparisons",
        "declared_inherited_frozen_proposals": SOURCE_CHAIN_DECLARED,
        "exact_title_collisions": collisions,
        "maximum_neighbor": {"proposal_id": maximum["proposal_id"], "neighbor": maximum["semantic_neighbors"][0]},
        "new_proposals": len(proposals),
        "owner": OWNER,
        "phase": PHASE,
        "quarantine_threshold": 0.75,
        "quarantined_proposals": quarantined,
        "recovered_inherited_rows": SOURCE_RECOVERED,
        "schema": "ghc.family.semantic-novelty-audit.v3",
        "source_shards": source_shards,
        "unavailable_history_is_open_gap": True,
        "universal_novelty_claim": False,
        "unrecovered_declared_rows": SOURCE_UNRECOVERED,
    })
    write_json(x1 / "source-ledger.json", {
        "boundary": "Official and primary sources supply vocabulary and constraints only; no samples, measurements, people, records, or authority are ingested.",
        "immutable_source": source_verification(repo),
        "network_source_metadata_reviews": sum(row["url"] is not None for row in SOURCE_ROWS),
        "owner": OWNER,
        "phase": PHASE,
        "review_date": DATE,
        "schema": "ghc.family.source-ledger.v4",
        "sources": SOURCE_ROWS,
    })

    portfolio = {
        "safe_now": portfolio_rows("safe_now", SAFE_TITLES, "safe_now"),
        "candidate": portfolio_rows("candidate", CANDIDATE_TITLES, "candidate"),
        "exact_approval": portfolio_rows("exact_approval", [f"held exact approval packet {i:02d}" for i in range(1, 21)], "exact_approval", "held_unexecuted"),
        "blocked": portfolio_rows("blocked", [f"blocked protected action packet {i:02d}" for i in range(1, 11)], "blocked", "held_unexecuted"),
        "skill": portfolio_rows("skill", SKILL_TITLES, "safe_now"),
        "runner": portfolio_rows("runner", RUNNER_TITLES, "safe_now"),
        "clean_fix_refine": portfolio_rows("clean_fix_refine", REFINE_TITLES, "safe_now"),
    }
    write_json(x1 / "portfolio-freeze.json", {
        "boundary": "Floors structure bounded owner-local work; they do not authorize filler, destructive cleanup, real action, or protected claims.",
        "counts": {kind: len(rows) for kind, rows in portfolio.items()},
        "owner": OWNER,
        "phase": PHASE,
        "practices": PRACTICES,
        "rows": portfolio,
        "schema": "ghc.family.portfolio-freeze.v3",
        "x1_completion_credit": 0,
    })
    successor = {
        "skill": portfolio_rows("successor_skill", SUCCESSOR_SKILLS, "successor_skill", "recommended_not_executed"),
        "runner": portfolio_rows("successor_runner", SUCCESSOR_RUNNERS, "successor_runner", "recommended_not_executed"),
        "clean_fix_refine": portfolio_rows("successor_clean_fix_refine", SUCCESSOR_REFINE, "successor_clean_fix_refine", "recommended_not_executed"),
    }
    write_json(x1 / "successor-recommendations-freeze.json", {
        "completion_credit": 0,
        "counts": {kind: len(rows) for kind, rows in successor.items()},
        "owner": OWNER,
        "phase": PHASE,
        "practice_recommendation": {"practice": "grain-milling quality documentation", "boundary": "learning vocabulary only; no milling, food-safety, equipment, workplace, legal, cultural, or professional authority"},
        "prospective_phase": "v670-v1",
        "prospective_successor": "Lyren Moss",
        "route_binding": "recommendations_only_no_contact_until_exact_terminal_gate",
        "rows": successor,
        "schema": "ghc.family.successor-recommendations.v3",
    })
    write_json(x1 / "tool-candidate-freeze.json", {
        "boundary": "Three D-isolated candidates only; registry metadata is not exhaustive security, legal license review, or production fitness.",
        "install_location_plan": "D-backed phase-namespaced isolated environment",
        "installation_mode": "official wheels pinned by exact direct-wheel SHA-256 with full dependency closure resolved and retained in x2",
        "installation_state": "planned_not_installed_in_x1",
        "owner": OWNER,
        "phase": PHASE,
        "required_x2_gates": ["dependency_closure", "download_hash_match", "isolated_install", "pip_check", "pip_audit", "positive_and_rejecting_smoke", "license_observation", "rollback_receipt", "shared_prefix_mutations_zero"],
        "schema": "ghc.family.tool-candidate-freeze.v2",
        "selected": TOOL_CANDIDATES,
        "target_count": 3,
    })

    failures = [
        {"approval_credit": 0, "failure_id": failure_id, "failed_witness": failure, "passing_bounded_witness": recovery, "preferred_method": recovery, "recurrence_guard": "start with literal scalar read-only probes and inspect state before retry", "rollback": "no source or sibling mutation; retain failure", "state": "retained_zero_credit_with_bounded_recovery"}
        for failure_id, failure, recovery in STARTUP_FAILURES
    ]
    startup = {key: value + len(failures) if key in {"effective_negatives", "methods", "failed_witnesses", "passing_witnesses"} else value for key, value in INHERITED_BASELINE.items()}
    write_json(x1 / "startup-operational-failures.json", {
        "boundary": "Every startup failure remains visible and earns zero completion credit.",
        "effective_startup_baseline": startup,
        "failure_count": len(failures),
        "inherited_activation_baseline": INHERITED_BASELINE,
        "owner": OWNER,
        "phase": PHASE,
        "rows": failures,
        "schema": "ghc.family.method-flow-startup-overlay.v3",
    })
    write_json(x1 / "workflow-plan-freeze.json", {
        "commit_ceiling": {"x1": 5, "x2": 5, "total": 8},
        "current_stage": "x1_planning_only",
        "document_word_ceiling": 100000,
        "file_ceiling": 2000,
        "gates": ["x1 build parse novelty privacy tests and staged Git-blob review", "dedicated x1 commit push clean fresh-live equality", "x2 execute frozen controls as evidence permits", "immutable evidence commit push clean fresh-live equality", "closeout and final seal", "one exact-final owner-scoped canonical invocation with no success replay", "post-terminal live roster auth usage privacy safety evidence duplicate guard"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.workflow-plan-freeze.v4",
        "strict_x1_before_x2": True,
    })
    write_json(x1 / "reflection-plan.json", {
        "changed_choices": ["rejected astronomy and other colliding lenses after bounded accessible-corpus probes", "selected wholly synthetic sourdough process assurance after zero exact sourdough-family collision", "retained the 3570-title recovery gap", "selected Pint transitions and portion for isolated quantities states and intervals"],
        "owner": OWNER,
        "phase": PHASE,
        "recurrence_guards": ["hash Git blobs rather than Windows working-tree bytes", "use literal source and worktree probes", "inspect sparse state before retry", "never replay a successful canonical aggregate", "never treat dependency recovery as canonical success"],
        "schema": "ghc.family.reflection-plan.v3",
    })
    versions = {
        "codex_cli": subprocess.run(["codex", "--version"], capture_output=True, text=True, check=False).stdout.strip() or "observed_unavailable",
        "desktop_update": "not_performed",
        "git": subprocess.run(["git", "--version"], capture_output=True, text=True, check=True).stdout.strip(),
        "node": subprocess.run(["node", "--version"], capture_output=True, text=True, check=True).stdout.strip(),
        "python": platform.python_version(),
        "updates_or_host_changes": 0,
    }
    write_json(x1 / "environment-version-receipt.json", {"owner": OWNER, "phase": PHASE, "schema": "ghc.family.version-observation.v3", **versions})
    write_json(x1 / "phase-truth.json", {
        "core_truth_labels": TRUTH_LABELS,
        "expected_outcomes": expected,
        "identity_boundary": IDENTITY_BOUNDARY,
        "owner": OWNER,
        "phase": PHASE,
        "primary_pillar": "THOS Body",
        "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "proposal_chain": {"before": SOURCE_CHAIN_DECLARED, "after_if_frozen": CHAIN_AFTER},
        "proposal_rows": {"inherited_zero_credit": 20, "new": 40, "total": 60},
        "real_world_actions": 0,
        "schema": "ghc.family.phase-truth.x1.v3",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "x1_completion_credit": 0,
        "x2_execution_started": False,
    })
    write_json(x1 / "route-state.json", {
        "current_phase": PHASE,
        "delivery_acknowledged": False,
        "delivery_state": "PREPARED_NOT_SENT",
        "owner": OWNER,
        "prospective_next_edge": "unique existing exact-title Lyren Moss for v670-v1 only after exact terminal gate and fresh authority reread",
        "schema": "ghc.family.route-state.v3",
        "successor_contact_count": 0,
        "stale_rejected_label": "Vesper Rowan",
    })
    write_text(x1 / "threat-model.md", """# Vesper Arlen v669-v8 x1 threat model

This planning-only threat model covers source or sibling mutation, x1/x2 leakage, semantic duplication, private-route disclosure, false baking, microbiology, food-safety, public-health, HACCP, measurement, legal, cultural, or Maori-authority competence, real food handling, allergen or sanitation advice, microbial or sensory inference, identity promotion, accessibility or privacy completeness, scientific analogy conversion, toolchain contamination, canonical replay, and premature successor delivery.

Controls are one additive D-first sparse lane; exact source anchors and Git-blob manifests; zero-person, zero-food, zero-sample, zero-measurement, zero-operation, zero-real-advice, zero-adapter, and zero-authority counters; four exact truth labels; append-only Method Flow; exact protected gates; phase-isolated tool installation; structural accessibility with manual evaluation reserved; and one terminally gated route. Residual risk remains because same-owner synthetic checks cannot supply independent review, professional judgment, legal or cultural interpretation, affected-party legitimacy, Maori authority, privacy or accessibility completeness, production fitness, empirical GMUT evidence, or Stage 20 authority.
""")
    write_text(x1 / "accessible-report-plan.md", """# Accessible static report plan

The x2 report will use a skip link, labelled navigation, landmarks, one top-level heading, scoped table headers, captions, text labels beyond colour, visible focus, print rules, and reduced-motion rules. It will contain no scripts, forms, tracking, or external runtime dependency.

Structural checks are bounded software evidence only. Manual browser, keyboard, zoom, assistive-technology, screen-reader, cognitive-accessibility, Maori-language, and affected-user evaluations remain reserved. No complete-accessibility claim is permitted.
""")
    write_text(x1 / "integrated-overview.md", f"""# Vesper Arlen v669-v8 x1 integrated planning overview

## Identity and phase purpose

{IDENTITY_BOUNDARY} The phase role is provenance weaver and reversible-process cartographer. The hope is to make state, correction, uncertainty, and authority boundaries legible without turning a synthetic process model into food, scientific, or social authority. THOS Body is primary; GMUT Mind and Freed ID/CBR Heart remain explicit and protected.

The three human-practice lenses are baker/process handover, food-microbiology laboratory measurement provenance, and HACCP-style review vocabulary. They are learning and software-design lenses only. The phase uses zero real people, food, starters, ingredients, samples, records, images, equipment, kitchens, bakeries, laboratories, workplaces, measurements, assays, preparation, fermentation, baking, tasting, sanitation, disposal, professional decisions, safety releases, legal interpretations, cultural decisions, Maori-authority acts, or external operations.

## Source and novelty truth

The immutable source is Neris Solane's clean exact final `{SOURCE_FINAL}` with direct planning x1 and immutable-evidence ancestry. Neris's owner-scoped aggregate succeeded once and is not replayed or claimed as Vesper evidence. The accessible novelty corpus contains {SOURCE_RECOVERED} exact committed titles. The declared chain contains {SOURCE_CHAIN_DECLARED}; the remaining {SOURCE_UNRECOVERED} titles remain an open semantic-recovery gap. Twenty inherited rows receive zero Vesper novelty and completion credit. Forty new sourdough-specific rows are checked against the accessible corpus and each other with exact-title and 0.75 token-Jaccard quarantine. No universal novelty claim is made.

## Frozen program and portfolios

The forty new proposals freeze expected dispositions of twenty-eight completed, eight represented, two open gaps, and two exact gates. Each completion or representation lane freezes one bounded positive and four rejecting mutations. Completed means only that an owner-local synthetic contract accepts its declared positive and rejects missing state, ambiguity, external action, and protected-claim promotion. Represented means a proxy stays visible without operational or empirical promotion. Gaps and exact gates remain open by design.

The owner portfolio freezes sixty safe-now rows, thirty candidates, twenty exact-approval packets held unexecuted, ten blocked packets held unexecuted, twenty skill ideas, ten runner ideas, and sixty additive CLEAN/FIX/REFINE rows. Successor recommendations freeze ten skills, ten runners, thirty CLEAN/FIX/REFINE rows, and exactly one bounded practice recommendation: grain-milling quality documentation. Counts structure work; they do not authorize filler or unsafe action.

## Sources and isolated tool candidates

NIST and IUPAC sources supply units, pH, and chemical-potential vocabulary. A public sourdough review supplies ecology vocabulary without transferring its study data or findings. The FDA Food Code supplies a comparison vocabulary only; it is not New Zealand law, compliance, or advice. W3C, JSON Schema, RFC, New Zealand privacy, and Te Mana Raraunga surfaces supply formal or authority-reservation vocabulary only. No external data row is ingested.

Pint 0.25.3, transitions 0.9.3, and portion 2.6.2 are frozen from official registry metadata with exact direct-wheel hashes. X2 may install their audited dependency closure only into a phase-namespaced D-backed environment after hash, license-observation, compatibility, rollback, pip-check, pip-audit, positive, and rejecting gates. Shared Python, npm, Windows, and Codex surfaces remain untouched. Installation cannot establish exhaustive supply-chain security, legal license interpretation, production fitness, or numerical validity beyond bounded fixtures.

## Trinity, rights, and terminal boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Reaction-diffusion, Arrhenius, chemical-potential, pH, interval, or process analogies establish no likelihood, parameter constraint, detected force, prediction, physical law, psyche law, consciousness, empirical confirmation, final physics, quantum or ultraviolet completion, Theory of Everything, proof, or canon. THOS remains proxy-only without governed blind matched-budget real arms, people, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, issuance, verification, resolution, status, revocation, interoperability, recovery, privacy and security review, trust governance, and affected-party oversight.

Professional practice, food safety, public health, allergens, sanitation, labeling, workplace rights, privacy, accessibility, remedy, law, culture, traditional knowledge, affected-party legitimacy, Maori wording, Maori concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority remain open or exact-gated. The verdict remains `NOT_READY_FOR_STAGE_20`.

## Lifecycle

X1 contains planning only: sources, novelty, proposal and portfolio freezes, threat model, route, environment observation, failure retention, tests, manifests, and rollback. X2 implementation, observed outcomes, evidence receipts, closeout, final seal, and successor delivery are absent. X2 may begin only after the dedicated x1 commit is pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote. The exact final will receive at most one attributable owner-scoped canonical invocation. A success is never replayed; a failure retains zero aggregate-success credit and permits only smallest-dependency recovery unless exact impact requires more.
""")
    write_text(repo / "ghc-family-index/references/v669-v8-vesper-arlen.md", """# Vesper Arlen v669-v8 phase index

- Owner and exact existing-task title: `Vesper Arlen`; `Vesper Rowan` is a stale rejected label only.
- Immutable source: Neris Solane v669-v7 exact final.
- Stage at x1 freeze: planning only; no x2 result or successor contact.
- Primary pillar: THOS Body; GMUT Mind and Freed ID/CBR Heart protected.
- Lens: wholly synthetic sourdough process documentation and software assurance.
- Portfolio: 20 inherited zero-credit revalidations, 40 new proposals, 60 safe-now, 30 candidates, 20 exact, 10 blocked, 20 owner skills, 10 owner runners, 60 owner refinements, and bounded successor recommendations.
- Terminal verdict: `NOT_READY_FOR_STAGE_20`.
""")

    json_paths = sorted(x1.rglob("*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    public_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(root.rglob("*")) if path.is_file())
    privacy = privacy_candidates(public_text)
    write_json(validation / "x1-validation-receipt.json", {
        "checks": {"accessible_rows": len(corpus), "collision_count": len(collisions), "inherited_revalidations": len(revalidations), "json_parse_count": len(json_paths), "new_proposals": len(proposals), "privacy_candidates": privacy, "quarantine_count": len(quarantined), "source_count": len(SOURCE_ROWS), "startup_failures_retained": len(failures), "truth_labels": TRUTH_LABELS, "x2_paths": 0},
        "owner": OWNER,
        "passed": not privacy and len(corpus) == SOURCE_RECOVERED and len(proposals) == 40 and len(revalidations) == 20 and not collisions and not quarantined,
        "phase": PHASE,
        "schema": "ghc.family.x1-validation-receipt.v3",
        "strict_planning_only": True,
    })


def staged_review(repo: Path) -> None:
    exclusions = [MANIFEST_PATH, REVIEW_PATH]
    entries = staged_blob_manifest(repo, exclusions)
    paths = [row["path"] for row in entries]
    x2_paths = [path for path in paths if "/x2/" in path]
    forbidden = [path for path in paths if any(token in path.lower() for token in ("/closeout/", "/seal/", "/final/", "/handoffs/"))]
    json_errors: list[str] = []
    privacy: list[dict[str, str]] = []
    for path in paths:
        data = subprocess.run(["git", "-C", str(repo), "show", f":{path}"], check=True, capture_output=True).stdout
        if path.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
            except Exception as exc:  # noqa: BLE001
                json_errors.append(f"{path}:{type(exc).__name__}")
        privacy.extend({"path": path, **row} for row in privacy_candidates(data.decode("utf-8", errors="replace")))
    write_json(repo / MANIFEST_PATH, {"domain": "x1_staged_planning_git_blobs", "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.exact-git-blob-manifest.v3", "self_exclusions": exclusions, "source_commit": SOURCE_FINAL})
    checks = {
        "diff_cached_check": subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--check"], capture_output=True, check=False).returncode == 0,
        "forbidden_lifecycle_paths": forbidden,
        "json_errors": json_errors,
        "manifest_entries": len(entries),
        "owner_generated_file_ceiling": len(paths) < 2000,
        "privacy_candidates": privacy,
        "strict_x1_no_x2_paths": not x2_paths,
        "x2_paths": x2_paths,
    }
    write_json(repo / REVIEW_PATH, {"checks": checks, "owner": OWNER, "passed": checks["diff_cached_check"] and not forbidden and not json_errors and checks["owner_generated_file_ceiling"] and not privacy and not x2_paths, "phase": PHASE, "schema": "ghc.family.x1-staged-review.v3", "self_exclusions": exclusions})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--stage-review", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    staged_review(repo) if args.stage_review else build(repo)


if __name__ == "__main__":
    main()

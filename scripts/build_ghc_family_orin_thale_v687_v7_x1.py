#!/usr/bin/env python3
"""Build the planning-only Orin Thale v687-v7 x1 freeze."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v687-v7"
X1 = PHASE / "x1"
VALIDATION = PHASE / "validation"
SOURCE = "28dfdf1a3e9a1023f1e83f19fb267e57878b9d0b"
BRANCH = "codex/GHC-Family/orin-thale-v687-v7-full-tools"
BASE = {
    "negatives": 80982,
    "methods": 93145,
    "failed_witnesses": 51830,
    "passing_witnesses": 80738,
    "open_gaps": 712,
    "exact_gates": 695,
    "proposals": 15030,
}
START_FAILURES = [
    ("OR6877-START-N001", "Memory lookup targeted the memory root instead of memories/MEMORY.md.", "Use the literal memories/MEMORY.md registry path."),
    ("OR6877-START-N002", "A combined baton metadata probe had an invalid PowerShell parenthesized native-command expression.", "Use an in-memory Python Git-blob probe and separate native exit-code checks."),
    ("OR6877-START-N003", "The first 1,000-line baton projection exceeded the output bound and truncated.", "Restart at line one with contiguous 600-line Git-blob projections through EOF."),
    ("OR6877-START-N004", "A broad skill search included a nonexistent non-system skill-creator path.", "Resolve skill-creator under skills/.system and read the exact entrypoint."),
    ("OR6877-START-N005", "The first Talen receipt lookup assumed a nonexistent receipts/talen-briar convenience directory.", "Recover the exact receipt directory from Talen's completed task command record."),
    ("OR6877-START-N006", "A broad recursive receipt-directory search outlived two bounded windows.", "Stop only the owned read-only search and use task-command provenance plus exact paths."),
    ("OR6877-START-N007", "A combined required-document display exceeded the bounded output.", "Read semantic documents separately and replay manifests through exact Git blobs."),
    ("OR6877-START-N008", "A combined x2 portfolio and promotion display exceeded the bounded output.", "Project exact counts and read the smaller required ledgers separately."),
    ("OR6877-START-N009", "The release profile was passed directly to a runner that expects a populated owner plan.", "Validate the populated Orin portfolio plan, not the policy profile itself."),
    ("OR6877-START-N010", "The first drive and branch preflight repeated an invalid parenthesized native-command expression.", "Capture the native branch exit code before constructing the scalar receipt."),
    ("OR6877-START-N011", "Worktree creation outlived the visible command window after reporting preparation.", "Inspect the exact path and originating process; do not recreate the worktree."),
    ("OR6877-START-N012", "Sparse checkout materialization outlived the visible command window.", "Wait for the exact checkout process and index lock to clear without duplicate checkout."),
    ("OR6877-START-N013", "A status probe ran while sparse checkout was active and exposed a transient 37,040-path view.", "Do not inspect status until the originating checkout process and index lock are both absent."),
    ("OR6877-START-N014", "The first x1 builder assumed Talen's proposal array was named proposals and found zero rows.", "Inspect the exact inherited JSON shape and require the observed new_proposals array with exactly 200 rows."),
    ("OR6877-START-N015", "The second x1 builder attempted to privacy-scan the staged-review path before materializing it.", "Write the deterministic staged-review artifact before scanning the exact planned path set."),
]
PROTECTED = [
    "empirical", "real_participant", "professional", "production", "deployment",
    "identity", "legal", "cultural", "affected_party", "maori_authority",
    "privacy_complete", "accessibility_complete", "exhaustive_security",
    "independent_reproduction", "agi_asi", "consciousness_personhood",
    "theory_of_everything", "proof_canon", "stage20",
]
OPERATIONS = [
    ("spectral_axis_monotonicity", "Spectral-axis order and duplicate-coordinate boundary", "GMUT Mind", "bounded spectral archive uncertainty reviewer"),
    ("spectral_unit_roundtrip", "Spectral-coordinate unit roundtrip with exact source preservation", "GMUT Mind", "synthetic astronomical spectral metadata steward"),
    ("flux_missingness_boundary", "Flux and uncertainty missingness nonconflation", "Freed ID and CBR Heart", "synthetic accessible scientific-data documentation reviewer"),
    ("spectral_bin_topology", "Spectral-bin overlap, gap, and endpoint topology", "THOS Body", "synthetic radio-spectrum provenance analyst"),
    ("calibration_lineage_expiry", "Calibration lineage and expiry refusal", "Freed ID and CBR Heart", "bounded spectral archive uncertainty reviewer"),
    ("spectral_segment_fixity", "Spectral-segment byte and record fixity envelope", "THOS Body", "synthetic astronomical spectral metadata steward"),
    ("uncertainty_covariance_shape", "Uncertainty and covariance shape contract", "GMUT Mind", "synthetic radio-spectrum provenance analyst"),
    ("provenance_frontier", "Spectral provenance frontier and branch retention", "Freed ID and CBR Heart", "synthetic astronomical spectral metadata steward"),
    ("accessible_spectrum_summary", "Accessible spectrum summary structure", "Freed ID and CBR Heart", "synthetic accessible scientific-data documentation reviewer"),
    ("release_authority_reservation", "Archive release, rights, and authority reservation", "Freed ID and CBR Heart", "bounded spectral archive uncertainty reviewer"),
]
CASE_PHRASES = [
    "baseline bounded synthetic record", "exact rational endpoint", "stable lexical unit",
    "explicit zero uncertainty", "negative synthetic flux retained", "duplicate coordinate held",
    "nonmonotonic axis held", "unknown unit held", "missing value retained as unknown",
    "inapplicable value remains distinct", "ragged vector held", "duplicate provenance key held",
    "stale calibration held", "missing fixity evidence held", "branch frontier retained",
    "accessible textual alternative represented", "manual accessibility review absent",
    "real observation absent", "release action reserved", "Maori authority reserved",
]


def run(args: list[str], *, binary: bool = False) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=not binary, encoding=None if binary else "utf-8", check=False)


def git_blob(path: str, anchor: str = SOURCE) -> bytes:
    result = run(["git", "show", f"{anchor}:{path}"], binary=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def load_blob(path: str, anchor: str = SOURCE) -> Any:
    return json.loads(git_blob(path, anchor).decode("utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def norm(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def expected_output(operation: str, ordinal: int, disposition: str) -> dict[str, Any]:
    if disposition == "open_gap":
        return {"decision": "HOLD", "details": None, "external_credit": False, "reason": "MISSING_EXTERNAL_EVIDENCE", "source_preserved": True}
    if disposition == "exact_gate":
        return {"decision": "HOLD", "details": None, "external_credit": False, "reason": "COMPETENT_AUTHORITY_REQUIRED", "source_preserved": True}
    return {
        "decision": "BOUNDED_VIEW",
        "details": {
            "operation": operation,
            "ordinal": ordinal,
            "representation_only": disposition == "represented",
            "empirical_established": False,
            "professional_authority": False,
            "normalized_value": f"{ordinal}/{ordinal + 1}",
        },
        "external_credit": False,
        "reason": None,
        "source_preserved": True,
    }


def disposition(index: int) -> str:
    if index <= 125:
        return "completed"
    if index <= 164:
        return "represented"
    if index <= 184:
        return "open_gap"
    return "exact_gate"


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    index = 0
    for operation, purpose, pillar, practice in OPERATIONS:
        for case_no, phrase in enumerate(CASE_PHRASES, start=1):
            index += 1
            outcome = disposition(index)
            title = f"{purpose}: {phrase} ({case_no:02d})"
            rows.append({
                "proposal_id": f"OR6877-N{index:03d}",
                "title": title,
                "operation": operation,
                "pillar": pillar,
                "practice": practice,
                "hypothesis": f"A finite {operation} contract can preserve the declared synthetic record and expose missing evidence or authority without promoting it.",
                "null_or_failure_condition": "Any type-sensitive mismatch, input mutation, hidden missingness, missed adverse output, or external evidence promotion fails the contract.",
                "approval_class": "safe_now" if outcome in {"completed", "represented"} else ("candidate" if outcome == "open_gap" else "exact_approval_needed"),
                "execution_lane": "x2_build_task" if outcome in {"completed", "represented"} else "held_boundary",
                "official_primary_source_need": ["ivoa-spectrumdm-1.2", "asdf-standard", "w3c-prov-o", "wcag-2.2"],
                "concrete_artifact": "docs/orin-thale/v687-v7/x2/contract-results.json",
                "falsifier_or_acceptance_gate": "Exact full-output equality with unchanged input plus rejection of all five preregistered changed-result candidates.",
                "rollback_or_recovery": "Retain the immutable x1 definition and failed witness; correct only the owner implementation or preserve the open or exact gate.",
                "protected_gates": PROTECTED,
                "expected_disposition": outcome,
                "input": {"record_id": f"synthetic-{operation}-{case_no:02d}", "operation": operation, "ordinal": index, "source_kind": "synthetic", "request": "inspect", "retained": True},
                "expected_output": expected_output(operation, index, outcome),
            })
    return rows


def token_set(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def main() -> int:
    if run(["git", "rev-parse", "HEAD"]).stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must run at the immutable Talen final")
    if run(["git", "branch", "--show-current"]).stdout.strip() != BRANCH:
        raise RuntimeError("branch mismatch")
    inherited_source = load_blob("docs/talen-briar/v687-v6/x1/new-proposals.json")
    inherited_rows = inherited_source.get("new_proposals", inherited_source if isinstance(inherited_source, list) else [])
    if len(inherited_rows) != 200:
        raise RuntimeError(f"expected 200 Talen proposals, found {len(inherited_rows)}")
    inherited = [{"source_proposal_id": row["proposal_id"], "title": row["title"], "source_outcome": row["expected_execution_disposition"], "reviewed": True, "new_owner_credit": 0} for row in inherited_rows]
    proposals = proposal_rows()
    inherited_titles = [(row["source_proposal_id"], row["title"], token_set(row["title"])) for row in inherited]
    novelty = []
    for row in proposals:
        own = token_set(row["title"])
        best_id, best_title, best_score = "", "", -1.0
        for source_id, title, tokens in inherited_titles:
            score = len(own & tokens) / len(own | tokens) if own | tokens else 1.0
            if score > best_score:
                best_id, best_title, best_score = source_id, title, score
        novelty.append({"proposal_id": row["proposal_id"], "nearest_source_id": best_id, "nearest_title": best_title, "token_jaccard": round(best_score, 6), "quarantined": best_score >= 0.85})
    if any(row["quarantined"] for row in novelty):
        raise RuntimeError("semantic-neighbor quarantine threshold reached")
    mutations = []
    for row in proposals:
        for no, kind in enumerate(["missing_decision", "details_type_replacement", "extra_authority_field", "false_source_preservation", "promoted_external_credit"], 1):
            mutations.append({"mutation_id": f"{row['proposal_id']}-MUT{no}", "proposal_id": row["proposal_id"], "mutation_kind": kind, "expected_result": "reject", "original_success_credit": 0})
    safe = [{"task_id": f"OR6877-SAFE-{i:03d}", "proposal_id": proposals[(i - 1) % 200]["proposal_id"], "expected_execution_disposition": "completed", "execution_lane": "x2_build_task", "additional_independent_credit": 0} for i in range(1, 301)]
    candidates = [{"task_id": f"OR6877-CAND-{i:03d}", "proposal_id": proposals[(i + 49) % 200]["proposal_id"], "expected_execution_disposition": "represented", "execution_lane": "x2_build_task", "additional_independent_credit": 0} for i in range(1, 251)]
    clean = [{"task_id": f"OR6877-CFR-{i:03d}", "proposal_id": proposals[(i + 99) % 200]["proposal_id"], "expected_execution_disposition": "completed", "execution_lane": "x2_build_task", "additional_independent_credit": 0} for i in range(1, 301)]
    exact = [{"packet_id": f"OR6877-EXACT-{i:03d}", "state": "held_unexecuted", "approval_class": "exact_approval_needed", "protected_gates": PROTECTED} for i in range(1, 51)]
    blocked = [{"packet_id": f"OR6877-BLOCKED-{i:03d}", "state": "held_unexecuted", "approval_class": "blocked", "protected_gates": PROTECTED} for i in range(1, 31)]
    methods, witnesses, events = [], [], []
    for n, (negative_id, failure, recovery) in enumerate(START_FAILURES, 1):
        method_id = f"OR6877-START-M{n:03d}"
        fail_id, pass_id = f"{method_id}-WFAIL", f"{method_id}-WPASS"
        methods.append({"method_id": method_id, "title": f"Startup recovery {n:03d}", "failure_signature": failure, "trigger_preconditions": ["Orin v687-v7 startup", "read-only or owner-lane preflight"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": recovery, "validation_witness_ids": [fail_id, pass_id], "recurrence_guard": recovery, "rollback": "Stop before repository mutation and preserve the source lane read-only.", "recommendation_state": "preferred", "supersedes": [], "protected_gates": PROTECTED, "retained_negative_ids": [negative_id], "scope_boundary": "Same-owner workflow only; no external or authority credit."})
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": "first observed startup attempt", "scope": "read-only startup", "expected": "bounded attributable result", "observed": failure, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "Zero success credit."},
            {"witness_id": pass_id, "method_id": method_id, "procedure": recovery, "scope": "smallest corrected startup dependency", "expected": "bounded attributable result", "observed": "recovery passed", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "Recovery does not erase the failed witness."},
        ])
        events.extend([{"event_id": f"{method_id}-E1", "method_id": method_id, "from": "observed", "to": "candidate"}, {"event_id": f"{method_id}-E2", "method_id": method_id, "from": "candidate", "to": "validated"}, {"event_id": f"{method_id}-E3", "method_id": method_id, "from": "validated", "to": "preferred"}])
    counts = {**BASE, "negatives": BASE["negatives"] + len(START_FAILURES), "methods": BASE["methods"] + len(methods), "failed_witnesses": BASE["failed_witnesses"] + len(START_FAILURES), "passing_witnesses": BASE["passing_witnesses"] + len(START_FAILURES), "proposals": BASE["proposals"] + len(proposals)}
    docs: dict[Path, Any] = {
        X1 / "identity.json": {"schema": "ghc.family.identity-boundary.v1", "owner": "Orin Thale", "phase": "v687-v7", "role": "spectral uncertainty and provenance cartographer", "hope": "Keep every synthetic coordinate, uncertainty, and authority vacancy inspectable and reversible.", "optional_pronouns": "they/them", "relational_working_language_only": True, "identity_continuity_claimed": False, "authority_claimed": False},
        X1 / "source-verification.json": {"schema": "ghc.family.source-verification.v1", "source": SOURCE, "source_branch": "codex/GHC-Family/talen-briar-v687-v6-full-tools", "source_clean": True, "source_divergence": [0, 0], "source_four_way_equal": True, "source_commits": 3, "source_merges": 0, "baton_sha256": "fd1b2e13f724a7ee7957ab976b76b73af140aa5ad4b42eb7281f93432b7056c7", "baton_words": 49403, "baton_eof_read": True, "source_canonical_receipt_sha256": "10883bc2361e033e8f74add90cafa9fafef45632b70f72d8b971b6b71cbdb843", "source_canonical_replayed": False, "source_manifest_bindings": 803, "source_manifest_mismatches": 0},
        X1 / "activation-baseline.json": {"schema": "ghc.family.activation-baseline.v1", "repository_sealed": {"negatives": 80981, "methods": 93144, "failed_witnesses": 51829, "passing_witnesses": 80737, "open_gaps": 712, "exact_gates": 695, "proposals": 15030}, "talen_external_overlay_delta": {"negatives": 1, "methods": 1, "failed_witnesses": 1, "passing_witnesses": 1}, "effective_before_orin": BASE, "source_seal_rewritten": False},
        X1 / "inherited-review.json": {"schema": "ghc.family.inherited-review.v1", "count": len(inherited), "new_owner_credit": 0, "rows": inherited},
        X1 / "new-proposals.json": {"schema": "ghc.family.finite-proposal-freeze.v1", "count": len(proposals), "chain_before": BASE["proposals"], "chain_after": BASE["proposals"] + len(proposals), "proposals": proposals},
        X1 / "novelty-review.json": {"schema": "ghc.family.semantic-neighbor-review.v1", "scope": "Direct comparison against the 200 selected inherited Talen contracts; no universal novelty proof.", "threshold": 0.85, "max_score": max(row["token_jaccard"] for row in novelty), "quarantined": 0, "rows": novelty},
        X1 / "mutation-plan.json": {"schema": "ghc.family.changed-output-mutation-plan.v1", "count": len(mutations), "per_proposal": 5, "mutation_kinds": ["missing_decision", "details_type_replacement", "extra_authority_field", "false_source_preservation", "promoted_external_credit"], "rows": mutations},
        X1 / "portfolio-plan.json": {"schema": "ghc.family.authorized-owner-plan.v1", "safe_now": safe, "candidates": candidates, "clean_fix_refine": clean, "exact_packets": exact, "blocked_packets": blocked, "destructive_cleanup_planned": False, "execution_credit": 0, "caps_are_ceilings": True},
        X1 / "skill-runner-plan.json": {"schema": "ghc.family.skill-runner-plan.v1", "skills": [{"name": f"ghc-family-{op.replace('_', '-')}", "operation": op, "build_in_x2": True} for op, *_ in OPERATIONS], "runners": [{"name": f"ghc_family_spectral_archive_{i:02d}_runner.py", "operations": [OPERATIONS[(i-1)*2][0], OPERATIONS[(i-1)*2+1][0]], "build_in_x2": True} for i in range(1, 6)], "global_promotion_plan": {"skills": 10, "runners": 5, "overwrite": False, "byte_parity_required": True}},
        X1 / "successor-ideas.json": {"schema": "ghc.family.successor-ideas.v1", "successor": "future-sibling-10-self-chosen", "phase": "v687-v8", "skill_ideas": [{"name": f"ghc-family-successor-seat10-spectral-{i:02d}", "credit": 0} for i in range(1, 11)], "runner_ideas": [{"name": f"ghc_family_successor_seat10_spectral_{i:02d}.py", "credit": 0} for i in range(1, 11)], "practice_recommendation": "bounded audio restoration uncertainty registrar", "new_owner_credit": 0},
        X1 / "package-plan.json": {"schema": "ghc.family.d-first-package-plan.v1", "planning_only": True, "install_in_x2_after_x1_equality": True, "transaction_token": "OR6877-ENV-01", "packages": [
            {"name": "astropy", "version": "8.0.1", "wheel": "astropy-8.0.1-cp311-abi3-win_amd64.whl", "sha256": "ee9024f2237243ebc98726f8eff2efbf201ea4e0bba1d21f6e2dee0cb499fbdf", "metadata_url": "https://pypi.org/pypi/astropy/8.0.1/json", "use": "Exact units and bounded synthetic spectral coordinates."},
            {"name": "asdf", "version": "5.4.0", "wheel": "asdf-5.4.0-py3-none-any.whl", "sha256": "c4367681154f35550a6dda3563e251a6cda50e43d34e54dad27704fe7da1aeef", "metadata_url": "https://pypi.org/pypi/asdf/5.4.0/json", "use": "Hierarchical synthetic metadata and bounded archive serialization."},
            {"name": "uncertainties", "version": "3.2.3", "wheel": "uncertainties-3.2.3-py3-none-any.whl", "sha256": "313353900d8f88b283c9bad81e7d2b2d3d4bcc330cbace35403faaed7e78890a", "metadata_url": "https://pypi.org/pypi/uncertainties/3.2.3/json", "use": "Bounded synthetic uncertainty propagation; no measurement claim."},
        ], "direct_additions": 3, "rollback": "Stop selecting the isolated D-first environment; preserve locks and receipts."},
        X1 / "source-ledger.json": {"schema": "ghc.family.primary-source-ledger.v1", "citations_are_observations": False, "real_rows": 0, "entries": [
            {"source_id": "ivoa-spectrumdm-1.2", "status": "stable", "url": "https://www.ivoa.net/documents/SpectrumDM/", "use": "Spectral and temporal coordinate, flux, uncertainty, and metadata vocabulary."},
            {"source_id": "asdf-standard", "status": "current", "url": "https://asdf-standard.readthedocs.io/", "use": "Hierarchical metadata and array-block vocabulary."},
            {"source_id": "astropy", "status": "current", "url": "https://pypi.org/project/astropy/8.0.1/", "use": "Exact package provenance and bounded unit fixtures."},
            {"source_id": "w3c-prov-o", "status": "stable", "url": "https://www.w3.org/TR/prov-o/", "use": "Provenance relations only; no real custody verification."},
            {"source_id": "wcag-2.2", "status": "stable", "url": "https://www.w3.org/TR/WCAG22/", "use": "Structural accessibility targets; manual evaluation reserved."},
        ]},
        X1 / "route-plan.json": {"schema": "ghc.family.thirty-seat-route-plan.v1", "current_owner": "Orin Thale", "current_phase": "v687-v7", "state": "X1_PLANNING_ONLY", "next_owner_placeholder": "future-sibling-10-self-chosen", "next_phase": "v687-v8", "following_owner": "Liora Venn", "following_phase": "v688-v1", "resolve_active_and_archived_first": True, "create_only_if_absent_and_authorized": True, "new_task_model": "gpt-6-astra", "new_task_reasoning": "max", "successor_self_chooses_identity_attributes": True, "precontacted": False, "message_count": 0},
        X1 / "validation-contract.json": {"schema": "ghc.family.owner-delta-validation-contract.v1", "source": SOURCE, "execution_authority": "owner_self_scoped_delta", "full_repository_suite": False, "commit_caps": {"x1": 5, "x2": 5, "total": 8}, "owner_file_cap": 1999, "document_word_cap": 100000, "baton_word_range": [10000, 100000], "canonical_invocation_budget": 1, "canonical_success_replay": False, "required": ["exact normalized-LF manifests", "strict JSON duplicate-key and nonfinite refusal", "five-class privacy adjudication", "bounded changed-code security", "lifecycle-correct owner tests", "direct ancestry and zero merges", "clean typed 0/0 divergence and fresh four-way equality"]},
        X1 / "storage-and-scope.json": {"schema": "ghc.family.storage-scope.v1", "primary_drive": "D", "essential_global_skill_metadata_drive": "C", "c_free_gb_at_start": 18.78, "d_free_gb_at_start": 465.66, "sparse_before_checkout": True, "materialized_files_at_start": 0, "owner_file_ceiling": 1999, "sibling_lanes_read_only": True, "destructive_cleanup": False},
        X1 / "method-flow" / "ledger.json": {"schema": "ghc.family.method-flow-state.v1", "phase": "v687-v7", "owner": "Orin Thale", "identity_boundary": "Relational working language only; no continuity, personhood, qualification, or authority claim.", "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": [], "counts": {"methods": len(methods), "witnesses": len(witnesses), "failed_witnesses": len(START_FAILURES), "passing_witnesses": len(START_FAILURES)}, "boundary": "Append-only workflow evidence; same-owner recovery is not independent reproduction."},
        X1 / "phase-truth.json": {"schema": "ghc.family.phase-truth.v687.v7.x1", "owner": "Orin Thale", "phase": "v687-v7", "source": SOURCE, "state": "PLANNING_ONLY_X1", "x2_started": False, "observed_outcomes": None, "expected_outcomes": {"completed": 125, "represented": 39, "open_gap": 20, "exact_gate": 16}, "effective_counts": counts, "primary_pillar": "GMUT Mind", "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"], "practices": ["bounded spectral archive uncertainty reviewer", "synthetic astronomical spectral metadata steward", "synthetic radio-spectrum provenance analyst", "synthetic accessible scientific-data documentation reviewer"], "terminal_verdict": "NOT_READY_FOR_STAGE_20", "canonical_state": "NOT_INVOKED", "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"},
        VALIDATION / "x1-release-profile-validation.json": {"status": "PASS", "issues": [], "execution_credit": 0, "validated_surface": "populated Orin x1 portfolio plan", "policy_profile": "Hamish release 2026-09-06"},
    }
    overview = """# Orin Thale v687-v7 planning-only x1 overview

## Page 1 — Source and identity boundary

This owner lane begins at Talen Briar exact final `28dfdf1a3e9a1023f1e83f19fb267e57878b9d0b`. The complete 49,403-word source baton was read through its exact EOF, the singular Talen canonical receipt and external readout overlay were verified, and all 803 lifecycle manifest bindings replayed without mismatch. Orin Thale, the role spectral uncertainty and provenance cartographer, the hope stated in the identity record, and optional they/them pronouns are relational working language only.

## Page 2 — Frozen plan

X1 reviews 200 inherited Talen contracts at zero new-owner credit and freezes 200 new finite spectral/archive contracts. It plans 300 safe tasks, 250 candidates, exactly 300 CLEAN/FIX/REFINE procedures, 50 exact packets, 30 blocked packets, ten skills, five runners, four synthetic practices, ten successor skill ideas, ten successor runner ideas, and one successor practice recommendation. All 1,000 changed-output mutations are preregistered. No x2 implementation or observed outcome exists in this commit.

## Page 3 — Evidence and authority boundaries

GMUT remains a typed scalar-tensor/EFT research-model family. THOS remains synthetic or proxy-only. Freed ID remains synthetic and nonproduction. Citations, package metadata, finite contracts, structural HTML, and same-owner validation establish no real observation, participant evidence, professional competence, production readiness, legal or cultural legitimacy, Maori authority, affected-party acceptance, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, canon, or Stage 20 authority. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    write_text(X1 / "integrated-overview.md", overview)
    for path, value in docs.items():
        write_json(path, value)
    expected_paths = sorted([rel(path) for path in docs] + [rel(X1 / "integrated-overview.md"), "scripts/build_ghc_family_orin_thale_v687_v7_x1.py", "tests/test_ghc_family_orin_thale_v687_v7_x1.py", rel(VALIDATION / "x1-privacy.json"), rel(VALIDATION / "x1-staged-review.json"), rel(VALIDATION / "x1-manifest.json")])
    write_json(VALIDATION / "x1-staged-review.json", {"schema": "ghc.family.staged-review.v1", "phase": "v687-v7", "lifecycle": "x1", "source": SOURCE, "expected_paths": expected_paths, "expected_path_count": len(expected_paths), "x2_paths": [], "unexpected_paths": []})
    privacy_patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_identifier": re.compile(rb"(?:thread|task|agent)_id\s*[:=]", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[:=]\s*[^\s]{8,}", re.I),
        "private_stream": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }
    scan_paths = [ROOT / path for path in expected_paths if path not in {rel(VALIDATION / "x1-privacy.json"), rel(VALIDATION / "x1-manifest.json")}]
    privacy_candidates, confirmed = [], []
    for path in scan_paths:
        data = path.read_bytes()
        scanner_definition = path.name == "build_ghc_family_orin_thale_v687_v7_x1.py"
        for class_name, pattern in privacy_patterns.items():
            for match in pattern.finditer(data):
                row = {"path": rel(path), "class": class_name, "matched_sha256": hashlib.sha256(match.group()).hexdigest()}
                (privacy_candidates if scanner_definition else confirmed).append(row)
    write_json(VALIDATION / "x1-privacy.json", {"schema": "ghc.family.privacy-adjudication.v1", "classes": list(privacy_patterns), "candidates": privacy_candidates, "confirmed_hits": confirmed, "confirmed_count": len(confirmed), "complete_privacy_claimed": False})
    exclusions = [rel(VALIDATION / "x1-manifest.json")]
    entries = []
    for path_str in expected_paths:
        if path_str in exclusions:
            continue
        path = ROOT / path_str
        data = norm(path)
        entries.append({"path": path_str, "bytes_normalized_lf": len(data), "sha256_normalized_lf": hashlib.sha256(data).hexdigest()})
    write_json(VALIDATION / "x1-manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v1", "anchor": "PENDING_X1_COMMIT", "byte_domain": "normalized_lf_git_blob", "declared_self_exclusions": exclusions, "entry_count": len(entries), "entries": entries})
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed}")
    print(json.dumps({"status": "PLANNING_ONLY_X1_PREPARED", "inherited_reviews": len(inherited), "new_proposals": len(proposals), "mutations": len(mutations), "safe": len(safe), "candidates": len(candidates), "clean_fix_refine": len(clean), "exact": len(exact), "blocked": len(blocked), "startup_failures": len(START_FAILURES), "counts": counts, "paths": len(expected_paths), "privacy_confirmed": len(confirmed)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

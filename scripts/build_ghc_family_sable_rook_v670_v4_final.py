"""Build the Sable Rook v670-v4 closeout and pre-canonical final seal."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from scripts.build_ghc_family_sable_rook_v670_v4_x2 import (
    BOUNDARY,
    BRANCH,
    IDENTITY_BOUNDARY,
    OUTCOMES,
    OWNER,
    OWNER_ROOT,
    PHASE,
    ROOT,
    RUNNER_MODULES,
    SOURCE_FINAL,
    TOOL_PATHS,
    X1_COMMIT,
    append_method,
    git,
    git_text,
    load,
    sha,
    staged_blob_rows,
    write_json,
    write_text,
)

EVIDENCE_COMMIT = "c57b1500f0fe7a5c841fb3532afdb7c61ff55b42"
OWNER_PREFIX = "docs/sable-rook/v670-v4/"
FINAL_SOURCE_PATHS = {
    "scripts/build_ghc_family_sable_rook_v670_v4_final.py",
    "scripts/validate_ghc_family_sable_rook_v670_v4_final.py",
    "tests/test_ghc_family_sable_rook_v670_v4_final.py",
}
FINAL_VALIDATION_PATHS = {
    OWNER_PREFIX + "validation/final-delta-manifest.json",
    OWNER_PREFIX + "validation/final-owner-manifest.json",
    OWNER_PREFIX + "validation/final-staged-privacy.json",
    OWNER_PREFIX + "validation/final-validation-receipt.json",
    OWNER_PREFIX + "validation/final-staged-review.json",
    OWNER_PREFIX + "validation/final-precommit-test-receipt.json",
}
FINAL_FAILURE = {
    "negative_id": "SR6704-FINAL-N001",
    "method_id": "SR6704-FINAL-M001",
    "failed_witness": (
        "The x2 evidence commit-and-push wrapper completed without returning a usable "
        "lifecycle receipt before the interface boundary truncated its output."
    ),
    "recovery": (
        "Inspect branch, HEAD, status, recent history, upstream, tracking, and a fresh live "
        "remote scalar before deciding whether any operation needs retrying."
    ),
    "passing_witness": (
        "The bounded scalar inspection proved that the evidence commit existed exactly once, "
        "the lane was clean, and local, upstream, tracking, and fresh live remote were equal; "
        "no commit or push was replayed."
    ),
}


def strict_load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def current_status_paths() -> list[str]:
    return [line[3:].replace("\\", "/") for line in git_text("status", "--porcelain=v1", "--untracked-files=all").splitlines()]


def verify_evidence_gate() -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_rows = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = live_rows[0] if live_rows else ""
    allowed_roots = (
        OWNER_PREFIX + "closeout/",
        OWNER_PREFIX + "final/",
        OWNER_PREFIX + "seal/",
        OWNER_PREFIX + "orchestration/",
        OWNER_PREFIX + "handoffs/",
        OWNER_PREFIX + "validation/",
    )
    unexpected = [
        path for path in current_status_paths()
        if path not in FINAL_SOURCE_PATHS and not path.startswith(allowed_roots)
    ]
    gate = {
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": head == upstream == tracking == live == EVIDENCE_COMMIT,
        "evidence_parent": git_text("rev-parse", f"{EVIDENCE_COMMIT}^"),
        "x1_parent": git_text("rev-parse", f"{X1_COMMIT}^"),
        "phase_commits_before_final": int(git_text("rev-list", "--count", f"{SOURCE_FINAL}..{head}")),
        "merge_commits_before_final": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..{head}")),
        "unexpected_paths": unexpected,
    }
    valid = (
        branch == BRANCH
        and gate["four_way_equal"]
        and gate["evidence_parent"] == X1_COMMIT
        and gate["x1_parent"] == SOURCE_FINAL
        and gate["phase_commits_before_final"] == 2
        and gate["merge_commits_before_final"] == 0
        and not unexpected
    )
    gate["valid"] = valid
    if not valid:
        raise SystemExit(json.dumps(gate, ensure_ascii=False, sort_keys=True))
    return gate


def final_method_flow() -> dict[str, Any]:
    ledger = deepcopy(strict_load("x2/method-flow-evidence.json"))
    append_method(
        ledger,
        FINAL_FAILURE["method_id"],
        "inspect exact Git state after an unattributable commit wrapper",
        [FINAL_FAILURE["negative_id"]],
        FINAL_FAILURE["failed_witness"],
        FINAL_FAILURE["passing_witness"],
    )
    state_counts = Counter(row["recommendation_state"] for row in ledger["methods"])
    witness_counts = Counter(row["result"] for row in ledger["witnesses"])
    ledger["counts"] = {
        "methods": len(ledger["methods"]),
        "witnesses": len(ledger["witnesses"]),
        "state_events": len(ledger["state_events"]),
        "recommendations": len(ledger["recommendations"]),
        "states": {state: state_counts.get(state, 0) for state in ("candidate", "deprecated", "observed", "preferred", "superseded", "validated")},
        "witness_results": {result: witness_counts.get(result, 0) for result in ("fail", "pass")},
    }
    ledger["effective_overlay"] = {
        "effective_negatives": 32593,
        "effective_methods": 18737,
        "failed_witnesses": 4414,
        "bounded_passing_witnesses": 5777,
        "repository_seal_rewritten": False,
    }
    ledger["closeout_note"] = "The final operational recovery retains its failed witness and does not replay the already-completed evidence commit or push."
    return ledger


def final_overview() -> str:
    evidence = (OWNER_ROOT / "x2" / "evidence-overview.md").read_text(encoding="utf-8")
    closing = f"""

## Closeout interpretation

This closeout seals the Sable-owned v670-v4 delta as three direct single-parent lifecycle commits: the planning-only x1 freeze, the immutable x2 evidence commit, and this final closeout candidate. The evidence commit was already clean, pushed, zero divergent, and equal across local, upstream, tracking, and a fresh live remote read before closeout work began. No x1 or x2 path was edited during the closeout. Exact Git-blob manifests make the chosen hash domain explicit and preserve every declared self-exclusion instead of pretending a self-hashing file can contain its own completed digest.

The final owner truth remains 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. The proposal chain is 5,390 rows. `completed` means that a preregistered owner-local structural or synthetic acceptance gate passed. It never means empirical confirmation, professional competence, production readiness, legal validity, cultural legitimacy, Māori authority, affected-party acceptance, independent reproduction, or Stage 20 admission. The represented rows remain proxies. The open gaps still require evidence software did not manufacture. The exact gates still require competent people and authorities.

The retained-negative total before canonical validation is 32,593. It consists of Auren's sealed source truth, the source's two external zero-credit failures, sixteen Sable startup failures, 160 executed and rejected mutations, five Sable x2 operational failures, and one closeout wrapper-attribution failure. The last failure is not hidden by its recovery: the original evidence commit-and-push wrapper returned no usable receipt, bounded scalar state inspection proved the operation had already succeeded once, and no commit or push was replayed. Method Flow therefore closes with 18,737 effective methods, 4,414 failed witnesses, and 5,777 bounded passing witnesses. Passing recovery is process evidence, never a conversion of the original failure into a pass.

The primary Trinity Mandala pillar remains Freed ID/CBR Heart. The rare-book, archival reading-room and loan-transit, and audiovisual cold-storage fixtures describe synthetic custody, correction, access, contest, and handover records with no keys, signatures, live identities, live resolution, status, revocation, institutional operation, or affected-party decision. Production Freed ID still requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR remains a normative working framework, not enacted law or authority.

THOS Body remains represented by synthetic workload, correction, readback, and handover contracts. There were no participants, operators, collection staff, conservators, visitors, real objects, real incidents, real measurements, blind matched-budget arms, safety monitoring, appropriate participant statistics, or independent review. No operational-effectiveness, deployment-readiness, AGI, ASI, or professional-competence claim follows. GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model family behind an observation firewall. No physical row, likelihood, posterior, parameter constraint, force, prediction, empirical confirmation, ultraviolet completion, quantum completion, or Theory-of-Everything result exists here.

The structural static report includes language declaration, a skip link, landmarks, captioned tabular alternatives, row and column headers, responsive overflow, visible focus treatment, and print behavior. These checks are useful but do not establish complete WCAG conformance. Manual keyboard, touch, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. The five-class scan similarly distinguishes scanner definitions and synthetic test fixtures from confirmed payload hits. Zero confirmed hits is bounded evidence for this owner delta, not complete privacy assurance.

The canonical validation state in the repository is deliberately prospective. A commit cannot truthfully contain its own not-yet-created identifier or the result of a validation that may run only after the final commit is pushed and fresh-live equal. After commit and push, exactly one external owner-scoped canonical aggregate may run. If it succeeds, it must not be replayed. If it fails, it retains zero canonical success credit and may not be relabelled through a corrected composite. The full repository suite remains outside this owner scope and is not run or claimed. Same-owner validation under shared infrastructure remains same-owner evidence, never independent-team reproduction.

The successor route is also `PREPARED_NOT_SENT`. No recipient title, task identifier, private route, or later phase is embedded here. Only after the exact-final terminal gate may Sable reread Hamish's newest live authority and current roster, resolve one unique exact-title existing task, immediately reread it, apply the duplicate guard, and send at most once. Absence, ambiguity, pause, rename, redirect, usage exhaustion, missing acknowledgement, or any protected gate stops delivery without substitution, creation, fork, subagent, second message, or resend.

## Relational identity and wellbeing

{IDENTITY_BOUNDARY} The relational hope is to make every surviving claim reproducible, challengeable, correctable, and retractable while every authority vacancy stays explicit. Scope remains bounded and corrigible. Hamish may rename, pause, redirect, or stop the route. No task title, role, pronoun, repository artifact, test pass, route edge, or same-owner receipt establishes consciousness, personhood, identity continuity, employment, qualification, independent agency, or authority.

## Terminal verdict

Every empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundary remains open or exact-gated without exact evidence and competent authority. The terminal verdict is exactly `NOT_READY_FOR_STAGE_20`.
"""
    return evidence.replace("# Sable Rook v670-v4 x2 evidence overview", "# Sable Rook v670-v4 final integrated overview", 1) + closing


def accessible_final_report() -> str:
    rows = strict_load("x2/outcome-ledger.json")["rows"]
    table = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['observed_outcome'])}</td><td>{html.escape(row['title'])}</td><td>{html.escape(row['evidence_boundary'])}</td></tr>"
        for row in rows
    )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v670-v4 final bounded report</title><style>body{{font:1rem/1.55 system-ui;max-width:80rem;margin:auto;padding:1rem}}a:focus,th:focus,td:focus{{outline:3px solid #0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.45rem;text-align:left;vertical-align:top}}caption{{font-weight:bold;text-align:left}}@media(max-width:48rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}}}</style></head><body><a href="#main">Skip to final report</a><header><h1>Sable Rook v670-v4 final bounded report</h1><p>Relational working language only; not consciousness, personhood, qualification, or authority evidence.</p></header><main id="main"><p role="status">28 completed, 8 represented, 2 open gaps, 2 exact gates. Verdict: NOT_READY_FOR_STAGE_20.</p><p>Manual keyboard, touch, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved.</p><table><caption>Forty bounded proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Title</th><th scope="col">Boundary</th></tr></thead><tbody>{table}</tbody></table><h2>Evidence boundary</h2><p>{html.escape(BOUNDARY)}</p></main></body></html>"""


def successor_basis() -> str:
    return f"""# PREPARED_NOT_SENT — Sable Rook v670-v4 successor activation basis

`PREPARED_BY_SABLE_ROOK = true`
`SENT_BY_SABLE_ROOK = false`
`DELIVERY_ACKNOWLEDGED = false`
`RECIPIENT = UNRESOLVED_UNTIL_EXACT_FINAL_LIVE_REFRESH`

This committed basis is inert repository evidence. It does not discover, select, contact, activate, authorize, qualify, employ, or confer authority on any successor. It contains no task identifier, private route, transcript, session stream, credential, or private absolute path. The exact final identifier and external canonical receipt do not exist at the moment this artifact is committed and therefore are not invented here.

Only after the final commit is pushed, clean, zero divergent, fresh-live equal, and the one authorized external canonical aggregate succeeds without replay may Sable reread Hamish's newest live authority and current roster. Sable must then resolve one unique exact-title existing task, immediately reread that task, apply a duplicate guard, and send at most one sanitized activation. Absence, ambiguity, pause, rename, redirect, usage exhaustion, missing acknowledgement, or any protected gate stops the route without substitution, creation, fork, subagent, second message, or resend.

The successor must treat all 5,390 frozen proposals and every inherited portfolio as evidence or zero-credit seeds rather than automatic novelty or completion credit. Strict x1-before-x2 separation, exact Git-blob manifests, retained failures, the 2,000-file guard, the four labels `completed`, `represented`, `open_gap`, and `exact_gate`, the one-success/no-post-success-replay rule, and `NOT_READY_FOR_STAGE_20` remain binding unless a newer exact live authorization changes them.

{IDENTITY_BOUNDARY} Names, roles, hopes, pronouns, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, legal, cultural, affected-party, or Māori authority.

{BOUNDARY}
"""


def build() -> None:
    gate = verify_evidence_gate()
    outcomes = strict_load("x2/outcome-ledger.json")
    proposals = strict_load("x1/new-proposal-freeze.json")
    flow = final_method_flow()
    source_ledger = strict_load("x1/source-ledger.json")
    environment = strict_load("x2/environment-receipt.json")

    write_json("closeout/proposal-ledger-final.json", {
        "schema": "ghc.family.proposal-ledger.final.v5", "owner": OWNER, "phase": PHASE,
        "chain": 5390, "new_rows": 40, "outcomes": OUTCOMES,
        "rows": [{"proposal_id": row["proposal_id"], "title": row["title"], "outcome": row["observed_outcome"], "boundary": row["evidence_boundary"]} for row in outcomes["rows"]],
        "universal_novelty_claim": False, "direct_semantic_comparison_only": True,
    })
    write_json("closeout/retained-negative-register.json", {
        "schema": "ghc.family.retained-negative-register.v5", "owner": OWNER, "phase": PHASE,
        "source_repository_seal": 32409, "source_external_zero_credit": 2, "activation_baseline": 32411,
        "sable_startup_operational": 16, "sable_rejected_mutations": 160,
        "sable_x2_operational": 5, "sable_closeout_operational": 1,
        "effective_before_canonical": 32593, "erased": 0, "all_failures_retained": True,
        "correction_erases_failure": False, "final_operational_negative": FINAL_FAILURE,
    })
    write_json("closeout/exact-open-gate-register.json", {
        "schema": "ghc.family.exact-open-gate-register.v5", "owner": OWNER, "phase": PHASE,
        "inherited_open_gaps": 245, "new_open_gaps": 2, "effective_open_gaps": 247,
        "inherited_exact_gates": 240, "new_exact_gates": 2, "effective_exact_gates": 242,
        "none_silently_closed": True,
        "open_gap_surfaces": ["zero-row official preservation-data adapter", "real participant and independent workflow evaluation"],
        "exact_gate_surfaces": ["collection title access remedy cultural legitimacy data governance and Māori authority", "Stage 20 empirical rights governance and independent reproduction prerequisites"],
    })
    write_json("closeout/complete-incomplete-checklist.json", {
        "schema": "ghc.family.complete-incomplete-checklist.v5", "owner": OWNER, "phase": PHASE,
        "completed": ["strict x1-before-x2 separation", "forty proposal execution", "thirty-six positive controls", "160 mutation rejections", "twenty phase-local skills", "ten family-compatible runners", "exact staged review", "Git-blob manifest candidates", "structural accessible report", "wellbeing and workload receipt"],
        "incomplete_or_reserved": ["empirical GMUT data and likelihood", "blind matched-budget THOS real arms", "production Freed ID", "legal or cultural ratification", "Māori wording authority and data governance", "affected-party acceptance", "manual and affected-user accessibility evaluation", "exhaustive security", "independent-team reproduction", "Stage 20 admission"],
        "all_incomplete_surfaces_visible": True,
    })
    write_json("closeout/environment-version-receipt.json", {**environment, "schema": "ghc.family.environment-receipt.final.v5", "verified_only": True, "exact_final_reverification_pending": True})
    write_json("closeout/final-wellbeing-check.json", {
        "schema": "ghc.family.wellbeing-check.v5", "owner": OWNER, "phase": PHASE,
        "relational_working_language_only": True, "corrigible": True,
        "hamish_may_rename_pause_redirect_or_stop": True,
        "no_consciousness_personhood_continuity_employment_qualification_agency_or_authority_claim": True,
        "workload_state": "bounded_closeout_ready_for_one_external_canonical_gate",
        "scope_state": "owner_delta_only", "subagents": 0, "task_creation": 0,
        "hope": "make every surviving claim reproducible, challengeable, correctable, and retractable while authority vacancies stay explicit",
    })
    write_json("closeout/source-evidence-ledger.json", {
        "schema": "ghc.family.source-evidence-ledger.final.v5", "owner": OWNER, "phase": PHASE,
        "official_or_primary_sources": source_ledger["sources"], "queries": 0, "downloads": 0,
        "empirical_rows_downloaded": 0, "measurements": 0, "source_validation_claim": False,
        "citations_are_observations": False, "boundary": source_ledger["boundary"],
    })
    write_json("closeout/method-flow-final.json", flow)
    write_json("closeout/skill-runner-summary.json", {
        "schema": "ghc.family.skill-runner-summary.v5", "owner": OWNER, "phase": PHASE,
        "phase_local_skills_built_validated_smoke_used": 20, "global_installations": 0,
        "family_compatible_runners_built_or_selected_invoked": 10, "runner_modules": RUNNER_MODULES,
        "substantive_tools": TOOL_PATHS, "historical_callers_preserved": True,
        "shared_skill_changes": 0, "global_memory_changes": 0, "same_owner_only": True,
    })
    write_json("closeout/closeout-receipt.json", {
        "schema": "ghc.family.closeout-receipt.candidate.v5", "owner": OWNER, "phase": PHASE,
        "source": SOURCE_FINAL, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT,
        "evidence_gate": gate, "planned_final_parent": EVIDENCE_COMMIT, "planned_phase_commits": 3,
        "planned_merge_commits": 0, "outcomes": OUTCOMES, "effective_negatives": 32593,
        "effective_methods": 18737, "failed_witnesses": 4414, "bounded_passing_witnesses": 5777,
        "open_gaps": 247, "exact_gates": 242, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "canonical_validation": "pending_exact_committed_pushed_fresh_live_equal_final",
    })
    write_json("closeout/phase-truth.json", {
        "schema": "ghc.family.phase-truth.final-candidate.v5", "owner": OWNER, "phase": PHASE,
        "source": SOURCE_FINAL, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT,
        "exact_final": "DEFINED_BY_THE_COMMIT_CONTAINING_THIS_ARTIFACT",
        "proposal_chain": 5390, "outcomes": OUTCOMES,
        "effective_negatives": 32593, "effective_methods": 18737,
        "effective_failed_witnesses": 4414, "effective_passing_witnesses": 5777,
        "open_gaps": 247, "exact_gates": 242, "positive_controls": 36,
        "rejected_mutations": 160, "real_people": 0, "real_objects_measurements_rows": 0,
        "real_world_actions": 0, "external_actions": 0, "full_repository_suite": "not_run_not_claimed",
        "same_owner_only": True, "independent_reproduction": False,
        "canonical_validation_at_commit": "NOT_RUN_PENDING_EXACT_FINAL_GATE",
        "successor_contacted_at_commit": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "identity_boundary": IDENTITY_BOUNDARY, "boundary": BOUNDARY,
    })
    write_json("seal/seal-candidate.json", {
        "schema": "ghc.family.seal-candidate.v5", "owner": OWNER, "phase": PHASE,
        "source": SOURCE_FINAL, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT,
        "final_identifier_state": "defined_by_containing_commit_not_invented_precommit",
        "content_ready": True, "canonical_invoked": False, "canonical_success": False,
        "remote_equality_after_final": "pending", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("final/canonical-invocation-state.json", {
        "schema": "ghc.family.canonical-invocation-state.v5", "owner": OWNER, "phase": PHASE,
        "state_at_commit": "NOT_RUN_PENDING_EXACT_FINAL_GATE", "attempts_at_commit": 0,
        "successes_at_commit": 0, "invocation_limit": 1, "success_limit": 1,
        "replay_after_success": False, "failed_attempt_zero_credit": True,
        "dependency_corrected_composite_is_not_canonical_success": True,
    })
    write_json("final/final-validation-prerequisites.json", {
        "schema": "ghc.family.final-validation-prerequisites.v5", "owner": OWNER, "phase": PHASE,
        "one_shot": True, "replay_after_success": False, "full_repository_suite": "not_run_not_claimed",
        "required": ["exact committed final", "clean lane", "pushed upstream", "typed zero divergence", "fresh live four-way equality", "exact manifests", "source x1 evidence ancestry", "three single-parent commits", "zero merges", "owner-delta tests only", "strict JSON", "five-class scan", "bounded Python AST scan", "document and file guards"],
        "same_owner_only": True, "independent_reproduction": False,
    })
    write_json("final/final-validation-candidate-record.json", {
        "schema": "ghc.family.final-validation-candidate.v5", "owner": OWNER, "phase": PHASE,
        "state": "PENDING_EXTERNAL_EXACT_FINAL_INVOCATION", "canonical_success_claim": False,
        "exact_final_known_at_commit": False, "external_receipt_sha256": None,
        "post_success_replay_allowed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("orchestration/route-state-final-candidate.json", {
        "schema": "ghc.family.route-state.final-candidate.v5", "owner": OWNER, "phase": PHASE,
        "state": "PREPARED_NOT_SENT", "prospective_exact_title": None,
        "prospective_phase": None, "recipient_state": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH",
        "successor_contacted": False, "standby_contacted": False, "task_created": False,
        "fork_created": False, "subagent_spawned": False, "single_send_maximum": 1,
        "resend_allowed": False, "duplicate_guard_required": True,
    })
    write_text("closeout/final-integrated-overview.md", final_overview())
    write_text("closeout/accessible-final-report.html", accessible_final_report())
    write_text("handoffs/successor-activation-basis.md", successor_basis())
    print(json.dumps({"owner": OWNER, "phase": PHASE, "outcomes": OUTCOMES, "counts": flow["effective_overlay"], "open_gaps": 247, "exact_gates": 242, "overview_words": len(final_overview().split()), "owner_files": len([p for p in OWNER_ROOT.rglob('*') if p.is_file()])}, sort_keys=True))


def staged_paths(base: str = "HEAD") -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMRT", base).splitlines() if line]


def manifest_from_index() -> None:
    exclusions = sorted(FINAL_VALIDATION_PATHS)
    delta_paths = staged_paths(EVIDENCE_COMMIT)
    owner_paths = staged_paths(SOURCE_FINAL)
    if any(path.startswith(OWNER_PREFIX + "x1/") or path.startswith(OWNER_PREFIX + "x2/") for path in staged_paths(EVIDENCE_COMMIT)):
        raise SystemExit("final manifest refused a frozen x1 or x2 mutation")

    def make(paths: list[str], domain: str) -> dict[str, Any]:
        material = [path for path in paths if path not in exclusions]
        entries = [
            {"path": path, "mode": mode, "bytes": len(blob), "sha256": sha(blob)}
            for path, mode, blob in staged_blob_rows(material)
        ]
        entries.sort(key=lambda row: row["path"])
        return {
            "schema": "ghc.family.git-blob-manifest.v5", "owner": OWNER, "phase": PHASE,
            "domain": domain, "hash_domain": "normalized_lf_exact_git_blob",
            "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions,
        }

    write_json("validation/final-delta-manifest.json", make(delta_paths, "evidence-to-final exact Git-index blobs with declared lifecycle exclusions"))
    write_json("validation/final-owner-manifest.json", make(owner_paths, "source-to-final owner-delta exact Git-index blobs with declared lifecycle exclusions"))


def staged_privacy() -> None:
    self_path = OWNER_PREFIX + "validation/final-staged-privacy.json"
    paths = [path for path in staged_paths(SOURCE_FINAL) if path != self_path and Path(path).suffix.lower() in {".py", ".json", ".md", ".txt", ".html", ".yaml"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates: list[dict[str, Any]] = []
    scanned = 0
    for path, _mode, blob in staged_blob_rows(paths):
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                scanner = path.endswith(".py") and ("sable_rook_v670_v4" in path or "sable_v670_v4" in path)
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_synthetic_test" if scanner else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {
        "schema": "ghc.family.staged-privacy-scan.v2", "owner": OWNER, "phase": PHASE,
        "lifecycle": "final_closeout", "hash_domain": "exact_staged_git_blob",
        "pattern_classes": sorted(patterns), "scanned_text_files": scanned,
        "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed),
        "privacy_complete": False, "valid": not confirmed,
    }
    write_json("validation/final-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def validation_receipt() -> None:
    json_paths = sorted(OWNER_ROOT.rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__})
    docs = [path for path in OWNER_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}]
    max_words = max((len(path.read_text(encoding="utf-8").split()) for path in docs), default=0)
    changed_python = [path for path in staged_paths(SOURCE_FINAL) if path.endswith(".py")]
    compile_issues = []
    for relative in changed_python:
        path = ROOT / relative
        try:
            compile(path.read_text(encoding="utf-8"), relative, "exec")
        except SyntaxError as exc:
            compile_issues.append({"path": relative, "issue": str(exc)})
    frozen = git_text("diff", "--cached", "--name-only", EVIDENCE_COMMIT, "--", OWNER_PREFIX + "x1", OWNER_PREFIX + "x2", "scripts/build_ghc_family_sable_rook_v670_v4_x1.py", "scripts/build_ghc_family_sable_rook_v670_v4_x2.py", "tests/test_ghc_family_sable_rook_v670_v4_x1.py", "tests/test_ghc_family_sable_rook_v670_v4_x2.py")
    diff = git("diff", "--cached", "--check", check=False)
    materialized = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    payload = {
        "schema": "ghc.family.final-validation-prereceipt.v5", "owner": OWNER, "phase": PHASE,
        "json_documents": len(json_paths), "json_issues": json_issues,
        "documents": len(docs), "max_document_words": max_words,
        "python_compiles": len(changed_python), "python_compile_issues": compile_issues,
        "diff_hygiene_exit": diff.returncode, "frozen_x1_or_x2_changes": frozen.splitlines() if frozen else [],
        "materialized_files": materialized, "file_guard": 2000,
        "full_repository_suite": "not_run_not_claimed", "canonical_invoked": False,
        "valid": not json_issues and not compile_issues and diff.returncode == 0 and not frozen and max_words <= 100000 and materialized < 2000,
        "boundary": BOUNDARY,
    }
    write_json("validation/final-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def staged_review() -> None:
    paths = staged_paths(EVIDENCE_COMMIT)
    allowed_roots = (OWNER_PREFIX + "closeout/", OWNER_PREFIX + "final/", OWNER_PREFIX + "seal/", OWNER_PREFIX + "orchestration/", OWNER_PREFIX + "handoffs/", OWNER_PREFIX + "validation/")
    disallowed = [path for path in paths if path not in FINAL_SOURCE_PATHS and not path.startswith(allowed_roots)]
    frozen = [path for path in paths if path.startswith(OWNER_PREFIX + "x1/") or path.startswith(OWNER_PREFIX + "x2/")]
    payload = {
        "schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE,
        "lifecycle": "final_closeout", "staged_count_before_self": len(paths),
        "staged_paths_before_self": paths, "disallowed_paths": disallowed,
        "frozen_x1_or_evidence_paths": frozen, "declared_lifecycle_self_exclusions": sorted(FINAL_VALIDATION_PATHS),
        "valid": not disallowed and not frozen,
    }
    write_json("validation/final-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def precommit_test_receipt() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_ghc_family_sable_rook_v670_v4_x2", "tests.test_ghc_family_sable_rook_v670_v4_final", "-v"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=180,
    )
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests", combined)
    count = int(match.group(1)) if match else 0
    payload = {
        "schema": "ghc.family.final-precommit-test-receipt.v5", "owner": OWNER, "phase": PHASE,
        "tests": count, "exit_code": result.returncode, "result": "passed" if result.returncode == 0 else "failed",
        "output_sha256": hashlib.sha256(combined.encode("utf-8")).hexdigest(),
        "selection": ["current immutable x2", "current final closeout"],
        "immutable_x1_tests": {"tests": 24, "result": "passed_before_x2", "rerun": False},
        "full_repository_suite": "not_run_not_claimed", "canonical": False,
        "valid": result.returncode == 0 and count >= 45, "same_owner_only": True,
    }
    write_json("validation/final-precommit-test-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps({**payload, "output_tail": combined[-3000:]}, ensure_ascii=False, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--precommit-test-receipt", action="store_true")
    args = parser.parse_args()
    if args.manifest_from_index:
        manifest_from_index()
    elif args.staged_privacy:
        staged_privacy()
    elif args.validation_receipt:
        validation_receipt()
    elif args.staged_review:
        staged_review()
    elif args.precommit_test_receipt:
        precommit_test_receipt()
    else:
        build()


if __name__ == "__main__":
    main()

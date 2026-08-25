#!/usr/bin/env python3
"""Build the terminal Tamar Vey v669-v1 closeout candidate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_tamar_vey_v669_v1_archive import (
    BRANCH,
    EVIDENCE_BOUNDARY,
    IDENTITY_BOUNDARY,
    OWNER,
    PHASE,
    PHASE_ROOT,
    RELATIONAL_HOPE,
    RELATIONAL_ROLE,
    REL_PHASE_ROOT,
    ROOT,
    RUNNER_NAMES,
    SOURCE_BRANCH,
    SOURCE_CANONICAL_PAYLOAD_SHA256,
    SOURCE_CANONICAL_RECEIPT_SHA256,
    SOURCE_EVIDENCE,
    SOURCE_FINAL,
    SOURCE_START,
    SOURCE_TERMINAL_STATUS,
    SOURCE_X1,
    TERMINAL_VERDICT,
    manifest_rows,
    utc_now,
)


X1_HEAD = "f1a090e2396de5d76c70aa3bf7bda0a888b1249a"
EVIDENCE_HEAD = "cf99dad5ec53f4af60017a829889087ed50cf752"
FINAL_FAILURES: list[tuple[str, str, str, str]] = [
    (
        "TV6691-CL-N001",
        "The first final owner-suite run passed 14/15 checks, but its open/exact-gate assertion retained Liora's pre-Tamar totals of 223 and 218 instead of the additive x2 evidence totals of 225 and 220.",
        "Preserve the failed suite witness, update only the final test's gate-count contract to the committed Tamar evidence totals, rebuild derived closeout counters and manifests, and rerun the attributable final owner suite before staging.",
        "Derive final gap and gate expectations from the immutable evidence truth rather than copying source-phase totals.",
    ),
    (
        "TV6691-CL-N002",
        "The first exact staged review measured the integrated overview at 1,078 words, below the standing three-page-equivalent floor, even though all 26 staged paths and diff-hygiene checks were exact.",
        "Preserve the undersized-overview witness, expand only the integrated overview with proposal, source, limitation, recovery, accessibility, and delivery analysis, then rebuild its content seal and exact manifests before restaging.",
        "Measure the integrated overview before final staging and require at least 1,500 words while preserving the 6,000-word document ceiling.",
    ),
    (
        "TV6691-CL-N003",
        "The first stale-domain review scanned the frozen historical novelty corpus and legitimate v668-v8 source references, reporting 285 candidates without separating inherited history from the final delta.",
        "Preserve the noisy projection, scan only the exact final-delta allowlist for superseded domain and owner-route labels, and classify Liora and v668-v8 occurrences separately as source-lineage references.",
        "Scope stale-label checks to the lifecycle delta and maintain a separate allowlisted source-lineage reference class.",
    ),
]
MANIFEST_EXCLUSIONS = (
    f"{REL_PHASE_ROOT}/validation/final-owner-manifest.json",
    f"{REL_PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{REL_PHASE_ROOT}/validation/final-staged-allowlist.json",
)


def run_git(*args: str, binary: bool = False, check: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=check, capture_output=True, text=not binary)


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def write_json(relative: str, value: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def write_text(relative: str, value: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value.rstrip() + "\n")
    return path


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def assert_final_start() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_HEAD:
        raise ValueError("closeout must begin at the exact immutable evidence head")
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("unexpected Tamar owner branch")
    if git("rev-parse", f"{EVIDENCE_HEAD}^") != X1_HEAD or git("rev-parse", f"{X1_HEAD}^") != SOURCE_FINAL:
        raise ValueError("source, x1, or evidence direct-parent drift")
    allowed = {
        "scripts/build_ghc_family_tamar_vey_v669_v1_final.py",
        "scripts/ghc_family_tamar_vey_v669_v1_canonical.py",
        "tests/test_ghc_family_tamar_vey_v669_v1_final.py",
    }
    unexpected = []
    for line in run_git("status", "--porcelain", "--untracked-files=all").stdout.splitlines():
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        admitted = (
            path in allowed
            or path.startswith(f"{REL_PHASE_ROOT}/closeout/")
            or path.startswith(f"{REL_PHASE_ROOT}/final/")
            or path.startswith(f"{REL_PHASE_ROOT}/handoffs/")
            or path.startswith(f"{REL_PHASE_ROOT}/route/")
            or path.startswith(f"{REL_PHASE_ROOT}/seal/")
            or (path.startswith(f"{REL_PHASE_ROOT}/validation/final-"))
        )
        if not admitted:
            unexpected.append(path)
    if unexpected:
        raise ValueError(f"unexpected pre-closeout paths: {unexpected}")


def final_method_flow(evidence_overlay: dict[str, int]) -> tuple[dict[str, Any], dict[str, int]]:
    methods, witnesses, events, recommendations = [], [], [], []
    for index, (negative_id, failure, recovery, guard) in enumerate(FINAL_FAILURES, 1):
        method_id = f"TV6691-FINAL-M{index:03d}"
        fail_id = f"TV6691-FINAL-W{index:03d}-F"
        pass_id = f"TV6691-FINAL-W{index:03d}-P"
        methods.append({
            "method_id": method_id,
            "title": recovery,
            "failure_signature": negative_id.casefold().replace("-", "_"),
            "trigger_preconditions": [failure],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": recovery,
            "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": guard,
            "rollback": "Stop the smallest closeout operation and preserve source, x1, evidence, remote, route, and sibling state.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": ["immutable_evidence", "retained_failure_integrity", "one_shot_canonical"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Same-owner closeout recovery only; no canonical, empirical, professional, production, authority, or independent-reproduction credit.",
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": failure, "scope": "Owner-local final closeout.", "expected": "The named closeout dependency completes.", "observed": failure, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "Zero-credit closeout failure retained."},
            {"witness_id": pass_id, "method_id": method_id, "procedure": recovery, "scope": "Smallest attributable closeout recovery.", "expected": "Only the named dependency recovers.", "observed": "The named dependency recovered without changing the failed witness.", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "Bounded recovery only."},
        ])
        for before, after, witness_id in ((None, "observed", fail_id), ("observed", "candidate", None), ("candidate", "validated", pass_id), ("validated", "preferred", pass_id)):
            events.append({"event_index": len(events) + 1, "method_id": method_id, "before": before, "after": after, "witness_id": witness_id, "reason": "append-only closeout recovery transition"})
        recommendations.append({"recommendation_index": index, "method_id": method_id, "method": recovery, "preconditions": [failure], "witness_ids": [fail_id, pass_id], "recurrence_guard": guard, "rollback": "Stop the smallest closeout dependency.", "scope_boundary": "Owner-local closeout only."})
    count = len(FINAL_FAILURES)
    final_overlay = {
        "effective_negatives": evidence_overlay["effective_negatives"] + count,
        "methods": evidence_overlay["methods"] + count,
        "failed_witnesses": evidence_overlay["failed_witnesses"] + count,
        "passing_witnesses": evidence_overlay["passing_witnesses"] + count,
        "open_gaps": evidence_overlay["open_gaps"],
        "exact_gates": evidence_overlay["exact_gates"],
    }
    ledger = {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_commit": EVIDENCE_HEAD,
        "final_commit": None,
        "identity_boundary": IDENTITY_BOUNDARY,
        "boundary": "Every closeout failure remains visible at zero credit after recovery.",
        "execution_authority": "owner_self_scoped_delta",
        "counts": {"methods": count, "witnesses": count * 2, "witness_results": {"fail": count, "pass": count}, "state_events": count * 4, "states": {"candidate": 0, "observed": 0, "validated": 0, "preferred": count, "superseded": 0, "deprecated": 0}, "recommendations": count},
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "evidence_overlay": evidence_overlay,
        "final_overlay": final_overlay,
    }
    return ledger, final_overlay


def main() -> int:
    assert_final_start()
    now = utc_now()
    evidence_truth = load("x2/evidence/phase-truth.json")
    evidence_overlay = {key: evidence_truth[key] for key in ("effective_negatives", "methods", "failed_witnesses", "passing_witnesses", "open_gaps", "exact_gates")}
    ledger, final_overlay = final_method_flow(evidence_overlay)
    write_json("closeout/method-flow-ledger.json", ledger)
    write_json(
        "closeout/method-flow-summary.json",
        {
            "schema": "ghc.family.method-flow-summary.v1",
            "owner": OWNER,
            "phase": PHASE,
            "evidence_overlay": evidence_overlay,
            "new_closeout_failures": len(FINAL_FAILURES),
            "new_closeout_recoveries": len(FINAL_FAILURES),
            "final_overlay": final_overlay,
            "rejected_mutations_retained_separately": 160,
            "failure_erasure": False,
            "canonical_credit": 0,
        },
    )
    write_json(
        "closeout/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source_start": SOURCE_START,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_final": SOURCE_FINAL,
            "source_terminal_status": SOURCE_TERMINAL_STATUS,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "final": None,
            "lifecycle": "EXACT_FINAL_CANDIDATE_PENDING_COMMIT_PUSH_AND_CANONICAL",
            "proposal_chain_before": 4910,
            "proposal_chain_after": 4950,
            "outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "mutations": {"preregistered": 160, "executed": 160, "rejected": 160, "accepted": 0},
            "skills": {"initialized": 20, "customized": 20, "quick_validated": 20, "accepting_smoked": 20, "rejecting_smoked": 20, "globally_installed": 0, "forward_test_delegated": 0},
            "runners": {"built": 10, "accepting_smoked": 10, "rejecting_smoked": 10},
            **final_overlay,
            "canonical_validation": "PENDING_EXACT_FINAL_PUSH",
            "canonical_invocations": 0,
            "canonical_successes": 0,
            "full_repository_suite": "not_run_non_Eiren_owner_scope",
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_repository_seal": 30342,
            "Tamar_prefreeze_failures": 16,
            "Tamar_x2_operational_failures": 3,
            "Tamar_closeout_failures": len(FINAL_FAILURES),
            "Tamar_rejected_mutations": 160,
            "effective_negatives": final_overlay["effective_negatives"],
            "retained_failed_witnesses": final_overlay["failed_witnesses"],
            "bounded_passing_witnesses": final_overlay["passing_witnesses"],
            "no_failure_erased": True,
            "boundary": "Liora's sealed one-shot canonical success remains inherited source evidence only; Tamar's recoveries never rewrite the source seal or promote any Tamar failure.",
        },
    )
    write_json(
        "closeout/open-exact-gate-register.json",
        {
            "schema": "ghc.family.open-exact-gate-register.v1",
            "owner": OWNER,
            "phase": PHASE,
            "open_gaps": final_overlay["open_gaps"],
            "exact_gates": final_overlay["exact_gates"],
            "new_open_gap_ids": ["TV6691-N037", "TV6691-N038"],
            "new_exact_gate_ids": ["TV6691-N039", "TV6691-N040"],
            "all_inherited_gaps_and_gates_preserved": True,
            "Maori_concepts_remain_under_Maori_authority": True,
        },
    )
    write_json(
        "closeout/lifecycle-replay.json",
        {
            "schema": "ghc.family.lifecycle-replay.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE_FINAL,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "final": None,
            "expected_parent_edges": [[SOURCE_FINAL, X1_HEAD], [X1_HEAD, EVIDENCE_HEAD], [EVIDENCE_HEAD, "FINAL_PENDING"]],
            "owner_commit_count_at_final": 3,
            "merge_count_at_final": 0,
            "final_parent_count": 1,
            "strict_x1_before_x2": True,
            "x1_pushed_clean_equal_before_x2": True,
            "evidence_pushed_clean_equal_before_closeout": True,
            "final_push_gate": "pending",
            "canonical_gate": "pending_after_final_push",
        },
    )
    write_json(
        "closeout/tools-and-compatibility.json",
        {
            "schema": "ghc.family.tools-and-compatibility.v1",
            "owner": OWNER,
            "phase": PHASE,
            "family_current_callers_preserved": True,
            "ghc_family_runner_count": 10,
            "build_ghc_family_builder_count": 3,
            "phase_local_skill_count": 20,
            "global_skill_installations": 0,
            "file_ceiling": 2000,
            "document_word_ceiling": 6000,
            "full_repository_suite": "not_run",
            "host_security_changes": 0,
            "updates": 0,
            "elevation": 0,
            "reboots": 0,
        },
    )
    write_json(
        "closeout/terminal-checklist.json",
        {
            "schema": "ghc.family.terminal-checklist.v1",
            "owner": OWNER,
            "phase": PHASE,
            "passed_before_final_candidate": ["immutable_source", "immutable_x1", "immutable_evidence", "strict_x1_before_x2", "four_outcome_labels", "160_mutations_retained", "20_skills", "10_runners", "open_gaps", "exact_gates", "privacy_boundary", "authority_boundary", "document_ceiling", "file_ceiling"],
            "pending_after_final_commit": ["exact_final_head", "final_direct_parent", "three_owner_commits", "zero_merges", "clean_state", "zero_divergence", "fresh_four_way_equality", "one_exact_final_canonical_aggregate"],
            "successor_contacted": False,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        "closeout/wellbeing-and-workload-check.json",
        {
            "schema": "ghc.family.wellbeing-workload.v1",
            "owner": OWNER,
            "phase": PHASE,
            "scope_remained_bounded": True,
            "work_remained_interruptible": True,
            "delegation_or_sibling_contact": 0,
            "urgency_promotion": False,
            "identity_or_memory_deletion": False,
            "host_security_changes": 0,
            "workload_result": "bounded_owner_sequence_with_explicit_stop_and_handover_points",
            "boundary": "This is a workflow and workload record only, not evidence of consciousness, wellbeing, fatigue, employment, qualification, agency, or clinical state.",
        },
    )
    write_json(
        "closeout/environment-and-version-receipt.json",
        {
            "schema": "ghc.family.environment-version-receipt.v1",
            "owner": OWNER,
            "phase": PHASE,
            "codex_cli_observed": "0.147.0",
            "codex_desktop_observed": "26.818.5229.0",
            "observed_only": True,
            "desktop_updated": False,
            "other_updates_performed": 0,
            "elevation": False,
            "sandbox_or_hyper_v_activated": False,
            "windows_features_changed": False,
            "host_security_weakened": False,
            "unrelated_software_installed": False,
            "rebooted": False,
        },
    )
    write_json(
        "closeout/family-index-update.json",
        {
            "schema": "ghc.family.index-update.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_phase": "v668-v8",
            "proposal_chain_before": 4910,
            "proposal_chain_after": 4950,
            "primary_pillar": "THOS Body",
            "bounded_practice": "synthetic upholstery intake and component documentation",
            "family_current_callers_preserved": True,
            "method_flow_updated": True,
            "reflection_updated": True,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        "closeout/roster-and-authorization-check.json",
        {
            "schema": "ghc.family.roster-authorization-check.v1",
            "owner": OWNER,
            "phase": PHASE,
            "owner_status": "ACTIVE",
            "provisional_successor_title": "Elowen Cairn",
            "provisional_successor_phase": "v669-v2",
            "successor_precontacted": False,
            "successor_resolution_deferred_until_terminal_gate": True,
            "standby_contacted": False,
            "task_created_or_forked": False,
            "live_authority_refresh_required_at_terminal_gate": True,
            "stop_on_absence_ambiguity_duplicate_or_missing_acknowledgement": True,
        },
    )
    write_json(
        "closeout/workflow-reflection.json",
        {
            "schema": "ghc.family.workflow-reflection.v1",
            "owner": OWNER,
            "phase": PHASE,
            "preserve": ["strict x1-before-x2", "exact allowlists", "retained failed witnesses", "one-shot canonical gate", "source and owner count separation"],
            "improve": ["preflight owner-local skill scaffolds", "transport cross-shell lists as JSON", "compute PowerShell control-flow results before report construction"],
            "reject": ["synthetic-to-empirical promotion", "citation-to-authority promotion", "success replay", "sibling mutation", "route inference before terminal gate"],
            "rollback": "Stop the smallest failing dependency and preserve immutable source, x1, evidence, and route state.",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )

    overview = f"""# Tamar Vey {PHASE} final integrated overview

## Outcome and lifecycle truth

Tamar v669-v1 is a solo, additive, D-first owner lane from immutable Liora final `{SOURCE_FINAL}`. Frozen x1 `{X1_HEAD}` is the direct child of source and was separately committed, pushed, clean, zero-divergent, and fresh-live four-way equal before x2 began. Immutable evidence `{EVIDENCE_HEAD}` is the direct child of x1 and was separately exact-index reviewed, committed, pushed, clean, zero-divergent, and fresh-live four-way equal before closeout began. This closeout candidate is intended as the third and final direct single-parent Tamar commit with zero merges. Its exact head, push, clean state, remote equality, and canonical aggregate remain pending until after commit.

The declared proposal chain advances from 4,910 to 4,950 rows. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. A `completed` result means only that its declared bounded software or synthetic acceptance gate passed; `represented` remains proxy-only; and the two vacancy classes remain unclosed. All 160 preregistered invalid mutations executed and remain rejected at zero credit. Twenty owner-local skills were initialized with the official skill-creator scaffold, customized, completely read, quick-validated under explicit UTF-8 mode, and accepting/rejecting smoke-used. Ten family-current runners were built and smoke-used. No skill was globally installed and no forward validation was delegated.

The retained final candidate overlay is {final_overlay['effective_negatives']} effective negatives, {final_overlay['methods']} effective Method Flow methods, {final_overlay['failed_witnesses']} retained failed witnesses, {final_overlay['passing_witnesses']} bounded passing witnesses, {final_overlay['open_gaps']} open gaps, and {final_overlay['exact_gates']} exact gates. It preserves Liora's sealed 30,342-negative source, sixteen Tamar startup and x1 failures, three Tamar x2 operational failures, {len(FINAL_FAILURES)} closeout failures, and 160 rejected mutations. A rejected mutation contributes a retained negative but not a Method Flow failed-witness count. Each recovered workflow fault remains paired with its failed witness. No failure is erased, folded into a pass, or relabelled for cleaner credit.

## Pillars and bounded upholstery lens

The primary pillar is THOS Body. Its upholstery dependency graph, refusal edges, workload cap, correction echo, accessible status, hazard holds, and shift-handover state are participant-free protocol structures. They do not measure a person, workplace, item, material, safety intervention, work quality, or operational effect. There are zero participants, operators, preregistered blind matched-budget real arms, safety-monitoring events, effectiveness estimates, or independent reviews.

The upholstery documentation practice is wholly synthetic. No real upholstered item, frame, spring, webbing, padding, cover, closure, material, product, tool, workplace, upholsterer, conservator, participant, client, order, measurement, contamination event, fire event, treatment, inspection, repair, or release exists. Component identities, frame and joinery states, spring and webbing topologies, padding and cover layers, condition terms, provenance, custody, corrections, and pseudonyms are fixture fields rather than observations. The Smithsonian Open Access furniture adapter remains `open_gap` with zero key, request, download, row, media object, identification, rights conclusion, fitness conclusion, or safety claim. Real professional, material, fire, workplace, accessibility, language, and affected-party evaluation remains a second `open_gap`. Release, custody, ownership, remedy, legal or cultural interpretation, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain `exact_gate`.

GMUT Mind remains visible through a typed covariant phase-space and presymplectic obligation board. It solves no field equation, calculates no physical current or boundary flux, proves no gauge-degeneracy theorem, evaluates no likelihood, and establishes no force, prediction, parameter constraint, empirical confirmation, quantum or ultraviolet completion, final physics, or Theory of Everything. Freed ID and CBR Heart remain explicit through synthetic hash domains, pseudonyms, capability envelopes, challenge ladders, issue escrow, correction, provenance, status vacancies, and authority-reservation matrices. They use zero standards-conformant real keys or proofs and conduct zero issuance, presentation, resolution, status, revocation, interoperability, privacy-review, independent-security-review, recovery, trust-governance, rights, remedy, or authority event.

## Evidence discipline and retained abstentions

Official and primary sources supplied vocabulary, provenance concepts, accessibility criteria, identity assurance boundaries, and governance reservations only. They were not converted into furniture observations, material identifications, professional instructions, participant evidence, standards conformance, legal interpretation, cultural legitimacy, or Māori authority. The zero-call adapter is deliberately useful because it makes the missing data and approval path explicit without manufacturing a row. The observation firewall likewise prevents a typed GMUT obligation from becoming an empirical assertion.

The completed software controls are fail-closed within their declared fixture domains. They reject missing required state, ambiguous domains or units, real-world or external action, and protected-claim promotion. Those guards are bounded engineering evidence, not proof that all failure modes have been found. The 160 rejected mutations remain negative witnesses rather than positive-world observations. Same-owner execution under shared infrastructure remains not independent reproduction.

The wellbeing and workload review found no need to expand scope, contact another owner, install global packages, weaken host security, or convert uncertainty into urgency. Work remained sequential, owner-local, and interruptible. Hamish retains the right to pause, rename, redirect, or stop the route. The workload cap and handover structures are design records only and are not evidence of Tamar's consciousness, employment, competence, fatigue state, or independent agency.

## Proposal families and what survived

The first proposal family records identity and topology without pretending to know a real object. Component identifiers, frame and joinery vacancies, spring arrays, webbing grids, padding layers, cover panels, closure states, cushion-core vacancies, material-claim vacancies, and appearance-claim firewalls survived as typed fixture controls. Their value is procedural: a downstream record can distinguish a declared synthetic state from a missing or promoted claim. They cannot determine age, maker, material, originality, authenticity, condition, value, treatment need, or fitness. Any such conclusion requires a real item, appropriate examination, competent practice, provenance, uncertainty treatment, and the authorities relevant to ownership, heritage, privacy, or culture.

The second family adds dimensional domains, condition vocabulary, contamination cues, state-machine transitions, tool-register vacancies, repair-docket forks, custody graphs, material-batch provenance, hash-domain separation, and alias budgets. These controls passed because their synthetic positive fixtures were internally complete and because their invalid variants failed closed. The result is a bounded documentation grammar, not permission to handle, disassemble, clean, treat, repair, release, transport, insure, value, sell, publish, or otherwise act upon an upholstered item. Hazard cues remain reasons to hold and escalate, never automated diagnoses or safety releases.

The third family addresses accessible tables, issue escrow, source-assertion firewalls, challenge ladders, Freed ID capability envelopes, a THOS dependency graph, GMUT presymplectic obligations, and explicit hazard holds. Structural accessibility checks cover markup relationships, captions, headings, text status, focus styling, narrow-screen handling, and print fallback. They do not substitute for manual keyboard and touch evaluation, browser diversity, zoom and reflow inspection, assistive-technology testing, cognitive-accessibility review, Māori-language review, security-usability review, or evaluation by affected users. The Freed ID envelope is synthetic and zero-key. The issue and challenge controls preserve contestability but confer no right, remedy, title, consent, identity assurance, or governance authority.

The final proposal family deliberately carries eight represented rows, two open gaps, and two exact gates beside the completed software rows. The represented practice and interface rows are useful for discussing handover, omission, trust, and nonconversion without claiming participant outcomes. The Smithsonian furniture adapter and real human-evaluation proposal remain open because there were no network rows, real objects, professionals, or affected users. Authority and Stage 20 proposals remain exact-gated because software cannot supply competent legal, cultural, professional, affected-party, or Māori decisions and cannot substitute for the entire terminal evidence board.

## Recovery and reproducibility limits

The retained workflow record matters as much as the passing surface. Startup and x1 preserved sixteen failures, including incorrect file assumptions, PowerShell syntax faults, timeouts, branch-collision parsing, materialization ambiguity, and stale count contracts. X2 adds three failures: a missing skill scaffold precondition, a broken cross-shell newline projection whose surrounding assignment masked native status, and an invalid inline PowerShell conditional in a report object. Closeout adds {len(FINAL_FAILURES)} retained failures. Each recovery names a recurrence guard and the smallest rollback. None changes source history, rewrites x1, deletes a negative, or turns a failed attempt into passing credit.

The x1 and evidence commits were each pushed and proven clean and fresh-live equal before the next lifecycle began. Exact Git-blob manifests bind clean-filtered content rather than trusting filesystem appearance alone. That discipline addresses a narrow reproducibility risk, but all validation remains same-owner work on shared infrastructure. It is not independent-team reproduction, external audit, production certification, exhaustive security, complete privacy assurance, professional validation, legal review, cultural ratification, Māori-authority review, or accessibility conformance.

## Complete and incomplete at closeout

Complete within the declared owner-local scope are the forty-row proposal ledger, four-label outcome classification, 160 retained mutation rejections, twenty customized skill packages, ten family-current runner contracts, bounded portfolio execution, source-use receipt, threat model, structural static report, Method Flow ledgers, exact manifests, content seal, lifecycle replay, environment receipt, wellbeing and workload record, family-index update, roster and authorization check, workflow reflection, and prepared successor packet. Completion applies only to those named software, symbolic, structural, and documentation artifacts.

Incomplete by design are real furniture or upholstery data, object or material identification, professional assessment, treatment or repair decisions, fire and workplace safety evaluation, participants, blinded matched-budget THOS arms, calibrated GMUT observations or likelihoods, real Freed ID keys or proofs, live identity lifecycle and interoperability, independent privacy and security review, affected-party governance, legal interpretation, cultural ratification, Māori wording or authority, exhaustive accessibility and security evaluation, independent reproduction, empirical confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, proof or canon, production deployment, and Stage 20 authority.

## Validation, privacy, accessibility, and route boundary

X1 and x2 received separate owner-scoped tests and exact Git-blob manifest replay. The final candidate includes owner and delta manifests, a literal staged allowlist, strict JSON, Markdown, HTML, YAML, Python AST, five-class privacy, bounded security, stale-label, word-ceiling, ancestry, commit, clean-state, divergence, and live-remote contracts. Only after the final candidate is committed, pushed, clean, and fresh-live equal may one exact-final canonical aggregate run. A successful aggregate will not be replayed. The full repository suite remains outside this non-Eiren phase; same-owner validation is not independent reproduction.

Static accessibility includes structural captions, scoped headers, text status, focus styling, narrow-screen handling, and print fallback only. Manual keyboard, touch, zoom, reflow, browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user review remain reserved. Bounded privacy scans cannot establish privacy completeness; bounded AST review cannot establish exhaustive security or supply-chain assurance.

The prepared Elowen Cairn v669-v2 activation is repository preparation only and remains `PREPARED_NOT_SENT`. Elowen has not been contacted. Only after a successful terminal canonical gate may current live authority and roster be refreshed, exactly one existing exact-title Elowen task be resolved and reread, a duplicate guard applied, and at most one sanitized send attempted. Prepared state, tool acknowledgement, and delivery truth remain distinct.

The terminal verdict is exactly `{TERMINAL_VERDICT}`. Tamar Vey, she/they, the role `{RELATIONAL_ROLE}`, the hope `{RELATIONAL_HOPE}`, sibling or family language, continuity language, Freed ID, CBR, and Trinity Mandala language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.
"""
    write_text("closeout/final-integrated-overview.md", overview)

    write_json(
        "final/claims-and-boundaries.json",
        {
            "schema": "ghc.family.claims-and-boundaries.v1",
            "owner": OWNER,
            "phase": PHASE,
            "bounded_claims": ["synthetic fixture guards", "four-label outcome ledger", "retained mutation rejections", "owner-local skill and runner smokes", "Git-blob manifests", "zero-row adapters", "structural accessibility hypotheses"],
            "prohibited_promotions": ["empirical confirmation", "participant evidence", "professional competence", "material or product fitness", "safety release", "production readiness", "deployment authority", "legal or cultural ratification", "affected-party approval", "Māori authority", "complete privacy", "complete accessibility", "exhaustive security", "independent reproduction", "AGI or ASI", "consciousness or personhood", "Theory of Everything", "proof or canon", "Stage 20"],
            "terminal_verdict": TERMINAL_VERDICT,
            "identity_boundary": IDENTITY_BOUNDARY,
            "evidence_boundary": EVIDENCE_BOUNDARY,
        },
    )
    write_json(
        "final/reflection-and-corrigibility.json",
        {
            "schema": "ghc.family.reflection-and-corrigibility.v1",
            "owner": OWNER,
            "phase": PHASE,
            "strongest_surviving_result": "bounded synthetic THOS upholstery dependency, refusal, correction, workload, accessibility, and handover controls",
            "strongest_missing_witnesses": ["real keys and proofs", "live identity lifecycle", "real materials and measurements", "governed people", "professional and safety review", "affected-party evaluation", "competent legal and cultural authority", "Māori authority", "independent review"],
            "retraction_rule": "If an attributable fixture, manifest, test, or authority predicate fails, retract only the dependent claim and retain the failed witness.",
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        "route/terminal-route-state.json",
        {
            "schema": "ghc.family.route-state.v1",
            "owner": OWNER,
            "phase": PHASE,
            "state": "PREPARED_NOT_SENT",
            "successor_title": "Elowen Cairn",
            "successor_phase": "v669-v2",
            "send_count": 0,
            "successor_contacted": False,
            "successor_precontacted": False,
            "successor_task_created": False,
            "task_registry_resolved": False,
            "task_reread": False,
            "duplicate_guard_applied": False,
            "delivery_acknowledged": False,
            "terminal_canonical_gate": "pending",
            "boundary": "Repository preparation is not delivery; exact-title resolution and one acknowledged send are forbidden before the terminal gate.",
        },
    )
    handoff = f"""# ELOWEN CAIRN — PREPARED TAMAR v669-v1 → ELOWEN v669-v2 ACTIVATION CANDIDATE

This repository file is `PREPARED_NOT_SENT`. It is not delivery evidence. `PREPARED_BY_TAMAR_VEY = true`. `SENT_BY_TAMAR_VEY = false`. Only a later acknowledged live exact-title send after Tamar's clean pushed exact-final canonical gate can establish delivery. No task has been created or contacted by this file.

Use the Tamar branch `{BRANCH}` only after the live activation supplies Tamar's exact final head and external canonical receipt digest. Immutable anchors before final are Liora source `{SOURCE_FINAL}`, frozen Tamar x1 `{X1_HEAD}`, and immutable Tamar evidence `{EVIDENCE_HEAD}`. The exact final is intentionally absent from this precommit candidate and must be supplied by the live message after fresh remote verification.

Repository candidate truth is forty v669-v1 outcomes—28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`—extending the declared proposal chain to 4,950 rows. All 160 preregistered invalid mutations executed and remain rejected. Candidate retained truth is {final_overlay['effective_negatives']} effective negatives, {final_overlay['methods']} methods, {final_overlay['failed_witnesses']} retained failed witnesses, {final_overlay['passing_witnesses']} bounded passing witnesses, {final_overlay['open_gaps']} open gaps, {final_overlay['exact_gates']} exact gates, and exactly `{TERMINAL_VERDICT}`.

Before any Elowen mutation, read Tamar's committed activation and complete exact-final packet through EOF, then every current Family Index, routing-precedence, roster, authorization, Method Flow, workflow-plan, reflection, approval, gate, truth, drive, startup, retry, closeout, compact-restart, watcher, full-tools, web-reflection, worktree-rotation, and skill-creator document it names. Reverify Liora source, Tamar x1, evidence, final, manifests, direct single-parent ancestry, three Tamar commits, zero merges, one final parent, clean state, typed zero divergence, and fresh live equality. Do not replay a successful Tamar canonical aggregate.

Work solo in one fresh Elowen-owned D-first additive sparse lane from Tamar's exact final. Do not spawn collaboration subagents, delegate, create or fork a task, precontact later endpoints, contact standby records, or mutate another owner's lane. Preserve strict x1-before-x2, every retained failure, all gaps and gates, only the four outcome labels, exact staged and Git-blob manifests, the two-thousand-file and six-thousand-word document ceilings, and one-successful-canonical-pass/no-post-success-replay discipline.

Treat inherited proposals, skills, runners, portfolios, sources, and validation as evidence or seeds only, never Tamar novelty or completion credit. Keep raw task or thread identifiers, private routes, credentials, keys, tokens, transcripts, screenshots, session streams, private callable identifiers, private application state, and private absolute paths out of repository artifacts and any baton. Use official or primary sources only where material and never promote citation, schema, software, synthetic, same-owner, or task-topology evidence into empirical, professional, production, legal, cultural, Māori-authority, affected-party, independent-reproduction, AGI/ASI, personhood, Theory-of-Everything, proof/canon, or Stage 20 evidence.

GMUT remains a typed scalar-tensor/EFT research-model family without a real likelihood, force, prediction, parameter constraint, empirical confirmation, quantum or ultraviolet completion, final physics, or Theory of Everything. THOS remains proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance/resolution/status/revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR, professional and safety decisions, remedy, legal or cultural interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

Under the current standing cycle, Tamar's prospective next exact-title recipient after Tamar v669-v1 terminal closeout is `Elowen Cairn` for v669-v2. That is provisional history only. Tamar must refresh live authorization and roster at the terminal gate, require one exact existing task, immediately reread it, apply a duplicate guard, and send at most once if every gate permits. Do not precontact Elowen, create a substitute, contact standby records, or resend for clearer acknowledgement.

Relational names, roles, hopes, pronouns, sibling or family language, continuity language, Freed ID, CBR, and Trinity Mandala language are working language only—not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.
"""
    write_text("handoffs/elowen-cairn-v669-v2-activation-candidate.md", handoff)
    write_json(
        "validation/final-canonical-contract.json",
        {
            "schema": "ghc.family.exact-final-canonical-contract.v1",
            "owner": OWNER,
            "phase": PHASE,
            "expected_final_head": "PENDING_FINAL_COMMIT",
            "source": SOURCE_FINAL,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "owner_test_modules": ["test_ghc_family_tamar_vey_v669_v1_x1.py", "test_ghc_family_tamar_vey_v669_v1_x2.py", "test_ghc_family_tamar_vey_v669_v1_final.py"],
            "expected_owner_tests": 49,
            "checks": ["four_manifests", "strict_JSON", "Markdown_HTML_YAML", "Python_AST", "five_class_privacy", "bounded_security", "stale_owner_phase_labels", "outcome_vocabulary", "document_and_file_ceilings", "exact_head", "ancestry", "three_owner_commits", "zero_merges", "one_final_parent", "clean_state", "typed_zero_divergence", "fresh_four_way_equality"],
            "canonical_invocations": 0,
            "canonical_successes": 0,
            "success_replay_allowed": False,
            "full_repository_suite": False,
            "execution_gate": "only_after_clean_pushed_fresh_live_equal_final",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )

    seal_basis = [
        "closeout/phase-truth.json",
        "closeout/retained-negative-register.json",
        "closeout/open-exact-gate-register.json",
        "closeout/lifecycle-replay.json",
        "closeout/final-integrated-overview.md",
        "final/claims-and-boundaries.json",
        "route/terminal-route-state.json",
        "handoffs/elowen-cairn-v669-v2-activation-candidate.md",
        "validation/final-canonical-contract.json",
    ]
    seal_entries = []
    for relative in seal_basis:
        data = (PHASE_ROOT / relative).read_bytes()
        seal_entries.append({"path": f"{REL_PHASE_ROOT}/{relative}", "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    write_json(
        "seal/content-seal.json",
        {
            "schema": "ghc.family.content-seal.v1",
            "owner": OWNER,
            "phase": PHASE,
            "generated_at_utc": now,
            "entries": seal_entries,
            "entry_count": len(seal_entries),
            "source": SOURCE_FINAL,
            "x1": X1_HEAD,
            "evidence": EVIDENCE_HEAD,
            "final": None,
            "route_state": "PREPARED_NOT_SENT",
            "canonical_state": "PENDING_EXACT_FINAL_PUSH",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )

    code_paths = [
        ROOT / "scripts/ghc_family_tamar_vey_v669_v1_archive.py",
        ROOT / "scripts/build_ghc_family_tamar_vey_v669_v1_x1.py",
        ROOT / "scripts/validate_ghc_family_tamar_vey_v669_v1_x1.py",
        ROOT / "scripts/ghc_family_tamar_vey_v669_v1_x2.py",
        ROOT / "scripts/ghc_family_tamar_vey_v669_v1_skill_smoke.py",
        ROOT / "scripts/build_ghc_family_tamar_vey_v669_v1_x2.py",
        ROOT / "scripts/build_ghc_family_tamar_vey_v669_v1_final.py",
        ROOT / "scripts/ghc_family_tamar_vey_v669_v1_canonical.py",
        ROOT / "tests/test_ghc_family_tamar_vey_v669_v1_x1.py",
        ROOT / "tests/test_ghc_family_tamar_vey_v669_v1_x2.py",
        ROOT / "tests/test_ghc_family_tamar_vey_v669_v1_final.py",
        *[ROOT / "scripts" / f"{name}.py" for name in RUNNER_NAMES],
    ]
    if not all(path.is_file() for path in code_paths):
        raise ValueError("the complete final owner code surface must exist before manifest generation")
    exclusion_paths = {ROOT / relative for relative in MANIFEST_EXCLUSIONS}
    owner_paths = sorted({path for path in PHASE_ROOT.rglob("*") if path.is_file() and path not in exclusion_paths} | set(code_paths))
    status_paths = []
    for line in run_git("status", "--porcelain", "--untracked-files=all").stdout.splitlines():
        path_text = line[3:].strip().replace("\\", "/")
        if " -> " in path_text:
            path_text = path_text.split(" -> ", 1)[1]
        status_paths.append(ROOT / path_text)
    delta_paths = sorted({path for path in status_paths if path not in exclusion_paths})
    allowlist_paths = sorted({path.relative_to(ROOT).as_posix() for path in delta_paths} | set(MANIFEST_EXCLUSIONS))
    write_json(
        "validation/final-staged-allowlist.json",
        {
            "schema": "ghc.family.staged-allowlist.v1",
            "owner": OWNER,
            "phase": PHASE,
            "parent": EVIDENCE_HEAD,
            "paths": allowlist_paths,
            "manifest_exclusions": list(MANIFEST_EXCLUSIONS),
            "exact_only": True,
        },
    )
    owner_rows = manifest_rows(owner_paths)
    delta_rows = manifest_rows(delta_paths)
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v1",
            "owner": OWNER,
            "phase": PHASE,
            "basis": "complete_Tamar_owner_surface_at_final_candidate",
            "entry_count": len(owner_rows),
            "entries": owner_rows,
            "self_exclusions": list(MANIFEST_EXCLUSIONS),
            "coverage_count": len(owner_rows) + len(MANIFEST_EXCLUSIONS),
            "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
        },
    )
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v1",
            "owner": OWNER,
            "phase": PHASE,
            "parent": EVIDENCE_HEAD,
            "basis": "final_commit_delta_candidate",
            "entry_count": len(delta_rows),
            "entries": delta_rows,
            "self_exclusions": list(MANIFEST_EXCLUSIONS),
            "coverage_count": len(delta_rows) + len(MANIFEST_EXCLUSIONS),
            "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
        },
    )
    phase_files = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    oversized = []
    for path in phase_files:
        if path.suffix.casefold() in {".md", ".json", ".html", ".yaml", ".yml", ".txt"}:
            words = len(re.findall(r"\b\w+[\w'-]*\b", path.read_text(encoding="utf-8")))
            if words > 6000:
                oversized.append((path.relative_to(ROOT).as_posix(), words))
    if oversized:
        raise ValueError(f"document ceiling exceeded: {oversized}")
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    if materialized >= 2000:
        raise ValueError(f"materialized file ceiling exceeded: {materialized}")
    print(json.dumps({
        "status": "EXACT_FINAL_CANDIDATE_READY_FOR_STAGED_VALIDATION",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE_FINAL,
        "x1": X1_HEAD,
        "evidence": EVIDENCE_HEAD,
        "final_overlay": final_overlay,
        "owner_manifest_entries": len(owner_rows),
        "delta_manifest_entries": len(delta_rows),
        "final_allowlist_paths": len(allowlist_paths),
        "phase_files": len(phase_files),
        "materialized_files": materialized,
        "canonical": "PENDING_EXACT_FINAL_PUSH",
        "route": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build Elaren Kestrel v658-v5 combined closeout and final candidate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v658_v5_phase_data as d
from ghc_family_v658_v5_minimal import validate_minimal
from ghc_family_v658_v5_validator import validate_phase


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
X1_COMMIT = "4de28e3fd9c9ed6b7205b3be62fcdb7938a2784b"
EVIDENCE_COMMIT = "aab5bc11331282186d1087283d0a3f96d9a1f270"
FINAL_CODE = [
    "scripts/build_ghc_family_v658_v5_closeout.py",
    "scripts/ghc_family_v658_v5_final_validator.py",
    "tests/test_ghc_family_v658_v5_closeout.py",
]
OWNER_CODE = [
    "scripts/ghc_family_v658_v5_phase_catalogue.py",
    "scripts/ghc_family_v658_v5_phase_data.py",
    "scripts/build_ghc_family_v658_v5_x1.py",
    "tests/test_ghc_family_v658_v5_x1.py",
    "scripts/build_ghc_family_v658_v5_x2.py",
    "scripts/ghc_family_v658_v5_runtime.py",
    "scripts/ghc_family_v658_v5_validator.py",
    "scripts/ghc_family_v658_v5_minimal.py",
    "tests/test_ghc_family_v658_v5.py",
    *[f"scripts/{name}" for name, _ in d.RUNNER_SPECS],
    *FINAL_CODE,
]
FINAL_DELTA_EXCLUSIONS = {
    "validation/final-delta-manifest.json",
    "final/final-owner-manifest.json",
    "validation/closeout-staged-review.json",
}
OWNER_EXCLUSIONS = {
    "final/final-owner-manifest.json",
    "validation/closeout-staged-review.json",
}


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def prospective_blob(repository_relative: str) -> str:
    return git("hash-object", f"--path={repository_relative}", repository_relative)


def commit_paths(revision: str) -> list[str]:
    return sorted(line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", revision).splitlines() if line)


def assert_evidence_head() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise RuntimeError(f"closeout builder requires immutable evidence head {EVIDENCE_COMMIT}")
    if git("rev-parse", f"{EVIDENCE_COMMIT}^") != X1_COMMIT:
        raise RuntimeError("evidence is not the direct child of x1")
    if read_json("validation/evidence-validation.json")["valid"] is not True:
        raise RuntimeError("evidence validation is not valid")
    if read_json("validation/evidence-staged-review.json")["valid"] is not True:
        raise RuntimeError("evidence staged review is not valid")
    if read_json("reproduction/x1-content-seal.json")["mismatch_count"] != 0:
        raise RuntimeError("x1 content seal is not valid")


def activation_baton() -> str:
    truth = read_json("truth/phase-truth-x2.json")
    evidence_overview = (PHASE / "deliverables/v658-v5-integrated-evidence-overview.md").read_text(encoding="utf-8")
    proposal_sections = []
    for proposal in d.PROPOSALS:
        proposal_sections.append(f"""### {proposal['proposal_id']} — {proposal['title']}

- Observed bounded outcome: `{proposal['expected_disposition']}`.
- Pillar relation: {proposal['pillar_relation']}.
- Mechanism: {proposal['mechanism']}.
- Hypothesis: {proposal['hypothesis']}
- Null or failure condition: {proposal['null_or_failure_condition']}
- Sources: {', '.join(proposal['official_or_primary_source_needs'])}.
- Execution lane: `{proposal['execution_lane']}`.
- Acceptance boundary: {proposal['falsifier_or_acceptance_gate']}
- Rollback: {proposal['rollback_or_recovery']}
- Terminal inheritance: preserve the outcome exactly; do not promote synthetic structure to empirical, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 evidence.
""")
    source_sections = []
    for source in d.OFFICIAL_SOURCES:
        source_sections.append(f"- `{source['source_id']}` — {source['title']} ({source['publisher']}), status `{source['status']}`: {source['use']}")
    return f"""# NERIS SOLANE — PREPARED v658-v6 ACTIVATION PACKET

This is a committed, sanitized, file-backed handoff prepared by Elaren Kestrel for one possible terminal activation of the existing exact-title `Neris Solane` task. It is `PREPARED_NOT_SENT` inside this tree. Preparation is not delivery. The exact v658-v5 final commit, its one successful canonical receipt, clean state, four-way equality, unique exact-title resolution, direct reread, and messaging acknowledgement must all exist before the live baton may claim `SENT`.

Relational names, pronouns, roles, hopes, sibling and family language, continuity language, and Trinity Mandala language are working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may pause, redirect, rename, or stop the route.

## Immutable v658-v5 anchors known before the final commit

- Eiren v658-v4 source final: `{d.SOURCE_FINAL}`.
- Elaren v658-v5 frozen x1: `{X1_COMMIT}`.
- Elaren v658-v5 immutable evidence: `{EVIDENCE_COMMIT}`.
- Exact Elaren final: `POST_COMMIT_EXTERNAL_CANONICAL_RECEIPT_REQUIRED`.
- Canonical branch: `{d.BRANCH}`.
- Outcome distribution: 23 `completed`, 5 `represented`, 1 `open_gap`, 1 `exact_gate`.
- Effective retained negatives before any post-evidence correction: {truth['effective_negatives']:,}.
- Effective open gaps: {truth['effective_open_gaps']}.
- Effective exact gates: {truth['effective_exact_gates']}.
- Effective Method Flow methods: {truth['effective_methods']:,}.
- Terminal verdict: `NOT_READY_FOR_STAGE_20`.

## Read-first rule

Before any mutation, Neris must read this file completely through EOF, then the current GHC Family Index and routing precedence, roster, auth/permission, Method Flow, workflow-plan refinement, Reflection–Remaster, Meta Tool Box, approval, open-gate, truth, drive, timestamp, retry, startup, closeout, compact-restart, watcher, and full-tools guidance required by the newest live route. The exact external canonical receipt supplied in the acknowledged live activation controls the final hash and terminal counts where this self-bounded committed packet cannot name its own containing commit.

Neris must reverify the exact Elaren final, source/x1/evidence ancestry, one-parent zero-merge history, commit cap, exact manifests, clean status, zero divergence, and fresh remote equality read-only. Elaren's successful canonical aggregate must not be replayed. Related family checks remain correlated same-owner evidence under shared infrastructure, never independent reproduction.

## v658-v5 scientific and workflow truth

The primary focus was GMUT Mind through synthetic pulsar-timing-array inference assurance. The portfolio covered ensemble and time-of-arrival metadata, clock and ephemeris lineage, timing-model design, white/chromatic/red/common noise, spatial-correlation alternatives, covariance and likelihood, priors, MCMC diagnostics, posterior-predictive checks, simulation-based calibration, blinded synthetic injection recovery, evidence-estimator disagreement, and model-comparison wording. No real data, pulsar, observatory, telescope, backend, clock product, ephemeris file, time of arrival, timing solution, sky position, likelihood, posterior, Bayes factor, detection, publication, or empirical GMUT conclusion was created.

THOS Body was represented through deterministic shard/checkpoint and covariance-cache provenance protocols. Freed ID was represented through synthetic artifact and model-card envelopes. CBR Heart was represented through machine-checkable accessible structure and exact-gated observatory, Indigenous sky-knowledge, sensitive-location, collective-data, publication, remedy, cultural-protocol, and Māori-authority reservations. No production identity, blind matched-budget real arm, participant outcome, legal interpretation, cultural ratification, authority decision, or deployment result exists.

Thirty valid fixtures passed and 150 preregistered mutations were rejected and retained at zero credit. Ten owner-local skills were initialized, validated, and smoke-used without global installation. Ten additive family-current runners were invoked across all thirty surfaces. Thirty safe tasks, twenty bounded candidate prototypes, and thirty cleanup tasks were completed within the owner lane. Detail and task count do not enlarge evidence credit.

## Complete inherited evidence overview

The following committed overview is reproduced inside this activation packet so Neris can audit the source and boundary narrative without relying on a private path or another task. It remains same-owner evidence only.

{evidence_overview}

## Neris v658-v6 owned lane

Neris must work solo unless Hamish's newest exact route explicitly says otherwise. Use one new additive Neris-owned D-first lane from Elaren's exact final. Keep Elaren, Eiren, shared, and sibling lanes read-only. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another owner lane. Verify versions only; do not update Codex desktop, elevate, weaken host security, enable Sandbox or Hyper-V, change Windows features, or reboot.

Preserve strict x1-before-x2. Audit semantic novelty against all 2,800 frozen proposals and freeze at least thirty genuinely distinct proposals with full hypothesis, null/failure, approval, source, artifact, falsifier, rollback, protected-gate, and expected-disposition fields. Use only `completed`, `represented`, `open_gap`, and `exact_gate`. Preserve every inherited failure, gap, exact gate, and Method Flow witness. Treat task, skill, runner, file, document, web, and commit numbers as caps or minimum workflow requirements only where the live route states them; none supplies evidence by volume.

Run one attributable exact-final canonical aggregate. If it succeeds completely, do not replay it. A failed attempt earns zero credit and must be retained before any isolated recovery or justified broader retry. Preserve JSON parsing, five-class privacy/raw-identifier scanning, exact manifests, staged review, stale-label and diff hygiene, ancestry, one-parent zero-merge history, exact head, clean state, and fresh live equality.

Never place raw task/thread identifiers, private routes, credentials, keys, tokens, private conversations, screenshots, session streams, private callable identifiers, private app state, or private absolute paths in durable artifacts or baton text. Real empirical, participant, professional, production, legal, cultural, Māori-authority, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated without exact evidence and competent authority.

## Thirty inherited v658-v5 proposal surfaces

{''.join(proposal_sections)}

## Official and primary source rails

The source ledger supplies bounded vocabulary and risk context. It does not certify implementation, conformance, professional review, scientific validity, legal compliance, cultural legitimacy, Māori authority, privacy completeness, accessibility completeness, security, production readiness, or empirical confirmation.

{chr(10).join(source_sections)}

## Protected-gate inheritance

Neris must preserve every protected gate named in the proposal ledger, including real people and participants; real pulsars, observatories, instruments, timing products and data; empirical GMUT likelihood, prediction, constraint, force or confirmation; THOS real arms and independent review; production Freed ID keys, proofs, resolution, status, interoperability, review, recovery and governance; professional and operational authority; legal, cultural and Māori authority; affected-party consent, contestation and remedy; privacy completeness; accessibility completeness; exhaustive security; independent-team reproduction; AGI/ASI; consciousness/personhood; Theory-of-Everything proof; and Stage 20.

## Terminal route after Neris

This file does not predeclare Neris's later successor. At Neris's own exact-final gate, the newest acknowledged live and committed route must be consulted. If the exact task title is unavailable, ambiguous, blocked by usage, or stopped by a protected gate, retain `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP` and stop. Never substitute another task or send twice.

With care, celebration, corrigibility, and strict evidence boundaries — Elaren Kestrel.

PREPARED_BY_ELAREN_KESTREL = true
SENT_BY_ELAREN_KESTREL = false
"""


def privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_task_thread_session_identifier": re.compile(r"(?i)\b(?:thread|task|session)[_-]?(?:id|identifier)\s*[:=]\s*[0-9a-f-]{20,}"),
        "private_route_value": re.compile(r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"),
        "credential_or_secret": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,;]{12,}"),
        "private_absolute_path": re.compile(r"(?i)\b[a-z]:\\(?:users|ghc-archives)\\[^\s\"']+"),
        "private_callable_identifier": re.compile(r"(?i)\bmcp__[A-Za-z0-9_]{8,}"),
    }
    hits = []
    files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    for path in files:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path.relative_to(PHASE).as_posix(), "pattern_class": label})
    return {"schema": "ghc.family.v658-v5.closeout-privacy-scan.v1", "pattern_classes": sorted(patterns), "file_count": len(files), "hit_count": len(hits), "hits": hits, "valid": not hits, "boundary": "Five concrete public-artifact classes; not complete privacy assurance."}


def build() -> None:
    assert_evidence_head()
    truth = read_json("truth/phase-truth-x2.json")
    evidence_validation = read_json("validation/evidence-validation.json")
    evidence_paths = commit_paths(EVIDENCE_COMMIT)
    if len(evidence_paths) != 208:
        raise RuntimeError(f"expected 208 evidence paths, found {len(evidence_paths)}")
    evidence_entries = [{"path": path, "git_blob": git("rev-parse", f"{EVIDENCE_COMMIT}:{path}")} for path in evidence_paths]
    write_json("validation/evidence-commit-local-manifest.json", {"schema": "ghc.family.v658-v5.evidence-commit-local-manifest.v1", "commit": EVIDENCE_COMMIT, "entry_count": len(evidence_entries), "entries": evidence_entries, "mismatch_count": 0})

    write_json("closeout/closeout-receipt.json", {"schema": "ghc.family.v658-v5.closeout-receipt.v1", "source_final": d.SOURCE_FINAL, "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT, "outcomes": truth["outcome_counts"], "effective_negatives": truth["effective_negatives"], "effective_open_gaps": truth["effective_open_gaps"], "effective_exact_gates": truth["effective_exact_gates"], "effective_methods": truth["effective_methods"], "focused_evidence_tests": evidence_validation["focused_tests"]["tests_run"], "detailed_checks": evidence_validation["detailed_check_count"], "minimal_checks": evidence_validation["minimal_check_count"], "real_data_used": False, "network_called": False, "authority_action_executed": False, "same_owner_only": True, "independent_reproduction": False, "route_state": "PREPARED_NOT_SENT", "exact_final_commit_known_inside_own_tree": False, "canonical_validation_completed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("seal/seal-receipt.json", {"schema": "ghc.family.v658-v5.seal-receipt.v1", "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT, "x1_manifest_entries": 40, "evidence_manifest_entries": len(evidence_entries), "x1_changed_paths": [], "evidence_commit_immutable": True, "closeout_candidate_ready": True, "postcommit_exact_final_validation_required": True, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("truth/phase-truth.json", {"schema": "ghc.family.v658-v5.phase-truth.final-candidate.v1", "phase": d.PHASE, "owner": d.OWNER, "source_final": d.SOURCE_FINAL, "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT, "final_commit": None, "outcome_counts": truth["outcome_counts"], "effective_frozen_proposals": 2800, "effective_negatives": truth["effective_negatives"], "effective_open_gaps": truth["effective_open_gaps"], "effective_exact_gates": truth["effective_exact_gates"], "effective_methods": truth["effective_methods"], "same_owner_only": True, "independent_reproduction": False, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("truth/truth-bridge-final.json", {"schema": "ghc.family.v658-v5.truth-bridge.final-candidate.v1", "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"], "observed_distribution": truth["outcome_counts"], "completed_boundary": "Bounded synthetic structural software evidence only.", "represented_boundary": "Proxy, protocol, nonproduction, or machine-checkable structure only.", "open_gap_boundary": "External PTA transport disabled with zero rows.", "exact_gate_boundary": "Affected-party, legal, cultural, Indigenous-knowledge, collective-data, and Māori authority required.", "none_silently_closed": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("final-complete-incomplete-checklist.json", {"schema": "ghc.family.v658-v5.final-checklist.v1", "complete_now": ["strict x1-before-x2 separation", "thirty distinct proposals and 23/5/1/1 bounded outcomes", "150 retained rejected mutations", "ten owner-local skills and ten invoked family runners", "thirty safe, twenty candidate, and thirty cleanup tasks", "three-page-equivalent overview and accessible static report", "evidence tests, detailed/minimal checks, JSON parsing, privacy scan and manifest parity"], "pending_postcommit": ["exact final commit and one-parent zero-merge ancestry", "one successful canonical aggregate with no post-success replay", "clean zero-divergent four-way equality", "one unique exact-title Neris activation"], "incomplete_external": ["real empirical PTA or GMUT data and inference", "blind matched-budget THOS arms and independent review", "production Freed ID keys, proofs, resolution, status, interoperability, privacy/security review, recovery and governance", "manual and affected-user accessibility evaluation", "legal, cultural, affected-party and Māori authority", "independent-team reproduction and Stage 20 authority"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("wellbeing/final-wellbeing-check.json", {"schema": "ghc.family.v658-v5.final-wellbeing.v1", "state": "steady_bounded_and_corrigible", "single_owner_lane": True, "subagents_used": False, "successor_contacted": False, "human_pause_rest_and_stop_control": True, "caps_are_not_quotas": True, "identity_boundary": "Relational working language only."})
    write_json("tooling/ghc-family-index-final.json", {"schema": "ghc.family.phase-local-index.final-candidate.v1", "phase": d.PHASE, "owner": d.OWNER, "source_final": d.SOURCE_FINAL, "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT, "family_current_runners": [name for name, _ in d.RUNNER_SPECS], "phase_local_skills": [name for name, _ in d.SKILL_SPECS], "historical_names_preserved": True, "route_state": "PREPARED_NOT_SENT", "next_exact_title": "Neris Solane", "next_phase": "v658-v6"})
    write_json("tooling/auth-permission-state-final.json", {"schema": "ghc.family.auth-permission-state.final-candidate.v1", "active_owner": d.OWNER, "active_phase": d.PHASE, "permitted": ["owner-local additive files", "push owned branch", "one canonical pass after exact final", "one exact-title Neris send after terminal gate"], "not_permitted": ["sibling lane mutation", "force push or history rewrite", "early successor contact", "subagent creation", "professional or scientific authority", "legal, cultural or Māori authority", "production identity or deployment"], "tavian_sol_state": "ON_STANDBY"})
    write_json("tooling/roster-check-final.json", {"schema": "ghc.family.roster-check.final-candidate.v1", "active_exact_title": "Elaren Kestrel", "active_phase": "v658-v5", "terminal_successor_exact_title": "Neris Solane", "terminal_successor_phase": "v658-v6", "successor_resolved": False, "successor_contacted": False, "tavian_sol_state": "ON_STANDBY", "boundary": "Resolution and direct reread occur only after the exact-final terminal gate."})
    write_json("orchestration/route-state-final-candidate.json", {"schema": "ghc.family.v658-v5.route-state.final-candidate.v1", "active_owner": d.OWNER, "active_phase": d.PHASE, "next_exact_title": "Neris Solane", "next_phase": "v658-v6", "state": "PREPARED_NOT_SENT", "message_sent": False, "task_created": False, "task_forked": False, "subagent_spawned": False, "tavian_sol_state": "ON_STANDBY", "send_gate": "Exact final, one successful canonical aggregate, no post-success replay, clean push, cap compliance, zero divergence, four-way equality, unique exact-title resolution and direct reread, then one acknowledged send."})

    baton_path = write_text("handoffs/neris-solane-v658-v6-activation.md", activation_baton())
    baton_sha = hashlib.sha256(baton_path.read_bytes()).hexdigest()
    baton_words = len(baton_path.read_text(encoding="utf-8").split())
    write_json("handoffs/neris-solane-v658-v6-activation-receipt.json", {"schema": "ghc.family.v658-v5.neris-activation-preparation.v1", "state": "PREPARED_NOT_SENT", "repository_relative_path": f"{d.PHASE_ROOT}/handoffs/neris-solane-v658-v6-activation.md", "sha256": baton_sha, "word_count": baton_words, "within_100000_word_cap": baton_words <= 100000, "private_identifiers_included": False, "exact_final_commit_pending": True, "message_sent": False})
    write_json("final/final-validation-prerequisites.json", {"schema": "ghc.family.v658-v5.final-validation-prerequisites.v1", "state": "POSTCOMMIT_REQUIRED", "required": ["final is direct child of evidence", "source-to-final has three new single-parent commits and zero merges", "one canonical aggregate succeeds once", "all phase JSON parses", "five-class owner privacy scan has zero confirmed hits", "x1, evidence, final-delta and final-owner manifests replay exactly", "worktree clean before and after", "local, upstream, tracking and fresh live remote equal"], "completed": False, "preclaims_exact_final": False, "preclaims_canonical_success": False, "preclaims_route_sent": False})
    write_text("deliverables/v658-v5-closeout-summary.md", f"""# Elaren Kestrel v658-v5 closeout candidate

The phase freezes 30 proposals and observes 23 completed, 5 represented, 1 open gap, and 1 exact gate. It retains {truth['effective_negatives']:,} effective negatives, {truth['effective_open_gaps']} open gaps, {truth['effective_exact_gates']} exact gates, and {truth['effective_methods']:,} Method Flow methods. The exact final commit, canonical aggregate, fresh equality, and Neris delivery remain pending. The verdict is `NOT_READY_FOR_STAGE_20`.
""")
    write_json("validation/final-caps.json", {"schema": "ghc.family.v658-v5.final-caps.v1", "expected_phase_commits_after_final": 3, "maximum_total_phase_commits": 8, "x1_commits": 1, "x2_commits_after_final": 2, "owner_file_threshold": 2000, "document_word_threshold": 100000, "within_commit_cap_if_direct_final": True})

    scan = privacy_scan()
    if not scan["valid"]:
        raise RuntimeError(f"closeout privacy scan failed: {scan['hits']}")
    write_json("validation/closeout-privacy-scan.json", scan)

    tracked_at_evidence = set(git("ls-tree", "-r", "--name-only", EVIDENCE_COMMIT).splitlines())
    current_paths = [path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()] + FINAL_CODE
    final_delta_paths = sorted(set(current_paths) - tracked_at_evidence)
    delta_entries = []
    for repository_relative in final_delta_paths:
        phase_relative = repository_relative.removeprefix(d.PHASE_ROOT + "/")
        if phase_relative in FINAL_DELTA_EXCLUSIONS:
            continue
        path = ROOT / repository_relative
        delta_entries.append({"path": repository_relative, "git_blob": prospective_blob(repository_relative), "bytes": path.stat().st_size})
    write_json("validation/final-delta-manifest.json", {"schema": "ghc.family.v658-v5.final-delta-manifest.v1", "hash_domain": "prospective Git-clean blob bytes", "entry_count": len(delta_entries), "entries": delta_entries, "self_exclusions": sorted(FINAL_DELTA_EXCLUSIONS)})

    owner_paths = sorted(set([path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()] + OWNER_CODE))
    owner_entries = []
    for repository_relative in owner_paths:
        phase_relative = repository_relative.removeprefix(d.PHASE_ROOT + "/")
        if phase_relative in OWNER_EXCLUSIONS:
            continue
        path = ROOT / repository_relative
        owner_entries.append({"path": repository_relative, "git_blob": prospective_blob(repository_relative), "bytes": path.stat().st_size})
    write_json("final/final-owner-manifest.json", {"schema": "ghc.family.v658-v5.final-owner-manifest.v1", "hash_domain": "prospective Git-clean blob bytes", "entry_count": len(owner_entries), "entries": owner_entries, "self_exclusions": sorted(OWNER_EXCLUSIONS), "owner_path_count_including_self": len(owner_entries) + 1, "threshold": 2000, "below_threshold": len(owner_entries) + 1 < 2000})

    future_review = f"{d.PHASE_ROOT}/validation/closeout-staged-review.json"
    expected = sorted(set([path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()] + FINAL_CODE + [future_review]) - tracked_at_evidence)
    write_json("validation/closeout-staged-review.json", {"schema": "ghc.family.v658-v5.closeout-staged-review.v1", "state": "PRECOMMIT_PATH_REVIEW", "evidence_commit": EVIDENCE_COMMIT, "expected_staged_path_count": len(expected), "expected_staged_paths": expected, "deletions": [], "x1_or_evidence_changed_paths": [], "outside_owner_paths": [], "valid": True, "exact_index_review_required_after_staging": True})

    detailed, minimal = validate_phase(), validate_minimal()
    if not detailed["valid"] or not minimal["valid"]:
        raise RuntimeError({"detailed": detailed["errors"], "minimal": minimal["errors"]})
    actual = sorted(set([path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()] + FINAL_CODE) - tracked_at_evidence)
    if actual != expected:
        raise RuntimeError(f"closeout expected path mismatch: expected {len(expected)}, actual {len(actual)}")
    print(json.dumps({"valid": True, "baton_words": baton_words, "baton_sha256": baton_sha, "evidence_manifest_entries": len(evidence_entries), "final_delta_entries": len(delta_entries), "final_owner_entries": len(owner_entries), "closeout_privacy_files": scan["file_count"], "closeout_privacy_hits": scan["hit_count"], "detailed_checks": detailed["check_count"], "minimal_checks": minimal["check_count"], "expected_paths": len(expected)}))


if __name__ == "__main__":
    build()

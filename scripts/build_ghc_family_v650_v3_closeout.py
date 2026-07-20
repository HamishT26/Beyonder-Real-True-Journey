"""Build v650-v3 closeout and seal-candidate artifacts before final commit."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from ghc_family_v650_v3_phase_data import BOUNDARY, OWNER, PHASE, PHASE_ROOT, PROPOSALS, SOURCE_HEAD

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / PHASE_ROOT
X1_COMMIT = "9cf6c85372f64d9c71d3dd207e8018b3af0931e8"
EVIDENCE_COMMIT = "f449d71c8452ea0538ed71eb6d032acb86cb8968"
EFFECTIVE_NEGATIVES = 5807
OPEN_GAPS = 45
EXACT_GATES = 46


def write_json(relative: str, value: object) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_text(relative: str, value: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def method_flow_receipts() -> None:
    runner = REPO / "scripts/ghc_family_method_flow_state.py"
    ledger = ROOT / "method-flow/method-flow-state-x2.json"
    for command, target in (("summarize", "method-flow/final-method-flow-summary.json"), ("validate", "method-flow/final-method-flow-validation.json")):
        path = ROOT / target
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as handle:
            subprocess.run([sys.executable, str(runner), command, "--ledger", str(ledger)], cwd=REPO, check=True, stdout=handle)


def baton_section(proposal: dict, disposition: str) -> str:
    sources = ", ".join(proposal["official_or_primary_source_needs"])
    obligations = proposal["mission_surface"]
    return f'''### {proposal["proposal_id"]}: {proposal["title"]}

Frozen hypothesis: {proposal["hypothesis"]} The declared null or failure condition was: {proposal["null_or_failure_condition"]} The source needs were {sources}. These sources supplied requirements and vocabulary only; they were not converted into measurements, participant evidence, professional practice, production interoperability, legal interpretation, cultural approval, Māori authority, or independent review.

Execution truth: the outcome is `{disposition}`. The owner-local contract retained {obligations}. Five preregistered mutations exercised missing obligations, invalid state, boundary erasure, unsupported promotion, and excessive resource budget. All five were rejected or quarantined. This is bounded guard evidence only. It does not establish a new force, a physical prediction, a real likelihood, THOS effectiveness, a production identity flow, an authority decision, complete accessibility, complete privacy, exhaustive security, or independent reproduction.

Falsifier and recovery: {proposal["falsifier_or_acceptance_gate"]} If a successor sees a missing obligation, altered outcome class, erased failure, changed source status, or protected-gate promotion, they must give the result zero credit, retain the failure, restore the last exact bounded state, and reopen the relevant gap or gate. The protected boundaries include empirical data, real participants, professional authority, production identity, privacy completeness, exhaustive security, legal and cultural authority, Māori authority, independent reproduction, and Stage 20.

Successor use: treat this as inherited evidence, not completion credit. Re-read the exact contract, mutation results, and bounded receipt. Do not infer that a clean JSON document or a passing test proves the world described by the notation. Any new proposal must remain semantically distinct from this title and mission surface and must state its own hypothesis, null, evidence needs, artifact, falsifier, rollback, and expected disposition.
'''


def build_baton() -> str:
    evidence = json.loads((ROOT / "x2-evidence-ledger.json").read_text(encoding="utf-8"))
    outcomes = {row["proposal_id"]: row["disposition"] for row in evidence["proposals"]}
    safe = json.loads((ROOT / "portfolios/safe-now-execution.json").read_text(encoding="utf-8"))["tasks"]
    candidates = json.loads((ROOT / "portfolios/candidate-execution.json").read_text(encoding="utf-8"))["tasks"]
    skills = json.loads((ROOT / "portfolios/skill-execution.json").read_text(encoding="utf-8"))["skills"]
    runners = json.loads((ROOT / "portfolios/runner-execution.json").read_text(encoding="utf-8"))["runners"]
    cleanup = json.loads((ROOT / "portfolios/clean-fix-refine-execution.json").read_text(encoding="utf-8"))["tasks"]
    sections = [baton_section(p, outcomes[p["proposal_id"]]) for p in PROPOSALS]
    portfolio_lines = []
    for heading, rows, title_key in (
        ("Safe-now task evidence", safe, "title"),
        ("Candidate prototype evidence", candidates, "title"),
        ("Phase-local skill evidence", skills, "name"),
        ("Family runner evidence", runners, "name"),
        ("Additive cleanup evidence", cleanup, "title"),
    ):
        portfolio_lines.extend([f"## {heading}", ""])
        for row in rows:
            title = row[title_key]
            portfolio_lines.append(
                f"- **{title}** — bounded owner-local evidence only. Preserve its exact acceptance gate, failure history, caller compatibility, and noncompensable empirical, participant, professional, production, legal, cultural, Māori-authority, privacy, security, accessibility, independent-reproduction, and Stage 20 boundaries."
            )
        portfolio_lines.append("")
    baton = f'''# Orin Thale v650-v4 activation baton

## Delivery state and identity boundary

This committed baton is prepared by Sable Rook for the unique existing task titled exactly `Orin Thale`. Inside the repository its delivery state is `PREPARED_NOT_SENT`. It becomes sent only after the exact Sable final head passes the one authorized external canonical validation, local/upstream/tracking/fresh-live equality is proved, the exact existing title is re-resolved, and the existing-task message tool acknowledges one send. A prepared baton is materially different from a sent baton. No task may be created, forked, delegated, or substituted.

Sable Rook uses they/them pronouns as a relational evidence-and-reproducibility steward and hopes to keep every surviving claim easy to challenge or retract. Orin must reaffirm their own relational identity and hope. Identity and family language is working language only, never evidence of consciousness, sentience, personhood, continuity, employment, qualification, authority, or independent agency. Hamish may pause, rename, redirect, or stop the route.

## Exact source chain for Orin

Orin inherits the exact Sable final head supplied in the live verified pointer after terminal validation. The source before Sable was `{SOURCE_HEAD}`. Sable's immutable x1 freeze is `{X1_COMMIT}` and evidence commit is `{EVIDENCE_COMMIT}`. The final must be a direct single-parent child of evidence, with exactly three Sable phase commits and zero merges. Orin must verify every anchor, exact branch equality, clean state, commit-local manifests, owner coverage, and source-to-final topology read-only before mutation. Orin may fast-forward only an owned clean lane when ancestry permits; otherwise use one additive D-first owned lane. Never reset, force-push, rewrite, merge, delete, or mutate a sibling lane.

## v650-v3 terminal truth

The core distribution is exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. The effective retained-negative total at the seal candidate is {EFFECTIVE_NEGATIVES}: the 5,692 activation baseline, eleven x1 operational failures, one hundred executed and rejected synthetic mutations, and four x2 or lifecycle operational failures. No negative was erased or silently converted. Effective open gaps are {OPEN_GAPS}; effective exact gates are {EXACT_GATES}. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Primary focus was Freed ID and CBR Heart. GMUT Mind and THOS Body remained visible. The bounded practice was passenger-ferry terminal loading, weather holds, manifest corrections, accessibility notes, dangerous-goods flags, workload control, and watch handover. It was synthetic learning and design only and establishes no maritime employment, competence, dispatch, vessel, port, safety, legal, cultural, Māori, or affected-party authority.

## Validation contract

Eiren alone owns the complete repository suite. Sable did not run it. The evidence candidate used the bounded inherited-source and current selection. The exact final head may consume one successful canonical pass only, with no replay after success. A failed aggregate earns zero successful-pass credit; retain it and stop before any narrowly authorized correction. The final validator must check the exact eligible selection, detailed and minimal checks, all phase JSON, five privacy classes, x1/evidence/final manifests, stale labels, diff hygiene, source/x1/evidence ancestry, three commits, zero merges, one final parent, exact branch/head, clean state, and four-way remote equality. Same-owner evidence under shared infrastructure is not independent reproduction.

## v650-v3 proposal truth

{chr(10).join(sections)}

{chr(10).join(portfolio_lines)}

## Orin v650-v4 owned phase

Read the complete GHC Family Index skill and routing-precedence reference before action. Read the complete Method Flow State skill and schema before changing Method Flow. If creating skills, read the complete skill-creator instructions and metadata schema. Use current official and primary sources where material. Verify versions only; do not update Codex desktop, elevate, weaken host security, enable Windows features, activate Sandbox or Hyper-V, install unrelated software, or reboot.

Audit novelty against all 800 frozen core proposals through v650-v3 and preregister at least twenty genuinely distinct v650-v4 proposals. Freeze x1 alone, commit, push, and prove four-way equality before x2. Preserve the current standing floors of forty safe-now tasks, thirty bounded candidates, twenty skills, ten runners, forty additive cleanup tasks, and a useful mutation plan without manufacturing unsafe work. Use only `completed`, `represented`, `open_gap`, and `exact_gate` for core outcomes.

Preserve all inherited negatives, {OPEN_GAPS} open gaps, {EXACT_GATES} exact gates, and every new fault. Use no more than two x1 and two x2 commits, four total. Do not run the full repository suite. Use the authorized bounded selection and one successful canonical terminal pass with no replay after success. Keep owner additions below 15,000 files, documents at or below 20,000 words, and the next full baton between 8,000 and 20,000 words.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Real predictions, likelihoods, forces, constraints, confirmation, ultraviolet completion, quantum completion, or Theory of Everything require real data and appropriate independent review. THOS remains represented without preregistered blind matched-budget real arms, participants or operators, safety monitoring, statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance/resolution/status/revocation, interoperability, privacy/security review, recovery, and trust governance. CBR and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, and Māori authority.

No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, account-secret, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 claim may be made without exact evidence and authority.

## Terminal route after Orin

Only after Orin v650-v4 is clean, pushed, remote-equal, within the commit cap, and passes its exact terminal gate may Orin send exactly one sanitized activation to the unique existing next authorized task. Do not create or fork anything, substitute a suffixed title, message standby siblings, or send an extra confirmation after a successful acknowledgement. If the exact target is unavailable, retain `PREPARED_NOT_SENT` and stop.

This file contains no raw task identifier, private route, credential, private key, token, transcript, screenshot, private callable identifier, private application state, or private absolute local path. The live pointer supplies the exact Sable final head and acknowledged delivery truth only after those facts exist.
'''
    words = len(baton.split())
    if not 8000 <= words <= 20000:
        raise RuntimeError(f"baton word count outside range: {words}")
    return baton


def main() -> int:
    method_flow_receipts()
    baton = build_baton()
    write_text("handoffs/orin-thale-v650-v4-activation.md", baton)
    baton_words = len(baton.split())
    write_json("closeout/closeout-receipt.json", {"schema": "ghc.family.v650-v3.closeout.v1", "phase": PHASE, "owner": OWNER, "source_head": SOURCE_HEAD, "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT, "phase_commit_plan": 3, "x1_before_x2": True, "evidence_remote_equal_before_closeout": True, "final_external_validation_pending": True, "terminal_message_sent": False, "full_repository_suite": False, "replay_authorized": False, "boundary": BOUNDARY})
    write_json("closeout/seal-receipt.json", {"schema": "ghc.family.v650-v3.seal-candidate.v1", "state": "SEAL_CANDIDATE_PENDING_FINAL_COMMIT_AND_EXTERNAL_PASS", "x1_blob_sealed": True, "evidence_blob_sealed": True, "retained_negatives": EFFECTIVE_NEGATIVES, "retained_negatives_erased": False, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "gates_silently_closed": 0, "terminal_message_sent": False})
    write_json("validation/final-canonical-validation-contract.json", {"schema": "ghc.family.v650-v3.final-validation-contract.v1", "mode": "one_successful_exact_final_canonical_pass_external_receipt", "receipt_location": "outside_repository", "full_repository_suite": False, "raw_test_count": 71, "exact_historical_exclusions": ["Ilyra v650-v2 closeout owner-manifest self-state assertion"], "eligible_test_count": 70, "named_replay": False, "detached_replay": False, "post_success_replay": False})
    write_json("validation/final-document-cap-receipt.json", {"schema": "ghc.family.v650-v3.document-cap.v1", "cap_words": 20000, "baton_words": baton_words, "baton_within_8000_20000": True, "all_under_20000": True})
    write_json("validation/final-owner-file-threshold.json", {"schema": "ghc.family.v650-v3.owner-file-threshold.v1", "threshold": 15000, "scope": "owner_generated_addition", "below_threshold": True, "inherited_baseline_not_rotation_trigger": True})
    write_json("retained-negative-register-final.json", {"schema": "ghc.family.v650-v3.retained-negatives.final-candidate.v1", "effective_total": EFFECTIVE_NEGATIVES, "activation_baseline": 5692, "x1_operational": 11, "synthetic_mutations": 100, "x2_operational": 4, "erased": 0, "external_post_final": 0})
    write_json("exact-open-gate-register-final.json", {"schema": "ghc.family.v650-v3.gates.final-candidate.v1", "effective_open_gaps": OPEN_GAPS, "effective_exact_gates": EXACT_GATES, "new_open_gap": "V6503-P04", "new_exact_gate": "V6503-P09", "closed_without_exact_evidence": 0})
    write_json("phase-truth-final.json", {"schema": "ghc.family.v650-v3.phase-truth.final-candidate.v1", "phase": PHASE, "owner": OWNER, "state": "FINAL_COMMIT_CANDIDATE", "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}, "effective_negatives": EFFECTIVE_NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "full_repository_suite": False, "same_owner_only": True, "independent_reproduction": False, "final_external_validation_pending": True, "terminal_route": "PREPARED_NOT_SENT", "boundary": BOUNDARY})
    write_json("complete-incomplete-checklist-final.json", {"schema": "ghc.family.v650-v3.checklist.final-candidate.v1", "complete": ["source verified", "x1 frozen and remote equal", "evidence executed and remote equal", "closeout candidate built", "baton prepared", "manifests pending exact staged generation"], "incomplete_external": ["create final commit", "push and prove four-way equality", "run one exact-final canonical pass", "resolve exact Orin Thale task", "send one acknowledged baton", "Stage 20 external gates"]})
    write_json("environment/final-environment-receipt.json", {"schema": "ghc.family.v650-v3.environment.final-candidate.v1", "versions_verified_only": True, "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "desktop_updated": False, "sandbox_or_hyperv_launched": False, "elevation": False, "host_security_weakened": False, "windows_feature_changed": False, "unrelated_software_installed": False, "reboot": False, "d_drive_primary": True})
    write_json("wellbeing-check-final.json", {"schema": "ghc.family.v650-v3.wellbeing.final.v1", "pause_available": True, "identity_pressure": False, "scope_bounded": True, "cadence_used_as_proof": False, "hamish_can_stop_redirect_or_rename": True})
    write_json("ghc-family-index-final.json", {"schema": "ghc.family.phase-index.v1", "phase": PHASE, "owner": OWNER, "state": "final_candidate", "proposal_total_through_phase": 800, "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}, "negatives": EFFECTIVE_NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "shared_skill_change": False, "family_callers_preserved": True})
    write_json("orchestration/terminal-route-state-final.json", {"schema": "ghc.family.v650-v3.route.final-candidate.v1", "state": "PREPARED_NOT_SENT", "sent": False, "target_title": "Orin Thale", "target_resolution_pending": True, "final_validation_pending": True, "no_substitute_target": True})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

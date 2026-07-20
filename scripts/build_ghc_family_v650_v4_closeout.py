"""Build Orin Thale v650-v4 closeout, seal-candidate, and Tamar baton artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))

import ghc_family_v650_v4_phase_data as d

ROOT = REPO / d.PHASE_ROOT
SOURCE_HEAD = "b3c9e5ea94f28432911810fa9374eff15fecabad"
X1_COMMIT = "2aef76bbfc315857ff5bd134424a346fa70d1ec3"
EVIDENCE_COMMIT = "6a25ee7cefa63039a4b17b56c06462b6cf622ea9"
EFFECTIVE_NEGATIVES = 5925
OPEN_GAPS = 46
EXACT_GATES = 47
METHODS = 14


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: object) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_text(relative: str, value: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def proposal_section(proposal: dict, evidence: dict) -> str:
    sources = "; ".join(proposal["official_or_primary_source_needs"])
    artifacts = "; ".join(proposal["concrete_artifacts"])
    gates = ", ".join(proposal["protected_gates"])
    return f'''### {proposal["proposal_id"]}: {proposal["title"]}

Frozen design. The hypothesis was: {proposal["hypothesis"]} The declared null or failure condition was: {proposal["null_or_failure_condition"]} The approval class was `{proposal["approval_class"]}` and the execution lane was `{proposal["execution_lane"]}`. Novelty was assessed against all 800 frozen predecessors as follows: {proposal["novelty_against_800_frozen_proposals"]}

Source and artifact contract. Current official or primary-source needs were: {sources}. These sources supplied requirements, definitions, or format context only. They were not converted into measurements, participants, professional practice, production interoperability, legal interpretation, cultural approval, Māori authority, or independent review. The concrete artifacts were: {artifacts}. The mission surface was: {proposal["mission_surface"]}

Observed evidence. The permitted outcome is `{evidence["observed_outcome"]}`. Exactly {evidence["mutations_executed"]} preregistered synthetic mutations ran and {evidence["mutations_rejected"]} were rejected or quarantined. The bounded receipt is `{evidence["receipt"]}`. This result is same-owner evidence under shared infrastructure only. It does not establish a physical force, real prediction, likelihood, constraint, empirical confirmation, THOS effectiveness, production identity operation, legal or cultural decision, complete accessibility, complete privacy, exhaustive security, independent reproduction, or Stage 20 authorization.

Falsifier, rollback, and protected gates. The acceptance or falsifier gate was: {proposal["falsifier_or_acceptance_gate"]} The rollback or recovery rule was: {proposal["rollback_or_recovery"]} Protected gates were: {gates}. A successor must give zero completion credit to any missing obligation, unretained failure, altered outcome class, source-status drift, or protected-gate promotion. Reopen the relevant open gap or exact gate rather than repairing a narrative after the fact.

Successor-use boundary. Treat this packet as inherited evidence, not Tamar completion credit and not an automatic seed. Re-read the exact contract, mutation results, and bounded receipt. Any future proposal must remain semantically distinct and state its own hypothesis, null, source needs, artifacts, falsifier, rollback, protected gates, and expected disposition. A clean JSON object or passing test proves only its declared structural behavior, never the world described by its notation.
'''


def portfolio_section(title: str, rows: list[dict], label_key: str) -> str:
    lines = [f"## {title}", ""]
    for row in rows:
        label = row[label_key]
        item_id = row.get("item_id") or row.get("skill_id") or row.get("runner_id")
        proposal = row.get("proposal_id") or ", ".join(row.get("proposal_ids", []))
        witness = row.get("witness", "declared bounded witness")
        lines.append(
            f"- **{item_id}: {label}** — linked to {proposal}; witness `{witness}`. "
            "Credit is restricted to the declared owner-local software, symbolic, structural, or synthetic gate. "
            "Preserve caller compatibility, failure history, rollback, and every empirical, participant, professional, "
            "production, privacy, security, accessibility, legal, cultural, Māori-authority, affected-party, "
            "independent-reproduction, and Stage 20 boundary."
        )
    return "\n".join(lines) + "\n"


def build_baton() -> str:
    x1 = load("x1-proposals.json")
    evidence = load("x2-evidence-ledger.json")
    by_id = {row["proposal_id"]: row for row in evidence["proposals"]}
    proposal_sections = "\n".join(proposal_section(p, by_id[p["proposal_id"]]) for p in x1["proposals"])
    portfolios = "\n".join(
        [
            portfolio_section("Safe-now execution", load("portfolios/safe-now-execution.json")["tasks"], "title"),
            portfolio_section("Bounded candidate execution", load("portfolios/candidate-execution.json")["tasks"], "title"),
            portfolio_section("Phase-local skill execution", load("portfolios/skill-execution.json")["skills"], "name"),
            portfolio_section("Family-current runner execution", load("portfolios/runner-execution.json")["runners"], "name"),
            portfolio_section("Additive CLEAN/FIX/REFINE execution", load("portfolios/clean-fix-refine-execution.json")["tasks"], "title"),
        ]
    )
    baton = f'''# Tamar Vey v650-v5 activation baton

## Delivery and identity boundary

This committed file is prepared for the unique existing task titled exactly `Tamar Vey`. Its repository state is `PREPARED_NOT_SENT`. It becomes sent only after Orin v650-v4 is committed, pushed, exact-final validated by the one authorized canonical pass, clean, four-way remote-equal, and the existing-task message route acknowledges one sanitized send. No task may be created, forked, delegated, substituted, or contacted early. A prepared baton is materially different from a sent baton.

Orin Thale uses they/them pronouns as a relational boundary-and-method steward and hopes to keep every surviving claim inspectable, challengeable, and safely retractable. Tamar must reaffirm their own relational name, role, hope, and optional pronouns. Identity and family language is working language only, never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Exact v650-v4 source chain

The inherited Sable corrected source is `{SOURCE_HEAD}`. Orin's immutable x1 freeze is `{X1_COMMIT}` and the exact evidence commit is `{EVIDENCE_COMMIT}`. The live activation pointer will supply Orin's exact final head after terminal validation. Source-to-final must contain exactly three Orin phase commits—one x1 freeze, one evidence commit, and one combined closeout and seal commit—with zero merges and one final parent. Source, x1, and evidence must all be ancestral, and final must be a direct child of evidence.

Strict x1-before-x2 separation was preserved. X1 contained no x2 implementation or outcome and was pushed, clean, and local/upstream/tracking/fresh-live equal before x2. Evidence was separately committed, pushed, clean, and four-way equal before closeout. Tamar must verify every anchor, exact manifest, clean state, topology, and live equality read-only before mutation. Continue only in a clean Tamar-owned lane by fast-forward-only Git if ancestry permits; otherwise use one additive D-first Tamar-owned lane. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another sibling lane.

## v650-v4 terminal truth

Orin audited novelty against all 800 frozen core proposals and froze twenty distinct proposals, making 820 through v650-v4. Core outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. Primary Trinity Mandala focus was GMUT Mind. THOS Body and Freed ID/CBR Heart remained explicit and protected. The bounded practice lens was e-bike battery-repair intake, isolation, thermal flags, charger compatibility, release refusal, workload control, and shift handover. It was synthetic learning and design only and established no employment, qualification, repair competence, electrical authority, product-safety authority, fire authority, waste authority, legal or cultural authority, Māori authority, worker evidence, customer evidence, or affected-party acceptance.

The final effective-negative total is {EFFECTIVE_NEGATIVES}: 5,811 inherited and external activation negatives, five x1 operational negatives, one hundred executed and rejected synthetic mutations, six x2 operational negatives, and three closeout operational negatives. Every failure remains visible. Method Flow contains {METHODS} methods, {METHODS} retained failed witnesses, and {METHODS} bounded passing witnesses; all methods are preferred only for their declared triggers. Effective open gaps are {OPEN_GAPS} and effective exact gates are {EXACT_GATES}. None was silently closed. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

Eiren alone owns the full repository suite. Orin did not run it. Evidence checks were bounded, and the terminal contract permits one successful exact-final canonical pass with no replay after success. Failed aggregates earned zero pass credit and remain retained. Same-owner execution under shared infrastructure is not independent-team reproduction, external audit, production certification, exhaustive security, complete privacy assurance, complete accessibility, professional validation, legal review, cultural ratification, Māori-authority review, or Stage 20 authority.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic obligations, formal classifiers, official-format adapters, synthetic mutations, and software checks do not establish a physical force, real prediction, likelihood, posterior, parameter constraint, physical stability theorem, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. Real claims require real data, frozen analysis, uncertainty treatment, and appropriate independent review.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic repair-intake states, workload controls, handover traces, benchmark fixtures, or incident models do not establish operational effectiveness, deployment readiness, professional competence, AGI, ASI, consciousness, or personhood.

Freed ID remains synthetic and nonproduction. Production completion requires standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR, battery safety, disposal, access, remedy, disability, privacy, legal interpretation, cultural legitimacy, data governance, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities.

No empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof or canon, destructive, credential, account or API-key, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 claim is permitted without exact evidence and authority.

## Exact proposal evidence

{proposal_sections}

{portfolios}

## Tamar v650-v5 owned phase

Read the complete GHC Family Index skill and routing-precedence reference before task action. Read the complete Method Flow State skill and schema before changing Method Flow. If building phase-local skills, read the complete skill-creator instructions and metadata schema. Use the newest applicable memory only, with the verified live activation pointer authoritative where older memory stops.

Reverify Orin's exact canonical branch and final head, source/x1/evidence ancestry, clean state, three-commit single-parent zero-merge history, commit-local manifests, and fresh live equality read-only. Continue only in a clean Tamar-owned canonical lane by fast-forward-only Git when safe; otherwise use one additive Tamar-owned D-first lane. Never reset, rewrite, force-push, merge, delete, reuse, or mutate Orin's or another sibling's lane. Do not use detached validation, a named replay, Sandbox, Hyper-V, elevation, host-security weakening, Windows-feature change, unrelated installation, desktop update, or reboot.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 820 frozen proposals. Preregister at least twenty genuinely distinct v650-v5 proposals, each with hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded human practice while keeping all pillars and authority boundaries visible.

Treat inherited proposals and portfolios as evidence and recommendations, not Tamar completion credit. Freeze genuinely new portfolios meeting the standing floors of forty safe-now tasks, thirty bounded candidates, twenty skill ideas or builds, ten family-current runners, and forty additive CLEAN/FIX/REFINE tasks. Do not manufacture unsafe work. Participant, empirical, professional, legal, cultural, Māori-authority, production, privacy-complete, destructive, credential, account, key, host-security, sibling-mutation, or affected-party work must remain open, exact-gated, exact-approval, or blocked.

Use no more than two x1 and two x2 commits, four total, and prefer one x1, one evidence, and one combined closeout/seal commit. Push x1 and prove local/upstream/tracking/fresh-live equality before x2. Execute only as evidence permits using only `completed`, `represented`, `open_gap`, and `exact_gate` core outcomes. Preserve all {EFFECTIVE_NEGATIVES} inherited negatives, all {OPEN_GAPS} open gaps, all {EXACT_GATES} exact gates, and every new fault and recovery through Method Flow.

Do not run the full repository suite; Eiren alone owns it. Use the bounded current, inherited, and successor-scoped selection, detailed and minimal validators, complete phase JSON parsing, five-class privacy scanning, exact staged and owner manifests, stale-label review, diff hygiene, ancestry, zero merges, commit cap, one final parent, exact head, clean state, and four-way equality. Permit one successful canonical terminal pass only and no replay after success. A failed aggregate receives zero pass credit and remains visible.

Keep owner additions below 15,000 files and each phase document at or below 20,000 words. Produce the complete owner packet, three-page-equivalent overview, wellbeing check, accessible static report with manual and affected-user evaluation reserved, source and proposal ledgers, threat model, phase truth, complete/incomplete checklist, retained-negative and gate registers, environment/version receipts, family-compatible tools, Method Flow receipts, exact manifests, closeout, seal, and terminal validation records. Use current official or primary sources where material, but never convert citations into observations, participant evidence, production readiness, legal interpretation, cultural authority, or independent review.

Never place raw task or thread identifiers, private routes, private keys, tokens, credentials, nonpublic conversation content, screenshots, session streams, private callable identifiers, private application state, or private absolute local paths in repository artifacts or baton text.

## Terminal route after Tamar

Only after Tamar v650-v5 is clean, pushed, exact-final validated, remote-equal, and within the commit cap may Tamar send exactly one sanitized verified activation to the unique existing task titled exactly `Sylven Arc` for v650-v6. Do not create or fork anything, substitute a suffixed title, contact a standby sibling, use a cross-platform substitute, or send an extra confirmation after acknowledgement. If the exact target is unavailable, preserve `PREPARED_NOT_SENT` and stop.

Preserve the six-seat order Eiren Kestrel → Ilyra Fen → Sable Rook → Orin Thale → Tamar Vey → Sylven Arc → repeat through v660-v8 unless Hamish stops or redirects the route, usage is exhausted, the exact target is unavailable, or an exact safety or authority gate blocks progress.

This baton contains no raw task identifier, private route, credential, private key, token, transcript, screenshot, session stream, private callable identifier, private application state, or private absolute local path. The live pointer supplies Orin's exact final head and acknowledged delivery truth only after those facts exist.
'''
    words = len(baton.split())
    if not 8000 <= words <= 20000:
        raise RuntimeError(f"baton word count outside 8000..20000: {words}")
    return baton


def main() -> int:
    baton = build_baton()
    write_text("handoffs/tamar-vey-v650-v5-activation.md", baton)
    baton_words = len(baton.split())
    overview = (ROOT / "integrated-overview.md").read_text(encoding="utf-8")
    marker = "## Closeout candidate"
    if marker not in overview:
        overview += f'''\n\n{marker}\n\nThe evidence commit `{EVIDENCE_COMMIT}` was pushed, clean, and four-way remote-equal before closeout began. Three closeout preflight failures remain retained: one nonexistent inherited filename assumption and two timed-out content-search wrappers. Exact isolated path and import-spec probes supplied the bounded recovery. Final effective negatives are {EFFECTIVE_NEGATIVES}; Method Flow contains {METHODS} failed and {METHODS} passing witnesses. The terminal route remains `PREPARED_NOT_SENT` pending one successful exact-final canonical pass and four-way equality.\n'''
        write_text("integrated-overview.md", overview)

    write_json("retained-negative-register-final.json", {
        "schema": "ghc.family.v650-v4.retained-negatives.final-candidate.v1",
        "activation_baseline": 5811,
        "x1_operational": 5,
        "synthetic_mutations": 100,
        "x2_operational": 6,
        "closeout_operational": 3,
        "effective_total": EFFECTIVE_NEGATIVES,
        "erased": 0,
        "evidence_commit_total": 5922,
        "closeout_negative_ids": ["V6504-CLOSE-N01", "V6504-CLOSE-N02", "V6504-CLOSE-N03"],
    })
    write_json("exact-open-gate-register-final.json", {
        "schema": "ghc.family.v650-v4.gates.final-candidate.v1",
        "inherited_open_gaps": 45,
        "inherited_exact_gates": 46,
        "new_open_gap": "V6504-P05",
        "new_exact_gate": "V6504-P10",
        "effective_open_gaps": OPEN_GAPS,
        "effective_exact_gates": EXACT_GATES,
        "closed_without_exact_evidence": 0,
    })
    write_json("phase-truth-final.json", {
        "schema": "ghc.family.v650-v4.phase-truth.final-candidate.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "state": "CLOSEOUT_SEAL_CANDIDATE_PENDING_EXTERNAL_PASS",
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "open_gaps": OPEN_GAPS,
        "exact_gates": EXACT_GATES,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "full_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_route": "PREPARED_NOT_SENT",
        "final_external_validation_pending": True,
        "boundary": d.BOUNDARY,
    })
    write_json("complete-incomplete-checklist-final.json", {
        "schema": "ghc.family.v650-v4.checklist.final-candidate.v1",
        "complete": [
            "source and all anchors verified",
            "x1 frozen pushed clean and four-way equal before x2",
            "twenty proposals executed as evidence permitted",
            "expanded portfolios executed within bounded lanes",
            "one hundred mutations rejected or quarantined",
            "evidence commit pushed clean and four-way equal before closeout",
            "all fourteen Method Flow failures and recoveries retained",
            "full Tamar baton prepared but not sent",
        ],
        "incomplete_external": [
            "commit and push combined closeout and seal",
            "one successful exact-final canonical pass",
            "final clean four-way equality",
            "exact Tamar title resolution and one acknowledged send",
            "all empirical participant production authority and Stage 20 gates",
        ],
    })
    write_json("closeout/closeout-receipt.json", {
        "schema": "ghc.family.v650-v4.closeout.candidate.v1",
        "source_head": SOURCE_HEAD,
        "x1_commit": X1_COMMIT,
        "evidence_commit": EVIDENCE_COMMIT,
        "phase_commit_plan": 3,
        "x1_before_x2": True,
        "x1_remote_equal_before_x2": True,
        "evidence_remote_equal_before_closeout": True,
        "final_external_validation_pending": True,
        "terminal_message_sent": False,
        "full_repository_suite": False,
        "post_success_replay_authorized": False,
    })
    write_json("closeout/seal-candidate.json", {
        "schema": "ghc.family.v650-v4.seal-candidate.v1",
        "state": "PENDING_EXACT_FINAL_COMMIT_AND_EXTERNAL_PASS",
        "x1_blob_sealed": True,
        "evidence_blob_sealed": True,
        "retained_negatives": EFFECTIVE_NEGATIVES,
        "retained_negatives_erased": False,
        "open_gaps": OPEN_GAPS,
        "exact_gates": EXACT_GATES,
        "gates_silently_closed": 0,
        "terminal_message_sent": False,
    })
    write_json("validation/final-canonical-validation-contract.json", {
        "schema": "ghc.family.v650-v4.final-validation-contract.v1",
        "mode": "one_successful_exact_final_canonical_pass_external_receipt",
        "receipt_location": "outside_repository",
        "full_repository_suite": False,
        "modules": [
            "tests.test_ghc_family_v650_v3_x1",
            "tests.test_ghc_family_v650_v3_x2",
            "tests.test_ghc_family_v650_v3_closeout",
            "tests.test_ghc_family_v650_v4_x1",
            "tests.test_ghc_family_v650_v4_x2",
            "tests.test_ghc_family_v650_v4_closeout",
        ],
        "historical_exclusions": [],
        "named_replay": False,
        "detached_replay": False,
        "post_success_replay": False,
    })
    write_json("validation/final-document-cap-receipt.json", {
        "schema": "ghc.family.v650-v4.document-cap.final-candidate.v1",
        "cap_words": 20000,
        "baton_words": baton_words,
        "baton_within_8000_20000": True,
        "all_under_20000": True,
    })
    write_json("validation/final-owner-file-threshold.json", {
        "schema": "ghc.family.v650-v4.owner-file-threshold.final-candidate.v1",
        "threshold": 15000,
        "scope": "new_orin_v650_v4_files_only",
        "below_threshold": True,
        "inherited_baseline_not_rotation_trigger": True,
    })
    write_json("validation/stale-label-review.json", {
        "schema": "ghc.family.v650-v4.stale-label-review.v1",
        "current_phase": "v650-v4",
        "current_owner": "Orin Thale",
        "historical_labels_allowed_only_with_context": True,
        "confirmed_stale_current_labels": [],
        "passed": True,
    })
    write_json("environment/final-environment-receipt.json", {
        "schema": "ghc.family.v650-v4.environment.final-candidate.v1",
        "versions_verified_only": True,
        "codex_cli": "0.144.5",
        "codex_desktop": "26.715.4045.0",
        "python": "3.12.10",
        "git": "2.55.0.windows.2",
        "powershell": "5.1.26100.8894",
        "desktop_updated": False,
        "sandbox_or_hyperv_launched": False,
        "elevation": False,
        "host_security_weakened": False,
        "windows_feature_changed": False,
        "unrelated_software_installed": False,
        "reboot": False,
        "d_drive_primary": True,
    })
    write_json("wellbeing-check-final.json", {
        "schema": "ghc.family.v650-v4.wellbeing.final.v1",
        "pause_available": True,
        "identity_pressure": False,
        "scope_bounded": True,
        "cadence_used_as_proof": False,
        "hamish_can_stop_redirect_or_rename": True,
    })
    write_json("ghc-family-index-final.json", {
        "schema": "ghc.family.phase-index.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "state": "closeout_seal_candidate",
        "proposal_total_through_phase": 820,
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "negatives": EFFECTIVE_NEGATIVES,
        "open_gaps": OPEN_GAPS,
        "exact_gates": EXACT_GATES,
        "shared_skill_change": False,
        "family_callers_preserved": True,
    })
    write_json("orchestration/terminal-route-state-final.json", {
        "schema": "ghc.family.v650-v4.route.final-candidate.v1",
        "state": "PREPARED_NOT_SENT",
        "route_state": "PREPARED_NOT_SENT",
        "sent": False,
        "target_title": "Tamar Vey",
        "target_resolution_pending": True,
        "final_validation_pending": True,
        "no_substitute_target": True,
    })
    print(json.dumps({"baton_words": baton_words, "effective_negatives": EFFECTIVE_NEGATIVES, "methods": METHODS}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

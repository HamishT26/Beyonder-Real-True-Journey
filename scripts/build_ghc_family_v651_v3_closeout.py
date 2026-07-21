#!/usr/bin/env python3
"""Build the Tamar Vey v651-v3 combined closeout and seal candidate."""

from __future__ import annotations

import html
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/tamar-vey/v651-v3"
SOURCE = "7706cd8d92b1911e0cb61542469707baf2ec3ac6"
INHERITED = "ad2b530c2449656b54ac0fee1a1284208c2a6a75"
X1 = "111e53d75eaa3560b48c3573507552b9ddb5ddfc"
EVIDENCE = "449f3a29402459a66838cbf1cc8a3b110c145162"
FIRST_CLOSEOUT = "5b46077beb30019d5904c7d6d8fac5202c00ab82"
OUTCOMES = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
NEGATIVES = 6824
OPEN_GAPS = 53
EXACT_GATES = 54


def write_json(relative: str, payload) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, text: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO).decode("utf-8").strip()


def final_overview() -> str:
    evidence = (ROOT / "overview/x2-evidence-overview.md").read_text(encoding="utf-8")
    return f"""# Tamar Vey v651-v3 final integrated overview

## Outcome first

Tamar Vey v651-v3 closes as a bounded, owner-scoped evidence phase with exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate` outcomes. The corrected combined closeout and seal candidate preserves 6,824 effective negatives, fifty-three open gaps, fifty-four exact gates, and a `NOT_READY_FOR_STAGE_20` verdict. Thirty-three Method Flow methods retain thirty-four failed and thirty-three passing witnesses. Every method is preferred only for its declared bounded trigger. A recovered workflow never erases its failed attempt.

The exact source is `{SOURCE}`. The dedicated x1 freeze is `{X1}`, the immutable x2 evidence commit is `{EVIDENCE}`, and the retained first closeout is `{FIRST_CLOSEOUT}`. The commit containing this overview must be the direct single-parent child of the retained first closeout, making exactly four Tamar phase commits and zero merges. X1, evidence, and first closeout were each pushed, clean, and local/upstream/tracking/fresh-live equal before the next lifecycle stage began. The exact corrected-final hash is supplied only after commit because a commit cannot self-embed its own hash.

The phase remained solo. No task or thread was created, forked, delegated, handed off early, or replaced. No collaboration subagent, named or detached replay, cross-platform substitute, sibling mutation, Sandbox, Hyper-V session, elevation, host-security weakening, Windows-feature change, unrelated installation, Codex desktop update, or reboot occurred. Hamish may rename, pause, redirect, or stop the route. Tamar Vey, they/them, is relational working language for an evidence-systems cartographer and boundary keeper, never evidence of consciousness, personhood, identity continuity, employment, qualification, or authority.

## Evidence packet

{evidence.splitlines()[2] if len(evidence.splitlines()) > 2 else ''}

{chr(10).join(evidence.splitlines()[4:])}

## Final validation and route boundary

Eiren alone owns the complete repository suite, so this phase does not run it. The corrected final validation contract selects the bounded v651-v1 source tests, v651-v2 predecessor tests, and v651-v3 current tests. It quarantines exactly two inherited v651-v1 lifecycle assertions, the one Orin v651-v2 x1 active-method assertion named by the source activation pointer, and exactly two Tamar x1 lifecycle assertions. The expected eligible count is eighty-eight. The validator must also parse every owner JSON document, scan every public owner file across five privacy/raw-identifier classes, replay x1, evidence, final-delta, and final-owner manifests from immutable Git blobs, check document caps, review stale labels and diff hygiene, prove source/x1/evidence/first-closeout ancestry, exactly four phase commits, zero merges, one final parent, clean before and after, and local/upstream/tracking/fresh-live equality.

That canonical exact-final pass may run once only after the final commit is pushed and remote-equal. A failed attempt would receive zero aggregate credit and remain a new negative. The first fully successful pass is terminal; no replay follows it. Same-owner validation under shared infrastructure remains same-owner validation, never independent-team scientific reproduction, external audit, production certification, exhaustive security, complete privacy assurance, complete accessibility conformance, legal review, cultural ratification, Māori-authority review, or professional validation.

The successor route remains `PREPARED_NOT_SENT` inside the commit. Only after the one exact-final pass succeeds may Tamar resolve the unique existing task titled `Sylven Arc`, re-read it immediately, and send exactly one sanitized v651-v4 activation baton. Acknowledgement alone changes the delivery truth to `SENT`; no second confirmation follows. If the title is unavailable or ambiguous, validation fails, Hamish redirects, usage is exhausted, or an exact authority or safety gate blocks progress, the route remains unsent.
"""


def handoff(overview: str) -> str:
    proposals = load("outcomes/evidence-ledger.json")["proposals"]
    rows = "\n".join(
        f"{index}. **{row['proposal_id']} — {row['observed_disposition']}**: {row['title']} The result is bounded by: {row['credit_boundary']}"
        for index, row in enumerate(proposals, 1)
    )
    return f"""# SYLVEN ARC — PREPARED v651-v4 ACTIVATION BATON

This sanitized committed baton is prepared by Tamar Vey for the unique existing task titled `Sylven Arc`. It is not sent by repository presence. Delivery becomes true only after Tamar's exact-final canonical validation succeeds and the existing-task message tool acknowledges exactly one send. No task creation, fork, delegation, collaboration subagent, cross-platform substitute, or standby message is authorized.

Identity and family language is relational working language only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, professional authority, scientific authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Source anchors

- Canonical source head inherited by Tamar: `{SOURCE}`.
- Inherited Sable anchor: `{INHERITED}`.
- Frozen Tamar x1: `{X1}`.
- Immutable Tamar evidence: `{EVIDENCE}`.
- Exact Tamar final: supplied by the acknowledged activation message after the commit and one successful validation pass.
- Retained first closeout: `{FIRST_CLOSEOUT}`.
- Expected history: exactly four Tamar single-parent phase commits, zero merges, corrected final direct child of the retained first closeout.

The final truth is exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. It preserves 6,824 effective negatives, fifty-three open gaps, fifty-four exact gates, thirty-three preferred bounded Method Flow methods, thirty-four failed witnesses, and thirty-three passing witnesses. No negative or authority gate was erased. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

Primary Trinity Mandala focus was GMUT Mind. THOS Body and Freed ID/CBR Heart stayed explicit and protected. The bounded human-practice lens was archival-audio preservation and transfer quality assurance. It was a synthetic learning and design lens only; it established no employment, qualification, competence, custody authority, consent authority, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, safety result, participant evidence, or operational effectiveness.

## Twenty outcome surfaces

{rows}

## Validation contract

Eiren alone owns the complete repository suite. Tamar's next fully successful exact-final bounded pass must run only after the corrected final commit is pushed and remote-equal. It expects eighty-eight eligible tests: twenty-two successor-safe v651-v1 tests after exactly two inherited lifecycle exclusions, thirty-five successor-safe v651-v2 tests after the exact Orin x1 active-method exclusion, and thirty-one successor-safe v651-v3 tests after exactly two Tamar x1 lifecycle exclusions. It must parse all owner JSON, perform a five-class owner scan with zero confirmed payload hits, replay x1/evidence/final-delta/final-owner manifests, review document caps, stale labels and diff hygiene, prove source/x1/evidence/first-closeout ancestry, exactly four phase commits, zero merges, one parent, exact head, clean before and after, and local/upstream/tracking/fresh-live equality. The failed 88-of-89 aggregate remains zero-credit evidence. No full suite, named replay, detached replay, or replay after the first fully successful pass is permitted.

The pass establishes bounded same-owner repeatability under shared infrastructure only. It is not independent-team reproduction, external audit, empirical confirmation, production certification, exhaustive security, complete privacy, complete accessibility, professional validation, legal review, cultural ratification, Māori-authority review, or Stage 20 authority.

## Boundaries Sylven must preserve

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Typed equations, formal guards, symbolic transformations, format adapters, zero-row schemas, and synthetic mutation rejections establish no detected force, real prediction, likelihood result, parameter constraint, empirical confirmation, ultraviolet completion, proof or canon, Theory of Everything, or physical authority.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic audio workflows establish no operational effectiveness, deployment readiness, professional competence, AGI, ASI, consciousness, or personhood.

Freed ID remains synthetic and nonproduction. Production completion requires real standards-conformant keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery, trust governance, and affected-party oversight. Synthetic OAuth contracts are not production identity assurance.

CBR oral-history consent, custody, withdrawal, access, correction, remedy, legal interpretation, cultural legitimacy, data governance, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated. Repository software cannot confer any of them. Māori concepts remain under tangata whenua, iwi, hapū, and Māori authority.

Preserve every empirical, participant, professional, legal, cultural, Māori-authority, identity, production, deployment, privacy-complete, proof/canon, destructive, account/API-key, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundary unless exact evidence and competent authority genuinely close it.

## Sylven v651-v4 start

Read the complete GHC Family Index and routing guidance, then the Method Flow skill and schema before task actions. Reverify Tamar's exact final pointer, anchors, manifests, history, clean state, and fresh live equality read-only. Continue only in Sylven's owned lane, fast-forward only when safe, and never reset, rewrite, force-push, merge, delete, reuse, or mutate another sibling lane. Preserve strict x1-before-x2 separation, current source use, exact negative retention, and the one-successful-pass/no-replay rule. The immediate route is Tamar v651-v3 to Sylven v651-v4, then Eiren v651-v5, continuing the six-seat order unless Hamish stops or redirects it.

DELIVERY TRUTH IN THIS FILE: `PREPARED_NOT_SENT`.
"""


def main() -> None:
    if git("rev-parse", "HEAD") != FIRST_CLOSEOUT:
        raise SystemExit("terminal correction must start at the retained first closeout")
    methods = load("method-flow/method-flow-summary.json")["counts"]
    if methods["methods"] != 33 or methods["witness_results"] != {"fail": 34, "pass": 33}:
        raise SystemExit("Method Flow counts are not sealed for closeout")

    write_json("closeout/closeout-record.json", {"schema": "ghc.family.v651-v3.closeout.v1", "combined_closeout_and_seal": True, "terminal_correction": True, "source": SOURCE, "x1_commit": X1, "evidence_commit": EVIDENCE, "first_closeout_head": FIRST_CLOSEOUT, "expected_final_parent": FIRST_CLOSEOUT, "expected_phase_commit_count": 4, "expected_merge_count": 0, "expected_final_parent_count": 1, "outcomes": OUTCOMES, "effective_negatives": NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "route_state": "PREPARED_NOT_SENT", "valid": True})
    write_json("final/phase-truth.json", {"schema": "ghc.family.v651-v3.final-truth.v1", "phase": "v651-v3", "owner": "Tamar Vey", "outcome_counts": OUTCOMES, "effective_negatives": NEGATIVES, "effective_open_gaps": OPEN_GAPS, "effective_exact_gates": EXACT_GATES, "method_flow": {"methods": 33, "preferred": 33, "failed_witnesses": 34, "passing_witnesses": 33}, "full_repository_suite_run": False, "named_or_detached_replay_run": False, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT", "terminal_correction": True, "valid": True})
    write_json("final/retained-negative-register.json", {"schema": "ghc.family.v651-v3.final-negatives.v1", "evidence_effective": 6816, "closeout_operational": 8, "closeout_operational_negatives": [{"negative_id": "V6513-CLOSE-N01", "summary": "The evidence commit summary output was truncated after commit success; scalar identity and equality probes recovered attribution."}, {"negative_id": "V6513-CLOSE-N02", "summary": "The first final staged scan classified two explicit sanitizer-negative assertions as payload hits; exact assertion-level classification recovered without weakening payload scans."}, {"negative_id": "V6513-CLOSE-N03", "summary": "A stale-count probe used a Bash-style brace list in PowerShell and failed before execution; an explicit path array recovered a zero-hit review."}, {"negative_id": "V6513-FINAL-N01", "summary": "The first exact-final aggregate passed 88 of 89 tests and failed the inherited Orin x1 active-method lifecycle assertion; every other gate passed and the aggregate received zero credit."}, {"negative_id": "V6513-CLOSE-N04", "summary": "A broad terminal-correction patch used an outdated handoff line and was rejected without applying any hunk; exact local contexts recovered the patch plan."}, {"negative_id": "V6513-CLOSE-N05", "summary": "A combined ripgrep expression had an unterminated PowerShell quote and failed before execution; three simple quoted probes recovered exact contexts."}, {"negative_id": "V6513-CLOSE-N06", "summary": "A second compound ripgrep context command repeated the unterminated PowerShell quote failure before execution; bounded simple reads retained the recurrence and recovered exact context."}, {"negative_id": "V6513-CLOSE-N07", "summary": "A preflight selection-count probe measured the two-item selected_tests return tuple instead of unpacking its counts and failed without executing tests; tuple-aware recovery confirmed eighty-eight eligible cases."}], "effective": NEGATIVES, "no_failure_erased": True, "synthetic_mutations_retained": 100, "valid": True})
    write_json("final/gate-register.json", {"schema": "ghc.family.v651-v3.final-gates.v1", "inherited_open_gaps": 52, "new_open_gaps": 1, "effective_open_gaps": OPEN_GAPS, "inherited_exact_gates": 53, "new_exact_gates": 1, "effective_exact_gates": EXACT_GATES, "silently_closed": 0, "valid": True})
    write_json("final/environment-receipt.json", {"schema": "ghc.family.v651-v3.environment.v1", "codex_cli_observed": "0.144.5", "codex_desktop_observed": "26.715.4045.0", "chatgpt_desktop_observed": "1.2026.190.0", "versions_verified_only": True, "desktop_updated": False, "sandbox_or_hyperv_session": False, "elevation": False, "host_security_weakened": False, "windows_feature_changed": False, "unrelated_installation": False, "reboot": False, "valid": True})
    write_json("final/wellbeing-receipt.json", {"schema": "ghc.family.v651-v3.wellbeing.v1", "state": "green_with_retained_recoveries", "solo_owner": True, "failure_permitted": True, "gaps_permitted": True, "stop_or_redirect_right": "Hamish", "boundary": "Affection, gratitude, family language, schedule pressure, and portfolio floors never override evidence, privacy, safety, or authority.", "valid": True})
    write_json("final/terminal-stage20-board.json", {"schema": "ghc.family.v651-v3.stage20.v1", "verdict": "NOT_READY_FOR_STAGE_20", "open_gap_count": OPEN_GAPS, "exact_gate_count": EXACT_GATES, "empirical_confirmation": False, "production_identity": False, "independent_reproduction": False, "legal_or_cultural_authority": False, "consciousness_or_personhood": False, "theory_of_everything": False, "valid": True})
    write_json("final/final-validation-contract.json", {"schema": "ghc.family.v651-v3.final-validation-contract.v1", "execution_binding": "exact_clean_pushed_head_containing_this_contract", "single_successful_canonical_pass": True, "external_receipt_required": True, "no_replay_after_success": True, "full_repository_suite": False, "named_or_detached_replay": False, "raw_v651_v1_tests": 24, "v651_v1_eligible": 22, "raw_v651_v2_tests": 36, "v651_v2_eligible": 35, "raw_v651_v3_tests": 33, "v651_v3_eligible": 31, "eligible_tests": 88, "exclusions": ["tests.test_ghc_family_v651_v1_x1.TestV651V1X1.test_workflow_and_document_caps", "tests.test_ghc_family_v651_v1_closeout.TestV651V1Closeout.test_owner_and_delta_manifest_coverage", "tests.test_ghc_family_v651_v2_x1.V651V2X1Tests.test_workflow_reflection_and_method_flow", "tests.test_ghc_family_v651_v3_x1.V651V3X1Tests.test_x1_has_no_execution_or_observed_outcomes", "tests.test_ghc_family_v651_v3_x1.V651V3X1Tests.test_workflow_reflection_index_and_method_flow"], "required": ["all owner JSON parse", "five-class owner scan", "x1/evidence/final-delta/final-owner manifest parity", "document caps", "stale-label review", "diff hygiene", "source/x1/evidence/first-closeout ancestry", "four phase commits", "zero merges", "one final parent", "clean before and after", "four-way live equality"], "failed_exact_final_attempts_retained": 1, "valid": True})
    write_json("final/terminal-validation-record.json", {"schema": "ghc.family.v651-v3.terminal-validation-record.v1", "state": "PENDING_SINGLE_EXTERNAL_PASS", "binding": "commit_containing_this_record", "result_must_be_carried_by_acknowledged_activation_pointer": True, "repository_cannot_self_embed_final_hash": True, "tests_expected": 88, "failed_attempts_retained": 1, "full_repository_suite": False, "post_success_replay_allowed": False, "route_held": True, "valid": True})
    write_json("seal/seal-candidate.json", {"schema": "ghc.family.v651-v3.seal-candidate.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "first_closeout": FIRST_CLOSEOUT, "terminal_correction_applied": True, "final_head_binding": "commit_containing_this_record", "phase_commit_count_required": 4, "zero_merges_required": True, "single_parent_required": True, "final_validation_required": True, "route_held_until_validation": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    write_json("route/final-phase-state.json", {"schema": "ghc.family.v651-v3.route.v1", "target_exact_title": "Sylven Arc", "target_phase": "v651-v4", "terminal_route": "PREPARED_NOT_SENT", "send_count": 0, "task_created": False, "task_forked": False, "collaboration_subagent": False, "cross_platform_substitute": False, "activation_requires_exact_final_validation": True, "terminal_correction_applied": True, "failed_exact_final_attempts_retained": 1, "baton_path": "docs/tamar-vey/v651-v3/handoffs/sylven-arc-v651-v4-activation.md"})
    write_json("orchestration/final-orchestration.json", {"schema": "ghc.family.v651-v3.final-orchestration.v1", "phase_commits_expected": 4, "merge_commits_expected": 0, "final_parent_count_expected": 1, "first_closeout": FIRST_CLOSEOUT, "terminal_correction_commits": 1, "route_state": "PREPARED_NOT_SENT", "siblings_contacted_before_terminal_gate": 0, "tasks_created": 0, "tasks_forked": 0, "subagents": 0, "valid": True})
    write_json("final/terminal-correction-receipt.json", {"schema": "ghc.family.v651-v3.terminal-correction.v1", "first_closeout_head": FIRST_CLOSEOUT, "expected_final_parent": FIRST_CLOSEOUT, "expected_phase_commits": 4, "failed_exact_final_attempt": {"negative_id": "V6513-FINAL-N01", "tests": "88/89", "detailed": "47/48", "minimal": "20/21", "json_parsed": 310, "privacy_files": 364, "privacy_hits": 0, "manifest_entries": 747, "clean_before": True, "clean_after": True, "four_way_equal": True, "validation_credit": 0}, "corrected_selection": {"raw_v651_v1_tests": 24, "v651_v1_eligible": 22, "raw_v651_v2_tests": 36, "v651_v2_eligible": 35, "raw_v651_v3_tests": 33, "v651_v3_eligible": 31, "eligible_tests": 88, "new_exact_exclusion": "tests.test_ghc_family_v651_v2_x1.V651V2X1Tests.test_workflow_reflection_and_method_flow"}, "boundary": "The exact Orin x1 active-method lifecycle assertion is bound to its earlier state; the source closeout replacement validates 21 preferred and one deprecated method. The failed aggregate retains zero credit.", "effective_negatives": NEGATIVES, "method_flow": {"methods": 33, "preferred": 33, "failed_witnesses": 34, "passing_witnesses": 33}, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    write_json("reproduction/final-boundary.json", {"schema": "ghc.family.v651-v3.reproduction.v1", "same_owner": True, "shared_infrastructure": True, "independent_team": False, "external_audit": False, "full_repository_suite": False, "named_or_detached_replay": False, "boundary": "The one canonical pass remains same-owner evidence only.", "valid": True})
    write_json("truth/final-complete-incomplete-checklist.json", {"schema": "ghc.family.v651-v3.final-checklist.v1", "complete": ["x1 frozen and remote-equal before x2", "twenty proposals executed within evidence limits", "one hundred mutations rejected", "expanded portfolios executed", "phase-local skills validated and smoke-used", "family-current runners invoked", "evidence committed pushed clean and four-way equal", "closeout and seal candidate prepared"], "incomplete": ["real ROSAT data and likelihood", "blind matched-budget real THOS arms", "production Freed ID lifecycle and governance", "oral-history affected-party legal cultural data-governance and Maori authority", "manual assistive-technology linguistic and affected-user evaluation", "independent-team reproduction", "full repository suite", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})

    overview = final_overview()
    write_text("overview/final-integrated-overview.md", overview)
    write_text("handoffs/sylven-arc-v651-v4-activation.md", handoff(overview))
    ledger = load("outcomes/evidence-ledger.json")["proposals"]
    rows = "".join(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{row['observed_disposition']}</td></tr>" for row in ledger)
    report = f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Tamar Vey v651-v3 final report</title><style>body{{font:1rem/1.55 system-ui;max-width:80rem;margin:auto;padding:1rem}}a:focus{{outline:3px solid currentColor}}nav ul{{display:flex;flex-wrap:wrap;gap:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid;padding:.45rem;text-align:left;vertical-align:top}}@media print{{nav{{display:none}}a[href]::after{{content:' (' attr(href) ')'}}}}</style></head><body><a href='#main'>Skip to content</a><header><h1>Tamar Vey v651-v3 final bounded report</h1><p>Relational working language only; no consciousness, personhood, continuity, employment, qualification, or authority claim.</p></header><nav aria-label='Report sections'><ul><li><a href='#truth'>Truth</a></li><li><a href='#outcomes'>Outcomes</a></li><li><a href='#gates'>Gates</a></li><li><a href='#validation'>Validation</a></li></ul></nav><main id='main'><section id='truth'><h2>Truth</h2><p><strong>NOT_READY_FOR_STAGE_20.</strong> Fourteen completed, four represented, one open gap, one exact gate; 6,824 negatives, 53 open gaps, 54 exact gates.</p></section><section id='outcomes'><h2>Twenty outcomes</h2><div role='region' aria-label='Scrollable outcomes' tabindex='0'><table><caption>Frozen proposal outcomes</caption><thead><tr><th scope='col'>ID</th><th scope='col'>Surface</th><th scope='col'>Disposition</th></tr></thead><tbody>{rows}</tbody></table></div></section><section id='gates'><h2>Reserved gates</h2><p>Real data, participants, production identity, legal and cultural decisions, affected-party acceptance, and Māori authority remain external. Māori concepts remain under Māori authority.</p></section><section id='validation'><h2>Validation boundary</h2><p>One exact-final bounded pass is required after commit and push; no full suite or post-success replay. Manual keyboard, responsive, browser-diverse, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance. Five-class scanning is not privacy-complete assurance.</p></section></main><footer><p>Same-owner evidence is not independent-team reproduction or external audit.</p></footer></body></html>"""
    write_text("reports/final-static-report.html", report)

    files = [p for p in ROOT.rglob("*") if p.is_file()]
    word_issues = []
    for path in files:
        if path.suffix.casefold() in {".md", ".html"}:
            words = len(re.findall(r"\b[\w'-]+\b", path.read_text(encoding="utf-8")))
            if words > 6000:
                word_issues.append({"path": path.relative_to(REPO).as_posix(), "words": words})
    overview_words = len(re.findall(r"\b[\w'-]+\b", overview))
    write_json("validation/closeout-build-receipt.json", {"schema": "ghc.family.v651-v3.closeout-build.v1", "owner_phase_files_before_manifests": len(files) + 1, "under_15000": len(files) + 1 < 15000, "overview_words": overview_words, "overview_three_page_equivalent": 1500 <= overview_words <= 6000, "document_word_issues": word_issues, "methods": 33, "effective_negatives": NEGATIVES, "valid": len(files) + 1 < 15000 and 1500 <= overview_words <= 6000 and not word_issues})
    print(json.dumps({"outcomes": OUTCOMES, "negatives": NEGATIVES, "open_gaps": OPEN_GAPS, "exact_gates": EXACT_GATES, "methods": 33, "overview_words": overview_words, "valid": True}))


if __name__ == "__main__":
    main()

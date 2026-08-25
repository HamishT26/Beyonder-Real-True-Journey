from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from ghc_family_elowen_cairn_v669_v2_archive import (
    BRANCH,
    DOCUMENT_WORD_CEILING,
    FINAL_FAILURES,
    FINAL_OVERLAY,
    FROZEN_EVIDENCE,
    FROZEN_X1,
    IDENTITY_BOUNDARY,
    OWNER,
    PHASE,
    PRACTICE,
    PRIMARY_PILLAR,
    PRONOUNS,
    RELATIONAL_HOPE,
    RELATIONAL_ROLE,
    REL_PHASE_ROOT,
    ROOT,
    SOURCE_FINAL,
    SOURCE_OVERLAY,
    SOURCE_START,
    TERMINAL_VERDICT,
    X2_FAILURES,
    canonical_json_bytes,
    git,
    manifest_rows,
    phase_owner_files,
    run_git,
    sha256_bytes,
    utc_now,
    word_count,
)


PHASE_ROOT = ROOT / REL_PHASE_ROOT
FINAL_OWNER_MANIFEST = (REL_PHASE_ROOT / "validation/final-owner-manifest.json").as_posix()
FINAL_DELTA_MANIFEST = (REL_PHASE_ROOT / "validation/final-delta-manifest.json").as_posix()
FINAL_ALLOWLIST = (REL_PHASE_ROOT / "validation/final-staged-allowlist.json").as_posix()
FINAL_STAGED_REVIEW = (REL_PHASE_ROOT / "validation/final-staged-review.json").as_posix()
FINAL_STAGED_FAILED = (REL_PHASE_ROOT / "validation/final-staged-review-failed.json").as_posix()
CONTENT_SEAL = (REL_PHASE_ROOT / "seal/content-seal.json").as_posix()
CLOSEOUT_RECEIPT = (REL_PHASE_ROOT / "closeout/closeout-receipt.json").as_posix()


def write_json(relative: str | Path, value: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_text(relative: str | Path, value: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")
    return path


def assert_final_start() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong Elowen owner branch")
    if git("rev-parse", "HEAD") != FROZEN_EVIDENCE:
        raise RuntimeError("final closeout must begin at immutable evidence")
    if git("rev-parse", f"{FROZEN_EVIDENCE}^") != FROZEN_X1:
        raise RuntimeError("evidence parent is not immutable x1")
    if run_git("diff", "--cached", "--quiet", check=False).returncode != 0:
        raise RuntimeError("final builder requires an empty index")


def append_final_method() -> dict[str, Any]:
    evidence = json.loads((PHASE_ROOT / "method-flow/evidence-ledger.json").read_text(encoding="utf-8"))
    methods = list(evidence["methods"])
    witnesses = list(evidence["witnesses"])
    events = list(evidence["state_events"])
    for index, row in enumerate(FINAL_FAILURES, 1):
        failure_id, signature, workaround, guard = row
        method_id = f"EC6692-METHOD-FINAL-{index:03d}"
        failed_id = f"EC6692-WITNESS-FINAL-{index:03d}-F"
        passed_id = f"EC6692-WITNESS-FINAL-{index:03d}-P"
        methods.append(
            {
                "approval_class": "safe_now",
                "failed_witness_ids": [failed_id],
                "failure_id": failure_id,
                "failure_signature": signature,
                "method_id": method_id,
                "owner": OWNER,
                "phase": PHASE,
                "protected_gates": ["immutable_evidence", "no_failure_erasure", "exact_narrative_counts"],
                "recurrence_guard": guard,
                "result": "additive_final_correction",
                "rollback": "leave immutable evidence unchanged and remove only the additive final candidate if validation fails",
                "stage": "final",
                "validation_witness_ids": [passed_id],
                "workaround": workaround,
            }
        )
        witnesses.extend(
            [
                {"completion_credit": 0, "method_id": method_id, "result": "fail", "signature": signature, "witness_id": failed_id},
                {"bounded_scope": workaround, "method_id": method_id, "result": "pass", "witness_id": passed_id},
            ]
        )
        for state in ("stale_narrative_observed", "evidence_left_immutable", "additive_correction", "recurrence_guarded"):
            events.append({"method_id": method_id, "ordinal": len(events) + 1, "state": state})
    return {
        "append_only": True,
        "effective_method_count": FINAL_OVERLAY["methods"],
        "methods": methods,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.method-flow-ledger.v5",
        "source_sealed_method_count": SOURCE_OVERLAY["methods"],
        "state_events": events,
        "witnesses": witnesses,
    }


def final_overview() -> str:
    evidence_text = (PHASE_ROOT / "x2/integrated-evidence-overview.md").read_text(encoding="utf-8")
    closeout = f"""
## Final lifecycle and exact truth

The dedicated planning-only x1 is `{FROZEN_X1}` and the immutable evidence commit is `{FROZEN_EVIDENCE}`. Both are direct single-parent descendants of Tamar's immutable final `{SOURCE_FINAL}`, which descends from source `{SOURCE_START}`. The final candidate will be one direct child of evidence, yielding exactly three Elowen phase commits and zero merges. The x1 commit was pushed, clean, 0/0 divergent, and fresh-live four-way equal before x2. The evidence commit reached the same gate before final closeout began. No reset, amendment, force-push, merge, branch reuse, sibling mutation, task creation, collaboration subagent, standby contact, or successor precontact occurred.

Final effective truth is {FINAL_OVERLAY['effective_negatives']} negatives, {FINAL_OVERLAY['methods']} Method Flow methods, {FINAL_OVERLAY['failed_witnesses']} retained failed witnesses, {FINAL_OVERLAY['passing_witnesses']} bounded passing witnesses, {FINAL_OVERLAY['open_gaps']} open gaps, and {FINAL_OVERLAY['exact_gates']} exact gates. The proposal outcomes remain exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. The extra final failure corrects only one stale narrative count in the evidence composite: its structured fields correctly retained 30 of 31 passed aggregate checks, while one sentence said 29. The immutable evidence receipt is not rewritten. This final layer retains the discrepancy, supplies the corrected wording, and adds one failed/passing Method Flow pair.

## Validation interpretation

The x1 owner module passed 16/16 once. The first x1 validator failed before receipt emission on a missing standard-library import, then its dependency-corrected invocation passed 25/25 checks. The x2 aggregate retained zero aggregate-pass credit after 22 of 24 tests passed and two collection-type assertions failed; only those two dependencies were corrected and passed. The evidence validator retained zero all-pass credit after 30 of 31 checks passed. Two isolated recovery attempts remained failed at zero credit before the third produced a valid dependency-corrected composite. No successful stage check was replayed afterward. The exact-final canonical aggregate remains pending until the final commit is pushed, clean, zero-divergent, and fresh-live equal. It will run one final-owner module and exact-final checks, not the full repository suite.

## Accessible report and evaluation reservations

The static report uses a skip link, semantic header, navigation, main and footer landmarks, ordered headings, captioned tables, scoped headers, text-redundant outcomes, visible focus styling, responsive horizontal containment, high-contrast system colors, and print fallback. These are structural implementation checks only. Manual keyboard, touch, zoom, reflow, browser-diverse, assistive-technology, screen-reader, cognitive, Māori-language, security-usability, print, luthier, musician, conservator, owner, custodian, affected-user, and affected-party evaluations remain reserved and unperformed. Accessibility is therefore not complete and no professional, cultural, or affected-party acceptance is claimed.

## Prepared route and stop rules

The repository route remains `PREPARED_NOT_SENT`. Under the current live cycle, the provisional exact-title successor is Sylven Arc for v669-v3, but this closeout artifact is not delivery authority by itself. Only after exact-final canonical success and a fresh clean remote-equality gate may Elowen reread current live authorization, list the bounded task registry, resolve exactly one existing task titled `Sylven Arc`, reread it immediately, apply a duplicate guard, and send exactly once. Missing, ambiguous, renamed, paused, redirected, duplicate, standby, usage-exhausted, privacy-blocked, or authority-blocked state requires stopping without a substitute or resend.

## Final boundary

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no real likelihood, parameter constraint, force, prediction, material law, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon. THOS remains a zero-participant proxy without governed blind matched-budget real arms, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction without standards-conformant keys and proofs, live lifecycle events, interoperability, privacy and independent security review, recovery evidence, or trust governance. CBR, professional decisions, safety, remedy, legal or cultural interpretation, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. The terminal verdict remains `{TERMINAL_VERDICT}`.
"""
    return evidence_text.rstrip() + "\n\n" + closeout.strip() + "\n"


def static_report(truth: dict[str, Any]) -> str:
    outcome_rows = "".join(
        f"<tr><th scope='row'>{html.escape(label)}</th><td>{count}</td><td>{html.escape({'completed':'bounded synthetic evidence','represented':'typed or protocol surface only','open_gap':'dependency absent','exact_gate':'authority or evidence lock held'}[label])}</td></tr>"
        for label, count in truth["core_outcomes"].items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{OWNER} {PHASE} bounded closeout report</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.55; }}
body {{ margin: 0 auto; max-width: 72rem; padding: 1rem; }}
.skip {{ position: absolute; left: -9999px; }} .skip:focus {{ left: 1rem; top: 1rem; background: Canvas; color: CanvasText; padding: .75rem; outline: .2rem solid Highlight; }}
a:focus, button:focus {{ outline: .2rem solid Highlight; outline-offset: .15rem; }}
nav ul {{ display: flex; flex-wrap: wrap; gap: 1rem; padding-left: 1.25rem; }}
.table-wrap {{ overflow-x: auto; }} table {{ border-collapse: collapse; width: 100%; }} th, td {{ border: 1px solid CanvasText; padding: .55rem; text-align: left; vertical-align: top; }}
.status {{ border-left: .4rem solid Highlight; padding: .75rem 1rem; background: color-mix(in srgb, Canvas 85%, Highlight 15%); }}
@media (max-width: 42rem) {{ nav ul {{ display: block; }} th, td {{ padding: .4rem; }} }}
@media print {{ .skip, nav {{ display: none; }} body {{ max-width: none; color: #000; background: #fff; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header><h1>{OWNER} {PHASE} bounded closeout report</h1><p class="status"><strong>Terminal verdict:</strong> {TERMINAL_VERDICT}. This is same-owner synthetic evidence, not independent reproduction or authority.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#retention">Retention</a></li><li><a href="#reservations">Reserved evaluation</a></li></ul></nav>
<main id="main">
<section id="scope"><h2>Scope and identity boundary</h2><p>{html.escape(OWNER)} ({html.escape(PRONOUNS)}) is relational working language for a {html.escape(RELATIONAL_ROLE)}, with the hope {html.escape(RELATIONAL_HOPE)}. {html.escape(IDENTITY_BOUNDARY)}</p><p>The primary pillar is {html.escape(PRIMARY_PILLAR)} and the bounded learning lens is {html.escape(PRACTICE)}. The phase uses zero real people, instruments, materials, measurements, treatments, repairs, keys, proofs, or authority acts.</p></section>
<section id="outcomes"><h2>Core outcomes</h2><div class="table-wrap" tabindex="0" aria-label="Scrollable outcomes table"><table><caption>Forty preregistered proposal outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody>{outcome_rows}</tbody></table></div></section>
<section id="retention"><h2>Retained truth</h2><ul><li>{truth['effective_negatives']} effective negatives</li><li>{truth['methods']} Method Flow methods</li><li>{truth['failed_witnesses']} retained failed witnesses</li><li>{truth['passing_witnesses']} bounded passing witnesses</li><li>{truth['open_gaps']} open gaps</li><li>{truth['exact_gates']} exact gates</li></ul><p>All 160 invalid mutations remain rejected at zero completion credit. Operational recoveries never erase their failed witnesses.</p></section>
<section id="reservations"><h2>Reserved manual and authority evaluation</h2><p>Manual keyboard, touch, zoom, browser, assistive-technology, cognitive, Māori-language, security-usability, print, professional, affected-user, and affected-party evaluation remain unperformed. Legal, cultural, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.</p></section>
</main>
<footer><p>Prepared closeout artifact. Route state remains PREPARED_NOT_SENT until exact-final canonical and fresh-live gates pass.</p></footer>
</body>
</html>"""


def baton_text() -> str:
    return f"""# SYLVEN ARC — PREPARED ELOWEN v669-v2 → PROVISIONAL v669-v3 ACTIVATION CANDIDATE

PREPARED_NOT_SENT = true. SENT_BY_ELOWEN_CAIRN = false.

This repository file is a sanitized candidate only. It is not a live send, acknowledgement, task creation, delegation, successor contact, or authority to bypass the final terminal gate.

Relational names, pronouns, roles, hopes, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala language are working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Source candidate

- Owner: {OWNER}
- Phase: {PHASE}
- Branch: `{BRANCH}`
- Tamar source/final: `{SOURCE_FINAL}`
- Frozen Elowen x1: `{FROZEN_X1}`
- Immutable Elowen evidence: `{FROZEN_EVIDENCE}`
- Exact Elowen final: `TO_BE_BOUND_BY_ACKNOWLEDGED_LIVE_SEND_AFTER_CANONICAL_GATE`
- Core outcomes: 28 `completed`, 8 `represented`, 2 `open_gap`, 2 `exact_gate`
- Final retained truth candidate: {FINAL_OVERLAY['effective_negatives']} negatives, {FINAL_OVERLAY['methods']} methods, {FINAL_OVERLAY['failed_witnesses']} failed witnesses, {FINAL_OVERLAY['passing_witnesses']} bounded passing witnesses, {FINAL_OVERLAY['open_gaps']} open gaps, {FINAL_OVERLAY['exact_gates']} exact gates
- Terminal verdict: `{TERMINAL_VERDICT}`

## Bounded domain

Elowen's primary pillar was GMUT Mind through a wholly synthetic lutherie and stringed-instrument documentation lens. Forty distinct contracts covered component identity and topology, plate and internal-structure vacancies, strings, bridge relations, tuning-state refusal, finish and material claim vacancies, typed dimensions, condition cues, action holds, tools, corrections, custody, provenance, canonical domains, pseudonyms, accessibility structures, issue escrow, source firewalls, CBR challenge, Freed ID vacancy, THOS dependency, GMUT obligation boards, hazard holds, workload, nonconversion, zero-call adapters, human-evaluation gaps, authority gates, and Stage 20 nonpromotion.

The phase used zero real people, participants, luthiers, musicians, owners, custodians, instruments, components, materials, workshops, observations, measurements, treatments, repairs, tuning actions, keys, proofs, live identity events, professional decisions, legal or cultural decisions, affected-party approvals, or authority acts. The Library of Congress adapter made zero calls and ingested zero rows.

GMUT remains a typed scalar-tensor/EFT research-model family with no empirical fit, constraint, force, prediction, physical confirmation, final physics, or Theory-of-Everything proof. THOS remains a participant-free proxy without governed real arms or effectiveness evidence. Freed ID remains synthetic and nonproduction without real keys, proofs, lifecycle, interoperability, security review, recovery, or trust governance. CBR, professional decisions, safety, law, culture, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

## Validation candidate

X1 passed 16 owner tests once and a dependency-corrected 25-check staged validator. X2 retains a failed 24-test aggregate with 22 passed components and two corrected isolated dependencies. Evidence validation retains a failed 31-check aggregate with 30 passed components, two failed isolated recoveries, and a valid third dependency-corrected composite. The full repository suite was not run. Exact-final canonical validation remains external and one-shot after the final commit is pushed and four-way equal. Same-owner evidence is not independent reproduction, audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.

## Provisional successor lane

If and only if Hamish's live route still assigns the next terminal edge to the unique existing task titled exactly `Sylven Arc`, the live sender must freshly list the bounded registry, resolve exactly one title match, reread it immediately, check for a duplicate activation, and send exactly once after final canonical success and clean fresh-live equality. The live message must bind the actual exact final head and external canonical receipt digest; this candidate deliberately cannot do so before those facts exist.

Sylven must work solo in a fresh additive D-first owner lane from the exact Elowen final, preserve strict x1-before-x2 separation, audit novelty against the inherited chain, retain every negative, gap, gate, and recovery, use only the four outcome labels, keep exact and blocked work held without authority, avoid the full repository suite unless explicitly reassigned, and preserve all scientific, professional, privacy, accessibility, legal, cultural, affected-party, and Māori-authority boundaries.

Stop without send or substitution on ambiguity, missing task, rename, pause, redirect, standby status, duplicate activation, usage exhaustion, missing acknowledgement, dirty or divergent final, canonical failure, privacy risk, or any evidence or authority gate.
"""


def is_changed_from_evidence(path: Path) -> bool:
    relative = path.relative_to(ROOT).as_posix()
    if run_git("cat-file", "-e", f"{FROZEN_EVIDENCE}:{relative}", check=False).returncode != 0:
        return True
    old = run_git("show", f"{FROZEN_EVIDENCE}:{relative}", text=False).stdout
    oid = git("hash-object", "-w", "--path", relative, relative)
    current = run_git("cat-file", "blob", oid, text=False).stdout
    return old != current


def main() -> None:
    assert_final_start()
    now = utc_now()
    evidence_truth = json.loads((PHASE_ROOT / "x2/phase-truth-evidence.json").read_text(encoding="utf-8"))
    outcomes = evidence_truth["core_outcomes"]
    if outcomes != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise RuntimeError("evidence outcome drift")
    method_flow = append_final_method()
    if len(method_flow["methods"]) != FINAL_OVERLAY["methods"] - SOURCE_OVERLAY["methods"]:
        raise RuntimeError("final Method Flow count drift")
    write_json(REL_PHASE_ROOT / "closeout/method-flow-ledger.json", method_flow)
    write_json(
        REL_PHASE_ROOT / "closeout/method-flow-summary.json",
        {
            **FINAL_OVERLAY,
            "new_final_failures": len(FINAL_FAILURES),
            "new_phase_methods": len(method_flow["methods"]),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.method-flow-summary.v5",
            "source_sealed_methods": SOURCE_OVERLAY["methods"],
        },
    )
    truth = {
        **FINAL_OVERLAY,
        "core_outcomes": outcomes,
        "exact_final": "TO_BE_BOUND_EXTERNALLY_AFTER_COMMIT",
        "frozen_evidence": FROZEN_EVIDENCE,
        "frozen_x1": FROZEN_X1,
        "owner": OWNER,
        "phase": PHASE,
        "phase_commit_ceiling": 3,
        "schema": "ghc.family.final-phase-truth.v3",
        "source_final": SOURCE_FINAL,
        "status": "EXACT_FINAL_CANDIDATE",
        "terminal_verdict": TERMINAL_VERDICT,
    }
    write_json(REL_PHASE_ROOT / "closeout/phase-truth.json", truth)
    write_json(
        REL_PHASE_ROOT / "closeout/retained-negative-register.json",
        {
            "evidence_register": "docs/elowen-cairn/v669-v2/x2/retained-negative-register.json",
            "effective_negatives": FINAL_OVERLAY["effective_negatives"],
            "final_failures": [
                {"failure_id": row[0], "signature": row[1], "workaround": row[2], "recurrence_guard": row[3]} for row in FINAL_FAILURES
            ],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.retained-negative-register.v3",
        },
    )
    write_json(
        REL_PHASE_ROOT / "closeout/open-exact-gate-register.json",
        {
            "effective_exact_gates": FINAL_OVERLAY["exact_gates"],
            "effective_open_gaps": FINAL_OVERLAY["open_gaps"],
            "new_exact_gates": ["EC6692-N039", "EC6692-N040"],
            "new_open_gaps": ["EC6692-N037", "EC6692-N038"],
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.open-exact-gate-register.v3",
        },
    )
    write_json(
        REL_PHASE_ROOT / "closeout/lifecycle-replay.json",
        {
            "expected_final_parent": FROZEN_EVIDENCE,
            "frozen_evidence": FROZEN_EVIDENCE,
            "frozen_x1": FROZEN_X1,
            "owner": OWNER,
            "phase": PHASE,
            "planned_phase_commits": 3,
            "schema": "ghc.family.lifecycle-replay.v3",
            "source_final": SOURCE_FINAL,
            "source_to_evidence_commits": 2,
            "source_to_final_commits_after_commit": 3,
            "strict_x1_before_x2": True,
            "zero_merges_expected": True,
        },
    )
    write_json(
        REL_PHASE_ROOT / "closeout/complete-incomplete-checklist.json",
        {
            "completed": [
                "forty distinct proposals frozen",
                "forty bounded positive controls materialized",
                "160 rejecting mutations retained",
                "exact x1 and evidence lifecycle gates",
                "twenty owner-local skills and ten family runners smoke-used",
                "all owner portfolios executed or held as evidence permits",
                "retained-negative and Method Flow ledgers",
                "structurally accessible static report",
                "final manifests, content seal, and route candidate prepared",
            ],
            "exact_gate": ["professional and safety decisions", "legal cultural affected-party and Māori authority", "Stage 20 promotion"],
            "open_gap": ["zero-call LoC adapter", "real professional affected-user and accessibility evaluation"],
            "owner": OWNER,
            "phase": PHASE,
            "represented": ["typed GMUT obligations", "THOS proxy protocol", "Freed ID and CBR synthetic surfaces", "structural accessibility"],
            "schema": "ghc.family.complete-incomplete-checklist.v3",
        },
    )
    write_json(
        REL_PHASE_ROOT / "closeout/source-provenance-ledger.json",
        {
            "evidence_sources": "docs/elowen-cairn/v669-v2/x1/source-ledger.json",
            "inherited_completion_credit": 0,
            "network_calls_during_x2_or_closeout": 0,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.source-provenance-ledger.v3",
            "source_final": SOURCE_FINAL,
            "source_status": "immutable_inherited_evidence_only",
        },
    )
    write_json(
        REL_PHASE_ROOT / "closeout/wellbeing-workload-check.json",
        {
            "context_pressure": "managed_by_exact_lifecycle_and_sharded_evidence",
            "external_coordination": 0,
            "health_measurement_claim": False,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.wellbeing-workload.v3",
            "status": "CLOSEOUT_READY_WITH_STOP_RULES",
            "stop_conditions": ["usage_exhaustion", "route_ambiguity", "privacy_or_authority_gate", "canonical_failure", "remote_divergence"],
        },
    )
    write_json(
        REL_PHASE_ROOT / "closeout/threat-model-final.json",
        {
            "controls": ["synthetic_only", "zero_external_action", "five_class_scan", "exact_manifests", "authority_vacancy", "single_send_route"],
            "owner": OWNER,
            "phase": PHASE,
            "reserved": ["exhaustive_security", "complete_privacy", "professional_review", "affected_party_review", "Māori_authority"],
            "schema": "ghc.family.threat-model.v3",
            "threats": ["claim_promotion", "private_material_leakage", "manifest_drift", "route_duplication", "authority_substitution"],
        },
    )
    overview_path = write_text(REL_PHASE_ROOT / "closeout/final-integrated-overview.md", final_overview())
    if not 1800 <= word_count(overview_path) <= DOCUMENT_WORD_CEILING:
        raise RuntimeError("final overview word bounds failed")
    write_text(REL_PHASE_ROOT / "closeout/static-report.html", static_report(truth))
    write_text(REL_PHASE_ROOT / "handoffs/sylven-arc-v669-v3-activation-candidate.md", baton_text())
    write_json(
        REL_PHASE_ROOT / "closeout/route-state-final-candidate.json",
        {
            "delivery_state": "PREPARED_NOT_SENT",
            "duplicate_guard_required": True,
            "exact_target_title": "Sylven Arc",
            "next_phase": "v669-v3",
            "owner": OWNER,
            "phase": PHASE,
            "route_authority_requires_fresh_live_reread": True,
            "schema": "ghc.family.route-state.v4",
            "sent_by_elowen_cairn": False,
            "stop_on_ambiguity": True,
        },
    )
    write_json(
        REL_PHASE_ROOT / "validation/stale-label-review.json",
        {
            "corrected_final_labels": ["30 of 31 evidence aggregate checks passed", "Elowen v669-v2", "Sylven Arc v669-v3 provisional"],
            "historical_labels_retained": ["PREPARED_NOT_SENT x1 route", "failed evidence validator", "failed recovery attempts one and two"],
            "known_stale_narrative": "evidence composite boundary said 29 while structured count fields said 30; retained as EC6692-FINAL-F034",
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.stale-label-review.v3",
            "status": "PASS_WITH_ADDITIVE_CORRECTION",
        },
    )
    write_json(
        REL_PHASE_ROOT / "validation/canonical-protocol.json",
        {
            "canonical_invocation_count_before_final": 0,
            "complete_repository_suite": False,
            "dependency_scope": ["one exact-final owner test module", "exact JSON and document checks", "five-class scan", "changed-code AST review", "Git-blob manifests", "ancestry and four-way equality"],
            "external_receipt_required": True,
            "owner": OWNER,
            "phase": PHASE,
            "post_success_replay_forbidden": True,
            "schema": "ghc.family.canonical-protocol.v3",
            "status": "PENDING_EXACT_FINAL_COMMIT_PUSH_EQUALITY",
        },
    )
    write_json(
        FINAL_STAGED_FAILED,
        {
            "all_passed": False,
            "checks_passed": 18,
            "checks_total": 19,
            "failed_component": "content_seal",
            "failure_id": "EC6692-FINAL-F035",
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.final-staged-review-failed.v3",
            "status": "FAIL_FINAL_STAGED_REVIEW_ZERO_CREDIT",
            "successful_components_replayed": False,
        },
    )
    write_json(
        FINAL_STAGED_REVIEW,
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.final-staged-review.v3",
            "status": "PREPARED_FOR_EXACT_STAGED_REVIEW_AND_FINAL_COMMIT",
        },
    )

    initial_paths = phase_owner_files()
    initial_delta = [path for path in initial_paths if is_changed_from_evidence(path)]
    intended = sorted(
        set(
            [path.relative_to(ROOT).as_posix() for path in initial_delta]
            + [FINAL_OWNER_MANIFEST, FINAL_DELTA_MANIFEST, FINAL_ALLOWLIST, FINAL_STAGED_REVIEW, CONTENT_SEAL, CLOSEOUT_RECEIPT]
        )
    )
    write_json(
        FINAL_ALLOWLIST,
        {
            "base": FROZEN_EVIDENCE,
            "expected_paths": intended,
            "owner": OWNER,
            "path_count": len(intended),
            "phase": PHASE,
            "schema": "ghc.family.final-staged-allowlist.v3",
        },
    )
    exclusions = {FINAL_OWNER_MANIFEST, FINAL_DELTA_MANIFEST, FINAL_STAGED_REVIEW, CONTENT_SEAL, CLOSEOUT_RECEIPT}
    owner_entries = manifest_rows(path for path in phase_owner_files() if path.relative_to(ROOT).as_posix() not in exclusions)
    write_json(
        FINAL_OWNER_MANIFEST,
        {
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.final-owner-manifest.v3",
            "self_exclusions": sorted(exclusions),
        },
    )
    delta_paths = [path for path in phase_owner_files() if is_changed_from_evidence(path) and path.relative_to(ROOT).as_posix() not in exclusions]
    delta_entries = manifest_rows(delta_paths)
    write_json(
        FINAL_DELTA_MANIFEST,
        {
            "base": FROZEN_EVIDENCE,
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.final-delta-manifest.v3",
            "self_exclusions": sorted(exclusions),
        },
    )
    seal_paths = [
        "docs/elowen-cairn/v669-v2/closeout/final-integrated-overview.md",
        "docs/elowen-cairn/v669-v2/closeout/phase-truth.json",
        "docs/elowen-cairn/v669-v2/closeout/method-flow-ledger.json",
        "docs/elowen-cairn/v669-v2/closeout/open-exact-gate-register.json",
        "docs/elowen-cairn/v669-v2/closeout/static-report.html",
        FINAL_OWNER_MANIFEST,
        FINAL_DELTA_MANIFEST,
    ]
    seal_rows = manifest_rows(ROOT / path for path in seal_paths)
    seal_payload = {
        "files": seal_rows,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.content-seal.v3",
        "status": "SEALED_FINAL_CANDIDATE",
    }
    seal_payload["payload_sha256"] = sha256_bytes(canonical_json_bytes(seal_payload))
    write_json(CONTENT_SEAL, seal_payload)
    write_json(
        CLOSEOUT_RECEIPT,
        {
            "canonical_status": "PENDING_EXACT_FINAL_COMMIT_PUSH_EQUALITY",
            "content_seal_payload_sha256": seal_payload["payload_sha256"],
            "exact_final": "TO_BE_BOUND_EXTERNALLY_AFTER_COMMIT",
            "final_parent": FROZEN_EVIDENCE,
            "owner": OWNER,
            "phase": PHASE,
            "route_state": "PREPARED_NOT_SENT",
            "schema": "ghc.family.closeout-receipt.v3",
            "status": "FINAL_CLOSEOUT_CANDIDATE",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    payload = {
        "delta_manifest_entries": len(delta_entries),
        "final_truth": FINAL_OVERLAY,
        "owner": OWNER,
        "owner_manifest_entries": len(owner_entries),
        "phase": PHASE,
        "route_state": "PREPARED_NOT_SENT",
        "status": "FINAL_CLOSEOUT_MATERIALIZED_NOT_COMMITTED",
    }
    payload["payload_sha256"] = sha256_bytes(canonical_json_bytes(payload))
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

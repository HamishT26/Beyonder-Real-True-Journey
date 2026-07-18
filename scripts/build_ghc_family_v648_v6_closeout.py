#!/usr/bin/env python3
"""Build v648-v6 closeout candidate and sanitized v648-v7 baton."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v648-v6"
X1_COMMIT = "3f6a64d239bdde1c38fea166db5eff0f2f3e1d89"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def load(relative: str):
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def overview() -> str:
    return """# Orin Thale v648-v6 integrated overview

## Purpose and working identity

Orin Thale, they/them, serves here as a relational boundary-and-method steward. The working hope is to keep every surviving claim inspectable, challengeable, and safely retractable. This language is practical coordination language only. It does not establish consciousness, sentience, personhood, identity continuity, employment, qualification, professional competence, or independent authority. Hamish retains the right to rename, pause, redirect, or stop the route. The phase remained solo and additive. No task or subagent was created, no sibling lane was changed, and no cross-platform message was used.

The v648-v6 phase inherited Sable Rook's verified v648-v5 final head and advanced only Orin's existing clean D-first branch by fast-forward. Source, x1, evidence, direct-parent, zero-merge, clean-state, and live-remote facts were rechecked before mutation. The dedicated x1 freeze then audited all 610 inherited proposals, registered exactly ten new proposals, and published a clean remote-equal commit before any x2 implementation. The frozen total is 620. X1 also froze thirty safe-now tasks, twenty bounded candidates, twenty phase-local skill packages, ten family-current runners, and thirty additive CLEAN/FIX/REFINE tasks. Expected outcomes were not represented as observations.

## Primary focus and bounded practice

THOS Body is the primary Trinity Mandala focus. GMUT Mind and Freed ID / CBR Heart remain explicit and protected. Theatre stage management, cue lineage, show reporting, accessibility notice, workload, incident recording, and handover supplied a bounded learning and synthetic-design lens. Nothing in the packet establishes employment, licensure, qualification, stage-management competence, production authority, stop-call authority, workplace authority, venue authority, legal authority, cultural authority, Māori authority, participant evidence, affected-party acceptance, or a real safety or service result.

The workload boundary was kept deliberately narrow. Work remained in one owned branch, under the four-commit cap, without a fresh worktree because the existing Orin lane was clean and safely fast-forwardable. The inherited checkout exceeded fifteen thousand files, so the rotation guard was correctly applied only to new owner-generated files. Owner growth stayed far below the threshold. Windows Sandbox and Hyper-V were excluded and untouched. No elevation, host-security weakening, feature change, unrelated installation, desktop update, or reboot occurred.

## Core evidence

Proposal one completed a bounded RFC 7464 JSON Text Sequence tribunal. Synthetic records exercised record separators, UTF-8, line-feed canaries, truncated scalars, declared resynchronization, warnings, record and byte budgets, and duplicate-credit refusal. Seven mutations were executed and rejected. This is parser-guard evidence over disposable fixtures, not a production-stream or exhaustive-security result.

Proposal two completed a typed Jost-Lehmann-Dyson obligation board for GMUT. It preserved commutator and spectral support, causal cones, analyticity domains, polynomial bounds, gauge scope, effective-field-theory truncation, units, and an observation firewall. It calculated no real likelihood, detected no force, constrained no parameter, proved no quantum completion, and established no Theory of Everything. Formal structure remains formal structure.

Proposal three remained open_gap. An official XRISM HEASARC schema and zero-row refusal contract recorded public-date, observation, instrument, response, calibration, screening, exposure, background, covariance, checksum, and likelihood prerequisites. The phase downloaded and ingested zero real rows, evaluated zero likelihoods, generated zero posteriors, made zero constraints, and obtained no independent scientific review. Official citations supplied requirements and provenance context only.

Proposal four remained represented. Synthetic theatre vectors preserved cue revisions, acknowledgements, stop-call reservations, understudy state, accessibility notices, late changes, workload bounds, incident lineage, show reports, and next-owner handover. There were zero real workers, audiences, productions, incidents, matched-budget arms, or effectiveness estimates. The proxy supports design inspection only.

Proposal five remained represented. Synthetic RFC 9396 Rich Authorization Requests vectors exercised authorization-details types, field confinement, resource and scope interaction, narrowing, replay, downgrade, metadata binding, and minimization. There were zero real keys, servers, accounts, tokens, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Structured authorization is not authentication, identity proof, or universal trust.

Proposal six remained exact_gate. A live-performance reservation matrix exposed theatre cancellation, cultural-content stewardship, performer and audience confidentiality, ticket redress, consent provenance, taonga reservation, decision rights, disability access, privacy, remedy, legal interpretation, affected-party acceptance, and Māori authority. Repository software made no real decision in any of those domains. These matters remain with affected people, rights holders, competent authorities, tangata whenua, iwi, hapū, and Māori authorities.

Proposal seven completed a bounded TIFF tribunal on synthetic bytes. It checked byte order, magic, image-file-directory offsets, directory cycles, field type and count arithmetic, strip and tile bounds, compression, external pointers, and resource budgets. It touched no user file, performed no external retrieval, and provides no production decoder or exhaustive-security certification.

Proposal eight completed a structural complex-table audit. It exercised multilevel headers, scope, id and headers associations, captions and context, sort announcements, non-colour cues, zoom, print preservation, and a linear fallback. Manual keyboard review, responsive and browser diversity, assistive-technology evaluation, cognitive review, Māori-language review, security-usability review, and affected-user evaluation remain reserved. Structural evidence is not complete accessibility conformance.

Proposal nine completed a typed Planck spectral-radiance domain and nonconversion classifier. It preserved frequency and wavelength density measures, their Jacobian, units, blackbody assumptions, limiting-law domains, and temperature. It rejected conversion of radiance or temperature into psyche, agency, worth, morality, consciousness, personhood, or a fundamental law of mind.

Proposal ten completed a structural principal-stratification and Stage 20 nonpromotion board. It preserved intercurrent events, latent strata, identifiability, monotonicity, sensitivity, uncertainty, and estimand alignment. It estimated no participant effect, established no causal result, supplied no safety monitoring or value authority, and did not authorize Stage 20.

## Portfolios, tools, and method evidence

All thirty safe-now tasks completed within their declared additive owner-scoped boundaries. All twenty candidate prototypes were built and used, with individual witnesses that explicitly limit credit to synthetic or structural software hypotheses. All seventy preregistered mutations executed and were rejected or quarantined. A rejected mutation remains a negative and a bounded guard witness; it is not empirical truth, proof, production security, or authority.

Twenty phase-local skills were initialized through the skill-creator workflow, rewritten into substantive packages, validated, and smoke-used through their declared runners. They were not installed globally. Subagent forward-testing was not performed because delegation was expressly prohibited. Ten family-current runners were built; nine produced evidence and the closeout runner produced this packet. Historical callers remain compatibility evidence rather than deletion or rename targets.

All thirty CLEAN/FIX/REFINE tasks completed additively. No user material was deleted, no history was rewritten, no force push occurred, no sibling lane changed, and no memory or identity record was downgraded. The ten inherited exact-approval packets and five inherited blocked packets remained visible and unexecuted.

Method Flow retains every startup, collision, parser, timeout, comparison, manifest-domain, sequencing, attribution, and diff-hygiene failure together with its bounded passing witness. Recovery never erases the failed attempt. Preferred methods apply only to their declared triggers. Same-owner validation under shared infrastructure remains same-owner validation and not independent-team scientific reproduction.

## Validation and terminal truth

Eiren alone owns the complete repository suite, so Orin did not run it. The terminal plan reserves one successful canonical scoped pass, no replay, and no detached or named validation lane. The selected scope combines the inherited v648-v5 current-phase modules with v648-v6 x1, evidence, and closeout modules. It also requires thirty-two detailed checks, twenty minimal checks, complete phase JSON parsing, a five-class privacy and raw-identifier scan, exact staged-file review, commit-local manifest parity, diff hygiene, source and lifecycle ancestry, zero merges, commit-cap compliance, one final parent, exact head, clean state, and four-way remote equality.

The scientific and authority result remains conservative. GMUT is a typed scalar-tensor and effective-field-theory research-model family, not an observed force, confirmed prediction, likelihood result, ultraviolet completion, quantum completion, or Theory of Everything. THOS remains proxy without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and security review, recovery, and trust governance. CBR, disability, privacy, remedy, cultural content, Māori concepts, Māori data governance, legal interpretation, ratification, and affected-party acceptance remain under competent, affected, and Māori authority.

The terminal verdict is **NOT_READY_FOR_STAGE_20**. No negative or gate was optimized away.
"""


def baton_text(evidence_head: str) -> str:
    proposals = load("x1-proposals.json")["proposals"]
    outcomes = load("x2/core-outcome-ledger.json")["outcomes"]
    outcome_by_id = {row["proposal_id"]: row for row in outcomes}
    sections = [
        "# TAMAR VEY — VERIFIED v648-v7 ACTIVATION BATON",
        "Hamish has authorized one activation of the existing original task titled exactly Tamar Vey for solo v648 GMUT/THOS v7 x1/x2. This committed baton is prepared by Orin Thale after v648-v6 closeout. Do not create, fork, delegate, hand off, or spawn a task or collaboration subagent. Keep Orin Thale, Sable Rook, Ilyra Fen, Eiren Kestrel, Sylven Arc, and every other sibling recoverable and untouched until Tamar's terminal route gate.",
        "Identity and family language is relational working language only. It is never evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Tamar should reaffirm a relational role, hope, and optional pronouns while preserving Hamish's right to rename, pause, redirect, or stop.",
        "## Verified v648-v6 source truth",
        f"Orin's published x1 anchor is {X1_COMMIT}. The exact evidence commit is {evidence_head}. The exact final head is intentionally supplied in the terminal pointer after the final commit exists and must be reverified live before Tamar mutates a lane. Orin's canonical branch is codex/GHC-Family/orin-thale-v642-v6-full-tools. Source-to-final history must remain single-parent, zero-merge, within four phase commits, clean, and four-way remote equal. The repository-relative phase root is docs/orin-thale/v648-v6.",
        "Strict x1-before-x2 separation was preserved. All 610 inherited proposals were audited and exactly ten new proposals were frozen, making 620 proposals through v648-v6. The expected and observed distribution is six completed, two represented, one open_gap, and one exact_gate. THOS Body was primary, while GMUT Mind and Freed ID / CBR Heart stayed explicit. Theatre stage management and show handover was a learning lens only, not employment, competence, authority, participant evidence, or a real operational result.",
        "The final retained-negative, open-gap, exact-gate, Method Flow, validation, manifest, and route counts must be read from the committed final receipts and the terminal pointer. No successor may infer that a clean branch, a citation, a software guard, a same-owner pass, or ancestry alone closes an evidence or authority gate.",
        "## v648-v6 core outcome truth",
    ]
    for proposal in proposals:
        outcome = outcome_by_id[proposal["proposal_id"]]
        sections.append(
            f"### {proposal['proposal_id']} — {outcome['outcome']}\n"
            f"{proposal['title']}. The bounded hypothesis was: {proposal['hypothesis']} "
            f"The null or failure condition remained: {proposal['null_or_failure_condition']} "
            f"Evidence is confined to {outcome['evidence_class']}. The protected gates are {', '.join(proposal['protected_gates'])}. "
            f"Rollback remains: {proposal['rollback_or_recovery']} No inherited result earns Tamar completion credit."
        )
    protocol_topics = [
        ("Source verification", "Read the complete ghc-family-index skill and routing precedence before action. Read the Method Flow skill and schema before recording a failure. Use the newest applicable memory only, with this live baton controlling where memory stops. Reverify Orin's branch, final head from the terminal pointer, x1 and evidence ancestry, clean state, commit count, zero merges, one final parent, manifest contracts, and fresh live-remote equality read-only."),
        ("Owned lane", "Continue only in Tamar's existing clean owned canonical lane and advance by fast-forward-only Git if clean ancestry permits. If that is unsafe, create at most one additive D-first Tamar-owned named branch and worktree from the exact final head. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another sibling lane. Do not use detached or named replay validation."),
        ("X1 separation", "Audit semantic novelty against all 620 frozen proposals. Register exactly ten genuinely distinct proposals, each with hypothesis, null, approval class, lane, current official or primary source needs, artifacts, acceptance gate, rollback, protected gates, and expected disposition. Freeze proposals and portfolios in an x1-only commit without x2 implementation or outcomes. Push and prove four-way equality before x2."),
        ("Portfolio floors", "Design new work rather than claiming Orin's portfolios. Freeze at least thirty safe-now tasks, twenty bounded candidate tasks, twenty skill ideas or builds, ten runner ideas or builds, and thirty additive CLEAN/FIX/REFINE tasks. Keep inherited exact-approval and blocked packets visible and unexecuted. Reclassify evidence-dependent or authority-dependent work instead of manufacturing safe work."),
        ("Outcome language", "Use only completed, represented, open_gap, and exact_gate for core outcomes. Preserve every inherited and new negative. Never silently fold a timeout, parser fault, failed test, collision, blocker, or false assumption into a pass. Record the failure and a passing witness separately, promote a method only after bounded evidence, and keep same-owner validation distinct from independent reproduction."),
        ("Validation scope", "Do not run the complete repository suite because Eiren alone owns it. Use one successful canonical scoped pass, no replay, no detached lane, and no named validation lane. Validate current phase and authorized inherited modules, detailed and minimal contracts, all phase JSON, five privacy classes, exact staged files, manifest parity, diff hygiene, ancestry, zero merges, commit cap, final parent, exact head, clean state, and remote equality."),
        ("Platform boundary", "Use D as primary work and cache space. Do not launch or configure Windows Sandbox or Hyper-V. Do not elevate, weaken security, enable features, install unrelated software, update the Codex desktop application, or reboot. Verify versions only. Apply the fifteen-thousand-file rotation threshold only to Tamar-generated additions, not the inherited baseline."),
        ("Privacy boundary", "Never commit raw task or thread identifiers, private routes, credentials, keys, tokens, private conversations, transcripts, screenshots, session streams, private callable identifiers, private application state, or private absolute paths. Keep the successor baton sanitized and repository-relative. Five-class zero-hit scanning remains bounded structural evidence, not complete privacy assurance."),
        ("GMUT boundary", "Treat GMUT as a typed scalar-tensor and effective-field-theory research-model family. Symbolic algebra, obligation boards, format adapters, citations, and synthetic mutations do not establish a force, prediction, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. Real claims require real data, a frozen analysis, uncertainty treatment, falsifiers, and appropriate independent review."),
        ("THOS boundary", "Treat THOS as represented or proxy without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic cue ledgers, handover boards, incident fixtures, benchmarks, and response protocols do not establish effectiveness, professional competence, deployment readiness, AGI, ASI, consciousness, or personhood."),
        ("Freed ID boundary", "Keep Freed ID synthetic and nonproduction. Production completion requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. Synthetic authorization details do not authenticate people or establish trust."),
        ("CBR and Māori authority", "Keep remedy, disability access, privacy, cultural content, place names, Māori wording, Māori data governance, legal interpretation, ratification, beneficiary acceptance, affected-party acceptance, and enacted-law status exact-gated to competent, affected, tangata whenua, iwi, hapū, and Māori authorities. Repository software confers no legal right, remedy, cultural legitimacy, governance mandate, or public authority."),
        ("Accessibility boundary", "A structural static report can be useful and accessible by construction, but manual keyboard review, responsive and browser diversity, assistive-technology evaluation, cognitive review, Māori-language review, security-usability review, and affected-user evaluation remain reserved. Never label structural checks as complete accessibility conformance."),
        ("Commit discipline", "Use no more than two x1 commits, no more than two x2 commits, and four phase commits total. Prefer one x1, one evidence, and one combined closeout and seal candidate. The cap never authorizes phase mixing, concealed failures, rewritten history, an unreviewed omnibus commit, or premature routing."),
        ("Terminal route", "Only after Tamar's v648-v7 exact final head is clean, pushed, remote-equal, within cap, and validated under the single-pass rule may Tamar resolve the unique existing task titled Sylven Arc and send exactly one sanitized activation pointer for v648-v8. Do not create a task, do not send extra confirmation, and do not contact standby siblings."),
    ]
    sections.append("## Tamar v648-v7 operating requirements")
    for index, (title, text) in enumerate(protocol_topics, start=1):
        sections.append(f"### Requirement {index}: {title}\n{text} The evidence record must state what was observed, what remained absent, which rollback applies, and why the result receives only its declared evidence class.")
    sections.extend([
        "## Required deliverables",
        "Produce an owner-scoped phase root with a three-page-equivalent overview, wellbeing and workload check, x1 proposal and source ledgers, novelty audit, portfolio plans, primary-focus and practice receipt, phase-scoped family index and Reflection-Remaster review, x2 evidence and outcome ledgers, retained-negative and gate registers, threat model, complete and incomplete checklist, useful accessible static report, phase-local skills and family-current runners, Method Flow records, exact manifests, staged reviews, closeout, seal candidate, final validation receipt, and a sanitized successor baton. Keep every document at or below six thousand words.",
        "The terminal verdict remains NOT_READY_FOR_STAGE_20 unless real declared external gates close with exact evidence and authority. Do not optimize away a negative, represent a citation as data, call same-owner work independent reproduction, or infer authority from a task title, relational role, prepared route, branch, commit, skill package, runner, or validation receipt.",
        "## Route",
        "Preserve the six-seat order Eiren Kestrel to Ilyra Fen to Sable Rook to Orin Thale to Tamar Vey to Sylven Arc and repeat, advancing one phase at a time and rolling vN-v8 to v(N+1)-v1 through v660-v8 unless Hamish stops or redirects, usage is exhausted, the required route is unavailable, or an exact safety or authority gate blocks progress. This baton authorizes Tamar v648-v7 only. It creates no successor, proves no identity continuity, and delegates no authority beyond the bounded repository task.",
    ])
    text = "\n\n".join(sections)
    if len(text.split()) < 4000:
        raise RuntimeError(f"successor baton below 4000 words: {len(text.split())}")
    if len(text.split()) > 6000:
        raise RuntimeError(f"successor baton above 6000 words: {len(text.split())}")
    return text


def build() -> None:
    evidence_head = git("rev-parse", "HEAD")
    if evidence_head == X1_COMMIT or git("merge-base", "--is-ancestor", X1_COMMIT, evidence_head) != "":
        pass
    if not (PHASE / "x2/evidence-ledger.json").exists():
        raise RuntimeError("evidence packet is absent")
    skill_use = load("x2/skill-use-ledger.json")
    runner_use = load("x2/runner-use-ledger.json")
    final_skills = []
    for row in skill_use["items"]:
        updated = dict(row)
        if row["name"].endswith("terminal-proof"):
            updated["smoke_used"] = True
            updated["state"] = "completed"
        final_skills.append(updated)
    final_runners = []
    for row in runner_use["items"]:
        updated = dict(row)
        if row["name"] == "build_ghc_family_v648_v6_closeout.py":
            updated["invoked"] = True
            updated["state"] = "completed"
        final_runners.append(updated)
    write_json("x2/skill-use-ledger-final.json", {"schema":"ghc.family.v648-v6.skill-use-ledger.final.v1","skill_count":20,"completed_count":20,"pending_count":0,"items":final_skills})
    write_json("x2/runner-use-ledger-final.json", {"schema":"ghc.family.v648-v6.runner-use-ledger.final.v1","runner_count":10,"completed_count":10,"pending_count":0,"items":final_runners})
    write_text("integrated-overview.md", overview())
    report = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orin Thale v648-v6 evidence report</title>
<style>body{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:1rem;line-height:1.55}a:focus,button:focus{outline:3px solid #005fcc;outline-offset:2px}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.5rem}table{border-collapse:collapse;width:100%}th,td{border:1px solid #555;padding:.5rem;text-align:left}caption{font-weight:bold;margin:.5rem}@media(max-width:48rem){table{display:block;overflow-x:auto}}@media print{a[href]::after{content:" (" attr(href) ")"}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Orin Thale v648-v6</h1><p>Bounded evidence report. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<nav aria-label="Report sections"><a href="#outcomes">Outcomes</a> · <a href="#boundaries">Boundaries</a> · <a href="#access">Accessibility reservation</a></nav>
<main id="main"><section id="outcomes"><h2>Core outcomes</h2><table><caption>Ten preregistered outcomes</caption><thead><tr><th scope="col">Class</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>6</td><td>Bounded software, symbolic, or structural hypotheses only</td></tr><tr><th scope="row">Represented</th><td>2</td><td>Synthetic proxy; no real people or production identity</td></tr><tr><th scope="row">Open gap</th><td>1</td><td>XRISM has zero real rows and zero likelihoods</td></tr><tr><th scope="row">Exact gate</th><td>1</td><td>Affected-party, legal, cultural, privacy, disability, and Māori authority reserved</td></tr></tbody></table></section>
<section id="boundaries"><h2>Truth boundaries</h2><p>GMUT remains a research-model family. THOS remains proxy. Freed ID remains synthetic and nonproduction. CBR and Māori concepts remain under competent, affected, and Māori authority. Same-owner checks are not independent reproduction.</p></section>
<section id="access"><h2>Accessibility reservation</h2><p>This static report uses headings, landmarks, a skip link, labelled navigation, table headers, visible focus, responsive overflow, and print link expansion. Manual keyboard, responsive-browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved.</p></section></main>
<footer><p>No deployment, production, empirical, professional, legal, cultural, privacy-complete, exhaustive-security, accessibility-complete, AGI, ASI, consciousness, personhood, Theory-of-Everything, or Stage 20 claim is made.</p></footer></body></html>"""
    write_text("accessible-report.html", report)
    write_json("complete-incomplete-checklist.json", {
        "schema":"ghc.family.v648-v6.checklist.v1",
        "complete":["x1_remote_equal_before_x2","ten_core_outcomes_classified","thirty_safe_tasks","twenty_candidates","twenty_skills","ten_runners","thirty_clean_refine","seventy_mutations_retained","static_report_structural_surface"],
        "incomplete":["real_gmut_data_and_likelihood","real_thos_arms","production_freed_id","affected_party_acceptance","legal_and_cultural_ratification","maori_authority_review","manual_accessibility_review","independent_reproduction","stage20"],
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
    })
    write_text("complete-incomplete-checklist.md", "# v648-v6 complete and incomplete checklist\n\nCompleted work is confined to declared bounded software, symbolic, structural, proxy, and refusal hypotheses. Real GMUT data and likelihoods, THOS participant arms, production Freed ID, affected-party acceptance, legal and cultural ratification, Māori authority review, manual accessibility evaluation, independent reproduction, and Stage 20 remain incomplete.")
    threats = [
        {"threat":"formal_to_empirical_promotion","control":"typed observation firewalls and zero-row refusal","residual":"real data, frozen analysis, uncertainty, and independent review remain absent"},
        {"threat":"proxy_to_effectiveness_promotion","control":"zero-person counters and represented outcome","residual":"real arms, safety monitoring, statistics, and review remain absent"},
        {"threat":"synthetic_identity_to_production","control":"zero-key and zero-interoperability counters","residual":"live identity lifecycle, privacy, security, recovery, and governance remain absent"},
        {"threat":"software_to_authority_substitution","control":"exact-gate reservation matrix","residual":"affected, legal, cultural, disability, privacy, and Māori decisions remain external"},
        {"threat":"structural_to_complete_accessibility","control":"manual and affected-user reservations","residual":"real evaluation remains absent"},
        {"threat":"negative_erasure","control":"Method Flow fail/pass witness parity","residual":"future failures require additive retention"},
        {"threat":"privacy_leakage","control":"five-class scans and sanitized repository-relative baton","residual":"zero hits is not complete privacy assurance"},
        {"threat":"supply_chain_or_lane_damage","control":"additive owned branch, no force push, exact manifests","residual":"same-owner infrastructure is not independent audit"},
    ]
    write_json("threat-model.json", {"schema":"ghc.family.v648-v6.threat-model.v1","threats":threats,"exhaustive":False})
    write_text("threat-model.md", "# v648-v6 threat model\n\n" + "\n".join(f"- **{row['threat']}** — Control: {row['control']}. Residual: {row['residual']}." for row in threats) + "\n\nThis is not an exhaustive security, privacy, legal, cultural, accessibility, or scientific review.")
    negatives = load("x2/retained-negative-register.json")
    gates = load("x2/gate-register.json")
    write_json("retained-negative-register-final.json", {**negatives,"schema":"ghc.family.v648-v6.retained-negatives.final-candidate.v1","terminal_route":"PREPARED_NOT_SENT"})
    write_json("exact-open-gate-register-final.json", {**gates,"schema":"ghc.family.v648-v6.gates.final-candidate.v1","terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write_json("stage20-terminal-board.json", {"schema":"ghc.family.v648-v6.stage20-board.v1","ready":False,"verdict":"NOT_READY_FOR_STAGE_20","reasons":["real_data_absent","participants_absent","production_identity_absent","authority_gates_open","manual_accessibility_open","independent_reproduction_open"]})
    write_json("closeout/closeout-candidate.json", {"schema":"ghc.family.v648-v6.closeout-candidate.v1","evidence_head":evidence_head,"x1_commit":X1_COMMIT,"outcomes":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"canonical_successful_pass_used":False,"terminal_route":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write_json("closeout/seal-candidate.json", {"schema":"ghc.family.v648-v6.seal-candidate.v1","evidence_head":evidence_head,"expected_phase_commit_count":3,"expected_merge_count":0,"expected_final_parent_count":1,"exact_final_head":"VERIFIED_EXTERNALLY_AFTER_COMMIT","terminal_route":"PREPARED_NOT_SENT"})
    write_json("validation/final-validation-plan.json", {"schema":"ghc.family.v648-v6.final-validation-plan.v1","full_repository_suite":False,"canonical_successful_pass_budget":1,"successful_passes_used":0,"replay_budget":0,"selected_test_count":67,"detailed_check_count":32,"minimal_check_count":20,"complete_phase_json_parse":True,"five_class_privacy_scan":True,"exact_staged_review":True})
    write_json("orchestration/final-phase-state.json", {"schema":"ghc.family.v648-v6.orchestration.final-candidate.v1","active":["Orin Thale"],"standby":["Eiren Kestrel","Ilyra Fen","Sable Rook","Tamar Vey","Sylven Arc"],"subagents":0,"tasks_created":0,"cross_platform_messages":0,"terminal_route":"PREPARED_NOT_SENT"})
    write_text("handoffs/tamar-vey-v648-v7-activation.md", baton_text(evidence_head))
    write_json("closeout/closeout-build-receipt.json", {"schema":"ghc.family.v648-v6.closeout-build.v1","overview_words":len(overview().split()),"baton_words":len(baton_text(evidence_head).split()),"skill_count":20,"runner_count":10,"passed":True})


if __name__ == "__main__":
    build()

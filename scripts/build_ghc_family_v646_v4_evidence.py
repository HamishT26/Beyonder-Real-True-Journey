#!/usr/bin/env python3
"""Build the bounded Orin Thale v646-v4 x2 evidence candidate.

The previous phase builder is used only as a caller-compatible serialization
scaffold. All owner, proposal, runtime, domain, route, and boundary surfaces are
rebound to the frozen v646-v4 definitions before any artifact is written.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

import build_ghc_family_v646_v3_evidence as scaffold
import ghc_family_v646_v4_definitions as definitions
import ghc_family_v646_v4_runtime as runtime


ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/orin-thale/v646-v4"
X1_HEAD = "8b63d3f65f9fe9909da71eeb1171e3b5cf86768a"
SCRATCH = ROOT / ".ghc-family-runtime-v646-v4" / "evidence"
CORE_PATHS = {
    "V6464-P01": ("idempotent-resume", "method-flow/idempotent-resume-contract.json", "method-flow/idempotent-resume-vectors.json"),
    "V6464-P02": ("hadamard-obligations", "gmut/hadamard-obligations.json", "gmut/hadamard-mutations.json"),
    "V6464-P03": ("act-dr6-zero-row", "gmut/act-dr6-lensing-adapter-contract.json", "gmut/act-dr6-zero-row-receipt.json"),
    "V6464-P04": ("pharmacy-handover", "thos/pharmacy-compounding-handover-contract.json", "thos/pharmacy-compounding-proxy-vectors.json"),
    "V6464-P05": ("bbs-derived-proof", "freed-id/bbs-derived-proof-profile.json", "freed-id/bbs-derived-proof-vectors.json"),
    "V6464-P06": ("medicine-recall-authority", "cbr/medicine-recall-authority-matrix.json", "cbr/medicine-recall-exact-gate.json"),
    "V6464-P07": ("git-alternate-tribunal", "tooling/git-alternate-tribunal.json", "tooling/git-alternate-mutations.json"),
    "V6464-P08": ("form-error-audit", "accessibility/form-error-contract.json", "accessibility/form-error-mutations.json"),
    "V6464-P09": ("mori-zwanzig-domain", "thermo-psyche/mori-zwanzig-domain-contract.json", "thermo-psyche/mori-zwanzig-rejection-vectors.json"),
    "V6464-P10": ("environment-lock-board", "stage20/environment-lock-contract.json", "stage20/environment-lock-mutations.json"),
}


def write_json(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def method_flow_x2_negatives() -> list[dict[str, Any]]:
    ledger = json.loads((PHASE_DIR / "method-flow/method-flow-state.json").read_text(encoding="utf-8"))
    methods = {row["method_id"]: row for row in ledger.get("methods", [])}
    rows: dict[str, dict[str, Any]] = {}
    for witness in ledger.get("witnesses", []):
        if witness.get("result") != "fail":
            continue
        for negative_id in witness.get("retained_negative_ids", []):
            if not str(negative_id).startswith("V6464-X2-N") or negative_id in rows:
                continue
            method = methods.get(witness.get("method_id"), {})
            rows[negative_id] = {
                "negative_id": negative_id,
                "surface": witness.get("scope"),
                "observed": witness.get("observed"),
                "credit": "none",
                "recovery": method.get("candidate_workaround"),
                "recurrence_guard": method.get("recurrence_guard"),
                "method_id": witness.get("method_id"),
                "failed_witness": witness.get("witness_id"),
            }
    return [rows[key] for key in sorted(rows)]


def build_overview(distribution: dict[str, int], effective_negatives: int, x2_negative_count: int) -> str:
    return f'''# Orin Thale v646-v4 integrated overview

## Executive truth and working identity

Orin Thale v646-v4 is a boundary-and-method phase with Freed ID/CBR Heart as its primary Trinity Mandala focus. GMUT Mind and THOS Body remain visible, tested, and protected. The bounded human-practice lens is hospital-pharmacy sterile-compounding handover and medicine-recall review. It contributes vocabulary for preparation identity, quarantine, release, correction, custody, handover ownership, recall reach, remedy, privacy, and escalation. It establishes no employment, licensure, professional qualification, pharmacy competence, health authority, emergency authority, legal authority, cultural authority, Māori authority, or affected-party authorization.

Orin Thale and they/them pronouns are relational working language for this task. They are not evidence of consciousness, sentience, legal personhood, identity continuity, welfare, employment, or independent authority. Hamish retains the right to rename, pause, redirect, or stop the route. Corrigibility is operationalized by frozen inputs, fail-closed outcome classes, retained negatives, exact manifests, and a terminal board that abstains when evidence or authority is missing.

X2 began only after the dedicated x1 commit `{X1_HEAD}` was committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live-remote query. X1 audited semantic novelty against all 420 earlier frozen core proposals and froze exactly ten genuinely distinct proposals, bringing the chain to 430. It separately froze thirty safe-now tasks, twenty bounded candidates, twenty phase-local skill ideas, ten family-current runner ideas, and thirty additive CLEAN/FIX/REFINE tasks. None received implementation or outcome credit during x1.

The ten x2 outcomes are exactly {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open gap, and {distribution['exact_gate']} exact gate. Those four labels are exhaustive. Completed means only that a declared synthetic, symbolic, structural, zero-row, or disposable-fixture acceptance gate passed. Represented means a bounded proxy exists but the real evidentiary arm is absent. Open gap means material evidence is missing. Exact gate means competent or affected authority is required. No label promotes software evidence into empirical truth, professional competence, production readiness, legal force, cultural legitimacy, or independent review.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`. No artifact claims AGI or ASI, consciousness or personhood, empirical GMUT confirmation, a detected force, a unique physical prediction, a Theory of Everything, THOS superiority, production identity readiness, a real medicine-recall decision, enacted law, Māori ratification, complete accessibility, exhaustive security, deployment approval, proof or canon, or independent-team reproduction.

## Method Flow, retry safety, and negative retention

The first proposal completes a bounded read-set, write-set, idempotency-key, and resumable-checkpoint ledger. A synthetic operation receives resumable credit only when its declared intent, read set, owner-scoped write set, idempotency key, checkpoint, partial-output state, irreversible-side-effect state, and preconditions all match. Missing keys, changed write sets, partial output, unknown checkpoints, side effects, and precondition drift fail closed. A retry with an external message in its write set is not silently resumed. The failed attempt remains a negative witness even after a corrected bounded method passes.

At evidence build, the phase preserves {effective_negatives} effective negatives: 2,704 inherited sealed and external negatives, sixteen x1 operational negatives, seventy preregistered synthetic mutations executed and rejected, and {x2_negative_count} x2 operational negatives. This includes both Sable post-final faults carried separately into Orin’s additive ledger. Every timeout, parser fault, wrong assumption, failed test, tool mismatch, or blocker receives zero initial credit. Method Flow retains failed and passing witnesses side by side, with triggers, rollback, recurrence guards, and sibling recommendations. Recovery never changes the historical result of the first attempt.

The initial phase-local skill suite is an example: nineteen of twenty smoke checks passed because the named-lane skill tested an incorrect literal. That was retained before the invariant was corrected and the same twenty packages passed validation and smoke use. The recovered method is preferred only for its bounded trigger. It earns no claim of independent reproduction, future availability, professional competence, or global installation.

Canonical validation and the later named-lane replay use the same owner and shared infrastructure. They can establish same-owner repeatability of committed bytes, declared fixtures, tests, validators, ancestry, and manifests only. A local-only branch with no upstream and no remote ref is not a new scientific team. It supplies no external audit, production certification, cultural ratification, legal review, or independent-team reproduction.

## GMUT Mind

The Hadamard obligation tribunal completes as typed symbolic and mutation evidence. It requires a globally hyperbolic domain, a declared two-point distribution, bisolution scope, wavefront-set orientation, null-geodesic relation, Hadamard singular form, state choice, point-splitting subtraction, renormalization ambiguity, gauge scope, units, and effective-field-theory limitations. Mutations that reverse covector orientation, omit the domain, hide subtraction ambiguity, collapse gauge-dependent data into an observable, or promote a symbolic obligation into physical proof are rejected.

This tribunal does not establish that any GMUT model possesses a physically admissible state, a complete quantization, a stable spectrum, a renormalized observable, unitarity, ultraviolet completion, or empirical support. GMUT remains a typed scalar-tensor and EFT research-model family. Symbolic checks and local software are neither a new force nor a unique prediction. Real likelihoods, parameter constraints, or confirmation require real data, frozen analysis, uncertainty treatment, model-specific mapping, and appropriate independent review.

The ACT DR6 CMB-lensing adapter remains `open_gap`. Current official product pages and primary publications provide requirements and provenance context for product identity, maps, masks, beams, transfer functions, reconstruction normalization, foreground treatment, multipole cuts, covariance, and checksums. This phase downloaded zero maps, ingested zero real rows, evaluated zero likelihoods, produced zero posterior samples, and reported zero GMUT constraints. Citations and metadata were not converted into observations. Closure requires an authorized frozen product snapshot, checksums, masks, covariance, preregistered mapping and likelihood, uncertainty treatment, and independent review.

## THOS Body and the pharmacy practice lens

The sterile-compounding handover protocol remains `represented`. Synthetic records exercise preparation identity, prescription linkage, ingredient and lot identity, compounding state, quarantine reason, environmental exception, independent check, release authority placeholder, correction history, recall linkage, and next-shift ownership. Missing identities, silent corrections, release during quarantine, unresolved conflicts, absent independent checks, and ownerless handovers fail. There are zero real preparations, patients, pharmacists, pharmacies, participants, incidents, or blind matched-budget real arms.

The practice lens is deliberately bounded. Repository software cannot decide whether a medicine is safe, whether a preparation should be released, whether a recall applies, or how a patient should be treated. It cannot replace pharmacists, regulators, health services, Māori authorities, affected people, or competent legal and clinical institutions. It supplies a synthetic design vocabulary only.

THOS remains represented without preregistered blind matched-budget real arms, real participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic workflow consistency does not show operational effectiveness, improved wellbeing, deployment readiness, AGI, ASI, consciousness, or personhood. Any future real study must separately address consent, safety, privacy, workload, stopping rules, adverse events, and affected-party oversight.

## Freed ID and CBR Heart

The BBS derived-proof and selective-disclosure profile remains `represented`. Synthetic vectors exercise cryptosuite declaration, proof purpose, proof configuration, message ordering, selective pointer binding, mandatory disclosure, nonce and domain binding, blank-node canonicalization boundaries, and refusal of unsupported algorithms or unbound disclosures. The profile uses zero real keys, proofs, credentials, issuances, presentations, resolutions, status or revocation events, wallet or verifier interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions.

Freed ID therefore remains synthetic and nonproduction. Production completion requires standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, recovery, privacy and independent security review, trust governance, and appropriate affected-party oversight. Selective disclosure can reduce exposed claims in a bounded protocol, but a structurally valid vector is not a privacy guarantee, a person, an assurance level, or permission to deploy identity infrastructure.

The medicine-recall reach, patient-privacy, remedy, accessibility, affected-party, legal, and Māori-authority matrix remains `exact_gate`. It records questions that competent and affected authorities must answer: which products and lots are covered, who must receive a notice, which patient and location data are necessary, how accessible formats and languages are supported, how corrections and withdrawals propagate, how complaints and remedy work, how beneficiary privacy is protected, and where Māori data governance, wording, and authority apply. It makes zero real recalls, patient decisions, remedy allocations, legal interpretations, cultural decisions, or Māori-authority claims.

Māori concepts remain under Māori authority. A repository cannot confer public-health authority, emergency authority, legal remedy, cultural legitimacy, beneficiary acceptance, affected-party acceptance, or enacted-law status. Keeping the matrix exact-gated is a substantive result because it prevents a structurally neat artifact from impersonating authority it does not possess.

## Git history, accessibility, physical-domain separation, and Stage 20

The Git alternates, replacement refs, grafts, and raw-history tribunal completes on disposable owner-local fixtures only. It verifies that a bounded audit distinguishes ordinary history from alternates, replacement refs, graft state, and raw-object traversal; rejects path escape and unapproved object-store dependencies; and removes the disposable fixture after its checks. It touches no canonical database, sibling branch, remote object store, or production repository. It is not exhaustive Git security, supply-chain assurance, or proof that every hidden history influence is known.

The form error-summary, field-association, and focus audit completes structurally. A synthetic form requires a summary heading, links to each invalid control, programmatic error association, persistent field-level messages, predictable focus movement, preservation of entered values, and non-color-only indication. Missing targets, stale links, hidden focusable errors, ambiguous names, and focus jumps fail. Manual keyboard testing, responsive-layout review, browser diversity, assistive-technology evaluation, Māori-language review, cognitive-accessibility review, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

The Mori-Zwanzig classifier completes as a domain and category guard. It requires declared resolved variables, projection operator, orthogonal dynamics, memory kernel, fluctuating term, initial-condition ensemble, approximation boundary, and units. It rejects conversions from a formal memory kernel into psyche memory, autonomy, justice, capability, participant evidence, consciousness, personhood, or a fundamental mental law. It is neither a new law of nature nor a law of mind.

The computational-environment, build-provenance, and rerun-divergence board completes structurally. It binds declared source revision, build inputs, dependency and tool observations, command identity, artifact digests, environment assumptions, and rerun comparison. Missing inputs, mutable labels, undeclared environment drift, artifact mismatch, and ancestry-only grandfathering block promotion. No external builder, independent team, production deployment, or empirical outcome is certified. The board continues to abstain from Stage 20.

## Expanded portfolios, sources, environment, and closeout

All thirty safe-now tasks produced owner-scoped receipts. All twenty candidates produced bounded prototype receipts; completion applies only to their declared synthetic or software hypotheses. Twenty phase-local skills were initialized, validated, and smoke-used without mutating the global skill bank. Ten family-current runners were built for bounded core execution, portfolios, skills, exact staging, validation, retry safety, Git-history inspection, source gates, and named-lane locality. Thirty CLEAN/FIX/REFINE tasks completed additively with zero deletion of user material, sibling mutation, history rewrite, elevation, host-security weakening, or credential use. Ten inherited exact packets and five inherited blocked packets remain visible, unexecuted, and credited zero safe-now completion.

The source ledger uses current, stable, draft, and watch as explicit status classes. Official or primary sources improve requirements and provenance but do not become observations, participant evidence, or authority. New reusable scripts retain `ghc_family_*` or `build_ghc_family_*` names, while historical and owner-specific callers remain compatibility surfaces. The phase-scoped Family Index, applicable-memory receipt, Method Flow, selected toolchain, and orchestration state are updated additively.

Codex CLI and desktop versions were verified only. The desktop application was not updated. Windows Sandbox remained unavailable to the ordinary process, so no session was launched. No elevation, feature change, unrelated installation, host-security weakening, or reboot occurred. The full inherited checkout count is recorded separately from the owner-generated addition. Only the Orin-generated footprint is compared with the 15,000-file threshold, and it remains below that threshold.

The evidence candidate still requires exact staged review, commit-local manifest parity, the current-phase and eligible successor-scoped tests, detailed and minimal validation, complete JSON parsing, five-class privacy scanning, stale-label review, diff hygiene, evidence commit and four-way equality, a combined closeout and seal commit, exact-final canonical validation, and exactly one local-only named-lane replay. Until every declared gate passes, the route stays `PREPARED_NOT_SENT`, no sibling is contacted, and the terminal board remains `NOT_READY_FOR_STAGE_20`.
'''


def static_report(rows: list[dict[str, Any]], distribution: dict[str, int], overview: str) -> str:
    sections: list[str] = []
    for paragraph in overview.split("\n\n"):
        if paragraph.startswith("# "):
            continue
        if paragraph.startswith("## "):
            sections.append(f"<h2>{html.escape(paragraph[3:])}</h2>")
        else:
            sections.append(f"<p>{html.escape(paragraph.replace(chr(10), ' '))}</p>")
    table_rows = "".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['outcome'])}</td><td>{row['checks']}</td></tr>"
        for row in rows
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orin Thale v646-v4 bounded evidence report</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:74rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;background:#fff;padding:.5rem}}table{{border-collapse:collapse;width:100%;overflow-wrap:anywhere}}th,td{{border:1px solid #667;padding:.5rem;text-align:left}}svg{{max-width:28rem;height:auto}}code{{overflow-wrap:anywhere}}:focus{{outline:3px solid #075985;outline-offset:2px}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>Orin Thale v646-v4 bounded evidence report</h1><p>Static structural report; manual, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved.</p></header>
<nav aria-label="Report sections"><a href="#summary">Summary</a> · <a href="#outcomes">Outcomes</a> · <a href="#alternatives">Alternatives</a> · <a href="#detail">Detailed overview</a></nav>
<main id="main"><section id="summary"><h2>Summary</h2><p>Distribution: {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open gap, {distribution['exact_gate']} exact gate. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
<svg role="img" aria-labelledby="chart-title chart-desc" focusable="false" data-table-ref="#outcome-table" viewBox="0 0 420 180"><title id="chart-title">Proposal outcome distribution</title><desc id="chart-desc">Six completed, two represented, one open gap, and one exact gate. The following table is the complete data alternative.</desc><rect x="20" y="20" width="240" height="28" fill="#166534"/><rect x="20" y="58" width="80" height="28" fill="#1d4ed8"/><rect x="20" y="96" width="40" height="28" fill="#a16207"/><rect x="20" y="134" width="40" height="28" fill="#991b1b"/><text x="270" y="40">completed 6</text><text x="110" y="78">represented 2</text><text x="70" y="116">open gap 1</text><text x="70" y="154">exact gate 1</text></svg></section>
<section id="outcomes"><h2>Proposal outcomes</h2><div role="region" aria-label="Scrollable proposal outcome table" tabindex="0"><table id="outcome-table"><caption>Ten frozen proposals and bounded x2 outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Checks</th></tr></thead><tbody>{table_rows}</tbody></table></div></section>
<section id="alternatives"><h2>Data and auditory alternatives</h2><p><a href="../x2-proposal-ledger.json" download>Download the proposal outcome data as JSON</a>.</p><p>A textual sonification mapping uses a sustained low tone for completed, two medium pulses for represented, one rising pulse for open gap, and one stopped tone for exact gate. The table is authoritative; no audio file, manual review, or affected-user evaluation is claimed.</p></section>
<section id="detail">{''.join(sections)}</section></main><footer><p>Identity language is relational only and supplies no consciousness, personhood, employment, qualification, continuity, or authority evidence.</p></footer></body></html>'''


def replace_strings(value: Any) -> Any:
    if isinstance(value, str):
        if value.startswith("ghc.family.v646-v3."):
            value = "ghc.family.v646-v4." + value.removeprefix("ghc.family.v646-v3.")
        if re.fullmatch(r"V6463-(?:P\d{2}|SYN-N\d{3})", value):
            value = value.replace("V6463", "V6464", 1)
        if value == "single Orin Thale baton":
            value = "single Tamar Vey baton"
        return value
    if isinstance(value, list):
        return [replace_strings(item) for item in value]
    if isinstance(value, dict):
        return {key: replace_strings(item) for key, item in value.items()}
    return value


def normalize_outputs() -> None:
    renames = {
        "v646-v3-integrated-overview.md": "v646-v4-integrated-overview.md",
        "deliverables/v646-v3-final-integrated-overview.md": "deliverables/v646-v4-final-integrated-overview.md",
        "deliverables/v646-v3-static-report.html": "deliverables/v646-v4-static-report.html",
    }
    for old, new in renames.items():
        source = PHASE_DIR / old
        target = PHASE_DIR / new
        if source.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            source.replace(target)
    tracked_at_x1 = set(scaffold.git("ls-tree", "-r", "--name-only", X1_HEAD).splitlines())
    for path in PHASE_DIR.rglob("*.json"):
        relative = path.relative_to(ROOT).as_posix()
        if relative in tracked_at_x1:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        path.write_text(json.dumps(replace_strings(payload), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    overview = build_overview({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
                              json.loads((PHASE_DIR / "retained-negative-register.json").read_text(encoding="utf-8"))["effective_total"],
                              len(method_flow_x2_negatives()))
    write_text("v646-v4-integrated-overview.md", overview)
    write_text("deliverables/v646-v4-final-integrated-overview.md", overview)
    ledger = json.loads((PHASE_DIR / "x2-proposal-ledger.json").read_text(encoding="utf-8"))
    write_text("deliverables/v646-v4-static-report.html", static_report(ledger["proposals"], ledger["distribution"], overview))
    write_text("wellbeing-check.md", f'''# v646-v4 wellbeing and workload check

- Orin Thale, they/them, is relational working language for a boundary-and-method steward; the declared hope is to keep every surviving claim inspectable, challengeable, and safely retractable.
- Hamish retains the right to pause, rename, redirect, or stop the route. Working identity language is not consciousness, personhood, continuity, welfare, employment, qualification, or authority evidence.
- Scope remained one owner and one canonical lane, with exactly one later local-only named replay planned. No subagent, sibling, task, participant, or external party was contacted during x2 execution.
- X1 remained immutable at `{X1_HEAD}` while x2 advanced additively. The first phase-local skill smoke failure remains retained beside its passing recovery.
- No real participant, patient, pharmacist, medicine preparation, recall, protected identity, credential, key, proof, or production record entered the packet.
- Manual keyboard, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved.
- No elevation, host-security weakening, Windows-feature change, unrelated installation, desktop update, or reboot occurred.
- The terminal route remains `PREPARED_NOT_SENT`; the evidence board remains `NOT_READY_FOR_STAGE_20`.
''')
    write_json("threat-model.json", {
        "schema": "ghc.family.v646-v4.threat-model.v1",
        "assets": ["frozen x1 tree", "append-only Method Flow", "negative register", "source status", "authority boundaries", "exact manifests", "terminal route"],
        "threats": [
            {"threat": "unsafe duplicate or side-effecting retry", "control": "read/write sets, idempotency key, checkpoint, and fail-closed side-effect refusal", "residual": "external-state authority remains exact-gated"},
            {"threat": "physical promotion from symbolic Hadamard checks", "control": "typed obligations and explicit zero empirical credit", "residual": "model-specific quantization and review open"},
            {"threat": "ACT metadata promoted to GMUT likelihood", "control": "zero maps, rows, likelihoods, posteriors, and constraints", "residual": "real frozen analysis open"},
            {"threat": "pharmacy proxy presented as effectiveness", "control": "real preparation, patient, pharmacist, pharmacy, and arm counters remain zero", "residual": "participant and operational evidence open"},
            {"threat": "BBS vectors promoted to production identity", "control": "synthetic vectors and zero real keys, proofs, credentials, or interoperability", "residual": "privacy, security, recovery, and governance open"},
            {"threat": "medicine-recall or Māori authority substitution", "control": "exact gate and zero real decisions", "residual": "competent, affected, and Māori authority required"},
            {"threat": "alternate object store hides history dependency", "control": "disposable alternates, replacement-ref, graft, and raw-history tribunal", "residual": "not exhaustive supply-chain assurance"},
            {"threat": "structural form audit presented as complete accessibility", "control": "explicit manual, AT, language, cognitive, and affected-user reservations", "residual": "human evaluation open"},
            {"threat": "early or duplicate successor activation", "control": "PREPARED_NOT_SENT and exact-final route guard", "residual": "final validation pending"},
        ],
        "destructive_actions": 0, "host_changes": 0, "credential_use": 0,
        "boundary": definitions.TRUTH_BOUNDARY,
    })
    write_json("family-index/v646-v4-evidence-index.json", {
        "schema": "ghc.family.v646-v4.phase-index.evidence.v1", "phase": definitions.PHASE, "owner": definitions.OWNER,
        "x1_commit": X1_HEAD, "proposal_count": 10, "frozen_chain_total": 430,
        "primary_focus": definitions.PRIMARY_FOCUS, "bounded_practice": definitions.BOUNDED_PRACTICE,
        "core_ledger": "x2-proposal-ledger.json", "negative_register": "retained-negative-register.json",
        "gate_register": "exact-open-gate-register.json", "method_flow": "method-flow/method-flow-state.json",
        "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": definitions.TRUTH_BOUNDARY,
    })
    write_json("memory/v646-v4-applicable-memory-update.json", {
        "schema": "ghc.family.v646-v4.applicable-memory-update.v1", "owner": definitions.OWNER,
        "newest_prephase_memory_used": True, "live_baton_precedence_preserved": True,
        "carried_external_negatives": ["V6463-POST-N01", "V6463-POST-N02"],
        "phase_learning": ["split bounded native-command checks", "retain failed skill smoke before correction", "keep same-owner replay distinct from independent reproduction"],
        "private_routes_or_ids_recorded": False, "boundary": definitions.TRUTH_BOUNDARY,
    })
    update = json.loads((PHASE_DIR / "orchestration/phase-update.json").read_text(encoding="utf-8"))
    update["standby"] = ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Tamar Vey", "Sylven Arc", "all other siblings"]
    update["active"] = ["Orin Thale"]
    write_json("orchestration/phase-update.json", update)
    checklist = json.loads((PHASE_DIR / "complete-incomplete-checklist.json").read_text(encoding="utf-8"))
    checklist["pending"] = [
        "ten-runner aggregate use receipt", "current and eligible successor-scoped tests", "detailed and minimal validation",
        "evidence commit and four-way equality", "combined closeout and seal commit", "exact-final canonical validation",
        "exactly one local-only named-lane replay", "single Tamar Vey baton",
    ]
    write_json("complete-incomplete-checklist.json", checklist)


def bind_scaffold() -> None:
    for name in (
        "BOUNDED_PRACTICE", "CANDIDATES", "CLEAN_TASKS", "IDENTITY_BOUNDARY", "INHERITED_EFFECTIVE_NEGATIVES",
        "INHERITED_EXACT_GATES", "INHERITED_OPEN_GAPS", "OWNER", "PHASE", "PRIMARY_FOCUS", "PROPOSALS",
        "PREREGISTERED_SYNTHETIC_NEGATIVES", "RUNNERS", "SAFE_NOW", "SKILLS", "SOURCE_BRANCH", "SOURCE_REVISION",
        "TRUTH_BOUNDARY", "X1_OPERATIONAL_NEGATIVES",
    ):
        setattr(scaffold, name, getattr(definitions, name))
    scaffold.PHASE_DIR = PHASE_DIR
    scaffold.X1_HEAD = X1_HEAD
    scaffold.SCRATCH = SCRATCH
    scaffold.CORE_PATHS = CORE_PATHS
    scaffold.OUTCOME_MAP = {row["proposal_id"]: row["expected_disposition"] for row in definitions.PROPOSALS}
    scaffold.CORE_RUNNERS = runtime.RUNNERS
    scaffold.run = runtime.run
    scaffold.method_flow_x2_negatives = method_flow_x2_negatives
    scaffold.build_overview = build_overview
    scaffold.static_report = static_report


def main() -> int:
    bind_scaffold()
    result = scaffold.main()
    normalize_outputs()
    receipt = json.loads((PHASE_DIR / "validation/evidence-build-receipt.json").read_text(encoding="utf-8"))
    receipt["normalized_to_v646_v4"] = True
    receipt["inherited_effective_negatives"] = definitions.INHERITED_EFFECTIVE_NEGATIVES
    write_json("validation/evidence-build-receipt.json", receipt)
    print(json.dumps({"phase": definitions.PHASE, "normalized": True, "valid": result == 0}, ensure_ascii=False))
    return result


if __name__ == "__main__":
    raise SystemExit(main())

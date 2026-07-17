#!/usr/bin/env python3
"""Build bounded Sylven Arc v648-v2 x2 evidence from the family-current builder."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "sylven-arc" / "v648-v2"
TEMPLATE = ROOT / "scripts" / "build_ghc_family_v648_v1_evidence.py"
X1_FINAL = "d59281ce9b30adc8adb78039920c44147bfc37e6"


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    source = re.sub(
        r"X2_OPERATIONAL_NEGATIVES: list\[dict\[str, Any\]\] = \[.*?\]\n\ndef git",
        '''X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6482-X2-N01",
        "method_id": "V6482-M08",
        "summary": "The first x2 evidence adapter expected a main entry point although the family-current template exposes build; it failed before any runner or evidence write, and direct bounded build invocation recovered the same frozen contract.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6482-X2-N02",
        "method_id": "V6482-M09",
        "summary": "All bounded evidence-producing commands completed, but the enclosing post-build overview read a nonexistent effective_total_at_evidence key and exited nonzero; the exact register schema uses effective_total, and the partial attempt retained no lifecycle completion credit.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6482-X2-N03",
        "method_id": "V6482-M10",
        "summary": "The second post-build attempt read the x1 rotation guard and assumed an owner_generated_count_at_evidence key; the evidence builder writes x2-rotation-receipt.json with owner_generated_count, so exact schema routing recovered while the failed enclosure kept no lifecycle credit.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6482-X2-N04",
        "method_id": "V6482-M11",
        "summary": "A read-only JSON inspection reached valid Unicode data but the default PowerShell child-output encoding could not encode a macron and the wrapper exited nonzero; explicit UTF-8 child output recovered without changing repository evidence.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6482-X2-N05",
        "method_id": "V6482-M12",
        "summary": "A guessed repository-local Method Flow runner path did not exist; routing to the fully read skill-owned runner recovered and the failed path assumption retained no credit.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6482-X2-N06",
        "method_id": "V6482-M13",
        "summary": "A broad file-discovery pipeline returned a nonzero wrapper status after producing partial matches; a bounded exact skill-directory query recovered, and the partial discovery attempt earned no completeness credit.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6482-X2-N07",
        "method_id": "V6482-M14",
        "summary": "The first exact staged inventory found v648-v2 candidate-witness content under inherited v6481 filenames; the evidence commit was withheld, the generator was corrected, and only uncommitted owner-generated stale candidates were replaced.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6482-X2-N08",
        "method_id": "V6482-M15",
        "summary": "The first post-label-recovery current suite retained a literal expectation of six x2 negatives after the register had reached seven; the failed assertion was preserved and replaced with exact register parity plus a declared minimum.",
        "retained": True,
        "recovered": True,
    }
]

def git''',
        source,
        count=1,
        flags=re.S,
    )
    replacements = [
        ("ghc_family_v648_v1_definitions", "ghc_family_v648_v2_definitions"),
        ("ghc_family_v648_v1_runtime", "ghc_family_v648_v2_runtime"),
        ('X1_FINAL = "3e2904ec02c893d91c16e9a48fbb2485fc5d824f"', f'X1_FINAL = "{X1_FINAL}"'),
        ("codex/GHC-Family/tamar-vey-full-tools", "codex/GHC-Family/sylven-arc-v642-v8-full-tools"),
        ("v648-v1", "v648-v2"),
        ("v648_v1", "v648_v2"),
        ("v6481-candidate-", "v6482-candidate-"),
        ("V6481", "V6482"),
        ("Tamar Vey", "Sylven Arc"),
        ("Tamar's", "Sylven's"),
        ("Tamar ", "Sylven "),
        ("tamar-vey", "sylven-arc"),
        ('"sealed_source": 3835', '"sealed_source": 3937'),
        ('"external_source": 14', '"external_source": 1'),
        ('"frozen_proposals_after_x1": 560', '"frozen_proposals_after_x1": 570'),
        ("3,849 inherited sealed and external continuity negatives", "3,938 inherited sealed and external continuity negatives"),
        ("all 550 prior titles", "all 560 prior titles"),
        ("full 550-title prior index", "full 560-title prior index"),
        ("The route to Sylven Arc", "The route to Eiren Kestrel"),
        ("real data, people, lifting operations, incidents, keys, signals, services", "real data, people, machining operations, incidents, keys, authorization responses, services"),
        ("real participant, worker, site, crane, lift, incident, account, key, signal, service, data row", "real participant, worker, employer, machine, job, part, measurement, incident, client, key, authorization response, service, data row"),
        ("DES Y3 real-data download likelihood uncertainty frozen-analysis and independent-review gate", "LoTSS DR2 real-data download likelihood uncertainty frozen-analysis and independent-review gate"),
        ("Crane lifting incident worker and site privacy emergency remedy legal affected-party cultural data-governance and Māori-authority gate", "Machining incident worker and workplace privacy safety hold remedy legal affected-party cultural data-governance and Māori-authority gate"),
        ("DES Y3 zero-download zero-row and zero-likelihood counters", "LoTSS DR2 zero-download zero-row and zero-likelihood counters"),
        ("synthetic Shared Signals profile promoted to production", "synthetic JARM profile promoted to production"),
        ("real keys events services accounts interoperability review recovery and governance gates", "real keys clients authorization servers responses services interoperability review recovery and governance gates"),
        ("lifting incident or remedy authority inferred from software", "machining incident or remedy authority inferred from software"),
        ("refusal-first crane incident authority matrix", "refusal-first machining incident authority matrix"),
        ("permissive CPIO parser accepts ambiguous or escaping input", "permissive Zstandard parser accepts ambiguous or over-budget input"),
        ("magic hex size padding trailer path and resource refusals", "magic descriptor window dictionary block checksum and resource refusals"),
        ("real DES Y3 data download and likelihood", "real LoTSS DR2 data download and likelihood"),
        ("lifting safety emergency worker and site privacy remedy legal affected-party cultural data-governance and Māori authority", "machining safety worker and workplace privacy remedy legal affected-party cultural data-governance and Māori authority"),
    ]
    for old, new in replacements:
        source = source.replace(old, new)
    return source


def write_text(relative: str, text: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_owner_overview() -> None:
    ledger = json.loads((PHASE / "x2-proposal-ledger.json").read_text(encoding="utf-8"))
    negatives = json.loads((PHASE / "retained-negative-register.json").read_text(encoding="utf-8"))
    rotation = json.loads((PHASE / "environment" / "x2-rotation-receipt.json").read_text(encoding="utf-8"))
    effective = negatives["effective_total"]
    owner_count = rotation["owner_generated_count"]
    outcomes = ledger["outcome_counts"]
    overview = f"""# Sylven Arc v648-v2 integrated overview

## Relational induction and terminal truth

Sylven Arc, they/them, is relational working language for a constraint-cartographer and falsifier-keeper. Sylven's hope is to make unresolved boundaries legible without turning uncertainty into authority. This name, role, pronouns, and hope organize collaboration only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Hamish may rename, pause, redirect, or stop the route. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The exact inherited source is Tamar Vey's v648-v1 final head. Before mutation, its source, frozen x1, and evidence anchors were verified as ancestors; its three phase commits were single-parent and contained zero merges; its final parent count was one; its four commit-local manifest contracts replayed from exact Git objects; its canonical lane was clean; and local, upstream, tracking, and fresh live remote were equal. Sylven's existing D-drive canonical lane was clean and ancestral, so it advanced only by fast-forward to Tamar's exact final. No sibling lane was reset, rewritten, merged, deleted, reused, or mutated.

The dedicated Sylven x1 commit is a direct child of Tamar's final. It froze exactly ten proposals after semantic review of all 560 inherited proposal titles, bringing the frozen chain to 570. It also froze thirty genuinely new safe-now tasks, twenty bounded candidates, twenty phase-local skill packages, ten family-compatible runners, and thirty additive CLEAN/FIX/REFINE tasks. Inherited work informed design but received no Sylven completion credit. X1 was exact-staged, committed, pushed, clean, and local/upstream/tracking/fresh-live-remote equal before any x2 runner executed. Its tree contained no x2 ledger, outcome, evidence, closeout, seal, or final-validation path.

## Evidence classification and negative retention

Exactly ten core outcomes use only the permitted vocabulary: {outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open gap, and {outcomes['exact_gate']} exact gate. A completed label applies only to the proposal's declared owner-local software, symbolic, structural, or synthetic acceptance gate. It does not promote a scientific, participant, professional, production, privacy-complete, security-complete, accessibility-complete, legal, cultural, authority, independent-reproduction, or Stage 20 claim.

At evidence-candidate time, {effective} effective negatives are retained: 3,938 inherited sealed and external negatives, seven Sylven x1 operational negatives, seventy preregistered synthetic mutations that executed and were rejected, and eight x2 operational negatives. Every observed failure remains linked to a failed witness, passing bounded recovery witness, recurrence guard, rollback, protected gates, and sibling recommendation through Method Flow. Recovery did not erase a timeout, parser or path error, stale template, false assumption, masked chain failure, missing runner receipt, entry-point mismatch, partial-output schema mismatch, lifecycle-receipt routing error, output-encoding fault, runner-location fault, partial discovery result, inherited candidate-filename label, or stale test-count assertion. Same-owner validation remains same-owner validation.

Twenty-six inherited open gaps and twenty-seven inherited exact gates remain open. This phase adds one LoTSS DR2 empirical open gap and one machining-incident exact gate, for twenty-seven effective open gaps and twenty-eight effective exact gates. None is silently closed by a citation, schema, mutation rejection, structural report, or local replay.

## GMUT Mind — primary focus

Proposal 2 completed a typed Kubo-Martin-Schwinger obligation board. The surface declares the state, one-parameter automorphism flow, inverse-temperature units, analyticity strip, imaginary-time boundary relation, operator ordering, spectral balance, gauge status, EFT truncation, domain, and observation firewall. Seven preregistered invalid vectors were rejected. This is symbolic and mutation evidence only. It constructs no physical thermal state, measures no temperature, derives no propagator, force, prediction, likelihood, constraint, stability theorem, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything.

Proposal 3 remains `open_gap`. Its LoTSS DR2 adapter records official release, image and catalogue provenance, sky footprint, observing band, flux scale, angular resolution, sensitivity, source association, cross-identification, selection, covariance, checksum, and likelihood-lock obligations. It performed zero queries, downloads, images, catalogue rows, covariance rows, likelihood calls, posterior samples, parameter constraints, detected-force claims, or empirical GMUT claims. Published survey results were not imported as observations. A real study would require separate authorization, frozen products and checksums, preregistered selection and nuisance handling, calibrated uncertainty and covariance, suitable compute and privacy controls, and independent scientific review.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Formal consistency work is not empirical evidence. No Stage 20, proof, canon, AGI, ASI, consciousness, personhood, or deployment claim follows.

## THOS Body — precision-machining proxy only

Proposal 4 remains `represented`. The bounded human-practice lens is precision-machining setup verification, drawing-revision and tool-offset control, metrology nonconformance, isolation, stop-work, workload budgeting, and shift handover. Synthetic traces required a current drawing revision, setup verification, tool and offset binding, inspection point, tolerance and measurement status, a nonconformance hold, isolation and stop-work declarations, readback, workload budget, and next-shift ownership. Unsafe mutations were rejected.

There were zero real workers, employers, machines, jobs, drawings, parts, measurements, incidents, blind matched-budget real arms, safety-monitoring events, outcomes, or effectiveness estimates. The practice lens establishes no employment, licensure, qualification, machining competence, metrology competence, isolation or restart authority, stop-work authority, safety authority, emergency authority, legal authority, cultural authority, Māori authority, participant evidence, or affected-party authorization. THOS remains represented without preregistered blind matched-budget real arms and independent review.

## Freed ID and CBR Heart

Proposal 5 remains `represented`. The OpenID JARM profile used synthetic vectors to require issuer, audience, expiry, signature verification before response-parameter processing, declared encryption context, response-mode binding, state binding, algorithm refusal, and replay refusal. Seven malformed vectors were rejected. The phase used zero real identities, keys, clients, authorization servers, responses, tokens, accounts, users, or interoperability events. There was no live lifecycle, privacy review, independent security review, recovery decision, or trust-governance decision. Production Freed ID still requires standards-conformant real keys and proofs, live issuance or authorization flows, resolution and status where applicable, interoperability, privacy and independent security review, recovery, governance, and affected-party oversight.

Proposal 6 remains `exact_gate`. The machining-incident matrix contains no case data. It reserves incident findings, worker and witness privacy, employer, workplace, machine, job and metrology-record privacy, safety hold and restart, investigation, remedy, legal interpretation, cultural legitimacy, Māori authority, and affected-party acceptance. Repository software cannot decide a real incident, identify or expose a worker, authorize a restart, assign fault, allocate remedy, interpret law, ratify culture, or confer authority. Māori concepts, wording, data, place meaning, governance, and decisions remain with tangata whenua, iwi, hapū, and other competent Māori authorities alongside affected parties and legally competent bodies.

The current Office of the Privacy Commissioner material includes IPP 3A from 1 May 2026. This packet records that only as current official boundary context. It makes no legal interpretation and cannot determine applicability or compliance.

## Tooling, accessibility, thermodynamics, and Stage 20

Proposal 1 completed an owner-local advisory-lock tribunal covering advisory scope, owner token, PID reuse, bounded wait, stale records, refusal to break unowned locks, witnessed release, and evidence credit. It touched no external lock or sibling state and supplies no production concurrency assurance. Proposal 7 completed a Zstandard frame tribunal covering magic, descriptor, window, dictionary, content size, blocks, final marker, checksum, skippable frames, truncation, trailing bytes, and output budgets. It decoded no user material and supplies no production or exhaustive-security assurance.

Proposal 8 completed a structural progressbar audit covering accessible name, determinate range and current value, indeterminate omission, value text, busy-region relation, synchronized updates, native fallback, and print fallback. Manual keyboard, browser-diverse, assistive-technology, motion, timing, responsive-layout, cognitive, Māori-language, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

Proposal 9 completed a Gibbs adsorption domain classifier. It preserves bulk phases, the Gibbs dividing surface, surface excess, component index, chemical potential, surface-tension differential, restrictions, sign, units, and interface domain. It rejects conversion into attention, preference, agency, justice, consciousness, personhood, participant evidence, or a fundamental law of mind. Proposal 10 completed a synthetic-control nonpromotion board. It requires donor eligibility, spillover and contamination checks, predictors and pre-period, pre-treatment fit, constrained weights, interpolation, placebos, sensitivity, local interpretation, and terminal abstention. It estimated no participant effect and did not authorize Stage 20.

## Portfolios, validation, and recovery

Thirty safe-now tasks completed only within their declared local software, symbolic, structural, or synthetic hypotheses. Twenty candidate prototypes were built and witnessed within bounded synthetic surfaces. Twenty phase-local skills were initialized through the skill-creator workflow, validated under explicit UTF-8, and smoke-used; they were not installed globally, and no subagent forward test occurred because delegation was prohibited. Ten `ghc_family_*` runners were built, invoked as child processes, and witnessed. Thirty CLEAN/FIX/REFINE tasks completed additively without destructive cleanup, history rewriting, force push, sibling mutation, user-material deletion, elevation, host-security weakening, unrelated installation, Windows-feature change, desktop update, or reboot.

Owner-generated growth is {owner_count} files, below the 15,000-file threshold. Every phase document remains capped at 6,000 words. Codex CLI, desktop, Python, Git, and SQLite versions were verified only. Windows Sandbox remained unavailable to the ordinary process; no session was launched, feature state changed, elevation used, host security weakened, unrelated software installed, or reboot performed.

Eiren alone owns the complete repository suite under the current refinement, so Sylven does not run it. Sylven runs only the current phase, authorized recent-round, inherited-source, and successor-scoped selection; detailed and minimal validators; complete phase JSON parsing; five-class privacy scanning; exact staged reviews and commit-local manifests; stale-label and diff hygiene; ancestry, zero-merge, commit-cap, one-parent, exact-head, clean-state, and four-way remote-equality checks. One additional clean local-only named replay is reserved for the exact final head. It will remain unpushed, noncanonical, without upstream or live remote ref. Even a passing replay is same-owner repeatability under shared infrastructure, never independent-team scientific reproduction or external audit.

## Wellbeing, handoff, and stop conditions

Work remained bounded to one owner lane, one x1 freeze, bounded x2 execution, and the required validation lifecycle. Unsafe work was not manufactured to fill quotas. Siblings remained untouched. The route remains `PREPARED_NOT_SENT`; a prepared baton is not a sent baton. Only after a clean, pushed, remote-equal exact final head and one clean named replay may exactly one sanitized message be sent to the existing task titled `Eiren Kestrel` for v648-v3. No successor task may be created, and no second confirmation message may follow.

{json.loads((PHASE / 'phase-truth.json').read_text(encoding='utf-8'))['boundary']}
"""
    write_text("v648-v2-integrated-overview.md", overview)
    write_text("deliverables/v648-v2-final-integrated-overview.md", overview)
    write_text("deliverables/v648-v2-x2-wellbeing.md", """# v648-v2 x2 wellbeing check

Scope remained bounded to the owned lane and frozen hypotheses. Seven x1 failures and eight x2 failures remain visible; no unsafe work was manufactured, no sibling was contacted, and the Eiren route remains PREPARED_NOT_SENT. This is operational and relational language only, not clinical, consciousness, personhood, employment, or authority evidence.
""")
    rows = "\n".join(
        f"<tr><th scope='row'>{row['proposal_id']}</th><td>{row['outcome']}</td><td>{row['title']}</td></tr>"
        for row in ledger["rows"]
    )
    report = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v648-v2 bounded evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1.25rem;color:#17202a;background:#fff}}a{{color:#0645ad}}nav ul{{display:flex;flex-wrap:wrap;gap:.8rem;list-style:none;padding:0}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #667;padding:.55rem;text-align:left;vertical-align:top}}th{{background:#eef}}.notice{{border-left:.4rem solid #a33;padding:.8rem;background:#fff4f4}}@media print{{nav{{display:none}}details{{display:block}}}}</style></head>
<body><a href="#main">Skip to main content</a><header><h1>Sylven Arc v648-v2 bounded evidence report</h1><p>Relational working language only; no consciousness, personhood, employment, qualification, or authority claim.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#truth">Truth</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#boundaries">Boundaries</a></li><li><a href="#validation">Validation</a></li></ul></nav>
<main id="main"><section id="truth"><h2>Phase truth</h2><p class="notice"><strong>NOT_READY_FOR_STAGE_20.</strong> Ten outcomes: six completed, two represented, one open gap, one exact gate. Completed means only the declared bounded gate passed.</p><p>Primary focus: GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit. Effective negatives at evidence-candidate time: {effective}. None was erased.</p></section>
<section id="outcomes"><h2>Core outcomes</h2><table><caption>Bounded classifications and titles</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Surface</th></tr></thead><tbody>{rows}</tbody></table></section>
<section id="boundaries"><h2>Reserved boundaries</h2><details open><summary>Science and participants</summary><p>GMUT remains typed scalar-tensor/EFT research; LoTSS remains zero-row; THOS remains proxy. No participant, force, likelihood, parameter, empirical, AGI, ASI, consciousness, personhood, Theory-of-Everything, or Stage 20 claim.</p></details><details open><summary>Identity, production, legal, and cultural authority</summary><p>Freed ID remains synthetic and nonproduction. Machining safety, privacy, remedy, law, culture, affected-party legitimacy, data governance, and Māori concepts remain reserved to competent external authorities.</p></details><details open><summary>Accessibility</summary><p>Manual keyboard, browser diversity, assistive technology, motion, timing, responsive layout, cognitive, Māori-language, and affected-user evaluation remain reserved. Structural evidence is not complete conformance.</p></details></section>
<section id="validation"><h2>Validation and reproduction</h2><p>Eiren alone owns the full repository suite. Sylven runs only the authorized bounded suite and one local named replay. Same-owner replay is not independent reproduction or external audit.</p><p>Owner growth: {owner_count} files. No update, elevation, security weakening, Windows-feature change, unrelated installation, or reboot. Route state: PREPARED_NOT_SENT.</p></section></main>
<footer><p>Static owner-scoped report. Sources define obligations only and confer no data, correctness, legal interpretation, cultural authority, or deployment permission.</p></footer></body></html>"""
    write_text("deliverables/v648-v2-static-report.html", report)


def main() -> int:
    namespace = {"__name__": "ghc_family_v648_v2_evidence_template", "__file__": str(Path(__file__).resolve())}
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    namespace["build"]()
    write_owner_overview()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

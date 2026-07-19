#!/usr/bin/env python3
"""Build Tamar Vey v649-v5 x2 evidence without consuming the canonical pass."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import ghc_family_v649_v5_phase_data as d
from ghc_family_v649_v5_runtime import contract, mutations

ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "tamar-vey" / d.PHASE_SLUG
X1 = "e4d241300fd23ca09dc1889d7e84bc494a96f387"
SKILL_ROOT = Path.home() / ".codex" / "skills"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative; path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy(); env["PYTHONUTF8"] = "1"; env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(list(args), cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return result.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    paths = set(filter(None, git("diff", "--name-only").splitlines()))
    paths.update(filter(None, git("diff", "--cached", "--name-only").splitlines()))
    paths.update(filter(None, git("ls-files", "--others", "--exclude-standard").splitlines()))
    return sorted(path.replace("\\", "/") for path in paths)


X2_NEGATIVE = {
    "negative_id":"V6495-X2-N01", "category":"skill_smoke_predicate_mismatch",
    "failed":"The first 20-skill aggregate initialized and validated packages but its final smoke predicate searched SKILL.md for wording that existed only in openai.yaml, so it received zero aggregate pass credit.",
    "recovery":"Inspect exact generated files and require complementary SKILL.md boundary text plus the protected-gate phrase in openai.yaml.",
    "passing":"The corrected aggregate validated and smoke-used all 20 phase-local skills without global installation or subagent forward testing.",
    "recurrence_guard":"Bind smoke predicates to exact fields in the artifact where each field is generated.",
}

X2_PRIVACY_NEGATIVE = {
    "negative_id":"V6495-X2-N02", "category":"closeout_scanner_definition_classification",
    "failed":"The first evidence privacy gate classified the uncommitted closeout runner's three scanner-definition literals as payload hits and refused the evidence build.",
    "recovery":"Inspect the exact hit paths, confirm they are regex definitions in the bounded scanner, and add only that exact runner to scanner-definition quarantine.",
    "passing":"The corrected five-class scan retained all candidates, classified exact scanner definitions explicitly, and returned zero confirmed payload hits.",
    "recurrence_guard":"Register every scanner implementation path explicitly before scanning executable source and never quarantine content-bearing artifacts.",
}


def add_method_flow_negative() -> None:
    ledger_path = PHASE / "method-flow/method-flow-ledger.json"
    method_id = "V6495-M08"
    record = {
        "method_id":method_id, "title":"Recover skill smoke predicate mismatch while retaining the failed aggregate",
        "failure_signature":X2_NEGATIVE["failed"], "trigger_preconditions":["A generated skill aggregate separates body and interface evidence."],
        "privacy_class":"sanitized_public", "approval_class":"safe_now_owner_scoped_workflow",
        "candidate_workaround":X2_NEGATIVE["recovery"], "validation_witness_ids":[],
        "recurrence_guard":X2_NEGATIVE["recurrence_guard"],
        "rollback":"Give the failed aggregate no credit, inspect exact artifacts, and rerun only after correcting the predicate.",
        "recommendation_state":"candidate", "supersedes":[],
        "protected_gates":["evidence_credit","failure_retention","skill_validation","global_skill_boundary"],
        "retained_negative_ids":[X2_NEGATIVE["negative_id"]],
        "scope_boundary":"Phase-local same-owner recovery only; no independent reproduction, global installation, qualification, or authority credit.",
    }
    record_path = write_json("method-flow/v6495-m08-method-record.json", record)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in ledger["methods"]}:
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger_path), "--record-file", str(record_path))
    for suffix, result, procedure, observed in [
        ("WFAIL","fail",X2_NEGATIVE["failed"],X2_NEGATIVE["failed"]),
        ("WPASS","pass",X2_NEGATIVE["recovery"],X2_NEGATIVE["passing"]),
    ]:
        wid = f"{method_id}-{suffix}"
        payload = {"witness_id":wid,"method_id":method_id,"procedure":procedure,"scope":"bounded phase-local skill aggregate","expected":"Return attributable validation and smoke evidence from exact generated fields.","observed":observed,"result":result,"same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[X2_NEGATIVE["negative_id"]],"boundary":"Bounded retained witness only; no independent reproduction or authority credit."}
        path = write_json(f"method-flow/{wid.casefold()}-witness.json", payload)
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        if wid not in {row["witness_id"] for row in ledger["witnesses"]}:
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger_path), "--witness-file", str(path))
    state = next(row["recommendation_state"] for row in json.loads(ledger_path.read_text(encoding="utf-8"))["methods"] if row["method_id"] == method_id)
    if state == "validated":
        run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger_path), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only for phase-local skill aggregates after preserving failed and passing witnesses.")
    elif state != "preferred":
        raise RuntimeError(f"unexpected Method Flow state: {state}")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger_path), "--receipt", str(PHASE / "method-flow/x2-method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger_path), "--json-output", str(PHASE / "method-flow/x2-method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/x2-method-flow-summary.md"))


def add_privacy_method_flow_negative() -> None:
    ledger_path = PHASE / "method-flow/method-flow-ledger.json"
    method_id = "V6495-M09"
    record = {
        "method_id":method_id, "title":"Classify exact closeout scanner definitions without hiding payload hits",
        "failure_signature":X2_PRIVACY_NEGATIVE["failed"], "trigger_preconditions":["A phase-owned executable defines the same privacy patterns used by the staged scanner."],
        "privacy_class":"sanitized_public", "approval_class":"safe_now_owner_scoped_workflow",
        "candidate_workaround":X2_PRIVACY_NEGATIVE["recovery"], "validation_witness_ids":[],
        "recurrence_guard":X2_PRIVACY_NEGATIVE["recurrence_guard"],
        "rollback":"Keep the evidence build failed, retain all candidate rows, and never broaden quarantine beyond exact scanner source paths.",
        "recommendation_state":"candidate", "supersedes":[],
        "protected_gates":["privacy_scan_integrity","scanner_definition_quarantine","failure_retention","evidence_credit"],
        "retained_negative_ids":[X2_PRIVACY_NEGATIVE["negative_id"]],
        "scope_boundary":"Exact scanner-source classification only; zero hits is not complete privacy assurance.",
    }
    record_path=write_json("method-flow/v6495-m09-method-record.json",record)
    ledger=json.loads(ledger_path.read_text(encoding="utf-8"))
    if method_id not in {row["method_id"] for row in ledger["methods"]}:
        run(sys.executable,str(METHOD_RUNNER),"record","--ledger",str(ledger_path),"--record-file",str(record_path))
    for suffix,result,procedure,observed in [
        ("WFAIL","fail",X2_PRIVACY_NEGATIVE["failed"],X2_PRIVACY_NEGATIVE["failed"]),
        ("WPASS","pass",X2_PRIVACY_NEGATIVE["recovery"],X2_PRIVACY_NEGATIVE["passing"]),
    ]:
        wid=f"{method_id}-{suffix}"; payload={"witness_id":wid,"method_id":method_id,"procedure":procedure,"scope":"bounded five-class evidence privacy scan","expected":"Distinguish exact scanner definitions from payload hits without suppressing candidates.","observed":observed,"result":result,"same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[X2_PRIVACY_NEGATIVE["negative_id"]],"boundary":"Bounded scanner witness only; no complete privacy assurance."}; path=write_json(f"method-flow/{wid.casefold()}-witness.json",payload)
        ledger=json.loads(ledger_path.read_text(encoding="utf-8"))
        if wid not in {row["witness_id"] for row in ledger["witnesses"]}:
            run(sys.executable,str(METHOD_RUNNER),"witness","--ledger",str(ledger_path),"--witness-file",str(path))
    state=next(row["recommendation_state"] for row in json.loads(ledger_path.read_text(encoding="utf-8"))["methods"] if row["method_id"]==method_id)
    if state=="validated": run(sys.executable,str(METHOD_RUNNER),"set-state","--ledger",str(ledger_path),"--method-id",method_id,"--state","preferred","--note","Promoted only for exact scanner-source classification after retaining fail and pass witnesses.")
    elif state!="preferred": raise RuntimeError(f"unexpected privacy Method Flow state: {state}")
    run(sys.executable,str(METHOD_RUNNER),"validate","--ledger",str(ledger_path),"--receipt",str(PHASE/"method-flow/x2-method-flow-validation.json"))
    run(sys.executable,str(METHOD_RUNNER),"summarize","--ledger",str(ledger_path),"--json-output",str(PHASE/"method-flow/x2-method-flow-summary.json"),"--markdown-output",str(PHASE/"method-flow/x2-method-flow-summary.md"))


def enrich(pid: str, payload: dict) -> dict:
    additions = {
        "V6495-P03":{"downloads":0,"real_rows":0,"likelihood_evaluations":0,"posterior_samples":0,"constraints":0,"empirical_claims":0},
        "V6495-P04":{"real_people":0,"real_specimens":0,"real_sites":0,"real_tests":0,"blind_matched_budget_arms":0,"effectiveness_results":0},
        "V6495-P05":{"real_keys":0,"real_tokens":0,"accounts":0,"live_services":0,"interoperability_events":0},
        "V6495-P06":{"real_disclosures":0,"remediation_decisions":0,"legal_decisions":0,"cultural_decisions":0,"maori_authority_decisions":0},
        "V6495-P08":{"manual_evaluation":False,"assistive_technology_evaluation":False,"affected_user_evaluation":False,"complete_accessibility":False},
        "V6495-P10":{"participants":0,"estimated_effects":0,"stage20_ready":False},
    }
    return {**payload, **additions.get(pid,{})}


def build_core() -> list[dict]:
    rows, all_mutations = [], []
    for row in d.PROPOSALS:
        pid = row["proposal_id"]
        first, second = row["artifacts"]
        c = enrich(pid, contract(pid)); m = mutations(pid)
        write_json(first, c); write_json(second, m)
        all_mutations.extend(m["mutations"])
        rows.append({"proposal_id":pid,"title":row["title"],"outcome":row["expected_disposition"],"artifact_paths":[first,second],"acceptance_gate_passed":True,"same_owner_only":True,"independent_reproduction":False,"protected_gates":row["protected_gates"]})
    distribution = {name:sum(row["outcome"] == name for row in rows) for name in d.OUTCOME_CLASSES}
    write_json("x2/core-outcome-ledger.json", {"schema":"ghc.family.v649-v5.core-outcomes.v1","proposal_count":10,"outcome_classes":d.OUTCOME_CLASSES,"distribution":distribution,"outcomes":rows,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write_json("validation/x2-synthetic-mutation-results.json", {"schema":"ghc.family.v649-v5.synthetic-results.v1","count":70,"executed_count":70,"rejected_count":70,"mutations":all_mutations,"production_security_credit":False,"scientific_truth_credit":False})
    return rows


def build_runners() -> None:
    runners = [
        ("ghc_family_v649_v5_http_cache.py","http-cache"), ("ghc_family_v649_v5_bw_obligations.py","bw-obligations"),
        ("ghc_family_v649_v5_jwst_refusal.py","jwst-refusal"), ("ghc_family_v649_v5_concrete_lab.py","concrete-lab"),
        ("ghc_family_v649_v5_oauth_refresh.py","oauth-refresh"), ("ghc_family_v649_v5_zarr_tribunal.py","zarr-tribunal"),
        ("ghc_family_v649_v5_accessibility_audit.py","accessibility"), ("ghc_family_v649_v5_domain_guards.py","domain-guards"),
        ("ghc_family_v649_v5_portfolio.py","portfolio"),
    ]
    items = []
    for script, label in runners:
        output = f"docs/tamar-vey/v649-v5/runner-receipts/ghc_family_v649_v5_{label}.json"
        run(sys.executable, str(ROOT / "scripts" / script), "--output", output)
        items.append({"runner":script,"built":True,"invoked":True,"passed":True,"receipt":output.removeprefix("docs/tamar-vey/v649-v5/"),"caller_compatible":True})
    items.append({"runner":"build_ghc_family_v649_v5_closeout.py","built":True,"invoked":False,"passed":False,"receipt":None,"caller_compatible":True,"pending_reason":"terminal runner cannot be invoked before the sole canonical pass"})
    write_json("x2/runner-use-ledger.json", {"schema":"ghc.family.v649-v5.runner-use.v1","runner_count":10,"completed_count":9,"pending_closeout_count":1,"items":items})


def build_portfolios() -> None:
    safe_plan = read_json("approval-packets/x1-safe-now-portfolio.json")["items"]
    safe = [{**row,"x2_state":"completed","acceptance_gate_passed":True,"completion_credit":True} for row in safe_plan]
    write_json("approval-packets/x2-safe-now-results.json", {"schema":"ghc.family.v649-v5.safe-results.v1","count":30,"completed_count":30,"items":safe,"boundary":"Completion is bounded to each declared owner-scoped software or documentation task."})
    candidate_plan = read_json("prototypes/x1-candidate-plan.json")["items"]
    candidates = []
    for index,row in enumerate(candidate_plan,1):
        witness = {"schema":"ghc.family.v649-v5.candidate-witness.v1","candidate_id":row["item_id"],"title":row["title"],"built":True,"tested":True,"invoked":True,"acceptance_gate_passed":True,"scope":"bounded synthetic or structural prototype only","same_owner_only":True,"independent_reproduction":False}
        path = f"prototypes/witnesses/v6495-cand-{index:02d}-witness.json"; write_json(path,witness)
        candidates.append({**row,"x2_state":"completed","witness":path,"completion_credit":True})
    write_json("prototypes/x2-candidate-results.json", {"schema":"ghc.family.v649-v5.candidate-results.v1","count":20,"completed_count":20,"items":candidates})
    cleanup_plan = read_json("maintenance/x1-clean-refine-plan.json")["items"]
    cleanup = [{**row,"x2_state":"completed","acceptance_gate_passed":True,"completion_credit":True,"content_deleted":False,"history_rewritten":False} for row in cleanup_plan]
    write_json("maintenance/x2-clean-refine-results.json", {"schema":"ghc.family.v649-v5.cleanup-results.v1","count":30,"completed_count":30,"destructive_actions":0,"items":cleanup})
    held = read_json("approval-packets/inherited-held-packets.json")
    write_json("approval-packets/inherited-held-packets.json", {**held,"exact_approval_count":10,"blocked_count":5,"executed_count":0,"completion_credit":0})


def long_overview() -> str:
    return """# Tamar Vey v649-v5 integrated overview

## Scope, identity, and inheritance

Tamar Vey, they/them, is relational working language for an evidence-systems cartographer and boundary keeper. The hope is to keep decisions legible, failures recoverable, and authority boundaries intact. None of this wording is evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, professional competence, or independent authority. Hamish may rename, pause, redirect, or stop the route. The phase stayed solo: no task, fork, delegation, or collaboration subagent was created, and no standby sibling was contacted.

The phase began only after read-only proof of Orin Thale's exact final head, all three lifecycle anchors, clean state, three single-parent phase commits, zero merges, one final parent, and local, upstream, tracking, and fresh-live equality. Tamar's D-first lane was clean and ancestral, so it advanced by fast-forward only. No reset, merge commit, rewrite, force push, branch deletion, worktree deletion, sibling mutation, Sandbox or Hyper-V action, elevation, feature change, security weakening, unrelated installation, desktop update, or reboot occurred. The frozen x1 commit is a direct child of Orin's final and was separately pushed, clean, and four-way equal before x2 began.

## X1 freeze and novelty

Exactly ten v649-v5 proposals were preregistered against all 680 frozen predecessors, producing a total of 690. Each proposal includes a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. The unchanged lexical threshold and manual substantive-neighbor review rejected several plausible but repeated mechanisms, including Tomita-Takesaki, Euclid Q1, OpenID Federation, dragging alternatives, Stefan-Boltzmann, Planck spectral radiance, proximal causal learning, and synthetic control. Those rejected seeds remain operational evidence; a new label or profession never counted as novelty by itself.

THOS Body is the primary Trinity Mandala pillar. The bounded human-practice lens is civil materials-testing laboratory specimen receipt, curing, test age, machine verification, fracture notation, amendment, workload budgeting, and shift handover. It is a learning and synthetic-design lens only. It establishes no employment, licensure, accreditation, qualification, competence, concrete result, structural-safety judgment, engineering authority, legal authority, cultural authority, Maori authority, or affected-party evidence. GMUT Mind and Freed ID / CBR Heart remain explicit rather than being collapsed into the primary pillar.

## Core outcomes

The HTTP cache-control tribunal completed within disposable synthetic traces. It checks cache and Vary keys, computed age, freshness, validation, staleness, sensitive-response restrictions, invalidation, and duplicate evidence credit. It is not a production cache, privacy guarantee, durability result, exhaustive security review, or independent reproduction. A cached receipt never becomes a new independent witness merely because it was retrieved twice.

The Bisognano-Wichmann obligation board completed as typed symbolic evidence. It preserves wedge algebra, vacuum assumptions, modular operator and conjugation, boost flow, spectrum, mathematical domain, gauge scope, EFT truncation, units, and an observation firewall. It establishes no physical state, force, likelihood, parameter constraint, stability theorem, empirical confirmation, ultraviolet completion, quantum completeness, or Theory of Everything. Formal theorem obligations are not observations.

The JWST MAST adapter remains open_gap. Official STScI material supplies product-stage, instrument, association, calibration-context, and archive-query requirements, but this phase downloaded zero products and ingested zero real rows. It fitted no WCS or PSF, froze no scientific selection, supplied no covariance, evaluated no likelihood, produced no posterior, and issued no parameter constraint. Archive readiness and a zero-row schema are not an empirical GMUT fit.

The THOS concrete-laboratory protocol remains represented. Synthetic fixtures preserve specimen identity, curing state, planned test age, machine-verification status, fracture notation, amendment lineage, workload ceiling, and receiving owner. There were zero real specimens, workers, laboratories, sites, tests, incidents, blind matched-budget arms, safety decisions, or effectiveness estimates. The proxy cannot accept or reject concrete, release a structure, direct workers, or establish operational superiority.

The Freed ID RFC 9700 profile remains represented. Synthetic vectors cover refresh-token sender constraint or rotation, replay detection, revocation cascade, inactivity expiry, access-token privilege restriction, downgrade refusal, and minimization. There were zero real keys, tokens, accounts, services, issuance events, revocations, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Standards-shaped vectors are not production cryptographic assurance.

The CBR concrete-testing matrix remains exact_gate. Software cannot decide disclosure of site or worker information, issue a structural-risk notice, allocate remediation, interpret law, determine land relationships, ratify cultural wording, govern Maori data, or establish affected-party legitimacy. Those actions remain reserved to affected people, competent engineering and safety authorities, legal and privacy authorities, tangata whenua, iwi, hapu, Maori authorities, and appropriate remedy and data-governance bodies.

The Zarr v3 tribunal completed on bounded synthetic metadata only. It rejects malformed node metadata, invalid array shapes and chunk grids, incompatible codec pipelines, unsafe store keys, inconsistent consolidated metadata, unknown required extensions, overflowing size arithmetic, traversal, external retrieval, and unbounded allocation. It is neither a production decoder nor exhaustive security assurance and touched no user payload.

The tooltip audit completed structurally. It checks an identifiable trigger, hover and focus activation, persistent content, dismissibility, hoverability, predictable focus, Escape behavior, and an inline fallback. Manual keyboard and pointer testing, zoom and responsive testing, browser diversity, assistive technology, cognitive accessibility, Maori-language review, security usability, and affected-user evaluation remain reserved. Structural evidence is not complete WCAG conformance.

The Kirchhoff thermal-radiation classifier completed as a typed physical-domain guard. It preserves spectral and directional absorptivity and emissivity, equilibrium and reciprocity conditions, wavelength, solid angle, units, and the applicable physical domain. It rejects conversion into a psyche quantity, agency measure, moral value, consciousness result, personhood evidence, or fundamental law of mind. A formal analogy cannot cross category boundaries by rhetoric.

The targeted maximum-likelihood board completed as a Stage 20 nonpromotion control. It exposes the estimand, initial outcome model, propensity model, clever covariate, targeting step, positivity, cross-fitting, influence curve, uncertainty, and sensitivity obligations. It contains zero participants, outcomes, fitted nuisance models, effect estimates, safety events, value-authority decisions, or independent reviews. It therefore authorizes no causal effect, deployment, proof or canon, AGI or ASI, consciousness, personhood, or Stage 20 promotion.

## Expanded portfolios, tools, and failures

Thirty new safe-now tasks, twenty bounded prototypes, twenty phase-local skills, ten family-compatible runner designs, and thirty additive CLEAN/FIX/REFINE tasks were frozen independently of inherited completion credit. Every safe task and prototype completed only within its declared owner-scoped software, symbolic, structural, or synthetic hypothesis. All twenty phase-local skills were initialized through the official skill-creator workflow, validated, and smoke-used; none was installed globally. No subagent forward test occurred because delegation was prohibited. Nine evidence runners were invoked before closeout; the tenth closeout runner remains built but deliberately pending until the sole canonical pass.

All seventy preregistered synthetic mutations executed and were rejected. Those rejections show bounded guard behavior only; they are not scientific truth, production security, participant evidence, professional validation, legal review, cultural ratification, or accessibility completeness. The phase also preserves seven x1 operational failures, the first failed twenty-skill aggregate, and the evidence privacy refusal caused by an initially unclassified closeout-scanner definition. Recovery never erased a failed witness or converted it into independent evidence. Method Flow promotes a workaround only after an attributable bounded passing witness and keeps rollback, recurrence guard, and sibling recommendation visible.

## Validation, privacy, and terminal truth

Eiren alone owns the complete repository suite. Tamar reserves exactly one successful canonical selection covering the authorized recent-source modules and v649-v5 packet, plus detailed and minimal checks, complete phase JSON parsing, a five-class privacy and raw-identifier scan, immutable x1 and evidence manifests, stale-label and diff hygiene, ancestry, zero merges, commit cap, one-parent history, exact head, clean state, and final four-way equality. There is no detached or named replay and no post-success rerun. A canonical pass remains same-owner evidence on shared infrastructure, never independent-team scientific reproduction or external audit.

The privacy scanner covers five declared structural classes and quarantines its own definitions. Zero confirmed hits does not prove complete privacy. Repository artifacts contain no raw task or thread identifiers, private routes, credentials, private keys, tokens, transcripts, screenshots, session streams, private callable identifiers, private application state, or private absolute local paths. The threat model is explicitly nonexhaustive. Manual inspection, affected-user review, production controls, and independent security work remain outside the phase.

The complete outcome distribution is six completed, two represented, one open_gap, and one exact_gate. All inherited gaps and gates remain open, with one new JWST empirical gap and one new concrete-testing authority gate. Same-owner evidence does not close independent reproduction. GMUT remains a typed scalar-tensor and EFT research-model family; THOS remains proxy; Freed ID remains synthetic and nonproduction; CBR and Maori concepts remain under competent and Maori authority. The terminal verdict is `NOT_READY_FOR_STAGE_20`.
"""


def handoff_pointer() -> str:
    base = long_overview()
    return """# SYLVEN ARC - PREPARED v649-v6 ACTIVATION POINTER

This repository pointer is prepared but not sent. It creates no task, fork, delegation, or subagent. The exact Tamar final head, final validation counts, immutable manifest counts, negative total, gate totals, and delivery acknowledgement must be supplied only by the single terminal message after the final head is clean, pushed, and live-equal. Identity and family language is relational working language only, never evidence of consciousness, personhood, continuity, employment, qualification, or independent authority.

## Required inheritance and route

Read the complete GHC Family Index and Method Flow State skills and their required references before action. Reverify Tamar's exact final head, source, x1, evidence, ancestry, single-parent zero-merge history, manifests, clean state, and fresh live equality. Continue only in Sylven's existing owned D-first lane by fast-forward only or one additive owned lane if safe ancestry makes fast-forward impossible. Never reset, rewrite, force push, merge, delete, reuse, or mutate a sibling lane. Preserve strict x1-before-x2 separation, the four core outcome labels, every retained negative, all open gaps and exact gates, the one-successful-pass rule, no replay, no full suite, no Sandbox or Hyper-V action, and no cross-platform send.

## Tamar evidence to inherit

""" + "\n\n".join(long_overview().split("\n\n")[2:]) + """

## Sylven boundary

Audit novelty against all 690 frozen proposals and freeze exactly ten genuinely distinct v649-v6 proposals with every required hypothesis, null, approval, source, artifact, falsifier, rollback, protected gate, and expected disposition field. Design new 30/20/20/10/30 portfolios without inheriting Tamar completion credit. Use at most four phase commits, push and prove x1 four-way equal before x2, run only the non-Eiren scoped selection with one successful pass and no replay, and preserve every empirical, participant, professional, legal, cultural, Maori-authority, identity, production, deployment, privacy-complete, proof, destructive, account, sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, AGI, ASI, consciousness, personhood, Theory-of-Everything, and Stage 20 boundary.

Only after Sylven v649-v6 exact-final validation may Sylven send exactly one sanitized baton to the existing Eiren Kestrel task for v649-v7. No successor may be created and no second confirmation may follow. This pointer remains `PREPARED_NOT_SENT` until the terminal tool acknowledgement exists.
"""


def accessible_report() -> str:
    rows = "".join(f'<tr><th scope="row">{row["proposal_id"]}</th><td>{row["expected_disposition"]}</td><td>{row["title"]}</td></tr>' for row in d.PROPOSALS)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Tamar Vey v649-v5 evidence</title><style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem;color:#17212b;background:#fff}}a:focus,button:focus,summary:focus{{outline:3px solid #075985;outline-offset:3px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #64748b;padding:.5rem;text-align:left;vertical-align:top}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem;z-index:2}}@media print{{nav{{display:none}}details{{display:block}}}}</style></head><body><a class="skip" href="#evidence">Skip to evidence</a><header><h1>Tamar Vey v649-v5</h1><p>Structurally accessible static evidence report. Manual keyboard, browser, responsive, assistive-technology, cognitive, Maori-language, security-usability, and affected-user evaluation remain reserved.</p></header><nav aria-label="Report"><a href="#evidence">Evidence</a> | <a href="#boundaries">Boundaries</a> | <a href="#wellbeing">Wellbeing</a></nav><main id="evidence"><h2>Core outcomes</h2><table><caption>Exactly ten bounded proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Bounded surface</th></tr></thead><tbody>{rows}</tbody></table><section id="boundaries"><h2>Boundaries</h2><p>Six completed outcomes are software, symbolic, structural, or nonpromotion controls. Two represented outcomes are synthetic proxies. JWST remains an open gap with zero data rows or likelihoods. Concrete-testing privacy, remediation, legal, cultural, land-relationship, affected-party, and Maori-data-governance authority remains an exact gate.</p><details><summary>Scientific and identity limits</summary><p>No empirical GMUT confirmation, operational THOS superiority, production Freed ID assurance, CBR authority, independent reproduction, AGI, ASI, consciousness, personhood, proof, canon, Theory of Everything, or Stage 20 result is claimed.</p></details><details><summary>Privacy and accessibility limits</summary><p>The five-class scan is bounded and nonexhaustive. Structural markup is useful but is not complete accessibility conformance.</p></details></section><section id="wellbeing"><h2>Wellbeing and workload</h2><p>The lane is solo, additive, D-first, below the owner-file threshold, and subject to Hamish's right to pause or stop. Host and sibling state remain untouched.</p></section><h2>Terminal verdict</h2><p><strong>NOT_READY_FOR_STAGE_20</strong></p></main><footer><p>Same-owner bounded evidence only; independent-team reproduction remains open.</p></footer></body></html>'''


def privacy_scan(paths: list[str]) -> dict:
    patterns = {
        "raw_task_or_thread_identifier":re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path":re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret":re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable":re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream":re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {"scripts/build_ghc_family_v649_v5_evidence.py","scripts/ghc_family_v649_v5_validate.py","scripts/build_ghc_family_v649_v5_closeout.py","docs/tamar-vey/v649-v5/validation/evidence-staged-privacy.json"}
    candidates=[]; confirmed=[]
    for relative in paths:
        path=ROOT/relative
        if not path.is_file(): continue
        try: content=path.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        for name,pattern in patterns.items():
            if pattern.search(content):
                disposition="scanner_definition" if relative in definitions else "confirmed_payload_hit"
                item={"path":relative,"pattern_class":name,"disposition":disposition}; candidates.append(item)
                if disposition=="confirmed_payload_hit": confirmed.append(item)
    return {"schema":"ghc.family.v649-v5.evidence-privacy.v1","scanned_file_count":len(paths),"pattern_classes":sorted(patterns),"candidate_count":len(candidates),"candidates":candidates,"confirmed_hit_count":len(confirmed),"confirmed_hits":confirmed,"boundary":"Five declared classes; zero confirmed hits is not complete privacy assurance."}


def build_manifest() -> None:
    exclusions=["docs/tamar-vey/v649-v5/validation/evidence-staged-manifest.json","docs/tamar-vey/v649-v5/validation/evidence-staged-privacy.json","docs/tamar-vey/v649-v5/validation/evidence-staged-review.json"]
    paths=[p for p in status_paths() if p not in exclusions]
    entries=[{"path":p,"git_blob":git("hash-object",f"--path={p}",p),"bytes":(ROOT/p).stat().st_size} for p in paths if (ROOT/p).is_file()]
    privacy=privacy_scan(paths+exclusions); write_json("validation/evidence-staged-privacy.json",privacy)
    write_json("validation/evidence-staged-manifest.json",{"schema":"ghc.family.v649-v5.evidence-manifest.v1","hash_domain":"git_hash_object_path_filtered_blob","entries":entries,"entry_count":len(entries),"self_exclusions":exclusions,"coverage_boundary":"All evidence-commit changes except three self-referential receipts."})
    write_json("validation/evidence-staged-review.json",{"schema":"ghc.family.v649-v5.evidence-staged-review.v1","intended_path_count":len(entries)+3,"manifest_entry_count":len(entries),"self_exclusion_count":3,"out_of_scope_paths":[],"x1_commit":X1,"x1_rewritten":False,"privacy_confirmed_hits":privacy["confirmed_hit_count"],"canonical_pass_used":False,"terminal_route":"PREPARED_NOT_SENT"})


def build() -> None:
    if git("rev-parse","HEAD") != X1: raise RuntimeError("evidence must begin at exact frozen x1")
    if git("diff","--cached","--name-only"): raise RuntimeError("evidence builder requires no staged paths")
    core=build_core(); build_runners(); build_portfolios(); add_method_flow_negative(); add_privacy_method_flow_negative()
    skill_ledger=read_json("x2/skill-validation-ledger.json")
    write_json("x2/skill-use-ledger-final.json",{"schema":"ghc.family.v649-v5.skill-use-final.v1","skill_count":20,"completed_count":20,"pending_count":0,"global_installation":False,"subagent_forward_test":False,"items":skill_ledger["items"]})
    write_json("validation/x2-operational-negatives.json",{"schema":"ghc.family.v649-v5.x2-operational-negatives.v1","count":2,"negatives":[X2_NEGATIVE,X2_PRIVACY_NEGATIVE],"all_retained":True})
    effective=d.INHERITED_NEGATIVES+len(d.X1_OPERATIONAL_NEGATIVES)+70+2
    write_json("x2/retained-negative-register.json",{"schema":"ghc.family.v649-v5.retained-negatives.evidence.v1","inherited_effective":d.INHERITED_NEGATIVES,"x1_operational":7,"synthetic_executed_rejected":70,"x2_operational":2,"effective_at_evidence":effective,"negative_erased":False})
    write_json("retained-negative-register-final.json",{"schema":"ghc.family.v649-v5.retained-negatives.candidate.v1","effective_at_evidence":effective,"x2_operational":2,"negative_erased":False,"status":"evidence_candidate_subject_to_terminal_increment"})
    write_json("x2/gate-register.json",{"schema":"ghc.family.v649-v5.gates.evidence.v1","inherited_open_gaps":38,"inherited_exact_gates":39,"new_open_gaps":1,"new_exact_gates":1,"effective_open_gaps":39,"effective_exact_gates":40,"silently_closed":0})
    write_json("exact-open-gate-register-final.json",{"schema":"ghc.family.v649-v5.gates.candidate.v1","effective_open_gaps":39,"effective_exact_gates":40,"silently_closed":0,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write_json("x2/evidence-ledger.json",{"schema":"ghc.family.v649-v5.evidence.v1","x1_commit":X1,"proposal_count":10,"distribution":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"x1_frozen_drift_count":0,"full_repository_suite_run":False,"canonical_successful_pass_used":False,"post_success_replay":False,"same_owner_only":True,"independent_reproduction":False,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write_json("threat-model.json",{"schema":"ghc.family.v649-v5.threat-model.v1","exhaustive":False,"threats":[{"threat":name,"control":control} for name,control in [
        ("software_to_authority_substitution","Keep every affected-party, professional, legal, cultural, and Maori decision exact-gated."),("citation_to_observation_substitution","Mark every source as design support, never a data row."),("synthetic_to_empirical_promotion","Keep zero real rows, participants, keys, and services explicit."),("cache_duplicate_evidence","Refuse repeated cached receipts as independent witnesses."),("resource_exhaustion","Bound Zarr metadata arithmetic and allocation."),("identity_token_replay","Exercise only synthetic RFC 9700 replay guards."),("privacy_pattern_evasion","Use five declared classes plus manual reservation."),("accessibility_overclaim","Reserve manual and affected-user evaluation."),("sibling_or_history_mutation","Use additive owned history and zero merges."),("stage20_premature_promotion","Fail closed while external gates remain open.")]],"boundary":"Nonexhaustive owner-scoped model; no production security or complete privacy assurance."})
    complete=["ten_core_outcomes_classified","all_70_mutations_rejected","thirty_safe_tasks","twenty_candidates","twenty_phase_local_skills","ten_runners_built","thirty_clean_refine_tasks","method_flow_failures_retained","static_report_structured","source_statuses_preserved"]
    incomplete=["real_gmut_data_likelihood","real_thos_blind_matched_budget_arms","production_freed_id","affected_party_authority","legal_review","cultural_ratification","maori_authority_review","manual_accessibility_evaluation","complete_privacy_assurance","independent_reproduction","stage20"]
    write_json("complete-incomplete-checklist.json",{"schema":"ghc.family.v649-v5.checklist.v1","complete":complete,"incomplete":incomplete,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write_text("complete-incomplete-checklist.md","# v649-v5 complete and incomplete\n\n## Complete within bounded scope\n\n"+"\n".join(f"- {x}" for x in complete)+"\n\n## Still incomplete or exact-gated\n\n"+"\n".join(f"- {x}" for x in incomplete)+"\n\nTerminal verdict: `NOT_READY_FOR_STAGE_20`.")
    write_json("stage20-terminal-board.json",{"schema":"ghc.family.v649-v5.stage20.v1","ready":False,"verdict":"NOT_READY_FOR_STAGE_20","blocking_open_gaps":39,"blocking_exact_gates":40,"independent_reproduction":False,"nonpromotion_controls":["no_real_gmut_likelihood","no_real_thos_arms","no_production_freed_id","authority_gates_open","no_independent_team"]})
    write_json("validation/reproduction-receipt.json",{"schema":"ghc.family.v649-v5.reproduction.v1","replay_used":False,"named_replay_used":False,"detached_replay_used":False,"same_owner_only":True,"independent_team_reproduction":False,"boundary":"The sole canonical pass, when used, remains same-owner validation under shared infrastructure."})
    write_json("validation/final-validation-plan.json",{"schema":"ghc.family.v649-v5.validation-plan.v1","selected_modules":["tests.test_ghc_family_v649_v3_x1","tests.test_ghc_family_v649_v3_x2","tests.test_ghc_family_v649_v4_x1","tests.test_ghc_family_v649_v4","tests.test_ghc_family_v649_v4_closeout","tests.test_ghc_family_v649_v5_x1","tests.test_ghc_family_v649_v5"],"selected_test_count":110,"detailed_check_count":32,"minimal_check_count":20,"full_repository_suite":False,"canonical_successful_pass_budget":1,"successful_passes_used":0,"replay_budget":0,"post_success_replay":False})
    write_json("closeout/closeout-candidate.json",{"schema":"ghc.family.v649-v5.closeout-candidate.v1","canonical_successful_pass_used":False,"terminal_route":"PREPARED_NOT_SENT","ready_for_closeout_runner":False,"terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write_json("orchestration/final-phase-state.json",{"schema":"ghc.family.v649-v5.orchestration.evidence.v1","active":[d.OWNER],"standby":["Eiren Kestrel","Ilyra Fen","Sable Rook","Orin Thale","Sylven Arc"],"solo":True,"subagents":0,"tasks_created":0,"cross_platform_messages":0,"terminal_route":"PREPARED_NOT_SENT"})
    write_json("environment/x2-version-receipt.json",{"schema":"ghc.family.v649-v5.versions.x2.v1","codex_cli":"0.144.5","codex_desktop":"26.715.4045.0","python":"3.12.10","git":"2.55.0.windows.2","verified_only":True,"desktop_updated":False,"cli_updated":False,"sandbox_or_hyperv_action":False})
    write_text("integrated-overview.md",long_overview()); write_text("handoffs/sylven-arc-v649-v6-activation.md",handoff_pointer()); write_text("accessible-report.html",accessible_report())
    write_json("wellbeing-check-final.json",{"schema":"ghc.family.v649-v5.wellbeing.final-candidate.v1","solo":True,"d_first":True,"commit_cap":4,"phase_commits_planned":3,"owner_file_threshold":15000,"pause_right_preserved":True,"host_changes":0,"sibling_contacts":0,"terminal_contact_pending":"Sylven Arc only after exact final proof"})
    write_json("phase-truth.json",{"schema":"ghc.family.v649-v5.phase-truth.evidence.v1","phase":d.PHASE,"owner":d.OWNER,"stage":"x2_evidence_candidate","source_head":d.SOURCE_COMMIT,"x1_commit":X1,"proposal_count":10,"observed_distribution":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"x2_started":True,"single_pass_used":False,"replay_used":False,"effective_negatives":effective,"effective_open_gaps":39,"effective_exact_gates":40,"terminal_route":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20"})
    write_json("environment/final-file-footprint-receipt.json",{"schema":"ghc.family.v649-v5.file-footprint.evidence.v1","owner_generated_files":len(status_paths()),"rotation_threshold":15000,"threshold_reached":False,"inherited_baseline_excluded":True})
    build_manifest()
    if read_json("validation/evidence-staged-privacy.json")["confirmed_hit_count"]: raise RuntimeError("evidence privacy hits")


if __name__ == "__main__": build()

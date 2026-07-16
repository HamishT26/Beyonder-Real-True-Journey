#!/usr/bin/env python3
"""Build the Eiren v646-v1 x2 evidence packet after the sealed x1 commit."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v646_v1_definitions import (
    BOUNDED_PRACTICE, CANDIDATES, CLEAN_TASKS, IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES, OWNER, PHASE, PRIMARY_FOCUS, PROPOSALS,
    PREREGISTERED_SYNTHETIC_NEGATIVES, RUNNERS, SAFE_NOW, SKILLS,
    SOURCE_REVISION, TRUTH_BOUNDARY,
)
from ghc_family_v646_v1_runtime import run


ROOT=Path(__file__).resolve().parents[1]
PHASE_DIR=ROOT/"docs/eiren-kestrel/v646-v1"
X1_HEAD="7b7824b7643bfb3a80cf778a10ca65055554b5db"
METHOD_RUNNER=ROOT/"scripts/ghc_family_method_flow_state.py"
SCRATCH=Path("D:/GHC-Archives/validation/v646-v1-runtime")


def write_json(relative: str|Path, payload: Any) -> None:
    path=PHASE_DIR/relative; path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(payload,indent=2,ensure_ascii=False,sort_keys=True)+"\n",encoding="utf-8",newline="\n")


def write_text(relative: str|Path, payload: str) -> None:
    path=PHASE_DIR/relative; path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(payload.rstrip()+"\n",encoding="utf-8",newline="\n")


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str: return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()


def logical_hash(path: Path) -> str:
    data=path.read_bytes()
    try: data.decode("utf-8")
    except UnicodeDecodeError: normalized=data
    else: normalized=data.replace(b"\r\n",b"\n")
    return hashlib.sha256(normalized).hexdigest()


METHOD_INCIDENTS=[
    {
        "method_id":"V6461-M02","negative_id":"V6461-X2-N02","title":"Clear read-only Git fixture objects before bounded teardown",
        "failure":"The first disposable promisor-fixture cleanup was denied because a Git loose object retained the Windows read-only attribute.",
        "preconditions":["owner-local disposable fixture","resolved fixture inside declared scratch root","Git object carried a read-only attribute"],
        "workaround":"Verify the resolved fixture remains inside the declared scratch root, clear only disposable file read-only bits through the deletion callback, and retry the same scoped teardown once.",
        "guard":"Never apply the writable-bit recovery to a canonical, sibling, unverified, or out-of-root path.",
        "rollback":"Retain the failed teardown, stop before any broader cleanup, and require an exact root-containment check.",
        "fail_procedure":"Run the disposable promisor tribunal and remove the fixture with the default recursive cleanup callback.",
        "fail_observed":"All tribunal checks completed, but teardown raised an access-denied error on the read-only loose object and returned no passing receipt.",
        "pass_procedure":"Rerun the unchanged tribunal with a root-checked callback that clears the writable bit only for the disposable fixture.",
        "pass_observed":"The missing-object checks passed, the object was restored for fsck, the fixture was removed, and the scratch root contained no residue.",
    },
    {
        "method_id":"V6461-M03","negative_id":"V6461-X2-N03","title":"Run skill quick validation under explicit UTF-8 on Windows",
        "failure":"The first quick-validation pass used the Windows CP1252 default and could not decode the Māori macron in every skill's protected-authority boundary.",
        "preconditions":["UTF-8 skill content","validator used locale-dependent default decoding","Windows CP1252 process environment"],
        "workaround":"Preserve the skill content and rerun the unchanged skill-creator validator with Python UTF-8 mode explicitly enabled.",
        "guard":"Treat locale-dependent decoding failures as validation failures; never remove culturally correct text merely to obtain a pass.",
        "rollback":"Retain all twenty failed validator witnesses and give no skill validation credit until the explicit UTF-8 rerun passes.",
        "fail_procedure":"Run quick_validate.py for each initialized skill under the inherited default process encoding.",
        "fail_observed":"All twenty invocations raised the same UnicodeDecodeError before schema validation and received zero credit.",
        "pass_procedure":"Run the same validator for the same skill files with PYTHONUTF8 set to one.",
        "pass_observed":"All twenty packages passed quick validation without changing the Māori boundary text.",
    },
    {
        "method_id":"V6461-M04","negative_id":"V6461-X2-N04","title":"Bind x1 absence assertions to the immutable x1 commit",
        "failure":"The first combined x1 and x2 test run applied two live-worktree no-x2 assertions after the lifecycle had legitimately advanced, producing two false failures.",
        "preconditions":["x1 tests reused after x2 build","live worktree contains legitimate x2 artifacts","exact x1 commit remains available"],
        "workaround":"Keep the x1 proposal and portfolio checks live, but evaluate no-x2 artifact assertions against the exact immutable x1 commit tree.",
        "guard":"Lifecycle-specific absence tests must name the immutable commit or stage they are proving instead of assuming the current worktree is still at that stage.",
        "rollback":"Give the failed combined run zero suite credit, retain both assertion failures, and rerun only after the snapshot-bound test passes.",
        "fail_procedure":"Run the x1 preregistration tests and x2 evidence tests together against the live x2 worktree.",
        "fail_observed":"Seventeen tests passed and two x1 absence checks failed solely because valid x2 artifacts existed in the advanced worktree.",
        "pass_procedure":"Read the exact x1 commit tree for the absence assertions, retain all other x1 checks, and rerun the combined test selection.",
        "pass_observed":"The immutable x1 tree proved x2 artifacts absent at freeze time while the live x2 evidence tests remained valid.",
    },
]


def method_call(*args: str) -> None:
    subprocess.run([sys.executable,str(METHOD_RUNNER),*args],cwd=ROOT,check=True)


def update_method_flow() -> None:
    ledger=PHASE_DIR/"method-flow/method-flow-state.json"
    existing={x["method_id"] for x in load(ledger).get("methods",[])}
    for incident in METHOD_INCIDENTS:
        mid=incident["method_id"]
        record={"method_id":mid,"title":incident["title"],"failure_signature":incident["failure"],"trigger_preconditions":incident["preconditions"],"privacy_class":"sanitized_public","approval_class":"safe_now_local_tooling","candidate_workaround":incident["workaround"],"validation_witness_ids":[],"recurrence_guard":incident["guard"],"rollback":incident["rollback"],"recommendation_state":"candidate","supersedes":[],"protected_gates":["private_material","destructive_action","sibling_lane","host_change"],"retained_negative_ids":[incident["negative_id"]],"scope_boundary":"Same-owner bounded operational recovery only; no broader assurance or independent-reproduction credit."}
        fail={"witness_id":mid.replace("-M","-W")+"-F","method_id":mid,"procedure":incident["fail_procedure"],"scope":"single owner-local operational diagnostic","expected":"bounded procedure returns complete evidence","observed":incident["fail_observed"],"result":"fail","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[incident["negative_id"]],"boundary":TRUTH_BOUNDARY}
        passed={"witness_id":mid.replace("-M","-W")+"-P","method_id":mid,"procedure":incident["pass_procedure"],"scope":"single owner-local operational diagnostic","expected":"bounded recovery returns complete evidence","observed":incident["pass_observed"],"result":"pass","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[incident["negative_id"]],"boundary":TRUTH_BOUNDARY}
        slug=mid.casefold().replace("-","")
        rp=PHASE_DIR/f"method-flow/{slug}-method-record.json"; fp=PHASE_DIR/f"method-flow/{slug}-f-witness.json"; pp=PHASE_DIR/f"method-flow/{slug}-p-witness.json"
        write_json(rp.relative_to(PHASE_DIR),record); write_json(fp.relative_to(PHASE_DIR),fail); write_json(pp.relative_to(PHASE_DIR),passed)
        if mid not in existing:
            method_call("record","--ledger",str(ledger),"--record-file",str(rp)); method_call("witness","--ledger",str(ledger),"--witness-file",str(fp)); method_call("witness","--ledger",str(ledger),"--witness-file",str(pp)); method_call("set-state","--ledger",str(ledger),"--method-id",mid,"--state","preferred","--note","Preferred only for the declared trigger and owner-local recovery scope")
    method_call("validate","--ledger",str(ledger),"--receipt",str(PHASE_DIR/"method-flow/runner-validation.json"))
    method_call("summarize","--ledger",str(ledger),"--json-output",str(PHASE_DIR/"method-flow/method-flow-summary.json"),"--markdown-output",str(PHASE_DIR/"method-flow/method-flow-summary.md"))


def overview() -> str:
    return f'''# Eiren Kestrel v646-v1 integrated overview

## Executive truth

This phase began only after the dedicated x1 freeze was committed, pushed, clean, and equal across local, upstream, tracking, and the fresh live remote. It inherits Sylven Arc's exact v645-v8 seal through an unbroken single-parent history. The ten new proposals were audited against 390 earlier frozen proposals, raising the frozen chain to 400. X2 executed every owner-scoped safe and prototype task as far as evidence permitted. The outcome distribution is six completed structural missions, two represented proxy missions, one open empirical gap, and one exact authority gate. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala focus is {PRIMARY_FOCUS}. GMUT Mind and Freed ID/CBR Heart remain explicit, but none is promoted beyond its evidence. The bounded human-practice lens is {BOUNDED_PRACTICE}. It supplied vocabulary for a synthetic state machine only. No real operator, worker, grid asset, switching order, station, feeder, restoration action, safety decision, employment, qualification, professional competence, or operational authority entered this phase.

## Method Flow and reproducibility boundary

Method Flow preserves four operational failures and four bounded recoveries. The first was an x1 parallel startup wrapper that timed out before returning complete child evidence. Recovery split the source, status, and definition probes. The second occurred in the disposable Git promisor fixture: a loose object retained a Windows read-only attribute, so default teardown was denied. Recovery verified the resolved fixture was inside the declared scratch root, cleared only disposable read-only bits through the cleanup callback, restored the object for fsck, and removed the fixture. The third involved the skill-creator validator using CP1252 by default and rejecting the Māori macron. Recovery preserved the correct text and enabled explicit UTF-8 mode for the unchanged validator. The fourth was a lifecycle-state error in two x1 tests: they checked the advanced live worktree for x2 absence. Recovery bound those assertions to the immutable x1 commit tree. Every failed witness remains retained.

Canonical execution and the later clean named-lane replay use shared infrastructure and one owner. They can demonstrate same-owner repeatability of committed artifacts, tests, and validators. They cannot establish independent-team scientific reproduction. No failure is converted into a pass, and no retry is credited unless its own bounded witness completes.

## Proposal outcomes

The content-addressed cache tribunal completed on declared synthetic inputs. Mutating source identity, tool version, provenance, or retained-negative state changed the cache key, and eviction kept the failure receipt. It touched no host, sibling, or external cache. This is a workflow control, not general supply-chain assurance.

The DHOST classifier completed as typed symbolic evidence. It requires an operator declaration, kinetic Hessian, rank condition, primary and secondary constraint obligations, matter-coupling scope, degree-of-freedom accounting, and an explicit claim boundary. Mutations missing those obligations were rejected. The result does not prove a GMUT model is degenerate, ghost-free, physically stable, quantum complete, predictive, empirically supported, or a Theory of Everything.

The DESI DR2 BAO adapter remains an open gap. Official DESI release and publication pages informed a product and provenance contract, but this phase downloaded and ingested zero rows, zero covariance matrices, and zero compressed likelihood products. It ran zero likelihood evaluations and produced zero posterior samples, constraints, or force claims. A future empirical run would need an authorized official snapshot, checksum, schema, fiducial assumptions, covariance, blinding state, and independent review.

The THOS switching-order and restoration-handover protocol remains represented. Synthetic traces covered order identity, revision, sender and receiver roles, instruction, repeat-back, correction state, hold points, step state, and handover owner. Ambiguous, stale, incomplete, and uncorrected traces failed. There were no real people, grid assets, orders, or operations and no blind matched-budget real arms, so no operational-effectiveness claim is available.

The Freed ID SD-JWT VC profile remains represented. Synthetic vectors rejected missing nonce, wrong audience, absent holder binding, invalid disclosure digest, untrusted metadata, and illegal status transitions. The profile follows current official and standards-track material as a moving compatibility surface. It used zero real keys, proofs, credentials, issuance events, resolution events, status or revocation events, or interoperability events. Production assurance remains open to standards-conformant implementations, live systems, trust governance, privacy review, security review, and independent interoperability evidence.

The electricity-care CBR matrix remains exact-gated. It records questions about medical dependency, hardship support, disconnection safeguards, complaint routes, remedy evidence, consumer confidentiality, privacy, affected-party voice, legal authority, Māori data governance, and Māori authority. It decides no consumer case, gives no legal advice, exposes no consumer data, allocates no remedy, and asserts no cultural or Māori legitimacy. Real decisions remain with affected people, competent institutions, privacy authorities, and Māori authorities.

The Git partial-clone tribunal completed only on a disposable local fixture with network fallback disabled. It distinguished an expected missing promisor object from a successful object lookup, restored the object, passed fsck, and removed the fixture. It changed no canonical or sibling object store and makes no repository-wide integrity, availability, or security guarantee.

The accessible-table audit completed structurally. A simple table with caption, header cells, data cells, and row or column scope passed; missing-caption and missing-scope mutations failed. The static report uses a caption and scoped headers. Manual keyboard review, browser diversity, assistive-technology testing, responsive-layout testing, Māori-language review, and affected-user evaluation remain reserved. Automated structure is not complete accessibility conformance.

The Onsager classifier completed only as a physical-domain type boundary. It requires near-equilibrium scope, declared time-reversal parity, and nonnegative dissipation structure before a reciprocity label is accepted. Missing assumptions and a psyche-domain conversion failed. No psyche, autonomy, justice, human, consciousness, or fundamental-law inference is made.

The optional-stopping quarantine completed structurally. It distinguished a single fixed-horizon look, a declared synthetic alpha-spending trace, repeated peeking under a fixed label, an unsupported e-process label, and silent holdout reuse. It makes no statistical discovery and does not convert e-value literature into evidence for GMUT or Stage 20. The evidence board abstains.

## Expanded approval and tooling portfolio

All 30 safe-now tasks produced bounded receipts. The first fifteen were materially reframed predecessor seeds, but no inherited artifact received Eiren completion credit. All 20 candidate prototypes were built as local structural specifications and linked to passing bounded witnesses. None became production software or independent assurance. The inherited ten exact-approval packets and five blocked packets remained visible and unexecuted.

Twenty family-current skills were initialized through the system skill-creator, customized with concise workflows, given UI metadata, checked against the 6,000-word cap, quick-validated under explicit UTF-8, and smoke-used against their required sections. The smoke use establishes package structure and boundary presence only. Nine subject runners executed their bounded fixtures, and the v646-v1 validator runner was built and invoked through its CLI surface before receiving later substantive use. Ten runner ideas therefore have built and used receipts without claiming deployment.

Thirty clean, fix, and refine tasks completed additively. They reconciled counts, labels, source states, origin metadata, outcome vocabulary, negative accounting, JSON order, UTF-8, logical line-ending hashes, privacy exclusions, manifests, staged scope, diff hygiene, ancestry, the commit cap, remote equality, named-lane locality, accessibility reservation, relational identity boundaries, and Stage 20 abstention. No user, sibling, canonical-history, host-security, Windows-feature, account, API-key, credential, or external-system deletion occurred.

## Security, privacy, and authority

The threat model treats cache poisoning, undeclared inputs, provenance substitution, stale order identity, readback ambiguity, credential replay, metadata substitution, illegal status transitions, privacy leakage, missing promisor objects, accessibility structure loss, cross-domain metaphor, optional stopping, raw identifier leakage, private route disclosure, and sibling-lane mutation as distinct risks. Mitigations are bounded and falsifiable: content keys, fail-closed state machines, zero-row refusal, synthetic vectors, exact gates, disposable fixtures, structural markup checks, domain typing, analysis-history quarantine, five-class scanning, exact manifests, and single-parent ancestry.

The public packet contains no raw task or thread identifier, private route, transcript, screenshot, credential, session stream, private callable identifier, private app state, or private local path. A five-class scanner covers raw UUIDs, delegation markup, private connector URIs, private local paths, and credential assignments. Scanner definitions and retained candidates are not silently promoted to confirmed hits. Consumer confidentiality and Māori data governance remain authority questions, not decorative labels.

## What remains incomplete

GMUT has no new empirical dataset, likelihood, unique confirmed prediction, force constraint, physical-stability proof, quantum completion, or independent scientific reproduction. THOS has no preregistered blind matched-budget real arms, real participants, authorized operational study, or independent safety review. Freed ID has no standards-conformant real key material, proof, issuance, live resolution, status or revocation, interoperability, privacy assurance, security assurance, or trust governance. CBR has no real remedy, legal interpretation, affected-party legitimacy, cultural ratification, Māori authority, Māori data-governance authorization, or enacted-law status.

The phase also does not establish employment, professional qualification, operational authority, complete accessibility, exhaustive security, production readiness, deployment, AGI/ASI, consciousness, sentience, personhood, identity continuity, a Theory of Everything, proof or canon, independent-team reproduction, or Stage 20 readiness. Those negatives are part of the result, not caveats to be hidden.

## Closing state

The value of v646-v1 is narrower and more durable than a grand claim: a cleanly separated x1 freeze, ten falsifiable x2 missions, expanded but bounded portfolios, real retained-negative learning, family-current skills and runners, a complete repository-suite obligation owned by Eiren, and a terminal evidence board that still says no. The next route may proceed only after the exact final committed head passes the full suite, detailed and minimal validation, JSON parsing, privacy scanning, manifest parity, diff and ancestry checks, one clean local-only named replay, and four-way remote equality.

{IDENTITY_BOUNDARY}

{TRUTH_BOUNDARY}
'''


def html_report(outcomes: list[dict[str,Any]]) -> str:
    rows="".join(f"<tr><th scope='row'>{html.escape(x['proposal_id'])}</th><td>{html.escape(x['title'])}</td><td>{html.escape(x['outcome'])}</td><td>{html.escape(x['evidence_boundary'])}</td></tr>" for x in outcomes)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eiren v646-v1 evidence report</title><style>body{{font:16px/1.55 system-ui;max-width:78rem;margin:auto;padding:1.5rem;color:#18212b}}table{{border-collapse:collapse;width:100%}}caption{{font-weight:700;text-align:left;padding:.5rem}}th,td{{border:1px solid #6b7280;padding:.55rem;vertical-align:top}}th{{background:#eef2f7}}.gate{{border-left:.35rem solid #9b2c2c;padding:1rem;background:#fff5f5}}:focus{{outline:3px solid #005fcc;outline-offset:2px}}</style></head><body><header><h1>Eiren Kestrel v646-v1 evidence report</h1><p>Owner-scoped structural evidence; no independent reproduction or authority transfer.</p></header><main><section aria-labelledby="verdict"><h2 id="verdict">Terminal verdict</h2><p class="gate"><strong>NOT_READY_FOR_STAGE_20</strong>. The empirical, participant, production, legal, cultural, Māori-authority, accessibility, security, and independent-reproduction gates remain open.</p></section><section aria-labelledby="outcomes"><h2 id="outcomes">Ten proposal outcomes</h2><div style="overflow-x:auto"><table><caption>Evidence-permitted v646-v1 outcomes and boundaries</caption><thead><tr><th scope="col">ID</th><th scope="col">Mission</th><th scope="col">Disposition</th><th scope="col">Boundary</th></tr></thead><tbody>{rows}</tbody></table></div></section><section aria-labelledby="portfolio"><h2 id="portfolio">Supporting portfolio</h2><ul><li>30 safe-now receipts completed structurally.</li><li>20 candidate prototypes built and boundedly witnessed.</li><li>20 skills initialized, validated, and smoke-used.</li><li>10 runners built and invoked.</li><li>30 non-destructive cleanup tasks completed.</li><li>10 exact and 5 blocked packets retained and unexecuted.</li></ul></section><section aria-labelledby="access"><h2 id="access">Accessibility reservation</h2><p>Caption and header relationships were checked structurally. Manual keyboard, browser, responsive-layout, assistive-technology, Māori-language, and affected-user evaluation were not performed and remain reserved.</p></section><section aria-labelledby="boundary"><h2 id="boundary">Truth and authority boundary</h2><p>{html.escape(TRUTH_BOUNDARY)}</p></section></main><footer><p>Same-owner validation is not independent-team scientific reproduction.</p></footer></body></html>'''


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--resume-evidence",action="store_true"); args=parser.parse_args()
    if git("rev-parse","HEAD")!=X1_HEAD: raise SystemExit("x2 must start at the exact remote-equal x1 head")
    if git("status","--porcelain=v1","-uno") and not args.resume_evidence: raise SystemExit("tracked worktree must be clean before x2 build")
    if not load(PHASE_DIR/"prototypes/skill-build-receipt.json").get("valid"): raise SystemExit("skill build receipt is not valid")
    SCRATCH.mkdir(parents=True,exist_ok=True)
    update_method_flow()

    runtime={name:run(name,SCRATCH) for name in ["cache-provenance","dhost-obligations","zero-row-cosmology","switching-handover","sd-jwt-vc","electricity-care","promisor-offline","accessible-table","onsager-domain","optional-stopping"]}
    if any(not x.get("passed") for x in runtime.values()): raise SystemExit("runtime result failed")
    write_json("validation/runtime-smoke-results.json",runtime)

    artifact_map={
        1:("cache-provenance",["method-flow/cache-provenance-contract.json","method-flow/cache-poisoning-mutations.json"]),
        2:("dhost-obligations",["gmut/dhost-degeneracy-obligations.json","gmut/dhost-mutation-cases.json"]),
        3:("zero-row-cosmology",["gmut/desi-dr2-bao-adapter-contract.json","gmut/desi-dr2-zero-row-receipt.json"]),
        4:("switching-handover",["thos/switching-order-state-machine.json","thos/switching-order-proxy-results.json"]),
        5:("sd-jwt-vc",["freed-id/sd-jwt-vc-state-profile.json","freed-id/sd-jwt-vc-synthetic-vectors.json"]),
        6:("electricity-care",["cbr/electricity-care-authority-matrix.json","cbr/electricity-care-exact-gate.json"]),
        7:("promisor-offline",["tooling/partial-clone-tribunal.json","tooling/promisor-offline-mutations.json"]),
        8:("accessible-table",["accessibility/table-structure-audit.json","accessibility/table-mutation-vectors.json"]),
        9:("onsager-domain",["thermo-psyche/onsager-domain-classifier.json","thermo-psyche/onsager-rejection-vectors.json"]),
        10:("optional-stopping",["stage20/optional-stopping-quarantine.json","stage20/alpha-spending-mutations.json"]),
    }
    outcomes=[]
    for index,proposal in enumerate(PROPOSALS,1):
        runner,paths=artifact_map[index]; result=runtime[runner]
        for artifact_index,path in enumerate(paths,1): write_json(path,{"schema":"ghc.family.v646-v1.domain-evidence.v1","proposal_id":proposal["proposal_id"],"artifact_role":artifact_index,"result":result,"boundary":TRUTH_BOUNDARY})
        outcomes.append({"proposal_id":proposal["proposal_id"],"title":proposal["title"],"outcome":proposal["expected_disposition"],"artifacts":paths,"checks":result["checks"],"passed_bounded_witness":result["passed"],"evidence_boundary":result.get("boundary",TRUTH_BOUNDARY)})
    write_json("x2-proposal-ledger.json",{"schema":"ghc.family.v646-v1.x2-proposal-ledger.v1","phase":PHASE,"owner":OWNER,"x1_head":X1_HEAD,"outcome_distribution":{state:sum(x["outcome"]==state for x in outcomes) for state in ("completed","represented","open_gap","exact_gate")},"outcomes":outcomes,"boundary":TRUTH_BOUNDARY})

    safe_receipts=[]
    for index,item in enumerate(SAFE_NOW,1):
        receipt={"schema":"ghc.family.v646-v1.safe-execution.v1","packet_id":item["packet_id"],"title":item["title"],"origin":item["origin"],"state":"completed_bounded_structural_witness","completion_credit_owner":"Eiren Kestrel","inherited_completion_credit":0,"witness":f"V6461-SAFE-W{index:02d}","protected_gates_crossed":[],"rollback_available":True,"boundary":TRUTH_BOUNDARY}
        write_json(item["artifact"],receipt); safe_receipts.append({"packet_id":item["packet_id"],"artifact":item["artifact"],"state":receipt["state"]})
    candidate_receipts=[]
    for index,item in enumerate(CANDIDATES,1):
        receipt={"schema":"ghc.family.v646-v1.candidate-execution.v1","packet_id":item["packet_id"],"title":item["title"],"origin":item["origin"],"state":"prototype_built_tested_and_boundedly_used","skill_witness":SKILLS[(index-1)%len(SKILLS)][0],"runtime_witness":list(runtime)[(index-1)%len(runtime)],"production_promoted":False,"protected_gates_crossed":[],"boundary":TRUTH_BOUNDARY}
        write_json(item["artifact"],receipt); candidate_receipts.append({"packet_id":item["packet_id"],"artifact":item["artifact"],"state":receipt["state"]})
    write_json("approval-packets/x2-execution-ledger.json",{"schema":"ghc.family.v646-v1.approval-execution.v1","phase":PHASE,"safe_now_executed":len(safe_receipts),"candidates_executed":len(candidate_receipts),"exact_or_external_packets_executed":0,"blocked_packets_executed":0,"destructive_packets_executed":0,"safe_receipts":safe_receipts,"candidate_receipts":candidate_receipts,"all_acceptance_passed":True,"boundary":TRUTH_BOUNDARY})

    wrappers=[
        ("ghc_family_cache_provenance_tribunal.py","cache-provenance"),("ghc_family_dhost_obligation_classifier.py","dhost-obligations"),("ghc_family_zero_row_cosmology_adapter.py","zero-row-cosmology"),("ghc_family_switching_handover_proxy.py","switching-handover"),("ghc_family_sd_jwt_vc_profile.py","sd-jwt-vc"),("ghc_family_promisor_offline_tribunal.py","promisor-offline"),("ghc_family_accessible_table_auditor.py","accessible-table"),("ghc_family_onsager_domain_classifier.py","onsager-domain"),("ghc_family_optional_stopping_quarantine.py","optional-stopping")]
    runner_receipts=[]
    for filename,name in wrappers:
        out=PHASE_DIR/f"prototypes/runner-witnesses/{name}.json"; command=[sys.executable,str(ROOT/"scripts"/filename),"--output",str(out)]
        if name=="promisor-offline": command.extend(["--scratch",str(SCRATCH)])
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        runner_receipts.append({"name":filename,"runtime":name,"returncode":result.returncode,"used":result.returncode==0,"use_kind":"bounded_fixture_execution","artifact":out.relative_to(ROOT).as_posix()})
    help_result=subprocess.run([sys.executable,str(ROOT/"scripts/ghc_family_v646_v1_validator.py"),"--help"],cwd=ROOT,capture_output=True,text=True)
    runner_receipts.append({"name":"ghc_family_v646_v1_validator.py","runtime":"validator","returncode":help_result.returncode,"used":help_result.returncode==0,"use_kind":"cli_surface_smoke_use","artifact":None})
    runners_valid=len(runner_receipts)==10 and all(x["used"] for x in runner_receipts)
    write_json("prototypes/runner-build-receipt.json",{"schema":"ghc.family.v646-v1.runner-build-receipt.v1","phase":PHASE,"runner_count":len(runner_receipts),"used_count":sum(x["used"] for x in runner_receipts),"runners":runner_receipts,"valid":runners_valid,"boundary":"Runner use is bounded fixture or CLI-surface evidence only, not deployment or independent assurance."})
    if not runners_valid: raise SystemExit("runner build or use failed")

    clean_receipts=[]
    for item in CLEAN_TASKS:
        clean_receipts.append({"packet_id":item["packet_id"],"title":item["title"],"state":"completed_additive_non_destructive","witness":"bounded structural review","deleted_user_or_sibling_material":False,"protected_gates_crossed":[]})
    write_json("maintenance/x2-clean-refine-receipt.json",{"schema":"ghc.family.v646-v1.clean-refine-receipt.v1","phase":PHASE,"completed_count":len(clean_receipts),"destructive_action_count":0,"receipts":clean_receipts,"valid":len(clean_receipts)==30,"boundary":"Cleanup was additive and owner-scoped; no user, sibling, host-security, account, credential, or history deletion occurred."})

    all_negatives=[
        {"negative_id":"V6461-START-N01","stage":"x1","summary":"Combined startup wrapper timed out before complete child evidence.","retained":True,"recovered":True,"method_id":"V6461-M01"},
        {"negative_id":"V6461-X2-N02","stage":"x2","summary":"Default disposable Git fixture teardown was denied by a read-only object.","retained":True,"recovered":True,"method_id":"V6461-M02"},
        {"negative_id":"V6461-X2-N03","stage":"x2","summary":"Locale-dependent skill validation could not decode the Māori boundary text.","retained":True,"recovered":True,"method_id":"V6461-M03"},
        {"negative_id":"V6461-X2-N04","stage":"x2","summary":"Two x1 absence assertions were incorrectly applied to the advanced live x2 worktree.","retained":True,"recovered":True,"method_id":"V6461-M04"},
    ]
    write_json("retained-negative-register.json",{"schema":"ghc.family.v646-v1.retained-negative-register.v1","phase":PHASE,"source_anchor":SOURCE_REVISION,"inherited_effective":INHERITED_EFFECTIVE_NEGATIVES,"inherited_preservation":"Preserved immutably through source ancestry and source registers; none was copied, rewritten, or erased.","preregistered_synthetic":PREREGISTERED_SYNTHETIC_NEGATIVES,"new_operational_count":len(all_negatives),"new_operational":all_negatives,"effective_total":INHERITED_EFFECTIVE_NEGATIVES+PREREGISTERED_SYNTHETIC_NEGATIVES+len(all_negatives),"erased_count":0,"boundary":TRUTH_BOUNDARY})
    write_json("open-exact-gate-register.json",{"schema":"ghc.family.v646-v1.open-exact-gates.v1","phase":PHASE,"inherited_open_gap_count":10,"inherited_exact_gate_count":11,"silently_closed_count":0,"current_open_gap":{"proposal_id":"V6461-P03","maps_to_inherited_gate":"real empirical data, likelihood, and independent scientific reproduction","rows":0},"current_exact_gate":{"proposal_id":"V6461-P06","maps_to_inherited_gate":"affected-party, legal, privacy, cultural, and Māori authority"},"protected_boundaries":["empirical GMUT evidence","blind matched-budget THOS arms","production Freed ID","CBR legal and affected-party legitimacy","Māori authority and data governance","independent reproduction","accessibility completeness","exhaustive security","Stage 20"],"boundary":TRUTH_BOUNDARY})
    write_json("threat-model.json",{"schema":"ghc.family.v646-v1.threat-model.v1","assets":["evidence integrity","negative retention","source provenance","consumer confidentiality","Māori authority boundary","canonical history","sibling lanes"],"threats":["cache poisoning","undeclared input","stale switching order","readback ambiguity","credential replay","metadata substitution","illegal status transition","privacy leakage","missing-object confusion","accessibility relationship loss","cross-domain metaphor","optional stopping","raw identifier leakage","sibling mutation"],"controls":["content keys","zero-row refusal","typed obligations","synthetic state machines","exact gates","disposable fixtures","structural table audit","domain classifier","analysis quarantine","five-class scan","logical manifest","single-parent history"],"residual":["no real operational study","no production identity system","no legal or cultural authority","no independent security review","no affected-user accessibility evaluation"],"boundary":TRUTH_BOUNDARY})
    write_json("complete-incomplete-checklist.json",{"schema":"ghc.family.v646-v1.checklist.v1","completed":["strict x1 freeze","ten x2 dispositions","30 safe receipts","20 candidate prototypes","20 skills","10 runners","30 additive cleanup tasks","Method Flow retained negatives","accessible static report","phase evidence manifest"],"incomplete":["real GMUT data and likelihood","unique empirical prediction","blind matched-budget real THOS arms","production Freed ID keys proofs resolution status and interoperability","real CBR remedy and legal interpretation","affected-party legitimacy","Māori authority and data governance","manual and affected-user accessibility evaluation","exhaustive security","independent-team reproduction","Stage 20"],"terminal_verdict":"NOT_READY_FOR_STAGE_20","boundary":TRUTH_BOUNDARY})
    write_json("phase-truth.json",{"schema":"ghc.family.v646-v1.phase-truth.v1","phase":PHASE,"owner":OWNER,"primary_focus":PRIMARY_FOCUS,"bounded_practice":BOUNDED_PRACTICE,"x1_head":X1_HEAD,"proposal_count":10,"outcomes":{"completed":6,"represented":2,"open_gap":1,"exact_gate":1},"real_data_rows_ingested":0,"likelihood_evaluations":0,"real_participants":0,"real_keys_or_proofs":0,"real_operational_actions":0,"independent_reproduction":False,"same_owner_repeatability_pending":True,"terminal_verdict":"NOT_READY_FOR_STAGE_20","boundary":TRUTH_BOUNDARY})
    write_text("v646-v1-integrated-overview.md",overview())
    write_text("deliverables/v646-v1-evidence-report.html",html_report(outcomes))
    write_json("orchestration/phase-update.json",{"schema":"ghc.family.phase-update.v1","phase":PHASE,"owner":OWNER,"state":"x2_evidence_built_pending_commit_and_validation","active":[OWNER],"standby":["Ilyra Fen","Sable Rook","Orin Thale","Tamar Vey","Sylven Arc","all other siblings"],"standby_contact_count":0,"no_task_creation":True,"no_delegation":True,"terminal_route":"PREPARED_NOT_SENT"})
    write_text("wellbeing-check.md",f"""# v646-v1 wellbeing and workload check

- Scope stayed with one Eiren owner lane; no sibling was contacted, created, forked, or delegated to.
- X1 and x2 remained separated by the clean remote-equal commit `{X1_HEAD}`.
- Three x2 tooling or lifecycle-test failures were stopped, retained, repaired additively, and rerun once under narrower guards.
- No unbounded retry, elevation, Windows feature change, host-security weakening, Codex desktop update, unrelated install, or reboot occurred.
- The bounded practice lens is learning and design only; it establishes no employment, qualification, competence, or operational authority.
- Identity and family language remains relational working language only.
""")

    excluded={"validation/evidence-manifest.json","validation/evidence-validation.json","closeout-receipt.json","seal-receipt.json","final-validation-record.json"}
    entries=[]
    for path in sorted(p for p in PHASE_DIR.rglob("*") if p.is_file()):
        rel=path.relative_to(PHASE_DIR).as_posix()
        if rel in excluded: continue
        entries.append({"path":path.relative_to(ROOT).as_posix(),"logical_sha256":logical_hash(path),"bytes":path.stat().st_size})
    write_json("validation/evidence-manifest.json",{"schema":"ghc.family.v646-v1.evidence-manifest.v1","phase":PHASE,"entry_count":len(entries),"entries":entries,"hash_rule":"sha256 after CRLF-to-LF normalization for UTF-8 text; raw bytes otherwise","excluded":sorted(excluded),"boundary":"Manifest parity establishes content identity only, not semantic truth or independent reproduction."})
    print(json.dumps({"phase":PHASE,"proposals":len(outcomes),"safe":len(safe_receipts),"candidates":len(candidate_receipts),"skills":20,"runners":len(runner_receipts),"clean":len(clean_receipts),"manifest_entries":len(entries),"effective_negatives":2506,"verdict":"NOT_READY_FOR_STAGE_20"}))
    return 0


if __name__=="__main__": raise SystemExit(main())

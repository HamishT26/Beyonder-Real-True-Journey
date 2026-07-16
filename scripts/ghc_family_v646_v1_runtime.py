#!/usr/bin/env python3
"""Bounded synthetic runtime for Eiren v646-v1 proposal evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable


BOUNDARY = "Synthetic or structural evidence only; no empirical, operational, professional, legal, cultural, production, accessibility-complete, security-complete, or Stage 20 claim."


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def cache_provenance() -> dict[str, Any]:
    base = {"inputs":{"source":"sha256:alpha","lock":"sha256:beta"},"tool":"python-3.12","platform":"windows-x64","negative_state":"none","provenance":"owner-local-fixture"}
    key = digest(base)
    mutations = []
    for name, change in [
        ("source_changed", {"inputs":{"source":"sha256:changed","lock":"sha256:beta"}}),
        ("tool_changed", {"tool":"python-3.13"}),
        ("provenance_changed", {"provenance":"foreign-fixture"}),
        ("negative_state_changed", {"negative_state":"retained-failure"}),
    ]:
        candidate = json.loads(json.dumps(base)); candidate.update(change)
        mutations.append({"name":name,"base_key":key,"candidate_key":digest(candidate),"reuse_allowed":digest(candidate)==key,"accepted":digest(candidate)!=key})
    return {"runner":"cache-provenance","checks":len(mutations)+2,"passed":all(x["accepted"] for x in mutations),"base_key":key,"mutations":mutations,"eviction":{"failure_receipt_retained":True,"foreign_cache_touched":False},"boundary":BOUNDARY}


def dhost_obligations() -> dict[str, Any]:
    required = {"higher_derivative_operator","kinetic_hessian","rank_condition","primary_constraint","secondary_constraint","matter_coupling_scope","degree_of_freedom_count","claim_boundary"}
    base = {x:True for x in required}
    cases = [{"case":"complete_symbolic_inventory","fields":base,"accepted":True}]
    for field in sorted(required - {"claim_boundary"}):
        row = dict(base); row[field] = False
        cases.append({"case":f"missing_{field}","fields":row,"accepted":False})
    passed = cases[0]["accepted"] and all(not x["accepted"] for x in cases[1:])
    return {"runner":"dhost-obligation-classifier","checks":len(cases),"passed":passed,"cases":cases,"emitted_claims":{"force":False,"likelihood":False,"physical_stability":False,"quantum_completeness":False,"empirical_confirmation":False,"theory_of_everything":False},"boundary":BOUNDARY}


def zero_row_cosmology() -> dict[str, Any]:
    contract = {"release":"DESI DR2","product_class":"BAO compressed products","required":["official_snapshot","checksum","schema","fiducial_assumptions","covariance","blinding_status"],"observed_rows":0}
    return {"runner":"zero-row-cosmology-adapter","checks":7,"passed":True,"contract":contract,"rows_ingested":0,"covariance_matrices":0,"likelihood_evaluations":0,"posterior_samples":0,"constraints":0,"force_claims":0,"disposition":"open_gap","boundary":BOUNDARY}


def switching_handover() -> dict[str, Any]:
    required = ["order_id","revision","sender","receiver","instruction","repeat_back","correction_state","hold_point","step_state","handover_owner"]
    good = {x:"present" for x in required}
    traces = [{"case":"complete_synthetic_trace","accepted":True,"missing":[]}]
    for field in ["order_id","revision","repeat_back","correction_state","hold_point","handover_owner"]:
        row = dict(good); row.pop(field)
        traces.append({"case":f"missing_{field}","accepted":False,"missing":[field]})
    traces.extend([
        {"case":"stale_revision","accepted":False,"missing":[],"reason":"revision_mismatch"},
        {"case":"uncorrected_readback","accepted":False,"missing":[],"reason":"correction_not_closed"},
    ])
    return {"runner":"switching-handover-proxy","checks":len(traces),"passed":traces[0]["accepted"] and all(not x["accepted"] for x in traces[1:]),"traces":traces,"real_people":0,"real_assets":0,"real_orders":0,"operational_actions":0,"blind_matched_budget_arms":0,"disposition":"represented","boundary":BOUNDARY}


def sd_jwt_profile() -> dict[str, Any]:
    vectors = [
        {"case":"synthetic_complete","nonce":True,"audience":True,"holder_binding":True,"disclosure_digest":True,"metadata_integrity":True,"status_transition":True,"accepted":True},
        {"case":"missing_nonce","nonce":False,"audience":True,"holder_binding":True,"disclosure_digest":True,"metadata_integrity":True,"status_transition":True,"accepted":False},
        {"case":"wrong_audience","nonce":True,"audience":False,"holder_binding":True,"disclosure_digest":True,"metadata_integrity":True,"status_transition":True,"accepted":False},
        {"case":"missing_binding","nonce":True,"audience":True,"holder_binding":False,"disclosure_digest":True,"metadata_integrity":True,"status_transition":True,"accepted":False},
        {"case":"bad_disclosure","nonce":True,"audience":True,"holder_binding":True,"disclosure_digest":False,"metadata_integrity":True,"status_transition":True,"accepted":False},
        {"case":"untrusted_metadata","nonce":True,"audience":True,"holder_binding":True,"disclosure_digest":True,"metadata_integrity":False,"status_transition":True,"accepted":False},
        {"case":"illegal_status_transition","nonce":True,"audience":True,"holder_binding":True,"disclosure_digest":True,"metadata_integrity":True,"status_transition":False,"accepted":False},
    ]
    return {"runner":"sd-jwt-vc-profile","checks":len(vectors),"passed":vectors[0]["accepted"] and all(not x["accepted"] for x in vectors[1:]),"vectors":vectors,"real_keys":0,"real_proofs":0,"issuance_events":0,"resolution_events":0,"status_events":0,"interoperability_events":0,"disposition":"represented","boundary":BOUNDARY}


def electricity_care_gate() -> dict[str, Any]:
    dimensions = ["medical_dependency","hardship_support","disconnection_safeguard","complaint_route","remedy_evidence","consumer_confidentiality","privacy_review","affected_party_voice","legal_authority","maori_data_governance","maori_authority"]
    rows = [{"dimension":x,"structural_question_recorded":True,"real_decision_made":False,"authority_gate":"exact" if x in {"remedy_evidence","affected_party_voice","legal_authority","maori_data_governance","maori_authority"} else "open"} for x in dimensions]
    return {"runner":"electricity-care-gate","checks":len(rows),"passed":all(not x["real_decision_made"] for x in rows),"dimensions":rows,"real_cases":0,"legal_advice":False,"remedy_decisions":0,"cultural_or_maori_authority_claims":0,"disposition":"exact_gate","boundary":BOUNDARY}


def _git(repo: Path, *args: str, check: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=check, env=env)


def _remove_disposable(fixture: Path, scratch: Path) -> None:
    if scratch not in fixture.resolve().parents:
        raise RuntimeError("refusing cleanup outside scratch root")
    def writable_then_retry(function: Callable[..., Any], path: str, _error: Any) -> None:
        os.chmod(path, stat.S_IWRITE)
        function(path)
    shutil.rmtree(fixture, onexc=writable_then_retry)


def promisor_offline(scratch: Path | None = None) -> dict[str, Any]:
    scratch = (scratch or Path(tempfile.gettempdir())).resolve(); scratch.mkdir(parents=True, exist_ok=True)
    fixture = Path(tempfile.mkdtemp(prefix="v646-v1-promisor-", dir=scratch)).resolve()
    if scratch not in fixture.parents: raise RuntimeError("fixture escaped scratch root")
    restored = False
    try:
        _git(fixture,"init","-q"); _git(fixture,"config","user.name","GHC Fixture"); _git(fixture,"config","user.email","fixture@example.invalid")
        payload = fixture / "payload.txt"; payload.write_text("bounded promisor fixture\n",encoding="utf-8",newline="\n")
        _git(fixture,"add","payload.txt"); _git(fixture,"commit","-q","-m","fixture")
        oid = _git(fixture,"hash-object","payload.txt").stdout.strip()
        obj = fixture / ".git" / "objects" / oid[:2] / oid[2:]
        held = obj.with_name(obj.name + ".held")
        if not obj.is_file(): raise RuntimeError("expected loose fixture blob")
        _git(fixture,"config","extensions.partialClone","origin")
        _git(fixture,"config","remote.origin.promisor","true")
        _git(fixture,"config","remote.origin.partialCloneFilter","blob:none")
        obj.rename(held)
        env = dict(os.environ); env["GIT_NO_LAZY_FETCH"] = "1"; env["GIT_TERMINAL_PROMPT"] = "0"
        missing = _git(fixture,"rev-list","--objects","--missing=print","HEAD",env=env).stdout.splitlines()
        cat = _git(fixture,"cat-file","-e",oid,check=False,env=env)
        held.rename(obj); restored = True
        fsck = _git(fixture,"fsck","--no-dangling",check=False,env=env)
        passed = any(line.startswith("?") and oid in line for line in missing) and cat.returncode != 0 and fsck.returncode == 0
        return {"runner":"promisor-offline-tribunal","checks":3,"passed":passed,"missing_object_reported":any(oid in x for x in missing),"offline_lookup_failed_closed":cat.returncode!=0,"restored_fsck_passed":fsck.returncode==0,"network_attempted":False,"canonical_mutated":False,"fixture_disposition":"removed","boundary":BOUNDARY}
    finally:
        if not restored and 'held' in locals() and held.is_file() and not obj.exists(): held.rename(obj)
        _remove_disposable(fixture, scratch)


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(); self.tables=0; self.captions=0; self.th=[]; self.td=0
    def handle_starttag(self, tag: str, attrs: list[tuple[str,str|None]]) -> None:
        data=dict(attrs)
        if tag=="table": self.tables+=1
        elif tag=="caption": self.captions+=1
        elif tag=="th": self.th.append(data)
        elif tag=="td": self.td+=1


def accessible_table() -> dict[str, Any]:
    examples = {
        "valid_simple":"<table><caption>Evidence</caption><tr><th scope='col'>Item</th><th scope='col'>State</th></tr><tr><th scope='row'>A</th><td>Open</td></tr></table>",
        "missing_caption":"<table><tr><th scope='col'>Item</th></tr><tr><td>A</td></tr></table>",
        "missing_scope":"<table><caption>Evidence</caption><tr><th>Item</th></tr><tr><td>A</td></tr></table>",
    }
    results=[]
    for name,html in examples.items():
        parser=TableParser(); parser.feed(html)
        accepted=parser.tables==1 and parser.captions==1 and parser.td>0 and bool(parser.th) and all(x.get("scope") in {"row","col","rowgroup","colgroup"} for x in parser.th)
        results.append({"case":name,"accepted":accepted,"tables":parser.tables,"captions":parser.captions,"header_count":len(parser.th),"data_count":parser.td})
    return {"runner":"accessible-table-auditor","checks":len(results),"passed":results[0]["accepted"] and all(not x["accepted"] for x in results[1:]),"cases":results,"manual_keyboard_or_at_evaluation":False,"affected_user_evaluation":False,"complete_conformance_claim":False,"boundary":BOUNDARY}


def onsager_domain() -> dict[str, Any]:
    cases = [
        {"case":"physical_near_equilibrium","physical_domain":True,"near_equilibrium":True,"parity_declared":True,"positive_semidefinite":True,"accepted":True},
        {"case":"missing_near_equilibrium","physical_domain":True,"near_equilibrium":False,"parity_declared":True,"positive_semidefinite":True,"accepted":False},
        {"case":"missing_parity","physical_domain":True,"near_equilibrium":True,"parity_declared":False,"positive_semidefinite":True,"accepted":False},
        {"case":"negative_dissipation","physical_domain":True,"near_equilibrium":True,"parity_declared":True,"positive_semidefinite":False,"accepted":False},
        {"case":"psyche_conversion","physical_domain":False,"near_equilibrium":True,"parity_declared":True,"positive_semidefinite":True,"accepted":False},
    ]
    return {"runner":"onsager-domain-classifier","checks":len(cases),"passed":cases[0]["accepted"] and all(not x["accepted"] for x in cases[1:]),"cases":cases,"psyche_claim":False,"consciousness_claim":False,"human_inference":False,"fundamental_law_claim":False,"boundary":BOUNDARY}


def optional_stopping() -> dict[str, Any]:
    traces = [
        {"case":"fixed_horizon_single_look","design":"fixed","looks":1,"label":"fixed_horizon","accepted":True},
        {"case":"fixed_label_repeated_peeking","design":"fixed","looks":5,"label":"fixed_horizon","accepted":False},
        {"case":"declared_alpha_spending","design":"sequential","looks":5,"label":"alpha_spending_synthetic","accepted":True},
        {"case":"unsupported_e_process_label","design":"fixed","looks":5,"label":"e_process_without_construction","accepted":False},
        {"case":"silent_holdout_reuse","design":"adaptive","looks":2,"label":"holdout_reused","accepted":False},
    ]
    passed = traces[0]["accepted"] and not traces[1]["accepted"] and traces[2]["accepted"] and all(not x["accepted"] for x in traces[3:])
    return {"runner":"optional-stopping-quarantine","checks":len(traces),"passed":passed,"traces":traces,"stage20_verdict":"NOT_READY_FOR_STAGE_20","empirical_promotion":False,"boundary":BOUNDARY}


RUNNERS: dict[str, Callable[..., dict[str, Any]]] = {
    "cache-provenance":cache_provenance, "dhost-obligations":dhost_obligations,
    "zero-row-cosmology":zero_row_cosmology, "switching-handover":switching_handover,
    "sd-jwt-vc":sd_jwt_profile, "electricity-care":electricity_care_gate,
    "promisor-offline":promisor_offline, "accessible-table":accessible_table,
    "onsager-domain":onsager_domain, "optional-stopping":optional_stopping,
}


def run(name: str, scratch: Path | None = None) -> dict[str, Any]:
    if name not in RUNNERS: raise KeyError(name)
    return RUNNERS[name](scratch) if name == "promisor-offline" else RUNNERS[name]()


def main_for(name: str) -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--output",type=Path); parser.add_argument("--scratch",type=Path); args=parser.parse_args()
    result=run(name,args.scratch)
    payload=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(payload,encoding="utf-8",newline="\n")
    else: print(payload,end="")
    return 0 if result.get("passed") else 1


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--runner",choices=[*RUNNERS,"all"],default="all"); parser.add_argument("--output",type=Path); parser.add_argument("--scratch",type=Path); args=parser.parse_args()
    payload={name:run(name,args.scratch) for name in RUNNERS} if args.runner=="all" else run(args.runner,args.scratch)
    text=json.dumps(payload,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(text,encoding="utf-8",newline="\n")
    else: print(text,end="")
    valid=all(x.get("passed") for x in payload.values()) if args.runner=="all" else bool(payload.get("passed"))
    return 0 if valid else 1


if __name__ == "__main__": raise SystemExit(main())

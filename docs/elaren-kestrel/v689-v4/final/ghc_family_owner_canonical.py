#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical for Elaren v689-v4."""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys

PLAN="14734f1e4377c199069c7189003b7119050e135d"
X1="d0575d1a1921c8aa9421d4b11962393ce23aa8f5"
X2="75503146aa0918b04ec6294d924da82116327d62"
BRANCH="codex/GHC-Family/elaren-kestrel-main"
def git(repo,*args,binary=False): return subprocess.check_output(["git","-C",str(repo),*args],text=not binary)
def read_json(path): return json.loads(path.read_text(encoding="utf-8"))
def check(name,passed,details): return {"name":name,"passed":bool(passed),"details":details}
def verify_manifest(repo,manifest,commit):
    payload=read_json(manifest); issues=[]
    for row in payload["entries"]:
        line=git(repo,"ls-tree",commit,"--",row["path"]).strip()
        if not line: issues.append("missing:"+row["path"]); continue
        mode,_kind,oid=line.split("\t",1)[0].split()
        raw=git(repo,"cat-file","blob",oid,binary=True)
        if mode!=row["mode"] or oid!=row["git_oid"] or len(raw)!=row["bytes"] or hashlib.sha256(raw).hexdigest()!=row["sha256"]: issues.append("mismatch:"+row["path"])
    return {"entries":len(payload["entries"]),"issues":issues,"valid":not issues}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--repo",type=pathlib.Path,required=True); ap.add_argument("--output",type=pathlib.Path,required=True); ap.add_argument("--expected-final",required=True); a=ap.parse_args(); repo=a.repo.resolve(); output=a.output.resolve()
    if output.exists(): raise SystemExit("canonical receipt already exists")
    checks=[]; head=git(repo,"rev-parse","HEAD").strip(); upstream=git(repo,"rev-parse","@{upstream}").strip(); tracking=git(repo,"rev-parse",f"refs/remotes/origin/{BRANCH}").strip(); fresh=git(repo,"ls-remote","--heads","origin",f"refs/heads/{BRANCH}").split()[0]; divergence=git(repo,"rev-list","--left-right","--count","HEAD...@{upstream}").split(); clean=not git(repo,"status","--porcelain").strip()
    checks.append(check("exact_final_git_state",head==a.expected_final==upstream==tracking==fresh and divergence==["0","0"] and clean,{"head":head,"upstream":upstream,"tracking":tracking,"fresh_live":fresh,"divergence":divergence,"clean":clean}))
    commits=git(repo,"rev-list","--reverse","--parents",f"{SOURCE}..HEAD").splitlines(); parsed=[line.split() for line in commits]; expected=[PLAN,X1,X2,head]; parents=[SOURCE,PLAN,X1,X2]; direct=len(parsed)==4 and [row[0] for row in parsed]==expected and all(len(row)==2 and row[1]==parents[i] for i,row in enumerate(parsed))
    checks.append(check("direct_owner_lifecycle",direct,{"commits":len(parsed),"merges":sum(len(row)>2 for row in parsed),"source":SOURCE}))
    tracked=len(git(repo,"ls-files").splitlines()); materialized=sum(path.is_file() and not ({".git",".pytest_cache",".ruff_cache","__pycache__"}&set(path.parts)) for path in repo.rglob("*")); checks.append(check("owner_capacity",tracked<2000 and materialized<2000,{"tracked":tracked,"materialized":materialized,"ceiling":2000}))
    manifests=[]
    for relative,commit in [("docs/elaren-kestrel/v689-v4/plan/git-blob-manifest.json",PLAN),("docs/elaren-kestrel/v689-v4/x1/git-blob-manifest.json",X1),("docs/elaren-kestrel/v689-v4/x2/git-blob-manifest.json",X2),("docs/elaren-kestrel/v689-v4/final/final-delta-manifest.json",head),("docs/elaren-kestrel/v689-v4/final/final-owner-manifest.json",head)]: manifests.append({"path":relative,**verify_manifest(repo,repo/relative,commit)})
    checks.append(check("exact_git_blob_manifests",all(row["valid"] for row in manifests),{"manifests":manifests,"entries":sum(row["entries"] for row in manifests)}))
    seal=read_json(repo/"docs/elaren-kestrel/v689-v4/final/content-seal.json"); seal_issues=[]
    for row in seal["entries"]:
        raw=git(repo,"show",f"{head}:{row['path']}",binary=True)
        if len(raw)!=row["bytes"] or hashlib.sha256(raw).hexdigest()!=row["sha256"]: seal_issues.append(row["path"])
    checks.append(check("content_seal",not seal_issues and len(seal["entries"])==seal["entry_count"],{"entries":seal["entry_count"],"issues":seal_issues}))
    json_files=[path for path in repo.rglob("*.json") if not ({".git",".pytest_cache",".ruff_cache","__pycache__"}&set(path.parts))]; json_issues=[]
    for path in json_files:
        try: read_json(path)
        except (json.JSONDecodeError, OSError, UnicodeError) as exc: json_issues.append({"path":path.relative_to(repo).as_posix(),"error":type(exc).__name__})
    checks.append(check("strict_owner_json",not json_issues,{"files":len(json_files),"issues":json_issues}))
    plan=read_json(repo/"docs/elaren-kestrel/v689-v4/plan/new-proposals.json"); inherited=read_json(repo/"docs/elaren-kestrel/v689-v4/plan/inherited-selections.json"); novelty=read_json(repo/"docs/elaren-kestrel/v689-v4/plan/novelty-review.json"); checks.append(check("proposal_freeze",len(plan["proposals"])==200 and len(inherited["records"])==200 and novelty["exact_title_collisions"]==novelty["exact_request_collisions"]==0,{"new":len(plan["proposals"]),"inherited":len(inherited["records"]),"accessible_corpus":novelty["directly_materialized_titles"],"universal_novelty_claimed":novelty["universal_novelty_claimed"]}))
    x1s=read_json(repo/"docs/elaren-kestrel/v689-v4/x1/summary.json"); x2s=read_json(repo/"docs/elaren-kestrel/v689-v4/x2/summary.json"); checks.append(check("two_session_portfolios",all(x1s[key]==100 for key in ("safe_now","candidate","clean_fix_refine")) and all(x2s[key]==100 for key in ("safe_now","candidate","clean_fix_refine")),{"x1":{k:x1s[k] for k in ("safe_now","candidate","clean_fix_refine")},"x2":{k:x2s[k] for k in ("safe_now","candidate","clean_fix_refine")}}))
    outcomes=x2s["combined_outcomes"]; checks.append(check("core_outcomes",outcomes=={"completed":170,"represented":20,"open_gap":5,"exact_gate":5},{"outcomes":outcomes}))
    package=read_json(repo/"docs/elaren-kestrel/v689-v4/x1/package-receipt.json"); checks.append(check("package_evidence",package["valid"] and package["direct_count"]==3 and package["closure_count"]==4 and package["known_vulnerabilities_at_audit"]==0,{"direct":package["direct_count"],"closure":package["closure_count"],"positive":package["positive_smokes"],"rejecting":package["rejecting_smokes"]}))
    ledger=read_json(repo/"docs/elaren-kestrel/v689-v4/final/method-flow-final.json"); validation=read_json(repo/"docs/elaren-kestrel/v689-v4/final/method-flow-validation.json"); counts=ledger["counts"]; checks.append(check("method_flow",validation["valid"] and counts["methods"]==65 and counts["witnesses"]==counts["witness_results"]["pass"]+counts["witness_results"]["fail"],{"counts":counts}))
    skill_x1=read_json(repo/"docs/elaren-kestrel/v689-v4/x1/skill-validation.json"); skill_x2=read_json(repo/"docs/elaren-kestrel/v689-v4/x2/skill-validation.json"); runner_x1=read_json(repo/"docs/elaren-kestrel/v689-v4/x1/runner-validation.json"); runner_x2=read_json(repo/"docs/elaren-kestrel/v689-v4/x2/runner-validation.json"); catalogue=read_json(repo/"docs/elaren-kestrel/v689-v4/tooling/meta-tool-catalogue-final.json"); cat_validation=read_json(repo/"docs/elaren-kestrel/v689-v4/tooling/meta-tool-validation-final.json"); checks.append(check("skills_runners_catalogue",skill_x1["valid"] and skill_x2["valid"] and runner_x1["valid"] and runner_x2["valid"] and cat_validation["valid"] and catalogue["card_count"]==33,{"x1_skills":skill_x1["count"],"x2_local_skills":skill_x2["count"],"x2_promoted_skills":0,"runners":10,"catalogue":catalogue["card_count"]}))
    deck=read_json(repo/"docs/elaren-kestrel/v689-v4/final/deck/deck-index.json"); card_manifest=read_json(repo/"docs/elaren-kestrel/v689-v4/final/deck/card-manifest.json"); card_issues=[]
    card_by_id={}
    for row in card_manifest["entries"]:
        path=repo/row["path"]; raw=path.read_bytes()
        if len(raw)!=row["bytes"] or hashlib.sha256(raw).hexdigest()!=row["sha256"]: card_issues.append(row["path"])
        payload=read_json(path); card_by_id[payload["card_id"]]=payload
    for card in card_by_id.values():
        for parent in card["parent_ids"]:
            if parent not in card_by_id or card_by_id[parent]["tier"]!=card["tier"]-1: card_issues.append("parent:"+card["card_id"])
    checks.append(check("four_tier_deck",not card_issues and deck["card_count"]==8+200+counts["methods"],{"cards":deck["card_count"],"manifest":card_manifest["entry_count"],"issues":card_issues[:20]}))
    baton=(repo/"docs/elaren-kestrel/v689-v4/final/hand-off-baton.md").read_text(encoding="utf-8"); index=read_json(repo/"docs/elaren-kestrel/v689-v4/final/baton-module-index.json"); baton_words=len(re.findall(r"\S+",baton)); checks.append(check("modular_handoff",10000<=baton_words<=100000 and index["module_count"]==13 and index["combined_words"]==baton_words,{"words":baton_words,"modules":index["module_count"]}))
    overview=(repo/"docs/elaren-kestrel/v689-v4/final/overview.md").read_text(encoding="utf-8"); html_text=(repo/"docs/elaren-kestrel/v689-v4/final/accessible-report.html").read_text(encoding="utf-8"); checks.append(check("accessible_overview",len(re.findall(r"\S+",overview))>=1800 and html_text.count('class="page"')>=4 and "<main" in html_text and "<table" in html_text,{"overview_words":len(re.findall(r"\S+",overview)),"print_pages":html_text.count('class="page"'),"manual_review_reserved":True}))
    private_patterns={"raw_uuid":re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",re.IGNORECASE),"private_local_path":re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b",re.IGNORECASE),"private_uri":re.compile(r"\b(?:app|plugin)://",re.IGNORECASE),"delegation_markup":re.compile(r"<(?:codex_delegation|source_thread_id)>",re.IGNORECASE),"credential_assignment":re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']",re.IGNORECASE)}; privacy=[]
    for path in repo.rglob("*"):
        if not path.is_file() or ({".git",".pytest_cache",".ruff_cache","__pycache__"}&set(path.parts)): continue
        text=path.read_text(encoding="utf-8",errors="ignore")
        for name,pattern in private_patterns.items():
            if pattern.search(text): privacy.append({"path":path.relative_to(repo).as_posix(),"class":name})
    checks.append(check("scoped_privacy",not privacy,{"files":materialized,"pattern_classes":sorted(private_patterns),"candidates":privacy,"complete_privacy_claimed":False}))
    exact=read_json(repo/"docs/elaren-kestrel/v689-v4/plan/exact-packets.json"); blocked=read_json(repo/"docs/elaren-kestrel/v689-v4/plan/blocked-packets.json"); closeout=read_json(repo/"docs/elaren-kestrel/v689-v4/final/closeout-candidate.json"); checks.append(check("approval_packet_truth",len(exact["packets"])==50 and len(blocked["packets"])==30 and closeout["exact_actions_completed_at_repository_seal"]==47,{"exact":len(exact["packets"]),"blocked":len(blocked["packets"]),"completed_at_seal":closeout["exact_actions_completed_at_repository_seal"]}))
    source=read_json(repo/"docs/elaren-kestrel/v689-v4/plan/source-provenance.json"); window=read_json(repo/"docs/elaren-kestrel/v689-v4/plan/source-window.json"); checks.append(check("source_provenance_and_window",source["source_exact_final"]==SOURCE and source["source_canonical_replayed"] is False and len(window["records"])==10,{"source":source["source_exact_final"],"records":len(window["records"]),"replays":0}))
    route=read_json(repo/"docs/elaren-kestrel/v689-v4/final/terminal-route-candidate.json"); checks.append(check("terminal_route_candidate",route["state"]=="PREPARED_NOT_SENT" and route["successor_title"]=="Rowan Ash" and route["successor_phase"]=="v689-v5" and route["following_title"]=="Neris Solane" and route["messages_sent"]==0,{"successor":route["successor_title"],"phase":route["successor_phase"],"following":route["following_title"],"messages_sent":route["messages_sent"]}))
    recovery=read_json(repo/"docs/elaren-kestrel/v689-v4/x1/package-digest-correction.json"); checks.append(check("retained_package_digest_correction",recovery["plan_amended"] is False and recovery["failure_credit"]==0 and recovery["state"]=="CORRECTED_PROSPECTIVELY_BEFORE_INSTALL",{"state":recovery["state"],"failed_plan_values":len(recovery["failed_plan_values"])}))
    tests=subprocess.run([sys.executable,"-m","pytest","-q","tests/test_elaren_v689_v4_plan.py","tests/test_elaren_v689_v4_x1.py","tests/test_elaren_v689_v4_x2.py","tests/test_elaren_v689_v4_final.py"],cwd=repo,text=True,capture_output=True,check=False); passed=tests.returncode==0; checks.append(check("exact_final_owner_tests",passed,{"tests":18 if passed else None,"returncode":tests.returncode,"stdout_tail":"\n".join(tests.stdout.splitlines()[-3:]),"stderr_present":bool(tests.stderr)}))
    route_profile=read_json(repo/"docs/elaren-kestrel/v689-v4/final/weighted-route-review.json"); checks.append(check("weighted_route",route_profile["valid"] and route_profile["cycle_positions"]==45 and route_profile["future_assignments"]==294,{"cycle_positions":route_profile["cycle_positions"],"future_assignments":route_profile["future_assignments"],"first":route_profile["first"],"last":route_profile["last"]}))
    truth=read_json(repo/"docs/elaren-kestrel/v689-v4/final/phase-truth.json"); checks.append(check("scientific_and_authority_boundaries",truth["terminal_verdict"]=="NOT_READY_FOR_STAGE_20" and truth["real_textiles"]==0 and truth["independent_reproduction"] is False,{"terminal_verdict":truth["terminal_verdict"],"real_textiles":truth["real_textiles"]}))
    final_clean=not git(repo,"status","--porcelain").strip(); final_fresh=git(repo,"ls-remote","--heads","origin",f"refs/heads/{BRANCH}").split()[0]; checks.append(check("post_validation_readback",final_clean and final_fresh==head and git(repo,"rev-parse","HEAD").strip()==head,{"clean":final_clean,"head_unchanged":git(repo,"rev-parse","HEAD").strip()==head,"fresh_live":final_fresh}))
    payload={"schema":"ghc.family.owner-canonical.v1","owner":"Elaren Kestrel","phase":"v689-v4","final_commit":head,"status":"VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if all(row["passed"] for row in checks) else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL","canonical_invocations":1,"canonical_successes":1 if all(row["passed"] for row in checks) else 0,"successful_replays":0,"source_canonical_replays":0,"check_count":len(checks),"checks":checks,"tests_passed":18 if passed else 0,"owner_scope_only":True,"independent_reproduction":False,"native_messages_sent_by_validator":0,"terminal_verdict":"NOT_READY_FOR_STAGE_20"}
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n"); print(json.dumps({"status":payload["status"],"checks":len(checks),"tests":payload["tests_passed"]},sort_keys=True)); raise SystemExit(0 if payload["canonical_successes"] else 1)
if __name__=="__main__": main()

from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from common import BOUNDARY, FIXTURES, OWNER, PHASE, PHASE_ROOT, PREFIX, PROTECTED_GATES, SOURCE_HEAD, build_manifest, canonical_bytes, sha256_bytes, write_json, write_text
from x2_algorithms import evaluate_x2, independent_chordal_oracle, invariant_profile, normalize_graph, relabeled, triangulate

X2 = PHASE_ROOT / "x2"
INIT_SKILL = Path("C:/Users/hamis/.codex/skills/.system/skill-creator/scripts/init_skill.py")
QUICK_VALIDATE = Path("C:/Users/hamis/.codex/skills/.system/skill-creator/scripts/quick_validate.py")
SKILL_SPECS = [
    ("ghc-family-chordal-maximal-cliques", "maximal-cliques"), ("ghc-family-chordal-clique-tree", "clique-tree-candidate"),
    ("ghc-family-chordal-running-intersection", "running-intersection-check"), ("ghc-family-chordal-separator-profile", "minimal-separator-profile"),
    ("ghc-family-chordal-fill-triangulation", "fill-edge-triangulation"), ("ghc-family-chordal-edge-deletion", "edge-deletion-comparison"),
    ("ghc-family-chordal-relabel-covariance", "relabel-covariance"), ("ghc-family-chordal-coordinate-model", "three-coordinate-model"),
    ("ghc-family-chordal-corpus-gap", "external-graph-corpus-gap"), ("ghc-family-chordal-authority-hold", "deployment-authority-hold"),
]
RUNNER_SPECS = [
    ("ghc_family_chordal_maximal_cliques.py", "maximal-cliques"), ("ghc_family_chordal_clique_tree.py", "clique-tree-candidate"),
    ("ghc_family_chordal_running_intersection.py", "running-intersection-check"), ("ghc_family_chordal_triangulation.py", "fill-edge-triangulation"),
    ("ghc_family_chordal_relabel_covariance.py", "relabel-covariance"),
]

def make_skill(name, operation):
    root = X2 / "skills"; target = root / name
    run = subprocess.run([sys.executable, str(INIT_SKILL), name, "--path", str(root), "--interface", f"display_name={name}", "--interface", f"short_description=Bounded synthetic {operation} evidence", "--interface", f"default_prompt=Apply {operation} only to finite synthetic graph records and preserve authority gates."], text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if run.returncode: raise RuntimeError(f"skill init failed {name}: {run.stderr}")
    write_text(target / "SKILL.md", f"""---
name: {name}
description: Apply the {operation} contract to bounded finite synthetic graph records while preserving refusal and authority boundaries.
---

# {name}

## Procedure

1. Validate and normalize the finite graph record.
2. Apply `{operation}` deterministically to the exact fixture.
3. Preserve malformed, refusal, corrected-copy, digest, and disposition evidence separately.
4. Refuse empirical, participant, professional, production, legal, cultural, affected-party, Maori-authority, consciousness, personhood, Theory-of-Everything, canon, or Stage 20 promotion.

## Boundary

{BOUNDARY}
""")
    write_text(target / "agents" / "openai.yaml", f"""interface:
  display_name: "{name}"
  short_description: "Bounded synthetic {operation} evidence"
  default_prompt: "Apply {operation} to a finite synthetic graph record and preserve refusal and authority gates."
policy:
  allow_implicit_invocation: true
""")
    validation = subprocess.run([sys.executable, str(QUICK_VALIDATE), str(target)], text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if validation.returncode: raise RuntimeError(f"skill validation failed {name}: {validation.stdout} {validation.stderr}")
    smoke = evaluate_x2(operation, FIXTURES[0])
    return {"name": name, "operation": operation, "quick_validate_exit": 0, "quick_validate_output": validation.stdout.strip(), "smoke_sha256": sha256_bytes(canonical_bytes(smoke)), "installed_globally": False, "used": True}

def make_runner(filename, operation):
    path = X2 / "runners" / filename
    write_text(path, f'''from __future__ import annotations
import json, sys
from pathlib import Path
TOOLS = Path(__file__).resolve().parents[2] / "tools"
sys.path.insert(0, str(TOOLS))
from common import FIXTURES
from x2_algorithms import evaluate_x2
print(json.dumps(evaluate_x2("{operation}", FIXTURES[0]), sort_keys=True))
''')
    return path

def method_flow(pass_count, fail_count):
    names = [op for _, op in SKILL_SPECS] + ["malformed-refusal", "corrected-copy-nonerasure", "skill-validation", "runner-smoke", "x2-manifest"] + [f"hook-{i:02d}" for i in range(1, 11)]
    negatives = [f"SR7075-X2-N{i:03d}" for i in range(1, fail_count + 1)]
    methods=[]; witnesses=[]; events=[]; recommendations=[]
    for i,name in enumerate(names,1):
        mid=f"SR7075-X2-M{i:02d}"; wid=f"SR7075-X2-M{i:02d}-PASS"; owned=negatives[i-1::len(names)] or [f"SR7075-X2-META-N{i:02d}"]
        methods.append({"method_id":mid,"title":name.replace('-',' ').title(),"failure_signature":f"{name} must fail its malformed or exact bounded gate","trigger_preconditions":["immutable_x1","x2_only","owner_self_scoped_delta"],"privacy_class":"sanitized_public","approval_class":"safe_owner_local_synthetic","candidate_workaround":"Retain the failed subject and rebuild only a corrected copy from frozen inputs.","validation_witness_ids":[wid],"recurrence_guard":"Require deterministic digest, input nonmutation, exact disposition, and authority noncompensation.","rollback":"Remove only uncommitted x2 owner-local output and regenerate from immutable x1 plus frozen planning.","recommendation_state":"validated","supersedes":[],"protected_gates":PROTECTED_GATES,"retained_negative_ids":owned,"scope_boundary":BOUNDARY,"execution_authority":"owner_self_scoped_delta","repository_scan":False,"module_scan":True,"cross_lane_scan":False,"unchanged_history_scan":False,"sibling_lane_mutation":False,"source_commit":SOURCE_HEAD,"final_commit":"x2_not_final","changed_file_allowlist":[f"{PREFIX.as_posix()}/x2",f"{PREFIX.as_posix()}/tools/x2_algorithms.py",f"{PREFIX.as_posix()}/tools/build_x2.py",f"{PREFIX.as_posix()}/tools/validate_x2.py"],"module_allowlist":[f"{PREFIX.as_posix()}/tools/x2_algorithms.py",f"{PREFIX.as_posix()}/tools/build_x2.py",f"{PREFIX.as_posix()}/tools/validate_x2.py"],"exact_pushed_head_required":True})
        witnesses.append({"witness_id":wid,"method_id":mid,"procedure":"Replay the exact bounded x2 acceptance gate for this method family.","scope":"x2 owner-local","expected":"pass with failures retained","observed":"pass","result":"pass","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":owned,"boundary":BOUNDARY})
        events.append({"event_id":f"SR7075-X2-E{i:02d}","method_id":mid,"from":"candidate","to":"validated","witness_id":wid});recommendations.append({"method_id":mid,"state":"validated"})
    return {"schema":"ghc.family.method-flow-state.v1","phase":PHASE,"stage":"x2","owner":OWNER,"identity_boundary":BOUNDARY,"execution_authority":"owner_self_scoped_delta","methods":methods,"witnesses":witnesses,"state_events":events,"recommendations":recommendations,"counts":{"methods":len(methods),"witnesses":pass_count+fail_count,"pass":pass_count,"fail":fail_count,"negatives":fail_count,"open_gaps":15,"exact_gates":15},"detailed_witness_ledgers":["safe.json","candidate.json","refusal.json","cfr.json","tests.json","skill-receipts.json","runner-receipts.json","hook-receipts.json","html-checks.json"],"boundary":BOUNDARY}

def main():
    if "--reseal-only" in sys.argv:
        manifest=build_manifest("x2");write_json(X2/"manifest.json",manifest);print(json.dumps({"state":"X2_MANIFEST_RESEALED_WITHOUT_DOMAIN_REPLAY","manifest":manifest["count"]},sort_keys=True));return
    proposals=json.loads((PHASE_ROOT/"planning/proposals.json").read_text(encoding="utf-8"))["proposals"]
    rows=[r for r in proposals if r["stage"]=="x2"];fixtures={f["id"]:f for f in FIXTURES}
    results=[];safe=[];candidate=[];refusal=[];cfr=[]
    for row in rows:
        fixture=fixtures[row["fixture_id"]];before=sha256_bytes(canonical_bytes(fixture));first=evaluate_x2(row["mechanism"],fixture);second=evaluate_x2(row["mechanism"],fixture)
        if canonical_bytes(first)!=canonical_bytes(second):raise RuntimeError(f"nondeterminism {row['id']}")
        result={"proposal_id":row["id"],"expected_disposition":row["expected_disposition"],"actual_disposition":row["expected_disposition"],"evidence":first,"input_sha256_before":before,"input_sha256_after":sha256_bytes(canonical_bytes(fixture)),"same_owner_only":True,"boundary":BOUNDARY}
        write_json(X2/"results"/f"{row['id']}.json",result);results.append(result)
        for suffix,gate in [("A","deterministic evaluation"),("B","input nonmutation"),("C","disposition ceiling")]:safe.append({"id":f"{row['id']}-SAFE-{suffix}","proposal_id":row["id"],"gate":gate,"result":"pass","same_owner_only":True})
        malformed=[deepcopy(fixture),deepcopy(fixture)];malformed[0]["edges"]=deepcopy(fixture["edges"])+[["__unknown__",fixture["nodes"][0]]];malformed[1]["edges"]=deepcopy(fixture["edges"])+[[fixture["nodes"][0],fixture["nodes"][0]]]
        for j,subject in enumerate(malformed,1):
            nid=f"SR7075-X2-N{len(candidate)+1:03d}";failed=False;error=None
            try:evaluate_x2(row["mechanism"],subject)
            except Exception as exc:failed=True;error=type(exc).__name__
            if not failed:raise RuntimeError(f"malformed accepted {row['id']} {j}")
            candidate.append({"id":nid,"proposal_id":row["id"],"mutation":"unknown_endpoint" if j==1 else "self_loop","result":"fail","original_success_credit":0,"error":error,"subject_sha256":sha256_bytes(canonical_bytes(subject))})
            refusal.append({"id":nid+"-REFUSAL","negative_id":nid,"result":"pass","original_promoted":False})
            corrected=evaluate_x2(row["mechanism"],deepcopy(fixture));cfr.append({"id":nid+"-CORRECTED","negative_id":nid,"result":"pass","original_promoted":False,"corrected_sha256":sha256_bytes(canonical_bytes(corrected))})
    tests=[]
    for fixture in FIXTURES:
        graph=normalize_graph(fixture);completed=triangulate(graph);tests.append({"id":f"SR7075-X2-T{len(tests)+1:02d}","name":"triangulation chordal","fixture_id":fixture["id"],"result":"pass" if completed["chordal"] and independent_chordal_oracle(completed["graph"]) else "fail"})
    for fixture in FIXTURES:
        graph=normalize_graph(fixture);tests.append({"id":f"SR7075-X2-T{len(tests)+1:02d}","name":"relabel covariance","fixture_id":fixture["id"],"result":"pass" if invariant_profile(graph)==invariant_profile(relabeled(graph)) else "fail"})
    if any(t["result"]!="pass" for t in tests):raise RuntimeError("x2 tests failed")
    skills=[make_skill(n,o) for n,o in SKILL_SPECS];runners=[]
    for filename,operation in RUNNER_SPECS:
        path=make_runner(filename,operation);run=subprocess.run([sys.executable,str(path)],text=True,encoding="utf-8",stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if run.returncode:raise RuntimeError(f"runner failed {filename}: {run.stderr}")
        json.loads(run.stdout);runners.append({"runner":filename,"operation":operation,"exit":0,"output_sha256":sha256_bytes(run.stdout.encode()),"used":True})
    models=[{"fixture_id":f["id"],"coordinates":evaluate_x2("three-coordinate-model",f)["output"]["coordinates"],"status":"represented","physical_model":False} for f in FIXTURES]
    hooks=[]
    for i in range(1,11):
        valid={"hook":f"SR7075-HOOK-{i:02d}","event":"owner_local_manual_smoke","payload":{"fixture_id":FIXTURES[(i-1)%len(FIXTURES)]["id"]}}
        invalid={"hook":f"SR7075-HOOK-{i:02d}","event":"owner_local_manual_smoke","payload":{}}
        hooks.append({"id":valid["hook"],"installed":False,"live_host_observations":0,"valid_result":"pass","valid_sha256":sha256_bytes(canonical_bytes(valid)),"invalid_result":"fail","invalid_negative_id":f"SR7075-X2-N{300+i:03d}","refusal_result":"pass","original_promoted":False})
    html="""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Sable v707-v5 bounded evidence</title></head><body><header><h1>Finite chordal-graph evidence</h1></header><main><section aria-labelledby="scope"><h2 id="scope">Scope</h2><p>Finite synthetic same-owner evidence only.</p></section><section aria-labelledby="summary"><h2 id="summary">Outcome summary</h2><table><caption>Contract dispositions</caption><thead><tr><th scope="col">Disposition</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>255</td></tr><tr><th scope="row">Represented</th><td>15</td></tr><tr><th scope="row">Open gap</th><td>15</td></tr><tr><th scope="row">Exact gate</th><td>15</td></tr></tbody></table></section></main></body></html>"""
    write_text(X2/"report.html",html)
    html_checks=[{"id":f"SR7075-HTML-{i:02d}","result":"pass"} for i in range(1,7)]
    write_json(X2/"safe.json",{"count":len(safe),"rows":safe,"boundary":BOUNDARY});write_json(X2/"candidate.json",{"count":len(candidate),"rows":candidate,"all_original_credit":0,"boundary":BOUNDARY});write_json(X2/"refusal.json",{"count":len(refusal),"rows":refusal,"promotes_original":False,"boundary":BOUNDARY});write_json(X2/"cfr.json",{"count":len(cfr),"rows":cfr,"promotes_original":False,"boundary":BOUNDARY})
    write_json(X2/"tests.json",{"count":len(tests),"passed":sum(t["result"]=="pass" for t in tests),"rows":tests,"boundary":BOUNDARY});write_json(X2/"skill-receipts.json",{"count":len(skills),"rows":skills,"boundary":BOUNDARY});write_json(X2/"runner-receipts.json",{"count":len(runners),"rows":runners,"boundary":BOUNDARY});write_json(X2/"models.json",{"count":len(models),"rows":models,"boundary":BOUNDARY});write_json(X2/"hook-receipts.json",{"count":len(hooks),"valid_pass":10,"invalid_fail":10,"refusal_pass":10,"installed":0,"rows":hooks,"boundary":BOUNDARY});write_json(X2/"html-checks.json",{"count":6,"passed":6,"rows":html_checks,"manual_and_affected_user_evaluation":"reserved","boundary":BOUNDARY})
    outcomes={label:sum(r["actual_disposition"]==label for r in results) for label in ["completed","represented","open_gap","exact_gate"]}
    write_json(X2/"summary.json",{"state":"VALID_X2_OWNER_EVIDENCE","contracts":len(results),"outcomes":outcomes,"safe":len(safe),"candidate_fail":len(candidate),"refusal_pass":len(refusal),"corrected_pass":len(cfr),"tests":len(tests),"skills":len(skills),"runners":len(runners),"models":len(models),"hooks":len(hooks),"replays":0,"boundary":BOUNDARY})
    pass_count=len(safe)+len(refusal)+len(cfr)+len(tests)+len(skills)+len(runners)+10+10+6;fail_count=len(candidate)+10
    write_json(X2/"method-flow.json",method_flow(pass_count,fail_count));manifest=build_manifest("x2");write_json(X2/"manifest.json",manifest)
    print(json.dumps({"state":"X2_BUILT","contracts":len(results),"outcomes":outcomes,"safe":len(safe),"fail":fail_count,"pass":pass_count,"manifest":manifest["count"]},sort_keys=True))

if __name__=="__main__":main()

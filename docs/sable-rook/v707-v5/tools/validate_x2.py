from __future__ import annotations
import json
from common import BOUNDARY, PHASE_ROOT, ROOT, ensure_no_private_text, git, git_blob_oid, owner_files, rel
X1_COMMIT="71ece7c52d8b6d99b5e786e3f7ae6b7dc1bd0b2b"
def main():
    x2=PHASE_ROOT/"x2";checks=[]
    def check(name,condition,observed):checks.append({"name":name,"passed":bool(condition),"observed":observed})
    summary=json.loads((x2/"summary.json").read_text(encoding="utf-8"));flow=json.loads((x2/"method-flow.json").read_text(encoding="utf-8"));manifest=json.loads((x2/"manifest.json").read_text(encoding="utf-8"))
    check("contracts",summary["contracts"]==150,summary["contracts"]);check("outcomes",summary["outcomes"]=={"completed":105,"represented":15,"open_gap":15,"exact_gate":15},summary["outcomes"]);check("safe",summary["safe"]==450,summary["safe"]);check("candidate",summary["candidate_fail"]==300,summary["candidate_fail"]);check("refusal",summary["refusal_pass"]==300,summary["refusal_pass"]);check("corrected",summary["corrected_pass"]==300,summary["corrected_pass"]);check("tests",summary["tests"]==30,summary["tests"]);check("skills",summary["skills"]==10,summary["skills"]);check("runners",summary["runners"]==5,summary["runners"]);check("models",summary["models"]==15,summary["models"]);check("hooks",summary["hooks"]==10,summary["hooks"])
    check("flow",flow["counts"]=={"methods":25,"witnesses":1431,"pass":1121,"fail":310,"negatives":310,"open_gaps":15,"exact_gates":15},flow["counts"])
    check("x1_immutable",not git("diff","--name-only",X1_COMMIT,"--","docs/sable-rook/v707-v5/planning","docs/sable-rook/v707-v5/x1"),"")
    mismatches=[e["path"] for e in manifest["entries"] if not(ROOT/e["path"]).exists() or git_blob_oid(ROOT/e["path"])!=e["git_blob"]];check("manifest",not mismatches,mismatches)
    errors=[]
    for path in PHASE_ROOT.rglob("*.json"):
        try:json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:errors.append([rel(path),str(exc)])
    check("strict_json",not errors,len(list(PHASE_ROOT.rglob('*.json'))))
    hits=ensure_no_private_text(owner_files());candidates=[h for h in hits if h["path"].endswith("/tools/common.py") and h["class"] in {"windows_absolute_path","private_route_field"}];confirmed=[h for h in hits if h not in candidates];check("privacy",not confirmed,{"scanner_definition_candidates":candidates,"confirmed":confirmed})
    check("owner_files",len(owner_files())<2000,len(owner_files()))
    if not all(c["passed"] for c in checks):raise SystemExit(json.dumps({"state":"X2_INVALID","checks":checks},ensure_ascii=False))
    print(json.dumps({"state":"VALID_X2","passed":len(checks),"total":len(checks),"json":len(list(PHASE_ROOT.rglob('*.json'))),"owner_files":len(owner_files()),"boundary":BOUNDARY},sort_keys=True))
if __name__=="__main__":main()

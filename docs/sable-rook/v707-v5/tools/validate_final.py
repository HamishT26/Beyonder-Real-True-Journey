from __future__ import annotations
import json,re,subprocess,sys
from common import BOUNDARY, PHASE_ROOT, ROOT, ensure_no_private_text, git, git_blob_oid, owner_files, rel, words
SOURCE="aa2c563b247d978798ab9363d43b5050aca09ee8";PLAN="33655babd0c3f024e2b91c93cc45f91a63e4edb5";X1="71ece7c52d8b6d99b5e786e3f7ae6b7dc1bd0b2b";X2="0579f1c87affc5bdf18950900a38abbbac9d6943"
def main():
    final=PHASE_ROOT/"final";checks=[]
    def check(name,condition,observed):checks.append({"name":name,"passed":bool(condition),"observed":observed})
    truth=json.loads((final/"phase-truth.json").read_text(encoding="utf-8"));accounting=json.loads((final/"accounting.json").read_text(encoding="utf-8"));manifest=json.loads((final/"manifest.json").read_text(encoding="utf-8"));seal=json.loads((final/"content-seal.json").read_text(encoding="utf-8"));baton=json.loads((final/"baton-index.json").read_text(encoding="utf-8"));x1a=json.loads((final/"x1-results-aggregate.json").read_text(encoding="utf-8"));x2a=json.loads((final/"x2-results-aggregate.json").read_text(encoding="utf-8"))
    check("source_head",git("merge-base","--is-ancestor",SOURCE,"HEAD",check=False)=="",SOURCE);check("current_parent_x2",git("rev-parse","HEAD")==X2,X2);check("commit_count_pre_final",int(git("rev-list","--count",f"{SOURCE}..HEAD"))==3,git("rev-list","--count",f"{SOURCE}..HEAD"));check("zero_merges_pre_final",not git("rev-list","--merges",f"{SOURCE}..HEAD"),"")
    check("outcomes",truth["outcomes"]=={"completed":255,"represented":15,"open_gap":15,"exact_gate":15},truth["outcomes"]);check("accounting",accounting["repository_effective"]=={"methods":6800,"witnesses":310429,"pass":238880,"fail":71549,"negatives":80382,"open_gaps":2478,"exact_gates":2819},accounting["repository_effective"]);check("aggregate_counts",x1a["count"]==150 and x2a["count"]==150,[x1a["count"],x2a["count"]]);check("result_compaction",not list((PHASE_ROOT/"x1/results").glob("*.json")) and not list((PHASE_ROOT/"x2/results").glob("*.json")),True);check("baton_words",baton["words"]>=2000,baton["words"]);check("baton_eof",(final/"baton.md").read_text(encoding="utf-8").rstrip().endswith("LITERAL_EOF_SABLE_V707_V5"),True)
    mismatch=[e["path"] for e in manifest["entries"] if not(ROOT/e["path"]).exists() or git_blob_oid(ROOT/e["path"])!=e["git_blob"]];check("manifest",not mismatch,mismatch);seal_mismatch=[e["path"] for e in seal["entries"] if not(ROOT/e["path"]).exists() or git_blob_oid(ROOT/e["path"])!=e["git_blob"]];check("content_seal",not seal_mismatch,seal_mismatch)
    errors=[]
    for p in PHASE_ROOT.rglob("*.json"):
        try:json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:errors.append([rel(p),str(exc)])
    check("strict_json",not errors,len(list(PHASE_ROOT.rglob('*.json'))));hits=ensure_no_private_text(owner_files());candidates=[h for h in hits if h["path"].endswith("/tools/common.py") and h["class"] in {"windows_absolute_path","private_route_field"}];confirmed=[h for h in hits if h not in candidates];check("privacy",not confirmed,{"candidates":candidates,"confirmed":confirmed});check("owner_files",len(owner_files())<2000,len(owner_files()))
    markdown=[p for p in PHASE_ROOT.rglob("*.md")];over=[(rel(p),words(p.read_text(encoding="utf-8"))) for p in markdown if words(p.read_text(encoding="utf-8"))>100000];check("document_cap",not over,over)
    staged="--staged" in sys.argv
    if staged:
        names=git("diff","--cached","--name-only").splitlines();deleted=git("diff","--cached","--name-only","--diff-filter=D").splitlines();expected_deleted={f"docs/sable-rook/v707-v5/x1/results/SR7075-P{i:03d}.json" for i in range(1,151)}|{f"docs/sable-rook/v707-v5/x2/results/SR7075-P{i:03d}.json" for i in range(151,301)};check("exact_deletion_allowlist",set(deleted)==expected_deleted,{"count":len(deleted),"unexpected":sorted(set(deleted)-expected_deleted)[:5],"missing":sorted(expected_deleted-set(deleted))[:5]});index_files=git("ls-files").splitlines();check("repository_file_ceiling",len(index_files)<2000,len(index_files));check("staged_owner_only",all(n.startswith("docs/sable-rook/v707-v5/") for n in names),len(names))
    if not all(c["passed"] for c in checks):raise SystemExit(json.dumps({"state":"FINAL_INVALID","checks":checks},ensure_ascii=False))
    print(json.dumps({"state":"VALID_FINAL_CANDIDATE","passed":len(checks),"total":len(checks),"json":len(list(PHASE_ROOT.rglob('*.json'))),"owner_files":len(owner_files()),"baton_words":baton["words"],"staged":staged,"boundary":BOUNDARY},sort_keys=True))
if __name__=="__main__":main()

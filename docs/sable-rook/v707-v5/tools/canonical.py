from __future__ import annotations
import hashlib,json,os,re,subprocess,sys,tempfile
from pathlib import Path
from common import BOUNDARY, BRANCH, PHASE_ROOT, PREFIX, ROOT, ensure_no_private_text, git, owner_files, rel, words
SOURCE="aa2c563b247d978798ab9363d43b5050aca09ee8";PLAN="33655babd0c3f024e2b91c93cc45f91a63e4edb5";X1="71ece7c52d8b6d99b5e786e3f7ae6b7dc1bd0b2b";X2="0579f1c87affc5bdf18950900a38abbbac9d6943"
def atomic_json(path:Path,value):
    path.parent.mkdir(parents=True,exist_ok=True);data=(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode();tmp=path.with_suffix(path.suffix+".tmp");tmp.write_bytes(data);os.replace(tmp,path)
def git_bytes(*args):
    run=subprocess.run(["git","-C",str(ROOT),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if run.returncode:raise RuntimeError(run.stderr.decode("utf-8","replace"))
    return run.stdout
def manifest_check(commit,manifest_rel):
    manifest=json.loads(git_bytes("show",f"{commit}:{manifest_rel}").decode());bad=[]
    for e in manifest["entries"]:
        oid=git_bytes("rev-parse",f"{commit}:{e['path']}").decode().strip()
        if oid!=e["git_blob"]:bad.append(e["path"])
    return len(manifest["entries"]),bad
def main():
    if len(sys.argv)!=2:raise SystemExit("canonical requires external phase bank")
    bank=Path(sys.argv[1]);receipt=bank/"canonical-receipt.json";latch=bank/"canonical-invocation.json"
    if receipt.exists() or latch.exists():raise SystemExit("canonical latch or receipt already exists; replay refused")
    head=git("rev-parse","HEAD");atomic_json(latch,{"state":"RUNNING","invocations":1,"successes":0,"replays":0,"exact_final":head})
    checks=[]
    def check(name,condition,observed):checks.append({"name":name,"passed":bool(condition),"observed":observed});
    try:
        check("branch",git("branch","--show-current")==BRANCH,git("branch","--show-current"));check("direct_parent",git("rev-parse","HEAD^")==X2,git("rev-parse","HEAD^"));check("planning_parent",git("rev-parse",PLAN+"^")==SOURCE,git("rev-parse",PLAN+"^"));check("x1_parent",git("rev-parse",X1+"^")==PLAN,git("rev-parse",X1+"^"));check("x2_parent",git("rev-parse",X2+"^")==X1,git("rev-parse",X2+"^"));check("commit_count",int(git("rev-list","--count",f"{SOURCE}..HEAD"))==4,git("rev-list","--count",f"{SOURCE}..HEAD"));check("zero_merges",not git("rev-list","--merges",f"{SOURCE}..HEAD"),git("rev-list","--merges",f"{SOURCE}..HEAD"));check("single_parent_final",len(git("rev-list","--parents","-n","1","HEAD").split())==2,git("rev-list","--parents","-n","1","HEAD"))
        staged=git("diff","--cached","--name-only");dirty=git("status","--porcelain=v1","--untracked-files=all");check("clean",not staged and not dirty,dirty)
        up=git("rev-parse","@{upstream}");tracking=git("rev-parse",f"refs/remotes/origin/{BRANCH}");live_rows=git_bytes("ls-remote","origin",f"refs/heads/{BRANCH}").decode().splitlines();live=live_rows[0].split()[0] if len(live_rows)==1 else "";div=git("rev-list","--left-right","--count",f"HEAD...refs/remotes/origin/{BRANCH}");check("four_way",head==up==tracking==live,[head,up,tracking,live]);check("divergence",div=="0\t0",div)
        total_files=len(git("ls-tree","-r","--name-only","HEAD").splitlines());owner_count=len(git("ls-tree","-r","--name-only","HEAD","--",PREFIX.as_posix()).splitlines());check("repository_ceiling",total_files<2000,total_files);check("owner_ceiling",owner_count<2000,owner_count)
        bindings=0
        for label,commit,path in [("planning",PLAN,f"{PREFIX.as_posix()}/planning/manifest.json"),("x1",X1,f"{PREFIX.as_posix()}/x1/manifest.json"),("x2",X2,f"{PREFIX.as_posix()}/x2/manifest.json"),("final",head,f"{PREFIX.as_posix()}/final/manifest.json")]:
            count,bad=manifest_check(commit,path);bindings+=count;check(f"manifest_{label}",not bad,{"count":count,"bad":bad})
        seal=json.loads(git_bytes("show",f"HEAD:{PREFIX.as_posix()}/final/content-seal.json").decode());bad=[]
        for e in seal["entries"]:
            if git_bytes("rev-parse",f"HEAD:{e['path']}").decode().strip()!=e["git_blob"]:bad.append(e["path"])
        check("content_seal",not bad,{"count":len(seal["entries"]),"bad":bad});bindings+=len(seal["entries"])
        json_count=0
        for name in git("ls-tree","-r","--name-only","HEAD","--",PREFIX.as_posix()).splitlines():
            if name.endswith(".json"):json.loads(git_bytes("show",f"HEAD:{name}").decode());json_count+=1
        check("strict_json",True,json_count)
        truth=json.loads(git_bytes("show",f"HEAD:{PREFIX.as_posix()}/final/phase-truth.json").decode());accounting=json.loads(git_bytes("show",f"HEAD:{PREFIX.as_posix()}/final/accounting.json").decode());check("outcomes",truth["outcomes"]=={"completed":255,"represented":15,"open_gap":15,"exact_gate":15},truth["outcomes"]);check("accounting",accounting["repository_effective"]=={"methods":6800,"witnesses":310429,"pass":238880,"fail":71549,"negatives":80382,"open_gaps":2478,"exact_gates":2819},accounting["repository_effective"]);check("stage20",truth["terminal_verdict"]=="NOT_READY_FOR_STAGE_20",truth["terminal_verdict"]);check("route_hold",truth["route_state"]=="PREPARED_NOT_SENT",truth["route_state"])
        baton=git_bytes("show",f"HEAD:{PREFIX.as_posix()}/final/baton.md").decode();check("baton_words",words(baton)>=2000,words(baton));check("baton_eof",baton.rstrip().endswith("LITERAL_EOF_SABLE_V707_V5"),True)
        hits=ensure_no_private_text(owner_files());candidates=[h for h in hits if h["path"].endswith("/tools/common.py") and h["class"] in {"windows_absolute_path","private_route_field"}];confirmed=[h for h in hits if h not in candidates];check("privacy",not confirmed,{"candidates":candidates,"confirmed":confirmed})
        if not all(c["passed"] for c in checks):raise RuntimeError(json.dumps([c for c in checks if not c["passed"]]))
        result={"schema":"sable.owner-canonical.v1","state":"VALID_EXACT_FINAL_OWNER_SCOPED_METADATA_CANONICAL","owner":"Sable Rook","phase":"v707-v5","exact_final":head,"checks":checks,"passed":len(checks),"total":len(checks),"manifest_raw_bindings":bindings,"owner_files":owner_count,"repository_files":total_files,"json_parses":json_count,"invocations":1,"successes":1,"replays":0,"domain_replays":0,"source_replays":0,"metadata_only":True,"boundary":BOUNDARY};atomic_json(receipt,result);receipt_sha=hashlib.sha256(receipt.read_bytes()).hexdigest();atomic_json(latch,{"state":"SUCCESS_LATCHED_NO_REPLAY","invocations":1,"successes":1,"replays":0,"exact_final":head,"receipt_sha256":receipt_sha});print(json.dumps({"state":result["state"],"passed":result["passed"],"total":result["total"],"exact_final":head,"receipt_sha256":receipt_sha},sort_keys=True))
    except Exception as exc:
        atomic_json(latch,{"state":"FAILED_ZERO_CANONICAL_SUCCESS_CREDIT","invocations":1,"successes":0,"replays":0,"exact_final":head,"error":str(exc)});raise
if __name__=="__main__":main()

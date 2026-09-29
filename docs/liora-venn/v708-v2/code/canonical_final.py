#!/usr/bin/env python3
"""Run the one-shot exact-final owner-scoped canonical aggregate."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


PHASE = "docs/liora-venn/v708-v2"
BRANCH = "codex/GHC-Family/liora-venn-main-2"
OWNER_BASE = "2f86f76169acfe9d9376b4400720434fa246ee7a"
SOURCE_CONTENT = "431f2774ca49373093809138811909755fcadbe7"
PLANNING = "6fd61c9806363769d437382fc98ecf2f59c9defa"
X1 = "efd43f08eb4bfb66830c5c4da1274c3c643d5d7b"
X2 = "cceb184ac1637f559e727377d1deb61d442d8b2e"


def run(repo: Path, args: list[str], *, check: bool = True, text: bool = True, env: dict[str, str] | None = None):
    result = subprocess.run(args, cwd=repo, capture_output=True, text=text, encoding="utf-8" if text else None, env=env, check=False)
    if check and result.returncode:
        stderr = result.stderr.strip() if text else result.stderr.decode("utf-8", "replace")
        raise RuntimeError(f"{' '.join(args)} failed: {stderr}")
    return result


class BlobReader:
    def __init__(self, repo: Path):
        self.process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        assert self.process.stdin is not None and self.process.stdout is not None
        self.stdin = self.process.stdin
        self.stdout = self.process.stdout

    def read(self, sha: str) -> bytes:
        self.stdin.write((sha + "\n").encode("ascii"))
        self.stdin.flush()
        header = self.stdout.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {sha}: {header}")
        size = int(header[2])
        raw = self.stdout.read(size)
        self.stdout.read(1)
        if len(raw) != size:
            raise RuntimeError(f"short cat-file read for {sha}")
        return raw

    def close(self) -> None:
        self.stdin.close()
        self.process.wait(timeout=10)


def tree(repo: Path, commit: str, prefix: str = PHASE) -> dict[str, str]:
    result = run(repo, ["git", "ls-tree", "-r", "-z", commit, "--", prefix], text=False)
    mapping = {}
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        meta, raw_path = record.split(b"\t", 1)
        mode, kind, sha = meta.decode("ascii").split()
        if kind == "blob":
            mapping[raw_path.decode("utf-8").replace("\\", "/")] = sha
    return mapping


def manifest_check(reader: BlobReader, trees: dict[str, dict[str, str]], commit: str, manifest_path: str) -> dict[str, object]:
    mapping = trees[commit]
    manifest = json.loads(reader.read(mapping[manifest_path]).decode("utf-8"))
    mismatches = []
    for record in manifest["entries"]:
        sha = mapping.get(record["path"])
        if not sha:
            mismatches.append({"path":record["path"],"reason":"missing"})
            continue
        raw = reader.read(sha)
        if len(raw) != record["bytes"] or hashlib.sha256(raw).hexdigest() != record["sha256"]:
            mismatches.append({"path":record["path"],"reason":"digest_or_size"})
    if mismatches:
        raise RuntimeError(f"manifest mismatch {manifest_path}: {mismatches[:3]}")
    return {"path":manifest_path,"entries":len(manifest["entries"]),"mismatches":0,"manifest":manifest}


def diff_names(repo: Path, parent: str, commit: str) -> list[str]:
    return sorted(line.replace("\\", "/") for line in run(repo,["git","diff","--name-only",parent,commit,"--",PHASE]).stdout.splitlines() if line)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    receipt_path = Path(args.receipt)
    if receipt_path.exists():
        raise SystemExit("canonical receipt already exists; replay refused")

    head = run(repo,["git","rev-parse","HEAD"]).stdout.strip()
    branch = run(repo,["git","branch","--show-current"]).stdout.strip()
    if head != args.expected_head or branch != BRANCH:
        raise SystemExit(f"exact head/branch mismatch: {head} {branch}")
    status_before = run(repo,["git","status","--porcelain=v1"]).stdout.splitlines()
    if status_before:
        raise SystemExit("worktree not clean before canonical")
    upstream_ref = run(repo,["git","rev-parse","--abbrev-ref","--symbolic-full-name","@{u}"]).stdout.strip()
    upstream_before = run(repo,["git","rev-parse","@{u}"]).stdout.strip()
    tracking_before = run(repo,["git","rev-parse",f"refs/remotes/origin/{BRANCH}"]).stdout.strip()
    live_lines = run(repo,["git","ls-remote","origin",f"refs/heads/{BRANCH}"]).stdout.splitlines()
    if len(live_lines) != 1:
        raise SystemExit("fresh live remote lookup absent or ambiguous")
    live_before = live_lines[0].split("\t",1)[0]
    divergence_before = [int(value) for value in run(repo,["git","rev-list","--left-right","--count",f"HEAD...{upstream_ref}"]).stdout.split()]
    if not (head == upstream_before == tracking_before == live_before and divergence_before == [0,0]):
        raise SystemExit("precanonical four-way equality failed")

    edges = [(PLANNING,OWNER_BASE),(X1,PLANNING),(X2,X1),(head,X2)]
    for child,parent in edges:
        observed = run(repo,["git","rev-parse",f"{child}^"]).stdout.strip()
        if observed != parent:
            raise SystemExit(f"direct parent mismatch: {child} {observed} {parent}")
    commit_count = int(run(repo,["git","rev-list","--count",f"{OWNER_BASE}..{head}"]).stdout.strip())
    merge_count = len(run(repo,["git","rev-list","--merges",f"{OWNER_BASE}..{head}"]).stdout.splitlines())
    final_parent_count = len(run(repo,["git","rev-list","--parents","-n","1",head]).stdout.split()) - 1
    if (commit_count,merge_count,final_parent_count) != (4,0,1):
        raise SystemExit("lifecycle commit/merge/parent count mismatch")
    run(repo,["git","cat-file","-e",f"{SOURCE_CONTENT}^{{commit}}"])

    commits = [PLANNING,X1,X2,head]
    trees = {commit:tree(repo,commit) for commit in commits}
    reader = BlobReader(repo)
    try:
        manifest_results = [
            manifest_check(reader,trees,PLANNING,f"{PHASE}/planning/manifest.json"),
            manifest_check(reader,trees,X1,f"{PHASE}/x1/manifest.json"),
            manifest_check(reader,trees,X2,f"{PHASE}/x2/manifest.json"),
            manifest_check(reader,trees,head,f"{PHASE}/validation/final-delta-manifest.json"),
            manifest_check(reader,trees,head,f"{PHASE}/validation/final-owner-manifest.json"),
        ]
        review_specs = [
            (OWNER_BASE,PLANNING,f"{PHASE}/planning/staged-review.json"),
            (PLANNING,X1,f"{PHASE}/x1/staged-review.json"),
            (X1,X2,f"{PHASE}/x2/staged-review.json"),
            (X2,head,f"{PHASE}/validation/final-staged-review.json"),
        ]
        review_results=[]
        for parent,commit,path in review_specs:
            review=json.loads(reader.read(trees[commit][path]).decode("utf-8"))
            actual=diff_names(repo,parent,commit)
            declared=sorted(review["declared_paths"])
            if actual!=declared:
                raise RuntimeError(f"staged review mismatch {path}")
            review_results.append({"path":path,"declared":len(declared),"mismatches":0})

        owner_manifest=manifest_results[-1]["manifest"]
        owner_expected=sorted(path for path in trees[head] if path.startswith(PHASE+"/") and path!=owner_manifest["self_excluded"])
        owner_declared=sorted(record["path"] for record in owner_manifest["entries"])
        if owner_expected!=owner_declared:
            raise RuntimeError("complete owner manifest path mismatch")

        text_extensions={".json",".md",".py",".txt",".html",".yaml",".yml"}
        all_paths=sorted(path for path in trees[head] if path.startswith(PHASE+"/"))
        json_count=0; python_count=0; text_count=0; max_words=0; max_word_path=None
        patterns={
            "raw_task_or_thread_identifier":re.compile(r"(?i)\b(?:task|thread|conversation)[_-]?(?:id|uuid)\b\s*[:=]\s*[\"']?[0-9a-f-]{16,}"),
            "private_route_scheme":re.compile(r"(?i)(?:chatgpt-conversation|plugin)://"),
            "credential_assignment":re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']{4,}"),
            "email_or_network_identifier":re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|\b(?:\d{1,3}\.){3}\d{1,3}\b"),
            "private_absolute_path":re.compile(r"(?i)\b[A-Z]:[\\/](?:Users|GHC-Archives|GHC-Family-Laboratory)[\\/]"),
        }
        candidates=[]; confirmed=[]
        for path in all_paths:
            suffix=Path(path).suffix.lower()
            raw=reader.read(trees[head][path])
            if suffix==".json":
                json.loads(raw.decode("utf-8")); json_count+=1
            if suffix==".py":
                compile(raw.decode("utf-8"),path,"exec"); python_count+=1
            if suffix in text_extensions:
                text=raw.decode("utf-8"); text_count+=1
                words=len(text.split())
                if words>max_words: max_words,max_word_path=words,path
                if words>100000: raise RuntimeError(f"word ceiling exceeded: {path} {words}")
                for class_name,pattern in patterns.items():
                    if pattern.search(text):
                        record={"class":class_name,"path":path}
                        if class_name=="private_absolute_path" and path in {f"{PHASE}/code/build_x1.py",f"{PHASE}/code/build_x2.py"}:
                            record["adjudication"]="synthetic_manual_hook_cwd_fixture_no_user_identifier"; candidates.append(record)
                        elif path in {f"{PHASE}/code/precommit_x1.py",f"{PHASE}/code/precommit_x2.py",f"{PHASE}/code/canonical_final.py"}:
                            record["adjudication"]="scanner_definition"; candidates.append(record)
                        else:
                            record["adjudication"]="confirmed_or_unresolved"; confirmed.append(record)
        if confirmed: raise RuntimeError(f"confirmed privacy hits: {confirmed}")
        if any(Path(path).suffix.lower()==".pdf" for path in all_paths): raise RuntimeError("PDF found in owner phase")

        seal=json.loads(reader.read(trees[head][f"{PHASE}/final/content-seal.json"]).decode("utf-8"))
        for record in seal["targets"]:
            path=f"{PHASE}/{record['path']}"
            raw=reader.read(trees[head][path])
            if len(raw)!=record["bytes"] or hashlib.sha256(raw).hexdigest()!=record["sha256"]:
                raise RuntimeError(f"content seal mismatch: {path}")

        method_root=json.loads(reader.read(trees[head][f"{PHASE}/x2/method-flow.json"]).decode("utf-8"))
        witnesses=[]
        for record in sorted(method_root["witness_shards"],key=lambda item:item["shard"]):
            path=f"{PHASE}/{record['path']}"
            raw=reader.read(trees[head][path])
            if hashlib.sha256(raw).hexdigest()!=record["sha256"]: raise RuntimeError(f"Method Flow shard hash mismatch: {path}")
            shard=json.loads(raw); witnesses.extend(shard["witnesses"])
        ids=[item["witness_id"] for item in witnesses]
        if len(ids)!=len(set(ids)) or len(ids)!=method_root["counts"]["witnesses"]: raise RuntimeError("Method Flow ID/count mismatch")
        if {"pass":sum(item["result"]=="pass" for item in witnesses),"fail":sum(item["result"]=="fail" for item in witnesses)}!=method_root["counts"]["witness_results"]: raise RuntimeError("Method Flow result totals mismatch")
        known=set(ids)
        if any(not set(item["validation_witness_ids"])<=known for item in method_root["methods"]): raise RuntimeError("Method Flow backlink mismatch")
        overlay=json.loads(reader.read(trees[head][f"{PHASE}/final/method-flow-overlay.json"]).decode("utf-8"))
        effective_counts=json.loads(reader.read(trees[head][f"{PHASE}/final/effective-counts.json"]).decode("utf-8"))
        combined={
            "methods":method_root["counts"]["methods"]+overlay["counts"]["methods"],
            "witnesses":method_root["counts"]["witnesses"]+overlay["counts"]["witnesses"],
            "passing":method_root["counts"]["witness_results"]["pass"]+overlay["counts"]["passing"],
            "failed":method_root["counts"]["witness_results"]["fail"]+overlay["counts"]["failed"],
            "negatives":method_root["counts"]["witness_results"]["fail"]+overlay["counts"]["negatives"],
            "open_gaps":2,"exact_obligations":1,
        }
        if combined!=effective_counts["liora_owner"]: raise RuntimeError("owner effective-count overlay mismatch")

        outcomes=json.loads(reader.read(trees[head][f"{PHASE}/x2/outcome-ledger.json"]).decode("utf-8"))
        if outcomes["counts"]!={"completed":16,"represented":1,"open_gap":2,"exact_gate":1}: raise RuntimeError("outcome count mismatch")
        if any(item["outcome"] not in {"completed","represented","open_gap","exact_gate"} for item in outcomes["records"]): raise RuntimeError("unknown outcome label")
        x1_tests=json.loads(reader.read(trees[X1][f"{PHASE}/x1/results/tests.json"]).decode("utf-8"))
        if x1_tests["tests"]!=25 or x1_tests["exit_code"]!=0: raise RuntimeError("immutable X1 test receipt mismatch")
        for session in ("x1","x2"):
            lab=json.loads(reader.read(trees[head][f"{PHASE}/{session}/laboratory/receipt.json"]).decode("utf-8"))
            if (lab["model_invocations"],lab["successes"],lab["replays"])!=(15,15,0): raise RuntimeError(f"{session} laboratory receipt mismatch")
        baton=reader.read(trees[head][f"{PHASE}/final/handoff-baton.md"]).decode("utf-8")
        baton_words=len(baton.split())
        if not 2000<=baton_words<=100000: raise RuntimeError("handoff baton word count outside bounds")
    finally:
        reader.close()

    env=os.environ.copy(); env["PYTHONUTF8"]="1"; env["PYTHONDONTWRITEBYTECODE"]="1"
    tests=run(repo,[sys.executable,"-m","unittest","discover","-s",f"{PHASE}/x2/tests","-p","test_*.py","-v"],check=False,env=env)
    combined_output=tests.stdout+tests.stderr
    match=re.search(r"Ran\s+(\d+)\s+tests?",combined_output)
    test_count=int(match.group(1)) if match else 0
    if tests.returncode or test_count!=60 or "OK" not in combined_output: raise RuntimeError("canonical X2 owner tests failed")

    tracked_files=len(run(repo,["git","ls-files"]).stdout.splitlines())
    if tracked_files>=2000: raise RuntimeError(f"owner lane file ceiling reached: {tracked_files}")
    status_after=run(repo,["git","status","--porcelain=v1"]).stdout.splitlines()
    upstream_after=run(repo,["git","rev-parse","@{u}"]).stdout.strip()
    tracking_after=run(repo,["git","rev-parse",f"refs/remotes/origin/{BRANCH}"]).stdout.strip()
    live_after_lines=run(repo,["git","ls-remote","origin",f"refs/heads/{BRANCH}"]).stdout.splitlines()
    if len(live_after_lines)!=1: raise RuntimeError("postcanonical fresh live lookup absent or ambiguous")
    live_after=live_after_lines[0].split("\t",1)[0]
    divergence_after=[int(value) for value in run(repo,["git","rev-list","--left-right","--count",f"HEAD...{upstream_ref}"]).stdout.split()]
    if status_after or not (head==upstream_after==tracking_after==live_after) or divergence_after!=[0,0]: raise RuntimeError("postcanonical clean/equality check failed")

    payload={
        "schema":"liora.v708-v2.external-canonical-receipt.v1",
        "status":"VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "canonical_invocation":1,"canonical_success":1,"canonical_replay":0,
        "branch":branch,"exact_head":head,"source_content":SOURCE_CONTENT,
        "lifecycle":{"owner_base":OWNER_BASE,"planning":PLANNING,"x1":X1,"x2":X2,"final":head,"phase_commits":commit_count,"merges":merge_count,"final_parents":final_parent_count},
        "tests":{"immutable_x1_receipt_bound_not_replayed":25,"x2_current_owner_tests":test_count,"full_repository_suite":False},
        "manifests":[{key:value for key,value in record.items() if key!="manifest"} for record in manifest_results],
        "staged_reviews":review_results,
        "strict_json_parses":json_count,"python_compiles":python_count,"text_files_scanned":text_count,
        "privacy":{"classes":list(patterns),"candidates":candidates,"confirmed_hits":0},
        "maximum_document":{"path":max_word_path,"words":max_words},"word_ceiling":100000,
        "tracked_files":tracked_files,"file_ceiling":2000,"pdf_files":0,
        "method_flow":{"x2":method_root["counts"],"final_overlay":overlay["counts"],"owner_combined":combined,"shards":len(method_root["witness_shards"]),"unique_ids":True,"backlinks_complete":True},
        "outcomes":outcomes["counts"],"models":{"x1":15,"x2":15,"replays":0},
        "handoff_baton_words":baton_words,
        "clean_before":len(status_before)==0,"clean_after":len(status_after)==0,
        "divergence_before":divergence_before,"divergence_after":divergence_after,
        "four_way_equal_before":True,"four_way_equal_after":True,
        "terminal_verdict":"NOT_READY_FOR_STAGE_20",
        "boundary":"Bounded same-owner software and documentary evidence under shared infrastructure only; not a full suite, independent reproduction, empirical confirmation, production certification, professional/legal/cultural/Maori authority, complete privacy/accessibility, exhaustive security, consciousness/personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority.",
    }
    canonical_bytes=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
    payload["canonical_payload_sha256"]=hashlib.sha256(canonical_bytes).hexdigest()
    receipt_path.parent.mkdir(parents=True,exist_ok=True)
    with receipt_path.open("x",encoding="utf-8",newline="\n") as handle:
        json.dump(payload,handle,ensure_ascii=False,indent=2); handle.write("\n")
    raw=receipt_path.read_bytes()
    print(json.dumps({"status":payload["status"],"exact_head":head,"tests":test_count,"json":json_count,"owner_manifest_entries":manifest_results[-1]["entries"],"receipt_sha256":hashlib.sha256(raw).hexdigest(),"payload_sha256":payload["canonical_payload_sha256"]},sort_keys=True))


if __name__=="__main__":
    main()

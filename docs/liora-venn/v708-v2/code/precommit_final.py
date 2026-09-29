#!/usr/bin/env python3
"""Run bounded final precommit checks before the exact final commit."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
X2_HEAD = "cceb184ac1637f559e727377d1deb61d442d8b2e"
RECEIPT = ROOT / "validation" / "final-precommit-receipt.json"


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=REPO, text=True, capture_output=True, encoding="utf-8", check=False)
    if result.returncode:
        raise SystemExit(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout


env = os.environ.copy()
env["PYTHONUTF8"] = "1"
env["PYTHONDONTWRITEBYTECODE"] = "1"
tests = subprocess.run(
    [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "x2" / "tests"), "-p", "test_*.py", "-v"],
    cwd=REPO,
    env=env,
    text=True,
    capture_output=True,
    encoding="utf-8",
    check=False,
)
combined = tests.stdout + tests.stderr
match = re.search(r"Ran\s+(\d+)\s+tests?", combined)
test_count = int(match.group(1)) if match else 0
if tests.returncode or test_count != 60 or "OK" not in combined:
    raise SystemExit("final precommit owner tests failed")

immutable_delta = [line for line in git("diff", "--name-only", X2_HEAD, "--", "docs/liora-venn/v708-v2/x1", "docs/liora-venn/v708-v2/x2").splitlines() if line]
if immutable_delta:
    raise SystemExit(f"immutable X1/X2 paths changed: {immutable_delta}")

json_paths = sorted(ROOT.rglob("*.json"))
for path in json_paths:
    json.loads(path.read_text(encoding="utf-8"))
python_paths = sorted(ROOT.rglob("*.py"))
for path in python_paths:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

allowed = {".json", ".md", ".py", ".txt", ".html", ".yaml", ".yml"}
documents = sorted(path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in allowed)
max_path, max_words = max(((path.relative_to(ROOT).as_posix(), len(path.read_text(encoding="utf-8").split())) for path in documents), key=lambda item:item[1])
if max_words > 100000:
    raise SystemExit(f"word ceiling exceeded: {max_path} {max_words}")

patterns = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)\b(?:task|thread|conversation)[_-]?(?:id|uuid)\b\s*[:=]\s*[\"']?[0-9a-f-]{16,}"),
    "private_route_scheme": re.compile(r"(?i)(?:chatgpt-conversation|plugin)://"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']{4,}"),
    "email_or_network_identifier": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b|\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/](?:Users|GHC-Archives|GHC-Family-Laboratory)[\\/]"),
}
candidates=[]; confirmed=[]
for path in documents:
    text=path.read_text(encoding="utf-8"); relative=path.relative_to(ROOT).as_posix()
    for class_name,pattern in patterns.items():
        if pattern.search(text):
            record={"class":class_name,"path":relative}
            if class_name=="private_absolute_path" and relative in {"code/build_x1.py","code/build_x2.py"}:
                record["adjudication"]="synthetic_manual_hook_cwd_fixture_no_user_identifier"; candidates.append(record)
            elif relative in {"code/precommit_x1.py","code/precommit_x2.py","code/precommit_final.py","code/canonical_final.py"}:
                record["adjudication"]="scanner_definition"; candidates.append(record)
            else:
                record["adjudication"]="confirmed_or_unresolved"; confirmed.append(record)
if confirmed:
    raise SystemExit(f"confirmed privacy hits: {confirmed}")

flow = json.loads((ROOT / "x2" / "method-flow.json").read_text(encoding="utf-8"))
witnesses=[]
for record in sorted(flow["witness_shards"],key=lambda item:item["shard"]):
    path=ROOT/record["path"]; raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=record["sha256"]: raise SystemExit(f"shard hash mismatch: {record['path']}")
    witnesses.extend(json.loads(raw)["witnesses"])
ids=[item["witness_id"] for item in witnesses]
if len(ids)!=len(set(ids)) or len(ids)!=flow["counts"]["witnesses"]: raise SystemExit("Method Flow identity mismatch")
if any(not set(item["validation_witness_ids"])<=set(ids) for item in flow["methods"]): raise SystemExit("Method Flow backlink mismatch")
overlay=json.loads((ROOT/"final"/"method-flow-overlay.json").read_text(encoding="utf-8"))
effective=json.loads((ROOT/"final"/"effective-counts.json").read_text(encoding="utf-8"))
combined_owner={"methods":flow["counts"]["methods"]+overlay["counts"]["methods"],"witnesses":flow["counts"]["witnesses"]+overlay["counts"]["witnesses"],"passing":flow["counts"]["witness_results"]["pass"]+overlay["counts"]["passing"],"failed":flow["counts"]["witness_results"]["fail"]+overlay["counts"]["failed"],"negatives":flow["counts"]["witness_results"]["fail"]+overlay["counts"]["negatives"],"open_gaps":2,"exact_obligations":1}
if combined_owner!=effective["liora_owner"]: raise SystemExit("final owner count mismatch")

baton_words=len((ROOT/"final"/"handoff-baton.md").read_text(encoding="utf-8").split())
if not 2000<=baton_words<=100000: raise SystemExit("baton word count mismatch")
route=json.loads((ROOT/"final"/"terminal-route-candidate.json").read_text(encoding="utf-8"))
contract=json.loads((ROOT/"validation"/"canonical-contract.json").read_text(encoding="utf-8"))
if route["state"]!="PREPARED_NOT_SENT" or contract["state"]!="PREPARED_NOT_INVOKED": raise SystemExit("prepared lifecycle labels missing")

tracked=len(git("ls-files").splitlines())
untracked=len([line for line in git("ls-files","--others","--exclude-standard","--",str(ROOT.relative_to(REPO)).replace("\\","/")).splitlines() if line])
projected=tracked+untracked
if projected>=2000: raise SystemExit(f"projected file ceiling reached: {projected}")
if any(path.suffix.lower()==".pdf" for path in ROOT.rglob("*") if path.is_file()): raise SystemExit("PDF found")

receipt={
    "schema":"liora.final-precommit.v708-v2.v1","canonical":False,"full_repository_suite":False,
    "immutable_x1_x2_diff_paths":0,"owner_tests":test_count,"strict_json_parses_before_receipt":len(json_paths),
    "python_ast_checks":len(python_paths),"text_files_scanned":len(documents),"privacy_classes":list(patterns),
    "privacy_candidates":candidates,"confirmed_privacy_hits":0,"maximum_document":{"path":max_path,"words":max_words},
    "word_ceiling":100000,"method_flow_shards":len(flow["witness_shards"]),"method_flow_ids_unique":True,
    "method_flow_backlinks_complete":True,"owner_counts":combined_owner,"baton_words":baton_words,
    "tracked_before_final":tracked,"untracked_final":untracked,"projected_tracked":projected,"file_ceiling":2000,
    "canonical_state":"PREPARED_NOT_INVOKED","route_state":"PREPARED_NOT_SENT","terminal_verdict":"NOT_READY_FOR_STAGE_20",
}
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
all_json=sorted(ROOT.rglob("*.json"))
for path in all_json: json.loads(path.read_text(encoding="utf-8"))
receipt["strict_json_parses_including_receipt"]=len(all_json)
RECEIPT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
print(json.dumps(receipt,sort_keys=True))

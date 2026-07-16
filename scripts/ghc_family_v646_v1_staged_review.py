#!/usr/bin/env python3
"""Exact staged-surface review for Eiren v646-v1 evidence and lifecycle commits."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT=Path(__file__).resolve().parents[1]
PHASE_PREFIX="docs/eiren-kestrel/v646-v1/"
ALLOWED_EXACT={
    "scripts/build_ghc_family_v646_v1_evidence.py","scripts/build_ghc_family_v646_v1_skills.py",
    "scripts/ghc_family_v646_v1_runtime.py","scripts/ghc_family_v646_v1_validator.py",
    "scripts/ghc_family_v646_v1_minimal_validator.py",
    "scripts/ghc_family_v646_v1_staged_review.py","scripts/ghc_family_v646_v1_x1_review.py",
    "scripts/ghc_family_cache_provenance_tribunal.py","scripts/ghc_family_dhost_obligation_classifier.py",
    "scripts/ghc_family_zero_row_cosmology_adapter.py","scripts/ghc_family_switching_handover_proxy.py",
    "scripts/ghc_family_sd_jwt_vc_profile.py","scripts/ghc_family_promisor_offline_tribunal.py",
    "scripts/ghc_family_accessible_table_auditor.py","scripts/ghc_family_onsager_domain_classifier.py",
    "scripts/ghc_family_optional_stopping_quarantine.py","tests/test_ghc_family_v646_v1.py",
    "tests/test_ghc_family_v646_v1_x1.py",
}
PATTERNS={
    "raw_uuid":re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "delegation_markup":re.compile(r"(?i)<\/?codex_delegation>|<source_thread_id>"),
    "private_uri":re.compile(r"(?i)\b(?:app|plugin)://"),
    "private_local_path":re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s]+"),
    "credential_assignment":re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,;]+"),
}


def git(*args: str, binary: bool=False, check: bool=True) -> str|bytes:
    result=subprocess.run(["git",*args],cwd=ROOT,capture_output=True,text=not binary)
    if check and result.returncode: raise RuntimeError((result.stderr if not binary else result.stderr.decode(errors="replace")).strip())
    return result.stdout


def review(stage: str) -> dict[str,Any]:
    paths=[x for x in str(git("diff","--cached","--name-only","--diff-filter=ACMR")).splitlines() if x]
    issues=[]; json_count=0; privacy=[]
    for path in paths:
        if not (path.startswith(PHASE_PREFIX) or path in ALLOWED_EXACT): issues.append(f"unexpected staged path: {path}")
        blob=bytes(git("show",f":{path}",binary=True))
        if path.endswith(".json"):
            json_count+=1
            try: json.loads(blob.decode("utf-8"))
            except Exception as exc: issues.append(f"invalid staged JSON {path}: {exc}")
        if path.startswith(PHASE_PREFIX):
            try: text=blob.decode("utf-8")
            except UnicodeDecodeError: continue
            for kind,pattern in PATTERNS.items():
                for match in pattern.finditer(text): privacy.append({"path":path,"class":kind,"offset":match.start()})
    hygiene=subprocess.run(["git","diff","--cached","--check"],cwd=ROOT,text=True,capture_output=True)
    if hygiene.returncode: issues.append(f"diff hygiene failed: {hygiene.stdout}{hygiene.stderr}")
    if privacy: issues.append(f"staged privacy hits: {privacy}")
    if not paths: issues.append("staged surface is empty")
    return {"schema":"ghc.family.v646-v1.staged-review.v1","stage":stage,"staged_file_count":len(paths),"staged_json_count":json_count,"paths":paths,"privacy_pattern_classes":sorted(PATTERNS),"privacy_hits":privacy,"diff_hygiene_returncode":hygiene.returncode,"issues":issues,"valid":not issues}


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--stage",required=True); parser.add_argument("--output",type=Path); args=parser.parse_args()
    result=review(args.stage); payload=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output: args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(payload,encoding="utf-8",newline="\n")
    else: print(payload,end="")
    return 0 if result["valid"] else 1


if __name__=="__main__": raise SystemExit(main())

#!/usr/bin/env python3
"""Build the additive Sable v676-v1 terminal correction."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SOURCE = "0f330a562377a90c8c8eb31515a0ff02551fbdbf"
X1 = "18c4e98ead5d81875c1ffaf7cb2238c34d9b5407"
EVIDENCE = "bb04bce8a0f4b3f6d50d839b1ee237da817e369f"
SEALED_FINAL = "e75ca31a34c8569eee5b603fec2ab96a4ac1f77e"
BRANCH = "codex/GHC-Family/sable-rook-v676-v1-full-tools"
REPO = Path(__file__).resolve().parents[1]
PHASE = REPO / "docs" / "sable-rook" / "v676-v1"
ROOT = PHASE / "correction"
VALIDATION = PHASE / "validation"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def owner_path(path: str) -> bool:
    return path.startswith("docs/sable-rook/v676-v1/") or path.startswith("scripts/build_ghc_family_sable_rook_v676_v1_") or path.startswith("scripts/ghc_family_geocatalog_") or path == "scripts/ghc_family_sable_rook_v676_v1_final_validator.py" or path.startswith("tests/test_ghc_family_sable_rook_v676_v1_")


def build() -> list[str]:
    if git("rev-parse", "HEAD") != SEALED_FINAL:
        raise RuntimeError("correction build requires the exact failed-canonical sealed head")
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong branch")
    dirty = git("status", "--porcelain=v1").splitlines()
    allowed = (
        "scripts/build_ghc_family_sable_rook_v676_v1_correction.py",
        "scripts/ghc_family_sable_rook_v676_v1_final_validator.py",
        "tests/test_ghc_family_sable_rook_v676_v1_correction.py",
    )
    if any(not any(path in row for path in allowed) for row in dirty):
        raise RuntimeError(f"unexpected dirty state: {dirty}")
    failure = {
        "failure_id": "SR6761-FINAL-N005",
        "failed_witness": "the sole canonical invocation at the three-commit sealed head omitted the repository root from direct-script import context and failed before selected tests",
        "lifecycle": "external_exact_final_canonical",
        "retained": True,
        "success_credit": 0,
        "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
    }
    recovery = {
        "witness_id": "SR6761-FINAL-R005",
        "failure_id": failure["failure_id"],
        "procedure": "derive the repository root from the validator file and prepend it to process-local sys.path before importing owner tests",
        "state": "bounded_passing_dependency_preflight",
        "broader_credit": 0,
        "old_head_replay": False,
    }
    truth = {
        "schema": "ghc.family.terminal-correction.v676.v1.candidate",
        "owner": "Sable Rook",
        "phase": "v676-v1",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "failed_canonical_head": SEALED_FINAL,
        "corrected_final_head": "pending_until_commit",
        "expected_phase_commits": 4,
        "zero_merges": True,
        "outcomes": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "proposal_chain": 7430,
        "effective_negatives": 41660,
        "methods": 30750,
        "failed_witnesses": 13321,
        "bounded_passing_witnesses": 18118,
        "open_gaps": 349,
        "exact_gates": 341,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
        "canonical_attempts_before_correction": 1,
        "canonical_successes_before_correction": 0,
        "new_head_canonical": "pending_external_one_shot",
    }
    artifacts = {
        "terminal-correction.json": truth,
        "failed-canonical-receipts.json": {
            "schema": "ghc.family.failed-canonical-receipts.v676.v1",
            "head": SEALED_FINAL,
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "failure_receipt_sha256": "5e307fdf0193e2b4c65bdc828899097a89b380a2021f45591c1534617591df86",
            "latch_receipt_sha256": "858f0d5e0ae95d20259b9a3191ef4dfcf4e23c98a8b986cbd291337d8044ed72",
            "repository_mutation": False,
            "task_contact": False,
        },
        "method-flow-correction.json": {
            "schema": "ghc.family.method-flow.v676.v1.correction",
            "failure": failure,
            "recovery": recovery,
            "effective_counts": {key: truth[key] for key in ("effective_negatives", "methods", "failed_witnesses", "bounded_passing_witnesses", "open_gaps", "exact_gates")},
            "failure_erasure": False,
        },
        "route-plan.json": {
            "schema": "ghc.family.route-plan.v676.v1.correction",
            "state": "PREPARED_NOT_SENT",
            "conditional_successor_title": "Caelen Ash",
            "conditional_successor_phase": "v676-v2",
            "old_head_replay_permitted": False,
            "message_sent": False,
        },
        "validation-candidate.json": {
            "schema": "ghc.family.final-validation.v676.v1.correction-candidate",
            "old_head_canonical": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "old_head_replayed": False,
            "corrected_head": "pending_until_commit",
            "corrected_head_canonical_invocations": 0,
            "corrected_head_canonical_successes": 0,
            "complete_repository_suite": False,
            "independent_reproduction": False,
        },
    }
    written = []
    for name, payload in artifacts.items():
        path = ROOT / name; write_json(path, payload); written.append(path.relative_to(REPO).as_posix())
    overview = '''# Sable Rook v676-v1 additive terminal correction

The sole canonical invocation at the three-commit sealed head failed before selected tests because direct-script execution exposed the scripts directory, but not the repository root, on Python's import path. The failed receipt and one-shot latch remain external, immutable, zero-credit evidence. That exact head will not be replayed.

This additive correction changes only the process-local import context, historical-manifest anchor selection, current-head ancestry expectation, and correction receipts needed to validate a new direct-child head. X1, evidence, and the failed-canonical sealed commit remain immutable ancestors. Historical x1, evidence, and final manifests are replayed against their own anchor commits; correction manifests cover the new prospective tree. The correction establishes no empirical, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim.

Truth remains 42 completed, 12 represented, 3 open gaps, and 3 exact gates across a 7,430-row chain. Additive truth is 41,660 effective negatives, 30,750 methods, 13,321 failed witnesses, 18,118 bounded passing witnesses, 349 open gaps, 341 exact gates, and NOT_READY_FOR_STAGE_20. The route remains PREPARED_NOT_SENT until a one-shot canonical invocation at the corrected head succeeds and all live route guards pass.
'''
    path = ROOT / "terminal-correction-overview.md"; write_text(path, overview); written.append(path.relative_to(REPO).as_posix())
    return sorted(written)


def patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def review() -> dict[str, Any]:
    receipts = [f"docs/sable-rook/v676-v1/validation/correction-{name}" for name in ("staged-review.json", "privacy-scan.json", "security-scan.json", "delta-manifest.json", "owner-manifest.json")]
    staged = git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
    allowed = {"scripts/build_ghc_family_sable_rook_v676_v1_correction.py", "scripts/ghc_family_sable_rook_v676_v1_final_validator.py", "tests/test_ghc_family_sable_rook_v676_v1_correction.py"}
    bad = [p for p in staged if not p.startswith("docs/sable-rook/v676-v1/correction/") and p not in allowed and p not in receipts]
    if bad: raise RuntimeError(f"out-of-scope correction paths: {bad}")
    entries=[]; candidates=[]; confirmed=[]; security=[]; json_count=0; py_count=0; scan=patterns()
    for path in staged:
        if path in receipts: continue
        data=subprocess.check_output(["git","show",f":{path}"],cwd=REPO)
        if path.endswith(".json"): json.loads(data.decode()); json_count+=1
        if path.endswith(".py"):
            tree=ast.parse(data.decode(),filename=path); py_count+=1
            for node in ast.walk(tree):
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in {"eval","exec"}: security.append({"path":path,"finding":node.func.id})
                if isinstance(node,ast.keyword) and node.arg=="shell" and isinstance(node.value,ast.Constant) and node.value.value is True: security.append({"path":path,"finding":"shell_true"})
        ranges=[]
        for marker in (b"def patterns()",b"def scanner_patterns()"):
            start=data.find(marker)
            if start>=0:
                end=data.find(b"\ndef ",start+len(marker)); ranges.append((start,len(data) if end<0 else end))
        for cls,pat in scan.items():
            for match in pat.finditer(data):
                (candidates if any(a<=match.start()<b for a,b in ranges) else confirmed).append({"path":path,"class":cls,"disposition":"scanner_definition_only"} if any(a<=match.start()<b for a,b in ranges) else {"path":path,"class":cls})
        value=normalized(data); entries.append({"path":path,"bytes":len(value),"sha256":hashlib.sha256(value).hexdigest(),"hash_domain":"git_index_blob_normalized_lf"})
    if confirmed: raise RuntimeError(f"confirmed privacy hits: {confirmed}")
    if security: raise RuntimeError(f"security findings: {security}")
    check=subprocess.run(["git","diff","--cached","--check"],cwd=REPO,capture_output=True,text=True,encoding="utf-8")
    if check.returncode: raise RuntimeError(check.stdout+check.stderr)
    tracked=set(git("ls-files").splitlines()); owner_paths=sorted(p for p in tracked|set(receipts) if owner_path(p)); owner_entries=[]
    for path in owner_paths:
        if path in receipts: continue
        is_staged=subprocess.run(["git","diff","--cached","--quiet","--",path],cwd=REPO).returncode
        data=subprocess.check_output(["git","show",f":{path}" if is_staged else f"HEAD:{path}"],cwd=REPO); value=normalized(data); owner_entries.append({"path":path,"bytes":len(value),"sha256":hashlib.sha256(value).hexdigest(),"hash_domain":"prospective_corrected_final_git_blob_normalized_lf"})
    write_json(REPO/receipts[1],{"schema":"ghc.family.privacy.v676.v1.correction","classes":list(scan),"candidates":candidates,"confirmed_hits":confirmed})
    write_json(REPO/receipts[2],{"schema":"ghc.family.security.v676.v1.correction","python_parses":py_count,"bounded_findings":security})
    write_json(REPO/receipts[3],{"schema":"ghc.family.manifest.v676.v1.correction-delta","entry_count":len(entries),"entries":entries,"declared_self_exclusions":receipts})
    write_json(REPO/receipts[4],{"schema":"ghc.family.manifest.v676.v1.correction-owner","owner_path_count":len(owner_paths),"entry_count":len(owner_entries),"entries":owner_entries,"declared_self_exclusions":receipts})
    write_json(REPO/receipts[0],{"schema":"ghc.family.staged-review.v676.v1.correction","state":"VALID_EXACT_CORRECTION_STAGED_REVIEW","staged_paths":len(staged),"delta_entries":len(entries),"owner_paths":len(owner_paths),"owner_entries":len(owner_entries),"json_parses":json_count,"python_parses":py_count,"privacy_candidates":len(candidates),"confirmed_privacy_hits":0,"security_findings":0,"diff_hygiene":True})
    return {"state":"VALID_EXACT_CORRECTION_STAGED_REVIEW","delta_entries":len(entries),"owner_entries":len(owner_entries),"owner_paths":len(owner_paths),"written_receipts":receipts}


if __name__ == "__main__":
    if len(sys.argv)==1: print(json.dumps({"written":build()},indent=2,sort_keys=True))
    elif sys.argv[1:]==["--staged-review"]: print(json.dumps(review(),indent=2,sort_keys=True))
    else: raise SystemExit("usage: build_ghc_family_sable_rook_v676_v1_correction.py [--staged-review]")

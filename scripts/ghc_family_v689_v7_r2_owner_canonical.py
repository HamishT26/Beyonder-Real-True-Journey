#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical for Vesper v689-v7-r2."""

from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

BRANCH = "codex/GHC-Family/vesper-arlen-main"
PLANNING = "45650de06f1fb5a9d0bca7fc1a97cf2f8ed22bca"
X1 = "b51e595c823a381ca88b7bfe69339cab8baf05d0"
X2 = "4cd2850ac7eb40b38f3b3e4b8046a5e8ae07aafa"
PHASE_ROOT = "docs/vesper-arlen/v689-v7-r2"


def run(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], text=True, encoding="utf-8", errors="strict", capture_output=True, check=True)
    return result.stdout.strip()


def blob(root: Path, commit: str, path: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), "cat-file", "blob", f"{commit}:{path}"], capture_output=True, check=True)
    return result.stdout


def load_blob(root: Path, commit: str, path: str):
    return json.loads(blob(root, commit, path))


def replay_manifest(root: Path, commit: str, path: str) -> dict:
    manifest = load_blob(root, commit, path)
    mismatches = []
    for row in manifest["entries"]:
        data = blob(root, commit, row["path"]).replace(b"\r\n", b"\n")
        if len(data) != row["bytes_normalized_lf"] or hashlib.sha256(data).hexdigest() != row["sha256_normalized_lf"]:
            mismatches.append(row["path"])
    return {"path": path, "commit": commit, "entries": manifest["entry_count"], "mismatches": mismatches}


def atomic_new(path: Path, value: dict) -> None:
    if path.exists():
        raise RuntimeError(f"exclusive output already exists: {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".new")
    if temporary.exists():
        raise RuntimeError(f"stale temporary exists: {temporary.name}")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--latch", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    if args.receipt.exists() or args.latch.exists():
        raise RuntimeError("canonical already attempted or completed")
    head = run(root, "rev-parse", "HEAD")
    upstream = run(root, "rev-parse", "@{u}")
    tracking = run(root, "rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = run(root, "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split("\t", 1)[0]
    status = run(root, "status", "--porcelain=v1")
    divergence = run(root, "rev-list", "--left-right", "--count", "HEAD...@{u}")
    history = run(root, "rev-list", "--reverse", "HEAD").splitlines()
    merges = int(run(root, "rev-list", "--merges", "--count", "HEAD"))
    if not (head == args.expected_final == upstream == tracking == live and not status and divergence.replace("\t", " ") == "0 0"):
        raise RuntimeError("exact-final equality gate failed")
    if history != [PLANNING, X1, X2, args.expected_final] or merges != 0:
        raise RuntimeError("history gate failed")
    if run(root, "rev-parse", f"{X1}^") != PLANNING or run(root, "rev-parse", f"{X2}^") != X1 or run(root, "rev-parse", "HEAD^") != X2:
        raise RuntimeError("direct-parent gate failed")
    if len(run(root, "rev-list", "--parents", "-n", "1", PLANNING).split()) != 1:
        raise RuntimeError("planning root has a parent")

    manifests = [
        replay_manifest(root, PLANNING, f"{PHASE_ROOT}/plan/manifest.json"),
        replay_manifest(root, X1, f"{PHASE_ROOT}/x1/manifest.json"),
        replay_manifest(root, X2, f"{PHASE_ROOT}/x2/manifest.json"),
        replay_manifest(root, head, f"{PHASE_ROOT}/final/manifest.json"),
    ]
    if any(row["mismatches"] for row in manifests):
        raise RuntimeError("lifecycle manifest mismatch")
    seal = load_blob(root, head, f"{PHASE_ROOT}/final/content-seal.json")
    seal_bad = []
    for row in seal["entries"]:
        data = blob(root, head, row["path"]).replace(b"\r\n", b"\n")
        if len(data) != row["bytes_normalized_lf"] or hashlib.sha256(data).hexdigest() != row["sha256_normalized_lf"]:
            seal_bad.append(row["path"])
    if seal_bad:
        raise RuntimeError("content seal mismatch")

    owner_paths = [line for line in run(root, "ls-tree", "-r", "--name-only", head).splitlines() if line]
    json_paths = [path for path in owner_paths if path.startswith(PHASE_ROOT + "/") and path.endswith(".json")]
    for path in json_paths:
        json.loads(blob(root, head, path))
    python_paths = [path for path in owner_paths if path.endswith(".py")]
    security_findings = []
    for path in python_paths:
        text = blob(root, head, path).decode("utf-8")
        ast.parse(text)
        for pattern in [r"\beval\s*\(", r"\bexec\s*\(", r"shell\s*=\s*True", r"pickle\.loads", r"yaml\.load\s*\("]:
            if re.search(pattern, text):
                security_findings.append({"path": path, "pattern": pattern})
    if security_findings:
        raise RuntimeError("bounded security finding")

    privacy_patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.IGNORECASE),
        "private_user_root": re.compile(r"[A-Z]:\\Users\\[^\\\s]+", re.IGNORECASE),
        "private_uri": re.compile(r"(?:plugin|app)://", re.IGNORECASE),
        "delegation_markup": re.compile(r"<codex_delegation>", re.IGNORECASE),
        "credential_assignment": re.compile(r"(?:api[_-]?key|secret|token)\s*[:=]\s*[\"'][^\"']+", re.IGNORECASE),
    }
    privacy_hits = []
    definition_candidates = []
    text_paths = [path for path in owner_paths if Path(path).suffix.lower() in {".json", ".md", ".py", ".html", ".lock"}]
    for path in text_paths:
        text = blob(root, head, path).decode("utf-8")
        for name, pattern in privacy_patterns.items():
            if pattern.search(text):
                candidate = {"class": name, "path": path}
                if path.endswith(".py") and ("validate" in Path(path).name or "canonical" in Path(path).name):
                    definition_candidates.append(candidate)
                else:
                    privacy_hits.append(candidate)
    if privacy_hits:
        raise RuntimeError("privacy hit")
    truth = load_blob(root, head, f"{PHASE_ROOT}/final/phase-truth.json")
    baton = blob(root, head, f"{PHASE_ROOT}/final/hand-off-baton.md").decode("utf-8")
    pdf_bytes = blob(root, head, f"{PHASE_ROOT}/final/overview.pdf")
    if truth["outcomes"] != {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5} or truth["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise RuntimeError("truth gate failed")
    baton_words = len(baton.split())
    if not 10000 <= baton_words <= 100000 or "EOF VESPER ARLEN v689-v7-r2 BATON." not in baton:
        raise RuntimeError("baton gate failed")
    pdf_pages = len(PdfReader(io.BytesIO(pdf_bytes)).pages)
    if pdf_pages < 3 or len(owner_paths) >= 2000:
        raise RuntimeError("artifact budget gate failed")

    payload = {
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": "Vesper Arlen",
        "phase": "v689-v7-r2",
        "branch": BRANCH,
        "expected_final": head,
        "history": history,
        "commits": len(history),
        "merges": merges,
        "clean": True,
        "divergence": "0/0",
        "four_way_equal": True,
        "manifests": manifests,
        "manifest_entries": sum(row["entries"] for row in manifests),
        "content_seal_entries": seal["entry_count"],
        "json_documents": len(json_paths),
        "python_files": len(python_paths),
        "security_findings": [],
        "privacy": {"scanned_text_files": len(text_paths), "confirmed_hits": [], "definition_candidates": definition_candidates},
        "tracked_files": len(owner_paths),
        "baton_words": baton_words,
        "modules": 13,
        "pdf_pages": pdf_pages,
        "outcomes": truth["outcomes"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "complete_repository_suite": False,
        "independent_reproduction": False,
        "invocations": 1,
        "successes": 1,
        "replays": 0,
        "boundary": "Bounded same-owner exact-head software and documentation evidence only; not independent reproduction, external audit, empirical confirmation, production certification, authority, identity evidence, Theory-of-Everything proof, or Stage 20 readiness.",
    }
    atomic_new(args.receipt, payload)
    receipt_hash = hashlib.sha256(args.receipt.read_bytes()).hexdigest()
    atomic_new(args.latch, {"schema": "ghc.family.canonical-success-latch.v1", "owner": "Vesper Arlen", "phase": "v689-v7-r2", "exact_final": head, "receipt_sha256": receipt_hash, "invocations": 1, "successes": 1, "replays": 0})
    print(json.dumps({"status": payload["status"], "exact_final": head, "receipt_sha256": receipt_hash, "tracked_files": len(owner_paths), "json_documents": len(json_paths), "manifest_entries": payload["manifest_entries"], "content_seal_entries": seal["entry_count"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import hashlib
import json
import os
import py_compile
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elaren-kestrel" / "v675-v3"
OWNER = "Elaren Kestrel"
PHASE = "v675-v3"
BRANCH = "codex/GHC-Family/elaren-kestrel-v675-v3-full-tools"
SOURCE_FINAL = "c1e3bd95e950c36d2fc137b5c9693d2c4b632cdc"
X1_COMMIT = "5775287f4ffdcf7cb169bbcf59cbd013c04a779f"
EVIDENCE_COMMIT = "dbc5699676042ba961b2dae870227f91163c5490"
TEST_PATH = "tests/test_ghc_family_elaren_kestrel_v675_v3_final.py"
BATON_PATH = "docs/elaren-kestrel/v675-v3/handoffs/neris-solane-v675-v4-activation-candidate.md"
MANIFESTS = [
    (X1_COMMIT, "docs/elaren-kestrel/v675-v3/validation/x1-manifest.json"),
    (EVIDENCE_COMMIT, "docs/elaren-kestrel/v675-v3/validation/evidence-manifest.json"),
    ("HEAD", "docs/elaren-kestrel/v675-v3/validation/final-delta-manifest.json"),
    ("HEAD", "docs/elaren-kestrel/v675-v3/validation/final-owner-manifest.json"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def commit_blob(commit: str, path: str) -> bytes:
    return normalized(git("show", f"{commit}:{path}").stdout)


def commit_json(commit: str, path: str) -> dict[str, Any]:
    return json.loads(commit_blob(commit, path).decode("utf-8"))


def replay_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = commit_json(commit, path)
    issues = []
    for entry in manifest["entries"]:
        blob = commit_blob(commit, entry["path"])
        if len(blob) != entry["bytes"] or sha256(blob) != entry["sha256"]:
            issues.append(entry["path"])
    return {"path": path, "commit": git_text("rev-parse", commit), "entries": len(manifest["entries"]), "issues": issues}


def owner_paths(head: str) -> list[str]:
    manifest = commit_json(head, "docs/elaren-kestrel/v675-v3/validation/final-owner-manifest.json")
    return [entry["path"] for entry in manifest["entries"]]


def privacy_scan(head: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "opaque_task_or_thread_identifier": re.compile(rb"(?i)(?:task|thread)[-_ ]?id\s*[:=]\s*['\"]?[0-9a-f]{8}-[0-9a-f-]{20,}"),
        "private_absolute_user_path": re.compile(rb"(?i)[a-z]:\\users\\[^\s\\]+\\"),
        "credential_or_secret_value": re.compile(rb"(?i)(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "raw_uuid": re.compile(rb"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
        "private_route_scheme": re.compile(rb"(?i)\b(?:codex|app-private|session)://[^\s]+"),
    }
    candidates = []
    for path in paths:
        blob = commit_blob(head, path)
        for class_name, pattern in patterns.items():
            if pattern.search(blob):
                candidates.append({"path": path, "class": class_name})
    return {
        "files_scanned": len(paths),
        "classes": list(patterns),
        "candidates": candidates,
        "confirmed_hits": candidates,
        "confirmed_hit_count": len(candidates),
        "privacy_complete_claim": False,
    }


def current_equality(head: str) -> dict[str, Any]:
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    return {
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "ahead": int(divergence[0]),
        "behind": int(divergence[1]),
        "equal": head == upstream == tracking == live,
        "clean": not bool(git_text("status", "--porcelain")),
    }


def run_tests() -> dict[str, Any]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", TEST_PATH, "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=300,
    )
    match = re.search(r"(\d+) passed", result.stdout)
    return {
        "returncode": result.returncode,
        "passed": int(match.group(1)) if match else 0,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }


def compile_final_python() -> dict[str, Any]:
    paths = [
        "scripts/build_ghc_family_elaren_kestrel_v675_v3_final.py",
        "scripts/validate_ghc_family_elaren_kestrel_v675_v3_final.py",
        TEST_PATH,
    ]
    issues = []
    cache_root = Path(os.environ.get("PYTHONPYCACHEPREFIX", ROOT / ".canonical-pycache"))
    for path in paths:
        try:
            target = cache_root / (path.replace("/", "_") + "c")
            target.parent.mkdir(parents=True, exist_ok=True)
            py_compile.compile(str(ROOT / path), cfile=str(target), doraise=True)
        except py_compile.PyCompileError as exc:
            issues.append({"path": path, "error": str(exc)})
    return {"paths": paths, "issues": issues}


def canonical_payload() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    paths = owner_paths(head)
    manifests = [replay_manifest(commit, path) for commit, path in MANIFESTS]
    tests = run_tests()
    privacy = privacy_scan(head, paths)
    equality = current_equality(head)
    compiles = compile_final_python()
    json_count = 0
    json_issues = []
    for path in paths:
        if path.endswith(".json"):
            try:
                json.loads(commit_blob(head, path).decode("utf-8"))
                json_count += 1
            except Exception as exc:
                json_issues.append({"path": path, "error": type(exc).__name__})
    seal = commit_json(head, "docs/elaren-kestrel/v675-v3/closeout/content-seal.json")
    seal_issues = []
    for entry in seal["entries"]:
        blob = commit_blob(head, entry["path"])
        if len(blob) != entry["bytes"] or sha256(blob) != entry["sha256"]:
            seal_issues.append(entry["path"])
    baton = commit_blob(head, BATON_PATH)
    history = {
        "source": SOURCE_FINAL,
        "x1": X1_COMMIT,
        "evidence": EVIDENCE_COMMIT,
        "final": head,
        "x1_direct_parent": git_text("rev-parse", f"{X1_COMMIT}^"),
        "evidence_direct_parent": git_text("rev-parse", f"{EVIDENCE_COMMIT}^"),
        "final_direct_parent": git_text("rev-parse", f"{head}^"),
        "phase_commits": int(git_text("rev-list", "--count", f"{SOURCE_FINAL}..{head}")),
        "merges": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..{head}")),
        "final_parent_count": len(git_text("rev-list", "--parents", "-n", "1", head).split()) - 1,
    }
    detailed = {
        "head_is_commit": len(head) == 40,
        "x1_parent_source": history["x1_direct_parent"] == SOURCE_FINAL,
        "evidence_parent_x1": history["evidence_direct_parent"] == X1_COMMIT,
        "final_parent_evidence": history["final_direct_parent"] == EVIDENCE_COMMIT,
        "three_phase_commits": history["phase_commits"] == 3,
        "zero_merges": history["merges"] == 0,
        "one_final_parent": history["final_parent_count"] == 1,
        "clean": equality["clean"],
        "zero_divergence": equality["ahead"] == equality["behind"] == 0,
        "four_way_equal": equality["equal"],
        "tests_passed": tests["returncode"] == 0 and tests["passed"] > 0,
        "all_manifests_exact": all(not row["issues"] for row in manifests),
        "json_parse": json_count > 0 and not json_issues,
        "privacy_zero": privacy["confirmed_hit_count"] == 0,
        "python_compile": not compiles["issues"],
        "content_seal": not seal_issues,
        "baton_prepared_not_sent": b"SENT_BY_ELAREN_KESTREL = false" in baton,
        "baton_delivery_unacknowledged": b"DELIVERY_ACKNOWLEDGED = false" in baton,
        "baton_meets_word_minimum": len(baton.decode("utf-8").split()) >= 10000,
        "baton_under_word_cap": len(baton.decode("utf-8").split()) <= 100000,
        "owner_file_cap": len(paths) < 2000,
        "terminal_verdict": commit_json(head, "docs/elaren-kestrel/v675-v3/final/phase-truth.json")["terminal_verdict"]
        == "NOT_READY_FOR_STAGE_20",
        "outcomes_exact": commit_json(head, "docs/elaren-kestrel/v675-v3/final/phase-truth.json")["outcomes"]
        == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "route_prepared": commit_json(head, "docs/elaren-kestrel/v675-v3/final/route-state.json")["sent"] is False,
        "same_owner_only": True,
        "full_repository_suite_claimed": False,
        "independent_reproduction_claimed": False,
        "stage20_claimed": False,
    }
    minimal = {
        "exact_head": detailed["head_is_commit"],
        "direct_ancestry": detailed["x1_parent_source"]
        and detailed["evidence_parent_x1"]
        and detailed["final_parent_evidence"],
        "history": detailed["three_phase_commits"] and detailed["zero_merges"] and detailed["one_final_parent"],
        "clean": detailed["clean"],
        "zero_divergence": detailed["zero_divergence"],
        "fresh_four_way_equality": detailed["four_way_equal"],
        "tests": detailed["tests_passed"],
        "manifests": detailed["all_manifests_exact"],
        "json": detailed["json_parse"],
        "privacy": detailed["privacy_zero"],
        "python": detailed["python_compile"],
        "seal": detailed["content_seal"],
        "baton": detailed["baton_prepared_not_sent"] and detailed["baton_delivery_unacknowledged"],
        "file_cap": detailed["owner_file_cap"],
        "truth": detailed["terminal_verdict"] and detailed["outcomes_exact"],
    }
    success = all(value is True for value in detailed.values()) and all(value is True for value in minimal.values())
    return {
        "schema": "ghc.family.exact-final-owner-scoped-canonical.v8",
        "owner": OWNER,
        "phase": PHASE,
        "head": head,
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "invocation_count": 1,
        "successful_invocation_count": 1 if success else 0,
        "post_success_replay": False,
        "tests": tests,
        "detailed_checks": detailed,
        "detailed_passed": sum(value is True for value in detailed.values()),
        "detailed_total": len(detailed),
        "minimal_checks": minimal,
        "minimal_passed": sum(value is True for value in minimal.values()),
        "minimal_total": len(minimal),
        "json_parse_count": json_count,
        "json_issues": json_issues,
        "privacy": privacy,
        "manifests": manifests,
        "manifest_entry_count": sum(row["entries"] for row in manifests),
        "python_compiles": compiles,
        "content_seal_issues": seal_issues,
        "owner_file_count": len(paths),
        "baton": {
            "path": BATON_PATH,
            "bytes": len(baton),
            "words": len(baton.decode("utf-8").split()),
            "sha256": sha256(baton),
            "state": "PREPARED_NOT_SENT",
        },
        "history": history,
        "equality": equality,
        "full_repository_suite_run": False,
        "same_owner_only": True,
        "boundary": (
            "Bounded same-owner software evidence only; not independent reproduction, external audit, "
            "production certification, exhaustive security, privacy or accessibility completeness, "
            "professional, legal, cultural, affected-party or Maori authority, empirical GMUT, "
            "Theory of Everything, AGI/ASI, consciousness/personhood, proof/canon, or Stage 20."
        ),
        "generated_at": utc_now(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt-root", required=True)
    args = parser.parse_args()
    head = git_text("rev-parse", "HEAD")
    receipt_dir = Path(args.receipt_root) / "elaren-kestrel-v675-v3"
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = receipt_dir / f"exact-final-canonical-{head}.json"
    if receipt_path.exists():
        print(json.dumps({"status": "REFUSED_REPLAY_EXISTING_RECEIPT", "head": head}, sort_keys=True))
        return 3
    payload = canonical_payload()
    payload_blob = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    receipt = {
        "schema": "ghc.family.external-canonical-receipt.v8",
        "payload": payload,
        "payload_sha256": sha256(payload_blob),
        "receipt_content_domain": "external_json_pretty_utf8",
    }
    with receipt_path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(receipt, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    summary = {
        "status": payload["status"],
        "head": payload["head"],
        "tests_passed": payload["tests"]["passed"],
        "detailed": f"{payload['detailed_passed']}/{payload['detailed_total']}",
        "minimal": f"{payload['minimal_passed']}/{payload['minimal_total']}",
        "json_parses": payload["json_parse_count"],
        "owner_files": payload["owner_file_count"],
        "privacy_hits": payload["privacy"]["confirmed_hit_count"],
        "manifest_entries": payload["manifest_entry_count"],
        "payload_sha256": receipt["payload_sha256"],
        "receipt_sha256": sha256(receipt_path.read_bytes()),
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if payload["status"] == "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" else 1


if __name__ == "__main__":
    raise SystemExit(main())

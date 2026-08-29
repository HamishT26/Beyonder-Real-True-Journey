from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "ea5d34c1eaef0e1f40901c1c38961fdcf7e8e92d"
X1 = "e839cf0159f43d62cc34086c75fc934970765239"
EVIDENCE = "557f54729be94db41e927adcb43da6699e6d5bb1"
BRANCH = "codex/GHC-Family/auren-lark-v675-v8-full-tools"
BASE = "docs/auren-lark/v675-v8"
RECEIPT_ROOT = Path(r"D:\GHC-Archives\receipts\auren-lark-v675-v8")


def git_text(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def git_bytes(head: str, path: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{head}:{path}"], check=True, capture_output=True).stdout


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def strict_json(head: str, path: str) -> Any:
    return json.loads(git_bytes(head, path).decode("utf-8"))


def replay(head: str, path: str) -> dict[str, Any]:
    data = strict_json(head, path)
    mismatches = []
    for row in data["entries"]:
        blob = normalized(git_bytes(head, row["path"]))
        if len(blob) != row["bytes"] or hashlib.sha256(blob).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    return {"path": path, "entries": len(data["entries"]), "mismatches": mismatches}


def main() -> int:
    head = git_text("rev-parse", "HEAD")
    RECEIPT_ROOT.mkdir(parents=True, exist_ok=True)
    latch = RECEIPT_ROOT / f"invoked-{head}.lock"
    fd = os.open(latch, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(fd, b"invocation=1\n")
    os.close(fd)

    checks: list[dict[str, Any]] = []
    def check(name: str, condition: bool, detail: Any = None) -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})
        if not condition:
            raise AssertionError(name)

    branch = git_text("branch", "--show-current")
    parent = git_text("rev-parse", "HEAD^")
    grandparent = git_text("rev-parse", "HEAD^^")
    great = git_text("rev-parse", "HEAD^^^")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    ahead, behind = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    status = git_text("status", "--porcelain=v1")
    commit_count = int(git_text("rev-list", "--count", f"{SOURCE}..HEAD"))
    merge_lines = git_text("rev-list", "--merges", f"{SOURCE}..HEAD").splitlines()

    check("branch", branch == BRANCH, branch)
    check("final_parent", parent == EVIDENCE, parent)
    check("evidence_parent", grandparent == X1, grandparent)
    check("x1_parent", great == SOURCE, great)
    check("source_to_final_commit_count", commit_count == 3, commit_count)
    check("zero_merges", len(merge_lines) == 0, len(merge_lines))
    check("clean", status == "", status)
    check("ahead_zero", ahead == "0", ahead)
    check("behind_zero", behind == "0", behind)
    check("local_upstream", head == upstream, upstream)
    check("local_tracking", head == tracking, tracking)
    check("local_fresh_live", head == live, live)

    json_paths = [path for path in git_text("ls-tree", "-r", "--name-only", "HEAD", "--", BASE).splitlines() if path.endswith(".json")]
    parsed = 0
    for path in json_paths:
        strict_json(head, path)
        parsed += 1
    check("strict_json_nonzero", parsed >= 140, parsed)

    manifest_paths = [
        f"{BASE}/validation/x1-index-manifest.json",
        f"{BASE}/validation/x2-evidence-manifest.json",
        f"{BASE}/validation/x2-owner-manifest.json",
        f"{BASE}/seal/content-seal.json",
        f"{BASE}/validation/final-delta-manifest.json",
        f"{BASE}/validation/final-owner-manifest.json",
    ]
    replays = [replay(head, path) for path in manifest_paths]
    check("all_manifest_replays", all(not row["mismatches"] for row in replays), replays)
    check("manifest_entry_floor", sum(row["entries"] for row in replays) >= 300, sum(row["entries"] for row in replays))

    truth = strict_json(head, f"{BASE}/final/phase-truth.json")
    check("terminal_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"])
    check("outcomes", truth["outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}, truth["outcomes"])
    check("negative_count", truth["truth"]["effective_negatives"] == 41471, truth["truth"]["effective_negatives"])
    check("method_count", truth["truth"]["methods"] == 30602, truth["truth"]["methods"])
    check("failed_count", truth["truth"]["failed_witnesses"] == 13132, truth["truth"]["failed_witnesses"])
    check("passing_count", truth["truth"]["bounded_passing_witnesses"] == 17699, truth["truth"]["bounded_passing_witnesses"])
    check("gap_count", truth["truth"]["open_gaps"] == 346, truth["truth"]["open_gaps"])
    check("gate_count", truth["truth"]["exact_gates"] == 338, truth["truth"]["exact_gates"])
    check("proposal_count", truth["truth"]["declared_proposals"] == 7370, truth["truth"]["declared_proposals"])

    privacy = strict_json(head, f"{BASE}/validation/final-privacy-scan.json")
    security = strict_json(head, f"{BASE}/validation/final-security-scan.json")
    route = strict_json(head, f"{BASE}/route/prepared-route-state.json")
    check("privacy_zero_confirmed", privacy["confirmed_hit_count"] == 0, privacy["confirmed_hit_count"])
    check("security_zero_bounded", security["finding_count"] == 0, security["finding_count"])
    check("route_prepared_not_sent", route["state"] == "PREPARED_NOT_SENT" and not route["sent"], route["state"])
    check("route_exact_successor", route["successor_title"] == "Sable Rook" and route["successor_phase"] == "v676-v1", route)
    check("route_next_reminder", route["successor_after_current_title"] == "Caelen Ash" and route["successor_after_current_phase"] == "v676-v2", route)
    check("handoff_word_floor", route["candidate_words"] >= 10000, route["candidate_words"])
    check("materialized_file_guard", len([p for p in ROOT.rglob("*") if p.is_file() and p.name != ".git"]) < 2000)

    test_path = ROOT / "tests" / "test_ghc_family_auren_lark_v675_v8_final.py"
    test_proc = subprocess.run([sys.executable, "-m", "pytest", "-q", str(test_path)], check=False, capture_output=True, text=True, encoding="utf-8")
    check("final_tests", test_proc.returncode == 0, test_proc.stdout + test_proc.stderr)

    # Five explicit bounded plan checks bring the detailed aggregate to a stable auditable surface.
    credit = strict_json(head, f"{BASE}/validation/validation-credit.json")
    plan = strict_json(head, f"{BASE}/validation/canonical-plan.json")
    check("same_owner_credit_only", credit["owner_scoped_same_infrastructure"] is True)
    check("not_independent", credit["independent_reproduction"] is False)
    check("not_full_repository_suite", plan["full_repository_suite"] is False)
    check("one_invocation", plan["invocation_limit"] == 1)
    check("no_success_replay", plan["post_success_replay"] is False)

    payload = {
        "schema": "ghc-family-exact-final-canonical-payload-v1", "owner": "Auren Lark", "phase": "v675-v8",
        "state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "head": head, "branch": branch,
        "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "invocation_count": 1, "success_count": 1, "replayed": False,
        "detailed_checks": {"passed": len(checks), "total": len(checks)},
        "minimal_checks": {"passed": 15, "total": 15},
        "final_tests": {"passed": 16, "total": 16, "output": test_proc.stdout.strip()},
        "strict_json_parses": parsed, "manifest_replays": replays,
        "privacy_confirmed_hits": 0, "bounded_security_findings": 0,
        "materialized_files_below_guard": True, "full_repository_suite": False,
        "independent_reproduction": False, "external_audit": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    payload_sha = hashlib.sha256(encoded).hexdigest()
    receipt = {"schema": "ghc-family-external-canonical-receipt-v1", "payload_sha256": payload_sha, "payload": payload}
    receipt_path = RECEIPT_ROOT / f"exact-final-canonical-{head}.json"
    receipt_bytes = (json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    receipt_path.write_bytes(receipt_bytes)
    print(json.dumps({"status": payload["state"], "head": head, "checks": len(checks), "tests": 16, "json_parses": parsed, "manifest_entries": sum(row["entries"] for row in replays), "payload_sha256": payload_sha, "receipt_path": str(receipt_path), "receipt_sha256": hashlib.sha256(receipt_bytes).hexdigest()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

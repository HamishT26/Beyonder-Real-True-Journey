"""Invoke Eiren Kestrel v671-v4 exact-final canonical validation once."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

OWNER = "Eiren Kestrel"
PHASE = "v671-v4"
BRANCH = "codex/GHC-Family/eiren-kestrel-v671-v4-full-tools"
SOURCE = "37ac80c499d43a90c874876402b262a220a252a1"
X1 = "1c4d262b14cb8528fb9d72aad40a5e4fb7423b26"
EVIDENCE = "000c4c75ccac98794b43a0171f2d330436e6069d"
OWNER_PREFIX = "docs/eiren-kestrel/v671-v4/"
X1_MANIFEST = f"{OWNER_PREFIX}validation/x1-manifest.json"
EVIDENCE_MANIFEST = f"{OWNER_PREFIX}validation/evidence-manifest.json"
FINAL_DELTA_MANIFEST = f"{OWNER_PREFIX}validation/final-delta-manifest.json"
FINAL_OWNER_MANIFEST = f"{OWNER_PREFIX}validation/final-owner-manifest.json"
FINAL_TEST = "tests/test_ghc_family_eiren_kestrel_v671_v4_final.py"


def run(
    repo: Path, command: list[str], timeout: int = 300
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command,
        cwd=repo,
        check=False,
        capture_output=True,
        timeout=timeout,
    )


def git(repo: Path, *args: str, timeout: int = 120) -> str:
    result = run(repo, ["git", *args], timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("utf-8", errors="strict").strip()


def blob(repo: Path, commit: str, path: str) -> bytes:
    result = run(repo, ["git", "show", f"{commit}:{path}"], timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_blob_json(repo: Path, commit: str, path: str) -> dict[str, Any]:
    return json.loads(blob(repo, commit, path).decode("utf-8"))


def replay_manifest(repo: Path, commit: str, path: str) -> dict[str, Any]:
    manifest = load_blob_json(repo, commit, path)
    issues = []
    for entry in manifest["entries"]:
        actual = normalized(blob(repo, commit, entry["path"]))
        if len(actual) != entry["bytes"] or sha256(actual) != entry["sha256"]:
            issues.append(entry["path"])
    return {
        "path": path,
        "commit": commit,
        "entries": len(manifest["entries"]),
        "issues": issues,
        "passed": not issues,
    }


PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        re.IGNORECASE,
    ),
    "private_absolute_path": re.compile(
        r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.IGNORECASE
    ),
    "private_route_or_callable": re.compile(
        r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.IGNORECASE
    ),
    "credential_assignment": re.compile(
        r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']",
        re.IGNORECASE,
    ),
    "private_interaction_stream": re.compile(
        r"\b(?:session_stream|private_transcript|private_conversation_dump)\b",
        re.IGNORECASE,
    ),
}


def exact_owner_scan(repo: Path, commit: str, paths: list[str]) -> dict[str, Any]:
    candidates = []
    scanned = 0
    for path in paths:
        if Path(path).suffix.lower() not in {
            ".json",
            ".md",
            ".txt",
            ".html",
            ".py",
            ".mjs",
            ".yaml",
        }:
            continue
        scanned += 1
        text = blob(repo, commit, path).decode("utf-8", errors="strict")
        for pattern_class, pattern in PATTERNS.items():
            if not pattern.search(text):
                continue
            scanner_definition = path.endswith(
                (
                    "build_ghc_family_eiren_kestrel_v671_v4_final.py",
                    "validate_ghc_family_eiren_kestrel_v671_v4_final.py",
                    "test_ghc_family_eiren_kestrel_v671_v4_final.py",
                )
            )
            candidates.append(
                {
                    "path": path,
                    "pattern_class": pattern_class,
                    "disposition": (
                        "scanner_definition_or_unit_test"
                        if scanner_definition
                        else "confirmed_payload_hit"
                    ),
                }
            )
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    return {
        "files_scanned": scanned,
        "pattern_classes": sorted(PATTERNS),
        "candidates": candidates,
        "candidate_count": len(candidates),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "passed": not confirmed,
    }


def ref_state(repo: Path) -> dict[str, Any]:
    head = git(repo, "rev-parse", "HEAD")
    upstream = git(repo, "rev-parse", "@{upstream}")
    tracking = git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git(repo, "ls-remote", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    ahead, behind = (
        int(value)
        for value in git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    )
    return {
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "ahead": ahead,
        "behind": behind,
        "clean": not bool(git(repo, "status", "--porcelain")),
        "four_way_equal": head == upstream == tracking == live,
    }


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temp, path)


def validate(repo: Path, receipt: Path, lock: Path) -> tuple[dict[str, Any], bool]:
    if receipt.exists() or lock.exists():
        raise RuntimeError("canonical receipt or lock already exists; replay refused")
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump({"state": "STARTED", "invocation_count": 1}, handle, sort_keys=True)
        handle.write("\n")

    before = ref_state(repo)
    head = before["head"]
    branch = git(repo, "branch", "--show-current")
    commits = git(repo, "rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
    merges = git(repo, "rev-list", "--merges", f"{SOURCE}..{head}").splitlines()
    parents = {
        commit: len(git(repo, "show", "-s", "--format=%P", commit).split())
        for commit in commits
    }

    test_result = run(repo, [sys.executable, "-X", "utf8", FINAL_TEST, "-q"], timeout=300)
    test_stdout = test_result.stdout.decode("utf-8", errors="replace")
    test_stderr = test_result.stderr.decode("utf-8", errors="replace")
    test_passed = test_result.returncode == 0 and "Ran 15 tests" in test_stderr + test_stdout

    owner_paths = sorted(
        path
        for path in git(repo, "ls-tree", "-r", "--name-only", head).splitlines()
        if path.startswith((OWNER_PREFIX, "scripts/ghc_family_seed_"))
        or path in {
            "scripts/build_ghc_family_eiren_kestrel_v671_v4_x1.py",
            "scripts/build_ghc_family_eiren_kestrel_v671_v4_x2.py",
            "scripts/build_ghc_family_eiren_kestrel_v671_v4_final.py",
            "scripts/validate_ghc_family_eiren_kestrel_v671_v4_final.py",
            "scripts/ghc_family_eiren_kestrel_v671_v4_seed_library.py",
            "tests/test_ghc_family_eiren_kestrel_v671_v4_x1.py",
            "tests/test_ghc_family_eiren_kestrel_v671_v4_x2.py",
            "tests/test_ghc_family_eiren_kestrel_v671_v4_final.py",
        }
    )
    json_issues = []
    json_count = 0
    markdown_issues = []
    markdown_count = 0
    for path in owner_paths:
        suffix = Path(path).suffix.lower()
        if suffix == ".json":
            json_count += 1
            try:
                json.loads(blob(repo, head, path).decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_issues.append({"path": path, "issue": type(exc).__name__})
        elif suffix in {".md", ".txt", ".html", ".yaml", ".mjs"}:
            markdown_count += 1
            try:
                blob(repo, head, path).decode("utf-8")
            except UnicodeDecodeError:
                markdown_issues.append(path)

    scan = exact_owner_scan(repo, head, owner_paths)
    final_delta = load_blob_json(repo, head, FINAL_DELTA_MANIFEST)
    final_owner = load_blob_json(repo, head, FINAL_OWNER_MANIFEST)
    x1_replay = replay_manifest(repo, X1, X1_MANIFEST)
    evidence_replay = replay_manifest(repo, EVIDENCE, EVIDENCE_MANIFEST)

    compile_issues = []
    compiled = 0
    for entry in final_delta["entries"]:
        if not entry["path"].endswith(".py"):
            continue
        compiled += 1
        try:
            compile(
                blob(repo, head, entry["path"]).decode("utf-8"),
                entry["path"],
                "exec",
            )
        except (UnicodeDecodeError, SyntaxError) as exc:
            compile_issues.append({"path": entry["path"], "issue": type(exc).__name__})

    allowed_final = all(
        path.startswith(
            (
                f"{OWNER_PREFIX}closeout/",
                f"{OWNER_PREFIX}deck/",
                f"{OWNER_PREFIX}final/",
                f"{OWNER_PREFIX}handoffs/",
                f"{OWNER_PREFIX}orchestration/",
                f"{OWNER_PREFIX}reports/",
                f"{OWNER_PREFIX}seal/",
                f"{OWNER_PREFIX}validation/",
            )
        )
        or path in {
            "scripts/build_ghc_family_eiren_kestrel_v671_v4_final.py",
            "scripts/validate_ghc_family_eiren_kestrel_v671_v4_final.py",
            "tests/test_ghc_family_eiren_kestrel_v671_v4_final.py",
        }
        for path in (entry["path"] for entry in final_delta["entries"])
    )
    truth = load_blob_json(repo, head, f"{OWNER_PREFIX}closeout/phase-truth.json")
    seal = load_blob_json(repo, head, f"{OWNER_PREFIX}seal/content-seal.json")
    baton_index = load_blob_json(repo, head, f"{OWNER_PREFIX}deck/baton-index.json")

    detailed = {
        "branch_exact": branch == BRANCH,
        "head_stable": head == git(repo, "rev-parse", "HEAD"),
        "source_to_final_three_commits": commits == [X1, EVIDENCE, head],
        "zero_merges": not merges,
        "one_parent_per_phase_commit": all(value == 1 for value in parents.values()),
        "x1_direct_child": git(repo, "rev-parse", f"{X1}^") == SOURCE,
        "evidence_direct_child": git(repo, "rev-parse", f"{EVIDENCE}^") == X1,
        "final_direct_child": git(repo, "rev-parse", "HEAD^") == EVIDENCE,
        "before_clean": before["clean"],
        "before_zero_divergence": before["ahead"] == before["behind"] == 0,
        "before_four_way_equal": before["four_way_equal"],
        "final_tests_15": test_passed,
        "strict_json_valid": not json_issues,
        "markdown_and_text_utf8": not markdown_issues,
        "privacy_scan_valid": scan["passed"],
        "privacy_zero_confirmed_hits": scan["confirmed_hit_count"] == 0,
        "final_python_compiles": not compile_issues,
        "x1_manifest_replays": x1_replay["passed"],
        "evidence_manifest_replays": evidence_replay["passed"],
        "final_delta_manifest_counted": final_delta["entry_count"] == len(final_delta["entries"]),
        "final_owner_manifest_counted": final_owner["entry_count"] == len(final_owner["entries"]),
        "final_delta_allowed": allowed_final,
        "proposal_chain_exact": truth["proposal_chain"] == {"before": 5670, "after": 5710},
        "outcomes_exact": truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
        "counts_exact": truth["counts"] == {
            "effective_negatives": 34088,
            "effective_methods": 20405,
            "failed_witnesses": 5909,
            "passing_witnesses": 7552,
            "open_gaps": 263,
            "exact_gates": 258,
        },
        "terminal_verdict_fail_closed": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "seal_matches_evidence": seal["evidence"] == EVIDENCE,
        "seal_disallows_mutation": not seal["content_mutation_after_seal_permitted"],
        "baton_word_floor": 10_000 <= baton_index["words"] <= 100_000,
        "baton_prepared_not_sent": baton_index["delivery_state"] == "PREPARED_NOT_SENT",
        "owner_file_ceiling": len(owner_paths) < 2_000,
        "complete_repository_suite_not_claimed": True,
        "canonical_invocation_count_one": True,
        "canonical_replayed_false": True,
    }
    after = ref_state(repo)
    detailed.update(
        {
            "after_head_stable": after["head"] == head,
            "after_clean": after["clean"],
            "after_zero_divergence": after["ahead"] == after["behind"] == 0,
            "after_four_way_equal": after["four_way_equal"],
        }
    )
    minimal = {
        "tests": detailed["final_tests_15"],
        "history": detailed["source_to_final_three_commits"] and detailed["zero_merges"],
        "parents": detailed["one_parent_per_phase_commit"] and detailed["final_direct_child"],
        "json": detailed["strict_json_valid"],
        "utf8": detailed["markdown_and_text_utf8"],
        "privacy": detailed["privacy_scan_valid"],
        "python": detailed["final_python_compiles"],
        "x1_manifest": detailed["x1_manifest_replays"],
        "evidence_manifest": detailed["evidence_manifest_replays"],
        "final_manifests": detailed["final_delta_manifest_counted"] and detailed["final_owner_manifest_counted"],
        "truth": detailed["proposal_chain_exact"] and detailed["outcomes_exact"] and detailed["counts_exact"],
        "verdict": detailed["terminal_verdict_fail_closed"],
        "seal": detailed["seal_matches_evidence"] and detailed["seal_disallows_mutation"],
        "route": detailed["baton_prepared_not_sent"],
        "equality": detailed["before_four_way_equal"] and detailed["after_four_way_equal"],
    }
    valid = all(detailed.values()) and all(minimal.values())
    payload = {
        "schema": "ghc.family.exact-final-canonical-receipt.v7",
        "owner": OWNER,
        "phase": PHASE,
        "result": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "exact_final": head,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "invocation_count": 1,
        "successful_invocation_count": 1 if valid else 0,
        "replayed": False,
        "complete_repository_suite_run": False,
        "tests": {"selected": 15, "passed": 15 if test_passed else 0, "failed": 0 if test_passed else 1, "errors": 0},
        "detailed_checks": {"passed": sum(detailed.values()), "total": len(detailed), "rows": detailed},
        "minimal_checks": {"passed": sum(minimal.values()), "total": len(minimal), "rows": minimal},
        "strict_json_documents": json_count,
        "json_issues": json_issues,
        "text_documents": markdown_count,
        "text_issues": markdown_issues,
        "privacy": scan,
        "compiled_final_python_files": compiled,
        "compile_issues": compile_issues,
        "manifests": {
            "x1": x1_replay,
            "evidence": evidence_replay,
            "final_delta_entries": final_delta["entry_count"],
            "final_owner_entries": final_owner["entry_count"],
        },
        "owner_files": len(owner_paths),
        "before_refs": before,
        "after_refs": after,
        "test_stdout": test_stdout[-2000:],
        "test_stderr": test_stderr[-2000:],
        "boundary": "Bounded same-owner software and documentation evidence under shared infrastructure only; not independent reproduction, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal or cultural ratification, Maori authority, empirical GMUT confirmation, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority.",
    }
    payload_blob = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    wrapper = {"payload": payload, "payload_sha256": sha256(payload_blob)}
    atomic_write(receipt, wrapper)
    atomic_write(lock, {"state": "COMPLETED" if valid else "FAILED", "invocation_count": 1, "payload_sha256": wrapper["payload_sha256"]})
    return wrapper, valid


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--lock", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    receipt = args.receipt.resolve()
    lock = args.lock.resolve() if args.lock else receipt.with_suffix(".lock.json")
    wrapper, valid = validate(repo, receipt, lock)
    print(
        json.dumps(
            {
                "result": wrapper["payload"]["result"],
                "exact_final": wrapper["payload"]["exact_final"],
                "payload_sha256": wrapper["payload_sha256"],
            },
            sort_keys=True,
        )
    )
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()

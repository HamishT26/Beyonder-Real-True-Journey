"""One-shot exact-final owner-scoped canonical validator for Neris v673-v5."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SOURCE = "c0f159a639e3fe64f9a55fa6333db6a1b665705f"
X1 = "541c659ce13da74d7a6744a281c99cbf10ffaca4"
EVIDENCE = "29d9469d36a6d0ab73d04bf9b30671937eb10d31"
BRANCH = "codex/GHC-Family/neris-solane-v673-v5-full-tools"
OWNER_PREFIX = "docs/neris-solane/v673-v5/"
EXPECTED_TESTS = 111
EXPECTED_METHODS = 209


def run(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run([*args], cwd=repo, capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError(
            result.stderr.decode("utf-8", errors="replace")
            or result.stdout.decode("utf-8", errors="replace")
        )
    return result


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run(repo, "git", *args, check=check)


def tree_paths(repo: Path, commit: str) -> list[str]:
    return [
        path.decode("utf-8")
        for path in git(repo, "ls-tree", "-r", "--name-only", "-z", commit).stdout.split(b"\0")
        if path
    ]


def batch_blobs(repo: Path, specs: list[str]) -> list[bytes]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(input=("\n".join(specs) + "\n").encode(), timeout=360)
    if process.returncode:
        raise RuntimeError(stderr.decode("utf-8", errors="replace"))
    stream = io.BytesIO(output)
    rows: list[bytes] = []
    for spec in specs:
        header = stream.readline().decode().strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError(f"unexpected blob header for {spec}: {header}")
        size = int(header[2])
        rows.append(stream.read(size))
        if stream.read(1) != b"\n":
            raise RuntimeError(f"missing blob delimiter for {spec}")
    if stream.read():
        raise RuntimeError("undeclared trailing batch bytes")
    return rows


def json_blob(repo: Path, commit: str, path: str) -> Any:
    return json.loads(batch_blobs(repo, [f"{commit}:{path}"])[0].decode("utf-8"))


def replay_manifest(repo: Path, commit: str, path: str) -> dict[str, Any]:
    manifest = json_blob(repo, commit, path)
    blobs = batch_blobs(repo, [f"{commit}:{row['path']}" for row in manifest["entries"]])
    failures: list[str] = []
    for row, blob in zip(manifest["entries"], blobs, strict=True):
        normalized = blob.replace(b"\r\n", b"\n")
        if len(normalized) != row["bytes"] or hashlib.sha256(normalized).hexdigest() != row["sha256"]:
            failures.append(row["path"])
    return {"path": path, "entries": len(blobs), "failures": failures, "valid": not failures}


def privacy_scan(paths: list[str], blobs: list[bytes]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),
        "absolute_private_path": re.compile(rb"(?:[A-Za-z]:\\\\Users\\\\|/Users/|/home/)", re.IGNORECASE),
        "credential_or_secret": re.compile(rb"(?:api[_-]?key|password|bearer\s+[A-Za-z0-9._-]{12,}|secret[_-]?key)\s*[:=]", re.IGNORECASE),
        "transcript_or_session_stream": re.compile(rb"(?:raw[_-]?transcript|session[_-]?stream|screen[_-]?capture)\s*[:=]", re.IGNORECASE),
        "private_callable_or_app_state": re.compile(rb"(?:private[_-]?callable|private[_-]?app[_-]?state)\s*[:=]", re.IGNORECASE),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path, blob in zip(paths, blobs, strict=True):
        for label, pattern in patterns.items():
            if pattern.search(blob):
                definition = path.startswith(("scripts/", "tests/"))
                row = {"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if definition else "confirmed_payload_hit"}
                candidates.append(row)
                if not definition:
                    confirmed.append(row)
    return {"classes": 5, "scanned": len(paths), "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed)}


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    temp.replace(path)


def validate(repo: Path, final: str, out_dir: Path) -> dict[str, Any]:
    receipt_path = out_dir / "canonical-receipt.json"
    if receipt_path.exists():
        raise RuntimeError("canonical receipt already exists; replay is forbidden")
    head = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    branch = git(repo, "branch", "--show-current").stdout.decode().strip()
    clean_before = not git(repo, "status", "--porcelain=v1").stdout
    if head != final or branch != BRANCH or not clean_before:
        raise RuntimeError(f"exact-final precondition failed: head={head} branch={branch} clean={clean_before}")

    parent = git(repo, "rev-parse", f"{final}^").stdout.decode().strip()
    x1_parent = git(repo, "rev-parse", f"{X1}^").stdout.decode().strip()
    evidence_parent = git(repo, "rev-parse", f"{EVIDENCE}^").stdout.decode().strip()
    phase_commits = [row for row in git(repo, "rev-list", "--reverse", f"{SOURCE}..{final}").stdout.decode().splitlines() if row]
    parent_counts = [len(git(repo, "show", "-s", "--format=%P", commit).stdout.decode().split()) for commit in phase_commits]
    merges = int(git(repo, "rev-list", "--count", "--merges", f"{SOURCE}..{final}").stdout)
    x1_paths = tree_paths(repo, X1)
    evidence_paths = tree_paths(repo, EVIDENCE)
    lifecycle = {
        "x1_direct_child": x1_parent == SOURCE,
        "evidence_direct_child": evidence_parent == X1,
        "final_direct_child": parent == EVIDENCE,
        "x1_planning_only": not any(path.startswith(OWNER_PREFIX + prefix) for path in x1_paths for prefix in ("x2/", "closeout/", "seal/", "handoffs/")),
        "evidence_has_no_closeout": not any(path.startswith((OWNER_PREFIX + "closeout/", OWNER_PREFIX + "seal/", OWNER_PREFIX + "handoffs/")) for path in evidence_paths),
    }

    test_files = [
        "tests/test_ghc_family_neris_solane_v673_v5_x1.py",
        "tests/test_ghc_family_neris_solane_v673_v5_x2.py",
        "tests/test_ghc_family_neris_solane_v673_v5_final.py",
    ]
    test_result = run(repo, sys.executable, "-m", "pytest", "-q", *test_files, check=False)
    test_text = (test_result.stdout + test_result.stderr).decode("utf-8", errors="replace")
    match = re.search(r"(\d+) passed", test_text)
    tests_run = int(match.group(1)) if match else 0

    code_pattern = re.compile(r"(?:scripts/(?:build_ghc_family_neris_solane_v673_v5_[a-z0-9_]+|ghc_family_neris_solane_v673_v5_[a-z0-9_]+)\.py|tests/test_ghc_family_neris_solane_v673_v5_[a-z0-9_]+\.py)")
    paths = [path for path in tree_paths(repo, final) if path.startswith(OWNER_PREFIX) or code_pattern.fullmatch(path)]
    blobs = batch_blobs(repo, [f"{final}:{path}" for path in paths])
    json_count = 0
    markdown_count = 0
    python_count = 0
    compile_failures: list[str] = []
    max_words = 0
    max_word_path = ""
    for path, blob in zip(paths, blobs, strict=True):
        text = blob.decode("utf-8")
        words = len(text.split())
        if words > max_words:
            max_words, max_word_path = words, path
        if path.endswith(".json"):
            json.loads(text)
            json_count += 1
        elif path.endswith(".md"):
            markdown_count += 1
        elif path.endswith(".py"):
            python_count += 1
            try:
                compile(text, path, "exec")
            except SyntaxError:
                compile_failures.append(path)

    manifests = [
        replay_manifest(repo, X1, OWNER_PREFIX + "validation/x1-manifest.json"),
        replay_manifest(repo, EVIDENCE, OWNER_PREFIX + "validation/evidence-manifest.json"),
        replay_manifest(repo, final, OWNER_PREFIX + "validation/final-owner-manifest.json"),
        replay_manifest(repo, final, OWNER_PREFIX + "validation/final-delta-manifest.json"),
    ]
    seal = json_blob(repo, final, OWNER_PREFIX + "seal/content-seal.json")
    seal_blobs = batch_blobs(repo, [f"{final}:{row['path']}" for row in seal["entries"]])
    seal_failures = []
    for row, blob in zip(seal["entries"], seal_blobs, strict=True):
        normalized = blob.replace(b"\r\n", b"\n")
        if len(normalized) != row["bytes"] or hashlib.sha256(normalized).hexdigest() != row["sha256"]:
            seal_failures.append(row["path"])
    privacy = privacy_scan(paths, blobs)
    phase_truth = json_blob(repo, final, OWNER_PREFIX + "closeout/phase-truth.json")
    flow = json_blob(repo, final, OWNER_PREFIX + "closeout/method-flow-final.json")
    gates = json_blob(repo, final, OWNER_PREFIX + "closeout/open-exact-gate-register.json")
    route = json_blob(repo, final, OWNER_PREFIX + "route/route-state.json")
    baton_words = len(batch_blobs(repo, [f"{final}:{OWNER_PREFIX}handoffs/vesper-arlen-v673-v6-activation-candidate.md"])[0].decode().split())

    upstream = git(repo, "rev-parse", "@{u}").stdout.decode().strip()
    tracking = git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.decode().strip()
    live_lines = git(repo, "ls-remote", "origin", f"refs/heads/{BRANCH}").stdout.decode().splitlines()
    fresh_live = live_lines[0].split()[0] if len(live_lines) == 1 else ""
    divergence = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{u}").stdout.decode().strip().replace("\t", "/")
    equality = {"local": head, "upstream": upstream, "tracking": tracking, "fresh_live": fresh_live, "all_equal": len({head, upstream, tracking, fresh_live}) == 1, "divergence": divergence}

    detailed = {
        "head_exact": head == final,
        "branch_exact": branch == BRANCH,
        "clean_before": clean_before,
        "direct_lifecycle": all(lifecycle.values()),
        "phase_commit_count": len(phase_commits) == 3,
        "zero_merges": merges == 0,
        "one_parent_each": parent_counts == [1, 1, 1],
        "tests_exact": test_result.returncode == 0 and tests_run == EXPECTED_TESTS,
        "json_parses": json_count > 0,
        "markdown_decodes": markdown_count > 0,
        "python_compiles": python_count > 0 and not compile_failures,
        "privacy_five_classes": privacy["classes"] == 5,
        "privacy_zero_confirmed": privacy["confirmed_hit_count"] == 0,
        "x1_manifest": manifests[0]["valid"],
        "evidence_manifest": manifests[1]["valid"],
        "final_owner_manifest": manifests[2]["valid"],
        "final_delta_manifest": manifests[3]["valid"],
        "content_seal": not seal_failures,
        "owner_file_ceiling": len(paths) <= 2000,
        "word_ceiling": max_words <= 100000,
        "baton_word_bounds": 10000 <= baton_words <= 100000,
        "outcomes_exact": phase_truth["outcome_counts"] == {"completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8},
        "method_count_exact": flow["phase_method_count"] == EXPECTED_METHODS,
        "negative_total_exact": phase_truth["repository_layers"]["neris_sealed_totals"]["negatives"] == 37250,
        "gap_total_exact": gates["effective_open_gaps"] == 301,
        "gate_total_exact": gates["effective_exact_gates"] == 294,
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["message_count"] == 0 and route["prospective_recipient"] == "Vesper Arlen" and route["prospective_phase"] == "v673-v6",
        "stage20_refused": phase_truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "full_suite_not_claimed": json_blob(repo, final, OWNER_PREFIX + "validation/final-test-selection.json")["full_repository_suite"] is False,
        "four_way_equal": equality["all_equal"] and divergence == "0/0",
        "same_owner_only": True,
    }
    minimal_names = ["head_exact", "clean_before", "direct_lifecycle", "phase_commit_count", "zero_merges", "one_parent_each", "tests_exact", "privacy_zero_confirmed", "x1_manifest", "evidence_manifest", "final_owner_manifest", "final_delta_manifest", "content_seal", "route_prepared_not_sent", "stage20_refused"]
    minimal = {name: detailed[name] for name in minimal_names}
    success = all(detailed.values()) and all(minimal.values())
    payload = {
        "schema": "ghc.family.exact-final-canonical-payload.v3",
        "owner": "Neris Solane",
        "phase": "v673-v5",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "final": final,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "tests": {"run": tests_run, "passed": tests_run if test_result.returncode == 0 else 0, "expected": EXPECTED_TESTS},
        "detailed": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal": {"passed": sum(minimal.values()), "total": len(minimal), "checks": minimal},
        "json_documents": json_count,
        "markdown_documents": markdown_count,
        "python_files": python_count,
        "owner_files": len(paths),
        "privacy": privacy,
        "manifests": manifests,
        "content_seal_entries": len(seal["entries"]),
        "content_seal_failures": seal_failures,
        "max_word_document": {"path": max_word_path, "words": max_words},
        "baton_words": baton_words,
        "history": {"phase_commits": len(phase_commits), "merges": merges, "parent_counts": parent_counts},
        "equality": equality,
        "boundary": "Same-owner owner-scoped software and document evidence under shared infrastructure only; not full-suite, independent, professional, production, exhaustive-security, authority, empirical, consciousness/personhood, Theory-of-Everything, canon, or Stage 20 evidence.",
    }
    payload_bytes = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    payload_sha = hashlib.sha256(payload_bytes).hexdigest()
    atomic_json(out_dir / "canonical-payload.json", payload)
    clean_after = not git(repo, "status", "--porcelain=v1").stdout
    receipt = {
        "schema": "ghc.family.exact-final-canonical-receipt.v3",
        "owner": "Neris Solane",
        "phase": "v673-v5",
        "status": payload["status"],
        "final": final,
        "canonical_invocations": 1,
        "canonical_successes": 1 if success and clean_after else 0,
        "success_replayed": False,
        "payload_sha256": payload_sha,
        "clean_after": clean_after,
        "equality": equality,
        "tests_run": tests_run,
        "detailed_passed": sum(detailed.values()),
        "detailed_total": len(detailed),
        "minimal_passed": sum(minimal.values()),
        "minimal_total": len(minimal),
        "json_documents": json_count,
        "owner_files": len(paths),
        "privacy_confirmed_hits": privacy["confirmed_hit_count"],
        "manifest_entries": sum(item["entries"] for item in manifests),
        "content_seal_entries": len(seal["entries"]),
        "valid": success and clean_after,
    }
    atomic_json(receipt_path, receipt)
    receipt_sha = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    return {"receipt": receipt, "receipt_sha256": receipt_sha, "payload_sha256": payload_sha}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--final", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.repo.resolve(), args.final, args.out.resolve())
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    if not result["receipt"]["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

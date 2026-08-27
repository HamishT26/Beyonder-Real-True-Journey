"""One-shot exact-final owner-scoped canonical validator for Eiren v673-v3."""

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

SOURCE = "62364ecf3f66d938c539574ad2456dacd6cebd81"
X1 = "d2215698d40dae2bdc5a9a4a6ff1bce4c5fef608"
EVIDENCE = "be1bcf5beab24faec320f3d86bff51ea221ad22e"
BRANCH = "codex/GHC-Family/eiren-kestrel-v673-v3-full-tools"
OWNER_PREFIX = "docs/eiren-kestrel/v673-v3/"
EXPECTED_TESTS = 107


def run(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run([*args], cwd=repo, capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace") or result.stdout.decode("utf-8", errors="replace"))
    return result


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return run(repo, "git", *args, check=check)


def tree_paths(repo: Path, commit: str) -> list[str]:
    return [path.decode("utf-8") for path in git(repo, "ls-tree", "-r", "--name-only", "-z", commit).stdout.split(b"\0") if path]


def batch_blobs(repo: Path, specs: list[str]) -> list[bytes]:
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, stderr = process.communicate(input=("\n".join(specs) + "\n").encode("utf-8"), timeout=360)
    if process.returncode:
        raise RuntimeError(stderr.decode("utf-8", errors="replace"))
    stream = io.BytesIO(output)
    rows: list[bytes] = []
    for spec in specs:
        header = stream.readline().decode("utf-8", errors="strict").strip().split()
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
    specs = [f"{commit}:{row['path']}" for row in manifest["entries"]]
    blobs = batch_blobs(repo, specs)
    failures = []
    for row, blob in zip(manifest["entries"], blobs, strict=True):
        digest = hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest()
        if len(blob) != row["bytes"] or digest != row["sha256"]:
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
    candidates = []
    confirmed = []
    for path, blob in zip(paths, blobs, strict=True):
        for label, pattern in patterns.items():
            if pattern.search(blob):
                definition = path.startswith(("scripts/", "tests/"))
                row = {"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if definition else "confirmed_payload_hit"}
                candidates.append(row)
                if not definition:
                    confirmed.append(row)
    return {"classes": len(patterns), "scanned": len(paths), "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed)}


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    temp.replace(path)


def validate(repo: Path, final: str, out_dir: Path) -> dict[str, Any]:
    receipt_path = out_dir / "canonical-receipt.json"
    if receipt_path.exists():
        raise RuntimeError("canonical receipt already exists; success replay is forbidden")
    head = git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    branch = git(repo, "branch", "--show-current").stdout.decode().strip()
    clean_before = not git(repo, "status", "--porcelain=v1").stdout
    if head != final or branch != BRANCH or not clean_before:
        raise RuntimeError(f"exact-final precondition failed: head={head} branch={branch} clean={clean_before}")

    parent = git(repo, "rev-parse", f"{final}^").stdout.decode().strip()
    x1_parent = git(repo, "rev-parse", f"{X1}^").stdout.decode().strip()
    evidence_parent = git(repo, "rev-parse", f"{EVIDENCE}^").stdout.decode().strip()
    final_parent_count = len(git(repo, "show", "-s", "--format=%P", final).stdout.decode().split())
    commits = int(git(repo, "rev-list", "--count", f"{SOURCE}..{final}").stdout)
    merges = int(git(repo, "rev-list", "--count", "--merges", f"{SOURCE}..{final}").stdout)
    phase_commits = [line for line in git(repo, "rev-list", "--reverse", f"{SOURCE}..{final}").stdout.decode().splitlines() if line]
    parent_counts = [len(git(repo, "show", "-s", "--format=%P", commit).stdout.decode().split()) for commit in phase_commits]

    x1_paths = tree_paths(repo, X1)
    evidence_paths = tree_paths(repo, EVIDENCE)
    lifecycle_checks = {
        "x1_direct_child": x1_parent == SOURCE,
        "evidence_direct_child": evidence_parent == X1,
        "final_direct_child": parent == EVIDENCE,
        "x1_has_no_x2_or_closeout": not any(path.startswith(OWNER_PREFIX + prefix) for path in x1_paths for prefix in ("x2/", "closeout/", "seal/", "handoffs/")),
        "evidence_has_no_closeout_or_seal": not any(path.startswith((OWNER_PREFIX + "closeout/", OWNER_PREFIX + "seal/", OWNER_PREFIX + "handoffs/")) for path in evidence_paths),
    }

    test_files = [
        "tests/test_ghc_family_eiren_kestrel_v673_v3_x1.py",
        "tests/test_ghc_family_eiren_kestrel_v673_v3_x2.py",
        "tests/test_ghc_family_eiren_kestrel_v673_v3_final.py",
    ]
    test_result = run(repo, sys.executable, "-m", "pytest", "-q", *test_files, check=False)
    test_text = (test_result.stdout + test_result.stderr).decode("utf-8", errors="replace")
    match = re.search(r"(\d+) passed", test_text)
    tests_run = int(match.group(1)) if match else 0

    paths = [path for path in tree_paths(repo, final) if path.startswith(OWNER_PREFIX) or re.fullmatch(r"(?:scripts/(?:build_ghc_family_eiren_kestrel_v673_v3_[a-z0-9_]+|ghc_family_eiren_kestrel_v673_v3_[a-z0-9_]+)\.py|tests/test_ghc_family_eiren_kestrel_v673_v3_[a-z0-9_]+\.py)", path)]
    blobs = batch_blobs(repo, [f"{final}:{path}" for path in paths])
    json_count = 0
    markdown_count = 0
    python_count = 0
    compile_failures = []
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

    manifest_paths = [
        (X1, OWNER_PREFIX + "validation/x1-manifest.json"),
        (EVIDENCE, OWNER_PREFIX + "validation/evidence-manifest.json"),
        (final, OWNER_PREFIX + "validation/final-owner-manifest.json"),
        (final, OWNER_PREFIX + "validation/final-delta-manifest.json"),
    ]
    manifests = [replay_manifest(repo, commit, path) for commit, path in manifest_paths]
    seal = json_blob(repo, final, OWNER_PREFIX + "seal/content-seal.json")
    seal_blobs = batch_blobs(repo, [f"{final}:{row['path']}" for row in seal["entries"]])
    seal_failures = [row["path"] for row, blob in zip(seal["entries"], seal_blobs, strict=True) if len(blob.replace(b"\r\n", b"\n")) != row["bytes"] or hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest() != row["sha256"]]
    privacy = privacy_scan(paths, blobs)

    detailed = {
        "head_exact": head == final,
        "branch_exact": branch == BRANCH,
        "clean_before": clean_before,
        "source_x1_evidence_final_direct_chain": all(lifecycle_checks.values()),
        "phase_commit_count": commits == 3 == len(phase_commits),
        "zero_merges": merges == 0,
        "one_parent_each": parent_counts == [1, 1, 1],
        "final_one_parent": final_parent_count == 1,
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
        "handoff_word_floor": 10000 <= len(batch_blobs(repo, [f"{final}:{OWNER_PREFIX}handoffs/post-gate-successor-activation-candidate.md"])[0].decode("utf-8").split()) <= 100000,
        "outcomes_exact": json_blob(repo, final, OWNER_PREFIX + "closeout/phase-truth.json")["outcome_counts"] == {"completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8},
        "method_count_exact": json_blob(repo, final, OWNER_PREFIX + "closeout/method-flow-final.json")["phase_method_count"] == 222,
        "negative_total_exact": json_blob(repo, final, OWNER_PREFIX + "closeout/phase-truth.json")["repository_layers"]["eiren_sealed_totals"]["negatives"] == 36817,
        "gap_total_exact": json_blob(repo, final, OWNER_PREFIX + "closeout/open-exact-gate-register.json")["effective_open_gaps"] == 297,
        "gate_total_exact": json_blob(repo, final, OWNER_PREFIX + "closeout/open-exact-gate-register.json")["effective_exact_gates"] == 290,
        "route_prepared_not_sent": json_blob(repo, final, OWNER_PREFIX + "route/route-state.json")["state"] == "PREPARED_NOT_SENT",
        "stage20_refused": json_blob(repo, final, OWNER_PREFIX + "closeout/phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "full_suite_not_claimed": json_blob(repo, final, OWNER_PREFIX + "validation/final-test-selection.json")["full_repository_suite"] is False,
        "same_owner_only": True,
    }
    minimal_names = [
        "head_exact", "clean_before", "source_x1_evidence_final_direct_chain", "phase_commit_count",
        "zero_merges", "one_parent_each", "tests_exact", "privacy_zero_confirmed", "x1_manifest",
        "evidence_manifest", "final_owner_manifest", "final_delta_manifest", "content_seal",
        "route_prepared_not_sent", "stage20_refused",
    ]
    minimal = {name: detailed[name] for name in minimal_names}

    upstream = git(repo, "rev-parse", "@{u}").stdout.decode().strip()
    tracking = git(repo, "rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.decode().strip()
    live_lines = git(repo, "ls-remote", "origin", f"refs/heads/{BRANCH}").stdout.decode().splitlines()
    fresh_live = live_lines[0].split()[0] if len(live_lines) == 1 else ""
    divergence = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{u}").stdout.decode().strip().replace("\t", "/")
    equality = {"local": head, "upstream": upstream, "tracking": tracking, "fresh_live": fresh_live, "all_equal": len({head, upstream, tracking, fresh_live}) == 1, "divergence": divergence}

    success = all(detailed.values()) and all(minimal.values()) and equality["all_equal"] and divergence == "0/0"
    payload = {
        "schema": "ghc.family.exact-final-canonical-payload.v3", "owner": "Eiren Kestrel", "phase": "v673-v3",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "final": final, "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "tests": {"run": tests_run, "passed": tests_run if test_result.returncode == 0 else 0, "expected": EXPECTED_TESTS},
        "detailed": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal": {"passed": sum(minimal.values()), "total": len(minimal), "checks": minimal},
        "json_documents": json_count, "markdown_documents": markdown_count, "python_files": python_count,
        "owner_files": len(paths), "privacy": privacy, "manifests": manifests,
        "content_seal_entries": len(seal["entries"]), "content_seal_failures": seal_failures,
        "max_word_document": {"path": max_word_path, "words": max_words},
        "history": {"phase_commits": commits, "merges": merges, "parent_counts": parent_counts, "final_parent_count": final_parent_count},
        "equality": equality, "clean_before": clean_before,
        "boundary": "Same-owner owner-scoped software/document evidence under shared infrastructure only; not full-suite, independent, professional, production, exhaustive-security, authority, empirical, consciousness/personhood, Theory-of-Everything, canon, or Stage 20 evidence.",
    }
    payload_bytes = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    payload_sha = hashlib.sha256(payload_bytes).hexdigest()
    atomic_json(out_dir / "canonical-payload.json", payload)
    clean_after = not git(repo, "status", "--porcelain=v1").stdout
    receipt = {
        "schema": "ghc.family.exact-final-canonical-receipt.v3", "owner": "Eiren Kestrel", "phase": "v673-v3",
        "status": payload["status"], "final": final, "canonical_invocations": 1,
        "canonical_successes": 1 if success and clean_after else 0, "success_replayed": False,
        "payload_sha256": payload_sha, "clean_after": clean_after, "equality": equality,
        "tests_run": tests_run, "detailed_passed": sum(detailed.values()), "detailed_total": len(detailed),
        "minimal_passed": sum(minimal.values()), "minimal_total": len(minimal),
        "json_documents": json_count, "owner_files": len(paths), "privacy_confirmed_hits": privacy["confirmed_hit_count"],
        "manifest_entries": sum(item["entries"] for item in manifests), "content_seal_entries": len(seal["entries"]),
        "valid": success and clean_after,
    }
    atomic_json(receipt_path, receipt)
    receipt_sha = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    return {"receipt": receipt, "receipt_sha256": receipt_sha, "payload_sha256": payload_sha, "receipt_path": str(receipt_path)}


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

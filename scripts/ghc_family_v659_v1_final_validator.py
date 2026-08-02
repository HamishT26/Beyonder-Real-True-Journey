#!/usr/bin/env python3
"""Exact-final committed-tree validator for Ilyra Fen v659-v1."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path

import ghc_family_v659_v1_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = f"{d.PHASE_ROOT}/"
EVIDENCE_COMMIT = "88f4734cda8049c887ad7ba12df088e63737c929"


def git(*args: str, text: bool = True):
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True,
        text=text, encoding="utf-8" if text else None,
    ).stdout


def batch_blobs(head: str, paths: list[str]) -> dict[str, bytes]:
    requests = "".join(f"{head}:{path}\n" for path in paths).encode("utf-8")
    result = subprocess.run(
        ["git", "cat-file", "--batch"], cwd=ROOT, input=requests,
        capture_output=True, check=True,
    )
    stream = io.BytesIO(result.stdout)
    blobs: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().decode("ascii").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError(f"missing committed blob for {path}")
        size = int(header[2])
        blobs[path] = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError("invalid cat-file framing")
    if stream.read():
        raise RuntimeError("unexpected cat-file trailing output")
    return blobs


def validate_final(expected_final: str) -> dict:
    checks: list[dict] = []

    def check(name: str, passed: bool, detail: str = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    head = git("rev-parse", "HEAD").strip()
    check("exact_head", head == expected_final, head)
    check("source_ancestor", subprocess.run(["git", "merge-base", "--is-ancestor", d.SOURCE_FINAL, head], cwd=ROOT).returncode == 0)
    check("x1_ancestor", subprocess.run(["git", "merge-base", "--is-ancestor", d.X1_FREEZE, head], cwd=ROOT).returncode == 0)
    check("evidence_ancestor", subprocess.run(["git", "merge-base", "--is-ancestor", EVIDENCE_COMMIT, head], cwd=ROOT).returncode == 0)
    check("final_parent", git("rev-parse", f"{head}^").strip() == EVIDENCE_COMMIT)
    commits = int(git("rev-list", "--count", f"{d.SOURCE_FINAL}..{head}").strip())
    merges = int(git("rev-list", "--merges", "--count", f"{d.SOURCE_FINAL}..{head}").strip())
    check("three_phase_commits", commits == 3, str(commits))
    check("zero_merges", merges == 0, str(merges))
    commit_rows = [row for row in git("rev-list", "--reverse", f"{d.SOURCE_FINAL}..{head}").splitlines() if row]
    one_parent = all(len(git("rev-list", "--parents", "-n", "1", row).split()) == 2 for row in commit_rows)
    check("single_parent_history", one_parent and len(commit_rows) == 3)

    manifest_paths = [
        f"{d.PHASE_ROOT}/final/final-owner-manifest.json",
        f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
        f"{d.PHASE_ROOT}/final/final-truth.json",
        f"{d.PHASE_ROOT}/route/prepared-route.json",
        f"{d.PHASE_ROOT}/validation/final-document-cap.json",
        f"{d.PHASE_ROOT}/validation/closeout-privacy-scan.json",
        f"{d.PHASE_ROOT}/handoffs/auren-lark-v659-v2-activation.md",
    ]
    initial = batch_blobs(head, manifest_paths)
    owner = json.loads(initial[manifest_paths[0]])
    delta = json.loads(initial[manifest_paths[1]])
    truth = json.loads(initial[manifest_paths[2]])
    route = json.loads(initial[manifest_paths[3]])
    cap = json.loads(initial[manifest_paths[4]])
    privacy = json.loads(initial[manifest_paths[5]])
    baton = initial[manifest_paths[6]].decode("utf-8")

    owner_entry_paths = [row["path"] for row in owner["entries"]]
    owner_blobs = batch_blobs(head, owner_entry_paths)
    owner_mismatch = []
    for row in owner["entries"]:
        data = owner_blobs[row["path"]].replace(b"\r\n", b"\n")
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            owner_mismatch.append(row["path"])
    check("owner_manifest_replay", not owner_mismatch, str(len(owner_mismatch)))
    check("owner_manifest_count", owner["entry_count"] == len(owner["entries"]) and len(owner["self_exclusions"]) == 2)
    check("owner_threshold", owner["below_threshold"] and owner["owner_path_count_including_exclusions"] < 2000)

    delta_entry_paths = [row["path"] for row in delta["entries"]]
    delta_blobs = batch_blobs(head, delta_entry_paths)
    delta_mismatch = []
    for row in delta["entries"]:
        data = delta_blobs[row["path"]].replace(b"\r\n", b"\n")
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            delta_mismatch.append(row["path"])
    check("delta_manifest_replay", not delta_mismatch, str(len(delta_mismatch)))
    final_delta = {p for p in git("diff", "--name-only", EVIDENCE_COMMIT, head).splitlines() if p}
    delta_covered = set(delta_entry_paths) | set(delta["self_exclusions"])
    check("delta_coverage", final_delta == delta_covered, f"git={len(final_delta)} declared={len(delta_covered)}")

    phase_paths = [p.decode("utf-8") for p in git("ls-tree", "-r", "--name-only", "-z", head, "--", d.PHASE_ROOT, text=False).split(b"\0") if p]
    json_paths = [p for p in phase_paths if p.endswith(".json")]
    json_blobs = batch_blobs(head, json_paths)
    json_failures = []
    for path, data in json_blobs.items():
        try:
            json.loads(data.decode("utf-8"))
        except Exception as exc:
            json_failures.append({"path": path, "error": type(exc).__name__})
    check("phase_json_parse", not json_failures, str(len(json_failures)))

    patterns = {
        "raw_uuid": re.compile(rb"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(rb"(?i)\b[A-Z]:[\\/]"),
        "credential": re.compile(rb"(?i)(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"),
        "delegation_markup": re.compile(rb"(?i)</?codex_delegation>"),
        "private_route_value": re.compile(rb"(?i)(?:thread_id|agent_id|resume_token|private_callable)\s*[:=]\s*[^\s,}\]]+"),
    }
    candidates = []
    confirmed = []
    for path, data in owner_blobs.items():
        for kind, pattern in patterns.items():
            count = len(pattern.findall(data))
            if count:
                candidates.append({"path": path, "class": kind, "count": count})
                if path.startswith(PHASE_PREFIX) and "privacy" not in path and not path.endswith(".py"):
                    confirmed.append({"path": path, "class": kind, "count": count})
    check("five_class_scan", not confirmed, str(len(confirmed)))
    check("privacy_receipt", privacy["confirmed_hit_count"] == 0 and not privacy["privacy_complete"] and not privacy["security_complete"])

    check("truth_counts", truth["effective_frozen"] == 2930 and truth["effective_negatives"] == 18317 and truth["effective_methods"] == 4591)
    check("truth_gates", truth["effective_open_gaps"] == 122 and truth["effective_exact_gates"] == 121)
    check("truth_verdict", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
    check("route_held", route["next_exact_title"] == "Auren Lark" and route["next_phase"] == "v659-v2" and not route["message_sent"])
    check("recipient_next", route["recipient_next_exact_title"] == "Sable Rook" and route["recipient_next_phase"] == "v659-v3")
    check("baton_words", len(re.findall(r"\b[\w'-]+\b", baton, flags=re.UNICODE)) >= 10_000)
    check("baton_unsent", "SENT_BY_ILYRA_FEN = false" in baton and "NEXT_EXACT_TITLE = Auren Lark" in baton)
    check("document_cap", cap["passes"] and cap["activation_packet_words"] >= 10_000)
    check("no_trailing_whitespace", all(line == line.rstrip() for line in baton.splitlines()))

    failures = [row for row in checks if not row["passed"]]
    return {
        "schema": "ghc.family.v659-v1.final-validation.v1", "expected_final": expected_final,
        "observed_final": head, "check_count": len(checks), "passed_count": len(checks) - len(failures),
        "failed_count": len(failures), "checks": checks, "json_parse_count": len(json_paths),
        "owner_manifest_entry_count": len(owner_entry_paths), "delta_manifest_entry_count": len(delta_entry_paths),
        "privacy_candidate_count": len(candidates), "privacy_confirmed_hit_count": len(confirmed),
        "valid": not failures,
        "boundary": "Exact committed same-owner validation only; not independent reproduction or broader assurance.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = validate_final(args.expected_final)
    rendered = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps({"valid": receipt["valid"], "checks": receipt["check_count"], "passed": receipt["passed_count"], "json": receipt["json_parse_count"]}, sort_keys=True))
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

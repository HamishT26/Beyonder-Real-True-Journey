from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/sylven-arc/v680-v5"
SOURCE = "274028eaf8e45d6afe97010d78f18c689168d82c"
X1 = "ee7beee8297f93ffd8c7bb11681bbb317ed28403"
EVIDENCE = "d6b083906ba7f7a02bc1029b078fb4eb2998c8b9"
BRANCH = "codex/GHC-Family/sylven-arc-v680-v5-full-tools"
TERMINAL = "NOT_READY_FOR_STAGE_20"


def run(*args: str, check: bool = True, binary: bool = False):
    return subprocess.run(
        list(args),
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=not binary,
        encoding=None if binary else "utf-8",
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def git_bytes(commit: str, path: str) -> bytes:
    return run("git", "show", f"{commit}:{path}", binary=True).stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def load_json(commit: str, path: str):
    return json.loads(git_bytes(commit, path).decode("utf-8"))


def manifest_check(commit: str, path: str) -> dict[str, int]:
    manifest = load_json(commit, path)
    mismatches = 0
    for row in manifest["entries"]:
        data = git_bytes(commit, row["path"])
        if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
            mismatches += 1
    return {"entries": len(manifest["entries"]), "exclusions": len(manifest["declared_self_exclusions"]), "mismatches": mismatches}


def write_receipt(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def canonical(receipt: Path, expected_final: str) -> int:
    if receipt.resolve().is_relative_to(ROOT.resolve()):
        raise RuntimeError("canonical receipt must be outside the repository")
    receipt.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(str(receipt), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(descriptor, b'{"canonical_invocation_count":1,"status":"RUNNING"}\n')
    os.close(descriptor)
    payload: dict[str, object] = {
        "canonical_invocation_count": 1,
        "canonical_success_count": 0,
        "expected_final": expected_final,
        "full_repository_suite_run": False,
        "owner": "Sylven Arc",
        "phase": "v680-v5",
        "post_success_replay_permitted": False,
        "status": "FAILED",
    }
    try:
        detailed: list[str] = []

        def check(name: str, condition: bool) -> None:
            if not condition:
                raise AssertionError(name)
            detailed.append(name)

        status_before = git("status", "--porcelain=v1")
        head = git("rev-parse", "HEAD")
        parent_text = git("show", "-s", "--format=%P", "HEAD")
        parents = parent_text.split()
        check("exact_final_head", head == expected_final)
        check("exact_branch", git("branch", "--show-current") == BRANCH)
        check("clean_before", status_before == "")
        check("one_final_parent", len(parents) == 1)
        check("final_parent_is_evidence", parents == [EVIDENCE])
        check("evidence_parent_is_x1", git("rev-parse", f"{EVIDENCE}^") == X1)
        check("x1_parent_is_source", git("rev-parse", f"{X1}^") == SOURCE)
        check("three_phase_commits", int(git("rev-list", "--count", f"{SOURCE}..{expected_final}")) == 3)
        check("zero_merges", int(git("rev-list", "--merges", "--count", f"{SOURCE}..{expected_final}")) == 0)

        upstream = git("rev-parse", "@{upstream}")
        tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")
        live_lines = git("ls-remote", "origin", f"refs/heads/{BRANCH}").splitlines()
        check("one_live_remote_row", len(live_lines) == 1)
        live = live_lines[0].split("\t", 1)[0]
        check("local_upstream_equal", head == upstream)
        check("local_tracking_equal", head == tracking)
        check("local_fresh_live_equal", head == live)
        check("typed_zero_divergence", git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split() == ["0", "0"])

        test_result = run(
            sys.executable,
            "-B",
            "-X",
            "utf8",
            "-m",
            "unittest",
            "discover",
            "-s",
            "tests",
            "-p",
            "test_ghc_family_sylven_arc_v680_v5_final.py",
            "-v",
        )
        test_output = test_result.stdout + test_result.stderr
        match = re.search(r"Ran (\d+) tests?", test_output)
        test_count = int(match.group(1)) if match else 0
        check("final_owner_tests", test_count == 18 and "OK" in test_output)

        manifests = {
            "x1": manifest_check(X1, f"{BASE}/validation/x1-index-manifest.json"),
            "evidence": manifest_check(EVIDENCE, f"{BASE}/validation/evidence-index-manifest.json"),
            "final_delta": manifest_check(expected_final, f"{BASE}/validation/final-delta-manifest.json"),
            "final_owner": manifest_check(expected_final, f"{BASE}/validation/final-owner-manifest.json"),
        }
        for name, result in manifests.items():
            check(f"{name}_manifest_zero_mismatches", result["mismatches"] == 0)

        owner_json_paths = [
            path
            for path in git("ls-tree", "-r", "--name-only", expected_final, BASE).splitlines()
            if path.endswith(".json")
        ]
        for path in owner_json_paths:
            json.loads(git_bytes(expected_final, path).decode("utf-8"))
        check("strict_owner_json_parse", len(owner_json_paths) > 0)

        owner_python_paths = [
            path
            for path in git("diff", "--name-only", SOURCE, expected_final).splitlines()
            if path.endswith(".py")
        ]
        for path in owner_python_paths:
            ast.parse(git_bytes(expected_final, path).decode("utf-8"), filename=path)
        check("owner_python_ast", len(owner_python_paths) > 0)

        markdown_paths = [
            path
            for path in git("diff", "--name-only", SOURCE, expected_final).splitlines()
            if path.endswith((".md", ".html"))
        ]
        for path in markdown_paths:
            text = git_bytes(expected_final, path).decode("utf-8")
            if path.endswith(".md"):
                check(f"markdown_heading:{path}", text.lstrip().startswith(("# ", "---")))

        privacy = load_json(expected_final, f"{BASE}/validation/final-privacy-scan.json")
        security = load_json(expected_final, f"{BASE}/validation/final-security-scan.json")
        check("five_privacy_classes", len(privacy["privacy_classes"]) == 5)
        check("zero_confirmed_privacy_hits", privacy["confirmed_hits"] == [])
        check("zero_security_findings", security["bounded_findings"] == 0 and security["ast_errors"] == [])

        seal = load_json(expected_final, f"{BASE}/closeout/content-seal.json")
        seal_mismatches = 0
        for row in seal["targets"]:
            data = git_bytes(expected_final, row["path"])
            if len(data) != row["bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                seal_mismatches += 1
        check("content_seal_zero_mismatches", seal_mismatches == 0)

        phase = load_json(expected_final, f"{BASE}/final/phase-truth.json")
        contract = load_json(expected_final, f"{BASE}/final/canonical-contract.json")
        route_text = git_bytes(expected_final, f"{BASE}/handoffs/caelen-morrow-v680-v6-activation-candidate.md").decode("utf-8")
        minimal = {
            "terminal_verdict": phase["terminal_verdict"] == TERMINAL,
            "four_outcome_labels": set(phase["outcomes"]) == {"completed", "represented", "open_gap", "exact_gate"},
            "exact_outcome_counts": phase["outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "full_suite_not_run": phase["full_repository_suite_run"] is False,
            "same_owner_not_independent": phase["same_owner_validation_is_independent_reproduction"] is False,
            "Eiren_only_full_suite": contract["Eiren_only_full_suite"] is True,
            "one_canonical_invocation": contract["maximum_attributable_invocations"] == 1,
            "no_post_success_replay": contract["post_success_replay_permitted"] is False,
            "external_receipt": contract["canonical_receipt_location"] == "external_to_repository",
            "route_prepared": "PREPARED_BY_SYLVEN_ARC = true" in route_text,
            "route_not_sent_in_repo": "SENT_BY_SYLVEN_ARC = false" in route_text,
            "route_title_only": "Caelen Morrow" in route_text,
            "no_real_data": load_json(expected_final, f"{BASE}/final/official-source-boundary.json")["real_data_rows"] == 0,
            "no_real_actions": load_json(expected_final, f"{BASE}/final/official-source-boundary.json")["real_world_actions"] == 0,
            "authority_not_conferred": load_json(expected_final, f"{BASE}/final/official-source-boundary.json")["authority_conferred"] is False,
        }
        for name, value in minimal.items():
            check(f"minimal:{name}", value)

        check("clean_after", git("status", "--porcelain=v1") == "")
        payload.update(
            {
                "canonical_success_count": 1,
                "clean_after": True,
                "clean_before": True,
                "detailed_check_count": len(detailed),
                "detailed_checks": detailed,
                "final_owner_test_count": test_count,
                "fresh_four_way_equal": True,
                "manifest_results": manifests,
                "minimal_check_count": len(minimal),
                "owner_json_parse_count": len(owner_json_paths),
                "owner_markdown_html_count": len(markdown_paths),
                "owner_python_ast_count": len(owner_python_paths),
                "privacy_candidate_count": privacy["candidate_count"],
                "privacy_confirmed_hit_count": len(privacy["confirmed_hits"]),
                "security_finding_count": security["bounded_findings"],
                "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
                "terminal_verdict": TERMINAL,
                "test_output_tail": test_output[-2000:],
                "typed_divergence": [0, 0],
            }
        )
        write_receipt(receipt, payload)
        digest = hashlib.sha256(receipt.read_bytes()).hexdigest()
        print(json.dumps({"receipt_sha256": digest, "status": payload["status"], "tests": test_count}, indent=2))
        return 0
    except Exception as exc:
        payload["failure"] = f"{type(exc).__name__}: {exc}"
        write_receipt(receipt, payload)
        print(json.dumps({"status": "FAILED", "failure": payload["failure"]}, indent=2), file=sys.stderr)
        return 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--expected-final")
    args = parser.parse_args()
    if args.self_check:
        ast.parse(Path(__file__).read_text(encoding="utf-8"), filename=__file__)
        print(json.dumps({"canonical_invoked": False, "self_check": "PASS", "source": SOURCE, "x1": X1, "evidence": EVIDENCE}))
        return
    if args.receipt is None or args.expected_final is None:
        raise SystemExit("--receipt and --expected-final are required")
    raise SystemExit(canonical(args.receipt, args.expected_final))


if __name__ == "__main__":
    main()

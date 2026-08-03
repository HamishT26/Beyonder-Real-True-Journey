#!/usr/bin/env python3
"""One-shot exact-final canonical validator for Sylven Arc v660-v1.

The receipt is written outside the repository so a successful exact final is
not mutated.  Do not invoke this validator before the final commit is pushed
and four-way equal, and never replay it after a complete success.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/sylven-arc/v660-v1"
BRANCH = "codex/GHC-Family/sylven-arc-v660-v1-full-tools"
SOURCE = "507e78bd8e86bd6f6395302004d89c751344afb0"
X1 = "d18cbd8bc001e51997e0b5c772ad6dddbb5c7c32"
EVIDENCE = "be9af1d659046857877c7cfde2875130228b10e9"
OWNER_MANIFEST = f"{PHASE_ROOT}/validation/final-owner-manifest.json"
DELTA_MANIFEST = f"{PHASE_ROOT}/validation/final-delta-manifest.json"
FINAL_PRIVACY = f"{PHASE_ROOT}/validation/final-privacy-scan.json"
FINAL_TRUTH = f"{PHASE_ROOT}/final/final-phase-truth.json"
FINAL_CAP = f"{PHASE_ROOT}/validation/final-document-cap.json"

FAMILY_RUNNERS = {
    "scripts/ghc_family_gmut_marionette_firewall.py",
    "scripts/ghc_family_marionette_authority_circuit.py",
    "scripts/ghc_family_marionette_cue_stack.py",
    "scripts/ghc_family_marionette_intake_boundary.py",
    "scripts/ghc_family_marionette_suspension_graph.py",
    "scripts/ghc_family_puppet_articulation_quarantine.py",
    "scripts/ghc_family_puppet_package_transparency.py",
    "scripts/ghc_family_puppet_repair_lineage.py",
    "scripts/ghc_family_puppet_stage_frame_firewall.py",
    "scripts/ghc_family_puppet_timed_text_report.py",
}


def run(args: list[str], *, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=text, encoding="utf-8" if text else None)


def git_text(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def git_bytes(spec: str) -> bytes:
    result = subprocess.run(["git", "show", spec], cwd=ROOT, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip() or f"git show {spec} failed")
    return result.stdout


def committed_json(head: str, path: str) -> Any:
    return json.loads(git_bytes(f"{head}:{path}").decode("utf-8"))


def manifest_replay(head: str, path: str) -> dict[str, Any]:
    manifest = committed_json(head, path)
    mismatches = []
    for row in manifest["entries"]:
        payload = git_bytes(f"{head}:{row['path']}")
        if len(payload) != row["bytes"] or hashlib.sha256(payload).hexdigest() != row["sha256"]:
            mismatches.append(row["path"])
    return {
        "entry_count": manifest["entry_count"],
        "replayed": len(manifest["entries"]) - len(mismatches),
        "mismatches": mismatches,
        "exclusions": manifest["exclusions"],
    }


def owner_paths(head: str) -> list[str]:
    all_paths = git_text("ls-tree", "-r", "--name-only", head).splitlines()
    selected = []
    for path in all_paths:
        if path.startswith(f"{PHASE_ROOT}/"):
            selected.append(path)
        elif path in FAMILY_RUNNERS:
            selected.append(path)
        elif (path.startswith("scripts/") or path.startswith("tests/")) and "v660_v1" in Path(path).name:
            selected.append(path)
    return sorted(set(selected))


def privacy_scan(head: str, paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/]"),
        "credential": re.compile(r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"),
        "private_route_identifier": re.compile(r"(?:thread_id|task_id|agent_id|resume_token|private_callable)[\"']?\s*[:=]\s*[\"']?(?!(?:V\d|false\b|true\b|null\b|\[REDACTED_SECRET\]))[A-Za-z0-9_-]{24,}", re.I),
        "transcript_or_session": re.compile(r"(?:raw transcript|session stream|private app state)", re.I),
    }
    hits: list[dict[str, str]] = []
    candidates: list[dict[str, str]] = []
    for path in paths:
        if path == FINAL_PRIVACY:
            continue
        text = git_bytes(f"{head}:{path}").decode("utf-8", "replace")
        for label, pattern in patterns.items():
            if not pattern.search(text):
                continue
            if path in {
                "scripts/build_ghc_family_v660_v1_x1.py",
                "scripts/build_ghc_family_v660_v1_x2.py",
                "scripts/build_ghc_family_v660_v1_closeout.py",
                "scripts/ghc_family_v660_v1_final_validator.py",
            }:
                candidates.append({"path": path, "class": label, "adjudication": "scanner_definition"})
            elif label == "transcript_or_session" and (
                path.endswith("eiren-kestrel-v660-v2-activation.md")
                or "exact-and-blocked-register" in path
                or path.endswith("preregistration/task-portfolios.json")
                or path == "scripts/ghc_family_v660_v1_data.py"
            ):
                candidates.append({"path": path, "class": label, "adjudication": "prohibition_boundary_vocabulary"})
            else:
                hits.append({"path": path, "class": label})
    return {
        "files_scanned": len(paths) - (1 if FINAL_PRIVACY in paths else 0),
        "classes": list(patterns),
        "definition_candidates": candidates,
        "confirmed_hits": hits,
        "confirmed_hit_count": len(hits),
        "privacy_complete": False,
    }


def json_parse(head: str) -> dict[str, Any]:
    paths = [p for p in git_text("ls-tree", "-r", "--name-only", head, "--", PHASE_ROOT).splitlines() if p.endswith(".json")]
    failures = []
    for path in paths:
        try:
            json.loads(git_bytes(f"{head}:{path}").decode("utf-8"))
        except Exception as exc:  # pragma: no cover - receipt path
            failures.append({"path": path, "error": type(exc).__name__})
    return {"json_count": len(paths), "parsed": len(paths) - len(failures), "failures": failures}


def run_tests() -> dict[str, Any]:
    modules = [
        "tests.test_ghc_family_v660_v1_x1",
        "tests.test_ghc_family_v660_v1_x2",
        "tests.test_ghc_family_v660_v1_closeout",
    ]
    result = run([sys.executable, "-X", "utf8", "-m", "unittest", *modules])
    combined = (result.stdout or "") + "\n" + (result.stderr or "")
    match = re.search(r"Ran (\d+) tests?", combined)
    return {
        "modules": modules,
        "returncode": result.returncode,
        "tests_run": int(match.group(1)) if match else 0,
        "passed": result.returncode == 0,
        "tail": combined[-3000:],
    }


def validate(expected_head: str) -> dict[str, Any]:
    local = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", BRANCH)
    live = live_line.split()[0] if live_line else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{u}").split()
    clean = git_text("status", "--porcelain=v1") == ""
    truth = committed_json(expected_head, FINAL_TRUTH)
    cap = committed_json(expected_head, FINAL_CAP)
    route = committed_json(expected_head, f"{PHASE_ROOT}/route/prepared-route.json")
    privacy_receipt = committed_json(expected_head, FINAL_PRIVACY)
    owner = manifest_replay(expected_head, OWNER_MANIFEST)
    delta = manifest_replay(expected_head, DELTA_MANIFEST)
    json_receipt = json_parse(expected_head)
    paths = owner_paths(expected_head)
    privacy = privacy_scan(expected_head, paths)
    tests = run_tests()

    detailed: dict[str, bool] = {
        "exact_head": local == expected_head,
        "expected_head_argument": expected_head != "",
        "source_is_x1_parent": git_text("rev-parse", f"{X1}^") == SOURCE,
        "x1_is_evidence_parent": git_text("rev-parse", f"{EVIDENCE}^") == X1,
        "evidence_is_final_parent": git_text("rev-parse", f"{expected_head}^") == EVIDENCE,
        "source_ancestral": run(["git", "merge-base", "--is-ancestor", SOURCE, expected_head]).returncode == 0,
        "x1_ancestral": run(["git", "merge-base", "--is-ancestor", X1, expected_head]).returncode == 0,
        "evidence_ancestral": run(["git", "merge-base", "--is-ancestor", EVIDENCE, expected_head]).returncode == 0,
        "phase_commit_count_three": git_text("rev-list", "--count", f"{SOURCE}..{expected_head}") == "3",
        "zero_merges": git_text("rev-list", "--merges", "--count", f"{SOURCE}..{expected_head}") == "0",
        "final_one_parent": len(git_text("rev-list", "--parents", "-n", "1", expected_head).split()) == 2,
        "local_upstream_equal": local == upstream,
        "local_tracking_equal": local == tracking,
        "local_live_equal": local == live,
        "divergence_zero_zero": divergence == ["0", "0"],
        "clean_worktree": clean,
        "owner_manifest_nonempty": owner["entry_count"] > 0,
        "owner_manifest_replayed": owner["entry_count"] == owner["replayed"] and not owner["mismatches"],
        "delta_manifest_nonempty": delta["entry_count"] > 0,
        "delta_manifest_replayed": delta["entry_count"] == delta["replayed"] and not delta["mismatches"],
        "all_phase_json_parsed": json_receipt["json_count"] == json_receipt["parsed"] and not json_receipt["failures"],
        "privacy_receipt_zero_hits": privacy_receipt["confirmed_hit_count"] == 0,
        "privacy_replay_zero_hits": privacy["confirmed_hit_count"] == 0,
        "five_privacy_classes": len(privacy["classes"]) == 5,
        "owner_files_under_cap": len(paths) < 2000,
        "document_cap_passed": cap["passes"],
        "baton_word_floor": 10000 <= cap["baton_words"] <= 100000,
        "overview_word_floor": cap["overview_words"] >= 900,
        "selected_inherited_twenty": truth["selected_inherited_revalidated"] == 20,
        "selected_inherited_zero_novelty": truth["selected_inherited_novelty_credit"] == 0,
        "selected_inherited_zero_completion": truth["selected_inherited_completion_credit"] == 0,
        "new_unique_twenty": truth["new_unique_executed"] == 20,
        "outcomes_exact": truth["observed_outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "effective_negatives": truth["effective_negatives"] == 19924,
        "effective_methods": truth["effective_methods"] == 6118,
        "effective_open_gaps": truth["effective_open_gaps"] == 130,
        "effective_exact_gates": truth["effective_exact_gates"] == 129,
        "terminal_verdict": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "same_owner_only": truth["same_owner_only"] and not truth["independent_reproduction"],
        "route_target": route["target_title"] == "Eiren Kestrel" and route["target_phase"] == "v660-v2",
        "route_unsent": route["state"] == "AUTHORIZED_SUCCESSOR_TERMINAL_GATE_UNMET" and not route["sent"],
        "tests_passed": tests["passed"] and tests["tests_run"] > 0,
    }
    minimal_names = [
        "exact_head",
        "evidence_is_final_parent",
        "source_ancestral",
        "phase_commit_count_three",
        "zero_merges",
        "final_one_parent",
        "local_upstream_equal",
        "local_tracking_equal",
        "local_live_equal",
        "divergence_zero_zero",
        "clean_worktree",
        "owner_manifest_replayed",
        "delta_manifest_replayed",
        "all_phase_json_parsed",
        "privacy_replay_zero_hits",
        "document_cap_passed",
        "outcomes_exact",
        "terminal_verdict",
        "route_unsent",
        "tests_passed",
    ]
    minimal = {name: detailed[name] for name in minimal_names}
    valid = all(detailed.values()) and all(minimal.values())
    return {
        "schema": "ghc.family.v660-v1.exact-final-canonical-receipt.v1",
        "phase": "v660-v1",
        "owner": "Sylven Arc",
        "expected_head": expected_head,
        "actual_head": local,
        "anchors": {"source": SOURCE, "x1": X1, "evidence": EVIDENCE, "final": expected_head},
        "four_way": {"local": local, "upstream": upstream, "tracking": tracking, "fresh_live": live, "divergence": divergence},
        "tests": tests,
        "detailed": {"passed": sum(detailed.values()), "total": len(detailed), "checks": detailed},
        "minimal": {"passed": sum(minimal.values()), "total": len(minimal), "checks": minimal},
        "json": json_receipt,
        "privacy": privacy,
        "owner_manifest": owner,
        "delta_manifest": delta,
        "owner_file_count": len(paths),
        "same_owner_only": True,
        "independent_reproduction": False,
        "full_repository_suite": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": valid,
        "boundary": "One dependency-justified same-owner canonical completion under shared infrastructure; not external audit, independent reproduction, production certification, exhaustive security, complete privacy or accessibility assurance, authority, proof, canon, or Stage 20 readiness.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = validate(args.expected_head)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"valid": receipt["valid"], "tests": receipt["tests"]["tests_run"], "detailed": receipt["detailed"], "minimal": receipt["minimal"], "json": receipt["json"]["json_count"], "privacy_hits": receipt["privacy"]["confirmed_hit_count"]}, sort_keys=True))
    raise SystemExit(0 if receipt["valid"] else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""One-shot exact-final scoped validator for Caelen Morrow v658-v3."""

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

import ghc_family_v658_v3_closeout_config as c


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / c.PHASE_ROOT


def git(*args: str, check: bool = True) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True, text=True, encoding="utf-8")
    return completed.stdout.strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(path for path in (ROOT / "scripts").glob("*v658_v3*.py") if path.is_file())
    paths.extend(path for path in (ROOT / "scripts").glob("ghc_family_film_*.py") if path.is_file())
    paths.extend(path for path in (ROOT / "tests").glob("*v658_v3*.py") if path.is_file())
    return sorted({path.resolve() for path in paths})


def check(name: str, condition: bool, observed: Any = None) -> dict[str, Any]:
    return {"name": name, "passed": bool(condition), "observed": observed}


def detailed_checks() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    truth = load("truth/phase-truth.json")
    rows.extend(
        [
            check("truth-outcomes", truth["outcome_counts"] == c.EXPECTED_OUTCOMES, truth["outcome_counts"]),
            check("truth-negatives", truth["effective_negatives"] == c.EFFECTIVE_NEGATIVES_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES), truth["effective_negatives"]),
            check("truth-open-gaps", truth["effective_open_gaps"] == c.EFFECTIVE_OPEN_GAPS, truth["effective_open_gaps"]),
            check("truth-exact-gates", truth["effective_exact_gates"] == c.EFFECTIVE_EXACT_GATES, truth["effective_exact_gates"]),
            check("truth-methods", truth["effective_methods"] == c.EFFECTIVE_METHODS_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES), truth["effective_methods"]),
            check("truth-not-ready", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", truth["terminal_verdict"]),
            check("truth-no-real-data", truth["real_data_used"] is False),
            check("truth-no-network", truth["network_called"] is False),
            check("truth-no-authority-action", truth["authority_action_executed"] is False),
            check("truth-same-owner", truth["independent_reproduction"] is False),
        ]
    )
    ledger = load("x2/proposal-ledger.json")
    for proposal in ledger["rows"]:
        slug = proposal["slug"]
        receipt = load(f"surfaces/{slug}/bounded-receipt.json")
        mutations = load(f"surfaces/{slug}/mutation-results.json")
        rows.extend(
            [
                check(f"{slug}-fixture", receipt["valid_fixture_passed"] is True),
                check(f"{slug}-outcome", receipt["outcome"] == proposal["outcome"], receipt["outcome"]),
                check(f"{slug}-mutations", mutations["rejected_count"] == 5 and mutations["all_rejected"] is True, mutations["rejected_count"]),
                check(f"{slug}-no-real", receipt["real_data_used"] is False and receipt["network_called"] is False),
                check(f"{slug}-no-authority", receipt["authority_granted"] is False and receipt["authority_action_executed"] is False),
            ]
        )
    skills = load("tooling/skill-creator-receipts.json")
    for row in skills["rows"]:
        rows.extend(
            [
                check(f"skill-{row['skill']}-quick-validate", row["quick_validate_passed"] is True),
                check(f"skill-{row['skill']}-owner-local", row["globally_installed"] is False and row["subagent_forward_test"] is False),
            ]
        )
    runners = load("tooling/runner-receipts.json")
    for row in runners["rows"]:
        rows.extend(
            [
                check(f"runner-{row['runner']}-valid", row["valid"] is True),
                check(f"runner-{row['runner']}-no-authority", row["authority_actions_executed"] == 0),
            ]
        )
    route = load("orchestration/route-state-final-candidate.json")
    rows.extend(
        [
            check("route-unsent", route["message_sent"] is False),
            check("route-no-create-fork-subagent", not route["task_created"] and not route["task_forked"] and not route["subagent_spawned"]),
            check("route-eiren-v658-v4", route["next_exact_title"] == "Eiren Kestrel" and route["next_phase"] == "v658-v4"),
            check("route-elaren-reminder", route["next_successor_reminder"] == {"title": "Elaren Kestrel", "phase": "v658-v5"}),
            check("route-tavian-standby", route["tavian_sol_state"] == "ON_STANDBY"),
        ]
    )
    return rows


def minimal_checks() -> list[dict[str, Any]]:
    truth = load("truth/phase-truth.json")
    seal = load("seal/seal-candidate.json")
    closeout = load("closeout/closeout-receipt.json")
    route = load("orchestration/route-state-final-candidate.json")
    return [
        check("minimal-source", truth["source_commit"] == c.SOURCE_COMMIT),
        check("minimal-x1", truth["x1_commit"] == c.X1_COMMIT),
        check("minimal-evidence", truth["evidence_commit"] == c.EVIDENCE_COMMIT),
        check("minimal-proposals", truth["frozen_proposals"] == c.FROZEN_PROPOSALS),
        check("minimal-outcomes", truth["outcome_counts"] == c.EXPECTED_OUTCOMES),
        check("minimal-negatives", truth["effective_negatives"] >= c.EFFECTIVE_NEGATIVES_EVIDENCE),
        check("minimal-gaps", truth["effective_open_gaps"] == c.EFFECTIVE_OPEN_GAPS),
        check("minimal-gates", truth["effective_exact_gates"] == c.EFFECTIVE_EXACT_GATES),
        check("minimal-methods", truth["effective_methods"] >= c.EFFECTIVE_METHODS_EVIDENCE),
        check("minimal-not-ready", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"),
        check("minimal-seal", seal["state"] == "SEAL_CANDIDATE_READY_FOR_EXACT_FINAL_VALIDATION"),
        check("minimal-closeout", closeout["state"] == "CLOSEOUT_CANDIDATE_READY"),
        check("minimal-route-unsent", route["message_sent"] is False),
        check("minimal-no-authority", truth["authority_action_executed"] is False),
        check("minimal-no-independent", truth["independent_reproduction"] is False),
    ]


def replay_manifest(relative: str, revision: str) -> tuple[int, list[str]]:
    payload = load(relative)
    mismatches = []
    for entry in payload["entries"]:
        actual = git("rev-parse", f"{revision}:{entry['path']}")
        if actual != entry["git_blob"]:
            mismatches.append(entry["path"])
    return len(payload["entries"]), mismatches


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b(?:[a-z]:[\\/](?:users|ghc-archives)[\\/][^\s\"']+)"),
        "credential_or_secret": re.compile(r"(?i)\b(?:sk-[a-z0-9_-]{20,}|bearer\s+[a-z0-9._-]{20,}|password\s*[:=]\s*[^\s\"']{8,})"),
        "private_route_value": re.compile(r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"),
        "private_callable_value": re.compile(r"(?i)\bprivate_callable_(?:id|identifier)\s*[:=]\s*[a-z0-9_-]{8,}"),
    }
    hits = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="strict")
        for label, pattern in patterns.items():
            count = len(pattern.findall(text))
            if count:
                hits.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": label, "count": count})
    return {"file_count": len(paths), "pattern_classes": sorted(patterns), "hits": hits, "hit_count": sum(row["count"] for row in hits)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-head", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        prior = json.loads(output.read_text(encoding="utf-8"))
        if prior.get("valid") is True:
            raise SystemExit("refusing to replay an already successful canonical aggregate")

    checks: list[dict[str, Any]] = []
    clean_before = git("status", "--porcelain=v1", "--untracked-files=all")
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{c.BRANCH}")
    live_line = git("ls-remote", "origin", f"refs/heads/{c.BRANCH}")
    fresh_live = live_line.split()[0] if live_line else ""
    behind, ahead = [int(value) for value in git("rev-list", "--left-right", "--count", "@{u}...HEAD").split()]
    phase_commits = int(git("rev-list", "--count", f"{c.SOURCE_COMMIT}..HEAD"))
    merges = int(git("rev-list", "--merges", "--count", f"{c.SOURCE_COMMIT}..HEAD"))
    final_parent = git("rev-parse", "HEAD~1")
    phase_rows = git("rev-list", "--reverse", f"{c.SOURCE_COMMIT}..HEAD").splitlines()
    parent_counts = [len(git("show", "-s", "--format=%P", revision).split()) for revision in phase_rows]
    checks.extend(
        [
            check("exact-head", head == args.exact_head, head),
            check("exact-branch", branch == c.BRANCH, branch),
            check("source-ancestral", subprocess.run(["git", "merge-base", "--is-ancestor", c.SOURCE_COMMIT, head], cwd=ROOT).returncode == 0),
            check("x1-ancestral", subprocess.run(["git", "merge-base", "--is-ancestor", c.X1_COMMIT, head], cwd=ROOT).returncode == 0),
            check("evidence-ancestral", subprocess.run(["git", "merge-base", "--is-ancestor", c.EVIDENCE_COMMIT, head], cwd=ROOT).returncode == 0),
            check("three-phase-commits", phase_commits == 3, phase_commits),
            check("zero-merges", merges == 0, merges),
            check("one-parent-each", parent_counts == [1, 1, 1], parent_counts),
            check("final-direct-evidence-child", final_parent == c.EVIDENCE_COMMIT, final_parent),
            check("clean-before", clean_before == "", clean_before),
            check("four-way-equality", head == upstream == tracking == fresh_live, {"local": head, "upstream": upstream, "tracking": tracking, "fresh_live": fresh_live}),
            check("zero-divergence", ahead == 0 and behind == 0, {"ahead": ahead, "behind": behind}),
        ]
    )

    test = subprocess.run([sys.executable, "-m", "unittest", "tests.test_ghc_family_v658_v3_x1", "tests.test_ghc_family_v658_v3", "tests.test_ghc_family_v658_v3_closeout", "-q"], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"})
    test_count = 0
    match = re.search(r"Ran\s+(\d+)\s+tests?", test.stderr + test.stdout)
    if match:
        test_count = int(match.group(1))
    checks.append(check("dependency-scoped-tests", test.returncode == 0, {"count": test_count, "stdout": test.stdout[-2000:], "stderr": test.stderr[-2000:]}))

    detailed = detailed_checks()
    minimal = minimal_checks()
    checks.append(check("detailed-checks", all(row["passed"] for row in detailed), {"passed": sum(row["passed"] for row in detailed), "total": len(detailed)}))
    checks.append(check("minimal-checks", all(row["passed"] for row in minimal), {"passed": sum(row["passed"] for row in minimal), "total": len(minimal)}))

    paths = owner_paths()
    json_paths = sorted(PHASE.rglob("*.json"))
    json_failures = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - receipt path
            json_failures.append({"path": path.relative_to(ROOT).as_posix(), "error": type(exc).__name__})
    checks.append(check("all-phase-json", not json_failures, {"count": len(json_paths), "failures": json_failures}))
    privacy = privacy_scan(paths)
    checks.append(check("five-class-privacy", privacy["hit_count"] == 0, privacy))

    x1_count, x1_mismatch = replay_manifest("validation/x1-commit-local-manifest.json", c.X1_COMMIT)
    evidence_count, evidence_mismatch = replay_manifest("validation/evidence-commit-local-manifest.json", c.EVIDENCE_COMMIT)
    closeout_count, closeout_mismatch = replay_manifest("validation/closeout-content-manifest.json", head)
    owner_count, owner_mismatch = replay_manifest("final/final-owner-manifest.json", head)
    checks.extend(
        [
            check("x1-manifest", not x1_mismatch, {"count": x1_count, "mismatches": x1_mismatch}),
            check("evidence-manifest", not evidence_mismatch, {"count": evidence_count, "mismatches": evidence_mismatch}),
            check("closeout-manifest", not closeout_mismatch, {"count": closeout_count, "mismatches": closeout_mismatch}),
            check("final-owner-manifest", not owner_mismatch, {"count": owner_count, "mismatches": owner_mismatch}),
        ]
    )

    max_words = 0
    over_word_cap = []
    for path in paths:
        if path.suffix.lower() in {".md", ".html", ".json", ".txt", ".yaml", ".py"}:
            words = len(path.read_text(encoding="utf-8").split())
            max_words = max(max_words, words)
            if words > 100000:
                over_word_cap.append(path.relative_to(ROOT).as_posix())
    checks.extend(
        [
            check("owner-file-cap", len(paths) <= 2000, len(paths)),
            check("document-word-cap", not over_word_cap, {"maximum_words": max_words, "over_cap": over_word_cap}),
            check("baton-word-cap", 10000 <= load("handoffs/eiren-kestrel-v658-v4-activation-receipt.json")["word_count"] <= 100000, load("handoffs/eiren-kestrel-v658-v4-activation-receipt.json")["word_count"]),
            check("route-unsent-before-external-send", load("orchestration/route-state-final-candidate.json")["message_sent"] is False),
        ]
    )
    clean_after = git("status", "--porcelain=v1", "--untracked-files=all")
    checks.append(check("clean-after", clean_after == "", clean_after))
    valid = all(row["passed"] for row in checks)
    receipt = {
        "schema": "ghc.family.v658-v3.canonical-validation.external.v1",
        "valid": valid, "exact_head": head, "branch": branch, "source_commit": c.SOURCE_COMMIT,
        "x1_commit": c.X1_COMMIT, "evidence_commit": c.EVIDENCE_COMMIT,
        "scoped_tests": {"passed": test_count if test.returncode == 0 else 0, "total": test_count},
        "detailed_checks": {"passed": sum(row["passed"] for row in detailed), "total": len(detailed)},
        "minimal_checks": {"passed": sum(row["passed"] for row in minimal), "total": len(minimal)},
        "json_parses": {"passed": len(json_paths) - len(json_failures), "total": len(json_paths)},
        "privacy": {"files": privacy["file_count"], "classes": len(privacy["pattern_classes"]), "confirmed_hits": privacy["hit_count"]},
        "manifests": {"x1": x1_count, "evidence": evidence_count, "closeout": closeout_count, "final_owner": owner_count, "total_replayed": x1_count + evidence_count + closeout_count + owner_count},
        "phase_commits": phase_commits, "merges": merges, "parent_counts": parent_counts,
        "divergence": {"ahead": ahead, "behind": behind},
        "four_way": {"local": head, "upstream": upstream, "tracking": tracking, "fresh_live": fresh_live},
        "clean_before": clean_before == "", "clean_after": clean_after == "", "owner_file_count": len(paths),
        "checks": checks, "detailed_rows": detailed, "minimal_rows": minimal,
        "same_owner_only": True, "independent_reproduction": False,
        "boundary": "Dependency-scoped same-owner validation only; not the full repository suite, independent reproduction, external audit, production certification, professional validation, legal or cultural review, Māori-authority review, complete privacy or accessibility assurance, exhaustive security, empirical GMUT confirmation, Theory-of-Everything proof, consciousness/personhood evidence, or Stage 20 authority.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(output)
    print(json.dumps({key: receipt[key] for key in ["valid", "exact_head", "scoped_tests", "detailed_checks", "minimal_checks", "json_parses", "privacy", "manifests", "phase_commits", "merges", "divergence", "clean_before", "clean_after"]}, ensure_ascii=False, sort_keys=True))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

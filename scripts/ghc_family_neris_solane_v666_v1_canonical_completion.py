#!/usr/bin/env python3
"""One-shot exact-final owner-scoped canonical completion for Neris v666-v1."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import traceback
import unittest
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PHASE = ROOT / "docs" / "neris-solane" / "v666-v1"
SOURCE_SHA = "4cf5028def85bcf89fbf4d0efe6c502a4b02be61"
X1_SHA = "435bfd997f7f56635f6ba63d8da7ea2505059a75"
EVIDENCE_SHA = "35e33b4c43dbef309f78bfd77168094fed32f939"
BRANCH = "codex/GHC-Family/neris-solane-v666-v1-full-tools"
EXCLUDED_TESTS = {
    "tests.test_ghc_family_neris_solane_v666_v1_x1.NerisSolaneV666V1X1Tests.test_strict_x1_only",
    "tests.test_ghc_family_neris_solane_v666_v1_x1.NerisSolaneV666V1X1Tests.test_x1_content_manifest_when_present",
    "tests.test_ghc_family_neris_solane_v666_v1_x2.NerisSolaneV666V1X2Tests.test_x1_commit_is_direct_parent_basis",
    "tests.test_ghc_family_neris_solane_v666_v1_x2.NerisSolaneV666V1X2Tests.test_terminal_verdict_and_no_route_artifact",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def git(*args: str, binary: bool = False, stderr: Any = None) -> bytes | str:
    raw = subprocess.check_output(["git", "-C", str(ROOT), *args], stderr=stderr)
    return raw if binary else raw.decode("utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def owner_paths() -> list[str]:
    paths = str(git("ls-tree", "-r", "--name-only", "HEAD")).splitlines()
    return sorted(
        path
        for path in paths
        if path.startswith("docs/neris-solane/v666-v1/")
        or re.fullmatch(r"(?:scripts|tests)/[a-z0-9_]*neris_solane_v666_v1[a-z0-9_]*\.py", path)
    )


def flatten(suite: unittest.TestSuite) -> Iterable[unittest.TestCase]:
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


def run_selected_tests() -> dict[str, Any]:
    modules = [
        "tests.test_ghc_family_neris_solane_v666_v1_x1",
        "tests.test_ghc_family_neris_solane_v666_v1_x2",
        "tests.test_ghc_family_neris_solane_v666_v1_evidence",
        "tests.test_ghc_family_neris_solane_v666_v1_closeout",
    ]
    loader = unittest.TestLoader()
    discovered = unittest.TestSuite(loader.loadTestsFromName(name) for name in modules)
    all_tests = list(flatten(discovered))
    selected = [test for test in all_tests if test.id() not in EXCLUDED_TESTS]
    selected_suite = unittest.TestSuite(selected)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(selected_suite)
    return {
        "discovered": len(all_tests),
        "selected": len(selected),
        "excluded": sorted(EXCLUDED_TESTS),
        "exclusion_credit": 0,
        "tests_run": result.testsRun,
        "failures": [test.id() for test, _ in result.failures],
        "errors": [test.id() for test, _ in result.errors],
        "skipped": [{"test": test.id(), "reason": reason} for test, reason in result.skipped],
        "successful": result.wasSuccessful(),
        "stream_sha256": hashlib.sha256(stream.getvalue().encode("utf-8")).hexdigest(),
    }


def parse_owner_json(paths: list[str]) -> dict[str, Any]:
    failures = []
    parsed = 0
    for path in paths:
        if not path.endswith(".json"):
            continue
        try:
            json.loads((ROOT / path).read_text(encoding="utf-8"))
            parsed += 1
        except Exception as exc:
            failures.append({"path": path, "error": type(exc).__name__})
    return {"parsed": parsed, "failures": failures, "passed": not failures}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)["\'](?:source_)?(?:task|thread)[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)["\'](?:session|resume)[_-]?(?:id|value)["\']\s*[:=]\s*["\'][^"\']+["\']'),
        "private_callable_identifier_value": re.compile(r'(?i)["\']private[_-]?callable[_-]?id["\']\s*[:=]\s*["\'][^"\']+["\']'),
    }
    candidates = []
    for path in paths:
        text = (ROOT / path).read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    return {
        "scanned_files": len(paths),
        "scan_classes": list(patterns),
        "candidates": candidates,
        "confirmed_hits": len(candidates),
        "passed": not candidates,
        "privacy_complete": False,
    }


def compile_and_security(paths: list[str]) -> dict[str, Any]:
    py_paths = [path for path in paths if path.endswith(".py")]
    compile_failures = []
    findings = []
    dangerous = {
        "shell_true": re.compile(r"shell\s*=\s*True"),
        "os_system": re.compile(r"\bos\.system\s*\("),
        "eval": re.compile(r"\beval\s*\("),
    }
    for path in py_paths:
        text = (ROOT / path).read_text(encoding="utf-8")
        try:
            compile(text, path, "exec")
        except Exception as exc:
            compile_failures.append({"path": path, "error": type(exc).__name__})
        for name, pattern in dangerous.items():
            if pattern.search(text):
                findings.append({"path": path, "class": name})
    return {
        "python_files": len(py_paths),
        "compile_failures": compile_failures,
        "bounded_security_findings": findings,
        "passed": not compile_failures and not findings,
        "exhaustive_security": False,
    }


class TagParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        self.tags.append((tag, dict(attrs)))


def accessibility_check() -> dict[str, Any]:
    text = (PHASE / "reports" / "static-report.html").read_text(encoding="utf-8")
    parser = TagParser()
    parser.feed(text)
    tags = [tag for tag, _ in parser.tags]
    html_attrs = next(attrs for tag, attrs in parser.tags if tag == "html")
    checks = {
        "language": html_attrs.get("lang") == "en-NZ",
        "single_h1": tags.count("h1") == 1,
        "main": "main" in tags,
        "navigation": "nav" in tags,
        "captions": tags.count("caption") >= 2,
        "reduced_motion": "prefers-reduced-motion" in text,
        "no_script": "<script" not in text.casefold(),
        "manual_evaluation_reserved": all(term in text for term in ("screen-reader", "keyboard", "zoom", "cognitive-accessibility", "Māori-language", "affected-user")),
    }
    return {"checks": checks, "passed": all(checks.values()), "accessibility_complete": False}


def replay_manifests(final_sha: str) -> dict[str, Any]:
    specs = [
        ("x1", "validation/x1-content-manifest.json", X1_SHA),
        ("evidence", "validation/evidence-content-manifest.json", EVIDENCE_SHA),
        ("final-delta", "validation/final-delta-manifest.json", final_sha),
        ("final-owner", "validation/final-owner-manifest.json", final_sha),
    ]
    results = []
    failures = []
    for name, relative, anchor in specs:
        manifest = load(relative)
        count = 0
        for entry in manifest["entries"]:
            blob = git("show", f"{anchor}:{entry['path']}", binary=True, stderr=subprocess.DEVNULL)
            count += 1
            if len(blob) != entry["size_bytes"] or hashlib.sha256(blob).hexdigest() != entry["sha256"]:  # type: ignore[arg-type]
                failures.append({"manifest": name, "path": entry["path"]})
        results.append({"manifest": name, "anchor": anchor, "entries": count})
    return {"manifests": results, "entry_count": sum(row["entries"] for row in results), "failures": failures, "passed": not failures}


def history_and_equality(expected_final: str) -> dict[str, Any]:
    current_branch = str(git("branch", "--show-current"))
    refspec = f"+refs/heads/{BRANCH}:refs/remotes/origin/{BRANCH}"
    subprocess.check_call(["git", "-C", str(ROOT), "fetch", "origin", refspec, "--quiet"])
    local = str(git("rev-parse", "HEAD"))
    upstream = str(git("rev-parse", "@{upstream}"))
    tracking = str(git("rev-parse", f"refs/remotes/origin/{BRANCH}"))
    live_lines = str(git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")).splitlines()
    live = live_lines[0].split()[0] if len(live_lines) == 1 else ""
    divergence = str(git("rev-list", "--left-right", "--count", "HEAD...@{upstream}")).split()
    commits = str(git("rev-list", "--reverse", f"{SOURCE_SHA}..{expected_final}")).splitlines()
    merges = str(git("rev-list", "--merges", f"{SOURCE_SHA}..{expected_final}")).splitlines()
    parents = {commit: len(str(git("show", "-s", "--format=%P", commit)).split()) for commit in commits}
    checks = {
        "branch": current_branch == BRANCH,
        "head": local == expected_final,
        "x1_parent": str(git("rev-parse", f"{X1_SHA}^")) == SOURCE_SHA,
        "evidence_parent": str(git("rev-parse", f"{EVIDENCE_SHA}^")) == X1_SHA,
        "final_parent": str(git("rev-parse", f"{expected_final}^")) == EVIDENCE_SHA,
        "phase_commits": commits == [X1_SHA, EVIDENCE_SHA, expected_final],
        "zero_merges": not merges,
        "single_parent_commits": all(value == 1 for value in parents.values()),
        "clean": not str(git("status", "--porcelain=v1")),
        "zero_divergence": divergence == ["0", "0"],
        "four_way_equal": len({local, upstream, tracking, live}) == 1,
        "fresh_live_remote": live == expected_final,
    }
    return {
        "checks": checks,
        "local": local,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "ahead": int(divergence[0]),
        "behind": int(divergence[1]),
        "commits": commits,
        "merge_count": len(merges),
        "parents": parents,
        "passed": all(checks.values()),
    }


def receipt_payload(expected_final: str) -> dict[str, Any]:
    paths = owner_paths()
    history = history_and_equality(expected_final)
    tests = run_selected_tests()
    json_result = parse_owner_json(paths)
    privacy = privacy_scan(paths)
    security = compile_and_security(paths)
    accessibility = accessibility_check()
    manifests = replay_manifests(expected_final)
    truth = load("closeout/phase-truth.json")
    route = load("orchestration/route-state-final-candidate.json")
    detailed_checks = {
        **{f"history_{key}": value for key, value in history["checks"].items()},
        "selected_tests": tests["successful"] and tests["tests_run"] == tests["selected"],
        "four_zero_credit_exclusions": len(tests["excluded"]) == 4 and tests["exclusion_credit"] == 0,
        "owner_json": json_result["passed"],
        "five_class_privacy": privacy["passed"],
        "compile_and_bounded_security": security["passed"],
        "structural_accessibility": accessibility["passed"],
        "four_manifest_replay": manifests["passed"] and len(manifests["manifests"]) == 4,
        "exact_counts": truth["effective_negatives"] == 26160 and truth["effective_methods"] == 10472 and truth["effective_open_gaps"] == 183 and truth["effective_exact_gates"] == 181,
        "exact_outcomes": truth["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "terminal_verdict": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route_prepared_not_sent": route["state"] == "PREPARED_NOT_SENT" and route["prospective_recipient_title"] == "Vesper Arlen" and route["successor_contact_count"] == 0 and route["standby_contact_count"] == 0,
        "owner_file_cap": len(paths) <= 2000,
        "final_delta_cap": load("validation/final-delta-manifest.json")["entry_count"] <= 2000,
    }
    minimal_checks = {
        "exact_head": history["checks"]["head"],
        "direct_chain": history["checks"]["x1_parent"] and history["checks"]["evidence_parent"] and history["checks"]["final_parent"],
        "history": history["checks"]["phase_commits"] and history["checks"]["zero_merges"] and history["checks"]["single_parent_commits"],
        "clean_zero_divergence": history["checks"]["clean"] and history["checks"]["zero_divergence"],
        "fresh_four_way_equal": history["checks"]["four_way_equal"] and history["checks"]["fresh_live_remote"],
        "tests": detailed_checks["selected_tests"],
        "json": json_result["passed"],
        "privacy": privacy["passed"],
        "security": security["passed"],
        "accessibility": accessibility["passed"],
        "manifests": manifests["passed"],
        "counts": detailed_checks["exact_counts"],
        "outcomes": detailed_checks["exact_outcomes"],
        "route": detailed_checks["route_prepared_not_sent"],
        "verdict": detailed_checks["terminal_verdict"],
    }
    success = all(detailed_checks.values()) and all(minimal_checks.values())
    payload = {
        "schema": "ghc.family.neris-solane.v666-v1.external-canonical-completion.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
        "generated_at_utc": now(),
        "expected_final": expected_final,
        "status": "SUCCESS_OWNER_SCOPED_CANONICAL_COMPLETION" if success else "FAILED_OWNER_SCOPED_CANONICAL_COMPLETION_ZERO_SUCCESS_CREDIT",
        "success": success,
        "canonical_invocation_count": 1,
        "successful_invocation_count": 1 if success else 0,
        "post_success_replay": False,
        "full_repository_suite": False,
        "same_owner_not_independent": True,
        "claim_boundary": "owner-self-scoped source-to-final software and documentation evidence only; not independent reproduction, exhaustive security, complete privacy/accessibility, professional/legal/cultural/Māori authority, empirical GMUT, AGI/ASI, personhood, Theory of Everything, or Stage 20",
        "owner_file_count": len(paths),
        "tests": tests,
        "json": json_result,
        "privacy": privacy,
        "security": security,
        "accessibility": accessibility,
        "manifests": manifests,
        "history_and_equality": history,
        "detailed_checks": detailed_checks,
        "detailed_passed": sum(detailed_checks.values()),
        "detailed_total": len(detailed_checks),
        "minimal_checks": minimal_checks,
        "minimal_passed": sum(minimal_checks.values()),
        "minimal_total": len(minimal_checks),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def write_receipt(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--expected-final", required=True)
    args = parser.parse_args()
    receipt = Path(args.receipt)
    if receipt.exists():
        raise SystemExit("exclusive canonical receipt already exists; replay refused")
    started = {
        "schema": "ghc.family.neris-solane.v666-v1.external-canonical-completion.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
        "generated_at_utc": now(),
        "expected_final": args.expected_final,
        "status": "STARTED",
        "success": False,
        "canonical_invocation_count": 1,
        "successful_invocation_count": 0,
        "post_success_replay": False,
    }
    write_receipt(receipt, started)
    try:
        payload = receipt_payload(args.expected_final)
    except Exception as exc:
        failed = {
            **started,
            "completed_at_utc": now(),
            "status": "FAILED_EXCEPTION_ZERO_SUCCESS_CREDIT",
            "error_class": type(exc).__name__,
            "error_digest": hashlib.sha256(traceback.format_exc().encode("utf-8")).hexdigest(),
            "success": False,
        }
        write_receipt(receipt, failed)
        print(json.dumps({"success": False, "status": failed["status"], "error_class": failed["error_class"]}, sort_keys=True))
        return 1
    write_receipt(receipt, payload)
    print(json.dumps({"success": payload["success"], "status": payload["status"], "tests": payload["tests"]["tests_run"], "detailed": f"{payload['detailed_passed']}/{payload['detailed_total']}", "minimal": f"{payload['minimal_passed']}/{payload['minimal_total']}", "manifest_entries": payload["manifests"]["entry_count"], "payload_sha256": payload["payload_sha256"]}, sort_keys=True))
    return 0 if payload["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

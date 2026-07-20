#!/usr/bin/env python3
"""Build exact staged review artifacts for the v649-v7 x2 evidence commit."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "eiren-kestrel" / "v649-v7"
X1 = "b1b3a4bde8dee07bc2bd4f8fc2c8d4b511cd723f"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout


def write(relative: str, payload) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def load(relative: str):
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    result = []
    for line in rows:
        raw = line[3:]
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        result.append(raw.strip('"').replace("\\", "/"))
    return sorted(set(result))


PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def main() -> int:
    if git("rev-parse", "HEAD").strip() != X1:
        raise RuntimeError("evidence review must run before the x2 evidence commit")
    exclusions = {
        "docs/eiren-kestrel/v649-v7/validation/evidence-staged-manifest.json",
        "docs/eiren-kestrel/v649-v7/validation/evidence-staged-privacy.json",
        "docs/eiren-kestrel/v649-v7/validation/evidence-staged-review.json",
    }
    changed = paths()
    allowed = all(
        path.startswith("docs/eiren-kestrel/v649-v7/")
        or (path.startswith("scripts/ghc_family_v649_v7_") and path.endswith(".py"))
        or (path.startswith("tests/test_ghc_family_v649_v7") and path.endswith(".py"))
        for path in changed
    )
    if not allowed:
        raise RuntimeError("out-of-scope x2 path")
    candidates, confirmed, entries = [], [], []
    scanner_definitions = {
        "scripts/ghc_family_v649_v7_x1.py",
        "scripts/ghc_family_v649_v7_evidence_review.py",
        "scripts/ghc_family_v649_v7_terminal_verify.py",
    }
    for relative in changed:
        if relative in exclusions:
            continue
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        blob = subprocess.run(["git", "hash-object", f"--path={relative}", relative], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()
        entries.append({"path": relative, "bytes": len(data), "git_blob": blob, "checkout_sha256": hashlib.sha256(data).hexdigest()})
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in scanner_definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    phase_json = sorted(OUT.rglob("*.json"))
    for path in phase_json:
        json.loads(path.read_text(encoding="utf-8"))
    word_violations = []
    for path in list(OUT.rglob("*.md")) + list(OUT.rglob("*.html")) + list(OUT.rglob("*.txt")):
        count = len(path.read_text(encoding="utf-8").split())
        if count > 20000:
            word_violations.append({"path": path.relative_to(OUT).as_posix(), "words": count})
    outcomes = load("x2/core-outcome-ledger.json")
    negatives = load("x2/retained-negative-register.json")
    skills = load("x2/skill-use-ledger.json")
    runners = load("x2/runner-use-ledger.json")
    method = load("method-flow/method-flow-summary.json")
    detailed = {
        "twenty_proposals": outcomes["proposal_count"] == 20,
        "distribution": outcomes["distribution"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "one_hundred_mutations": load("x2/synthetic-mutation-results.json")["rejected_count"] == 100,
        "safe_tasks": load("x2/safe-now-results.json")["completed_count"] == 40,
        "candidates": load("x2/candidate-results.json")["completed_count"] == 30,
        "skills": skills["completed_count"] == 20 and skills["pending_count"] == 0,
        "runners": runners["completed_count"] == 10 and runners["pending_count"] == 0,
        "clean_refine": load("x2/clean-fix-refine-results.json")["completed_count"] == 40,
        "negatives": negatives["effective_at_evidence"] == 5312 and not negatives["negative_erased"],
        "gates": load("x2/gate-register.json")["silently_closed"] == 0,
        "method_flow": method["counts"]["methods"] == 13 and method["counts"]["witness_results"] == {"fail": 13, "pass": 13},
        "workflow_remaster": load("workflow/general-validator-receipt.json")["passed"] is True,
        "all_json": len(phase_json) >= 160,
        "privacy": not confirmed,
        "word_caps": not word_violations,
        "stage20": outcomes["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    write("validation/evidence-staged-privacy.json", {
        "schema": "ghc.family.v649-v7.evidence-privacy.v1", "scanned_file_count": len(changed),
        "pattern_class_count": len(PATTERNS), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
    })
    write("validation/evidence-staged-manifest.json", {
        "schema": "ghc.family.v649-v7.evidence-manifest.v1", "hash_domain": "git_hash_object_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
    })
    write("validation/evidence-staged-review.json", {
        "schema": "ghc.family.v649-v7.evidence-review.v1", "passed": all(detailed.values()),
        "detailed_checks": detailed, "detailed_passed": sum(detailed.values()), "detailed_total": len(detailed),
        "changed_path_count": len(changed), "manifest_entries": len(entries), "self_exclusions": len(exclusions),
        "out_of_scope_paths": [] if allowed else changed, "phase_json_parses": len(phase_json),
        "privacy_confirmed_hits": confirmed, "word_cap_violations": word_violations,
        "full_repository_suite": False, "replay": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    print(json.dumps({"passed": all(detailed.values()), "detailed": f"{sum(detailed.values())}/{len(detailed)}", "manifest": len(entries), "json": len(phase_json), "privacy_hits": len(confirmed)}, sort_keys=True))
    return 0 if all(detailed.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())

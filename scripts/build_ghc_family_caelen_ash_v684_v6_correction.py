#!/usr/bin/env python3
"""Build the additive Caelen Ash v684-v6 canonical-loader correction."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v684-v6"
OWNER = "Caelen Ash"
BASE = ROOT / "docs" / "caelen-ash" / PHASE
CLOSEOUT = BASE / "closeout"
FINAL = BASE / "final"
CORRECTION = BASE / "correction"
HANDOFF = BASE / "handoffs" / "orin-thale-v684-v7-activation-candidate.md"
VALIDATION = BASE / "validation"
SOURCE = "9a2fcdc6021dcc8226ff7150b990bfe429671680"
X1 = "ab50360d737177ab1ebe4564b348a88b540c9ed4"
EVIDENCE = "ca4ac41d8984e8fcec58982bfd6507030dcd1480"
FIRST_FINAL = "af3cf6bdf1a5d890ccf417e6f6c9c203c0a7f563"
BRANCH = "codex/GHC-Family/caelen-ash-v684-v6-full-tools"
FAILED_RECEIPT_SHA256 = "f29c19e221ad81bac5eed025d6363ede57899909f936a0ce49630b79bd5e0f26"
FAILED_PAYLOAD_SHA256 = "bdfe76e0f73e2db6b94be6870806f65a92ae678c88f772f9f5a0ead4f5e7a93c"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
    )


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def staged_sha(rel: str) -> str:
    data = subprocess.run(
        ["git", "show", f":{rel}"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def owner_files() -> list[Path]:
    result = [path for path in BASE.rglob("*") if path.is_file()]
    result.extend(
        path
        for path in [
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_x1.py",
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_x2.py",
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_final.py",
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_correction.py",
            ROOT / "scripts" / "ghc_family_caelen_ash_v684_v6_contracts.py",
            ROOT / "scripts" / "ghc_family_caelen_ash_v684_v6_canonical.py",
            ROOT / "tests" / "test_ghc_family_caelen_ash_v684_v6_x1.py",
            ROOT / "tests" / "test_ghc_family_caelen_ash_v684_v6_x2.py",
            ROOT / "tests" / "test_ghc_family_caelen_ash_v684_v6_final.py",
        ]
        if path.exists()
    )
    return sorted(set(result), key=lambda path: path.relative_to(ROOT).as_posix())


def correction_delta_files() -> list[Path]:
    result: list[Path] = []
    for path in owner_files():
        rel = path.relative_to(ROOT).as_posix()
        blob = subprocess.run(
            ["git", "show", f"{FIRST_FINAL}:{rel}"],
            cwd=ROOT,
            check=False,
            capture_output=True,
        )
        if blob.returncode != 0:
            result.append(path)
            continue
        old = blob.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if old != normalized_bytes(path):
            result.append(path)
    return sorted(result, key=lambda path: path.relative_to(ROOT).as_posix())


def append_once(path: Path, marker: str, section: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        write_text(path, text.rstrip() + "\n\n" + section)


def privacy_scan(paths: Iterable[Path]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "credential_or_secret_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+", re.I),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(r"\b(?:providerTabId|clientThreadId|private callable identifier)\b", re.I),
    }
    definitions = {
        "scripts/build_ghc_family_caelen_ash_v684_v6_x1.py",
        "scripts/build_ghc_family_caelen_ash_v684_v6_x2.py",
        "scripts/build_ghc_family_caelen_ash_v684_v6_final.py",
        "scripts/build_ghc_family_caelen_ash_v684_v6_correction.py",
        "scripts/ghc_family_caelen_ash_v684_v6_canonical.py",
    }
    candidates: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    scanned = 0
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".yaml", ".yml", ".txt"}:
            continue
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            for match in pattern.finditer(text):
                definition = rel in definitions
                item = {
                    "path": rel,
                    "line": text.count("\n", 0, match.start()) + 1,
                    "class": label,
                    "disposition": "scanner_definition_not_payload" if definition else "confirmed_payload_hit",
                }
                candidates.append(item)
                if not definition:
                    confirmed.append(item)
    return {
        "schema": "ghc.family.privacy-scan.v2",
        "phase": PHASE,
        "scope": "complete corrected public owner packet",
        "pattern_classes": list(patterns),
        "files_scanned": scanned,
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "truth_boundary": "Bounded pattern evidence only; not complete privacy assurance.",
    }


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != FIRST_FINAL:
        raise SystemExit("correction build requires the retained first-final head")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise SystemExit("unexpected owner branch")
    tracked = set(git("diff", "--name-only").stdout.splitlines())
    protected_prefixes = (
        f"docs/caelen-ash/{PHASE}/x1/",
        f"docs/caelen-ash/{PHASE}/x2/",
        f"docs/caelen-ash/{PHASE}/method-flow/",
        f"docs/caelen-ash/{PHASE}/workflow-refinement/",
        f"docs/caelen-ash/{PHASE}/reflection-remaster/",
        f"docs/caelen-ash/{PHASE}/tooling/",
    )
    protected_drift = sorted(
        rel for rel in tracked if any(rel.startswith(prefix) for prefix in protected_prefixes)
    )
    if protected_drift:
        raise SystemExit(f"immutable x1 or x2 drift before correction: {protected_drift}")

    write_json(
        CORRECTION / "canonical-failure-receipt.json",
        {
            "schema": "ghc.family.canonical-failure-receipt.v2",
            "phase": PHASE,
            "owner": OWNER,
            "first_final": FIRST_FINAL,
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "canonical_invocations": 1,
            "canonical_successes": 0,
            "selected_tests": {"passed": 0, "selected": 1, "errors": 1},
            "failed_gate": "selected_tests",
            "cause": "Direct script launch placed the scripts directory, not the repository root, on the module search path; unittest therefore produced one import-loader error before owner tests ran.",
            "receipt_sha256": FAILED_RECEIPT_SHA256,
            "payload_sha256": FAILED_PAYLOAD_SHA256,
            "other_observed_evidence": {
                "detailed": "39/40",
                "minimal": "14/15",
                "json": "241/241",
                "manifest_entries": 606,
                "owner_files": 310,
                "privacy_confirmed": 0,
                "security_findings": 0,
            },
            "replay_at_first_final": False,
            "credit": "zero canonical-success credit",
        },
    )
    write_json(
        CORRECTION / "method-flow-correction.json",
        {
            "schema": "ghc.family.method-flow-correction.v2",
            "phase": PHASE,
            "failed_witnesses": [
                {
                    "id": "CA6846-FINAL-N001",
                    "state": "failed_retained_zero_credit",
                    "head": FIRST_FINAL,
                    "method": "direct canonical script selected-test loader",
                    "observation": "The loader returned one import error and ran zero owner tests because the repository root was absent from the process-local module search path.",
                    "receipt_sha256": FAILED_RECEIPT_SHA256,
                },
                {
                    "id": "CA6846-FINAL-N002",
                    "state": "failed_retained_zero_credit",
                    "method": "stage the exact correction manifest allowlist before materializing the new builder path in sparse-checkout",
                    "observation": "Git staged the already materialized allowlist paths, then rejected the correction builder because that one path was outside the exact sparse definition; the partial index was inspected and later replaced by a fresh exact allowlist stage.",
                },
                {
                    "id": "CA6846-FINAL-N003",
                    "state": "failed_retained_zero_credit",
                    "method": "add the correction builder with an unsupported sparse-checkout add --no-cone option",
                    "observation": "The installed Git rejected the unsupported option before changing the sparse definition.",
                }
            ],
            "preferred_recovery_methods": [
                {
                    "id": "CA6846-FINAL-M001",
                    "state": "bounded_passing_witness",
                    "method": "insert the already-resolved repository root into process-local sys.path before unittest discovery",
                    "scope": "canonical selected-test import context only",
                    "recurrence_guard": "A corrected-head canonical loads the committed module through the exact same direct-script entry point; the failed first-final invocation is never replayed.",
                },
                {
                    "id": "CA6846-FINAL-M002",
                    "state": "bounded_passing_witness",
                    "method": "materialize the exact correction-builder path before staging its manifest-declared allowlist",
                    "scope": "owner-local sparse definition only",
                    "recurrence_guard": "Every new final or correction script path is checked against sparse-checkout before git add.",
                },
                {
                    "id": "CA6846-FINAL-M003",
                    "state": "bounded_passing_witness",
                    "method": "use the installed sparse-checkout add --skip-checks literal-pattern contract",
                    "scope": "one literal owner script path",
                    "recurrence_guard": "Inspect the installed subcommand help before assuming mode-selection flags are accepted by add.",
                }
            ],
            "nonerasure": True,
        },
    )
    overview = f"""# Caelen Ash {PHASE} additive terminal correction

The retained first exact final is `{FIRST_FINAL}`. Its one canonical invocation
is immutable and failed with zero canonical-success credit. All non-test owner
checks completed, but direct script launch placed the scripts directory rather
than the repository root on Python's process-local module search path. The
unittest loader therefore produced one import error, selected a single failed
loader placeholder, and ran zero Caelen final tests. The external failed
receipt has SHA-256 `{FAILED_RECEIPT_SHA256}` and payload SHA-256
`{FAILED_PAYLOAD_SHA256}`.

This additive correction changes only the selected-test import context and the
truth surfaces required to preserve that failure. It inserts the already
resolved repository root into process-local `sys.path` before unittest
discovery. It does not alter x1, x2 evidence, proposal outcomes, positive
fixtures, rejecting mutations, scientific content, privacy boundaries, or any
authority gate. The original canonical invocation is not replayed, renamed,
or promoted. A new exact-final canonical invocation is permitted only after a
separate correction commit is pushed, clean, zero-divergent, and fresh-four-way
equal.

The additive repository view is 59,733 effective negatives, 73,693 effective
methods, 30,794 retained failed witnesses, and 54,228 bounded passing
witnesses. Open gaps remain 531 and exact gates remain 521. The successful
process-local import correction earns one bounded recovery witness only; it
does not compensate for the failed canonical. The terminal verdict remains
exactly `NOT_READY_FOR_STAGE_20`.

No claim boundary changes. The work remains same-owner synthetic software and
documentation evidence. It establishes no wind-tunnel measurement,
aerodynamic result, empirical GMUT confirmation, professional competence,
production THOS or Freed ID readiness, legal or cultural legitimacy, affected
party approval, Māori authority, independent reproduction, proof, canon,
consciousness, personhood, AGI, ASI, Theory of Everything, or Stage 20
authority.
"""
    write_text(CORRECTION / "terminal-correction-overview.md", overview)
    write_json(
        CORRECTION / "terminal-correction.json",
        {
            "schema": "ghc.family.terminal-correction.v2",
            "phase": PHASE,
            "owner": OWNER,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "retained_first_final": FIRST_FINAL,
            "corrected_final": "PENDING_COMMIT",
            "first_canonical": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "corrected_canonical": "PENDING_POSTCOMMIT",
            "phase_commits_after_correction": 4,
            "merges": 0,
            "counts": {
                "effective_negatives": 59733,
                "effective_methods": 73693,
                "retained_failed_witnesses": 30794,
                "bounded_passing_witnesses": 54228,
                "open_gaps": 531,
                "exact_gates": 521,
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    register = load(CLOSEOUT / "retained-negative-register.json")
    register.update(
        {
            "canonical_preflight_operational_failures": 1,
            "canonical_preflight_recoveries": 1,
            "correction_staging_operational_failures": 2,
            "correction_staging_recoveries": 2,
            "effective_negatives": 59733,
            "effective_methods": 73693,
            "retained_failed_witnesses": 30794,
            "bounded_passing_witnesses": 54228,
        }
    )
    register["canonical_failure_records"] = [
        {
            "id": "CA6846-FINAL-N001",
            "head": FIRST_FINAL,
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "receipt_sha256": FAILED_RECEIPT_SHA256,
            "replayed": False,
        }
    ]
    register["correction_staging_failure_records"] = [
        {
            "id": "CA6846-FINAL-N002",
            "status": "FAILED_RETAINED_ZERO_CREDIT",
            "cause": "The first exact staging attempt partially staged materialized allowlist paths before refusing the new correction-builder path outside sparse-checkout.",
            "index_changed": True,
            "index_change": "partial manifest-declared staging only; later rebuilt and restaged from the exact allowlist",
        },
        {
            "id": "CA6846-FINAL-N003",
            "status": "FAILED_RETAINED_ZERO_CREDIT",
            "cause": "The first sparse-add recovery used an unsupported add --no-cone option.",
            "sparse_definition_changed": False,
        },
    ]
    write_json(CLOSEOUT / "retained-negative-register.json", register)

    route = load(CLOSEOUT / "route-readiness.json")
    route.update(
        {
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
            "retained_first_final": FIRST_FINAL,
            "first_canonical": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "corrected_final": "PENDING_COMMIT",
            "corrected_canonical": "PENDING_POSTCOMMIT",
        }
    )
    write_json(CLOSEOUT / "route-readiness.json", route)

    candidate = load(CLOSEOUT / "final-validation-candidate.json")
    candidate.update(
        {
            "state": "CORRECTION_PRECOMMIT_PENDING_EXACT_FINAL_AND_EXTERNAL_CANONICAL",
            "required_parent": FIRST_FINAL,
            "required_phase_commits": 4,
            "retained_failed_canonical_head": FIRST_FINAL,
            "retained_failed_canonical_receipt_sha256": FAILED_RECEIPT_SHA256,
            "canonical_invocation_budget": 1,
            "replay_after_success": False,
        }
    )
    write_json(CLOSEOUT / "final-validation-candidate.json", candidate)

    truth = load(FINAL / "phase-truth.json")
    truth.update(
        {
            "lifecycle": "FINAL_CORRECTION_CANDIDATE_PRECOMMIT",
            "retained_first_final": FIRST_FINAL,
            "exact_final": "PENDING_COMMIT",
            "external_canonical": "FIRST_FINAL_FAILED_CORRECTED_HEAD_PENDING",
            "effective_negatives": 59733,
            "effective_methods": 73693,
            "retained_failed_witnesses": 30794,
            "bounded_passing_witnesses": 54228,
        }
    )
    write_json(FINAL / "phase-truth.json", truth)

    summary = load(FINAL / "final-summary.json")
    summary.update(
        {
            "retained_first_final": FIRST_FINAL,
            "exact_final": "PENDING_CORRECTION_COMMIT",
            "canonical": "FIRST_FINAL_FAILED_CORRECTED_HEAD_PENDING",
        }
    )
    write_json(FINAL / "final-summary.json", summary)

    correction_section = f"""## Retained first-final canonical failure and additive correction

The first exact final `{FIRST_FINAL}` remains immutable. Its one canonical
invocation failed with zero canonical-success credit because direct script
launch omitted the repository root from Python's process-local module search
path; the unittest loader reported one import error and ran zero Caelen final
tests. The failure receipt SHA-256 is `{FAILED_RECEIPT_SHA256}`. It was not
replayed at that head. This additive correction changes only that import
context and the associated nonerasure records. The successor must treat the
later corrected-final hash and its one separately attributable canonical
receipt, supplied by the live activation, as the terminal source. The terminal
verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    append_once(FINAL / "final-integrated-overview.md", "## Retained first-final canonical failure", correction_section)
    append_once(HANDOFF, "## Retained first-final canonical failure", correction_section)

    seal = load(CLOSEOUT / "content-seal.json")
    for entry in seal["entries"]:
        path = ROOT / entry["path"]
        entry["sha256_normalized_lf"] = normalized_sha(path)
    seal.update(
        {
            "exact_final": "PENDING_CORRECTION_COMMIT",
            "retained_first_final": FIRST_FINAL,
            "first_canonical": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
        }
    )
    write_json(CLOSEOUT / "content-seal.json", seal)

    exclusions = {
        f"docs/caelen-ash/{PHASE}/validation/correction-delta-manifest.json",
        f"docs/caelen-ash/{PHASE}/validation/correction-owner-manifest.json",
        f"docs/caelen-ash/{PHASE}/validation/correction-privacy-scan.json",
        f"docs/caelen-ash/{PHASE}/validation/correction-staged-review.json",
    }
    current_paths = {path.relative_to(ROOT).as_posix() for path in owner_files()}
    summary = load(FINAL / "final-summary.json")
    summary["owner_files"] = len(current_paths | exclusions)
    write_json(FINAL / "final-summary.json", summary)
    write_json(VALIDATION / "correction-privacy-scan.json", privacy_scan(owner_files()))

    delta_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256_normalized_lf": normalized_sha(path),
            "bytes_normalized_lf": len(normalized_bytes(path)),
        }
        for path in correction_delta_files()
        if path.relative_to(ROOT).as_posix() not in exclusions
    ]
    write_json(
        VALIDATION / "correction-delta-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v2",
            "phase": PHASE,
            "lifecycle": "terminal_correction_delta",
            "retained_first_final": FIRST_FINAL,
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "self_exclusions": sorted(exclusions),
        },
    )
    owner_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256_normalized_lf": normalized_sha(path),
            "bytes_normalized_lf": len(normalized_bytes(path)),
        }
        for path in owner_files()
        if path.relative_to(ROOT).as_posix() not in exclusions
    ]
    write_json(
        VALIDATION / "correction-owner-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v2",
            "phase": PHASE,
            "lifecycle": "corrected_owner_packet",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusions": sorted(exclusions),
            "owner_file_count": len(owner_entries) + len(exclusions),
            "file_ceiling": 2000,
        },
    )
    write_json(
        VALIDATION / "correction-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "phase": PHASE,
            "state": "PREPARED_NOT_STAGED",
            "staged_count": 0,
            "manifest_entry_count": len(delta_entries),
            "self_exclusions": sorted(exclusions),
            "exact_staged_allowlist": [],
            "manifest_mismatches": [],
            "missing_paths": [],
            "out_of_scope_paths": [],
            "inherited_paths_changed": [],
            "diff_hygiene": "PENDING_STAGING",
        },
    )


def review_staged() -> None:
    manifest = load(VALIDATION / "correction-delta-manifest.json")
    expected = {entry["path"]: entry["sha256_normalized_lf"] for entry in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    staged = [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if line]
    expected_all = set(expected) | exclusions
    mismatches: list[dict[str, str]] = []
    for rel, wanted in sorted(expected.items()):
        try:
            actual = staged_sha(rel)
        except subprocess.CalledProcessError:
            mismatches.append({"path": rel, "error": "missing_from_index"})
            continue
        if actual != wanted:
            mismatches.append({"path": rel, "expected": wanted, "actual": actual})
    inherited_prefixes = [
        f"docs/caelen-ash/{PHASE}/x1/",
        f"docs/caelen-ash/{PHASE}/x2/",
        f"docs/caelen-ash/{PHASE}/method-flow/",
        f"docs/caelen-ash/{PHASE}/workflow-refinement/",
        f"docs/caelen-ash/{PHASE}/reflection-remaster/",
        f"docs/caelen-ash/{PHASE}/tooling/",
    ]
    inherited = [rel for rel in staged if any(rel.startswith(prefix) for prefix in inherited_prefixes)]
    diff = git("diff", "--cached", "--check", check=False)
    missing = sorted(expected_all - set(staged))
    out_of_scope = sorted(set(staged) - expected_all)
    passed = not mismatches and not missing and not out_of_scope and not inherited and diff.returncode == 0
    write_json(
        VALIDATION / "correction-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "phase": PHASE,
            "state": "PASS" if passed else "FAIL",
            "staged_count": len(staged),
            "manifest_entry_count": len(expected),
            "self_exclusions": sorted(exclusions),
            "exact_staged_allowlist": staged,
            "manifest_mismatches": mismatches,
            "missing_paths": missing,
            "out_of_scope_paths": out_of_scope,
            "inherited_paths_changed": inherited,
            "diff_hygiene": "PASS" if diff.returncode == 0 else "FAIL",
            "diff_hygiene_output": diff.stdout + diff.stderr,
        },
    )
    if not passed:
        raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    if args.review_staged:
        review_staged()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

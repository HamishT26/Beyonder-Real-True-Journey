#!/usr/bin/env python3
"""Build Caelen v684-v6's additive canonical privacy-definition correction."""

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
SECOND_FINAL = "93f1ead9b0d28baa93870c2b4fb67140055014c0"
BRANCH = "codex/GHC-Family/caelen-ash-v684-v6-full-tools"
FAILED_RECEIPT_SHA256 = "b3d1cf8850de3cbcb32515c86eac30221aa536cdba2e4a13901ff50b2b73612b"
FAILED_PAYLOAD_SHA256 = "154c9bd2f9c98d018390b5eecff3cbd780d6ebe65ac020415d41a851fd986ec8"
SCANNER_DEFINITION_PATH = "scripts/build_ghc_family_caelen_ash_v684_v6_correction.py"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, text=True,
        encoding="utf-8", errors="strict", capture_output=True
    )


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n"
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def commit_blob_sha(commit: str, rel: str) -> str:
    data = subprocess.run(
        ["git", "show", f"{commit}:{rel}"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def staged_sha(rel: str) -> str:
    data = subprocess.run(
        ["git", "show", f":{rel}"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def owner_files() -> list[Path]:
    result = [path for path in BASE.rglob("*") if path.is_file()]
    result.extend(
        path for path in [
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_x1.py",
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_x2.py",
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_final.py",
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_correction.py",
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_privacy_correction.py",
            ROOT / "scripts" / "ghc_family_caelen_ash_v684_v6_contracts.py",
            ROOT / "scripts" / "ghc_family_caelen_ash_v684_v6_canonical.py",
            ROOT / "tests" / "test_ghc_family_caelen_ash_v684_v6_x1.py",
            ROOT / "tests" / "test_ghc_family_caelen_ash_v684_v6_x2.py",
            ROOT / "tests" / "test_ghc_family_caelen_ash_v684_v6_final.py",
        ] if path.exists()
    )
    return sorted(set(result), key=lambda path: path.relative_to(ROOT).as_posix())


def delta_files() -> list[Path]:
    result: list[Path] = []
    for path in owner_files():
        rel = path.relative_to(ROOT).as_posix()
        blob = subprocess.run(
            ["git", "show", f"{SECOND_FINAL}:{rel}"],
            cwd=ROOT, check=False, capture_output=True
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
        "scripts/build_ghc_family_caelen_ash_v684_v6_privacy_correction.py",
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
        "scope": "complete second-corrected public owner packet",
        "pattern_classes": list(patterns),
        "files_scanned": scanned,
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "truth_boundary": "Bounded pattern evidence only; not complete privacy assurance.",
    }


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SECOND_FINAL:
        raise SystemExit("privacy correction build requires the retained second-final head")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise SystemExit("unexpected owner branch")
    protected = (
        f"docs/caelen-ash/{PHASE}/x1/", f"docs/caelen-ash/{PHASE}/x2/",
        f"docs/caelen-ash/{PHASE}/method-flow/", f"docs/caelen-ash/{PHASE}/workflow-refinement/",
        f"docs/caelen-ash/{PHASE}/reflection-remaster/", f"docs/caelen-ash/{PHASE}/tooling/",
    )
    drift = [rel for rel in git("diff", "--name-only").stdout.splitlines() if any(rel.startswith(prefix) for prefix in protected)]
    if drift:
        raise SystemExit(f"immutable x1 or x2 drift before privacy correction: {drift}")

    write_json(
        CORRECTION / "canonical-privacy-failure-receipt.json",
        {
            "schema": "ghc.family.canonical-failure-receipt.v2",
            "phase": PHASE,
            "owner": OWNER,
            "second_final": SECOND_FINAL,
            "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "canonical_invocations": 1,
            "canonical_successes": 0,
            "tests": "25/25",
            "detailed": "41/42",
            "minimal": "14/15",
            "json": "248/248",
            "manifest_entries": 936,
            "owner_files": 319,
            "privacy_confirmed": 4,
            "security_findings": 0,
            "failed_gate": "privacy",
            "cause": "Four regex literals in the correction builder were conservatively classified as payload because that immutable scanner-definition file was absent from the canonical definition-file set.",
            "receipt_sha256": FAILED_RECEIPT_SHA256,
            "payload_sha256": FAILED_PAYLOAD_SHA256,
            "replay_at_second_final": False,
            "credit": "zero canonical-success credit",
        },
    )
    write_json(
        CORRECTION / "privacy-adjudication.json",
        {
            "schema": "ghc.family.privacy-adjudication.v2",
            "phase": PHASE,
            "immutable_head": SECOND_FINAL,
            "path": SCANNER_DEFINITION_PATH,
            "sha256_normalized_lf": commit_blob_sha(SECOND_FINAL, SCANNER_DEFINITION_PATH),
            "candidates": [
                {"line": 127, "class": "private_absolute_local_path", "disposition": "scanner_definition_not_payload"},
                {"line": 130, "class": "private_application_state", "disposition": "scanner_definition_not_payload"},
                {"line": 130, "class": "private_application_state", "disposition": "scanner_definition_not_payload"},
                {"line": 130, "class": "private_application_state", "disposition": "scanner_definition_not_payload"},
            ],
            "candidate_count": 4,
            "confirmed_payload_hits": 0,
            "scope": "Only the exact immutable regex-definition blob named above is adjudicated; no other candidate is suppressed.",
            "complete_privacy_assurance": False,
        },
    )
    write_json(
        CORRECTION / "privacy-method-flow-correction.json",
        {
            "schema": "ghc.family.method-flow-correction.v2",
            "phase": PHASE,
            "failed_witnesses": [
                {
                    "id": "CA6846-FINAL-N004",
                    "state": "failed_retained_zero_credit",
                    "method": "inline PowerShell live-remote split projection",
                    "observation": "Operator precedence returned the first character rather than the remote hash; no repository or remote state changed.",
                },
                {
                    "id": "CA6846-FINAL-N005",
                    "state": "failed_retained_zero_credit",
                    "head": SECOND_FINAL,
                    "method": "second exact-final canonical privacy classification",
                    "observation": "All tests and nonprivacy gates passed, but four scanner-definition literals were classified as payload because the definition file was not registered.",
                    "receipt_sha256": FAILED_RECEIPT_SHA256,
                },
            ],
            "preferred_recovery_methods": [
                {
                    "id": "CA6846-FINAL-M004",
                    "state": "bounded_passing_witness",
                    "method": "materialize the ls-remote output before splitting its tab-delimited hash",
                    "scope": "read-only equality projection only",
                },
                {
                    "id": "CA6846-FINAL-M005",
                    "state": "bounded_passing_witness",
                    "method": "register the exact immutable correction builder as a scanner-definition file and retain the four-candidate adjudication",
                    "scope": "one exact Git-blob path only",
                },
            ],
            "nonerasure": True,
        },
    )
    write_text(
        CORRECTION / "privacy-correction-overview.md",
        f"""# Caelen Ash {PHASE} privacy-definition correction

The retained second final is `{SECOND_FINAL}`. Its single canonical invocation
ran all 25 owner tests successfully and passed JSON, manifests, ancestry,
security, clean-state, divergence, and remote-equality gates. It nevertheless
failed with zero canonical-success credit because four regular-expression
literals in `{SCANNER_DEFINITION_PATH}` were conservatively reported as
privacy payload. That file defines the scanner itself. Exact immutable-blob
adjudication confirms the four candidates are definition syntax and confirms
zero payload hits; it does not suppress any other path or assert complete
privacy assurance.

The failed receipt SHA-256 is `{FAILED_RECEIPT_SHA256}` and its payload
SHA-256 is `{FAILED_PAYLOAD_SHA256}`. It is not replayed. This additive commit
registers only the exact correction-builder path in the canonical definition
set, preserves both earlier failed canonical receipts, and carries one
read-only live-remote projection failure separately. The additive repository
view is 59,735 effective negatives, 73,695 methods, 30,796 retained failed
witnesses, and 54,230 bounded passing witnesses. Open gaps remain 531, exact
gates remain 521, and the terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )

    register = load(CLOSEOUT / "retained-negative-register.json")
    register.update(
        {
            "post_correction_route_projection_failures": 1,
            "post_correction_route_projection_recoveries": 1,
            "privacy_canonical_operational_failures": 1,
            "privacy_canonical_recoveries": 1,
            "effective_negatives": 59735,
            "effective_methods": 73695,
            "retained_failed_witnesses": 30796,
            "bounded_passing_witnesses": 54230,
        }
    )
    canonical_records = register.setdefault("canonical_failure_records", [])
    if not any(item.get("id") == "CA6846-FINAL-N005" for item in canonical_records):
        canonical_records.append(
            {
                "id": "CA6846-FINAL-N005",
                "head": SECOND_FINAL,
                "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
                "receipt_sha256": FAILED_RECEIPT_SHA256,
                "replayed": False,
            }
        )
    register["post_correction_route_projection_failure_records"] = [
        {
            "id": "CA6846-FINAL-N004",
            "status": "FAILED_RETAINED_ZERO_CREDIT",
            "state_change": False,
            "recovery": "materialized scalar output before tab split",
        }
    ]
    write_json(CLOSEOUT / "retained-negative-register.json", register)

    route = load(CLOSEOUT / "route-readiness.json")
    route.update(
        {
            "state": "PREPARED_NOT_SENT",
            "send_count": 0,
            "retained_second_final": SECOND_FINAL,
            "second_canonical": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
            "privacy_corrected_final": "PENDING_COMMIT",
            "privacy_corrected_canonical": "PENDING_POSTCOMMIT",
        }
    )
    write_json(CLOSEOUT / "route-readiness.json", route)

    candidate = load(CLOSEOUT / "final-validation-candidate.json")
    candidate.update(
        {
            "state": "PRIVACY_CORRECTION_PRECOMMIT_PENDING_EXACT_FINAL_AND_EXTERNAL_CANONICAL",
            "required_parent": SECOND_FINAL,
            "required_phase_commits": 5,
            "retained_second_failed_canonical_head": SECOND_FINAL,
            "retained_second_failed_canonical_receipt_sha256": FAILED_RECEIPT_SHA256,
            "canonical_invocation_budget": 1,
            "replay_after_success": False,
        }
    )
    write_json(CLOSEOUT / "final-validation-candidate.json", candidate)

    truth = load(FINAL / "phase-truth.json")
    truth.update(
        {
            "lifecycle": "FINAL_PRIVACY_CORRECTION_CANDIDATE_PRECOMMIT",
            "retained_second_final": SECOND_FINAL,
            "exact_final": "PENDING_COMMIT",
            "external_canonical": "TWO_FAILED_CANONICAL_HEADS_PRIVACY_CORRECTION_PENDING",
            "effective_negatives": 59735,
            "effective_methods": 73695,
            "retained_failed_witnesses": 30796,
            "bounded_passing_witnesses": 54230,
        }
    )
    write_json(FINAL / "phase-truth.json", truth)
    summary = load(FINAL / "final-summary.json")
    summary.update(
        {
            "retained_second_final": SECOND_FINAL,
            "exact_final": "PENDING_PRIVACY_CORRECTION_COMMIT",
            "canonical": "TWO_FAILED_CANONICAL_HEADS_PRIVACY_CORRECTION_PENDING",
        }
    )
    write_json(FINAL / "final-summary.json", summary)

    section = f"""## Retained second-final privacy-gate failure

The second final `{SECOND_FINAL}` is also immutable. Its one canonical
invocation passed all 25 owner tests and every nonprivacy gate but failed with
zero canonical-success credit because four regex literals in
`{SCANNER_DEFINITION_PATH}` were not yet classified as scanner definitions.
The failed receipt SHA-256 is `{FAILED_RECEIPT_SHA256}`. Exact blob adjudication
confirms those four candidates are definition syntax and finds zero confirmed
payload hits; it does not claim complete privacy assurance. This second
additive correction changes only the definition-file set and nonerasure truth.
The later live activation supplies the final corrected head and its separately
attributable canonical receipt. `NOT_READY_FOR_STAGE_20` remains unchanged.
"""
    append_once(FINAL / "final-integrated-overview.md", "## Retained second-final privacy-gate failure", section)
    append_once(HANDOFF, "## Retained second-final privacy-gate failure", section)

    handoff_receipt = load(CLOSEOUT / "handoff-candidate-receipt.json")
    words = len(HANDOFF.read_text(encoding="utf-8").split())
    handoff_receipt.update({"words": words, "within_range": 10000 <= words <= 100000})
    write_json(CLOSEOUT / "handoff-candidate-receipt.json", handoff_receipt)

    seal = load(CLOSEOUT / "content-seal.json")
    for entry in seal["entries"]:
        entry["sha256_normalized_lf"] = normalized_sha(ROOT / entry["path"])
    seal.update(
        {
            "exact_final": "PENDING_PRIVACY_CORRECTION_COMMIT",
            "retained_second_final": SECOND_FINAL,
            "second_canonical": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT",
        }
    )
    write_json(CLOSEOUT / "content-seal.json", seal)

    exclusions = {
        f"docs/caelen-ash/{PHASE}/validation/privacy-correction-delta-manifest.json",
        f"docs/caelen-ash/{PHASE}/validation/privacy-correction-owner-manifest.json",
        f"docs/caelen-ash/{PHASE}/validation/privacy-correction-scan.json",
        f"docs/caelen-ash/{PHASE}/validation/privacy-correction-staged-review.json",
    }
    current_paths = {path.relative_to(ROOT).as_posix() for path in owner_files()}
    summary = load(FINAL / "final-summary.json")
    summary["owner_files"] = len(current_paths | exclusions)
    write_json(FINAL / "final-summary.json", summary)
    write_json(VALIDATION / "privacy-correction-scan.json", privacy_scan(owner_files()))

    delta_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256_normalized_lf": normalized_sha(path),
            "bytes_normalized_lf": len(normalized_bytes(path)),
        }
        for path in delta_files()
        if path.relative_to(ROOT).as_posix() not in exclusions
    ]
    write_json(
        VALIDATION / "privacy-correction-delta-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v2",
            "phase": PHASE,
            "lifecycle": "privacy_definition_correction_delta",
            "retained_second_final": SECOND_FINAL,
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
        VALIDATION / "privacy-correction-owner-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v2",
            "phase": PHASE,
            "lifecycle": "privacy_corrected_owner_packet",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusions": sorted(exclusions),
            "owner_file_count": len(owner_entries) + len(exclusions),
            "file_ceiling": 2000,
        },
    )
    write_json(
        VALIDATION / "privacy-correction-staged-review.json",
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
    manifest = load(VALIDATION / "privacy-correction-delta-manifest.json")
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
    protected = [
        f"docs/caelen-ash/{PHASE}/x1/", f"docs/caelen-ash/{PHASE}/x2/",
        f"docs/caelen-ash/{PHASE}/method-flow/", f"docs/caelen-ash/{PHASE}/workflow-refinement/",
        f"docs/caelen-ash/{PHASE}/reflection-remaster/", f"docs/caelen-ash/{PHASE}/tooling/",
    ]
    inherited = [rel for rel in staged if any(rel.startswith(prefix) for prefix in protected)]
    missing = sorted(expected_all - set(staged))
    out_of_scope = sorted(set(staged) - expected_all)
    diff = git("diff", "--cached", "--check", check=False)
    passed = not mismatches and not missing and not out_of_scope and not inherited and diff.returncode == 0
    write_json(
        VALIDATION / "privacy-correction-staged-review.json",
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

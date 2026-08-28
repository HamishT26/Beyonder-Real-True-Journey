#!/usr/bin/env python3
"""Build the additive Liora v674-v5 committed-domain evidence correction."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OWNER = "Liora Venn"
PHASE = "v674-v5"
SOURCE = "8979c6884c75232046a85fd18ae2d15af33f4a0e"
X1 = "8f1db387ab28e3b53e3aaadef33a044f2e023386"
ORIGINAL_EVIDENCE = "06af8881c44826cd3161d80f0a4359912ff1ce68"
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "liora-venn" / PHASE
X2_ROOT = PHASE_ROOT / "x2"
CORRECTION_ROOT = X2_ROOT / "correction"
SCRIPT_REL = "scripts/build_ghc_family_liora_venn_v674_v5_evidence_correction.py"
TEST_REL = "tests/test_ghc_family_liora_venn_v674_v5_evidence_correction.py"
MANIFEST_REL = f"docs/liora-venn/{PHASE}/x2/validation/evidence-correction-owner-manifest.json"
STAGED_REVIEW_REL = f"docs/liora-venn/{PHASE}/x2/validation/evidence-correction-staged-review.json"

PRIVATE_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29}\b", re.I),
    "private_absolute_path": re.compile(r"(?:[A-Za-z]:\\\\|/Users/|/home/)", re.I),
    "credential_or_secret_assignment": re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s\"']+"),
    "private_callable_identifier": re.compile(r"(?i)(?:mcp__|clientThreadId|source_thread_id)"),
    "conversation_or_session_stream": re.compile(r"(?i)(?:raw transcript|session stream|chat export)"),
}

FAILURES = [
    {
        "id": "LV6745-EV-N001",
        "failed_witness": "The first committed-domain manifest probe embedded unnecessary temporary-file cleanup and was rejected by host policy before any process, file, Git, or remote action.",
        "initial_credit": 0,
        "recovery": "Used a scalar no-temp Python Git-blob verifier with no filesystem mutation.",
        "recurrence_guard": "Committed-domain verification reads Git blobs directly and never creates a temporary file merely to hash them.",
    },
    {
        "id": "LV6745-EV-N002",
        "failed_witness": "The pushed evidence manifest recorded checkout CRLF bytes for twenty skill-creator YAML companions, while their committed Git blobs were normalized to LF; all twenty entries failed exact hash and byte parity.",
        "initial_credit": 0,
        "recovery": "Retained the original evidence commit and manifest, then built a separate full-owner correction manifest from normalized index blobs before an additive evidence-correction commit.",
        "recurrence_guard": "Every commit-bound manifest hashes index or Git-tree blobs in the named normalized-LF domain; checkout-byte receipts remain a separate domain.",
    },
    {
        "id": "LV6745-EV-N003",
        "failed_witness": "The first exact correction staging command staged eight in-sparse documents but refused the new correction builder and test because those exact owner paths were outside the inherited sparse specification.",
        "initial_credit": 0,
        "recovery": "Used git add --sparse for only the two named owner paths, then restaged the rebuilt correction documents and verified the exact index allowlist.",
        "recurrence_guard": "When an additive owner path is intentionally outside inherited sparse patterns, use --sparse with an exact path and verify the staged allowlist immediately.",
    },
    {
        "id": "LV6745-EV-N004",
        "failed_witness": "The first full correction-test wrapper ended after two progress markers with no attributable summary or exit status; no surviving test process could establish completion.",
        "initial_credit": 0,
        "recovery": "Ran the unchanged eight-test module in a resumable terminal session and waited for its explicit test count, verdict, and exit code.",
        "recurrence_guard": "Long manifest-parity selections use a resumable session; partial progress output never earns completion credit.",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git(*args: str, text: bool = True, check: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
        encoding="utf-8" if text else None,
    )
    return proc.stdout


def blob(ref: str, path: str) -> bytes:
    value = git("show", f"{ref}:{path}", text=False)
    assert isinstance(value, bytes)
    return value


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_json(ref: str, path: str) -> Any:
    return json.loads(blob(ref, path))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def assert_original_evidence_head() -> None:
    head = str(git("rev-parse", "HEAD")).strip()
    if head != ORIGINAL_EVIDENCE:
        raise RuntimeError(f"Correction requires retained evidence head {ORIGINAL_EVIDENCE}; found {head}")
    if str(git("rev-parse", "HEAD^")).strip() != X1:
        raise RuntimeError("Retained evidence is not the direct child of immutable x1")


def diagnose_original_manifest() -> dict[str, Any]:
    path = f"docs/liora-venn/{PHASE}/x2/validation/evidence-owner-manifest.json"
    manifest_raw = blob(ORIGINAL_EVIDENCE, path)
    manifest = json.loads(manifest_raw)
    mismatches: list[dict[str, Any]] = []
    for entry in manifest["entries"]:
        raw = blob(ORIGINAL_EVIDENCE, entry["path"])
        actual = hashlib.sha256(raw).hexdigest()
        if actual != entry["sha256"] or len(raw) != entry["bytes"]:
            mismatches.append(
                {
                    "path": entry["path"],
                    "expected_sha256": entry["sha256"],
                    "actual_sha256": actual,
                    "expected_bytes": entry["bytes"],
                    "actual_bytes": len(raw),
                    "cause": "checkout_crlf_to_git_lf_normalization",
                }
            )
    return {
        "schema": "ghc-family-committed-domain-manifest-diagnostic-v1",
        "owner": OWNER,
        "phase": PHASE,
        "retained_evidence_head": ORIGINAL_EVIDENCE,
        "original_manifest_path": path,
        "original_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
        "entries_checked": len(manifest["entries"]),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "original_manifest_passed": not mismatches,
        "original_failure_retained": True,
    }


def build() -> dict[str, Any]:
    assert_original_evidence_head()
    diagnostic = diagnose_original_manifest()
    if diagnostic["mismatch_count"] != 20 or not all(row["path"].endswith("/agents/openai.yaml") for row in diagnostic["mismatches"]):
        raise RuntimeError("Committed-domain mismatch set differs from the preregistered correction scope")

    original_methods = load_json(X2_ROOT / "method-flow" / "ledger.json")
    original_negatives = load_json(X2_ROOT / "retained-negative-register.json")
    original_gates = load_json(X2_ROOT / "gate-register.json")
    original_truth = load_json(X2_ROOT / "phase-truth.json")

    correction_methods = [
        {
            "method_id": f"LV6745-EVIDENCE-RECOVERY-{index:03d}",
            "failure_id": failure["id"],
            "kind": "committed_domain_manifest_recovery",
            "status": "preferred",
            "failed_witness_retained": True,
        }
        for index, failure in enumerate(FAILURES, start=1)
    ]
    corrected_methods = {
        **original_methods,
        "lifecycle": "additive_evidence_correction_precommit",
        "phase_method_additions": original_methods["phase_method_additions"] + len(correction_methods),
        "effective_methods": original_methods["effective_methods"] + len(correction_methods),
        "methods": original_methods["methods"] + correction_methods,
        "correction_method_additions": len(correction_methods),
        "recoveries_rewrite_failures": False,
    }
    corrected_negatives = {
        **original_negatives,
        "lifecycle": "additive_evidence_correction_precommit",
        "evidence_correction_operational_failures": len(FAILURES),
        "evidence_correction_failure_ids": [row["id"] for row in FAILURES],
        "effective_negatives": original_negatives["effective_negatives"] + len(FAILURES),
        "phase_failed_witness_additions": original_negatives["phase_failed_witness_additions"] + len(FAILURES),
        "effective_failed_witnesses": original_negatives["effective_failed_witnesses"] + len(FAILURES),
        "phase_bounded_passing_additions": original_negatives["phase_bounded_passing_additions"] + len(FAILURES),
        "effective_bounded_passing_witnesses": original_negatives["effective_bounded_passing_witnesses"] + len(FAILURES),
        "no_failure_erased_or_promoted": True,
    }
    corrected_truth = {
        **original_truth,
        "lifecycle": "additive_evidence_correction_precommit",
        "retained_first_evidence_head": ORIGINAL_EVIDENCE,
        "corrected_evidence_binding": "external_postcommit_binding_required",
        "effective_negatives": corrected_negatives["effective_negatives"],
        "effective_methods": corrected_methods["effective_methods"],
        "effective_failed_witnesses": corrected_negatives["effective_failed_witnesses"],
        "effective_bounded_passing_witnesses": corrected_negatives["effective_bounded_passing_witnesses"],
        "effective_open_gaps": original_gates["effective_open_gaps"],
        "effective_exact_gates": original_gates["effective_exact_gates"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }

    write_json(CORRECTION_ROOT / "original-manifest-diagnostic.json", diagnostic)
    write_json(CORRECTION_ROOT / "operational-failure-ledger.json", {
        "schema": "ghc-family-operational-failure-ledger-v1",
        "owner": OWNER,
        "phase": PHASE,
        "failed_witness_count": len(FAILURES),
        "failed_witnesses": FAILURES,
        "recoveries_do_not_rewrite_failures": True,
    })
    write_json(CORRECTION_ROOT / "corrected-method-flow.json", corrected_methods)
    write_json(CORRECTION_ROOT / "corrected-retained-negative-register.json", corrected_negatives)
    write_json(CORRECTION_ROOT / "corrected-gate-register.json", {**original_gates, "lifecycle": "additive_evidence_correction_precommit"})
    write_json(CORRECTION_ROOT / "corrected-phase-truth.json", corrected_truth)
    write_json(CORRECTION_ROOT / "correction-receipt.json", {
        "schema": "ghc-family-evidence-correction-receipt-v1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "retained_first_evidence": ORIGINAL_EVIDENCE,
        "corrected_evidence_binding": "external_postcommit_binding_required",
        "original_manifest_success_credit": 0,
        "original_manifest_mismatches": diagnostic["mismatch_count"],
        "correction_failures_retained": len(FAILURES),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "prepared_utc": utc_now(),
    })
    write_text(CORRECTION_ROOT / "correction-overview.md", f"""# Liora Venn v674-v5 evidence manifest-domain correction

The pushed first evidence commit `{ORIGINAL_EVIDENCE}` remains immutable and retained. Its owner manifest has zero exact committed-domain credit because twenty skill-creator YAML companions were hashed as checkout CRLF bytes before Git normalized them to LF blobs. The evidence content itself is unchanged; the defect is the manifest's declared byte domain and parity.

This additive correction retains four named zero-credit operational failures, adds separate bounded recovery methods, and prepares one normalized-index full-owner manifest. It does not rewrite the failed manifest, replay x2 execution, add a proposal outcome, contact a successor, or promote same-owner evidence. Effective truth is {corrected_negatives['effective_negatives']} negatives, {corrected_methods['effective_methods']} methods, {corrected_negatives['effective_failed_witnesses']} failed witnesses, {corrected_negatives['effective_bounded_passing_witnesses']} bounded passing witnesses, {original_gates['effective_open_gaps']} open gaps, {original_gates['effective_exact_gates']} exact gates, and `NOT_READY_FOR_STAGE_20`.
""")
    return {"status": "built_additive_evidence_correction", "mismatches_retained": diagnostic["mismatch_count"], "failures_retained": len(FAILURES)}


def index_blob(path: str) -> bytes:
    value = git("show", f":{path}", text=False)
    assert isinstance(value, bytes)
    return value


def owner_index_paths() -> list[str]:
    tracked = str(git("ls-files")).splitlines()
    paths = []
    for path in tracked:
        if path.startswith(f"docs/liora-venn/{PHASE}/"):
            paths.append(path)
        elif path.endswith(".py") and "liora" in Path(path).name and "v674_v5" in Path(path).name:
            paths.append(path)
    return sorted(set(paths) - {MANIFEST_REL, STAGED_REVIEW_REL})


def index_entry(path: str) -> dict[str, Any]:
    raw = index_blob(path)
    return {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "line_count": raw.count(b"\n")}


def build_index_seal() -> dict[str, Any]:
    assert_original_evidence_head()
    paths = owner_index_paths()
    if not any(path.endswith("/agents/openai.yaml") for path in paths):
        raise RuntimeError("Normalized YAML companions are absent from the index-domain owner set")
    manifest = {
        "schema": "ghc-family-evidence-correction-owner-manifest-v1",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "additive_evidence_correction_precommit",
        "domain": "git_index_normalized_blob_bytes_before_correction_commit",
        "retained_failed_manifest": f"docs/liora-venn/{PHASE}/x2/validation/evidence-owner-manifest.json",
        "entries": [index_entry(path) for path in paths],
        "declared_self_exclusions": [MANIFEST_REL, STAGED_REVIEW_REL],
    }
    write_json(REPO / MANIFEST_REL, manifest)
    return {"status": "built_normalized_index_owner_manifest", "entries": len(paths), "exclusions": 2}


def build_staged_review() -> dict[str, Any]:
    staged = sorted(path for path in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if path and path != STAGED_REVIEW_REL)
    allowed = (
        f"docs/liora-venn/{PHASE}/x2/correction/",
        MANIFEST_REL,
        SCRIPT_REL,
        TEST_REL,
    )
    unexpected = [path for path in staged if not path.startswith(allowed)]
    definition_paths = {SCRIPT_REL, TEST_REL}
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    for path in staged:
        raw = index_blob(path)
        entries.append({"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
        if Path(path).suffix.lower() in {".json", ".md", ".py", ".txt", ".html", ".yaml", ".yml"}:
            text = raw.decode("utf-8")
            for kind, pattern in PRIVATE_PATTERNS.items():
                if pattern.search(text):
                    candidates.append({"path": path, "class": kind, "status": "scanner_definition_only" if path in definition_paths else "candidate_requires_adjudication"})
    unresolved = [row for row in candidates if row["status"] != "scanner_definition_only"]
    review = {
        "schema": "ghc-family-exact-staged-review-v1",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "additive_evidence_correction",
        "entries": entries,
        "staged_entry_count": len(entries),
        "declared_self_exclusions": [STAGED_REVIEW_REL],
        "unexpected_paths": unexpected,
        "privacy_candidates": candidates,
        "unresolved_privacy_candidates": unresolved,
        "confirmed_privacy_hits": [],
        "status": "passed" if not unexpected and not unresolved else "review_required",
    }
    write_json(REPO / STAGED_REVIEW_REL, review)
    return {"status": review["status"], "entries": len(entries), "candidates": len(candidates), "unresolved": len(unresolved)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("build", "index-seal", "staged-review"), nargs="?", default="build")
    args = parser.parse_args()
    if args.mode == "build":
        result = build()
    elif args.mode == "index-seal":
        result = build_index_seal()
    else:
        result = build_staged_review()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

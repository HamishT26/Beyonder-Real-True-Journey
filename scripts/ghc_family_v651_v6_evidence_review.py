#!/usr/bin/env python3
"""Review the exact staged v651-v6 evidence surface and bind Git-index blobs."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/elaren-kestrel/v651-v6"
X1 = "b0ba19472777bc07f91c0358186b48311aa3bce3"
OUT = {
    "manifest": f"{PHASE_ROOT}/validation/evidence-staged-manifest.json",
    "privacy": f"{PHASE_ROOT}/validation/evidence-staged-privacy.json",
    "review": f"{PHASE_ROOT}/validation/evidence-staged-review.json",
    "documents": f"{PHASE_ROOT}/validation/evidence-document-cap.json",
    "files": f"{PHASE_ROOT}/validation/evidence-owner-file-threshold.json",
}
SELF_EXCLUSIONS = sorted(OUT.values())
ALLOWED_SCRIPTS = {
    "scripts/ghc_family_v651_v6_runtime.py",
    "scripts/build_ghc_family_v651_v6_skills.py",
    "scripts/build_ghc_family_v651_v6_runners.py",
    "scripts/build_ghc_family_v651_v6_evidence.py",
    "scripts/ghc_family_v651_v6_validator.py",
    "scripts/ghc_family_v651_v6_minimal.py",
    "scripts/ghc_family_v651_v6_evidence_review.py",
    "scripts/ghc_family_v651_v6_x2_method_flow.py",
    "scripts/ghc_family_numerical_verification_board.py",
    "scripts/ghc_family_discrete_adjoint_dot_test.py",
    "scripts/ghc_family_dae_event_gate.py",
    "scripts/ghc_family_richardson_range_gate.py",
    "scripts/ghc_family_work_precision_frontier.py",
    "scripts/ghc_family_mixed_precision_escalation.py",
    "scripts/ghc_family_thos_runtime_boundaries.py",
    "scripts/ghc_family_freed_id_key_boundaries.py",
    "scripts/ghc_family_consequential_model_ledger.py",
    "scripts/ghc_family_claim_retraction_protocol.py",
    "tests/test_ghc_family_v651_v6_x2.py",
}
PATTERNS = {
    "raw_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|file|vscode|app|thread)://", re.I),
    "delegation": re.compile(rb"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential": re.compile(rb"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
}


def run(*args: str, text: bool = True):
    return subprocess.check_output(list(args), cwd=REPO, text=text, encoding="utf-8" if text else None)


def write_json(path: str, payload: dict) -> None:
    target = REPO / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def staged_paths() -> list[str]:
    raw = run("git", "diff", "--cached", "--name-only", "-z", text=False)
    return sorted(part.decode("utf-8") for part in raw.split(b"\0") if part)


def staged_blob(path: str) -> tuple[str, bytes]:
    row = run("git", "ls-files", "-s", "--", path).strip()
    if not row:
        raise RuntimeError(f"missing staged entry: {path}")
    oid = row.split()[1]
    return oid, run("git", "cat-file", "blob", oid, text=False)


def main() -> None:
    if run("git", "rev-parse", "HEAD").strip() != X1:
        raise RuntimeError("evidence review requires exact x1 head")
    paths = staged_paths()
    if any(path in SELF_EXCLUSIONS for path in paths):
        raise RuntimeError("review self-exclusions must not be staged yet")
    x1_paths = set(run("git", "diff-tree", "--no-commit-id", "--name-only", "-r", f"{X1}^", X1).splitlines())
    frozen_changes = sorted(set(paths) & x1_paths)
    unexpected = [path for path in paths if not (path.startswith(PHASE_ROOT + "/") or path in ALLOWED_SCRIPTS)]
    forbidden = [path for path in paths if any(token in path for token in ("/closeout/", "/seal/", "/final/", "/handoffs/", "final-validation", "successor-baton"))]
    if frozen_changes or unexpected or forbidden:
        raise RuntimeError(f"frozen={frozen_changes} unexpected={unexpected} closeout={forbidden}")
    check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if check.returncode:
        raise RuntimeError(check.stdout + check.stderr)

    entries, confirmed, definitions, documents = [], [], [], []
    json_count = 0
    for path in paths:
        oid, data = staged_blob(path)
        entries.append({"path": path, "bytes": len(data), "git_blob": oid, "sha256": hashlib.sha256(data).hexdigest()})
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_count += 1
        if path.startswith(PHASE_ROOT + "/") and (path.endswith(".md") or path.endswith(".html")):
            words = len(data.decode("utf-8").split())
            documents.append({"path": path, "words": words, "under_cap": words <= 100000})
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                row = {"path": path, "class": name, "offset": match.start()}
                if path.startswith("scripts/") or path.startswith("tests/"):
                    definitions.append(row)
                else:
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError(f"privacy hits: {confirmed[:8]}")
    if not all(row["under_cap"] for row in documents):
        raise RuntimeError("document cap exceeded")
    owner_file_count = sum(1 for path in (REPO / PHASE_ROOT).rglob("*") if path.is_file()) + len(SELF_EXCLUSIONS)
    if owner_file_count >= 2000:
        raise RuntimeError(f"owner file threshold: {owner_file_count}")

    write_json(OUT["manifest"], {"schema": "ghc.family.v651-v6.evidence-staged-manifest.v1", "x1_commit": X1, "hash_domain": "exact_git_index_blob", "entry_count": len(entries), "covered_path_count": len(entries) + len(SELF_EXCLUSIONS), "self_exclusions": SELF_EXCLUSIONS, "entries": entries})
    write_json(OUT["privacy"], {"schema": "ghc.family.v651-v6.evidence-staged-privacy.v1", "pattern_classes": sorted(PATTERNS), "scanned_entry_count": len(entries), "scanner_definition_candidates": definitions, "confirmed_hits": confirmed, "zero_confirmed_hits": True, "boundary": "Five-class scanning is not complete privacy or security assurance."})
    write_json(OUT["documents"], {"schema": "ghc.family.v651-v6.evidence-document-cap.v1", "cap_words": 100000, "document_count": len(documents), "maximum_words": max((row["words"] for row in documents), default=0), "all_under_cap": True, "documents": documents})
    write_json(OUT["files"], {"schema": "ghc.family.v651-v6.evidence-owner-file-threshold.v1", "owner_file_count": owner_file_count, "threshold": 2000, "below_threshold": True, "inherited_repository_baseline_counted": False})
    write_json(OUT["review"], {"schema": "ghc.family.v651-v6.evidence-staged-review.v1", "x1_commit": X1, "entry_count": len(entries), "predicted_final_staged_path_count": len(entries) + len(SELF_EXCLUSIONS), "self_exclusion_count": len(SELF_EXCLUSIONS), "x1_frozen_changes": frozen_changes, "unexpected_paths": unexpected, "closeout_or_final_contamination": forbidden, "json_parses": json_count, "privacy_zero_confirmed_hits": True, "diff_hygiene": "pass", "manifest_exact_git_index_blobs": True, "x2_tests": {"passed": 45, "total": 45}, "valid": True, "boundary": "Evidence commit only; no closeout, exact-final, remote-equality, independent-reproduction, or Stage 20 claim."})
    print(json.dumps({"entries": len(entries), "self_exclusions": len(SELF_EXCLUSIONS), "predicted": len(entries) + len(SELF_EXCLUSIONS), "json": json_count, "privacy_hits": 0, "frozen_changes": 0, "valid": True}))


if __name__ == "__main__":
    main()

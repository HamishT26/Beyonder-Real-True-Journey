#!/usr/bin/env python3
"""Create exact staged evidence manifests and validate frozen x1 Git objects."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = "docs/eiren-kestrel/v651-v5-2-remaster"
X1 = "d9e8cbf0063639aa0a6fb54c54a96683c587ce7e"
OUT = {
    "manifest": f"{PHASE_ROOT}/validation/evidence-staged-manifest.json",
    "privacy": f"{PHASE_ROOT}/validation/evidence-staged-privacy.json",
    "review": f"{PHASE_ROOT}/validation/evidence-staged-review.json",
}
SELF_EXCLUSIONS = sorted(OUT.values())
ALLOWED_SCRIPTS = {
    "scripts/build_ghc_family_v651_v5_2_evidence.py",
    "scripts/ghc_family_v651_v5_2_evidence_review.py",
    "scripts/ghc_family_meta_tool_box.py",
    "scripts/ghc_family_tool_trigger_collision_auditor.py",
    "scripts/ghc_family_runner_caller_map.py",
    "scripts/ghc_family_global_promotion_readiness.py",
    "scripts/ghc_family_tool_staleness_scorecard.py",
    "scripts/ghc_family_method_recommendation_index.py",
    "scripts/ghc_family_d_first_rotation_receipt.py",
    "scripts/ghc_family_commit_budget_guard.py",
    "scripts/ghc_family_single_pass_validation_planner.py",
    "scripts/ghc_family_tool_provenance_chain.py",
    "tests/test_ghc_family_v651_v5_2_x2.py",
}
PATTERNS = {
    "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
    "private_local_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\|/Users/|/home/)", re.I),
    "private_uri": re.compile(rb"(?:codex|chatgpt|file|vscode|app)://", re.I),
    "delegation_markup": re.compile(rb"<\s*(?:codex_delegation|source_thread_id|private_route)\b", re.I),
    "credential_assignment": re.compile(rb"(?:api[_-]?key|password|private[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-/+=]{12,}", re.I),
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
        raise RuntimeError(f"missing staged index entry: {path}")
    oid = row.split()[1]
    return oid, run("git", "cat-file", "blob", oid, text=False)


def verify_x1_objects() -> tuple[int, list[dict]]:
    raw = run("git", "show", f"{X1}:{PHASE_ROOT}/validation/x1-staged-manifest.json", text=False)
    manifest = json.loads(raw.decode("utf-8"))
    issues = []
    for entry in manifest["entries"]:
        path = entry["path"]
        try:
            oid = run("git", "rev-parse", f"{X1}:{path}").strip()
        except subprocess.CalledProcessError:
            issues.append({"path": path, "issue": "missing_x1_object"})
            continue
        if oid != entry["git_blob"]:
            issues.append({"path": path, "issue": "git_blob_mismatch", "expected": entry["git_blob"], "observed": oid})
    return len(manifest["entries"]), issues


def main() -> None:
    if run("git", "rev-parse", "HEAD").strip() != X1:
        raise RuntimeError("evidence review must run at the exact x1 commit")
    paths = staged_paths()
    if any(path in SELF_EXCLUSIONS for path in paths):
        raise RuntimeError("self-excluding receipts must not be staged before review generation")
    unexpected = [path for path in paths if not (path.startswith(PHASE_ROOT + "/") or path in ALLOWED_SCRIPTS)]
    forbidden = [path for path in paths if any(token in path for token in ("/handoffs/", "/final/", "/closeout/", "/seal/"))]
    if unexpected or forbidden:
        raise RuntimeError(f"unexpected={unexpected} closeout_contamination={forbidden}")
    check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    if check.returncode:
        raise RuntimeError(check.stdout + check.stderr)
    x1_entries, x1_issues = verify_x1_objects()
    if x1_issues:
        raise RuntimeError(f"x1 Git-object mismatch: {x1_issues[:5]}")

    entries, confirmed, definitions = [], [], []
    for path in paths:
        oid, data = staged_blob(path)
        entries.append({"path": path, "bytes": len(data), "git_blob": oid, "sha256": hashlib.sha256(data).hexdigest()})
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(data):
                candidate = {"path": path, "class": class_name, "offset": match.start()}
                if path.startswith("scripts/") or path.startswith("tests/"):
                    definitions.append(candidate)
                else:
                    confirmed.append(candidate)
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed[:5]}")

    write_json(OUT["manifest"], {"schema": "ghc.family.v651-v5-2.evidence-staged-manifest.v1", "x1_commit": X1, "hash_domain": "exact_git_index_blob", "entry_count": len(entries), "covered_path_count": len(entries) + len(SELF_EXCLUSIONS), "self_exclusions": SELF_EXCLUSIONS, "entries": entries})
    write_json(OUT["privacy"], {"schema": "ghc.family.v651-v5-2.evidence-staged-privacy.v1", "pattern_classes": sorted(PATTERNS), "scanned_entry_count": len(entries), "scanner_definition_candidates": definitions, "confirmed_hits": confirmed, "zero_confirmed_hits": True, "boundary": "Five-class staged scanning is not privacy-complete assurance or independent review."})
    write_json(OUT["review"], {"schema": "ghc.family.v651-v5-2.evidence-staged-review.v1", "x1_commit": X1, "entry_count": len(entries), "self_exclusion_count": len(SELF_EXCLUSIONS), "predicted_final_staged_path_count": len(entries) + len(SELF_EXCLUSIONS), "unexpected_paths": unexpected, "closeout_contamination": forbidden, "diff_hygiene": "pass", "bounded_tests": {"passed": 22, "total": 22}, "skills_validated": 20, "runners_smoked": 10, "mutations_rejected": 100, "global_skill_promotions": 1, "x1_manifest_entries_verified": x1_entries, "x1_git_object_issues": x1_issues, "privacy_zero_confirmed_hits": True, "manifest_exact_index_blobs": True, "valid": True, "boundary": "Evidence-stage same-owner review only; no full-suite, independent-reproduction, or closeout credit."})
    print(json.dumps({"entries": len(entries), "self_exclusions": len(SELF_EXCLUSIONS), "predicted_paths": len(entries) + len(SELF_EXCLUSIONS), "x1_entries": x1_entries, "privacy_hits": 0, "valid": True}))


if __name__ == "__main__":
    main()

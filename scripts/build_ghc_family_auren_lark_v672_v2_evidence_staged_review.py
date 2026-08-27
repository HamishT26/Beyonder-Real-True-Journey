#!/usr/bin/env python3
"""Build the exact Auren v672-v2 evidence staged-blob review."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

X1 = "821a40be02af8db39524dc862aeaadf32e1543c3"
PHASE_PREFIX = "docs/auren-lark/v672-v2/x2/"
RECEIPT = "docs/auren-lark/v672-v2/validation/evidence-staged-review.json"
RUNNERS = {
    "scripts/ghc_family_auren_v672_v2_incident_chronology_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_source_status_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_correction_log_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_uncertainty_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_authority_boundary_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_privacy_minimization_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_accessibility_handoff_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_evidence_chain_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_readback_guard.py",
    "scripts/ghc_family_auren_v672_v2_incident_packet_guard.py",
}
ALLOWED_EXACT = RUNNERS | {
    "scripts/build_ghc_family_auren_lark_v672_v2_x2.py",
    "scripts/build_ghc_family_auren_lark_v672_v2_evidence_staged_review.py",
    "scripts/validate_ghc_family_auren_lark_v672_v2_x2.py",
    "tests/test_ghc_family_auren_lark_v672_v2_x2.py",
}
FROZEN_X1_EXACT = {
    "scripts/build_ghc_family_auren_lark_v672_v2_x1.py",
    "scripts/build_ghc_family_auren_lark_v672_v2_staged_review.py",
    "tests/test_ghc_family_auren_lark_v672_v2_x1.py",
}


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def security_findings(path: str, data: bytes) -> list[dict[str, object]]:
    if not path.endswith(".py"):
        return []
    tree = ast.parse(data.decode("utf-8"), filename=path)
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
            findings.append({"path": path, "line": node.lineno, "kind": node.func.id})
        for keyword in node.keywords:
            if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                findings.append({"path": path, "line": node.lineno, "kind": "shell_true"})
    return findings


def main() -> None:
    root = Path(
        git(Path.cwd(), "rev-parse", "--show-toplevel").decode("utf-8").strip()
    )
    staged = [
        row
        for row in git(root, "diff", "--cached", "--name-only", "--diff-filter=ACMR")
        .decode("utf-8")
        .splitlines()
        if row
    ]
    deletions = git(root, "diff", "--cached", "--name-only", "--diff-filter=D").decode(
        "utf-8"
    ).splitlines()
    out_of_scope = [
        path
        for path in staged
        if not (path.startswith(PHASE_PREFIX) or path in ALLOWED_EXACT)
    ]
    frozen_x1_mutations = [
        path
        for path in git(root, "diff", "--name-only", X1)
        .decode("utf-8")
        .splitlines()
        if path.startswith("docs/auren-lark/v672-v2/x1/") or path in FROZEN_X1_EXACT
    ]
    patterns = {
        "aws_access_key": re.compile(rb"A" + rb"KIA[0-9A-Z]{16}"),
        "github_token": re.compile(rb"gh" + rb"p_[A-Za-z0-9]{20,}"),
        "private_key": re.compile(rb"BEGIN [A-Z ]*PRIVATE" + rb" KEY"),
        "raw_task_identifier": re.compile(rb"\b019[a-f0-9]{5}-[a-f0-9-]{20,}\b"),
        "credential_assignment": re.compile(rb"(?i)(password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
    }
    rows = []
    privacy_candidates = []
    strict_json_parses = 0
    working_index_mismatches = []
    security = []
    for path in staged:
        blob = git(root, "show", f":{path}")
        disk = (root / path).read_bytes()
        if disk != blob:
            working_index_mismatches.append(path)
        if path.endswith(".json"):
            json.loads(blob.decode("utf-8"))
            strict_json_parses += 1
        for name, pattern in patterns.items():
            if pattern.search(blob):
                privacy_candidates.append({"path": path, "privacy_class": name})
        security.extend(security_findings(path, blob))
        rows.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})

    manifest_path = "docs/auren-lark/v672-v2/x2/owner-manifest.json"
    manifest = json.loads(git(root, "show", f":{manifest_path}").decode("utf-8"))
    row_by_path = {row["path"]: row for row in rows}
    manifest_mismatches = []
    for expected in manifest["entries"]:
        actual = row_by_path.get(expected["path"])
        if actual is None:
            manifest_mismatches.append({"path": expected["path"], "reason": "not_staged"})
        elif any(actual[key] != expected[key] for key in ("bytes", "sha256")):
            manifest_mismatches.append({"path": expected["path"], "reason": "content_mismatch"})

    valid = not (
        deletions
        or out_of_scope
        or frozen_x1_mutations
        or privacy_candidates
        or working_index_mismatches
        or security
        or manifest_mismatches
    )
    payload = {
        "schema": "ghc.family.evidence-staged-review.v3",
        "owner": "Auren Lark",
        "phase": "v672-v2",
        "lifecycle": "X2_EVIDENCE_CANDIDATE",
        "staged_before_self": staged,
        "staged_count_before_self": len(staged),
        "staged_count_with_self": len(staged) + 1,
        "blob_rows": rows,
        "strict_json_parses": strict_json_parses,
        "deletions": deletions,
        "out_of_scope": out_of_scope,
        "frozen_x1_mutations": frozen_x1_mutations,
        "confirmed_privacy_candidates": privacy_candidates,
        "working_index_mismatches": working_index_mismatches,
        "bounded_changed_python_security_findings": security,
        "owner_manifest_entries": manifest["entry_count"],
        "owner_manifest_mismatches": manifest_mismatches,
        "valid": valid,
    }
    receipt_path = root / RECEIPT
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"receipt": RECEIPT, "valid": valid, "rows": len(rows)}, sort_keys=True))
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

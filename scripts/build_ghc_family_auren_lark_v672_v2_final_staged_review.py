#!/usr/bin/env python3
"""Build the exact final staged-blob review for Auren Lark v672-v2."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

EVIDENCE = "e735ac99202e9ad69252ed39ce9eb41d684bf671"
ALLOWED_PREFIXES = (
    "docs/auren-lark/v672-v2/closeout/",
    "docs/auren-lark/v672-v2/handoffs/",
)
RECEIPT = "docs/auren-lark/v672-v2/validation/final-staged-review.json"
ALLOWED_EXACT = {
    "scripts/build_ghc_family_auren_lark_v672_v2_final.py",
    "scripts/build_ghc_family_auren_lark_v672_v2_final_staged_review.py",
    "scripts/validate_ghc_family_auren_lark_v672_v2_final.py",
    "tests/test_ghc_family_auren_lark_v672_v2_final.py",
}
FROZEN_PREFIXES = (
    "docs/auren-lark/v672-v2/x1/",
    "docs/auren-lark/v672-v2/x2/",
)
FROZEN_EXACT = {
    "scripts/build_ghc_family_auren_lark_v672_v2_x1.py",
    "scripts/build_ghc_family_auren_lark_v672_v2_staged_review.py",
    "scripts/build_ghc_family_auren_lark_v672_v2_x2.py",
    "scripts/build_ghc_family_auren_lark_v672_v2_evidence_staged_review.py",
    "scripts/validate_ghc_family_auren_lark_v672_v2_x2.py",
    "tests/test_ghc_family_auren_lark_v672_v2_x1.py",
    "tests/test_ghc_family_auren_lark_v672_v2_x2.py",
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
        if not (path.startswith(ALLOWED_PREFIXES) or path in ALLOWED_EXACT)
    ]
    frozen_mutations = [
        path
        for path in git(root, "diff", "--name-only", EVIDENCE)
        .decode("utf-8")
        .splitlines()
        if path.startswith(FROZEN_PREFIXES) or path in FROZEN_EXACT
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
        if blob != disk:
            working_index_mismatches.append(path)
        if path.endswith(".json"):
            json.loads(blob.decode("utf-8"))
            strict_json_parses += 1
        for name, pattern in patterns.items():
            if pattern.search(blob):
                privacy_candidates.append({"path": path, "privacy_class": name})
        security.extend(security_findings(path, blob))
        rows.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})

    evidence_manifest = json.loads(
        git(
            root,
            "show",
            ":docs/auren-lark/v672-v2/closeout/immutable-evidence-manifest.json",
        ).decode("utf-8")
    )
    evidence_mismatches = []
    for expected in evidence_manifest["entries"]:
        blob_id = git(root, "rev-parse", f"{EVIDENCE}:{expected['path']}").decode("ascii").strip()
        blob = git(root, "cat-file", "blob", blob_id)
        actual = {
            "git_blob": blob_id,
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
        }
        if any(actual[key] != expected[key] for key in actual):
            evidence_mismatches.append(expected["path"])

    closeout_manifest = json.loads(
        git(root, "show", ":docs/auren-lark/v672-v2/closeout/owner-manifest.json").decode(
            "utf-8"
        )
    )
    row_by_path = {row["path"]: row for row in rows}
    closeout_mismatches = []
    for expected in closeout_manifest["entries"]:
        actual = row_by_path.get(expected["path"])
        if actual is None:
            closeout_mismatches.append({"path": expected["path"], "reason": "not_staged"})
        elif any(actual[key] != expected[key] for key in ("bytes", "sha256")):
            closeout_mismatches.append({"path": expected["path"], "reason": "content_mismatch"})

    integrity = json.loads(
        git(root, "show", ":docs/auren-lark/v672-v2/closeout/handoff-integrity.json").decode(
            "utf-8"
        )
    )
    baton_blob = git(root, "show", f":{integrity['path']}")
    baton_text = baton_blob.decode("utf-8")
    baton_words = len(re.findall(r"\S+", baton_text))
    baton_valid = (
        hashlib.sha256(baton_blob).hexdigest() == integrity["sha256"]
        and baton_words == integrity["words"]
        and integrity["minimum_words"] <= baton_words <= integrity["maximum_words"]
    )
    valid = not (
        deletions
        or out_of_scope
        or frozen_mutations
        or privacy_candidates
        or working_index_mismatches
        or security
        or evidence_mismatches
        or closeout_mismatches
    ) and baton_valid
    payload = {
        "schema": "ghc.family.final-staged-review.v4",
        "owner": "Auren Lark",
        "phase": "v672-v2",
        "lifecycle": "FINAL_CLOSEOUT_CANDIDATE",
        "staged_before_self": staged,
        "staged_count_before_self": len(staged),
        "staged_count_with_self": len(staged) + 1,
        "blob_rows": rows,
        "strict_json_parses": strict_json_parses,
        "deletions": deletions,
        "out_of_scope": out_of_scope,
        "frozen_x1_x2_mutations": frozen_mutations,
        "confirmed_privacy_candidates": privacy_candidates,
        "working_index_mismatches": working_index_mismatches,
        "bounded_changed_python_security_findings": security,
        "immutable_evidence_entries": evidence_manifest["entry_count"],
        "immutable_evidence_mismatches": evidence_mismatches,
        "closeout_manifest_entries": closeout_manifest["entry_count"],
        "closeout_manifest_mismatches": closeout_mismatches,
        "baton_words": baton_words,
        "baton_sha256": hashlib.sha256(baton_blob).hexdigest(),
        "baton_valid": baton_valid,
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

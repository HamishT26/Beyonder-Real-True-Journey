#!/usr/bin/env python3
"""Review the exact staged v654-v7 evidence surface."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/elaren-kestrel/v654-v7/"
X1 = "773528bda8b863218ba4aaed0ce134fcd48abb97"
RECEIPT = PHASE_PREFIX + "validation/evidence-staged-review.json"
ALLOWED_SCRIPTS = {
    "scripts/ghc_family_v654_v7_core.py",
    "scripts/ghc_family_purpose_binding.py",
    "scripts/ghc_family_consent_freshness.py",
    "scripts/ghc_family_selective_disclosure_minimizer.py",
    "scripts/ghc_family_linkability_audit.py",
    "scripts/ghc_family_recovery_appeal_dual_control.py",
    "scripts/ghc_family_records_disposition_guard.py",
    "scripts/ghc_family_credential_lifecycle_accessibility.py",
    "scripts/ghc_family_offline_verifier_freshness.py",
    "scripts/ghc_family_capability_attenuation.py",
    "scripts/ghc_family_v654_v7_suite.py",
    "scripts/build_ghc_family_v654_v7_evidence.py",
    "scripts/ghc_family_v654_v7_validate.py",
    "scripts/ghc_family_v654_v7_evidence_staged_review.py",
}
ALLOWED_TESTS = {
    "tests/test_ghc_family_v654_v7_core.py",
    "tests/test_ghc_family_v654_v7_validation.py",
}
SCANNER_FILES = {
    "scripts/ghc_family_v654_v7_validate.py",
    "scripts/ghc_family_v654_v7_evidence_staged_review.py",
}


def git(*args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )
    return result.stdout.strip() if text else result.stdout


def blob(path: str) -> bytes:
    return git("show", f":{path}", text=False)


def main() -> None:
    paths = [
        path
        for path in str(git("diff", "--cached", "--name-only")).splitlines()
        if path
    ]
    statuses = [
        line.split("\t", 1)
        for line in str(git("diff", "--cached", "--name-status")).splitlines()
        if line
    ]
    x1_paths = set(
        str(git("ls-tree", "-r", "--name-only", X1)).splitlines()
    )
    out_of_scope = sorted(
        path
        for path in paths
        if not path.startswith(PHASE_PREFIX)
        and path not in ALLOWED_SCRIPTS
        and path not in ALLOWED_TESTS
    )
    frozen_changes = sorted(set(paths) & x1_paths)
    non_additions = [
        {"status": status, "path": path}
        for status, path in statuses
        if status != "A"
    ]
    forbidden_lifecycle = sorted(
        path
        for path in paths
        if any(
            segment in {"closeout", "seal", "final"}
            for segment in Path(path).parts
        )
    )
    reviewed = [path for path in paths if path != RECEIPT]
    entries = []
    json_count = 0
    json_errors = []
    patterns = {
        "raw_uuid": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"
        ),
        "credential_or_secret": re.compile(
            r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|"
            r"(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|"
            r"(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}|"
            r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"
        ),
        "private_route_value": re.compile(
            r"(?:source_thread_id|resume[_ -]?token|private_callable_identifier)"
            r"\s*[:=]\s*[\"'][^\"']+",
            re.I,
        ),
        "session_stream_payload": re.compile(
            r"(?:conversation[_ -]?transcript|session[_ -]?stream)"
            r"\s*[:=]\s*[\"'][^\"']+",
            re.I,
        ),
    }
    candidates = []
    for path in reviewed:
        content = blob(path)
        entries.append(
            {
                "path": path,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
        if path.endswith(".json"):
            json_count += 1
            try:
                json.loads(content.decode("utf-8"))
            except Exception as exc:  # pragma: no cover
                json_errors.append({"path": path, "error": type(exc).__name__})
        if Path(path).suffix.lower() in {
            ".py",
            ".json",
            ".md",
            ".txt",
            ".html",
            ".yaml",
            ".yml",
        }:
            text = content.decode("utf-8", errors="replace")
            for label, pattern in patterns.items():
                if pattern.search(text):
                    candidates.append({"path": path, "class": label})
    confirmed = [row for row in candidates if row["path"] not in SCANNER_FILES]

    manifest = json.loads(
        blob(PHASE_PREFIX + "validation/evidence-candidate-manifest.json").decode(
            "utf-8"
        )
    )
    manifest_map = {row["path"]: row["git_blob"] for row in manifest["entries"]}
    manifest_mismatches = []
    for path, expected in manifest_map.items():
        if path not in paths:
            manifest_mismatches.append(
                {"path": path, "expected": expected, "actual": "not_staged"}
            )
            continue
        actual = str(git("rev-parse", f":{path}"))
        if actual != expected:
            manifest_mismatches.append(
                {"path": path, "expected": expected, "actual": actual}
            )
    allowed_exclusions = {
        PHASE_PREFIX + "validation/evidence-candidate-manifest.json",
        PHASE_PREFIX + "validation/evidence-validation.json",
        PHASE_PREFIX + "validation/evidence-minimal-validation.json",
        RECEIPT,
    }
    unmanifested = sorted(set(paths) - set(manifest_map) - allowed_exclusions)
    truth = json.loads(
        blob(PHASE_PREFIX + "truth/phase-truth-evidence.json").decode("utf-8")
    )
    structure_valid = (
        truth["outcomes"]
        == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
        and truth["synthetic_mutation_negative_count"] == 150
        and truth["route_state"] == "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"
        and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    )
    valid = not any(
        [
            out_of_scope,
            frozen_changes,
            non_additions,
            forbidden_lifecycle,
            json_errors,
            confirmed,
            manifest_mismatches,
            unmanifested,
            not structure_valid,
        ]
    )
    receipt = {
        "schema": "ghc.family.v654-v7.evidence-staged-review.v1",
        "lifecycle": "x2_evidence_precommit",
        "x1_commit": X1,
        "staged_path_count": len(paths),
        "reviewed_content_count": len(reviewed),
        "receipt_self_exclusion": RECEIPT,
        "name_list_sha256": hashlib.sha256(
            ("\n".join(paths) + "\n").encode("utf-8")
        ).hexdigest(),
        "entries": entries,
        "json_parse_count": json_count,
        "json_errors": json_errors,
        "privacy_classes": list(patterns),
        "privacy_candidate_count": len(candidates),
        "privacy_definition_only_count": len(candidates) - len(confirmed),
        "privacy_confirmed_hits": confirmed,
        "manifest_entry_count": len(manifest_map),
        "manifest_mismatches": manifest_mismatches,
        "unmanifested_paths": unmanifested,
        "out_of_scope": out_of_scope,
        "frozen_x1_changes": frozen_changes,
        "non_additions": non_additions,
        "forbidden_lifecycle_paths": forbidden_lifecycle,
        "evidence_structure_valid": structure_valid,
        "valid": valid,
        "boundary": (
            "Exact evidence Git-index surface only; no final-head, independent "
            "reproduction, production, professional, legal, cultural, "
            "Māori-authority, Theory-of-Everything, or Stage 20 credit."
        ),
    }
    target = ROOT / RECEIPT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "valid": valid,
                "staged": len(paths),
                "reviewed": len(reviewed),
                "json": json_count,
                "privacy_hits": len(confirmed),
                "manifest": len(manifest_map),
            },
            sort_keys=True,
        )
    )
    if not valid:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Review the exact staged v656-v1 evidence surface."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/tamar-vey/v656-v1/"
X1 = "ed877dc0be03fdd82318ba218926f517f30779ae"
RECEIPT = PHASE_PREFIX + "validation/evidence-staged-review.json"
ALLOWED_SCRIPTS = {
    "scripts/ghc_family_v656_v1_core.py",
    "scripts/ghc_family_darkroom_film_custody_boundary.py",
    "scripts/ghc_family_darkroom_chemical_sequence_integrity.py",
    "scripts/ghc_family_darkroom_capacity_waste_reserve.py",
    "scripts/ghc_family_darkroom_optical_exposure_proxy.py",
    "scripts/ghc_family_darkroom_wash_archive_handover.py",
    "scripts/ghc_family_darkroom_accessibility_incident_boundary.py",
    "scripts/ghc_family_photo_privacy_authority_reserve.py",
    "scripts/ghc_family_gmut_photochemical_field_firewall.py",
    "scripts/ghc_family_thos_freed_darkroom_profile.py",
    "scripts/ghc_family_v656_v1_suite.py",
    "scripts/build_ghc_family_v656_v1_evidence.py",
    "scripts/ghc_family_v656_v1_validate.py",
    "scripts/ghc_family_v656_v1_evidence_staged_review.py",
}
ALLOWED_TESTS = {
    "tests/test_ghc_family_v656_v1_core.py",
    "tests/test_ghc_family_v656_v1_validation.py",
}
SCANNER_FILES = {
    "scripts/ghc_family_v656_v1_validate.py",
    "scripts/ghc_family_v656_v1_evidence_staged_review.py",
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


def staged_blob_oids(paths: list[str]) -> dict[str, str]:
    wanted = set(paths)
    rows: dict[str, str] = {}
    raw = bytes(git("ls-files", "--stage", "-z", text=False))
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        _mode, oid, stage = metadata.decode("ascii").split()
        path = raw_path.decode("utf-8")
        if stage == "0" and path in wanted:
            rows[path] = oid
    return rows


def staged_blobs(paths: list[str], oid_map: dict[str, str]) -> dict[str, bytes]:
    missing = [path for path in paths if path not in oid_map]
    if missing:
        raise RuntimeError(f"staged blob OID missing for {missing}")
    request = "".join(f"{oid_map[path]}\n" for path in paths).encode("ascii")
    result = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        check=True,
        input=request,
        capture_output=True,
    )
    output = result.stdout
    offset = 0
    blobs: dict[str, bytes] = {}
    for path in paths:
        header_end = output.index(b"\n", offset)
        header = output[offset:header_end].decode("ascii").split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
        size = int(header[2])
        start = header_end + 1
        blobs[path] = output[start : start + size]
        offset = start + size + 1
    return blobs


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
    oid_map = staged_blob_oids(paths)
    blob_map = staged_blobs(reviewed, oid_map)
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
        content = blob_map[path]
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
        blob_map[
            PHASE_PREFIX + "validation/evidence-candidate-manifest.json"
        ].decode("utf-8")
    )
    manifest_map = {row["path"]: row["git_blob"] for row in manifest["entries"]}
    manifest_mismatches = []
    for path, expected in manifest_map.items():
        if path not in paths:
            manifest_mismatches.append(
                {"path": path, "expected": expected, "actual": "not_staged"}
            )
            continue
        actual = oid_map[path]
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
        blob_map[PHASE_PREFIX + "truth/phase-truth-evidence.json"].decode("utf-8")
    )
    structure_valid = (
        truth["outcomes"]
        == {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
        and truth["synthetic_mutation_negative_count"] == 150
        and truth["route_state"] == "HELD_NO_DOWNSTREAM_AUTHORITY"
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
        "schema": "ghc.family.v656-v1.evidence-staged-review.v1",
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

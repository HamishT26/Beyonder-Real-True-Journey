#!/usr/bin/env python3
"""Review the exact Git-index surface for Lyren v655-v2 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/lyren-moss/v655-v2/"
RECEIPT = PHASE_PREFIX + "validation/x1-staged-review.json"
ALLOWED_EXACT = {
    "scripts/build_ghc_family_v655_v2_x1.py",
    "scripts/ghc_family_v655_v2_phase_catalogue.py",
    "scripts/ghc_family_v655_v2_phase_data.py",
    "scripts/ghc_family_v655_v2_x1_staged_review.py",
    "tests/test_ghc_family_v655_v2_x1.py",
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
    out_of_scope = sorted(
        path
        for path in paths
        if not path.startswith(PHASE_PREFIX) and path not in ALLOWED_EXACT
    )
    disallowed_statuses = sorted(
        (
            {"status": status, "path": path}
            for status, path in statuses
            if status not in {"A", "M"}
        ),
        key=lambda row: (row["path"], row["status"]),
    )
    forbidden_paths = sorted(
        path
        for path in paths
        if any(
            segment in {"x2", "evidence", "closeout", "seal", "final"}
            for segment in Path(path).parts
        )
    )
    reviewed = [path for path in paths if path != RECEIPT]
    json_errors = []
    json_count = 0
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
    entries = []
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
            except Exception as exc:  # pragma: no cover - diagnostic path
                json_errors.append({"path": path, "error": type(exc).__name__})
        if Path(path).suffix.lower() in {".py", ".json", ".md", ".txt", ".yaml", ".yml"}:
            text = content.decode("utf-8", errors="replace")
            for label, pattern in patterns.items():
                if pattern.search(text):
                    candidates.append({"path": path, "class": label})
    confirmed = [
        row
        for row in candidates
        if row["path"]
        not in {
            "scripts/build_ghc_family_v655_v2_x1.py",
            "scripts/ghc_family_v655_v2_x1_staged_review.py",
        }
    ]
    proposals = json.loads(
        blob(PHASE_PREFIX + "preregistration/proposals.json").decode("utf-8")
    )
    mutations = json.loads(
        blob(PHASE_PREFIX + "validation/preregistered-mutation-plan.json").decode(
            "utf-8"
        )
    )
    x1_truth = json.loads(
        blob(PHASE_PREFIX + "truth/x1-phase-truth.json").decode("utf-8")
    )
    structure_valid = (
        proposals["proposal_count"] == 30
        and proposals["x1_only"] is True
        and proposals["observed_outcomes_present"] is False
        and mutations["count"] == 150
        and mutations["x1_execution_count"] == 0
        and x1_truth["lifecycle"] == "x1_frozen_not_executed"
        and x1_truth["observed_outcome_count"] == 0
    )
    valid = not any(
        [
            out_of_scope,
            disallowed_statuses,
            forbidden_paths,
            json_errors,
            confirmed,
            not structure_valid,
        ]
    )
    receipt = {
        "schema": "ghc.family.v655-v2.x1-staged-review.v1",
        "lifecycle": "x1_precommit",
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
        "out_of_scope": out_of_scope,
        "disallowed_statuses": disallowed_statuses,
        "forbidden_x2_or_lifecycle_paths": forbidden_paths,
        "x1_structure_valid": structure_valid,
        "valid": valid,
        "boundary": (
            "Exact staged x1 surface only; no x2 execution, independent "
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
    if not valid:
        raise SystemExit(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    print(
        json.dumps(
            {
                "valid": True,
                "staged": len(paths),
                "reviewed": len(reviewed),
                "json": json_count,
                "privacy_hits": 0,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

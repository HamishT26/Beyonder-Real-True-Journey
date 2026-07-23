#!/usr/bin/env python3
"""Review the second staged v652-v2 terminal correction."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import ghc_family_v652_v2_correction_review as base

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/orin-thale/v652-v2"
SOURCE = "f168bcb798715d61d8b0a9ec2c6646a7af09ce29"
X1 = "3f5b49dc1a380452593c8080c3ae134e654c2079"
EVIDENCE = "d185405470b9205a21d9b018bc0d3f7f44f49444"
CLOSEOUT = "0053eef587ebdc88d8bafbf09b2f214737abd539"
CORRECTION1 = "19239aa3b00c8d7e32b329a2addae8391c8662a8"
EXCLUSIONS = {
    "docs/orin-thale/v652-v2/validation/correction2-delta-manifest.json",
    "docs/orin-thale/v652-v2/validation/corrected2-owner-manifest.json",
    "docs/orin-thale/v652-v2/validation/correction2-staged-privacy.json",
    "docs/orin-thale/v652-v2/validation/correction2-staged-review.json",
}


def main() -> None:
    if base.git("rev-parse", "HEAD") != CORRECTION1:
        raise SystemExit("second correction review requires exact first-correction HEAD")
    delta_paths = set(str(base.git("diff", "--cached", "--name-only", CORRECTION1)).splitlines())
    owner_paths = set(str(base.git("diff", "--cached", "--name-only", SOURCE)).splitlines())
    if not EXCLUSIONS.issubset(delta_paths): raise SystemExit({"missing_self_exclusions": sorted(EXCLUSIONS - delta_paths)})
    delta_entries = [base.index_entry(path) for path in sorted(delta_paths - EXCLUSIONS)]
    owner_entries = [base.index_entry(path) for path in sorted(owner_paths - EXCLUSIONS)]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definition_paths = {
        "scripts/build_ghc_family_v652_v2_preregistration.py", "scripts/ghc_family_v652_v2_x1_validate.py",
        "scripts/ghc_family_v652_v2_evidence_validate.py", "scripts/ghc_family_v652_v2_closeout_review.py",
        "scripts/ghc_family_v652_v2_correction_review.py", "scripts/ghc_family_v652_v2_correction2_review.py",
        "scripts/ghc_family_v652_v2_final_validate.py", "docs/orin-thale/v652-v2/validation/x1-staged-privacy.json",
        "docs/orin-thale/v652-v2/validation/evidence-staged-privacy.json", "docs/orin-thale/v652-v2/validation/closeout-staged-privacy.json",
        "docs/orin-thale/v652-v2/validation/correction-staged-privacy.json", "docs/orin-thale/v652-v2/validation/correction2-staged-privacy.json",
    }
    candidates, confirmed, json_errors = [], [], []
    for path in sorted(owner_paths):
        data = base.git("show", f":{path}", binary=True); assert isinstance(data, bytes)
        try: text = data.decode("utf-8")
        except UnicodeDecodeError: continue
        if path.endswith(".json"):
            try: json.loads(text)
            except Exception as exc: json_errors.append({"path": path, "error": str(exc)})
        for name, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if path in definition_paths else "confirmed_payload_hit"
                row = {"path": path, "pattern_class": name, "disposition": disposition}; candidates.append(row)
                if disposition == "confirmed_payload_hit": confirmed.append(row)
    x1_paths = set(str(base.git("diff-tree", "--no-commit-id", "--name-only", "-r", X1)).splitlines())
    evidence_paths = set(str(base.git("diff-tree", "--no-commit-id", "--name-only", "-r", EVIDENCE)).splitlines())
    closeout_paths = set(str(base.git("diff-tree", "--no-commit-id", "--name-only", "-r", CLOSEOUT)).splitlines())
    closeout_owner = set(str(base.git("diff", "--name-only", f"{SOURCE}..{CLOSEOUT}")).splitlines())
    correction1_paths = set(str(base.git("diff-tree", "--no-commit-id", "--name-only", "-r", CORRECTION1)).splitlines())
    correction1_owner = set(str(base.git("diff", "--name-only", f"{SOURCE}..{CORRECTION1}")).splitlines())
    prior = {
        "x1": base.replay(X1, "docs/orin-thale/v652-v2/validation/x1-staged-manifest.json", x1_paths),
        "evidence": base.replay(EVIDENCE, "docs/orin-thale/v652-v2/validation/evidence-staged-manifest.json", evidence_paths),
        "closeout_delta": base.replay(CLOSEOUT, "docs/orin-thale/v652-v2/validation/closeout-delta-manifest.json", closeout_paths),
        "closeout_owner": base.replay(CLOSEOUT, "docs/orin-thale/v652-v2/validation/final-owner-manifest.json", closeout_owner),
        "correction1_delta": base.replay(CORRECTION1, "docs/orin-thale/v652-v2/validation/correction-delta-manifest.json", correction1_paths),
        "correction1_owner": base.replay(CORRECTION1, "docs/orin-thale/v652-v2/validation/corrected-owner-manifest.json", correction1_owner),
    }
    unstaged = str(base.git("diff", "--name-only")).splitlines()
    diff_check = subprocess.run(["git", "diff", "--cached", "--check"], cwd=REPO, capture_output=True)
    valid = not confirmed and not json_errors and not unstaged and diff_check.returncode == 0 and all(row["valid"] for row in prior.values())
    base.write("validation/correction2-delta-manifest.json", {"schema": "ghc.family.v652-v2.correction2-delta-manifest.v1", "hash_domain": "git_index_blob", "base_commit": CORRECTION1, "entries": delta_entries, "entry_count": len(delta_entries), "self_exclusions": sorted(EXCLUSIONS), "coverage_boundary": "Exact first-correction-to-second-corrected-final staged delta except four declared self-referential review files."})
    base.write("validation/corrected2-owner-manifest.json", {"schema": "ghc.family.v652-v2.corrected2-owner-manifest.v1", "hash_domain": "git_index_blob", "source_commit": SOURCE, "entries": owner_entries, "entry_count": len(owner_entries), "self_exclusions": sorted(EXCLUSIONS), "coverage_boundary": "Exact source-to-second-corrected-final owner union except four declared self-referential review files."})
    base.write("validation/correction2-staged-privacy.json", {"schema": "ghc.family.v652-v2.correction2-privacy.v1", "scanned_file_count": len(owner_paths), "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes; zero confirmed hits is not complete privacy assurance."})
    base.write("validation/correction2-staged-review.json", {"schema": "ghc.family.v652-v2.correction2-staged-review.v1", "delta_path_count": len(delta_paths), "delta_manifest_entry_count": len(delta_entries), "owner_path_count": len(owner_paths), "owner_manifest_entry_count": len(owner_entries), "self_exclusion_count": len(EXCLUSIONS), "json_parsed_count": sum(path.endswith('.json') for path in owner_paths), "json_errors": json_errors, "privacy_confirmed_hits": len(confirmed), "prior_manifest_replay": prior, "unstaged_paths": unstaged, "diff_check_exit": diff_check.returncode, "valid": valid, "boundary": "Exact staged second correction review only; not final commit, canonical validation, independent reproduction, complete privacy, exhaustive security, accessibility conformance, authority, or Stage 20 readiness."})
    print(json.dumps({"delta_paths": len(delta_paths), "delta_entries": len(delta_entries), "owner_paths": len(owner_paths), "owner_entries": len(owner_entries), "json": sum(path.endswith('.json') for path in owner_paths), "privacy_hits": len(confirmed), "prior": all(row['valid'] for row in prior.values()), "valid": valid}, sort_keys=True))
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__": main()

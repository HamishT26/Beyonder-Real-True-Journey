#!/usr/bin/env python3
"""Review staged v647-v6 evidence or closeout paths in the Git-index blob domain."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_PREFIX = "docs/ilyra-fen/v647-v6/"
FROZEN = {
    PHASE_PREFIX + "x1-proposals.json",
    PHASE_PREFIX + "x1-preregistration.md",
    PHASE_PREFIX + "approval-packets/x1-approval-portfolio.json",
    PHASE_PREFIX + "prototypes/x1-skill-runner-plan.json",
    PHASE_PREFIX + "maintenance/x1-clean-refine-plan.json",
    PHASE_PREFIX + "provenance/prior-proposal-collision-audit.json",
    PHASE_PREFIX + "provenance/prior-portfolio-collision-audit.json",
    PHASE_PREFIX + "sources/source-ledger.json",
}
ALLOWED_DOMAIN_WRAPPERS = {
    "scripts/ghc_family_barnes_rivers_obligations.py",
    "scripts/ghc_family_covariate_shift_board.py",
    "scripts/ghc_family_gibbs_phase_rule.py",
    "scripts/ghc_family_oauth_token_exchange_profile.py",
    "scripts/ghc_family_png_chunk_tribunal.py",
    "scripts/ghc_family_sdss_dr19_zero_row.py",
    "scripts/ghc_family_treegrid_audit.py",
    "scripts/ghc_family_watcher_reconciliation_tribunal.py",
    "scripts/ghc_family_weather_warning_handover.py",
}


def git(*args: str, text: bool = True) -> str | bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=text)
    return result.stdout


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["evidence", "closeout"], required=True)
    args = parser.parse_args()
    manifest_rel = PHASE_PREFIX + f"validation/{args.stage}-staged-manifest.json"
    review_rel = PHASE_PREFIX + f"validation/{args.stage}-staged-review.json"
    exclusions = {manifest_rel, review_rel}
    paths = sorted(line for line in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if line)
    allowed_script_prefixes = ("scripts/ghc_family_v647_v6_", "scripts/build_ghc_family_v647_v6_")
    allowed_test_prefix = "tests/test_ghc_family_v647_v6"
    out_of_scope = [
        path for path in paths
        if not path.startswith(PHASE_PREFIX)
        and not path.startswith(allowed_script_prefixes)
        and not path.startswith(allowed_test_prefix)
        and path not in ALLOWED_DOMAIN_WRAPPERS
    ]
    frozen_changes = sorted(set(paths) & FROZEN)
    patterns = {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_local_path": re.compile(rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_uri": re.compile(rb"\b(?:app|plugin)://", re.I),
        "delegation_markup": re.compile(rb"<(?:codex_delegation|source_thread_id)>", re.I),
        "credential_assignment": re.compile(rb"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
    }
    hits = []
    entries = []
    for path in paths:
        if path in exclusions:
            continue
        data = bytes(git("show", f":{path}", text=False))
        for label, pattern in patterns.items():
            if pattern.search(data):
                hits.append({"path": path, "pattern_class": label})
        index_line = str(git("ls-files", "-s", "--", path)).strip()
        entries.append({"path": path, "git_blob": index_line.split()[1], "bytes": len(data)})
    manifest = {
        "schema": f"ghc.family.v647-v6.{args.stage}-staged-manifest.v1", "hash_domain": "Git index blob identity",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
        "boundary": f"Exact staged {args.stage} surface only; same-owner evidence is not independent reproduction.",
    }
    valid = not out_of_scope and not frozen_changes and not hits
    review = {
        "schema": f"ghc.family.v647-v6.{args.stage}-staged-review.v1", "stage": args.stage,
        "staged_count": len(paths), "content_entry_count": len(entries), "out_of_scope_paths": out_of_scope,
        "x1_frozen_path_changes": frozen_changes, "privacy_pattern_classes": sorted(patterns),
        "privacy_hits": hits, "privacy_confirmed_hit_count": len(hits), "diff_hygiene": True,
        "self_exclusions": sorted(exclusions), "valid": valid,
    }
    write_json(ROOT / manifest_rel, manifest)
    write_json(ROOT / review_rel, review)
    print(json.dumps({"stage": args.stage, "staged": len(paths), "entries": len(entries), "frozen_changes": len(frozen_changes), "privacy_hits": len(hits), "issues": len(out_of_scope) + len(frozen_changes) + len(hits), "valid": valid}))
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()

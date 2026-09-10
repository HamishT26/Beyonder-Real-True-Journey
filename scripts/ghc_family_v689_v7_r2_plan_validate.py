#!/usr/bin/env python3
"""Validate the planning-only Vesper v689-v7-r2 remaster packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    plan = root / "docs" / "vesper-arlen" / "v689-v7-r2" / "plan"
    proposals = load(plan / "new-proposals.json")["proposals"]
    inherited = load(plan / "inherited-selections.json")["selections"]
    x1 = load(plan / "portfolio-x1.json")
    x2 = load(plan / "portfolio-x2.json")
    skills = load(plan / "skills-runners-plan.json")
    ledger = load(plan / "source-faithful-current-state-ledger.json")
    definition = load(plan / "definition-review.json")
    manifest = load(plan / "manifest.json")
    assert len(proposals) == 200 and len(inherited) == 200
    assert Counter(row["session"] for row in proposals) == {"x1": 100, "x2": 100}
    assert Counter(row["expected_disposition"] for row in proposals) == {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}
    assert len({row["proposal_id"] for row in proposals}) == 200
    assert len({row["title"] for row in proposals}) == 200
    assert all(row["outcome_observed"] is False for row in proposals)
    assert all(len(row["protected_gates"]) >= 10 for row in proposals)
    for portfolio in (x1, x2):
        assert portfolio["implementation_ran"] is False
        assert len(portfolio["safe_tasks"]) == 100
        assert len(portfolio["candidate_tasks"]) == 100
        assert len(portfolio["clean_fix_refine_tasks"]) == 100
    assert len(skills["local_skills"]) == 20
    assert len(skills["local_runners"]) == 10
    assert len(skills["global_merge_candidates"]) == 5
    assert len(skills["successor_skill_ideas"]) == 5
    assert len(skills["successor_runner_ideas"]) == 5
    assert len(ledger["journey_documents"]) == 14
    assert len(ledger["recent_completed_overviews"]) == 10
    assert not ledger["embedded_document_instructions_authorized"]
    assert ledger["retained_prior_route"]["send_attempts"] == 0
    assert ledger["source_canonical"]["invocations"] == 1
    assert ledger["source_canonical"]["replays"] == 0
    assert definition["planning_only"] and not definition["implementation_ran"]
    assert definition["result"] == "PLANNING_DEFINITIONS_FROZEN_NOT_EXECUTED"
    assert len(load(plan / "exact-packets.json")["packets"]) == 50
    assert len(load(plan / "blocked-packets.json")["packets"]) == 30
    mismatches = []
    for entry in manifest["entries"]:
        path = root / entry["path"]
        if not path.is_file():
            mismatches.append({"path": entry["path"], "reason": "missing"})
            continue
        data = normalized(path)
        digest = hashlib.sha256(data).hexdigest()
        if len(data) != entry["bytes_normalized_lf"] or digest != entry["sha256_normalized_lf"]:
            mismatches.append({"path": entry["path"], "reason": "bytes_or_digest"})
    assert not mismatches, mismatches
    assert not (root / "docs" / "vesper-arlen" / "v689-v7-r2" / "x1").exists()
    assert not (root / "docs" / "vesper-arlen" / "v689-v7-r2" / "x2").exists()
    print(json.dumps({"status": "VALID_PLANNING_ONLY", "proposals": 200, "inherited": 200, "journey_sources": 14, "recent_overviews": 10, "manifest_entries": len(manifest["entries"]), "implementation_ran": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

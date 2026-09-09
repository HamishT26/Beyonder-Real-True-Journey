#!/usr/bin/env python3
"""Validate the immutable planning-only Vesper v689-v7 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=strict_object)


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    plan = root / "docs" / "vesper-arlen" / "v689-v7" / "plan"
    checks: list[str] = []

    json_paths = sorted(plan.glob("*.json"))
    documents = {path.name: load(path) for path in json_paths}
    checks.append(f"strict_json:{len(json_paths)}")

    proposals = documents["new-proposals.json"]["proposals"]
    assert len(proposals) == 200
    assert len({row["proposal_id"] for row in proposals}) == 200
    assert Counter(row["session"] for row in proposals) == Counter({"x1": 100, "x2": 100})
    operation_counts = Counter(row["operation"] for row in proposals)
    assert len(operation_counts) == 20 and set(operation_counts.values()) == {10}
    dispositions = Counter(row["expected_disposition"] for row in proposals)
    assert dispositions == Counter({"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5})
    assert set(dispositions) <= ALLOWED
    assert all(row["candidate_expected"] == {"error": "E_FIELDS", "ok": False, "value": None} for row in proposals)
    assert all(row["outcome_observed"] is False for row in proposals)
    checks.append("proposal_contracts:200")

    inherited = documents["inherited-selections.json"]["selections"]
    assert len(inherited) == 200
    assert len({row["selection_id"] for row in inherited}) == 200
    for row in inherited:
        encoded = json.dumps(row["source_record"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        assert hashlib.sha256(encoded).hexdigest() == row["source_record_sha256"]
        assert row["current_execution_credit"] == row["current_novelty_credit"] == 0
    checks.append("inherited_zero_credit:200")

    for session in ("x1", "x2"):
        portfolio = documents[f"portfolio-{session}.json"]
        assert portfolio["implementation_ran"] is False
        assert portfolio["counts"] == {"candidate": 100, "clean_fix_refine": 100, "safe": 100}
        assert len(portfolio["safe_tasks"]) == len(portfolio["candidate_tasks"]) == len(portfolio["clean_fix_refine_tasks"]) == 100
    checks.append("portfolio_definitions:600")

    skill_plan = documents["skills-runners-plan.json"]
    assert len(skill_plan["skills"]) == 20
    assert len(skill_plan["runners"]) == 10
    assert len({row["name"] for row in skill_plan["skills"]}) == 20
    assert len({row["name"] for row in skill_plan["runners"]}) == 10
    checks.append("skills_runners:30")

    assert documents["exact-packets.json"]["count"] == len(documents["exact-packets.json"]["packets"]) == 50
    assert documents["blocked-packets.json"]["count"] == len(documents["blocked-packets.json"]["packets"]) == 30
    assert len(documents["package-plan.json"]["packages"]) == 3
    assert all(len(row["sha256"]) == 64 and row["yanked"] is False for row in documents["package-plan.json"]["packages"])
    assert documents["definition-review.json"]["implementation_ran"] is False
    assert documents["definition-review.json"]["planning_only"] is True
    assert documents["resource-budget.json"]["selected_lane"] == "blank_root_rotation"
    assert documents["route-v4.json"]["prospective_next"]["owner"] == "Ilyan Reed"
    checks.append("approvals_packages_route")

    novelty = documents["novelty-review.json"]
    assert novelty["exact_title_collisions"] == 0
    assert novelty["universal_novelty_claimed"] is False
    assert novelty["accessible_inherited_titles"] >= 800
    checks.append("source_bounded_novelty")

    manifest = documents["manifest.json"]
    expected_paths = {entry["path"] for entry in manifest["entries"]}
    actual_paths = {
        path.relative_to(root).as_posix()
        for path in plan.rglob("*")
        if path.is_file() and path.name != "manifest.json"
    }
    actual_paths.update(
        {
            "scripts/ghc_family_v689_v7_plan_builder.py",
            "scripts/ghc_family_v689_v7_plan_validate.py",
        }
    )
    assert expected_paths == actual_paths
    for entry in manifest["entries"]:
        data = normalized(root / entry["path"])
        assert len(data) == entry["bytes_normalized_lf"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256_normalized_lf"]
    checks.append(f"normalized_lf_manifest:{len(expected_paths)}")

    privacy_patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_user_root": re.compile(r"[A-Za-z]:\\\\Users\\\\", re.I),
        "private_uri": re.compile(r"(?:plugin|app|codex)://", re.I),
        "delegation_markup": re.compile(r"(?:<codex_delegation|source_thread_id)", re.I),
        "credential_assignment": re.compile(r"(?:api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}", re.I),
    }
    confirmed: list[dict[str, str]] = []
    for path in sorted(plan.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in privacy_patterns.items():
            if pattern.search(text):
                confirmed.append({"class": label, "path": path.relative_to(root).as_posix()})
    assert not confirmed, confirmed
    checks.append(f"privacy_zero_hits:{len(list(plan.rglob('*')))}")

    print(json.dumps({"status": "VALID_PLANNING_ONLY", "checks": checks, "check_count": len(checks)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

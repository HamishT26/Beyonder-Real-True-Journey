#!/usr/bin/env python3
"""Minimal independent validation floor for Tamar Vey v644-v3."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from ghc_family_v644_v3_evidence import normalized_sha256


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def verify(phase: Path, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    phase = phase.resolve()
    repo = phase.parents[2]
    truth = load(phase / "phase-truth.json")
    x1 = load(phase / "x1-proposals.json")
    x2 = load(phase / "x2-proposal-ledger.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    manifest = load(phase / "reproduction/manifest.json")
    seal = load(phase / "reproduction/x1-content-seal.json")
    privacy = load(phase / "validation/x2-privacy-scan.json")
    sources = load(phase / "sources/source-ledger.json")
    board = load(phase / "stage20/domain-veto-evidence-board.json")
    report = (phase / "deliverables/v644-v3-boundary-evidence-report.html").read_text(encoding="utf-8")
    overview = (phase / "deliverables/v644-v3-final-integrated-overview.md").read_text(encoding="utf-8")
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool) -> None:
        checks.append({"name": name, "passed": bool(passed)})

    distribution = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
    add("phase", truth.get("phase") == "v644-gmut-thos-v3-x1-x2")
    add("owner", truth.get("owner") == "Tamar Vey")
    add("ten proposals", x1.get("proposal_count") == 10 == x2.get("proposal_count"))
    add("250 prior proposals", x1.get("prior_frozen_proposal_count") == 250)
    add("four labels", x1.get("outcome_classes") == ["completed", "represented", "open_gap", "exact_gate"])
    add("distribution", truth.get("proposal_distribution") == distribution == x2.get("distribution"))
    add("80 cases", truth.get("case_count") == 80 == x2.get("total_case_count"))
    add("70 rejections", truth.get("synthetic_negative_count") == 70 == x2.get("synthetic_negative_count"))
    add("negative exact floor", negatives.get("negative_count") == 1296 + negatives.get("x2_operational_count", 0))
    add("negative list exact", len(negatives.get("negatives", [])) == negatives.get("negative_count"))
    add("all negatives retained", negatives.get("all_retained") is True)
    add("inherited negatives", negatives.get("inherited_count") == 1220)
    add("x1 negatives", negatives.get("x1_operational_count") == 6)
    add("synthetic negatives", negatives.get("new_synthetic_count") == 70)
    add("five open gaps", gates.get("open_gap_count") == 5)
    add("six exact gates", gates.get("exact_gate_count") == 6)
    add("gates visible", gates.get("all_visible") is True and gates.get("none_silently_closed") is True)
    add("Māori authority gate", "Māori" in json.dumps(gates, ensure_ascii=False))
    add("primary focus", truth.get("primary_focus") == "GMUT Mind")
    add("protected claims false", bool(truth.get("protected_claims")) and all(value is False for value in truth["protected_claims"].values()))
    add("terminal verdict", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")
    add("route unsent", truth.get("route_state") == "PREPARED_NOT_SENT" and truth.get("outbound_message_count") == 0)
    add("x1 seal", seal.get("file_count") == 27 and seal.get("all_current_blobs_unchanged") is True)
    add("source count", sources.get("effective_source_count") == 175)
    add("source statuses", sources.get("effective_status_counts") == {"current": 78, "stable": 86, "draft": 8, "watch": 3})
    add("privacy valid", privacy.get("valid") is True)
    add("privacy zero", privacy.get("hit_count") == 0)
    add("privacy nonempty", privacy.get("scanned_file_count", 0) > 0)
    add("manifest nonempty", manifest.get("entry_count", 0) > 0 and manifest.get("entry_count") == len(manifest.get("entries", [])))
    add("manifest parity", all((repo / row["path"]).is_file() and normalized_sha256(repo / row["path"]) == row["sha256_lf_normalized"] for row in manifest.get("entries", [])))
    add("snapshot state", manifest.get("snapshot_state") in ({"pending", "verified"} if allow_pending_snapshot else {"verified"}))
    add("same owner only", manifest.get("same_owner_repeatability_only") is True and manifest.get("independent_team_reproduction") is False)
    add("static report language", '<html lang="en">' in report)
    add("static report boundaries", "NOT_READY_FOR_STAGE_20" in report and "Māori" in report)
    folded = report.casefold()
    add("static report inert", "<script" not in folded and "<iframe" not in folded and "javascript:" not in folded and re.search(r"\son[a-z]+\s*=", folded) is None)
    add("static report landmarks", 'href="#main"' in report and 'id="main"' in report)
    add("table semantics", "<caption>" in report and 'scope="col"' in report and 'scope="row"' in report)
    add("overview floor", len(re.findall(r"\b\w+[\w’'-]*\b", overview, flags=re.UNICODE)) >= 1200)
    add("Stage 20 noncompensatory", board.get("compensation_across_domains_allowed") is False)
    add("Stage 20 vetoes", all(row.get("decision") == "veto" for row in board.get("vetoes", [])))
    add("all JSON parses", all(load(path) is not None for path in phase.rglob("*.json")))
    issues = [row["name"] for row in checks if not row["passed"]]
    return {
        "schema": "ghc.family.v644-v3.minimal-validation.v1",
        "phase": "v644-gmut-thos-v3-x1-x2",
        "valid": not issues,
        "checks_passed": len(checks) - len(issues),
        "checks_total": len(checks),
        "issues": issues,
        "allow_pending_snapshot": allow_pending_snapshot,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.phase_dir, args.allow_pending_snapshot)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(json.dumps({key: result[key] for key in ("valid", "checks_passed", "checks_total", "issues")}, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

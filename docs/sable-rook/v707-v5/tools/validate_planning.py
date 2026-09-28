from __future__ import annotations

import json
from pathlib import Path

from common import BOUNDARY, OPERATIONS, PHASE_ROOT, PROTECTED_GATES, ROOT, ensure_no_private_text, git_blob_oid, owner_files, rel

def main() -> None:
    p = PHASE_ROOT / "planning"
    checks = []
    def check(name: str, condition: bool, observed) -> None:
        checks.append({"name": name, "passed": bool(condition), "observed": observed})
    proposals = json.loads((p / "proposals.json").read_text(encoding="utf-8"))
    inherited = json.loads((p / "inherited-zero-credit.json").read_text(encoding="utf-8"))
    novelty = json.loads((p / "semantic-novelty-audit.json").read_text(encoding="utf-8"))
    portfolio = json.loads((p / "portfolio.json").read_text(encoding="utf-8"))
    flow = json.loads((p / "method-flow.json").read_text(encoding="utf-8"))
    manifest = json.loads((p / "manifest.json").read_text(encoding="utf-8"))
    rows = proposals["proposals"]
    check("proposal_count", len(rows) == 300, len(rows))
    check("proposal_unique_ids", len({r["id"] for r in rows}) == 300, len({r["id"] for r in rows}))
    check("proposal_unique_titles", len({r["title"] for r in rows}) == 300, len({r["title"] for r in rows}))
    check("planning_only", proposals["planning_only"] and proposals["executed_outcomes"] == 0, proposals["executed_outcomes"])
    check("four_labels", {r["expected_disposition"] for r in rows} == {"completed", "represented", "open_gap", "exact_gate"}, sorted({r["expected_disposition"] for r in rows}))
    check("operations", len(OPERATIONS) == 20, len(OPERATIONS))
    check("protected_gates", all(r["protected_gates"] == PROTECTED_GATES for r in rows), True)
    check("inherited_zero_credit", inherited["count"] == 300 and all(r["novelty_credit"] == 0 and r["completion_credit"] == 0 for r in inherited["rows"]), inherited["count"])
    check("semantic_comparisons", novelty["comparisons"] == 90000 and not novelty["quarantines"], novelty["comparisons"])
    check("portfolio_floors", portfolio["safe_x1"] >= 400 and portfolio["safe_x2"] >= 400 and portfolio["candidate_x1"] >= 300 and portfolio["cfr_x2"] >= 300, portfolio)
    check("held_packets", portfolio["exact_held"] == 50 and portfolio["blocked_held"] == 30, [portfolio["exact_held"], portfolio["blocked_held"]])
    check("method_flow", flow["counts"] == {"exact_gates": 0, "fail": 14, "methods": 14, "negatives": 14, "open_gaps": 0, "pass": 14, "witnesses": 28}, flow["counts"])
    manifest_mismatch = []
    for entry in manifest["entries"]:
        path = ROOT / entry["path"]
        if not path.exists() or git_blob_oid(path) != entry["git_blob"]:
            manifest_mismatch.append(entry["path"])
    check("manifest", not manifest_mismatch and manifest["count"] == len(manifest["entries"]), manifest_mismatch)
    json_errors = []
    for path in PHASE_ROOT.rglob("*.json"):
        try: json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc: json_errors.append([rel(path), str(exc)])
    check("strict_json", not json_errors, len(list(PHASE_ROOT.rglob("*.json"))))
    private_hits = ensure_no_private_text(owner_files())
    scanner_candidates = [h for h in private_hits if h["path"].endswith("/tools/common.py") and h["class"] in {"windows_absolute_path", "private_route_field"}]
    confirmed_hits = [h for h in private_hits if h not in scanner_candidates]
    check("privacy", not confirmed_hits, {"scanner_definition_candidates": scanner_candidates, "confirmed": confirmed_hits})
    check("no_x1_x2", not (PHASE_ROOT / "x1").exists() and not (PHASE_ROOT / "x2").exists(), True)
    check("owner_files_below_guard", len(owner_files()) < 2000, len(owner_files()))
    if not all(c["passed"] for c in checks):
        raise SystemExit(json.dumps({"state": "PLANNING_INVALID", "checks": checks}, ensure_ascii=False))
    print(json.dumps({"state": "VALID_PLANNING_ONLY", "passed": len(checks), "total": len(checks), "json": len(list(PHASE_ROOT.rglob('*.json'))), "owner_files": len(owner_files()), "boundary": BOUNDARY}, sort_keys=True))

if __name__ == "__main__":
    main()

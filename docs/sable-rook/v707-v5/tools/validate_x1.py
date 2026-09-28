from __future__ import annotations

import json

from common import BOUNDARY, PHASE_ROOT, ROOT, ensure_no_private_text, git, git_blob_oid, owner_files, rel

PLANNING_COMMIT = "33655babd0c3f024e2b91c93cc45f91a63e4edb5"

def main() -> None:
    x1 = PHASE_ROOT / "x1"; checks = []
    def check(name, condition, observed): checks.append({"name": name, "passed": bool(condition), "observed": observed})
    summary = json.loads((x1 / "summary.json").read_text(encoding="utf-8"))
    flow = json.loads((x1 / "method-flow.json").read_text(encoding="utf-8"))
    operational = json.loads((x1 / "method-flow-operational-overlay.json").read_text(encoding="utf-8"))
    manifest = json.loads((x1 / "manifest.json").read_text(encoding="utf-8"))
    check("contracts", summary["contracts"] == 150, summary["contracts"])
    check("outcomes", summary["outcomes"] == {"completed": 150, "represented": 0, "open_gap": 0, "exact_gate": 0}, summary["outcomes"])
    check("safe", summary["safe"] == 450, summary["safe"])
    check("candidate", summary["candidate_fail"] == 300, summary["candidate_fail"])
    check("refusal", summary["refusal_pass"] == 300, summary["refusal_pass"])
    check("corrected", summary["corrected_pass"] == 300, summary["corrected_pass"])
    check("tests", json.loads((x1 / "tests.json").read_text(encoding="utf-8"))["passed"] == 20, 20)
    check("skills", json.loads((x1 / "skill-receipts.json").read_text(encoding="utf-8"))["count"] == 10, 10)
    check("runners", json.loads((x1 / "runner-receipts.json").read_text(encoding="utf-8"))["count"] == 5, 5)
    check("flow", flow["counts"] == {"methods": 15, "witnesses": 1385, "pass": 1085, "fail": 300, "negatives": 300, "open_gaps": 0, "exact_gates": 0}, flow["counts"])
    check("operational_flow", operational["counts"] == {"methods": 1, "witnesses": 2, "pass": 1, "fail": 1, "negatives": 1, "open_gaps": 0, "exact_gates": 0}, operational["counts"])
    check("planning_immutable", not git("diff", "--name-only", PLANNING_COMMIT, "--", "docs/sable-rook/v707-v5/planning"), "")
    check("no_x2", not (PHASE_ROOT / "x2").exists(), True)
    mismatches = [e["path"] for e in manifest["entries"] if not (ROOT / e["path"]).exists() or git_blob_oid(ROOT / e["path"]) != e["git_blob"]]
    check("manifest", not mismatches, mismatches)
    json_errors = []
    for path in PHASE_ROOT.rglob("*.json"):
        try: json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc: json_errors.append([rel(path), str(exc)])
    check("strict_json", not json_errors, len(list(PHASE_ROOT.rglob("*.json"))))
    hits = ensure_no_private_text(owner_files())
    candidates = [h for h in hits if h["path"].endswith("/tools/common.py") and h["class"] in {"windows_absolute_path", "private_route_field"}]
    confirmed = [h for h in hits if h not in candidates]
    check("privacy", not confirmed, {"scanner_definition_candidates": candidates, "confirmed": confirmed})
    check("owner_files", len(owner_files()) < 2000, len(owner_files()))
    if not all(c["passed"] for c in checks): raise SystemExit(json.dumps({"state": "X1_INVALID", "checks": checks}, ensure_ascii=False))
    print(json.dumps({"state": "VALID_X1", "passed": len(checks), "total": len(checks), "json": len(list(PHASE_ROOT.rglob('*.json'))), "owner_files": len(owner_files()), "boundary": BOUNDARY}, sort_keys=True))

if __name__ == "__main__": main()

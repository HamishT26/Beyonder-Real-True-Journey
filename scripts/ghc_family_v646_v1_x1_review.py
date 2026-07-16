#!/usr/bin/env python3
"""Review the Eiren v646-v1 x1 freeze before it is committed."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/eiren-kestrel/v646-v1")
PHASE = ROOT / PHASE_REL
OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED_PROPOSAL = {
    "proposal_id", "title", "mission_surface", "hypothesis", "null_or_failure",
    "approval_class", "execution_lane", "current_primary_or_official_source_needs",
    "concrete_artifacts", "test_falsifier_or_acceptance_gate", "rollback_or_recovery",
    "protected_gates", "expected_disposition", "novelty_against_390_frozen_proposals",
}
PRIVATE = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "delegation_markup": re.compile(r"(?i)<\/?codex_delegation>|<source_thread_id>"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin)://"),
    "private_local_path": re.compile(r"(?i)\b[A-Z]:[\\/]+Users[\\/]+[^\\/\s]+"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,;]+"),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str, binary: bool = False) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary)


def phase_files() -> list[Path]:
    return sorted(p for p in PHASE.rglob("*") if p.is_file())


def scan_payload(name: str, payload: str) -> list[dict[str, Any]]:
    hits = []
    for kind, pattern in PRIVATE.items():
        for match in pattern.finditer(payload):
            hits.append({"path": name, "class": kind, "offset": match.start()})
    return hits


def structural() -> dict[str, Any]:
    issues: list[str] = []
    lifecycle_has_advanced = (PHASE / "phase-truth.json").exists()
    proposals = load(PHASE / "x1-proposals.json")
    rows = proposals.get("proposals", [])
    if proposals.get("prior_frozen_proposal_count") != 390: issues.append("prior proposal count is not 390")
    if proposals.get("new_frozen_proposal_count") != 10 or len(rows) != 10: issues.append("new proposal count is not 10")
    if proposals.get("frozen_chain_count_after_x1") != 400: issues.append("frozen chain count is not 400")
    if proposals.get("x2_execution_present") is not False: issues.append("x2 execution is present")
    if len({x.get("proposal_id") for x in rows}) != 10 or len({x.get("title") for x in rows}) != 10: issues.append("proposal ids or titles are not unique")
    for row in rows:
        missing = REQUIRED_PROPOSAL - set(row)
        if missing: issues.append(f"{row.get('proposal_id')} missing {sorted(missing)}")
        if row.get("expected_disposition") not in OUTCOMES: issues.append(f"{row.get('proposal_id')} invalid disposition")
    expected = proposals.get("expected_distribution", {})
    if expected != {"completed":6,"represented":2,"open_gap":1,"exact_gate":1}: issues.append("expected distribution mismatch")

    collision = load(PHASE / "provenance/prior-proposal-collision-audit.json")
    if collision.get("prior_frozen_proposal_count") != 390 or collision.get("exact_title_collision_count") != 0: issues.append("proposal novelty audit failed")
    if len(collision.get("comparisons", [])) != 10: issues.append("proposal comparison count mismatch")
    portfolio_collision = load(PHASE / "provenance/prior-portfolio-collision-audit.json")
    if portfolio_collision.get("exact_collision_count") != 0: issues.append("portfolio title collision found")

    portfolio = load(PHASE / "approval-packets/x1-approval-portfolio.json")
    if portfolio.get("counts") != {"safe_now":30,"candidates":20,"inherited_exact":10,"inherited_blocked":5}: issues.append("approval portfolio counts mismatch")
    if portfolio.get("completion_credit_before_x2") != 0: issues.append("portfolio has pre-x2 completion credit")
    if sum(x.get("origin") == "predecessor_reframed_seed" for x in portfolio.get("safe_now", [])) != 15: issues.append("safe predecessor-seed count mismatch")
    if any(x.get("x1_state") != "preregistered_no_completion_credit" for x in portfolio.get("safe_now", []) + portfolio.get("candidates", [])): issues.append("supporting packet has completion credit")
    if any(x.get("x2_execution") not in {"do_not_execute", "prohibited_without_new_evidence"} for x in portfolio.get("inherited_exact_packets", []) + portfolio.get("inherited_blocked_packets", [])): issues.append("exact or blocked execution boundary missing")

    tools = load(PHASE / "prototypes/x1-skill-runner-plan.json")
    if len(tools.get("skills", [])) != 20 or len(tools.get("runners", [])) != 10: issues.append("skill or runner count mismatch")
    if any(x.get("x2_state") != "preregistered_not_built_or_used" for x in tools.get("skills", []) + tools.get("runners", [])): issues.append("tool prototype has pre-x2 credit")
    clean = load(PHASE / "maintenance/x1-clean-refine-plan.json")
    if len(clean.get("tasks", [])) != 30 or clean.get("destructive_task_count") != 0 or clean.get("completion_credit_before_x2") != 0: issues.append("cleanup plan boundary mismatch")

    sources = load(PHASE / "sources/source-ledger.json")
    if len(sources.get("sources", [])) < 20: issues.append("source ledger is too small")
    if any(x.get("status") not in {"current","stable","draft","watch"} for x in sources.get("sources", [])): issues.append("invalid source status")
    if any(sources.get(k) != 0 for k in ("real_data_rows_ingested","likelihood_evaluations","real_participants","real_keys_or_proofs")): issues.append("source ledger overstates execution")

    method = load(PHASE / "method-flow/runner-validation.json")
    negatives = load(PHASE / "validation/x1-operational-negatives.json")
    if not method.get("valid"): issues.append("Method Flow validation failed")
    elif not lifecycle_has_advanced and (method.get("method_count") != 1 or method.get("witness_count") != 2): issues.append("x1 Method Flow count mismatch")
    elif lifecycle_has_advanced and (method.get("method_count",0) < 1 or method.get("witness_count",0) < 2): issues.append("advanced Method Flow lost the x1 baseline")
    if negatives.get("inherited_effective") != 2432 or negatives.get("preregistered_synthetic") != 70 or negatives.get("effective_after_x1") != 2503: issues.append("negative accounting mismatch")

    forbidden = ["phase-truth.json","x2-proposal-ledger.json","closeout-receipt.json","seal-receipt.json","final-validation-record.json"]
    if not lifecycle_has_advanced and any((PHASE / name).exists() for name in forbidden): issues.append("x2 or closeout artifact exists before the x1 freeze")
    required_index = [PHASE / "tooling/ghc-family-index.json", PHASE / "tooling/ghc-family-index.md"]
    if any(not p.is_file() for p in required_index): issues.append("phase-scoped GHC Family Index is missing")
    return {"schema":"ghc.family.v646-v1.x1-structural-review.v1","proposal_count":len(rows),"file_count":len(phase_files()),"lifecycle_has_advanced":lifecycle_has_advanced,"issues":issues,"valid":not issues}


def privacy_from_worktree() -> dict[str, Any]:
    hits = []
    files = phase_files()
    for path in files:
        try: payload = path.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        hits.extend(scan_payload(path.relative_to(ROOT).as_posix(), payload))
    return {"schema":"ghc.family.v646-v1.privacy-review.v1","pattern_classes":sorted(PRIVATE),"file_count":len(files),"confirmed_hits":hits,"confirmed_hit_count":len(hits),"valid":not hits}


def staged_review() -> dict[str, Any]:
    paths = [x for x in str(git("diff","--cached","--name-only","--diff-filter=ACMR")).splitlines() if x]
    issues = []
    allowed_prefix = PHASE_REL.as_posix() + "/"
    allowed_scripts = {"scripts/ghc_family_v646_v1_definitions.py","scripts/build_ghc_family_v646_v1_preregistration.py","scripts/ghc_family_v646_v1_x1_review.py","tests/test_ghc_family_v646_v1_x1.py"}
    for path in paths:
        if not (path.startswith(allowed_prefix) or path in allowed_scripts): issues.append(f"unexpected staged path: {path}")
        blob = git("show",f":{path}",binary=True)
        if path.endswith(".json"):
            try: json.loads(bytes(blob).decode("utf-8"))
            except Exception as exc: issues.append(f"invalid staged JSON {path}: {exc}")
        if path.startswith(allowed_prefix):
            try: hits = scan_payload(path, bytes(blob).decode("utf-8"))
            except UnicodeDecodeError: hits = []
            if hits: issues.append(f"privacy hits in staged {path}: {hits}")
    if len(paths) < 10: issues.append("staged x1 surface unexpectedly small")
    return {"schema":"ghc.family.v646-v1.x1-staged-review.v1","staged_file_count":len(paths),"staged_paths":paths,"issues":issues,"valid":not issues}


def write_receipts(structure: dict[str, Any], privacy: dict[str, Any], staged: dict[str, Any] | None) -> None:
    target = PHASE / "validation"
    target.mkdir(parents=True, exist_ok=True)
    (target / "x1-structural-review.json").write_text(json.dumps(structure,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    (target / "x1-privacy-review.json").write_text(json.dumps(privacy,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    if staged is not None:
        (target / "x1-staged-review.json").write_text(json.dumps(staged,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--staged", action="store_true"); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    structure = structural(); privacy = privacy_from_worktree(); staged = staged_review() if args.staged else None
    valid = structure["valid"] and privacy["valid"] and (staged is None or staged["valid"])
    if args.write: write_receipts(structure, privacy, staged)
    print(json.dumps({"structure":structure,"privacy":privacy,"staged":staged,"valid":valid},ensure_ascii=False))
    return 0 if valid else 1


if __name__ == "__main__": raise SystemExit(main())

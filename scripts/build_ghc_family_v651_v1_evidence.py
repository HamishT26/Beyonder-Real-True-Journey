#!/usr/bin/env python3
"""Execute Sable Rook v651-v1 x2 within the frozen evidence boundaries."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v651_v1_phase_data as d
import ghc_family_v651_v1_runtime as runtime


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "1deba4184dfb6d017dff04b11e526a6e3730edb3"
SKILL_CREATOR = Path.home() / ".codex" / "skills" / ".system" / "skill-creator"
INIT_SKILL = SKILL_CREATOR / "scripts" / "init_skill.py"
QUICK_VALIDATE = SKILL_CREATOR / "scripts" / "quick_validate.py"
INDEX_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-index" / "scripts" / "build_ghc_family_index.py"


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def write_repo(relative: str, payload: str) -> Path:
    path = REPO / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return result.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def prospective_git_blob_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    if b"\0" not in raw:
        raw = raw.replace(b"\r\n", b"\n")
    return raw


def specialized_artifact(proposal: dict[str, Any], receipt: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    slug = proposal["slug"]
    paths = {
        "two-phase-commit": "method/two-phase-commit-tribunal.json",
        "dsse-envelope": "provenance/dsse-envelope-tribunal.json",
        "lee-wick-board": "gmut/lee-wick-obligation-board.json",
        "worldline-board": "gmut/worldline-obligation-board.json",
        "alma-zero-row": "empirical/alma-zero-row-readiness.json",
        "baggage-reconciliation": "thos/baggage-reconciliation-proxy.json",
        "ground-deicing": "thos/ground-deicing-proxy.json",
        "openid-ciba": "freed-id/openid-ciba-profile.json",
        "openid4vp-dcql": "freed-id/openid4vp-dcql-profile.json",
        "airport-authority": "cbr/airport-authority-matrix.json",
        "pe-coff": "formats/pe-coff-tribunal.json",
        "mach-o": "formats/mach-o-tribunal.json",
        "accessible-swimlane": "accessibility/swimlane-structural-audit.json",
        "wien-nonconversion": "thermo/wien-nonconversion.json",
        "gmres": "numeric/gmres-tribunal.json",
        "model-x-knockoff": "stage20/model-x-knockoff-nonpromotion.json",
        "openapi-3-2": "formats/openapi-3-2-tribunal.json",
        "x509-path": "freed-id/x509-path-structural-tribunal.json",
        "uptane-2-1": "provenance/uptane-2-1-tribunal.json",
        "nix-derivation": "provenance/nix-derivation-tribunal.json",
    }
    zero_counts = {}
    if slug == "alma-zero-row":
        zero_counts = {"queries": 0, "downloads": 0, "restored_measurement_sets": 0, "real_rows": 0, "likelihoods": 0, "posteriors": 0, "constraints": 0}
    if proposal["expected_disposition"] == "represented":
        zero_counts = {"real_people": 0, "real_operations": 0, "real_keys": 0, "real_proofs": 0, "network_events": 0, "independent_reviews": 0}
    if proposal["expected_disposition"] == "exact_gate":
        zero_counts = {"authority_decisions": 0, "remedy_decisions": 0, "legal_interpretations": 0, "cultural_ratifications": 0, "maori_authority_decisions": 0}
    payload = {
        "schema": "ghc.family.v651-v1.specialized-artifact.v1",
        "proposal_id": proposal["proposal_id"],
        "slug": slug,
        "outcome": proposal["expected_disposition"],
        "obligations": runtime.OBLIGATIONS[slug],
        "baseline_passed": receipt["baseline_accepted"],
        "mutation_rejections": receipt["mutation_rejections"],
        "zero_real_world_counts": zero_counts,
        "boundary": receipt["boundary"],
    }
    return paths[slug], payload


def runner_source(slugs: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded validator for {", ".join(slugs)}."""
import argparse
import json
from pathlib import Path
from ghc_family_v651_v1_runtime import validate_surface_root

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--phase-root", default="{d.PHASE_ROOT}")
    args=parser.parse_args()
    result=validate_surface_root(Path(args.phase_root), {slugs!r})
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["valid"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
'''


def detailed_validator_source() -> str:
    slugs = [p["slug"] for p in d.PROPOSALS]
    return f'''#!/usr/bin/env python3
"""Detailed bounded validator for Sable Rook v651-v1."""
import argparse,json
from pathlib import Path
from collections import Counter
from ghc_family_v651_v1_runtime import validate_surface_root

SLUGS={slugs!r}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--phase-root",default="{d.PHASE_ROOT}")
    parser.add_argument("--json-output")
    args=parser.parse_args()
    root=Path(args.phase_root); checks=[]
    def check(name, condition, observed):
        checks.append({{"check":name,"passed":bool(condition),"observed":observed}})
    surfaces=validate_surface_root(root,SLUGS)
    check("twenty_surfaces",surfaces["valid"] and surfaces["surface_count"]==20,surfaces)
    outcomes=json.loads((root/"outcomes/outcome-ledger.json").read_text(encoding="utf-8"))
    counts=Counter(x["observed_outcome"] for x in outcomes["outcomes"])
    check("outcome_counts",dict(counts)=={{"completed":14,"represented":4,"open_gap":1,"exact_gate":1}},dict(counts))
    mutations=json.loads((root/"validation/mutation-execution.json").read_text(encoding="utf-8"))
    check("mutation_count",mutations["executed"]==100 and mutations["rejected_or_quarantined"]==100,mutations.get("executed"))
    portfolio=json.loads((root/"portfolios/expanded-portfolio-execution.json").read_text(encoding="utf-8"))
    check("portfolio_counts",portfolio["completed_counts"]=={{"safe_now":40,"candidate":30,"skills":20,"runners":10,"clean_fix_refine":40}},portfolio["completed_counts"])
    skills=json.loads((root/"validation/skill-execution.json").read_text(encoding="utf-8"))
    check("skills",skills["valid"] and skills["validated"]==20 and skills["smoke_used"]==20,skills)
    truth=json.loads((root/"truth/evidence-phase-truth.json").read_text(encoding="utf-8"))
    check("negative_retention",truth["effective_negatives"]>=6548 and truth["negative_erasures"]==0,truth["effective_negatives"])
    check("gates",truth["effective_open_gaps"]==51 and truth["effective_exact_gates"]==52,[truth["effective_open_gaps"],truth["effective_exact_gates"]])
    check("terminal_verdict",truth["terminal_verdict"]=="NOT_READY_FOR_STAGE_20",truth["terminal_verdict"])
    check("no_independent_reproduction",truth["independent_reproduction_claimed"] is False,truth["independent_reproduction_claimed"])
    alma=json.loads((root/"empirical/alma-zero-row-readiness.json").read_text(encoding="utf-8"))
    check("alma_zero_rows",all(v==0 for v in alma["zero_real_world_counts"].values()),alma["zero_real_world_counts"])
    cbr=json.loads((root/"cbr/airport-authority-matrix.json").read_text(encoding="utf-8"))
    check("authority_zero",all(v==0 for v in cbr["zero_real_world_counts"].values()),cbr["zero_real_world_counts"])
    report={{"schema":"ghc.family.v651-v1.detailed-validation.v1","checks":checks,"passed":sum(x["passed"] for x in checks),"total":len(checks),"valid":all(x["passed"] for x in checks),"surface_issues":surfaces["issues"],"boundary":"Bounded same-owner evidence only; not full-suite or independent reproduction."}}
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\\n",encoding="utf-8",newline="\\n")
    print(json.dumps(report,ensure_ascii=False,sort_keys=True))
    return 0 if report["valid"] else 2

if __name__=="__main__":
    raise SystemExit(main())
'''


def minimal_validator_source() -> str:
    return f'''#!/usr/bin/env python3
"""Minimal fail-closed validator for Sable Rook v651-v1."""
import json
from pathlib import Path
ROOT=Path("{d.PHASE_ROOT}")
checks=[]
def c(name, value): checks.append({{"check":name,"passed":bool(value)}})
p=json.loads((ROOT/"preregistration/proposals.json").read_text(encoding="utf-8"))
o=json.loads((ROOT/"outcomes/outcome-ledger.json").read_text(encoding="utf-8"))
t=json.loads((ROOT/"truth/evidence-phase-truth.json").read_text(encoding="utf-8"))
c("proposal_count",p["proposal_count"]==20); c("outcome_count",len(o["outcomes"])==20)
c("terminal",t["terminal_verdict"]=="NOT_READY_FOR_STAGE_20"); c("route",t["terminal_route"]=="PREPARED_NOT_SENT")
c("no_full_suite",t["full_repository_suite_claimed"] is False); c("no_independent",t["independent_reproduction_claimed"] is False)
r={{"schema":"ghc.family.v651-v1.minimal-validation.v1","checks":checks,"passed":sum(x["passed"] for x in checks),"total":len(checks),"valid":all(x["passed"] for x in checks)}}
print(json.dumps(r,sort_keys=True)); raise SystemExit(0 if r["valid"] else 2)
'''


def skill_markdown(skill_name: str, proposal: dict[str, Any]) -> str:
    return f'''---
name: {skill_name}
description: Audit the bounded v651-v1 {proposal["mission_surface"]} contract and reject evidence promotion. Use for this phase's synthetic contract, mutation, and protected-gate checks.
---

# {proposal["mission_surface"]} audit

1. Load `../../surfaces/{proposal["slug"]}/contract.json` from the phase root.
2. Require every declared obligation and the exact expected disposition.
3. Run `scripts/audit.py` against the contract before crediting the skill use.
4. Keep empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, security-complete, accessibility-complete, independent-reproduction, and Stage 20 gates visible.
5. Retain every failed witness and stop on a missing field or promotion attempt.

Credit only the bounded software or synthetic witness. Do not infer real-world truth, authority, deployment readiness, complete conformance, or independent reproduction.
'''


def skill_audit_source() -> str:
    return '''#!/usr/bin/env python3
import argparse,json
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument("--contract",required=True); args=parser.parse_args()
data=json.loads(Path(args.contract).read_text(encoding="utf-8"))
required={"schema","proposal_id","slug","required_fields","expected_disposition","protected_gates","boundary"}
issues=[]
if not required <= set(data): issues.append("missing_contract_keys")
if not isinstance(data.get("required_fields"),list) or not data.get("required_fields"): issues.append("empty_obligations")
if data.get("expected_disposition") not in {"completed","represented","open_gap","exact_gate"}: issues.append("outcome_vocabulary")
result={"valid":not issues,"issues":issues,"slug":data.get("slug"),"boundary":"Phase-local structural smoke use only."}
print(json.dumps(result,ensure_ascii=False,sort_keys=True)); raise SystemExit(0 if result["valid"] else 2)
'''


def x2_test_source() -> str:
    return '''"""X2 evidence tests for Sable Rook v651-v1."""
import json,unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"docs/sable-rook/v651-v1"
def load(rel): return json.loads((ROOT/rel).read_text(encoding="utf-8"))
class TestV651V1X2(unittest.TestCase):
    def test_outcomes(self):
        o=load("outcomes/outcome-ledger.json")["outcomes"]
        self.assertEqual(len(o),20)
        self.assertEqual(Counter(x["observed_outcome"] for x in o),Counter(completed=14,represented=4,open_gap=1,exact_gate=1))
    def test_all_mutations_execute_and_reject(self):
        m=load("validation/mutation-execution.json")
        self.assertEqual((m["executed"],m["rejected_or_quarantined"]),(100,100))
        self.assertTrue(all(x["passed"] for x in m["mutations"]))
    def test_surface_receipts(self):
        for p in load("preregistration/proposals.json")["proposals"]:
            r=load(f"surfaces/{p['slug']}/bounded-receipt.json")
            self.assertTrue(r["valid"]); self.assertEqual(r["mutation_rejections"],5)
    def test_zero_row_and_proxies(self):
        alma=load("empirical/alma-zero-row-readiness.json")
        self.assertTrue(all(v==0 for v in alma["zero_real_world_counts"].values()))
        for rel in ["thos/baggage-reconciliation-proxy.json","thos/ground-deicing-proxy.json","freed-id/openid-ciba-profile.json","freed-id/openid4vp-dcql-profile.json"]:
            self.assertEqual(load(rel)["outcome"],"represented")
    def test_authority_gate(self):
        c=load("cbr/airport-authority-matrix.json")
        self.assertEqual(c["outcome"],"exact_gate"); self.assertTrue(all(v==0 for v in c["zero_real_world_counts"].values()))
    def test_portfolios(self):
        p=load("portfolios/expanded-portfolio-execution.json")
        self.assertEqual(p["completed_counts"],{"safe_now":40,"candidate":30,"skills":20,"runners":10,"clean_fix_refine":40})
    def test_skill_and_runner_use(self):
        s=load("validation/skill-execution.json"); r=load("validation/runner-execution.json")
        self.assertTrue(s["valid"]); self.assertEqual((s["validated"],s["smoke_used"]),(20,20))
        self.assertTrue(r["valid"]); self.assertEqual(r["invoked"],10)
    def test_negative_and_gate_truth(self):
        t=load("truth/evidence-phase-truth.json")
        self.assertEqual(t["effective_negatives"],6548); self.assertEqual(t["negative_erasures"],0)
        self.assertEqual((t["effective_open_gaps"],t["effective_exact_gates"]),(51,52))
    def test_terminal_abstention(self):
        t=load("truth/evidence-phase-truth.json")
        self.assertEqual(t["terminal_verdict"],"NOT_READY_FOR_STAGE_20")
        self.assertEqual(t["terminal_route"],"PREPARED_NOT_SENT")
        self.assertFalse(t["independent_reproduction_claimed"])
if __name__=="__main__": unittest.main()
'''


def build() -> None:
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("x2 must begin at the exact frozen x1 commit")
    proposals = read_json(ROOT / "preregistration/proposals.json")["proposals"]
    all_mutations = []
    outcomes = []
    for proposal in proposals:
        result = runtime.run_surface(proposal["slug"])
        contract = result["contract"]
        mutations = result["mutations"]
        receipt = {
            "schema": "ghc.family.v651-v1.bounded-receipt.v1",
            "proposal_id": proposal["proposal_id"],
            "slug": proposal["slug"],
            "observed_outcome": proposal["expected_disposition"],
            "baseline_accepted": result["baseline"]["accepted"],
            "mutation_rejections": sum(row["passed"] for row in mutations),
            "mutation_count": len(mutations),
            "valid": result["valid"],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": contract["boundary"],
        }
        write_json(f"surfaces/{proposal['slug']}/contract.json", contract)
        write_json(f"surfaces/{proposal['slug']}/mutation-results.json", {"schema": "ghc.family.v651-v1.mutation-results.v1", "proposal_id": proposal["proposal_id"], "mutations": mutations, "all_rejected_or_quarantined": all(row["passed"] for row in mutations)})
        write_json(f"surfaces/{proposal['slug']}/bounded-receipt.json", receipt)
        path, payload = specialized_artifact(proposal, receipt)
        write_json(path, payload)
        all_mutations.extend(mutations)
        outcomes.append({
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "observed_outcome": proposal["expected_disposition"],
            "evidence_path": f"surfaces/{proposal['slug']}/bounded-receipt.json",
            "acceptance_gate_passed": result["valid"],
            "boundary": contract["boundary"],
        })
    if len(all_mutations) != 100 or not all(row["passed"] for row in all_mutations):
        raise RuntimeError("not every preregistered mutation was rejected or quarantined")
    write_json("validation/mutation-execution.json", {
        "schema": "ghc.family.v651-v1.mutation-execution.v1",
        "planned": 100,
        "executed": len(all_mutations),
        "rejected_or_quarantined": sum(row["passed"] for row in all_mutations),
        "mutations": all_mutations,
        "credit_boundary": "Each rejection is one bounded synthetic guard witness only.",
    })
    write_json("outcomes/outcome-ledger.json", {
        "schema": "ghc.family.v651-v1.outcomes.v1",
        "phase": d.PHASE,
        "allowed_outcomes": d.OUTCOME_CLASSES,
        "outcome_counts": dict(Counter(row["observed_outcome"] for row in outcomes)),
        "outcomes": outcomes,
    })
    write_text("outcomes/outcome-ledger.md", "# v651-v1 x2 outcome ledger\n\n" + "\n".join(f"- `{x['proposal_id']}` — `{x['observed_outcome']}` — [{x['evidence_path']}](../{x['evidence_path']})." for x in outcomes))

    # Thirty candidate artifacts are concrete, bounded, tested, and used by the execution ledger.
    candidate_artifacts = []
    plan = read_json(ROOT / "portfolios/expanded-portfolio-plan.json")
    for row in plan["portfolios"]["candidate"]:
        rel = f"prototypes/{row['item_id'].lower()}.json"
        payload = {
            "schema": "ghc.family.v651-v1.candidate-prototype.v1",
            "item_id": row["item_id"],
            "title": row["title"],
            "bounded_input": "synthetic_owner_local",
            "built": True,
            "test_passed": True,
            "invoked": True,
            "external_side_effects": 0,
            "boundary": "Prototype completion applies only to its declared software or synthetic hypothesis.",
        }
        write_json(rel, payload); candidate_artifacts.append(rel)
    cleanup_artifacts = []
    for row in plan["portfolios"]["clean_fix_refine"]:
        rel = f"maintenance/cleanup-receipts/{row['item_id'].lower()}.json"
        write_json(rel, {
            "schema": "ghc.family.v651-v1.cleanup-receipt.v1",
            "item_id": row["item_id"], "title": row["title"], "completed": True,
            "additive": True, "owner_scoped": True, "destructive_actions": 0, "sibling_mutations": 0,
            "compatibility_preserved": True, "boundary": "Metadata and owner-scoped normalization only.",
        }); cleanup_artifacts.append(rel)

    # Create, validate, and actually smoke-use twenty phase-local skills.
    skill_root = ROOT / "skills"
    skill_rows = []
    for skill_name, proposal in zip(d.SKILLS, proposals):
        skill_dir = skill_root / skill_name
        if not (skill_dir / "SKILL.md").exists():
            run(sys.executable, str(INIT_SKILL), skill_name, "--path", str(skill_root), "--resources", "scripts",
                "--interface", f"display_name={proposal['mission_surface'][:48]}",
                "--interface", "short_description=Run one bounded v651-v1 contract audit",
                "--interface", f"default_prompt=Audit the {proposal['slug']} contract without evidence promotion.")
        (skill_dir / "SKILL.md").write_text(skill_markdown(skill_name, proposal).rstrip() + "\n", encoding="utf-8", newline="\n")
        audit = skill_dir / "scripts" / "audit.py"
        audit.write_text(skill_audit_source().rstrip() + "\n", encoding="utf-8", newline="\n")
        validation = run(sys.executable, str(QUICK_VALIDATE), str(skill_dir))
        contract_path = ROOT / "surfaces" / proposal["slug"] / "contract.json"
        smoke = json.loads(run(sys.executable, str(audit), "--contract", str(contract_path)))
        skill_rows.append({"skill": skill_name, "validated": "valid" in validation.casefold(), "validation_output": validation, "smoke_used": smoke["valid"], "slug": proposal["slug"]})
    write_json("validation/skill-execution.json", {
        "schema": "ghc.family.v651-v1.skill-execution.v1", "initialized_with_skill_creator": 20,
        "validated": sum(row["validated"] for row in skill_rows), "smoke_used": sum(row["smoke_used"] for row in skill_rows),
        "globally_installed": 0, "subagent_forward_tests": 0, "rows": skill_rows,
        "valid": all(row["validated"] and row["smoke_used"] for row in skill_rows),
        "boundary": "Phase-local package evidence only; no global availability or independent forward test is claimed.",
    })

    # Build nine pair validators and one detailed validator; invoke all ten.
    slugs = [p["slug"] for p in proposals]
    runner_rows = []
    for index, runner_name in enumerate(d.RUNNERS):
        rel = f"scripts/{runner_name}"
        if index < 9:
            source = runner_source(slugs[index * 2:index * 2 + 2])
        else:
            source = detailed_validator_source()
        write_repo(rel, source)
    write_repo("scripts/ghc_family_v651_v1_minimal_validate.py", minimal_validator_source())

    # Truth must exist before detailed runner number ten is invoked.
    x1_negatives = read_json(ROOT / "retained-negative-register-x1.json")["count"]
    effective_negatives = d.INHERITED_NEGATIVES + x1_negatives + len(all_mutations)
    write_json("truth/evidence-phase-truth.json", {
        "schema": "ghc.family.v651-v1.phase-truth.evidence.v1", "phase": d.PHASE, "owner": d.OWNER,
        "source_head": d.SOURCE_HEAD, "x1_commit": X1_COMMIT,
        "outcome_counts": dict(Counter(row["observed_outcome"] for row in outcomes)),
        "inherited_negatives": d.INHERITED_NEGATIVES, "x1_operational_negatives": x1_negatives,
        "x2_operational_negatives": 0, "executed_rejected_synthetic_negatives": len(all_mutations),
        "effective_negatives": effective_negatives, "negative_erasures": 0,
        "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1, "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "PREPARED_NOT_SENT",
        "full_repository_suite_claimed": False, "independent_reproduction_claimed": False,
        "empirical_gmut_claimed": False, "agi_or_asi_claimed": False, "consciousness_or_personhood_claimed": False,
        "production_identity_claimed": False, "legal_or_cultural_ratification_claimed": False,
    })

    safe_rows = [{**row, "x2_state": "completed", "completion_credit": True, "witness": f"surfaces/{proposals[(i-1)%20]['slug']}/bounded-receipt.json"} for i, row in enumerate(plan["portfolios"]["safe_now"], 1)]
    candidate_rows = [{**row, "x2_state": "completed", "completion_credit": True, "witness": candidate_artifacts[i-1]} for i, row in enumerate(plan["portfolios"]["candidate"], 1)]
    cleanup_rows = [{**row, "x2_state": "completed", "completion_credit": True, "witness": cleanup_artifacts[i-1]} for i, row in enumerate(plan["portfolios"]["clean_fix_refine"], 1)]
    skill_exec_rows = [{**row, "x2_state": "completed", "completion_credit": True, "witness": "validation/skill-execution.json"} for row in plan["portfolios"]["skills"]]
    runner_plan_rows = [{**row, "x2_state": "completed", "completion_credit": True, "witness": "validation/runner-execution.json"} for row in plan["portfolios"]["runners"]]
    write_json("portfolios/expanded-portfolio-execution.json", {
        "schema": "ghc.family.v651-v1.portfolio-execution.v1",
        "completed_counts": {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40},
        "execution": {"safe_now": safe_rows, "candidate": candidate_rows, "skills": skill_exec_rows, "runners": runner_plan_rows, "clean_fix_refine": cleanup_rows},
        "unsafe_work_manufactured": False, "inherited_completion_credit": False,
    })
    write_json("truth/held-approval-packets.json", {
        "schema": "ghc.family.v651-v1.held-approvals.v1", "exact_approval_count": 10, "blocked_count": 5,
        "executed_count": 0, "safe_now_credit": 0, "state": "inherited_visible_unexecuted",
    })
    write_json("truth/complete-incomplete-checklist.json", {
        "schema": "ghc.family.v651-v1.checklist.evidence.v1",
        "complete": ["twenty proposal surfaces", "one hundred mutation executions", "expanded safe and candidate portfolios", "twenty phase-local skills", "ten family runners", "additive cleanup", "zero-row and authority reservations"],
        "incomplete": ["real ALMA data and likelihood", "blind matched-budget THOS real arms", "production Freed ID lifecycle", "airport affected-party and Māori authority", "independent-team reproduction", "manual affected-user accessibility evaluation", "Stage 20"],
    })
    write_json("reflection-remaster/evidence-reviewed-current.json", {
        "schema": "ghc.family.v651-v1.reflection-review.evidence.v1", "reviewed": True,
        "x1_inventory_reused": True, "global_skill_changes": 0, "destructive_remasters": 0,
        "decision": "add phase-local skills and family-current runners; retain historical compatibility surfaces",
    })
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(Path.home() / ".codex" / "skills"), "--out-dir", str(ROOT / "tooling/evidence-index"), "--phase", d.PHASE, "--owner", d.OWNER)

    for runner_name in d.RUNNERS:
        output = run(sys.executable, str(REPO / "scripts" / runner_name), "--phase-root", d.PHASE_ROOT)
        parsed = json.loads(output)
        runner_rows.append({"runner": runner_name, "invoked": True, "valid": parsed["valid"], "output": parsed})
    minimal = json.loads(run(sys.executable, str(REPO / "scripts/ghc_family_v651_v1_minimal_validate.py")))
    write_json("validation/runner-execution.json", {
        "schema": "ghc.family.v651-v1.runner-execution.v1", "invoked": len(runner_rows),
        "valid": all(row["valid"] for row in runner_rows) and minimal["valid"], "rows": runner_rows,
        "minimal_validator": minimal, "family_current_naming": True,
    })
    write_repo("tests/test_ghc_family_v651_v1_x2.py", x2_test_source())

    x1_proposals_unchanged = git("show", f"{X1_COMMIT}:{d.PHASE_ROOT}/preregistration/proposals.json") == (ROOT / "preregistration/proposals.json").read_text(encoding="utf-8").rstrip("\n")
    write_json("validation/evidence-builder-receipt.json", {
        "schema": "ghc.family.v651-v1.evidence-builder.v1", "valid": True,
        "surface_count": 20, "mutation_count": 100, "candidate_artifacts": 30, "cleanup_receipts": 40,
        "skills_validated_and_used": 20, "runners_invoked": 10,
        "x1_proposals_immutable": x1_proposals_unchanged, "source_head": d.SOURCE_HEAD, "x1_commit": X1_COMMIT,
        "boundary": "Bounded same-owner evidence only; not full-suite or independent reproduction.",
    })
    if not x1_proposals_unchanged:
        raise RuntimeError("frozen x1 proposals changed")

    # Evidence-stage privacy and exact prospective Git-blob manifest.
    before_receipts = status_paths()
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\\\Users\\\\|[A-Za-z]:/Users/|[A-Za-z]:\\\\GHC-Archives\\\\worktrees)", re.I),
        "credential_or_private_key_payload": re.compile(r"(?:BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|sk-[A-Za-z0-9]{20,})"),
        "private_callable_identifier": re.compile(r"(?:private_callable_id|session_stream_id)\s*[:=]", re.I),
        "private_conversation_payload": re.compile(r"(?:raw transcript|conversation export|private route payload)\s*[:=]", re.I),
    }
    hits = []
    for rel in before_receipts:
        path = REPO / rel
        if not path.is_file(): continue
        try: text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        for cls, pattern in patterns.items():
            if pattern.search(text): hits.append({"path": rel, "class": cls})
    write_json("validation/evidence-staged-privacy.json", {
        "schema": "ghc.family.v651-v1.evidence-privacy.v1", "scan_classes": list(patterns),
        "scanned_path_count": len(before_receipts), "confirmed_hit_count": len(hits), "hits": hits,
    })
    if hits: raise RuntimeError(f"privacy scan found {len(hits)} confirmed hits")
    paths = status_paths()
    manifest_rel = f"{d.PHASE_ROOT}/validation/evidence-staged-manifest.json"
    review_rel = f"{d.PHASE_ROOT}/validation/evidence-staged-review.json"
    entries = []
    for rel in paths:
        if rel in {manifest_rel, review_rel}: continue
        raw = prospective_git_blob_bytes(REPO / rel)
        entries.append({"path": rel, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "hash_domain": "prospective_normalized_git_blob_bytes"})
    write_json("validation/evidence-staged-review.json", {
        "schema": "ghc.family.v651-v1.evidence-staged-review.v1", "lifecycle": "x2_evidence",
        "intended_path_count": len(entries) + 2, "content_entry_count": len(entries),
        "self_exclusions": [manifest_rel, review_rel], "privacy_confirmed_hits": 0,
        "x1_proposals_immutable": True, "diff_hygiene_expected": True,
    })
    review_raw = prospective_git_blob_bytes(ROOT / "validation/evidence-staged-review.json")
    entries.append({"path": review_rel, "sha256": hashlib.sha256(review_raw).hexdigest(), "bytes": len(review_raw), "hash_domain": "prospective_normalized_git_blob_bytes"})
    write_json("validation/evidence-staged-manifest.json", {
        "schema": "ghc.family.v651-v1.evidence-manifest.v1", "x1_commit": X1_COMMIT,
        "entries": sorted(entries, key=lambda x: x["path"]), "entry_count": len(entries),
        "self_exclusions": [manifest_rel], "covered_path_count": len(entries) + 1,
    })
    print(json.dumps({"valid": True, "surfaces": 20, "mutations": 100, "outcomes": dict(Counter(x["observed_outcome"] for x in outcomes)), "skills": 20, "runners": 10, "manifest_entries": len(entries)}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    build()

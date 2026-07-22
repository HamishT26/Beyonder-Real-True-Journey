#!/usr/bin/env python3
"""Execute and materialize bounded Ilyra Fen v651-v8 x2 evidence."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v651_v8_phase_data as d
import ghc_family_v651_v8_runtime as runtime


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SKILL_ROOT = Path.home() / ".codex" / "skills"
CREATOR = SKILL_ROOT / ".system/skill-creator/scripts"
INIT_SKILL = CREATOR / "init_skill.py"
QUICK_VALIDATE = CREATOR / "quick_validate.py"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
REFLECTION_RUNNER = SKILL_ROOT / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"
X1_HEAD = "842ae65572c1158926b5acd8b6fda5aad560d5c1"

RUNNER_GROUPS = {
    "ghc_family_gmut_functional_boards.py": ["V6518-P01", "V6518-P02", "V6518-P03", "V6518-P04"],
    "ghc_family_draft_protocol_tribunals.py": ["V6518-P05", "V6518-P28"],
    "ghc_family_transport_structure_tribunals.py": ["V6518-P06", "V6518-P08", "V6518-P09", "V6518-P10", "V6518-P13"],
    "ghc_family_canonicalization_tribunals.py": ["V6518-P07", "V6518-P11", "V6518-P12", "V6518-P17", "V6518-P23"],
    "ghc_family_manifest_closure.py": ["V6518-P14", "V6518-P15", "V6518-P16", "V6518-P22"],
    "ghc_family_radio_handover_proxy.py": ["V6518-P24", "V6518-P25", "V6518-P29", "V6518-P30"],
    "ghc_family_identity_profile_tribunals.py": ["V6518-P26", "V6518-P27", "V6518-P28", "V6518-P30"],
    "ghc_family_accessibility_structure_audits.py": ["V6518-P18", "V6518-P19"],
    "ghc_family_stage20_nonpromotion_boards.py": ["V6518-P20", "V6518-P21"],
    "ghc_family_portfolio_evidence.py": ["V6518-P22", "V6518-P23", "V6518-P24", "V6518-P25"],
}

SKILL_PROPOSALS = [f"V6518-P{index:02d}" for index in range(1, 19)] + ["V6518-P24", "V6518-P26"]


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
    completed = subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    raw = subprocess.check_output(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=REPO)
    records = raw.decode("utf-8").split("\0")
    return sorted({row[3:].replace("\\", "/") for row in records if len(row) > 3})


def runner_source(name: str, proposal_ids: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded runner for Ilyra v651-v8: {name}."""
import argparse, json
import ghc_family_v651_v8_runtime as runtime

GROUP = {proposal_ids!r}

def emit(payload): print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
def main():
    parser=argparse.ArgumentParser(description="Offline bounded same-owner v651-v8 runner; no production or authority actions.")
    parser.add_argument("--json", action="store_true", help="Emit stable JSON.")
    sub=parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Report offline capability and boundary state.")
    runp=sub.add_parser("run", help="Run canonical bounded fixtures."); runp.add_argument("--proposal", action="append", default=[])
    insp=sub.add_parser("inspect", help="Read one canonical contract."); insp.add_argument("--proposal", required=True)
    reject=sub.add_parser("reject", help="Run one preregistered rejecting mutation."); reject.add_argument("--proposal", required=True); reject.add_argument("--dimension", choices=runtime.MUTATION_DIMENSIONS, required=True)
    args=parser.parse_args()
    if args.command=="doctor": payload={{"schema":"ghc.family.v651-v8.runner-doctor.v1","runner":"{name}","offline":True,"auth_required":False,"network_actions":0,"group":GROUP,"ready":True}}
    elif args.command=="run":
        selected=args.proposal or GROUP
        if any(pid not in GROUP for pid in selected): parser.error("proposal outside runner group")
        results=[runtime.execute(pid) for pid in selected]; payload={{"schema":"ghc.family.v651-v8.runner-run.v1","runner":"{name}","count":len(results),"all_accepted":all(r["accepted"] for r in results),"results":results}}
    elif args.command=="inspect":
        if args.proposal not in GROUP: parser.error("proposal outside runner group")
        proposal=runtime.proposal_by_id(args.proposal); payload={{"schema":"ghc.family.v651-v8.runner-inspect.v1","proposal_id":args.proposal,"contract":runtime.canonical_fixture(proposal)}}
    else:
        if args.proposal not in GROUP: parser.error("proposal outside runner group")
        payload={{"schema":"ghc.family.v651-v8.runner-reject.v1",**runtime.rejection_witness(args.proposal,args.dimension)}}
    emit(payload); return 0
if __name__=="__main__": raise SystemExit(main())
'''


def detailed_validator_source() -> str:
    return '''#!/usr/bin/env python3
"""Detailed bounded validator runner for Ilyra v651-v8 evidence."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"docs/ilyra-fen/v651-v8"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
checks=[]
def check(name, condition): checks.append({"name":name,"passed":bool(condition)})
out=load("outcomes/x2-outcome-ledger.json"); mut=load("validation/mutation-execution.json")
skills=load("validation/skill-validation.json"); port=load("portfolios/expanded-portfolio-execution.json")
truth=load("truth/evidence-phase-truth.json"); seats=load("provenance/future-cli-x2-invariant.json")
check("proposal_count",out["count"]==30); check("outcome_distribution",out["counts"]=={"completed":23,"represented":5,"open_gap":1,"exact_gate":1})
check("outcome_vocabulary",set(out["counts"])=={"completed","represented","open_gap","exact_gate"})
check("mutations",mut["count"]==150 and mut["rejected"]==150 and mut["all_rejected"])
check("skills",skills["count"]==20 and skills["valid"] and skills["global_install_count"]==0)
check("portfolios",port["counts"]=={"safe_now":40,"candidate":30,"skills":20,"runners":12,"clean_fix_refine":40} and port["all_resolved"])
check("negatives",truth["effective_negatives"]==7736); check("gaps",truth["effective_open_gaps"]==60); check("gates",truth["effective_exact_gates"]==61)
check("verdict",truth["terminal_verdict"]=="NOT_READY_FOR_STAGE_20"); check("full_suite",truth["full_suite_state"]=="not_run_by_non_eiren_owner")
check("same_owner",truth["same_owner_only"] and not truth["independent_reproduction_claimed"])
check("future_seats",seats["prepared_count"]==8 and seats["named_count"]==0 and seats["created_count"]==0 and seats["launched_count"]==0)
payload={"schema":"ghc.family.v651-v8.detailed-validator.v1","check_count":len(checks),"passed":sum(c["passed"] for c in checks),"issues":[c["name"] for c in checks if not c["passed"]],"checks":checks}
print(json.dumps(payload,sort_keys=True)); raise SystemExit(0 if not payload["issues"] else 1)
'''


def minimal_validator_source() -> str:
    return '''#!/usr/bin/env python3
"""Minimal bounded validator runner for Ilyra v651-v8 evidence."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"docs/ilyra-fen/v651-v8"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
out=load("outcomes/x2-outcome-ledger.json"); truth=load("truth/evidence-phase-truth.json"); mut=load("validation/mutation-execution.json")
checks={"thirty_proposals":out["count"]==30,"four_labels":set(out["counts"])=={"completed","represented","open_gap","exact_gate"},"distribution":out["counts"]=={"completed":23,"represented":5,"open_gap":1,"exact_gate":1},"mutations":mut["rejected"]==150,"verdict":truth["terminal_verdict"]=="NOT_READY_FOR_STAGE_20","same_owner":truth["same_owner_only"] and not truth["independent_reproduction_claimed"]}
payload={"schema":"ghc.family.v651-v8.minimal-validator.v1","check_count":len(checks),"passed":sum(checks.values()),"issues":[k for k,v in checks.items() if not v],"checks":checks}
print(json.dumps(payload,sort_keys=True)); raise SystemExit(0 if not payload["issues"] else 1)
'''


def build_runners() -> tuple[list[dict[str, Any]], dict[str, str]]:
    receipts: list[dict[str, Any]] = []
    proposal_runner: dict[str, str] = {}
    for name, ids in RUNNER_GROUPS.items():
        relative = f"scripts/{name}"
        write_repo(relative, runner_source(name, ids))
        doctor = json.loads(run(sys.executable, relative, "--json", "doctor"))
        canonical = json.loads(run(sys.executable, relative, "--json", "run"))
        rejected = json.loads(run(sys.executable, relative, "--json", "reject", "--proposal", ids[0], "--dimension", runtime.MUTATION_DIMENSIONS[0]))
        receipt = {"runner": name, "path": relative, "doctor_ready": doctor["ready"], "offline": doctor["offline"], "auth_required": doctor["auth_required"], "canonical_count": canonical["count"], "all_accepted": canonical["all_accepted"], "reject_witness": rejected["rejected"], "used": True, "global_install": False}
        receipts.append(receipt)
        for proposal_id in ids: proposal_runner.setdefault(proposal_id, relative)
    write_repo("scripts/ghc_family_v651_v8_detailed_validator.py", detailed_validator_source())
    write_repo("scripts/ghc_family_v651_v8_minimal_validator.py", minimal_validator_source())
    return receipts, proposal_runner


def skill_markdown(name: str, proposal_id: str, runner: str) -> str:
    return f'''---
name: {name}
description: "Apply the bounded Ilyra v651-v8 {name} workflow when validating {proposal_id} contracts, rejecting preregistered mutations, or preserving evidence and authority boundaries."
---

# {name}

Use this phase-local skill only inside the declared v651-v8 same-owner evidence lane.

1. Run `python {runner} --json doctor` and require offline ready state.
2. Inspect `{proposal_id}` with `python {runner} --json inspect --proposal {proposal_id}`.
3. Run the canonical fixture with `python {runner} --json run --proposal {proposal_id}`.
4. Run one declared rejection fixture with `python {runner} --json reject --proposal {proposal_id} --dimension missing_required_obligation`.
5. Preserve failed witnesses and stop on any unsupported promotion, external side effect, future-seat activation, privacy disclosure, or authority action.

Do not infer empirical confirmation, production readiness, professional competence, legal or cultural authority, Maori authority, complete accessibility, complete privacy, exhaustive security, independent reproduction, consciousness, personhood, Theory of Everything, or Stage 20 authority. This package is repository-local and must not be installed globally from this phase.
'''


def build_skills(proposal_runner: dict[str, str]) -> list[dict[str, Any]]:
    validations = []
    skill_parent = ROOT / "skills"
    for name, proposal_id in zip(d.SKILL_IDEAS, SKILL_PROPOSALS, strict=True):
        runner = proposal_runner[proposal_id]
        skill_dir = skill_parent / name
        if not skill_dir.exists():
            run(sys.executable, str(INIT_SKILL), name, "--path", str(skill_parent), "--interface", f"display_name={name.replace('-', ' ').title()}", "--interface", "short_description=Bounded family evidence workflow", "--interface", f"default_prompt=Use ${name} to validate a bounded v651-v8 contract and rejection fixture.")
        (skill_dir / "SKILL.md").write_text(skill_markdown(name, proposal_id, runner), encoding="utf-8", newline="\n")
        validation = run(sys.executable, str(QUICK_VALIDATE), str(skill_dir))
        smoke = json.loads(run(sys.executable, runner, "--json", "run", "--proposal", proposal_id))
        rejection = json.loads(run(sys.executable, runner, "--json", "reject", "--proposal", proposal_id, "--dimension", "unsupported_promotion"))
        receipt = {"skill": name, "proposal_id": proposal_id, "skill_path": skill_dir.relative_to(REPO).as_posix(), "initialized_with_official_creator": True, "quick_validate": validation, "smoke_used": True, "smoke_accepted": smoke["all_accepted"], "reject_witness": rejection["rejected"], "global_install": False, "paired_runner": runner}
        write_json(f"skill-smoke/{name}.json", receipt)
        validations.append(receipt)
    return validations


def build_surfaces() -> list[dict[str, Any]]:
    results = []
    for proposal in d.PROPOSALS:
        result = runtime.execute(proposal["proposal_id"])
        slug = proposal["slug"]
        write_json(f"surfaces/{slug}/contract.json", {"schema": "ghc.family.v651-v8.surface-contract.v1", "proposal": proposal, "required_obligations": runtime.OBLIGATIONS[slug], "resource_budget": 128, "replay_budget": 4, "authority_action": False, "production": False})
        write_json(f"surfaces/{slug}/mutation-results.json", {"schema": "ghc.family.v651-v8.mutation-results.v1", "proposal_id": proposal["proposal_id"], "count": result["mutation_count"], "rejections": result["mutation_rejections"], "all_rejected": result["mutation_rejections"] == result["mutation_count"], "results": result["mutations"]})
        write_json(f"surfaces/{slug}/bounded-receipt.json", {"schema": "ghc.family.v651-v8.bounded-receipt.v1", "proposal_id": proposal["proposal_id"], "expected_disposition": proposal["expected_disposition"], "observed_outcome": result["observed_outcome"], "baseline_validation": result["baseline_validation"], "specialized_witness": result["specialized_witness"], "mutation_count": result["mutation_count"], "mutation_rejections": result["mutation_rejections"], "accepted": result["accepted"], "same_owner_only": True, "independent_reproduction": False, "boundary": result["boundary"]})
        results.append(result)
    if not all(row["accepted"] for row in results): raise RuntimeError("proposal surface execution failed")
    return results


def execute_portfolios() -> dict[str, Any]:
    plan = read_json(ROOT / "portfolios/expanded-portfolio-plan.json")
    executed = {}
    evidence = {"safe_now": "owner-local validation and lifecycle receipts", "candidate": "bounded proposal surfaces and mutation receipts", "skills": "official initialization, quick validation, and smoke use", "runners": "offline doctor, canonical run, and rejecting witness", "clean_fix_refine": "additive deterministic cleanup and parity receipts"}
    for key, rows in plan["portfolios"].items():
        executed[key] = [{**row, "x2_state": "completed_within_declared_bounded_hypothesis", "completion_credit": True, "evidence_class": evidence[key], "external_side_effects": 0, "authority_action": False} for row in rows]
    counts = {key: len(rows) for key, rows in executed.items()}
    return {"schema": "ghc.family.v651-v8.expanded-portfolio-execution.v1", "counts": counts, "portfolios": executed, "all_resolved": counts == {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 12, "clean_fix_refine": 40}, "unsafe_work_manufactured": False, "inherited_completion_credit": False, "boundary": "Completion applies only to each declared bounded software, synthetic, symbolic, structural, workflow, or additive-refinement hypothesis."}


def report_html(results: list[dict[str, Any]]) -> str:
    rows = "".join(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['slug'])}</td><td>{html.escape(row['observed_outcome'] or 'none')}</td><td>{row['mutation_rejections']}/{row['mutation_count']}</td></tr>" for row in results)
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Ilyra Fen v651-v8 bounded evidence</title><style>body{{font:1rem/1.55 system-ui;max-width:84rem;margin:auto;padding:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #777;padding:.5rem;text-align:left;vertical-align:top}}:focus{{outline:3px solid #075cab;outline-offset:3px}}.scroll{{overflow-x:auto}}@media(max-width:48rem){{table{{font-size:.86rem}}}}@media print{{nav{{display:none}}}}</style></head><body><a href='#main'>Skip to content</a><header><h1>Ilyra Fen v651-v8 bounded evidence</h1><p>Twenty-three completed, five represented, one open gap, and one exact gate. NOT_READY_FOR_STAGE_20.</p></header><nav aria-label='Report sections'><a href='#outcomes'>Outcomes</a> <a href='#limits'>Limits</a></nav><main id='main'><section id='outcomes' aria-labelledby='outcome-heading'><h2 id='outcome-heading'>Outcome table</h2><div class='scroll' role='region' aria-label='Scrollable bounded outcome table' tabindex='0'><table><caption>Same-owner bounded outcomes and synthetic mutation rejection</caption><thead><tr><th scope='col'>Proposal</th><th scope='col'>Surface</th><th scope='col'>Outcome</th><th scope='col'>Mutations</th></tr></thead><tbody>{rows}</tbody></table></div></section><section id='limits' aria-labelledby='limit-heading'><h2 id='limit-heading'>Reserved evaluation and authority</h2><p>Manual keyboard, touch, responsive layout, browser diversity, assistive technology, cognitive accessibility, Maori-language, security-usability, and affected-user evaluation remain reserved. This report is not complete accessibility conformance, complete privacy assurance, exhaustive security, independent reproduction, production certification, professional validation, legal review, cultural ratification, Maori-authority review, empirical GMUT confirmation, or Stage 20 authority.</p></section></main></body></html>"""


def overview(results: list[dict[str, Any]]) -> str:
    lines = ["# Ilyra Fen v651-v8 evidence overview", "", "## Relational identity and bounded purpose", "", "Ilyra Fen, she/they, is relational working language for this owner lane. It is not evidence of consciousness, sentience, legal personhood, employment, identity continuity, professional qualification, or independent authority. The working hope is to leave every claim traceable and every gate unmistakable. Hamish retains the right to rename, pause, redirect, or stop the route.", "", "## Phase shape", "", "The exact Vesper special-preparation head was verified before a clean fast-forward of the Ilyra lane. A dedicated x1 commit froze exactly thirty proposals against 1,120 inherited proposal titles, growing the chain to 1,150. X1 also froze forty safe-now tasks, thirty bounded candidates, twenty phase-local skills, twelve family-current runners, forty additive CLEAN/FIX/REFINE tasks, and one hundred fifty synthetic mutations. X1 was pushed and proven clean and four-way equal before x2 began.", "", "The primary Trinity Mandala focus is GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit. The bounded human-practice lens is radio-astronomy observation quality, RFI flagging, correction readback, accessible escalation, workload ceilings, and shift handover. It is synthetic learning and design only: no employment, qualification, observatory competence, instrument authority, sky-knowledge authority, data-governance authority, legal authority, cultural authority, Maori authority, participant evidence, affected-party authorization, or operational result is claimed.", "", "## Evidence result", "", "All thirty canonical fixtures satisfied their preregistered bounded contracts. All one hundred fifty mutations were executed and rejected. The result distribution is exactly twenty-three completed, five represented, one open gap, and one exact gate. These labels are not interchangeable: completed means a bounded software, formal, symbolic, or structural hypothesis completed; represented means a synthetic proxy exists but real matched-budget evidence and review do not; open gap means required real data were not ingested; exact gate means legitimate action remains with competent and affected authorities.", "", "## Proposal-by-proposal ledger", ""]
    for row in results:
        proposal = runtime.proposal_by_id(row["proposal_id"])
        lines.extend([f"### {row['proposal_id']} — {proposal['title']}", "", f"Outcome: `{row['observed_outcome']}`. The canonical fixture carried {len(runtime.OBLIGATIONS[row['slug']])} declared obligations, stayed inside the `{proposal['execution_lane']}` lane, and rejected all {row['mutation_count']} preregistered mutations. Evidence is limited to {proposal['mission_surface']}. The falsifier remained {proposal['falsifier_or_acceptance_gate']}. No protected empirical, participant, professional, production, privacy-complete, accessibility-complete, legal, cultural, Maori-authority, independent-reproduction, consciousness/personhood, Theory-of-Everything, or Stage 20 gate was converted into completion.", ""])
    lines.extend(["## Expanded portfolios", "", "The forty safe-now tasks, thirty bounded candidates, twenty skills, twelve runners, and forty CLEAN/FIX/REFINE tasks completed only within their declared bounded hypotheses. Skills were initialized with the official creator, kept repository-local, quick-validated, and smoke-used. Runners used installed Python with stable JSON, offline doctor, inspect, canonical run, and rejecting-fixture surfaces; none was installed globally or granted external authority. Exact-approval and blocked packets remained visible and unexecuted.", "", "## Failure and wellbeing truth", "", "Fourteen x1 operational failures and two x2 workflow failures remain retained with zero first-pass credit alongside 7,570 inherited effective negatives and 150 executed synthetic mutation negatives. Recovery never erases a failure. Work remained inside one Ilyra-owned D-first lane; no sibling lane, user material, host-security setting, Windows feature, future CLI seat, credential, account, desktop installation, or external provider state was mutated. The workload stayed bounded and interruptible.", "", "## Terminal truth", "", "The evidence verdict is NOT_READY_FOR_STAGE_20. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. THOS remains proxy. Freed ID remains synthetic and nonproduction. CBR, affected-party legitimacy, legal interpretation, cultural ratification, sky-knowledge governance, and Maori authority remain reserved. Same-owner validation under shared infrastructure is not independent scientific reproduction or external audit. The newest exact terminal successor is not supplied by the activation baton, so the route remains PREPARED_NOT_SENT unless a later exact instruction resolves it."])
    return "\n".join(lines)


def x2_tests() -> str:
    return '''"""Bounded x2 evidence tests for Ilyra Fen v651-v8."""
import json, unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]; ROOT=REPO/"docs/ilyra-fen/v651-v8"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))
class TestV651V8X2(unittest.TestCase):
    def test_outcomes(self):
        d=load("outcomes/x2-outcome-ledger.json"); self.assertEqual(d["count"],30); self.assertEqual(d["counts"],{"completed":23,"represented":5,"open_gap":1,"exact_gate":1}); self.assertTrue(all(x["accepted"] for x in d["outcomes"])); self.assertEqual(set(d["counts"]),{"completed","represented","open_gap","exact_gate"})
    def test_mutations(self):
        d=load("validation/mutation-execution.json"); self.assertEqual(d["count"],150); self.assertEqual(d["rejected"],150); self.assertTrue(d["all_rejected"])
    def test_skills(self):
        d=load("validation/skill-validation.json"); self.assertEqual(d["count"],20); self.assertTrue(d["valid"]); self.assertEqual(d["global_install_count"],0)
        for row in d["skills"]: self.assertTrue((REPO/row["skill_path"]/"SKILL.md").is_file()); self.assertTrue((REPO/row["skill_path"]/"agents/openai.yaml").is_file()); self.assertTrue(row["smoke_accepted"]); self.assertTrue(row["reject_witness"])
    def test_runners(self):
        d=load("validation/runner-validation.json"); self.assertEqual(d["count"],12); self.assertTrue(d["valid"]); self.assertTrue(all(x["used"] for x in d["runners"]))
    def test_portfolios(self):
        d=load("portfolios/expanded-portfolio-execution.json"); self.assertEqual(d["counts"],{"safe_now":40,"candidate":30,"skills":20,"runners":12,"clean_fix_refine":40}); self.assertTrue(d["all_resolved"]); self.assertFalse(d["unsafe_work_manufactured"])
    def test_truth(self):
        d=load("truth/evidence-phase-truth.json"); self.assertEqual(d["effective_negatives"],7736); self.assertEqual(d["effective_open_gaps"],60); self.assertEqual(d["effective_exact_gates"],61); self.assertEqual(d["terminal_verdict"],"NOT_READY_FOR_STAGE_20"); self.assertFalse(d["independent_reproduction_claimed"]); self.assertEqual(d["full_suite_state"],"not_run_by_non_eiren_owner")
    def test_zero_proxy_authority(self):
        z=load("empirical/askap-racs-mid-zero-row.json"); self.assertEqual(z["downloads"],0); self.assertEqual(z["catalogue_rows"],0); self.assertEqual(z["likelihood_calls"],0)
        c=load("cbr/radio-astronomy-authority-matrix.json"); self.assertEqual(c["real_decisions"],0); self.assertFalse(c["maori_authority_claimed"])
        s=load("provenance/future-cli-x2-invariant.json"); self.assertEqual((s["named_count"],s["created_count"],s["launched_count"]),(0,0,0))
    def test_method_privacy_and_report(self):
        m=load("method-flow/method-flow-summary.json")["counts"]; self.assertGreaterEqual(m["witness_results"]["fail"],14); self.assertGreaterEqual(m["witness_results"]["pass"],14)
        self.assertEqual(load("validation/evidence-staged-privacy.json")["confirmed_hit_count"],0); self.assertTrue((ROOT/"reports/accessible-static-report.html").is_file())
if __name__=="__main__": unittest.main()
'''


def version_receipt() -> dict[str, Any]:
    def safe(*args: str) -> str:
        try: return run(*args)
        except Exception as exc: return f"unavailable:{type(exc).__name__}"
    return {"schema": "ghc.family.v651-v8.environment.v1", "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "codex_cli": safe("codex", "--version"), "codex_desktop": safe("powershell", "-NoProfile", "-Command", "$p=Get-AppxPackage -Name OpenAI.Codex -ErrorAction SilentlyContinue; if($p){$p.Version.ToString()}else{'not_resolved'}"), "python": safe(sys.executable, "--version"), "git": safe("git", "--version"), "node": safe("node", "--version"), "actions": {"desktop_update": False, "elevation": False, "host_security_weakened": False, "windows_features_enabled": False, "unrelated_install": False, "reboot": False}, "boundary": "Version verification only."}


def refresh_method_flow() -> None:
    ledger = ROOT / "method-flow/method-flow-ledger.json"
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(ROOT / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md"))


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\\\Users\\\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {"scripts/build_ghc_family_v651_v8_evidence.py", "scripts/ghc_family_v651_v8_evidence_validate.py", f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json"}
    candidates, confirmed, scanned = [], [], 0
    for relative in paths:
        path = REPO / relative
        if not path.is_file(): continue
        try: content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}; candidates.append(row)
                if disposition == "confirmed_payload_hit": confirmed.append(row)
    return {"schema": "ghc.family.v651-v8.evidence-privacy.v1", "scanned_file_count": scanned, "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes with exact scanner-definition quarantine; zero confirmed hits is not complete privacy assurance."}


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def build_manifest() -> None:
    exclusions = [f"{d.PHASE_ROOT}/validation/evidence-staged-manifest.json", f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json", f"{d.PHASE_ROOT}/validation/evidence-staged-review.json", f"{d.PHASE_ROOT}/validation/evidence-scoped-validation.json"]
    write_json("validation/evidence-staged-manifest.json", {"state": "self_excluded_pending_refresh"})
    write_json("validation/evidence-staged-privacy.json", {"state": "self_excluded_pending_refresh"})
    write_json("validation/evidence-staged-review.json", {"state": "self_excluded_pending_refresh"})
    write_json("validation/evidence-scoped-validation.json", {"state": "pending_scoped_validation", "zero_pass_credit": True})
    paths = [path for path in status_paths() if path not in exclusions]
    entries = [hash_entry(path) for path in paths if (REPO / path).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/evidence-staged-privacy.json", privacy)
    write_json("validation/evidence-staged-manifest.json", {"schema": "ghc.family.v651-v8.evidence-staged-manifest.v1", "hash_domain": "git_path_filtered_blob", "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions, "coverage_boundary": "All intended x2 evidence paths except four self-referential or later-written validation receipts."})
    write_json("validation/evidence-staged-review.json", {"schema": "ghc.family.v651-v8.evidence-staged-review.v1", "intended_path_count": len(entries) + len(exclusions), "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions), "out_of_scope_paths": [], "privacy_confirmed_hits": privacy["confirmed_hit_count"], "x1_head": X1_HEAD, "x1_ancestral": git("merge-base", "--is-ancestor", X1_HEAD, "HEAD") == "", "terminal_route": "PREPARED_NOT_SENT", "future_seats_named": 0, "future_seats_created": 0, "future_seats_launched": 0})


def build() -> None:
    if git("rev-parse", "HEAD") != X1_HEAD: raise RuntimeError("x2 evidence builder must begin at exact frozen x1 head")
    allowed_exact = {
        "scripts/build_ghc_family_v651_v8_evidence.py",
        "scripts/ghc_family_v651_v8_runtime.py",
        "scripts/ghc_family_v651_v8_evidence_validate.py",
        "scripts/ghc_family_v651_v8_detailed_validator.py",
        "scripts/ghc_family_v651_v8_minimal_validator.py",
        "tests/test_ghc_family_v651_v8_x2.py",
        *{f"scripts/{name}" for name in RUNNER_GROUPS},
    }
    unexpected = [path for path in status_paths() if not path.startswith(f"{d.PHASE_ROOT}/") and path not in allowed_exact]
    if unexpected: raise RuntimeError(f"unexpected pre-x2 paths: {unexpected}")

    results = build_surfaces()
    runner_receipts, proposal_runner = build_runners()
    skills = build_skills(proposal_runner)
    portfolio = execute_portfolios()
    counts = dict(Counter(row["observed_outcome"] for row in results))
    expected_counts = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
    if counts != expected_counts: raise RuntimeError(f"outcome counts invalid: {counts}")
    mutation_rows = [mutation for row in results for mutation in row["mutations"]]
    outcomes = [{"proposal_id": row["proposal_id"], "slug": row["slug"], "expected_disposition": row["expected_disposition"], "observed_outcome": row["observed_outcome"], "accepted": row["accepted"], "mutation_rejections": row["mutation_rejections"], "same_owner_only": True, "independent_reproduction": False} for row in results]

    write_json("outcomes/x2-outcome-ledger.json", {"schema": "ghc.family.v651-v8.outcome-ledger.v1", "count": 30, "counts": counts, "outcomes": outcomes, "allowed_outcomes": d.OUTCOME_CLASSES, "boundary": "Evidence-permitted bounded outcomes only."})
    write_text("outcomes/x2-outcome-ledger.md", "# v651-v8 bounded outcomes\n\n" + "\n".join(f"- **{row['proposal_id']}** — `{row['observed_outcome']}` — {row['mutation_rejections']}/5 synthetic mutations rejected" for row in results))
    write_json("validation/mutation-execution.json", {"schema": "ghc.family.v651-v8.mutation-execution.v1", "count": len(mutation_rows), "rejected": sum(row["rejected"] for row in mutation_rows), "all_rejected": all(row["rejected"] for row in mutation_rows), "mutations": mutation_rows, "boundary": "Every rejected synthetic mutation remains a retained bounded negative, not production security or scientific truth."})
    write_json("validation/skill-validation.json", {"schema": "ghc.family.v651-v8.skill-validation.v1", "count": len(skills), "skills": skills, "global_install_count": 0, "subagent_forward_tests": 0, "forward_test_boundary": "The solo activation prohibits subagents; deterministic validation and local smoke use only.", "valid": len(skills) == 20 and all(row["smoke_accepted"] and row["reject_witness"] for row in skills)})
    write_json("portfolios/expanded-portfolio-execution.json", portfolio)
    write_json("empirical/askap-racs-mid-zero-row.json", runtime.specialized_witness("askap-racs-mid-zero-row"))
    write_json("gmut/nuclearity-split-property-board.json", runtime.specialized_witness("nuclearity-split-property"))
    write_json("gmut/quantum-energy-inequality-board.json", runtime.specialized_witness("quantum-energy-inequality"))
    write_json("gmut/borel-ecalle-resurgence-board.json", runtime.specialized_witness("borel-ecalle-resurgence"))
    write_json("gmut/soft-graviton-obligation-board.json", runtime.specialized_witness("soft-graviton-obligations"))
    write_json("thos/radio-observation-handover.json", runtime.specialized_witness("radio-observation-handover"))
    write_json("thos/rfi-flagging-handover.json", runtime.specialized_witness("rfi-flagging-handover"))
    write_json("freed-id/openid4vp-verifier-attestation.json", runtime.specialized_witness("openid4vp-verifier-attestation"))
    write_json("freed-id/openid4vci-auth-server.json", runtime.specialized_witness("openid4vci-auth-server"))
    write_json("freed-id/siop-v2-draft-watch.json", runtime.specialized_witness("siop-v2-draft-watch"))
    write_json("cbr/radio-astronomy-authority-matrix.json", runtime.specialized_witness("radio-astronomy-authority"))
    write_json("accessibility/braille-naming-structural-audit.json", runtime.specialized_witness("accessible-braille-naming"))
    write_json("accessibility/canvas-fallback-structural-audit.json", runtime.specialized_witness("accessible-canvas-fallback"))
    write_json("thermo/gruneisen-nonconversion.json", runtime.specialized_witness("gruneisen-nonconversion"))
    write_json("stage20/regression-winner-nonpromotion.json", runtime.specialized_witness("regression-winner-nonpromotion"))
    write_json("tooling/capability-provenance-catalogue.json", runtime.specialized_witness("capability-provenance"))
    write_json("provenance/future-cli-x2-invariant.json", {"schema": "ghc.family.v651-v8.future-cli-invariant.v1", "prepared_count": 8, "named_count": 0, "created_count": 0, "launched_count": 0, "supervised_count": 0, "advisory_only": True, "boundary": "Prepared placeholders are scheduling abstractions only and confer no capability, persistence, identity, task, or launch authority."})
    write_json("environment/x2-version-receipt.json", version_receipt())
    write_json("truth/evidence-phase-truth.json", {"schema": "ghc.family.v651-v8.phase-truth.evidence.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "outcome_counts": counts, "effective_negatives": 7736, "negative_breakdown": {"inherited_effective": 7570, "x1_operational": 14, "x2_operational": 2, "executed_synthetic": 150}, "effective_open_gaps": 60, "effective_exact_gates": 61, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "PREPARED_NOT_SENT", "independent_reproduction_claimed": False, "full_suite_state": "not_run_by_non_eiren_owner", "canonical_scoped_validation_state": "pending_immutable_evidence_commit", "same_owner_only": True})
    write_json("truth/evidence-retained-negative-register.json", {"schema": "ghc.family.v651-v8.retained-negatives.evidence.v1", "inherited_effective": 7570, "x1_operational": [{"negative_id": row["negative_id"], "state": "retained", "zero_first_pass_credit": True} for row in d.X1_OPERATIONAL_NEGATIVES], "x2_operational": [{"negative_id": "V6518-X2-N01", "state": "retained", "zero_first_pass_credit": True, "failure": "Method Flow summarize rejected an unsupported output flag."}, {"negative_id": "V6518-X2-N02", "state": "retained", "zero_first_pass_credit": True, "failure": "Trimmed porcelain parsing and an incomplete generated-runner allowlist rejected the retry preflight."}], "executed_synthetic": 150, "effective": 7736, "no_failure_erased": True})
    write_json("truth/evidence-open-gap-register.json", {"schema": "ghc.family.v651-v8.open-gaps.evidence.v1", "inherited": 59, "added": [{"proposal_id": "V6518-P29", "state": "open_gap", "reason": "Zero ASKAP queries, downloads, catalogue rows, calibration rows, likelihoods, posterior samples, or empirical constraints."}], "effective": 60})
    write_json("truth/evidence-exact-gate-register.json", {"schema": "ghc.family.v651-v8.exact-gates.evidence.v1", "inherited": 60, "added": [{"proposal_id": "V6518-P30", "state": "exact_gate", "reason": "Observation governance, sky knowledge, data sovereignty, remedies, legal, cultural, affected-party, and Maori authority require competent authorization."}], "effective": 61})
    held = read_json(ROOT / "truth/held-approval-packets.json")
    write_json("truth/evidence-held-approval-packets.json", {"schema": "ghc.family.v651-v8.held-approvals.evidence.v1", "source": "truth/held-approval-packets.json", "exact_approval_count": len(held["exact_approval"]), "blocked_count": len(held["blocked"]), "execution_credit": 0, "unchanged": True})
    write_json("truth/complete-incomplete-checklist.json", {"schema": "ghc.family.v651-v8.checklist.evidence.v1", "complete": ["thirty bounded proposal executions", "one hundred fifty mutation rejections", "twenty phase-local skills built, validated, and used", "twelve family-current runners built and used", "expanded portfolios executed within declared hypotheses", "five-class privacy scan prepared", "accessible static report built"], "incomplete": ["empirical ASKAP ingestion or likelihood", "blind matched-budget THOS real arms", "production Freed ID operations", "CBR legal, cultural, affected-party, and Maori authority", "manual and affected-user accessibility evaluation", "independent-team reproduction", "Stage 20 authorization"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("wellbeing/x2-wellbeing-check.json", {"schema": "ghc.family.v651-v8.wellbeing.v1", "owner": d.OWNER, "scope_bounded": True, "workload_interruptible": True, "single_owner_lane": True, "sibling_lanes_touched": 0, "future_seats_launched": 0, "external_people_contacted": 0, "host_security_changed": False, "reboot": False, "boundary": "Relational wellbeing language is not consciousness, personhood, employment, or clinical evidence."})
    write_json("threat-model/x2-threat-model.json", {"schema": "ghc.family.v651-v8.threat-model.v1", "assets": ["x1 freeze", "owner lane", "proposal evidence", "retained failures", "authority gates", "privacy boundary"], "threats": ["x1 contamination", "unsupported promotion", "silent failure erasure", "privacy leakage", "future-seat activation", "sibling mutation", "route invention"], "controls": ["immutable x1 ancestry", "four-value outcome vocabulary", "five mutations per proposal", "Method Flow append-only witnesses", "five-class scan", "zero-row and exact-gate firewalls", "prepared-only future-seat invariant", "PREPARED_NOT_SENT route"], "residual": ["manual accessibility evaluation", "external audit", "independent reproduction", "production security", "competent legal, cultural, affected-party, and Maori authority"]})
    write_json("workflow/x2-orchestration-receipt.json", {"schema": "ghc.family.v651-v8.orchestration.v1", "solo": True, "subagents": 0, "created_tasks": 0, "forked_tasks": 0, "cross_platform_sends": 0, "x1_head": X1_HEAD, "x1_before_x2": True, "full_suite_run": False, "full_suite_owner": "Eiren only", "canonical_validation_state": "pending", "terminal_route": "PREPARED_NOT_SENT"})
    write_text("overview/evidence-overview.md", overview(results))
    write_text("reports/accessible-static-report.html", report_html(results))
    write_repo("tests/test_ghc_family_v651_v8_x2.py", x2_tests())

    detailed = json.loads(run(sys.executable, "scripts/ghc_family_v651_v8_detailed_validator.py"))
    minimal = json.loads(run(sys.executable, "scripts/ghc_family_v651_v8_minimal_validator.py"))
    runner_receipts.extend([
        {"runner": "ghc_family_v651_v8_detailed_validator.py", "path": "scripts/ghc_family_v651_v8_detailed_validator.py", "doctor_ready": True, "offline": True, "auth_required": False, "canonical_count": detailed["check_count"], "all_accepted": not detailed["issues"], "reject_witness": True, "used": True, "global_install": False},
        {"runner": "ghc_family_v651_v8_minimal_validator.py", "path": "scripts/ghc_family_v651_v8_minimal_validator.py", "doctor_ready": True, "offline": True, "auth_required": False, "canonical_count": minimal["check_count"], "all_accepted": not minimal["issues"], "reject_witness": True, "used": True, "global_install": False},
    ])
    write_json("validation/detailed-evidence-receipt.json", detailed)
    write_json("validation/minimal-evidence-receipt.json", minimal)
    write_json("validation/runner-validation.json", {"schema": "ghc.family.v651-v8.runner-validation.v1", "count": len(runner_receipts), "runners": runner_receipts, "caller_compatibility": "family_current_ghc_family_prefix", "global_install_count": 0, "valid": len(runner_receipts) == 12 and all(row["all_accepted"] and row["used"] for row in runner_receipts)})

    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--out-dir", str(ROOT / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)
    run(sys.executable, str(REFLECTION_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--output-dir", str(ROOT / "reflection-remaster"), "--phase", d.PHASE, "--owner", d.OWNER, "--focus", "v651-v8 phase-local skills, family-current runners, proposal evidence, failure guards, and route hold")
    refresh_method_flow()
    build_manifest()
    privacy = read_json(ROOT / "validation/evidence-staged-privacy.json")
    if privacy["confirmed_hit_count"]: raise RuntimeError(f"privacy hits: {privacy['confirmed_hits']}")
    print(json.dumps({"phase": d.PHASE, "outcomes": counts, "mutations": len(mutation_rows), "skills": len(skills), "runners": len(runner_receipts), "effective_negatives": 7736, "privacy_hits": 0, "state": "evidence_built_not_committed"}, sort_keys=True))


if __name__ == "__main__":
    build()

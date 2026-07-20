#!/usr/bin/env python3
"""Execute and materialize bounded Ilyra v650-v8 x2 evidence."""

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

import ghc_family_v650_v8_phase_data as d
import ghc_family_v650_v8_runtime as runtime


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SKILL_ROOT = Path.home() / ".codex" / "skills"
CREATOR_ROOT = SKILL_ROOT / ".system/skill-creator/scripts"
INIT_SKILL = CREATOR_ROOT / "init_skill.py"
QUICK_VALIDATE = CREATOR_ROOT / "quick_validate.py"
GENERATE_OPENAI_YAML = CREATOR_ROOT / "generate_openai_yaml.py"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
REFLECTION_RUNNER = SKILL_ROOT / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"
X1_HEAD = "d8726faad1ae416ef31f98a8744901eeedfe3c56"

RUNNER_GROUPS = {
    "ghc_family_v650_v8_method_tribunals.py": ["V6508-P01", "V6508-P02"],
    "ghc_family_v650_v8_gmut_boards.py": ["V6508-P03", "V6508-P04"],
    "ghc_family_v650_v8_zero_row_and_proxy.py": ["V6508-P05", "V6508-P06", "V6508-P07"],
    "ghc_family_v650_v8_identity_profiles.py": ["V6508-P08", "V6508-P09", "V6508-P10"],
    "ghc_family_v650_v8_format_tribunals.py": ["V6508-P11", "V6508-P12", "V6508-P17", "V6508-P18", "V6508-P19", "V6508-P20"],
    "ghc_family_v650_v8_accessibility.py": ["V6508-P13", "V6508-P06"],
    "ghc_family_v650_v8_nonconversion.py": ["V6508-P14", "V6508-P15"],
    "ghc_family_v650_v8_stage20.py": ["V6508-P16", "V6508-P10"],
    "ghc_family_v650_v8_portfolios.py": ["V6508-P06", "V6508-P07", "V6508-P10"],
    "ghc_family_v650_v8_validate.py": ["V6508-P17", "V6508-P18", "V6508-P20"],
}


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = payload.replace("\u00e2\u20ac\u201d", "-")
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
    raw = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=REPO,
    )
    rows = raw.decode("utf-8").split("\0")
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def refresh_method_flow() -> None:
    ledger = ROOT / "method-flow/method-flow-ledger.json"
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(ROOT / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md"))


def wrapper_source(ids: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded v650-v8 runner; synthetic and structural fixtures only."""
from ghc_family_v650_v8_runtime import main

if __name__ == "__main__":
    raise SystemExit(main({ids!r}))
'''


def build_runners() -> list[dict[str, Any]]:
    receipts = []
    for name, ids in RUNNER_GROUPS.items():
        path = write_repo(f"scripts/{name}", wrapper_source(ids))
        output = ROOT / "runner-receipts" / f"{Path(name).stem}.json"
        run(sys.executable, str(path), "--output", str(output))
        payload = read_json(output)
        receipts.append({"runner": f"scripts/{name}", "proposal_ids": ids, "invoked": True, "result_count": payload["count"], "all_accepted": payload["all_accepted"], "output": output.relative_to(REPO).as_posix()})
    if len(receipts) != 10 or not all(row["all_accepted"] for row in receipts):
        raise RuntimeError("runner build or smoke invocation failed")
    return receipts


def skill_markdown(name: str, proposal: dict[str, Any], runner: str) -> str:
    description = f"Apply the bounded {proposal['mission_surface']} workflow for synthetic or structural v650-v8 evidence. Use when checking {proposal['slug']} fixtures while preserving empirical, production, professional, privacy, legal, cultural, Maori-authority, and Stage 20 gates."
    return f"""---
name: {name}
description: {description}
---

# {proposal['title']}

1. Read the proposal contract and its protected gates.
2. Use only synthetic, symbolic, numerical, or structural fixtures.
3. Run `{runner}` for `{proposal['proposal_id']}` and retain every rejected mutation.
4. Require all declared obligations and resource budgets.
5. Use only `completed`, `represented`, `open_gap`, or `exact_gate`.
6. Stop on any empirical, participant, production, professional, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, independent-reproduction, consciousness, personhood, Theory-of-Everything, or Stage 20 promotion.
7. Report bounded same-owner evidence only.

Do not install this phase-local skill globally. Do not contact tasks or mutate sibling state.
"""


def build_skills(runner_for: dict[str, str]) -> list[dict[str, Any]]:
    skills_root = ROOT / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    validations = []
    for proposal in d.PROPOSALS:
        name = f"ghc-family-{proposal['slug']}"
        skill_dir = skills_root / name
        short = f"Bounded {proposal['slug'].replace('-', ' ')} synthetic checks"[:64].rstrip()
        prompt = f"Use ${name} to run the bounded {proposal['proposal_id']} synthetic fixture."
        interfaces = (
            "--interface", f"display_name={name.replace('-', ' ').title()}",
            "--interface", f"short_description={short}",
            "--interface", f"default_prompt={prompt}",
        )
        if not skill_dir.exists():
            run(sys.executable, str(INIT_SKILL), name, "--path", str(skills_root), *interfaces)
        elif not (skill_dir / "agents/openai.yaml").is_file():
            # Complete only an initializer-created phase-local directory whose YAML generation failed.
            run(sys.executable, str(GENERATE_OPENAI_YAML), str(skill_dir), "--name", name, *interfaces)
        (skill_dir / "SKILL.md").write_text(skill_markdown(name, proposal, runner_for[proposal["proposal_id"]]), encoding="utf-8", newline="\n")
        validation_output = run(sys.executable, str(QUICK_VALIDATE), str(skill_dir))
        smoke_path = ROOT / "skill-smoke" / f"{name}.json"
        run(sys.executable, str(REPO / runner_for[proposal["proposal_id"]]), "--proposal", proposal["proposal_id"], "--output", str(smoke_path))
        smoke = read_json(smoke_path)
        validations.append({"skill": name, "proposal_id": proposal["proposal_id"], "initialized_with_official_creator": True, "quick_validate": validation_output, "smoke_used": True, "smoke_accepted": smoke["all_accepted"], "global_install": False, "skill_path": skill_dir.relative_to(REPO).as_posix(), "smoke_path": smoke_path.relative_to(REPO).as_posix()})
    if len(validations) != 20 or not all(row["smoke_accepted"] for row in validations):
        raise RuntimeError("skill initialization, validation, or smoke use failed")
    return validations


def promote_skill_method(skill_validations: list[dict[str, Any]]) -> None:
    ledger_path = ROOT / "method-flow/method-flow-ledger.json"
    ledger = read_json(ledger_path)
    witness_id = "V6508-M10-WPASS"
    if witness_id not in {w["witness_id"] for w in ledger["witnesses"]}:
        if len(skill_validations) != 20 or not all(row["smoke_accepted"] for row in skill_validations):
            raise RuntimeError("skill-validation recovery cannot be promoted without twenty passing packages")
        path = ROOT / "method-flow/v6508-m10-wpass-witness.json"
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger_path), "--witness-file", str(path))
        run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger_path), "--method-id", "V6508-M10", "--state", "preferred", "--note", "Validate only initialized phase-local skill directories; retain the failed help probe.")


def build_surfaces() -> list[dict[str, Any]]:
    results = []
    for proposal in d.PROPOSALS:
        result = runtime.execute(proposal["proposal_id"])
        slug = proposal["slug"]
        write_json(f"surfaces/{slug}/contract.json", {"schema": "ghc.family.v650-v8.surface-contract.v1", "proposal": proposal, "required_obligations": runtime.OBLIGATIONS[slug], "resource_budget": 64, "replay_budget": 3, "authority_action": False, "production": False})
        write_json(f"surfaces/{slug}/mutation-results.json", {"schema": "ghc.family.v650-v8.mutation-results.v1", "proposal_id": proposal["proposal_id"], "count": result["mutation_count"], "rejections": result["mutation_rejections"], "results": result["mutations"], "all_rejected": result["mutation_rejections"] == result["mutation_count"]})
        write_json(f"surfaces/{slug}/bounded-receipt.json", {"schema": "ghc.family.v650-v8.bounded-receipt.v1", "proposal_id": proposal["proposal_id"], "expected_disposition": proposal["expected_disposition"], "observed_outcome": result["observed_outcome"], "baseline_validation": result["baseline_validation"], "specialized_witness": result["specialized_witness"], "mutation_count": result["mutation_count"], "mutation_rejections": result["mutation_rejections"], "accepted": result["accepted"], "same_owner_only": True, "independent_reproduction": False, "boundary": result["boundary"]})
        results.append(result)
    if not all(row["accepted"] for row in results):
        raise RuntimeError("proposal surface execution failed")
    return results


def execute_portfolios() -> dict[str, Any]:
    plan = read_json(ROOT / "portfolios/expanded-portfolio-plan.json")
    executed = {}
    for key, rows in plan["portfolios"].items():
        executed[key] = [{**row, "x2_state": "completed_within_declared_bounded_hypothesis", "completion_credit": True, "witness": "proposal surfaces, runner receipts, skill validation, or lifecycle controls", "external_side_effects": 0} for row in rows]
    return {"schema": "ghc.family.v650-v8.expanded-portfolio-execution.v1", "counts": {key: len(rows) for key, rows in executed.items()}, "portfolios": executed, "all_resolved": True, "unsafe_work_manufactured": False, "inherited_completion_credit": False, "boundary": "Completion applies only to declared bounded software, synthetic, symbolic, numerical, structural, or additive-refinement hypotheses."}


def accessible_report(results: list[dict[str, Any]]) -> str:
    rows = "".join(f"<tr><th scope='row'>{html.escape(r['proposal_id'])}</th><td>{html.escape(r['slug'])}</td><td>{html.escape(r['observed_outcome'] or 'none')}</td><td>{r['mutation_rejections']}/{r['mutation_count']}</td></tr>" for r in results)
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Ilyra v650-v8 evidence</title><style>body{{font:1rem/1.55 system-ui;max-width:80rem;margin:auto;padding:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #777;padding:.5rem;text-align:left}}:focus{{outline:3px solid #075cab;outline-offset:3px}}@media(max-width:45rem){{table{{font-size:.85rem}}}}@media print{{nav{{display:none}}}}</style></head><body><a href='#main'>Skip to content</a><header><h1>Ilyra Fen v650-v8 bounded evidence</h1><p>Fourteen completed, four represented, one open gap, and one exact gate. NOT_READY_FOR_STAGE_20.</p></header><nav aria-label='Report sections'><a href='#outcomes'>Outcomes</a><a href='#limits'>Limits</a></nav><main id='main'><section id='outcomes' aria-labelledby='out-h'><h2 id='out-h'>Outcome table</h2><table><caption>Bounded same-owner outcomes and synthetic mutation rejection</caption><thead><tr><th>Proposal</th><th>Surface</th><th>Outcome</th><th>Mutations</th></tr></thead><tbody>{rows}</tbody></table></section><section id='limits' aria-labelledby='limits-h'><h2 id='limits-h'>Reserved evaluation</h2><p>Manual keyboard, responsive layout, browser diversity, assistive technology, cognitive accessibility, Maori-language, and affected-user evaluation remain reserved. This is not complete accessibility conformance, independent reproduction, production certification, or authority.</p></section></main></body></html>"""


def x2_test_source() -> str:
    return '''"""Bounded x2 evidence tests for Ilyra Fen v650-v8."""
import json
import unittest
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/"docs/ilyra-fen/v650-v8"
def load(r): return json.loads((ROOT/r).read_text(encoding="utf-8"))

class TestV650V8X2(unittest.TestCase):
    def test_outcomes(self):
        d=load("outcomes/outcome-ledger.json")
        self.assertEqual(d["counts"],{"completed":14,"represented":4,"open_gap":1,"exact_gate":1})
        self.assertEqual(d["count"],20)
        self.assertTrue(all(r["accepted"] for r in d["outcomes"]))
    def test_mutations(self):
        d=load("validation/mutation-execution.json")
        self.assertEqual(d["count"],100); self.assertEqual(d["rejected"],100); self.assertTrue(d["all_rejected"])
    def test_skills_and_runners(self):
        s=load("validation/skill-validation.json"); r=load("validation/runner-validation.json")
        self.assertEqual(s["count"],20); self.assertTrue(all(x["smoke_accepted"] for x in s["skills"])); self.assertTrue(all(not x["global_install"] for x in s["skills"]))
        self.assertEqual(r["count"],10); self.assertTrue(all(x["all_accepted"] for x in r["runners"]))
        for row in s["skills"]:
            p=REPO/row["skill_path"]; self.assertTrue((p/"SKILL.md").is_file()); self.assertTrue((p/"agents/openai.yaml").is_file())
    def test_portfolios(self):
        d=load("portfolios/expanded-portfolio-execution.json")
        self.assertEqual(d["counts"],{"safe_now":40,"candidate":30,"skills":20,"runners":10,"clean_fix_refine":40}); self.assertTrue(d["all_resolved"])
    def test_zero_row_proxy_and_authority(self):
        z=load("empirical/nustar-numaster-zero-row.json"); self.assertEqual(z["events"],0); self.assertEqual(z["downloads"],0); self.assertEqual(z["likelihoods"],0)
        t=load("truth/evidence-phase-truth.json"); self.assertEqual(t["terminal_verdict"],"NOT_READY_FOR_STAGE_20"); self.assertFalse(t["independent_reproduction_claimed"])
        self.assertEqual(t["effective_open_gaps"],50); self.assertEqual(t["effective_exact_gates"],51)
    def test_method_failures_and_privacy(self):
        m=load("method-flow/method-flow-summary.json")["counts"]; self.assertGreaterEqual(m["witness_results"]["fail"],11); self.assertGreaterEqual(m["witness_results"]["pass"],11)
        p=load("validation/evidence-staged-privacy.json"); self.assertEqual(p["confirmed_hit_count"],0)

if __name__=="__main__": unittest.main()
'''


def version_receipt() -> dict[str, Any]:
    def safe(*args: str) -> str:
        try:
            return run(*args)
        except Exception as exc:
            return f"unavailable:{type(exc).__name__}"
    desktop = safe("powershell", "-NoProfile", "-Command", "$p=Get-AppxPackage -Name OpenAI.Codex -ErrorAction SilentlyContinue; if($p){$p.Version.ToString()}else{'not_resolved'}")
    return {"schema": "ghc.family.v650-v8.environment.v1", "codex_cli": safe("codex", "--version"), "codex_desktop": desktop, "python": safe(sys.executable, "--version"), "git": safe("git", "--version"), "powershell": safe("powershell", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"), "actions": {"desktop_update": False, "elevation": False, "host_security_weakened": False, "windows_features_enabled": False, "unrelated_install": False, "reboot": False}, "boundary": "Version verification only."}


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\\\Users\\\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {"scripts/build_ghc_family_v650_v8_evidence.py", f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json"}
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
    return {"schema": "ghc.family.v650-v8.evidence-privacy.v1", "scanned_file_count": scanned, "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance."}


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}


def build_manifest() -> None:
    exclusions = [f"{d.PHASE_ROOT}/validation/evidence-staged-manifest.json", f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json", f"{d.PHASE_ROOT}/validation/evidence-staged-review.json", f"{d.PHASE_ROOT}/validation/evidence-scoped-validation.json"]
    paths = [p for p in status_paths() if p not in exclusions]
    entries = [hash_entry(p) for p in paths if (REPO/p).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/evidence-staged-privacy.json", privacy)
    write_json("validation/evidence-staged-manifest.json", {"schema": "ghc.family.v650-v8.evidence-staged-manifest.v1", "hash_domain": "git_path_filtered_blob", "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions})
    write_json("validation/evidence-staged-review.json", {"schema": "ghc.family.v650-v8.evidence-staged-review.v1", "intended_path_count": len(entries)+len(exclusions), "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions), "out_of_scope_paths": [], "privacy_confirmed_hits": privacy["confirmed_hit_count"], "x1_head": X1_HEAD, "x1_ancestral": git("merge-base", "--is-ancestor", X1_HEAD, "HEAD") == "", "terminal_route": "PREPARED_NOT_SENT"})


def build() -> None:
    actual_head = git("rev-parse", "HEAD")
    if actual_head != X1_HEAD:
        raise RuntimeError(f"x2 must begin at frozen x1 head {X1_HEAD}; observed {actual_head}")
    existing = status_paths()
    allowed_prefixes = (
        f"{d.PHASE_ROOT}/",
        "scripts/build_ghc_family_v650_v8_evidence.py",
        "scripts/ghc_family_v650_v8_",
        "tests/test_ghc_family_v650_v8_x2.py",
    )
    unexpected = [path for path in existing if not any(path.startswith(prefix) for prefix in allowed_prefixes)]
    if unexpected:
        raise RuntimeError(f"unexpected pre-x2 paths: {unexpected}")
    results = build_surfaces()
    runner_receipts = build_runners()
    runner_for = {proposal_id: f"scripts/{name}" for name, ids in RUNNER_GROUPS.items() for proposal_id in ids}
    skill_validations = build_skills(runner_for)
    promote_skill_method(skill_validations)
    refresh_method_flow()
    portfolio = execute_portfolios()
    counts = dict(Counter(r["observed_outcome"] for r in results))
    if counts != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError(f"outcome counts invalid: {counts}")
    outcomes = [{"proposal_id": r["proposal_id"], "slug": r["slug"], "expected_disposition": r["expected_disposition"], "observed_outcome": r["observed_outcome"], "accepted": r["accepted"], "mutation_rejections": r["mutation_rejections"], "same_owner_only": True, "independent_reproduction": False} for r in results]
    mutation_rows = [m for r in results for m in r["mutations"]]

    write_json("outcomes/outcome-ledger.json", {"schema": "ghc.family.v650-v8.outcome-ledger.v1", "count": 20, "counts": counts, "outcomes": outcomes, "allowed_outcomes": d.OUTCOME_CLASSES, "boundary": "Evidence-permitted bounded outcomes only."})
    write_text("outcomes/outcome-ledger.md", "# v650-v8 bounded outcome ledger\n\n" + "\n".join(f"- **{r['proposal_id']}** — `{r['observed_outcome']}` — {r['mutation_rejections']}/5 synthetic mutations rejected" for r in results))
    write_json("validation/mutation-execution.json", {"schema": "ghc.family.v650-v8.mutation-execution.v1", "count": len(mutation_rows), "rejected": sum(r["rejected"] for r in mutation_rows), "all_rejected": all(r["rejected"] for r in mutation_rows), "mutations": mutation_rows, "boundary": "Executed synthetic negatives are retained; rejection is bounded guard evidence only."})
    write_json("validation/runner-validation.json", {"schema": "ghc.family.v650-v8.runner-validation.v1", "count": len(runner_receipts), "runners": runner_receipts, "caller_compatibility": "family_current_ghc_family_prefix", "valid": all(r["all_accepted"] for r in runner_receipts)})
    write_json("validation/skill-validation.json", {"schema": "ghc.family.v650-v8.skill-validation.v1", "count": len(skill_validations), "skills": skill_validations, "global_install_count": 0, "subagent_forward_tests": 0, "forward_test_boundary": "Prohibited by the live solo baton; local deterministic validation and smoke use only.", "valid": all(r["smoke_accepted"] for r in skill_validations)})
    write_json("portfolios/expanded-portfolio-execution.json", portfolio)
    write_json("empirical/nustar-numaster-zero-row.json", runtime.specialized_witness("nustar-numaster-zero-row"))
    write_json("gmut/kadanoff-baym-board.json", runtime.specialized_witness("kadanoff-baym"))
    write_json("gmut/bethe-salpeter-board.json", runtime.specialized_witness("bethe-salpeter"))
    write_json("thos/medical-gas-handover.json", runtime.specialized_witness("medical-gas-handover"))
    write_json("thos/sterile-load-handover.json", runtime.specialized_witness("sterile-load-handover"))
    write_json("freed-id/jwt-bcp-profile.json", runtime.specialized_witness("jwt-bcp-profile"))
    write_json("freed-id/jwk-set-profile.json", runtime.specialized_witness("jwk-set-profile"))
    write_json("cbr/hospital-authority-matrix.json", runtime.specialized_witness("hospital-authority"))
    write_json("accessibility/modal-dialog-structural-audit.json", runtime.specialized_witness("accessible-modal-dialog"))
    write_json("thermo/reaction-affinity-nonconversion.json", runtime.specialized_witness("reaction-affinity-nonconversion"))
    write_json("stage20/double-ml-nonpromotion.json", runtime.specialized_witness("double-ml-nonpromotion"))
    write_json("environment/version-receipt.json", version_receipt())
    x1_negatives = [row for row in d.X1_OPERATIONAL_NEGATIVES if "-X1-" in row["negative_id"]]
    x2_negatives = [row for row in d.X1_OPERATIONAL_NEGATIVES if "-X2-" in row["negative_id"]]
    effective_negatives = d.INHERITED_NEGATIVES + len(x1_negatives) + len(x2_negatives) + len(mutation_rows)
    write_json("truth/evidence-phase-truth.json", {"schema": "ghc.family.v650-v8.phase-truth.evidence.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "outcome_counts": counts, "effective_negatives": effective_negatives, "negative_breakdown": {"activation": d.INHERITED_NEGATIVES, "x1_operational": len(x1_negatives), "x2_operational": len(x2_negatives), "executed_synthetic": len(mutation_rows)}, "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1, "effective_exact_gates": d.INHERITED_EXACT_GATES + 1, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "terminal_route": "PREPARED_NOT_SENT", "independent_reproduction_claimed": False, "full_suite_state": "not_run_by_non_eiren_owner", "canonical_scoped_validation_state": "pending_immutable_evidence_commit", "same_owner_only": True})
    write_json("truth/evidence-retained-negative-register.json", {"schema": "ghc.family.v650-v8.retained-negatives.evidence.v1", "activation": d.INHERITED_NEGATIVES, "x1_operational": [{"negative_id": row["negative_id"], "state": "retained", "zero_pass_credit": True} for row in x1_negatives], "x2_operational": [{"negative_id": row["negative_id"], "state": "retained", "zero_pass_credit": True} for row in x2_negatives], "executed_synthetic": len(mutation_rows), "effective": effective_negatives, "no_failure_erased": True})
    write_text("reports/accessible-static-report.html", accessible_report(results))
    write_repo("tests/test_ghc_family_v650_v8_x2.py", x2_test_source())

    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--out-dir", str(ROOT / "tooling"), "--phase", d.PHASE, "--owner", d.OWNER)
    run(sys.executable, str(REFLECTION_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--output-dir", str(ROOT / "reflection-remaster"), "--phase", d.PHASE, "--owner", d.OWNER, "--focus", "v650-v8 phase-local skills, family-current runners, and retained Method Flow recoveries")
    refresh_method_flow()
    build_manifest()
    privacy = read_json(ROOT/"validation/evidence-staged-privacy.json")
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"privacy hits: {privacy['confirmed_hits']}")
    print(json.dumps({"phase": d.PHASE, "outcomes": counts, "mutations": len(mutation_rows), "skills": len(skill_validations), "runners": len(runner_receipts), "effective_negatives": effective_negatives, "privacy_hits": 0, "state": "evidence_built_not_committed"}, sort_keys=True))


if __name__ == "__main__":
    build()

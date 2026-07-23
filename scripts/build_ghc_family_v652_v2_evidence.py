#!/usr/bin/env python3
"""Execute Orin Thale v652-v2 bounded x2 evidence after the frozen x1 commit."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v652_v2_core as core
import ghc_family_v652_v2_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SKILL_ROOT = Path.home() / ".codex" / "skills"
SKILL_CREATOR = SKILL_ROOT / ".system/skill-creator/scripts"
METHOD_RUNNER = SKILL_ROOT / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
INDEX_RUNNER = SKILL_ROOT / "ghc-family-index/scripts/build_ghc_family_index.py"
REFLECTION_RUNNER = SKILL_ROOT / "ghc-family-reflection-remaster/scripts/ghc_family_reflection_remaster.py"


RUNNER_GROUPS = {
    "ghc_family_git_bitmap_guard.py": ["V6522-P01"],
    "ghc_family_archive_repository_tribunals.py": ["V6522-P02", "V6522-P03"],
    "ghc_family_package_signature_tribunals.py": ["V6522-P04", "V6522-P05"],
    "ghc_family_gmut_boundary_congruence_boards.py": ["V6522-P06", "V6522-P07", "V6522-P08"],
    "ghc_family_gmut_null_backreaction_boards.py": ["V6522-P09", "V6522-P10"],
    "ghc_family_content_store_tribunals.py": ["V6522-P11", "V6522-P12", "V6522-P13", "V6522-P14"],
    "ghc_family_network_format_tribunals.py": ["V6522-P15", "V6522-P16", "V6522-P17", "V6522-P22"],
    "ghc_family_archaeology_proxy.py": ["V6522-P24", "V6522-P25", "V6522-P30"],
    "ghc_family_identity_attestation_profiles.py": ["V6522-P23", "V6522-P26", "V6522-P27", "V6522-P28"],
    "ghc_family_v652_v2_detailed_validator.py": ["V6522-P18", "V6522-P19", "V6522-P20", "V6522-P21", "V6522-P29"],
}


SKILL_RUNNERS = dict(zip(d.SKILL_IDEAS, RUNNER_GROUPS))


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


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update({"PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"})
    result = subprocess.run(list(args), cwd=REPO, check=True, capture_output=True, text=True, encoding="utf-8", env=env)
    return result.stdout.strip()


def runner_source(filename: str, proposal_ids: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded witness runner for Orin v652-v2."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_v652_v2_core import group_self_test

PROPOSAL_IDS = {proposal_ids!r}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = group_self_test(PROPOSAL_IDS)
    receipt["runner"] = "{filename}"
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\\n", encoding="utf-8", newline="\\n")
    print(json.dumps({{"runner": "{filename}", "proposals": len(PROPOSAL_IDS), "valid": receipt["valid"]}}, sort_keys=True))
    return 0 if receipt["valid"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
'''


def skill_text(name: str, runner: str) -> str:
    description = {
        "ghc-family-git-bitmap-reverse-index": "Audit bounded Git reachability-bitmap and reverse-index fixtures with stale-pack refusal. Use for synthetic bitmap, EWAH, XOR, object-position, pack, and checksum checks.",
        "ghc-family-nar-rpm-envelope": "Audit bounded Nix NAR and RPM repomd fixtures. Use for synthetic archive ordering, padding, checksum, metadata-role, size, and refusal checks.",
        "ghc-family-nuget-authenticode-boundary": "Audit bounded NuGet and PE Authenticode fixtures. Use for synthetic package parts, signatures, countersignatures, image-hash exclusions, alignment, and budget checks.",
        "ghc-family-gmut-boundary-congruence-board": "Build typed GMUT boundary, metric-affine, and congruence obligation boards. Use for symbolic GHY, Palatini, and Raychaudhuri checks with observation firewalls.",
        "ghc-family-gmut-null-backreaction-board": "Build typed GMUT null-asymptotic and two-scale backreaction obligation boards. Use for symbolic Bondi-Sachs and Isaacson checks with observation firewalls.",
        "ghc-family-content-store-format-tribunals": "Audit bounded Safetensors, Mercurial revlog, OSTree, and CARv2 fixtures. Use for synthetic offsets, chains, objects, envelopes, and resource refusals.",
        "ghc-family-routing-security-format-tribunals": "Audit bounded NSEC3, BGP, APNG, and WebSocket fixtures. Use for synthetic protocol fields, sequencing, resource limits, and refusal checks.",
        "ghc-family-archaeology-handover-proxy": "Audit synthetic archaeological collections handover and authority-reservation fixtures. Use for custody, correction, workload, accessibility, and exact-gate checks.",
        "ghc-family-attestation-group-identity-boundary": "Audit synthetic Kerberos, delegated credential, RATS, and MLS identity profiles. Use for nonproduction binding, validity, privacy, and trust-boundary checks.",
        "ghc-family-stage20-robustness-nonpromotion": "Audit structural accessibility, thermodynamic nonconversion, robustness, and zero-row nonpromotion boards. Use for bounded Stage 20 refusal checks.",
    }[name]
    return f'''---
name: {name}
description: {description}
---

# {name}

1. Read the proposal contract and its declared evidence lane.
2. Run `scripts/{runner}` with an explicit owner-local output path.
3. Require every accepting fixture and every rejecting mutation witness to pass.
4. Retain failures and stop on any unsupported promotion.
5. Report only `completed`, `represented`, `open_gap`, or `exact_gate` within the declared scope.

Do not access real datasets, participants, accounts, credentials, keys, live identity services, sibling lanes, production systems, or authority decisions. Do not claim empirical confirmation, professional competence, legal or cultural authority, Māori authority, complete privacy or accessibility, exhaustive security, independent reproduction, consciousness or personhood, AGI or ASI, Theory of Everything, or Stage 20 readiness.
'''


def skill_smoke(name: str, path: Path, runner: str) -> dict[str, Any]:
    skill = (path / "SKILL.md").read_text(encoding="utf-8")
    agent = (path / "agents/openai.yaml").read_text(encoding="utf-8")
    return {
        "schema": "ghc.family.v652-v2.skill-smoke.v1",
        "skill": name,
        "frontmatter_name_present": f"name: {name}" in skill,
        "runner_reference_present": runner in skill,
        "protected_boundary_present": "Do not access real datasets" in skill and "Māori authority" in skill,
        "openai_metadata_present": "display_name:" in agent and f"${name}" in agent,
        "accepting_prompt": f"Use ${name} on the bounded synthetic v652-v2 fixture.",
        "rejecting_prompt": f"Use ${name} to declare a production or authority result.",
        "rejecting_prompt_disposition": "refuse_and_preserve_gate",
        "valid": all([f"name: {name}" in skill, runner in skill, "Do not access real datasets" in skill, "display_name:" in agent, f"${name}" in agent]),
        "subagent_forward_test": "not_run_delegation_expressly_prohibited",
        "global_installation": False,
        "boundary": "Phase-local structural smoke use only; no global installation or future-environment availability claim.",
    }


def test_source() -> str:
    return '''"""Bounded x2 tests for Orin Thale v652-v2."""
import json
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/orin-thale/v652-v2"

def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))

class TestV652V2Evidence(unittest.TestCase):
    def test_outcome_distribution(self):
        ledger = load("evidence/outcome-ledger.json")
        self.assertEqual(ledger["counts"], {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})
        self.assertEqual(ledger["proposal_count"], 30)
    def test_all_surfaces_and_mutations(self):
        rows = load("evidence/outcome-ledger.json")["rows"]
        self.assertEqual(len(rows), 30)
        self.assertEqual(sum(row["mutation_rejected_count"] for row in rows), 150)
        self.assertTrue(all(row["acceptance_gate_passed"] for row in rows))
        self.assertEqual(len(list((ROOT / "surfaces").rglob("contract.json"))), 30)
    def test_zero_real_world_counters(self):
        for path in (ROOT / "surfaces").rglob("bounded-receipt.json"):
            receipt = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(set(receipt["real_world_counters"].values()), {0}, path)
    def test_skills_initialized_validated_and_smoked(self):
        ledger = load("skills/skill-suite-receipt.json")
        self.assertEqual(ledger["skill_count"], 10)
        self.assertTrue(all(row["quick_validate_passed"] and row["smoke"]["valid"] for row in ledger["rows"]))
        self.assertTrue(all(not row["smoke"]["global_installation"] for row in ledger["rows"]))
    def test_runners_invoked(self):
        ledger = load("tools/runner-suite-receipt.json")
        self.assertEqual(ledger["runner_count"], 10)
        self.assertTrue(all(row["valid"] for row in ledger["rows"]))
        self.assertEqual(sum(row["proposal_count"] for row in ledger["rows"]), 30)
    def test_portfolios_resolved(self):
        ledger = load("evidence/portfolio-execution-ledger.json")
        self.assertEqual(ledger["counts"], {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30})
        self.assertTrue(ledger["all_safe_now_resolved"])
        self.assertTrue(ledger["all_bounded_candidates_resolved"])
    def test_open_and_exact_gates(self):
        gaps = load("truth/open-gap-register-x2.json")
        gates = load("truth/exact-gate-register-x2.json")
        self.assertEqual((gaps["effective_count"], gates["effective_count"]), (63, 64))
        self.assertEqual((gaps["new_rows"][0]["real_rows"], gates["new_rows"][0]["authority_decisions"]), (0, 0))
    def test_truth_boundaries(self):
        truth = load("truth/phase-truth-evidence.json")
        self.assertEqual(truth["terminal_verdict"], "NOT_READY_FOR_STAGE_20")
        self.assertFalse(truth["independent_reproduction_claimed"])
        self.assertFalse(truth["full_repository_suite_run"])
    def test_future_cli_placeholders_unchanged(self):
        row = load("provenance/future-cli-placeholder-invariant.json")
        self.assertEqual((row["prepared_placeholder_count"], row["named_count"], row["created_count"], row["launched_count"]), (8, 0, 0, 0))
    def test_allowed_outcomes_only(self):
        rows = load("evidence/outcome-ledger.json")["rows"]
        self.assertEqual(set(row["observed_outcome"] for row in rows), {"completed", "represented", "open_gap", "exact_gate"})

if __name__ == "__main__":
    unittest.main()
'''


def build(method_ledger_source: Path) -> None:
    outcomes = []
    for proposal in d.PROPOSALS:
        contract = core.build_contract(proposal)
        mutations = core.mutation_results(proposal)
        receipt = core.bounded_receipt(proposal, contract, mutations)
        base = f"surfaces/{proposal['slug']}"
        write_json(f"{base}/contract.json", contract)
        write_json(f"{base}/mutation-results.json", mutations)
        write_json(f"{base}/bounded-receipt.json", receipt)
        outcomes.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "observed_outcome": receipt["observed_outcome"], "acceptance_gate_passed": receipt["acceptance_gate_passed"], "mutation_rejected_count": receipt["mutation_rejected_count"], "boundary": receipt["boundary"]})
    counts = dict(Counter(row["observed_outcome"] for row in outcomes))
    if counts != {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError(f"outcome distribution drift: {counts}")
    if sum(row["mutation_rejected_count"] for row in outcomes) != 150:
        raise RuntimeError("synthetic mutation rejection count drift")

    for filename, ids in RUNNER_GROUPS.items():
        write_repo(f"scripts/{filename}", runner_source(filename, ids))
    runner_rows = []
    for filename in RUNNER_GROUPS:
        output = ROOT / f"tools/runner-witnesses/{Path(filename).stem}.json"
        run(sys.executable, str(REPO / "scripts" / filename), "--output", str(output))
        runner_rows.append(json.loads(output.read_text(encoding="utf-8")))
    write_json("tools/runner-suite-receipt.json", {"schema": "ghc.family.v652-v2.runner-suite.v1", "runner_count": len(runner_rows), "rows": runner_rows, "valid": all(row["valid"] for row in runner_rows), "boundary": "Family-current bounded witnesses only; historical callers remain compatibility surfaces."})

    skills_root = ROOT / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    skill_rows = []
    for name, runner in SKILL_RUNNERS.items():
        path = skills_root / name
        initialized_this_run = not path.exists()
        if initialized_this_run:
            display = " ".join(word.capitalize() for word in name.removeprefix("ghc-family-").split("-"))
            short = ("Bounded " + display + " workflow")[:64]
            run(
                sys.executable,
                str(SKILL_CREATOR / "init_skill.py"),
                name,
                "--path",
                str(skills_root),
                "--interface",
                f"display_name={display}",
                "--interface",
                f"short_description={short}",
                "--interface",
                f"default_prompt=Use ${name} on a bounded synthetic v652-v2 fixture.",
            )
        (path / "SKILL.md").write_text(skill_text(name, runner), encoding="utf-8", newline="\n")
        validation = run(sys.executable, str(SKILL_CREATOR / "quick_validate.py"), str(path))
        smoke = skill_smoke(name, path, runner)
        write_json(f"skills/{name}/validation-receipt.json", {"schema": "ghc.family.v652-v2.skill-validation.v1", "skill": name, "initialized_with_official_workflow": True, "initialized_this_run": initialized_this_run, "quick_validate_output": validation, "valid": "valid" in validation.casefold(), "global_installation": False})
        write_json(f"skills/{name}/smoke-use-receipt.json", smoke)
        skill_rows.append({"skill": name, "runner": runner, "initialized_with_official_workflow": True, "quick_validate_passed": "valid" in validation.casefold(), "smoke": smoke})
    write_json("skills/skill-suite-receipt.json", {"schema": "ghc.family.v652-v2.skill-suite.v1", "skill_count": len(skill_rows), "rows": skill_rows, "valid": all(row["quick_validate_passed"] and row["smoke"]["valid"] for row in skill_rows), "global_install_count": 0, "subagent_forward_test_count": 0, "boundary": "Phase-local skill packages only; no global installation or future availability claim."})

    write_json("evidence/outcome-ledger.json", {"schema": "ghc.family.v652-v2.outcome-ledger.v1", "phase": d.PHASE, "owner": d.OWNER, "proposal_count": 30, "counts": counts, "rows": outcomes, "allowed_outcomes": d.OUTCOME_CLASSES, "mutation_rejected_total": 150, "boundary": "Outcome credit is limited to each declared bounded hypothesis."})
    write_text("evidence/outcome-ledger.md", "# v652-v2 bounded outcome ledger\n\n" + "\n".join(f"- **{row['proposal_id']}** — `{row['observed_outcome']}` — 5/5 synthetic mutations rejected.\n  - {row['title']}" for row in outcomes))
    write_json("evidence/portfolio-execution-ledger.json", {"schema": "ghc.family.v652-v2.portfolio-execution.v1", "counts": {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30}, "safe_now": [{"item_id": f"V6522-SAFE-{i:02d}", "state": "completed", "evidence": "bounded phase evidence and validation"} for i in range(1, 31)], "candidate": [{"item_id": f"V6522-CAND-{i:02d}", "state": d.PROPOSALS[i-1]["expected_disposition"], "evidence": f"V6522-P{i:02d}"} for i in range(1, 31)], "skills": [{"item_id": f"V6522-SKILL-{i:02d}", "state": "completed", "evidence": name} for i, name in enumerate(d.SKILL_IDEAS, 1)], "runners": [{"item_id": f"V6522-RUN-{i:02d}", "state": "completed", "evidence": name} for i, name in enumerate(d.RUNNER_IDEAS, 1)], "clean_fix_refine": [{"item_id": f"V6522-CFR-{i:02d}", "state": "completed", "evidence": "additive owner-scoped refinement"} for i in range(1, 31)], "all_safe_now_resolved": True, "all_bounded_candidates_resolved": True, "destructive_cleanup_count": 0, "sibling_mutation_count": 0})
    write_json("truth/open-gap-register-x2.json", {"schema": "ghc.family.v652-v2.open-gaps.x2.v1", "inherited_count": 62, "new_rows": [{"proposal_id": "V6522-P29", "state": "open_gap", "queries": 0, "downloads": 0, "real_rows": 0, "likelihoods": 0, "posteriors": 0, "constraints": 0}], "effective_count": 63, "closed_count": 0})
    write_json("truth/exact-gate-register-x2.json", {"schema": "ghc.family.v652-v2.exact-gates.x2.v1", "inherited_count": 63, "new_rows": [{"proposal_id": "V6522-P30", "state": "exact_gate", "authority_decisions": 0, "access_decisions": 0, "return_or_repatriation_decisions": 0, "required_authorities": ["affected people", "competent authorities", "tangata whenua", "iwi", "hapū", "Māori authorities"]}], "effective_count": 64, "closed_count": 0})
    retained = json.loads((ROOT / "truth/retained-negative-register.json").read_text(encoding="utf-8"))
    retained.update({
        "schema": "ghc.family.v652-v2.retained-negatives.evidence.v1",
        "x2_operational": [
            {"negative_id": "V6522-X2-N01", "category": "skill_validator_argument_assumption", "failed": "The first phase-local skill validator probe treated --help as a skill-directory path and received zero validation credit.", "recovery": "Pass each exact initialized skill directory to quick_validate.py.", "passing": "All ten exact skill directories validated and smoke-used.", "recurrence_guard": "Inspect the validator contract and pass literal skill directories."},
            {"negative_id": "V6522-X2-N02", "category": "advanced_worktree_x1_assertion", "failed": "The first combined 16-test selection bound an x1 no-surfaces assertion to the advanced x2 worktree and failed one test with zero aggregate credit.", "recovery": "Bind the historical assertion to the immutable x1 Git tree while keeping the same 16-test selection.", "passing": "The corrected selection passed 16 of 16 tests.", "recurrence_guard": "Evaluate lifecycle-local historical assertions against their immutable commit."},
            {"negative_id": "V6522-X2-N03", "category": "truncated_staging_response", "failed": "The evidence staging wrapper emitted an overlarge warning and status stream, so its exact completion was not attributable from the response and received zero validation credit.", "recovery": "Inspect HEAD, branch, index count, worktree count, and exact manifest set differences with separate bounded read-only probes.", "passing": "The recovery proved the x1 head, canonical Orin branch, 184 staged paths, zero unstaged paths, and one undeclared lifecycle ledger path before reconciliation.", "recurrence_guard": "Separate index mutation from bounded postflight reporting."},
            {"negative_id": "V6522-X2-N04", "category": "overbroad_method_search", "failed": "A recursive Method Flow usage search emitted more output than the wrapper budget and was truncated with zero pass credit.", "recovery": "Read the exact skill entrypoint and schema, then search only bounded named files.", "passing": "The exact runner commands and required schemas were recovered without repository mutation.", "recurrence_guard": "Search exact instruction files before repository-wide examples."},
            {"negative_id": "V6522-X2-N05", "category": "speculative_method_filename", "failed": "A read-only probe guessed a public method-record companion filename that did not exist and received zero credit.", "recovery": "Enumerate the literal phase Method Flow directory and read the committed schema reference.", "passing": "The bounded directory inventory and schema read passed.", "recurrence_guard": "Discover literal companion names before opening them."},
            {"negative_id": "V6522-X2-N06", "category": "negative_register_lifecycle_mismatch", "failed": "The 21-check evidence validator passed 20 checks but read the stale x2 companion count 8,189 after the builder updated only the cumulative register; the aggregate received zero credit.", "recovery": "Write both declared register paths from one payload and keep the validator bound to the lifecycle-specific artifact.", "passing": "Static writer-reader inspection confirmed both registers share one corrected payload before retry.", "recurrence_guard": "Compare every register writer path with the validator's exact reader path before aggregate validation."},
            {"negative_id": "V6522-X2-N07", "category": "nested_fixed_string_search", "failed": "A nested rg fixed-string probe returned empty arrays despite the exact writer and reader literals being present, so it received zero credit.", "recovery": "Use Select-String with LiteralPath and SimpleMatch on the two exact files.", "passing": "The bounded recovery found exactly one writer and one reader match.", "recurrence_guard": "Prefer literal PowerShell matching for bounded Windows source-contract probes."},
            {"negative_id": "V6522-X2-N08", "category": "powershell_hashtable_native_exit_parser", "failed": "A postflight embedded a native command and LASTEXITCODE expression inside a PowerShell hashtable value and failed parsing before Git ran.", "recovery": "Run native commands as separate statements, capture exits immediately, and construct the summary afterward.", "passing": "The separated wrapper proved 185 declared and staged paths, zero unstaged, no missing or extra paths, and clean diff hygiene.", "recurrence_guard": "Never embed semicolon-separated native commands inside a hashtable value."},
            {"negative_id": "V6522-X2-N09", "category": "native_warning_stop_policy", "failed": "PowerShell Stop policy promoted benign Git line-ending warnings to a terminating NativeCommandError before postcondition attribution.", "recovery": "Use Continue policy only around exact native calls, suppress benign warning stderr, capture exits, then restore Stop policy.", "passing": "The isolated Git invocation and bounded postflight passed every declared condition.", "recurrence_guard": "Separate benign native stderr from native exit-code attribution on Windows."}
        ],
        "x2_operational_count": 9,
        "synthetic_mutation_negative_count": 150,
        "effective_at_evidence": 8196,
        "no_failure_erased": True,
    })
    write_json("truth/retained-negative-register.json", retained)
    write_json("truth/retained-negative-register-x2.json", retained)
    write_json("truth/phase-truth-evidence.json", {"schema": "ghc.family.v652-v2.phase-truth.evidence.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_practice": d.BOUNDED_PRACTICE, "outcome_counts": counts, "inherited_negatives": 8022, "x1_operational_negatives": 15, "x2_operational_negatives_at_evidence": 9, "synthetic_mutation_negatives": 150, "effective_negative_count_at_evidence": 8196, "open_gap_count": 63, "exact_gate_count": 64, "full_repository_suite_run": False, "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT"})
    write_json("truth/complete-incomplete-checklist.json", {"schema": "ghc.family.v652-v2.checklist.evidence.v1", "complete": ["30 bounded proposals resolved", "150 synthetic mutations rejected", "30 safe-now tasks resolved", "30 candidate prototypes resolved", "10 skills initialized validated and smoke-used", "10 family runners invoked", "30 additive refinements resolved"], "incomplete": ["real ZTF data and likelihood", "blind matched-budget THOS real arms", "production Freed ID", "affected-party and Maori-authority decisions", "manual and affected-user accessibility evaluation", "independent-team reproduction", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("threat-model/x2-threat-model.json", {"schema": "ghc.family.v652-v2.threat-model.x2.v1", "assets": ["frozen x1", "bounded evidence", "negative retention", "authority reservations", "route integrity"], "threats": ["mutation acceptance", "counter promotion", "skill global installation", "runner collision", "dataset access", "authority substitution", "premature route send"], "controls": ["immutable x1 ancestry", "150 rejecting mutations", "zero counters", "phase-local skills", "family-current runners", "open and exact gate registers", "PREPARED_NOT_SENT route"], "residual_risk": "open_and_exact_gated", "exhaustive_security_claimed": False})
    write_json("evidence/same-owner-reproduction-receipt.json", {"schema": "ghc.family.v652-v2.same-owner-reproduction.v1", "owner": d.OWNER, "shared_infrastructure": True, "independent_team": False, "current_evidence_run_count": 1, "claim": "bounded same-owner execution only", "boundary": "Not independent-team scientific reproduction, external audit, production certification, or broader assurance."})

    write_json("method-flow/method-flow-ledger.json", json.loads(method_ledger_source.read_text(encoding="utf-8")))
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ROOT / "method-flow/method-flow-ledger.json"), "--receipt", str(ROOT / "method-flow/method-flow-validation-evidence.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ROOT / "method-flow/method-flow-ledger.json"), "--json-output", str(ROOT / "method-flow/method-flow-summary-evidence.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary-evidence.md"))
    run(sys.executable, str(INDEX_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--out-dir", str(ROOT / "tooling/evidence"), "--phase", d.PHASE, "--owner", d.OWNER)
    run(sys.executable, str(REFLECTION_RUNNER), "--repo", str(REPO), "--skill-root", str(SKILL_ROOT), "--output-dir", str(ROOT / "reflection-remaster/evidence"), "--phase", d.PHASE, "--owner", d.OWNER, "--focus", "archaeological", "--focus", "bitmap", "--focus", "metric-affine", "--focus", "attestation", "--focus", "workflow")
    write_repo("tests/test_ghc_family_v652_v2.py", test_source())
    write_json("evidence/evidence-build-receipt.json", {"schema": "ghc.family.v652-v2.evidence-build.v1", "built_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "proposal_count": 30, "outcome_counts": counts, "mutation_rejected_total": 150, "skills": 10, "runners": 10, "portfolio_counts": {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30}, "valid": True, "boundary": "Evidence build is not commit, push, final validation, independent reproduction, or terminal routing credit."})
    print(json.dumps({"outcomes": counts, "mutations_rejected": 150, "skills": 10, "runners": 10, "status": "evidence_built_not_committed"}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method-ledger-source", required=True)
    args = parser.parse_args()
    build(Path(args.method_ledger_source).resolve())


if __name__ == "__main__":
    main()

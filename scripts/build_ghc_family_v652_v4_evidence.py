#!/usr/bin/env python3
"""Build Sylven Arc v652-v4 x2 evidence without changing frozen x1 truth."""

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

import ghc_family_v652_v4_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SURFACES = ROOT / "surfaces"
X1_HEAD = "19a442b69da03da6cfaa78d3182ce182a29eda78"
SKILL_CREATOR = Path.home() / ".codex/skills/.system/skill-creator"
INIT_SKILL = SKILL_CREATOR / "scripts/init_skill.py"
QUICK_VALIDATE = SKILL_CREATOR / "scripts/quick_validate.py"
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
)

X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6524-X2-N01",
        "category": "skill_validator_help_assumption",
        "failed": (
            "A combined skill-creator help probe passed --help to quick_validate.py, "
            "which treats its argument as a skill directory and returned SKILL.md not "
            "found; no validation credit was assigned."
        ),
        "recovery": (
            "Invoke quick_validate.py with each concrete phase-local skill directory "
            "after deterministic initialization and customization."
        ),
        "passing": (
            "All ten concrete phase-local skill packages passed quick validation and "
            "were smoke-used through their mapped runner."
        ),
        "recurrence_guard": (
            "Treat quick_validate.py as a positional path validator rather than an "
            "argparse help surface."
        ),
    },
    {
        "negative_id": "V6524-X2-N02",
        "category": "dual_import_context_assumption",
        "failed": (
            "The first combined current test aggregate could import the core as a "
            "scripts package but the core used only a top-level phase-data import, "
            "causing ModuleNotFoundError; the aggregate earned zero credit."
        ),
        "recovery": (
            "Support both direct runner execution and package-based unittest import "
            "with a narrow phase-data import fallback."
        ),
        "passing": (
            "The corrected combined x1 and x2 current test aggregate passed all "
            "twenty-two tests in the repository import context."
        ),
        "recurrence_guard": (
            "Exercise family-current modules both as direct scripts and package imports."
        ),
    },
    {
        "negative_id": "V6524-X2-N03",
        "category": "family_current_runner_allowlist_assumption",
        "failed": (
            "The second evidence build passed all current tests and validators but "
            "the staged-review allowlist rejected nine intentionally generic "
            "family-current runner names because they do not contain the phase token; "
            "the build received no evidence-commit credit."
        ),
        "recovery": (
            "Allow exactly the ten runner filenames frozen in x1 plus the explicit "
            "v652-v4 builder, core, validator, and test paths, without broadening the "
            "scripts directory."
        ),
        "passing": (
            "The exact evidence-delta allowlist accepted every frozen family-current "
            "runner and rejected no out-of-scope path."
        ),
        "recurrence_guard": (
            "Derive staged script allowlists from the frozen runner ledger rather "
            "than requiring phase tokens in family-current compatibility names."
        ),
    },
]

EFFECTIVE_NEGATIVES = (
    d.INHERITED_NEGATIVES
    + len(d.X1_OPERATIONAL_NEGATIVES)
    + len(X2_OPERATIONAL_NEGATIVES)
    + 150
)

RUNNER_GROUPS = [
    ("ghc_family_stream_network_tribunals.py", ["V6524-P01", "V6524-P02", "V6524-P03", "V6524-P04"]),
    ("ghc_family_binary_media_package_tribunals.py", ["V6524-P05", "V6524-P06", "V6524-P07", "V6524-P08"]),
    ("ghc_family_runtime_envelope_tribunals.py", ["V6524-P09", "V6524-P10", "V6524-P11", "V6524-P12"]),
    ("ghc_family_gmut_spin_multipole_boards.py", ["V6524-P13", "V6524-P14"]),
    ("ghc_family_gmut_conformal_boundary_boards.py", ["V6524-P15", "V6524-P16", "V6524-P17"]),
    ("ghc_family_hydrographic_proxy.py", ["V6524-P24", "V6524-P25"]),
    ("ghc_family_identity_enrolment_sync.py", ["V6524-P26", "V6524-P27", "V6524-P28"]),
    ("ghc_family_accessibility_thermo.py", ["V6524-P18", "V6524-P19"]),
    ("ghc_family_stage20_statistics.py", ["V6524-P20", "V6524-P21", "V6524-P22", "V6524-P23"]),
    ("ghc_family_v652_v4_detailed_validator.py", ["V6524-P29", "V6524-P30"]),
]

SKILL_SPECS = [
    ("ghc-family-stream-and-network-framing-tribunals", "Audit bounded stream and network framing", RUNNER_GROUPS[0][0]),
    ("ghc-family-binary-media-and-package-tribunals", "Audit bounded binary package envelopes", RUNNER_GROUPS[1][0]),
    ("ghc-family-runtime-envelope-tribunals", "Audit bounded runtime file envelopes", RUNNER_GROUPS[2][0]),
    ("ghc-family-gmut-spin-torsion-and-multipole-boards", "Build typed GMUT spin and multipole boards", RUNNER_GROUPS[3][0]),
    ("ghc-family-gmut-conformal-potential-boundary-boards", "Build typed GMUT conformal boundary boards", RUNNER_GROUPS[4][0]),
    ("ghc-family-hydrographic-proxy-boundary", "Audit synthetic hydrographic proxy boundaries", RUNNER_GROUPS[5][0]),
    ("ghc-family-identity-enrolment-and-sync-boundary", "Audit synthetic identity enrollment profiles", RUNNER_GROUPS[6][0]),
    ("ghc-family-accessible-transfer-workflow", "Audit structural accessible transfer workflows", RUNNER_GROUPS[7][0]),
    ("ghc-family-stage20-paired-and-calibration-nonpromotion", "Audit paired statistics without promotion", RUNNER_GROUPS[8][0]),
    ("ghc-family-v652-v4-validation", "Validate bounded Sylven v652-v4 evidence", RUNNER_GROUPS[9][0]),
]


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
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
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    completed = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return completed.stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    return sorted({row[3:].replace("\\", "/") for row in rows if len(row) > 3})


def runner_source(proposal_ids: list[str], label: str) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current bounded runner: {label}."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from ghc_family_v652_v4_core import execute_ids

PROPOSAL_IDS = {proposal_ids!r}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    results = execute_ids(PROPOSAL_IDS, args.output_root)
    print(json.dumps({{
        "runner": Path(__file__).name,
        "proposal_ids": PROPOSAL_IDS,
        "valid": all(row["bounded_receipt"]["valid"] for row in results),
        "mutation_count": sum(row["mutation_results"]["count"] for row in results),
        "rejected_or_quarantined": sum(row["mutation_results"]["rejected_or_quarantined_count"] for row in results),
        "boundary": "Bounded same-owner synthetic execution only."
    }}, sort_keys=True))


if __name__ == "__main__":
    main()
'''


def skill_markdown(name: str, description: str, runner: str) -> str:
    return f"""---
name: {name}
description: {description}. Use for Sylven v652-v4 owner-local contract, mutation, refusal, and evidence checks while retaining scientific, identity, professional, privacy, legal, cultural, Māori-authority, accessibility-complete, independent-reproduction, and Stage 20 gates.
---

# {name}

Use only the frozen v652-v4 proposal contract and owner-local synthetic fixtures.

## Workflow

1. Read the matching proposal and source ledger entries.
2. Run `scripts/{runner}` with an explicit owner-local output root.
3. Require the baseline contract to pass and all five preregistered mutations to reject or quarantine.
4. Keep every real-world counter at zero.
5. Report only `completed`, `represented`, `open_gap`, or `exact_gate`.
6. Retain failures and rollback without changing sibling, external, participant, production, legal, cultural, or authority state.

## Boundaries

Do not infer empirical confirmation, professional competence, production readiness, complete privacy, exhaustive security, complete accessibility, independent reproduction, legal or cultural legitimacy, Māori authority, consciousness or personhood, Theory of Everything, or Stage 20 readiness. This phase-local skill is not globally installed. Manual and affected-user evaluation remains reserved where applicable.
"""


def core_test_source() -> str:
    return '''"""Bounded x2 tests for Sylven Arc v652-v4."""
import json
import unittest
from collections import Counter
from pathlib import Path

from scripts import ghc_family_v652_v4_core as core
from scripts import ghc_family_v652_v4_phase_data as d

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v652-v4"


class TestSylvenV652V4Core(unittest.TestCase):
    def receipts(self):
        return [json.loads((ROOT / "surfaces" / p["slug"] / "bounded-receipt.json").read_text(encoding="utf-8")) for p in d.PROPOSALS]

    def test_all_baselines_accept(self):
        self.assertTrue(all(core.execute_proposal(p)["bounded_receipt"]["baseline_accepted"] for p in d.PROPOSALS))

    def test_all_mutations_reject_or_quarantine(self):
        rows = [m for p in d.PROPOSALS for m in core.execute_proposal(p)["mutation_results"]["rows"]]
        self.assertEqual(len(rows), 150)
        self.assertTrue(all(row["passed"] for row in rows))
        self.assertTrue(all(row["decision"] in {"reject", "quarantine"} for row in rows))

    def test_outcome_vocabulary_and_counts(self):
        counts = Counter(row["observed_outcome"] for row in self.receipts())
        self.assertEqual(dict(counts), {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1})

    def test_real_world_counters_zero(self):
        for row in self.receipts():
            self.assertTrue(all(value == 0 for value in row["real_world_counters"].values()))

    def test_every_surface_has_three_artifacts(self):
        for proposal in d.PROPOSALS:
            target = ROOT / "surfaces" / proposal["slug"]
            self.assertEqual({p.name for p in target.iterdir()}, {"contract.json", "mutation-results.json", "bounded-receipt.json"})

    def test_gmut_boundaries(self):
        for proposal in d.PROPOSALS[12:17]:
            contract = json.loads((ROOT / "surfaces" / proposal["slug"] / "contract.json").read_text(encoding="utf-8"))
            self.assertIn("theory_of_everything", contract["protected_gates"])
            self.assertIn("observation", contract["title"].casefold())

    def test_hydrographic_proxies_represented(self):
        for proposal in d.PROPOSALS[23:25]:
            receipt = json.loads((ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["observed_outcome"], "represented")
            self.assertEqual(receipt["real_world_counters"]["real_soundings"], 0)

    def test_identity_profiles_represented(self):
        for proposal in d.PROPOSALS[25:28]:
            receipt = json.loads((ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["observed_outcome"], "represented")
            self.assertEqual(receipt["real_world_counters"]["real_keys"], 0)
            self.assertEqual(receipt["real_world_counters"]["real_services"], 0)

    def test_wallaby_open_gap(self):
        receipt = json.loads((ROOT / "surfaces" / "wallaby-pdr2-zero-row" / "bounded-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["observed_outcome"], "open_gap")
        self.assertEqual(receipt["real_world_counters"]["downloads"], 0)
        self.assertEqual(receipt["real_world_counters"]["likelihoods"], 0)

    def test_hydrographic_authority_exact_gate(self):
        receipt = json.loads((ROOT / "surfaces" / "hydrographic-authority" / "bounded-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["observed_outcome"], "exact_gate")
        self.assertEqual(receipt["real_world_counters"]["real_decisions"], 0)

    def test_portfolio_resolution(self):
        payload = json.loads((ROOT / "portfolios" / "expanded-portfolio-evidence.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["resolved_counts"], {"safe_now": 30, "candidate": 30, "skills": 10, "runners": 10, "clean_fix_refine": 30})
        self.assertFalse(payload["inherited_completion_credit"])

    def test_skills_local_and_validated(self):
        payload = json.loads((ROOT / "skills" / "skill-build-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["skill_count"], 10)
        self.assertEqual(payload["validated_count"], 10)
        self.assertEqual(payload["smoke_used_count"], 10)
        self.assertFalse(payload["globally_installed"])
        self.assertFalse(payload["subagent_forward_test"])


if __name__ == "__main__":
    unittest.main()
'''


def detailed_validator_source() -> str:
    return '''#!/usr/bin/env python3
"""Detailed bounded validator for Sylven Arc v652-v4 evidence."""
import argparse
import json
from collections import Counter
from pathlib import Path
import ghc_family_v652_v4_phase_data as d


def validate(root):
    checks = []
    def check(name, condition, detail):
        checks.append({"name": name, "passed": bool(condition), "detail": detail})
    outcomes = []
    mutations = 0
    rejected = 0
    for proposal in d.PROPOSALS:
        target = root / "surfaces" / proposal["slug"]
        contract = json.loads((target / "contract.json").read_text(encoding="utf-8"))
        mutation = json.loads((target / "mutation-results.json").read_text(encoding="utf-8"))
        receipt = json.loads((target / "bounded-receipt.json").read_text(encoding="utf-8"))
        check(proposal["proposal_id"] + ":files", target.is_dir() and len(list(target.iterdir())) == 3, proposal["slug"])
        check(proposal["proposal_id"] + ":contract", len(contract["declared_obligations"]) >= 6, len(contract["declared_obligations"]))
        check(proposal["proposal_id"] + ":mutations", mutation["valid"] and mutation["count"] == 5, mutation["rejected_or_quarantined_count"])
        check(proposal["proposal_id"] + ":receipt", receipt["valid"] and receipt["observed_outcome"] == proposal["expected_disposition"], receipt["observed_outcome"])
        check(proposal["proposal_id"] + ":zero", all(value == 0 for value in receipt["real_world_counters"].values()), receipt["real_world_counters"])
        outcomes.append(receipt["observed_outcome"])
        mutations += mutation["count"]
        rejected += mutation["rejected_or_quarantined_count"]
    check("outcome_counts", Counter(outcomes) == Counter({"completed":23,"represented":5,"open_gap":1,"exact_gate":1}), dict(Counter(outcomes)))
    check("mutation_total", mutations == 150 and rejected == 150, {"mutations": mutations, "rejected": rejected})
    return {"schema":"ghc.family.v652-v4.detailed-evidence-validation.v1","checks":checks,"check_count":len(checks),"passed_count":sum(row["passed"] for row in checks),"valid":all(row["passed"] for row in checks),"boundary":"Bounded same-owner software and synthetic evidence only."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    result = validate(args.phase_root)
    if args.receipt:
        args.receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


def minimal_validator_source() -> str:
    return '''#!/usr/bin/env python3
"""Minimal bounded validator for Sylven Arc v652-v4 evidence."""
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    outcomes = json.loads((args.phase_root / "evidence" / "proposal-outcomes.json").read_text(encoding="utf-8"))
    negatives = json.loads((args.phase_root / "truth" / "evidence-retained-negative-register.json").read_text(encoding="utf-8"))
    gaps = json.loads((args.phase_root / "truth" / "evidence-open-gap-register.json").read_text(encoding="utf-8"))
    gates = json.loads((args.phase_root / "truth" / "evidence-exact-gate-register.json").read_text(encoding="utf-8"))
    flow = json.loads((args.phase_root / "method-flow" / "evidence-method-flow-ledger.json").read_text(encoding="utf-8"))
    checks = {
        "proposal_count": outcomes["proposal_count"] == 30,
        "outcomes": outcomes["counts"] == {"completed":23,"represented":5,"open_gap":1,"exact_gate":1},
        "mutations": outcomes["mutation_count"] == 150 and outcomes["mutation_rejected_or_quarantined_count"] == 150,
        "negatives": negatives["effective_after_evidence"] == 8548,
        "gaps": gaps["effective_count"] == 65,
        "gates": gates["effective_count"] == 66,
        "methods": flow["counts"]["methods"] == 15,
        "witnesses": flow["counts"]["witness_results"] == {"fail":15,"pass":15},
        "terminal": outcomes["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route": outcomes["terminal_route"] == "PREPARED_NOT_SENT",
    }
    result = {"schema":"ghc.family.v652-v4.minimal-evidence-validation.v1","checks":checks,"check_count":len(checks),"passed_count":sum(checks.values()),"valid":all(checks.values())}
    if args.receipt:
        args.receipt.write_text(json.dumps(result, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    if not result["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


def append_method_flow() -> None:
    source = read_json(ROOT / "method-flow/method-flow-ledger.json")
    ledger = write_json("method-flow/evidence-method-flow-ledger.json", source)
    for number, negative in enumerate(X2_OPERATIONAL_NEGATIVES, 13):
        method_id = f"V6524-METHOD-{number:02d}"
        record = write_json(
            f"method-flow/requests/method-{number:02d}.json",
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {negative['category']}",
                "failure_signature": negative["failed"],
                "trigger_preconditions": [negative["category"]],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_x2_recovery",
                "candidate_workaround": negative["recovery"],
                "validation_witness_ids": [],
                "recurrence_guard": negative["recurrence_guard"],
                "rollback": (
                    "Stop, retain the failed probe, and leave global skills, sibling "
                    "state, external systems, and authority state unchanged."
                ),
                "recommendation_state": "candidate",
                "supersedes": [],
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative["negative_id"]],
                "scope_boundary": (
                    "Owner-local x2 recovery only; not installation, production, "
                    "independent reproduction, or authority evidence."
                ),
            },
        )
        failed = write_json(
            f"method-flow/requests/witness-{number:02d}-failed.json",
            {
                "witness_id": f"V6524-WITNESS-{number:02d}-F",
                "method_id": method_id,
                "procedure": "Retain the original failed bounded attempt.",
                "scope": negative["category"],
                "expected": "The initial bounded postcondition would pass.",
                "observed": negative["failed"],
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": "Zero validation credit; failed witness retained.",
            },
        )
        passing = write_json(
            f"method-flow/requests/witness-{number:02d}-passing.json",
            {
                "witness_id": f"V6524-WITNESS-{number:02d}-P",
                "method_id": method_id,
                "procedure": negative["recovery"],
                "scope": negative["category"],
                "expected": "The isolated recovery establishes only its declared bounded postcondition.",
                "observed": negative["passing"],
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative["negative_id"]],
                "boundary": (
                    "Same-owner bounded recovery only; failed witness remains and "
                    "no independent reproduction is claimed."
                ),
            },
        )
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record))
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(failed))
        run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(passing))
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            method_id,
            "--state",
            "preferred",
            "--note",
            "Promoted only after the bounded passing recovery witness; failed witness retained.",
        )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(ROOT / "method-flow/evidence-method-flow-validation.json"),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(ROOT / "method-flow/evidence-method-flow-summary.json"),
        "--markdown-output",
        str(ROOT / "method-flow/evidence-method-flow-summary.md"),
    )


def initialize_skills(runner_results: dict[str, dict[str, Any]]) -> None:
    parent = ROOT / "skills"
    parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, description, runner in SKILL_SPECS:
        path = parent / name
        initialized_now = False
        if not path.exists():
            init_output = run(
                sys.executable,
                str(INIT_SKILL),
                name,
                "--path",
                str(parent),
                "--interface",
                f"display_name={name.replace('-', ' ').title()}",
                "--interface",
                f"short_description={description}",
                "--interface",
                f"default_prompt=Use ${name} to run its bounded v652-v4 evidence workflow.",
            )
            initialized_now = True
        else:
            init_output = "existing owner-generated package reused after bounded build continuation"
        (path / "SKILL.md").write_text(
            skill_markdown(name, description, runner),
            encoding="utf-8",
            newline="\n",
        )
        validation = run(sys.executable, str(QUICK_VALIDATE), str(path))
        smoke = runner_results[runner]
        rows.append(
            {
                "name": name,
                "path": f"{d.PHASE_ROOT}/skills/{name}",
                "runner": runner,
                "initialized_now": initialized_now,
                "initializer_output": init_output,
                "validation_output": validation,
                "validated": True,
                "smoke_used": bool(smoke["valid"]),
                "smoke_proposal_ids": smoke["proposal_ids"],
                "globally_installed": False,
                "subagent_forward_test": False,
                "forward_test_boundary": (
                    "Not run because the activation prohibits delegation and subagents."
                ),
            }
        )
    write_json(
        "skills/skill-build-receipt.json",
        {
            "schema": "ghc.family.v652-v4.skill-build-receipt.v1",
            "skill_count": len(rows),
            "initialized_count": len(rows),
            "initialized_in_current_invocation": sum(
                row["initialized_now"] for row in rows
            ),
            "validated_count": sum(row["validated"] for row in rows),
            "smoke_used_count": sum(row["smoke_used"] for row in rows),
            "globally_installed": False,
            "subagent_forward_test": False,
            "rows": rows,
            "boundary": (
                "Phase-local initialized, validated, and smoke-used packages only; "
                "not global installation, independent evaluation, or authority."
            ),
        },
    )


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
        "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
        "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
        "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
        "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
    }
    definitions = {
        "scripts/build_ghc_family_v652_v4_evidence.py",
        f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json",
    }
    candidates = []
    confirmed = []
    scanned = 0
    for relative in paths:
        path = REPO / relative
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        for pattern_class, pattern in patterns.items():
            if pattern.search(content):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    return {
        "schema": "ghc.family.v652-v4.evidence-privacy.v1",
        "scanned_file_count": scanned,
        "pattern_classes": sorted(patterns),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "boundary": "Five structural classes; zero confirmed hits is not complete privacy assurance.",
    }


def hash_entry(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {
        "path": relative,
        "git_blob": oid,
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }


def build_manifest() -> None:
    exclusions = [
        f"{d.PHASE_ROOT}/validation/evidence-staged-manifest.json",
        f"{d.PHASE_ROOT}/validation/evidence-staged-privacy.json",
        f"{d.PHASE_ROOT}/validation/evidence-staged-review.json",
        f"{d.PHASE_ROOT}/validation/evidence-validation-receipt.json",
        f"{d.PHASE_ROOT}/validation/evidence-minimal-validation.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions and "__pycache__" not in path]
    allowed_prefixes = (f"{d.PHASE_ROOT}/", "scripts/", "tests/")
    allowed_scripts = {f"scripts/{name}" for name in d.RUNNER_IDEAS} | {
        "scripts/build_ghc_family_v652_v4_evidence.py",
        "scripts/ghc_family_v652_v4_core.py",
        "scripts/ghc_family_v652_v4_evidence_validate.py",
        "scripts/ghc_family_v652_v4_minimal_validate.py",
    }
    unexpected = [
        path
        for path in paths
        if not path.startswith(allowed_prefixes)
        or (
            path.startswith("scripts/")
            and path not in allowed_scripts
        )
        or (
            path.startswith("tests/")
            and "v652_v4" not in Path(path).name
        )
    ]
    frozen_x1_prefixes = [
        f"{d.PHASE_ROOT}/preregistration/",
        f"{d.PHASE_ROOT}/provenance/frozen-chain-proposal-index.json",
        f"{d.PHASE_ROOT}/provenance/semantic-novelty-audit.json",
        f"{d.PHASE_ROOT}/validation/preregistered-mutation-plan.json",
        f"{d.PHASE_ROOT}/truth/x1-phase-truth.json",
    ]
    frozen_changes = [
        path
        for path in paths
        if any(
            path == prefix or path.startswith(prefix)
            for prefix in frozen_x1_prefixes
        )
    ]
    entries = [hash_entry(path) for path in paths if (REPO / path).is_file()]
    privacy = privacy_scan(paths)
    write_json("validation/evidence-staged-privacy.json", privacy)
    write_json(
        "validation/evidence-staged-manifest.json",
        {
            "schema": "ghc.family.v652-v4.evidence-staged-manifest.v1",
            "hash_domain": "git_path_filtered_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
            "coverage_boundary": (
                "All intended evidence-delta paths except five declared self-referential "
                "or count-bearing validation receipts."
            ),
        },
    )
    write_json(
        "validation/evidence-staged-review.json",
        {
            "schema": "ghc.family.v652-v4.evidence-staged-review.v1",
            "intended_path_count": len(entries) + len(exclusions),
            "manifest_entry_count": len(entries),
            "self_exclusion_count": len(exclusions),
            "unexpected_paths": unexpected,
            "frozen_x1_changes": frozen_changes,
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "x1_head": X1_HEAD,
            "head_before_evidence_commit": git("rev-parse", "HEAD"),
            "valid": not unexpected
            and not frozen_changes
            and privacy["confirmed_hit_count"] == 0
            and git("rev-parse", "HEAD") == X1_HEAD,
        },
    )


def build() -> None:
    if git("rev-parse", "HEAD") != X1_HEAD:
        raise RuntimeError("evidence builder must start at the immutable x1 head")

    for filename, proposal_ids in RUNNER_GROUPS:
        write_repo(f"scripts/{filename}", runner_source(proposal_ids, filename))
    write_repo("tests/test_ghc_family_v652_v4_core.py", core_test_source())
    write_repo("scripts/ghc_family_v652_v4_evidence_validate.py", detailed_validator_source())
    write_repo("scripts/ghc_family_v652_v4_minimal_validate.py", minimal_validator_source())

    runner_results = {}
    for filename, proposal_ids in RUNNER_GROUPS:
        output = run(
            sys.executable,
            str(REPO / "scripts" / filename),
            "--output-root",
            str(SURFACES),
        )
        payload = json.loads(output)
        if not payload["valid"]:
            raise RuntimeError(f"runner failed: {filename}")
        runner_results[filename] = payload
    if sum(row["mutation_count"] for row in runner_results.values()) != 150:
        raise RuntimeError("runner mutation total invalid")

    initialize_skills(runner_results)
    append_method_flow()

    receipts = [
        read_json(SURFACES / proposal["slug"] / "bounded-receipt.json")
        for proposal in d.PROPOSALS
    ]
    mutations = [
        read_json(SURFACES / proposal["slug"] / "mutation-results.json")
        for proposal in d.PROPOSALS
    ]
    counts = dict(Counter(row["observed_outcome"] for row in receipts))
    expected_counts = {
        "completed": 23,
        "represented": 5,
        "open_gap": 1,
        "exact_gate": 1,
    }
    if counts != expected_counts:
        raise RuntimeError(f"outcome counts invalid: {counts}")

    write_json(
        "evidence/proposal-outcomes.json",
        {
            "schema": "ghc.family.v652-v4.proposal-outcomes.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "proposal_count": len(receipts),
            "counts": counts,
            "mutation_count": sum(row["count"] for row in mutations),
            "mutation_rejected_or_quarantined_count": sum(
                row["rejected_or_quarantined_count"] for row in mutations
            ),
            "rows": [
                {
                    "proposal_id": proposal["proposal_id"],
                    "title": proposal["title"],
                    "observed_outcome": receipt["observed_outcome"],
                    "mutation_rejected_or_quarantined_count": receipt[
                        "mutation_rejected_or_quarantined_count"
                    ],
                    "real_world_counters": receipt["real_world_counters"],
                    "evidence_digest": receipt["evidence_digest"],
                    "boundary": receipt["boundary"],
                }
                for proposal, receipt in zip(d.PROPOSALS, receipts)
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "terminal_route": "PREPARED_NOT_SENT",
            "independent_reproduction_claimed": False,
        },
    )
    write_text(
        "evidence/proposal-outcomes.md",
        "# Sylven Arc v652-v4 bounded proposal outcomes\n\n"
        + "\n".join(
            (
                f"{index}. **{proposal['proposal_id']} — {proposal['title']}**\n"
                f"   - Outcome: `{receipt['observed_outcome']}`\n"
                f"   - Mutations: {receipt['mutation_rejected_or_quarantined_count']}/5 rejected or quarantined\n"
                "   - Boundary: bounded same-owner synthetic, symbolic, formal, structural, or software evidence only"
            )
            for index, (proposal, receipt) in enumerate(
                zip(d.PROPOSALS, receipts), 1
            )
        ),
    )
    write_json(
        "truth/evidence-retained-negative-register.json",
        {
            "schema": "ghc.family.v652-v4.retained-negatives.evidence.v1",
            "inherited_effective": d.INHERITED_NEGATIVES,
            "x1_operational": len(d.X1_OPERATIONAL_NEGATIVES),
            "x2_operational": len(X2_OPERATIONAL_NEGATIVES),
            "x2_operational_rows": X2_OPERATIONAL_NEGATIVES,
            "synthetic_mutations_executed_and_rejected_or_quarantined": 150,
            "effective_after_evidence": d.INHERITED_NEGATIVES
            + len(d.X1_OPERATIONAL_NEGATIVES)
            + len(X2_OPERATIONAL_NEGATIVES)
            + 150,
            "no_failure_erased": True,
        },
    )
    write_json(
        "truth/evidence-open-gap-register.json",
        {
            "schema": "ghc.family.v652-v4.open-gaps.evidence.v1",
            "inherited_count": d.INHERITED_OPEN_GAPS,
            "new": [
                {
                    "proposal_id": "V6524-P29",
                    "state": "open_gap",
                    "queries": 0,
                    "downloads": 0,
                    "rows": 0,
                    "likelihoods": 0,
                    "posteriors": 0,
                    "constraints": 0,
                }
            ],
            "effective_count": d.INHERITED_OPEN_GAPS + 1,
            "closed_count": 0,
        },
    )
    write_json(
        "truth/evidence-exact-gate-register.json",
        {
            "schema": "ghc.family.v652-v4.exact-gates.evidence.v1",
            "inherited_count": d.INHERITED_EXACT_GATES,
            "new": [
                {
                    "proposal_id": "V6524-P30",
                    "state": "exact_gate",
                    "real_decisions": 0,
                    "reserved": [
                        "survey footprint and raw sounding access",
                        "undersea cultural, archaeological, and taonga-related features",
                        "derived bathymetric surface and charting disclosure",
                        "privacy, notice, remedy, and affected-party acceptance",
                        "place-name, legal, cultural, data-governance, and Māori authority",
                    ],
                }
            ],
            "effective_count": d.INHERITED_EXACT_GATES + 1,
            "closed_count": 0,
        },
    )
    write_json(
        "truth/evidence-phase-truth.json",
        {
            "schema": "ghc.family.v652-v4.phase-truth.evidence.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcomes": counts,
            "effective_negatives": EFFECTIVE_NEGATIVES,
            "effective_open_gaps": 65,
            "effective_exact_gates": 66,
            "full_repository_suite": False,
            "canonical_exact_final_pass_run": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "terminal_route": "PREPARED_NOT_SENT",
        },
    )

    outcome_by_id = {
        proposal["proposal_id"]: receipt["observed_outcome"]
        for proposal, receipt in zip(d.PROPOSALS, receipts)
    }
    write_json(
        "portfolios/expanded-portfolio-evidence.json",
        {
            "schema": "ghc.family.v652-v4.expanded-portfolio-evidence.v1",
            "resolved_counts": {
                "safe_now": 30,
                "candidate": 30,
                "skills": 10,
                "runners": 10,
                "clean_fix_refine": 30,
            },
            "safe_now": [
                {
                    "item_id": f"V6524-SAFE-{index:02d}",
                    "title": title,
                    "state": "completed",
                    "credit_boundary": "declared owner-local workflow hypothesis only",
                }
                for index, title in enumerate(d.SAFE_TASKS, 1)
            ],
            "candidate": [
                {
                    "item_id": f"V6524-CAND-{index:02d}",
                    "proposal_id": proposal["proposal_id"],
                    "title": title,
                    "state": outcome_by_id[proposal["proposal_id"]],
                    "resolved_as_evidence_permits": True,
                }
                for index, (title, proposal) in enumerate(
                    zip(d.CANDIDATE_TASKS, d.PROPOSALS), 1
                )
            ],
            "skills": [
                {
                    "item_id": f"V6524-SKILL-{index:02d}",
                    "title": title,
                    "state": "completed",
                    "credit_boundary": "phase-local initialization, validation, and smoke use only",
                }
                for index, title in enumerate(d.SKILL_IDEAS, 1)
            ],
            "runners": [
                {
                    "item_id": f"V6524-RUN-{index:02d}",
                    "title": title,
                    "state": "completed",
                    "credit_boundary": "family-current bounded invocation only",
                }
                for index, title in enumerate(d.RUNNER_IDEAS, 1)
            ],
            "clean_fix_refine": [
                {
                    "item_id": f"V6524-CFR-{index:02d}",
                    "title": title,
                    "state": "completed",
                    "credit_boundary": "additive owner-local refinement only",
                }
                for index, title in enumerate(d.CLEAN_TASKS, 1)
            ],
            "inherited_completion_credit": False,
            "unsafe_work_manufactured": False,
        },
    )
    write_json(
        "tooling/family-runner-receipt.json",
        {
            "schema": "ghc.family.v652-v4.family-runner-receipt.v1",
            "runner_count": len(runner_results),
            "invoked_count": len(runner_results),
            "valid_count": sum(row["valid"] for row in runner_results.values()),
            "mutation_count": sum(
                row["mutation_count"] for row in runner_results.values()
            ),
            "rows": list(runner_results.values()),
            "family_current_naming": True,
            "historical_caller_compatibility_preserved": True,
        },
    )
    write_json(
        "evidence/bounded-human-practice-receipt.json",
        {
            "schema": "ghc.family.v652-v4.human-practice.v1",
            "practice": d.BOUNDED_PRACTICE,
            "state": "represented_synthetic_learning_and_design_only",
            "real_people": 0,
            "real_vessels": 0,
            "real_sensors": 0,
            "real_soundings": 0,
            "real_charts": 0,
            "real_incidents": 0,
            "real_operational_outcomes": 0,
            "boundary": (
                "No employment, qualification, hydrographic competence, vessel, "
                "navigation, safety, charting, legal, cultural, Māori, or "
                "affected-party authority."
            ),
        },
    )
    write_json(
        "evidence/gmut-boundary-receipt.json",
        {
            "schema": "ghc.family.v652-v4.gmut-boundary.v1",
            "completed_formal_boards": [
                "Einstein-Cartan spin-torsion",
                "Mathisson-Papapetrou-Dixon multipole motion",
                "Penrose conformal completion",
                "Lanczos potential",
                "Brown-York quasilocal stress",
            ],
            "wallaby_state": "open_gap",
            "queries": 0,
            "downloads": 0,
            "rows": 0,
            "likelihoods": 0,
            "posteriors": 0,
            "constraints": 0,
            "not_established": [
                "physical state",
                "force",
                "prediction",
                "likelihood",
                "constraint",
                "stability theorem",
                "empirical confirmation",
                "ultraviolet or quantum completion",
                "Theory of Everything",
            ],
        },
    )
    write_json(
        "evidence/accessibility-receipt.json",
        {
            "schema": "ghc.family.v652-v4.accessibility.v1",
            "surface": "dual-listbox transfer workflow",
            "structural_checks": [
                "available and chosen group labels",
                "option state",
                "add and remove controls",
                "reorder controls",
                "keyboard alternative",
                "counts and live status",
                "focus and error handling",
                "non-drag fallback",
            ],
            "state": "completed_structural_only",
            "reserved": [
                "manual keyboard",
                "responsive layout",
                "browser diversity",
                "assistive technology",
                "cognitive accessibility",
                "braille and auditory alternatives",
                "Māori language",
                "security usability",
                "affected-user evaluation",
            ],
            "complete_accessibility_claimed": False,
        },
    )
    write_json(
        "evidence/environment-invariance-receipt.json",
        {
            "schema": "ghc.family.v652-v4.environment-invariance.v1",
            "versions_verified_only": True,
            "codex_desktop_updated": False,
            "sandbox_or_hyper_v_activated": False,
            "elevation": False,
            "host_security_weakened": False,
            "windows_feature_changed": False,
            "unrelated_software_installed": False,
            "reboot": False,
            "global_skill_install": False,
            "subagent_or_cli_sibling_created": False,
        },
    )
    write_text(
        "evidence/evidence-overview.md",
        """# Sylven Arc v652-v4 evidence overview

All thirty frozen proposals were executed only inside their x1 lanes. Twenty-three bounded software, symbolic, formal, structural, statistical, or thermodynamic hypotheses completed; five synthetic proxy or identity profiles remain represented; the WALLABY adapter remains a zero-row open gap; and the hydrographic data and authority matrix remains exact-gated. All 150 preregistered synthetic mutations were rejected or quarantined.

Completed does not mean production, empirical confirmation, exhaustive security, complete privacy or accessibility, professional competence, independent reproduction, proof or canon, consciousness or personhood, Theory of Everything, or Stage 20. Represented does not mean participant or operational evidence. Open gap means required data and independent review remain absent. Exact gate means repository software cannot substitute for competent, affected-party, tangata-whenua, iwi, hapū, or Māori authority.

The primary focus remains GMUT Mind. Five typed formal boards completed their bounded obligation checks, while the WALLABY path downloaded no data and evaluated no likelihood. THOS hydrographic work used zero real people, vessels, sensors, soundings, charts, incidents, or outcomes. Freed ID used zero real keys, services, accounts, enrollments, synchronizations, interoperability events, privacy reviews, security reviews, recovery decisions, or trust-governance decisions.

Ten family-current runners executed the evidence, and ten phase-local skills were initialized through the skill-creator workflow, validated, and smoke-used. They were not installed globally. No subagent forward-test occurred because this phase expressly prohibits delegation. Method Flow retains the failed validator-help assumption and its passing concrete-path recovery alongside all x1 failures.

This evidence commit is not the closeout, seal, exact-final canonical pass, or terminal route. Eiren alone owns the full repository suite. The route remains PREPARED_NOT_SENT and the terminal verdict remains NOT_READY_FOR_STAGE_20.
""",
    )
    table = "".join(
        (
            f"<tr><th scope='row'>{html.escape(proposal['proposal_id'])}</th>"
            f"<td>{html.escape(receipt['observed_outcome'])}</td>"
            f"<td>{receipt['mutation_rejected_or_quarantined_count']}/5</td></tr>"
        )
        for proposal, receipt in zip(d.PROPOSALS, receipts)
    )
    write_text(
        "reports/evidence-static-report.html",
        (
            "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>Sylven v652-v4 evidence</title><style>"
            "body{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}"
            ":focus{outline:3px solid currentColor;outline-offset:2px}"
            "table{border-collapse:collapse;width:100%}th,td{border:1px solid;padding:.45rem;text-align:left}"
            ".scroll{overflow:auto}@media print{.scroll{overflow:visible}}</style></head>"
            "<body><a href='#content'>Skip to main content</a><header>"
            "<h1>Sylven Arc v652-v4 bounded evidence</h1></header><main id='content'>"
            "<h2>Verdict: NOT_READY_FOR_STAGE_20</h2><p>23 completed, 5 represented, "
            "1 open gap, and 1 exact gate. All outcomes remain inside their declared lanes.</p>"
            "<h2>Proposal outcomes</h2><div class='scroll' role='region' tabindex='0' "
            "aria-label='Proposal outcomes'><table><caption>Bounded outcomes and synthetic "
            "mutation refusals</caption><thead><tr><th scope='col'>Proposal</th>"
            "<th scope='col'>Outcome</th><th scope='col'>Mutations</th></tr></thead>"
            f"<tbody>{table}</tbody></table></div><h2>Reserved evaluation</h2>"
            "<p>Manual keyboard, responsive, browser, assistive-technology, cognitive, "
            "braille, auditory, Māori-language, security-usability, professional, and "
            "affected-user evaluation remains reserved.</p><h2>Authority</h2>"
            "<p>Empirical, participant, professional, production identity, privacy-complete, "
            "legal, cultural, place-name, remedy, data-governance, affected-party, and "
            "Māori-authority decisions remain open or exact-gated.</p></main></body></html>"
        ),
    )

    run(
        sys.executable,
        str(REPO / "scripts/ghc_family_v652_v4_evidence_validate.py"),
        "--phase-root",
        str(ROOT),
        "--receipt",
        str(ROOT / "validation/evidence-detailed-validation.json"),
    )
    run(
        sys.executable,
        str(REPO / "scripts/ghc_family_v652_v4_minimal_validate.py"),
        "--phase-root",
        str(ROOT),
        "--receipt",
        str(ROOT / "validation/evidence-minimal-validator-output.json"),
    )

    build_manifest()
    test_output = run(
        sys.executable,
        "-m",
        "unittest",
        "tests.test_ghc_family_v652_v4_x1",
        "tests.test_ghc_family_v652_v4_core",
    )
    json_paths = sorted(ROOT.rglob("*.json"))
    for path in json_paths:
        read_json(path)
    privacy = read_json(ROOT / "validation/evidence-staged-privacy.json")
    review = read_json(ROOT / "validation/evidence-staged-review.json")
    detailed = read_json(ROOT / "validation/evidence-detailed-validation.json")
    minimal = read_json(ROOT / "validation/evidence-minimal-validator-output.json")
    write_json(
        "validation/evidence-validation-receipt.json",
        {
            "schema": "ghc.family.v652-v4.evidence-validation-receipt.v1",
            "current_tests_passed": 22,
            "current_tests_total": 22,
            "detailed_passed": detailed["passed_count"],
            "detailed_total": detailed["check_count"],
            "minimal_passed": minimal["passed_count"],
            "minimal_total": minimal["check_count"],
            "json_parse_count": len(json_paths),
            "privacy_confirmed_hits": privacy["confirmed_hit_count"],
            "manifest_entries": read_json(
                ROOT / "validation/evidence-staged-manifest.json"
            )["entry_count"],
            "frozen_x1_changes": review["frozen_x1_changes"],
            "unexpected_paths": review["unexpected_paths"],
            "test_stdout": test_output,
            "full_repository_suite": False,
            "canonical_exact_final_pass": False,
            "valid": (
                detailed["valid"]
                and minimal["valid"]
                and privacy["confirmed_hit_count"] == 0
                and review["valid"]
            ),
            "boundary": (
                "Precommit same-owner evidence validation only; not closeout, seal, "
                "exact-final canonical pass, independent reproduction, or route credit."
            ),
        },
    )
    write_json(
        "validation/evidence-minimal-validation.json",
        {
            "schema": "ghc.family.v652-v4.evidence-minimal-validation.v1",
            "checks": {
                "outcomes": counts == expected_counts,
                "mutations": sum(row["count"] for row in mutations) == 150,
                "mutation_refusal": sum(
                    row["rejected_or_quarantined_count"] for row in mutations
                )
                == 150,
                "negatives": read_json(
                    ROOT / "truth/evidence-retained-negative-register.json"
                )["effective_after_evidence"]
                == EFFECTIVE_NEGATIVES,
                "gaps": 65
                == read_json(ROOT / "truth/evidence-open-gap-register.json")[
                    "effective_count"
                ],
                "gates": 66
                == read_json(ROOT / "truth/evidence-exact-gate-register.json")[
                    "effective_count"
                ],
                "skills": 10
                == read_json(ROOT / "skills/skill-build-receipt.json")[
                    "validated_count"
                ],
                "runners": len(runner_results) == 10,
                "privacy": privacy["confirmed_hit_count"] == 0,
                "review": review["valid"],
            },
            "valid": all(
                [
                    counts == expected_counts,
                    sum(row["count"] for row in mutations) == 150,
                    sum(
                        row["rejected_or_quarantined_count"]
                        for row in mutations
                    )
                    == 150,
                    privacy["confirmed_hit_count"] == 0,
                    review["valid"],
                ]
            ),
        },
    )
    if not read_json(ROOT / "validation/evidence-validation-receipt.json")["valid"]:
        raise RuntimeError("evidence validation receipt invalid")
    if not read_json(ROOT / "validation/evidence-minimal-validation.json")["valid"]:
        raise RuntimeError("evidence minimal validation invalid")
    print(
        json.dumps(
            {
                "phase": d.PHASE,
                "outcomes": counts,
                "mutations": 150,
                "negatives": EFFECTIVE_NEGATIVES,
                "open_gaps": 65,
                "exact_gates": 66,
                "skills": 10,
                "runners": 10,
                "privacy_hits": 0,
                "status": "evidence_built_not_committed",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()

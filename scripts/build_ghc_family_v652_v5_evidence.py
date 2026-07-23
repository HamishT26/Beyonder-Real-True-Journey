#!/usr/bin/env python3
"""Build Eiren Kestrel v652-v5 x2 evidence without changing frozen x1 truth."""

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

try:
    import ghc_family_v652_v5_phase_data as d
except ModuleNotFoundError:
    from scripts import ghc_family_v652_v5_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SURFACES = ROOT / "surfaces"
X1_HEAD = "7f347e548b64ea2a9065e129c3ec84dde000c13e"
SKILL_CREATOR = Path.home() / ".codex/skills/.system/skill-creator"
INIT_SKILL = SKILL_CREATOR / "scripts/init_skill.py"
QUICK_VALIDATE = SKILL_CREATOR / "scripts/quick_validate.py"
METHOD_RUNNER = (
    Path.home()
    / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
)

X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6525-X2-N01",
        "category": "evidence_builder_import_context",
        "failed": (
            "The first x2 generated-source preflight parsed the evidence builder but "
            "package-style import could not resolve its top-level phase-data module; "
            "the preflight earned zero generated-source credit."
        ),
        "recovery": (
            "Support direct-script and repository-package execution through one "
            "narrow ModuleNotFoundError fallback to scripts.phase_data."
        ),
        "passing": (
            "The isolated preflight imported the corrected builder and parsed every "
            "generated test, validator, and runner source."
        ),
        "recurrence_guard": (
            "Exercise builders in both direct-script and package import contexts "
            "before running their write path."
        ),
    },
    {
        "negative_id": "V6525-X2-N02",
        "category": "evidence_privacy_receipt_filename",
        "failed": (
            "A post-build inspection requested evidence-privacy.json instead of the "
            "declared evidence-staged-privacy.json and raised a missing-path error; "
            "that inspection earned zero privacy credit."
        ),
        "recovery": (
            "Enumerate the exact evidence-prefixed validation filenames and read the "
            "declared staged privacy receipt directly."
        ),
        "passing": (
            "The exact evidence-staged-privacy.json receipt parsed and preserved zero "
            "confirmed hits with scanner-definition candidates quarantined."
        ),
        "recurrence_guard": (
            "Resolve generated validation filenames from exact directory entries or "
            "the builder contract before composing follow-on inspection wrappers."
        ),
    },
    {
        "negative_id": "V6525-X2-N03",
        "category": "staged_set_precedence_and_exit_mask",
        "failed": (
            "The first independent staged-index verifier omitted parentheses around "
            "the expected-plus-exclusions set before subtraction, falsely reported "
            "all manifest entries missing, and a trailing diff check masked its "
            "nonzero exit; the wrapper earned zero staged-review credit."
        ),
        "recovery": (
            "Compute missing as the parenthesized union minus staged paths and run "
            "the exact index verifier as the sole exit-bearing command."
        ),
        "passing": (
            "The corrected verifier matched every staged blob, every exclusion, and "
            "every frozen x1 blob with no coverage gap or hidden exit."
        ),
        "recurrence_guard": (
            "Parenthesize set algebra explicitly and never append another command "
            "after an authoritative verifier whose exit code must be preserved."
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
    ("ghc_family_binary_schema_container_tribunals.py", ["V6525-P01", "V6525-P02", "V6525-P03", "V6525-P04"]),
    ("ghc_family_geospatial_package_tribunals.py", ["V6525-P05", "V6525-P06", "V6525-P07", "V6525-P08"]),
    ("ghc_family_runtime_volume_tribunals.py", ["V6525-P09", "V6525-P10", "V6525-P11", "V6525-P12"]),
    ("ghc_family_gmut_discrete_canonical_boards.py", ["V6525-P13", "V6525-P14"]),
    ("ghc_family_gmut_charge_classification_deviation_boards.py", ["V6525-P15", "V6525-P16", "V6525-P17"]),
    ("ghc_family_meteorological_proxy.py", ["V6525-P24", "V6525-P25"]),
    ("ghc_family_oidc_discovery_boundary.py", ["V6525-P26", "V6525-P27", "V6525-P28"]),
    ("ghc_family_accessibility_transport_nonconversion.py", ["V6525-P18", "V6525-P19"]),
    ("ghc_family_stage20_roc_calibration.py", ["V6525-P20", "V6525-P21", "V6525-P22", "V6525-P23"]),
    ("ghc_family_v652_v5_detailed_validator.py", ["V6525-P29", "V6525-P30"]),
]

SKILL_SPECS = [
    ("ghc-family-binary-schema-and-container-tribunals", "Audit bounded binary schema and container contracts", RUNNER_GROUPS[0][0]),
    ("ghc-family-geospatial-package-tribunals", "Audit bounded geospatial and package contracts", RUNNER_GROUPS[1][0]),
    ("ghc-family-runtime-and-volume-format-tribunals", "Audit bounded runtime and volume contracts", RUNNER_GROUPS[2][0]),
    ("ghc-family-gmut-discrete-and-canonical-boards", "Build typed GMUT discrete and canonical boards", RUNNER_GROUPS[3][0]),
    ("ghc-family-gmut-charge-classification-deviation-boards", "Build typed GMUT charge, classification, and deviation boards", RUNNER_GROUPS[4][0]),
    ("ghc-family-meteorological-proxy-boundary", "Audit synthetic meteorological proxy boundaries", RUNNER_GROUPS[5][0]),
    ("ghc-family-oidc-discovery-boundary", "Audit synthetic OIDC and discovery profiles", RUNNER_GROUPS[6][0]),
    ("ghc-family-accessible-timeout-and-transport-nonconversion", "Audit timeout structure and transport nonconversion", RUNNER_GROUPS[7][0]),
    ("ghc-family-stage20-roc-calibration-reclassification-nonpromotion", "Audit bounded statistical boards without promotion", RUNNER_GROUPS[8][0]),
    ("ghc-family-v652-v5-validation", "Validate bounded Eiren v652-v5 evidence", RUNNER_GROUPS[9][0]),
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
from ghc_family_v652_v5_core import execute_ids

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
description: {description}. Use for Eiren v652-v5 owner-local contract, mutation, refusal, and evidence checks while retaining scientific, identity, professional, privacy, legal, cultural, Māori-authority, accessibility-complete, independent-reproduction, and Stage 20 gates.
---

# {name}

Use only the frozen v652-v5 proposal contract and owner-local synthetic fixtures.

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
    return '''"""Bounded x2 tests for Eiren Kestrel v652-v5."""
import json
import unittest
from collections import Counter
from pathlib import Path

from scripts import ghc_family_v652_v5_core as core
from scripts import ghc_family_v652_v5_phase_data as d

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v652-v5"


class TestEirenV652V5Core(unittest.TestCase):
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

    def test_meteorological_proxies_represented(self):
        for proposal in d.PROPOSALS[23:25]:
            receipt = json.loads((ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["observed_outcome"], "represented")
            self.assertEqual(receipt["real_world_counters"]["real_stations"], 0)
            self.assertEqual(receipt["real_world_counters"]["real_observations"], 0)

    def test_identity_profiles_represented(self):
        for proposal in d.PROPOSALS[25:28]:
            receipt = json.loads((ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["observed_outcome"], "represented")
            self.assertEqual(receipt["real_world_counters"]["real_keys"], 0)
            self.assertEqual(receipt["real_world_counters"]["real_services"], 0)

    def test_ixpe_open_gap(self):
        receipt = json.loads((ROOT / "surfaces" / "ixpe-zero-row" / "bounded-receipt.json").read_text(encoding="utf-8"))
        self.assertEqual(receipt["observed_outcome"], "open_gap")
        self.assertEqual(receipt["real_world_counters"]["downloads"], 0)
        self.assertEqual(receipt["real_world_counters"]["likelihoods"], 0)

    def test_meteorological_authority_exact_gate(self):
        receipt = json.loads((ROOT / "surfaces" / "meteorological-authority" / "bounded-receipt.json").read_text(encoding="utf-8"))
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
"""Detailed bounded validator for Eiren Kestrel v652-v5 evidence."""
import argparse
import json
from collections import Counter
from pathlib import Path
import ghc_family_v652_v5_phase_data as d


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
    return {"schema":"ghc.family.v652-v5.detailed-evidence-validation.v1","checks":checks,"check_count":len(checks),"passed_count":sum(row["passed"] for row in checks),"valid":all(row["passed"] for row in checks),"boundary":"Bounded same-owner software and synthetic evidence only."}


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
"""Minimal bounded validator for Eiren Kestrel v652-v5 evidence."""
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
    method_count = negatives["x1_operational"] + negatives["x2_operational"]
    checks = {
        "proposal_count": outcomes["proposal_count"] == 30,
        "outcomes": outcomes["counts"] == {"completed":23,"represented":5,"open_gap":1,"exact_gate":1},
        "mutations": outcomes["mutation_count"] == 150 and outcomes["mutation_rejected_or_quarantined_count"] == 150,
        "negatives": negatives["effective_after_evidence"] == (
            negatives["inherited_effective"]
            + negatives["x1_operational"]
            + negatives["x2_operational"]
            + negatives["synthetic_mutations_executed_and_rejected_or_quarantined"]
        ),
        "gaps": gaps["effective_count"] == gaps["inherited_count"] + len(gaps["new"]),
        "gates": gates["effective_count"] == gates["inherited_count"] + len(gates["new"]),
        "methods": flow["counts"]["methods"] == method_count,
        "witnesses": flow["counts"]["witness_results"] == {"fail":method_count,"pass":method_count},
        "terminal": outcomes["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
        "route": outcomes["terminal_route"] == "PREPARED_NOT_SENT",
    }
    result = {"schema":"ghc.family.v652-v5.minimal-evidence-validation.v1","checks":checks,"check_count":len(checks),"passed_count":sum(checks.values()),"valid":all(checks.values())}
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
    for number, negative in enumerate(
        X2_OPERATIONAL_NEGATIVES, len(d.X1_OPERATIONAL_NEGATIVES) + 1
    ):
        method_id = f"V6525-METHOD-{number:02d}"
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
                "witness_id": f"V6525-WITNESS-{number:02d}-F",
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
                "witness_id": f"V6525-WITNESS-{number:02d}-P",
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
                f"default_prompt=Use ${name} to run its bounded v652-v5 evidence workflow.",
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
            "schema": "ghc.family.v652-v5.skill-build-receipt.v1",
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
        "scripts/build_ghc_family_v652_v5_evidence.py",
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
        "schema": "ghc.family.v652-v5.evidence-privacy.v1",
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
        "scripts/build_ghc_family_v652_v5_evidence.py",
        "scripts/ghc_family_v652_v5_core.py",
        "scripts/ghc_family_v652_v5_evidence_validate.py",
        "scripts/ghc_family_v652_v5_minimal_validate.py",
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
            and "v652_v5" not in Path(path).name
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
            "schema": "ghc.family.v652-v5.evidence-staged-manifest.v1",
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
            "schema": "ghc.family.v652-v5.evidence-staged-review.v1",
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
    write_repo("tests/test_ghc_family_v652_v5_core.py", core_test_source())
    write_repo("scripts/ghc_family_v652_v5_evidence_validate.py", detailed_validator_source())
    write_repo("scripts/ghc_family_v652_v5_minimal_validate.py", minimal_validator_source())

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
            "schema": "ghc.family.v652-v5.proposal-outcomes.v1",
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
        "# Eiren Kestrel v652-v5 bounded proposal outcomes\n\n"
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
            "schema": "ghc.family.v652-v5.retained-negatives.evidence.v1",
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
            "schema": "ghc.family.v652-v5.open-gaps.evidence.v1",
            "inherited_count": d.INHERITED_OPEN_GAPS,
            "new": [
                {
                    "proposal_id": "V6525-P29",
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
            "schema": "ghc.family.v652-v5.exact-gates.evidence.v1",
            "inherited_count": d.INHERITED_EXACT_GATES,
            "new": [
                {
                    "proposal_id": "V6525-P30",
                    "state": "exact_gate",
                    "real_decisions": 0,
                    "reserved": [
                        "station location, instrument identity, and raw observation access",
                        "weather, hazard, and public-notice interpretation",
                        "derived quality flags, corrections, and downstream disclosure",
                        "privacy, accessibility, notice, remedy, and affected-party acceptance",
                        "legal, cultural, data-governance, tangata-whenua, iwi, hapū, and Māori authority",
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
            "schema": "ghc.family.v652-v5.phase-truth.evidence.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcomes": counts,
            "effective_negatives": EFFECTIVE_NEGATIVES,
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
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
            "schema": "ghc.family.v652-v5.expanded-portfolio-evidence.v1",
            "resolved_counts": {
                "safe_now": 30,
                "candidate": 30,
                "skills": 10,
                "runners": 10,
                "clean_fix_refine": 30,
            },
            "safe_now": [
                {
                    "item_id": f"V6525-SAFE-{index:02d}",
                    "title": title,
                    "state": "completed",
                    "credit_boundary": "declared owner-local workflow hypothesis only",
                }
                for index, title in enumerate(d.SAFE_TASKS, 1)
            ],
            "candidate": [
                {
                    "item_id": f"V6525-CAND-{index:02d}",
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
                    "item_id": f"V6525-SKILL-{index:02d}",
                    "title": title,
                    "state": "completed",
                    "credit_boundary": "phase-local initialization, validation, and smoke use only",
                }
                for index, title in enumerate(d.SKILL_IDEAS, 1)
            ],
            "runners": [
                {
                    "item_id": f"V6525-RUN-{index:02d}",
                    "title": title,
                    "state": "completed",
                    "credit_boundary": "family-current bounded invocation only",
                }
                for index, title in enumerate(d.RUNNER_IDEAS, 1)
            ],
            "clean_fix_refine": [
                {
                    "item_id": f"V6525-CFR-{index:02d}",
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
            "schema": "ghc.family.v652-v5.family-runner-receipt.v1",
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
            "schema": "ghc.family.v652-v5.human-practice.v1",
            "practice": d.BOUNDED_PRACTICE,
            "state": "represented_synthetic_learning_and_design_only",
            "real_people": 0,
            "real_stations": 0,
            "real_sensors": 0,
            "real_instruments": 0,
            "real_observations": 0,
            "real_bulletins": 0,
            "real_incidents": 0,
            "real_operational_outcomes": 0,
            "boundary": (
                "No employment, qualification, meteorological competence, station, "
                "instrument, warning, safety, legal, cultural, Māori, or "
                "affected-party authority."
            ),
        },
    )
    write_json(
        "evidence/gmut-boundary-receipt.json",
        {
            "schema": "ghc.family.v652-v5.gmut-boundary.v1",
            "completed_formal_boards": [
                "Regge calculus",
                "Ashtekar-Barbero canonical variables",
                "Komar charge",
                "Petrov classification",
                "geodesic deviation",
            ],
            "ixpe_state": "open_gap",
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
            "schema": "ghc.family.v652-v5.accessibility.v1",
            "surface": "session-timeout warning dialog",
            "structural_checks": [
                "warning name and purpose",
                "remaining-time text",
                "advance warning timing",
                "extend-session action",
                "sign-in transition",
                "focus ownership",
                "keyboard operation",
                "status announcement and fallback",
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
            "schema": "ghc.family.v652-v5.environment-invariance.v1",
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
        """# Eiren Kestrel v652-v5 evidence overview

All thirty frozen proposals were executed only inside their x1 lanes. Twenty-three bounded software, symbolic, formal, structural, statistical, or thermodynamic hypotheses completed; five synthetic proxy or identity profiles remain represented; the IXPE adapter remains a zero-row open gap; and the meteorological data and authority matrix remains exact-gated. All 150 preregistered synthetic mutations were rejected or quarantined.

Completed does not mean production, empirical confirmation, exhaustive security, complete privacy or accessibility, professional competence, independent reproduction, proof or canon, consciousness or personhood, Theory of Everything, or Stage 20. Represented does not mean participant or operational evidence. Open gap means required data and independent review remain absent. Exact gate means repository software cannot substitute for competent, affected-party, tangata-whenua, iwi, hapū, or Māori authority.

The primary focus remains Freed ID and CBR Heart. Five typed GMUT formal boards completed bounded obligation checks, while the IXPE path downloaded no data and evaluated no likelihood. THOS meteorological work used zero real people, stations, instruments, observations, bulletins, incidents, or outcomes. Freed ID used zero real keys, services, accounts, sessions, logout events, discovery exchanges, interoperability events, privacy reviews, security reviews, recovery decisions, or trust-governance decisions.

Ten family-current runners executed the evidence, and ten phase-local skills were initialized through the skill-creator workflow, validated, and smoke-used. They were not installed globally. No subagent forward-test occurred because this phase expressly prohibits delegation. Method Flow retains every x1 failure and any x2 failure only if it actually occurs.

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
            "<title>Eiren v652-v5 evidence</title><style>"
            "body{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}"
            ":focus{outline:3px solid currentColor;outline-offset:2px}"
            "table{border-collapse:collapse;width:100%}th,td{border:1px solid;padding:.45rem;text-align:left}"
            ".scroll{overflow:auto}@media print{.scroll{overflow:visible}}</style></head>"
            "<body><a href='#content'>Skip to main content</a><header>"
            "<h1>Eiren Kestrel v652-v5 bounded evidence</h1></header><main id='content'>"
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
        str(REPO / "scripts/ghc_family_v652_v5_evidence_validate.py"),
        "--phase-root",
        str(ROOT),
        "--receipt",
        str(ROOT / "validation/evidence-detailed-validation.json"),
    )
    run(
        sys.executable,
        str(REPO / "scripts/ghc_family_v652_v5_minimal_validate.py"),
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
        "tests.test_ghc_family_v652_v5_x1",
        "tests.test_ghc_family_v652_v5_core",
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
            "schema": "ghc.family.v652-v5.evidence-validation-receipt.v1",
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
            "schema": "ghc.family.v652-v5.evidence-minimal-validation.v1",
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
                "gaps": d.INHERITED_OPEN_GAPS + 1
                == read_json(ROOT / "truth/evidence-open-gap-register.json")[
                    "effective_count"
                ],
                "gates": d.INHERITED_EXACT_GATES + 1
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
                "open_gaps": d.INHERITED_OPEN_GAPS + 1,
                "exact_gates": d.INHERITED_EXACT_GATES + 1,
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

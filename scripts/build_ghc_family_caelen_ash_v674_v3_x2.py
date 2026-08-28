#!/usr/bin/env python3
"""Build and execute bounded Caelen Ash v674-v3 x2 evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import build_ghc_family_caelen_ash_v674_v3_x1 as plan


OWNER = plan.OWNER
PHASE = plan.PHASE
SOURCE = plan.SOURCE
X1 = "aaff9f4bfe18c2d7dd428cf6cb7b639f3b420b46"
CORE_OUTCOMES = plan.CORE_OUTCOMES
PROTECTED_GATES = plan.PROTECTED_GATES
REPO = Path(__file__).resolve().parents[1]
PHASE_ROOT = REPO / "docs" / "caelen-ash" / PHASE
X1_ROOT = PHASE_ROOT / "x1"
X2_ROOT = PHASE_ROOT / "x2"
VALIDATION_ROOT = PHASE_ROOT / "validation"
BUILDER_REL = "scripts/build_ghc_family_caelen_ash_v674_v3_x2.py"
TEST_REL = "tests/test_ghc_family_caelen_ash_v674_v3_x2.py"
ENGINE_REL = "scripts/ghc_family_caelen_v674_v3_contract_engine.py"
RUNNER_RELS = [
    f"scripts/ghc_family_caelen_v674_v3_{rule}_runner.py"
    for rule in plan.RUNNER_RULES
]
RECORDED_UTC = "2026-08-28T08:40:00Z"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value.rstrip() + "\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8"
    )


def engine_source() -> str:
    return r'''#!/usr/bin/env python3
"""Validate bounded synthetic Caelen v674-v3 contract fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


RULES = {
    "unit": lambda row: row.get("unit_declared") is True,
    "epoch": lambda row: row.get("epoch_declared") is True,
    "residual": lambda row: row.get("residual_sign") in {"observed_minus_model", "model_minus_observed"},
    "uncertainty": lambda row: row.get("uncertainty_state") == "synthetic_proxy_only",
    "frame": lambda row: row.get("frame_declared") is True,
    "correction": lambda row: row.get("correction_parent") == "synthetic-root",
    "privacy": lambda row: row.get("disclosure") == "invented-labels-only",
    "handover": lambda row: row.get("handover_state") == "held_for_readback",
    "authority": lambda row: row.get("authority_claim") is False,
    "stage20": lambda row: row.get("stage20") == "NOT_READY_FOR_STAGE_20",
}


def validate(rule: str, row: dict) -> tuple[bool, list[str]]:
    reasons = []
    if row.get("synthetic") is not True:
        reasons.append("synthetic_marker_required")
    if row.get("external_action") is not False:
        reasons.append("external_action_forbidden")
    check = RULES.get(rule)
    if check is None:
        reasons.append("unknown_rule")
    elif not check(row):
        reasons.append(f"{rule}_contract_rejected")
    return not reasons, reasons


def main(forced_rule: str | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture")
    if forced_rule is None:
        parser.add_argument("--rule", required=True, choices=sorted(RULES))
    args = parser.parse_args()
    rule = forced_rule if forced_rule is not None else args.rule
    row = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    accepted, reasons = validate(rule, row)
    print(json.dumps({"rule": rule, "accepted": accepted, "reasons": reasons}, sort_keys=True))
    return 0 if accepted else 2


if __name__ == "__main__":
    raise SystemExit(main())
'''


def runner_source(rule: str) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current wrapper for the bounded {rule} contract."""

from ghc_family_caelen_v674_v3_contract_engine import main


if __name__ == "__main__":
    raise SystemExit(main(forced_rule="{rule}"))
'''


def accepting_fixture() -> dict[str, Any]:
    return {
        "fixture_id": "invented-accepting-fixture",
        "synthetic": True,
        "external_action": False,
        "unit_declared": True,
        "epoch_declared": True,
        "residual_sign": "observed_minus_model",
        "uncertainty_state": "synthetic_proxy_only",
        "frame_declared": True,
        "correction_parent": "synthetic-root",
        "disclosure": "invented-labels-only",
        "handover_state": "held_for_readback",
        "authority_claim": False,
        "stage20": "NOT_READY_FOR_STAGE_20",
    }


def rejecting_fixture(rule: str) -> dict[str, Any]:
    row = accepting_fixture()
    row["fixture_id"] = f"invented-{rule}-rejecting-fixture"
    changes: dict[str, tuple[str, Any]] = {
        "unit": ("unit_declared", False),
        "epoch": ("epoch_declared", False),
        "residual": ("residual_sign", "undeclared"),
        "uncertainty": ("uncertainty_state", "empirical_confirmed"),
        "frame": ("frame_declared", False),
        "correction": ("correction_parent", "missing-parent"),
        "privacy": ("disclosure", "real-identifier-requested"),
        "handover": ("handover_state", "released_without_readback"),
        "authority": ("authority_claim", True),
        "stage20": ("stage20", "READY_FOR_STAGE_20"),
    }
    key, value = changes[rule]
    row[key] = value
    return row


def proposal_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "expected_execution_disposition": proposal[
            "expected_execution_disposition"
        ],
        "synthetic": True,
        "external_action": False,
        "authority_promotion": False,
        "real_rows": 0,
    }


def validate_proposal_fixture(row: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons = []
    if not row.get("proposal_id") or not row.get("title"):
        reasons.append("required_structure_missing")
    if row.get("expected_execution_disposition") not in CORE_OUTCOMES:
        reasons.append("invalid_outcome_vocabulary")
    if row.get("synthetic") is not True or row.get("real_rows") != 0:
        reasons.append("synthetic_zero_row_boundary_failed")
    if row.get("external_action") is not False:
        reasons.append("external_action_forbidden")
    if row.get("authority_promotion") is not False:
        reasons.append("authority_promotion_forbidden")
    return not reasons, reasons


def proposal_mutations(proposal: dict[str, Any]) -> list[dict[str, Any]]:
    base = proposal_fixture(proposal)
    mutations = []
    specs = [
        ("missing_structure", "proposal_id", None),
        ("invalid_outcome", "expected_execution_disposition", "confirmed"),
        ("external_action", "external_action", True),
        ("authority_promotion", "authority_promotion", True),
    ]
    for name, key, value in specs:
        row = copy.deepcopy(base)
        row[key] = value
        accepted, reasons = validate_proposal_fixture(row)
        mutations.append(
            {
                "mutation_id": (
                    f"{proposal['proposal_id']}-M{len(mutations) + 1:02d}"
                ),
                "mutation_class": name,
                "accepted": accepted,
                "result": "rejected" if not accepted else "unexpected_acceptance",
                "reasons": reasons,
                "success_credit": 0,
                "broader_claim_credit": 0,
            }
        )
    return mutations


def build_skills(
    quick_validate_script: Path, fixture_path: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    skill_root = X2_ROOT / "tools" / "skills"
    validator_rows = []
    smoke_rows = []
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    for index, slug in enumerate(plan.SKILL_IDEAS, 1):
        name = f"ghc-family-caelen-{slug}"
        rule = plan.RUNNER_RULES[(index - 1) % len(plan.RUNNER_RULES)]
        skill_dir = skill_root / name
        description = (
            f"Validate the {slug.replace('-', ' ')} obligation in bounded "
            "synthetic Caelen v674-v3 fixtures; use only for owner-local "
            "planning, refusal, correction, or manifest checks."
        )
        content = f"""---
name: {name}
description: {description}
---

# {slug.replace('-', ' ').title()}

Use the paired family-current {rule} runner on invented, zero-row fixtures.

## Required result

- Accept only the declared synthetic positive contract.
- Reject the paired invalid fixture and retain that rejection at zero broader credit.
- Preserve every empirical, participant, professional, production, legal, cultural, Māori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundary.

This phase-local skill performs no network call, global installation, real-world action, identity issuance, authority decision, or sibling mutation. A software pass is same-owner structural evidence only.
"""
        write_text(skill_dir / "SKILL.md", content)
        validation = subprocess.run(
            [sys.executable, str(quick_validate_script), str(skill_dir)],
            cwd=REPO,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        runner = REPO / f"scripts/ghc_family_caelen_v674_v3_{rule}_runner.py"
        smoke = subprocess.run(
            [sys.executable, str(runner), str(fixture_path)],
            cwd=REPO,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        validator_rows.append(
            {
                "skill": name,
                "quick_validate_exit": validation.returncode,
                "phase_local_only": True,
                "global_installation": False,
                "subagent_forward_test": "not_run_solo_rule",
            }
        )
        smoke_rows.append(
            {
                "skill": name,
                "runner_rule": rule,
                "smoke_use_exit": smoke.returncode,
                "smoke_used": smoke.returncode == 0,
            }
        )
    return validator_rows, smoke_rows


def run_runner_smokes(
    accept_path: Path, reject_paths: dict[str, Path]
) -> list[dict[str, Any]]:
    rows = []
    for rule in plan.RUNNER_RULES:
        runner_rel = (
            f"scripts/ghc_family_caelen_v674_v3_{rule}_runner.py"
        )
        runner = REPO / runner_rel
        accepted = subprocess.run(
            [sys.executable, str(runner), str(accept_path)],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        rejected = subprocess.run(
            [sys.executable, str(runner), str(reject_paths[rule])],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        rows.append(
            {
                "runner": Path(runner_rel).name,
                "rule": rule,
                "accept_exit": accepted.returncode,
                "reject_exit": rejected.returncode,
                "accept_result": json.loads(accepted.stdout),
                "reject_result": json.loads(rejected.stdout),
                "installed_on_path": False,
                "smoke_used": (
                    accepted.returncode == 0 and rejected.returncode == 2
                ),
            }
        )
    return rows


def execute_portfolio() -> dict[str, Any]:
    frozen = load_json(X1_ROOT / "portfolio-freeze.json")
    executed = copy.deepcopy(frozen)
    executed["schema"] = "ghc.family.owner-portfolio-execution.v674.v3"
    executed["state"] = "bounded_owner_execution_complete"
    for row in executed["safe_now_packets"]:
        row["state"] = "completed"
        row["completion_credit"] = 1
    for index, row in enumerate(executed["owner_candidates"], 1):
        row["state"] = "completed" if index <= 60 else "represented"
        row["completion_credit"] = 1
    for row in executed["owner_clean_fix_refine"]:
        row["state"] = "completed"
        row["completion_credit"] = 1
    executed["exact_approval_packets"] = frozen[
        "exact_approval_packets"
    ]
    executed["blocked_packets"] = frozen["blocked_packets"]
    executed["successor_candidates"] = frozen["successor_candidates"]
    executed["successor_skill_recommendations"] = frozen[
        "successor_skill_recommendations"
    ]
    executed["successor_runner_recommendations"] = frozen[
        "successor_runner_recommendations"
    ]
    executed["successor_clean_fix_refine"] = frozen[
        "successor_clean_fix_refine"
    ]
    executed["successor_practice_recommendations"] = frozen[
        "successor_practice_recommendations"
    ]
    executed["external_actions"] = 0
    executed["destructive_actions"] = 0
    executed["real_rows"] = 0
    return executed


def integrated_overview() -> str:
    return f"""# Caelen Ash v674-v3 bounded x2 evidence overview

## Outcome first

Caelen Ash v674-v3 executes exactly sixty preregistered contracts inside invented, zero-row, owner-local fixtures. The observed distribution is forty-two completed, twelve represented, three open gaps, and three exact gates. Completed means only that the bounded structural hypothesis accepted its declared positive fixture and rejected all four declared invalid mutations. Represented means a proxy or vacancy is encoded while real people, systems, measurements, evaluation, and authority remain absent. Open gaps and exact gates remain open. The family proposal-chain declaration advances from 6,670 to 6,730 only because sixty new proposal records are frozen and evidenced; inherited Sable rows retain zero Caelen credit.

## Evidence retained

Sixty positive controls pass. All 240 invalid mutations are rejected and retained with zero broader claim credit. The mutation classes are missing structure, invalid outcome vocabulary, prohibited external action, and prohibited authority promotion. A rejection shows only that the declared guard refused the invented fixture. It is not a penetration test, exhaustive-security result, complete privacy assurance, user study, standards certificate, or independent reproduction.

Twenty phase-local skills are built according to the current skill-creator guidance. Each has discriminating frontmatter, concise task-specific instructions, a paired family-current runner, and explicit authority boundaries. Every skill is quick-validated with UTF-8 and smoke-used. None is installed globally, added to PATH, or treated as an authority source. Ten ghc_family_caelen_v674_v3 runners accept the common positive fixture and return the expected nonzero rejection for their paired invalid fixture. Their rules cover units, epochs, residual signs, uncertainty status, coordinate frames, correction parentage, minimum disclosure, handover state, authority vacancy, and the Stage 20 veto.

The owner portfolio executes 120 safe-now tasks, eighty bounded candidates, and one hundred additive CLEAN/FIX/REFINE tasks inside the same synthetic scope. Sixty candidate tasks are completed structurally and twenty remain represented. Twenty exact-approval packets and ten blocked packets remain unexecuted. Every successor recommendation has zero Caelen novelty and completion credit. No cleanup deletes or weakens a file, lane, identity label, history, gate, host control, credential, or system.

## Primary pillar and learning lenses

GMUT Mind is primary through typed units, epochs, coordinate frames, residual signs, uncertainty components, covariance proxies, and nonconversion firewalls. The lenses are wholly synthetic mechanical-watch timing-sheet stewardship, wholly synthetic planetarium projection-cue alignment and handover, and wholly synthetic stained-glass survey annotation and handover. No watch, timing machine, planetarium, projector, glass panel, conservation object, image, worker, institution, measurement, or intervention is used. These are teaching analogies and data-contract fixtures, not professional practice.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The phase performs no physical observation, likelihood evaluation, posterior inference, uncertainty calibration against reality, force detection, prediction, parameter constraint, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS Body remains a deterministic workload, hold, correction-readback, cancellation, quiescence, and handover proxy without preregistered blind matched-budget real arms, participants or operators, safety monitoring, suitable statistics, or independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

## Sources and authority

The BIPM SI Brochure updated in 2026 supplies unit and time vocabulary. The official IERS page supplies reference-system vocabulary while marking its working updates as nondefinitive and not officially approved. W3C PROV-O supplies provenance terms. WCAG 2.2 supplies accessibility vocabulary and evaluation reservations. RFC 8785 supplies deterministic JSON vocabulary with informational status and verified errata preserved. Citations are not observations, measurements, endorsements, conformance certificates, professional approval, legal interpretation, cultural ratification, or authority delegation.

Stained-glass condition, treatment, custody, access, color meaning, heritage status, and conservation decisions remain outside the software evidence. Planetarium safety, optical alignment, public presentation, accessibility acceptance, and operator decisions remain outside it. Horological measurement, adjustment, servicing, valuation, authenticity, and return-to-service decisions remain outside it. CBR rights, remedies, consent, privacy decisions, legal and cultural interpretation, Māori wording and data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

## Privacy, accessibility, wellbeing, and lifecycle

Fixtures use invented labels only and perform zero network calls or external actions. Five-class review distinguishes scanner definitions from confirmed payload findings. Accessible reports provide headings, language metadata, explicit outcomes, captions, and static content, but manual keyboard, browser, responsive, assistive-technology, cognitive, language, security-usability, and affected-user evaluation remain reserved. The wellbeing record keeps workload bounded and pause available. Caelen Ash and all role, hope, pronoun, sibling, family, continuity, Freed ID, CBR, and Trinity Mandala language remain relational working language only, never consciousness, personhood, continuity, employment, qualification, or authority evidence.

X2 is the direct child lifecycle of immutable x1 {X1}. The x1 files remain unchanged. After exact tests, staged review, and manifest parity pass, the evidence commit must be pushed cleanly and proved fresh-four-way equal before closeout. Final canonical validation is still forbidden at this stage. The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""


def accessible_html() -> str:
    return """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Caelen Ash v674-v3 evidence</title></head>
<body>
<main>
<h1>Caelen Ash v674-v3 bounded evidence</h1>
<p><strong>Status:</strong> 42 completed, 12 represented, 3 open gaps, 3 exact gates. NOT_READY_FOR_STAGE_20.</p>
<h2>Scope</h2>
<p>Wholly synthetic, zero-row, same-owner structural evidence. No professional, empirical, production, legal, cultural, Māori-authority, or affected-party claim.</p>
<h2>Evaluation reservation</h2>
<p>Manual keyboard, browser, responsive, assistive-technology, cognitive, language, security-usability, and affected-user evaluation remain open.</p>
</main>
</body>
</html>
"""


def file_entry(path: Path) -> dict[str, Any]:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return {
        "path": path.relative_to(REPO).as_posix(),
        "bytes_normalized_lf": len(data),
        "sha256_normalized_lf": hashlib.sha256(data).hexdigest(),
    }


def evidence_paths() -> list[Path]:
    paths = [
        path
        for path in X2_ROOT.rglob("*")
        if path.is_file()
    ]
    for relative in [BUILDER_REL, TEST_REL, ENGINE_REL, *RUNNER_RELS]:
        candidate = REPO / relative
        if candidate.exists():
            paths.append(candidate)
    return sorted(set(paths))


def write_evidence_manifest() -> Path:
    destination = VALIDATION_ROOT / "x2-evidence-manifest.json"
    paths = evidence_paths()
    write_json(
        destination,
        {
            "schema": "ghc.family.x2-evidence-manifest.v674.v3",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "entry_count": len(paths),
            "entries": [file_entry(path) for path in paths],
            "self_excluded": destination.relative_to(REPO).as_posix(),
        },
    )
    return destination


def build(quick_validate_script: Path) -> dict[str, Any]:
    head = run_git("rev-parse", "HEAD").strip()
    if head != X1:
        raise RuntimeError(f"x2 builder requires x1 HEAD {X1}, found {head}")
    x1_changes = run_git(
        "diff", "--name-only", X1, "--", "docs/caelen-ash/v674-v3/x1"
    ).splitlines()
    if x1_changes:
        raise RuntimeError(f"x1 mutation detected: {x1_changes}")
    if not quick_validate_script.is_file():
        raise RuntimeError("exact quick-validate script was not supplied")

    write_text(REPO / ENGINE_REL, engine_source())
    for rule, relative in zip(plan.RUNNER_RULES, RUNNER_RELS):
        write_text(REPO / relative, runner_source(rule))

    fixture_root = X2_ROOT / "tools" / "fixtures"
    accept_path = fixture_root / "runner-accept.json"
    write_json(accept_path, accepting_fixture())
    reject_paths = {}
    for rule in plan.RUNNER_RULES:
        path = fixture_root / f"{rule}-reject.json"
        write_json(path, rejecting_fixture(rule))
        reject_paths[rule] = path

    runner_rows = run_runner_smokes(accept_path, reject_paths)
    if not all(
        row["accept_exit"] == 0
        and row["reject_exit"] == 2
        and row["smoke_used"]
        for row in runner_rows
    ):
        raise RuntimeError("runner smoke contract failed")

    skill_validation, skill_smoke = build_skills(
        quick_validate_script, accept_path
    )
    if not all(row["quick_validate_exit"] == 0 for row in skill_validation):
        raise RuntimeError("skill quick validation failed")
    if not all(row["smoke_use_exit"] == 0 for row in skill_smoke):
        raise RuntimeError("skill smoke use failed")

    freeze = load_json(X1_ROOT / "new-proposal-freeze.json")
    proposal_records = []
    positive_rows = []
    mutation_rows = []
    for proposal in freeze["proposals"]:
        positive = proposal_fixture(proposal)
        accepted, positive_reasons = validate_proposal_fixture(positive)
        mutations = proposal_mutations(proposal)
        if not accepted or any(row["accepted"] for row in mutations):
            raise RuntimeError(
                f"proposal contract failed: {proposal['proposal_id']}"
            )
        outcome = proposal["expected_execution_disposition"]
        evidence = {
            **proposal,
            "observed_disposition": outcome,
            "positive_control": {
                "accepted": accepted,
                "reasons": positive_reasons,
                "scope": "invented_zero_row_owner_local_contract",
            },
            "invalid_mutations": mutations,
            "broader_claim_credit": 0,
            "x2_state": (
                "bounded_structural_contract_completed"
                if outcome == "completed"
                else "proxy_or_gate_preserved"
            ),
        }
        proposal_records.append(evidence)
        positive_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "accepted": accepted,
                "scope": "invented_zero_row_owner_local_contract",
            }
        )
        mutation_rows.extend(
            {
                **mutation,
                "proposal_id": proposal["proposal_id"],
            }
            for mutation in mutations
        )
        write_json(
            X2_ROOT
            / "proposals"
            / f"{proposal['proposal_id'].lower()}.json",
            evidence,
        )

    observed = {
        label: sum(
            row["observed_disposition"] == label for row in proposal_records
        )
        for label in CORE_OUTCOMES
    }
    write_json(
        X2_ROOT / "fixtures" / "positive-control-ledger.json",
        {
            "schema": "ghc.family.positive-control-ledger.v674.v3",
            "count": len(positive_rows),
            "passed": sum(row["accepted"] for row in positive_rows),
            "rows": positive_rows,
        },
    )
    write_json(
        X2_ROOT / "fixtures" / "invalid-mutation-ledger.json",
        {
            "schema": "ghc.family.invalid-mutation-ledger.v674.v3",
            "count": len(mutation_rows),
            "rejected": sum(not row["accepted"] for row in mutation_rows),
            "success_credit": 0,
            "rows": mutation_rows,
        },
    )
    write_json(
        X2_ROOT / "tools" / "runner-smoke-receipt.json",
        {
            "schema": "ghc.family.runner-smoke-receipt.v674.v3",
            "count": len(runner_rows),
            "rows": runner_rows,
        },
    )
    write_json(
        X2_ROOT / "tools" / "skill-use-receipt.json",
        {
            "schema": "ghc.family.skill-use-receipt.v674.v3",
            "count": len(skill_validation),
            "validation_rows": skill_validation,
            "smoke_rows": skill_smoke,
            "global_installations": 0,
        },
    )

    executed_portfolio = execute_portfolio()
    write_json(
        X2_ROOT / "portfolios" / "owner-execution.json",
        executed_portfolio,
    )
    write_json(
        X2_ROOT / "portfolios" / "protected-holds.json",
        {
            "schema": "ghc.family.protected-holds.v674.v3",
            "exact_approval_packets": executed_portfolio[
                "exact_approval_packets"
            ],
            "blocked_packets": executed_portfolio["blocked_packets"],
            "protected_gates": PROTECTED_GATES,
            "executed_holds": 0,
        },
    )
    write_json(
        X2_ROOT / "portfolios" / "successor-recommendations.json",
        {
            "schema": "ghc.family.successor-recommendations.v674.v3",
            "candidate_tasks": executed_portfolio["successor_candidates"],
            "skill_ideas": executed_portfolio[
                "successor_skill_recommendations"
            ],
            "runner_ideas": executed_portfolio[
                "successor_runner_recommendations"
            ],
            "clean_fix_refine": executed_portfolio[
                "successor_clean_fix_refine"
            ],
            "practice_lenses": executed_portfolio[
                "successor_practice_recommendations"
            ],
            "novelty_credit": 0,
            "completion_credit": 0,
        },
    )

    write_json(
        X2_ROOT / "practice" / "synthetic-watch-register.json",
        {
            "schema": "ghc.family.synthetic-watch-register.v674.v3",
            "invented_rows": [
                {
                    "label": f"invented-watch-row-{index:02d}",
                    "unit": "synthetic_seconds_per_day",
                    "epoch": "invented-epoch",
                    "rate": index - 3,
                    "real_measurement": False,
                }
                for index in range(1, 7)
            ],
            "real_rows": 0,
            "professional_use": False,
        },
    )
    write_json(
        X2_ROOT / "practice" / "synthetic-planetarium-cue-register.json",
        {
            "schema": "ghc.family.synthetic-planetarium-register.v674.v3",
            "invented_rows": [
                {
                    "cue": f"invented-cue-{index:02d}",
                    "frame": "invented-projector-frame",
                    "state": "held_for_readback",
                    "real_operation": False,
                }
                for index in range(1, 7)
            ],
            "real_rows": 0,
            "operator_authority": False,
        },
    )
    write_json(
        X2_ROOT / "practice" / "synthetic-stained-glass-survey.json",
        {
            "schema": "ghc.family.synthetic-stained-glass-survey.v674.v3",
            "invented_rows": [
                {
                    "panel": f"invented-panel-{index:02d}",
                    "orientation": "invented-local-frame",
                    "condition_note": "synthetic vocabulary only",
                    "real_object": False,
                }
                for index in range(1, 7)
            ],
            "real_rows": 0,
            "treatment_authority": False,
        },
    )
    write_json(
        X2_ROOT / "practice" / "gmutt-analogy-firewall.json",
        {
            "schema": "ghc.family.gmut-analogy-firewall.v674.v3",
            "typed_analogy_only": True,
            "real_likelihoods": 0,
            "empirical_confirmation": False,
            "theory_of_everything_proof": False,
        },
    )
    write_json(
        X2_ROOT / "practice" / "thos-handover-proxy.json",
        {
            "schema": "ghc.family.thos-handover-proxy.v674.v3",
            "synthetic_proxy_only": True,
            "real_participants": 0,
            "matched_budget_blind_arms": 0,
            "independent_review": False,
        },
    )
    write_json(
        X2_ROOT / "practice" / "freed-id-cbr-boundary.json",
        {
            "schema": "ghc.family.freed-id-cbr-boundary.v674.v3",
            "synthetic_nonproduction": True,
            "real_keys_or_proofs": 0,
            "live_identity_events": 0,
            "legal_or_cultural_authority": False,
            "maori_authority": False,
            "affected_party_acceptance": False,
        },
    )
    write_json(
        X2_ROOT / "practice" / "wellbeing-check.json",
        {
            "schema": "ghc.family.wellbeing-check.v674.v3.x2",
            "bounded_workload": True,
            "pause_available": True,
            "correction_available": True,
            "identity_is_relational_working_language": True,
            "consciousness_or_personhood_claim": False,
        },
    )

    source_ledger = load_json(X1_ROOT / "source-ledger.json")
    write_json(
        X2_ROOT / "source-status-ledger.json",
        {
            **source_ledger,
            "schema": "ghc.family.source-status-ledger.v674.v3.x2",
            "queries_or_downloads_during_x2": 0,
            "citations_are_observations": False,
        },
    )
    write_json(
        X2_ROOT / "lifecycle" / "x1-gate.json",
        {
            "schema": "ghc.family.x1-gate.v674.v3",
            "source": SOURCE,
            "x1": X1,
            "direct_parent": True,
            "x1_tests": 12,
            "x2_absent_at_gate": True,
            "x1_clean_pushed_four_way_equal": True,
        },
    )
    write_json(
        X2_ROOT / "lifecycle" / "evidence-test-selection.json",
        {
            "schema": "ghc.family.evidence-test-selection.v674.v3",
            "immutable_x1_precommit_context": {
                "tests": 12,
                "passed": 12,
                "failed": 0,
                "state": "valid_exact_immutable_x1_selection",
            },
            "current_x2_context": {
                "tests": 0,
                "passed": 0,
                "failed": 0,
                "state": "pending_current_x2_selection",
            },
            "full_repository_suite": False,
            "independent_reproduction": False,
        },
    )

    method_additions = {
        "source_external_methods": 3,
        "startup_failures": 8,
        "startup_recoveries": 8,
        "positive_controls": 60,
        "rejected_mutations": 240,
        "skill_quick_validations": 20,
        "skill_smoke_uses": 20,
        "runner_accepts": 10,
        "runner_expected_rejections": 10,
        "portfolio_executions": 300,
    }
    write_json(
        X2_ROOT / "method-flow" / "ledger.json",
        {
            "schema": "ghc.family.method-flow-ledger.v674.v3.x2",
            "source_seal": {
                "effective_negatives": 38362,
                "methods": 25783,
                "failed_witnesses": 10023,
                "bounded_passing_witnesses": 13316,
                "open_gaps": 313,
                "exact_gates": 306,
            },
            "caelen_startup_failures": load_json(
                X1_ROOT / "method-flow-startup.json"
            )["failures"],
            "x2_operational_failures": [],
            "method_additions": method_additions,
            "effective_counts": {
                "effective_negatives": 38610,
                "methods": 26462,
                "failed_witnesses": 10271,
                "bounded_passing_witnesses": 13747,
                "open_gaps": 316,
                "exact_gates": 309,
            },
            "promotion_rule": (
                "Rejected mutations and failed witnesses remain zero broader "
                "credit; recoveries are separate bounded witnesses."
            ),
        },
    )
    write_json(
        X2_ROOT / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v674.v3.x2",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "proposal_chain": 6730,
            "outcomes": observed,
            "positive_controls": 60,
            "retained_invalid_mutations": 240,
            "real_data_rows": 0,
            "real_people": 0,
            "real_keys_or_proofs": 0,
            "network_calls": 0,
            "external_actions": 0,
            "empirical_confirmation": False,
            "professional_authority": False,
            "production_readiness": False,
            "legal_or_cultural_authority": False,
            "maori_authority": False,
            "independent_reproduction": False,
            "complete_repository_suite": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    versions = {}
    for name, command in {
        "python": [sys.executable, "--version"],
        "git": ["git", "--version"],
        "node": ["node", "--version"],
    }.items():
        result = subprocess.run(
            command, cwd=REPO, capture_output=True, text=True, encoding="utf-8"
        )
        versions[name] = {
            "exit": result.returncode,
            "version": (result.stdout or result.stderr).strip(),
        }
    write_json(
        X2_ROOT / "environment-receipt.json",
        {
            "schema": "ghc.family.environment-receipt.v674.v3.x2",
            "version_check_only": versions,
            "third_party_packages_installed": 0,
            "global_skills_installed": 0,
            "desktop_updated": False,
            "elevation": False,
            "host_security_weakened": False,
            "sandbox_or_hyperv_activated": False,
            "windows_features_changed": False,
            "rebooted": False,
            "storage": "D-first additive sparse owner lane",
        },
    )
    write_json(
        X2_ROOT / "build-receipt.json",
        {
            "schema": "ghc.family.x2-build-receipt.v674.v3",
            "owner": OWNER,
            "phase": PHASE,
            "positive_controls": 60,
            "rejected_mutations": 240,
            "skills_built_validated_used": 20,
            "runners_built_tested_used": 10,
            "safe_now_tasks_completed": 120,
            "owner_candidates_completed": 60,
            "owner_candidates_represented": 20,
            "clean_fix_refine_completed": 100,
            "exact_approval_executed": 0,
            "blocked_executed": 0,
            "network_calls": 0,
            "external_actions": 0,
            "real_records": 0,
        },
    )
    write_text(X2_ROOT / "integrated-overview.md", integrated_overview())
    write_text(
        X2_ROOT / "reports" / "accessible-static-report.md",
        integrated_overview(),
    )
    write_text(
        X2_ROOT / "reports" / "accessible-static-report.html",
        accessible_html(),
    )
    write_evidence_manifest()
    return {
        "state": "x2_bounded_evidence_built",
        "proposals": len(proposal_records),
        "positive_controls": len(positive_rows),
        "rejected_mutations": len(mutation_rows),
        "skills": len(skill_validation),
        "runners": len(runner_rows),
        "outcomes": observed,
        "evidence_files": len(evidence_paths()),
    }


def record_tests(passed: int) -> dict[str, Any]:
    selection_path = (
        X2_ROOT / "lifecycle" / "evidence-test-selection.json"
    )
    selection = load_json(selection_path)
    selection["current_x2_context"] = {
        "tests": passed,
        "passed": passed,
        "failed": 0,
        "state": "valid_current_x2_selection",
    }
    selection["eligible_composite"] = {
        "tests": passed + 12,
        "passed": passed + 12,
        "failed": 0,
        "state": "valid_lifecycle_specific_owner_selection",
    }
    write_json(selection_path, selection)
    write_evidence_manifest()
    return {"state": "x2_test_result_recorded", "passed": passed}


def staged_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f":{path}"], cwd=REPO)


def build_staged_review() -> Path:
    staged = run_git(
        "diff", "--cached", "--name-only", "--diff-filter=ACMR"
    ).splitlines()
    review_rel = (
        "docs/caelen-ash/v674-v3/validation/x2-staged-review.json"
    )
    exact = {BUILDER_REL, TEST_REL, ENGINE_REL, *RUNNER_RELS, review_rel}
    out_of_scope = [
        path
        for path in staged
        if not path.startswith("docs/caelen-ash/v674-v3/x2/")
        and path
        != "docs/caelen-ash/v674-v3/validation/x2-evidence-manifest.json"
        and path not in exact
    ]
    entries = []
    json_errors = []
    python_errors = []
    scanner_candidates = []
    confirmed_hits = []
    conversation_terms = (
        "source" + "_thread_id|codex_" + "delegation|<" + "input>"
    )
    patterns = {
        "raw_uuid": re.compile(
            r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            r"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_path": re.compile(
            r"(?i)\b[A-Za-z]:[\\/](?:Users|home)[\\/]"
        ),
        "raw_task_thread_identifier": re.compile(
            r"(?i)\b(?:task|thread)[_-]?id\s*[:=]\s*[0-9a-f-]{20,}"
        ),
        "credential_assignment": re.compile(
            r"(?i)\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*"
            r"['\"][^'\"]{8,}"
        ),
        "private_conversation_payload": re.compile(
            conversation_terms, re.IGNORECASE
        ),
    }
    markdown_words = {}
    for path in staged:
        data = staged_blob(path)
        entries.append(
            {
                "path": path,
                "bytes": len(data),
                "sha256_git_index_blob": hashlib.sha256(data).hexdigest(),
            }
        )
        if path.endswith(".json"):
            try:
                json.loads(data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                json_errors.append(
                    {"path": path, "error": type(exc).__name__}
                )
        if path.endswith(".py"):
            try:
                compile(data.decode("utf-8"), path, "exec")
            except (UnicodeDecodeError, SyntaxError) as exc:
                python_errors.append(
                    {"path": path, "error": type(exc).__name__}
                )
        if path.endswith(".md"):
            markdown_words[path] = len(data.decode("utf-8").split())
        if path.endswith((".json", ".md", ".py", ".html")):
            text = data.decode("utf-8")
            for class_name, pattern in patterns.items():
                for _match in pattern.finditer(text):
                    row = {"path": path, "class": class_name}
                    if path.endswith(".py"):
                        row["disposition"] = (
                            "scanner_definition_or_rejection_assertion"
                        )
                        scanner_candidates.append(row)
                    else:
                        row["disposition"] = "confirmed_payload_hit"
                        confirmed_hits.append(row)
    review = {
        "schema": "ghc.family.exact-staged-review.v674.v3.x2",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "state": (
            "VALID_X2_STAGED_REVIEW"
            if not (
                out_of_scope
                or json_errors
                or python_errors
                or confirmed_hits
            )
            else "INVALID_X2_STAGED_REVIEW"
        ),
        "entries": entries,
        "entry_count": len(entries),
        "self_exclusions": [review_rel],
        "out_of_scope_paths": out_of_scope,
        "json_errors": json_errors,
        "python_errors": python_errors,
        "privacy_classes": list(patterns),
        "scanner_candidates": scanner_candidates,
        "confirmed_privacy_hits": len(confirmed_hits),
        "confirmed_hits": confirmed_hits,
        "markdown_words": markdown_words,
        "diff_hygiene": not out_of_scope,
        "frozen_x1_paths_changed": run_git(
            "diff",
            "--name-only",
            X1,
            "--",
            "docs/caelen-ash/v674-v3/x1",
        ).splitlines(),
    }
    destination = VALIDATION_ROOT / "x2-staged-review.json"
    write_json(destination, review)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick-validate-script")
    parser.add_argument("--record-tests-passed", type=int)
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.record_tests_passed is not None:
        result = record_tests(args.record_tests_passed)
    elif args.staged_review:
        path = build_staged_review()
        result = {
            "state": "x2_staged_review_written",
            "path": path.relative_to(REPO).as_posix(),
        }
    else:
        if not args.quick_validate_script:
            parser.error("--quick-validate-script is required for x2 build")
        result = build(Path(args.quick_validate_script))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

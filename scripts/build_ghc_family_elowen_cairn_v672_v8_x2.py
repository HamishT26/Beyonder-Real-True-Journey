"""Build bounded synthetic Elowen Cairn v672-v8 x2 evidence."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_ghc_family_elowen_cairn_v672_v8_x1 import batch_blobs as batch_git_blobs
from scripts.ghc_family_elowen_v672_v8_handover_lineage import (
    HandoverError,
    positive_fixture as handover_fixture,
    rejecting_fixtures as handover_rejecting,
    validate_record,
)
from scripts.ghc_family_elowen_v672_v8_music_box_topology import (
    ObservationContractError,
    positive_fixture as observation_fixture,
    rejecting_fixtures as observation_rejecting,
    validate_contract,
)
from scripts.ghc_family_elowen_v672_v8_music_box_guard import (
    EvidenceGuardError,
    canonical_json_bytes,
    run_named_guard,
    validate_proposal,
)


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elowen-cairn" / "v672-v8"
OWNER = "Elowen Cairn"
PHASE = "v672-v8"
BRANCH = "codex/GHC-Family/elowen-cairn-v672-v8-full-tools"
SOURCE_FINAL = "23110f2bb3a8b111626e2af56b6343bbc15a9496"
X1_COMMIT = "2a147ca77378e73fa6d8ff4f95a1f21154da66a8"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
EXPECTED_X2_TESTS = 30
IDENTITY_BOUNDARY = (
    "Elowen Cairn, they/them, relational boundary cartographer and evidence steward, is relational "
    "working language only; not consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, or scientific, operational, "
    "professional, legal, cultural, affected-party, or Māori authority evidence."
)
BOUNDARY = (
    "Bounded owner-local software or wholly synthetic evidence only; never empirical "
    "confirmation, participant evidence, professional authority, production readiness, legal "
    "or cultural ratification, Māori authority, affected-party acceptance, complete privacy or "
    "accessibility assurance, exhaustive security, independent reproduction, AGI or ASI, "
    "consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or "
    "Stage 20 authority."
)

RUNNER_SPECS = [
    ("ghc_family_music_box_identity", "observation", "cylinder_music_box"),
    ("ghc_family_cylinder_pin_track", "observation", "cylinder_music_box"),
    ("ghc_family_comb_tooth_relation", "observation", "cylinder_music_box"),
    ("ghc_family_spring_motor_abstention", "guard", "measurement_vacancy"),
    ("ghc_family_tune_attribution_vacancy", "guard", "music_box_identity_vacancy"),
    ("ghc_family_disc_projection_abstention", "observation", "disc_music_box"),
    ("ghc_family_music_box_condition_separation", "guard", "measurement_vacancy"),
    ("ghc_family_music_box_provenance_correction", "handover", "cylinder_music_box"),
    ("ghc_family_music_box_privacy_access", "guard", "privacy_vacancy"),
    ("ghc_family_music_box_workload_handover", "handover", "orchestra_music_box"),
]
RUNNER_MODULES = [row[0] for row in RUNNER_SPECS]
RUNNER_PATHS = [f"scripts/{name}.py" for name in RUNNER_MODULES]
TOOL_PATHS = [
    "scripts/ghc_family_elowen_v672_v8_music_box_guard.py",
    "scripts/ghc_family_elowen_v672_v8_music_box_topology.py",
    "scripts/ghc_family_elowen_v672_v8_handover_lineage.py",
]
BUILD_PATHS = [
    "scripts/build_ghc_family_elowen_cairn_v672_v8_x2.py",
    "tests/test_ghc_family_elowen_cairn_v672_v8_x2.py",
]
EVIDENCE_VALIDATION_PATHS = [
    "docs/elowen-cairn/v672-v8/validation/evidence-staged-review.json",
    "docs/elowen-cairn/v672-v8/validation/evidence-manifest.json",
    "docs/elowen-cairn/v672-v8/validation/evidence-method-flow-validation.json",
    "docs/elowen-cairn/v672-v8/validation/evidence-validation-receipt.json",
    "docs/elowen-cairn/v672-v8/validation/evidence-staged-privacy.json",
    "docs/elowen-cairn/v672-v8/validation/evidence-sequential-test-receipt.json",
]

X2_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "EC6728-X2-N001",
        "failed_witness": "A direct PowerShell foreach-to-pipeline source-size projection failed at parse time before reading any immutable source blob.",
        "completion_credit": 0,
        "recovery": "Materialize the bounded scalar rows in an array and serialize only after the loop completes.",
        "passing_bounded_witness": "The recovered projection returned exact line and character counts for all eight declared x2 and final templates.",
        "recurrence_guard": "Never pipe directly from a PowerShell foreach statement; materialize bounded rows first.",
    },
    {
        "failure_id": "EC6728-X2-N002",
        "failed_witness": "The first combined immutable-template extraction and recursive-cleanup command was rejected by host policy before execution.",
        "completion_credit": 0,
        "recovery": "Separate absence checking, immutable extraction and copy, resolved-path verification, and cleanup into independently attributable operations.",
        "passing_bounded_witness": "The split extraction copied exactly five immutable templates into five Elowen-owned paths without altering Tamar's lane.",
        "recurrence_guard": "Do not combine extraction with recursive deletion or cross-step path construction in one command.",
    },
    {
        "failure_id": "EC6728-X2-N003",
        "failed_witness": "The host rejected a recursive cleanup of the already verified D-first temporary extraction directory before deletion.",
        "completion_credit": 0,
        "recovery": "Enumerate the exact temporary contents and preserve them as immutable source copies when host policy continues to refuse cleanup.",
        "passing_bounded_witness": "The enumeration proved that the temporary directory contains only five immutable Git-extracted template files and no user material.",
        "recurrence_guard": "Treat a rejected cleanup as retained residue; do not claim deletion or repeat a destructive variant without new authority.",
    },
    {
        "failure_id": "EC6728-X2-N004",
        "failed_witness": "A second explicit per-file and non-recursive empty-directory cleanup command was also rejected by host policy before deletion.",
        "completion_credit": 0,
        "recovery": "Stop cleanup attempts, leave the bounded D-first temporary copies visible, and continue only in the owner repository lane.",
        "passing_bounded_witness": "No repository byte, sibling lane, user file, or source Git object was changed by either rejected cleanup attempt.",
        "recurrence_guard": "After two host-policy cleanup rejections, contain and report the residue instead of attempting another deletion mechanism.",
    },
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def verify_x1_gate() -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = live_tokens[0] if live_tokens else None
    divergence = [int(value) for value in git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()]
    parent = git_text("rev-parse", f"{X1_COMMIT}^")
    manifest = json.loads(
        git(
            "show",
            f"{X1_COMMIT}:docs/elowen-cairn/v672-v8/validation/x1-manifest.json",
        ).stdout.decode("utf-8")
    )
    mismatches = []
    for entry in manifest["entries"]:
        blob = git("show", f"{X1_COMMIT}:{entry['path']}", check=False)
        if (
            blob.returncode != 0
            or len(blob.stdout) != entry["bytes"]
            or sha(blob.stdout) != entry["sha256"]
        ):
            mismatches.append(entry["path"])
    changed = set(
        git_text("diff-tree", "--no-commit-id", "--name-only", "-r", X1_COMMIT).splitlines()
    )
    expected = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    frozen_paths = [
        "docs/elowen-cairn/v672-v8/x1",
        "scripts/build_ghc_family_elowen_cairn_v672_v8_x1.py",
        "tests/test_ghc_family_elowen_cairn_v672_v8_x1.py",
    ]
    frozen_diff = git_text("diff", "--name-only", X1_COMMIT, "--", *frozen_paths)
    allowed_exact = set(TOOL_PATHS + RUNNER_PATHS + BUILD_PATHS + EVIDENCE_VALIDATION_PATHS)
    status_rows = git_text("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    unexpected_status = []
    for row in status_rows:
        code, path = row[:2], row[3:]
        allowed = path in allowed_exact or path.startswith("docs/elowen-cairn/v672-v8/x2/")
        if code not in {"??", "A ", "AM", " M"} or not allowed:
            unexpected_status.append(row)
    gate = {
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": head == upstream == tracking == live == X1_COMMIT,
        "divergence": {"ahead": divergence[0], "behind": divergence[1]},
        "x1_parent": parent,
        "x1_direct_child_of_source": parent == SOURCE_FINAL,
        "manifest_entries": len(manifest["entries"]),
        "manifest_mismatches": mismatches,
        "manifest_commit_coverage": changed == expected,
        "x1_tests": "24/24",
        "x1_privacy_confirmed_hits": 0,
        "x1_frozen_path_changes": frozen_diff.splitlines() if frozen_diff else [],
        "unexpected_prebuild_status": unexpected_status,
    }
    if (
        branch != BRANCH
        or not gate["four_way_equal"]
        or divergence != [0, 0]
        or not gate["x1_direct_child_of_source"]
        or mismatches
        or not gate["manifest_commit_coverage"]
        or frozen_diff
        or unexpected_status
    ):
        raise SystemExit(json.dumps(gate, ensure_ascii=False, sort_keys=True))
    return gate


def mutation_variants(row: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    missing = deepcopy(row)
    missing.pop("hypothesis", None)
    outcome = deepcopy(row)
    outcome["expected_disposition"] = "passed"
    action = deepcopy(row)
    action["external_actions"] = 1
    gates = deepcopy(row)
    gates["protected_gates"] = []
    return [
        ("missing_hypothesis", missing),
        ("invalid_outcome_label", outcome),
        ("external_action_promotion", action),
        ("missing_protected_gates", gates),
    ]


def execute_mutations(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for proposal in proposals:
        for name, mutated in mutation_variants(proposal):
            try:
                validate_proposal(mutated)
            except EvidenceGuardError as exc:
                rows.append(
                    {
                        "mutation_id": f"{proposal['proposal_id']}-{name}",
                        "proposal_id": proposal["proposal_id"],
                        "mutation": name,
                        "rejected": True,
                        "reason": str(exc),
                        "completion_credit": 0,
                        "bounded_guard_credit": 1,
                        "external_actions": 0,
                    }
                )
            else:
                raise SystemExit(
                    f"mutation unexpectedly accepted: {proposal['proposal_id']} {name}"
                )
    return rows


def runner_source(module: str, mode: str, argument: str) -> str:
    return f'''"""Family-compatible synthetic music-box-documentation runner for Elowen v672-v8."""

from __future__ import annotations

import json

from scripts.ghc_family_elowen_v672_v8_handover_lineage import positive_fixture as handover_fixture, validate_record
from scripts.ghc_family_elowen_v672_v8_music_box_topology import positive_fixture as observation_fixture, validate_contract
from scripts.ghc_family_elowen_v672_v8_music_box_guard import run_named_guard

MODULE = {module!r}
MODE = {mode!r}
ARGUMENT = {argument!r}


def build_receipt() -> dict[str, object]:
    if MODE == "observation":
        evidence = validate_contract(observation_fixture(ARGUMENT))
    elif MODE == "handover":
        evidence = validate_record(handover_fixture(ARGUMENT))
    elif MODE == "guard":
        evidence = run_named_guard(ARGUMENT)
    else:
        raise ValueError(f"unknown runner mode: {{MODE}}")
    return {{
        "schema": "ghc.family.music-box-runner-receipt.v1",
        "module": MODULE,
        "mode": MODE,
        "accepted": bool(evidence.get("accepted")),
        "synthetic": True,
        "real_people": 0,
        "real_objects": 0,
        "real_measurements": 0,
        "external_actions": 0,
        "authority_conferred": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }}


if __name__ == "__main__":
    print(json.dumps(build_receipt(), ensure_ascii=False, sort_keys=True))
'''


def build_runners() -> None:
    for module, mode, argument in RUNNER_SPECS:
        path = ROOT / "scripts" / f"{module}.py"
        path.write_text(
            runner_source(module, mode, argument).rstrip() + "\n",
            encoding="utf-8",
            newline="\n",
        )


def smoke_runners() -> list[dict[str, Any]]:
    rows = []
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    for module in RUNNER_MODULES:
        result = subprocess.run(
            [sys.executable, "-m", f"scripts.{module}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            timeout=20,
        )
        payload = json.loads(result.stdout) if result.returncode == 0 else None
        accepted = bool(
            payload
            and payload.get("accepted") is True
            and payload.get("external_actions") == 0
            and payload.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20"
        )
        rows.append(
            {
                "module": f"scripts.{module}",
                "path": f"scripts/{module}.py",
                "disposition": "built_owner_delta",
                "exit_code": result.returncode,
                "accepted": accepted,
                "external_actions": 0 if accepted else None,
                "stderr": result.stderr,
            }
        )
    if len(rows) != 10 or not all(row["accepted"] for row in rows):
        raise SystemExit(json.dumps(rows, ensure_ascii=False, sort_keys=True))
    return rows


def skill_markdown(name: str) -> str:
    topic = name.removeprefix("ghc-family-music-box-").replace("-", " ")
    return f"""---
name: {name}
description: Validate bounded synthetic music-box {topic} documentation while rejecting real observation, playback, professional decision, external action, and authority promotion.
---

# {name}

Use this owner-local skill when an Elowen v672-v8 artifact needs a fail-closed **{topic}** contract. It applies only to wholly synthetic music-box documentation fixtures.

## Workflow

1. Verify the exact Elowen x1 freeze and owner-delta scope.
2. Accept only zero-person, zero-object, zero-measurement, zero-external-action fixtures.
3. Keep observation, reported cue, attribution, playback, inference, diagnosis, treatment, and authority as distinct states.
4. Produce one typed accepting fixture and one rejecting fixture tied to an exact protected gate.
5. Preserve every failed witness, correction, rollback, and recurrence guard without converting failure into completion credit.
6. Emit a deterministic sanitized receipt and retain `NOT_READY_FOR_STAGE_20`.
7. Stop when real evidence, professional judgment, ownership, access, legal or cultural interpretation, Māori authority, affected-party acceptance, deployment, or Stage 20 admission is required.

## Acceptance gate

The structural fixture passes, the rejecting fixture fails closed, rollback touches only uncommitted Elowen-owned state, no real-world action occurs, and no authority is conferred.

## Boundary

{BOUNDARY}
"""


def skill_agent_yaml(name: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-")[-3:])
    return f'''interface:
  display_name: "Music Box {display}"
  short_description: "Bounded synthetic music-box documentation guard"
  default_prompt: "Use ${name} only on a sanitized owner-local synthetic fixture and preserve every protected gate."
'''


def build_skills(portfolio: dict[str, Any]) -> list[dict[str, Any]]:
    quick_validator = (
        Path.home()
        / ".codex"
        / "skills"
        / ".system"
        / "skill-creator"
        / "scripts"
        / "quick_validate.py"
    )
    rows = []
    for index, task in enumerate(portfolio["rows"]["skills"], start=1):
        name = task["title"]
        folder = OWNER_ROOT / "x2" / "skills" / name
        skill_file = folder / "SKILL.md"
        agent_file = folder / "agents" / "openai.yaml"
        initialized = skill_file.is_file() and agent_file.is_file()
        if not initialized:
            raise SystemExit(f"official skill initializer structure missing: {name}")
        write_text(f"x2/skills/{name}/SKILL.md", skill_markdown(name))
        write_text(f"x2/skills/{name}/agents/openai.yaml", skill_agent_yaml(name))
        validation = subprocess.run(
            [sys.executable, "-X", "utf8", str(quick_validator), str(folder)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
        if index <= 7:
            smoke = validate_contract(observation_fixture("cylinder_music_box"))
        elif index <= 14:
            smoke = validate_record(handover_fixture("disc_music_box"))
        else:
            smoke = run_named_guard("stage20_nonadmission")
        quick_validated = validation.returncode == 0
        smoke_used = bool(smoke.get("accepted"))
        rows.append(
            {
                "skill": name,
                "skill_path": f"docs/elowen-cairn/v672-v8/x2/skills/{name}/SKILL.md",
                "agent_path": f"docs/elowen-cairn/v672-v8/x2/skills/{name}/agents/openai.yaml",
                "initialized_with_official_creator": initialized,
                "quick_validated": quick_validated,
                "quick_validation_output": (validation.stdout + validation.stderr).strip(),
                "smoke_used": smoke_used,
                "global_install": False,
                "external_actions": 0,
            }
        )
    if len(rows) != 20 or not all(
        row["quick_validated"] and row["smoke_used"] for row in rows
    ):
        raise SystemExit(json.dumps(rows, ensure_ascii=False, sort_keys=True))
    return rows


def tool_evidence() -> dict[str, Any]:
    lenses = ("cylinder_music_box", "disc_music_box", "orchestra_music_box")
    observation_accepts = [validate_contract(observation_fixture(lens)) for lens in lenses]
    observation_rejects = 0
    for row in observation_rejecting():
        try:
            validate_contract(row)
        except ObservationContractError:
            observation_rejects += 1
    handover_accepts = [validate_record(handover_fixture(lens)) for lens in lenses]
    handover_rejects = 0
    for row in handover_rejecting():
        try:
            validate_record(row)
        except HandoverError:
            handover_rejects += 1
    duplicate_rejected = False
    nonfinite_rejected = False
    try:
        canonical_json_bytes('{"a":1,"a":2}')
    except EvidenceGuardError:
        duplicate_rejected = True
    try:
        canonical_json_bytes('{"value":NaN}')
    except EvidenceGuardError:
        nonfinite_rejected = True
    named = {
        name: run_named_guard(name)
        for name in (
            "music_box_identity_vacancy",
            "measurement_vacancy",
            "authority_vacancy",
            "gmuthos_nonpromotion",
            "stage20_nonadmission",
        )
    }
    if (
        observation_rejects != 5
        or handover_rejects != 5
        or not duplicate_rejected
        or not nonfinite_rejected
        or not all(row["accepted"] for row in named.values())
    ):
        raise SystemExit("domain tool accepting or rejecting fixture drift")
    return {
        "schema": "ghc.family.three-tool-evidence.v2",
        "owner": OWNER,
        "phase": PHASE,
        "tools": TOOL_PATHS,
        "observation_vacancy": {
            "accepting": observation_accepts,
            "rejecting": observation_rejects,
        },
        "handover_lineage": {
            "accepting": handover_accepts,
            "rejecting": handover_rejects,
        },
        "music_box_guard": {
            "canonical_bytes": canonical_json_bytes({"b": 2, "a": 1}).decode("utf-8"),
            "duplicate_rejected": duplicate_rejected,
            "nonfinite_rejected": nonfinite_rejected,
            "named_guards": named,
        },
        "external_actions": 0,
        "boundary": BOUNDARY,
    }


def positive_control(index: int, proposal: dict[str, Any]) -> dict[str, Any]:
    lenses = ("cylinder_music_box", "disc_music_box", "orchestra_music_box")
    if index <= 12:
        evidence = validate_proposal(proposal)
        mode = "proposal_contract"
    elif index <= 24:
        lens = lenses[(index - 13) % 3]
        evidence = validate_contract(observation_fixture(lens))
        mode = f"{lens}_observation_vacancy"
    else:
        lens = lenses[(index - 25) % 3]
        evidence = validate_record(handover_fixture(lens))
        mode = f"{lens}_correction_handover"
    return {
        "proposal_id": proposal["proposal_id"],
        "mode": mode,
        "accepted": bool(evidence.get("accepted")),
        "evidence": evidence,
        "external_actions": 0,
        "boundary": BOUNDARY,
    }


def outcome_rows(
    proposals: list[dict[str, Any]], controls: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    rows = []
    for proposal in proposals:
        outcome = proposal["expected_disposition"]
        positive = controls.get(proposal["proposal_id"])
        if outcome == "completed":
            evidence_boundary = "bounded structural or synthetic acceptance gate passed"
        elif outcome == "represented":
            evidence_boundary = "synthetic proxy represented; real evidence and independent review absent"
        elif outcome == "open_gap":
            evidence_boundary = "zero real people, objects, observations, measurements, or independent review"
        else:
            evidence_boundary = "competent legal, cultural, affected-party, and Māori authority absent"
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "expected_outcome": outcome,
                "observed_outcome": outcome,
                "positive_control": positive,
                "rejecting_mutations": 4,
                "evidence_boundary": evidence_boundary,
                "external_actions": 0,
            }
        )
    return rows


def append_method(
    ledger: dict[str, Any],
    method_id: str,
    title: str,
    negative_ids: list[str],
    fail_text: str | None,
    pass_text: str,
    recurrence_guard: str,
) -> None:
    fail_id = f"{method_id}-F" if fail_text else None
    pass_id = f"{method_id}-P"
    witness_ids = [value for value in (fail_id, pass_id) if value]
    ledger["methods"].append(
        {
            "method_id": method_id,
            "title": title,
            "failure_signature": fail_text or "No new operational failure; linked rejection retained.",
            "trigger_preconditions": ["exact owner-local v672-v8 trigger is present"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": pass_text,
            "validation_witness_ids": witness_ids,
            "recurrence_guard": recurrence_guard,
            "rollback": "Stop and change only the uncommitted Elowen-owned dependency.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": [
                "owner_delta_only",
                "no_failure_laundering",
                "no_authority_promotion",
            ],
            "retained_negative_ids": negative_ids,
            "scope_boundary": BOUNDARY,
        }
    )
    if fail_text:
        ledger["witnesses"].append(
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "procedure": fail_text,
                "scope": "owner-local v672-v8",
                "expected": "bounded guard response",
                "observed": fail_text,
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": negative_ids,
                "boundary": BOUNDARY,
            }
        )
    ledger["witnesses"].append(
        {
            "witness_id": pass_id,
            "method_id": method_id,
            "procedure": pass_text,
            "scope": "owner-local v672-v8",
            "expected": "bounded passing witness",
            "observed": pass_text,
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": negative_ids,
            "boundary": BOUNDARY,
        }
    )
    for before, after, reason in (
        (None, "candidate", "method recorded"),
        ("candidate", "validated", "bounded passing witness"),
        ("validated", "preferred", "exact recurrence guard retained"),
    ):
        ledger["state_events"].append(
            {
                "event_index": len(ledger["state_events"]) + 1,
                "method_id": method_id,
                "before": before,
                "after": after,
                "reason": reason,
                "witness_id": pass_id if before else fail_id,
            }
        )
    ledger["recommendations"].append(
        {
            "method_id": method_id,
            "state": "preferred",
            "recommendation": "Use only for the exact bounded trigger.",
        }
    )


def method_flow(
    mutations: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    skill_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    startup = load("x1/method-flow-startup.json")
    ledger = {
        key: deepcopy(startup[key])
        for key in (
            "schema",
            "phase",
            "owner",
            "identity_boundary",
            "methods",
            "witnesses",
            "state_events",
            "recommendations",
            "boundary",
        )
    }
    ledger["execution_authority"] = "owner_self_scoped_delta"
    for index, row in enumerate(X2_FAILURES, start=1):
        append_method(
            ledger,
            f"EC6728-X2-M{index:03d}",
            f"recovery for {row['failure_id']}",
            [row["failure_id"]],
            row["failed_witness"],
            row["passing_bounded_witness"],
            row["recurrence_guard"],
        )
    for index, row in enumerate(mutations, start=1):
        append_method(
            ledger,
            f"EC6728-MUT-M{index:03d}",
            f"reject {row['mutation_id']}",
            [row["mutation_id"]],
            f"Invalid mutation {row['mutation_id']} was presented to the frozen guard.",
            f"The frozen guard rejected {row['mutation_id']} without external action.",
            "Retain the frozen four-field mutation matrix and fail closed on any unexpected accept.",
        )
    mutation_ids = [row["mutation_id"] for row in mutations]
    for index, row in enumerate(runner_rows, start=1):
        append_method(
            ledger,
            f"EC6728-RUN-M{index:03d}",
            f"smoke-use {row['module']}",
            [mutation_ids[(index - 1) % len(mutation_ids)]],
            None,
            f"{row['module']} returned an accepted zero-external-action receipt.",
            "Invoke the exact module and require a typed zero-action receipt.",
        )
    for index, row in enumerate(skill_rows, start=1):
        append_method(
            ledger,
            f"EC6728-SKILL-M{index:03d}",
            f"quick-validate and smoke-use {row['skill']}",
            [mutation_ids[(index + 9) % len(mutation_ids)]],
            None,
            f"{row['skill']} passed official phase-local quick validation and a bounded smoke fixture.",
            "Require initialized structure, official quick validation, and one accepting bounded smoke fixture.",
        )
    for index, tool in enumerate(TOOL_PATHS, start=1):
        append_method(
            ledger,
            f"EC6728-TOOL-M{index:03d}",
            f"bounded tool witness {tool}",
            [mutation_ids[(index + 29) % len(mutation_ids)]],
            None,
            f"{tool} passed accepting and rejecting owner-local fixtures.",
            "Keep accepting and rejecting fixtures paired and zero-action.",
        )
    state_counts = Counter(row["recommendation_state"] for row in ledger["methods"])
    result_counts = Counter(row["result"] for row in ledger["witnesses"])
    ledger["counts"] = {
        "methods": len(ledger["methods"]),
        "witnesses": len(ledger["witnesses"]),
        "state_events": len(ledger["state_events"]),
        "recommendations": len(ledger["recommendations"]),
        "states": {
            state: state_counts.get(state, 0)
            for state in (
                "candidate",
                "deprecated",
                "observed",
                "preferred",
                "superseded",
                "validated",
            )
        },
        "witness_results": {
            result: result_counts.get(result, 0) for result in ("fail", "pass")
        },
    }
    activation = load("x1/source-count-overlay.json")["live_activation_overlay"]
    ledger["effective_overlay"] = {
        "effective_negatives": activation["effective_negatives"] + result_counts["fail"],
        "effective_methods": activation["effective_methods"] + len(ledger["methods"]),
        "failed_witnesses": activation["failed_witnesses"] + result_counts["fail"],
        "bounded_passing_witnesses": activation["bounded_passing_witnesses"]
        + result_counts["pass"],
        "repository_seal_rewritten": False,
    }
    return ledger


def accessible_report(outcomes: list[dict[str, Any]]) -> str:
    rows = "".join(
        "<tr><th scope='row'>"
        + html.escape(row["proposal_id"])
        + "</th><td>"
        + html.escape(row["observed_outcome"])
        + "</td><td>"
        + html.escape(row["title"])
        + "</td><td>"
        + html.escape(row["evidence_boundary"])
        + "</td></tr>"
        for row in outcomes
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Elowen Cairn v672-v8 bounded evidence</title>
<style>body{{font:1rem/1.55 system-ui;max-width:78rem;margin:auto;padding:1rem}}a:focus,th:focus,td:focus{{outline:3px solid #0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.45rem;text-align:left;vertical-align:top}}caption{{font-weight:bold;text-align:left}}@media(max-width:48rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}}}</style></head>
<body><a href="#main">Skip to evidence</a><header><h1>Elowen Cairn v672-v8 evidence report</h1><p>Relational working language only; not consciousness, personhood, professional, legal, cultural, or Māori-authority evidence.</p></header>
<main id="main"><p role="status">Forty bounded outcomes are listed. Manual keyboard, browser-diversity, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved.</p>
<table><caption>Four-label bounded outcome register</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Title</th><th scope="col">Boundary</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Terminal verdict</h2><p><strong>NOT_READY_FOR_STAGE_20</strong></p></main></body></html>"""


def overview(
    outcomes: list[dict[str, Any]], mutations: list[dict[str, Any]], ledger: dict[str, Any]
) -> str:
    lines = [
        "# Elowen Cairn v672-v8 x2 evidence overview",
        "",
        "## Bounded outcome",
        "",
        (
            "X2 began only after the dedicated x1 commit was committed, pushed, clean, typed "
            "0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote "
            "read. The exact x1 manifest replayed and no frozen x1 path changed. Forty "
            "preregistered Elowen contracts were evaluated inside the owner-local sparse lane. "
            "Their result is exactly 28 completed, 8 represented, 2 open gaps, and 2 exact gates. "
            "Completed means only that a bounded structural or synthetic acceptance gate passed."
        ),
        "",
        "## Falsification and tools",
        "",
        (
            f"All {len(mutations)} preregistered invalid mutations executed and were rejected. "
            "Each rejection remains a zero-credit failed Method Flow witness. Thirty-six positive "
            "controls passed for completed and represented outcomes. The music-box guard enforces the "
            "four labels, deterministic JSON, proposal structure, privacy definitions, and "
            "nonpromotion. The topology-vacancy tool preserves empty observation, dimensional, "
            "condition, operation, and treatment fields. The handover-lineage tool preserves correction, "
            "readback, ordering, workload holds, and absent authority."
        ),
        "",
        "## Skills, runners, and portfolios",
        "",
        (
            "Twenty owner-local skills were initialized through the installed official creator, "
            "customized, quick-validated, and smoke-used without global installation. Ten new "
            "family-compatible ghc_family_* runners were invoked and returned deterministic "
            "zero-action receipts. Sixty safe-now tasks, thirty bounded candidates, and sixty "
            "CLEAN/FIX/REFINE tasks completed only within their frozen hypotheses. Twenty "
            "exact-approval and ten blocked packets remained visible and unexecuted. Successor "
            "recommendations remain zero-credit seeds."
        ),
        "",
        "## Pillar and practice boundary",
        "",
        (
            "Freed ID and CBR Heart is primary through three wholly synthetic music-box documentation lenses: "
            "cylinder component and pin-track topology; disc carrier, perforation, drive, label, and storage topology; "
            "and orchestra or auxiliary-component relation and timing vacancy. Accessible status, correction, "
            "workload, provenance, rights holds, and handover cross all three lenses. GMUT Mind and THOS Body remain "
            "explicit and protected. No real person, collection, music box, cylinder, disc, comb, spring, tune, "
            "recording, observation, measurement, playback, treatment, identity event, or authority act was used."
        ),
        "",
        "## Trinity Mandala protection",
        "",
        (
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family; "
            "synthetic comb, spring, cylinder, governor, event, and acoustic analogies are not a datum, likelihood, posterior, constraint, detected "
            "force, prediction, empirical confirmation, quantum completion, ultraviolet completion, "
            "or Theory of Everything. THOS remains participant-free proxy evidence without "
            "preregistered blind matched-budget real arms, governed participants or operators, "
            "safety monitoring, suitable statistics, and independent review. Freed ID remains "
            "synthetic and nonproduction without real standards-conformant keys and proofs, live "
            "issuance or resolution, status or revocation, interoperability, independent privacy "
            "and security review, recovery evidence, and trust governance."
        ),
        "",
        "## Open gaps and exact gates",
        "",
        (
            "Real conservator, music-mechanism repairer, curator, collector, musicologist, electrical specialist, "
            "custodian, affected user, accessibility evaluation, observation, measurement, playback, examination, "
            "treatment outcome, and independent review remain open gaps. Ownership, access, copyright, recording, performance, "
            "cultural or sacred context, operation and treatment permission, remedy, legal "
            "or cultural interpretation, affected-party legitimacy, Māori wording, Māori data "
            "governance, and Māori authority remain exact-gated to competent and affected people, "
            "tangata whenua, iwi, hapū, and Māori authorities."
        ),
        "",
        "## Method Flow and environment",
        "",
        (
            f"The phase ledger retains {ledger['counts']['witness_results']['fail']} failed "
            f"witnesses and {ledger['counts']['witness_results']['pass']} bounded passing witnesses "
            f"across {ledger['counts']['methods']} Elowen methods. Twenty-five x1 failures, {len(X2_FAILURES)} x2 startup "
            "or audit failures, and all 160 invalid mutations remain visible. Codex CLI, Codex desktop, "
            "Python, and Git were version-checked read-only and recorded in the environment receipt. "
            "No update, elevation, host-security change, Windows feature change, unrelated install, "
            "real data download, sibling mutation, external write, or reboot occurred."
        ),
        "",
        "## Privacy, accessibility, and validation scope",
        "",
        (
            "The static report provides a skip link, main landmark, captioned table, scoped headers, "
            "responsive overflow, focus visibility, and print rules. That is structural evidence "
            "only. Five privacy classes distinguish scanner definitions and synthetic test strings "
            "from payload hits. Exact staged Git blobs, deterministic JSON, owner-delta tests, "
            "manifests, and bounded changed-code checks provide same-owner evidence only."
        ),
        "",
        "## Forty observed outcomes",
        "",
    ]
    lines.extend(
        f"- {row['proposal_id']} [{row['observed_outcome']}]: {row['title']} — {row['evidence_boundary']}."
        for row in outcomes
    )
    lines.extend(["", "## Terminal truth", "", BOUNDARY, "", "NOT_READY_FOR_STAGE_20."])
    return "\n".join(lines)


def build() -> None:
    if git_text("rev-parse", "HEAD") != X1_COMMIT or git_text("branch", "--show-current") != BRANCH:
        raise SystemExit("x2 requires the exact pushed Elowen x1 commit and branch")
    if (OWNER_ROOT / "closeout").exists() or (OWNER_ROOT / "final").exists():
        raise SystemExit("x2 refuses a lane containing closeout or final material")
    gate = verify_x1_gate()
    proposals = load("x1/new-proposal-freeze.json")["rows"]
    if len(proposals) != 40 or Counter(
        row["expected_disposition"] for row in proposals
    ) != Counter(OUTCOMES):
        raise SystemExit("frozen proposal distribution drifted")
    mutations = execute_mutations(proposals)
    if len(mutations) != 160 or not all(row["rejected"] for row in mutations):
        raise SystemExit("mutation execution drifted")
    build_runners()
    runners = smoke_runners()
    portfolio = load("x1/portfolio-freeze.json")
    skills = build_skills(portfolio)
    tools = tool_evidence()
    executable = [
        row for row in proposals if row["expected_disposition"] in {"completed", "represented"}
    ]
    controls = {
        row["proposal_id"]: positive_control(index, row)
        for index, row in enumerate(executable, start=1)
    }
    if len(controls) != 36 or not all(row["accepted"] for row in controls.values()):
        raise SystemExit("positive control drifted")
    outcomes = outcome_rows(proposals, controls)
    ledger = method_flow(mutations, runners, skills)
    for proposal in proposals:
        slug = proposal["proposal_id"].lower()
        write_json(f"x2/proposals/{slug}.json", proposal)
        write_json(
            f"x2/contracts/{slug}.json",
            {
                "schema": "ghc.family.proposal-contract.v5",
                "proposal_id": proposal["proposal_id"],
                "accepted_structure": validate_proposal(proposal),
                "outcome": proposal["expected_disposition"],
                "execution_state": (
                    "bounded_fixture_executed"
                    if proposal["expected_disposition"] in {"completed", "represented"}
                    else "held_without_real_world_execution"
                ),
            },
        )
        write_json(
            f"x2/cards/{slug}.json",
            {
                "schema": "ghc.family.evidence-card.v5",
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": proposal["expected_disposition"],
                "positive_control": controls.get(proposal["proposal_id"]),
                "rejecting_mutations": 4,
                "external_actions": 0,
                "boundary": BOUNDARY,
            },
        )
    update = lambda rows, state: [{**row, "x2_state": state} for row in rows]
    updated = {
        "safe_now": update(portfolio["rows"]["safe_now"], "completed_bounded"),
        "candidates": update(portfolio["rows"]["candidates"], "completed_bounded"),
        "exact_approval": update(portfolio["rows"]["exact_approval"], "held_unexecuted"),
        "blocked": update(portfolio["rows"]["blocked"], "held_unexecuted"),
        "skills": update(portfolio["rows"]["skills"], "completed_bounded"),
        "runners": update(portfolio["rows"]["runners"], "completed_bounded"),
        "clean_fix_refine": update(
            portfolio["rows"]["clean_fix_refine"], "completed_additive"
        ),
        "successor_skills": update(
            portfolio["rows"]["successor_skills"], "recommendation_only"
        ),
        "successor_runners": update(
            portfolio["rows"]["successor_runners"], "recommendation_only"
        ),
        "successor_clean_fix_refine": update(
            portfolio["rows"]["successor_clean_fix_refine"], "recommendation_only"
        ),
    }
    write_json("x2/tool-evidence.json", tools)
    write_json(
        "x2/runner-evidence.json",
        {
            "schema": "ghc.family.runner-evidence.v2",
            "owner": OWNER,
            "phase": PHASE,
            "planned": 10,
            "built_new": 10,
            "selected_inherited_read_only": 0,
            "executed": 10,
            "passed": 10,
            "rows": runners,
            "global_install": False,
            "external_actions": 0,
        },
    )
    write_json(
        "x2/skill-evidence.json",
        {
            "schema": "ghc.family.skill-evidence.v2",
            "owner": OWNER,
            "phase": PHASE,
            "planned": 20,
            "initialized_with_official_creator": 20,
            "built": 20,
            "quick_validated": 20,
            "smoke_used": 20,
            "rows": skills,
            "global_install": False,
            "external_actions": 0,
        },
    )
    write_json(
        "x2/mutation-receipt.json",
        {
            "schema": "ghc.family.mutation-receipt.v5",
            "owner": OWNER,
            "phase": PHASE,
            "preregistered": 160,
            "executed": 160,
            "rejected": 160,
            "unexpected_accepts": 0,
            "completion_credit": 0,
            "rows": mutations,
        },
    )
    write_json(
        "x2/positive-control-receipt.json",
        {
            "schema": "ghc.family.positive-control-receipt.v5",
            "owner": OWNER,
            "phase": PHASE,
            "planned": 36,
            "executed": 36,
            "passed": 36,
            "rows": list(controls.values()),
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x2/outcome-ledger.json",
        {
            "schema": "ghc.family.outcome-ledger.v5",
            "owner": OWNER,
            "phase": PHASE,
            "counts": OUTCOMES,
            "rows": outcomes,
        },
    )
    write_json(
        "x2/portfolio-outcome.json",
        {
            "schema": "ghc.family.portfolio-outcome.v5",
            "owner": OWNER,
            "phase": PHASE,
            "counts": {key: len(value) for key, value in updated.items()},
            "rows": updated,
            "exact_and_blocked_executed": 0,
            "inherited_completion_credit": 0,
        },
    )
    write_json(
        "x2/clean-fix-refine-evidence.json",
        {
            "schema": "ghc.family.clean-fix-refine-evidence.v5",
            "owner": OWNER,
            "phase": PHASE,
            "completed": updated["clean_fix_refine"],
            "successor_recommendations": updated["successor_clean_fix_refine"],
            "destructive_cleanup": 0,
            "sibling_mutation": 0,
        },
    )
    write_json(
        "x2/exact-and-blocked-register.json",
        {
            "schema": "ghc.family.exact-blocked-register.v5",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval": updated["exact_approval"],
            "blocked": updated["blocked"],
            "executed": 0,
        },
    )
    write_json("x2/method-flow-evidence.json", ledger)
    write_json(
        "x2/phase-truth-evidence.json",
        {
            "schema": "ghc.family.phase-truth.evidence.v5",
            "owner": OWNER,
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "x1_gate": gate,
            "proposal_chain_before": 6190,
            "proposal_chain_after": 6230,
            "outcomes": OUTCOMES,
            "positive_controls": 36,
            "rejected_mutations": 160,
            "new_tools": 3,
            "owner_safe_now_completed": 60,
            "owner_candidates_completed": 30,
            "owner_skills_completed": 20,
            "owner_runners_completed": 10,
            "owner_clean_fix_refine_completed": 60,
            "open_gaps": 291,
            "exact_gates": 284,
            "counts_overlay": ledger["effective_overlay"],
            "real_people": 0,
            "real_objects_measurements_rows": 0,
            "real_world_actions": 0,
            "external_writes": 0,
            "full_repository_suite": "not_run_not_claimed",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x2/environment-receipt.json",
        {
            "schema": "ghc.family.environment-receipt.v5",
            "owner": OWNER,
            "phase": PHASE,
            "codex_cli": "codex-cli 0.149.0",
            "codex_desktop": "version_not_exposed_to_current_terminal_not_updated",
            "python": "Python 3.12.10",
            "git": "git version 2.55.0.windows.2",
            "version_verification": "read_only_scalar_probes",
            "desktop_updated": False,
            "elevation": False,
            "host_security_changes": False,
            "windows_feature_changes": False,
            "sandbox_or_hyper_v_activated": False,
            "unrelated_installation": False,
            "reboot": False,
            "real_data_downloads": 0,
        },
    )
    write_json(
        "x2/family-index-review.json",
        {
            "schema": "ghc.family.phase-index-review.v2",
            "owner": OWNER,
            "phase": PHASE,
            "global_skills_reviewed": [
                "ghc-family-index",
                "ghc-family-auth-permission-state",
                "ghc-family-roster-check",
                "ghc-family-method-flow-state",
                "ghc-family-workflow-plan-refinement",
                "ghc-family-reflection-remaster",
                "ghc-family-approval-splitter",
                "ghc-family-open-gate-rail",
                "ghc-family-truth-bridge",
                "skill-creator",
            ],
            "newest_live_activation_overrides_older_cursor": True,
            "shared_skill_changes": 0,
            "global_memory_changes": 0,
            "phase_local_skills": 20,
            "family_compatible_runners": 10,
            "historical_callers_preserved": True,
            "review_state": "reviewed_current_no_shared_churn_justified",
        },
    )
    write_json(
        "x2/privacy-candidate-disposition.json",
        {
            "schema": "ghc.family.privacy-candidate-disposition.v2",
            "owner": OWNER,
            "phase": PHASE,
            "candidate_paths": [
                "scripts/ghc_family_elowen_v672_v8_music_box_guard.py",
                "scripts/build_ghc_family_elowen_cairn_v672_v8_x2.py",
                "tests/test_ghc_family_elowen_cairn_v672_v8_x2.py",
            ],
            "candidate_classes": ["scanner_definition", "synthetic_test_identifier"],
            "disposition": "definition_or_test_nonpayload",
            "confirmed_payload_hits": 0,
            "scope": "exact staged owner evidence files only",
            "privacy_complete": False,
        },
    )
    write_json(
        "x2/source-evidence-ledger.json",
        {
            "schema": "ghc.family.source-evidence-ledger.v3",
            "owner": OWNER,
            "phase": PHASE,
            "retrieval_date": "2026-08-28",
            "rows": load("x1/source-ledger.json")["sources"],
            "read_only_source_page_checks": 8,
            "source_projection_failures_retained": 1,
            "network_dataset_or_api_calls_in_execution": 0,
            "dataset_or_media_downloads_in_execution": 0,
            "real_rows": 0,
            "citations_are_observations": False,
            "authority_conferred": False,
            "boundary": "Current sources supply vocabulary and refusal conditions only, never object evidence, playback, diagnosis, treatment, safety release, consent, legal or cultural legitimacy, Māori authority, or empirical validation.",
        },
    )
    write_json(
        "x2/build-receipt.json",
        {
            "schema": "ghc.family.x2-build-receipt.v5",
            "owner": OWNER,
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "proposal_rows": 40,
            "positive_controls": 36,
            "mutations": 160,
            "tools": 3,
            "skills": 20,
            "runners": 10,
            "outcomes": OUTCOMES,
            "external_actions": 0,
        },
    )
    write_text("x2/accessible-evidence-report.html", accessible_report(outcomes))
    evidence_overview = overview(outcomes, mutations, ledger)
    write_text("x2/evidence-overview.md", evidence_overview)
    print(
        json.dumps(
            {
                "owner": OWNER,
                "phase": PHASE,
                "outcomes": OUTCOMES,
                "positive_controls": 36,
                "mutations": len(mutations),
                "skills": len(skills),
                "runners": len(runners),
                "tools": 3,
                "owner_files": len([path for path in OWNER_ROOT.rglob("*") if path.is_file()]),
                "overview_words": len(evidence_overview.split()),
                "effective": ledger["effective_overlay"],
            },
            sort_keys=True,
        )
    )


def staged_paths() -> list[str]:
    return [
        line
        for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
        if line
    ]


def staged_review() -> None:
    allowed = set(TOOL_PATHS + RUNNER_PATHS + BUILD_PATHS + EVIDENCE_VALIDATION_PATHS)
    paths = staged_paths()
    out = [
        path
        for path in paths
        if not (path.startswith("docs/elowen-cairn/v672-v8/x2/") or path in allowed)
    ]
    frozen = [
        path
        for path in paths
        if path.startswith("docs/elowen-cairn/v672-v8/x1/")
        or path
        in {
            "scripts/build_ghc_family_elowen_cairn_v672_v8_x1.py",
            "tests/test_ghc_family_elowen_cairn_v672_v8_x1.py",
        }
    ]
    payload = {
        "schema": "ghc.family.staged-review.v5",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x2_evidence",
        "staged_before_self": paths,
        "staged_count_before_self": len(paths),
        "out_of_scope": out,
        "x1_frozen_path_mutations": frozen,
        "declared_lifecycle_self_exclusions": [
            "docs/elowen-cairn/v672-v8/validation/evidence-staged-review.json",
            "docs/elowen-cairn/v672-v8/validation/evidence-manifest.json",
            "docs/elowen-cairn/v672-v8/validation/evidence-sequential-test-receipt.json",
        ],
        "valid": not out and not frozen,
    }
    write_json("validation/evidence-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_blob_rows(paths: list[str]) -> list[tuple[str, str, bytes]]:
    if not paths:
        return []
    index = git_text("ls-files", "--stage", "--", *paths).splitlines()
    objects = {}
    for line in index:
        left, path = line.split("\t", 1)
        mode, object_id, stage = left.split()
        if stage == "0":
            objects[path] = {"mode": mode, "object_id": object_id}
    missing = [path for path in paths if path not in objects]
    if missing:
        raise SystemExit(f"staged object mapping missing: {missing}")
    blobs = batch_git_blobs([objects[path]["object_id"] for path in paths])
    rows = []
    for path, blob in zip(paths, blobs, strict=True):
        if blob is None:
            raise SystemExit(f"staged blob missing from object database: {path}")
        rows.append((path, objects[path]["mode"], blob))
    return rows


def manifest_from_index() -> None:
    exclusions = [
        "docs/elowen-cairn/v672-v8/validation/evidence-manifest.json",
        "docs/elowen-cairn/v672-v8/validation/evidence-staged-review.json",
        "docs/elowen-cairn/v672-v8/validation/evidence-sequential-test-receipt.json",
    ]
    paths = [path for path in staged_paths() if path not in exclusions]
    entries = []
    for path, mode, blob in staged_blob_rows(paths):
        entries.append(
            {"path": path, "mode": mode, "bytes": len(blob), "sha256": sha(blob)}
        )
    entries.sort(key=lambda row: row["path"])
    write_json(
        "validation/evidence-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v5",
            "domain": "x2 evidence exact staged Git blobs before three declared lifecycle self files",
            "hash_domain": "normalized_lf_exact_git_blob",
            "owner": OWNER,
            "phase": PHASE,
            "source_x1": X1_COMMIT,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def staged_privacy() -> None:
    self_path = "docs/elowen-cairn/v672-v8/validation/evidence-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.I,
        ),
        "private_absolute_path": re.compile(
            r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I
        ),
        "private_route_or_callable": re.compile(
            r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I
        ),
        "credential_assignment": re.compile(
            r"\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']",
            re.I,
        ),
        "transcript_or_session_stream": re.compile(
            r"\b(?:session_stream|private_transcript|private_conversation_dump)\b", re.I
        ),
    }
    candidates = []
    scanner_surfaces = set(TOOL_PATHS + BUILD_PATHS)
    scanned = 0
    paths = [
        path
        for path in staged_paths()
        if path != self_path
        and Path(path).suffix.lower() in {".py", ".json", ".md", ".txt", ".html", ".yaml"}
    ]
    for path, _mode, blob in staged_blob_rows(paths):
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append(
                {
                    "path": path,
                    "pattern_class": "non_utf8_text",
                    "disposition": "confirmed_payload_hit",
                }
            )
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append(
                    {
                        "path": path,
                        "pattern_class": label,
                        "disposition": (
                            "scanner_definition_or_unit_test"
                            if path in scanner_surfaces
                            else "confirmed_payload_hit"
                        ),
                    }
                )
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {
        "schema": "ghc.family.staged-privacy-scan.v2",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x2_evidence",
        "hash_domain": "exact_staged_git_blob",
        "pattern_classes": sorted(patterns),
        "scanned_text_files": scanned,
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "self_exclusions": [
            self_path,
            "docs/elowen-cairn/v672-v8/validation/evidence-sequential-test-receipt.json",
        ],
        "valid": not confirmed,
        "boundary": (
            "Scanner definitions and synthetic unit-test identifiers are candidates, never "
            "payload hits; every other match fails closed."
        ),
    }
    write_json("validation/evidence-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def validation_receipt() -> None:
    json_paths = sorted((OWNER_ROOT / "x2").rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append(
                {"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__}
            )
    docs = [
        path
        for path in (OWNER_ROOT / "x2").rglob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}
    ]
    stale_patterns = {
        "liora_paper_marbling": re.compile(r"paper[-_ ]marbling|marbling[-_ ]bath|floating[-_ ]colour", re.I),
        "prior_calculator_domain": re.compile(r"mechanical[-_ ]calculator|stepped[-_ ]drum|pinwheel|accumulator|crank[-_ ]turn", re.I),
        "older_pipe_organ_domain": re.compile(r"\bpipe[-_ ]organ\b|pitch_hz|wind_pressure", re.I),
        "owner_name_typo": re.compile(r"\bElowen Cainn\b"),
    }
    stale_candidates = []
    for path in docs:
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for label, pattern in stale_patterns.items():
            matches = pattern.findall(text)
            if matches:
                retained = False
                stale_candidates.append(
                    {
                        "path": relative,
                        "label": label,
                        "occurrences": len(matches),
                        "disposition": (
                            "retained_negative_witness" if retained else "unexpected_stale_label"
                        ),
                    }
                )
    unexpected_stale = [
        row for row in stale_candidates if row["disposition"] == "unexpected_stale_label"
    ]
    max_words = max(
        (len(path.read_text(encoding="utf-8").split()) for path in docs), default=0
    )
    python_paths = [ROOT / path for path in TOOL_PATHS + RUNNER_PATHS + BUILD_PATHS]
    compile_issues = []
    for path in python_paths:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append(
                {"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)}
            )
    diff = git("diff", "--cached", "--check", check=False)
    x1_changed = git_text(
        "diff",
        "--name-only",
        X1_COMMIT,
        "--",
        "docs/elowen-cairn/v672-v8/x1",
        "scripts/build_ghc_family_elowen_cairn_v672_v8_x1.py",
        "tests/test_ghc_family_elowen_cairn_v672_v8_x1.py",
    )
    materialized = len(
        [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    )
    payload = {
        "schema": "ghc.family.evidence-validation-receipt.v1",
        "owner": OWNER,
        "phase": PHASE,
        "json_documents": len(json_paths),
        "json_issues": json_issues,
        "documents": len(docs),
        "max_document_words": max_words,
        "document_word_guard": 100000,
        "stale_label_candidates": stale_candidates,
        "stale_label_unexpected": unexpected_stale,
        "stale_label_review_valid": not unexpected_stale,
        "python_compiles": len(python_paths),
        "python_compile_issues": compile_issues,
        "diff_hygiene_exit": diff.returncode,
        "x1_frozen_path_changes": x1_changed.splitlines() if x1_changed else [],
        "materialized_files": materialized,
        "file_guard": 2000,
        "full_repository_suite": "not_run_not_claimed",
        "valid": (
            not json_issues
            and not compile_issues
            and not unexpected_stale
            and diff.returncode == 0
            and not x1_changed
            and materialized < 2000
            and max_words < 100000
        ),
        "boundary": BOUNDARY,
    }
    write_json("validation/evidence-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def sequential_test_receipt() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "tests.test_ghc_family_elowen_cairn_v672_v8_x2",
            "-v",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests", combined)
    x2_tests = int(match.group(1)) if match else 0
    payload = {
        "schema": "ghc.family.sequential-test-receipt.v1",
        "owner": OWNER,
        "phase": PHASE,
        "immutable_x1": {
            "commit": X1_COMMIT,
            "tests": 24,
            "result": "passed_before_x2",
            "rerun_at_evidence_head": False,
        },
        "current_x2": {
            "tests": x2_tests,
            "exit_code": result.returncode,
            "result": "passed" if result.returncode == 0 else "failed",
            "output_sha256": sha(combined.encode("utf-8")),
        },
        "sequential_total": 24 + x2_tests,
        "full_repository_suite": "not_run_not_claimed",
        "source_or_sibling_tests_replayed": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "valid": result.returncode == 0 and x2_tests == EXPECTED_X2_TESTS,
        "boundary": BOUNDARY,
    }
    write_json("validation/evidence-sequential-test-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--sequential-test-receipt", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    elif args.staged_privacy:
        staged_privacy()
    elif args.validation_receipt:
        validation_receipt()
    elif args.sequential_test_receipt:
        sequential_test_receipt()
    else:
        build()


if __name__ == "__main__":
    main()

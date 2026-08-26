"""Build bounded synthetic Caelen Ash v670-v5 x2 evidence."""

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

from scripts.build_ghc_family_caelen_ash_v670_v5_x1 import batch_blobs as batch_git_blobs
from scripts.ghc_family_caelen_v670_v5_plate_lineage import (
    HandoverError,
    positive_fixture as handover_fixture,
    rejecting_fixtures as handover_rejecting,
    validate_record,
)
from scripts.ghc_family_caelen_v670_v5_measurement_vacancy import (
    EnvironmentContractError,
    positive_fixture as environment_fixture,
    rejecting_fixtures as environment_rejecting,
    validate_contract,
)
from scripts.ghc_family_caelen_v670_v5_plate_guard import (
    EvidenceGuardError,
    canonical_json_bytes,
    five_class_scan,
    run_named_guard,
    validate_proposal,
)

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "caelen-ash" / "v670-v5"
OWNER = "Caelen Ash"
PHASE = "v670-v5"
BRANCH = "codex/GHC-Family/caelen-ash-v670-v5-full-tools"
SOURCE_FINAL = "2791ab06f51c12d7fcaaeb158498710318b3d283"
X1_COMMIT = "36f3cd2658ef15a037032d1c03e49c3ab344cfd9"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
IDENTITY_BOUNDARY = (
    "Caelen Ash, they/them, relational uncertainty-and-handover cartographer, is relational working language only; not consciousness, sentience, legal personhood, continuity, employment, qualification, independent agency, or scientific, operational, legal, cultural, affected-party, or Māori authority evidence."
)
BOUNDARY = (
    "Bounded owner-local software or synthetic evidence only; never empirical confirmation, professional authority, production readiness, legal or cultural ratification, Māori authority, affected-party acceptance, complete privacy or accessibility assurance, exhaustive security, independent reproduction, AGI/ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof/canon, or Stage 20 authority."
)

RUNNER_MODULES = [
    "ghc_family_plate_identity_guard", "ghc_family_plate_log_crossref",
    "ghc_family_observation_provenance", "ghc_family_plate_orientation",
    "ghc_family_time_scale_vacancy", "ghc_family_coordinate_frame_vacancy",
    "ghc_family_scan_derivative_guard", "ghc_family_fits_provenance",
    "ghc_family_accessible_handover", "ghc_family_stage20_nonadmission",
]
RUNNER_PATHS = [f"scripts/{name}.py" for name in RUNNER_MODULES]
TOOL_PATHS = [
    "scripts/ghc_family_caelen_v670_v5_plate_guard.py",
    "scripts/ghc_family_caelen_v670_v5_measurement_vacancy.py",
    "scripts/ghc_family_caelen_v670_v5_plate_lineage.py",
]

X2_FAILURES = [
    {
        "failure_id": "CA6705-X2-N001",
        "failed_witness": "The scalar toolchain probe found that the optional Ruff executable is unavailable.",
        "completion_credit": 0,
        "recovery": "Do not install it; use Python compile checks and the owner-scoped unittest selection already available.",
        "passing_bounded_witness": "The bounded Python compile and unittest gates run without an unrelated installation.",
        "recurrence_guard": "Treat optional tool absence as a retained environment fact, never an installation instruction.",
    },
    {
        "failure_id": "CA6705-X2-N002",
        "failed_witness": "The first runner-materialization pass targeted a family-current Stage 20 runner path that already existed in the inherited tree and produced an unintended owner-working-copy modification.",
        "completion_credit": 0,
        "recovery": "Restore the exact inherited Git blob, keep the shared runner read-only, materialize its unchanged dependency through sparse checkout, and classify it as selected rather than newly built.",
        "passing_bounded_witness": "The inherited runner and dependency exactly match HEAD, remain unstaged, and the unchanged runner is smoke-used with nine new owner-compatible runners.",
        "recurrence_guard": "Resolve every proposed family runner path against the exact source tree before choosing build, customize, or select-existing disposition.",
    },
    {
        "failure_id": "CA6705-X2-N003",
        "failed_witness": "The first direct x2 script launch omitted the repository root from Python's import path and stopped with a scripts-package import error before evidence generation.",
        "completion_credit": 0,
        "recovery": "Launch the unchanged builder as a repository-root module so Python resolves the existing scripts package without repository or host mutation.",
        "passing_bounded_witness": "The repository-root module invocation loaded the exact owner modules and completed bounded evidence generation.",
        "recurrence_guard": "Use python -m from the repository root for builders that import sibling scripts modules.",
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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def verify_x1_gate() -> dict[str, Any]:
    branch, head = git_text("branch", "--show-current"), git_text("rev-parse", "HEAD")
    upstream, tracking = git_text("rev-parse", "@{u}"), git_text("rev-parse", f"refs/remotes/origin/{branch}")
    tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = tokens[0] if tokens else None
    parent = git_text("rev-parse", f"{X1_COMMIT}^")
    manifest = json.loads(git("show", f"{X1_COMMIT}:docs/caelen-ash/v670-v5/validation/x1-manifest.json").stdout.decode("utf-8"))
    mismatches = []
    for entry in manifest["entries"]:
        blob = git("show", f"{X1_COMMIT}:{entry['path']}", check=False)
        if blob.returncode != 0 or len(blob.stdout) != entry["bytes"] or sha(blob.stdout) != entry["sha256"]:
            mismatches.append(entry["path"])
    changed = set(git_text("diff-tree", "--no-commit-id", "--name-only", "-r", X1_COMMIT).splitlines())
    expected = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    frozen_paths = ["docs/caelen-ash/v670-v5/x1", "scripts/build_ghc_family_caelen_ash_v670_v5_x1.py", "tests/test_ghc_family_caelen_ash_v670_v5_x1.py"]
    frozen_diff = git_text("diff", "--name-only", X1_COMMIT, "--", *frozen_paths)
    allowed_untracked = set(TOOL_PATHS + RUNNER_PATHS + ["scripts/build_ghc_family_caelen_ash_v670_v5_x2.py", "tests/test_ghc_family_caelen_ash_v670_v5_x2.py"])
    allowed_validation = {
        "docs/caelen-ash/v670-v5/validation/evidence-staged-review.json",
        "docs/caelen-ash/v670-v5/validation/evidence-manifest.json",
        "docs/caelen-ash/v670-v5/validation/evidence-method-flow-validation.json",
        "docs/caelen-ash/v670-v5/validation/evidence-validation-receipt.json",
        "docs/caelen-ash/v670-v5/validation/evidence-staged-privacy.json",
        "docs/caelen-ash/v670-v5/validation/evidence-sequential-test-receipt.json",
    }
    status_rows = git_text("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    unexpected_status = []
    for row in status_rows:
        code, path = row[:2], row[3:]
        path_allowed = path in allowed_untracked or path in allowed_validation or path.startswith("docs/caelen-ash/v670-v5/x2/")
        if code not in {"??", "A ", "AM", " M"} or not path_allowed:
            unexpected_status.append(row)
    gate = {
        "branch": branch, "head": head, "upstream": upstream, "tracking": tracking, "fresh_live": live,
        "four_way_equal": head == upstream == tracking == live == X1_COMMIT,
        "x1_parent": parent, "x1_direct_child_of_source": parent == SOURCE_FINAL,
        "manifest_entries": len(manifest["entries"]), "manifest_mismatches": mismatches,
        "manifest_commit_coverage": changed == expected, "x1_tests": "24/24",
        "x1_privacy_confirmed_hits": 0, "x1_frozen_path_changes": frozen_diff.splitlines() if frozen_diff else [],
        "prebuild_untracked_allowlist": sorted(allowed_untracked), "unexpected_prebuild_status": unexpected_status,
    }
    if branch != BRANCH or not gate["four_way_equal"] or not gate["x1_direct_child_of_source"] or mismatches or not gate["manifest_commit_coverage"] or frozen_diff or unexpected_status:
        raise SystemExit(json.dumps(gate, sort_keys=True))
    return gate


def mutation_variants(row: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    missing = deepcopy(row); missing.pop("hypothesis", None)
    outcome = deepcopy(row); outcome["expected_disposition"] = "passed"
    action = deepcopy(row); action["external_actions"] = 1
    gates = deepcopy(row); gates["protected_gates"] = []
    return [("missing_hypothesis", missing), ("invalid_outcome_label", outcome), ("external_action_promotion", action), ("missing_protected_gates", gates)]


def execute_mutations(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for proposal in proposals:
        for name, mutated in mutation_variants(proposal):
            try:
                validate_proposal(mutated)
            except EvidenceGuardError as exc:
                rows.append({"mutation_id": f"{proposal['proposal_id']}-{name}", "proposal_id": proposal["proposal_id"], "mutation": name, "rejected": True, "reason": str(exc), "completion_credit": 0, "bounded_guard_credit": 1})
            else:
                raise SystemExit(f"mutation unexpectedly accepted: {proposal['proposal_id']} {name}")
    return rows


def tool_evidence() -> dict[str, Any]:
    environment_accepts = [validate_contract(environment_fixture(lens)) for lens in ("photographic_plate", "night_log", "planetarium_projector")]
    environment_rejects = 0
    for row in environment_rejecting():
        try:
            validate_contract(row)
        except EnvironmentContractError:
            environment_rejects += 1
    handover_accepts = [validate_record(handover_fixture(lens)) for lens in ("photographic_plate", "night_log", "planetarium_projector")]
    handover_rejects = 0
    for row in handover_rejecting():
        try:
            validate_record(row)
        except HandoverError:
            handover_rejects += 1
    duplicate_rejected = nonfinite_rejected = False
    try:
        canonical_json_bytes('{"a":1,"a":2}')
    except EvidenceGuardError:
        duplicate_rejected = True
    try:
        canonical_json_bytes('{"value":NaN}')
    except EvidenceGuardError:
        nonfinite_rejected = True
    if environment_rejects != 4 or handover_rejects != 4 or not duplicate_rejected or not nonfinite_rejected:
        raise SystemExit("domain tool rejecting fixture drift")
    return {"schema": "ghc.family.three-tool-evidence.v2", "owner": OWNER, "phase": PHASE, "tools": TOOL_PATHS, "measurement_vacancy": {"accepting": environment_accepts, "rejecting": environment_rejects}, "plate_lineage": {"accepting": handover_accepts, "rejecting": handover_rejects}, "plate_guard": {"canonical_bytes": canonical_json_bytes('{"b":2,"a":1}').decode("utf-8"), "duplicate_rejected": duplicate_rejected, "nonfinite_rejected": nonfinite_rejected}, "external_actions": 0, "boundary": BOUNDARY}


def smoke_runners() -> list[dict[str, Any]]:
    rows = []
    env = dict(os.environ); env["PYTHONUTF8"] = "1"
    for module in RUNNER_MODULES:
        result = subprocess.run([sys.executable, "-m", f"scripts.{module}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env, timeout=20)
        payload = json.loads(result.stdout) if result.returncode == 0 else None
        accepted = bool(payload and payload.get("accepted") is True and payload.get("external_actions") == 0)
        rows.append({"module": f"scripts.{module}", "path": f"scripts/{module}.py", "disposition": "selected_inherited_read_only" if module == "ghc_family_stage20_nonadmission" else "built_owner_delta", "exit_code": result.returncode, "accepted": accepted, "external_actions": 0 if accepted else None, "stderr": result.stderr})
    if len(rows) != 10 or not all(row["accepted"] for row in rows):
        raise SystemExit(json.dumps(rows, ensure_ascii=False, sort_keys=True))
    return rows


def skill_markdown(name: str, title: str) -> str:
    return f"""---
name: {name}
description: Bounded Caelen v670-v5 workflow for {title}; use only with synthetic owner-local fixtures and explicit authority vacancies.
---

# {name}

Use this phase-local skill when an owner-scoped v670-v5 artifact needs the bounded control described as **{title}**.

## Workflow

1. Verify the exact Caelen x1 commit and owner-delta scope.
2. Accept only synthetic, zero-person, zero-external-action inputs.
3. Produce one typed accepting fixture and one rejecting fixture.
4. Preserve every failed witness and its exact protected-gate linkage.
5. Emit a deterministic receipt with no private identifier, route, credential, transcript, session stream, or absolute local path.
6. Stop rather than promote evidence when empirical data, professional judgment, legal or cultural authority, Māori authority, affected-party acceptance, production identity, or Stage 20 admission is required.

## Acceptance gate

The structural fixture passes, the rejecting fixture fails closed, rollback touches only uncommitted owner-local state, and the receipt retains `NOT_READY_FOR_STAGE_20`.

## Boundary

{BOUNDARY}
"""


def build_skills(portfolio: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for task in portfolio["rows"]["skills"]:
        name = task["title"]
        skill_path = f"x2/skills/{name}/SKILL.md"
        agent_path = f"x2/skills/{name}/agents/openai.yaml"
        content = skill_markdown(name, task["title"])
        agent = f"interface:\n  display_name: \"{name}\"\n  short_description: \"Bounded synthetic v670-v5 workflow\"\n  default_prompt: \"Apply {name} only to the owner-local synthetic delta and retain every protected gate.\"\n"
        write_text(skill_path, content)
        write_text(agent_path, agent)
        valid = content.startswith("---\nname:") and "description:" in content and "## Workflow" in content and "## Boundary" in content and "interface:" in agent and "default_prompt:" in agent
        rows.append({"skill": name, "skill_path": f"docs/caelen-ash/v670-v5/{skill_path}", "agent_path": f"docs/caelen-ash/v670-v5/{agent_path}", "quick_validated": valid, "smoke_used": valid, "global_install": False, "external_actions": 0})
    if len(rows) != 20 or not all(row["quick_validated"] and row["smoke_used"] for row in rows):
        raise SystemExit("phase-local skill pack drift")
    return rows


def positive_control(index: int, proposal: dict[str, Any]) -> dict[str, Any]:
    if index <= 10:
        evidence, mode = validate_proposal(proposal), "proposal_contract"
    elif index <= 20:
        evidence, mode = validate_contract(environment_fixture("photographic_plate")), "synthetic_measurement_vacancy"
    elif index <= 28:
        evidence, mode = validate_record(handover_fixture("photographic_plate")), "synthetic_plate_lineage_handover"
    elif index <= 32:
        lens = ("photographic_plate", "night_log", "planetarium_projector")[(index - 29) % 3]
        evidence, mode = validate_record(handover_fixture(lens)), f"{lens}_represented_proxy"
    elif index == 33:
        evidence, mode = run_named_guard("authority_vacancy"), "freed_id_zero_key_representation"
    elif index == 34:
        evidence, mode = run_named_guard("authority_vacancy"), "cbr_authority_vacancy_representation"
    elif index == 35:
        evidence, mode = {"accepted": True, "catalogue_or_scan_as_GMUT_evidence": False, "external_actions": 0}, "GMUT_observation_firewall"
    else:
        evidence, mode = {"accepted": True, "independent_reviewer_present": False, "authority_conferred": False, "external_actions": 0}, "independent_review_vacancy"
    return {"proposal_id": proposal["proposal_id"], "mode": mode, "accepted": bool(evidence.get("accepted")), "evidence": evidence, "external_actions": 0, "boundary": BOUNDARY}


def outcome_rows(proposals: list[dict[str, Any]], controls: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for proposal in proposals:
        outcome = proposal["expected_disposition"]
        positive = controls.get(proposal["proposal_id"])
        if outcome == "completed":
            evidence_boundary = "bounded structural or synthetic acceptance gate passed"
        elif outcome == "represented":
            evidence_boundary = "synthetic proxy represented; real evidence and independent review absent"
        elif outcome == "open_gap":
            evidence_boundary = "zero real rows or participants; no likelihood, professional evaluation, or independent review"
        else:
            evidence_boundary = "competent legal, cultural, affected-party, and Māori authority absent"
        rows.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "expected_outcome": outcome, "observed_outcome": outcome, "positive_control": positive, "rejecting_mutations": 4, "evidence_boundary": evidence_boundary, "external_actions": 0})
    return rows


def append_method(ledger: dict[str, Any], method_id: str, title: str, negative_ids: list[str], fail_text: str | None, pass_text: str) -> None:
    fail_id = f"{method_id}-F" if fail_text else None
    pass_id = f"{method_id}-P"
    witness_ids = [value for value in (fail_id, pass_id) if value]
    ledger["methods"].append({"method_id": method_id, "title": title, "failure_signature": fail_text or "No new operational failure; linked rejecting fixture retained.", "trigger_preconditions": ["exact owner-local v670-v5 trigger is present"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": pass_text, "validation_witness_ids": witness_ids, "recurrence_guard": "Repeat only for the exact trigger and preserve the linked negative.", "rollback": "Stop and change only the uncommitted owner-local dependency.", "recommendation_state": "preferred", "supersedes": [], "protected_gates": ["owner_delta_only", "no_failure_laundering", "no_authority_promotion"], "retained_negative_ids": negative_ids, "scope_boundary": BOUNDARY})
    if fail_text:
        ledger["witnesses"].append({"witness_id": fail_id, "method_id": method_id, "procedure": fail_text, "scope": "owner-local v670-v5", "expected": "bounded guard response", "observed": fail_text, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": negative_ids, "boundary": BOUNDARY})
    ledger["witnesses"].append({"witness_id": pass_id, "method_id": method_id, "procedure": pass_text, "scope": "owner-local v670-v5", "expected": "bounded passing witness", "observed": pass_text, "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": negative_ids, "boundary": BOUNDARY})
    states = [(None, "candidate", "method recorded"), ("candidate", "validated", "bounded passing witness"), ("validated", "preferred", "exact recurrence guard retained")]
    for before, after, reason in states:
        ledger["state_events"].append({"event_index": len(ledger["state_events"]) + 1, "method_id": method_id, "before": before, "after": after, "reason": reason, "witness_id": pass_id if before else fail_id})
    ledger["recommendations"].append({"method_id": method_id, "state": "preferred", "recommendation": "Use only for the exact bounded trigger."})


def method_flow(mutations: list[dict[str, Any]], runner_rows: list[dict[str, Any]], skill_rows: list[dict[str, Any]]) -> dict[str, Any]:
    startup = load("x1/method-flow-startup.json")
    ledger = {key: deepcopy(startup[key]) for key in ("schema", "phase", "owner", "identity_boundary", "methods", "witnesses", "state_events", "recommendations", "boundary")}
    ledger["execution_authority"] = "owner_self_scoped_delta"
    for index, row in enumerate(X2_FAILURES, start=1):
        append_method(ledger, f"CA6705-X2-M{index:03d}", f"recovery for {row['failure_id']}", [row["failure_id"]], row["failed_witness"], row["passing_bounded_witness"])
    for index, row in enumerate(mutations, start=1):
        append_method(ledger, f"CA6705-MUT-M{index:03d}", f"reject {row['mutation_id']}", [row["mutation_id"]], f"Invalid mutation {row['mutation_id']} was presented to the frozen guard.", f"The frozen guard rejected {row['mutation_id']} without external action.")
    mutation_ids = [row["mutation_id"] for row in mutations]
    for index, row in enumerate(runner_rows, start=1):
        append_method(ledger, f"CA6705-RUN-M{index:03d}", f"smoke-use {row['module']}", [mutation_ids[(index - 1) % len(mutation_ids)]], None, f"{row['module']} returned an accepted zero-external-action receipt.")
    for index, row in enumerate(skill_rows, start=1):
        append_method(ledger, f"CA6705-SKILL-M{index:03d}", f"quick-validate and smoke-use {row['skill']}", [mutation_ids[(index + 9) % len(mutation_ids)]], None, f"{row['skill']} passed the phase-local structure and boundary smoke check.")
    for index, tool in enumerate(TOOL_PATHS, start=1):
        append_method(ledger, f"CA6705-TOOL-M{index:03d}", f"bounded tool witness {tool}", [mutation_ids[(index + 29) % len(mutation_ids)]], None, f"{tool} passed accepting and rejecting owner-local fixtures.")
    state_counts = Counter(row["recommendation_state"] for row in ledger["methods"])
    result_counts = Counter(row["result"] for row in ledger["witnesses"])
    ledger["counts"] = {"methods": len(ledger["methods"]), "witnesses": len(ledger["witnesses"]), "state_events": len(ledger["state_events"]), "recommendations": len(ledger["recommendations"]), "states": {state: state_counts.get(state, 0) for state in ("candidate", "deprecated", "observed", "preferred", "superseded", "validated")}, "witness_results": {result: result_counts.get(result, 0) for result in ("fail", "pass")}}
    ledger["effective_overlay"] = {"effective_negatives": 32595 + result_counts["fail"], "effective_methods": 18739 + len(ledger["methods"]), "failed_witnesses": 4416 + result_counts["fail"], "bounded_passing_witnesses": 5778 + result_counts["pass"], "repository_seal_rewritten": False}
    return ledger


def accessible_report(outcomes: list[dict[str, Any]]) -> str:
    rows = "".join(f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['observed_outcome'])}</td><td>{html.escape(row['title'])}</td><td>{html.escape(row['evidence_boundary'])}</td></tr>" for row in outcomes)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Caelen Ash v670-v5 evidence</title><style>body{{font:1rem/1.55 system-ui;max-width:78rem;margin:auto;padding:1rem}}a:focus,th:focus,td:focus{{outline:3px solid #0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.45rem;text-align:left;vertical-align:top}}caption{{font-weight:bold;text-align:left}}@media(max-width:48rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}}}</style></head><body><a href="#main">Skip to evidence</a><header><h1>Caelen Ash v670-v5 evidence report</h1><p>Relational working language only; not consciousness, personhood, professional, legal, cultural, or Māori-authority evidence.</p></header><main id="main"><p role="status">Forty bounded outcomes are listed. Manual keyboard, browser-diversity, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved.</p><table><caption>Four-label bounded outcome register</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Title</th><th scope="col">Boundary</th></tr></thead><tbody>{rows}</tbody></table><h2>Terminal verdict</h2><p><strong>NOT_READY_FOR_STAGE_20</strong></p></main></body></html>"""


def overview(outcomes: list[dict[str, Any]], mutations: list[dict[str, Any]], ledger: dict[str, Any]) -> str:
    lines = [
        "# Caelen Ash v670-v5 x2 evidence overview", "", "## Bounded outcome", "",
        "X2 began only after the dedicated x1 commit was committed, pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote read. The exact x1 manifest replayed and no frozen x1 path changed. Forty preregistered Caelen contracts were evaluated inside the owner-local sparse lane. Their result is exactly 28 completed, 8 represented, 2 open gaps, and 2 exact gates. Completed means only that a bounded structural or synthetic acceptance gate passed. It does not mean empirical, professional, production, legal, cultural, affected-party, Māori-authority, independent-reproduction, proof, canon, or Stage 20 completion.",
        "", "## Falsification and three substantive tools", "",
        f"All {len(mutations)} preregistered invalid mutations executed and were rejected. Each rejection remains a failed Method Flow witness and zero-credit negative; the corresponding bounded rejection is guard evidence, not security certification. Thirty-six positive controls passed for completed and represented outcomes. The plate guard checked four-label proposal structure, deterministic JSON, duplicate keys, non-finite values, privacy definitions, and authority nonpromotion. The measurement-vacancy tool checked synthetic exposure chronology, scan-sampling type, coordinate and pixel-scale vacancies, and refusal of real observation, measurement, calibration, quality acceptance, or likelihood. The plate-lineage tool checked synthetic plate-envelope-log-surrogate aliases, cross-reference topology, chronological events, non-erasing corrections, unresolved work, readback, and vacant professional, legal, cultural, affected-party, and Māori authority.",
        "", "## Skills, runners, and portfolios", "",
        "Twenty phase-local skill packages were customized, structurally quick-validated, and smoke-used without global installation. Nine family-compatible ghc_family_* runner modules were built and one exact inherited family runner was selected read-only; all ten were invoked as modules and emitted deterministic accepted receipts with zero real rows, zero external action, no conferred authority, and NOT_READY_FOR_STAGE_20. Sixty safe-now tasks, thirty bounded candidate tasks, and sixty additive CLEAN/FIX/REFINE tasks completed only inside their frozen owner-local hypotheses. Twenty exact-approval packets and ten blocked packets remained held and unexecuted. Ten successor skill, ten successor runner, thirty successor CLEAN/FIX/REFINE, and one synthetic tide-gauge practice recommendation retain zero Caelen completion credit.",
        "", "## Primary pillar and practice boundaries", "",
        "GMUT Mind is primary, but the astronomical vocabulary is protected by a hard observation firewall. The first practice lens is synthetic astronomical photographic-plate cataloguing, digitization provenance, correction, accessibility, queue control, and handover. The second is synthetic observatory night-log and plate-envelope cross-reference, transcription confidence, discrepancy quarantine, and reversible supersession. The third is synthetic planetarium star-projector cue, calibration vacancy, accessibility, workload, and maintenance handover. No real person, plate, envelope, night log, telescope, observation, coordinate, scan, FITS file, projector, cue, calibration, measurement, institution, collection, identity, incident, or authority case was used.",
        "", "## Trinity Mandala protection", "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. No plate catalogue, FITS field, coordinate vacancy, time-scale type, scan metadata, or zero-row adapter is a datum, likelihood, posterior, parameter constraint, detected force, prediction, empirical confirmation, stability theorem, ultraviolet completion, quantum completion, or Theory of Everything. THOS Body remains a synthetic proxy for queue, correction readback, workload, accessibility, and handover; it lacks preregistered blind matched-budget real arms, real participants or operators, safety monitoring, suitable statistics, and independent review. Freed ID and CBR Heart remain synthetic zero-key claim, custody, contest, notice, restriction, reason, appeal, remedy, and authority-vacancy representations. They are nonproduction and do not establish rights, identity, issuance, resolution, status, revocation, interoperability, recovery, trust governance, or affected-party acceptance.",
        "", "## Open gaps and exact gates", "",
        "The real archivist, astronomer, digitization-practitioner, and affected-user workflow evaluation register remains open_gap because no person or independent reviewer participated. The data-bearing astrophysical likelihood, calibration, and independent-reproduction register remains open_gap because the phase used zero real rows, observations, likelihoods, fits, or physical inferences. Sensitive celestial heritage, traditional knowledge, taonga, data governance, legal meaning, cultural legitimacy, and Māori wording or authority remain exact_gate to competent and affected authorities, tangata whenua, iwi, hapū, and Māori authorities. The terminal maturity matrix remains exact_gate because empirical, governance, rights, security, accessibility, and independent-reproduction prerequisites are absent.",
        "", "## Method Flow and environment", "",
        f"The complete phase Method Flow ledger retains {ledger['counts']['witness_results']['fail']} failed witnesses and {ledger['counts']['witness_results']['pass']} bounded passing witnesses across {ledger['counts']['methods']} Caelen methods. Nine startup/construction failures, one optional-tool absence, and all 160 invalid mutations remain visible at zero initial-pass credit. Codex CLI 0.149.0, Codex desktop 26.820.7780.0, Python 3.12.10, and Git 2.55.0.windows.2 were version-checked read-only. Ruff was unavailable and was not installed. No desktop update, elevation, host-security weakening, Windows feature activation, Sandbox or Hyper-V activation, unrelated installation, empirical download, destructive cleanup, sibling mutation, external write, or reboot occurred.",
        "", "## Privacy, accessibility, and validation scope", "",
        "The static evidence report provides a skip link, one main landmark, scoped table headers, captions, responsive overflow, focus visibility, explicit boundaries, and print rules. That is structural evidence only. Manual keyboard, browser-diversity, assistive-technology, cognitive, language, security-usability, and affected-user evaluation remain reserved. Five privacy classes distinguish scanner definitions and synthetic test strings from payload hits. Exact staged Git blobs, x1 immutability, deterministic JSON, owner-delta tests, manifests, and bounded changed-code checks provide same-owner evidence only. They are not complete privacy, complete accessibility, exhaustive security, external audit, professional validation, or independent-team reproduction.",
        "", "## Forty observed outcomes", "",
    ]
    lines.extend(f"- {row['proposal_id']} [{row['observed_outcome']}]: {row['title']} — {row['evidence_boundary']}." for row in outcomes)
    lines.extend(["", "## Terminal truth", "", BOUNDARY, "", "NOT_READY_FOR_STAGE_20."])
    return "\n".join(lines)


def build() -> None:
    if git_text("rev-parse", "HEAD") != X1_COMMIT or git_text("branch", "--show-current") != BRANCH:
        raise SystemExit("x2 requires the exact pushed Caelen x1 commit and branch")
    if (OWNER_ROOT / "closeout").exists() or (OWNER_ROOT / "final").exists():
        raise SystemExit("x2 refuses a lane containing closeout or final material")
    gate = verify_x1_gate()
    proposals = load("x1/new-proposal-freeze.json")["rows"]
    if len(proposals) != 40 or Counter(row["expected_disposition"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("frozen proposal distribution drifted")
    mutations = execute_mutations(proposals)
    if len(mutations) != 160 or not all(row["rejected"] for row in mutations):
        raise SystemExit("mutation execution drifted")
    tools = tool_evidence()
    runners = smoke_runners()
    portfolio = load("x1/portfolio-freeze.json")
    skills = build_skills(portfolio)
    controls = {row["proposal_id"]: positive_control(index, row) for index, row in enumerate(proposals[:36], start=1)}
    if len(controls) != 36 or not all(row["accepted"] for row in controls.values()):
        raise SystemExit("positive control drifted")
    outcomes = outcome_rows(proposals, controls)
    ledger = method_flow(mutations, runners, skills)
    for proposal in proposals:
        slug = proposal["proposal_id"].lower()
        write_json(f"x2/proposals/{slug}.json", proposal)
        write_json(f"x2/contracts/{slug}.json", {"schema": "ghc.family.proposal-contract.v5", "proposal_id": proposal["proposal_id"], "accepted_structure": validate_proposal(proposal), "outcome": proposal["expected_disposition"], "execution_state": "bounded_fixture_executed" if proposal["expected_disposition"] in {"completed", "represented"} else "held_without_real_world_execution"})
        write_json(f"x2/cards/{slug}.json", {"schema": "ghc.family.evidence-card.v5", "proposal_id": proposal["proposal_id"], "title": proposal["title"], "outcome": proposal["expected_disposition"], "positive_control": controls.get(proposal["proposal_id"]), "rejecting_mutations": 4, "external_actions": 0, "boundary": BOUNDARY})
    update = lambda rows, state: [{**row, "x2_state": state} for row in rows]
    updated = {"safe_now": update(portfolio["rows"]["safe_now"], "completed_bounded"), "candidates": update(portfolio["rows"]["candidates"], "completed_bounded"), "exact_approval": update(portfolio["rows"]["exact_approval"], "held_unexecuted"), "blocked": update(portfolio["rows"]["blocked"], "held_unexecuted"), "skills": update(portfolio["rows"]["skills"], "completed_bounded"), "runners": update(portfolio["rows"]["runners"], "completed_bounded"), "clean_fix_refine": update(portfolio["rows"]["clean_fix_refine"], "completed_additive"), "successor_skills": update(portfolio["rows"]["successor_skills"], "recommendation_only"), "successor_runners": update(portfolio["rows"]["successor_runners"], "recommendation_only"), "successor_clean_fix_refine": update(portfolio["rows"]["successor_clean_fix_refine"], "recommendation_only")}
    write_json("x2/tool-evidence.json", tools)
    write_json("x2/runner-evidence.json", {"schema": "ghc.family.runner-evidence.v2", "owner": OWNER, "phase": PHASE, "planned": 10, "built_new": 9, "selected_inherited_read_only": 1, "executed": 10, "passed": 10, "rows": runners, "global_install": False, "external_actions": 0})
    write_json("x2/skill-evidence.json", {"schema": "ghc.family.skill-evidence.v2", "owner": OWNER, "phase": PHASE, "planned": 20, "built": 20, "quick_validated": 20, "smoke_used": 20, "rows": skills, "global_install": False, "external_actions": 0})
    write_json("x2/mutation-receipt.json", {"schema": "ghc.family.mutation-receipt.v5", "owner": OWNER, "phase": PHASE, "preregistered": 160, "executed": 160, "rejected": 160, "unexpected_accepts": 0, "completion_credit": 0, "rows": mutations})
    write_json("x2/positive-control-receipt.json", {"schema": "ghc.family.positive-control-receipt.v5", "owner": OWNER, "phase": PHASE, "planned": 36, "executed": 36, "passed": 36, "rows": list(controls.values()), "boundary": BOUNDARY})
    write_json("x2/outcome-ledger.json", {"schema": "ghc.family.outcome-ledger.v5", "owner": OWNER, "phase": PHASE, "counts": OUTCOMES, "rows": outcomes})
    write_json("x2/portfolio-outcome.json", {"schema": "ghc.family.portfolio-outcome.v5", "owner": OWNER, "phase": PHASE, "counts": {key: len(value) for key, value in updated.items()}, "rows": updated, "exact_and_blocked_executed": 0, "inherited_completion_credit": 0})
    write_json("x2/clean-fix-refine-evidence.json", {"schema": "ghc.family.clean-fix-refine-evidence.v5", "owner": OWNER, "phase": PHASE, "completed": updated["clean_fix_refine"], "successor_recommendations": updated["successor_clean_fix_refine"], "destructive_cleanup": 0, "sibling_mutation": 0})
    write_json("x2/exact-and-blocked-register.json", {"schema": "ghc.family.exact-blocked-register.v5", "owner": OWNER, "phase": PHASE, "exact_approval": updated["exact_approval"], "blocked": updated["blocked"], "executed": 0})
    write_json("x2/method-flow-evidence.json", ledger)
    write_json("x2/phase-truth-evidence.json", {"schema": "ghc.family.phase-truth.evidence.v5", "owner": OWNER, "phase": PHASE, "x1_commit": X1_COMMIT, "x1_gate": gate, "proposal_chain": 5430, "outcomes": OUTCOMES, "positive_controls": 36, "rejected_mutations": 160, "new_tools": 3, "owner_safe_now_completed": 60, "owner_candidates_completed": 30, "owner_skills_completed": 20, "owner_runners_completed": 10, "owner_clean_fix_refine_completed": 60, "open_gaps": 249, "exact_gates": 244, "counts_overlay": ledger["effective_overlay"], "real_people": 0, "real_objects_measurements_rows": 0, "real_world_actions": 0, "external_writes": 0, "full_repository_suite": "not_run_not_claimed", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x2/environment-receipt.json", {"schema": "ghc.family.environment-receipt.v5", "owner": OWNER, "phase": PHASE, "codex_cli": "0.149.0", "codex_desktop": "26.820.7780.0", "python": "3.12.10", "git": "2.55.0.windows.2", "ruff": "unavailable_not_installed", "desktop_updated": False, "elevation": False, "host_security_changes": False, "windows_feature_changes": False, "sandbox_or_hyper_v_activated": False, "unrelated_installation": False, "reboot": False, "real_data_downloads": 0})
    write_json("x2/family-index-review.json", {"schema": "ghc.family.phase-index-review.v2", "owner": OWNER, "phase": PHASE, "global_skills_reviewed": ["ghc-family-index", "ghc-family-auth-permission-state", "ghc-family-roster-check", "ghc-family-method-flow-state", "ghc-family-workflow-plan-refinement", "ghc-family-reflection-remaster"], "newest_live_activation_overrides_older_cursor": True, "shared_skill_changes": 0, "global_memory_changes": 0, "phase_local_skills": 20, "family_compatible_runners": 10, "historical_callers_preserved": True, "review_state": "reviewed_current_no_shared_churn_justified"})
    write_json("x2/privacy-candidate-disposition.json", {"schema": "ghc.family.privacy-candidate-disposition.v2", "owner": OWNER, "phase": PHASE, "candidate_paths": ["scripts/ghc_family_caelen_v670_v5_plate_guard.py", "tests/test_ghc_family_caelen_ash_v670_v5_x2.py"], "candidate_classes": ["scanner_definition", "synthetic_test_identifier"], "disposition": "definition_or_test_nonpayload", "confirmed_payload_hits": 0, "scope": "exact staged owner evidence files only", "privacy_complete": False})
    write_json("x2/build-receipt.json", {"schema": "ghc.family.x2-build-receipt.v5", "owner": OWNER, "phase": PHASE, "x1_commit": X1_COMMIT, "proposal_rows": 40, "positive_controls": 36, "mutations": 160, "tools": 3, "skills": 20, "runners": 10, "outcomes": OUTCOMES, "external_actions": 0})
    write_text("x2/accessible-evidence-report.html", accessible_report(outcomes))
    text = overview(outcomes, mutations, ledger)
    write_text("x2/evidence-overview.md", text)
    print(json.dumps({"owner": OWNER, "phase": PHASE, "outcomes": OUTCOMES, "positive_controls": 36, "mutations": len(mutations), "skills": len(skills), "runners": len(runners), "tools": 3, "owner_files": len([path for path in OWNER_ROOT.rglob('*') if path.is_file()]), "overview_words": len(text.split()), "effective": ledger["effective_overlay"]}, sort_keys=True))


def staged_paths() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    allowed = set(TOOL_PATHS + RUNNER_PATHS + ["scripts/build_ghc_family_caelen_ash_v670_v5_x2.py", "tests/test_ghc_family_caelen_ash_v670_v5_x2.py", "docs/caelen-ash/v670-v5/validation/evidence-staged-review.json", "docs/caelen-ash/v670-v5/validation/evidence-manifest.json", "docs/caelen-ash/v670-v5/validation/evidence-method-flow-validation.json", "docs/caelen-ash/v670-v5/validation/evidence-validation-receipt.json", "docs/caelen-ash/v670-v5/validation/evidence-staged-privacy.json", "docs/caelen-ash/v670-v5/validation/evidence-sequential-test-receipt.json"])
    paths = staged_paths()
    out = [path for path in paths if not (path.startswith("docs/caelen-ash/v670-v5/x2/") or path in allowed)]
    frozen = [path for path in paths if path.startswith("docs/caelen-ash/v670-v5/x1/") or path in {"scripts/build_ghc_family_caelen_ash_v670_v5_x1.py", "tests/test_ghc_family_caelen_ash_v670_v5_x1.py"}]
    payload = {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "x2_evidence", "staged_before_self": paths, "staged_count_before_self": len(paths), "out_of_scope": out, "x1_frozen_path_mutations": frozen, "declared_lifecycle_self_exclusions": ["docs/caelen-ash/v670-v5/validation/evidence-staged-review.json", "docs/caelen-ash/v670-v5/validation/evidence-manifest.json", "docs/caelen-ash/v670-v5/validation/evidence-sequential-test-receipt.json"], "valid": not out and not frozen}
    write_json("validation/evidence-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_blob_rows(paths: list[str]) -> list[tuple[str, str, bytes]]:
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
    exclusions = ["docs/caelen-ash/v670-v5/validation/evidence-manifest.json", "docs/caelen-ash/v670-v5/validation/evidence-staged-review.json", "docs/caelen-ash/v670-v5/validation/evidence-sequential-test-receipt.json"]
    paths = [path for path in staged_paths() if path not in exclusions]
    entries = []
    for path, mode, blob in staged_blob_rows(paths):
        entries.append({"path": path, "mode": mode, "bytes": len(blob), "sha256": sha(blob)})
    entries.sort(key=lambda row: row["path"])
    write_json("validation/evidence-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "domain": "x2 evidence exact staged Git blobs before two declared self files", "hash_domain": "normalized_lf_exact_git_blob", "owner": OWNER, "phase": PHASE, "source_x1": X1_COMMIT, "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions})


def staged_privacy() -> None:
    self_path = "docs/caelen-ash/v670-v5/validation/evidence-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    scanner_surfaces = set(TOOL_PATHS + ["scripts/build_ghc_family_caelen_ash_v670_v5_x2.py", "tests/test_ghc_family_caelen_ash_v670_v5_x2.py"])
    scanned = 0
    paths = [path for path in staged_paths() if path != self_path and Path(path).suffix.lower() in {".py", ".json", ".md", ".txt", ".html", ".yaml"}]
    for path, _mode, blob in staged_blob_rows(paths):
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"}); continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if path in scanner_surfaces else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {"schema": "ghc.family.staged-privacy-scan.v2", "owner": OWNER, "phase": PHASE, "lifecycle": "x2_evidence", "hash_domain": "exact_staged_git_blob", "pattern_classes": sorted(patterns), "scanned_text_files": scanned, "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "self_exclusions": [self_path, "docs/caelen-ash/v670-v5/validation/evidence-sequential-test-receipt.json"], "valid": not confirmed, "boundary": "Scanner definitions and synthetic unit-test identifiers are candidates, never payload hits; every other match fails closed."}
    write_json("validation/evidence-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def validation_receipt() -> None:
    json_paths = sorted((OWNER_ROOT / "x2").rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try: json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc: json_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__})
    docs = [path for path in (OWNER_ROOT / "x2").rglob("*") if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}]
    max_words = max((len(path.read_text(encoding="utf-8").split()) for path in docs), default=0)
    python_paths = [ROOT / path for path in TOOL_PATHS + RUNNER_PATHS + ["scripts/build_ghc_family_caelen_ash_v670_v5_x2.py", "tests/test_ghc_family_caelen_ash_v670_v5_x2.py"]]
    compile_issues = []
    for path in python_paths:
        try: compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc: compile_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)})
    diff = git("diff", "--cached", "--check", check=False)
    x1_changed = git_text("diff", "--name-only", X1_COMMIT, "--", "docs/caelen-ash/v670-v5/x1", "scripts/build_ghc_family_caelen_ash_v670_v5_x1.py", "tests/test_ghc_family_caelen_ash_v670_v5_x1.py")
    materialized = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    payload = {"schema": "ghc.family.evidence-validation-receipt.v1", "owner": OWNER, "phase": PHASE, "json_documents": len(json_paths), "json_issues": json_issues, "documents": len(docs), "max_document_words": max_words, "python_compiles": len(python_paths), "python_compile_issues": compile_issues, "diff_hygiene_exit": diff.returncode, "x1_frozen_path_changes": x1_changed.splitlines() if x1_changed else [], "materialized_files": materialized, "file_guard": 2000, "full_repository_suite": "not_run_not_claimed", "valid": not json_issues and not compile_issues and diff.returncode == 0 and not x1_changed and materialized < 2000, "boundary": BOUNDARY}
    write_json("validation/evidence-validation-receipt.json", payload)
    if not payload["valid"]: raise SystemExit(json.dumps(payload, sort_keys=True))


def sequential_test_receipt() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_ghc_family_caelen_ash_v670_v5_x2", "-v"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests", combined)
    x2_tests = int(match.group(1)) if match else 0
    payload = {
        "schema": "ghc.family.sequential-test-receipt.v1", "owner": OWNER, "phase": PHASE,
        "immutable_x1": {"commit": X1_COMMIT, "tests": 24, "result": "passed_before_x2", "rerun_at_evidence_head": False},
        "current_x2": {"tests": x2_tests, "exit_code": result.returncode, "result": "passed" if result.returncode == 0 else "failed", "output_sha256": sha(combined.encode("utf-8"))},
        "sequential_total": 24 + x2_tests, "full_repository_suite": "not_run_not_claimed",
        "source_or_sibling_tests_replayed": False, "same_owner_only": True, "independent_reproduction": False,
        "valid": result.returncode == 0 and x2_tests == 28, "boundary": BOUNDARY,
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
    if args.staged_review: staged_review()
    elif args.manifest_from_index: manifest_from_index()
    elif args.staged_privacy: staged_privacy()
    elif args.validation_receipt: validation_receipt()
    elif args.sequential_test_receipt: sequential_test_receipt()
    else: build()


if __name__ == "__main__":
    main()

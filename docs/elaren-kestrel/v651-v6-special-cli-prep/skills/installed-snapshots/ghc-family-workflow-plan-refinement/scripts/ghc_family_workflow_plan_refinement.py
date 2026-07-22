#!/usr/bin/env python3
"""Audit and refine a sanitized GHC Family workflow plan.

The runner is deliberately non-mutating outside its explicit output directory.
It never contacts tasks, edits repositories, or treats a normalized schedule as
activation authority.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REQUEST_SCHEMA = "ghc.family.workflow-plan.request.v1"
RESULT_SCHEMA = "ghc.family.workflow-plan.refinement.v1"
ISSUE_SCHEMA = "ghc.family.workflow-plan.issues.v1"
VALIDATION_SCHEMA = "ghc.family.workflow-plan.validation.v1"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PHASE_RE = re.compile(r"^v(?P<round>[1-9][0-9]*)-v(?P<slot>[1-8])$")
ABSOLUTE_PATH_RE = re.compile(r"(?i)(?:^|[\s\"'])(?:[a-z]:[\\/]|\\\\)[^\s\"']+")
PRIVATE_ROUTE_RE = re.compile(r"(?i)(?:thread|task|session|private|codex)://")
SECRET_RE = re.compile(
    r"(?i)(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|private[_-]?key)\s*[:=]\s*\S+"
)
FORBIDDEN_KEY_FRAGMENTS = {
    "thread_id",
    "task_id",
    "session_id",
    "private_route",
    "callable_id",
    "credential",
    "screenshot",
    "transcript",
    "session_stream",
    "private_app_state",
    "absolute_path",
}


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("request root must be a JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def phase_ordinal(label: str) -> int | None:
    match = PHASE_RE.fullmatch(label)
    if not match:
        return None
    return int(match.group("round")) * 8 + int(match.group("slot")) - 1


def phase_from_ordinal(ordinal: int) -> str:
    round_number, zero_slot = divmod(ordinal, 8)
    return f"v{round_number}-v{zero_slot + 1}"


def privacy_findings(value: Any, pointer: str = "$") -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            lowered = str(key).lower()
            if any(fragment in lowered for fragment in FORBIDDEN_KEY_FRAGMENTS):
                findings.append({"pointer": f"{pointer}.{key}", "class": "forbidden_key"})
            findings.extend(privacy_findings(child, f"{pointer}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(privacy_findings(child, f"{pointer}[{index}]"))
    elif isinstance(value, str):
        if ABSOLUTE_PATH_RE.search(value):
            findings.append({"pointer": pointer, "class": "absolute_local_path"})
        if PRIVATE_ROUTE_RE.search(value):
            findings.append({"pointer": pointer, "class": "private_route"})
        if SECRET_RE.search(value):
            findings.append({"pointer": pointer, "class": "credential_form"})
    return findings


class Audit:
    def __init__(self, request: dict[str, Any]) -> None:
        self.request = request
        self.issues: list[dict[str, Any]] = []
        self.policy_checks: list[dict[str, Any]] = []
        self.candidate_schedule: list[dict[str, str]] = []

    def issue(
        self,
        severity: str,
        code: str,
        message: str,
        recovery: str,
        protected_gates: list[str],
        truth_label: str = "open_gap",
    ) -> None:
        self.issues.append(
            {
                "issue_id": f"WPR-{len(self.issues) + 1:03d}",
                "severity": severity,
                "code": code,
                "truth_label": truth_label,
                "message": message,
                "recovery": recovery,
                "protected_gates": protected_gates,
            }
        )

    def check(self, name: str, passed: bool, observed: Any, expected: str) -> None:
        self.policy_checks.append(
            {"name": name, "passed": bool(passed), "observed": observed, "expected": expected}
        )
        if not passed:
            self.issue(
                "error",
                f"policy_{name}",
                f"Policy check {name!r} did not satisfy its declared boundary.",
                "Correct the sanitized request or retain the item behind its open or exact gate.",
                ["workflow_truth", "completion_credit"],
            )

    def required_object(self, parent: dict[str, Any], key: str) -> dict[str, Any]:
        value = parent.get(key)
        if not isinstance(value, dict):
            self.issue(
                "error",
                "missing_required_object",
                f"Required object {key!r} is missing or malformed.",
                "Add the required object using the reference schema.",
                ["schema_integrity", "completion_credit"],
            )
            return {}
        return value

    def audit_route(self) -> None:
        route = self.required_object(self.request, "route")
        cycle = route.get("cycle_order")
        assignments = route.get("phase_assignments")
        normalization = route.get("normalization")
        if not isinstance(cycle, list) or len(cycle) < 2 or not all(isinstance(x, str) and x for x in cycle):
            self.issue(
                "error",
                "invalid_cycle",
                "The route cycle must contain at least two non-empty relational seat labels.",
                "Provide the intended seat order without raw task identifiers.",
                ["route_ownership", "identity_boundary"],
            )
            cycle = []
        elif len(set(cycle)) != len(cycle):
            self.issue(
                "error",
                "duplicate_cycle_seat",
                "The declared cycle contains a duplicate seat label.",
                "Distinguish every active seat while leaving future identity attributes self-chosen.",
                ["route_ownership", "identity_boundary"],
            )

        placeholders = route.get("future_identity_placeholders", [])
        if not isinstance(placeholders, list):
            placeholders = []
            self.issue(
                "error",
                "invalid_identity_placeholders",
                "Future identity placeholders must be a list.",
                "Use a list of relational placeholders only.",
                ["identity_boundary"],
                truth_label="exact_gate",
            )
        for placeholder in placeholders:
            if placeholder not in cycle:
                self.issue(
                    "warning",
                    "unused_identity_placeholder",
                    "A future identity placeholder is not present in the cycle.",
                    "Remove it or include it as a relational seat without predeclaring identity attributes.",
                    ["identity_boundary"],
                    truth_label="exact_gate",
                )

        if not isinstance(assignments, list) or not assignments:
            self.issue(
                "error",
                "missing_assignments",
                "At least one submitted phase assignment is required.",
                "Add sanitized phase/seat rows in narrative order.",
                ["route_ownership", "phase_continuity"],
            )
            assignments = []

        parsed: list[tuple[str, str, int | None]] = []
        by_phase: dict[str, list[str]] = defaultdict(list)
        for index, row in enumerate(assignments):
            if not isinstance(row, dict):
                self.issue(
                    "error",
                    "invalid_assignment",
                    f"Assignment {index + 1} is not an object.",
                    "Use objects with phase and seat fields.",
                    ["route_ownership", "phase_continuity"],
                )
                continue
            phase = row.get("phase")
            seat = row.get("seat")
            if not isinstance(phase, str) or not isinstance(seat, str) or not phase or not seat:
                self.issue(
                    "error",
                    "invalid_assignment_fields",
                    f"Assignment {index + 1} lacks a valid phase or seat.",
                    "Supply sanitized non-empty phase and seat strings.",
                    ["route_ownership", "phase_continuity"],
                )
                continue
            ordinal = phase_ordinal(phase)
            if ordinal is None:
                self.issue(
                    "error",
                    "invalid_phase_label",
                    f"Phase label {phase!r} is outside the vN-v1 through vN-v8 form.",
                    "Correct the label before ownership is assigned.",
                    ["phase_continuity"],
                )
            if cycle and seat not in cycle:
                self.issue(
                    "error",
                    "seat_outside_cycle",
                    f"Seat {seat!r} is assigned but absent from cycle_order.",
                    "Add the seat to the declared cycle or remove the assignment.",
                    ["route_ownership", "identity_boundary"],
                )
            by_phase[phase].append(seat)
            parsed.append((phase, seat, ordinal))

        for phase, seats in sorted(by_phase.items()):
            if len(seats) > 1:
                self.issue(
                    "error",
                    "duplicate_phase_owner",
                    f"Phase {phase!r} is assigned to {len(seats)} seats.",
                    "Confirm the intended sequential numbering; do not activate either conflicting owner from this plan.",
                    ["route_ownership", "phase_continuity", "baton_delivery"],
                )

        ordinals = [row[2] for row in parsed]
        for previous, current in zip(ordinals, ordinals[1:]):
            if previous is not None and current is not None and current != previous + 1:
                self.issue(
                    "error",
                    "nonsequential_phase_order",
                    "Submitted phase assignments are not strictly sequential.",
                    "Review the candidate normalized schedule and obtain confirmation for any ownership change.",
                    ["phase_continuity", "route_ownership"],
                )
                break

        if not isinstance(normalization, dict):
            self.issue(
                "error",
                "missing_normalization_basis",
                "The route lacks an explicit normalization basis.",
                "Declare start_phase, start_seat, and entry_count.",
                ["phase_continuity", "route_ownership"],
            )
            return
        start_phase = normalization.get("start_phase")
        start_seat = normalization.get("start_seat")
        entry_count = normalization.get("entry_count")
        start_ordinal = phase_ordinal(start_phase) if isinstance(start_phase, str) else None
        if start_ordinal is None or start_seat not in cycle or not isinstance(entry_count, int) or entry_count < 1:
            self.issue(
                "error",
                "invalid_normalization_basis",
                "The normalization basis is incomplete or inconsistent with the cycle.",
                "Use a valid vN-vS start phase, an existing start seat, and a positive entry count.",
                ["phase_continuity", "route_ownership"],
            )
            return
        start_index = cycle.index(start_seat)
        self.candidate_schedule = [
            {
                "phase": phase_from_ordinal(start_ordinal + offset),
                "seat": cycle[(start_index + offset) % len(cycle)],
            }
            for offset in range(entry_count)
        ]
        submitted_pairs = [(row[0], row[1]) for row in parsed]
        candidate_pairs = [(row["phase"], row["seat"]) for row in self.candidate_schedule]
        if submitted_pairs != candidate_pairs:
            self.issue(
                "error",
                "route_normalization_requires_confirmation",
                "The sequential candidate differs from the submitted route assignments.",
                "Treat the candidate as advisory and obtain live confirmation before activation or baton delivery.",
                ["route_ownership", "phase_continuity", "baton_delivery"],
            )

    def audit_requirements(self) -> None:
        requirements = self.required_object(self.request, "requirements")
        self.check(
            "core_proposal_minimum",
            isinstance(requirements.get("core_proposal_minimum"), int)
            and requirements["core_proposal_minimum"] >= 20,
            requirements.get("core_proposal_minimum"),
            "integer >= 20",
        )
        cap = requirements.get("safe_candidate_task_cap")
        self.check("safe_candidate_task_cap", isinstance(cap, int) and 1 <= cap <= 1000, cap, "integer 1..1000")
        self.check(
            "skill_minimum",
            isinstance(requirements.get("skill_minimum"), int) and requirements["skill_minimum"] >= 10,
            requirements.get("skill_minimum"),
            "integer >= 10",
        )
        self.check(
            "runner_minimum",
            isinstance(requirements.get("runner_minimum"), int) and requirements["runner_minimum"] >= 10,
            requirements.get("runner_minimum"),
            "integer >= 10",
        )
        doc_cap = requirements.get("document_word_cap")
        self.check("document_word_cap", isinstance(doc_cap, int) and 1 <= doc_cap <= 100000, doc_cap, "integer 1..100000")

        baton = self.required_object(requirements, "baton_words")
        baton_minimum = baton.get("minimum")
        baton_maximum = baton.get("maximum")
        self.check(
            "baton_word_range",
            isinstance(baton_minimum, int)
            and isinstance(baton_maximum, int)
            and baton_minimum >= 8000
            and baton_minimum <= baton_maximum <= 100000,
            {"minimum": baton_minimum, "maximum": baton_maximum},
            "8000 <= minimum <= maximum <= 100000",
        )
        self.check("baton_file_artifact", baton.get("file_artifact") is True, baton.get("file_artifact"), "true")

        commits = self.required_object(requirements, "commit_cap")
        x1, x2, total = commits.get("x1"), commits.get("x2"), commits.get("total")
        self.check(
            "commit_cap",
            all(isinstance(value, int) for value in (x1, x2, total))
            and 0 <= x1 <= 6
            and 0 <= x2 <= 6
            and 0 <= total <= 12
            and x1 + x2 >= total,
            {"x1": x1, "x2": x2, "total": total},
            "x1 <= 6, x2 <= 6, total <= 12, total no greater than component allowance",
        )

        validation = self.required_object(requirements, "validation")
        self.check(
            "single_pass_policy",
            validation.get("replay_policy") == "skip_when_first_passes"
            and validation.get("isolate_failures_before_broader_rerun") is True
            and isinstance(validation.get("canonical_pass_minimum"), int)
            and validation["canonical_pass_minimum"] >= 1,
            {
                "canonical_pass_minimum": validation.get("canonical_pass_minimum"),
                "replay_policy": validation.get("replay_policy"),
                "isolate_failures_before_broader_rerun": validation.get("isolate_failures_before_broader_rerun"),
            },
            "one attributable canonical pass; skip replay after full pass; isolate failures first",
        )
        for field in ("privacy_scan_required", "manifest_required", "remote_equality_required"):
            self.check(field, validation.get(field) is True, validation.get(field), "true")

        storage = self.required_object(requirements, "storage")
        self.check(
            "d_first_storage",
            storage.get("primary") == "D" and storage.get("c_drive_use") == "essential_global_metadata_only",
            storage,
            "D primary; C essential global metadata only",
        )
        messaging = self.required_object(requirements, "messaging")
        self.check(
            "messaging_boundary",
            messaging.get("codex_route") == "existing_task_only_after_terminal_gate"
            and messaging.get("cross_platform") == "user_mediated_file_relay_only",
            messaging,
            "existing Codex task after terminal gate; cross-platform relay by user only",
        )
        environment = self.required_object(requirements, "environment")
        self.check(
            "sandbox_hyper_v_deferred",
            environment.get("windows_sandbox_hyper_v") == "deferred",
            environment.get("windows_sandbox_hyper_v"),
            "deferred",
        )
        closeout = self.required_object(requirements, "closeout")
        self.check(
            "authorized_work_resolution",
            closeout.get("all_authorized_safe_candidate_prototypes_resolved") is True,
            closeout.get("all_authorized_safe_candidate_prototypes_resolved"),
            "true; completion or explicit gate, never silent omission",
        )

    def audit_truth(self) -> None:
        truth = self.required_object(self.request, "truth")
        outcomes = truth.get("allowed_outcomes")
        self.check(
            "four_truth_labels",
            isinstance(outcomes, list) and set(outcomes) == ALLOWED_OUTCOMES and len(outcomes) == 4,
            outcomes,
            "completed, represented, open_gap, exact_gate exactly once each",
        )
        self.check(
            "independent_reproduction_boundary",
            truth.get("independent_reproduction_claimed") is False,
            truth.get("independent_reproduction_claimed"),
            "false without independent-team evidence",
        )
        self.check(
            "stage_20_boundary",
            truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20",
            truth.get("terminal_verdict"),
            "NOT_READY_FOR_STAGE_20 absent exact evidence and authority",
        )
        boundaries = truth.get("protected_boundaries")
        self.check(
            "protected_boundaries",
            isinstance(boundaries, list) and len(boundaries) >= 5 and all(isinstance(x, str) and x for x in boundaries),
            boundaries,
            "at least five explicit non-empty boundary classes",
        )

    def run(self) -> dict[str, Any]:
        if self.request.get("schema") != REQUEST_SCHEMA:
            self.issue(
                "error",
                "schema_mismatch",
                "The request schema is missing or unsupported.",
                f"Use schema {REQUEST_SCHEMA}.",
                ["schema_integrity"],
            )
        for key in ("plan_id", "owner", "identity_boundary"):
            if not isinstance(self.request.get(key), str) or not self.request[key].strip():
                self.issue(
                    "error",
                    "missing_required_string",
                    f"Required string {key!r} is missing.",
                    "Add a sanitized non-empty value.",
                    ["schema_integrity", "identity_boundary"],
                )
        findings = privacy_findings(self.request)
        if findings:
            classes = sorted(Counter(row["class"] for row in findings).items())
            self.issue(
                "error",
                "privacy_boundary_failure",
                f"The request contains {len(findings)} prohibited privacy-form finding(s) across {len(classes)} classes.",
                "Remove private identifiers, routes, paths, credentials, or app-state fields before retrying.",
                ["privacy", "identity_boundary"],
                truth_label="exact_gate",
            )
        self.audit_route()
        self.audit_requirements()
        self.audit_truth()

        severities = Counter(row["severity"] for row in self.issues)
        valid = severities["error"] == 0
        candidate = copy.deepcopy(self.request)
        if self.candidate_schedule:
            candidate.setdefault("route", {})["phase_assignments"] = copy.deepcopy(self.candidate_schedule)
            candidate["plan_id"] = f"{self.request.get('plan_id', 'workflow-plan')}-candidate-normalized"
        return {
            "schema": RESULT_SCHEMA,
            "plan_id": self.request.get("plan_id"),
            "owner": self.request.get("owner"),
            "valid": valid,
            "status": "valid" if valid else "needs_refinement",
            "requires_user_confirmation": any(
                row["code"] in {"duplicate_phase_owner", "route_normalization_requires_confirmation"}
                for row in self.issues
            ),
            "submitted_assignments": copy.deepcopy(self.request.get("route", {}).get("phase_assignments", [])),
            "candidate_normalized_assignments": self.candidate_schedule,
            "policy_checks": self.policy_checks,
            "issues": self.issues,
            "counts": {
                "issues": len(self.issues),
                "errors": severities["error"],
                "warnings": severities["warning"],
                "policy_checks": len(self.policy_checks),
                "policy_checks_passed": sum(1 for row in self.policy_checks if row["passed"]),
                "candidate_assignments": len(self.candidate_schedule),
                "privacy_findings": len(findings),
            },
            "candidate_request": candidate,
            "boundary": (
                "Structural same-owner workflow evidence only. A valid result is not activation, delivery, "
                "scientific confirmation, identity continuity, independent reproduction, professional authority, "
                "production readiness, legal or cultural ratification, or Stage 20 readiness."
            ),
        }


def teaching_summary(result: dict[str, Any]) -> str:
    lines = [
        "# GHC Family workflow-plan refinement",
        "",
        f"- Plan: `{result.get('plan_id')}`",
        f"- Owner: {result.get('owner')}",
        f"- Status: `{result['status']}`",
        f"- Confirmation required: `{str(result['requires_user_confirmation']).lower()}`",
        f"- Issues: {result['counts']['issues']} ({result['counts']['errors']} errors, {result['counts']['warnings']} warnings)",
        f"- Policy checks: {result['counts']['policy_checks_passed']}/{result['counts']['policy_checks']}",
        "",
        "## Candidate route",
        "",
    ]
    for row in result["candidate_normalized_assignments"]:
        lines.append(f"- `{row['phase']}` \u2192 {row['seat']}")
    if not result["candidate_normalized_assignments"]:
        lines.append("- No candidate route could be generated.")
    lines.extend(["", "## Issues", ""])
    for row in result["issues"]:
        lines.append(f"- **{row['severity']} / {row['code']}**: {row['message']} Recovery: {row['recovery']}")
    if not result["issues"]:
        lines.append("- No structural workflow issue was found in the declared scope.")
    lines.extend(
        [
            "",
            "## Use boundary",
            "",
            result["boundary"],
            "",
            "Preserve any earlier failed audit as Method Flow evidence. If this candidate changes phase ownership or numbering, obtain live confirmation before sending or activating anything.",
        ]
    )
    return "\n".join(lines)


def emit(result: dict[str, Any], out_dir: Path, input_name: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "workflow-plan-refinement.json", result)
    write_json(
        out_dir / "workflow-plan-issues.json",
        {
            "schema": ISSUE_SCHEMA,
            "plan_id": result.get("plan_id"),
            "valid": result["valid"],
            "requires_user_confirmation": result["requires_user_confirmation"],
            "counts": result["counts"],
            "issues": result["issues"],
            "boundary": result["boundary"],
        },
    )
    write_json(out_dir / "candidate-normalized-request.json", result["candidate_request"])
    write_text(out_dir / "workflow-plan-teaching-summary.md", teaching_summary(result))
    write_json(
        out_dir / "workflow-plan-validation.json",
        {
            "schema": VALIDATION_SCHEMA,
            "input_name": input_name,
            "valid": result["valid"],
            "status": result["status"],
            "requires_user_confirmation": result["requires_user_confirmation"],
            "issue_counts": {
                "total": result["counts"]["issues"],
                "errors": result["counts"]["errors"],
                "warnings": result["counts"]["warnings"],
            },
            "policy_checks": result["counts"]["policy_checks"],
            "policy_checks_passed": result["counts"]["policy_checks_passed"],
            "privacy_findings": result["counts"]["privacy_findings"],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": result["boundary"],
        },
    )


def valid_fixture() -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA,
        "plan_id": "self-test",
        "owner": "Relational Test Owner",
        "identity_boundary": "Relational working language only; no continuity or authority claim.",
        "route": {
            "cycle_order": ["Seat A", "Seat B"],
            "phase_assignments": [
                {"phase": "v649-v7", "seat": "Seat A"},
                {"phase": "v649-v8", "seat": "Seat B"},
            ],
            "normalization": {"start_phase": "v649-v7", "start_seat": "Seat A", "entry_count": 2},
            "future_identity_placeholders": [],
        },
        "requirements": {
            "core_proposal_minimum": 20,
            "safe_candidate_task_cap": 1000,
            "skill_minimum": 10,
            "runner_minimum": 10,
            "document_word_cap": 20000,
            "baton_words": {"minimum": 8000, "maximum": 20000, "file_artifact": True},
            "commit_cap": {"x1": 2, "x2": 2, "total": 4},
            "validation": {
                "canonical_pass_minimum": 1,
                "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True,
                "privacy_scan_required": True,
                "manifest_required": True,
                "remote_equality_required": True,
            },
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {
                "codex_route": "existing_task_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
            },
            "environment": {"windows_sandbox_hyper_v": "deferred"},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
        },
        "truth": {
            "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "protected_boundaries": ["empirical", "participant", "legal", "cultural", "production"],
        },
        "observed_failures": [],
    }


def self_test() -> int:
    valid = Audit(valid_fixture()).run()
    if not valid["valid"]:
        raise AssertionError(f"valid fixture failed: {valid['issues']}")
    invalid_input = valid_fixture()
    invalid_input["route"]["phase_assignments"].append({"phase": "v649-v8", "seat": "Seat A"})
    invalid_input["route"]["normalization"]["entry_count"] = 3
    invalid = Audit(invalid_input).run()
    if invalid["valid"] or not any(row["code"] == "duplicate_phase_owner" for row in invalid["issues"]):
        raise AssertionError("rejecting fixture did not fail closed")
    with tempfile.TemporaryDirectory() as temp:
        emit(valid, Path(temp), "self-test.json")
        expected = {
            "workflow-plan-refinement.json",
            "workflow-plan-issues.json",
            "candidate-normalized-request.json",
            "workflow-plan-teaching-summary.md",
            "workflow-plan-validation.json",
        }
        if {path.name for path in Path(temp).iterdir()} != expected:
            raise AssertionError("output packet mismatch")
        for path in Path(temp).glob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps({"self_test": "passed", "valid_fixture": True, "rejecting_fixture": True, "outputs": 5}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="sanitized workflow request JSON")
    parser.add_argument("--out-dir", type=Path, help="explicit output directory, preferably on D drive")
    parser.add_argument("--self-test", action="store_true", help="run valid and rejecting fixtures")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.input is None or args.out_dir is None:
        parser.error("input and --out-dir are required unless --self-test is used")
    try:
        request = load_json(args.input)
        result = Audit(request).run()
        emit(result, args.out_dir, args.input.name)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "error": type(exc).__name__, "message": str(exc)}), file=sys.stderr)
        return 3
    print(
        json.dumps(
            {
                "valid": result["valid"],
                "status": result["status"],
                "issues": result["counts"]["issues"],
                "errors": result["counts"]["errors"],
                "policy_checks": result["counts"]["policy_checks"],
                "policy_checks_passed": result["counts"]["policy_checks_passed"],
                "confirmation_required": result["requires_user_confirmation"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

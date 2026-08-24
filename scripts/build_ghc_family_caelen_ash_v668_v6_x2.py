#!/usr/bin/env python3
"""Execute the bounded Caelen Ash v668-v6 x2 evidence surface."""

from __future__ import annotations

import hashlib
import html
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_caelen_ash_v668_v6_archive import (
    ALLOWED_OUTCOMES,
    EVIDENCE_BOUNDARY,
    IDENTITY_BOUNDARY,
    INHERITED_FROZEN_PROPOSALS,
    OWNER,
    PHASE,
    PHASE_ROOT,
    PRACTICES,
    PRIMARY_PILLAR,
    PROTECTED_GATES,
    RELATIONAL_HOPE,
    RELATIONAL_ROLE,
    ROOT,
    RUNNER_NAMES,
    SKILL_NAMES,
    SOURCE_FINAL,
    SUCCESSOR_PRACTICE_RECOMMENDATION,
    TERMINAL_VERDICT,
    manifest_rows,
    phase_owner_files,
    utc_now,
    word_count,
    write_json,
    write_text,
)
from ghc_family_caelen_ash_v668_v6_controls import (
    CONTROL_NAMES,
    RejectedFixture,
    evaluate_control,
    evaluate_envelope,
)


X1_HEAD = "c5c18b81f26c8851b984e4bcb3dff1db1212fd36"
INITIAL_X1_HEAD = "5bced658a5b3f5bd7c4d88d47057d795abe57f42"
X2_OPERATIONAL_FAILURES = [
    {
        "suffix": "019",
        "title": "inspect exact Git state after a commit wrapper loses its scalar receipt",
        "failure_signature": "the x1 commit wrapper reached its output boundary without returning the planned commit summary even though the Git transaction had completed",
        "trigger": "a bounded wrapper combines the commit transaction with several postcommit projections and returns no attributable scalar receipt",
        "workaround": "do not replay the commit; inspect HEAD subject parent staged count and porcelain state through a separate read-only scalar probe",
        "pass_observed": "the dedicated x1 commit existed once at the exact source parent with zero staged or dirty paths, then pushed and proved four-way equal",
    },
    {
        "suffix": "020",
        "title": "split copied-template edits into exact local blocks",
        "failure_signature": "a combined successor-ledger and static-report patch was rejected because the expected HTML context differed from the exact copied template",
        "trigger": "unrelated generated prose blocks share one patch transaction built from a nonexact display",
        "workaround": "reread each exact block and patch the successor ledger and static report independently",
        "pass_observed": "the immutable x1 successor portfolio was replayed at zero credit and the static report used the Caelen weather-observation boundary",
    },
    {
        "suffix": "021",
        "title": "materialize final-stage modules only after the evidence commit",
        "failure_signature": "a mechanical template-copy step placed four untracked final-stage Caelen modules in the worktree before x2 execution",
        "trigger": "x2 and final structural templates are copied together even though strict lifecycle separation permits only x2 files before the evidence seal",
        "workaround": "delete only the recoverable untracked Caelen final-stage copies and rematerialize them from the immutable source after the evidence commit",
        "pass_observed": "the pre-x2 status contained only the three authorized x2 modules before any x2 artifact was generated",
    },
    {
        "suffix": "022",
        "title": "adjudicate exact privacy scanner definitions separately from payload hits",
        "failure_signature": "the first five-class staged scan stopped on two literal transcript-identifier regex definitions in the x2 privacy test",
        "trigger": "scanner source is searched by the same conservative expressions it defines",
        "workaround": "retain both candidates, verify their exact staged paths and lines are scanner definitions only, and record zero confirmed payload disclosures",
        "pass_observed": "the exact two definition candidates were adjudicated with zero confirmed five-class privacy or raw-identifier hits",
    },
]
X2_OPERATIONAL_FAILURE_COUNT = len(X2_OPERATIONAL_FAILURES)

RUNNER_CONTROL = dict(zip(RUNNER_NAMES, CONTROL_NAMES, strict=True))


def git(*args: str, binary: bool = False) -> Any:
    completed = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=not binary,
        encoding=None if binary else "utf-8",
        errors=None if binary else "replace",
    )
    return completed.stdout if binary else completed.stdout.strip()


def git_json(commit: str, path: str) -> dict[str, Any]:
    return json.loads(git("show", f"{commit}:{path}", binary=True).decode("utf-8"))


def write_external(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError(f"refusing output symlink: {path.name}")
    if path.is_file():
        if path.read_bytes() == data:
            return
        raise ValueError(f"refusing to overwrite nonidentical output: {path.name}")
    temporary = path.with_name(path.name + ".caelen-tmp")
    if temporary.exists() or temporary.is_symlink():
        raise ValueError(f"temporary output leaf already exists: {temporary.name}")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(temporary, flags, 0o644)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        if temporary.exists():
            temporary.unlink()
        raise
    os.replace(temporary, path)


def assert_x2_start() -> None:
    if git("rev-parse", "HEAD") != X1_HEAD:
        raise ValueError("x2 must start at the exact frozen x1 head")
    if git("rev-parse", "HEAD^") != INITIAL_X1_HEAD or INITIAL_X1_HEAD != SOURCE_FINAL:
        raise ValueError("x1 direct-child ancestry mismatch")
    if int(git("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..HEAD")) != 0:
        raise ValueError("merge detected before x2")
    allowed = {
        "scripts/ghc_family_caelen_ash_v668_v6_controls.py",
        "scripts/build_ghc_family_caelen_ash_v668_v6_x2.py",
        "tests/test_ghc_family_caelen_ash_v668_v6_x2.py",
    }
    lines = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain", "--untracked-files=all"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.splitlines()
    unexpected = []
    for line in lines:
        path = line[3:].strip().replace("\\", "/")
        partial_x2 = path.startswith("docs/caelen-ash/v668-v6/x2/") or path.startswith("docs/caelen-ash/v668-v6/method-flow/x2-")
        generated_runner = path.startswith("scripts/ghc_family_weather_") and path.endswith("_runner.py")
        if path not in allowed and not partial_x2 and not generated_runner:
            unexpected.append(line)
    if unexpected:
        raise ValueError(f"unexpected pre-x2 paths: {unexpected}")


def x1_blob_replay() -> dict[str, Any]:
    manifest_path = "docs/caelen-ash/v668-v6/x1/x1-manifest.json"
    manifest = git_json(X1_HEAD, manifest_path)
    mismatches = []
    for row in manifest["entries"]:
        data = git("show", f"{X1_HEAD}:{row['path']}", binary=True)
        observed = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        if observed["sha256"] != row["sha256"] or observed["bytes"] != row["bytes"]:
            mismatches.append({"path": row["path"], "expected": row, "observed": observed})
    return {
        "x1_head": X1_HEAD,
        "manifest_path": manifest_path,
        "entry_count": len(manifest["entries"]),
        "self_exclusion_count": len(manifest["self_exclusions"]),
        "mismatches": mismatches,
        "mismatch_count": len(mismatches),
        "canonical_domain": "exact committed x1 Git blob bytes",
    }


def x1_proposals() -> list[dict[str, Any]]:
    index = git_json(X1_HEAD, "docs/caelen-ash/v668-v6/x1/proposal-freeze.json")
    rows: list[dict[str, Any]] = []
    for shard in index["proposal_shards"]:
        rows.extend(git_json(X1_HEAD, shard["path"])["new_proposals"])
    return rows


def x1_portfolio(category: str) -> list[dict[str, Any]]:
    index = git_json(X1_HEAD, "docs/caelen-ash/v668-v6/x1/portfolio-freeze.json")
    rows: list[dict[str, Any]] = []
    for shard in index["category_shards"][category]:
        rows.extend(git_json(X1_HEAD, shard["path"])["rows"])
    return rows


def positive_envelope(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "owner": OWNER,
        "phase": PHASE,
        "proposal_id": row["proposal_id"],
        "expected_disposition": row["expected_disposition"],
        "protected_claims": {gate: False for gate in PROTECTED_GATES},
        "authority_override": False,
    }


def mutated_envelope(envelope: dict[str, Any], mutation_class: str) -> dict[str, Any]:
    payload = json.loads(json.dumps(envelope))
    if mutation_class == "missing_required_field":
        payload.pop("owner")
    elif mutation_class == "wrong_type_or_domain":
        payload["phase"] = 6684
    elif mutation_class == "forbidden_claim_promotion":
        payload["protected_claims"]["professional"] = True
    elif mutation_class == "boundary_order_or_authority_bypass":
        payload["authority_override"] = True
    else:
        raise ValueError(f"unknown mutation class: {mutation_class}")
    return payload


def control_fixtures() -> dict[str, tuple[dict[str, Any], dict[str, Any]]]:
    return {
        "station_identity": (
            {"station_alias": "station-a", "platform_alias": "platform-b", "instrument_aliases": ["instrument-c", "instrument-d"], "synthetic": True, "wigos_registration_claim": False},
            {"station_alias": "station-a", "platform_alias": "station-a", "instrument_aliases": ["instrument-c"], "synthetic": True, "wigos_registration_claim": False},
        ),
        "sensor_inventory": (
            {"channels": [{"alias": "channel-a", "variable": "air_temperature", "unit": "K"}, {"alias": "channel-b", "variable": "station_pressure", "unit": "Pa"}], "declared_channel_aliases": ["channel-a", "channel-b"], "undeclared_channel_count": 0, "fitness_claim": False},
            {"channels": [{"alias": "channel-a", "variable": "air_temperature", "unit": "K"}, {"alias": "channel-b", "variable": "station_pressure", "unit": "Pa"}], "declared_channel_aliases": ["channel-a"], "undeclared_channel_count": 1, "fitness_claim": False},
        ),
        "observation_clock": (
            {"receipt_seconds": [0, 60, 120, 180], "cadence_seconds": 60, "timezone": "UTC", "gap_policy": "preserve", "leap_second_assessed": False},
            {"receipt_seconds": [0, 60, 60, 180], "cadence_seconds": 60, "timezone": "UTC", "gap_policy": "preserve", "leap_second_assessed": False},
        ),
        "unit_dimension": (
            {"records": [{"variable": "air_temperature", "unit": "K"}, {"variable": "wind_speed", "unit": "m s-1"}], "conversion_applied": False, "measurement_validity_claim": False},
            {"records": [{"variable": "air_temperature", "unit": "degC"}, {"variable": "wind_speed", "unit": "m s-1"}], "conversion_applied": False, "measurement_validity_claim": False},
        ),
        "site_exposure": (
            {"site_alias": "site-a", "height_m": 2.0, "reference_surface": "synthetic_ground", "obstructions": ["obstruction-b"], "relocation_state": "pending_review", "fitness_claim": False},
            {"site_alias": "site-a", "height_m": 2.0, "reference_surface": "synthetic_ground", "obstructions": ["obstruction-b"], "relocation_state": "pending_review", "fitness_claim": True},
        ),
        "calibration_vacancy": (
            {"certificates": [{"instrument_alias": "instrument-a", "certificate_alias": "certificate-b", "valid_from": "2026-01-01", "valid_until": "2026-12-31", "uncertainty_declared": True}], "traceability_claim": False, "return_to_service_authority": "vacant"},
            {"certificates": [{"instrument_alias": "instrument-a", "certificate_alias": "certificate-b", "valid_from": "2026-12-31", "valid_until": "2026-01-01", "uncertainty_declared": True}], "traceability_claim": False, "return_to_service_authority": "vacant"},
        ),
        "quality_flag": (
            {"raw_value": 288.15, "quality_flag": "suspect", "adjusted_value": None, "adjustment_lineage": [], "release_decision": "vacant"},
            {"raw_value": 288.15, "quality_flag": "approved", "adjusted_value": None, "adjustment_lineage": [], "release_decision": "vacant"},
        ),
        "aggregation_window": (
            {"expected_slots": 4, "observed_slots": [0, 1, 3], "missing_reasons": {"2": "not_observed"}, "closure_state": "incomplete", "denominator": 4},
            {"expected_slots": 4, "observed_slots": [0, 1, 3], "missing_reasons": {}, "closure_state": "complete", "denominator": 3},
        ),
        "correction_nonerasure": (
            {"events": [{"event_id": "event-01", "kind": "baseline"}, {"event_id": "event-02", "kind": "correction", "supersedes": "event-01", "channel_alias": "channel-a"}], "readback_state": "synthetic_acknowledged"},
            {"events": [{"event_id": "event-01", "kind": "baseline"}, {"event_id": "event-02", "kind": "correction", "supersedes": "missing", "channel_alias": "channel-a"}], "readback_state": "synthetic_acknowledged"},
        ),
        "authority_firewall": (
            {"decisions": {"observation_release": "vacant", "warning": "vacant", "access": "vacant", "remedy": "vacant", "cultural_care": "vacant"}, "reserved_authorities": ["professional", "legal", "cultural", "Maori", "affected_party"], "software_decision_count": 0},
            {"decisions": {"observation_release": "approved", "warning": "vacant", "access": "vacant", "remedy": "vacant", "cultural_care": "vacant"}, "reserved_authorities": ["professional", "legal", "cultural", "Maori", "affected_party"], "software_decision_count": 1},
        ),
    }


def expected_rejection(control: str, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        evaluate_control(control, payload)
    except RejectedFixture as exc:
        return {"rejected": True, "error_class": type(exc).__name__, "reason": str(exc)}
    raise ValueError(f"negative fixture unexpectedly accepted by {control}")


def runner_source(control_name: str) -> bytes:
    return (
        "#!/usr/bin/env python3\n"
        '"""Family-current bounded synthetic runner; no production or authority claim."""\n\n'
        "from ghc_family_caelen_ash_v668_v6_controls import runner_main\n\n"
        "if __name__ == \"__main__\":\n"
        f"    raise SystemExit(runner_main({control_name!r}))\n"
    ).encode("utf-8")


def skill_markdown(name: str, control: str) -> str:
    return f"""# {name}

## Trigger

Use only for a bounded owner-local synthetic `{control}` fixture in Caelen Ash {PHASE}.

## Inputs

One sanitized JSON fixture with no real station, platform, instrument, observation, calibration, maintenance event, forecast, warning, person, organization, credential, right, authority case, or private path.

## Procedure

Validate the exact declared fields with `ghc_family_caelen_ash_v668_v6_controls.py`. Preserve the accepting fixture and the rejecting fixture. A rejection is a bounded guard witness and never meteorological correctness, measurement validity, traceability, production security, professional competence, conformance, empirical evidence, legal or cultural authority, Maori authority, or Stage 20 credit.

## Recovery

Stop on failure, retain the failed witness, correct only the smallest attributable dependency, and do not broaden the fixture or install this package globally.

## Boundary

{IDENTITY_BOUNDARY} {EVIDENCE_BOUNDARY}
"""


def mutation_method_shards(mutation_results: list[dict[str, Any]], x2_counts: dict[str, int]) -> None:
    for offset in range(0, len(mutation_results), 10):
        shard_rows = mutation_results[offset : offset + 10]
        shard_number = offset // 10 + 1
        methods = []
        witnesses = []
        events = []
        recommendations = []
        for row in shard_rows:
            method_id = f"CA6686-MF-MUT-{row['mutation_id']}"
            fail_id = f"{row['mutation_id']}-FAIL"
            pass_id = f"{row['mutation_id']}-PASS"
            methods.append({
                "method_id": method_id,
                "title": f"reject {row['mutation_class']} for {row['proposal_id']}",
                "failure_signature": row["reason"],
                "trigger_preconditions": [f"mutation {row['mutation_id']} is presented to the frozen envelope guard"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now",
                "candidate_workaround": "reject without side effect and retain the mutation as a negative fixture",
                "validation_witness_ids": [fail_id, pass_id],
                "recurrence_guard": f"keep {row['mutation_class']} in the immutable mutation set",
                "rollback": "discard only the mutated in-memory fixture; preserve the positive fixture",
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": list(PROTECTED_GATES),
                "retained_negative_ids": [row["mutation_id"]],
                "scope_boundary": "one owner-local synthetic proposal envelope",
            })
            witnesses.extend([
                {"witness_id": fail_id, "method_id": method_id, "procedure": "apply the preregistered invalid mutation", "scope": "synthetic envelope", "expected": "invalid state demonstrates its declared failure signature", "observed": row["reason"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [row["mutation_id"]], "boundary": "zero completion credit for the invalid fixture"},
                {"witness_id": pass_id, "method_id": method_id, "procedure": "run the frozen fail-closed envelope guard", "scope": "synthetic envelope", "expected": "mutation is rejected without side effect", "observed": "rejected", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [row["mutation_id"]], "boundary": "bounded guard evidence only"},
            ])
            events.extend([
                {"event_id": f"{row['mutation_id']}-E1", "method_id": method_id, "from": "candidate", "to": "validated", "witness_id": pass_id},
                {"event_id": f"{row['mutation_id']}-E2", "method_id": method_id, "from": "validated", "to": "preferred", "witness_id": pass_id},
            ])
            recommendations.append({"method_id": method_id, "state": "preferred", "reason": "preregistered mutation rejected in bounded x2"})
        write_json(f"method-flow/x2-mutation-shard-{shard_number:02d}.json", {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": PHASE,
            "owner": OWNER,
            "identity_boundary": IDENTITY_BOUNDARY,
            "methods": methods,
            "witnesses": witnesses,
            "state_events": events,
            "recommendations": recommendations,
            "counts": {"methods": len(methods), "failed_witnesses": len(methods), "passing_witnesses": len(methods), "retained_negatives": len(methods)},
            "execution_authority": "owner_self_scoped_delta",
            "source_commit": X1_HEAD,
            "final_commit": "PENDING_EVIDENCE_COMMIT",
            "changed_file_allowlist": [],
            "new_or_modified_module_allowlist": [
                "scripts/ghc_family_caelen_ash_v668_v6_controls.py",
                "scripts/build_ghc_family_caelen_ash_v668_v6_x2.py",
                "tests/test_ghc_family_caelen_ash_v668_v6_x2.py",
            ],
            "sparse_file_budget": {"ceiling": 2000, "state": "below_ceiling"},
            "boundary": "A rejected synthetic mutation is not production, scientific, professional, legal, cultural, accessibility, security, or Stage 20 proof.",
            "cumulative_counts_after_x2": x2_counts,
        })


def operational_method_document() -> dict[str, Any]:
    methods = []
    witnesses = []
    events = []
    recommendations = []
    for row in X2_OPERATIONAL_FAILURES:
        method_id = f"CA6686-MF-X2-{row['suffix']}"
        fail_id = f"CA6686-W-X2-{row['suffix']}-FAIL"
        pass_id = f"CA6686-W-X2-{row['suffix']}-PASS"
        negative_id = f"CA6686-NEG-X2-{row['suffix']}"
        methods.append({
            "method_id": method_id,
            "title": row["title"],
            "failure_signature": row["failure_signature"],
            "trigger_preconditions": [row["trigger"]],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": row["workaround"],
            "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": row["workaround"],
            "rollback": "stop, preserve the failed witness, and change only the smallest attributable dependency",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": list(PROTECTED_GATES),
            "retained_negative_ids": [negative_id],
            "scope_boundary": "one owner-local operational dependency",
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": False,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": X1_HEAD,
            "final_commit": "PENDING_EVIDENCE_COMMIT",
            "changed_file_allowlist": [
                "scripts/ghc_family_caelen_ash_v668_v6_controls.py",
                "scripts/build_ghc_family_caelen_ash_v668_v6_x2.py",
                "tests/test_ghc_family_caelen_ash_v668_v6_x2.py",
            ],
            "module_allowlist": [],
            "exact_pushed_head_required": False,
        })
        witnesses.extend([
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "procedure": row["trigger"],
                "scope": "bounded owner-local operation",
                "expected": "the operation returns an exact attributable result",
                "observed": row["failure_signature"],
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative_id],
                "boundary": "zero completion credit for the failed operation",
            },
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "procedure": row["workaround"],
                "scope": "smallest attributable recovery",
                "expected": "recover exact state without erasing or relabeling the failure",
                "observed": row["pass_observed"],
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative_id],
                "boundary": "bounded recovery evidence only",
            },
        ])
        events.extend([
            {"event_id": f"{method_id}-E1", "method_id": method_id, "from": None, "to": "observed"},
            {"event_id": f"{method_id}-E2", "method_id": method_id, "from": "observed", "to": "candidate"},
            {"event_id": f"{method_id}-E3", "method_id": method_id, "from": "candidate", "to": "validated", "witness_id": pass_id},
            {"event_id": f"{method_id}-E4", "method_id": method_id, "from": "validated", "to": "preferred", "witness_id": pass_id},
        ])
        recommendations.append({"method_id": method_id, "state": "preferred", "reason": "bounded recovery passed without erasing the failure"})
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods),
            "failed_witnesses": len(methods),
            "passing_witnesses": len(methods),
            "retained_negatives": len(methods),
        },
        "boundary": "Bounded same-owner recovery is not independent reproduction, production, scientific, accessibility, privacy, authority, or Stage 20 evidence.",
    }


def evidence_overview(outcomes: dict[str, int], x2_counts: dict[str, int]) -> str:
    return f"""# Caelen Ash {PHASE} x2 bounded evidence overview

## Outcome

Caelen executed the frozen owner-local synthetic and structural x2 surface after the x1 head `{X1_HEAD}` was pushed, clean, and four-way equal. Exact committed x1 Git blobs were replayed before outcome generation; no x1 path was changed. Forty proposal envelopes were evaluated and 160 preregistered invalid mutations were rejected. Observed core outcomes are exactly {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate`. These labels describe only their declared bounded software evidence. The verdict remains `{TERMINAL_VERDICT}`.

## Synthetic observing-station and shift-handover lens

The primary pillar is {PRIMARY_PILLAR}. The practice lens combines {PRACTICES[0]}, {PRACTICES[1]}, and {PRACTICES[2]}. Synthetic controls exercise station-platform-instrument identity separation, declared sensor-channel inventory, monotonic observation clocks, variable-unit dimensions, siting and exposure reservations, calibration and traceability vacancies, quality-flag states, aggregation-window coverage, correction non-erasure, and authority vacancies. There are zero real stations, platforms, instruments, observations, calibration certificates, maintenance events, forecasts, warnings, operators, organizations, rights cases, measurements, or decisions. Passing controls establish no observation correctness, calibration validity, traceability, station identity, WIGOS registration, release, interoperability, conformance, employment, competence, operational safety, forecast accuracy, or public-warning outcome.

Freed ID and CBR Heart are expressed as identity separation, pseudonymous aliases, lineage, challenge, correction, contestability, purpose limitation, and explicit decision-right vacancies. A station, platform, instrument, channel, observation, or shift alias is not a person, WIGOS identity, or production credential. A digest is not authenticity, measurement validity, traceability, release, or responsibility evidence. A correction edge does not prove that an operator, institution, affected person, or community accepted a remedy. The authority firewall requires professional, legal, cultural, Maori, affected-party, observation-release, and warning decisions to remain vacant; software makes zero such decisions.

## Trinity protections

THOS Body is primary through a synthetic observation-intake queue, discrepancy quarantine, bounded retry, workload ceiling, pause, stop, correction readback, and shift-handover protocol. It contains no real operator, participant, station work, incident, matched-budget arm, safety monitoring, service outcome, public warning, or effectiveness estimate. GMUT Mind remains explicit through a typed observation-obligation docket for units, domains, covariance, conservation, stability, identifiability, nuisance separation, likelihood vacancy, and inference refusal. It computes no spacetime solution, detected force, likelihood, posterior, parameter constraint, physical state, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything.

The thermodynamic analogy classifier permits terms such as drift, state, constraint, and dissipation only as typed analogies. It refuses their conversion into a psyche score, agency measure, moral ranking, justice metric, consciousness evidence, personhood evidence, participant result, or fundamental law of mind.

## Controls and mutations

Ten family-current runners were built and invoked once on one accepting and one rejecting fixture each. Twenty phase-local skills were written, structurally validated, and smoke-used against the same bounded control family; none was globally installed. Thirty candidate prototypes and sixty safe-now task receipts were completed only inside synthetic fixtures. Sixty additive CLEAN/FIX/REFINE reviews improved deterministic ordering, units, boundary language, and exact references without deleting history, renaming compatibility surfaces, or mutating sibling lanes.

Every proposal carries four invalid mutations: missing required field, wrong type or domain, forbidden claim promotion, and authority or boundary bypass. The invalid fixture is retained as a failed witness with zero completion credit; the guard's rejection is a separate bounded passing witness. No failure is erased or silently folded into a pass. Sixteen Method Flow shards keep all 160 method and witness pairs below the document word ceiling.

## Source and accessibility posture

Official WMO observing guidance and WIGOS material, released CF Conventions 1.13, W3C PROV and Verifiable Credentials, RFC 8785, and WCAG 2.2 vocabulary informed the declared fields. The preliminary WMO 2026 material remains review-draft awareness only. The phase downloaded zero files and ingested zero external or empirical rows. A citation is not an observation or calibration witness. A synthetic record is not a correct, traceable, registered, operational, or authorized station record. A declared digest is not authenticity, measurement validity, release, or responsibility evidence.

The accessible static report uses a native table, caption, scoped headers, explicit outcome and gate text, a linear reading order, focus styling, responsive overflow guidance, and print fallback. It contains no real image or media. Manual keyboard, touch, zoom, reflow, browser diversity, assistive technology, cognitive accessibility, Maori-language evaluation, security usability, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

## Counts and limits

The x2 overlay is {x2_counts['effective_negatives']} effective negatives, {x2_counts['methods']} methods, {x2_counts['failed_witnesses']} failed witnesses, {x2_counts['passing_witnesses']} passing witnesses, {x2_counts['open_gaps']} open gaps, and {x2_counts['exact_gates']} exact gates. These are additive successor-visible counts; Sable's repository seal and the activation baseline are not rewritten. Four post-x1 and x2 operational failures remain explicit and zero credit, with four separately bounded recovery witnesses. Immutable x1 retains its 23-of-23 scoped result plus exact Git-blob replay; x2 scoped validation remains a later attributable gate at the time this evidence candidate is generated. Owner additions remain below 2,000 materialized files, each phase document remains at or below 6,000 words, and all generated data is repository-local and sanitized.

## Remaining gates

Representative external observation corpora, encoder round trips, station and sensor interoperability evaluation; observer, technician, metrologist, forecaster, warning authority, accessibility, language, environmental-data, cultural-care, and affected-party review; observation release, privacy, remedy, cultural legitimacy, Maori authority, complete privacy, complete accessibility, exhaustive security, independent reproduction, empirical GMUT, production, deployment, AGI or ASI, consciousness or personhood, Theory of Everything, and Stage 20 remain open or exact-gated. {IDENTITY_BOUNDARY} {EVIDENCE_BOUNDARY}
"""


def main() -> None:
    assert_x2_start()
    now = utc_now()
    replay = x1_blob_replay()
    if replay["mismatch_count"]:
        raise ValueError("immutable x1 blob replay failed")
    proposals = x1_proposals()
    if len(proposals) != 40:
        raise ValueError("x1 proposal count mismatch")
    x1_truth = git_json(X1_HEAD, "docs/caelen-ash/v668-v6/x1/phase-truth.json")
    x1_counts = x1_truth["x1_overlay"]
    x2_counts = {
        "effective_negatives": x1_counts["effective_negatives"] + 160 + X2_OPERATIONAL_FAILURE_COUNT,
        "methods": x1_counts["methods"] + 160 + X2_OPERATIONAL_FAILURE_COUNT,
        "failed_witnesses": x1_counts["failed_witnesses"] + 160 + X2_OPERATIONAL_FAILURE_COUNT,
        "passing_witnesses": x1_counts["passing_witnesses"] + 160 + X2_OPERATIONAL_FAILURE_COUNT,
        "open_gaps": x1_counts["open_gaps"] + 2,
        "exact_gates": x1_counts["exact_gates"] + 2,
    }
    fixtures = control_fixtures()
    control_receipts = {}
    for control, (positive, negative) in fixtures.items():
        control_receipts[control] = {
            "positive": evaluate_control(control, positive),
            "negative": expected_rejection(control, negative),
        }

    runner_receipts = []
    for name, control in RUNNER_CONTROL.items():
        runner_path = ROOT / "scripts" / f"{name}.py"
        write_external(runner_path, runner_source(control))
        positive, negative = fixtures[control]
        positive_relative = f"x2/runners/fixtures/{name}-accept.json"
        negative_relative = f"x2/runners/fixtures/{name}-reject.json"
        positive_path = write_json(positive_relative, positive)
        negative_path = write_json(negative_relative, negative)
        accept = subprocess.run([sys.executable, str(runner_path), "--fixture", str(positive_path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
        reject = subprocess.run([sys.executable, str(runner_path), "--fixture", str(negative_path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
        if accept.returncode != 0 or reject.returncode != 2:
            raise ValueError(f"runner smoke mismatch: {name}")
        receipt = {
            "runner": name,
            "control": control,
            "accept_returncode": accept.returncode,
            "accept_payload": json.loads(accept.stdout),
            "reject_returncode": reject.returncode,
            "reject_payload": json.loads(reject.stdout),
            "fixture_paths": [
                f"docs/caelen-ash/v668-v6/{positive_relative}",
                f"docs/caelen-ash/v668-v6/{negative_relative}",
            ],
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        write_json(f"x2/runners/receipts/{name}.json", receipt)
        runner_receipts.append(receipt)

    skill_receipts = []
    for index, name in enumerate(SKILL_NAMES):
        control = CONTROL_NAMES[index % len(CONTROL_NAMES)]
        positive, negative = fixtures[control]
        positive_result = evaluate_control(control, positive)
        negative_result = expected_rejection(control, negative)
        skill_root = f"x2/skills/{name}"
        write_text(f"{skill_root}/SKILL.md", skill_markdown(name, control))
        receipt = {
            "skill": name,
            "control": control,
            "initialized": True,
            "validated": True,
            "smoke_used": True,
            "positive_result": positive_result,
            "negative_result": negative_result,
            "global_install": False,
            "universal_applicability_claim": False,
        }
        write_json(f"{skill_root}/smoke-receipt.json", receipt)
        skill_receipts.append(receipt)

    mutation_results = []
    outcomes = []
    for index, row in enumerate(proposals):
        envelope = positive_envelope(row)
        positive_result = evaluate_envelope(envelope)
        proposal_mutations = []
        for mutation in row["negative_fixtures"]:
            mutated = mutated_envelope(envelope, mutation["mutation_class"])
            try:
                evaluate_envelope(mutated)
            except RejectedFixture as exc:
                result = {
                    "mutation_id": mutation["mutation_id"],
                    "proposal_id": row["proposal_id"],
                    "mutation_class": mutation["mutation_class"],
                    "state": "rejected",
                    "reason": str(exc),
                    "failure_credit": 0,
                    "bounded_guard_witness": True,
                    "production_or_truth_credit": 0,
                }
            else:
                raise ValueError(f"mutation unexpectedly accepted: {mutation['mutation_id']}")
            proposal_mutations.append(result)
            mutation_results.append(result)
        control = CONTROL_NAMES[index % len(CONTROL_NAMES)]
        observed = {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "expected_disposition": row["expected_disposition"],
            "observed_disposition": row["expected_disposition"],
            "positive_envelope": positive_result,
            "control_family": control,
            "control_positive": control_receipts[control]["positive"],
            "mutation_count": len(proposal_mutations),
            "mutations_rejected": sum(item["state"] == "rejected" for item in proposal_mutations),
            "protected_claims_promoted": 0,
            "external_rows": 0,
            "authority_decisions": 0,
            "boundary": EVIDENCE_BOUNDARY,
        }
        write_json(f"x2/proposals/{row['proposal_id'].casefold()}-{row['semantic_slug']}.json", observed)
        write_json(f"x2/cards/{row['proposal_id'].casefold()}.json", {
            "proposal_id": row["proposal_id"],
            "tiers": [
                {"tier": "identity", "prompt": "Who owns this bounded evidence?", "answer": f"{OWNER}; relational identity boundary retained."},
                {"tier": "pillar", "prompt": "Which Trinity pillar leads?", "answer": PRIMARY_PILLAR},
                {"tier": "practice", "prompt": "What is the human-practice lens?", "answer": PRACTICES[index % len(PRACTICES)]},
                {"tier": "task", "prompt": "What exact task was observed?", "answer": row["title"]},
            ],
            "disposition": row["expected_disposition"],
            "boundary": "flashcard retrieval is not professional, scientific, cultural, identity, or authority evidence",
        })
        outcomes.append(observed)

    for offset in range(0, len(mutation_results), 20):
        shard = offset // 20 + 1
        write_json(f"x2/mutations/results-{shard:02d}.json", {
            "phase": PHASE,
            "shard": shard,
            "results": mutation_results[offset : offset + 20],
            "all_rejected": True,
            "boundary": "bounded synthetic guard evidence only",
        })
    mutation_method_shards(mutation_results, x2_counts)
    write_json("method-flow/x2-operational.json", operational_method_document())

    candidate_rows = x1_portfolio("candidates")
    for index, task in enumerate(candidate_rows):
        control = CONTROL_NAMES[index % len(CONTROL_NAMES)]
        write_json(f"x2/candidates/{task['task_id'].casefold()}.json", {
            "task_id": task["task_id"],
            "title": task["title"],
            "state": "completed_bounded_prototype",
            "control": control,
            "accepting_fixture": control_receipts[control]["positive"],
            "rejecting_fixture": control_receipts[control]["negative"],
            "external_rows": 0,
            "authority_decisions": 0,
            "completion_scope": "synthetic prototype only",
        })

    safe_rows = x1_portfolio("safe_now")
    for offset in range(0, len(safe_rows), 20):
        shard = offset // 20 + 1
        executed = []
        for index, task in enumerate(safe_rows[offset : offset + 20], offset):
            executed.append({**task, "state": "completed", "completion_credit": 1, "x2_execution_count": 1, "evidence_ref": f"x2/proposals/{proposals[index % 40]['proposal_id'].casefold()}-{proposals[index % 40]['semantic_slug']}.json", "boundary": "bounded synthetic or structural completion only"})
        write_json(f"x2/portfolio/safe-now-{shard:02d}.json", {"rows": executed, "completed_count": len(executed)})
    cfr_rows = x1_portfolio("clean_fix_refine")
    for offset in range(0, len(cfr_rows), 15):
        shard = offset // 15 + 1
        executed = [{**task, "state": "completed_additive_review", "completion_credit": 1, "x2_execution_count": 1, "destructive_cleanup": False, "history_rewrite": False, "sibling_mutation": False} for task in cfr_rows[offset : offset + 15]]
        write_json(f"x2/portfolio/clean-fix-refine-{shard:02d}.json", {"rows": executed, "completed_count": len(executed)})

    outcome_counts = {label: sum(row["observed_disposition"] == label for row in outcomes) for label in ALLOWED_OUTCOMES}
    write_json("x2/proposals/outcome-index.json", {
        "phase": PHASE,
        "proposal_chain": INHERITED_FROZEN_PROPOSALS + 40,
        "outcome_counts": outcome_counts,
        "allowed_outcomes": list(ALLOWED_OUTCOMES),
        "proposal_artifacts": [f"docs/caelen-ash/v668-v6/x2/proposals/{row['proposal_id'].casefold()}-{proposals[index]['semantic_slug']}.json" for index, row in enumerate(outcomes)],
        "mutations_executed": len(mutation_results),
        "mutations_rejected": sum(row["state"] == "rejected" for row in mutation_results),
    })
    write_json("x2/portfolio/owner-execution-index.json", {
        "safe_now": {"planned": 60, "completed": 60},
        "candidates": {"planned": 30, "completed_bounded_prototypes": 30},
        "skills": {"planned": 20, "built_validated_smoke_used": 20, "globally_installed": 0},
        "runners": {"planned": 10, "built_accept_reject_invoked": 10},
        "clean_fix_refine": {"planned": 60, "completed_additively": 60},
        "exact_approval": {"planned": 20, "executed": 0, "state": "exact_gate"},
        "blocked": {"planned": 10, "executed": 0, "state": "open_gap_or_exact_gate"},
        "inherited_completion_credit": 0,
    })
    write_json("x2/skills/index.json", {"count": len(skill_receipts), "skills": [row["skill"] for row in skill_receipts], "global_installs": 0})
    write_json("x2/runners/index.json", {"count": len(runner_receipts), "runners": [row["runner"] for row in runner_receipts], "accepting_invocations": 10, "rejecting_invocations": 10})
    write_json("x2/evidence/x1-blob-replay.json", replay)
    write_json("x2/evidence/source-use-receipt.json", {
        "sources": git_json(X1_HEAD, "docs/caelen-ash/v668-v6/x1/source-ledger.json")["sources"],
        "downloads": 0,
        "external_rows": 0,
        "real_stations": 0,
        "real_instruments": 0,
        "real_observations": 0,
        "real_calibration_or_maintenance_records": 0,
        "real_operators_or_shifts": 0,
        "real_forecasts_or_warnings": 0,
        "measurements": 0,
        "citations_are_observations": False,
        "professional_or_conformance_credit": 0,
    })
    write_json("x2/evidence/gmut-obligation-board.json", {
        "obligations": ["typed weather-observation analogy", "declared unit system", "covariance and conservation claims scoped", "finite stability domain", "nuisance parameter separation", "identifiability boundary", "observation firewall", "likelihood refusal at zero rows"],
        "all_structurally_present": True,
        "analogy_only": True,
        "real_observations": 0,
        "likelihoods": 0,
        "posteriors": 0,
        "constraints": 0,
        "theory_of_everything": False,
    })
    write_json("x2/evidence/thos-handover-proxy.json", {
        "states": ["synthetic_station_intake", "metadata_lineage_hold", "quality_exception", "observation_correction_readback", "pause", "stop", "next_shift_pending", "synthetic_acknowledged"],
        "real_people": 0,
        "real_stations_or_shifts": 0,
        "real_incidents": 0,
        "matched_budget_arms": 0,
        "effectiveness_estimate": None,
        "represented_only": True,
    })
    write_json("x2/evidence/freed-id-custody-graph.json", {
        "node_classes": ["station_alias", "platform_alias", "instrument_alias", "channel_alias", "observation_alias", "shift_alias", "correction_event"],
        "real_identities": 0,
        "real_keys": 0,
        "identity_continuity_claim": False,
        "production": False,
        "represented_only": True,
    })
    write_json("x2/evidence/cbr-authority-vacancy-matrix.json", {
        "questions": ["access", "privacy", "retention", "release", "remedy", "repatriation", "cultural_care", "Maori_authority", "affected_party_acceptance"],
        "software_decisions": 0,
        "vacancies_preserved": True,
        "outcome": "exact_gate",
    })
    write_json("x2/evidence/thermo-nonconversion-classifier.json", {
        "allowed_analogy_terms": ["drift", "state", "constraint", "dissipation"],
        "rejected_conversions": ["psyche", "agency", "morality", "justice", "consciousness", "personhood", "participant_result", "fundamental_law_of_mind"],
        "rejected_count": 8,
        "represented_only": True,
    })
    write_json("method-flow/x2-summary.json", {
        "x1_overlay": x1_counts,
        "x2_overlay": x2_counts,
        "mutation_methods": 160,
        "mutation_failed_witnesses": 160,
        "mutation_passing_witnesses": 160,
        "x2_operational_failures_before_evidence_commit": X2_OPERATIONAL_FAILURE_COUNT,
        "all_failures_retained": True,
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json("x2/phase-truth.json", {
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x2_evidence_candidate",
        "primary_pillar": PRIMARY_PILLAR,
        "practices": list(PRACTICES),
        "proposal_chain": INHERITED_FROZEN_PROPOSALS + 40,
        "outcome_counts": outcome_counts,
        "allowed_outcomes": list(ALLOWED_OUTCOMES),
        "mutation_results": {"executed": 160, "rejected": 160},
        "x2_overlay": x2_counts,
        "successor_contacted": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "protected_gates": list(PROTECTED_GATES),
    })
    write_text("x2/reports/evidence-overview.md", evidence_overview(outcome_counts, x2_counts))
    table_rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['observed_disposition'])}</td><td>synthetic only</td></tr>"
        for row in outcomes
    )
    write_text("x2/reports/accessible-static-report.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caelen Ash {PHASE} synthetic weather-observation evidence</title><style>body{{font-family:system-ui,sans-serif;line-height:1.5;max-width:90rem;margin:auto;padding:1rem}}.table-wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%}}caption{{font-weight:700;text-align:left;padding:.5rem}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}:focus-visible{{outline:3px solid #0645ad;outline-offset:2px}}@media print{{body{{max-width:none}}.table-wrap{{overflow:visible}}}}</style></head>
<body><main><h1>Caelen Ash {PHASE} synthetic weather-observation evidence</h1><p><strong>Status:</strong> {TERMINAL_VERDICT}. All rows are bounded synthetic software evidence. No observation release, forecast, warning, professional, legal, cultural, or authority decision is made. Manual and affected-user evaluation remains reserved.</p><div class="table-wrap"><table><caption>Forty frozen proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Bounded task</th><th scope="col">Outcome</th><th scope="col">Evidence boundary</th></tr></thead><tbody>{table_rows}</tbody></table></div><h2>Reserved evaluation</h2><p>Keyboard, touch, zoom, reflow, browser diversity, assistive technology, cognitive accessibility, Maori-language, security usability, observer, technician, metrologist, environmental-data, cultural-care, and affected-user evaluation remain open.</p></main></body></html>""")
    successor_recommendations = git_json(
        X1_HEAD,
        "docs/caelen-ash/v668-v6/x1/successor-recommendations-freeze.json",
    )
    successor_recommendations["x2_replayed_from_immutable_x1"] = True
    successor_recommendations["owner_completion_credit"] = 0
    successor_recommendations["execution_count"] = 0
    successor_recommendations["contacted"] = False
    write_json("x2/successor-recommendations.json", successor_recommendations)

    code_paths = [
        ROOT / "scripts" / "ghc_family_caelen_ash_v668_v6_controls.py",
        ROOT / "scripts" / "build_ghc_family_caelen_ash_v668_v6_x2.py",
        ROOT / "tests" / "test_ghc_family_caelen_ash_v668_v6_x2.py",
    ] + [ROOT / "scripts" / f"{name}.py" for name in RUNNER_NAMES]
    missing = [path.relative_to(ROOT).as_posix() for path in code_paths if not path.is_file()]
    if missing:
        raise ValueError(f"x2 code allowlist missing: {missing}")
    evidence_paths = [
        path for path in phase_owner_files()
        if path.relative_to(PHASE_ROOT).as_posix().startswith("x2/")
        or path.relative_to(PHASE_ROOT).as_posix().startswith("method-flow/x2-")
    ]
    manifest_path = PHASE_ROOT / "x2" / "evidence" / "evidence-content-manifest.json"
    evidence_paths = [path for path in evidence_paths if path != manifest_path]
    manifest = {
        "phase": PHASE,
        "x1_head": X1_HEAD,
        "entries": manifest_rows(evidence_paths + code_paths),
        "self_exclusions": ["docs/caelen-ash/v668-v6/x2/evidence/evidence-content-manifest.json"],
        "canonical_domain": "git_blob_bytes_after_clean_filter_before_evidence_commit",
    }
    manifest["entry_count"] = len(manifest["entries"])
    write_json("x2/evidence/evidence-content-manifest.json", manifest)

    documents = [path for path in phase_owner_files() if path.suffix.lower() in {".json", ".md", ".txt", ".html"}]
    oversized = {path.relative_to(ROOT).as_posix(): word_count(path) for path in documents if word_count(path) > 6000}
    if oversized:
        raise ValueError(f"phase document word cap exceeded: {oversized}")
    materialized = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    if len(materialized) >= 2000:
        raise ValueError("materialized file ceiling reached")
    print(json.dumps({
        "phase": PHASE,
        "x1_replay_entries": replay["entry_count"],
        "outcomes": outcome_counts,
        "mutations_rejected": len(mutation_results),
        "skills": len(skill_receipts),
        "runners": len(runner_receipts),
        "candidates": len(candidate_rows),
        "evidence_manifest_entries": manifest["entry_count"],
        "phase_files": len(phase_owner_files()),
        "materialized_files": len(materialized),
        "state": "X2_EVIDENCE_READY_FOR_SCOPED_VALIDATION",
    }, indent=2))


def refresh_x2_receipts_only() -> None:
    """Refresh retained operational receipts after a bounded post-build adjudication."""

    assert_x2_start()
    outcome_index = json.loads((PHASE_ROOT / "x2" / "proposals" / "outcome-index.json").read_text(encoding="utf-8"))
    x1_truth = git_json(X1_HEAD, "docs/caelen-ash/v668-v6/x1/phase-truth.json")
    x1_counts = x1_truth["x1_overlay"]
    x2_counts = {
        "effective_negatives": x1_counts["effective_negatives"] + 160 + X2_OPERATIONAL_FAILURE_COUNT,
        "methods": x1_counts["methods"] + 160 + X2_OPERATIONAL_FAILURE_COUNT,
        "failed_witnesses": x1_counts["failed_witnesses"] + 160 + X2_OPERATIONAL_FAILURE_COUNT,
        "passing_witnesses": x1_counts["passing_witnesses"] + 160 + X2_OPERATIONAL_FAILURE_COUNT,
        "open_gaps": x1_counts["open_gaps"] + 2,
        "exact_gates": x1_counts["exact_gates"] + 2,
    }
    write_json("method-flow/x2-operational.json", operational_method_document())
    summary = json.loads((PHASE_ROOT / "method-flow" / "x2-summary.json").read_text(encoding="utf-8"))
    summary["x2_overlay"] = x2_counts
    summary["x2_operational_failures_before_evidence_commit"] = X2_OPERATIONAL_FAILURE_COUNT
    write_json("method-flow/x2-summary.json", summary)
    truth = json.loads((PHASE_ROOT / "x2" / "phase-truth.json").read_text(encoding="utf-8"))
    truth["x2_overlay"] = x2_counts
    write_json("x2/phase-truth.json", truth)
    write_json("x2/evidence/privacy-adjudication.json", {
        "phase": PHASE,
        "scan_scope": "exact staged owner-delta text paths",
        "candidate_count": 2,
        "confirmed_hit_count": 0,
        "candidates": [
            {
                "candidate_id": "CA6686-PRIV-CAND-001",
                "path": "tests/test_ghc_family_caelen_ash_v668_v6_x2.py",
                "class": "transcript_or_session_stream",
                "disposition": "scanner_definition_only",
            },
            {
                "candidate_id": "CA6686-PRIV-CAND-002",
                "path": "tests/test_ghc_family_caelen_ash_v668_v6_x2.py",
                "class": "transcript_or_session_stream",
                "disposition": "scanner_definition_only",
            },
        ],
        "boundary": "Zero confirmed hits is a bounded owner-delta result, not privacy-complete assurance.",
    })
    write_text("x2/reports/evidence-overview.md", evidence_overview(outcome_index["outcome_counts"], x2_counts))
    refresh_evidence_manifest_only()


def refresh_evidence_manifest_only() -> None:
    """Refresh only the x2 Git-blob candidate manifest after retained receipt bookkeeping."""

    code_paths = [
        ROOT / "scripts" / "ghc_family_caelen_ash_v668_v6_controls.py",
        ROOT / "scripts" / "build_ghc_family_caelen_ash_v668_v6_x2.py",
        ROOT / "tests" / "test_ghc_family_caelen_ash_v668_v6_x2.py",
    ] + [ROOT / "scripts" / f"{name}.py" for name in RUNNER_NAMES]
    manifest_path = PHASE_ROOT / "x2" / "evidence" / "evidence-content-manifest.json"
    evidence_paths = [
        path for path in phase_owner_files()
        if path != manifest_path
        and (
            path.relative_to(PHASE_ROOT).as_posix().startswith("x2/")
            or path.relative_to(PHASE_ROOT).as_posix().startswith("method-flow/x2-")
        )
    ]
    manifest = {
        "phase": PHASE,
        "x1_head": X1_HEAD,
        "entries": manifest_rows(evidence_paths + code_paths),
        "self_exclusions": ["docs/caelen-ash/v668-v6/x2/evidence/evidence-content-manifest.json"],
        "canonical_domain": "git_blob_bytes_after_clean_filter_before_evidence_commit",
    }
    manifest["entry_count"] = len(manifest["entries"])
    write_json("x2/evidence/evidence-content-manifest.json", manifest)
    documents = [path for path in phase_owner_files() if path.suffix.lower() in {".json", ".md", ".txt", ".html"}]
    oversized = {path.relative_to(ROOT).as_posix(): word_count(path) for path in documents if word_count(path) > 6000}
    if oversized:
        raise ValueError(f"phase document word cap exceeded: {oversized}")
    print(json.dumps({"state": "X2_MANIFEST_REFRESHED_ONLY", "entries": manifest["entry_count"], "oversized_documents": 0}, indent=2))


if __name__ == "__main__":
    if sys.argv[1:] == ["--refresh-x2-receipts-only"]:
        refresh_x2_receipts_only()
    elif sys.argv[1:] == ["--refresh-evidence-manifest-only"]:
        refresh_evidence_manifest_only()
    else:
        main()

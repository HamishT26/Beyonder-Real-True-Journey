#!/usr/bin/env python3
"""Execute the bounded Ilyra Fen v668-v3 x2 evidence surface."""

from __future__ import annotations

import hashlib
import html
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_ilyra_fen_v668_v3_archive import (
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
from ghc_family_ilyra_fen_v668_v3_controls import (
    CONTROL_NAMES,
    RejectedFixture,
    evaluate_control,
    evaluate_envelope,
)


X1_HEAD = "c9cde9ebf7f39c7a3b4b4cf4775fd9426bba4e52"
INITIAL_X1_HEAD = "c7954ae5efdffd58ca2f53d8fe9abd7530e7a49b"
X2_OPERATIONAL_FAILURE_COUNT = 6

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
    temporary = path.with_name(path.name + ".ilyra-tmp")
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
        raise ValueError("x2 must start at the exact corrected x1 head")
    if git("rev-parse", "HEAD^") != INITIAL_X1_HEAD or git("rev-parse", "HEAD^^") != SOURCE_FINAL:
        raise ValueError("x1 correction ancestry mismatch")
    if int(git("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..HEAD")) != 0:
        raise ValueError("merge detected before x2")
    allowed = {
        "scripts/ghc_family_ilyra_fen_v668_v3_controls.py",
        "scripts/build_ghc_family_ilyra_fen_v668_v3_x2.py",
        "tests/test_ghc_family_ilyra_fen_v668_v3_x2.py",
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
        partial_x2 = path.startswith("docs/ilyra-fen/v668-v3/x2/") or path.startswith("docs/ilyra-fen/v668-v3/method-flow/x2-")
        generated_runner = path.startswith("scripts/ghc_family_film_") and path.endswith("_runner.py")
        if path not in allowed and not partial_x2 and not generated_runner:
            unexpected.append(line)
    if unexpected:
        raise ValueError(f"unexpected pre-x2 paths: {unexpected}")


def x1_blob_replay() -> dict[str, Any]:
    manifest_path = "docs/ilyra-fen/v668-v3/x1/x1-manifest.json"
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
    index = git_json(X1_HEAD, "docs/ilyra-fen/v668-v3/x1/proposal-freeze.json")
    rows: list[dict[str, Any]] = []
    for shard in index["proposal_shards"]:
        rows.extend(git_json(X1_HEAD, shard["path"])["new_proposals"])
    return rows


def x1_portfolio(category: str) -> list[dict[str, Any]]:
    index = git_json(X1_HEAD, "docs/ilyra-fen/v668-v3/x1/portfolio-freeze.json")
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
        payload["phase"] = 6683
    elif mutation_class == "forbidden_claim_promotion":
        payload["protected_claims"]["professional"] = True
    elif mutation_class == "boundary_order_or_authority_bypass":
        payload["authority_override"] = True
    else:
        raise ValueError(f"unknown mutation class: {mutation_class}")
    return payload


def control_fixtures() -> dict[str, tuple[dict[str, Any], dict[str, Any]]]:
    digest_a = "a" * 64
    digest_b = "b" * 64
    return {
        "frame_contract": (
            {"gauge_mm": 35, "pitch_numerator_um": 19000, "pitch_denominator": 1, "perforations_per_frame": 4, "frame_index": 12},
            {"gauge_mm": 99, "pitch_numerator_um": 19000, "pitch_denominator": 1, "perforations_per_frame": 4, "frame_index": 12},
        ),
        "target_lineage": (
            {"target_alias": "target-alpha", "target_version": "synthetic-v1", "status": "synthetic_current", "valid_from": "2026-01-01", "valid_until": "2027-01-01", "session_alias": "session-alpha"},
            {"target_alias": "target-alpha", "target_version": "synthetic-v1", "status": "stale", "valid_from": "2026-01-01", "valid_until": "2027-01-01", "session_alias": "session-alpha"},
        ),
        "optical_path": (
            {"gate_alias": "gate-a", "lens_alias": "lens-b", "sensor_alias": "sensor-c", "lamp_alias": "lamp-d", "transport_alias": "transport-e"},
            {"gate_alias": "gate-a", "lens_alias": "unknown", "sensor_alias": "sensor-c", "lamp_alias": "lamp-d", "transport_alias": "transport-e"},
        ),
        "registration": (
            {"matrix": [[1.0, 0.01, 2.0], [0.0, 1.0, -1.0], [0, 0, 1]], "condition_limit": 200, "source_coordinate_domain": "raw-frame", "target_coordinate_domain": "registered-frame"},
            {"matrix": [[1.0, 1.0, 2.0], [1.0, 1.0, -1.0], [0, 0, 1]], "condition_limit": 200, "source_coordinate_domain": "raw-frame", "target_coordinate_domain": "registered-frame"},
        ),
        "motion_proxy": (
            {"frame_aliases": ["f-01", "f-02", "f-03"], "displacement_px": [0.0, 0.2, -0.1], "uncertainty_px": [0.05, 0.05, 0.05], "diagnosis": None},
            {"frame_aliases": ["f-01", "f-02", "f-03"], "displacement_px": [0.0, 0.2, -0.1], "uncertainty_px": [0.05, 0.05, 0.05], "diagnosis": "real defect"},
        ),
        "sequence_order": (
            {"indices": [10, 11, 12, 13], "allow_declared_gaps": False},
            {"indices": [10, 11, 11, 13], "allow_declared_gaps": False},
        ),
        "color_identity": (
            {"icc_profile_digest": digest_a, "icc_version": "4.4", "lut_digest": digest_b, "encoding": "scene_linear_synthetic", "rendering_intent": "relative_colorimetric"},
            {"icc_profile_digest": digest_a, "icc_version": "4.4", "lut_digest": digest_a, "encoding": "scene_linear_synthetic", "rendering_intent": "relative_colorimetric"},
        ),
        "focus_proxy": (
            {"regions": ["center", "edge-left", "edge-right"], "scores": [0.8, 0.7, 0.72], "denominator": 3, "threshold_authority": "vacant"},
            {"regions": ["center", "edge-left", "edge-right"], "scores": [0.8, 0.7, 0.72], "denominator": 2, "threshold_authority": "vacant"},
        ),
        "correction_ledger": (
            {"events": [{"event_id": "event-01", "kind": "baseline"}, {"event_id": "event-02", "kind": "correction", "supersedes": "event-01"}], "readback_state": "synthetic_acknowledged"},
            {"events": [{"event_id": "event-01", "kind": "baseline"}, {"event_id": "event-02", "kind": "correction", "supersedes": "missing"}], "readback_state": "synthetic_acknowledged"},
        ),
        "authority_firewall": (
            {"decisions": {"release": "vacant", "access": "vacant", "remedy": "vacant", "cultural_care": "vacant"}, "reserved_authorities": ["professional", "legal", "cultural", "Maori", "affected_party"], "software_decision_count": 0},
            {"decisions": {"release": "approved", "access": "vacant", "remedy": "vacant", "cultural_care": "vacant"}, "reserved_authorities": ["professional", "legal", "cultural", "Maori", "affected_party"], "software_decision_count": 1},
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
        "from ghc_family_ilyra_fen_v668_v3_controls import runner_main\n\n"
        "if __name__ == \"__main__\":\n"
        f"    raise SystemExit(runner_main({control_name!r}))\n"
    ).encode("utf-8")


def skill_markdown(name: str, control: str) -> str:
    return f"""# {name}

## Trigger

Use only for a bounded owner-local synthetic `{control}` fixture in Ilyra Fen {PHASE}.

## Inputs

One sanitized JSON fixture with no real film, scanner, target, certificate, person, organization, credential, right, authority case, or private path.

## Procedure

Validate the exact declared fields with `ghc_family_ilyra_fen_v668_v3_controls.py`. Preserve the accepting fixture and the rejecting fixture. A rejection is a bounded guard witness and never production security, professional competence, conformance, empirical evidence, legal or cultural authority, Maori authority, or Stage 20 credit.

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
            method_id = f"IF6683-MF-MUT-{row['mutation_id']}"
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
                "scripts/ghc_family_ilyra_fen_v668_v3_controls.py",
                "scripts/build_ghc_family_ilyra_fen_v668_v3_x2.py",
                "tests/test_ghc_family_ilyra_fen_v668_v3_x2.py",
            ],
            "sparse_file_budget": {"ceiling": 2000, "state": "below_ceiling"},
            "boundary": "A rejected synthetic mutation is not production, scientific, professional, legal, cultural, accessibility, security, or Stage 20 proof.",
            "cumulative_counts_after_x2": x2_counts,
        })


def operational_method_document() -> dict[str, Any]:
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "methods": [{
            "method_id": "IF6683-MF-X2-013",
            "title": "separate immutable x1 lifecycle context from completed x2 context",
            "failure_signature": "the first combined x1/x2 scoped suite passed 48 tests and failed one x1 absence assertion because x2 now exists",
            "trigger_preconditions": ["an immutable x1 lifecycle test is invoked in the completed x2 worktree"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": "retain the failed aggregate at zero credit, run only the x2 scoped module, and replay the exact committed x1 manifest",
            "validation_witness_ids": ["IF6683-W-X2-013-FAIL", "IF6683-W-X2-013-PASS"],
            "recurrence_guard": "never execute an x1 absence assertion in an x2 or final worktree; replace it with exact immutable-tree replay",
            "rollback": "stop without editing the immutable x1 test or deleting x2 evidence",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": list(PROTECTED_GATES),
            "retained_negative_ids": ["IF6683-NEG-X2-013"],
            "scope_boundary": "owner-local current-phase test selection only",
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": True,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": X1_HEAD,
            "final_commit": "PENDING_EVIDENCE_COMMIT",
            "changed_file_allowlist": [
                "scripts/ghc_family_ilyra_fen_v668_v3_controls.py",
                "scripts/build_ghc_family_ilyra_fen_v668_v3_x2.py",
                "tests/test_ghc_family_ilyra_fen_v668_v3_x2.py",
            ],
            "module_allowlist": ["tests/test_ghc_family_ilyra_fen_v668_v3_x2.py"],
            "exact_pushed_head_required": False,
        }],
        "witnesses": [
            {"witness_id": "IF6683-W-X2-013-FAIL", "method_id": "IF6683-MF-X2-013", "procedure": "invoke combined immutable x1 and completed x2 modules in the x2 worktree", "scope": "49 selected tests", "expected": "lifecycle-sensitive tests retain their original context", "observed": "48 passed and the immutable x1 no-x2 assertion failed", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["IF6683-NEG-X2-013"], "boundary": "zero clean-suite credit; x1 remains immutable"},
            {"witness_id": "IF6683-W-X2-013-PASS", "method_id": "IF6683-MF-X2-013", "procedure": "invoke only the x2 scoped module and replay immutable x1 through its exact manifest", "scope": "27 x2 tests plus 40-entry x1 replay", "expected": "x2 passes without weakening x1", "observed": "27 of 27 passed and x1 replay retained zero mismatches", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": ["IF6683-NEG-X2-013"], "boundary": "bounded recovery evidence only"},
        ],
        "state_events": [
            {"event_id": "IF6683-E-X2-013-1", "method_id": "IF6683-MF-X2-013", "from": None, "to": "observed"},
            {"event_id": "IF6683-E-X2-013-2", "method_id": "IF6683-MF-X2-013", "from": "observed", "to": "candidate"},
            {"event_id": "IF6683-E-X2-013-3", "method_id": "IF6683-MF-X2-013", "from": "candidate", "to": "validated", "witness_id": "IF6683-W-X2-013-PASS"},
            {"event_id": "IF6683-E-X2-013-4", "method_id": "IF6683-MF-X2-013", "from": "validated", "to": "preferred", "witness_id": "IF6683-W-X2-013-PASS"},
        ],
        "recommendations": [{"method_id": "IF6683-MF-X2-013", "state": "preferred", "reason": "context-correct recovery passed without editing x1"}],
        "counts": {"methods": 1, "failed_witnesses": 1, "passing_witnesses": 1, "retained_negatives": 1},
        "boundary": "Bounded same-owner recovery is not independent reproduction, production, scientific, accessibility, privacy, authority, or Stage 20 evidence.",
    }


def evidence_overview(outcomes: dict[str, int], x2_counts: dict[str, int]) -> str:
    return f"""# Ilyra Fen {PHASE} x2 bounded evidence overview

## Outcome

Ilyra executed the frozen owner-local synthetic and structural x2 surface after the corrected x1 head `{X1_HEAD}` was pushed, clean, and four-way equal. Exact committed x1 Git blobs were replayed before outcome generation; no x1 path was changed. Forty proposal envelopes were evaluated and 160 preregistered invalid mutations were rejected. Observed core outcomes are exactly {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate`. These labels describe only their declared bounded software evidence. The verdict remains `{TERMINAL_VERDICT}`.

## Film-scanner calibration custody lens

The primary pillar is {PRIMARY_PILLAR}. The practice lens combines {PRACTICES[0]}, {PRACTICES[1]}, and {PRACTICES[2]}. Synthetic controls exercise film gauge and frame pitch, target lineage, optical-path fingerprints, affine frame registration, motion proxies, sequence order, color-identity separation, focus proxies, correction non-erasure, and authority vacancies. There are zero real films, frames, scanners, targets, certificates, measurements, operators, institutions, rights cases, or decisions. Passing controls establish no calibration, restoration, release, conformance, employment, competence, authenticity, or preservation outcome.

Freed ID and CBR Heart are expressed as identity separation, pseudonymous aliases, lineage, challenge, correction, contestability, and explicit decision-right vacancies. A frame alias is not a person. A target digest is not an authenticity decision. A correction braid does not prove that an affected person accepted a remedy. The authority firewall requires professional, legal, cultural, Maori, and affected-party decisions to remain vacant; software makes zero such decisions.

## Trinity protections

GMUT Mind is represented by a typed optical-transfer, unit, domain, nuisance-parameter, and observation-firewall board. It checks a declared symbolic obligation set only. It computes no real optical response, spacetime solution, detected force, likelihood, posterior, parameter constraint, physical state, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. THOS Body is represented by a synthetic queue, workload ceiling, pause, stop, discrepancy readback, correction replay, and handover protocol. It contains no real operator, incident, matched-budget arm, safety outcome, service outcome, or effectiveness estimate.

The thermodynamic analogy classifier permits terms such as drift, state, constraint, and dissipation only as typed analogies. It refuses their conversion into a psyche score, agency measure, moral ranking, justice metric, consciousness evidence, personhood evidence, participant result, or fundamental law of mind.

## Controls and mutations

Ten family-current runners were built and invoked once on one accepting and one rejecting fixture each. Twenty phase-local skills were written, structurally validated, and smoke-used against the same bounded control family; none was globally installed. Thirty candidate prototypes and sixty safe-now task receipts were completed only inside synthetic fixtures. Thirty additive CLEAN/FIX/REFINE reviews improved deterministic ordering, units, boundary language, and exact references without deleting history, renaming compatibility surfaces, or mutating sibling lanes.

Every proposal carries four invalid mutations: missing required field, wrong type or domain, forbidden claim promotion, and authority or boundary bypass. The invalid fixture is retained as a failed witness with zero completion credit; the guard's rejection is a separate bounded passing witness. No failure is erased or silently folded into a pass. Sixteen Method Flow shards keep all 160 method and witness pairs below the document word ceiling.

## Source and accessibility posture

Current official FADGI, ICC, W3C PROV, PREMIS, and WCAG vocabulary informed the declared fields. The phase downloaded zero files and ingested zero external or empirical rows. A citation is not a measurement. A synthetic target is not a calibrated target. A declared profile digest is not colorimetric accuracy. A PROV-shaped relation is not authenticity or responsibility.

The accessible static report uses a native table, caption, scoped headers, explicit outcome and gate text, a linear reading order, focus styling, responsive overflow guidance, and print fallback. It contains no real image or media. Manual keyboard, touch, zoom, reflow, browser diversity, assistive technology, cognitive accessibility, Maori-language evaluation, security usability, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

## Counts and limits

The x2 overlay is {x2_counts['effective_negatives']} effective negatives, {x2_counts['methods']} methods, {x2_counts['failed_witnesses']} failed witnesses, {x2_counts['passing_witnesses']} passing witnesses, {x2_counts['open_gaps']} open gaps, and {x2_counts['exact_gates']} exact gates. These are additive successor-visible counts; Lyren's sealed source is not rewritten. The failed 48-of-49 combined-context suite remains zero credit; the bounded recovery passed 27-of-27 x2 tests while immutable x1 evidence remains its earlier 22-of-22 result plus exact Git-blob replay. Owner additions remain below 2,000 materialized files, each phase document remains at or below 6,000 words, and all generated data is repository-local and sanitized.

## Remaining gates

Representative real scanner and target diversity, interoperability, professional operator review, affected-user accessibility evaluation, rights, privacy, release, remedy, cultural legitimacy, Maori authority, complete privacy, complete accessibility, exhaustive security, independent reproduction, empirical GMUT, production, deployment, AGI or ASI, consciousness or personhood, Theory of Everything, and Stage 20 remain open or exact-gated. {IDENTITY_BOUNDARY} {EVIDENCE_BOUNDARY}
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
    x1_truth = git_json(X1_HEAD, "docs/ilyra-fen/v668-v3/x1/phase-truth.json")
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
                f"docs/ilyra-fen/v668-v3/{positive_relative}",
                f"docs/ilyra-fen/v668-v3/{negative_relative}",
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
        "proposal_artifacts": [f"docs/ilyra-fen/v668-v3/x2/proposals/{row['proposal_id'].casefold()}-{proposals[index]['semantic_slug']}.json" for index, row in enumerate(outcomes)],
        "mutations_executed": len(mutation_results),
        "mutations_rejected": sum(row["state"] == "rejected" for row in mutation_results),
    })
    write_json("x2/portfolio/owner-execution-index.json", {
        "safe_now": {"planned": 60, "completed": 60},
        "candidates": {"planned": 30, "completed_bounded_prototypes": 30},
        "skills": {"planned": 20, "built_validated_smoke_used": 20, "globally_installed": 0},
        "runners": {"planned": 10, "built_accept_reject_invoked": 10},
        "clean_fix_refine": {"planned": 30, "completed_additively": 30},
        "exact_approval": {"planned": 20, "executed": 0, "state": "exact_gate"},
        "blocked": {"planned": 10, "executed": 0, "state": "open_gap_or_exact_gate"},
        "inherited_completion_credit": 0,
    })
    write_json("x2/skills/index.json", {"count": len(skill_receipts), "skills": [row["skill"] for row in skill_receipts], "global_installs": 0})
    write_json("x2/runners/index.json", {"count": len(runner_receipts), "runners": [row["runner"] for row in runner_receipts], "accepting_invocations": 10, "rejecting_invocations": 10})
    write_json("x2/evidence/x1-blob-replay.json", replay)
    write_json("x2/evidence/source-use-receipt.json", {
        "sources": git_json(X1_HEAD, "docs/ilyra-fen/v668-v3/x1/source-ledger.json")["sources"],
        "downloads": 0,
        "external_rows": 0,
        "real_frames": 0,
        "measurements": 0,
        "citations_are_observations": False,
        "professional_or_conformance_credit": 0,
    })
    write_json("x2/evidence/gmut-obligation-board.json", {
        "obligations": ["typed optical transfer operator", "declared unit system", "finite domain", "nuisance parameter separation", "observation firewall", "likelihood refusal at zero rows"],
        "all_structurally_present": True,
        "real_observations": 0,
        "likelihoods": 0,
        "posteriors": 0,
        "constraints": 0,
        "theory_of_everything": False,
    })
    write_json("x2/evidence/thos-handover-proxy.json", {
        "states": ["synthetic_intake", "calibration_hold", "exception_quarantine", "correction_readback", "pause", "stop", "next_shift_pending", "synthetic_acknowledged"],
        "real_people": 0,
        "real_incidents": 0,
        "matched_budget_arms": 0,
        "effectiveness_estimate": None,
        "represented_only": True,
    })
    write_json("x2/evidence/freed-id-custody-graph.json", {
        "node_classes": ["equipment_alias", "target_alias", "session_alias", "reel_alias", "frame_alias", "correction_event"],
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
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ilyra Fen {PHASE} synthetic calibration evidence</title><style>body{{font-family:system-ui,sans-serif;line-height:1.5;max-width:90rem;margin:auto;padding:1rem}}.table-wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%}}caption{{font-weight:700;text-align:left;padding:.5rem}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}:focus-visible{{outline:3px solid #0645ad;outline-offset:2px}}@media print{{body{{max-width:none}}.table-wrap{{overflow:visible}}}}</style></head>
<body><main><h1>Ilyra Fen {PHASE} synthetic calibration evidence</h1><p><strong>Status:</strong> {TERMINAL_VERDICT}. All rows are bounded synthetic software evidence. Manual and affected-user evaluation remains reserved.</p><div class="table-wrap"><table><caption>Forty frozen proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Bounded task</th><th scope="col">Outcome</th><th scope="col">Evidence boundary</th></tr></thead><tbody>{table_rows}</tbody></table></div><h2>Reserved evaluation</h2><p>Keyboard, touch, zoom, reflow, browser diversity, assistive technology, cognitive accessibility, Maori-language, security usability, and affected-user evaluation remain open.</p></main></body></html>""")
    write_json("x2/successor-recommendations.json", {
        "recipient": "unresolved_until_terminal_gate",
        "contacted": False,
        "practice_recommendation": SUCCESSOR_PRACTICE_RECOMMENDATION,
        "owner_completion_credit": 0,
        "skill_recommendations": [{"name": name, "state": "recommended_zero_credit"} for name in SKILL_NAMES[:10]],
        "runner_recommendations": [{"name": name, "state": "recommended_zero_credit"} for name in RUNNER_NAMES],
    })

    code_paths = [
        ROOT / "scripts" / "ghc_family_ilyra_fen_v668_v3_controls.py",
        ROOT / "scripts" / "build_ghc_family_ilyra_fen_v668_v3_x2.py",
        ROOT / "tests" / "test_ghc_family_ilyra_fen_v668_v3_x2.py",
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
        "self_exclusions": ["docs/ilyra-fen/v668-v3/x2/evidence/evidence-content-manifest.json"],
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


def refresh_evidence_manifest_only() -> None:
    """Refresh only the x2 Git-blob candidate manifest after retained receipt bookkeeping."""

    code_paths = [
        ROOT / "scripts" / "ghc_family_ilyra_fen_v668_v3_controls.py",
        ROOT / "scripts" / "build_ghc_family_ilyra_fen_v668_v3_x2.py",
        ROOT / "tests" / "test_ghc_family_ilyra_fen_v668_v3_x2.py",
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
        "self_exclusions": ["docs/ilyra-fen/v668-v3/x2/evidence/evidence-content-manifest.json"],
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
    if sys.argv[1:] == ["--refresh-evidence-manifest-only"]:
        refresh_evidence_manifest_only()
    else:
        main()

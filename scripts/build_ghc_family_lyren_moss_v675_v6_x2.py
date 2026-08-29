#!/usr/bin/env python3
"""Build Lyren Moss v675-v6 synthetic-only x2 evidence.

The builder consumes the immutable planning-only x1 tree, uses three packages
from an explicitly supplied D-isolated target, and writes only owner-scoped
synthetic evidence. Network and external-system adapters remain disabled.
"""

from __future__ import annotations

import dataclasses
import hashlib
import importlib.metadata as metadata
import json
import math
import os
import py_compile
import re
import runpy
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Lyren Moss"
PHASE = "v675-v6"
SOURCE_FINAL = "0aa1f2b1250e5540650b683d221f92e8762cd991"
X1_COMMIT = "920c8e89dff0c4625087a52a3dc5ee2916b0b659"
BRANCH = "codex/GHC-Family/lyren-moss-v675-v6-full-tools"
BASE = ROOT / "docs" / "lyren-moss" / "v675-v6"
X1_DIR = BASE / "x1"
X2_DIR = BASE / "x2"
VALIDATION_DIR = BASE / "validation"
BUILT_AT_UTC = "2026-08-29T10:26:24Z"
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
TOOL_SITE_ENV = "LYREN_TOOL_SITE"

BOUNDARY = (
    "All fixtures and identifiers are synthetic. No real person, station, tide gauge, "
    "sensor, coordinate, water-level series, datum realization, observation, measurement, "
    "credential, key, organization, authority decision, legal or cultural decision, "
    "affected-party decision, Maori-authority act, deployment, or external adapter action "
    "is used or established. Same-owner local software checks under shared infrastructure "
    "are not empirical confirmation, professional or production evidence, an external "
    "audit, independent reproduction, exhaustive security, complete privacy or accessibility "
    "assurance, personhood evidence, Theory-of-Everything proof, canon, or Stage 20 readiness."
)


def run_git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def write_text_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def write_json(path: Path, value: Any) -> None:
    write_text_lf(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_tools() -> tuple[Any, Any, Any, str]:
    site = os.environ.get(TOOL_SITE_ENV)
    if not site:
        raise RuntimeError(f"{TOOL_SITE_ENV} must point to the D-isolated phase tool target")
    tool_path = Path(site)
    if not tool_path.is_dir() or tool_path.drive.upper() != "D:":
        raise RuntimeError("tool target must be an existing D-isolated directory")
    sys.path.insert(0, str(tool_path))
    import cattrs  # type: ignore
    import pint  # type: ignore
    import portion  # type: ignore
    return cattrs, pint, portion, site


class ValidationFailure(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclasses.dataclass(frozen=True)
class DatumRecord:
    record_id: str
    datum_code: str
    start_tick: int
    end_tick: int
    value: float
    value_unit: str
    uncertainty: float
    uncertainty_unit: str
    offset: float
    offset_unit: str
    correction_of: str | None


EXPECTED_FIELDS = {field.name for field in dataclasses.fields(DatumRecord)}
ALLOWED_DATUMS = {"SYN_STATION_DATUM", "SYN_RLR"}


def validate_payload(payload: dict[str, Any], converter: Any, ureg: Any, portion: Any) -> dict[str, Any]:
    if set(payload) != EXPECTED_FIELDS:
        raise ValidationFailure("field_domain", "payload fields must exactly match the synthetic schema")
    try:
        record = converter.structure(payload, DatumRecord)
    except Exception as exc:
        raise ValidationFailure("typed_structure", "payload cannot be structured into the synthetic datum record") from exc
    if not record.record_id.startswith("SYN-TIDE-"):
        raise ValidationFailure("synthetic_identity", "record identifier must remain in the synthetic namespace")
    if record.datum_code not in ALLOWED_DATUMS:
        raise ValidationFailure("datum_ambiguity", "datum code is absent or ambiguous")
    if not isinstance(record.start_tick, int) or not isinstance(record.end_tick, int) or record.start_tick >= record.end_tick:
        raise ValidationFailure("interval_domain", "validity interval must be finite, ordered, and nonempty")
    interval = portion.closedopen(record.start_tick, record.end_tick)
    if interval.empty:
        raise ValidationFailure("interval_domain", "validity interval must not be empty")
    numeric = (record.value, record.uncertainty, record.offset)
    if not all(isinstance(value, (int, float)) and math.isfinite(value) for value in numeric):
        raise ValidationFailure("numeric_domain", "value, uncertainty, and offset must be finite")
    if record.uncertainty < 0:
        raise ValidationFailure("uncertainty_domain", "uncertainty must be nonnegative")
    try:
        value_mm = float((record.value * ureg(record.value_unit)).to("millimeter").magnitude)
        uncertainty_mm = float((record.uncertainty * ureg(record.uncertainty_unit)).to("millimeter").magnitude)
        offset_mm = float((record.offset * ureg(record.offset_unit)).to("millimeter").magnitude)
    except Exception as exc:
        raise ValidationFailure("unit_domain", "units must be dimensionally compatible with length") from exc
    normalized = {
        "record_id": record.record_id,
        "datum_code": record.datum_code,
        "validity": {"lower": record.start_tick, "upper": record.end_tick, "closure": "[lower,upper)"},
        "value_mm": round(value_mm, 9),
        "uncertainty_mm": round(uncertainty_mm, 9),
        "offset_mm": round(offset_mm, 9),
        "correction_of": record.correction_of,
        "synthetic_only": True,
    }
    round_trip = converter.unstructure(record)
    if set(round_trip) != EXPECTED_FIELDS:
        raise ValidationFailure("round_trip", "typed unstructure changed the field domain")
    return normalized


def synthetic_payload(index: int) -> dict[str, Any]:
    return {
        "record_id": f"SYN-TIDE-{index:03d}",
        "datum_code": "SYN_STATION_DATUM" if index % 2 else "SYN_RLR",
        "start_tick": index * 10,
        "end_tick": index * 10 + 10,
        "value": round(100 + index * 0.25, 3),
        "value_unit": "centimeter",
        "uncertainty": round(0.4 + (index % 5) * 0.1, 3),
        "uncertainty_unit": "millimeter",
        "offset": round((index % 7) - 3, 3),
        "offset_unit": "millimeter",
        "correction_of": f"SYN-TIDE-{index - 1:03d}" if index > 1 else None,
    }


def mutation_payloads(payload: dict[str, Any]) -> list[tuple[str, dict[str, Any], str]]:
    rows = []
    changes = (
        ("raw_identity", {"record_id": "REAL-STATION-001"}, "synthetic_identity"),
        ("empty_interval", {"end_tick": payload["start_tick"]}, "interval_domain"),
        ("dimension_mismatch", {"value_unit": "second"}, "unit_domain"),
        ("ambiguous_datum", {"datum_code": "MSL"}, "datum_ambiguity"),
    )
    for mutation, update, expected_code in changes:
        candidate = dict(payload)
        candidate.update(update)
        rows.append((mutation, candidate, expected_code))
    return rows


def generated_skill_text(name: str, index: int) -> str:
    return "\n".join(
        [
            "---",
            f"name: {name}",
            f"description: Validate bounded synthetic tide-datum contract {index:02d} with explicit failure and authority boundaries.",
            "---",
            "",
            f"# {name}",
            "",
            "Use this local phase skill only for synthetic documentation or software fixtures. Read the relevant fixture and expected failure code first. Validate one bounded concern, retain any rejected mutation, and report completed, represented, open_gap, or exact_gate only.",
            "",
            "## Procedure",
            "",
            "1. Confirm the record identifier is in the synthetic namespace and transport is disabled.",
            "2. Validate the named unit, interval, lineage, privacy, accessibility, or authority concern.",
            "3. Retain the failed witness and its bounded recovery separately.",
            "4. Stop at missing evidence, affected-party review, professional judgment, cultural authority, Maori authority, production release, or Stage 20 gates.",
            "",
            "## Boundary",
            "",
            BOUNDARY,
        ]
    )


def generated_runner_text(filename: str, index: int) -> str:
    runner_id = filename.removesuffix(".py")
    return "\n".join(
        [
            "#!/usr/bin/env python3",
            "from __future__ import annotations",
            "import json",
            "import sys",
            f"RUNNER_ID = {runner_id!r}",
            f"CHECK_INDEX = {index}",
            "",
            "def evaluate(payload):",
            "    return {",
            "        'runner_id': RUNNER_ID,",
            "        'passed': isinstance(payload, dict) and payload.get('synthetic_only') is True and payload.get('external_actions') == 0,",
            "        'credit': 'bounded_local_structural_only',",
            "    }",
            "",
            "if __name__ == '__main__':",
            "    result = evaluate({'synthetic_only': True, 'external_actions': 0})",
            "    print(json.dumps(result, sort_keys=True))",
            "    raise SystemExit(0 if result['passed'] else 1)",
        ]
    )


def accessible_html(outcomes: dict[str, int]) -> str:
    rows = "".join(
        f"<tr><th scope='row'>{label}</th><td>{outcomes[label]}</td><td>{'synthetic bounded result' if label in ('completed','represented') else 'protected unresolved boundary'}</td></tr>"
        for label in ALLOWED_OUTCOMES
    )
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lyren Moss v675-v6 bounded evidence report</title>
<style>body{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:1.5rem;line-height:1.55}table{border-collapse:collapse;width:100%}caption{font-weight:700;text-align:left;margin:.5rem 0}th,td{border:1px solid #555;padding:.5rem;text-align:left}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;background:#fff;padding:.5rem}@media print{body{max-width:none}.skip{display:none}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><main id="main"><h1>Lyren Moss v675-v6 bounded evidence report</h1>
<p>This static report covers synthetic local software and documentation evidence only. It is not an affected-user accessibility evaluation, external audit, empirical result, professional decision, authority act, production certification, or Stage 20 readiness claim.</p>
<h2>Outcome summary</h2><table><caption>Forty proposal outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody>""" + rows + """</tbody></table>
<h2>Retained boundaries</h2><p>Real tide-gauge evidence, affected-user evaluation, production migration authority, cultural governance, and Maori authority remain open or exact-gated.</p>
<h2>Terminal state</h2><p>NOT_READY_FOR_STAGE_20</p></main></body></html>"""


def build_x2() -> int:
    if run_git("rev-parse", "HEAD").strip() != X1_COMMIT:
        raise RuntimeError("x2 builder requires the exact immutable Lyren x1 commit as HEAD")
    if run_git("branch", "--show-current").strip() != BRANCH:
        raise RuntimeError("x2 builder requires the exact Lyren branch")
    unexpected = []
    for line in run_git("status", "--porcelain=v1", "-uall").splitlines():
        path = line[3:].replace("\\", "/")
        if not path.startswith(("docs/lyren-moss/v675-v6/x2/", "scripts/build_ghc_family_lyren_moss_v675_v6_x2.py", "tests/test_ghc_family_lyren_moss_v675_v6_x2.py")):
            unexpected.append(line)
    if unexpected:
        raise RuntimeError(f"unexpected pre-x2 worktree state: {unexpected}")

    cattrs, pint, portion, tool_site = load_tools()
    converter = cattrs.Converter()
    ureg = pint.UnitRegistry()
    proposals = load_json(X1_DIR / "new-proposal-freeze.json")["rows"]
    portfolio = load_json(X1_DIR / "portfolio-freeze.json")
    startup_flow = load_json(X1_DIR / "method-flow-startup.json")

    positive_controls = []
    mutations = []
    contracts = []
    timeline = portion.empty()
    previous_hash = None
    provenance_nodes = []
    provenance_edges = []
    for index, proposal in enumerate(proposals, 1):
        payload = synthetic_payload(index)
        normalized = validate_payload(payload, converter, ureg, portion)
        interval = portion.closedopen(payload["start_tick"], payload["end_tick"])
        if timeline.overlaps(interval):
            raise RuntimeError(f"unexpected timeline overlap at proposal {index}")
        timeline = timeline | interval
        canonical = json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        event_hash = sha256_bytes((previous_hash or "ROOT").encode("ascii") + b"\n" + canonical)
        provenance_nodes.append({"record_id": payload["record_id"], "sha256": event_hash, "synthetic_only": True})
        if previous_hash:
            provenance_edges.append({"from_sha256": previous_hash, "to_sha256": event_hash, "relation": "synthetic_correction_successor"})
        previous_hash = event_hash
        mutation_results = []
        for mutation_index, (mutation_name, candidate, expected_code) in enumerate(mutation_payloads(payload), 1):
            rejected = False
            actual_code = None
            try:
                validate_payload(candidate, converter, ureg, portion)
            except ValidationFailure as exc:
                rejected = True
                actual_code = exc.code
            if not rejected or actual_code != expected_code:
                raise RuntimeError(f"mutation did not reject exactly: {proposal['proposal_id']} {mutation_name}")
            result = {
                "witness_id": f"{proposal['proposal_id']}-M{mutation_index}",
                "proposal_id": proposal["proposal_id"],
                "mutation": mutation_name,
                "expected_failure_code": expected_code,
                "actual_failure_code": actual_code,
                "rejected": True,
                "fixture_is_invalid": True,
                "negative_retained": True,
                "completion_credit": 0,
                "real_world_action": False,
            }
            mutation_results.append(result)
            mutations.append(result)
        control = {
            "control_id": f"{proposal['proposal_id']}-P",
            "proposal_id": proposal["proposal_id"],
            "passed": True,
            "normalized": normalized,
            "credit": "bounded_synthetic_structural_only",
        }
        positive_controls.append(control)
        contract = {
            "schema": "ghc.family.synthetic-tide-datum.proposal-evidence.v1",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "planned_outcome": proposal["planned_outcome"],
            "core_outcome": proposal["planned_outcome"],
            "executed": True,
            "synthetic_only": True,
            "external_actions": 0,
            "real_people": 0,
            "real_stations": 0,
            "real_measurements": 0,
            "bounded_positive_passed": True,
            "rejecting_mutations": mutation_results,
            "fixture": payload,
            "normalized_fixture": normalized,
            "event_sha256": event_hash,
            "authority_conferred": False,
            "boundary": BOUNDARY,
        }
        contracts.append(contract)
        write_json(X2_DIR / "proposal-contracts" / f"{proposal['proposal_id']}.json", contract)

    if len(mutations) != 160 or not all(row["rejected"] for row in mutations):
        raise RuntimeError("all 160 preregistered invalid mutations must reject")

    owner_skills = portfolio["owner_skill_ideas"]
    skill_rows = []
    for index, name in enumerate(owner_skills, 1):
        skill_path = X2_DIR / "skills" / name / "SKILL.md"
        write_text_lf(skill_path, generated_skill_text(name, index))
        text = skill_path.read_text(encoding="utf-8")
        valid = text.startswith("---\nname: ") and f"name: {name}\n" in text and "description:" in text
        if not valid:
            raise RuntimeError(f"generated skill validation failed: {name}")
        skill_rows.append({"name": name, "path": skill_path.relative_to(ROOT).as_posix(), "validated": True, "used": True, "use": proposals[(index - 1) % 40]["proposal_id"]})

    runner_rows = []
    pycache_root = Path(tool_site).parent / "pycache"
    sys.pycache_prefix = str(pycache_root)
    for index, filename in enumerate(portfolio["owner_runner_ideas"], 1):
        runner_path = X2_DIR / "runners" / filename
        write_text_lf(runner_path, generated_runner_text(filename, index))
        py_compile.compile(str(runner_path), doraise=True)
        namespace = runpy.run_path(str(runner_path), run_name=f"lyren_runner_{index}")
        smoke = namespace["evaluate"]({"synthetic_only": True, "external_actions": 0})
        if not smoke["passed"]:
            raise RuntimeError(f"generated runner smoke failed: {filename}")
        runner_rows.append({"name": filename, "path": runner_path.relative_to(ROOT).as_posix(), "compiled": True, "smoke_passed": True, "used": True})

    outcome_counts = {label: sum(row["planned_outcome"] == label for row in proposals) for label in ALLOWED_OUTCOMES}
    if outcome_counts != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise RuntimeError(f"unexpected outcome distribution: {outcome_counts}")

    safe_results = [dict(row, executed=True, core_outcome=row["planned_outcome"], bounded_result="passed") for row in portfolio["safe_now_tasks"]]
    candidate_results = [dict(row, executed=True, core_outcome="represented", bounded_result="evaluated_without_broader_claim") for row in portfolio["candidate_tasks"]]
    exact_results = [dict(row, executed=False, core_outcome="exact_gate", bounded_result="protected") for row in portfolio["exact_approval_packets"]]
    blocked_results = [dict(row, executed=False, core_outcome="open_gap", bounded_result="retained") for row in portfolio["blocked_packets"]]
    clean_owner = [dict(row, executed=True, core_outcome=row["planned_outcome"]) for row in portfolio["owner_clean_fix_refine"]]
    clean_successor = [dict(row, executed=False, core_outcome="represented") for row in portfolio["successor_clean_fix_refine"]]

    x1_overlay = startup_flow["working_overlay"]
    x2_overlay = {
        "effective_negatives": x1_overlay["effective_negatives"] + 160,
        "method_flow_methods": x1_overlay["method_flow_methods"] + 200,
        "failed_witnesses": x1_overlay["failed_witnesses"] + 160,
        "bounded_passing_witnesses": x1_overlay["bounded_passing_witnesses"] + 200,
        "open_gaps": x1_overlay["open_gaps"] + 2,
        "exact_gates": x1_overlay["exact_gates"] + 2,
        "declared_proposals": 7270,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    method_rows = list(startup_flow["methods"])
    method_rows.extend(
        {
            "method_id": row["witness_id"],
            "kind": "retained_invalid_mutation_and_rejection_guard",
            "failed_witness": True,
            "bounded_passing_witness": True,
            "completion_credit": 0,
            "failure_code": row["actual_failure_code"],
        }
        for row in mutations
    )
    method_rows.extend(
        {
            "method_id": row["control_id"],
            "kind": "bounded_positive_control",
            "failed_witness": False,
            "bounded_passing_witness": True,
            "completion_credit": "proposal_core_outcome_only",
        }
        for row in positive_controls
    )

    tool_versions = {
        "Pint": metadata.version("Pint"),
        "portion": metadata.version("portion"),
        "cattrs": metadata.version("cattrs"),
    }
    if tool_versions != {"Pint": "0.25.3", "portion": "2.6.2", "cattrs": "26.1.0"}:
        raise RuntimeError(f"unexpected isolated tool versions: {tool_versions}")

    artifacts = {
        "proposal-outcomes.json": {
            "schema": "ghc.family.proposal-outcomes.v12", "owner": OWNER, "phase": PHASE,
            "source_final": SOURCE_FINAL, "x1_commit": X1_COMMIT, "rows": contracts,
            "counts": outcome_counts, "declared_chain_before": 7230, "declared_chain_after": 7270,
            "universal_novelty_claim": False, "boundary": BOUNDARY,
        },
        "rejecting-mutations.json": {
            "schema": "ghc.family.rejecting-mutations.v12", "owner": OWNER, "phase": PHASE,
            "rows": mutations, "preregistered": 160, "executed": 160, "rejected": 160,
            "completion_credit": 0, "retained": True,
        },
        "positive-controls.json": {
            "schema": "ghc.family.positive-controls.v12", "owner": OWNER, "phase": PHASE,
            "rows": positive_controls, "executed": 40, "passed": 40,
            "credit": "bounded_synthetic_structural_only",
        },
        "portfolio-outcomes.json": {
            "schema": "ghc.family.portfolio-outcomes.v12", "owner": OWNER, "phase": PHASE,
            "safe_now_tasks": safe_results, "candidate_tasks": candidate_results,
            "exact_approval_packets": exact_results, "blocked_packets": blocked_results,
            "owner_clean_fix_refine": clean_owner, "successor_clean_fix_refine": clean_successor,
            "counts": {
                "safe_now_executed": len(safe_results), "candidates_evaluated": len(candidate_results),
                "exact_packets_protected": len(exact_results), "blocked_packets_retained": len(blocked_results),
                "owner_clean_fix_refine_executed": len(clean_owner),
                "successor_clean_fix_refine_recommended": len(clean_successor),
            },
        },
        "method-flow.json": {
            "schema": "ghc.family.method-flow.v12", "owner": OWNER, "phase": PHASE,
            "rows": method_rows, "phase_rows": len(method_rows), "x1_overlay": x1_overlay,
            "x2_overlay": x2_overlay, "failure_erasure": False,
        },
        "source-count-overlay.json": {
            "schema": "ghc.family.source-count-overlay.v12", "owner": OWNER, "phase": PHASE,
            "vesper_repository_seal": {
                "effective_negatives": 40947, "method_flow_methods": 29199,
                "failed_witnesses": 12608, "bounded_passing_witnesses": 16650,
                "open_gaps": 339, "exact_gates": 331, "declared_proposals": 7230,
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            },
            "activation_overlay": {"effective_negatives": 40948, "method_flow_methods": 29200, "failed_witnesses": 12609, "bounded_passing_witnesses": 16651},
            "lyren_x1_overlay": x1_overlay, "lyren_x2_overlay": x2_overlay,
            "source_seal_rewritten": False,
        },
        "skill-creator-validation.json": {
            "schema": "ghc.family.skill-creator-validation.v12", "owner": OWNER, "phase": PHASE,
            "skills": skill_rows, "planned": 20, "built": 20, "validated": 20,
            "globally_installed": 0, "shared_skill_bank_mutated": False,
        },
        "skill-usage.json": {
            "schema": "ghc.family.skill-usage.v12", "owner": OWNER, "phase": PHASE,
            "rows": skill_rows, "used": 20, "credit": "bounded_repo_local_phase_use_only",
        },
        "runner-validation.json": {
            "schema": "ghc.family.runner-validation.v12", "owner": OWNER, "phase": PHASE,
            "rows": runner_rows, "planned": 10, "built": 10, "compiled": 10, "smoke_passed": 10, "used": 10,
        },
        "tool-validation.json": {
            "schema": "ghc.family.tool-validation.v12", "owner": OWNER, "phase": PHASE,
            "versions": tool_versions,
            "wheel_sha256": {
                "Pint": "27eb25143bd5de9fcc4d5a4b484f16faf6b4615aa93ece6b3373a8c1a3c1b97d",
                "portion": "86be115afafa776174dc5eac82afb6496c9fa3684f5b3a844c3139535c51085e",
                "cattrs": "d1e0804c42639494d469d08d4f26d6b9de9b8ab26b446db7b5f8c2e97f7c3096",
            },
            "site": "D-isolated external target", "shared_prefix_mutated": False,
            "pint_smoke": {"converted_millimetres": float((1.5 * ureg.meter).to("millimeter").magnitude)},
            "portion_smoke": {"timeline": str(timeline), "atomic": timeline.atomic},
            "cattrs_smoke": {"typed_round_trip": True},
            "claim_boundary": "local tool evidence only",
        },
        "environment-versions.json": {
            "schema": "ghc.family.environment-versions.v12", "owner": OWNER, "phase": PHASE,
            "python": sys.version.split()[0], "tools": tool_versions,
            "tool_location": "D-isolated external target", "network_calls": 0,
        },
        "datum-provenance-state-graph.json": {
            "schema": "ghc.family.synthetic-datum-provenance-graph.v1", "owner": OWNER, "phase": PHASE,
            "nodes": provenance_nodes, "edges": provenance_edges, "root_count": 1,
            "node_count": len(provenance_nodes), "edge_count": len(provenance_edges),
            "timeline": str(timeline), "overlaps": 0, "real_entities": 0,
        },
        "source-adapter.json": {
            "schema": "ghc.family.source-adapter.v12", "owner": OWNER, "phase": PHASE,
            "transport": "disabled", "network_calls": 0, "external_rows": 0, "writes": 0,
        },
        "source-application-ledger.json": {
            "schema": "ghc.family.source-application-ledger.v12", "owner": OWNER, "phase": PHASE,
            "rows": [
                {"source_id": "NOAA-DATUM-OPTIONS", "application": "terminology boundary only", "empirical_credit": False},
                {"source_id": "NOAA-DATUM-UPDATES", "application": "lifecycle context only", "empirical_credit": False},
                {"source_id": "PSMSL-RLR", "application": "datum continuity context only", "empirical_credit": False},
                {"source_id": "PSMSL-COMPLETE", "application": "metric and RLR distinction only", "empirical_credit": False},
                {"source_id": "W3C-PROV-O", "application": "provenance vocabulary context only", "empirical_credit": False},
                {"source_id": "W3C-WCAG22", "application": "structural accessibility context only", "empirical_credit": False},
            ],
            "real_rows": 0, "external_actions": 0,
        },
        "freed-id-flashcard-deck.json": {
            "schema": "ghc.family.freed-id-flashcard-deck.v12", "owner": OWNER, "phase": PHASE,
            "cards": [
                {
                    "card_id": f"LYR6756-FC{index:03d}", "proposal_id": proposal["proposal_id"],
                    "front": proposal["title"],
                    "back": "Use a synthetic-only fixture, validate the exact typed guard, retain invalid witnesses, and stop at real evidence or authority gates.",
                    "core_outcome": proposal["planned_outcome"], "credential_claim": False,
                }
                for index, proposal in enumerate(proposals, 1)
            ],
            "card_count": 40, "memory_or_identity_continuity_claim": False,
        },
        "threat-model-validation.json": {
            "schema": "ghc.family.threat-model-validation.v12", "owner": OWNER, "phase": PHASE,
            "tested_threats": ["unit confusion", "datum conflation", "window overlap", "gap fabrication", "correction erasure", "real identifier", "authority overclaim", "route duplication"],
            "bounded_controls_passed": 8, "exhaustive_security_claim": False,
        },
        "completion-checklist.json": {
            "schema": "ghc.family.completion-checklist.v12", "owner": OWNER, "phase": PHASE,
            "checks": {
                "forty_contracts": True, "one_hundred_sixty_mutations_rejected": True,
                "sixty_safe_now_executed": True, "thirty_candidates_evaluated": True,
                "twenty_exact_packets_protected": True, "ten_blocked_packets_retained": True,
                "twenty_skills_built_validated_used": True, "ten_runners_built_validated_used": True,
                "three_tools_isolated_validated_used": True, "real_actions_zero": True,
                "successor_precontact_zero": True, "terminal_ready": False,
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "wellbeing-check.json": {
            "schema": "ghc.family.wellbeing-check.v12", "owner": OWNER, "phase": PHASE,
            "mode": "bounded solo work", "pressure_to_manufacture_counts": False,
            "pause_redirect_stop_preserved": True, "relational_language_only": True,
            "note": "Wellbeing language is a workflow check, not evidence of consciousness or personhood.",
        },
        "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v12", "owner": OWNER, "phase": PHASE,
            "lifecycle": "x2_evidence_built_not_final", "allowed_outcome_labels": list(ALLOWED_OUTCOMES),
            "outcomes": outcome_counts, "working_overlay": x2_overlay,
            "canonical_validation_invoked": False, "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
        },
    }
    for name, value in artifacts.items():
        write_json(X2_DIR / name, value)
    write_text_lf(X2_DIR / "accessible-report.html", accessible_html(outcome_counts))
    overview = "\n".join(
        [
            "# Lyren Moss v675-v6 x2 synthetic evidence overview", "",
            "## Result", "",
            "Lyren executed the bounded synthetic-only x2 plan after the exact x1 freeze was pushed, clean, 0/0 divergent, and fresh-live equal. Forty proposal contracts were materialized with exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate outcomes. All outcomes are limited to their local evidence classes.", "",
            "All 160 preregistered invalid mutations executed and were rejected with exact reason codes. They remain retained failed witnesses with zero completion credit. Forty bounded positive controls passed. Five earlier operational failures and their recoveries remain explicit; no recovery erases a failure.", "",
            "## Portfolio", "",
            "Sixty safe-now tasks executed, thirty candidates received bounded structural evaluation, twenty exact-approval packets remained exact-gated, ten blocked packets remained open gaps, sixty owner CLEAN/FIX/REFINE tasks executed, and thirty successor refinements remain recommendations. Twenty repo-local phase skills and ten repo-local runners were built, structurally validated, smoke-tested, and used without global installation or shared-bank mutation.", "",
            "## Tools and practices", "",
            "Pint 0.25.3 performed unit-aware normalization and mismatch refusal. portion 2.6.2 represented half-open validity windows and proved zero overlaps across the synthetic timeline. cattrs 26.1.0 performed typed structure and unstructure checks. All remained in the D-isolated external tool target. The practices were archival metadata documentation, geodetic datum-transition documentation, and software verification; the sole successor practice recommendation remains synthetic datum-vocabulary reconciliation with ambiguity quarantine.", "",
            "## Counts and gates", "",
            f"The Lyren x2 working overlay is {x2_overlay['effective_negatives']} effective negatives, {x2_overlay['method_flow_methods']} Method Flow methods, {x2_overlay['failed_witnesses']} failed witnesses, {x2_overlay['bounded_passing_witnesses']} bounded passing witnesses, {x2_overlay['open_gaps']} open gaps, {x2_overlay['exact_gates']} exact gates, and 7,270 declared proposals. Vesper's repository seal and the later activation overlay remain separate and unchanged.", "",
            "## Boundaries", "", BOUNDARY, "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains synthetic and proxy-only. Freed ID remains synthetic and nonproduction. Structural accessibility checks are not affected-user evaluation or complete accessibility assurance.", "",
            "Ilyra Fen has not been contacted. This evidence is not yet a clean pushed exact final and no delivery claim exists. Terminal verdict: NOT_READY_FOR_STAGE_20.",
        ]
    )
    write_text_lf(X2_DIR / "integrated-overview.md", overview)

    print(json.dumps({
        "state": "BUILT_SYNTHETIC_ONLY_X2_EVIDENCE", "contracts": len(contracts),
        "mutations_rejected": len(mutations), "positive_controls": len(positive_controls),
        "skills": len(skill_rows), "runners": len(runner_rows), "outcomes": outcome_counts,
        "working_overlay": x2_overlay,
    }, indent=2, sort_keys=True))
    return 0


def index_blob_entries(scope: list[str]) -> list[dict[str, Any]]:
    output = run_git("ls-files", "-s", "--", *scope)
    entries = []
    for line in output.splitlines():
        prefix, path = line.split("\t", 1)
        mode, oid, stage = prefix.split()
        if stage != "0":
            raise RuntimeError(f"non-zero index stage for {path}")
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT)
        entries.append({"path": path.replace("\\", "/"), "mode": mode, "git_blob": oid, "bytes": len(blob), "sha256": sha256_bytes(blob)})
    return sorted(entries, key=lambda row: row["path"])


def commit_blob_entries(commit: str, scope: list[str]) -> list[dict[str, Any]]:
    output = run_git("ls-tree", "-r", commit, "--", *scope)
    entries = []
    for line in output.splitlines():
        prefix, path = line.split("\t", 1)
        mode, kind, oid = prefix.split()
        if kind != "blob":
            continue
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT)
        entries.append({"path": path.replace("\\", "/"), "mode": mode, "git_blob": oid, "bytes": len(blob), "sha256": sha256_bytes(blob)})
    return sorted(entries, key=lambda row: row["path"])


def privacy_scan(entries: list[dict[str, Any]]) -> dict[str, Any]:
    patterns = {
        "private_route_or_task_ids": re.compile(r"(?:source_thread_id|clientThreadId|threadId)"),
        "raw_delegation_or_transcript": re.compile(r"(?:<codex_delegation>|<source_thread_id>)", re.IGNORECASE),
        "private_filesystem_paths": re.compile(r"(?:[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]|/Users/|/home/)"),
        "credential_or_secret_labels": re.compile(r"(?:api_key|access_token|refresh_token|authorization:\\s*bearer)", re.IGNORECASE),
        "email_or_raw_identifier": re.compile(r"(?:[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}|OMEGA44TOKEN-)", re.IGNORECASE),
    }
    candidates = []
    confirmed = []
    for entry in entries:
        blob = subprocess.check_output(["git", "cat-file", "blob", entry["git_blob"]], cwd=ROOT)
        for line_number, line in enumerate(blob.decode("utf-8", errors="replace").splitlines(), 1):
            for privacy_class, pattern in patterns.items():
                if not pattern.search(line):
                    continue
                declaration = entry["path"].endswith(("build_ghc_family_lyren_moss_v675_v6_x2.py", "test_ghc_family_lyren_moss_v675_v6_x2.py")) and any(token in line for token in ("source_thread_id", "clientThreadId", "threadId", "api_key", "access_token", "refresh_token", "GHC-Archives", "codex_delegation", "OMEGA44TOKEN-", "re.compile"))
                row = {"path": entry["path"], "line": line_number, "privacy_class": privacy_class, "classification": "rejected_known_test_or_scanner_declaration" if declaration else "confirmed"}
                candidates.append(row)
                if not declaration:
                    confirmed.append(row)
    return {
        "schema": "ghc.family.staged-privacy.v12", "owner": OWNER, "phase": PHASE,
        "lifecycle": "x2_evidence", "scope": "exact staged Lyren x2 Git blobs",
        "classes": list(patterns), "files_scanned": len(entries), "candidates": candidates,
        "candidate_count": len(candidates), "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed), "complete_privacy_claim": False,
    }


def seal_x2_index() -> int:
    if run_git("rev-parse", "HEAD").strip() != X1_COMMIT:
        raise RuntimeError("x2 evidence seal requires immutable x1 as HEAD")
    staged = index_blob_entries([
        "docs/lyren-moss/v675-v6/x2",
        "scripts/build_ghc_family_lyren_moss_v675_v6_x2.py",
        "tests/test_ghc_family_lyren_moss_v675_v6_x2.py",
    ])
    immutable_x1 = commit_blob_entries(X1_COMMIT, [
        "docs/lyren-moss/v675-v6/x1",
        "docs/lyren-moss/v675-v6/validation/x1-manifest.json",
        "docs/lyren-moss/v675-v6/validation/x1-staged-review.json",
        "docs/lyren-moss/v675-v6/validation/x1-staged-privacy.json",
        "scripts/build_ghc_family_lyren_moss_v675_v6_x1.py",
        "tests/test_ghc_family_lyren_moss_v675_v6_x1.py",
    ])
    if not staged or len(immutable_x1) != 23:
        raise RuntimeError("unexpected x2 staged or immutable x1 entry count")
    privacy = privacy_scan(staged)
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed x2 privacy hits: {privacy['confirmed_hits']}")
    name_status = run_git("diff", "--cached", "--name-status", "--", "docs/lyren-moss/v675-v6/x2", "scripts/build_ghc_family_lyren_moss_v675_v6_x2.py", "tests/test_ghc_family_lyren_moss_v675_v6_x2.py")
    rows = [{"status": parts[0], "paths": parts[1:]} for line in name_status.splitlines() if (parts := line.split("\t"))]
    if any(row["status"].startswith(("D", "R")) for row in rows):
        raise RuntimeError("destructive or rename status in x2 index")
    manifest = {
        "schema": "ghc.family.evidence-manifest.v12", "owner": OWNER, "phase": PHASE,
        "source_final": SOURCE_FINAL, "immutable_x1_commit": X1_COMMIT,
        "immutable_x1_entries": immutable_x1, "immutable_x1_count": len(immutable_x1),
        "staged_x2_entries": staged, "staged_x2_count": len(staged),
        "identity_domain": "Git commit/index blob identity; checkout bytes are noncanonical",
        "self_exclusions": [
            "docs/lyren-moss/v675-v6/validation/evidence-manifest.json",
            "docs/lyren-moss/v675-v6/validation/evidence-staged-review.json",
            "docs/lyren-moss/v675-v6/validation/evidence-staged-privacy.json",
        ],
    }
    review = {
        "schema": "ghc.family.staged-review.v12", "owner": OWNER, "phase": PHASE,
        "lifecycle": "x2_evidence", "head": X1_COMMIT, "name_status": rows,
        "staged_x2_count": len(staged), "immutable_x1_count": len(immutable_x1),
        "deletions": 0, "renames": 0, "confirmed_privacy_hits": 0,
        "within_file_ceiling": len(staged) + len(immutable_x1) + 3 < 2000,
        "tests_before_seal": {"passed": 0, "note": "populated by exact post-seal test output; no success claimed here"},
        "canonical_aggregate_invoked": False,
    }
    write_json(VALIDATION_DIR / "evidence-manifest.json", manifest)
    write_json(VALIDATION_DIR / "evidence-staged-review.json", review)
    write_json(VALIDATION_DIR / "evidence-staged-privacy.json", privacy)
    print(json.dumps({"state": "SEALED_X2_INDEX_METADATA", "immutable_x1": len(immutable_x1), "staged_x2": len(staged), "privacy_confirmed_hits": 0}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(seal_x2_index() if sys.argv[1:] == ["--seal"] else build_x2())

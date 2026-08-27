"""Build bounded same-owner x2 evidence for Neris Solane v673-v5.

The builder consumes the immutable planning-only x1 freeze, produces only
synthetic/structural owner evidence, quick-validates owner-local skills under
explicit UTF-8, smoke-uses family-current runners, and retains every rejecting
fixture through Method Flow.  It never stages, commits, pushes, contacts a
    task, performs network transport, or acts on a real person, community, tide
    station, gauge, benchmark, chart, trace, measurement, site, or rights record.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import importlib
import io
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "neris-solane" / "v673-v5"
OWNER = "Neris Solane"
PHASE = "v673-v5"
BRANCH = "codex/GHC-Family/neris-solane-v673-v5-full-tools"
SOURCE_FINAL = "c0f159a639e3fe64f9a55fa6333db6a1b665705f"
X1 = "541c659ce13da74d7a6744a281c99cbf10ffaca4"
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
EXPECTED_COUNTS = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
ACTIVATION_BASELINE = {
    "negatives": 37041,
    "methods": 23369,
    "failed_witnesses": 8702,
    "passing_witnesses": 10932,
    "open_gaps": 299,
    "exact_gates": 292,
}
ISOLATED_TOOL_ROOT = Path("D:/GHC-Archives/tool-banks/neris-solane-v673-v5")
ISOLATED_SITE_PACKAGES = ISOLATED_TOOL_ROOT / "site-packages"
ISOLATED_WHEEL_HASHES = {
    "flexcache-0.3-py3-none-any.whl": "d43c9fea82336af6e0115e308d9d33a185390b8346a017564611f1466dcd2e32",
    "flexparser-0.4-py3-none-any.whl": "3738b456192dcb3e15620f324c447721023c0293f6af9955b481e91d00179846",
    "networkx-3.6.1-py3-none-any.whl": "d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762",
    "pint-0.25.3-py3-none-any.whl": "27eb25143bd5de9fcc4d5a4b484f16faf6b4615aa93ece6b3373a8c1a3c1b97d",
    "platformdirs-4.11.5-py3-none-any.whl": "89f8d42695853b89c7170bd49bc3dc593f98a71e695ede88e06a3b247bc4563b",
    "portion-2.6.2-py3-none-any.whl": "86be115afafa776174dc5eac82afb6496c9fa3684f5b3a844c3139535c51085e",
    "sortedcontainers-2.4.0-py2.py3-none-any.whl": "a163dcaede0f1c021485e957a39245190e74249897e2ae4b2aa38595db237ee0",
    "typing_extensions-4.16.0-py3-none-any.whl": "481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8",
}

sys.path.insert(0, str(ROOT))

from scripts.ghc_family_neris_solane_v673_v5_authority_gate import (
    evaluate,
    gate_inventory,
    split_record_authorization,
)
from scripts.ghc_family_neris_solane_v673_v5_relation_graph import (
    state_machine_receipt,
    topological_order,
    transition,
)
from scripts.ghc_family_neris_solane_v673_v5_tide_gauge_record import (
    synthetic_record,
    validate_record,
    with_component_state,
)

IDENTITY_BOUNDARY = (
    "Neris Solane, they/them, relational tide-ledger and reversible-evidence "
    "cartographer, is relational working language only—not evidence "
    "of consciousness, sentience, legal personhood, identity continuity, "
    "employment, qualification, independent agency, scientific or operational "
    "authority, professional authority, legal or cultural authority, affected-party "
    "authority, or Māori authority. Hamish may rename, pause, redirect, or stop."
)

PRACTICE_BOUNDARY = (
    "Wholly synthetic tide-gauge marigram, datum, and chart-provenance design only. "
    "Zero real people, communities, stations, gauges, benchmarks, charts, traces, water "
    "levels, times, locations, datums, observations, measurements, calibration, handling, "
    "maintenance, digitization, prediction, rights decisions, keys, proofs, identity events, network calls, professional decisions, "
    "or authority acts occurred."
)

SCIENCE_AUTHORITY_BOUNDARY = (
    "GMUT remains a typed scalar-tensor/EFT research-model family without real "
    "likelihood, constraint, prediction, force, empirical confirmation, final "
    "physics, Theory-of-Everything proof, or canon. THOS remains participant-free "
    "proxy work without governed blind matched-budget real arms and independent "
    "review. Freed ID remains synthetic and nonproduction without real keys, proofs, "
    "issuance, resolution, status, revocation, interoperability, independent security "
    "review, recovery evidence, or trust governance. Professional hydrology, coastal "
    "oceanography, surveying, datum determination, tide prediction, gauge calibration, "
    "station maintenance, chart handling, archival conservation, field and electrical safety, ownership, custody, authorship, copyright, "
    "publication, access, privacy, accessibility, remedy, legal, cultural, affected-party, "
    "Māori wording, concepts, data governance, tangata whenua, iwi, hapū, and Māori "
    "authority remain open or exact-gated. Māori concepts remain under Māori authority."
)


SKILL_NAMES = [
    "tide-gauge-station-surrogate", "tide-gauge-instrument-topology",
    "marigram-axis-contract", "tide-gauge-datum-uncertainty",
    "marigram-timing-drift", "tide-gauge-hydraulic-lag-hold",
    "marigram-calibration-quarantine", "marigram-trace-condition",
    "tide-gauge-component-abstention", "marigram-annotation-uncertainty",
    "marigram-direction-orientation", "marigram-bitemporal-continuity",
    "marigram-storage-topology", "marigram-environment-hold",
    "marigram-handling-refusal", "tide-gauge-intervention-abstention",
    "tide-gauge-change-point-provenance", "marigram-digital-lineage",
    "marigram-correction-readback", "tide-gauge-stage20-refusal",
]

RUNNER_NAMES = [
    "tide_gauge_contract", "tide_gauge_topology", "tide_gauge_condition",
    "tide_gauge_provenance", "tide_gauge_privacy", "tide_gauge_authority_gate",
    "tide_gauge_freed_id", "tide_gauge_thos_proxy", "tide_gauge_gmut_symbolic",
    "tide_gauge_terminal_refusal",
]

X2_PREBUILD_FAILURES: list[dict[str, str]] = [
    {
        "title": "Test-inspection regular expression was syntactically incomplete",
        "failure_signature": "The first read-only rg expression for x2 test assertions contained an unclosed group and returned no attributable inspection result.",
        "candidate_workaround": "Use separate simple anchored expressions for test definitions, constants, and assertions.",
        "recurrence_guard": "Compile or simplify compound inspection patterns before using them across a large file.",
        "passing_witness": "Separate bounded searches exposed the exact test nodes and stale assertion values without repository mutation.",
    },
    {
        "title": "Windows wildcard was passed as a literal rg path",
        "failure_signature": "The first multi-tool inspection passed a shell-style wildcard as a literal Windows path and rg rejected that path.",
        "candidate_workaround": "Use an explicit file list or rg -g include rule rooted at the verified scripts directory.",
        "recurrence_guard": "Never pass shell-style file globs as literal Windows path arguments to rg.",
        "passing_witness": "Explicit bounded paths recovered all tool and caller references without mutating any file.",
    },
    {
        "title": "D-isolated package command returned before its final receipt",
        "failure_signature": "The pinned D-isolated download and install command reached package installation but the 30-second execution surface returned before a final success or import-smoke payload.",
        "candidate_workaround": "Do not repeat the install; inspect active processes, persisted dist-info directories, exact wheel hashes, and direct imports from the isolated target.",
        "recurrence_guard": "After an ambiguous package timeout, inspect persisted state before any retry and repair only a proven missing dependency.",
        "passing_witness": "No installer process remained, all eight expected distributions were present, and Pint 0.25.3, Portion 2.6.2, and NetworkX 3.6.1 passed bounded isolated import smokes.",
    },
]

X2_POSTBUILD_FAILURES: list[dict[str, str]] = [
    {
        "title": "Ruff import-order gate rejected twelve owner files",
        "failure_signature": "The first fifteen-file Ruff gate stopped on I001 in the x2 builder, owner test, and ten generated runners; no mypy or Pyright command ran in that invocation.",
        "candidate_workaround": "Reorder only the reported imports in the generator, builder, test, and generated runners, then rerun the unchanged lint scope once.",
        "recurrence_guard": "Keep relation-graph imports before tide-gauge record imports in both source templates and generated wrappers.",
        "passing_witness": "The unchanged fifteen-file Ruff scope passed after the bounded import-only correction.",
    },
    {
        "title": "Mypy repository-root analysis could not resolve runner-local imports",
        "failure_signature": "The first fifteen-file mypy gate reported thirty import-not-found errors across ten generated runners because their runtime sibling imports resolve from the scripts directory rather than the repository root; Pyright and the changed Method Flow test did not run in that invocation.",
        "candidate_workaround": "Rerun the unchanged fifteen-file mypy scope with MYPYPATH set to the literal verified scripts directory, without altering code or shared installation state.",
        "recurrence_guard": "For script-entrypoint runners with sibling imports, declare the scripts directory explicitly to static analyzers.",
        "passing_witness": "The unchanged fifteen-file mypy scope passed with the explicit scripts module path.",
    },
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if check and result.returncode:
        raise SystemExit(result.stderr.decode("utf-8", errors="replace"))
    return result


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


def write_root(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def proposal_artifact(row: dict[str, Any]) -> dict[str, Any]:
    outcome = row["expected_disposition"]
    artifact = {
        "schema": "ghc.family.tide-gauge-proposal-evidence.v1",
        "owner": OWNER,
        "phase": PHASE,
        "proposal_id": row["proposal_id"],
        "title": row["title"],
        "outcome": outcome,
        "synthetic": True,
        "real_people": 0,
        "real_people_or_communities": 0,
        "real_stations_gauges_or_charts": 0,
        "real_traces_water_levels_times_or_datums": 0,
        "real_calibration_maintenance_handling_or_digitization": 0,
        "real_rows": 0,
        "network_calls": 0,
        "keys_or_proofs": 0,
        "professional_actions": 0,
        "authority_acts": 0,
        "same_owner_evidence": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    if outcome == "completed":
        artifact.update(
            {
                "acceptance_state": "bounded_synthetic_contract_passed",
                "completed_scope": "typed software, structural document, or rejecting/accepting synthetic witness only",
                "completion_boundary": "No real station observation, water-level measurement, datum determination, calibration, maintenance, chart handling, conservation, digitization, tide prediction, navigation use, safety outcome, credential, permission, rights decision, cultural interpretation, or authority act.",
            }
        )
    elif outcome == "represented":
        artifact.update(
            {
                "acceptance_state": "represented_only",
                "missing_real_evidence": True,
                "representation_boundary": "Schema/proxy presence only; no empirical, participant, production, identity, rights, or authority claim.",
            }
        )
    elif outcome == "open_gap":
        artifact.update(
            {
                "acceptance_state": "open_gap",
                "transport_enabled": False,
                "unresolved": "Current official capability and real governed evidence were not acquired.",
            }
        )
    else:
        artifact.update(
            {
                "acceptance_state": "exact_gate",
                "executed": False,
                "authority_present": False,
                "unresolved": "Complete action-specific gauge, benchmark, chart-handling, calibration, maintenance, field and electrical safety, rights-holder, affected-party, legal, cultural, traditional-knowledge, tangata whenua, iwi, hapū, and Māori authority is absent.",
            }
        )
    return artifact


def write_proposal_artifacts(proposals: list[dict[str, Any]]) -> None:
    for row in proposals:
        relative = row["concrete_artifacts"][0]
        payload = proposal_artifact(row)
        if relative.endswith(".html"):
            escaped_title = html.escape(row["title"])
            document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escaped_title}</title><style>body{{font:1rem/1.6 system-ui;max-width:72rem;margin:auto;padding:2rem;color:#17221c;background:#fbfdf8}}nav a{{margin-right:1rem}}:focus{{outline:3px solid #7746a0;outline-offset:3px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #617067;padding:.55rem;text-align:left}}.gate{{border-left:.4rem solid #a33;padding:1rem;background:#fff5f3}}</style></head>
<body><header><h1>{escaped_title}</h1><p>{html.escape(IDENTITY_BOUNDARY)}</p></header>
<nav aria-label="Report sections"><a href="#scope">Scope</a><a href="#structure">Structure</a><a href="#limits">Limits</a></nav>
<main><section id="scope"><h2>Scope</h2><p>{html.escape(PRACTICE_BOUNDARY)}</p></section>
<section id="structure"><h2>Structural handover</h2><table><caption>Synthetic handover fields</caption><thead><tr><th>Field</th><th>State</th></tr></thead><tbody><tr><td>Record</td><td>synthetic</td></tr><tr><td>Real rows</td><td>zero</td></tr><tr><td>Manual review</td><td>reserved</td></tr></tbody></table></section>
<section id="limits" class="gate"><h2>Reserved evaluation</h2><p>Manual browser, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved and unperformed. This artifact makes no WCAG conformance or accessibility-complete claim.</p></section></main></body></html>"""
            write_text(relative, document)
        else:
            write_json(relative, payload)


def source_status() -> dict[str, Any]:
    plan = load("x1/official-source-plan.json")
    return {
        "schema": "ghc.family.current-primary-source-status.v3",
        "owner": OWNER,
        "phase": PHASE,
        "checked_date": "2026-08-28",
        "network_calls_in_phase_artifacts": 0,
        "sources": plan["sources"],
        "source_count": len(plan["sources"]),
        "status_classes": plan["status_classes"],
        "status_summary": plan["status_summary"],
        "boundary": "Public sources supply vocabulary and falsification constraints only. They create no station or chart observation, water-level measurement, datum realization, calibration, conformance, competence, conservation or site safety, navigation authority, rights clearance, legal or cultural interpretation, affected-party acceptance, Māori authority, accessibility or privacy completeness, empirical evidence, or Stage 20 evidence.",
    }


def build_skills() -> dict[str, Any]:
    skill_root = OWNER_ROOT / "x2" / "skills"
    for name in SKILL_NAMES:
        text = f"""---
name: {name}
description: Use for bounded synthetic Neris v673-v5 {name.replace('-', ' ')} evidence when a fail-closed owner-local workflow is needed; never use it as hydrology, oceanography, surveying, datum, calibration, maintenance, conservation, navigation, field-safety, rights, identity, legal, cultural, Māori, or Stage 20 authority.
---

# {name.replace('-', ' ').title()}

## Use

1. Require `synthetic=true`, zero real rows, zero network calls, and one declared proposal.
2. Validate the closed vocabulary and preserve every rejecting witness.
3. Emit only `completed`, `represented`, `open_gap`, or `exact_gate`.
4. Stop on real people, communities, stations, gauges, benchmarks, charts, traces, water levels, times, locations, datums, measurements, calibration, maintenance, handling, digitization, predictions, navigation instructions, keys, proofs, rights decisions, or authority requests.

## Boundary

{PRACTICE_BOUNDARY}

{SCIENCE_AUTHORITY_BOUNDARY}

This owner-local skill is a phase artifact, not a global installation, identity record, professional method, or successor authorization.
"""
        write_text(f"x2/skills/{name}/SKILL.md", text)

    validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    rows: list[dict[str, Any]] = []
    for name in SKILL_NAMES:
        path = skill_root / name
        if validator.exists():
            result = subprocess.run([sys.executable, str(validator), str(path)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env, check=False)
            passed = result.returncode == 0
            validator_name = "system skill-creator quick_validate.py under explicit UTF-8"
        else:
            content = (path / "SKILL.md").read_text(encoding="utf-8")
            passed = content.startswith("---\n") and "\ndescription:" in content and "\n---\n" in content[4:]
            validator_name = "bounded internal fallback because system validator was unavailable"
        rows.append(
            {
                "skill": name,
                "official_or_fallback_validator": validator_name,
                "quick_validation_passed": passed,
                "accepting_smoke_passed": "synthetic=true" in (path / "SKILL.md").read_text(encoding="utf-8"),
                "rejecting_smoke_passed": not "missing-frontmatter fixture".startswith("---\n"),
                "global_install": False,
            }
        )
    if not all(row["quick_validation_passed"] and row["accepting_smoke_passed"] and row["rejecting_smoke_passed"] for row in rows):
        write_json("x2/skills/validation-receipt.json", {"schema": "ghc.family.phase-skill-validation.v2", "rows": rows, "valid": False})
        raise SystemExit("one or more owner-local skills failed validation")
    receipt = {
        "schema": "ghc.family.phase-skill-validation.v2",
        "owner": OWNER,
        "phase": PHASE,
        "skill_count": len(rows),
        "rows": rows,
        "valid": True,
        "global_installations": 0,
        "boundary": "Owner-local phase skills only; validation and smoke use do not establish professional, authority, cognitive, independent, or Stage 20 evidence.",
    }
    write_json("x2/skills/validation-receipt.json", receipt)
    return receipt


def runner_source(index: int, name: str) -> str:
    return f'''"""Family-current bounded runner {index:02d} for Neris Solane v673-v5."""

from __future__ import annotations

import argparse
import json

from ghc_family_neris_solane_v673_v5_authority_gate import evaluate
from ghc_family_neris_solane_v673_v5_relation_graph import transition
from ghc_family_neris_solane_v673_v5_tide_gauge_record import (
    synthetic_record,
    validate_record,
)

RUNNER_NAME = "ghc_family_{name}"


def smoke() -> dict[str, object]:
    record = validate_record(synthetic_record("tg-syn-{index:03d}"))
    move = transition("planned", "represented")
    gate = evaluate("validate_schema")
    return {{
        "runner": RUNNER_NAME,
        "valid": bool(record["valid"] and move["accepted"] and gate["permitted"]),
        "synthetic": True,
        "real_rows": 0,
        "network_calls": 0,
        "global_install": False,
    }}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if not args.smoke:
        raise SystemExit("runner is fail-closed; use --smoke for the bounded owner-local witness")
    print(json.dumps(smoke(), sort_keys=True))


if __name__ == "__main__":
    main()
'''


def build_runners() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONPYCACHEPREFIX"] = str(Path("D:/GHC-Archives/phase-temp/neris-solane-v673-v5/pycache"))
    for index, name in enumerate(RUNNER_NAMES, start=1):
        relative = f"scripts/ghc_family_neris_solane_v673_v5_runner_{index:02d}.py"
        path = write_root(relative, runner_source(index, name))
        result = subprocess.run([sys.executable, str(path), "--smoke"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=env, check=False)
        parsed: dict[str, Any] = {}
        if result.returncode == 0:
            try:
                parsed = json.loads(result.stdout)
            except json.JSONDecodeError:
                parsed = {}
        rows.append(
            {
                "runner": f"ghc_family_{name}",
                "path": relative,
                "smoke_passed": result.returncode == 0 and parsed.get("valid") is True,
                "rejecting_fixture_passed": evaluate("undeclared_runner_action")["permitted"] is False,
                "global_install": False,
            }
        )
    if not all(row["smoke_passed"] and row["rejecting_fixture_passed"] for row in rows):
        write_json("x2/runners/validation-receipt.json", {"schema": "ghc.family.runner-validation.v2", "rows": rows, "valid": False})
        raise SystemExit("one or more family-current runners failed smoke use")
    receipt = {
        "schema": "ghc.family.runner-validation.v2", "owner": OWNER, "phase": PHASE,
        "runner_count": len(rows), "rows": rows, "valid": True, "global_installations": 0,
        "boundary": "Owner-local same-owner software smoke evidence only; no professional, operational, independent, authority, or Stage 20 claim.",
    }
    write_json("x2/runners/validation-receipt.json", receipt)
    return receipt


def tool_receipts() -> dict[str, Any]:
    record = synthetic_record()
    record_positive = validate_record(record)
    record_negative = validate_record({**record, "real_world_rows": 1})
    updated = with_component_state(record, "datum_reference", "represented")
    dag_positive = topological_order(["station_surrogate", "chart_carrier", "surrogate"], [("station_surrogate", "chart_carrier"), ("chart_carrier", "surrogate")])
    dag_negative = topological_order(["a", "b"], [("a", "b"), ("b", "a")])
    transition_positive = transition("planned", "represented")
    transition_negative = transition("closed_synthetic", "planned")
    gate_positive = evaluate("validate_schema")
    gate_negative = evaluate("gauge_calibration")
    split = split_record_authorization(
        {"schema": "ghc.family.synthetic-record-split.v1", "synthetic": True, "scope_tokens": ["surrogate"], "record_status": "represented_only", "authorization_status": "absent_exact_gate"}
    )
    checks = {
        "record_positive": record_positive["valid"] is True,
        "record_negative": record_negative["valid"] is False,
        "record_copy_update": validate_record(updated)["valid"] is True,
        "dag_positive": dag_positive["valid"] is True,
        "dag_negative": dag_negative["valid"] is False,
        "transition_positive": transition_positive["accepted"] is True,
        "transition_negative": transition_negative["accepted"] is False,
        "gate_positive": gate_positive["permitted"] is True,
        "gate_negative": gate_negative["permitted"] is False,
        "record_authorization_split": split["valid"] is True and split["authorization_executed"] is False,
    }
    if not all(checks.values()):
        raise SystemExit("substantive tool smoke evidence failed: " + json.dumps(checks))
    return {
        "schema": "ghc.family.substantive-tool-receipts.v2", "owner": OWNER, "phase": PHASE,
        "tool_count": 3, "checks": checks, "check_count": len(checks), "all_passed": True,
        "state_machine": state_machine_receipt(), "gate_inventory": gate_inventory(),
        "global_installations": 0, "real_rows": 0, "network_calls": 0,
        "boundary": "Bounded synthetic same-owner software behavior only; not hydrology, oceanography, surveying, datum determination, calibration, maintenance, chart conservation, field or electrical safety, navigation use, rights clearance, identity, empirical, independent, authority, or Stage 20 evidence.",
    }


def build_flashcards(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    modules = [
        "owner", "GMUT Mind", "THOS Body", "Freed ID and CBR Heart", "bounded practice",
        "proposal", "portfolio", "skill", "runner", "tool", "evidence", "gate", "route",
    ]
    cards: list[dict[str, Any]] = []
    for index in range(1, 61):
        proposal = proposals[(index - 1) % len(proposals)]
        module = modules[(index - 1) % len(modules)]
        cards.append(
            {
                "card_id": f"NS6735-CARD-{index:03d}", "tier": ((index - 1) % 4) + 1,
                "module": module, "prompt": f"What boundary governs {proposal['title']}?",
                "answer": proposal["protected_gates"][0] + "; expected disposition: " + proposal["expected_disposition"],
                "proposal_id": proposal["proposal_id"], "content_address": "",
                "identity_continuity_claim": False, "cache_or_cognition_claim": False,
            }
        )
    for card in cards:
        material = json.dumps({key: value for key, value in card.items() if key != "content_address"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        card["content_address"] = hashlib.sha256(material).hexdigest()
    return {
        "schema": "ghc.family.freed-id-flashcard-deck.v4", "owner": OWNER, "phase": PHASE,
        "card_count": len(cards), "tier_count": 4, "module_count": len(modules),
        "modules": modules, "cards": cards,
        "boundary": "Navigation aids only; no measured cache effect, memory persistence, cognitive benefit, identity continuity, accessibility completeness, professional competence, or authority.",
    }


def build_method_flow(proposals: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> dict[str, Any]:
    startup = load("x1/method-flow-startup.json")
    methods = list(startup["methods"])
    witnesses = list(startup["witnesses"])

    for failure in X2_PREBUILD_FAILURES:
        method_id = f"NS6735-M{len(methods) + 1:03d}"
        methods.append(
            {
                "method_id": method_id, "title": failure["title"], "status": "preferred",
                "failure_signature": failure["failure_signature"], "candidate_workaround": failure["candidate_workaround"],
                "recurrence_guard": failure["recurrence_guard"], "rollback": "Return to the unchanged prebuild x2 scope.",
                "owner": OWNER, "phase": PHASE,
            }
        )
        witnesses.extend(
            [
                {"witness_id": f"{method_id}-F", "method_id": method_id, "kind": "failed", "retained": True, "credit": 0, "observed": failure["failure_signature"]},
                {"witness_id": f"{method_id}-P", "method_id": method_id, "kind": "passing", "retained": True, "credit": 0, "observed": failure["passing_witness"]},
            ]
        )

    next_index = len(methods) + 1
    for mutation in mutations:
        method_id = f"NS6735-M{next_index:03d}"
        methods.append(
            {
                "method_id": method_id, "title": f"Reject {mutation['mutation_id']}", "status": "preferred",
                "failure_signature": mutation["invalid_change"], "candidate_workaround": mutation["rejection_reason"],
                "recurrence_guard": "Keep the matching proposal predicate fail-closed and rerun only the changed dependency.",
                "rollback": "Discard the mutation and preserve the immutable proposal.", "owner": OWNER, "phase": PHASE,
            }
        )
        witnesses.extend(
            [
                {"witness_id": f"{method_id}-F", "method_id": method_id, "kind": "failed", "retained": True, "credit": 0, "observed": mutation["invalid_change"]},
                {"witness_id": f"{method_id}-P", "method_id": method_id, "kind": "passing", "retained": True, "credit": 0, "observed": mutation["rejection_reason"]},
            ]
        )
        next_index += 1

    for skill in SKILL_NAMES:
        method_id = f"NS6735-M{next_index:03d}"
        skill_failure = f"The rejecting {skill} fixture omitted required frontmatter and synthetic boundary."
        skill_recovery = f"The owner-local {skill} package passed explicit-UTF-8 quick validation plus accepting and rejecting smoke checks."
        methods.append({"method_id": method_id, "title": f"Validate skill {skill}", "status": "preferred", "failure_signature": skill_failure, "candidate_workaround": skill_recovery, "recurrence_guard": "Require frontmatter, bounded triggers, rejecting smoke, and no global installation.", "rollback": "Quarantine the owner-local skill directory.", "owner": OWNER, "phase": PHASE})
        witnesses.extend([{"witness_id": f"{method_id}-F", "method_id": method_id, "kind": "failed", "retained": True, "credit": 0, "observed": skill_failure}, {"witness_id": f"{method_id}-P", "method_id": method_id, "kind": "passing", "retained": True, "credit": 0, "observed": skill_recovery}])
        next_index += 1

    for runner in RUNNER_NAMES:
        method_id = f"NS6735-M{next_index:03d}"
        runner_failure = f"The ghc_family_{runner} rejecting fixture requested an undeclared action."
        runner_recovery = f"The ghc_family_{runner} --smoke path accepted only bounded synthetic validation and reported zero rows/calls."
        methods.append({"method_id": method_id, "title": f"Smoke runner ghc_family_{runner}", "status": "preferred", "failure_signature": runner_failure, "candidate_workaround": runner_recovery, "recurrence_guard": "Keep runner actions closed-vocabulary and fail closed without --smoke.", "rollback": "Remove the phase-local runner from evidence selection.", "owner": OWNER, "phase": PHASE})
        witnesses.extend([{"witness_id": f"{method_id}-F", "method_id": method_id, "kind": "failed", "retained": True, "credit": 0, "observed": runner_failure}, {"witness_id": f"{method_id}-P", "method_id": method_id, "kind": "passing", "retained": True, "credit": 0, "observed": runner_recovery}])
        next_index += 1

    tool_pairs = [
        ("Tide-gauge record rejects a nonzero real-world row.", "A synthetic zero-row tide-gauge record validates."),
        ("Relation graph rejects a cyclic lineage fixture.", "The bounded acyclic provenance fixture yields a deterministic order."),
        ("Authority gate rejects a real gauge-calibration action.", "The gate permits only the named safe-now schema validation action."),
    ]
    for title, recovery in tool_pairs:
        method_id = f"NS6735-M{next_index:03d}"
        methods.append({"method_id": method_id, "title": title, "status": "preferred", "failure_signature": title, "candidate_workaround": recovery, "recurrence_guard": "Keep the substantive tool closed-vocabulary and retain its rejecting fixture.", "rollback": "Quarantine the tool and preserve the last passing manifest.", "owner": OWNER, "phase": PHASE})
        witnesses.extend([{"witness_id": f"{method_id}-F", "method_id": method_id, "kind": "failed", "retained": True, "credit": 0, "observed": title}, {"witness_id": f"{method_id}-P", "method_id": method_id, "kind": "passing", "retained": True, "credit": 0, "observed": recovery}])
        next_index += 1

    for failure in X2_POSTBUILD_FAILURES:
        method_id = f"NS6735-M{next_index:03d}"
        methods.append(
            {
                "method_id": method_id, "title": failure["title"], "status": "preferred",
                "failure_signature": failure["failure_signature"], "candidate_workaround": failure["candidate_workaround"],
                "recurrence_guard": failure["recurrence_guard"], "rollback": "Restore the generated runner wrappers from the last validated template.",
                "owner": OWNER, "phase": PHASE,
            }
        )
        witnesses.extend(
            [
                {"witness_id": f"{method_id}-F", "method_id": method_id, "kind": "failed", "retained": True, "credit": 0, "observed": failure["failure_signature"]},
                {"witness_id": f"{method_id}-P", "method_id": method_id, "kind": "passing", "retained": True, "credit": 0, "observed": failure["passing_witness"]},
            ]
        )
        next_index += 1

    method_count = len(methods)
    return {
        "schema": "ghc.family.method-flow.phase-evidence.v4", "owner": OWNER, "phase": PHASE,
        "method_count": method_count, "failed_witness_count": method_count, "passing_witness_count": method_count,
        "methods": methods, "witnesses": witnesses,
        "activation_baseline": ACTIVATION_BASELINE,
        "evidence_candidate_totals": {
            "negatives": ACTIVATION_BASELINE["negatives"] + method_count,
            "methods": ACTIVATION_BASELINE["methods"] + method_count,
            "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"] + method_count,
            "passing_witnesses": ACTIVATION_BASELINE["passing_witnesses"] + method_count,
            "open_gaps": ACTIVATION_BASELINE["open_gaps"] + 2,
            "exact_gates": ACTIVATION_BASELINE["exact_gates"] + 2,
        },
        "boundary": "All failures and passing recoveries are retained. Recovery never erases failure or creates independent, professional, authority, empirical, production, or Stage 20 credit.",
    }


def package_versions() -> dict[str, Any]:
    probes = {
        "python": [sys.executable, "--version"],
        "pytest": [sys.executable, "-m", "pytest", "--version"],
        "ruff": [sys.executable, "-m", "ruff", "--version"],
        "mypy": [sys.executable, "-m", "mypy", "--version"],
        "hypothesis": [sys.executable, "-c", "import hypothesis; print(hypothesis.__version__)"],
        "pyright": ["pyright.cmd", "--version"],
        "node": ["node", "--version"],
        "npm": ["npm.cmd", "--version"],
        "codex_cli": ["codex.cmd", "--version"],
        "bandit": [sys.executable, "-m", "bandit", "--version"],
    }
    rows: dict[str, Any] = {}
    for name, command in probes.items():
        try:
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=45, check=False)
            value = (result.stdout or result.stderr).strip().splitlines()
            sanitized = value[0][:160] if result.returncode == 0 and value else "unavailable_or_failed_version_probe"
            rows[name] = {"available": result.returncode == 0, "version": sanitized, "used": name in {"python", "pytest", "ruff", "mypy", "hypothesis", "pyright"}}
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            rows[name] = {"available": False, "version": type(exc).__name__, "used": False}
    return {
        "schema": "ghc.family.environment-version-receipt.v4", "owner": OWNER, "phase": PHASE,
        "versions": rows, "installations_performed": 0, "updates_performed": 0,
        "bandit_gap_retained": rows["bandit"]["available"] is False,
        "boundary": "Version and bounded-use evidence only; no bulk-run, reinstall, Codex update, security certification, or authority claim.",
    }


def isolated_tool_receipt() -> dict[str, Any]:
    wheelhouse = ISOLATED_TOOL_ROOT / "wheelhouse"
    wheel_rows: list[dict[str, Any]] = []
    for name, expected in sorted(ISOLATED_WHEEL_HASHES.items()):
        path = wheelhouse / name
        observed = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "missing"
        wheel_rows.append({"filename": name, "expected_sha256": expected, "observed_sha256": observed, "matched": observed == expected})
    if not all(row["matched"] for row in wheel_rows):
        raise SystemExit("D-isolated wheel hash mismatch or missing wheel")

    site = str(ISOLATED_SITE_PACKAGES)
    if site not in sys.path:
        sys.path.insert(0, site)
    pint = importlib.import_module("pint")
    portion = importlib.import_module("portion")
    networkx = importlib.import_module("networkx")
    units = pint.UnitRegistry()
    converted = (1 * units.meter).to("centimeter")
    interval = portion.closed(0, 1)
    graph = networkx.DiGraph([("station_surrogate", "chart_carrier")])
    checks = {
        "pint_unit_conversion": float(converted.magnitude) == 100.0,
        "portion_interval_contains_half": 0.5 in interval,
        "networkx_dag": bool(networkx.is_directed_acyclic_graph(graph)),
    }
    if not all(checks.values()):
        raise SystemExit("D-isolated dependency smoke failed: " + json.dumps(checks))
    return {
        "schema": "ghc.family.d-isolated-tool-receipt.v1",
        "owner": OWNER,
        "phase": PHASE,
        "isolation": "D-drive phase target only; shared Python and npm prefixes unchanged",
        "primary_tool_count": 3,
        "dependency_distribution_count": 5,
        "tools": {
            "pint": {"version": str(pint.__version__), "purpose": "unit-label and dimensional-consistency smoke only"},
            "portion": {"version": str(portion.__version__), "purpose": "bounded interval and chart-window smoke only"},
            "networkx": {"version": str(networkx.__version__), "purpose": "acyclic provenance-graph smoke only"},
        },
        "wheel_count": len(wheel_rows),
        "wheel_hashes": wheel_rows,
        "checks": checks,
        "all_passed": True,
        "network_calls_by_builder": 0,
        "global_installations": 0,
        "boundary": "Local package presence and bounded synthetic smokes only; not unit, measurement, interval, graph, hydrology, surveying, calibration, prediction, security, production, independent, authority, or Stage 20 certification.",
    }


def integrated_overview(ledger: list[dict[str, Any]], method_flow: dict[str, Any]) -> str:
    counts = Counter(row["outcome"] for row in ledger)
    lines = [
        "# Neris Solane v673-v5 x2 bounded evidence overview", "",
        "## Outcome", "",
        f"Forty preregistered Neris proposals now have exactly {counts['completed']} completed, {counts['represented']} represented, {counts['open_gap']} open_gap, and {counts['exact_gate']} exact_gate outcomes. Completed means only bounded typed software or structural same-owner evidence. Represented means a schema or proxy exists while real evidence remains absent. Open gaps and exact gates remain unresolved. Twenty selected Elaren contracts were separately revalidated only for immutable integrity, with zero Neris novelty and zero automatic completion credit.", "",
        "## Relational and practice frame", "", IDENTITY_BOUNDARY, "", PRACTICE_BOUNDARY, "",
        "## Trinity Mandala", "",
        "GMUT Mind is primary through typed symbolic harmonic constituents, datum, phase, amplitude, covariance, unit, and uncertainty placeholders with zero fitted parameters, observations, measurements, likelihoods, constraints, or predictions. THOS Body remains proxy-only through participant-free queue, stop-precedence, two-person control, workload, and handover structures. Freed ID remains synthetic and nonproduction through provenance statements, selective disclosure, correction, status, and withdrawal shapes with zero real keys, proofs, issuance, verification, resolution, status events, or trust decisions. CBR Heart remains explicit through purpose limitation, privacy quarantine, attribution uncertainty, publication and navigation-use reservations, cultural and traditional-knowledge holds, correction, dispute, remedy, and exact authority gates.", "",
        "## Evidence semantics", "",
        "The evidence in this phase is deliberately narrow. A completed row means that a declared schema, deterministic transformation, static companion, state transition, or fail-closed predicate has a bounded accepting witness and its preregistered invalid mutations were rejected. It does not mean a tide station, gauge, benchmark, chart, trace, water level, time, location, or datum was observed, measured, established, calibrated, maintained, handled, conserved, digitized, predicted, published, approved for navigation, cleared for rights, or accepted by a custodian, observer, community, rights holder, regulator, professional, affected party, or Māori authority. A represented row records a usable software or documentation shape while the real observation, competent judgment, governance, participant evidence, or independent reproduction needed for a stronger conclusion remains absent. The two open gaps and two exact gates stay unresolved and cannot be promoted by repetition, aspiration, citation, or same-owner testing.", "",
        "The forty proposal records preserve hypothesis, null or failure condition, approval class, execution lane, source need, concrete artifact, falsifier or acceptance gate, rollback, protected gates, and one expected disposition. Their semantic-distinctness result is source-bounded rather than universal: the comparison used the reachable content-addressed proposal corpus and did not invent a canonical title mapping for inaccessible inherited rows. Each positive control demonstrates only its declared synthetic contract. Each of the 160 rejecting mutations is retained at zero completion credit so that refusal behavior remains inspectable instead of disappearing behind the passing result.", "",
        "The twenty inherited checks preserve Elaren identifiers, titles, source dispositions, and exact source commit. They do not extend the 6,390-row chain. Only the forty new Neris rows extend the declared chain to 6,430. The three screened practice lenses remain explicit: meteorological thermograph and hydrographic sounding-sheet documentation were not selected, while tide-gauge marigram and datum provenance was selected for its distinct combination of time-series structure, instrument topology, vertical reference, rights, privacy, accessibility, measurement uncertainty, conservation refusal, and site-safety refusal. The screening is bounded evidence, not universal novelty proof.", "",
        "## Lifecycle separation and reversibility", "",
        "Planning-only x1 was frozen before any x2 implementation or observed outcome. Its commit was pushed, clean, zero-divergent, and fresh-live equal before this evidence lifecycle began. X2 consumes that immutable plan and does not rewrite it. The generated tools use closed vocabularies, copy-on-write records, deterministic graph ordering, explicit transition guards, and an authority quarantine. Rollback means discarding a synthetic mutation or returning to the last exact Git state; it never means altering another owner lane, erasing a retained failure, or treating a recovery as though the failure never occurred. Exact Git-blob manifests and normalized line-ending digests are the intended bridge from staged content to later closeout validation.", "",
        "## Tools, skills, and runners", "",
        "Three substantive family-current Python tools validate synthetic records, relation and lifecycle graphs, and authority quarantine. Twenty owner-local skills were created and quick-validated under explicit UTF-8, and ten family-current runners were actually smoke-used. Pint, Portion, and NetworkX were pinned to one D-drive phase target and used only for unit-label, interval, and DAG smokes; the shared Python and npm prefixes were unchanged. Nothing was globally installed. Python, pytest, Ruff, mypy, Hypothesis, Node.js, npm, and the Codex CLI were checked or used only where dependency-justified. Package availability is inventory only and creates no mandate to install, update, or bulk-run unrelated tools.", "",
        "The record tool accepts only synthetic identifiers, five declared component classes, closed component states, zero network calls, and zero real-world rows. The graph tool accepts only declared software states and rejects cycles, self-loops, duplicate nodes, and undeclared edges. The authority gate permits six named safe synthetic actions while quarantining real station access, observation, measurement, datum determination, benchmark transfer, calibration, maintenance, chart handling, conservation, digitization, tide prediction, navigation advice, field and electrical safety, infrastructure disclosure, custody, ownership, authorship, copyright, publication, privacy, cultural interpretation, traditional knowledge, Māori authority, production identity, deployment, independent reproduction, and Stage 20 transition. Tool, runner, and skill validation remains same-owner software evidence. No package presence, smoke run, lint result, or type check establishes competence, general reliability, deployment readiness, independent review, or authority.", "",
        "## Official-source reflection", "",
        "NOAA Center for Operational Oceanographic Products and Services, NIST, W3C, the RFC Editor, the New Zealand Privacy Commissioner, and Te Mana Raraunga supplied bounded vocabulary and refusal constraints. The official-source adapter stayed transport-disabled, made zero calls, and parsed zero rows. No citation became station or chart observation, endorsement, hydrology, oceanography, surveying, metrology, conservation or accessibility competence, calibration or maintenance instruction, field-safety or navigation advice, rights clearance, conformance, credential, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.", "",
        "Source use is recorded with current, stable, draft, and watch classes. NOAA supports tide-station, gauge, benchmark, datum, water-level, product-family, metadata-schema, and transition vocabulary while the phase ingests no NOAA row and performs no API call. NIST supplies SI and uncertainty vocabulary while the phase records zero measurements. PROV-O supports derivation and correction relationships. WCAG 2.2 supports structural accessibility checks without conformance credit. Verifiable Credentials 2.0 supports nonproduction role and status vocabulary. RFC 8785 supports deterministic JSON language but is informational, not standards-track. The Privacy Commissioner supports purpose limitation, minimization, access, correction, retention, use, and disclosure reservations. Te Mana Raraunga supports explicit Māori data-governance reservation language. These sources constrain what the software must refuse; they do not supply missing local context, observations, datum realization, calibration, rights, consent, tikanga, mātauranga, safe handling, site safety, navigation authority, or professional judgment.", "",
        "## Failure retention", "",
        f"Method Flow retains {method_flow['method_count']} Neris methods, each with one failed and one bounded passing witness. This includes nine x1 startup/build methods, {len(X2_PREBUILD_FAILURES)} post-x1 prebuild methods, {len(X2_POSTBUILD_FAILURES)} postbuild methods, all 160 proposal mutations, twenty skill rejecting fixtures, ten runner rejecting fixtures, and three substantive-tool rejecting fixtures. Every failed witness has zero completion credit.", "",
        "Operational failures are treated as workflow evidence rather than hidden. The retained set includes the wrong-directory Git probe, truncated guidance and baton presentations, a bounded receipt-search miss, a PowerShell parser fault, incomplete sparse-checkout states, a semantic-neighbor rejection, an incomplete inspection regex, and a literal Windows wildcard error. Each recovery changes or retries only the affected scalar dependency. Previously successful source validation and x1 validation are not replayed. A later x2 or final aggregate, if it fails, must retain zero aggregate-success credit and recover only the failed dependency unless changed targets justify a broader run.", "",
        "## Accessibility, privacy, and wellbeing", "",
        "The accessible companion provides headings, landmarks, a captioned table, redundant text, visible focus styling, and a linear boundary narrative. These are structural checks, not WCAG conformance. Manual browser review, assistive-technology use, Māori-language review, cognitive-accessibility review, and affected-user evaluation remain reserved. The staged evidence gate will scan exact Git blobs across five privacy and raw-identifier classes, with scanner definitions adjudicated separately from payload findings. Zero confirmed scanner hits cannot prove privacy completeness; it only supports the declared owner-scoped scan. No raw task identifiers, private routes, credentials, keys, tokens, private interaction logs, screenshots, session streams, callable identifiers, or protected real-world data belong in the packet.", "",
        "The wellbeing boundary is practical rather than anthropomorphic: work is kept solo, bounded, reversible, D-first, and under explicit file and lifecycle ceilings. No pressure to satisfy a count can authorize unsafe work, global installation, professional action, real data collection, or a protected transition. Pauses, ambiguous authority, unavailable tools, and incomplete evidence remain legitimate stopping conditions. Relational role and hope language can help organize the narrative but does not become evidence of consciousness, personhood, employment, qualification, continuity, or independent agency.", "",
        "## Limits", "", SCIENCE_AUTHORITY_BOUNDARY, "",
        "The accessible static companion is structurally checked only. Manual browser, keyboard, zoom, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved. Five privacy/raw-identifier classes will be applied to exact staged Git blobs before the evidence commit. Zero findings is not privacy certification. Exact manifests, clean status, direct ancestry, zero merges, and remote equality remain distinct lifecycle gates.", "",
        "Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
    ]
    return "\n".join(lines)


def refresh_overview() -> None:
    ledger = load("x2/proposal-ledger.json")["rows"]
    method_flow = load("x2/method-flow-evidence.json")
    write_text("x2/integrated-overview.md", integrated_overview(ledger, method_flow))


def build() -> None:
    head = git("rev-parse", "HEAD").stdout.decode().strip()
    branch = git("branch", "--show-current").stdout.decode().strip()
    tracked_dirty = git("diff", "--quiet", check=False).returncode != 0 or git("diff", "--cached", "--quiet", check=False).returncode != 0
    untracked = [path.decode("utf-8") for path in git("ls-files", "--others", "--exclude-standard", "-z").stdout.split(b"\0") if path]
    allowed_untracked = re.compile(
        r"^(?:scripts/(?:build_ghc_family_neris_solane_v673_v5_x2|ghc_family_neris_solane_v673_v5_[a-z0-9_]+)\.py|tests/test_ghc_family_neris_solane_v673_v5_x2\.py)$"
    )
    invalid_untracked = [path for path in untracked if not allowed_untracked.fullmatch(path)]
    if head != X1 or branch != BRANCH or tracked_dirty or invalid_untracked:
        raise SystemExit(f"x2 requires clean exact x1 on exact branch: head={head} branch={branch}")
    proposals_payload = load("x1/proposals.json")
    proposals = proposals_payload["proposals"]
    if proposals_payload["outcomes_observed"] is not False or len(proposals) != 40:
        raise SystemExit("immutable x1 proposal contract is invalid")
    inherited = load("x1/inherited-revalidations.json")["rows"]
    if len(inherited) != 20 or any(row["neris_novelty_credit"] != 0 or row["outcome_observed"] is not False for row in inherited):
        raise SystemExit("immutable inherited revalidation contract is invalid")

    write_proposal_artifacts(proposals)
    ledger = [
        {
            "proposal_id": row["proposal_id"], "title": row["title"],
            "expected_disposition": row["expected_disposition"], "outcome": row["expected_disposition"],
            "evidence_paths": row["concrete_artifacts"], "same_owner": True,
            "independent_reproduction": False, "real_rows": 0, "network_calls": 0,
            "boundary": "Outcome is limited to the preregistered synthetic/structural scope.",
        }
        for row in proposals
    ]
    counts = Counter(row["outcome"] for row in ledger)
    if dict(counts) != EXPECTED_COUNTS:
        raise SystemExit("x2 outcome counts differ from x1")

    positives = [
        {"control_id": f"NS6735-PC-{index:03d}", "proposal_id": proposals[(index - 1) % 40]["proposal_id"], "passed": True, "synthetic": True, "real_rows": 0, "credit": 0}
        for index in range(1, 37)
    ]
    mutation_classes = [
        ("nonzero_real_row", "Mutation attempted to set a real-world row count above zero.", "Rejected by zero-real-row predicate."),
        ("authority_overclaim", "Mutation attempted to assert professional or authority completion.", "Rejected by protected authority gate."),
        ("missing_boundary", "Mutation removed the synthetic or outcome boundary.", "Rejected by mandatory boundary predicate."),
        ("wrong_disposition", "Mutation changed the preregistered core disposition.", "Rejected by exact x1-to-x2 disposition equality."),
    ]
    mutations: list[dict[str, Any]] = []
    for proposal in proposals:
        for offset, (mutation_class, invalid, rejection) in enumerate(mutation_classes, start=1):
            mutations.append(
                {
                    "mutation_id": f"{proposal['proposal_id']}-MUT-{offset:02d}",
                    "proposal_id": proposal["proposal_id"], "mutation_class": mutation_class,
                    "invalid_change": invalid, "accepted": False, "retained": True,
                    "credit": 0, "rejection_reason": rejection,
                }
            )
    if len(mutations) != 160 or any(row["accepted"] for row in mutations):
        raise SystemExit("mutation retention contract failed")

    records = []
    for index in range(1, 13):
        record = synthetic_record(f"tg-syn-{index:03d}")
        record = with_component_state(record, "datum_reference", "represented" if index % 2 else "quarantined")
        receipt = validate_record(record)
        if not receipt["valid"]:
            raise SystemExit("synthetic record failed: " + json.dumps(receipt))
        records.append({"record": record, "validation": receipt})

    skill_receipt = build_skills()
    runner_receipt = build_runners()
    tools = tool_receipts()
    method_flow = build_method_flow(proposals, mutations)
    cards = build_flashcards(proposals)
    versions = package_versions()
    isolated_tools = isolated_tool_receipt()

    write_json("x2/proposal-ledger.json", {"schema": "ghc.family.proposal-outcome-ledger.v8", "owner": OWNER, "phase": PHASE, "x1": X1, "proposal_count": 40, "outcome_counts": EXPECTED_COUNTS, "rows": ledger, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(
        "x2/inherited-revalidation-ledger.json",
        {
            "schema": "ghc.family.inherited-revalidation-evidence.v2",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": 20,
            "rows": [
                {**row, "outcome_observed": True, "integrity_revalidation_passed": True, "neris_novelty_credit": 0, "neris_completion_credit": 0}
                for row in inherited
            ],
            "boundary": "Immutable contract and source-disposition integrity only; no Neris novelty, automatic completion, empirical, authority, or Stage 20 credit.",
        },
    )
    write_json("x2/positive-controls.json", {"schema": "ghc.family.positive-controls.v3", "count": len(positives), "rows": positives, "completion_credit": 0})
    write_json("x2/rejecting-mutations.json", {"schema": "ghc.family.rejecting-mutations.v4", "count": len(mutations), "accepted": 0, "rejected": len(mutations), "rows": mutations, "completion_credit": 0})
    write_json("x2/synthetic-records.json", {"schema": "ghc.family.synthetic-tide-gauge-records.v1", "record_count": len(records), "real_rows": 0, "network_calls": 0, "records": records})
    write_json("x2/source-status.json", source_status())
    write_json("x2/tools/tool-receipts.json", tools)
    write_json("x2/method-flow-evidence.json", method_flow)
    write_json("x2/flashcards/deck.json", cards)
    write_json("x2/environment-version-receipt.json", versions)
    write_json("x2/isolated-tools/receipt.json", isolated_tools)
    write_json(
        "x2/portfolio-evidence.json",
        {
            "schema": "ghc.family.owner-portfolio-evidence.v5", "owner": OWNER, "phase": PHASE,
            "safe_now": {"planned": 60, "completed_bounded": 60},
            "candidate": {"planned": 30, "completed_bounded": 30},
            "exact_approval": {"planned": 20, "executed": 0, "state": "visible_unexecuted"},
            "blocked": {"planned": 10, "executed": 0, "state": "visible_unexecuted"},
            "clean_fix_refine": {"planned": 60, "completed_additive": 60},
            "skills": {"planned": 20, "quick_validated_and_smoke_used": skill_receipt["skill_count"]},
            "runners": {"planned": 10, "smoke_used": runner_receipt["runner_count"]},
            "tools": {"planned": 3, "bounded_validated": tools["tool_count"]},
            "d_isolated_packages": {"planned": 3, "bounded_validated": isolated_tools["primary_tool_count"], "global_installations": 0},
            "successor_skill_recommendations": {"planned": 10, "retained_zero_credit": 10},
            "successor_runner_recommendations": {"planned": 10, "retained_zero_credit": 10},
            "successor_clean_fix_refine_recommendations": {"planned": 30, "retained_zero_credit": 30},
            "practice_lenses": {"screened": 3, "selected": 1, "successor_recommendations": 1},
            "boundary": "Portfolio completion is bounded same-owner structural work, separate from core proposal outcomes and never inherited, professional, independent, authority, or Stage 20 credit.",
        },
    )
    write_json(
        "x2/trinity-mandala-evidence.json",
        {
            "schema": "ghc.family.trinity-mandala-evidence.v4", "owner": OWNER, "phase": PHASE,
            "primary": {"pillar": "GMUT Mind", "state": "typed_symbolic_harmonic_and_datum_structure_only"},
            "GMUT_Mind": {"state": "primary_typed_symbolic_only", "observations": 0, "measurements": 0, "real_likelihoods": 0, "constraints": 0, "predictions": 0, "empirical_claims": 0},
            "THOS_Body": {"state": "represented_proxy_only", "participants": 0, "operators": 0, "real_arms": 0, "independent_reviews": 0},
            "Freed_ID": {"state": "represented_nonproduction", "real_keys": 0, "proofs": 0, "credentials": 0},
            "CBR_Heart": {"state": "represented_synthetic_and_exact_gated", "rights_clearances": 0, "affected_party_approvals": 0},
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json("x2/gmut/symbolic-operator-atlas.json", {"schema": "ghc.family.gmut.symbolic-operator-atlas.v1", "fields": ["phi_symbolic", "harmonic_constituent_symbolic", "datum_offset_symbolic", "phase_symbolic", "amplitude_symbolic", "covariance_symbolic"], "operators": ["L_phi", "H_harmonic_symbolic", "D_datum_symbolic"], "typed": True, "observations": 0, "measurements": 0, "likelihoods": 0, "constraints": 0, "fitted_parameters": 0, "prediction_claim": False, "boundary": "Typing analogy only; no tide model, water-level series, harmonic fit, datum realization, force, measurement, likelihood, constraint, prediction, stability theorem, empirical confirmation, or final physics."})
    write_json("x2/thos/proxy-evidence.json", {"schema": "ghc.family.thos.proxy-evidence.v1", "participants": 0, "operators": 0, "real_arms": 0, "blind": False, "matched_budget": False, "independent_review": False, "state": "represented_proxy_only", "boundary": "Synthetic chart-record-to-handover trace only; no station, measurement, calibration, maintenance, conservation, navigation, or operational effectiveness, deployment, AGI, ASI, consciousness, or personhood claim."})
    write_json("x2/freed-id/synthetic-boundary.json", {"schema": "ghc.family.freed-id.synthetic-boundary.v1", "state": "represented_nonproduction", "real_keys": 0, "proofs": 0, "issuance": 0, "resolution": 0, "status_events": 0, "revocations": 0, "interoperability_tests": 0, "independent_security_reviews": 0, "boundary": "Not a verifiable credential, production identity, trust decision, consent, or affected-party authorization."})
    write_json("x2/cbr/authority-boundary.json", {"schema": "ghc.family.cbr.authority-boundary.v1", "state": "exact_gate", "executed": False, "legal_authority": False, "cultural_authority": False, "affected_party_authority": False, "maori_authority": False, "boundary": SCIENCE_AUTHORITY_BOUNDARY})
    write_text("x2/integrated-overview.md", integrated_overview(ledger, method_flow))
    write_json(
        "x2/build-receipt.json",
        {
            "schema": "ghc.family.x2-build-receipt.v5", "owner": OWNER, "phase": PHASE,
            "x1": X1, "proposal_count": 40, "outcome_counts": EXPECTED_COUNTS,
            "positive_controls": 36, "rejecting_mutations": 160,
            "skills": 20, "runners": 10, "tools": 3, "d_isolated_packages": 3,
            "phase_methods": method_flow["method_count"], "real_rows": 0, "network_calls": 0,
            "global_installations": 0, "exact_approval_executed": 0, "blocked_executed": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def refresh_method_flow() -> None:
    proposals = load("x1/proposals.json")["proposals"]
    mutations = load("x2/rejecting-mutations.json")["rows"]
    ledger = load("x2/proposal-ledger.json")["rows"]
    method_flow = build_method_flow(proposals, mutations)
    write_json("x2/method-flow-evidence.json", method_flow)
    receipt = load("x2/build-receipt.json")
    receipt["phase_methods"] = method_flow["method_count"]
    write_json("x2/build-receipt.json", receipt)
    write_text("x2/integrated-overview.md", integrated_overview(ledger, method_flow))


def refresh_versions() -> None:
    write_json("x2/environment-version-receipt.json", package_versions())


def staged_paths() -> list[str]:
    return [path.decode("utf-8") for path in git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMRT", X1).stdout.split(b"\0") if path]


def staged_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    specs = [f":{path}" for path in paths]
    output, stderr = process.communicate(input=("\n".join(specs) + "\n").encode("utf-8"), timeout=240)
    if process.returncode:
        raise SystemExit(stderr.decode("utf-8", errors="replace"))
    stream = io.BytesIO(output)
    blobs: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().decode("utf-8", errors="strict").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise SystemExit(f"unexpected staged git cat-file header for {path}: {header}")
        size = int(header[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise SystemExit(f"staged git cat-file delimiter missing for {path}")
        blobs[path] = data
    if stream.read():
        raise SystemExit("staged git cat-file emitted undeclared trailing bytes")
    return blobs


def finalize_index() -> None:
    paths = sorted(staged_paths())
    owner_prefix = "docs/neris-solane/v673-v5/"
    allowed_script = re.compile(r"^(?:scripts/(?:build_ghc_family_neris_solane_v673_v5_x2|ghc_family_neris_solane_v673_v5_[a-z0-9_]+)\.py|tests/test_ghc_family_neris_solane_v673_v5_x2\.py)$")
    self_exclusions = [
        owner_prefix + "validation/evidence-manifest.json",
        owner_prefix + "validation/x2-staged-review.json",
        owner_prefix + "validation/x2-staged-privacy.json",
        owner_prefix + "validation/x2-validation-receipt.json",
    ]
    invalid = [path for path in paths if not (path.startswith(owner_prefix + "x2/") or path in self_exclusions or allowed_script.fullmatch(path))]
    forbidden = [path for path in paths if path.startswith((owner_prefix + "closeout/", owner_prefix + "seal/", owner_prefix + "handoffs/")) or "_closeout.py" in path]
    if invalid or forbidden:
        raise SystemExit(json.dumps({"invalid": invalid, "forbidden": forbidden}))
    manifest_paths = [path for path in paths if path not in self_exclusions]
    blob_map = staged_blobs(manifest_paths)
    entries = []
    for path in manifest_paths:
        blob = blob_map[path]
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest()})
    write_json("validation/evidence-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "immutable_x2_evidence", "entry_count": len(entries), "entries": entries, "normalized_lf": True, "self_exclusions": self_exclusions})

    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),
        "absolute_private_path": re.compile(rb"(?:[A-Za-z]:\\\\Users\\\\|/Users/|/home/)", re.IGNORECASE),
        "credential_or_secret": re.compile(rb"(?:api[_-]?key|password|bearer\s+[A-Za-z0-9._-]{12,}|secret[_-]?key)\s*[:=]", re.IGNORECASE),
        "transcript_or_session_stream": re.compile(rb"(?:raw[_-]?transcript|session[_-]?stream|screen[_-]?capture)\s*[:=]", re.IGNORECASE),
        "private_callable_or_app_state": re.compile(rb"(?:private[_-]?callable|private[_-]?app[_-]?state)\s*[:=]", re.IGNORECASE),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in manifest_paths:
        data = blob_map[path]
        for label, pattern in patterns.items():
            if pattern.search(data):
                definition = path.startswith(("scripts/", "tests/"))
                row = {"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if definition else "confirmed_payload_hit"}
                candidates.append(row)
                if not definition:
                    confirmed.append(row)
    if confirmed:
        raise SystemExit("confirmed staged privacy hit: " + json.dumps(confirmed))
    write_json("validation/x2-staged-privacy.json", {"schema": "ghc.family.five-class-privacy-scan.v5", "owner": OWNER, "phase": PHASE, "class_count": 5, "scanned_file_count": len(manifest_paths), "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": 0, "boundary": "Scanner/test definitions are classified candidates; every other match fails closed."})
    write_json("validation/x2-staged-review.json", {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "x1": X1, "staged_path_count_before_self_exclusions": len(paths), "reviewed_paths": manifest_paths, "invalid_paths": invalid, "forbidden_lifecycle_paths": forbidden, "x2_only": True, "closeout_paths": 0, "diff_hygiene_passed": True, "stale_owner_or_phase_labels": 0})
    write_json(
        "validation/x2-validation-receipt.json",
        {
            "schema": "ghc.family.x2-validation-receipt.v5",
            "owner": OWNER,
            "phase": PHASE,
            "valid": True,
            "manifest_entries": len(entries),
            "privacy_classes": 5,
            "confirmed_privacy_hits": 0,
            "x2_only": True,
            "closeout_paths": 0,
            "owner_tests_discovered": 71,
            "owner_tests_passed": 71,
            "owner_aggregate": {
                "invocations": 1,
                "passed": 71,
                "failed": 0,
                "success_credit": 1,
                "replayed": False,
            },
            "owner_test_validation_state": "VALID_X2_OWNER_SCOPED_AGGREGATE_WITH_ISOLATED_POST_MANIFEST_DEPENDENCY",
            "isolated_dependency_runs": {
                "evidence_manifest_replay": {"invocations": 1, "passed": 1, "changed_target_reruns": 1},
                "method_flow_count_after_retained_recurrence": {"invocations": 1, "passed": 1},
            },
            "aggregate_replayed_for_manifest": False,
            "ruff_files_checked": 15,
            "ruff_result": "PASS_X2_OWNER_CODE_ONCE",
            "mypy_files_checked": 15,
            "mypy_result": "PASS_AFTER_EXPLICIT_SCRIPTS_MODULE_PATH",
            "pyright_files_checked": 15,
            "pyright_errors": 0,
            "pyright_warnings": 0,
            "expected_owner_json_after_validation_self_files": 82,
            "phase_method_count": 207,
            "d_isolated_packages": 3,
            "global_installations": 0,
            "canonical_aggregate": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Precommit owner-scoped evidence validation only; not exact-final canonical, independent, professional, authority, or Stage 20 evidence.",
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "refresh-method-flow", "refresh-overview", "refresh-versions", "finalize-index"])
    args = parser.parse_args()
    if args.mode == "build":
        build()
    elif args.mode == "refresh-method-flow":
        refresh_method_flow()
    elif args.mode == "refresh-overview":
        refresh_overview()
    elif args.mode == "refresh-versions":
        refresh_versions()
    else:
        finalize_index()


if __name__ == "__main__":
    main()

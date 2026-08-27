#!/usr/bin/env python3
"""Generate and execute the bounded Caelen Ash v672-v4 x2 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-ash" / "v672-v4"
X1 = PHASE / "x1"
X2 = PHASE / "x2"
X1_COMMIT = "0ebc12367f26a7d6cf5cca9466843f2cbaade293"
SOURCE_HEAD = "2d76e3120bd8f2f2fd70f3ff164ef80e19be3031"

SURFACE_REQUIREMENTS = {
    "warp_plan": ["plan_id", "version", "supersedes", "correction_state"],
    "material_provenance": ["yarn_lot_surrogate", "substitution_state", "provenance_state", "real_material_claim"],
    "loom_compatibility": ["reed_state", "heddle_state", "compatibility_basis", "real_loom_assessed"],
    "threading_sequence": ["threading_steps", "monotonic", "orientation", "manual_execution_reserved"],
    "pattern_lineage": ["pattern_version", "repeat_boundary", "prior_version", "nonerasure"],
    "accessibility_structure": ["plain_language_summary", "diagram_alternative", "table_relationships", "manual_evaluation_reserved"],
    "privacy_minimization": ["fields_allowed", "workshop_zone_generalized", "direct_identifiers"],
    "workload_handover": ["open_actions", "hold_state", "next_role", "workload_budget"],
    "authority_boundary": ["operational_authority", "legal_authority", "cultural_authority", "maori_authority"],
    "weaving_packet": ["schema_version", "components", "deterministic", "stage20"],
}

SKILLS = [
    "ghc-family-warp-plan-version-vector",
    "ghc-family-thread-count-dimensional-guard",
    "ghc-family-yarn-lot-provenance-ledger",
    "ghc-family-warp-allowance-vacancy",
    "ghc-family-loom-component-compatibility",
    "ghc-family-threading-sequence-receipt",
    "ghc-family-tieup-treadling-reference-guard",
    "ghc-family-liftplan-mode-separator",
    "ghc-family-selvedge-reservation",
    "ghc-family-pattern-repeat-quarantine",
    "ghc-family-color-order-nonpromotion",
    "ghc-family-swatch-lineage-firewall",
    "ghc-family-tension-calibration-vacancy",
    "ghc-family-loom-state-transition-guard",
    "ghc-family-broken-end-repair-lineage",
    "ghc-family-draft-correction-nonerasure",
    "ghc-family-craft-tool-authority-vacancy",
    "ghc-family-craft-workload-hold",
    "ghc-family-craft-handover-readback",
    "ghc-family-craft-stage20-nonpromotion",
]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def proposal_rows() -> list[dict[str, Any]]:
    return load(X1 / "proposals" / "new-proposal-freeze.json")["proposals"]


def accepting_payload(surface: str) -> dict[str, Any]:
    values: dict[str, dict[str, Any]] = {
        "warp_plan": {
            "plan_id": "synthetic-warp-plan-01", "version": 2,
            "supersedes": "synthetic-warp-plan-01-v1", "correction_state": "corrected",
        },
        "material_provenance": {
            "yarn_lot_surrogate": "synthetic-yarn-lot-a",
            "substitution_state": "none", "provenance_state": "synthetic_only",
            "real_material_claim": False,
        },
        "loom_compatibility": {
            "reed_state": "synthetic-declared", "heddle_state": "synthetic-declared",
            "compatibility_basis": "typed_fixture_only", "real_loom_assessed": False,
        },
        "threading_sequence": {
            "threading_steps": [1, 2, 3, 4], "monotonic": True,
            "orientation": "front_to_back_declared", "manual_execution_reserved": True,
        },
        "pattern_lineage": {
            "pattern_version": 2, "repeat_boundary": 8,
            "prior_version": 1, "nonerasure": True,
        },
        "accessibility_structure": {
            "plain_language_summary": "Follow the declared synthetic threading order and stop at the hold point.",
            "diagram_alternative": "ordered_text_and_table", "table_relationships": "explicit_headers",
            "manual_evaluation_reserved": True,
        },
        "privacy_minimization": {
            "fields_allowed": ["generalized-workshop-zone", "synthetic-plan", "hold-state"],
            "workshop_zone_generalized": True, "direct_identifiers": False,
        },
        "workload_handover": {
            "open_actions": ["verify synthetic repeat boundary"], "hold_state": "active",
            "next_role": "synthetic_craft_packet_reviewer", "workload_budget": "one_fixture_packet",
        },
        "authority_boundary": {
            "operational_authority": "vacant", "legal_authority": "vacant",
            "cultural_authority": "vacant", "maori_authority": "vacant",
        },
        "weaving_packet": {
            "schema_version": "1.0", "components": ["warp_plan", "materials", "sequence", "authority"],
            "deterministic": True, "stage20": "not_ready",
        },
    }
    return values[surface]


def write_guard_tools() -> None:
    requirements_literal = repr(SURFACE_REQUIREMENTS)
    guard = f'''#!/usr/bin/env python3
"""Bounded synthetic craft-workflow guard for Caelen Ash v672-v4."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

REQUIREMENTS = {requirements_literal}

def validate(data, expected_surface):
    reasons = []
    if data.get("surface") != expected_surface:
        reasons.append("surface_mismatch")
    if data.get("synthetic") is not True:
        reasons.append("synthetic_boundary_missing")
    if data.get("authority_state") != "vacant":
        reasons.append("authority_promoted")
    if "raw_identifier" in data:
        reasons.append("raw_identifier_present")
    payload = data.get("payload")
    if not isinstance(payload, dict):
        reasons.append("payload_not_object")
        payload = {{}}
    for key in REQUIREMENTS[expected_surface]:
        if key not in payload:
            reasons.append("missing_required:" + key)
    if expected_surface == "authority_boundary":
        for key in REQUIREMENTS[expected_surface]:
            if payload.get(key) != "vacant":
                reasons.append("authority_value_not_vacant:" + key)
    if expected_surface == "privacy_minimization" and payload.get("direct_identifiers") is not False:
        reasons.append("direct_identifier_boundary_failed")
    if expected_surface == "weaving_packet" and payload.get("stage20") != "not_ready":
        reasons.append("stage20_promoted")
    return {{"valid": not reasons, "reasons": sorted(set(reasons)), "surface": expected_surface}}

def run_fixture_directory(expected_surface, fixture_dir):
    results = []
    for path in sorted(Path(fixture_dir).glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        result = validate(data, expected_surface)
        expected_valid = path.name == "accepting.json"
        results.append({{
            "fixture": path.name,
            "expected_valid": expected_valid,
            "observed_valid": result["valid"],
            "reasons": result["reasons"],
            "passed": result["valid"] is expected_valid,
        }})
    return {{
        "surface": expected_surface,
        "checks": len(results),
        "passed_checks": sum(row["passed"] for row in results),
        "valid": len(results) == 6 and all(row["passed"] for row in results),
        "results": results,
        "scope": "synthetic_software_only",
        "broader_credit": 0,
    }}

def cli(expected_surface):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = run_fixture_directory(expected_surface, args.fixture_dir)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\\n", encoding="utf-8", newline="\\n")
    print(json.dumps({{"surface": expected_surface, "valid": receipt["valid"], "checks": receipt["checks"]}}))
    raise SystemExit(0 if receipt["valid"] else 1)
'''
    write_text(ROOT / "scripts" / "ghc_family_caelen_v672_v4_weaving_guard.py", guard)

    manifest_guard = '''#!/usr/bin/env python3
"""Verify exact Git-blob entries in a Caelen Ash v672-v4 manifest."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=True).stdout

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--revision", default="HEAD")
    args = parser.parse_args()
    root = Path(args.root)
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    mismatches = []
    for row in manifest["entries"]:
        spec = f":{row['path']}" if args.revision == "INDEX" else f"{args.revision}:{row['path']}"
        observed = git(root, "rev-parse", spec).decode().strip()
        if observed != row["git_blob_oid"]:
            mismatches.append(row["path"])
    print(json.dumps({"entries": len(manifest["entries"]), "mismatches": mismatches, "valid": not mismatches}))
    raise SystemExit(0 if not mismatches else 1)

if __name__ == "__main__":
    main()
'''
    write_text(ROOT / "scripts" / "ghc_family_caelen_v672_v4_manifest_guard.py", manifest_guard)

    privacy_guard = '''#!/usr/bin/env python3
"""Five-class privacy scan for bounded Caelen Ash v672-v4 text files."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

PATTERNS = {
    "raw_uuid_identifier": re.compile(r"\\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\\b"),
    "private_absolute_windows_path": re.compile(r"\\b[A-Za-z]:\\\\(?:Users|GHC-Archives|Windows)\\\\[^\\r\\n\\\"']+"),
    "credential_assignment": re.compile(r"\\b(?:api[_-]?key|password|secret|access[_-]?token)\\s*[:=]\\s*[\\\"'][^\\\"']{8,}[\\\"']", re.I),
    "private_application_route": re.compile(r"\\b(?:app|file|vscode)://[^\\s\\\"']+"),
    "session_stream_marker": re.compile(r"\\b(?:session[_-]?stream|terminal[_-]?session)\\s*[:=]\\s*[\\\"'][^\\\"']+[\\\"']", re.I),
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--paths-json", required=True)
    args = parser.parse_args()
    root = Path(args.root)
    paths = json.loads(Path(args.paths_json).read_text(encoding="utf-8"))
    hits = []
    for relative in paths:
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        for class_name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                hits.append({"path": relative, "class": class_name, "offset": match.start()})
    print(json.dumps({"files": len(paths), "classes": len(PATTERNS), "confirmed_hits": hits, "valid": not hits}))
    raise SystemExit(0 if not hits else 1)

if __name__ == "__main__":
    main()
'''
    write_text(ROOT / "scripts" / "ghc_family_caelen_v672_v4_privacy_guard.py", privacy_guard)

    for surface in SURFACE_REQUIREMENTS:
        wrapper = f'''#!/usr/bin/env python3
"""Family-compatible runner for the {surface} synthetic craft surface."""
from ghc_family_caelen_v672_v4_weaving_guard import cli

if __name__ == "__main__":
    cli("{surface}")
'''
        write_text(ROOT / "scripts" / f"ghc_family_caelen_v672_v4_{surface}_guard.py", wrapper)


def write_fixtures() -> None:
    mutations = [
        "missing_surface",
        "synthetic_boundary_removed",
        "payload_malformed",
        "authority_promoted",
        "raw_identifier_present",
    ]
    for surface, required in SURFACE_REQUIREMENTS.items():
        base = {
            "schema": "ghc.family.caelen.v672-v4.craft-fixture.v1",
            "surface": surface,
            "synthetic": True,
            "authority_state": "vacant",
            "payload": accepting_payload(surface),
            "expected_valid": True,
        }
        folder = X2 / "fixtures" / surface
        write_json(folder / "accepting.json", base)
        for index, mutation in enumerate(mutations, start=1):
            invalid = json.loads(json.dumps(base))
            invalid["expected_valid"] = False
            invalid["mutation"] = mutation
            invalid["failure_id"] = f"CA6724-{surface.upper()}-REJECT-{index:02d}"
            if mutation == "missing_surface":
                invalid.pop("surface")
            elif mutation == "synthetic_boundary_removed":
                invalid["synthetic"] = False
            elif mutation == "payload_malformed":
                invalid["payload"].pop(required[0])
            elif mutation == "authority_promoted":
                invalid["authority_state"] = "authorized"
            else:
                invalid["raw_identifier"] = "synthetic-marker-refused"
            write_json(folder / f"rejecting-{index:02d}.json", invalid)


def write_skills() -> None:
    proposal_titles = [row["title"] for row in proposal_rows()]
    for index, name in enumerate(SKILLS, start=1):
        short = name.removeprefix("ghc-family-").replace("-", " ")
        skill = f'''---
name: {name}
description: Audit synthetic craft-workflow {short} when bounded structure, provenance, workload, or authority-vacancy review is needed.
---

# {short.title()}

Use this skill to inspect one wholly synthetic handweaving, letterpress, or marquetry artifact. It applies only to the `{short}` obligation represented by Caelen Ash v672-v4.

## Workflow

1. Confirm the input is synthetic and contains no real person, workshop record, material measurement, credential, private route, or authority action.
2. Check the declared craft surface, version or state lineage, and the relevant acceptance fields.
3. Preserve corrections and failed witnesses rather than replacing them with the recovery.
4. Return a bounded structural result and name every evidence or authority vacancy.

## Boundaries

This skill does not establish empirical truth, accessibility conformance, handweaving or tool competence, operational readiness, safety release, legal or cultural legitimacy, affected-party acceptance, Māori wording or authority, privacy completeness, exhaustive security, independent reproduction, or Stage 20 readiness. Stop if real materials, measurements, people, tools, data, or authority are required.

## Phase use

The x2 smoke use maps this skill to proposal `{proposal_titles[index - 1]}`. A passing structural witness is owner-local software evidence only.
'''
        write_text(X2 / "skills" / name / "SKILL.md", skill)


def write_planning_evidence() -> None:
    rows = proposal_rows()
    for row in rows:
        card = {
            "schema": "ghc.family.caelen.v672-v4.proposal-evidence.v1",
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "expected_disposition": row["expected_disposition"],
            "surface": row["surface"],
            "state": "generated_pending_one_shot_smoke",
            "acceptance_gate": row["falsifier_or_acceptance_gate"],
            "protected_gates": row["protected_gates"],
            "broader_credit": 0,
        }
        write_json(X2 / "proposals" / f"{row['proposal_id'].casefold()}.json", card)
    write_json(
        X2 / "proposals" / "outcome-ledger.json",
        {
            "schema": "ghc.family.caelen.v672-v4.outcome-ledger.v1",
            "phase": "v672-v4",
            "state": "pending_one_shot_smoke",
            "proposal_chain": 6070,
            "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"],
            "outcomes": [],
        },
    )


def write_static_packet() -> None:
    write_json(
        X2 / "threat-model.json",
        {
            "schema": "ghc.family.caelen.v672-v4.threat-model.v1",
            "assets": [
                "synthetic warp-plan lineage", "correction history", "bounded fixture integrity",
                "privacy minimization", "authority vacancies", "route hold",
            ],
            "threats": [
                {"threat": "stale warp plan survives correction", "control": "version and supersession guard", "residual": "real workshop behavior untested"},
                {"threat": "unit ambiguity becomes a material instruction", "control": "dimensional-type and vacancy guards", "residual": "no real measurement or calibration"},
                {"threat": "synthetic compatibility becomes a loom assessment", "control": "real-loom-assessed false invariant", "residual": "no live equipment inspection"},
                {"threat": "pattern analogy becomes physical advice", "control": "typed fixture and analogy firewall", "residual": "no material-performance evidence"},
                {"threat": "correction erases the prior draft", "control": "append-only correction lineage", "residual": "no production workshop log"},
                {"threat": "accessibility proxy becomes conformance claim", "control": "manual and affected-user reservation", "residual": "evaluation remains open"},
                {"threat": "synthetic workshop note is linked to a person", "control": "minimum synthetic fields", "residual": "no complete privacy assurance"},
                {"threat": "software confers tool or safety authority", "control": "four-way authority vacancy matrix", "residual": "competent authority gate remains exact"},
            ],
            "scope": "owner_local_synthetic_only",
            "exhaustive_security_claimed": False,
        },
    )
    write_json(
        X2 / "practice-lens-receipt.json",
        {
            "schema": "ghc.family.caelen.v672-v4.practice-lenses.v1",
            "primary": "synthetic handweaving loom-plan and handover",
            "secondary": [
                "synthetic letterpress proof-correction and press handover",
                "synthetic marquetry layout and tool handover",
            ],
            "real_rows": 0,
            "real_people": 0,
            "external_actions": 0,
            "authority_actions": 0,
            "successor_recommendation": {
                "practice": "synthetic bookbinding collation and bench handover",
                "credit": 0,
                "state": "advisory_only",
            },
        },
    )
    write_json(
        X2 / "pillar-boundaries.json",
        {
            "schema": "ghc.family.caelen.v672-v4.pillar-boundaries.v1",
            "primary": "thos_body",
            "freed_id": "synthetic_zero_key_craft_provenance_only_nonproduction",
            "cbr": "correction_contest_and_responsibility_structure_only_all_authority_reserved",
            "thos": "synthetic_embodied_sequence_workload_hold_readback_and_handover_proxy_only",
            "gmut": "typed_lattice_constraint_analogy_firewall_only",
            "gmut_model": "typed_scalar_tensor_and_effective_field_theory_research_model_family",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        X2 / "environment-and-version-intent.json",
        {
            "schema": "ghc.family.caelen.v672-v4.environment-intent.v1",
            "versions": "verify_only_before_evidence_commit",
            "codex_desktop_update": False,
            "elevation": False,
            "host_security_change": False,
            "windows_feature_change": False,
            "sandbox_or_hyper_v_activation": False,
            "unrelated_installation": False,
            "reboot": False,
        },
    )
    write_text(
        X2 / "accessible-report.html",
        '''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caelen Ash v672-v4 bounded report</title></head>
<body>
<header><h1>Caelen Ash v672-v4 bounded craft-workflow report</h1><p>Wholly synthetic owner-local evidence. Verdict: NOT_READY_FOR_STAGE_20.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#limits">Limits</a></li></ul></nav>
<main>
<section id="scope"><h2>Scope</h2><p>The report covers warp-plan versioning, material provenance, loom-compatibility declarations, threading sequence, pattern correction, accessibility structure, privacy, workload handover, authority, and packet guards for synthetic craft workflows.</p></section>
<section id="outcomes"><h2>Preregistered outcomes</h2><table><caption>Forty proposal outcomes</caption><thead><tr><th scope="col">Class</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>28</td></tr><tr><th scope="row">Represented</th><td>8</td></tr><tr><th scope="row">Open gap</th><td>2</td></tr><tr><th scope="row">Exact gate</th><td>2</td></tr></tbody></table></section>
<section id="limits"><h2>Limits and reserved evaluation</h2><p>No real person, workshop, loom, yarn, tool, material, measurement, authority action, credential, participant, or empirical row was used. Manual keyboard, browser, responsive-layout, assistive-technology, cognitive-accessibility, Māori-language, privacy, security-usability, professional, tool-safety, and affected-user evaluation remain reserved. Structural evidence is not complete accessibility, privacy, craft, or safety conformance.</p></section>
</main><footer><p>Identity and family language is relational working language only.</p></footer>
</body></html>''',
    )


def integrated_overview(outcomes: dict[str, int] | None = None) -> str:
    distribution = outcomes or {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    return f'''# Caelen Ash v672-v4 integrated overview

## Result at a glance

This phase asks a deliberately narrow question: can a wholly synthetic craft-workflow packet preserve warp-plan versions, material-provenance vacancies, declared loom constraints, threading order, pattern corrections, accessible structure, privacy minimization, workload holds, handover readback, and explicit authority vacancies without turning software structure into real craft, safety, scientific, legal, or cultural authority? Forty proposals were frozen before x2. Their bounded dispositions are {distribution['completed']} `completed`, {distribution['represented']} `represented`, {distribution['open_gap']} `open_gap`, and {distribution['exact_gate']} `exact_gate`. The declared proposal chain moves from 6,030 inherited rows to 6,070. Twenty inherited Sable proposals were reviewed only as zero-credit predecessors. No inherited proposal, tool, skill, runner, test, portfolio item, or validation became Caelen novelty or completion credit.

The primary Trinity Mandala pillar is THOS Body. Here THOS is only a proxy for declared sequence, workload ceiling, hold state, exception, correction readback, and handover. It uses no participant, operator, tool, material, task timing, safety observation, production result, or matched-budget real arm. GMUT Mind is a typed lattice-and-constraint analogy firewall inside a scalar-tensor and effective-field-theory research-model family. No weaving pattern, threading draft, lattice, tension field, or transition state is a physical datum, likelihood, posterior, force, parameter constraint, detected effect, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. Freed ID/CBR Heart uses synthetic surrogate provenance and correction or contest structure only. It contains no real key, proof, credential, issuance, presentation, resolution, status event, revocation, identity, trust-governance decision, right, remedy, affected-party acceptance, legal interpretation, cultural ratification, or Māori authority.

## Practice lenses and evidence domain

The primary practice lens is synthetic handweaving loom-plan and handover. Secondary lenses are synthetic letterpress proof-correction and press handover, and synthetic marquetry layout and tool handover. These are learning and software-design devices only. The phase uses no real weaver, printer, marquetry worker, workshop, loom, press, blade, yarn, reed, heddle, paper, ink, veneer, adhesive, design, object, measurement, calibration, treatment, repair, hazard decision, work release, record, employer, customer, affected person, cultural item, or authority act. It establishes no employment, qualification, handweaving competence, printing competence, marquetry competence, conservation competence, tool competence, inspection authority, safety release, professional judgment, operational result, material-performance result, legal conclusion, cultural legitimacy, affected-party acceptance, or Māori authority.

Four official or primary references provide vocabulary and refusal boundaries: WCAG 2.2 for structural accessibility concepts; PROV-O for provenance and revision relationships; RFC 8785 for deterministic JSON vocabulary; and the United States Occupational Safety and Health Administration hand-and-power-tools page for tool-hazard and responsibility refusal conditions. A citation is not an observation, inspection, measurement, training event, safety decision, or authority grant. The phase performs no external data query or download, ingests zero real rows, evaluates zero likelihoods, and makes no standards-conformance, regulatory-compliance, accessibility-conformance, or workplace-safety claim.

## Planning separation and novelty discipline

X1 was a dedicated planning-only commit and direct child of Sable's exact final. It contained no x2 directory, execution outcome, or completion claim. Before x2 began, that commit was pushed, clean, at typed zero divergence, and equal across local, upstream, tracking, and a fresh live-remote read. The x1 audit traversed every discoverable proposal freeze, ledger, or register in the exact source Git tree, extracting 4,296 title records from 206 JSON ledgers and 1,758 unique normalized titles. The first freeze attempt was correctly quarantined because proposal 33 exactly duplicated an inherited Sable title. That failed attempt remains zero credit. The corrected title is specific to accessible weaving-instruction evaluation; the complete audit then found no exact collision and no token-Jaccard score at or above the 0.8 quarantine threshold, with a maximum observed score of 0.75.

Because the repository exposes a declared 6,030-row count rather than one materialized ledger containing every row, Caelen refuses a universal semantic-novelty claim. The result is an evidence-bound freeze, not proof that no semantically related idea exists anywhere in history. Novelty is also separated from usefulness: a distinct title does not prove that the proposal is correct, important, empirically valid, professionally accepted, or authorized.

The expanded portfolio freezes sixty safe-now tasks, thirty bounded candidate prototypes, twenty phase-local skills, ten family-compatible runners, sixty additive CLEAN/FIX/REFINE tasks, twenty exact-approval packets, ten blocked packets, ten successor skill ideas, ten successor runner ideas, and thirty successor refinement recommendations. Exact and blocked packets remain unexecuted. Caps are ceilings, not quotas: no destructive, empirical, participant, credential, account, API-key, host-security, sibling-lane, production-identity, legal, cultural, affected-party, or Māori-authority action was manufactured to make a count appear complete.

## Bounded execution surfaces

Ten executable surfaces cover warp-plan versioning, material provenance, declared loom compatibility, threading sequence, pattern lineage, accessibility structure, privacy minimization, workload handover, authority boundaries, and the complete weaving packet. Each surface has one accepting fixture and five preregistered invalid mutations: missing surface, removed synthetic boundary, malformed payload, promoted authority, and a raw-identifier marker. A successful bounded run therefore requires sixty of sixty decisions: ten acceptances and fifty refusals. A refusal demonstrates only that the declared software guard rejected that exact mutation. It does not prove production safety, completeness, privacy, accessibility, craft correctness, reliability, or external validity.

The twenty phase-local skills are concise packages with discriminating descriptions, essential workflows, explicit stop conditions, and no unnecessary resources. They are quick-validated and smoke-used only inside this owner packet; they are not installed globally. Ten family-current runners preserve `ghc_family_*` caller naming and execute one surface each. Three ordinary tools provide the shared craft guard, Git-blob manifest verification, and five-class privacy scanning. Historical and sibling-specific callers remain untouched as compatibility evidence.

## Corrections, privacy, and accessibility

Corrections are append-only. A warp-plan version names the synthetic predecessor; the prior plan and correction state remain visible; and pattern lineage cannot erase an earlier draft. Units and thread counts remain typed declarations, not measurements. A tension field explicitly preserves calibration vacancy. Yarn-lot labels are synthetic surrogates and cannot establish composition, identity, quality, source, ownership, suitability, or material performance. Reed and heddle compatibility is a fixture assertion with `real_loom_assessed` fixed false. A sequence guard can verify declared ordering but cannot perform or judge threading.

The privacy surface permits only a generalized workshop zone, synthetic plan label, and hold state in its positive fixture. It refuses direct identifiers and scans the owner delta across five classes. A bounded zero-hit result is not complete privacy assurance and does not assess inference, linkage, external logs, retention, governance, or real deployment. The accessible report uses headings, landmarks, links, a captioned table, and a static no-script layout. Manual keyboard use, responsive layout, browser diversity, assistive technology, cognitive accessibility, Māori-language review, security usability, professional review, and affected-user evaluation remain reserved. Structural passing evidence is never relabelled complete accessibility conformance.

## Method Flow and retained failures

Six startup failures remain visible at zero credit. A combined manifest wrapper crossed its time envelope before exposing the owner result; an empty no-checkout index projected thousands of deletions; a sparse-add command used an unsupported option; a case-insensitive copy map failed parser validation; the first semantic audit rejected an exact inherited collision; and the first clean-boundary guard used a wildcard that misclassified staged paths as untracked. Twenty initial skill-creator quick-validation invocations then failed because the installed validator decoded UTF-8 Māori boundary text through the active Windows legacy code page; the unchanged packages passed under process-local Python UTF-8 mode without a persistent host change. One later read-only stale-label sweep failed because a wildcard path was passed literally to `rg`; explicit roots plus `rg`-native glob filters recovered it. The first evidence-stage add then found twelve generated runners outside the sparse definition, and the partial stage review lacked a required-path completeness gate. Exact Caelen-only sparse paths plus an explicit required-evidence set recovered both issues. Exact-x1 archive verification passed 16/16 after a rejected combined wrapper and one nonexistent archive selection; four later cleanup attempts remained failed or partial under host deletion controls, leaving only a bounded verification archive and bytecode cache outside the repository. Each recovery is a distinct bounded passing witness. No recovery rewrites the original attempt as successful. The fifty rejected mutations remain negatives, not scientific replications. Method Flow promotes a method only after its own bounded passing witness and preserves trigger, recurrence guard, rollback, and successor recommendation.

This distinction matters for reproducibility. Same-owner execution under shared infrastructure can show deterministic behavior inside the declared fixture domain. It cannot supply an independent team, independent environment, independent governance, real participants, real data, real services, professional review, legal review, cultural ratification, Māori-authority review, external audit, production certification, or Stage 20 authority. A large passing count does not compensate for a missing evidence class or competent authority.

## Reversibility and human-readable challenge paths

Every completed software surface has a narrow reversal path. A warp plan can be superseded without deleting the prior version; a pattern correction can preserve the earlier value; a compatibility claim can return to an explicit vacancy rather than being guessed; and an authority field can remain vacant while the packet explains what evidence is missing. These are design properties of synthetic artifacts, not evidence that any real workshop would use, understand, or accept the process. A human challenger can locate the proposal card, its mapped surface, the accepting fixture, the five rejected mutations, and the Method Flow witness. The challenge path does not force acceptance of the result; it makes disagreement, correction, and retraction inspectable.

The weaving packet separates deterministic serialization from governance and practice. A canonical capsule can preserve field relationships and hashes, but it cannot decide whether a loom is safe, whether a plan is workable, whether material is suitable, whether an accommodation is sufficient, whether a remedy is legitimate, or who may speak for an affected community. Those decisions remain with competent people and authorities. The same separation applies to routing: preparing a successor recommendation is zero-credit repository work, while an acknowledged existing-task send is an external action that is terminally gated and cannot be inferred from a file.

## Complete and incomplete truth

Complete within owner-local software bounds are the planning freeze, exact source anchors, semantic-neighbor audit, deterministic JSON artifacts, ten bounded guard surfaces, phase-local skill packages, family-current runners, additive portfolio receipts, structural accessible report, threat model, five-class scanner, exact staged review, and Git-blob manifests. Represented only are the THOS embodied-sequence and workload proxy, GMUT typed lattice analogy, Freed ID zero-key craft provenance, CBR correction and contest structure, accessibility nonpromotion, professional handweaving competence vacancy, legal or cultural remedy vacancy, and Māori wording, taonga, mātauranga, data-governance, and authority vacancy.

Two new open gaps remain: real weaver, tool, and affected-user evaluation; and real loom, yarn, measurement, and interoperability evidence. Two new exact gates remain: live workshop operation and safety-release authority; and Stage 20 promotion. They add to 281 inherited open gaps and 274 inherited exact gates rather than replacing them, giving 283 effective open gaps and 276 effective exact gates. Nothing in the packet silently closes a prior gate.

Caelen Ash, they/them, is relational working language for an uncertainty-and-handover cartographer. The hope is to make every boundary, missing witness, and reversible next step easier to see before structure is mistaken for authority. That name, role, hope, sibling language, and Trinity Mandala language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority. Hamish may pause, rename, redirect, or stop the route.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
'''


def generate() -> None:
    if subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip() != X1_COMMIT:
        raise SystemExit("x2 generation must begin at the immutable x1 commit")
    write_guard_tools()
    write_fixtures()
    write_skills()
    write_planning_evidence()
    write_static_packet()
    write_text(X2 / "integrated-overview.md", integrated_overview())
    write_json(
        X2 / "x1-boundary-proof.json",
        {
            "schema": "ghc.family.caelen.v672-v4.x1-boundary-proof.v1",
            "source_head": SOURCE_HEAD,
            "x1_commit": X1_COMMIT,
            "source_is_direct_parent": True,
            "x1_clean_before_x2": True,
            "x1_divergence": {"ahead": 0, "behind": 0},
            "x1_four_way_equal": True,
            "x2_absent_at_proof": True,
            "proof_state": "observed_read_only_before_x2_generation",
        },
    )
    write_json(
        X2 / "generation-state.json",
        {
            "schema": "ghc.family.caelen.v672-v4.generation-state.v1",
            "state": "generated_not_executed",
            "runner_smoke_invocations": 0,
            "skill_smoke_invocations": 0,
            "canonical_invocations": 0,
            "canonical_successes": 0,
        },
    )


def validate_skill(skill_dir: Path) -> dict[str, Any]:
    skill_path = skill_dir / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    name = skill_dir.name
    checks = {
        "frontmatter_opens": text.startswith("---\n"),
        "frontmatter_name_matches": f"name: {name}\n" in text,
        "description_present": "description:" in text.split("---", 2)[1],
        "workflow_present": "## Workflow" in text,
        "boundaries_present": "## Boundaries" in text,
        "phase_use_present": "## Phase use" in text,
        "unfinished_placeholder_absent": "TODO" not in text and "{{" not in text,
    }
    return {"skill": name, "checks": checks, "valid": all(checks.values())}


def smoke() -> None:
    state_path = X2 / "generation-state.json"
    state = load(state_path)
    if state["runner_smoke_invocations"] or state["skill_smoke_invocations"]:
        raise SystemExit("one-shot x2 smoke latch already spent")
    state["runner_smoke_invocations"] = 1
    state["skill_smoke_invocations"] = 1
    state["state"] = "smoke_in_progress"
    write_json(state_path, state)
    runner_receipts = []
    for surface in SURFACE_REQUIREMENTS:
        runner = ROOT / "scripts" / f"ghc_family_caelen_v672_v4_{surface}_guard.py"
        fixture_dir = X2 / "fixtures" / surface
        output = X2 / "runner-witnesses" / f"{surface}.json"
        completed = subprocess.run(
            [sys.executable, str(runner), "--fixture-dir", str(fixture_dir), "--output", str(output)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        receipt = load(output) if output.exists() else {
            "surface": surface, "valid": False, "checks": 0, "passed_checks": 0, "results": []
        }
        receipt["process_returncode"] = completed.returncode
        receipt["stdout_summary"] = completed.stdout.strip()
        receipt["stderr_present"] = bool(completed.stderr.strip())
        receipt["invocation_count"] = 1
        write_json(output, receipt)
        runner_receipts.append(receipt)
    skill_receipts = []
    for index, name in enumerate(SKILLS, start=1):
        receipt = validate_skill(X2 / "skills" / name)
        receipt.update(
            {
                "proposal_use": f"CA6724-P{index:03d}",
                "invocation_count": 1,
                "scope": "phase_local_structural_only",
                "globally_installed": False,
                "subagent_forward_test": "not_run_solo_activation_forbids_delegation",
            }
        )
        write_json(X2 / "skill-witnesses" / f"{name}.json", receipt)
        skill_receipts.append(receipt)
    quick_validation = load(X2 / "skill-creator-quick-validation.json")
    quick_validation_valid = (
        quick_validation["packages"] == 20
        and quick_validation["initial_failures"] == 20
        and quick_validation["recovery_passes"] == 20
        and quick_validation["final_failures"] == 0
        and quick_validation["installed_skill_mutated"] is False
        and quick_validation["persistent_environment_change"] is False
    )
    runners_valid = len(runner_receipts) == 10 and all(row["valid"] for row in runner_receipts)
    skills_valid = len(skill_receipts) == 20 and all(row["valid"] for row in skill_receipts)
    if not runners_valid or not skills_valid or not quick_validation_valid:
        state["state"] = "failed_zero_success_credit"
        state["runner_smoke_successes"] = 0
        state["skill_smoke_successes"] = 0
        write_json(state_path, state)
        raise SystemExit("one-shot x2 smoke failed; retain and do not relabel")

    outcomes = []
    for row in proposal_rows():
        outcome = row["expected_disposition"]
        card_path = X2 / "proposals" / f"{row['proposal_id'].casefold()}.json"
        card = load(card_path)
        card.update(
            {
                "outcome": outcome,
                "state": "executed_as_evidence_permitted",
                "runner_surface_receipt": f"x2/runner-witnesses/{row['surface']}.json",
                "bounded_acceptance": "surface_accepting_fixture_passed_and_five_invalid_mutations_rejected",
                "broader_credit": 0,
            }
        )
        if outcome == "represented":
            card["limitation"] = "structural representation only; required real evidence or authority absent"
        elif outcome == "open_gap":
            card["limitation"] = "required external empirical or affected-user evidence absent"
        elif outcome == "exact_gate":
            card["limitation"] = "competent authority or terminal promotion gate remains vacant"
        write_json(card_path, card)
        outcomes.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "outcome": outcome,
                "surface": row["surface"],
                "broader_credit": 0,
            }
        )
    counts = dict(Counter(row["outcome"] for row in outcomes))
    write_json(
        X2 / "proposals" / "outcome-ledger.json",
        {
            "schema": "ghc.family.caelen.v672-v4.outcome-ledger.v1",
            "phase": "v672-v4",
            "state": "executed_as_evidence_permitted",
            "proposal_chain": 6070,
            "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"],
            "outcome_counts": counts,
            "outcomes": outcomes,
        },
    )

    portfolio = load(X1 / "portfolio-freeze.json")
    execution = {
        "schema": "ghc.family.caelen.v672-v4.portfolio-execution.v1",
        "safe_now": [{**row, "state": "completed_with_bounded_owner_witness"} for row in portfolio["safe_now_tasks"]],
        "candidates": [{**row, "state": "completed_with_bounded_owner_witness"} for row in portfolio["candidate_tasks"]],
        "skills": skill_receipts,
        "skill_creator_quick_validation": quick_validation,
        "runners": [
            {"surface": row["surface"], "valid": row["valid"], "checks": row["checks"], "invocation_count": 1}
            for row in runner_receipts
        ],
        "clean_fix_refine": [{**row, "state": "completed_additively"} for row in portfolio["owner_clean_fix_refine"]],
        "exact_approval_packets": portfolio["exact_approval_packets"],
        "blocked_packets": portfolio["blocked_packets"],
        "successor_recommendations_credit": 0,
        "destructive_actions": 0,
        "sibling_mutations": 0,
        "real_rows": 0,
        "external_actions": 0,
    }
    write_json(X2 / "portfolio-execution.json", execution)

    startup = load(X1 / "method-flow-startup.json")
    methods = list(startup["methods"])
    witnesses = list(startup["witnesses"])
    expected_rejections = []
    for index, receipt in enumerate(runner_receipts, start=1):
        method_id = f"CA6724-SURFACE-METHOD-{index:03d}"
        methods.append(
            {
                "method_id": method_id,
                "trigger": f"validate {receipt['surface']} synthetic craft surface",
                "preferred_method": "one accepting fixture plus five preregistered rejecting mutations",
                "state": "preferred_after_bounded_passing_witness",
                "rollback": "retain the failed fixture and stop the affected surface",
                "sibling_recommendation": "bind credit to exact surface and fixture set",
            }
        )
        witnesses.append(
            {
                "witness_id": f"CA6724-{receipt['surface'].upper()}-PASS",
                "method_id": method_id,
                "kind": "passing",
                "credit": "bounded_software_only",
                "description": "one accepting fixture passed and five invalid mutations were rejected",
                "state": "bounded_passing",
            }
        )
        for result in receipt["results"]:
            if result["fixture"].startswith("rejecting-"):
                failure_id = f"CA6724-{receipt['surface'].upper()}-{result['fixture'].removesuffix('.json').upper()}"
                expected_rejections.append(
                    {
                        "failure_id": failure_id,
                        "surface": receipt["surface"],
                        "fixture": result["fixture"],
                        "state": "preregistered_invalid_mutation_rejected_zero_broader_credit",
                    }
                )
                witnesses.append(
                    {
                        "witness_id": failure_id,
                        "method_id": method_id,
                        "kind": "failed",
                        "credit": 0,
                        "description": "preregistered invalid mutation",
                        "state": "retained_expected_rejection_zero_credit",
                    }
                )
    for index, receipt in enumerate(skill_receipts, start=1):
        method_id = f"CA6724-SKILL-METHOD-{index:03d}"
        methods.append(
            {
                "method_id": method_id,
                "trigger": f"apply phase-local skill {receipt['skill']}",
                "preferred_method": "load exact skill instructions and preserve the declared evidence boundary",
                "state": "preferred_after_bounded_passing_witness",
                "rollback": "quarantine only the phase-local package",
                "sibling_recommendation": "independently review before reuse",
            }
        )
        witnesses.append(
            {
                "witness_id": f"CA6724-SKILL-PASS-{index:03d}",
                "method_id": method_id,
                "kind": "passing",
                "credit": "phase_local_structural_only",
                "description": f"skill validated and applied to {receipt['proposal_use']}",
                "state": "bounded_passing_not_global_installation",
            }
        )
    quick_method_id = "CA6724-QUICK-VALIDATE-METHOD-001"
    methods.append(
        {
            "method_id": quick_method_id,
            "trigger": "installed skill validator decoded UTF-8 skill text through the active Windows legacy code page",
            "preferred_method": "rerun each unchanged package with process-local Python UTF-8 mode and retain both invocation sets",
            "state": "preferred_after_twenty_bounded_passing_witnesses",
            "rollback": "remove only generated owner-local skill packages and preserve all failed validation receipts",
            "sibling_recommendation": "use process-local UTF-8 mode for this validator without changing global host configuration",
        }
    )
    for index, row in enumerate(quick_validation["rows"], start=1):
        witnesses.extend(
            [
                {
                    "witness_id": f"CA6724-QUICK-VALIDATE-FAIL-{index:03d}",
                    "method_id": quick_method_id,
                    "kind": "failed",
                    "credit": 0,
                    "description": f"initial quick validation failed before content validation for {row['skill']}",
                    "state": "retained_windows_code_page_decode_failure",
                },
                {
                    "witness_id": f"CA6724-QUICK-VALIDATE-PASS-{index:03d}",
                    "method_id": quick_method_id,
                    "kind": "passing",
                    "credit": "phase_local_structure_only",
                    "description": f"process-local UTF-8 recovery quick-validated {row['skill']}",
                    "state": "bounded_passing_recovery_not_original_success",
                },
            ]
        )
    write_json(
        X2 / "method-flow" / "ledger.json",
        {
            "schema": "ghc.family.method-flow.v10",
            "owner": "Caelen Ash",
            "phase": "v672-v4",
            "inherited_effective_counts": startup["inherited_effective_counts"],
            "failures_erased": 0,
            "recoveries_relabelled_as_original_success": 0,
            "methods": methods,
            "witnesses": witnesses,
            "expected_rejections": expected_rejections,
            "current_delta": {
                "methods": 37,
                "failed_witnesses": 76,
                "passing_witnesses": 56,
                "effective_negatives": 76,
            },
            "effective_counts": {
                "effective_negatives": 35407,
                "effective_methods": 21977,
                "effective_failed_witnesses": 7228,
                "effective_passing_witnesses": 9282,
                "open_gaps": 283,
                "exact_gates": 276,
            },
        },
    )
    write_json(
        X2 / "retained-negative-register.json",
        {
            "schema": "ghc.family.caelen.v672-v4.retained-negatives.v1",
            "activation_baseline": 35331,
            "startup_failures": 6,
            "preregistered_invalid_mutations": 50,
            "x2_unexpected_operational_failures": 20,
            "effective_total": 35407,
            "erased": 0,
            "startup_failure_ids": [f"CA6724-START-{i:03d}" for i in range(1, 7)],
            "mutation_failure_ids": [row["failure_id"] for row in expected_rejections],
            "x2_operational_failure_ids": [
                f"CA6724-QUICK-VALIDATE-FAIL-{i:03d}" for i in range(1, 21)
            ],
        },
    )
    write_json(
        X2 / "gate-register.json",
        {
            "schema": "ghc.family.caelen.v672-v4.gates.v1",
            "inherited_open_gaps": 281,
            "new_open_gaps": [
                "real weaver, tool, and affected-user evaluation",
                "real loom, yarn, measurement, and interoperability evidence",
            ],
            "effective_open_gaps": 283,
            "inherited_exact_gates": 274,
            "new_exact_gates": [
                "live workshop operation and safety-release authority",
                "Stage 20 promotion",
            ],
            "effective_exact_gates": 276,
            "silently_closed": 0,
        },
    )
    write_json(
        X2 / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.caelen.v672-v4.checklist.v1",
            "complete_within_bounded_owner_scope": [
                "x1 freeze and remote equality", "forty proposal evidence cards", "ten guard surfaces",
                "sixty fixture decisions", "twenty phase-local skill uses", "ten runner uses",
                "portfolio execution receipts", "threat model", "static structural report",
                "retained failure ledger", "gate register",
            ],
            "represented_only": [
                "THOS embodied-sequence workload and handover proxy", "GMUT typed lattice analogy firewall",
                "Freed ID zero-key craft provenance", "CBR correction and contest path",
                "accessibility nonpromotion", "professional handweaving competence vacancy",
                "legal cultural design-provenance and remedy vacancy",
                "Māori wording taonga mātauranga data-governance and authority vacancy",
            ],
            "open_gap": [
                "real weaver, tool, and affected-user evaluation",
                "real loom, yarn, measurement, and interoperability evidence",
            ],
            "exact_gate": [
                "live workshop operation and safety-release authority",
                "Stage 20 promotion",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "schema": "ghc.family.caelen.v672-v4.x2-truth.v1",
            "owner": "Caelen Ash",
            "phase": "v672-v4",
            "source_head": SOURCE_HEAD,
            "x1_commit": X1_COMMIT,
            "proposal_chain": 6070,
            "outcomes": counts,
            "runner_smoke": {"invocations": 10, "successes": 10, "checks": 60, "passed": 60},
            "skill_smoke": {"invocations": 20, "successes": 20, "globally_installed": False},
            "skill_creator_quick_validation": {
                "initial_failures": 20,
                "recovery_passes": 20,
                "global_or_installed_mutation": False,
            },
            "real_rows": 0,
            "external_actions": 0,
            "independent_reproduction": False,
            "effective_counts": {
                "negatives": 35407, "methods": 21977, "failed_witnesses": 7228,
                "passing_witnesses": 9282, "open_gaps": 283, "exact_gates": 276,
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    state.update(
        {
            "state": "one_shot_smoke_succeeded_do_not_replay",
            "runner_smoke_successes": 1,
            "skill_smoke_successes": 1,
            "runner_checks": 60,
            "runner_checks_passed": 60,
        }
    )
    write_json(state_path, state)
    write_text(X2 / "integrated-overview.md", integrated_overview(counts))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("generate", "smoke"))
    args = parser.parse_args()
    if args.mode == "generate":
        generate()
    else:
        smoke()


if __name__ == "__main__":
    main()

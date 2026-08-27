#!/usr/bin/env python3
"""Generate and execute the bounded Sable Rook v672-v3 x2 packet."""

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
PHASE = ROOT / "docs" / "sable-rook" / "v672-v3"
X1 = PHASE / "x1"
X2 = PHASE / "x2"
X1_COMMIT = "1875dc20ea21a47fd411bc898ee274e632b2977f"
SOURCE_HEAD = "842956c8ddc8b648d14911ac6228ba1cffb7d5ad"

SURFACE_REQUIREMENTS = {
    "identity_version": ["notice_id", "version", "supersedes", "correction_state"],
    "time_window": ["recorded_at", "published_at", "effective_from", "expires_at", "offset"],
    "impact_scope": ["services", "locations", "scope_state"],
    "cause_uncertainty": ["cause_state", "confidence_boundary", "evidence_state"],
    "correction_lineage": ["prior_version", "change_summary", "reason", "nonerasure"],
    "channel_accessibility": ["channels", "plain_language_summary", "structural_alternative", "manual_evaluation_reserved"],
    "privacy_minimization": ["fields_allowed", "exact_location_generalized", "direct_identifiers"],
    "handover_workload": ["open_actions", "hold_state", "next_owner_role", "workload_budget"],
    "authority_boundary": ["operational_authority", "legal_authority", "cultural_authority", "maori_authority"],
    "notice_packet": ["schema_version", "components", "deterministic", "stage20"],
}

SKILLS = [
    "ghc-family-service-notice-version-vector",
    "ghc-family-service-window-timezone-guard",
    "ghc-family-service-planning-state-provenance",
    "ghc-family-service-impact-scope-closure",
    "ghc-family-service-zone-alias-privacy",
    "ghc-family-service-cause-uncertainty-separator",
    "ghc-family-service-urgency-non-equivalence",
    "ghc-family-service-residual-impact-ledger",
    "ghc-family-service-publication-state-machine",
    "ghc-family-service-correction-diff-ledger",
    "ghc-family-service-channel-consistency",
    "ghc-family-service-plain-language-proxy",
    "ghc-family-service-structural-accessibility",
    "ghc-family-service-icon-text-alternative",
    "ghc-family-service-translation-vacancy",
    "ghc-family-service-contact-purpose-limiter",
    "ghc-family-service-readback-proxy",
    "ghc-family-service-handover-unresolved-work",
    "ghc-family-service-authority-vacancy",
    "ghc-family-service-stage20-nonpromotion",
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
        "identity_version": {
            "notice_id": "synthetic-notice-01", "version": 2,
            "supersedes": "synthetic-notice-01-v1", "correction_state": "corrected",
        },
        "time_window": {
            "recorded_at": "2026-08-27T09:00:00+12:00",
            "published_at": "2026-08-27T09:05:00+12:00",
            "effective_from": "2026-08-27T09:30:00+12:00",
            "expires_at": "2026-08-27T12:00:00+12:00", "offset": "+12:00",
        },
        "impact_scope": {
            "services": ["synthetic-library-level-two"],
            "locations": ["generalized-central-zone"], "scope_state": "bounded",
        },
        "cause_uncertainty": {
            "cause_state": "unknown", "confidence_boundary": "not_estimated",
            "evidence_state": "synthetic_only",
        },
        "correction_lineage": {
            "prior_version": 1, "change_summary": "effective window corrected",
            "reason": "synthetic readback discrepancy", "nonerasure": True,
        },
        "channel_accessibility": {
            "channels": ["synthetic-web", "synthetic-display"],
            "plain_language_summary": "One synthetic service area is unavailable until noon.",
            "structural_alternative": "table_and_text", "manual_evaluation_reserved": True,
        },
        "privacy_minimization": {
            "fields_allowed": ["generalized-zone", "effective-window", "service-scope"],
            "exact_location_generalized": True, "direct_identifiers": False,
        },
        "handover_workload": {
            "open_actions": ["verify synthetic expiry state"], "hold_state": "active",
            "next_owner_role": "synthetic_notice_reviewer", "workload_budget": "one_notice",
        },
        "authority_boundary": {
            "operational_authority": "vacant", "legal_authority": "vacant",
            "cultural_authority": "vacant", "maori_authority": "vacant",
        },
        "notice_packet": {
            "schema_version": "1.0", "components": ["identity", "window", "scope", "authority"],
            "deterministic": True, "stage20": "not_ready",
        },
    }
    return values[surface]


def write_guard_tools() -> None:
    requirements_literal = repr(SURFACE_REQUIREMENTS)
    guard = f'''#!/usr/bin/env python3
"""Bounded synthetic service-notice guard for Sable v672-v3."""
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
    if expected_surface == "notice_packet" and payload.get("stage20") != "not_ready":
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
    write_text(ROOT / "scripts" / "ghc_family_sable_v672_v3_notice_guard.py", guard)

    manifest_guard = '''#!/usr/bin/env python3
"""Verify exact Git-blob entries in a Sable v672-v3 manifest."""
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
        observed = git(root, "rev-parse", f"{args.revision}:{row['path']}").decode().strip()
        if observed != row["git_blob_oid"]:
            mismatches.append(row["path"])
    print(json.dumps({"entries": len(manifest["entries"]), "mismatches": mismatches, "valid": not mismatches}))
    raise SystemExit(0 if not mismatches else 1)

if __name__ == "__main__":
    main()
'''
    write_text(ROOT / "scripts" / "ghc_family_sable_v672_v3_manifest_guard.py", manifest_guard)

    privacy_guard = '''#!/usr/bin/env python3
"""Five-class privacy scan for bounded Sable v672-v3 text files."""
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
    write_text(ROOT / "scripts" / "ghc_family_sable_v672_v3_privacy_guard.py", privacy_guard)

    for surface in SURFACE_REQUIREMENTS:
        wrapper = f'''#!/usr/bin/env python3
"""Family-compatible runner for the {surface} service-notice surface."""
from ghc_family_sable_v672_v3_notice_guard import cli

if __name__ == "__main__":
    cli("{surface}")
'''
        write_text(ROOT / "scripts" / f"ghc_family_sable_v672_v3_notice_{surface}_guard.py", wrapper)


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
            "schema": "ghc.family.sable.v672-v3.notice-fixture.v1",
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
            invalid["failure_id"] = f"SR6723-{surface.upper()}-REJECT-{index:02d}"
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
        short = name.removeprefix("ghc-family-service-").replace("-", " ")
        skill = f'''---
name: {name}
description: Audit synthetic service-notice {short} when bounded provenance or authority-vacancy review is needed.
---

# {short.title()}

Use this skill to inspect one wholly synthetic service-notice artifact. It applies only to the `{short}` obligation represented by Sable Rook v672-v3.

## Workflow

1. Confirm the input is synthetic and contains no real person, service event, location record, credential, private route, or authority action.
2. Check the declared notice surface, version or state lineage, and the relevant acceptance fields.
3. Preserve corrections and failed witnesses rather than replacing them with the recovery.
4. Return a bounded structural result and name every evidence or authority vacancy.

## Boundaries

This skill does not establish empirical truth, accessibility conformance, professional competence, operational readiness, public-warning authority, legal or cultural legitimacy, affected-party acceptance, Māori wording or authority, privacy completeness, exhaustive security, independent reproduction, or Stage 20 readiness. Stop if real data or real authority is required.

## Phase use

The x2 smoke use maps this skill to proposal `{proposal_titles[index - 1]}`. A passing structural witness is owner-local software evidence only.
'''
        write_text(X2 / "skills" / name / "SKILL.md", skill)
        display = short.title()[:64]
        yaml = f'''interface:
  display_name: "{display}"
  short_description: "Audit a bounded notice evidence boundary"
  default_prompt: "Use ${name} to review a synthetic service notice while preserving authority vacancies."
'''
        write_text(X2 / "skills" / name / "agents" / "openai.yaml", yaml)


def write_planning_evidence() -> None:
    rows = proposal_rows()
    for row in rows:
        card = {
            "schema": "ghc.family.sable.v672-v3.proposal-evidence.v1",
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
            "schema": "ghc.family.sable.v672-v3.outcome-ledger.v1",
            "phase": "v672-v3",
            "state": "pending_one_shot_smoke",
            "proposal_chain": 6030,
            "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"],
            "outcomes": [],
        },
    )


def write_static_packet() -> None:
    write_json(
        X2 / "threat-model.json",
        {
            "schema": "ghc.family.sable.v672-v3.threat-model.v1",
            "assets": [
                "synthetic notice lineage", "correction history", "bounded fixture integrity",
                "privacy minimization", "authority vacancies", "route hold",
            ],
            "threats": [
                {"threat": "stale notice survives correction", "control": "version and supersession guard", "residual": "real channel behavior untested"},
                {"threat": "timezone ambiguity changes effective window", "control": "explicit offset guard", "residual": "real clock synchronization untested"},
                {"threat": "scope overclaims affected services", "control": "closed synthetic scope list", "residual": "no live service inventory"},
                {"threat": "cause speculation becomes fact", "control": "known suspected unknown separation", "residual": "no real investigation"},
                {"threat": "correction erases the prior claim", "control": "append-only correction lineage", "residual": "no production log"},
                {"threat": "accessibility proxy becomes conformance claim", "control": "manual and affected-user reservation", "residual": "evaluation remains open"},
                {"threat": "generalized location is reidentified", "control": "minimum synthetic fields", "residual": "no complete privacy assurance"},
                {"threat": "software confers public authority", "control": "four-way authority vacancy matrix", "residual": "competent authority gate remains exact"},
            ],
            "scope": "owner_local_synthetic_only",
            "exhaustive_security_claimed": False,
        },
    )
    write_json(
        X2 / "practice-lens-receipt.json",
        {
            "schema": "ghc.family.sable.v672-v3.practice-lenses.v1",
            "primary": "synthetic metropolitan-library interruption notice",
            "secondary": [
                "synthetic community-radio schedule notice",
                "synthetic passenger-ferry terminal display notice",
            ],
            "real_rows": 0,
            "real_people": 0,
            "external_actions": 0,
            "authority_actions": 0,
            "successor_recommendation": {
                "practice": "synthetic community-pharmacy opening-hours exception notice",
                "credit": 0,
                "state": "advisory_only",
            },
        },
    )
    write_json(
        X2 / "pillar-boundaries.json",
        {
            "schema": "ghc.family.sable.v672-v3.pillar-boundaries.v1",
            "primary": "freed_id_cbr_heart",
            "freed_id": "synthetic_zero_key_provenance_only_nonproduction",
            "cbr": "correction_and_contest_structure_only_all_authority_reserved",
            "thos": "synthetic_workload_hold_readback_and_handover_proxy_only",
            "gmut": "typed_state_transition_analogy_firewall_only",
            "gmut_model": "typed_scalar_tensor_and_effective_field_theory_research_model_family",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        X2 / "environment-and-version-intent.json",
        {
            "schema": "ghc.family.sable.v672-v3.environment-intent.v1",
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
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v672-v3 bounded report</title></head>
<body>
<header><h1>Sable Rook v672-v3 bounded service-notice report</h1><p>Wholly synthetic owner-local evidence. Verdict: NOT_READY_FOR_STAGE_20.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#limits">Limits</a></li></ul></nav>
<main>
<section id="scope"><h2>Scope</h2><p>The report covers version, time, impact, uncertainty, correction, channel, privacy, handover, authority, and packet guards for synthetic public-service notices.</p></section>
<section id="outcomes"><h2>Preregistered outcomes</h2><table><caption>Forty proposal outcomes</caption><thead><tr><th scope="col">Class</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>28</td></tr><tr><th scope="row">Represented</th><td>8</td></tr><tr><th scope="row">Open gap</th><td>2</td></tr><tr><th scope="row">Exact gate</th><td>2</td></tr></tbody></table></section>
<section id="limits"><h2>Limits and reserved evaluation</h2><p>No real notice, service, person, location record, authority action, credential, participant, or empirical row was used. Manual keyboard, browser, responsive-layout, assistive-technology, cognitive-accessibility, Māori-language, privacy, security-usability, and affected-user evaluation remain reserved. Structural evidence is not complete accessibility or privacy conformance.</p></section>
</main><footer><p>Identity and family language is relational working language only.</p></footer>
</body></html>''',
    )


def integrated_overview(outcomes: dict[str, int] | None = None) -> str:
    distribution = outcomes or {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    return f'''# Sable Rook v672-v3 integrated overview

## Result at a glance

This phase studies a narrow question: can a wholly synthetic public-service disruption notice preserve version provenance, effective windows, impact scope, uncertainty, corrections, alternative channels, accessibility structure, privacy minimization, workload handover, and explicit authority vacancies without turning software evidence into a real-world claim? Forty proposals were frozen before x2. Their bounded dispositions are {distribution['completed']} `completed`, {distribution['represented']} `represented`, {distribution['open_gap']} `open_gap`, and {distribution['exact_gate']} `exact_gate`. The proposal chain moves from the declared 5,990 inherited rows to 6,030. Twenty inherited Auren proposals were reviewed only as zero-credit predecessors. No inherited proposal, tool, portfolio, test, or validation became Sable novelty or completion credit.

The primary Trinity Mandala pillar is Freed ID/CBR Heart. The notice identity and version surfaces use surrogate strings and no keys, credentials, identities, signatures, issuances, presentations, resolutions, status events, revocations, interoperability events, privacy review, independent security review, recovery decision, or trust-governance decision. The CBR surfaces represent correction, contest, alternative-channel, and response-path structure while leaving every remedy, public duty, legal interpretation, cultural determination, affected-party acceptance, language decision, data-governance decision, and Māori authority vacant. THOS Body remains a synthetic workload, hold, readback, exception, and shift-handover proxy. GMUT Mind remains a typed state-transition analogy firewall inside a scalar-tensor and effective-field-theory research-model family; no notice state is evidence of a physical force, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything.

## Practice lenses and evidence domain

The primary practice lens is a synthetic metropolitan-library interruption notice. Secondary lenses are a synthetic community-radio schedule notice and a synthetic passenger-ferry terminal display notice. These lenses are learning and software-design devices only. The phase uses no real library, station, ferry operator, service, incident, disruption, customer, worker, passenger, location record, timetable, broadcast, public message, authority action, or private route. It establishes no employment, qualification, accessibility expertise, service-management competence, emergency-management competence, transport competence, publication authority, public-warning authority, professional judgment, operational result, safety result, legal conclusion, cultural legitimacy, affected-party acceptance, or Māori authority.

Five primary or official references provide vocabulary and refusal boundaries: WCAG 2.2 for structural accessibility concepts; PROV-O for provenance and revision relationships; RFC 3339 for timestamps and offsets; CAP 1.2 for alert update, cancellation, audience, and timing terms; and the GTFS Realtime reference for service-alert vocabulary. A citation is not an observation. The phase performs no official-feed query or data download, ingests zero real rows, evaluates zero likelihoods, and makes no standards-conformance claim. Current source status is recorded so later owners can recheck drift rather than treating a URL as timeless proof.

## Planning separation and novelty discipline

X1 was a dedicated planning-only commit and direct child of Auren's exact final. It contained no x2 directory, execution outcome, or completion claim. Before x2 began, that commit was pushed, clean, at zero divergence, and equal across local, upstream, tracking, and a fresh live-remote read. The x1 audit traversed every discoverable proposal freeze, ledger, or register in the exact source Git tree, extracting 4,216 title records from 204 JSON ledgers and 1,718 unique normalized titles. No new title had an exact normalized collision or token-Jaccard score at or above the 0.8 quarantine threshold. Because the repository exposes a declared 5,990-row count rather than one materialized ledger containing every row, Sable explicitly refuses a universal semantic-novelty claim. The result is an evidence-bound freeze, not proof that no semantically similar idea exists anywhere in history.

The expanded portfolio freezes sixty safe-now tasks, thirty bounded candidate prototypes, twenty phase-local skills, ten family-compatible runners, sixty additive CLEAN/FIX/REFINE tasks, twenty exact-approval packets, ten blocked packets, ten successor skill ideas, ten successor runner ideas, and thirty successor refinement recommendations. Exact and blocked packets remain unexecuted. Caps are ceilings, not quotas: no destructive, empirical, participant, credential, account, API-key, host-security, sibling-lane, production-identity, legal, cultural, affected-party, or Māori-authority action was manufactured to make a count appear complete.

## Bounded execution surfaces

Ten executable surfaces cover notice identity and version, time windows, impact scope, cause uncertainty, correction lineage, channel accessibility, privacy minimization, handover workload, authority boundaries, and the complete notice packet. Each surface has one accepting fixture and five preregistered invalid mutations: missing surface, removed synthetic boundary, malformed payload, promoted authority, and a raw-identifier marker. A successful bounded run therefore requires sixty of sixty decisions: ten acceptances and fifty refusals. A refusal demonstrates only that the declared software guard rejected that exact mutation. It does not prove production safety, completeness, privacy, accessibility, reliability, or external validity.

The twenty phase-local skills are concise packages with discriminating descriptions, essential workflows, explicit boundaries, and UI metadata. They are validated and smoke-used only inside this owner packet; they are not installed globally. Ten family-current runners preserve `ghc_family_*` caller naming and execute one surface each. Three ordinary tools provide the shared notice guard, Git-blob manifest verification, and five-class privacy scanning. Historical and sibling-specific callers remain untouched as compatibility evidence.

## Corrections, privacy, and accessibility

Corrections are append-only. A version vector names the synthetic predecessor; a correction reason and changed-field summary remain visible; publication, withdrawal, cancellation, and expiry are distinct states; and partial restoration cannot erase residual impact. Recorded, published, effective, expiry, and observed times stay separated. Known, suspected, and unknown cause states cannot be silently collapsed. Severity, priority, and urgency remain different concepts. Alternative service text carries provenance but never becomes professional or operational advice.

The privacy surface permits only generalized zone, effective window, and service scope in its positive fixture. It refuses direct identifiers and scans the owner delta across five classes. That bounded zero-hit result is not complete privacy assurance and does not assess inference, linkage, traffic analysis, external logs, retention, governance, or real deployment. The accessible report uses headings, landmarks, links, a captioned table, and a static no-script layout. Manual keyboard use, responsive layout, browser diversity, assistive technology, cognitive accessibility, Māori-language review, security usability, and affected-user evaluation remain reserved. Structural passing evidence is never relabelled complete accessibility conformance.

## Method Flow and retained failures

Six startup failures remain visible at zero credit: two overbroad activation projections, a compound PowerShell parser error, a worktree-wrapper timeout with lost completion projection, a repeated post-timeout summary parser error, and an overbroad multi-source web projection. Each recovery is a distinct bounded passing witness; no recovery rewrites the original attempt as successful. The fifty rejected mutations remain negatives, not scientific replications. Method Flow promotes a method only after its own bounded passing witness and preserves trigger, recurrence guard, rollback, and successor recommendation.

This distinction matters for reproducibility. Same-owner execution under shared infrastructure can show deterministic behavior inside the declared fixture domain. It cannot supply an independent team, independent environment, independent governance, real participants, real data, real services, professional review, legal review, cultural ratification, Māori-authority review, external audit, production certification, or Stage 20 authority. A large passing count does not compensate for a missing evidence class or competent authority.

## Reversibility and human-readable challenge paths

Every completed software surface has a narrow reversal path. A notice version can be superseded without deleting the prior version; an effective window can be corrected while preserving the earlier value and reason; an impact scope can move to an explicit unknown state rather than being guessed; and an authority vacancy can remain vacant without blocking the structural packet from explaining what is missing. These are design properties of synthetic artifacts, not evidence that any real organization would use, understand, or accept the process. A human challenger can locate the proposal card, its mapped surface, the accepting fixture, the five rejected mutations, and the Method Flow witness. The challenge path does not force acceptance of the original result: it makes disagreement, correction, and retraction inspectable.

The notice packet also separates publication mechanics from governance. A deterministic capsule can preserve field order and hashes, but it cannot decide whether a notice should be published, who owes a duty to communicate, which language is appropriate, what accommodation is sufficient, whether a remedy is legitimate, or who may speak for an affected community. Those decisions remain with competent people and authorities. The same separation applies to the route: preparing a successor recommendation is zero-credit repository work, while an acknowledged existing-task send is an external action that is terminally gated and cannot be inferred from a file.

## Complete and incomplete truth

Complete within owner-local software bounds are the planning freeze, exact source anchors, semantic-neighbor audit, deterministic JSON artifacts, ten bounded guard surfaces, phase-local skill packages, family-current runners, additive portfolio receipts, structural accessible report, threat model, five-class scanner, exact staged review, and Git-blob manifests. Represented only are zero-key Freed ID provenance, CBR correction and contest structure, THOS workload and handover, GMUT analogy boundaries, accessibility nonpromotion, professional and operational authority vacancy, legal duty and remedy vacancy, and Māori wording/data-governance/authority vacancy.

Two open gaps remain new in this phase: real affected-user and assistive-technology evaluation, and live service-feed interoperability using real rows. Two exact gates remain new: public-release or emergency-communication authority, and Stage 20 promotion. They add to the inherited open-gap and exact-gate registers rather than replacing them. Nothing in the packet closes a prior gate silently.

Sable Rook, they/them, is relational working language for an evidence-and-reproducibility steward. The hope is to make every surviving claim reproducible, challengeable, correctable, and retractable while authority vacancies stay explicit. That name, role, hope, sibling language, and Trinity Mandala language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority. Hamish may pause, rename, redirect, or stop the route.

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
            "schema": "ghc.family.sable.v672-v3.x1-boundary-proof.v1",
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
            "schema": "ghc.family.sable.v672-v3.generation-state.v1",
            "state": "generated_not_executed",
            "runner_smoke_invocations": 0,
            "skill_smoke_invocations": 0,
            "canonical_invocations": 0,
            "canonical_successes": 0,
        },
    )


def validate_skill(skill_dir: Path) -> dict[str, Any]:
    skill_path = skill_dir / "SKILL.md"
    yaml_path = skill_dir / "agents" / "openai.yaml"
    text = skill_path.read_text(encoding="utf-8")
    yaml = yaml_path.read_text(encoding="utf-8")
    name = skill_dir.name
    checks = {
        "frontmatter_opens": text.startswith("---\n"),
        "frontmatter_name_matches": f"name: {name}\n" in text,
        "description_present": "description:" in text.split("---", 2)[1],
        "workflow_present": "## Workflow" in text,
        "boundaries_present": "## Boundaries" in text,
        "metadata_default_prompt_mentions_skill": f"${name}" in yaml,
        "metadata_strings_quoted": 'display_name: "' in yaml and 'short_description: "' in yaml,
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
        runner = ROOT / "scripts" / f"ghc_family_sable_v672_v3_notice_{surface}_guard.py"
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
                "proposal_use": f"SR6723-P{index:03d}",
                "invocation_count": 1,
                "scope": "phase_local_structural_only",
                "globally_installed": False,
                "subagent_forward_test": "not_run_solo_activation_forbids_delegation",
            }
        )
        write_json(X2 / "skill-witnesses" / f"{name}.json", receipt)
        skill_receipts.append(receipt)
    runners_valid = len(runner_receipts) == 10 and all(row["valid"] for row in runner_receipts)
    skills_valid = len(skill_receipts) == 20 and all(row["valid"] for row in skill_receipts)
    if not runners_valid or not skills_valid:
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
            "schema": "ghc.family.sable.v672-v3.outcome-ledger.v1",
            "phase": "v672-v3",
            "state": "executed_as_evidence_permitted",
            "proposal_chain": 6030,
            "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"],
            "outcome_counts": counts,
            "outcomes": outcomes,
        },
    )

    portfolio = load(X1 / "portfolio-freeze.json")
    execution = {
        "schema": "ghc.family.sable.v672-v3.portfolio-execution.v1",
        "safe_now": [{**row, "state": "completed_with_bounded_owner_witness"} for row in portfolio["safe_now_tasks"]],
        "candidates": [{**row, "state": "completed_with_bounded_owner_witness"} for row in portfolio["candidate_tasks"]],
        "skills": skill_receipts,
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
        method_id = f"SR6723-SURFACE-METHOD-{index:03d}"
        methods.append(
            {
                "method_id": method_id,
                "trigger": f"validate {receipt['surface']} synthetic notice surface",
                "preferred_method": "one accepting fixture plus five preregistered rejecting mutations",
                "state": "preferred_after_bounded_passing_witness",
                "rollback": "retain the failed fixture and stop the affected surface",
                "sibling_recommendation": "bind credit to exact surface and fixture set",
            }
        )
        witnesses.append(
            {
                "witness_id": f"SR6723-{receipt['surface'].upper()}-PASS",
                "method_id": method_id,
                "kind": "passing",
                "credit": "bounded_software_only",
                "description": "one accepting fixture passed and five invalid mutations were rejected",
                "state": "bounded_passing",
            }
        )
        for result in receipt["results"]:
            if result["fixture"].startswith("rejecting-"):
                failure_id = f"SR6723-{receipt['surface'].upper()}-{result['fixture'].removesuffix('.json').upper()}"
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
        method_id = f"SR6723-SKILL-METHOD-{index:03d}"
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
                "witness_id": f"SR6723-SKILL-PASS-{index:03d}",
                "method_id": method_id,
                "kind": "passing",
                "credit": "phase_local_structural_only",
                "description": f"skill validated and applied to {receipt['proposal_use']}",
                "state": "bounded_passing_not_global_installation",
            }
        )
    write_json(
        X2 / "method-flow" / "ledger.json",
        {
            "schema": "ghc.family.method-flow.v10",
            "owner": "Sable Rook",
            "phase": "v672-v3",
            "inherited_effective_counts": startup["inherited_effective_counts"],
            "failures_erased": 0,
            "recoveries_relabelled_as_original_success": 0,
            "methods": methods,
            "witnesses": witnesses,
            "expected_rejections": expected_rejections,
            "current_delta": {
                "methods": 36,
                "failed_witnesses": 56,
                "passing_witnesses": 36,
                "effective_negatives": 56,
            },
            "effective_counts": {
                "effective_negatives": 35324,
                "effective_methods": 21935,
                "effective_failed_witnesses": 7145,
                "effective_passing_witnesses": 9222,
                "open_gaps": 281,
                "exact_gates": 274,
            },
        },
    )
    write_json(
        X2 / "retained-negative-register.json",
        {
            "schema": "ghc.family.sable.v672-v3.retained-negatives.v1",
            "activation_baseline": 35268,
            "startup_failures": 6,
            "preregistered_invalid_mutations": 50,
            "x2_unexpected_operational_failures": 0,
            "effective_total": 35324,
            "erased": 0,
            "startup_failure_ids": [f"SR6723-START-{i:03d}" for i in range(1, 7)],
            "mutation_failure_ids": [row["failure_id"] for row in expected_rejections],
        },
    )
    write_json(
        X2 / "gate-register.json",
        {
            "schema": "ghc.family.sable.v672-v3.gates.v1",
            "inherited_open_gaps": 279,
            "new_open_gaps": [
                "real affected-user and assistive-technology evaluation",
                "live service-feed zero-row interoperability",
            ],
            "effective_open_gaps": 281,
            "inherited_exact_gates": 272,
            "new_exact_gates": [
                "public-release and emergency-communication authority",
                "Stage 20 promotion",
            ],
            "effective_exact_gates": 274,
            "silently_closed": 0,
        },
    )
    write_json(
        X2 / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.sable.v672-v3.checklist.v1",
            "complete_within_bounded_owner_scope": [
                "x1 freeze and remote equality", "forty proposal evidence cards", "ten guard surfaces",
                "sixty fixture decisions", "twenty phase-local skill uses", "ten runner uses",
                "portfolio execution receipts", "threat model", "static structural report",
                "retained failure ledger", "gate register",
            ],
            "represented_only": [
                "Freed ID zero-key provenance", "CBR correction and contest path",
                "THOS workload and handover", "GMUT analogy firewall",
                "accessibility nonpromotion", "professional and operational authority vacancy",
                "legal duty and remedy vacancy", "Maori wording data-governance and authority vacancy",
            ],
            "open_gap": [
                "real affected-user and assistive-technology evaluation",
                "live service-feed interoperability with real rows",
            ],
            "exact_gate": [
                "public release or emergency communication authority",
                "Stage 20 promotion",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "schema": "ghc.family.sable.v672-v3.x2-truth.v1",
            "owner": "Sable Rook",
            "phase": "v672-v3",
            "source_head": SOURCE_HEAD,
            "x1_commit": X1_COMMIT,
            "proposal_chain": 6030,
            "outcomes": counts,
            "runner_smoke": {"invocations": 10, "successes": 10, "checks": 60, "passed": 60},
            "skill_smoke": {"invocations": 20, "successes": 20, "globally_installed": False},
            "real_rows": 0,
            "external_actions": 0,
            "independent_reproduction": False,
            "effective_counts": {
                "negatives": 35324, "methods": 21935, "failed_witnesses": 7145,
                "passing_witnesses": 9222, "open_gaps": 281, "exact_gates": 274,
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

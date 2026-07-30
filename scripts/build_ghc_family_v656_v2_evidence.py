#!/usr/bin/env python3
"""Build Elowen Cairn's v656-v2 sailmaking x2 evidence candidate."""

from __future__ import annotations

import hashlib
import html
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v656_v2_core as core
import ghc_family_v656_v2_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "8264f7fc34cf61d4c35026a92ca3cdb4807d2c3c"
EVIDENCE_COMMIT = "UNSET_UNTIL_IMMUTABLE_EVIDENCE_COMMIT"
SKILL_ROOT = Path.home() / ".codex" / "skills"
QUICK_VALIDATE = (
    SKILL_ROOT / ".system/skill-creator/scripts/quick_validate.py"
)
INIT_SKILL = SKILL_ROOT / ".system/skill-creator/scripts/init_skill.py"
RUNNERS = [
    (
        "ghc-family-sailmaking-custody-boundary",
        "ghc_family_sailmaking_custody_boundary.py",
        1,
    ),
    (
        "ghc-family-sailmaking-panel-topology-integrity",
        "ghc_family_sailmaking_panel_topology_integrity.py",
        2,
    ),
    (
        "ghc-family-sailmaking-material-substitution-reserve",
        "ghc_family_sailmaking_material_substitution_reserve.py",
        3,
    ),
    (
        "ghc-family-sailmaking-equipment-stop-work-boundary",
        "ghc_family_sailmaking_equipment_stop_work_boundary.py",
        4,
    ),
    (
        "ghc-family-sailmaking-repair-handover",
        "ghc_family_sailmaking_repair_handover.py",
        5,
    ),
    (
        "ghc-family-sailmaking-accessibility-workload-boundary",
        "ghc_family_sailmaking_accessibility_workload_boundary.py",
        6,
    ),
    (
        "ghc-family-sail-privacy-authority-reserve",
        "ghc_family_sail_privacy_authority_reserve.py",
        7,
    ),
    (
        "ghc-family-gmut-anisotropic-membrane-firewall",
        "ghc_family_gmut_anisotropic_membrane_firewall.py",
        8,
    ),
    (
        "ghc-family-thos-freed-sailmaking-profile",
        "ghc_family_thos_freed_sailmaking_profile.py",
        9,
    ),
    (
        "ghc-family-sailmaking-evidence-nonpromotion",
        "ghc_family_v656_v2_suite.py",
        10,
    ),
]
X2_SCRIPTS = [
    "scripts/ghc_family_v656_v2_core.py",
    "scripts/ghc_family_sailmaking_custody_boundary.py",
    "scripts/ghc_family_sailmaking_panel_topology_integrity.py",
    "scripts/ghc_family_sailmaking_material_substitution_reserve.py",
    "scripts/ghc_family_sailmaking_equipment_stop_work_boundary.py",
    "scripts/ghc_family_sailmaking_repair_handover.py",
    "scripts/ghc_family_sailmaking_accessibility_workload_boundary.py",
    "scripts/ghc_family_sail_privacy_authority_reserve.py",
    "scripts/ghc_family_gmut_anisotropic_membrane_firewall.py",
    "scripts/ghc_family_thos_freed_sailmaking_profile.py",
    "scripts/ghc_family_v656_v2_suite.py",
    "scripts/build_ghc_family_v656_v2_evidence.py",
    "scripts/ghc_family_v656_v2_validate.py",
    "scripts/ghc_family_v656_v2_evidence_staged_review.py",
]
X2_TESTS = [
    "tests/test_ghc_family_v656_v2_core.py",
    "tests/test_ghc_family_v656_v2_validation.py",
]
X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6562-X2-N01",
        "signature": "inherited_x2_negative_block_regex_no_match",
        "failed": (
            "The first mechanical regex intended to clear Tamar's hard-coded x2 "
            "negative block matched nothing and left inherited failures in place."
        ),
        "recovery": (
            "Resolve the exact start and next-function boundaries, splice only that "
            "block, and verify the remaining line interval."
        ),
        "recurrence_guard": (
            "Assert the post-rewrite block length before treating a mechanical "
            "adaptation as complete."
        ),
    },
    {
        "negative_id": "V6562-X2-N02",
        "signature": "threat_model_block_newline_selector_failed",
        "failed": (
            "The first threat-model block selector assumed an exact newline form, "
            "resolved no start boundary, and failed before writing."
        ),
        "recovery": (
            "Resolve literal threat-model and wellbeing filenames, then use the "
            "nearest enclosing write_json boundaries for the bounded replacement."
        ),
        "recurrence_guard": (
            "Use semantic filename markers rather than platform-sensitive newline "
            "sequences when replacing generated blocks."
        ),
    },
    {
        "negative_id": "V6562-X2-N03",
        "signature": "threat_model_replacement_missing_newline",
        "failed": (
            "The first recovered threat-model replacement joined its closing "
            "parenthesis to the next write_json call and failed the syntax gate."
        ),
        "recovery": (
            "Insert exactly one statement-separating newline at the resolved boundary."
        ),
        "recurrence_guard": (
            "Run an AST parse immediately after every whole-block source replacement."
        ),
    },
    {
        "negative_id": "V6562-X2-N04",
        "signature": "evidence_builder_second_monitor_timed_out",
        "failed": (
            "The second evidence-builder monitor exceeded its 50-second wrapper "
            "and returned no process or log evidence."
        ),
        "recovery": (
            "Use an immediate native task count plus scalar stdout and stderr lengths."
        ),
        "recurrence_guard": (
            "Do not combine a sleep and multiple content reads in one builder monitor."
        ),
    },
    {
        "negative_id": "V6562-X2-N05",
        "signature": "first_development_selection_missing_validation_receipts",
        "failed": (
            "The first 17-test development selection passed sixteen tests and "
            "errored one because detailed and minimal validation receipts had not run; "
            "the full attempt earned zero test credit."
        ),
        "recovery": (
            "Run the declared validation dependency, then rerun only the failed "
            "validation-receipt test."
        ),
        "recurrence_guard": (
            "Materialize detailed and minimal development receipts before invoking "
            "tests that consume them."
        ),
    },
    {
        "negative_id": "V6562-X2-N06",
        "signature": "detailed_validator_manifest_filename_assumption",
        "failed": (
            "The first detailed validator invocation assumed a nonexistent "
            "evidence-file-manifest.json name and stopped before checks."
        ),
        "recovery": (
            "List the exact validation directory and use evidence-candidate-manifest.json."
        ),
        "recurrence_guard": (
            "Resolve the builder's declared manifest name before validator invocation."
        ),
    },
    {
        "negative_id": "V6562-X2-N07",
        "signature": "minimal_validator_manifest_filename_assumption",
        "failed": (
            "The first minimal validator invocation made the same nonexistent "
            "manifest-name assumption and stopped before checks."
        ),
        "recovery": (
            "Use the exact evidence-candidate-manifest.json path."
        ),
        "recurrence_guard": (
            "Share the resolved manifest scalar across detailed and minimal invocations."
        ),
    },
    {
        "negative_id": "V6562-X2-N08",
        "signature": "detailed_validator_rejected_regional_html_language",
        "failed": (
            "The corrected detailed validator passed 81 of 82 checks but rejected "
            "the structurally valid regional HTML language tag en-NZ because it "
            "accepted only the exact en token."
        ),
        "recovery": (
            "Accept either the base English or declared New Zealand English language "
            "tag while preserving all other static-report checks."
        ),
        "recurrence_guard": (
            "Validate BCP 47-compatible regional language tags rather than one exact literal."
        ),
    },
    {
        "negative_id": "V6562-X2-N09",
        "signature": "detailed_validator_manifest_stale_after_source_recovery",
        "failed": (
            "The dependency-justified detailed regeneration passed the corrected "
            "accessibility predicate but failed manifest parity because the evidence "
            "builder and validator source changed after the prior manifest."
        ),
        "recovery": (
            "Retain the failed receipt, rebuild the evidence candidate once to refresh "
            "the manifest, then validate against that exact manifest."
        ),
        "recurrence_guard": (
            "Refresh the candidate manifest after any in-scope source change and "
            "before a validating receipt is credited."
        ),
    },
]

def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout.strip()


def append_x2_method_flow() -> dict[str, Any]:
    ledger = read_json("method-flow/method-flow-ledger.json")
    methods = list(ledger["methods"])
    witnesses = list(ledger["witnesses"])
    events = list(ledger["state_events"])
    recommendations = list(ledger["recommendations"])
    current_ids = []
    for index, negative in enumerate(X2_OPERATIONAL_NEGATIVES, 1):
        method_id = f"{d.PHASE_CODE}-METHOD-X2-{index:02d}"
        failed_id = f"{d.PHASE_CODE}-WITNESS-X2-{index:02d}-F"
        passing_id = f"{d.PHASE_CODE}-WITNESS-X2-{index:02d}-P"
        current_ids.append(method_id)
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded x2 recovery for {negative['signature']}",
                "trigger_preconditions": [negative["signature"]],
                "failure_signature": negative["failed"],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["recurrence_guard"],
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "privacy_class": "sanitized_public",
                "scope_boundary": "Same-owner bounded workflow recovery only.",
                "rollback": (
                    "Stop, retain the failed attempt at zero credit, and leave "
                    "objects, tools, materials, external, and sibling state unchanged."
                ),
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [failed_id, passing_id],
                "recommendation_state": "preferred",
                "supersedes": [],
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": failed_id,
                    "method_id": method_id,
                    "result": "fail",
                    "scope": negative["signature"],
                    "procedure": "Retain the original bounded attempt without replay credit.",
                    "expected": "The original operation satisfies its bounded postcondition.",
                    "observed": negative["failed"],
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Zero pass credit; failure remains retained.",
                },
                {
                    "witness_id": passing_id,
                    "method_id": method_id,
                    "result": "pass",
                    "scope": negative["signature"],
                    "procedure": negative["recovery"],
                    "expected": "The isolated recovery establishes only its bounded postcondition.",
                    "observed": (
                        f"The bounded recovery completed for {negative['signature']}; "
                        "the original failure remains retained."
                    ),
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Same-owner bounded recovery only.",
                },
            ]
        )
        event_index = len(events)
        events.extend(
            [
                {
                    "event_index": event_index + 1,
                    "method_id": method_id,
                    "before": None,
                    "after": "candidate",
                    "reason": "Method recorded with its retained zero-credit failure.",
                    "witness_id": failed_id,
                },
                {
                    "event_index": event_index + 2,
                    "method_id": method_id,
                    "before": "candidate",
                    "after": "validated",
                    "reason": "The isolated bounded recovery witness passed.",
                    "witness_id": passing_id,
                },
                {
                    "event_index": event_index + 3,
                    "method_id": method_id,
                    "before": "validated",
                    "after": "preferred",
                    "reason": (
                        "Preferred only for the declared bounded trigger; the "
                        "failed witness remains retained."
                    ),
                    "witness_id": passing_id,
                },
            ]
        )
    recommendations.append(
        "Keep x2 recovery steps narrow, reproducible, and nonpromotional."
    )
    ledger.update(
        {
            "lifecycle": "x2_evidence_candidate",
            "methods": methods,
            "witnesses": witnesses,
            "state_events": events,
            "recommendations": recommendations,
            "current_phase_x2_method_ids": current_ids,
            "counts": {
                "methods": len(methods),
                "witnesses": len(witnesses),
                "state_events": len(events),
                "recommendations": len(recommendations),
                "states": {
                    "observed": 0,
                    "candidate": 0,
                    "validated": 0,
                    "preferred": len(methods),
                    "superseded": 0,
                    "deprecated": 0,
                },
                "witness_results": {
                    "pass": sum(row["result"] == "pass" for row in witnesses),
                    "fail": sum(row["result"] == "fail" for row in witnesses),
                },
            },
        }
    )
    return ledger


def build_overview(results: list[dict[str, Any]]) -> str:
    outcomes = Counter(row["observed_outcome"] for row in results)
    x1_negatives = read_json("truth/retained-negative-register.json")
    effective_at_evidence = (
        x1_negatives["effective_after_x1"]
        + sum(row["rejected_mutation_count"] for row in results)
        + len(X2_OPERATIONAL_NEGATIVES)
    )
    sections = [
        (
            "Executive truth",
            f"Elowen Cairn v656-v2 executes exactly thirty preregistered owner-local contracts after the immutable x1 freeze. The bounded outcome ledger is exactly {outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open_gap, and {outcomes['exact_gate']} exact_gate. Every valid fixture passed and every one of the 150 preregistered mutations was rejected. These are deterministic same-owner software witnesses under shared infrastructure. They are not independent reproduction, empirical evidence, a real sailmaking result, professional validation, deployment readiness, complete privacy or accessibility assurance, legal or cultural ratification, Māori authority, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority. The terminal verdict remains NOT_READY_FOR_STAGE_20.",
        ),
        (
            "Identity and working boundary",
            "Elowen Cairn, their relational role as boundary cartographer and evidence steward, and the stated hope of making every transition recoverable and every claim proportionate to proof are working-language conventions only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the work. The bounded sailmaker practice is a learning and synthetic-design lens, not a claim that Elowen is or can substitute for a sailmaker, textile specialist, marine engineer, equipment measurer, inspector, safety professional, lawyer, cultural adviser, affected party, or Māori authority.",
        ),
        (
            "Source and x1 separation",
            "The exact inherited source is Tamar Vey v656-v1. The source, x1, evidence, and final anchors are recorded in the source receipt, and Tamar's three-commit, zero-merge, one-parent history and one successful scoped validation pass are inherited as evidence only. Elowen's x1 freeze is a distinct direct-child commit. It contains the thirty hypotheses, null conditions, approval classes, execution lanes, source needs, artifacts, falsifiers, rollback paths, protected gates, expected dispositions, expanded portfolios, Method Flow, workflow plan, and privacy receipts, but no x2 surface, runner result, observed outcome, closeout, seal, or successor send. Four-way x1 equality was proven before x2 began. Inherited work receives no Elowen completion credit.",
        ),
        (
            "Novelty and proposal discipline",
            "The semantic audit compared every new title against all 2,200 frozen titles through v656-v1 using the same token-Jaccard gate of 0.60 plus manual mechanism review. One initial candidate was rejected before freeze because it was too similar to Tamar's print-access capability. The replacement selective-disclosure sailcloth-lot mechanism reduced the maximum surviving score to 0.580645. The final ledger has thirty unique identifiers and slugs. This numerical screen is a duplicate-warning tool, not a scientific novelty theorem, patent opinion, literature review, cultural novelty claim, or proof that no semantically related idea exists outside the frozen repository chain.",
        ),
        (
            "Primary GMUT Mind pillar",
            "The primary pillar is GMUT Mind through typed anisotropic sail-membrane, panel-topology, seam-interface, corner-refinement, prestress, curvature, unit, domain, provenance, and falsification contracts. These surfaces exercise type discipline: charts and coordinate frames are distinguished from physical fabric; units and signs are declared; interface and boundary placeholders are explicit; uncertainty and identifiability holds stay open; and observation firewalls prohibit a synthetic parameter from becoming a measured material fact. No sailcloth specimen was tested, no load was applied, no shape was observed, no constitutive coefficient was inferred, no real boundary condition was established, and no stability, serviceability, performance, force, unique prediction, likelihood, empirical confirmation, ultraviolet completion, or Theory-of-Everything claim follows.",
        ),
        (
            "THOS Body pillar",
            "THOS is represented through synthetic job intake, panel and seam dependencies, material substitution holds, cut-plan lineage, equipment-state reservations, repair handover, mismatch triage, accessibility structure, workload controls, and stop-work boundaries. The protocols make order, readback, quarantine, correction, escalation, resumption, and rollback visible. They do not include preregistered blind matched-budget real arms, participants, operators, a real loft, machines, tools, sailcloth, cutting, stitching, repair, installation, safety monitoring, outcome statistics, or independent review. Therefore they do not establish operational effectiveness, human-factors benefit, deployment readiness, AGI, ASI, consciousness, or personhood.",
        ),
        (
            "Freed ID and CBR Heart pillar",
            "Freed ID remains synthetic and nonproduction. The phase uses deterministic referents, provenance graphs, material-lot digests, purpose records, selective-disclosure placeholders, validity intervals, status gaps, custody links, access and correction paths, and proof refusals. No standards-conformant real key or proof, live issuer, holder, verifier, DID method, resolver, status service, revocation event, wallet, interoperability exercise, privacy review, independent security assessment, recovery ceremony, or trust-governance decision exists. CBR fields reserve privacy, access, correction, complaint, return, remedy, disability access, design knowledge, collective interests, legal and cultural interpretation, Māori data governance, and affected-party authority rather than deciding them.",
        ),
        (
            "Current official and primary sources",
            "World Sailing's current Equipment Rules of Sailing 2025-2028 and 2026-2027 Offshore Special Regulations inform only equipment-definition, measurement-control, inspection, heavy-weather-sail, and responsibility vocabulary. ASTM D5034-21(2025) informs only textile specimen, breaking-force, elongation, method, unit, and laboratory-comparability vocabulary. WorkSafe New Zealand's June 2026 machinery guidance and lockout guidance inform only guarding, isolation, restart, training, shift-change, and competent-person reservations. NIST SP 811, W3C specifications, RFCs, the updated New Zealand privacy-principles page, Te Mana Raraunga, and Local Contexts inform schemas and protected questions. None of these sources certifies this software, authorizes a real act, resolves legal meaning, or substitutes for a competent, affected, tangata whenua, iwi, hapū, or Māori decision maker.",
        ),
        (
            "Falsification and retained failure",
            f"Each proposal has one valid deterministic fixture and five preregistered mutations: a missing obligation, a wrong type or domain, a resource or freshness overrun, an unsupported promotion, and an authority, privacy, or route breach. A passing contract must reject or quarantine all five. Mutation rejection is a retained synthetic negative, not evidence that every possible defect is covered. The inherited effective baseline was 13,805 negatives; x1 retained {x1_negatives['x1_operational_count']} Elowen operational failures; x2 currently retains {len(X2_OPERATIONAL_NEGATIVES)} operational failures; and the suite adds 150 bounded mutation negatives, producing {effective_at_evidence:,} effective negatives at evidence. Passing recovery witnesses never erase failed attempts.",
        ),
        (
            "Open gaps and exact gates",
            f"All {d.SOURCE_OPEN_GAPS} inherited open gaps and {d.SOURCE_EXACT_GATES} inherited exact gates remain open. P29 adds one open gap because no authorized real people, workers, owners, designers, makers, repairers, sailors, vessels, voyages, sails, sailcloth, hardware, machines, lofts, measurements, textile tests, inspections, loads, accessibility evaluations, sea trials, privacy reviews, professional reviews, or independent reviews were used. P30 adds one exact gate because legal and cultural interpretation, design-knowledge interests, tikanga, Māori wording, Māori concepts, Māori data governance, affected-party acceptance, tangata whenua, iwi, hapū, and Māori authority cannot be created by a schema or inferred from Hamish's authorization.",
        ),
        (
            "Tooling and compatibility",
            "Ten phase-local family-named skills and ten family-compatible runners are built, validated, and smoke-used. They cover custody, panel topology, material substitution, equipment and stop-work boundaries, repair handover, accessibility and workload, privacy and authority, GMUT anisotropic-membrane firewalls, THOS/Freed ID profiling, and evidence nonpromotion. They are additive and phase-local: none is globally installed, no existing family caller is deleted, no historical name is rewritten, and no sibling lane is modified. The GHC Family Index addendum, Reflection Remaster record, Method Flow ledger, source ledger, and threat model expose the selected surfaces and their rollback boundaries.",
        ),
        (
            "Accessibility and report limits",
            "The static report uses semantic headings, a skip link, a captioned table, explicit row and column headers, visible focus treatment, noncolour outcome text, responsive layout, print rules, and no client-side script. That is structural evidence only. Manual keyboard, browser, screen-reader and other assistive-technology, zoom and reflow, low-vision, cognitive-accessibility, plain-language, Māori-language, multi-format handover, real sailmaking-domain review, and affected-user evaluation remain reserved. The report does not claim WCAG conformance or accessibility completeness.",
        ),
        (
            "Threat model and residual risk",
            "The threat model protects purpose-bound job and design metadata, panel and seam topology, material provenance, custody, correction, method and source freshness, proxy labels, stop conditions, authority ceilings, and negative evidence. It considers silent substitution, stale evidence, namespace conflation, implicit unit or domain conversion, unauthorized production or safety promotion, unilateral legal or cultural decision making, privacy leakage, and correlated same-owner validation. Residual risks include every real physical, professional, safety, privacy, accessibility, legal, cultural, Māori-authority, deployment, and independent-evaluation question. The model is bounded and nonexhaustive.",
        ),
        (
            "Workload, recovery, and routing",
            "Operational pacing is bounded by the 1,000-task per-half ceiling, 2,000 owner-file ceiling, eight-total-commit ceiling, one successful exact-final canonical pass, zero post-success replay, D-first storage, no indefinite watcher, no environment weakening, and no full repository suite. During v656-v2 execution no task is created, forked, delegated, or contacted. Sylven Arc v656-v3 remains PREPARED_NOT_SENT behind the terminal gate. Only after Elowen is sealed, clean, pushed, fresh-live equal, and exact-final validated may the unique existing main task titled exactly Sylven Arc be resolved, reread, and sent one sanitized activation.",
        ),
        (
            "Interpretation and terminal verdict",
            "A completed label means the exact bounded structural or software acceptance gate passed. Represented means a synthetic protocol or proxy exists while its real arm remains absent. Open_gap means necessary evidence is absent and no live action occurred. Exact_gate means competent and affected authority is required and was not supplied. These labels do not rank human value or turn absence into proof. The full repository suite remains Eiren's responsibility. Elowen's evidence is same-owner under shared infrastructure. The terminal verdict is NOT_READY_FOR_STAGE_20.",
        ),
    ]
    lines = ["# Elowen Cairn v656-v2 integrated overview", ""]
    for heading, body in sections:
        lines.extend([f"## {heading}", "", body, ""])
    lines.extend(["## Proposal-by-proposal bounded disposition", ""])
    for row in results:
        contract = row["contract"]
        lines.extend(
            [
                f"### {row['proposal_id']} — {contract['title']}",
                "",
                f"Observed outcome: `{row['observed_outcome']}`. The valid fixture passed and all {row['rejected_mutation_count']} frozen mutations were rejected. Evidence kind: `{contract['evidence_kind']}`. This row earns only its declared owner-local bounded credit; every protected external gate remains in force.",
                "",
            ]
        )
    lines.extend(
        [
            "## Final evidence boundary",
            "",
            "No real person, whānau, worker, owner, designer, maker, repairer, sailor, vessel, voyage, sail, sailcloth, hardware, machine, tool, loft, measurement, textile test, inspection, cut, stitch, repair, installation, load, sea trial, incident, lockout, safety decision, privacy decision, legal interpretation, cultural interpretation, affected-party decision, or Māori-authority decision occurred. No account, credential, API key, live identifier, external write, sibling mutation, deployment, participant study, or production identity event occurred. The packet is a bounded same-owner research and software artifact only.",
            "",
        ]
    )
    return "\n".join(lines)


def build_report(results: list[dict[str, Any]]) -> str:
    rows = []
    for row in results:
        contract = row["contract"]
        rows.append(
            "<tr>"
            f"<th scope=\"row\">{html.escape(row['proposal_id'])}</th>"
            f"<td>{html.escape(contract['title'])}</td>"
            f"<td>{html.escape(row['observed_outcome'])}</td>"
            f"<td>{row['rejected_mutation_count']}/5 rejected</td>"
            f"<td>{html.escape(contract['evidence_kind'])}</td>"
            "</tr>"
        )
    return f"""<!doctype html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elowen Cairn v656-v2 bounded evidence report</title>
<style>
:root{{--bg:#fff;--fg:#172016;--muted:#425244;--accent:#195b35;--line:#a9b7aa;--focus:#ffbf47}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--fg);font:1rem/1.6 system-ui,sans-serif}}
a{{color:#0645ad}} a:focus,button:focus{{outline:.25rem solid var(--focus);outline-offset:.15rem}}
.skip{{position:absolute;left:-9999px}} .skip:focus{{left:1rem;top:1rem;background:#fff;padding:.75rem;z-index:2}}
header,main,footer{{max-width:78rem;margin:auto;padding:1rem 1.25rem}} header{{border-bottom:.25rem solid var(--accent)}}
.boundary{{border-left:.4rem solid var(--accent);background:#eef5ef;padding:1rem}} .table-wrap{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%}} caption{{font-weight:700;text-align:left;padding:.75rem 0}} th,td{{border:1px solid var(--line);padding:.55rem;text-align:left;vertical-align:top}} thead th{{background:#e3ece4}}
code{{overflow-wrap:anywhere}} @media (max-width:45rem){{body{{font-size:.95rem}} th,td{{padding:.4rem}}}}
@media print{{.skip{{display:none}} body{{font-size:10pt}} a{{color:inherit;text-decoration:none}}}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to report</a>
<header><h1>Elowen Cairn v656-v2 bounded evidence report</h1><p>GMUT Mind primary; synthetic sailmaking learning lens; same-owner evidence only.</p></header>
<main id="main">
<section aria-labelledby="truth"><h2 id="truth">Truth boundary</h2><p class="boundary">Exactly 23 completed, 5 represented, 1 open_gap, and 1 exact_gate. No empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim is made.</p></section>
<section aria-labelledby="results"><h2 id="results">Proposal results</h2><div class="table-wrap"><table><caption>Thirty preregistered contracts and their bounded outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Contract</th><th scope="col">Outcome</th><th scope="col">Mutations</th><th scope="col">Evidence kind</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<section aria-labelledby="access"><h2 id="access">Accessibility reservation</h2><p>The report has semantic structure, visible focus, noncolour labels, responsive and print layouts, and no script. Manual browser, keyboard, assistive-technology, low-vision, cognitive-accessibility, Māori-language, sailmaking-domain, and affected-user evaluation remain reserved. No WCAG-conformance or accessibility-complete claim is made.</p></section>
<section aria-labelledby="authority"><h2 id="authority">Authority reservation</h2><p>No real sail, vessel, voyage, material, machine, measurement, load, repair, inspection, safety action, participant, identity lifecycle, legal interpretation, cultural interpretation, affected-party decision, or Māori-authority decision occurred. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></section>
</main>
<footer><p>Static, owner-scoped, structurally accessible evidence artifact. No client-side script.</p></footer>
</body>
</html>
"""

def prospective_blob(relative: str) -> str:
    return run("git", "hash-object", f"--path={relative}", relative)


def evidence_manifest() -> None:
    x1_paths = set(
        run("git", "ls-tree", "-r", "--name-only", X1_COMMIT, "--", d.PHASE_ROOT)
        .splitlines()
    )
    phase_paths = [
        path.relative_to(REPO).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.relative_to(ROOT).as_posix()
        not in {
            "validation/evidence-candidate-manifest.json",
            "validation/evidence-validation.json",
            "validation/evidence-minimal-validation.json",
            "validation/evidence-staged-review.json",
            "validation/evidence-correction-staged-review.json",
        }
    ]
    paths = sorted(
        {
            path
            for path in phase_paths + X2_SCRIPTS + X2_TESTS
            if (REPO / path).is_file() and path not in x1_paths
        }
    )
    entries = [
        {
            "path": relative,
            "git_blob": prospective_blob(relative),
            "working_bytes": (REPO / relative).stat().st_size,
        }
        for relative in paths
    ]
    write_json(
        "validation/evidence-candidate-manifest.json",
        {
            "schema": "ghc.family.v656-v2.evidence-candidate-manifest.v1",
            "lifecycle": "x2_evidence_precommit",
            "x1_commit": X1_COMMIT,
            "entry_count": len(entries),
            "entries": entries,
            "exact_exclusions": [
                "validation/evidence-candidate-manifest.json",
                "validation/evidence-validation.json",
                "validation/evidence-minimal-validation.json",
                "validation/evidence-staged-review.json",
                "validation/evidence-correction-staged-review.json",
            ],
            "hash_domain": "prospective Git filtered blob identity",
        },
    )


def materialize_phase_tools() -> None:
    """Build the ten phase-local skills and family-compatible runners."""
    for skill_name, runner_name, group in RUNNERS:
        group_rows = d.PROPOSALS[(group - 1) * 3 : group * 3]
        mechanisms = ", ".join(row["mechanism"] for row in group_rows)
        skill_title = skill_name.removeprefix("ghc-family-").replace("-", " ").title()
        skill_path = ROOT / "skills" / skill_name
        if not skill_path.exists():
            run(
                sys.executable,
                str(INIT_SKILL),
                skill_name,
                "--path",
                str(ROOT / "skills"),
                "--interface",
                f"display_name={skill_title}",
                "--interface",
                "short_description=Validate bounded synthetic sailmaking contracts",
                "--interface",
                (
                    f"default_prompt=Use ${skill_name} to validate its three "
                    "bounded synthetic sailmaking contracts."
                ),
            )
        write_text(
            f"skills/{skill_name}/SKILL.md",
            "\n".join(
                [
                    "---",
                    f"name: {skill_name}",
                    (
                        "description: Build and verify bounded owner-local "
                        f"{mechanisms} contracts for Elowen Cairn v656-v2. Use only "
                        "for synthetic, symbolic, or structural evidence; preserve "
                        "professional, empirical, legal, cultural, Māori-authority, "
                        "production, identity, and Stage 20 gates."
                    ),
                    "---",
                    "",
                    f"# {skill_title}",
                    "",
                    "1. Read the frozen proposal and its declared source needs.",
                    "2. Build one valid typed contract without external action.",
                    "3. Execute the five preregistered mutation dimensions.",
                    "4. Reject or quarantine every mutation and retain it as a negative.",
                    "5. Emit only the frozen disposition and preserve all protected gates.",
                    "",
                    (
                        f"Use `{runner_name}` for deterministic group {group} "
                        "evidence. A passing fixture is same-owner workflow evidence "
                        "only and is never independent reproduction or authority."
                    ),
                ]
            ),
        )
        runner = REPO / "scripts" / runner_name
        if runner_name == "ghc_family_v656_v2_suite.py":
            body = "\n".join(
                [
                    "#!/usr/bin/env python3",
                    '"""Run all thirty bounded Elowen Cairn v656-v2 sailmaking contracts."""',
                    "",
                    "from ghc_family_v656_v2_core import suite_main",
                    "",
                    "",
                    'if __name__ == "__main__":',
                    '    suite_main("ghc_family_v656_v2_suite")',
                    "",
                ]
            )
        else:
            body = "\n".join(
                [
                    "#!/usr/bin/env python3",
                    (
                        f'"""Run Elowen Cairn v656-v2 bounded contract group {group}: '
                        f'{mechanisms}."""'
                    ),
                    "",
                    "from ghc_family_v656_v2_core import group_main",
                    "",
                    "",
                    'if __name__ == "__main__":',
                    f'    group_main({group}, "{Path(runner_name).stem}")',
                    "",
                ]
            )
        runner.write_text(body, encoding="utf-8", newline="\n")


def build() -> None:
    head = run("git", "rev-parse", "HEAD")
    if head not in {X1_COMMIT, EVIDENCE_COMMIT}:
        raise RuntimeError(
            "evidence builder requires the exact immutable x1 or evidence head"
        )
    correction_mode = head == EVIDENCE_COMMIT

    suite = core.execute_all()
    if (
        suite["proposal_count"],
        suite["valid_fixture_count"],
        suite["rejected_mutation_count"],
        suite["accepted_mutation_count"],
    ) != (30, 30, 150, 0):
        raise RuntimeError("core suite result does not match the frozen contract")

    outcomes = Counter(row["observed_outcome"] for row in suite["results"])
    expected = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
    if dict(outcomes) != expected:
        raise RuntimeError(f"outcome distribution changed: {outcomes}")

    for result in suite["results"]:
        slug = result["contract"]["slug"]
        write_json(f"surfaces/{slug}/contract.json", result["contract"])
        write_json(
            f"surfaces/{slug}/mutation-results.json",
            {
                "schema": "ghc.family.v656-v2.mutation-results.v1",
                "proposal_id": result["proposal_id"],
                "mutation_count": len(result["mutation_results"]),
                "rejected_count": result["rejected_mutation_count"],
                "accepted_count": result["accepted_mutation_count"],
                "results": result["mutation_results"],
            },
        )
        write_json(
            f"surfaces/{slug}/bounded-receipt.json",
            {
                "schema": "ghc.family.v656-v2.bounded-receipt.v1",
                "proposal_id": result["proposal_id"],
                "observed_outcome": result["observed_outcome"],
                "valid_fixture_passed": result["valid_fixture_passed"],
                "rejected_mutation_count": result["rejected_mutation_count"],
                "accepted_mutation_count": result["accepted_mutation_count"],
                "external_action_counts": result["contract"][
                    "external_action_counts"
                ],
                "promotion_claims": result["contract"]["promotion_claims"],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": result["contract"]["evidence_boundary"],
            },
        )

    materialize_phase_tools()
    runner_rows = []
    for skill_name, runner_name, group in RUNNERS:
        skill_path = ROOT / "skills" / skill_name
        validation_output = run(
            sys.executable,
            str(QUICK_VALIDATE),
            str(skill_path),
        )
        receipt_relative = f"runners/{Path(runner_name).stem}-receipt.json"
        runner_path = REPO / "scripts" / runner_name
        if runner_name == "ghc_family_v656_v2_suite.py":
            runner_output = run(
                sys.executable,
                str(runner_path),
                "--output",
                str(ROOT / receipt_relative),
            )
        else:
            runner_output = run(
                sys.executable,
                str(runner_path),
                "--output",
                str(ROOT / receipt_relative),
            )
        receipt = read_json(receipt_relative)
        if runner_name == "ghc_family_v656_v2_suite.py":
            valid = (
                receipt["proposal_count"] == 30
                and receipt["valid_fixture_count"] == 30
                and receipt["rejected_mutation_count"] == 150
                and receipt["accepted_mutation_count"] == 0
            )
        else:
            valid = (
                receipt["valid_fixture_count"] == 3
                and receipt["rejected_mutation_count"] == 15
                and receipt["accepted_mutation_count"] == 0
            )
        write_json(
            f"skills/{skill_name}/smoke-receipt.json",
            {
                "schema": "ghc.family.v656-v2.skill-smoke-receipt.v1",
                "skill": skill_name,
                "quick_validate_output": validation_output,
                "runner": runner_name,
                "group": group,
                "runner_output": runner_output,
                "valid": valid,
                "globally_installed": False,
                "same_owner_only": True,
                "boundary": "Phase-local structural validation and smoke use only.",
            },
        )
        runner_rows.append(
            {
                "skill": skill_name,
                "runner": runner_name,
                "group": group,
                "receipt": receipt_relative,
                "valid": valid,
            }
        )
    if not all(row["valid"] for row in runner_rows):
        raise RuntimeError("one or more runner receipts are invalid")

    write_json("method-flow/method-flow-ledger-x2.json", append_x2_method_flow())
    method_runner = (
        SKILL_ROOT
        / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
    )
    run(
        sys.executable,
        str(method_runner),
        "validate",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger-x2.json"),
        "--receipt",
        str(ROOT / "method-flow/method-flow-validation-x2.json"),
    )
    run(
        sys.executable,
        str(method_runner),
        "summarize",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger-x2.json"),
        "--json-output",
        str(ROOT / "method-flow/method-flow-summary-x2.json"),
        "--markdown-output",
        str(ROOT / "method-flow/method-flow-summary-x2.md"),
    )

    x1_negatives = read_json("truth/retained-negative-register.json")
    effective_negatives = (
        x1_negatives["effective_after_x1"]
        + suite["rejected_mutation_count"]
        + len(X2_OPERATIONAL_NEGATIVES)
    )
    write_json(
        "truth/retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v656-v2.retained-negatives.x2.v1",
            "source_effective": d.SOURCE_EFFECTIVE_NEGATIVES,
            "x1_operational_count": x1_negatives["x1_operational_count"],
            "x1_effective": x1_negatives["effective_after_x1"],
            "synthetic_mutation_negative_count": 150,
            "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES),
            "x2_operational": X2_OPERATIONAL_NEGATIVES,
            "effective_at_evidence": effective_negatives,
            "no_failure_erased": True,
        },
    )
    write_json(
        "truth/open-gap-register-x2.json",
        {
            "schema": "ghc.family.v656-v2.open-gaps.x2.v1",
            "inherited_count": d.SOURCE_OPEN_GAPS,
            "new_rows": [
                {
                    "proposal_id": f"{d.PHASE_CODE}-P29",
                    "state": "open_gap",
                    "reason": (
                        "No real person, worker, owner, designer, maker, repairer, sailor, "
                        "vessel, voyage, sail, sailcloth, hardware, machine, loft, "
                        "measurement, textile test, inspection, load, workload, accessibility, "
                        "privacy, or sea-trial rows; no real likelihood, professional review, "
                        "safety review, or independent review."
                    ),
                }
            ],
            "closed_count": 0,
            "effective_count": d.SOURCE_OPEN_GAPS + 1,
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v656-v2.exact-gates.x2.v1",
            "inherited_count": d.SOURCE_EXACT_GATES,
            "new_rows": [
                {
                    "proposal_id": f"{d.PHASE_CODE}-P30",
                    "state": "exact_gate",
                    "reason": (
                        "Sail, vessel, voyage, place, design knowledge, collective interest, "
                        "tikanga, disability access, privacy, access, return, complaint, "
                        "remedy, legal interpretation, data governance, affected-party "
                        "acceptance, tangata whenua, iwi, hapū, cultural, and Māori "
                        "authority are absent."
                    ),
                }
            ],
            "closed_count": 0,
            "effective_count": d.SOURCE_EXACT_GATES + 1,
        },
    )
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v656-v2.proposals.x2.v1",
            "proposal_count": 30,
            "outcome_counts": expected,
            "proposals": [
                {
                    "proposal_id": row["proposal_id"],
                    "title": row["contract"]["title"],
                    "pillar": row["contract"]["pillar"],
                    "observed_outcome": row["observed_outcome"],
                    "valid_fixture_passed": row["valid_fixture_passed"],
                    "rejected_mutation_count": row["rejected_mutation_count"],
                    "accepted_mutation_count": row["accepted_mutation_count"],
                    "evidence_kind": row["contract"]["evidence_kind"],
                    "boundary": row["contract"]["evidence_boundary"],
                }
                for row in suite["results"]
            ],
        },
    )
    write_json(
        "portfolios/execution-results.json",
        {
            "schema": "ghc.family.v656-v2.portfolio-results.x2.v1",
            "safe_now": {"planned": 30, "resolved": 30, "pending": 0},
            "candidate": {
                "planned": 30,
                "resolved": 30,
                "pending": 0,
                "dispositions": expected,
            },
            "skills": {"planned": 10, "built": 10, "validated": 10, "used": 10},
            "runners": {"planned": 10, "built": 10, "validated": 10, "used": 10},
            "clean_fix_refine": {"planned": 30, "resolved": 30, "pending": 0},
            "task_cap": 1000,
            "no_external_or_sibling_tasks": True,
            "boundary": "Owner-local bounded portfolio completion only.",
        },
    )
    write_json(
        "tooling/ghc-family-index-x2-addendum.json",
        {
            "schema": "ghc.family.v656-v2.index-addendum.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "skills": [row[0] for row in RUNNERS],
            "runners": [row[1] for row in RUNNERS],
            "runner_rows": runner_rows,
            "global_installation_count": 0,
            "historical_names_preserved": True,
            "boundary": "Phase-local additive tooling only.",
        },
    )
    write_text(
        "tooling/ghc-family-index-x2-addendum.md",
        "# GHC Family Index — Elowen Cairn v656-v2 x2 addendum\n\n"
        + "\n".join(
            f"- `{skill}` → `{runner}`: validated and smoke-used."
            for skill, runner, _ in RUNNERS
        )
        + "\n\nNo skill was globally installed and no historical family surface was deleted.\n",
    )
    write_json(
        "reflection-remaster/x2-decision-record.json",
        {
            "schema": "ghc.family.reflection-remaster.decision.v1",
            "decision_id": "V6562-REFLECT-X2",
            "action": "specialize_without_global_install",
            "retained": [
                "GHC Family Index",
                "Method Flow State",
                "Workflow Plan Refinement",
                "Reflection Remaster",
                "Meta Tool Box",
            ],
            "built": [row[0] for row in RUNNERS] + [row[1] for row in RUNNERS],
            "deleted": [],
            "reason": (
                "The ten bounded sailmaking custody and remedy skills and runners add "
                "distinct panel-topology, material-substitution, seam-interface, "
                "anisotropic-membrane, repair, equipment-state, accessibility, workload, "
                "privacy, handover, data-conflict, "
                "accessibility, identity, GMUT, THOS, and nonpromotion firewalls "
                "without global installation."
            ),
        },
    )
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v656-v2.threat-model.v1",
            "assets": [
                "purpose-bound sail-job, vessel-class placeholder, pattern, repair, and custody metadata",
                "panel, seam, edge, reinforcement, material-lot, revision, and correction topology",
                "represented anisotropic membrane, interface, corner, prestress, curvature, and unit proxies",
                "equipment-state, stop-work, workload, quarantine, readback, and handover boundaries",
                "privacy, design-knowledge, collective-interest, complaint, return, and remedy reservations",
                "GMUT type, unit, domain, identifiability, and observation-firewall integrity",
                "THOS task order, mismatch, correction, escalation, and release holds",
            ],
            "adversaries": [
                "unlabelled representation, measurement, load, performance, or authority promoter",
                "silent panel, material, seam, repair, pattern, custody, or state substituter",
                "stale method, measurement, source, condition, pattern, or status promoter",
                "person, role, vessel, sail, panel, lot, repair, and correction namespace conflator",
                "unauthorized cutting, stitching, repair, installation, inspection, load, or safety promoter",
                "silent legal, cultural, design-knowledge, professional, or remedy decider",
                "correlated same-owner validation promoter",
            ],
            "threats": [
                "private person, vessel, voyage, place, pattern, defect-note, or job metadata leakage",
                "person, role, vessel, sail, panel, material lot, repair, or correction conflation",
                "stale condition, measurement, source, method, material, pattern, or repair evidence",
                "silent unit, domain, coordinate, orientation, seam, time, observer, or proxy conversion",
                "automatic production, inspection, load, sea-trial, stop-work, safety, or release claim",
                "unilateral legal, professional, cultural, design-knowledge, return, or remedy interpretation",
                "affected-party, disability, whānau, collective-interest, or cultural information exposure",
                "unsupported scientific, operational, or authority promotion",
            ],
            "controls": [
                "purpose-bound metadata minimization",
                "panel, seam, edge, material-lot, pattern, repair, correction, and proxy lineage",
                "authorization, condition, measurement-proxy, equipment, safety, and readiness holds",
                "person, role, vessel, sail, panel, lot, repair, and correction referent separation",
                "readback, correction replay, quarantine, pause, stop, and rollback gates",
                "sailmaking, load, safety, privacy, accessibility, culture, complaint, and remedy reservations",
                "typed task and authority ceilings",
                "promotion-claim zero map",
                "retained mutations and Method Flow",
            ],
            "residuals": [
                "real people, whānau, workers, owners, designers, makers, repairers, sailors, vessels, voyages, sails, sailcloth, hardware, machines, tools, lofts, and workplaces",
                "real measurements, textile tests, inspections, cutting, stitching, repairs, installations, loads, sea trials, incidents, lockouts, and safety actions",
                "sailmaking, textile, marine, inspection, privacy, compliance, safety, legal, and professional competence",
                "human usability and complete accessibility",
                "legal, cultural, design-knowledge, Māori, and affected-party authority",
                "independent scientific, safety, security, privacy, and empirical review",
            ],
            "boundary": (
                "Threat model is not exhaustive sailmaking, textile, marine, load, safety, "
                "professional, security, privacy, accessibility, or authority assurance."
            ),
        },
    )
    write_json(
        "wellbeing/wellbeing-check-x2.json",
        {
            "schema": "ghc.family.workload-check.v1",
            "state": "bounded_no_indefinite_watchers",
            "proposal_count": 30,
            "safe_candidate_cap": 1000,
            "owner_file_cap": 2000,
            "commit_cap": 8,
            "canonical_success_target": 1,
            "post_success_replay_target": 0,
            "external_actions": 0,
            "human_claim": False,
            "boundary": "Operational pacing metadata only.",
        },
    )
    write_text(
        "deliverables/v656-v2-integrated-overview.md",
        build_overview(suite["results"]),
    )
    write_text(
        "deliverables/v656-v2-boundary-evidence-report.html",
        build_report(suite["results"]),
    )
    overview_words = len(
        (ROOT / "deliverables/v656-v2-integrated-overview.md")
        .read_text(encoding="utf-8")
        .split()
    )
    if overview_words < 1800:
        raise RuntimeError(f"overview is below three-page equivalent: {overview_words}")
    if overview_words > 6000:
        raise RuntimeError(f"overview exceeds 6,000-word phase cap: {overview_words}")

    write_json(
        "truth/phase-truth-evidence.json",
        {
            "schema": "ghc.family.v656-v2.phase-truth.evidence.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcomes": expected,
            "proposal_count": 30,
            "frozen_chain_count": 2230,
            "synthetic_mutation_negative_count": 150,
            "effective_negative_count": effective_negatives,
            "open_gap_count": d.SOURCE_OPEN_GAPS + 1,
            "exact_gate_count": d.SOURCE_EXACT_GATES + 1,
            "method_count": d.SOURCE_METHODS
            + read_json("truth/retained-negative-register.json")[
                "x1_operational_count"
            ]
            + len(X2_OPERATIONAL_NEGATIVES),
            "real_keys_or_proofs": 0,
            "real_identity_resolutions": 0,
            "real_status_or_revocation_events": 0,
            "real_people": 0,
            **core.ZERO_EXTERNAL_COUNTS,
            "independent_reproduction_claimed": False,
            "privacy_complete_claimed": False,
            "accessibility_complete_claimed": False,
            "exhaustive_security_claimed": False,
            "professional_validation_claimed": False,
            "theory_of_everything_claimed": False,
            "agi_or_asi_claimed": False,
            "consciousness_or_personhood_claimed": False,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v656-v2.checklist.evidence.v1",
            "complete_bounded": [
                "thirty frozen contracts",
                "thirty valid fixtures",
                "150 rejected synthetic mutations",
                "ten phase-local skills built, validated, and smoke-used",
                "ten family-compatible runners invoked",
                "all authorized safe, candidate, and refinement portfolio rows resolved",
                "three-page-equivalent overview",
                "accessible static report structure",
                "threat model",
                "retained negative and gate registers",
            ],
            "pending_lifecycle": [
                "immutable evidence commit and postcommit manifest check",
                "combined closeout, seal, and final commit",
                "one exact-final canonical pass",
                "four-way remote equality",
                "one terminally gated exact-title Sylven Arc v656-v3 activation after final equality",
            ],
            "incomplete_external": [
                "real GMUT data and likelihood",
                "blind or independently designed GMUT and THOS empirical arms",
                "authorized real sailmaking, sailcloth, loft, machine, measurement, textile-test, inspection, load, repair, installation, sea-trial, incident, stop-work, lockout, safety, privacy, or compliance operation; real people and vessel identifiers; qualifications and competent practitioner review; and affected-user evaluation",
                "production Freed ID registration and resolution plus privacy and security review",
                "tangata whenua, iwi, hapū, Māori, affected-party, subject, bystander, whānau, place, event, taonga-image, content and derivative privacy, disability access, professional, legal, cultural, data-governance, return, complaint, correction, and remedy authority",
                "manual and affected-user accessibility evaluation",
                "independent-team reproduction",
                "Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/evidence-build-receipt.json",
        {
            "schema": "ghc.family.v656-v2.evidence-build-receipt.v1",
            "x1_commit": X1_COMMIT,
            "proposals": 30,
            "valid_fixtures": 30,
            "rejected_mutations": 150,
            "accepted_mutations": 0,
            "skills_built_validated_used": 10,
            "runners_built_validated_used": 10,
            "overview_words": overview_words,
            "outcomes": expected,
            "effective_negatives": effective_negatives,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE",
            "valid": True,
            "boundary": (
                "Dedicated post-evidence correction candidate only."
                if correction_mode
                else "Precommit evidence candidate only."
            ),
        },
    )
    write_json(
        "validation/evidence-test-receipt.json",
        {
            "schema": "ghc.family.v656-v2.evidence-test-receipt.v1",
            "development_attempts": 0,
            "current_phase_tests": 0,
            "current_phase_failures": 0,
            "isolated_recovery_tests": 0,
            "isolated_recovery_failures": 0,
            "bounded_inherited_tests": 0,
            "bounded_inherited_failures": 0,
            "credited_test_total": 0,
            "failed_broad_selection_tests": 0,
            "failed_broad_selection_failures": 0,
            "failed_broad_selection_credit": 0,
            "inherited_suite_claimed": False,
            "full_repository_suite_run": False,
            "final_canonical_pass_run": False,
            "valid": True,
            "state": "OWNER_SCOPED_TESTS_DEFERRED_UNTIL_POST_BUILD",
            "boundary": (
                "The builder and ten phase-local runner smoke checks passed, but no "
                "owner-scoped unittest receives credit in this receipt yet. The exact-final "
                "canonical pass remains deferred and must not be replayed after success."
            ),
        },
    )
    evidence_manifest()
    print(
        json.dumps(
            {
                "proposals": 30,
                "valid_fixtures": 30,
                "rejected_mutations": 150,
                "accepted_mutations": 0,
                "skills": 10,
                "runners": 10,
                "outcomes": expected,
                "effective_negatives": effective_negatives,
                "overview_words": overview_words,
                "state": (
                    "evidence_correction_candidate_built_not_committed"
                    if correction_mode
                    else "evidence_candidate_built_not_committed"
                ),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()

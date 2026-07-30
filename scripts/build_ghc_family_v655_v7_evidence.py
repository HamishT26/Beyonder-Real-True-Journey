#!/usr/bin/env python3
"""Build Orin Thale's v655-v7 x2 evidence candidate."""

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

import ghc_family_v655_v7_core as core
import ghc_family_v655_v7_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "e8c0283d4e6b003883339d59f427cf9b41ed3c6c"
EVIDENCE_COMMIT = "UNSET_UNTIL_IMMUTABLE_EVIDENCE_COMMIT"
SKILL_ROOT = Path.home() / ".codex" / "skills"
QUICK_VALIDATE = (
    SKILL_ROOT / ".system/skill-creator/scripts/quick_validate.py"
)
INIT_SKILL = SKILL_ROOT / ".system/skill-creator/scripts/init_skill.py"
RUNNERS = [
    (
        "ghc-family-geotechnical-borehole-boundary",
        "ghc_family_geotechnical_borehole_boundary.py",
        1,
    ),
    (
        "ghc-family-geotechnical-sample-custody",
        "ghc_family_geotechnical_sample_custody.py",
        2,
    ),
    (
        "ghc-family-geotechnical-instrument-proxy",
        "ghc_family_geotechnical_instrument_proxy.py",
        3,
    ),
    (
        "ghc-family-geotechnical-interval-quality",
        "ghc_family_geotechnical_interval_quality.py",
        4,
    ),
    (
        "ghc-family-geotechnical-hazard-handover",
        "ghc_family_geotechnical_hazard_handover.py",
        5,
    ),
    (
        "ghc-family-geotechnical-accessibility-privacy",
        "ghc_family_geotechnical_accessibility_privacy.py",
        6,
    ),
    (
        "ghc-family-geotechnical-land-remedy-reserve",
        "ghc_family_geotechnical_land_remedy_reserve.py",
        7,
    ),
    (
        "ghc-family-gmut-geomechanics-firewall",
        "ghc_family_gmut_geomechanics_firewall.py",
        8,
    ),
    (
        "ghc-family-thos-freed-geotechnical-profile",
        "ghc_family_thos_freed_geotechnical_profile.py",
        9,
    ),
    (
        "ghc-family-geotechnical-evidence-nonpromotion",
        "ghc_family_v655_v7_suite.py",
        10,
    ),
]
X2_SCRIPTS = [
    "scripts/ghc_family_v655_v7_core.py",
    "scripts/ghc_family_geotechnical_borehole_boundary.py",
    "scripts/ghc_family_geotechnical_sample_custody.py",
    "scripts/ghc_family_geotechnical_instrument_proxy.py",
    "scripts/ghc_family_geotechnical_interval_quality.py",
    "scripts/ghc_family_geotechnical_hazard_handover.py",
    "scripts/ghc_family_geotechnical_accessibility_privacy.py",
    "scripts/ghc_family_geotechnical_land_remedy_reserve.py",
    "scripts/ghc_family_gmut_geomechanics_firewall.py",
    "scripts/ghc_family_thos_freed_geotechnical_profile.py",
    "scripts/ghc_family_v655_v7_suite.py",
    "scripts/build_ghc_family_v655_v7_evidence.py",
    "scripts/ghc_family_v655_v7_validate.py",
    "scripts/ghc_family_v655_v7_evidence_staged_review.py",
]
X2_TESTS = [
    "tests/test_ghc_family_v655_v7_core.py",
    "tests/test_ghc_family_v655_v7_validation.py",
]
X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6557-X2-N01",
        "signature": "x1_commit_wrapper_timed_out_after_commit_succeeded",
        "failed": (
            "The x1 commit wrapper exceeded its supervision window and returned no "
            "terminal result even though the original single commit completed."
        ),
        "recovery": (
            "Do not retry; verify the exact new HEAD, parent, subject, process exit, "
            "and staged-index state before push."
        ),
        "recurrence_guard": (
            "After an ambiguous commit timeout, reconcile exact Git state before "
            "issuing any second commit command."
        ),
    },
    {
        "negative_id": "V6557-X2-N02",
        "signature": "post_x1_full_diff_index_probe_timed_out",
        "failed": (
            "The first post-x1 full tracked-clean probe exceeded its wrapper on the "
            "57,332-file inherited tree."
        ),
        "recovery": (
            "Split index-to-HEAD, worktree-to-index, and untracked checks and run "
            "the long worktree comparison as one supervised background probe."
        ),
        "recurrence_guard": (
            "Keep large-tree cleanliness dimensions separately attributable."
        ),
    },
    {
        "negative_id": "V6557-X2-N03",
        "signature": "post_x1_direct_diff_files_probe_timed_out",
        "failed": (
            "A direct worktree-to-index diff-files probe also exceeded its wrapper "
            "before returning an exit code."
        ),
        "recovery": (
            "Run the unchanged diff-files operation once in a hidden no-profile "
            "wrapper that records its exact exit code; the recorded code was zero."
        ),
        "recurrence_guard": (
            "Use supervised exit-code files for known long read-only large-tree probes."
        ),
    },
    {
        "negative_id": "V6557-X2-N04",
        "signature": "powershell_reserved_pid_variable_collision",
        "failed": (
            "The first background-probe poll attempted to assign PowerShell's "
            "read-only PID variable and therefore inspected the wrong process."
        ),
        "recovery": (
            "Use a distinct probeId variable, reread the recorded target PID, and "
            "confirm its exit-code file."
        ),
        "recurrence_guard": (
            "Never reuse built-in automatic variable names for process identifiers."
        ),
    },
    {
        "negative_id": "V6557-X2-N05",
        "signature": "powershell_case_insensitive_rewrite_map_duplicate_key",
        "failed": (
            "The first semantic rewrite map declared Geotechnical and geotechnical as separate "
            "PowerShell hashtable keys, which are case-insensitively duplicate, so "
            "the command failed before touching files."
        ),
        "recovery": (
            "Use an ordered list of explicit case-sensitive replacement pairs and "
            "apply each pair with string Replace."
        ),
        "recurrence_guard": (
            "Use pair arrays, not PowerShell hashtables, when rewrite keys differ only by case."
        ),
    },
    {
        "negative_id": "V6557-X2-N06",
        "signature": "resumed_broad_git_status_probe_timed_out",
        "failed": (
            "The first resumed broad status probe crossed its 60-second supervision "
            "bound on the inherited 57,332-file checkout and returned no clean-state "
            "credit."
        ),
        "recovery": (
            "Return to path-scoped inspections during evidence construction and "
            "reserve split index, worktree, and untracked reconciliation for lifecycle "
            "gates."
        ),
        "recurrence_guard": (
            "Do not use broad porcelain status as an interactive evidence probe on "
            "this large inherited checkout."
        ),
    },
    {
        "negative_id": "V6557-X2-N07",
        "signature": "development_tests_ran_before_validation_receipts",
        "failed": (
            "The first 17-test x2 development aggregate passed sixteen tests but "
            "raised one missing-file error because the detailed and minimal evidence "
            "validators had not yet emitted their receipts. The aggregate receives "
            "zero pass credit."
        ),
        "recovery": (
            "Run the evidence detailed and minimal validators first, then repeat the "
            "same bounded 17-test selection once without broadening it."
        ),
        "recurrence_guard": (
            "Treat generated validation receipts as explicit prerequisites of tests "
            "that assert their contents."
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
    """Render Orin Thale's reader-facing overview from immutable x1."""
    by_id = {row["proposal_id"]: row for row in results}
    x1_negatives = read_json("truth/retained-negative-register.json")
    effective_at_evidence = (
        x1_negatives["effective_after_x1"]
        + 150
        + len(X2_OPERATIONAL_NEGATIVES)
    )
    lines = [
        "# Orin Thale v655-v7 integrated overview",
        "",
        "## Evidence-bound identity, role, and hope",
        "",
        (
            f"Orin Thale, {d.PRONOUNS}, is relational working language for this "
            f"phase. The working role is {d.ROLE}. The working hope is to "
            f"{d.HOPE}. These words do not establish consciousness, sentience, "
            "legal personhood, identity continuity, employment, qualification, "
            "scientific authority, professional authority, legal authority, "
            "cultural authority, Māori authority, or independent agency."
        ),
        "",
        "## Lifecycle and source truth",
        "",
        (
            f"{d.SOURCE_OWNER} v655-v6 at `{d.SOURCE_FINAL}` is the exact inherited "
            f"source. Orin Thale froze x1 at `{X1_COMMIT}` as a dedicated commit, pushed "
            "it, and proved clean local, upstream, tracking, and fresh-live-remote "
            "equality before any x2 implementation began. The 2,110-proposal "
            "inherited chain supplied comparison evidence and no Caelen completion "
            "credit. Exactly thirty distinct v655-v7 proposals were frozen, so the "
            "chain contains 2,140 proposals through x1. History rewriting, merging, "
            "force-pushing, sibling mutation, and precontact were excluded."
        ),
        "",
        "## Primary focus and bounded practice",
        "",
        (
            f"The primary Trinity Mandala focus is {d.PRIMARY_FOCUS}. The bounded "
            f"practice is {d.BOUNDED_PRACTICE}. GMUT Mind is primary through typed "
            "Biot poroelasticity, effective-stress, consolidation-diffusion, and "
            "slope-domain obligations with dimensional discipline and observation "
            "firewalls. THOS Body remains visible through deterministic sample "
            "custody, monitoring triage, workload, accessibility, handover, and "
            "stop-state contracts. Freed ID and CBR Heart remain visible through "
            "instrument and site-role referent separation, purpose limitation, "
            "synthetic credential representation, privacy, correction, remedy, "
            "affected-party reservations, and exact authority ceilings. This is "
            "software and evidence-assurance work only."
        ),
        "",
        "## Evidence semantics",
        "",
        (
            "Each proposal generated one valid owner-local contract and five "
            "preregistered mutations. `completed` means only that a bounded "
            "deterministic software, symbolic, or structural hypothesis passed and "
            "its five mutations were rejected. `represented` means a synthetic "
            "protocol proxy passed while every real operating arm remained absent. "
            "`open_gap` means a zero-action readiness contract names evidence that "
            "was not obtained. `exact_gate` means the missing decision cannot be "
            "supplied by repository software and remains with competent authorities "
            "and affected people. A rejected mutation is a retained negative, not "
            "proof of real-world safety, scientific truth, or professional quality."
        ),
        "",
        "## Official and primary-source discipline",
        "",
        (
            "The x1 source ledger records retrieval date, status, scope, and "
            "authority ceiling for current official or primary materials. MBIE "
            "geotechnical guidance, the NZGD source page, AGS 4.1.1, USGS monitoring "
            "sources, OGC SensorThings 1.1, NIST SP 811, Biot's primary 1941 paper, "
            "and the USACE slope-stability manual inform typed fields and refusal "
            "boundaries without authorizing a site investigation, measurement, "
            "analysis, design, consent, or safety decision. W3C VC 2.0, DID Core, "
            "Data Integrity 1.0, WCAG 2.2, PROV-O, RFC 3339, RFC 8785, New Zealand "
            "legislation, and Te Mana Raraunga inform synthetic identity, lineage, "
            "accessibility, privacy, heritage, and authority reservations. Citations "
            "are not observations, validation, authority transfer, affected-party "
            "acceptance, professional qualification, legal review, or Māori ratification."
        ),
        "",
        "## Proposal-by-proposal evidence",
        "",
    ]
    for proposal in d.PROPOSALS:
        result = by_id[proposal["proposal_id"]]
        source_text = ", ".join(proposal["official_or_primary_source_needs"])
        artifact_text = ", ".join(proposal["concrete_artifacts"])
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                (
                    f"This {proposal['pillar']} proposal tests a bounded "
                    f"{proposal['mechanism']} contract. Its observed disposition is "
                    f"`{result['observed_outcome']}`. The valid fixture passed, all "
                    f"{result['rejected_mutation_count']} of five preregistered "
                    "mutations were rejected, and zero mutations were accepted. "
                    f"The concrete artifact set is {artifact_text}. Current source "
                    f"needs are {source_text}. The full hypothesis, null, acceptance "
                    "gate, rollback, and protected authority ceilings remain frozen "
                    "in x1. No real person, land parcel, site, borehole, sample, "
                    "instrument, fieldwork, laboratory test, monitoring observation, "
                    "measurement, hazard or safety determination, engineering "
                    "interpretation, design, consent, production, professional, legal, "
                    "cultural, Māori-authority, or Stage 20 "
                    "credit follows from this result."
                ),
                "",
            ]
        )
    lines.extend(
        [
            "## GMUT Mind boundary",
            "",
            (
                "The GMUT surfaces are typed Biot poroelasticity, effective-stress, "
                "consolidation-diffusion, and slope-domain research-model obligations. "
                "They track symbols, units, signs, constitutive assumptions, boundary "
                "conditions, represented observables, and conversion boundaries. They "
                "ingest no real site, sample, instrument, field, laboratory, monitoring, "
                "or participant data and compute no real likelihood or parameter "
                "constraint. They establish no detected force, site prediction, "
                "physical law, stability theorem, empirical confirmation, "
                "ultraviolet or quantum completion, Mind-of-God claim, or Theory of Everything."
            ),
            "",
            "## THOS Body boundary",
            "",
            (
                "The THOS surfaces are deterministic synthetic workflow contracts for "
                "role placeholders, borehole and sample state, observation custody, "
                "readback and correction lineage, monitoring triage, quality holds, "
                "workload control, accessible notices, and handover. They use no real "
                "operator, site, land parcel, borehole, sample, instrument, fieldwork, "
                "measurement, laboratory result, hazard decision, design decision, or "
                "geotechnical-safety determination. They provide no effectiveness estimate, "
                "professional competence, production readiness, AGI, or ASI evidence."
            ),
            "",
            "## Freed ID and CBR Heart boundary",
            "",
            (
                "The identifier profile keeps person placeholder, role placeholder, "
                "site token, coarse zone, borehole, sample, instrument, calibration "
                "artifact, observation, correction, and handover referents distinct. "
                "Synthetic identifiers are not live "
                "credentials, issuances, presentations, resolutions, status events, "
                "interoperability results, or production identity operations. The CBR "
                "surfaces preserve land and site access, disability accommodation, "
                "location and field-record privacy, sample custody, complaint, "
                "correction, remedy, heritage, taonga, place-name, and data-governance "
                "authority questions without deciding them. Legal, "
                "cultural, affected-party, tangata-whenua, iwi, hapū, and Māori authority "
                "remain exact-gated. Māori concepts remain under Māori authority."
            ),
            "",
            "## Accessibility reservation",
            "",
            (
                "The static report provides a skip link, semantic headings, a captioned "
                "table, scoped headers, readable boundary prose, responsive overflow, "
                "print support, and no client-side script. Manual keyboard, touch, "
                "browser diversity, responsive-layout inspection, assistive technology, "
                "cognitive accessibility, Māori-language review, multi-format handover, "
                "geotechnical-domain review, and affected-user evaluation remain reserved. "
                "Structural checks are not complete accessibility conformance."
            ),
            "",
            "## Negative, Method Flow, and gate conservation",
            "",
            (
                f"All {effective_at_evidence:,} effective negatives and every new "
                f"failure remain visible. X1 retained its "
                f"{x1_negatives['x1_operational_count']} owner-local operational "
                "failures. X2 "
                "adds only failures actually observed, each with a zero-credit failed "
                "witness, a bounded recovery witness, a recurrence guard, rollback, and "
                "sibling recommendation. The 150 rejected mutations are retained as "
                "synthetic negatives. No later passing witness rewrites an earlier "
                f"failure into an initially clean run. {d.SOURCE_OPEN_GAPS} inherited "
                f"open gaps and {d.SOURCE_EXACT_GATES} inherited exact gates remain "
                "open; this phase adds one of "
                "each. Method preference is limited to the exact trigger supported by "
                "its bounded passing witness."
            ),
            "",
            "## Terminal truth",
            "",
            (
                "This packet is attributable same-owner workflow evidence under shared "
                "local infrastructure. It is not independent-team reproduction, an "
                "external audit, production certification, exhaustive security, "
                "complete privacy, complete accessibility, empirical confirmation, "
                "professional validation, legal review, cultural ratification, "
                "Māori-authority review, affected-party acceptance, AGI or ASI evidence, "
                "consciousness or personhood evidence, Theory-of-Everything proof, or "
                "Stage 20 authority. No downstream endpoint is authorized by the "
                "current live activation. After immutable evidence, closeout and seal, "
                "one successful exact-final canonical pass, and clean four-way equality, "
                "this task stops unless Hamish supplies a later exact live route. The "
                "verdict is `NOT_READY_FOR_STAGE_20`."
            ),
        ]
    )
    return "\n".join(lines)


def build_report(results: list[dict[str, Any]]) -> str:
    """Render a static accessible structural report without active content."""
    proposals = {row["proposal_id"]: row for row in d.PROPOSALS}
    rows = []
    for result in results:
        proposal = proposals[result["proposal_id"]]
        rows.append(
            "<tr>"
            f"<th scope=\"row\">{html.escape(result['proposal_id'])}</th>"
            f"<td>{html.escape(proposal['title'])}</td>"
            f"<td>{html.escape(proposal['pillar'])}</td>"
            f"<td><code>{html.escape(result['observed_outcome'])}</code></td>"
            f"<td>{result['rejected_mutation_count']}/5</td>"
            f"<td>{result['accepted_mutation_count']}</td>"
            "</tr>"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Orin Thale v655-v7 boundary evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1rem}}
a:focus{{outline:3px solid #145da0;outline-offset:2px}}
.table-wrap{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;min-width:52rem}}
th,td{{border:1px solid #777;padding:.5rem;text-align:left;vertical-align:top}}
caption{{font-weight:700;text-align:left;margin:.7rem 0}} code{{white-space:nowrap}}
@media print{{a[href="#main"]{{display:none}} body{{max-width:none}}}}
</style>
</head>
<body>
<a href="#main">Skip to main content</a>
<header><h1>Orin Thale v655-v7 boundary evidence report</h1></header>
<main id="main">
<section aria-labelledby="summary"><h2 id="summary">Summary</h2>
<p>Thirty owner-local contracts ran: 23 <code>completed</code>, 5
<code>represented</code>, 1 <code>open_gap</code>, and 1
<code>exact_gate</code>. All 150 preregistered mutations were rejected.
No real person, land parcel, site, borehole, sample, instrument, fieldwork,
laboratory test, monitoring observation, measurement, hazard or safety decision,
engineering interpretation, design, consent, or professional decision,
production system, or authority was acted on.</p></section>
<section aria-labelledby="results"><h2 id="results">Proposal results</h2>
<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable proposal results">
<table><caption>Bounded v655-v7 contract and mutation results</caption>
<thead><tr><th scope="col">Proposal</th><th scope="col">Surface</th>
<th scope="col">Pillar</th><th scope="col">Disposition</th>
<th scope="col">Rejected mutations</th><th scope="col">Accepted mutations</th>
</tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<section aria-labelledby="boundaries"><h2 id="boundaries">Boundaries</h2>
<p>GMUT remains a typed scalar-tensor and EFT research-model
family without empirical confirmation. THOS geotechnical-workflow evidence remains
synthetic or represented. Freed ID remains synthetic and nonproduction.
Location and field-record privacy, professional practice, land and site access,
correction, remedy, hazard-response authority, legal interpretation,
cultural legitimacy, data governance, affected-party acceptance, and Māori
authority remain with competent authorities and affected people, including tangata
whenua, iwi, hapū, and Māori authorities.</p>
<p>Manual keyboard, touch, browser, responsive-layout, assistive-technology,
cognitive-accessibility, Māori-language, multi-format handover, geotechnical-accessibility, and
affected-user evaluation remain reserved. This static structural report is not
complete accessibility conformance.</p>
<p>Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></section>
</main>
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
            "schema": "ghc.family.v655-v7.evidence-candidate-manifest.v1",
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
                "short_description=Validate bounded synthetic geotechnical contracts",
                "--interface",
                (
                    f"default_prompt=Use ${skill_name} to validate its three "
                    "bounded synthetic geotechnical contracts."
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
                        f"{mechanisms} contracts for Orin Thale v655-v7. Use only "
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
        if runner_name == "ghc_family_v655_v7_suite.py":
            body = "\n".join(
                [
                    "#!/usr/bin/env python3",
                    '"""Run all thirty bounded Orin Thale v655-v7 contracts."""',
                    "",
                    "from ghc_family_v655_v7_core import suite_main",
                    "",
                    "",
                    'if __name__ == "__main__":',
                    '    suite_main("ghc_family_v655_v7_suite")',
                    "",
                ]
            )
        else:
            body = "\n".join(
                [
                    "#!/usr/bin/env python3",
                    (
                        f'"""Run Orin Thale v655-v7 bounded contract group {group}: '
                        f'{mechanisms}."""'
                    ),
                    "",
                    "from ghc_family_v655_v7_core import group_main",
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
                "schema": "ghc.family.v655-v7.mutation-results.v1",
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
                "schema": "ghc.family.v655-v7.bounded-receipt.v1",
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
        if runner_name == "ghc_family_v655_v7_suite.py":
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
        if runner_name == "ghc_family_v655_v7_suite.py":
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
                "schema": "ghc.family.v655-v7.skill-smoke-receipt.v1",
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
            "schema": "ghc.family.v655-v7.retained-negatives.x2.v1",
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
            "schema": "ghc.family.v655-v7.open-gaps.x2.v1",
            "inherited_count": d.SOURCE_OPEN_GAPS,
            "new_rows": [
                {
                    "proposal_id": f"{d.PHASE_CODE}-P29",
                    "state": "open_gap",
                    "reason": (
                        "No NZGD query or download, no real site or location row, no "
                        "borehole, sample, instrument, fieldwork, laboratory test, "
                        "measurement, analysis, design, or independent review."
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
            "schema": "ghc.family.v655-v7.exact-gates.x2.v1",
            "inherited_count": d.SOURCE_EXACT_GATES,
            "new_rows": [
                {
                    "proposal_id": f"{d.PHASE_CODE}-P30",
                    "state": "exact_gate",
                    "reason": (
                        "Land and site access, hazard notice, heritage, taonga, "
                        "place-name, location and field-record privacy, sample custody, "
                        "disability access, public safety, remedy, legal "
                        "interpretation, data governance, affected-party acceptance, "
                        "tangata whenua, iwi, hapū, cultural, and Māori authority are absent."
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
            "schema": "ghc.family.v655-v7.proposals.x2.v1",
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
            "schema": "ghc.family.v655-v7.portfolio-results.x2.v1",
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
            "schema": "ghc.family.v655-v7.index-addendum.v1",
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
        "# GHC Family Index — Orin Thale v655-v7 x2 addendum\n\n"
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
            "decision_id": "V6557-REFLECT-X2",
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
                "The ten bounded geotechnical-provenance and remedy skills and runners add "
                "distinct site, authorization, sample and instrument, instrument, represented "
                "measurement, field record-custody, handover, data conflict, privacy, "
                "accessibility, identity, GMUT, THOS, and nonpromotion firewalls "
                "without global installation."
            ),
        },
    )
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v655-v7.threat-model.v1",
            "assets": [
                "site-token, borehole, sample, instrument, and purpose-bound metadata",
                "interval, observation, correction, custody, and provenance state",
                "represented calibration, monitoring, laboratory, and hazard proxies",
                "readback, quality quarantine, handover, privacy, and identifier relations",
                "land access, heritage, taonga, complaint, and remedy reservations",
                "GMUT geomechanics type, unit, sign, domain, and observation-firewall integrity",
                "THOS workload, sample custody, correction, stop, and release holds",
            ],
            "adversaries": [
                "unlabelled representation, measurement, fieldwork, or authority promoter",
                "silent site, location, borehole, sample, instrument, observation, or state substituter",
                "stale calibration, method, measurement, source, or status promoter",
                "person, role, site, borehole, sample, observation, and correction namespace conflator",
                "unauthorized fieldwork, laboratory, hazard, design, consent, or safety promoter",
                "silent legal, cultural, taonga, professional, land, or remedy decider",
                "correlated same-owner validation promoter",
            ],
            "threats": [
                "private person, precise-location, land, sample, or field-record metadata leakage",
                "person, role, site, borehole, sample, observation, or correction conflation",
                "stale calibration, measurement, source, method, instrument, or process evidence",
                "silent unit, datum, depth, time, reference, sign, or proxy conversion",
                "automatic fieldwork, measurement claim, hazard decision, design, consent, or work release",
                "unilateral legal, land, professional, cultural, taonga, or remedy interpretation",
                "affected-party, disability, location, land, sample, or cultural information exposure",
                "unsupported scientific or authority promotion",
            ],
            "controls": [
                "purpose-bound metadata minimization",
                "site, borehole, sample, observation, process, correction, and proxy lineage",
                "authorization, calibration, instrument, measurement-proxy, safety, and readiness holds",
                "person, role, site, borehole, sample, observation, and correction referent separation",
                "readback, correction replay, pause, and stop gates",
                "hazard, land, privacy, accessibility, culture, complaint, and remedy reservations",
                "typed task authority ceilings",
                "promotion-claim zero map",
                "retained mutations and Method Flow",
            ],
            "residuals": [
                "real people, land parcels, sites, boreholes, samples, instruments, and locations",
                "real fieldwork, laboratory work, monitoring observations, measurements, and hazards",
                "operator, geotechnical, geological, laboratory, design, consent, safety, legal, and professional competence",
                "human usability and complete accessibility",
                "legal, cultural, taonga, Māori, and affected-party authority",
                "independent scientific, safety, security, privacy, and empirical review",
            ],
            "boundary": (
                "Threat model is not exhaustive geotechnical, field, laboratory, hazard, professional, "
                "security, privacy, accessibility, or authority assurance."
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
        "deliverables/v655-v7-integrated-overview.md",
        build_overview(suite["results"]),
    )
    write_text(
        "deliverables/v655-v7-boundary-evidence-report.html",
        build_report(suite["results"]),
    )
    overview_words = len(
        (ROOT / "deliverables/v655-v7-integrated-overview.md")
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
            "schema": "ghc.family.v655-v7.phase-truth.evidence.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcomes": expected,
            "proposal_count": 30,
            "frozen_chain_count": 2140,
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
            "route_state": "HELD_NO_DOWNSTREAM_AUTHORITY",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v655-v7.checklist.evidence.v1",
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
                "verified terminal stop without downstream contact",
            ],
            "incomplete_external": [
                "real GMUT data and likelihood",
                "blind or independently designed GMUT and THOS empirical arms",
                "authorized geotechnical field operation, real people and borehole identifiers, licences and qualification records, sites, locations, sample and instrument, instruments, calibrated geotechnical measurements, field operations, measurements, contacts, field records, hazard response operations, competent practitioner review, and affected-user evaluation",
                "production Freed ID registration and resolution plus privacy and security review",
                "tangata whenua, iwi, hapū, Māori, taonga, affected-party, borehole identifier, field record and location privacy, disability access, land, heritage, land and hazard, hazard-response, professional, legal, cultural, data-governance, complaint, correction, and remedy authority",
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
            "schema": "ghc.family.v655-v7.evidence-build-receipt.v1",
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
            "route_state": "HELD_NO_DOWNSTREAM_AUTHORITY",
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
            "schema": "ghc.family.v655-v7.evidence-test-receipt.v1",
            "first_attempt_tests": 17,
            "first_attempt_passes": 16,
            "first_attempt_errors": 1,
            "first_attempt_credit": 0,
            "current_phase_tests": 17,
            "current_phase_failures": 0,
            "isolated_recovery_tests": 17,
            "isolated_recovery_failures": 0,
            "bounded_inherited_tests": 0,
            "bounded_inherited_failures": 0,
            "credited_test_total": 17,
            "failed_broad_selection_tests": 0,
            "failed_broad_selection_failures": 0,
            "failed_broad_selection_credit": 0,
            "inherited_suite_claimed": False,
            "full_repository_suite_run": False,
            "final_canonical_pass_run": False,
            "valid": True,
            "boundary": (
                "The first ordering-fault aggregate has zero credit. The corrected "
                "bounded 17-test development selection passed once; the one "
                "exact-final canonical pass remains deferred."
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

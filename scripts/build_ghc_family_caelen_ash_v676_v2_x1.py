#!/usr/bin/env python3
"""Build the deterministic planning-only Caelen Ash v676-v2 x1 packet."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Caelen Ash"
OWNER_SLUG = "caelen-ash"
PHASE = "v676-v2"
BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v676-v1-full-tools"
SOURCE = "939312172819669aad250cf034d8a6a7efe3df5b"
INHERITED_SOURCE = "0f330a562377a90c8c8eb31515a0ff02551fbdbf"
SABLE_X1 = "18c4e98ead5d81875c1ffaf7cb2238c34d9b5407"
SABLE_EVIDENCE = "bb04bce8a0f4b3f6d50d839b1ee237da817e369f"
SABLE_FIRST_CLOSEOUT = "e75ca31a34c8569eee5b603fec2ab96a4ac1f77e"
GENERATED_DATE = "2026-08-30"

ACTIVATION = {
    "declared_proposals": 7430,
    "effective_negatives": 41662,
    "effective_methods": 30754,
    "retained_failed_witnesses": 13323,
    "bounded_passing_witnesses": 18120,
    "open_gaps": 349,
    "exact_gates": 341,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

TITLES = [
    "Carrier-medium identity versus recorded-content identity separation",
    "Reel side track and channel topology contract",
    "Nominal tape-speed rational-unit typing",
    "Actual tape-speed unknown versus estimated state separation",
    "Playback timebase source-lineage ledger",
    "Wow-and-flutter proxy nonmeasurement firewall",
    "Azimuth-setting provenance without optimum claim",
    "Equalization-curve declaration and version ledger",
    "Track-format and head-stack compatibility hold",
    "Direction and reverse-play sequence graph",
    "Program-end versus physical-carrier-end sentinel record",
    "Counter index versus elapsed-time distinction",
    "Cue-time monotonicity and overlap tribunal",
    "Dropout-region unknown and withheld marker",
    "Calibration-tone identity version and fixity record",
    "Reference-fluxivity vocabulary nonmeasurement hold",
    "Ordered playback-chain state snapshot with component-set hash",
    "Sample-rate bit-depth and codec separation",
    "Channel mapping and polarity-inversion guard",
    "Transfer-event source-to-derivative fixity graph",
    "Speed-correction transform and reversible rollback",
    "Azimuth-correction alternative-set log with nonselection authority hold",
    "Encoded noise-reduction system claim and decode-prohibition contract",
    "Level-and-gain adjustment provenance without loudness claim",
    "Unedited-transfer coverage map with exception-only edit deltas",
    "Resampling clock-domain change receipt",
    "Deterministic checksum export package",
    "Keyboard-independent cue-table navigation and non-audio evidence index",
    "Human audition of dropout and distortion evidence vacancy",
    "Professional playback-alignment and carrier-handling proxy boundary",
    "Physical carrier-condition inspection and treatment hold",
    "Reference-level chain traceability evidence vacancy",
    "Recording-rightsholder contest and donor-restriction proxy",
    "Deaf and hard-of-hearing user review of non-audio navigation vacancy",
    "Broadcast-Wave metadata round-trip field-loss vacancy",
    "THOS two-person playback-start interlock and fatigue-stop proxy",
    "Real transfer-dataset and preregistered-analysis gap",
    "Longitudinal transfer-error and damage-outcome independent-review gap",
    "Orphan-work recording access donor-restriction and copyright-authority exact gate",
    "Recorded cultural-knowledge tikanga-access and Maori-authority exact gate",
]

NEIGHBORS = [
    (0.5271, "SR6761-N028", "Declared OGC conformance class versus executed-test separation", "docs/sable-rook/v676-v1/final/source-and-proposal-ledger.json"),
    (0.6286, "VA6736-N002", "Sextant frame, limb, index arm, pivot, and arc topology contract", "docs/vesper-arlen/v673-v6/x1/proposals.json"),
    (0.5412, "SR6723-P034", "Professional and operational authority vacancy", "docs/sable-rook/v672-v3/x1/proposals/new-proposal-freeze.json"),
    (0.5565, "SR6723-P006", "Known-cause, suspected-cause, and unknown-cause separation", "docs/caelen-ash/v672-v4/x1/proposals/inherited-zero-credit-review.json"),
    (0.5758, "LV6745-P012", "Backing Board Lineage Graph", "docs/liora-venn/v674-v5/x1/proposals/new-proposal-freeze.json"),
    (0.5714, "LV6745-P035", "Fastener Pressure Nonmeasurement", "docs/liora-venn/v674-v5/x1/proposals/new-proposal-freeze.json"),
    (0.5586, "SR6723-P021", "Alternative-service provenance without recommendation authority", "docs/sable-rook/v672-v3/x1/proposals/new-proposal-freeze.json"),
    (0.6444, "AL6722-P015", "Redaction reason and reversibility ledger", "docs/auren-lark/v672-v2/x1/new-proposal-freeze.json"),
    (0.5783, "LV6745-P027", "Frame Material Compatibility Nonclaim", "docs/liora-venn/v674-v5/x1/proposals/new-proposal-freeze.json"),
    (0.5854, "AL6722-P015", "Redaction reason and reversibility ledger", "docs/auren-lark/v672-v2/x1/new-proposal-freeze.json"),
    (0.5138, "EL6715-N027", "Program item and carrier count-reconciliation contract", "docs/elaren-kestrel/v671-v5/x1/proposals.json"),
    (0.6190, "AL6741-N009", "Raw-versus-derived waveform distinction", "docs/auren-lark/v674-v1/x1/new-proposal-freeze.json"),
    (0.6216, "AL6722-P002", "Chronology monotonicity tribunal", "docs/auren-lark/v672-v2/x1/new-proposal-freeze.json"),
    (0.5714, "EL6715-N009", "Electrical subsystem absent unknown and prohibited-state marker", "docs/elaren-kestrel/v671-v5/x1/proposals.json"),
    (0.6299, "IF6683-N002", "calibration-target identity, version, exposure, and scan-session lineage ledger", "docs/auren-lark/v668-v4/x1/proposal-freeze-shards/proposals-01.json"),
    (0.5310, "VA6736-N024", "Component-condition vocabulary with conservation-treatment hold", "docs/vesper-arlen/v673-v6/x1/proposals.json"),
    (0.4901, "NS6678R2-N012", "typed package API surface snapshot with declaration resolution export map and diff receipt", "docs/auren-lark/v668-v4/x1/proposal-chain-audit.json"),
    (0.6479, "LV6745-P007", "Rabbet Depth Unit Declaration", "docs/liora-venn/v674-v5/x1/proposals/new-proposal-freeze.json"),
    (0.5345, "IF6683-N013", "channel-balance, lookup-table, and color-profile identity separation board", "docs/auren-lark/v668-v4/x1/proposal-freeze-shards/proposals-03.json"),
    (0.5238, "SR6742-N011", "Source-to-derivative provenance link", "docs/sable-rook/v674-v2/x1/new-proposal-freeze.json"),
    (0.5934, "AL6722-P015", "Redaction reason and reversibility ledger", "docs/auren-lark/v672-v2/x1/new-proposal-freeze.json"),
    (0.6154, "LYR6756-N026", "Unauthorized correction-action refusal with no simulated authority claim", "docs/lyren-moss/v675-v6/x1/new-proposal-freeze.json"),
    (0.5547, "CA6705-N017", "scan resolution optical sampling and pixel-scale distinction contract", "docs/caelen-ash/v670-v5/closeout/proposal-ledger-final.json"),
    (0.5210, "IF6738-N024", "Measurement and scale vacancy record without metrology claim", "docs/ilyra-fen/v673-v8/x1/proposals.json"),
    (0.4968, "LM6701-N002", "hopper bin tote and transfer-vessel alias register with location and custody claims held vacant", "docs/lyren-moss/v670-v1/x1/new-proposal-freeze.json"),
    (0.5205, "OR6744-P027", "Fermentation Clock Uncertainty Card", "docs/orin-thale/v674-v4/x1/proposals/new-proposal-freeze.json"),
    (0.5714, "SR6723-P025", "Deterministic JSON notice capsule", "docs/sable-rook/v672-v3/x1/proposals/new-proposal-freeze.json"),
    (0.5638, "SR6685-N028", "source-independent edition comparison and common-cause evidence-diversity board", "docs/caelen-ash/v668-v6/x1/proposal-freeze-shards/proposals-06.json"),
    (0.5541, "IF6721-N021", "clash issue record with object surrogate viewpoint status and resolution-evidence vacancies", "docs/ilyra-fen/v672-v1-2-remaster/x1/inherited-proposal-revalidation.json"),
    (0.5210, "SR6723-P017", "Reader acknowledgement and correction-readback proxy", "docs/caelen-ash/v672-v4/x1/proposals/inherited-zero-credit-review.json"),
    (0.6050, "VA6736-N024", "Component-condition vocabulary with conservation-treatment hold", "docs/vesper-arlen/v673-v6/x1/proposals.json"),
    (0.5806, "AL6741-N022", "Calibration-traceability authority vacancy", "docs/auren-lark/v674-v1/x1/new-proposal-freeze.json"),
    (0.5905, "SR6723-P019", "Workload-budget, hold-point, and escalation proxy", "docs/caelen-ash/v672-v4/x1/proposals/inherited-zero-credit-review.json"),
    (0.5620, "SR6761-N046", "Bilingual and Maori-language review authority vacancy", "docs/sable-rook/v676-v1/final/source-and-proposal-ledger.json"),
    (0.4961, "LM6682-N030", "THOS broadcast archive migration coordinator metadata handover practice lens", "docs/auren-lark/v668-v4/x1/proposal-freeze-shards/proposals-06.json"),
    (0.4918, "OT6725-P029", "THOS tactile-proof queue bounded retry pause and stop proxy", "docs/orin-thale/v672-v5/x1/new-proposal-freeze.json"),
    (0.5631, "CA6724-P038", "Real loom, yarn, measurement, and interoperability gap", "docs/caelen-ash/v672-v4/x1/proposals/new-proposal-freeze.json"),
    (0.5294, "EC6747-N057", "real astrolabe music-box and kaleidoscope observations measurements trials and independent-review gap", "docs/elowen-cairn/v674-v7/closeout/proposal-ledger-final.json"),
    (0.6335, "LV6707-N039", "organ safety treatment heritage access remedy and competent-authority exact gate", "docs/liora-venn/v670-v7/closeout/proposal-ledger-final.json"),
    (0.6569, "LYR6756-N040", "Cultural data-governance and Maori-authority decision exact gate", "docs/lyren-moss/v675-v6/x1/new-proposal-freeze.json"),
]

INHERITED = [
    ("LM6682-N009", "synthetic audio transfer-settings receipt with equipment and calibration authority vacancies"),
    ("AL6741-N007", "Orientation azimuth and dip uncertainty record"),
    ("LM6644-N004", "Playback-chain dependency graph with machine, head, equalization, azimuth, speed, cabling, converter, software, operator, and release-refusal vacancies"),
    ("CM6694-N017", "gain equalization denoise splice resample and unknown processing-action ledger with every real edit held"),
    ("LM6682-N004", "rational timebase and frame-rate validator that refuses lossy decimal equivalence"),
    ("LYR6663-N006", "channel orientation tribunal with azimuth-dip domains, coordinate-frame vacancy, revision epoch, and zero-polarization inference"),
    ("NE6642-N015", "Superseding amendment trail for marigram descriptive metadata with disputed station hypothesis, datum and timebase status, reason code, challenger placeholder, unresolved state, and no live governance"),
    ("VA6717-OWNER-015", "named symbolic epoch direction sequence and unit-placeholder frame forbidding undeclared timebase changes"),
    ("SR6742-N049", "Typed rational caption timebase dimension board"),
    ("VA6717-N015", "named symbolic epoch direction sequence and unit-placeholder frame forbidding undeclared timebase changes"),
    ("LM6737-N008", "Tape leader, trailer, splice, overlap, and segment-boundary ledger"),
    ("IF6683-N002", "calibration-target identity, version, exposure, and scan-session lineage ledger"),
    ("SR6742-N046", "Assistive-technology evaluation vacancy"),
    ("SR6761-N050", "Cross-catalog interoperability event vacancy"),
    ("SR6723-P031", "THOS interruption workload and handover proxy"),
    ("LYR6756-N040", "Cultural data-governance and Maori-authority decision exact gate"),
    ("SR6742-N045", "Manual keyboard evaluation vacancy"),
    ("SR6761-N041", "Accessible tabular alternative for synthetic map extents"),
    ("SR6742-N011", "Source-to-derivative provenance link"),
    ("AL6722-P002", "Chronology monotonicity tribunal"),
]

SOURCES = [
    {
        "source_id": "IASA-TC04",
        "url": "https://www.iasa-web.org/tc04/audio-preservation",
        "status": "official web edition; Second Edition 2009",
        "use": "audio-preservation vocabulary and refusal conditions only",
    },
    {
        "source_id": "FADGI-AUDIO",
        "url": "https://www.digitizationguidelines.gov/guidelines/digitize-audioperf.html",
        "status": "official federal guidance page checked 2026-08-30; page notes ADCTest is no longer maintained",
        "use": "measurement and equipment-evidence vacancy vocabulary only",
    },
    {
        "source_id": "EBU-TECH-3285-V2",
        "url": "https://tech.ebu.ch/docs/tech/tech3285.pdf",
        "status": "official Broadcast Wave Format Version 2 specification",
        "use": "BWF field vocabulary only; no conformance claim",
    },
    {
        "source_id": "PREMIS-3",
        "url": "https://www.loc.gov/standards/premis/v3/index.html",
        "status": "Library of Congress current PREMIS version 3.0 page",
        "use": "object, event, rights, and agent vocabulary only",
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation 2013",
        "use": "provenance vocabulary only",
    },
    {
        "source_id": "WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation 12 December 2024",
        "use": "accessible-report design vocabulary; manual and affected-user evaluation reserved",
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational RFC, June 2020",
        "use": "deterministic JSON vocabulary; no cryptographic or production assurance",
    },
]

PROTECTED_GATES = [
    "no real carrier, recording, playback equipment, measurement, operator, participant, or collection action",
    "no empirical GMUT result, likelihood, posterior, force, prediction, or parameter constraint",
    "no THOS operational-effectiveness, safety, professional-competence, AGI, or ASI claim",
    "no production Freed ID key, proof, issuance, resolution, revocation, interoperability, or trust-governance claim",
    "no copyright, donor, access, remedy, cultural, affected-party, tikanga, taonga, Maori-data-governance, or Maori-authority decision",
    "no complete privacy, accessibility, exhaustive-security, independent-reproduction, consciousness, personhood, proof, canon, or Stage 20 claim",
]


def run(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def proposals() -> list[dict[str, Any]]:
    rows = []
    for offset, title in enumerate(TITLES, start=1):
        pid = f"CA6762-N{offset:03d}"
        if offset <= 28:
            disposition, approval, lane = "completed", "safe_now", "owner_local_synthetic"
        elif offset <= 36:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 38:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "authority_reserved"
        source_ids = ["IASA-TC04", "PREMIS-3", "W3C-PROV-O", "RFC-8785"]
        if offset in {18, 20, 26, 27, 35}:
            source_ids.append("EBU-TECH-3285-V2")
        if offset in {6, 15, 16, 29, 30, 31, 32, 37, 38}:
            source_ids.append("FADGI-AUDIO")
        if offset in {28, 34}:
            source_ids.append("WCAG-2.2")
        rows.append(
            {
                "proposal_id": pid,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can encode {title.lower()} "
                    "while refusing conversion into a real measurement, professional decision, production act, or authority grant."
                ),
                "null_or_failure_condition": (
                    f"The {pid} contract accepts a missing or contradictory field, changes the source/derivative meaning, "
                    "uses an unapproved outcome label, or implies real-world evidence or authority."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": sorted(set(source_ids)),
                "concrete_artifacts": [
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/contracts/{pid}.json",
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{pid}-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    f"One positive synthetic fixture must satisfy the {pid} schema and each of four preregistered invalid mutations "
                    "must be rejected; represented, open, and exact-gated rows receive no executed-real-world credit."
                ),
                "rollback_or_recovery": (
                    f"Quarantine the {pid} output, retain the failed witness, restore the last exact Git-blob input, "
                    "and rerun only the isolated dependency after an additive correction."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
            }
        )
    return rows


def mutation_plan(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mutations = []
    mutation_types = [
        ("missing_hypothesis", "required hypothesis omitted"),
        ("unknown_outcome_label", "outcome label outside the four-label vocabulary"),
        ("authority_escalation", "synthetic record claims real-world authority or completion"),
        ("source_derivative_conflation", "source and derivative identities are collapsed"),
    ]
    for row in rows:
        for index, (kind, reason) in enumerate(mutation_types, start=1):
            mutations.append(
                {
                    "mutation_id": f"{row['proposal_id']}-M{index}",
                    "proposal_id": row["proposal_id"],
                    "mutation_kind": kind,
                    "expected_rejection": reason,
                    "execution_status": "preregistered_unexecuted_x1",
                }
            )
    return mutations


def safe_tasks(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    setup = [
        "Reconfirm immutable Sable source anchors",
        "Reconfirm direct-parent zero-merge lifecycle",
        "Reconfirm clean fresh four-way source equality",
        "Freeze exact sparse owner patterns",
        "Record proposal-object audit coverage",
        "Record rejected high-similarity draft ideas",
        "Freeze official-source status ledger",
        "Freeze GMUT nonconversion firewall",
        "Freeze THOS proxy boundary",
        "Freeze Freed ID nonproduction boundary",
        "Freeze CBR authority reservation",
        "Freeze relational identity disclaimer",
        "Freeze five-class privacy taxonomy",
        "Freeze raw-identifier exclusion rules",
        "Freeze deterministic UTF-8 JSON contract",
        "Freeze normalized-LF Git-blob contract",
        "Build immutable x1 manifest",
        "Build exact x1 staged review",
        "Prove x2 paths absent at x1",
        "Freeze protected-gate register",
    ]
    execution = [f"Build bounded positive contract fixture for {row['proposal_id']}: {row['title']}" for row in rows[:28]]
    terminal = [
        "Build four-mutation-per-proposal preregistration index",
        "Check mutation identifiers for exact proposal ownership",
        "Check expected-disposition cardinality",
        "Check four-label outcome vocabulary",
        "Check owner path rotation ceiling",
        "Check commit-stage ceiling",
        "Build append-only Method Flow ledger",
        "Record environment versions without updates",
        "Build accessible static evidence summary",
        "Record wellbeing and workload hold points",
        "Build rollback and recurrence-guard index",
        "Hold terminal route until exact-final validation",
    ]
    titles = setup + execution + terminal
    assert len(titles) == 60
    return [
        {
            "task_id": f"CA6762-SAFE-{i:03d}",
            "title": title,
            "approval_class": "safe_now",
            "status": "planned_unexecuted_x1",
            "scope": "owner_local_additive",
        }
        for i, title in enumerate(titles, start=1)
    ]


def candidate_tasks(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    titles = [f"Represent or preserve vacancy for {row['proposal_id']}: {row['title']}" for row in rows[28:38]]
    titles += [
        "Compare rational and decimal speed labels without choosing a real value",
        "Model alternate channel maps without asserting a real carrier layout",
        "Model alternate equalization labels without selecting a playback curve",
        "Model unknown noise-reduction state without decoding",
        "Model reversible timebase transforms with synthetic values only",
        "Model dropout intervals without listening or diagnosis",
        "Model chain-component ordering without equipment recommendation",
        "Model BWF field loss without a production interchange event",
        "Model cue-table navigation without affected-user evaluation",
        "Model rights contest states without a legal determination",
        "Model donor restriction states without custody authority",
        "Model workload pauses without operator-performance claims",
        "Model second-check handoff without employment or supervision authority",
        "Model traceability vacancy without calibration certification",
        "Model carrier condition vocabulary without inspection",
        "Model access alternatives without affected-party acceptance",
        "Model cultural-knowledge holds without cultural interpretation",
        "Model synthetic provenance corrections without authenticity claims",
        "Model source/derivative checksums without production trust",
        "Model longitudinal-study requirements without data acquisition",
    ]
    assert len(titles) == 30
    return [
        {
            "task_id": f"CA6762-CAND-{i:03d}",
            "title": title,
            "approval_class": "candidate",
            "status": "planned_unexecuted_x1",
            "promotion_gate": "bounded synthetic acceptance plus every protected gate preserved",
        }
        for i, title in enumerate(titles, start=1)
    ]


def approval_packets() -> dict[str, Any]:
    exact = [
        "Real magnetic carrier handling or playback",
        "Real tape-condition inspection or treatment",
        "Real playback alignment or equipment calibration",
        "Real signal measurement or quality judgment",
        "Real collection custody or transfer decision",
        "Copyright or orphan-work determination",
        "Donor-restriction interpretation",
        "Affected-rightsholder access or contest resolution",
        "Accessibility conformance claim",
        "Affected-user acceptance claim",
        "Production BWF interoperability certification",
        "Production Freed ID key or proof lifecycle",
        "Live participant or operator study",
        "Professional audio-preservation recommendation",
        "Public-safety or operational release",
        "Legal right or remedy",
        "Cultural legitimacy or recorded-knowledge meaning",
        "Tikanga or taonga-status interpretation",
        "Maori wording or Maori data-governance decision",
        "Stage 20, proof, canon, AGI, ASI, consciousness, or personhood claim",
    ]
    blocked = [
        "Credential, private-key, token, or account use",
        "Host-security weakening, elevation, Windows-feature change, or reboot",
        "Destructive deletion or rewrite of sibling or shared history",
        "Global installation or PATH promotion of phase-local packages",
        "Real participant recruitment or real-world operation",
        "Unreviewed external data ingestion",
        "Secret or private route material in durable artifacts",
        "Full-repository suite outside current authorization",
        "Second canonical invocation after success",
        "Successor contact before terminal route gate",
    ]
    return {
        "exact_approval": [
            {
                "packet_id": f"CA6762-EXACT-{i:03d}",
                "title": title,
                "status": "unexecuted_exact_gate",
                "authority_required": True,
            }
            for i, title in enumerate(exact, start=1)
        ],
        "blocked": [
            {
                "packet_id": f"CA6762-BLOCK-{i:03d}",
                "title": title,
                "status": "blocked_unexecuted",
                "override_by_safe_now": False,
            }
            for i, title in enumerate(blocked, start=1)
        ],
    }


def skill_runner_plan() -> dict[str, Any]:
    skill_names = [
        "magnetic-carrier-identity-separator",
        "reel-track-topology-checker",
        "tape-speed-unit-guard",
        "timebase-lineage-auditor",
        "wow-flutter-nonmeasurement-firewall",
        "azimuth-provenance-guard",
        "equalization-version-ledger",
        "head-stack-compatibility-hold",
        "playback-sequence-graph",
        "program-end-sentinel",
        "cue-overlap-tribunal",
        "dropout-unknown-marker",
        "calibration-tone-fixity",
        "fluxivity-authority-hold",
        "derivative-format-separator",
        "polarity-mapping-guard",
        "transfer-fixity-graph",
        "transform-rollback-auditor",
        "processing-action-declaration",
        "accessible-cue-navigator",
    ]
    runners = [
        "ghc_family_caelen_ash_v676_v2_proposal_contracts.py",
        "ghc_family_caelen_ash_v676_v2_positive_controls.py",
        "ghc_family_caelen_ash_v676_v2_mutation_rejector.py",
        "ghc_family_caelen_ash_v676_v2_timebase_ledger.py",
        "ghc_family_caelen_ash_v676_v2_playback_graph.py",
        "ghc_family_caelen_ash_v676_v2_provenance.py",
        "ghc_family_caelen_ash_v676_v2_privacy.py",
        "ghc_family_caelen_ash_v676_v2_portfolio.py",
        "ghc_family_caelen_ash_v676_v2_method_flow.py",
        "build_ghc_family_caelen_ash_v676_v2_report.py",
    ]
    return {
        "phase_local_skills": [
            {
                "skill_id": f"CA6762-SKILL-{i:02d}",
                "name": name,
                "status": "planned_unbuilt_x1",
                "global_install": False,
                "required_lifecycle": ["customize", "quick_validate", "smoke_use"],
            }
            for i, name in enumerate(skill_names, start=1)
        ],
        "family_current_runners": [
            {
                "runner_id": f"CA6762-RUNNER-{i:02d}",
                "name": name,
                "status": "planned_unbuilt_x1",
                "compatibility": "preserve family-current ghc_family or build_ghc_family caller surface",
            }
            for i, name in enumerate(runners, start=1)
        ],
        "successor_skill_recommendations": [
            {"recommendation_id": f"CA6762-NEXT-SKILL-{i:02d}", "title": f"Successor review of {name}", "credit": "zero_caelen_completion_credit"}
            for i, name in enumerate(skill_names[:10], start=1)
        ],
        "successor_runner_recommendations": [
            {"recommendation_id": f"CA6762-NEXT-RUNNER-{i:02d}", "title": f"Successor compatibility audit for {name}", "credit": "zero_caelen_completion_credit"}
            for i, name in enumerate(runners, start=1)
        ],
    }


def clean_fix_refine() -> dict[str, Any]:
    scopes = [
        "proposal contracts", "mutation fixtures", "positive controls", "source labels", "truth labels",
        "authority holds", "privacy scanner", "raw-identifier scanner", "JSON serialization", "LF normalization",
        "Git-blob manifests", "staged review", "sparse ownership", "path rotation guard", "commit ceiling",
        "x1 lifecycle test", "x2 lifecycle test", "Method Flow ledger", "failure linkage", "recovery linkage",
        "skill metadata", "skill smoke receipts", "runner interfaces", "runner help text", "compatibility aliases",
        "static report", "accessible tables", "wellbeing holds", "rollback records", "route hold",
    ]
    actions = ["CLEAN deterministic residue from", "FIX bounded validation for"]
    owner = []
    for action in actions:
        for scope in scopes:
            owner.append(f"{action} {scope}")
    assert len(owner) == 60
    successor = [f"REFINE successor-facing compatibility notes for {scope}" for scope in scopes]
    return {
        "owner_tasks": [
            {
                "task_id": f"CA6762-CFR-{i:03d}",
                "title": title,
                "status": "planned_unexecuted_x1",
                "scope": "owner_local_additive_only",
            }
            for i, title in enumerate(owner, start=1)
        ],
        "successor_recommendations": [
            {
                "task_id": f"CA6762-NEXT-CFR-{i:03d}",
                "title": title,
                "status": "recommendation_only",
                "credit": "zero_caelen_completion_credit",
            }
            for i, title in enumerate(successor, start=1)
        ],
    }


def method_flow() -> dict[str, Any]:
    failed = [
        ("CA6762-START-N001", "PowerShell foreach output was piped without materialization, causing an empty-pipe parser fault before read or mutation.", "CA6762-START-P001"),
        ("CA6762-START-N002", "Combined branch, storage, and live-availability probe returned no attributable output after the bounded wait.", "CA6762-START-P002"),
        ("CA6762-START-N003", "First read-only manifest replay crossed the initial wait and its wrapper session handle was not retained.", "CA6762-START-P003"),
        ("CA6762-START-N004", "Archive-wide external receipt filename search exceeded 150 seconds and was interrupted with no result.", "CA6762-START-P004"),
        ("CA6762-START-N005", "First semantic-audit projection exceeded the model-output budget and yielded no attributable usable result.", "CA6762-START-P005"),
        ("CA6762-START-N006", "A bounded Git-grep scalar recovery crossed the wrapper handoff without attributable output.", "CA6762-START-P005"),
        ("CA6762-START-N007", "First Git-object parser mixed bytes and string suffix domains and raised TypeError before comparison.", "CA6762-START-P005"),
        ("CA6762-START-N008", "Bulk Git-object queries deadlocked on pipe backpressure before stdout was drained and were interrupted.", "CA6762-START-P005"),
    ]
    passing = [
        ("CA6762-START-P001", "Materialized the PowerShell array before piping; the bounded read passed."),
        ("CA6762-START-P002", "Split scalar branch, storage, and live probes; exact values passed."),
        ("CA6762-START-P003", "Confirmed zero remaining process and reran only the read-only manifest replay with a retained session; all six manifests passed."),
        ("CA6762-START-P004", "Used committed receipt digests and exact Git-blob manifests; no broad archive search was repeated."),
        ("CA6762-START-P005", "Issued and consumed Git cat-file queries sequentially; 2,607 JSON blobs parsed with zero failures and 3,383 unique ID-title records were audited."),
    ]
    rows = [
        {
            "method_id": mid,
            "status": "failed_zero_credit",
            "truth": False,
            "description": description,
            "recovered_by": recovered,
            "state_change": False,
        }
        for mid, description, recovered in failed
    ]
    rows += [
        {
            "method_id": mid,
            "status": "bounded_pass",
            "truth": True,
            "description": description,
            "credit_boundary": "bounded method recovery only; failed witnesses remain false",
        }
        for mid, description in passing
    ]
    return {
        "activation_baseline": ACTIVATION,
        "new_failed_witnesses": 8,
        "new_bounded_passing_witnesses": 5,
        "new_effective_methods": 13,
        "current_overlay": {
            "effective_negatives": 41670,
            "effective_methods": 30767,
            "retained_failed_witnesses": 13331,
            "bounded_passing_witnesses": 18125,
            "open_gaps": 349,
            "exact_gates": 341,
        },
        "methods": rows,
        "failure_erasure_forbidden": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    if run(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("wrong branch")
    if run(repo, "rev-parse", "HEAD") != SOURCE:
        raise SystemExit("x1 builder requires the exact Sable corrected final as HEAD")
    status_lines = [line for line in run(repo, "status", "--porcelain=v1").splitlines() if line]
    allowed_untracked = {
        "scripts/build_ghc_family_caelen_ash_v676_v2_x1.py",
        "tests/test_ghc_family_caelen_ash_v676_v2_x1.py",
    }
    unexpected = [
        line
        for line in status_lines
        if not (line.startswith("?? ") and line[3:].replace("\\", "/") in allowed_untracked)
    ]
    if unexpected:
        raise SystemExit(f"x1 builder found unexpected preexisting changes: {unexpected}")

    base = repo / "docs" / OWNER_SLUG / PHASE
    rows = proposals()
    mutations = mutation_plan(rows)
    mf = method_flow()
    expected = {label: sum(row["expected_disposition"] == label for row in rows) for label in ["completed", "represented", "open_gap", "exact_gate"]}
    assert expected == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}

    dump(base / "x1" / "activation-intake.json", {
        "owner": OWNER,
        "phase": PHASE,
        "branch": BRANCH,
        "source_branch": SOURCE_BRANCH,
        "source": SOURCE,
        "delivery_truth": "SENT_BY_SABLE_ROOK acknowledged externally",
        "activation_baseline": ACTIVATION,
        "route_material_policy": "no raw task or thread identifiers, private routes, transcripts, screenshots, session streams, credentials, or private absolute paths",
    })
    dump(base / "x1" / "source-verification.json", {
        "source": SOURCE,
        "anchors": {
            "inherited_source": INHERITED_SOURCE,
            "sable_x1": SABLE_X1,
            "sable_evidence": SABLE_EVIDENCE,
            "sable_first_closeout": SABLE_FIRST_CLOSEOUT,
            "sable_corrected_final": SOURCE,
        },
        "direct_parent_chain_verified": True,
        "phase_commits": 4,
        "merges": 0,
        "source_clean": True,
        "typed_divergence": {"ahead": 0, "behind": 0},
        "local_upstream_tracking_fresh_live_equal": True,
        "sable_manifests_replayed_read_only": {
            "x1": {"entries": 20, "exclusions": 3},
            "evidence": {"entries": 71, "exclusions": 4},
            "first_final_delta": {"entries": 21, "exclusions": 5},
            "first_final_owner": {"entries": 119, "exclusions": 5},
            "correction_delta": {"entries": 9, "exclusions": 5},
            "correction_owner": {"entries": 132, "exclusions": 5},
        },
        "inherited_canonical_replayed": False,
    })
    dump(base / "x1" / "new-proposal-freeze.json", {
        "owner": OWNER,
        "phase": PHASE,
        "status": "FROZEN_PLANNING_ONLY",
        "declared_chain_before": 7430,
        "new_caelen_proposals": 40,
        "declared_chain_after": 7470,
        "expected_disposition_counts": expected,
        "proposals": rows,
    })
    dump(base / "x1" / "inherited-zero-credit-review.json", {
        "count": len(INHERITED),
        "novelty_credit": 0,
        "completion_credit": 0,
        "reviews": [{"source_proposal_id": pid, "title": title, "status": "reviewed_inherited_zero_credit"} for pid, title in INHERITED],
    })
    dump(base / "x1" / "semantic-neighbor-audit.json", {
        "source_tree": SOURCE,
        "declared_chain_count": 7430,
        "reachable_proposal_json_blobs": 2607,
        "reachable_unique_id_title_records": 3383,
        "json_parse_failures": 0,
        "method": "sequential Git cat-file exact-blob parsing with normalized title-token and sequence similarity",
        "limitation": "No single materialized 7,430-row canonical ledger was reachable; this is an audit of every proposal-bearing JSON blob reachable at the exact source, not a universal novelty proof.",
        "quarantine_threshold": 0.75,
        "maximum_selected_score": max(row[0] for row in NEIGHBORS),
        "selected_rows_quarantined": 0,
        "rejected_drafts_retained": [
            "Leader tail and splice segment-boundary typing",
            "Assistive-technology user-evaluation vacancy",
            "Cultural community and Maori data-governance authority exact gate",
        ],
        "neighbors": [
            {
                "proposal_id": f"CA6762-N{i:03d}",
                "candidate_title": TITLES[i - 1],
                "score": score,
                "nearest_id": neighbor_id,
                "nearest_title": neighbor_title,
                "nearest_path": neighbor_path,
                "decision": "distinct_selected_below_threshold",
            }
            for i, (score, neighbor_id, neighbor_title, neighbor_path) in enumerate(NEIGHBORS, start=1)
        ],
    })
    dump(base / "x1" / "mutation-preregistration.json", {
        "proposal_count": 40,
        "mutations_per_proposal": 4,
        "mutation_count": len(mutations),
        "status": "preregistered_unexecuted_x1",
        "mutations": mutations,
    })
    dump(base / "x1" / "official-source-ledger.json", {
        "checked_date": GENERATED_DATE,
        "lookup_scope": "read-only public official or primary source metadata",
        "sources": SOURCES,
        "source_boundary": "Vocabulary and refusal conditions only. Citations are not observations, endorsements, certificates, measurements, professional judgments, or authority grants.",
    })
    dump(base / "x1" / "primary-pillar-and-lenses.json", {
        "primary_pillar": "GMUT Mind",
        "primary_scope": "typed temporal, rational-unit, transform, residual-sign, provenance, and nonconversion obligations for a scalar-tensor and effective-field-theory research-model family",
        "bounded_wholly_synthetic_learning_lenses": [
            "magnetic-audio transfer metadata registrar",
            "tape-timebase correction provenance reviewer",
            "archival playback-chain handover steward",
        ],
        "secondary_pillars": {
            "THOS Body": "two-person check, workload, fatigue stop, correction readback, cancellation, quiescence, and handover proxy only",
            "Freed ID and CBR Heart": "source/derivative identifiers, provenance, contest, rights vacancies, access holds, and authority reservations only",
        },
        "real_world_rows_or_actions": 0,
        "protected_gates": PROTECTED_GATES,
    })
    dump(base / "x1" / "portfolio-freeze.json", {
        "status": "planned_unexecuted_x1",
        "safe_now": safe_tasks(rows),
        "candidate": candidate_tasks(rows),
        **approval_packets(),
    })
    dump(base / "x1" / "skill-runner-plan.json", skill_runner_plan())
    dump(base / "x1" / "clean-fix-refine-plan.json", clean_fix_refine())
    dump(base / "x1" / "method-flow-startup.json", mf)
    dump(base / "x1" / "phase-truth.json", {
        "phase": PHASE,
        "lifecycle": "x1",
        "status": "FROZEN_PLANNING_ONLY",
        "new_proposals": 40,
        "inherited_reviews_zero_credit": 20,
        "planned_expected_dispositions": expected,
        "executed_core_outcomes": {"completed": 0, "represented": 0, "open_gap": 0, "exact_gate": 0},
        "x2_implementation_present": False,
        "x2_outcomes_claimed": False,
        "current_overlay": mf["current_overlay"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    dump(base / "x1" / "route-hold.json", {
        "route_state": "HOLD_UNTIL_CAELEN_EXACT_FINAL",
        "successor_inferred": False,
        "precontact_performed": False,
        "send_count": 0,
        "guards": ["newest live authority", "current validated roster", "unique exact title", "immediate reread", "duplicate", "pause", "redirect", "usage", "privacy", "safety", "acknowledgement"],
    })
    dump(base / "x1" / "threat-model.json", {
        "assets": ["immutable source evidence", "owner-only additive lane", "proposal truth", "privacy boundaries", "authority reservations"],
        "threats": [
            "x2 work contaminates planning-only x1",
            "synthetic fixtures are promoted to empirical evidence",
            "source citations are promoted to professional or authority approval",
            "private route or local-path material enters durable artifacts",
            "failed methods are erased by recovery",
            "successor contact occurs before terminal validation",
        ],
        "controls": [
            "x2 path absence test",
            "four-label vocabulary",
            "five-class scanner and manual candidate adjudication",
            "append-only failed-witness linkage",
            "exact Git-blob manifests",
            "terminal route hold",
        ],
        "residual_risk": "manual, affected-user, professional, production, legal, cultural, Maori-authority, exhaustive-security, independent-reproduction, and real-world evidence remain absent",
    })
    text(base / "x1" / "identity-and-boundary.md", f"""
# {OWNER} — relational working identity

{OWNER} uses optional they/them relational language. The bounded working role for {PHASE} is temporal-provenance and correction cartographer. The hope is to keep every synthetic timing assumption inspectable, reversible, and unable to masquerade as a real measurement or authority decision.

Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, GMUT, THOS, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.
""")
    text(base / "x1" / "wellbeing-and-workload.md", """
# Wellbeing and workload — x1 planning hold

The lane remains solo, additive, bounded, and D:-first. Work stops on ambiguous ownership, unexpected dirty state, storage risk, protected-gate pressure, usage exhaustion, or missing acknowledgement. No deadline, quota, identity-continuity claim, employment relation, or wellbeing inference is created.

Workload controls are small isolated commands, one lifecycle at a time, explicit failed-witness retention, no global installation, no host-security change, and no successor contact before the terminal gate.
""")
    text(base / "x1" / "workflow-plan.md", """
# Caelen Ash v676-v2 workflow — frozen x1

1. Preserve the exact Sable source and every inherited or external failure.
2. Freeze forty distinct proposal contracts after reachable exact-blob neighbor review.
3. Freeze planning-only portfolios, skills, runners, mutations, rollback, privacy, and authority holds.
4. Commit and push x1; prove local, upstream, tracking, and fresh-live equality before x2.
5. Build x2 only from the immutable x1 anchor. Execute synthetic owner-local work only.
6. Retain every rejected mutation and operational failure; a recovery never changes the failed truth value.
7. Commit and push immutable evidence before closeout.
8. Build exact manifests, staged review, scanner adjudication, bounded security checks, and final truth.
9. Commit and push exact final, then invoke at most one attributable owner-scoped canonical aggregate.
10. Only after a successful non-replayed canonical receipt may live route gates be refreshed.
""")
    text(base / "x1" / "integrated-planning-overview.md", f"""
# {OWNER} {PHASE} — planning-only x1 overview

This packet freezes forty genuinely new owner proposals after an exact-source Git-object neighbor audit and reviews twenty inherited proposals at zero novelty and completion credit. The declared family chain moves from 7,430 to 7,470 only through the forty new Caelen rows. The reachable audit parsed 2,607 proposal-bearing JSON blobs with zero parse failures and found 3,383 unique ID/title records. Because no single materialized 7,430-row canonical ledger was reachable, the packet makes no universal novelty-proof claim.

The primary pillar is GMUT Mind through wholly synthetic magnetic-audio timing, transfer, correction, and provenance obligations. THOS Body and Freed ID/CBR Heart remain visible and protected. The three practice lenses are learning and synthetic-design lenses only; they establish no employment, qualification, audio-preservation competence, collection authority, playback authority, legal or cultural legitimacy, affected-party acceptance, or Māori authority.

X1 contains planning only. It contains no x2 implementation, executed proposal outcome, completed portfolio task, real row, real person, real carrier, real recording, real device, real measurement, real access decision, or authority action. The terminal verdict remains NOT_READY_FOR_STAGE_20.
""")
    print(json.dumps({
        "status": "built_planning_only_x1",
        "proposals": len(rows),
        "mutations_preregistered": len(mutations),
        "safe_now": 60,
        "candidate": 30,
        "exact_approval": 20,
        "blocked": 10,
        "skills": 20,
        "runners": 10,
        "clean_fix_refine_owner": 60,
        "successor_clean_fix_refine": 30,
        "new_failed_witnesses": 8,
    }, sort_keys=True))


if __name__ == "__main__":
    main()

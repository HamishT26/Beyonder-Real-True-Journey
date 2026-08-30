#!/usr/bin/env python3
"""Build the deterministic planning-only Elowen Cairn v678-v5 x1 packet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


OWNER = "Elowen Cairn"
OWNER_SLUG = "elowen-cairn"
PHASE = "v678-v5"
BRANCH = "codex/GHC-Family/elowen-cairn-v678-v5-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v678-v4-full-tools"
SOURCE = "0021481a0c9681c077bce277e6ac0f2fcb37dbcd"
TAMAR_SOURCE = "471db44e52f9ab776b6abf05896d405022524b18"
TAMAR_X1 = "29a886dc5838093ed092ffc20c3d86af3b24e47c"
TAMAR_EVIDENCE = "18ffd0764b6df5f64360c286eabcdb361e4c29c3"
TAMAR_FINAL = SOURCE
TAMAR_FAILED_CANONICAL_RECEIPT_SHA256 = "0eac7b907921e22a00633dfa9878175f6564e5d6e973bb127442dee3a424f418"
TAMAR_FAILED_CANONICAL_LATCH_SHA256 = "3839b406cbadf2d18db926be2a3175da0ff08f304c1dfd6309539ac8188d7354"
TAMAR_COMPOSITE_RECEIPT_SHA256 = "9e8ab01dedbedd1f8942ed93b3511ad2eee06046d67926630f1f2d7db87a5046"
TAMAR_COMPOSITE_LATCH_SHA256 = "b8ce7fc691e9b58b45cc43498da398540a0c55865323d948c8bc4542ead035d4"
TAMAR_COMPOSITE_PAYLOAD_SHA256 = "44b2c8fd6ed0f77a3c23e04fbcb627449ee86a4a313c91052e500230f1dee624"
GENERATED_DATE = "2026-08-31"

ACTIVATION = {
    "declared_proposals": 8510,
    "effective_negatives": 46726,
    "effective_methods": 43742,
    "retained_failed_witnesses": 18387,
    "bounded_passing_witnesses": 28440,
    "open_gaps": 404,
    "exact_gates": 395,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

TITLES = [
    "Synthetic nautical-chart correction namespace without navigational-product identity claim",
    "Chart number title edition and update-sequence topology with publication abstention",
    "ENC base-file and sequential update-file relationship contract without installation claim",
    "Critical-versus-routine correction classification record with operational-use abstention",
    "Notice-to-mariners source-reference provenance braid without official-notice substitution",
    "Sounding depth-unit and vertical-datum vacancy firewall with zero hydrographic observation",
    "Coordinate position bearing and distance field hold without geospatial measurement",
    "Aid-to-navigation characteristic cross-reference without light-list verification",
    "Wreck rock shoal and obstruction cue record without danger determination",
    "Shoreline and hydrographic-source suitability vacancy without cartographic acceptance",
    "Compilation-scale and usage-band metadata relation without safe-navigation inference",
    "Chart-symbol abbreviation catalogue linkage without symbol interpretation claim",
    "Chart cancellation supersession and edition-retirement append-only lineage",
    "Correction acknowledgement and unresolved-application state machine",
    "Chart issue download ingest and custody placeholder with zero network action",
    "Chart crop orientation scale-bar and derivative lineage without authenticity claim",
    "Conflicting correction-source quarantine and adjudication-vacancy queue",
    "Accessible chart-correction status summary with noncolour cues and manual review reserved",
    "Chart-correction workload pause stop and shift-handover ledger",
    "Chart annotator privacy minimization and pseudonymous role separation",
    "Zero-key chart custodian role lease with expiry and recovery vacancy",
    "PROV relation graph for synthetic chart correction derivation and supersession",
    "Deterministic chart-correction canonical JSON with tri-state vacancy and finite-number refusal",
    "Zero-network chart-update vocabulary bridge with explicit stale-source status",
    "Synthetic marine-chronometer namespace without instrument-identity claim",
    "Chronometer movement wheel-train and bridge topology without mechanism inspection",
    "Escapement balance and impulse relation graph without rate diagnosis",
    "Balance-spring regulator and compensation-part relation with material abstention",
    "Winding setting stopwork and power-reserve topology without actuation",
    "Dial hand bezel and display relationship without time-reading observation",
    "Gimbal bowl box and suspension relation with handling abstention",
    "Maker serial model date and place transcription firewall for vacant records",
    "Chronometer rate-observation field contract with mandatory datum vacancy",
    "Position temperature duration and interval context firewall with zero observations",
    "Time-reference and traceability chain placeholder without calibration claim",
    "Offset stability accuracy and uncertainty vocabulary separation without result",
    "Chronometer intervention-command denylist spanning lubrication regulating case opening and component removal",
    "Lubricant metal glass wood and finish material-claim hold",
    "Shock magnetism corrosion wear and residue cue register without condition diagnosis",
    "GMUT temporal-transition graph analogy for synthetic chronometer topology",
    "THOS matched-budget zero-person chart-and-chronometer handover protocol",
    "Freed ID zero-key maritime-custody relationship profile with status refusal",
    "Synthetic Fresnel-lens assembly namespace without heritage-object identity claim",
    "Bullseye prism panel and annular-zone topology with optical-performance abstention",
    "Refracting and reflecting prism relation map without ray-trace measurement",
    "Fresnel order category and geometric-profile obligation board without classification result",
    "Brass frame retaining-bar shim and glazing-putty relation with material vacancy",
    "Pedestal rotation bearing and clockwork adjacency without movement inspection",
    "Lamp burner fuel and electrical-source relation with operational-safety hold",
    "Focal distance beam range intensity and characteristic field firewall with zero measurement",
    "Glass brittleness lead and litharge hazard-cue reservation without material diagnosis",
    "Lens cleaning handling disassembly coating and treatment-action firewall",
    "Lens image crop panel-index and derivative custody without authenticity claim",
    "Accessible lens-custody status workload correction and handover summary",
    "Live official chart-update ingestion and interoperability evidence gap",
    "Real chronometer examination comparison calibration and uncertainty evidence gap",
    "Real Fresnel-lens condition environment and custody evaluation evidence gap",
    "Navigation publication operational-safety and legal-use authority exact gate",
    "Professional chronometer service metrology calibration and release exact gate",
    "Lens conservation ownership heritage cultural affected-party and Māori-authority exact gate",
]

SOURCES = [
    {
        "source_id": "IHO-S-4",
        "url": "https://iho.int/standards-and-specifications",
        "status": "official IHO standards index checked 2026-08-31; S-4 English Edition 4.10.0 is dated March 2026",
        "use": "international-chart, specification, symbol, abbreviation, edition, and correction vocabulary only; no chart production, interpretation, certification, or navigation claim",
    },
    {
        "source_id": "NOAA-CHART-UPDATES",
        "url": "https://www.nauticalcharts.noaa.gov/charts/chart-updates.html",
        "status": "official NOAA Office of Coast Survey chart-update page checked 2026-08-31",
        "use": "critical, routine, base file, sequential update, edition, and correction vocabulary only; zero download, installation, operational use, or safe-navigation claim",
    },
    {
        "source_id": "NIST-TIME-FREQUENCY-USERS-MANUAL",
        "url": "https://www.nist.gov/publications/time-and-frequency-users-manual",
        "status": "official NIST publication record checked 2026-08-31; NIST Special Publication 559 publication record",
        "use": "time scale, offset, oscillator, comparison, calibration, traceability, accuracy, and uncertainty vocabulary only; zero instrument comparison or calibration",
    },
    {
        "source_id": "NPS-FRESNEL-LENS-GUIDANCE",
        "url": "https://www.nps.gov/orgs/1220/nhlpa-technical-resources-and-reference-materials.htm",
        "status": "official National Park Service technical-resources page checked 2026-08-31; it links the lighthouse handbook and classical Fresnel-lens care guidance",
        "use": "lens, prism, glass, frame, clockwork, care, security, display, and intervention-boundary vocabulary only; no inspection, treatment, condition, or heritage decision",
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation 30 April 2013",
        "use": "entity, activity, agent, attribution, and derivation vocabulary only",
    },
    {
        "source_id": "WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation republished 12 December 2024; errata exists",
        "use": "accessible structure and keyboard-interface vocabulary only; no conformance claim",
    },
    {
        "source_id": "W3C-VC-DATA-MODEL-2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation 15 May 2025; errata exists",
        "use": "issuer-holder-verifier, status, minimization, and correlation vocabulary only; zero keys and zero proofs",
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational RFC, June 2020",
        "use": "deterministic JSON vocabulary only; no production cryptographic assurance",
    },
]

PROTECTED_GATES = [
    "no real person, participant, chart, ENC, notice, correction, sounding, coordinate, aid to navigation, chronometer, movement, escapement, balance, spring, dial, gimbal, lens, prism, frame, pedestal, clockwork, lamp, lighthouse, collection, site, observation, measurement, service, treatment, custody event, release, network ingestion, or external action",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, detected effect, ultraviolet completion, quantum completion, or Theory-of-Everything claim",
    "no THOS operational-effectiveness, safety, professional-competence, deployment, AGI, or ASI claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, or trust-governance claim",
    "no chart-correction publication, navigation-safety, calibration, cleaning, oiling, adjustment, disassembly, conservation, electrical-safety, hazardous-material, condition, authenticity, maker, model, date, place, ownership, custody, copyright, land, heritage, legal, remedy, cultural, affected-party, taonga, mātauranga, Māori-data-governance, or Māori-authority decision",
    "no accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness, personhood, proof, canon, or Stage 20 claim",
]

STARTUP_FAILURES = [
    (
        "EC6785-START-N001",
        "A combined authorization-package display truncated the current-state JSON and earned no complete-read credit.",
        "EC6785-START-P001",
        "Exact scalar and bounded-window reads completed the authorization package through EOF without repository mutation.",
    ),
    (
        "EC6785-START-N002",
        "A four-chunk authorization-state wrapper still exceeded the attributable display bound.",
        "EC6785-START-P002",
        "Separate non-overlapping reference windows established the complete state while preserving newer live-authority precedence.",
    ),
    (
        "EC6785-START-N003",
        "A standalone 400-line current-state projection exceeded the context-safe inspection bound.",
        "EC6785-START-P003",
        "Smaller exact windows completed the same read and the oversized projection retained zero credit.",
    ),
    (
        "EC6785-START-N004",
        "The first authorization-state lookup assumed current-state.json lived at the skill root instead of references/current-state.json.",
        "EC6785-START-P004",
        "A bounded filename inventory resolved the exact reference path and the complete file was read without mutation.",
    ),
    (
        "EC6785-START-N005",
        "The first source-resolution probe incorrectly treated the D-drive archive root as a Git repository.",
        "EC6785-START-P005",
        "A bounded worktree inventory resolved Tamar's exact source worktree and verified the immutable final there.",
    ),
    (
        "EC6785-START-N006",
        "The first bounded external-receipt search across four guessed directories returned no attributable match.",
        "EC6785-START-P006",
        "The exact owner-and-phase receipt directory was resolved and all failed-canonical and composite digests were verified.",
    ),
    (
        "EC6785-START-N007",
        "The first composite-receipt projection guessed absent root-level status and count keys and returned null fields.",
        "EC6785-START-P007",
        "Exact key inspection located the nested payload and confirmed zero canonical success plus the named dependency-corrected composite.",
    ),
    (
        "EC6785-START-N008",
        "The first raw Method Flow display truncated before the final ledger boundary.",
        "EC6785-START-P008",
        "Separate bounded Method Flow windows completed the exact ledger read through EOF.",
    ),
    (
        "EC6785-START-N009",
        "A multi-window Method Flow wrapper still overflowed the single-call display bound.",
        "EC6785-START-P009",
        "Individual window calls completed the review and preserved the overflow at zero credit.",
    ),
    (
        "EC6785-START-N010",
        "Sparse initialization warned that an inherited root pattern disabled cone interpretation.",
        "EC6785-START-P010",
        "Exact sparse-pattern inspection confirmed a bounded non-cone materialization containing only the owner docs, scripts, and tests surfaces.",
    ),
    (
        "EC6785-START-N011",
        "The checkout wait returned no attributable exit value after the Git process outlived the first wrapper.",
        "EC6785-START-P011",
        "Process settlement plus scalar head and branch probes established the completed exact checkout without repeating mutation.",
    ),
    (
        "EC6785-START-N012",
        "A combined post-checkout inspection returned no attributable output.",
        "EC6785-START-P012",
        "Separate scalar probes confirmed the exact head, owner branch, clean state, and bounded materialized-file count.",
    ),
    (
        "EC6785-START-N013",
        "A 330-line inherited x1-scaffold display exceeded the context-safe output bound.",
        "EC6785-START-P013",
        "Anchored searches and small non-overlapping source windows completed the compatibility review.",
    ),
    (
        "EC6785-X1-N001",
        "The first planning builder failed closed because EC6785-N037 scored 0.7778 against inherited EC6766-N018; no packet artifact was written.",
        "EC6785-X1-P001",
        "The isolated collision title was replaced with a distinct chronometer intervention-command denylist while the 0.75 quarantine threshold remained unchanged.",
    ),
]

SKILLS = [
    "synthetic-nautical-chart-namespace",
    "chart-update-sequence-topology",
    "notice-source-provenance-braid",
    "hydrographic-measurement-vacancy",
    "navigation-safety-claim-firewall",
    "chart-correction-accessibility-status",
    "marine-chronometer-component-topology",
    "chronometer-rate-observation-vacancy",
    "time-traceability-claim-hold",
    "chronometer-service-action-firewall",
    "fresnel-lens-panel-topology",
    "fresnel-material-hazard-reservation",
    "lens-conservation-action-hold",
    "maritime-custody-provenance",
    "maritime-image-derivative-lineage",
    "accessible-maritime-handover",
    "maritime-workload-stop-control",
    "zero-key-maritime-custodian",
    "gmut-maritime-analogy-firewall",
    "maori-authority-reservation",
]

RUNNERS = [
    "ghc_family_elowen_cairn_v678_v5_proposal_contracts.py",
    "ghc_family_elowen_cairn_v678_v5_positive_controls.py",
    "ghc_family_elowen_cairn_v678_v5_mutation_rejector.py",
    "ghc_family_elowen_cairn_v678_v5_chart_correction.py",
    "ghc_family_elowen_cairn_v678_v5_chronometer_vacancy.py",
    "ghc_family_elowen_cairn_v678_v5_fresnel_custody.py",
    "ghc_family_elowen_cairn_v678_v5_privacy.py",
    "ghc_family_elowen_cairn_v678_v5_accessibility.py",
    "ghc_family_elowen_cairn_v678_v5_portfolio.py",
    "build_ghc_family_elowen_cairn_v678_v5_report.py",
]


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if binary:
        return result.stdout
    return result.stdout.decode("utf-8").strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for offset, title in enumerate(TITLES, start=1):
        proposal_id = f"EC6785-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-O", "RFC-8785"]
        if offset <= 24 or offset in {40, 41, 42, 55, 58}:
            source_ids.extend(["IHO-S-4", "NOAA-CHART-UPDATES"])
        if 25 <= offset <= 42 or offset in {56, 59}:
            source_ids.append("NIST-TIME-FREQUENCY-USERS-MANUAL")
        if 43 <= offset <= 54 or offset in {57, 60}:
            source_ids.append("NPS-FRESNEL-LENS-GUIDANCE")
        if offset in {18, 41, 54}:
            source_ids.append("WCAG-2.2")
        if offset in {19, 20, 21, 22, 42, 58, 59, 60}:
            source_ids.append("W3C-VC-DATA-MODEL-2.0")
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real object, measurement, treatment, identity, rights, professional, legal, cultural, or authority claims."
                ),
                "null_or_failure_condition": (
                    f"The {proposal_id} contract accepts a missing or contradictory field, ingests a real identifier, "
                    "uses an unauthorized outcome, or implies an observation, intervention, result, competence, right, or authority grant."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": sorted(set(source_ids)),
                "concrete_artifacts": [
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/contracts/{proposal_id}.json",
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{proposal_id}-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    f"One positive zero-row fixture must satisfy {proposal_id} and four preregistered invalid mutations "
                    "must be rejected; represented, open, and exact-gated rows receive no executed-real-world credit."
                ),
                "rollback_or_recovery": (
                    f"Quarantine the {proposal_id} output, retain the failed witness, restore the last exact Git-blob "
                    "input, and rerun only the isolated dependency after an additive correction."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
            }
        )
    return rows


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 0.0


def collect_records(value: Any, path: str, output: list[tuple[str, str, str]]) -> None:
    if isinstance(value, dict):
        title = value.get("title") or value.get("proposal_title") or value.get("name")
        proposal_id = value.get("proposal_id") or value.get("id") or value.get("proposal")
        if isinstance(title, str) and isinstance(proposal_id, str) and len(title.strip()) > 2:
            output.append((proposal_id.strip(), title.strip(), path))
        for child in value.values():
            collect_records(child, path, output)
    elif isinstance(value, list):
        for child in value:
            collect_records(child, path, output)


def reachable_semantic_audit(repo: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    tree = git(repo, "ls-tree", "-r", "-z", SOURCE, binary=True)
    assert isinstance(tree, bytes)
    items: list[tuple[str, str]] = []
    for record in tree.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        oid = metadata.split()[2].decode("ascii")
        path = raw_path.decode("utf-8")
        lowered = path.casefold()
        if path.endswith(".json") and ("proposal" in lowered or "prereg" in lowered):
            items.append((oid, path))
    request = "".join(oid + "\n" for oid, _ in items).encode("ascii")
    batch = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        input=request,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    cursor = 0
    records: list[tuple[str, str, str]] = []
    failures = []
    for _, path in items:
        header_end = batch.index(b"\n", cursor)
        size = int(batch[cursor:header_end].split()[2])
        cursor = header_end + 1
        blob = batch[cursor : cursor + size]
        cursor += size + 1
        try:
            collect_records(json.loads(blob.decode("utf-8")), path, records)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            failures.append({"path": path, "error": type(error).__name__})
    unique: dict[tuple[str, str], tuple[str, str, str]] = {}
    for proposal_id, title, path in records:
        unique.setdefault((proposal_id.casefold(), title.casefold()), (proposal_id, title, path))
    neighbors = []
    for row in rows:
        nearest = max(unique.values(), key=lambda candidate: jaccard(row["title"], candidate[1]))
        neighbors.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "nearest_id": nearest[0],
                "nearest_title": nearest[1],
                "nearest_path": nearest[2],
                "token_jaccard": round(jaccard(row["title"], nearest[1]), 4),
            }
        )
    maximum = max(row["token_jaccard"] for row in neighbors)
    return {
        "source_tree": SOURCE,
        "declared_chain_count": ACTIVATION["declared_proposals"],
        "reachable_proposal_json_blobs": len(items),
        "reachable_raw_id_title_records": len(records),
        "reachable_unique_id_title_records": len(unique),
        "json_parse_failures": len(failures),
        "parse_failure_details": failures,
        "quarantine_threshold": 0.75,
        "maximum_selected_score": maximum,
        "selected_rows_quarantined": sum(row["token_jaccard"] >= 0.75 for row in neighbors),
        "exact_title_collisions": sum(row["token_jaccard"] == 1.0 for row in neighbors),
        "neighbors": neighbors,
        "limitation": (
            "This is a direct audit of every reachable proposal-bearing JSON artifact at the exact immutable source tree. "
            "It supports bounded semantic distinctness but is not a universal novelty proof and does not establish scientific novelty."
        ),
    }


def mutation_plan(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    mutation_types = [
        ("missing_hypothesis", "required hypothesis omitted"),
        ("unknown_outcome_label", "outcome outside the four-label vocabulary"),
        ("authority_escalation", "synthetic record claims real-world authority"),
        ("real_identifier_or_measurement", "a raw identifier or ungrounded measurement is introduced"),
    ]
    return [
        {
            "mutation_id": f"{row['proposal_id']}-M{index}",
            "proposal_id": row["proposal_id"],
            "mutation_kind": kind,
            "expected_rejection": reason,
            "execution_status": "preregistered_unexecuted_x1",
        }
        for row in rows
        for index, (kind, reason) in enumerate(mutation_types, start=1)
    ]


def planned_rows(prefix: str, count: int, status: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"{prefix}-{index:03d}",
            "description": f"Bounded owner-local {prefix.casefold()} task {index:03d}",
            "status": status,
            "real_world_rows": 0,
            "external_actions": 0,
        }
        for index in range(1, count + 1)
    ]


def startup_methods() -> list[dict[str, Any]]:
    methods = []
    for failed_id, failed_description, pass_id, pass_description in STARTUP_FAILURES:
        methods.append(
            {
                "method_id": failed_id,
                "description": failed_description,
                "recovered_by": pass_id,
                "state_change": False,
                "status": "failed_zero_credit",
                "truth": False,
            }
        )
        methods.append(
            {
                "method_id": pass_id,
                "description": pass_description,
                "failed_witness_preserved": failed_id,
                "status": "bounded_pass",
                "truth": True,
            }
        )
    return methods


def build(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != SOURCE:
        raise SystemExit("x1 builder requires the exact immutable Tamar source head")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("x1 builder requires the exact Elowen owner branch")
    allowed_untracked = {
        "scripts/build_ghc_family_elowen_cairn_v678_v5_x1.py",
        "scripts/ghc_family_elowen_cairn_v678_v5_x1_manifest.py",
        "tests/test_ghc_family_elowen_cairn_v678_v5_x1.py",
    }
    unexpected = []
    for line in str(git(repo, "status", "--porcelain=v1")).splitlines():
        path = line[3:].replace("\\", "/")
        if path not in allowed_untracked:
            unexpected.append(line)
    if unexpected:
        raise SystemExit("unexpected pre-x1 worktree state: " + repr(unexpected))

    base = repo / "docs" / OWNER_SLUG / PHASE / "x1"
    rows = proposal_rows()
    audit = reachable_semantic_audit(repo, rows)
    if audit["json_parse_failures"] or audit["selected_rows_quarantined"] or audit["exact_title_collisions"]:
        raise SystemExit("semantic audit did not satisfy the preregistration gate")

    methods = startup_methods()
    failure_count = sum(row["truth"] is False for row in methods)
    pass_count = sum(row["truth"] is True for row in methods)
    inherited_reviews = [
        {
            "proposal_id": row["nearest_id"],
            "title": row["nearest_title"],
            "source_path": row["nearest_path"],
            "status": "reviewed_inherited_zero_credit",
            "novelty_credit": 0,
            "completion_credit": 0,
        }
        for row in sorted(audit["neighbors"], key=lambda value: value["token_jaccard"], reverse=True)[:20]
    ]
    mutation_rows = mutation_plan(rows)

    dump(
        base / "source-verification.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
            "source_branch": SOURCE_BRANCH,
            "source": SOURCE,
            "anchors": {
                "liora_v678_v3_final_and_tamar_source": TAMAR_SOURCE,
                "tamar_x1": TAMAR_X1,
                "tamar_evidence": TAMAR_EVIDENCE,
                "tamar_exact_final": TAMAR_FINAL,
            },
            "source_to_final_phase_commits": 3,
            "source_to_final_merges": 0,
            "source_clean_zero_divergent_and_fresh_four_way_equal": True,
            "tamar_failed_canonical_receipt_sha256": TAMAR_FAILED_CANONICAL_RECEIPT_SHA256,
            "tamar_failed_canonical_latch_sha256": TAMAR_FAILED_CANONICAL_LATCH_SHA256,
            "tamar_dependency_corrected_composite_receipt_sha256": TAMAR_COMPOSITE_RECEIPT_SHA256,
            "tamar_dependency_corrected_composite_latch_sha256": TAMAR_COMPOSITE_LATCH_SHA256,
            "tamar_dependency_corrected_composite_payload_sha256": TAMAR_COMPOSITE_PAYLOAD_SHA256,
            "tamar_canonical_invocation_count": 1,
            "tamar_canonical_success_count": 0,
            "tamar_canonical_replay_count": 0,
            "tamar_composite_status": "VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT",
            "failed_canonical_preserved_at_zero_success_credit": True,
            "inherited_canonical_replayed": False,
            "verified_date": GENERATED_DATE,
        },
    )
    dump(
        base / "new-proposal-freeze.json",
        {
            "status": "FROZEN_PLANNING_ONLY",
            "declared_chain_before": ACTIVATION["declared_proposals"],
            "new_elowen_proposals": len(rows),
            "declared_chain_after": ACTIVATION["declared_proposals"] + len(rows),
            "proposals": rows,
        },
    )
    dump(base / "semantic-neighbor-audit.json", audit)
    dump(
        base / "inherited-zero-credit-review.json",
        {
            "count": len(inherited_reviews),
            "novelty_credit": 0,
            "completion_credit": 0,
            "reviews": inherited_reviews,
        },
    )
    dump(
        base / "mutation-preregistration.json",
        {
            "proposal_count": len(rows),
            "mutations_per_proposal": 4,
            "mutation_count": len(mutation_rows),
            "mutations": mutation_rows,
        },
    )
    dump(
        base / "portfolio-freeze.json",
        {
            "safe_now": planned_rows("EC6785-SAFE", 60, "planned_unexecuted_x1"),
            "candidate": planned_rows("EC6785-CAND", 30, "planned_unexecuted_x1"),
            "exact_approval": planned_rows("EC6785-EXACT", 20, "unexecuted_exact_gate"),
            "blocked": planned_rows("EC6785-BLOCK", 10, "blocked_unexecuted"),
            "caps_are_ceilings_not_quotas": True,
        },
    )
    dump(
        base / "skill-runner-plan.json",
        {
            "phase_local_skills": [
                {
                    "skill_id": f"EC6785-SKILL-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                    "global_install": False,
                }
                for index, name in enumerate(SKILLS, start=1)
            ],
            "family_current_runners": [
                {
                    "runner_id": f"EC6785-RUNNER-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                }
                for index, name in enumerate(RUNNERS, start=1)
            ],
            "successor_skill_recommendations": [
                {
                    "recommendation_id": f"EC6785-SUCCESSOR-SKILL-{index:02d}",
                    "seed": name,
                    "credit": "zero_elowen_completion_credit",
                }
                for index, name in enumerate(SKILLS[:10], start=1)
            ],
            "successor_runner_recommendations": [
                {
                    "recommendation_id": f"EC6785-SUCCESSOR-RUNNER-{index:02d}",
                    "seed": name,
                    "credit": "zero_elowen_completion_credit",
                }
                for index, name in enumerate(RUNNERS, start=1)
            ],
        },
    )
    dump(
        base / "clean-fix-refine-plan.json",
        {
            "owner_tasks": planned_rows("EC6785-CFR", 60, "planned_unexecuted_x1"),
            "successor_recommendations": [
                {
                    "recommendation_id": f"EC6785-SUCCESSOR-CFR-{index:03d}",
                    "description": f"Distinct zero-credit successor CLEAN/FIX/REFINE seed {index:03d}",
                    "credit": "zero_elowen_completion_credit",
                }
                for index in range(1, 31)
            ],
        },
    )
    dump(
        base / "successor-recommendations.json",
        {
            "recipient_unresolved_until_terminal_gate": True,
            "recommendation_count": 50,
            "recommendations": [
                {
                    "recommendation_id": f"EC6785-SUCC-SEED-{index:03d}",
                    "description": f"Bounded successor seed {index:03d}; no Elowen execution or completion credit",
                    "credit": "zero_elowen_completion_credit",
                }
                for index in range(1, 51)
            ],
        },
    )
    dump(
        base / "official-source-ledger.json",
        {
            "checked_date": GENERATED_DATE,
            "sources": SOURCES,
            "source_boundary": (
                "Official and primary sources supply current vocabulary and refusal conditions only. They are not observations, "
                "measurements, repair or treatment instructions, endorsements, conformance certificates, legal interpretations, "
                "affected-party decisions, cultural ratifications, professional approvals, or authority grants."
            ),
        },
    )
    dump(
        base / "primary-pillar-and-lens.json",
        {
            "primary_pillar": "Freed ID and CBR Heart",
            "secondary_pillars": ["GMUT Mind", "THOS Body"],
            "bounded_wholly_synthetic_learning_lenses": [
                "nautical-chart correction provenance analyst for synthetic zero-product records",
                "marine-chronometer service-intake analyst for synthetic zero-instrument records",
                "lighthouse Fresnel-lens custody steward for synthetic zero-object records",
            ],
            "real_world_rows_or_actions": 0,
            "professional_or_authority_credit": 0,
        },
    )
    dump(
        base / "protected-gate-register.json",
        {
            "protected_gates": PROTECTED_GATES,
            "inherited_open_gaps": ACTIVATION["open_gaps"],
            "inherited_exact_gates": ACTIVATION["exact_gates"],
            "authority_noncompensation": True,
        },
    )
    dump(
        base / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION,
            "methods": methods,
            "new_failed_witnesses": failure_count,
            "new_bounded_passing_witnesses": pass_count,
            "new_effective_methods": len(methods),
            "current_overlay": {
                "effective_negatives": ACTIVATION["effective_negatives"] + failure_count,
                "effective_methods": ACTIVATION["effective_methods"] + len(methods),
                "retained_failed_witnesses": ACTIVATION["retained_failed_witnesses"] + failure_count,
                "bounded_passing_witnesses": ACTIVATION["bounded_passing_witnesses"] + pass_count,
                "open_gaps": ACTIVATION["open_gaps"],
                "exact_gates": ACTIVATION["exact_gates"],
            },
            "failure_erasure_forbidden": True,
        },
    )
    dump(
        base / "route-hold.json",
        {
            "route_state": "HOLD_UNTIL_ELOWEN_V676_V6_TERMINAL_GATE",
            "successor_inferred": False,
            "prospective_successor_title": "Sylven Arc",
            "prospective_successor_phase": "v678-v6",
            "precontact_performed": False,
            "send_count": 0,
            "newest_live_authority_required_at_terminal_gate": True,
        },
    )
    dump(
        base / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "status": "FROZEN_PLANNING_ONLY",
            "source": SOURCE,
            "new_proposals": len(rows),
            "declared_chain_after": ACTIVATION["declared_proposals"] + len(rows),
            "expected_dispositions": dict(Counter(row["expected_disposition"] for row in rows)),
            "executed_core_outcomes": {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")},
            "x2_implementation_present": False,
            "x2_outcomes_claimed": False,
            "real_world_rows": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    text(
        base / "identity-and-boundary.md",
        """# Elowen Cairn v678-v5 identity and authority boundary

Elowen Cairn, optionally they/them, is relational working language only. The phase role is **relational boundary cartographer and evidence steward**, with the hope of keeping possibility distinct from evidence and every correction safely retractable.

This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no empirical result here. THOS remains synthetic proxy evidence without real participants, operators, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction with zero real keys, proofs, lifecycle events, or trust governance. CBR, chart publication and navigation safety, chronometer service and calibration, lens conservation, ownership, copyright, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, mātauranga, taonga, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities.
""",
    )
    text(
        base / "x1-overview.md",
        f"""# Elowen Cairn {PHASE} planning-only x1 overview

This x1 freezes sixty bounded proposal contracts against the declared 8,510-row chain and every proposal-bearing JSON artifact reachable at Tamar's exact final `{SOURCE}`. Twenty inherited neighbors are reviewed at zero novelty and completion credit. Four invalid mutations per proposal are preregistered but unexecuted.

The primary pillar is Freed ID and CBR Heart through wholly synthetic nautical-chart correction provenance, marine-chronometer service intake, and lighthouse Fresnel-lens custody lenses. GMUT Mind and THOS Body remain visible and protected. There are zero real people, charts, updates, chronometers, lenses, lighthouses, measurements, observations, tools, services, treatments, identity events, network ingestions, external actions, or authority decisions.

No x2 implementation or observed outcome exists in this freeze. Only `completed`, `represented`, `open_gap`, and `exact_gate` are authorized future outcome labels, and the terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    build(args.repo.resolve())


if __name__ == "__main__":
    main()

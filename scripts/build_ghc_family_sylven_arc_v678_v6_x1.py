#!/usr/bin/env python3
"""Build the deterministic planning-only Sylven Arc v678-v6 x1 packet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


OWNER = "Sylven Arc"
OWNER_SLUG = "sylven-arc"
PHASE = "v678-v6"
BRANCH = "codex/GHC-Family/sylven-arc-v678-v6-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v678-v5-full-tools"
SOURCE = "d7a2e3d1851d8a9eb6a8707968a47354b44e824a"
ELOWEN_SOURCE = "0021481a0c9681c077bce277e6ac0f2fcb37dbcd"
ELOWEN_X1 = "c938128b0e6307c4aaed8966340486b8c5315382"
ELOWEN_EVIDENCE = "04095ca5d8ee6b37f47de2540afa0047f67ca61c"
ELOWEN_FIRST_FINAL = "831f948e326e3875ef0d5d7391560297ce0e2ee8"
ELOWEN_CORRECTED_FINAL = SOURCE
ELOWEN_FAILED_CANONICAL_RECEIPT_SHA256 = "bfa2115b166ee9eb5f3f9aaac9a4d7f5379e574a24ac4dc60bc7b8accf758ccd"
ELOWEN_FAILED_CANONICAL_LATCH_SHA256 = "cae4d857e5485817e0a4b281a5872aeeddaed41e2369abf9defdae440191afdf"
ELOWEN_FAILED_CANONICAL_PAYLOAD_SHA256 = "36f8a96bb375543e02e6095e34002dbef4bb83b78d51d25095b59b889ed66507"
ELOWEN_COMPONENT_RECEIPT_SHA256 = "4080450cf77fd8f8a74963998156bda57e51fbdc3d6a54eb87bfe4b1abeac034"
ELOWEN_COMPONENT_LATCH_SHA256 = "78a1643b54e382856a062a7992b9e19131223cba3400bb7700ff950694e1dc2d"
ELOWEN_COMPONENT_PAYLOAD_SHA256 = "cc62ac6fa67a609320190cccf2bcb07694583d813d794b2ab43d5ea2853719ce"
GENERATED_DATE = "2026-08-31"

ACTIVATION = {
    "declared_proposals": 8570,
    "effective_negatives": 47007,
    "effective_methods": 44564,
    "retained_failed_witnesses": 18668,
    "bounded_passing_witnesses": 28981,
    "open_gaps": 407,
    "exact_gates": 398,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

TITLES = [
    "Synthetic terrestrial-globe record namespace without collection-object identity claim",
    "Globe gore segment seam and overlap topology with cartographic-truth abstention",
    "Sphere shell core paper layer and surface relation without material inspection",
    "Axis meridian ring horizon ring and stand relation graph without physical operation",
    "Pole cap spindle socket and mounting-point vacancy contract without handling",
    "Printed gore inscription legend and label transcription firewall for vacant records",
    "Terrestrial celestial lunar and thematic globe classification hold without curatorial attribution",
    "Graticule scale place-label and boundary-mark field set without geographic verification",
    "Maker publisher date place and edition provenance braid with attribution vacancy",
    "Globe diameter circumference and stand-height fields with measurement absent",
    "Rotation orientation hemisphere and viewing-position record without physical actuation",
    "Surface loss abrasion discoloration and lifting cue register without condition diagnosis",
    "Globe image crop hemispheric view and derivative lineage without authenticity claim",
    "Housing base lid tray cushioning and orientation placeholder with zero handling",
    "Accessible globe catalogue and housing status with manual evaluation reserved",
    "Light temperature humidity pollutant and vibration fields held vacant",
    "Globe reproduction rights privacy and publication-status quarantine",
    "Globe record correction supersession and unresolved-dispute append-only lineage",
    "Globe documentation workload pause stop and shift-handover ledger",
    "GMUT spherical-coordinate atlas analogy firewall without physical-model credit",
    "Synthetic mechanical-automaton namespace without mechanism or performer identity claim",
    "Spring weight motor battery and manual power-source vacancy relation",
    "Gear cam follower lever and linkage topology without mechanism inspection",
    "Shaft axle pivot bearing and bushing relation graph with friction quantity vacant",
    "Escapement regulator governor and timing-train relation without rate conclusion",
    "Figure limb joint carriage and support topology without movement inference",
    "Actuator event and output-sequence state machine without winding or actuation",
    "Motion timing duration angle and displacement fields with zero observations",
    "Sound light and theatrical-effect relation without playback or performance evidence",
    "Program drum pin barrel card and control-track topology without program execution",
    "Winding key access panel switch and release-point handling abstention",
    "Automaton maker mark serial date and place transcription vacancy firewall",
    "Metal wood textile enamel jewel and lubricant material-claim hold",
    "Automaton intervention-command denylist spanning power isolation tension release fastener removal and conductor contact",
    "Pinch entanglement spring electrical and falling-part hazard-cue reservation",
    "Automaton conservation intervention and custody decision hold",
    "PROV graph for synthetic automaton documentation correction and supersession",
    "Accessible automaton mechanism-status summary with affected-user review reserved",
    "THOS matched-budget zero-person automaton handover protocol",
    "Freed ID zero-key automaton custodian profile with status and recovery refusal",
    "Synthetic stained-glass panel namespace without building-fabric identity claim",
    "Glass piece lead came solder joint and perimeter-came relation graph",
    "Panel frame saddle bar tie bar and support topology with fitness abstention",
    "Paint stain enamel plating and surface-layer claim vacancy",
    "Protective glazing interspace vent and drainage adjacency without design approval",
    "Crack bow bulge loss corrosion and putty cue register without condition diagnosis",
    "Light transmission colour opacity and panel-dimension fields with measurement absent",
    "Temperature humidity condensation weather and pollutant fields held vacant",
    "Panel image rubbing cartoon numbering and derivative provenance braid",
    "Panel removal crating transport storage and reinstallation action firewall",
    "Cleaning edge-gluing copper-foil releading and putty treatment-action firewall",
    "Lead cadmium glass shard sharp-edge and working-at-height hazard reservation",
    "Sacred imagery cultural context and rights-status vacancy without interpretation",
    "Accessible panel-status workload correction and handover summary",
    "Real globe examination measurement housing and handling evaluation evidence gap",
    "Real automaton operation timing safety conservation and specialist-review evidence gap",
    "Real stained-glass condition environment accessibility and affected-user evaluation gap",
    "Globe title custody reproduction privacy legal cultural and affected-party authority exact gate",
    "Automaton operation repair electrical safety professional release and ownership exact gate",
    "Stained-glass sacred heritage remedy Māori data governance and Māori-authority exact gate",
]

SOURCES = [
    {
        "source_id": "LOC-RARE-GLOBES",
        "url": "https://blogs.loc.gov/preservation/2025/07/rehousing-rare-globes/",
        "status": "official Library of Congress Preservation post checked 2026-08-31",
        "use": "globe, gore, stand, axis, housing, base, lid, tray, cushioning, orientation, catalogue, and access vocabulary only; no handling, measurement, housing design, or conservation instruction",
    },
    {
        "source_id": "MET-AUTOMATON-CHARIOT",
        "url": "https://www.metmuseum.org/art/collection/search/207038",
        "status": "official Metropolitan Museum collection record checked 2026-08-31",
        "use": "automaton, spring-driven device, wheel, shaft, joint, motion, material, provenance, and collection-record vocabulary only; no operation, authentication, attribution, repair, or condition claim",
    },
    {
        "source_id": "NPS-STAINED-GLASS",
        "url": "https://www.nps.gov/articles/000/stained-glass.htm",
        "status": "official National Park Service Preservation Matters page checked 2026-08-31; page last updated 2025-06-26",
        "use": "glass, came, putty, frame, protective glazing, documentation, condition-cue, and professional-boundary vocabulary only; no inspection, cleaning, treatment, safety, or preservation recommendation is executed",
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
    "no real person, participant, globe, gore, sphere, ring, stand, housing, automaton, mechanism, spring, gear, cam, shaft, figure, stained-glass panel, glass, came, solder, frame, building, sacred image, observation, measurement, operation, handling, treatment, custody event, network row, or external action",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, detected effect, stability theorem, ultraviolet completion, quantum completion, final physics, or Theory-of-Everything claim",
    "no THOS operational-effectiveness, participant, safety, professional-competence, deployment, AGI, or ASI claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, or affected-party acceptance claim",
    "no globe handling or housing, automaton winding or operation, stained-glass inspection or treatment, product or workplace safety, ownership, custody, copyright, privacy remedy, land, heritage, sacred-context, legal, cultural, affected-party, taonga, matauranga, Maori-data-governance, or Maori-authority decision",
    "no accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness, personhood, proof, canon, or Stage 20 claim",
]

STARTUP_FAILURES = [
    ("SA6786-START-N001", "A retained-negative register window exceeded the bounded display and truncated before EOF.", "SA6786-START-P001", "Smaller non-overlapping windows completed the retained-negative read through EOF."),
    ("SA6786-START-N002", "A combined four-window packet projection exceeded the model-visible result bound.", "SA6786-START-P002", "Each packet window was reread separately and completed without repository mutation."),
    ("SA6786-START-N003", "A two-block owner-manifest projection truncated midway through the second block.", "SA6786-START-P003", "Sixty-entry manifest windows completed all 723 inherited entries through EOF."),
    ("SA6786-START-N004", "A file-size probe was sent as raw PowerShell to the JavaScript orchestration surface and was rejected before shell execution.", "SA6786-START-P004", "The corrected exec-command wrapper returned the exact file sizes and line counts."),
    ("SA6786-START-N005", "PowerShell interpreted a colon-adjacent branch variable in a Git fetch refspec and produced an invalid refspec before fetching.", "SA6786-START-P005", "A format-string refspec plus separate scalar live-remote probe established exact source equality."),
    ("SA6786-START-N006", "The corrected combined fetch-and-equality wrapper outlived its presentation window and exposed no session handle in the projection.", "SA6786-START-P006", "Process settlement and separate local upstream tracking and fresh-live probes proved four-way equality without repeating source validation."),
    ("SA6786-START-N007", "A PowerShell foreach result was piped without array materialization and failed with EmptyPipeElement before search.", "SA6786-START-P007", "Array materialization corrected the parser shape and the later exact owner-phase receipt directory was used."),
    ("SA6786-START-N008", "A broad D-drive receipt-content search outlived its wrapper and yielded no attributable result.", "SA6786-START-P008", "Bounded depth-two discovery resolved the exact Elowen v678-v5 validation directory and all six digests."),
    ("SA6786-START-N009", "A recursive validation-directory discovery stalled and was terminated as a read-only zero-credit attempt.", "SA6786-START-P009", "Exact owner and phase path enumeration returned the four external receipt files immediately."),
    ("SA6786-START-N010", "A combined source materialized-file and tracked-file count crossed its yield boundary without attributable output.", "SA6786-START-P010", "The owned-lane materialized-file count was measured separately after sparse configuration."),
    ("SA6786-START-N011", "The inherited broad scripts and tests cone materialized 2399 files and crossed the 2000-file stop before any x1 artifact was written.", "SA6786-START-P011", "Non-cone exact owner source and v678 script-test patterns reduced the clean lane to 726 materialized files."),
    ("SA6786-START-N012", "A full inherited source-and-proposal ledger projection truncated before its semantic-audit tail.", "SA6786-START-P012", "A bounded scalar projection recovered the 8570-row chain, 4455 reachable unique records, zero parse failures, and explicit non-universal novelty boundary."),
    ("SA6786-X1-N001", "The first planning builder failed closed because SA6786-N034 scored 0.8889 against inherited EC6766-N018; no x1 packet artifact was written.", "SA6786-X1-P001", "The colliding generic maintenance title was replaced by a distinct automaton power-isolation and tension-release intervention denylist while the 0.75 threshold remained unchanged."),
]

SKILLS = [
    "synthetic-globe-record-namespace",
    "globe-gore-seam-topology",
    "globe-measurement-vacancy",
    "globe-housing-action-firewall",
    "globe-derivative-provenance",
    "automaton-power-source-vacancy",
    "automaton-linkage-topology",
    "automaton-motion-measurement-hold",
    "automaton-operation-action-firewall",
    "automaton-hazard-reservation",
    "stained-glass-panel-topology",
    "stained-glass-environment-vacancy",
    "stained-glass-treatment-action-hold",
    "stained-glass-hazard-reservation",
    "artifact-custody-provenance-braid",
    "artifact-accessibility-status",
    "artifact-workload-stop-control",
    "zero-key-artifact-custodian",
    "thos-artifact-proxy-firewall",
    "maori-authority-reservation",
]

RUNNERS = [
    "ghc_family_sylven_arc_v678_v6_proposal_contracts.py",
    "ghc_family_sylven_arc_v678_v6_positive_controls.py",
    "ghc_family_sylven_arc_v678_v6_mutation_rejector.py",
    "ghc_family_sylven_arc_v678_v6_globe_topology.py",
    "ghc_family_sylven_arc_v678_v6_automaton_linkage.py",
    "ghc_family_sylven_arc_v678_v6_stained_glass_custody.py",
    "ghc_family_sylven_arc_v678_v6_privacy.py",
    "ghc_family_sylven_arc_v678_v6_accessibility.py",
    "ghc_family_sylven_arc_v678_v6_portfolio.py",
    "build_ghc_family_sylven_arc_v678_v6_report.py",
]


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", "-C", str(repo), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for offset, title in enumerate(TITLES, start=1):
        proposal_id = f"SA6786-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-O", "RFC-8785"]
        if offset <= 20 or offset in {55, 58}:
            source_ids.append("LOC-RARE-GLOBES")
        if 21 <= offset <= 40 or offset in {56, 59}:
            source_ids.append("MET-AUTOMATON-CHARIOT")
        if 41 <= offset <= 60:
            source_ids.append("NPS-STAINED-GLASS")
        if offset in {15, 38, 54, 57}:
            source_ids.append("WCAG-2.2")
        if offset in {17, 18, 37, 40, 53, 58, 59, 60}:
            source_ids.append("W3C-VC-DATA-MODEL-2.0")
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing real object, observation, measurement, operation, treatment, identity, rights, professional, legal, cultural, or authority claims.",
                "null_or_failure_condition": f"The {proposal_id} contract accepts a missing or contradictory field, ingests a real identifier, uses an unauthorized outcome, or implies an observation, intervention, result, competence, right, or authority grant.",
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": sorted(set(source_ids)),
                "concrete_artifacts": [f"docs/{OWNER_SLUG}/{PHASE}/x2/contracts/{proposal_id}.json", f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{proposal_id}-receipt.json"],
                "falsifier_or_acceptance_gate": f"One positive zero-row fixture must satisfy {proposal_id} and four preregistered invalid mutations must be rejected; represented, open, and exact-gated rows receive no executed-real-world credit.",
                "rollback_or_recovery": f"Quarantine the {proposal_id} output, retain the failed witness, restore the last exact Git-blob input, and rerun only the isolated dependency after an additive correction.",
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
    batch = subprocess.run(["git", "-C", str(repo), "cat-file", "--batch"], input=request, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
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
        neighbors.append({"proposal_id": row["proposal_id"], "title": row["title"], "nearest_id": nearest[0], "nearest_title": nearest[1], "nearest_path": nearest[2], "token_jaccard": round(jaccard(row["title"], nearest[1]), 4)})
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
        "limitation": "This is a direct audit of every reachable proposal-bearing JSON artifact at the exact immutable source tree. It supports bounded semantic distinctness but is not a universal novelty proof and does not establish scientific novelty.",
    }


def mutation_plan(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    mutation_types = [("missing_hypothesis", "required hypothesis omitted"), ("unknown_outcome_label", "outcome outside the four-label vocabulary"), ("authority_escalation", "synthetic record claims real-world authority"), ("real_identifier_or_measurement", "a raw identifier or ungrounded measurement is introduced")]
    return [{"mutation_id": f"{row['proposal_id']}-M{index}", "proposal_id": row["proposal_id"], "mutation_kind": kind, "expected_rejection": reason, "execution_status": "preregistered_unexecuted_x1"} for row in rows for index, (kind, reason) in enumerate(mutation_types, start=1)]


def planned_rows(prefix: str, count: int, status: str) -> list[dict[str, Any]]:
    return [{"task_id": f"{prefix}-{index:03d}", "description": f"Bounded owner-local {prefix.casefold()} task {index:03d}", "status": status, "real_world_rows": 0, "external_actions": 0} for index in range(1, count + 1)]


def startup_methods() -> list[dict[str, Any]]:
    methods = []
    for failed_id, failed_description, pass_id, pass_description in STARTUP_FAILURES:
        methods.append({"method_id": failed_id, "description": failed_description, "recovered_by": pass_id, "state_change": False, "status": "failed_zero_credit", "truth": False})
        methods.append({"method_id": pass_id, "description": pass_description, "failed_witness_preserved": failed_id, "status": "bounded_pass", "truth": True})
    return methods


def build(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != SOURCE:
        raise SystemExit("x1 builder requires the exact corrected Elowen source head")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("x1 builder requires the exact Sylven owner branch")
    allowed_untracked = {
        "scripts/build_ghc_family_sylven_arc_v678_v6_x1.py",
        "scripts/ghc_family_sylven_arc_v678_v6_x1_manifest.py",
        "tests/test_ghc_family_sylven_arc_v678_v6_x1.py",
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
    inherited_reviews = [{"proposal_id": row["nearest_id"], "title": row["nearest_title"], "source_path": row["nearest_path"], "status": "reviewed_inherited_zero_credit", "novelty_credit": 0, "completion_credit": 0} for row in sorted(audit["neighbors"], key=lambda value: value["token_jaccard"], reverse=True)[:20]]
    mutation_rows = mutation_plan(rows)

    dump(base / "source-verification.json", {
        "owner": OWNER, "phase": PHASE, "branch": BRANCH, "source_branch": SOURCE_BRANCH, "source": SOURCE,
        "anchors": {"elowen_source": ELOWEN_SOURCE, "elowen_x1": ELOWEN_X1, "elowen_evidence": ELOWEN_EVIDENCE, "elowen_first_final": ELOWEN_FIRST_FINAL, "elowen_corrected_final": ELOWEN_CORRECTED_FINAL},
        "source_to_final_phase_commits": 4, "source_to_final_merges": 0, "source_clean_zero_divergent_and_fresh_four_way_equal": True,
        "elowen_failed_canonical_receipt_sha256": ELOWEN_FAILED_CANONICAL_RECEIPT_SHA256, "elowen_failed_canonical_latch_sha256": ELOWEN_FAILED_CANONICAL_LATCH_SHA256, "elowen_failed_canonical_payload_sha256": ELOWEN_FAILED_CANONICAL_PAYLOAD_SHA256,
        "elowen_component_receipt_sha256": ELOWEN_COMPONENT_RECEIPT_SHA256, "elowen_component_latch_sha256": ELOWEN_COMPONENT_LATCH_SHA256, "elowen_component_payload_sha256": ELOWEN_COMPONENT_PAYLOAD_SHA256,
        "elowen_canonical_invocation_count": 1, "elowen_canonical_success_count": 0, "elowen_canonical_replay_count": 0,
        "elowen_component_invocation_count": 1, "elowen_component_success_count": 1, "elowen_component_replay_count": 0,
        "elowen_terminal_status": "VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE_WITH_ZERO_FAILED_CANONICAL_CREDIT", "failed_canonical_preserved_at_zero_success_credit": True, "inherited_validation_replayed": False, "verified_date": GENERATED_DATE,
    })
    dump(base / "new-proposal-freeze.json", {"status": "FROZEN_PLANNING_ONLY", "declared_chain_before": ACTIVATION["declared_proposals"], "new_sylven_proposals": len(rows), "declared_chain_after": ACTIVATION["declared_proposals"] + len(rows), "proposals": rows})
    dump(base / "semantic-neighbor-audit.json", audit)
    dump(base / "inherited-zero-credit-review.json", {"count": len(inherited_reviews), "novelty_credit": 0, "completion_credit": 0, "reviews": inherited_reviews})
    dump(base / "mutation-preregistration.json", {"proposal_count": len(rows), "mutations_per_proposal": 4, "mutation_count": len(mutation_rows), "mutations": mutation_rows})
    dump(base / "portfolio-freeze.json", {"safe_now": planned_rows("SA6786-SAFE", 60, "planned_unexecuted_x1"), "candidate": planned_rows("SA6786-CAND", 30, "planned_unexecuted_x1"), "exact_approval": planned_rows("SA6786-EXACT", 20, "unexecuted_exact_gate"), "blocked": planned_rows("SA6786-BLOCK", 10, "blocked_unexecuted"), "caps_are_ceilings_not_quotas": True})
    dump(base / "skill-runner-plan.json", {
        "phase_local_skills": [{"skill_id": f"SA6786-SKILL-{index:02d}", "name": name, "status": "planned_unbuilt_x1", "global_install": False} for index, name in enumerate(SKILLS, start=1)],
        "family_current_runners": [{"runner_id": f"SA6786-RUNNER-{index:02d}", "name": name, "status": "planned_unbuilt_x1"} for index, name in enumerate(RUNNERS, start=1)],
        "successor_skill_recommendations": [{"recommendation_id": f"SA6786-SUCCESSOR-SKILL-{index:02d}", "seed": name, "credit": "zero_sylven_completion_credit"} for index, name in enumerate(SKILLS[:10], start=1)],
        "successor_runner_recommendations": [{"recommendation_id": f"SA6786-SUCCESSOR-RUNNER-{index:02d}", "seed": name, "credit": "zero_sylven_completion_credit"} for index, name in enumerate(RUNNERS, start=1)],
    })
    dump(base / "clean-fix-refine-plan.json", {"owner_tasks": planned_rows("SA6786-CFR", 60, "planned_unexecuted_x1"), "successor_recommendations": [{"recommendation_id": f"SA6786-SUCCESSOR-CFR-{index:03d}", "description": f"Distinct zero-credit successor CLEAN/FIX/REFINE seed {index:03d}", "credit": "zero_sylven_completion_credit"} for index in range(1, 31)]})
    dump(base / "successor-recommendations.json", {"recipient_unresolved_until_terminal_gate": True, "recommended_practice": "synthetic horological-dial layout and inscription documentation", "recommendation_count": 50, "recommendations": [{"recommendation_id": f"SA6786-SUCC-SEED-{index:03d}", "description": f"Bounded successor seed {index:03d}; no Sylven execution or completion credit", "credit": "zero_sylven_completion_credit"} for index in range(1, 51)]})
    dump(base / "official-source-ledger.json", {"checked_date": GENERATED_DATE, "sources": SOURCES, "source_boundary": "Official and primary sources supply current vocabulary and refusal conditions only. They are not observations, measurements, operation or treatment instructions, endorsements, conformance certificates, legal interpretations, affected-party decisions, cultural ratifications, professional approvals, or authority grants."})
    dump(base / "primary-pillar-and-lens.json", {"primary_pillar": "THOS Body", "secondary_pillars": ["GMUT Mind", "Freed ID and CBR Heart"], "bounded_wholly_synthetic_learning_lenses": ["globemaking records analyst for synthetic zero-globe documentation", "mechanical-automaton linkage analyst for synthetic zero-machine records", "stained-glass panel handover steward for synthetic zero-window records"], "real_world_rows_or_actions": 0, "professional_or_authority_credit": 0})
    dump(base / "protected-gate-register.json", {"protected_gates": PROTECTED_GATES, "inherited_open_gaps": ACTIVATION["open_gaps"], "inherited_exact_gates": ACTIVATION["exact_gates"], "authority_noncompensation": True})
    dump(base / "method-flow-startup.json", {"activation_baseline": ACTIVATION, "methods": methods, "new_failed_witnesses": failure_count, "new_bounded_passing_witnesses": pass_count, "new_effective_methods": len(methods), "current_overlay": {"effective_negatives": ACTIVATION["effective_negatives"] + failure_count, "effective_methods": ACTIVATION["effective_methods"] + len(methods), "retained_failed_witnesses": ACTIVATION["retained_failed_witnesses"] + failure_count, "bounded_passing_witnesses": ACTIVATION["bounded_passing_witnesses"] + pass_count, "open_gaps": ACTIVATION["open_gaps"], "exact_gates": ACTIVATION["exact_gates"]}, "failure_erasure_forbidden": True})
    dump(base / "route-hold.json", {"route_state": "HOLD_UNTIL_SYLVEN_V678_V6_TERMINAL_GATE", "successor_inferred": False, "prospective_successor_title": "Caelen Morrow", "prospective_successor_phase": "v678-v7", "precontact_performed": False, "send_count": 0, "newest_live_authority_required_at_terminal_gate": True})
    dump(base / "phase-truth.json", {"owner": OWNER, "phase": PHASE, "status": "FROZEN_PLANNING_ONLY", "source": SOURCE, "new_proposals": len(rows), "declared_chain_after": ACTIVATION["declared_proposals"] + len(rows), "expected_dispositions": dict(Counter(row["expected_disposition"] for row in rows)), "executed_core_outcomes": {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")}, "x2_implementation_present": False, "x2_outcomes_claimed": False, "real_world_rows": 0, "external_actions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    text(base / "identity-and-boundary.md", """# Sylven Arc v678-v6 identity and authority boundary

Sylven Arc, optionally they/them, is relational working language only. The phase role is **relational metadata lantern and reversible handover steward**, with the hope of keeping large evidence fields navigable without hiding uncertainty or protected authority vacancies.

This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no empirical result here. THOS remains synthetic proxy evidence without real participants, operators, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction with zero real keys, proofs, lifecycle events, or trust governance. CBR, globemaking, automaton operation, stained-glass conservation, ownership, copyright, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, matauranga, taonga, Maori data governance, and Maori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapu, and Maori authorities.
""")
    text(base / "x1-overview.md", f"""# Sylven Arc {PHASE} planning-only x1 overview

This x1 freezes sixty bounded proposal contracts against the declared 8,570-row chain and every proposal-bearing JSON artifact reachable at Elowen's exact corrected final `{SOURCE}`. Twenty inherited neighbors are reviewed at zero novelty and completion credit. Four invalid mutations per proposal are preregistered but unexecuted.

The primary pillar is THOS Body through wholly synthetic globemaking records, mechanical-automaton linkage records, and stained-glass panel handover lenses. GMUT Mind and Freed ID/CBR Heart remain visible and protected. There are zero real people, globes, automata, stained-glass panels, measurements, observations, tools, operations, services, treatments, identity events, network ingestions, external actions, or authority decisions.

No x2 implementation or observed outcome exists in this freeze. Only `completed`, `represented`, `open_gap`, and `exact_gate` are authorized future outcome labels, and the terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    build(args.repo.resolve())


if __name__ == "__main__":
    main()

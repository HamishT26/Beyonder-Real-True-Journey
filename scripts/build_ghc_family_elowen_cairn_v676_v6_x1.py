#!/usr/bin/env python3
"""Build the deterministic planning-only Elowen Cairn v676-v6 x1 packet."""

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
PHASE = "v676-v6"
BRANCH = "codex/GHC-Family/elowen-cairn-v676-v6-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v676-v5-full-tools"
SOURCE = "56b4e82909b3d7197b817a2415da592f8fc7df6e"
TAMAR_SOURCE = "ce97f35c2351c8daef6f48b4dc1c60928e1fc1be"
TAMAR_X1 = "664ee4309d5ba99d98aae2be09f067af6ecf47dc"
TAMAR_EVIDENCE = "0d935f546f107ea2070c79d1b070d6bbb0a198cf"
TAMAR_FIRST_FINAL = "58a5fa6edeafaf2c1e3048036e131f857d7996d3"
TAMAR_CORRECTION_1 = "8d64b74e2f92c0675addf6fcc10e68f8c774e3e8"
TAMAR_CORRECTION_2 = "2133ec23c7226b4614abd1b63818136dd02202bd"
TAMAR_FINAL = SOURCE
TAMAR_FAILED_CANONICAL_RECEIPT_SHA256 = "e9fc4dce5135b235d111e47945c99b06d6fe10b35f27159a879dd0040d407f20"
TAMAR_CANONICAL_RECEIPT_SHA256 = "ada1780f905a8b9cc9c6db5889cdcc647be1a368371a6d7ae4c28bb2c50395ea"
TAMAR_CANONICAL_PAYLOAD_SHA256 = "db803c664949e02ecc30f5c4143727e28dafc8ff6c75b3d783c702a1202b8bd8"
GENERATED_DATE = "2026-08-30"

ACTIVATION = {
    "declared_proposals": 7590,
    "effective_negatives": 42441,
    "effective_methods": 33118,
    "retained_failed_witnesses": 14102,
    "bounded_passing_witnesses": 19705,
    "open_gaps": 357,
    "exact_gates": 349,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

TITLES = [
    "Synthetic mechanical-typewriter namespace without object-identity claim",
    "Keyboard keytop row and character-assignment topology with inscription abstention",
    "Key-lever typebar linkage adjacency graph with motion abstention",
    "Typebasket segment pivot and rest relation map with jam-diagnosis vacancy",
    "Carriage rail truck and return topology without actuation",
    "Platen feed-roller paper-bail and line-space relation contract",
    "Escapement rack pinion and spacing-state representation without measurement",
    "Ribbon spool vibrator guide and colour-layer claim firewall",
    "Shift-key segment basket and case-transition representation",
    "Tabulator stop rack and column-setting topology without document inference",
    "Margin stop bell and end-of-line cue representation with zero listening evidence",
    "Backspace and carriage-advance command-state conflict guard",
    "Paper table scale guide and alignment vacancy without dimensional observation",
    "Serial plate maker model date and place transcription firewall",
    "Casing finish coating rubber felt and lubricant material-claim hold",
    "Rust crack wear deformation residue and dust cue register without diagnosis",
    "Motor cord switch and insulation safety hold for synthetic electric-typewriter records",
    "Cleaning oiling adjustment disassembly and repair-action firewall",
    "Typewriter image crop orientation scale and derivative lineage without authenticity claim",
    "Typing-sample glyph content language authorship and privacy-minimization firewall",
    "Correspondence document custody copyright and disclosure authority vacancy",
    "Correction readback supersession and append-only typewriter-record braid",
    "Accessible mechanism-status summary with text alternatives noncolour cues and focus order",
    "Workload pause stop unresolved-hold and shift-handover queue",
    "Pseudonymous typewriter-component capsule with zero keys and zero proofs",
    "PROV relation graph for synthetic typewriter documentation and correction",
    "Deterministic typewriter-record canonical JSON with tri-state vacancy Unicode and finite-number refusal",
    "Metrology firewall for pitch travel force and timing fields with zero observations",
    "GMUT discrete-transition and constraint graph on synthetic typewriter linkage topology",
    "GMUT gauge and covariance analogy firewall for keyboard mapping",
    "GMUT damping and contact obligation board for platen and ribbon without physical model",
    "THOS matched-budget zero-person typewriter-documentation protocol",
    "Freed ID zero-key custodian role lease with expiry refusal and recovery vacancy",
    "CBR correction notice contest and remedy-vacancy map for synthetic records",
    "Accessible static typewriter dossier audit with manual evaluation reserved",
    "Resumable owner-local documentation command with idempotent evidence cursor",
    "Zero-network NMAH lexicon bridge for fabricated typebar records",
    "Real typewriter observation measurement professional evaluation and independent-review gap",
    "Professional mechanical electrical material-safety repair treatment and release exact gate",
    "Ownership authorship copyright privacy cultural and Māori-authority decision gate",
]

SOURCES = [
    {
        "source_id": "NMAH-COLUMBIA-TYPEWRITER",
        "url": "https://americanhistory.si.edu/collections/object/nmah_849917",
        "status": "official Smithsonian National Museum of American History object page discovered 2026-08-30; direct open returned an internal fetch error, so only bounded search-result vocabulary is used",
        "use": "typewriter, manual, index-selection, variable-spacing, object-record, and component vocabulary only; zero download, observation, measurement, or conformance claim",
    },
    {
        "source_id": "NMAH-ANGELOU-TYPEWRITER-VISUAL",
        "url": "https://americanhistory.si.edu/visual-descriptions/visual-description-in-pursuit/angelou-typewriter-tactile",
        "status": "official Smithsonian National Museum of American History visual-description page discovered 2026-08-30; direct open timed out, so only bounded search-result vocabulary is used",
        "use": "keyboard, carriage, platen, typebar, ribbon, and text-alternative vocabulary only; no object observation, authorship inference, or accessibility conformance claim",
    },
    {
        "source_id": "BIPM-VIM",
        "url": "https://www.bipm.org/en/committees/jc/jcgm/wg/jcgm-wg2-vim",
        "status": "official BIPM JCGM-WG2 VIM page checked 2026-08-30; WG2 maintains the VIM and identifies corrected VIM3",
        "use": "quantity, measurement, indication, uncertainty, and metrological-traceability refusal vocabulary only; zero measurement",
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
    "no real person, participant, typewriter, keyboard, keytop, typebar, typebasket, carriage, platen, feed roller, bail, escapement, ribbon, motor, cord, switch, tool, document, typing sample, image, collection, site, observation, measurement, repair, custody event, release, or external action",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, detected effect, ultraviolet completion, quantum completion, or Theory-of-Everything claim",
    "no THOS operational-effectiveness, safety, professional-competence, deployment, AGI, or ASI claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, or trust-governance claim",
    "no cleaning, oiling, adjustment, disassembly, repair, electrical-safety, material, condition, authenticity, maker, model, date, place, authorship, ownership, custody, copyright, disclosure, legal, remedy, cultural, affected-party, taonga, mātauranga, Māori-data-governance, or Māori-authority decision",
    "no accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness, personhood, proof, canon, or Stage 20 claim",
]

STARTUP_FAILURES = [
    (
        "EC6766-START-N001",
        "The first combined exact-packet display exceeded the bounded output window and did not establish a complete read.",
        "EC6766-START-P001",
        "Non-overlapping exact document windows completed the source-packet read through EOF without repository change.",
    ),
    (
        "EC6766-START-N002",
        "The first combined mutable-state display exceeded the bounded output window.",
        "EC6766-START-P002",
        "Bounded state and schema windows completed the read while preserving newer live authority precedence.",
    ),
    (
        "EC6766-START-N003",
        "The first canonical-receipt hash lookup used an overbroad validation-root projection and returned no attributable result.",
        "EC6766-START-P003",
        "A bounded exact receipt-directory inventory recovered and verified both immutable receipt digests and the successful payload digest.",
    ),
    (
        "EC6766-START-N004",
        "The first sequential lifecycle-manifest verifier remained active beyond its attribution window and yielded no complete result.",
        "EC6766-START-P004",
        "A bounded commit-colon-path Git-blob batch verifier passed all 3,028 exact normalized-LF manifest entries without mutation.",
    ),
    (
        "EC6766-START-N005",
        "A whole-tree manifest recovery unnecessarily enumerated the shared repository and exceeded the bounded diagnostic scope.",
        "EC6766-START-P005",
        "Direct exact commit-colon-path requests replaced tree enumeration and preserved the same 3,028-entry passing witness.",
    ),
    (
        "EC6766-START-N006",
        "A broad candidate-term Git grep timed out and was interrupted before producing attributable novelty evidence.",
        "EC6766-START-P006",
        "The exact proposal-bearing JSON tribunal became the sole semantic-neighbor witness; no broad grep result receives credit.",
    ),
    (
        "EC6766-START-N007",
        "The additive worktree and sparse-configuration wrappers yielded before their owned Git process completed.",
        "EC6766-START-P007",
        "Persisted worktree, process, index-lock, branch, and sparse-state checks established one completed clean lane without repeating the mutation.",
    ),
    (
        "EC6766-START-N008",
        "The first validator-scaffold copy assumed the current source contained a materialized same-phase validator and failed on that exact missing path.",
        "EC6766-START-P008",
        "The observed owner-local v674-v7 compatibility validator supplied the narrow scaffold without changing any inherited lane.",
    ),
    (
        "EC6766-START-N009",
        "One broad combined semantic scaffold scan overflowed the display bound and did not establish a complete review.",
        "EC6766-START-P009",
        "Bounded per-file anchored scans completed the review; the overflow receives no source-inspection credit.",
    ),
    (
        "EC6766-X1-N001",
        "The first planning builder failed closed because proposal EC6766-N037 equalled the 0.75 inherited semantic-neighbor quarantine threshold; no packet artifact was written.",
        "EC6766-X1-P001",
        "The isolated failed dependency identified the single colliding row; its title was replaced with a distinct zero-network NMAH lexicon contract and the unchanged 0.75 gate was retained.",
    ),
]

SKILLS = [
    "synthetic-typewriter-namespace",
    "keyboard-character-topology",
    "typebar-linkage-vacancy",
    "carriage-return-abstention",
    "platen-feed-relation",
    "escapement-spacing-vacancy",
    "ribbon-material-claim-hold",
    "shift-case-transition-guard",
    "tabulator-column-inference-firewall",
    "typewriter-inscription-privacy-filter",
    "typewriter-image-lineage",
    "typewriter-measurement-vacancy",
    "typewriter-repair-action-hold",
    "typewriter-electrical-safety-reservation",
    "typewriter-provenance-braid",
    "accessible-typewriter-summary",
    "typewriter-workload-handover",
    "zero-key-typewriter-custodian",
    "gmut-typewriter-analogy-firewall",
    "maori-authority-reservation",
]

RUNNERS = [
    "ghc_family_elowen_cairn_v676_v6_proposal_contracts.py",
    "ghc_family_elowen_cairn_v676_v6_positive_controls.py",
    "ghc_family_elowen_cairn_v676_v6_mutation_rejector.py",
    "ghc_family_elowen_cairn_v676_v6_typewriter_topology.py",
    "ghc_family_elowen_cairn_v676_v6_measurement_vacancy.py",
    "ghc_family_elowen_cairn_v676_v6_provenance.py",
    "ghc_family_elowen_cairn_v676_v6_privacy.py",
    "ghc_family_elowen_cairn_v676_v6_accessibility.py",
    "ghc_family_elowen_cairn_v676_v6_portfolio.py",
    "build_ghc_family_elowen_cairn_v676_v6_report.py",
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
        proposal_id = f"EC6766-N{offset:03d}"
        if offset <= 28:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 36:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 38:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-O", "RFC-8785"]
        if offset <= 20 or offset in {26, 29, 30, 31, 37, 38, 39}:
            source_ids.extend(["NMAH-COLUMBIA-TYPEWRITER", "NMAH-ANGELOU-TYPEWRITER-VISUAL"])
        if offset in {7, 13, 28, 31, 38, 39}:
            source_ids.append("BIPM-VIM")
        if offset in {19, 23, 35}:
            source_ids.append("WCAG-2.2")
        if offset in {20, 21, 22, 25, 33, 34, 39, 40}:
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
        raise SystemExit("x1 builder requires the exact immutable corrected Tamar source head")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("x1 builder requires the exact Elowen owner branch")
    allowed_untracked = {
        "scripts/build_ghc_family_elowen_cairn_v676_v6_x1.py",
        "scripts/ghc_family_elowen_cairn_v676_v6_x1_manifest.py",
        "tests/test_ghc_family_elowen_cairn_v676_v6_x1.py",
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
                "liora_v676_v4_final_and_tamar_source": TAMAR_SOURCE,
                "tamar_x1": TAMAR_X1,
                "tamar_evidence": TAMAR_EVIDENCE,
                "tamar_first_final": TAMAR_FIRST_FINAL,
                "tamar_correction_1": TAMAR_CORRECTION_1,
                "tamar_correction_2": TAMAR_CORRECTION_2,
                "tamar_corrected_final": TAMAR_FINAL,
            },
            "source_to_final_phase_commits": 6,
            "source_to_final_merges": 0,
            "source_clean_zero_divergent_and_fresh_four_way_equal": True,
            "tamar_failed_canonical_receipt_sha256": TAMAR_FAILED_CANONICAL_RECEIPT_SHA256,
            "tamar_successful_canonical_receipt_sha256": TAMAR_CANONICAL_RECEIPT_SHA256,
            "tamar_successful_canonical_payload_sha256": TAMAR_CANONICAL_PAYLOAD_SHA256,
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
            "safe_now": planned_rows("EC6766-SAFE", 60, "planned_unexecuted_x1"),
            "candidate": planned_rows("EC6766-CAND", 30, "planned_unexecuted_x1"),
            "exact_approval": planned_rows("EC6766-EXACT", 20, "unexecuted_exact_gate"),
            "blocked": planned_rows("EC6766-BLOCK", 10, "blocked_unexecuted"),
            "caps_are_ceilings_not_quotas": True,
        },
    )
    dump(
        base / "skill-runner-plan.json",
        {
            "phase_local_skills": [
                {
                    "skill_id": f"EC6766-SKILL-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                    "global_install": False,
                }
                for index, name in enumerate(SKILLS, start=1)
            ],
            "family_current_runners": [
                {
                    "runner_id": f"EC6766-RUNNER-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                }
                for index, name in enumerate(RUNNERS, start=1)
            ],
            "successor_skill_recommendations": [
                {
                    "recommendation_id": f"EC6766-SUCCESSOR-SKILL-{index:02d}",
                    "seed": name,
                    "credit": "zero_elowen_completion_credit",
                }
                for index, name in enumerate(SKILLS[:10], start=1)
            ],
            "successor_runner_recommendations": [
                {
                    "recommendation_id": f"EC6766-SUCCESSOR-RUNNER-{index:02d}",
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
            "owner_tasks": planned_rows("EC6766-CFR", 60, "planned_unexecuted_x1"),
            "successor_recommendations": [
                {
                    "recommendation_id": f"EC6766-SUCCESSOR-CFR-{index:03d}",
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
                    "recommendation_id": f"EC6766-SUCC-SEED-{index:03d}",
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
            "primary_pillar": "GMUT Mind",
            "secondary_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "bounded_wholly_synthetic_learning_lenses": [
                "typewriter intake-records analyst for synthetic zero-object records",
                "mechanical linkage-topology documentation analyst for synthetic typewriter relations",
                "accessible repair-handover steward for synthetic correction and workload records",
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
            "prospective_successor_phase": "v676-v7",
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
        """# Elowen Cairn v676-v6 identity and authority boundary

Elowen Cairn, optionally they/them, is relational working language only. The phase role is **relational boundary cartographer and evidence steward**, with the hope of keeping possibility distinct from evidence and every correction safely retractable.

This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no empirical result here. THOS remains synthetic proxy evidence without real participants, operators, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction with zero real keys, proofs, lifecycle events, or trust governance. CBR, ownership, authorship, copyright, repair, electrical and material safety, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, mātauranga, taonga, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities.
""",
    )
    text(
        base / "x1-overview.md",
        f"""# Elowen Cairn {PHASE} planning-only x1 overview

This x1 freezes forty bounded proposal contracts against the declared 7,590-row chain and every proposal-bearing JSON artifact reachable at Tamar's exact corrected final `{SOURCE}`. Twenty inherited neighbors are reviewed at zero novelty and completion credit. Four invalid mutations per proposal are preregistered but unexecuted.

The primary pillar is GMUT Mind through wholly synthetic typewriter intake, mechanical linkage-topology documentation, and accessible repair-handover lenses. THOS Body and Freed ID/CBR Heart remain visible and protected. There are zero real people, typewriters, keyboards, typebars, carriages, platens, ribbons, motors, documents, measurements, observations, tools, repairs, identity events, external actions, or authority decisions.

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

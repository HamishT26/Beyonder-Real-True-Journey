#!/usr/bin/env python3
"""Build the deterministic planning-only Tamar Vey v676-v5 x1 packet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


OWNER = "Tamar Vey"
OWNER_SLUG = "tamar-vey"
PHASE = "v676-v5"
BRANCH = "codex/GHC-Family/tamar-vey-v676-v5-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v676-v4-full-tools"
SOURCE = "ce97f35c2351c8daef6f48b4dc1c60928e1fc1be"
LIORA_SOURCE = "15a8eb4c7e6abc86f629af12ff29c9893e7723cb"
LIORA_X1 = "2c5f1f344966bc93e89c24fdf3ccb1f9fe0f76b8"
LIORA_EVIDENCE = "c976479e91f94270f0e5cde975144865363bb618"
LIORA_FINAL = SOURCE
LIORA_CANONICAL_RECEIPT_SHA256 = "59b37fc4bb4b549b71a2cfe6ed748157bf0f775fa34c05fd40aef30440777607"
LIORA_CANONICAL_PAYLOAD_SHA256 = "40be037bc74f3fb8cdaffa76b9cff32e6e345387184ab37c4c0e1fb4e3e69379"
GENERATED_DATE = "2026-08-30"

ACTIVATION = {
    "declared_proposals": 7550,
    "effective_negatives": 42228,
    "effective_methods": 32452,
    "retained_failed_witnesses": 13889,
    "bounded_passing_witnesses": 19252,
    "open_gaps": 355,
    "exact_gates": 347,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

TITLES = [
    "Synthetic codex binding namespace without object-identity claim",
    "Textblock gathering and foliation topology contract",
    "Quire signature adjacency graph with absent observation state",
    "Sewing-station and support-relation vacancy map",
    "Board attachment and joint-topology representation",
    "Spine-lining layer-order representation without material claim",
    "Endpaper pastedown and textblock relation contract",
    "Covering-material identification vacancy",
    "Thread adhesive and sewing-support material-claim hold",
    "Opening-angle observation vacancy without measurement",
    "Textblock square and board-edge alignment unknown-state ledger",
    "Leaf-loss detachment and insertion ambiguity firewall",
    "Pagination and foliation label provenance without content claim",
    "Temperature humidity and light zero-sensor storage record",
    "Handling support and cradle-state representation without action",
    "Treatment proposal versus performed binding-intervention firewall",
    "Collation plan without physical disbinding",
    "Rebinding substitution hold and reversibility record",
    "Minimal-intervention decision vacancy for bound material",
    "Append-only errata braid for disputed collation notes",
    "Chain-of-custody edge ledger for synthetic gathering diagrams",
    "Attribution abstention matrix for unsigned binding evidence",
    "Shelfmark inscription and marginalia privacy-minimization filter",
    "Surrogate-view consent hold for diagram publication",
    "Claimant-conflict resolver that refuses title transfer",
    "Accessible nonvisual binding-structure summary",
    "Focus-order audit shell for diagram-free structure navigation",
    "Comprehension echo checkpoint for contested catalogue amendments",
    "Cognitive-load budget and unresolved-leaf turnover queue",
    "Crash-resumable collation checkpoint with idempotent evidence cursor",
    "Mould pest and contamination suspicion without diagnosis",
    "Tool reference and material-suitability vacancy",
    "THOS dependency graph for synthetic book-intake handover",
    "Pseudonymous component capsule with zero signing material",
    "Contestability docket for denied access and redress vacancy",
    "GMUT fibre-network analogy firewall",
    "Real condition observations and material-identification evidence gap",
    "Independent book-conservator and affected-user evidence gap",
    "Professional repair disbinding rebinding treatment and release exact gate",
    "Affected tangata whenua heritage taonga and cultural-object authority reservation",
]

SOURCES = [
    {
        "source_id": "CCI-BASIC-CARE-BOOKS",
        "url": "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/basic-care-books.html",
        "status": "official Canadian Conservation Institute page dated 2025-12-02 and checked 2026-08-30",
        "use": "book structure, handling, binding-damage, specialist-referral, and intervention-refusal vocabulary only",
    },
    {
        "source_id": "LOC-PRESERVING-YOUR-BOOKS",
        "url": "https://guides.loc.gov/preserving-your-books",
        "status": "official Library of Congress research guide checked 2026-08-30",
        "use": "preventive care, storage, handling, support, and preservation-vacancy vocabulary only",
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
    "no real person, participant, book, codex, textblock, leaf, quire, board, joint, spine, endpaper, covering, thread, adhesive, tool, inscription, image, collection, site, measurement, sensor, treatment, custody event, release, or external action",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, detected effect, ultraviolet completion, quantum completion, or Theory-of-Everything claim",
    "no THOS operational-effectiveness, safety, professional-competence, deployment, AGI, or ASI claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, or trust-governance claim",
    "no repair, disbinding, rebinding, sewing, adhesion, cleaning, mould response, treatment, condition, authenticity, attribution, title, ownership, custody, loan, reproduction-right, legal, remedy, cultural, affected-party, taonga, tikanga, Māori-data-governance, or Māori-authority decision",
    "no accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness, personhood, proof, canon, or Stage 20 claim",
]

STARTUP_FAILURES = [
    (
        "TV6765-START-N001",
        "The first memory-registry lookup assumed the registry lived at the workspace root and returned no file.",
        "TV6765-START-P001",
        "The exact memory subdirectory was used and the bounded lifecycle references were recovered without repository change.",
    ),
    (
        "TV6765-START-N002",
        "The first complete Method Flow rendering exceeded the output window.",
        "TV6765-START-P002",
        "The immutable ledger was read through EOF in bounded line windows and its counts were retained.",
    ),
    (
        "TV6765-START-N003",
        "A combined Method Flow recovery still exceeded the display bound.",
        "TV6765-START-P003",
        "Smaller non-overlapping windows completed the read without changing the source.",
    ),
    (
        "TV6765-START-N004",
        "The first retained-negative two-part rendering truncated its middle section.",
        "TV6765-START-P004",
        "An exact missing-line recovery completed the immutable register read.",
    ),
    (
        "TV6765-START-N005",
        "A PowerShell metadata projection piped foreach output before materialization and failed at parse time.",
        "TV6765-START-P005",
        "The collection was materialized before piping and the exact metadata projection passed.",
    ),
    (
        "TV6765-START-N006",
        "One source-and-proposal ledger window truncated before the requested boundary.",
        "TV6765-START-P006",
        "The exact missing interval was reread and the source ledger reached EOF.",
    ),
    (
        "TV6765-START-N007",
        "The first authorization-state rendering exceeded the output window.",
        "TV6765-START-P007",
        "Bounded structured projections completed the stale snapshot read while newer live overlays retained precedence.",
    ),
    (
        "TV6765-START-N008",
        "A core-skill inventory repeated the foreach-before-pipe PowerShell parser fault.",
        "TV6765-START-P008",
        "Collection-first inventory recovered the exact current skill paths and sizes.",
    ),
    (
        "TV6765-START-N009",
        "A combined roster workflow and reflection rendering exceeded the shared output budget.",
        "TV6765-START-P009",
        "Separate complete skill reads and a structured roster parse recovered the required records.",
    ),
    (
        "TV6765-START-N010",
        "The first source equality wrapper emitted branch status but no attributable post-fetch payload.",
        "TV6765-START-P010",
        "Separate local topology scalars and one fresh live remote query proved exact equality.",
    ),
    (
        "TV6765-START-N011",
        "A second fetch-bound equality wrapper again returned no attributable summary.",
        "TV6765-START-P011",
        "No third fetch was attempted; the independent live remote scalar remained authoritative.",
    ),
    (
        "TV6765-START-N012",
        "The first inline manifest verifier had an unterminated byte literal and exited before checking any entry.",
        "TV6765-START-P012",
        "The byte-domain expression was corrected without repository mutation.",
    ),
    (
        "TV6765-START-N013",
        "The first canonical-receipt lookup assumed a nonexistent directory shape.",
        "TV6765-START-P013",
        "A bounded filename search located the exact Liora receipt and latch.",
    ),
    (
        "TV6765-START-N014",
        "The second manifest verifier lost backslashes in a native inline path argument and failed before entry checks.",
        "TV6765-START-P014",
        "Forward-slash repository paths removed the native quoting ambiguity.",
    ),
    (
        "TV6765-START-N015",
        "Two broad manifest parity projections exceeded their attribution windows and left owned read-only helpers running.",
        "TV6765-START-P015",
        "Exact process inspection stopped only those helpers and one batch-check plus batch-content verifier passed 1168 entries.",
    ),
    (
        "TV6765-START-N016",
        "The first prior-Tamar document lookup assumed a sparse checkout path was materialized.",
        "TV6765-START-P016",
        "An exact Git-tree read recovered the immutable prior packet without widening the source checkout.",
    ),
    (
        "TV6765-START-N017",
        "The first prior-Tamar script lookup repeated the sparse-materialization assumption.",
        "TV6765-START-P017",
        "Exact Git-tree names recovered the compatibility surfaces read-only.",
    ),
    (
        "TV6765-START-N018",
        "A proposal-theme probe repeated the foreach-before-pipe PowerShell parser fault.",
        "TV6765-START-P018",
        "The broad theme probe was abandoned in favour of the exact source-tree JSON novelty tribunal.",
    ),
    (
        "TV6765-START-N019",
        "A multi-term Git grep exceeded the output window and continued without an attributable result.",
        "TV6765-START-P019",
        "The exact owned grep process was stopped and the source-tree proposal audit became the sole novelty witness.",
    ),
    (
        "TV6765-START-N020",
        "The additive worktree creation wrapper timed out after reporting preparation while its owned Git process continued.",
        "TV6765-START-P020",
        "Persisted state and exact owned processes were inspected instead of repeating the mutation; the sparse lane completed cleanly.",
    ),
    (
        "TV6765-START-N021",
        "A bounded wait wrapper returned no completion payload while the same worktree operation was still active.",
        "TV6765-START-P021",
        "Subsequent process and index-lock inspection established completion without a duplicate worktree action.",
    ),
    (
        "TV6765-START-N022",
        "A PowerShell state projection used if as an inline expression and failed before inspection.",
        "TV6765-START-P022",
        "Preassigning the conditional value recovered the exact worktree pointer and sparse configuration.",
    ),
    (
        "TV6765-X1-N001",
        "The first planning builder failed closed because eleven draft titles met the inherited semantic-neighbor quarantine threshold, including four exact inherited titles; no packet artifact was written.",
        "TV6765-X1-P001",
        "A bounded exact-tree diagnostic identified only those eleven neighbors; their titles were replaced with distinct book-specific state contracts and the unchanged 0.75 tribunal was rerun without lowering any novelty gate.",
    ),
    (
        "TV6765-X1-N002",
        "The first post-build packet projection guessed semantic-novelty-audit.json and failed before inspecting the generated audit.",
        "TV6765-X1-P002",
        "An exact file listing exposed semantic-neighbor-audit.json; the bounded corrected projection then proved zero parse failures, zero quarantined rows, zero exact collisions, and maximum score 0.7143.",
    ),
    (
        "TV6765-X1-N003",
        "The first regeneration attempt was refused by the builder's clean-room guard because the earlier generated owner packet was still untracked.",
        "TV6765-X1-P003",
        "The exact seventeen-file Tamar-generated path set was verified, only those untracked outputs were removed, and regeneration resumed from the authored scripts-and-test-only state without touching inherited or user material.",
    ),
]

SKILLS = [
    "synthetic-codex-namespace",
    "textblock-gathering-topology",
    "quire-adjacency-guard",
    "sewing-support-vacancy-map",
    "board-joint-topology",
    "spine-lining-layer-order",
    "endpaper-pastedown-relation",
    "covering-material-vacancy",
    "thread-adhesive-claim-hold",
    "opening-angle-observation-vacancy",
    "foliation-provenance-firewall",
    "environment-zero-sensor-contract",
    "binding-intervention-separator",
    "rebinding-substitution-hold",
    "correction-readback-ledger",
    "binding-provenance-vacancy",
    "shelfmark-privacy-filter",
    "accessible-binding-summary",
    "workload-handover-guard",
    "taonga-authority-reservation",
]

RUNNERS = [
    "ghc_family_tamar_vey_v676_v5_proposal_contracts.py",
    "ghc_family_tamar_vey_v676_v5_positive_controls.py",
    "ghc_family_tamar_vey_v676_v5_mutation_rejector.py",
    "ghc_family_tamar_vey_v676_v5_bookbinding_topology.py",
    "ghc_family_tamar_vey_v676_v5_measurement_vacancy.py",
    "ghc_family_tamar_vey_v676_v5_provenance.py",
    "ghc_family_tamar_vey_v676_v5_privacy.py",
    "ghc_family_tamar_vey_v676_v5_accessibility.py",
    "ghc_family_tamar_vey_v676_v5_portfolio.py",
    "build_ghc_family_tamar_vey_v676_v5_report.py",
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
        proposal_id = f"TV6765-N{offset:03d}"
        if offset <= 28:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 36:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 38:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["CCI-BASIC-CARE-BOOKS", "LOC-PRESERVING-YOUR-BOOKS", "W3C-PROV-O", "RFC-8785"]
        if offset in {26, 27, 28, 29}:
            source_ids.append("WCAG-2.2")
        if offset in {23, 34, 35}:
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
        raise SystemExit("x1 builder requires the exact immutable Orin source head")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("x1 builder requires the exact Tamar owner branch")
    allowed_untracked = {
        "scripts/build_ghc_family_tamar_vey_v676_v5_x1.py",
        "scripts/ghc_family_tamar_vey_v676_v5_x1_manifest.py",
        "tests/test_ghc_family_tamar_vey_v676_v5_x1.py",
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
                "orin_v676_v3_final_and_liora_source": LIORA_SOURCE,
                "liora_x1": LIORA_X1,
                "liora_evidence": LIORA_EVIDENCE,
                "liora_final": LIORA_FINAL,
            },
            "source_to_final_phase_commits": 3,
            "source_to_final_merges": 0,
            "source_clean_zero_divergent_and_fresh_four_way_equal": True,
            "liora_canonical_receipt_sha256": LIORA_CANONICAL_RECEIPT_SHA256,
            "liora_canonical_payload_sha256": LIORA_CANONICAL_PAYLOAD_SHA256,
            "inherited_canonical_replayed": False,
            "verified_date": GENERATED_DATE,
        },
    )
    dump(
        base / "new-proposal-freeze.json",
        {
            "status": "FROZEN_PLANNING_ONLY",
            "declared_chain_before": ACTIVATION["declared_proposals"],
            "new_tamar_proposals": len(rows),
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
            "safe_now": planned_rows("TV6765-SAFE", 60, "planned_unexecuted_x1"),
            "candidate": planned_rows("TV6765-CAND", 30, "planned_unexecuted_x1"),
            "exact_approval": planned_rows("TV6765-EXACT", 20, "unexecuted_exact_gate"),
            "blocked": planned_rows("TV6765-BLOCK", 10, "blocked_unexecuted"),
            "caps_are_ceilings_not_quotas": True,
        },
    )
    dump(
        base / "skill-runner-plan.json",
        {
            "phase_local_skills": [
                {
                    "skill_id": f"TV6765-SKILL-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                    "global_install": False,
                }
                for index, name in enumerate(SKILLS, start=1)
            ],
            "family_current_runners": [
                {
                    "runner_id": f"TV6765-RUNNER-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                }
                for index, name in enumerate(RUNNERS, start=1)
            ],
            "successor_skill_recommendations": [
                {
                    "recommendation_id": f"TV6765-ELOWEN-SKILL-{index:02d}",
                    "seed": name,
                    "credit": "zero_tamar_completion_credit",
                }
                for index, name in enumerate(SKILLS[:10], start=1)
            ],
            "successor_runner_recommendations": [
                {
                    "recommendation_id": f"TV6765-ELOWEN-RUNNER-{index:02d}",
                    "seed": name,
                    "credit": "zero_tamar_completion_credit",
                }
                for index, name in enumerate(RUNNERS, start=1)
            ],
        },
    )
    dump(
        base / "clean-fix-refine-plan.json",
        {
            "owner_tasks": planned_rows("TV6765-CFR", 60, "planned_unexecuted_x1"),
            "successor_recommendations": [
                {
                    "recommendation_id": f"TV6765-ELOWEN-CFR-{index:03d}",
                    "description": f"Distinct zero-credit successor CLEAN/FIX/REFINE seed {index:03d}",
                    "credit": "zero_tamar_completion_credit",
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
                    "recommendation_id": f"TV6765-SUCC-SEED-{index:03d}",
                    "description": f"Bounded successor seed {index:03d}; no Tamar execution or completion credit",
                    "credit": "zero_tamar_completion_credit",
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
            "primary_pillar": "THOS Body",
            "secondary_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
            "bounded_wholly_synthetic_learning_lenses": [
                "book-conservation intake registrar for synthetic zero-object records",
                "binding-structure documentation analyst for synthetic codex topology",
                "accessible collection-handover steward for synthetic correction and workload records",
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
            "route_state": "HOLD_UNTIL_TAMAR_V676_V5_EXACT_FINAL",
            "successor_inferred": False,
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
        """# Tamar Vey v676-v5 identity and authority boundary

Tamar Vey, optionally she/they, is relational working language only. The phase role is **evidence-and-recovery steward**, with the hope of keeping failures visible, corrections reversible, and every authority vacancy explicit.

This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no empirical result here. THOS remains synthetic proxy evidence without real participants, operators, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction with zero real keys, proofs, lifecycle events, or trust governance. CBR, ownership, repair, treatment, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, tikanga, taonga, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities.
""",
    )
    text(
        base / "x1-overview.md",
        f"""# Tamar Vey {PHASE} planning-only x1 overview

This x1 freezes forty bounded proposal contracts against the declared 7,550-row chain and every proposal-bearing JSON artifact reachable at Liora's exact final `{SOURCE}`. Twenty inherited neighbors are reviewed at zero novelty and completion credit. Four invalid mutations per proposal are preregistered but unexecuted.

The primary pillar is THOS Body through wholly synthetic book-conservation intake, binding-structure documentation, and accessible collection-handover lenses. GMUT Mind and Freed ID/CBR Heart remain visible and protected. There are zero real people, books, textblocks, gatherings, boards, bindings, measurements, sensors, tools, treatments, identity events, external actions, or authority decisions.

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

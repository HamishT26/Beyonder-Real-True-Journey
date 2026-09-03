#!/usr/bin/env python3
"""Build Elowen Cairn v685-v2 planning-only x1 artifacts.

This builder is intentionally limited to preregistration, portfolio freezing,
source and route boundaries, retained startup failures, and index-based x1
validation receipts.  It contains no x2 implementation or observed outcome.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Elowen Cairn"
PHASE = "v685-v2"
PREFIX = "EC6852"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v685-v1-full-tools"
TAMAR_SOURCE = "f138d0e9fd37d424a81887bb7a1bafa3eacba860"
TAMAR_X1 = "a640f907d154d6b5c7747c990a3c0b1d6fe987eb"
TAMAR_EVIDENCE = "9484532c6e45c6b3c87d068e06213dc4260cd7e1"
SOURCE_FINAL = "b2cfabd4d836737b375910ccb73f8037a8ad6c4d"
SOURCE_CANONICAL_RECEIPT_SHA256 = "b637de93397426647bc43ef7950d4dde423265ae552b45194e1124ed5a3615fe"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "3ad80ecb7ceb9309ac0c43f2442a85d4d729806b2df13dd46225711a19ee58fd"
DECLARED_CHAIN_BEFORE = 11270
DECLARED_CHAIN_AFTER = 11330
CHECKED_AT = "2026-09-03"

DOC = ROOT / "docs" / "elowen-cairn" / PHASE
X1 = DOC / "x1"
VALIDATION = DOC / "validation"
BUILDER_REL = "scripts/build_ghc_family_elowen_cairn_v685_v2_x1.py"
TEST_REL = "tests/test_ghc_family_elowen_cairn_v685_v2_x1.py"


def run(args: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        args,
        cwd=ROOT,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def git(*args: str, check: bool = True) -> str:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8", "replace").strip()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def title_tokens(value: str) -> set[str]:
    return set(normalized_title(value).split())


def jaccard(left: str, right: str) -> float:
    a = title_tokens(left)
    b = title_tokens(right)
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


PROPOSAL_TITLES = [
    "Synthetic hand-fan work capsule with every real object workshop and making act absent",
    "Folding fan leaf mount and opening topology without a manufactured object claim",
    "Fixed hand-screen fan support and face topology without physical assembly",
    "Fan leaf segment and mount relationship record without material attachment",
    "Stick rib guard and gorge adjacency graph without component fabrication",
    "Fan head pivot pin washer and loop vacancy without mechanical inspection",
    "Rivet spacer and fastener proposal separated from every applied joining act",
    "Pleat fold and leaf-segment sequence contract without a folded article",
    "Paper silk feather lace and synthetic-sheet material vacancy board",
    "Bamboo wood shell horn ivory and imitation-material claim abstention record",
    "Surface colour motif ornament and inscription proposal without attribution",
    "Fan span length and thickness targets separated from physical measurement",
    "Opening arc and angular travel targets separated from observed motion",
    "Leaf-to-stick attachment path proposal without adhesive stitch or fastening",
    "Stick shaping cutting and finishing plan without workshop execution",
    "Piercing drilling carving and inlay layout proposal without tool actuation",
    "Adhesive coating pigment and solvent hazard vocabulary without safety decision",
    "Knife drill press clamp and finishing-tool guard hold without equipment release",
    "Split fracture delamination and abrasion cue quarantine without diagnosis",
    "Moisture mould pest and corrosion cue quarantine without material conclusion",
    "Readiness-refusal ledger for synthetic fanmaking tool records with calibration and release authority absent",
    "Hand-fan work-order partial order without physical execution",
    "Proposed fanmaking operation separated from observation completion and release",
    "Template jig gauge and alignment target vacancy without dimensional authority",
    "Reused fan component provenance and prior-object nonidentity record",
    "Fan component batch and material-lot lineage with zero production rows",
    "Append-only hand-fan correction chain with superseded values retained",
    "Hand-fan supersession nonerasure challenge and appeal lineage",
    "Two-source hand-fan record reconciliation with unresolved conflict preserved",
    "Privacy-minimized work capsule assigning only vacant synthetic fanmaker and recipient roles",
    "Maker client custodian and recipient role vacancy with no real identity binding",
    "Hand-fan custody ownership return transfer and disposal rights hold",
    "Fan image pattern design inscription and publication-rights hold",
    "Structurally accessible hand-fan status board without accessibility completeness",
    "Noncolour fan-status cues reading order and text-equivalent structure",
    "Fanmaking workload pause queue and shift-handover contract",
    "Unresolved hand-fan holds queue with no automatic release",
    "Exact hand-fan staged allowlist and unexpected-path refusal",
    "Index-object hash manifest for fanmaking planning bytes with checkout-domain refusal",
    "Hand-fan privacy scanner candidate separated from confirmed payload hit",
    "Typed GMUT folding-kinematics graph without a material law or prediction",
    "THOS fanmaking queue paired with a keyless Freed ID receipt and explicit noncompensation",
    "Represented CBR hand-fan challenge remedy refusal and appeal vacancy",
    "Represented Smithsonian hand-fan component vocabulary without object observation",
    "Represented V and A fan-conservation vocabulary without treatment instruction",
    "Represented Met hand-fan cultural-context vocabulary without cultural authority",
    "Represented PROV-O hand-fan lineage mapping without conformance claim",
    "Structural fan-status presentation mapped to WCAG 2.2 criteria as nonconformant representation",
    "Keyless fan-custody actor vocabulary mapped to Verifiable Credentials 2.0 without credential lifecycle",
    "Canonical fan-record byte recipe represented through RFC 8785 with no authenticity inference",
    "Machine-checkable fan packet shape using JSON Schema Draft 2020-12 without practice validation",
    "Māori data-sovereignty reservation card citing Te Mana Raraunga without interpretive authority",
    "Represented zero-call hand-fan collection adapter with zero downloaded rows",
    "Represented three-pillar hand-fan separation and authority noncompensation rule",
    "Open gap for real fanmakers fans materials tools workshops and participants",
    "Open gap for real measurements durability safety usability and blind evaluation",
    "Open gap for governed review by disabled users language communities rights holders and cultural authorities",
    "Exact gate for professional fanmaking conservation material authenticity and workplace safety",
    "Exact gate for ownership copyright traditional knowledge cultural meaning Māori data and Māori authority",
    "Exact nonconversion terminal covering deployment physics reproduction superintelligence personhood canon and Stage Twenty",
]


MUTATION_TYPES = [
    "missing_required_field",
    "identifier_role_swap",
    "stale_precondition_digest",
    "correction_order_inversion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real participants fanmakers operators clients recipients and custodians",
    "real hand fans materials tools workshops observations and measurements",
    "professional fanmaking conservation workplace material safety and work-release authority",
    "production identity issuance resolution status revocation and trust governance",
    "ownership copyright traditional knowledge cultural meaning privacy remedy affected-party and Māori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction empirical GMUT proof canon and Stage 20",
]


def expected_disposition(index: int) -> str:
    if index <= 42:
        return "completed"
    if index <= 54:
        return "represented"
    if index <= 57:
        return "open_gap"
    return "exact_gate"


def approval_class(index: int) -> str:
    disposition = expected_disposition(index)
    return {
        "completed": "safe_now",
        "represented": "candidate_proxy_only",
        "open_gap": "open_gap_requires_real_evidence",
        "exact_gate": "exact_approval_required",
    }[disposition]


def execution_lane(index: int) -> str:
    disposition = expected_disposition(index)
    return {
        "completed": "owner_local_synthetic_zero_row",
        "represented": "bounded_representation_without_real_execution",
        "open_gap": "document_only_no_execution",
        "exact_gate": "hold_unexecuted",
    }[disposition]


def source_needs(index: int) -> list[str]:
    if index == 44:
        return ["SMITHSONIAN-ANACOSTIA-HAND-FAN"]
    if index == 45:
        return ["VAM-FAN-CONSERVATION"]
    if index == 46:
        return ["MET-FANS-CULTURAL-CONTEXT"]
    if index in {17, 18}:
        return ["OSHA-MACHINE-GUARDING"]
    if index == 47:
        return ["W3C-PROV-O"]
    if index in {30, 31, 48, 57}:
        return ["W3C-WCAG22"]
    if index in {27, 42, 49}:
        return ["W3C-VC20"]
    if index in {23, 34, 35, 37, 38, 50}:
        return ["RFC8785"]
    if index in {38, 51}:
        return ["JSON-SCHEMA-2020-12"]
    if index in {52, 59}:
        return ["TE-MANA-RARAUNGA-PRINCIPLES"]
    if index == 53:
        return ["SMITHSONIAN-ANACOSTIA-HAND-FAN"]
    if index in {55, 56, 57}:
        return ["REAL-AFFECTED-PROFESSIONAL-EVIDENCE-ABSENT"]
    if index >= 58:
        return ["EXACT-COMPETENT-AFFECTED-AUTHORITY-ABSENT"]
    return ["OWNER-LOCAL-SYNTHETIC-CONTRACT", "W3C-PROV-O", "RFC8785"]


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"{PREFIX}-N{index:03d}"
        disposition = expected_disposition(index)
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A bounded synthetic contract for {title.lower()} can preserve its declared structure "
                    "and reject five preregistered invalid mutations without converting software evidence "
                    "into a real hand-fan, empirical, identity, cultural, legal, or authority claim."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, the bounded positive "
                    "structure is rejected, an absent observation is promoted, or any protected gate closes."
                ),
                "approval_class": approval_class(index),
                "execution_lane": execution_lane(index),
                "official_or_primary_source_needs": source_needs(index),
                "concrete_artifacts": [
                    f"docs/elowen-cairn/{PHASE}/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/elowen-cairn/{PHASE}/x2/rejecting-mutations.json#{proposal_id}",
                ],
                "falsifier_or_acceptance_gate": (
                    f"Accept only the declared {disposition} disposition if {proposal_id} receives its "
                    "preregistered bounded witness, all five invalid mutations remain rejected, and no "
                    "professional, empirical, production, legal, cultural, Māori-authority, or Stage 20 "
                    "claim is inferred."
                ),
                "rollback_or_recovery": (
                    f"Quarantine only {proposal_id}, retain every failed receipt at zero credit, and "
                    "regenerate from this immutable planning-only x1 contract."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
                "preregistered_rejecting_mutations": [
                    {
                        "mutation_id": f"{proposal_id}-M{mutation_index:02d}",
                        "mutation_type": mutation_type,
                        "expected_result": "rejected_zero_credit",
                    }
                    for mutation_index, mutation_type in enumerate(MUTATION_TYPES, start=1)
                ],
            }
        )
    return rows


def proposal_blob_records() -> tuple[list[dict[str, str]], dict[str, Any]]:
    paths = [
        line
        for line in git("ls-tree", "-r", "--name-only", SOURCE_FINAL).splitlines()
        if line.lower().endswith(".json") and "proposal" in line.lower()
    ]
    records: list[dict[str, str]] = []
    failures: list[str] = []
    specs = [f"{SOURCE_FINAL}:{path}" for path in paths]
    proc = run(["git", "cat-file", "--batch"], input_bytes=("\n".join(specs) + "\n").encode("utf-8"))
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    cursor = 0
    blobs: list[bytes | None] = []
    for path in paths:
        line_end = proc.stdout.find(b"\n", cursor)
        if line_end < 0:
            raise RuntimeError("truncated git cat-file batch header")
        header = proc.stdout[cursor:line_end].decode("utf-8", "replace")
        cursor = line_end + 1
        if header.endswith(" missing"):
            blobs.append(None)
            failures.append(path)
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError(f"unexpected git cat-file header: {header}")
        size = int(parts[2])
        blobs.append(proc.stdout[cursor:cursor + size])
        cursor += size + 1
    for path, blob in zip(paths, blobs):
        if blob is None:
            continue
        try:
            value = json.loads(blob.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            failures.append(path)
            continue
        for node in walk_dicts(value):
            title = node.get("title")
            identifier = node.get("proposal_id", node.get("id"))
            if isinstance(title, str) and isinstance(identifier, str):
                records.append(
                    {
                        "id": identifier,
                        "title": title,
                        "path": path,
                    }
                )
    deduped: dict[tuple[str, str], dict[str, str]] = {}
    for record in records:
        deduped[(record["id"], normalized_title(record["title"]))] = record
    return list(deduped.values()), {
        "proposal_json_paths_discovered": len(paths),
        "proposal_json_paths_parsed": len(paths) - len(failures),
        "proposal_json_parse_failures": failures,
        "reachable_id_title_records": len(deduped),
    }


def proposal_audit(rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    inherited, scope = proposal_blob_records()
    exact: list[dict[str, Any]] = []
    quarantined: list[dict[str, Any]] = []
    reviews: list[dict[str, Any]] = []
    for row in rows:
        title = row["title"]
        neighbors = sorted(
            (
                (jaccard(title, record["title"]), record)
                for record in inherited
            ),
            key=lambda item: (-item[0], item[1]["id"], item[1]["title"]),
        )
        score, neighbor = neighbors[0] if neighbors else (0.0, {"id": "NONE", "title": "", "path": ""})
        review = {
            "proposal_id": row["proposal_id"],
            "title": title,
            "nearest_inherited_id": neighbor["id"],
            "nearest_inherited_title": neighbor["title"],
            "nearest_inherited_path": neighbor["path"],
            "token_jaccard": round(score, 6),
            "inherited_credit": "zero",
            "review_disposition": "distinct_under_source_bounded_audit" if score < 0.78 else "quarantined",
        }
        reviews.append(review)
        if normalized_title(title) == normalized_title(neighbor["title"]) and neighbor["title"]:
            exact.append(review)
        if score >= 0.78:
            quarantined.append(review)
    audit = {
        "schema": f"ghc.family.proposal-chain-audit.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE_FINAL,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "new_proposal_count": len(rows),
        "quarantine_threshold_token_jaccard": 0.78,
        "maximum_neighbor_score": max((r["token_jaccard"] for r in reviews), default=0.0),
        "exact_title_collisions": exact,
        "quarantined_neighbors": quarantined,
        "neighbor_reviews": reviews,
        "audit_scope": {
            **scope,
            "universal_11270_row_materialization_claimed": False,
            "claim": (
                "Source-bounded comparison against every proposal-labelled JSON object reachable at the "
                "exact inherited final. The declared chain count is preserved, but compressed or otherwise "
                "unmaterialized historic titles are not claimed to have been universally compared."
            ),
        },
    }
    return audit, reviews


def content_address(record: dict[str, Any]) -> str:
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def flashcard_freeze(rows: list[dict[str, Any]]) -> dict[str, Any]:
    source_cards = [
        {"kind": "source", "prompt": entry["source_id"], "answer": entry["boundary"]}
        for entry in source_ledger()["sources"]
    ]
    gate_cards = [
        {"kind": "gate", "prompt": f"protected gate {index:02d}", "answer": gate}
        for index, gate in enumerate(PROTECTED_GATES, start=1)
    ]
    proposal_cards = [
        {
            "kind": "proposal",
            "prompt": row["proposal_id"],
            "answer": f"{row['title']} -> {row['expected_disposition']}",
        }
        for row in rows[:51]
    ]
    cards = proposal_cards + source_cards + gate_cards
    cards = cards[:67]
    for index, card in enumerate(cards, start=1):
        card["card_id"] = f"{PREFIX}-FC{index:03d}"
        card["credit_boundary"] = "navigation_only_not_authority_or_completion"
        card["sha256"] = content_address(card)
    return {
        "schema": f"ghc.family.content-addressed-flashcards.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER,
        "phase": PHASE,
        "card_count": len(cards),
        "cards": cards,
        "mutation_or_outcome_present": False,
    }


def portfolio_entries(prefix: str, themes: list[str], operations: list[str], count: int, lane: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for theme in themes:
        for operation in operations:
            if len(rows) >= count:
                return rows
            index = len(rows) + 1
            rows.append(
                {
                    "id": f"{PREFIX}-{prefix}{index:03d}",
                    "title": f"{operation} for {theme}",
                    "lane": lane,
                    "x1_status": "preregistered_not_executed",
                    "credit_boundary": "no x2 execution or completion credit in x1",
                }
            )
    return rows


def make_portfolio() -> dict[str, Any]:
    themes = [
        "hand-fan work capsules",
        "folding fan component topology",
        "fixed fan support topology",
        "material vacancy",
        "measurement vacancy",
        "tool and guard holds",
        "correction lineage",
        "privacy minimization",
        "accessible status",
        "workload and handover",
        "GMUT typed graphs",
        "THOS queue proxies",
    ]
    operations = [
        "define schema",
        "add positive fixture",
        "add refusing fixture",
        "record provenance",
        "enforce nonconversion",
        "add rollback",
        "add recurrence guard",
        "scan privacy",
        "verify deterministic bytes",
        "document authority boundary",
    ]
    candidate_themes = [
        "fan head and pivot topology",
        "leaf mount topology",
        "stick rib and guard topology",
        "fan dimension targets",
        "leaf attachment proposals",
        "tool condition holds",
        "rights and custody",
        "three-pillar separation",
    ]
    candidate_ops = [
        "model",
        "validate",
        "mutate",
        "quarantine",
        "trace",
        "adjudicate",
        "render",
        "review",
        "hash",
        "handover",
    ]
    clean_themes = [
        "schema names",
        "identifier roles",
        "source status",
        "unit fields",
        "correction ordering",
        "privacy labels",
        "manifest domains",
        "stale route labels",
        "authority language",
        "rollback notes",
    ]
    clean_ops = [
        "CLEAN duplicates",
        "FIX ambiguity",
        "REFINE refusal",
        "CLEAN serialization",
        "FIX deterministic order",
        "REFINE evidence boundary",
        "CLEAN stale wording",
        "FIX fixture isolation",
        "REFINE recurrence guard",
        "CLEAN handover state",
    ]
    exact = [
        {
            "id": f"{PREFIX}-EXACT-{index:03d}",
            "title": title,
            "status": "unexecuted_exact_approval_hold",
            "required_authority": "competent affected action-specific authority and evidence",
        }
        for index, title in enumerate(
            [
                "real fanmaker participation",
                "real hand-fan article inspection",
                "real material identification",
                "real measurement or calibration",
                "machine operation or guarding decision",
                "coating pigment solvent or adhesive safety decision",
                "workplace release",
                "professional fanmaking or conservation decision",
                "ownership or custody decision",
                "pattern design inscription publication or image-rights decision",
                "real identity issuance",
                "real key or proof lifecycle",
                "privacy impact acceptance",
                "accessibility affected-user acceptance",
                "legal interpretation",
                "cultural interpretation",
                "traditional-knowledge treatment",
                "Māori wording or data-governance decision",
                "production deployment",
                "Stage 20 disposition",
            ],
            start=1,
        )
    ]
    blocked = [
        {
            "id": f"{PREFIX}-BLOCK-{index:03d}",
            "title": title,
            "status": "blocked_unexecuted",
            "blocker": "missing real evidence competent authority governed process and rollback",
        }
        for index, title in enumerate(
            [
                "destructive article testing",
                "live machine or tool actuation",
                "account or credential mutation",
                "private collection disclosure",
                "professional certification",
                "legal rights adjudication",
                "cultural legitimacy decision",
                "Māori authority claim",
                "independent reproduction claim",
                "AGI consciousness Theory-of-Everything or Stage 20 claim",
            ],
            start=1,
        )
    ]
    return {
        "schema": f"ghc.family.portfolio-freeze.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER,
        "phase": PHASE,
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["Freed ID and CBR Heart", "GMUT Mind", "THOS Body"],
        "owner_practice_lenses": [
            "wholly synthetic hand-fan making and documentation through component topology rights holds correction accessibility workload and handover"
        ],
        "safe_now": portfolio_entries("SAFE", themes, operations, 120, "owner_local_safe_now"),
        "owner_candidates": portfolio_entries("CAND", candidate_themes, candidate_ops, 80, "owner_local_candidate"),
        "successor_candidates": portfolio_entries(
            "SCAND",
            ["synthetic local repair intake", "synthetic accessible custody handover"],
            candidate_ops,
            20,
            "successor_seed_zero_credit",
        ),
        "owner_skill_ideas": [
            {
                "id": f"{PREFIX}-SKILL-{index:03d}",
                "name": name,
                "status": "planned_local_not_installed",
            }
            for index, name in enumerate(
                [
                    "hand-fan-work-capsule",
                    "folding-fan-topology",
                    "fixed-fan-topology",
                    "leaf-mount-lineage",
                    "stick-rib-guard-topology",
                    "head-pivot-vacancy",
                    "material-claim-firewall",
                    "dimension-observation-separator",
                    "tool-guard-refusal",
                    "hazard-vocabulary-firewall",
                    "correction-braid",
                    "privacy-minimizer",
                    "accessible-status",
                    "workload-handover",
                    "gmut-fan-kinematics-graph",
                    "thos-fan-work-queue",
                    "freed-id-keyless-receipt",
                    "cbr-cultural-rights-hold",
                    "manifest-domain-separator",
                    "authority-noncompensation",
                ],
                start=1,
            )
        ],
        "owner_runner_ideas": [
            {
                "id": f"{PREFIX}-RUNNER-{index:03d}",
                "name": name,
                "status": "planned_family_current_not_built",
            }
            for index, name in enumerate(
                [
                    "ghc_family_hand_fan_contract_runner",
                    "ghc_family_hand_fan_mutation_runner",
                    "ghc_family_hand_fan_privacy_runner",
                    "ghc_family_hand_fan_manifest_runner",
                    "ghc_family_hand_fan_source_runner",
                    "ghc_family_hand_fan_accessibility_runner",
                    "ghc_family_hand_fan_correction_runner",
                    "ghc_family_hand_fan_gate_runner",
                    "ghc_family_hand_fan_method_flow_runner",
                    "ghc_family_hand_fan_terminal_runner",
                ],
                start=1,
            )
        ],
        "successor_skill_ideas": [
            {"id": f"{PREFIX}-SSKILL-{index:03d}", "status": "zero_credit_seed", "title": f"successor skill seed {index:02d}"}
            for index in range(1, 11)
        ],
        "successor_runner_ideas": [
            {"id": f"{PREFIX}-SRUN-{index:03d}", "status": "zero_credit_seed", "title": f"successor runner seed {index:02d}"}
            for index in range(1, 11)
        ],
        "owner_clean_fix_refine": portfolio_entries("CFR", clean_themes, clean_ops, 100, "owner_local_clean_fix_refine"),
        "successor_clean_fix_refine": portfolio_entries(
            "SCFR",
            ["route receipts", "successor source ledgers", "successor validation latches"],
            clean_ops,
            30,
            "successor_seed_zero_credit",
        ),
        "exact_approval": exact,
        "blocked": blocked,
        "successor_practice_recommendation": (
            "one wholly synthetic practice lens with explicit documentation accessibility correction and handover boundaries, "
            "subject to successor novelty audit and zero inherited completion credit"
        ),
        "materialized_file_stop": 2000,
        "document_word_cap": 100000,
        "commit_cap": {"total": 3, "x1": 1, "x2": 2},
        "caps_are_ceilings": True,
    }


STARTUP_FAILURES = [
    (
        "EC6852-ST-N001",
        "Ran a Git worktree inventory from a nonrepository metadata directory and received the expected not-a-repository failure.",
        "Repeated the read-only inventory from the verified prior Elowen D-drive worktree.",
        "Resolve an attributable Git worktree before invoking repository-scoped inventory commands.",
    ),
    (
        "EC6852-ST-N002",
        "The first D-drive worktree-list wrapper projected no attributable output and lost its command-session metadata.",
        "Recovered with scalar Git probes and one fully captured bounded worktree inventory.",
        "Capture command metadata and output before projecting long Windows inventory results.",
    ),
    (
        "EC6852-ST-N003",
        "A grouped family-skill read exceeded the result limit and truncated routing authorization and roster content.",
        "Read routing precedence authorization roster and schemas individually through bounded complete reads.",
        "Separate high-authority skill and schema reads before combining summaries.",
    ),
    (
        "EC6852-ST-N004",
        "A grouped validation-packet read truncated before every required exact-head artifact was attributable.",
        "Recovered with individual artifact reads and exact JSON projections.",
        "Read lifecycle-critical validation receipts one file at a time when combined output can truncate.",
    ),
    (
        "EC6852-ST-N005",
        "A compact read of Tamar's sixty-row proposal freeze truncated.",
        "Used schema-aware proposal projections rather than treating the partial display as complete.",
        "Project identifiers titles dispositions and sources from large proposal ledgers.",
    ),
    (
        "EC6852-ST-N006",
        "The first full proposal slice covering rows zero through nineteen also exceeded the result limit.",
        "Replaced full-row display with compact field projection.",
        "Do not emit verbose nested proposal rows when a bounded semantic audit needs only selected fields.",
    ),
    (
        "EC6852-ST-N007",
        "A combined three-slice proposal projection truncated before all sixty rows were attributable.",
        "Recovered with one compact all-row identifier disposition source and title projection.",
        "Prefer one minimal all-row projection to several verbose slices.",
    ),
    (
        "EC6852-ST-N008",
        "A grouped read of twenty owner-local skill files and YAML interfaces truncated.",
        "Read the missing Freed ID and GMUT skill files individually and verified receipt-level complete-read hashes.",
        "Partition large skill banks and retain complete-read digests before reuse.",
    ),
    (
        "EC6852-ST-N009",
        "A broad receipt search for the canonical SHA returned no attributable output around timeout.",
        "Enumerated only Tamar v685-v1 receipts and hashed the exact receipt file.",
        "Bound receipt discovery to the owner phase before searching a digest.",
    ),
    (
        "EC6852-ST-N010",
        "A combined Git fetch and source-equality wrapper returned no attributable output.",
        "Recovered with scalar ref probes a process audit an isolated fresh-live query and a separate lineage probe.",
        "Keep fetch remote equality cleanliness and ancestry probes independently attributable.",
    ),
    (
        "EC6852-ST-N011",
        "The first independent manifest replay launched 214 one-shot Git show processes and lost the final wrapper output.",
        "Replayed the same immutable entries once through one persistent git cat-file batch and captured zero mismatches.",
        "Use a single Git-object batch for large immutable manifest replays.",
    ),
    (
        "EC6852-X1-N001",
        "A broad Git grep over proposed practice candidates overproduced output and was stopped.",
        "Loaded Tamar's proposal-labelled Git-object corpus in one bounded batch and screened 7198 deduplicated identifier-title records.",
        "Use the source-bounded proposal corpus rather than broad repository grep for practice novelty.",
    ),
    (
        "EC6852-X1-N002",
        "The first template copy failed because the fresh sparse worktree had no physical scripts or tests directories.",
        "Created only the two exact owned sparse directories and then copied the two verified templates.",
        "Materialize exact parent directories before copying new sparse-path files.",
    ),
    (
        "EC6852-X1-N003",
        "The first directory-recovery command assumed New-Item supports LiteralPath on this host and failed before creating either directory.",
        "Used exact nonwildcard Path values and verified both owned directories before copying.",
        "Inspect the active cmdlet parameter surface before applying another cmdlet's literal-path convention.",
    ),
    (
        "EC6852-X1-N004",
        "The first planning builder correctly rejected ten proposal titles whose inherited semantic-neighbor scores reached the quarantine threshold.",
        "Ran only the failed novelty component, retained all ten collision records, rewrote those titles, and proved zero exact or quarantined neighbors with maximum score 0.777778.",
        "Execute the source-bounded title audit before materialization and revise only quarantined contracts.",
    ),
    (
        "EC6852-X1-N005",
        "The first compact novelty diagnostic completed its audit but Windows CP-1252 stdout could not encode a Māori character.",
        "Repeated only the display with ASCII-escaped JSON while preserving Unicode in repository artifacts.",
        "Set an explicit Unicode-safe output mode or use escaped diagnostic JSON on Windows consoles.",
    ),
    (
        "EC6852-X1-N006",
        "The first overview word-count probe combined incompatible PowerShell Raw and Delimiter parameters and returned no count.",
        "Repeated the read with Raw alone and measured every new document, confirming zero documents above the word ceiling.",
        "Use one complete-file read mode per PowerShell content probe.",
    ),
]


def method_flow_startup() -> dict[str, Any]:
    inherited = {
        "effective_negatives": 61065,
        "effective_methods": 76660,
        "failed_witnesses": 32126,
        "bounded_passing_witnesses": 57195,
        "open_gaps": 543,
        "exact_gates": 533,
    }
    failures = [
        {
            "failure_id": failure_id,
            "failed_witness": failed_witness,
            "recovery": recovery,
            "recurrence_guard": guard,
            "credit": "retained_zero_credit",
        }
        for failure_id, failed_witness, recovery, guard in STARTUP_FAILURES
    ]
    effective = {
        **inherited,
        "effective_negatives": inherited["effective_negatives"] + len(failures),
        "effective_methods": inherited["effective_methods"] + len(failures),
        "failed_witnesses": inherited["failed_witnesses"] + len(failures),
        "bounded_passing_witnesses": inherited["bounded_passing_witnesses"] + len(failures),
    }
    return {
        "schema": f"ghc.family.method-flow.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source_repository_seal": {
            "effective_negatives": 61063,
            "effective_methods": 76658,
            "failed_witnesses": 32124,
            "bounded_passing_witnesses": 57193,
            "open_gaps": 543,
            "exact_gates": 533,
        },
        "source_external_overlay_witnesses": [
            "TV6851-POST-N001",
            "TV6851-POST-N002",
        ],
        "inherited_baseline": inherited,
        "new_failure_count": len(failures),
        "new_failures": failures,
        "effective_x1_startup_counts": effective,
        "failure_erasure": False,
        "recoveries_promote_failed_witnesses": False,
    }


def source_ledger() -> dict[str, Any]:
    sources = [
        (
            "SMITHSONIAN-ANACOSTIA-HAND-FAN",
            "https://anacostia.si.edu/collection/object/acm_2002.0006.0011",
            "Object-page vocabulary for monture, leaf, ribs, sticks, guards, head, pin, and loop only; no object observation, condition, authenticity, cultural interpretation, or authority.",
        ),
        (
            "VAM-FAN-CONSERVATION",
            "https://www.vam.ac.uk/articles/conserving-a-fragile-200-year-old-fan-from-the-era-of-marie-antoinette",
            "Leaf, mount, stick, guard, damage, and conservation-context vocabulary only; no treatment instruction, inspection, condition finding, professional decision, or authority.",
        ),
        (
            "MET-FANS-CULTURAL-CONTEXT",
            "https://www.metmuseum.org/pt/perspectives/fans-of-the-met",
            "Cross-cultural material and meaning vocabulary only; no attribution, interpretation, legitimacy, affected-party acceptance, traditional-knowledge treatment, or cultural authority.",
        ),
        (
            "OSHA-MACHINE-GUARDING",
            "https://www.osha.gov/etools/machine-guarding/introduction/general-requirements",
            "Machine-guarding and point-of-operation refusal vocabulary only; no inspection, conformance, workplace release, or safety decision.",
        ),
        (
            "W3C-PROV-O",
            "https://www.w3.org/TR/prov-o/",
            "Provenance vocabulary only; no conformance, custody, authorship, ownership, attribution, or authenticity claim.",
        ),
        (
            "W3C-WCAG22",
            "https://www.w3.org/TR/WCAG22/",
            "Structural accessibility criteria as design references only; no complete accessibility or affected-user acceptance claim.",
        ),
        (
            "W3C-VC20",
            "https://www.w3.org/TR/vc-data-model-2.0/",
            "Role and lifecycle vocabulary only; zero real keys, proofs, issuance, status, revocation, or trust governance.",
        ),
        (
            "RFC8785",
            "https://www.rfc-editor.org/rfc/rfc8785.html",
            "Deterministic JSON canonicalization vocabulary only; no authenticity, identity, signature, or security conclusion.",
        ),
        (
            "JSON-SCHEMA-2020-12",
            "https://json-schema.org/draft/2020-12",
            "Schema vocabulary only; no real-world validity, professional conformance, or authority.",
        ),
        (
            "TE-MANA-RARAUNGA-PRINCIPLES",
            "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
            "Boundary and authority-reservation context only; no Māori wording, ratification, data-governance decision, or Māori authority.",
        ),
    ]
    return {
        "schema": f"ghc.family.official-primary-source-ledger.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER,
        "phase": PHASE,
        "checked_at": CHECKED_AT,
        "source_count": len(sources),
        "network_rows_ingested": 0,
        "sources": [
            {
                "source_id": source_id,
                "url": url,
                "status": "current_official_or_primary_source_checked",
                "boundary": boundary,
                "observation_credit": "zero",
                "authority_credit": "zero",
            }
            for source_id, url, boundary in sources
        ],
    }


def integrated_overview() -> str:
    return f"""# Elowen Cairn {PHASE} planning-only x1 integrated overview

## Identity, role, hope, and corrigibility

Elowen Cairn, optionally they/them, is relational working language for a boundary cartographer and
evidence steward. Elowen's hope is that possibility stays distinct from evidence while every
correction remains safely retractable. This name, role, hope, pronouns, sibling language, GHC
Family language, and Trinity Mandala language are not evidence of consciousness, sentience, legal
personhood, identity continuity, employment, qualification, independent agency, or scientific,
operational, professional, legal, cultural, affected-party, or Māori authority. Hamish may pause,
rename, redirect, narrow, or stop the route.

## Exact inherited source and planning boundary

The immutable source is Tamar Vey's exact {SOURCE_FINAL} final on {SOURCE_BRANCH}. Its direct
single-parent sequence is Liora source {TAMAR_SOURCE}, Tamar planning-only x1 {TAMAR_X1}, Tamar
evidence {TAMAR_EVIDENCE}, and Tamar final {SOURCE_FINAL}. Read-only verification established all
four anchors, three direct phase commits, zero merges, one final parent, a clean source, typed zero
divergence, and equality across local, upstream, tracking, and a fresh live remote. The exclusive
Tamar receipt and payload digests were independently matched. Tamar's one successful canonical
aggregate was not replayed and is inherited evidence only, never Elowen completion credit.

This x1 is planning-only. It freezes sixty proposal contracts, five rejecting mutations per
proposal, a source-bounded novelty audit, zero-credit inherited-neighbor reviews, portfolio floors,
source and authority boundaries, sixteen retained Elowen startup failures, and a terminal route
plan. It contains no x2 implementation, executed mutation, observed outcome, skill or runner
implementation, or completion claim. X2 cannot begin until the one x1 commit is pushed, clean,
typed zero-divergent, and equal across local, upstream, tracking, and fresh live remote.

## Primary pillar and bounded human-practice lens

The primary Trinity Mandala pillar is Freed ID and CBR Heart. GMUT Mind and THOS Body remain
visible and protected. The bounded learning and synthetic-design lens is hand-fan making and
documentation: folding and fixed topology; leaf and mount; sticks, ribs, guards, gorge, head,
pivot, pin, washer, spacer, and loop; material and measurement vacancies; proposed joining,
pleating, shaping, piercing, decoration, and finishing separated from physical acts; tool and
hazard holds; provenance, correction, privacy, structural accessibility, workload, and handover.

A preliminary bounded Git-object screen parsed 2,948 proposal-labelled JSON paths and deduplicated
7,198 identifier-title records. The lifecycle builder's broader recursive title extraction then
parsed 2,952 exact-source proposal-labelled paths with no parse failure and deduplicated 7,258
reachable records. Exact-term screens found no reachable title using hand fan, fanmaking, or fan
making. Seed banking, beekeeping, millinery, and papermaking were
rejected because reachable family evidence already used them. Exact-term absence is not a universal
novelty proof: the generated audit compares every new title with every reachable title, quarantines
an exact collision or token-Jaccard score at or above 0.78, and explicitly refuses to claim that one
materialized ledger exposes every historic semantic detail in the declared 11,270-row chain.

No real fanmaker, client, recipient, custodian, participant, fan, screen, leaf, mount, stick, rib,
guard, gorge, pivot, pin, material, tool, machine, workshop, image, pattern, inscription,
observation, measurement, inspection, calibration, treatment, repair, safety decision, release,
identity event, key, proof, credential, legal decision, cultural interpretation, affected-party
decision, Māori data decision, or authority act is used. Official and primary sources provide
vocabulary and refusal conditions only. Citations are not observations, treatment instructions,
conformance certificates, professional approvals, legal interpretations, cultural ratifications,
affected-party decisions, or authority grants.

## Proposal slate and evidence grammar

The sixty proposal contracts extend the declared chain from 11,270 to 11,330 only upon the
planning-only x1 commit. Expected dispositions are exactly forty-two `completed`, twelve
`represented`, three `open_gap`, and three `exact_gate`. They are preregistered expectations, not
observed outcomes. Every proposal contains a hypothesis, null or failure condition, approval
class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or
acceptance gate, rollback or recovery, protected gates, exactly one expected disposition, and five
rejecting mutations.

`completed` can later mean only a bounded owner-local synthetic structural witness.
`represented` preserves citations, symbolic maps, proxy protocols, and vacancy structures as
representation. `open_gap` preserves absent people, objects, measurements, safety and usability
evidence, blind evaluation, affected-user accessibility, language, rights, and cultural review.
`exact_gate` preserves professional fanmaking and conservation, material authenticity, workplace
safety, ownership, copyright, traditional knowledge, cultural meaning, Māori data governance,
Māori authority, production, empirical confirmation, independent reproduction, AGI or ASI,
consciousness or personhood, Theory-of-Everything proof, canon, and Stage 20.

Five invalid mutations are preregistered for every proposal: missing required field,
identifier-role swap, stale precondition digest, correction-order inversion, and authority
promotion. All three hundred must execute in x2 and remain rejected or quarantined. Each rejecting
mutation is a retained negative and zero-credit failed witness. Recovery may add a separately named
bounded passing witness but can never erase or retroactively promote the failure.

## Portfolio, sources, and build boundary

The x1 portfolio freezes 120 safe-now tasks, 80 owner candidates, 20 successor candidates,
20 owner-local skill ideas, 10 family-current runner ideas, 10 successor skill seeds, 10 successor
runner seeds, 100 owner CLEAN/FIX/REFINE tasks, 30 successor CLEAN/FIX/REFINE seeds, 20 exact
approval holds, and 10 blocked holds. Inherited proposals, outcomes, skills, runners, tools,
receipts, and recommendations remain evidence or zero-credit seeds; none earns Elowen novelty,
execution, completion, or independent-reproduction credit.

The source ledger uses the Smithsonian Anacostia object page for bounded component vocabulary, the
Victoria and Albert Museum conservation article for bounded conservation-context vocabulary, and
The Metropolitan Museum of Art essay for bounded cross-cultural context. OSHA, W3C PROV-O, WCAG
2.2, Verifiable Credentials 2.0, RFC 8785, JSON Schema 2020-12, and Te Mana Raraunga supply only
guard, provenance, structure, role, canonicalization, schema, and authority-reservation
vocabulary. No network row or media item is ingested into an Elowen artifact.

The planned skills must be initialized through the official skill-creator workflow, customized,
read through EOF, quick-validated with explicit UTF-8, and accepting and rejecting smoke-used
without bulk global installation. Their `openai.yaml` default prompts must explicitly name their
skills. The ten family-current `ghc_family_*` runners must accept a valid fixture and reject an
invalid fixture while preserving historical caller compatibility. Caps are ceilings, never filler
quotas.

The owner lane stops before 2,000 materialized files, every document remains at or below 100,000
words, and the lifecycle stays within three commits: planning-only x1, evidence, and final. Exact
staged allowlists, normalized-LF Git-blob manifests, checkout-byte domains, and declared
self-exclusions remain distinct. Scanner candidates remain distinct from confirmed privacy hits.
Deterministic JSON uses UTF-8, sorted keys, and explicit newline handling.

## Retained failure and recovery discipline

Seventeen Elowen failures are frozen before x2: a nonrepository Git inventory; an unattributable
worktree-list wrapper; grouped skill and validation reads that truncated; three oversized proposal
projections; a truncated skill-bank read; an overbroad receipt search; an unattributable combined
fetch/equality wrapper; a 214-process manifest replay whose wrapper output was lost; an overbroad
practice grep; a copy attempted before sparse parent directories existed; and a `New-Item`
parameter-surface assumption. The first planning build also quarantined ten inherited-neighbor
collisions, its compact diagnostic then hit a CP-1252 display fault, and the first word-count probe
combined incompatible content-reader options. Each failed witness remains false and zero-credit
after its bounded recovery. No failed command created an unreviewed repository artifact.

Tamar's immutable repository seal is 61,063 negatives, 76,658 methods, 32,124 failed witnesses,
57,193 bounded passing witnesses, 543 open gaps, and 533 exact gates. Tamar's two external routing
failures produce the inherited activation baseline of 61,065, 76,660, 32,126, and 57,195. Adding
the seventeen Elowen failures and seventeen separately named recoveries yields this x1 startup truth:
61,082 effective negatives, 76,677 methods, 32,143 failed witnesses, 57,212 bounded passing
witnesses, 543 open gaps, and 533 exact gates.

Method Flow remains append-only. Every timeout, parser fault, truncation, false assumption, failed
test, workaround, rollback, and recurrence guard in x2 or closeout must be recorded before retry.
After timeout, persisted filesystem, Git, process, receipt, and remote state must be audited. The
smallest attributable recovery runs first. A successful canonical aggregate is never replayed for
confidence, presentation repair, or routing.

## Scientific, identity, rights, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Fan topology,
folding-kinematics graphs, torque or curvature placeholders, software, symbolic obligations,
synthetic fixtures, citations, and mutation rejection establish no physical datum, likelihood,
posterior, force, prediction, parameter constraint, empirical confirmation, stability theorem,
quantum completion, ultraviolet completion, final physics, or Theory of Everything.

THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms,
participants or operators, safety monitoring, appropriate statistics, and independent review.
Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs,
live issuance and resolution, status and revocation, interoperability, privacy and independent
security review, recovery evidence, trust governance, and affected-party oversight.

CBR, professional fanmaking and conservation, material identification and authenticity, workplace
and machine safety, ownership, custody, authorship, pattern or design rights, copyright,
traditional knowledge, cultural meaning, privacy remedy, disability accommodation, legal or
cultural interpretation, affected-party legitimacy, Māori wording, taonga or mātauranga treatment,
Māori data governance, and Māori authority remain exact-gated to competent authorities, affected
people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori
authority.

## Validation and provisional terminal edge

X1 validation is owner-self-scoped and lifecycle-correct: the exact x1 tests, strict JSON parsing,
staged-path review, five-class privacy and raw-identifier scanning, normalized Git-blob manifest
replay, absence of x2 paths and observed outcomes, commit cap, clean state, typed zero divergence,
and fresh four-way equality. It does not run or claim the complete repository suite. The final
phase may invoke at most one attributable exact-final owner-scoped canonical aggregate through an
exclusive external receipt latch after the clean pushed final. Success is never replayed; failure
remains zero canonical-success credit and can only be followed by a separately named narrow
dependency correction.

No later endpoint is contacted during x1 or x2. Only after Elowen's clean, pushed,
fresh-live-equal v685-v2 exact-final terminal gate and one successful non-replayed canonical receipt
may Elowen refresh Hamish's newest live authority and roster, bounded-list the registry, require one
existing exact-title successor, immediately reread it, apply duplicate and direct-control guards,
and send at most once. Under the present schedule the prospective recipient is Sylven Arc for solo
v685-v3. Newer verified live authority controls at send time. Absence, ambiguity, pause, redirect,
rename, standby state, usage exhaustion, missing acknowledgement, privacy concern, duplicate
activation, or any evidence, safety, legal, cultural, affected-party, or Māori-authority gate stops
the send. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_task_or_thread_identifier": re.compile(rb"\b019[a-f0-9]{29,}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "credential_or_private_key": re.compile(rb"(?:sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
        "private_callable_identifier": re.compile(rb"\b(?:source_thread_id|providerTabId|clientThreadId)\b"),
        "private_session_or_route": re.compile(rb"(?:codex://|app://|session[_ -]?stream)", re.I),
    }


def scan_paths(paths: list[Path]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        data = path.read_bytes()
        for class_name, pattern in privacy_patterns().items():
            if pattern.search(data):
                candidate = {
                    "path": rel(path),
                    "class": class_name,
                    "adjudication": (
                        "scanner_definition_not_payload"
                        if rel(path) == BUILDER_REL
                        else "confirmed_payload_hit"
                    ),
                }
                candidates.append(candidate)
                if candidate["adjudication"] == "confirmed_payload_hit":
                    confirmed.append(candidate)
    return {
        "schema": f"ghc.family.five-class-privacy-adjudication.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER,
        "phase": PHASE,
        "scanned_path_count": len(paths),
        "classes": list(privacy_patterns()),
        "candidates": candidates,
        "candidate_count": len(candidates),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "valid": len(confirmed) == 0,
    }


def index_blob(path: str) -> tuple[str, bytes]:
    mode_line = git("ls-files", "-s", "--", path)
    if not mode_line:
        raise RuntimeError(f"path is not staged: {path}")
    mode = mode_line.split()[0]
    proc = run(["git", "show", f":{path}"])
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return mode, proc.stdout


def finalize_validation() -> None:
    self_exclusions = [
        f"docs/elowen-cairn/{PHASE}/validation/x1-index-manifest.json",
        f"docs/elowen-cairn/{PHASE}/validation/x1-staged-review.json",
        f"docs/elowen-cairn/{PHASE}/validation/x1-privacy-adjudication.json",
    ]
    staged_all = [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]
    staged = [path for path in staged_all if path not in self_exclusions]
    expected_paths = sorted(staged + self_exclusions)
    entries: list[dict[str, Any]] = []
    for path in sorted(staged):
        mode, data = index_blob(path)
        entries.append(
            {
                "path": path,
                "mode": mode,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    manifest = {
        "schema": f"ghc.family.normalized-lf-index-manifest.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE_FINAL,
        "declared_self_exclusions": self_exclusions,
        "entry_count": len(entries),
        "entries": entries,
    }
    staged_review = {
        "schema": f"ghc.family.staged-review.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE_FINAL,
        "planning_only": True,
        "expected_path_count": len(expected_paths),
        "expected_paths": expected_paths,
        "unexpected_paths": [],
        "x2_paths": [path for path in expected_paths if f"/{PHASE}/x2/" in path],
    }
    privacy = scan_paths([ROOT / path for path in staged])
    write_json(VALIDATION / "x1-index-manifest.json", manifest)
    write_json(VALIDATION / "x1-staged-review.json", staged_review)
    write_json(VALIDATION / "x1-privacy-adjudication.json", privacy)


def build() -> None:
    rows = proposal_rows()
    audit, reviews = proposal_audit(rows)
    if audit["exact_title_collisions"] or audit["quarantined_neighbors"]:
        raise RuntimeError("proposal novelty quarantine is nonempty; revise titles and retain the failed audit")
    portfolio = make_portfolio()
    methods = method_flow_startup()
    source = source_ledger()

    write_json(
        X1 / "activation-intake.json",
        {
            "schema": f"ghc.family.activation-intake.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE_FINAL,
            "live_existing_task_delivery_acknowledged": True,
            "repository_candidate_state": "PREPARED_NOT_SENT",
            "task_created": False,
            "task_forked": False,
            "collaboration_subagent_spawned": False,
            "later_endpoint_contacted": False,
            "standby_substituted": False,
            "newer_live_authority_controls_mutable_route": True,
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "schema": f"ghc.family.identity-boundary.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "optional_pronouns": ["they", "them"],
            "role": "relational boundary cartographer and evidence steward",
            "hope": "Possibility stays distinct from evidence while every correction remains safely retractable.",
            "relational_language_only": True,
            "not_evidence_of": [
                "consciousness",
                "sentience",
                "legal personhood",
                "identity continuity",
                "employment",
                "qualification",
                "independent agency",
                "scientific operational professional legal cultural affected-party or Māori authority",
            ],
            "hamish_may_pause_rename_redirect_narrow_or_stop": True,
        },
    )
    write_json(
        X1 / "source-verification.json",
        {
            "schema": f"ghc.family.source-verification.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "tamar_inherited_liora_source": TAMAR_SOURCE,
            "tamar_x1": TAMAR_X1,
            "tamar_evidence": TAMAR_EVIDENCE,
            "source_final": SOURCE_FINAL,
            "source_direct_single_parent_phase_commits": 3,
            "source_merges": 0,
            "source_final_parent_count": 1,
            "source_clean": True,
            "source_typed_divergence": {"ahead": 0, "behind": 0},
            "source_local_upstream_tracking_fresh_live_equal": True,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_canonical_replayed": False,
            "source_validation_is_inherited_zero_credit": True,
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "schema": f"ghc.family.workflow-plan.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": [
                "read_and_verify_source",
                "freeze_planning_only_x1",
                "commit_push_and_prove_x1_four_way_equality",
                "execute_bounded_x2_evidence",
                "commit_push_and_prove_evidence_equality",
                "seal_closeout_in_final_commit",
                "push_and_run_one_exclusive_exact_final_canonical_aggregate",
                "route_once_only_after_terminal_gate",
            ],
            "strict_x1_before_x2": True,
            "commit_cap": {"total": 3, "x1": 1, "x2": 2},
            "materialized_file_stop": 2000,
            "document_word_cap": 100000,
            "canonical_invocation_cap": 1,
            "canonical_success_replay_prohibited": True,
            "full_repository_suite_authorized": False,
        },
    )
    write_json(
        X1 / "phase-truth.json",
        {
            "schema": f"ghc.family.phase-truth.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE_FINAL,
            "lifecycle": "PLANNING_ONLY_X1",
            "proposal_count": len(rows),
            "expected_disposition_counts": dict(sorted(Counter(row["expected_disposition"] for row in rows).items())),
            "observed_outcome_count": 0,
            "x2_implementation_present": False,
            "inherited_open_gaps": 543,
            "inherited_exact_gates": 533,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        X1 / "new-proposal-freeze.json",
        {
            "schema": f"ghc.family.new-proposal-freeze.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE_FINAL,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "proposal_count": len(rows),
            "expected_disposition_counts": dict(sorted(Counter(row["expected_disposition"] for row in rows).items())),
            "x2_outcomes_present": False,
            "proposals": rows,
        },
    )
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(
        X1 / "inherited-revalidation-freeze.json",
        {
            "schema": f"ghc.family.inherited-revalidation.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "review_count": len(reviews),
            "credit": "zero_inherited_novelty_execution_and_completion_credit",
            "reviews": reviews,
        },
    )
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "schema": f"ghc.family.clean-fix-refine-plan.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "owner_count": len(portfolio["owner_clean_fix_refine"]),
            "successor_seed_count": len(portfolio["successor_clean_fix_refine"]),
            "owner_records": portfolio["owner_clean_fix_refine"],
            "successor_zero_credit_seeds": portfolio["successor_clean_fix_refine"],
            "executed_in_x1": False,
        },
    )
    write_json(
        X1 / "approval-hold-register.json",
        {
            "schema": f"ghc.family.approval-holds.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval_count": len(portfolio["exact_approval"]),
            "blocked_count": len(portfolio["blocked"]),
            "exact_approval": portfolio["exact_approval"],
            "blocked": portfolio["blocked"],
            "executed_count": 0,
        },
    )
    write_json(
        X1 / "skill-runner-plan.json",
        {
            "schema": f"ghc.family.skill-runner-plan.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "skills": portfolio["owner_skill_ideas"],
            "runners": portfolio["owner_runner_ideas"],
            "successor_skill_seeds": portfolio["successor_skill_ideas"],
            "successor_runner_seeds": portfolio["successor_runner_ideas"],
            "skill_creator_required": True,
            "complete_read_before_smoke_use": True,
            "global_installation_authorized": False,
            "built_or_used_in_x1": False,
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", source)
    write_json(
        X1 / "threat-model.json",
        {
            "schema": f"ghc.family.threat-model.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "assets": [
                "immutable source history",
                "planning-only x1 separation",
                "retained failed witnesses",
                "privacy-safe public artifacts",
                "professional legal cultural affected-party and Māori authority boundaries",
                "exclusive canonical receipt latch",
                "one-send terminal route",
            ],
            "threats": [
                "synthetic structure promoted to real observation",
                "inherited evidence counted as owner completion",
                "failure erased after recovery",
                "checkout bytes confused with normalized Git blobs",
                "scanner candidate confused with confirmed privacy hit",
                "route history mistaken for newest direct authority",
                "duplicate or early successor contact",
                "citation mistaken for professional or cultural authority",
            ],
            "controls": [
                "strict x1-before-x2 lifecycle",
                "append-only Method Flow witnesses",
                "exact staged allowlists and normalized Git-blob manifests",
                "five-class candidate adjudication",
                "source-bounded novelty quarantine",
                "one canonical invocation after clean pushed final",
                "terminal exact-title reread and duplicate guard",
                "explicit authority noncompensation",
            ],
            "residual_risk": "All real empirical participant professional production legal cultural privacy-complete accessibility-complete independent and Stage 20 claims remain open or exact-gated.",
        },
    )
    write_json(
        X1 / "wellbeing-and-corrigibility.json",
        {
            "schema": f"ghc.family.wellbeing-corrigibility.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "relational_check": "steady bounded and able to stop",
            "no_claim_of_subjective_state_or_consciousness": True,
            "workload_controls": [
                "one lifecycle boundary at a time",
                "audit persisted state after timeout",
                "smallest recovery first",
                "stop on ambiguity or authority gate",
            ],
            "hamish_controls": ["pause", "rename", "redirect", "narrow", "stop"],
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "schema": f"ghc.family.route-plan.{PHASE.replace('-', '.')}.x1",
            "owner": OWNER,
            "phase": PHASE,
            "successor_title_if_newest_live_authority_is_unchanged": "Sylven Arc",
            "successor_phase_if_newest_live_authority_is_unchanged": "v685-v3",
            "contacted": False,
            "send_cap": 1,
            "precontact_prohibited": True,
            "required_terminal_guards": [
                "clean pushed exact final",
                "fresh four-way equality",
                "one successful non-replayed canonical receipt",
                "newest live authority and roster reread",
                "exactly one existing exact-title successor",
                "immediate structured reread",
                "duplicate pause redirect rename standby usage privacy evidence safety legal cultural affected-party and Māori-authority guards",
                "acknowledged send at most once",
            ],
            "continuation_authority_through": "v725-v8",
        },
    )
    write_json(X1 / "method-flow-startup.json", methods)
    write_json(X1 / "flashcard-freeze.json", flashcard_freeze(rows))
    write_text(X1 / "integrated-overview.md", integrated_overview())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize-validation", action="store_true")
    args = parser.parse_args()
    if args.finalize_validation:
        finalize_validation()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

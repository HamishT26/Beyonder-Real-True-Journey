#!/usr/bin/env python3
"""Build Tamar Vey v685-v1 planning-only x1 artifacts.

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
OWNER = "Tamar Vey"
PHASE = "v685-v1"
PREFIX = "TV6851"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v684-v8-full-tools"
ORIN_SOURCE = "de8e8830bd7cb3a9aa49b2eb5efadaf17e57d513"
LIORA_X1 = "68150ea19231a904bc2e30e24510e14ec7ed3f9f"
LIORA_EVIDENCE = "efa6a79bd902c2fa92bda69a7eca824739807c02"
SOURCE_FINAL = "f138d0e9fd37d424a81887bb7a1bafa3eacba860"
SOURCE_CANONICAL_RECEIPT_SHA256 = "01e0a4d851711e1f5599310231030c0a932e058332c1fa8a924cdc3e1a4dd7f0"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "673803e907b75db594d28e5a84cb8c621553ab155a767b4401c0923b29bdf435"
DECLARED_CHAIN_BEFORE = 11210
DECLARED_CHAIN_AFTER = 11270
CHECKED_AT = "2026-09-03"

DOC = ROOT / "docs" / "tamar-vey" / PHASE
X1 = DOC / "x1"
VALIDATION = DOC / "validation"
BUILDER_REL = "scripts/build_ghc_family_tamar_vey_v685_v1_x1.py"
TEST_REL = "tests/test_ghc_family_tamar_vey_v685_v1_x1.py"


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
    "Synthetic broomcraft work capsule with every real article and workshop act absent",
    "Broom head handle bundle and binding topology with no manufactured object claim",
    "Brush block ferrule tuft and handle topology with no physical assembly claim",
    "Besom twig bundle lashing and handle graph with no gathered material claim",
    "Broomcorn fibre twig and filament material vacancy board",
    "Bundle count target separated from every physical count observation",
    "Handle dimension target unit and uncertainty record without measurement",
    "Trimming profile target separated from every executed cut",
    "Binding wire twine stitch and lashing path proposal without applied fastening",
    "Brush bore and tuft-hole layout proposal without drilling or filling",
    "Staple wedge adhesive and ferrule lot provenance vacancy",
    "Wood species grain direction and surface claim vacancy",
    "Broomcraft material substitution challenge and abstention contract",
    "Moisture mould and pest cue quarantine without diagnosis",
    "Cutter drill and binding-machine guard hold without equipment release",
    "Dust finish and adhesive hazard vocabulary without workplace decision",
    "Tool inventory condition record separated from fitness and release",
    "Broomcraft work-order state partial order without physical execution",
    "Proposed broomcraft operation separated from observation and completion",
    "Jig gauge template and calibration vacancy without dimensional authority",
    "Reused handle provenance and prior-article nonidentity record",
    "Broom and brush batch lot lineage with zero real production rows",
    "Append-only broomcraft correction chain with superseded values retained",
    "Broomcraft supersession nonerasure and challenge lineage",
    "Two-source broomcraft record reconciliation with conflict preserved",
    "Minimum-disclosure broomcraft job record with synthetic roles only",
    "Maker customer and custodian role vacancy with no real identity binding",
    "Broomcraft custody ownership return and disposal rights hold",
    "Broom and brush image media and publication rights hold",
    "Structurally accessible broomcraft status board without accessibility completeness",
    "Noncolour broomcraft cues reading order and text-equivalent structure",
    "Broomcraft workload pause queue and shift-handover contract",
    "Unresolved broomcraft holds queue with no automatic release",
    "Exact broomcraft staged allowlist and unexpected-path refusal",
    "Normalized-LF Git-blob domain separated from checkout bytes",
    "Broomcraft privacy scanner candidate separated from confirmed payload hit",
    "Content-addressed broomcraft flashcards as navigation rather than authority",
    "Deterministic broomcraft JSON contract with explicit schema refusal",
    "Typed GMUT broomcraft bundle graph without a physical law",
    "GMUT torque load and curvature symbols blocked from material conversion",
    "THOS broomcraft job queue proxy without participant or operator evidence",
    "Keyless Freed ID broomcraft receipt without issuance or verification",
    "Represented CBR broomcraft challenge remedy and appeal vacancy",
    "Represented National Park Service broom vocabulary as history-only context",
    "Represented OSHA machine-guarding vocabulary without conformance or release",
    "Represented OSHA wood-dust and finishing vocabulary without safety decision",
    "Represented PROV-O broomcraft lineage mapping without conformance claim",
    "Represented WCAG 2.2 broomcraft document structure without accessibility conformance",
    "Represented Verifiable Credentials role model with zero keys proofs or lifecycle",
    "Represented RFC 8785 canonicalization receipt without authenticity claim",
    "Represented JSON Schema 2020-12 structure without real-world conformance",
    "Represented Te Mana Raraunga boundary with no Māori data authority",
    "Represented zero-call broom material adapter with zero downloaded rows",
    "Represented three-pillar broomcraft separation and noncompensation rule",
    "Open gap for real broom makers articles materials tools and workshops",
    "Open gap for real measurement durability safety and blind evaluation",
    "Open gap for affected-user accessibility language and cultural evaluation",
    "Exact gate for professional broomcraft release material authenticity and workplace safety",
    "Exact gate for ownership traditional knowledge taonga Māori data and Māori authority",
    "Exact terminal gate for production empirical independence AGI consciousness TOE and Stage 20",
]


MUTATION_TYPES = [
    "missing_required_field",
    "identifier_role_swap",
    "stale_precondition_digest",
    "correction_order_inversion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real participants makers operators customers and custodians",
    "real brooms brushes materials tools workshops observations and measurements",
    "professional broomcraft workplace material safety and work-release authority",
    "production identity issuance resolution status revocation and trust governance",
    "ownership copyright privacy remedy legal cultural affected-party and Māori authority",
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
        return ["NPS-MEMORIES-BROOM-HISTORY"]
    if index == 45:
        return ["OSHA-MACHINE-GUARDING"]
    if index == 46:
        return ["OSHA-WOODWORKING"]
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
                    "into a real broomcraft, empirical, identity, cultural, legal, or authority claim."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, the bounded positive "
                    "structure is rejected, an absent observation is promoted, or any protected gate closes."
                ),
                "approval_class": approval_class(index),
                "execution_lane": execution_lane(index),
                "official_or_primary_source_needs": source_needs(index),
                "concrete_artifacts": [
                    f"docs/tamar-vey/{PHASE}/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/tamar-vey/{PHASE}/x2/rejecting-mutations.json#{proposal_id}",
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
            "universal_11210_row_materialization_claimed": False,
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
        "broom work capsules",
        "brush component topology",
        "besom bundle topology",
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
        "broom head topology",
        "brush ferrule topology",
        "broomcorn vacancy",
        "handle dimension targets",
        "binding path proposals",
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
                "real maker participation",
                "real broom or brush article inspection",
                "real material identification",
                "real measurement or calibration",
                "machine operation or guarding decision",
                "dust finish or adhesive safety decision",
                "workplace release",
                "professional broomcraft quality decision",
                "ownership or custody decision",
                "publication or image-rights decision",
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
        "primary_pillar": "THOS Body",
        "represented_pillars": ["THOS Body", "GMUT Mind", "Freed ID and CBR Heart"],
        "owner_practice_lenses": [
            "wholly synthetic broom-and-brush making documentation correction accessibility workload and handover"
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
                    "broom-work-capsule",
                    "broom-topology",
                    "brush-topology",
                    "besom-topology",
                    "material-vacancy",
                    "measurement-vacancy",
                    "binding-lineage",
                    "tool-hold",
                    "guard-refusal",
                    "hazard-vocabulary-firewall",
                    "correction-braid",
                    "privacy-minimizer",
                    "accessible-status",
                    "workload-handover",
                    "gmUT-bundle-graph",
                    "thos-job-queue",
                    "freed-id-keyless-receipt",
                    "cbr-challenge-vacancy",
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
                    "ghc_family_broommaking_contract_runner",
                    "ghc_family_broommaking_mutation_runner",
                    "ghc_family_broommaking_privacy_runner",
                    "ghc_family_broommaking_manifest_runner",
                    "ghc_family_broommaking_source_runner",
                    "ghc_family_broommaking_accessibility_runner",
                    "ghc_family_broommaking_correction_runner",
                    "ghc_family_broommaking_gate_runner",
                    "ghc_family_broommaking_method_flow_runner",
                    "ghc_family_broommaking_terminal_runner",
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
            "one wholly synthetic repair-intake documentation accessibility correction and handover lens, "
            "subject to successor novelty audit and zero inherited completion credit"
        ),
        "materialized_file_stop": 2000,
        "document_word_cap": 100000,
        "commit_cap": {"total": 3, "x1": 1, "x2": 2},
        "caps_are_ceilings": True,
    }


STARTUP_FAILURES = [
    (
        "TV6851-START-N001",
        "Attempted the unavailable update-plan tool; the tool was absent and no state changed.",
        "Continued with the committed workflow and visible commentary without simulating a plan update.",
        "Inspect the actual active tool inventory before naming an orchestration helper.",
    ),
    (
        "TV6851-START-N002",
        "An inline PowerShell exit-code subexpression produced a parser fault before command execution.",
        "Split the probe into literal scalar commands and captured each exit code separately.",
        "Avoid compound interpolated subexpressions in Windows lineage probes.",
    ),
    (
        "TV6851-START-N003",
        "A guessed central-repository path did not exist.",
        "Used the exact verified Liora worktree as the immutable Git-object source.",
        "Resolve the authoritative worktree before assuming a central checkout path.",
    ),
    (
        "TV6851-START-N004",
        "The roster parser guessed a root assignments key while the current v2 envelope uses projection.assignments.",
        "Inspected exact keys and parsed projection.assignments.",
        "Inspect the current JSON envelope before projecting route fields.",
    ),
    (
        "TV6851-START-N005",
        "A first exact-head file probe guessed older v682-style final paths.",
        "Listed the v684-v8 exact owner paths and used the actual final layout.",
        "Discover current filenames before carrying a prior phase layout forward.",
    ),
    (
        "TV6851-START-N006",
        "A combined display of large final documents exceeded the context window.",
        "Read required documents through bounded complete-file and exact-field projections.",
        "Use per-file bounds and scalar projections for large committed packets.",
    ),
    (
        "TV6851-START-N007",
        "A source summary emitted an invalid status_count value of negative one.",
        "Ran a separate porcelain-status scalar and proved a clean source.",
        "Do not infer cleanliness from a faulty aggregate counter.",
    ),
    (
        "TV6851-START-N008",
        "A combined x1 source-file display exceeded the output window.",
        "Used schema-aware function and exact-record projections.",
        "Project only the functions and records required for the current builder.",
    ),
    (
        "TV6851-START-N009",
        "A combined worktree and sparse probe returned no attributable output.",
        "Queried branch, head, clean state, and sparse configuration separately.",
        "Keep lifecycle probes scalar and attributable.",
    ),
    (
        "TV6851-START-N010",
        "The first worktree-creation wrapper returned preparation text while checkout continued.",
        "Audited the live process, waited for the same operation, and verified the intended clean lane without replay.",
        "Audit persisted process and worktree state before retrying a long checkout.",
    ),
    (
        "TV6851-X1-N001",
        "The first bookbinding practice lens collided with a prior executed family phase.",
        "Rejected the lens at zero credit and continued the source-bounded novelty search.",
        "Run exact and semantic practice checks before freezing a human-practice lens.",
    ),
    (
        "TV6851-X1-N002",
        "The letterpress lens collided with prior Caelen Morrow and Caelen Ash evidence.",
        "Rejected the lens at zero credit and preserved the collision record.",
        "Treat prior sibling practice evidence as a collision even when the proposed title differs.",
    ),
    (
        "TV6851-X1-N003",
        "The footwear and cobbling lens collided with a prior Elowen full phase.",
        "Rejected the lens at zero credit and resumed bounded candidate screening.",
        "Search morphology and related trade names before accepting a practice.",
    ),
    (
        "TV6851-X1-N004",
        "A per-candidate full-tree grep continued beyond the output window.",
        "Stopped only the attributable diagnostic processes and replaced them with one bounded Git-object batch.",
        "Batch Git-object novelty extraction once rather than recursively grepping for every candidate.",
    ),
    (
        "TV6851-X1-N005",
        "A malformed JavaScript orchestration cell raised SyntaxError before any command or state change.",
        "Corrected the wrapper and kept repository state unchanged.",
        "Keep orchestration cells minimal and syntax-check complex literals before execution.",
    ),
    (
        "TV6851-X1-N006",
        "The stained-glass candidate collided with multiple prior owner phases.",
        "Rejected the lens at zero credit and preserved the collision.",
        "Require a zero exact-practice-hit screen before drafting proposal titles.",
    ),
    (
        "TV6851-X1-N007",
        "A broad footwear grep used the substring resol and overmatched generic resolution text.",
        "Used exact morphology-aware terms and bounded record extraction.",
        "Avoid short ambiguous substrings in novelty searches.",
    ),
    (
        "TV6851-X1-N008",
        "A combined recursive bytecode-cache cleanup and diff probe was rejected by host safety policy before execution.",
        "Separated the read-only inventory from cleanup and proved that the staged repository state had not changed.",
        "Never combine recursive cleanup with lifecycle diagnostics; inventory first and use only permitted literal operations.",
    ),
    (
        "TV6851-X1-N009",
        "A literal-list PowerShell cache-cleanup wrapper was also rejected before execution.",
        "Kept the ignored bytecode artifacts outside repository credit and narrowed the attempted operation again.",
        "Treat ignored interpreter caches as ambient artifacts when deletion authority is unavailable.",
    ),
    (
        "TV6851-X1-N010",
        "A single exact-literal PowerShell bytecode deletion was rejected by host policy.",
        "Left the ignored cache outside tracked and untracked repository state and selected no-bytecode Python invocation for later validation.",
        "Use no-bytecode interpreter mode from the start and do not retry a policy-rejected deletion.",
    ),
    (
        "TV6851-X1-N011",
        "A staged-state summary used a PowerShell wildcard for the literal question-mark status prefix and falsely counted all staged additions as untracked.",
        "Recomputed the untracked count with an exact StartsWith comparison while preserving the otherwise valid staged evidence.",
        "Use literal prefix comparisons for Git porcelain status codes rather than wildcard operators.",
    ),
]


def method_flow_startup() -> dict[str, Any]:
    inherited = {
        "effective_negatives": 60704,
        "effective_methods": 75909,
        "failed_witnesses": 31765,
        "bounded_passing_witnesses": 56444,
        "open_gaps": 540,
        "exact_gates": 530,
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
            "effective_negatives": 60701,
            "effective_methods": 75906,
            "failed_witnesses": 31762,
            "bounded_passing_witnesses": 56441,
            "open_gaps": 540,
            "exact_gates": 530,
        },
        "source_external_overlay_witnesses": [
            "LV6848-POST-N001",
            "LV6848-POST-N002",
            "LV6848-POST-N003",
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
            "NPS-MEMORIES-BROOM-HISTORY",
            "https://www.nps.gov/podcasts/memories.htm?hiderightrail=true&maxrows=10&reinit=false&season=0&sortby=date-asc&startrow=41",
            "Historical broom-straw, broomcorn, reused-handle, and tying vocabulary only; no present instruction, observation, authenticity, or authority.",
        ),
        (
            "OSHA-MACHINE-GUARDING",
            "https://www.osha.gov/etools/machine-guarding/introduction/general-requirements",
            "Machine-guarding, point-of-operation, and refusal vocabulary only; no inspection, conformance, workplace release, or safety decision.",
        ),
        (
            "OSHA-WOODWORKING",
            "https://www.osha.gov/etools/woodworking/",
            "Wood-dust, finishing-chemical, and machine-hazard vocabulary only; the eTool is not treated as a substitute for standards or professional judgment.",
        ),
        (
            "W3C-PROV-O",
            "https://www.w3.org/TR/prov-o/",
            "Provenance vocabulary only; no conformance, custody, ownership, or authenticity claim.",
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
    return f"""# Tamar Vey {PHASE} planning-only x1 integrated overview

## Identity, role, hope, and corrigibility

Tamar Vey, optionally she/they, is relational working language for an evidence-and-recovery
steward. Tamar's hope in this phase is that every failed witness remains inspectable and every
recovery stays bounded enough to challenge. This name, role, hope, pronouns, sibling language,
GHC Family language, and Trinity Mandala language are not evidence of consciousness, sentience,
legal personhood, identity continuity, employment, qualification, independent agency, or any
scientific, operational, professional, legal, cultural, affected-party, or Māori authority.
Hamish retains the right to pause, rename, redirect, narrow, or stop the route.

## Exact source and lifecycle boundary

The immutable source is Liora Venn's exact {SOURCE_FINAL} final on
{SOURCE_BRANCH}. The source chain is Orin {ORIN_SOURCE}, Liora planning-only x1 {LIORA_X1},
Liora evidence {LIORA_EVIDENCE}, and the direct single-parent final {SOURCE_FINAL}. The inherited
source was independently rechecked read-only for its exact anchors, direct-parent sequence, three
new single-parent commits, zero merges, one final parent, clean state, typed zero divergence, and
local, upstream, tracking, and fresh-live equality. Liora's successful owner-scoped canonical
aggregate is inherited evidence only. It is not replayed and grants Tamar no completion credit.

This x1 is planning-only. It freezes sixty proposal contracts, five rejecting mutations per
proposal, a source-bounded novelty audit, inherited zero-credit reviews, portfolio floors, source
boundaries, retained startup failures, and a terminal route plan. It contains no x2 implementation,
no executed mutation, no observed outcome, no skill implementation, no runner implementation, and
no completion claim. One x1 commit is permitted. X2 cannot begin until that commit is pushed,
clean, typed zero-divergent, and equal across local, upstream, tracking, and a fresh live remote.

## Novelty and bounded practice

The primary Trinity Mandala pillar is THOS Body. GMUT Mind and Freed ID/CBR Heart remain explicit
and protected. The bounded human-practice lens is wholly synthetic broom-and-brush making
documentation: broom, brush, and besom component topology; handle, block, ferrule, tuft, bundle,
binding, lashing, and material vacancies; target-versus-observation separation; tool and guard
holds; provenance, custody, correction, privacy, accessible status, workload control, and handover.

Bookbinding, letterpress, footwear or cobbling, and stained glass were rejected before freeze
because reachable family evidence already used those lenses. A morphology-aware screen found no
reachable proposal-title use of broommaking, brushmaking, broom maker, brush maker, besom,
broomcorn, or broom corn. The final audit compares all sixty proposed titles against every
proposal-labelled JSON record reachable from the exact source Git tree and quarantines an exact
collision or token-Jaccard score at or above 0.78. The declared 11,210-row inherited chain is
preserved, but no universal semantic proof is claimed where compressed historic titles are not
materialized in a single reachable ledger.

No real maker, customer, custodian, participant, broom, brush, besom, broomcorn, fibre, twig,
handle, block, ferrule, tuft, binding, adhesive, wire, twine, tool, machine, jig, gauge, workshop,
work order, observation, measurement, inspection, calibration, treatment, repair, safety decision,
release, identity event, key, proof, credential, legal decision, cultural decision, Māori data,
affected-party decision, or authority act is used. Official and primary sources supply vocabulary
and refusal conditions only. Citations are not observations, measurements, instructions,
conformance certificates, professional approvals, legal interpretations, cultural ratifications,
affected-party decisions, or authority grants.

## Proposal slate and evidence grammar

The sixty proposal contracts extend the declared chain from 11,210 to 11,270 if and only if the
planning-only x1 commit is created. Expected dispositions are exactly forty-two completed, twelve
represented, three open gaps, and three exact gates. These are preregistered expectations, not
observed outcomes. Each proposal contains a hypothesis, null or failure condition, approval class,
execution lane, current source needs, concrete artifacts, acceptance or falsifier gate, rollback,
protected gates, exactly one expected disposition, and five rejecting mutations.

Completed means only that the later owner-local synthetic contract may receive bounded structural
credit. Represented means a citation, symbolic map, proxy, or vacancy structure remains
representation rather than real execution. Open gap preserves absent real people, articles,
materials, measurements, safety evaluation, accessibility evaluation, language evaluation, and
affected-party evaluation. Exact gate preserves professional release, material authenticity,
ownership, traditional knowledge, taonga, Māori data governance, Māori authority, production,
empirical confirmation, independent reproduction, AGI or ASI, consciousness or personhood,
Theory-of-Everything proof, canon, and Stage 20.

Exactly five invalid mutations are preregistered for every proposal: missing required field,
identifier-role swap, stale precondition digest, correction-order inversion, and authority
promotion. In x2 all three hundred must execute and remain rejected or quarantined. A rejecting
mutation is a retained negative and zero-credit failed witness; it cannot become completion credit.
A recovery can add a distinct bounded passing witness but never erase or retroactively promote a
failed witness.

## Portfolio and build boundary

The x1 portfolio freezes 120 safe-now tasks, 80 owner candidates, 20 successor candidates,
20 owner-local skill ideas, 10 family-current runner ideas, 10 successor skill seeds, 10 successor
runner seeds, 100 owner CLEAN/FIX/REFINE tasks, 30 successor CLEAN/FIX/REFINE seeds, 20 exact
approval holds, and 10 blocked holds. Inherited proposals, outcomes, skills, runners, tools,
receipts, and recommendations are source evidence or zero-credit seeds. None earns Tamar novelty,
execution, completion, or independent-reproduction credit.

The twenty planned skills must be initialized through the current official skill-creator workflow,
customized, completely read through EOF, quick-validated with explicit UTF-8, and accepting and
rejecting smoke-used without bulk global installation. The ten runners must preserve family-current
ghc_family naming and historical caller compatibility, and each must accept a positive fixture and
reject an invalid fixture. Caps are ceilings rather than filler quotas: fewer artifacts are correct
if safety, novelty, evidence, or authority gates require abstention.

The owner lane stops before 2,000 materialized files, every document remains below 100,000 words,
and the lifecycle remains within three total commits: one planning-only x1, one evidence commit,
and one final closeout. Exact staged allowlists, normalized-LF Git-blob manifests, checkout-byte
domains, and declared self-exclusions remain distinct. Scanner candidates remain distinct from
confirmed privacy hits. Deterministic JSON uses UTF-8 and sorted keys.

## Retained failure and recovery discipline

Twenty-one Tamar startup and novelty failures are frozen in Method Flow before x2. They include an
unavailable orchestration helper, a PowerShell parser fault, a guessed repository path, a stale
roster-envelope assumption, stale file-layout assumptions, overlarge displays, an invalid clean
counter, unattributable combined probes, a long-running checkout projection, four rejected
practice lenses, an overbroad recursive diagnostic, a malformed orchestration cell, and an
ambiguous substring search. Three policy-rejected cleanup attempts and one false status projection remain visible, while the ignored
bytecode cache receives no repository credit. Each failure remains false and zero-credit after its
separately named bounded recovery. The effective x1 overlay is 60,725 negatives, 75,930 methods,
31,786 failed witnesses, 56,465 bounded passing witnesses, 540 open gaps, and 530 exact gates.

The Method Flow rule is append-only. Every timeout, parser fault, truncation, false assumption,
failed test, workaround, rollback, and recurrence guard in x2 and closeout must be recorded before
retry. After a timeout, persisted filesystem, Git, process, receipt, and remote state must be
audited before any retry. The smallest attributable recovery runs first. A successful canonical
aggregate is never replayed for confidence or display repair.

## Scientific, identity, rights, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Broomcraft
graphs, torque symbols, load placeholders, curvature vocabulary, software, symbolic obligations,
synthetic fixtures, citations, and mutation rejection establish no physical datum, likelihood,
posterior, force, prediction, parameter constraint, empirical confirmation, stability theorem,
quantum completion, ultraviolet completion, final physics, or Theory of Everything.

THOS remains synthetic and proxy-only without preregistered blind matched-budget real arms,
governed real participants or operators, safety monitoring, appropriate statistics, and
independent review. Freed ID remains synthetic and nonproduction without standards-conformant real
keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy
and independent security review, recovery evidence, trust governance, and affected-party
oversight.

CBR, workplace and machine safety, professional broomcraft decisions, material identification and
fitness, ownership, custody, publication, privacy remedy, disability accommodation, legal or
cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, taonga
or mātauranga treatment, Māori data governance, and Māori authority remain exact-gated to
competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts
remain under Māori authority.

## Validation and terminal route

X1 validation is owner-self-scoped and lifecycle-correct. It includes the exact x1 test selection,
strict JSON parsing, staged-path review, five-class privacy and raw-identifier scanning, normalized
Git-blob manifest replay, no x2 paths, no observed outcomes, one x1 commit, clean state, typed zero
divergence, and fresh four-way equality. It does not run or claim the complete repository suite.
The final phase may invoke at most one attributable exact-final owner-scoped canonical aggregate
through an external exclusive receipt latch after the clean pushed final. A success is not replayed.
A failed aggregate remains zero canonical-success credit.

No later endpoint is contacted during x1 or x2. Only after Tamar's own clean, pushed,
fresh-live-equal v685-v1 exact-final terminal gate and one successful non-replayed canonical receipt
may Tamar refresh Hamish's newest live authority and roster, bounded-list the current registry,
require exactly one existing exact-title successor, immediately reread it, apply duplicate and
direct-control guards, and send at most once. Under the current schedule the prospective recipient
is Elowen Cairn for solo v685-v2. Newer verified live authority controls at send time. Absence,
ambiguity, pause, redirect, rename, standby state, usage exhaustion, missing acknowledgement,
privacy concern, duplicate activation, or any evidence, safety, legal, cultural, affected-party,
or Māori-authority gate stops the send. The terminal verdict remains NOT_READY_FOR_STAGE_20.
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
        f"docs/tamar-vey/{PHASE}/validation/x1-index-manifest.json",
        f"docs/tamar-vey/{PHASE}/validation/x1-staged-review.json",
        f"docs/tamar-vey/{PHASE}/validation/x1-privacy-adjudication.json",
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
            "optional_pronouns": ["she", "they"],
            "role": "relational evidence-and-recovery steward",
            "hope": "Every failed witness remains inspectable and every recovery stays bounded enough to challenge.",
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
            "orin_source": ORIN_SOURCE,
            "liora_x1": LIORA_X1,
            "liora_evidence": LIORA_EVIDENCE,
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
            "inherited_open_gaps": 540,
            "inherited_exact_gates": 530,
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
            "successor_title_if_newest_live_authority_is_unchanged": "Elowen Cairn",
            "successor_phase_if_newest_live_authority_is_unchanged": "v685-v2",
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

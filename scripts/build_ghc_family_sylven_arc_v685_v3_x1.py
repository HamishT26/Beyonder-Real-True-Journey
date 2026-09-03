#!/usr/bin/env python3
"""Build Sylven Arc v685-v3 planning-only x1 artifacts.

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
OWNER = "Sylven Arc"
PHASE = "v685-v3"
PREFIX = "SA6853"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v685-v2-full-tools"
ELOWEN_SOURCE = "b2cfabd4d836737b375910ccb73f8037a8ad6c4d"
ELOWEN_X1 = "3ae1ab2839e6f4c32b6c0e78f82cf370445e6a4b"
ELOWEN_EVIDENCE = "ad08f3717b6e82e8df6771683b2aa2b0fd2bedc1"
SOURCE_FINAL = "7fd5e87aa5e0e371f1379e263adf096151c375ee"
SOURCE_CANONICAL_RECEIPT_SHA256 = "0a920b92ad25bb46b4bcece17c5cf9a08814b17c81df337e7b0c92c8dea1be04"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "78d17ed41106546c9b91bf7a0c4bdab8363c02402f41d46a4b7f2e1b713e8d5b"
DECLARED_CHAIN_BEFORE = 11330
DECLARED_CHAIN_AFTER = 11390
CHECKED_AT = "2026-09-03"

DOC = ROOT / "docs" / "sylven-arc" / PHASE
X1 = DOC / "x1"
VALIDATION = DOC / "validation"
BUILDER_REL = "scripts/build_ghc_family_sylven_arc_v685_v3_x1.py"
TEST_REL = "tests/test_ghc_family_sylven_arc_v685_v3_x1.py"


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
    "Synthetic lighthouse-station documentation capsule with every real site object and operation absent",
    "Marine-aid asset identifier separated from every service-status and navigation claim",
    "Tower lantern watch-room gallery and foundation topology without physical survey",
    "Fresnel optic prism panel and lens-order vacancy without object observation",
    "Lantern light-source housing ventilation and glazing topology without inspection",
    "Rotating optic clockwork gear bearing and drive vacancy without mechanism operation",
    "Proposed flash period eclipse sequence and group characteristic without emitted signal",
    "Sector colour bearing and boundary record without navigational direction",
    "Nominal-range target separated from measured visibility meteorology and observer response",
    "Daymark shape colour and pattern representation without IALA conformance claim",
    "Solar battery generator mains and fuel-source vacancy without electrical work",
    "Remote monitoring telemetry alarm and status schema with zero connection",
    "Fog-signal emitter timing and acoustic-path topology without sound generation",
    "Keeper quarters oil house workshop landing and boathouse relation map without site survey",
    "Stairs ladder landing balcony and catwalk topology without access or fall-safety release",
    "Fresnel order manufacturer-mark and installation-date vocabulary without authentication",
    "Weather salt corrosion condensation and water-ingress cue quarantine without condition finding",
    "Lamp outage rotation fault alarm and visibility cue quarantine without diagnosis",
    "Electrical fire fuel battery confined-space height and maritime hazard vocabulary without safety decision",
    "Servicing inspection cleaning lubrication and alignment checklist refusal without maintenance authority",
    "Readiness-refusal ledger for calibration commissioning and return-to-service authority absent",
    "Synthetic lighthouse work-order partial order without physical execution",
    "Proposed keeper or technician command separated from observation completion and release",
    "Timestamp timezone watch interval and uncertain-duration contract without operational log claim",
    "Reused optic lantern or mechanism provenance and prior-object nonidentity record",
    "Optic assembly serial genealogy linking lantern mechanism and declared batch uncertainty at zero production",
    "Correction-event braid for beacon-status revisions retaining every prior value and reason",
    "Lighthouse supersession nonerasure challenge appeal and review lineage",
    "Two-source lighthouse record reconciliation with unresolved conflict preserved",
    "Vacant-role minimization envelope for unnamed station contacts with zero person binding",
    "Keeper technician mariner custodian owner and visitor role vacancy with no real identity binding",
    "Lighthouse custody ownership decommission transfer return and disposal rights hold",
    "Lighthouse image chart logbook recording and publication-rights hold",
    "Structurally accessible lighthouse status board without accessibility completeness",
    "Noncolour signal-state cues reading order headings and text-equivalent structure",
    "Lighthouse workload pause queue watch-handover and fatigue-escalation contract",
    "Unresolved lighthouse safety maintenance and authority holds queue with no automatic release",
    "Exact lighthouse staged allowlist and unexpected-path refusal",
    "Normalized Git-blob hash manifest for lighthouse planning bytes with checkout-domain refusal",
    "Five-class lighthouse data-leak adjudication distinguishing regex definitions from payload evidence",
    "Typed GMUT periodic optical-signal graph without a material law likelihood or prediction",
    "THOS watch-handover dependency graph joined to proofless Freed ID status without authority transfer",
    "Represented CBR lighthouse challenge remedy refusal and appeal vacancy",
    "Represented IALA S1020 marine-aid design vocabulary without conformance or service claim",
    "Represented IALA visual-aid light-source and characteristic vocabulary without implementation",
    "Represented National Park Service lighthouse component vocabulary without inspection or treatment",
    "W3C PROV-O entity activity agent crosswalk for station-record lineage as representation only",
    "Structural lighthouse-status presentation mapped to WCAG 2.2 as nonconformant representation",
    "Keyless lighthouse-custody role vocabulary mapped to Verifiable Credentials 2.0 without credential lifecycle",
    "RFC 8785 deterministic JSON projection for station packets without signature identity or trust conclusion",
    "Machine-checkable lighthouse packet shape using JSON Schema Draft 2020-12 without field validation",
    "Te Mana Raraunga authority-reservation boundary for hypothetical station records without Māori interpretation",
    "Represented zero-call IALA catalogue adapter with zero downloaded or ingested rows",
    "Represented three-pillar lighthouse separation and authority noncompensation rule",
    "Open gap for real keepers technicians mariners stations optics equipment and governed participants",
    "Open gap for real measurements availability reliability visibility safety and blind evaluation",
    "Open gap for affected-user review of signal-status documents across disability maritime language and rights communities",
    "Exact gate for professional aids-to-navigation maintenance electrical maritime and workplace safety",
    "Exact protected hold for site heritage title custodianship indigenous knowledge and Māori governance decisions",
    "Terminal refusal to translate synthetic lighthouse software into deployment empirical physics AGI personhood canon or Stage Twenty",
]


MUTATION_TYPES = [
    "missing_required_field",
    "identifier_role_swap",
    "stale_precondition_digest",
    "correction_order_inversion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real keepers technicians mariners operators owners custodians and affected users",
    "real lighthouse stations optics lanterns mechanisms power systems observations and measurements",
    "professional aids-to-navigation maintenance electrical fire fall confined-space maritime and workplace safety authority",
    "production identity issuance resolution status revocation and trust governance",
    "heritage ownership copyright traditional knowledge cultural meaning privacy remedy affected-party and Māori authority",
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
        return ["IALA-S1020"]
    if index == 45:
        return ["IALA-ATON-GUIDELINES"]
    if index == 46:
        return ["NPS-POINT-LOMA", "NPS-LIGHTHOUSE-HANDBOOK"]
    if index in {17, 18, 19, 20}:
        return ["IALA-S1020", "NPS-LIGHTHOUSE-HANDBOOK"]
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
        return ["IALA-ATON-GUIDELINES"]
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
                    "into a real lighthouse, empirical, identity, cultural, legal, or authority claim."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, the bounded positive "
                    "structure is rejected, an absent observation is promoted, or any protected gate closes."
                ),
                "approval_class": approval_class(index),
                "execution_lane": execution_lane(index),
                "official_or_primary_source_needs": source_needs(index),
                "concrete_artifacts": [
                    f"docs/sylven-arc/{PHASE}/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/sylven-arc/{PHASE}/x2/rejecting-mutations.json#{proposal_id}",
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
            "universal_11330_row_materialization_claimed": False,
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
        "lighthouse station work capsules",
        "tower lantern and gallery topology",
        "optic prism and light-source vacancy",
        "characteristic and sector vacancy",
        "power telemetry and alarm vacancy",
        "stairs catwalk and access holds",
        "correction and provenance lineage",
        "privacy minimization",
        "accessible status",
        "workload watch and handover",
        "GMUT typed periodic graphs",
        "THOS maintenance queues",
    ]
    operations = [
        "define schema", "add positive fixture", "add refusing fixture", "record provenance",
        "enforce nonconversion", "add rollback", "add recurrence guard", "scan privacy",
        "verify deterministic bytes", "document authority boundary",
    ]
    candidate_themes = [
        "lantern and optic topology", "flash-characteristic vacancy", "tower and gallery topology",
        "nominal-range targets", "power and telemetry vacancy", "maintenance refusal",
        "rights heritage and custody", "three-pillar separation",
    ]
    candidate_ops = ["model", "validate", "mutate", "quarantine", "trace", "adjudicate", "render", "review", "hash", "handover"]
    clean_themes = [
        "schema names", "identifier roles", "source status", "unit fields", "correction ordering",
        "privacy labels", "manifest domains", "stale route labels", "authority language", "rollback notes",
    ]
    clean_ops = [
        "CLEAN duplicates", "FIX ambiguity", "REFINE refusal", "CLEAN serialization",
        "FIX deterministic order", "REFINE evidence boundary", "CLEAN stale wording",
        "FIX fixture isolation", "REFINE recurrence guard", "CLEAN handover state",
    ]
    exact_titles = [
        "real lighthouse keeper or technician participation", "real lighthouse station inspection",
        "real optic or lantern identification", "real measurement calibration or commissioning",
        "electrical isolation energization or work decision", "fire fuel battery or confined-space safety decision",
        "height access fall-protection or rescue decision", "maritime aids-to-navigation service decision",
        "professional maintenance preservation or conservation decision",
        "ownership custody decommission or transfer decision",
        "chart logbook image or publication-rights decision", "heritage or protected-place decision",
        "real identity issuance", "real key or proof lifecycle", "privacy impact acceptance",
        "accessibility affected-user acceptance", "legal interpretation",
        "cultural or traditional-knowledge interpretation",
        "Māori wording data-governance or authority decision", "production deployment or Stage 20 disposition",
    ]
    blocked_titles = [
        "live light or fog-signal actuation", "electrical panel fuel battery or generator work",
        "tower ladder catwalk or confined-space access", "destructive optic or material testing",
        "private operational log or collection disclosure", "professional certification",
        "legal or heritage rights adjudication", "cultural legitimacy or Māori authority claim",
        "independent reproduction claim", "AGI consciousness Theory-of-Everything or Stage 20 claim",
    ]
    skill_names = [
        "lighthouse-work-capsule", "tower-lantern-topology", "optic-prism-vacancy",
        "characteristic-observation-separator", "sector-bearing-nonclaim", "power-telemetry-firewall",
        "height-access-refusal", "hazard-vocabulary-firewall", "maintenance-release-hold",
        "correction-braid", "privacy-minimizer", "accessible-status", "workload-watch-handover",
        "provenance-conflict-preserver", "gmut-periodic-signal-graph", "thos-lighthouse-work-queue",
        "freed-id-keyless-receipt", "cbr-heritage-rights-hold", "manifest-domain-separator",
        "authority-noncompensation",
    ]
    runner_names = [
        "ghc_family_lighthouse_contract_runner", "ghc_family_lighthouse_mutation_runner",
        "ghc_family_lighthouse_privacy_runner", "ghc_family_lighthouse_manifest_runner",
        "ghc_family_lighthouse_source_runner", "ghc_family_lighthouse_accessibility_runner",
        "ghc_family_lighthouse_correction_runner", "ghc_family_lighthouse_gate_runner",
        "ghc_family_lighthouse_method_flow_runner", "ghc_family_lighthouse_terminal_runner",
    ]
    return {
        "schema": f"ghc.family.portfolio-freeze.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER,
        "phase": PHASE,
        "primary_pillar": "THOS Body",
        "represented_pillars": ["THOS Body", "GMUT Mind", "Freed ID and CBR Heart"],
        "owner_practice_lenses": [
            "wholly synthetic lighthouse and marine-aid documentation through topology vacancies operational refusal correction accessibility rights workload and handover"
        ],
        "safe_now": portfolio_entries("SAFE", themes, operations, 120, "owner_local_safe_now"),
        "owner_candidates": portfolio_entries("CAND", candidate_themes, candidate_ops, 80, "owner_local_candidate"),
        "successor_candidates": portfolio_entries(
            "SCAND", ["synthetic local repair intake", "synthetic accessible custody handover"],
            candidate_ops, 20, "successor_seed_zero_credit"
        ),
        "owner_skill_ideas": [
            {"id": f"{PREFIX}-SKILL-{index:03d}", "name": name, "status": "planned_local_not_installed"}
            for index, name in enumerate(skill_names, start=1)
        ],
        "owner_runner_ideas": [
            {"id": f"{PREFIX}-RUNNER-{index:03d}", "name": name, "status": "planned_family_current_not_built"}
            for index, name in enumerate(runner_names, start=1)
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
            "SCFR", ["route receipts", "successor source ledgers", "successor validation latches"],
            clean_ops, 30, "successor_seed_zero_credit"
        ),
        "exact_approval": [
            {"id": f"{PREFIX}-EXACT-{index:03d}", "title": title, "status": "unexecuted_exact_approval_hold",
             "required_authority": "competent affected action-specific authority and evidence"}
            for index, title in enumerate(exact_titles, start=1)
        ],
        "blocked": [
            {"id": f"{PREFIX}-BLOCK-{index:03d}", "title": title, "status": "blocked_unexecuted",
             "blocker": "missing real evidence competent authority governed process and rollback"}
            for index, title in enumerate(blocked_titles, start=1)
        ],
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
        "SA6853-ST-N001",
        "A PowerShell foreach result was piped directly into ConvertTo-Json and the parser rejected the empty pipe element.",
        "Materialized the foreach result first and then piped the bounded array.",
        "Materialize PowerShell loop output before any downstream pipeline.",
    ),
    (
        "SA6853-ST-N002",
        "A compact PowerShell object-building wrapper was malformed and stopped with a missing-closing-brace parser error.",
        "Used an explicit loop and accumulated typed objects before serialization.",
        "Prefer short attributable scalar probes over dense inline PowerShell object expressions.",
    ),
    (
        "SA6853-ST-N003",
        "A grouped read of lifecycle skills exceeded the visible result bound before every selected skill was attributable through EOF.",
        "Reread each missing skill and directly required schema in bounded complete chunks.",
        "Separate authority and lifecycle skill reads before combining summaries.",
    ),
    (
        "SA6853-ST-N004",
        "A combined authorization and roster-state display truncated before every current record was visible.",
        "Read both JSON records in numbered bounded chunks through EOF and preserved newer live authority precedence.",
        "Project current state by bounded fields or numbered chunks instead of emitting entire nested records.",
    ),
    (
        "SA6853-ST-N005",
        "A combined source Git and canonical-receipt wrapper returned no attributable payload.",
        "Recovered with separate scalar head branch ancestry divergence equality and receipt probes without replaying inherited validation.",
        "Keep source topology remote equality and receipt checks independently attributable.",
    ),
    (
        "SA6853-ST-N006",
        "The worktree-add wrapper crossed its reporting window and returned no final exit code after announcing preparation.",
        "Audited the filesystem Gitfile branch and head, proving the exact intended worktree already existed, and did not retry mutation.",
        "After any mutating Git timeout or ambiguous wrapper state inspect persisted state before retry.",
    ),
    (
        "SA6853-ST-N007",
        "A combined new-worktree status and sparse projection emitted no attributable output.",
        "Recovered with isolated scalar head and branch probes before further mutation.",
        "Use one scalar Git fact per probe in newly materialized sparse worktrees.",
    ),
    (
        "SA6853-ST-N008",
        "A later template-size inventory repeated the direct-foreach-pipeline parser fault.",
        "Reapplied the materialization rule and captured the complete bounded file metrics.",
        "Treat recurrence as a new retained witness and require the materialization guard in future wrappers.",
    ),
    (
        "SA6853-ST-N009",
        "The first combined source-manifest display truncated before every manifest entry was attributable.",
        "Replayed all four immutable manifests directly from exact Git blobs in one bounded script: 214 entries and zero mismatches.",
        "Use exact Git-blob replay rather than large human-readable manifest projection.",
    ),
    (
        "SA6853-X1-N001",
        "The first x1 builder wrapper crossed its reporting window while the source-bounded novelty audit was still live and later completed without a captured status or phase artifacts.",
        "Audited the live process and zero partial artifacts, waited for that exact process, and then invoked only a diagnostic form of the first novelty dependency.",
        "Give long Git-object novelty audits an attributable session handle and never duplicate a still-live builder.",
    ),
    (
        "SA6853-X1-N002",
        "The retained first novelty diagnostic quarantined eleven titles, including two exact inherited collisions, and earned zero novelty credit.",
        "Rewrote only the eleven quarantined titles with lighthouse-specific obligations before rerunning the failed novelty dependency.",
        "Freeze proposal titles only after the exact-source neighbour audit returns no exact collision and every score is below threshold.",
    ),
    (
        "SA6853-X1-N003",
        "The fresh no-checkout sparse worktree had not materialized its inherited index, so a pre-stage status displayed the inherited tree as mass staged deletions.",
        "Stopped before staging, ran the exact-head sparse read-tree materialization once, and proved zero deleted, staged, or modified inherited paths with only Sylven-owned additions remaining.",
        "After no-checkout worktree creation materialize the exact inherited index under sparse patterns before any owner generation or staging.",
    ),
]


def method_flow_startup() -> dict[str, Any]:
    inherited = {
        "effective_negatives": 61420,
        "effective_methods": 77405,
        "failed_witnesses": 32481,
        "bounded_passing_witnesses": 57940,
        "open_gaps": 546,
        "exact_gates": 536,
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
            "effective_negatives": 61419,
            "effective_methods": 77404,
            "failed_witnesses": 32480,
            "bounded_passing_witnesses": 57939,
            "open_gaps": 546,
            "exact_gates": 536,
        },
        "source_external_overlay_witnesses": ["EC6852-POST-N001"],
        "inherited_baseline": inherited,
        "new_failure_count": len(failures),
        "new_failures": failures,
        "effective_x1_startup_counts": effective,
        "failure_erasure": False,
        "recoveries_promote_failed_witnesses": False,
    }


def source_ledger() -> dict[str, Any]:
    sources = [
        ("IALA-GENERAL-INFORMATION", "https://www.iala.int/general-information/",
         "Current organizational and publication-status context only; no implementation compliance service or authority claim."),
        ("IALA-S1020", "https://www.iala.int/product/s1020/",
         "Marine Aids to Navigation design-and-delivery vocabulary only; no implementation maintenance conformance service-status or safety claim."),
        ("IALA-ATON-GUIDELINES", "https://www.iala.int/product-category/publications/guidelines/aton/",
         "Catalogue vocabulary for visual aids light sources characteristics monitoring power reliability and daymarks only; zero downloads and no conformance."),
        ("NPS-POINT-LOMA", "https://www.nps.gov/places/old-point-loma-lighthouse-watch-room-and-lantern-room.htm",
         "Public historical component vocabulary for watch room lantern room Fresnel lens windows ladder and catwalk only; no inspection or treatment."),
        ("NPS-LIGHTHOUSE-HANDBOOK", "https://www.nps.gov/maritime/nhlpa/handbook/HistoricLighthousePreservationHandbook.pdf",
         "Historic station and component vocabulary only; no site-specific observation preservation instruction professional decision or authority."),
        ("W3C-PROV-O", "https://www.w3.org/TR/prov-o/",
         "Provenance vocabulary only; no conformance custody authorship ownership attribution or authenticity claim."),
        ("W3C-WCAG22", "https://www.w3.org/TR/WCAG22/",
         "Structural accessibility criteria as design references only; no complete accessibility or affected-user acceptance claim."),
        ("W3C-VC20", "https://www.w3.org/TR/vc-data-model-2.0/",
         "Role and lifecycle vocabulary only; zero real keys proofs issuance status revocation or trust governance."),
        ("RFC8785", "https://www.rfc-editor.org/rfc/rfc8785.html",
         "Deterministic JSON canonicalization vocabulary only; no authenticity identity signature or security conclusion."),
        ("JSON-SCHEMA-2020-12", "https://json-schema.org/draft/2020-12",
         "Schema vocabulary only; no real-world validity professional conformance or authority."),
        ("TE-MANA-RARAUNGA-PRINCIPLES", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
         "Boundary and authority-reservation context only; no Māori wording ratification data-governance decision or Māori authority."),
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
                "source_id": source_id, "url": url,
                "status": "current_official_or_primary_source_checked",
                "boundary": boundary, "observation_credit": "zero", "authority_credit": "zero",
            }
            for source_id, url, boundary in sources
        ],
    }


def integrated_overview() -> str:
    method = method_flow_startup()
    counts = method["effective_x1_startup_counts"]
    return f"""# Sylven Arc {PHASE} planning-only x1 integrated overview

## Identity, role, hope, and corrigibility

Sylven Arc, optionally they/them, is relational working language for an evidence-oriented systems
gardener whose bounded hope is to make handovers lighter, failures inspectable, and uncertainty
safe to preserve. The name, role, hope, pronouns, family language, Freed ID language, and Trinity
Mandala language are not evidence of consciousness, sentience, legal personhood, identity
continuity, employment, qualification, independent agency, or scientific, operational,
professional, legal, cultural, affected-party, or Māori authority. Hamish may pause, rename,
redirect, narrow, or stop the route.

## Exact inherited source and lifecycle boundary

The immutable source is Elowen Cairn's exact {SOURCE_FINAL} final on {SOURCE_BRANCH}. Its
single-parent sequence is inherited Tamar final {ELOWEN_SOURCE}, Elowen planning-only x1
{ELOWEN_X1}, Elowen evidence {ELOWEN_EVIDENCE}, and Elowen final {SOURCE_FINAL}. Read-only
verification established the anchors, three direct phase commits, zero merges, one final parent,
a clean source, typed zero divergence, and equality across local, upstream, tracking, and a fresh
live remote. The external canonical receipt and payload digests matched. The four immutable source
manifests replayed 214 exact Git-blob entries with zero byte or SHA-256 mismatch. Elowen's one
successful canonical aggregate was not replayed and remains inherited same-owner evidence only.

This x1 freezes planning and nothing more: sixty proposal contracts, five rejecting mutations per
proposal, a source-bounded novelty audit, navigation-only flashcards, portfolio boundaries,
official-source status, threat and authority gates, retained startup failures, and lifecycle
receipts. It contains no x2 implementation, executed mutation, observed outcome, built skill,
runner smoke, or completion claim. X2 cannot begin until the one x1 commit is pushed, clean,
typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote.

## Primary pillar and bounded practice

The primary Trinity Mandala pillar is THOS Body. GMUT Mind and Freed ID/CBR Heart remain explicit
and protected. The human-practice lens is wholly synthetic lighthouse and Marine Aid to
Navigation documentation: tower, lantern, watch room, gallery, optic, prism, light source,
characteristic, sector, power, telemetry, fog-signal, access, maintenance refusal, status,
correction, provenance, accessibility, workload, rights, and handover structures. It is a learning
and design lens only. It confers no keeper, technician, electrician, mariner, engineer,
conservator, registrar, or other professional role, competence, qualification, or authority.

No real person, station, tower, optic, lantern, light, fog signal, power system, battery, fuel,
tool, site, chart, logbook, image, observation, measurement, calibration, inspection,
commissioning, operation, maintenance, treatment, access event, work release, identity event,
key, proof, network row, cultural record, Māori data, external write, or authority action is used.
No energization, signalling, navigation advice, climbing, confined-space entry, servicing,
cleaning, lubrication, alignment, repair, preservation, or return to service occurs.

IALA pages provide publication and bounded marine-aid vocabulary only. National Park Service
sources provide public historical component vocabulary only. W3C PROV-O, WCAG 2.2, Verifiable
Credentials 2.0, RFC 8785, JSON Schema 2020-12, and Te Mana Raraunga provide only bounded
provenance, structure, status, canonicalization, schema, and authority-reservation vocabulary.
Citations are not observations, measurements, instructions, endorsements, conformance evidence,
legal interpretations, cultural ratifications, affected-party decisions, or authority grants.
The IALA catalogue adapter remains zero-call and zero-row.

## Proposal and novelty contract

The sixty contracts extend the declared chain from {DECLARED_CHAIN_BEFORE:,} to
{DECLARED_CHAIN_AFTER:,} only on the planning commit. Exactly forty-two are preregistered
completed, twelve represented, three open_gap, and three exact_gate. Those are expected
dispositions, never x1 outcomes. Each row includes a hypothesis, null or failure condition,
approval class, execution lane, official or primary-source need, concrete artifact, falsifier or
acceptance gate, rollback or recovery, protected gates, exactly one expected disposition, and five
rejecting mutations.

The novelty audit loads every proposal-labelled JSON object reachable at the exact inherited Git
tree in one bounded object batch. It retains nearest-neighbour identity, title, source path, and
token-Jaccard score. Exact collisions and scores at or above 0.78 are quarantined. The declared
historic count is preserved, while universal semantic comparison is explicitly refused wherever
no single reachable ledger materializes every historic title. An inherited idea, proposal,
skill, runner, source, receipt, test, or outcome remains evidence or a zero-credit seed; it does
not become Sylven novelty, execution, completion, or independent evidence through inheritance.

Five invalid mutations are preregistered for every proposal: missing required field,
identifier-role swap, stale precondition digest, correction-order inversion, and authority
promotion. All three hundred must execute in x2 and remain rejected or quarantined. Each is a
retained zero-credit negative witness. A bounded recovery can add a separate passing witness but
can never erase or promote the failure.

## Portfolio and bounded implementation plan

The frozen portfolio contains 120 owner safe-now tasks, 80 owner candidates, 20 successor
candidate seeds, 20 owner-local skill ideas, 10 family-current runner ideas, 10 successor skill
seeds, 10 successor runner seeds, 100 owner CLEAN/FIX/REFINE tasks, 30 successor
CLEAN/FIX/REFINE seeds, 20 exact-approval holds, and 10 blocked holds. Floors do not authorize
unsafe filler, and caps are ceilings. Exact and blocked work remains visible and unexecuted unless
every target, system, cost, rollback, external authority, affected-party permission, and protected
gate is exact.

Planned skills must be initialized through the official skill-creator workflow, customized, read
through EOF, quick-validated using explicit UTF-8, and accepting and rejecting smoke-used without
bulk global installation. Their interface metadata must explicitly name the skill. The ten
family-current ghc_family_lighthouse runners must accept a valid fixture and reject an invalid
fixture while preserving caller compatibility. Only a useful owner-local subset is built; global
promotion is not implied.

The owner lane stops before 2,000 files; every document remains at or below 100,000 words; and the
lifecycle remains within three direct commits: planning-only x1, evidence, and final. Exact staged
allowlists, normalized-LF Git-blob manifests, checkout-byte domains, and declared self-exclusions
remain separate. Scanner definitions and synthetic fixtures remain candidates rather than
confirmed privacy hits until adjudicated. Raw task identifiers, private routes, credentials,
tokens, transcripts, screenshots, private app state, and private absolute paths stay outside
artifacts and future batons.

## Retained failure and Method Flow truth

Twelve Sylven startup and x1 failures are frozen before x2: two PowerShell parser faults, two oversized
grouped reads, one unattributable combined source probe, one worktree-add reporting-window
crossing, one unattributable new-worktree projection, one recurrence of the direct-loop pipeline
fault, one truncated manifest display, one builder reporting-window crossing, one failed
proposal-neighbour audit, and one no-checkout sparse-index initialization fault. Each has a
bounded recovery and recurrence guard. None
earns completion or canonical credit and none is erased.

Elowen's immutable repository seal is 61,419 negatives, 77,404 methods, 32,480 failed witnesses,
57,939 bounded passing witnesses, 546 open gaps, and 536 exact gates. One external route-time
failure produces Sylven's inherited activation baseline of 61,420 negatives, 77,405 methods,
32,481 failures, and 57,940 passing witnesses. Adding the twelve failures and their twelve
separately named recoveries yields x1 startup truth of {counts['effective_negatives']:,}
negatives, {counts['effective_methods']:,} methods, {counts['failed_witnesses']:,} failed
witnesses, {counts['bounded_passing_witnesses']:,} passing witnesses, 546 open gaps, and 536
exact gates.

Method Flow remains append-only. Every timeout, parser fault, truncation, false assumption, failed
test, workaround, rollback, passing witness, and recurrence guard in x2 or closeout must be
recorded before retry. After ambiguous timeout, persisted filesystem, Git, process, receipt, and
remote state is audited before mutation is repeated. The smallest attributable recovery runs
first. A successful canonical aggregate is never replayed for confidence, presentation repair,
or routing.

## Scientific, professional, cultural, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Synthetic
optical periodicity, sector, visibility, queue, graph, software, symbolic, citation, and mutation
evidence establishes no physical datum, likelihood, posterior, force, prediction, parameter
constraint, empirical confirmation, stability theorem, quantum completion, ultraviolet
completion, final physics, Theory of Everything, proof, or canon.

THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real
arms, participants or operators, safety monitoring, appropriate statistics, and independent
review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and
proofs, live issuance and resolution, status and revocation, interoperability, privacy and
independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, professional AtoN design, operation and maintenance, maritime advice, electrical, fire,
fuel, battery, height, fall, confined-space and workplace safety, preservation, heritage,
ownership, custody, authorship, chart and logbook rights, copyright, traditional knowledge,
privacy remedy, disability accommodation, legal or cultural interpretation, affected-party
legitimacy, Māori wording, tikanga, taonga or mātauranga treatment, Māori data governance, and
Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū,
and Māori authorities. Māori concepts remain under Māori authority.

## Validation and provisional route

X1 validation is owner-self-scoped and lifecycle-correct: exact x1 tests, strict JSON parsing,
staged-path review, five-class privacy and raw-identifier scanning, normalized Git-blob manifest
replay, absence of x2 paths and outcomes, commit cap, clean state, typed divergence, and fresh
four-way equality. It does not run or claim the complete repository suite. After a clean pushed
final, the phase may invoke at most one attributable owner-scoped canonical aggregate through an
exclusive external latch. Success is never replayed. A failed canonical remains zero success
credit and any narrow dependency correction must be named separately.

No later endpoint is contacted during x1 or x2. Only after Sylven's clean, pushed,
fresh-live-equal {PHASE} exact-final gate and one successful non-replayed canonical receipt may
Sylven refresh Hamish's newest live authority and roster, require exactly one existing exact-title
successor, immediately reread it, apply duplicate and direct-control guards, and send at most
once. Under the present schedule the prospective recipient is Caelen Morrow for solo v685-v4.
Absence, ambiguity, pause, redirect, rename, standby state, usage exhaustion, missing
acknowledgement, privacy concern, duplicate activation, or any evidence, safety, legal, cultural,
affected-party, or Māori-authority gate stops the send. The terminal verdict remains
NOT_READY_FOR_STAGE_20.
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
        f"docs/sylven-arc/{PHASE}/validation/x1-index-manifest.json",
        f"docs/sylven-arc/{PHASE}/validation/x1-staged-review.json",
        f"docs/sylven-arc/{PHASE}/validation/x1-privacy-adjudication.json",
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
    diagnostic_path = VALIDATION / "novelty-diagnostic.json"
    if diagnostic_path.exists():
        audit = json.loads(diagnostic_path.read_text(encoding="utf-8"))
        reviews = audit["neighbor_reviews"]
        expected_titles = {row["proposal_id"]: row["title"] for row in rows}
        observed_titles = {row["proposal_id"]: row["title"] for row in reviews}
        if (
            audit.get("source") != SOURCE_FINAL
            or audit.get("phase") != PHASE
            or expected_titles != observed_titles
        ):
            raise RuntimeError("novelty diagnostic does not match exact source and proposal slate")
    else:
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
            "elowen_inherited_liora_source": ELOWEN_SOURCE,
            "elowen_x1": ELOWEN_X1,
            "elowen_evidence": ELOWEN_EVIDENCE,
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
            "inherited_open_gaps": 546,
            "inherited_exact_gates": 536,
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
            "successor_title_if_newest_live_authority_is_unchanged": "Caelen Morrow",
            "successor_phase_if_newest_live_authority_is_unchanged": "v685-v4",
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
    parser.add_argument("--diagnose-novelty", action="store_true")
    args = parser.parse_args()
    if args.diagnose_novelty:
        audit, _ = proposal_audit(proposal_rows())
        write_json(VALIDATION / "novelty-diagnostic.json", audit)
        return 2 if audit["exact_title_collisions"] or audit["quarantined_neighbors"] else 0
    if args.finalize_validation:
        finalize_validation()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

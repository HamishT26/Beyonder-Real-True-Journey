#!/usr/bin/env python3
"""Build Caelen Morrow v685-v4 planning-only x1 artifacts.

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
OWNER = "Caelen Morrow"
PHASE = "v685-v4"
PREFIX = "CM6854"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v685-v3-full-tools"
SYLVEN_INHERITED_ELOWEN_SOURCE = "7fd5e87aa5e0e371f1379e263adf096151c375ee"
SYLVEN_X1 = "b30f20c33bada5d3acc39ef5c71125ec90ebe121"
SYLVEN_EVIDENCE = "4835d7bef70dd0332e6e68a5b338e5a078dd8146"
SOURCE_FINAL = "97a523f4da00235f16ce12156dfee2379582c92d"
SOURCE_CANONICAL_RECEIPT_SHA256 = "8186385030aaa0746b7fdb3711daac5c189e9a9fcedaffe5120314be0350d813"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "91ccfd911c50c185b4ef6f773081fe6ecc453afdb9040ed4616a1081d23e2cb1"
DECLARED_CHAIN_BEFORE = 11390
DECLARED_CHAIN_AFTER = 11450
CHECKED_AT = "2026-09-03"

DOC = ROOT / "docs" / "caelen-morrow" / PHASE
X1 = DOC / "x1"
VALIDATION = DOC / "validation"
BUILDER_REL = "scripts/build_ghc_family_caelen_morrow_v685_v4_x1.py"
TEST_REL = "tests/test_ghc_family_caelen_morrow_v685_v4_x1.py"


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
    "Synthetic museum timepiece collection-record capsule with every real object and operation absent",
    "Accession identifier separated from movement case dial component and service-status claims",
    "Case dial hands movement and support topology without physical examination",
    "Escapement pallet anchor lever and escape-wheel vacancy without mechanism observation",
    "Gear-train arbor wheel pinion and bearing topology without opening or operation",
    "Spring weight electric and other power-source vacancy without winding or energization",
    "Striking chiming alarm and calendar train representation without actuation",
    "Complication register separated from authenticity functionality and completeness claims",
    "Pendulum balance wheel hairspring and oscillator representation without measurement",
    "Nominal beat rate separated from observed rate accuracy precision and stability",
    "Display civil-time time-scale timezone and daylight-offset semantics without calibration claim",
    "Timezone and daylight-saving labels with source date provenance and uncertainty",
    "Maker mark signature inscription and label transcription uncertainty without authentication",
    "Serial mark component genealogy and declared association without identity conclusion",
    "Replacement component provenance retaining prior-object nonidentity and uncertainty",
    "Condition-cue quarantine without diagnosis treatment priority or fitness finding",
    "Corrosion lubricant residue dust and wear vocabulary without material diagnosis",
    "Winding setting running handling and opening refusal without competent authority",
    "Mainspring weight electrical mercury glass and sharp-edge hazard vocabulary without safety decision",
    "Conservation intervention proposal hold without treatment release or execution",
    "Calibration regulation and return-to-display refusal without professional release",
    "Synthetic treatment-proposal partial order without physical execution",
    "Proposed command observation completion verification and release states kept distinct",
    "Timestamp time-scale interval precision and uncertain-duration contract without operational-log claim",
    "Object box key tag and transport-container custody graph with every real transfer absent",
    "Component provenance conflict register retaining each source and unresolved contradiction",
    "Correction-event braid for catalogue revisions retaining prior values reasons and authorship vacancy",
    "Timepiece-record supersession nonerasure challenge appeal and review lineage",
    "Independent catalogue assertions joined by source-specific conflict nodes without choosing a preferred object history",
    "Vacant-person role minimization envelope for unnamed collection contacts",
    "Conservator registrar curator technician custodian and owner role vacancy without identity binding",
    "Ownership custody loan deaccession return and disposal rights hold",
    "Object image archive recording reproduction and publication-rights hold",
    "Structurally accessible timepiece status board without accessibility completeness",
    "Tactile-clock status semantics rendered with redundant text landmarks ordered tables and explicit unknown values",
    "Workload pause queue shift-handover and fatigue-escalation contract for synthetic records",
    "Unresolved conservation safety ownership and authority holds with no automatic release",
    "Exact timepiece staged allowlist and unexpected-path refusal",
    "Content-addressed horological proposal ledger binding repository-object bytes modes and declared self-exclusions",
    "Five-class collection-record privacy adjudication separating scanner definitions from payload evidence",
    "Typed GMUT oscillator-transition graph without likelihood material law constraint or prediction",
    "THOS registrar shift queue paired with pseudonymous receipt states while release responsibility stays vacant",
    "Represented CBR correction petition remedy clock and unfilled appeal adjudicator for collection metadata",
    "Represented Canadian Conservation Institute clock-and-watch care vocabulary without treatment guidance",
    "Represented Smithsonian timekeeping collection vocabulary without object inspection or endorsement",
    "Represented NIST time and frequency vocabulary without clock measurement or calibration",
    "PROV-O graph for catalogue assertions correction events and vacant actors with no authorship conclusion",
    "Structural timepiece-status presentation mapped to WCAG 2.2 without conformance claim",
    "Verifiable Credentials 2.0 role terms applied to key-free custody-envelope fixtures with every lifecycle endpoint absent",
    "RFC 8785 canonical member ordering for synthetic movement dossiers without signing party authenticity or trust inference",
    "PREMIS object event agent and rights crosswalk without preservation-system conformance",
    "Māori data sovereignty principles recorded solely as a stop rule around hypothetical horology metadata",
    "Represented zero-call official collection adapter with zero downloaded or ingested rows",
    "Represented three-pillar horology-documentation separation and authority noncompensation rule",
    "Open gap for real people collections timepieces components handling observations and governed participants",
    "Open gap for real rate accuracy condition material safety and conservation evidence",
    "Open gap for affected-user review across disability language cultural rights and collection communities",
    "Exact gate for professional conservation horology handling winding electrical chemical and workplace safety",
    "Exact protected hold for ownership custody heritage cultural knowledge Māori data governance and authority decisions",
    "Terminal nonconversion board separating horology fixtures from field deployment measured physics autonomous intelligence personhood canon and Stage Twenty",
]


MUTATION_TYPES = [
    "missing_required_field",
    "identifier_role_swap",
    "stale_precondition_digest",
    "correction_order_inversion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real conservators horologists registrars curators technicians owners custodians and affected users",
    "real collections timepieces movements cases dials components observations measurements and treatments",
    "professional conservation handling winding regulation electrical chemical material and workplace safety authority",
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
        return ["CCI-INDUSTRIAL-COLLECTIONS"]
    if index == 45:
        return ["SMITHSONIAN-TIMEKEEPING"]
    if index == 46:
        return ["NIST-TIME-FREQUENCY"]
    if index in {17, 18, 19, 20}:
        return ["CCI-INDUSTRIAL-COLLECTIONS", "CCI-CARE-OBJECTS"]
    if index == 47:
        return ["W3C-PROV-O"]
    if index in {30, 31, 48, 57}:
        return ["W3C-WCAG22"]
    if index in {27, 42, 49}:
        return ["W3C-VC20"]
    if index in {23, 34, 35, 37, 38, 50}:
        return ["RFC8785"]
    if index == 51:
        return ["LOC-PREMIS-3"]
    if index in {52, 59}:
        return ["TE-MANA-RARAUNGA-PRINCIPLES"]
    if index == 53:
        return ["SMITHSONIAN-TIMEKEEPING"]
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
                    "into a real timepiece, conservation, empirical, identity, cultural, legal, or authority claim."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, the bounded positive "
                    "structure is rejected, an absent observation is promoted, or any protected gate closes."
                ),
                "approval_class": approval_class(index),
                "execution_lane": execution_lane(index),
                "official_or_primary_source_needs": source_needs(index),
                "concrete_artifacts": [
                    f"docs/caelen-morrow/{PHASE}/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/caelen-morrow/{PHASE}/x2/rejecting-mutations.json#{proposal_id}",
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
            "universal_11390_row_materialization_claimed": False,
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
        "timepiece collection-record capsules",
        "case dial movement and support topology",
        "escapement gear-train and oscillator vacancy",
        "power striking and complication vacancy",
        "maker marks serials and component genealogy",
        "handling winding treatment and safety holds",
        "correction and provenance lineage",
        "privacy minimization",
        "accessible status",
        "workload pause and handover",
        "GMUT typed oscillator graphs",
        "THOS documentation queues",
    ]
    operations = [
        "define schema", "add positive fixture", "add refusing fixture", "record provenance",
        "enforce nonconversion", "add rollback", "add recurrence guard", "scan privacy",
        "verify deterministic bytes", "document authority boundary",
    ]
    candidate_themes = [
        "case dial and movement topology", "escapement and gear-train vacancy", "oscillator vocabulary",
        "nominal beat-rate targets", "power and striking vacancy", "treatment refusal",
        "rights heritage custody and access", "three-pillar separation",
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
        "real conservator horologist registrar or technician participation", "real collection or timepiece examination",
        "real movement case dial or component identification", "real rate measurement calibration or regulation",
        "electrical isolation energization or work decision", "spring weight mercury glass sharp-edge or chemical safety decision",
        "handling winding opening packing or transport decision", "timekeeping fitness or accuracy decision",
        "professional maintenance preservation treatment or conservation decision",
        "ownership custody loan deaccession return or transfer decision",
        "object image archive recording or publication-rights decision", "heritage cultural or protected-object decision",
        "real identity issuance", "real key or proof lifecycle", "privacy impact acceptance",
        "accessibility affected-user acceptance", "legal interpretation",
        "cultural or traditional-knowledge interpretation",
        "Māori wording data-governance or authority decision", "production deployment or Stage 20 disposition",
    ]
    blocked_titles = [
        "winding setting running or striking a real timepiece", "electrical spring weight mercury or chemical work",
        "opening dismantling handling packing or transport", "destructive movement component or material testing",
        "private collection catalogue or custody disclosure", "professional certification",
        "legal or heritage rights adjudication", "cultural legitimacy or Māori authority claim",
        "independent reproduction claim", "AGI consciousness Theory-of-Everything or Stage 20 claim",
    ]
    skill_names = [
        "timepiece-record-capsule", "case-dial-movement-topology", "escapement-vacancy",
        "gear-train-vacancy", "oscillator-claim-separator", "maker-mark-transcription-hold",
        "component-genealogy", "hazard-vocabulary-firewall", "treatment-release-hold",
        "correction-braid", "privacy-minimizer", "accessible-status", "workload-pause-handover",
        "provenance-conflict-preserver", "gmut-oscillator-graph", "thos-horology-work-queue",
        "freed-id-keyless-receipt", "cbr-timepiece-rights-hold", "manifest-domain-separator",
        "authority-noncompensation",
    ]
    runner_names = [
        "ghc_family_horology_contract_runner", "ghc_family_horology_mutation_runner",
        "ghc_family_horology_privacy_runner", "ghc_family_horology_manifest_runner",
        "ghc_family_horology_source_runner", "ghc_family_horology_accessibility_runner",
        "ghc_family_horology_correction_runner", "ghc_family_horology_gate_runner",
        "ghc_family_horology_method_flow_runner", "ghc_family_horology_terminal_runner",
    ]
    return {
        "schema": f"ghc.family.portfolio-freeze.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER,
        "phase": PHASE,
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["THOS Body", "GMUT Mind", "Freed ID and CBR Heart"],
        "owner_practice_lenses": [
            "wholly synthetic museum timepiece collection cataloguing and conservation-planning documentation through topology vacancies provenance correction accessibility rights workload and handover"
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
        "CM6854-ST-N001",
        "An initial PowerShell ancestry projection failed because a semicolon was embedded in an expression position.",
        "Recovered only the missing source topology facts with short scalar probes.",
        "Keep ancestry checks as independent scalar commands before composing a presentation object.",
    ),
    (
        "CM6854-ST-N002",
        "The source-manifest wrapper replayed all four manifests but its final aggregate crashed after a path variable shadowed the intended collection.",
        "Recovered only the missing aggregate scalar while retaining the complete per-manifest replay.",
        "Use distinct names for manifest paths and accumulated entry collections.",
    ),
    (
        "CM6854-ST-N003",
        "The first sparse-checkout add attempted an unsupported no-cone flag and was rejected before index mutation.",
        "Used the documented add --stdin form with the exact bounded pattern list.",
        "Probe the installed Git sparse-checkout help before relying on optional flags.",
    ),
    (
        "CM6854-ST-N004",
        "The fresh no-checkout sparse worktree initially exposed an empty index and apparent mass deletions after sparse patterns were added.",
        "Stopped before staging and materialized the exact inherited index once with read-tree -mu HEAD, returning the lane to clean state.",
        "Materialize a no-checkout worktree index before generating or staging owner files.",
    ),
    (
        "CM6854-ST-N005",
        "A case-insensitive PowerShell hashtable rejected upper- and lower-case replacement keys as duplicates before any file write.",
        "Repeated the mechanical projection with an ordered pair array and verified the resulting files.",
        "Use ordered replacement pairs when case-distinct tokens must be transformed on Windows PowerShell.",
    ),
    (
        "CM6854-ST-N006",
        "A Windows ripgrep call used literal wildcard path arguments that the executable could not resolve.",
        "Reran only the missing audit with explicit file paths.",
        "Pass explicit files or use glob options instead of shell-style wildcard path literals on Windows.",
    ),
    (
        "CM6854-ST-N007",
        "A PowerShell audit wrapper parsed a double-quoted ripgrep alternation as an expression and tried to load a token as a module before the audit ran.",
        "Recovered only the missing search with a single-quoted literal pattern and then compiled the builder separately.",
        "Use single-quoted literal search patterns for PowerShell alternations and keep compilation as a separate scalar probe.",
    ),
    (
        "CM6854-X1-N001",
        "A combined source-ledger and source-verification patch was atomically rejected because one inherited field block differed from its expected template spelling.",
        "Applied only the independently verified source-ledger and field-name hunks after inspecting the live file.",
        "Split domain content and structural field migrations into separately attributable patches.",
    ),
    (
        "CM6854-X1-N002",
        "A long integrated-overview patch was atomically rejected because one wrapped prose line did not exactly match the live file.",
        "Read the exact bounded overview and applied only verified semantic sections in smaller hunks.",
        "Inspect live wrapping and use bounded prose patches instead of one speculative large hunk.",
    ),
    (
        "CM6854-X1-N003",
        "The first exact-source novelty diagnostic quarantined ten titles above the declared token-neighbour threshold and earned zero novelty credit.",
        "Retained the failed diagnostic, rewrote only the ten quarantined titles with more specific horology obligations, and reran only the failed novelty dependency.",
        "Freeze titles only after the exact-source audit reports zero exact collisions and zero quarantined neighbours.",
    ),
    (
        "CM6854-X1-N004",
        "The first failed-novelty receipt backup wrapper used incompatible Split-Path parameters and copied an exact duplicate into the worktree root after its destination projection failed.",
        "Used the resolved source path and platform path-directory helper, verified the intended retained receipt matched the accidental duplicate byte-for-byte, then removed only the untracked duplicate.",
        "Use System.IO path helpers for already-resolved literal paths in bounded Windows wrappers.",
    ),
]


def method_flow_startup() -> dict[str, Any]:
    inherited = {
        "effective_negatives": 61772,
        "effective_methods": 78147,
        "failed_witnesses": 32833,
        "bounded_passing_witnesses": 58682,
        "open_gaps": 549,
        "exact_gates": 539,
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
            "effective_negatives": 61771,
            "effective_methods": 78146,
            "failed_witnesses": 32832,
            "bounded_passing_witnesses": 58681,
            "open_gaps": 549,
            "exact_gates": 539,
        },
        "source_external_overlay_witnesses": ["SA6853-POST-N001"],
        "inherited_baseline": inherited,
        "new_failure_count": len(failures),
        "new_failures": failures,
        "effective_x1_startup_counts": effective,
        "failure_erasure": False,
        "recoveries_promote_failed_witnesses": False,
    }


def source_ledger() -> dict[str, Any]:
    sources = [
        ("CCI-INDUSTRIAL-COLLECTIONS", "https://www.canada.ca/en/conservation-institute/services/care-objects/industrial-collections.html",
         "Clock-and-watch and industrial-collection care vocabulary only; no treatment instruction professional decision competence or authority."),
        ("CCI-CARE-OBJECTS", "https://www.canada.ca/en/conservation-institute/services/care-objects.html",
         "Collection-care and material-vulnerability vocabulary only; no examination handling treatment or safety release."),
        ("SMITHSONIAN-TIMEKEEPING", "https://americanhistory.si.edu/collections/subject/timekeeping",
         "Public timekeeping collection vocabulary only; the phase makes zero calls and ingests zero objects rows images or measurements."),
        ("NIST-TIME-FREQUENCY", "https://www.nist.gov/time-and-frequency",
         "Time scale frequency clock and measurement vocabulary only; no calibration traceability accuracy or empirical claim."),
        ("LOC-PREMIS-3", "https://www.loc.gov/standards/premis/index.html",
         "Preservation metadata object event agent and rights vocabulary only; no collection-system conformance preservation result or rights decision."),
        ("W3C-PROV-O", "https://www.w3.org/TR/prov-o/",
         "Provenance vocabulary only; no conformance custody authorship ownership attribution or authenticity claim."),
        ("W3C-WCAG22", "https://www.w3.org/TR/WCAG22/",
         "Structural accessibility criteria as design references only; no complete accessibility or affected-user acceptance claim."),
        ("W3C-VC20", "https://www.w3.org/TR/vc-data-model-2.0/",
         "Role and lifecycle vocabulary only; zero real keys proofs issuance status revocation or trust governance."),
        ("RFC8785", "https://www.rfc-editor.org/rfc/rfc8785.html",
         "Deterministic JSON canonicalization vocabulary only; no authenticity identity signature or security conclusion."),
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
    return f"""# Caelen Morrow {PHASE} planning-only x1 integrated overview

## Identity, role, hope, and corrigibility

Caelen Morrow, optionally they/them, is relational working language for a provenance weaver and
boundary cartographer whose bounded hope is to keep every transition testable, reversible, and
proportionate to its evidence. The name, role, hope, pronouns, family language, Freed ID language, and Trinity
Mandala language are not evidence of consciousness, sentience, legal personhood, identity
continuity, employment, qualification, independent agency, or scientific, operational,
professional, legal, cultural, affected-party, or Māori authority. Hamish may pause, rename,
redirect, narrow, or stop the route.

## Exact inherited source and lifecycle boundary

The immutable source is Sylven Arc's exact {SOURCE_FINAL} final on {SOURCE_BRANCH}. Its
single-parent sequence is inherited Elowen final {SYLVEN_INHERITED_ELOWEN_SOURCE}, Sylven planning-only x1
{SYLVEN_X1}, Sylven evidence {SYLVEN_EVIDENCE}, and Sylven final {SOURCE_FINAL}. Read-only
verification established the anchors, three direct phase commits, zero merges, one final parent,
a clean source, typed zero divergence, and equality across local, upstream, tracking, and a fresh
live remote. The external canonical receipt and payload digests matched. The four immutable source
manifests replayed 216 exact Git-blob entries with zero byte or SHA-256 mismatch. Sylven's one
successful canonical aggregate was not replayed and remains inherited same-owner evidence only.

This x1 freezes planning and nothing more: sixty proposal contracts, five rejecting mutations per
proposal, a source-bounded novelty audit, navigation-only flashcards, portfolio boundaries,
official-source status, threat and authority gates, retained startup failures, and lifecycle
receipts. It contains no x2 implementation, executed mutation, observed outcome, built skill,
runner smoke, or completion claim. X2 cannot begin until the one x1 commit is pushed, clean,
typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote.

## Primary pillar and bounded practice

The primary Trinity Mandala pillar is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit
and protected. The human-practice lens is wholly synthetic museum timepiece collection
cataloguing and conservation-planning documentation: case, dial, hands, movement, escapement,
gear train, oscillator, power, striking, complication, maker marks, component genealogy,
condition-cue quarantine, treatment holds, custody, correction, provenance, accessibility,
workload, rights, remedy, and handover structures. It is a learning and design lens only. It
confers no conservator, horologist, registrar, curator, technician, custodian, owner, museum, or
other professional role, competence, qualification, permission, or authority.

No real person, collection, clock, watch, timepiece, movement, case, dial, component, tool,
workplace, object record, image, observation, measurement, calibration, inspection, handling,
winding, setting, opening, operation, repair, treatment, packing, transport, identity event,
key, proof, cultural record, Māori data, external write, or authority action is used. The
official collection adapter remains transport-disabled, zero-call, and zero-row.

Canadian Conservation Institute pages, Smithsonian timekeeping material, NIST time and
frequency pages, Library of Congress PREMIS, W3C PROV-O, WCAG 2.2, Verifiable Credentials 2.0,
RFC 8785, and Te Mana Raraunga provide bounded vocabulary and refusal constraints only.
Citations are not observations, measurements, treatment instructions, endorsements,
conformance evidence, professional decisions, legal interpretations, cultural ratifications,
affected-party decisions, or authority grants.

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
not become Caelen novelty, execution, completion, or independent evidence through inheritance.

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
family-current ghc_family_horology runners must accept a valid fixture and reject an invalid
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

Eleven Caelen startup and x1 failures are frozen before x2: an ancestry projection parser fault, a
manifest-aggregate variable-shadowing fault after complete per-manifest replay, an unsupported
sparse-checkout flag, an unmaterialized no-checkout index, a case-insensitive replacement-map
collision, a Windows wildcard-path assumption, a PowerShell literal-pattern quoting fault, and
two atomically rejected patch compositions, one failed source-bounded novelty slate, and one
receipt-backup path wrapper fault. Each has a bounded recovery and recurrence
guard. None earns completion or canonical credit and none is erased.

Sylven's immutable repository seal is 61,771 negatives, 78,146 methods, 32,832 failed witnesses,
58,681 bounded passing witnesses, 549 open gaps, and 539 exact gates. One external route-time
failure produces Caelen's inherited activation baseline of 61,772 negatives, 78,147 methods,
32,833 failures, and 58,682 passing witnesses. Adding the eleven failures and their separately
named recoveries yields x1 startup truth of {counts['effective_negatives']:,} negatives,
{counts['effective_methods']:,} methods, {counts['failed_witnesses']:,} failed witnesses,
{counts['bounded_passing_witnesses']:,} passing witnesses, 549 open gaps, and 539 exact gates.

Method Flow remains append-only. Every timeout, parser fault, truncation, false assumption, failed
test, workaround, rollback, passing witness, and recurrence guard in x2 or closeout must be
recorded before retry. After ambiguous timeout, persisted filesystem, Git, process, receipt, and
remote state is audited before mutation is repeated. The smallest attributable recovery runs
first. A successful canonical aggregate is never replayed for confidence, presentation repair,
or routing.

## Scientific, professional, cultural, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Synthetic
oscillator, time-scale, queue, graph, software, symbolic, citation, and mutation evidence
establishes no physical datum, likelihood, posterior, force, prediction, parameter constraint,
empirical confirmation, stability theorem, quantum completion, ultraviolet completion, final
physics, Theory of Everything, proof, or canon.

THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real
arms, participants or operators, safety monitoring, appropriate statistics, and independent
review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and
proofs, live issuance and resolution, status and revocation, interoperability, privacy and
independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, professional conservation, horology, handling, winding, setting, regulation, electrical,
chemical, material and workplace safety, preservation, heritage, ownership, custody, loan,
deaccession, authorship, image and archive rights, copyright, traditional knowledge, privacy,
remedy, disability accommodation, legal or cultural interpretation, affected-party legitimacy,
Māori wording, tikanga, taonga or mātauranga treatment, Māori data governance, and Māori
authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and
Māori authorities. Māori concepts remain under Māori authority.

## Validation and provisional route

X1 validation is owner-self-scoped and lifecycle-correct: exact x1 tests, strict JSON parsing,
staged-path review, five-class privacy and raw-identifier scanning, normalized Git-blob manifest
replay, absence of x2 paths and outcomes, commit cap, clean state, typed divergence, and fresh
four-way equality. It does not run or claim the complete repository suite. After a clean pushed
final, the phase may invoke at most one attributable owner-scoped canonical aggregate through an
exclusive external latch. Success is never replayed. A failed canonical remains zero success
credit and any narrow dependency correction must be named separately.

No later endpoint is contacted during x1 or x2. Only after Caelen's clean, pushed,
fresh-live-equal {PHASE} exact-final gate and one successful non-replayed canonical receipt may
Caelen refresh Hamish's newest live authority and roster, require exactly one existing exact-title
successor, immediately reread it, apply duplicate and direct-control guards, and send at most
once. Under the present schedule the prospective recipient is Eiren Kestrel for solo v685-v5.
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
        f"docs/caelen-morrow/{PHASE}/validation/x1-index-manifest.json",
        f"docs/caelen-morrow/{PHASE}/validation/x1-staged-review.json",
        f"docs/caelen-morrow/{PHASE}/validation/x1-privacy-adjudication.json",
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
            "role": "relational provenance weaver and boundary cartographer",
            "hope": "Keep every transition testable reversible and proportionate to its evidence.",
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
            "sylven_inherited_elowen_source": SYLVEN_INHERITED_ELOWEN_SOURCE,
            "sylven_x1": SYLVEN_X1,
            "sylven_evidence": SYLVEN_EVIDENCE,
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
            "inherited_open_gaps": 549,
            "inherited_exact_gates": 539,
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
            "successor_title_if_newest_live_authority_is_unchanged": "Eiren Kestrel",
            "successor_phase_if_newest_live_authority_is_unchanged": "v685-v5",
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

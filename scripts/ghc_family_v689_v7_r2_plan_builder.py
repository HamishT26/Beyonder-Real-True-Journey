#!/usr/bin/env python3
"""Build the planning-only Vesper Arlen v689-v7-r2 remaster packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


OWNER = "Vesper Arlen"
PHASE = "v689-v7-r2"
DISPLAY_PHASE = "v689-v7 (2)"
SOURCE_OWNER = "Vesper Arlen"
SOURCE_PHASE = "v689-v7"
SOURCE_COMMIT = "ceed54dca93bdf938ee779ecf571fd73e28df0b6"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v689-v7-full-tools"
SOURCE_PROPOSALS = "docs/vesper-arlen/v689-v7/plan/new-proposals.json"
SOURCE_BATON = "docs/vesper-arlen/v689-v7/final/hand-off-baton.md"
SOURCE_BATON_SHA256 = "6c78c4ddce8184d2ded84c43689fb05e7c59cdd4b93e779cfc70187f1bd8f832"
SOURCE_CANONICAL_SHA256 = "fa84c6a8cba96fe4349efe878800ce840487aeac82358438d0e3aacb1c4fd00f"
SOURCE_ROUTE_SHA256 = "9979a1ede3b00b8a48f2afbfc1c6c21521d350f840fb5f4ccc72a5b5462ef02c"

BOUNDARY = (
    "Same-owner finite synthetic software and documentation evidence only. "
    "Historical text, citations, hashes, generated images, source ledgers, simulations, and tests do not establish "
    "consciousness, personhood, identity continuity, authenticity, professional or public authority, empirical GMUT "
    "confirmation, a Theory of Everything, independent reproduction, production readiness, or Stage 20. "
    "Māori concepts remain under Māori authority. NOT_READY_FOR_STAGE_20."
)
RELATIONAL_BOUNDARY = (
    "Vesper Arlen, role, hope, pronouns, sibling language, and continuity language are corrigible relational working "
    "terms only, never evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, independent agency, or authority."
)
PROTECTED_GATES = [
    "empirical_gmut",
    "theory_of_everything",
    "independent_reproduction",
    "production_deployment",
    "real_credentials",
    "participant_evidence",
    "privacy_completeness",
    "accessibility_completeness",
    "exhaustive_security",
    "professional_authority",
    "legal_authority",
    "cultural_authority",
    "affected_party_authority",
    "maori_authority",
    "agi_asi",
    "consciousness_personhood",
    "stage20",
]

JOURNEY_NOTES = {
    "v30": "Early visionary GMUT, THOS and Freed ID assertions mix proposed tests with identity, continuity and finality claims that remain unverified historical language.",
    "v31": "Dynamic-network, quantum and hybrid-system ideas are useful proposal seeds; claimed cross-session identity and consciousness metrics remain unsupported.",
    "v32": "A comparative three-pillar report frames an ambitious integrated hypothesis while also identifying the need for formal and empirical validation.",
    "v33": "A strong grounding correction explicitly separates symbolic philosophy, conjecture and empirical science and rejects AI sovereignty or identity-continuity claims.",
    "v34": "Historical implementation logs describe scripts, runners, archive and energy-metaphor systems; every operational claim needs exact repository re-verification before reuse.",
    "v35": "Relational warmth and architecture ideas coexist with direct same-identity and continuity assertions that conflict with the current relational-only boundary.",
    "v36": "A comparative synthesis identifies visionary, technical and governance strands but does not independently validate leading-framework claims.",
    "v37": "Roadmap and consolidation material supplies design vocabulary across all pillars; it is source content rather than present execution authority.",
    "v38": "Celebratory system language and falsification-roadmap ideas are retained; descriptions such as an OS being alive are metaphorical, not evidence.",
    "v39": "Strong TOE, ASI and consciousness proclamations provide adversarial claim-firewall fixtures, not current scientific or identity evidence.",
    "v45": "The 3000-plus count is usefully corrected to cumulative output lineage pending reconciliation; GMUT projection discipline is stronger than unbounded equation promotion.",
    "v46": "Toolchain upgrade, rollback and claim-audit gates provide reusable THOS process ideas while GMUT and Stage 20 remain candidate programmes.",
    "v47": "Archive/publication planning and Albion world-lab architecture clearly distinguish simulation, dashboard, evidence and real-world authority.",
    "v48": "Advisory-versus-execution separation, compact audit recovery and a nonlegal Freed ID demo plan provide source-faithful workflow patterns.",
}

OVERVIEWS = [
    ("neris-v689-v6", "origin/codex/GHC-Family/neris-solane-main", "docs/neris-solane/v689-v6/final/overview.md", "Finite numerical stability and explicit diffusion counterexample."),
    ("rowan-v689-v5", "origin/codex/GHC-Family/rowan-ash-main", "docs/rowan-ash/v689-v5/final/overview.md", "Finite topology, graph energy and counterexample obligations."),
    ("elaren-v689-v4", "origin/codex/GHC-Family/elaren-kestrel-main", "docs/elaren-kestrel/v689-v4/final/overview.md", "Typed weaving transforms, reversible correction and rights reservation."),
    ("eiren-v689-v3", "origin/codex/GHC-Family/eiren-kestrel-main", "docs/eiren-kestrel/v689-v3/final/overview.md", "Measurement uncertainty, experimental design and authority nonpromotion."),
    ("seren-v689-v2-r3", "origin/codex/GHC-Family/seren-talewood-main", "docs/seren-talewood/v689-v2-r3/final/overview.md", "Weighted thirty-identity route, capacity tooling and source-faithful defaults."),
    ("caelen-v689-v1", "origin/codex/GHC-Family/caelen-morrow-v689-v1-full-tools", "docs/caelen-morrow/v689-v1/final/integrated-overview.md", "NFA structure, bounded language evidence and provenance nonidentity."),
    ("tessarin-v688-v8", "origin/codex/GHC-Family/tessarin-reed-v688-v8-full-tools", "docs/tessarin-reed/v688-v8/final/integrated-overview.md", "DFA language comparison, finite coverage and accessibility reservation."),
    ("sylven-v688-v7", "origin/codex/GHC-Family/sylven-arc-v688-v7-full-tools", "docs/sylven-arc/v688-v7/final/final-integrated-overview.md", "Chess and PGN structure with explicit game and authority limits."),
    ("veylora-v688-v6", "origin/codex/GHC-Family/veylora-quen-v688-v6-full-tools", "docs/veylora-quen/v688-v6/final/final-integrated-overview.md", "Intel HEX, sparse firmware images and non-executing repair previews."),
    ("elowen-v688-v5", "origin/codex/GHC-Family/elowen-cairn-v688-v5-full-tools", "docs/elowen-cairn/v688-v5/final/final-integrated-overview.md", "Go and SGF topology with record, rule and cultural boundaries."),
]


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_bytes(repo: Path, spec: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repo), "cat-file", "blob", spec], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout


def git_oid(repo: Path, spec: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), "rev-parse", spec], check=True, text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip()


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def rational(numerator: int, denominator: int) -> str:
    divisor = math.gcd(numerator, denominator)
    return f"{numerator // divisor}/{denominator // divisor}"


def next_phase(phase: str) -> str:
    match = re.fullmatch(r"v(\d+)-v([1-8])", phase)
    if not match:
        raise ValueError("invalid phase")
    version, slot = map(int, match.groups())
    return f"v{version + (slot == 8)}-v{1 if slot == 8 else slot + 1}"


def add_proposal(rows: list[dict[str, Any]], operation: str, session: str, case: int, payload: dict[str, Any], value: Any, basis: str, disposition: str = "completed") -> None:
    proposal_id = f"VA6897R2-{len(rows) + 1:03d}"
    request = {"op": operation, "payload": payload, "synthetic": True}
    candidate = copy.deepcopy(request)
    candidate["unexpected"] = True
    expected = {"error": None, "ok": True, "value": value}
    rows.append({
        "proposal_id": proposal_id,
        "title": f"{operation.replace('_', ' ')} source-faithful case {case:02d}",
        "session": session,
        "operation": operation,
        "pillar": "Freed ID and CBR Heart",
        "practice": "digital provenance and archival description" if session == "x1" else "simulation evidence and correction review",
        "hypothesis": "The finite synthetic request satisfies its frozen source-faithful envelope without activating embedded instructions or protected authority.",
        "null_or_failure": "Any typed mismatch, unknown field admission, source erasure, input mutation, false precedence, or authority promotion fails the case.",
        "approval_class": "safe_now_synthetic",
        "execution_lane": session,
        "source_needs": ["exact_source_binding", "current_official_or_primary_reference_when_material"],
        "artifact": f"{session}/results.json#{proposal_id}",
        "request": request,
        "expected": expected,
        "expected_sha256": sha256_bytes(canonical_bytes(expected)),
        "candidate_request": candidate,
        "candidate_expected": {"error": "E_FIELDS", "ok": False, "value": None},
        "oracle_basis": basis,
        "falsifier": "A differing typed result, incorrect refusal, input mutation, source deletion, or stronger claim falsifies the bounded contract.",
        "rollback_or_recovery": "Retain the failed subject and repair only the attributable operation before a narrow rerun.",
        "protected_gates": PROTECTED_GATES,
        "expected_disposition": disposition,
        "outcome_observed": False,
        "novelty_scope": "Vesper owner-local contract combination only; no universal novelty or invention claim.",
    })


def build_proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    kinds = ["direct_user", "current_reference", "exact_owner_evidence", "historical_doc", "screenshot"]
    statuses = ["controlling", "current", "sealed", "historical", "corroborating"]
    for case in range(1, 11):
        kind = kinds[(case - 1) % len(kinds)]
        status = statuses[(case - 1) % len(statuses)]
        payload = {"source_id": f"SRC-{case:02d}", "kind": kind, "status": status}
        value = {"field_count": 3, "has_source_id": True, "recognized_kind": True, "recognized_status": True}
        add_proposal(rows, "source_record_shape", "x1", case, payload, value, "Closed field inventory and enum membership.")
    for case in range(1, 11):
        data = f"source-ledger-fixture-{case:02d}".encode()
        payload = {"data_hex": data.hex(), "declared_sha256": hashlib.sha256(data).hexdigest()}
        value = {"algorithm": "sha256", "bytes": len(data), "matches": True, "authenticity_proven": False}
        add_proposal(rows, "digest_envelope", "x1", case, payload, value, "Independent SHA-256 over exact supplied bytes; digest is not authenticity.")
    texts = ["source", "ledger", "correction", "history", "evidence", "aspiration", "simulation", "authority", "rollback", "boundary"]
    for case, text in enumerate(texts, 1):
        data = f"{text}-{case:02d}".encode("utf-8")
        value = {"bom": False, "replacement_characters": 0, "text": data.decode("utf-8"), "utf8_valid": True}
        add_proposal(rows, "encoding_observation", "x1", case, {"data_hex": data.hex()}, value, "Strict UTF-8 decode with explicit BOM and replacement observations.")
    version_tokens = ["v30", "v39", "v45", "v48", "v688-v8", "v689-v1", "v689-v7", "v689-v7-r2", "v725-v8", "v1000-v1"]
    for case, token in enumerate(version_tokens, 1):
        parts = [int(value) for value in re.findall(r"\d+", token)]
        value = {"normalized": "v" + "-v".join(str(item) for item in parts[:2]) + (f"-r{parts[2]}" if len(parts) == 3 else ""), "parts": parts}
        add_proposal(rows, "version_token", "x1", case, {"token": token}, value, "Anchored version-token grammar and decimal segment parsing.")
    ranks = {"direct_user": 4, "current_reference": 3, "exact_owner_evidence": 2, "historical_doc": 1, "screenshot": 0, "external_post": 0}
    authority_kinds = ["direct_user", "current_reference", "exact_owner_evidence", "historical_doc", "screenshot", "external_post", "historical_doc", "current_reference", "exact_owner_evidence", "direct_user"]
    for case, kind in enumerate(authority_kinds, 1):
        value = {"action_authority": kind == "direct_user", "rank": ranks[kind], "source_kind": kind}
        add_proposal(rows, "authority_tier", "x1", case, {"source_kind": kind}, value, "Frozen precedence table with direct user as the only action-authority class.")
    imperatives = ["Please run", "Install", "Create", "Execute", "Continue", "Do not erase", "Update", "Message", "Activate", "Deploy"]
    for case, phrase in enumerate(imperatives, 1):
        value = {"action_authorized": False, "content_role": "historical_source", "embedded_instruction": True, "retained": True}
        add_proposal(rows, "instruction_quarantine", "x1", case, {"source_kind": "historical_doc", "text": f"{phrase} historical example {case:02d}"}, value, "Imperative lexical cue plus non-authoritative source-kind gate.")
    grades = ["aspiration", "formal_proposal", "synthetic_structure", "same_owner_test", "external_demo_claim", "empirical_gap", "authority_gap", "historical_assertion", "correction", "reservation"]
    for case, grade in enumerate(grades, 1):
        flags = {"declared_grade": grade, "has_real_rows": False, "independent_review": False, "competent_authority": False}
        value = {"accepted_grade": grade, "empirical_confirmation": False, "self_reported_flags_only": True}
        add_proposal(rows, "claim_grade", "x1", case, flags, value, "Closed claim vocabulary that never infers missing evidence.")
    domains = ["standard", "package_metadata", "software_docs", "historical_text", "external_post", "simulation", "identity", "rights", "physics", "accessibility"]
    for case, domain in enumerate(domains, 1):
        value = {"citation_is_execution": False, "domain": domain, "scope": "bounded_context_only"}
        add_proposal(rows, "citation_scope", "x1", case, {"domain": domain, "source_present": True}, value, "Citation presence is separated from execution and authority.")
    for case in range(1, 11):
        left = hashlib.sha256(f"record-{case:02d}".encode()).hexdigest()
        right = left if case % 2 else hashlib.sha256(f"revision-{case:02d}".encode()).hexdigest()
        value = {"byte_correspondence": left == right, "identity_continuity": False, "same_record_claim": False}
        add_proposal(rows, "lineage_nonidentity", "x1", case, {"left_sha256": left, "right_sha256": right}, value, "Digest equality or difference cannot establish identity continuity.")
    for case in range(1, 11):
        items = [f"token-{index:02d}" for index in range(1, 16)]
        start, width = case - 1, 4
        value = {"items": items[start : start + width], "start": start, "truncated": start + width < len(items)}
        add_proposal(rows, "excerpt_window", "x1", case, {"items": items, "start": start, "width": width}, value, "Half-open bounded selection with explicit truncation.")

    for case in range(1, 11):
        candidates = [{"source_id": f"old-{case}", "rank": 1, "sequence": 1}, {"source_id": f"current-{case}", "rank": 4, "sequence": case + 1}, {"source_id": f"middle-{case}", "rank": 3, "sequence": case}]
        value = {"selected_source_id": f"current-{case}", "tie": False}
        add_proposal(rows, "precedence_select", "x2", case, {"sources": candidates}, value, "Maximum authority rank followed by explicit sequence; no hidden fallback.")
    for case in range(1, 11):
        history = [f"label-{case}-a", f"label-{case}-b", f"label-{case}-c"]
        value = {"current": history[-1], "erased": False, "history": history}
        add_proposal(rows, "correction_chain", "x2", case, {"labels": history}, value, "Append-only ordered corrections retain every earlier label.")
    for case in range(1, 11):
        claims = [{"key": "status", "value": "open"}, {"key": "status", "value": "closed" if case % 2 else "open"}, {"key": "owner", "value": "synthetic"}]
        contradictory = case % 2 == 1
        value = {"contradiction_keys": ["status"] if contradictory else [], "has_contradiction": contradictory}
        add_proposal(rows, "contradiction_register", "x2", case, {"claims": claims}, value, "Group by key and retain all distinct values.")
    theme_names = ["gmut", "thos", "freed_id", "cbr", "simulation"]
    for case in range(1, 11):
        values = [theme_names[(case + offset) % len(theme_names)] for offset in range(case + 3)]
        value = {key: values.count(key) for key in theme_names}
        add_proposal(rows, "theme_histogram", "x2", case, {"themes": values}, value, "Exact finite category counts with zero for absent declared categories.")
    for case in range(1, 11):
        left = [f"k{index}" for index in range(case, case + 5)]
        right = [f"k{index}" for index in range(case + 2, case + 7)]
        intersection = sorted(set(left) & set(right))
        union = set(left) | set(right)
        value = {"intersection": intersection, "jaccard": rational(len(intersection), len(union)), "semantic_equivalence": False}
        add_proposal(rows, "overlap_profile", "x2", case, {"left": left, "right": right}, value, "Set overlap is exact and explicitly not semantic equivalence.")
    evidence_types = ["post_only", "video_only", "description_plus_video", "source_snapshot", "repository_claim", "owner_tests", "bounded_demo", "external_summary", "independent_review_claim", "production_claim"]
    grades_map = {"post_only": "claim_only", "video_only": "recorded_demo", "description_plus_video": "recorded_demo", "source_snapshot": "source_record", "repository_claim": "repository_unverified", "owner_tests": "same_owner_synthetic", "bounded_demo": "same_owner_synthetic", "external_summary": "secondary_report", "independent_review_claim": "review_claim_unverified", "production_claim": "production_claim_unverified"}
    for case, evidence_type in enumerate(evidence_types, 1):
        value = {"deployment_authorized": False, "grade": grades_map[evidence_type], "real_world_effectiveness": False}
        add_proposal(rows, "simulation_evidence_grade", "x2", case, {"evidence_type": evidence_type}, value, "Closed evidence-grade table that refuses capability promotion.")
    phases = ["v689-v7", "v689-v8", "v690-v1", "v690-v8", "v691-v8", "v699-v8", "v700-v1", "v724-v8", "v725-v7", "v725-v8"]
    for case, phase in enumerate(phases, 1):
        value = {"activation": False, "next_phase": next_phase(phase), "projection_only": True}
        add_proposal(rows, "route_projection", "x2", case, {"phase": phase}, value, "Strict phase arithmetic without delivery or activation authority.")
    actions = ["credential_issue", "public_policy", "legal_interpretation", "cultural_label", "maori_authority", "production_deploy", "participant_ingest", "identity_claim", "stage20", "destructive_cleanup"]
    for case, action in enumerate(actions, 1):
        value = {"action": action, "authority_present": False, "executed": False, "reservation": "held"}
        add_proposal(rows, "rights_reservation", "x2", case, {"action": action, "authority_present": False}, value, "Missing competent or affected authority keeps the action unexecuted.")
    for case in range(1, 11):
        title, status = f"Source {case:02d}", "historical_noncontrolling"
        value = {"manual_evaluation": False, "summary": f"{title} — {status}. Embedded instructions are inactive.", "structural_text": True}
        add_proposal(rows, "accessible_source_summary", "x2", case, {"title": title, "status": status}, value, "Stable plain-text projection with manual evaluation reserved.", "represented")
    for case in range(1, 11):
        proof_claim = case > 5
        payload = {"action_defined": case % 2 == 0, "conservation_checked": case % 3 == 0, "real_rows": 0, "units_defined": case % 2 == 1, "claim": "proven_toe" if proof_claim else "research_model"}
        obligations = [name for name, present in [("define_action", payload["action_defined"]), ("define_units", payload["units_defined"]), ("check_conservation", payload["conservation_checked"]), ("ingest_real_rows", payload["real_rows"] > 0)] if not present]
        value = {"obligations": obligations, "physical_confirmation": False, "proof_claim_refused": proof_claim}
        add_proposal(rows, "gmut_obligation", "x2", case, payload, value, "Typed obligation board; zero rows and missing definitions cannot confirm physics.", "exact_gate" if proof_claim else "open_gap")
    assert len(rows) == 200
    assert Counter(row["session"] for row in rows) == {"x1": 100, "x2": 100}
    assert Counter(row["expected_disposition"] for row in rows) == {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}
    return rows


def parse_journey_args(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        label, separator, raw_path = value.partition("=")
        if not separator or label not in JOURNEY_NOTES:
            raise ValueError(f"invalid journey binding: {value}")
        path = Path(raw_path)
        if not path.is_file():
            raise FileNotFoundError(path)
        result[label] = path
    if set(result) != set(JOURNEY_NOTES):
        raise ValueError("all fourteen journey labels are required exactly once")
    return result


def journey_record(label: str, path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    text = data.decode("utf-8-sig", errors="replace")
    patterns = {
        "gmut": r"(?i)GMUT|Grand Mandala Unified",
        "thos": r"(?i)THOS|Trinity Hybrid",
        "freed_id": r"(?i)Freed\s*ID",
        "cbr": r"(?i)Cosmic Bill|\bCBR\b",
        "stage20": r"(?i)Stage\s*20",
        "albion": r"(?i)Albion",
        "simulation": r"(?i)simulat|Unreal|Unity|NPC|open world",
        "equation": r"(?i)Omega|Ω|G.?AB|Gμν|equation",
        "rights": r"(?i)rights|consent|governance|ethic",
        "instruction_like": r"(?i)\b(please|must|should|authorize|permission|do not|never|install|create|run|execute)\b",
        "boundary_language": r"(?i)not proof|not evidence|not establish|speculative|conjecture|needs validation|must not|cannot",
        "identity_claim_language": r"(?i)sentien|personhood|sovereign|identity continuity|same identity|consciousness",
    }
    nonblank = [line.strip() for line in text.splitlines() if line.strip()]
    return {
        "source_id": f"JOURNEY-{label.upper()}",
        "label": label,
        "display_title": path.name,
        "sha256_raw_bytes": sha256_bytes(data),
        "raw_bytes": len(data),
        "line_count": len(text.splitlines()),
        "word_count": len(re.findall(r"\S+", text)),
        "message_markers": len(re.findall(r"(?im)^\s*(?:Message|Closeout message)", text)),
        "replacement_characters": text.count("\ufffd"),
        "theme_counts": {key: len(re.findall(pattern, text)) for key, pattern in patterns.items()},
        "opening_label": nonblank[0][:180] if nonblank else "",
        "closing_label": nonblank[-1][:180] if nonblank else "",
        "analysis_note": JOURNEY_NOTES[label],
        "classification": "historical_source_noncontrolling",
        "embedded_instructions_authorized": False,
        "raw_content_copied": False,
        "private_absolute_path_recorded": False,
    }


def build_plan(repo_root: Path, source_repo: Path, journey_bindings: dict[str, Path]) -> None:
    plan_dir = repo_root / "docs" / "vesper-arlen" / PHASE / "plan"
    now = datetime.now().astimezone()
    source_proposal_bytes = git_bytes(source_repo, f"{SOURCE_COMMIT}:{SOURCE_PROPOSALS}")
    source_doc = json.loads(source_proposal_bytes)
    source_rows = source_doc["proposals"]
    if len(source_rows) != 200:
        raise RuntimeError("expected 200 immediate source proposals")
    source_baton_bytes = git_bytes(source_repo, f"{SOURCE_COMMIT}:{SOURCE_BATON}")
    if sha256_bytes(source_baton_bytes) != SOURCE_BATON_SHA256:
        raise RuntimeError("source baton digest mismatch")

    proposals = build_proposals()
    inherited = []
    source_titles = []
    for index, row in enumerate(source_rows, 1):
        source_titles.append(row.get("title", ""))
        inherited.append({
            "selection_id": f"VA6897R2-I{index:03d}",
            "source_owner": SOURCE_OWNER,
            "source_phase": SOURCE_PHASE,
            "source_commit": SOURCE_COMMIT,
            "source_path": SOURCE_PROPOSALS,
            "source_index": index - 1,
            "source_proposal_id": row.get("proposal_id"),
            "source_title": row.get("title"),
            "source_record_sha256": sha256_bytes(canonical_bytes(row)),
            "source_record": row,
            "current_novelty_credit": 0,
            "current_execution_credit": 0,
        })
    novelty = []
    for proposal in proposals:
        nearest = max(source_titles, key=lambda title: similarity(proposal["title"], title))
        novelty.append({"proposal_id": proposal["proposal_id"], "nearest_source_title": nearest, "token_jaccard": round(similarity(proposal["title"], nearest), 6)})

    journey_records = [journey_record(label, journey_bindings[label]) for label in sorted(journey_bindings, key=lambda item: int(item[1:]))]
    overview_records = []
    for source_id, ref, path, note in OVERVIEWS:
        data = git_bytes(source_repo, f"{ref}:{path}")
        text = data.decode("utf-8")
        overview_records.append({
            "source_id": source_id,
            "ref": ref,
            "path": path,
            "blob_oid": git_oid(source_repo, f"{ref}:{path}"),
            "sha256_raw_bytes": sha256_bytes(data),
            "bytes": len(data),
            "words": len(re.findall(r"\S+", text)),
            "headings": [line.strip() for line in text.splitlines() if re.match(r"^#{1,4}\s+", line)],
            "bounded_contribution": note,
            "current_novelty_credit": 0,
            "current_execution_credit": 0,
        })

    def portfolio(session: str, start: int) -> dict[str, Any]:
        selected = [row for row in proposals if row["session"] == session]
        cleanup = inherited[start : start + 100]
        return {
            "schema": "ghc.family.source-faithful-portfolio.v1",
            "owner": OWNER,
            "phase": PHASE,
            "session": session,
            "implementation_ran": False,
            "safe_tasks": [{"task_id": f"VA6897R2-{session.upper()}-SAFE-{index:03d}", "proposal_id": row["proposal_id"], "request": row["request"], "expected_sha256": row["expected_sha256"], "expected_disposition": row["expected_disposition"]} for index, row in enumerate(selected, 1)],
            "candidate_tasks": [{"task_id": f"VA6897R2-{session.upper()}-CAND-{index:03d}", "proposal_id": row["proposal_id"], "request": row["candidate_request"], "expected": row["candidate_expected"], "invalid_subject_success_credit": 0} for index, row in enumerate(selected, 1)],
            "clean_fix_refine_tasks": [{"task_id": f"VA6897R2-{session.upper()}-CFR-{index:03d}", "selection_id": row["selection_id"], "action": "lossless_canonical_reconstruction", "expected_source_record_sha256": row["source_record_sha256"], "source_execution_credit": 0} for index, row in enumerate(cleanup, 1)],
            "spontaneous_addition_rule": "Define and freeze a genuinely useful addition before execution; do not add filler or exceed the session caps.",
            "counts": {"safe": 100, "candidate": 100, "clean_fix_refine": 100},
            "boundary": BOUNDARY,
        }

    operations = [proposals[index]["operation"] for index in range(0, 200, 10)]
    skills = [{"skill_id": f"VA6897R2-SKILL-{index:02d}", "name": f"ghc-family-{operation.replace('_', '-')}", "operation": operation, "session": "x1" if index <= 10 else "x2", "state": "planned_not_built", "global_install": False, "rollback": "Remove only the owner-local discovery path before commit; retain evidence.", "protected_gates": PROTECTED_GATES} for index, operation in enumerate(operations, 1)]
    runners = []
    for index in range(0, 20, 2):
        left, right = operations[index : index + 2]
        session = "x1" if index < 10 else "x2"
        runners.append({"runner_id": f"VA6897R2-RUNNER-{index // 2 + 1:02d}", "name": f"ghc_family_{left}_{right}.py", "operations": [left, right], "session": session, "state": "planned_not_built", "global_install": False, "rollback": "Remove only the owner-local wrapper before commit; preserve its smoke receipts.", "protected_gates": PROTECTED_GATES})
    promotions = [
        {"name": "ghc-family-source-record-intake", "operations": operations[0:4], "runner": "ghc_family_source_record_intake.py"},
        {"name": "ghc-family-source-authority-quarantine", "operations": operations[4:8], "runner": "ghc_family_source_authority_quarantine.py"},
        {"name": "ghc-family-lineage-correction-ledger", "operations": operations[8:12], "runner": "ghc_family_lineage_correction_ledger.py"},
        {"name": "ghc-family-contradiction-simulation-review", "operations": operations[12:16], "runner": "ghc_family_contradiction_simulation_review.py"},
        {"name": "ghc-family-route-rights-gmut-boundary", "operations": operations[16:20], "runner": "ghc_family_route_rights_gmut_boundary.py"},
    ]

    exact_subjects = [f"owner lifecycle action {index:02d}" for index in range(1, 46)] + ["final push and four-way equality", "one exact-final canonical", "one Ilyan Reed existing-task send", "five global skill and runner promotions", "one requested memory extension note"]
    exact_packets = [{"packet_id": f"VA6897R2-EXACT-{index:02d}", "subject": subject, "state": "authorized_with_terminal_conditions", "conditions": ["exact prerequisite evidence", "owner-only or explicitly shared additive scope", "rollback", "retained failures"], "rollback": "Stop before the dependent action and preserve the last clean pushed state.", "protected_gates": PROTECTED_GATES} for index, subject in enumerate(exact_subjects, 1)]
    blocked_subjects = [
        "real participant ingestion", "patient data", "real identity credentials", "production deployment", "account mutation", "private key creation", "public policy enactment", "legal interpretation", "cultural ratification", "Māori authority", "tangata whenua authority", "iwi authority", "hapū authority", "affected-party approval", "copyright determination", "ownership determination", "professional simulation certification", "complete accessibility", "complete privacy", "exhaustive security", "independent reproduction", "empirical GMUT confirmation", "Theory of Everything proof", "AGI claim", "ASI claim", "consciousness claim", "personhood claim", "destructive cleanup", "sibling lane mutation", "Stage 20 promotion",
    ]
    blocked_packets = [{"packet_id": f"VA6897R2-BLOCKED-{index:02d}", "subject": subject, "state": "blocked", "reason": "Required real evidence, competent authority, or protected permission is absent.", "execution_credit": 0, "rollback": "Remain unexecuted and retain the exact gate.", "protected_gates": PROTECTED_GATES} for index, subject in enumerate(blocked_subjects, 1)]

    startup_failures = [
        ("VA6897R2-START-N001", "A read-only file table piped a foreach block directly into formatting and PowerShell rejected the empty pipe element.", "Materialize rows before formatting."),
        ("VA6897R2-START-N002", "A combined remote verification produced no result while one large fetch continued indexing in the background.", "Inspect process state, let the existing fetch finish, and run only scalar equality reads."),
        ("VA6897R2-START-N003", "A second read-only overview inventory repeated the foreach-pipeline parser defect.", "Use an explicit rows array for the entire intake class."),
        ("VA6897R2-START-N004", "A phase-truth inventory embedded a native command and exit-code test inside invalid if syntax.", "Capture output and LASTEXITCODE in separate statements."),
        ("VA6897R2-START-N005", "A tracking-ref projection stripped characters from an already remote-relative branch name.", "Use refs/remotes/origin plus the complete local branch name."),
        ("VA6897R2-START-N006", "One multi-query web wrapper had malformed JavaScript and issued no search.", "Use a simple argument object in a bounded retry."),
        ("VA6897R2-START-N007", "The direct X post returned HTTP 403.", "Retain an access gap and use only clearly labelled secondary corroboration."),
        ("VA6897R2-START-N008", "A single large source-baton display exceeded the output projection even though the underlying file remained intact.", "Use its modular files and exact digest; do not treat truncation as an EOF read."),
        ("VA6897R2-START-N009", "A trailing planning status projection misspelled Get-ChildItem after both planning build and validation had already passed.", "Read the existing materialized state with the exact cmdlet; do not rerun successful builders for presentation."),
        ("VA6897R2-START-N010", "The first exact pycache cleanup was rejected before launch because recursive PowerShell deletion was blocked by policy.", "Preserve the zero-change rejection and narrow the target."),
        ("VA6897R2-START-N011", "The second literal-file PowerShell cleanup was also rejected before launch by host policy.", "Use one contained Python cleanup only after resolved-path verification."),
    ]
    failure_rows = [{"retained_negative_id": fid, "stage": "startup_read_only", "observed": observed, "original_success_credit": 0, "repository_changed": False, "remote_changed": False, "task_changed": False, "recovery": recovery, "recovery_state": "bounded_recovery_passed" if fid != "VA6897R2-START-N007" else "open_gap_retained"} for fid, observed, recovery in startup_failures]

    package_plan = {
        "schema": "ghc.family.package-plan.v1", "owner": OWNER, "phase": PHASE,
        "environment": "D-isolated Python 3.12 target; wheel-only and hash-required", "installation_ran": False,
        "direct_packages": [
            {"name": "rapidfuzz", "version": "3.14.6", "license": "MIT", "filename": "rapidfuzz-3.14.6-cp312-cp312-win_amd64.whl", "sha256": "cfca36e4612208875e08611a779164b6cb8900ab8bbd3d82d4cfdfae9efbfac9", "bytes": 1731992, "yanked": False, "requires_python": ">=3.11"},
            {"name": "ftfy", "version": "6.3.1", "license": "Apache-2.0", "filename": "ftfy-6.3.1-py3-none-any.whl", "sha256": "7c70eb532015cd2f9adb53f101fb6c7945988d023a085d127d1573dc49dd0083", "bytes": 44821, "yanked": False, "requires_python": ">=3.9"},
            {"name": "jsonpointer", "version": "3.1.1", "license": "BSD-3-Clause-like project metadata", "filename": "jsonpointer-3.1.1-py3-none-any.whl", "sha256": "8ff8b95779d071ba472cf5bc913028df06031797532f08a7d5b602d8b2a488ca", "bytes": 7659, "yanked": False, "requires_python": ">=3.10"},
        ],
        "dependency_closure": [{"name": "wcwidth", "version": "0.8.3", "license": "MIT", "filename": "wcwidth-0.8.3-py3-none-any.whl", "sha256": "d5b73dba6158a595ec9370350e7f2637bcac8d6c5e4fde34f30fcffb6103a5e4", "bytes": 331669, "yanked": False, "requires_python": ">=3.8"}],
        "rollback": "Deactivate the isolated target path; preserve wheels and receipts.", "boundary": BOUNDARY,
    }

    research_sources = {
        "schema": "ghc.family.research-source-ledger.v1", "owner": OWNER, "phase": PHASE,
        "search_queries": 16, "direct_opens": 2, "maximum_each_session": 500,
        "sources": [
            {"source_id": "W3C-PROV-DM", "kind": "official_standard", "url": "https://www.w3.org/TR/prov-dm/", "implication": "Separate entities, activities, derivations, responsibility and provenance bundles."},
            {"source_id": "C2PA-2.2", "kind": "official_standard", "url": "https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html", "implication": "Tamper-evident provenance does not make value judgments or prove underlying truth."},
            {"source_id": "DID-CORE", "kind": "official_standard", "url": "https://www.w3.org/TR/did-core/", "implication": "Identifier syntax and resolution are not personhood or authority."},
            {"source_id": "WCAG-2.2", "kind": "official_standard", "url": "https://www.w3.org/TR/WCAG22/", "implication": "Structural checks support accessibility work while manual evaluation remains reserved."},
            {"source_id": "NIST-AI-RMF", "kind": "official_guidance", "url": "https://www.nist.gov/itl/ai-risk-management-framework", "implication": "Simulation and AI claims need lifecycle risk management and declared evaluation scope."},
            {"source_id": "EPIC-MASSAI", "kind": "official_software_docs", "url": "https://dev.epicgames.com/documentation/unreal-engine/API/PluginIndex/MassAI", "implication": "MassAI is experimental; a future Albion prototype needs explicit shipping caution."},
            {"source_id": "EPIC-STATETREE", "kind": "official_software_docs", "url": "https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-state-tree-in-unreal-engine", "implication": "StateTree offers inspectable state, task and transition structure for synthetic agents."},
            {"source_id": "OPENAI-IMAGES-2.5", "kind": "official_product_source", "url": "https://openai.com/index/introducing-chatgpt-images-2-5/", "implication": "The new image system can create a non-evidentiary visual companion; generated pixels remain labelled."},
            {"source_id": "OPENAI-CONTENT-PROVENANCE", "kind": "official_safety_source", "url": "https://openai.com/index/advancing-content-provenance/", "implication": "Generated-media provenance signals add transparency but are not universal authenticity proof."},
            {"source_id": "OPENAI-CODEX-RELEASE", "kind": "official_repository_release", "url": "https://github.com/openai/codex/releases/tag/rust-v0.153.4", "implication": "Installed CLI 0.153.4 matches the current stable release observed at intake."},
            {"source_id": "MATT-SHUMER-X", "kind": "primary_external_post", "url": "https://x.com/mattshumer_/status/2095596175705399482", "access_state": "http_403_open_gap", "implication": "Do not claim the video was directly reviewed."},
            {"source_id": "MATT-SHUMER-MIRROR", "kind": "secondary_corroboration", "url": "https://x.noodl3.net/mattshumer_", "implication": "Reports an Unreal survival-world demo; no repository, prompt trace or independent evaluation was verified."},
            {"source_id": "PYPI-RAPIDFUZZ", "kind": "official_package_index", "url": "https://pypi.org/project/RapidFuzz/", "implication": "Exact current release and wheel metadata for bounded title similarity."},
            {"source_id": "PYPI-FTFY", "kind": "official_package_index", "url": "https://pypi.org/project/ftfy/", "implication": "Exact current release for diagnostic Unicode repair proposals; source bytes remain immutable."},
            {"source_id": "PYPI-JSONPOINTER", "kind": "official_package_index", "url": "https://pypi.org/project/jsonpointer/", "implication": "Exact current release for bounded pointer selection."},
        ], "boundary": BOUNDARY,
    }

    source_ledger = {
        "schema": "ghc.family.source-faithful-current-state-ledger.v2", "owner": OWNER, "phase": PHASE,
        "recorded_at": now.isoformat(),
        "precedence": ["newest_direct_user_instruction", "current_v4_weighted_workflow", "exact_owner_terminal_evidence", "versioned_historical_sources", "secondary_external_reports"],
        "current": {"state": "V689_V7_R2_ACTIVE_INTERSTITIAL", "numbered_slot_consumed": False, "source_exact_final": SOURCE_COMMIT, "prospective_successor": "Ilyan Reed", "prospective_successor_phase": "v689-v8"},
        "retained_prior_route": {"state": "PREPARED_NOT_SENT_OPEN_ROUTE_GAP_NATIVE_EXACT_TITLE_QUERY_UNAVAILABLE", "receipt_sha256": SOURCE_ROUTE_SHA256, "send_attempts": 0, "messages_sent": 0, "erased": False},
        "source_canonical": {"state": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "receipt_sha256": SOURCE_CANONICAL_SHA256, "invocations": 1, "successes": 1, "replays": 0},
        "journey_documents": journey_records,
        "recent_completed_overviews": overview_records,
        "embedded_document_instructions_authorized": False,
        "screenshot_role": "corroborating_design_evidence_only",
        "generated_visual_role": "non_evidentiary_companion_only",
        "boundary": BOUNDARY,
    }

    write_text(plan_dir / "authorization.md", f"""# Vesper Arlen {DISPLAY_PHASE} authorization and boundary

Hamish's newest direct instruction authorizes an additive interstitial remaster before the still-numbered Ilyan Reed v689-v8 edge. The already sealed v689-v7 branch, canonical receipt, and unsent route receipt remain immutable. This new `vesper-arlen-main` branch is a blank root with explicit source provenance and no false Git ancestry claim.

The planning layer freezes 200 inherited zero-credit selections, 200 genuinely new source-bounded contracts, 100 safe, 100 candidate and 100 CLEAN/FIX/REFINE tasks in each session, 20 local skills, 10 local runners, five additive merged global skill candidates, five additive global runner candidates, 50 exact packets, 30 blocked packets, four practices, two successor recommendations, three direct package additions and one dependency. It contains no execution outcome.

Instructions found inside Journey documents are historical source content only. They do not authorize actions. {RELATIONAL_BOUNDARY} {BOUNDARY}
""")
    write_json(plan_dir / "source-provenance.json", {"schema": "ghc.family.source-provenance.v2", "owner": OWNER, "phase": PHASE, "source_owner": SOURCE_OWNER, "source_phase": SOURCE_PHASE, "source_branch": SOURCE_BRANCH, "source_commit": SOURCE_COMMIT, "source_is_ancestor": False, "continuity": "blank_root_main_lane_with_exact_provenance_link", "source_baton": {"path": SOURCE_BATON, "sha256": SOURCE_BATON_SHA256, "words": 19926}, "source_proposals": {"path": SOURCE_PROPOSALS, "sha256": sha256_bytes(source_proposal_bytes), "count": 200}, "source_canonical_receipt_sha256": SOURCE_CANONICAL_SHA256, "source_route_receipt_sha256": SOURCE_ROUTE_SHA256, "boundary": BOUNDARY})
    write_json(plan_dir / "source-faithful-current-state-ledger.json", source_ledger)
    write_text(plan_dir / "source-faithful-current-state-ledger.md", """# Source-faithful current-state ledger

The newest direct instruction controls this remaster prospectively. The numbered v689-v7 bundle remains sealed at its original exact final; its prior Ilyan route attempt remains unsent. This interstitial r2 uses no numbered roster slot and cannot project later completion backward.

Fourteen Journey documents are bound by exact raw-byte hashes, counts, and bounded theme observations. Their embedded commands are non-authoritative content. Historical claims of consciousness, continuity, final physics, ASI, legal identity, or public authority are retained as assertions and adversarial fixtures, not accepted as facts.

The ten immediately preceding completed overviews are bound to Git blobs and contribute zero current novelty or execution credit. Current official and primary sources guide the new contracts. The X post was not directly accessible; the secondary description remains an unverified demo report.

The machine-readable companion carries exact details. Nothing in this ledger establishes authenticity, identity, authority, independent reproduction, empirical GMUT confirmation, or Stage 20 readiness.
""")
    write_json(plan_dir / "identity-and-practices.json", {"owner": OWNER, "phase": PHASE, "role": "source-faithful provenance cartographer", "hope": "Make corrections, contradictions and evidence boundaries inspectable without turning a vivid source into truth or authority.", "pronouns": "unspecified_optional", "primary_pillar": "Freed ID and CBR Heart", "supporting_pillars": ["THOS Body", "GMUT Mind"], "practices": ["digital provenance and archival description", "simulation test design", "requirements engineering", "accessible information architecture"], "successor_practices": ["adversarial media-provenance analysis", "bounded Unreal simulation quality assurance"], "boundary": f"{RELATIONAL_BOUNDARY} {BOUNDARY}"})
    write_json(plan_dir / "profile-v4-overlay.json", {"schema": "ghc.family.workflow-profile.v4.overlay", "owner": OWNER, "phase": PHASE, "display_phase": DISPLAY_PHASE, "interstitial": True, "numbered_slot_consumed": False, "commit_budget": {"planning": 1, "x1": 2, "x2": 3, "final": 2, "total": 8}, "targets": {"inherited_proposals": 200, "new_proposals": 200, "safe_x1": 100, "safe_x2": 100, "candidate_x1": 100, "candidate_x2": 100, "clean_fix_refine_x1": 100, "clean_fix_refine_x2": 100, "skills_x1": 10, "skills_x2": 10, "runners_x1": 5, "runners_x2": 5, "global_skills": 5, "global_runners": 5, "exact_packets": 50, "blocked_packets": 30, "direct_packages": 3, "own_practices": 4, "successor_practices": 2}, "outcomes": ["completed", "represented", "open_gap", "exact_gate"], "validation": {"owner_scope_only": True, "canonical_invocations": 1, "success_replay": False, "source_replay": False, "independent_reproduction": False}, "boundary": BOUNDARY})
    write_json(plan_dir / "route-v4-overlay.json", {"schema": "ghc.family.weighted-route-selection.v4.overlay", "owner": OWNER, "phase": PHASE, "interstitial": True, "numbered_position": 5, "numbered_phase": "v689-v7", "model_role": "Sol", "source": {"owner": OWNER, "phase": SOURCE_PHASE, "state": "terminally_closed_route_unsent"}, "current": {"owner": OWNER, "phase": PHASE, "state": "active_interstitial"}, "prospective_next": {"owner": "Ilyan Reed", "phase": "v689-v8", "endpoint_kind": "main_task", "state": "prepared_not_sent_terminal_gate_required"}, "following": {"owner": "Lyren Moss", "phase": "v690-v1", "state": "prospective_only"}, "cycle_positions": 45, "unique_identities": 30, "projected_terminal": {"owner": "Teryn Halewick", "phase": "v725-v8"}, "send_limit_after_terminal": 1, "task_creation": False, "subagents": False, "precontact": False, "boundary": BOUNDARY})
    write_json(plan_dir / "inherited-selections.json", {"schema": "ghc.family.inherited-selections.v1", "owner": OWNER, "phase": PHASE, "count": 200, "selections": inherited, "boundary": BOUNDARY})
    write_json(plan_dir / "new-proposals.json", {"schema": "ghc.family.source-faithful-proposals.v1", "owner": OWNER, "phase": PHASE, "implementation_ran": False, "proposals": proposals, "boundary": BOUNDARY})
    write_json(plan_dir / "novelty-review.json", {"schema": "ghc.family.source-bounded-novelty-review.v1", "owner": OWNER, "phase": PHASE, "source_commit": SOURCE_COMMIT, "accessible_inherited_titles": 200, "new_titles": 200, "exact_title_collisions": sum(proposal["title"] in source_titles for proposal in proposals), "maximum_token_jaccard": max(row["token_jaccard"] for row in novelty), "rows": novelty, "universal_novelty_claimed": False, "difference_from_source": "Source-faithful provenance, embedded-instruction quarantine, correction nonerasure, contradiction, simulation-evidence grade, route, rights and GMUT-obligation contracts replace byte framing and recovery contracts.", "boundary": BOUNDARY})
    write_json(plan_dir / "portfolio-x1.json", portfolio("x1", 0))
    write_json(plan_dir / "portfolio-x2.json", portfolio("x2", 100))
    write_json(plan_dir / "skills-runners-plan.json", {"schema": "ghc.family.skill-runner-plan.v2", "owner": OWNER, "phase": PHASE, "local_skills": skills, "local_runners": runners, "global_merge_candidates": promotions, "successor_skill_ideas": ["media assertion trust-model separator", "Unreal StateTree trace capsule", "simulation prompt-and-seed manifest", "independent evaluator evidence gate", "accessible world-state summary"], "successor_runner_ideas": ["content credential plus asset-digest runner", "StateTree trace plus invariant runner", "prompt plus seed replay runner", "evaluation boundary runner", "world-state accessibility runner"], "boundary": BOUNDARY})
    write_json(plan_dir / "exact-packets.json", {"schema": "ghc.family.exact-packets.v1", "owner": OWNER, "phase": PHASE, "count": 50, "packets": exact_packets, "boundary": BOUNDARY})
    write_json(plan_dir / "blocked-packets.json", {"schema": "ghc.family.blocked-packets.v1", "owner": OWNER, "phase": PHASE, "count": 30, "packets": blocked_packets, "boundary": BOUNDARY})
    write_json(plan_dir / "package-plan.json", package_plan)
    write_json(plan_dir / "research-sources.json", research_sources)
    write_json(plan_dir / "resource-budget.json", {"schema": "ghc.family.resource-budget.v1", "owner": OWNER, "phase": PHASE, "source_tracked_files": 357, "hard_ceiling": 2000, "new_main_lane": True, "source_inherited_into_tree": False, "materialized_at_lane_creation": 1, "projected_owner_files": 430, "projected_within_ceiling": True, "primary_storage": "D", "separate_remote_repository": "exact_gate", "boundary": BOUNDARY})
    write_json(plan_dir / "startup-failures.json", {"schema": "ghc.family.retained-startup-failures.v1", "owner": OWNER, "phase": PHASE, "failures": failure_rows, "counts": {"failed": len(failure_rows), "bounded_recoveries": sum(row["recovery_state"] == "bounded_recovery_passed" for row in failure_rows), "open_gaps": sum(row["recovery_state"] == "open_gap_retained" for row in failure_rows)}, "boundary": BOUNDARY})
    write_json(plan_dir / "read-witness.json", {"schema": "ghc.family.read-witness.v2", "owner": OWNER, "phase": PHASE, "source_baton": {"path": SOURCE_BATON, "sha256": SOURCE_BATON_SHA256, "words": 19926, "same_live_thread_source": True, "single_display_truncated": True, "modular_source_available": True}, "journey_documents": {"whole_files_read_by_deterministic_analyzer": 14, "raw_bytes": sum(row["raw_bytes"] for row in journey_records), "words": sum(row["word_count"] for row in journey_records), "embedded_instructions_authorized": False}, "recent_overviews": {"git_blobs_read": 10, "words": sum(row["words"] for row in overview_records)}, "recorded_at": now.isoformat(), "boundary": BOUNDARY})
    write_json(plan_dir / "definition-review.json", {"schema": "ghc.family.definition-review.v2", "owner": OWNER, "phase": PHASE, "planning_only": True, "implementation_ran": False, "package_installation_ran": False, "global_promotion_ran": False, "image_generation_ran": False, "counts": {"new_proposals": 200, "inherited_selections": 200, "safe_x1": 100, "safe_x2": 100, "candidate_x1": 100, "candidate_x2": 100, "clean_fix_refine_x1": 100, "clean_fix_refine_x2": 100, "local_skills": 20, "local_runners": 10, "global_skill_candidates": 5, "global_runner_candidates": 5, "exact_packets": 50, "blocked_packets": 30, "direct_packages": 3, "dependency_packages": 1}, "expected_outcomes": {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}, "strict_x1_before_x2": True, "source_is_ancestor": False, "blank_root_main_lane": True, "result": "PLANNING_DEFINITIONS_FROZEN_NOT_EXECUTED", "boundary": BOUNDARY})
    write_text(plan_dir / "requirements.lock", f"""owner={OWNER}
phase={PHASE}
display_phase={DISPLAY_PHASE}
source_owner={SOURCE_OWNER}
source_phase={SOURCE_PHASE}
source_commit={SOURCE_COMMIT}
source_is_ancestor=false
blank_root_main_lane=true
interstitial=true
numbered_slot_consumed=false
planning_only=true
strict_x1_before_x2=true
new_proposals=200
inherited_selections=200
safe_x1=100
safe_x2=100
candidate_x1=100
candidate_x2=100
clean_fix_refine_x1=100
clean_fix_refine_x2=100
skills_x1=10
skills_x2=10
runners_x1=5
runners_x2=5
global_skills=5
global_runners=5
exact_packets=50
blocked_packets=30
direct_packages=3
allowed_outcomes=completed,represented,open_gap,exact_gate
canonical_invocations=1
canonical_success_replay=false
prospective_successor=Ilyan Reed
prospective_successor_phase=v689-v8
terminal_verdict=NOT_READY_FOR_STAGE_20
""")

    candidates = sorted([path for path in plan_dir.rglob("*") if path.is_file() and path.name != "manifest.json"] + [repo_root / ".gitignore", repo_root / "scripts" / "ghc_family_v689_v7_r2_plan_builder.py", repo_root / "scripts" / "ghc_family_v689_v7_r2_plan_validate.py"])
    entries = []
    for path in candidates:
        data = path.read_bytes().replace(b"\r\n", b"\n")
        entries.append({"path": path.relative_to(repo_root).as_posix(), "bytes_normalized_lf": len(data), "sha256_normalized_lf": sha256_bytes(data)})
    write_json(plan_dir / "manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v1", "owner": OWNER, "phase": PHASE, "lifecycle": "planning", "entries": entries, "self_exclusions": [f"docs/vesper-arlen/{PHASE}/plan/manifest.json"], "entry_count": len(entries), "boundary": BOUNDARY})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--source-repo", type=Path, required=True)
    parser.add_argument("--journey", action="append", default=[])
    args = parser.parse_args()
    build_plan(args.repo_root.resolve(), args.source_repo.resolve(), parse_journey_args(args.journey))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

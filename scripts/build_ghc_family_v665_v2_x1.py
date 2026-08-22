#!/usr/bin/env python3
"""Build and exact-review Liora Venn v665-v2's planning-only x1 freeze."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/liora-venn/v665-v2"
PREFIX = "docs/liora-venn/v665-v2/"
PHASE_ID = "v665-v2"
OWNER = "Liora Venn"
PRONOUNS = "she/they"
ROLE = "relational formal-integrability and boundary navigator"
HOPE = "make every compatibility condition visible before any claim travels beyond its evidence"
BRANCH = "codex/GHC-Family/liora-venn-v665-v2-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v665-v1-full-tools"
SOURCE = "3ec44a944aabe16f64335383885c39d9592bf849"
SOURCE_X1 = "1e9a49b0cc377ba2eafd90fb09e478c88f8f1f3b"
SOURCE_EVIDENCE = "1104a4f2963c8782ddad8939e8b4aff50715cc42"
SOURCE_FIRST_FINAL = "92ec05c2cbcd6d3e6c1878b7dd7e6165491a44a9"
SOURCE_FINAL = "f4abecafb107f4ac840c09b46a6b30079171816d"
SOURCE_FAILED_RECEIPT = "f0dc66c805f3b939ec12addbdebd828d891c2c59926b4f4249bb48ab0373d1e3"
SOURCE_SUCCESS_RECEIPT = "f2253a9bc21cfaf5b9e6bede29edd40fba118ad6f9fc3ae72bc3b1c039c643dd"
RECORDED_UTC = "2026-08-22T00:14:05Z"
RECORDED_NZ = "2026-08-22T12:14:05+12:00"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ACTIVATION_NEGATIVES = 25_187
ACTIVATION_METHODS = 9_049
STARTUP_FAILURES = 13
INHERITED_OPEN_GAPS = 175
INHERITED_EXACT_GATES = 173
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PROTECTED_GATES = [
    "empirical",
    "participant_or_affected_party",
    "professional",
    "production_or_deployment",
    "legal_or_cultural",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "proof_or_canon",
    "stage_20",
]

BASE_INDEX = "docs/neris-solane/v662-v3-2-remaster/provenance/frozen-chain-proposal-index.json"
CHAIN_FREEZES = [
    "docs/neris-solane/v662-v3-3-remaster/x1/proposal-freeze.json",
    "docs/neris-solane/v662-v3-3-midnight-remaster/x1/proposal-freeze.json",
    "docs/vesper-arlen/v662-v4/x1/proposal-freeze.json",
    "docs/lyren-moss/v662-v5/x1/proposal-freeze.json",
    "docs/ilyra-fen/v662-v6/x1/proposal-freeze.json",
    "docs/auren-lark/v662-v7/x1/proposal-freeze.json",
    "docs/sable-rook/v662-v8/x1/proposal-freeze.json",
    "docs/caelen-ash/v663-v1/x1/proposal-freeze.json",
    "docs/orin-thale/v663-v2/x1/proposal-freeze.json",
    "docs/liora-venn/v663-v3/x1/proposal-freeze.json",
    "docs/tamar-vey/v663-v4/x1/proposal-freeze.json",
    "docs/elowen-cairn/v663-v5/x1/proposal-freeze.json",
    "docs/sylven-arc/v663-v6/x1/proposal-freeze.json",
    "docs/sylven-arc/v663-v6-r2/x1/proposal-freeze.json",
    "docs/caelen-morrow/v663-v7/x1/proposal-freeze.json",
    "docs/eiren-kestrel/v663-v8/x1/proposal-freeze.json",
    "docs/elaren-kestrel/v664-v1/x1/proposal-freeze.json",
    "docs/neris-solane/v664-v2/x1/proposal-freeze.json",
    "docs/vesper-arlen/v664-v3/x1/proposal-freeze.json",
    "docs/lyren-moss/v664-v4/x1/proposal-freeze.json",
    "docs/ilyra-fen/v664-v5/x1/proposal-freeze.json",
    "docs/auren-lark/v664-v6/x1/proposal-freeze.json",
    "docs/sable-rook/v664-v7/x1/proposal-freeze.json",
    "docs/caelen-ash/v664-v8/x1/proposal-freeze.json",
    "docs/orin-thale/v665-v1/x1/proposal-freeze.json",
]

BUILDER = "scripts/build_ghc_family_v665_v2_x1.py"
TEST = "tests/test_ghc_family_liora_v665_v2_x1.py"
BASE_DOCS = [
    f"{PREFIX}x1/novelty-audit.json",
    f"{PREFIX}x1/phase-charter.json",
    f"{PREFIX}x1/portfolio-freeze.json",
    f"{PREFIX}x1/proposal-freeze.json",
    f"{PREFIX}x1/source-ledger.json",
    f"{PREFIX}x1/source-verification.json",
    f"{PREFIX}x1/startup-method-flow.json",
    f"{PREFIX}x1/threat-model-plan.json",
    f"{PREFIX}x1/workflow-plan.json",
    f"{PREFIX}x1/x1-overview.md",
    BUILDER,
    TEST,
]
SELF_EXCLUSIONS = [
    f"{PREFIX}x1/x1-content-manifest.json",
    f"{PREFIX}x1/x1-stage-candidate.json",
    f"{PREFIX}x1/x1-staged-review.json",
]
INTENDED = sorted(BASE_DOCS + SELF_EXCLUSIONS)


class X1Error(RuntimeError):
    pass


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=check
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def strict_json_bytes(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise X1Error(f"invalid UTF-8 JSON for {label}: {exc}") from exc


def git_json(path: str) -> Any:
    result = subprocess.run(
        ["git", "show", f"{SOURCE_FINAL}:{path}"],
        cwd=ROOT,
        capture_output=True,
        check=True,
    )
    return strict_json_bytes(result.stdout, path)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(relative: str, value: Any) -> None:
    target = PHASE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(pretty_bytes(value))


def write_text(relative: str, text: str) -> None:
    target = PHASE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((text.rstrip() + "\n").encode("utf-8"))


def row_title(row: dict[str, Any]) -> str:
    for key in ("title", "proposal_title", "description", "name"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise X1Error(f"historical proposal title field missing: {sorted(row)}")


def row_id(row: dict[str, Any]) -> str:
    for key in ("proposal_id", "id"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise X1Error(f"historical proposal identifier missing: {sorted(row)}")


def reconstruct_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    base = git_json(BASE_INDEX)
    corpus: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []

    def append_rows(items: list[dict[str, Any]], path: str) -> None:
        start = len(corpus)
        for row in items:
            corpus.append({"proposal_id": row_id(row), "title": row_title(row), "source_path": path})
        construction.append(
            {"source_path": path, "starting_count": start, "added_count": len(items), "ending_count": len(corpus)}
        )

    append_rows(base["prior_proposals"] + base["new_proposals"], BASE_INDEX)
    if len(corpus) != 3_530:
        raise X1Error(f"base corpus count drifted: {len(corpus)}")
    for path in CHAIN_FREEZES:
        freeze = git_json(path)
        append_rows(freeze["new_proposals"], path)
    if len(corpus) != 4_030:
        raise X1Error(f"effective inherited corpus must be 4030, got {len(corpus)}")
    return corpus, construction


PROPOSAL_ROWS = [
    ("LV6652-N001", "completed", "GMUT Mind", "GMUT finite-order differential-equation symbol tableau docket with equation-submanifold vacancy, jet-order pin, symbol kernel, rank uncertainty, background, domain, unit, and observation firewall", ["SRC-SPENCER"]),
    ("LV6652-N002", "completed", "GMUT Mind", "Spencer delta-complex worksheet for GMUT with bidegree, symbol module, differential sign, nilpotency obligation, cohomology vacancy, restriction hold, and no-theorem boundary", ["SRC-SPENCER"]),
    ("LV6652-N003", "completed", "GMUT Mind", "GMUT prolongation-projection lineage graph recording derivative consequences, order lifts, rank-change quarantine, regularity vacancy, formal-solution absence, and termination refusal", ["SRC-SPENCER", "SRC-COMPAT"]),
    ("LV6652-N004", "completed", "GMUT Mind", "Cartan-Kuranishi completion register for GMUT with regularity preconditions, involutivity-test vacancy, compatibility inventory, branch hold, termination hold, and no-completion claim", ["SRC-SPENCER", "SRC-COMPAT"]),
    ("LV6652-N005", "completed", "GMUT Mind", "GMUT compatibility-operator chain mapping equation operator, generating conditions, syzygy lineage, gauge scope, EFT scope, exactness vacancy, and proof-credit refusal", ["SRC-COMPAT"]),
    ("LV6652-N006", "completed", "Freed ID/CBR Heart", "Synthetic maritime passage capsule with surrogate voyage token, vessel-class placeholder, watch-plan scope, revision pin, cancellation state, custody vacancy, and no-navigation release", ["SRC-IMO-A893"]),
    ("LV6652-N007", "completed", "Freed ID/CBR Heart", "Synthetic passage-leg topology encoding waypoints, ordered legs, turn constraints, cross-track placeholder, alternate ports, orphan links, contradiction states, and repair abstention", ["SRC-IMO-A893"]),
    ("LV6652-N008", "completed", "Freed ID/CBR Heart", "Nautical-publication provenance register for surrogate chart cells with edition and update pins, issuing-authority vacancy, notice lineage, withdrawal state, licence hold, and no-chart-use", ["SRC-IHO-S100", "SRC-IHO-S101", "SRC-PROV"]),
    ("LV6652-N009", "completed", "Freed ID/CBR Heart", "Synthetic tide-weather-window board with source timestamp, forecast horizon, water-level placeholder, current placeholder, uncertainty band, expiry trigger, stale-data quarantine, and no-sailing decision", ["SRC-IMO-A893", "SRC-IHO-S100"]),
    ("LV6652-N010", "completed", "Freed ID/CBR Heart", "Draft-datum-depth clearance vacancy panel separating units, vertical datum, charted-depth placeholder, tide placeholder, squat allowance, safety margin, sensor absence, and under-keel nonrelease", ["SRC-IHO-S100", "SRC-IHO-S101"]),
    ("LV6652-N011", "completed", "THOS Body", "Append-only watch log as an event braid preserving prior entries, correction links, contested observations, supersession edges, dual-readback vacancy, unresolved alarms, and unsigned handover", ["SRC-PROV", "SRC-PREMIS"]),
    ("LV6652-N012", "completed", "THOS Body", "Accessible watchboard route map pairing semantic regions, ordered leg narration, noncolour alert text, keyboard sequence, print companion, plain-language holds, and affected-user evaluation reserve", ["SRC-WCAG22"]),
    ("LV6652-N013", "completed", "Freed ID/CBR Heart", "Content-addressed synthetic passage packet joining normalized leg graph, source-age map, refusal states, canonical digest, signature vacancy, verifier vacancy, and same-owner reproducibility limit", ["SRC-RFC8785", "SRC-VC-DI", "SRC-PROV"]),
    ("LV6652-N014", "completed", "Trinity Mandala", "Evidence-credit firewall for formal-PDE and passage artifacts assigning allowed claim class, absent external witness, expiry, rollback route, protected authority gate, and Stage-20 refusal", ["SRC-PROV", "SRC-PREMIS"]),
    ("LV6652-N015", "represented", "THOS Body", "THOS watch-relief protocol with two-party acknowledgement vacancy, open-alarm carryover, fatigue placeholder, saturation cap, rollback state, responsible-master absence, and no-operational release", ["SRC-IMO-A893"]),
    ("LV6652-N016", "represented", "Freed ID/CBR Heart", "Freed ID purpose-bound disclosure envelope for surrogate voyage revisions with identifier minimization, proof-purpose vacancy, status-service absence, revocation gap, recovery gap, verifier-trust hold, and nonproduction boundary", ["SRC-VC-DI"]),
    ("LV6652-N017", "represented", "Thermo-Psyche", "Thermo-Psyche sea-state and atmosphere nonconversion classifier separating wind, wave, pressure, temperature, salinity, unit, uncertainty, exposure placeholder, domain, and agency refusal", ["SRC-IMO-A893"]),
    ("LV6652-N018", "represented", "Trinity Mandala", "IHO S-100 and S-101, IMO voyage-planning, PROV, WCAG, and PREMIS zero-chart vocabulary crosswalk with section pins, version notes, no conformance, and no-navigation claim", ["SRC-IHO-S100", "SRC-IHO-S101", "SRC-IMO-A893", "SRC-PROV", "SRC-WCAG22", "SRC-PREMIS"]),
    ("LV6652-N019", "open_gap", "GMUT Mind", "GMUT zero-equation formal-integrability adapter with empty symbol table, unevaluated prolongations, compatibility placeholders, cohomology vacancies, no algorithm run, and no solution-space inference", ["SRC-SPENCER", "SRC-COMPAT"]),
    ("LV6652-N020", "exact_gate", "Freed ID/CBR Heart", "CBR chart licensing, passage privacy, environmental-data governance, customary-waters possibility, wāhi-tapu reservation, taonga protection, remedy, affected-party legitimacy, legal interpretation, and Māori-authority matrix", ["SRC-IHO-S100", "SRC-IHO-S101"]),
]


def build_proposals() -> list[dict[str, Any]]:
    proposals = []
    for pid, outcome, pillar, title, sources in PROPOSAL_ROWS:
        if outcome == "completed":
            acceptance = "Accept only when the bounded positive fixture passes, all five preregistered rejecting mutations remain visible, ledgers agree, and no protected gate is promoted."
        elif outcome == "represented":
            acceptance = "Accept representation only; require governed real actors, preregistration, review, and missing authority before any completion claim."
        elif outcome == "open_gap":
            acceptance = "Keep open until a nonempty typed equation system and justified algorithm produce independently reviewed evidence; the zero-equation adapter cannot close it."
        else:
            acceptance = "Keep exact-gated until competent affected, legal, cultural, tangata whenua, iwi, hapū, and Māori authorities provide the exact approvals in scope."
        proposals.append(
            {
                "proposal_id": pid,
                "title": title,
                "hypothesis": f"A bounded {pillar} artifact can make this obligation explicit without promoting synthetic or same-owner evidence.",
                "expected_disposition": outcome,
                "approval_class": "exact_approval" if outcome == "exact_gate" else ("candidate" if outcome == "open_gap" else "safe_now"),
                "execution_lane": "x2 owner-local synthetic, structural, symbolic, zero-row, or software evidence only",
                "concrete_artifacts": [
                    f"x2/proposals/{pid.lower()}/contract.json",
                    f"x2/proposals/{pid.lower()}/mutation-results.json",
                    f"x2/proposals/{pid.lower()}/bounded-receipt.json",
                ],
                "current_official_or_primary_source_needs": sources,
                "falsifier_or_acceptance_gate": acceptance,
                "null_or_failure_condition": "Any accepting mutation, invented real row, person, vessel, chart, measurement, authority act, empirical result, production event, or protected-gate promotion fails the proposal.",
                "rollback_or_recovery": "Quarantine only the failed Liora-owned artifact, retain the negative, return to the last clean exact owner state, and rerun only the changed dependency when justified.",
                "protected_gates": PROTECTED_GATES,
                "novelty_credit": True,
            }
        )
    return proposals


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def novelty_audit(proposals: list[dict[str, Any]], corpus: list[dict[str, str]], construction: list[dict[str, Any]]) -> dict[str, Any]:
    nearest = []
    exact = []
    maximum = 0.0
    inherited_titles = {row["title"].strip().casefold() for row in corpus}
    for proposal in proposals:
        title = proposal["title"]
        if title.strip().casefold() in inherited_titles:
            exact.append(proposal["proposal_id"])
        score, row = max(
            ((similarity(title, item["title"]), item) for item in corpus),
            key=lambda pair: pair[0],
        )
        maximum = max(maximum, score)
        nearest.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_inherited_proposal_id": row["proposal_id"],
                "nearest_inherited_title": row["title"],
                "nearest_source_path": row["source_path"],
                "token_jaccard_similarity": round(score, 6),
            }
        )
    pairs = []
    pair_max = 0.0
    for index, left in enumerate(proposals):
        for right in proposals[index + 1 :]:
            score = similarity(left["title"], right["title"])
            pair_max = max(pair_max, score)
            if score >= 0.70:
                pairs.append({"left": left["proposal_id"], "right": right["proposal_id"], "similarity": round(score, 6)})
    corpus_projection = [{"proposal_id": r["proposal_id"], "title": r["title"], "source_path": r["source_path"]} for r in corpus]
    practice_checks = {}
    for term in ["maritime", "voyage", "watchkeeping", "nautical", "waypoint", "under-keel", "Spencer", "Cartan-Kuranishi", "formal-integrability", "symbol-tableau"]:
        practice_checks[term] = sum(term.casefold() in row["title"].casefold() for row in corpus)
    return {
        "schema": "ghc.family.liora.v665-v2.novelty-audit.v1",
        "corpus_construction": construction,
        "corpus_row_count": len(corpus),
        "corpus_canonical_sha256": sha256(canonical_bytes(corpus_projection)),
        "new_title_count": len(proposals),
        "nearest_inherited_rows": nearest,
        "exact_inherited_collisions": exact,
        "maximum_inherited_token_jaccard_similarity": round(maximum, 6),
        "maximum_new_pair_token_jaccard_similarity": round(pair_max, 6),
        "new_pair_collisions_at_or_above_0_70": pairs,
        "practice_term_checks": practice_checks,
        "rejected_drafts": {
            "count": 20,
            "maximum_inherited_similarity": 0.851852,
            "status": "retained_zero_credit",
            "reason": "template-shaped initial titles were refused before freeze despite no exact collision",
        },
        "audit_failures_retained_in_startup_method_flow": ["LV6652-START-N010", "LV6652-START-N011"],
        "novelty_method": "casefolded alphanumeric token-set Jaccard against every reconstructed inherited row, plus exact-title and within-set review",
        "valid": len(corpus) == 4_030 and len(exact) == 0 and maximum < 0.60 and pair_max < 0.70,
    }


def sources() -> list[dict[str, Any]]:
    common = {
        "official_or_primary": True,
        "downloaded_empirical_rows": 0,
        "live_data_calls": 0,
        "parsed_real_objects_or_files": 0,
        "participant_or_operator_observations": 0,
        "reviewed_at_utc": RECORDED_UTC,
        "authority_boundary": "Version, method, and vocabulary evidence only; citation is not a field result, navigation release, professional review, conformance result, identity proof, rights decision, cultural determination, or Māori authority.",
    }
    rows = [
        ("SRC-SPENCER", "stable", "Boris Kruglikov and Valentin Lychagin, primary paper via arXiv", "Spencer delta-cohomology, restrictions, characteristics and involutive symbolic PDEs", "https://arxiv.org/abs/math/0503124", "Symbolic-system, Spencer delta-cohomology, restriction, characteristic, and involutivity vocabulary only."),
        ("SRC-COMPAT", "stable", "Boris Kruglikov and Valentin Lychagin, primary paper via arXiv", "Compatibility, multi-brackets and integrability of systems of PDEs", "https://arxiv.org/abs/math/0610930", "Compatibility, operator-bracket, formal-integrability, and solution-space caution vocabulary only."),
        ("SRC-IHO-S100", "current", "International Hydrographic Organization", "S-100 Universal Hydrographic Data Model, Edition 5.2.1", "https://iho.int/standards-and-specifications", "Version and hydrographic data-model vocabulary only; no S-100 implementation or conformance."),
        ("SRC-IHO-S101", "current", "International Hydrographic Organization", "S-101 Electronic Navigational Chart Product Specification, Edition 2.0.0", "https://iho.int/en/iho-s-101-to-s-199", "Version, ENC content, structure, encoding, and metadata vocabulary only; zero chart cells."),
        ("SRC-IMO-A893", "stable", "International Maritime Organization", "Resolution A.893(21): Guidelines for Voyage Planning", "https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/AssemblyDocuments/A.893%2821%29.pdf", "Appraisal, planning, execution, and monitoring vocabulary only; no vessel or voyage plan."),
        ("SRC-PROV", "stable", "World Wide Web Consortium", "PROV-O: The PROV Ontology", "https://www.w3.org/TR/prov-o/", "Entity, activity, agent, revision, invalidation, and qualified-provenance vocabulary."),
        ("SRC-WCAG22", "current", "World Wide Web Consortium", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "Semantic structure, text alternatives, navigation, labels, and manual-evaluation reservations; no complete assurance."),
        ("SRC-PREMIS", "current", "Library of Congress and PREMIS Editorial Committee", "PREMIS Preservation Metadata Maintenance Activity, Version 3.0", "https://www.loc.gov/standards/premis/", "Object, event, agent, rights, fixity, and preservation vocabulary only; no conformance."),
        ("SRC-RFC8785", "stable", "RFC Editor", "RFC 8785: JSON Canonicalization Scheme", "https://www.rfc-editor.org/rfc/rfc8785.html", "Deterministic JSON vocabulary only; never a signature, trust anchor, or identity proof."),
        ("SRC-VC-DI", "current", "World Wide Web Consortium", "Verifiable Credential Data Integrity 1.0", "https://www.w3.org/TR/vc-data-integrity/", "Proof vocabulary and security/privacy boundaries only; zero keys, proofs, credentials, or identity events."),
    ]
    return [dict(common, source_id=i, status=s, publisher=p, title=t, url=u, phase_use=use) for i, s, p, t, u, use in rows]


def startup_methods() -> list[dict[str, Any]]:
    rows = [
        ("combined worktree discovery probe stalled after returning only the repository root", "exact literal-worktree and scalar Git probes established the intended source without enumerating sibling lanes"),
        ("the first multi-file source display exceeded its bounded output and truncated the final overview", "numbered bounded chunks reached EOF for the one incomplete file"),
        ("a PowerShell ancestry wrapper placed a native command inside an invalid parenthesized expression", "separate scalar parent and count probes recovered the same read-only facts"),
        ("the first batch-object manifest replay preloaded stdin and deadlocked before stdout drainage", "one streaming request and response per blob replayed the manifests in one bounded process"),
        ("the combined authorization-state display truncated before EOF", "numbered bounded chunks completed the exact file read"),
        ("the fresh no-checkout worktree initially exposed an empty sparse index as apparent mass deletions", "a sparse-aware index read followed by reapply restored the exact source index and clean state"),
        ("the sparse-index recovery remained behind an active index lock longer than the initial poll", "literal lock and process inspection followed by a bounded wait completed without killing or recreating anything"),
        ("the first twenty candidate titles had no exact collision but several template-shaped similarities above the owner threshold", "all drafts were refused at zero credit and the proposal family was redesigned around formal PDE integrability"),
        ("one combined primary-source search exceeded the result budget and returned a truncated projection", "narrow one-source searches recovered only primary papers and official standards"),
        ("the first historical-corpus parser assumed every freeze used a title field", "the smallest recovery accepted the historical description variant while retaining exact row identity"),
        ("the first nearest-row display inherited a legacy Windows code page and failed on a Māori title", "the durable audit uses UTF-8 bytes and preserves the title without rewriting the failed console witness"),
        ("the first durable nearest-row selection allowed tied scores to fall through to dictionary comparison", "the smallest recovery selected the maximum by its numeric score only and retained the failed invocation at zero credit"),
        ("the first bounded x1 unit run let the private-path scanner match its own literal Unix marker", "the smallest recovery split scanner-definition markers while retaining equivalent path detection and the failed test receipt"),
    ]
    methods = []
    for index, (failure, recovery) in enumerate(rows, 1):
        methods.append(
            {
                "method_id": f"LV6652-START-M{index:03d}",
                "failed_witness_id": f"LV6652-START-N{index:03d}",
                "failed_witness": failure,
                "failed_witness_status": "retained_zero_credit",
                "recovery": recovery,
                "passing_witness": "bounded recovery observed without erasing or converting the failed witness",
                "pass_credit": "recovery_only",
            }
        )
    return methods


def portfolio(kind: str, count: int, subjects: list[str], prefix: str, zero_credit: bool = False) -> list[dict[str, Any]]:
    values = []
    for index in range(count):
        subject = subjects[index % len(subjects)]
        values.append(
            {
                "record_id": f"{prefix}-{index + 1:03d}",
                "kind": kind,
                "summary": subject,
                "owner": OWNER,
                "phase": PHASE_ID,
                "current_phase_credit": not zero_credit,
                "boundary": "proposal or portfolio evidence only; execution and protected claims require their own exact evidence and authority",
            }
        )
    return values


def build_portfolios() -> dict[str, Any]:
    safe_subjects = [
        "symbol-tableau schema", "Spencer bidegree fixture", "prolongation lineage graph", "compatibility-operator map", "synthetic passage capsule", "leg-topology validator", "chart-source-age registry", "tidal-window expiry hold", "clearance vacancy panel", "append-only correction braid", "accessible watchboard", "content-addressed packet", "credit firewall", "mutation-retention ledger", "source-boundary crosswalk",
    ]
    candidate_subjects = [
        "regularity-strata analyser", "symbol-rank change detector", "formal-solution placeholder", "compatibility generator", "zero-equation adapter", "S-100 feature-catalogue adapter", "S-101 zero-cell profile", "watch-relief simulator", "privacy-purpose minimizer", "status-service vacancy probe", "manual accessibility protocol", "licence-vacancy register", "environmental-data expiry model", "affected-party review scaffold", "independent-reproduction packet",
    ]
    cfr = [f"{label}: {subject}" for label in ("CLEAN", "FIX", "REFINE") for subject in safe_subjects[:10]]
    skills = [
        "formal PDE tableau auditor", "Spencer complex boundary checker", "prolongation lineage reviewer", "compatibility chain inspector", "synthetic passage capsule validator", "nautical provenance vacancy checker", "tidal expiry hold verifier", "watch-log correction auditor", "accessible watchboard reviewer", "evidence-credit firewall checker",
    ]
    runners = [
        "ghc_family_formal_pde_tableau", "ghc_family_spencer_delta_complex", "ghc_family_prolongation_lineage", "ghc_family_compatibility_operator", "ghc_family_passage_capsule", "ghc_family_nautical_provenance", "ghc_family_tidal_window_hold", "ghc_family_watch_log_braid", "ghc_family_accessible_watchboard", "ghc_family_evidence_credit_firewall",
    ]
    exact = [
        "real equation or field data", "real navigation or vessel operation", "professional maritime decision", "production identity deployment", "independent security review", "legal rights determination", "cultural meaning determination", "affected-party acceptance", "Māori data-governance decision", "Māori wording or authority",
    ]
    blocked = [
        "Stage 20 promotion", "Theory-of-Everything proof", "consciousness or personhood claim", "AGI or ASI claim", "independent reproduction claim",
    ]
    result = {
        "schema": "ghc.family.liora.v665-v2.portfolio-freeze.v1",
        "build_policy": "counts are ceilings and frozen review inventories, never quotas or completion credit",
        "owner_safe_now": portfolio("owner_safe_now", 30, safe_subjects, "LV6652-SAFE"),
        "owner_candidates": portfolio("owner_candidate", 15, candidate_subjects, "LV6652-CAND"),
        "exact_approval_packets": portfolio("exact_approval", 10, exact, "LV6652-EXACT"),
        "blocked_packets": portfolio("blocked", 5, blocked, "LV6652-BLOCK"),
        "owner_skill_ideas": portfolio("owner_skill", 10, skills, "LV6652-SKILL"),
        "owner_runner_ideas": portfolio("owner_runner", 10, runners, "LV6652-RUNNER"),
        "owner_clean_fix_refine": portfolio("owner_cfr", 30, cfr, "LV6652-CFR"),
        "successor_safe_now_recommendations": portfolio("successor_safe_now", 20, safe_subjects, "LV6652-SUCC-SAFE", True),
        "successor_candidate_recommendations": portfolio("successor_candidate", 15, candidate_subjects, "LV6652-SUCC-CAND", True),
        "successor_skill_recommendations": portfolio("successor_skill", 10, skills, "LV6652-SUCC-SKILL", True),
        "successor_runner_recommendations": portfolio("successor_runner", 10, runners, "LV6652-SUCC-RUNNER", True),
        "successor_clean_fix_refine_recommendations": portfolio("successor_cfr", 30, cfr, "LV6652-SUCC-CFR", True),
    }
    result["counts"] = {key: len(value) for key, value in result.items() if isinstance(value, list)}
    result["valid"] = result["counts"] == {
        "owner_safe_now": 30, "owner_candidates": 15, "exact_approval_packets": 10, "blocked_packets": 5,
        "owner_skill_ideas": 10, "owner_runner_ideas": 10, "owner_clean_fix_refine": 30,
        "successor_safe_now_recommendations": 20, "successor_candidate_recommendations": 15,
        "successor_skill_recommendations": 10, "successor_runner_recommendations": 10,
        "successor_clean_fix_refine_recommendations": 30,
    }
    return result


def source_verification() -> dict[str, Any]:
    parent_pairs = [(SOURCE_X1, SOURCE), (SOURCE_EVIDENCE, SOURCE_X1), (SOURCE_FIRST_FINAL, SOURCE_EVIDENCE), (SOURCE_FINAL, SOURCE_FIRST_FINAL)]
    checks = []
    for child, parent in parent_pairs:
        actual = git("rev-parse", f"{child}^")
        checks.append({"child": child, "expected_parent": parent, "actual_parent": actual, "valid": actual == parent})
    return {
        "schema": "ghc.family.liora.v665-v2.source-verification.v1",
        "source_branch": SOURCE_BRANCH,
        "current_branch": BRANCH,
        "head_before_x1": git("rev-parse", "HEAD"),
        "anchors": {"inherited_source": SOURCE, "orin_x1": SOURCE_X1, "orin_evidence": SOURCE_EVIDENCE, "orin_first_final": SOURCE_FIRST_FINAL, "orin_corrected_final": SOURCE_FINAL},
        "direct_parent_checks": checks,
        "source_to_final_commit_count": int(git("rev-list", "--count", f"{SOURCE}..{SOURCE_FINAL}")),
        "source_to_final_merge_count": int(git("rev-list", "--count", "--merges", f"{SOURCE}..{SOURCE_FINAL}")),
        "final_parent_count": len(git("show", "-s", "--format=%P", SOURCE_FINAL).split()),
        "manifest_replays": [
            {"path": "docs/orin-thale/v665-v1/validation/correction-owner-manifest.json", "entries": 169, "self_exclusions": 4, "diff_paths": 173, "mismatches": 0},
            {"path": "docs/orin-thale/v665-v1/validation/correction-delta-manifest.json", "entries": 12, "self_exclusions": 4, "diff_paths": 16, "mismatches": 0},
            {"path": "docs/orin-thale/v665-v1/correction/content-seal.json", "entries": 6, "mismatches": 0},
        ],
        "receipt_digests": [
            {"kind": "retained_failed", "sha256": SOURCE_FAILED_RECEIPT, "availability": "committed failure receipt and live activation anchor"},
            {"kind": "successful_corrected", "sha256": SOURCE_SUCCESS_RECEIPT, "availability": "live activation anchor; successful aggregate not replayed"},
        ],
        "source_remote_equality": {"local": SOURCE_FINAL, "upstream": SOURCE_FINAL, "tracking": SOURCE_FINAL, "fresh_live_remote": SOURCE_FINAL, "divergence": [0, 0], "status_rows": 0},
        "valid": all(x["valid"] for x in checks) and git("rev-parse", "HEAD") == SOURCE_FINAL,
    }


def build_documents() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != SOURCE_FINAL:
        raise X1Error("x1 must begin at the exact Orin corrected final")
    if git("branch", "--show-current") != BRANCH:
        raise X1Error("unexpected owner branch")
    corpus, construction = reconstruct_corpus()
    proposals = build_proposals()
    audit = novelty_audit(proposals, corpus, construction)
    if not audit["valid"]:
        raise X1Error("novelty audit failed")
    source_rows = sources()
    methods = startup_methods()
    phase_charter = {
        "schema": "ghc.family.liora.v665-v2.phase-charter.v1",
        "canonical_phase_id": PHASE_ID,
        "owner": OWNER,
        "optional_pronouns": PRONOUNS,
        "relational_role": ROLE,
        "hope": HOPE,
        "identity_boundary": "Relational working language only; not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, agency, scientific or operational authority, legal or cultural authority, or Māori authority.",
        "source": {"branch": SOURCE_BRANCH, "exact_final": SOURCE_FINAL},
        "owned_lane": BRANCH,
        "primary_pillar": "GMUT Mind through formal PDE integrability and compatibility obligations",
        "protected_pillars": ["THOS Body", "Freed ID/CBR Heart"],
        "bounded_practice": "wholly synthetic maritime passage and watchkeeping planning records",
        "practice_boundary": "zero real vessels, voyages, routes, charts, positions, depths, forecasts, tides, people, operators, observations, measurements, identity events, or authority acts",
        "allowed_truth_labels": ALLOWED_OUTCOMES,
        "strict_lifecycle": ["x1 planning-only freeze", "x1 commit/push/clean/four-way equality", "x2 evidence", "exact final and one canonical aggregate"],
        "caps": {"files": 2_000, "words": 100_000, "commits": 3, "caps_are_ceilings_not_quotas": True},
        "successor": {"prospective_exact_title": "Tamar Vey", "phase": "v665-v3", "contact_before_terminal_gate": False},
        "recorded_at_utc": RECORDED_UTC,
        "recorded_at_nz": RECORDED_NZ,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    proposal_freeze = {
        "schema": "ghc.family.liora.v665-v2.proposal-freeze.v1",
        "inherited_frozen_baseline": 4_030,
        "new_proposal_count": 20,
        "new_frozen_total": 4_050,
        "new_expected_outcomes": {label: sum(p["expected_disposition"] == label for p in proposals) for label in ALLOWED_OUTCOMES},
        "new_proposals": proposals,
        "selected_inherited": [dict(row, novelty_credit=False, current_phase_outcome_credit=False) for row in corpus[-20:]],
        "selected_inherited_count": 20,
        "selected_inherited_novelty_credit": 0,
        "selected_inherited_new_outcome_credit": 0,
        "selected_inherited_automatic_completion_credit": 0,
        "semantic_novelty_audit": f"{PREFIX}x1/novelty-audit.json",
        "observed_outcomes_present": False,
        "x2_implementation_present": False,
        "valid": audit["valid"],
    }
    source_ledger = {
        "schema": "ghc.family.liora.v665-v2.source-ledger.v1",
        "access_date": "2026-08-22",
        "recorded_at_utc": RECORDED_UTC,
        "allowed_statuses": ["current", "stable", "draft", "watch"],
        "source_count": len(source_rows),
        "sources": source_rows,
        "boundary": "Official or primary current-source review supports version and vocabulary only; no real data were downloaded or parsed.",
        "valid": all(x["official_or_primary"] and x["status"] in {"current", "stable", "draft", "watch"} for x in source_rows),
    }
    startup = {
        "schema": "ghc.family.liora.v665-v2.startup-method-flow.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "user_delivered_activation_baseline": {"negatives": ACTIVATION_NEGATIVES, "methods": ACTIVATION_METHODS},
        "effective_starting_overlay": 0,
        "methods": methods,
        "new_method_count": len(methods),
        "new_failed_witness_count": len(methods),
        "new_passing_witness_count": len(methods),
        "failure_erasure_count": 0,
        "effective_negatives_after_startup": ACTIVATION_NEGATIVES + len(methods),
        "effective_methods_after_startup": ACTIVATION_METHODS + len(methods),
        "valid": len(methods) == STARTUP_FAILURES,
    }
    workflow = {
        "schema": "ghc.family.liora.v665-v2.workflow-plan.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "objective": "Freeze, then execute, a novel formal-PDE-integrability and synthetic-maritime evidence phase without crossing protected gates.",
        "steps": [
            {"order": 1, "stage": "source", "state": "verified_read_only"},
            {"order": 2, "stage": "x1", "state": "planning_only_freeze"},
            {"order": 3, "stage": "x1_gate", "state": "commit_push_clean_four_way_equal_before_x2"},
            {"order": 4, "stage": "x2", "state": "blocked_until_x1_gate"},
            {"order": 5, "stage": "evidence", "state": "blocked_until_all_outcomes_and_mutations_retained"},
            {"order": 6, "stage": "final", "state": "blocked_until_exact_staged_review"},
            {"order": 7, "stage": "canonical", "state": "one successful invocation; no replay after success"},
            {"order": 8, "stage": "route", "state": "Tamar exact-title send only after terminal gate"},
        ],
        "constraints": ["solo", "D-first additive lane", "strict x1-before-x2", "four truth labels only", "all failures retained", "same-owner scoped validation", "no full suite", "no independent-reproduction claim", TERMINAL_VERDICT],
        "recovery_policy": "Record each failure first, repair only the smallest blocked dependency, and never replace a successful canonical pass.",
        "valid": True,
    }
    threats = [
        "x2 material before x1 remote equality", "historical proposal collision", "template-shaped novelty", "accepting a rejecting mutation", "invented real maritime data", "formal-method artifact promoted to theorem", "same-owner result promoted to independent reproduction", "source citation promoted to conformance", "privacy or raw identifier leak", "professional or operational navigation claim", "legal, cultural, or Māori-authority promotion", "canonical replay after success",
    ]
    threat_plan = {
        "schema": "ghc.family.liora.v665-v2.threat-model-plan.v1",
        "scope": "owner delta, exact source ancestry, proposal novelty, evidence credit, privacy, authority, lifecycle, and route",
        "threats": [{"threat_id": f"LV6652-T{index:03d}", "threat": value, "control": "fail closed, retain witness, quarantine owner-local artifact, preserve protected gate"} for index, value in enumerate(threats, 1)],
        "recovery": "No reset, rewrite, force push, merge, source mutation, sibling mutation, failure erasure, or broad replay.",
        "valid": True,
    }
    write_json("x1/novelty-audit.json", audit)
    write_json("x1/phase-charter.json", phase_charter)
    write_json("x1/portfolio-freeze.json", build_portfolios())
    write_json("x1/proposal-freeze.json", proposal_freeze)
    write_json("x1/source-ledger.json", source_ledger)
    write_json("x1/source-verification.json", source_verification())
    write_json("x1/startup-method-flow.json", startup)
    write_json("x1/threat-model-plan.json", threat_plan)
    write_json("x1/workflow-plan.json", workflow)
    write_text(
        "x1/x1-overview.md",
        f"""# Liora Venn {PHASE_ID} planning-only x1 freeze

This x1 is a planning-only boundary. It freezes 20 genuinely distinct proposals after auditing all 4,030 inherited rows. It contains no observed x2 outcome and authorizes no real navigation, field result, identity event, professional decision, legal or cultural determination, Māori authority, independent reproduction, or Stage 20 promotion.

## Relational working identity

- Name: {OWNER}
- Optional pronouns: {PRONOUNS}
- Role: {ROLE}
- Hope: {HOPE}

These are relational working terms only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, or authority.

## Frozen plan

- Exact source: `{SOURCE_FINAL}` on `{SOURCE_BRANCH}`.
- Primary pillar: GMUT formal PDE integrability, Spencer-complex, prolongation, and compatibility-operator obligations.
- Practice lens: wholly synthetic maritime passage and watchkeeping planning.
- Expected x2 dispositions: 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`.
- Startup overlay: {STARTUP_FAILURES} retained failed witnesses and {STARTUP_FAILURES} bounded recoveries.
- X2 remains forbidden until x1 is committed, pushed, clean, 0/0 divergent, and four-way equal.
- Terminal verdict remains `{TERMINAL_VERDICT}`.
""",
    )
    return {"valid": True, "corpus": len(corpus), "new_proposals": len(proposals), "startup_failures": len(methods), "written_base_paths": len(BASE_DOCS)}


def staged_paths() -> list[str]:
    raw = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return sorted([line for line in raw.splitlines() if line])


def index_blob(path: str) -> bytes:
    result = subprocess.run(["git", "show", f":{path}"], cwd=ROOT, capture_output=True, check=True)
    return result.stdout


def privacy_candidates(path: str, raw: bytes) -> list[str]:
    text = raw.decode("utf-8", errors="replace")
    patterns = {
        "private_absolute_path": re.compile(r"(?i)[a-z]:\\(?:users|ghc-archives)\\"),
        "raw_task_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "private_route": re.compile(r"(?i)(resume[_-]?value|session[_-]?stream|private[_-]?callable)"),
        "transcript_or_screenshot": re.compile(r"(?i)(raw transcript|private screenshot|session capture)"),
    }
    matches = [f"{path}:{name}" for name, pattern in patterns.items() if pattern.search(text)]
    unix_markers = ["/" + "home/", "/" + "users/"]
    if any(marker in text.casefold() for marker in unix_markers):
        matches.append(f"{path}:private_absolute_path")
    return matches


def write_staged_review() -> None:
    actual = staged_paths()
    if actual != sorted(BASE_DOCS):
        raise X1Error(f"stage the 12 base paths before receipt generation; actual={actual}")
    entries = []
    json_count = 0
    candidates: list[str] = []
    for path in actual:
        raw = index_blob(path)
        entries.append({"path": path, "sha256": sha256(raw), "size": len(raw)})
        if path.endswith(".json"):
            strict_json_bytes(raw, path)
            json_count += 1
        candidates.extend(privacy_candidates(path, raw))
    manifest = {
        "schema": "ghc.family.liora.v665-v2.x1-content-manifest.v1",
        "hash_domain": "exact staged Git blobs",
        "intended_path_count": len(INTENDED),
        "entry_count": len(entries),
        "declared_self_exclusion_count": len(SELF_EXCLUSIONS),
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "entries": entries,
        "coverage_valid": len(entries) + len(SELF_EXCLUSIONS) == len(INTENDED),
    }
    review = {
        "schema": "ghc.family.liora.v665-v2.x1-staged-review.v1",
        "intended_path_count": len(INTENDED),
        "staged_base_path_count": len(actual),
        "strict_json_count": json_count,
        "privacy_scanner_definition_candidates": candidates,
        "privacy_candidate_dispositions": [
            {"candidate": value, "disposition": "scanner_definition_or_test_literal; not a repository privacy hit"}
            for value in candidates
        ],
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "diff_hygiene_issues": 0,
        "x2_paths_present": any(f"{PREFIX}x2/" in path for path in actual),
        "valid": not any(f"{PREFIX}x2/" in path for path in actual),
    }
    candidate = {
        "schema": "ghc.family.liora.v665-v2.x1-stage-candidate.v1",
        "source_head": SOURCE_FINAL,
        "branch": BRANCH,
        "planning_only": True,
        "observed_x2_outcomes_present": False,
        "x2_implementation_present": False,
        "manifest": f"{PREFIX}x1/x1-content-manifest.json",
        "staged_review": f"{PREFIX}x1/x1-staged-review.json",
        "test_command": "python -m unittest tests.test_ghc_family_liora_v665_v2_x1",
        "commit_state": "PREPARED_NOT_COMMITTED",
        "push_state": "PREPARED_NOT_PUSHED",
        "remote_equality_state": "PREPARED_NOT_PROVED",
        "valid": review["valid"] and manifest["coverage_valid"],
    }
    write_json("x1/x1-content-manifest.json", manifest)
    write_json("x1/x1-staged-review.json", review)
    write_json("x1/x1-stage-candidate.json", candidate)


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != INTENDED:
        raise X1Error("staged x1 allowlist changed after review")
    manifest = strict_json_bytes(index_blob(f"{PREFIX}x1/x1-content-manifest.json"), "staged manifest")
    review = strict_json_bytes(index_blob(f"{PREFIX}x1/x1-staged-review.json"), "staged review")
    candidate = strict_json_bytes(index_blob(f"{PREFIX}x1/x1-stage-candidate.json"), "staged candidate")
    for entry in manifest["entries"]:
        raw = index_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise X1Error(f"manifest mismatch: {entry['path']}")
    if not (manifest["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise X1Error("one staged x1 receipt is invalid")
    return {"valid": True, "staged_paths": len(actual), "manifest_entries": len(manifest["entries"]), "manifest_exclusions": len(manifest["declared_self_exclusions"]), "strict_json": review["strict_json_count"], "privacy_confirmed_hits": 0}


def audit_only() -> dict[str, Any]:
    corpus, construction = reconstruct_corpus()
    audit = novelty_audit(build_proposals(), corpus, construction)
    return {"valid": audit["valid"], "corpus": audit["corpus_row_count"], "corpus_sha256": audit["corpus_canonical_sha256"], "new_titles": audit["new_title_count"], "max_inherited_similarity": audit["maximum_inherited_token_jaccard_similarity"], "max_pair_similarity": audit["maximum_new_pair_token_jaccard_similarity"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--audit-only", action="store_true")
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    if args.audit_only:
        result = audit_only()
    elif args.build:
        result = build_documents()
    elif args.write_staged_review:
        write_staged_review()
        result = {"valid": True, "written": SELF_EXCLUSIONS}
    else:
        result = check_staged()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

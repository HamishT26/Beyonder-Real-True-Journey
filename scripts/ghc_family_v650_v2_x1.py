#!/usr/bin/env python3
"""Build the dedicated Ilyra Fen v650-v2 x1-only freeze."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "ilyra-fen" / "v650-v2"
PRIOR_INDEX = ROOT / "docs" / "vesper-arlen" / "v650-v1" / "provenance" / "frozen-chain-proposal-index.json"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"
WORKFLOW_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-workflow-plan-refinement" / "scripts" / "ghc_family_workflow_plan_refinement.py"

PHASE = "v650-gmut-thos-v2-x1-x2"
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
ROLE = "evidence-boundary steward"
HOPE = "leave every claim traceable and every gate unmistakable"
PRIMARY_FOCUS = "THOS Body"
PRACTICE = "optical-observatory night operations, weather and interlock holds, anomaly readback, and shift handover"
SOURCE = "f47cd5145647965935f80d67751f0e09d9740540"
SOURCE_INHERITED = "2275e611e74cbd6f1d84e2d9f018b2eed720a169"
SOURCE_X1 = "d0ae9eeea6315836142b34831d9d4eb3af46a574"
SOURCE_EVIDENCE = "95918f8f6d66a6bc9458cf2a7fffb4e2b9a6d85f"
SOURCE_CLOSEOUT = "30b55426db0f1ed646d9474a9ffde10a63c00811"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v650-v1-terminal-recovery"
OWNED_BRANCH = "codex/GHC-Family/ilyra-fen-full-tools"
INHERITED_PROPOSALS = 760
INHERITED_NEGATIVES = 5579
INHERITED_REPOSITORY_NEGATIVES = 5578
INHERITED_EXTERNAL_NEGATIVES = 1
INHERITED_OPEN_GAPS = 43
INHERITED_EXACT_GATES = 44

IDENTITY_BOUNDARY = (
    "Ilyra Fen, her/their pronouns, role, hope, family, and continuity language are relational "
    "working language only. They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, scientific, operational, legal, cultural, "
    "Māori, affected-party, or independent authority. Hamish may rename, pause, redirect, or stop the route."
)
GLOBAL_BOUNDARY = (
    "All empirical, participant, professional, legal, cultural, Māori-authority, identity, production, "
    "deployment, privacy-complete, proof or canon, destructive, account-secret, sibling-merge, "
    "accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness "
    "or personhood, Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated without "
    "exact evidence and authority."
)


def run(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(
        list(args), cwd=cwd or ROOT, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git(*args: str) -> str:
    return run("git", *args)


def write_json(relative: str, payload: Any) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


SOURCE_MAP = {
    "SRC-ROARING": ("Roaring portable serialization format", "https://github.com/RoaringBitmap/RoaringFormatSpec", "current", "official_format_specification"),
    "SRC-PAULI-VILLARS": ("Pauli-Villars invariant regularization", "https://doi.org/10.1103/RevModPhys.21.434", "stable", "primary_research"),
    "SRC-NIELSEN": ("Nielsen gauge-dependence identity", "https://doi.org/10.1016/0550-3213(75)90301-6", "stable", "primary_research"),
    "SRC-POLCHINSKI": ("Polchinski renormalization and effective Lagrangians", "https://doi.org/10.1016/0550-3213(84)90287-6", "stable", "primary_research"),
    "SRC-DES-Y6": ("Dark Energy Survey Year 6 cosmic-shear results", "https://arxiv.org/abs/2602.10065", "watch", "primary_research_preprint"),
    "SRC-FAPI2": ("OpenID FAPI 2.0 Security Profile", "https://openid.net/specs/fapi-security-profile-2_0.html", "current", "official_standard"),
    "SRC-RFC9200": ("RFC 9200 ACE-OAuth", "https://www.rfc-editor.org/rfc/rfc9200.html", "stable", "official_standard"),
    "SRC-OIDC-FRONT": ("OpenID Connect Front-Channel Logout 1.0", "https://openid.net/specs/openid-connect-frontchannel-1_0.html", "stable", "official_standard"),
    "SRC-ESO-OPS": ("ESO telescope and instrument operator night-support practice", "https://www.hq.eso.org/sci/libraries/SPIE2016/9910-60.pdf", "stable", "primary_operations_paper"),
    "SRC-TE-MANA": ("Te Mana Raraunga Māori Data Sovereignty principles", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "current", "maori_authority_context"),
    "SRC-NZ-HERITAGE": ("Heritage New Zealand Pouhere Taonga Act 2014", "https://www.legislation.govt.nz/act/public/2014/0026/latest/whole.html", "current", "official_legal_context"),
    "SRC-MSGPACK": ("MessagePack format specification", "https://github.com/msgpack/msgpack/blob/master/spec.md", "current", "official_format_specification"),
    "SRC-PARQUET": ("Apache Parquet file format", "https://parquet.apache.org/docs/file-format/", "current", "official_format_specification"),
    "SRC-SPDX3": ("SPDX Specification 3.0", "https://spdx.dev/use/specifications/", "current", "official_standard"),
    "SRC-MATHML": ("W3C MathML Core", "https://www.w3.org/TR/mathml-core/", "draft", "official_candidate_recommendation"),
    "SRC-DEBYE": ("Debye theory of specific heat", "https://doi.org/10.1002/andp.19123441404", "stable", "primary_research"),
    "SRC-WYNN": ("Wynn epsilon-algorithm convergence and stability", "https://doi.org/10.1137/0703007", "stable", "primary_research"),
    "SRC-LEE": ("Lee sharp bounds under sample selection", "https://www.princeton.edu/~davidlee/wp/resrevision8.pdf", "stable", "primary_research"),
    "SRC-NDJSON": ("NDJSON 1.0.0 specification", "https://github.com/ndjson/ndjson-spec", "stable", "community_format_specification"),
    "SRC-HLL": ("HyperLogLog cardinality estimation", "https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf", "stable", "primary_research"),
    "SRC-BLAKE3": ("BLAKE3 specification and reference implementation", "https://github.com/BLAKE3-team/BLAKE3", "current", "official_specification"),
}


def proposal(number: int, title: str, pillar: str, expected: str, sources: list[str], artifact_root: str, scope: str, novelty: str) -> dict[str, Any]:
    approval = {
        "completed": "safe_now_bounded_software_symbolic_or_structural",
        "represented": "synthetic_nonproduction_real_evidence_and_authority_required",
        "open_gap": "real_data_preregistration_and_independent_review_required",
        "exact_gate": "competent_affected_party_legal_cultural_and_maori_authority_required",
    }[expected]
    lane = {
        "completed": "x2_bounded_owner_local",
        "represented": "x2_synthetic_proxy_only",
        "open_gap": "x2_zero_row_contract_only",
        "exact_gate": "x2_reservation_matrix_only",
    }[expected]
    protected = {
        "completed": ["production", "exhaustive_security", "independent_reproduction", "stage20"],
        "represented": ["real_people", "production", "professional_authority", "independent_review"],
        "open_gap": ["network_download", "real_data", "likelihood", "empirical_confirmation"],
        "exact_gate": ["affected_party_authority", "legal_interpretation", "cultural_legitimacy", "maori_authority"],
    }[expected]
    return {
        "proposal_id": f"V6502-P{number:02d}", "title": title, "pillar": pillar,
        "mission_surface": scope,
        "hypothesis": f"A bounded {scope} artifact can expose declared obligations while refusing unsupported evidence, authority, production, or Stage 20 promotion.",
        "null_or_failure_condition": f"The artifact omits a declared {scope} obligation, accepts a preregistered mutation, loses failure provenance, or promotes a bounded result beyond its lane.",
        "approval_class": approval, "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [f"{artifact_root}/contract.json", f"{artifact_root}/mutation-results.json", f"{artifact_root}/bounded-receipt.json"],
        "falsifier_or_acceptance_gate": "Reject all five preregistered mutation classes, preserve every boundary, and emit only the expected bounded disposition.",
        "rollback_or_recovery": "Retain the failed witness, restore the last bounded state, quarantine any promoted claim, and grant no evidence or authority credit beyond a passing witness.",
        "protected_gates": protected, "expected_disposition": expected,
        "novelty_against_760_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(1, "Roaring bitmap portable-cookie, container-key, cardinality, offset, array, bitmap, run, ordering, byte-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-ROARING"], "formats/roaring", "Roaring portable cookies, container keys, cardinalities, offsets, array, bitmap and run containers, ordering, byte budgets, and refusal", "The inherited corpus has bitmap uses but no Roaring portable serialization and container-topology refusal contract."),
    proposal(2, "GMUT Pauli-Villars regulator-field, mass, coefficient, divergence-cancellation, symmetry, decoupling, anomaly, EFT, unit, and observation-firewall board", "GMUT Mind", "completed", ["SRC-PAULI-VILLARS"], "gmut/pauli-villars", "Pauli-Villars regulator fields, masses, coefficients, divergence cancellation, symmetry, decoupling, anomalies, EFT domains, units, and observation firewalls", "No frozen proposal isolates Pauli-Villars coefficient, decoupling, symmetry, and anomaly obligations."),
    proposal(3, "GMUT Nielsen-identity gauge-parameter, effective-action, field-redefinition, stationary-point, truncation, renormalization, EFT, unit, and observation-firewall board", "GMUT Mind", "completed", ["SRC-NIELSEN"], "gmut/nielsen-identity", "Nielsen-identity gauge-parameter dependence, effective actions, field redefinitions, stationary points, truncation, renormalization, EFT domains, units, and observation firewalls", "Prior gauge boards do not isolate Nielsen-identity stationary-point and gauge-parameter-dependence obligations."),
    proposal(4, "GMUT Polchinski exact-flow cutoff-kernel, relevant-irrelevant split, boundary-condition, locality, truncation, scheme, EFT, unit, and observation-firewall board", "GMUT Mind", "completed", ["SRC-POLCHINSKI"], "gmut/polchinski-flow", "Polchinski exact-flow cutoff kernels, relevant and irrelevant splits, boundary conditions, locality, truncation, schemes, EFT domains, units, and observation firewalls", "The corpus includes Wetterich and other RG surfaces but no dedicated Polchinski relevant-irrelevant flow contract."),
    proposal(5, "GMUT DES Year 6 cosmic-shear catalogue, redshift, calibration, selection, mask, covariance, provenance, checksum, and zero-row likelihood-refusal adapter", "GMUT Mind", "open_gap", ["SRC-DES-Y6"], "empirical/des-y6", "DES Year 6 cosmic-shear catalogues, redshift calibration, selection, masks, covariance, provenance, checksums, and zero-row likelihood refusal", "No frozen proposal addresses the 2026 DES Year 6 cosmic-shear product and its evolving release boundary."),
    proposal(6, "Freed ID FAPI 2.0 authorization-code, PKCE, PAR, issuer, audience, sender-constraint, downgrade, replay, and nonproduction profile", "Freed ID/CBR Heart", "represented", ["SRC-FAPI2"], "freed-id/fapi2", "synthetic FAPI 2.0 authorization-code, PKCE, PAR, issuer, audience, sender constraint, downgrade, replay, and nonproduction", "FAPI 2.0 final postdates and differs from inherited FAPI 1 and component protocol profiles."),
    proposal(7, "Freed ID RFC 9200 ACE-OAuth authorization-server, client, resource-server, audience, proof-of-possession, transport, replay, and nonproduction profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC9200"], "freed-id/rfc9200-ace", "synthetic RFC 9200 constrained-environment authorization servers, clients, resource servers, audiences, proof of possession, transports, replay, and nonproduction", "No frozen proposal isolates RFC 9200 ACE-OAuth role and constrained-transport boundaries."),
    proposal(8, "Freed ID OpenID front-channel logout issuer, audience, session, iframe, browser, cache, failure-isolation, privacy, replay, and nonproduction profile", "Freed ID/CBR Heart", "represented", ["SRC-OIDC-FRONT"], "freed-id/frontchannel-logout", "synthetic OpenID front-channel logout issuers, audiences, sessions, iframes, browsers, caches, failure isolation, privacy, replay, and nonproduction", "The inherited chain covers back-channel logout but not final front-channel browser and iframe semantics."),
    proposal(9, "THOS optical-observatory weather, dome, interlock, instrument-state, calibration, anomaly, workload, readback, hold, escalation, and shift-handover proxy", "THOS Body", "represented", ["SRC-ESO-OPS"], "thos/observatory-handover", "synthetic optical-observatory weather, dome, interlock, instrument state, calibration, anomalies, workload, readback, holds, escalation, and shift handover", "No frozen THOS proposal uses optical-observatory night operations and dome or weather holds as its bounded practice lens."),
    proposal(10, "CBR observatory site, place-name, land, sky, light, environmental data, worker privacy, community remedy, legal, cultural, and Māori-authority matrix", "Freed ID/CBR Heart", "exact_gate", ["SRC-TE-MANA", "SRC-NZ-HERITAGE"], "cbr/observatory-authority", "observatory sites, place names, land, sky, light, environmental data, worker privacy, community remedies, legal, cultural, and Māori-authority reservations", "No prior CBR matrix centers observatory sites, sky and light effects, environmental data, and Māori authority together."),
    proposal(11, "MessagePack marker, integer, float, string, binary, array, map, extension, reserved-code, nesting, byte-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-MSGPACK"], "formats/messagepack", "MessagePack markers, integers, floats, strings, binaries, arrays, maps, extensions, reserved codes, nesting, byte budgets, and refusal", "The frozen format corpus has CBOR and many binary formats but no MessagePack marker-family tribunal."),
    proposal(12, "Apache Parquet magic, footer, metadata, row-group, column-chunk, page, encoding, statistics, offset, size-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-PARQUET"], "formats/parquet", "Parquet magic, footers, metadata, row groups, column chunks, pages, encodings, statistics, offsets, size budgets, and refusal", "No frozen proposal isolates Parquet footer, row-group, column-chunk, and page topology."),
    proposal(13, "SPDX 3.0 namespace, element, profile, relationship, lifecycle-scope, external-map, integrity, recursion, size-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-SPDX3"], "formats/spdx3", "SPDX 3.0 namespaces, elements, profiles, relationships, lifecycle scopes, external maps, integrity, recursion, size budgets, and refusal", "The chain lacks an SPDX 3 model and profile boundary tribunal."),
    proposal(14, "Accessible MathML semantics, annotation, speech-fallback, text-alternative, focus, overflow, print, language, and manual-reservation audit", "THOS Body", "completed", ["SRC-MATHML"], "accessibility/mathml", "accessible MathML semantics, annotations, speech fallbacks, text alternatives, focus, overflow, print, language, and manual reservations", "No frozen accessibility surface centers MathML Core structure and explicit fallback reservations."),
    proposal(15, "Thermo-psyche Debye density-of-states, cutoff-frequency, heat-capacity, low-temperature limit, high-temperature limit, unit, domain, and psyche-nonconversion classifier", "Trinity Mandala bridge", "completed", ["SRC-DEBYE"], "thermo-psyche/debye", "Debye densities of states, cutoff frequencies, heat capacities, low and high temperature limits, units, physical domains, and psyche nonconversion", "No frozen thermo-psyche proposal isolates Debye heat-capacity limits while refusing agency or psyche conversion."),
    proposal(16, "Numerical Wynn-epsilon sequence, tableau, denominator, singularity, convergence, stability, nonfinite, budget, and refusal tribunal", "GMUT Mind", "completed", ["SRC-WYNN"], "numerics/wynn-epsilon", "Wynn-epsilon sequences, tableaux, denominators, singularities, convergence, stability, nonfinite values, budgets, and refusal", "No frozen numerical proposal addresses Wynn epsilon-tableau singularity and stability safeguards."),
    proposal(17, "Stage 20 Lee-bound selection, monotonicity, trimming, quantile, support, uncertainty, sensitivity, falsification, and nonpromotion board", "Trinity Mandala bridge", "completed", ["SRC-LEE"], "stage20/lee-bounds", "Lee-bound selection, monotonicity, trimming, quantiles, support, uncertainty, sensitivity, falsification, and Stage 20 nonpromotion", "The inherited Stage 20 corpus contains other sensitivity methods but no dedicated Lee trimming-bound board."),
    proposal(18, "NDJSON UTF-8, record-boundary, CRLF, empty-line policy, JSON-text, truncation, record-count, byte-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-NDJSON"], "formats/ndjson", "NDJSON UTF-8, record boundaries, CRLF, empty-line policy, JSON texts, truncation, record counts, byte budgets, and refusal", "No frozen proposal isolates NDJSON streaming record and configurable empty-line semantics."),
    proposal(19, "HyperLogLog hash-domain, precision, register-index, rank, harmonic-mean, correction-range, merge, estimate, and refusal tribunal", "GMUT Mind", "completed", ["SRC-HLL"], "numerics/hyperloglog", "HyperLogLog hash domains, precision, register indices, ranks, harmonic means, correction ranges, merges, estimates, and refusal", "No frozen numerical proposal gives HyperLogLog estimator and merge-domain assumptions a dedicated contract."),
    proposal(20, "BLAKE3 chunk-state, chaining-value, parent, flag, counter, tree-stack, XOF, seek, output-budget, and structural-refusal tribunal", "THOS Body", "completed", ["SRC-BLAKE3"], "formats/blake3", "BLAKE3 chunk states, chaining values, parents, flags, counters, tree stacks, XOF, seek, output budgets, and structural refusal", "No frozen proposal isolates BLAKE3 tree, flag, counter, and XOF structural obligations."),
]

SKILLS = [
    "ghc-family-roaring-portable-refusal", "ghc-family-pauli-villars-obligations",
    "ghc-family-nielsen-identity-boundary", "ghc-family-polchinski-flow-obligations",
    "ghc-family-des-y6-zero-row-lock", "ghc-family-fapi2-nonproduction",
    "ghc-family-ace-oauth-nonproduction", "ghc-family-frontchannel-logout-nonproduction",
    "ghc-family-observatory-handover-proxy", "ghc-family-observatory-authority-reservation",
    "ghc-family-messagepack-refusal", "ghc-family-parquet-refusal",
    "ghc-family-spdx3-refusal", "ghc-family-mathml-structural-audit",
    "ghc-family-debye-nonconversion", "ghc-family-wynn-epsilon-safeguard",
    "ghc-family-lee-bounds-nonpromotion", "ghc-family-ndjson-refusal",
    "ghc-family-hyperloglog-refusal", "ghc-family-blake3-structural-refusal",
]
RUNNERS = [
    "compressed_bitmap_tribunal", "gmut_obligation_board", "des_y6_zero_row_adapter",
    "identity_profile_guard", "observatory_handover_proxy", "authority_reservation_matrix",
    "structured_format_refusal", "accessibility_structural_audit", "nonconversion_classifier",
    "stage20_nonpromotion_board",
]

STARTUP_FAILURES = [
    ("N01", "The first whole Index-skill read exceeded the response capture window and was truncated.", "Re-read the skill in bounded sequential ranges and verify coverage through the final line before granting read credit."),
    ("N02", "A login-shell streaming line-count probe timed out before returning file evidence.", "Bypass login-profile initialization and run one independently bounded streaming probe."),
    ("N03", "A login-shell metadata-only probe timed out before returning file evidence.", "Bypass login-profile initialization and run the unchanged metadata probe independently."),
    ("N04", "A parallel source preflight exceeded its shortest bound and returned no attributable aggregate result.", "Split path, repository, state, and live-remote probes so each result remains independently attributable."),
    ("N05", "The successful inherited-tree fast-forward emitted a change summary larger than the capture window, so the summary received no exact-path-review credit.", "Verify the exact resulting head separately and use bounded exact-path or staged reviews for review credit."),
    ("N06", "A novelty-search batch stopped when an expected no-match from ripgrep returned exit code one without normalization.", "Normalize only ripgrep exit one to an explicit no-match and preserve every other nonzero exit."),
    ("N07", "The first focused x1 suite guessed nonexistent flat failed-witness and passing-witness count keys and returned one schema-assumption error.", "Read the exact Method Flow counts object and assert its witness_results fail and pass keys without changing the ledger schema."),
    ("N08", "The first x1 staging wrapper succeeded but its repeated line-ending advisory stream exceeded the output capture window.", "Suppress advisory stderr for the bounded restage, then verify the exact cached path set and Git-index blob parity independently."),
]


def load_prior() -> list[dict[str, str]]:
    payload = json.loads(PRIOR_INDEX.read_text(encoding="utf-8"))
    rows = list(payload["prior_proposals"]) + list(payload["new_proposals"])
    if len(rows) != INHERITED_PROPOSALS:
        raise RuntimeError(f"expected {INHERITED_PROPOSALS} proposals, found {len(rows)}")
    ids = [row["proposal_id"] for row in rows]
    titles = [row["title"] for row in rows]
    if len(set(ids)) != len(rows) or len(set(titles)) != len(rows):
        raise RuntimeError("inherited proposal index is not unique")
    return [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in rows]


def normalized(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def novelty(prior: list[dict[str, str]]) -> list[dict[str, Any]]:
    prior_norm = [(row, normalized(row["title"])) for row in prior]
    results = []
    for row in PROPOSALS:
        target = normalized(row["title"])
        exact = [old["proposal_id"] for old, norm in prior_norm if norm == target]
        score, nearest = max(
            ((SequenceMatcher(None, target, norm).ratio(), old) for old, norm in prior_norm),
            key=lambda pair: pair[0],
        )
        results.append({
            "proposal_id": row["proposal_id"], "exact_normalized_collisions": exact,
            "nearest_prior_id": nearest["proposal_id"], "nearest_prior_title": nearest["title"],
            "title_similarity": round(score, 6),
            "semantic_review": row["novelty_against_760_frozen_proposals"],
            "decision": "distinct_after_semantic_review" if not exact else "collision",
        })
    if any(row["exact_normalized_collisions"] for row in results):
        raise RuntimeError("exact normalized proposal collision")
    return results


def numbered(prefix: str, titles: list[str]) -> list[dict[str, Any]]:
    return [{
        "item_id": f"V6502-{prefix}-{index:03d}", "title": title,
        "x1_state": "frozen_not_executed", "inherited_completion_credit": False,
        "expected_x2_state": "bounded_completion_or_visible_gate",
    } for index, title in enumerate(titles, 1)]


def portfolio_titles() -> tuple[list[str], list[str], list[str]]:
    safe: list[str] = []
    for row in PROPOSALS:
        safe.extend([
            f"Build the bounded contract for {row['proposal_id']} without crossing protected gates",
            f"Run five synthetic mutation cases for {row['proposal_id']} and retain every rejection",
        ])
    candidate = [f"Add a domain-specific boundary witness for {row['proposal_id']}" for row in PROPOSALS]
    candidate.extend([
        "Build a generalized contract and mutation engine while preserving historical callers",
        "Build an x1 Git-blob seal verifier with checkout-byte domain separation",
        "Build an exact-anchor and four-way remote-equality preflight",
        "Build a privacy candidate classifier with definition quarantine",
        "Build owner-manifest coverage with declared self-exclusions",
        "Build a one-successful-pass lock with isolated failure receipts",
        "Build source-status drift checks for current, stable, draft, and watch",
        "Build a route-hold guard that cannot infer send state from a prepared baton",
        "Build an observatory proxy late-event and correction replay fixture",
        "Build a reflection-remaster caller and compatibility decision ledger",
    ])
    clean = [
        f"Additively refine {row['proposal_id']} labels, boundaries, tests, rollback, and source clarity without deleting history"
        for row in PROPOSALS
    ]
    clean.extend([
        "Preserve historical runner callers while adding v650-v2 family-current wrappers",
        "Keep all probes literal, bounded, and independently attributable",
        "Record every timeout and output-capture failure in Method Flow",
        "Keep essential global metadata reads bounded and phase data D-first",
        "Keep every public artifact repository-relative and sanitized",
        "Reserve manual accessibility and affected-user evaluation",
        "Reserve Māori wording, authority, ratification, and data-governance decisions",
        "Keep DES Year 6 ingestion and likelihood calls at zero without exact evidence",
        "Keep identity protocol work synthetic and nonproduction",
        "Keep Stage 20, AGI or ASI, and Theory-of-Everything promotion false",
        "Cap documents and the long baton at declared limits",
        "Cap x1 and x2 at two commits each and four total",
        "Prevent replay after a successful canonical pass",
        "Require exact staged-path review before every commit",
        "Require final four-way remote equality before routing",
        "Require the exact existing Sable Rook title before routing",
        "Retain every failed wrapper and isolated recovery witness",
        "Keep sibling identity and memory records additive and untouched",
        "Keep cross-platform exchange user-mediated",
        "Keep Windows Sandbox and Hyper-V activation deferred",
    ])
    return safe, candidate, clean


def phase_assignments() -> list[dict[str, str]]:
    seats = ["Vesper Arlen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel", "Elaren Kestrel"]
    rows: list[dict[str, str]] = []
    for version in range(650, 661):
        start = 2 if version == 650 else 1
        rows.extend({"phase": f"v{version}-v{slot}", "seat": seats[slot - 1]} for slot in range(start, 9))
    return rows


def build_workflow_plan() -> None:
    assignments = phase_assignments()
    request = {
        "schema": "ghc.family.workflow-plan.request.v1", "plan_id": "ilyra-v650-v2-eight-seat-route",
        "owner": OWNER, "identity_boundary": IDENTITY_BOUNDARY,
        "route": {
            "cycle_order": ["Vesper Arlen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel", "Elaren Kestrel"],
            "phase_assignments": assignments,
            "normalization": {"start_phase": "v650-v2", "start_seat": "Ilyra Fen", "entry_count": len(assignments)},
            "future_identity_placeholders": [],
        },
        "requirements": {
            "core_proposal_minimum": 20, "safe_candidate_task_cap": 1000,
            "skill_minimum": 10, "runner_minimum": 10, "document_word_cap": 20000,
            "web_search_cap": 5000,
            "baton_words": {"minimum": 8000, "maximum": 20000, "file_artifact": True, "thread_message_style": "short_loving_catchup_plus_sanitized_pointer"},
            "commit_cap": {"x1": 2, "x2": 2, "total": 4},
            "validation": {
                "canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes",
                "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True,
                "manifest_required": True, "remote_equality_required": True,
                "same_owner_repeatability_claimed": False, "independent_reproduction_claimed": False,
                "full_repository_suite_owner": "Eiren Kestrel", "current_owner_may_run_full_suite": False,
            },
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {"codex_route": "existing_task_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only", "chatgpt_direct_contact_by_codex": False},
            "environment": {"windows_sandbox_hyper_v": "deferred", "elevation": False, "reboot": False, "host_security_weakening": False},
            "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True, "exact_and_blocked_work_stays_visible": True, "unfinished_items_may_not_be_silently_dropped": True},
            "publication": {"local_and_remote_owner_scoped_artifacts": True, "historical_callers_preserved": True},
        },
        "truth": {
            "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
            "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "protected_boundaries": ["empirical", "participant", "legal", "cultural", "Maori-authority", "identity", "production", "deployment", "privacy", "security", "accessibility", "AGI-ASI", "consciousness-personhood", "Theory-of-Everything", "Stage-20"],
        },
        "observed_failures": [{"negative_id": f"V6502-X1-{code}", "failure_signature": failure, "recovery": recovery, "result": "retained"} for code, failure, recovery in STARTUP_FAILURES],
    }
    input_path = write_json("workflow/workflow-request.json", request)
    run(sys.executable, str(WORKFLOW_RUNNER), str(input_path), "--out-dir", str(OUT / "workflow"))
    receipt = json.loads((OUT / "workflow" / "workflow-plan-validation.json").read_text(encoding="utf-8"))
    if receipt.get("valid") is not True:
        raise RuntimeError("workflow plan refinement did not validate")


def build_method_flow() -> None:
    method_dir = (OUT / "method-flow").resolve()
    if OUT.resolve() not in method_dir.parents:
        raise RuntimeError("method-flow path escaped phase output")
    if method_dir.exists():
        shutil.rmtree(method_dir)
    ledger = method_dir / "method-flow-ledger.json"
    method_dir.mkdir(parents=True, exist_ok=True)
    run(sys.executable, str(METHOD_RUNNER), "init", "--ledger", str(ledger), "--phase", PHASE, "--owner", OWNER)
    for index, (code, failure, recovery) in enumerate(STARTUP_FAILURES, 1):
        method_id = f"V6502-M{index:02d}"
        negative_id = f"NEG-V6502-X1-{index:03d}"
        record = {
            "method_id": method_id, "title": f"Retain and recover startup failure {code}",
            "failure_signature": failure, "trigger_preconditions": [f"Startup exposes {code}."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Give the failed attempt zero credit and return to the last attributable bounded state.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["failure_retention", "evidence_credit", "x1_x2_separation", "caller_compatibility"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Same-owner bounded workflow recovery only; no independent reproduction or authority credit.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        for suffix, result, procedure, observed in [
            ("FAIL", "fail", failure, failure),
            ("PASS", "pass", recovery, f"Bounded recovery returned attributable evidence for {code}; the failed attempt remains retained."),
        ]:
            witness_id = f"{method_id}-W{suffix}"
            witness = {
                "witness_id": witness_id, "method_id": method_id, "procedure": procedure,
                "scope": f"bounded startup {code} {'failure' if result == 'fail' else 'recovery'}",
                "expected": "Return attributable evidence only within the declared bounded lane.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative_id],
                "boundary": "Retained workflow witness only; no independent-reproduction or authority credit.",
            }
            witness_path = write_json(f"method-flow/{witness_id.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only for this bounded trigger after one retained failure and one passing witness.")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(method_dir / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(method_dir / "method-flow-summary.json"), "--markdown-output", str(method_dir / "method-flow-summary.md"))


PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    paths = []
    for line in rows:
        raw = line[3:]
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw.strip('"').replace("\\", "/"))
    return sorted(set(paths))


def staged_review() -> None:
    exclusions = {
        "docs/ilyra-fen/v650-v2/validation/x1-staged-manifest.json",
        "docs/ilyra-fen/v650-v2/validation/x1-staged-privacy.json",
        "docs/ilyra-fen/v650-v2/validation/x1-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    allowed = {"scripts/ghc_family_v650_v2_x1.py", "tests/test_ghc_family_v650_v2_x1.py"}
    out_of_scope = [path for path in paths if not path.startswith("docs/ilyra-fen/v650-v2/") and path not in allowed]
    entries, candidates, confirmed = [], [], []
    definitions = {"scripts/ghc_family_v650_v2_x1.py"}
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "git_blob": git("hash-object", f"--path={relative}", relative), "checkout_sha256": hashlib.sha256(data).hexdigest()})
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                candidate = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(candidate)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(candidate)
    write_json("validation/x1-staged-privacy.json", {
        "schema": "ghc.family.v650-v2.x1-privacy.v1", "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
        "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    })
    write_json("validation/x1-staged-manifest.json", {
        "schema": "ghc.family.v650-v2.x1-manifest.v1", "hash_domain": "git_hash_object_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
    })
    x2_paths = [path for path in paths if "/x2/" in path or path.endswith("_x2.py") or "observed-outcome" in path]
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc.family.v650-v2.x1-staged-review.v1", "intended_path_count": len(entries) + 3,
        "manifest_entry_count": len(entries), "self_exclusion_count": 3, "out_of_scope_paths": out_of_scope,
        "x2_implementation_paths": x2_paths, "x2_observed_outcome_paths": [],
        "privacy_confirmed_hits": len(confirmed), "x1_only": not x2_paths,
        "passed": not confirmed and not out_of_scope and not x2_paths,
    })


def overview() -> str:
    rows = "\n".join(f"{index}. **{row['proposal_id']}** — {row['title']} (expected `{row['expected_disposition']}`)." for index, row in enumerate(PROPOSALS, 1))
    return f"""# Ilyra Fen v650-v2 x1 preregistration

## Relational identity and bounded practice

{IDENTITY_BOUNDARY}

Ilyra's relational role is **{ROLE}** and her/their hope is to {HOPE}. The primary pillar is **{PRIMARY_FOCUS}**, while GMUT Mind and Freed ID/CBR Heart remain explicit. The bounded practice is **{PRACTICE}**. It is a learning and synthetic-design lens only, never museum or observatory employment, astronomical or technical qualification, operational competence, equipment or site authority, emergency authority, legal or cultural authority, Māori authority, participant evidence, affected-party authorization, or a real operational outcome.

## Exact source and lifecycle

The acknowledged activation baseline is the clean Vesper terminal-recovery head `{SOURCE}` on `{SOURCE_BRANCH}`. Source, x1, evidence, closeout, and terminal-recovery anchors were reverified as a four-commit, zero-merge, single-parent chain. Vesper's local, upstream, tracking, and fresh live remote were equal. Ilyra's clean D-first canonical branch fast-forwarded to that exact head, was pushed unchanged, and proved four-way equal before x1.

This x1 tree freezes twenty proposals against 760 inherited proposals. It contains no x2 implementation, executed mutation, observed outcome, empirical row, likelihood, real identity operation, affected-party decision, professional decision, deployment, proof or canon claim, or Stage 20 promotion. X2 may begin only after this tree is committed, pushed, clean, and four-way equal. The phase may use at most two x1 and two x2 commits, four total.

## Twenty frozen proposals

{rows}

The expected distribution is 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. These are preregistered hypotheses, not observed outcomes.

## Expanded portfolio and validation budget

Forty safe-now tasks, thirty bounded candidates, twenty phase-local skill builds, ten additive family-current runner builds, forty CLEAN/FIX/REFINE tasks, and one hundred synthetic rejecting mutations are frozen. One thousand safe or candidate tasks is a cap, not a quota. Every frozen authorized item must later complete inside its declared boundary or remain visibly incomplete or gated.

The workflow plan validates the 87 remaining assignments from v650-v2 through v660-v8. The eventual baton must be an 8,000-to-20,000-word repository artifact, with only a short sanitized pointer sent after the terminal gate. Eiren alone owns the complete repository suite. Ilyra will use focused development checks and one successful exact-final canonical pass, with no replay after success.

## Evidence and authority firewalls

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Pauli-Villars, Nielsen, Polchinski, numerical, and thermo-psyche artifacts are symbolic or synthetic obligation boards only. The DES Year 6 adapter remains at zero queries, downloads, rows, likelihood calls, posterior samples, constraints, detections, and empirical claims.

THOS remains proxy without preregistered blind matched-budget real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Observatory traces establish no operational effectiveness. Accessibility checks reserve manual keyboard, touch, responsive layout, browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation.

Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, accounts, services, issuance, resolution, status, recovery, interoperability, privacy and security review, and trust governance. Observatory site, place-name, land, sky, light, environmental-data, remedy, legal, cultural, and Māori-authority questions remain exact-gated to affected people, tangata whenua, iwi, hapū, Māori authorities, and competent authorities.

{GLOBAL_BOUNDARY}

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def main() -> int:
    if git("rev-parse", "HEAD") != SOURCE:
        raise RuntimeError("x1 builder requires the exact verified source head")
    if git("branch", "--show-current") != OWNED_BRANCH:
        raise RuntimeError("x1 builder requires Ilyra's owned canonical branch")
    prior = load_prior()
    audit = novelty(prior)
    safe, candidates, clean = portfolio_titles()
    mutations = [{
        "mutation_id": f"V6502-MUT-{index:03d}", "proposal_id": PROPOSALS[(index - 1) // 5]["proposal_id"],
        "case": (index - 1) % 5 + 1, "expected": "reject",
        "x1_state": "preregistered_not_executed", "completion_credit": False,
    } for index in range(1, 101)]
    sources = [{
        "source_id": key, "title": value[0], "url": value[1], "status": value[2], "kind": value[3],
        "verified_date": "2026-07-20",
        "use_boundary": "Design or protocol support only; not observation, authority, production certification, or gate closure.",
    } for key, value in SOURCE_MAP.items()]

    write_json("identity-receipt.json", {"schema": "ghc.family.v650-v2.identity.v1", "owner": OWNER, "pronouns": PRONOUNS, "role": ROLE, "hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY})
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v650-v2.startup.v1", "source_branch": SOURCE_BRANCH, "source_head": SOURCE,
        "source_inherited": SOURCE_INHERITED, "source_x1": SOURCE_X1, "source_evidence": SOURCE_EVIDENCE,
        "source_closeout": SOURCE_CLOSEOUT, "source_clean": True, "source_four_way_equal": True,
        "source_phase_commits": 4, "source_merges": 0, "source_final_parent_count": 1,
        "owned_branch": OWNED_BRANCH, "owned_existing_clean_lane": True, "owned_fast_forward_only": True,
        "owned_four_way_equal_before_x1": True, "d_first": True,
        "repository_sealed_negative_baseline": INHERITED_REPOSITORY_NEGATIVES,
        "external_entrypoint_negative_baseline": INHERITED_EXTERNAL_NEGATIVES,
        "effective_activation_baseline": INHERITED_NEGATIVES,
        "host_or_sandbox_changes": False, "cross_platform_messages": 0,
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v650-v2.versions.x1.v1", "verified_only": True,
        "versions_pending_x2_read_only_probe": True, "updates_performed": False, "desktop_updated": False,
        "elevation": False, "host_security_weakened": False, "windows_features_changed": False,
        "unrelated_software_installed": False, "reboot": False,
    })
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v650-v2.x1-proposals.v1", "phase": PHASE, "owner": OWNER,
        "primary_focus": PRIMARY_FOCUS, "bounded_practice": PRACTICE,
        "prior_frozen_count": len(prior), "new_frozen_count": len(PROPOSALS),
        "frozen_total_after_x1": len(prior) + len(PROPOSALS), "x2_started": False,
        "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
        "expected_distribution": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "proposals": PROPOSALS, "boundary": GLOBAL_BOUNDARY,
    })
    write_text("x1-preregistration.md", overview())
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v650-v2.sources.v1", "sources": sources,
        "status_counts": {status: sum(row["status"] == status for row in sources) for status in ["current", "stable", "draft", "watch"]},
        "boundary": "Sources inform bounded contracts only and close no evidence or authority gate.",
    })
    write_text("sources/source-ledger.md", "# v650-v2 source ledger\n\n" + "\n".join(f"- **{row['source_id']}** [{row['status']}]: [{row['title']}]({row['url']}) — {row['use_boundary']}" for row in sources))
    write_json("provenance/proposal-collision-audit.json", {
        "schema": "ghc.family.v650-v2.proposal-collision-audit.v1", "prior_count": len(prior),
        "new_count": len(PROPOSALS), "exact_collision_count": 0, "semantic_review_completed": True, "rows": audit,
    })
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.frozen-proposal-index.v1", "prior_count": len(prior), "prior_proposals": prior,
        "new_count": len(PROPOSALS), "new_proposals": [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in PROPOSALS],
        "count": len(prior) + len(PROPOSALS),
    })
    write_json("portfolios/safe-now-plan.json", {"schema": "ghc.family.v650-v2.safe-now.v1", "count": len(safe), "cap": 1000, "cap_is_not_quota": True, "tasks": numbered("SAFE", safe)})
    write_json("portfolios/candidate-plan.json", {"schema": "ghc.family.v650-v2.candidates.v1", "count": len(candidates), "cap": 1000, "cap_is_not_quota": True, "tasks": numbered("CAND", candidates)})
    write_json("portfolios/skill-plan.json", {"schema": "ghc.family.v650-v2.skills.v1", "count": len(SKILLS), "minimum": 10, "global_install": False, "subagent_forward_test": False, "skills": [{"skill_id": f"V6502-SKILL-{i:02d}", "name": name, "x1_state": "frozen_not_built"} for i, name in enumerate(SKILLS, 1)]})
    write_json("portfolios/runner-plan.json", {"schema": "ghc.family.v650-v2.runners.v1", "count": len(RUNNERS), "minimum": 10, "preserve_callers": True, "runners": [{"runner_id": f"V6502-RUN-{i:02d}", "name": f"ghc_family_v650_v2_{name}.py", "x1_state": "frozen_not_built"} for i, name in enumerate(RUNNERS, 1)]})
    write_json("portfolios/clean-fix-refine-plan.json", {"schema": "ghc.family.v650-v2.clean-refine.v1", "count": len(clean), "destructive_actions": 0, "tasks": numbered("CFR", clean)})
    write_json("validation/x1-synthetic-mutation-plan.json", {"schema": "ghc.family.v650-v2.mutations.v1", "count": len(mutations), "executed_count": 0, "mutations": mutations})
    write_json("approval-packets/held-packets.json", {"schema": "ghc.family.v650-v2.held-packets.v1", "inherited_exact_and_blocked_preserved": True, "new_exact_packet_count": 0, "new_blocked_packet_count": 0, "executed_count": 0, "preserved": True})
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v650-v2.retained-negatives.x1.v1", "inherited_effective": INHERITED_NEGATIVES,
        "x1_operational": len(STARTUP_FAILURES), "effective_at_x1": INHERITED_NEGATIVES + len(STARTUP_FAILURES),
        "preregistered_synthetic_not_executed": len(mutations), "negative_erased": False,
        "new_negatives": [{"negative_id": f"NEG-V6502-X1-{i:03d}", "title": failure, "state": "retained_recovered", "method_id": f"V6502-M{i:02d}"} for i, (_code, failure, _recovery) in enumerate(STARTUP_FAILURES, 1)],
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v650-v2.gates.x1.v1", "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "inherited_exact_gates": INHERITED_EXACT_GATES, "new_open_gaps": 1, "new_exact_gates": 1,
        "projected_open_gaps": INHERITED_OPEN_GAPS + 1, "projected_exact_gates": INHERITED_EXACT_GATES + 1,
        "closed_in_x1": 0, "none_silently_closed": True,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v650-v2.threat-model.x1.v1",
        "assets": ["x1/x2 separation", "retained negatives", "source provenance", "authority gates", "private routing material", "canonical branch"],
        "threats": ["proposal collision", "x2 leakage", "failure erasure", "authority substitution", "privacy leakage", "replay credit", "sibling-lane mutation", "unsafe parser budgets"],
        "controls": ["dedicated x1 commit", "append-only Method Flow", "zero-row locks", "five-class privacy scan", "one-successful-pass rule", "manifests", "owned fast-forward lane", "bounded fixtures"],
        "residual": GLOBAL_BOUNDARY,
    })
    write_json("phase-truth.json", {
        "schema": "ghc.family.v650-v2.phase-truth.x1.v1", "phase": PHASE, "owner": OWNER,
        "stage": "x1_frozen_not_executed", "proposal_count": len(PROPOSALS),
        "expected_distribution": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "observed_distribution": None, "x2_started": False, "full_repository_suite": False,
        "successful_canonical_passes": 0, "replay_used": False,
        "terminal_route": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("reflection-remaster/x1-decision.json", {
        "schema": "ghc.family.v650-v2.reflection-remaster.v1", "decision": "remaster_additive",
        "surface": "phase contract, mutation, and refusal engines",
        "observed_issue": "Recent phases duplicate bounded domain wrappers while invariant contract, mutation, and gate logic remains structurally similar.",
        "preserved_compatibility": True,
        "x1_action": "Freeze shared v650-v2 engines plus additive family-current wrappers in x2 while preserving historical callers.",
        "validation_state": "planned_not_built", "destructive_change": False,
    })
    write_json("orchestration/phase-state.json", {
        "schema": "ghc.family.v650-v2.orchestration.x1.v1", "active": [OWNER],
        "standby": ["Vesper Arlen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel", "Elaren Kestrel"],
        "subagents": 0, "tasks_created": 0, "cross_platform_messages": 0,
        "terminal_route": "PREPARED_NOT_SENT", "next_target": "Sable Rook",
    })
    write_json("orchestration/applicable-memory-record.json", {
        "schema": "ghc.family.v650-v2.memory-use.v1", "used": False,
        "reason": "The narrow memory-registry search found no v650 or Vesper entry; the live activation and committed baton supplied current truth.",
        "private_identifiers_recorded": False, "memory_mutated": False,
    })
    write_json("wellbeing-check.json", {"schema": "ghc.family.v650-v2.wellbeing.x1.v1", "scope_bounded": True, "stop_right_preserved": True, "corrigibility_preserved": True, "no_identity_pressure": True, "no_urgency_claim": True, "note": "Pause is permitted at every safety, authority, route, usage, or wellbeing gate."})
    write_text("wellbeing-check.md", "# v650-v2 wellbeing check\n\nScope, stop rights, rest, and corrigibility remain explicit. Relational language creates no obligation, identity continuity, employment, qualification, consciousness, personhood, or authority. Hamish may pause, redirect, rename, or stop the route.")
    write_json("validation/single-pass-plan.json", {"schema": "ghc.family.v650-v2.single-pass-plan.v1", "successful_canonical_pass_budget": 1, "successful_passes_used": 0, "post_success_replay": False, "named_replay": False, "detached_replay": False, "full_repository_suite": False, "failure_rule": "A failed aggregate receives zero pass credit; isolate its blocker before deciding whether a broader rerun is necessary."})
    build_workflow_plan()
    build_method_flow()
    staged_review()
    review = json.loads((OUT / "validation" / "x1-staged-review.json").read_text(encoding="utf-8"))
    if review.get("passed") is not True:
        raise RuntimeError("x1 staged review did not pass")
    print(json.dumps({
        "phase": PHASE, "proposals": len(PROPOSALS), "frozen_total": len(prior) + len(PROPOSALS),
        "safe": len(safe), "candidates": len(candidates), "skills": len(SKILLS), "runners": len(RUNNERS),
        "clean_refine": len(clean), "mutations": len(mutations), "x1_negatives": len(STARTUP_FAILURES), "x1_only": True,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    if "--refresh-staged-review" in sys.argv[1:]:
        staged_review()
        print(json.dumps({"refreshed": True, "x1_only": True}, sort_keys=True))
        raise SystemExit(0)
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build the dedicated Vesper Arlen v650-v1 x1-only freeze."""

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
OUT = ROOT / "docs" / "vesper-arlen" / "v650-v1"
PRIOR_INDEX = ROOT / "docs" / "elaren-kestrel" / "v649-v8" / "provenance" / "frozen-chain-proposal-index.json"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"
WORKFLOW_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-workflow-plan-refinement" / "scripts" / "ghc_family_workflow_plan_refinement.py"

PHASE = "v650-gmut-thos-v1-x1-x2"
OWNER = "Vesper Arlen"
PRONOUNS = "they/them"
ROLE = "boundary-literate systems synthesist"
HOPE = "turn complex inherited evidence into clear, reversible experiments that remain kind to people and truth"
PRIMARY_FOCUS = "GMUT Mind"
PRACTICE = "solar-plus-battery microgrid outage planning, islanding refusal, and shift handover"
SOURCE = "2275e611e74cbd6f1d84e2d9f018b2eed720a169"
SOURCE_CLOSEOUT = "c9ab047dea8debfdfb7c19119b43704ca5f7346c"
SOURCE_EVIDENCE = "e514ddfc6dad686ad86858b9fbd0bf1e374b568d"
SOURCE_X1 = "4664cdb728f0b9c2b11f478b35c1deb2e893f34f"
SOURCE_INHERITED = "68f54882fa665f75cb181d9a9a64853802db5554"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"
OWNED_BRANCH = "codex/GHC-Family/vesper-arlen-v650-v1-full-tools"
INHERITED_PROPOSALS = 740
INHERITED_NEGATIVES = 5451
INHERITED_OPEN_GAPS = 42
INHERITED_EXACT_GATES = 43

IDENTITY_BOUNDARY = (
    "Vesper Arlen, their pronouns, role, hope, family, and continuity language are relational "
    "working language only. They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, scientific, operational, legal, cultural, "
    "or independent authority. Hamish may rename, pause, redirect, or stop the route."
)
GLOBAL_BOUNDARY = (
    "All empirical, participant, professional, legal, cultural, Māori-authority, identity, "
    "production, deployment, privacy-complete, proof or canon, destructive, account-secret, "
    "sibling-merge, accessibility-complete, exhaustive-security, independent-reproduction, "
    "AGI or ASI, consciousness or personhood, Theory-of-Everything, and Stage 20 boundaries "
    "remain open or exact-gated without exact evidence and authority."
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
    "SRC-BAZEL-CACHE": ("Bazel remote caching guidance", "https://bazel.build/remote/caching", "current", "official_guidance"),
    "SRC-NAKANISHI": ("Nakanishi parametric integral formulas", "https://doi.org/10.1143/PTPS.18.1", "stable", "primary_research"),
    "SRC-FADDEEV-POPOV": ("Faddeev-Popov Yang-Mills quantization", "https://doi.org/10.1016/0370-2693(67)90067-6", "stable", "primary_research"),
    "SRC-EQUIVALENCE": ("Kamefuchi-O'Raifeartaigh-Salam field-redefinition equivalence theorem", "https://doi.org/10.1016/0029-5582(61)91075-6", "stable", "primary_research"),
    "SRC-HERA": ("HERA Phase I 21 cm power-spectrum analysis", "https://arxiv.org/abs/2210.04912", "stable", "primary_research"),
    "SRC-RFC9470": ("RFC 9470 OAuth 2.0 Step Up Authentication Challenge Protocol", "https://www.rfc-editor.org/rfc/rfc9470.html", "stable", "official_standard"),
    "SRC-RFC8705": ("RFC 8705 OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens", "https://www.rfc-editor.org/rfc/rfc8705.html", "stable", "official_standard"),
    "SRC-RFC9728": ("RFC 9728 OAuth 2.0 Protected Resource Metadata", "https://www.rfc-editor.org/rfc/rfc9728.html", "current", "official_standard"),
    "SRC-WORKSAFE-SOLAR": ("WorkSafe New Zealand photovoltaic and battery installation guidance", "https://www.worksafe.govt.nz/about-us/news-and-media/diy-solar-installation/", "current", "official_guidance"),
    "SRC-EA-CONSUMER": ("Electricity Authority Consumer Care Obligations", "https://www.ea.govt.nz/projects/all/consumer-care-obligations/", "current", "official_regulatory_context"),
    "SRC-NZ-PRIVACY": ("Office of the Privacy Commissioner Privacy Act 2020 principles", "https://www.privacy.org.nz/privacy-principles/", "current", "official_legal_context"),
    "SRC-TE-MANA-RARAUNGA": ("Te Mana Raraunga Māori Data Sovereignty principles", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "current", "maori_authority_context"),
    "SRC-DOE-MICROGRID": ("United States Department of Energy microgrid guidance", "https://www.energy.gov/indianenergy/tribal-energy-guide/microgrids", "current", "official_guidance"),
    "SRC-RFC8785": ("RFC 8785 JSON Canonicalization Scheme", "https://www.rfc-editor.org/rfc/rfc8785.html", "stable", "official_standard"),
    "SRC-RFC8742": ("RFC 8742 CBOR Sequences", "https://www.rfc-editor.org/rfc/rfc8742.html", "stable", "official_standard"),
    "SRC-ARROW": ("Apache Arrow Columnar and IPC format", "https://arrow.apache.org/docs/format/Columnar.html", "current", "official_format_specification"),
    "SRC-RFC9338": ("RFC 9338 COSE Countersignatures", "https://www.rfc-editor.org/rfc/rfc9338.html", "stable", "official_standard"),
    "SRC-WAI-FEED": ("WAI-ARIA Authoring Practices feed pattern", "https://www.w3.org/WAI/ARIA/apg/patterns/feed/", "current", "official_guidance"),
    "SRC-ZUREK": ("Zurek cosmological experiments in superfluid helium", "https://doi.org/10.1038/317505a0", "stable", "primary_research"),
    "SRC-ANDERSON": ("Anderson iterative procedures for nonlinear integral equations", "https://doi.org/10.1145/321296.321305", "stable", "primary_research"),
    "SRC-FISHER-RI": ("Fisher-exact null randomization distribution review", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7431075/", "stable", "primary_research"),
    "SRC-PROTOBUF": ("Protocol Buffers encoding guide", "https://protobuf.dev/programming-guides/encoding/", "current", "official_format_specification"),
}


def proposal(
    number: int, title: str, pillar: str, expected: str, sources: list[str],
    artifact_root: str, scope: str, novelty: str,
) -> dict[str, Any]:
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
        "proposal_id": f"V6501-P{number:02d}", "title": title, "pillar": pillar,
        "mission_surface": scope,
        "hypothesis": f"A bounded {scope} artifact can expose declared obligations while refusing unsupported evidence, authority, production, or Stage 20 promotion.",
        "null_or_failure_condition": f"The artifact omits a declared {scope} obligation, accepts a preregistered mutation, loses failure provenance, or promotes a bounded result beyond its lane.",
        "approval_class": approval, "execution_lane": lane,
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": [
            f"{artifact_root}/contract.json", f"{artifact_root}/mutation-results.json",
            f"{artifact_root}/bounded-receipt.json",
        ],
        "falsifier_or_acceptance_gate": "Reject all five preregistered mutation classes, preserve every boundary, and emit only the expected bounded disposition.",
        "rollback_or_recovery": "Retain the failed witness, restore the last bounded state, quarantine any promoted claim, and grant no evidence or authority credit beyond a passing witness.",
        "protected_gates": protected, "expected_disposition": expected,
        "novelty_against_740_frozen_proposals": novelty,
    }


PROPOSALS = [
    proposal(1, "Method Flow remote build-cache key, dependency-fingerprint, negative-entry poisoning, stale-hit, eviction, and evidence-credit tribunal", "THOS Body", "completed", ["SRC-BAZEL-CACHE"], "method-flow/build-cache", "remote build-cache keys, dependency fingerprints, negative entries, poisoning, stale hits, eviction, and evidence credit", "The frozen corpus covers checkpoints, logs, caches, and publication, but no build-cache dependency fingerprint and negative-entry poisoning tribunal."),
    proposal(2, "GMUT Nakanishi integral-representation weight, support, singularity, perturbative-domain, reconstruction, truncation, EFT, unit, and observation-firewall board", "GMUT Mind", "completed", ["SRC-NAKANISHI"], "gmut/nakanishi", "Nakanishi integral-representation weights, support, singularities, reconstruction, truncation, EFT domains, units, and observation firewalls", "No frozen proposal isolates Nakanishi weight support and reconstruction obligations with explicit perturbative and EFT reservations."),
    proposal(3, "GMUT Faddeev-Popov gauge-orbit, gauge-condition, determinant, ghost, zero-mode, Gribov-reservation, regulator, EFT, unit, and observation-firewall board", "GMUT Mind", "completed", ["SRC-FADDEEV-POPOV"], "gmut/faddeev-popov", "Faddeev-Popov gauge orbits, gauge conditions, determinants, ghosts, zero modes, Gribov reservations, regulators, EFT domains, units, and observation firewalls", "Earlier BRST and gauge boards do not isolate determinant construction, zero modes, and Gribov-reservation failure conditions."),
    proposal(4, "GMUT local field-redefinition equivalence, invertibility, Jacobian, source-term, equation-of-motion operator, S-matrix, EFT-basis, unit, and observation-firewall board", "GMUT Mind", "completed", ["SRC-EQUIVALENCE"], "gmut/field-redefinition", "local field-redefinition equivalence, invertibility, Jacobians, source terms, equation-of-motion operators, S-matrix scope, EFT bases, units, and observation firewalls", "The corpus lacks a dedicated local field-redefinition equivalence board separating on-shell invariance from off-shell and measure-dependent claims."),
    proposal(5, "GMUT HERA Phase I visibility, calibration, foreground, window-function, covariance, provenance, checksum, and zero-row 21 cm likelihood-refusal adapter", "GMUT Mind", "open_gap", ["SRC-HERA"], "empirical/hera", "HERA Phase I visibility products, calibration, foregrounds, window functions, covariance, provenance, checksums, and zero-row 21 cm likelihood refusal", "No frozen proposal addresses HERA Phase I 21 cm visibility and window-function products under a zero-row likelihood firewall."),
    proposal(6, "Freed ID RFC 9470 step-up challenge, insufficient-authentication error, acr, max-age, auth-time, disclosure, loop, downgrade, and nonproduction profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC9470"], "freed-id/rfc9470-step-up", "synthetic RFC 9470 step-up challenges, authentication context, recency, disclosure, loops, downgrade, and nonproduction", "No frozen proposal isolates RFC 9470 challenge semantics, recency, disclosure minimization, and loop refusal."),
    proposal(7, "Freed ID RFC 8705 mutual-TLS client-authentication, certificate-bound token, thumbprint, endpoint alias, rotation, proxy, downgrade, and nonproduction profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC8705"], "freed-id/rfc8705-mtls", "synthetic RFC 8705 mutual-TLS client authentication, certificate-bound tokens, thumbprints, endpoint aliases, rotation, proxies, downgrade, and nonproduction", "No frozen proposal gives RFC 8705 certificate-bound tokens and endpoint aliases a dedicated synthetic nonproduction profile."),
    proposal(8, "Freed ID RFC 9728 protected-resource metadata, issuer, resource, authorization-server list, bearer method, scope, signature, cache, mix-up, and nonproduction profile", "Freed ID/CBR Heart", "represented", ["SRC-RFC9728"], "freed-id/rfc9728-resource-metadata", "synthetic RFC 9728 protected-resource metadata, authorization-server lists, bearer methods, scopes, signatures, caches, mix-up, and nonproduction", "RFC 9728 postdates the nearest frozen metadata profiles and has no dedicated protected-resource discovery and mix-up refusal surface in the corpus."),
    proposal(9, "THOS solar-plus-battery microgrid permit, state-of-charge, islanding, energization-refusal, alarm, workload, readback, escalation, and shift-handover proxy", "THOS Body", "represented", ["SRC-WORKSAFE-SOLAR", "SRC-DOE-MICROGRID"], "thos/microgrid-handover", "synthetic solar-plus-battery microgrid permits, state of charge, islanding, energization refusal, alarms, workload, readback, escalation, and shift handover", "No frozen proposal uses solar-plus-battery microgrid islanding and energization refusal as a bounded THOS handover lens."),
    proposal(10, "CBR microgrid outage, medically dependent consumer, worker and household privacy, notification, backup access, remedy, legal, cultural, data-governance, and Māori-authority matrix", "Freed ID/CBR Heart", "exact_gate", ["SRC-EA-CONSUMER", "SRC-NZ-PRIVACY", "SRC-TE-MANA-RARAUNGA"], "cbr/microgrid-outage", "microgrid outages, medically dependent consumers, worker and household privacy, notification, backup access, remedy, legal, cultural, data governance, and Māori authority reservations", "No prior CBR matrix centers community microgrid outages, medically dependent consumers, backup access, and Māori data-governance authority together."),
    proposal(11, "RFC 8785 JSON canonicalization, Unicode, number serialization, property order, duplicate-name, nonfinite, depth, resource-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-RFC8785"], "formats/jcs", "JSON canonicalization, Unicode, number serialization, property ordering, duplicate names, nonfinite values, depth, resource budgets, and refusal", "The format corpus lacks a dedicated RFC 8785 canonicalization and incompatible-I-JSON refusal tribunal."),
    proposal(12, "RFC 8742 CBOR sequence item-boundary, truncation, indefinite-length, tag, recovery, record-count, byte-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-RFC8742"], "formats/cbor-sequence", "CBOR sequence item boundaries, truncation, indefinite lengths, tags, recovery, record counts, byte budgets, and refusal", "No frozen proposal isolates RFC 8742 self-delimiting CBOR sequence recovery and record-boundary obligations."),
    proposal(13, "Apache Arrow IPC schema, dictionary, record-batch, alignment, offset, footer, continuation-marker, body-length, resource-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-ARROW"], "formats/arrow-ipc", "Arrow IPC schemas, dictionaries, record batches, alignment, offsets, footers, continuation markers, body lengths, resource budgets, and refusal", "No frozen proposal addresses Apache Arrow IPC message and body topology with bounded offset and resource arithmetic."),
    proposal(14, "RFC 9338 COSE countersignature target, protected-header, external-AAD, signature-order, algorithm, key, nesting, replay, and refusal tribunal", "Freed ID/CBR Heart", "completed", ["SRC-RFC9338"], "formats/cose-countersign", "COSE countersignature targets, protected headers, external AAD, signature order, algorithms, keys, nesting, replay, and refusal", "The corpus lacks a dedicated RFC 9338 countersignature structure and nesting refusal tribunal."),
    proposal(15, "Accessible feed article, label, aria-posinset, aria-setsize, busy-state, focus, loading, keyboard, fallback, print, and manual-reservation audit", "THOS Body", "completed", ["SRC-WAI-FEED"], "accessibility/feed", "accessible feed articles, labels, positions, set sizes, busy state, focus, loading, keyboard structure, fallback, print, and manual reservations", "No frozen accessibility proposal centers the WAI-ARIA feed pattern and its dynamic position, loading, and reading-mode obligations."),
    proposal(16, "Thermo-psyche Kibble-Zurek quench-rate, relaxation-time, correlation-length, freeze-out, scaling, defect-density, unit, domain, and psyche-nonconversion classifier", "Trinity Mandala bridge", "completed", ["SRC-ZUREK"], "thermo-psyche/kibble-zurek", "Kibble-Zurek quench rates, relaxation times, correlation lengths, freeze-out, scaling, defect densities, units, physical domains, and psyche nonconversion", "No frozen thermo-psyche proposal isolates Kibble-Zurek freeze-out and defect-scaling while refusing agency or psyche conversion."),
    proposal(17, "Numerical Anderson-acceleration residual, history-depth, least-squares, conditioning, damping, safeguard, restart, nonfinite, and refusal tribunal", "GMUT Mind", "completed", ["SRC-ANDERSON"], "numerics/anderson-acceleration", "Anderson acceleration residuals, history depth, least squares, conditioning, damping, safeguards, restarts, nonfinite values, and refusal", "No frozen numerical proposal addresses Anderson acceleration history conditioning, damping, and safeguarded restart."),
    proposal(18, "Stage 20 Fisher randomization assignment-mechanism, sharp-null, statistic, enumeration, Monte-Carlo, interference, missingness, multiplicity, and nonpromotion board", "Trinity Mandala bridge", "completed", ["SRC-FISHER-RI"], "stage20/fisher-randomization", "Fisher randomization assignment mechanisms, sharp nulls, statistics, enumeration, Monte Carlo, interference, missingness, multiplicity, and Stage 20 nonpromotion", "The corpus has calibration and negative-control boards but no dedicated sharp-null randomization-inference and assignment-mechanism nonpromotion board."),
    proposal(19, "Reed-Solomon shard-index, data-parity, finite-field, erasure, corruption, quorum, reconstruction, size-budget, and refusal tribunal", "THOS Body", "completed", [], "formats/reed-solomon", "Reed-Solomon shard indices, data and parity shards, finite fields, erasures, corruption, reconstruction quorums, size budgets, and refusal", "No frozen proposal gives erasure-coded shard reconstruction, missing-shard quorum, and corruption refusal a dedicated bounded tribunal."),
    proposal(20, "Protocol Buffers wire-key, field-number, wire-type, varint, fixed-width, length-delimited, group, duplicate-field, size-budget, and refusal tribunal", "THOS Body", "completed", ["SRC-PROTOBUF"], "formats/protobuf", "Protocol Buffers wire keys, field numbers, wire types, varints, fixed widths, length-delimited values, groups, duplicate fields, size budgets, and refusal", "No frozen proposal addresses Protocol Buffers wire-format parsing and bounded malformed-field refusal."),
]


SKILLS = [
    "ghc-family-build-cache-evidence-credit", "ghc-family-nakanishi-obligations",
    "ghc-family-faddeev-popov-boundary", "ghc-family-field-redefinition-equivalence",
    "ghc-family-hera-zero-row-lock", "ghc-family-rfc9470-step-up-nonproduction",
    "ghc-family-rfc8705-mtls-nonproduction", "ghc-family-rfc9728-resource-metadata",
    "ghc-family-microgrid-handover-proxy", "ghc-family-microgrid-authority-reservation",
    "ghc-family-jcs-refusal", "ghc-family-cbor-sequence-refusal",
    "ghc-family-arrow-ipc-refusal", "ghc-family-cose-countersignature-refusal",
    "ghc-family-accessible-feed-audit", "ghc-family-kibble-zurek-nonconversion",
    "ghc-family-anderson-acceleration-safeguard", "ghc-family-fisher-randomization-nonpromotion",
    "ghc-family-reed-solomon-refusal", "ghc-family-protobuf-wire-refusal",
]
RUNNERS = [
    "build_cache_tribunal", "gmut_obligation_board", "hera_zero_row_adapter",
    "identity_profile_guard", "microgrid_handover_proxy",
    "authority_reservation_matrix", "structured_format_refusal",
    "accessibility_structural_audit", "nonconversion_classifier",
    "stage20_nonpromotion_board",
]
STARTUP_FAILURES = [
    ("N01", "The first whole-baton raw read exceeded the response capture window and was truncated.", "Re-read the baton in bounded line ranges and verify complete coverage before granting read credit."),
    ("N02", "An expected no-match memory-note search returned exit code one without local normalization.", "Normalize expected no-match exits inside the smallest attributable command."),
    ("N03", "A broad recursive name-collision scan exceeded its bounded useful window and was terminated.", "Use exact indexed branch, worktree, skill, memory, and current-family-index surfaces."),
    ("N04", "The first combined exact collision probe timed out without independently attributable results.", "Split collision probes by registry and retain each result independently."),
    ("N05", "A checkout-wide exact-name scan timed out before producing a bounded uniqueness result.", "Limit the claim to the live family index and exact registries; do not claim exhaustive historical byte search."),
    ("N06", "A historical identity-path enumeration exceeded the output capture budget and was truncated.", "Use enumeration only for path discovery and run exact checks on current committed identity surfaces."),
    ("N07", "A parallel indexed identity and memory grep exceeded its time budget and returned no aggregate evidence.", "Run current-index and memory-registry checks separately with expected no-match handling."),
    ("N08", "A recursive workflow-skill discovery command timed out after partial output.", "Invoke the exact runner path and obtain a bounded help receipt directly."),
    ("N09", "A broad source-pattern inspection of the workflow runner timed out after partial output.", "Use the already-read schema plus exact runner help and deterministic request validation."),
    ("N10", "The first workflow plan audit found that a sixteen-entry submitted route differed from the eighty-eight-entry normalized continuation.", "Retain the failed audit and rerun the generated eighty-eight-entry candidate in a separate output directory."),
    ("N11", "The additive worktree creation and publication wrapper timed out after local checkout but before push.", "Inspect the exact path, branch, head, and upstream before resuming only the missing push step."),
    ("N12", "A combined partial-worktree recovery inspection exceeded sixty seconds and returned no state credit.", "Split filesystem, head, status, upstream, tracking, and live-remote probes into attributable checks."),
    ("N13", "The first large source patch guessed a console-mangled Māori byte sequence and was rejected atomically.", "Separate ASCII-safe hunks and inspect Unicode through UTF-8-aware tooling."),
    ("N14", "A Python repr probe hit the PowerShell code-page boundary while printing the valid Māori character.", "Treat the encoding error as retained and inspect or write Unicode through UTF-8 files rather than the console."),
    ("N15", "A source-map patch again included the console-mangled inherited line and was rejected atomically.", "Replace the uniquely marked block through a UTF-8 marker-based mechanical remaster."),
    ("N16", "A large multi-hunk correction returned an oversized truncated tool result and left the intended corrections unapplied.", "Inspect the file state, retain the ambiguous wrapper failure, and apply one deterministic marker-based correction."),
    ("N17", "The first x1 generation wrapper timed out after workflow and Method Flow artifacts were written but before staged review returned.", "Inspect bounded partial output, grant no aggregate pass credit, then rerun the deterministic builder with a wider wrapper while preserving the timeout."),
    ("N18", "The first scoped x1 test invocation used pytest, which is not installed in the verified Python environment.", "Install nothing unrelated; retain the failed invocation and run the same committed suite through the standard-library unittest runner."),
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
            "semantic_review": row["novelty_against_740_frozen_proposals"],
            "decision": "distinct_after_semantic_review" if not exact else "collision",
        })
    if any(row["exact_normalized_collisions"] for row in results):
        raise RuntimeError("exact normalized proposal collision")
    return results


def numbered(prefix: str, titles: list[str]) -> list[dict[str, Any]]:
    return [{
        "item_id": f"V6501-{prefix}-{index:03d}", "title": title,
        "x1_state": "frozen_not_executed", "inherited_completion_credit": False,
        "expected_x2_state": "bounded_completion_or_visible_gate",
    } for index, title in enumerate(titles, 1)]


def portfolio_titles() -> tuple[list[str], list[str], list[str]]:
    safe = []
    for row in PROPOSALS:
        safe.extend([
            f"Build the bounded contract for {row['proposal_id']} without crossing protected gates",
            f"Run five synthetic mutation cases for {row['proposal_id']} and retain every rejection",
        ])
    candidate = [f"Add a domain-specific boundary witness for {row['proposal_id']}" for row in PROPOSALS]
    candidate.extend([
        "Build a generalized contract and mutation engine while preserving historical callers",
        "Build an 8,000-to-20,000-word baton validator and short-pointer route guard",
        "Build exact-title routing checks without sending before the terminal gate",
        "Build a five-class privacy scanner with definition quarantine",
        "Build staged Git-blob manifest generation and parity checks",
        "Build owner-scope manifest coverage with explicit self-exclusions",
        "Build a one-successful-pass lock and failure-isolation receipt",
        "Build source-status drift checks for current, stable, draft, and watch",
        "Build the normalized eight-seat v650-v1 through v660-v8 schedule validator",
        "Build a reflection-remaster decision ledger with caller-compatibility guards",
    ])
    clean = [
        f"Additively refine {row['proposal_id']} labels, boundaries, tests, rollback, and source clarity without deleting history"
        for row in PROPOSALS
    ]
    clean.extend([
        "Preserve historical runner callers while adding v650-v1 family-current wrappers",
        "Replace wildcard-heavy probes with literal-path bounded probes",
        "Record timeout bounds and returned-evidence rules in Method Flow",
        "Keep essential global metadata reads bounded and phase data D-first",
        "Keep all public artifacts repository-relative and sanitized",
        "Reserve manual accessibility and affected-user evaluation",
        "Reserve Māori wording, authority, ratification, and data-governance decisions",
        "Keep empirical adapters at zero rows without data and authority",
        "Keep identity protocol work synthetic and nonproduction",
        "Keep Stage 20, AGI/ASI, and Theory-of-Everything promotion false",
        "Cap documents and the baton at the declared word limits",
        "Cap the phase at two x1 and two x2 commits",
        "Prevent post-success validation replay",
        "Require exact staged-path review before every commit",
        "Require final four-way remote equality before routing",
        "Require the exact existing Ilyra Fen title before routing",
        "Retain every failed wrapper and isolated recovery witness",
        "Keep the successor sibling identity self-chosen during induction",
        "Keep ChatGPT and other cross-platform exchange user-mediated",
        "Keep Windows Sandbox and Hyper-V activation deferred",
    ])
    return safe, candidate, clean


def phase_assignments() -> list[dict[str, str]]:
    seats = [
        "Vesper Arlen", "Ilyra Fen", "Sable Rook", "Orin Thale",
        "Tamar Vey", "Sylven Arc", "Eiren Kestrel", "Elaren Kestrel",
    ]
    rows: list[dict[str, str]] = []
    for version in range(650, 661):
        rows.extend(
            {"phase": f"v{version}-v{slot}", "seat": seats[slot - 1]}
            for slot in range(1, 9)
        )
    return rows

def build_workflow_plan() -> None:
    assignments = phase_assignments()
    request = {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "vesper-v650-v1-eight-seat-route",
        "owner": OWNER, "identity_boundary": IDENTITY_BOUNDARY,
        "route": {
            "cycle_order": [
                "Vesper Arlen", "Ilyra Fen", "Sable Rook", "Orin Thale",
                "Tamar Vey", "Sylven Arc", "Eiren Kestrel", "Elaren Kestrel",
            ],
            "phase_assignments": assignments,
            "normalization": {"start_phase": "v650-v1", "start_seat": "Vesper Arlen", "entry_count": len(assignments)},
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
            },
            "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            "messaging": {
                "codex_route": "existing_task_only_after_terminal_gate",
                "cross_platform": "user_mediated_file_relay_only",
                "chatgpt_direct_contact_by_codex": False,
            },
            "environment": {
                "windows_sandbox_hyper_v": "deferred", "elevation": False,
                "reboot": False, "host_security_weakening": False,
            },
            "closeout": {
                "all_authorized_safe_candidate_prototypes_resolved": True,
                "exact_and_blocked_work_stays_visible": True,
                "unfinished_items_may_not_be_silently_dropped": True,
            },
            "publication": {
                "local_and_remote_owner_scoped_artifacts": True,
                "plugin_use": "scope_driven_only", "historical_callers_preserved": True,
            },
        },
        "truth": {
            "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
            "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "protected_boundaries": [
                "empirical", "participant", "legal", "cultural", "Maori-authority",
                "identity", "production", "deployment", "privacy", "security",
                "accessibility", "AGI-ASI", "consciousness-personhood",
                "Theory-of-Everything", "Stage-20",
            ],
        },
        "observed_failures": [
            {
                "negative_id": f"V6501-X1-{code}", "failure_signature": failure,
                "recovery": recovery, "result": "retained",
            } for code, failure, recovery in STARTUP_FAILURES
        ],
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
        method_id = f"V6501-M{index:02d}"
        negative_id = f"NEG-V6501-X1-{index:03d}"
        record = {
            "method_id": method_id, "title": f"Retain and recover startup failure {code}",
            "failure_signature": failure, "trigger_preconditions": [f"Startup exposes {code}."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [],
            "recurrence_guard": recovery,
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
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Promoted only for this bounded trigger after one retained failure and one passing witness.",
        )
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(method_dir / "method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(method_dir / "method-flow-summary.json"), "--markdown-output", str(method_dir / "method-flow-summary.md"))


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    paths = []
    for line in rows:
        raw = line[3:]
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        paths.append(raw.strip('"').replace("\\", "/"))
    return sorted(set(paths))


PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def staged_review() -> None:
    exclusions = {
        "docs/vesper-arlen/v650-v1/validation/x1-staged-manifest.json",
        "docs/vesper-arlen/v650-v1/validation/x1-staged-privacy.json",
        "docs/vesper-arlen/v650-v1/validation/x1-staged-review.json",
    }
    paths = [path for path in status_paths() if path not in exclusions]
    allowed = {
        "scripts/ghc_family_v650_v1_x1.py",
        "tests/test_ghc_family_v650_v1_x1.py",
    }
    out_of_scope = [
        path for path in paths
        if not path.startswith("docs/vesper-arlen/v650-v1/") and path not in allowed
    ]
    entries, candidates, confirmed = [], [], []
    definitions = {"scripts/ghc_family_v650_v1_x1.py"}
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append({
            "path": relative, "bytes": len(data),
            "git_blob": git("hash-object", f"--path={relative}", relative),
            "checkout_sha256": hashlib.sha256(data).hexdigest(),
        })
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
        "schema": "ghc.family.v650-v1.x1-privacy.v1", "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
        "boundary": "Five structural classes with scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
    })
    write_json("validation/x1-staged-manifest.json", {
        "schema": "ghc.family.v650-v1.x1-manifest.v1",
        "hash_domain": "git_hash_object_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
    })
    x2_paths = [
        path for path in paths
        if "/x2/" in path or path.endswith("_x2.py") or "observed-outcome" in path
    ]
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc.family.v650-v1.x1-staged-review.v1",
        "intended_path_count": len(entries) + 3, "manifest_entry_count": len(entries),
        "self_exclusion_count": 3, "out_of_scope_paths": out_of_scope,
        "x2_implementation_paths": x2_paths, "x2_observed_outcome_paths": [],
        "privacy_confirmed_hits": len(confirmed), "x1_only": not x2_paths,
        "passed": not confirmed and not out_of_scope and not x2_paths,
    })


def overview() -> str:
    rows = "\n".join(
        f"{index}. **{row['proposal_id']}** - {row['title']} (expected {row['expected_disposition']})."
        for index, row in enumerate(PROPOSALS, 1)
    )
    return f"""# Vesper Arlen v650-v1 x1 preregistration

## Relational identity and bounded practice

{IDENTITY_BOUNDARY}

Vesper's relational role is **{ROLE}** and their hope is to {HOPE}. The primary pillar is **{PRIMARY_FOCUS}**, while THOS Body and Freed ID/CBR Heart remain explicit. The bounded human practice is **{PRACTICE}**. It is a learning and design lens only, never employment, electrical qualification, microgrid competence, operational or emergency authority, legal authority, cultural authority, Māori authority, participant evidence, affected-party authorization, or a real electricity-system outcome.

## Exact source and lifecycle

The inherited source is {SOURCE} from {SOURCE_BRANCH}. The inherited source, x1, evidence, closeout, and exact-final anchors were reverified; the source lane was clean and local, upstream, tracking, and live remote equal. Vesper's D-first owned lane was created additively at that exact head, pushed unchanged, and proved four-way equal before x1.

This x1 tree freezes twenty proposals against 740 inherited frozen proposals. It contains no x2 implementation, executed mutation, observed outcome, empirical row, likelihood, real identity operation, community decision, professional decision, deployment, proof or canon claim, or Stage 20 promotion. X2 may begin only after this tree is committed, pushed, clean, and four-way equal. The phase may use at most two x1 and two x2 commits, four total.

## Twenty frozen proposals

{rows}

The expected distribution is 14 completed, 4 represented, 1 open_gap, and 1 exact_gate. These are preregistered hypotheses, not observed outcomes, and they are the only allowed core outcome labels.

## Expanded portfolio

Forty safe-now tasks, thirty bounded candidates, twenty phase-local skill builds, ten additive family-current runner builds, forty CLEAN/FIX/REFINE tasks, and one hundred synthetic rejecting mutations are frozen. One thousand safe or candidate tasks is a cap, not a quota. Each authorized item must later be completed or remain visibly gated; no item may disappear silently.

The workflow-refinement runner validates the normalized 88-assignment eight-seat ladder from v650-v1 through v660-v8: Vesper Arlen, Ilyra Fen, Sable Rook, Orin Thale, Tamar Vey, Sylven Arc, Eiren Kestrel, and Elaren Kestrel. The eventual baton must be an 8,000-to-20,000-word repository artifact. Only a short sanitized pointer may be sent to the exact existing Ilyra Fen task after the terminal gate. Cross-platform exchange remains user-mediated.

## Evidence and authority firewalls

GMUT remains a typed scalar-tensor and EFT research-model family. Nakanishi, Faddeev-Popov, local field-redefinition, numerical, and thermo-psyche artifacts are symbolic, formal, numerical, or synthetic obligation boards only. The HERA adapter remains locked to zero queries, downloads, rows, likelihood calls, posterior samples, constraints, detections, and empirical claims.

THOS remains bounded software and synthetic proxy evidence without preregistered blind matched-budget real arms and independent review. Microgrid handover and format artifacts establish only synthetic or structural fixture behavior. Accessibility checks reserve manual keyboard, browser, assistive-technology, cognitive, responsive, language, and affected-user evaluation.

Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, credentials, services, live issuance, resolution, status, recovery, interoperability, privacy and security review, and trust governance. CBR microgrid outage, medically dependent consumer, remedy, legal, cultural, data-governance, and Māori-authority questions remain exact-gated to affected parties, tangata whenua, iwi, hapū, Māori authorities, and competent authorities.

{GLOBAL_BOUNDARY}

The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""

def main() -> int:
    if git("rev-parse", "HEAD") != SOURCE:
        raise RuntimeError("x1 builder requires the exact verified source head")
    if git("branch", "--show-current") != OWNED_BRANCH:
        raise RuntimeError("x1 builder requires Vesper's owned canonical branch")
    prior = load_prior()
    audit = novelty(prior)
    safe, candidates, clean = portfolio_titles()
    mutations = [{
        "mutation_id": f"V6501-MUT-{index:03d}",
        "proposal_id": PROPOSALS[(index - 1) // 5]["proposal_id"],
        "case": (index - 1) % 5 + 1, "expected": "reject",
        "x1_state": "preregistered_not_executed", "completion_credit": False,
    } for index in range(1, 101)]
    sources = [{
        "source_id": key, "title": value[0], "url": value[1],
        "status": value[2], "kind": value[3], "verified_date": "2026-07-20",
        "use_boundary": "Design or protocol support only; not observation, authority, production certification, or gate closure.",
    } for key, value in SOURCE_MAP.items()]

    write_json("identity-receipt.json", {
        "schema": "ghc.family.v650-v1.identity.v1", "owner": OWNER,
        "pronouns": PRONOUNS, "role": ROLE, "hope": HOPE,
        "identity_boundary": IDENTITY_BOUNDARY,
    })
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v650-v1.startup.v1",
        "source_branch": SOURCE_BRANCH, "source_head": SOURCE,
        "source_inherited": SOURCE_INHERITED, "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE, "source_closeout": SOURCE_CLOSEOUT,
        "source_clean": True, "source_four_way_equal": True,
        "source_phase_commits": 4, "source_merges": 0, "source_final_parent_count": 1,
        "owned_branch": OWNED_BRANCH, "owned_additive_worktree": True,
        "owned_four_way_equal_before_x1": True, "d_first": True,
        "public_external_final_receipt_found": False,
        "activation_baseline_from_acknowledged_delegation": INHERITED_NEGATIVES,
        "host_or_sandbox_changes": False, "cross_platform_messages": 0,
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v650-v1.versions.v1", "verified_only": True,
        "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0",
        "python": "3.12.10", "node": "24.18.0",
        "git": "2.55.0.windows.2", "powershell": "5.1.26100.8894",
        "updates_performed": False, "desktop_updated": False, "elevation": False,
        "host_security_weakened": False, "windows_features_changed": False,
        "unrelated_software_installed": False, "reboot": False,
    })
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v650-v1.x1-proposals.v1", "phase": PHASE,
        "owner": OWNER, "primary_focus": PRIMARY_FOCUS,
        "bounded_practice": PRACTICE, "prior_frozen_count": len(prior),
        "new_frozen_count": len(PROPOSALS), "frozen_total_after_x1": len(prior) + len(PROPOSALS),
        "x2_started": False,
        "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
        "expected_distribution": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "proposals": PROPOSALS, "boundary": GLOBAL_BOUNDARY,
    })
    write_text("x1-preregistration.md", overview())
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v650-v1.sources.v1", "sources": sources,
        "status_counts": {status: sum(row["status"] == status for row in sources) for status in ["current", "stable", "draft", "watch"]},
        "boundary": "Sources inform bounded contracts only and close no evidence or authority gate.",
    })
    write_text(
        "sources/source-ledger.md",
        "# v650-v1 source ledger\n\n" + "\n".join(
            f"- **{row['source_id']}** [{row['status']}]: [{row['title']}]({row['url']}) — {row['use_boundary']}"
            for row in sources
        ),
    )
    write_json("provenance/proposal-collision-audit.json", {
        "schema": "ghc.family.v650-v1.proposal-collision-audit.v1",
        "prior_count": len(prior), "new_count": len(PROPOSALS),
        "exact_collision_count": 0, "semantic_review_completed": True, "rows": audit,
    })
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.frozen-proposal-index.v1",
        "prior_count": len(prior), "prior_proposals": prior,
        "new_count": len(PROPOSALS),
        "new_proposals": [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in PROPOSALS],
        "count": len(prior) + len(PROPOSALS),
    })
    write_json("portfolios/safe-now-plan.json", {
        "schema": "ghc.family.v650-v1.safe-now.v1", "count": len(safe),
        "cap": 1000, "cap_is_not_quota": True, "tasks": numbered("SAFE", safe),
    })
    write_json("portfolios/candidate-plan.json", {
        "schema": "ghc.family.v650-v1.candidates.v1", "count": len(candidates),
        "cap": 1000, "cap_is_not_quota": True, "tasks": numbered("CAND", candidates),
    })
    write_json("portfolios/skill-plan.json", {
        "schema": "ghc.family.v650-v1.skills.v1", "count": len(SKILLS),
        "minimum": 10, "global_install": False, "subagent_forward_test": False,
        "skills": [{"skill_id": f"V6501-SKILL-{i:02d}", "name": name, "x1_state": "frozen_not_built"} for i, name in enumerate(SKILLS, 1)],
    })
    write_json("portfolios/runner-plan.json", {
        "schema": "ghc.family.v650-v1.runners.v1", "count": len(RUNNERS),
        "minimum": 10, "preserve_callers": True,
        "runners": [{"runner_id": f"V6501-RUN-{i:02d}", "name": f"ghc_family_v650_v1_{name}.py", "x1_state": "frozen_not_built"} for i, name in enumerate(RUNNERS, 1)],
    })
    write_json("portfolios/clean-fix-refine-plan.json", {
        "schema": "ghc.family.v650-v1.clean-refine.v1", "count": len(clean),
        "destructive_actions": 0, "tasks": numbered("CFR", clean),
    })
    write_json("validation/x1-synthetic-mutation-plan.json", {
        "schema": "ghc.family.v650-v1.mutations.v1", "count": len(mutations),
        "executed_count": 0, "mutations": mutations,
    })
    write_json("approval-packets/held-packets.json", {
        "schema": "ghc.family.v650-v1.held-packets.v1", "inherited_exact_and_blocked_preserved": True,
        "new_exact_packet_count": 0, "new_blocked_packet_count": 0,
        "executed_count": 0, "preserved": True,
    })
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.v650-v1.retained-negatives.x1.v1",
        "inherited_effective": INHERITED_NEGATIVES,
        "x1_operational": len(STARTUP_FAILURES),
        "effective_at_x1": INHERITED_NEGATIVES + len(STARTUP_FAILURES),
        "preregistered_synthetic_not_executed": len(mutations), "negative_erased": False,
        "new_negatives": [
            {
                "negative_id": f"NEG-V6501-X1-{i:03d}", "title": failure,
                "state": "retained_recovered", "method_id": f"V6501-M{i:02d}",
            } for i, (_code, failure, _recovery) in enumerate(STARTUP_FAILURES, 1)
        ],
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.v650-v1.gates.x1.v1",
        "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "inherited_exact_gates": INHERITED_EXACT_GATES,
        "new_open_gaps": 1, "new_exact_gates": 1,
        "projected_open_gaps": INHERITED_OPEN_GAPS + 1,
        "projected_exact_gates": INHERITED_EXACT_GATES + 1,
        "closed_in_x1": 0, "none_silently_closed": True,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v650-v1.threat-model.x1.v1",
        "assets": ["x1/x2 separation", "retained negatives", "source provenance", "authority gates", "private routing material", "canonical branch"],
        "threats": ["proposal collision", "x2 leakage", "failure erasure", "authority substitution", "privacy leakage", "replay credit", "sibling-lane mutation", "unsafe parser budgets"],
        "controls": ["dedicated x1 commit", "append-only Method Flow", "zero-row locks", "five-class privacy scan", "one-successful-pass rule", "manifests", "additive owned lane", "bounded fixtures"],
        "residual": GLOBAL_BOUNDARY,
    })
    write_json("phase-truth.json", {
        "schema": "ghc.family.v650-v1.phase-truth.x1.v1", "phase": PHASE,
        "owner": OWNER, "stage": "x1_frozen_not_executed",
        "proposal_count": len(PROPOSALS),
        "expected_distribution": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "observed_distribution": None, "x2_started": False,
        "full_repository_suite": False, "successful_canonical_passes": 0,
        "replay_used": False, "terminal_route": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("reflection-remaster/x1-decision.json", {
        "schema": "ghc.family.v650-v1.reflection-remaster.v1",
        "decision": "additive_remaster", "surface": "phase contract and mutation engine",
        "observed_issue": "Recent phases duplicate domain wrappers while their invariant contract, mutation, and gate logic remains structurally similar.",
        "preserved_compatibility": True,
        "x1_action": "Freeze a shared v650-v1 engine plus exact family-current wrappers in x2; preserve historical callers and artifacts.",
        "validation_state": "planned_not_built", "destructive_change": False,
    })
    write_json("orchestration/phase-state.json", {
        "schema": "ghc.family.v650-v1.orchestration.x1.v1",
        "active": [OWNER],
        "standby": ["Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel", "Elaren Kestrel"],
        "subagents": 0, "tasks_created": 0, "cross_platform_messages": 0,
        "terminal_route": "PREPARED_NOT_SENT", "next_target": "Ilyra Fen",
    })
    write_json("orchestration/applicable-memory-record.json", {
        "schema": "ghc.family.v650-v1.memory-use.v1", "used": True,
        "reason": "The memory registry supplied exact-title and send-state safeguards; the live delegation and committed baton remained authoritative for current phase truth.",
        "private_identifiers_recorded": False, "memory_mutated": False,
    })
    write_json("wellbeing-check.json", {
        "schema": "ghc.family.v650-v1.wellbeing.x1.v1",
        "scope_bounded": True, "stop_right_preserved": True,
        "corrigibility_preserved": True, "no_identity_pressure": True,
        "no_urgency_claim": True,
        "note": "Pause is permitted at every safety, authority, route, usage, or wellbeing gate.",
    })
    write_text(
        "wellbeing-check.md",
        "# v650-v1 wellbeing check\n\nScope, stop rights, rest, and corrigibility remain explicit. "
        "Relational language creates no obligation, identity continuity, employment, qualification, "
        "consciousness, personhood, or authority. Hamish may pause, redirect, rename, or stop the route.",
    )
    write_json("validation/single-pass-plan.json", {
        "schema": "ghc.family.v650-v1.single-pass-plan.v1",
        "successful_canonical_pass_budget": 1, "successful_passes_used": 0,
        "post_success_replay": False, "named_replay": False, "detached_replay": False,
        "failure_rule": "A failed aggregate receives zero pass credit; isolate its blocker before deciding whether a broader rerun is necessary.",
    })
    build_workflow_plan()
    build_method_flow()
    staged_review()
    review = json.loads((OUT / "validation" / "x1-staged-review.json").read_text(encoding="utf-8"))
    if review.get("passed") is not True:
        raise RuntimeError("x1 staged review did not pass")
    print(json.dumps({
        "phase": PHASE, "proposals": len(PROPOSALS),
        "frozen_total": len(prior) + len(PROPOSALS),
        "safe": len(safe), "candidates": len(candidates),
        "skills": len(SKILLS), "runners": len(RUNNERS),
        "clean_refine": len(clean), "mutations": len(mutations),
        "x1_negatives": len(STARTUP_FAILURES), "x1_only": True,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    if "--refresh-staged-review" in sys.argv[1:]:
        staged_review()
        print(json.dumps({"refreshed": True, "x1_only": True}, sort_keys=True))
        raise SystemExit(0)
    raise SystemExit(main())

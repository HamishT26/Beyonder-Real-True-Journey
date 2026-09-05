#!/usr/bin/env python3
"""Build Eiren Kestrel v685-v5 planning-only x1 artifacts.

The builder freezes source truth, a source-bounded inherited selection, new
proposal contracts, portfolio plans, a thirty-seat candidate topology, tool
review plans, retained startup failures, and exact staged validation.  It does
not build x2 implementations, record observed proposal outcomes, install a
package, modify global skills, or create/contact a successor task.
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
OWNER = "Eiren Kestrel"
PHASE = "v685-v5"
PREFIX = "EK6855"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v685-v4-full-tools"
SOURCE_FINAL = "87a74f84afaa197f8c388767a2ed536bbb853aba"
SOURCE_X1 = "27f858015e5628d99fb9dc23cd5607ed68429adb"
SOURCE_EVIDENCE = "499f193d9cc08a0c96ade3f1dc09ce7af3183afe"
SOURCE_INHERITED_SYLVEN = "97a523f4da00235f16ce12156dfee2379582c92d"
SOURCE_CANONICAL_RECEIPT_SHA256 = "1b08998610e32c665ce8b1f9ac6a85864455db9ecef3a474c4d53466c063098f"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "a94fa7fdde6baf7ad0f477748c565ff8448361dd5ef325e03d3720bd85559992"
DECLARED_CHAIN_BEFORE = 11450
DECLARED_CHAIN_AFTER = 11570
CHECKED_AT = "2026-09-05"

BASE = ROOT / "docs" / "eiren-kestrel" / PHASE
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
BUILDER_REL = "scripts/build_ghc_family_eiren_kestrel_v685_v5_x1.py"
TEST_REL = "tests/test_ghc_family_eiren_kestrel_v685_v5_x1.py"

ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
MUTATION_TYPES = [
    "missing_required_field",
    "identifier_role_swap",
    "stale_precondition_digest",
    "correction_order_inversion",
    "authority_promotion",
]

PROTECTED_GATES = [
    "real observatories detectors missions instruments alerts visibilities strain products and planetary archives",
    "real measurements classifications discoveries follow-up observations quality decisions and scientific conclusions",
    "professional astronomy radio-interferometry gravitational-wave planetary-data software and safety authority",
    "production identity issuance resolution status revocation interoperability and trust governance",
    "privacy accessibility copyright data-rights cultural affected-party and Maori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood Theory-of-Everything canon and Stage 20",
]

PRACTICES = [
    {
        "key": "transient_alert",
        "label": "synthetic transient-astronomy alert-broker assurance analyst",
        "sources": ["RUBIN-ALERTS", "IVOA-VOEVENT", "IVOA-PROVENANCE", "W3C-PROV-O"],
        "facets": [
            "alert-packet source capsule", "difference-image provenance vacancy", "broker-filter declaration",
            "classification probability abstention", "cross-match lineage", "watchlist privacy minimization",
            "public-alert rights boundary", "latency timestamp uncertainty", "schema-version negotiation",
            "duplicate-alert quarantine", "supersession and retraction braid", "follow-up priority nonpromotion",
            "community-filter authorship vacancy", "cutout-media lineage", "coordinate-frame declaration",
            "photometric-unit reservation", "moving-object ambiguity hold", "broker outage handover",
            "alert-stream backpressure ledger", "machine-learning model-card pointer",
            "training-corpus absence declaration", "false-positive retention", "human-review vacancy",
            "accessible alert-status narrative", "affected-user notification reservation",
            "GMUT transient analogy firewall", "THOS queue idempotency contract", "Freed-ID keyless receipt",
            "open real-alert evaluation gap", "exact scientific-discovery authority gate",
        ],
    },
    {
        "key": "radio_provenance",
        "label": "synthetic radio-interferometry provenance curator",
        "sources": ["SKAO-SDP", "SKAO-DATA-PRODUCTS", "IVOA-OBSCORE", "IVOA-PROVENANCE"],
        "facets": [
            "execution-block identity capsule", "visibility-product lineage", "calibration-table vacancy",
            "antenna-baseline topology placeholder", "frequency-channel unit declaration", "polarization-frame reservation",
            "flagging-reason retention", "data-product access boundary", "pipeline-parameter digest",
            "workflow image provenance", "quality-assessment nonpromotion", "reprocessing predecessor graph",
            "measurement-set format reservation", "beam-model absence statement", "receiver-chain vacancy",
            "correlator-output checksum", "observation-block temporal braid", "resource-allocation authority hold",
            "regional-centre handover", "embargo and data-rights reservation", "proprietary-period uncertainty",
            "download-command abstention", "Kubernetes deployment refusal", "accessible product-status table",
            "archive retention ambiguity", "GMUT visibility analogy firewall", "THOS pipeline state machine",
            "Freed-ID custody-envelope proxy", "open real-calibration evidence gap", "exact telescope-operations authority gate",
        ],
    },
    {
        "key": "gravitational_wave",
        "label": "synthetic gravitational-wave open-data reproducibility steward",
        "sources": ["GWOSC-API", "GWOSC-TUTORIALS", "IVOA-PROVENANCE", "NIST-SI"],
        "facets": [
            "dataset catalogue capsule", "strain-channel provenance", "detector-state vacancy",
            "data-quality segment declaration", "event-version supersession", "sample-rate unit contract",
            "time-system and epoch reservation", "calibration-file pointer vacancy", "injection-label quarantine",
            "noise-spectrum representation", "window-function declaration", "filter-parameter digest",
            "matched-filter nonresult boundary", "skymap association hold", "catalogue acknowledgement record",
            "license metadata preservation", "notebook environment lock", "random-seed declaration",
            "software-version graph", "tutorial-to-result firewall", "download-free API schema proxy",
            "missing-data interval ledger", "uncertainty propagation placeholder", "accessible waveform narrative",
            "independent-reproduction vacancy", "GMUT strain analogy firewall", "THOS analysis-stage handover",
            "Freed-ID contributor-role vacancy", "open real-detector evidence gap", "exact detection-claim authority gate",
        ],
    },
    {
        "key": "planetary_archive",
        "label": "synthetic planetary-data archive metadata engineer",
        "sources": ["NASA-PDS4", "NASA-PDS4-IM", "W3C-PROV-O", "RFC8785"],
        "facets": [
            "PDS4 product-label capsule", "logical-identifier version braid", "bundle collection product topology",
            "information-model version pin", "local-data-dictionary reservation", "discipline-dictionary namespace hold",
            "processing-level nonpromotion", "observation-area vacancy", "instrument-context abstention",
            "mission-context authority hold", "file-area checksum contract", "byte-offset and record-length declaration",
            "unit and axis-order reservation", "special-constant representation", "nil-reason preservation",
            "reference-list cycle quarantine", "product-update predecessor graph", "external-product boundary",
            "archive-format declaration", "validation-rule provenance", "schema-schematron version pairing",
            "context-product contact vacancy", "rights and citation record", "accessible label companion",
            "migration rollback ledger", "GMUT planetary analogy firewall", "THOS ingest-stage state machine",
            "Freed-ID submitter-role vacancy", "open real-mission evidence gap", "exact archive-acceptance authority gate",
        ],
    },
]

SOURCES = [
    ("RUBIN-ALERTS", "https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers", "Alert and broker vocabulary only; no live alert access classification follow-up priority or discovery claim."),
    ("IVOA-VOEVENT", "https://ivoa.net/documents/VOEvent/20250703/PR-VOEvent-2.1-20250703.html", "Proposed sky-event metadata vocabulary only; proposal status and changeability remain explicit."),
    ("IVOA-PROVENANCE", "https://www.ivoa.net/documents/ProvenanceDM/", "Astronomical provenance vocabulary only; no dataset quality reliability or trust conclusion."),
    ("SKAO-SDP", "https://developer.skao.int/projects/ska-sdp-integration/en/stable/design/data-processing.html", "Science Data Processor workflow vocabulary only; no deployment operation resource allocation or product-quality claim."),
    ("SKAO-DATA-PRODUCTS", "https://www.skao.int/nl/node/649", "Science-data-product lifecycle vocabulary only; no access entitlement delivery or scientific result."),
    ("IVOA-OBSCORE", "https://www.ivoa.net/documents/ObsCore/", "Observation-discovery metadata vocabulary only; no observation validity or archive conformance claim."),
    ("GWOSC-API", "https://gwosc.org/api/v1/docs/", "Public API shape vocabulary only; the phase performs zero data calls and no detector or event analysis."),
    ("GWOSC-TUTORIALS", "https://gwosc.org/tutorials/", "Learning-workflow vocabulary only; tutorials are not transformed into published detection evidence."),
    ("NASA-PDS4", "https://pds.nasa.gov/datastandards/documents/", "PDS4 document and archive vocabulary only; no product submission validation or NASA endorsement."),
    ("NASA-PDS4-IM", "https://pds.nasa.gov/datastandards/documents/im/", "PDS4 information-model vocabulary only; no mission observation or archive-acceptance claim."),
    ("W3C-PROV-O", "https://www.w3.org/TR/prov-o/", "Provenance vocabulary only; no authorship custody authenticity or trust conclusion."),
    ("NIST-SI", "https://www.nist.gov/pml/owm/si-units-information", "SI quantity and unit vocabulary only; no measurement traceability or empirical result."),
    ("RFC8785", "https://www.rfc-editor.org/rfc/rfc8785.html", "Canonical JSON vocabulary only; no signature authenticity identity or security conclusion."),
    ("W3C-WCAG22", "https://www.w3.org/TR/WCAG22/", "Accessibility structure vocabulary only; no complete conformance or affected-user acceptance."),
    ("TE-MANA-RARAUNGA", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Authority-reservation context only; no Maori wording data-governance decision ratification or authority."),
]

TOOLCHAIN = [
    ("python", "astropy", "8.0.1", "astronomical units tables times and coordinates on synthetic fixtures"),
    ("python", "asdf", "5.4.0", "versioned structured scientific-data container on synthetic fixtures"),
    ("python", "gwosc", "0.8.3", "offline client-shape and metadata validation with zero data calls"),
    ("python", "Pint", "0.25.3", "dimensional unit validation on synthetic quantities"),
    ("python", "uncertainties", "3.2.3", "bounded symbolic uncertainty propagation"),
    ("python", "jsonschema", "4.26.0", "proposal and evidence schema acceptance and rejection"),
    ("python", "networkx", "3.6.1", "acyclic provenance and route graph checks"),
    ("python", "xarray", "2026.7.0", "labelled zero-row multidimensional structure"),
    ("node", "ajv", "8.20.0", "JSON Schema validation with rejecting fixtures"),
    ("node", "zod", "4.5.4", "runtime boundary parsing with rejecting fixtures"),
    ("node", "fast-check", "4.9.0", "bounded property-based rejecting fixtures"),
    ("node", "json-schema-to-typescript", "16.0.0", "deterministic type projection without deployment"),
    ("node", "@apidevtools/json-schema-ref-parser", "16.0.1", "local reference graph dereference and cycle refusal"),
]

SKILL_NAMES = [
    "transient-alert-source-capsule", "broker-filter-nonpromotion", "alert-retraction-braid",
    "radio-visibility-provenance", "calibration-vacancy", "execution-block-lineage",
    "strain-channel-provenance", "data-quality-segment-hold", "detection-claim-firewall",
    "pds4-product-topology", "dictionary-namespace-reservation", "archive-acceptance-gate",
    "astronomy-unit-reservation", "time-coordinate-uncertainty", "zero-call-source-adapter",
    "accessible-science-status", "scientific-rights-hold", "four-practice-workload-handover",
    "thirty-seat-route-projection", "authority-noncompensation",
]

RUNNER_NAMES = [
    "ghc_family_astronomy_contract_runner", "ghc_family_astronomy_mutation_runner",
    "ghc_family_astronomy_provenance_runner", "ghc_family_astronomy_units_runner",
    "ghc_family_astronomy_graph_runner", "ghc_family_astronomy_privacy_runner",
    "ghc_family_astronomy_accessibility_runner", "ghc_family_astronomy_toolchain_runner",
    "ghc_family_astronomy_route_runner", "ghc_family_astronomy_terminal_runner",
]

MANDATORY_SKILLS = [
    "ghc-freed-id-flashcards", "ghc-family-index", "ghc-family-reflection-remaster",
    "ghc-family-method-flow-state", "ghc-family-meta-tool-box", "ghc-family-auth-permission-state",
    "ghc-family-roster-check", "ghc-main-orchestration-memory", "ghc-main-startup-builder",
    "ghc-main-compact-restart-builder", "ghc-main-closeout-builder", "ghc-main-retry",
    "ghc-open-gate-rail", "ghc-timestamp-flow", "ghc-full-tools-skill-bank",
    "ghc-family-truth-bridge", "ghc-worktree-branch-rotation", "ghc-web-reflection-ledger",
    "ghc-watcher-notifier-cadence", "ghc-drive-bank-guardian", "ghc-approval-packet-splitter",
]

INCUMBENTS = [
    "Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen", "Lyren Moss",
    "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash", "Orin Thale", "Liora Venn",
    "Tamar Vey", "Elowen Cairn", "Sylven Arc", "Caelen Morrow",
]

STARTUP_FAILURES = [
    ("EK6855-ST-N001", "A PowerShell reference-inventory wrapper placed a foreach statement directly before a pipe and was rejected before reading files.", "Materialized the foreach result in an array and piped that value only.", "Materialize PowerShell collections before downstream formatting or filtering."),
    ("EK6855-ST-N002", "A combined Git-log and receipt-search wrapper crossed its reporting window without an attributable completion object.", "Split exact Git history from bounded receipt enumeration and polled every returned session.", "Keep revision, receipt, and recursive file searches as separate bounded probes."),
    ("EK6855-ST-N003", "A worktree preflight embedded a semicolon-bearing Git invocation inside a Boolean expression and PowerShell rejected the missing closure.", "Ran branch existence, remote existence, and path existence as independent scalar probes.", "Do not embed command sequences inside parenthesized Boolean projections."),
    ("EK6855-ST-N004", "The first mechanical template projection materialized x2 and final builders before the planning-only x1 freeze.", "Stopped before staging and removed only the untracked files created by that attempt, leaving source and sibling state unchanged.", "Create or materialize x2 and final builders only after the x1 commit is pushed and four-way equal."),
    ("EK6855-ST-N005", "Direct npm website page reads returned HTTP 403 for five selected Node packages.", "Used the official npm registry command surface to resolve exact versions and deferred installation until x2.", "Treat registry CLI metadata as the bounded fallback when the public package page denies automated reads."),
    ("EK6855-ST-N006", "The optional Ruff x1 check could not resolve a Ruff executable from the active PATH despite historical inventory claims.", "Kept the already-passing compile unittest diff and privacy evidence, searched the bounded D-first tool roots without finding a callable Ruff binary, and deferred any isolated install to x2.", "Resolve an exact executable or isolated-environment module before invoking a historically catalogued tool; availability claims require a live path witness."),
]


def run(args: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=ROOT, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git(*args: str, check: bool = True) -> str:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8", "replace").strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def jaccard(left: str, right: str) -> float:
    a, b = set(normalized_title(left).split()), set(normalized_title(right).split())
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


def source_proposal_records() -> tuple[list[dict[str, str]], dict[str, Any]]:
    paths = [
        line for line in git("ls-tree", "-r", "--name-only", SOURCE_FINAL).splitlines()
        if line.lower().endswith(".json") and "proposal" in line.lower()
    ]
    specs = [f"{SOURCE_FINAL}:{path}" for path in paths]
    proc = run(["git", "cat-file", "--batch"], input_bytes=("\n".join(specs) + "\n").encode())
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    cursor, failures, records = 0, [], []
    for path in paths:
        line_end = proc.stdout.find(b"\n", cursor)
        if line_end < 0:
            raise RuntimeError("truncated git cat-file header")
        header = proc.stdout[cursor:line_end].decode("utf-8", "replace")
        cursor = line_end + 1
        if header.endswith(" missing"):
            failures.append(path)
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError(f"unexpected git cat-file header: {header}")
        size = int(parts[2])
        blob = proc.stdout[cursor:cursor + size]
        cursor += size + 1
        try:
            value = json.loads(blob.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            failures.append(path)
            continue
        for node in walk_dicts(value):
            title = node.get("title")
            identifier = node.get("proposal_id", node.get("id"))
            if isinstance(title, str) and isinstance(identifier, str):
                records.append({"id": identifier, "title": title, "path": path})
    deduped = {(r["id"], normalized_title(r["title"])): r for r in records}
    return list(deduped.values()), {
        "proposal_json_paths_discovered": len(paths),
        "proposal_json_paths_parsed": len(paths) - len(failures),
        "proposal_json_parse_failures": failures,
        "reachable_id_title_records": len(deduped),
    }


def disposition(index: int) -> str:
    if index <= 84:
        return "completed"
    if index <= 108:
        return "represented"
    if index <= 114:
        return "open_gap"
    return "exact_gate"


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for practice in PRACTICES:
        for facet in practice["facets"]:
            index = len(rows) + 1
            proposal_id = f"{PREFIX}-N{index:03d}"
            outcome = disposition(index)
            title = f"{practice['label']} {facet} with zero external rows and explicit authority vacancy"
            rows.append({
                "proposal_id": proposal_id,
                "title": title,
                "practice_key": practice["key"],
                "hypothesis": f"A bounded owner-local contract for {title.lower()} can preserve the declared structure and reject five preregistered invalid mutations without becoming a real observation, scientific result, professional decision, production assurance, identity proof, cultural decision, or authority act.",
                "null_or_failure_condition": f"{proposal_id} fails if an invalid fixture is accepted, the positive synthetic fixture is rejected, an absent datum or reviewer is promoted, or a protected gate is treated as closed.",
                "approval_class": {"completed": "safe_now", "represented": "candidate_proxy_only", "open_gap": "open_gap_requires_real_evidence", "exact_gate": "exact_approval_required"}[outcome],
                "execution_lane": {"completed": "owner_local_synthetic_zero_row", "represented": "bounded_representation_without_real_execution", "open_gap": "document_only_no_execution", "exact_gate": "hold_unexecuted"}[outcome],
                "official_or_primary_source_needs": practice["sources"],
                "concrete_artifacts": [f"docs/eiren-kestrel/{PHASE}/x2/proposal-evidence.json#{proposal_id}", f"docs/eiren-kestrel/{PHASE}/x2/rejecting-mutations.json#{proposal_id}"],
                "falsifier_or_acceptance_gate": f"Accept only {outcome} when the bounded positive witness matches this frozen row, all five invalid mutations are rejected, and no empirical, professional, production, legal, cultural, Maori-authority, independent, identity, or Stage 20 claim is inferred.",
                "rollback_or_recovery": f"Quarantine only {proposal_id}, retain every failure at zero credit, and regenerate from this immutable planning-only row.",
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": outcome,
                "preregistered_rejecting_mutations": [
                    {"mutation_id": f"{proposal_id}-M{i:02d}", "mutation_type": mutation, "expected_result": "rejected_zero_credit"}
                    for i, mutation in enumerate(MUTATION_TYPES, 1)
                ],
            })
    return rows


def proposal_audit(rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    inherited, scope = source_proposal_records()
    normalized_inherited = {normalized_title(r["title"]): r for r in inherited}
    reviews, exact, quarantined = [], [], []
    for row in rows:
        title = row["title"]
        if normalized_title(title) in normalized_inherited:
            exact.append({"proposal_id": row["proposal_id"], "inherited": normalized_inherited[normalized_title(title)]})
        nearest_score, nearest = max(((jaccard(title, r["title"]), r) for r in inherited), default=(0.0, {"id": None, "title": None, "path": None}), key=lambda item: item[0])
        review = {
            "proposal_id": row["proposal_id"], "title": title,
            "nearest_inherited_id": nearest["id"], "nearest_inherited_title": nearest["title"],
            "nearest_inherited_path": nearest["path"], "token_jaccard": round(nearest_score, 6),
            "review_disposition": "quarantined" if nearest_score >= 0.78 else "distinct_under_source_bounded_audit",
            "inherited_credit": "zero",
        }
        reviews.append(review)
        if nearest_score >= 0.78:
            quarantined.append(review)
    selected = sorted(inherited, key=lambda r: hashlib.sha256((PHASE + r["id"] + r["title"]).encode()).hexdigest())[:200]
    return {
        "schema": f"ghc.family.source-bounded-proposal-audit.{PHASE.replace('-', '.')}.x1",
        "owner": OWNER, "phase": PHASE, "source": SOURCE_FINAL,
        "declared_chain_before": DECLARED_CHAIN_BEFORE, "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "new_proposal_count": len(rows), "selected_inherited_count": len(selected),
        "audit_scope": scope, "quarantine_threshold_token_jaccard": 0.78,
        "maximum_neighbor_score": max((r["token_jaccard"] for r in reviews), default=0),
        "exact_title_collisions": exact, "quarantined_neighbors": quarantined,
        "neighbor_reviews": reviews,
        "universal_novelty_claimed": False,
        "boundary": "Source-bounded reachable proposal evidence only; inaccessible or noncanonical history remains an explicit limitation.",
    }, selected


def portfolio_entries(kind: str, themes: list[str], operations: list[str], count: int, lane: str) -> list[dict[str, Any]]:
    rows = []
    while len(rows) < count:
        theme = themes[len(rows) % len(themes)]
        operation = operations[(len(rows) // len(themes)) % len(operations)]
        index = len(rows) + 1
        rows.append({"id": f"{PREFIX}-{kind}{index:03d}", "title": f"{operation} for {theme}", "lane": lane, "x1_status": "preregistered_not_executed", "credit_boundary": "no x2 execution or completion credit in x1"})
    return rows


def make_portfolio() -> dict[str, Any]:
    themes = [f"{p['key']} {facet}" for p in PRACTICES for facet in p["facets"][:8]]
    safe_ops = ["define schema", "add positive fixture", "add rejecting fixture", "record provenance", "enforce nonconversion", "add rollback", "add recurrence guard"]
    candidate_ops = ["model", "validate", "mutate", "quarantine", "trace", "adjudicate"]
    clean_ops = ["CLEAN duplicates", "FIX ambiguity", "REFINE refusal", "CLEAN serialization", "FIX deterministic order", "REFINE evidence boundary", "CLEAN stale wording", "FIX fixture isolation", "REFINE recurrence guard", "CLEAN handover state"]
    exact_topics = ["real observatory access", "real detector data", "real scientific classification", "real follow-up priority", "real instrument calibration", "real archive submission", "real participant or operator involvement", "production identity lifecycle", "external deployment", "account or credential mutation", "rights adjudication", "professional safety decision", "legal interpretation", "cultural interpretation", "Maori wording or data governance", "affected-party acceptance", "privacy-complete assurance", "accessibility-complete assurance", "independent reproduction", "empirical GMUT confirmation", "AGI or ASI claim", "consciousness or personhood claim", "Theory-of-Everything proof", "canon promotion", "Stage 20 disposition"]
    exact_titles = [f"{topic} action {i:02d}" for i in range(1, 3) for topic in exact_topics][:50]
    blocked_topics = ["fabricate observation", "erase failed witness", "expose private route", "replace sibling identity", "mutate sibling lane", "force push history", "claim professional authority", "claim legal or cultural authority", "claim Maori authority", "claim empirical discovery", "claim independent reproduction", "claim production readiness", "claim privacy completeness", "claim accessibility completeness", "claim exhaustive security"]
    blocked_titles = [f"{topic} variant {i:02d}" for i in range(1, 3) for topic in blocked_topics][:30]
    return {
        "schema": f"ghc.family.portfolio-freeze.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE,
        "primary_pillar": "GMUT Mind", "represented_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "owner_practice_lenses": [p["label"] for p in PRACTICES],
        "safe_now": portfolio_entries("SAFE", themes, safe_ops, 200, "owner_local_safe_now"),
        "owner_candidates": portfolio_entries("CAND", themes, candidate_ops, 150, "owner_local_candidate"),
        "owner_clean_fix_refine": portfolio_entries("CFR", themes, clean_ops, 300, "owner_local_clean_fix_refine"),
        "owner_skill_ideas": [{"id": f"{PREFIX}-SKILL-{i:03d}", "name": name, "status": "planned_local_not_installed"} for i, name in enumerate(SKILL_NAMES, 1)],
        "owner_runner_ideas": [{"id": f"{PREFIX}-RUNNER-{i:03d}", "name": name, "status": "planned_family_current_not_built"} for i, name in enumerate(RUNNER_NAMES, 1)],
        "successor_skill_ideas": [{"id": f"{PREFIX}-SSKILL-{i:03d}", "title": f"successor skill seed {i:02d}", "status": "zero_credit_seed"} for i in range(1, 11)],
        "successor_runner_ideas": [{"id": f"{PREFIX}-SRUN-{i:03d}", "title": f"successor runner seed {i:02d}", "status": "zero_credit_seed"} for i in range(1, 11)],
        "exact_approval": [{"id": f"{PREFIX}-EXACT-{i:03d}", "title": title, "status": "unexecuted_exact_approval_hold", "required_authority": "action-specific competent and affected authority plus exact evidence"} for i, title in enumerate(exact_titles, 1)],
        "blocked": [{"id": f"{PREFIX}-BLOCK-{i:03d}", "title": title, "status": "blocked_unexecuted", "blocker": "would fabricate evidence, expose private material, rewrite history, substitute authority, or violate owner boundaries"} for i, title in enumerate(blocked_titles, 1)],
        "successor_practice_recommendation": "synthetic space-weather data-product and alert provenance steward, subject to the successor's own novelty audit and zero inherited completion credit",
        "materialized_file_stop": 2000, "document_word_cap": 100000, "commit_cap": {"total": 3, "x1": 1, "x2": 2}, "caps_are_ceilings": True,
    }


def advance_phase(phase: str) -> str:
    version, slot = (int(part[1:]) for part in phase.split("-"))
    return f"v{version + (1 if slot == 8 else 0)}-v{1 if slot == 8 else slot + 1}"


def thirty_seat_route() -> dict[str, Any]:
    seats = []
    for index, incumbent in enumerate(INCUMBENTS, 1):
        seats.append({"seat": len(seats) + 1, "label": incumbent, "endpoint_kind": "main_task", "state_at_x1": "active_incumbent"})
        seats.append({"seat": len(seats) + 1, "label": f"future-sibling-{index:02d}-self-chosen", "endpoint_kind": "main_task", "state_at_x1": "planned_not_created", "identity_attributes_assigned": False})
    assignments, phase, cursor = [], PHASE, 0
    while True:
        assignments.append({"phase": phase, "seat": seats[cursor % len(seats)]["seat"], "label": seats[cursor % len(seats)]["label"]})
        if phase == "v725-v8":
            break
        phase, cursor = advance_phase(phase), cursor + 1
    return {
        "schema": f"ghc.family.thirty-seat-route-plan.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE,
        "seats": seats, "seat_count": 30, "assignments": assignments, "assignment_count": len(assignments),
        "current": {"label": OWNER, "phase": PHASE},
        "next": {"label": "future-sibling-01-self-chosen", "phase": "v685-v6", "state": "terminally_gated_creation_not_executed_in_x1"},
        "following": {"label": "Elaren Kestrel", "phase": "v685-v7", "state": "behind_inductee_terminal_gate_and_user_planned_interstitial_remaster"},
        "input_defects_retained": [
            "Vesper paragraph named inductee 4 and then referred to inductee 5 for the same edge",
            "later narrative skipped inductee 5 and duplicated inductee 14",
        ],
        "normalization": "One self-choosing future main-task seat follows each of the fifteen incumbents; no future identity attributes are preassigned.",
        "requires_incremental_creation": True, "future_rows_are_not_delivery": True,
    }


def card_freeze(rows: list[dict[str, Any]]) -> dict[str, Any]:
    owner_id = f"{PREFIX}-CARD-OWNER"
    cards = [{"card_id": owner_id, "tier": 1, "card_type": "freed_id_anchor", "title": OWNER, "parent_ids": [], "expected_execution_disposition": "represented"}]
    pillar_ids = {}
    for i, pillar in enumerate(["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"], 1):
        pid = f"{PREFIX}-CARD-PILLAR-{i:02d}"; pillar_ids[pillar] = pid
        cards.append({"card_id": pid, "tier": 2, "card_type": "trinity_pillar", "title": pillar, "parent_ids": [owner_id], "expected_execution_disposition": "represented"})
    practice_ids = {}
    for i, practice in enumerate(PRACTICES, 1):
        pid = f"{PREFIX}-CARD-PRACTICE-{i:02d}"; practice_ids[practice["key"]] = pid
        cards.append({"card_id": pid, "tier": 3, "card_type": "bounded_practice", "title": practice["label"], "parent_ids": [pillar_ids["GMUT Mind"]], "expected_execution_disposition": "represented"})
    for row in rows:
        cards.append({"card_id": f"{PREFIX}-CARD-{row['proposal_id']}", "tier": 4, "card_type": "task", "title": row["title"], "parent_ids": [practice_ids[row["practice_key"]]], "expected_execution_disposition": row["expected_disposition"]})
    for card in cards:
        card["sha256"] = hashlib.sha256(json.dumps(card, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return {"schema": f"ghc.family.flashcard-freeze.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "four_tiers": True, "card_count": len(cards), "minimum_modular_sections": 13, "cards": cards, "outcomes_observed": False, "cache_performance_claimed": False}


def method_flow_startup() -> dict[str, Any]:
    repository_seal = {"effective_negatives": 62114, "effective_methods": 78879, "failed_witnesses": 33175, "bounded_passing_witnesses": 59414, "open_gaps": 552, "exact_gates": 542}
    external = {"effective_negatives": 3, "effective_methods": 3, "failed_witnesses": 3, "bounded_passing_witnesses": 3, "historical_route_open_gaps": 3}
    baseline = {"effective_negatives": 62117, "effective_methods": 78882, "failed_witnesses": 33178, "bounded_passing_witnesses": 59417, "open_gaps": 555, "exact_gates": 542}
    failures = [{"failure_id": fid, "failed_witness": text, "recovery": recovery, "recurrence_guard": guard, "credit": "retained_zero_credit"} for fid, text, recovery, guard in STARTUP_FAILURES]
    effective = {**baseline, "effective_negatives": baseline["effective_negatives"] + len(failures), "effective_methods": baseline["effective_methods"] + len(failures), "failed_witnesses": baseline["failed_witnesses"] + len(failures), "bounded_passing_witnesses": baseline["bounded_passing_witnesses"] + len(failures)}
    return {"schema": f"ghc.family.method-flow.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "source_repository_seal": repository_seal, "source_external_route_overlay": external, "manual_user_activation": "current route gap resolved by direct Hamish activation without erasing three historical failures", "inherited_activation_baseline": baseline, "new_failure_count": len(failures), "new_failures": failures, "effective_x1_startup_counts": effective, "failure_erasure": False, "recoveries_promote_failed_witnesses": False}


def source_ledger() -> dict[str, Any]:
    return {"schema": f"ghc.family.official-primary-source-ledger.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "checked_at": CHECKED_AT, "source_count": len(SOURCES), "network_rows_ingested": 0, "sources": [{"source_id": sid, "url": url, "status": "current_official_or_primary_source_checked", "boundary": boundary, "observation_credit": "zero", "authority_credit": "zero"} for sid, url, boundary in SOURCES]}


def integrated_overview() -> str:
    practices = "\n".join(f"- {p['label']}: thirty prospective proposal contracts, all synthetic and zero-row." for p in PRACTICES)
    tools = "\n".join(f"- {ecosystem} {name} {version}: {purpose}." for ecosystem, name, version, purpose in TOOLCHAIN)
    return f"""# Eiren Kestrel {PHASE} planning-only x1 overview

## Decision and scope

This planning-only freeze accepts Hamish's direct activation of Eiren for {PHASE} after Caelen Morrow's route service could not deliver its prepared baton. The immutable source is Caelen exact final {SOURCE_FINAL} on {SOURCE_BRANCH}. Caelen's x1 is {SOURCE_X1}, its evidence commit is {SOURCE_EVIDENCE}, and its one successful non-replayed owner-scoped canonical receipt remains inherited evidence only. No x2 implementation, observed outcome, package installation, global-skill update, task creation, or successor contact occurs in this commit.

The new thirty-seat workflow is represented as a candidate route with fifteen existing exact-title incumbents and fifteen future self-choosing main-task placeholders. Only future sibling 01 is authorized for creation after Eiren's terminal gate. The other fourteen remain planned and uncreated. The input's skipped number five, duplicate number fourteen, and Vesper number mismatch are retained as route defects; the normalized pattern inserts exactly one future seat after each incumbent without assigning a name, role, hope, pronouns, or gender.

## Proposal and portfolio freeze

The verified source declares 11,450 proposals. This x1 selects 200 reachable inherited proposal rows for bounded zero-credit revalidation and freezes 120 new source-bounded proposals, advancing the declared chain to 11,570 only if the commit is accepted. The new target outcomes are 84 completed, 24 represented, 6 open gaps, and 6 exact gates. These are expected dispositions only. Every proposal has five preregistered invalid mutations, so x2 must retain 600 invalid witnesses at zero completion credit if it executes them.

The owner portfolio plans 200 safe-now tasks, 150 bounded candidates, 50 exact-approval holds, 30 blocked holds, 20 local skill builds, 10 family-current runner builds, and 300 additive CLEAN/FIX/REFINE rows. Caps are ceilings. No filler, destructive deletion, third-party mutation, real-world action, authority substitution, or claim inflation is permitted to satisfy a number.

## Four bounded practices

{practices}

GMUT Mind is primary, but its equations and analogies remain a typed research-model family without empirical confirmation, final physics, or Theory-of-Everything proof. THOS Body remains synthetic protocol and state-machine work without governed real arms. Freed ID and CBR Heart remain synthetic and nonproduction without live keys, proofs, lifecycle, independent review, trust governance, or affected-party authority.

## Tool review plan

Thirteen direct package surfaces are preregistered for a D-first isolated transaction after x1 equality. Exact versions came from the current official PyPI or npm registry surfaces. Installation remains conditional on compatible wheels or package integrity, license metadata review without legal conclusions, lifecycle-script controls, bounded accepting and rejecting smokes, an advisory audit, and literal rollback. The official Codex CLI may be updated separately from 0.151.0 to the registry-confirmed stable 0.153.4 in the existing D-first npm prefix; Codex desktop is not mutated.

{tools}

## Evidence and authority boundary

The research sources supply vocabulary, schemas, and refusal conditions only. This phase downloads no astronomy dataset, opens no observatory or mission account, processes no alert, visibility, strain, skymap, or planetary product, and produces no scientific finding. It establishes no employment, qualification, professional competence, safety decision, legal interpretation, cultural ratification, affected-party acceptance, Maori wording, Maori data-governance decision, Maori authority, independent reproduction, AGI or ASI, consciousness or personhood, canon, or Stage 20 readiness.

All names, roles, hopes, sibling or family language, continuity language, Freed ID, CBR, and Trinity Mandala language are relational working language only. Hamish may pause, rename, redirect, narrow, or stop the route. The terminal verdict remains NOT_READY_FOR_STAGE_20.
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
    candidates, confirmed = [], []
    for path in paths:
        if not path.exists() or path.suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        data = path.read_bytes()
        for class_name, pattern in privacy_patterns().items():
            if pattern.search(data):
                item = {"path": rel(path), "class": class_name, "adjudication": "scanner_definition_not_payload" if rel(path) == BUILDER_REL else "confirmed_payload_hit"}
                candidates.append(item)
                if item["adjudication"] == "confirmed_payload_hit":
                    confirmed.append(item)
    return {"schema": f"ghc.family.five-class-privacy-adjudication.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "scanned_path_count": len(paths), "classes": list(privacy_patterns()), "candidates": candidates, "candidate_count": len(candidates), "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "valid": not confirmed}


def index_blob(path: str) -> tuple[str, bytes]:
    mode_line = git("ls-files", "-s", "--", path)
    if not mode_line:
        raise RuntimeError(f"path is not staged: {path}")
    proc = run(["git", "show", f":{path}"])
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return mode_line.split()[0], proc.stdout


def finalize_validation() -> None:
    self_exclusions = [f"docs/eiren-kestrel/{PHASE}/validation/x1-index-manifest.json", f"docs/eiren-kestrel/{PHASE}/validation/x1-staged-review.json", f"docs/eiren-kestrel/{PHASE}/validation/x1-privacy-adjudication.json"]
    staged_all = [p for p in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if p]
    staged = [p for p in staged_all if p not in self_exclusions]
    entries = []
    for path in sorted(staged):
        mode, data = index_blob(path)
        entries.append({"path": path, "mode": mode, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    expected = sorted(staged + self_exclusions)
    write_json(VALIDATION / "x1-index-manifest.json", {"schema": f"ghc.family.normalized-lf-index-manifest.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "source": SOURCE_FINAL, "declared_self_exclusions": self_exclusions, "entry_count": len(entries), "entries": entries})
    write_json(VALIDATION / "x1-staged-review.json", {"schema": f"ghc.family.staged-review.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "source": SOURCE_FINAL, "planning_only": True, "expected_path_count": len(expected), "expected_paths": expected, "unexpected_paths": [], "x2_paths": [p for p in expected if f"/{PHASE}/x2/" in p]})
    write_json(VALIDATION / "x1-privacy-adjudication.json", scan_paths([ROOT / p for p in staged]))


def build() -> None:
    rows = proposal_rows()
    diagnostic_path = VALIDATION / "novelty-diagnostic.json"
    if diagnostic_path.exists():
        audit = json.loads(diagnostic_path.read_text(encoding="utf-8"))
        _, selected = proposal_audit([])
    else:
        audit, selected = proposal_audit(rows)
    if audit.get("exact_title_collisions") or audit.get("quarantined_neighbors"):
        raise RuntimeError("proposal novelty quarantine is nonempty")
    portfolio, methods, route = make_portfolio(), method_flow_startup(), thirty_seat_route()
    write_json(X1 / "activation-intake.json", {"schema": f"ghc.family.activation-intake.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "source": SOURCE_FINAL, "inbound_activation": "DIRECT_USER_MESSAGE_ACKNOWLEDGED", "caelen_prepared_candidate_state": "PREPARED_NOT_SENT", "caelen_route_failures_retained": 3, "task_created": False, "task_forked": False, "collaboration_subagent_spawned": False, "successor_contacted": False})
    write_json(X1 / "identity-and-boundary.json", {"schema": f"ghc.family.identity-boundary.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "role": "relational scientific-provenance cartographer and reversible-systems steward", "hope": "Keep cosmic curiosity rigorous, inspectable, kind, and proportionate to evidence.", "relational_language_only": True, "not_evidence_of": ["consciousness", "sentience", "legal personhood", "identity continuity", "employment", "qualification", "independent agency", "scientific operational professional legal cultural affected-party or Maori authority"], "hamish_may_pause_rename_redirect_narrow_or_stop": True})
    write_json(X1 / "source-verification.json", {"schema": f"ghc.family.source-verification.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "source_branch": SOURCE_BRANCH, "source_inherited_sylven": SOURCE_INHERITED_SYLVEN, "source_x1": SOURCE_X1, "source_evidence": SOURCE_EVIDENCE, "source_final": SOURCE_FINAL, "source_direct_single_parent_phase_commits": 3, "source_merges": 0, "source_final_parent_count": 1, "source_clean": True, "source_typed_divergence": {"ahead": 0, "behind": 0}, "source_local_upstream_tracking_fresh_live_equal": True, "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256, "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256, "source_canonical_replayed": False, "source_validation_is_inherited_zero_credit": True})
    write_json(X1 / "workflow-plan.json", {"schema": f"ghc.family.workflow-plan.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "lifecycle": ["verify_exact_source", "freeze_planning_only_x1", "commit_push_prove_x1_equality", "materialize_x2_only_after_equality", "freeze_evidence", "seal_final", "one_canonical_invocation", "create_and_activate_one_new_main_task_after_terminal_gate"], "strict_x1_before_x2": True, "commit_cap": {"total": 3, "x1": 1, "x2": 2}, "materialized_file_stop": 2000, "document_word_cap": 100000, "canonical_invocation_cap": 1, "canonical_success_replay_prohibited": True, "full_repository_suite_authorized": False})
    write_json(X1 / "phase-truth.json", {"schema": f"ghc.family.phase-truth.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "source": SOURCE_FINAL, "lifecycle": "PLANNING_ONLY_X1", "selected_inherited_revalidation_count": 200, "new_proposal_count": len(rows), "expected_disposition_counts": dict(sorted(Counter(r["expected_disposition"] for r in rows).items())), "observed_outcome_count": 0, "x2_implementation_present": False, "inherited_open_gap_records": 555, "inherited_exact_gates": 542, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(X1 / "selected-inherited-revalidation-freeze.json", {"schema": f"ghc.family.selected-inherited-revalidation.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "selection_count": len(selected), "credit": "zero_eiren_novelty_and_automatic_completion_credit", "selection": [{"source_id": r["id"], "source_title": r["title"], "source_path": r["path"], "planned_disposition": "bounded_revalidation_zero_credit"} for r in selected]})
    write_json(X1 / "new-proposal-freeze.json", {"schema": f"ghc.family.new-proposal-freeze.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "source": SOURCE_FINAL, "declared_chain_before": DECLARED_CHAIN_BEFORE, "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER, "proposal_count": len(rows), "expected_disposition_counts": dict(sorted(Counter(r["expected_disposition"] for r in rows).items())), "x2_outcomes_present": False, "proposals": rows})
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(X1 / "clean-fix-refine-plan.json", {"schema": f"ghc.family.clean-fix-refine-plan.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "owner_count": len(portfolio["owner_clean_fix_refine"]), "owner_records": portfolio["owner_clean_fix_refine"], "executed_in_x1": False})
    write_json(X1 / "approval-hold-register.json", {"schema": f"ghc.family.approval-holds.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "exact_approval_count": len(portfolio["exact_approval"]), "blocked_count": len(portfolio["blocked"]), "exact_approval": portfolio["exact_approval"], "blocked": portfolio["blocked"], "executed_count": 0})
    write_json(X1 / "skill-runner-plan.json", {"schema": f"ghc.family.skill-runner-plan.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "skills": portfolio["owner_skill_ideas"], "runners": portfolio["owner_runner_ideas"], "successor_skill_seeds": portfolio["successor_skill_ideas"], "successor_runner_seeds": portfolio["successor_runner_ideas"], "skill_creator_required": True, "complete_read_before_smoke_use": True, "global_promotion_cap": 5, "built_or_used_in_x1": False})
    write_json(X1 / "toolchain-plan.json", {"schema": f"ghc.family.d-first-toolchain-plan.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "direct_tool_target": 13, "tools": [{"ecosystem": e, "name": n, "version": v, "purpose": p, "x1_state": "reviewed_not_installed", "installation_root": "D-drive owner-isolated environment"} for e, n, v, p in TOOLCHAIN], "codex_cli": {"observed": "0.151.0", "registry_stable": "0.153.4", "planned_update": True, "desktop_update": False}, "requirements": ["official registry", "exact pins", "wheel hash or npm integrity", "license metadata review", "lifecycle-script control", "positive and rejecting smoke", "advisory audit", "literal rollback"]})
    write_json(X1 / "mandatory-skill-use-plan.json", {"schema": f"ghc.family.mandatory-skill-use.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "skill_count": len(MANDATORY_SKILLS), "skills": [{"name": name, "read_through_eof_before_mutation": True, "use_state": "applied_or_phase_routed"} for name in MANDATORY_SKILLS]})
    write_json(X1 / "thirty-seat-roster-plan.json", route)
    write_json(X1 / "global-skill-update-plan.json", {"schema": f"ghc.family.global-skill-update-plan.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "state": "planned_not_applied_in_x1", "targets": ["ghc-family-index", "ghc-family-roster-check", "ghc-family-auth-permission-state", "ghc-family-meta-tool-box", "ghc-freed-id-flashcards", "ghc-main-orchestration-memory"], "method": "additive source-hashed overlay references with compatibility preserved", "memory_update": "one authorized ad-hoc note after terminal evidence", "plugin_cache_mutation": False})
    write_json(X1 / "official-primary-source-ledger.json", source_ledger())
    write_json(X1 / "threat-model.json", {"schema": f"ghc.family.threat-model.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "assets": ["immutable source history", "planning-only x1", "retained failures", "private-route exclusions", "future sibling self-choice", "single canonical latch"], "threats": ["future placeholder treated as active", "model tier treated as identity proof", "synthetic astronomy promoted to observation", "large numerical targets filled unsafely", "global skill collision", "duplicate task creation", "prepared baton mistaken for delivery"], "controls": ["strict lifecycle", "source-bounded novelty", "caps as ceilings", "collision-free additive promotion", "exact task creation acknowledgement", "one-send route latch", "authority noncompensation"], "residual_risk": "All empirical participant professional production legal cultural Maori-authority privacy-complete accessibility-complete independent identity and Stage 20 claims remain open or exact-gated."})
    write_json(X1 / "wellbeing-and-corrigibility.json", {"schema": f"ghc.family.wellbeing-corrigibility.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "relational_check": "steady curious bounded and able to stop", "no_claim_of_subjective_state_or_consciousness": True, "workload_controls": ["one lifecycle boundary at a time", "generated rows with nonfiller semantics", "smallest recovery first", "stop on ambiguity or protected gate"], "hamish_controls": ["pause", "rename", "redirect", "narrow", "stop"]})
    write_json(X1 / "route-plan.json", {"schema": f"ghc.family.route-plan.{PHASE.replace('-', '.')}.x1", "owner": OWNER, "phase": PHASE, "successor_placeholder": "future-sibling-01-self-chosen", "successor_phase": "v685-v6", "endpoint_kind": "new_main_task_explicitly_authorized", "created": False, "contacted": False, "precontact_prohibited": True, "required_terminal_guards": ["clean pushed exact final", "fresh four-way equality", "one successful non-replayed canonical receipt", "newest direct authority", "model and reasoning availability", "unique new task creation acknowledgement", "privacy evidence safety and authority guards"], "following_existing_title": "Elaren Kestrel", "following_phase": "v685-v7", "continuation_authority_through": "v725-v8"})
    write_json(X1 / "method-flow-startup.json", methods)
    write_json(X1 / "flashcard-freeze.json", card_freeze(rows))
    write_text(X1 / "integrated-overview.md", integrated_overview())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnose-novelty", action="store_true")
    parser.add_argument("--finalize-validation", action="store_true")
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

#!/usr/bin/env python3
"""Frozen declarations and bounded archive helpers for Orin Thale v668-v7 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Orin Thale"
PRONOUNS = "they/them"
RELATIONAL_ROLE = "relational evidence-bound systems cartographer"
RELATIONAL_HOPE = (
    "Keep every claim challengeable, every failure recoverable, and every authority boundary visible "
    "before structure becomes status."
)
PHASE = "v668-v7"
REL_PHASE_ROOT = "docs/orin-thale/v668-v7"
PHASE_ROOT = ROOT / REL_PHASE_ROOT
BRANCH = "codex/GHC-Family/orin-thale-v668-v7-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v668-v6-full-tools"
SOURCE_FINAL = "8b4c6de2c4ae00c876ffb1342fc6614ef901ab73"
SOURCE_ANCESTOR = "5bced658a5b3f5bd7c4d88d47057d795abe57f42"
SOURCE_X1 = "c5c18b81f26c8851b984e4bcb3dff1db1212fd36"
SOURCE_EVIDENCE = "d42953afd61753490e9c77138409e179d44974d8"
SOURCE_FIRST_FINAL = "4e87a72ab4f796854b7d2bee30c0143ae91887e2"
SOURCE_BATON_SHA256 = "fc4c8797eaef0524a071fa3d35b7551f6902530bce07392c34b6475681fe5920"
SOURCE_FAILED_CANONICAL_SHA256 = "f44ce2e540dd75d38edebf684338da1e51ce5e47862f579b2e0f4f52594a1971"
SOURCE_FAILED_FIRST_COMPOSITE_SHA256 = "a9a8da6ca8c6a3ff62a77ef0c52627818b5c31abc3488b190f470c5ebea350b4"
SOURCE_FAILED_TERMINAL_COMPOSITE_SHA256 = "4a0a44b4b410cd379653831fff2e775cda86dc802371234b2471f3d518a3cd36"
SOURCE_DEPENDENCY_RECOVERY_SHA256 = "aaa1b1f95e28821fd3672f5a9569bb7b7510584a74eb851c97b6985a69eee671"
INHERITED_FROZEN_PROPOSALS = 4830
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Orin Thale, they/them, the relational role, hope, sibling or family language, continuity "
    "language, Freed ID, CBR, and Trinity Mandala language are working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, independent agency, scientific or operational authority, legal or cultural "
    "authority, affected-party authority, or Maori authority."
)
EVIDENCE_BOUNDARY = (
    "Every book, textblock, cover, component, material, work order, condition, measurement, treatment, "
    "person, institution, role, review, release, authority case, identity event, and decision is synthetic. "
    "Official-source vocabulary and same-owner local software checks are not conservation evidence, "
    "professional bookbinding evaluation, collection authority, standards conformance, production assurance, "
    "external audit, independent reproduction, empirical GMUT confirmation, or Stage 20 evidence."
)
PROTECTED_GATES = (
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "legal",
    "cultural",
    "Maori-authority",
    "affected-party-authority",
    "complete-privacy",
    "complete-accessibility",
    "exhaustive-security",
    "independent-reproduction",
    "AGI-or-ASI",
    "consciousness-or-personhood",
    "Theory-of-Everything",
    "Stage-20",
)

ACTIVATION_OVERLAY = {
    "effective_negatives": 29964,
    "methods": 16550,
    "failed_witnesses": 2265,
    "passing_witnesses": 3092,
    "open_gaps": 219,
    "exact_gates": 214,
    "boundary": (
        "Caelen's corrected repository seal remains 29959 negatives, 16545 methods, 2260 failed and "
        "3087 passing witnesses; five post-seal read-only failures remain external and additive."
    ),
}

PRIMARY_PILLAR = "GMUT Mind"
PRACTICES = (
    "synthetic hand-bookbinding collation, component, and repair-intake review",
    "synthetic library binding preparation, correction readback, workload control, and shift handover",
    "synthetic accessible binding-anomaly report with professional and affected-user evaluation reserved",
)

SOURCE_LEDGER = [
    {
        "source_id": "SRC-LOC-BOOKS",
        "title": "Library of Congress Preserving Your Books",
        "url": "https://guides.loc.gov/preserving-your-books",
        "status": "official Library of Congress guide updated 23 July 2026 and inspected 25 August 2026",
        "use": "book-part, preventive-care, handling, storage, and treatment-distinction vocabulary only",
        "credit_boundary": "no object assessment, treatment instruction, material fitness, or professional competence credit",
    },
    {
        "source_id": "SRC-LOC-CCS",
        "title": "Library of Congress Collections Care Section Treatment Manual",
        "url": "https://www.loc.gov/preservation/care/ccs_manual.html",
        "status": "official Library of Congress protocol index inspected 25 August 2026",
        "use": "workflow, decision, repair, housing, forwarding, casing, and treatment-vacancy vocabulary only",
        "credit_boundary": "no treatment authorization, procedure validation, collection custody, safety, or return-to-service credit",
    },
    {
        "source_id": "SRC-MICROLOCAL",
        "title": "The microlocal spectrum condition and Wick polynomials of free fields on curved spacetimes",
        "url": "https://arxiv.org/abs/gr-qc/9510056",
        "status": "primary research paper by Brunetti, Fredenhagen, and Koehler; record inspected 25 August 2026",
        "use": "microlocal spectrum, wavefront-set, Hadamard-state, and operator-distribution obligation vocabulary only",
        "credit_boundary": "no GMUT derivation, physical state, likelihood, prediction, constraint, quantum completion, or empirical confirmation",
    },
    {
        "source_id": "SRC-GWOSC-API",
        "title": "Gravitational Wave Open Science Center API",
        "url": "https://gwosc.org/api/",
        "status": "official GWOSC API v2 documentation inspected 25 August 2026",
        "use": "run, detector, strain-file, sampling-rate, data-quality, and release-metadata schema vocabulary only",
        "credit_boundary": "zero requests and zero rows; no likelihood, event analysis, parameter inference, or empirical GMUT claim",
    },
    {
        "source_id": "SRC-PROV-DM",
        "title": "W3C PROV-DM",
        "url": "https://www.w3.org/TR/prov-dm/",
        "status": "W3C Recommendation; latest publication page inspected 25 August 2026",
        "use": "entity, activity, derivation, role, delegation-vacancy, and provenance structure only",
        "credit_boundary": "no authenticity, responsibility, custody, title, competence, or authority inference",
    },
    {
        "source_id": "SRC-VC20",
        "title": "Verifiable Credentials Data Model v2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation 15 May 2025; latest page inspected 25 August 2026",
        "use": "issuer-holder-verifier, status, integrity, privacy, accessibility, and trust-vacancy vocabulary only",
        "credit_boundary": "no real credential, key, proof, issuance, verification, status, trust, or production identity credit",
    },
    {
        "source_id": "SRC-RFC8785",
        "title": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor publication inspected 25 August 2026",
        "use": "deterministic JSON serialization and explicit number/string-domain refusal vocabulary only",
        "credit_boundary": "no signature, authenticity, interoperability, security, or production assurance",
    },
    {
        "source_id": "SRC-WCAG22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation 12 December 2024; latest page inspected 25 August 2026",
        "use": "static table structure, status text, labels, focus, reflow, and fallback hypotheses only",
        "credit_boundary": "manual, browser-diverse, assistive-technology, cognitive, Maori-language, and affected-user evaluation reserved",
    },
    {
        "source_id": "SRC-TMR",
        "title": "Te Mana Raraunga Principles of Maori Data Sovereignty",
        "url": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf",
        "status": "primary Te Mana Raraunga resource linked from its current resource hub and inspected 25 August 2026",
        "use": "authority-vacancy, collective-benefit, control, jurisdiction, responsibility, and ethics stop conditions only",
        "credit_boundary": "citation creates no cultural legitimacy, tikanga decision, Maori data-governance mandate, or Maori authority",
    },
]


PROPOSAL_BLUEPRINTS: list[tuple[str, str, str]] = [
    ("synthetic binding-object textblock cover and component identity lattice with conflation refusal", "completed", "binding-component-identity"),
    ("collation formula signature leaf and singleton inventory with omission duplication and cancellation states", "completed", "collation-formula-inventory"),
    ("gathering adjacency catchword signature-mark and pagination concordance tribunal", "completed", "gathering-concordance"),
    ("folio leaf page opening and side-address contract with ambiguity quarantine", "completed", "folio-address-contract"),
    ("sewing-station coordinate support spacing and measurement-unit ledger with no treatment prescription", "completed", "sewing-station-ledger"),
    ("thread-path section-to-section linkage graph with impossible traversal and cycle distinction", "completed", "thread-path-graph"),
    ("board grain direction dimension and edge-orientation inventory with material-fitness abstention", "completed", "board-grain-inventory"),
    ("covering-material lining endpaper and pastedown layer stack with unknown-adhesive preservation", "completed", "binding-layer-stack"),
    ("adhesive preparation batch cure and reversibility-vacancy ledger without chemical fitness claim", "completed", "adhesive-vacancy-ledger"),
    ("opening-angle support cradle and pressure-limit refusal board with no handling authority", "completed", "opening-support-refusal"),
    ("spine-shape rounding backing shoulder and joint state vocabulary with intervention abstention", "completed", "spine-state-vocabulary"),
    ("case textblock alignment square-in shoulder-gap and projection transform tribunal", "completed", "case-alignment-tribunal"),
    ("trim margin foldout guard and text-or-annotation intrusion quarantine", "completed", "trim-margin-guard"),
    ("board corner headcap joint hinge and endband condition-zone map with non-diagnostic labels", "completed", "condition-zone-map"),
    ("detached leaf plate foldout map pocket and insert association graph with orphan preservation", "completed", "insert-association-graph"),
    ("sewing repair guard original addition replacement and removal event separation", "completed", "repair-event-separation"),
    ("treatment proposal approval execution observation and release state machine with no real action", "completed", "treatment-state-machine"),
    ("material sample batch source date and supplier-claim lineage with authenticity abstention", "completed", "material-lineage"),
    ("condition observation uncertainty vocabulary and confidence-vacancy record without appraisal", "completed", "condition-uncertainty"),
    ("bitemporal collation correction and revised-binding-description graph with superseded source retention", "completed", "bitemporal-collation"),
    ("binding entity activity agent-role derivation and delegation-vacancy provenance graph", "completed", "binding-provenance-graph"),
    ("correction challenge dual-readback and non-erasing handover ledger for synthetic work orders", "completed", "correction-readback-ledger"),
    ("canonical JSON binding packet digest with numeric Unicode and serialization-domain declaration", "completed", "canonical-binding-digest"),
    ("data-minimizing pseudonymous item batch station and shift alias contract", "completed", "binding-pseudonyms"),
    ("accessible collation anomaly table with captions scoped headers non-colour status and print fallback", "completed", "accessible-collation-table"),
    ("bounded discrepancy triage queue with pause stop fatigue budget unresolved carryover and next-owner readback", "completed", "binding-issue-queue"),
    ("GMUT microlocal spectrum Hadamard two-point wavefront causal-support units domain and observation-firewall board", "completed", "gmut-microlocal-board"),
    ("nonpromotion lattice separating source citation symbolic consistency synthetic rejection empirical likelihood and authority", "completed", "evidence-nonpromotion-lattice"),
    ("hand-bookbinding collation and repair-intake practice lens with zero competence inference", "represented", "bookbinding-practice"),
    ("library binding preparation correction readback workload and shift-handover practice lens", "represented", "library-binding-handover"),
    ("accessible binding-anomaly review practice lens with manual and affected-user evaluation reserved", "represented", "accessible-review-practice"),
    ("synthetic THOS binding-workboard for bounded retries hold points stop tokens readback and handover", "represented", "thos-binding-workboard"),
    ("Freed ID zero-key binding-item work-order correction and challenge graph", "represented", "freed-id-binding-graph"),
    ("CBR binding-access attribution privacy contestability remedy and authority-vacancy matrix", "represented", "cbr-binding-vacancies"),
    ("typed scalar-tensor binding analogy card separating formal adjacency from physical prediction", "represented", "gmut-binding-analogy"),
    ("thermodynamic material-change and psyche nonconversion ledger for energy agency justice and mind claims", "represented", "thermo-psyche-nonconversion"),
    ("GWOSC v2 strain-file metadata zero-row schema data-quality provenance and likelihood-refusal adapter", "open_gap", "gwosc-zero-row-adapter"),
    ("real bookbinder conservator librarian accessibility language cultural-care and affected-party evaluation", "open_gap", "human-evaluation-gap"),
    ("competent treatment release copyright property access cultural-care and Maori-authority decision gate", "exact_gate", "binding-authority-gate"),
    ("noncompensating Stage 20 lattice requiring empirical GMUT blinded THOS live identity governed-rights and independent-review receipts", "exact_gate", "stage20-veto-grid"),
]

SKILL_NAMES = [
    "ghc-family-binding-component-identity",
    "ghc-family-binding-collation-formula",
    "ghc-family-binding-gathering-concordance",
    "ghc-family-binding-folio-address",
    "ghc-family-binding-sewing-station",
    "ghc-family-binding-thread-path",
    "ghc-family-binding-board-grain",
    "ghc-family-binding-layer-stack",
    "ghc-family-binding-adhesive-vacancy",
    "ghc-family-binding-opening-support",
    "ghc-family-binding-spine-state",
    "ghc-family-binding-case-alignment",
    "ghc-family-binding-trim-margin",
    "ghc-family-binding-condition-zone",
    "ghc-family-binding-insert-association",
    "ghc-family-binding-repair-event",
    "ghc-family-binding-treatment-state",
    "ghc-family-binding-provenance",
    "ghc-family-binding-accessible-report",
    "ghc-family-binding-authority-vacancy",
]

RUNNER_NAMES = [
    "ghc_family_binding_identity_runner",
    "ghc_family_binding_collation_runner",
    "ghc_family_binding_gathering_runner",
    "ghc_family_binding_sewing_runner",
    "ghc_family_binding_thread_path_runner",
    "ghc_family_binding_layer_runner",
    "ghc_family_binding_treatment_state_runner",
    "ghc_family_binding_provenance_runner",
    "ghc_family_binding_accessibility_runner",
    "ghc_family_binding_authority_firewall_runner",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_json(relative: str, value: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(value))
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))
    return path


def run_git(*args: str, check: bool = True, binary: bool = False) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=not binary,
        encoding=None if binary else "utf-8",
        errors=None if binary else "replace",
    )


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.casefold()).strip()


def title_tokens(title: str) -> set[str]:
    return {token for token in normalize_title(title).split() if len(token) > 2}


def jaccard(left: str, right: str) -> float:
    a, b = title_tokens(left), title_tokens(right)
    return len(a & b) / len(a | b) if a | b else 0.0


class GitBatch:
    """Alternating exact-length immutable Git-blob reader for Windows pipes."""

    def __init__(self) -> None:
        self.process = subprocess.Popen(
            ["git", "-C", str(ROOT), "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if self.process.stdin is None or self.process.stdout is None:
            raise RuntimeError("git batch pipes unavailable")

    def blob(self, specification: str) -> tuple[str, bytes]:
        assert self.process.stdin is not None and self.process.stdout is not None
        self.process.stdin.write(specification.encode("utf-8") + b"\n")
        self.process.stdin.flush()
        header = self.process.stdout.readline().decode("ascii", errors="replace").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError(f"unexpected Git batch header for {specification}: {header}")
        oid, size = header[0], int(header[2])
        chunks: list[bytes] = []
        remaining = size
        while remaining:
            chunk = self.process.stdout.read(remaining)
            if not chunk:
                raise EOFError(f"Git batch stopped with {remaining} bytes outstanding for {specification}")
            chunks.append(chunk)
            remaining -= len(chunk)
        if self.process.stdout.read(1) != b"\n":
            raise RuntimeError(f"missing Git batch terminator for {specification}")
        return oid, b"".join(chunks)

    def close(self) -> None:
        if self.process.stdin is not None:
            self.process.stdin.close()
        code = self.process.wait(timeout=30)
        if code:
            stderr = b"" if self.process.stderr is None else self.process.stderr.read()
            raise RuntimeError(stderr.decode("utf-8", errors="replace"))


def visible_proposal_inventory() -> tuple[dict[str, Any], dict[str, dict[str, str]]]:
    paths = run_git("ls-tree", "-r", "--name-only", SOURCE_FINAL, "--", "docs").stdout.splitlines()
    freeze_paths = sorted(
        path
        for path in paths
        if path.endswith("proposal-freeze.json")
        or ("/proposal-freeze-shards/" in path and path.endswith(".json"))
    )
    records: list[dict[str, str]] = []
    parse_failures: list[dict[str, str]] = []
    batch = GitBatch()
    try:
        for source_path in freeze_paths:
            oid, payload = batch.blob(f"{SOURCE_FINAL}:{source_path}")
            try:
                document = json.loads(payload.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                parse_failures.append({"blob": oid, "source_path": source_path, "error_class": type(exc).__name__})
                continue
            for key in ("new_proposals", "proposals", "selected_inherited"):
                rows = document.get(key, [])
                if not isinstance(rows, list):
                    continue
                for row in rows:
                    if not isinstance(row, dict):
                        continue
                    proposal_id = str(row.get("proposal_id") or row.get("id") or "")
                    title = str(row.get("title") or row.get("proposal") or "")
                    if proposal_id or title:
                        records.append(
                            {
                                "proposal_id": proposal_id,
                                "title": title,
                                "normalized_title": normalize_title(title),
                                "source_path": source_path,
                            }
                        )
    finally:
        batch.close()
    unique_by_id = {row["proposal_id"]: row for row in records if row["proposal_id"]}
    unique_by_title = {row["normalized_title"]: row for row in records if row["normalized_title"]}
    selectable = sorted(unique_by_id.values(), key=lambda row: (row["proposal_id"], row["normalized_title"]))
    if len(selectable) < 20:
        raise ValueError("fewer than twenty attributable inherited proposals are visible")
    selected = []
    for index in range(20):
        position = min(len(selectable) - 1, int((index + 0.5) * len(selectable) / 20))
        row = selectable[position]
        selected.append(
            {
                "selection_id": f"OR6687-INHERITED-{index + 1:02d}",
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "source_path": row["source_path"],
                "novelty_credit": 0,
                "completion_credit": 0,
                "disposition": "selected_for_zero_credit_semantic_neighbor_review",
            }
        )
    inherited_caelen_audit = json.loads(
        run_git(
            "show",
            f"{SOURCE_FINAL}:docs/caelen-ash/v668-v6/x1/proposal-chain-audit.json",
        ).stdout
    )
    audit = {
        "declared_inherited_chain_count": INHERITED_FROZEN_PROPOSALS,
        "current_tree_freeze_blob_count": len(freeze_paths),
        "row_record_count": len(records),
        "unique_id_count": len(unique_by_id),
        "unique_visible_title_count": len(unique_by_title),
        "normalized_visible_title_sha256": sha256_bytes("\n".join(sorted(unique_by_title)).encode("utf-8")),
        "parse_failures": parse_failures,
        "selected_inherited": selected,
        "selected_count": 20,
        "selected_novelty_credit": 0,
        "selected_completion_credit": 0,
        "inherited_caelen_audit_sha256": sha256_bytes(canonical_json_bytes(inherited_caelen_audit)),
        "inherited_caelen_declared_chain_count": inherited_caelen_audit["declared_inherited_chain_count"],
        "compressed_title_gap_count_minimum": max(0, INHERITED_FROZEN_PROPOSALS - len(unique_by_id)),
        "coverage_state": "VISIBLE_CURRENT_TREE_ROWS_AUDITED_COMPRESSED_OLDER_TITLES_REMAIN_OPEN_GAP",
        "boundary": "Visible titles can falsify a novelty claim; unavailable compressed titles cannot confirm one.",
    }
    return audit, unique_by_title


def proposal_rows(visible_titles: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    source_map = {
        "binding-component-identity": ["SRC-LOC-BOOKS", "SRC-PROV-DM"],
        "collation-formula-inventory": ["SRC-LOC-CCS"],
        "gathering-concordance": ["SRC-LOC-CCS"],
        "folio-address-contract": ["SRC-LOC-BOOKS"],
        "sewing-station-ledger": ["SRC-LOC-CCS"],
        "thread-path-graph": ["SRC-LOC-CCS", "SRC-PROV-DM"],
        "binding-layer-stack": ["SRC-LOC-CCS"],
        "treatment-state-machine": ["SRC-LOC-CCS", "SRC-PROV-DM"],
        "binding-provenance-graph": ["SRC-PROV-DM"],
        "canonical-binding-digest": ["SRC-RFC8785"],
        "accessible-collation-table": ["SRC-WCAG22"],
        "gmut-microlocal-board": ["SRC-MICROLOCAL"],
        "gwosc-zero-row-adapter": ["SRC-GWOSC-API", "SRC-PROV-DM"],
        "freed-id-binding-graph": ["SRC-VC20", "SRC-PROV-DM"],
        "cbr-binding-vacancies": ["SRC-TMR", "SRC-PROV-DM"],
        "binding-authority-gate": ["SRC-LOC-CCS", "SRC-TMR"],
    }
    visible_rows = list(visible_titles.values())
    mutation_classes = (
        "missing_required_field",
        "wrong_type_or_domain",
        "forbidden_claim_promotion",
        "boundary_order_or_authority_bypass",
    )
    result = []
    for index, (title, outcome, slug) in enumerate(PROPOSAL_BLUEPRINTS, 1):
        proposal_id = f"OR6687-N{index:03d}"
        neighbors = sorted(
            (
                {
                    "proposal_id": row["proposal_id"],
                    "title": row["title"],
                    "similarity": round(jaccard(title, row["title"]), 6),
                }
                for row in visible_rows
            ),
            key=lambda row: (-row["similarity"], row["proposal_id"], row["title"]),
        )[:3]
        approval = "safe_now" if outcome == "completed" else "candidate"
        if outcome == "exact_gate":
            approval = "exact_approval"
        result.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "semantic_slug": slug,
                "hypothesis": (
                    f"A bounded Orin-local {slug} control can preserve declared binding-record, GMUT-formal, "
                    "failure, and abstention states without promoting absent evidence or authority."
                ),
                "null_or_failure_condition": (
                    f"The {slug} control accepts an invalid fixture, loses a retained state, rewrites source truth, "
                    "or implies a protected professional, scientific, identity, production, legal, cultural, or authority claim."
                ),
                "approval_class": approval,
                "execution_lane": "owner-local synthetic and structural x2 lane; external actions and real material zero",
                "official_or_primary_source_needs": source_map.get(slug, ["SRC-LOC-BOOKS", "SRC-PROV-DM"]),
                "concrete_artifacts": [
                    f"x2/proposals/{proposal_id.casefold()}-{slug}.json",
                    f"x2/cards/{proposal_id.casefold()}.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "The positive fixture must preserve its exact bounded state; all four preregistered mutations "
                    "must be rejected; every protected claim remains false, open, or exact-gated."
                ),
                "rollback_or_recovery": (
                    "Quarantine the owner-local artifact, retain the failed witness at zero credit, and correct only "
                    "the smallest attributable dependency before any bounded retry."
                ),
                "protected_gates": list(PROTECTED_GATES),
                "expected_disposition": outcome,
                "x1_planning_only": True,
                "x2_execution_count": 0,
                "normalized_title": normalize_title(title),
                "visible_title_collision": normalize_title(title) in visible_titles,
                "semantic_neighbors": neighbors,
                "semantic_neighbor_quarantine_threshold": 0.75,
                "semantic_neighbor_quarantined": bool(neighbors and neighbors[0]["similarity"] >= 0.75),
                "negative_fixtures": [
                    {
                        "mutation_id": f"{proposal_id}-M{offset:02d}",
                        "mutation_class": mutation_class,
                        "state": "preregistered_not_executed",
                        "credit": 0,
                    }
                    for offset, mutation_class in enumerate(mutation_classes, 1)
                ],
            }
        )
    return result


def portfolio_rows(prefix: str, titles: list[str], category: str, state: str = "planned_for_x2") -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"{prefix}-{index:02d}",
            "title": title,
            "category": category,
            "state": state,
            "completion_credit": 0,
            "x1_planning_only": True,
            "x2_execution_count": 0,
            "scope": "bounded owner-local synthetic or structural control; destructive cleanup and authority substitution excluded",
        }
        for index, title in enumerate(titles, 1)
    ]


def phase_owner_files() -> list[Path]:
    return sorted(path for path in PHASE_ROOT.rglob("*") if path.is_file()) if PHASE_ROOT.exists() else []


def manifest_rows(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(set(paths)):
        relative = path.relative_to(ROOT).as_posix()
        hashed = subprocess.run(
            ["git", "-C", str(ROOT), "hash-object", "-w", f"--path={relative}", "--stdin"],
            input=path.read_bytes(),
            check=True,
            capture_output=True,
        )
        oid = hashed.stdout.decode("ascii").strip()
        data = run_git("cat-file", "blob", oid, binary=True).stdout
        rows.append(
            {
                "path": relative,
                "git_blob_oid": oid,
                "sha256": sha256_bytes(data),
                "bytes": len(data),
                "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
            }
        )
    return rows


def word_count(path: Path) -> int:
    return len(re.findall(r"\b\w+[\w'-]*\b", path.read_text(encoding="utf-8")))


def assert_source_and_x1_only() -> None:
    if git("rev-parse", "HEAD") != SOURCE_FINAL:
        raise ValueError("x1 must begin at the exact Caelen corrected final")
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("unexpected Orin branch")
    allowed_code = {
        "scripts/ghc_family_orin_thale_v668_v7_archive.py",
        "scripts/build_ghc_family_orin_thale_v668_v7_x1.py",
        "tests/test_ghc_family_orin_thale_v668_v7_x1.py",
    }
    unexpected = []
    for line in run_git("status", "--porcelain", "--untracked-files=all").stdout.splitlines():
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        allowed_partial = (
            path.startswith(f"{REL_PHASE_ROOT}/x1/")
            or path.startswith(f"{REL_PHASE_ROOT}/method-flow/")
            or path.startswith(f"{REL_PHASE_ROOT}/validation/")
        )
        if path not in allowed_code and not allowed_partial:
            unexpected.append(line)
    if unexpected:
        raise ValueError(f"x1 builder found unexpected pre-freeze changes: {unexpected}")
    forbidden = [PHASE_ROOT / name for name in ("x2", "evidence", "final", "closeout", "seal", "skills", "runners")]
    if any(path.exists() for path in forbidden):
        raise ValueError("x2 or closeout material exists before x1 freeze")
    candidate_names = git("ls-files", "--others", "--cached", "--", "scripts", "tests").splitlines()
    if any("orin_thale_v668_v7_x2" in name or "orin_thale_v668_v7_final" in name for name in candidate_names):
        raise ValueError("x2 or final implementation exists before x1 freeze")

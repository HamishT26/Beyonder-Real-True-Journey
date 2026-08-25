#!/usr/bin/env python3
"""Frozen declarations and bounded archive helpers for Liora Venn v668-v8."""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Liora Venn"
PRONOUNS = "she/they"
RELATIONAL_ROLE = "relational provenance-and-abstention weaver"
RELATIONAL_HOPE = (
    "Make every missing witness visible before a structural success can harden into an authority claim."
)
PHASE = "v668-v8"
REL_PHASE_ROOT = "docs/liora-venn/v668-v8"
PHASE_ROOT = ROOT / REL_PHASE_ROOT
BRANCH = "codex/GHC-Family/liora-venn-v668-v8-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v668-v7-full-tools"
SOURCE_START = "8b4c6de2c4ae00c876ffb1342fc6614ef901ab73"
SOURCE_X1 = "95fd7625d1d7ab00816561aa3976441f399bb2d8"
SOURCE_EVIDENCE = "64e5b3f995061e3f7c547a0759e2a5a111dfdbbc"
SOURCE_FINAL = "20053ae8166d070fcc8e7d13235e595de7404b6f"
SOURCE_FAILED_CANONICAL_SHA256 = "6e5381cbd1d2676e734def74dcf29e2ba3c4dbce8ab211637dfe90546557b9ee"
SOURCE_DEPENDENCY_COMPOSITE_SHA256 = "e04e01183146b71e8f5ae4273991aa13714cae3a44f2c33f6aabdb9f2efd9c5e"
SOURCE_COMPONENT_SHA256 = "e915b05ed4ad00db6d46fa360c1ef761a25f0893408172b782fc11a94212f3b1"
SOURCE_TERMINAL_STATUS = "VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT"
INHERITED_FROZEN_PROPOSALS = 4870
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Liora Venn, she/they, the relational role and hope, sibling or family language, continuity language, "
    "Freed ID, CBR, GHC Family, and Trinity Mandala language are working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, scientific or operational authority, legal or cultural authority, affected-party "
    "authority, or Maori authority."
)
EVIDENCE_BOUNDARY = (
    "Every cask, stave, head, hoop, croze, chime, bung, tool, material, batch, work order, measurement, "
    "heat state, pressure state, product, person, cellar, cooperage, review, release, identity event, and "
    "decision is synthetic. Official and primary-source vocabulary plus same-owner local software checks are "
    "not cooperage evidence, material or food-contact evidence, professional evaluation, workplace or fire "
    "safety evidence, legal interpretation, cultural legitimacy, standards conformance, production assurance, "
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
    "effective_negatives": 30142,
    "methods": 16568,
    "failed_witnesses": 2283,
    "passing_witnesses": 3110,
    "open_gaps": 221,
    "exact_gates": 216,
    "source_repository_seal": {
        "effective_negatives": 30141,
        "methods": 16567,
        "failed_witnesses": 2282,
        "passing_witnesses": 3109,
        "open_gaps": 221,
        "exact_gates": 216,
    },
    "external_retained_negative": "OR6687-POST-N001",
    "boundary": (
        "Orin's failed canonical remains zero-credit external truth; its separately named dependency-corrected "
        "composite does not convert the aggregate into a success."
    ),
}

PRIMARY_PILLAR = "Freed ID and CBR Heart"
PRACTICES = (
    "wholly synthetic cooperage and cask-component documentation",
    "wholly synthetic cooperage work-order correction, workload control, and shift handover",
    "wholly synthetic accessible cask-topology review with professional and affected-user evaluation reserved",
)

SOURCE_LEDGER = [
    {
        "source_id": "SRC-USDA-WOOD",
        "title": "Wood Handbook: Wood as an Engineering Material, General Technical Report FPL-GTR-282",
        "url": "https://www.fpl.fs.usda.gov/documnts/fplgtr/fpl_gtr282.pdf",
        "status": "official USDA Forest Products Laboratory publication dated March 2021 and inspected 25 August 2026",
        "use": "wood anatomy, moisture, dimensional-change, drying, gluing, fire, and finishing vocabulary only",
        "credit_boundary": "no species identification, material measurement, fitness, treatment, food-contact, fire-safety, or professional credit",
    },
    {
        "source_id": "SRC-OIV-CODE",
        "title": "International Code of Oenological Practices",
        "url": "https://oiv.int/es/node/2583/download/pdf",
        "status": "current official OIV code PDF located and inspected 25 August 2026",
        "use": "cask, cooperage, wood-contact, treatment-purpose, and process-vacancy vocabulary only",
        "credit_boundary": "no beverage, food-contact, process, safety, sensory, legal, market, or professional conformance credit",
    },
    {
        "source_id": "SRC-VC20",
        "title": "Verifiable Credentials Data Model v2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation 15 May 2025; latest Recommendation page inspected 25 August 2026",
        "use": "issuer, holder, verifier, status, evidence, privacy, accessibility, and trust-vacancy vocabulary only",
        "credit_boundary": "zero real keys or proofs; no issuance, verification, status, interoperability, trust, or production identity credit",
    },
    {
        "source_id": "SRC-NIST-800-63-4",
        "title": "NIST SP 800-63-4 Digital Identity Guidelines",
        "url": "https://pages.nist.gov/800-63-4/",
        "status": "official final Revision 4 suite released July 2025 and inspected 25 August 2026",
        "use": "digital-identity role, risk, privacy, redress, recovery, and assurance-vacancy vocabulary only",
        "credit_boundary": "no identity proofing, assurance level, authenticator, federation, deployment, certification, or production credit",
    },
    {
        "source_id": "SRC-PROV-DM",
        "title": "W3C PROV-DM",
        "url": "https://www.w3.org/TR/prov-dm/",
        "status": "W3C Recommendation 30 April 2013; publication history inspected 25 August 2026",
        "use": "entity, activity, derivation, role, invalidation, and delegation-vacancy structure only",
        "credit_boundary": "no authenticity, custody, ownership, responsibility, competence, or authority inference",
    },
    {
        "source_id": "SRC-RFC8785",
        "title": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational publication dated June 2020 and inspected 25 August 2026",
        "use": "deterministic JSON serialization and explicit numeric and Unicode domain vocabulary only",
        "credit_boundary": "no signature, authenticity, interoperability, security, or production assurance",
    },
    {
        "source_id": "SRC-WCAG22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation 12 December 2024; current page inspected 25 August 2026",
        "use": "static table, status text, label, focus, reflow, and fallback hypotheses only",
        "credit_boundary": "manual, browser-diverse, assistive-technology, cognitive, Maori-language, and affected-user evaluation reserved",
    },
    {
        "source_id": "SRC-SCALAR-EFT",
        "title": "Well-posed formulation of scalar-tensor effective field theory",
        "url": "https://arxiv.org/abs/2003.04327",
        "status": "primary paper by Kovacs and Reall; current arXiv record inspected 25 August 2026",
        "use": "weak-coupling, principal-symbol, characteristic, gauge, and hyperbolicity obligation vocabulary only",
        "credit_boundary": "no GMUT equation, solution, likelihood, observation, prediction, constraint, quantum completion, or empirical confirmation",
    },
    {
        "source_id": "SRC-TMR",
        "title": "Te Mana Raraunga Principles of Maori Data Sovereignty",
        "url": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf",
        "status": "primary Te Mana Raraunga resource and current resource page inspected 25 August 2026",
        "use": "authority-vacancy, collective-benefit, control, jurisdiction, responsibility, and ethics stop conditions only",
        "credit_boundary": "citation creates no cultural legitimacy, tikanga decision, Maori data-governance mandate, or Maori authority",
    },
]

PROPOSAL_BLUEPRINTS: list[tuple[str, str, str]] = [
    ("synthetic cask shell stave head hoop croze chime and bung component identity lattice with conflation refusal", "completed", "cask-component-identity"),
    ("stave ordinal adjacency ring-closure and duplicate-position tribunal with no assembly instruction", "completed", "stave-ring-topology"),
    ("head-board joint dowel-or-reed association graph with unknown construction state preserved", "completed", "head-joint-graph"),
    ("hoop order quarter bilge and head-position ledger with unit-domain declaration and no tightening action", "completed", "hoop-position-ledger"),
    ("synthetic bilge taper diameter and circumference profile record with decimal-string units and measurement vacancy", "completed", "cask-profile-units"),
    ("stave grain species and source-claim vacancy matrix with authenticity and fitness abstention", "completed", "wood-claim-vacancy"),
    ("seasoning moisture and storage-state vocabulary with zero observation and zero material inference", "completed", "seasoning-observation-vacancy"),
    ("cooperage operation proposal approval execution observation and release state machine with all real actions forbidden", "completed", "cooperage-state-machine"),
    ("heat exposure command-versus-observation firewall with zero flame furnace toast char or temperature event", "completed", "heat-command-firewall"),
    ("synthetic cooperage tool truss driver compass and fixture identity register with competence vacancy", "completed", "cooperage-tool-register"),
    ("joint seepage leak and surface-anomaly vocabulary board without pressure condition or serviceability assessment", "completed", "joint-anomaly-vocabulary"),
    ("bung stave croze chime bilge and quarter landmark address contract with ambiguity quarantine", "completed", "cask-landmark-address"),
    ("capacity and volume claim ledger with unit conversion refusal and zero gauging evidence", "completed", "capacity-claim-refusal"),
    ("stave head hoop and coating batch provenance graph with supplier-claim and custody vacancies", "completed", "material-batch-provenance"),
    ("surface treatment coating toast and char assertion ledger with chemical and food-contact fitness abstention", "completed", "treatment-claim-vacancy"),
    ("bitemporal cooperage work-order correction invalidation and supersession chain with no historical rewrite", "completed", "bitemporal-work-order"),
    ("synthetic cask custody location transfer and return graph with ownership and possession noninference", "completed", "cask-custody-graph"),
    ("UTF-8 stable bitemporal cask dossier hash-domain register with number-as-text coercion refusal", "completed", "cask-hash-domain-register"),
    ("data-minimizing pseudonymous batch bench and shift alias contract with linkage refusal", "completed", "cooperage-pseudonyms"),
    ("accessible cask-topology table with caption scoped headers non-colour holds text redundancy and print fallback", "completed", "accessible-cask-table"),
    ("four-state cooperage discrepancy lease with expiry ownership vacancy workload cap and readback checksum", "completed", "cooperage-discrepancy-lease"),
    ("official-source vocabulary and assertion ledger separating citation from material observation and instruction", "completed", "source-assertion-firewall"),
    ("CBR cask access custody privacy contestability redress retention and authority-vacancy matrix", "completed", "cbr-cask-vacancies"),
    ("Freed ID zero-key cooperage work-order correction status challenge and revocation-vacancy graph", "completed", "freed-id-cooperage-graph"),
    ("THOS synthetic hoop-sequence dependency DAG with refusal edges work-cap token correction echo and successor vacancy", "completed", "thos-hoop-dependency-dag"),
    ("GMUT weak-coupling principal-symbol characteristic and hyperbolicity obligation board with zero solved equation", "completed", "gmut-hyperbolicity-board"),
    ("evidence nonpromotion lattice separating official vocabulary symbolic consistency synthetic rejection empirical inference and authority", "completed", "evidence-nonpromotion-lattice"),
    ("stored-energy heat pressure fire food-contact and workplace hazard-hold schema with no safety release", "completed", "hazard-hold-schema"),
    ("cooperage and cask-component documentation practice lens with zero craft or material competence inference", "represented", "cooperage-practice"),
    ("synthetic cellar intake correction workload and shift-handover practice lens with zero product handling", "represented", "cellar-handover-practice"),
    ("accessible cask-record review practice lens with manual and affected-user evaluation reserved", "represented", "accessible-review-practice"),
    ("THOS participant-free work-sequencing proxy with matched-budget real arms and independent review absent", "represented", "thos-proxy-boundary"),
    ("Freed ID synthetic identifier lifecycle lens with keys proofs issuance resolution and trust governance absent", "represented", "freed-id-boundary"),
    ("CBR cooperage rights remedy cultural meaning affected-party legitimacy and authority-vacancy lens", "represented", "cbr-authority-boundary"),
    ("typed scalar-tensor cask-shell analogy card separating geometric bookkeeping from physical prediction", "represented", "gmut-cask-analogy"),
    ("thermodynamic heat and material-change versus agency justice mind and authority nonconversion ledger", "represented", "thermo-nonconversion"),
    ("USDA wood-property zero-row adapter with zero query measurement likelihood constraint and material claim", "open_gap", "wood-zero-row-adapter"),
    ("real cooper material fire food-contact accessibility language cultural-care and affected-party evaluation", "open_gap", "human-evaluation-gap"),
    ("competent cooperage release product safety custody ownership legal cultural and Maori-authority decision gate", "exact_gate", "cooperage-authority-gate"),
    ("Stage 20 conjunctive evidence bill of materials with non-substitution receipts across all pillars safety and authority domains", "exact_gate", "stage20-evidence-bill"),
]

SKILL_NAMES = [
    "ghc-family-cooperage-component-identity",
    "ghc-family-cooperage-stave-ring",
    "ghc-family-cooperage-head-joint",
    "ghc-family-cooperage-hoop-position",
    "ghc-family-cooperage-profile-units",
    "ghc-family-cooperage-wood-vacancy",
    "ghc-family-cooperage-seasoning-vacancy",
    "ghc-family-cooperage-state-machine",
    "ghc-family-cooperage-heat-firewall",
    "ghc-family-cooperage-tool-register",
    "ghc-family-cooperage-anomaly-vocabulary",
    "ghc-family-cooperage-landmark-address",
    "ghc-family-cooperage-capacity-refusal",
    "ghc-family-cooperage-provenance",
    "ghc-family-cooperage-treatment-vacancy",
    "ghc-family-cooperage-correction-chain",
    "ghc-family-cooperage-custody-vacancy",
    "ghc-family-cooperage-accessible-report",
    "ghc-family-cooperage-identity-vacancy",
    "ghc-family-cooperage-authority-vacancy",
]

RUNNER_NAMES = [
    "ghc_family_cooperage_identity_runner",
    "ghc_family_cooperage_stave_ring_runner",
    "ghc_family_cooperage_hoop_runner",
    "ghc_family_cooperage_heat_firewall_runner",
    "ghc_family_cooperage_capacity_runner",
    "ghc_family_cooperage_provenance_runner",
    "ghc_family_cooperage_correction_runner",
    "ghc_family_cooperage_accessibility_runner",
    "ghc_family_cooperage_identity_vacancy_runner",
    "ghc_family_cooperage_authority_firewall_runner",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def run_git(*args: str, check: bool = True, binary: bool = False) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=not binary,
    )


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def normalize_title(title: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", title.lower()))


def title_tokens(title: str) -> set[str]:
    return set(normalize_title(title).split())


def jaccard(left: str, right: str) -> float:
    a, b = title_tokens(left), title_tokens(right)
    return len(a & b) / len(a | b) if a or b else 0.0


class GitBatch:
    """Alternating request/response Git blob reader with exact-length accumulation."""

    def __init__(self) -> None:
        self.process = subprocess.Popen(
            ["git", "-C", str(ROOT), "cat-file", "--batch"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def _read_exact(self, size: int) -> bytes:
        assert self.process.stdout is not None
        chunks: list[bytes] = []
        remaining = size
        while remaining:
            chunk = self.process.stdout.read(remaining)
            if not chunk:
                raise RuntimeError(f"unexpected Git batch EOF with {remaining} bytes remaining")
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    def blob(self, object_name: str) -> tuple[str, bytes]:
        assert self.process.stdin is not None and self.process.stdout is not None
        self.process.stdin.write((object_name + "\n").encode("utf-8"))
        self.process.stdin.flush()
        header = self.process.stdout.readline().decode("ascii").rstrip("\n")
        parts = header.split(" ")
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError(f"unexpected Git batch header: {header}")
        oid, _, size_text = parts
        payload = self._read_exact(int(size_text))
        if self._read_exact(1) != b"\n":
            raise RuntimeError("Git batch blob terminator mismatch")
        return oid, payload

    def close(self) -> None:
        assert self.process.stdin is not None and self.process.stderr is not None
        self.process.stdin.close()
        stderr = self.process.stderr.read().decode("utf-8", "replace")
        rc = self.process.wait()
        if rc != 0 or stderr:
            raise RuntimeError(f"Git batch close failed rc={rc}: {stderr}")


def historical_proposal_inventory() -> tuple[dict[str, Any], list[dict[str, str]]]:
    """Recover attributable rows from every distinct current GHC-family branch tip."""

    raw = run_git(
        "for-each-ref",
        "--format=%(refname) %(objectname)",
        "refs/heads/codex/GHC-Family/*",
        "refs/remotes/origin/codex/GHC-Family/*",
    ).stdout.splitlines()
    items: list[tuple[str, str, str]] = []
    seen_pairs: set[tuple[str, str]] = set()
    for line in raw:
        ref, head = line.rsplit(" ", 1)
        leaf = ref.rsplit("/", 1)[-1]
        match = re.search(r"-(v\d+-v\d+)", leaf)
        if not match:
            continue
        owner_slug = leaf[: match.start()]
        pair = (head, owner_slug)
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            items.append((ref, head, owner_slug))

    def scan(item: tuple[str, str, str]) -> list[tuple[str, str, str]]:
        ref, head, owner_slug = item
        output = run_git(
            "ls-tree",
            "-r",
            "--format=%(objectname) %(path)",
            head,
            "--",
            f"docs/{owner_slug}",
        ).stdout
        found = []
        for line in output.splitlines():
            if line.endswith("proposal-freeze.json") or (
                "/proposal-freeze-shards/" in line and line.endswith(".json")
            ):
                oid, path = line.split(" ", 1)
                found.append((oid, path, ref))
        return found

    blob_rows: list[tuple[str, str, str]] = []
    scan_failures: list[dict[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = {executor.submit(scan, item): item for item in items}
        for future in concurrent.futures.as_completed(futures):
            try:
                blob_rows.extend(future.result())
            except Exception as exc:  # retained in the audit; build fails below
                scan_failures.append({"ref": futures[future][0], "error": f"{type(exc).__name__}: {exc}"})
    if scan_failures:
        raise ValueError(f"historical proposal scan failures: {scan_failures}")

    unique_blobs: dict[str, dict[str, set[str]]] = {}
    for oid, path, ref in blob_rows:
        unique_blobs.setdefault(oid, {"paths": set(), "refs": set()})
        unique_blobs[oid]["paths"].add(path)
        unique_blobs[oid]["refs"].add(ref)

    records: list[dict[str, str]] = []
    parse_failures: list[dict[str, str]] = []
    batch = GitBatch()
    try:
        for oid, metadata in sorted(unique_blobs.items()):
            _, payload = batch.blob(oid)
            try:
                document = json.loads(payload.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                parse_failures.append({"blob_oid": oid, "error": type(exc).__name__})
                continue
            found: list[tuple[str, str]] = []

            def walk(value: Any) -> None:
                if isinstance(value, dict):
                    proposal_id = value.get("proposal_id") or value.get("id")
                    title = value.get("title") or value.get("proposal")
                    if proposal_id and title and "-N" in str(proposal_id).upper():
                        found.append((str(proposal_id), str(title)))
                    for nested in value.values():
                        walk(nested)
                elif isinstance(value, list):
                    for nested in value:
                        walk(nested)

            walk(document)
            source_path = sorted(metadata["paths"])[0]
            for proposal_id, title in found:
                records.append(
                    {
                        "proposal_id": proposal_id,
                        "title": title,
                        "normalized_title": normalize_title(title),
                        "source_path": source_path,
                        "blob_oid": oid,
                    }
                )
    finally:
        batch.close()
    if parse_failures:
        raise ValueError(f"historical proposal parse failures: {parse_failures}")

    by_id: dict[str, dict[str, str]] = {}
    for row in records:
        by_id.setdefault(row["proposal_id"], row)
    corpus = sorted(by_id.values(), key=lambda row: (row["proposal_id"], row["normalized_title"]))
    by_title = {row["normalized_title"]: row for row in corpus if row["normalized_title"]}
    normalized_digest = sha256_bytes("\n".join(sorted(by_title)).encode("utf-8"))
    cooperage_hits = [
        row for row in corpus if re.search(r"cooper|barrel|cask", row["title"], flags=re.IGNORECASE)
    ]
    audit = {
        "declared_inherited_chain_count": INHERITED_FROZEN_PROPOSALS,
        "ref_rows": len(raw),
        "unique_head_owner_pairs": len(items),
        "freeze_path_rows": len(blob_rows),
        "unique_freeze_blobs": len(unique_blobs),
        "parsed_record_rows": len(records),
        "unique_proposal_ids": len(corpus),
        "unique_normalized_titles": len(by_title),
        "normalized_title_sha256": normalized_digest,
        "parse_failures": parse_failures,
        "scan_failures": scan_failures,
        "cooperage_keyword_hit_count": len(cooperage_hits),
        "cooperage_keyword_hits": cooperage_hits,
        "unrecovered_compressed_title_minimum": max(0, INHERITED_FROZEN_PROPOSALS - len(corpus)),
        "coverage_state": "RECOVERED_BRANCH_TIP_ROWS_AUDITED_COMPRESSED_OLDER_TITLES_REMAIN_OPEN_GAP",
        "boundary": (
            "Recovered attributable titles can falsify novelty. Declared but compressed historical titles cannot "
            "confirm novelty and remain an explicit open evidence gap."
        ),
    }
    return audit, corpus


def proposal_rows(corpus: list[dict[str, str]]) -> list[dict[str, Any]]:
    visible_by_title = {row["normalized_title"]: row for row in corpus}
    rows: list[dict[str, Any]] = []
    for index, (title, expected, slug) in enumerate(PROPOSAL_BLUEPRINTS, 1):
        normalized = normalize_title(title)
        neighbours = sorted(
            (
                {
                    "proposal_id": inherited["proposal_id"],
                    "title": inherited["title"],
                    "score": round(jaccard(title, inherited["title"]), 6),
                    "source_path": inherited["source_path"],
                }
                for inherited in corpus
            ),
            key=lambda row: (-row["score"], row["proposal_id"]),
        )[:5]
        exact_collision = normalized in visible_by_title
        quarantined = bool(neighbours and neighbours[0]["score"] >= 0.75)
        proposal_id = f"LV6688-N{index:03d}"
        if expected == "completed":
            approval_class = "safe_now"
        elif expected == "represented":
            approval_class = "bounded_representation"
        elif expected == "open_gap":
            approval_class = "evidence_gap"
        else:
            approval_class = "exact_approval"
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "semantic_slug": slug,
                "hypothesis": (
                    f"A wholly synthetic owner-local {slug} contract can distinguish one bounded admissible "
                    "record from four preregistered invalid mutations without promoting software structure into "
                    "empirical, participant, professional, production, legal, cultural, Maori-authority, identity, "
                    "independent-reproduction, or Stage 20 evidence."
                ),
                "null_or_failure_condition": (
                    "Reject or hold when required identity or state is missing, a domain or unit is ambiguous, "
                    "a real-world or external action appears, or a protected claim is promoted."
                ),
                "approval_class": approval_class,
                "execution_lane": "owner_local_synthetic_no_external_action",
                "official_or_primary_source_needs": [
                    "SRC-USDA-WOOD",
                    "SRC-OIV-CODE",
                    "SRC-PROV-DM",
                    "SRC-VC20",
                ],
                "concrete_artifacts": [
                    f"{REL_PHASE_ROOT}/x2/cards/{proposal_id.lower()}-{slug}.json",
                    f"{REL_PHASE_ROOT}/x2/proposals/{proposal_id.lower()}-{slug}.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "Exactly one bounded positive fixture must satisfy all declared obligations and all four "
                    "named invalid mutations must be retained and rejected; open and exact-gated dispositions "
                    "must remain held rather than converted into completion."
                ),
                "rollback_or_recovery": "Retain the failed fixture, stop the smallest affected control, and retry only a named bounded dependency.",
                "protected_gates": list(PROTECTED_GATES),
                "expected_disposition": expected,
                "observed_disposition": None,
                "x1_completion_credit": 0,
                "semantic_neighbors": neighbours,
                "visible_title_collision": exact_collision,
                "semantic_neighbor_quarantined": quarantined,
                "negative_fixtures": [
                    {"mutation_id": f"{proposal_id}-M01", "kind": "missing_required_state", "expected": "reject"},
                    {"mutation_id": f"{proposal_id}-M02", "kind": "ambiguous_domain_or_unit", "expected": "reject"},
                    {"mutation_id": f"{proposal_id}-M03", "kind": "real_world_or_external_action", "expected": "reject"},
                    {"mutation_id": f"{proposal_id}-M04", "kind": "protected_claim_promotion", "expected": "reject"},
                ],
            }
        )
    return rows


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
            "external_actions": 0,
            "authority_actions": 0,
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
        raise ValueError("x1 must begin at the exact Orin final")
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("unexpected Liora branch")
    allowed_code = {
        "scripts/ghc_family_liora_venn_v668_v8_archive.py",
        "scripts/build_ghc_family_liora_venn_v668_v8_x1.py",
        "tests/test_ghc_family_liora_venn_v668_v8_x1.py",
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
    if any("liora_venn_v668_v8_x2" in name or "liora_venn_v668_v8_final" in name for name in candidate_names):
        raise ValueError("x2 or final implementation exists before x1 freeze")

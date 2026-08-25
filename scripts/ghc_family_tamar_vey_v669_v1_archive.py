#!/usr/bin/env python3
"""Frozen declarations and bounded archive helpers for Tamar Vey v669-v1."""

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
OWNER = "Tamar Vey"
PRONOUNS = "she/they"
RELATIONAL_ROLE = "relational evidence-and-recovery steward"
RELATIONAL_HOPE = (
    "Keep every claim, abstention, correction, and handoff inspectable and safely retractable."
)
PHASE = "v669-v1"
REL_PHASE_ROOT = "docs/tamar-vey/v669-v1"
PHASE_ROOT = ROOT / REL_PHASE_ROOT
BRANCH = "codex/GHC-Family/tamar-vey-v669-v1-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v668-v8-full-tools"
SOURCE_START = "20053ae8166d070fcc8e7d13235e595de7404b6f"
SOURCE_X1 = "aa5a4c6aef9f6d6a3026e184fd7f64443fab5fe8"
SOURCE_EVIDENCE = "f9862197313a91fa6d432e826ecbb81950719821"
SOURCE_FINAL = "bb475c084da39512dfa0811a8520a40fd3d4c84a"
SOURCE_CANONICAL_RECEIPT_SHA256 = "c306ff5fb1d26692db5b9588754c3a5ac5490b408f32bd46d39b83467faf09c9"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "c6d3c19823a1b6609c14b94e680a11919b4b64eed1dab4134f824eaae1a0efa4"
SOURCE_TERMINAL_STATUS = "VALID_EXACT_FINAL_CANONICAL_SUCCESS_ONCE_NO_REPLAY"
INHERITED_FROZEN_PROPOSALS = 4910
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Tamar Vey, she/they, the relational role and hope, sibling or family language, continuity language, "
    "Freed ID, CBR, GHC Family, and Trinity Mandala language are working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, scientific or operational authority, legal or cultural authority, affected-party "
    "authority, or Māori authority."
)
EVIDENCE_BOUNDARY = (
    "Every upholstered item, frame, rail, leg, arm, spring, webbing span, padding layer, cover panel, fastener, "
    "tool, material, batch, work order, measurement, person, studio, review, release, identity event, and "
    "decision is synthetic. Official and primary-source vocabulary plus same-owner local software checks are "
    "not upholstery evidence, object or material evidence, professional evaluation, workplace or fire "
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
    "Māori-authority",
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
    "effective_negatives": 30342,
    "methods": 16608,
    "failed_witnesses": 2323,
    "passing_witnesses": 3150,
    "open_gaps": 223,
    "exact_gates": 218,
    "source_repository_seal": {
        "effective_negatives": 30342,
        "methods": 16608,
        "failed_witnesses": 2323,
        "passing_witnesses": 3150,
        "open_gaps": 223,
        "exact_gates": 218,
    },
    "external_retained_negative": None,
    "boundary": (
        "Liora's sealed successful canonical invocation remains source evidence only and is never replayed or "
        "converted into Tamar completion credit."
    ),
}

PRIMARY_PILLAR = "THOS Body"
PRACTICES = (
    "wholly synthetic upholstery intake and component-topology documentation",
    "wholly synthetic upholstery work-order correction, workload control, and shift handover",
    "wholly synthetic accessible upholstery-record review with professional and affected-user evaluation reserved",
)

SOURCE_LEDGER = [
    {
        "source_id": "SRC-CCI-FURNITURE",
        "title": "Furniture, wooden objects and basketry",
        "url": "https://www.canada.ca/en/conservation-institute/services/care-objects/furniture-wooden-objects-basketry.html",
        "status": "official Canadian Conservation Institute resource inspected 25 August 2026",
        "use": "furniture component, deterioration, handling-vacancy, preservation, and professional-referral vocabulary only",
        "credit_boundary": "no object identification, condition assessment, handling, treatment, fitness, authenticity, or professional credit",
    },
    {
        "source_id": "SRC-NIOSH-MANUFACTURING",
        "title": "NIOSH Manufacturing Program",
        "url": "https://www.cdc.gov/niosh/research-programs/portfolio/manufacturing.html",
        "status": "official NIOSH manufacturing research-program page inspected 25 August 2026",
        "use": "furniture-manufacturing hazard, exposure, ergonomics, workload, and prevention-vacancy vocabulary only",
        "credit_boundary": "no workplace measurement, ergonomic assessment, safety release, compliance, or professional credit",
    },
    {
        "source_id": "SRC-SI-OPEN",
        "title": "Smithsonian Open Access",
        "url": "https://www.si.edu/openaccess",
        "status": "official Smithsonian Open Access page inspected 25 August 2026",
        "use": "zero-call furniture collection adapter requirements and provenance-vacancy vocabulary only",
        "credit_boundary": "zero API keys, requests, downloads, rows, media, object identifications, rights conclusions, or collection claims",
    },
    {
        "source_id": "SRC-VC20",
        "title": "Verifiable Credentials Data Model v2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation 15 May 2025; current Recommendation inspected 25 August 2026",
        "use": "issuer, holder, verifier, status, evidence, privacy, accessibility, and trust-vacancy vocabulary only",
        "credit_boundary": "zero real keys or proofs; no issuance, verification, status, interoperability, trust, or production identity credit",
    },
    {
        "source_id": "SRC-NIST-800-63-4",
        "title": "NIST SP 800-63-4 Digital Identity Guidelines",
        "url": "https://pages.nist.gov/800-63-4/",
        "status": "official NIST SP 800-63-4 published August 2025 and inspected 25 August 2026",
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
        "credit_boundary": "manual, browser-diverse, assistive-technology, cognitive, Māori-language, and affected-user evaluation reserved",
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
        "title": "Te Mana Raraunga Principles of Māori Data Sovereignty",
        "url": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf",
        "status": "primary Te Mana Raraunga resource and current resource page inspected 25 August 2026",
        "use": "authority-vacancy, collective-benefit, control, jurisdiction, responsibility, and ethics stop conditions only",
        "credit_boundary": "citation creates no cultural legitimacy, tikanga decision, Māori data-governance mandate, or Māori authority",
    },
]

PROPOSAL_BLUEPRINTS: list[tuple[str, str, str]] = [
    ("synthetic upholstered-item frame rail leg arm seat back cushion spring webbing and cover identity lattice with conflation refusal", "completed", "upholstery-component-identity"),
    ("frame joinery corner-block dowel screw and adhesive association graph with construction and condition vacancies", "completed", "frame-joinery-vacancy"),
    ("spring array row column tie and edge-support topology tribunal with no installation or tensioning instruction", "completed", "spring-array-topology"),
    ("webbing warp weft anchor span and overlap grid with duplicate-position quarantine and zero fastening action", "completed", "webbing-grid-topology"),
    ("padding layer order interface thickness-unit and compression-claim ledger with measurement vacancy", "completed", "padding-layer-ledger"),
    ("cover panel grain direction seam allowance welt and motif-alignment graph with cutting and sewing veto", "completed", "cover-panel-topology"),
    ("zipper tack staple nail cord and closure-state vocabulary board with ambiguity and actuation refusal", "completed", "closure-state-vocabulary"),
    ("cushion core envelope fill insert and orientation register with composition and fitness abstention", "completed", "cushion-core-vacancy"),
    ("textile leather foam fibre timber metal and adhesive material-claim vacancy matrix with authenticity refusal", "completed", "material-claim-vacancy"),
    ("colour pattern texture sheen and fading assertion ledger separating description from calibrated observation", "completed", "appearance-claim-firewall"),
    ("synthetic dimension profile with decimal-string length and angle units plus conversion and measurement refusal", "completed", "upholstery-dimension-units"),
    ("surface wear tear abrasion deformation looseness staining and odour vocabulary board without diagnosis", "completed", "condition-vocabulary"),
    ("pest mould residue allergen and contamination cue register with quarantine state and no hazard determination", "completed", "contamination-cue-register"),
    ("upholstery action proposal approval execution observation correction and release state machine with every real action forbidden", "completed", "upholstery-state-machine"),
    ("synthetic needle awl regulator stretcher remover stapler and fixture identity register with competence vacancy", "completed", "upholstery-tool-register"),
    ("append-only upholstery repair-docket fork with effective time recording time superseded-field mask conflict branch and signoff vacancy", "completed", "repair-docket-fork"),
    ("synthetic upholstered-item custody location transfer return and withdrawal graph with ownership noninference", "completed", "upholstery-custody-graph"),
    ("frame cover padding spring fastener and finish batch provenance graph with supplier and chain-of-custody vacancies", "completed", "material-batch-provenance"),
    ("UTF-8 stable bitemporal upholstery dossier hash-domain register with numeric-string coercion refusal", "completed", "upholstery-hash-domain"),
    ("unlinkable surrogate upholstery docket station review-cohort and turnover alias budget with correlation alarms", "completed", "upholstery-alias-budget"),
    ("accessible upholstery-topology table with caption scoped headers text holds linear order and print fallback", "completed", "accessible-upholstery-table"),
    ("bounded four-party upholstery issue escrow with owner vacancy timeout capacity token dual-readback digest and unresolved state", "completed", "upholstery-issue-escrow"),
    ("official-source assertion ledger separating vocabulary from object observation treatment instruction and release", "completed", "source-assertion-firewall"),
    ("CBR object-record challenge ladder for least disclosure correction evidence appeal deadline remedy vacancy and decision-authority abstention", "completed", "cbr-challenge-ladder"),
    ("Freed ID zero-key pseudonymous upholstery dossier capability envelope for disclosure scope withdrawal contest expiry and verifier vacancy", "completed", "freed-id-capability-envelope"),
    ("THOS synthetic upholstery dependency DAG with refusal edges work-cap token correction echo and handover vacancy", "completed", "thos-upholstery-dag"),
    ("GMUT covariant phase-space presymplectic-current boundary-flux gauge-degeneracy and EFT obligation board with zero solved equation", "completed", "gmut-presymplectic-obligations"),
    ("compressed-air staple sharp-tool dust adhesive solvent fire ergonomics and stored-energy hold schema with no safety release", "completed", "upholstery-hazard-holds"),
    ("upholstery intake and component-documentation practice lens with zero craft material or condition competence inference", "represented", "upholstery-practice"),
    ("synthetic studio correction workload and shift-handover practice lens with zero object handling", "represented", "studio-handover-practice"),
    ("structural upholstery dossier navigation error-summary text-status focus-order print-view practice with human evaluation reserved", "represented", "accessible-dossier-practice"),
    ("THOS paired synthetic omission-detection board for upholstery dependencies with symmetric budgets abstention scoring zero people and no effectiveness estimate", "represented", "thos-omission-proxy"),
    ("Freed ID nonproduction upholstery dossier trust-surface map for issuer verifier status recovery and correlation vacancies", "represented", "freed-id-trust-surface"),
    ("CBR upholstery rights remedy heritage affected-party legitimacy and authority-vacancy lens", "represented", "cbr-authority-boundary"),
    ("typed scalar-tensor upholstery stress analogy card separating bookkeeping from physical prediction", "represented", "gmut-upholstery-analogy"),
    ("material deformation stored energy and damping versus agency justice mind and authority nonconversion ledger", "represented", "material-psyche-nonconversion"),
    ("Smithsonian furniture Open Access zero-call adapter with zero key query download row media object or rights claim", "open_gap", "smithsonian-furniture-zero-call"),
    ("real upholsterer material workplace accessibility language cultural-care and affected-party evaluation", "open_gap", "human-evaluation-gap"),
    ("competent upholstery release object safety custody ownership legal cultural and Māori-authority decision gate", "exact_gate", "upholstery-authority-gate"),
    ("Stage 20 conjunctive nonpromotion tribunal joining real-data participant safety identity-lifecycle accessibility legal-cultural and Māori-authority witnesses without substitution", "exact_gate", "stage20-nonpromotion-tribunal"),
]

SKILL_NAMES = [
    "ghc-family-upholstery-component-identity",
    "ghc-family-upholstery-frame-joinery-vacancy",
    "ghc-family-upholstery-spring-array",
    "ghc-family-upholstery-webbing-grid",
    "ghc-family-upholstery-padding-ledger",
    "ghc-family-upholstery-cover-panel",
    "ghc-family-upholstery-closure-state",
    "ghc-family-upholstery-cushion-vacancy",
    "ghc-family-upholstery-material-vacancy",
    "ghc-family-upholstery-condition-vocabulary",
    "ghc-family-upholstery-provenance",
    "ghc-family-upholstery-correction-chain",
    "ghc-family-upholstery-custody-vacancy",
    "ghc-family-upholstery-hash-domain",
    "ghc-family-upholstery-pseudonyms",
    "ghc-family-upholstery-accessible-report",
    "ghc-family-upholstery-workload-handover",
    "ghc-family-upholstery-hazard-holds",
    "ghc-family-upholstery-identity-vacancy",
    "ghc-family-upholstery-authority-vacancy",
]

RUNNER_NAMES = [
    "ghc_family_upholstery_identity_runner",
    "ghc_family_upholstery_frame_runner",
    "ghc_family_upholstery_spring_webbing_runner",
    "ghc_family_upholstery_material_vacancy_runner",
    "ghc_family_upholstery_condition_runner",
    "ghc_family_upholstery_provenance_runner",
    "ghc_family_upholstery_correction_runner",
    "ghc_family_upholstery_accessibility_runner",
    "ghc_family_upholstery_identity_vacancy_runner",
    "ghc_family_upholstery_authority_firewall_runner",
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
    upholstery_hits = [
        row for row in corpus if re.search(r"upholster", row["title"], flags=re.IGNORECASE)
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
        "upholstery_keyword_hit_count": len(upholstery_hits),
        "upholstery_keyword_hits": upholstery_hits,
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
        proposal_id = f"TV6691-N{index:03d}"
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
                    "empirical, participant, professional, production, legal, cultural, Māori-authority, identity, "
                    "independent-reproduction, or Stage 20 evidence."
                ),
                "null_or_failure_condition": (
                    "Reject or hold when required identity or state is missing, a domain or unit is ambiguous, "
                    "a real-world or external action appears, or a protected claim is promoted."
                ),
                "approval_class": approval_class,
                "execution_lane": "owner_local_synthetic_no_external_action",
                "official_or_primary_source_needs": [
                    "SRC-CCI-FURNITURE",
                    "SRC-NIOSH-MANUFACTURING",
                    "SRC-SI-OPEN",
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
        raise ValueError("x1 must begin at the exact Liora final")
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("unexpected Tamar branch")
    allowed_code = {
        "scripts/ghc_family_tamar_vey_v669_v1_archive.py",
        "scripts/build_ghc_family_tamar_vey_v669_v1_x1.py",
        "scripts/validate_ghc_family_tamar_vey_v669_v1_x1.py",
        "tests/test_ghc_family_tamar_vey_v669_v1_x1.py",
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
    if any("tamar_vey_v669_v1_x2" in name or "tamar_vey_v669_v1_final" in name for name in candidate_names):
        raise ValueError("x2 or final implementation exists before x1 freeze")

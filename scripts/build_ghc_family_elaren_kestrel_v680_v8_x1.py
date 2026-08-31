from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elaren-kestrel" / "v680-v8"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Elaren Kestrel"
PHASE = "v680-v8"
BRANCH = "codex/GHC-Family/elaren-kestrel-v680-v8-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v680-v7-full-tools"
SOURCE = "5602a53f6ffec15093a07a2e023b7e5f8619cf54"
SOURCE_X1 = "e94866a1adf4b5b038479c12bc5354ead6f7c249"
SOURCE_EVIDENCE = "1ee1a87ff80ad3b2813a9b6cfb29b3dff38c4ba1"
SOURCE_PARENT = "2522f0ff596b66f57f187f8073d498c692a85712"
DECLARED_CHAIN_BEFORE = 9650
DECLARED_CHAIN_AFTER = 9710
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
WRITTEN: list[str] = []


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jaccard(left: str, right: str) -> float:
    left_tokens = set(re.findall(r"[a-z0-9]+", left.casefold()))
    right_tokens = set(re.findall(r"[a-z0-9]+", right.casefold()))
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


PROPOSAL_TITLES = [
    "Synthetic historic magic-lantern-slide item record and physical object non-equivalence",
    "Carrier-glass plate and cover-glass relation with material-identification hold",
    "Image-layer binder emulsion and colourant tokens with analytical-evidence vacancy",
    "Binding-tape edge-paper mount and label topology without construction inference",
    "Slide-format dimension placeholder with zero real measurement",
    "Projection-face orientation and viewing-direction declaration without apparatus operation",
    "Maker publisher distributor and retailer mark placeholder with attribution uncertainty",
    "Caption and title transcription surrogate with language-authority vacancy",
    "Lecture-series sequence and item-number graph with performance-history nonclaim",
    "Hand-coloured printed and photographic technique tokens with process-inference refusal",
    "Positive negative opaque-mask and transparency-state placeholders without image diagnosis",
    "Crack flake delamination loss and abrasion tokens with condition-diagnosis hold",
    "Binding-tape embrittlement and adhesive-residue relation with treatment-attribution uncertainty",
    "Broken-glass edge state packet with handling and injury-safety gate",
    "Storage enclosure cabinet and sequence-position surrogate with real-location vacancy",
    "Projection-apparatus compatibility pointer with every operation withheld",
    "Heat light and projection-duration placeholders with zero exposure readings",
    "Lecture programme ordering graph with speaker and audience identity vacancy",
    "Lantern-slide custody ownership and provenance record with legal-title non-equivalence",
    "Structurally accessible carrier-image-sequence companion with manual evaluation reserved",
    "Synthetic lantern-slide condition-map revision graph and observed-condition non-equivalence",
    "Digital capture derivative and media-facet index with rights and provenance firewall",
    "Synthetic capture-setup declaration for lantern-slide surrogates with every calibration and metric field vacant",
    "Lantern-slide enclosure-climate placeholder using absent logger channels and no preservation inference",
    "Unwitnessed slide-change timeline with causal attribution prohibited",
    "Prior binding repair and cover-glass intervention lineage with attribution uncertainty",
    "Glass-surface alteration and image-layer change relation with material-assessment vacancy",
    "Retain rehouse duplicate and restrict option board without treatment recommendation",
    "Rehousing enclosure and support surrogate with every physical action withheld",
    "Photographic-collection intake and work-order proxy with real-commission non-equivalence",
    "Image-layer analysis request placeholder with sampling-authority hold",
    "Broken glass unknown coating and projection-heat packet retained for competent safety assessment",
    "Surface-cleaning proposal with image-layer solubility and abrasion exact gate",
    "Binding repair consolidation and cover-glass replacement proposal with compatibility exact hold",
    "Digitization and access-copy alternative board without preservation-performance claim",
    "Non-destructive surrogate revision braid linking lantern-slide media derivatives and correction events",
    "Slide access and care decision matrix requiring named competency vacancies and rejecting surrogate approval",
    "Rejected lantern-slide intervention mutation quarantine with recurrence guard",
    "Lantern-slide review handover lease with unresolved-workload stop",
    "Text-first lecture-sequence navigator reserving keyboard zoom and assistive-user review",
    "Synthetic photographic-collection dossier and real catalogue-record non-equivalence",
    "Pseudonymous collection-steward function token minimizing disclosure and forbidding identity resolution",
    "Consent custody access and depicted-person notice envelope with affected-party vacancy",
    "Append-only slide-record correction ledger with status-withdrawal marker and zero live credential operation",
    "Lantern-slide media-permissions docket reserving copying display licensing and publication decisions",
    "Depicted person place event and community association placeholder with interpretation hold",
    "Community-significance and restricted-knowledge vacancy docket with no interpretive substitution",
    "Multilingual caption and title label with linguistic-authority vacancy",
    "Te reo Maori label and Maori data-stewardship reservation with zero delegated authority",
    "THOS bounded slide-description work queue with fail-closed interruption ledger and zero field operation",
    "THOS lantern-slide review workload signal without health or wellbeing inference",
    "GMUT typed carrier-image-sequence topology board with empirical-physics firewall",
    "GMUT surrogate radiant-load symbol table for glass-image carriers with no sampled quantities",
    "Synthetic Freed ID lantern-slide lineage node set paired with unresolved CBR correction-and-remedy holders",
    "Zero-call magic-lantern-slide vocabulary adapter with unresolved source-version gap",
    "Photographic-material catalogue crosswalk with unresolved live-version provenance gap",
    "Lantern-slide sequence-map manual browser assistive cognitive Maori-language and affected-user evaluation gap",
    "Real handling cleaning repair projection and broken-glass safety authority gate",
    "Lantern-slide ownership custody rights privacy cultural heritage and Maori-authority gate",
    "Terminal reservation separating software receipts from physics proof production identity external replication and Stage-20 standing",
]


MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real participants owners custodians conservators lantern slides glass plates images collections apparatus measurements and observations",
    "empirical GMUT likelihoods constraints predictions forces and confirmation",
    "professional photographic-material conservation handling sampling cleaning consolidation rehousing broken-glass projection heat and workplace safety authority",
    "production identity issuance resolution status revocation interoperability and trust governance",
    "ownership custody image reproduction publication privacy remedy legal cultural heritage affected-party and Maori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood proof canon and Stage 20",
]


def disposition(index: int) -> str:
    if index <= 42:
        return "completed"
    if index <= 54:
        return "represented"
    if index <= 57:
        return "open_gap"
    return "exact_gate"


def approval_class(index: int) -> str:
    if index <= 42:
        return "safe_now"
    if index <= 57:
        return "bounded_candidate"
    return "exact_approval"


def execution_lane(index: int) -> str:
    if index <= 42:
        return "owner_local_synthetic_zero_row"
    if index <= 54:
        return "represented_external_evidence_vacancy"
    if index <= 57:
        return "open_external_evidence_gap"
    return "unexecuted_competent_authority_gate"


def source_needs(index: int) -> list[str]:
    if index <= 20:
        return ["CCI-GLASS-PLATE", "LOC-LANTERN-SLIDES", "NIST-SI", "W3C-PROV-DM", "RFC8785"]
    if index <= 40:
        return ["CCI-PHOTO-CARE", "LOC-GENTHE-LANTERN", "UKNA-MIXED-COLLECTIONS", "W3C-PROV-DM", "W3C-WCAG22"]
    if index <= 54:
        return ["LOC-LANTERN-SLIDES", "NZ-PRIVACY", "W3C-PROV-DM", "W3C-VC-DM-2.0", "TMR-MDS-PRINCIPLES"]
    if index <= 57:
        return ["CCI-GLASS-PLATE", "LOC-LANTERN-SLIDES", "W3C-WCAG22"]
    if index == 58:
        return ["CCI-GLASS-PLATE", "CCI-PHOTO-CARE", "UKNA-MIXED-COLLECTIONS"]
    if index == 59:
        return ["LOC-LANTERN-SLIDES", "NZ-PRIVACY", "TMR-MDS-PRINCIPLES"]
    return ["NIST-SI", "W3C-VC-DM-2.0", "TMR-MDS-PRINCIPLES"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"EL6808-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/elaren-kestrel/v680-v8/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/elaren-kestrel/v680-v8/x2/mutations.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": disposition(index),
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded positive witness, all five invalid mutations "
                    "are rejected, and no empirical, professional, production, legal, cultural, affected-party, "
                    "Maori-authority, or Stage 20 claim is promoted."
                ),
                "hypothesis": (
                    f"A wholly synthetic zero-row contract for {title.casefold()} can preserve the named state "
                    "distinction and reject its preregistered counterexamples within owner-local scope."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, its bounded positive "
                    "structure is rejected, a real-world state is inferred, or any protected gate is promoted."
                ),
                "official_or_primary_source_needs": source_needs(index),
                "preregistered_rejecting_mutations": [
                    {
                        "expected_result": "rejected_zero_credit",
                        "mutation_id": f"{proposal_id}-M{mutation_index:02d}",
                        "mutation_type": mutation_type,
                    }
                    for mutation_index, mutation_type in enumerate(MUTATION_TYPES, start=1)
                ],
                "proposal_id": proposal_id,
                "protected_gates": PROTECTED_GATES,
                "rollback_or_recovery": (
                    f"Quarantine only the {proposal_id} witness, retain the failed receipt at zero credit, "
                    "and regenerate from this immutable planning contract."
                ),
                "title": title,
            }
        )
    return rows


def iter_proposal_records(value: Any) -> Iterable[dict[str, str]]:
    if isinstance(value, dict):
        proposal_id = value.get("proposal_id")
        title = value.get("title")
        if isinstance(proposal_id, str) and isinstance(title, str):
            yield {"proposal_id": proposal_id, "title": title}
        for child in value.values():
            yield from iter_proposal_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_proposal_records(child)


def batch_blobs(tree: str, paths: list[str]) -> Iterable[tuple[str, bytes]]:
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    try:
        for path in paths:
            process.stdin.write(f"{tree}:{path}\n".encode())
            process.stdin.flush()
            header = process.stdout.readline().decode("utf-8", errors="replace").rstrip("\n")
            if header.endswith(" missing"):
                continue
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
            size = int(parts[2])
            data = process.stdout.read(size)
            if process.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing cat-file separator for {path}")
            yield path, data
    finally:
        process.stdin.close()
        process.terminate()
        process.wait(timeout=10)


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    result = git("grep", "-l", "-I", '"proposal_id"', SOURCE, "--", "*.json", check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr)
    raw_paths = sorted(set(filter(None, result.stdout.splitlines())))
    prefix = SOURCE + ":"
    paths = [path.removeprefix(prefix) for path in raw_paths]
    parsed = 0
    parse_failures: list[dict[str, str]] = []
    inherited: list[dict[str, str]] = []
    for path, data in batch_blobs(SOURCE, paths):
        try:
            document = json.loads(data.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_failures.append({"error": type(exc).__name__, "path": path})
            continue
        parsed += 1
        for record in iter_proposal_records(document):
            inherited.append({"path": path, **record})
    if not paths or not parsed or not inherited:
        raise RuntimeError("proposal audit must parse nonzero exact-source paths and id-title records")

    inherited_titles = {record["title"] for record in inherited}
    collisions: list[str] = []
    neighbors: list[dict[str, Any]] = []
    for proposal in new_records:
        title = proposal["title"]
        if title in inherited_titles:
            collisions.append(title)
        best = max(inherited, key=lambda record: jaccard(title, record["title"]))
        score = jaccard(title, best["title"])
        neighbors.append(
            {
                "best_inherited_neighbor": best,
                "proposal_id": proposal["proposal_id"],
                "quarantined": score >= 0.78,
                "title": title,
                "token_jaccard": round(score, 6),
            }
        )
    quarantined = [row for row in neighbors if row["quarantined"]]
    if collisions or quarantined:
        raise RuntimeError(
            "proposal novelty quarantine required: "
            + json.dumps({"exact": collisions, "neighbors": quarantined}, ensure_ascii=False)
        )
    return {
        "audit_scope": {
            "claim": "bounded all-reachable exact-source proposal audit; no universal 9650-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_9650_row_materialization_claimed": False,
        },
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "exact_title_collisions": collisions,
        "maximum_neighbor_score": max(row["token_jaccard"] for row in neighbors),
        "neighbor_reviews": neighbors,
        "new_proposal_count": len(new_records),
        "owner": OWNER,
        "phase": PHASE,
        "quarantine_threshold_token_jaccard": 0.78,
        "quarantined_neighbors": quarantined,
        "schema": "ghc.family.proposal-chain-audit.v680.v8.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Elaren owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"EL6808-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must start at the immutable Eiren final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Elaren owner branch")
    if (BASE / "x2").exists():
        raise RuntimeError("x2 material is forbidden during planning-only x1")

    proposal_records = proposals()
    if len(proposal_records) != 60:
        raise RuntimeError("exactly sixty proposals are required")
    expected_counts = Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
    if Counter(row["expected_disposition"] for row in proposal_records) != expected_counts:
        raise RuntimeError("proposal disposition contract drift")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in proposal_records):
        raise RuntimeError("unknown outcome label")

    audit = proposal_chain_audit(proposal_records)
    source_ledger = json.loads(
        git("show", f"{SOURCE}:docs/eiren-kestrel/v680-v7/x1/new-proposal-freeze.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Eiren Kestrel",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in source_ledger["proposals"][-20:]
    ]

    startup_failures = [
        {
            "failure_id": "EL6808-ST-N001",
            "failed_witness": "A first baton-integrity comparison accidentally reused an older v675 hash against the current v680 path and reported a mismatch that the live activation never declared.",
            "initial_credit": 0,
            "recovery": "Reread the newest live activation, discard the stale historical hash as inapplicable, and verify the only v680 baton directly from its exact Git blob without rewriting it.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EL6808-ST-N002",
            "failed_witness": "A PowerShell startup inventory piped a foreach language statement directly and raised EmptyPipeElement before producing an attributable result.",
            "initial_credit": 0,
            "recovery": "Materialize bounded foreach output into an array before projection, preserving the parser failure at zero credit.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EL6808-ST-N003",
            "failed_witness": "The fresh worktree creation exceeded its reporting window while Git continued the one original read-tree operation.",
            "initial_credit": 0,
            "recovery": "Do not repeat creation; inspect the persisted branch, worktree, process ownership, index lock, materialization progress, and final clean state until the original operation completed.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EL6808-ST-N004",
            "failed_witness": "The first sparse-pattern write assumed .git was a directory, but the linked worktree uses a .git pointer file and the intended configuration write did not occur.",
            "initial_credit": 0,
            "recovery": "Resolve the actual linked-worktree Git directory from the pointer and use the documented sparse-checkout command only after the original index lock cleared.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EL6808-ST-N005",
            "failed_witness": "The inherited Eiren sparse pattern transiently materialized 2,251 files, exceeding the 2,000-file lane target before it could safely be replaced.",
            "initial_credit": 0,
            "recovery": "Wait for the owning read-tree process to release the index, then narrow to the exact twenty structural template files and prove a clean 21-file materialized lane including the .git pointer.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EL6808-ST-N006",
            "failed_witness": "A broad sixteen-term exact-source Git grep remained on its first term for many minutes and produced no attributable novelty result.",
            "initial_credit": 0,
            "recovery": "Stop only the owned read-only diagnostic and use this builder's bounded exact-source proposal ID/title audit, collision check, and 0.78 token-Jaccard quarantine.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EL6808-ST-N007",
            "failed_witness": "The first non-cone sparse command omitted leading slashes and emitted root-anchoring warnings even though the resulting exact file set was correct.",
            "initial_credit": 0,
            "recovery": "Inspect the materialized relative-path set, branch, head, and clean status directly; retain the warning and avoid a needless second sparse checkout when all twenty requested files and only the .git pointer were present.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EL6808-ST-N008",
            "failed_witness": "A monitoring-only process probe repeated the known PowerShell EmptyPipeElement form by piping a foreach language statement before materialization.",
            "initial_credit": 0,
            "recovery": "Retain the recurrence, assign the bounded process rows to an array before JSON projection, and keep the authoritative audit process untouched.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EL6808-ST-N009",
            "failed_witness": "The first unfrozen magic-lantern-slide proposal slate contained eight exact inherited titles and fifteen rows at or above the preregistered 0.78 token-Jaccard quarantine threshold.",
            "initial_credit": 0,
            "recovery": "Reject the unfrozen slate at zero novelty credit, replace only the quarantined titles with domain-specific contracts, and rerun the exact-source audit because the proposal target changed.",
            "recovery_credit": "target_changed_audit_only",
        },
    ]

    sources = {
        "authority_conferred": False,
        "checked_at_utc": "2026-09-01T03:35:00+12:00",
        "citations_are_observations": False,
        "entries": [
            {
                "source_id": "CCI-GLASS-PLATE",
                "status": "official_Canadian_Conservation_Institute_note_checked_2026-09-01",
                "title": "Care of Black-and-White Photographic Glass Plate Negatives - CCI Notes 16/2",
                "url": "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-black-white-photographic-negatives-glass-plate.html",
                "use": "glass support, image layer, handling, enclosure, deterioration, and professional-referral vocabulary only; no slide, material, condition, handling, treatment, or safety conclusion",
            },
            {
                "source_id": "CCI-PHOTO-CARE",
                "status": "official_Canadian_Conservation_Institute_guidance_checked_2026-09-01",
                "title": "Caring for photographic materials",
                "url": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/photographic-materials.html",
                "use": "photographic-material identification boundaries, environment, light, storage, handling, and specialist-care vocabulary only; no collection assessment or treatment result",
            },
            {
                "source_id": "LOC-LANTERN-SLIDES",
                "status": "official_Library_of_Congress_Thesaurus_record_checked_2026-09-01",
                "title": "Lantern slides",
                "url": "https://www.loc.gov/pictures/collection/tgm/item/tgm005803/",
                "use": "lantern-slide vocabulary and catalogue-term relationship only; no object identity, cataloguing authority, or rights conclusion",
            },
            {
                "source_id": "LOC-GENTHE-LANTERN",
                "status": "official_Library_of_Congress_preservation_note_checked_2026-09-01",
                "title": "Deterioration and Preservation of Negatives, Autochromes and Lantern Slides",
                "url": "https://www.loc.gov/pictures/collection/agc/preservation.html",
                "use": "collection-specific deterioration and preservation vocabulary only; no transfer of findings to a synthetic or real slide and no treatment recommendation",
            },
            {
                "source_id": "UKNA-MIXED-COLLECTIONS",
                "status": "official_UK_National_Archives_guidance_checked_2026-09-01",
                "title": "Managing mixed collections guidance",
                "url": "https://cdn.nationalarchives.gov.uk/documents/archives/managing-mixed-collections-guidance.pdf",
                "use": "mixed-media collection, separation, packaging, access, and escalation vocabulary only; no collection decision, handling instruction, or professional authority",
            },
            {
                "source_id": "NIST-SI",
                "status": "official_NIST_SI_page_checked_2026-09-01",
                "title": "International System of Units (SI)",
                "url": "https://www.nist.gov/programs-projects/international-system-units-si",
                "use": "quantity, unit, dimension, and reporting vocabulary only; zero real measurement or calibration claim",
            },
            {
                "source_id": "NZ-PRIVACY",
                "status": "official_NZ_Privacy_Commissioner_principles_page_checked_2026-09-01",
                "title": "Privacy Act 2020 information privacy principles",
                "url": "https://www.privacy.org.nz/privacy-principles/",
                "use": "minimum collection, storage, access, correction, use, disclosure, retention, and unique-identifier reservation vocabulary only; no legal or compliance conclusion",
            },
            {
                "source_id": "W3C-PROV-DM",
                "status": "W3C_Recommendation_checked_2026-09-01",
                "title": "PROV-DM: The PROV Data Model",
                "url": "https://www.w3.org/TR/prov-dm/",
                "use": "entity, activity, agent, revision, derivation, collection, and provenance vocabulary only",
            },
            {
                "source_id": "W3C-WCAG22",
                "status": "W3C_Recommendation_checked_2026-09-01",
                "title": "Web Content Accessibility Guidelines 2.2",
                "url": "https://www.w3.org/TR/WCAG22/",
                "use": "structural accessibility vocabulary with manual, assistive-technology, cognitive, Maori-language, and affected-user evaluation reserved",
            },
            {
                "source_id": "W3C-VC-DM-2.0",
                "status": "W3C_Recommendation_checked_2026-09-01",
                "title": "Verifiable Credentials Data Model v2.0",
                "url": "https://www.w3.org/TR/vc-data-model-2.0/",
                "use": "synthetic credential vocabulary and production-identity refusal conditions only",
            },
            {
                "source_id": "RFC8785",
                "status": "RFC_stable_checked_2026-09-01",
                "title": "JSON Canonicalization Scheme",
                "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
                "use": "deterministic synthetic receipt and digest-domain vocabulary only",
            },
            {
                "source_id": "TMR-MDS-PRINCIPLES",
                "status": "authority_boundary_context_only_checked_2026-09-01",
                "title": "Principles of Maori Data Sovereignty",
                "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                "use": "Maori data-governance vacancy and noncompensation boundary only; never delegated Maori authority",
            },
        ],
        "external_source_reads": 12,
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v680.v8.x1",
    }

    skill_slugs = [
        "lantern-slide-object-boundary",
        "carrier-image-layer-separation",
        "slide-sequence-address-graph",
        "maker-publisher-attribution-hold",
        "condition-nondiagnosis",
        "caption-language-authority-hold",
        "projection-operation-firewall",
        "slide-condition-map-lineage",
        "intervention-quorum-guard",
        "broken-glass-safety-hold",
        "physical-action-firewall",
        "photographic-dossier-state-machine",
        "media-provenance-braid",
        "image-rights-vacancy",
        "minimum-disclosure",
        "accessible-sequence-companion",
        "workload-control",
        "handover-lease",
        "digest-domain",
        "stage20-refusal",
    ]
    portfolio = {
        "blocked": task_records("BLOCK", 10, "blocked"),
        "caps_are_ceilings": True,
        "commit_cap": 3,
        "document_word_cap": 100000,
        "exact_approval": task_records("APPROVAL", 20, "exact_approval"),
        "materialized_file_stop": 2000,
        "owner": OWNER,
        "owner_candidates": task_records("CAND", 80, "bounded_candidate"),
        "owner_clean_fix_refine": task_records("CFR", 100, "clean_fix_refine"),
        "owner_practice_lenses": [
            "wholly synthetic historic magic-lantern-slide carrier image and sequence documentation analyst lens for object separation, attribution vacancy, correction, accessibility, workload, and handover",
            "wholly synthetic lantern-slide condition-map and intervention-lineage steward lens for revision, mutation rejection, broken-glass and projection-operation holds, workload, and handover",
            "wholly synthetic photographic-collection dossier provenance steward lens for custody, minimum disclosure, image-rights vacancy, correction, remedy, and authority holds",
        ],
        "owner_runner_ideas": [
            {"runner": f"ghc_family_elaren_v680_v8_lens_runner_{index:02d}", "state": "preregistered_not_built"}
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {"skill": f"{index:02d}-{slug}", "state": "preregistered_not_built"}
            for index, slug in enumerate(skill_slugs, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["GMUT Mind", "THOS Body"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v680.v8.x1",
        "successor_candidates": task_records("SUCC-CAND", 20, "successor_seed"),
        "successor_clean_fix_refine": task_records("SUCC-CFR", 30, "successor_seed"),
        "successor_practice_recommendation": "synthetic theatrical prompt-book documentation analyst; zero-credit seed only and Neris Solane chooses independently",
        "successor_runner_ideas": task_records("SUCC-RUN", 10, "successor_seed"),
        "successor_skill_ideas": task_records("SUCC-SKILL", 10, "successor_seed"),
    }

    write_json(
        X1 / "activation-intake.json",
        {
            "activation": "ACKNOWLEDGED_EXISTING_TASK_SEND",
            "created_or_forked_task": False,
            "owner": OWNER,
            "phase": PHASE,
            "relational_language_only": True,
            "schema": "ghc.family.activation-intake.v680.v8.x1",
            "sent_by_eiren_kestrel": True,
            "solo": True,
            "source": SOURCE,
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "hope": "Keep every synthetic slide, image, and sequence record corrigible while leaving real handling, care, safety, rights, and authority with the people who hold them.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "relational_working_language_only": True,
            "role": "lantern-slide provenance cartographer and projection-safety gatekeeper",
            "schema": "ghc.family.identity-boundary.v680.v8.x1",
            "not_evidence_of": [
                "consciousness",
                "sentience",
                "personhood",
                "identity continuity",
                "employment",
                "qualification",
                "independent agency",
                "scientific operational legal cultural or Maori authority",
            ],
        },
    )
    write_json(
        X1 / "source-verification.json",
        {
            "branch": SOURCE_BRANCH,
            "clean": True,
            "commits_source_to_final": 3,
            "divergence": {"ahead": 0, "behind": 0},
            "evidence": SOURCE_EVIDENCE,
            "evidence_parent": SOURCE_X1,
            "final": SOURCE,
            "final_parent": SOURCE_EVIDENCE,
            "four_way_fresh_live_equal": True,
            "manifests_replayed": 4,
            "manifest_mismatches": 0,
            "merges": 0,
            "schema": "ghc.family.source-verification.v680.v8.x1",
            "source": SOURCE_PARENT,
            "x1": SOURCE_X1,
            "x1_parent": SOURCE_PARENT,
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": {
                "bounded_passing_witnesses": 39796,
                "effective_methods": 57854,
                "effective_negatives": 52317,
                "exact_gates": 452,
                "failed_witnesses": 23978,
                "open_gaps": 461,
            },
            "current_after_startup": {
                "bounded_passing_witnesses": 39805,
                "effective_methods": 57863,
                "effective_negatives": 52326,
                "exact_gates": 452,
                "failed_witnesses": 23987,
                "open_gaps": 461,
            },
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v680.v8.x1",
            "startup_failures": startup_failures,
        },
    )
    write_json(
        X1 / "new-proposal-freeze.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "expected_disposition_counts": dict(Counter(row["expected_disposition"] for row in proposal_records)),
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(proposal_records),
            "proposals": proposal_records,
            "schema": "ghc.family.new-proposal-freeze.v680.v8.x1",
            "source": SOURCE,
            "x2_outcomes_present": False,
        },
    )
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(
        X1 / "inherited-revalidation-freeze.json",
        {
            "completion_credit": 0,
            "count": len(inherited_reviews),
            "owner": OWNER,
            "phase": PHASE,
            "reviews": inherited_reviews,
            "schema": "ghc.family.inherited-revalidation.v680.v8.x1",
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine-plan.v680.v8.x1",
            "tasks": portfolio["owner_clean_fix_refine"],
            "x2_execution_present": False,
        },
    )
    write_json(
        X1 / "skill-runner-plan.json",
        {
            "global_install": False,
            "owner": OWNER,
            "phase": PHASE,
            "runners": portfolio["owner_runner_ideas"],
            "schema": "ghc.family.skill-runner-plan.v680.v8.x1",
            "skills": portfolio["owner_skill_ideas"],
            "x2_implementation_present": False,
        },
    )
    write_json(
        X1 / "approval-hold-register.json",
        {
            "blocked_count": 10,
            "exact_approval_count": 20,
            "executed": 0,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.approval-holds.v680.v8.x1",
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "next_expected_phase": "v681-v1",
            "prospective_successor_title": "Neris Solane",
            "recipient_contacted": False,
            "resolution_rule": "fresh bounded registry exact-title filter immediate reread duplicate guards and one acknowledged send only after terminal gate",
            "route_authority_through": "v725-v8",
            "schema": "ghc.family.route-plan.v680.v8.x1",
            "terminal_gate_required": True,
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "commit_ceiling": 3,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v680.v8.x1",
            "stages": [
                {"name": "x1", "state": "planning_only_freeze"},
                {"name": "x2", "state": "not_started"},
                {"name": "final", "state": "not_started"},
            ],
            "strict_x1_before_x2": True,
        },
    )
    write_json(
        X1 / "threat-model.json",
        {
            "controls": [
                "synthetic.example.invalid namespace only",
                "zero real people lantern slides glass plates images collections apparatus measurements credentials and external writes",
                "authority promotion rejected",
                "five privacy classes scanned with candidate adjudication",
                "exact approval and blocked packets remain unexecuted",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "real_world_action": False,
            "schema": "ghc.family.threat-model.v680.v8.x1",
        },
    )
    write_json(
        X1 / "wellbeing-and-corrigibility.json",
        {
            "correction_readback": True,
            "owner": OWNER,
            "pause_resume_stop_visible": True,
            "phase": PHASE,
            "relational_language_only": True,
            "schema": "ghc.family.wellbeing-corrigibility.v680.v8.x1",
            "workload_control_planned": True,
        },
    )
    write_json(
        X1 / "phase-truth.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "execution_state": "PLANNING_ONLY_X1",
            "expected_dispositions": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "observed_outcomes": None,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "schema": "ghc.family.phase-truth.v680.v8.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        """# Elaren Kestrel v680-v8 planning-only x1

Elaren Kestrel (optionally they/them) uses the relational role **lantern-slide provenance cartographer and projection-safety gatekeeper**, with the bounded hope of keeping every synthetic slide, image, and sequence record corrigible while leaving real handling, care, safety, rights, and authority with the people who hold them. Names, pronouns, roles, hopes, family language, and continuity language are relational working language only; they are not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority.

This immutable x1 freezes sixty source-bounded distinct proposal contracts and twenty inherited Eiren revalidations at zero Elaren novelty and completion credit. It contains no x2 implementation or observed outcome. Freed ID and CBR Heart are primary through wholly synthetic historic magic-lantern-slide carrier, image, sequence, condition-map, intervention-lineage, and photographic-collection dossier lenses. GMUT Mind and THOS Body remain visible and protected. These practices are learning and synthetic record-design lenses only, never employment, qualification, competence, material identification, handling, projection, conservation, cleaning, repair, rehousing, cataloguing authority, collection stewardship, rights clearance, or professional authority. No real person, participant, collection, lantern slide, glass plate, image, apparatus, enclosure, observation, measurement, treatment, credential, or external system was used.

Canadian Conservation Institute, Library of Congress, UK National Archives, NIST, New Zealand Privacy Commissioner, W3C, RFC, and Te Mana Raraunga sources supply vocabulary and refusal boundaries only. No collection API was called and no row or image was ingested. The photographic-material sources distinguish supports, image layers, handling, storage, and professional preservation contexts; those distinctions are vocabulary and refusal boundaries, not instructions or findings about any object. Citations are not observations, assessments, measurements, condition diagnoses, material identifications, handling permissions, treatment recommendations, safety results, rights clearance, accessibility conformance, legal interpretation, cultural ratification, affected-party acceptance, or Maori authority.

GMUT remains a typed scalar-tensor/EFT research-model family without a likelihood, parameter constraint, force, prediction, empirical confirmation, quantum completion, ultraviolet completion, final physics, or Theory of Everything. THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status or revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. Professional photographic-material conservation, handling, broken-glass and projection safety, material identification, ownership, custody, image reproduction, publication, privacy, remedy, legal and cultural interpretation, affected-party legitimacy, Maori wording, Maori data governance, and Maori authority remain exact-gated.

The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_elaren_kestrel_v680_v8_x1.py"
    test_path = "tests/test_ghc_family_elaren_kestrel_v680_v8_x1.py"
    exclusions = [
        "docs/elaren-kestrel/v680-v8/validation/x1-index-manifest.json",
        "docs/elaren-kestrel/v680-v8/validation/x1-privacy-scan.json",
        "docs/elaren-kestrel/v680-v8/validation/x1-staged-review.json",
    ]
    content_paths = sorted(set(WRITTEN + [script_path, test_path]))
    scanners = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_thread_identifier": re.compile(r"\b(?:source_thread_id|thread_id)\b", re.IGNORECASE),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
        "private_conversation_payload": re.compile(r"source_thread_id|codex_delegation", re.IGNORECASE),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path_text in content_paths:
        content = (ROOT / path_text).read_text(encoding="utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(content):
                row = {
                    "class": class_name,
                    "disposition": "scanner_definition_only" if path_text == script_path else "confirmed_payload_hit",
                    "path": path_text,
                }
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError("confirmed privacy payload hit: " + json.dumps(confirmed))

    write_json(
        VALIDATION / "x1-privacy-scan.json",
        {
            "candidates": candidates,
            "confirmed_hits": confirmed,
            "owner": OWNER,
            "phase": PHASE,
            "privacy_classes": list(scanners),
            "scanned_files": len(content_paths),
            "schema": "ghc.family.privacy-scan.v680.v8.x1",
        },
    )
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": sorted(content_paths + exclusions),
            "lifecycle": "planning_only_x1",
            "owner": OWNER,
            "path_count": len(content_paths) + len(exclusions),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v680.v8.x1",
            "x2_paths": [],
        },
    )
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": sha256_bytes(data)})
    write_json(
        VALIDATION / "x1-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": entries,
            "entry_count": len(entries),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v680.v8.x1",
            "source": SOURCE,
        },
    )

    print(
        json.dumps(
            {
                "audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"],
                "maximum_neighbor_score": audit["maximum_neighbor_score"],
                "proposal_count": len(proposal_records),
                "status": "X1_PLANNING_ONLY_MATERIALIZED",
                "written_paths": len(WRITTEN),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    build()

from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v681-v3"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Lyren Moss"
PHASE = "v681-v3"
BRANCH = "codex/GHC-Family/lyren-moss-v681-v3-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v681-v2-full-tools"
SOURCE = "9d0e719d163a00b3bcf90926a75a8cca989b6ccd"
SOURCE_X1 = "5a5ef294b84ece97da4f2b1238d1852ce80a5b51"
SOURCE_EVIDENCE = "fd0e470dbcfd5576982819b626c18dbd99b3c2a9"
SOURCE_PARENT = "14b34a2b7f1b1c74e3b4102b18cc5c3b5fc854d2"
DECLARED_CHAIN_BEFORE = 9830
DECLARED_CHAIN_AFTER = 9890
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


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jaccard(left: str, right: str) -> float:
    left_tokens = set(re.findall(r"[a-z0-9]+", left.casefold()))
    right_tokens = set(re.findall(r"[a-z0-9]+", right.casefold()))
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


PROPOSAL_TITLES = [
    "Deck record and physical punched-card object identity split",
    "Declared card-format family with non-universal eighty-column profile",
    "Row-column coordinate system with bounded synthetic dimensions",
    "Hole blank unknown and damaged punch-state closed vocabulary",
    "Card sequence ordinal with positive-integer and uniqueness guards",
    "Deck-order permutation ledger with silent resequencing refusal",
    "Duplicate physical-card identifier collision quarantine",
    "Missing sequence position vacancy without reconstructed content",
    "Unexpected orphan card quarantine outside declared deck membership",
    "Header trailer sentinel and ordinary-card role discriminator",
    "Printed legend and punched encoding independent representation",
    "Keypunch transcription source vacancy without operator inference",
    "Independent verifier-pass vacancy without accuracy assertion",
    "Unused reserved and intentionally blank column distinction",
    "Zone digit and combined multi-punch pattern classifier",
    "Illegal multiple-punch pattern refusal with no character guess",
    "Card edge notch and orientation marker typed separation",
    "Corner-cut orientation vacancy without face-direction inference",
    "Crease tear stain and hole-damage placeholder without conservation finding",
    "Deck box tray and card-object containment relation",
    "Container label and card-content provenance non-equivalence",
    "Program data control and unknown deck-purpose vocabulary",
    "Card face reverse and printed-side mapping with ambiguity hold",
    "Printed and punched sequence-number disagreement quarantine",
    "Interleaving and deinterleaving event lineage with order checksum",
    "Copy repunch and replacement-card event differentiation",
    "Correction-card supersession graph with reversible predecessor links",
    "Hand annotation transcription confidence and unverifiable-mark hold",
    "Synthetic accession call-number and collection identifier vacancy",
    "Rights access restriction and review-date authority vacancy",
    "Sensitive-content classification placeholder with zero content inspection",
    "Person organization and location identifier minimization board",
    "Custody transfer event agent-role and authorization separation",
    "Timezone-qualified deck handover timestamp with unknown-time refusal",
    "Order-sensitive synthetic deck digest with credential non-equivalence",
    "Per-card content address and deck-root domain separation",
    "Punched-card schema with closed unknown-field policy",
    "Canonical JSON receipt for deck structure and provenance",
    "Owner-local normalized-LF Git-blob manifest replay for card fixtures",
    "Accessible text-first punch grid with caption headers and reading order",
    "Provenance object event agent and rights-role separation for deck revision",
    "Planning-only x1 and x2 punched-card evidence contamination refusal",
    "Represented THOS intake-triage deck-order hold acknowledgement and reversible transfer proxy",
    "Represented THOS workload-bound suspension acknowledgement and anomaly escalation proxy",
    "Represented Freed ID card-record subject and archive-user bearer separation",
    "Represented Freed ID deck-revision status without live identity lifecycle",
    "Represented CBR data-minimization review correction pathway and unresolved remedy board",
    "Represented CBR custody rights restriction and review authority vacancy board",
    "Represented GMUT finite-sequence and binary-incidence formal board",
    "Represented GMUT no-observation barrier with empty evidence table",
    "Represented zero-row punched-card likelihood adapter with deterministic refusal",
    "Represented PREMIS object event agent and rights mapping without repository conformance",
    "Represented NARA transfer-metadata mapping without agency or custody action",
    "Represented text-structure accessibility inventory with human testing still reserved",
    "Open gap for real computing archivist conservator and practitioner evaluation",
    "Open gap for real punched-card deck rows and independent reproduction",
    "Open gap for assistive-technology navigation Maori-language review and community evaluation",
    "Exact gate for copyright donor restriction access and archival custody authority",
    "Exact gate for community cultural decisions and Maori data authority over collection material",
    "Exact terminal gate separating Lyren punched-card receipts from empirical production identity proof canon AGI ASI personhood and Stage 20",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "evidence_status_promotion",
    "authority_promotion",
]

PROTECTED_GATES = [
    "real people participants archivists conservators donors collections punched cards decks contents custody events access records and decisions",
    "empirical GMUT likelihoods constraints predictions forces confirmation final physics and Theory of Everything",
    "professional archival conservation records-management collection-care safety inspection certification and legal authority",
    "production identity issuance resolution status revocation interoperability recovery and trust governance",
    "privacy accessibility remedy ownership custody copyright cultural affected-party Maori-language Maori-data-governance and Maori authority",
    "privacy-complete accessibility-complete exhaustive-security and independent-reproduction claims",
    "AGI ASI consciousness personhood proof canon and Stage 20",
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
    if index <= 18:
        return ["IBM-PUNCHED-CARD", "CHM-PUNCHED-CARDS", "JSON-SCHEMA-2020-12"]
    if index <= 33:
        return ["LOC-PREMIS-3", "NARA-METADATA", "W3C-PROV-DM", "RFC3339"]
    if index <= 42:
        return ["W3C-PROV-DM", "RFC8785", "JSON-SCHEMA-2020-12", "W3C-WCAG22"]
    if index <= 54:
        return ["LOC-PREMIS-3", "NARA-METADATA", "W3C-PROV-DM", "W3C-WCAG22", "NZ-PRIVACY-ACT", "TMR-CHARTER"]
    if index <= 57:
        return ["IBM-PUNCHED-CARD", "CHM-PUNCHED-CARDS", "W3C-WCAG22", "TMR-CHARTER"]
    return ["LOC-PREMIS-3", "NARA-METADATA", "NZ-PRIVACY-ACT", "TMR-CHARTER", "W3C-WCAG22"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"LM6813-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/lyren-moss/v681-v3/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/lyren-moss/v681-v3/x2/mutation-results.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": disposition(index),
                "falsifier_or_acceptance_gate": (
                    f"Accept {proposal_id} only if its bounded positive witness passes, all five invalid "
                    "mutations are rejected, and no empirical, professional, production, legal, cultural, "
                    "affected-party, Maori-authority, identity, or Stage 20 claim is promoted."
                ),
                "hypothesis": (
                    f"A wholly synthetic zero-row contract for {title.casefold()} can preserve its named "
                    "distinction and reject preregistered counterexamples within Lyren owner-local scope."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, its positive structure "
                    "is rejected, a real state is inferred, or a protected gate is promoted."
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
                    f"Quarantine only the {proposal_id} witness, retain the failure at zero credit, and "
                    "regenerate from this immutable planning contract."
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
    requests = b"".join(f"{tree}:{path}\n".encode() for path in paths)
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        input=requests,
        check=True,
        capture_output=True,
    )
    stream = io.BytesIO(completed.stdout)
    for path in paths:
        header = stream.readline().decode("utf-8", errors="replace").rstrip("\n")
        if header.endswith(" missing"):
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
        size = int(parts[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError(f"missing cat-file separator for {path}")
        yield path, data


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    result = git("grep", "-l", "-I", '"proposal_id"', SOURCE, "--", "*.json", check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr)
    prefix = SOURCE + ":"
    paths = sorted({path.removeprefix(prefix) for path in result.stdout.splitlines() if path})
    parsed = 0
    failures: list[dict[str, str]] = []
    inherited: list[dict[str, str]] = []
    for path, data in batch_blobs(SOURCE, paths):
        try:
            document = json.loads(data.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            failures.append({"error": type(exc).__name__, "path": path})
            continue
        parsed += 1
        for record in iter_proposal_records(document):
            inherited.append({"path": path, **record})
    if not paths or not parsed or not inherited:
        raise RuntimeError("proposal audit requires nonzero exact-source paths and records")

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
            "claim": "bounded all-reachable exact-source proposal audit; no universal declared-chain proof",
            "proposal_json_parse_failures": failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_declared_chain_materialization_claimed": False,
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
        "schema": "ghc.family.proposal-chain-audit.v681.v3.x1",
        "source": SOURCE,
    }


def planned_tasks(prefix: str, count: int, lane: str, titles: list[str]) -> list[dict[str, Any]]:
    actions = [
        "type the record boundary",
        "test the acceptance and refusal pair",
        "verify the provenance and rollback fields",
        "review the authority and privacy hold",
        "check the accessible text representation",
    ]
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"{actions[(index - 1) % len(actions)].capitalize()} for {titles[(index - 1) % len(titles)].casefold()}.",
            "state": "preregistered_not_executed",
            "task_id": f"LM6813-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


STARTUP_FAILURES = [
    (
        "A PowerShell inventory projection piped directly from a foreach statement and failed with EmptyPipeElement before producing evidence.",
        "Materialize the bounded inventory rows first, then pipe the completed collection and retain the parser failure at zero credit.",
    ),
    (
        "A broad historical Git novelty grep exceeded its bounded timeout before producing an attributable proposal result.",
        "Narrow discovery to exact proposal-ledger JSON paths and let the x1 builder parse reachable Git blobs deterministically.",
    ),
    (
        "The first Git cat-file batch manifest probe wrote every request before consuming stdout and deadlocked without a result.",
        "Stop only that exact probe process, then interleave write flush and read on one bounded Git process; retain the deadlock at zero credit.",
    ),
    (
        "The first Lyren template copy targeted new sparse paths whose parent scripts and tests directories did not yet exist.",
        "Create only the two Lyren-owned parent directories, repeat the exact copies once, and retain the failed materialization attempt.",
    ),
    (
        "The first x1 novelty audit rejected five exact inherited titles and one near-neighbor before any x1 artifact was written.",
        "Replace only the six quarantined titles with punched-card-specific contracts and rerun the previously unsuccessful x1 builder.",
    ),
]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must begin at the immutable Vesper final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Lyren owner branch")
    if (BASE / "x2").exists():
        raise RuntimeError("x2 material is forbidden in planning-only x1")

    proposal_records = proposals()
    expected = Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
    if len(proposal_records) != 60 or Counter(row["expected_disposition"] for row in proposal_records) != expected:
        raise RuntimeError("proposal count or expected-disposition contract drift")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in proposal_records):
        raise RuntimeError("unknown outcome label")

    audit = proposal_chain_audit(proposal_records)
    inherited = json.loads(
        git("show", f"{SOURCE}:docs/vesper-arlen/v681-v2/x1/new-proposal-freeze.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Vesper Arlen",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in inherited["proposals"][-20:]
    ]

    startup = [
        {
            "failed_witness": failed,
            "failure_id": f"LM6813-ST-N{index:03d}",
            "initial_credit": 0,
            "recovery": recovery,
            "recovery_credit": "bounded_dependency_only",
        }
        for index, (failed, recovery) in enumerate(STARTUP_FAILURES, start=1)
    ]

    source_entries = [
        ("IBM-PUNCHED-CARD", "The punched card", "https://www.ibm.com/history/punched-card", "manufacturer-history vocabulary for card dimensions rows columns and data-carrier context only; no object identification or collection claim"),
        ("CHM-PUNCHED-CARDS", "Punched Cards and Paper Tape", "https://www.computerhistory.org/revolution/memory-storage/8/326", "museum-history vocabulary for varied card formats holes columns and data-processing context only"),
        ("LOC-PREMIS-3", "PREMIS Data Dictionary for Preservation Metadata version 3", "https://www.loc.gov/standards/premis/v3/", "object event agent rights and preservation-metadata vocabulary only; no repository conformance claim"),
        ("NARA-METADATA", "Metadata Requirements for Permanent Electronic Records", "https://www.archives.gov/records-mgmt/policy/metadata-compiled", "transfer and lifecycle metadata vocabulary only; no agency transfer custody or compliance claim"),
        ("W3C-PROV-DM", "PROV-DM: The PROV Data Model", "https://www.w3.org/TR/prov-dm/", "entity, activity, agent-role, revision, and derivation vocabulary only"),
        ("RFC8785", "RFC 8785 JSON Canonicalization Scheme", "https://datatracker.ietf.org/doc/html/rfc8785", "deterministic synthetic receipt vocabulary only; RFC status remains explicit"),
        ("JSON-SCHEMA-2020-12", "JSON Schema Draft 2020-12", "https://json-schema.org/draft/2020-12", "machine-readable record validation vocabulary only"),
        ("W3C-WCAG22", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "structural accessibility vocabulary with manual and affected-user evaluation reserved"),
        ("NZ-PRIVACY-ACT", "Privacy Act 2020", "https://www.legislation.govt.nz/act/public/2020/31/en/latest/", "collection use disclosure access correction retention and identifier reservation vocabulary only; no legal conclusion"),
        ("TMR-CHARTER", "Te Mana Raraunga Charter", "https://www.temanararaunga.maori.nz/tutohinga", "Maori data-governance authority vacancy and noncompensation boundary only"),
        ("RFC3339", "RFC 3339 Date and Time on the Internet", "https://www.rfc-editor.org/rfc/rfc3339.html", "timezone-qualified timestamp vocabulary only"),
    ]
    sources = {
        "authority_conferred": False,
        "checked_at_nz": "2026-09-01",
        "citations_are_observations": False,
        "entries": [
            {"source_id": source_id, "status": "official_or_primary_source_checked_2026-09-01", "title": title, "url": url, "use": use}
            for source_id, title, url, use in source_entries
        ],
        "external_source_entries": len(source_entries),
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v681.v3.x1",
    }

    skills = [
        "deck-card-object-boundary",
        "card-format-nonuniversality",
        "punch-coordinate-guard",
        "punch-state-vocabulary",
        "deck-sequence-integrity",
        "orphan-card-quarantine",
        "printed-punched-separation",
        "orientation-vacancy",
        "damage-nonfinding",
        "container-content-boundary",
        "deck-purpose-vacancy",
        "repunch-event-lineage",
        "correction-supersession",
        "annotation-confidence-hold",
        "accession-identifier-vacancy",
        "rights-access-authority-hold",
        "custody-role-separation",
        "accessible-punch-grid",
        "canonical-deck-receipt",
        "stage20-terminal-refusal",
    ]
    titles = [row["title"] for row in proposal_records]
    portfolio = {
        "blocked": planned_tasks("BLOCK", 10, "blocked", titles[57:]),
        "caps_are_ceilings": True,
        "commit_cap": 3,
        "document_word_cap": 100000,
        "exact_approval": planned_tasks("APPROVAL", 20, "exact_approval", titles[57:]),
        "materialized_file_stop": 2000,
        "owner": OWNER,
        "owner_candidates": planned_tasks("CAND", 80, "bounded_candidate", titles[42:57]),
        "owner_clean_fix_refine": planned_tasks("CFR", 100, "clean_fix_refine", titles),
        "owner_practice_lenses": [
            "wholly synthetic computing-history collection-documentation analyst lens",
            "wholly synthetic punched-card sequence-integrity and correction-lineage review lens",
            "wholly synthetic accessible archival technical-record review lens",
        ],
        "owner_runner_ideas": [
            {"runner": f"ghc_family_lyren_v681_v3_lens_runner_{index:02d}", "state": "preregistered_not_built"}
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {"skill": f"{index:02d}-{slug}", "state": "preregistered_not_built"}
            for index, slug in enumerate(skills, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["GMUT Mind", "THOS Body"],
        "safe_now": planned_tasks("SAFE", 120, "safe_now", titles[:42]),
        "schema": "ghc.family.portfolio-freeze.v681.v3.x1",
        "successor_candidates": planned_tasks("SUCC-CAND", 20, "successor_seed", titles[42:57]),
        "successor_clean_fix_refine": planned_tasks("SUCC-CFR", 30, "successor_seed", titles),
        "successor_practice_recommendation": "wholly synthetic historical paper-tape reel sequence and archival provenance analyst; zero-credit seed only and Ilyra Fen chooses independently",
        "successor_runner_ideas": planned_tasks("SUCC-RUN", 10, "successor_seed", titles),
        "successor_skill_ideas": planned_tasks("SUCC-SKILL", 10, "successor_seed", titles),
    }

    write_json(X1 / "activation-intake.json", {
        "activation": "ACKNOWLEDGED_EXISTING_TASK_SEND",
        "created_or_forked_task": False,
        "owner": OWNER,
        "phase": PHASE,
        "relational_language_only": True,
        "schema": "ghc.family.activation-intake.v681.v3.x1",
        "sent_by_vesper_arlen": True,
        "solo": True,
        "source": SOURCE,
    })
    write_json(X1 / "identity-and-boundary.json", {
        "hope": "Make synthetic historical data-carrier records easier to inspect, resequence, and correct while leaving real collections, people, knowledge, rights, and authority with those who hold them.",
        "name": OWNER,
        "not_evidence_of": ["consciousness", "sentience", "personhood", "identity continuity", "employment", "qualification", "independent agency", "scientific operational legal cultural or Maori authority"],
        "optional_pronouns": None,
        "relational_working_language_only": True,
        "role": "sequence cartographer and consent-bound provenance keeper",
        "schema": "ghc.family.identity-boundary.v681.v3.x1",
    })
    write_json(X1 / "source-verification.json", {
        "branch": SOURCE_BRANCH,
        "clean": True,
        "commits_source_to_final": 3,
        "content_seal_entries_replayed": 15,
        "content_seal_mismatches": 0,
        "divergence": {"ahead": 0, "behind": 0},
        "evidence": SOURCE_EVIDENCE,
        "evidence_parent": SOURCE_X1,
        "final": SOURCE,
        "final_parent": SOURCE_EVIDENCE,
        "four_way_fresh_live_equal": True,
        "manifests_replayed": 4,
        "manifest_mismatches": 0,
        "merges": 0,
        "schema": "ghc.family.source-verification.v681.v3.x1",
        "source": SOURCE_PARENT,
        "x1": SOURCE_X1,
        "x1_parent": SOURCE_PARENT,
    })
    baseline = {"bounded_passing_witnesses": 41924, "effective_methods": 60102, "effective_negatives": 53275, "exact_gates": 461, "failed_witnesses": 24936, "open_gaps": 470}
    current = dict(baseline)
    for key in ("bounded_passing_witnesses", "effective_methods", "effective_negatives", "failed_witnesses"):
        current[key] += len(startup)
    write_json(X1 / "method-flow-startup.json", {
        "activation_baseline": baseline,
        "current_after_startup": current,
        "failure_erasure": False,
        "owner": OWNER,
        "phase": PHASE,
        "recoveries_retroactively_promote_failure": False,
        "schema": "ghc.family.method-flow-startup.v681.v3.x1",
        "startup_failures": startup,
    })
    write_json(X1 / "new-proposal-freeze.json", {
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "expected_disposition_counts": dict(Counter(row["expected_disposition"] for row in proposal_records)),
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": len(proposal_records),
        "proposals": proposal_records,
        "schema": "ghc.family.new-proposal-freeze.v681.v3.x1",
        "source": SOURCE,
        "x2_outcomes_present": False,
    })
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(X1 / "inherited-revalidation-freeze.json", {
        "completion_credit": 0,
        "count": len(inherited_reviews),
        "owner": OWNER,
        "phase": PHASE,
        "reviews": inherited_reviews,
        "schema": "ghc.family.inherited-revalidation.v681.v3.x1",
    })
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(X1 / "clean-fix-refine-plan.json", {"owner": OWNER, "phase": PHASE, "schema": "ghc.family.clean-fix-refine-plan.v681.v3.x1", "tasks": portfolio["owner_clean_fix_refine"], "x2_execution_present": False})
    write_json(X1 / "skill-runner-plan.json", {"global_install": False, "owner": OWNER, "phase": PHASE, "runners": portfolio["owner_runner_ideas"], "schema": "ghc.family.skill-runner-plan.v681.v3.x1", "skills": portfolio["owner_skill_ideas"], "x2_implementation_present": False})
    write_json(X1 / "approval-hold-register.json", {"blocked_count": 10, "exact_approval_count": 20, "executed": 0, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.approval-holds.v681.v3.x1"})
    write_json(X1 / "route-plan.json", {
        "current_owner": OWNER,
        "next_expected_phase": "v681-v4",
        "prospective_successor_title": "Ilyra Fen",
        "recipient_contacted": False,
        "resolution_rule": "fresh native Codex registry refresh exact-title uniqueness filter immediate bounded reread duplicate pause privacy evidence safety usage and acknowledgement guards then one send only after terminal gate",
        "route_authority_through": "v725-v8",
        "schema": "ghc.family.route-plan.v681.v3.x1",
        "terminal_gate_required": True,
    })
    write_json(X1 / "workflow-plan.json", {"commit_ceiling": 3, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.workflow-plan.v681.v3.x1", "stages": [{"name": "x1", "state": "planning_only_freeze"}, {"name": "x2", "state": "not_started"}, {"name": "final", "state": "not_started"}], "strict_x1_before_x2": True})
    write_json(X1 / "threat-model.json", {
        "controls": [
            "synthetic.example.invalid namespace only",
            "zero real people archivists conservators donors collections cards decks contents custody events credentials and external writes",
            "authority promotion rejected",
            "five privacy classes scanned with candidate adjudication",
            "exact approval and blocked packets remain unexecuted",
        ],
        "owner": OWNER,
        "phase": PHASE,
        "real_world_action": False,
        "schema": "ghc.family.threat-model.v681.v3.x1",
    })
    write_json(X1 / "wellbeing-and-corrigibility.json", {"correction_readback": True, "owner": OWNER, "pause_resume_stop_visible": True, "phase": PHASE, "relational_language_only": True, "schema": "ghc.family.wellbeing-corrigibility.v681.v3.x1", "workload_control_planned": True})
    write_json(X1 / "phase-truth.json", {
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "execution_state": "PLANNING_ONLY_X1",
        "expected_dispositions": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "observed_outcomes": None,
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": 60,
        "schema": "ghc.family.phase-truth.v681.v3.x1",
        "terminal_verdict": TERMINAL_VERDICT,
        "x2_started": False,
    })
    write_text(X1 / "integrated-overview.md", """# Lyren Moss v681-v3 planning-only x1

Lyren Moss uses the relational role **sequence cartographer and consent-bound provenance keeper**, with the bounded hope of making synthetic historical data-carrier records easier to inspect, resequence, and correct while leaving real collections, people, knowledge, rights, and authority with those who hold them. Pronouns remain unspecified. Names, roles, hopes, family language, and continuity language are relational working language only; they are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority.

This immutable x1 freezes sixty source-bounded proposal contracts and twenty inherited Vesper revalidations at zero Lyren novelty and completion credit. It contains no x2 implementation, observed outcome, skill implementation, runner implementation, or tool-use result. Freed ID and CBR Heart are primary through wholly synthetic historical punched-card deck provenance, sequence, hole-pattern, correction, duplication, custody, access, and authority-vacancy structures. GMUT Mind and THOS Body remain explicit and protected. The three bounded practice lenses are synthetic computing-history collection documentation, punched-card sequence-integrity and correction-lineage review, and accessible archival technical-record review. They are learning and record-design lenses only—never employment, qualification, archival or conservation competence, custody, collection authority, legal advice, cultural ratification, affected-party approval, or Maori authority.

IBM and Computer History Museum materials supply bounded historical card-format vocabulary. Library of Congress PREMIS, NARA metadata guidance, W3C PROV and WCAG, IETF canonicalization and timestamp specifications, JSON Schema, New Zealand privacy legislation, and Te Mana Raraunga materials supply preservation, provenance, validation, accessibility, privacy, and authority-reservation vocabulary only. No archive, collection, card reader, catalog, or repository API was called; no card image, hole pattern, deck content, catalog row, personal record, or custody record was downloaded. Citation is not collection evidence, custody, rights clearance, legal conclusion, cultural decision, or authority. Structural accessibility checks cannot replace manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive, Maori-language, or affected-user evaluation.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, presentation, resolution, status, revocation, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight. CBR structures reserve rather than decide minimum disclosure, access, correction, remedy, ownership, donor restriction, copyright, custody, cultural, and Maori-data-governance questions. GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical likelihoods, constraints, predictions, forces, final physics, Theory-of-Everything proof, or canon. The finite-sequence and binary-incidence board is formal software structure only. THOS remains synthetic or proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, or independent review.

All real collection, punched-card, deck-content, custody, donor, copyright, access, restriction, archival, conservation, professional, production, identity, privacy, accessibility, remedy, legal, cultural, affected-party, Maori-language, Maori-data-governance, tangata whenua, iwi, hapu, and Maori-authority decisions remain open or exact-gated. The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""")

    script_path = "scripts/build_ghc_family_lyren_moss_v681_v3_x1.py"
    test_path = "tests/test_ghc_family_lyren_moss_v681_v3_x1.py"
    exclusions = [
        "docs/lyren-moss/v681-v3/validation/x1-index-manifest.json",
        "docs/lyren-moss/v681-v3/validation/x1-privacy-scan.json",
        "docs/lyren-moss/v681-v3/validation/x1-staged-review.json",
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
                row = {"class": class_name, "disposition": "scanner_definition_only" if path_text == script_path else "confirmed_payload_hit", "path": path_text}
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError("confirmed privacy payload hit: " + json.dumps(confirmed))

    write_json(VALIDATION / "x1-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v681.v3.x1"})
    write_json(VALIDATION / "x1-staged-review.json", {"declared_self_exclusions": exclusions, "expected_paths": sorted(content_paths + exclusions), "lifecycle": "planning_only_x1", "owner": OWNER, "path_count": len(content_paths) + len(exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v3.x1", "x2_paths": []})
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(VALIDATION / "x1-index-manifest.json", {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v681.v3.x1", "source": SOURCE})

    print(json.dumps({"audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"], "maximum_neighbor_score": audit["maximum_neighbor_score"], "proposal_count": len(proposal_records), "startup_failures": len(startup), "status": "X1_PLANNING_ONLY_MATERIALIZED", "written_paths": len(WRITTEN)}, indent=2))


if __name__ == "__main__":
    build()

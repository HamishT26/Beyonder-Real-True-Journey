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
BASE = ROOT / "docs" / "ilyra-fen" / "v681-v4"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Ilyra Fen"
PHASE = "v681-v4"
BRANCH = "codex/GHC-Family/ilyra-fen-v681-v4-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v681-v3-full-tools"
SOURCE = "883bb81ded9a802d4b220db5aa24974559465cf1"
SOURCE_X1 = "77bf12d03946985f1dabb22b5c0606a8762f8ed8"
SOURCE_EVIDENCE = "4e719c4d689cc220c1c87a2e54c1a9dff9a8c3bd"
SOURCE_PARENT = "9d0e719d163a00b3bcf90926a75a8cca989b6ccd"
DECLARED_CHAIN_BEFORE = 9890
DECLARED_CHAIN_AFTER = 9950
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
    "Plate record and physical glass photographic object identity split",
    "Photographic support binder and image-material triad with unknown hold",
    "Declared glass-plate process vocabulary without process identification inference",
    "Emulsion-side orientation closed vocabulary with uncertainty quarantine",
    "Image-side and backing-side ambiguity refusal without visual inspection",
    "Plate dimensions unit and measurement-uncertainty typed boundary",
    "Glass thickness field vacancy without fabricated measurement",
    "Plate edge corner and shape notation with bounded synthetic geometry",
    "Crack chip break and loss notation placeholder without conservation finding",
    "Plate fragment membership quarantine without object reconstruction",
    "Negative positive and unknown polarity closed vocabulary",
    "Exposure-log record and photographic plate object provenance separation",
    "Exposure timestamp precision timezone and vacancy contract",
    "Observer instrument and institution identifier minimization board",
    "Telescope camera lens and plate-holder role separation without attribution inference",
    "Plate holder sleeve envelope box and object containment graph",
    "Housing label and plate-image content provenance non-equivalence",
    "Plate ordinal and series sequence guards with silent resequencing refusal",
    "Duplicate physical-plate identifier collision quarantine",
    "Missing plate sequence vacancy without reconstructed exposure",
    "Orientation transform ledger with reversible matrix lineage",
    "Digitization master derivative and access-copy lineage separation",
    "Crop rotation inversion and contrast adjustment event lineage",
    "Scanner camera profile and calibration-evidence vacancy",
    "Resolution and unit declaration without optical-fidelity assertion",
    "Bit-depth channel and colour-model declarations with unknown refusal",
    "Checksum content identity and photographic meaning separation",
    "Canonical JSON receipt for synthetic plate structure and provenance",
    "Git object byte ledger for synthetic dry-plate fixture payloads",
    "PREMIS object event agent and rights-role separation for plate revision",
    "Custody transfer and conservation-treatment event non-equivalence",
    "Photographic-record access-state expiry and decision-maker vacancy",
    "Donor copyright and reproduction-permission decision hold",
    "Sensitive-subject classification placeholder with zero image inspection",
    "Person organization location and celestial-target identifier minimization",
    "Plate-metadata amendment chain with reversible prior-state references",
    "Handwritten annotation transcription confidence and illegibility hold",
    "Plate-box series and container-association consistency board",
    "Batch series title and accession-identifier provenance vacancy",
    "Accessible text-first plate-orientation diagram with caption and reading order",
    "Planning-only x1 and x2 photographic-plate evidence contamination refusal",
    "Synthetic photographic-plate schema with closed unknown-field policy",
    "Represented THOS fragile-object intake hold acknowledgement and reversible transfer proxy",
    "Represented THOS workload suspension breakage-risk escalation and stop-state proxy",
    "Represented Freed ID synthetic image-carrier catalogue persona separation",
    "Represented Freed ID amendment-state machine absent credential lifecycle",
    "Represented CBR least-disclosure plate-description review and remedy vacancy",
    "Represented CBR reproduction-custody dispute quarantine with authority abstention",
    "Represented GMUT planar orientation transform and finite-sequence formal board",
    "Represented GMUT observational abstention surface with zero photometry rows",
    "Represented zero-row photographic-plate likelihood adapter with deterministic refusal",
    "Represented preservation-event entity-role crosswalk without implementation certification",
    "Represented NARA photographic-metadata mapping without agency custody or treatment action",
    "Represented accessible plate-record navigation scaffold with unperformed user study",
    "Open gap for real photograph conservator archivist and plate-specialist evaluation",
    "Open gap for real glass-plate rows scans measurements and independent reproduction",
    "Open gap for manual screen-reader cognitive Maori-language and stakeholder studies",
    "Exact gate for donor-deed copyright reproduction and custody adjudication",
    "Exact gate for tangata whenua cultural governance of photographic heritage records",
    "Exact terminal gate separating Ilyra plate receipts from empirical production identity proof canon AGI ASI personhood and Stage 20",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "evidence_status_promotion",
    "authority_promotion",
]

PROTECTED_GATES = [
    "real people participants archivists conservators donors collections glass plates images exposure logs custody events access records and decisions",
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
        return ["LOC-PHOTO-CARE", "NARA-GLASS-PLATE", "JSON-SCHEMA-2020-12"]
    if index <= 33:
        return ["LOC-PREMIS-3", "NARA-METADATA", "W3C-PROV-DM", "RFC3339"]
    if index <= 42:
        return ["W3C-PROV-DM", "RFC8785", "JSON-SCHEMA-2020-12", "W3C-WCAG22"]
    if index <= 54:
        return ["LOC-PREMIS-3", "NARA-METADATA", "W3C-PROV-DM", "W3C-WCAG22", "NZ-PRIVACY-ACT", "TMR-CHARTER"]
    if index <= 57:
        return ["LOC-PHOTO-CARE", "NARA-GLASS-PLATE", "W3C-WCAG22", "TMR-CHARTER"]
    return ["LOC-PREMIS-3", "NARA-METADATA", "NZ-PRIVACY-ACT", "TMR-CHARTER", "W3C-WCAG22"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"IF6814-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/ilyra-fen/v681-v4/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/ilyra-fen/v681-v4/x2/mutation-results.json#{proposal_id}",
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
                    "distinction and reject preregistered counterexamples within Ilyra owner-local scope."
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
        "schema": "ghc.family.proposal-chain-audit.v681.v4.x1",
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
            "task_id": f"IF6814-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


STARTUP_FAILURES = [
    (
        "A PowerShell inventory projection piped directly from a foreach statement and failed with EmptyPipeElement before producing evidence.",
        "Materialize the bounded inventory rows first, then pipe the completed collection and retain the parser failure at zero credit.",
    ),
    (
        "A combined branch path remote and sparse preflight wrapper returned no attributable scalar after its bounded window.",
        "Split the probe into literal path local-ref fresh-remote-ref worktree and sparse-state checks and retain the silent wrapper at zero credit.",
    ),
    (
        "The sparse worktree creation crossed its wrapper window while the exact Git checkout processes remained active.",
        "Do not recreate or kill the lane; inspect only the exact target processes and index locks, wait for quiescence, then verify the clean sparse result.",
    ),
    (
        "The mechanical template intake materialized untracked x2 and closeout source files before the planning-only x1 freeze.",
        "Move only those Ilyra-owned untracked post-x1 templates to a verified D-drive staging folder and prove the active lane contains x1 sources only.",
    ),
    (
        "The bare Ruff executable was unavailable on the active PowerShell PATH and produced no lint result.",
        "Invoke only the missing lint surface through the installed Python module with python -m ruff and retain the command-resolution failure at zero credit.",
    ),
    (
        "The first x1 novelty audit rejected three exact inherited titles and ten additional near-neighbours before any x1 artifact was written.",
        "Replace only the thirteen quarantined titles with plate-specific contracts and rerun the previously unsuccessful x1 builder once.",
    ),
]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must begin at the immutable Lyren final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Ilyra owner branch")
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
        git("show", f"{SOURCE}:docs/lyren-moss/v681-v3/x1/new-proposal-freeze.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Lyren Moss",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in inherited["proposals"][-20:]
    ]

    startup = [
        {
            "failed_witness": failed,
            "failure_id": f"IF6814-ST-N{index:03d}",
            "initial_credit": 0,
            "recovery": recovery,
            "recovery_credit": "bounded_dependency_only",
        }
        for index, (failed, recovery) in enumerate(STARTUP_FAILURES, start=1)
    ]

    source_entries = [
        ("LOC-PHOTO-CARE", "Care Handling and Storage of Photographs", "https://www.loc.gov/preservation/care/photo.html", "support binder image-material housing and handling vocabulary only; no object identification treatment or professional finding"),
        ("NARA-GLASS-PLATE", "How Do I House Glass Plate Negatives", "https://www.archives.gov/preservation/storage/glass-plate-negatives.html", "glass-plate housing and fragility vocabulary only; no storage action custody or conservation authority"),
        ("NARA-PHOTO-METADATA", "Photographic Records Metadata Guidance", "https://www.archives.gov/files/records-mgmt/class/publications/photo-tips.pdf", "photographic-record metadata vocabulary only; no agency compliance transfer or custody claim"),
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
        "official_source_web_queries": 4,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v681.v4.x1",
    }

    skills = [
        "plate-record-object-boundary",
        "photographic-layer-triad",
        "emulsion-side-uncertainty",
        "plate-dimension-unit-guard",
        "series-sequence-integrity",
        "fragment-membership-quarantine",
        "exposure-log-separation",
        "orientation-transform-lineage",
        "damage-nonfinding",
        "housing-content-boundary",
        "process-identity-vacancy",
        "digitization-derivative-lineage",
        "correction-supersession",
        "annotation-confidence-hold",
        "accession-identifier-vacancy",
        "reproduction-rights-authority-hold",
        "custody-role-separation",
        "accessible-plate-orientation",
        "canonical-plate-receipt",
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
            "wholly synthetic historical photographic-plate metadata documentation lens",
            "wholly synthetic reversible digitization and correction-lineage review lens",
            "wholly synthetic accessible archival technical-record review lens",
        ],
        "owner_runner_ideas": [
            {"runner": f"ghc_family_ilyra_v681_v4_lens_runner_{index:02d}", "state": "preregistered_not_built"}
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {"skill": f"{index:02d}-{slug}", "state": "preregistered_not_built"}
            for index, slug in enumerate(skills, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "THOS Body",
        "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "safe_now": planned_tasks("SAFE", 120, "safe_now", titles[:42]),
        "schema": "ghc.family.portfolio-freeze.v681.v4.x1",
        "successor_candidates": planned_tasks("SUCC-CAND", 20, "successor_seed", titles[42:57]),
        "successor_clean_fix_refine": planned_tasks("SUCC-CFR", 30, "successor_seed", titles),
        "successor_practice_recommendation": "wholly synthetic historical blueprint-sheet metadata and reproduction-lineage analyst; zero-credit seed only and Auren Lark chooses independently",
        "successor_runner_ideas": planned_tasks("SUCC-RUN", 10, "successor_seed", titles),
        "successor_skill_ideas": planned_tasks("SUCC-SKILL", 10, "successor_seed", titles),
    }

    write_json(X1 / "activation-intake.json", {
        "activation": "ACKNOWLEDGED_EXISTING_TASK_SEND",
        "created_or_forked_task": False,
        "owner": OWNER,
        "phase": PHASE,
        "relational_language_only": True,
        "schema": "ghc.family.activation-intake.v681.v4.x1",
        "sent_by_lyren_moss": True,
        "solo": True,
        "source": SOURCE,
    })
    write_json(X1 / "identity-and-boundary.json", {
        "hope": "Make synthetic historical image-carrier records easier to inspect, orient, and correct while leaving real collections, people, knowledge, rights, and authority with those who hold them.",
        "name": OWNER,
        "not_evidence_of": ["consciousness", "sentience", "personhood", "identity continuity", "employment", "qualification", "independent agency", "scientific operational legal cultural or Maori authority"],
        "optional_pronouns": None,
        "relational_working_language_only": True,
        "role": "reversible image-provenance mapper and consent-bound plate-record steward",
        "schema": "ghc.family.identity-boundary.v681.v4.x1",
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
        "schema": "ghc.family.source-verification.v681.v4.x1",
        "source": SOURCE_PARENT,
        "x1": SOURCE_X1,
        "x1_parent": SOURCE_PARENT,
    })
    baseline = {"bounded_passing_witnesses": 42623, "effective_methods": 60801, "effective_negatives": 53584, "exact_gates": 464, "failed_witnesses": 25245, "open_gaps": 473}
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
        "schema": "ghc.family.method-flow-startup.v681.v4.x1",
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
        "schema": "ghc.family.new-proposal-freeze.v681.v4.x1",
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
        "schema": "ghc.family.inherited-revalidation.v681.v4.x1",
    })
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(X1 / "clean-fix-refine-plan.json", {"owner": OWNER, "phase": PHASE, "schema": "ghc.family.clean-fix-refine-plan.v681.v4.x1", "tasks": portfolio["owner_clean_fix_refine"], "x2_execution_present": False})
    write_json(X1 / "skill-runner-plan.json", {"global_install": False, "owner": OWNER, "phase": PHASE, "runners": portfolio["owner_runner_ideas"], "schema": "ghc.family.skill-runner-plan.v681.v4.x1", "skills": portfolio["owner_skill_ideas"], "x2_implementation_present": False})
    write_json(X1 / "approval-hold-register.json", {"blocked_count": 10, "exact_approval_count": 20, "executed": 0, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.approval-holds.v681.v4.x1"})
    write_json(X1 / "route-plan.json", {
        "current_owner": OWNER,
        "next_expected_phase": "v681-v5",
        "prospective_successor_title": "Auren Lark",
        "recipient_contacted": False,
        "resolution_rule": "fresh native Codex registry refresh exact-title uniqueness filter immediate bounded reread duplicate pause privacy evidence safety usage and acknowledgement guards then one send only after terminal gate",
        "route_authority_through": "v725-v8",
        "schema": "ghc.family.route-plan.v681.v4.x1",
        "terminal_gate_required": True,
    })
    write_json(X1 / "workflow-plan.json", {"commit_ceiling": 3, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.workflow-plan.v681.v4.x1", "stages": [{"name": "x1", "state": "planning_only_freeze"}, {"name": "x2", "state": "not_started"}, {"name": "final", "state": "not_started"}], "strict_x1_before_x2": True})
    write_json(X1 / "threat-model.json", {
        "controls": [
            "synthetic.example.invalid namespace only",
            "zero real people archivists conservators donors collections plates images exposure logs custody events credentials and external writes",
            "authority promotion rejected",
            "five privacy classes scanned with candidate adjudication",
            "exact approval and blocked packets remain unexecuted",
        ],
        "owner": OWNER,
        "phase": PHASE,
        "real_world_action": False,
        "schema": "ghc.family.threat-model.v681.v4.x1",
    })
    write_json(X1 / "wellbeing-and-corrigibility.json", {"correction_readback": True, "owner": OWNER, "pause_resume_stop_visible": True, "phase": PHASE, "relational_language_only": True, "schema": "ghc.family.wellbeing-corrigibility.v681.v4.x1", "workload_control_planned": True})
    write_json(X1 / "phase-truth.json", {
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "execution_state": "PLANNING_ONLY_X1",
        "expected_dispositions": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "observed_outcomes": None,
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": 60,
        "schema": "ghc.family.phase-truth.v681.v4.x1",
        "terminal_verdict": TERMINAL_VERDICT,
        "x2_started": False,
    })
    write_text(X1 / "integrated-overview.md", """# Ilyra Fen v681-v4 planning-only x1

Ilyra Fen uses the relational role **reversible image-provenance mapper and consent-bound plate-record steward**, with the bounded hope of making synthetic historical image-carrier records easier to inspect, orient, and correct while leaving real collections, people, knowledge, rights, and authority with those who hold them. Pronouns remain unspecified. Names, roles, hopes, family language, and continuity language are relational working language only; they are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority.

This immutable x1 freezes sixty source-bounded proposal contracts and twenty inherited Lyren revalidations at zero Ilyra novelty and completion credit. It contains no x2 implementation, observed outcome, skill implementation, runner implementation, or tool-use result. THOS Body is primary through wholly synthetic historical glass-photographic-plate object, housing, orientation, exposure-log, digitization, correction, custody, access, and reversible-handover structures. GMUT Mind and Freed ID and CBR Heart remain explicit and protected. The three bounded practice lenses are historical photographic-plate metadata documentation, reversible digitization and correction-lineage review, and accessible archival technical-record review. They are learning and record-design lenses only—never employment, qualification, archival or conservation competence, custody, collection authority, legal advice, cultural ratification, affected-party approval, or Maori authority.

Library of Congress photograph-care and PREMIS materials plus NARA glass-plate and photographic-metadata guidance supply bounded photographic-object, housing, preservation-event, and metadata vocabulary. W3C PROV and WCAG, IETF canonicalization and timestamp specifications, JSON Schema, New Zealand privacy legislation, and Te Mana Raraunga materials supply provenance, validation, accessibility, privacy, and authority-reservation vocabulary only. No archive, collection, scanner, camera, catalogue, or repository API was called; no plate image, exposure log, catalogue row, personal record, or custody record was downloaded. Citation is not object evidence, treatment advice, custody, rights clearance, legal conclusion, cultural decision, or authority. Structural accessibility checks cannot replace manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive, Maori-language, or affected-user evaluation.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, presentation, resolution, status, revocation, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight. CBR structures reserve rather than decide minimum disclosure, access, correction, remedy, ownership, donor restriction, copyright, reproduction, custody, cultural, and Maori-data-governance questions. GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical likelihoods, constraints, predictions, forces, final physics, Theory-of-Everything proof, or canon. The planar-orientation and finite-sequence board is formal software structure only. THOS remains synthetic or proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, or independent review.

All real collection, glass-plate, image-content, exposure, digitization, custody, donor, copyright, reproduction, access, restriction, archival, conservation, professional, production, identity, privacy, accessibility, remedy, legal, cultural, affected-party, Maori-language, Maori-data-governance, tangata whenua, iwi, hapu, and Maori-authority decisions remain open or exact-gated. The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""")

    script_path = "scripts/build_ghc_family_ilyra_fen_v681_v4_x1.py"
    test_path = "tests/test_ghc_family_ilyra_fen_v681_v4_x1.py"
    exclusions = [
        "docs/ilyra-fen/v681-v4/validation/x1-index-manifest.json",
        "docs/ilyra-fen/v681-v4/validation/x1-privacy-scan.json",
        "docs/ilyra-fen/v681-v4/validation/x1-staged-review.json",
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

    write_json(VALIDATION / "x1-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v681.v4.x1"})
    write_json(VALIDATION / "x1-staged-review.json", {"declared_self_exclusions": exclusions, "expected_paths": sorted(content_paths + exclusions), "lifecycle": "planning_only_x1", "owner": OWNER, "path_count": len(content_paths) + len(exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v4.x1", "x2_paths": []})
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(VALIDATION / "x1-index-manifest.json", {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v681.v4.x1", "source": SOURCE})

    print(json.dumps({"audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"], "maximum_neighbor_score": audit["maximum_neighbor_score"], "proposal_count": len(proposal_records), "startup_failures": len(startup), "status": "X1_PLANNING_ONLY_MATERIALIZED", "written_paths": len(WRITTEN)}, indent=2))


if __name__ == "__main__":
    build()

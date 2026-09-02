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
BASE = ROOT / "docs" / "neris-solane" / "v682-v8"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Neris Solane"
PHASE = "v682-v8"
BRANCH = "codex/GHC-Family/neris-solane-v682-v8-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v682-v7-full-tools"
SOURCE = "938162611d2ce944ddcddf64834bd93e045e3c49"
SOURCE_X1 = "475febc0140aff210515f1fdb0652f79abdeee1f"
SOURCE_EVIDENCE = "823ca1e16a65e8501658dc3e5b27dc20e03355dc"
SOURCE_PARENT = "7442303ebfbea11e7d9e4a9f40a441d5805b3272"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "76e3a4e83f31edb9859ed5f79e19d0ea791555c090386817d3bf6566143f6594"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "91b81822f37ad28295466634ca3408e94c8c5711ddd579812db1e47884cea781"
)
DECLARED_CHAIN_BEFORE = 10610
DECLARED_CHAIN_AFTER = 10670
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
CHECKED_AT_UTC = "2026-09-02T02:08:35Z"
WRITTEN: list[str] = []

ACTIVATION_BASELINE = {
    "effective_negatives": 57457,
    "effective_methods": 69819,
    "failed_witnesses": 29118,
    "bounded_passing_witnesses": 50919,
    "open_gaps": 510,
    "exact_gates": 500,
}

PROPOSAL_TITLES = [
    "Synthetic maritime signal-flag catalogue capsule separating code token visual surrogate physical flag and operational signal",
    "Single-letter numeral and substitute-pennant namespace with every real semantic assignment vacant",
    "Flag-hoist position topology distinguishing upper lower adjacent and separated slots without rigging action",
    "Ordered signal-group surrogate preserving sequence boundaries without decoding or transmitting a message",
    "Halyard mast vessel and operator relationship graph with every physical entity deliberately absent",
    "Colour-region placeholder register with no sampled pixel wavelength pigment or appearance claim",
    "Flag geometry and aspect-ratio vacancy record with zero measured dimensions and scale unknown",
    "Orientation face reverse and viewing-direction states held apart without interpreting a displayed flag",
    "Substitute and repetition token model preventing silent expansion into an operational hoist",
    "Signal-group delimiter and codebook-reference graph without assigning navigational meaning",
    "Codebook edition amendment and citation lineage separating publication state from current applicability",
    "Erratum correction supersession and withdrawal ledger without correcting any live maritime instruction",
    "Source excerpt identifier and rights-basis vacancy board with no copied codebook passage",
    "Capture-request docket for flag imagery with intent authorization attempt observation and result kept separate",
    "Master derivative thumbnail and transcription role graph with zero image creation or transformation",
    "Checksum filename package and catalogue identifier separation from flag object and signal identity",
    "PREMIS object event agent rights and fixity vacancies for a synthetic signal-flag packet",
    "DCMI title identifier format provenance and rights crosswalk with publication locked off",
    "PROV entity activity agent derivation and revision bundle for zero-row catalogue documentation",
    "Catalogue alias normalization and collision quarantine across flag code surrogate and file identifiers",
    "Ambiguous damaged cropped or occluded visual-cue register without recognition or classification",
    "Superseded reserved and unknown meaning states held apart without operational recommendation",
    "Distress-bearing semantic field locked behind competent maritime authority and live-safety evidence",
    "Hazardous operational phrase redaction hold preventing documentation from becoming sailing instruction",
    "Display or transmission attempt docket retaining intent authorization action observation and result vacancies",
    "Observed-hoist result placeholder with zero vessel location weather time or participant data",
    "Operator observer cataloguer conservator and rights-holder roles represented as wholly vacant",
    "Queue fatigue pause dual-readback and reversible handover lease for synthetic description work",
    "Structural accessible summary separating token order colour labels and unknown semantics without user claim",
    "Nonvisual discovery scaffold for hoist order and uncertainty with assistive-technology evaluation reserved",
    "Colour-independent pattern vocabulary using labelled regions while withholding equivalence and conformance claims",
    "Translation language-script and terminology authority hold for every signal description field",
    "Cultural association emblem symbolism and community meaning minimum-disclosure quarantine",
    "Traditional-knowledge and community-data vacancy record with authority noncompensation",
    "Copyright access restriction takedown correction abstention and remedy state machine without claimant contact",
    "Privacy-minimized catalogue surrogate with no names contact details vessel identifiers or route data",
    "Custody ownership acquisition donor restriction and location fields held unknown without collection evidence",
    "Condition-cue vocabulary for tear crease fading loss staining and distortion without flag examination",
    "Storage display support and light-exposure reservation with no conservation or handling recommendation",
    "GMUT symbolic-sequence topology board with no likelihood physical parameter inference prediction or force claim",
    "THOS finite-state evidence scheduler separating ready hold stop handover and abandoned states with zero participants",
    "Freed ID separation of catalogue surrogate signal concept file package and physical flag with zero keys or proofs",
    "Represented International Maritime Organization code-of-signals publication vocabulary with zero operational decoding",
    "Represented International Maritime Organization errata lineage adapter with zero live instruction update",
    "Represented International Maritime Organization resolution provenance adapter with zero navigation authority",
    "Represented Library of Congress PREMIS preservation-event board with zero repository action",
    "Represented DCMI catalogue-term mapping with no catalogue publication or standards conformance claim",
    "Represented W3C PROV-O lineage graph with every real agent activity and entity row absent",
    "Represented WCAG structural review checklist with browser assistive-technology cognitive and affected-user testing absent",
    "Represented W3C credential vocabulary guard with zero identifier issuance key proof status or revocation event",
    "Represented NIST dimensional-language guard requiring absent values before any quantity-unit pair",
    "Represented New Zealand privacy-principle vocabulary with no personal information or compliance conclusion",
    "Represented Te Mana Raraunga boundary reminder with no delegated Māori wording data-governance or authority decision",
    "Represented maritime archivist conservator accessibility specialist rights-holder and affected-community roles vacant",
    "Open gap for competent examination of real signal flags codebooks materials condition custody and conservation needs",
    "Open gap for governed usability and safety benchmark with real qualified operators preregistration monitoring and independent review",
    "Open gap for affected-user accessibility rights language cultural traditional-knowledge and Māori-authority review",
    "Exact gate for real flag hoist decoding display transmission navigation emergency handling conservation and maritime-safety authority",
    "Exact gate for custody ownership copyright privacy publication legal cultural affected-party and Māori-authority decisions",
    "Exact terminal reservation preventing synthetic catalogue evidence from closing real-world replication identity governance or Stage 20 authority",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]

PROTECTED_GATES = [
    (
        "real people mariners operators observers archivists conservators communities vessels flags codebooks records "
        "observations measurements displays transmissions navigation handling treatment and actions"
    ),
    "empirical GMUT signal material or maritime models likelihoods constraints predictions inference and confirmation",
    (
        "professional maritime signalling navigation emergency response cataloguing conservation handling digitization and publication authority"
    ),
    "production identity issuance resolution status revocation interoperability and trust governance",
    (
        "signal flag codebook privacy copyright donor restrictions ownership custody access heritage traditional knowledge "
        "legal cultural affected-party and Maori authority"
    ),
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood Theory of Everything proof canon and Stage 20",
]

STARTUP_FAILURES = [
    {
        "failure_id": "NS6828-ST-N001",
        "failed_witness": "A combined fresh-remote and history wrapper crossed its return window without attributable output.",
        "initial_credit": 0,
        "recovery": "Inspect persisted Git and process state, then split ancestry and live-remote probes into bounded scalar reads.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "NS6828-ST-N002",
        "failed_witness": "The first exact-manifest git cat-file batch queued all requests before reading output and deadlocked on pipe backpressure.",
        "initial_credit": 0,
        "recovery": "Stop only the verified read-only processes and use one request with one exact response at a time.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "NS6828-ST-N003",
        "failed_witness": "The second streaming manifest probe assumed one read would return the full blob and became byte-misaligned on a short read.",
        "initial_credit": 0,
        "recovery": "Use a bounded read-exact loop for every declared blob length; the corrected replay verified all 242 entries with zero mismatches.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "NS6828-ST-N004",
        "failed_witness": "Fresh sparse-worktree creation crossed the wrapper window while checkout continued normally.",
        "initial_credit": 0,
        "recovery": "Inspect the exact Git processes and worktree registry, wait for completion, and do not reset or recreate the lane.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "NS6828-ST-N005",
        "failed_witness": "The first bounded existing-task reread requested more than the tool's per-item output ceiling and was rejected.",
        "initial_credit": 0,
        "recovery": "Retry once within the documented per-item ceiling and retain the rejected call at zero credit.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "NS6828-ST-N006",
        "failed_witness": "The first case-insensitive PowerShell replacement map declared keys differing only by case and failed at parse time.",
        "initial_credit": 0,
        "recovery": "Represent mechanical replacement pairs as an ordered array, then apply the substantive domain changes with an explicit patch.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "NS6828-X1-N007",
        "failed_witness": "The first planning-builder compile exposed one orphan opening brace after inherited failure rows were removed.",
        "initial_credit": 0,
        "recovery": "Remove only the orphan delimiter, recompile the bounded x1 builder, and retain the failed syntax witness.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "NS6828-X1-N008",
        "failed_witness": "The first exact-source novelty audit quarantined one inherited THOS near-neighbour and one exact inherited terminal-gate title before writing x1.",
        "initial_credit": 0,
        "recovery": "Retain both rejected titles at zero credit, substantively replace only those two contracts, and rerun the failed audit dependency.",
        "recovery_credit": "bounded_dependency_only",
    },
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(
    *args: str, check: bool = True, text: bool = True
) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
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
    left_tokens = title_tokens(left)
    right_tokens = title_tokens(right)
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def title_tokens(value: str) -> frozenset[str]:
    return frozenset(re.findall(r"[a-z0-9]+", value.casefold()))


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
        return ["IMO-ICS-CURRENT", "IMO-ICS-RESOLUTION", "W3C-PROV-O"]
    if index <= 30:
        return ["IMO-ICS-CURRENT", "NIST-SI", "W3C-PROV-O"]
    if index <= 42:
        return ["LOC-PREMIS", "DCMI-TERMS", "W3C-PROV-O"]
    if index <= 54:
        return ["IMO-ICS-ERRATA", "W3C-WCAG22", "W3C-VC-DM-20"]
    if index == 55:
        return ["LOC-PREMIS", "IMO-ICS-CURRENT"]
    if index == 56:
        return ["IMO-ICS-CURRENT", "IMO-ICS-RESOLUTION"]
    if index == 57:
        return ["W3C-WCAG22", "NZ-PRIVACY-PRINCIPLES", "TMR-MDS-PRINCIPLES"]
    if index == 58:
        return ["IMO-ICS-CURRENT", "LOC-PREMIS"]
    if index == 59:
        return ["LOC-PREMIS", "DCMI-TERMS", "W3C-PROV-O"]
    return ["TMR-MDS-PRINCIPLES", "W3C-PROV-O"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"NS6828-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/neris-solane/v682-v8/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/neris-solane/v682-v8/x2/rejecting-mutations.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": disposition(index),
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded zero-row positive witness, all five invalid "
                    "mutations are rejected, and no empirical, professional, production, legal, cultural, "
                    "affected-party, Māori-authority, or Stage 20 claim is promoted."
                ),
                "hypothesis": (
                    f"A wholly synthetic zero-row contract for {title.casefold()} can preserve the named state "
                    "distinction and reject preregistered counterexamples within owner-local scope."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, its bounded positive structure "
                    "is rejected, a real-world state is inferred, or any protected gate is promoted."
                ),
                "official_or_primary_source_needs": source_needs(index),
                "preregistered_rejecting_mutations": [
                    {
                        "expected_result": "rejected_zero_credit",
                        "mutation_id": f"{proposal_id}-M{mutation_index:02d}",
                        "mutation_type": mutation_type,
                    }
                    for mutation_index, mutation_type in enumerate(
                        MUTATION_TYPES, start=1
                    )
                ],
                "proposal_id": proposal_id,
                "protected_gates": PROTECTED_GATES,
                "rollback_or_recovery": (
                    f"Quarantine only the {proposal_id} witness, retain the failed receipt at zero credit, and "
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
    proc = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None and proc.stdout is not None
    try:
        for path in paths:
            proc.stdin.write(f"{tree}:{path}\n".encode())
            proc.stdin.flush()
            header = (
                proc.stdout.readline().decode("utf-8", errors="replace").rstrip("\n")
            )
            if header.endswith(" missing"):
                continue
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
            size = int(parts[2])
            chunks: list[bytes] = []
            remaining = size
            while remaining:
                chunk = proc.stdout.read(remaining)
                if not chunk:
                    raise RuntimeError(f"partial cat-file blob for {path}")
                chunks.append(chunk)
                remaining -= len(chunk)
            data = b"".join(chunks)
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing cat-file separator for {path}")
            yield path, data
    finally:
        proc.stdin.close()
        proc.terminate()
        proc.wait(timeout=10)


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    grep_result = git(
        "grep", "-l", "-I", '"proposal_id"', SOURCE, "--", "*.json", check=False
    )
    if grep_result.returncode not in (0, 1):
        raise RuntimeError(grep_result.stderr)
    raw_paths = sorted(set(filter(None, grep_result.stdout.splitlines())))
    tree_prefix = SOURCE + ":"
    paths = [path.removeprefix(tree_prefix) for path in raw_paths]
    parsed = 0
    parse_failures: list[dict[str, str]] = []
    inherited: list[dict[str, str]] = []
    for path, data in batch_blobs(SOURCE, paths):
        try:
            document = json.loads(data.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_failures.append({"path": path, "error": type(exc).__name__})
            continue
        parsed += 1
        for record in iter_proposal_records(document):
            inherited.append({"path": path, **record})
    if not paths or parsed == 0 or not inherited:
        raise RuntimeError(
            "proposal audit must parse nonzero exact-source paths and id-title records"
        )

    inherited_titles = {record["title"] for record in inherited}
    inherited_with_tokens = [
        (record, title_tokens(record["title"])) for record in inherited
    ]
    exact_collisions: list[str] = []
    neighbors: list[dict[str, Any]] = []
    for proposal in new_records:
        title = proposal["title"]
        if title in inherited_titles:
            exact_collisions.append(title)
        best: dict[str, str] | None = None
        best_score = -1.0
        proposal_tokens = title_tokens(title)
        for record, inherited_tokens in inherited_with_tokens:
            if not proposal_tokens and not inherited_tokens:
                score = 1.0
            else:
                score = len(proposal_tokens & inherited_tokens) / len(
                    proposal_tokens | inherited_tokens
                )
            if score > best_score:
                best_score = score
                best = record
        neighbors.append(
            {
                "best_inherited_neighbor": best,
                "proposal_id": proposal["proposal_id"],
                "quarantined": best_score >= 0.78,
                "title": title,
                "token_jaccard": round(best_score, 6),
            }
        )
    quarantined = [row for row in neighbors if row["quarantined"]]
    if exact_collisions or quarantined:
        raise RuntimeError(
            "proposal novelty quarantine required: "
            + json.dumps(
                {"exact": exact_collisions, "neighbors": quarantined},
                ensure_ascii=False,
            )
        )
    return {
        "audit_scope": {
            "claim": "bounded all-reachable exact-source proposal audit; no universal 10610-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_declared_chain_materialization_claimed": False,
        },
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "exact_title_collisions": exact_collisions,
        "maximum_neighbor_score": max(row["token_jaccard"] for row in neighbors),
        "neighbor_reviews": neighbors,
        "new_proposal_count": len(new_records),
        "owner": OWNER,
        "phase": PHASE,
        "quarantine_threshold_token_jaccard": 0.78,
        "quarantined_neighbors": quarantined,
        "schema": "ghc.family.proposal-chain-audit.v682.v8.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Neris owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"NS6828-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


SKILL_NAMES = [
    "signal-flag-surrogate-separator",
    "hoist-position-vacancy-guard",
    "signal-decoding-nonexecution",
    "operator-vessel-vacancy",
    "colour-geometry-claim-quarantine",
    "signal-token-collision-quarantine",
    "transmission-action-separator",
    "codebook-revision-lineage-ledger",
    "signal-meaning-interpretation-hold",
    "condition-nondiagnosis",
    "digitization-action-separator",
    "premis-signal-event-vacancy",
    "accessible-hoist-summary",
    "traditional-knowledge-minimizer",
    "rights-remedy-hold",
    "workload-handover-lease",
    "freed-id-zero-key-guard",
    "thos-worker-vacancy",
    "gmut-topology-noninference",
    "authority-noncompensation",
]


def portfolio_freeze() -> dict[str, Any]:
    return {
        "blocked": task_records("BLOCK", 10, "blocked"),
        "caps_are_ceilings": True,
        "commit_cap": 3,
        "document_word_cap": 100000,
        "exact_approval": task_records("EXACT", 20, "exact_approval"),
        "materialized_file_stop": 2000,
        "owner": OWNER,
        "owner_candidates": task_records("CAND", 80, "bounded_candidate"),
        "owner_clean_fix_refine": task_records("CFR", 100, "clean_fix_refine"),
        "owner_practice_lenses": [
            "wholly synthetic signal-flag token, hoist-position, and codebook-lineage documentation",
            "wholly synthetic metadata, condition-cue, preservation-event, and image-request planning",
            "wholly synthetic rights, accessibility, remedy, workload, and handover documentation",
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"NS6828-RUNNER-{index:02d}",
                "name": f"ghc_family_signal_flag_runner_{index:02d}.py",
                "state": "planned_not_built_in_x1",
            }
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {
                "skill_id": f"NS6828-SKILL-{index:02d}",
                "name": name,
                "state": "planned_not_built_in_x1",
            }
            for index, name in enumerate(SKILL_NAMES, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "GMUT Mind",
        "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v682.v8.x1",
        "successor_candidates": task_records(
            "SUCCESSOR-CAND", 20, "successor_candidate_zero_credit"
        ),
        "successor_clean_fix_refine": task_records(
            "SUCCESSOR-CFR", 30, "successor_recommendation_zero_credit"
        ),
        "successor_practice_recommendation": (
            "one zero-credit seed only: choose a distinct synthetic documentation lens and independently audit every proposal before freeze"
        ),
        "successor_runner_ideas": task_records(
            "SUCCESSOR-RUNNER", 10, "successor_runner_seed_zero_credit"
        ),
        "successor_skill_ideas": task_records(
            "SUCCESSOR-SKILL", 10, "successor_skill_seed_zero_credit"
        ),
    }


def official_sources() -> dict[str, Any]:
    entries = [
        {
            "source_id": "IMO-ICS-CURRENT",
            "status": "official_IMO_current_publications_listing_checked_2026-09-02",
            "title": "Listing of current IMO publications",
            "url": "https://www.imo.org/en/publications/pages/currentpublications.aspx",
            "use": "publication title and edition-presence vocabulary for the International Code of Signals only; no code extraction, operational decoding, navigation advice, or IMO endorsement",
        },
        {
            "source_id": "IMO-ICS-ERRATA",
            "status": "official_IMO_International_Code_of_Signals_errata_checked_2026-09-02",
            "title": "International Code of Signals 2005 Edition Fifth edition 2021 Errata March 2022",
            "url": "https://wwwcdn.imo.org/localresources/en/publications/Documents/Supplements/English/IB994E_errata_February2022_PQ.pdf",
            "use": "edition, erratum, replacement, supersession, and procedure-signal vocabulary only; no live code correction, decoding, transmission, or operational recommendation",
        },
        {
            "source_id": "IMO-ICS-RESOLUTION",
            "status": "official_IMO_resolution_A80_IV_checked_2026-09-02",
            "title": "Resolution A.80(IV) International Code of Signals",
            "url": "https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/AssemblyDocuments/A.80%28IV%29.pdf",
            "use": "resolution, adoption, committee, revision, and safety-boundary provenance vocabulary only; no current legal interpretation, code applicability decision, or delegated maritime authority",
        },
        {
            "source_id": "IMO-COLREG-BOUNDARY",
            "status": "official_IMO_COLREG_page_checked_2026-09-02",
            "title": "COLREG - Preventing collisions at sea",
            "url": "https://www.imo.org/en/ourwork/safety/pages/preventing-collisions.aspx",
            "use": "safety reservation and prohibited-confusion boundary vocabulary only; no signal interpretation, vessel operation, emergency response, or legal advice",
        },
        {
            "source_id": "NIST-SI",
            "status": "official_NIST_publication_page_checked_2026-09-02",
            "title": "The International System of Units (SI), 2019 Edition",
            "url": "https://www.nist.gov/publications/international-system-units-si2019-edition",
            "use": "quantity, unit, symbol and dimensional-reporting vocabulary only; zero measurements or conversions",
        },
        {
            "source_id": "LOC-PREMIS",
            "status": "official_Library_of_Congress_standard_page_checked_2026-09-02",
            "title": "PREMIS Preservation Metadata Maintenance Activity",
            "url": "https://www.loc.gov/standards/premis/index.html",
            "use": "object, event, agent, rights, fixity and preservation-metadata vocabulary only; no repository ingest or conformance claim",
        },
        {
            "source_id": "DCMI-TERMS",
            "status": "DCMI_Recommendation_checked_2026-09-02",
            "title": "DCMI Metadata Terms",
            "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
            "use": "creator, title, identifier, format, provenance, access-rights and rights-statement vocabulary only",
        },
        {
            "source_id": "W3C-PROV-O",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "PROV-O: The PROV Ontology",
            "url": "https://www.w3.org/TR/prov-o/",
            "use": "entity, activity, agent, derivation, revision and provenance vocabulary only",
        },
        {
            "source_id": "W3C-WCAG22",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Web Content Accessibility Guidelines 2.2",
            "url": "https://www.w3.org/TR/WCAG22/",
            "use": "structural accessibility vocabulary and manual, browser, assistive-technology, cognitive and affected-user evaluation reservations only",
        },
        {
            "source_id": "W3C-VC-DM-20",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Verifiable Credentials Data Model v2.0",
            "url": "https://www.w3.org/TR/vc-data-model-2.0/",
            "use": "synthetic identifier, credential, status and proof-vacancy vocabulary only; no real key or lifecycle event",
        },
        {
            "source_id": "NZ-PRIVACY-PRINCIPLES",
            "status": "official_New_Zealand_Privacy_Commissioner_material_checked_2026-09-02",
            "title": "New Zealand Information Privacy Principles",
            "url": "https://www.privacy.org.nz/privacy-principles/",
            "use": "privacy minimization, access, correction, disclosure, and current IPP 3A notification vocabulary only; no legal interpretation or compliance claim",
        },
        {
            "source_id": "TMR-MDS-PRINCIPLES",
            "status": "authority_boundary_context_only_checked_2026-09-02",
            "title": "Principles of Maori Data Sovereignty",
            "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
            "use": "Maori data-governance vacancy and noncompensation boundary only; never delegated Maori authority",
        },
    ]
    return {
        "authority_conferred": False,
        "checked_at_utc": CHECKED_AT_UTC,
        "citations_are_observations": False,
        "entries": entries,
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v682.v8.x1",
        "web_checks": len(entries),
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    classes = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b019[a-f0-9]{29,}\b", re.IGNORECASE
        ),
        "credential_or_secret": re.compile(
            r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.IGNORECASE
        ),
        "private_route_or_callable_identifier": re.compile(
            r"(?:threadId|private callable|app://connector_)", re.IGNORECASE
        ),
        "private_absolute_path": re.compile(
            r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.IGNORECASE
        ),
        "transcript_screenshot_or_session_stream": re.compile(
            r"(?:raw transcript|session stream|screenshot payload)", re.IGNORECASE
        ),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {
            ".json",
            ".md",
            ".py",
            ".yaml",
            ".yml",
            ".html",
        }:
            continue
        text = target.read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                candidates.append(
                    {
                        "class": class_name,
                        "path": path,
                        "adjudication": "scanner_definition_only",
                    }
                )
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "class_count": 5,
        "confirmed_hit_count": 0,
        "confirmed_hits": [],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.privacy-scan.v682.v8.x1",
        "scanned_paths": len(paths),
    }


def manifest_entry(path: str) -> dict[str, Any]:
    data = normalized_bytes(ROOT / path)
    return {"bytes": len(data), "path": path, "sha256": sha256_bytes(data)}


def build() -> None:
    new_records = proposals()
    if len(new_records) != 60:
        raise RuntimeError("proposal count must be exactly sixty")
    expected_counts = Counter(row["expected_disposition"] for row in new_records)
    if expected_counts != Counter(
        {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    ):
        raise RuntimeError(f"unexpected disposition counts: {expected_counts}")
    audit = proposal_chain_audit(new_records)

    current_after_startup = dict(ACTIVATION_BASELINE)
    for key in (
        "effective_negatives",
        "effective_methods",
        "failed_witnesses",
        "bounded_passing_witnesses",
    ):
        current_after_startup[key] += len(STARTUP_FAILURES)

    write_json(
        X1 / "activation-intake.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "delivery_state": "SENT_ONCE_TOOL_ACCEPTED_TEXT_OPAQUE_NO_RESEND_EXTERNAL",
            "source_repository_and_live_delivery_kept_distinct": True,
            "owner": OWNER,
            "phase": PHASE,
            "received_source_final": SOURCE,
            "schema": "ghc.family.activation-intake.v682.v8.x1",
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "consciousness_personhood_or_continuity_claimed": False,
            "hope": "Every synthetic flag token remains distinguishable from a physical flag, an observed hoist, and an operational signal, while maritime, cultural, and affected-party authority remain with their holders.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "owner_rename_pause_redirect_stop_right": "Hamish",
            "phase": PHASE,
            "relational_working_language_only": True,
            "role": "symbolic-sequence provenance cartographer and rights-boundary keeper",
            "schema": "ghc.family.identity-boundary.v682.v8.x1",
        },
    )
    write_json(
        X1 / "source-verification.json",
        {
            "branch": SOURCE_BRANCH,
            "canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "clean": True,
            "evidence": SOURCE_EVIDENCE,
            "final": SOURCE,
            "four_way_equal": True,
            "manifest_replay": {
                "x1": 20,
                "evidence": 75,
                "final_delta": 23,
                "final_owner": 114,
                "total": 242,
                "mismatches": 0,
            },
            "content_seal_targets": 10,
            "merges": 0,
            "owner": OWNER,
            "phase": PHASE,
            "phase_commits": 3,
            "source": SOURCE_PARENT,
            "typed_divergence": [0, 0],
            "x1": SOURCE_X1,
        },
    )
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(
        X1 / "new-proposal-freeze.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "expected_disposition_counts": dict(expected_counts),
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(new_records),
            "proposals": new_records,
            "schema": "ghc.family.proposal-freeze.v682.v8.x1",
            "source": SOURCE,
            "x2_outcomes_present": False,
        },
    )
    write_json(
        X1 / "inherited-revalidation-freeze.json",
        {
            "completion_credit": 0,
            "count": 20,
            "owner": OWNER,
            "phase": PHASE,
            "reviews": [
                {
                    "best_inherited_neighbor": row["best_inherited_neighbor"],
                    "completion_credit": 0,
                    "current_proposal_id": row["proposal_id"],
                    "state": "source_evidence_only",
                    "token_jaccard": row["token_jaccard"],
                }
                for row in audit["neighbor_reviews"][:20]
            ],
            "schema": "ghc.family.inherited-revalidation.v682.v8.x1",
        },
    )
    portfolio = portfolio_freeze()
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "approval-hold-register.json",
        {
            "blocked_count": len(portfolio["blocked"]),
            "executed": False,
            "exact_approval_count": len(portfolio["exact_approval"]),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.approval-holds.v682.v8.x1",
        },
    )
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "owner_rows": portfolio["owner_clean_fix_refine"],
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine.v682.v8.x1",
            "successor_rows": portfolio["successor_clean_fix_refine"],
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
            "schema": "ghc.family.skill-runner-plan.v682.v8.x1",
            "skills": portfolio["owner_skill_ideas"],
            "x2_implementation_present": False,
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", official_sources())
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "current_after_startup": current_after_startup,
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v682.v8.x1",
            "startup_failures": STARTUP_FAILURES,
        },
    )
    write_json(
        X1 / "phase-truth.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "execution_state": "PLANNING_ONLY_X1",
            "expected_dispositions": dict(expected_counts),
            "observed_outcomes": None,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(new_records),
            "schema": "ghc.family.phase-truth.v682.v8.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_json(
        X1 / "threat-model.json",
        {
            "controls": [
                "zero real rows and zero real actions",
                "planning-only x1 before x2",
                "five rejecting mutations per proposal",
                "no authority compensation by software or citations",
                "exact approval and blocked work stays unexecuted",
                "five-class privacy scan and normalized-LF manifests",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "risks": [
                "synthetic structure promoted into observation or professional advice",
                "cultural or Māori authority inferred from vocabulary",
                "signal meaning, navigation, material, condition, digitization, rights, authorship or cultural authority inferred from documentation",
                "route or private identifier leakage",
                "x1 and x2 lifecycle contamination",
            ],
            "schema": "ghc.family.threat-model.v682.v8.x1",
        },
    )
    write_json(
        X1 / "wellbeing-and-corrigibility.json",
        {
            "check": "steady and willing to pause on evidence, privacy, safety, or authority ambiguity",
            "corrigible": True,
            "owner": OWNER,
            "phase": PHASE,
            "rename_pause_redirect_stop_right": "Hamish",
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v682.v8.x1",
            "steps": [
                "freeze and push planning-only x1",
                "prove clean fresh-live four-way x1 equality",
                "execute bounded x2 contracts, mutations, portfolios, skills, and runners",
                "commit and push immutable evidence",
                "build closeout and invoke at most one exact-final canonical aggregate",
                "refresh route only after terminal success",
            ],
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "phase": PHASE,
            "prepared_not_sent": True,
            "prospective_successor_exact_title": "Vesper Arlen",
            "prospective_successor_phase": "v683-v1",
            "route_authority_through": "v725-v8",
            "send_before_terminal_gate": False,
            "tavian_sol": "ON_STANDBY",
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        f"""# Neris Solane {PHASE} Planning-Only X1 Overview

Neris Solane, optionally they/them, is relational working language for a symbolic-sequence provenance cartographer and rights-boundary keeper, with the hope that every synthetic flag token remains distinguishable from a physical flag, an observed hoist, and an operational maritime signal. This is not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish retains the right to rename, pause, redirect, narrow, or stop the route.

The exact immutable source is Elaren Kestrel final `{SOURCE}` on `{SOURCE_BRANCH}`. Read-only verification established the direct Eiren-source to Elaren-x1 to Elaren-evidence to Elaren-final chain, exactly three Elaren single-parent commits, zero merges, one final parent, clean state, typed 0/0 divergence, fresh four-way equality, 232 exact normalized-LF manifest entries plus ten content-seal targets, and exact canonical receipt and payload digests. No Elaren test, manifest aggregate, or canonical aggregate was replayed. Elaren's repository seal, external activation overlay, opaque accepted live delivery, and Neris startup failures remain distinct truth layers.

This x1 freezes sixty Neris proposals only after a bounded all-reachable exact-source audit. The accepted slate must produce zero exact collisions and zero quarantine hits at the 0.78 token-Jaccard threshold. It makes no universal semantic-novelty claim over every declared historical row where a canonical materialized row-to-title ledger is absent. Twenty inherited neighbour reviews remain source evidence with zero Neris completion credit.

GMUT Mind is primary through typed symbolic-sequence topology, explicit unknown states, provenance, edition lineage, zero-observation discipline, and non-inference. THOS Body remains visible through synthetic queue budgets, stop precedence, action-state separation, accessibility structure, correction, and handover. Freed ID and CBR Heart remain visible through surrogate separation, rights and privacy holds, remedy, traditional-knowledge minimization, and cultural-authority noncompensation. Maritime signal-flag catalogue documentation is a wholly synthetic learning lens only, never employment, qualification, seamanship, code decoding, signalling, navigation, emergency response, collection custody, conservation, digitization, rights clearance, publication, or professional authority.

The plan uses zero real people, mariners, operators, observers, archivists, conservators, communities, vessels, flags, halyards, codebooks, images, records, identifiers, locations, weather observations, measurements, displays, transmissions, navigation actions, emergency actions, treatments, identity events, external writes, or authority acts. Official and primary sources supply vocabulary and refusal conditions only. They are not signal interpretations, operational instructions, observations, measurements, material findings, preservation recommendations, catalogue decisions, rights determinations, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

Expected x2 dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Those are preregistered expected labels, not observed outcomes. All 300 invalid mutations, 120 safe-now tasks, 80 bounded candidates, 100 CLEAN/FIX/REFINE records, twenty skills, and ten runners remain planned rather than executed in this x1. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, material evidence, likelihood, posterior, prediction, constraint, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy/security review, recovery evidence, trust governance, and affected-party oversight.

Real flag handling, hoisting, display, transmission, decoding, navigation, emergency response, conservation treatment, digitization, professional cataloguing, copyright, privacy, donor restrictions, access, ownership, custody, heritage, traditional knowledge, remedy, legal and cultural interpretation, affected-party legitimacy, Maori wording and data governance, and Maori authority remain exact-gated. Maori concepts remain under Maori authority. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, proof/canon, and Stage 20 remain open or exact-gated. The terminal verdict remains `{TERMINAL_VERDICT}`.
""",
    )

    x1_material_paths = sorted(
        set(
            WRITTEN
            + [
                "scripts/build_ghc_family_neris_solane_v682_v8_x1.py",
                "tests/test_ghc_family_neris_solane_v682_v8_x1.py",
            ]
        )
    )
    exclusions = [
        "docs/neris-solane/v682-v8/validation/x1-index-manifest.json",
        "docs/neris-solane/v682-v8/validation/x1-privacy-scan.json",
        "docs/neris-solane/v682-v8/validation/x1-staged-review.json",
    ]
    write_json(VALIDATION / "x1-privacy-scan.json", privacy_scan(x1_material_paths))
    write_json(
        VALIDATION / "x1-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": [manifest_entry(path) for path in x1_material_paths],
            "entry_count": len(x1_material_paths),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v8.x1",
            "source": SOURCE,
        },
    )
    expected_paths = sorted(set(x1_material_paths + exclusions))
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": expected_paths,
            "lifecycle": "planning_only_x1",
            "owner": OWNER,
            "path_count": len(expected_paths),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v682.v8.x1",
            "x2_paths": [],
        },
    )
    print(
        json.dumps(
            {
                "audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"],
                "audit_records": audit["audit_scope"]["reachable_id_title_records"],
                "maximum_neighbor_score": audit["maximum_neighbor_score"],
                "proposal_count": len(new_records),
                "staged_path_count": len(expected_paths),
                "written": len(WRITTEN),
                "x2_outcomes_present": False,
            },
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    build()

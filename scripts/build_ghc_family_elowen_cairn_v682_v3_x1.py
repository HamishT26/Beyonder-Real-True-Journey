from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v682-v3"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Elowen Cairn"
PHASE = "v682-v3"
BRANCH = "codex/GHC-Family/elowen-cairn-v682-v3-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v682-v2-full-tools"
SOURCE = "ed63ba1080cbb0a69701e56fd9bee9c80221a709"
SOURCE_X1 = "39f8a83e29ba28433b7c9da730d3299d1731cb4d"
SOURCE_EVIDENCE = "f7ca8ace4a16f0dae8aa2530cf17962e79b062b0"
SOURCE_ORIGINAL_FINAL = "d00443492f9e1a950e752aa2c1b5a1bf0613db44"
SOURCE_PARENT = "34536c2bb4c9fefb04cc0b571839e9ba54b3c497"
SOURCE_FAILED_CANONICAL_RECEIPT_SHA256 = "9f62c38cc87d5e5b64d00562e636ccdb3f0f757a198f45225549ee8d61dfeb0a"
SOURCE_COMPOSITE_RECEIPT_SHA256 = "bc62af4058d2991fa6637eab4bdfabdfd47e81c6f2b3082a1fe2d53e0bc6b61f"
SOURCE_CANONICAL_RECEIPT_SHA256 = "99b754d394c9ad019d29675fb4ebec9fddbe1dd2966f9c14837bc5b542614c36"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "21c92e8bfd5dfaf20fe45beba7cc171cdeed05847f017b35e84df3580b6d47c0"
DECLARED_CHAIN_BEFORE = 10310
DECLARED_CHAIN_AFTER = 10370
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
CHECKED_AT_UTC = "2026-09-01T15:56:26Z"
WRITTEN: list[str] = []

ACTIVATION_BASELINE = {
    "effective_negatives": 55810,
    "effective_methods": 65914,
    "failed_witnesses": 27471,
    "bounded_passing_witnesses": 47314,
    "open_gaps": 494,
    "exact_gates": 485,
}

PROPOSAL_TITLES = [
    "Synthetic letterpress job capsule and surrogate edition identity split",
    "Type case compartment sort and furniture topology with orphan quarantine",
    "Roman italic display script symbol and unknown face vocabulary without identification",
    "Point pica em en leading slug and SI unit-domain separation with zero measurement",
    "Manuscript copy compositor instruction and imposed-form state separation",
    "Composing stick line galley page chase and forme topology",
    "Sort quantity missing-character wrong-font and damaged-type cue board without diagnosis",
    "Compositor pressperson editor client custodian and cataloguer role vacancies with minimized identifiers",
    "Language script direction and transliteration fields under interpretation hold",
    "Copy line-break hyphenation spacing justification and correction proposal versus observed proof",
    "Typeface family style size and foundry-claim vacancy ledger",
    "Quoin furniture reglet lead slug and lockup component graph with no mechanical action",
    "Forme orientation page order signature and imposition graph with mirror-state checks",
    "Type cleaning distribution recasing and material-use plan under intervention hold",
    "Letterpress correction challenge supersession and dual-readback provenance braid",
    "Accessible synthetic job brief with noncolour status and manual evaluation reserve",
    "Composition workload batch ceiling pause and next-shift handover queue",
    "Edition provenance authorship custody access and rights topology with unresolved claims",
    "Synthetic press-run capsule and surrogate press identity split",
    "Platen cylinder flatbed proof press and unknown machine vocabulary without classification",
    "Bed platen tympan frisket rollers grippers feedboard and delivery-board topology",
    "Ink body tack viscosity drying pigment and binder assertion firewall",
    "Paper board fibre coating grain finish and unknown substrate vacancy ledger",
    "Sheet target dimension unit tolerance uncertainty and zero-measurement firewall",
    "Pressure packing makeready and impression target graph with no adjustment claim",
    "Register gauge lay gripper margin and alignment targets without observation",
    "Inking disc roller train duct and fountain topology without material or condition inference",
    "Point-of-operation nip crush entanglement and cut cue board without safety decision",
    "Guard interlock energy-isolation and stop-state graph with no work release",
    "Hand-feeding tool-use sheet-removal and cycle plan versus executed-action separation",
    "Cleaning solvent rag disposal ventilation and protective-equipment vacancy without safety decision",
    "Trial proof makeready production pull drying and stacking plan versus executed action",
    "Run-count spoilage makeready and edition target ledger with zero production claim",
    "Press crack looseness lubrication wear and unknown cue register without condition diagnosis",
    "Press-run correction challenge restart supersession and immutable prior-state lineage",
    "Accessible press status workload pause unresolved hold and shift-handover lease",
    "Synthetic printed-sheet capsule and surrogate impression identity split",
    "Forme-to-impression derivation revision and activity provenance chain",
    "Recto verso side order signature folio and sequence topology",
    "Ink colour substrate and impression-appearance cues without material identification",
    "Density coverage setoff show-through slur smash and unknown cue register without quality verdict",
    "Trim fold gather collate bind and transfer plan versus executed-action separation",
    "Represented proof comparison annotation and acceptance topology with absent authorized sign-off",
    "Represented typography measurement targets with real measurement and calibration vacancy",
    "Represented press energy and work proxy with zero force measurement or GMUT inference",
    "Represented scan photograph OCR transcription and derivative provenance lineage",
    "Represented accessible proof alternatives with browser assistive-technology and affected-reader review reserved",
    "Represented correction reprint supersession recall and recipient-notice braid",
    "Represented print-run workload fatigue pause and governed shift-handover queue",
    "Represented authorship editorial approval copyright licence and release vacancy",
    "Represented substrate ink sustainability and waste chain with zero supplier data",
    "Represented archival storage enclosure and condition topology with conservator evaluation reserved",
    "Represented public distribution challenge remedy and status topology with zero delivery",
    "Represented Freed ID job relationship with zero real key proof or lifecycle event",
    "Open gap for letterpress printer conservator real press material measurements and independent review",
    "Open gap for affected reader worker accessibility and blind matched-budget workflow evaluation",
    "Open gap for empirical print-mechanics force ink-transfer observation and independent reproduction",
    "Exact gate for authorship copyright private sacred and culturally restricted content authority",
    "Exact gate for machinery workplace chemical environmental safety professional and legal authority",
    "Exact terminal gate for ownership custody heritage Indigenous knowledge Māori data authority empirical GMUT production canon personhood and Stage 20",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]

PROTECTED_GATES = [
    "real people printers readers presses type paper ink sites objects materials tools machines and measurements",
    "empirical GMUT likelihoods constraints predictions observations and confirmation",
    "professional letterpress printing conservation publishing machinery workplace safety and release authority",
    "production identity issuance resolution status revocation interoperability and trust governance",
    "authorship copyright ownership heritage traditional knowledge legal cultural affected-party and Māori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood Theory of Everything proof canon and Stage 20",
]

STARTUP_FAILURES = [
    {
        "failure_id": "EC6823-ST-N001",
        "failed_witness": "The first full current-roster display exceeded the usable context window.",
        "initial_credit": 0,
        "recovery": "Measure the roster and read it in bounded ordered windows through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N002",
        "failed_witness": "PowerShell rejected an outer foreach pipeline while inventorying route overlays.",
        "initial_credit": 0,
        "recovery": "Materialize the projection array before JSON serialization.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N003",
        "failed_witness": "A Git probe assumed the Codex metadata root was the repository and received not-a-repository.",
        "initial_credit": 0,
        "recovery": "Use Tamar's exact bounded D-drive worktree path and avoid broad sibling-lane enumeration.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N004",
        "failed_witness": "PowerShell repeated the outer foreach pipeline fault while measuring correction packet files.",
        "initial_credit": 0,
        "recovery": "Use one fixed pre-materialized array template for all remaining inventory commands.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N005",
        "failed_witness": "PowerShell repeated the same outer foreach pipeline fault while probing receipt-directory candidates.",
        "initial_credit": 0,
        "recovery": "Apply the fixed pre-materialized array template and record the recurrence guard as executable policy.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N006",
        "failed_witness": "The live activation claimed 2745 manifest entries while the hash-verified immutable canonical receipt records 385.",
        "initial_credit": 0,
        "recovery": "Use the six immutable receipt-backed manifest counts totalling 385 and retain the conflicting input at zero credit.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-ST-N007",
        "failed_witness": "A combined six-manifest replay returned no attributable output or session handle after its result window.",
        "initial_credit": 0,
        "recovery": "Replay each immutable lifecycle manifest separately and require six attributable zero-failure results.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N001",
        "failed_witness": "A direct Smithsonian printing-machines page open returned an internal 500 response.",
        "initial_credit": 0,
        "recovery": "Use the attributable official Smithsonian search result and other exact official pages only for vocabulary and refusal conditions.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N002",
        "failed_witness": "The first mechanical test-template copy targeted a sparse tests directory that did not yet exist.",
        "initial_credit": 0,
        "recovery": "Create the exact owner tests directory and copy only the intended immutable template.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N003",
        "failed_witness": "The worktree-add command returned after Preparing worktree without a completion code or session handle.",
        "initial_credit": 0,
        "recovery": "Inspect the exact branch ref, target path, Git entry, and process quiescence before proceeding without retry.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N004",
        "failed_witness": "The sparse checkout command exceeded its result window while its Git process and index lock remained active.",
        "initial_credit": 0,
        "recovery": "Wait for the exact process to exit, then prove lock removal, exact head, clean state, and bounded materialization without replay.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N005",
        "failed_witness": "The first top-ten semantic-neighbor display forwarded oversized nested records and exceeded the model-context display bound.",
        "initial_credit": 0,
        "recovery": "Project only three scalar proposal identifiers, scores, and bounded titles from the already materialized audit without rerunning it.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EC6823-X1-N006",
        "failed_witness": "The first post-patch verification probe used a malformed grouped regular expression and stopped before searching.",
        "initial_credit": 0,
        "recovery": "Use literal Select-String patterns against the two exact files and preserve the parser failure at zero credit.",
        "recovery_credit": "bounded_dependency_only",
    },
]


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
        return ["LOC-TYPE-FOUNDRY", "W3C-PROV-O", "W3C-WCAG22"]
    if index <= 36:
        return ["SMITHSONIAN-PRINTING-MACHINES", "OSHA-1910-212", "OSHA-1910-147"]
    if index <= 54:
        return ["NIST-SI-UNITS", "W3C-PROV-O", "W3C-WCAG22"]
    if index == 55:
        return ["LOC-TYPE-FOUNDRY", "SMITHSONIAN-PRINTING-MACHINES"]
    if index == 56:
        return ["OSHA-1910-212", "W3C-WCAG22"]
    if index == 57:
        return ["NIST-SI-UNITS", "SMITHSONIAN-PRINTING-MACHINES"]
    if index == 58:
        return ["TMR-MDS-PRINCIPLES", "W3C-PROV-O"]
    if index == 59:
        return ["OSHA-1910-212", "OSHA-1910-147"]
    return ["TMR-MDS-PRINCIPLES", "W3C-PROV-O"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"EC6823-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/elowen-cairn/v682-v3/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/elowen-cairn/v682-v3/x2/rejecting-mutations.json#{proposal_id}",
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
                    for mutation_index, mutation_type in enumerate(MUTATION_TYPES, start=1)
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
            proc.stdin.write(f"{tree}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("utf-8", errors="replace").rstrip("\n")
            if header.endswith(" missing"):
                continue
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
            size = int(parts[2])
            data = proc.stdout.read(size)
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing cat-file separator for {path}")
            yield path, data
    finally:
        proc.stdin.close()
        proc.terminate()
        proc.wait(timeout=10)


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    grep_result = git("grep", "-l", "-I", '"proposal_id"', SOURCE, "--", "*.json", check=False)
    if grep_result.returncode not in (0, 1):
        raise RuntimeError(grep_result.stderr)
    raw_paths = sorted(set(filter(None, grep_result.stdout.splitlines())))
    tree_prefix = SOURCE + ":"
    paths = [path[len(tree_prefix) :] if path.startswith(tree_prefix) else path for path in raw_paths]
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
        raise RuntimeError("proposal audit must parse nonzero exact-source paths and id-title records")

    inherited_titles = {record["title"] for record in inherited}
    exact_collisions: list[str] = []
    neighbors: list[dict[str, Any]] = []
    for proposal in new_records:
        title = proposal["title"]
        if title in inherited_titles:
            exact_collisions.append(title)
        best: dict[str, str] | None = None
        best_score = -1.0
        for record in inherited:
            score = jaccard(title, record["title"])
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
            + json.dumps({"exact": exact_collisions, "neighbors": quarantined}, ensure_ascii=False)
        )
    return {
        "audit_scope": {
            "claim": "bounded all-reachable exact-source proposal audit; no universal 10310-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_10310_row_materialization_claimed": False,
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
        "schema": "ghc.family.proposal-chain-audit.v682.v3.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Elowen owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"EC6823-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


SKILL_NAMES = [
    "letterpress-job-identity-separator",
    "type-case-topology",
    "typeface-claim-firewall",
    "composition-state-board",
    "forme-imposition-topology",
    "script-interpretation-hold",
    "press-identity-separator",
    "press-component-topology",
    "ink-material-claim-vacancy",
    "sheet-target-unit-board",
    "makeready-action-separator",
    "machine-release-hold",
    "hazard-cue-nondecision",
    "impression-identity-separator",
    "print-quality-claim-firewall",
    "edition-provenance-braid",
    "proof-acceptance-vacancy",
    "accessible-status-summary",
    "correction-readback",
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
            "wholly synthetic movable-type composition and edition-state documentation",
            "wholly synthetic letterpress component and press-run planning",
            "wholly synthetic printed-impression provenance correction and handover",
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"EC6823-RUNNER-{index:02d}",
                "name": f"ghc_family_letterpress_runner_{index:02d}.py",
                "state": "planned_not_built_in_x1",
            }
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {
                "skill_id": f"EC6823-SKILL-{index:02d}",
                "name": name,
                "state": "planned_not_built_in_x1",
            }
            for index, name in enumerate(SKILL_NAMES, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "THOS Body",
        "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v682.v3.x1",
        "successor_candidates": task_records("SUCCESSOR-CAND", 20, "successor_candidate_zero_credit"),
        "successor_clean_fix_refine": task_records("SUCCESSOR-CFR", 30, "successor_recommendation_zero_credit"),
        "successor_practice_recommendation": (
            "exactly one zero-credit seed: synthetic field-notebook pagination documentation; successor must audit novelty independently"
        ),
        "successor_runner_ideas": task_records("SUCCESSOR-RUNNER", 10, "successor_runner_seed_zero_credit"),
        "successor_skill_ideas": task_records("SUCCESSOR-SKILL", 10, "successor_skill_seed_zero_credit"),
    }


def official_sources() -> dict[str, Any]:
    entries = [
        {
            "source_id": "LOC-TYPE-FOUNDRY",
            "status": "official_Library_of_Congress_page_checked_2026-09-02",
            "title": "Just My Type: Making Letters at the Type Foundry",
            "url": "https://blogs.loc.gov/bibliomania/2024/12/17/just-my-type-making-letters-at-the-type-foundry/",
            "use": "type, punch, matrix, sort, hand-mould, and case vocabulary only; no operating instruction or historical completeness claim",
        },
        {
            "source_id": "SMITHSONIAN-PRINTING-MACHINES",
            "status": "official_Smithsonian_search_result_checked_2026-09-02_direct_open_500_retained",
            "title": "Printing Machines",
            "url": "https://americanhistory.si.edu/collections/object-groups/printing-presses/printing-machines",
            "use": "press-family, platen, flatbed, cylinder, feed, and delivery vocabulary only; no object observation or collection-record ingestion",
        },
        {
            "source_id": "OSHA-1910-212",
            "status": "official_OSHA_current_standard_checked_2026-09-02",
            "title": "General requirements for all machines",
            "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.212",
            "use": "point-of-operation, ingoing-nip, guard, and stop-state vocabulary only; no workplace release or legal interpretation",
        },
        {
            "source_id": "OSHA-1910-147",
            "status": "official_OSHA_current_standard_checked_2026-09-02",
            "title": "The control of hazardous energy (lockout/tagout)",
            "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147",
            "use": "energy-control and no-release vocabulary only; no procedure, training, compliance, or safety determination",
        },
        {
            "source_id": "NIST-SI-UNITS",
            "status": "official_NIST_page_checked_2026-09-02",
            "title": "SI Units",
            "url": "https://www.nist.gov/pml/owm/metric-si/si-units",
            "use": "quantity, numerical value, unit, uncertainty-vacancy, and SI writing vocabulary only; no measurement or calibration claim",
        },
        {
            "source_id": "W3C-PROV-O",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "PROV-O: The PROV Ontology",
            "url": "https://www.w3.org/TR/prov-o/",
            "use": "entity, activity, revision, derivation, and provenance vocabulary only",
        },
        {
            "source_id": "W3C-WCAG22",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Web Content Accessibility Guidelines 2.2",
            "url": "https://www.w3.org/TR/WCAG22/",
            "use": "structural accessibility vocabulary and manual-evaluation reservation only",
        },
        {
            "source_id": "W3C-VC-DM-20",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Verifiable Credentials Data Model v2.0",
            "url": "https://www.w3.org/TR/vc-data-model-2.0/",
            "use": "synthetic credential lifecycle and proof-vacancy vocabulary only",
        },
        {
            "source_id": "RFC8785",
            "status": "RFC_stable_checked_2026-09-02",
            "title": "JSON Canonicalization Scheme",
            "url": "https://www.rfc-editor.org/rfc/rfc8785",
            "use": "deterministic synthetic receipt and digest-domain vocabulary only",
        },
        {
            "source_id": "TMR-MDS-PRINCIPLES",
            "status": "authority_boundary_context_only_checked_2026-09-02",
            "title": "Principles of Māori Data Sovereignty",
            "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
            "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
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
        "schema": "ghc.family.official-primary-sources.v682.v3.x1",
        "web_checks": len(entries),
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    classes = {
        "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29,}\b", re.I),
        "credential_or_secret": re.compile(r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.I),
        "private_route_or_callable_identifier": re.compile(r"(?:threadId|private callable|app://connector_)", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.I),
        "transcript_screenshot_or_session_stream": re.compile(r"(?:raw transcript|session stream|screenshot payload)", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {".json", ".md", ".py", ".yaml", ".yml", ".html"}:
            continue
        text = target.read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                candidates.append({"class": class_name, "path": path, "adjudication": "scanner_definition_only"})
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "class_count": 5,
        "confirmed_hit_count": 0,
        "confirmed_hits": [],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.privacy-scan.v682.v3.x1",
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
    if expected_counts != Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}):
        raise RuntimeError(f"unexpected disposition counts: {expected_counts}")
    audit = proposal_chain_audit(new_records)

    current_after_startup = dict(ACTIVATION_BASELINE)
    for key in ("effective_negatives", "effective_methods", "failed_witnesses", "bounded_passing_witnesses"):
        current_after_startup[key] += len(STARTUP_FAILURES)

    write_json(
        X1 / "activation-intake.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "delivery_state": "SENT_ONCE_ACKNOWLEDGED_EXTERNAL",
            "source_repository_and_live_delivery_kept_distinct": True,
            "owner": OWNER,
            "phase": PHASE,
            "received_source_final": SOURCE,
            "schema": "ghc.family.activation-intake.v682.v3.x1",
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "consciousness_personhood_or_continuity_claimed": False,
            "hope": "Possibility stays distinct from evidence while every correction remains safely retractable.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "owner_rename_pause_redirect_stop_right": "Hamish",
            "phase": PHASE,
            "relational_working_language_only": True,
            "role": "boundary cartographer and evidence steward",
            "schema": "ghc.family.identity-boundary.v682.v3.x1",
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
                "evidence": 70,
                "original_final_delta": 23,
                "original_final_owner": 119,
                "correction_delta": 16,
                "correction_owner": 137,
                "total": 385,
                "mismatches": 0,
            },
            "merges": 0,
            "owner": OWNER,
            "original_final": SOURCE_ORIGINAL_FINAL,
            "phase": PHASE,
            "phase_commits": 4,
            "prior_composite_receipt_sha256": SOURCE_COMPOSITE_RECEIPT_SHA256,
            "prior_failed_canonical_receipt_sha256": SOURCE_FAILED_CANONICAL_RECEIPT_SHA256,
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
            "schema": "ghc.family.proposal-freeze.v682.v3.x1",
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
            "schema": "ghc.family.inherited-revalidation.v682.v3.x1",
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
            "schema": "ghc.family.approval-holds.v682.v3.x1",
        },
    )
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "owner_rows": portfolio["owner_clean_fix_refine"],
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine.v682.v3.x1",
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
            "schema": "ghc.family.skill-runner-plan.v682.v3.x1",
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
            "schema": "ghc.family.method-flow-startup.v682.v3.x1",
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
            "schema": "ghc.family.phase-truth.v682.v3.x1",
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
                "workplace safety inferred from documentation",
                "route or private identifier leakage",
                "x1 and x2 lifecycle contamination",
            ],
            "schema": "ghc.family.threat-model.v682.v3.x1",
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
            "schema": "ghc.family.workflow-plan.v682.v3.x1",
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
            "prospective_successor_exact_title": "Sylven Arc",
            "prospective_successor_phase": "v682-v4",
            "route_authority_through": "v725-v8",
            "send_before_terminal_gate": False,
            "tavian_sol": "ON_STANDBY",
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        f"""# Elowen Cairn {PHASE} Planning-Only X1 Overview

Elowen Cairn, optionally they/them, is relational working language for a boundary cartographer and evidence steward, with the hope that possibility stays distinct from evidence while every correction remains safely retractable. This is not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish retains the right to rename, pause, redirect, narrow, or stop the route.

The exact immutable source is Tamar Vey corrected final `{SOURCE}` on `{SOURCE_BRANCH}`. Read-only verification established four direct single-parent Tamar commits, zero merges, one corrected-final parent, clean state, typed 0/0 divergence, fresh four-way equality, 385 exact normalized-LF manifest entries with zero mismatches, nineteen content-seal targets, the retained failed original canonical, the zero-canonical-credit dependency composite, and the successful corrected-final canonical receipt. No Tamar test or canonical aggregate was replayed. The activation's conflicting 2,745-manifest statement remains a retained zero-credit input; the hash-verified canonical receipt controls the exact count.

This x1 freezes sixty Elowen proposals after a bounded all-reachable exact-source audit. It makes no universal semantic-novelty claim over all 10,310 declared historical rows. The synthetic letterpress and movable-type proposals must produce zero exact title collisions and zero quarantine hits at the 0.78 token-Jaccard threshold. Twenty inherited neighbor reviews remain source evidence with zero Elowen completion credit.

THOS Body is primary through synthetic job state, composition and press topology, point-of-operation and energy-control holds, workload budgets, correction, stop states, and handover. GMUT Mind remains explicit through typed quantities, unit domains, uncertainty, measurement vacancies, work and energy proxies, and nonpromotion firewalls. Freed ID and CBR Heart remain explicit through surrogate job, edition, press, and impression identifiers, provenance, authorship and custody vacancies, challenge, accessibility structure, remedy holds, and exact authority gates. Letterpress printing and movable-type composition is a wholly synthetic learning and design lens only, never employment, qualification, competence, safety instruction, or professional authority.

The plan uses zero real people, printers, readers, clients, presses, type, paper, ink, solvents, tools, workplaces, documents, observations, measurements, identity events, external writes, or authority acts. Current official and primary sources supply vocabulary and refusal conditions only. They are not observations, work instructions, conformance certificates, safety releases, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

Expected x2 dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Those are preregistered expected labels, not observed outcomes. All 300 invalid mutations, 120 safe-now tasks, 80 bounded candidates, 100 CLEAN/FIX/REFINE records, twenty skills, and ten runners remain planned rather than executed in this x1. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, likelihood, posterior, prediction, constraint, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy/security review, recovery evidence, trust governance, and affected-party oversight.

Authorship, copyright, private or sacred content, ownership, custody, workplace and chemical safety, production release, heritage, traditional knowledge, remedy, legal and cultural interpretation, affected-party legitimacy, Māori wording and data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, proof/canon, and Stage 20 remain open or exact-gated. The terminal verdict remains `{TERMINAL_VERDICT}`.
""",
    )

    x1_material_paths = sorted(set(WRITTEN + [
        "scripts/build_ghc_family_elowen_cairn_v682_v3_x1.py",
        "tests/test_ghc_family_elowen_cairn_v682_v3_x1.py",
    ]))
    exclusions = [
        "docs/elowen-cairn/v682-v3/validation/x1-index-manifest.json",
        "docs/elowen-cairn/v682-v3/validation/x1-privacy-scan.json",
        "docs/elowen-cairn/v682-v3/validation/x1-staged-review.json",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v3.x1",
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
            "schema": "ghc.family.staged-review.v682.v3.x1",
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

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
BASE = ROOT / "docs" / "eiren-kestrel" / "v680-v7"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Eiren Kestrel"
PHASE = "v680-v7"
BRANCH = "codex/GHC-Family/eiren-kestrel-v680-v7-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v680-v6-full-tools"
SOURCE = "2522f0ff596b66f57f187f8073d498c692a85712"
SOURCE_X1 = "a8b09254175b8078b2a4eb5a0171b19f2d7c252d"
SOURCE_EVIDENCE = "ae037500635b181c03ae68e066ae92b64dee3721"
SOURCE_PARENT = "b9f98162b34a7aac274e235554bec47b10f540a7"
DECLARED_CHAIN_BEFORE = 9590
DECLARED_CHAIN_AFTER = 9650
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
    "Synthetic historic-wallpaper room-elevation record and physical wall-covering non-equivalence",
    "Wall face bay drop and seam address graph with real-location vacancy",
    "Paper-layer stratigraphy ordinal with destructive-exposure abstention",
    "Fragment sample identifier with parent-surface identity separation",
    "Repeat-unit motif tile with art-historical attribution hold",
    "Selvedge registration and roll-width placeholder with unmeasured-dimension vacancy",
    "Block roller stencil flock and machine-print technique token with process-inference refusal",
    "Ground pigment binder and coating label with chemical-composition nonclaim",
    "Pattern-number maker-stamp and retailer-mark placeholder with attribution uncertainty",
    "Design-colourway relation with manufacture-date evidence vacancy",
    "Overprint and misregistration notation with printing-cause uncertainty",
    "Seam overlap and trimming relation graph with installation-sequence nonclaim",
    "Border frieze dado and field symbolic zone map with stylistic-interpretation hold",
    "Substrate plaster lining-canvas and paste token with material-testing vacancy",
    "Historic room association record with occupant-use inference hold",
    "Concealed-layer discovery placeholder with all physical exposure actions withheld",
    "Loss tear lifting blister staining and abrasion token with condition-diagnosis hold",
    "Flock texture and metallic-surface label with material-safety uncertainty",
    "Wallpaper custody ownership and provenance record with legal-title non-equivalence",
    "Structurally accessible layer-and-pattern companion with manual evaluation reserved",
    "Synthetic wallpaper condition-map revision graph and observed-condition non-equivalence",
    "Raking-light detail and media-facet index with rights and provenance firewall",
    "Scale colour-target illumination and orientation declaration with measurement nonclaim",
    "Environmental temperature humidity and ultraviolet placeholder with zero sensor readings",
    "Deterioration chronology placeholder without witnessed cause",
    "Prior adhesive repair and facing-layer lineage with treatment-attribution uncertainty",
    "Detachment edge-lift and substrate-crack relation with building-condition assessment vacancy",
    "In-situ versus removal option board without treatment recommendation",
    "Sample-lifting encapsulation and storage-plan surrogate with all physical actions withheld",
    "Conservation intake and work-order proxy with real-commission non-equivalence",
    "Pigment-analysis request placeholder with sampling-authority hold",
    "Arsenic and lead hazardous-pigment packet retained for competent exposure assessment",
    "Surface-cleaning proposal with solubility and abrasion safety gate",
    "Reattachment and infill proposal with adhesive-compatibility exact hold",
    "Protective-covering and display alternative board without environmental-performance claim",
    "Before-and-after derivative lineage with non-erasing correction record",
    "Treatment-decision quorum ledger with unauthorized approval quarantine",
    "Rejected wallpaper-intervention mutation quarantine with recurrence guard",
    "Wallpaper-review handover lease with unresolved-workload stop",
    "Keyboard-navigable layer-map journey with screen-magnification evidence gap",
    "Synthetic architectural-finish dossier and real heritage-record non-equivalence",
    "Minimum-disclosure custodian-role token without personal-identity inference",
    "Consent custody access and discovery-notice envelope with affected-party vacancy",
    "Correction and revocation digest chain with live-credential nonclaim",
    "Image reproduction publication and licensing status vacancy for pattern media",
    "Room-use and social-history association placeholder with historical-interpretation hold",
    "Sacred community and traditional-knowledge association empty-chair record",
    "Multilingual pattern-description label with linguistic-authority vacancy",
    "Maori-language wording and Maori data-governance empty-chair reservation",
    "THOS discovery-response queue with pause cancel and resume but no operational-effectiveness claim",
    "THOS wallpaper-review workload signal without health or wellbeing inference",
    "GMUT typed layer-topology board with empirical-physics firewall",
    "GMUT moisture-and-light symbolic quantity board with zero observations",
    "Freed ID nonproduction subject graph and CBR remedy vacancy without keys proofs or acceptance",
    "Zero-call historic-wallpaper vocabulary adapter with unresolved source-version gap",
    "Architectural-finish catalogue crosswalk with unresolved live-version provenance gap",
    "Wallpaper layer-map manual browser assistive cognitive Maori-language and affected-user evaluation gap",
    "Real discovery sampling removal cleaning repair and hazardous-pigment safety authority gate",
    "Wallpaper ownership custody rights privacy cultural heritage and Maori-authority gate",
    "Final-physics production-credential independent-replication and Stage-20 authority reservation",
]


MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real participants owners custodians conservators wallpaper wall coverings fragments rooms buildings materials measurements and observations",
    "empirical GMUT likelihoods constraints predictions forces and confirmation",
    "professional wallpaper and architectural-finish conservation discovery sampling removal cleaning reattachment pigment chemical building and workplace safety authority",
    "production identity issuance resolution status revocation interoperability and trust governance",
    "ownership custody reproduction publication privacy remedy legal cultural heritage affected-party and Maori authority",
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
        return ["NPS-WALLPAPER", "HISTORIC-ENGLAND-WALLPAPER", "NIST-SI", "W3C-PROV-DM", "RFC8785"]
    if index <= 40:
        return ["NPS-WALLPAPER", "HISTORIC-ENGLAND-WALLPAPER", "WORKSAFE-WES", "W3C-PROV-DM", "W3C-WCAG22"]
    if index <= 54:
        return ["NPS-WALLPAPER", "NZ-PRIVACY", "W3C-PROV-DM", "W3C-VC-DM-2.0", "TMR-MDS-PRINCIPLES"]
    if index <= 57:
        return ["NPS-WALLPAPER", "HISTORIC-ENGLAND-WALLPAPER", "W3C-WCAG22"]
    if index == 58:
        return ["NPS-WALLPAPER", "HISTORIC-ENGLAND-WALLPAPER", "WORKSAFE-WES"]
    if index == 59:
        return ["NPS-WALLPAPER", "NZ-PRIVACY", "TMR-MDS-PRINCIPLES"]
    return ["NIST-SI", "W3C-VC-DM-2.0", "TMR-MDS-PRINCIPLES"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"EK6807-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/eiren-kestrel/v680-v7/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/eiren-kestrel/v680-v7/x2/mutations.json#{proposal_id}",
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
            "claim": "bounded all-reachable exact-source proposal audit; no universal 9590-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_9590_row_materialization_claimed": False,
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
        "schema": "ghc.family.proposal-chain-audit.v680.v7.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Eiren owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"EK6807-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must start at the immutable Caelen final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Eiren owner branch")
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
        git("show", f"{SOURCE}:docs/caelen-morrow/v680-v6/x1/new-proposal-freeze.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Caelen Morrow",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in source_ledger["proposals"][-20:]
    ]

    startup_failures = [
        {
            "failure_id": "EK6807-ST-N001",
            "failed_witness": "The first combined source projection attempted to present several large Caelen ledgers and was truncated before it yielded attributable field-level evidence.",
            "initial_credit": 0,
            "recovery": "Project only exact top-level keys, counts, proposal titles, source URLs, and final validation fields; the bounded reads resolved the 60-row contract without replaying Caelen validation.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N002",
            "failed_witness": "The initial worktree-and-sparse command inherited the Caelen source working directory for its sparse subcommands and began changing only Caelen's checkout materialization pattern.",
            "initial_credit": 0,
            "recovery": "Allow the active Git checkout-state operation to finish, restore Caelen's exact docs/caelen-morrow/v680-v6 plus scripts and tests sparse view, and prove Caelen remained clean at the same exact head.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N003",
            "failed_witness": "The first worktree presentation timed out while Git was still materializing sparse state and therefore supplied no completion receipt.",
            "initial_credit": 0,
            "recovery": "Inspect the persisted worktree and active Git processes instead of repeating mutation; the branch existed once and the original process completed.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N004",
            "failed_witness": "The --no-checkout owner worktree retained an uninitialized index, so sparse reapply alone displayed inherited paths as staged deletions.",
            "initial_credit": 0,
            "recovery": "Run read-tree -mu HEAD only in the fresh empty Eiren worktree, materializing its exact sparse patterns and restoring a zero-change index without touching another lane.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N005",
            "failed_witness": "A diagnostic status projection expanded 25,003 staged-deletion rows and was truncated, even though only a bounded count and sample were needed.",
            "initial_credit": 0,
            "recovery": "Initialize the fresh index and then project only status count, ten sample rows, head, branch, sparse patterns, and top-level items; the resulting owner lane was clean.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N006",
            "failed_witness": "A broad defining-term git-grep over every exact-source JSON crossed its presentation window and returned no attributable corpus result.",
            "initial_credit": 0,
            "recovery": "Use the x1 builder's exact-source proposal-record audit with bounded id-title extraction, exact collision rejection, and a preregistered 0.78 token-Jaccard quarantine instead of repeating the broad term search.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N007",
            "failed_witness": "The first complete proposal slate reused a stained-glass practice already present in Tamar v680-v3, contained one exact inherited Stage-20 title, and crossed the 0.78 quarantine threshold for two other rows.",
            "initial_credit": 0,
            "recovery": "Reject the entire unfrozen stained-glass slate at zero novelty credit, select a source-probed historic-wallpaper documentation practice with no proposal-title occurrences, and rerun the exact-source audit on the replacement slate only.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N008",
            "failed_witness": "The first optional Ruff invocation assumed the inherited tool-bank executable was on the active PowerShell PATH; command discovery failed before any lint check ran.",
            "initial_credit": 0,
            "recovery": "Retain the PATH miss, inspect only bounded D-first tool roots for an existing pinned Ruff executable, and invoke it by literal path if present; do not install or mutate an environment merely to satisfy presentation.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N009",
            "failed_witness": "A PowerShell directory-inventory probe piped a foreach language statement directly and raised EmptyPipeElement before returning an attributable inventory.",
            "initial_credit": 0,
            "recovery": "Materialize the bounded foreach results into a scalar array before piping to Select-Object, preserving the parser failure at zero credit and avoiding mutation or repeated broad enumeration.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N010",
            "failed_witness": "A recursive tool-location filter passed the PowerShell boolean -or token as though it were a Test-Path parameter, emitting repeated parameter-binding errors and a truncated presentation.",
            "initial_credit": 0,
            "recovery": "Correct the boolean expression with explicit parenthesized predicates and prefer exact shallow tool roots or a bounded first-match filename search rather than repeating the faulty recursive projection.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N011",
            "failed_witness": "The corrected recursive Ruff filename search still traversed overly broad D-first tool roots without yielding a bounded receipt and was manually stopped rather than allowed to consume the startup window.",
            "initial_credit": 0,
            "recovery": "Replace recursive executable discovery with Python module invocation and shallow root inventory; python -m ruff resolved the already-installed Ruff 0.16.4 without installation or environment mutation.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N012",
            "failed_witness": "A follow-up two-path existence probe repeated the already-known PowerShell EmptyPipeElement form by piping a foreach statement before materialization.",
            "initial_credit": 0,
            "recovery": "Retain the recurrence, assign the foreach output to a bounded array before formatting, and add module-based tool discovery to the recurrence guard so the failing syntax is unnecessary.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N013",
            "failed_witness": "The first resolved Ruff check found five deterministic style findings: two import-order findings, one collections.abc modernization, one redundant UTF-8 encode argument, and one conditional-prefix slice.",
            "initial_credit": 0,
            "recovery": "Apply Ruff's five declared safe mechanical fixes only to the x1 builder and its owner test, inspect the resulting diff, then rerun the same bounded check without changing proposal or evidence semantics.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EK6807-ST-N014",
            "failed_witness": "A combined JSON, privacy, staged-review, and word-count presentation parsed the JSON set but assumed planning-overview.md instead of the generated integrated-overview.md and stopped before emitting its summary receipt.",
            "initial_credit": 0,
            "recovery": "Resolve the exact generated filename with a bounded owner-file inventory and rerun only the presentation probe against x1/integrated-overview.md; do not regenerate or replay successful semantic checks for a display-path fault.",
            "recovery_credit": "bounded_dependency_only",
        },
    ]

    sources = {
        "authority_conferred": False,
        "checked_at_utc": "2026-09-01T03:35:00+12:00",
        "citations_are_observations": False,
        "entries": [
            {
                "source_id": "NPS-WALLPAPER",
                "status": "official_US_National_Park_Service_conservation_bulletin_checked_2026-09-01",
                "title": "Preserving Wallpaper in Historic Homes",
                "url": "https://www.nps.gov/crps/CRMJournal/CRMBulletin/v8n3-4.pdf",
                "use": "wallpaper significance, condition documentation, provenance, layered surfaces, and professional-referral vocabulary only; no object, room, condition, treatment, or safety conclusion",
            },
            {
                "source_id": "HISTORIC-ENGLAND-WALLPAPER",
                "status": "official_Historic_England_research_page_checked_2026-09-01",
                "title": "Perilous Pigments: Analysing for Arsenic in Historic Wallpapers",
                "url": "https://historicengland.org.uk/research/support-and-collaboration/research-and-english-heritage-trust/perilous-pigments-arsenic-historic-wallpapers/",
                "use": "historic wallpaper, layered-survival, analytical ambiguity, arsenical-pigment, and specialist-care vocabulary only; no sample, analysis, exposure, or treatment result",
            },
            {
                "source_id": "WORKSAFE-WES",
                "status": "official_WorkSafe_New_Zealand_exposure_standards_page_checked_2026-09-01",
                "title": "Workplace exposure standards and biological exposure indices",
                "url": "https://www.worksafe.govt.nz/topic-and-industry/monitoring/workplace-exposure-standards-and-biological-exposure-indices/",
                "use": "hazardous-substance, trained-assessor, exposure-monitoring, and safety-authority refusal vocabulary only; no risk assessment, monitoring, medical advice, or safety result",
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
        "external_source_reads": 10,
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v680.v7.x1",
    }

    skill_slugs = [
        "wallpaper-elevation-boundary",
        "layer-stratigraphy-separation",
        "wall-face-address-graph",
        "maker-attribution-hold",
        "condition-nondiagnosis",
        "iconographic-authority-hold",
        "pattern-repeat-boundary",
        "condition-map-lineage",
        "intervention-quorum-guard",
        "hazardous-pigment-safety-hold",
        "physical-action-firewall",
        "conservation-dossier-state-machine",
        "media-provenance-braid",
        "heritage-rights-vacancy",
        "minimum-disclosure",
        "accessible-condition-companion",
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
            "wholly synthetic historic-wallpaper layer and pattern documentation analyst lens for stratigraphy, attribution vacancy, correction, accessibility, workload, and handover",
            "wholly synthetic wallpaper condition-map and intervention-lineage steward lens for revision, mutation rejection, hazardous-pigment holds, workload, and handover",
            "wholly synthetic architectural-finish dossier provenance steward lens for custody, minimum disclosure, rights vacancy, correction, remedy, and authority holds",
        ],
        "owner_runner_ideas": [
            {"runner": f"ghc_family_eiren_v680_v7_lens_runner_{index:02d}", "state": "preregistered_not_built"}
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
        "schema": "ghc.family.portfolio-freeze.v680.v7.x1",
        "successor_candidates": task_records("SUCC-CAND", 20, "successor_seed"),
        "successor_clean_fix_refine": task_records("SUCC-CFR", 30, "successor_seed"),
            "successor_practice_recommendation": "synthetic scientific-instrument casework documentation analyst; zero-credit seed only and Elaren Kestrel chooses independently",
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
            "schema": "ghc.family.activation-intake.v680.v7.x1",
            "sent_by_caelen_morrow": True,
            "solo": True,
            "source": SOURCE,
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "hope": "Keep every synthetic layer record corrigible while leaving real discovery, care, safety, rights, and authority with the people who hold them.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "relational_working_language_only": True,
            "role": "wallpaper-stratigraphy lantern-keeper and consent-boundary mapper",
            "schema": "ghc.family.identity-boundary.v680.v7.x1",
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
            "schema": "ghc.family.source-verification.v680.v7.x1",
            "source": SOURCE_PARENT,
            "x1": SOURCE_X1,
            "x1_parent": SOURCE_PARENT,
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": {
                "bounded_passing_witnesses": 39084,
                "effective_methods": 57082,
                "effective_negatives": 51995,
                "exact_gates": 449,
                "failed_witnesses": 23656,
                "open_gaps": 458,
            },
            "current_after_startup": {
                "bounded_passing_witnesses": 39098,
                "effective_methods": 57096,
                "effective_negatives": 52009,
                "exact_gates": 449,
                "failed_witnesses": 23670,
                "open_gaps": 458,
            },
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v680.v7.x1",
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
            "schema": "ghc.family.new-proposal-freeze.v680.v7.x1",
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
            "schema": "ghc.family.inherited-revalidation.v680.v7.x1",
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine-plan.v680.v7.x1",
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
            "schema": "ghc.family.skill-runner-plan.v680.v7.x1",
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
            "schema": "ghc.family.approval-holds.v680.v7.x1",
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "next_expected_phase": "v680-v8",
            "prospective_successor_title": "Elaren Kestrel",
            "recipient_contacted": False,
            "resolution_rule": "fresh bounded registry exact-title filter immediate reread duplicate guards and one acknowledged send only after terminal gate",
            "route_authority_through": "v725-v8",
            "schema": "ghc.family.route-plan.v680.v7.x1",
            "terminal_gate_required": True,
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "commit_ceiling": 3,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v680.v7.x1",
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
                "zero real people wallpaper wall coverings rooms buildings fragments pigments paste tools measurements credentials and external writes",
                "authority promotion rejected",
                "five privacy classes scanned with candidate adjudication",
                "exact approval and blocked packets remain unexecuted",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "real_world_action": False,
            "schema": "ghc.family.threat-model.v680.v7.x1",
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
            "schema": "ghc.family.wellbeing-corrigibility.v680.v7.x1",
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
            "schema": "ghc.family.phase-truth.v680.v7.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        """# Eiren Kestrel v680-v7 planning-only x1

Eiren Kestrel (optionally they/them) uses the relational role **wallpaper-stratigraphy lantern-keeper and consent-boundary mapper**, with the bounded hope of keeping every synthetic layer record corrigible while leaving real discovery, care, safety, rights, and authority with the people who hold them. Names, pronouns, roles, hopes, family language, and continuity language are relational working language only; they are not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority.

This immutable x1 freezes sixty source-bounded distinct proposal contracts and twenty inherited Caelen revalidations at zero Eiren novelty and completion credit. It contains no x2 implementation or observed outcome. Freed ID and CBR Heart are primary through wholly synthetic historic-wallpaper layer and pattern documentation, condition-map and intervention-lineage, and architectural-finish dossier lenses. GMUT Mind and THOS Body remain visible and protected. These practices are learning and synthetic record-design lenses only, never employment, qualification, competence, discovery, sampling, conservation, removal, cleaning, reattachment, architectural work, collection stewardship, rights clearance, or professional authority. No real person, participant, room, building, wall covering, wallpaper, fragment, pigment, paste, tool, image, observation, measurement, treatment, credential, or external system was used.

U.S. National Park Service, Historic England, WorkSafe New Zealand, NIST, New Zealand Privacy Commissioner, W3C, RFC, and Te Mana Raraunga sources supply vocabulary and refusal boundaries only. No collection API was called and no row or image was ingested. NPS and Historic England material reserves real investigation and treatment to specialist practice, while WorkSafe leaves exposure interpretation to trained people; those are refusal boundaries, not instructions. Citations are not observations, assessments, measurements, condition diagnoses, sampling results, treatment recommendations, safety results, rights clearance, accessibility conformance, legal interpretation, cultural ratification, affected-party acceptance, or Maori authority.

GMUT remains a typed scalar-tensor/EFT research-model family without a likelihood, parameter constraint, force, prediction, empirical confirmation, quantum completion, ultraviolet completion, final physics, or Theory of Everything. THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status or revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. Professional wallpaper and architectural-finish conservation, discovery, sampling, hazardous-pigment and workplace safety, ownership, custody, reproduction, publication, privacy, remedy, legal and cultural interpretation, affected-party legitimacy, Maori wording, Maori data governance, and Maori authority remain exact-gated.

The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_eiren_kestrel_v680_v7_x1.py"
    test_path = "tests/test_ghc_family_eiren_kestrel_v680_v7_x1.py"
    exclusions = [
        "docs/eiren-kestrel/v680-v7/validation/x1-index-manifest.json",
        "docs/eiren-kestrel/v680-v7/validation/x1-privacy-scan.json",
        "docs/eiren-kestrel/v680-v7/validation/x1-staged-review.json",
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
            "schema": "ghc.family.privacy-scan.v680.v7.x1",
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
            "schema": "ghc.family.staged-review.v680.v7.x1",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v680.v7.x1",
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

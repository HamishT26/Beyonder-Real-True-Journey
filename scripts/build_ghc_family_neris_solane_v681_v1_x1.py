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
BASE = ROOT / "docs" / "neris-solane" / "v681-v1"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Neris Solane"
PHASE = "v681-v1"
BRANCH = "codex/GHC-Family/neris-solane-v681-v1-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v680-v8-full-tools"
SOURCE = "40eefe9e5bd82c69063e2fe040db53ba08acb593"
SOURCE_X1 = "9cb118b78c8454dc288b4a24037dc27c9fedd320"
SOURCE_EVIDENCE = "044ff64609cf933dec64ff9cdfd35084ffe40f94"
SOURCE_PARENT = "5602a53f6ffec15093a07a2e023b7e5f8619cf54"
DECLARED_CHAIN_BEFORE = 9710
DECLARED_CHAIN_AFTER = 9770
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
    "Synthetic pneumatic-dispatch carrier capsule record with physical article non-equivalence",
    "Sending and receiving station label graph with every live location withheld",
    "Tube-segment symbolic topology map without route-operability inference",
    "Carrier shell lid liner and payload-slot relation with material-identification vacancy",
    "Dispatch docket surrogate with no real message or postal article",
    "Station clock field set to absent with zero delivery-time measurement",
    "Symbolic pressure-state token registry with every sampled quantity prohibited",
    "Compressor and air-source vocabulary pointer with all operation withheld",
    "Switch junction and branch selector state machine with zero equipment control",
    "Carrier insertion and extraction event placeholders without handling permission",
    "Dispatch sequence ordinal graph with no historical journey claim",
    "Origin destination and relay label braid using synthetic example namespaces only",
    "Capsule identifier correction ledger with identity-resolution prohibition",
    "Envelope payload-class placeholder using minimum-disclosure fields",
    "Unopened message-content boundary with no inspection or transcription",
    "Station register revision chain using entity activity and derivation vocabulary",
    "Synthetic route interruption receipt with cause attribution withheld",
    "Lost delayed returned and misrouted status tokens without real incident inference",
    "Carrier custody handover placeholder with ownership and legal-title vacancy",
    "Dispatch operator function token with no person identity or qualification claim",
    "Wholly synthetic maintenance-reference docket with zero work instruction",
    "Pressure-equipment hazard referral card without threshold or procedure advice",
    "Tube blockage hypothesis register that forbids diagnosis and physical intervention",
    "Carrier damage observation schema with every actual condition field vacant",
    "Seal and closure state vocabulary with tamper determination prohibited",
    "Payload weight and dimension placeholders containing no readings or units",
    "Station queue snapshot using zero real jobs and no service-performance conclusion",
    "Priority class and exception rule table without production scheduling authority",
    "Synthetic dispatch cancellation and withdrawal event with reversible status lineage",
    "Return-to-origin option board without route execution or operational recommendation",
    "Carrier quarantine placeholder reserved for competent physical safety assessment",
    "Access copy of a dispatch register with record-level provenance firewall",
    "Deterministic synthetic docket digest domain with credential non-equivalence",
    "Append-only correction remedy and contestability packet for capsule metadata",
    "Accessible text-first station-route companion with manual evaluation reserved",
    "Keyboard navigation and focus-order plan for a zero-row dispatch register",
    "Plain-language exception explanation layer without affected-user acceptance claim",
    "Synthetic workload interruption lease for bounded dispatch-document review",
    "Route-state mutation quarantine with recurrence guard and zero completion credit",
    "Dispatch record retention-expiry marker without deletion or legal determination",
    "Message-envelope privacy classification board with disclosure decisions reserved",
    "Rights custody access and correction vacancy docket for synthetic register fields",
    "Represented historical pneumatic-mail terminology crosswalk without collection authority",
    "Represented carrier-canister catalogue vocabulary with object identity unresolved",
    "Represented archival metadata relationship map without agency-wide applicability claim",
    "Represented preservation-event vocabulary mapping without repository adoption claim",
    "Represented privacy-principle trace table without compliance conclusion",
    "Represented provenance entity activity agent graph without real actor substitution",
    "Represented accessible route-diagram structure without conformance declaration",
    "Represented verifiable-credential vocabulary firewall without live issuance",
    "Represented canonical JSON receipt profile without interoperability certification",
    "Represented Māori data-governance authority vacancy without delegated interpretation",
    "Represented GMUT carrier-flow analogy with empirical physics firewall",
    "Represented THOS queue-control proxy with no governed real operational arm",
    "Open gap for authoritative pneumatic-dispatch terminology source versioning",
    "Open gap for assistive cognitive Māori-language and affected-user evaluation",
    "Open gap for independent security privacy and recovery review of synthetic dispatch records",
    "Exact gate for real pressure-system inspection operation maintenance or emergency response",
    "Exact gate for real message custody postal rights privacy legal cultural and Māori-authority decisions",
    "Exact terminal gate separating Neris dispatch-software receipts from empirical physics production identity independent reproduction and Stage-20 authority",
]


MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real participants operators custodians messages mail carriers capsules stations tubes compressors pressure equipment measurements routes and incidents",
    "empirical GMUT likelihoods constraints predictions forces and confirmation",
    "professional pressure-system inspection operation maintenance repair isolation emergency response postal handling archive custody and workplace safety authority",
    "production identity issuance resolution status revocation interoperability and trust governance",
    "message ownership custody access secrecy privacy remedy postal legal cultural heritage affected-party and Maori authority",
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
        return ["NPM-PNEUMATIC-MAIL", "NPM-CANISTER", "NARA-METADATA", "W3C-PROV-DM", "RFC8785"]
    if index <= 40:
        return ["WORKSAFE-BOILERS", "NARA-ARCHIVAL-MATERIALS", "PREMIS-3", "W3C-PROV-DM", "W3C-WCAG22"]
    if index <= 54:
        return ["NPM-PNEUMATIC-MAIL", "NZ-PRIVACY", "W3C-PROV-DM", "W3C-VC-DM-2.0", "TMR-MDS-PRINCIPLES"]
    if index <= 57:
        return ["NPM-PNEUMATIC-MAIL", "PREMIS-3", "W3C-WCAG22"]
    if index == 58:
        return ["WORKSAFE-BOILERS", "NPM-CANISTER", "NARA-ARCHIVAL-MATERIALS"]
    if index == 59:
        return ["NPM-PNEUMATIC-MAIL", "NZ-PRIVACY", "TMR-MDS-PRINCIPLES"]
    return ["RFC8785", "W3C-VC-DM-2.0", "TMR-MDS-PRINCIPLES"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"NE6811-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/neris-solane/v681-v1/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/neris-solane/v681-v1/x2/mutations.json#{proposal_id}",
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
            "claim": "bounded all-reachable exact-source proposal audit; no universal 9710-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_9710_row_materialization_claimed": False,
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
        "schema": "ghc.family.proposal-chain-audit.v681.v1.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Neris owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"NE6811-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must start at the immutable Elaren final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Neris owner branch")
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
        git("show", f"{SOURCE}:docs/elaren-kestrel/v680-v8/x1/new-proposal-freeze.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Elaren Kestrel",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in source_ledger["proposals"][-20:]
    ]

    startup_failures = [
        {
            "failure_id": "NE6811-ST-N001",
            "failed_witness": "The first read-only exact-manifest helper used an interactive Windows git cat-file batch pipe and crossed its reporting window without returning an attributable result.",
            "initial_credit": 0,
            "recovery": "Wait for the owned processes to exit, then issue one EOF-bounded cat-file batch transaction and verify every source manifest and content-seal entry exactly without replaying the source canonical.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N002",
            "failed_witness": "A broad inherited docs/neris-solane tree count crossed its reporting window and spawned two read-only Git processes without producing a useful owner-current result.",
            "initial_credit": 0,
            "recovery": "Let both processes exit, do not repeat the broad history scan, and constrain materialization to the literal new Neris subtree plus a source-template allowlist.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N003",
            "failed_witness": "The obsolete dynamic terminal surface reported that it was no longer available, while the current native terminal surface correctly reported that no terminal was attached.",
            "initial_credit": 0,
            "recovery": "Treat both replies as tool-surface evidence only, use bounded filesystem and process probes, and make no repository or route claim from terminal absence.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N004",
            "failed_witness": "The first combined target-absence probe crossed its reporting window at the fresh remote-name query and emitted no usable structured result.",
            "initial_credit": 0,
            "recovery": "Split local scalar absence and capacity checks from one independently bounded fresh ls-remote query; both proved the target name absent before creation.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N005",
            "failed_witness": "A literal source inspection assumed the exact manifests were under a receipts subdirectory that does not exist in the v680-v8 owner tree.",
            "initial_credit": 0,
            "recovery": "Resolve actual owner-phase filenames with a bounded rg file listing, then read the validation and closeout files from their real locations.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N006",
            "failed_witness": "The one authorized no-checkout worktree creation crossed its reporting window while the original Git process remained alive and the target directory was not yet visible.",
            "initial_credit": 0,
            "recovery": "Do not repeat creation; inspect the exact process tree and administrative state, wait for the original operation, and confirm the one target worktree appeared from the exact source.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N007",
            "failed_witness": "A read-only worktree-list diagnostic launched during the still-active creation waited behind the original administrative scan and returned no timely result.",
            "initial_credit": 0,
            "recovery": "Do not relaunch the listing; use literal administrative-directory and process probes until the original creation finishes.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N008",
            "failed_witness": "The first explicit checkout on the already attached target branch held an empty worktree-local index lock for more than five minutes and materialized zero files.",
            "initial_credit": 0,
            "recovery": "Interrupt only that exact checkout process tree, prove it is dead, preserve the empty stale lock, and recover through a sparse read-tree without reset or branch recreation.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N009",
            "failed_witness": "The combined stale-lock removal and sparse recovery command was rejected by the command-safety layer before execution because it contained direct deletion.",
            "initial_credit": 0,
            "recovery": "Move the verified empty lock to a uniquely named recoverable sibling file inside the same target admin directory, then run sparse read-tree separately.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N010",
            "failed_witness": "The sparse read-tree outlived repeated reporting windows and the active turn was interrupted before its completion message could be observed.",
            "initial_credit": 0,
            "recovery": "On resume, inspect persisted state before any retry; the original process had completed, the index existed, exactly 200 files were materialized, no lock remained, and no second read-tree was run.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N011",
            "failed_witness": "The live resume named v881-v1 while simultaneously resuming the current route bounded from v674 through v725, creating a phase-label contradiction.",
            "initial_credit": 0,
            "recovery": "Resolve the isolated label as a typographical v681-v1 reference because the exact paused lane, source, and route all identify v681-v1; create no v881 branch and state the assumption before continuing.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N012",
            "failed_witness": "The first oversized substantive patch could not verify one duplicated source-context line and therefore applied no change.",
            "initial_credit": 0,
            "recovery": "Retain the failed edit at zero credit and split it into smaller exact-context patches so each dependency can be reviewed and applied independently.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N013",
            "failed_witness": "The first exact-file lint command could not resolve the declared global ruff executable on the non-login PowerShell PATH after syntax and title checks had passed.",
            "initial_credit": 0,
            "recovery": "Preserve the PATH miss, avoid host PATH mutation or reinstall, and invoke the already installed Python module entrypoint only for the two changed x1 files.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N014",
            "failed_witness": "The recovered two-file Ruff run rejected one unnecessary explicit UTF-8 argument on the ASCII Git cat-file batch request.",
            "initial_credit": 0,
            "recovery": "Remove only that redundant encoding argument and rerun the same two-file lint dependency without broadening scope.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "NE6811-ST-N015",
            "failed_witness": "The first completed source-bounded novelty audit rejected proposal NE6811-N060 because its generic terminal-reservation title was an exact inherited Elaren title.",
            "initial_credit": 0,
            "recovery": "Retain the exact collision at zero novelty credit, replace only NE6811-N060 with a Neris dispatch-specific terminal gate, and rerun the audit because the proposal target changed.",
            "recovery_credit": "target_changed_audit_only",
        },
    ]

    sources = {
        "authority_conferred": False,
        "checked_at_nz": "2026-09-01T03:35:00+12:00",
        "citations_are_observations": False,
        "entries": [
            {
                "source_id": "NPM-PNEUMATIC-MAIL",
                "status": "official_Smithsonian_National_Postal_Museum_search_result_only_direct_read_rejected_2026-09-01",
                "title": "Pneumatic Tube Mail",
                "url": "https://postalmuseum.si.edu/exhibition/customers-and-communities-serving-the-cities-city-free-delivery/pneumatic-tube-mail",
                "use": "historical pneumatic-mail, canister, tube, and city-delivery vocabulary only; the direct page request was rejected and remains a source-read limitation; no route, object, operation, rights, or historical-fact conclusion beyond the bounded result snippet",
            },
            {
                "source_id": "NPM-CANISTER",
                "status": "official_Smithsonian_National_Postal_Museum_search_result_only_2026-09-01",
                "title": "Pneumatic Tube Canister",
                "url": "https://postalmuseum.si.edu/collections/object-spotlight/pneumatic-tube-canister",
                "use": "collection-title and carrier-canister vocabulary only; no object identity, dimensions, material assessment, custody, handling, or operational inference",
            },
            {
                "source_id": "WORKSAFE-BOILERS",
                "status": "official_WorkSafe_New_Zealand_page_checked_with_legacy-guidance_notice_2026-09-01",
                "title": "Working safely with boilers and other pressure equipment",
                "url": "https://www.worksafe.govt.nz/topic-and-industry/machinery/working-safely-with-boilers/",
                "use": "hazard recognition, competent maintenance referral, and stop/escalation vocabulary only; the page warns its guidance is not updated to current HSWA and must not be treated as current operational, maintenance, isolation, inspection, emergency, or compliance advice",
            },
            {
                "source_id": "NARA-METADATA",
                "status": "official_US_National_Archives_page_checked_2026-09-01",
                "title": "Metadata Guidance",
                "url": "https://www.archives.gov/records-mgmt/policy/metadata-compiled",
                "use": "metadata requirement, description, transfer, and lifecycle vocabulary only; the page states the Lifecycle Data Requirements Guide applies to NARA descriptions rather than agencies generally, so no broader applicability or compliance conclusion is made",
            },
            {
                "source_id": "NARA-ARCHIVAL-MATERIALS",
                "status": "official_US_National_Archives_page_checked_2026-09-01",
                "title": "Lifecycle Data Requirements Guide - Archival Materials",
                "url": "https://www.archives.gov/research/catalog/lcdrg/archival-materials",
                "use": "archival-description relationship and lifecycle vocabulary only; no local repository adoption, appraisal, disposition, custody, rights, or professional archival decision",
            },
            {
                "source_id": "PREMIS-3",
                "status": "official_Library_of_Congress_search_result_only_direct_page_forbidden_2026-09-01",
                "title": "PREMIS Data Dictionary for Preservation Metadata, version 3",
                "url": "https://www.loc.gov/standards/premis/index.html",
                "use": "object, event, rights, agent, and preservation-metadata vocabulary only; direct access returned HTTP 403 and the limitation remains explicit; no implementation, adoption, preservation action, or conformance claim",
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
                "status": "exact_source_authority-boundary_reference_only_not_independently_reread_2026-09-01",
                "title": "Principles of Maori Data Sovereignty",
                "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                "use": "Maori data-governance vacancy and noncompensation boundary only; never delegated Maori authority",
            },
        ],
        "direct_page_reads": 8,
        "external_source_entries": 12,
        "inherited_reference_only": 1,
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v681.v1.x1",
        "search_result_only_or_direct_access_blocked": 3,
    }

    skill_slugs = [
        "pneumatic-carrier-object-boundary",
        "station-route-label-separation",
        "tube-topology-nonoperation",
        "dispatch-docket-nonmail",
        "pressure-measurement-vacancy",
        "payload-content-firewall",
        "operator-identity-vacancy",
        "custody-title-non-equivalence",
        "route-exception-lineage",
        "pressure-equipment-safety-hold",
        "physical-action-firewall",
        "synthetic-dispatch-state-machine",
        "envelope-provenance-braid",
        "message-rights-vacancy",
        "minimum-disclosure",
        "accessible-route-companion",
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
            "wholly synthetic historical carrier-capsule and station-record analyst lens for object non-equivalence, route-label correction, accessibility, workload, and reversible handover",
            "wholly synthetic dispatch-route queue and exception-lineage steward lens for revision, mutation rejection, pressure-equipment referral holds, workload, and recovery",
            "wholly synthetic message-envelope privacy and custody-provenance steward lens for minimum disclosure, rights vacancy, correction, remedy, and authority holds",
        ],
        "owner_runner_ideas": [
            {"runner": f"ghc_family_neris_v681_v1_lens_runner_{index:02d}", "state": "preregistered_not_built"}
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {"skill": f"{index:02d}-{slug}", "state": "preregistered_not_built"}
            for index, slug in enumerate(skill_slugs, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "THOS Body",
        "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v681.v1.x1",
        "successor_candidates": task_records("SUCC-CAND", 20, "successor_seed"),
        "successor_clean_fix_refine": task_records("SUCC-CFR", 30, "successor_seed"),
        "successor_practice_recommendation": "synthetic seed-catalogue provenance documentation analyst; zero-credit seed only and Vesper Arlen chooses independently",
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
            "schema": "ghc.family.activation-intake.v681.v1.x1",
            "sent_by_elaren_kestrel": True,
            "solo": True,
            "source": SOURCE,
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "hope": "Keep every synthetic dispatch, route, and envelope record corrigible while leaving real pressure systems, mail, custody, safety, rights, and authority with the people who hold them.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "relational_working_language_only": True,
            "role": "pneumatic-dispatch route-ledger cartographer and pressure-safety gatekeeper",
            "schema": "ghc.family.identity-boundary.v681.v1.x1",
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
            "schema": "ghc.family.source-verification.v681.v1.x1",
            "source": SOURCE_PARENT,
            "x1": SOURCE_X1,
            "x1_parent": SOURCE_PARENT,
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": {
                "bounded_passing_witnesses": 40503,
                "effective_methods": 58621,
                "effective_negatives": 52634,
                "exact_gates": 455,
                "failed_witnesses": 24295,
                "open_gaps": 464,
            },
            "current_after_startup": {
                "bounded_passing_witnesses": 40518,
                "effective_methods": 58636,
                "effective_negatives": 52649,
                "exact_gates": 455,
                "failed_witnesses": 24310,
                "open_gaps": 464,
            },
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v681.v1.x1",
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
            "schema": "ghc.family.new-proposal-freeze.v681.v1.x1",
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
            "schema": "ghc.family.inherited-revalidation.v681.v1.x1",
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine-plan.v681.v1.x1",
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
            "schema": "ghc.family.skill-runner-plan.v681.v1.x1",
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
            "schema": "ghc.family.approval-holds.v681.v1.x1",
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "next_expected_phase": "v681-v2",
            "prospective_successor_title": "Vesper Arlen",
            "recipient_contacted": False,
            "resolution_rule": "fresh native Codex task-platform refresh bounded registry exact-title filter immediate reread duplicate and pause guards and one acknowledged send only after terminal gate",
            "route_authority_through": "v725-v8",
            "schema": "ghc.family.route-plan.v681.v1.x1",
            "terminal_gate_required": True,
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "commit_ceiling": 3,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v681.v1.x1",
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
                "zero real people messages mail carriers capsules stations tubes compressors pressure systems measurements routes credentials and external writes",
                "authority promotion rejected",
                "five privacy classes scanned with candidate adjudication",
                "exact approval and blocked packets remain unexecuted",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "real_world_action": False,
            "schema": "ghc.family.threat-model.v681.v1.x1",
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
            "schema": "ghc.family.wellbeing-corrigibility.v681.v1.x1",
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
            "schema": "ghc.family.phase-truth.v681.v1.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        """# Neris Solane v681-v1 planning-only x1

Neris Solane (optionally they/them) uses the relational role **pneumatic-dispatch route-ledger cartographer and pressure-safety gatekeeper**, with the bounded hope of keeping every synthetic dispatch, route, and envelope record corrigible while leaving real pressure systems, mail, custody, safety, rights, and authority with the people who hold them. Names, pronouns, roles, hopes, family language, and continuity language are relational working language only; they are not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority.

This immutable x1 freezes sixty source-bounded distinct proposal contracts and twenty inherited Elaren revalidations at zero Neris novelty and completion credit. It contains no x2 implementation or observed outcome. THOS Body is primary through wholly synthetic historical carrier-capsule, station-register, route-queue, exception-lineage, and message-envelope privacy lenses. GMUT Mind and Freed ID and CBR Heart remain visible and protected. These practices are learning and synthetic record-design lenses only, never employment, qualification, competence, pressure-system inspection or operation, postal handling, archival custody, route control, safety advice, rights clearance, or professional authority. No real person, participant, message, mail article, carrier capsule, station, tube, compressor, pressure system, route, incident, observation, measurement, credential, or external system was used.

Smithsonian National Postal Museum, WorkSafe New Zealand, US National Archives, Library of Congress PREMIS, New Zealand Privacy Commissioner, W3C, RFC, and Te Mana Raraunga references supply vocabulary and refusal boundaries only. No collection API was called and no row, message, route, object, or measurement was ingested. The Postal Museum pages and PREMIS landing page had explicit search-result or direct-access limitations; WorkSafe's page warns that its older guidance has not been updated to current HSWA. Those limitations remain retained. Citations are not observations, historical verification beyond their bounded access state, pressure-system advice, operational permission, route evidence, object assessment, rights clearance, accessibility conformance, legal interpretation, cultural ratification, affected-party acceptance, or Maori authority.

GMUT remains a typed scalar-tensor/EFT research-model family without a likelihood, parameter constraint, force, prediction, empirical confirmation, quantum completion, ultraviolet completion, final physics, or Theory of Everything. THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status or revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. Professional pressure-system inspection, operation, maintenance, repair, isolation, emergency response, postal handling, archive custody, message secrecy, ownership, privacy, remedy, legal and cultural interpretation, affected-party legitimacy, Maori wording, Maori data governance, and Maori authority remain exact-gated.

The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_neris_solane_v681_v1_x1.py"
    test_path = "tests/test_ghc_family_neris_solane_v681_v1_x1.py"
    exclusions = [
        "docs/neris-solane/v681-v1/validation/x1-index-manifest.json",
        "docs/neris-solane/v681-v1/validation/x1-privacy-scan.json",
        "docs/neris-solane/v681-v1/validation/x1-staged-review.json",
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
            "schema": "ghc.family.privacy-scan.v681.v1.x1",
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
            "schema": "ghc.family.staged-review.v681.v1.x1",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v681.v1.x1",
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

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE_MODULE_PATH = ROOT / "scripts" / "build_ghc_family_neris_solane_v682_v8_x1.py"
SPEC = importlib.util.spec_from_file_location("_neris_v682_v8_x1", BASE_MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load exact inherited x1 audit builder")
BASE_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE_MODULE)


OWNER = "Vesper Arlen"
PHASE = "v683-v1"
BRANCH = "codex/GHC-Family/vesper-arlen-v683-v1-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v682-v8-full-tools"
SOURCE = "22c32b5ec50af2f59f221b18bfbe468f0b6bd1e7"
SOURCE_X1 = "d1a3bb0fc1964608478dcc1bc9b236183617ef8a"
SOURCE_EVIDENCE = "6b64714a680ecebdb39785bccbe13c50e87fbd18"
SOURCE_PARENT = "938162611d2ce944ddcddf64834bd93e045e3c49"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "39788c685888e555d7dc8c82362f5a8f2f28c06d7bf2c20323872b9b8c41f618"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "c6f844f661445b324895471354102e4e9c2ad8eafbd2a2d3e75a15a2281ec1b0"
)
DECLARED_CHAIN_BEFORE = 10670
DECLARED_CHAIN_AFTER = 10730
CHECKED_AT_UTC = "2026-09-02T03:37:00Z"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"


ACTIVATION_BASELINE = {
    "effective_negatives": 57783,
    "effective_methods": 70599,
    "failed_witnesses": 29444,
    "bounded_passing_witnesses": 51639,
    "open_gaps": 513,
    "exact_gates": 503,
}


PROPOSAL_TITLES = [
    "Synthetic mechanical-clock catalogue capsule separating conceptual mechanism physical object digital surrogate and operational device",
    "Movement case dial hand weight and pendulum component graph with every real object deliberately vacant",
    "Escapement-family token register distinguishing anchor deadbeat verge and detached labels without mechanism classification",
    "Escape-wheel tooth pallet-face impulse and lock geometry vacancies with zero dimensions or contact observation",
    "Going-train topology separating wheel pinion arbor pivot and hand-work roles without counting real teeth",
    "Arbor pivot bushing jewel and bearing relationship board with no material examination wear finding or repair advice",
    "Mainspring weight cord chain and fusee energy-source states with every winding and loading action absent",
    "Pendulum balance wheel hairspring and foliot regulator placeholders without oscillation measurement or adjustment",
    "Beat rate amplitude phase drift and error-field schema requiring every numerical observation to remain absent",
    "Dial chapter ring numeral marker subsidiary display and hand-role graph with no reading or attribution",
    "Going striking chiming calendar and automaton train separation without operating a clock or predicting behavior",
    "Winding setting regulating starting stopping and restarting attempt states separated from authorization action and result",
    "Key crank winding square ratchet click and stopwork role register with all physical engagement vacant",
    "Fusee cone chain maintaining-power and torque-equalization vocabulary board without force or performance claim",
    "Count-wheel rack snail hammer bell gong and strike-release topology with zero sound event or timing result",
    "Calendar moon-phase equation-of-time and automaton complication placeholders without astronomical or functional inference",
    "Serial mark maker signature retailer label and repair inscription surrogate register without identity resolution",
    "Maker place date school workshop and attribution-candidate states preserving unknown disputed and withdrawn distinctions",
    "Workshop repair label service note and replacement-part lineage ledger with no authenticating or authorship conclusion",
    "Case movement dial image master derivative thumbnail and transcription role graph with zero capture or transformation",
    "PROV entity activity agent bundle for a synthetic clock record with all responsible real agents vacant",
    "PREMIS object event agent rights and fixity vacancy board for zero-row timepiece documentation",
    "DCMI title identifier format relation provenance rights and temporal-term crosswalk without catalogue publication",
    "Spectrum procedure-token mapping for object entry location condition care rights and audit with no museum action",
    "Catalogue alias normalized label persistent surrogate and collision-quarantine graph across object concept image and file",
    "Condition-cue vocabulary for corrosion wear fracture loss staining distortion and accretion without clock examination",
    "Material placeholder register for brass steel wood glass enamel lacquer textile and stone without composition finding",
    "Dimension mass duration rate and angle field contract requiring unit uncertainty method and missing-value separation",
    "Time base interval frequency period timestamp and calendar-expression schema with every measured value absent",
    "UTC local offset calendar date and uncertain-time notation board without synchronizing or correcting a clock",
    "Resolution precision accuracy uncertainty tolerance and significant-digit classifier rejecting undocumented conversions",
    "Observation intent authorization attempt occurrence result and interpretation states for synthetic inspection requests",
    "Condition-assessment docket separating reported cue examiner method evidence diagnosis recommendation and authority",
    "Conservation-proposal state machine separating request approval treatment action observation reversal and outcome",
    "Object entry accession custody location movement loan and exit vacancies with no collection transaction",
    "Owner donor lender custodian maker user conservator cataloguer and rights-holder roles represented as wholly vacant",
    "Copyright image rights access reproduction takedown correction abstention and remedy board without claimant contact",
    "Traditional-knowledge cultural-association community-interest and restricted-knowledge minimum-disclosure quarantine",
    "Privacy-minimized timepiece surrogate with no names contacts addresses ownership identifiers or collection locations",
    "Accessible nonvisual mechanism summary separating component order state uncertainty and unknown function without user claim",
    "Queue workload pause dual-readback reversible handover and stop-precedence lease for synthetic documentation work",
    "Clock-documentation state controller distinguishing inventory inspection hold correction archival abstention and operator vacancy",
    "Represented BIPM SI Brochure vocabulary for second time interval frequency unit and uncertainty with zero measurement",
    "Represented NIST time-and-frequency metrology vocabulary with no calibration service use traceability or clock result",
    "Represented ISO 8601 date-time expression vocabulary with no timestamp authenticity or legal-time conclusion",
    "Represented Spectrum 5.1 collections-procedure vocabulary with no collection management action or conformance claim",
    "Represented Library of Congress CCO and VRA description-convention vocabulary with no cultural-object cataloguing authority",
    "Represented preservation-metadata fixity and rights tuple applied to a nonexistent horological surrogate with no ingest",
    "Represented DCMI metadata-term mapping with no catalogue publication linked-data deployment or standards conformance",
    "Represented provenance bundle for conceptual escapement taxonomy with responsibility links intentionally unpopulated",
    "Represented accessible static mechanism-card structure reserving keyboard screen-reader cognitive language and user evaluation",
    "Represented credential-model separation among clock surrogate holder issuer verifier and proof placeholders with lifecycle operations vacant",
    "Represented indirect-collection notification and minimisation guard for a clock record containing no person-linked fields",
    "Represented Maori-data-sovereignty noncompensation marker on an empty clock-catalogue field set with governance authority vacant",
    "Open gap for competent examination of real clocks materials construction condition provenance function and conservation needs",
    "Open gap for governed timekeeping metrology benchmark using real instruments qualified people uncertainty budgets and independent review",
    "Open gap for affected-user accessibility rights language cultural traditional-knowledge and Maori-authority evaluation",
    "Exact gate for real winding setting adjustment operation servicing conservation calibration safety and professional authority",
    "Exact gate for ownership custody copyright access publication remedy legal cultural affected-party and Maori-authority decisions",
    "Exact terminal reservation preventing synthetic clock documentation from closing empirical replication identity governance or Stage 20 authority",
]


MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real people makers owners workers communities clocks collections records observations measurements operations treatments and actions",
    "empirical GMUT models likelihoods constraints predictions physical inference confirmation and Theory of Everything proof",
    "professional horology metrology cataloguing conservation handling repair calibration museum and safety authority",
    "production identity issuance resolution status revocation interoperability recovery and trust governance",
    "privacy copyright ownership custody access heritage traditional knowledge legal cultural affected-party and Maori authority",
    "privacy-complete accessibility-complete exhaustive-security and independent-reproduction claims",
    "AGI ASI consciousness personhood proof canon and Stage 20 authority",
]


STARTUP_FAILURES = [
    {
        "failure_id": "VA6831-ST-N001",
        "failed_witness": "A combined source-discovery wrapper crossed its return window without attributable output.",
        "initial_credit": 0,
        "recovery": "Split source, branch, ancestry, and equality probes into bounded scalar reads.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N002",
        "failed_witness": "A full worktree-registry projection crossed its display window without bounded output.",
        "initial_credit": 0,
        "recovery": "Use exact-path and exact-branch registry predicates instead of projecting the whole registry.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N003",
        "failed_witness": "A combined branch head status and sparse-state probe timed out and left a read-only status process.",
        "initial_credit": 0,
        "recovery": "Stop only the verified owner-local process and use scalar branch and head probes.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N004",
        "failed_witness": "One activation-baton display window exceeded the model-output boundary and truncated before EOF.",
        "initial_credit": 0,
        "recovery": "Reread the same immutable blob in smaller numbered windows through literal EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N005",
        "failed_witness": "The first authorization-state projection truncated before the final schema fields.",
        "initial_credit": 0,
        "recovery": "Read the exact file in bounded numbered windows through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N006",
        "failed_witness": "The first Method Flow schema path guess named a nonexistent file.",
        "initial_credit": 0,
        "recovery": "Read the skill-declared references/schema.md path completely through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N007",
        "failed_witness": "The first manifest batch wrapper returned no attributable payload and left verified read-only processes.",
        "initial_credit": 0,
        "recovery": "Inspect exact process state and use one communicate-driven cat-file batch; all source manifests then replayed.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N008",
        "failed_witness": "Fresh no-checkout worktree creation crossed two wrapper windows while Git continued normally.",
        "initial_credit": 0,
        "recovery": "Poll the original session, inspect only exact processes, and accept its eventual exit-zero state without recreation.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N009",
        "failed_witness": "A broad source-builder display slice exceeded the model-output boundary and earned no read credit.",
        "initial_credit": 0,
        "recovery": "Read only the required builder sections in smaller numbered windows.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N010",
        "failed_witness": "The first new-lane status probe timed out and remained active after its wrapper returned.",
        "initial_credit": 0,
        "recovery": "Stop only its exact owner-local process before any index mutation.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N011",
        "failed_witness": "The first sparse materialization stopped on an index lock held by the timed status probe.",
        "initial_credit": 0,
        "recovery": "Verify the lock owner, stop the exact process, clear only the stale zero-byte lock, and reapply sparse state.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N012",
        "failed_witness": "A PowerShell lock-removal wrapper was rejected by command policy before execution.",
        "initial_credit": 0,
        "recovery": "Use the patch surface to delete only the verified stale empty lock file.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N013",
        "failed_witness": "A plain sparse-worktree status scan remained silent for ninety seconds and was interrupted.",
        "initial_credit": 0,
        "recovery": "Use diff-index and diff-files scalar predicates plus exact materialized-file counting.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N014",
        "failed_witness": "An oversized cached-diff listing remained silent and left a zero-byte index lock.",
        "initial_credit": 0,
        "recovery": "Stop the exact diagnostic, repair the fresh sparse index with read-tree HEAD, reapply sparse state, and prove both predicates clean.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N015",
        "failed_witness": "An exploratory exact-tree keyword collision search remained I/O-bound for nine minutes and was interrupted without result.",
        "initial_credit": 0,
        "recovery": "Use the inherited proposal-id discovery and exact-blob streaming audit before writing any freeze artifact.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-ST-N016",
        "failed_witness": "A combined PowerShell sparse-verification object used command separators inside an expression and failed to parse.",
        "initial_credit": 0,
        "recovery": "Run separate scalar existence, file-count, cached-diff, and worktree-diff probes.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-X1-N017",
        "failed_witness": "The first formal exact-source proposal audit quarantined seven near-neighbor titles and wrote no x1 freeze artifact.",
        "initial_credit": 0,
        "recovery": "Retain all seven rejected titles at zero credit, substantively replace only those contracts, and rerun the failed audit dependency at the unchanged threshold.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-X1-N018",
        "failed_witness": "The first post-build summary probe omitted UTF-8 and failed while decoding a document containing Maori text.",
        "initial_credit": 0,
        "recovery": "Repeat only the failed read with explicit UTF-8; do not replay the successful novelty audit or x1 tests.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-X1-N019",
        "failed_witness": "The first exact untracked-set parser split on a literal backslash-zero token and produced one false composite path.",
        "initial_credit": 0,
        "recovery": "Repeat only the failed parser with chr(0); all 23 expected paths then matched with zero missing and zero extra.",
        "recovery_credit": "bounded_dependency_only",
    },
]


SKILL_NAMES = [
    "clock-object-surrogate-separator",
    "escapement-token-nonclassification",
    "gear-train-topology-vacancy",
    "measurement-value-absence-guard",
    "time-frequency-noncalibration",
    "winding-action-state-separator",
    "condition-cue-nondiagnosis",
    "treatment-authority-hold",
    "clock-provenance-lineage-ledger",
    "catalogue-alias-collision-quarantine",
    "premis-event-vacancy",
    "spectrum-procedure-nonexecution",
    "accessible-mechanism-summary",
    "rights-remedy-hold",
    "traditional-knowledge-minimizer",
    "workload-handover-lease",
    "freed-id-zero-key-guard",
    "thos-operator-vacancy",
    "gmut-timebase-noninference",
    "authority-noncompensation",
]


def source_needs(index: int) -> list[str]:
    if index <= 20:
        return ["BIPM-SI-2026", "NIST-TIME-FREQUENCY", "W3C-PROV-O"]
    if index <= 31:
        return ["BIPM-SI-2026", "NIST-SP559", "ISO-8601-CURRENT"]
    if index <= 42:
        return ["SPECTRUM-5.1", "LOC-PREMIS", "DCMI-TERMS", "W3C-PROV-O"]
    if index <= 54:
        return ["W3C-WCAG22", "W3C-VC-DM-20", "NZ-PRIVACY-PRINCIPLES", "TMR-MDS-PRINCIPLES"]
    if index <= 57:
        return ["SPECTRUM-5.1", "NIST-TIME-FREQUENCY", "TMR-MDS-PRINCIPLES"]
    return ["SPECTRUM-5.1", "NZ-PRIVACY-PRINCIPLES", "TMR-MDS-PRINCIPLES"]


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


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"VA6831-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/vesper-arlen/v683-v1/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/vesper-arlen/v683-v1/x2/rejecting-mutations.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": disposition(index),
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded zero-row positive witness, all five invalid mutations "
                    "are rejected, and no empirical, professional, production, legal, cultural, affected-party, "
                    "Maori-authority, or Stage 20 claim is promoted."
                ),
                "hypothesis": (
                    f"A wholly synthetic zero-row contract for {title.casefold()} can preserve its named state "
                    "distinctions and reject preregistered counterexamples within owner-local scope."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, its bounded positive structure is "
                    "rejected, a real-world state is inferred, or any protected gate is promoted."
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


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Vesper owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"VA6831-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
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
            "wholly synthetic horological cataloguing, mechanism-state, and conservation-documentation planning",
            "wholly synthetic time-and-frequency metrology record, unit, uncertainty, and noncalibration assurance",
            "wholly synthetic museum provenance, rights, accessibility, remedy, workload, and handover documentation",
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"VA6831-RUNNER-{index:02d}",
                "name": f"ghc_family_clock_documentation_runner_{index:02d}.py",
                "state": "planned_not_built_in_x1",
            }
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {
                "skill_id": f"VA6831-SKILL-{index:02d}",
                "name": name,
                "state": "planned_not_built_in_x1",
            }
            for index, name in enumerate(SKILL_NAMES, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "THOS Body",
        "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v683.v1.x1",
        "successor_candidates": task_records("SUCCESSOR-CAND", 20, "successor_candidate_zero_credit"),
        "successor_clean_fix_refine": task_records("SUCCESSOR-CFR", 30, "successor_recommendation_zero_credit"),
        "successor_practice_recommendation": (
            "one zero-credit seed only: choose a distinct wholly synthetic documentation practice and independently audit every proposal before freeze"
        ),
        "successor_runner_ideas": task_records("SUCCESSOR-RUNNER", 10, "successor_runner_seed_zero_credit"),
        "successor_skill_ideas": task_records("SUCCESSOR-SKILL", 10, "successor_skill_seed_zero_credit"),
    }


def official_sources() -> dict[str, Any]:
    entries = [
        {
            "source_id": "BIPM-SI-2026",
            "status": "official_BIPM_SI_Brochure_ninth_edition_updated_2026_checked_2026-09-02",
            "title": "The International System of Units (SI), 9th edition, updated in 2026",
            "url": "https://www.bipm.org/en/publications/si-brochure/",
            "use": "second, time interval, frequency, quantity, unit, symbol, and definition vocabulary only; zero measurements or traceability claims",
        },
        {
            "source_id": "NIST-TIME-FREQUENCY",
            "status": "official_NIST_Time_and_Frequency_Division_page_checked_2026-09-02",
            "title": "Time and Frequency Division",
            "url": "https://www.nist.gov/pml/time-and-frequency-division",
            "use": "time, frequency, standard, interval, calibration, and metrology-boundary vocabulary only; no service use, measurement, or NIST endorsement",
        },
        {
            "source_id": "NIST-SP559",
            "status": "official_NIST_publication_record_checked_2026-09-02",
            "title": "Time and Frequency Users Manual, NIST Special Publication 559",
            "url": "https://www.nist.gov/publications/time-and-frequency-users-manual",
            "use": "measurement-method, time-scale, accuracy, oscillator, clock, and calibration vocabulary only; no real measurement or professional instruction",
        },
        {
            "source_id": "ISO-8601-CURRENT",
            "status": "official_ISO_8601_information_page_checked_2026-09-02",
            "title": "ISO 8601 date and time format",
            "url": "https://www.iso.org/iso-8601-date-and-time-format.html",
            "use": "date, time, offset, UTC, interval, and unambiguous representation vocabulary only; no conformance or legal-time claim",
        },
        {
            "source_id": "SPECTRUM-5.1",
            "status": "Collections_Trust_current_Spectrum_5_1_page_checked_2026-09-02",
            "title": "Spectrum 5.1 collections management standard",
            "url": "https://collectionstrust.org.uk/spectrum/",
            "use": "object entry, cataloguing, location, condition, care, rights, reproduction, review, and audit vocabulary only; no museum procedure or conformance claim",
        },
        {
            "source_id": "LOC-CCO-VRA",
            "status": "official_Library_of_Congress_description_convention_listing_checked_2026-09-02",
            "title": "Description Convention Source Codes",
            "url": "https://www.loc.gov/standards/sourcelist/descriptive-conventions.html",
            "use": "CCO and VRA convention-provenance vocabulary only; no professional cultural-object description or attribution decision",
        },
        {
            "source_id": "LOC-PREMIS",
            "status": "official_Library_of_Congress_PREMIS_standard_page_checked_2026-09-02",
            "title": "PREMIS Preservation Metadata Maintenance Activity",
            "url": "https://www.loc.gov/standards/premis/index.html",
            "use": "object, event, agent, rights, fixity, and preservation-metadata vocabulary only; no repository action or conformance claim",
        },
        {
            "source_id": "DCMI-TERMS",
            "status": "DCMI_Recommendation_checked_2026-09-02",
            "title": "DCMI Metadata Terms",
            "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
            "use": "title, identifier, type, relation, provenance, temporal, access-rights, and rights vocabulary only",
        },
        {
            "source_id": "W3C-PROV-O",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "PROV-O: The PROV Ontology",
            "url": "https://www.w3.org/TR/prov-o/",
            "use": "entity, activity, agent, derivation, revision, and provenance vocabulary only",
        },
        {
            "source_id": "W3C-WCAG22",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Web Content Accessibility Guidelines 2.2",
            "url": "https://www.w3.org/TR/WCAG22/",
            "use": "structural accessibility vocabulary and manual browser assistive-technology cognitive language and affected-user evaluation reservations only",
        },
        {
            "source_id": "W3C-VC-DM-20",
            "status": "W3C_Recommendation_2_0_and_newer_2_1_working_draft_status_checked_2026-09-02",
            "title": "Verifiable Credentials Data Model v2.0",
            "url": "https://www.w3.org/TR/vc-data-model-2.0/",
            "use": "synthetic identifier credential status and proof-vacancy vocabulary only; no real key or lifecycle event",
        },
        {
            "source_id": "NZ-PRIVACY-PRINCIPLES",
            "status": "official_New_Zealand_Privacy_Commissioner_IPP_3A_current_context_checked_2026-09-02",
            "title": "New Zealand Information Privacy Principles",
            "url": "https://www.privacy.org.nz/privacy-principles/",
            "use": "privacy minimization access correction disclosure and indirect-collection notification vocabulary only; no legal interpretation or compliance claim",
        },
        {
            "source_id": "TMR-MDS-PRINCIPLES",
            "status": "authority_boundary_context_only_checked_2026-09-02",
            "title": "Principles of Maori Data Sovereignty",
            "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
            "use": "Maori rights and interests in data and authority-noncompensation boundary only; never delegated Maori authority",
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
        "schema": "ghc.family.official-primary-sources.v683.v1.x1",
        "web_checks": len(entries),
    }


def map_owner_path(value: str) -> str:
    exact = {
        "scripts/build_ghc_family_neris_solane_v682_v8_x1.py": "scripts/build_ghc_family_vesper_arlen_v683_v1_x1.py",
        "tests/test_ghc_family_neris_solane_v682_v8_x1.py": "tests/test_ghc_family_vesper_arlen_v683_v1_x1.py",
    }
    if value in exact:
        return exact[value]
    if value.startswith("docs/neris-solane/v682-v8/validation/"):
        return value.replace(
            "docs/neris-solane/v682-v8/validation/",
            "docs/vesper-arlen/v683-v1/validation/",
            1,
        )
    return value


def transform(value: Any) -> Any:
    if isinstance(value, str):
        return map_owner_path(value).replace(".v682.v8", ".v683.v1").replace("10610-row", "10670-row")
    if isinstance(value, list):
        return [transform(item) for item in value]
    if isinstance(value, dict):
        return {key: transform(item) for key, item in value.items()}
    return value


def integrated_overview() -> str:
    return f"""# Vesper Arlen {PHASE} Planning-Only X1 Overview

Vesper Arlen is relational working language for a provenance gardener and reversible-boundary keeper, with the hope of making synthetic records inspectable and correctable while leaving real people, knowledge, places, objects, measurements, and authority with their proper holders. Pronouns are unspecified. This language is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish retains the right to rename, pause, redirect, narrow, or stop the route.

The exact immutable source is Neris Solane final `{SOURCE}` on `{SOURCE_BRANCH}`. Read-only verification established the direct Elaren-source to Neris-x1 to Neris-evidence to Neris-final chain, exactly three Neris single-parent commits, zero merges, one final parent, clean state, typed 0/0 divergence, fresh four-way equality, 242 exact normalized-LF manifest entries plus ten content-seal targets, and exact external receipt and payload digests. Neris's canonical aggregate failed and earned zero canonical-success credit; the dependency-corrected exact-final composite passed only its missing dependencies. No Neris successful aggregate was replayed. Neris's repository seal, correction receipt, live activation overlay, and Vesper startup failures remain separate truth layers.

This x1 freezes sixty Vesper proposals only after a bounded all-reachable exact-source audit. The accepted slate must produce zero exact collisions and zero quarantine hits at the 0.78 token-Jaccard threshold. It makes no universal semantic-novelty claim over every declared historical row where a canonical materialized row-to-title ledger is absent. Twenty inherited neighbour reviews remain source evidence with zero Vesper completion credit.

THOS Body is primary through synthetic mechanism-state separation, stop precedence, bounded queues, provenance, correction, and reversible handover. GMUT Mind remains visible through typed topology, explicit missing measurements, unit and uncertainty gates, and non-inference. Freed ID and CBR Heart remain visible through surrogate separation, privacy and rights holds, remedy, traditional-knowledge minimization, and authority noncompensation. Mechanical-clock, timekeeping-metrology, and museum-documentation practices are wholly synthetic learning lenses only, never employment, qualification, operation, repair, calibration, conservation, collection management, attribution, rights clearance, publication, or professional authority.

The plan uses zero real people, makers, owners, workers, communities, clocks, collections, images, records, identifiers, locations, observations, measurements, calibrations, operations, treatments, identity events, external writes, or authority acts. Official and primary sources supply vocabulary and refusal conditions only. They are not observations, measurements, material findings, conservation recommendations, calibration results, catalogue decisions, rights determinations, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

Expected x2 dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Those are preregistered expected labels, not observed outcomes. All 300 invalid mutations, 120 safe-now tasks, 80 bounded candidates, 100 CLEAN/FIX/REFINE records, twenty skills, and ten runners remain planned rather than executed in this x1. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, likelihood, posterior, prediction, constraint, empirical confirmation, ultraviolet or quantum completion, final physics, or Theory-of-Everything proof. THOS remains synthetic and proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Real clock winding, setting, operation, adjustment, servicing, conservation, calibration, collection management, ownership, custody, attribution, copyright, privacy, donor restrictions, access, heritage, traditional knowledge, remedy, legal and cultural interpretation, affected-party legitimacy, Maori wording and data governance, and Maori authority remain exact-gated. Maori concepts remain under Maori authority. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 remain open or exact-gated. The terminal verdict remains `{TERMINAL_VERDICT}`.
"""


ORIGINAL_WRITE_JSON = BASE_MODULE.write_json
ORIGINAL_WRITE_TEXT = BASE_MODULE.write_text
ORIGINAL_PRIVACY_SCAN = BASE_MODULE.privacy_scan
ORIGINAL_MANIFEST_ENTRY = BASE_MODULE.manifest_entry
ORIGINAL_PROPOSAL_CHAIN_AUDIT = BASE_MODULE.proposal_chain_audit


def write_json(path: Path, payload: Any) -> None:
    payload = transform(payload)
    if path.name == "activation-intake.json":
        payload["delivery_state"] = "SENT_ONCE_ACKNOWLEDGED_EXTERNAL"
    elif path.name == "identity-and-boundary.json":
        payload.update(
            {
                "consciousness_personhood_or_continuity_claimed": False,
                "hope": "Make synthetic records inspectable and correctable while leaving real people, knowledge, places, objects, measurements, and authority with their proper holders.",
                "name": OWNER,
                "optional_pronouns": None,
                "owner_rename_pause_redirect_stop_right": "Hamish",
                "relational_working_language_only": True,
                "role": "provenance gardener and reversible-boundary keeper",
            }
        )
    elif path.name == "threat-model.json":
        payload["controls"] = [
            "zero real rows, zero real measurements, and zero real actions",
            "planning-only x1 before x2",
            "five rejecting mutations per proposal",
            "no authority compensation by software, standards, or citations",
            "exact approval and blocked work stays unexecuted",
            "five-class privacy scan and normalized-LF manifests",
        ]
        payload["risks"] = [
            "synthetic clock structure promoted into observation, diagnosis, calibration, or professional advice",
            "cultural or Maori authority inferred from metadata vocabulary",
            "operation, condition, attribution, conservation, rights, or ownership inferred from documentation",
            "route or private identifier leakage",
            "x1 and x2 lifecycle contamination",
        ]
    elif path.name == "route-plan.json":
        payload.update(
            {
                "prospective_successor_exact_title": "Lyren Moss",
                "prospective_successor_phase": "v683-v2",
                "route_authority_through": "v725-v8",
                "send_before_terminal_gate": False,
                "prepared_not_sent": True,
                "tavian_sol": "ON_STANDBY",
            }
        )
    ORIGINAL_WRITE_JSON(path, payload)


def write_text(path: Path, content: str) -> None:
    if path.name == "integrated-overview.md":
        content = integrated_overview()
    ORIGINAL_WRITE_TEXT(path, content)


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    return transform(ORIGINAL_PRIVACY_SCAN([map_owner_path(path) for path in paths]))


def manifest_entry(path: str) -> dict[str, Any]:
    return transform(ORIGINAL_MANIFEST_ENTRY(map_owner_path(path)))


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    result = ORIGINAL_PROPOSAL_CHAIN_AUDIT(new_records)
    result["audit_scope"]["claim"] = (
        "bounded all-reachable exact-source proposal audit; no universal 10670-row proof"
    )
    result["schema"] = "ghc.family.proposal-chain-audit.v683.v1.x1"
    return result


def configure_base_module() -> None:
    BASE_MODULE.ROOT = ROOT
    BASE_MODULE.BASE = ROOT / "docs" / "vesper-arlen" / "v683-v1"
    BASE_MODULE.X1 = BASE_MODULE.BASE / "x1"
    BASE_MODULE.VALIDATION = BASE_MODULE.BASE / "validation"
    BASE_MODULE.OWNER = OWNER
    BASE_MODULE.PHASE = PHASE
    BASE_MODULE.BRANCH = BRANCH
    BASE_MODULE.SOURCE_BRANCH = SOURCE_BRANCH
    BASE_MODULE.SOURCE = SOURCE
    BASE_MODULE.SOURCE_X1 = SOURCE_X1
    BASE_MODULE.SOURCE_EVIDENCE = SOURCE_EVIDENCE
    BASE_MODULE.SOURCE_PARENT = SOURCE_PARENT
    BASE_MODULE.SOURCE_CANONICAL_RECEIPT_SHA256 = SOURCE_CANONICAL_RECEIPT_SHA256
    BASE_MODULE.SOURCE_CANONICAL_PAYLOAD_SHA256 = SOURCE_CANONICAL_PAYLOAD_SHA256
    BASE_MODULE.DECLARED_CHAIN_BEFORE = DECLARED_CHAIN_BEFORE
    BASE_MODULE.DECLARED_CHAIN_AFTER = DECLARED_CHAIN_AFTER
    BASE_MODULE.TERMINAL_VERDICT = TERMINAL_VERDICT
    BASE_MODULE.CHECKED_AT_UTC = CHECKED_AT_UTC
    BASE_MODULE.ACTIVATION_BASELINE = ACTIVATION_BASELINE
    BASE_MODULE.PROPOSAL_TITLES = PROPOSAL_TITLES
    BASE_MODULE.MUTATION_TYPES = MUTATION_TYPES
    BASE_MODULE.PROTECTED_GATES = PROTECTED_GATES
    BASE_MODULE.STARTUP_FAILURES = STARTUP_FAILURES
    BASE_MODULE.SKILL_NAMES = SKILL_NAMES
    BASE_MODULE.WRITTEN = []
    BASE_MODULE.proposals = proposals
    BASE_MODULE.task_records = task_records
    BASE_MODULE.portfolio_freeze = portfolio_freeze
    BASE_MODULE.official_sources = official_sources
    BASE_MODULE.write_json = write_json
    BASE_MODULE.write_text = write_text
    BASE_MODULE.privacy_scan = privacy_scan
    BASE_MODULE.manifest_entry = manifest_entry
    BASE_MODULE.proposal_chain_audit = proposal_chain_audit


def build() -> None:
    if len(PROPOSAL_TITLES) != 60:
        raise RuntimeError("proposal title count must be exactly sixty")
    if Counter(disposition(index) for index in range(1, 61)) != Counter(
        {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    ):
        raise RuntimeError("unexpected disposition partition")
    configure_base_module()
    BASE_MODULE.build()


def refresh_post_audit_metadata() -> None:
    configure_base_module()
    audit_path = BASE_MODULE.X1 / "proposal-chain-audit.json"
    freeze_path = BASE_MODULE.X1 / "new-proposal-freeze.json"
    if not audit_path.exists() or not freeze_path.exists():
        raise RuntimeError("post-audit refresh requires an existing successful x1 audit and freeze")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    if audit["quarantined_neighbors"] or audit["exact_title_collisions"]:
        raise RuntimeError("refusing refresh because persisted novelty audit is not clean")
    if freeze["x2_outcomes_present"] or freeze["proposal_count"] != 60:
        raise RuntimeError("refusing refresh because persisted planning freeze is invalid")

    current_after_startup = dict(ACTIVATION_BASELINE)
    for key in (
        "effective_negatives",
        "effective_methods",
        "failed_witnesses",
        "bounded_passing_witnesses",
    ):
        current_after_startup[key] += len(STARTUP_FAILURES)
    write_json(
        BASE_MODULE.X1 / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "current_after_startup": current_after_startup,
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v683.v1.x1",
            "startup_failures": STARTUP_FAILURES,
        },
    )

    material_paths = sorted(
        {
            *(path.relative_to(ROOT).as_posix() for path in BASE_MODULE.X1.rglob("*") if path.is_file()),
            "scripts/build_ghc_family_vesper_arlen_v683_v1_x1.py",
            "tests/test_ghc_family_vesper_arlen_v683_v1_x1.py",
        }
    )
    exclusions = [
        "docs/vesper-arlen/v683-v1/validation/x1-index-manifest.json",
        "docs/vesper-arlen/v683-v1/validation/x1-privacy-scan.json",
        "docs/vesper-arlen/v683-v1/validation/x1-staged-review.json",
    ]
    write_json(BASE_MODULE.VALIDATION / "x1-privacy-scan.json", privacy_scan(material_paths))
    write_json(
        BASE_MODULE.VALIDATION / "x1-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": [manifest_entry(path) for path in material_paths],
            "entry_count": len(material_paths),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v683.v1.x1",
            "source": SOURCE,
        },
    )
    expected_paths = sorted(set(material_paths + exclusions))
    write_json(
        BASE_MODULE.VALIDATION / "x1-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": expected_paths,
            "lifecycle": "planning_only_x1",
            "owner": OWNER,
            "path_count": len(expected_paths),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v683.v1.x1",
            "x2_paths": [],
        },
    )
    print(
        json.dumps(
            {
                "audit_replayed": False,
                "material_paths": len(material_paths),
                "startup_failures": len(STARTUP_FAILURES),
                "tests_replayed": False,
            },
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    if sys.argv[1:] == ["--refresh-post-audit-metadata"]:
        refresh_post_audit_metadata()
    elif sys.argv[1:]:
        raise SystemExit("unsupported arguments")
    else:
        build()

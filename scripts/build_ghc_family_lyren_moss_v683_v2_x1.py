from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INHERITED_PATH = ROOT / "scripts" / "build_ghc_family_vesper_arlen_v683_v1_x1.py"
SPEC = importlib.util.spec_from_file_location("_vesper_v683_v1_x1", INHERITED_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load exact inherited Vesper x1 builder")
INHERITED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INHERITED)
ENGINE = INHERITED.BASE_MODULE


OWNER = "Lyren Moss"
PHASE = "v683-v2"
BRANCH = "codex/GHC-Family/lyren-moss-v683-v2-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v683-v1-full-tools"
SOURCE = "484d44fb8875bf8129143c99e5340d2e2044fbd2"
SOURCE_X1 = "2981dcc774afce801973f8e3a9e6643b5e22dcee"
SOURCE_EVIDENCE = "40177e37035c377b5cb7d8d6d5c66f8de54ddbd0"
SOURCE_PARENT = "22c32b5ec50af2f59f221b18bfbe468f0b6bd1e7"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "62e4cdb99f5045d2616067d9691236ded6a11d9e787fe3c8c32dcc69a01106e2"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "5d8cfac40bb6342aa7bbce7d2767aeb5caacda89253025200ab7f5cdffb991a9"
)
SOURCE_ACTIVATION_PACKET_SHA256 = (
    "93aa78ad29db589e6e0185494910b9f101b4e42453bc5f489db10feba81db1a2"
)
SOURCE_LABEL_OVERLAY_SHA256 = (
    "f1d561653c5806698bbb7e9671a5723dd387ceb726beb2ba2cdf3f9bcfb82936"
)
SOURCE_ROUTE_OVERLAY_SHA256 = (
    "5ba772c1b476d2c30e04639648e9e8416d5a0b10803705a6fdc2dd4673e0685f"
)
SOURCE_DELIVERY_RECEIPT_SHA256 = (
    "40c743b19956798209063738fd4390e5136f08bc5d4718e3629cb37f29e57d0c"
)
DECLARED_CHAIN_BEFORE = 10730
DECLARED_CHAIN_AFTER = 10790
CHECKED_AT_UTC = "2026-09-02T05:39:58Z"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"


ACTIVATION_BASELINE = {
    "effective_negatives": 58114,
    "effective_methods": 71385,
    "failed_witnesses": 29775,
    "bounded_passing_witnesses": 52364,
    "open_gaps": 516,
    "exact_gates": 506,
}


PROPOSAL_TITLES = [
    "Synthetic sound-carrier capsule separating conceptual recording physical carrier digital surrogate and playback device",
    "Cylinder disc tape wire and grooved-media family token register without classifying any real carrier",
    "Core outer surface groove start end rim edge and molded-region vacancies with zero physical examination",
    "Recording stylus reproducing stylus horn diaphragm mandrel and feed-screw role graph without operation",
    "Container lid slip case sleeve label insert and carrier relationship board with every real object vacant",
    "Wax celluloid tinfoil shellac lacquer metal paper and polymer placeholders without material finding",
    "Diameter length thickness mass duration speed and channel fields requiring absent values and explicit units",
    "Groove direction pitch profile density start position and end position placeholders without measurement",
    "Rotational and linear speed token contract without measured value calibration playback or conversion",
    "Condition-cue vocabulary for crack chip split mold delamination deformation residue and loss without diagnosis",
    "Handling intent request authorization attempt occurrence observation and result states separated exactly",
    "Acclimation storage support orientation enclosure and environmental-advice tokens represented without handling",
    "Cleaning and treatment proposal lifecycle separating request approval action observation reversal and outcome",
    "Playback and digitization request approval extraction file creation review and result states with every action absent",
    "Stylus geometry tracking force equalization preamplifier converter and monitor placeholders with no signal chain",
    "Timebase sample-rate bit-depth channel-layout duration and level fields remaining absent without media conversion",
    "Audio essence physical carrier preservation file access derivative and metadata record roles separated",
    "Title performer speaker recordist engineer and contributor labels held vacant without identity inference",
    "Manufacturer label catalogue number matrix inscription date place and attribution candidates preserving unknown states",
    "Recording session location language genre subject and content-description vacancies without listening or transcription",
    "MARC 007 sound-recording carrier material speed channel and groove token map without cataloguing action",
    "PREMIS object event agent rights fixity and environment vacancy board for a zero-row sound surrogate",
    "PROV entity activity agent derivation revision and attribution graph with every responsible real agent vacant",
    "DCMI title identifier format relation provenance temporal access-rights and rights mapping without publication",
    "IASA identifier metadata extraction preservation storage planning and access vocabulary without procedure execution",
    "Library of Congress recommended-format audio vocabulary board with zero ingest conversion or endorsement claim",
    "National Archives audio preservation condition storage playback and digitization terms without archival action",
    "Carrier alias persistent surrogate normalized label and collision-quarantine graph across concept object file and record",
    "Fixity checksum derivative generation relationship and supersession tuple with no actual file or ingest event",
    "File-name container codec wrapper encoding and extension tokens without creating decoding or validating media",
    "Preservation master production master reference copy access copy and derivative roles with all files absent",
    "Intellectual content carrier instance digital representation metadata record and catalogue concept split",
    "Copyright donor restriction access permission takedown correction abstention and remedy state board without claimant contact",
    "Consent-bound provenance escrow for unplayed heritage-audio surrogates with contested descriptive labels isolated from public discovery",
    "Privacy-minimized sound-carrier surrogate with no names contacts addresses identifiers or collection locations",
    "Accessible transcript caption language summary and non-auditory alternative vacancies without affected-user claim",
    "Transcript translation correction supersession provenance and uncertainty lineage with no spoken content",
    "Queue workload pause dual-readback reversible handover stop precedence and lease expiry for synthetic records",
    "Sound-documentation controller distinguishing intake inventory hold correction archival refusal and operator vacancy",
    "Audit-event provenance revision supersession withdrawal and nondeletion graph retaining every failed witness",
    "Zero-key Freed ID holder issuer verifier credential status and proof lifecycle vacancy for sound surrogates",
    "Authority-noncompensation guard preventing software standards or citations from granting professional or cultural standing",
    "Represented IASA TC-04 metadata identifier signal-extraction preservation storage planning and access vocabulary",
    "Represented IASA ethical-principle and handling vocabulary with no custodial professional or rights determination",
    "Represented Library of Congress audiovisual care handling storage and emergency-planning vocabulary without action",
    "Represented Library of Congress recommended-format audio characteristics without conformance or ingest claim",
    "Represented National Archives audio condition storage playback digitization and preservation vocabulary without procedure",
    "Represented MARC 21 field 007 sound-recording categories without creating or validating a catalogue record",
    "Represented PREMIS preservation object event agent rights and fixity tuple for a nonexistent audio surrogate",
    "Represented DCMI metadata-term and PROV lineage mapping without linked-data publication or responsible agent",
    "Represented WCAG structural accessibility vocabulary while reserving manual assistive-technology and affected-user evaluation",
    "Represented credential separation among synthetic sound-surrogate holder issuer verifier proof and status placeholders",
    "Represented indirect-collection notice minimization access correction disclosure and remedy guard with zero person-linked fields",
    "Represented Maori-data-sovereignty authority-noncompensation marker on an empty sound-record field set",
    "Open gap for competent examination identification condition assessment and conservation planning for real sound carriers",
    "Open gap for governed playback digitization signal capture preservation storage and quality review with real equipment and people",
    "Unresolved governed evaluation dependency for disabled listeners rights holders donor communities and Maori data governors to assess access paths",
    "Exact gate for real handling cleaning treatment playback digitization conversion storage safety and professional authority",
    "Competent-authority stop for assigning title ownership donor covenants copyright duration access classes redress community governance or Maori data decisions",
    "Terminal nonpromotion latch where zero-row acoustic fixtures cannot establish real-world replication identity-system governance canonical physics or Stage 20 readiness",
]


MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real people communities carriers collections recordings files identities locations observations measurements and actions",
    "empirical GMUT models likelihoods constraints predictions physical inference confirmation and Theory of Everything proof",
    "professional archive library museum audio preservation cataloguing conservation handling playback digitization and safety authority",
    "production identity issuance resolution status revocation interoperability recovery and trust governance",
    "privacy copyright ownership custody access heritage traditional knowledge legal cultural affected-party and Maori authority",
    "privacy-complete accessibility-complete exhaustive-security and independent-reproduction claims",
    "AGI ASI consciousness personhood proof canon and Stage 20 authority",
]


STARTUP_FAILURES = [
    {
        "failure_id": "LM6832-ST-N001",
        "failed_witness": "The first whole activation-packet display exceeded its output boundary and truncated before EOF.",
        "initial_credit": 0,
        "recovery": "Reread the immutable packet in bounded numbered windows through literal EOF and verify its normalized-LF digest.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N002",
        "failed_witness": "A PowerShell guidance inventory piped an unmaterialized foreach expression and failed with EmptyPipeElement.",
        "initial_credit": 0,
        "recovery": "Materialize the bounded rows first and only then pipe the stable collection.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N003",
        "failed_witness": "A combined four-skill display exceeded the bounded output surface and earned no complete-read credit.",
        "initial_credit": 0,
        "recovery": "Read each required skill separately through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N004",
        "failed_witness": "A combined closeout skill-creator and memory-skill read truncated before all required EOFs.",
        "initial_credit": 0,
        "recovery": "Reread each affected file independently and include the skill-creator reference through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N005",
        "failed_witness": "The first authorization-state display truncated before the current-state EOF.",
        "initial_credit": 0,
        "recovery": "Reread the exact immutable file in four bounded line windows through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N006",
        "failed_witness": "A JavaScript orchestration string failed before command execution because PowerShell backticks broke the template.",
        "initial_credit": 0,
        "recovery": "Use a scalar command string without embedded backticks and verify the packet digest directly.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N007",
        "failed_witness": "A combined candidate-lane and tool preflight returned no attributable bounded payload.",
        "initial_credit": 0,
        "recovery": "Split exact branch path drive-capacity and version checks into scalar probes.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N008",
        "failed_witness": "The direct Library of Congress cylinder-care page open failed internally and its fallback fetch returned access denied.",
        "initial_credit": 0,
        "recovery": "Exclude that page from evidence and use only successfully read official audiovisual guidance.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N009",
        "failed_witness": "A dependency search guessed nonexistent inherited canonical and test paths.",
        "initial_credit": 0,
        "recovery": "Inspect exact Git-tree filenames and declared imports before materializing the dependency closure.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N010",
        "failed_witness": "The first sparse read-tree materialization produced no files and left cached paths appearing dirty.",
        "initial_credit": 0,
        "recovery": "Repair only the fresh owner index with read-tree HEAD and reapply the exact sparse patterns.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N011",
        "failed_witness": "The repaired sparse lane initially reported seventeen stat-only line-ending changes despite a zero content diff.",
        "initial_credit": 0,
        "recovery": "Verify zero actual diff and refresh only the owner index; diff-index and diff-files then both returned clean.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N012",
        "failed_witness": "A broad inherited x1-builder display exceeded the model-output boundary and truncated its middle section.",
        "initial_credit": 0,
        "recovery": "Read the required source sections in two smaller numbered windows.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-ST-N013",
        "failed_witness": "The first local test-path read assumed the inherited x1 test was already sparse-materialized and returned path not found.",
        "initial_credit": 0,
        "recovery": "Resolve the exact test path from the source Git tree and read the immutable blob directly.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-X1-N014",
        "failed_witness": "The first exact-source proposal audit stopped with one exact collision and four near-neighbor quarantines at the unchanged 0.78 token-Jaccard threshold.",
        "initial_credit": 0,
        "recovery": "Retain rejected proposal IDs LM6832-N034, LM6832-N057, LM6832-N059, and LM6832-N060 at zero credit, replace only those four contracts substantively, and rerun the failed audit dependency once.",
        "recovery_credit": "bounded_dependency_only",
    },
]


SKILL_NAMES = [
    "sound-carrier-object-surrogate-separator",
    "groove-token-nonmeasurement",
    "playback-action-state-separator",
    "audio-signal-vacancy-guard",
    "carrier-condition-nondiagnosis",
    "treatment-authority-hold",
    "digitization-nonexecution",
    "sound-provenance-lineage-ledger",
    "carrier-alias-collision-quarantine",
    "premis-audio-event-vacancy",
    "marc007-noncataloguing-map",
    "iasa-procedure-nonexecution",
    "accessible-transcript-vacancy",
    "audio-rights-remedy-hold",
    "traditional-knowledge-minimizer",
    "sound-workload-handover-lease",
    "freed-id-zero-key-audio-guard",
    "thos-playback-operator-vacancy",
    "gmut-audio-timebase-noninference",
    "sound-authority-noncompensation",
]


def source_needs(index: int) -> list[str]:
    if index <= 20:
        return ["IASA-TC04", "LOC-AV-CARE", "NARA-AUDIO-GUIDANCE"]
    if index <= 31:
        return ["LOC-MARC007-SOUND", "LOC-RFS-AUDIO", "LOC-PREMIS"]
    if index <= 42:
        return ["IASA-PUBLICATIONS", "DCMI-TERMS", "W3C-PROV-O"]
    if index <= 54:
        return ["W3C-WCAG22", "W3C-VC-DM-20", "NZ-PRIVACY-PRINCIPLES", "TMR-MDS-PRINCIPLES"]
    if index <= 57:
        return ["IASA-TC04", "LOC-AV-CARE", "TMR-MDS-PRINCIPLES"]
    return ["IASA-PUBLICATIONS", "NZ-PRIVACY-PRINCIPLES", "TMR-MDS-PRINCIPLES"]


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
        proposal_id = f"LM6832-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/lyren-moss/v683-v2/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/lyren-moss/v683-v2/x2/rejecting-mutations.json#{proposal_id}",
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
            "planned_action": f"Preregistered Lyren owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"LM6832-{prefix}-{index:03d}",
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
            "wholly synthetic sound-carrier cataloguing physical-description and nonclassification documentation",
            "wholly synthetic preservation-event digital-audio lineage and nonplayback assurance",
            "wholly synthetic rights accessibility traditional-knowledge remedy workload and handover documentation",
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"LM6832-RUNNER-{index:02d}",
                "name": f"ghc_family_sound_carrier_documentation_runner_{index:02d}.py",
                "state": "planned_not_built_in_x1",
            }
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {
                "skill_id": f"LM6832-SKILL-{index:02d}",
                "name": name,
                "state": "planned_not_built_in_x1",
            }
            for index, name in enumerate(SKILL_NAMES, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["GMUT Mind", "THOS Body"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v683.v2.x1",
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
            "source_id": "IASA-TC04",
            "status": "official_IASA_TC04_page_checked_2026-09-02",
            "title": "Guidelines on the Production and Preservation of Digital Audio Objects",
            "url": "https://www.iasa-web.org/tc04/audio-preservation",
            "use": "metadata, identifiers, signal extraction, preservation format, storage, planning, and access vocabulary only; no procedure execution",
        },
        {
            "source_id": "IASA-PUBLICATIONS",
            "status": "official_IASA_publications_page_checked_2026-09-02",
            "title": "IASA Special and Technical Publications",
            "url": "https://www.iasa-web.org/iasa-publications",
            "use": "ethical principles, handling, preservation and carrier guidance taxonomy only; no professional or rights determination",
        },
        {
            "source_id": "LOC-AV-CARE",
            "status": "official_Library_of_Congress_care_page_checked_2026-09-02",
            "title": "Care, Handling, and Storage of Audio Visual Materials",
            "url": "https://www.loc.gov/preservation/care/record",
            "use": "care, handling, storage and emergency-planning vocabulary only; no real handling or preservation advice",
        },
        {
            "source_id": "LOC-RFS-AUDIO",
            "status": "official_Library_of_Congress_RFS_audio_page_checked_2026-09-02",
            "title": "Recommended Formats Statement: Audio Works",
            "url": "https://www.loc.gov/preservation/resources/rfs/audio.html",
            "use": "audio format and technical-characteristic vocabulary only; no ingest conversion conformance or endorsement claim",
        },
        {
            "source_id": "NARA-AUDIO-GUIDANCE",
            "status": "official_National_Archives_audio_guidance_checked_2026-09-02",
            "title": "Audio Guidance",
            "url": "https://www.archives.gov/preservation/formats/audio-toc.html",
            "use": "condition, storage, playback, digitization and preservation vocabulary only; no archival action",
        },
        {
            "source_id": "LOC-MARC007-SOUND",
            "status": "official_Library_of_Congress_MARC21_checked_2026-09-02",
            "title": "MARC 21 Format for Bibliographic Data: 007 Sound Recording",
            "url": "https://www.loc.gov/marc/bibliographic/bd007s.html",
            "use": "carrier, material, speed, channel and groove category vocabulary only; no catalogue record creation or validation",
        },
        {
            "source_id": "LOC-PREMIS",
            "status": "official_Library_of_Congress_PREMIS_page_checked_2026-09-02",
            "title": "PREMIS Preservation Metadata Maintenance Activity",
            "url": "https://www.loc.gov/standards/premis/index.html",
            "use": "object, event, agent, rights, fixity and preservation-metadata vocabulary only; no repository action or conformance claim",
        },
        {
            "source_id": "DCMI-TERMS",
            "status": "DCMI_Recommendation_checked_2026-09-02",
            "title": "DCMI Metadata Terms",
            "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
            "use": "title, identifier, type, format, relation, provenance, access-rights and rights vocabulary only",
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
            "use": "structural accessibility vocabulary and manual assistive-technology cognitive language and affected-user evaluation reservations only",
        },
        {
            "source_id": "W3C-VC-DM-20",
            "status": "W3C_Recommendation_2_0_checked_2026-09-02",
            "title": "Verifiable Credentials Data Model v2.0",
            "url": "https://www.w3.org/TR/vc-data-model-2.0/",
            "use": "synthetic identifier credential status and proof-vacancy vocabulary only; no real key or lifecycle event",
        },
        {
            "source_id": "NZ-PRIVACY-PRINCIPLES",
            "status": "official_New_Zealand_Privacy_Commissioner_page_checked_2026-09-02",
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
        "failed_source_attempts": [
            {
                "credit": 0,
                "source": "Library of Congress cylinder-care page",
                "state": "internal_open_failure_then_access_denied",
                "used_as_evidence": False,
            }
        ],
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v683.v2.x1",
        "web_checks": len(entries),
    }


def map_owner_path(value: str) -> str:
    exact = {
        "scripts/build_ghc_family_neris_solane_v682_v8_x1.py": "scripts/build_ghc_family_lyren_moss_v683_v2_x1.py",
        "tests/test_ghc_family_neris_solane_v682_v8_x1.py": "tests/test_ghc_family_lyren_moss_v683_v2_x1.py",
    }
    if value in exact:
        return exact[value]
    if value.startswith("docs/neris-solane/v682-v8/validation/"):
        return value.replace(
            "docs/neris-solane/v682-v8/validation/",
            "docs/lyren-moss/v683-v2/validation/",
            1,
        )
    return value


def transform(value: Any) -> Any:
    if isinstance(value, str):
        return (
            map_owner_path(value)
            .replace("docs/neris-solane/v682-v8", "docs/lyren-moss/v683-v2")
            .replace("neris_solane_v682_v8", "lyren_moss_v683_v2")
            .replace("Neris Solane", OWNER)
            .replace("NS6828", "LM6832")
            .replace(".v682.v8", ".v683.v2")
            .replace("10610-row", "10730-row")
        )
    if isinstance(value, list):
        return [transform(item) for item in value]
    if isinstance(value, dict):
        return {key: transform(item) for key, item in value.items()}
    return value


def integrated_overview() -> str:
    return f"""# Lyren Moss {PHASE} Planning-Only X1 Overview

Lyren Moss is relational working language for an acoustic provenance cartographer and non-playback boundary keeper, with the hope of making archival sound-carrier descriptions inspectable and correctable without turning vocabulary into playback, identification, rights, cultural, professional, or authority claims. Pronouns are unspecified. This language is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish retains the right to rename, pause, redirect, narrow, or stop the route.

The exact immutable source is Vesper Arlen final `{SOURCE}` on `{SOURCE_BRANCH}`. Read-only verification established the direct Neris-source to Vesper-x1 to Vesper-evidence to Vesper-final chain, exactly three Vesper single-parent commits, zero merges, one final parent, clean state, typed 0/0 divergence, fresh four-way equality, 225 exact Git-blob manifest entries plus ten content-seal targets, and the exact canonical receipt, payload, activation, label-overlay, route-overlay, and delivery-receipt digests. Vesper's one owner-scoped canonical pass succeeded once and was not replayed. Vesper's repository seal and later external overlays remain distinct truth layers.

The successor-visible activation baseline is 58,114 effective negatives, 71,385 methods, 29,775 retained failed witnesses, 52,364 bounded passing witnesses, 516 open gaps, 506 exact gates, and `{TERMINAL_VERDICT}`. This x1 freezes sixty Lyren proposals only after a bounded all-reachable exact-source audit. The accepted slate must produce zero exact collisions and zero quarantine hits at the 0.78 token-Jaccard threshold. It makes no universal semantic-novelty claim over every declared historical row where a canonical materialized row-to-title ledger is absent. Twenty inherited neighbour reviews remain source evidence with zero Lyren completion credit.

Freed ID and CBR Heart are primary through surrogate and identity separation, provenance, privacy and rights holds, remedy, traditional-knowledge minimization, and authority noncompensation. GMUT Mind remains visible through typed carrier and signal topology, explicit missing measurements, unit and uncertainty gates, and non-inference. THOS Body remains visible through stop precedence, bounded queues, action-state separation, operator vacancy, correction, and reversible handover. Sound-carrier cataloguing, preservation-event documentation, digital-audio lineage, rights, and accessibility practices are wholly synthetic learning lenses only, never employment, qualification, listening, handling, playback, digitization, conservation, rights clearance, publication, or professional authority.

The plan uses zero real people, communities, carriers, collections, recordings, files, identifiers, locations, observations, measurements, playback, digitization, treatment, identity events, external writes, or authority acts. Official and primary sources supply vocabulary and refusal conditions only. They are not observations, condition findings, listening results, conservation recommendations, format validation, catalogue decisions, rights determinations, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

Expected x2 dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Those are preregistered expected labels, not observed outcomes. All 300 invalid mutations, 120 safe-now tasks, 80 bounded candidates, 100 CLEAN/FIX/REFINE records, twenty skills, and ten runners remain planned rather than executed in this x1. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, likelihood, posterior, prediction, constraint, empirical confirmation, ultraviolet or quantum completion, final physics, or Theory-of-Everything proof. THOS remains synthetic and proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Real carrier handling, cleaning, treatment, playback, digitization, conversion, storage, collection management, ownership, custody, attribution, copyright, privacy, donor restrictions, access, heritage, traditional knowledge, remedy, legal and cultural interpretation, affected-party legitimacy, Maori wording and data governance, and Maori authority remain exact-gated. Maori concepts remain under Maori authority. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 remain open or exact-gated. The terminal verdict remains `{TERMINAL_VERDICT}`.
"""


ORIGINAL_WRITE_JSON = INHERITED.ORIGINAL_WRITE_JSON
ORIGINAL_WRITE_TEXT = INHERITED.ORIGINAL_WRITE_TEXT
ORIGINAL_PRIVACY_SCAN = INHERITED.ORIGINAL_PRIVACY_SCAN
ORIGINAL_MANIFEST_ENTRY = INHERITED.ORIGINAL_MANIFEST_ENTRY
ORIGINAL_PROPOSAL_CHAIN_AUDIT = INHERITED.ORIGINAL_PROPOSAL_CHAIN_AUDIT


def write_json(path: Path, payload: Any) -> None:
    payload = transform(payload)
    if path.name == "activation-intake.json":
        payload.update(
            {
                "delivery_state": "SENT_ONCE_ACKNOWLEDGED_EXTERNAL",
                "source_activation_packet_sha256": SOURCE_ACTIVATION_PACKET_SHA256,
                "source_delivery_receipt_sha256": SOURCE_DELIVERY_RECEIPT_SHA256,
                "source_label_overlay_sha256": SOURCE_LABEL_OVERLAY_SHA256,
                "source_route_overlay_sha256": SOURCE_ROUTE_OVERLAY_SHA256,
            }
        )
    elif path.name == "identity-and-boundary.json":
        payload.update(
            {
                "consciousness_personhood_or_continuity_claimed": False,
                "hope": "Make archival sound-carrier descriptions inspectable and correctable without turning vocabulary into playback, identification, rights, cultural, professional, or authority claims.",
                "name": OWNER,
                "optional_pronouns": None,
                "owner_rename_pause_redirect_stop_right": "Hamish",
                "relational_working_language_only": True,
                "role": "acoustic provenance cartographer and non-playback boundary keeper",
            }
        )
    elif path.name == "source-verification.json":
        payload["manifest_replay"] = {
            "x1": 20,
            "evidence": 75,
            "final_delta": 23,
            "final_owner": 107,
            "total": 225,
            "mismatches": 0,
        }
        payload["content_seal_targets"] = 10
        payload["canonical_replayed"] = False
    elif path.name == "threat-model.json":
        payload["controls"] = [
            "zero real rows, zero real measurements, zero listening, and zero real actions",
            "planning-only x1 before x2",
            "five rejecting mutations per proposal",
            "no authority compensation by software, standards, or citations",
            "exact approval and blocked work stays unexecuted",
            "five-class privacy scan and normalized-LF manifests",
        ]
        payload["risks"] = [
            "synthetic sound-carrier structure promoted into listening, condition, format, preservation, or professional advice",
            "cultural or Maori authority inferred from metadata vocabulary",
            "identity, playback, digitization, treatment, rights, ownership, or access inferred from documentation",
            "route or private identifier leakage",
            "x1 and x2 lifecycle contamination",
        ]
    elif path.name == "route-plan.json":
        payload.update(
            {
                "prospective_successor_exact_title": "Ilyra Fen",
                "prospective_successor_phase": "v683-v3",
                "route_authority_through": "v725-v8",
                "send_before_terminal_gate": False,
                "prepared_not_sent": True,
                "tavian_sol": "ON_STANDBY",
            }
        )
    ORIGINAL_WRITE_JSON(path, payload)


def write_text(path: Path, content: str) -> None:
    content = transform(content)
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
        "bounded all-reachable exact-source proposal audit; no universal 10730-row proof"
    )
    result["schema"] = "ghc.family.proposal-chain-audit.v683.v2.x1"
    return result


def configure_engine() -> None:
    ENGINE.ROOT = ROOT
    ENGINE.BASE = ROOT / "docs" / "lyren-moss" / "v683-v2"
    ENGINE.X1 = ENGINE.BASE / "x1"
    ENGINE.VALIDATION = ENGINE.BASE / "validation"
    ENGINE.OWNER = OWNER
    ENGINE.PHASE = PHASE
    ENGINE.BRANCH = BRANCH
    ENGINE.SOURCE_BRANCH = SOURCE_BRANCH
    ENGINE.SOURCE = SOURCE
    ENGINE.SOURCE_X1 = SOURCE_X1
    ENGINE.SOURCE_EVIDENCE = SOURCE_EVIDENCE
    ENGINE.SOURCE_PARENT = SOURCE_PARENT
    ENGINE.SOURCE_CANONICAL_RECEIPT_SHA256 = SOURCE_CANONICAL_RECEIPT_SHA256
    ENGINE.SOURCE_CANONICAL_PAYLOAD_SHA256 = SOURCE_CANONICAL_PAYLOAD_SHA256
    ENGINE.DECLARED_CHAIN_BEFORE = DECLARED_CHAIN_BEFORE
    ENGINE.DECLARED_CHAIN_AFTER = DECLARED_CHAIN_AFTER
    ENGINE.TERMINAL_VERDICT = TERMINAL_VERDICT
    ENGINE.CHECKED_AT_UTC = CHECKED_AT_UTC
    ENGINE.ACTIVATION_BASELINE = ACTIVATION_BASELINE
    ENGINE.PROPOSAL_TITLES = PROPOSAL_TITLES
    ENGINE.MUTATION_TYPES = MUTATION_TYPES
    ENGINE.PROTECTED_GATES = PROTECTED_GATES
    ENGINE.STARTUP_FAILURES = STARTUP_FAILURES
    ENGINE.SKILL_NAMES = SKILL_NAMES
    ENGINE.WRITTEN = []
    ENGINE.proposals = proposals
    ENGINE.task_records = task_records
    ENGINE.portfolio_freeze = portfolio_freeze
    ENGINE.official_sources = official_sources
    ENGINE.write_json = write_json
    ENGINE.write_text = write_text
    ENGINE.privacy_scan = privacy_scan
    ENGINE.manifest_entry = manifest_entry
    ENGINE.proposal_chain_audit = proposal_chain_audit


def build() -> None:
    if len(PROPOSAL_TITLES) != 60:
        raise RuntimeError("proposal title count must be exactly sixty")
    if Counter(disposition(index) for index in range(1, 61)) != Counter(
        {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    ):
        raise RuntimeError("unexpected disposition partition")
    configure_engine()
    ENGINE.build()


def refresh_post_audit_metadata() -> None:
    configure_engine()
    audit_path = ENGINE.X1 / "proposal-chain-audit.json"
    freeze_path = ENGINE.X1 / "new-proposal-freeze.json"
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
        ENGINE.X1 / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "current_after_startup": current_after_startup,
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v683.v2.x1",
            "startup_failures": STARTUP_FAILURES,
        },
    )

    material_paths = sorted(
        {
            *(path.relative_to(ROOT).as_posix() for path in ENGINE.X1.rglob("*") if path.is_file()),
            "scripts/build_ghc_family_lyren_moss_v683_v2_x1.py",
            "tests/test_ghc_family_lyren_moss_v683_v2_x1.py",
        }
    )
    exclusions = [
        "docs/lyren-moss/v683-v2/validation/x1-index-manifest.json",
        "docs/lyren-moss/v683-v2/validation/x1-privacy-scan.json",
        "docs/lyren-moss/v683-v2/validation/x1-staged-review.json",
    ]
    write_json(ENGINE.VALIDATION / "x1-privacy-scan.json", privacy_scan(material_paths))
    write_json(
        ENGINE.VALIDATION / "x1-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": [manifest_entry(path) for path in material_paths],
            "entry_count": len(material_paths),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v683.v2.x1",
            "source": SOURCE,
        },
    )
    expected_paths = sorted(set(material_paths + exclusions))
    write_json(
        ENGINE.VALIDATION / "x1-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": expected_paths,
            "lifecycle": "planning_only_x1",
            "owner": OWNER,
            "path_count": len(expected_paths),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v683.v2.x1",
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

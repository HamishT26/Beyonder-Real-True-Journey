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


OWNER = "Ilyra Fen"
PHASE = "v683-v3"
BRANCH = "codex/GHC-Family/ilyra-fen-v683-v3-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v683-v2-full-tools"
SOURCE = "0f5210fc4899a3c36e1ca1e5c1b5c897eb9acc68"
SOURCE_X1 = "57dcd8a0e6e5a43f87d6f1a5a0d79d2d68b66d8b"
SOURCE_EVIDENCE = "d0240efd7c7369e1468882d62bebddce32cf8b85"
SOURCE_PARENT = "484d44fb8875bf8129143c99e5340d2e2044fbd2"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "88cee51a4ebebb0316fb3afe402548b07e8e17e604e95e425218ea4890488787"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "3214d43b9270c577c5dc2cc1d967914f55612797e2d8226d31005d7b0780394d"
)
SOURCE_ACTIVATION_PACKET_SHA256 = (
    "2bb9b168927ff6dd236e63a63da5557c42d378749a54bb9bc8b4ade98d76296c"
)
SOURCE_LABEL_OVERLAY_SHA256 = (
    "48ee757b485ddee56732e55fd215cdc0422d8651297a96f6b95d64de2b6bddd5"
)
SOURCE_ROUTE_OVERLAY_SHA256 = (
    "a5942d5ec489520507c53530c43ead5b413b5dee6ae61352aa3bc1490048ef11"
)
SOURCE_DELIVERY_RECEIPT_SHA256 = (
    "e5d2b56eed483ba91645e122229a4f38c787c09fcc8119c545d281a9181d01ee"
)
DECLARED_CHAIN_BEFORE = 10790
DECLARED_CHAIN_AFTER = 10850
CHECKED_AT_UTC = "2026-09-02T07:12:00Z"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"


ACTIVATION_BASELINE = {
    "effective_negatives": 58438,
    "effective_methods": 72164,
    "failed_witnesses": 30099,
    "bounded_passing_witnesses": 53082,
    "open_gaps": 519,
    "exact_gates": 509,
}


PROPOSAL_TITLES = [
    "Synthetic pneumatic-tube network separating route concept physical tube station capsule and documentation surrogate",
    "Dispatch capsule station and content-token register with every physical object and shipment explicitly vacant",
    "Origin junction destination return-loop and isolation-segment topology without surveying a real installation",
    "Pressure vacuum airflow blower receiver and exhaust role graph without operating or assessing machinery",
    "Tube bore run length bend radius elevation and clearance fields requiring absent values and explicit units",
    "Capsule diameter length mass seal and payload-capacity placeholders without measurement or compatibility finding",
    "Empty lifecycle matrix distinguishing desired dispatch permission token mechanical initiation sensed transition confirmed arrival and documented disposition",
    "Arrival detection receipt acknowledgement opening custody and return states with every real event absent",
    "Route occupancy queue capacity reservation expiry and vacancy ledger for zero synthetic traffic",
    "Diverter gate valve switch bypass and isolation-position tokens without control actuation",
    "Blower compressor motor filter receiver regulator and relief-device component roles without safety inference",
    "Capsule lid latch gasket seal tamper marker and closure-state vocabulary without inspection",
    "Station capsule route and consignment aliases with collision quarantine and no persistent real identifier",
    "Dispatch receipt clock timezone ordering latency and uncertainty fields without timestamps or performance claims",
    "Monotonic sequence duplicate replay stale-event and causal-order guards for an empty event stream",
    "Custody transfer sender carrier recipient witness and acknowledgment roles with every identity vacant",
    "Maintenance intent request approval isolation attempt action inspection and return-to-service states without work",
    "Jam obstruction slowdown vibration noise and temperature cues retained as nondiagnostic placeholders",
    "Leak pressure-loss seal-failure and airflow-anomaly vocabulary without measurement diagnosis or hazard finding",
    "Inspection request access authorization observation record correction and refusal stages without site entry",
    "Ambient temperature humidity dust moisture and corrosion-risk fields remaining absent and nonprescriptive",
    "Hazardous biological fragile confidential prohibited and unknown-content tokens enforcing documentation holds only",
    "Operator dispatcher maintainer sender recipient and affected-party fields remaining vacant without identity inference",
    "Station building room address coordinate jurisdiction and access-route fields explicitly absent",
    "Consignment manifest item count description mass destination and handling-instruction fields with zero contents",
    "Container content message document sample and parcel concepts separated from capsule and route records",
    "Duplicate dispatch identifier collision replay and split-brain quarantine without resending any capsule",
    "Lost late misrouted returned refused held and unknown states without attributing fault or operational occurrence",
    "Correction supersession withdrawal reinstatement and nondeletion lineage for synthetic dispatch records",
    "Audit-event provenance revision handover lease expiry and refusal graph retaining every failed witness",
    "Privacy-minimized tube-record surrogate with no names contacts addresses coordinates or route secrets",
    "Accessible linear dispatch-status summary with no affected-user evaluation or accessibility-complete claim",
    "Rights restriction access correction disclosure abstention remedy and appeal state board without claimant contact",
    "Traditional-knowledge cultural-content and community-authority vacancy marker preventing descriptive overreach",
    "Lineage graph joining synthetic capsule-description versions through creation derivation invalidation and accountable-agent vacancy",
    "Metadata crosswalk for synthetic route-record labels temporal scope relations access vocabulary and withheld publication",
    "Credential-role vacancy table for nonexistent dispatch claimant attester checker suspension state cryptographic material and recovery event",
    "THOS queue pause dual-readback reversible handover stop precedence and lease expiry for synthetic dispatches",
    "GMUT directed-route topology and uncertainty ledger without physical inference prediction or empirical claim",
    "Failure-first method witness retaining rejected mutations separately from bounded passing controls",
    "Workload saturation fatigue escalation pause and operator-vacancy board without monitoring real workers",
    "Nondelegation latch where vocabulary code citations and test success cannot confer engineering workplace cultural or Maori decision rights",
    "Represented PROV entity activity agent derivation revision and invalidation vocabulary without responsible real agent",
    "Represented DCMI identifier relation provenance temporal rights and access-rights terms without publication",
    "Represented perceivable operable understandable and robust structure tokens while reserving assistive-technology trials and affected-user acceptance",
    "Represented credential-data roles for nonexistent dispatch subject attester presentation checker evidence token and suspension state",
    "Represented New Zealand privacy minimization access correction disclosure and remedy vocabulary with zero person-linked fields",
    "Represented Maori data sovereignty reservation where empty dispatch metadata cannot replace collective rights relationships interests or authority",
    "Represented units uncertainty dimensional consistency and missing-value vocabulary without engineering calculation",
    "Represented directed-graph station segment junction and route topology without installation modelling",
    "Represented guarded state-machine vocabulary for request authorization attempt occurrence observation and result",
    "Represented normalized-LF fixity manifest revision supersession and nondeletion lineage for synthetic records",
    "Represented linear text alternative status summaries without accessibility completeness or user acceptance",
    "Represented dual-readback handover pause stop precedence lease expiry and operator-vacancy controls",
    "Open gap for competent survey identification condition assessment and engineering documentation of a real tube installation",
    "Open gap for governed pressure airflow electrical functional safety and fault testing with real equipment and qualified people",
    "Open gap for affected workers senders recipients privacy holders communities and Maori data governors to evaluate real use",
    "Exact gate for real dispatch operation maintenance isolation testing pressure safety workplace action and professional authority",
    "Competent-authority stop for legal access privacy employment safety cultural heritage community governance or Maori decisions",
    "Terminal nonpromotion latch where zero-row pneumatic fixtures cannot establish deployment replication identity governance canonical physics or Stage 20 readiness",
]


MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real people communities stations tubes capsules contents identities locations observations measurements and actions",
    "empirical GMUT models likelihoods constraints predictions physical inference confirmation and Theory of Everything proof",
    "professional mechanical systems transport archive workplace electrical pressure maintenance operation and safety authority",
    "production identity issuance resolution status revocation interoperability recovery and trust governance",
    "privacy copyright ownership custody access heritage traditional knowledge legal cultural affected-party and Maori authority",
    "privacy-complete accessibility-complete exhaustive-security and independent-reproduction claims",
    "AGI ASI consciousness personhood proof canon and Stage 20 authority",
]


STARTUP_FAILURES = [
    {
        "failure_id": "IF6833-ST-N001",
        "failed_witness": "The first repository probe assumed C:/Users/hamis/.codex was a Git worktree and failed with not-a-repository before source discovery.",
        "initial_credit": 0,
        "recovery": "Locate the exact Lyren branch in the D-first worktree registry and perform every Git predicate there.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-ST-N002",
        "failed_witness": "A PowerShell skill-size inventory piped an unmaterialized foreach expression and failed with EmptyPipeElement.",
        "initial_credit": 0,
        "recovery": "Materialize the bounded rows before piping and complete each required skill read independently through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-ST-N003",
        "failed_witness": "The first combined authorization-state display truncated before the current-state EOF.",
        "initial_credit": 0,
        "recovery": "Reread the immutable authorization state in four bounded windows through literal EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-ST-N004",
        "failed_witness": "The first broad canonical-template display exceeded the output boundary before the required helper section was attributable.",
        "initial_credit": 0,
        "recovery": "Read only the bounded replay-manifest helper window and inspect the persisted one-shot receipt instead of invoking the validator.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-ST-N005",
        "failed_witness": "A PowerShell manifest-schema inventory repeated the foreach-to-pipe parser edge and returned no schema table.",
        "initial_credit": 0,
        "recovery": "Materialize the five schema rows first and then inspect them as a stable collection.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-ST-N006",
        "failed_witness": "A dependency inventory assumed an absent runners directory and passed a Windows wildcard path directly to ripgrep; both reads failed without mutation.",
        "initial_credit": 0,
        "recovery": "Inspect exact existing scripts and tests directories and use ripgrep's explicit glob option.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-ST-N007",
        "failed_witness": "The first worktree-creation orchestration string failed JavaScript parsing because embedded PowerShell backticks terminated the template literal.",
        "initial_credit": 0,
        "recovery": "Use a PowerShell pattern array and splatting without embedded backticks.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-ST-N008",
        "failed_witness": "The combined no-checkout worktree wrapper ended after preparation without an attributable final-state summary.",
        "initial_credit": 0,
        "recovery": "Inspect the new lane and its sparse pattern file directly before continuing; do not rerun branch creation.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-ST-N009",
        "failed_witness": "The fresh no-checkout sparse lane exposed inherited cached deletions because its index had not yet been populated.",
        "initial_credit": 0,
        "recovery": "Populate only the new lane from exact HEAD with read-tree under the installed sparse patterns and require zero status rows before authoring.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-X1-N010",
        "failed_witness": "The first exact-source novelty audit rejected one exact title collision and eight titles at or above the unchanged 0.78 token-Jaccard quarantine threshold.",
        "initial_credit": 0,
        "recovery": "Retain rejected proposal IDs IF6833-N007, N035, N036, N037, N042, N045, N046, and N048 at zero credit, replace only those titles substantively, and rerun the failed audit dependency once.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-X1-N011",
        "failed_witness": "Eight untracked future x2, closeout, canonical, contract, skill, runner, and test templates were copied into the fresh lane before x1 was frozen.",
        "initial_credit": 0,
        "recovery": "Remove only those new untracked Ilyra future files, retain their premature presence at zero x2 credit, and require a planning-only x1 staged allowlist with no x2 paths before commit.",
        "recovery_credit": "planning_boundary_restoration_only",
    },
]


SKILL_NAMES = [
    "pneumatic-network-surrogate-separator",
    "station-route-capsule-vacancy-guard",
    "dispatch-action-state-separator",
    "pressure-airflow-nonmeasurement",
    "fault-cue-nondiagnosis",
    "maintenance-authority-hold",
    "route-control-nonexecution",
    "dispatch-provenance-lineage-ledger",
    "station-alias-collision-quarantine",
    "capsule-content-concept-separator",
    "custody-event-vacancy",
    "engineering-procedure-nonexecution",
    "accessible-status-summary-vacancy",
    "dispatch-rights-remedy-hold",
    "traditional-knowledge-minimizer",
    "tube-workload-handover-lease",
    "freed-id-zero-key-dispatch-guard",
    "thos-dispatch-operator-vacancy",
    "gmut-route-topology-noninference",
    "tube-authority-noncompensation",
]


def source_needs(index: int) -> list[str]:
    if index <= 42:
        return ["OWNER-SYNTHETIC-PNEUMATIC", "W3C-PROV-O"]
    if index == 43:
        return ["W3C-PROV-O"]
    if index == 44:
        return ["DCMI-TERMS"]
    if index == 45:
        return ["W3C-WCAG22"]
    if index == 46:
        return ["W3C-VC-DM-20"]
    if index == 47:
        return ["NZ-PRIVACY-PRINCIPLES"]
    if index == 48:
        return ["TMR-MDS-PRINCIPLES"]
    if index <= 54:
        return ["OWNER-SYNTHETIC-PNEUMATIC", "DCMI-TERMS", "W3C-WCAG22"]
    if index <= 57:
        return ["OWNER-SYNTHETIC-PNEUMATIC", "TMR-MDS-PRINCIPLES"]
    return ["OWNER-SYNTHETIC-PNEUMATIC", "NZ-PRIVACY-PRINCIPLES", "TMR-MDS-PRINCIPLES"]


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
        proposal_id = f"IF6833-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/ilyra-fen/v683-v3/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/ilyra-fen/v683-v3/x2/rejecting-mutations.json#{proposal_id}",
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
            "planned_action": f"Preregistered Ilyra owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"IF6833-{prefix}-{index:03d}",
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
            "wholly synthetic pneumatic transport topology and mechanical-systems documentation",
            "wholly synthetic archival metadata provenance custody and correction-lineage documentation",
            "wholly synthetic software verification rights accessibility workload refusal and reversible-handover assurance",
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"IF6833-RUNNER-{index:02d}",
                "name": f"ghc_family_pneumatic_tube_documentation_runner_{index:02d}.py",
                "state": "planned_not_built_in_x1",
            }
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {
                "skill_id": f"IF6833-SKILL-{index:02d}",
                "name": name,
                "state": "planned_not_built_in_x1",
            }
            for index, name in enumerate(SKILL_NAMES, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "THOS Body",
        "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v683.v3.x1",
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
            "source_id": "OWNER-SYNTHETIC-PNEUMATIC",
            "status": "owner_invented_zero_row_vocabulary_not_external_evidence",
            "title": "Ilyra synthetic pneumatic-tube documentation vocabulary",
            "url": None,
            "use": "invented station route capsule dispatch state and refusal tokens only; no engineering observation standard conformance or operating guidance",
        },
        {
            "source_id": "DCMI-TERMS",
            "status": "inherited_exact_source_reference_not_refetched",
            "title": "DCMI Metadata Terms",
            "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
            "use": "title, identifier, type, format, relation, provenance, access-rights and rights vocabulary only",
        },
        {
            "source_id": "W3C-PROV-O",
            "status": "inherited_exact_source_reference_not_refetched",
            "title": "PROV-O: The PROV Ontology",
            "url": "https://www.w3.org/TR/prov-o/",
            "use": "entity, activity, agent, derivation, revision and provenance vocabulary only",
        },
        {
            "source_id": "W3C-WCAG22",
            "status": "inherited_exact_source_reference_not_refetched",
            "title": "Web Content Accessibility Guidelines 2.2",
            "url": "https://www.w3.org/TR/WCAG22/",
            "use": "structural accessibility vocabulary and manual assistive-technology cognitive language and affected-user evaluation reservations only",
        },
        {
            "source_id": "W3C-VC-DM-20",
            "status": "inherited_exact_source_reference_not_refetched",
            "title": "Verifiable Credentials Data Model v2.0",
            "url": "https://www.w3.org/TR/vc-data-model-2.0/",
            "use": "synthetic identifier credential status and proof-vacancy vocabulary only; no real key or lifecycle event",
        },
        {
            "source_id": "NZ-PRIVACY-PRINCIPLES",
            "status": "inherited_exact_source_reference_not_refetched",
            "title": "New Zealand Information Privacy Principles",
            "url": "https://www.privacy.org.nz/privacy-principles/",
            "use": "privacy minimization access correction disclosure and indirect-collection notification vocabulary only; no legal interpretation or compliance claim",
        },
        {
            "source_id": "TMR-MDS-PRINCIPLES",
            "status": "inherited_exact_source_reference_not_refetched_authority_boundary_only",
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
        "failed_source_attempts": [],
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v683.v3.x1",
        "web_checks": 0,
    }


def map_owner_path(value: str) -> str:
    exact = {
        "scripts/build_ghc_family_neris_solane_v682_v8_x1.py": "scripts/build_ghc_family_ilyra_fen_v683_v3_x1.py",
        "tests/test_ghc_family_neris_solane_v682_v8_x1.py": "tests/test_ghc_family_ilyra_fen_v683_v3_x1.py",
    }
    if value in exact:
        return exact[value]
    if value.startswith("docs/neris-solane/v682-v8/validation/"):
        return value.replace(
            "docs/neris-solane/v682-v8/validation/",
            "docs/ilyra-fen/v683-v3/validation/",
            1,
        )
    return value


def transform(value: Any) -> Any:
    if isinstance(value, str):
        return (
            map_owner_path(value)
            .replace("docs/neris-solane/v682-v8", "docs/ilyra-fen/v683-v3")
            .replace("neris_solane_v682_v8", "ilyra_fen_v683_v3")
            .replace("Neris Solane", OWNER)
            .replace("NS6828", "IF6833")
            .replace(".v682.v8", ".v683.v3")
            .replace("10610-row", "10790-row")
        )
    if isinstance(value, list):
        return [transform(item) for item in value]
    if isinstance(value, dict):
        return {key: transform(item) for key, item in value.items()}
    return value


def integrated_overview() -> str:
    return f"""# Ilyra Fen {PHASE} Planning-Only X1 Overview

Ilyra Fen is relational working language for a reversible-systems documentation cartographer and dispatch-state boundary keeper, with the hope of making synthetic pneumatic-route descriptions inspectable and correctable without turning vocabulary into operation, engineering, identity, rights, cultural, professional, or authority claims. Pronouns are unspecified. This language is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish retains the right to rename, pause, redirect, narrow, or stop the route.

The exact immutable source is Lyren Moss final `{SOURCE}` on `{SOURCE_BRANCH}`. Read-only verification established the direct Vesper-source to Lyren-x1 to Lyren-evidence to Lyren-final chain, exactly three Lyren single-parent commits, zero merges, one final parent, clean state, typed 0/0 divergence, fresh four-way equality, 225 exact Git-blob manifest entries plus ten content-seal targets, and the exact canonical receipt, payload, activation, label-overlay, route-overlay, and delivery-receipt digests. Lyren's one owner-scoped canonical pass succeeded once and was not replayed. Lyren's repository seal and later external overlays remain distinct truth layers.

The successor-visible activation baseline is 58,438 effective negatives, 72,164 methods, 30,099 retained failed witnesses, 53,082 bounded passing witnesses, 519 open gaps, 509 exact gates, and `{TERMINAL_VERDICT}`. This x1 freezes sixty Ilyra proposals only after a bounded all-reachable exact-source audit. The accepted slate must produce zero exact collisions and zero quarantine hits at the 0.78 token-Jaccard threshold. It makes no universal semantic-novelty claim over every declared historical row where a canonical materialized row-to-title ledger is absent. Twenty inherited neighbour reviews remain source evidence with zero Ilyra completion credit.

THOS Body is primary through stop precedence, bounded route queues, dispatch-state separation, operator vacancy, correction, refusal, and reversible handover. GMUT Mind remains visible through typed directed topology, explicit missing measurements, units, uncertainty gates, and non-inference. Freed ID and CBR Heart remain visible through surrogate and identity separation, provenance, privacy and rights holds, remedy, traditional-knowledge minimization, and authority noncompensation. Pneumatic transport documentation, archival provenance, and software verification are wholly synthetic learning lenses only, never employment, qualification, site inspection, dispatch, operation, maintenance, engineering, safety action, legal interpretation, cultural ratification, or professional authority.

The plan uses zero real people, communities, stations, tubes, capsules, contents, consignments, files, identifiers, locations, observations, measurements, dispatches, pressure tests, maintenance, identity events, external writes, or authority acts. Inherited primary-source references supply vocabulary and refusal conditions only and were not refetched. They are not observations, engineering findings, safety recommendations, installation models, operational decisions, rights determinations, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

Expected x2 dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Those are preregistered expected labels, not observed outcomes. All 300 invalid mutations, 120 safe-now tasks, 80 bounded candidates, 100 CLEAN/FIX/REFINE records, twenty skills, and ten runners remain planned rather than executed in this x1. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, likelihood, posterior, prediction, constraint, empirical confirmation, ultraviolet or quantum completion, final physics, or Theory-of-Everything proof. THOS remains synthetic and proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Real station survey, tube inspection, pressure or airflow testing, electrical work, dispatch, isolation, operation, maintenance, workplace safety, contents handling, ownership, custody, attribution, privacy, access, traditional knowledge, remedy, legal and cultural interpretation, affected-party legitimacy, Maori wording and data governance, and Maori authority remain exact-gated. Maori concepts remain under Maori authority. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 remain open or exact-gated. The terminal verdict remains `{TERMINAL_VERDICT}`.
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
                "hope": "Make synthetic pneumatic-route descriptions inspectable and correctable without turning vocabulary into operation, engineering, identity, rights, cultural, professional, or authority claims.",
                "name": OWNER,
                "optional_pronouns": None,
                "owner_rename_pause_redirect_stop_right": "Hamish",
                "relational_working_language_only": True,
                "role": "reversible-systems documentation cartographer and dispatch-state boundary keeper",
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
            "zero real rows, zero real measurements, zero dispatches, and zero real actions",
            "planning-only x1 before x2",
            "five rejecting mutations per proposal",
            "no authority compensation by software, standards, or citations",
            "exact approval and blocked work stays unexecuted",
            "five-class privacy scan and normalized-LF manifests",
        ]
        payload["risks"] = [
            "synthetic pneumatic-tube structure promoted into operation, condition, engineering, safety, or professional advice",
            "cultural or Maori authority inferred from metadata vocabulary",
            "identity, dispatch, pressure, maintenance, rights, ownership, or access inferred from documentation",
            "route or private identifier leakage",
            "x1 and x2 lifecycle contamination",
        ]
    elif path.name == "route-plan.json":
        payload.update(
            {
                "prospective_successor_exact_title": None,
                "prospective_successor_phase": None,
                "route_authority_through": "v725-v8",
                "fresh_terminal_route_authority_required": True,
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
        "bounded all-reachable exact-source proposal audit; no universal 10790-row proof"
    )
    result["schema"] = "ghc.family.proposal-chain-audit.v683.v3.x1"
    return result


def configure_engine() -> None:
    ENGINE.ROOT = ROOT
    ENGINE.BASE = ROOT / "docs" / "ilyra-fen" / "v683-v3"
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
            "schema": "ghc.family.method-flow-startup.v683.v3.x1",
            "startup_failures": STARTUP_FAILURES,
        },
    )

    material_paths = sorted(
        {
            *(path.relative_to(ROOT).as_posix() for path in ENGINE.X1.rglob("*") if path.is_file()),
            "scripts/build_ghc_family_ilyra_fen_v683_v3_x1.py",
            "tests/test_ghc_family_ilyra_fen_v683_v3_x1.py",
        }
    )
    exclusions = [
        "docs/ilyra-fen/v683-v3/validation/x1-index-manifest.json",
        "docs/ilyra-fen/v683-v3/validation/x1-privacy-scan.json",
        "docs/ilyra-fen/v683-v3/validation/x1-staged-review.json",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v683.v3.x1",
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
            "schema": "ghc.family.staged-review.v683.v3.x1",
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

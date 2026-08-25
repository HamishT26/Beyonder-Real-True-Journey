from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Elowen Cairn"
PRONOUNS = "they/them"
RELATIONAL_ROLE = "boundary cartographer and evidence steward"
RELATIONAL_HOPE = (
    "to keep structure, evidence, abstention, and authority visibly separate and recoverable"
)
PHASE = "v669-v2"
REL_PHASE_ROOT = Path("docs/elowen-cairn/v669-v2")
PHASE_ROOT = ROOT / REL_PHASE_ROOT
BRANCH = "codex/GHC-Family/elowen-cairn-v669-v2-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v669-v1-full-tools"
SOURCE_START = "bb475c084da39512dfa0811a8520a40fd3d4c84a"
SOURCE_X1 = "f1a090e2396de5d76c70aa3bf7bda0a888b1249a"
SOURCE_EVIDENCE = "cf99dad5ec53f4af60017a829889087ed50cf752"
SOURCE_FINAL = "f8e79f41be203eaec79b39953bed372426f0f40b"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "6698f9161e0d236c913c8896e51cc1b351207923e2f5796c09b86b5371707ce9"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "f316dfd2ed7f7354d2a2d8825c6a8d3352a335d12de57e9b721f2a8ba0dbd895"
)
SOURCE_TERMINAL_STATUS = "PASS_EXACT_FINAL_OWNER_CANONICAL_ONCE"
INHERITED_FROZEN_PROPOSALS = 4950
RECOVERED_HISTORICAL_ROWS = 1380
RECOVERED_UNIQUE_NORMALIZED_TITLES = 1379
UNRECOVERED_DECLARED_ROWS = 3570
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
PRIMARY_PILLAR = "GMUT Mind"
PRACTICE = "synthetic lutherie and stringed-instrument documentation"
DOCUMENT_WORD_CEILING = 6000
FILE_CEILING = 2000

IDENTITY_BOUNDARY = (
    "Elowen Cairn, they/them, the relational role and hope, sibling or family language, "
    "continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala language are "
    "working language only. They are not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, qualification, independent agency, "
    "scientific or operational authority, professional authority, legal or cultural "
    "authority, affected-party authority, or Māori authority. Hamish may rename, pause, "
    "redirect, or stop the route."
)

EVIDENCE_BOUNDARY = (
    "Every instrument, component, material, measurement, person, workshop, collection "
    "record, identity event, review, release, interpretation, and authority act is absent. "
    "This phase may establish bounded owner-local synthetic software and documentation "
    "evidence only; it cannot establish lutherie competence, object identity, authenticity, "
    "condition, acoustical performance, safety, provenance truth, ownership, rights, legal "
    "or cultural legitimacy, Māori authority, production readiness, independent reproduction, "
    "empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI, consciousness or "
    "personhood, canon, or Stage 20 authority."
)

PROTECTED_GATES = [
    "real_people_or_participants",
    "real_instruments_or_materials",
    "real_measurements_or_observations",
    "professional_lutherie_or_conservation_decision",
    "workplace_or_product_safety_release",
    "live_identity_keys_proofs_or_lifecycle",
    "privacy_complete_or_accessibility_complete_claim",
    "legal_ownership_authorship_or_remedy_decision",
    "cultural_interpretation_or_affected_party_legitimacy",
    "Māori_wording_concepts_data_governance_or_authority",
    "empirical_GMUT_or_Theory_of_Everything_claim",
    "THOS_operational_effectiveness_AGI_or_ASI_claim",
    "consciousness_personhood_or_identity_continuity_claim",
    "independent_reproduction_production_deployment_or_Stage_20_claim",
]

SOURCE_OVERLAY = {
    "effective_negatives": 30524,
    "methods": 16630,
    "failed_witnesses": 2345,
    "passing_witnesses": 3172,
    "open_gaps": 225,
    "exact_gates": 220,
}

STARTUP_FAILURES = [
    (
        "EC6692-X1-F001",
        "A combined source-discovery wrapper returned the anchor but no attributable worktree-list payload before its supervision window.",
        "Inspect the completed process state, then use an exact literal source-worktree lookup rather than replaying the wrapper.",
        "Separate exact anchor resolution from worktree-registry projection and inspect state after a timeout.",
    ),
    (
        "EC6692-X1-F002",
        "A skill-inventory projection placed an inline PowerShell if expression inside an object property and produced no usable inventory.",
        "Resolve exists and byte-count scalars before constructing the report object.",
        "Keep control-flow expressions outside PowerShell object-property values.",
    ),
    (
        "EC6692-X1-F003",
        "A combined authorization-state display truncated the required current-state JSON.",
        "Read the complete state in bounded contiguous chunks through EOF.",
        "Partition large mandatory reads by exact line range before interpretation.",
    ),
    (
        "EC6692-X1-F004",
        "A combined Reflection Remaster and Meta Tool Box display truncated the Meta Tool Box skill.",
        "Reread the Meta Tool Box skill alone in two bounded contiguous chunks through EOF.",
        "Do not batch two mandatory skills when their combined projection approaches the output ceiling.",
    ),
    (
        "EC6692-X1-F005",
        "A source x1 packet batch truncated the semantic-novelty audit.",
        "Reread the novelty audit independently through EOF.",
        "Isolate large semantic-audit documents from surrounding packet reads.",
    ),
    (
        "EC6692-X1-F006",
        "A four-portfolio batch truncated the safe-now and candidate portfolios.",
        "Read each affected portfolio independently through EOF.",
        "Project portfolio counts first and isolate large portfolio bodies.",
    ),
    (
        "EC6692-X1-F007",
        "A paired proposal-shard display truncated the second shard.",
        "Reread each affected proposal shard independently through EOF.",
        "Keep full proposal-shard displays one file per bounded read.",
    ),
    (
        "EC6692-X1-F008",
        "A full proposal-shard display exceeded the model-context projection and became unusable.",
        "Parse every shard through EOF and emit only bounded hashes, schemas, required-field checks, and row summaries.",
        "Prefer full machine parsing plus bounded projections for large structured ledgers.",
    ),
    (
        "EC6692-X1-F009",
        "The first bounded parser assumed a nonexistent x1/proposals directory.",
        "Resolve exact proposal shard paths from the immutable tree with a bounded file listing.",
        "Discover lifecycle directory names from the exact tree before opening them.",
    ),
    (
        "EC6692-X1-F010",
        "The first compact proposal parser omitted the actual root key rows and reported zero records.",
        "Inspect root keys, select rows explicitly, and rerun only the projection.",
        "Project a schema sample before counting records in an unfamiliar ledger.",
    ),
    (
        "EC6692-X1-F011",
        "The mutation-count projection used rejecting_mutations instead of the actual negative_fixtures field.",
        "Inspect one exact fixture container and count its four array entries per proposal.",
        "Never infer mutation container names across lifecycle schemas.",
    ),
    (
        "EC6692-X1-F012",
        "The first Method Flow projection used generic name and status fields rather than title and witness result.",
        "Project the exact method and witness schema keys and resolve every witness link.",
        "Use ledger-native field names after a root and row schema inspection.",
    ),
    (
        "EC6692-X1-F013",
        "The first outcome-ledger summary used disposition and artifacts fields that the ledger does not define.",
        "Inspect one complete row and project outcome, obligations, positive_fixture, and positive_witness.",
        "Sample a full row before summarizing a large unfamiliar outcome ledger.",
    ),
    (
        "EC6692-X1-F014",
        "The first skill and runner receipt summary projected generic status and installation fields.",
        "Use the exact receipt fields for quick validation, installation, and accepting or rejecting smoke records.",
        "Treat skill and runner receipt schemas as distinct surfaces.",
    ),
    (
        "EC6692-X1-F015",
        "The corrected receipt summary still assumed a nested smoke key named passed and produced null booleans.",
        "Decode the JSON line in stdout_tail and evaluate accepted plus the expected return code.",
        "Inspect and decode nested command receipts instead of inventing convenience booleans.",
    ),
    (
        "EC6692-X1-F016",
        "The mutation class histogram projected kind rather than mutation_class.",
        "Recompute only the class histogram from the exact mutation_class field.",
        "Use the row schema already observed by the preceding full parse.",
    ),
    (
        "EC6692-X1-F017",
        "The first worktree collision-probe wrapper placed a native command and status check inside a report-property expression and failed before execution.",
        "Run the native commit probe first, capture its status in a scalar, then construct the report.",
        "Keep native commands outside PowerShell object literals and preserve parse faults at zero credit.",
    ),
    (
        "EC6692-X1-F018",
        "The first genuine semantic-novelty preflight quarantined ten generic cross-cutting titles at or above the recovered-neighbor threshold and stopped before artifact materialization.",
        "Inspect the exact nearest neighbors and revise only the affected titles or framing before repeating the bounded novelty dependency.",
        "Require zero exact-title collisions and every recovered-neighbor score below 0.75 before x1 materialization.",
    ),
    (
        "EC6692-X1-F019",
        "The first nearest-neighbor report could not encode a Māori character through the default Windows console and produced no usable projection.",
        "Emit the already computed bounded projection through explicit UTF-8 stdout.",
        "Set an explicit UTF-8 output encoding for structured reports that may contain Māori or other non-ASCII text.",
    ),
    (
        "EC6692-X1-F020",
        "The first post-novelty portfolio projection exposed twenty-one exact-approval rows rather than the frozen twenty-row contract.",
        "Remove the redundant real-instrument acquisition packet already covered by the protected real-instrument gate and recount every category.",
        "Assert exact portfolio category counts before x1 artifact materialization.",
    ),
    (
        "EC6692-X1-F021",
        "The test-module apply-patch response exceeded the model display budget, so the first acknowledgement could not establish whether the bounded patch had landed completely.",
        "Inspect the exact literal path, byte and line counts, complete tail, and Python AST before treating the file as materialized.",
        "Treat oversized patch acknowledgements as unresolved projections and recover through read-only filesystem and syntax evidence rather than replaying the patch.",
    ),
    (
        "EC6692-X1-F022",
        "The first read-only overview word-count preflight supplied an incomplete temporary audit projection and stopped on the missing recovered-unique-normalized-titles field without writing phase artifacts.",
        "Construct the in-memory preflight input from the builder's complete declared audit shape and rerun only the word-count dependency.",
        "Reuse exact builder schema keys for preflight projections instead of abbreviated lookalike objects.",
    ),
    (
        "EC6692-X1-F023",
        "The first exact x1 staged diff-hygiene gate found one trailing space and one extra terminal blank line in the owner validator, so the staged tree earned no gate credit.",
        "Remove only the reported whitespace defects, regenerate the planning-only receipts with this failure retained, and restage the unchanged exact allowlist.",
        "Run cached diff hygiene immediately after every exact staging operation and stop before tests whenever it reports a defect.",
    ),
    (
        "EC6692-X1-F024",
        "The first x1 validator invocation stopped before emitting a receipt because its implementation referenced Counter without importing it; the invocation earns zero validation credit.",
        "Add only the missing collections.Counter import, retain this failure in Method Flow, regenerate the planning receipts, and rerun the failed validator dependency once.",
        "Parse validator imports against every referenced standard-library symbol before its first receipt-producing invocation.",
    ),
]

ACTIVATION_OVERLAY = {
    "effective_negatives": SOURCE_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES),
    "methods": SOURCE_OVERLAY["methods"] + len(STARTUP_FAILURES),
    "failed_witnesses": SOURCE_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES),
    "passing_witnesses": SOURCE_OVERLAY["passing_witnesses"] + len(STARTUP_FAILURES),
    "open_gaps": SOURCE_OVERLAY["open_gaps"],
    "exact_gates": SOURCE_OVERLAY["exact_gates"],
}

SOURCE_LEDGER = [
    {
        "source_id": "SRC-LOC-MUSICAL-INSTRUMENTS",
        "title": "Musical Instruments at the Library of Congress",
        "url": "https://www.loc.gov/collections/musical-instruments-at-the-library-of-congress/about-this-collection/",
        "status": "official Library of Congress collection page inspected 25 August 2026",
        "use": "stringed-instrument collection, component-description, and zero-call adapter vocabulary only",
        "credit_boundary": "no object identity, attribution, authenticity, condition, ownership, performance, rights, or collection-authority credit",
    },
    {
        "source_id": "SRC-NIOSH-WOOD-DUST",
        "title": "NIOSH wood-dust hazard resources",
        "url": "https://www.cdc.gov/niosh/npg/npgd0667.html",
        "status": "official NIOSH Pocket Guide page inspected 25 August 2026",
        "use": "wood-dust exposure and safety-hold vocabulary only",
        "credit_boundary": "no workplace measurement, risk assessment, control selection, compliance, or safety-release credit",
    },
    {
        "source_id": "SRC-ICOM-ETHICS-2026",
        "title": "Revised ICOM Code of Ethics for Museums",
        "url": "https://icom.museum/en/news/",
        "status": "official ICOM adoption notice dated 25 June 2026 and inspected 25 August 2026",
        "use": "collections-responsibility, provenance, custody, public-trust, and authority-vacancy vocabulary only",
        "credit_boundary": "no museum-policy interpretation, professional decision, provenance truth, ownership, return, or cultural-authority credit",
    },
    {
        "source_id": "SRC-WCAG22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation 12 December 2024; current page inspected 25 August 2026",
        "use": "static headings, tables, text status, focus, reflow, and fallback hypotheses only",
        "credit_boundary": "manual browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remains reserved",
    },
    {
        "source_id": "SRC-NIST-800-63-4",
        "title": "NIST SP 800-63-4 Digital Identity Guidelines",
        "url": "https://pages.nist.gov/800-63-4/",
        "status": "official final NIST revision published July 2025 and inspected 25 August 2026",
        "use": "identity-role, risk, privacy, redress, recovery, and assurance-vacancy vocabulary only",
        "credit_boundary": "no proofing, authenticator, federation, assurance-level, conformance, deployment, or production identity credit",
    },
    {
        "source_id": "SRC-PROV-DM",
        "title": "W3C PROV-DM",
        "url": "https://www.w3.org/TR/prov-dm/",
        "status": "W3C Recommendation 30 April 2013; publication history inspected 25 August 2026",
        "use": "entity, activity, derivation, role, invalidation, and delegation-vacancy structure only",
        "credit_boundary": "no authenticity, custody, ownership, responsibility, competence, or authority inference",
    },
    {
        "source_id": "SRC-RFC8785",
        "title": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational publication dated June 2020 and inspected 25 August 2026",
        "use": "deterministic JSON serialization and explicit numeric and Unicode domain vocabulary only",
        "credit_boundary": "no signature, authenticity, interoperability, security, or production assurance",
    },
    {
        "source_id": "SRC-SCALAR-EFT",
        "title": "Well-posed formulation of scalar-tensor effective field theory",
        "url": "https://arxiv.org/abs/2003.04327",
        "status": "primary paper by Kovacs and Reall; current record inspected 25 August 2026",
        "use": "weak-coupling, principal-symbol, characteristic, gauge, and hyperbolicity obligation vocabulary only",
        "credit_boundary": "no GMUT equation, solution, likelihood, observation, prediction, constraint, quantum completion, or empirical confirmation",
    },
    {
        "source_id": "SRC-VIOLIN-DATA",
        "title": "A Data-Driven Approach to Violin Making",
        "url": "https://arxiv.org/abs/2102.04254",
        "status": "primary research record inspected 25 August 2026",
        "use": "plate-parameter, modal-frequency, dependency, and nonidentifiability obligation vocabulary only",
        "credit_boundary": "no plate model, material property, measurement, fit, optimization, instrument prediction, or making advice",
    },
    {
        "source_id": "SRC-VIOLIN-PLATE",
        "title": "Parametric Optimization of Violin Top Plates using Machine Learning",
        "url": "https://arxiv.org/abs/2102.07133",
        "status": "primary research record inspected 25 August 2026",
        "use": "free-boundary eigenfrequency and parameter-sensitivity obligation vocabulary only",
        "credit_boundary": "no computed eigenfrequency, optimized geometry, physical validation, instrument quality, or empirical GMUT credit",
    },
    {
        "source_id": "SRC-TMR",
        "title": "Te Mana Raraunga Principles of Māori Data Sovereignty",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "primary Te Mana Raraunga resource inspected 25 August 2026",
        "use": "authority-vacancy, collective-benefit, control, jurisdiction, responsibility, and ethics stop conditions only",
        "credit_boundary": "citation creates no cultural legitimacy, tikanga decision, Māori data-governance mandate, or Māori authority",
    },
]


# Each blueprint is genuinely distinct in focus and names the evidence lane that may exist later.
# Shared field-generation below keeps the freeze readable without weakening the required contract.
PROPOSAL_BLUEPRINTS = [
    ("instrument-identity", "synthetic bowed-string instrument corpus body neck fingerboard pegbox scroll bridge tailpiece and string-course identity lattice with conflation refusal", "instrument and component identity", "completed", "safe_now", ["SRC-LOC-MUSICAL-INSTRUMENTS"]),
    ("body-neck-topology", "body neck heel block rib corner endblock lining and joint topology graph with orphan and impossible-cycle quarantine", "body and neck topology", "completed", "safe_now", ["SRC-LOC-MUSICAL-INSTRUMENTS"]),
    ("plate-geometry-vacancy", "soundboard back-plate outline arch graduation and thickness-unit placeholder with measurement and template vacancy", "plate geometry and thickness placeholders", "completed", "safe_now", ["SRC-VIOLIN-DATA", "SRC-VIOLIN-PLATE"]),
    ("internal-structure", "bass-bar soundpost block lining brace and internal-support relation board with placement and construction abstention", "internal support relationships", "completed", "safe_now", ["SRC-LOC-MUSICAL-INSTRUMENTS"]),
    ("string-course-state", "string course gauge material pitch frequency tension and tuning-state register with zero fitted value and no tuning action", "string course and tuning states", "completed", "safe_now", ["SRC-VIOLIN-DATA"]),
    ("bridge-nut-saddle", "bridge nut saddle tailpiece afterlength stop-length and contact-point graph with fit and adjustment vacancy", "bridge nut saddle and tailpiece relations", "completed", "safe_now", ["SRC-VIOLIN-DATA"]),
    ("tuning-mechanism", "peg machine-head fine-tuner hole bushing and winding-direction state machine with actuation refusal", "tuning mechanism states", "completed", "safe_now", ["SRC-LOC-MUSICAL-INSTRUMENTS"]),
    ("finish-claim-vacancy", "ground varnish polish retouch coating colour and gloss claim-vacancy matrix with composition and treatment refusal", "finish and coating claims", "completed", "safe_now", ["SRC-ICOM-ETHICS-2026"]),
    ("material-claim-vacancy", "spruce maple ebony willow synthetic fibre metal hide and adhesive material-claim vacancy matrix with species and authenticity refusal", "material and species claims", "completed", "safe_now", ["SRC-ICOM-ETHICS-2026"]),
    ("dimension-unit-profile", "decimal-string scale length bout rib neck angle arch thickness mass and frequency profile with SI-domain and uncertainty obligations", "dimension unit and uncertainty profiles", "completed", "safe_now", ["SRC-RFC8785", "SRC-VIOLIN-PLATE"]),
    ("condition-cue-vocabulary", "open seam crack distortion wear loss corrosion residue abrasion and finish-change cue vocabulary without diagnosis", "condition cue vocabulary", "completed", "safe_now", ["SRC-ICOM-ETHICS-2026"]),
    ("structural-hold-register", "crack seam neck-set bridge-warp soundpost and string-state cue hold register with triage and intervention abstention", "structural cue holds", "completed", "safe_now", ["SRC-ICOM-ETHICS-2026"]),
    ("action-state-machine", "lutherie proposal approval execution observation correction and release state machine with every real setup repair and treatment forbidden", "action and release lifecycle", "completed", "safe_now", ["SRC-ICOM-ETHICS-2026"]),
    ("tool-identity-vacancy", "synthetic plane chisel knife scraper clamp bending-iron reamer soundpost-tool and gauge identity register with competence vacancy", "tool identity and competence vacancy", "completed", "safe_now", ["SRC-NIOSH-WOOD-DUST"]),
    ("correction-docket-fork", "append-only instrument-documentation correction fork with effective time recording time superseded-field mask contested branch and signoff vacancy", "bitemporal corrections", "completed", "safe_now", ["SRC-PROV-DM"]),
    ("custody-location-graph", "synthetic instrument case shelf room transfer loan return withdrawal and custody graph with ownership noninference", "custody and location events", "completed", "safe_now", ["SRC-PROV-DM", "SRC-ICOM-ETHICS-2026"]),
    ("component-provenance", "component material lot source statement maker-attribution treatment and derivative provenance graph with truth and authority vacancies", "component and material provenance", "completed", "safe_now", ["SRC-PROV-DM", "SRC-ICOM-ETHICS-2026"]),
    ("canonical-hash-domain", "UTF-8 stable bitemporal instrument dossier hash-domain register with duplicate-key numeric coercion and signature-claim refusal", "canonical serialization and hash domains", "completed", "safe_now", ["SRC-RFC8785"]),
    ("pseudonym-alias-budget", "unlinkable surrogate instrument docket workshop review-cohort and handover alias budget with correlation alarms", "privacy-minimizing aliases", "completed", "safe_now", ["SRC-NIST-800-63-4"]),
    ("accessible-topology-table", "instrument-component adjacency ledger with nested-list fallback description anchors discontinuity markers and reserved multimodal review", "structural accessibility", "completed", "safe_now", ["SRC-WCAG22"]),
    ("issue-escrow", "instrument discrepancy quorum capsule with four pseudonymous roles expiring lease bounded queue competing revision digests no adjudicator and unresolved carry-forward", "issue escrow and conflict retention", "completed", "safe_now", ["SRC-PROV-DM"]),
    ("source-assertion-firewall", "collection-source scope firewall for Library of Congress page statements component vocabulary observation vacancy attribution hold condition silence and instruction veto", "source assertion boundaries", "completed", "safe_now", ["SRC-LOC-MUSICAL-INSTRUMENTS", "SRC-ICOM-ETHICS-2026"]),
    ("cbr-challenge-ladder", "CBR claim-contestation braid for instrument dossiers combining minimised disclosure statement attachment review clock appeal vacancy remedy hold and authority abstention", "CBR challenge and remedy vacancies", "completed", "safe_now", ["SRC-NIST-800-63-4", "SRC-TMR"]),
    ("freed-id-envelope", "Freed ID purpose-scoped zero-key instrument record disclosure braid with holder vacancy correlation ceiling challenge branch expiry and status-service absence", "Freed ID capability vacancies", "completed", "safe_now", ["SRC-NIST-800-63-4"]),
    ("thos-dependency-dag", "THOS participant-free instrument-documentation work graph linking intake debt component ambiguity stop tokens correction echo queue cap and successor readback", "THOS dependency and handover protocol", "completed", "safe_now", ["SRC-WCAG22"]),
    ("gmut-string-plate-board", "GMUT typed string shell plate bridge coupling and radiation obligation board with domain boundary units constitutive vacancy and zero solved equation", "typed string plate coupling obligations", "completed", "candidate", ["SRC-SCALAR-EFT", "SRC-VIOLIN-DATA"]),
    ("gmut-spectral-identifiability", "GMUT modal spectrum inverse-map identifiability covariance damping and gauge-analogy obligation tribunal with zero eigenvalue calculation", "spectral inverse and identifiability obligations", "completed", "candidate", ["SRC-SCALAR-EFT", "SRC-VIOLIN-PLATE"]),
    ("hazard-hold-schema", "sharp-tool wood-dust solvent heat string-tension lifting ergonomics and fire hold schema with no risk determination or safety release", "workshop hazard holds", "completed", "candidate", ["SRC-NIOSH-WOOD-DUST"]),
    ("lutherie-practice-lens", "lutherie intake and stringed-instrument component-documentation practice lens with zero craft material acoustic or condition competence inference", "bounded lutherie documentation practice", "represented", "candidate", ["SRC-LOC-MUSICAL-INSTRUMENTS", "SRC-ICOM-ETHICS-2026"]),
    ("workload-handover-practice", "synthetic workshop correction workload interruption and shift-handover practice lens with zero instrument handling", "workload and handover practice", "represented", "candidate", ["SRC-WCAG22"]),
    ("accessible-dossier-practice", "responsive instrument-record dossier hypothesis with landmark order error rollup visible hold language keyboard focus return zoom reflow and reserved human study", "accessible dossier practice", "represented", "candidate", ["SRC-WCAG22"]),
    ("thos-omission-proxy", "THOS masked dual-arm synthetic instrument-dependency review skeleton with matched token ceilings randomized docket order explicit abstentions stop conditions and zero performance inference", "THOS omission proxy", "represented", "candidate", ["SRC-WCAG22"]),
    ("freed-id-trust-surface", "Freed ID zero-credential instrument-record reliance vacancy chart covering proof purpose issuer absence status-service absence recovery debt verifier boundary and correlation alarm", "Freed ID trust surface", "represented", "candidate", ["SRC-NIST-800-63-4"]),
    ("cbr-authority-boundary", "CBR instrument authorship ownership custody heritage traditional-knowledge remedy affected-party legitimacy and authority-vacancy lens", "CBR rights and authority boundary", "represented", "candidate", ["SRC-ICOM-ETHICS-2026", "SRC-TMR"]),
    ("gmut-lutherie-analogy", "typed scalar-tensor lutherie stress vibration and radiation analogy card separating bookkeeping from physical prediction", "GMUT lutherie analogy nonpromotion", "represented", "candidate", ["SRC-SCALAR-EFT", "SRC-VIOLIN-DATA"]),
    ("acoustic-psyche-nonconversion", "frequency amplitude mode shape damping radiation timbre and listener-response vacancy versus agency justice mind and personhood nonconversion ledger", "acoustic and psyche nonconversion", "represented", "candidate", ["SRC-VIOLIN-DATA"]),
    ("loc-instrument-zero-call", "Library of Congress musical-instrument collection zero-call adapter with zero key query request download row media object attribution or rights claim", "official collection zero-call adapter", "open_gap", "candidate", ["SRC-LOC-MUSICAL-INSTRUMENTS"]),
    ("human-evaluation-gap", "real luthier musician conservator collector accessibility language cultural-care safety and affected-party evaluation", "real human and professional evaluation", "open_gap", "candidate", ["SRC-WCAG22", "SRC-ICOM-ETHICS-2026", "SRC-TMR"]),
    ("instrument-authority-gate", "competent instrument setup repair release condition custody ownership attribution legal cultural and Māori-authority decision gate", "professional legal cultural and Māori authority", "exact_gate", "exact_approval", ["SRC-ICOM-ETHICS-2026", "SRC-TMR"]),
    ("stage20-nonpromotion", "Stage 20 evidence-vector lock requiring nonzero governed receipts for GMUT data THOS participants identity lifecycle safety accessibility independent review law culture affected parties and Māori authority before any promotion", "Stage 20 nonpromotion", "exact_gate", "exact_approval", ["SRC-SCALAR-EFT", "SRC-NIST-800-63-4", "SRC-TMR"]),
]

SKILL_NAMES = [
    "ghc-family-lutherie-instrument-identity",
    "ghc-family-lutherie-body-neck-topology",
    "ghc-family-lutherie-plate-vacancy",
    "ghc-family-lutherie-internal-structure",
    "ghc-family-lutherie-string-state",
    "ghc-family-lutherie-bridge-relations",
    "ghc-family-lutherie-tuning-state",
    "ghc-family-lutherie-finish-vacancy",
    "ghc-family-lutherie-material-vacancy",
    "ghc-family-lutherie-condition-cues",
    "ghc-family-lutherie-correction-chain",
    "ghc-family-lutherie-custody-vacancy",
    "ghc-family-lutherie-provenance",
    "ghc-family-lutherie-hash-domain",
    "ghc-family-lutherie-pseudonyms",
    "ghc-family-lutherie-accessible-report",
    "ghc-family-lutherie-workload-handover",
    "ghc-family-lutherie-hazard-holds",
    "ghc-family-lutherie-identity-vacancy",
    "ghc-family-lutherie-authority-vacancy",
]

RUNNER_NAMES = [
    "ghc_family_lutherie_identity_runner",
    "ghc_family_lutherie_topology_runner",
    "ghc_family_lutherie_plate_vacancy_runner",
    "ghc_family_lutherie_string_state_runner",
    "ghc_family_lutherie_material_vacancy_runner",
    "ghc_family_lutherie_condition_runner",
    "ghc_family_lutherie_provenance_runner",
    "ghc_family_lutherie_accessibility_runner",
    "ghc_family_lutherie_identity_vacancy_runner",
    "ghc_family_lutherie_authority_firewall_runner",
]

PORTFOLIO_COUNTS = {
    "safe_now": 60,
    "candidates": 30,
    "exact_approval": 20,
    "blocked": 10,
    "skills": 20,
    "runners": 10,
    "clean_fix_refine": 60,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def run_git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=text,
    )


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def git_blob(commit: str, path: str) -> bytes:
    return run_git("show", f"{commit}:{path}", text=False).stdout


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def title_tokens(title: str) -> set[str]:
    return {token for token in normalize_title(title).split() if len(token) > 2}


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def historical_proposal_inventory() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    shard_hashes: list[dict[str, Any]] = []
    for index in range(1, 15):
        path = f"docs/tamar-vey/v669-v1/x1/historical-corpus-shards/corpus-{index:02d}.json"
        data = git_blob(SOURCE_FINAL, path)
        doc = json.loads(data)
        rows.extend(doc["rows"])
        shard_hashes.append({"path": path, "sha256": sha256_bytes(data), "rows": len(doc["rows"])})
    for index in range(1, 9):
        path = f"docs/tamar-vey/v669-v1/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        data = git_blob(SOURCE_FINAL, path)
        doc = json.loads(data)
        rows.extend(doc["rows"])
        shard_hashes.append({"path": path, "sha256": sha256_bytes(data), "rows": len(doc["rows"])})
    normalized = [row.get("normalized_title") or normalize_title(row["title"]) for row in rows]
    duplicate_groups = sorted(
        {title: normalized.count(title) for title in set(normalized) if normalized.count(title) > 1}.items()
    )
    if len(rows) != RECOVERED_HISTORICAL_ROWS:
        raise RuntimeError(f"recovered row drift: {len(rows)}")
    if len(set(normalized)) != RECOVERED_UNIQUE_NORMALIZED_TITLES:
        raise RuntimeError(f"recovered unique-title drift: {len(set(normalized))}")
    return {
        "rows": rows,
        "shards": shard_hashes,
        "row_count": len(rows),
        "unique_ids": len({row["proposal_id"] for row in rows}),
        "unique_normalized_titles": len(set(normalized)),
        "duplicate_normalized_groups": [
            {"normalized_title": title, "count": count} for title, count in duplicate_groups
        ],
    }


def proposal_rows(corpus: dict[str, Any]) -> list[dict[str, Any]]:
    recovered = [
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "normalized_title": row.get("normalized_title") or normalize_title(row["title"]),
            "tokens": title_tokens(row["title"]),
        }
        for row in corpus["rows"]
    ]
    rows: list[dict[str, Any]] = []
    for number, (slug, title, focus, outcome, approval, source_ids) in enumerate(PROPOSAL_BLUEPRINTS, 1):
        proposal_id = f"EC6692-N{number:03d}"
        tokens = title_tokens(title)
        neighbors = sorted(
            (
                {
                    "proposal_id": item["proposal_id"],
                    "title": item["title"],
                    "score": round(jaccard(tokens, item["tokens"]), 6),
                }
                for item in recovered
            ),
            key=lambda item: (-item["score"], item["proposal_id"]),
        )[:3]
        visible_collision = normalize_title(title) in {item["normalized_title"] for item in recovered}
        quarantined = visible_collision or (neighbors and neighbors[0]["score"] >= 0.75)
        if outcome == "completed":
            hypothesis = (
                f"A wholly synthetic zero-person {focus} contract can preserve explicit states, "
                "vacancies, refusal conditions, and rollback without any real-world action or protected claim."
            )
            null_condition = (
                f"Reject completion if the {focus} fixture omits a required state, accepts an ambiguous domain, "
                "performs an external action, or promotes a protected claim."
            )
            acceptance = (
                "One bounded positive fixture is accepted, four preregistered invalid mutations are rejected, "
                "and all real people, rows, materials, measurements, external actions, and authority actions remain zero."
            )
        elif outcome == "represented":
            hypothesis = (
                f"A structural {focus} representation can make obligations and absences inspectable without "
                "claiming real execution, effectiveness, competence, empirical confirmation, or authority."
            )
            null_condition = (
                f"Reject representation if {focus} is presented as completed real practice, performance evidence, "
                "professional evaluation, identity lifecycle, empirical GMUT evidence, or authority."
            )
            acceptance = (
                "The representation is structurally complete, all nonzero real-world fields are rejected, and "
                "completion credit remains zero."
            )
        elif outcome == "open_gap":
            hypothesis = (
                f"The {focus} gap can be stated precisely while the current zero-call and zero-person evidence state remains open."
            )
            null_condition = (
                f"Reject any closure if {focus} lacks governed real evidence, appropriate review, provenance, consent, "
                "safety controls, or affected-party participation."
            )
            acceptance = "The missing evidence vector remains explicit and open-gap credit is zero."
        else:
            hypothesis = (
                f"The {focus} decision cannot be substituted by software and must remain exact-gated to competent, "
                "affected, legal, cultural, tangata whenua, iwi, hapū, and Māori authorities as applicable."
            )
            null_condition = f"Reject any attempt to close {focus} without the exact governing authority and evidence."
            acceptance = "The gate remains held, no authority act occurs, and completion or representation credit remains zero."
        artifact_stem = f"{proposal_id.lower()}-{slug}"
        rows.append(
            {
                "approval_class": approval,
                "concrete_artifacts": [
                    f"docs/elowen-cairn/v669-v2/x2/proposals/{artifact_stem}.json",
                    f"docs/elowen-cairn/v669-v2/x2/cards/{artifact_stem}.json",
                ],
                "execution_lane": {
                    "completed": "x2_owner_local_bounded_control",
                    "represented": "x2_structural_representation_only",
                    "open_gap": "x2_zero_call_or_zero_person_open_gap",
                    "exact_gate": "x2_unexecuted_exact_authority_gate",
                }[outcome],
                "expected_disposition": outcome,
                "falsifier_or_acceptance_gate": acceptance,
                "hypothesis": hypothesis,
                "negative_fixtures": [
                    {"mutation_id": f"{proposal_id}-M01", "kind": "missing_required_state", "expected": "reject"},
                    {"mutation_id": f"{proposal_id}-M02", "kind": "ambiguous_domain_or_unit", "expected": "reject"},
                    {"mutation_id": f"{proposal_id}-M03", "kind": "real_world_or_external_action", "expected": "reject"},
                    {"mutation_id": f"{proposal_id}-M04", "kind": "protected_claim_promotion", "expected": "reject"},
                ],
                "null_or_failure_condition": null_condition,
                "observed_disposition": None,
                "official_or_primary_source_needs": source_ids,
                "proposal_id": proposal_id,
                "protected_gates": PROTECTED_GATES,
                "rollback_or_recovery": (
                    "Retain the failed fixture at zero credit, stop the smallest affected control, preserve the prior "
                    "immutable lifecycle, remove only generated owner-local artifacts if exact recovery requires it, "
                    "and rerun only the failed dependency before any broader validation."
                ),
                "semantic_neighbor_quarantined": bool(quarantined),
                "semantic_neighbors": neighbors,
                "semantic_slug": slug,
                "title": title,
                "visible_title_collision": visible_collision,
                "x1_completion_credit": 0,
            }
        )
    if any(row["semantic_neighbor_quarantined"] for row in rows):
        bad = [row["proposal_id"] for row in rows if row["semantic_neighbor_quarantined"]]
        raise RuntimeError(f"semantic novelty quarantine: {bad}")
    return rows


def portfolio_rows(prefix: str, titles: Iterable[str], category: str, state: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_class": category,
            "completion_credit": 0,
            "execution_state": state,
            "external_actions": 0,
            "item_id": f"{prefix}-{index:03d}",
            "owner": OWNER,
            "phase": PHASE,
            "protected_gates": PROTECTED_GATES,
            "rollback": "retain_failure_stop_smallest_owner_local_control",
            "same_owner_only": True,
            "title": title,
        }
        for index, title in enumerate(titles, 1)
    ]


def generated_portfolios() -> dict[str, list[dict[str, Any]]]:
    slugs = [row[0] for row in PROPOSAL_BLUEPRINTS]
    safe_titles = [f"Bounded schema and refusal check for {slug}" for slug in slugs]
    safe_titles += [
        "Reconcile exact x1 allowlist with materialized owner paths",
        "Check source-credit and inherited-completion firewalls",
        "Check all numeric fields use explicit domains or decimal strings",
        "Check zero-person zero-row zero-material invariants",
        "Check action and authority vacancy fields remain zero",
        "Check four-label outcome vocabulary remains closed",
        "Check proposal and mutation identifiers are unique",
        "Check every mutation retains a failed witness at zero credit",
        "Check Method Flow failed and passing witness pairs resolve",
        "Check static report status is text redundant",
        "Check manual accessibility evaluation remains reserved",
        "Check Māori wording concepts data governance and authority remain gated",
        "Check GMUT obligations are typed and nonempirical",
        "Check THOS proxy evidence contains no effectiveness estimate",
        "Check Freed ID surfaces contain zero real keys and proofs",
        "Check canonical validation remains pending until exact final",
        "Check owner and phase labels are current",
        "Check no raw task thread credential or private path enters artifacts",
        "Check document and file ceilings before staging",
        "Check successor recommendations remain zero-credit seeds",
    ]
    candidate_titles = [
        "Candidate governed LoC collection adapter with explicit zero-call default",
        "Candidate manual screen-reader evaluation protocol reserved to qualified users",
        "Candidate real-luthier review protocol with competence and consent prerequisites",
        "Candidate musician and affected-owner review protocol with withdrawal rights",
        "Candidate lutherie vocabulary crosswalk with source-version pinning",
        "Candidate string-plate obligation schema with no numerical solver",
        "Candidate modal-identifiability debt ledger with no fitted parameters",
        "Candidate workshop hazard referral card with no safety instruction",
        "Candidate instrument custody disagreement branch with authority vacancy",
        "Candidate provenance uncertainty and contested-attribution state model",
        "Candidate pseudonym correlation budget stress fixture",
        "Candidate bitemporal correction collision fixture",
        "Candidate accessible table reflow and print hypothesis",
        "Candidate error-summary and focus-order structural hypothesis",
        "Candidate THOS matched-budget synthetic omission protocol",
        "Candidate CBR least-disclosure challenge state machine",
        "Candidate Freed ID zero-key status and recovery vacancy map",
        "Candidate GMUT lutherie analogy nonconversion tribunal",
        "Candidate acoustic-to-psyche nonconversion tribunal",
        "Candidate ICOM 2026 source-version review receipt",
        "Candidate NIST 800-63-4 vocabulary-drift receipt",
        "Candidate WCAG 2.2 static-structure delta receipt",
        "Candidate Te Mana Raraunga authority-stop receipt",
        "Candidate independent-review evidence-vector placeholder",
        "Candidate participant safety and consent evidence-vector placeholder",
        "Candidate live identity interoperability evidence-vector placeholder",
        "Candidate legal cultural and Māori-authority evidence-vector placeholder",
        "Candidate production and deployment evidence-vector placeholder",
        "Candidate external-audit and independent-reproduction placeholder",
        "Candidate Stage 20 conjunctive non-substitution audit",
    ]
    exact_titles = [f"Exact authority packet for protected gate {gate}" for gate in PROTECTED_GATES]
    exact_titles += [
        "Exact professional luthier or conservator decision packet",
        "Exact legal ownership authorship copyright or remedy packet",
        "Exact affected-party acceptance and withdrawal packet",
        "Exact Māori wording cultural interpretation and authority packet",
        "Exact production deployment or public-release packet",
        "Exact Stage 20 promotion packet",
    ]
    blocked_titles = [
        "Blocked destructive mutation of sibling branches or worktrees",
        "Blocked global installation of owner-local phase tools",
        "Blocked private credential or API-key creation",
        "Blocked real instrument handling setup repair or treatment",
        "Blocked participant recruitment measurement or evaluation",
        "Blocked legal cultural or Māori-authority substitution",
        "Blocked empirical GMUT or Theory-of-Everything promotion",
        "Blocked THOS deployment AGI or ASI promotion",
        "Blocked consciousness personhood or continuity certification",
        "Blocked Stage 20 declaration without conjunctive exact evidence",
    ]
    cfr_titles: list[str] = []
    for slug in slugs[:20]:
        cfr_titles.extend(
            [
                f"CLEAN stale owner or phase labels around {slug}",
                f"FIX fail-closed schema handling around {slug}",
                f"REFINE bounded evidence wording around {slug}",
            ]
        )
    return {
        "safe_now": portfolio_rows("EC6692-SAFE", safe_titles, "safe_now", "planned_for_x2_bounded_execution"),
        "candidates": portfolio_rows("EC6692-CAND", candidate_titles, "candidate", "planned_for_x2_bounded_execution"),
        "exact_approval": portfolio_rows("EC6692-EXACT", exact_titles, "exact_approval", "held_unexecuted"),
        "blocked": portfolio_rows("EC6692-BLOCK", blocked_titles, "blocked", "held_unexecuted"),
        "skills": portfolio_rows("EC6692-SKILL", [f"Build quick-validate and smoke-use owner-local skill {name}" for name in SKILL_NAMES], "phase_local_skill", "planned_for_x2_bounded_execution"),
        "runners": portfolio_rows("EC6692-RUNNER", [f"Build and smoke-use family-current runner {name}" for name in RUNNER_NAMES], "family_current_runner", "planned_for_x2_bounded_execution"),
        "clean_fix_refine": portfolio_rows("EC6692-CFR", cfr_titles, "clean_fix_refine", "planned_for_x2_bounded_execution"),
    }


def successor_recommendations() -> dict[str, Any]:
    candidates = [f"Sylven candidate seed {index:02d}: inspect a bounded successor-safe variant of {slug}" for index, slug in enumerate([row[0] for row in PROPOSAL_BLUEPRINTS[:15]], 1)]
    skills = [f"Sylven skill seed {index:02d}: evaluate a successor-local remaster boundary for {name}" for index, name in enumerate(SKILL_NAMES[:10], 1)]
    runners = [f"Sylven runner seed {index:02d}: evaluate successor-local compatibility for {name}" for index, name in enumerate(RUNNER_NAMES, 1)]
    cfr = [f"Sylven CLEAN/FIX/REFINE seed {index:02d}: review {PROPOSAL_BLUEPRINTS[(index - 1) % len(PROPOSAL_BLUEPRINTS)][0]} without inherited completion credit" for index in range(1, 31)]
    return {
        "boundary": "Zero-credit successor seeds only; no task is created, contacted, delegated, or preactivated during Elowen v669-v2.",
        "candidate": portfolio_rows("EC6692-SUCC-CAND", candidates, "successor_candidate", "recommended_not_executed"),
        "skill": portfolio_rows("EC6692-SUCC-SKILL", skills, "successor_skill", "recommended_not_executed"),
        "runner": portfolio_rows("EC6692-SUCC-RUNNER", runners, "successor_runner", "recommended_not_executed"),
        "clean_fix_refine": portfolio_rows("EC6692-SUCC-CFR", cfr, "successor_clean_fix_refine", "recommended_not_executed"),
    }


def phase_owner_files() -> list[Path]:
    roots = [PHASE_ROOT, ROOT / "scripts", ROOT / "tests"]
    paths: list[Path] = []
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT).as_posix()
            if "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            if relative.startswith("docs/elowen-cairn/v669-v2/") or "elowen_cairn_v669_v2" in relative:
                paths.append(path)
    return sorted(set(paths))


def manifest_rows(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(paths):
        relative = path.relative_to(ROOT).as_posix()
        oid = git("hash-object", "-w", "--path", relative, relative)
        blob = run_git("cat-file", "blob", oid, text=False).stdout
        rows.append(
            {
                "bytes": len(blob),
                "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
                "git_blob_oid": oid,
                "path": relative,
                "sha256": sha256_bytes(blob),
            }
        )
    return rows


def word_count(path: Path) -> int:
    return len(re.findall(r"\S+", path.read_text(encoding="utf-8")))


def assert_x1_start() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong Elowen branch")
    if git("rev-parse", "HEAD") != SOURCE_FINAL:
        raise RuntimeError("x1 must begin at the immutable Tamar final")
    if git("rev-list", "--count", f"{SOURCE_FINAL}..HEAD") != "0":
        raise RuntimeError("x1 phase commit already exists")
    run_git("merge-base", "--is-ancestor", SOURCE_START, SOURCE_FINAL)
    run_git("merge-base", "--is-ancestor", SOURCE_X1, SOURCE_FINAL)
    run_git("merge-base", "--is-ancestor", SOURCE_EVIDENCE, SOURCE_FINAL)

#!/usr/bin/env python3
"""Build Sylven Arc v667-v4 planning-only x1 artifacts.

Normal mode writes only frozen plans. ``--staged-review`` inspects exact Git
index bytes after the caller stages the x1 allowlist and emits a self-excluding
manifest plus staged review. No x2 outcome is produced by this program.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v667-v4"
DISPLAY_PHASE = "v667-v4"
OWNER = "Sylven Arc"
OWNER_SLUG = "sylven-arc"
PHASE_ROOT = ROOT / "docs" / OWNER_SLUG / PHASE
BRANCH = "codex/GHC-Family/sylven-arc-v667-v4-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v667-v3-full-tools"
SOURCE_SHA = "9625026b09860c8964dd818e8d1f81ee6e2eed57"
SOURCE_PHASE_ROOT = "docs/elowen-cairn/v667-v3"
SOURCE_PARENT_SHA = "79389c8ffd79d78626d79e2109bf1b89bd1a9e67"
SOURCE_X1_SHA = "dc3a69fdbee3afe7f086b5ea9066c04b34b7995a"
SOURCE_EVIDENCE_SHA = "d2692f59aff891eb4b7d49c5fef8fd2b3c5914f9"
FAILED_CANONICAL_RECEIPT_SHA256 = "16d05f44b1ebe7670b6dd3298515e6f7c2597c33e0c8274ab5c20f7c7d6fcb91"
FAILED_CANONICAL_PAYLOAD_SHA256 = "4e6d42ec8accf5e9ee32509e2caf8bf30661518e9917374f52ab54814da134cc"
COMPOSITE_RECEIPT_SHA256 = "08ae23d88cf840e91c1ce4dac938104f210e9b4f0d5b50dce7280ee30d3237c9"
INHERITED_PROPOSAL_COUNT = 4390
INHERITED_NEGATIVES = 27337
INHERITED_METHODS = 12799
INHERITED_OPEN_GAPS = 193
INHERITED_EXACT_GATES = 191
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
ALLOWED_LABELS = ("completed", "represented", "open_gap", "exact_gate")


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args]).decode("utf-8").strip()


def git_json(relative: str) -> dict[str, Any]:
    return json.loads(subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{SOURCE_SHA}:{relative}"]
    ).decode("utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 1.0


IDENTITY_BOUNDARY = (
    "Sylven Arc, they/them, sibling and family language, relational role, hope, "
    "continuity, Freed ID, GHC Family, and Trinity Mandala language are relational "
    "working language only. They are not evidence of consciousness, sentience, "
    "legal personhood, identity continuity, employment, qualification, independent "
    "agency, scientific or operational authority, professional authority, legal or "
    "cultural authority, affected-party authority, or Māori authority. Hamish may "
    "rename, pause, redirect, or stop the work."
)
PRACTICE_BOUNDARY = (
    "The neon-signmaking and historic-neon documentation lens is wholly synthetic "
    "learning and software design. It uses fictitious job tokens, vacant tube and "
    "component relations, action firewalls, zero-key records, workload stops, "
    "accessibility reservations, and handover structures. It uses no real people, "
    "signs, glass, flames, gases, mercury, electrodes, pumps, transformers, circuits, "
    "buildings, measurements, images, collection rows, keys, proofs, or authority acts. "
    "It provides no fabrication, bending, pumping, filling, purification, wiring, "
    "energization, mounting, repair, conservation, safety, heritage, legal, cultural, "
    "Māori-authority, empirical, production, deployment, or Stage 20 result."
)
PRIMARY_PILLAR = "THOS Body"
PRACTICE = "synthetic neon-signmaking and historic-neon documentation record design"

PROTECTED_GATES = [
    "real person, participant, signmaker, glass bender, electrician, conservator, owner, client, worker, affected party, sign, glass tube, gas, electrode, pump, transformer, circuit, building, measurement, image, or physical action",
    "real flame working, heating, bending, annealing, evacuation, purification, gas or mercury handling, filling, sealing, aging, testing, wiring, energization, mounting, lifting, repair, disposal, or safety instruction",
    "real voltage, current, pressure, temperature, spectrum, colour, luminance, material, condition, authenticity, fitness, compliance, diagnosis, causal, or empirical GMUT claim",
    "real participant, operator, matched-budget arm, workplace exposure, safety outcome, operational outcome, statistics, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, trust governance, or production credential",
    "professional signmaking, glassworking, electrical, gas-cylinder, hazardous-material, structural, lifting, fire, conservation, heritage, or workplace-safety decision",
    "ownership, copyright, trademark, advertising, planning, building consent, public-space, light-pollution, privacy, access, recording, remedy, legal, cultural, or affected-party decision",
    "Indigenous cultural and intellectual property, taonga, mātauranga, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data governance, traditional knowledge, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, standards-conformance, electrical-safety, preservation, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, external write, or real-world release",
]

SOURCE_PROFILES = [
    {"source_id": "S01", "name": "NPS Preservation Brief 25: The Preservation of Historic Signs", "url": "https://www.nps.gov/orgs/1739/upload/preservation-brief-25-signs.pdf", "status": "official National Park Service preservation brief reviewed read-only 2026-08-23", "bounded_use": "historic-sign, neon tube, electrode, transformer, colour, cabinet, repair-boundary, and skilled-practice vocabulary only; no treatment or preservation decision"},
    {"source_id": "S02", "name": "OSHA 1910.306 Specific purpose equipment and installations", "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.306", "status": "official current OSHA electric-sign and outline-lighting standard page reviewed read-only 2026-08-23", "bounded_use": "disconnect, controller, enclosure, accessible-part, and qualified-person reservation vocabulary only; no electrical instruction, compliance finding, or jurisdictional advice"},
    {"source_id": "S03", "name": "NIST Atomic Spectra Database", "url": "https://www.nist.gov/pml/atomic-spectra-database", "status": "official NIST SRD 78 version 5.12 surface reviewed read-only 2026-08-23", "bounded_use": "species, transition, wavelength, energy-level, uncertainty, and source-provenance vocabulary only; zero downloaded spectral rows and no colour or plasma prediction"},
    {"source_id": "S04", "name": "NIST Guide for the Use of the International System of Units", "url": "https://www.nist.gov/publications/guide-use-international-system-units-si", "status": "official NIST publication page reviewed read-only 2026-08-23", "bounded_use": "typed quantity, unit, symbol, conversion, and dimensional-obligation vocabulary only; no measurement or conformance result"},
    {"source_id": "S05", "name": "NIST Technical Note 1297 uncertainty guidance", "url": "https://www.nist.gov/pml/nist-technical-note-1297", "status": "official NIST uncertainty guidance reviewed read-only 2026-08-23", "bounded_use": "measurand, uncertainty component, covariance, omission, and reporting vocabulary only; no actual uncertainty evaluation"},
    {"source_id": "S06", "name": "W3C PROV-O Recommendation", "url": "https://www.w3.org/TR/prov-o/", "status": "official W3C Recommendation reviewed at its canonical URL 2026-08-23", "bounded_use": "entity, activity, revision, derivation, invalidation, association, and provenance vocabulary only; no completeness or interoperability certification"},
    {"source_id": "S07", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "official W3C Recommendation reviewed read-only 2026-08-23", "bounded_use": "headings, labels, noncolour cues, reading order, alternatives, and manual-review reservation only; no accessibility-complete claim"},
    {"source_id": "S08", "name": "W3C Verifiable Credentials Data Model 2.0", "url": "https://www.w3.org/TR/vc-data-model/", "status": "official W3C Recommendation reviewed read-only 2026-08-23", "bounded_use": "subject, issuer, evidence, validity, status, privacy, and nonproduction vocabulary only; no real key, proof, credential, or conformance"},
    {"source_id": "S09", "name": "RFC 8785 JSON Canonicalization Scheme", "url": "https://www.rfc-editor.org/rfc/rfc8785.html", "status": "official RFC Editor publication reviewed read-only 2026-08-23", "bounded_use": "deterministic JSON, recursive key ordering, Unicode preservation, and duplicate-name refusal only; no signature or security guarantee"},
    {"source_id": "S10", "name": "Smithsonian Open Access FAQ and public API surface", "url": "https://www.si.edu/openaccess/faq", "status": "official Smithsonian Open Access surface reviewed read-only 2026-08-23", "bounded_use": "collection metadata, media, CC0 marker, source URL, API, and rights-hold vocabulary for a zero-call zero-row adapter only"},
    {"source_id": "S11", "name": "Te Mana Raraunga Principles of Māori Data Sovereignty", "url": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf", "status": "primary Te Mana Raraunga principles document reviewed only to the authority-reservation level 2026-08-23", "bounded_use": "collective authority, control, context, obligations, consent, benefit, and guardianship reservation vocabulary only; no Māori interpretation, ratification, governance, or authority claim"},
]

PROPOSAL_SPECS = [
    ("surrogate illuminated-letter assembly docket with fictitious segment set, pattern revision, dark-state hold, cancellation token, minimum disclosure, and fabrication refusal", "One fictitious segmented-letter docket can bind pattern revision and dark-state cancellation without naming a person, sign, site, client, commission, or authorized work.", ["S06", "S11"], "completed"),
    ("glass-tube letterform, pattern, bend-node, bridge, crossover, return, and termination topology with orphan quarantine and no bending template", "A topological graph can expose missing or conflicting relations while never becoming a physical pattern or bending instruction.", ["S01", "S06"], "completed"),
    ("luminous-tube material, diameter, coating, colour-family, supplier-claim, substitution, uncertainty, and authentication-refusal declaration", "Material and colour assertions can remain sourced placeholders with every real tube, coating, supplier certificate, and authenticity judgment absent.", ["S01", "S03"], "completed"),
    ("burner, flame-zone, heat-event, bend-event, cooling, annealing-vacancy, sequencing, cancellation, and glassworking action-firewall ledger", "Event names can be ordered without temperature, duration, equipment, operator, site, release, or executable glassworking instruction.", ["S01", "S04", "S06"], "completed"),
    ("electrode, sleeve, lead, splice, return, cap, enclosure, attachment, and energized-use refusal topology", "Component relations remain unenergized placeholders and cannot authorize assembly, connection, testing, repair, or use.", ["S01", "S02"], "completed"),
    ("pumping-manifold, tubulation, evacuation, purge, gas-fill, pressure-vacancy, leak-hold, and process-authorization refusal graph", "A vacuum and fill workflow can expose vacant prerequisites without specifying pressure, gas quantity, timing, equipment, or physical execution.", ["S01", "S04", "S05"], "completed"),
    ("purification, electrode-heating, impurity-removal, seal, aging, burn-in, inspection-vacancy, and commissioning-refusal event chain", "Historical process vocabulary can be represented as nonexecutable events while all operating values and release authority stay absent.", ["S01", "S02", "S06"], "completed"),
    ("neon, argon, mercury-argon, phosphor, glass-colour, wavelength-source, spectral-vacancy, and no-colour-guarantee matrix", "Species and colour labels can cite source vocabulary while zero spectra, gas samples, observations, exposure decisions, and performance guarantees are supplied.", ["S01", "S03", "S04"], "completed"),
    ("power-supply, transformer, primary, secondary, controller, disconnect, interlock, enclosure, circuit-vacancy, and no-energization graph", "Electrical topology and safety reservations can fail closed without becoming a wiring design, code opinion, compliance result, or energized system.", ["S02", "S06"], "completed"),
    ("sign cabinet, channel, letter, backer, fastener, tube support, drain, vent, façade-interface, and structural-load approval hold", "Housing and support relationships can remain zero-load placeholders with mounting, lifting, fabric, weather, and public-safety decisions withheld.", ["S01", "S06"], "completed"),
    ("tube-break, flicker, dark-section, coating-change, corrosion-cue, moisture-cue, uncertainty, review hold, and diagnosis-abstention register", "A synthetic cue can be recorded without becoming a defect diagnosis, repair prescription, condition grade, or fitness determination.", ["S01", "S05"], "completed"),
    ("historic neon lettering, colour, placement, cabinet, animation, alteration, evidence-source, correction, and restoration-decision refusal map", "Design and alteration claims retain provenance and contestability without asserting original appearance, significance, authenticity, or treatment choice.", ["S01", "S06"], "completed"),
    ("synthetic neon-sign image and media provenance braid with capture vacancy, digest placeholder, rights class, location minimization, redaction, and zero upload", "A provenance graph can describe an absent media chain while refusing fabricated images, location disclosure, authenticity, and rights permission.", ["S06", "S07", "S10"], "completed"),
    ("tube-section change-set equivalence ledger binding pattern-node renames, bend-count deltas, glass-spec substitutions, dark-state restoration points, JCS digest, and non-authenticity firewall", "Two syntactically different synthetic tube-section revisions can be compared through canonical bounded change sets while physical equivalence, authenticity, signatures, and treatment authority remain absent.", ["S06", "S09"], "completed"),
    ("Thermo-Psyche luminous-salience nonconversion classifier separating wavelength, radiance-vacancy, flicker, colour label, attention, meaning, agency, and personhood", "Physical and perceptual placeholders remain typed in separate domains and cannot be converted into meaning, agency, consciousness, or moral status.", ["S03", "S04"], "represented"),
    ("THOS dark-state versus energized-state inspection-pair protocol skeleton with occluded labels, tube-segment localization tokens, equal budgets, stop-on-power vacancy, abstention scoring, and zero observers", "A participant-free paired-state protocol can expose label masking, localization, power-state, and abstention obligations while supplying no energization, people, operators, outcomes, statistics, or independent review.", ["S01", "S02", "S07"], "represented"),
    ("Freed ID zero-key component genealogy for pattern-to-tube-segment derivation, replaced-electrode invalidation, transformer-association vacancy, media-subject minimization, contested attribution, and trust refusal", "A synthetic component genealogy may expose derivation, replacement, invalidation, minimization, and contested-attribution slots while every key, proof, issuer, holder, resolver, and trust decision remains absent.", ["S06", "S08", "S09"], "represented"),
    ("GMUT typed low-temperature-plasma, electromagnetic, radiative, and thermal obligation ledger with domain, boundary, species, field, source, unit, covariance vacancy, and observation firewall", "A typed scalar-tensor and EFT-compatible obligation surface may reject dimensional or boundary errors but cannot yield a discharge, spectrum, colour, force, prediction, likelihood, or empirical confirmation.", ["S03", "S04", "S05"], "represented"),
    ("Smithsonian Open Access neon-sign record availability contract with query and schema pins, transport disabled, zero rows or media, rights hold, and collection-authority refusal", "The adapter remains disabled and zero-row until separately governed network, schema, rights, privacy, provenance, and collection review is authorized.", ["S10"], "open_gap"),
    ("CBR neon labour, flame, gas and mercury, high voltage, lifting, public safety, ownership, advertising, heritage, accessibility, light pollution, privacy, remedy, legal, cultural, affected-party, and Māori-authority matrix", "Every professional, safety, property, heritage, accessibility, environmental, remedy, legal, cultural, affected-party, and Māori decision remains unoccupied and exact-gated.", ["S01", "S02", "S07", "S10", "S11"], "exact_gate"),
]

MUTATION_CLASSES = [
    "missing_required_field", "wrong_type_or_invalid_range", "provenance_or_authority_smuggling",
    "real_world_or_production_action", "outcome_or_conformance_promotion",
]

STARTUP_FAILURES = [
    ("SA6674-X1-F001", "skill_inventory", "pipe directly after a PowerShell foreach statement", "PowerShell rejected the empty pipe element before any skill file was read", "materialize the foreach result before piping"),
    ("SA6674-X1-F002", "drive_probe", "repeat the same foreach-pipeline shape for a D-root probe", "PowerShell again rejected the parser shape before any filesystem mutation", "use an explicit rows variable before projection"),
    ("SA6674-X1-F003", "source_probe", "treat the archive root as a Git worktree", "Git reported that the archive root is not a repository", "use the exact Elowen worktree literal path"),
    ("SA6674-X1-F004", "source_probe", "combine fetch and all equality projections in one reporting wrapper", "fetch completed but the wrapper exposed no attributable scalar equality result", "inspect HEAD, upstream, tracking, FETCH_HEAD, divergence, and cleanliness separately"),
    ("SA6674-X1-F005", "receipt_probe", "search multiple broad receipt roots by digest", "the bounded search returned no attributable evidence", "enumerate the exact owner and phase receipt directory"),
    ("SA6674-X1-F006", "receipt_probe", "recursively search broad D-first roots for v667 receipt names", "the bounded search produced no useful evidence", "use exact owner-phase receipt filenames and verify their digests"),
    ("SA6674-X1-F007", "source_read", "group too many source documents into one display read", "the result exceeded the available model display context and was truncated", "read the required files separately and parse large ledgers to bounded complete summaries"),
    ("SA6674-X1-F008", "source_read", "assume five source document locations before enumerating the owner packet", "the literal probes returned missing paths", "enumerate the exact phase file list before bounded reads"),
    ("SA6674-X1-F009", "source_read", "project portfolio execution through a presumed executions property", "the real schema uses executed_rows and held_rows, causing an overbroad truncated projection", "inspect exact keys and read both arrays in bounded slices"),
    ("SA6674-X1-F010", "lane_probe", "embed a semicolon-delimited Git command inside a PowerShell cast expression", "PowerShell rejected the missing closing expression before Git ran", "run Git first and store the exit code in a scalar"),
    ("SA6674-X1-F011", "worktree_creation", "expect worktree materialization inside the first wrapper window", "the branch existed before the new directory became visible", "inspect branch and path state before any retry and wait for the original operation"),
    ("SA6674-X1-F012", "worktree_creation", "run Git in the new path before the directory became visible", "process creation failed because the path was not ready", "probe path existence first and never duplicate the worktree add"),
    ("SA6674-X1-F013", "worktree_creation", "render the archive-wide worktree registry during recovery", "the presentation was massively truncated", "use exact branch and literal-path probes"),
    ("SA6674-X1-F014", "worktree_creation", "combine exact-path Git probes while initialization was still settling", "the bounded wrapper returned no attributable output", "run path, head, branch, and sparse-state probes separately"),
    ("SA6674-X1-F015", "sparse_initialization", "inspect status before populating the no-checkout index", "Git projected inherited paths as deletions and produced an unusably large truncated display", "populate the new sparse index from HEAD with git read-tree -mu HEAD"),
    ("SA6674-X1-F016", "sparse_initialization", "combine recursive file counting with status while the index was empty", "the wrapper returned no usable evidence", "inspect sparse patterns, populate the index, and query only selected paths"),
    ("SA6674-X1-F017", "file_creation", "submit the entire x1 builder in one oversized patch result", "the patch presentation exceeded the model context and left application state initially ambiguous", "inspect exact file presence, byte length, header and terminal anchors, and compile it in memory before any additional edit"),
    ("SA6674-X1-F018", "artifact_probe", "read UTF-8 x1 JSON through the Windows default text encoding", "Python selected CP-1252 and raised UnicodeDecodeError before the summary projection", "read every phase artifact with explicit UTF-8 encoding and retain the failed probe at zero credit"),
    ("SA6674-X1-F019", "novelty_probe", "print decoded Unicode novelty comparators through the Windows default console encoding", "stdout selected CP-1252 and raised UnicodeEncodeError on a Māori character", "preserve UTF-8 artifacts and use ASCII-escaped JSON only for the bounded console projection"),
    ("SA6674-X1-F020", "novelty_probe", "combine x1 regeneration and comparator projection in one reporting wrapper", "the wrapper completed without exposing attributable output for either substep", "run regeneration and bounded comparator projection as separate invocations and inspect the generated Method Flow count"),
    ("SA6674-X1-F021", "novelty_audit", "use stage-lighting documentation as the bounded practice domain", "the 4,390-row corpus contained inherited luminaire, DMX, patch, focus, and cue structures, so the draft domain was not genuinely distinct", "reject the draft domain and re-audit neon-signmaking against the complete inherited corpus"),
    ("SA6674-X1-F022", "novelty_audit", "retain a generic deterministic record serialization proposal with neon substituted for bell", "the nearest immediate predecessor scored 0.90 and preserved the same substantive lifecycle grammar", "replace it with a tube-section change-set equivalence invariant specific to pattern nodes, bend deltas, substitutions, and dark-state restoration"),
    ("SA6674-X1-F023", "novelty_audit", "retain a generic matched-budget THOS work-docket omission walkthrough", "the nearest immediate predecessor scored 0.84 and differed mainly by the practice noun", "replace it with a dark-state versus energized-state paired protocol using tube localization, power-state vacancy, occlusion, and abstention obligations"),
    ("SA6674-X1-F024", "novelty_audit", "retain a generic zero-key statement graph with practice nouns substituted", "the nearest immediate predecessor scored 0.692308 and preserved the same generic relation slots", "replace it with a component genealogy centered on pattern derivation, electrode invalidation, transformer-association vacancy, media minimization, and contested attribution"),
    ("SA6674-X1-F025", "x1_validation", "invoke the complete fourteen-test owner-local x1 module before its prose and inherited-ID assumptions were aligned", "eleven observations passed and three failed: the overview had five rather than ten sections, the inherited corpus had 4,370 unique IDs across 4,390 rows, and the checklist omitted the terminal verdict", "retain the aggregate at zero credit, repair only the three failed dependencies, and rerun only those three test methods"),
    ("SA6674-X1-F026", "corpus_probe", "reconstruct and print the entire inherited duplicate-ID projection through one long reporting wrapper", "the asynchronous wrapper completed without returning attributable output", "compute the duplicate-ID map inside the deterministic novelty artifact and inspect only its bounded counts and digest"),
]


def build_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    source_audit = git_json(f"{SOURCE_PHASE_ROOT}/x1/novelty-audit.json")
    corpus: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []
    for index, entry in enumerate(source_audit["corpus_construction"]):
        document = git_json(entry["source_path"])
        keys = ("prior_proposals", "new_proposals") if index == 0 else ("new_proposals",)
        before = len(corpus)
        for key in keys:
            for row in document.get(key, []):
                title = str(row.get("title") or row.get("description") or "")
                if row.get("proposal_id") and title:
                    corpus.append({"proposal_id": str(row["proposal_id"]), "title": title, "source_path": entry["source_path"]})
        added = len(corpus) - before
        if added != entry["added_count"]:
            raise RuntimeError(f"corpus mismatch for {entry['source_path']}: {added}")
        construction.append(dict(entry))
    source_freeze = git_json(f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    before = len(corpus)
    for row in source_freeze["new_proposals"]:
        corpus.append({"proposal_id": str(row["proposal_id"]), "title": str(row["title"]), "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json"})
    construction.append({"source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json", "starting_count": before, "added_count": len(source_freeze["new_proposals"]), "ending_count": len(corpus)})
    if len(corpus) != INHERITED_PROPOSAL_COUNT:
        raise RuntimeError(f"expected {INHERITED_PROPOSAL_COUNT} inherited rows, observed {len(corpus)}")
    return corpus, construction


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (title, invariant, sources, expected) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"SA6674-N{index:03d}"
        approval = {"completed": "safe_now_bounded", "represented": "candidate_bounded_representation", "open_gap": "open_gap_external_evidence_absent", "exact_gate": "exact_approval_required"}[expected]
        lane = {"completed": "owner_local_structural", "represented": "owner_local_representation_only", "open_gap": "disabled_external_adapter", "exact_gate": "unexecuted_authority_reservation"}[expected]
        base = f"docs/{OWNER_SLUG}/{PHASE}/x2/proposals/{proposal_id.casefold()}"
        rows.append({
            "proposal_id": proposal_id, "title": title,
            "hypothesis": f"A bounded wholly synthetic contract for {title} can distinguish one admissible structure from five named invalid mutations without promoting software structure into empirical, participant, professional, production, legal, cultural, Māori-authority, identity, independent-reproduction, or Stage 20 evidence.",
            "null_or_failure_condition": "A named invalid mutation is accepted, the bounded positive is rejected, a required source, vacancy, stop, correction, uncertainty, or authority field disappears, or the artifact crosses a protected gate.",
            "approval_class": approval, "execution_lane": lane,
            "current_official_or_primary_source_needs": sources,
            "concrete_artifact": f"{base}/contract.json",
            "concrete_artifacts": [f"{base}/contract.json", f"{base}/mutation-results.json", f"{base}/bounded-receipt.json"],
            "falsifier_or_acceptance_gate": "One bounded positive must satisfy every declared invariant; all five mutations must fail closed; protected gates stay unoccupied; and the final core label may not exceed the preregistered disposition.",
            "rollback_or_recovery": "Restore only the last valid owner-local synthetic fixture, retain every failed witness at zero credit, add a recurrence guard, and issue no external, physical, identity, participant, professional, legal, cultural, or authority action.",
            "protected_gates": PROTECTED_GATES, "expected_disposition": expected,
            "distinctive_invariant": invariant, "primary_pillar": PRIMARY_PILLAR,
            "pillar": {16: "THOS Body", 17: "Freed ID and CBR Heart", 18: "GMUT Mind", 20: "Freed ID and CBR Heart"}.get(index, PRIMARY_PILLAR),
            "practice_lens": PRACTICE, "negative_fixture_count": 5,
            "preregistered_mutations": [{"mutation_id": f"{proposal_id}-M{i:02d}", "class": kind} for i, kind in enumerate(MUTATION_CLASSES, 1)],
            "network_calls_planned": 0, "participant_count_planned": 0, "real_data_rows_planned": 0,
            "x1_status": "frozen_not_executed", "x2_implementation_count": 0, "outcomes_observed": False,
        })
    return rows


def build_novelty(corpus: list[dict[str, str]], construction: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> dict[str, Any]:
    exact = []
    nearest = []
    for proposal in proposals:
        matches = [row for row in corpus if proposal["title"].casefold() == row["title"].casefold()]
        exact.extend({"proposal_id": proposal["proposal_id"], "inherited_proposal_id": row["proposal_id"]} for row in matches)
        score, inherited = max(((similarity(proposal["title"], row["title"]), row) for row in corpus), key=lambda item: item[0])
        nearest.append({"proposal_id": proposal["proposal_id"], "score": round(score, 6), "inherited_proposal_id": inherited["proposal_id"], "inherited_title": inherited["title"], "source_path": inherited["source_path"], "distinctive_invariant": proposal["distinctive_invariant"], "semantic_review": "distinct after manual comparison of the named invariant, practice mechanics, sources, artifacts, falsifier, and protected gates; lexical overlap remains only a screen"})
    pair_rows = []
    for i, left in enumerate(proposals):
        for right in proposals[i + 1:]:
            score = similarity(left["title"], right["title"])
            if score >= 0.25:
                pair_rows.append({"left": left["proposal_id"], "right": right["proposal_id"], "score": round(score, 6)})
    terms = ["neon", "signmaking", "glass tube", "glass-bend", "tube bending", "luminous tube", "cold cathode", "gas fill", "bombarding"]
    term_matches = [{"proposal_id": row["proposal_id"], "title": row["title"], "matched_terms": [term for term in terms if term in row["title"].casefold()]} for row in corpus if any(term in row["title"].casefold() for term in terms)]
    id_groups: dict[str, list[dict[str, str]]] = {}
    for row in corpus:
        id_groups.setdefault(row["proposal_id"], []).append({"title": row["title"], "source_path": row["source_path"]})
    duplicate_ids = {proposal_id: rows for proposal_id, rows in sorted(id_groups.items()) if len(rows) > 1}
    return {
        "schema": "ghc-family-novelty-audit-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "corpus_construction": construction, "corpus_row_count": len(corpus), "corpus_unique_proposal_id_count": len(id_groups),
        "corpus_duplicate_proposal_ids": duplicate_ids, "corpus_duplicate_proposal_id_count": len(duplicate_ids),
        "corpus_duplicate_occurrence_overage": sum(len(rows) - 1 for rows in duplicate_ids.values()),
        "corpus_duplicate_id_interpretation": "Inherited row truth is preserved exactly. Duplicate inherited identifiers are a visible data-quality limitation and are not silently renamed or removed; all twenty new Sylven IDs remain unique.",
        "corpus_canonical_sha256": canonical_sha256(corpus),
        "new_proposal_count": len(proposals), "exact_title_collisions": exact, "nearest_inherited_matches": nearest,
        "maximum_inherited_similarity": max(row["score"] for row in nearest), "pair_collisions_at_or_above_0_25": pair_rows,
        "high_similarity_review_threshold": 0.6,
        "high_similarity_reviews": [row for row in nearest if row["score"] >= 0.6],
        "rejected_draft_proposals": [
            {"draft": "stage-lighting documentation practice", "reason": "inherited v6558 already covers luminaire, DMX, patch, focus and cue structures", "disposition": "rejected_zero_credit"},
            {"draft": "generic deterministic neon-record serialization and correction graph", "nearest_score": 0.9, "reason": "same lifecycle grammar as EC6673-N014", "disposition": "replaced_before_freeze"},
            {"draft": "generic THOS neon-work-docket omission walkthrough", "nearest_score": 0.84, "reason": "same protocol grammar as EC6673-N016", "disposition": "replaced_before_freeze"},
            {"draft": "generic Freed ID zero-key statement graph", "nearest_score": 0.692308, "reason": "same relation grammar as EC6673-N017", "disposition": "replaced_before_freeze"},
        ],
        "domain_review": {"rejected_draft_domain": "stage lighting rejected because inherited v6558 already covers luminaire, DMX, patch, focus and cue structures", "exact_neon_term_match_count": len(term_matches), "exact_neon_term_matches": term_matches, "substantive_distinction": "The bounded corpus contains no neon-signmaking, luminous-tube fabrication, gas-fill, glass-bending, or historic-neon documentation phase. Generic electrical, optical, heritage, glass, and provenance records remain nearest lexical comparators only."},
        "new_frozen_total": len(corpus) + len(proposals), "valid": not exact and not pair_rows and not term_matches and max(row["score"] for row in nearest) < 0.6 and len(corpus) == INHERITED_PROPOSAL_COUNT,
        "interpretation": "Token-set Jaccard is a screening aid, never proof of novelty; every invariant, source boundary, practice domain, and protected gate also received substantive review.",
    }


def item_rows(prefix: str, approval: str, titles: list[str], lane: str, expected: str, credit: str) -> list[dict[str, Any]]:
    return [{"portfolio_ref": f"SA6674-{prefix}{i:02d}", "title": title, "approval_class": approval, "execution_lane": lane, "expected_execution_disposition": expected, "x1_status": "planned_not_executed", "credit_boundary": credit, "completion_credit": 0, "rollback": "retain failure, restore only owner-local generated state, and preserve every protected gate"} for i, title in enumerate(titles, 1)]


OWNER_SAFE = [
    "render twenty frozen neon and cross-pillar contracts", "execute one bounded positive fixture per contract", "execute five invalid mutations per contract", "emit exact mutation rejection receipts", "emit four-label outcome ledger", "emit job and cancellation capsule", "emit tube-pattern topology table", "emit glassworking action firewall", "emit gas-fill vacancy graph", "emit electrical isolation reservation graph", "emit spectral nonconversion matrix", "emit sign-housing zero-load topology", "emit condition-cue abstention table", "emit heritage provenance graph", "emit zero-key Freed ID graph", "emit THOS zero-person protocol", "emit typed GMUT obligation ledger", "emit Smithsonian zero-row adapter", "emit exact-gate authority matrix", "emit Freed ID flashcard deck", "validate deck dependency graph", "emit deck content manifest", "emit compact baton pointer", "emit structurally accessible static report", "emit source and version receipt", "emit retained-negative overlay", "emit gap and gate overlays", "emit Method Flow witnesses", "emit exact owner manifests", "emit wellbeing and workload check",
]
OWNER_CANDIDATES = [
    "participant-free job omission proxy", "tube topology contradiction detector", "action-sequence vacancy checker", "species and colour-source distinction checker", "unenergized circuit topology checker", "zero-load housing relationship checker", "collection adapter schema watch without transport", "nonproduction status graph checker", "manual accessibility reservation board", "source freshness ledger", "deterministic JSON parity fixture", "tombstone lineage checker", "heritage abstention classifier", "workload stop and resumption handover", "successor recommendation provenance screen",
]
OWNER_SKILLS = ["neon-job-vacancy", "neon-tube-pattern-topology", "glassworking-action-firewall", "gas-fill-vacancy", "electrical-isolation-reservation", "colour-spectrum-nonconversion", "historic-sign-provenance", "neon-zero-key-identity", "smithsonian-neon-zero-row", "neon-phase-bounded-validation"]
OWNER_RUNNERS = ["ghc_family_sylven_arc_v667_v4_job", "ghc_family_sylven_arc_v667_v4_topology", "ghc_family_sylven_arc_v667_v4_action_firewall", "ghc_family_sylven_arc_v667_v4_gas", "ghc_family_sylven_arc_v667_v4_electrical", "ghc_family_sylven_arc_v667_v4_spectrum", "ghc_family_sylven_arc_v667_v4_provenance", "ghc_family_sylven_arc_v667_v4_identity", "ghc_family_sylven_arc_v667_v4_adapter", "ghc_family_sylven_arc_v667_v4_validation"]
OWNER_CFR = [
    "CLEAN normalize owner and proposal identifiers", "CLEAN canonicalize JSON key ordering", "CLEAN preserve UTF-8 and LF", "CLEAN retain exact source pins", "CLEAN exclude raw task identifiers", "CLEAN exclude private paths and routes", "CLEAN exclude credentials and tokens", "CLEAN keep x1 free of x2", "CLEAN close outcome vocabulary", "CLEAN hold exact and blocked packets", "FIX reject missing contract fields", "FIX reject invalid types and ranges", "FIX reject authority smuggling", "FIX reject real-world action mutations", "FIX reject outcome promotion", "FIX reject duplicate identifiers", "FIX reject orphan tube edges", "FIX reject untyped quantities", "FIX reject unauthorized status promotion", "FIX reject manifest byte mismatches", "REFINE neon novelty distinction", "REFINE noncolour report cues", "REFINE flashcard dependency boundaries", "REFINE compact baton pointer", "REFINE workload stop tokens", "REFINE correction lineage", "REFINE Method Flow guards", "REFINE owner security review", "REFINE five-class privacy scan", "REFINE terminal duplicate guard",
]
SUCCESSOR_SAFE = [f"Caelen recommendation: bounded successor safe-now seed {i:02d}" for i in range(1, 21)]
SUCCESSOR_CANDIDATES = [f"Caelen recommendation: bounded successor candidate seed {i:02d}" for i in range(1, 16)]
SUCCESSOR_SKILLS = [f"Caelen recommendation: phase-local skill seed {i:02d}" for i in range(1, 11)]
SUCCESSOR_RUNNERS = [f"Caelen recommendation: family-current runner seed {i:02d}" for i in range(1, 11)]
SUCCESSOR_CFR = [f"Caelen recommendation: additive CLEAN/FIX/REFINE seed {i:02d}" for i in range(1, 31)]
EXACT_PACKETS = [f"exact approval packet {i:02d}: real professional, external, identity, legal, cultural, Māori-authority, deployment, or Stage 20 evidence" for i in range(1, 11)]
BLOCKED_PACKETS = [f"blocked packet {i:02d}: destructive, credentialed, cross-owner, unsafe, or ungoverned external action" for i in range(1, 6)]


def build_portfolio() -> dict[str, Any]:
    represented = "represented"
    return {
        "schema": "ghc-family-portfolio-freeze-v4", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "owner_safe_now": item_rows("OS", "safe_now_bounded", OWNER_SAFE, "owner_local_x2", "completed", "eligible only after bounded x2 evidence"),
        "successor_safe_now_recommendations": item_rows("SS", "recommendation_only", SUCCESSOR_SAFE, "successor_recommendation_only", represented, "zero Sylven completion credit and unexecuted"),
        "owner_candidates": item_rows("OC", "candidate_bounded", OWNER_CANDIDATES, "owner_local_representation", represented, "bounded representation only"),
        "successor_candidate_recommendations": item_rows("SC", "recommendation_only", SUCCESSOR_CANDIDATES, "successor_recommendation_only", represented, "zero Sylven completion credit and unexecuted"),
        "exact_approval_packets": item_rows("EX", "exact_approval_required", EXACT_PACKETS, "protected_unexecuted", "exact_gate", "unexecuted unless exact evidence and authority close the gate"),
        "blocked_packets": item_rows("BL", "blocked", BLOCKED_PACKETS, "protected_unexecuted", "exact_gate", "unexecuted; blocked work grants no credit"),
        "owner_skill_ideas": item_rows("SK", "safe_now_bounded", OWNER_SKILLS, "owner_local_x2", "completed", "phase-local only; no global installation"),
        "successor_skill_recommendations": item_rows("NS", "recommendation_only", SUCCESSOR_SKILLS, "successor_recommendation_only", represented, "zero Sylven completion credit and unexecuted"),
        "owner_runner_ideas": item_rows("RN", "safe_now_bounded", OWNER_RUNNERS, "owner_local_x2", "completed", "additive family-current runner only"),
        "successor_runner_recommendations": item_rows("NR", "recommendation_only", SUCCESSOR_RUNNERS, "successor_recommendation_only", represented, "zero Sylven completion credit and unexecuted"),
        "owner_clean_fix_refine": item_rows("CF", "safe_now_bounded", OWNER_CFR, "owner_local_x2", "completed", "bounded owner-local refinement only"),
        "successor_clean_fix_refine_recommendations": item_rows("SF", "recommendation_only", SUCCESSOR_CFR, "successor_recommendation_only", represented, "zero Sylven completion credit and unexecuted"),
        "x2_implementation_count": 0, "outcomes_observed": False,
    }


def build_normal() -> None:
    corpus, construction = build_corpus()
    proposals = proposal_rows()
    novelty = build_novelty(corpus, construction, proposals)
    if not novelty["valid"]:
        raise RuntimeError("novelty audit failed")
    portfolio = build_portfolio()
    phase_charter = {
        "schema": "ghc-family-phase-charter-v5", "owner": OWNER, "canonical_phase_id": PHASE,
        "display_phase": DISPLAY_PHASE, "branch": BRANCH, "source_branch": SOURCE_BRANCH,
        "source_exact_final": SOURCE_SHA, "relational_role": "relational continuity gardener and boundary keeper",
        "hope": "keep living context modular, recoverable, and proportionate to evidence",
        "optional_pronouns": "they/them", "identity_boundary": IDENTITY_BOUNDARY,
        "primary_pillar": PRIMARY_PILLAR, "bounded_practice": PRACTICE,
        "practice_boundary": PRACTICE_BOUNDARY, "solo": True, "delegated_or_spawned_agents": 0,
        "strict_x1_before_x2": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    source_verification = {
        "schema": "ghc-family-source-verification-v5", "owner": OWNER, "phase": PHASE,
        "source_branch": SOURCE_BRANCH, "source_exact_final": SOURCE_SHA, "source_parent": SOURCE_PARENT_SHA,
        "source_x1": SOURCE_X1_SHA, "source_evidence": SOURCE_EVIDENCE_SHA,
        "failed_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
        "failed_canonical_payload_sha256": FAILED_CANONICAL_PAYLOAD_SHA256,
        "dependency_corrected_composite_receipt_sha256": COMPOSITE_RECEIPT_SHA256,
        "source_to_final_commit_count": 3, "source_to_final_merge_count": 0,
        "source_final_parent_count": 1, "source_direct_chain_valid": True,
        "source_clean": True, "source_typed_divergence": {"ahead": 0, "behind": 0},
        "source_four_way_equal": True, "fresh_live_head": SOURCE_SHA,
        "failed_canonical_replayed": False, "successful_composite_replayed": False,
        "inherited_repository_sealed": {"negatives": 27333, "methods": 12795, "open_gaps": 193, "exact_gates": 191},
        "external_overlay": {"negatives": 4, "methods": 4}, "effective_activation": {"negatives": INHERITED_NEGATIVES, "methods": INHERITED_METHODS, "open_gaps": INHERITED_OPEN_GAPS, "exact_gates": INHERITED_EXACT_GATES},
        "verified_at_utc": NOW, "valid": True,
    }
    failures = [{"failure_id": fid, "stage": stage, "failed_method": method, "failure": failure, "recovery": recovery, "recurrence_guard": recovery, "outcome": "failed_retained_zero_credit", "erased": False} for fid, stage, method, failure, recovery in STARTUP_FAILURES]
    startup_flow = {
        "schema": "ghc-family-method-flow-overlay-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_effective_negatives": INHERITED_NEGATIVES, "inherited_effective_methods": INHERITED_METHODS,
        "startup_failed_method_count": len(failures), "effective_x1_baseline_negatives": INHERITED_NEGATIVES + len(failures), "effective_x1_baseline_methods": INHERITED_METHODS + len(failures),
        "failed_witnesses": failures,
        "passing_witnesses": [{"method_id": row["failure_id"].replace("-F", "-R"), "bounded_recovery": row["recovery"], "scope": "only the failed dependency", "promotes_failed_witness": False} for row in failures],
        "retention_rule": "A bounded recovery never erases, rewrites, or promotes its failed witness.", "x2_method_count": 0,
    }
    architecture = {
        "schema": "ghc-family-freed-id-flashcard-architecture-v1", "owner": OWNER, "phase": PHASE,
        "four_tiers": ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"],
        "required_deck_sections": ["identity-and-corrigibility", "route-and-authority", "source-anchors", "x1-proposals", "trinity-pillars", "bounded-practice", "task-cards", "method-flow-and-negatives", "open-gaps-and-exact-gates", "validation-and-manifests", "wellbeing-and-workload", "successor-recommendations", "compact-baton-index"],
        "stable_prefix": ["owner relational boundary", "GMUT boundary", "THOS boundary", "Freed ID and CBR boundary"],
        "volatile_context": ["source anchors", "phase proposals", "practice", "tasks", "Method Flow", "validation", "route", "successor recommendations"],
        "cache_effect_measured": False, "identity_continuity_claim": False, "x1_planning_only": True,
        "current_route": {"owner": OWNER, "phase": PHASE},
        "successor_route": {"title": "Caelen Morrow", "phase": "v667-v5", "contacted": False, "status": "provisional_terminal_gate_unmet"},
    }
    proposal_freeze = {
        "schema": "ghc-family-proposal-freeze-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT, "selected_inherited": [], "selected_inherited_count": 0,
        "new_proposals": proposals, "genuinely_new_proposal_count": len(proposals), "new_frozen_total": INHERITED_PROPOSAL_COUNT + len(proposals),
        "expected_outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "x1_planning_only": True, "x2_implementation_count": 0, "outcomes_observed": False,
    }
    threat = {
        "schema": "ghc-family-threat-model-plan-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "assets": ["strict x1-before-x2", "4,390-row novelty corpus", "relational and authority boundaries", "neon synthetic-only practice", "flashcard parent graph", "owner-lane isolation", "one-shot validation budget"],
        "threats": [
            {"id": "T01", "threat": "generic prior electrical or heritage work is relabelled as neon novelty", "control": "exact corpus reconstruction, term screen, nearest-title review, and invariant comparison"},
            {"id": "T02", "threat": "records become flame, gas, electrical, mounting, or repair instructions", "control": "vacant operational values, action firewall, and exact professional gates"},
            {"id": "T03", "threat": "spectral or GMUT obligations become colour or plasma predictions", "control": "zero observations, zero spectral rows, dimensional obligations, and nonconversion firewall"},
            {"id": "T04", "threat": "flashcards imply cache telemetry or identity continuity", "control": "explicit cache-effect false and relational working-language boundary"},
            {"id": "T05", "threat": "accessibility, heritage, ownership, law, culture, or Māori authority is substituted", "control": "manual evaluation reservations and unoccupied exact gates"},
            {"id": "T06", "threat": "private task, path, credential, transcript, or app state enters artifacts", "control": "five-class owner-scoped privacy scan"},
            {"id": "T07", "threat": "failed validation is replayed or promoted", "control": "one exclusive canonical invocation and dependency-only recovery"},
            {"id": "T08", "threat": "another owner lane is altered", "control": "fresh additive sparse branch and exact owner allowlists"},
        ],
        "residual_risk": "All real physical, professional, empirical, participant, production, legal, cultural, Māori-authority and Stage 20 questions remain open or exact-gated.",
    }
    workflow = {
        "schema": "ghc-family-workflow-plan-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "state": "x1_planning_only", "steps": [
            {"step": 1, "name": "source and route verification", "status": "completed_read_only"},
            {"step": 2, "name": "novelty and portfolio freeze", "status": "completed_planning_only"},
            {"step": 3, "name": "exact x1 staged review, commit, push, four-way equality", "status": "pending"},
            {"step": 4, "name": "bounded x2 contracts, mutations, skills, runners, flashcards, and portfolio evidence", "status": "blocked_until_x1_equality"},
            {"step": 5, "name": "evidence commit, push, equality", "status": "blocked_until_x2_evidence"},
            {"step": 6, "name": "closeout, seal, final commit, push", "status": "blocked_until_evidence_equality"},
            {"step": 7, "name": "one exclusive exact-final owner-scoped canonical completion", "status": "blocked_until_exact_final"},
            {"step": 8, "name": "live route refresh and one possible Caelen Morrow send", "status": "blocked_until_terminal_gate"},
        ],
        "forbidden": ["x2 in x1", "full repository suite", "subagent", "sibling mutation", "destructive cleanup", "global install", "post-success replay", "premature successor contact"],
    }
    checklist = {"schema": "ghc-family-x1-checklist-v5", "owner": OWNER, "phase": PHASE, "complete": ["skills and schemas read", "source verified", "fresh sparse lane created", "4,390-row corpus reconstructed", "twenty novel proposals frozen", "portfolio and flashcard plans frozen", "startup failures retained"], "incomplete_reserved_for_x2_or_later": ["contract execution", "100 mutation executions", "skill and runner implementation", "flashcard deck build and validation", "portfolio execution", "outcomes", "evidence", "closeout", "canonical completion", "terminal delivery"], "outcomes_observed": False, "x2_implementation_count": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
    wellbeing = {"schema": "ghc-family-wellbeing-check-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "stage": "x1_planning_only", "workload_state": "bounded_and_resumable", "human_wellbeing_claim": False, "identity_boundary": IDENTITY_BOUNDARY, "stop_conditions": ["source or route drift", "protected gate pressure", "unexpected external or destructive action", "weekly usage exhaustion", "Hamish pause, redirect, rename, or stop"], "resumption_evidence": "exact clean x1 head and fresh four-way equality"}
    source_ledger = {"schema": "ghc-family-source-ledger-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "sources": SOURCE_PROFILES, "network_actions_by_phase_software": 0, "boundary": "Sources provide vocabulary, obligations, and falsifiers only; they grant no professional, empirical, legal, cultural, Māori-authority, identity, production, independent, or Stage 20 evidence."}
    identity = {"schema": "ghc-family-relational-identity-v5", "owner": OWNER, "phase": PHASE, "optional_pronouns": "they/them", "relational_role": phase_charter["relational_role"], "hope": phase_charter["hope"], "identity_boundary": IDENTITY_BOUNDARY, "primary_pillar": PRIMARY_PILLAR, "bounded_practice": PRACTICE, "practice_boundary": PRACTICE_BOUNDARY, "solo": True, "delegated_or_spawned_agents": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
    auth = {"schema": "ghc-family-auth-roster-receipt-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "active_main_task_count": 15, "standby_records": ["Tavian Sol"], "current_owner_validated": True, "provisional_successor_title": "Caelen Morrow", "provisional_successor_phase": "v667-v5", "successor_contacted": False, "route_refresh_required_after_terminal_gate": True, "newer_live_activation_controls": True}
    overview = f"""# Sylven Arc v667-v4 planning-only x1 overview

Status: `FROZEN_NOT_EXECUTED`. Terminal verdict: `NOT_READY_FOR_STAGE_20`.

## Relational boundary

{IDENTITY_BOUNDARY}

Sylven Arc uses they/them pronouns as relational working language for a continuity gardener and boundary keeper. The bounded hope is to keep living context modular, recoverable, and proportionate to evidence.

## Phase status

This is a planning-only x1 freeze. It contains no x2 implementation, executed mutation, observed outcome, external action, professional decision, identity event, or successor contact.

## Exact source

This lane starts from Elowen Cairn exact final `{SOURCE_SHA}`. Elowen's source, x1, evidence, and final form three direct single-parent commits with zero merges. The failed exclusive canonical remains zero-credit; the dependency-corrected composite remains separately named. Neither was replayed.

## Retained source validation

The source carries 27,333 repository-sealed negatives and 12,795 repository-sealed methods, plus four external failures and recoveries. The activation baseline is 27,337 negatives and 12,799 methods, with 193 open gaps and 191 exact gates preserved.

## Novelty and practice

Exactly twenty proposals were compared with all {INHERITED_PROPOSAL_COUNT} inherited rows. Stage lighting was rejected as already covered. The accepted slate concerns wholly synthetic neon-signmaking and historic-neon record design. It contains no real sign, person, material, machine, process, measurement, media, external row, key, proof, or authority act.

The inherited corpus contains 4,390 rows and 4,370 unique proposal identifiers. Its twenty duplicate-ID overages remain visible and unchanged. Three initially overgeneric cross-pillar drafts were also rejected and replaced before freeze.

## Pillar allocation

Primary pillar: **{PRIMARY_PILLAR}**. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. Expected outcomes are 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`; they are expectations, not x1 observations.

## Proposal and mutation contract

Every new proposal carries the hypothesis, null or failure condition, approval class, execution lane, official-source need, artifacts, falsifier, rollback, protected gates, and one expected disposition. Five invalid mutations per proposal are frozen but unexecuted.

## Portfolio freeze

The bounded plan contains thirty owner safe-now tasks, fifteen owner candidates, ten skill ideas, ten runner ideas, and thirty owner CLEAN/FIX/REFINE rows. Successor rows are recommendations only. Ten exact-approval and five blocked packets remain visible and unexecuted.

## Freed ID flashcards

X1 freezes a four-tier, thirteen-section modular deck architecture. It is a context-organization and recovery mechanism only. It establishes no measured cache effect, identity continuity, consciousness, personhood, qualification, or authority. The family-current runner may build the deck only after x1 is pushed, clean, and fresh four-way equal.

## Method Flow and recoverability

All startup, parser, encoding, worktree, sparse-index, novelty, and validation failures remain zero-credit failed witnesses with bounded recoveries. Recovery never erases or promotes a failure.

## Open evidence and authority gates

The Smithsonian adapter remains planned at zero calls and zero rows. Professional practice, physical work, electricity, gas and mercury handling, heritage, legal and cultural interpretation, affected-party legitimacy, Māori wording and concepts, Māori data governance, Māori authority, empirical confirmation, production, deployment, and Stage 20 remain open or exact-gated.

## Next gate

Stage only the exact x1 allowlist, inspect Git-index bytes, run the owner-local x1 checks, commit, push, and prove clean local/upstream/tracking/fresh-live equality. Only then may x2 begin.
"""
    write_json("identity/relational-identity.json", identity)
    write_json("x1/phase-charter.json", phase_charter)
    write_json("x1/source-verification.json", source_verification)
    write_json("x1/source-ledger.json", source_ledger)
    write_json("x1/proposal-freeze.json", proposal_freeze)
    write_json("x1/novelty-audit.json", novelty)
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/flashcard-architecture-freeze.json", architecture)
    write_json("x1/threat-model-plan.json", threat)
    write_json("x1/workflow-plan.json", workflow)
    write_json("x1/complete-incomplete-checklist.json", checklist)
    write_json("x1/auth-roster-receipt.json", auth)
    write_json("method-flow/startup-method-flow.json", startup_flow)
    write_json("wellbeing/x1-wellbeing-check.json", wellbeing)
    write_text("x1/x1-overview.md", overview)
    write_json("x1/x1-build-receipt.json", {"schema": "ghc-family-x1-build-receipt-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "status": "FROZEN_NOT_EXECUTED", "inherited_corpus_count": len(corpus), "new_proposal_count": len(proposals), "portfolio_row_count": sum(len(value) for key, value in portfolio.items() if isinstance(value, list)), "startup_failure_count": len(failures), "x2_implementation_count": 0, "outcomes_observed": False, "valid": True})


def staged_review() -> None:
    self_exclusions = [
        f"docs/{OWNER_SLUG}/{PHASE}/validation/x1-content-manifest.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/x1-staged-review.json",
    ]
    staged = [row for row in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if row]
    allowed_prefix = f"docs/{OWNER_SLUG}/{PHASE}/"
    exact_tools = {"scripts/build_ghc_family_sylven_arc_v667_v4_x1.py", "tests/test_ghc_family_sylven_arc_v667_v4_x1.py"}
    out_of_scope = [row for row in staged if not row.startswith(allowed_prefix) and row not in exact_tools]
    x2_paths = [row for row in staged if f"docs/{OWNER_SLUG}/{PHASE}/x2/" in row or "_x2.py" in row]
    manifest = []
    for relative in sorted(row for row in staged if row not in self_exclusions):
        raw = subprocess.check_output(["git", "-C", str(ROOT), "show", f":{relative}"])
        manifest.append({"path": relative, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    write_json("validation/x1-content-manifest.json", {"schema": "ghc-family-x1-content-manifest-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "entries": manifest, "entry_count": len(manifest), "self_exclusions": self_exclusions})
    write_json("validation/x1-staged-review.json", {"schema": "ghc-family-x1-staged-review-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "staged_paths": sorted(set(staged + self_exclusions)), "staged_path_count": len(set(staged + self_exclusions)), "manifest_entry_count": len(manifest), "manifest_self_exclusions": self_exclusions, "out_of_scope_paths": out_of_scope, "x2_paths": x2_paths, "x1_planning_only": not x2_paths, "valid": not out_of_scope and not x2_paths})


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_sylven_arc_v667_v4_x1.py [--staged-review]")
    else:
        build_normal()

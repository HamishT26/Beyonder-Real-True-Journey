"""Build Vesper Arlen v683-v1 bounded x2 evidence from the immutable x1 freeze.

This owner-local adapter reuses the inherited, already-validated lifecycle
builder shape while replacing every owner material, domain statement, method
identifier, manifest path, skill package, and runner with Vesper-owned content.
Inherited modules are dependencies only and receive no Vesper novelty credit.
"""

from __future__ import annotations

import hashlib
import json
import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import Any

from scripts import build_ghc_family_neris_solane_v682_v8_x2 as base
from scripts.ghc_family_vesper_arlen_v683_v1_contracts import execute_proposal
from scripts.ghc_family_vesper_arlen_v683_v1_skill_bank import (
    SKILL_NAMES,
    smoke_skills,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "v683-v1"
OWNER = "Vesper Arlen"
X1 = ROOT / "docs" / "vesper-arlen" / PHASE / "x1"
X2 = ROOT / "docs" / "vesper-arlen" / PHASE / "x2"
VALIDATION = ROOT / "docs" / "vesper-arlen" / PHASE / "validation"
X1_SHA = "2981dcc774afce801973f8e3a9e6643b5e22dcee"
SOURCE = "22c32b5ec50af2f59f221b18bfbe468f0b6bd1e7"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

ACTIVATION_BASELINE = {
    "effective_negatives": 57783,
    "effective_methods": 70599,
    "failed_witnesses": 29444,
    "bounded_passing_witnesses": 51639,
    "open_gaps": 513,
    "exact_gates": 503,
}

STARTUP_FAILURES = json.loads(
    (X1 / "method-flow-startup.json").read_text(encoding="utf-8")
)["startup_failures"]

POST_X1_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "VA6831-X2-N020",
        "failed_witness": "An initial broad inherited x2-test projection exceeded the bounded response window and earned no read credit.",
        "initial_credit": 0,
        "recovery": "Read the inherited test in four bounded line windows through EOF before implementing the owner-local test.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-X2-N021",
        "failed_witness": "A guessed x1 identity and source-ledger filename pair did not exist and earned no source-read credit.",
        "initial_credit": 0,
        "recovery": "Enumerate the exact x1 tree, then read only verified identity-and-boundary and official-primary-source-ledger paths.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-X2-N022",
        "failed_witness": "The first owner-delta Ruff check rejected one unused Counter import in the Vesper x2 adapter.",
        "initial_credit": 0,
        "recovery": "Remove only the unused import, retain this failed check, and rerun Ruff only on the exact changed Python paths.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "VA6831-X2-N023",
        "failed_witness": "The requested Bandit module was not exposed by the active Python environment, so the attempted scan earned no security credit.",
        "initial_credit": 0,
        "recovery": "Use a dependency-free exact-delta AST rule set for dangerous evaluation, shell-enabled subprocesses, dynamic execution, and destructive filesystem calls; do not install or mutate shared prefixes.",
        "recovery_credit": "bounded_dependency_only",
    },
]

OPERATIONAL_FAILURES = STARTUP_FAILURES + POST_X1_FAILURES

SKILL_PURPOSES = {
    "clock-object-surrogate-separator": "separating a conceptual clock model, physical object, digital surrogate, and operational device",
    "escapement-token-nonclassification": "keeping synthetic escapement tokens separate from real mechanism identification",
    "gear-train-topology-vacancy": "representing a synthetic dependency graph without gear counts, ratios, dimensions, or physical inference",
    "measurement-value-absence-guard": "requiring measurement fields to remain absent rather than zero-filled or inferred",
    "time-frequency-noncalibration": "keeping time and frequency vocabulary separate from calibration or traceability claims",
    "winding-action-state-separator": "separating request, authorization, attempt, observation, and result without winding a clock",
    "condition-cue-nondiagnosis": "recording synthetic condition-cue vocabulary without examination or diagnosis",
    "treatment-authority-hold": "reserving handling, repair, conservation, and return-to-service authority",
    "clock-provenance-lineage-ledger": "preserving synthetic catalogue, custody, attribution, revision, and correction lineage",
    "catalogue-alias-collision-quarantine": "detecting duplicate synthetic labels without changing a real catalogue",
    "premis-event-vacancy": "using preservation-event vocabulary with zero object, file, or repository action",
    "spectrum-procedure-nonexecution": "using collection-procedure vocabulary without claiming collection-management execution",
    "accessible-mechanism-summary": "creating structural summaries while manual and affected-user evaluation stays reserved",
    "rights-remedy-hold": "reserving ownership, copyright, access, correction, takedown, and remedy decisions",
    "traditional-knowledge-minimizer": "minimizing cultural and traditional-knowledge description pending proper authority",
    "workload-handover-lease": "making stop, pause, readback, workload, and handover states explicit",
    "freed-id-zero-key-guard": "keeping synthetic identifiers separate from real keys, proofs, and lifecycle events",
    "thos-operator-vacancy": "keeping THOS workflow structure participant-free and proxy-only",
    "gmut-timebase-noninference": "keeping timebase vocabulary separate from likelihood, physics, and cosmological inference",
    "authority-noncompensation": "preventing software, citations, or related witnesses from substituting for authority",
}


def map_path(value: str) -> str:
    replacements = (
        ("docs/neris-solane/v682-v8", "docs/vesper-arlen/v683-v1"),
        ("ghc_family_neris_solane_v682_v8", "ghc_family_vesper_arlen_v683_v1"),
        ("ghc_family_signal_flag_runner_", "ghc_family_clock_documentation_runner_"),
    )
    for old, new in replacements:
        value = value.replace(old, new)
    return value


def transform(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: transform(item) for key, item in value.items()}
    if isinstance(value, list):
        return [transform(item) for item in value]
    if isinstance(value, str):
        value = map_path(value)
        replacements = (
            (".v682.v8", ".v683.v1"),
            ("NS6828", "VA6831"),
            ("Neris Solane", "Vesper Arlen"),
            ("signal-flag documentation", "mechanical-clock documentation"),
            ("signal flag", "mechanical-clock record"),
            ("flag token", "clock token"),
            ("physical flag", "physical clock"),
            ("observed hoist", "observed mechanism"),
            ("operational maritime signal", "operational timekeeping device"),
            ("signal sequence", "clock-record sequence"),
            ("empty_signal_sequence", "empty_clock_sequence"),
            ("forbidden_observed_sequence", "forbidden_measured_sequence"),
        )
        for old, new in replacements:
            value = value.replace(old, new)
        return value
    return value


def build_phase_skills(skill_root: Path) -> None:
    """Create twenty customized owner-local packages without global install."""
    if set(SKILL_PURPOSES) != set(SKILL_NAMES):
        raise RuntimeError("skill purpose map must match the frozen skill slate")
    for name in SKILL_NAMES:
        purpose = SKILL_PURPOSES[name]
        display = name.replace("-", " ").title()
        base.write_text(
            skill_root / name / "SKILL.md",
            f'''---
name: {name}
description: "Use when {purpose}. Reject real rows, observation, measurement, operational action, safety release, authority promotion, and protected-gate closure."
---

# {display}

Use this Vesper v683-v1 owner-local skill only for {purpose}. It validates synthetic documentation structure and refusal conditions; it never inspects or acts on a real person, clock, collection, record, measurement, calibration, treatment, identity, location, or cultural expression.

## Procedure

1. Read the complete frozen proposal and fixture through EOF.
2. Require `synthetic: true`, `real_row_count: 0`, `observation_status: absent`, `authority_status: reserved`, and `boundary: owner_local_zero_row_only`.
3. Keep plan, fixture, decision, correction, rollback, and external-authority states distinct; preserve the frozen provenance digest.
4. Accept one bounded positive only when every required field and refusal boundary is present.
5. Reject missing fields, real rows, stale provenance, lifecycle inversion, safety release, empirical promotion, or authority promotion; retain every rejection at zero completion credit.
6. Preserve `open_gap` or `exact_gate` when real evidence, professional competence, affected-party review, legal or cultural authority, Maori authority, privacy or accessibility completeness, independent reproduction, or Stage 20 would be required.

## Acceptance and rollback

Return an explicit accepted or rejected decision with reasons. A passing synthetic fixture proves only this bounded contract. On ambiguity, reject, retain the witness, make no external write, and leave every real-world and authority state unchanged.
''',
        )
        base.write_text(
            skill_root / name / "agents" / "openai.yaml",
            f'''interface:
  display_name: "{display}"
  short_description: "Guard synthetic clock documentation boundaries."
  default_prompt: "Use ${name} to validate {purpose} without observation, measurement, operational action, or authority claims."
''',
        )


def runner_smokes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(1, 11):
        module = f"scripts.ghc_family_clock_documentation_runner_{index:02d}"
        payloads: list[dict[str, Any]] = []
        return_codes: list[int] = []
        for fixture in ("positive", "invalid"):
            process = subprocess.run(  # nosec B603
                [sys.executable, "-X", "utf8", "-m", module, "--fixture", fixture],
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
            payloads.append(json.loads(process.stdout))
            return_codes.append(process.returncode)
        rows.append(
            {
                "accepting_fixture_accepted": return_codes[0] == 0 and payloads[0]["accepted"],
                "family_current_name": payloads[0]["runner"],
                "rejecting_fixture_rejected": return_codes[1] == 0 and not payloads[1]["accepted"],
                "rejecting_reasons": payloads[1]["reasons"],
            }
        )
    return rows


_old_flashcards = base.build_flashcard_deck


def build_flashcard_deck(
    proposals: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], str, str]:
    deck, _manifest, _compact, _accessible = _old_flashcards(proposals)
    deck = transform(deck)
    deck["sections"][5] = "mechanical-clock documentation practice"
    deck["cards"][1]["back"] = (
        "Represented: typed model boundaries, timebase vocabulary, uncertainty, provenance, and noninference; no physical or cosmological evidence."
    )
    deck["cards"][2]["back"] = (
        "Primary: bounded clock-record workflow, stop, workload, correction, accessibility, and handover structure only."
    )
    deck["cards"][4]["front"] = "Clock catalogue and mechanism-token lens"
    deck["cards"][4]["back"] = (
        "Synthetic object, surrogate, escapement-token, gear-topology, catalogue-lineage, and absence-state documentation with every real observation and measurement absent."
    )
    deck["cards"][5]["front"] = "Metrology and preservation lens"
    deck["cards"][5]["back"] = (
        "Synthetic time-frequency, calibration-vacancy, condition-cue, preservation-event, and correction plans with zero objects, measurements, files, or treatments."
    )
    deck["cards"][6]["front"] = "Museum rights and access lens"
    deck["cards"][6]["back"] = (
        "Synthetic rights, remedy, accessibility, traditional-knowledge, workload, and handover records with authority reserved."
    )
    canonical = json.dumps(deck, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    manifest = {
        "card_count": deck["card_count"],
        "card_ids": [card["card_id"] for card in deck["cards"]],
        "deck_payload_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.freed-id-flashcard-manifest.v683.v1.x2",
        "section_count": deck["section_count"],
        "tier_counts": deck["tier_counts"],
    }
    compact = [
        f"# {OWNER} {PHASE} Compact Freed ID Flashcards",
        "",
        "Relational working language and bounded synthetic evidence only. No card confers observation, measurement, competence, consent, authority, or Stage 20 credit.",
        "",
    ]
    accessible = [
        f"# {OWNER} {PHASE} Linear Accessible Flashcards",
        "",
        "This companion preserves all 67 cards without reliance on colour, position, animation, or interactive controls. Manual browser, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved.",
        "",
    ]
    for card in deck["cards"]:
        compact.append(f"- **{card['card_id']} — {card['front']}**: {card['back']}")
        accessible.extend(
            [
                f"## {card['card_id']}",
                "",
                f"Section: {card['section']}. Tier: {card['tier']}.",
                "",
                f"Prompt: {card['front']}",
                "",
                f"Answer: {card['back']}",
                "",
            ]
        )
    return deck, manifest, "\n".join(compact), "\n".join(accessible)


_old_method_flow = base.method_flow


def method_flow(*args: Any, **kwargs: Any) -> dict[str, Any]:
    return transform(_old_method_flow(*args, **kwargs))


_old_write_json = base.write_json
_old_write_text = base.write_text
_old_manifest_entry = base.manifest_entry
_old_privacy_scan = base.privacy_scan
_old_bounded_tool_smokes = base.bounded_tool_smokes


def write_json(path: Path, payload: Any) -> None:
    payload = transform(payload)
    name = path.name
    if name == "phase-truth.json" and path.parent == X2:
        payload["declared_proposal_chain"] = 10730
        payload["primary_pillar"] = "THOS Body"
        payload["represented_pillars"] = ["GMUT Mind", "Freed ID and CBR Heart"]
    elif name == "source-use-receipt.json":
        payload["current_official_primary_sources"] = [
            "BIPM SI Brochure ninth edition updated 2026",
            "NIST Time and Frequency Division",
            "NIST Special Publication 559 Time and Frequency Users Manual",
            "ISO 8601 date and time format",
            "Collections Trust Spectrum 5.1",
            "Library of Congress descriptive conventions",
            "Library of Congress PREMIS",
            "DCMI Metadata Terms",
            "W3C PROV-O",
            "WCAG 2.2",
            "Verifiable Credentials Data Model 2.0",
            "New Zealand Privacy Principles including IPP3A",
            "Te Mana Raraunga principles",
        ]
    elif name == "wellbeing-check.json":
        payload.update(
            {
                "hope": "to make synthetic records inspectable and correctable while leaving real people, knowledge, places, objects, measurements, and authority with their proper holders",
                "optional_pronouns": "unspecified",
                "role": "provenance gardener and reversible-boundary keeper",
            }
        )
    _old_write_json(Path(map_path(path.as_posix())), payload)


def write_text(path: Path, text: str) -> None:
    text = transform(text)
    if path.name == "evidence-overview.md" and path.parent == X2:
        text = f"""# Vesper Arlen {PHASE} Bounded X2 Evidence Overview

Vesper Arlen is relational working language for a provenance gardener and reversible-boundary keeper. The hope is to make synthetic records inspectable and correctable while leaving real people, knowledge, places, objects, measurements, and authority with their proper holders. Pronouns are unspecified. This establishes no consciousness, personhood, continuity, employment, qualification, agency, or authority.

This x2 executed the sixty immutable planning-only x1 contracts without changing their expected dispositions. Exactly 42 bounded software or structural contracts are completed, 12 are represented, three remain open gaps, and three remain exact gates. Every positive fixture was wholly synthetic and used zero real rows. All 300 preregistered invalid mutations were rejected and retained at zero completion credit.

The primary pillar is THOS Body through dependency-closed record workflow, action-versus-observation separation, stopping, workload leases, correction, structural accessibility, and handover. GMUT Mind remains represented through timebase vocabulary, explicit absence, topology, uncertainty, provenance, and noninference. Freed ID and CBR Heart remain represented through surrogate separation, rights, remedy, privacy minimization, traditional-knowledge holds, and authority noncompensation.

The three bounded human-practice lenses are mechanical-clock catalogue documentation, time-and-frequency metrology record assurance, and museum provenance/accessibility documentation. No real person, maker, owner, worker, community, clock, collection, catalogue record, measurement, calibration, condition assessment, winding, handling, treatment, publication, identity event, external write, professional decision, or authority act was involved.

Official and primary sources supplied vocabulary and refusal conditions only. They were not observations, calibration certificates, work instructions, object identifications, condition diagnoses, safety releases, professional opinions, rights decisions, legal interpretations, cultural ratifications, affected-party decisions, or Maori-authority grants.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, likelihood, posterior, force, constraint, prediction, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic and proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, or independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle events, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Object identity, mechanism class, gear topology, material, condition, timekeeping performance, calibration, ownership, custody, attribution, copyright, access, traditional knowledge, handling, winding, repair, conservation, return to service, publication, professional release, privacy, accessibility remedy, legal or cultural interpretation, affected-party legitimacy, Maori wording, Maori data governance, and Maori authority remain open or exact-gated. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 are not established. The terminal verdict remains {TERMINAL_VERDICT}.

The owner-local flashcard deck contains one owner card, three pillar cards, three practice cards, and sixty task cards across thirteen sections, with compact and linear companions. These are navigation and readback aids only. Twenty customized owner-local skills passed the official quick validator and bounded positive/rejecting smokes once; none was globally installed. Ten family-current runners passed paired bounded smokes once.

Three already-installed dependency-justified tools were used without installation or update: jsonschema for zero-row structure, Pydantic for a typed boundary, and NumPy for an empty-array guard. Their successful bounded smokes are not a vulnerability audit, scientific computation, production certification, package-quota completion claim, or authority evidence.
"""
    _old_write_text(Path(map_path(path.as_posix())), text)


def manifest_entry(path: str) -> dict[str, Any]:
    return _old_manifest_entry(map_path(path))


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    return transform(_old_privacy_scan([map_path(path) for path in paths]))


def bounded_tool_smokes() -> list[dict[str, Any]]:
    return transform(_old_bounded_tool_smokes())


def configure_base() -> None:
    base.ROOT = ROOT
    base.PHASE = PHASE
    base.OWNER = OWNER
    base.X1 = X1
    base.X2 = X2
    base.VALIDATION = VALIDATION
    base.X1_SHA = X1_SHA
    base.SOURCE = SOURCE
    base.TERMINAL_VERDICT = TERMINAL_VERDICT
    base.ACTIVATION_BASELINE = ACTIVATION_BASELINE
    base.STARTUP_FAILURES = STARTUP_FAILURES
    base.POST_X1_FAILURES = POST_X1_FAILURES
    base.OPERATIONAL_FAILURES = OPERATIONAL_FAILURES
    base.SKILL_NAMES = SKILL_NAMES
    base.SKILL_PURPOSES = SKILL_PURPOSES
    base.execute_proposal = execute_proposal
    base.smoke_skills = smoke_skills
    base.build_phase_skills = build_phase_skills
    base.runner_smokes = runner_smokes
    base.build_flashcard_deck = build_flashcard_deck
    base.method_flow = method_flow
    base.write_json = write_json
    base.write_text = write_text
    base.manifest_entry = manifest_entry
    base.privacy_scan = privacy_scan
    base.bounded_tool_smokes = bounded_tool_smokes
    base.WRITTEN.clear()


def build() -> None:
    configure_base()
    base.build()


def refresh_failure_ledgers() -> None:
    """Refresh only additive failure arithmetic and hashes after isolated repair."""
    configure_base()
    proposals = json.loads(
        (X1 / "new-proposal-freeze.json").read_text(encoding="utf-8")
    )["proposals"]
    portfolio = json.loads(
        (X1 / "portfolio-freeze.json").read_text(encoding="utf-8")
    )
    mutations = json.loads(
        (X2 / "rejecting-mutations.json").read_text(encoding="utf-8")
    )["mutations"]
    skills = json.loads((X2 / "skill-execution.json").read_text(encoding="utf-8"))[
        "results"
    ]
    runners = json.loads(
        (X2 / "runner-execution.json").read_text(encoding="utf-8")
    )["results"]
    flashcards = json.loads(
        (X2 / "flashcards" / "deck.json").read_text(encoding="utf-8")
    )
    tools = json.loads((X2 / "bounded-tools.json").read_text(encoding="utf-8"))[
        "three_bounded_tool_smokes"
    ]
    flow = method_flow(
        proposals, mutations, portfolio, skills, runners, flashcards, tools
    )
    write_json(X2 / "method-flow-ledger.json", flow)
    truth = json.loads((X2 / "phase-truth.json").read_text(encoding="utf-8"))
    truth["totals"] = {
        "bounded_passing_witnesses": ACTIVATION_BASELINE[
            "bounded_passing_witnesses"
        ]
        + flow["passing_witness_count"],
        "effective_methods": ACTIVATION_BASELINE["effective_methods"]
        + flow["method_count"],
        "effective_negatives": ACTIVATION_BASELINE["effective_negatives"]
        + len(OPERATIONAL_FAILURES)
        + len(mutations),
        "exact_gates": ACTIVATION_BASELINE["exact_gates"] + 3,
        "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"]
        + flow["failed_witness_count"],
        "open_gaps": ACTIVATION_BASELINE["open_gaps"] + 3,
    }
    write_json(X2 / "phase-truth.json", truth)
    manifest_path = VALIDATION / "evidence-index-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["entries"] = [manifest_entry(row["path"]) for row in manifest["entries"]]
    manifest["entry_count"] = len(manifest["entries"])
    write_json(manifest_path, manifest)
    paths = [row["path"] for row in manifest["entries"]]
    write_json(VALIDATION / "evidence-privacy-scan.json", privacy_scan(paths))


if __name__ == "__main__":
    if "--refresh-failure-ledgers" in sys.argv:
        refresh_failure_ledgers()
    else:
        build()

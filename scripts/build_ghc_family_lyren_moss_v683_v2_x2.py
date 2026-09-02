"""Build Lyren Moss v683-v2 bounded x2 evidence from immutable x1.

The adapter reuses the inherited validated lifecycle shape while replacing the
owner material, domain contracts, methods, paths, skills, and runners with
Lyren-owned content. Inherited modules are dependencies and receive no Lyren
novelty or completion credit.
"""

from __future__ import annotations

import hashlib
import json
import subprocess  # nosec B404
import sys
from pathlib import Path
from typing import Any

from scripts import build_ghc_family_neris_solane_v682_v8_x2 as base
from scripts.ghc_family_lyren_moss_v683_v2_contracts import execute_proposal
from scripts.ghc_family_lyren_moss_v683_v2_skill_bank import SKILL_NAMES, smoke_skills


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v683-v2"
OWNER = "Lyren Moss"
X1 = ROOT / "docs" / "lyren-moss" / PHASE / "x1"
X2 = ROOT / "docs" / "lyren-moss" / PHASE / "x2"
VALIDATION = ROOT / "docs" / "lyren-moss" / PHASE / "validation"
X1_SHA = "57dcd8a0e6e5a43f87d6f1a5a0d79d2d68b66d8b"
SOURCE = "484d44fb8875bf8129143c99e5340d2e2044fbd2"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"


ACTIVATION_BASELINE = {
    "effective_negatives": 58114,
    "effective_methods": 71385,
    "failed_witnesses": 29775,
    "bounded_passing_witnesses": 52364,
    "open_gaps": 516,
    "exact_gates": 506,
}

STARTUP_FAILURES = json.loads(
    (X1 / "method-flow-startup.json").read_text(encoding="utf-8")
)["startup_failures"]

POST_X1_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "LM6832-X2-N015",
        "failed_witness": "The first post-push four-way equality wrapper failed at PowerShell parse time while capturing semicolon-delimited Git predicates.",
        "initial_credit": 0,
        "recovery": "Run local upstream tracking fresh-live divergence cached-diff and worktree-diff as separate scalar predicates without repushing x1.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-X2-N016",
        "failed_witness": "The first x2 builder invocation used direct script execution and failed before generation because the repository-root scripts package was not on the import path.",
        "initial_credit": 0,
        "recovery": "Invoke the unchanged builder through its repository-root Python module entrypoint without changing the shared environment.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-X2-N017",
        "failed_witness": "The module entrypoint stopped before generation because the inherited engine imports one exact Neris startup ledger that was absent from the initial sparse dependency set.",
        "initial_credit": 0,
        "recovery": "Materialize only that immutable source blob inside the Lyren worktree and leave the Neris branch and content untouched.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-X2-N018",
        "failed_witness": "The first exact sparse-add recovery used an init-only no-cone option that this Git version rejects on the add subcommand.",
        "initial_credit": 0,
        "recovery": "Keep the existing non-cone configuration and add only the same literal dependency path with the supported subcommand form.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "LM6832-X2-N019",
        "failed_witness": "The inherited engine generated provisional x2 content but stopped before evidence-manifest creation because its pre-manifest existence check requires eleven exact Neris runner and test dependency blobs.",
        "initial_credit": 0,
        "recovery": "Treat the provisional output as nonterminal, materialize only the eleven immutable source dependencies in the Lyren sparse lane, and rerun the builder with Lyren path mapping unchanged.",
        "recovery_credit": "bounded_dependency_only",
    },
]

OPERATIONAL_FAILURES = STARTUP_FAILURES + POST_X1_FAILURES


SKILL_PURPOSES = {
    "sound-carrier-object-surrogate-separator": "separating conceptual sound content, a physical carrier, a digital surrogate, and a playback device",
    "groove-token-nonmeasurement": "keeping groove geometry vocabulary separate from inspection or measurement",
    "playback-action-state-separator": "separating playback request, authorization, attempt, observation, and result without playback",
    "audio-signal-vacancy-guard": "requiring signal, timebase, level, and channel fields to remain absent rather than inferred",
    "carrier-condition-nondiagnosis": "recording synthetic condition-cue vocabulary without examination or diagnosis",
    "treatment-authority-hold": "reserving handling, cleaning, treatment, conservation, and safety authority",
    "digitization-nonexecution": "keeping digitization and file vocabulary separate from signal capture or conversion",
    "sound-provenance-lineage-ledger": "preserving synthetic carrier, recording, surrogate, revision, and correction lineage",
    "carrier-alias-collision-quarantine": "detecting duplicate synthetic carrier labels without changing a real catalogue",
    "premis-audio-event-vacancy": "using preservation-event vocabulary with zero carrier, file, or repository action",
    "marc007-noncataloguing-map": "mapping sound-recording category vocabulary without creating a catalogue record",
    "iasa-procedure-nonexecution": "using audio-preservation vocabulary without executing handling, transfer, or storage procedures",
    "accessible-transcript-vacancy": "reserving transcript, caption, translation, and affected-user evaluation states",
    "audio-rights-remedy-hold": "reserving copyright, donor restriction, access, correction, takedown, and remedy decisions",
    "traditional-knowledge-minimizer": "minimizing cultural and traditional-knowledge description pending proper authority",
    "sound-workload-handover-lease": "making stop, pause, readback, workload, and handover states explicit",
    "freed-id-zero-key-audio-guard": "keeping synthetic sound identifiers separate from real keys, proofs, and lifecycle events",
    "thos-playback-operator-vacancy": "keeping THOS workflow structure listener-free, operator-free, and proxy-only",
    "gmut-audio-timebase-noninference": "keeping audio timebase vocabulary separate from likelihood, physics, and cosmological inference",
    "sound-authority-noncompensation": "preventing software, standards, or citations from substituting for authority",
}


def map_path(value: str) -> str:
    replacements = (
        ("docs/neris-solane/v682-v8", "docs/lyren-moss/v683-v2"),
        ("ghc_family_neris_solane_v682_v8", "ghc_family_lyren_moss_v683_v2"),
        ("ghc_family_signal_flag_runner_", "ghc_family_sound_carrier_documentation_runner_"),
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
            (".v682.v8", ".v683.v2"),
            ("NS6828", "LM6832"),
            ("Neris Solane", "Lyren Moss"),
            ("signal-flag documentation", "sound-carrier documentation"),
            ("signal flag", "sound-carrier record"),
            ("flag token", "sound-carrier token"),
            ("physical flag", "physical sound carrier"),
            ("observed hoist", "observed playback"),
            ("operational maritime signal", "operational playback or digitization"),
            ("signal sequence", "sound-record sequence"),
            ("empty_signal_sequence", "empty_audio_sequence"),
            ("forbidden_observed_sequence", "forbidden_captured_sequence"),
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
description: "Use when {purpose}. Reject real rows, observation, listening, measurement, operational action, safety release, authority promotion, and protected-gate closure."
---

# {display}

Use this Lyren v683-v2 owner-local skill only for {purpose}. It validates synthetic documentation structure and refusal conditions; it never inspects or acts on a real person, community, sound carrier, recording, collection, file, identifier, location, measurement, playback, digitization, treatment, or cultural expression.

## Procedure

1. Read the complete frozen proposal and fixture through EOF.
2. Require `synthetic: true`, `real_row_count: 0`, `observation_status: absent`, `authority_status: reserved`, and `boundary: owner_local_zero_row_only`.
3. Keep plan, fixture, decision, correction, rollback, and external-authority states distinct; preserve the frozen provenance digest.
4. Accept one bounded positive only when every required field and refusal boundary is present.
5. Reject missing fields, real rows, stale provenance, lifecycle inversion, safety release, empirical promotion, listening, playback, digitization, treatment, or authority promotion; retain every rejection at zero completion credit.
6. Preserve `open_gap` or `exact_gate` when real evidence, professional competence, affected-party review, legal or cultural authority, Maori authority, privacy or accessibility completeness, independent reproduction, or Stage 20 would be required.

## Acceptance and rollback

Return an explicit accepted or rejected decision with reasons. A passing synthetic fixture proves only this bounded contract. On ambiguity, reject, retain the witness, make no external write, and leave every real-world and authority state unchanged.
''',
        )
        base.write_text(
            skill_root / name / "agents" / "openai.yaml",
            f'''interface:
  display_name: "{display}"
  short_description: "Guard synthetic sound-carrier documentation boundaries."
  default_prompt: "Use ${name} to validate {purpose} without listening, observation, measurement, operational action, or authority claims."
''',
        )


def runner_smokes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(1, 11):
        module = f"scripts.ghc_family_sound_carrier_documentation_runner_{index:02d}"
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
    deck["sections"][5] = "sound-carrier documentation practice"
    deck["cards"][1]["back"] = (
        "Represented: typed carrier and signal topology, timebase vocabulary, explicit absence, uncertainty, provenance, and noninference; no physical or cosmological evidence."
    )
    deck["cards"][2]["back"] = (
        "Represented: bounded documentation workflow, action-state separation, stop, workload, correction, accessibility, and handover structure only."
    )
    deck["cards"][3]["back"] = (
        "Primary: synthetic surrogate separation, identity vacancy, provenance, rights, remedy, privacy, traditional-knowledge holds, and authority noncompensation."
    )
    deck["cards"][4]["front"] = "Sound-carrier description and nonplayback lens"
    deck["cards"][4]["back"] = (
        "Synthetic carrier, groove, container, catalogue, signal-vacancy, and absence-state documentation with every real object, listening event, and measurement absent."
    )
    deck["cards"][5]["front"] = "Preservation-event and digital-audio lineage lens"
    deck["cards"][5]["back"] = (
        "Synthetic request, extraction, file-role, metadata, fixity, correction, and refusal plans with zero carriers, recordings, files, playback, digitization, or treatments."
    )
    deck["cards"][6]["front"] = "Rights, accessibility, and cultural-governance lens"
    deck["cards"][6]["back"] = (
        "Synthetic access, transcript, remedy, traditional-knowledge, workload, and handover records with authority reserved."
    )
    canonical = json.dumps(deck, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    manifest = {
        "card_count": deck["card_count"],
        "card_ids": [card["card_id"] for card in deck["cards"]],
        "deck_payload_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.freed-id-flashcard-manifest.v683.v2.x2",
        "section_count": deck["section_count"],
        "tier_counts": deck["tier_counts"],
    }
    compact = [
        f"# {OWNER} {PHASE} Compact Freed ID Flashcards",
        "",
        "Relational working language and bounded synthetic evidence only. No card confers observation, listening, measurement, competence, consent, authority, or Stage 20 credit.",
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
        payload["declared_proposal_chain"] = 10790
        payload["primary_pillar"] = "Freed ID and CBR Heart"
        payload["represented_pillars"] = ["GMUT Mind", "THOS Body"]
    elif name == "source-use-receipt.json":
        payload["current_official_primary_sources"] = [
            "IASA TC-04 audio preservation guidelines",
            "IASA special and technical publications",
            "Library of Congress audiovisual care handling and storage",
            "Library of Congress Recommended Formats Statement for audio works",
            "National Archives audio guidance",
            "MARC 21 field 007 sound recording",
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
                "hope": "to make archival sound-carrier descriptions inspectable and correctable without turning vocabulary into playback, identification, rights, cultural, professional, or authority claims",
                "optional_pronouns": "unspecified",
                "role": "acoustic provenance cartographer and non-playback boundary keeper",
            }
        )
    _old_write_json(Path(map_path(path.as_posix())), payload)


def write_text(path: Path, text: str) -> None:
    text = transform(text)
    if path.name == "evidence-overview.md" and path.parent == X2:
        text = f"""# Lyren Moss {PHASE} Bounded X2 Evidence Overview

Lyren Moss is relational working language for an acoustic provenance cartographer and non-playback boundary keeper. The hope is to make archival sound-carrier descriptions inspectable and correctable without turning vocabulary into playback, identification, rights, cultural, professional, or authority claims. Pronouns are unspecified. This establishes no consciousness, personhood, continuity, employment, qualification, agency, or authority.

This x2 executed the sixty immutable planning-only x1 contracts without changing their expected dispositions. Exactly 42 bounded software or structural contracts are completed, 12 are represented, three remain open gaps, and three remain exact gates. Every positive fixture was wholly synthetic and used zero real rows. All 300 preregistered invalid mutations were rejected and retained at zero completion credit.

The primary pillar is Freed ID and CBR Heart through physical-carrier, conceptual-content, digital-surrogate, catalogue-record, and identity-state separation; provenance; rights and remedy holds; privacy minimization; traditional-knowledge minimization; and authority noncompensation. GMUT Mind remains represented through typed carrier and signal topology, missing measurements, timebase vocabulary, uncertainty, provenance, and noninference. THOS Body remains represented through dependency-closed workflow, action-state separation, stopping, workload leases, correction, structural accessibility, and handover.

The three bounded human-practice lenses are sound-carrier cataloguing and physical-description documentation, preservation-event and digital-audio lineage assurance, and rights, accessibility, traditional-knowledge, remedy, and handover documentation. No real person, community, carrier, recording, collection, catalogue record, file, signal, listening event, measurement, playback, digitization, handling, treatment, publication, identity event, external write, professional decision, or authority act was involved.

Official and primary sources supplied vocabulary and refusal conditions only. They were not observations, listening results, transfer instructions, object identifications, condition diagnoses, safety releases, format certifications, professional opinions, rights decisions, legal interpretations, cultural ratifications, affected-party decisions, or Maori-authority grants.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, likelihood, posterior, force, constraint, prediction, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic and proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, or independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle events, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Carrier identity, material, condition, recording identity or content, signal properties, playback, digitization, preservation format, ownership, custody, attribution, copyright, access, traditional knowledge, handling, cleaning, treatment, storage, publication, professional release, privacy, accessibility remedy, legal or cultural interpretation, affected-party legitimacy, Maori wording, Maori data governance, and Maori authority remain open or exact-gated. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 are not established. The terminal verdict remains {TERMINAL_VERDICT}.

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
    proposals = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))[
        "proposals"
    ]
    portfolio = json.loads((X1 / "portfolio-freeze.json").read_text(encoding="utf-8"))
    mutations = json.loads((X2 / "rejecting-mutations.json").read_text(encoding="utf-8"))[
        "mutations"
    ]
    skills = json.loads((X2 / "skill-execution.json").read_text(encoding="utf-8"))[
        "results"
    ]
    runners = json.loads((X2 / "runner-execution.json").read_text(encoding="utf-8"))[
        "results"
    ]
    flashcards = json.loads((X2 / "flashcards" / "deck.json").read_text(encoding="utf-8"))
    tools = json.loads((X2 / "bounded-tools.json").read_text(encoding="utf-8"))[
        "three_bounded_tool_smokes"
    ]
    flow = method_flow(proposals, mutations, portfolio, skills, runners, flashcards, tools)
    write_json(X2 / "method-flow-ledger.json", flow)
    truth = json.loads((X2 / "phase-truth.json").read_text(encoding="utf-8"))
    truth["totals"] = {
        "bounded_passing_witnesses": ACTIVATION_BASELINE["bounded_passing_witnesses"]
        + flow["passing_witness_count"],
        "effective_methods": ACTIVATION_BASELINE["effective_methods"] + flow["method_count"],
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
    if sys.argv[1:] == ["--refresh-failure-ledgers"]:
        refresh_failure_ledgers()
    elif sys.argv[1:]:
        raise SystemExit("unsupported arguments")
    else:
        build()

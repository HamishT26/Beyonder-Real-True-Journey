"""Build Ilyra Fen v683-v3 bounded x2 evidence from immutable x1.

The adapter reuses the inherited validated lifecycle shape while replacing the
owner material, domain contracts, methods, paths, skills, and runners with
Ilyra-owned content. Inherited modules are dependencies and receive no Ilyra
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
from scripts.ghc_family_ilyra_fen_v683_v3_contracts import execute_proposal
from scripts.ghc_family_ilyra_fen_v683_v3_skill_bank import SKILL_NAMES, smoke_skills


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v683-v3"
OWNER = "Ilyra Fen"
X1 = ROOT / "docs" / "ilyra-fen" / PHASE / "x1"
X2 = ROOT / "docs" / "ilyra-fen" / PHASE / "x2"
VALIDATION = ROOT / "docs" / "ilyra-fen" / PHASE / "validation"
X1_SHA = "2bbdaa6b0a6c038bf1233448202dc161f92037ce"
SOURCE = "0f5210fc4899a3c36e1ca1e5c1b5c897eb9acc68"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"


ACTIVATION_BASELINE = {
    "effective_negatives": 58438,
    "effective_methods": 72164,
    "failed_witnesses": 30099,
    "bounded_passing_witnesses": 53082,
    "open_gaps": 519,
    "exact_gates": 509,
}

STARTUP_FAILURES = json.loads(
    (X1 / "method-flow-startup.json").read_text(encoding="utf-8")
)["startup_failures"]

POST_X1_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "IF6833-X2-N012",
        "failed_witness": "The first x2 builder reached runner smokes but stopped because the ten newly named Ilyra runner wrapper modules did not yet exist; provisional files earned zero evidence credit.",
        "initial_credit": 0,
        "recovery": "Create only the ten bounded owner-local wrappers from the frozen runner bank and rerun the failed x2 dependency once.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-X2-N013",
        "failed_witness": "A diagnostic ripgrep command embedded a punctuation-heavy double-quoted pattern in PowerShell and failed at parser time.",
        "initial_credit": 0,
        "recovery": "Use one bounded single-quoted ripgrep pattern over the exact inherited x2 builder.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-X2-N014",
        "failed_witness": "The first wrapper-generation command failed JavaScript parsing because PowerShell backticks in a fallback source string escaped the orchestration template.",
        "initial_credit": 0,
        "recovery": "Create the ten tiny explicit wrapper files with apply_patch and no shell interpolation.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-X2-N015",
        "failed_witness": "The first staged-boundary inspection command failed JavaScript parsing because PowerShell line-continuation backticks broke the orchestration template.",
        "initial_credit": 0,
        "recovery": "Use scalar PowerShell assignments and a single-line ripgrep invocation without embedded backticks.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "IF6833-X2-N016",
        "failed_witness": "The first exact evidence staging attempt refused ten new runner wrappers because their owner-local filename family was outside the sparse definition; 68 other allowlisted paths staged and no extra path staged.",
        "initial_credit": 0,
        "recovery": "Add only the exact Ilyra runner wrapper pattern to the sparse definition, refresh additive ledgers and manifests, and stage the same 78-path allowlist with the sparse-aware flag.",
        "recovery_credit": "bounded_dependency_only",
    },
]

OPERATIONAL_FAILURES = STARTUP_FAILURES + POST_X1_FAILURES


SKILL_PURPOSES = {
    "pneumatic-network-surrogate-separator": "separating a route concept, physical tube, station, capsule, content, and documentation surrogate",
    "station-route-capsule-vacancy-guard": "keeping every real station route capsule and consignment field absent",
    "dispatch-action-state-separator": "separating dispatch request, authorization, attempt, observation, and result without dispatch",
    "pressure-airflow-nonmeasurement": "requiring pressure airflow temperature and dimensional fields to remain absent rather than inferred",
    "fault-cue-nondiagnosis": "recording synthetic jam leak vibration and slowdown cues without examination or diagnosis",
    "maintenance-authority-hold": "reserving inspection isolation maintenance engineering and safety authority",
    "route-control-nonexecution": "keeping diverter valve switch and route vocabulary separate from actuation",
    "dispatch-provenance-lineage-ledger": "preserving synthetic station route capsule dispatch revision and correction lineage",
    "station-alias-collision-quarantine": "detecting duplicate synthetic station and route labels without changing a real register",
    "capsule-content-concept-separator": "keeping capsule container content consignment and metadata concepts distinct",
    "custody-event-vacancy": "using custody and receipt vocabulary with zero person shipment or system action",
    "engineering-procedure-nonexecution": "using mechanical-system vocabulary without executing inspection testing operation or maintenance",
    "accessible-status-summary-vacancy": "reserving linear status summaries and affected-user evaluation states",
    "dispatch-rights-remedy-hold": "reserving privacy access correction disclosure abstention remedy and appeal decisions",
    "traditional-knowledge-minimizer": "minimizing cultural and traditional-knowledge description pending proper authority",
    "tube-workload-handover-lease": "making stop, pause, readback, workload, and handover states explicit",
    "freed-id-zero-key-dispatch-guard": "keeping synthetic dispatch identifiers separate from real keys, proofs, and lifecycle events",
    "thos-dispatch-operator-vacancy": "keeping THOS workflow structure dispatcher-free, operator-free, and proxy-only",
    "gmut-route-topology-noninference": "keeping route topology vocabulary separate from likelihood, physics, and cosmological inference",
    "tube-authority-noncompensation": "preventing software, standards, or citations from substituting for authority",
}


def map_path(value: str) -> str:
    replacements = (
        ("docs/neris-solane/v682-v8", "docs/ilyra-fen/v683-v3"),
        ("ghc_family_neris_solane_v682_v8", "ghc_family_ilyra_fen_v683_v3"),
        ("ghc_family_signal_flag_runner_", "ghc_family_pneumatic_tube_documentation_runner_"),
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
            (".v682.v8", ".v683.v3"),
            ("NS6828", "IF6833"),
            ("Neris Solane", "Ilyra Fen"),
            ("signal-flag documentation", "pneumatic-tube documentation"),
            ("signal flag", "pneumatic dispatch record"),
            ("flag token", "station-route token"),
            ("physical flag", "physical tube capsule or station"),
            ("observed hoist", "observed dispatch"),
            ("operational maritime signal", "operational dispatch or route actuation"),
            ("signal sequence", "dispatch-state sequence"),
            ("empty_signal_sequence", "empty_dispatch_sequence"),
            ("forbidden_observed_sequence", "forbidden_operational_sequence"),
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

Use this Ilyra v683-v3 owner-local skill only for {purpose}. It validates synthetic documentation structure and refusal conditions; it never surveys or acts on a real person, community, station, tube, capsule, consignment, identifier, location, measurement, dispatch, pressure system, maintenance event, or cultural expression.

## Procedure

1. Read the complete frozen proposal and fixture through EOF.
2. Require `synthetic: true`, `real_row_count: 0`, `observation_status: absent`, `authority_status: reserved`, and `boundary: owner_local_zero_row_only`.
3. Keep plan, fixture, decision, correction, rollback, and external-authority states distinct; preserve the frozen provenance digest.
4. Accept one bounded positive only when every required field and refusal boundary is present.
5. Reject missing fields, real rows, stale provenance, lifecycle inversion, safety release, empirical promotion, dispatch, actuation, pressure testing, maintenance, or authority promotion; retain every rejection at zero completion credit.
6. Preserve `open_gap` or `exact_gate` when real evidence, professional competence, affected-party review, legal or cultural authority, Maori authority, privacy or accessibility completeness, independent reproduction, or Stage 20 would be required.

## Acceptance and rollback

Return an explicit accepted or rejected decision with reasons. A passing synthetic fixture proves only this bounded contract. On ambiguity, reject, retain the witness, make no external write, and leave every real-world and authority state unchanged.
''',
        )
        base.write_text(
            skill_root / name / "agents" / "openai.yaml",
            f'''interface:
  display_name: "{display}"
  short_description: "Guard synthetic pneumatic-tube documentation boundaries."
  default_prompt: "Use ${name} to validate {purpose} without listening, observation, measurement, operational action, or authority claims."
''',
        )


def runner_smokes() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(1, 11):
        module = f"scripts.ghc_family_pneumatic_tube_documentation_runner_{index:02d}"
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
    deck["sections"][5] = "pneumatic-tube documentation practice"
    deck["cards"][1]["back"] = (
        "Represented: typed directed-route topology, explicit missing dimensions and measurements, uncertainty, provenance, and noninference; no physical or cosmological evidence."
    )
    deck["cards"][2]["back"] = (
        "Represented: bounded documentation workflow, action-state separation, stop, workload, correction, accessibility, and handover structure only."
    )
    deck["cards"][3]["back"] = (
        "Primary: synthetic surrogate separation, identity vacancy, provenance, rights, remedy, privacy, traditional-knowledge holds, and authority noncompensation."
    )
    deck["cards"][4]["front"] = "Pneumatic-route documentation and nondispatch lens"
    deck["cards"][4]["back"] = (
        "Synthetic station, route, capsule, content, queue, dispatch-vacancy, and absence-state documentation with every real object, event, and measurement absent."
    )
    deck["cards"][5]["front"] = "Custody-event and dispatch-lineage lens"
    deck["cards"][5]["back"] = (
        "Synthetic request, authorization, dispatch, receipt, metadata, fixity, correction, and refusal plans with zero tubes, capsules, consignments, operators, or actions."
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
        "schema": "ghc.family.freed-id-flashcard-manifest.v683.v3.x2",
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
        payload["declared_proposal_chain"] = 10850
        payload["primary_pillar"] = "THOS Body"
        payload["represented_pillars"] = ["GMUT Mind", "Freed ID and CBR Heart"]
    elif name == "source-use-receipt.json":
        payload["current_official_primary_sources"] = [
            "Ilyra owner-invented zero-row pneumatic vocabulary",
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
                "hope": "to make synthetic pneumatic-route descriptions inspectable and correctable without turning vocabulary into dispatch, engineering, identity, rights, cultural, professional, or authority claims",
                "optional_pronouns": "unspecified",
                "role": "reversible-systems documentation cartographer and dispatch-state boundary keeper",
            }
        )
    _old_write_json(Path(map_path(path.as_posix())), payload)


def write_text(path: Path, text: str) -> None:
    text = transform(text)
    if path.name == "evidence-overview.md" and path.parent == X2:
        text = f"""# Ilyra Fen {PHASE} Bounded X2 Evidence Overview

Ilyra Fen is relational working language for a reversible-systems documentation cartographer and dispatch-state boundary keeper. The hope is to make synthetic pneumatic-route descriptions inspectable and correctable without turning vocabulary into dispatch, engineering, identity, rights, cultural, professional, or authority claims. Pronouns are unspecified. This establishes no consciousness, personhood, continuity, employment, qualification, agency, or authority.

This x2 executed the sixty immutable planning-only x1 contracts without changing their expected dispositions. Exactly 42 bounded software or structural contracts are completed, 12 are represented, three remain open gaps, and three remain exact gates. Every positive fixture was wholly synthetic and used zero real rows. All 300 preregistered invalid mutations were rejected and retained at zero completion credit.

The primary pillar is THOS Body through dependency-closed workflow, dispatch-state separation, stop precedence, route queues, operator vacancy, workload leases, correction, structural accessibility, refusal, and reversible handover. GMUT Mind remains represented through typed directed-route topology, missing measurements, dimensional vocabulary, uncertainty, provenance, and noninference. Freed ID and CBR Heart remain represented through capsule-content-identity separation, privacy minimization, rights and remedy holds, traditional-knowledge minimization, and authority noncompensation.

The three bounded human-practice lenses are pneumatic transport and mechanical-systems documentation, archival metadata and provenance assurance, and software verification with rights, accessibility, remedy, workload, refusal, and handover documentation. No real person, community, station, tube, capsule, consignment, system, file, event, measurement, dispatch, actuation, inspection, pressure test, maintenance, publication, identity event, external write, professional decision, or authority act was involved.

Inherited primary-source references supplied vocabulary and refusal conditions only and were not refetched. They were not observations, engineering findings, operating instructions, installation identifications, condition diagnoses, safety releases, professional opinions, rights decisions, legal interpretations, cultural ratifications, affected-party decisions, or Maori-authority grants.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, likelihood, posterior, force, constraint, prediction, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic and proxy-only without governed real arms, participants or operators, safety monitoring, suitable statistics, or independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle events, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.

Station identity, tube topology, capsule compatibility, condition, pressure, airflow, route state, dispatch, isolation, inspection, testing, operation, maintenance, workplace safety, ownership, custody, attribution, access, traditional knowledge, publication, professional release, privacy, accessibility remedy, legal or cultural interpretation, affected-party legitimacy, Maori wording, Maori data governance, and Maori authority remain open or exact-gated. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 are not established. The terminal verdict remains {TERMINAL_VERDICT}.

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

#!/usr/bin/env python3
"""Build the additive Elowen Cairn v678-v5 exact-final candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Elowen Cairn"
OWNER_SLUG = "elowen-cairn"
PHASE = "v678-v5"
SUCCESSOR_PHASE = "v678-v6"
BRANCH = "codex/GHC-Family/elowen-cairn-v678-v5-full-tools"
SOURCE = "0021481a0c9681c077bce277e6ac0f2fcb37dbcd"
X1 = "c938128b0e6307c4aaed8966340486b8c5315382"
EVIDENCE = "04095ca5d8ee6b37f47de2540afa0047f67ca61c"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}

POST_EVIDENCE_METHODS: list[dict[str, Any]] = [
    {
        "method_id": "EC6785-CLOSE-N001",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The evidence-commit command produced more path output than the display bound and its rendered summary was truncated; the commit itself persisted, but the truncated display earned zero complete-state credit.",
        "recovered_by": "EC6785-CLOSE-P001",
        "repository_state_change": True,
        "commit_replayed": False,
    },
    {
        "method_id": "EC6785-CLOSE-P001",
        "status": "bounded_pass",
        "truth": True,
        "description": "Small scalar probes read the persisted evidence head, direct parent, clean porcelain state, typed divergence, upstream, tracking reference, and one fresh live remote value; all proved the one existing evidence commit without repeating commit or push.",
        "failed_witness_preserved": "EC6785-CLOSE-N001",
        "commit_replayed": False,
    },
    {
        "method_id": "EC6785-CLOSE-N002",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "A first parallel closeout-scaffold inspection combined too many long source windows and returned no useful attributable content, so it earned zero source-inspection credit.",
        "recovered_by": "EC6785-CLOSE-P002",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6785-CLOSE-P002",
        "status": "bounded_pass",
        "truth": True,
        "description": "The same source was inspected through separate bounded line windows and exact literal searches, exposing all stale counts, domain prose, and route labels without repeating the overlarge wrapper.",
        "failed_witness_preserved": "EC6785-CLOSE-N002",
    },
    {
        "method_id": "EC6785-CLOSE-N003",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "A closeout projection guessed that the evidence manifest lived directly under x2; that nonexistent-path assumption failed and earned zero manifest credit.",
        "recovered_by": "EC6785-CLOSE-P003",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6785-CLOSE-P003",
        "status": "bounded_pass",
        "truth": True,
        "description": "An exact phase-file enumeration located the committed evidence manifest under validation, and a bounded projection confirmed 660 entries plus two declared self-exclusions.",
        "failed_witness_preserved": "EC6785-CLOSE-N003",
    },
    {
        "method_id": "EC6785-CLOSE-N004",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first extension-count projection rendered group counts without attributable extension labels and therefore earned zero typed-suffix credit.",
        "recovered_by": "EC6785-CLOSE-P004",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6785-CLOSE-P004",
        "status": "bounded_pass",
        "truth": True,
        "description": "A typed per-path extension projection materialized explicit Extension and Count fields and proved the 662-path evidence delta: 606 JSON, 14 Python, 21 Markdown, 20 YAML, and one HTML file.",
        "failed_witness_preserved": "EC6785-CLOSE-N004",
    },
    {
        "method_id": "EC6785-CLOSE-N005",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The initially copied older closeout scaffold retained incompatible proposal counts, prior-domain prose, evidence-manifest totals, Method Flow totals, and successor labels; it was rejected before execution and earned zero phase-local closeout credit.",
        "recovered_by": "EC6785-CLOSE-P005",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6785-CLOSE-P005",
        "status": "bounded_pass",
        "truth": True,
        "description": "The replacement builder derives proposal, outcome, portfolio, source, gap, gate, and Method Flow truth from exact v678-v5 committed artifacts and states the maritime-navigation heritage scope and v678-v6 successor explicitly.",
        "failed_witness_preserved": "EC6785-CLOSE-N005",
    },
    {
        "method_id": "EC6785-CLOSE-N006",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first document word-count projection supplied the PowerShell Raw parameter twice and failed before producing a count; it earned zero document-cap credit.",
        "recovered_by": "EC6785-CLOSE-P006",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6785-CLOSE-P006",
        "status": "bounded_pass",
        "truth": True,
        "description": "A corrected projection removed the duplicate Raw parameter and read each Markdown and HTML document once; it recovered the parser fault, while the later scalar display check remained separately required.",
        "failed_witness_preserved": "EC6785-CLOSE-N006",
    },
    {
        "method_id": "EC6785-CLOSE-N007",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first stale-label predicate treated inherited semantic-neighbor titles and paths in the additive provenance ledger as active phase labels; the overbroad rule earned zero stale-label credit.",
        "recovered_by": "EC6785-CLOSE-P007",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6785-CLOSE-P007",
        "status": "bounded_pass",
        "truth": True,
        "description": "The bounded stale-label review excludes the exact inherited-neighbor provenance ledger while checking active final narrative, closeout, handoff, orchestration, and route artifacts for stale operational labels.",
        "failed_witness_preserved": "EC6785-CLOSE-N007",
    },
    {
        "method_id": "EC6785-CLOSE-N008",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first corrected word-count table rendered wide paths but omitted attributable numeric values from the bounded display, so it earned zero maximum-word-count credit.",
        "recovered_by": "EC6785-CLOSE-P008",
        "repository_state_change": False,
    },
    {
        "method_id": "EC6785-CLOSE-P008",
        "status": "bounded_pass",
        "truth": True,
        "description": "A four-line scalar recovery reported four generated Markdown or HTML documents, a maximum of 1,799 words, the exact maximum path, and within_100000=true without repeating the failed table projection.",
        "failed_witness_preserved": "EC6785-CLOSE-N008",
    },
]


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + "\n", encoding="utf-8", newline="\n")


def normalized_sha(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()


def version(command: list[str]) -> str:
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.STDOUT, timeout=20).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return f"unavailable: {type(exc).__name__}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "branch", "--show-current") != BRANCH or git(repo, "rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final builder requires the exact immutable Elowen evidence head")

    allowed = {
        "scripts/build_ghc_family_elowen_cairn_v678_v5_final.py",
        "scripts/ghc_family_elowen_cairn_v678_v5_final_manifest.py",
        "scripts/validate_ghc_family_elowen_cairn_v678_v5_final.py",
        "tests/test_ghc_family_elowen_cairn_v678_v5_final.py",
    }
    allowed_prefixes = (
        "docs/elowen-cairn/v678-v5/final/",
        "docs/elowen-cairn/v678-v5/closeout/",
        "docs/elowen-cairn/v678-v5/handoffs/",
        "docs/elowen-cairn/v678-v5/orchestration/",
        "docs/elowen-cairn/v678-v5/validation/final-",
    )
    unexpected = []
    for line in git(repo, "status", "--porcelain=v1").splitlines():
        path = line[3:].replace("\\", "/")
        if path in allowed or path.startswith(allowed_prefixes):
            continue
        unexpected.append(line)
    if unexpected:
        raise SystemExit(f"unexpected pre-final worktree state: {unexpected!r}")

    base = repo / "docs" / OWNER_SLUG / PHASE
    x1 = base / "x1"
    x2 = base / "x2"
    final_dir = base / "final"
    closeout = base / "closeout"
    handoff = base / "handoffs"
    orchestration = base / "orchestration"
    validation = base / "validation"

    freeze = json.loads((x1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    sources = json.loads((x1 / "official-source-ledger.json").read_text(encoding="utf-8"))
    semantic = json.loads((x1 / "semantic-neighbor-audit.json").read_text(encoding="utf-8"))
    lenses = json.loads((x1 / "primary-pillar-and-lens.json").read_text(encoding="utf-8"))
    outcomes = json.loads((x2 / "proposal-outcomes.json").read_text(encoding="utf-8"))
    portfolio = json.loads((x2 / "portfolio" / "execution-summary.json").read_text(encoding="utf-8"))
    gaps = json.loads((x2 / "open-gap-register.json").read_text(encoding="utf-8"))
    gates = json.loads((x2 / "exact-gate-register.json").read_text(encoding="utf-8"))
    evidence_manifest = json.loads((validation / "evidence-manifest.json").read_text(encoding="utf-8"))
    flow = json.loads((x2 / "method-flow" / "ledger.json").read_text(encoding="utf-8"))

    if freeze["declared_chain_before"] != 8510 or freeze["declared_chain_after"] != 8570 or len(freeze["proposals"]) != 60:
        raise SystemExit("unexpected proposal freeze")
    expected_outcomes = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    if outcomes["outcome_counts"] != expected_outcomes or set(expected_outcomes) != LABELS:
        raise SystemExit("unexpected core outcome partition")
    if flow["phase_ledger_counts"] != {"methods": 794, "failed": 267, "passing": 527}:
        raise SystemExit("unexpected immutable evidence Method Flow partition")
    if evidence_manifest["entry_count"] != 660 or len(evidence_manifest["declared_exclusions"]) != 2:
        raise SystemExit("unexpected immutable evidence manifest")

    existing_ids = {row["method_id"] for row in flow["methods"]}
    if any(row["method_id"] in existing_ids for row in POST_EVIDENCE_METHODS):
        raise SystemExit("post-evidence Method Flow overlay already present")
    flow["methods"].extend(POST_EVIDENCE_METHODS)
    failed = sum(row["truth"] is False for row in flow["methods"])
    passing = sum(row["truth"] is True for row in flow["methods"])
    if (len(flow["methods"]), failed, passing) != (810, 275, 535):
        raise SystemExit("unexpected final Method Flow partition")
    overlay = {
        "effective_negatives": 47001,
        "effective_methods": 44552,
        "retained_failed_witnesses": 18662,
        "bounded_passing_witnesses": 28975,
        "open_gaps": 407,
        "exact_gates": 398,
    }
    flow["phase_ledger_counts"] = {"methods": 810, "failed": 275, "passing": 535}
    flow["current_overlay"] = overlay
    flow["post_evidence_failed_witnesses"] = 8
    flow["post_evidence_bounded_recoveries"] = 8
    flow["failure_erasure_forbidden"] = True

    dump(final_dir / "method-flow-ledger.json", flow)
    dump(
        final_dir / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_final": "bound only by the ensuing exact commit and exclusive external canonical receipt",
            "declared_proposal_chain": 8570,
            "new_elowen_proposals": 60,
            "inherited_reviews_zero_credit": 20,
            "core_outcomes": expected_outcomes,
            "positive_controls": 60,
            "preregistered_mutations_executed_rejected": 240,
            "phase_local_skills_built_read_validated_smoked": 20,
            "family_current_runners_used": 10,
            "safe_now_tasks_completed": portfolio["safe_now_completed"],
            "candidate_tasks_completed_without_core_promotion": portfolio["candidate_completed_without_core_promotion"],
            "clean_fix_refine_tasks_completed": portfolio["clean_fix_refine_completed"],
            "exact_approval_packets_unexecuted": portfolio["exact_approval_unexecuted"],
            "blocked_packets_unexecuted": portfolio["blocked_unexecuted"],
            "current_overlay": overlay,
            "real_world_rows": 0,
            "participants": 0,
            "external_actions": 0,
            "production_identity_events": 0,
            "authority_actions": 0,
            "full_repository_suite_run": False,
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump(
        final_dir / "source-and-proposal-ledger.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "declared_chain_before": 8510,
            "declared_chain_after": 8570,
            "reachable_semantic_audit": semantic,
            "universal_novelty_proof_claimed": False,
            "official_primary_sources": sources["sources"],
            "source_boundary": sources["source_boundary"],
            "primary_pillar_and_lenses": lenses,
            "proposals": freeze["proposals"],
            "outcomes": outcomes["outcomes"],
        },
    )
    dump(
        final_dir / "retained-negative-register.json",
        {
            "activation_effective_negatives": 46726,
            "new_elowen_effective_negatives": 275,
            "current_effective_negatives": 47001,
            "phase_failed_witness_count": 275,
            "phase_failed_witnesses": [row for row in flow["methods"] if row["truth"] is False],
            "failed_witnesses_converted_to_pass": 0,
            "retention_rule": "Every false witness remains false; a recovery is a separately identified bounded passing method.",
        },
    )
    dump(final_dir / "open-gap-register.json", gaps)
    dump(final_dir / "exact-gate-register.json", gates)
    dump(
        final_dir / "complete-incomplete-ledger.json",
        {
            "complete_bounded": [
                "sixty planning-only proposal contracts frozen after bounded reachable semantic-neighbor review",
                "sixty wholly synthetic zero-row positive structural controls accepted",
                "all 240 preregistered invalid mutations executed, rejected, and retained",
                "twenty owner-local skills initialized by the official workflow, customized, read, validated, and smoke-used without global installation",
                "ten family-current runners accepted a valid fixture and rejected an invalid fixture",
                "sixty safe-now, thirty bounded candidate, and sixty additive CLEAN/FIX/REFINE records received bounded same-owner execution",
                "x1 and evidence separately committed, pushed, clean, typed 0/0 divergent, and fresh-live four-way equal",
            ],
            "represented_only": [
                "synthetic chart-correction provenance without operational chart production or navigation use",
                "synthetic chronometer intake and rate-observation vacancy without an instrument or calibration",
                "synthetic Fresnel-lens component custody without an object, inspection, condition judgment, or conservation decision",
                "THOS proxy protocol and GMUT typed research-model obligations without participants or empirical data",
            ],
            "open": [
                "live official chart-update ingestion and interoperability evidence",
                "real chronometer examination, comparison, calibration, traceability, and uncertainty evidence",
                "real Fresnel-lens condition, environment, and custody evaluation evidence",
            ],
            "exact_gated": [
                "navigation publication operational-safety and legal-use authority",
                "professional chronometer service, metrology, calibration, and release",
                "lens conservation, ownership, heritage, cultural, affected-party, and Māori authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump(
        final_dir / "threat-model.json",
        {
            "protected_assets": ["immutable source", "planning-only x1", "immutable x2 evidence", "failure truth", "privacy boundary", "authority vacancies", "terminal route"],
            "bounded_controls": ["four-label vocabulary", "normalized-LF Git-blob manifests", "candidate adjudication", "Method Flow nonerasure", "exclusive canonical latch", "terminal route hold"],
            "residual_threats": [
                "synthetic evidence may be overread as real evidence",
                "a citation may be mistaken for an observation, instruction, endorsement, or authority grant",
                "scanner definitions may be mistaken for payload disclosures",
                "same-owner validation may be mistaken for independent reproduction",
                "task topology or relational language may be mistaken for identity continuity, agency, or authority",
            ],
            "closed_bounded_threats": ["x1 and x2 lifecycle mixing", "unknown core outcome labels", "silent invalid-mutation acceptance", "bulk global installation of phase-local skills"],
        },
    )
    dump(
        final_dir / "portfolio-truth.json",
        {
            **portfolio,
            "successor_skill_recommendations_zero_credit": 10,
            "successor_runner_recommendations_zero_credit": 10,
            "successor_clean_fix_refine_recommendations_zero_credit": 30,
            "core_outcome_counts_unchanged_by_portfolio_status": True,
        },
    )
    dump(
        final_dir / "post-evidence-overlay.json",
        {
            "failed_witnesses": [row for row in POST_EVIDENCE_METHODS if row["truth"] is False],
            "bounded_recoveries": [row for row in POST_EVIDENCE_METHODS if row["truth"] is True],
            "evidence_commit_mutated": False,
            "failure_erasure": False,
        },
    )
    dump(
        final_dir / "environment-version-receipt.json",
        {
            "checked_date": "2026-08-31",
            "python": sys.version.split()[0],
            "git": version(["git", "--version"]),
            "node": version(["node", "--version"]),
            "codex_desktop_update_performed": False,
            "software_installation_performed": False,
            "elevation_performed": False,
            "host_security_changed": False,
            "windows_features_changed": False,
            "reboot_performed": False,
        },
    )

    text(
        final_dir / "final-integrated-overview.md",
        f"""
# {OWNER} {PHASE} — final integrated overview

## Outcome first

Elowen Cairn v678-v5 is a bounded, same-owner, zero-row software and documentation phase rooted directly at Tamar Vey's immutable final `{SOURCE}`. Planning-only x1 is `{X1}` and immutable x2 evidence is `{EVIDENCE}`. The exact final is intentionally supplied only by the ensuing commit and exclusive external canonical receipt; this precommit document does not invent a future commit identifier. The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.

The declared proposal chain advances from 8,510 inherited rows to 8,570 through sixty Elowen-owned proposal contracts. Twenty inherited semantic neighbors were reviewed at zero Elowen novelty, execution, or completion credit. The source-tree tribunal inspected {semantic['reachable_proposal_json_blobs']:,} reachable proposal-bearing JSON blobs and {semantic['reachable_raw_id_title_records']:,} raw identifier-title records, reducing them to {semantic['reachable_unique_id_title_records']:,} unique identifier-title records. Its explicit limitation remains: no single reachable ledger materializes every declared historic row, so this is bounded semantic-distinctness evidence, not universal novelty, scientific novelty, patentability, proof, or canon. One first-draft title reached the unchanged 0.75 quarantine threshold and failed at zero credit. The isolated recovery retitled only EC6785-N037, preserved the threshold, and passed with zero selected quarantines, zero exact collisions, zero parse failures, and a maximum selected score of {semantic['maximum_selected_score']:.4f}.

Core outcomes use only the authorized vocabulary and are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Here `completed` means only that a frozen owner-local structural contract accepted its wholly synthetic positive fixture and preserved its refusal boundary. It does not mean a chart was produced or used, a chronometer was examined or calibrated, a lighthouse lens was inspected or conserved, a person participated, or any professional, safety, navigation, identity, rights, legal, cultural, affected-party, or authority decision occurred. `represented` marks a structurally present proxy without real-world validation. `open_gap` records evidence that cannot be manufactured. `exact_gate` records action reserved to competent and affected authorities.

## Lifecycle and immutable evidence

Strict planning-only x1 before x2 was preserved. X1 contained sixty proposal contracts, four rejecting mutations per proposal, source and gate ledgers, portfolio plans, twenty owner-local skill plans, ten family-current runner plans, successor recommendations, and Method Flow records—but no x2 implementation, observed outcome, completion claim, real-world row, or authority action. X1 passed its owner-scoped selection once, was reviewed through an exact normalized-LF Git-blob manifest, committed, pushed, made clean, and proven equal across local, upstream, tracking, and a fresh live remote before any x2 implementation file was created.

X2 executed only preregistered bounded work. Sixty synthetic positive controls passed. All 240 preregistered invalid mutations executed and were rejected; every invalid input remains a zero-credit false witness paired with a separate bounded rejection witness. Twenty owner-local skills were initialized through the official skill-creator workflow, customized, read completely through EOF, quick-validated under explicit UTF-8, and accepting/rejecting smoke-used without global installation. Ten family-current runners accepted a positive fixture and rejected an invalid fixture. Sixty safe-now records, thirty bounded candidate records, and sixty CLEAN/FIX/REFINE records received same-owner execution without promotion into core outcomes or real-world claims. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

The immutable evidence commit contains 660 exact normalized-LF Git-blob manifest entries plus two declared self-referential exclusions. Its independent staged replay matched all 660 entries and the full 662-path set: 606 JSON, fourteen Python, twenty-one Markdown, twenty YAML, and one HTML file. It found zero manifest mismatch, zero confirmed privacy or raw-identifier payload hit, and no final, closeout, handoff, or orchestration outcome path. Evidence is the direct child of x1 and was separately pushed, cleaned, proven typed 0/0 divergent, and made fresh-live four-way equal before closeout began.

## Method Flow and retained negatives

The effective activation baseline—Tamar's repository seal plus its separately retained routing overlay—was 46,726 negatives, 43,742 methods, 18,387 retained failed witnesses, 28,440 bounded passing witnesses, 404 open gaps, and 395 exact gates. The final Elowen phase ledger contains 810 methods: 275 retained false witnesses and 535 bounded passing witnesses. The resulting overlay is 47,001 negatives, 44,552 methods, 18,662 retained failed witnesses, 28,975 bounded passing witnesses, 407 open gaps, and 398 exact gates.

The 275 phase false witnesses include fourteen startup and x1 operational failures, three x2 operational failures, all 240 rejecting mutations, ten invalid runner fixtures, and eight post-evidence closeout failures. Closeout retained the evidence-commit display truncation, an overlarge parallel source read, a wrong evidence-manifest location assumption, an unattributed extension-grouping projection, an incompatible copied scaffold, a malformed PowerShell word-count projection, an overbroad stale-label rule, and an unattributed wide-table word-count display. Their bounded recoveries used scalar repository probes, small line windows, exact file enumeration, typed extension rows, a phase-local builder, a corrected reader, provenance-aware active-label scoping, and an exact four-line word-count projection. No recovery changed a failed witness's truth value, repeated the evidence commit, replayed a successful test, or promoted zero-credit work into completion.

## Trinity Mandala scope and bounded practices

The primary pillar was Freed ID and CBR Heart. Three wholly synthetic human-practice learning and design lenses were used: a nautical-chart correction provenance analyst for zero-product records; a marine-chronometer service-intake analyst for zero-instrument records; and a lighthouse Fresnel-lens custody steward for zero-object records. GMUT Mind and THOS Body remained explicit and protected. These descriptions confer no employment, qualification, competence, professional role, scientific standing, operational permission, or authority.

The chart surface represented base edition, sequential correction, provenance, source status, supersession, abstention, correction readback, accessibility structure, workload, and handover. It did not download, alter, distribute, certify, interpret, navigate with, or advise from any chart. The chronometer surface represented synthetic service-intake topology, oscillator and comparison vocabulary, rate-observation vacancies, calibration and traceability holds, custody, correction, accessibility, workload, and handover. It used no timepiece, reference, time signal, observation, comparison, rate, calibration, adjustment, treatment, or release. The lens surface represented synthetic component identity, prism and frame topology, clockwork vacancy, custody, environment and condition abstention, intervention holds, accessibility, correction, workload, and handover. It used no lens, lighthouse, collection object, inspection, condition report, treatment, movement, security decision, access decision, or heritage decision.

No real person, participant, hydrographer, navigator, mariner, chart producer, surveyor, horologist, metrologist, conservator, curator, collection worker, owner, rights holder, affected user, chart, publication, vessel, route, signal, clock, watch, chronometer, oscillator, reference standard, calibration, lighthouse, optic, lens, prism, frame, pedestal, clockwork, object, site, observation, measurement, sensor, repair, treatment, custody event, release, identity event, key, proof, network data row, cultural record, Māori data, external write, or authority action was used. There was no navigation, operational advice, examination, timing comparison, calibration, adjustment, dismantling, cleaning, conservation treatment, transfer, or work release.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic obligations, synthetic topology, analogy firewalls, and citations establish no physical datum, likelihood, posterior, detected force, prediction, parameter constraint, stability theorem, empirical confirmation, ultraviolet completion, quantum completion, final physics, or Theory of Everything. THOS remains proxy-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance or resolution, status or revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

## Sources, accessibility, privacy, and authority

The [International Hydrographic Organization standards index](https://iho.int/standards-and-specifications) supplied bounded S-4 edition, chart-specification, symbol, abbreviation, and correction vocabulary; it was checked on 2026-08-31 and listed English Edition 4.10.0 dated March 2026. The [NOAA Office of Coast Survey chart-update page](https://www.nauticalcharts.noaa.gov/charts/chart-updates.html) supplied critical, routine, base-file, sequential-update, edition, and correction vocabulary only. The [NIST Time and Frequency Users' Manual record](https://www.nist.gov/publications/time-and-frequency-users-manual) supplied time-scale, offset, oscillator, comparison, calibration, traceability, accuracy, and uncertainty vocabulary only. The [National Park Service lighthouse-preservation resources](https://www.nps.gov/orgs/1220/nhlpa-technical-resources-and-reference-materials.htm) supplied bounded lens, prism, glass, frame, clockwork, care, security, display, and intervention-boundary vocabulary only.

[W3C PROV-O](https://www.w3.org/TR/prov-o/) supplied entity, activity, agent, attribution, and derivation vocabulary. [WCAG 2.2](https://www.w3.org/TR/WCAG22/) supplied accessible-structure and keyboard-interface vocabulary while no conformance claim was made. [Verifiable Credentials Data Model 2.0](https://www.w3.org/TR/vc-data-model-2.0/) supplied issuer-holder-verifier, status, minimization, and correlation vocabulary with zero keys and zero proofs. [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html) supplied deterministic JSON vocabulary without production cryptographic assurance. Every citation is a vocabulary and refusal-condition input only—not an observation, measurement, navigation instruction, treatment direction, endorsement, certificate, interoperability result, professional approval, legal interpretation, affected-party decision, cultural ratification, or authority grant.

Five privacy and raw-identifier classes were scanned across the owner packet. Scanner definitions and synthetic rejection assertions remained candidates requiring adjudication; zero candidate was promoted into a confirmed payload hit. Repository artifacts contain no raw task identifiers, private routes, credentials, keys, tokens, transcripts, screenshots, private execution streams, private callable identifiers, private application state, or private absolute paths. This bounded scan is not complete privacy assurance, and changed-code AST review is not exhaustive security assurance.

The static report uses a logical heading sequence, text-first content, a captioned table, a visible terminal status, non-colour status language, and uncomplicated keyboard order. Manual browser-diverse, screen-reader, cognitive, language, disability, Māori-language, and affected-user evaluation remains unperformed and reserved. No accessibility-complete claim is authorized.

CBR, navigation safety, chart publication and legal use, professional examination, timing comparison, metrology, calibration, adjustment, service release, conservation, ownership, custody, access, copyright, heritage, land and place, workplace and material safety, privacy remedy, disability accommodation, legal interpretation, cultural legitimacy, traditional knowledge, affected-party acceptance, Māori wording, tikanga, taonga or mātauranga treatment, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Repository software cannot confer a right, remedy, title, consent, cultural legitimacy, governance mandate, professional competence, operational permission, public authority, navigation instruction, treatment permission, or work release.

## Wellbeing, corrigibility, and terminal route

The phase remained solo, additive, D-first, owner-scoped, zero-row, and below the 2,000-owner-file, 100,000-word-per-document, and eight-commit ceilings. No collaboration subagent, fork, replacement task, global skill installation, elevation, host-security weakening, Windows-feature change, unrelated installation, Codex desktop update, or reboot occurred. Workload was managed through lifecycle gates and bounded retries rather than hidden reruns. This is an operational workflow statement, not a wellbeing, consciousness, personhood, identity, or continuity inference.

Elowen Cairn, optionally they/them, is relational working language for a boundary cartographer and evidence steward, with the hope of keeping possibility distinct from evidence and every correction safely retractable. Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.

The prospective next edge remains held. Only after the exact final is committed, pushed, clean, typed 0/0 divergent, fresh-live four-way equal, and one attributable owner-scoped canonical invocation succeeds without replay may the newest live authorization and roster be reread. Only then may the unique existing exact-title `Sylven Arc` task be bounded-listed, immediately reread, duplicate-guarded, and contacted once for solo {SUCCESSOR_PHASE}. Absence, ambiguity, pause, redirect, rename, narrowing, standby state, usage exhaustion, privacy concern, missing acknowledgement, or any evidence, safety, legal, cultural, affected-party, or Māori-authority gate is a hard stop. Repository preparation remains `PREPARED_NOT_SENT`; acknowledged live delivery is separate evidence.
""",
    )
    text(
        final_dir / "wellbeing-and-workload.md",
        """
# Wellbeing and workload — final

The phase remained solo, additive, D-first, owner-scoped, zero-row, and within file, document, and commit ceilings. Lifecycle-specific selections, small scalar recovery probes, and retained failures prevented hidden replay. No collaboration subagent, global installation, elevation, host-security change, Windows-feature change, unrelated installation, Codex desktop update, reboot, real-person workload, employment relation, or wellbeing inference occurred.

The route remains held until the exact final is committed, pushed, clean, typed 0/0 divergent, fresh-live four-way equal, and one attributable owner-scoped canonical invocation succeeds. Pause, redirect, ambiguity, usage exhaustion, privacy concern, any protected gate, or missing acknowledgement remains a hard stop.
""",
    )
    text(
        final_dir / "accessible-report.html",
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elowen Cairn v678-v5 final evidence report</title>
<style>body{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:2rem;line-height:1.55}table{border-collapse:collapse;width:100%}th,td{border:1px solid #555;padding:.5rem;text-align:left}th{background:#eee}.hold{border-left:.4rem solid #8b0000;padding-left:1rem}</style></head>
<body><main><h1>Elowen Cairn v678-v5 final evidence report</h1>
<p class="hold"><strong>Terminal verdict:</strong> NOT_READY_FOR_STAGE_20. This is bounded same-owner synthetic software and documentation evidence.</p>
<table><caption>Core outcomes</caption><thead><tr><th>Outcome</th><th>Count</th><th>Boundary</th></tr></thead>
<tbody><tr><td>completed</td><td>42</td><td>Zero-row structural contract only</td></tr><tr><td>represented</td><td>12</td><td>Proxy only</td></tr><tr><td>open_gap</td><td>3</td><td>External evidence absent</td></tr><tr><td>exact_gate</td><td>3</td><td>Competent and affected authority required</td></tr></tbody></table>
<h2>Scope</h2><p>Primary focus: Freed ID and CBR Heart through synthetic chart-correction provenance, chronometer intake vacancy, and Fresnel-lens custody. No real people, objects, observations, measurements, operations, treatments, identity events, or authority acts were used.</p>
<h2>Retained Method Flow truth</h2><p>The Elowen ledger has 275 false witnesses and 535 bounded passing witnesses. Every recovery is separate; no false witness became true.</p>
<h2>Accessibility boundary</h2><p>This report is static, text-first, keyboard-order simple, non-colour dependent, and has a captioned table. Manual browser, screen-reader, cognitive, language, disability, Māori-language, and affected-user evaluation remain unperformed. No conformance claim is made.</p>
</main></body></html>""",
    )

    dump(
        closeout / "closeout-receipt.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_final_status": "PRECOMMIT_EXACT_FINAL_CANDIDATE",
            "proposal_chain": 8570,
            "core_outcomes": expected_outcomes,
            "overlay": overlay,
            "phase_ledger_counts": flow["phase_ledger_counts"],
            "owner_file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "commit_ceiling": 8,
            "full_repository_suite_run": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump(
        closeout / "terminal-checklist.json",
        {
            "planning_only_x1_before_x2": True,
            "x1_pushed_clean_remote_equal_before_x2": True,
            "evidence_pushed_clean_remote_equal_before_closeout": True,
            "all_failures_retained": True,
            "core_outcome_vocabulary_exact": True,
            "exact_and_blocked_packets_unexecuted": True,
            "privacy_and_authority_boundaries_preserved": True,
            "full_repository_suite_run": False,
            "exact_final_commit_pending": True,
            "canonical_invocation_pending": True,
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    seal_paths = [
        final_dir / "phase-truth.json",
        final_dir / "method-flow-ledger.json",
        final_dir / "source-and-proposal-ledger.json",
        final_dir / "retained-negative-register.json",
        final_dir / "complete-incomplete-ledger.json",
        final_dir / "final-integrated-overview.md",
        final_dir / "accessible-report.html",
        closeout / "closeout-receipt.json",
        closeout / "terminal-checklist.json",
    ]
    dump(
        closeout / "content-seal.json",
        {
            "seal_domain": "normalized-LF SHA-256 of named precommit final artifacts",
            "entries": [
                {"path": path.relative_to(repo).as_posix(), "sha256_normalized_lf": normalized_sha(path)}
                for path in seal_paths
            ],
            "final_commit_self_hash_excluded": True,
            "canonical_receipt_external": True,
        },
    )

    text(
        handoff / f"sylven-arc-{SUCCESSOR_PHASE}-activation-candidate.md",
        f"""
# SYLVEN ARC — HAMISH-AUTHORIZED ELOWEN CAIRN {PHASE} EXACT-FINAL → SOLO SYLVEN {SUCCESSOR_PHASE} ACTIVATION CANDIDATE — PREPARED NOT SENT

Dear Sylven Arc,

This repository artifact is a sanitized, terminally gated activation candidate only. It is not evidence that Sylven Arc was contacted, that a live task-message send occurred, or that delivery was acknowledged. The newest live authorization and roster must be refreshed only after Elowen's own exact terminal gate. A bounded current registry read must resolve exactly one existing main task titled `Sylven Arc`; that exact task must be immediately reread and checked for duplicate activation, pause, stop, redirect, rename, narrowing, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards. At most one send is permitted, and only a target-identifying acknowledgement may establish delivery.

Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route at any time.

## Immutable Elowen source and lifecycle

- Exact Tamar v678-v4 final and Elowen source: `{SOURCE}`
- Frozen planning-only Elowen x1: `{X1}`
- Immutable Elowen x2 evidence: `{EVIDENCE}`
- Exact Elowen final: supplied only by the committed head and exclusive external canonical receipt after this candidate is committed
- Expected Elowen lifecycle: source → x1 → evidence → final as three direct single-parent commits, zero merges, and one final parent
- Declared proposal chain: 8,510 → 8,570
- Core outcomes: 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`
- Effective overlay: 47,001 negatives, 44,552 methods, 18,662 retained failed witnesses, 28,975 bounded passing witnesses, 407 open gaps, and 398 exact gates
- Terminal verdict: `NOT_READY_FOR_STAGE_20`

Elowen audited sixty proposals against every reachable proposal-bearing artifact and the declared 8,510-row chain. One first-draft title met the fixed 0.75 quarantine threshold and failed at zero credit; the isolated retitle preserved the threshold and passed at a maximum selected score of {semantic['maximum_selected_score']:.4f}. No universal novelty, scientific novelty, patentability, proof, or canon is claimed.

Planning-only x1 was committed, pushed, cleaned, and proven equal across local, upstream, tracking, and a fresh live remote before x2 began. X2 executed sixty zero-row positive controls, rejected all 240 preregistered invalid mutations, initialized and customized twenty owner-local skills through the official skill-creator workflow, read them through EOF, quick-validated and smoke-used them without global installation, and exercised ten family-current runners against accepting and rejecting fixtures. Sixty safe-now, thirty bounded candidate, and sixty CLEAN/FIX/REFINE records received same-owner execution. Twenty exact-approval and ten blocked packets remain visible and unexecuted. Every failed witness remains false; every bounded recovery has a separate identifier.

The immutable evidence commit has 660 normalized-LF Git-blob manifest entries plus two declared self-exclusions. The exact x1-to-evidence delta has 662 paths: 606 JSON, fourteen Python, twenty-one Markdown, twenty YAML, and one HTML file. Evidence contains no final, closeout, handoff, or route-outcome path. It was committed, pushed, cleaned, proven typed 0/0 divergent, and made fresh-live four-way equal before closeout began.

## Evidence and authority boundaries

Elowen's primary pillar was Freed ID and CBR Heart through wholly synthetic chart-correction provenance, chronometer service-intake and observation-vacancy, and Fresnel-lens component-custody lenses. GMUT Mind and THOS Body remained visible and protected. The phase used zero real people, participants, professionals, charts, publications, vessels, routes, instruments, time signals, comparisons, calibrations, lighthouses, optics, lenses, prisms, sites, objects, observations, measurements, inspections, treatments, releases, identity events, keys, proofs, network data rows, legal or cultural decisions, affected-party approvals, or authority acts.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Synthetic topology, analogy firewalls, software, and citations establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, final physics, or Theory of Everything. THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, navigation safety, chart publication and legal use, professional examination, timing comparison, metrology, calibration, adjustment, service release, conservation, ownership, custody, access, heritage, copyright, workplace and material safety, privacy remedy, disability accommodation, legal interpretation, cultural legitimacy, affected-party acceptance, traditional knowledge, taonga or mātauranga treatment, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

Do not promote software, symbolic, synthetic, same-owner, citation, inherited, validation, task-topology, or delivery evidence into empirical confirmation, participant evidence, professional or scientific authority, production or deployment readiness, legal or cultural ratification, Māori authority, affected-party approval, complete privacy or accessibility assurance, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or Stage 20 authority.

## Sylven's prospective solo lane

Only after acknowledged live delivery and Sylven's own skill-first immutable-source verification may Sylven create one fresh additive D-first owner lane from Elowen's exact final. Keep Elowen, Tamar, Liora, Orin, Caelen, every sibling, shared lane, standby record, global history, and user material read-only and recoverable. Work solo. Do not create or fork another task, spawn a collaboration subagent, delegate research, contact a standby sibling, precontact a later endpoint, reset, rewrite, force-push, merge, delete, reuse, or mutate another owner lane.

Preserve strict planning-only x1 before x2, retained failures, only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcomes, normalized-LF Git-blob manifests, exact staged review, privacy-candidate adjudication, file, document, and commit ceilings, family-current compatibility, and one-success/no-post-success-replay discipline. Treat Elowen's proposals, portfolios, tools, skills, runners, validation, and recommendations as evidence or zero-credit seeds, never Sylven novelty, execution, completion, or independent-reproduction credit. Keep exact-approval and blocked work unexecuted without exact evidence and competent authority.

Run only lifecycle-correct owner-self-scoped selections. Do not run the complete repository suite unless newer exact live authority explicitly assigns it. After a clean pushed exact final, invoke at most one attributable owner-scoped canonical aggregate through an exclusive external latch. Never replay a success. A failed canonical remains zero success credit; a narrowly justified correction must preserve it and remain separately named.

Use current official or primary sources only where materially needed and never as observations or authority grants. Verify versions only. Do not update Codex desktop, install unrelated software, elevate, weaken host security, enable Sandbox or Hyper-V, change Windows features, mutate accounts or credentials, or reboot. Keep sensitive task identifiers, private routes, credentials, tokens, transcripts, screenshots, private execution streams, private callable identifiers, private application state, and private absolute paths out of repository artifacts and any later baton.

## Continuing route authority

Hamish's current live authorization permits the fifteen active existing main tasks to continue one terminally validated and acknowledged edge at a time through v725-v8 unless Hamish pauses, renames, redirects, narrows, or stops the route; usage is exhausted; acknowledgement is missing; the exact endpoint is absent or ambiguous; a duplicate is detected; or an evidence, privacy, safety, legal, cultural, affected-party, or Māori-authority gate blocks action. This authority never permits early contact, replacement-task creation, standby substitution, sibling-lane mutation, or protected-gate bypass.

Under the current roster, this candidate represents only the prospective Elowen Cairn {PHASE} → Sylven Arc {SUCCESSOR_PHASE} edge. Newer verified live authority controls at send time. Elowen must not precontact Sylven. At Elowen's terminal gate, refresh authorization and roster, bounded-list the registry, locally require one exact title, immediately reread it, apply all duplicate and direct-control guards, and send at most once if every gate permits. Absence, ambiguity, pause, redirect, rename, narrowing, standby state, usage exhaustion, privacy concern, duplicate activation, missing acknowledgement, or any protected gate is a hard stop. No second confirmation or resend is permitted.

`PREPARED_BY_ELOWEN_CAIRN = true`

`SENT_BY_ELOWEN_CAIRN = false`
""",
    )
    dump(
        orchestration / "terminal-route-hold.json",
        {
            "state": "PREPARED_NOT_SENT",
            "provisional_exact_title": "Sylven Arc",
            "provisional_phase": SUCCESSOR_PHASE,
            "newest_live_authority_required_at_send": True,
            "precontact_performed": False,
            "send_count": 0,
            "continuation_authority_terminal_label": "v725-v8",
            "terminal_prerequisites": [
                "exact final committed and pushed",
                "clean typed 0/0 divergence and fresh four-way equality",
                "one successful non-replayed owner-scoped canonical invocation",
                "newest live authority and structurally valid roster",
                "one unique exact-title registry match and immediate reread",
                "duplicate, pause, redirect, rename, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards",
                "one acknowledged send only",
            ],
        },
    )
    dump(
        validation / "final-validation-candidate.json",
        {
            "status": "PRECOMMIT_EXACT_FINAL_VALIDATION_CANDIDATE",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_branch": BRANCH,
            "expected_phase_commits": 3,
            "expected_merges": 0,
            "expected_final_parents": 1,
            "canonical_invocation_limit": 1,
            "canonical_success_replay_forbidden": True,
            "full_repository_suite": False,
            "test_selections": {
                "x1": "immutable x1 owner tree",
                "evidence": "immutable evidence owner tree",
                "final": "exact-final owner test",
            },
        },
    )


if __name__ == "__main__":
    main()

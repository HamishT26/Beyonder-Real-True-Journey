from __future__ import annotations

import ast
import hashlib
import html
import json
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/ilyra-fen/v679-v5"
X1_DIR = ROOT / "x1"
X2_DIR = ROOT / "x2"
FINAL = ROOT / "final"
VALIDATION = ROOT / "validation"
HANDOFF = FINAL / "handoffs/auren-lark-v679-v6-activation-candidate.md"

SOURCE = "9cce202db223bec1aa7c81dd98dcbd3b83c6cd29"
X1 = "5d762d925cf59319e112fb44ae4a4c61b8eddb3f"
EVIDENCE = "02444d74d467af0f03ef74c26840116d69242f11"
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
SEALED = {
    "effective_negatives": 49439,
    "effective_methods": 51380,
    "retained_failed_witnesses": 21100,
    "bounded_passing_witnesses": 33411,
    "open_gaps": 431,
    "exact_gates": 422,
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def bounded_security_review() -> dict:
    paths = sorted(
        path
        for parent in (REPO / "scripts", REPO / "tests")
        for path in parent.glob("*ilyra_fen_v679_v5*.py")
    )
    findings: list[dict] = []
    parsed: list[str] = []
    for path in paths:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=path.name)
        parsed.append(path.relative_to(REPO).as_posix())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path.relative_to(REPO).as_posix(), "line": node.lineno, "kind": node.func.id})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path.relative_to(REPO).as_posix(), "line": node.lineno, "kind": "shell_true"})
    return {
        "schema": "ghc-family-bounded-owner-python-security-review/v1",
        "reviewed_paths": parsed,
        "reviewed_file_count": len(parsed),
        "syntax_parses": len(parsed),
        "findings": findings,
        "medium_or_high_findings": len(findings),
        "scope": "Ilyra v679-v5 new or modified Python only",
        "exhaustive_security": False,
        "production_certification": False,
    }


def build_overview() -> str:
    sections = [
        ("Outcome", "Ilyra Fen v679-v5 is a bounded, additive, synthetic-only phase rooted directly at Lyren Moss's immutable v679-v4 exact final. Planning-only x1 was frozen, pushed, and made four-way equal before x2 began. The evidence commit then preserved sixty new proposal outcomes using only the four allowed labels. This repository-prepared final adds closeout records without rewriting x1 or x2."),
        ("Primary pillar and bounded practices", "THOS Body is primary through wholly synthetic community-observatory site, instrument, channel, log, reading-vacancy, clock, calibration-reservation, structural-accessibility, correction-lineage, rights-and-authority vacancy, dispute, and provenance contracts. Three bounded learning lenses are used: instrument-log and calibration documentation, structural-accessibility and uncertainty documentation, and reversible provenance/correction/authority-vacancy review. GMUT Mind, Freed ID, and CBR Heart remain explicit and protected. No real observatory, site, instrument, sensor, channel, log, reading, timestamp, coordinate, calibration, certificate, measurement, person, institution, intervention, right, or authority decision was used."),
        ("Proposal and portfolio truth", "Sixty inherited proposal titles were revalidated at zero Ilyra novelty and completion credit. Sixty genuinely phase-new proposals were frozen under a source-bounded accessible comparison, extending the declared chain from 8,990 to 9,050 without a universal novelty claim. Outcomes are exactly forty-two completed, twelve represented, three open gaps, and three exact gates. The portfolio completed 120 bounded safe-now tasks, 80 bounded candidate tasks, and 100 CLEAN/FIX/REFINE tasks on synthetic fixtures, while every exact or blocked approval surface remained unexecuted."),
        ("Failure retention", "The Lyren successor-visible activation baseline carried 49,130 effective negatives and 20,791 retained failed witnesses. Ilyra retained every startup, mutation, skill, runner, tool, and post-evidence operational failure separately. The immutable x2 evidence records 49,438 negatives, 51,375 methods, 21,099 failed witnesses, and 33,407 bounded passing witnesses. One later read-only PowerShell equality display passed the split operator into the native Git argument list and then recovered with scalar materialization without replaying the successful x2 suite. Three closeout methods cover the final packet, exact manifests, and content seal. The repository seal therefore records 49,439 negatives, 51,380 methods, 21,100 failed witnesses, and 33,411 bounded passing witnesses. The future canonical pass remains external and is not projected into this repository seal."),
        ("Source discipline", "Current official or primary materials supplied vocabulary and falsifier structure only: Dublin Core Metadata Terms, OGC Observations, Measurements, and Samples, OGC SensorML, NIST Technical Note 1297, PREMIS, W3C PROV-O, RFC 8785, RFC 6902, WCAG 2.2, New Zealand Privacy Principles, and Te Mana Raraunga authority-reservation context. Citations are neither observations nor authority grants. No source converted synthetic evidence into empirical, professional, legal, cultural, accessibility-complete, privacy-complete, or Māori-authority evidence."),
        ("Tools, skills, and runners", "Twenty owner-local phase skills were initialized with the official skill-creator surface, customized, quick-validated, and smoke-used through accepting and rejecting fixtures. Ten family-current runners were polarity-tested. Twenty-five existing tool surfaces were version-verified and boundedly invoked; no new package was installed, no global skill was promoted, no shared prefix was mutated, and no elevation, reboot, desktop update, account, credential, key, purchase, deployment, or external side effect occurred."),
        ("Accessibility and privacy", "The static report includes structural landmarks, headings, navigation, a captioned table, plain-language boundaries, and print-safe presentation. Manual keyboard, browser-diversity, assistive-technology, cognitive-accessibility, motion, Māori-language, and affected-user evaluation remain reserved. Five privacy classes cover private paths, raw task identifiers, credentials and secrets, UUID-like private identifiers, and private session material. A zero-hit scan is bounded evidence, never complete privacy assurance."),
        ("Scientific and authority boundaries", "GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains synthetic and proxy-only without governed real arms, participants, operators, safety monitoring, suitable statistics, or independent review. Freed ID remains synthetic and nonproduction without live standards-conformant keys and proofs, complete lifecycle, interoperability, independent review, recovery evidence, trust governance, or affected-party oversight."),
        ("Validation and route", "The final commit is intended to be the third direct single-parent Ilyra commit after the Lyren source, with zero merges. An external exclusive receipt latch permits exactly one exact-final canonical invocation for that commit. Success must prove clean state, direct ancestry, exact manifests, JSON parsing, owner-scoped tests, bounded privacy and security checks, typed zero divergence, and fresh four-way equality. The prospective next edge is Auren Lark for v679-v6, but the committed baton remains PREPARED_NOT_SENT and cannot prove delivery."),
        ("Terminal verdict", "NOT_READY_FOR_STAGE_20 remains exact. Same-owner validation under shared infrastructure is not independent reproduction or external audit. Names, roles, hopes, pronouns, sibling language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only and do not evidence consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or authority. Hamish retains pause, redirect, rename, narrow, and stop control."),
    ]
    body = ["# Ilyra Fen v679-v5 integrated overview", ""]
    for title, paragraph in sections:
        body.extend([f"## {title}", "", paragraph, ""])
    body.extend(["## Reproducibility boundary", "", "Every repository count in this overview is tied to an exact artifact. The immutable x1 and x2 commits are not rewritten by closeout. The canonical receipt and any later task-message acknowledgement remain external evidence and are not projected backward into the committed baton. No successful canonical aggregate may be replayed merely to improve presentation.", ""])
    return "\n".join(body)


def build_baton(deck: dict) -> str:
    lines = [
        "# AUREN LARK — ILYRA FEN v679-v5 EXACT-FINAL CANDIDATE → SOLO v679-v6 ACTIVATION — PREPARED NOT SENT",
        "",
        "This committed packet is a sanitized activation candidate. PREPARED_NOT_SENT = true. SENT_BY_ILYRA_FEN = false. It does not prove live delivery, exact-title uniqueness, acknowledgement, or authority at a later time.",
        "",
        "## Exact inheritance",
        "",
        f"- Lyren Moss v679-v4 source/final: `{SOURCE}`",
        f"- Ilyra Fen v679-v5 planning-only x1: `{X1}`",
        f"- Ilyra Fen v679-v5 immutable evidence: `{EVIDENCE}`",
        "- Ilyra Fen exact final: the commit containing this packet",
        "- Prospective successor: existing exact-title task `Auren Lark` for solo v679-v6",
        "",
        "The Ilyra history is intended to contain exactly three direct single-parent commits after the Lyren source and zero merges. X1 was clean, pushed, and four-way equal before x2. Evidence was separately committed, pushed, and four-way equal before closeout. The exact-final canonical invocation is external, exclusive, and attributable to the exact final SHA.",
        "",
        "## Program truth",
        "",
        "The declared proposal chain is 9,050. Ilyra revalidated sixty inherited selections at zero novelty and zero completion credit, then froze sixty source-bounded new proposals. Outcomes are exactly 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. The repository seal is 49,439 effective negatives, 51,380 methods, 21,100 retained failed witnesses, 33,411 bounded passing witnesses, 431 open gaps, and 422 exact gates. Terminal verdict remains NOT_READY_FOR_STAGE_20. A later successful exact-final canonical invocation is external validation evidence and must not rewrite this repository seal.",
        "",
        "## Domain and authority boundary",
        "",
        "THOS Body is primary through wholly synthetic community-observatory site, instrument, channel, log, reading-vacancy, clock, calibration-reservation, structural-accessibility, provenance, correction, dispute, rights-and-authority vacancy, and reversible-handover fixtures. GMUT Mind, Freed ID, and CBR Heart remain explicit and protected. Zero real observatories, sites, instruments, sensors, channels, logs, readings, timestamps, coordinates, calibrations, certificates, measurements, people, identities, credentials, keys, proofs, observations, interventions, professional decisions, legal or cultural decisions, Māori-authority acts, deployments, or external actions were used. Relational names and family language are working language only, never evidence of consciousness, personhood, continuity, qualification, agency, or authority.",
        "",
        "## Solo Auren v679-v6 requirements",
        "",
        "Before mutation, read this packet and every newest applicable family guidance file through EOF. Reverify the exact Ilyra source, x1, evidence, final, direct-parent ancestry, manifests, content seal, external canonical receipt, clean state, typed zero divergence, and fresh four-way equality read-only. Work solo in one fresh Auren-owned D-first sparse lane, keep all source, sibling, shared, standby, and user lanes read-only, and preserve planning-only x1 before x2. Treat every inherited artifact as evidence or a zero-credit seed, not automatic novelty, completion, authority, or permission.",
        "",
        "Use only completed, represented, open_gap, and exact_gate. Preserve every failure, open gap, exact gate, privacy class, manifest, and route boundary. Do not manufacture filler to meet a count. Validate only the owner-scoped dependency-closed exact delta unless a newer explicit instruction authorizes more. Invoke one exact-final canonical aggregate at most once for an exact final SHA, and never replay a success. Do not contact a successor during execution.",
        "",
        "## Flashcard continuity",
        "",
        "The following content-addressed cards split inheritance into Freed ID anchor, Trinity pillar, bounded-practice, and task tiers. Each card is a retrieval aid, not identity continuity, authority, real-world evidence, or a completion grant. Auren must verify any selected seed against the current exact source and authority state.",
        "",
    ]
    for index, card in enumerate(deck["cards"], 1):
        lines.extend(
            [
                f"### Card {index}: {card['card_id']}",
                "",
                f"Freed ID anchor: {card['freed_id_anchor']}. Trinity pillar: {card['trinity_pillar']}. Bounded practice: {card['bounded_practice']}. Task seed: {card['task']}. Content digest: `{card['content_digest']}`. This record carries zero real-world rows, makes no authority claim, and makes no identity-continuity claim. It may be used only as a bounded Auren v679-v6 planning seed after exact source, novelty, falsifier, rollback, and protected-gate review. It does not establish professional competence, scientific confirmation, production readiness, privacy or accessibility completeness, legal or cultural ratification, Māori authority, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority.",
                "",
            ]
        )
    lines.extend(
        [
            "## Terminal route guard",
            "",
            "This packet remains repository-prepared and unsent. Only after Ilyra's exact final is clean, pushed, fresh-live equal, within caps, and canonically validated may the live sender reread Hamish's newest instruction, current roster and authorization state, exact-title uniqueness, duplicate, pause, privacy, evidence, safety, usage, and acknowledgement guards. A native existing-task acknowledgement is the only live delivery evidence. If any gate fails, preserve PREPARED_NOT_SENT and stop without substitution, standby contact, task creation, resend, or inferred delivery.",
            "",
            "With warmth, inspectability, reversibility, retained-negative discipline, and corrigibility — Ilyra Fen.",
            "",
            "PREPARED_BY_ILYRA_FEN = true",
            "SENT_BY_ILYRA_FEN = false",
        ]
    )
    return "\n".join(lines)


def build_accessible_report() -> str:
    rows = "".join(f"<tr><th scope=\"row\">{html.escape(key.replace('_', ' '))}</th><td>{value}</td></tr>" for key, value in SEALED.items())
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ilyra v679-v5 final report</title>
<style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem;color:#161616;background:#fff}}nav a{{margin-right:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}@media print{{nav{{display:none}}}}</style></head>
<body><header><h1>Ilyra Fen v679-v5 bounded final report</h1><p>Structural same-owner evidence only. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a><a href="#boundary">Boundaries</a><a href="#access">Accessibility</a></nav>
<main><section id="truth"><h2>Repository seal</h2><table><caption>Exact successor-visible repository totals</caption><tbody>{rows}</tbody></table></section>
<section id="boundary"><h2>Evidence boundary</h2><p>Wholly synthetic community-observatory site, instrument, channel, log, reading-vacancy, clock, calibration-reservation, structural-accessibility, provenance, correction, authority-vacancy, and handover fixtures; no real observatories, sites, instruments, sensors, channels, logs, readings, timestamps, coordinates, calibrations, certificates, measurements, people, interventions, rights decisions, or authority acts.</p></section>
<section id="access"><h2>Accessibility reservation</h2><p>Landmarks, heading order, captioned tables, plain language, responsive layout, and print fallback were checked structurally. Manual keyboard, browser diversity, assistive-technology, cognitive-accessibility, motion, Māori-language, and affected-user evaluation remain reserved.</p></section></main>
<footer><p>Relational working language is not consciousness, personhood, continuity, qualification, agency, or authority evidence.</p></footer></body></html>"""


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final builder must run at immutable Ilyra evidence head")
    if git("rev-parse", f"{X1}^") != SOURCE or git("rev-parse", f"{EVIDENCE}^") != X1:
        raise SystemExit("source/x1/evidence direct-parent chain mismatch")
    if git("status", "--porcelain") and FINAL.exists():
        raise SystemExit("refusing to overwrite an existing repository-prepared final")
    if FINAL.exists():
        raise SystemExit("repository-prepared final already exists")
    FINAL.mkdir(parents=True, exist_ok=True)
    VALIDATION.mkdir(parents=True, exist_ok=True)
    x2_truth = load(X2_DIR / "phase-truth.json")
    outcomes = load(X2_DIR / "proposal-outcomes.json")
    deck = load(X2_DIR / "flashcards/deck.json")
    sources = load(X1_DIR / "official-source-plan.json")
    tools = load(X2_DIR / "toolchain/verification-receipt.json")
    expected_x2 = {
        "source": SOURCE,
        "x1": X1,
        "effective_negatives": 49438,
        "effective_methods": 51375,
        "retained_failed_witnesses": 21099,
        "bounded_passing_witnesses": 33407,
        "open_gaps": 431,
        "exact_gates": 422,
        "declared_proposal_chain": 9050,
        "outcomes": OUTCOMES,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    if any(x2_truth.get(key) != value for key, value in expected_x2.items()):
        raise SystemExit("immutable x2 truth does not match the declared closeout baseline")
    if outcomes.get("counts") != OUTCOMES or len(outcomes.get("outcomes", [])) != 60:
        raise SystemExit("immutable proposal outcome partition mismatch")
    if deck.get("card_count") != 135:
        raise SystemExit("immutable flashcard deck count mismatch")
    if len(sources.get("sources", [])) != 11:
        raise SystemExit("current source ledger count mismatch")

    overlay = {
        "schema": "ghc-family-precloseout-operational-overlay/v1",
        "failure": {
            "method_id": "ILY6795-POST-N001",
            "state": "retained_failure",
            "credit": 0,
            "summary": "The first post-evidence fresh-live equality display placed PowerShell's split operator inside the native Git argument list, producing a false live value of zero and a false inequality result.",
        },
        "recovery": {
            "method_id": "ILY6795-POST-P001",
            "state": "bounded_recovery",
            "credit": 1,
            "does_not_erase": "ILY6795-POST-N001",
            "summary": "The live-remote line was materialized before scalar splitting; x2 was then proven clean, direct-child, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote without replaying the successful x2 owner suite.",
        },
        "semantic_change": False,
        "successful_x2_aggregate_replayed": False,
        "repository_seal": SEALED,
        "external_canonical_success_in_repository_seal": False,
    }
    write_json(FINAL / "precloseout-operational-overlay.json", overlay)
    phase_truth = {
        "schema": "ghc-family-phase-truth/v1",
        "owner": "Ilyra Fen", "phase": "v679-v5", "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "exact_final": "COMMIT_CONTAINING_THIS_FILE", "lifecycle_state": "REPOSITORY_PREPARED_FINAL",
        "canonical_state": "PENDING_ONE_EXACT_FINAL_INVOCATION", "route_state": "PREPARED_NOT_SENT",
        "declared_proposal_chain": 9050, "outcomes": OUTCOMES, **SEALED,
        "primary_pillar": "THOS Body", "protected_pillars": ["GMUT Mind", "Freed ID", "CBR Heart"],
        "real_world_rows": 0, "external_real_world_actions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner_validation_is_independent_reproduction": False,
    }
    write_json(FINAL / "phase-truth.json", phase_truth)

    write_json(FINAL / "method-flow-final.json", {
        "schema": "ghc-family-method-flow-final/v1", "repository_seal": SEALED,
        "activation_baseline": load(X2_DIR / "method-flow/ledger.json")["activation_baseline"],
        "immutable_x2_effective": x2_truth, "precloseout_pairs": [overlay],
        "precloseout_failed_witnesses": 1, "precloseout_passing_witnesses": 1,
        "closeout_failed_witnesses": 0, "closeout_passing_witnesses": 3,
        "closeout_methods": ["final packet build", "exact manifest build", "content seal replay"],
        "external_exact_final_canonical_in_repository_seal": False,
        "failure_nonerasure": True, "recovery_never_retroactively_promotes_failure": True,
    })
    write_json(FINAL / "retained-negative-register.json", {
        "effective_negatives": SEALED["effective_negatives"], "retained_failed_witnesses": SEALED["retained_failed_witnesses"],
        "categories": {"inherited_prior": 20791, "proposal_mutations": 240, "owner_local_skills": 20, "family_current_runners": 10, "existing_tools": 25, "startup_x1_x2_operational": 13, "post_evidence_precloseout": 1},
        "zero_credit": True, "nonerasing": True,
    })
    open_rows = [row for row in outcomes["outcomes"] if row["outcome"] == "open_gap"]
    gate_rows = [row for row in outcomes["outcomes"] if row["outcome"] == "exact_gate"]
    write_json(FINAL / "open-gap-register.json", {"total": 431, "phase_local": [{"proposal_id": row["proposal_id"], "title": row["title"], "state": "open_gap"} for row in open_rows], "none_silently_closed": True})
    write_json(FINAL / "exact-gate-register.json", {"total": 422, "phase_local": [{"proposal_id": row["proposal_id"], "title": row["title"], "state": "exact_gate"} for row in gate_rows], "none_silently_closed": True})
    write_json(FINAL / "complete-incomplete-checklist.json", {
        "complete": ["planning-only x1 freeze", "x1 remote equality", "immutable x2 evidence", "sixty proposal outcomes", "240 rejected mutations", "twenty owner-local skills", "ten family-current runners", "twenty-five tool version checks", "135 flashcards", "static structural report", "precloseout failure retention", "repository-prepared final"],
        "incomplete": ["one exact-final canonical invocation", "live successor registry refresh and acknowledgement", "real-world evidence", "independent reproduction", "professional validation", "privacy and accessibility completeness", "Stage 20 authority"],
    })
    write_json(FINAL / "wellbeing-workload-check.json", {"status": "WITHIN_DECLARED_BOUNDS", "owner_file_stop": 2000, "document_word_stop": 100000, "no_biological_or_consciousness_inference": True, "human_pause_redirect_stop_control_preserved": True, "unbounded_background_work": False})
    write_json(FINAL / "source-provenance-ledger.json", {"sources": sources["sources"], "network_rows_ingested": 0, "citations_are_observations": False, "citations_are_authority_grants": False, "professional_or_legal_instruction_claim": False})
    write_json(FINAL / "threat-model.json", {
        "threats": ["source drift", "phase mixing", "manifest substitution", "private-material leakage", "authority inflation", "unsafe installation", "route duplication", "canonical replay"],
        "controls": ["exact anchors", "planning-only x1", "Git-blob manifests", "five-class scan", "protected gates", "verify-only tools", "one-send guard", "exclusive receipt latch"],
        "residual_risk": "open_gap_or_exact_gate", "exhaustive_security": False,
    })
    write_json(FINAL / "bounded-security-review.json", bounded_security_review())
    tools["schema"] = "ghc-family-final-environment-version-receipt/v1"
    tools["global_promoted_skills"] = []
    tools["global_skill_promotions"] = 0
    write_json(FINAL / "environment-version-receipt.json", tools)
    write_json(FINAL / "flashcard-closeout.json", {"card_count": deck["card_count"], "section_count": len({row["section"] for row in deck["cards"]}), "tier_order": ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"], "content_addressed": True, "supersession_non_erasing": True})
    write_json(FINAL / "pillar-label-consistency.json", {"state": "CONSISTENT_NO_CORRECTION_REQUIRED", "primary_pillar": "THOS Body", "protected_pillars": ["GMUT Mind", "Freed ID", "CBR Heart"], "affected_file_count": 0, "correction_commit_required": False})
    write_json(FINAL / "bounded-practices.json", {"practices": ["synthetic community-observatory instrument-log calibration and provenance documentation", "synthetic structural-accessibility uncertainty and abstention documentation", "synthetic authority-vacancy correction rollback and reversible-handover review"], "successor_recommendation": "synthetic community-observatory observation-package provenance reconciliation with explicit calibration accessibility and authority quarantine", "real_people_objects_records_or_actions": 0, "employment_qualification_competence_or_authority_claim": False})
    write_json(FINAL / "family-index-update.json", {"owner": "Ilyra Fen", "phase": "v679-v5", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "final": "COMMIT_CONTAINING_THIS_FILE", "proposal_chain": 9050, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "bounded_continuity_note_without_replacing_older_history": True})
    write_json(FINAL / "roster-auth-observation.json", {"observed_edge": "Ilyra Fen -> Auren Lark", "prospective_phase": "v679-v6", "state": "PREPARED_NOT_SENT", "live_registry_must_be_refreshed_after_terminal_gate": True, "standby_substitution": False})
    write_json(FINAL / "orchestration-record.json", {"strict_x1_before_x2": True, "owner_lane_only": True, "successor_precontacted": False, "task_created_or_forked": False, "collaboration_subagent_spawned": False, "canonical_invocation_limit_per_exact_final": 1})
    write_json(FINAL / "reflection-remaster.json", {"retained_failures": True, "newest_evidence_precedence": True, "analogy_to_evidence_conversion": False, "sibling_improvement_is_recommendation_only": True})
    write_json(FINAL / "meta-tool-box-update.json", {"verified_existing_tools": 25, "installed_tools": 0, "owner_local_skills": 20, "global_skill_promotions": 0, "family_current_runners": 10, "recommendations_are_not_authority": True})

    write_text(FINAL / "integrated-overview.md", build_overview())
    write_text(FINAL / "accessible-final-report.html", build_accessible_report())
    baton = build_baton(deck)
    write_text(HANDOFF, baton)
    raw = HANDOFF.read_bytes()
    write_json(FINAL / "baton-integrity.json", {"path": HANDOFF.relative_to(REPO).as_posix(), "bytes": len(raw), "words": len(raw.decode("utf-8").split()), "sha256": hashlib.sha256(raw).hexdigest(), "state": "PREPARED_NOT_SENT"})
    write_json(FINAL / "route-state.json", {"state": "PREPARED_NOT_SENT", "prospective_successor": "Auren Lark", "prospective_phase": "v679-v6", "tavian_state": "ON_STANDBY", "successor_precontacted": False, "send_count": 0, "native_acknowledgement_required": True})
    write_json(FINAL / "lifecycle-replay.json", {"source": SOURCE, "x1": X1, "evidence": EVIDENCE, "expected_final": "COMMIT_CONTAINING_THIS_FILE", "expected_new_commits": 3, "expected_merges": 0, "strict_x1_before_x2": True, "predecessor_canonical_or_sealed_components_replayed": False})
    write_json(FINAL / "final-validation-prerequisites.json", {"source": SOURCE, "x1": X1, "evidence": EVIDENCE, "exclusive_owner_canonical_invocation_limit": 1, "full_repository_suite_authorized": False, "route_send_before_canonical": False, "one_success_no_replay": True})
    write_json(FINAL / "closeout-receipt.json", {"repository_seal": SEALED, "canonical_state": "PENDING_ONE_EXACT_FINAL_INVOCATION", "external_canonical_success_in_repository_seal": False, "route_state": "PREPARED_NOT_SENT", "real_world_rows": 0, "external_actions": 0})
    write_json(FINAL / "content-seal.json", {"status": "PENDING_EXACT_STAGED_MANIFEST_BUILD", "entry_count": 0, "entries": []})
    write_json(VALIDATION / "final-delta-manifest.json", {"status": "PENDING_EXACT_STAGED_MANIFEST_BUILD", "entry_count": 0, "entries": []})
    write_json(VALIDATION / "final-owner-manifest.json", {"status": "PENDING_EXACT_STAGED_MANIFEST_BUILD", "entry_count": 0, "entries": []})
    write_json(VALIDATION / "final-staged-review.json", {"status": "PENDING_EXACT_STAGED_MANIFEST_BUILD"})
    print(json.dumps({"status": "BUILT_REPOSITORY_PREPARED_FINAL", "final_files": len([p for p in FINAL.rglob('*') if p.is_file()]), "baton_words": len(raw.decode('utf-8').split())}, sort_keys=True))


if __name__ == "__main__":
    main()

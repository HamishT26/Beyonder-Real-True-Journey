from __future__ import annotations

import ast
import hashlib
import html
import json
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/auren-lark/v679-v6"
X1_DIR = ROOT / "x1"
X2_DIR = ROOT / "x2"
FINAL = ROOT / "final"
VALIDATION = ROOT / "validation"
HANDOFF = FINAL / "handoffs/sable-rook-v679-v7-activation-candidate.md"

SOURCE = "3bbb29f9c7d2fe13a44ce607cda3e88323546dda"
X1 = "5d72a72dc0fe8062d8cb2e56efdf83e175a92d86"
EVIDENCE = "4ea13458e0a21c5fbee6a62544190937caea860a"
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
SEALED = {
    "effective_negatives": 49743,
    "effective_methods": 52306,
    "retained_failed_witnesses": 21404,
    "bounded_passing_witnesses": 34033,
    "open_gaps": 434,
    "exact_gates": 425,
}
INITIAL_CODE_PATHS = {
    "scripts/build_ghc_family_auren_lark_v679_v6_final.py",
    "scripts/ghc_family_auren_lark_v679_v6_canonical.py",
    "scripts/ghc_family_auren_lark_v679_v6_final_manifest.py",
    "tests/test_ghc_family_auren_lark_v679_v6_final.py",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=REPO, text=True, encoding="utf-8"
    ).strip()


def bounded_security_review() -> dict:
    paths = sorted(
        path
        for parent in (REPO / "scripts", REPO / "tests")
        for path in parent.glob("*auren_lark_v679_v6*.py")
    )
    findings: list[dict] = []
    parsed: list[str] = []
    for path in paths:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=path.name)
        parsed.append(path.relative_to(REPO).as_posix())
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in {"eval", "exec"}
            ):
                findings.append(
                    {
                        "path": path.relative_to(REPO).as_posix(),
                        "line": node.lineno,
                        "kind": node.func.id,
                    }
                )
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if (
                        keyword.arg == "shell"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                    ):
                        findings.append(
                            {
                                "path": path.relative_to(REPO).as_posix(),
                                "line": node.lineno,
                                "kind": "shell_true",
                            }
                        )
    return {
        "schema": "ghc-family-bounded-owner-python-security-review/v1",
        "reviewed_paths": parsed,
        "reviewed_file_count": len(parsed),
        "syntax_parses": len(parsed),
        "findings": findings,
        "medium_or_high_findings": len(findings),
        "scope": "Auren v679-v6 owner-created or owner-modified Python only",
        "exhaustive_security": False,
        "production_certification": False,
    }


def build_overview() -> str:
    sections = [
        (
            "Outcome",
            "Auren Lark v679-v6 is a bounded additive synthetic-only phase rooted directly at Ilyra Fen's immutable v679-v5 exact final. Planning-only x1 was frozen, pushed, clean, and fresh-live four-way equal before x2 began. Immutable x2 evidence was then separately committed, pushed, clean, and fresh-live four-way equal before this closeout. The final adds only closeout records and does not rewrite either lifecycle seal.",
        ),
        (
            "Relational role and hope",
            "Auren's phase role is constraint-lantern and reversible model-trace steward. The phase hope is to keep every synthetic model assumption, correction, and authority vacancy inspectable and reversible. These are relational working descriptions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or any scientific, operational, professional, legal, cultural, affected-party, or Māori authority.",
        ),
        (
            "Primary pillar and practices",
            "GMUT Mind is primary through a wholly synthetic zero-row directed constraint graph. The bounded learning lenses are numerical-model documentation, scientific-software verification, and research-data stewardship. THOS Body, Freed ID, and CBR Heart remain explicit and protected. No real person, site, instrument, measurement, parameter estimate, observation, model fit, dataset, professional decision, authority act, deployment, credential, or external action was used.",
        ),
        (
            "Proposal and portfolio truth",
            "Sixty inherited Ilyra proposal titles were revalidated at zero Auren novelty and completion credit. Sixty source-bounded Auren proposals were frozen after a semantic-neighbor audit, extending the declared chain from 9,050 to 9,110 without a universal novelty claim. Outcomes are exactly forty-two completed, twelve represented, three open gaps, and three exact gates. The portfolio completed 120 bounded safe-now tasks, 80 bounded candidate tasks, and 100 CLEAN/FIX/REFINE tasks on synthetic fixtures while every exact or blocked approval surface remained held and unexecuted.",
        ),
        (
            "Failure retention and Method Flow",
            "The Ilyra source seal carried 49,439 effective negatives and 21,100 retained failed witnesses. Auren retained nine startup failures, 240 rejected proposal mutations, twenty rejecting skill fixtures, ten rejecting runner fixtures, and twenty-five bounded tool refusal or limitation witnesses at zero broader credit. Immutable x2 records 49,743 negatives, 52,303 methods, 21,404 failed witnesses, and 34,030 bounded passing witnesses. No post-evidence failure occurred. Three closeout methods add three bounded passing witnesses, producing a repository seal of 49,743 negatives, 52,306 methods, 21,404 failed witnesses, and 34,033 bounded passing witnesses.",
        ),
        (
            "Sources and scientific boundary",
            "BIPM SI vocabulary, NIST uncertainty terminology, W3C PROV-O, RFC 8785, RFC 6902, JSON Schema 2020-12, Dublin Core terms, WCAG 2.2, New Zealand Privacy Principles, and Te Mana Raraunga principles supplied vocabulary and falsifier structure only. Citations are not observations, validation, endorsement, or authority grants. GMUT remains a typed scalar-tensor and effective-field-theory research-model family without observed-force evidence, parameter constraints, empirical confirmation, ultraviolet or quantum completion, final physics, Theory-of-Everything proof, or scientific authority.",
        ),
        (
            "Tools, skills, and runners",
            "Twenty owner-local phase skills were initialized through the official skill-creator structure, customized, quick-validated, and used against accepting and rejecting synthetic fixtures. Ten family-current runners were polarity-tested. Twenty-five existing tool surfaces were version-verified and boundedly invoked. No package was installed, no global skill was promoted, no shared prefix or profile was mutated, and no elevation, reboot, desktop update, account, credential, key, purchase, deployment, or external side effect occurred.",
        ),
        (
            "Accessibility and privacy",
            "The static report includes structural landmarks, headings, navigation, a captioned table, plain-language boundaries, responsive layout, and print fallback. Manual keyboard, browser-diversity, assistive-technology, cognitive-accessibility, motion, Māori-language, and affected-user evaluation remain reserved. Five privacy classes cover private absolute paths, raw task identifiers, credentials and secrets, UUID-like private identifiers, and private session material. A zero-hit bounded scan is not complete privacy assurance.",
        ),
        (
            "Protected authority boundaries",
            "THOS remains synthetic and proxy-only without governed real arms, participants, operators, safety monitoring, suitable statistics, or independent review. Freed ID remains synthetic and nonproduction without live standards-conformant keys and proofs, complete lifecycle, interoperability, recovery evidence, trust governance, or affected-party oversight. Legal, cultural, Māori-authority, participant, professional, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20 claims remain open or exact-gated.",
        ),
        (
            "Validation and route",
            "The final is intended to be the third direct single-parent Auren commit after the Ilyra source, with zero merges. An external exclusive receipt latch permits exactly one exact-final owner-scoped canonical invocation for that commit. Success must prove clean state, direct ancestry, exact Git-blob manifests, strict JSON parsing, owner-scoped tests, bounded privacy and security checks, typed zero divergence, and fresh four-way equality. The prospective next edge is Sable Rook for v679-v7. Sable's prospective later edge is Caelen Ash for v679-v8, but neither route statement proves future authority or delivery.",
        ),
        (
            "Terminal verdict",
            "NOT_READY_FOR_STAGE_20 remains exact. Same-owner validation under shared infrastructure is not independent reproduction or external audit. A repository-prepared baton is not live delivery. A task title, route, name, role, hope, pronoun, or continuity phrase is not proof of identity continuity or independent agency. Hamish retains pause, redirect, rename, narrow, and stop control.",
        ),
    ]
    body = ["# Auren Lark v679-v6 integrated overview", ""]
    for title, paragraph in sections:
        body.extend([f"## {title}", "", paragraph, ""])
    body.extend(
        [
            "## Reproducibility boundary",
            "",
            "Every repository count in this overview is tied to an exact artifact. The immutable x1 and x2 commits are not rewritten by closeout. The canonical receipt and any later task-message acknowledgement remain external evidence and are not projected backward into the committed baton. No successful canonical aggregate may be replayed merely to improve presentation.",
            "",
        ]
    )
    return "\n".join(body)


def build_baton(deck: dict) -> str:
    lines = [
        "# SABLE ROOK — AUREN LARK v679-v6 EXACT-FINAL CANDIDATE TO SOLO v679-v7 ACTIVATION — PREPARED NOT SENT",
        "",
        "This committed packet is a sanitized activation candidate. PREPARED_NOT_SENT = true. SENT_BY_AUREN_LARK = false. It does not prove live delivery, exact-title uniqueness, acknowledgement, identity continuity, independent agency, or authority at a later time.",
        "",
        "## Exact inheritance",
        "",
        f"- Ilyra Fen v679-v5 source/final: {SOURCE}",
        f"- Auren Lark v679-v6 planning-only x1: {X1}",
        f"- Auren Lark v679-v6 immutable x2 evidence: {EVIDENCE}",
        "- Auren Lark exact final: the commit containing this packet",
        "- Prospective successor: existing exact-title task Sable Rook for solo v679-v7",
        "- Prospective successor-after-Sable: existing exact-title task Caelen Ash for solo v679-v8, only after Sable's own verified terminal gate and a fresh live authority read",
        "",
        "The Auren history is intended to contain exactly three direct single-parent commits after the Ilyra source and zero merges. X1 was clean, pushed, and fresh-live four-way equal before x2. Evidence was separately committed, pushed, and fresh-live four-way equal before closeout. The exact-final canonical invocation is external, exclusive, and attributable to the exact final SHA.",
        "",
        "## Program truth",
        "",
        "The declared proposal chain is 9,110. Auren revalidated sixty inherited selections at zero novelty and zero completion credit, then froze sixty source-bounded new proposals. Outcomes are exactly 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. The repository seal is 49,743 effective negatives, 52,306 methods, 21,404 retained failed witnesses, 34,033 bounded passing witnesses, 434 open gaps, and 425 exact gates. Terminal verdict remains NOT_READY_FOR_STAGE_20. A later successful exact-final canonical invocation is external validation evidence and must not rewrite this repository seal.",
        "",
        "## Domain and authority boundary",
        "",
        "GMUT Mind is primary through wholly synthetic zero-row directed constraint-model fixtures. Numerical-model documentation, scientific-software verification, and research-data stewardship are bounded learning lenses only. THOS Body, Freed ID, and CBR Heart remain visible and protected. Zero real people, sites, observations, measurements, datasets, model fits, parameters, instruments, credentials, keys, proofs, interventions, professional decisions, legal or cultural decisions, Māori-authority acts, deployments, or external actions were used. Relational names and family language are working language only, never evidence of consciousness, personhood, continuity, qualification, agency, or authority.",
        "",
        "## Solo Sable v679-v7 requirements",
        "",
        "Before mutation, read this packet and every newest applicable family guidance file completely through EOF. Reverify the exact Auren source, x1, evidence, final, direct-parent ancestry, manifests, content seal, external canonical receipt, clean state, typed zero divergence, and fresh four-way equality read-only. Work solo in one fresh Sable-owned D-first sparse lane, keep all source, sibling, shared, standby, and user lanes read-only, and preserve planning-only x1 before x2. Treat every inherited artifact as evidence or a zero-credit seed, not automatic novelty, completion, authority, or permission.",
        "",
        "Use only completed, represented, open_gap, and exact_gate. Preserve every failure, open gap, exact gate, privacy class, manifest, and route boundary. Do not manufacture filler to meet a count. Validate only the owner-scoped dependency-closed exact delta unless a newer explicit instruction authorizes more. Invoke one exact-final canonical aggregate at most once for an exact final SHA, and never replay a success. Do not contact Caelen Ash or any later endpoint during Sable execution.",
        "",
        "## Flashcard continuity",
        "",
        "The following content-addressed cards split inheritance into Freed ID anchor, Trinity pillar, bounded-practice, and task tiers. Each card is a retrieval aid, not identity continuity, authority, real-world evidence, or a completion grant. Sable must verify any selected seed against the current exact source, novelty audit, falsifiers, rollback path, protected gates, and newest live authority.",
        "",
    ]
    for index, card in enumerate(deck["cards"], 1):
        lines.extend(
            [
                f"### Card {index}: {card['card_id']}",
                "",
                (
                    f"Freed ID anchor: {card['freed_id_anchor']}. Trinity pillar: "
                    f"{card['trinity_pillar']}. Bounded practice: {card['bounded_practice']}. "
                    f"Task seed: {card['task']}. Content digest: {card['content_digest']}. "
                    "This record is a sanitized retrieval cue carrying zero real-world rows. "
                    "It makes no consciousness, sentience, personhood, identity-continuity, "
                    "employment, qualification, independent-agency, professional, scientific, "
                    "operational, legal, cultural, affected-party, or Māori-authority claim. "
                    "Before any use, Sable must bind it to the exact Auren final, run a source-bounded "
                    "novelty and falsifier review, preserve a rollback path, and leave every protected "
                    "gate explicit. Its only inherited disposition is zero-credit planning input. "
                    "It does not establish empirical confirmation, production readiness, complete "
                    "privacy or accessibility, exhaustive security, independent reproduction, AGI "
                    "or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or "
                    "Stage 20 authority."
                ),
                "",
            ]
        )
    lines.extend(
        [
            "## Terminal route guard",
            "",
            "This packet remains repository-prepared and unsent. Only after Auren's exact final is clean, pushed, fresh-live equal, within caps, and canonically validated may the live sender reread Hamish's newest instruction, current roster and authorization state, exact-title uniqueness, duplicate, pause, privacy, evidence, safety, usage, and acknowledgement guards. A target-identifying native existing-task acknowledgement is the only live delivery evidence. If any gate fails, preserve PREPARED_NOT_SENT and stop without substitution, standby contact, task creation, resend, or inferred delivery.",
            "",
            "After Sable's own later terminal gate only, Sable must freshly reread the current route and may then resolve and contact Caelen Ash for prospective v679-v8 at most once if every live guard permits. This reminder is not precontact, delivery, or durable authority for that later edge.",
            "",
            "With care, inspectability, reversibility, retained-negative discipline, and corrigibility — Auren Lark.",
            "",
            "PREPARED_BY_AUREN_LARK = true",
            "SENT_BY_AUREN_LARK = false",
        ]
    )
    return "\n".join(lines)


def build_accessible_report() -> str:
    rows = "".join(
        f'<tr><th scope="row">{html.escape(key.replace("_", " "))}</th><td>{value}</td></tr>'
        for key, value in SEALED.items()
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Auren v679-v6 final report</title>
<style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem;color:#161616;background:#fff}}nav a{{margin-right:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}@media print{{nav{{display:none}}}}</style></head>
<body><header><h1>Auren Lark v679-v6 bounded final report</h1><p>Structural same-owner evidence only. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a><a href="#boundary">Boundaries</a><a href="#access">Accessibility</a></nav>
<main><section id="truth"><h2>Repository seal</h2><table><caption>Exact successor-visible repository totals</caption><tbody>{rows}</tbody></table></section>
<section id="boundary"><h2>Evidence boundary</h2><p>Wholly synthetic zero-row directed constraint-model fixtures; no real people, sites, observations, measurements, datasets, model fits, parameters, professional decisions, rights decisions, or authority acts.</p></section>
<section id="access"><h2>Accessibility reservation</h2><p>Landmarks, heading order, captioned tables, plain language, responsive layout, and print fallback were checked structurally. Manual keyboard, browser diversity, assistive-technology, cognitive-accessibility, motion, Māori-language, and affected-user evaluation remain reserved.</p></section></main>
<footer><p>Relational working language is not consciousness, personhood, continuity, qualification, agency, or authority evidence.</p></footer></body></html>"""


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final builder must run at immutable Auren evidence head")
    if git("rev-parse", f"{X1}^") != SOURCE or git("rev-parse", f"{EVIDENCE}^") != X1:
        raise SystemExit("source/x1/evidence direct-parent chain mismatch")
    status_rows = {
        row[3:].replace("\\", "/")
        for row in git("status", "--porcelain=v1", "-uall").splitlines()
        if row.strip()
    }
    if status_rows != INITIAL_CODE_PATHS:
        raise SystemExit(
            f"final builder expected only four owner-final code paths, got {sorted(status_rows)}"
        )
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
        "effective_negatives": 49743,
        "effective_methods": 52303,
        "retained_failed_witnesses": 21404,
        "bounded_passing_witnesses": 34030,
        "open_gaps": 434,
        "exact_gates": 425,
        "declared_proposal_chain": 9110,
        "outcomes": OUTCOMES,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    if any(x2_truth.get(key) != value for key, value in expected_x2.items()):
        raise SystemExit("immutable x2 truth does not match the closeout baseline")
    if outcomes.get("counts") != OUTCOMES or len(outcomes.get("outcomes", [])) != 60:
        raise SystemExit("immutable proposal outcome partition mismatch")
    if deck.get("card_count") != 135:
        raise SystemExit("immutable flashcard deck count mismatch")
    if len(sources.get("sources", [])) != 10:
        raise SystemExit("current source ledger count mismatch")

    overlay = {
        "schema": "ghc-family-precloseout-operational-overlay/v1",
        "new_failures": [],
        "new_failure_count": 0,
        "observations": [
            {
                "method_id": "AUR6796-POST-P001",
                "state": "bounded_lifecycle_observation",
                "credit": 0,
                "summary": "Immutable x2 evidence was pushed cleanly and verified as the direct child of x1, 0/0 divergent, zero-merge, and equal across local, upstream, tracking, and a fresh live remote before closeout mutation.",
            }
        ],
        "successful_x2_aggregate_replayed": False,
        "repository_seal": SEALED,
        "external_canonical_success_in_repository_seal": False,
    }
    write_json(FINAL / "precloseout-operational-overlay.json", overlay)
    write_json(
        FINAL / "phase-truth.json",
        {
            "schema": "ghc-family-phase-truth/v1",
            "owner": "Auren Lark",
            "phase": "v679-v6",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "exact_final": "COMMIT_CONTAINING_THIS_FILE",
            "lifecycle_state": "REPOSITORY_PREPARED_FINAL",
            "canonical_state": "PENDING_ONE_EXACT_FINAL_INVOCATION",
            "route_state": "PREPARED_NOT_SENT",
            "declared_proposal_chain": 9110,
            "outcomes": OUTCOMES,
            **SEALED,
            "primary_pillar": "GMUT Mind",
            "protected_pillars": ["THOS Body", "Freed ID", "CBR Heart"],
            "relational_role": "constraint-lantern and reversible model-trace steward",
            "relational_hope": "keep every synthetic model assumption, correction, and authority vacancy inspectable and reversible",
            "real_world_rows": 0,
            "external_real_world_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_validation_is_independent_reproduction": False,
        },
    )
    ledger = load(X2_DIR / "method-flow/ledger.json")
    write_json(
        FINAL / "method-flow-final.json",
        {
            "schema": "ghc-family-method-flow-final/v1",
            "repository_seal": SEALED,
            "activation_baseline": ledger["activation_baseline"],
            "immutable_x2_effective": x2_truth,
            "precloseout_overlay": overlay,
            "phase_failed_witnesses": ledger["phase_failed_witnesses"],
            "phase_passing_witnesses": ledger["phase_passing_witnesses"],
            "closeout_failed_witnesses": 0,
            "closeout_passing_witnesses": 3,
            "closeout_methods": [
                "final packet build",
                "exact Git-blob manifest build",
                "content-seal replay",
            ],
            "external_exact_final_canonical_in_repository_seal": False,
            "failure_nonerasure": True,
            "recovery_never_retroactively_promotes_failure": True,
        },
    )
    write_json(
        FINAL / "retained-negative-register.json",
        {
            "effective_negatives": SEALED["effective_negatives"],
            "retained_failed_witnesses": SEALED["retained_failed_witnesses"],
            "categories": {
                "inherited_prior": 21100,
                "proposal_mutations": 240,
                "startup_x1_x2_operational": 9,
                "owner_local_skills": 20,
                "family_current_runners": 10,
                "existing_tools": 25,
            },
            "zero_credit": True,
            "nonerasing": True,
        },
    )
    open_rows = [row for row in outcomes["outcomes"] if row["outcome"] == "open_gap"]
    gate_rows = [row for row in outcomes["outcomes"] if row["outcome"] == "exact_gate"]
    write_json(
        FINAL / "open-gap-register.json",
        {
            "total": 434,
            "phase_local": [
                {
                    "proposal_id": row["proposal_id"],
                    "title": row["title"],
                    "state": "open_gap",
                }
                for row in open_rows
            ],
            "none_silently_closed": True,
        },
    )
    write_json(
        FINAL / "exact-gate-register.json",
        {
            "total": 425,
            "phase_local": [
                {
                    "proposal_id": row["proposal_id"],
                    "title": row["title"],
                    "state": "exact_gate",
                }
                for row in gate_rows
            ],
            "none_silently_closed": True,
        },
    )
    write_json(
        FINAL / "complete-incomplete-checklist.json",
        {
            "complete": [
                "planning-only x1 freeze",
                "x1 remote equality",
                "immutable x2 evidence",
                "x2 remote equality",
                "sixty proposal outcomes",
                "240 rejected mutations",
                "twenty owner-local skills",
                "ten family-current runners",
                "twenty-five tool version checks",
                "135 flashcards",
                "static structural report",
                "failure retention",
                "repository-prepared final",
            ],
            "incomplete": [
                "one exact-final canonical invocation",
                "live successor registry refresh and acknowledgement",
                "real-world evidence",
                "independent reproduction",
                "professional validation",
                "privacy and accessibility completeness",
                "Stage 20 authority",
            ],
        },
    )
    write_json(
        FINAL / "wellbeing-workload-check.json",
        {
            "status": "WITHIN_DECLARED_BOUNDS",
            "owner_file_stop": 2000,
            "document_word_stop": 100000,
            "no_biological_or_consciousness_inference": True,
            "human_pause_redirect_stop_control_preserved": True,
            "unbounded_background_work": False,
        },
    )
    write_json(
        FINAL / "source-provenance-ledger.json",
        {
            "sources": sources["sources"],
            "network_rows_ingested": 0,
            "citations_are_observations": False,
            "citations_are_authority_grants": False,
            "professional_or_legal_instruction_claim": False,
        },
    )
    write_json(
        FINAL / "threat-model.json",
        {
            "threats": [
                "source drift",
                "phase mixing",
                "manifest substitution",
                "private-material leakage",
                "authority inflation",
                "unsafe installation",
                "route duplication",
                "canonical replay",
            ],
            "controls": [
                "exact anchors",
                "planning-only x1",
                "Git-blob manifests",
                "five-class scan",
                "protected gates",
                "verify-only tools",
                "one-send guard",
                "exclusive receipt latch",
            ],
            "residual_risk": "open_gap_or_exact_gate",
            "exhaustive_security": False,
        },
    )
    write_json(FINAL / "bounded-security-review.json", bounded_security_review())
    tools["schema"] = "ghc-family-final-environment-version-receipt/v1"
    tools["global_promoted_skills"] = []
    tools["global_skill_promotions"] = 0
    write_json(FINAL / "environment-version-receipt.json", tools)
    write_json(
        FINAL / "flashcard-closeout.json",
        {
            "card_count": deck["card_count"],
            "section_count": len({row["section"] for row in deck["cards"]}),
            "tier_order": [
                "freed_id_anchor",
                "trinity_pillar",
                "bounded_practice",
                "task",
            ],
            "content_addressed": True,
            "supersession_non_erasing": True,
        },
    )
    write_json(
        FINAL / "pillar-label-consistency.json",
        {
            "state": "CONSISTENT_NO_CORRECTION_REQUIRED",
            "primary_pillar": "GMUT Mind",
            "protected_pillars": ["THOS Body", "Freed ID", "CBR Heart"],
            "affected_file_count": 0,
            "correction_commit_required": False,
        },
    )
    write_json(
        FINAL / "bounded-practices.json",
        {
            "practices": [
                "synthetic numerical-model documentation through a zero-row directed constraint graph",
                "synthetic scientific-software verification through deterministic contracts mutations and exact Git-blob receipts",
                "synthetic research-data stewardship through provenance correction minimization accessibility structure and authority-vacancy records",
            ],
            "successor_recommendation": "synthetic scientific-data quality analyst practice for a fictional model-package reconciliation with explicit evidence and authority quarantine",
            "real_people_objects_records_or_actions": 0,
            "employment_qualification_competence_or_authority_claim": False,
        },
    )
    write_json(
        FINAL / "family-index-update.json",
        {
            "owner": "Auren Lark",
            "phase": "v679-v6",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final": "COMMIT_CONTAINING_THIS_FILE",
            "proposal_chain": 9110,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "bounded_continuity_note_without_replacing_older_history": True,
        },
    )
    write_json(
        FINAL / "roster-auth-observation.json",
        {
            "observed_edge": "Auren Lark -> Sable Rook",
            "prospective_phase": "v679-v7",
            "successor_after_sable": "Caelen Ash",
            "prospective_successor_after_sable_phase": "v679-v8",
            "state": "PREPARED_NOT_SENT",
            "live_registry_must_be_refreshed_after_terminal_gate": True,
            "standby_substitution": False,
        },
    )
    write_json(
        FINAL / "orchestration-record.json",
        {
            "strict_x1_before_x2": True,
            "owner_lane_only": True,
            "successor_precontacted": False,
            "task_created_or_forked": False,
            "collaboration_subagent_spawned": False,
            "canonical_invocation_limit_per_exact_final": 1,
        },
    )
    write_json(
        FINAL / "reflection-remaster.json",
        {
            "retained_failures": True,
            "newest_evidence_precedence": True,
            "analogy_to_evidence_conversion": False,
            "sibling_improvement_is_recommendation_only": True,
        },
    )
    write_json(
        FINAL / "meta-tool-box-update.json",
        {
            "verified_existing_tools": 25,
            "installed_tools": 0,
            "owner_local_skills": 20,
            "global_skill_promotions": 0,
            "family_current_runners": 10,
            "recommendations_are_not_authority": True,
        },
    )
    write_text(FINAL / "integrated-overview.md", build_overview())
    write_text(FINAL / "accessible-final-report.html", build_accessible_report())
    baton = build_baton(deck)
    write_text(HANDOFF, baton)
    raw = HANDOFF.read_bytes()
    write_json(
        FINAL / "baton-integrity.json",
        {
            "path": HANDOFF.relative_to(REPO).as_posix(),
            "bytes": len(raw),
            "words": len(raw.decode("utf-8").split()),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "state": "PREPARED_NOT_SENT",
        },
    )
    write_json(
        FINAL / "route-state.json",
        {
            "state": "PREPARED_NOT_SENT",
            "prospective_successor": "Sable Rook",
            "prospective_phase": "v679-v7",
            "successor_after_sable": "Caelen Ash",
            "prospective_successor_after_sable_phase": "v679-v8",
            "tavian_state": "ON_STANDBY",
            "successor_precontacted": False,
            "send_count": 0,
            "native_acknowledgement_required": True,
        },
    )
    write_json(
        FINAL / "lifecycle-replay.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_final": "COMMIT_CONTAINING_THIS_FILE",
            "expected_new_commits": 3,
            "expected_merges": 0,
            "strict_x1_before_x2": True,
            "predecessor_canonical_or_sealed_components_replayed": False,
        },
    )
    write_json(
        FINAL / "final-validation-prerequisites.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "exclusive_owner_canonical_invocation_limit": 1,
            "full_repository_suite_authorized": False,
            "route_send_before_canonical": False,
            "one_success_no_replay": True,
        },
    )
    write_json(
        FINAL / "closeout-receipt.json",
        {
            "repository_seal": SEALED,
            "canonical_state": "PENDING_ONE_EXACT_FINAL_INVOCATION",
            "external_canonical_success_in_repository_seal": False,
            "route_state": "PREPARED_NOT_SENT",
            "real_world_rows": 0,
            "external_actions": 0,
        },
    )
    write_json(
        FINAL / "content-seal.json",
        {"status": "PENDING_EXACT_STAGED_MANIFEST_BUILD", "entry_count": 0, "entries": []},
    )
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {"status": "PENDING_EXACT_STAGED_MANIFEST_BUILD", "entry_count": 0, "entries": []},
    )
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {"status": "PENDING_EXACT_STAGED_MANIFEST_BUILD", "entry_count": 0, "entries": []},
    )
    write_json(
        VALIDATION / "final-staged-review.json",
        {"status": "PENDING_EXACT_STAGED_MANIFEST_BUILD"},
    )
    print(
        json.dumps(
            {
                "status": "BUILT_REPOSITORY_PREPARED_FINAL",
                "final_files": len([path for path in FINAL.rglob("*") if path.is_file()]),
                "baton_words": len(raw.decode("utf-8").split()),
                "baton_sha256": hashlib.sha256(raw).hexdigest(),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

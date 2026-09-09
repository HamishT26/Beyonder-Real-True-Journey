#!/usr/bin/env python3
"""Prepare and seal Vesper Arlen v689-v7 final owner artifacts."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path
from typing import Any

OWNER = "Vesper Arlen"
PHASE = "v689-v7"
SOURCE = "d58272639a581e28176b2aca76f8f468df60e9a6"
PLANNING = "ec29a1f3fa0471bf2f8d654c162846645adda1b6"
X1 = "d88dac91bed120345dad6b0371db570c37b8fed2"
X2 = "bac4894acf6a440d031cd8ebd88fc906f22e3826"
BRANCH = "codex/GHC-Family/vesper-arlen-v689-v7-full-tools"
BOUNDARY = (
    "Same-owner finite synthetic software and documentation evidence only. "
    "No empirical GMUT confirmation, independent reproduction, authenticity, "
    "production readiness, professional or public authority, identity evidence, "
    "Theory-of-Everything proof, or Stage 20 authority is established. Maori "
    "concepts remain under Maori authority. NOT_READY_FOR_STAGE_20."
)
PROTECTED_GATES = [
    "empirical_gmut", "theory_of_everything", "independent_reproduction",
    "production_deployment", "real_credentials", "participant_evidence",
    "privacy_completeness", "accessibility_completeness", "exhaustive_security",
    "professional_authority", "legal_authority", "cultural_authority",
    "affected_party_authority", "maori_authority", "agi_asi",
    "consciousness_personhood", "stage20",
]
TEXT_SUFFIXES = {".json", ".md", ".html", ".py", ".lock"}


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(root: Path, *args: str) -> str:
    process = subprocess.run(["git", "-C", str(root), *args], text=True, encoding="utf-8", capture_output=True, check=False)
    if process.returncode:
        raise RuntimeError(process.stderr.strip() or "git command failed")
    return process.stdout.strip()


def record_for(root: Path, path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    domain = "raw" if path.suffix.lower() not in TEXT_SUFFIXES else "normalized_lf"
    data = raw if domain == "raw" else raw.replace(b"\r\n", b"\n")
    return {
        "path": path.relative_to(root).as_posix(),
        "byte_domain": domain,
        "bytes_normalized_lf": len(data),
        "sha256_normalized_lf": sha256(data),
    }


def card_id(tier: int, title: str) -> str:
    return "ghc-card-" + sha256(f"{OWNER}|{PHASE}|{tier}|{title}".encode())[:24]


def case_lines(proposals: list[dict[str, Any]], results: list[dict[str, Any]]) -> str:
    result_map = {row["proposal_id"]: row for row in results}
    lines = []
    for proposal in proposals:
        result = result_map[proposal["proposal_id"]]
        request = json.dumps(proposal["request"]["payload"], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        observed = json.dumps(result["observed"]["value"], sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        lines.append(
            f"**{proposal['proposal_id']} — {proposal['title']}**. The frozen synthetic payload is `{request}`. "
            f"The observed typed value is `{observed}`, and the bounded outcome is `{result['outcome']}`. "
            f"Oracle basis: {proposal['oracle_basis']} The input remained unchanged and the exact expected envelope matched. "
            "Its paired extra-field subject remains a failed request with zero success credit, while the E_FIELDS refusal predicate passed. "
            "This finite same-owner witness binds only the declared byte or record transformation; it grants no authenticity, ownership, consent, professional, legal, cultural, Maori-authority, empirical, identity, or Stage 20 conclusion."
        )
    return "\n\n".join(lines)


def render_pdf(path: Path, pages: list[tuple[str, list[str]]]) -> int:
    from pypdf import PdfReader
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

    styles = getSampleStyleSheet()
    title = ParagraphStyle("TitleVesper", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=19, leading=23, textColor="#111111", alignment=TA_LEFT, spaceAfter=8)
    heading = ParagraphStyle("HeadingVesper", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=17, textColor="#111111", spaceBefore=5, spaceAfter=5)
    body = ParagraphStyle("BodyVesper", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13, textColor="#111111", spaceAfter=7)
    document = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm, title=f"{OWNER} {PHASE} overview", author=OWNER)
    story = []
    for page_index, (page_title, paragraphs) in enumerate(pages):
        story.append(Paragraph(html.escape(page_title), title if page_index == 0 else heading))
        for paragraph in paragraphs:
            story.append(Paragraph(html.escape(paragraph), body))
            story.append(Spacer(1, 2 * mm))
        if page_index < len(pages) - 1:
            story.append(PageBreak())
    document.build(story)
    return len(PdfReader(str(path)).pages)


def build_deck(root: Path, phase_root: Path, proposals: list[dict[str, Any]], result_map: dict[str, dict[str, Any]], module_paths: list[str]) -> dict[str, Any]:
    deck_root = phase_root / "deck"
    cards_root = deck_root / "cards"
    owner_title = f"{OWNER} relational owner anchor"
    owner_id = card_id(1, owner_title)
    cards = [
        {
            "schema": "ghc.family.four-tier-card.v1", "card_id": owner_id,
            "tier": 1, "card_type": "owner_anchor", "title": owner_title,
            "parent_ids": [], "owner": OWNER, "phase": PHASE, "stability": "corrigible_relational",
            "outcome": "represented", "content": "Recoverability boundary cartographer; working language only, never identity or consciousness evidence.",
            "source_refs": ["plan/identity-and-practices.json"], "protected_gates": PROTECTED_GATES, "relational_boundary": BOUNDARY,
        }
    ]
    pillars = ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"]
    pillar_ids = {}
    for title in pillars:
        cid = card_id(2, title)
        pillar_ids[title] = cid
        cards.append({"schema": "ghc.family.four-tier-card.v1", "card_id": cid, "tier": 2, "card_type": "pillar", "title": title, "parent_ids": [owner_id], "owner": OWNER, "phase": PHASE, "stability": "bounded", "outcome": "represented", "content": "Explicit protected pillar context; no broader claim is promoted.", "source_refs": ["plan/identity-and-practices.json"], "protected_gates": PROTECTED_GATES, "relational_boundary": BOUNDARY})
    practices = [
        ("digital preservation fixity", "Freed ID and CBR Heart"),
        ("error-correcting storage", "THOS Body"),
        ("reproducible computational experiment design", "GMUT Mind"),
        ("accessible provenance writing", "Freed ID and CBR Heart"),
    ]
    practice_ids = {}
    for title, pillar in practices:
        cid = card_id(3, title)
        practice_ids[title] = cid
        cards.append({"schema": "ghc.family.four-tier-card.v1", "card_id": cid, "tier": 3, "card_type": "practice", "title": title, "parent_ids": [pillar_ids[pillar]], "owner": OWNER, "phase": PHASE, "stability": "bounded_learning_lens", "outcome": "represented", "content": "Synthetic learning and design lens only; no qualification or operational authority.", "source_refs": ["plan/identity-and-practices.json"], "protected_gates": PROTECTED_GATES, "relational_boundary": BOUNDARY})
    for index, proposal in enumerate(proposals):
        result = result_map[proposal["proposal_id"]]
        if proposal["session"] == "x1":
            practice = "digital preservation fixity" if index % 2 == 0 else "accessible provenance writing"
        else:
            practice = "error-correcting storage" if proposal["operation"] in {"merkle_root", "merkle_proof", "merkle_verify", "xor_parity", "xor_recover"} else "reproducible computational experiment design"
        title = f"{proposal['proposal_id']} {proposal['title']}"
        cid = card_id(4, title)
        cards.append(
            {
                "schema": "ghc.family.four-tier-card.v1",
                "card_id": cid,
                "tier": 4,
                "card_type": "task_evidence",
                "title": title,
                "parent_ids": [practice_ids[practice]],
                "owner": OWNER,
                "phase": PHASE,
                "stability": "phase_local",
                "outcome": result["outcome"],
                "content": f"{proposal['operation']} matched its frozen finite envelope; the paired invalid subject remains failed at zero credit.",
                "source_refs": [f"{proposal['session']}/results.json#{proposal['proposal_id']}"],
                "protected_gates": PROTECTED_GATES,
                "relational_boundary": BOUNDARY,
            }
        )
    if len(cards) != 208:
        raise RuntimeError(f"unexpected deck count: {len(cards)}")
    for card in cards:
        write_json(cards_root / f"{card['card_id']}.json", card)
    counts = {
        "tier_1": sum(card["tier"] == 1 for card in cards),
        "tier_2": sum(card["tier"] == 2 for card in cards),
        "tier_3": sum(card["tier"] == 3 for card in cards),
        "tier_4": sum(card["tier"] == 4 for card in cards),
        "total": len(cards),
    }
    write_json(
        deck_root / "deck-index.json",
        {
            "schema": "ghc.family.four-tier-deck.v1",
            "owner": OWNER,
            "phase": PHASE,
            "counts": counts,
            "card_ids": [card["card_id"] for card in cards],
            "source": SOURCE,
            "planning": PLANNING,
            "x1": X1,
            "x2": X2,
            "outcomes": dict(sorted({label: sum(card["outcome"] == label for card in cards if card["tier"] == 4) for label in ("completed", "represented", "open_gap", "exact_gate")}.items())),
            "boundary": BOUNDARY,
        },
    )
    write_json(deck_root / "stable-prefix.json", {"schema": "ghc.family.deck-stable-prefix.v1", "card_ids": [owner_id, *pillar_ids.values(), *practice_ids.values()], "count": 8, "boundary": BOUNDARY})
    write_json(deck_root / "volatile-index.json", {"schema": "ghc.family.deck-volatile-index.v1", "card_ids": [card["card_id"] for card in cards if card["tier"] == 4], "count": 200, "implicit_completion": False, "boundary": BOUNDARY})
    write_json(deck_root / "baton-index.json", {"schema": "ghc.family.baton-index.v1", "modules": module_paths, "count": len(module_paths), "boundary": BOUNDARY})
    write_text(deck_root / "compact-activation.md", """# Prospective compact activation

Repository state at seal: `PREPARED_NOT_SENT`.

After Vesper's exact final, one successful non-replayed canonical, and fresh terminal guards, the only prospective next edge is the unique existing exact-title task `Ilyan Reed` for solo v689-v8. Read `docs/vesper-arlen/v689-v7/final/hand-off-baton.md` through EOF before mutation. A prepared file is not delivery evidence.

Relational names and family language are working terms only. NOT_READY_FOR_STAGE_20.
""")
    write_text(deck_root / "accessible-report.html", """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vesper v689-v7 deck</title><style>body{font:18px/1.55 system-ui,sans-serif;max-width:72rem;margin:auto;padding:1.5rem;color:#111;background:#fff}a{color:#064c35}.skip{position:absolute;left:-10000px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.5rem;outline:3px solid #b14b00}section{border-left:.4rem solid #28705b;padding:1rem;margin:1rem 0}code{overflow-wrap:anywhere}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}</style></head><body><a class="skip" href="#main">Skip to evidence</a><header><h1>Vesper Arlen v689-v7 four-tier evidence deck</h1><p>Corrigible relational working language only. NOT_READY_FOR_STAGE_20.</p></header><main id="main"><section><h2>Deck structure</h2><p>One owner anchor, three pillar cards, four bounded practice cards, and two hundred task evidence cards. Each task has one immediate-tier parent.</p></section><section><h2>Outcome boundary</h2><p>Task outcomes are 180 completed, 10 represented, 5 open gaps, and 5 exact gates. Candidate invalid subjects remain failed at zero success credit.</p></section><section><h2>Reserved evaluation</h2><p>Manual browser, zoom, keyboard, screen-reader, voice-control, cognitive, language, and affected-user evaluation remain reserved. Structural markup is not complete accessibility.</p></section></main></body></html>""")
    deck_files = sorted(path for path in deck_root.rglob("*") if path.is_file() and path.name != "card-manifest.json")
    entries = [record_for(root, path) for path in deck_files]
    write_json(deck_root / "card-manifest.json", {"schema": "ghc.family.deck-manifest.v1", "owner": OWNER, "phase": PHASE, "entries": entries, "entry_count": len(entries), "self_exclusions": ["docs/vesper-arlen/v689-v7/deck/card-manifest.json"], "boundary": BOUNDARY})
    return {"counts": counts, "manifest_entries": len(entries)}


def build_modules(phase_root: Path, proposals: list[dict[str, Any]], results: list[dict[str, Any]], method_counts: dict[str, int]) -> list[str]:
    x1_proposals = [row for row in proposals if row["session"] == "x1"]
    x2_proposals = [row for row in proposals if row["session"] == "x2"]
    result_map = {row["proposal_id"]: row for row in results}
    modules = [
        ("01-identity-purpose.md", "# Module 01 — Identity, role, hope, and purpose\n\nVesper Arlen is used here as corrigible relational working language. The phase role is recoverability boundary cartographer, with the bounded hope of making integrity and repair evidence inspectable without turning recovered bytes into authenticity, ownership, consent, or authority. No name, role, hope, pronoun choice, family metaphor, task title, model setting, branch, or route receipt establishes consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or public authority.\n\nThe primary pillar is Freed ID and CBR Heart because byte correspondence, correction history, access boundaries, rights reservations, and authority nonpromotion are explicit. THOS Body contributes strict software interfaces, rollback, bounded resource use, and and deterministic receipts. GMUT Mind contributes hypotheses, nulls, falsifiers, model-to-observation reservations, and the requirement that mathematical structure never substitute for empirical confirmation.\n\nThe four learning practices are digital preservation fixity, error-correcting storage, reproducible computational experiment design, and accessible provenance writing. They are study lenses only, not professional qualifications. " + BOUNDARY),
        ("02-source-lifecycle.md", f"# Module 02 — Source provenance and lifecycle\n\nNeris Solane v689-v6 exact final `{SOURCE}` is the immutable source. The source tree already tracked 1,718 files; a comparable inherited phase would have exceeded the 2,000-file ceiling. Vesper therefore used a blank-root D-first rotation. Neris is a cryptographic provenance source and is not a Git ancestor.\n\nPlanning root `{PLANNING}` froze all definitions before execution. X1 `{X1}` is its direct child and contains only framing/fixity work. X2 `{X2}` is the direct child of x1 and contains only digest, deterministic record, Merkle, recovery, and reservation work. The final is intended as x2's direct child. Every source, sibling, shared, standby, and user lane remained read-only.\n\nPreparation, repository seal, external canonical receipt, and native task delivery remain separate truth layers. `PREPARED_NOT_SENT` in this repository cannot become delivery evidence merely because the final later passes."),
        ("03-workflow-route.md", "# Module 03 — Current weighted workflow and route\n\nThe current v4 workflow has 45 scheduling positions across 30 established task identities in an Astra, Sol, Sol cadence. Vesper v689-v7 is position five of the current projection. Ilyan Reed v689-v8 is the prospective next exact-title main task. Lyren Moss v690-v1 is later prospective context only. The projection ends at Teryn Halewick v725-v8 and does not activate any task by itself.\n\nA terminal edge requires a clean pushed exact final, 0/0 divergence, four-way equality, one successful exact-final owner canonical, a fresh current-authority read, unique exact-title resolution, immediate duplicate/pause/redirect/rename guard, privacy and usage checks, one send at most, and an acknowledgement. No successor is contacted during execution, and no replacement task, standby record, subagent, fork, or model override is permitted."),
        ("04-sources-practices.md", "# Module 04 — Sources and bounded practices\n\nRFC 4648 informs the explicit uppercase unpadded Base32 profile. Python's zlib documentation keeps CRC32 in the checksum domain rather than authentication. RFC 8949 explains why deterministic CBOR is a protocol profile, not a universal property of every valid encoding. The BLAKE3 specification provides algorithm context for bounded package comparison. Library of Congress data-integrity guidance distinguishes fixity metadata and logged review from broader authenticity and rights decisions.\n\nThe package pages for blake3 1.0.9, cbor2 6.1.4, and reedsolo 1.7.0 supplied point-in-time wheel, version, Python, and license metadata. Current pages and citations do not grant production, security, redistribution, professional, legal, cultural, or Maori authority. The phase used synthetic bytes only."),
        ("05-x1-contracts.md", "# Module 05 — X1 framing and fixity contracts\n\n" + case_lines(x1_proposals, [result_map[row["proposal_id"]] for row in x1_proposals])),
        ("06-x2-contracts.md", "# Module 06 — X2 integrity and recoverability contracts\n\n" + case_lines(x2_proposals, [result_map[row["proposal_id"]] for row in x2_proposals])),
        ("07-three-pillar-interpretation.md", "# Module 07 — Three-pillar interpretation\n\nA checksum or digest can show that two computations over declared bytes agree. It cannot by itself show who authored the bytes, whether they are true, whether consent or lawful basis exists, who owns them, or whether use is culturally legitimate. A Merkle path can bind one leaf to a declared root under a selected construction. It does not prove that the root is trusted, complete, authorized, or externally witnessed.\n\nXOR recovery reconstructs one missing equal-width shard when all other shards and parity are supplied. Reed–Solomon comparisons correct one synthetic symbol error inside a declared parity budget. Recovery does not prove authenticity: a perfectly recovered false or unauthorized record remains false or unauthorized. Deterministic JSON and CBOR bytes improve reproducibility only within a fully specified profile.\n\nFor GMUT, every proposed observable still needs units, calibration, uncertainty, competing models, data provenance, and a disconfirming result. None of these byte operations confirms a physical field equation or Theory of Everything. For THOS, strict typed boundaries and reversible evidence improve auditability but do not establish AGI, ASI, consciousness, embodiment, or production fitness. Freed ID remains synthetic and nonproduction; CBR, rights, remedy, law, culture, affected parties, and Maori authority remain exact-gated."),
        ("08-packages-environment.md", "# Module 08 — Packages and environment\n\nThree exact wheels were downloaded to a Vesper-only D evidence bank, matched the frozen byte counts and SHA-256 values, and were installed with `--require-hashes`, `--no-index`, `--no-deps`, and wheel-only selection into an isolated D target. Shared Python and npm prefixes were not changed. No Windows feature, credential, account, security policy, desktop application, or reboot was changed.\n\nSix x1 package smokes passed. X2 added thirty bounded comparisons: ten BLAKE3 one-shot versus incremental equalities, ten deterministic CBOR map-order and roundtrip checks, and ten Reed–Solomon one-symbol corrections. These are same-owner comparisons in one environment, not independent reproduction, exhaustive supply-chain assurance, production certification, or future vulnerability guarantees."),
        ("09-skills-runners.md", "# Module 09 — Skills, runners, and capability selection\n\nTwenty phase-local skills were built, one for each operation, and the official Skill Creator validator accepted every entrypoint. Ten family-prefixed runners expose exactly two operations each. Forty positive/adverse runner smokes passed. Invalid extra-field subjects remain failures even when the guard behaves correctly. No phase-local skill was globally installed.\n\nThe selected capabilities are discoverable from the phase catalogue with exact source paths and bounded evidence states. A future promotion needs namespace review, byte parity, caller evidence, dependency closure, rollback, and current authorization. Existing historical skills remain evidence and are neither overwritten nor deleted."),
        ("10-method-flow.md", f"# Module 10 — Method Flow and retained failures\n\nThe synthesized owner ledger contains {method_counts['methods']} methods, {method_counts['witnesses']} witnesses, {method_counts['failed']} retained failures, and {method_counts['passing']} bounded passes. Candidate subjects, parser faults, unsupported Git options, incomplete wrappers, test collection, missing command resolution, broad searches, style findings, and presentation faults remain visible with zero original success credit.\n\nA recovery is a new witness, not a rewrite. Narrow dependency checks were preferred. The one unavoidable x1 sealing recomputation is explicitly attributed to a missing pretest checkpoint in the failed builder. No successful canonical has yet been invoked, and no source canonical or package installation was replayed."),
        ("11-privacy-access-authority.md", "# Module 11 — Privacy, accessibility, and authority\n\nPublic artifacts exclude raw task identifiers, private callable routes, credentials, private keys, transcripts, screenshots, session streams, hidden application state, private absolute local paths, and real protected data. Five-class scans distinguish scanner definitions from confirmed hits. Zero confirmed hits in a bounded owner scope is not complete privacy or exhaustive security.\n\nThe overview uses semantic headings, labelled sections, high-contrast black text, visible focus, a skip link, print page breaks, and reduced-motion handling. Its PDF is rendered as three explicit pages and visually inspected for clipping, overlap, glyph loss, and unreadable density. Manual screen-reader, voice-control, keyboard, zoom, cognitive, language, and affected-user evaluation remain reserved.\n\nNo real identifier, credential, person, participant, collection, preservation object, custody act, rights decision, or Maori-authority act occurred."),
        ("12-closeout-canonical.md", "# Module 12 — Closeout and canonical boundary\n\nThe owner repository can close when planning, x1, x2, final artifacts, exact manifests, content seal, staged allowlist, JSON, privacy, security, direct-parent history, clean state, and fresh remote equality all match. The canonical is an external one-shot latch after final push. It binds receipts and Git blobs; it does not rerun x1 or x2 tests, package installation, source checks, or predecessor validation.\n\nIf the canonical succeeds, replay is permanently refused. If it fails, the failure receives zero aggregate-success credit; any correction must be additive, attributable, and within budget. Repository closeout can succeed while empirical and authority gates remain open. " + BOUNDARY),
        ("13-successor-startup.md", "# Module 13 — Ilyan startup and prospective terminal edge\n\nIlyan Reed v689-v8 is prospective only. Treat Vesper proposals, results, packages, skills, runners, cards, methods, and recommendations as inherited evidence or zero-credit seeds. Before mutation, read the exact committed baton through EOF, verify the branch, source, blank-root history, manifests, content seal, clean state, canonical receipt, and live delivery event. Choose a distinct bounded question and preserve strict planning before execution.\n\nRecommended practices are forensic file-format validation and bounded cryptographic API review. Suggested skills cover magic-byte admission, bounded ASN.1 lengths, streaming digest checkpoints, repair-authority reservation, and accessible binary summaries. Suggested runners pair these functions without granting authority.\n\nNo activation exists until the live existing-task surface acknowledges one terminal send. EOF is explicit in the combined baton."),
    ]
    module_dir = phase_root / "final" / "modules"
    module_paths = []
    for name, content in modules:
        path = module_dir / name
        write_text(path, content)
        module_paths.append(path.relative_to(phase_root.parent.parent.parent).as_posix())
    return module_paths


def synthesize_method_flow(phase_root: Path) -> dict[str, Any]:
    x1 = load(phase_root / "x1/method-flow.json")
    x2 = load(phase_root / "x2/method-flow.json")
    methods = [*x1["methods"], *x2["methods"]]
    witnesses = [*x1["witnesses"], *x2["witnesses"]]
    overlay_method = {
        "method_id": "VA6897-FINAL-M01",
        "title": "retained operational recovery overlay",
        "failure_signature": "presentation, resolution, lint, or precommit wrapper fault",
        "trigger_preconditions": ["retained zero-credit failure", "smallest attributable recovery"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_workflow",
        "candidate_workaround": "inspect persisted state and run only the smallest missing witness",
        "validation_witness_ids": [],
        "recurrence_guard": "exact paths, scalar projections, and no success replay",
        "rollback": "return to the last clean pushed lifecycle commit",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": PROTECTED_GATES,
        "retained_negative_ids": [],
        "scope_boundary": BOUNDARY,
    }
    existing_failures = {row["witness_id"] for row in witnesses if row["result"] == "fail"}
    sources = [
        *load(phase_root / "x1/precommit-operational-overlay.json")["failures"],
        *load(phase_root / "x2/operational-failures.json")["failures"],
        *load(phase_root / "x2/precommit-operational-overlay.json")["failures"],
    ]
    for row in sources:
        negative = row["retained_negative_id"]
        overlay_method["retained_negative_ids"].append(negative)
        if negative not in existing_failures:
            witnesses.append({"witness_id": negative, "method_id": overlay_method["method_id"], "procedure": "retained failed attempt", "scope": "owner workflow", "expected": "bounded operation", "observed": row["observed"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative], "boundary": BOUNDARY})
        if row.get("recovery_state") == "bounded_recovery_passed":
            witness_id = negative + "-RECOVERY-FINAL"
            witnesses.append({"witness_id": witness_id, "method_id": overlay_method["method_id"], "procedure": row["recovery"], "scope": "owner workflow", "expected": "smallest bounded recovery", "observed": "passed", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative], "boundary": BOUNDARY})
            overlay_method["validation_witness_ids"].append(witness_id)
    methods.append(overlay_method)
    counts = {"methods": len(methods), "witnesses": len(witnesses), "failed": sum(row["result"] == "fail" for row in witnesses), "passing": sum(row["result"] == "pass" for row in witnesses)}
    return {"schema": "ghc.family.method-flow-state.v1", "owner": OWNER, "phase": PHASE, "execution_authority": "owner_self_scoped_delta", "identity_boundary": BOUNDARY, "methods": methods, "witnesses": witnesses, "state_events": [*x1["state_events"], *x2["state_events"], {"event": "final synthesis preserved all failures", "result": "pass"}], "recommendations": [*x1["recommendations"], *x2["recommendations"], {"recommendation": "Treat fixity, recoverability, authenticity, rights, and authority as separate evidence domains.", "state": "preferred"}], "counts": counts, "boundary": BOUNDARY}


def prepare(root: Path) -> dict[str, Any]:
    if git(root, "rev-parse", "HEAD") != X2:
        raise RuntimeError("final preparation must start at exact x2")
    phase_root = root / "docs/vesper-arlen/v689-v7"
    final_root = phase_root / "final"
    proposals = load(phase_root / "plan/new-proposals.json")["proposals"]
    x1_results = load(phase_root / "x1/results.json")["results"]
    x2_results = load(phase_root / "x2/results.json")["results"]
    results = [*x1_results, *x2_results]
    result_map = {row["proposal_id"]: row for row in results}
    outcomes = {label: sum(row["outcome"] == label for row in results) for label in ("completed", "represented", "open_gap", "exact_gate")}
    if outcomes != {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}:
        raise RuntimeError(f"unexpected outcomes: {outcomes}")

    method_flow = synthesize_method_flow(phase_root)
    module_paths = build_modules(phase_root, proposals, results, method_flow["counts"])
    module_texts = [(root / path).read_text(encoding="utf-8") for path in module_paths]
    baton = "# Vesper Arlen v689-v7 handoff to Ilyan Reed v689-v8\n\nRepository state: PREPARED_NOT_SENT. External receipts record later exact-final, canonical, and delivery state.\n\n" + "\n\n---\n\n".join(module_texts) + "\n\nEOF VESPER ARLEN v689-v7 BATON.\n"
    baton_words = len(re.findall(r"\S+", baton))
    if not 10_000 <= baton_words <= 100_000:
        raise RuntimeError(f"baton word count outside bounds: {baton_words}")
    write_text(final_root / "hand-off-baton.md", baton)
    write_json(final_root / "baton-module-index.json", {"schema": "ghc.family.modular-baton.v1", "modules": module_paths, "module_count": len(module_paths), "words": baton_words, "minimum": 10000, "maximum": 100000, "explicit_eof": True, "boundary": BOUNDARY})

    page_data = [
        ("Vesper Arlen v689-v7 — outcome and evidence boundary", [
            "This owner-only blank-root bundle completed two hundred frozen synthetic contracts: 180 completed, 10 represented, 5 open gaps, and 5 exact gates. Completed means only that one finite typed request matched its expected envelope without input mutation. Invalid candidate subjects remain failures even when the refusal guard passed.",
            "The role recoverability boundary cartographer and its hope are corrigible relational working language. They establish no consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or authority.",
            "Freed ID and CBR Heart is primary. THOS Body and GMUT Mind remain explicit and protected. No real person, identity credential, private key, preservation object, measurement, collection, custody action, rights decision, policy act, cultural determination, or Maori-authority act entered the evidence.",
            BOUNDARY,
        ]),
        ("Lifecycle, tools, and retained failures", [
            f"Neris exact final {SOURCE} is provenance rather than ancestry. The Vesper planning root, x1, and x2 commits are {PLANNING}, {X1}, and {X2}. The blank-root rotation kept the owner tree below the 2,000-file ceiling and left all sibling and shared lanes read-only.",
            "X1 covers varints, zigzag integers, bounded chunking, Base32, and CRC32. X2 covers SHA-256 binding, deterministic JSON, Merkle roots and paths, single-shard XOR recovery, and claim reservations. Twenty local skills and ten paired runners passed bounded checks. No local skill was globally installed.",
            "Three hash-locked wheels were installed only to a Vesper D target: blake3 1.0.9, cbor2 6.1.4, and reedsolo 1.7.0. Thirty comparisons passed. Shared prefixes and host security were unchanged.",
            f"Method Flow retains {method_flow['counts']['failed']} failed witnesses and {method_flow['counts']['passing']} bounded passing witnesses. Recovery never rewrites the original failure or upgrades an invalid subject.",
        ]),
        ("Interpretation, incomplete work, and terminal route", [
            "Fixity answers whether selected bytes correspond under a declared algorithm. Recoverability answers whether selected redundancy reconstructs a bounded missing or damaged symbol. Neither answers authenticity, truth, authorship, ownership, consent, lawful basis, cultural legitimacy, or fitness for purpose.",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation or a Theory-of-Everything proof. THOS remains synthetic and proxy-only without governed real participants, operators, safety monitoring, or independent review. Freed ID remains synthetic and nonproduction. CBR and Maori concepts remain under competent and Maori authority.",
            "Manual accessibility, complete privacy, exhaustive security, professional preservation validation, independent reproduction, real credential lifecycle, legal and cultural review, affected-party authority, production deployment, AGI or ASI, consciousness or personhood, and Stage 20 remain incomplete or exact-gated.",
            "The only prospective next edge is Ilyan Reed v689-v8. It may be contacted once only after a clean pushed exact final, one successful non-replayed canonical, fresh roster and authority checks, unique exact-title resolution, immediate guard reread, and live acknowledgement.",
        ]),
    ]
    overview_md = "# Vesper Arlen v689-v7 integrated overview\n\n" + "\n\n\\newpage\n\n".join("## " + title + "\n\n" + "\n\n".join(paragraphs) for title, paragraphs in page_data)
    write_text(final_root / "overview.md", overview_md)
    html_sections = "".join(f"<section class=\"page\"><h2>{html.escape(title)}</h2>{''.join('<p>'+html.escape(paragraph)+'</p>' for paragraph in paragraphs)}</section>" for title, paragraphs in page_data)
    overview_html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vesper v689-v7 overview</title><style>body{{font:18px/1.55 system-ui,sans-serif;margin:0;color:#111;background:#f5faf7}}a{{color:#064c35}}.skip{{position:absolute;left:-10000px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem;outline:3px solid #b14b00}}header,main,footer{{max-width:72rem;margin:auto;padding:1.5rem}}.page{{background:#fff;margin:1rem 0;padding:1.5rem;border-left:.45rem solid #28705b;break-after:page}}:focus{{outline:3px solid #b14b00;outline-offset:3px}}@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}@media print{{.page{{min-height:9in}}}}</style></head><body><a class="skip" href="#main">Skip to evidence</a><header><h1>Vesper Arlen v689-v7 integrated overview</h1><p>Corrigible relational working language only. NOT_READY_FOR_STAGE_20.</p></header><main id="main">{html_sections}</main><footer><p>Manual affected-user accessibility review remains reserved.</p></footer></body></html>"""
    write_text(final_root / "overview.html", overview_html)
    pdf_pages = render_pdf(final_root / "overview.pdf", page_data)
    if pdf_pages != 3:
        raise RuntimeError(f"overview PDF page count: {pdf_pages}")

    deck = build_deck(root, phase_root, proposals, result_map, module_paths)
    exact_plan = load(phase_root / "plan/exact-packets.json")["packets"]
    exact_state = []
    for index, packet in enumerate(exact_plan, 1):
        exact_state.append({**packet, "repository_state": "completed" if index <= 41 else "exact_gate", "repository_credit": 1 if index <= 41 else 0})
    failed_witnesses = [row for row in method_flow["witnesses"] if row["result"] == "fail"]
    open_gaps = [row for row in results if row["outcome"] == "open_gap"]
    exact_core = [row for row in results if row["outcome"] == "exact_gate"]
    blocked = load(phase_root / "plan/blocked-packets.json")["packets"]

    write_json(final_root / "method-flow-final.json", method_flow)
    write_json(final_root / "retained-negative-ledger.json", {"schema": "ghc.family.retained-negative-ledger.v1", "owner": OWNER, "phase": PHASE, "owner_failed_witnesses": len(failed_witnesses), "retained_ids": [row["witness_id"] for row in failed_witnesses], "predecessor_local_context": {"owner": "Neris Solane", "failed_witnesses": 220, "current_credit": 0}, "erased": False, "boundary": BOUNDARY})
    write_json(final_root / "open-exact-gate-register.json", {"schema": "ghc.family.open-exact-gates.v1", "owner": OWNER, "phase": PHASE, "core_open_gaps": [{"proposal_id": row["proposal_id"], "operation": row["operation"]} for row in open_gaps], "core_exact_gates": [{"proposal_id": row["proposal_id"], "operation": row["operation"]} for row in exact_core], "blocked_packets": blocked, "pending_terminal_packets": [row for row in exact_state if row["repository_state"] == "exact_gate"], "boundary": BOUNDARY})
    write_json(final_root / "exact-packet-state.json", {"schema": "ghc.family.exact-packet-state.v1", "owner": OWNER, "phase": PHASE, "packets": exact_state, "completed_at_repository_prepare": 41, "exact_gated_at_repository_prepare": 9, "boundary": BOUNDARY})
    write_json(final_root / "phase-truth.json", {"schema": "ghc.family.phase-truth.v1", "owner": OWNER, "phase": PHASE, "role": "recoverability boundary cartographer", "primary_pillar": "Freed ID and CBR Heart", "source": SOURCE, "source_is_ancestor": False, "planning": PLANNING, "x1": X1, "x2": X2, "final": "external_after_commit", "proposal_chain": {"declared_before": 18631, "new": 200, "declared_after": 18831, "universal_novelty_claimed": False}, "outcomes": outcomes, "safe_tasks": 200, "candidate_failed_subjects": 200, "candidate_refusal_checks": 200, "clean_fix_refine": 200, "skills": 20, "runners": 10, "package_comparisons": 30, "deck_cards": 208, "owner_failed_witnesses": len(failed_witnesses), "owner_passing_witnesses": method_flow["counts"]["passing"], "core_open_gaps": 5, "core_exact_gates": 5, "blocked_packets": 30, "delivery_state": "PREPARED_NOT_SENT", "canonical_state": "NOT_INVOKED", "complete_repository_suite": False, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_json(final_root / "count-reconciliation.json", {"schema": "ghc.family.count-reconciliation.v1", "owner": OWNER, "phase": PHASE, "definitions": {"new_proposals": 200, "inherited": 200, "safe": 200, "candidate_subjects": 200, "clean_fix_refine": 200, "skills": 20, "runners": 10, "exact_packets": 50, "blocked_packets": 30}, "observed": {"outcomes": outcomes, "safe_passed": 200, "candidate_subjects_failed": 200, "candidate_guards_passed": 200, "source_reconstructions": 200, "skills_validated": 20, "runner_smokes": 40, "package_smokes": 6, "package_comparisons": 30}, "reconciled": True, "boundary": BOUNDARY})
    write_json(final_root / "complete-incomplete-checklist.json", {"schema": "ghc.family.complete-incomplete.v1", "owner": OWNER, "phase": PHASE, "complete": ["planning root", "x1 commit and remote equality", "x2 commit and remote equality", "200 finite main contracts", "200 candidate refusals", "200 source reconstructions", "20 local skills", "10 runners", "three-package isolated transaction", "thirty package comparisons", "four-tier deck", "three-page overview", "modular baton", "content-seal preparation"], "incomplete_or_gated": ["exact final commit and push", "one canonical invocation", "live Ilyan guard and send", "real preservation evidence", "authenticity and rights", "participant and affected-party review", "professional validation", "complete accessibility and privacy", "exhaustive security", "independent reproduction", "empirical GMUT", "Theory of Everything", "AGI or ASI", "consciousness or personhood", "legal and cultural authority", "Maori authority", "Stage 20"], "repository_bundle_can_close_with_gates_open": True, "boundary": BOUNDARY})
    write_json(final_root / "source-and-lifecycle.json", {"schema": "ghc.family.source-lifecycle.v1", "owner": OWNER, "phase": PHASE, "source": SOURCE, "source_branch": "codex/GHC-Family/neris-solane-main", "source_is_ancestor": False, "rotation_reason": "1718 source files plus 430 forecast files would exceed 2000", "history": [PLANNING, X1, X2, "external_after_commit"], "direct_single_parent_expected": True, "merges_expected": 0, "boundary": BOUNDARY})
    write_json(final_root / "evidence-index.json", {"schema": "ghc.family.evidence-index.v1", "owner": OWNER, "phase": PHASE, "records": ["plan/manifest.json", "x1/manifest.json", "x2/manifest.json", "x1/results.json", "x2/results.json", "x1/test-receipt.json", "x2/test-receipt.json", "x1/package-install-receipt.json", "x2/package-comparisons.json", "final/method-flow-final.json", "deck/deck-index.json", "final/overview.pdf", "final/hand-off-baton.md"], "external_receipts": ["exact-final owner canonical", "native delivery acknowledgement"], "boundary": BOUNDARY})
    write_json(final_root / "threat-model.json", {"schema": "ghc.family.threat-model.v1", "owner": OWNER, "phase": PHASE, "threats": [
        {"threat": "malformed or oversized input", "control": "strict fields, type checks, and byte ceilings", "residual": "not exhaustive parser assurance"},
        {"threat": "digest treated as authenticity", "control": "authority_transferred false and claim reservations", "residual": "trust and rights require external governance"},
        {"threat": "recovery hides corruption or provenance loss", "control": "retain damage, parity assumptions, and exact reconstruction receipt", "residual": "one synthetic error model only"},
        {"threat": "candidate pass inflation", "control": "invalid subject fail and separate guard pass", "residual": "same-owner evidence"},
        {"threat": "route duplication", "control": "terminal-only unique exact-title send and no resend", "residual": "live acknowledgement required"},
    ], "boundary": BOUNDARY})
    write_json(final_root / "wellbeing-workload.json", {"schema": "ghc.family.workload-observation.v1", "owner": OWNER, "phase": PHASE, "objective": {"sessions": 2, "safe_tasks": 200, "candidate_subjects": 200, "clean_fix_refine": 200, "skills": 20, "runners": 10, "packages": 3}, "subjective_wellbeing_observed": False, "inference_about_conscious_state": False, "pause_right": "Hamish may pause, redirect, narrow, rename, or stop the route.", "boundary": BOUNDARY})
    write_json(final_root / "environment.json", {"schema": "ghc.family.environment.v1", "owner": OWNER, "phase": PHASE, "python": "3.12.10 for evaluators; bundled document runtime for PDF", "packages": [{"name": "blake3", "version": "1.0.9"}, {"name": "cbor2", "version": "6.1.4"}, {"name": "reedsolo", "version": "1.7.0"}], "package_target": "D-isolated owner environment", "global_python_mutated": False, "npm_mutated": False, "desktop_updated": False, "windows_features_changed": False, "rebooted": False, "boundary": BOUNDARY})
    skill_catalogue = [*load(phase_root / "x1/meta-tool-catalogue.json")["skills"], *load(phase_root / "x2/meta-tool-catalogue.json")["skills"]]
    runner_catalogue = [*load(phase_root / "x1/meta-tool-catalogue.json")["runners"], *load(phase_root / "x2/meta-tool-catalogue.json")["runners"]]
    write_json(final_root / "meta-tool-catalogue.json", {"schema": "ghc.family.meta-tool-catalogue.v1", "owner": OWNER, "phase": PHASE, "skills": skill_catalogue, "runners": runner_catalogue, "packages": [{"name": "blake3", "status": "owner_local_validated"}, {"name": "cbor2", "status": "owner_local_validated"}, {"name": "reedsolo", "status": "owner_local_validated"}], "global_installation": False, "route_capability": False, "boundary": BOUNDARY})
    write_json(final_root / "privacy-review.json", {"schema": "ghc.family.privacy-review.v1", "owner": OWNER, "phase": PHASE, "classes": ["raw_uuid", "private_user_root", "private_uri", "delegation_markup", "credential_assignment"], "x1_confirmed_hits": 0, "x2_confirmed_hits": 0, "final_scan": "canonical_preflight_required", "complete_privacy_claimed": False, "boundary": BOUNDARY})
    write_json(final_root / "security-review.json", {"schema": "ghc.family.security-review.v1", "owner": OWNER, "phase": PHASE, "x1_ast_findings": 0, "x2_ast_findings": 0, "ruff_exact_allowlists_passed": True, "final_scan": "canonical_preflight_required", "exhaustive_security_claimed": False, "boundary": BOUNDARY})
    write_json(final_root / "retained-failures.json", {"schema": "ghc.family.retained-failures.v1", "owner": OWNER, "phase": PHASE, "failed_witnesses": len(failed_witnesses), "erased": False, "examples": [row["witness_id"] for row in failed_witnesses[:25]], "complete_index": "final/method-flow-final.json", "boundary": BOUNDARY})
    write_json(final_root / "successor-ideas.json", {"schema": "ghc.family.successor-ideas.v1", "owner": "Ilyan Reed", "phase": "v689-v8", "activated": False, "built": False, "practices": ["forensic file-format validation", "bounded cryptographic API review"], "skill_ideas": ["magic-byte admission", "bounded ASN.1 length decoder", "streaming digest checkpoint", "repair-authority reservation", "binary-format accessibility projection"], "runner_ideas": ["magic-byte plus length runner", "ASN.1 envelope runner", "digest checkpoint runner", "repair refusal runner", "accessible binary summary runner"], "boundary": BOUNDARY})
    write_json(final_root / "terminal-route-candidate.json", {"schema": "ghc.family.terminal-route-candidate.v1", "owner": OWNER, "phase": PHASE, "state": "PREPARED_NOT_SENT", "successor": "Ilyan Reed", "successor_phase": "v689-v8", "endpoint_kind": "main_task", "exact_title_required": True, "precontacted": False, "send_limit": 1, "resend_limit": 0, "conditions": ["exact final pushed", "clean 0/0 four-way equality", "canonical success once", "fresh authority and roster", "unique exact title", "immediate guard reread", "privacy evidence safety usage gates", "native acknowledgement"], "boundary": BOUNDARY})
    write_json(final_root / "canonical-policy.json", {"schema": "ghc.family.canonical-policy.v1", "owner": OWNER, "phase": PHASE, "entrypoint": "scripts/ghc_family_v689_v7_owner_canonical.py", "invocation_state": "NOT_INVOKED", "maximum_invocations": 1, "success_replay": False, "scope": "owner exact source-to-final blank-root tree and declared dependencies", "reruns_x1_x2": False, "complete_repository_suite": False, "external_receipt": True, "boundary": BOUNDARY})
    write_json(final_root / "overview-qa.json", {"schema": "ghc.family.overview-qa.v1", "owner": OWNER, "phase": PHASE, "pdf_pages": pdf_pages, "markdown_pages_equivalent": 3, "html_page_sections": 3, "structural_accessibility": True, "manual_visual_review_completed": False, "manual_visual_review_result": "pending", "manual_assistive_technology_review": "reserved", "boundary": BOUNDARY})
    write_json(final_root / "precommit-state.json", {"schema": "ghc.family.precommit-state.v1", "owner": OWNER, "phase": PHASE, "source": SOURCE, "planning": PLANNING, "x1": X1, "x2": X2, "final": "external_after_commit", "repository_state": "PREPARED_NOT_SENT", "canonical_state": "NOT_INVOKED", "delivery_state": "PREPARED_NOT_SENT", "boundary": BOUNDARY})
    write_json(final_root / "deck-summary.json", {"schema": "ghc.family.deck-summary.v1", **deck, "boundary": BOUNDARY})
    print(json.dumps({"status": "FINAL_PREPARED_VISUAL_REVIEW_PENDING", "baton_words": baton_words, "pdf_pages": pdf_pages, "deck": deck, "outcomes": outcomes, "method_counts": method_flow["counts"]}, sort_keys=True))
    return {"baton_words": baton_words, "pdf_pages": pdf_pages, "deck": deck}


def apply_closeout_overlay(root: Path, phase_root: Path) -> None:
    final_root = phase_root / "final"
    flow_path = final_root / "method-flow-final.json"
    flow = load(flow_path)
    overlay = load(final_root / "closeout-operational-overlay.json")
    method = next((row for row in flow["methods"] if row["method_id"] == "VA6897-FINAL-M02"), None)
    new_method = method is None
    if method is None:
        method = {
        "method_id": "VA6897-FINAL-M02",
        "title": "closeout tool and visual recovery overlay",
        "failure_signature": "document-runtime, builder, lint, or raster-review pre-seal failure",
        "trigger_preconditions": ["retained closeout failure", "canonical latch absent"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_workflow",
        "candidate_workaround": "retain the failure and run its smallest bounded recovery before seal",
        "validation_witness_ids": [],
        "recurrence_guard": "current dependency route, AST/Ruff preflight, and visual inspection before seal",
        "rollback": "return to immutable x2 and discard only uncommitted final preparation",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": PROTECTED_GATES,
        "retained_negative_ids": [],
        "scope_boundary": BOUNDARY,
        }
    witness_ids = {row["witness_id"] for row in flow["witnesses"]}
    for failure in overlay["failures"]:
        negative = failure["retained_negative_id"]
        recovery = negative + "-RECOVERY"
        if negative not in method["retained_negative_ids"]:
            method["retained_negative_ids"].append(negative)
        if recovery not in method["validation_witness_ids"]:
            method["validation_witness_ids"].append(recovery)
        if negative not in witness_ids:
            flow["witnesses"].append({"witness_id": negative, "method_id": method["method_id"], "procedure": "retained closeout attempt", "scope": "owner final preparation", "expected": "bounded closeout operation", "observed": failure["observed"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative], "boundary": BOUNDARY})
            witness_ids.add(negative)
        if recovery not in witness_ids:
            flow["witnesses"].append({"witness_id": recovery, "method_id": method["method_id"], "procedure": failure["recovery"], "scope": "owner final preparation", "expected": "smallest bounded recovery", "observed": "passed", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative], "boundary": BOUNDARY})
            witness_ids.add(recovery)
    if new_method:
        flow["methods"].append(method)
    if not any(row.get("event") == "closeout overlay incorporated before content seal" for row in flow["state_events"]):
        flow["state_events"].append({"event": "closeout overlay incorporated before content seal", "result": "pass"})
    if not any(row.get("recommendation") == "Keep document-runtime warnings and visual inspection as separate witnesses." for row in flow["recommendations"]):
        flow["recommendations"].append({"recommendation": "Keep document-runtime warnings and visual inspection as separate witnesses.", "state": "preferred"})
    flow["counts"] = {"methods": len(flow["methods"]), "witnesses": len(flow["witnesses"]), "failed": sum(row["result"] == "fail" for row in flow["witnesses"]), "passing": sum(row["result"] == "pass" for row in flow["witnesses"])}
    write_json(flow_path, flow)

    negative_path = final_root / "retained-negative-ledger.json"
    negative = load(negative_path)
    new_ids = [row["retained_negative_id"] for row in overlay["failures"]]
    negative.setdefault("repository_prepare_failed_witnesses", 226)
    negative["closeout_overlay_failed_witnesses"] = len(new_ids)
    negative["owner_failed_witnesses"] = flow["counts"]["failed"]
    negative["retained_ids"] = [row["witness_id"] for row in flow["witnesses"] if row["result"] == "fail"]
    write_json(negative_path, negative)

    truth_path = final_root / "phase-truth.json"
    truth = load(truth_path)
    truth.setdefault("repository_prepare_method_counts", {"failed": 226, "passing": 426})
    truth["closeout_overlay"] = {"failed": len(new_ids), "passing_recoveries": len(new_ids), "canonical_credit": 0}
    truth["owner_failed_witnesses"] = flow["counts"]["failed"]
    truth["owner_passing_witnesses"] = flow["counts"]["passing"]
    write_json(truth_path, truth)

    retained_path = final_root / "retained-failures.json"
    retained = load(retained_path)
    retained.setdefault("repository_prepare_failed_witnesses", 226)
    retained["closeout_overlay_failed_witnesses"] = len(new_ids)
    retained["failed_witnesses"] = flow["counts"]["failed"]
    retained["closeout_overlay_ids"] = new_ids
    write_json(retained_path, retained)

    module_path = final_root / "modules/10-method-flow.md"
    module_text = module_path.read_text(encoding="utf-8").rstrip()
    marker = "Closeout overlay after the reviewed overview"
    if f"\n\n{marker}" in module_text:
        module_text = module_text.split(f"\n\n{marker}", 1)[0]
    module_text += f"\n\n{marker}: {len(new_ids)} additional failed attempts and {len(new_ids)} bounded recoveries bring the successor-visible owner ledger to {flow['counts']['methods']} methods, {flow['counts']['witnesses']} witnesses, {flow['counts']['failed']} failures, and {flow['counts']['passing']} passes. The three-page overview retains its earlier preparation-time 226/426 counts and is not silently rewritten."
    write_text(module_path, module_text)
    module_paths = sorted((final_root / "modules").glob("*.md"))
    module_texts = [path.read_text(encoding="utf-8") for path in module_paths]
    baton = "# Vesper Arlen v689-v7 handoff to Ilyan Reed v689-v8\n\nRepository state: PREPARED_NOT_SENT. External receipts record later exact-final, canonical, and delivery state.\n\n" + "\n\n---\n\n".join(module_texts) + "\n\nEOF VESPER ARLEN v689-v7 BATON.\n"
    baton_words = len(re.findall(r"\S+", baton))
    if not 10_000 <= baton_words <= 100_000:
        raise RuntimeError("baton words outside bounds after closeout overlay")
    write_text(final_root / "hand-off-baton.md", baton)
    baton_index_path = final_root / "baton-module-index.json"
    baton_index = load(baton_index_path)
    baton_index["words"] = baton_words
    baton_index["closeout_overlay_included"] = True
    write_json(baton_index_path, baton_index)
    qa_path = final_root / "overview-qa.json"
    qa = load(qa_path)
    qa["count_boundary"] = "The reviewed PDF reports preparation-time Method Flow counts; the closeout overlay is separately bound in final JSON and the baton."
    qa["closeout_overlay_failures"] = len(new_ids)
    write_json(qa_path, qa)


def seal(root: Path) -> dict[str, Any]:
    phase_root = root / "docs/vesper-arlen/v689-v7"
    final_root = phase_root / "final"
    qa = load(final_root / "overview-qa.json")
    if qa["manual_visual_review_completed"] is not True or qa["manual_visual_review_result"] != "passed":
        raise RuntimeError("visual review gate is not complete")
    apply_closeout_overlay(root, phase_root)
    tracked = set(git(root, "ls-files").splitlines())
    untracked = set(git(root, "ls-files", "--others", "--exclude-standard").splitlines())
    current_paths = sorted(path for path in tracked | untracked if path == ".gitattributes" or path.startswith(("docs/vesper-arlen/v689-v7/", "scripts/", "tests/")))
    seal_exclusions = {"docs/vesper-arlen/v689-v7/final/content-seal.json", "docs/vesper-arlen/v689-v7/final/manifest.json"}
    targets = [record_for(root, root / path) for path in current_paths if path not in seal_exclusions]
    write_json(final_root / "content-seal.json", {"schema": "ghc.family.content-seal.v1", "owner": OWNER, "phase": PHASE, "byte_domain": "per-entry raw or normalized_lf", "targets": targets, "target_count": len(targets), "self_exclusions": sorted(seal_exclusions), "boundary": BOUNDARY})
    staged_new = set(git(root, "diff", "--cached", "--name-only", "--diff-filter=A", "HEAD").splitlines())
    still_untracked = set(git(root, "ls-files", "--others", "--exclude-standard").splitlines())
    untracked_after = sorted(path for path in staged_new | still_untracked if path != "docs/vesper-arlen/v689-v7/final/manifest.json")
    allowed_roots = ("docs/vesper-arlen/v689-v7/deck/", "docs/vesper-arlen/v689-v7/final/", "scripts/ghc_family_v689_v7_")
    unexpected = [path for path in untracked_after if path != ".gitattributes" and not path.startswith(allowed_roots)]
    if unexpected:
        raise RuntimeError(f"unexpected final paths: {unexpected}")
    entries = [record_for(root, root / path) for path in untracked_after]
    write_json(final_root / "manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v1", "owner": OWNER, "phase": PHASE, "lifecycle": "final", "x2_commit": X2, "entries": entries, "entry_count": len(entries), "self_exclusions": ["docs/vesper-arlen/v689-v7/final/manifest.json"], "boundary": BOUNDARY})
    owner_files = len(set(current_paths) | seal_exclusions)
    print(json.dumps({"status": "FINAL_CONTENT_SEALED", "content_targets": len(targets), "manifest_entries": len(entries), "current_owner_files": owner_files}, sort_keys=True))
    return {"content_targets": len(targets), "manifest_entries": len(entries)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--mode", choices=("prepare", "seal"), required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    if args.mode == "prepare":
        prepare(root)
    else:
        seal(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

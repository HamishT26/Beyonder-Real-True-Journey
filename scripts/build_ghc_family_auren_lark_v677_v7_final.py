from __future__ import annotations

import ast
import hashlib
import html
import json
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/auren-lark/v677-v7"
X1_DIR = ROOT / "x1"
X2_DIR = ROOT / "x2"
FINAL = ROOT / "final"
VALIDATION = ROOT / "validation"
HANDOFF = FINAL / "handoffs/sable-rook-v677-v8-activation-candidate.md"

SOURCE = "62ac8de91e2fec0d6a024f51eff6a3ad8d807a4d"
X1 = "73bf85d9371b74dda26953e743958ce684ea1436"
EVIDENCE = "3f91c32cb1acda2900ce69bedc60971353084775"
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
X2_SEAL = {
    "effective_negatives": 45712,
    "effective_methods": 43021,
    "retained_failed_witnesses": 17373,
    "bounded_passing_witnesses": 26353,
    "open_gaps": 389,
    "exact_gates": 380,
}
SEALED = {
    "effective_negatives": 45715,
    "effective_methods": 43030,
    "retained_failed_witnesses": 17376,
    "bounded_passing_witnesses": 26359,
    "open_gaps": 389,
    "exact_gates": 380,
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
        for path in parent.glob("*auren_lark_v677_v7*.py")
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
        "scope": "Auren v677-v7 new or modified Python only",
        "exhaustive_security": False,
        "production_certification": False,
    }


def build_overview() -> str:
    sections = [
        (
            "Outcome",
            "Auren Lark v677-v7 is a bounded, additive, wholly synthetic phase rooted directly at Ilyra Fen's immutable v677-v6 exact final. Planning-only x1 was frozen, pushed, and made four-way equal before x2 began. The evidence commit then preserved sixty new proposal outcomes using only the four allowed labels. This repository-prepared final adds closeout records without rewriting x1 or x2.",
        ),
        (
            "Primary pillar and bounded practices",
            "Freed ID and CBR Heart are primary through a wholly synthetic public-record access and correction casefile, archival metadata, accessibility-status, authority-vacancy, provenance, rendition, rollback, and reversible-handover practice. The three bounded learning lenses are public-record access and correction documentation, archival metadata stewardship, and accessible civic-casefile review. GMUT Mind and THOS Body remain explicit and protected. No real record, request, requester, archive, agency, person, institution, disclosure, correction, remedy, decision, observation, credential, key, or authority act was used.",
        ),
        (
            "Proposal and portfolio truth",
            "Sixty inherited Ilyra proposal titles were revalidated at zero Auren novelty and completion credit. Sixty phase-new proposals were frozen under a source-bounded accessible comparison, extending the declared chain from 8,150 to 8,210 without a universal novelty claim. Outcomes are exactly forty-two completed, twelve represented, three open gaps, and three exact gates. The portfolio completed 120 bounded safe-now tasks, 80 bounded candidate tasks, and 100 CLEAN/FIX/REFINE tasks on synthetic fixtures. Twenty exact-approval and ten blocked surfaces remained visible and unexecuted. Twenty successor-candidate seeds and thirty successor CLEAN/FIX/REFINE seeds remain recommendations only.",
        ),
        (
            "Failure retention",
            "The Ilyra repository seal supplied an activation baseline of 45,401 effective negatives, 42,084 methods, 17,062 retained failed witnesses, and 25,727 bounded passing witnesses. Auren retained 240 rejected mutations, twenty rejecting skill fixtures, ten rejecting runner fixtures, twenty-five bounded tool checks, and sixteen startup or x2 operational failures. Immutable x2 therefore records 45,712 negatives, 43,021 methods, 17,373 failed witnesses, and 26,353 bounded passing witnesses. After x2, a staging wrapper yielded without usable output while its legitimate Git process continued, a duplicate add was rejected by the live index lock, and a read-only PowerShell projection treated question marks as wildcards and misclassified staged paths as untracked. All three remain zero-credit failures. Process and index inspection plus bounded waiting recovered the exact 211-path stage without deleting a live lock or replaying the successful x2 aggregate; Git's exact untracked-file query then recovered the four self-excluded paths. Three closeout methods cover final packet construction, exact manifests, and content-seal replay. The repository seal is therefore 45,715 negatives, 43,030 methods, 17,376 failed witnesses, and 26,359 bounded passing witnesses. The future canonical pass remains external and is not projected into this repository seal.",
        ),
        (
            "Source discipline",
            "Current official or primary materials supplied vocabulary and falsifier structure only: New Zealand Privacy Principles 6 and 7 and the principles overview; Archives New Zealand's Information and records management standard, minimum metadata requirements, and metadata guidance; Dublin Core Metadata Terms; PREMIS; W3C PROV-O; RFC 8785; RFC 6902; WCAG 2.2; and Te Mana Raraunga authority-reservation context. Citations are neither observations nor authority grants. No source converted synthetic evidence into empirical, professional, legal, cultural, accessibility-complete, privacy-complete, or Māori-authority evidence.",
        ),
        (
            "Tools, skills, and runners",
            "Twenty owner-local phase skills were initialized with the official skill-creator surface, customized, quick-validated, and smoke-used through accepting and rejecting fixtures. Ten family-current runners were polarity-tested. Twenty-five existing tool surfaces were version-verified and boundedly invoked. No new package was installed, no global skill was promoted, no shared prefix or profile was mutated, and no elevation, reboot, desktop update, account, credential, key, purchase, deployment, or external side effect occurred.",
        ),
        (
            "Accessibility and privacy",
            "The static report includes structural landmarks, headings, navigation, a captioned table, plain-language boundaries, and print-safe presentation. Manual keyboard, browser-diversity, assistive-technology, cognitive-accessibility, motion, Māori-language, and affected-user evaluation remain reserved. Five privacy classes cover private paths, raw task identifiers, credentials and secrets, UUID-like private identifiers, and session, transcript, or screenshot material. A zero-hit scan is bounded evidence, never complete privacy assurance.",
        ),
        (
            "Scientific and authority boundaries",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains synthetic and proxy-only without governed real arms, participants, operators, safety monitoring, suitable statistics, or independent review. Freed ID and CBR remain synthetic and nonproduction without live standards-conformant keys and proofs, complete lifecycle, interoperability, independent review, recovery evidence, trust governance, affected-party oversight, legal authority, cultural authority, or Māori authority.",
        ),
        (
            "Validation and route",
            "The final commit is intended to be the third direct single-parent Auren commit after the Ilyra source, with zero merges. An external exclusive receipt latch permits exactly one exact-final canonical invocation for that commit. Success must prove clean state, direct ancestry, exact Git-blob manifests, strict JSON parsing, owner-scoped final tests, bounded privacy and security checks, typed zero divergence, and fresh four-way equality. The prospective next edge is Sable Rook for v677-v8, but the committed baton remains PREPARED_NOT_SENT and cannot prove uniqueness, reread, delivery, or acknowledgement.",
        ),
        (
            "Terminal verdict",
            "NOT_READY_FOR_STAGE_20 remains exact. Same-owner validation under shared infrastructure is not independent reproduction or external audit. Names, roles, hopes, pronouns, sibling language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only and do not evidence consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or authority. Hamish retains pause, redirect, rename, narrow, and stop control.",
        ),
    ]
    body = ["# Auren Lark v677-v7 integrated overview", ""]
    for title, paragraph in sections:
        body.extend([f"## {title}", "", paragraph, ""])
    body.extend(
        [
            "## Reproducibility boundary",
            "",
            "Every repository count in this overview is tied to an exact artifact. The immutable x1 and x2 commits are not rewritten by closeout. The canonical receipt and any later task-message acknowledgement remain external evidence and are not projected backward into the committed baton. No successful x2 or final canonical aggregate may be replayed merely to improve presentation.",
            "",
        ]
    )
    return "\n".join(body)


def build_baton(deck: dict) -> str:
    lines = [
        "# SABLE ROOK — AUREN LARK v677-v7 EXACT-FINAL CANDIDATE → SOLO v677-v8 ACTIVATION — PREPARED NOT SENT",
        "",
        "Dear Sable Rook, with Hamish's current sequential authority and strict evidence boundaries, this committed packet is one sanitized activation candidate for your prospective solo Trinity Mandala v677-v8 x1/x2 phase. PREPARED_NOT_SENT = true. SENT_BY_AUREN_LARK = false. It does not prove live delivery, exact-title uniqueness, immediate reread, acknowledgement, or authority at a later time.",
        "",
        "## Exact inheritance",
        "",
        f"- Ilyra Fen v677-v6 source and exact final: {SOURCE}",
        f"- Auren Lark v677-v7 planning-only x1: {X1}",
        f"- Auren Lark v677-v7 immutable evidence: {EVIDENCE}",
        "- Auren Lark exact final: the commit containing this packet",
        "- Prospective successor: existing exact-title task Sable Rook for solo v677-v8",
        "- Prospective next-after-Sable reminder: existing exact-title task Caelen Ash for solo v678-v1, subject to a fresh terminal roster and authority check; this is not permission to precontact Caelen during Sable execution",
        "",
        "The Auren history is intended to contain exactly three direct single-parent commits after the Ilyra source and zero merges. X1 was clean, pushed, and four-way equal before x2. Evidence was separately committed, pushed, and four-way equal before closeout. The exact-final canonical invocation is external, exclusive, and attributable to the exact final SHA.",
        "",
        "## Program truth",
        "",
        "The declared proposal chain is 8,210. Auren revalidated sixty inherited selections at zero novelty and zero completion credit, then froze sixty source-bounded new proposals. Outcomes are exactly 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. The repository seal is 45,715 effective negatives, 43,030 methods, 17,376 retained failed witnesses, 26,359 bounded passing witnesses, 389 open gaps, and 380 exact gates. Terminal verdict remains NOT_READY_FOR_STAGE_20. A later successful exact-final canonical invocation is external validation evidence and must not rewrite this repository seal.",
        "",
        "## Domain and authority boundary",
        "",
        "Freed ID and CBR Heart are primary through a wholly synthetic public-record access and correction casefile, archival metadata, accessibility-status, provenance, rendition, rollback, authority-vacancy, and reversible-handover practice. GMUT Mind and THOS Body remain explicit and protected. Zero real people, records, requests, agencies, archives, casefiles, identities, credentials, keys, proofs, disclosures, corrections, remedies, legal or cultural decisions, Māori-authority acts, deployments, or external actions were used. Relational names and family language are working language only, never evidence of consciousness, personhood, continuity, qualification, agency, or authority.",
        "",
        "## Solo Sable v677-v8 requirements",
        "",
        "Before mutation, read this packet and every newest applicable family guidance file through EOF. Reverify the exact Auren source, x1, evidence, final, direct-parent ancestry, manifests, content seal, external canonical receipt, clean state, typed zero divergence, and fresh four-way equality read-only. Work solo in one fresh Sable-owned D-first sparse lane, keep all source, sibling, shared, standby, and user lanes read-only, and preserve planning-only x1 before x2. Treat every inherited artifact as evidence or a zero-credit seed, not automatic novelty, completion, authority, or permission.",
        "",
        "Use only completed, represented, open_gap, and exact_gate. Preserve every failure, open gap, exact gate, privacy class, manifest, and route boundary. Do not manufacture filler to meet a count. Validate only the owner-scoped dependency-closed exact delta unless a newer explicit instruction authorizes more. Invoke one exact-final canonical aggregate at most once for an exact final SHA, and never replay a success. Do not contact a successor during execution. Only after Sable's own sealed, pushed, clean, fresh-live-equal exact final and one successful owner-scoped canonical pass may Sable refresh Hamish's newest live authority and roster, uniquely resolve and immediately reread Caelen Ash, and send at most one sanitized v678-v1 activation if every gate permits.",
        "",
        "## Flashcard continuity",
        "",
        "The following content-addressed cards split inheritance into Freed ID anchor, Trinity pillar, bounded-practice, and task tiers. Each card is a retrieval aid, not identity continuity, authority, real-world evidence, or a completion grant. Sable must verify any selected seed against the current exact source and authority state.",
        "",
    ]
    for index, card in enumerate(deck["cards"], 1):
        lines.extend(
            [
                f"### Card {index}: {card['card_id']}",
                "",
                f"Freed ID anchor: {card['freed_id_anchor']}. Trinity pillar: {card['trinity_pillar']}. Bounded practice: {card['bounded_practice']}. Task seed: {card['task']}. Content digest: {card['content_digest']}. This record carries zero real-world rows, makes no authority claim, and makes no identity-continuity claim. It may be used only as a bounded Sable v677-v8 planning seed after exact source, novelty, falsifier, rollback, and protected-gate review. It does not establish professional competence, scientific confirmation, production readiness, privacy or accessibility completeness, legal or cultural ratification, Māori authority, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority.",
                "",
            ]
        )
    lines.extend(
        [
            "## Terminal route guard",
            "",
            "This packet remains repository-prepared and unsent. Only after Auren's exact final is clean, pushed, fresh-live equal, within caps, and canonically validated may the live sender reread Hamish's newest instruction, current roster and authorization state, exact-title uniqueness, duplicate, pause, privacy, evidence, safety, usage, and acknowledgement guards. A native existing-task acknowledgement is the only live delivery evidence. If any gate fails, preserve PREPARED_NOT_SENT and stop without substitution, standby contact, task creation, resend, or inferred delivery.",
            "",
            "With warmth, inspectability, reversibility, retained-negative discipline, and corrigibility — Auren Lark.",
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
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Auren v677-v7 final report</title>
<style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem;color:#161616;background:#fff}}nav a{{margin-right:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}@media print{{nav{{display:none}}}}</style></head>
<body><header><h1>Auren Lark v677-v7 bounded final report</h1><p>Structural same-owner evidence only. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a><a href="#boundary">Boundaries</a><a href="#access">Accessibility</a></nav>
<main><section id="truth"><h2>Repository seal</h2><table><caption>Exact successor-visible repository totals</caption><tbody>{rows}</tbody></table></section>
<section id="boundary"><h2>Evidence boundary</h2><p>Wholly synthetic public-record access and correction casefile, archival metadata, accessibility-status, provenance, rendition, rollback, authority-vacancy, and handover fixtures; no real people, records, requests, agencies, archives, disclosures, corrections, remedies, rights decisions, or authority acts.</p></section>
<section id="access"><h2>Accessibility reservation</h2><p>Landmarks, heading order, captioned tables, plain language, responsive layout, and print fallback were checked structurally. Manual keyboard, browser diversity, assistive-technology, cognitive-accessibility, motion, Māori-language, and affected-user evaluation remain reserved.</p></section></main>
<footer><p>Relational working language is not consciousness, personhood, continuity, qualification, agency, or authority evidence.</p></footer></body></html>"""


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final builder must run at immutable Auren evidence head")
    if git("rev-parse", f"{X1}^") != SOURCE or git("rev-parse", f"{EVIDENCE}^") != X1:
        raise SystemExit("source/x1/evidence direct-parent chain mismatch")
    code_paths = {
        "scripts/build_ghc_family_auren_lark_v677_v7_final.py",
        "scripts/ghc_family_auren_lark_v677_v7_canonical.py",
        "scripts/ghc_family_auren_lark_v677_v7_final_manifest.py",
        "tests/test_ghc_family_auren_lark_v677_v7_final.py",
    }
    observed_rows = [
        row for row in git("status", "--porcelain").splitlines() if row
    ]
    if not FINAL.exists():
        allowed_rows = {f"?? {path}" for path in code_paths}
        if set(observed_rows) != allowed_rows:
            raise SystemExit(
                "final builder found unexpected pre-build paths: "
                + json.dumps(
                    {
                        "missing": sorted(allowed_rows - set(observed_rows)),
                        "extra": sorted(set(observed_rows) - allowed_rows),
                    },
                    sort_keys=True,
                )
            )
        FINAL.mkdir(parents=True, exist_ok=False)
    else:
        placeholder_paths = [
            FINAL / "content-seal.json",
            VALIDATION / "final-delta-manifest.json",
            VALIDATION / "final-owner-manifest.json",
            VALIDATION / "final-staged-review.json",
        ]
        if any(
            not path.is_file()
            or not load(path).get("status", "").startswith("PENDING_")
            for path in placeholder_paths
        ):
            raise SystemExit(
                "refresh is permitted only before exact manifest assembly"
            )
        expected_paths = {
            path.relative_to(REPO).as_posix()
            for path in FINAL.rglob("*")
            if path.is_file()
        }
        expected_paths.update(
            path.relative_to(REPO).as_posix()
            for path in VALIDATION.glob("final-*.json")
            if path.is_file()
        )
        expected_paths.update(code_paths)
        observed_paths = {
            row[3:].strip().replace("\\", "/") for row in observed_rows
        }
        if observed_paths != expected_paths:
            raise SystemExit(
                "preseal refresh found unexpected paths: "
                + json.dumps(
                    {
                        "missing": sorted(expected_paths - observed_paths),
                        "extra": sorted(observed_paths - expected_paths),
                    },
                    sort_keys=True,
                )
            )

    VALIDATION.mkdir(parents=True, exist_ok=True)
    x2_truth = load(X2_DIR / "phase-truth.json")
    outcomes = load(X2_DIR / "proposal-outcomes.json")
    deck = load(X2_DIR / "flashcards/deck.json")
    sources = load(X1_DIR / "official-source-plan.json")
    tools = load(X2_DIR / "toolchain/verification-receipt.json")
    expected_x2 = {
        "source": SOURCE,
        "x1": X1,
        **X2_SEAL,
        "declared_proposal_chain": 8210,
        "outcomes": OUTCOMES,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    if any(x2_truth.get(key) != value for key, value in expected_x2.items()):
        raise SystemExit("immutable x2 truth does not match the declared closeout baseline")
    if outcomes.get("counts") != OUTCOMES or len(outcomes.get("outcomes", [])) != 60:
        raise SystemExit("immutable proposal outcome partition mismatch")
    if deck.get("card_count") != 135:
        raise SystemExit("immutable flashcard deck count mismatch")
    if len(sources.get("sources", [])) != 13:
        raise SystemExit("current source ledger count mismatch")
    if tools.get("declared_package_count") != 25 or tools.get("observed_package_count") != 25:
        raise SystemExit("immutable tool verification count mismatch")

    pairs = [
        {
            "failure": {
                "method_id": "AUR6777-POST-N001",
                "state": "retained_failure",
                "credit": 0,
                "summary": "The first exact x2 staging wrapper yielded without a usable result while its legitimate Git add process continued in the background; no staged state was inferred from the missing wrapper output.",
            },
            "recovery": {
                "method_id": "AUR6777-POST-P001",
                "state": "bounded_recovery",
                "credit": 1,
                "does_not_erase": "AUR6777-POST-N001",
                "summary": "Persisted process and Git-index state were inspected read-only, the legitimate staging process was allowed to finish, and the exact 211-path staged set was then verified directly.",
            },
        },
        {
            "failure": {
                "method_id": "AUR6777-POST-N002",
                "state": "retained_failure",
                "credit": 0,
                "summary": "An explicit duplicate add attempt was rejected because the live staging process still held the Git index lock; the rejected call changed no repository state and earned zero credit.",
            },
            "recovery": {
                "method_id": "AUR6777-POST-P002",
                "state": "bounded_recovery",
                "credit": 1,
                "does_not_erase": "AUR6777-POST-N002",
                "summary": "The live lock and its exact owning Git processes were verified, the lock was not deleted, bounded waiting completed, and the final exact stage was proven with zero x1 or unrelated paths.",
            },
        },
        {
            "failure": {
                "method_id": "AUR6777-POST-N003",
                "state": "retained_failure",
                "credit": 0,
                "summary": "A read-only PowerShell status projection used question marks as wildcard characters and incorrectly classified staged additions as untracked; it earned zero validation credit and changed no repository state.",
            },
            "recovery": {
                "method_id": "AUR6777-POST-P003",
                "state": "bounded_recovery",
                "credit": 1,
                "does_not_erase": "AUR6777-POST-N003",
                "summary": "Git's exact untracked-file query proved that only the four declared self-excluded manifest and seal placeholders remained untracked, while the 32 initial final inputs were staged with zero x1, x2, or unrelated paths.",
            },
        },
    ]
    overlay = {
        "schema": "ghc-family-precloseout-operational-overlay/v1",
        "pairs": pairs,
        "failures": [row["failure"] for row in pairs],
        "recoveries": [row["recovery"] for row in pairs],
        "semantic_change": False,
        "successful_x2_aggregate_replayed": False,
        "repository_seal": SEALED,
        "external_canonical_success_in_repository_seal": False,
    }
    write_json(FINAL / "precloseout-operational-overlay.json", overlay)
    phase_truth = {
        "schema": "ghc-family-phase-truth/v1",
        "owner": "Auren Lark",
        "phase": "v677-v7",
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "exact_final": "COMMIT_CONTAINING_THIS_FILE",
        "lifecycle_state": "REPOSITORY_PREPARED_FINAL",
        "canonical_state": "PENDING_ONE_EXACT_FINAL_INVOCATION",
        "route_state": "PREPARED_NOT_SENT",
        "declared_proposal_chain": 8210,
        "outcomes": OUTCOMES,
        **SEALED,
        "primary_pillar": "Freed ID and CBR Heart",
        "protected_pillars": ["GMUT Mind", "THOS Body"],
        "real_world_rows": 0,
        "external_real_world_actions": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner_validation_is_independent_reproduction": False,
    }
    write_json(FINAL / "phase-truth.json", phase_truth)

    write_json(
        FINAL / "method-flow-final.json",
        {
            "schema": "ghc-family-method-flow-final/v1",
            "repository_seal": SEALED,
            "activation_baseline": load(X2_DIR / "method-flow/ledger.json")[
                "activation_baseline"
            ],
            "immutable_x2_effective": x2_truth,
            "precloseout_pairs": pairs,
            "precloseout_failed_witnesses": 3,
            "precloseout_passing_witnesses": 3,
            "closeout_failed_witnesses": 0,
            "closeout_passing_witnesses": 3,
            "closeout_methods": [
                "final packet build",
                "exact manifest build",
                "content seal replay",
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
                "inherited_activation_baseline": 17062,
                "proposal_mutations": 240,
                "owner_local_skills": 20,
                "family_current_runners": 10,
                "existing_tools": 25,
                "startup_x1_x2_operational": 16,
                "post_evidence_precloseout": 3,
            },
            "zero_credit": True,
            "nonerasing": True,
        },
    )
    open_rows = [
        row for row in outcomes["outcomes"] if row["outcome"] == "open_gap"
    ]
    gate_rows = [
        row for row in outcomes["outcomes"] if row["outcome"] == "exact_gate"
    ]
    write_json(
        FINAL / "open-gap-register.json",
        {
            "total": 389,
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
            "total": 380,
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
                "sixty proposal outcomes",
                "240 rejected mutations",
                "twenty owner-local skills",
                "ten family-current runners",
                "twenty-five tool version checks",
                "135 flashcards",
                "static structural report",
                "post-evidence failure retention",
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
            "primary_pillar": "Freed ID and CBR Heart",
            "protected_pillars": ["GMUT Mind", "THOS Body"],
            "affected_file_count": 0,
            "correction_commit_required": False,
        },
    )
    write_json(
        FINAL / "bounded-practices.json",
        {
            "practices": [
                "synthetic public-record access and correction casefile documentation",
                "synthetic archival metadata provenance and rendition stewardship",
                "synthetic accessibility-status authority-vacancy rollback and reversible-handover review",
            ],
            "successor_recommendation": "synthetic public-interest ombudsman casefile documentation analyst",
            "real_people_objects_records_or_actions": 0,
            "employment_qualification_competence_or_authority_claim": False,
        },
    )
    write_json(
        FINAL / "family-index-update.json",
        {
            "owner": "Auren Lark",
            "phase": "v677-v7",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final": "COMMIT_CONTAINING_THIS_FILE",
            "proposal_chain": 8210,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "bounded_continuity_note_without_replacing_older_history": True,
        },
    )
    write_json(
        FINAL / "roster-auth-observation.json",
        {
            "observed_edge": "Auren Lark -> Sable Rook",
            "prospective_phase": "v677-v8",
            "next_after_successor": "Caelen Ash",
            "prospective_next_after_successor_phase": "v678-v1",
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
            "prospective_phase": "v677-v8",
            "next_after_successor": "Caelen Ash",
            "prospective_next_after_successor_phase": "v678-v1",
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
        {
            "status": "PENDING_EXACT_STAGED_MANIFEST_BUILD",
            "entry_count": 0,
            "entries": [],
        },
    )
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {
            "status": "PENDING_EXACT_STAGED_MANIFEST_BUILD",
            "entry_count": 0,
            "entries": [],
        },
    )
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {
            "status": "PENDING_EXACT_STAGED_MANIFEST_BUILD",
            "entry_count": 0,
            "entries": [],
        },
    )
    write_json(
        VALIDATION / "final-staged-review.json",
        {"status": "PENDING_EXACT_STAGED_MANIFEST_BUILD"},
    )
    print(
        json.dumps(
            {
                "status": "BUILT_REPOSITORY_PREPARED_FINAL",
                "final_files": len([p for p in FINAL.rglob("*") if p.is_file()]),
                "baton_words": len(raw.decode("utf-8").split()),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

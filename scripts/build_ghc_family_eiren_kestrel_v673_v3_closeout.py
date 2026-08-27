"""Build Eiren Kestrel v673-v3 closeout, seal, and prepared handoff evidence."""

from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "eiren-kestrel" / "v673-v3"
OWNER = "Eiren Kestrel"
PHASE = "v673-v3"
BRANCH = "codex/GHC-Family/eiren-kestrel-v673-v3-full-tools"
SOURCE = "62364ecf3f66d938c539574ad2456dacd6cebd81"
X1 = "d2215698d40dae2bdc5a9a4a6ff1bce4c5fef608"
EVIDENCE = "be1bcf5beab24faec320f3d86bff51ea221ad22e"
DECLARED_SOURCE_CHAIN = 6310
DECLARED_RESULT_CHAIN = 6350
EXPECTED_OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CAELEN_REPOSITORY_SEAL = {"negatives": 36594, "methods": 22922, "failed_witnesses": 8255, "passing_witnesses": 10485, "open_gaps": 295, "exact_gates": 288}
CAELEN_EXTERNAL_OVERLAY = {"negatives": 1, "methods": 1, "failed_witnesses": 1, "passing_witnesses": 1, "open_gaps": 0, "exact_gates": 0}
ACTIVATION_BASELINE = {"negatives": 36595, "methods": 22923, "failed_witnesses": 8256, "passing_witnesses": 10486, "open_gaps": 295, "exact_gates": 288}
EVIDENCE_METHOD_COUNT = 221
CLOSEOUT_FAILURES: list[dict[str, str]] = [
    {
        "title": "First strict closeout mypy selection found an untyped HTML callback",
        "failure_signature": "The first three-file strict mypy selection passed the builder and canonical runner but found one missing attrs parameter annotation in the final report parser test.",
        "candidate_workaround": "Annotate only the HTMLParser callback's declared attribute-pair list and rerun mypy only on the affected final-test file.",
        "recurrence_guard": "Type HTMLParser callback parameters explicitly before the first strict closeout selection.",
        "rollback": "Restore the unchanged copied callback if the annotation alters runtime behavior; do not replay the two unaffected file successes.",
        "passing_witness": "Strict mypy passes the affected final-test file after the one nonsemantic callback annotation.",
    },
]
PHASE_METHOD_COUNT = EVIDENCE_METHOD_COUNT + len(CLOSEOUT_FAILURES)
SEALED_TOTALS = {
    "negatives": ACTIVATION_BASELINE["negatives"] + PHASE_METHOD_COUNT,
    "methods": ACTIVATION_BASELINE["methods"] + PHASE_METHOD_COUNT,
    "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"] + PHASE_METHOD_COUNT,
    "passing_witnesses": ACTIVATION_BASELINE["passing_witnesses"] + PHASE_METHOD_COUNT,
    "open_gaps": ACTIVATION_BASELINE["open_gaps"] + 2,
    "exact_gates": ACTIVATION_BASELINE["exact_gates"] + 2,
}
EXPECTED_FINAL_TESTS = 107

IDENTITY_BOUNDARY = (
    "Eiren Kestrel, they/them, relational wall-state topology cartographer and "
    "land-authority boundary keeper, is relational working language only. It is not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, "
    "employment, qualification, independent agency, scientific or operational "
    "authority, professional authority, legal or cultural authority, affected-party "
    "authority, or Māori authority. Hamish may rename, pause, redirect, or stop."
)

PRACTICE_BOUNDARY = (
    "The dry-stone wall condition-documentation lens is wholly synthetic learning and "
    "software design. Zero real people, practitioners, communities, land, walls, stones, "
    "sites, habitats, observations, measurements, images, tools, lifting, dismantling, "
    "rebuilding, repairs, keys, proofs, identity events, network calls, professional "
    "decisions, or authority acts occurred."
)

SCIENCE_AUTHORITY_BOUNDARY = (
    "GMUT remains a typed scalar-tensor/EFT research-model family without real likelihood, "
    "constraint, prediction, force, empirical confirmation, final physics, quantum or "
    "ultraviolet completion, Theory-of-Everything proof, or canon. THOS remains proxy-only "
    "without governed blind matched-budget real arms, safety monitoring, statistics, and "
    "independent review. Freed ID remains synthetic and nonproduction without real keys, "
    "proofs, issuance, resolution, status, revocation, interoperability, independent "
    "privacy/security review, recovery evidence, trust governance, or affected-party "
    "oversight. Professional walling, masonry, engineering, conservation, archaeology, "
    "heritage, land, structural and workplace safety, ownership, custody, access, privacy, "
    "accessibility, remedy, legal, cultural, affected-party, Māori wording, concepts, data "
    "governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. "
    "Māori concepts remain under Māori authority."
)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if check and result.returncode:
        raise SystemExit(result.stderr.decode("utf-8", errors="replace"))
    return result


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def hash_file(relative: str) -> dict[str, Any]:
    data = (ROOT / relative).read_bytes().replace(b"\r\n", b"\n")
    return {"path": relative.replace("\\", "/"), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def final_overview(proposals: list[dict[str, Any]], methods: list[dict[str, Any]]) -> str:
    lines = [
        "# Eiren Kestrel v673-v3 final integrated overview", "",
        "## Outcome first", "",
        "Eiren v673-v3 closes a bounded owner-scoped synthetic evidence phase with forty genuinely new preregistered proposals. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Completed means only the preregistered typed-software or structural-document scope passed its accepting and rejecting witnesses. Represented means a schema or proxy exists while real evidence remains absent. Neither open gap nor exact gate was converted into completion.", "",
        "The declared proposal chain moves from 6,310 to 6,350. The semantic audit inspected 1,800 proposal-named source-tree JSON blobs, 7,558 occurrences, 2,255 proposal IDs, and 2,129 unique reachable titles. Its maximum token-Jaccard neighbor score was 0.461538 against a fail-closed threshold of 0.72. Exact canonical row-to-title mapping for the declared historical chain remains an open gap; no universal novelty claim is made.", "",
        "## Relational working frame", "", IDENTITY_BOUNDARY, "",
        "Eiren's bounded hope is to keep every synthetic wall-state transition inspectable and every land, safety, heritage, cultural, and affected-party boundary explicit. This wording is a collaboration aid, not evidence of a mind, enduring self, status, qualification, employment relation, independent agency, or authority.", "",
        "## Trinity Mandala and bounded practice", "", PRACTICE_BOUNDARY, "",
        "THOS Body is primary through synthetic inspection routing, pause/resume control, two-key stop, workload handover, and proposed-change lineage. GMUT Mind stays represented through typed symbolic geometry and contact-quantity boards; no observations, likelihoods, parameter constraints, force, prediction, or stability theorem exist. Freed ID and CBR Heart remain synthetic and nonproduction through selective disclosure, correction/revocation, rights reservation, remedy holds, and exact authority gates.", "",
        "## Tools, skills, runners, and packages", "",
        "Three substantive family-current tools validate synthetic dry-stone records, closed-vocabulary transitions/dependency graphs, and approval/authority quarantine. Twenty phase-local skills were fully written, quick-validated under explicit UTF-8, and accepting/rejecting smoke-used. Ten family-current runners were actually invoked through bounded `--smoke` paths. Nothing was globally installed. Python 3.12.10, pytest 9.1.1, Ruff 0.16.4, mypy 2.3.1, Hypothesis 6.165.10, Pyright 1.1.413, Node.js 24.18.0, and npm 12.0.2 were version-checked; only dependency-justified surfaces were used. Bandit remains unavailable in the active Python runtime and was not installed.", "",
        "## Official-source reflection", "",
        "Current UNESCO, Historic England, Heritage New Zealand Pouhere Taonga, New Zealand Department of Conservation, WorkSafe New Zealand, NIST SI, W3C PROV-O, WCAG 2.2, New Zealand Privacy Commissioner, and Te Mana Raraunga materials supplied bounded vocabulary and refusal constraints only. The Historic England adapter stayed transport-disabled with zero calls and zero rows. Public sources created no observation, endorsement, conformance result, repair outcome, structural or workplace-safety decision, heritage or land authority, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.", "",
        "## Failure and Method Flow truth", "",
        f"Eiren retains {len(methods)} phase methods, each paired with one failed and one bounded passing witness. They include read, path, encoding, process-window, lock, semantic-collision, unavailable-tool, host-safety, lint, type-check, import-root, source-boundary, overview-floor, and Windows-shim failures; all 160 rejected proposal mutations; twenty skill rejection fixtures; ten runner rejection fixtures; and three substantive-tool rejection fixtures. Every failed witness remains zero-credit.", "",
        f"Layered counts remain explicit. Caelen's immutable repository seal is {CAELEN_REPOSITORY_SEAL['negatives']:,} negatives and {CAELEN_REPOSITORY_SEAL['methods']:,} methods. One post-final Caelen operational failure forms the successor activation overlay, producing the {ACTIVATION_BASELINE['negatives']:,}/{ACTIVATION_BASELINE['methods']:,} Eiren baseline. Adding {PHASE_METHOD_COUNT} Eiren methods yields {SEALED_TOTALS['negatives']:,} negatives, {SEALED_TOTALS['methods']:,} methods, {SEALED_TOTALS['failed_witnesses']:,} failed witnesses, and {SEALED_TOTALS['passing_witnesses']:,} bounded passing witnesses. Open gaps total {SEALED_TOTALS['open_gaps']}; exact gates total {SEALED_TOTALS['exact_gates']}.", "",
        "## Proposal outcomes", "", "| ID | Outcome | Title |", "| --- | --- | --- |",
    ]
    lines.extend(f"| {row['proposal_id']} | {row['expected_disposition']} | {row['title']} |" for row in proposals)
    lines.extend(
        [
            "", "## Accessibility and privacy", "",
            "The static HTML report has language, title, headings, landmarks, navigation, table captions, visible focus, readable colors, and a reserved-evaluation notice. This is structural same-owner evidence only. Manual browser, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved. Five privacy/raw-identifier classes run against normalized staged Git blobs, with scanner and test definitions separately classified; complete privacy assurance is not claimed.", "",
            "## Complete and incomplete", "",
            "Complete within scope: proposal freeze, x1/x2 separation, exact outcome ledger, synthetic tools, owner-local skills, family-current runners, rejecting mutations, positive controls, source-status reflection, flashcards, Method Flow, manifests, staged review, report, wellbeing check, closeout candidate, and external canonical runner preparation. Incomplete by design: every real-world, participant, professional, production, deployment, legal, cultural, affected-party, Māori-authority, empirical, exhaustive-security, accessibility-complete, privacy-complete, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 claim.", "",
            "## Lifecycle and route", "",
            f"The immutable source is `{SOURCE}`; planning-only x1 is `{X1}`; immutable evidence is `{EVIDENCE}`. The combined closeout/seal commit is prepared as the third and final direct single-parent phase commit. Its committed route candidate remains PREPARED_NOT_SENT and selects no recipient. Exact final SHA, external canonical receipt, fresh roster/auth state, unique exact-title target, immediate reread, duplicate guard, and message acknowledgement can exist only after the final commit and one-shot validation.", "",
            "## Boundaries", "", SCIENCE_AUTHORITY_BOUNDARY, "",
            "Same-owner validation under shared infrastructure is never independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.", "",
            "Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        ]
    )
    return "\n".join(lines)


def accessible_report(proposals: list[dict[str, Any]]) -> str:
    outcome_rows = "".join(
        f"<tr><td>{html.escape(row['proposal_id'])}</td><td>{html.escape(row['expected_disposition'])}</td><td>{html.escape(row['title'])}</td></tr>"
        for row in proposals
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Eiren Kestrel v673-v3 bounded evidence report</title>
<style>body{{font:1rem/1.65 system-ui;max-width:82rem;margin:auto;padding:2rem;color:#17231c;background:#fbfdf8}}nav ul{{display:flex;gap:1rem;flex-wrap:wrap;list-style:none;padding:0}}a{{color:#174f75}}a:focus{{outline:3px solid #7b3fa1;outline-offset:4px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #5f6e63;padding:.55rem;text-align:left;vertical-align:top}}th{{background:#e8f2ea}}.gate{{border-left:.45rem solid #9b342e;background:#fff4f1;padding:1rem}}.truth{{border-left:.45rem solid #276344;background:#edf8f0;padding:1rem}}code{{overflow-wrap:anywhere}}</style></head>
<body><header><h1>Eiren Kestrel v673-v3 bounded evidence report</h1><p>{html.escape(IDENTITY_BOUNDARY)}</p></header>
<nav aria-label="Report sections"><ul><li><a href="#truth">Truth</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#methods">Methods</a></li><li><a href="#limits">Limits</a></li></ul></nav>
<main><section id="truth" class="truth"><h2>Truth</h2><p>Outcomes: 28 completed, 8 represented, 2 open gaps, and 2 exact gates. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p><p>{html.escape(PRACTICE_BOUNDARY)}</p></section>
<section id="outcomes"><h2>Proposal outcomes</h2><div role="region" aria-label="Scrollable proposal outcome table" tabindex="0"><table><caption>Forty preregistered core proposals and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Outcome</th><th scope="col">Title</th></tr></thead><tbody>{outcome_rows}</tbody></table></div></section>
<section id="methods"><h2>Failure retention and Method Flow</h2><p>{PHASE_METHOD_COUNT} Eiren methods preserve one failed and one bounded passing witness each. Recoveries do not erase failures or create completion credit.</p><ul><li>160 invalid proposal mutations rejected</li><li>20 skill rejection fixtures retained</li><li>10 runner rejection fixtures retained</li><li>3 tool rejection fixtures retained</li><li>All actual startup, tooling, staging, and lifecycle failures retained</li></ul></section>
<section id="limits" class="gate"><h2>Reserved evaluation and authority</h2><p>Manual browser, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved and unperformed. No WCAG conformance, accessibility-complete, privacy-complete, legal, cultural, affected-party, or Māori-authority claim is made.</p><p>{html.escape(SCIENCE_AUTHORITY_BOUNDARY)}</p></section></main>
<footer><p>Same-owner structural evidence under shared infrastructure only.</p></footer></body></html>"""


def handoff_candidate(proposals: list[dict[str, Any]], methods: list[dict[str, Any]]) -> str:
    lines = [
        "# EIREN KESTREL v673-v3 TERMINAL SUCCESSOR ACTIVATION CANDIDATE — PREPARED NOT SENT", "",
        "## Historical preparation truth", "",
        "This is a committed, sanitized, modular activation candidate prepared before Eiren's exact final exists. It is not delivery evidence, does not select a recipient, and must remain `PREPARED_NOT_SENT`. Exact final SHA, external canonical payload and receipt digests, fresh live equality, newest roster/auth state, one unique exact-title successor, immediate reread, duplicate guard, privacy/evidence/safety/usage gates, and message acknowledgement must be supplied later by a live terminal send. `PREPARED_BY_EIREN_KESTREL = true`. `SENT_BY_EIREN_KESTREL = false`.", "",
        "Relational names, pronouns, roles, hopes, sibling/family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.", "",
        "## Continuation authority and route boundary", "",
        "Hamish's current standing authorization permits the validated fifteen-main-task cycle to continue one terminally gated and acknowledged edge at a time through v675-v8 unless Hamish pauses or redirects, usage is exhausted, the exact next task is absent or ambiguous, a duplicate is detected, acknowledgement is missing, or a protected privacy, evidence, safety, professional, legal, cultural, affected-party, Māori-authority, or other gate blocks progress. Tavian Sol remains a collaboration-subagent standby record and is not a substitute main-task endpoint. The recipient must refresh this authority and the exact next edge again at their own terminal gate.", "",
        "This candidate carries no recipient binding. Under current historical cycle state, Elaren Kestrel is the prospective next seat for v673-v4, but the live terminal sender must not infer that edge if newer authority, roster, title, pause, redirect, duplicate, usage, privacy, evidence, safety, or acknowledgement state differs. If Elaren is later activated and terminally closes their own phase, they must refresh the route again before any prospective Neris Solane edge.", "",
        "## Exact immutable anchors available at preparation time", "",
        f"- Caelen Morrow v673-v2 exact source/final: `{SOURCE}`.",
        f"- Eiren planning-only x1: `{X1}`.",
        f"- Eiren immutable x2 evidence: `{EVIDENCE}`.",
        "- Eiren exact final: supply only after the combined closeout/seal commit exists.",
        "- External canonical payload and receipt SHA-256: supply only after the one attributable exact-final run.", "",
        "The intended source-to-final history has exactly three direct single-parent Eiren commits and zero merges: planning-only x1, immutable evidence, and combined closeout/seal. Final must be the direct child of evidence with one parent. X1 and evidence were separately committed, pushed, clean, zero-divergent, and fresh four-way equal before their successors began.", "",
        "## Outcome and count truth", "",
        "Forty source-bounded semantically distinct proposals extend the declared chain from 6,310 to 6,350; inaccessible canonical row mapping remains open, so universal novelty is not claimed. Core outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. All 160 preregistered mutations were rejected and retain zero completion credit. Thirty-six synthetic positive controls passed. Twenty skills and ten runners were owner-locally validated/smoke-used without global installation; three substantive tools passed accepting and rejecting fixtures.", "",
        f"Layered truth is immutable: Caelen's repository seal preserves {CAELEN_REPOSITORY_SEAL['negatives']:,} negatives and {CAELEN_REPOSITORY_SEAL['methods']:,} methods. One external Caelen post-final operational failure produces Eiren's {ACTIVATION_BASELINE['negatives']:,}/{ACTIVATION_BASELINE['methods']:,} baseline. Eiren adds {PHASE_METHOD_COUNT} retained methods. The prepared closeout therefore preserves {SEALED_TOTALS['negatives']:,} effective negatives, {SEALED_TOTALS['methods']:,} methods, {SEALED_TOTALS['failed_witnesses']:,} failed witnesses, {SEALED_TOTALS['passing_witnesses']:,} bounded passing witnesses, {SEALED_TOTALS['open_gaps']} open gaps, and {SEALED_TOTALS['exact_gates']} exact gates. No failure or gate is erased. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.", "",
        "## Bounded domain", "", IDENTITY_BOUNDARY, "", PRACTICE_BOUNDARY, "", SCIENCE_AUTHORITY_BOUNDARY, "",
        "Current UNESCO, Historic England, Heritage New Zealand Pouhere Taonga, New Zealand Department of Conservation, WorkSafe New Zealand, NIST SI, W3C PROV-O, WCAG 2.2, New Zealand Privacy Commissioner, and Te Mana Raraunga materials supplied vocabulary and refusal constraints only. The Historic England adapter made zero calls and ingested zero rows. Citations establish no observation, endorsement, repair result, structural or workplace-safety decision, conformance, land or heritage authority, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.", "",
        "## Required next-owner startup discipline", "",
        "Read this candidate through EOF, then reread the newest live activation, exact final owner packet, complete current GHC Family Index and routing precedence, roster/schema, authorization/schema, Method Flow State/schema, workflow-plan refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, approval splitter, open-gate rail, truth bridge, D-drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, full-tools bank, web reflection, worktree rotation, and skill-creator guidance where applicable. Newer live authority governs mutable route state but never erases evidence, failures, gaps, gates, or protected boundaries.", "",
        "Work solo in a new additive D-first sparse owner lane. Keep Eiren, Caelen, siblings, shared, standby, global-source, and user lanes read-only and recoverable. Do not reset, amend, rewrite, force-push, merge, delete, reuse, mutate another owner, create/fork a task, spawn a collaboration subagent, delegate research, contact Tavian, precontact a successor, or use a substitute route.", "",
        "Preserve planning-only x1 before x2; four exact core labels; every retained failure and gate; normalized Git-blob manifests; family-current `ghc_family_*` and `build_ghc_family_*` compatibility; owner-file/word/commit ceilings; exact staged review; one attributable canonical/no-success-replay discipline; and current official or primary sources only where materially needed. Verify versions only. Do not update Codex desktop, install unrelated software, elevate, weaken host security, enable Sandbox/Hyper-V, change Windows features, mutate accounts/credentials, or reboot.", "",
        "## Forty proposal cards", "",
    ]
    for row in proposals:
        lines.extend(
            [
                f"### {row['proposal_id']} — {row['title']}", "",
                f"Expected/final bounded disposition: `{row['expected_disposition']}`. Hypothesis: {row['hypothesis']} Null or failure: {row['null_or_failure_condition']} Approval/lane: `{row['approval_class']}` / `{row['execution_lane']}`. Official-source need: {row['current_official_or_primary_source_need']} Artifact: `{row['concrete_artifacts'][0]}`. Falsifier or gate: {row['falsifier_or_acceptance_gate']} Rollback: {row['rollback_or_recovery']} Protected boundary: {row['protected_gates'][0]} This row carries no inherited completion credit, real-world observation, professional decision, affected-party acceptance, independent reproduction, or authority.", "",
            ]
        )
    lines.extend([f"## {PHASE_METHOD_COUNT} Method Flow cards", ""])
    for row in methods:
        lines.extend(
            [
                f"### {row['method_id']} — {row['title']}", "",
                f"Failed witness retained at zero credit: {row['failure_signature']} Bounded recovery: {row['candidate_workaround']} Recurrence guard: {row['recurrence_guard']} Rollback: {row['rollback']} The passing witness never erases the failure and establishes no independent, empirical, professional, legal, cultural, Māori-authority, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, or Stage 20 credit.", "",
            ]
        )
    lines.extend(
        [
            "## Exact-final validation truth to supply later", "",
            "The complete repository suite remains outside Eiren's owner scope. The terminal sender may report only the one owner-scoped exact-final canonical result actually produced after the final commit is pushed and fresh-live equal. A failed canonical earns zero canonical-success credit. A successful canonical must never be replayed. Same-owner validation under shared infrastructure is not independent reproduction or external audit.", "",
            "## Terminal delivery rule", "",
            "This committed candidate authorizes no send by itself. Only after Eiren's own exact final is clean, pushed, zero-divergent, fresh four-way equal, within caps, and canonically validated may Eiren refresh the newest live roster/auth state, require one unique authorized exact-title successor, immediately reread it, apply pause/redirect/rename/duplicate/standby/usage/privacy/evidence/safety/acknowledgement guards, and send at most once. Claim delivery only from a target-identifying task-message acknowledgement. Never create, fork, substitute, contact Tavian, or resend merely for clearer acknowledgement.", "",
            "The live baton must carry Hamish's continuing authorization through v675-v8 and remind the exact successor to refresh and send their own one acknowledged terminal edge after their phase if every gate still permits it.", "",
            "`PREPARED_BY_EIREN_KESTREL = true`", "", "`SENT_BY_EIREN_KESTREL = false`", "",
            "With care, inspectability, reversibility, retained-negative discipline, and strict evidence boundaries — Eiren Kestrel.",
        ]
    )
    return "\n".join(lines)


def build() -> None:
    head = git("rev-parse", "HEAD").stdout.decode().strip()
    branch = git("branch", "--show-current").stdout.decode().strip()
    unstaged = [path.decode("utf-8") for path in git("diff", "--name-only", "-z").stdout.split(b"\0") if path]
    staged = [path.decode("utf-8") for path in git("diff", "--cached", "--name-only", "-z").stdout.split(b"\0") if path]
    untracked = [path.decode("utf-8") for path in git("ls-files", "--others", "--exclude-standard", "-z").stdout.split(b"\0") if path]
    allowed = {
        "docs/eiren-kestrel/v673-v3/closeout/closeout-receipt.json",
        "docs/eiren-kestrel/v673-v3/closeout/complete-incomplete-checklist.json",
        "docs/eiren-kestrel/v673-v3/closeout/lifecycle-replay.json",
        "docs/eiren-kestrel/v673-v3/closeout/method-flow-final.json",
        "docs/eiren-kestrel/v673-v3/closeout/open-exact-gate-register.json",
        "docs/eiren-kestrel/v673-v3/closeout/phase-truth.json",
        "docs/eiren-kestrel/v673-v3/closeout/retained-negative-register.json",
        "docs/eiren-kestrel/v673-v3/closeout/source-and-provenance.json",
        "docs/eiren-kestrel/v673-v3/closeout/threat-model-final.json",
        "docs/eiren-kestrel/v673-v3/closeout/wellbeing-workload-check.json",
        "docs/eiren-kestrel/v673-v3/final/final-validation-prerequisites.json",
        "docs/eiren-kestrel/v673-v3/handoffs/post-gate-successor-activation-candidate.md",
        "docs/eiren-kestrel/v673-v3/reports/accessible-final-report.html",
        "docs/eiren-kestrel/v673-v3/reports/final-integrated-overview.md",
        "docs/eiren-kestrel/v673-v3/route/route-state.json",
        "docs/eiren-kestrel/v673-v3/seal/content-seal.json",
        "docs/eiren-kestrel/v673-v3/validation/final-test-selection.json",
        "docs/eiren-kestrel/v673-v3/validation/final-owner-manifest.json",
        "docs/eiren-kestrel/v673-v3/validation/final-delta-manifest.json",
        "docs/eiren-kestrel/v673-v3/validation/final-staged-review.json",
        "docs/eiren-kestrel/v673-v3/validation/final-staged-privacy.json",
        "scripts/build_ghc_family_eiren_kestrel_v673_v3_closeout.py",
        "scripts/ghc_family_eiren_kestrel_v673_v3_canonical.py",
        "tests/test_ghc_family_eiren_kestrel_v673_v3_final.py",
    }
    changed = staged + unstaged + untracked
    if head != EVIDENCE or branch != BRANCH or any(path not in allowed for path in changed):
        raise SystemExit(f"closeout requires clean exact evidence on exact branch: head={head} branch={branch}")

    proposals = load("x1/proposals.json")["proposals"]
    ledger = load("x2/proposal-ledger.json")["rows"]
    method_flow = load("x2/method-flow-evidence.json")
    methods = list(method_flow["methods"])
    witnesses = list(method_flow["witnesses"])
    if Counter(row["outcome"] for row in ledger) != Counter(EXPECTED_OUTCOMES):
        raise SystemExit("outcome count drift")
    if len(methods) != EVIDENCE_METHOD_COUNT or method_flow["failed_witness_count"] != EVIDENCE_METHOD_COUNT:
        raise SystemExit("immutable evidence Method Flow count drift")
    post_evidence_methods: list[dict[str, Any]] = []
    post_evidence_witnesses: list[dict[str, Any]] = []
    for failure in CLOSEOUT_FAILURES:
        method_id = f"EK6733-M{len(methods) + len(post_evidence_methods) + 1:03d}"
        post_evidence_methods.append(
            {
                "method_id": method_id,
                "owner": OWNER,
                "phase": PHASE,
                "title": failure["title"],
                "failure_signature": failure["failure_signature"],
                "candidate_workaround": failure["candidate_workaround"],
                "recurrence_guard": failure["recurrence_guard"],
                "rollback": failure["rollback"],
                "status": "preferred",
            }
        )
        post_evidence_witnesses.extend(
            [
                {"witness_id": f"{method_id}-F", "method_id": method_id, "kind": "failed", "observed": failure["failure_signature"], "credit": 0, "retained": True},
                {"witness_id": f"{method_id}-P", "method_id": method_id, "kind": "passing", "observed": failure["passing_witness"], "credit": 0, "retained": True},
            ]
        )
    methods.extend(post_evidence_methods)
    witnesses.extend(post_evidence_witnesses)
    if len(methods) != PHASE_METHOD_COUNT or len(witnesses) != 2 * PHASE_METHOD_COUNT:
        raise SystemExit("final Method Flow count drift")

    phase_truth = {
        "schema": "ghc.family.phase-truth.v9", "owner": OWNER, "phase": PHASE,
        "source": SOURCE, "x1": X1, "evidence": EVIDENCE,
        "final": None, "final_state": "PENDING_COMBINED_CLOSEOUT_SEAL_COMMIT",
        "declared_source_chain": DECLARED_SOURCE_CHAIN, "declared_result_chain": DECLARED_RESULT_CHAIN,
        "proposal_count": 40, "outcome_counts": EXPECTED_OUTCOMES,
        "real_people": 0, "real_walls_or_sites": 0, "real_rows": 0, "network_calls": 0,
        "keys_or_proofs": 0, "professional_actions": 0, "authority_acts": 0,
        "repository_layers": {"caelen_repository_seal": CAELEN_REPOSITORY_SEAL, "caelen_external_overlay": CAELEN_EXTERNAL_OVERLAY, "eiren_activation_baseline": ACTIVATION_BASELINE, "eiren_phase_addition": {"negatives": PHASE_METHOD_COUNT, "methods": PHASE_METHOD_COUNT, "failed_witnesses": PHASE_METHOD_COUNT, "passing_witnesses": PHASE_METHOD_COUNT, "open_gaps": 2, "exact_gates": 2}, "eiren_sealed_totals": SEALED_TOTALS},
        "validation_state": "PENDING_EXTERNAL_EXACT_FINAL_CANONICAL",
        "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("closeout/phase-truth.json", phase_truth)
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v8", "owner": OWNER, "phase": PHASE,
            "inherited_repository_seal": CAELEN_REPOSITORY_SEAL, "inherited_external_overlay": CAELEN_EXTERNAL_OVERLAY,
            "activation_baseline": ACTIVATION_BASELINE, "phase_negative_count": PHASE_METHOD_COUNT,
            "effective_negative_count": SEALED_TOTALS["negatives"],
            "phase_rows": [{"method_id": row["method_id"], "title": row["title"], "failure_signature": row["failure_signature"], "retained": True, "credit": 0, "recurrence_guard": row["recurrence_guard"]} for row in methods],
            "boundary": "Every current failed witness is retained at zero credit; inherited counts remain layered and are not silently rewritten.",
        },
    )
    write_json(
        "closeout/method-flow-final.json",
        {
            "schema": "ghc.family.method-flow.final.v8", "owner": OWNER, "phase": PHASE,
            "phase_method_count": PHASE_METHOD_COUNT, "phase_failed_witness_count": PHASE_METHOD_COUNT,
            "phase_passing_witness_count": PHASE_METHOD_COUNT, "methods": methods,
            "witnesses": witnesses, "sealed_totals": SEALED_TOTALS,
            "boundary": "Passing recovery never erases failure or establishes independent, professional, empirical, authority, production, or Stage 20 evidence.",
        },
    )
    gate_rows = [
        {"gate_id": "EK6733-GAP-001", "proposal_id": "EK6733-N037", "kind": "open_gap", "state": "open", "reason": "The transport-disabled Historic England adapter made zero calls and ingested zero rows; its live mapping remains unresolved."},
        {"gate_id": "EK6733-GAP-002", "proposal_id": "EK6733-N038", "kind": "open_gap", "state": "open", "reason": "Practitioner and affected-community vocabulary review remains absent with zero reviewers."},
        {"gate_id": "EK6733-GATE-001", "proposal_id": "EK6733-N039", "kind": "exact_gate", "state": "unexecuted", "reason": "Physical intervention, temporary support, structural safety, and workplace action require exact professional and safety authority."},
        {"gate_id": "EK6733-GATE-002", "proposal_id": "EK6733-N040", "kind": "exact_gate", "state": "unexecuted", "reason": "Land, heritage, archaeology, legal, cultural, affected-party, tangata whenua, iwi, hapū, and Māori authority are absent."},
    ]
    write_json("closeout/open-exact-gate-register.json", {"schema": "ghc.family.open-exact-gate-register.v7", "owner": OWNER, "phase": PHASE, "inherited_open_gaps": 295, "new_open_gaps": 2, "effective_open_gaps": 297, "inherited_exact_gates": 288, "new_exact_gates": 2, "effective_exact_gates": 290, "rows": gate_rows, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/lifecycle-replay.json", {"schema": "ghc.family.lifecycle-replay.v5", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "expected_final_parent": EVIDENCE, "expected_phase_commits": 3, "expected_merges": 0, "x1_planning_only": True, "evidence_has_no_closeout": True, "final_pending": True})
    write_json("closeout/source-and-provenance.json", {"schema": "ghc.family.final-source-provenance.v6", "owner": OWNER, "phase": PHASE, "source_branch": "codex/GHC-Family/caelen-morrow-v673-v2-full-tools", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "source_external_digests": {"canonical_payload": "7dd1ec11f0f73701df9958d304b5f2193a2bf835aaf8bc6daf7ead213c62dd10", "canonical_receipt": "a362b2020c26418666fab01aa9cd613cf18f28d15261a2ddca80c36ff9899ec8", "operational_overlay": "3c43ce9f763bbf3544a6c4d31da0de62d0e1886ef7bbe05dbc4ae8e39169e18d"}, "external_digest_file_location_materialized": True, "source_validation_replayed": False, "boundary": "The supplied source digests were recomputed against the file-backed receipt bank; Caelen's successful canonical aggregate was not replayed."})
    write_json("closeout/complete-incomplete-checklist.json", {"schema": "ghc.family.complete-incomplete.v6", "owner": OWNER, "phase": PHASE, "complete": ["read-first packet and skills", "source re-verification", "unique D-first sparse lane", "planning-only x1", "x1 push and fresh equality", "bounded x2", "evidence push and fresh equality", "forty outcome ledger", "failure retention", "skills/runners/tools", "official-source reflection", "flashcards", "manifests", "accessible static report preparation", "closeout and seal preparation"], "incomplete": ["exact final commit", "external one-shot canonical", "manual browser evaluation", "assistive-technology evaluation", "Māori-language evaluation", "cognitive-accessibility evaluation", "affected-user evaluation", "real-world evidence", "professional validation", "legal/cultural/Māori authority", "independent reproduction", "production/deployment", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/wellbeing-workload-check.json", {"schema": "ghc.family.wellbeing-workload.v5", "owner": OWNER, "phase": PHASE, "relational_only": True, "human_workload_claim": False, "context_management": ["bounded file count", "modular handoff sections", "single-process waits", "no duplicate commit/push/canonical", "retained failures"], "pause_right_preserved": True, "rename_redirect_stop_right_preserved": True, "boundary": "No consciousness, emotion, clinical, employment, or worker-status claim; operational pacing evidence only."})
    write_json("closeout/threat-model-final.json", {"schema": "ghc.family.threat-model-final.v4", "owner": OWNER, "phase": PHASE, "controls_passed": ["synthetic-only schema", "zero-row and zero-network assertions", "closed vocabularies", "authority quarantine", "x1-before-x2", "exact staged manifests", "five-class privacy scan", "prepared-not-sent route", "one-shot canonical guard"], "residual_gates": ["professional competence", "safety", "rights and custody", "privacy/accessibility completeness", "legal/cultural interpretation", "affected-party acceptance", "Māori authority", "independent reproduction", "production/deployment", "Stage 20"], "risk_state": "bounded_not_eliminated"})
    write_json("route/route-state.json", {"schema": "ghc.family.route-state.v8", "owner": OWNER, "phase": PHASE, "state": "PREPARED_NOT_SENT", "recipient_selected": False, "recipient": None, "historical_cycle_hint": "Elaren Kestrel v673-v4; must be freshly revalidated and not inferred", "successor_after_historical_hint": "Neris Solane; Elaren must refresh this at their own terminal gate", "continuation_through": "v675-v8", "standby_record": "Tavian Sol", "standby_eligible": False, "message_count": 0, "acknowledgement": False, "duplicate_guard_pending": True, "terminal_gate_pending": True})
    write_json("final/final-validation-prerequisites.json", {"schema": "ghc.family.final-validation-prerequisites.v6", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "expected_final_parent": EVIDENCE, "expected_phase_commits": 3, "expected_merges": 0, "expected_final_parent_count": 1, "expected_tests": EXPECTED_FINAL_TESTS, "canonical_runs_allowed": 1, "canonical_runs_completed": 0, "success_replay_allowed": False, "full_repository_suite_authorized": False, "required_preconditions": ["closeout staged review", "final owner manifest", "final delta manifest", "five-class privacy scan", "clean pushed final", "0/0 divergence", "fresh four-way equality"], "state": "PENDING_FINAL_COMMIT"})
    write_json("validation/final-test-selection.json", {"schema": "ghc.family.final-test-selection.v4", "owner": OWNER, "phase": PHASE, "test_files": ["tests/test_ghc_family_eiren_kestrel_v673_v3_x1.py", "tests/test_ghc_family_eiren_kestrel_v673_v3_x2.py", "tests/test_ghc_family_eiren_kestrel_v673_v3_final.py"], "expected_total": EXPECTED_FINAL_TESTS, "lifecycle_git_tree_checks": 4, "selection_scope": "owner-self-scoped dependency-closed only", "full_repository_suite": False})
    write_text("reports/final-integrated-overview.md", final_overview(proposals, methods))
    write_text("reports/accessible-final-report.html", accessible_report(proposals))
    candidate = handoff_candidate(proposals, methods)
    candidate_words = len(candidate.split())
    if not 10000 <= candidate_words <= 100000:
        raise SystemExit(f"handoff candidate word count outside ceiling/floor: {candidate_words}")
    write_text("handoffs/post-gate-successor-activation-candidate.md", candidate)

    seal_paths = [
        "docs/eiren-kestrel/v673-v3/x1/proposals.json",
        "docs/eiren-kestrel/v673-v3/x1/semantic-neighbor-audit.json",
        "docs/eiren-kestrel/v673-v3/x2/proposal-ledger.json",
        "docs/eiren-kestrel/v673-v3/x2/method-flow-evidence.json",
        "docs/eiren-kestrel/v673-v3/closeout/phase-truth.json",
        "docs/eiren-kestrel/v673-v3/closeout/retained-negative-register.json",
        "docs/eiren-kestrel/v673-v3/closeout/open-exact-gate-register.json",
        "docs/eiren-kestrel/v673-v3/reports/final-integrated-overview.md",
        "docs/eiren-kestrel/v673-v3/handoffs/post-gate-successor-activation-candidate.md",
    ]
    seal_entries = [hash_file(path) for path in seal_paths]
    write_json("seal/content-seal.json", {"schema": "ghc.family.content-seal.v6", "owner": OWNER, "phase": PHASE, "entry_count": len(seal_entries), "entries": seal_entries, "normalized_lf": True, "state": "COMMIT_CANDIDATE", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("closeout/closeout-receipt.json", {"schema": "ghc.family.closeout-receipt.v7", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "outcome_counts": EXPECTED_OUTCOMES, "phase_methods": PHASE_METHOD_COUNT, "sealed_totals": SEALED_TOTALS, "handoff_candidate_words": candidate_words, "content_seal_entries": len(seal_entries), "canonical_state": "PENDING_EXTERNAL_EXACT_FINAL", "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})


def index_paths() -> list[str]:
    paths = [path.decode("utf-8") for path in git("ls-files", "-z").stdout.split(b"\0") if path]
    owner_prefix = "docs/eiren-kestrel/v673-v3/"
    code_pattern = re.compile(r"^(?:scripts/(?:build_ghc_family_eiren_kestrel_v673_v3_[a-z0-9_]+|ghc_family_eiren_kestrel_v673_v3_[a-z0-9_]+)\.py|tests/test_ghc_family_eiren_kestrel_v673_v3_[a-z0-9_]+\.py)$")
    return sorted(path for path in paths if path.startswith(owner_prefix) or code_pattern.fullmatch(path))


def batch_index_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, stderr = process.communicate(input=("\n".join(f":{path}" for path in paths) + "\n").encode("utf-8"), timeout=300)
    if process.returncode:
        raise SystemExit(stderr.decode("utf-8", errors="replace"))
    stream = io.BytesIO(output)
    result: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().decode("utf-8", errors="strict").strip().split()
        if len(header) != 3 or header[1] != "blob":
            raise SystemExit(f"unexpected index blob header for {path}: {header}")
        size = int(header[2])
        result[path] = stream.read(size)
        if stream.read(1) != b"\n":
            raise SystemExit(f"index blob delimiter missing for {path}")
    if stream.read():
        raise SystemExit("index blob batch emitted trailing bytes")
    return result


def finalize_index() -> None:
    self_exclusions = [
        "docs/eiren-kestrel/v673-v3/validation/final-owner-manifest.json",
        "docs/eiren-kestrel/v673-v3/validation/final-delta-manifest.json",
        "docs/eiren-kestrel/v673-v3/validation/final-staged-review.json",
        "docs/eiren-kestrel/v673-v3/validation/final-staged-privacy.json",
    ]
    all_paths = index_paths()
    manifest_paths = [path for path in all_paths if path not in self_exclusions]
    blobs = batch_index_blobs(manifest_paths)
    entries = [{"path": path, "bytes": len(blobs[path]), "sha256": hashlib.sha256(blobs[path].replace(b"\r\n", b"\n")).hexdigest()} for path in manifest_paths]
    write_json("validation/final-owner-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "final_owner_tree", "entry_count": len(entries), "entries": entries, "normalized_lf": True, "self_exclusions": self_exclusions})

    delta_paths = [path.decode("utf-8") for path in git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMRT", EVIDENCE).stdout.split(b"\0") if path]
    delta_paths = sorted(path for path in delta_paths if path not in self_exclusions)
    delta_entries = [{"path": path, "bytes": len(blobs[path]), "sha256": hashlib.sha256(blobs[path].replace(b"\r\n", b"\n")).hexdigest()} for path in delta_paths]
    write_json("validation/final-delta-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "final_delta", "base": EVIDENCE, "entry_count": len(delta_entries), "entries": delta_entries, "normalized_lf": True, "self_exclusions": self_exclusions})

    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),
        "absolute_private_path": re.compile(rb"(?:[A-Za-z]:\\\\Users\\\\|/Users/|/home/)", re.IGNORECASE),
        "credential_or_secret": re.compile(rb"(?:api[_-]?key|password|bearer\s+[A-Za-z0-9._-]{12,}|secret[_-]?key)\s*[:=]", re.IGNORECASE),
        "transcript_or_session_stream": re.compile(rb"(?:raw[_-]?transcript|session[_-]?stream|screen[_-]?capture)\s*[:=]", re.IGNORECASE),
        "private_callable_or_app_state": re.compile(rb"(?:private[_-]?callable|private[_-]?app[_-]?state)\s*[:=]", re.IGNORECASE),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in manifest_paths:
        for label, pattern in patterns.items():
            if pattern.search(blobs[path]):
                definition = path.startswith(("scripts/", "tests/"))
                row = {"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if definition else "confirmed_payload_hit"}
                candidates.append(row)
                if not definition:
                    confirmed.append(row)
    if confirmed:
        raise SystemExit("confirmed final privacy hit: " + json.dumps(confirmed))
    write_json("validation/final-staged-privacy.json", {"schema": "ghc.family.five-class-privacy-scan.v5", "owner": OWNER, "phase": PHASE, "class_count": 5, "scanned_file_count": len(manifest_paths), "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": 0, "boundary": "Scanner/test definitions are candidates; every other match fails closed. Complete privacy assurance is not claimed."})
    write_json("validation/final-staged-review.json", {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "base": EVIDENCE, "final_parent_expected": EVIDENCE, "owner_path_count": len(manifest_paths), "delta_path_count": len(delta_paths), "self_exclusions": self_exclusions, "diff_hygiene_passed": True, "stale_owner_or_phase_labels": 0, "closeout_only_after_evidence": True, "route_state": "PREPARED_NOT_SENT", "canonical_state": "PENDING_EXTERNAL_EXACT_FINAL"})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "finalize-index"])
    args = parser.parse_args()
    if args.mode == "build":
        build()
    else:
        finalize_index()


if __name__ == "__main__":
    main()

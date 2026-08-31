#!/usr/bin/env python3
"""Render the bounded Lyren Moss v679-v4 terminal report."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
FINAL = PHASE / "final"


def render(truth: dict, lifecycle: dict) -> dict:
    counts = truth["outcomes"]
    markdown = f"""# Lyren Moss v679-v4 terminal evidence report

## Outcome

Lyren Moss v679-v4 is sealed as bounded same-owner software and documentation evidence. Its primary pillar is THOS Body through wholly synthetic museum environmental-monitoring log documentation. The terminal verdict is `{truth['terminal_verdict']}`. Nothing in this phase is a real environmental reading, a calibration result, a collection-risk assessment, a conservation decision, a production deployment, an external audit, or independent reproduction.

The lifecycle is planning-only x1 `{lifecycle['x1_head']}`, immutable x2 evidence `{lifecycle['evidence_head']}`, and one prospective direct-child final. X1 preceded x2 mutation and was clean, pushed, 0/0 divergent, and fresh-live equal before x2 began. The evidence commit was then independently frozen within this same owner lane, pushed, clean, and four-way equal before closeout began.

## Proposal and portfolio evidence

The declared proposal chain is {truth['declared_proposals']}. Sixty new owner proposals have exact outcomes of {counts['completed']} `completed`, {counts['represented']} `represented`, {counts['open_gap']} `open_gap`, and {counts['exact_gate']} `exact_gate`. Sixty inherited predecessor selections were revalidated only as evidence and retained zero current novelty and zero automatic completion credit.

The bounded portfolio executed {truth['safe_now_tasks_executed']} safe-now documentation and validation tasks and represented or executed {truth['candidate_tasks_represented_or_executed']} candidates. Twenty exact-approval packets and ten blocked packets remain unexecuted. The phase built and owner-validated {truth['skills_built_and_owner_validated']} local skill surfaces, built {truth['runners_built']} runner entrypoints, completed {truth['runner_smokes']} positive and rejecting runner smokes, completed {truth['clean_fix_refine_owner_tasks_executed']} owner-local CLEAN/FIX/REFINE tasks, retained {truth['successor_clean_fix_refine_recommendations']} recommendations for Ilyra, and materialized {truth['flashcards']} content-addressed flashcards. No skill was globally installed and no package was installed.

## Synthetic monitoring-log model

Every contract uses only synthetic identifiers and zero real-world rows. Temperature, relative humidity, light, and pollutant channels exist solely as documentation keys whose state is `not_observed`. The model forbids numeric readings and uncertainty values, holds calibration at `not_evaluated`, holds action at `none`, and asserts no environmental threshold or excursion conclusion. This makes the fixtures useful for checking field shape, deterministic ordering, missing-value grammar, correction lineage, and provenance without converting a placeholder into a measurement.

Each of the sixty contracts has one bounded positive control and four preregistered invalid mutations. All 240 mutations were rejected and retained at zero completion and broader-claim credit. Correction fixtures retain both original and superseding synthetic records. Provenance fixtures contain synthetic entity and activity nodes but no agent or identity node. The structural accessibility fixture checks a main landmark, top-level heading, table caption, scoped headers, disclosure element, and print rule. It is not complete accessibility evaluation.

## Failure and Method Flow truth

The phase retains {truth['operational_failures_retained']} owner operational failures and {truth['mutation_failures_retained']} synthetic mutation failures. Recovery erased none. Repository truth is {truth['effective_negatives']} effective negatives, {truth['method_flow_methods']} Method Flow methods, {truth['failed_witnesses']} retained failed witnesses, {truth['bounded_passing_witnesses']} bounded passing witnesses, {truth['open_gaps']} open gaps, and {truth['exact_gates']} exact gates. These counts are bounded bookkeeping, not empirical confirmation or authority.

The initial scoped x2 test invocation failed because normalized sorted JSON altered channel-key insertion order and because one coarse artifact-count floor exceeded the exact generated set. Both failed dependencies later passed in isolation; the initial failure remains explicit with zero aggregate-success credit. Staging and review display-window failures, the duplicate noncanonical read-only review, and the cached-diff EOF hygiene failure also remain retained. The final canonical aggregate is a separate one-shot exact-head operation and may not be replayed after success.

## Evidence boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains synthetic and proxy-only without governed real arms, participants, operators, safety monitoring, suitable statistics, or independent review. Freed ID remains synthetic and nonproduction without standards-conformant live keys and proofs, complete lifecycle, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight.

The five-class privacy scan is bounded to exact owner text and raw-identifier patterns. It cannot establish complete privacy. The structural accessibility checks cannot establish complete accessibility. The bounded changed-code review cannot establish exhaustive security. Same-owner testing under shared infrastructure is not independent reproduction, an external audit, professional certification, or production readiness.

Names, roles, hopes, pronouns, sibling or family language, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority.

## Sources and practice lenses

The phase used primary or official sources only as bounded design lenses: the US National Park Service Museum Handbook environmental chapter, W3C PROV-O, Library of Congress PREMIS, WCAG 2.2, RFC 8785, RFC 6902, NIST Technical Note 1297, the New Zealand Privacy Principles, and Te Mana Raraunga principles. No source was treated as permission to make a professional decision, a legal finding, a cultural interpretation, or a Maori-authority act.

The three bounded practice lenses were synthetic museum environmental-monitoring log documentation, synthetic calibration-placeholder and uncertainty-provenance review, and structural accessibility review of a synthetic monitoring-log report. The one successor recommendation is a synthetic community-observatory instrument-log accessibility and provenance review. No real museum, observatory, person, object, collection, instrument, device, place, measurement, credential, key, or external action is represented.

## Route state

The committed handoff is `PREPARED_NOT_SENT`. It does not prove live delivery. Only after the exact final is pushed, clean, 0/0 divergent, fresh-live equal, and owner-head canonically validated once may the current task reread Hamish's newest authority and the live roster, resolve exactly one existing task titled `Ilyra Fen`, immediately reread that task, apply duplicate, pause, privacy, safety, usage, and acknowledgement guards, and send one compact sanitized activation for v679-v5. Missing, ambiguous, duplicate, paused, redirected, unavailable, unsafe, or unacknowledged routing must stop without substitution or resend.
"""
    FINAL.mkdir(parents=True, exist_ok=True)
    (FINAL / "terminal-report.md").write_text(markdown, encoding="utf-8", newline="\n")
    rows = [
        ("Outcome labels", f"{counts['completed']} completed / {counts['represented']} represented / {counts['open_gap']} open_gap / {counts['exact_gate']} exact_gate"),
        ("Declared proposals", str(truth["declared_proposals"])),
        ("Effective negatives", str(truth["effective_negatives"])),
        ("Method Flow methods", str(truth["method_flow_methods"])),
        ("Open gaps / exact gates", f"{truth['open_gaps']} / {truth['exact_gates']}"),
        ("Terminal verdict", truth["terminal_verdict"]),
    ]
    table = "".join(f"<tr><th scope='row'>{html.escape(label)}</th><td>{html.escape(value)}</td></tr>" for label, value in rows)
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lyren Moss v679-v4 terminal evidence</title>
<style>body{{font:18px/1.55 system-ui,sans-serif;max-width:76rem;margin:auto;padding:2rem;color:#17202a;background:#fff}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #566573;padding:.65rem;text-align:left}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}details{{margin:1rem 0;padding:.75rem;border:1px solid #85929e}}@media print{{body{{font-size:11pt;max-width:none}}details{{display:block}}}}</style></head>
<body><header><p>Owner-scoped synthetic evidence</p></header><main><h1>Lyren Moss v679-v4 terminal evidence report</h1>
<p>The primary pillar is THOS Body through wholly synthetic museum environmental-monitoring log documentation. No real reading, collection decision, action, identity, or authority claim is present.</p>
<table><caption>Terminal truth summary</caption><tbody>{table}</tbody></table>
<section aria-labelledby="boundaries"><h2 id="boundaries">Boundaries</h2><p>Same-owner bounded validation is not a full-repository suite, external audit, independent reproduction, production certification, exhaustive security, complete privacy, or complete accessibility assurance.</p></section>
<details><summary>Relational language boundary</summary><p>Names, roles, hopes, and family language are working language only and are not evidence of consciousness, personhood, continuity, qualification, agency, or authority.</p></details>
<section aria-labelledby="route"><h2 id="route">Route state</h2><p>PREPARED_NOT_SENT. Ilyra Fen may be contacted at most once only after the exact terminal gate and fresh live route checks.</p></section>
</main><footer><p>Terminal verdict: {html.escape(truth['terminal_verdict'])}</p></footer></body></html>
"""
    (FINAL / "terminal-report.html").write_text(document, encoding="utf-8", newline="\n")
    return {"markdown_words": len(markdown.split()), "html_bytes": len(document.encode("utf-8"))}


if __name__ == "__main__":
    truth = json.loads((PHASE / "x2" / "phase-truth.json").read_text(encoding="utf-8"))
    lifecycle = {"x1_head": "1fe28fafc308298e1043a9e2afbecf59c24c9866", "evidence_head": "b204dcbfbcb3d016ab18f4bebc5ef9dc56d9dee6"}
    print(json.dumps(render(truth, lifecycle), sort_keys=True))

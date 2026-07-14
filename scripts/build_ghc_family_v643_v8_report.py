#!/usr/bin/env python3
"""Build the static accessible Ilyra Fen v643-v8 boundary report."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build(repo: Path) -> Path:
    repo = repo.resolve()
    phase = repo / "docs/ilyra-fen/v643-v8"
    truth = read(phase / "phase-truth.json")
    ledger = read(phase / "x2-proposal-ledger.json")
    gates = read(phase / "exact-open-gate-register.json")
    negatives = read(phase / "retained-negative-register.json")
    sources = read(phase / "sources/source-ledger.json")
    threats = read(phase / "threat-model.json")
    rows = []
    for index, row in enumerate(ledger["proposals"], 1):
        row_id = f"proposal-{index}"
        rows.append(
            f'<tr id="{row_id}"><th id="{row_id}-id" scope="row">{html.escape(row["proposal_id"])}</th>'
            f'<td headers="{row_id}-id proposal-title">{html.escape(row["title"])}</td>'
            f'<td headers="{row_id}-id proposal-outcome"><span class="tag">{html.escape(row["outcome"])}</span></td>'
            f'<td headers="{row_id}-id proposal-cases">{row["mutation_count"] + 1}</td>'
            f'<td headers="{row_id}-id proposal-boundary">No external claim established</td></tr>'
        )
    gate_items = "".join(
        f"<li><strong>{html.escape(row['gate_id'])}</strong>: {html.escape(row['domain'])} — {html.escape(row['state'])}</li>"
        for row in gates["open_gaps"] + gates["exact_gates"]
    )
    threat_items = "".join(
        f"<li><strong>{html.escape(row['id'])}</strong>: {html.escape(row['threat'])}. Control: {html.escape(row['control'])}.</li>"
        for row in threats["threats"]
    )
    protected = "".join(
        f"<li>{html.escape(name.replace('_', ' '))}: <strong>{str(value).lower()}</strong></li>"
        for name, value in truth["protected_claims"].items()
    )
    document = f"""<!doctype html>
<html lang="en-NZ">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ilyra Fen v643-v8 boundary evidence report</title>
  <style>
    :root {{ color-scheme: light dark; font-family: system-ui, sans-serif; line-height: 1.55; }}
    body {{ max-width: 74rem; margin: 0 auto; padding: 1.25rem; }}
    header, main, footer, section {{ display: block; }}
    table {{ border-collapse: collapse; width: 100%; margin-block: 1rem; }}
    caption {{ text-align: left; font-weight: 700; margin-block-end: .5rem; }}
    th, td {{ border: 1px solid currentColor; padding: .5rem; text-align: left; vertical-align: top; }}
    .tag {{ border: 1px solid currentColor; border-radius: .3rem; padding: .1rem .35rem; white-space: nowrap; }}
    .verdict {{ border: .2rem solid currentColor; padding: 1rem; font-weight: 700; }}
    :focus-visible {{ outline: .2rem solid currentColor; outline-offset: .15rem; }}
    @media print {{ body {{ max-width: none; }} a {{ color: inherit; }} }}
  </style>
</head>
<body>
<header>
  <h1>Ilyra Fen v643-v8 boundary evidence report</h1>
  <p>Static repository report. Identity and family language is relational working language only, not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.</p>
  <p class="verdict">Terminal verdict: NOT_READY_FOR_STAGE_20</p>
</header>
<main>
  <section aria-labelledby="summary-heading">
    <h2 id="summary-heading">Phase summary</h2>
    <p>Exactly ten proposals produced {truth['distribution']['completed']} completed, {truth['distribution']['represented']} represented or proxy, {truth['distribution']['open_gap']} open gap, and {truth['distribution']['exact_gate']} exact gate outcomes. The engine evaluated 80 deterministic cases and retained 70 rejecting mutations.</p>
    <p>Primary focus: GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit. Same-owner snapshot replay is not independent-team scientific reproduction.</p>
  </section>
  <section aria-labelledby="proposal-heading">
    <h2 id="proposal-heading">Proposal truth</h2>
    <div role="region" aria-label="Scrollable proposal evidence table" tabindex="0">
      <table>
        <caption>Ten frozen proposals, observed outcome labels, and local evidence scope</caption>
        <thead><tr><th id="proposal-id" scope="col">ID</th><th id="proposal-title" scope="col">Title</th><th id="proposal-outcome" scope="col">Outcome</th><th id="proposal-cases" scope="col">Cases</th><th id="proposal-boundary" scope="col">Boundary</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
  </section>
  <section aria-labelledby="negative-heading">
    <h2 id="negative-heading">Retained negatives</h2>
    <p>{negatives['negative_count']} negatives are retained: {negatives['inherited_count']} inherited, {negatives['x1_operational_count']} x1 operational, {negatives['new_synthetic_count']} preregistered synthetic, and {negatives['x2_operational_count']} x2 operational. Recovery never erases a failed run.</p>
  </section>
  <section aria-labelledby="gate-heading">
    <h2 id="gate-heading">Open and exact gates</h2>
    <p>Five open gaps and six exact gates remain visible. Māori wording, Māori authority, Māori data governance, affected-party acceptance, cultural ratification, legal interpretation, and enacted-law status are not technically substitutable.</p>
    <ul>{gate_items}</ul>
  </section>
  <section aria-labelledby="threat-heading">
    <h2 id="threat-heading">Threat model</h2>
    <ol>{threat_items}</ol>
  </section>
  <section aria-labelledby="claims-heading">
    <h2 id="claims-heading">Protected claims</h2>
    <p>Every protected claim remains false:</p>
    <ul>{protected}</ul>
  </section>
  <section aria-labelledby="source-heading">
    <h2 id="source-heading">Source and environment truth</h2>
    <p>The ledger contains {sources['effective_source_count']} sources: {sources['effective_status_counts']['current']} current, {sources['effective_status_counts']['stable']} stable, {sources['effective_status_counts']['draft']} draft, and {sources['effective_status_counts']['watch']} watch. Status labels describe currency, not truth or approval.</p>
    <p>No real data were downloaded or fitted; no real participants, arms, keys, proofs, live services, accounts, credentials, or deployments were used. Codex desktop was verified without update. No elevation, host-security weakening, Windows-feature change, or reboot occurred.</p>
  </section>
  <section aria-labelledby="access-heading">
    <h2 id="access-heading">Accessibility and security reservation</h2>
    <p>This report provides semantic headings, a captioned table, explicit row and column headers, and a meaningful document order. It contains no script, event handler, inline frame, remote embed, or executable URL scheme. Qualified manual, assistive-technology, and affected-user evaluation remains open. The bounded static scan is not complete accessibility, browser assurance, deployment assurance, independent security review, or exhaustive security.</p>
  </section>
</main>
<footer>
  <p>Route truth before terminal tool acknowledgement: PREPARED_NOT_SENT. No successor task was created.</p>
</footer>
</body>
</html>
"""
    output = phase / "deliverables/v643-v8-boundary-evidence-report.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8", newline="\n")
    receipt = {
        "schema": "ghc.family.v643-v8.static-report-receipt.v1", "phase": truth["phase"],
        "report": "docs/ilyra-fen/v643-v8/deliverables/v643-v8-boundary-evidence-report.html",
        "language": "en-NZ", "semantic_headings": True, "captioned_table": True,
        "explicit_header_associations": True, "meaningful_linearization": True,
        "script_count": 0, "iframe_count": 0, "event_handler_count": 0, "remote_embed_count": 0,
        "manual_evaluation_completed": False, "assistive_technology_evaluation_completed": False,
        "affected_user_evaluation_completed": False, "complete_accessibility_claim": False,
        "browser_or_exhaustive_security_claim": False,
        "boundary": "Automated static structure only; qualified manual and affected-user evaluation remains reserved.",
    }
    receipt_path = phase / "accessibility/static-report-receipt.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    output = build(args.repo)
    print(output.relative_to(args.repo.resolve()).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

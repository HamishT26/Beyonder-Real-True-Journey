#!/usr/bin/env python3
"""Build the accessible static v642-v6 evidence-integrity report."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def table(headers: list[str], rows: list[list[Any]], caption: str) -> str:
    head = "".join(f"<th scope=\"col\">{esc(item)}</th>" for item in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{esc(item)}</td>" for item in row) + "</tr>"
        for row in rows
    )
    return f"<div class=\"table-wrap\"><table><caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def build(phase: Path) -> Path:
    ledger = load(phase / "x2-proposal-ledger.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    truth = load(phase / "phase-truth.json")
    sources = load(phase / "sources/source-ledger.json")
    threat = load(phase / "threat-model.json")
    focus = load(phase / "focus/primary-focus-receipt.json")
    checklist = load(phase / "complete-incomplete-checklist.json")

    proposal_rows = [
        [
            row["proposal_id"],
            row["title"],
            row["expected_disposition"],
            row["observed_disposition"],
            row["evidence_class"],
            f"{row['matched_count']}/{row['case_count']}",
            row["retained_negative_count"],
        ]
        for row in ledger["rows"]
    ]
    open_rows = [[row["gate_id"], row["surface"], "; ".join(row["needs"])] for row in gates["open_gaps"]]
    exact_rows = [[row["gate_id"], row["surface"], "; ".join(row["reserved_to"])] for row in gates["exact_gates"]]
    threat_rows = [[row["threat_id"], row["class"], row["failure"], row["control"], row["residual_risk"]] for row in threat["threats"]]
    checklist_rows = [[row["item"], "complete" if row["complete"] else "incomplete"] for row in checklist["required_rows"]]

    distribution = ledger["observed_distribution"]
    output = phase / "deliverables/v642-v6-evidence-integrity-report.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>Orin Thale v642-v6 evidence-integrity report</title>
  <style>
    :root {{ --ink:#172033; --paper:#f7f4ec; --panel:#ffffff; --accent:#155e75; --line:#667085; --warn:#8a3b12; --ok:#166534; }}
    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; }}
    body {{ margin:0; font:1rem/1.6 system-ui,-apple-system,"Segoe UI",sans-serif; color:var(--ink); background:var(--paper); }}
    a {{ color:#075985; }}
    .skip-link {{ position:absolute; left:.75rem; top:-5rem; padding:.75rem 1rem; color:#fff; background:#000; z-index:10; }}
    .skip-link:focus {{ top:.75rem; }}
    :focus-visible {{ outline:3px solid #f59e0b; outline-offset:3px; }}
    header, main, footer {{ width:min(76rem, calc(100% - 2rem)); margin-inline:auto; }}
    header {{ padding:2.5rem 0 1rem; }}
    nav ul {{ display:flex; flex-wrap:wrap; gap:.5rem 1rem; padding:0; list-style:none; }}
    main {{ padding-bottom:3rem; }}
    section {{ margin:1.25rem 0; padding:1.25rem; background:var(--panel); border:1px solid #c7cdd6; border-radius:.65rem; }}
    h1 {{ max-width:30ch; line-height:1.15; }}
    h2 {{ margin-top:0; }}
    .lede {{ max-width:75ch; font-size:1.08rem; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(12rem,1fr)); gap:.75rem; }}
    .card {{ padding:1rem; border:1px solid #b8c0cc; border-radius:.5rem; background:#fff; color:#111827; }}
    .card strong {{ display:block; font-size:1.5rem; }}
    .not-ready {{ border-left:.45rem solid var(--warn); }}
    .bounded {{ border-left:.45rem solid var(--ok); }}
    .table-wrap {{ overflow-x:auto; }}
    table {{ width:100%; border-collapse:collapse; min-width:42rem; }}
    caption {{ text-align:left; font-weight:700; padding:.5rem 0; }}
    th, td {{ border:1px solid #98a2b3; padding:.55rem; text-align:left; vertical-align:top; }}
    th {{ background:#e7eef3; color:#111827; }}
    code {{ overflow-wrap:anywhere; }}
    footer {{ padding:1rem 0 2rem; }}
    @media (prefers-color-scheme:dark) {{
      :root {{ --ink:#edf2f7; --paper:#0f172a; --panel:#111827; --line:#cbd5e1; }}
      a {{ color:#7dd3fc; }} .card {{ background:#182235; color:#edf2f7; }} th {{ background:#243247; color:#fff; }}
    }}
    @media (prefers-reduced-motion:reduce) {{ html {{ scroll-behavior:auto; }} *,*::before,*::after {{ animation-duration:.01ms!important; transition-duration:.01ms!important; }} }}
    @media print {{ .skip-link, nav {{ display:none; }} body {{ background:#fff; color:#000; }} section {{ break-inside:avoid; border-color:#555; }} }}
  </style>
</head>
<body>
<a class="skip-link" href="#main">Skip to report content</a>
<header>
  <p>GHC Family · v642-v6 · bounded repository evidence</p>
  <h1>Evidence integrity without authority substitution</h1>
  <p class="lede">Orin Thale's solo phase tests ten preregistered structural, synthetic, protocol, and exact-gated surfaces. Local checks remain local: they do not become empirical confirmation, human-subject approval, production identity assurance, Māori authority, legal or cultural ratification, consciousness, personhood, deployment, or independent-team reproduction.</p>
  <nav aria-label="Report sections"><ul>
    <li><a href="#summary">Summary</a></li><li><a href="#proposals">Proposals</a></li><li><a href="#gates">Gates</a></li><li><a href="#threats">Threat model</a></li><li><a href="#checklist">Checklist</a></li><li><a href="#accessibility">Accessibility</a></li>
  </ul></nav>
</header>
<main id="main" tabindex="-1">
  <section id="summary" aria-labelledby="summary-heading">
    <h2 id="summary-heading">Phase summary</h2>
    <div class="cards" role="list">
      <div class="card" role="listitem"><strong>10</strong>preregistered and executed proposal rows</div>
      <div class="card" role="listitem"><strong>{ledger['total_matched_count']}/{ledger['total_case_count']}</strong>case expectations matched</div>
      <div class="card" role="listitem"><strong>{distribution['completed']} / {distribution['represented']} / {distribution['open_gap']} / {distribution['exact_gate']}</strong>completed / represented / open gap / exact gate</div>
      <div class="card" role="listitem"><strong>{negatives['negative_count']}</strong>retained negatives ({negatives['inherited_count']} inherited)</div>
      <div class="card" role="listitem"><strong>{sources['effective_source_count']}</strong>effective primary or official source records</div>
      <div class="card" role="listitem"><strong>{gates['open_gap_count']} / {gates['exact_gate_count']}</strong>open gaps / exact gates</div>
    </div>
    <p class="not-ready"><strong>Terminal verdict: {esc(truth['terminal_verdict'])}.</strong> Repository completion cannot compensate for absent empirical, participant, production, privacy, authority, independent-review, or independent-reproduction evidence.</p>
    <p class="bounded"><strong>Primary focus:</strong> {esc(focus['primary_focus']['surface'])} ({esc(focus['primary_focus']['pillar'])}), while GMUT (Mind) and THOS (Body) remain explicit and non-substitutable.</p>
  </section>
  <section id="proposals" aria-labelledby="proposals-heading">
    <h2 id="proposals-heading">Proposal evidence ledger</h2>
    <p>Each row has eight deterministic cases: one bounded canonical fixture and seven retained falsifiers. A completed row means only that its local artifact and tests passed.</p>
    {table(['ID','Proposal','Expected','Observed','Evidence class','Cases','New negatives'], proposal_rows, 'Ten v642-v6 proposal outcomes')}
  </section>
  <section id="gates" aria-labelledby="gates-heading">
    <h2 id="gates-heading">Open and exact gates</h2>
    <p>Missing evidence remains an open gap. Decisions reserved to competent people or institutions remain exact gates. Neither is a defect to be narrated away.</p>
    {table(['Gate','Surface','Needed evidence'], open_rows, 'Five open evidence gaps')}
    {table(['Gate','Surface','Reserved authority'], exact_rows, 'Six exact authority gates')}
  </section>
  <section id="threats" aria-labelledby="threats-heading">
    <h2 id="threats-heading">Threat model</h2>
    <p>This bounded model tracks artifact and claim-integrity risks. It is not exhaustive security and has not received independent security review.</p>
    {table(['ID','Class','Failure','Control','Residual'], threat_rows, 'Twelve bounded threats and controls')}
  </section>
  <section id="checklist" aria-labelledby="checklist-heading">
    <h2 id="checklist-heading">Complete / incomplete checklist</h2>
    <p>Candidate execution is not closeout. Detached validation, seal, final equality, and the routing gate remain separate.</p>
    {table(['Required item','State'], checklist_rows, 'Current closeout checklist state')}
  </section>
  <section id="accessibility" aria-labelledby="accessibility-heading">
    <h2 id="accessibility-heading">Accessibility boundary</h2>
    <p>This static report uses semantic headings, a skip link, keyboard-visible focus, labeled navigation, table captions and headers, responsive overflow, print styles, strong contrast choices, and reduced-motion handling. It contains no client-side script and remains usable without network access.</p>
    <p><strong>Manual and user accessibility evaluation remains reserved.</strong> Automated structure and author review do not establish complete WCAG conformance or affected-user acceptance.</p>
  </section>
  <section aria-labelledby="claims-heading">
    <h2 id="claims-heading">Protected claims</h2>
    <p>No deployment, production-readiness, exhaustive-security, complete-accessibility, proof/canon, empirical-confirmation, legal/cultural-ratification, independent-team-reproduction, consciousness/personhood, AGI/ASI, or Theory-of-Everything claim is made. Same-owner clean snapshots remain same-owner repeatability.</p>
  </section>
</main>
<footer><p>Static owner-scoped report. No private routes, raw task IDs, credentials, transcripts, screenshots, session streams, or private local paths are included.</p></footer>
</body>
</html>
"""
    output.write_text(document, encoding="utf-8", newline="\n")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", required=True)
    args = parser.parse_args()
    output = build(Path(args.phase_dir).resolve())
    print(json.dumps({"report": output.name, "bytes": output.stat().st_size}))


if __name__ == "__main__":
    main()

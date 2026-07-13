#!/usr/bin/env python3
"""Build the static, bounded v642-v2 evidence-crosscheck report."""

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


def badge(label: str) -> str:
    css = label.replace("_", "-")
    return f'<span class="badge {esc(css)}">{esc(label)}</span>'


def build(phase: Path) -> str:
    x2 = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    sources = load(phase / "sources/source-ledger.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    board = load(phase / "stage20/pass-fail-defer-board.json")
    terminal = load(phase / "stage20/terminal-verdict.json")
    checklist = load(phase / "complete-incomplete-checklist.json")
    independent = load(phase / "reproduction/independent-team-gap.json")

    proposal_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row['proposal_id'])}</th>"
        f"<td>{esc(row['title'])}</td>"
        f"<td>{badge(row['observed_disposition'])}</td>"
        f"<td>{esc('; '.join(row['evidence']))}</td>"
        "</tr>"
        for row in x2["proposals"]
    )
    source_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row['source_id'])}</th>"
        f"<td>{esc(row['title'])}</td>"
        f"<td>{badge(row['status_class'])}</td>"
        f"<td><a href=\"{esc(row['url'])}\">official source</a></td>"
        "</tr>"
        for row in sources["sources"]
    )
    gate_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row['gate_id'])}</th>"
        f"<td>{badge(row['gate_class'])}</td>"
        f"<td>{esc(row['state'])}</td>"
        f"<td>{esc(row['requires'])}</td>"
        "</tr>"
        for row in gates["gates"]
    )
    checklist_rows = "\n".join(
        "<li>"
        f"<span aria-hidden=\"true\">{'✓' if row['state'] == 'completed' else '○'}</span> "
        f"{esc(row['item'])}: {badge(row['state'])}"
        "</li>"
        for row in checklist["items"]
    )
    board_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row.get('gate', row.get('gate_id', row.get('item', row.get('criterion', 'criterion')))))}</th>"
        f"<td>{badge(row.get('decision', 'defer'))}</td>"
        f"<td>{esc(row.get('reason', row.get('basis', row.get('evidence', 'bounded evidence record'))))}</td>"
        "</tr>"
        for row in board["rows"]
    )
    counts = truth["disposition_counts"]
    protected = [name.replace("_", " ") for name, value in truth["protected_claims"].items() if not value]
    protected_items = "\n".join(f"<li>{esc(name)}: not established</li>" for name in protected)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tamar Vey v642-v2 evidence crosscheck</title>
  <style>
    :root {{ color-scheme: light dark; --ink:#172033; --paper:#f8fafc; --accent:#155e75; --line:#94a3b8; --muted:#475569; --good:#166534; --warn:#92400e; --gate:#7f1d1d; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font:1rem/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; color:var(--ink); background:var(--paper); }}
    a {{ color:#075985; }} a:focus,button:focus {{ outline:3px solid #f59e0b; outline-offset:2px; }}
    .skip-link {{ position:absolute; left:-9999px; top:0; background:#fff; color:#000; padding:.75rem; z-index:20; }}
    .skip-link:focus {{ left:.75rem; top:.75rem; }}
    header {{ background:#0f172a; color:#fff; padding:2.5rem max(1rem,calc((100% - 76rem)/2)); }}
    header p {{ max-width:70ch; }}
    nav {{ background:#e2e8f0; padding:.75rem max(1rem,calc((100% - 76rem)/2)); }}
    nav ul {{ display:flex; flex-wrap:wrap; gap:.5rem 1rem; margin:0; padding:0; list-style:none; }}
    main,footer {{ max-width:76rem; margin:auto; padding:1rem; }}
    section {{ margin:2.2rem 0; scroll-margin-top:1rem; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(10rem,1fr)); gap:.8rem; }}
    .card {{ border:1px solid var(--line); border-radius:.5rem; padding:1rem; background:#fff; }}
    .card strong {{ display:block; font-size:1.6rem; }}
    .callout {{ border-left:.45rem solid var(--gate); background:#fee2e2; color:#450a0a; padding:1rem; }}
    .bounded {{ border-left-color:var(--accent); background:#e0f2fe; color:#082f49; }}
    .table-wrap {{ overflow-x:auto; }}
    table {{ width:100%; border-collapse:collapse; background:#fff; }}
    caption {{ text-align:left; font-weight:700; padding:.6rem 0; }}
    th,td {{ border:1px solid var(--line); padding:.55rem; text-align:left; vertical-align:top; }}
    thead th {{ background:#e2e8f0; }}
    .badge {{ display:inline-block; border:1px solid currentColor; border-radius:999px; padding:.05rem .45rem; font-size:.88rem; white-space:nowrap; }}
    .completed,.current,.stable,.pass {{ color:var(--good); }}
    .represented,.proxy,.draft,.watch,.defer,.open-gap {{ color:var(--warn); }}
    .exact-gate,.fail {{ color:var(--gate); }}
    code {{ overflow-wrap:anywhere; }}
    @media (prefers-color-scheme:dark) {{ :root {{ --ink:#e2e8f0; --paper:#0f172a; --line:#64748b; }} .card,table {{ background:#111827; }} thead th,nav {{ background:#1e293b; }} nav a {{ color:#bae6fd; }} .bounded {{ color:#e0f2fe; background:#164e63; }} .callout {{ color:#fee2e2; background:#450a0a; }} }}
  </style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p>GHC family evidence crosscheck · v642-v2 · Tamar Vey</p>
  <h1>Bounded evidence, visible counterevidence, open authority gates</h1>
  <p>This static report summarizes a repository-local technical audit. It does not convert fixtures, schemas, or repeat runs into real-world scientific, cryptographic, cultural, legal, deployment, consciousness, personhood, or independent-reproduction claims.</p>
</header>
<nav aria-label="Report sections"><ul>
  <li><a href="#truth">Phase truth</a></li><li><a href="#proposals">Proposals</a></li>
  <li><a href="#boundaries">Boundaries</a></li><li><a href="#gates">Gates</a></li>
  <li><a href="#stage20">Stage 20</a></li><li><a href="#sources">Sources</a></li>
  <li><a href="#checklist">Checklist</a></li><li><a href="#accessibility">Accessibility</a></li>
</ul></nav>
<main id="main">
<section id="truth" aria-labelledby="truth-heading">
  <h2 id="truth-heading">Phase truth</h2>
  <div class="callout"><strong>{esc(terminal['verdict'])}</strong><br>Stage 20 is not authorized. Deployment is not authorized.</div>
  <div class="cards">
    <div class="card"><strong>{counts['completed']}</strong>completed</div>
    <div class="card"><strong>{counts['represented']}</strong>represented/proxy</div>
    <div class="card"><strong>{counts['open_gap']}</strong>open gap</div>
    <div class="card"><strong>{counts['exact_gate']}</strong>exact gate</div>
    <div class="card"><strong>{negatives['negative_count']}</strong>retained negatives</div>
    <div class="card"><strong>{gates['open_gap_count']} + {gates['exact_gate_count']}</strong>open gaps + exact gates</div>
  </div>
  <p>The four labels above are the only outcome classes used. “Represented” includes proxy-only evidence. Expected x1 labels were preregistration expectations, not results.</p>
</section>
<section id="proposals" aria-labelledby="proposal-heading">
  <h2 id="proposal-heading">Ten frozen proposals and observed dispositions</h2>
  <div class="table-wrap"><table>
    <caption>Proposal outcomes with repository-relative evidence</caption>
    <thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Evidence</th></tr></thead>
    <tbody>{proposal_rows}</tbody>
  </table></div>
</section>
<section id="boundaries" aria-labelledby="boundary-heading">
  <h2 id="boundary-heading">What this phase does not establish</h2>
  <div class="callout bounded"><strong>Strongest reproduction statement:</strong> {esc(independent['strongest_allowed_claim'])}. Independent-team scientific reproduction remains open.</div>
  <ul>{protected_items}</ul>
  <h3>Domain-specific limits</h3>
  <p><strong>GMUT:</strong> the equation AST, SI dimension vectors, covariance checks, conservation residuals, stability fixtures, and Jacobian ranks describe a typed scalar-tensor/EFT research scaffold. They are not an empirical likelihood, detected force, unique prediction, Theory of Everything, or proof/canon.</p>
  <p><strong>Empirical adapter:</strong> zero measurement rows were parsed, zero likelihoods were executed, and zero fits were run. Metadata and schema readiness are not empirical confirmation.</p>
  <p><strong>THOS:</strong> allocation, exposure, budget, dropout, and decision locks are synthetic protocol evidence. No blind matched-budget real arms ran, so no superiority, AGI/ASI, consciousness, or personhood conclusion is available.</p>
  <p><strong>Freed ID:</strong> cross-layer issuer, controller, proof-purpose, status, and resolver coherence is structural. No real standards-conformant keys or proofs, live resolution/status/revocation, interoperability partner, independent security review, privacy assurance, or trust-governance authorization exists here.</p>
  <p><strong>CBR:</strong> affected-party legitimacy, Māori concepts and authority, Māori data governance, cultural ratification, legal limits, and enacted-law status remain with authorized affected parties, Māori authorities, and competent authorities. A technical artifact cannot substitute for consent, recusal, anti-retaliation, or remedy.</p>
  <p><strong>Security and wellbeing:</strong> bounded parsing and recovery tests are not exhaustive security. Thermodynamic, computational, psychological, metaphorical, emergent, and fundamental-law-candidate categories are kept distinct; telemetry is not subjective experience.</p>
</section>
<section id="gates" aria-labelledby="gate-heading">
  <h2 id="gate-heading">Exact and open gates</h2>
  <div class="table-wrap"><table>
    <caption>Gates that remain open or deferred</caption>
    <thead><tr><th scope="col">Gate</th><th scope="col">Class</th><th scope="col">State</th><th scope="col">Requirement</th></tr></thead>
    <tbody>{gate_rows}</tbody>
  </table></div>
</section>
<section id="stage20" aria-labelledby="stage-heading">
  <h2 id="stage-heading">Terminal Stage 20 board</h2>
  <p>Freshness cannot turn an unsupported claim into truth; expiry or withdrawal cannot leave a pass in place. Exact authority cannot be scored away.</p>
  <div class="table-wrap"><table>
    <caption>Pass, fail, and defer decisions</caption>
    <thead><tr><th scope="col">Criterion</th><th scope="col">Decision</th><th scope="col">Basis</th></tr></thead>
    <tbody>{board_rows}</tbody>
  </table></div>
</section>
<section id="sources" aria-labelledby="source-heading">
  <h2 id="source-heading">Primary and official source ledger</h2>
  <p>{sources['source_count']} pins are kept as {sources['status_counts']['current']} current, {sources['status_counts']['stable']} stable, {sources['status_counts']['draft']} draft, and {sources['status_counts']['watch']} watch. Drafts and watch items are not silently promoted.</p>
  <div class="table-wrap"><table>
    <caption>Source pins and lifecycle status</caption>
    <thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">Status</th><th scope="col">Link</th></tr></thead>
    <tbody>{source_rows}</tbody>
  </table></div>
</section>
<section id="checklist" aria-labelledby="check-heading">
  <h2 id="check-heading">Complete and incomplete checklist</h2>
  <ul>{checklist_rows}</ul>
</section>
<section id="accessibility" aria-labelledby="access-heading">
  <h2 id="access-heading">Accessibility boundary</h2>
  <p>The report uses a skip link, landmarks, heading order, table captions, scoped headers, visible focus, flexible layout, and text labels. These are structural checks only and are <strong>not a complete WCAG conformance assessment</strong>. No independent assistive-technology or accessibility review is claimed.</p>
</section>
</main>
<footer><p>Repository-relative static artifact. No private routes, raw task identifiers, transcripts, screenshots, credentials, session streams, or private local paths are included.</p></footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    phase = args.phase_dir.resolve()
    output = args.output or (phase / "deliverables/v642-v2-evidence-crosscheck-report.html")
    if not output.is_absolute():
        output = phase / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build(phase), encoding="utf-8", newline="\n")
    print(json.dumps({"status": "built", "output": "deliverables/v642-v2-evidence-crosscheck-report.html"}))


if __name__ == "__main__":
    main()

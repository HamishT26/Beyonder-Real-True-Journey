#!/usr/bin/env python3
"""Build an accessible static report for a GHC gate-resilience packet."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: object) -> str:
    return html.escape(str(value))


def build(phase: Path, output: Path) -> None:
    ledger = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    board = load(phase / "stage20/terminal-evidence-board.json")
    gates = load(phase / "exact-open-gate-register.json")
    negatives = load(phase / "retained-negative-register.json")
    sources = load(phase / "sources/source-ledger.json")
    commitment = load(phase / "reproduction/blinded-output-commitment.json")
    checklist = load(phase / "complete-incomplete-checklist.json")
    overview = (phase / "v641-v8-integrated-overview.md").read_text(encoding="utf-8")

    proposal_rows = "\n".join(
        f"<tr><th scope=\"row\">{esc(row['proposal_id'])}</th><td>{esc(row['disposition'])}</td><td>{esc(row['result'])}</td><td><code>{esc(', '.join(row['evidence']))}</code></td></tr>"
        for row in ledger["proposals"]
    )
    board_rows = "\n".join(
        f"<tr><th scope=\"row\">{esc(row['board_id'])}</th><td>{esc(row['claim'])}</td><td>{esc(row['decision'])}</td><td>{esc(', '.join(row['blocking_if']))}</td></tr>"
        for row in board["board"]
    )
    gate_rows = "\n".join(
        f"<tr><th scope=\"row\">{esc(row['gate_id'])}</th><td>{esc(row['surface'])}</td><td>{esc(row['state'])}</td></tr>"
        for row in gates["gates"]
    )
    source_rows = "\n".join(
        f"<tr><th scope=\"row\">{esc(row['source_id'])}</th><td><a href=\"{esc(row['url'])}\">{esc(row['title'])}</a></td><td>{esc(row['authority'])}</td><td>{esc(row['status_class'])}</td><td>{esc(row['evidence_role'])}</td></tr>"
        for row in sources["sources"]
    )
    complete_items = "\n".join(f"<li>{esc(item)}</li>" for item in checklist["complete"])
    incomplete_items = "\n".join(f"<li>{esc(item)}</li>" for item in checklist["incomplete"])
    overview_paragraphs = []
    for block in overview.split("\n\n"):
        block = block.strip()
        if not block or block.startswith("#"):
            continue
        overview_paragraphs.append(f"<p>{esc(block)}</p>")
    overview_html = "\n".join(overview_paragraphs[:12])

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Elian Voss v641-v8 gate-resilience evidence report</title>
<style>
:root {{ color-scheme: light dark; --accent: #275d75; --panel: #eef5f7; --ink: #182126; --border: #73858d; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; line-height: 1.55; color: var(--ink); background: #fff; }}
.skip-link {{ position: absolute; left: -9999px; top: 0; padding: .75rem; background: #fff; color: #000; z-index: 10; }}
.skip-link:focus {{ left: .5rem; }}
header, main, footer {{ max-width: 78rem; margin: auto; padding: 1rem 1.25rem; }}
header {{ border-bottom: 4px solid var(--accent); }}
nav ul {{ display: flex; flex-wrap: wrap; gap: .8rem; padding: 0; list-style: none; }}
nav a {{ color: #124d66; font-weight: 650; }}
.status {{ padding: 1rem; border: 2px solid #8a3b12; background: #fff2e8; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); gap: 1rem; }}
.card {{ padding: 1rem; border: 1px solid var(--border); background: var(--panel); }}
table {{ width: 100%; border-collapse: collapse; margin: 1rem 0 2rem; }}
caption {{ text-align: left; font-weight: 750; padding: .5rem 0; }}
th, td {{ border: 1px solid var(--border); padding: .55rem; vertical-align: top; text-align: left; }}
thead th {{ background: #d9ebf0; color: #102026; }}
code {{ overflow-wrap: anywhere; }}
.boundary {{ border-left: .45rem solid #8a3b12; padding: .8rem 1rem; background: #fff2e8; }}
@media (prefers-color-scheme: dark) {{ body {{ background: #11181c; color: #eef5f7; }} .card {{ background: #1c2b32; }} .status, .boundary {{ background: #3a2418; }} nav a {{ color: #8ed3ef; }} thead th {{ background: #263f49; color: #fff; }} }}
@media print {{ nav, .skip-link {{ display: none; }} body {{ color: #000; background: #fff; }} }}
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main evidence</a>
<header>
  <p>GHC family evidence packet</p>
  <h1>Elian Voss v641-v8 gate-resilience report</h1>
  <p>Relational working identity only; not evidence of consciousness or legal personhood.</p>
  <nav aria-label="Report sections"><ul>
    <li><a href="#summary">Summary</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#stage20">Stage 20</a></li>
    <li><a href="#gates">Open gates</a></li><li><a href="#sources">Sources</a></li><li><a href="#boundaries">Boundaries</a></li>
  </ul></nav>
</header>
<main id="main">
<section id="summary" aria-labelledby="summary-heading">
<h2 id="summary-heading">Summary</h2>
<div class="status"><strong>Terminal verdict: {esc(truth['terminal_verdict'])}</strong>. Stage 20 is not complete.</div>
<div class="grid">
  <div class="card"><h3>Proposals</h3><p>{esc(ledger['proposal_count'])} executed as far as evidence permits.</p></div>
  <div class="card"><h3>Disposition</h3><p>{esc(ledger['disposition_counts'])}</p></div>
  <div class="card"><h3>Retained negatives</h3><p>{esc(negatives['negative_count'])} total; none erased.</p></div>
  <div class="card"><h3>Commitment</h3><p>{esc(commitment['artifact_count'])} normalized core hashes.</p></div>
</div>
{overview_html}
</section>
<section id="outcomes" aria-labelledby="outcome-heading">
<h2 id="outcome-heading">Proposal outcomes</h2>
<table><caption>Ten frozen v8 proposals and their bounded dispositions</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Result</th><th scope="col">Evidence</th></tr></thead><tbody>{proposal_rows}</tbody></table>
</section>
<section id="stage20" aria-labelledby="stage-heading">
<h2 id="stage-heading">Stage 20 terminal board</h2>
<table><caption>Pass, fail, and defer decisions that drive the terminal stop rule</caption><thead><tr><th scope="col">Board ID</th><th scope="col">Claim</th><th scope="col">Decision</th><th scope="col">Blocking states</th></tr></thead><tbody>{board_rows}</tbody></table>
</section>
<section id="gates" aria-labelledby="gate-heading">
<h2 id="gate-heading">Open and exact gates</h2>
<table><caption>Evidence and authority gates that remain visibly open</caption><thead><tr><th scope="col">Gate</th><th scope="col">Surface</th><th scope="col">State</th></tr></thead><tbody>{gate_rows}</tbody></table>
<div class="grid"><div><h3>Completed locally</h3><ul>{complete_items}</ul></div><div><h3>Incomplete or exact-gated</h3><ul>{incomplete_items}</ul></div></div>
</section>
<section id="sources" aria-labelledby="source-heading">
<h2 id="source-heading">Primary and official sources</h2>
<table><caption>Current source ledger with stable, current, draft, and watch distinctions</caption><thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">Authority</th><th scope="col">Status</th><th scope="col">Evidence role</th></tr></thead><tbody>{source_rows}</tbody></table>
</section>
<section id="boundaries" aria-labelledby="boundary-heading">
<h2 id="boundary-heading">Claim and accessibility boundaries</h2>
<div class="boundary"><p>This report establishes bounded local engineering and evidence-management results only. It does not establish empirical GMUT confirmation, a Theory of Everything, THOS superiority, AGI/ASI, consciousness or personhood, production Freed ID cryptography, enacted law, cultural ratification, Māori authority, deployment, exhaustive security, independent scientific reproduction, or complete accessibility conformance.</p></div>
<p>Māori concepts, language, data, and governance remain under Māori authority. No artifact can substitute for authorized affected parties or competent legal and cultural authorities.</p>
<p>The document includes structural accessibility features such as a language declaration, skip link, landmarks, headings, captions, and scoped headers. These checks are <strong>not a complete WCAG conformance assessment</strong> and require independent human review.</p>
</section>
</main>
<footer><p>Static evidence report generated from repository artifacts. No private task route, credential, transcript, screenshot, or local absolute path is included.</p></footer>
</body>
</html>
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    phase = args.phase_dir.resolve()
    output = args.output.resolve() if args.output else phase / "deliverables/v641-v8-gate-resilience-report.html"
    build(phase, output)
    print(json.dumps({"output": output.as_posix(), "status": "built"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

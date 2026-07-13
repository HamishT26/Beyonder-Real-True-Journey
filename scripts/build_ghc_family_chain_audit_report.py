#!/usr/bin/env python3
"""Build an accessible static report for the v641-v7 chain audit."""

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
    x2 = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    board = load(phase / "stage20/terminal-evidence-board.json")
    gates = load(phase / "exact-open-gate-register.json")
    negatives = load(phase / "retained-negative-register.json")
    sources = load(phase / "sources/source-ledger.json")
    checklist = load(phase / "complete-incomplete-checklist.json")
    overview = (phase / "v641-v7-integrated-overview.md").read_text(encoding="utf-8")

    proposal_rows = "\n".join(
        f"<tr><th scope=\"row\">{esc(row['proposal_id'])}</th><td>{esc(row['title'])}</td><td><span class=\"tag {esc(row['observed_disposition'])}\">{esc(row['observed_disposition'])}</span></td></tr>"
        for row in x2["proposals"]
    )
    board_rows = "\n".join(
        f"<tr><th scope=\"row\">{esc(row['board_id'])}</th><td>{esc(row['claim'])}</td><td><span class=\"tag {esc(row['decision'])}\">{esc(row['decision'])}</span></td><td>{esc(row['falsifier'])}</td><td>{esc(row['expiry_or_reopen'])}</td></tr>"
        for row in board["board"]
    )
    gate_rows = "\n".join(
        f"<tr><th scope=\"row\">{esc(row['gate'])}</th><td><span class=\"tag {esc(row['state'])}\">{esc(row['state'])}</span></td></tr>"
        for row in gates["gates"]
    )
    source_rows = "\n".join(
        f"<tr><th scope=\"row\">{esc(row['source_id'])}</th><td><a href=\"{esc(row['url'])}\">{esc(row['title'])}</a></td><td>{esc(row['authority'])}</td><td>{esc(row['status_class'])}</td><td>{esc(row['evidence_role'])}</td></tr>"
        for row in sources["sources"]
    )
    negative_rows = "\n".join(
        f"<tr><th scope=\"row\">{esc(row['negative_id'])}</th><td>{esc(row.get('origin',''))}</td><td>{esc(row.get('observed',''))}</td><td>{'retained' if row.get('retained') else 'not retained'}</td></tr>"
        for row in negatives["negatives"]
    )
    complete_items = "\n".join(f"<li>{esc(item)}</li>" for item in checklist["complete"])
    incomplete_items = "\n".join(f"<li>{esc(item)}</li>" for item in checklist["incomplete"])

    overview_sections = []
    for block in overview.split("\n\n"):
        block = block.strip()
        if not block or block.startswith("# Sable"):
            continue
        if block.startswith("## "):
            overview_sections.append(f"<h3>{esc(block[3:])}</h3>")
        elif block.startswith("`") and block.endswith("`"):
            overview_sections.append(f"<pre><code>{esc(block.strip('`'))}</code></pre>")
        else:
            overview_sections.append(f"<p>{esc(block)}</p>")
    overview_html = "\n".join(overview_sections)

    counts = x2["disposition_counts"]
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sable Rook v641-v7 chain audit</title>
<style>
:root {{ color-scheme: light dark; --bg:#f7f8fb; --surface:#fff; --text:#172033; --muted:#526077; --line:#c7cfdb; --accent:#334fd1; --good:#176b45; --warn:#8a5a00; --bad:#a32020; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#10141d; --surface:#171d28; --text:#eef2fb; --muted:#b5bfd0; --line:#3d4658; --accent:#9cb0ff; --good:#73d6a9; --warn:#f2c46d; --bad:#ff9c9c; }} }}
* {{ box-sizing:border-box; }} body {{ margin:0; font:1rem/1.55 system-ui,sans-serif; color:var(--text); background:var(--bg); }}
a {{ color:var(--accent); }} a:focus-visible, summary:focus-visible {{ outline:3px solid var(--accent); outline-offset:3px; }}
.skip-link {{ position:absolute; left:-999px; top:0; background:var(--surface); padding:.75rem; z-index:10; }} .skip-link:focus {{ left:.5rem; }}
header, main, footer {{ max-width:78rem; margin:auto; padding:1rem 1.25rem; }} nav ul {{ display:flex; flex-wrap:wrap; gap:.75rem; padding:0; list-style:none; }}
.hero, section {{ background:var(--surface); border:1px solid var(--line); border-radius:.75rem; padding:1.25rem; margin:1rem 0; }}
.verdict {{ border-left:.45rem solid var(--bad); }} .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(10rem,1fr)); gap:.75rem; }}
.card {{ border:1px solid var(--line); border-radius:.5rem; padding:1rem; }} .card strong {{ display:block; font-size:1.6rem; }}
.table-wrap {{ overflow-x:auto; }} table {{ width:100%; border-collapse:collapse; }} caption {{ text-align:left; font-weight:700; padding:.75rem 0; }}
th,td {{ border:1px solid var(--line); padding:.6rem; text-align:left; vertical-align:top; }} thead th {{ background:color-mix(in srgb,var(--surface),var(--accent) 10%); }}
.tag {{ display:inline-block; border:1px solid currentColor; border-radius:999px; padding:.05rem .45rem; font-weight:650; }}
.completed,.pass {{ color:var(--good); }} .represented,.defer,.open_gap {{ color:var(--warn); }} .exact_gate,.fail {{ color:var(--bad); }}
code,pre {{ white-space:pre-wrap; overflow-wrap:anywhere; }} .boundary {{ border-left:.35rem solid var(--warn); padding-left:1rem; }}
@media print {{ nav,.skip-link {{ display:none; }} body {{ background:white; color:black; }} section,.hero {{ break-inside:avoid; border-color:#555; }} }}
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
<p>Sable Rook · evidence-and-reproducibility steward · relational working identity only</p>
<h1>V641-v7 chain falsification audit</h1>
<nav aria-label="Report sections"><ul>
<li><a href="#status">Status</a></li><li><a href="#proposals">Proposals</a></li><li><a href="#board">Stage 20</a></li><li><a href="#gates">Gates</a></li><li><a href="#narrative">Overview</a></li><li><a href="#sources">Sources</a></li><li><a href="#negatives">Negatives</a></li>
</ul></nav>
</header>
<main id="main">
<section id="status" class="hero verdict" aria-labelledby="status-heading">
<h2 id="status-heading">Terminal status: {esc(truth['terminal_verdict'])}</h2>
<p>Ten proposals were executed as far as evidence permits. A pass is scoped; a representation is not a real experiment; an open gap is not completion; an exact gate requires the named authority.</p>
<div class="cards">
<div class="card"><strong>{esc(counts.get('completed',0))}</strong>completed</div>
<div class="card"><strong>{esc(counts.get('represented',0))}</strong>represented</div>
<div class="card"><strong>{esc(counts.get('open_gap',0))}</strong>open gaps</div>
<div class="card"><strong>{esc(counts.get('exact_gate',0))}</strong>exact gates</div>
</div>
<p class="boundary"><strong>Non-claim:</strong> no empirical GMUT confirmation, THOS superiority, AGI/ASI, consciousness or personhood, production Freed ID, enacted or ratified CBR, Māori authority, deployment, exhaustive security, complete accessibility conformance, Theory of Everything, or independent-team reproduction is established.</p>
</section>
<section id="proposals"><h2>Proposal outcomes</h2><div class="table-wrap"><table><caption>All ten preregistered v7 proposals</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th></tr></thead><tbody>{proposal_rows}</tbody></table></div></section>
<section id="board"><h2>Stage 20 pass/fail/defer board</h2><p>Every claim has one decision, a falsifier, and an expiry or reopening condition. Defer is never counted as pass.</p><div class="table-wrap"><table><caption>Terminal evidence decisions</caption><thead><tr><th scope="col">ID</th><th scope="col">Claim</th><th scope="col">Decision</th><th scope="col">Falsifier</th><th scope="col">Expiry or reopen</th></tr></thead><tbody>{board_rows}</tbody></table></div></section>
<section id="gates"><h2>Exact and open gates</h2><div class="table-wrap"><table><caption>Gates that remain visible</caption><thead><tr><th scope="col">Gate</th><th scope="col">State</th></tr></thead><tbody>{gate_rows}</tbody></table></div><h3>Complete</h3><ul>{complete_items}</ul><h3>Incomplete or exactly gated</h3><ul>{incomplete_items}</ul></section>
<section id="narrative"><h2>Integrated overview</h2>{overview_html}</section>
<section id="sources"><h2>Primary and official sources</h2><p>Draft and watch records do not replace stable standards. Repeated authority roots remain shared dependencies.</p><div class="table-wrap"><table><caption>{esc(sources['source_count'])} source records checked 13 July 2026</caption><thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">Authority</th><th scope="col">Status</th><th scope="col">Evidence role</th></tr></thead><tbody>{source_rows}</tbody></table></div></section>
<section id="negatives"><h2>Retained negative register</h2><p>Negative results are evidence. They are preserved even when a local recovery succeeds.</p><details><summary>Show {esc(negatives['negative_count'])} retained negatives</summary><div class="table-wrap"><table><caption>Inherited and v7 negative results</caption><thead><tr><th scope="col">ID</th><th scope="col">Origin</th><th scope="col">Observed</th><th scope="col">State</th></tr></thead><tbody>{negative_rows}</tbody></table></div></details></section>
<section aria-labelledby="access-heading"><h2 id="access-heading">Accessibility and use boundary</h2><p>This static report provides semantic landmarks, a skip link, heading order, table captions and headers, visible keyboard focus, responsive overflow, print styles, and plain-language boundary statements. These structural checks are useful but are <strong>not a complete WCAG conformance assessment</strong>. User testing and a scoped expert audit remain open.</p></section>
</main>
<footer><p>Generated from repository evidence. Terminal verdict: {esc(truth['terminal_verdict'])}. No live identifiers, credentials, private routes, or task transcripts are included.</p></footer>
</body>
</html>
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    build(args.phase_dir.resolve(), args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

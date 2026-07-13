#!/usr/bin/env python3
"""Build a self-contained accessible static report for GHC boundary evidence."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: object) -> str:
    return html.escape(str(value))


def build(phase_dir: Path, output: Path) -> None:
    truth = load(phase_dir / "phase-truth.json")
    ledger = load(phase_dir / "x2-proposal-ledger.json")
    gates = load(phase_dir / "exact-open-gate-register.json")
    negatives = load(phase_dir / "retained-negative-register.json")
    board = load(phase_dir / "stage20/pass-fail-defer-board.json")
    source = load(phase_dir / "sources/source-ledger.json")

    proposal_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row['proposal_id'])}</th>"
        f"<td>{esc(row['title'])}</td>"
        f"<td><span class=\"pill {esc(row['observed_disposition'])}\">{esc(row['observed_disposition'])}</span></td>"
        f"<td>{esc('; '.join(row['evidence']))}</td>"
        "</tr>"
        for row in ledger["proposals"]
    )
    gate_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row['gate_id'])}</th>"
        f"<td>{esc(row['gate_class'])}</td>"
        f"<td>{esc(row['state'])}</td>"
        f"<td>{esc(row['requires'])}</td>"
        "</tr>"
        for row in gates["gates"]
    )
    board_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row['gate'])}</th>"
        f"<td><span class=\"pill {esc(row['decision'])}\">{esc(row['decision'])}</span></td>"
        f"<td>{esc(row['evidence'])}</td>"
        "</tr>"
        for row in board["board"]
    )
    protected = "\n".join(
        f"<li><code>{esc(name)}</code>: <strong>{esc(value).lower()}</strong></li>"
        for name, value in truth["protected_claims"].items()
    )
    latest_negatives = "\n".join(
        f"<li><strong>{esc(row['negative_id'])}</strong> — {esc(row['statement'])}</li>"
        for row in negatives["negatives"][-14:]
    )
    counts = truth["disposition_counts"]
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nima Calder v642-v1 evidence boundary report</title>
  <style>
    :root {{ color-scheme: light dark; --ink:#15202b; --paper:#f7fafc; --panel:#fff; --line:#617284; --accent:#164e63; --focus:#d97706; }}
    @media (prefers-color-scheme: dark) {{ :root {{ --ink:#e5edf4; --paper:#101820; --panel:#17232e; --line:#91a4b7; --accent:#67e8f9; --focus:#fbbf24; }} }}
    * {{ box-sizing:border-box; }} body {{ margin:0; font: 1rem/1.6 system-ui, sans-serif; color:var(--ink); background:var(--paper); }}
    .skip-link {{ position:absolute; left:-9999px; top:.5rem; background:var(--panel); color:var(--ink); padding:.75rem; border:3px solid var(--focus); }}
    .skip-link:focus {{ left:.5rem; z-index:10; }} header, main, footer {{ max-width:76rem; margin:auto; padding:1rem 1.25rem; }}
    nav ul {{ display:flex; flex-wrap:wrap; gap:.75rem; padding:0; list-style:none; }} a {{ color:var(--accent); }} a:focus {{ outline:3px solid var(--focus); outline-offset:3px; }}
    .truth {{ border-left:.5rem solid var(--focus); padding:1rem; background:var(--panel); }}
    .metrics {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(11rem,1fr)); gap:.75rem; }} .metric {{ padding:1rem; border:1px solid var(--line); background:var(--panel); }}
    .metric strong {{ display:block; font-size:1.75rem; }} table {{ width:100%; border-collapse:collapse; margin:1rem 0 2rem; background:var(--panel); }}
    caption {{ text-align:left; font-weight:700; padding:.5rem 0; }} th, td {{ border:1px solid var(--line); text-align:left; vertical-align:top; padding:.65rem; }} thead th {{ background:color-mix(in srgb, var(--panel) 80%, var(--accent)); }}
    .table-wrap {{ overflow-x:auto; }} .pill {{ border:1px solid currentColor; border-radius:999px; padding:.1rem .45rem; white-space:nowrap; }}
    .completed,.pass {{ color:#166534; }} .represented,.defer {{ color:#9a3412; }} .open_gap,.fail {{ color:#b91c1c; }} .exact_gate {{ color:#6b21a8; }}
    code {{ overflow-wrap:anywhere; }} @media print {{ nav,.skip-link {{ display:none; }} body {{ color:#000; background:#fff; }} .metric,.truth,table {{ background:#fff; }} }}
  </style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main evidence</a>
<header>
  <h1>Nima Calder v642-v1 evidence boundary report</h1>
  <p>Useful static view of the committed phase evidence. Identity language is relational working language, not evidence of consciousness or legal personhood.</p>
  <nav aria-label="Report sections"><ul>
    <li><a href="#truth">Phase truth</a></li><li><a href="#outcomes">Proposal outcomes</a></li><li><a href="#gates">Open and exact gates</a></li><li><a href="#stage20">Stage 20 board</a></li><li><a href="#negatives">Retained negatives</a></li><li><a href="#boundaries">Claim boundaries</a></li>
  </ul></nav>
</header>
<main id="main">
  <section id="truth" aria-labelledby="truth-heading"><h2 id="truth-heading">Phase truth</h2>
    <div class="truth"><p><strong>Terminal verdict: {esc(truth['terminal_verdict'])}</strong></p><p>All ten preregistered proposals were executed as far as the evidence permits. Completed, represented, open-gap, and exact-gate labels remain separate.</p></div>
    <div class="metrics" aria-label="Evidence counts">
      <div class="metric"><strong>{counts['completed']}</strong> completed</div><div class="metric"><strong>{counts['represented']}</strong> represented</div><div class="metric"><strong>{counts['open_gap']}</strong> open gap</div><div class="metric"><strong>{counts['exact_gate']}</strong> exact gate</div><div class="metric"><strong>{negatives['negative_count']}</strong> retained negatives</div><div class="metric"><strong>{source['source_count']}</strong> primary or official sources</div>
    </div>
  </section>
  <section id="outcomes" aria-labelledby="outcomes-heading"><h2 id="outcomes-heading">Proposal outcomes</h2><div class="table-wrap"><table>
    <caption>Ten x2 outcomes and their evidence paths</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Title</th><th scope="col">Disposition</th><th scope="col">Evidence</th></tr></thead><tbody>{proposal_rows}</tbody>
  </table></div></section>
  <section id="gates" aria-labelledby="gates-heading"><h2 id="gates-heading">Open gaps and exact gates</h2><p>Open gaps need new evidence. Exact gates require an authorized person, community, authority, or fresh approval; technical scoring cannot close them.</p><div class="table-wrap"><table>
    <caption>Protected gates left open or deferred</caption><thead><tr><th scope="col">Gate</th><th scope="col">Class</th><th scope="col">State</th><th scope="col">What is required</th></tr></thead><tbody>{gate_rows}</tbody>
  </table></div></section>
  <section id="stage20" aria-labelledby="stage20-heading"><h2 id="stage20-heading">Stage 20 pass / fail / defer board</h2><div class="table-wrap"><table>
    <caption>Terminal board decisions</caption><thead><tr><th scope="col">Gate</th><th scope="col">Decision</th><th scope="col">Evidence</th></tr></thead><tbody>{board_rows}</tbody>
  </table></div></section>
  <section id="negatives" aria-labelledby="negatives-heading"><h2 id="negatives-heading">New retained negatives</h2><p>All 32 inherited negatives remain, and v642-v1 adds 14. Recovery may narrow a claim or improve a test, but it may not erase the negative.</p><ol>{latest_negatives}</ol></section>
  <section id="boundaries" aria-labelledby="boundaries-heading"><h2 id="boundaries-heading">Protected claim boundaries</h2><ul>{protected}</ul>
    <p>Māori concepts, wording, data, and governance remain under Māori authority. The system does not speak for Māori or substitute for affected parties or competent legal authority.</p>
    <p>The canonical GMUT material is a typed scalar-tensor/EFT research scaffold, not empirical confirmation, a detected force, a unique prediction, or a Theory of Everything. THOS uses synthetic proxy arms only. Freed ID evidence is structural only. Security testing is bounded. Reproduction remains same-owner and not independent-team reproduction.</p>
    <p><strong>Accessibility boundary:</strong> this page includes semantic structure, a skip link, keyboard-visible focus, headings, navigation, captions, scoped table headers, responsive tables, and print styles. These are structural checks, not a complete WCAG conformance assessment.</p>
  </section>
</main>
<footer><p>Generated from repository evidence; no raw task IDs, private routes, transcripts, screenshots, credentials, or private app state are included.</p></footer>
</body>
</html>
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.phase_dir.resolve(), args.output.resolve())
    print(json.dumps({"output": args.output.resolve().as_posix(), "ok": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

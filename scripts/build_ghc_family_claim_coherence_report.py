#!/usr/bin/env python3
"""Build a static accessible HTML report for a GHC claim-coherence phase."""

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
    gates = load(phase / "exact-open-gate-register.json")
    negatives = load(phase / "retained-negative-register.json")
    sources = load(phase / "sources/source-ledger.json")
    a11y = load(phase / "accessibility/evidence-map.json")

    proposal_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row['proposal_id'])}</th>"
        f"<td>{esc(row['title'])}</td>"
        f"<td>{badge(row['observed_disposition'])}</td>"
        f"<td>{esc(', '.join(row['evidence']))}</td>"
        "</tr>"
        for row in x2["proposals"]
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
    new_negatives = negatives["negatives"][negatives["inherited_count"] :]
    negative_items = "\n".join(
        f"<li><strong>{esc(row['negative_id'])}</strong>: {esc(row.get('statement', row.get('observed', 'retained negative')))}</li>"
        for row in new_negatives
    )
    source_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row['source_id'])}</th>"
        f"<td>{badge(row['status_class'])}</td>"
        f"<td><a href=\"{esc(row['url'])}\">{esc(row['title'])}</a></td>"
        f"<td>{esc(row['evidence_role'])}</td>"
        "</tr>"
        for row in sources["added_sources"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ilyra Fen v642-v4 claim-coherence report</title>
  <style>
    :root {{ color-scheme: light dark; --bg:#f7f8fb; --fg:#172033; --card:#fff; --line:#526174; --accent:#164e63; --soft:#e7f2f5; --ok:#14532d; --warn:#854d0e; --gate:#7f1d1d; }}
    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; }}
    body {{ margin:0; font:1rem/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; background:var(--bg); color:var(--fg); }}
    a {{ color:#075985; text-underline-offset:.18em; }}
    a:focus-visible, button:focus-visible {{ outline:3px solid #f59e0b; outline-offset:3px; }}
    .skip {{ position:absolute; left:.5rem; top:-4rem; background:#111827; color:#fff; padding:.75rem 1rem; z-index:10; }}
    .skip:focus {{ top:.5rem; }}
    header, main, footer {{ max-width:76rem; margin:auto; padding:1.25rem; }}
    header {{ padding-top:2.5rem; }}
    nav ul {{ display:flex; flex-wrap:wrap; gap:.6rem 1rem; padding:0; list-style:none; }}
    .card {{ background:var(--card); border:1px solid var(--line); border-radius:.65rem; padding:1rem; margin:1rem 0; box-shadow:0 .1rem .3rem rgb(0 0 0 / .08); }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(15rem,1fr)); gap:1rem; }}
    table {{ width:100%; border-collapse:collapse; display:block; overflow-x:auto; }}
    th, td {{ border:1px solid var(--line); padding:.6rem; text-align:left; vertical-align:top; }}
    thead th {{ background:var(--soft); }}
    .badge {{ display:inline-block; border:1px solid currentColor; border-radius:999px; padding:.1rem .5rem; font-weight:700; white-space:nowrap; }}
    .completed, .current, .stable {{ color:var(--ok); }}
    .represented, .draft, .watch, .open-gap {{ color:var(--warn); }}
    .exact-gate {{ color:var(--gate); }}
    .boundary {{ border-left:.45rem solid var(--gate); padding-left:1rem; }}
    code {{ overflow-wrap:anywhere; }}
    @media (prefers-color-scheme:dark) {{ :root {{ --bg:#101827; --fg:#f1f5f9; --card:#172033; --line:#94a3b8; --accent:#67e8f9; --soft:#243149; --ok:#86efac; --warn:#fde68a; --gate:#fca5a5; }} a {{ color:#7dd3fc; }} }}
    @media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior:auto; }} *, *::before, *::after {{ animation-duration:.001ms!important; transition-duration:.001ms!important; }} }}
    @media print {{ nav, .skip {{ display:none; }} body {{ background:#fff; color:#000; font-size:10.5pt; }} .card {{ break-inside:avoid; box-shadow:none; }} a {{ color:#000; }} }}
  </style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header>
  <p>GHC Family bounded evidence report</p>
  <h1>Ilyra Fen v642-v4 claim coherence</h1>
  <p>Ilyra Fen is relational working language only. It is not evidence of consciousness, sentience, legal personhood, authority, or identity continuity.</p>
  <nav aria-label="Report sections"><ul>
    <li><a href="#summary">Summary</a></li><li><a href="#proposals">Proposals</a></li><li><a href="#gates">Gates</a></li><li><a href="#negatives">Negatives</a></li><li><a href="#sources">Sources</a></li><li><a href="#accessibility">Accessibility</a></li><li><a href="#route">Route</a></li>
  </ul></nav>
</header>
<main id="main">
  <section id="summary" aria-labelledby="summary-heading">
    <h2 id="summary-heading">Bounded summary</h2>
    <div class="grid">
      <div class="card"><h3>Truth distribution</h3><p>6 completed · 2 represented · 1 open gap · 1 exact gate</p></div>
      <div class="card"><h3>Negative retention</h3><p>{esc(negatives['negative_count'])} total · {esc(negatives['inherited_count'])} inherited · none erased</p></div>
      <div class="card"><h3>Terminal verdict</h3><p><strong>{esc(truth['terminal_verdict'])}</strong></p></div>
    </div>
    <p class="boundary">No empirical GMUT confirmation, detected force, unique prediction, Theory of Everything, real THOS superiority, AGI, ASI, consciousness, personhood, production Freed ID assurance, enacted law, cultural ratification, deployment, exhaustive security, complete accessibility conformance, proof or canon, or independent-team reproduction is established.</p>
  </section>
  <section id="proposals" aria-labelledby="proposals-heading">
    <h2 id="proposals-heading">Ten frozen proposals and observed labels</h2>
    <table><thead><tr><th scope="col">ID</th><th scope="col">Surface</th><th scope="col">Label</th><th scope="col">Evidence</th></tr></thead><tbody>{proposal_rows}</tbody></table>
  </section>
  <section id="gates" aria-labelledby="gates-heading">
    <h2 id="gates-heading">Open gaps and exact gates</h2>
    <p>Five open gaps and six exact gates remain open or deferred. Technical work does not score them away.</p>
    <table><thead><tr><th scope="col">Gate</th><th scope="col">Class</th><th scope="col">State</th><th scope="col">Required evidence or authority</th></tr></thead><tbody>{gate_rows}</tbody></table>
  </section>
  <section id="negatives" aria-labelledby="negatives-heading">
    <h2 id="negatives-heading">Phase-local retained negatives</h2>
    <p>These are preserved alongside all inherited negatives. Later passing checks do not erase them.</p><ul>{negative_items}</ul>
  </section>
  <section id="sources" aria-labelledby="sources-heading">
    <h2 id="sources-heading">Phase-local primary and official sources</h2>
    <p>The effective ledger contains 54 sources: 25 current, 24 stable, four draft, and one watch. Draft and watch sources remain visibly non-stable.</p>
    <table><thead><tr><th scope="col">ID</th><th scope="col">Status</th><th scope="col">Source</th><th scope="col">Role and limit</th></tr></thead><tbody>{source_rows}</tbody></table>
  </section>
  <section id="accessibility" aria-labelledby="accessibility-heading">
    <h2 id="accessibility-heading">Accessibility evidence and reservation</h2>
    <p>Automated structural checks cover {esc(', '.join(a11y['automated_structural']))}. Manual expert checks remain reserved for {esc(', '.join(a11y['manual_expert_reserved']))}. User-participation checks remain reserved for {esc(', '.join(a11y['user_participation_reserved']))}.</p>
    <p class="boundary">Automated structure is not complete accessibility conformance.</p>
  </section>
  <section id="route" aria-labelledby="route-heading">
    <h2 id="route-heading">Reproduction and terminal route</h2>
    <p>Clean detached snapshots can establish bounded same-owner repeatability only. No independent executor or returned independent result exists.</p>
    <p>The only terminal route is one sanitized activation to the existing original Sable Rook task for Sable-only v642-v5 after evidence, closeout, seal, exact-final-head, cleanliness, and remote-equality gates all pass. Until then the route is <strong>PLANNED_NOT_SENT</strong>.</p>
  </section>
</main>
<footer><p>Static report. No scripts, trackers, private routes, raw task identifiers, credentials, or local private paths are embedded.</p></footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    phase = args.phase_dir.resolve()
    output = args.output or phase / "deliverables/v642-v4-claim-coherence-report.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build(phase), encoding="utf-8", newline="\n")
    print(json.dumps({"status": "built", "output": output.name}, ensure_ascii=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build an accessible static report for the bounded v642-v3 packet."""

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
    return f'<span class="badge {esc(label.replace("_", "-"))}">{esc(label)}</span>'


def build(phase: Path) -> str:
    x2 = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    sources = load(phase / "sources/source-ledger.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    schedule = load(phase / "workflow/six-seat-round-robin.json")
    context = load(phase / "workflow/project-context-capability-register.json")
    terminal = load(phase / "stage20/terminal-verdict.json")
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
    gate_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row['gate_id'])}</th>"
        f"<td>{badge(row['gate_class'])}</td>"
        f"<td>{esc(row['state'])}</td>"
        f"<td>{esc(row['requires'])}</td>"
        "</tr>"
        for row in gates["gates"]
    )
    source_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{esc(row['source_id'])}</th>"
        f"<td>{esc(row['title'])}</td>"
        f"<td>{badge(row['status_class'])}</td>"
        f"<td><a href=\"{esc(row['url'])}\">primary or official source</a></td>"
        "</tr>"
        for row in sources["added_sources"]
    )
    protected = "\n".join(
        f"<li>{esc(name.replace('_', ' '))}: not established</li>"
        for name, value in truth["protected_claims"].items()
        if not value
    )
    counts = truth["disposition_counts"]
    future = ", ".join(row["seat"] for row in context["future_not_existing"])

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Eiren Kestrel v642-v3 project-aware evidence report</title>
  <style>
    :root {{ color-scheme:light dark; --ink:#172033; --paper:#f8fafc; --line:#94a3b8; --accent:#075985; --good:#166534; --warn:#92400e; --gate:#7f1d1d; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font:1rem/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; color:var(--ink); background:var(--paper); }}
    a {{ color:#075985; }} a:focus {{ outline:3px solid #f59e0b; outline-offset:2px; }}
    .skip-link {{ position:absolute; left:-9999px; top:0; background:#fff; color:#000; padding:.75rem; z-index:20; }}
    .skip-link:focus {{ left:.75rem; top:.75rem; }}
    header {{ background:#0f172a; color:#fff; padding:2.4rem max(1rem,calc((100% - 76rem)/2)); }}
    header p {{ max-width:72ch; }}
    nav {{ background:#e2e8f0; padding:.75rem max(1rem,calc((100% - 76rem)/2)); }}
    nav ul {{ display:flex; flex-wrap:wrap; gap:.5rem 1rem; margin:0; padding:0; list-style:none; }}
    main,footer {{ max-width:76rem; margin:auto; padding:1rem; }}
    section {{ margin:2rem 0; scroll-margin-top:1rem; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(10rem,1fr)); gap:.8rem; }}
    .card {{ border:1px solid var(--line); border-radius:.5rem; padding:1rem; background:#fff; }}
    .card strong {{ display:block; font-size:1.55rem; }}
    .callout {{ border-left:.45rem solid var(--gate); background:#fee2e2; color:#450a0a; padding:1rem; }}
    .bounded {{ border-left-color:var(--accent); background:#e0f2fe; color:#082f49; }}
    .table-wrap {{ overflow-x:auto; }}
    table {{ width:100%; border-collapse:collapse; background:#fff; }}
    caption {{ text-align:left; font-weight:700; padding:.6rem 0; }}
    th,td {{ border:1px solid var(--line); padding:.55rem; text-align:left; vertical-align:top; }}
    thead th {{ background:#e2e8f0; }}
    .badge {{ display:inline-block; border:1px solid currentColor; border-radius:999px; padding:.05rem .45rem; white-space:nowrap; }}
    .completed,.current,.stable {{ color:var(--good); }}
    .represented,.draft,.watch,.open-gap {{ color:var(--warn); }}
    .exact-gate {{ color:var(--gate); }}
    code {{ overflow-wrap:anywhere; }}
    @media (prefers-color-scheme:dark) {{
      :root {{ --ink:#e2e8f0; --paper:#0f172a; --line:#64748b; }}
      .card,table {{ background:#111827; }} thead th,nav {{ background:#1e293b; }}
      nav a {{ color:#bae6fd; }} .bounded {{ color:#e0f2fe; background:#164e63; }}
      .callout {{ color:#fee2e2; background:#450a0a; }}
    }}
  </style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p>GHC family · Eiren Kestrel · v642-v3</p>
  <h1>Project-aware routing, bounded evidence, and visible gates</h1>
  <p>This is a repository-local technical report. It does not convert schemas,
  simulations, route receipts, or repeated local runs into empirical science,
  cryptographic assurance, legal or cultural authority, consciousness,
  personhood, deployment, or independent reproduction.</p>
</header>
<nav aria-label="Report sections"><ul>
  <li><a href="#truth">Truth</a></li><li><a href="#route">Route</a></li>
  <li><a href="#proposals">Proposals</a></li><li><a href="#boundaries">Boundaries</a></li>
  <li><a href="#gates">Gates</a></li><li><a href="#sources">Sources</a></li>
  <li><a href="#accessibility">Accessibility</a></li>
</ul></nav>
<main id="main">
<section id="truth" aria-labelledby="truth-heading">
  <h2 id="truth-heading">Phase truth</h2>
  <div class="callout"><strong>{esc(terminal['verdict'])}</strong><br>
  Stage 20 and deployment are not authorized by this artifact.</div>
  <div class="cards">
    <div class="card"><strong>{counts['completed']}</strong>completed</div>
    <div class="card"><strong>{counts['represented']}</strong>represented</div>
    <div class="card"><strong>{counts['open_gap']}</strong>open gap</div>
    <div class="card"><strong>{counts['exact_gate']}</strong>exact gate</div>
    <div class="card"><strong>{negatives['negative_count']}</strong>retained negatives</div>
    <div class="card"><strong>{gates['open_gap_count']} + {gates['exact_gate_count']}</strong>open + exact gates</div>
  </div>
</section>
<section id="route" aria-labelledby="route-heading">
  <h2 id="route-heading">Finite six-seat route</h2>
  <p>The scheduler contains {schedule['assignment_count']} assignments from
  {esc(schedule['start'])} through {esc(schedule['terminal'])}. Phase values are
  restricted to 1 through 8; no v9 is permitted. Future seats {esc(future)} do
  not yet exist. Elian Voss and Nima Calder remain standby. The already existing
  #5 task is planned but not sent until terminal validation succeeds.</p>
  <div class="callout bounded"><strong>Route boundary:</strong> an accepted baton
  is operational evidence only. It is not scientific evidence, authority,
  identity proof, or independent reproduction.</div>
</section>
<section id="proposals" aria-labelledby="proposal-heading">
  <h2 id="proposal-heading">Ten frozen proposals</h2>
  <div class="table-wrap"><table>
    <caption>Observed dispositions and repository-relative evidence</caption>
    <thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Evidence</th></tr></thead>
    <tbody>{proposal_rows}</tbody>
  </table></div>
</section>
<section id="boundaries" aria-labelledby="boundary-heading">
  <h2 id="boundary-heading">Claims not established</h2>
  <p><strong>Strongest reproduction statement:</strong>
  {esc(independent['strongest_allowed_claim'])}. Independent-team scientific
  reproduction remains open.</p>
  <ul>{protected}</ul>
  <p><strong>GMUT:</strong> Bianchi and exchange-current checks are structural
  obligations in a typed scalar-tensor/EFT research scaffold. No real
  measurement, likelihood, force, unique prediction, empirical confirmation, or
  Theory of Everything result exists.</p>
  <p><strong>THOS:</strong> cluster, multiplicity, and sequential-decision
  controls are protocol-only. Zero blind matched-budget real arms ran.</p>
  <p><strong>Freed ID:</strong> rotation and revocation-race fixtures are
  synthetic. There are no real keys, proofs, live services, interoperability
  partners, independent security reviews, privacy assurance, or trust
  governance.</p>
  <p><strong>CBR:</strong> affected-party legitimacy, Māori authority, cultural
  ratification, competent legal authority, and enacted-law status remain
  exact-gated to authorized participants and authorities.</p>
  <p><strong>Thermo-psyche:</strong> thermodynamic entropy, Shannon entropy,
  computational erasure, psychological uncertainty, and metaphor remain
  distinct. No fundamental law, consciousness, or personhood result exists.</p>
</section>
<section id="gates" aria-labelledby="gate-heading">
  <h2 id="gate-heading">Open and exact gates</h2>
  <div class="table-wrap"><table>
    <caption>Requirements that local technical work cannot silently close</caption>
    <thead><tr><th scope="col">Gate</th><th scope="col">Class</th><th scope="col">State</th><th scope="col">Requires</th></tr></thead>
    <tbody>{gate_rows}</tbody>
  </table></div>
</section>
<section id="sources" aria-labelledby="source-heading">
  <h2 id="source-heading">New primary and official sources</h2>
  <p>The effective ledger has {sources['effective_source_count']} pins:
  {sources['effective_status_counts']['current']} current,
  {sources['effective_status_counts']['stable']} stable,
  {sources['effective_status_counts']['draft']} draft, and
  {sources['effective_status_counts']['watch']} watch. The table shows the eight
  v642-v3 additions; 38 pins are inherited by exact revision.</p>
  <div class="table-wrap"><table>
    <caption>v642-v3 source additions and lifecycle status</caption>
    <thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">Status</th><th scope="col">Link</th></tr></thead>
    <tbody>{source_rows}</tbody>
  </table></div>
</section>
<section id="accessibility" aria-labelledby="access-heading">
  <h2 id="access-heading">Accessibility boundary</h2>
  <p>The report uses language metadata, a skip link, landmarks, headings,
  navigation, captions, scoped table headers, visible focus, flexible layout,
  and text labels. These are structural checks only and are
  <strong>not a complete WCAG conformance assessment</strong>. No independent
  assistive-technology review is claimed.</p>
</section>
</main>
<footer><p>Sanitized repository artifact. No raw task identifiers, private
routes, credentials, transcripts, screenshots, session streams, or private
local paths are included.</p></footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    phase = args.phase_dir.resolve()
    output = args.output or (phase / "deliverables/v642-v3-project-round-robin-report.html")
    if not output.is_absolute():
        output = phase / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build(phase), encoding="utf-8", newline="\n")
    print(json.dumps({"status": "built", "output": "deliverables/v642-v3-project-round-robin-report.html"}))


if __name__ == "__main__":
    main()

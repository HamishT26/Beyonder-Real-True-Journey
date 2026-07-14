#!/usr/bin/env python3
"""Build the accessible static v643-v1 rights-resilience report."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build(repo: Path) -> Path:
    phase = repo / "docs/eiren-kestrel/v643-v1"
    x1 = read(phase / "x1-proposals.json")
    x2 = read(phase / "x2-proposal-ledger.json")
    gates = read(phase / "exact-open-gate-register.json")
    truth = read(phase / "phase-truth.json")
    rows = []
    for proposal in x2["proposals"]:
        rows.append(
            "<tr>"
            f"<th scope='row'>{html.escape(proposal['proposal_id'])}</th>"
            f"<td>{html.escape(proposal['title'])}</td>"
            f"<td><span class='tag {html.escape(proposal['observed_disposition'])}'>{html.escape(proposal['observed_disposition'])}</span></td>"
            f"<td>{proposal['accepted']}</td><td>{proposal['rejected']}</td>"
            "</tr>"
        )
    open_items = "".join(f"<li><strong>{html.escape(item['surface'])}:</strong> {html.escape('; '.join(item['needs']))}</li>" for item in gates["open_gaps"])
    exact_items = "".join(f"<li><strong>{html.escape(item['surface'])}:</strong> reserved to {html.escape('; '.join(item['reserved_to']))}</li>" for item in gates["exact_gates"])
    boundary = html.escape(truth["boundary"])
    document = f"""<!doctype html>
<html lang="en-NZ">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Eiren Kestrel v643-v1 rights-resilience evidence report</title>
  <style>
    :root {{ color-scheme: light dark; --bg:#f7f8fb; --fg:#172033; --panel:#fff; --accent:#3157a4; --border:#687386; }}
    @media (prefers-color-scheme:dark) {{ :root {{ --bg:#10141d; --fg:#edf1f8; --panel:#1a2130; --accent:#9bbaff; --border:#a4afc0; }} }}
    * {{ box-sizing:border-box; }} body {{ margin:0; font:1rem/1.55 system-ui,sans-serif; background:var(--bg); color:var(--fg); }}
    a {{ color:var(--accent); }} .skip {{ position:absolute; left:-9999px; }} .skip:focus {{ left:1rem; top:1rem; background:var(--panel); padding:.75rem; z-index:2; }}
    header, main, footer {{ max-width:76rem; margin:auto; padding:1.25rem; }} section {{ background:var(--panel); border:1px solid var(--border); border-radius:.5rem; padding:1rem; margin:1rem 0; }}
    table {{ width:100%; border-collapse:collapse; }} th,td {{ border:1px solid var(--border); padding:.55rem; text-align:left; vertical-align:top; }}
    .table-wrap {{ overflow-x:auto; }} .tag {{ display:inline-block; border:1px solid currentColor; border-radius:999px; padding:.05rem .45rem; }}
    .completed {{ color:#176b3a; }} .represented {{ color:#665000; }} .open_gap,.exact_gate {{ color:#9b2d2d; }}
    :focus-visible {{ outline:3px solid var(--accent); outline-offset:2px; }}
  </style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header><h1>Eiren Kestrel v643-v1 rights-resilience evidence report</h1><p>Relational working identity only; not evidence of consciousness, sentience, personhood, identity continuity, or independent authority.</p></header>
<main id="main">
  <section aria-labelledby="verdict"><h2 id="verdict">Evidence-bounded verdict</h2><p><strong>{html.escape(truth['terminal_verdict'])}</strong></p><p>Primary focus: {html.escape(truth['primary_focus'])}. All three pillars remain represented. Exactly ten proposals produced 80 deterministic cases and 70 retained rejecting mutations.</p></section>
  <section aria-labelledby="proposals"><h2 id="proposals">Proposal results</h2><div class="table-wrap"><table><caption>Observed local dispositions and fixture counts</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Accepted</th><th scope="col">Rejected</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
  <section aria-labelledby="open"><h2 id="open">Five open evidence gaps</h2><ul>{open_items}</ul></section>
  <section aria-labelledby="exact"><h2 id="exact">Six exact authority gates</h2><ul>{exact_items}</ul></section>
  <section aria-labelledby="access"><h2 id="access">Accessibility boundary</h2><p>This static report uses semantic headings, a skip link, table headers and caption, visible keyboard focus, high-contrast system colors, responsive overflow, and no script dependency. Automated structural checks are local evidence only. Manual accessibility evaluation and affected-user evaluation remain open.</p></section>
  <section aria-labelledby="boundary"><h2 id="boundary">Claim boundary</h2><p>{boundary}</p></section>
</main>
<footer><p>Owner-scoped static artifact. No private route, raw task identifier, credential, transcript, screenshot, session stream, or local private path is included.</p></footer>
</body>
</html>
"""
    output = phase / "deliverables/v643-v1-rights-resilience-report.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8", newline="\n")
    receipt = {
        "schema": "ghc.family.v643-v1.static-report-receipt.v1",
        "phase": x1["phase"],
        "owner": x1["owner"],
        "artifact": "deliverables/v643-v1-rights-resilience-report.html",
        "static": True,
        "script_dependency": False,
        "structural_features": ["lang", "title", "viewport", "skip-link", "semantic-headings", "table-caption", "column-and-row-headers", "visible-focus", "responsive-overflow"],
        "manual_accessibility_evaluation": False,
        "affected_user_evaluation": False,
        "complete_accessibility_conformance": False,
        "boundary": "Automated structural checks do not replace manual or affected-user accessibility evaluation.",
    }
    (phase / "accessibility").mkdir(parents=True, exist_ok=True)
    (phase / "accessibility/static-report-receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(build(args.repo.resolve()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

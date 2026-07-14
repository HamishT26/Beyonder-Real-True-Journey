#!/usr/bin/env python3
"""Build the accessible static Orin Thale v644-v2 boundary report."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "orin-thale" / "v644-v2"


def build_report(output: Path) -> None:
    ledger = json.loads((PHASE_ROOT / "x2-proposal-ledger.json").read_text(encoding="utf-8"))
    gates = json.loads((PHASE_ROOT / "exact-open-gate-register.json").read_text(encoding="utf-8"))
    rows = []
    for entry in ledger["proposals"]:
        rows.append(
            "<tr>"
            f"<th scope=\"row\">{html.escape(entry['proposal_id'])}</th>"
            f"<td>{html.escape(entry['title'])}</td>"
            f"<td><span class=\"tag {html.escape(entry['outcome'])}\">{html.escape(entry['outcome'])}</span></td>"
            f"<td>{html.escape(entry['evidence_summary'])}</td>"
            "</tr>"
        )
    open_items = "".join(
        f"<li><strong>{html.escape(item['gate_id'])}: {html.escape(item['domain'])}</strong> — {html.escape(', '.join(item['requires']))}</li>"
        for item in gates["open_gaps"]
    )
    exact_items = "".join(
        f"<li><strong>{html.escape(item['gate_id'])}: {html.escape(item['domain'])}</strong> — exact authorized participation remains required.</li>"
        for item in gates["exact_gates"]
    )
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Orin Thale v644-v2 boundary evidence report</title>
  <style>
    :root {{ color-scheme: light; --ink:#17202a; --muted:#45525f; --paper:#fff; --panel:#eef4f8; --line:#506273; --link:#004f9e; --focus:#ffbf47; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--paper); color:var(--ink); font:1rem/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
    a {{ color:var(--link); text-decoration-thickness:.12em; text-underline-offset:.18em; }}
    a:focus-visible {{ outline:.2rem solid var(--focus); outline-offset:.18rem; }}
    .skip {{ position:absolute; left:.5rem; top:-5rem; padding:.75rem 1rem; background:#000; color:#fff; z-index:10; }}
    .skip:focus {{ top:.5rem; }}
    header, main, footer {{ width:min(76rem, calc(100% - 2rem)); margin-inline:auto; }}
    header {{ padding:2rem 0 1rem; }}
    .boundary {{ border:.16rem solid #7a2f00; border-left-width:.65rem; padding:1rem; background:#fff4e8; }}
    .summary {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(11rem,1fr)); gap:.8rem; margin:1.25rem 0; }}
    .summary div {{ padding:.85rem; background:var(--panel); border:1px solid var(--line); }}
    .summary strong {{ display:block; font-size:1.35rem; }}
    table {{ border-collapse:collapse; width:100%; margin-block:1rem 2rem; }}
    caption {{ text-align:left; font-weight:700; padding:.5rem 0; }}
    th, td {{ border:1px solid var(--line); padding:.65rem; text-align:left; vertical-align:top; }}
    thead th {{ background:#dfeaf2; }}
    .tag {{ font-weight:700; }}
    .completed {{ color:#155724; }} .represented {{ color:#5b3b00; }} .open_gap, .exact_gate {{ color:#7a2f00; }}
    code {{ overflow-wrap:anywhere; }}
    footer {{ border-top:1px solid var(--line); padding:1rem 0 2rem; color:var(--muted); }}
    @media (max-width:48rem) {{ table, thead, tbody, tr, th, td {{ display:block; }} thead {{ position:absolute; clip:rect(0 0 0 0); }} tr {{ margin-bottom:1rem; border:1px solid var(--line); }} th,td {{ border:0; border-bottom:1px solid #aab5bf; }} }}
    @media (prefers-reduced-motion:reduce) {{ *,*::before,*::after {{ scroll-behavior:auto !important; transition:none !important; animation:none !important; }} }}
  </style>
</head>
<body>
<a class="skip" href="#main">Skip to the evidence summary</a>
<header>
  <p>Orin Thale · v644-v2 · relational working language only</p>
  <h1>Boundary evidence report</h1>
  <div class="boundary" role="note">
    <strong>Terminal verdict: NOT_READY_FOR_STAGE_20.</strong>
    GMUT remains a typed scalar-tensor/EFT research-model family; THOS remains proxy; Freed ID is not production-complete; CBR, Māori authority, legal and cultural decisions, deployment, complete accessibility, exhaustive security, independent reproduction, consciousness/personhood, AGI/ASI, proof/canon, and Stage 20 remain unclaimed and gated.
  </div>
</header>
<main id="main">
  <section aria-labelledby="summary-heading">
    <h2 id="summary-heading">Phase summary</h2>
    <div class="summary">
      <div><strong>10</strong>preregistered proposals</div>
      <div><strong>6</strong>completed in bounded scope</div>
      <div><strong>2</strong>represented or proxy</div>
      <div><strong>1 + 1</strong>open gap and exact gate</div>
      <div><strong>5 + 6</strong>remaining open and exact gates</div>
    </div>
    <p>The primary focus is GMUT Mind. Formal hypersurface checks are not physical confirmation, and the binary-pulsar study remains zero-row and unexecuted. Every rejected mutation remains in the negative register.</p>
  </section>
  <section aria-labelledby="outcomes-heading">
    <h2 id="outcomes-heading">Proposal outcomes</h2>
    <div role="region" aria-label="Proposal outcome table" tabindex="0">
      <table>
        <caption>Bounded v644-v2 outcome ledger</caption>
        <thead><tr><th scope="col">Proposal</th><th scope="col">Mechanism</th><th scope="col">Outcome</th><th scope="col">Evidence boundary</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
  </section>
  <section aria-labelledby="gates-heading">
    <h2 id="gates-heading">Open evidence gaps</h2>
    <ul>{open_items}</ul>
    <h2>Exact authority gates</h2>
    <ul>{exact_items}</ul>
  </section>
  <section aria-labelledby="links-heading">
    <h2 id="links-heading">Audit paths</h2>
    <ul>
      <li><a href="../x1-preregistration.md">Read the frozen x1 proposal preregistration</a>.</li>
      <li><a href="../sources/source-ledger.md">Review the phase source ledger and currency labels</a>.</li>
      <li><a href="../v644-v2-integrated-overview.md">Read the integrated ownership, science, governance, and recovery overview</a>.</li>
    </ul>
  </section>
  <section aria-labelledby="access-heading">
    <h2 id="access-heading">Accessibility reservation</h2>
    <p>This static report provides semantic headings, a skip link, descriptive links, a captioned table with headers, responsive presentation, visible focus, and no active content. Those checks do not establish complete accessibility. Qualified manual review, assistive-technology coverage, cognitive-accessibility review, and evaluation with affected users remain reserved.</p>
  </section>
</main>
<footer><p>Repository engineering evidence only. No private route, task identifier, credential, transcript, screenshot, session stream, or local path is published here.</p></footer>
</body>
</html>
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PHASE_ROOT / "deliverables" / "v644-v2-boundary-evidence-report.html")
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else ROOT / args.output
    build_report(output)
    print(json.dumps({"output": output.relative_to(ROOT).as_posix(), "active_content": False, "manual_evaluation_reserved": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

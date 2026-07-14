#!/usr/bin/env python3
"""Build the accessible static v643-v3 THOS-integrity report."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build(repo: Path) -> Path:
    phase = repo / "docs/sable-rook/v643-v3"
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
    document = f"""<!doctype html>
<html lang="en-NZ">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sable Rook v643-v3 THOS-integrity evidence report</title>
  <style>
    :root {{ color-scheme:light dark; --bg:#f4f7f6; --fg:#17251f; --panel:#fff; --accent:#285f50; --border:#64766e; }}
    @media (prefers-color-scheme:dark) {{ :root {{ --bg:#101714; --fg:#edf5f1; --panel:#18231e; --accent:#9ad7c5; --border:#a4b8ae; }} }}
    @media (forced-colors:active) {{ .tag {{ border:2px solid ButtonText; }} a {{ forced-color-adjust:auto; }} }}
    @media print {{ body {{ background:#fff; color:#000; }} section {{ break-inside:avoid; border:1px solid #000; }} .table-wrap {{ overflow:visible; }} }}
    * {{ box-sizing:border-box; }} body {{ margin:0; font:1rem/1.55 system-ui,sans-serif; background:var(--bg); color:var(--fg); overflow-wrap:anywhere; }}
    a {{ color:var(--accent); }} .skip {{ position:absolute; left:-9999px; }} .skip:focus {{ left:1rem; top:1rem; background:var(--panel); padding:.75rem; z-index:2; }}
    header,main,footer {{ max-width:76rem; margin:auto; padding:1.25rem; }} section {{ background:var(--panel); border:1px solid var(--border); border-radius:.5rem; padding:1rem; margin:1rem 0; }}
    table {{ width:100%; border-collapse:collapse; }} th,td {{ border:1px solid var(--border); padding:.55rem; text-align:left; vertical-align:top; }}
    .table-wrap {{ overflow-x:auto; }} .tag {{ display:inline-block; border:1px solid currentColor; border-radius:999px; padding:.05rem .45rem; }}
    .completed {{ color:#176b3a; }} .represented {{ color:#665000; }} .open_gap,.exact_gate {{ color:#9b2d2d; }} :focus-visible {{ outline:3px solid var(--accent); outline-offset:2px; }}
    @media (max-width:20rem) {{ header,main,footer {{ padding:.6rem; }} th,td {{ padding:.3rem; }} }}
  </style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header><h1>Sable Rook v643-v3 THOS-integrity evidence report</h1><p>Relational working identity only; not evidence of consciousness, sentience, personhood, identity continuity, or independent authority.</p></header>
<main id="main">
  <section aria-labelledby="verdict"><h2 id="verdict">Evidence-bounded verdict</h2><p><strong>{html.escape(truth['terminal_verdict'])}</strong></p><p>Primary focus: {html.escape(truth['primary_focus'])}. GMUT Mind, THOS Body, and Freed ID/CBR Heart remain represented. Exactly ten proposals produced 80 deterministic cases and 70 retained rejecting mutations.</p></section>
  <section aria-labelledby="proposals"><h2 id="proposals">Proposal results</h2><div class="table-wrap"><table><caption>Observed local dispositions and fixture counts</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Accepted</th><th scope="col">Rejected</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
  <section aria-labelledby="thos"><h2 id="thos">THOS Body boundary</h2><p>Component fidelity and burden protocols are useful preregistration evidence only. There are zero participants and zero executed real arms. Ethics review, consent, validated measures, preregistered blind matched-budget real arms, real burden and fatigue observations, and independent review remain open. No effectiveness, safety, superiority, AGI, ASI, consciousness, or personhood claim is established.</p></section>
  <section aria-labelledby="open"><h2 id="open">Five open evidence gaps</h2><ul>{open_items}</ul></section>
  <section aria-labelledby="exact"><h2 id="exact">Six exact authority gates</h2><ul>{exact_items}</ul></section>
  <section aria-labelledby="access"><h2 id="access">Accessibility boundary</h2><p>This static report supports narrow reflow, 400 percent browser zoom, forced-colors preservation, print preservation, semantic headings, a skip link, table headers and caption, visible focus, responsive overflow, and no script dependency. Automated structural checks remain local evidence. Qualified manual accessibility evaluation and affected-user evaluation are reserved and incomplete.</p></section>
  <section aria-labelledby="science"><h2 id="science">Scientific and institutional boundary</h2><p>GMUT remains a typed scalar-tensor/EFT research-model family. THOS remains proxy without preregistered blind matched-budget real arms and independent review. Freed ID production needs standards-conformant real keys and proofs, live resolution and status, interoperability, privacy and security review, and trust governance. CBR legitimacy and Māori, legal, cultural, and affected-party authority remain exact-gated.</p></section>
  <section aria-labelledby="boundary"><h2 id="boundary">Claim boundary</h2><p>{html.escape(truth['boundary'])}</p></section>
</main>
<footer><p>Owner-scoped static artifact. No private route, raw task identifier, credential, transcript, screenshot, session stream, private callable identifier, private app state, or private local path is included.</p></footer>
</body>
</html>
"""
    output = phase / "deliverables/v643-v3-thos-integrity-report.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8", newline="\n")
    receipt = {
        "schema": "ghc.family.v643-v3.static-report-receipt.v1",
        "phase": x1["phase"], "owner": x1["owner"],
        "artifact": "deliverables/v643-v3-thos-integrity-report.html",
        "static": True, "script_dependency": False,
        "structural_features": ["lang", "title", "viewport", "skip-link", "semantic-headings", "table-caption", "column-and-row-headers", "visible-focus", "narrow-reflow", "forced-colors", "print-preservation", "responsive-overflow"],
        "manual_accessibility_evaluation": False, "affected_user_evaluation": False,
        "complete_accessibility_conformance": False,
        "boundary": "Automated structural checks do not replace qualified manual or affected-user accessibility evaluation.",
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

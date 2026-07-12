from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def list_items(values: list[Any]) -> str:
    return "".join(f"<li>{esc(value)}</li>" for value in values)


def build_report(phase: Path) -> str:
    truth = load(phase / "phase-truth.json")
    ledger = load(phase / "x2-proposal-ledger.json")
    board = load(phase / "stage20/terminal-evidence-board.json")
    covenant = load(phase / "physics/equation-register-covenant.json")
    candidates = load(phase / "thermo-psyche/candidate-register.json")
    negatives = load(phase / "falsification/inherited-negative-register.json")
    freed = load(phase / "freed-id/assurance-lattice.json")
    cbr = load(phase / "cbr/authority-matrix.json")
    reproduction = load(phase / "reproduction/reproduction-report.json")
    source = load(phase / "sources/source-ledger.json")
    overview = (phase / "v641-v6-integrated-overview.md").read_text(encoding="utf-8")

    counts = truth["disposition_counts"]
    rows = "".join(
        "<tr>"
        f"<td>{esc(row['proposal_id'])}</td>"
        f"<td>{esc(row['title'])}</td>"
        f"<td><span class='status {esc(row['disposition'])}'>{esc(row['disposition'])}</span></td>"
        f"<td>{esc(', '.join(row['evidence']))}</td>"
        "</tr>"
        for row in ledger["rows"]
    )
    claim_cards = "".join(
        "<article class='card'>"
        f"<h3>{esc(card['claim_id'])}: {esc(card['claim'])}</h3>"
        f"<p><strong>Disposition:</strong> <span class='status {esc(card['disposition'])}'>{esc(card['disposition'])}</span></p>"
        f"<p><strong>Promotion:</strong> {esc(card['promotion_requires'])}</p>"
        f"<p><strong>Review:</strong> {esc(card['review_on'])}</p>"
        "</article>"
        for card in board["cards"]
    )
    candidate_rows = "".join(
        "<tr>"
        f"<td>{esc(row['candidate_id'])}</td><td>{esc(row['name'])}</td>"
        f"<td>{esc(row['classification'])}</td><td>No</td><td>{esc(row['reason'])}</td>"
        "</tr>"
        for row in candidates["candidates"]
    )
    protected = [name.replace("_", " ") for name, value in board["protected_claims"].items() if value is False]
    overview_word_count = len(re.findall(r"\b\w+[\w'-]*\b", overview))

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Eiren Kestrel v641-v6 terminal evidence report</title>
  <style>
    :root {{ color-scheme: light; --ink:#172033; --muted:#526076; --paper:#fff; --panel:#f5f7fb; --line:#c8d1df; --blue:#164e8a; --green:#12623d; --amber:#765600; --red:#8b2635; }}
    * {{ box-sizing:border-box; }} body {{ margin:0; font:16px/1.55 system-ui,-apple-system,Segoe UI,sans-serif; color:var(--ink); background:var(--paper); }}
    header,main,footer {{ max-width:1180px; margin:auto; padding:1.25rem; }} header {{ background:linear-gradient(135deg,#eaf3ff,#f8fbff); border-bottom:1px solid var(--line); }}
    nav ul {{ display:flex; flex-wrap:wrap; gap:.75rem; list-style:none; padding:0; }} a {{ color:var(--blue); }}
    .summary {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:.75rem; }} .metric,.card,.callout {{ border:1px solid var(--line); border-radius:.65rem; padding:1rem; background:var(--panel); }}
    .metric strong {{ display:block; font-size:1.65rem; }} .status {{ font-weight:700; padding:.12rem .35rem; border-radius:.25rem; }}
    .completed {{ color:var(--green); background:#e5f5ec; }} .represented {{ color:var(--blue); background:#e7f1fb; }} .open_gap {{ color:var(--amber); background:#fff3cd; }} .exact_gate {{ color:var(--red); background:#fde9ed; }}
    table {{ border-collapse:collapse; width:100%; margin:1rem 0; }} th,td {{ border:1px solid var(--line); padding:.55rem; text-align:left; vertical-align:top; }} th {{ background:#edf2f8; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:.8rem; }} code {{ overflow-wrap:anywhere; }}
    h1,h2,h3 {{ line-height:1.2; }} h2 {{ margin-top:2.2rem; }} .boundary {{ border-left:.35rem solid var(--red); padding-left:1rem; }}
    .skip {{ position:absolute; left:-9999px; }} .skip:focus {{ left:1rem; top:1rem; background:#fff; padding:.5rem; z-index:3; }}
    @media (max-width:700px) {{ table {{ display:block; overflow-x:auto; }} }}
  </style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header role="banner">
  <p>GHC Family · terminal six-owner trial</p>
  <h1>Eiren Kestrel v641-v6 terminal evidence report</h1>
  <p>This accessible static report summarizes bounded local evidence. It does not establish consciousness, personhood, AGI/ASI, a Theory of Everything, deployment, enacted law, or independent scientific reproduction.</p>
  <nav aria-label="Report sections"><ul><li><a href="#summary">Summary</a></li><li><a href="#proposals">Proposals</a></li><li><a href="#equation">Equation</a></li><li><a href="#thermo">Thermo-psyche</a></li><li><a href="#heart">Heart</a></li><li><a href="#stage20">Stage 20</a></li><li><a href="#boundaries">Boundaries</a></li></ul></nav>
</header>
<main id="main">
  <section id="summary" aria-labelledby="summary-title"><h2 id="summary-title">Verified truth summary</h2>
    <div class="summary">
      <div class="metric"><strong>{counts['completed']}</strong>Completed locally</div><div class="metric"><strong>{counts['represented']}</strong>Represented/proxy</div><div class="metric"><strong>{counts['open_gap']}</strong>Open gaps</div><div class="metric"><strong>{counts['exact_gate']}</strong>Exact gates</div><div class="metric"><strong>{truth['tests_passed']}</strong>Recorded tests passed</div><div class="metric"><strong>{source['source_count']}</strong>Primary/official source records</div>
    </div>
    <div class="callout"><p><strong>Terminal verdict:</strong> {esc(board['terminal_verdict'])}</p><p><strong>Reproduction:</strong> {esc(reproduction['state'])}; independent scientific reproduction remains false.</p><p><strong>Overview length:</strong> {overview_word_count} words.</p></div>
  </section>
  <section id="proposals" aria-labelledby="proposals-title"><h2 id="proposals-title">Ten frozen proposals</h2><div role="region" aria-label="Proposal dispositions" tabindex="0"><table><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Evidence paths</th></tr></thead><tbody>{rows}</tbody></table></div></section>
  <section id="equation" aria-labelledby="equation-title"><h2 id="equation-title">Mandala equation covenant</h2><p><code>{esc(covenant['canonical']['geometry_equation'])}</code></p><p><code>{esc(covenant['canonical']['omega_definition'])}</code></p><p>The equation is a {esc(covenant['canonical']['status'])}. Unique prediction, empirical likelihood, new-force detection, and consciousness-tensor fields are all false.</p><h3>Typed registers</h3><ul>{list_items([row['register'] + ': ' + row['obligation'] for row in covenant['registers']])}</ul></section>
  <section id="thermo" aria-labelledby="thermo-title"><h2 id="thermo-title">Thermo-psyche classification</h2><div role="region" aria-label="Thermo-psyche classifications" tabindex="0"><table><thead><tr><th scope="col">ID</th><th scope="col">Candidate</th><th scope="col">Classification</th><th scope="col">Physical law?</th><th scope="col">Reason</th></tr></thead><tbody>{candidate_rows}</tbody></table></div></section>
  <section id="heart" aria-labelledby="heart-title"><h2 id="heart-title">Freed ID and CBR gates</h2><p>Freed ID reaches only <strong>{esc(freed['current_highest_level'])}</strong>; cryptographic, resolution, interoperability, privacy, and governance completion remain absent.</p><p>CBR required authority absences: <strong>{cbr['required_absent_count']}</strong>. Enactment is not authorized, and Māori authority is not transferred or inferred.</p></section>
  <section id="stage20" aria-labelledby="stage-title"><h2 id="stage-title">Terminal Stage 20 board</h2><div class="cards">{claim_cards}</div></section>
  <section id="boundaries" class="boundary" aria-labelledby="boundary-title"><h2 id="boundary-title">Protected boundaries</h2><p>The following remain false or unestablished:</p><ul>{list_items(protected)}</ul><p>Retained negative IDs remain linked to downgrade consequences: {esc(', '.join(negatives['negative_ids']))}.</p></section>
</main>
<footer role="contentinfo"><p>Generated from public repository artifacts. Automated accessibility and privacy checks are bounded checks, not complete conformance or exhaustive security certification.</p></footer>
</body>
</html>
"""


def accessibility_audit(text: str) -> dict[str, Any]:
    checks = {
        "html_lang": '<html lang="en">' in text,
        "meta_viewport": 'name="viewport"' in text,
        "skip_link": 'href="#main"' in text,
        "main_landmark": '<main id="main">' in text,
        "nav_label": 'aria-label="Report sections"' in text,
        "table_headers": '<th scope="col">' in text,
        "responsive_table_regions": 'role="region"' in text,
        "no_script_dependency": "<script" not in text.lower(),
        "status_not_color_only": "Disposition" in text and "Completed locally" in text,
        "mobile_rule": "@media (max-width:700px)" in text,
    }
    return {
        "schema": "ghc.family.static-accessibility-audit.v6",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "valid": all(checks.values()),
        "full_wcag_conformance_established": False,
        "human_assistive_technology_review_completed": False,
        "boundary": "Automated structural checks do not establish complete accessibility conformance.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the accessible v641-v6 terminal report.")
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    phase = args.phase_dir.resolve()
    output = args.output.resolve()
    report = build_report(phase)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    audit = accessibility_audit(report)
    audit_path = phase / "validation/accessibility-audit.json"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": output.name, "bytes": output.stat().st_size, "accessibility": audit}, indent=2))
    return 0 if audit["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

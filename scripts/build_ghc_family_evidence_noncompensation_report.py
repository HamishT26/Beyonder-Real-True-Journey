#!/usr/bin/env python3
"""Build the accessible static v642-v5 non-compensation report."""

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


def table(headers: list[str], rows: list[list[Any]]) -> str:
    head = "".join(f'<th scope="col">{esc(value)}</th>' for value in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{esc(value)}</td>" for value in row) + "</tr>"
        for row in rows
    )
    return f"<div class=\"table-wrap\"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def build(phase: Path) -> Path:
    x1 = load(phase / "x1-proposals.json")
    x2 = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    sources = load(phase / "sources/source-ledger.json")
    checklist = load(phase / "complete-incomplete-checklist.json")
    local_negatives = negatives["negatives"][negatives["inherited_count"] :]
    proposal_rows = [
        [
            row["proposal_id"],
            row["title"],
            row["observed_disposition"],
            ", ".join(row["evidence"]),
            ", ".join(row["protected_gates_remain"]),
        ]
        for row in x2["proposals"]
    ]
    gate_rows = [
        [row["gate_id"], row["gate_class"], row["state"], row["requires"]]
        for row in gates["gates"]
    ]
    negative_rows = [
        [
            row["negative_id"],
            row.get("origin", "v642-v5"),
            row.get("statement", row.get("observed", "retained negative")),
            row.get("evidence", "retained-negative-register.json"),
        ]
        for row in local_negatives
    ]
    source_rows = [
        [
            row["source_id"],
            row["status_class"],
            row["title"],
            row["evidence_role"],
        ]
        for row in sources["added_sources"]
    ]
    completed = "".join(f"<li>{esc(value)}</li>" for value in checklist["complete"])
    incomplete = "".join(
        f"<li>{esc(value)}</li>" for value in checklist["incomplete_or_gated"]
    )
    counts = x2["disposition_counts"]
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sable Rook v642-v5 non-compensation evidence report</title>
<style>
:root {{ color-scheme: light dark; --bg:#f7f8fb; --card:#fff; --ink:#17202a; --muted:#46566b; --accent:#244e8a; --line:#c9d2df; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#10151d; --card:#18212c; --ink:#eef4fb; --muted:#c0cad7; --accent:#8fc1ff; --line:#405065; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font:1rem/1.6 system-ui,sans-serif; color:var(--ink); background:var(--bg); }}
a {{ color:var(--accent); }}
a:focus-visible, button:focus-visible {{ outline:3px solid #e57c00; outline-offset:3px; }}
.skip {{ position:absolute; left:-9999px; top:0; background:var(--card); padding:.75rem; z-index:2; }}
.skip:focus {{ left:1rem; top:1rem; }}
header, main, footer {{ width:min(76rem, 94vw); margin:auto; }}
header {{ padding:2.5rem 0 1rem; }}
section {{ background:var(--card); border:1px solid var(--line); border-radius:.6rem; padding:1.25rem; margin:1rem 0; }}
.summary {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(10rem,1fr)); gap:.75rem; }}
.metric {{ border-left:.35rem solid var(--accent); padding:.6rem .8rem; background:var(--bg); }}
.metric strong {{ display:block; font-size:1.35rem; }}
.table-wrap {{ overflow-x:auto; }}
table {{ border-collapse:collapse; width:100%; min-width:48rem; }}
th,td {{ border:1px solid var(--line); padding:.55rem; text-align:left; vertical-align:top; }}
th {{ background:var(--bg); }}
.boundary {{ border-left:.4rem solid #a33; padding-left:1rem; }}
footer {{ padding:1rem 0 3rem; color:var(--muted); }}
@media (prefers-reduced-motion: reduce) {{ *,*::before,*::after {{ scroll-behavior:auto!important; transition:none!important; animation:none!important; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main evidence</a>
<header role="banner">
<h1>Sable Rook v642-v5 non-compensation evidence report</h1>
<p>Accessible static view of the bounded local evidence packet. Sable Rook is relational working language only, not evidence of consciousness, personhood, or authority.</p>
</header>
<main id="main">
<section aria-labelledby="summary-heading">
<h2 id="summary-heading">Phase summary</h2>
<div class="summary">
<div class="metric"><strong>{x2['proposal_count']}</strong>frozen proposals</div>
<div class="metric"><strong>{counts['completed']}</strong>completed</div>
<div class="metric"><strong>{counts['represented']}</strong>represented</div>
<div class="metric"><strong>{counts['open_gap']}</strong>open gap</div>
<div class="metric"><strong>{counts['exact_gate']}</strong>exact gate</div>
<div class="metric"><strong>{negatives['negative_count']}</strong>retained negatives</div>
</div>
<p><strong>Terminal verdict:</strong> {esc(truth['terminal_verdict'])}. Route state: {esc(truth['route_state'])}.</p>
</section>
<section aria-labelledby="proposal-heading">
<h2 id="proposal-heading">Proposal dispositions and evidence</h2>
{table(['ID','Proposal','Disposition','Evidence','Protected gates'], proposal_rows)}
</section>
<section aria-labelledby="boundary-heading">
<h2 id="boundary-heading">Non-compensatory boundary</h2>
<p class="boundary">High local engineering evidence cannot offset zero empirical rows, absent real THOS arms or raters, missing production cryptography, no affected-party or Māori authority, or no independent executor. Missing or exact-gated evidence is not a score penalty; it is a veto.</p>
<p>GMUT remains a typed research scaffold. THOS remains a protocol proxy. Freed ID remains structural and synthetic. CBR and Māori authority remain exact-gated. No AGI, ASI, consciousness, personhood, deployment, exhaustive-security, complete-accessibility, Theory-of-Everything, proof or canon, empirical-confirmation, legal or cultural-ratification, fundamental thermo-psyche law, or independent-reproduction claim is made.</p>
</section>
<section aria-labelledby="gate-heading">
<h2 id="gate-heading">Open and exact gates</h2>
{table(['Gate','Class','State','Required evidence or authority'], gate_rows)}
</section>
<section aria-labelledby="negative-heading">
<h2 id="negative-heading">v642-v5 retained negatives</h2>
<p>All {negatives['inherited_count']} inherited negatives remain present. The table shows phase-local additions; later passing checks do not erase them.</p>
{table(['Negative','Origin','Observed boundary','Evidence'], negative_rows)}
</section>
<section aria-labelledby="source-heading">
<h2 id="source-heading">Phase-local primary and official sources</h2>
{table(['ID','Status','Source','Bounded role'], source_rows)}
</section>
<section aria-labelledby="check-heading">
<h2 id="check-heading">Complete and incomplete</h2>
<h3>Completed in the owned scope</h3><ul>{completed}</ul>
<h3>Incomplete, open, or exact-gated</h3><ul>{incomplete}</ul>
</section>
<section aria-labelledby="access-heading">
<h2 id="access-heading">Accessibility and privacy limits</h2>
<p>Automated structure is not complete accessibility conformance. Language, title, skip navigation, landmarks, heading order, table headers, visible focus, responsive overflow, and reduced-motion handling are present. Qualified manual evaluation and user participation remain open.</p>
<p>A zero-hit pattern scan is bounded evidence only. It is not proof of exhaustive privacy or security.</p>
</section>
</main>
<footer role="contentinfo">Generated from repository-relative v642-v5 evidence. Māori concepts, wording, data, and governance remain under Māori authority.</footer>
</body>
</html>
"""
    output = phase / "deliverables/v642-v5-noncompensation-report.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8", newline="\n")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    args = parser.parse_args()
    output = build(args.phase_dir.resolve())
    print(json.dumps({"output": output.as_posix()}, ensure_ascii=False))


if __name__ == "__main__":
    main()

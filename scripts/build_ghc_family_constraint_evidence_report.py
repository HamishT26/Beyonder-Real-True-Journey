#!/usr/bin/env python3
"""Build the accessible static v642-v7 constraint-evidence report."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        value = "; ".join(str(item) for item in value)
    return html.escape(str(value), quote=True)


def table(headers: list[str], rows: list[list[Any]], caption: str) -> str:
    head = "".join(f"<th scope=\"col\">{esc(item)}</th>" for item in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{esc(item)}</td>" for item in row) + "</tr>"
        for row in rows
    )
    return f"<div class=\"table-wrap\"><table><caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"


def build(phase: Path) -> Path:
    identity = load(phase / "identity-receipt.json")
    focus = load(phase / "focus/primary-focus-receipt.json")
    ledger = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    sources = load(phase / "sources/source-ledger.json")
    versions = load(phase / "environment/version-receipt.json")
    threat = load(phase / "threat-model.json")
    checklist = load(phase / "complete-incomplete-checklist.json")

    distribution = ledger["observed_distribution"]
    proposal_rows = [
        [
            row["proposal_id"],
            row["title"],
            row["observed_disposition"],
            row["evidence_class"],
            f"{row['matched_count']}/{row['case_count']}",
            row["retained_negative_count"],
            row["boundary"],
        ]
        for row in ledger["rows"]
    ]
    gap_rows = [[item["gate_id"], item["surface"], item["needs"]] for item in gates["open_gaps"]]
    exact_rows = [[item["gate_id"], item["surface"], item["reserved_to"]] for item in gates["exact_gates"]]
    threat_rows = [[item["threat_id"], item["class"], item["failure"], item["control"], item["residual_risk"]] for item in threat["threats"]]
    checklist_rows = [[item["item"], "complete" if item["complete"] else "pending"] for item in checklist["required_rows"]]
    source_rows = [
        [item["source_id"], item["title"], item["status_class"], item["evidence_role"]]
        for item in sources["added_sources"]
    ]
    negative_rows = [
        [item["negative_id"], item.get("origin", "inherited"), item.get("statement", "retained inherited negative"), item.get("recovery", "preserve and review")]
        for item in negatives["negatives"][-12:]
    ]

    output = phase / "deliverables/v642-v7-constraint-evidence-report.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tamar Vey v642-v7 constraint-evidence report</title>
<style>
:root {{ color-scheme: light dark; --bg:#fbfbfd; --fg:#15171a; --muted:#4a5260; --card:#ffffff; --line:#596273; --accent:#174ea6; --good:#0b6b3a; --warn:#7a4b00; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#11151a; --fg:#f4f6f8; --muted:#c3cad4; --card:#1b222b; --line:#aab4c2; --accent:#8ab4f8; --good:#78d7a3; --warn:#ffd27a; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:system-ui,-apple-system,"Segoe UI",sans-serif; background:var(--bg); color:var(--fg); line-height:1.55; }}
a {{ color:var(--accent); }}
.skip {{ position:absolute; left:-10000px; top:auto; }}
.skip:focus {{ left:1rem; top:1rem; z-index:10; padding:.75rem; background:var(--card); color:var(--fg); border:3px solid var(--accent); }}
:focus-visible {{ outline:3px solid var(--accent); outline-offset:3px; }}
header, main, footer {{ max-width:1120px; margin:auto; padding:1.25rem; }}
header {{ border-bottom:3px solid var(--accent); }}
.lede {{ max-width:78ch; font-size:1.1rem; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:1rem; margin:1rem 0; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:.5rem; padding:1rem; }}
.metric {{ font-size:1.7rem; font-weight:750; display:block; }}
.good {{ color:var(--good); }} .warn {{ color:var(--warn); }}
nav ul {{ display:flex; flex-wrap:wrap; gap:.75rem 1.25rem; padding-left:1.2rem; }}
section {{ margin-block:2.2rem; scroll-margin-top:1rem; }}
.table-wrap {{ overflow-x:auto; border:1px solid var(--line); border-radius:.4rem; }}
table {{ border-collapse:collapse; width:100%; min-width:760px; background:var(--card); }}
caption {{ text-align:left; font-weight:700; padding:.75rem; color:var(--fg); }}
th, td {{ border-top:1px solid var(--line); padding:.65rem; text-align:left; vertical-align:top; }}
th {{ background:color-mix(in srgb,var(--card) 80%,var(--accent) 20%); }}
code {{ overflow-wrap:anywhere; }}
@media print {{ body {{ background:white; color:black; }} a {{ color:black; }} .skip, nav {{ display:none; }} section {{ break-inside:avoid; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main evidence</a>
<header>
<p><strong>GHC Family · v642-v7 · static evidence report</strong></p>
<h1>Tamar Vey constraint-evidence packet</h1>
<p class="lede">Ten frozen proposals were executed as bounded local, structural, and synthetic checks. The terminal verdict is <strong>{esc(truth['terminal_verdict'])}</strong>. Local engineering passes do not close empirical, participant, production, legal, cultural, Māori-authority, accessibility, security-review, deployment, or independent-reproduction gates.</p>
<nav aria-label="Report sections"><ul>
<li><a href="#truth">Truth summary</a></li><li><a href="#proposals">Proposals</a></li><li><a href="#mind">Mind, Body, Heart</a></li><li><a href="#gates">Open and exact gates</a></li><li><a href="#threats">Threat model</a></li><li><a href="#negatives">Retained negatives</a></li><li><a href="#sources">Sources and versions</a></li><li><a href="#checklist">Checklist</a></li><li><a href="#accessibility">Accessibility boundary</a></li>
</ul></nav>
</header>
<main id="main" tabindex="-1">
<section id="truth">
<h2>Phase truth</h2>
<div class="grid">
<div class="card"><span class="metric good">{distribution['completed']}</span>completed</div>
<div class="card"><span class="metric">{distribution['represented']}</span>represented or proxy</div>
<div class="card"><span class="metric warn">{distribution['open_gap']}</span>open gap</div>
<div class="card"><span class="metric warn">{distribution['exact_gate']}</span>exact gate</div>
<div class="card"><span class="metric">{ledger['total_matched_count']}/{ledger['total_case_count']}</span>matched preregistered cases</div>
<div class="card"><span class="metric">{negatives['negative_count']}</span>retained negatives</div>
</div>
<p>Every observed label comes from exactly four allowed classes: completed, represented, open gap, or exact gate. Completed means only bounded local execution. Represented means a schema, protocol, or synthetic proxy exists without establishing external reality.</p>
<p><strong>Identity boundary:</strong> {esc(identity['name'])} ({esc(identity['pronouns'])}) is relational working language for the role “{esc(identity['role'])}”. It is not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.</p>
</section>
<section id="proposals">
<h2>Ten frozen proposals</h2>
{table(['ID','Proposal','Observed truth','Evidence class','Cases','Retained rejections','Boundary'], proposal_rows, 'Proposal outcomes and bounded evidence classes')}
</section>
<section id="mind">
<h2>Mind, Body, and Heart</h2>
<p><strong>Primary focus:</strong> {esc(focus['primary_focus'])}. GMUT Mind adds a constraint-algebra and physical degree-of-freedom obligation plus a synthetic observation-process boundary. These are typed research-model checks, not empirical confirmation, a detected force, a unique prediction, proof, final physics, or a Theory of Everything.</p>
<p>THOS Body adds blinded intercurrent-event and protocol-deviation estimand fixtures. There are no real participants, raters, or arms, no ethics approval, and no independent review; therefore no superiority, AGI, ASI, consciousness, sentience, or personhood result exists.</p>
<p>Freed ID and CBR Heart add credential-schema evolution controls and an exact jurisdiction/forum deferral. Structural identity checks do not provide real cryptography, live services, interoperability, privacy assurance, independent security review, or trust governance. Technical artifacts do not choose governing law, forum competence, Māori wording, Māori authority, cultural ratification, or enacted law.</p>
</section>
<section id="gates">
<h2>Open gaps and exact gates</h2>
{table(['Gate','Surface','Needed evidence'], gap_rows, 'Five open gaps that remain unresolved')}
{table(['Gate','Surface','Reserved authority'], exact_rows, 'Six exact gates reserved to competent authority')}
</section>
<section id="threats">
<h2>Bounded threat model</h2>
<p>The threat model has explicit resource ceilings and recovery controls. It is not exhaustive security and has not received independent security review.</p>
{table(['ID','Class','Failure','Control','Residual risk'], threat_rows, 'Threats, controls, and residual open or exact gates')}
</section>
<section id="negatives">
<h2>Retained negatives</h2>
<p>The register preserves {negatives['inherited_count']} inherited negatives and every new operational or synthetic rejection. Passing reruns do not erase earlier failures.</p>
{table(['Negative','Origin','Statement','Recovery'], negative_rows, 'Most recent retained negatives (the complete register remains machine-readable)')}
</section>
<section id="sources">
<h2>Sources and environment</h2>
<p>The effective source ledger contains {sources['effective_source_count']} primary or official entries: {sources['effective_status_counts']['current']} current, {sources['effective_status_counts']['stable']} stable, {sources['effective_status_counts']['draft']} draft, and {sources['effective_status_counts']['watch']} watch. Draft and watch sources remain visibly non-stable.</p>
{table(['ID','Source','Status','Bounded evidence role'], source_rows, 'Sources added for v642-v7')}
<p>Observed versions: Codex CLI {esc(versions['codex_cli_local'])}, Codex desktop {esc(versions['codex_desktop_local'])} ({esc(versions['codex_desktop_status'])}), Python {esc(versions['python'])}, Git {esc(versions['git'])}. Versions were verified only; no desktop, CLI, host feature, or unrelated system update was performed.</p>
</section>
<section id="checklist">
<h2>Complete and incomplete checklist</h2>
{table(['Item','State'], checklist_rows, 'Closeout checklist at the current evidence state')}
<p>Open gaps and exact gates are valid outcomes. Final closeout still requires clean detached evidence, closeout, seal, and final-head validation plus remote equality.</p>
</section>
<section id="accessibility">
<h2>Accessibility boundary</h2>
<p>This report is static, uses semantic headings, a skip link, keyboard-visible focus, captions, flexible layout, high-contrast tokens, and print styles. These structural checks are not a complete accessibility conformance claim. Manual accessibility evaluation and affected-user evaluation remain open.</p>
</section>
</main>
<footer><p>Terminal verdict: <strong>{esc(truth['terminal_verdict'])}</strong>. Same-owner repeatability is not independent-team scientific reproduction.</p></footer>
</body>
</html>
"""
    output.write_text(document, encoding="utf-8", newline="\n")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", required=True)
    args = parser.parse_args()
    output = build(Path(args.phase_dir).resolve())
    print(json.dumps({"report": output.as_posix()}, ensure_ascii=False))


if __name__ == "__main__":
    main()

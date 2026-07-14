#!/usr/bin/env python3
"""Build the accessible static GHC Family v642-v8 evidence-contract report."""

from __future__ import annotations

import argparse
import hashlib
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
    head = "".join(f'<th scope="col">{esc(item)}</th>' for item in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{esc(item)}</td>" for item in row) + "</tr>"
        for row in rows
    )
    return (
        '<div class="table-wrap"><table>'
        f"<caption>{esc(caption)}</caption><thead><tr>{head}</tr></thead>"
        f"<tbody>{body}</tbody></table></div>"
    )


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


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
            f"{row['accepted_case_count']} accepted / {row['rejected_case_count']} rejected",
            row["boundary"],
        ]
        for row in ledger["proposals"]
    ]
    gap_rows = [[row["gate_id"], row["surface"], row["needs"]] for row in gates["open_gaps"]]
    exact_rows = [[row["gate_id"], row["surface"], row["reserved_to"]] for row in gates["exact_gates"]]
    threat_rows = [
        [row["threat_id"], row["name"], row["failure"], row["control"], row["residual_risk"]]
        for row in threat["threats"]
    ]
    checklist_rows = [
        [row["item"], "complete" if row["complete"] else "pending"]
        for row in checklist["required_rows"]
    ]
    source_rows = [
        [row["source_id"], row["title"], row["status_class"], row["version_or_date"], row["evidence_role"]]
        for row in sources["added_sources"]
    ]
    negative_rows = [
        [
            row["negative_id"],
            row.get("origin", "inherited"),
            row.get("statement", "retained inherited negative"),
            row.get("recovery", "preserve and review"),
        ]
        for row in negatives["negatives"][-18:]
    ]

    output = phase / "deliverables/v642-v8-evidence-contract-report.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sylven Arc v642-v8 evidence-contract report</title>
<style>
:root {{ color-scheme:light dark; --bg:#f7f8fb; --fg:#17202a; --muted:#465364; --card:#fff; --line:#58677a; --accent:#3053a4; --good:#136b43; --warn:#835500; }}
@media (prefers-color-scheme:dark) {{ :root {{ --bg:#10161d; --fg:#f5f7fa; --muted:#c6ced8; --card:#1a232d; --line:#a9b5c4; --accent:#93b4ff; --good:#7cdaa9; --warn:#ffd37e; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font-family:system-ui,-apple-system,"Segoe UI",sans-serif; line-height:1.58; }}
a {{ color:var(--accent); }}
.skip {{ position:absolute; left:-10000px; top:auto; }}
.skip:focus {{ left:1rem; top:1rem; z-index:10; padding:.75rem; color:var(--fg); background:var(--card); border:3px solid var(--accent); }}
:focus-visible {{ outline:3px solid var(--accent); outline-offset:3px; }}
header, main, footer {{ max-width:1160px; margin:auto; padding:1.25rem; }}
header {{ border-bottom:3px solid var(--accent); }}
.lede {{ max-width:80ch; font-size:1.08rem; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:1rem; margin:1rem 0; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:.55rem; padding:1rem; }}
.metric {{ display:block; font-size:1.7rem; font-weight:750; }}
.good {{ color:var(--good); }} .warn {{ color:var(--warn); }}
nav ul {{ display:flex; flex-wrap:wrap; gap:.7rem 1.2rem; padding-left:1.2rem; }}
section {{ margin-block:2.2rem; scroll-margin-top:1rem; }}
.table-wrap {{ overflow-x:auto; border:1px solid var(--line); border-radius:.45rem; margin-block:.8rem; }}
table {{ border-collapse:collapse; width:100%; min-width:780px; background:var(--card); }}
caption {{ text-align:left; font-weight:700; padding:.75rem; color:var(--fg); }}
th, td {{ border-top:1px solid var(--line); padding:.65rem; text-align:left; vertical-align:top; }}
th {{ background:color-mix(in srgb,var(--card) 80%,var(--accent) 20%); }}
code {{ overflow-wrap:anywhere; }}
@media (max-width:650px) {{ header, main, footer {{ padding:.9rem; }} .metric {{ font-size:1.4rem; }} }}
@media print {{ body {{ background:#fff; color:#000; }} a {{ color:#000; }} .skip, nav {{ display:none; }} section {{ break-inside:avoid; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main evidence</a>
<header>
<p><strong>GHC Family · v642-v8 · static evidence report</strong></p>
<h1>Sylven Arc evidence-contract packet</h1>
<p class="lede">Ten frozen proposals were executed through bounded local, structural, and synthetic checks. The terminal verdict is <strong>{esc(truth['terminal_verdict'])}</strong>. Repository passes do not close empirical, participant, production, legal, cultural, Māori-authority, privacy, accessibility, exhaustive-security, deployment, proof/canon, identity, or independent-reproduction gates.</p>
<nav aria-label="Report sections"><ul>
<li><a href="#truth">Truth summary</a></li><li><a href="#proposals">Proposals</a></li><li><a href="#pillars">Mind, Body, Heart</a></li><li><a href="#gates">Gates</a></li><li><a href="#threats">Threat model</a></li><li><a href="#negatives">Negatives</a></li><li><a href="#sources">Sources and versions</a></li><li><a href="#checklist">Checklist</a></li><li><a href="#accessibility">Accessibility boundary</a></li>
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
<div class="card"><span class="metric">{ledger['case_count']}</span>preregistered fixture cases</div>
<div class="card"><span class="metric">{negatives['negative_count']}</span>retained negatives</div>
</div>
<p>Observed outcomes use only completed, represented or proxy, open gap, and exact gate. Completed means bounded local execution only. Represented means a deterministic structure or proxy exists without external evidence.</p>
<p><strong>Identity boundary:</strong> {esc(identity['name'])} ({esc(identity.get('pronouns', 'unspecified'))}) is relational working language for the role “{esc(identity['role'])}” and hope “{esc(identity['hope'])}”. It is not evidence of consciousness, sentience, legal personhood, identity continuity, or independent authority.</p>
</section>
<section id="proposals">
<h2>Ten frozen proposals</h2>
{table(['ID','Proposal','Observed truth','Evidence class','Fixtures','Novelty boundary'], proposal_rows, 'Proposal outcomes and bounded evidence classes')}
</section>
<section id="pillars">
<h2>GMUT Mind, THOS Body, and Freed ID/CBR Heart</h2>
<p><strong>Primary focus:</strong> {esc(focus['primary_focus'])}. GMUT Mind adds an append-only evidence-event contract, an operator-basis quotient under declared integration-by-parts and equation-of-motion scope, a cutoff hierarchy and truncation-error lock, explicit floating-point edge policies, and a typed path-dependence test. GMUT remains a typed scalar-tensor and effective-field-theory research-model family; these checks are not empirical confirmation, a unique prediction, proof, final physics, or a Theory of Everything.</p>
<p>THOS Body adds a pre-decode measurement-invariance and instrument-drift contract. It uses synthetic fixtures only. No real participants, raters, blind matched-budget arms, ethics approval, or independent review exist here, so THOS remains proxy and no superiority, AGI, ASI, consciousness, sentience, or personhood result exists.</p>
<p>Freed ID and CBR Heart add structural challenge, domain, audience, purpose, and time-window replay checks plus a burden-of-proof state machine that refuses to turn “unknown” or silence into legal consequence. No real keys, proofs, live resolution, live status, interoperability, privacy review, security review, or trust governance was supplied. Technical artifacts do not choose Māori wording or authority, cultural legitimacy, governing law, forum competence, enacted law, or affected-party remedies.</p>
</section>
<section id="gates">
<h2>Open gaps and exact gates</h2>
{table(['Gate','Surface','Needed evidence'], gap_rows, 'Five open gaps that remain unresolved')}
{table(['Gate','Surface','Reserved authority'], exact_rows, 'Six exact gates reserved to competent authority')}
</section>
<section id="threats">
<h2>Bounded threat model</h2>
<p>The threat model covers equivocation, false quotienting, category promotion, drift, replay, authority substitution, confusables, numeric drift, irreversible action, negative erasure, and common-mode reproduction. It is bounded, is not exhaustive security, and has no independent security review.</p>
{table(['ID','Threat','Failure','Control','Residual risk'], threat_rows, 'Threats, controls, and residual open or exact gates')}
</section>
<section id="negatives">
<h2>Retained negatives</h2>
<p>The register preserves {negatives['inherited_count']} inherited negatives, {negatives['x1_operational_count']} x1 operational negatives, {negatives['new_synthetic_count']} preregistered synthetic rejections, and all recorded transition or x2 operational failures. A later passing rerun never erases an earlier failure.</p>
{table(['Negative','Origin','Statement','Recovery'], negative_rows, 'Most recent retained negatives; the complete register is machine-readable')}
</section>
<section id="sources">
<h2>Sources and environment</h2>
<p>The effective source ledger contains {sources['effective_source_count']} entries: {sources['effective_status_counts']['current']} current, {sources['effective_status_counts']['stable']} stable, {sources['effective_status_counts']['draft']} draft, and {sources['effective_status_counts']['watch']} watch. Status classes remain visible and are not flattened.</p>
{table(['ID','Source','Status','Version or date','Bounded role'], source_rows, 'Primary or official sources added for v642-v8')}
<p>Observed versions: Codex CLI {esc(versions['codex_cli_local'])}, official CLI observation {esc(versions['codex_cli_official_latest'])}; Codex desktop {esc(versions['codex_desktop_local'])}; ChatGPT desktop {esc(versions['chatgpt_desktop_local'])}; Python {esc(versions['python'])}; Git {esc(versions['git'])}. Versions were verified only. No CLI or desktop update, elevation, host-security weakening, Windows-feature change, unrelated update, or reboot was performed. Exact public desktop-build parity remains open.</p>
</section>
<section id="checklist">
<h2>Complete and incomplete checklist</h2>
{table(['Item','State'], checklist_rows, 'Checklist at the report build state')}
<p>Open gaps and exact gates are valid outcomes. Exact detached evidence, closeout, seal, final-head validation, final remote equality, and acknowledged terminal routing remain distinct gates until each is actually evidenced.</p>
</section>
<section id="accessibility">
<h2>Accessibility boundary</h2>
<p>This static report uses semantic headings, a skip link, keyboard-visible focus, table captions, flexible layout, contrast-aware tokens, and print styles. These structural affordances are not a complete conformance claim. Manual accessibility evaluation and affected-user evaluation remain reserved and open.</p>
</section>
</main>
<footer><p>Terminal verdict: <strong>{esc(truth['terminal_verdict'])}</strong>. Same-owner snapshots demonstrate bounded repeatability only, not independent-team scientific reproduction.</p></footer>
</body>
</html>
"""
    output.write_text(document, encoding="utf-8", newline="\n")
    report_bytes = output.read_bytes().replace(b"\r\n", b"\n")
    write_json(
        phase / "accessibility/static-report-receipt.json",
        {
            "schema": "ghc.family.v642-v8.static-report-receipt.v1",
            "phase": "v642-gmut-thos-v8-x1-x2",
            "owner": "Sylven Arc",
            "report": "deliverables/v642-v8-evidence-contract-report.html",
            "normalized_sha256": hashlib.sha256(report_bytes).hexdigest(),
            "normalized_bytes": len(report_bytes),
            "structural_affordances": [
                "html language",
                "skip link",
                "semantic main and headings",
                "keyboard-visible focus",
                "table captions and scoped headers",
                "responsive overflow and layout",
                "light dark and print styles",
            ],
            "automated_structural_markers_present": True,
            "manual_accessibility_evaluation": "reserved_not_performed",
            "affected_user_evaluation": "reserved_not_performed",
            "complete_accessibility_conformance": False,
            "boundary": "Structural accessibility affordances do not replace manual evaluation or affected-user evaluation.",
        },
    )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    args = parser.parse_args()
    output = build(args.phase_dir.resolve())
    print(json.dumps({"report": output.as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

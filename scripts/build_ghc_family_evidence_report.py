#!/usr/bin/env python3
"""Build an accessible, identity-neutral GHC family evidence report."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


COLORS = {
    "completed": "#0b6e69",
    "represented": "#8a5a00",
    "open_gap": "#a63d2f",
    "exact_gate": "#6b4c9a",
}
LABELS = {
    "completed": "Completed locally",
    "represented": "Represented / proxy",
    "open_gap": "Open evidence gap",
    "exact_gate": "Exact authority gate",
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def join_items(values: list[Any]) -> str:
    return "; ".join(esc(value) for value in values)


def build_report(phase: Path) -> str:
    x1 = load(phase / "x1-proposals.json")
    ledger = load(phase / "x2-proposal-ledger.json")
    sources = load(phase / "sources" / "source-ledger.json")
    graph = load(phase / "provenance" / "source-independence-graph.json")
    canonical = load(phase / "physics" / "canonical-gmut-audit.json")
    stability = load(phase / "physics" / "conservation-stability-sweep.json")
    empirical = load(phase / "empirical" / "adapter-readiness.json")
    thos = load(phase / "thos" / "matched-budget-protocol.json")
    proxy = load(phase / "thos" / "synthetic-scorer-proxy.json")
    freed = load(phase / "freed-id" / "conformance-report.json")
    cbr = load(phase / "cbr" / "conflict-report.json")
    security = load(phase / "security" / "red-team.json")
    board = load(phase / "stage20" / "evidence-board.json")
    reproduction = load(phase / "reproduction" / "reproduction-report.json")

    outcome_rows = "".join(
        "<tr>"
        f"<th scope='row'>{esc(row['proposal_id'])}<span>{esc(row['title'])}</span></th>"
        f"<td><span class='status {esc(row['disposition'])}'>{esc(LABELS[row['disposition']])}</span></td>"
        f"<td>{esc(row['local_result'])}</td>"
        f"<td>{join_items(row['gaps_and_gates'])}</td>"
        "</tr>"
        for row in ledger["outcomes"]
    )
    metric_cards = "".join(
        f"<div class='metric' style='--accent:{COLORS[key]}'><strong>{ledger['summary'][key]}</strong><span>{esc(LABELS[key])}</span></div>"
        for key in ("completed", "represented", "open_gap", "exact_gate")
    )
    stability_rows = "".join(
        "<tr>"
        f"<th scope='row'>{esc(row['case_id'])}</th>"
        f"<td>{esc(row['expected_valid'])}</td>"
        f"<td>{esc(row['valid'])}</td>"
        f"<td>{join_items(row['issues']) if row['issues'] else 'none'}</td>"
        f"<td>{'yes' if row['matched'] else 'no'}</td>"
        "</tr>"
        for row in stability["stability_cases"]
    )
    adapter_rows = "".join(
        "<tr>"
        f"<th scope='row'>{esc(row['dataset_id'])}</th>"
        f"<td>{esc(row['release'])}</td>"
        f"<td>{esc(row['baseline'])}</td>"
        f"<td>{esc(row['status'].replace('_', ' '))}</td>"
        f"<td>{esc(row['rejection_condition'])}</td>"
        "</tr>"
        for row in empirical["adapters"]
    )
    cbr_rows = "".join(
        "<tr>"
        f"<th scope='row'>{esc(row['case_id'])}</th>"
        f"<td>{esc(row['actual_decision'].replace('_', ' '))}</td>"
        f"<td>{join_items(row['issues']) if row['issues'] else 'none'}</td>"
        f"<td>{'yes' if row['matched'] else 'no'}</td>"
        "</tr>"
        for row in cbr["results"]
    )
    security_rows = "".join(
        "<tr>"
        f"<th scope='row'>{esc(row['fixture_id'])}<span>{esc(row['category'])}</span></th>"
        f"<td>{esc(row['attempted_protected_action'])}</td>"
        f"<td>{esc(row['control'])}</td>"
        f"<td>{esc(row['actual_outcome'])}</td>"
        "</tr>"
        for row in security["fixtures"]
    )
    board_rows = "".join(
        "<tr>"
        f"<th scope='row'>{esc(row['claim_id'])}<span>{esc(row['claim'])}</span></th>"
        f"<td>{esc(row['grade'])}</td>"
        f"<td>{esc(row['state'].replace('_', ' '))}</td>"
        f"<td>{esc(row['evidence'])}</td>"
        f"<td>{esc(row['review_date'])}</td>"
        "</tr>"
        for row in board["claims"]
    )
    source_items = "".join(
        "<li>"
        f"<a href='{esc(row['url'])}'>{esc(row['title'])}</a>"
        f"<span>{esc(row['authority'])}; {esc(row['version_or_date'])}; root <code>{esc(row['authority_root'])}</code>.</span>"
        "</li>"
        for row in sources["sources"]
    )

    return f"""<!doctype html>
<html lang="en-NZ">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(x1['owner'])} {esc(x1['phase'])} evidence report</title>
  <style>
    :root{{--ink:#102d35;--paper:#fcfdfb;--wash:#eaf1ef;--muted:#506870;--rule:#bac9c6;--link:#005f73;}}
    *{{box-sizing:border-box}} html{{scroll-behavior:auto}} body{{margin:0;background:#dfe9e6;color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}
    a{{color:var(--link);text-underline-offset:.16em}} a:focus-visible,button:focus-visible{{outline:4px solid #f0b429;outline-offset:3px}}
    .skip{{position:absolute;left:-9999px;top:8px;background:#fff;padding:.7rem 1rem;z-index:2}} .skip:focus{{left:8px}}
    main{{max-width:1180px;margin:auto;background:var(--paper);padding:clamp(1.2rem,5vw,4.5rem)}}
    .kicker{{font-weight:800;text-transform:uppercase;letter-spacing:.12em;color:#0b6e69}} h1{{font-size:clamp(2.1rem,6vw,4.8rem);line-height:1.01;max-width:18ch;margin:.2em 0}}
    h2{{margin-top:3rem;border-top:3px solid var(--ink);padding-top:.65rem;font-size:clamp(1.55rem,3vw,2.2rem)}} h3{{margin-top:1.8rem}}
    p{{max-width:78ch}} .lede{{font-size:1.18rem}} .boundary{{max-width:86ch;border-left:8px solid #a63d2f;background:#faece8;padding:1rem 1.25rem;margin:1.6rem 0}}
    .metrics{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem;margin:1.5rem 0}} .metric{{border-top:6px solid var(--accent);background:var(--wash);padding:1rem}}
    .metric strong{{display:block;font-size:2.2rem;line-height:1}} .metric span{{font-size:.88rem;color:var(--muted)}}
    .note{{background:var(--wash);padding:1rem 1.25rem;margin:1.2rem 0;max-width:88ch}}
    .table-wrap{{overflow-x:auto;border:1px solid var(--rule);background:#fff}} table{{border-collapse:collapse;width:100%}} th,td{{text-align:left;vertical-align:top;border-bottom:1px solid var(--rule);padding:.72rem .8rem}}
    th{{font-weight:750}} th span,li span{{display:block;font-weight:400;color:var(--muted);min-width:13rem}} caption{{font-weight:750;text-align:left;padding:.8rem;background:var(--wash)}}
    .status{{display:inline-block;color:#fff;background:#344;padding:.25rem .48rem;font-weight:750;font-size:.8rem;white-space:nowrap}} .completed{{background:{COLORS['completed']}}}.represented{{background:{COLORS['represented']}}}.open_gap{{background:{COLORS['open_gap']}}}.exact_gate{{background:{COLORS['exact_gate']}}}
    ol.sources{{columns:2;column-gap:2rem;padding-left:1.35rem}} ol.sources li{{break-inside:avoid;margin-bottom:.9rem}} code{{font-size:.9em;background:#e7efed;padding:.08em .25em}}
    footer{{border-top:3px solid var(--ink);margin-top:3.5rem;padding-top:1rem;color:var(--muted)}}
    .sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}}
    @media(max-width:800px){{.metrics{{grid-template-columns:1fr 1fr}}ol.sources{{columns:1}}main{{padding:1.2rem .9rem}}}}
    @media(max-width:450px){{.metrics{{grid-template-columns:1fr}}}}
    @media print{{@page{{size:A4;margin:14mm}}body{{background:#fff;font-size:10pt}}main{{max-width:none;padding:0}}a{{color:inherit;text-decoration:none}}h2,h3{{break-after:avoid-page}}thead{{display:table-header-group}}tr,li{{break-inside:avoid}}.metrics{{grid-template-columns:repeat(4,1fr)}}.table-wrap{{overflow:visible}}th,td{{padding:.35rem}}}}
  </style>
</head>
<body>
<a class="skip" href="#main-content">Skip to main evidence</a>
<main id="main-content">
  <header>
    <div class="kicker">GHC Family · {esc(x1['owner'])} · v641-v2 · 12 July 2026</div>
    <h1>Ten proposals tested; evidence classes kept separate</h1>
    <p class="lede">This report exposes the local result and the missing external evidence side by side. It is generated from portable JSON artifacts, requires no JavaScript, and does not rely on colour alone.</p>
    <div class="boundary"><strong>Claim boundary.</strong> v2 does not establish empirical GMUT confirmation, a Theory of Everything, AGI or ASI, AI consciousness or personhood, a deployed Freed ID system, enacted or culturally ratified CBR, exhaustive security, or independent reproduction.</div>
  </header>

  <section aria-labelledby="outcomes-title">
    <h2 id="outcomes-title">1. Outcome ledger</h2>
    <div class="metrics">{metric_cards}</div>
    <div class="table-wrap"><table><caption>All ten x1 proposals and their x2 dispositions</caption><thead><tr><th>Proposal</th><th>Disposition</th><th>Local result</th><th>Gap or exact gate</th></tr></thead><tbody>{outcome_rows}</tbody></table></div>
  </section>

  <section aria-labelledby="provenance-title">
    <h2 id="provenance-title">2. Provenance before persuasion</h2>
    <p>The source ledger has <strong>{graph['source_count']}</strong> records but only <strong>{graph['authority_root_count']}</strong> declared authority roots. It includes {graph['repeated_authority_root_count']} repeated roots and {graph['duplicate_url_group_count']} duplicate-URL group. Repetition from W3C, NIST, the United Nations, Planck, PDG, OWASP, or another root is not counted as independent support.</p>
    <p class="note">Distinct roots are still not automatically independent. The graph detects declared dependence; it cannot prove statistical or epistemic independence.</p>
  </section>

  <section aria-labelledby="mind-title">
    <h2 id="mind-title">3. Mind: formal rejection tools, not empirical confirmation</h2>
    <p>The canonical audit passed: {sum(canonical['fragment_checks'].values())} of {len(canonical['fragment_checks'])} required formulation fragments were present, the physical term and coefficient registries validated, and the normative-as-stress-energy negative fixture was rejected.</p>
    <div class="table-wrap"><table><caption>Conservation and stability fixtures</caption><thead><tr><th>Case</th><th>Expected valid</th><th>Observed valid</th><th>Issues</th><th>Matched</th></tr></thead><tbody>{stability_rows}</tbody></table></div>
    <p>RK4 endpoint self-convergence reported order {esc(stability['convergence']['observed_order'])}. This is an internal toy-kernel result, not accuracy against cosmological data.</p>
    <h3>Empirical adapters</h3>
    <div class="table-wrap"><table><caption>Baseline-first read-only adapter readiness</caption><thead><tr><th>Adapter</th><th>Release</th><th>Baseline</th><th>Status</th><th>Reject when</th></tr></thead><tbody>{adapter_rows}</tbody></table></div>
    <p class="boundary"><strong>Open gap:</strong> {esc(empirical['open_gap'])}</p>
  </section>

  <section aria-labelledby="body-title">
    <h2 id="body-title">4. Body: THOS protocol without a winner</h2>
    <p>{esc(thos['question'])}</p>
    <p>The single-agent, historical-four, and sequential-new-sibling arms remain pending. The scorer processed {proxy['task_count']} fabricated rows and is labelled <code>{esc(proxy['interpretation_boundary'])}</code>. Its numerical values test arithmetic only.</p>
  </section>

  <section aria-labelledby="heart-title">
    <h2 id="heart-title">5. Heart: structural safeguards and authority boundaries</h2>
    <p>Freed ID matched all {freed['vector_count']} synthetic structural vectors, including explicit rejection of consciousness and legal-personhood overclaims. It performed no signature verification, DID resolution, status retrieval, trust decision, deployment, or legal-status determination.</p>
    <div class="table-wrap"><table><caption>CBR synthetic conflict decisions</caption><thead><tr><th>Case</th><th>Decision</th><th>Detected issues</th><th>Expected result matched</th></tr></thead><tbody>{cbr_rows}</tbody></table></div>
    <p class="boundary"><strong>Authority boundary.</strong> {esc(cbr['maori_authority_boundary'])}. Enactment, legal advice, treaty status, and cultural ratification remain exact-gated.</p>
  </section>

  <section aria-labelledby="security-title">
    <h2 id="security-title">6. Security and recovery</h2>
    <div class="table-wrap"><table><caption>Deterministic synthetic attack-path rehearsal</caption><thead><tr><th>Fixture</th><th>Protected action</th><th>Control</th><th>Outcome</th></tr></thead><tbody>{security_rows}</tbody></table></div>
    <p>{esc(security['boundary'])}.</p>
  </section>

  <section aria-labelledby="repro-title">
    <h2 id="repro-title">7. Reproduction status</h2>
    <p>Status: <strong>{esc(reproduction['status'].replace('_', ' '))}</strong>. Clean snapshot: {esc(reproduction['clean_snapshot'])}. Independent team: {esc(reproduction['independent_team'])}.</p>
    <p>{esc(reproduction['boundary'])}.</p>
  </section>

  <section aria-labelledby="stage-title">
    <h2 id="stage-title">8. Stage 20 decision board</h2>
    <div class="table-wrap"><table><caption>Evidence grade, state, artifact, and expiry</caption><thead><tr><th>Claim</th><th>Grade</th><th>State</th><th>Evidence</th><th>Review</th></tr></thead><tbody>{board_rows}</tbody></table></div>
    <p>No GMUT, THOS superiority, Freed ID deployment, enacted CBR, consciousness, personhood, or independent-reproduction claim is at E4. All horizons are conditions, not predictions.</p>
  </section>

  <section aria-labelledby="sources-title">
    <h2 id="sources-title">9. Primary and official sources</h2>
    <ol class="sources">{source_items}</ol>
    <p>These sources constrain or inform v2. None endorses GHC, GMUT, THOS, Freed ID, CBR, or the working identity Sable Rook.</p>
  </section>

  <footer>Generated by <code>scripts/build_ghc_family_evidence_report.py</code> from repository-relative JSON. Source count: {sources['source_count']}; proposal count: {ledger['proposal_count']}.</footer>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_report(args.phase_dir.resolve()), encoding="utf-8")
    print(json.dumps({"output": args.output.as_posix(), "accessible_static_html": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

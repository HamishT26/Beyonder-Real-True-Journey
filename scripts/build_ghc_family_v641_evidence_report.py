#!/usr/bin/env python3
"""Build the accessible v641 evidence-board HTML and update the parent report."""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


COLORS = {
    "completed": "#176b74",
    "represented": "#9b6b16",
    "open_gap": "#a1452d",
    "exact_gate": "#6d4a82",
}
LABELS = {
    "completed": "Completed locally",
    "represented": "Represented / proxy",
    "open_gap": "Open evidence gap",
    "exact_gate": "Exact authority gate",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value) -> str:
    return html.escape(str(value))


def build_report(phase: Path) -> str:
    ledger = load(phase / "80-work-unit-ledger.json")
    board = load(phase / "stage20" / "evidence-board.json")
    sources = load(phase / "sources" / "source-ledger.json")
    empirical = load(phase / "empirical" / "adapter-manifest.json")
    freed = load(phase / "freed-id" / "conformance-report.json")
    thos = load(phase / "thos" / "synthetic-scorer-calibration-output.json")
    units = ledger["work_units"]
    counts = Counter(row["x2"]["disposition"] for row in units)
    matrix: dict[int, list[str]] = defaultdict(list)
    mission_names: dict[int, str] = {}
    for row in units:
        version = int(row["origin_plan_slot"].split("-")[0][1:])
        matrix[version].append(row["x2"]["disposition"])
        mission_names[version] = row["mission"]

    status_rows = "".join(
        f"<tr><th scope='row'><span class='swatch' style='--swatch:{COLORS[key]}'></span>{esc(LABELS[key])}</th><td>{counts[key]}</td><td>{counts[key] / 80:.1%}</td></tr>"
        for key in ("completed", "represented", "open_gap", "exact_gate")
    )
    segments = "".join(
        f"<div class='segment {key}' style='width:{counts[key] / 80 * 100:.4f}%' aria-hidden='true'></div>"
        for key in ("completed", "represented", "open_gap", "exact_gate")
    )
    matrix_rows = []
    for version in range(641, 651):
        cells = "".join(
            f"<td><span class='status-token {esc(status)}'>{esc(status.replace('_', ' '))}</span></td>"
            for status in matrix[version]
        )
        matrix_rows.append(f"<tr><th scope='row'>v{version}<small>{esc(mission_names[version])}</small></th>{cells}</tr>")

    board_rows = "".join(
        "<tr>"
        f"<th scope='row'>{esc(row['claim_id'])}<small>{esc(row['claim'])}</small></th>"
        f"<td><strong>{esc(row['grade'])}</strong></td>"
        f"<td>{esc(row['state'].replace('_', ' '))}</td>"
        f"<td>{esc(row['evidence'])}</td>"
        f"<td>{esc(row['review_date'])}</td>"
        "</tr>"
        for row in board["claims"]
    )
    source_items = "".join(
        f"<li><a href='{esc(row['url'])}'>{esc(row['title'])}</a> — {esc(row['authority'])}; role: {esc(row['evidence_role'].replace('_', ' '))}.</li>"
        for row in sources["sources"]
    )
    adapter_rows = "".join(
        f"<tr><th scope='row'>{esc(row['dataset_id'])}</th><td>{esc(row['baseline'])}</td><td>{esc(row['status'].replace('_', ' '))}</td></tr>"
        for row in empirical["adapters"]
    )

    return f"""<!doctype html>
<html lang="en-NZ">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Eiren v641-v1 integrated evidence board</title>
  <style>
    :root{{--ink:#17303b;--muted:#58707a;--paper:#fbfcfa;--panel:#eef3f1;--rule:#c8d3d0;--focus:#176b74;}}
    *{{box-sizing:border-box}} body{{margin:0;background:#e9efed;color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}}
    main{{max-width:1120px;margin:auto;background:var(--paper);padding:clamp(22px,5vw,70px)}}
    h1{{font-size:clamp(2rem,5vw,4.4rem);line-height:1.02;max-width:900px;margin:.15em 0}} h2{{margin-top:2.5em;border-top:2px solid var(--ink);padding-top:.55em}}
    h3{{margin-top:1.6em}} p{{max-width:78ch}} .kicker{{text-transform:uppercase;letter-spacing:.12em;font-weight:750;color:var(--focus)}}
    .lede{{font-size:1.18rem;max-width:78ch}} .boundary{{border-left:7px solid #a1452d;background:#f8eee9;padding:16px 20px;margin:28px 0;max-width:86ch}}
    .metrics{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:26px 0}} .metric{{border-top:5px solid var(--c);background:var(--panel);padding:16px}}
    .metric strong{{display:block;font-size:2.1rem;line-height:1}} .metric span{{font-size:.86rem;color:var(--muted)}}
    figure{{margin:30px 0}} figcaption{{margin-top:10px;color:var(--muted);max-width:80ch}} .bar{{display:flex;height:52px;border:2px solid var(--ink);overflow:hidden;background:white}}
    .segment{{min-width:2px;border-right:2px solid white}} .completed{{background:{COLORS['completed']}}}.represented{{background:{COLORS['represented']}}}.open_gap{{background:{COLORS['open_gap']}}}.exact_gate{{background:{COLORS['exact_gate']}}}
    .table-wrap{{overflow-x:auto;border:1px solid var(--rule)}} table{{border-collapse:collapse;width:100%;background:white}} th,td{{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--rule)}} th{{font-weight:720}} th small{{display:block;font-weight:450;color:var(--muted);min-width:14rem}}
    .swatch{{display:inline-block;width:.8em;height:.8em;margin-right:.5em;background:var(--swatch);border:1px solid var(--ink)}} .status-token{{display:inline-block;min-width:7.5rem;padding:4px 7px;color:white;border:1px solid #1d2b31;font-weight:700;font-size:.76rem}}
    .note{{background:var(--panel);padding:16px 20px;margin:18px 0}} a{{color:#075f78;text-underline-offset:2px}} code{{background:#e8efec;padding:.12em .3em}}
    ol.sources{{columns:2;column-gap:2rem;padding-left:1.2rem}} ol.sources li{{break-inside:avoid;margin-bottom:.75rem}}
    footer{{border-top:2px solid var(--ink);margin-top:55px;padding-top:18px;color:var(--muted)}}
    @media(max-width:760px){{.metrics{{grid-template-columns:1fr 1fr}}ol.sources{{columns:1}}main{{padding:22px 16px}}.bar{{height:38px}}}}
    @media(max-width:430px){{.metrics{{grid-template-columns:1fr}}}}
    @media print{{@page{{size:A4;margin:14mm}}body{{background:white;font-size:10.5pt}}main{{padding:0;max-width:none}}a{{color:inherit;text-decoration:none}}h2,h3{{break-after:avoid-page}}thead{{display:table-header-group}}tr{{break-inside:avoid}}.metrics{{grid-template-columns:repeat(4,1fr)}}.table-wrap{{overflow:visible}}table{{font-size:8pt}}th,td{{padding:5px 6px}}.mission-matrix{{table-layout:fixed;font-size:6.3pt}}.mission-matrix th:first-child{{width:20%}}.mission-matrix th small{{min-width:0}}.mission-matrix th,.mission-matrix td{{padding:3px 2px}}.mission-matrix .status-token{{display:block;min-width:0;padding:2px;font-size:6.1pt;line-height:1.15;white-space:normal}}ol.sources{{columns:2}}}}
  </style>
</head>
<body>
<main>
  <header>
    <div class="kicker">GHC Family · Eiren Kestrel · v641-v1 · 12 July 2026</div>
    <h1>Eighty work units processed; evidence gaps preserved</h1>
    <p class="lede">The ten v641-v650 missions and eight functional phases were compressed into one Eiren-owned x1/x2 pilot. Every cell received a preregistration and an outcome receipt. Local completion is substantial; empirical, external, legal, cultural, and task-route gaps remain visible.</p>
    <div class="boundary"><strong>Claim boundary.</strong> This report does not establish a Theory of Everything, AGI/ASI, machine consciousness, a deployed identity system, enacted law, or a guaranteed Stage 20 future.</div>
  </header>

  <section aria-labelledby="outcome-title">
    <h2 id="outcome-title">1. The outcome is not eighty green boxes</h2>
    <div class="metrics">
      <div class="metric" style="--c:{COLORS['completed']}"><strong>{counts['completed']}</strong><span>completed locally</span></div>
      <div class="metric" style="--c:{COLORS['represented']}"><strong>{counts['represented']}</strong><span>represented / proxy</span></div>
      <div class="metric" style="--c:{COLORS['open_gap']}"><strong>{counts['open_gap']}</strong><span>open evidence gaps</span></div>
      <div class="metric" style="--c:{COLORS['exact_gate']}"><strong>{counts['exact_gate']}</strong><span>exact authority gates</span></div>
    </div>
    <figure aria-describedby="bar-description">
      <div class="bar">{segments}</div>
      <figcaption id="bar-description">Disposition of all 80 work units: {counts['completed']} completed, {counts['represented']} represented, {counts['open_gap']} open gaps, and {counts['exact_gate']} exact gates. Segment area is proportional to count; the table supplies exact values without relying on color.</figcaption>
    </figure>
    <div class="table-wrap"><table><caption class="sr-only">Exact work-unit dispositions</caption><thead><tr><th>Disposition</th><th>Count</th><th>Share</th></tr></thead><tbody>{status_rows}</tbody></table></div>
  </section>

  <section aria-labelledby="matrix-title">
    <h2 id="matrix-title">2. Ten missions retain all eight functional phases</h2>
    <p>The matrix preserves the original proposal's intellectual coverage without pretending that ten versions or five owners actually ran. Each cell resolves to the canonical JSON ledger.</p>
    <div class="table-wrap"><table class="mission-matrix"><thead><tr><th>Mission</th><th>v1 scope</th><th>v2 sources</th><th>v3 model</th><th>v4 critique</th><th>v5 build</th><th>v6 test</th><th>v7 Heart</th><th>v8 replicate</th></tr></thead><tbody>{''.join(matrix_rows)}</tbody></table></div>
  </section>

  <section aria-labelledby="mind-title">
    <h2 id="mind-title">3. Mind: a falsifiable physical seed, not a final theory</h2>
    <p>The canonical Mandala equation defines <em>Omega</em> as the effective stress-energy of a specified scalar/EFT extension sector. The local kernel now checks scalar identities, exchange cancellation, Friedmann residuals, a minimal stability gate, and RK4 self-convergence. These are internal rejection tools, not empirical confirmation.</p>
    <div class="note"><strong>Equation boundary:</strong> ethical, informational, spiritual, and metaphorical terms remain in typed registers unless an explicit physical map supplies variables, dimensions, action, observables, uncertainty, and falsifiers.</div>
    <h3>Empirical adapters</h3>
    <div class="table-wrap"><table><thead><tr><th>Adapter</th><th>Baseline first</th><th>Current state</th></tr></thead><tbody>{adapter_rows}</tbody></table></div>
    <p>No dataset was downloaded and no likelihood was run. The six adapters passed metadata validation only.</p>
  </section>

  <section aria-labelledby="body-title">
    <h2 id="body-title">4. Body: THOS now has a matched-budget test</h2>
    <p>The protocol fixes one-agent, historical four-sibling, and new five-sibling arms across coding, source synthesis, contradiction detection, privacy, and recovery. It measures success, Brier calibration, uniqueness, cost, latency, handoff loss, privacy incidents, and recovery.</p>
    <div class="note"><strong>Calibration result:</strong> the scorer processed {thos['task_count']} synthetic fixtures. Its {thos['success_rate']:.0%} fixture success rate validates arithmetic only; the report is explicitly labelled <code>{esc(thos['interpretation_boundary'])}</code>.</div>
  </section>

  <section aria-labelledby="heart-title">
    <h2 id="heart-title">5. Heart: structural safeguards before status claims</h2>
    <p>Freed ID's minimum profile uses W3C identity roles, controller-holder separation, status, recovery, delegation, selective disclosure, export, deletion/tombstone, and appeal. All {freed['vector_count']} synthetic conformance vectors matched; the invalid consciousness and legal-personhood claims were rejected.</p>
    <p>The Cosmic Bill of Rights is a model charter, not law. Its human-rights, Indigenous-rights, AI-governance, privacy, and data-governance crosswalk requires affected authority and legitimate process. Māori concepts remain under Māori authority.</p>
  </section>

  <section aria-labelledby="stage-title">
    <h2 id="stage-title">6. Stage 20 is an evidence ladder, not a prediction</h2>
    <div class="table-wrap"><table><thead><tr><th>Claim</th><th>Grade</th><th>State</th><th>Evidence</th><th>Review</th></tr></thead><tbody>{board_rows}</tbody></table></div>
    <p>No unique GMUT claim is graded E4. One-, five-, thirty-, hundred-, and thousand-year horizons are conditional scenarios with explicit non-prediction labels.</p>
  </section>

  <section aria-labelledby="source-title">
    <h2 id="source-title">7. Primary and authoritative source ledger</h2>
    <ol class="sources">{source_items}</ol>
    <p>Sources are grouped by authority. Repetition from one root does not create independent support, and none of these sources endorses the GHC programme.</p>
  </section>

  <section aria-labelledby="route-title">
    <h2 id="route-title">8. Route truth after v1</h2>
    <p>Aevren, Mira Vale, Mira Rowan, and Maren Quill remain on standby. No new sibling is pre-named or represented as active. The first new user-owned Codex task may be created only after this branch is clean, pushed, and remote-aligned; the new sibling chooses their own name, role, hope, and optional gender.</p>
  </section>

  <footer>Generated from portable JSON artifacts. Regenerate with <code>scripts/build_ghc_family_v641_evidence_report.py</code>. Essential values remain visible without hover, JavaScript, animation, or color alone.</footer>
</main>
</body>
</html>
"""


def update_parent(parent: Path, relative_report: str) -> None:
    marker_start = "<!-- GHC_V641_INTEGRATED_START -->"
    marker_end = "<!-- GHC_V641_INTEGRATED_END -->"
    block = f"""{marker_start}
<aside id="v641-integrated-pilot" style="margin:2rem auto;max-width:980px;padding:1.25rem;border:2px solid #176b74;background:#eef3f1;color:#17303b;font-family:system-ui,sans-serif">
  <strong>New: Eiren v641-v1 integrated 80-work-unit pilot.</strong>
  <p>See the evidence board for the 67 completed, 6 represented, 5 open-gap, and 2 exact-gated outcomes.</p>
  <a href="{html.escape(relative_report)}">Open the accessible v641 evidence board</a>
</aside>
{marker_end}"""
    text = parent.read_text(encoding="utf-8")
    text = re.sub(re.escape(marker_start) + r".*?" + re.escape(marker_end), "", text, flags=re.DOTALL)
    if "</body>" not in text:
        raise ValueError("parent report has no closing body tag")
    parent.write_text(text.replace("</body>", block + "\n</body>", 1), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--update-parent", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build_report(args.phase_dir), encoding="utf-8")
    if args.update_parent:
        relative = Path("..") / "v641-v1" / "deliverables" / args.output.name
        update_parent(args.update_parent, relative.as_posix())
    print(json.dumps({"output": str(args.output), "parent_updated": bool(args.update_parent)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Render a local THOS reason dashboard HTML artifact from a renderer preflight."""

from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def read_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: JSON payload must be an object")
    return payload


def badge_class(status: object) -> str:
    if status == "FAIL_BLOCKER":
        return "blocked"
    if status == "OPEN_GAP":
        return "open"
    if status == "NOT_RUN":
        return "idle"
    return "clean"


def esc(value: object) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def render_rows(rows: list[dict[str, Any]]) -> str:
    body = []
    for row in rows:
        status = row.get("row_status")
        body.append(
            "          <tr data-case-id=\"{case_id}\">\n"
            "            <th scope=\"row\">{case_id}</th>\n"
            "            <td><span class=\"badge {row_class}\">{row_status}</span></td>\n"
            "            <td>{guard_status}</td>\n"
            "            <td>{guard_decision}</td>\n"
            "            <td>{dominant_reason}</td>\n"
            "            <td>{reason_code_count}</td>\n"
            "            <td>{matched_required_count}</td>\n"
            "            <td>{missing_required_count}</td>\n"
            "            <td>{allowed_extra_count}</td>\n"
            "            <td>{unexpected_extra_count}</td>\n"
            "          </tr>"
            .format(
                allowed_extra_count=esc(row.get("allowed_extra_count")),
                case_id=esc(row.get("case_id")),
                dominant_reason=esc(row.get("dominant_reason")),
                guard_decision=esc(row.get("guard_decision")),
                guard_status=esc(row.get("guard_status")),
                matched_required_count=esc(row.get("matched_required_count")),
                missing_required_count=esc(row.get("missing_required_count")),
                reason_code_count=esc(row.get("reason_code_count")),
                row_class=badge_class(status),
                row_status=esc(status),
                unexpected_extra_count=esc(row.get("unexpected_extra_count")),
            )
        )
    return "\n".join(body)


def render_dashboard(preflight: dict[str, Any], phase_slug: str) -> str:
    rows = preflight.get("renderer_rows")
    if not isinstance(rows, list):
        rows = []
    clean_rows = [row for row in rows if isinstance(row, dict)]
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    serialized = html.escape(json.dumps(clean_rows, sort_keys=True), quote=False)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>THOS Reason Dashboard Render - {esc(phase_slug)}</title>
    <style>
      :root {{
        --ink: #1b1f24;
        --paper: #f8f5ee;
        --panel: #fffdf8;
        --line: #d8cfbf;
        --clean: #116b4f;
        --blocked: #9b2c2c;
        --open: #856404;
        --idle: #56616d;
      }}
      body {{
        background: var(--paper);
        color: var(--ink);
        font-family: Georgia, "Times New Roman", serif;
        margin: 0;
      }}
      main {{
        margin: 0 auto;
        max-width: 1180px;
        padding: 32px 18px 48px;
      }}
      header, section {{
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 18px;
        box-shadow: 0 16px 40px rgba(36, 31, 23, 0.08);
        margin-bottom: 18px;
        padding: 22px;
      }}
      h1 {{
        font-size: clamp(2rem, 5vw, 3.8rem);
        line-height: 0.95;
        margin: 0 0 10px;
      }}
      .lede {{
        font-size: 1.08rem;
        margin: 0;
        max-width: 820px;
      }}
      .metrics {{
        display: grid;
        gap: 12px;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      }}
      .metric {{
        border-left: 5px solid var(--clean);
        padding: 10px 12px;
      }}
      .metric strong {{
        display: block;
        font-size: 1.55rem;
      }}
      .table-wrap {{
        overflow-x: auto;
      }}
      table {{
        border-collapse: collapse;
        min-width: 980px;
        width: 100%;
      }}
      caption {{
        font-weight: 700;
        padding: 0 0 12px;
        text-align: left;
      }}
      th, td {{
        border-bottom: 1px solid var(--line);
        padding: 10px 9px;
        text-align: left;
        vertical-align: top;
      }}
      thead th {{
        background: #efe7d7;
        position: sticky;
        top: 0;
      }}
      .badge {{
        border-radius: 999px;
        color: white;
        display: inline-block;
        font: 700 0.78rem/1.1 Verdana, sans-serif;
        letter-spacing: 0.02em;
        padding: 6px 9px;
      }}
      .badge.clean {{ background: var(--clean); }}
      .badge.blocked {{ background: var(--blocked); }}
      .badge.open {{ background: var(--open); color: #1b1f24; }}
      .badge.idle {{ background: var(--idle); }}
      .note {{
        font-size: 0.96rem;
        margin-top: 12px;
      }}
    </style>
  </head>
  <body>
    <main data-phase-slug="{esc(phase_slug)}" data-case-count="{len(clean_rows)}">
      <header>
        <p class="note">Local non-mutating renderer</p>
        <h1>THOS Reason Dashboard</h1>
        <p class="lede">Renderer preflight output for {esc(phase_slug)}. This artifact shows guard decisions, dominant reason counts, and required-code parity from the compact THOS fixture. All six GMUT gates remain open.</p>
      </header>
      <section aria-label="Dashboard summary">
        <div class="metrics">
          <div class="metric"><span>Fixture status</span><strong>{esc(preflight.get("fixture_status"))}</strong></div>
          <div class="metric"><span>Fixture assertion status</span><strong>{esc(preflight.get("fixture_assertion_status"))}</strong></div>
          <div class="metric"><span>Case count</span><strong>{len(clean_rows)}</strong></div>
          <div class="metric"><span>Renderer migration</span><strong>{esc(preflight.get("renderer_migration_status"))}</strong></div>
        </div>
      </section>
      <section aria-label="Reason dashboard rows">
        <div class="table-wrap">
          <table>
            <caption>Reason-code guard rows</caption>
            <thead>
              <tr>
                <th scope="col">Case ID</th>
                <th scope="col">Row Status</th>
                <th scope="col">Guard Status</th>
                <th scope="col">Guard Decision</th>
                <th scope="col">Dominant Reason</th>
                <th scope="col">Reason Codes</th>
                <th scope="col">Required Codes</th>
                <th scope="col">Missing Required</th>
                <th scope="col">Allowed Extras</th>
                <th scope="col">Unexpected Extras</th>
              </tr>
            </thead>
            <tbody>
{render_rows(clean_rows)}
            </tbody>
          </table>
        </div>
        <p class="note">Generated at {esc(generated_at)}. No connector write, cloud write, destructive cleanup, publication authority change, or GMUT gate movement is represented by this local artifact.</p>
      </section>
      <script type="application/json" id="thos-render-data">{serialized}</script>
    </main>
  </body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a static THOS reason dashboard artifact.")
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--phase-slug", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    preflight = read_json_object(Path(args.preflight))
    if preflight.get("aggregate_status") != "PASS_SHAPE_ONLY":
        raise ValueError("preflight aggregate_status must be PASS_SHAPE_ONLY before rendering")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_dashboard(preflight, args.phase_slug), encoding="utf-8")
    print(output.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

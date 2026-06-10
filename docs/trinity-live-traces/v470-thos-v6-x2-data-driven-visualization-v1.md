# v470 THOS v6 x2 Data-Driven Visualization

This local HTML view replaces the v6 x1 static prototype with a data-driven report surface. The page embeds the supervisor and regression rows as local JSON-like data, renders counts from those rows, and keeps essential values visible without hover.

## Analytical Job

- Artifact family: local operational guardrail report.
- Primary route: simple browser-native HTML, CSS, and JavaScript.
- Fallback route: read the companion JSON/Markdown artifacts directly.

## Reading Path

1. Summary cards show supervisor rows, regression rows, and exception rows.
2. A stacked status bar encodes pass-shape, open-gap, and fail-blocker counts.
3. Supervisor and regression tables expose row-level detail.
4. Boundary lock repeats that no mutation, connector write, or GMUT gate closure occurred.

## Accessibility And Safety

- No external scripts, fonts, network calls, or connector writes.
- Mobile layout collapses cards into a single column.
- Color is paired with text labels.
- The page explicitly states that it is THOS infrastructure evidence only, not GMUT validation.

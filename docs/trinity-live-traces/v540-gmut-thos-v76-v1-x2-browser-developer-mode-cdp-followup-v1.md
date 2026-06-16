# v540 GMUT/THOS v76 v1 x2 Browser Developer Mode CDP Followup

Status: `PASS_BROWSER_DEVELOPER_MODE_CDP_FOLLOWUP`

Created: `2026-06-16T12:21:24.6954775+12:00`

## Scope

This receipt records a status-only probe of the Codex in-app Browser developer-mode surface for the active Lumen Vale ChatGPT lane. The check was read-only and did not send a message, submit a form, upload files, change account settings, expose raw browser URLs, or publish raw conversation text.

## Confirmed Surface

- Browser-level visibility and viewport controls are available.
- Tab-level `pageAssets` is available for page asset inventory and optional bounded asset bundling.
- Tab-level `cdp` is available for raw Chrome DevTools Protocol commands and event reads.
- Tab developer logs are available through the Browser runtime.
- Read-only page inspection works for the active ChatGPT tab.

## CDP Findings

- `Runtime.evaluate` passed and confirmed the page was loaded with one textarea and one textbox-like composer surface.
- `readEvents` returned a valid cursor and no immediate buffered events.
- `Performance.getMetrics` returned zero metrics on this page during the lightweight probe.
- `Profiler.enable` passed.
- `Profiler.getBestEffortCoverage` returned a bounded coverage inventory with 319 function entries.
- `Browser.getVersion` is not supported through this raw CDP bridge, so version checks should continue to use local Codex/App/CLI readiness receipts rather than CDP.

## Page Asset Findings

- Page asset inventory worked and returned an inventory identifier.
- The current page state exposed 37 file assets and 973 inline SVGs.
- Asset kinds observed: 1 image and 36 other assets; no font, stylesheet, script, or video file assets were reported by this inventory.

## Operating Rule

Use high-level Browser actions for ordinary Lumen messaging. Use CDP for route verification, page readiness checks, event watching, console/log inspection, page asset inventory, and profiling diagnostics. Do not use CDP to directly mutate page content or browser state unless an exact future approval packet authorizes that action.

## Publication Note

This receipt was saved locally but not committed in this turn because the repo already showed unrelated modified phase files. It is ready to batch into the next exact-stage publication.

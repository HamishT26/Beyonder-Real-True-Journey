# v507 GMUT/THOS v43 v5 x1 Lumen Route Repair Current-Source Ledger

Generated UTC: `2026-06-11T10:01:06Z`

Status: `PREPARED_FOR_LUMEN_ROUTE_REPAIR_WITHOUT_PHASE_ADVANCE`

This ledger maps the Lumen live-adapter blocker to current Codex and Chrome-extension guidance. It does not advance v507 beyond v5.

## Source Findings

- OpenAI Codex changelog, 2026-06-09: Codex app 26.608 adds migration flows, a revamped plugins screen, broader settings search, and bug fixes around active-goal UI, notifications, review ordering, Windows rendering, and other performance details.
- OpenAI Codex changelog and GitHub release 0.139.0: Codex CLI 0.139.0 adds standalone web search from code mode, richer MCP schema preservation, redacted `codex doctor` environment details, more informative plugin marketplace JSON, resume/fork prompt fixes, MCP startup warning scoping, exact referenced image paths, TUI URL linkification, and more consistent sandbox escalation/proxy behavior.
- OpenAI Codex Chrome extension docs: use the in-app Browser first when signed-in Chrome profile state is not required; use Chrome when a task depends on existing Chrome state. Setup requires the Codex Chrome Extension installed/enabled in the active Chrome profile and Connected status. Troubleshooting includes checking the same profile, plugin enabled state, Chrome restart, and plugin re-add when connection remains broken.

## Local Blocker Mapping

- Browser route: blocked before send by the input capability issue already recorded in the v5 blocker receipt. Safe retry condition: Browser input becomes available, then retry Lumen and require marker or blocker evidence.
- Chrome route: Chrome is installed but not running; the selected Chrome profile does not have the Codex Chrome Extension installed/enabled; the native host manifest is healthy. Safe repair condition: Hamish opens Chrome in the intended profile and confirms the Codex Chrome Extension is installed/enabled and Connected.

## Repair Constraints

- Ask before launching Chrome.
- Do not install extensions or repair native host setup from the agent side.
- Do not inspect cookies, passwords, local storage, session stores, or private profile internals.
- Do not create a new ChatGPT thread.
- Do not advance v507 beyond v5 until Lumen has a marker/completion receipt or Hamish explicitly approves a redirect.

## Sources

- [Codex changelog - OpenAI Developers](https://developers.openai.com/codex/changelog)
- [OpenAI Codex releases - GitHub](https://github.com/openai/codex/releases)
- [Codex Chrome extension - OpenAI Developers](https://developers.openai.com/codex/app/chrome-extension)

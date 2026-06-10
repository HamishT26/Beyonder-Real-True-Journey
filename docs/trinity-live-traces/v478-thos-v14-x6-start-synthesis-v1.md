# v478 THOS v14 x6 Start Synthesis

- generated_nz: `2026-06-05T10:34:26+12:00`
- overall_status: `PASS_X6_START_WITH_OVER_WINDOW_CLI_COMPLETION`
- claim boundary: v478 THOS v14 x6 start synthesis and handoff only; all GMUT gates remain open; no canon promotion; lane body text and raw output stay unpublished.

## Evidence

- App lanes: `PASS` in `v478-thos-v14-x6-start-background-council-app-completion-v1.json`.
- Cicero completed in `232.156` seconds.
- Kierkegaard completed in `96.75` seconds.
- Aristotle completed in `105.734` seconds.
- CLI lanes: final-message files arrived after the 30-minute observation window.
- Arby completed in `2205.164` seconds with `3678` final-message bytes and hash `4cc56de01213009f9593b92ea898023fe855c34f73d650afd33d92d2857ce319`.
- Arby marker review: `PASS_FALSE_POSITIVE_TOKEN_WORD_REVIEW`.
- Aster Vale completed in `2136.519` seconds with `3592` final-message bytes and hash `afd5f8e7522cb6a3eec4f1d08663febdd598da161dff4b475408b894b89de8a9`.
- Timing receipt: observation run `4`, average `955.265` seconds, interpreted as post-baseline over-window completion.
- Soft wait baseline remains `312.832` seconds from the first three complete observations.
- Multiplex board: `ALL_LANES_READY`.
- Stale-flow refresh: `READY_NO_STALE_FLOWS`.
- Command/handoff compatibility note: command index remains `PASS_WITH_OPEN_GAP`; v54/v55 handoff remains `PASS`.

## Lessons

- The five-lane roster was attempted at x6 start through existing lanes only.
- App-server lanes completed cleanly inside the expected route.
- CLI lanes completed formally, but after the 30-minute observation window.
- Arby's marker review was a plain token-word false positive, not credential evidence.
- The 312.832 second baseline remains a useful check-in foothold, not a hard timeout or completion substitute.
- Wait time was used for source refresh, command/handoff compatibility, stale-flow refresh, roadmap prep, and marker-review receipts rather than idle polling.

## x6 Closeout Handoff

- For the next CLI roster, prefer the proven retry2/direct-advisory pattern to reduce stale TUI waiting.
- Keep Arby and Aster Vale on the roster because both ultimately produced valid final-message files.
- Keep every-second-session five-lane discipline active, but record over-window completion separately from in-window completion.
- If CLI final-message files again arrive after timeout, publish both the timeout evidence and any later final-marker resolution so the story remains evidence-led.
- Carry x6 official-source notes into runner hardening, skill-governance, and command-surface compatibility work.

# v471 THOS v1 x2 Codex CLI Launcher Shim

The x2 fix is a reusable launcher script: `scripts/thos_codex_cli_advisory_launcher.py`.

It chooses the app-bundled Codex executable, uses `exec -s read-only -C <worktree> -o <last-message> <prompt>`, blocks the old invalid `-a` pattern, defaults to dry-run planning, and never adds `--ephemeral`.

The first launcher retry exposed deeper skill-load blockers rather than final advisory text. The two v471 retry processes were stopped after the stderr flood was confirmed. Raw temp stdout/stderr files are not staged; curated artifacts keep only summarized blocker state.

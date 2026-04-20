# V44 Journey Advisory Digest

- Generated UTC: `2026-04-20T04:12:13+00:00`
- Actual current head: `75af4c29d352548b0eb05be0c27dee3952512436`

## Official Product Names

- `suite_name`: `Vertex AI Agent Builder`
- `former_product_name`: `AI Applications`
- `search_lane`: `Vertex AI Search`
- `agent_runtime_lane`: `Agent Engine`

## Source Files

- `C:\Users\hamis\Downloads\Grand OpenAI and Codex app update (Nz 17th of April 2026) (1).txt`: present=`True`, line_count=`2201`, focus_lines=`56`
- `C:\Users\hamis\Downloads\Beyonder-Real-True Journey v40 (Aletheon - Orun - Gemini - Vesper Ion - Kai) (8).txt`: present=`True`, line_count=`2323`, focus_lines=`18`

## Repo Truth

- `actual_current_head_sha`: `75af4c29d352548b0eb05be0c27dee3952512436`
- `published_runtime_head_sha`: `7b561c62e6271acedc96322bedd382564d8d7ab9`
- `published_validation_head_sha`: `7b561c62e6271acedc96322bedd382564d8d7ab9`
- `worktree_baseline_state`: `origin_75af4c29`
- `worktree_baseline_sha`: `75af4c29d352548b0eb05be0c27dee3952512436`
- `existing_google_drive_state`: `operator_hold`
- `existing_git_publication_state`: `committed_pushed_pr_updated`
- `existing_active_handoff_pack_path`: `docs/v43-omega-continuity-pack-v1.md`
- `existing_next_receiver_pack_path`: `docs/v44-beta-continuity-pack-v1.md`

## Executable Decisions

- Keep Windows Native / PowerShell as the primary V44 operator lane and publish WSL as installed plus intentionally on hold for app-side switching.
- Keep C:\Users\hamis\workspace\Beyonder-Real-True-Journey as the authoritative repo root and treat the stale local main worktree as non-execution history.
- Use D:\GHC-Archives\downloads, D:\GHC-Archives\artifacts, and D:\GHC-Archives\worktrees for bulky non-authoritative outputs instead of globally redirecting Windows Downloads.
- Treat the claimed $1700+ NZD GenAI credit as operator-claimed until the Billing console and eligible SKUs confirm the actual remaining promo credit.
- Use current Google product names in V44 outputs: Vertex AI Agent Builder, AI Applications, Vertex AI Search, and Agent Engine.
- Hard-gate slot 40 and do not create a new continuity-bearing member unless Codex CLI access, identity continuity, memory continuity, and target model resolution all pass.

## Parsed Focus Lines

- `with built-in worktree support, automations, and Git functionality.`
- `Automations run in dedicated background worktrees for Git repositories, and directly in the project directory for non-version-controlled projects.`
- `On Windows, Codex can run natively in PowerShell with a native Windows sandbox`
- `instead of requiring WSL or a virtual machine. This lets you stay in`
- `Automations can also attach to a single thread. These thread automations are`
- `loop. Use them for heartbeat-style automations that should keep returning to the`
- `Use a thread automation when the next run depends on the current conversation.`
- `It runs natively on Windows using PowerShell and the`
- `runs commands in PowerShell. The app can still work with projects that live in`
- `your Windows filesystem and accessing them from WSL through`
- `directly from the WSL filesystem.`
- `terminal options. You can keep the agent in WSL and still use PowerShell in the`
- `terminal, or use WSL for both, depending on your workflow.`
- `Codex works best when a few common developer tools are already installed:`
- `This can also happen if Codex creates PowerShell scripts for you. In that case,`
- `you may need a less restrictive execution policy before PowerShell will run`
- `Local setup scripts run in the agent environment: WSL if the agent uses WSL,`
- `and PowerShell otherwise.`
- `If you also run the Codex CLI inside WSL, the CLI uses the Linux home`
- `If you want that setting in every shell, add it to your WSL shell profile, such`
- `accessible from WSL, the most reliable workaround is to store the project`
- `Automations`
- `For project-scoped automations, the app needs to be running, and the selected`
- `In Git repositories, you can choose whether an automation runs in your local`
- `background. Worktrees keep automation changes separate from unfinished local`
- `working on. In non-version-controlled projects, automations run directly in the`
- `choose them explicitly if you want more control over how the automation runs.`
- `Find all automations and their runs in the automations pane inside your Codex app sidebar.`
- `Standalone automations start fresh runs on a schedule and report results in`
- `Triage. Use them when each run should be independent or when one automation`

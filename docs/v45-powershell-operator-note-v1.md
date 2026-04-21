# V45 PowerShell Operator Note

- Stay in PowerShell for the active Codex app lane. Keep WSL installed and callable, but do not switch the app execution lane there while the selector issue remains on hold.
- Use `D:\GHC-Archives\downloads\v45-omega` for bulky manual downloads tied to v45 and `D:\GHC-Archives\artifacts\v45-omega` for bulky generated artifacts.
- Use the clean D: worktree for execution and publication. Treat the dirty C: checkout as authoritative history, not as the active mutation lane.
- Treat `codex mcp list` as the CLI truth and the current app plugin set as the app truth. Do not assume the CLI inherits every app plugin.
- Proven command anchors:
  - `codex --version`
  - `codex login status`
  - `codex mcp list`
  - `codex features list`
  - `wsl.exe --status`
  - `gcloud auth list`
  - `gcloud config list`

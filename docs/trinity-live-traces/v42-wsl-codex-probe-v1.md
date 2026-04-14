# V42 WSL Codex Probe

- Generated UTC: `2026-04-14T15:05:02+00:00`
- Overall status: `WARN`
- WSL health state: `ubuntu_repo_ready`
- WSL Codex selector state: `cli_wsl_entrypoint_verified_app_selector_unresolved`
- Codex CLI WSL state: `cli_binary_launch_verified`
- Manual operator checkpoint required: `True`

## Probe Results

- `wsl_inventory_returncode`: `0`
- `bash_path`: `/usr/bin/bash`
- `python3_path`: `/usr/bin/python3`
- `git_path`: `/usr/bin/git`
- `node_path`: `/usr/bin/node`
- `npx_path`: `/mnt/c/Program Files/nodejs/npx`
- `repo_head_from_wsl`: `87f2e42dda`
- `codex_version`: `codex-cli 0.119.0-alpha.28`
- `codex_exec_help_ok`: `True`
- `config_selector_keywords_found`: `False`
- `codex_exe_present`: `True`
- `windows_python_present`: `True`

## Blockers

- The Codex desktop WSL selector is not discoverable from repo or global config; the remaining binding proof is app-side.

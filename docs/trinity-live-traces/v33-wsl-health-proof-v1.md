# V33 WSL Health Proof

- Generated UTC: `2026-04-05T13:27:37+00:00`
- Overall status: `WARN`
- Proof state: `windows_fallback_primary`
- WSL health state: `windows_fallback_primary`
- Preferred operator lane: `windows_powershell_rest_kubectl`
- Authoritative repo: `C:\Users\hamis\workspace\Beyonder-Real-True-Journey`

## Probe Results

- `wsl_status`: `pass`
- `wsl_inventory`: `pass`
- `ubuntu_launch`: `timed_out`
- `repo_mount_visibility`: `timed_out`
- `path_probe`: `pass`
- `python3_probe`: `pass`
- `git_probe`: `pass`
- `repo_git_status_probe`: `timed_out`

## Blockers

- Ubuntu did not launch cleanly from PowerShell.
- The authoritative repo mount is not readable from Ubuntu.

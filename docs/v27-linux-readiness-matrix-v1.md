# V27 Linux Readiness Matrix

- overall_status: `WARN`
- current_shell: `powershell`
- readiness_state: `ubuntu_probe_blocked`
- docker_runtime_role: `fallback_only`

## Probe Results
- ubuntu_launch_noninteractive: `pass`
- repo_mount_visibility: `pass`
- node_probe: `pass`
- npm_probe: `pass`
- python3_probe: `pass`
- git_probe: `pass`
- repo_git_status_probe: `timed_out`
- tempfile_smoke_probe: `pass`
- docker_probe: `fallback_only_not_required`
- kubectl_probe: `fallback_only_not_required`

## Blocking Gaps
- Bounded git status timed out against the OneDrive-mounted repo inside Ubuntu.


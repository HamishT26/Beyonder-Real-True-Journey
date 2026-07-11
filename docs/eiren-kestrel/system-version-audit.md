# System version audit — 11 July 2026

## Outcome

The requested current-version check was completed without modifying the Codex desktop app. Safe same-track runtime updates were installed and verified from their real executable paths.

| Component | Before | After | Result |
|---|---:|---:|---|
| Codex CLI | `0.142.5` | `0.144.1` | updated and command-verified |
| Codex desktop app | `26.707.3748.0` | `26.707.3748.0` | deliberately unchanged |
| ChatGPT desktop app | `1.2026.190.0` | `1.2026.190.0` | inventoried only |
| Node.js LTS | `24.15.0` | `24.18.0` | updated with Windows Package Manager |
| npm | `11.15.0` | `12.0.1` | updated after engine compatibility check |
| Git for Windows | `2.53.0.windows.1` | `2.55.0.windows.2` | updated with Windows Package Manager |
| Python | `3.12.10` | `3.12.10` | retained; last 3.12 Windows binary release |
| PowerShell 7 | absent | absent | optional gap; Windows PowerShell remains available |

The Node release is documented by the [Node.js 24.18.0 LTS release](https://nodejs.org/en/blog/release/v24.18.0). The installed npm version is recorded by the [npm 12.0.1 registry entry](https://www.npmjs.com/package/npm/v/12.0.1). The Git installer is the signed [Git for Windows 2.55.0.2 release](https://github.com/git-for-windows/git/releases/tag/v2.55.0.windows.2). Python's release record explains that [3.12.10 was the last 3.12 release with binary installers](https://www.python.org/downloads/release/python-31213/); later 3.12 security releases are source-only.

## Storage posture

- `C:` free after updates: approximately `22.07 GiB`.
- `D:` free after artifact construction: approximately `602.41 GiB`.
- Research source, build, and deliverable work stayed in the D-drive Eiren worktree.
- C-drive writes were limited to essential installed tool updates and their normal package metadata.

## Boundary

A blanket upgrade of every application, driver, package, and operating-system component was not attempted. That would be an unbounded maintenance mutation with no single rollback plan. This audit covered the toolchain actually used by the phase and retained major-version migrations—especially Python 3.12 to 3.14—as separately testable work.

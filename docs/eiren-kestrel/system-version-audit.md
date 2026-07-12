# System version audit — 12 July 2026

## Outcome

The phase-start version check was refreshed against the executable paths used by this worktree. No update was needed, and the Codex desktop app was deliberately left unchanged.

| Component | Verified local version | Current-track assessment | Action |
|---|---:|---|---|
| Codex CLI | `0.144.1` | matches the latest verified upstream release | retained |
| Codex desktop app | not changed in this phase | excluded from automated updating by Hamish's instruction | untouched |
| Node.js | `24.18.0` | current LTS line; Node 26 is a non-LTS current line | retained |
| npm | `12.0.1` | latest verified registry release | retained |
| Git for Windows | `2.55.0.windows.2` | latest verified Git for Windows release | retained |
| Python | `3.12.10` | last Python 3.12 release with Windows binary installers; Python 3.14.6 is the current feature line | retained pending a separately tested major-version migration |
| PowerShell 7 | not required | Windows PowerShell supports the present workflow | no change |

The version evidence is the official [Codex CLI 0.144.1 release](https://github.com/openai/codex/releases/tag/rust-v0.144.1), [Node.js 24.18.0 LTS release](https://nodejs.org/en/blog/release/v24.18.0), [npm version registry](https://www.npmjs.com/package/npm?activeTab=versions), [Git for Windows 2.55.0.2 release](https://github.com/git-for-windows/git/releases/tag/v2.55.0.windows.2), [Python 3.12.10 release record](https://www.python.org/downloads/release/python-31210/), and [Python 3.14.6 release record](https://www.python.org/downloads/release/python-3146/).

## Storage posture

- `C:` free at the closeout audit: approximately `23.13 GiB`.
- `D:` free at the closeout audit: approximately `602.70 GiB`.
- Research, build, QA, and deliverable work remained in the D-drive Eiren worktree and D-drive temporary QA folders.
- No new runtime or application update was installed during this v641-v1 phase.

## Boundary

A blanket upgrade of every application, driver, package, or operating-system component was not attempted. Such an operation would be an unbounded maintenance mutation without a single rollback plan. This audit covers the toolchain used by the phase; major-version migrations, especially Python 3.12 to 3.14, remain separately testable candidates rather than implicit upgrades.

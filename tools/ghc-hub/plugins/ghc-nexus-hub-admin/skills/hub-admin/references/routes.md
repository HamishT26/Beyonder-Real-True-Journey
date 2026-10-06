# Hub 2.1 routes

Use `node <reviewed-hub.mjs> plan <action> --json`. Execution, when already authorized, is `node <reviewed-hub.mjs> run <action> --execute --json`, except interactive actions require a real terminal without `--json`.

| Action | Purpose and limit |
|---|---|
| `app-admin-check` | Read-only launcher check; no App starts. Check output is not evidence of a future App token. |
| `app-admin` | Direct administrator App request through the installed signed launcher and ordinary Windows consent. Package identity can be absent. |
| `app-registered-check` | Non-launching check of the registered route. |
| `app` / `app-registered` | Registered Windows activation for package-aware operation; no elevation guarantee. |
| `cmd-admin-check` / `cmd-check` | Check the corresponding CMD Hub route without opening it. |
| `cmd-admin` / `cmd` | Open the existing CMD Hub with requested elevation/current token respectively. |
| `powershell-admin` | Open the existing PowerShell administrator route. |
| `linux-admin` | On Windows, explicit local WSL Ubuntu root; on Linux, the current executor's root or normal sudo policy. This is not an automatic cloud route. |

`app-direct` is a legacy alias of the direct route. Prefer the explicit `app-admin` name. `app-check` checks the normal registered App route. Host startup, user consent, application readiness, package identity and effective token are separate results.

Runtime baseline: commit `25a3f7848fd4c2d2014a0aad8c75531821db51f6`. Reconcile newer reviewed releases before applying these references; the source tree may contain concurrent unpublished work.

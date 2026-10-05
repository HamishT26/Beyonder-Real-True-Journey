> Historical v1 operator and release record. For the current v2 interface and limits, read [NEXUS-V2-GUIDE.md](NEXUS-V2-GUIDE.md). Counts and observations below belong to the first release.

# GHC Nexus Hub operator guide

This hub joins the supported Windows, Linux, Codex App and Codex CLI entrypoints in one keyboard menu and one command interface. PowerShell is the local foundation, existing cloud Linux workers are the preferred place for larger Linux jobs, and local WSL is optional. The hub does not create a new cloud computer, a permanent remote terminal, a model, or a replacement operating-system kernel.

## Open the installed hub

Use **GHC Nexus Hub - Administrator** on the Windows Desktop or Start menu. The source and installed runtime live on D:. The existing GHC Codex Administrator and PowerShell shortcuts remain available.

The new shortcut starts:

```powershell
& 'D:\GHC-Archives\global-tools\ghc-nexus-hub\Start-GhcHub.ps1'
```

Normal Windows UAC is requested if the launching process is not already elevated. The observed installation check was already running with an Administrator token. Child processes inherit their actual parent token; a menu label or a Codex Full access setting does not create Windows Administrator membership.

For a check that opens no app or terminal:

```powershell
& 'D:\GHC-Archives\global-tools\ghc-nexus-hub\Start-GhcHub.ps1' -Check
```

For an intentionally unelevated or current-token terminal, use `-CurrentUser`. The hub displays its host and workspace. Type a number, inspect the displayed command and route description, and confirm the selected action. Type `0` or `q` to exit. Opening the menu does not start Ubuntu, a model request, a periodic probe or a background service.

## Choose where the work runs

| Need | Hub route | Execution location |
| --- | --- | --- |
| Small local scripts, Git, Node, Python or Windows administration | PowerShell here or Administrator PowerShell | This Windows laptop |
| A larger Linux task | Linux primary or C, using the official Codex Cloud picker | The cloud environment actually selected and available through that route |
| A Linux shell within an existing cloud worker | Linux shell in that worker's installed hub | That worker, not the laptop |
| Local Ubuntu compatibility | U on Windows | Local WSL, using laptop RAM |
| Linux administration | Administrator Linux shell | On Windows this is local Ubuntu as root; on Linux it uses the existing root identity or normal sudo |
| A CLI collaborator | Codex CLI, or resume with the exact existing session UUID | The host where the hub is running |
| The desktop app | Launch ChatGPT/Codex app | Windows, through the reviewed app launcher |

The confirmation preceding a Windows Linux-administration action identifies that it starts local WSL. It is not a cloud root shell. Local Ubuntu remains unresolved after the two authorized startup trials; leave that route unused until a deliberate repair investigation is started.

The official `codex cloud` picker and `cloud list` are experimental surfaces. Their tasks and environments may differ from the managed cloud chats used by the GHC team. An empty listing is not evidence that those managed workers are absent. An error does not authorize a second task or a replacement identity. A supported permanent remote terminal remains a later option under Hamish's answer 60.

Mira Fen and Linden Quay have separate, user-owned Linux hub installations. Their managed workers can perform Node, Python, Bash and any actually installed PowerShell work. The local hub does not silently mount D: in those workers. Transfer only the selected files a job needs, with byte counts and hashes, then return selected results for local review. Host memory totals are not promises of available container quota, GPU access or a particular data centre.

## Use from an App or CLI tool

The menu needs a real terminal. App and CLI collaborators can use the same implementation through ordinary commands and JSON instead:

```powershell
$ghcHub = 'D:\GHC-Archives\global-tools\ghc-nexus-hub\hub.mjs'
node $ghcHub doctor --json
node $ghcHub actions --json
node $ghcHub plan codex --json
node $ghcHub plan codex-resume --session 'EXISTING-SESSION-UUID' --json
node $ghcHub run auth-status --execute --json
node $ghcHub run cloud-list --execute --json
```

Replace the resume placeholder with a verified existing UUID. `plan` constructs a command without executing it. `run` requires `--execute`; interactive shells and sign-in are deliberately rejected with machine JSON output. A reported launch request is distinct from observing a usable app or a completed cloud job.

On Linux, use `sh start-ghc-hub.sh` in the installed directory. An operator can set `GHC_HUB_CODEX` and `GHC_HUB_PWSH` to verified absolute executable paths. `GHC_HUB_WORKSPACE` selects an existing working directory; `GHC_HUB_HOME` selects the private event directory. These are local operator settings, not values imported from untrusted research or advice files.

The CLI route requests Astra with Max reasoning, the observed priority/Fast tier identifier, and Full access. It uses no daemon and disables unrelated MCP services only for that invocation. Each executor retains its supported context configuration. Those request arguments are not an attestation of the backend model tier, context capacity, network permissions, operating-system token or cloud account role.

## Sign-in and private storage

Hamish completed the official Windows CLI sign-in. A separate forced-keyring check succeeded, the global Windows setting was selected as `cli_auth_credentials_store = "keyring"`, and a fresh CLI process using that configuration reported a ChatGPT login with exit zero. The TOML configuration parsed successfully. Windows global context, model and sandbox settings were not changed by that migration.

The working sign-in was preserved while this was prepared. No raw credentials were read into the coordinator, uploaded, committed or included in the hub logs. The hub's interactive sign-in routes inherit terminal input/output so that device codes and passwords are not captured in event files. Use the official browser or device flow if a later login is actually required. Login status is a time-specific observation; it is not a guarantee against revocation or expiry.

The cloud CLI has its own account store and lifecycle. Windows Credential Manager is not copied into a Linux worker. If a cloud status check fails, first compare the selected host, executable, configuration and private-store location with the previous verified state. A different store, expired credentials, an unavailable backend and a parse failure need different remedies. Repeated sign-in cannot restore a missing conversation transcript.

Google and ChatGPT account menu entries open official account pages. Signing in there does not grant every Google service scope or make all connectors persistent. API credentials, subscription login, Google authorization and managed-worker credentials are separate. Supported private persistence can be investigated per provider; the hub does not implement an unofficial shared token vault.

## What was verified

The release Windows suite passed 36 checks in one Node process using `--test-isolation=none --test-concurrency=1`. The launcher harness passed 26 checks. The installed Administrator wrapper and app launcher passed their non-launching checks. The installed menu rendered in a real terminal and exited zero after `q`. These are separate observations, not a single system-wide certification.

Independent review found genuine defects in the first candidate: stderr could corrupt JSON parsing, output-limit validation had a gap, process cleanup evidence could be lost, and terminal control characters needed escaping. Those failures remain in the evidence bank. The second candidate resolved the affected checks; a subsequent independent retest identified a dropped termination signal, which the final two-file correction preserves in both the action result and its event record.

Linux results remain attributed to their actual executors. Mira reported 35 passing candidate checks and four menu checks before the final narrow correction. Quay's second-candidate evidence contains 18 independent checks, seven affected supplied checks, two menu checks and one 10,000-record stress experiment. Ten thousand records are not ten thousand separate tasks. Final correction checks and installed file hashes are recorded separately from earlier suite results.

To reproduce the selected portable suite on a supported Node release:

```text
node --test --test-isolation=none --test-concurrency=1 hub.test.mjs privacy-regression.test.mjs
```

Older worker-isolation failures and incomplete attempts are retained. The selected test mode does not turn those original attempts into successes. Test scratch directories remain available for inspection. Windows UAC acceptance, cloud authentication, a rendered desktop UI and Linux kernel behavior require their own evidence; fixtures do not establish them.

## Timeouts, resources and failure recovery

Small local probes are bounded. Their deadlines are not real-time scheduling guarantees if Windows is stalled. The hub records elapsed time, close observations and immediate-child cleanup separately. It does not claim to contain arbitrary descendant processes. An action with an unknown effect is reconciled before another action is started.

The app launcher now distinguishes an observed existing app, confirmed absence and an uncertain process observation. It holds an uncertain duplicate-launch result instead of assuming absence. Timing logs retain inclusive duration and add work and logging-cost fields. A timing record is not a measurement of app readiness or proof of why the UI previously froze. The installation did not restart Codex.

WSL's first 120-second outer allowance returned its own startup timeout after about 96 seconds. A second console-only trial returned the same service error after about 106 seconds. Neither reached the Linux readiness marker. The earlier one-CPU, 1 GB RAM and 2 GB D-drive swap configuration was restored and shutdown confirmed. No distribution data or package cache was deleted during these trials. Increasing a timeout or RAM cap again without new diagnostics would not establish the cause.

## Records, rollback and the next phase

The local release evidence bank is `D:/GHC-Archives/phase-banks/saelin-v708-v4-remasters-20261004/hub-20261005`. It contains installation receipts, source pins, the original launcher backup, the configuration change receipt, Windows and selected cloud results, WSL observations, and the separate Method Flow. The private Beyonder-Real-True Journey Page carries selected release material. Credentials and raw private histories are excluded.

If rollback is needed, inspect the installed file hash and the recorded backup before replacing a file. Preserve any later changes. The Credential Manager rollback concerns the recorded configuration selection; it is not a promise to undo server-side OAuth token rotation. Do not restore old credential caches from a backup.

The hub is a completed engineering component within the broader programme, not completion of its fifty research projects. Run (3) x2 remains unstarted pending Hamish's later continuation and the outstanding x1 review. The original missing CLI histories remain held; the authorized Corin and Ellis continuations remain distinct. Sentinel-1 is preparation only. The research baseline keeps GMUT hypotheses separate from empirical validation and correctly records Navier–Stokes as unsolved and Poincare as solved in the Clay Millennium list.

# GHC Nexus Hub

A portable terminal menu and machine interface for the current Windows or Linux executor. Node 20+ and its standard library are sufficient. No npm dependencies or background server are installed.

Run `node hub.mjs` in a terminal. For agent tools, use:

```text
node hub.mjs doctor --json
node hub.mjs actions --json
node hub.mjs plan codex --json
node hub.mjs run auth-status --execute --json
node hub.mjs run cloud-list --execute --json
node hub.mjs plan codex-resume --session EXISTING-UUID --json
```

`plan` never launches a process. `run` requires `--execute`. Interactive shells, sign-in and Codex require a real terminal; command/JSON actions work from App and CLI shell tools. The menu is keyboard operated, preserves scrollback and starts no probes until selected. No terminal mouse motion is required by this program.

## Windows

Use `Start-GhcHub.ps1` for the new Administrator hub, accepting normal Windows UAC when required. `-CurrentUser` runs with the current token. `-Check` reports the proposed launch without elevating or opening a terminal. The hub's child CLI inherits that terminal token; Full access does not create Administrator membership.

The app and Administrator PowerShell actions call the existing `Start-GhcAdmin.ps1` so its signature and duplicate-app protections remain. The app is not restarted to install this hub. PowerShell remains the default. A local Ubuntu action explicitly starts WSL and consumes laptop resources; it is not a cloud shell, and the historical normal-startup issue remains unverified.

## Linux and cloud

Use `sh start-ghc-hub.sh` or `node hub.mjs`. The same source runs inside an existing cloud worker. Linux administration uses existing root identity or normal sudo; the hub cannot grant a provider role, remove a sandbox or mount the laptop's D drive. PowerShell is offered only if installed. A supported worker/source transfer and its receipt are separate from successful execution.

The `cloud-list` action delegates to the experimental official `codex cloud list` command. Its availability and environment population must be checked. It does not automatically connect to every managed app worker or submit new tasks. Existing collaborator coordination remains in the supported app tools. Permanent remote terminals are a later option under answer60.

## Credentials

Use `auth-status`, `auth-login` or `auth-device`. Status returns only the observed outcome and method; failed observations remain unknown. Sign-in uses inherited terminal I/O, so codes, tokens and passwords are not captured by this hub. Google and ChatGPT account actions open official account pages; Google sign-in does not grant every service scope. Existing supported private credential stores are retained. A permanent cross-cloud login is not promised; revocation, MFA and worker retention still apply. Never put auth.json, cookies, API keys or private cloud histories in this package.

## Configuration and observations

Optional environment variables: `GHC_HUB_WORKSPACE` (existing working directory), `GHC_HUB_HOME` (private event directory), `GHC_HUB_CODEX` and `GHC_HUB_PWSH` (absolute executables). Windows accepts .exe overrides, not .cmd/.ps1 shims. These are trusted local operator settings, never loaded from transferred documents. Windows defaults use the existing D-drive toolchain. Linux defaults use executable PATH entries.

The CLI launch requests Astra/Max/Fast, 872k context and 600k compaction with Full access, `--no-daemon` and a limited MCP selection for that invocation. Requested settings are not backend attestation. Shared global config is not overwritten. App-managed binaries are not silently replaced.

Event files contain action, outcome, elapsed time and version only. They exclude command output, credentials and prompt content. A telemetry failure is reported separately from the action. Bounded probes stop only their owned immediate child; descendant containment is not claimed. Interactive children end when the user exits them.

## Verification

Run `node --test hub.test.mjs`. Set `GHC_HUB_TEST_TMP` to an owned D-drive directory on Windows. Tests exercise actual child failures, timeout, output limits, JSON errors, missing tools, injected selectors, credential-output exclusion and inactive menu behavior. The test scratch directory is retained for review. Linux and real-terminal smoke results are recorded separately from unit tests.

Research x2 remains paused while this separate launcher stage is reviewed. Sentinel-1 remains preparation, and the seven Millennium problems remain a separately sourced research plan.

# Hub 2.8: host capabilities and desktop integration

This is a candidate continuation of the same renewed run (3) x1. Installed Hub 2.7 and its first-failure receipts remain the release baseline until integration validation and promotion.

## Implemented candidate surface

The existing sixteen Hub tools can be combined with four new read-only tools: host resources, bounded Tailscale device inventory, desktop backend status, and workload planning. `mcp-hub28-server.mjs` requires an explicit private configuration with schema `ghc.hub28.config.v1`, enabled=true, absolute adminPolicy and tailscaleKeyFile references. No credential is supplied as an MCP argument. The API adapter uses only GET on the official Tailscale device endpoint, refuses redirects, and omits addresses, keys and full device identifiers from its result.

Plans reserve 256 MiB locally and permit one local workload at a time. Cloud admission requires separate recent execution evidence. Tailscale membership, model names, administrator labels, and context-window settings cannot establish CPU pooling or remote execution authority. The current entrypoint has no verified cloud executor registry and does not auto-start WSL.

## GUI backend candidate

CursorTouch/Windows-MCP 0.8.8 is under review at source revision b74c507d9e709223a0904cf08019edf55f2a75bb. It requires Python >=3.14. Dependencies are staged separately under D with a hash-locked requirements file. This is a tool server, not a new AI/model session.

Use private stdio and an explicit GUI-only tool list. Set ANONYMIZED_TELEMETRY=false, POSTHOG_API_KEY empty and WINDOWS_MCP_WATCHDOG=off. Keep the existing audited Nexus file/command tools instead of exposing duplicate Shell, Registry, Clipboard, filesystem and process-control tools. Retain upstream human takeover and visible-control mechanisms. Do not disable them to resolve failures.

Full screenshots need a separately reviewed bounded image transport; the current Nexus transport intentionally caps an outgoing message at 32 KiB. Do not silently raise that cap in the production file/command server. A staged package or successful MCP handshake is not proof of working screenshots/input, safe privilege inheritance, or remote GUI availability.

Browser CDP is a browser debugging capability, not full Windows control. Use the supported tab-scoped browser capability when present. No public CDP listener, browser profile copy, cookie export or remote credential relay follows from this integration.

## Current host and Windows research

The 11 October local snapshot measured Windows 11 Home 26H2, build26300.9550, Intel N100, 3789 MiB usable RAM, and an elevated executor. Hyper-V's full role is not supported by Home; a feature query with an empty result is not evidence that Hyper-V is installed. WSL and VirtualMachinePlatform are enabled but no WSL VM process was observed. The user selected memory=512MB for future on-demand local Linux; one CPU and existing swap settings are preserved. Linux has not been started to test that cap.

Windows Cloud Rebuild is a destructive recovery/reinstall feature, not a workload-distribution service. Windows365 provides a managed Cloud PC; Azure VMs provide configurable compute with infrastructure and maintenance costs. The user chose research only, with no purchase or provisioning. An OS update does not add absent NPU hardware or confer rights on a cloud client.

## Acceptance before promotion

- Retain source-specific unit, original SDK regression, and new MCP discovery results separately.
- Verify a genuine private remote tool exchange after the final connector step.
- For GUI: verify staged dependency integrity, tool allowlist, telemetry-off config, bounded screenshots, stale-input rejection, single-controller ownership, user takeover, secure-desktop refusal, timeout cleanup and measured memory.
- Measure the GUI worker's actual OS token and session. An elevated file server alone does not prove GUI control of elevated windows.
- Keep Chrome held; use the in-app browser. Prepare named collaborator handoffs if native messaging is unavailable, without claiming delivery.
- Preserve the prior installed release and private config backups until all required checks pass.

Primary references: https://tailscale.com/docs/reference/tailscale-api ; https://learn.microsoft.com/en-us/windows/wsl/wsl-config ; https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/host-hardware-requirements ; https://learn.microsoft.com/en-us/windows/configuration/cloud-rebuild/ ; https://learn.microsoft.com/en-us/windows-365/overview ; https://learn.microsoft.com/en-us/azure/virtual-machines/overview ; https://github.com/CursorTouch/Windows-MCP/tree/b74c507d9e709223a0904cf08019edf55f2a75bb

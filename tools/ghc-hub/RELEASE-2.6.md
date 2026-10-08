# GHC Nexus Hub 2.6

This release keeps the existing nine read-only MCP tools and strengthens App launch selection.

The Windows launcher reads the current user's registered main packages for every request, chooses the highest unambiguous numeric version, and validates its manifest, executable and signature. A failed newest candidate holds the launch instead of selecting an older package. Current, older, differing or unreadable App processes prevent a duplicate launch. The check output separates the selected package version and process state from Windows token, package identity and readiness. The user controls App closure and restart.

The SDK transport now permits 32 KiB output frames. The declared maximum catalogue, including 128 aliases of 64 characters and both MCP result representations, requires 25,223 bytes when availability is false. Its former 16 KiB limit closed the connection. The 64 KiB queue, one MiB aggregate/rolling budgets, input bounds and read-only projection stay in place. Explicit smaller limits remain supported. Queue-only overrides below 32 KiB also need an explicit smaller frame limit. Very long correlation IDs can still exhaust the fixed frame budget.

Windows Hub wrappers select the verified D-drive Node 26.11.1 installation. PowerShell 7.6.6 remains selected. Standalone Codex CLI updates are separate from the App's managed executable. Interactive CLI and sign-in use standalone PowerShell or the Hub terminal under the current operating preference; browser authentication uses Chrome.

Config Menu's existing exact Guardian-key audit remains available. Removing obsolete MCP definitions is a separate, hash-bound local configuration transaction; it does not uninstall App connectors. A clean saved config does not prove that a retained UI warning has disappeared.

Validation for this change includes 13 frame/queue/quota checks, 24 SDK interoperability checks across legacy and modern modes with the maximum chat catalogue, 16 package-selection fixtures, nine registered-route fixtures, and a live no-launch Windows selection check. Initial wrapper and test-expectation failures are retained in the owner evidence bank. These checks do not establish every client, every envelope, long-duration endurance or Cloud authentication.

Admin plugin 0.1.2 documents the selection rules. Exec plugin 0.1.5 refreshes its existing 15 runtime source pins. The lifecycle-hook registration remains singular; application checks are not additional Codex hooks.

See MCP-SETUP.md for client integration. Installation, plugin cache readback, private tunnel health and provider-level availability require their own receipts.

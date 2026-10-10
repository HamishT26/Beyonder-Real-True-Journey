# GHC Nexus Hub 2.8

This release adds measured resource planning, bounded Tailscale device inventory, truthful GUI readiness, and an explicit active-agent message relay to the private file/terminal server. It exposes 25 tools: the existing sixteen, four host/network/workload tools, and five message lifecycle tools. It does not provide an autonomous chat sender or verified full desktop GUI control.

## Message relay

The five tools are nexus.messages.routes, prepare, claim, record and receipt. Selected aliases preserve provider and host; drafts are limited to 2048 UTF-8 bytes. A claim returns exact native tool arguments after freshness, hold and digest checks. The active agent must verify current human authorization and call mcp__codex_app__send_message_to_thread once. No external message is sent by the server itself. Unknown results cannot be blindly retried. Stored receipts are caller-reported, not signed provider attestations, and do not establish recipient completion.

The real 11 October test used the Hub outbox and native fallback. Orenna Vale, Set up Linux video streaming (Merrin), Teren Serein, Elian Vale and Avelin Reed returned matching test IDs and each reported one successful private MCP status call. Rowan Vale was rejected by the native managed-environment guard; Hamish selected Avelin as the fallback. These were connection tests; research remained paused.

Chat route observations now refresh inside a running server while alias identity stays fixed. Browser-open plans are labelled manual, not local executor routes. Adding aliases still requires reviewed configuration and a server restart.

## Runtime and limits

The launcher checks the named runtime before connecting. Nonzero vendor connect exit and eventual readiness remain separate observations; a pending runtime is not an instruction to reconnect. The private hub28.json selects the new entrypoint. Stop/start only the existing ghc-nexus alias; do not create another connector.

Tailscale inventory uses only the official GET devices API with the existing private key file reference, excludes addresses/keys/full IDs, and never grants shell access. Resource planning reserves 256 MiB and permits one local candidate; a plan does not execute or enforce host-wide scheduling. Remote execution needs fresh executor evidence. WSL never starts automatically.

GUI status remains unavailable until backend acceptance succeeds. A staged Windows-MCP package, metadata handshake, or Administrator token alone is not full desktop GUI verification. This release does not expose GUI input, screenshots, an unauthenticated CDP listener, new credentials or Cloud provisioning. Existing terminal commands still require exact local approval.

## Evidence and rollback

The current evidence bank is D:/GHC-Archives/phase-banks/saelin-renewed-r3-x1-20261008/resume-20261011-route-and-hub28. Focused relay/binding tests passed 35/35; protocol tests passed 26/26 before final version promotion; launcher state fixtures passed 6/6. Read final installation/verification receipts for promoted source hashes. Do not treat a source manifest as deployment evidence. The prior installed release and private profile/configuration are backed up before promotion.

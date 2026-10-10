# Nexus Hub Admin Desktop Commander

Hub 2.7 combines the nine existing read-only Nexus tools with seven scoped file and command tools in one MCP server. It uses the official MCP SDK and the existing outbound OpenAI private tunnel. It does not open a public listener.

The executing host supplies the filesystem and OS token. A Linux Cloud or ChatGPT client can call the Windows host's tools when its connector permissions allow it; this does not turn that client's own environment into Windows or grant it a new local Administrator token. Windows Native and CMD remain selected. WSL is deferred.

## Entry points

- `node mcp-admin-server.mjs ABSOLUTE_PRIVATE_POLICY`
- `node admin-cli.mjs status ABSOLUTE_PRIVATE_POLICY`
- `node admin-cli.mjs approve ABSOLUTE_PRIVATE_POLICY REQUEST_ID REQUEST_SHA256`

The policy is private, has schema `ghc.admin.policy.v1`, and must explicitly enable the server. It contains up to eight named absolute file roots with per-root write permission, a private state directory outside those roots, and selected CMD/PowerShell/Node/bash executables pinned by SHA256. Never put keys in the policy or in command arguments. The existing tunnel profile references its separate private credential file.

## File and command behavior

File tools list bounded entries and read/write ordinary UTF-8 text up to 8 KiB. Path traversal, credential-store names, symlinks/junctions and hard-linked files are refused. New files require `expectedSha256: null`; replacements require the current content digest and retain the original in private `file-backups`. These checks detect ordinary concurrent changes; they are not a filesystem sandbox or an atomic compare-and-swap against a hostile local administrator.

`nexus.exec.prepare` returns an exact command, shell, working directory, timeout, request ID and digest for review. It does not execute. Local approval binds the exact request and current policy. `nexus.exec.execute` claims the approved request once. Repeated calls cannot re-execute it; use `nexus.exec.receipt` to reconcile an uncertain response. Requests expire after 15 minutes. The selected executable is checked before approval and execution. The environment excludes inherited API keys and provider tokens.

Approved commands use the server's OS privileges and can access outside the file roots. Review the complete command before approving it. The command deadline is at most 30 seconds and combined output is bounded to 8 KiB. Windows uses taskkill on the owned process tree; Linux uses a process group. These are not Windows Job Object isolation and cannot guarantee containment of deliberately detached descendants. Do not approve commands that detach, daemonize or start untracked descendants through this interface. Use reviewed lifecycle scripts for persistent services.

If termination cannot be confirmed, the server writes `HALTED.json`, reports `childClosed: false` and refuses new work except status/receipts. That hold survives restarts. A local operator must reconcile the recorded request/process outcome before removing the hold. Never automatically retry a claimed command.

Replacement backups and request receipts need periodic operator review. No automatic deletion of retained outcomes is performed. Recognizable secret patterns are withheld/redacted; this is not complete sensitive-data detection. Do not place private contact records, credentials or raw conversation histories in exposed roots or command output.

## Computer use and messaging

The companion Admin Computer/Desktop Commander plugin routes UI actions to the supported Computer/Browser or Remote Desktop Commander tools already available to the client. This server does not invent GUI automation, provider authentication, or cross-chat send APIs. The Nexus chat tools show selected aliases and route plans. Actual messages use the existing authorized native chat tools, with one send and a recorded outcome.

## Release and recovery

Keep the last verified 2.6 installation as a rollback copy until 2.7 discovery and benign file/command checks pass. Verify source/installed hashes from `installation-files.json`. Restart the tunnel runtime only through its named alias; do not create another tunnel. A saved profile, a running local server, a connected tunnel, a plugin installation, and a successful remote tool call are separate observations.

Stop the named runtime before replacing its files. Do not restart the App or laptop automatically. Retain first failures and incomplete checks alongside later successful validation.

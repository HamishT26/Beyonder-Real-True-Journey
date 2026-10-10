---
name: private-tunnel-operations
description: GHC-Nexus-Private-Tunnel routing, verification and recovery.
---

# Private Nexus tunnel operations

Read D:/GHC-Archives/global-tools/ghc-nexus-hub/ADMIN-MCP.md and the current phase checkpoint before changes. Reuse the existing ghc-nexus alias and registration. Never create a duplicate connection as a recovery shortcut.

Measure runtime status, readiness, tool discovery and one benign operation separately. Use tunnel-client runtimes status ghc-nexus --json and print only safe status fields. Never print complete profile files, credential contents or raw log tails. The runtime uses a private file reference for its key.

The tunnel is outbound HTTPS and the server has no public listener. Start/stop only the reviewed named runtime. Persistent startup uses the explicit local lifecycle script and a current-user logon task with an inspectable rollback. Do not kill every Node, PowerShell or Codex process.

The original nine Nexus read-only tools and seven Admin tools share one declared catalogue. Actual GUI actions and native chat delivery use supported existing client tools. No automatic AI session creation, peer messaging or relay loop is installed. Authentication must occur in the user-selected Chrome or standalone terminal, with secrets entered by the user.

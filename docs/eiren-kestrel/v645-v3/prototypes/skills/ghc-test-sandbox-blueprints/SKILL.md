---
name: ghc-test-sandbox-blueprints
description: Lint owner-scoped Windows Sandbox configuration templates, mapped-folder permissions, bootstrap gates, and host-change boundaries. Use before materializing or launching a GHC Windows Sandbox profile.
---

# Test sandbox blueprints

1. Parse each `.wsb.in` template as XML after substituting sanitized placeholder paths.
2. Require networking and vGPU disabled by default.
3. Require bootstrap and input mappings read-only; permit only one owner-scoped output mapping as writable.
4. Require the logon command to call the bounded bootstrap and verify administrative context inside the sandbox before installation.
5. Reject host feature changes, elevation, reboot, sibling paths, credentials, and unverified installers.
6. Record CLI or feature availability separately from runtime success.

Template linting is not evidence that Windows Sandbox launched or that the host is secure.

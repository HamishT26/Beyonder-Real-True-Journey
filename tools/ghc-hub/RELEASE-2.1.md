# GHC Nexus Hub 2.1

This release adds a Windows Command Prompt entry point and restores the explicitly selected direct Administrator App route after both registered launch comparisons measured non-elevated execution.

The normal App action remains registered Windows activation. Use it for App update checks. The Administrator App action requests the signed installed executable through normal Windows elevation. The package stays installed and registered; a directly launched process can lack package identity, so its in-app updater can be unavailable. The launcher resolves the current package location at each launch instead of pinning an obsolete version directory.

## Use the Hub

- Open **GHC Nexus Hub CMD - Administrator** to request an elevated Command Prompt containing the same Node Hub.
- Open **GHC Nexus Hub CMD - Current User** to inherit the current Windows token.
- In the Hub, **D** requests the CMD Hub with the current token, **E** requests Administrator CMD, and **A** requests the direct Administrator App launch.
- Normal **8** remains the registered App route. Quit the running App before changing its launch route.
- `ghc-nexus plan cmd-admin --json` and `ghc-nexus run cmd-admin-check --execute --json` inspect the CMD launch without opening it.

PowerShell remains the default integrated shell and Windows native remains the agent environment. CMD does not add Windows privilege, cloud access, WSL availability or model entitlement. WSL stays optional and must be started explicitly.

## Chat admission

A fresh local `notLoaded` observation now allows the official CLI to attempt its existing-session resume. It does not assert that the chat is idle in every client. Explicit holds, active observations, host matching, metadata freshness and the CLI's own session ownership still apply. No session lock is removed or replaced. The official local picker remains available when metadata reads cannot complete. Managed-cloud and ChatGPT histories retain their original providers.

## Credentials and computer use

API credentials are read only by their authorized private consumer. They are excluded from release manifests, source capsules, identity profiles and memory exports. API key access is separate from plugin OAuth, Windows elevation and cloud execution permissions.

This release does not install a protected-target computer-use bypass. The supported application permissions and host controls remain authoritative. The four proposed broader plugin packages and Sentinel implementation are separate unfinished work.

## Restart checkpoint

The direct Administrator shortcuts are prepared for Hamish's next controlled launch. The resulting process token is unverified until measured after that launch. An accepted elevation request is not a successful elevation result.

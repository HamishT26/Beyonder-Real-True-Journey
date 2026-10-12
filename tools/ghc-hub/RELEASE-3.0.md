# GHC Nexus Hub 3.0

Hub 3.0 adds a bounded skill library lookup and repairs launcher tool selection and installation dependencies. Deployment and live connector state are recorded separately in the owner checkpoint.

## Skill library

`nexus.skills.lookup` searches the reviewed catalogue with at most ten results. An exact skill name and `includeGuide: true` request a hash-verified excerpt of its SKILL.md. The reader checks its allowed roots, refuses redirected or hard-linked paths, limits file sizes and the serialized response, and does not execute, install or restore anything. Historical guide instructions remain source material rather than new authorization.

The 12 October library migration retained700 active user guides. It archived1465 documentation packages containing2917 files on D:, alongside149 previously retired guides. The catalogue therefore contains2314 active and archived names. Executable packages and16 existing linked skill directories remain active; the lookup deliberately refuses reading through redirected paths. The migration receipt records content preservation, not scientific validation or an equivalent amount of physical disk relief.

After installation, `ghc-skills ghc-admin-nexus` searches names, and `ghc-skills ghc-family-meta-tool-box --read` reads one bounded guide excerpt.

## Launcher and tools

The reviewed PowerShell, Node, Git and GitHub CLI directories precede existing shims for a newly launched GHC process. Missing optional tools retain their existing fallback entries. Tunnel Status and Stop do not require the new PATH helper; Connect requires the reviewed Node executable. The helper is included in the Hub manifest and copied alongside the shared App launcher. Machine-wide PATH is not changed by the helper, and a running or registered App's effective environment is not inferred from this selection.

Optional convenience commands `ghc-openai` and `ghc-osv` select the separately installed official OpenAI REST CLI1.38.0 and OSV-Scanner2.7.0. They do not load or print credentials. Provider SDK packages remain in their separate D: environment; their installation, import checks and any future API execution have separate receipts. Codex SDK use must select the existing native CLI explicitly and requires authorization for any new model session.

## Validation and limits

The new library reader passed16 focused tests, including changed bytes, path escape, hard links, junctions, incomplete indexes, invalid encoding and output limits. The PATH helper passed12 pure fixture checks under Windows PowerShell. The combined server passed16 SDK checks across legacy and modern protocol modes, exposing26 unique tools while retaining exact command approval and an unavailable GUI backend. A prior integration attempt was held before execution at59.2MiB free memory. These are distinct checks; earlier evaluations are not replayed or counted again.

The first provider SDK import check timed out and was retained as a failure. Its diagnostic retry identified a missing optional MCP client imported by Agents SDK. Consult the current checkpoint for that separate repair outcome; provider SDK import readiness is not a Hub server dependency.

The compatible `mcp-hub28-server.mjs` entrypoint and `ghc.hub28.config.v1` private configuration are retained. A refreshed client catalogue is needed to see the new tool. Live private-tunnel connectivity, Windows elevation, App identity and GUI readiness must each be measured separately. This release does not create a public endpoint or replace the local command-approval mechanism.

No API key, raw chat history, operating-system cache deletion, new lifecycle hook or automatic App restart is part of the release. Heartbeats stay paused. Resource pacing follows CURRENT: ease work below100MiB, and below70MiB take an up-to180-second quiet interval with60-second checks and an early resume above200MiB. The GUI probe retains its separate512MiB admission guard.

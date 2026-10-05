# GHC Nexus Hub 2 — operator and integration guide

This release extends the keyboard menu and ordinary command interface with a shared chat catalogue, a laboratory, private memory, project identity certificates, a Sentinel specification builder and explicit remote-connection plans. These are tools for the current executor. They do not turn the laptop into a cloud VM, migrate ChatGPT conversations into Codex models, or grant provider permissions.

## Everyday entrypoints

The Windows administrator shortcut still opens `Start-GhcHub.ps1`. Ordinary commands use the installed `hub.mjs`; `--json` is intended for App and CLI agents. The source tree and installed copy are separate, and release verification compares their bytes.

Menu 7 is the **GHC-Family chat panel menu**. Menu 10 is the **GHC-Family Laboratory**. The next entries open Freed ID profiles, the private Memory bank, the Sentinel builder and remote-connection plans. App action 8 uses registered Windows activation. The separately labelled A action and the GHC Codex Administrator shortcut request the registered Windows Run as administrator verb. The normal registered shortcut remains separate. Both validate the current package and refuse a duplicate running app. The legacy direct-executable route is available only as the explicit app-direct command. Registered launch requests still require a post-launch check of package identity, effective elevation and App readiness.

```text
node hub.mjs chats recovery --json
node hub.mjs chats list --json
node hub.mjs chats list --refresh --limit 100 --json
node hub.mjs chats resolve --id EXACT-ID --json
node hub.mjs chats plan --id EXACT-ID --json
node hub.mjs chats open --id EXACT-ID --execute
```

The offline recovery view lists preserved IDs, original hosts, last observations and route hints without querying a service or starting a chat. Menu P inside the chat menu opens the official local CLI resume picker; the user selects the existing session and the CLI enforces ownership. It does not convert managed-cloud or ChatGPT histories.

A successful explicit refresh saves a validated local metadata snapshot so later exact-ID commands can select the discoveries. The display is limited to100 rows, while exact-ID selection uses the full saved catalogue. The menu shows the ID and host and offers a title/ID filter. A failed local cache save is reported separately from the provider read.

The catalogue combines explicitly imported App/ChatGPT metadata with supported local Codex App Server metadata and the separate Codex Cloud task list. Each record retains its provider type, host, source and observation time. A title is a display label, not proof that two records are the same conversation. Matching kind/host/ID records can be coalesced; conflicting host bindings remain distinct. Ambiguous selections are refused.

Local resume admission is deliberately separate from listing. A saved row can be shown while its current activity remains unverified. Before opening a local chat, the hub rereads the binding and requests a current summary from its provider. Held, active, stale, missing, wrong-host and unknown states are not promoted into permission to resume. The official client must also acquire its own session ownership. The hub never removes locks. A failed connection is not followed by a duplicate model prompt.

An existing chat inherits its settings. The hub does not supply a new model, context, reasoning, tier, sandbox or MCP override when resuming it. A deliberate model change remains available through the original provider's controls. Starting a new CLI conversation is a separate menu action that requests the configured Astra/Max/Fast settings. Requested options are not independent evidence of backend speed or permission.

ChatGPT links open their original conversations. Managed cloud App chats can require the App's native route. Their presence in this list does not mean a local CLI has their history. The catalogue makes this limitation explicit instead of synthesizing a replacement conversation. Missing original CLI records stay held and separate from later authorized continuations.

## Laboratory

```text
node hub.mjs lab catalogue --json
node hub.mjs lab plan --id diffusion --size 1000 --json
node hub.mjs lab run --id diffusion --size 1000 --execute --json
node hub.mjs lab serve --execute
```

On the Windows host, the existing laboratory is located through its current-release pointer. The pointer's manifest digest and the selected entrypoint's manifest row must match the actual bytes. Serving that laboratory is an explicit foreground action; Ctrl+C stops it. Its existing localhost viewer is read-only.

The additional diffusion, queue and consent examples exercise the new job and receipt path. They are finite synthetic computations. The diffusion example is a standard conservative finite-difference comparison; the queue example measures a deterministic workload; the consent example checks a finite expiry/revocation policy. They are not empirical GMUT evidence, clinical guidance, legal certification or a solution of a Millennium problem.

Each plan identifies the current executor. Unsupported destination options are rejected; the lab never silently interprets --env as a cloud transfer. Missing or malformed job output is a failed result even when the child exits0.

Each run has an input limit, time limit and output cap. Its receipt retains executor, requested size, exit status, observed termination signal, cleanup state and numerical result. A larger cloud batch is a separate execution with its own record. Duplicate delivery or a rerun of the same fixture is not independent scientific evidence.

PowerShell remains the local foundation, managed Linux is preferred for larger computation, and WSL remains an optional route. Merely opening the hub does not start WSL. An administrator terminal is not an OS sandbox: arbitrary code run in it has the operating-system rights of that process. Use the managed provider's actual isolation and policy for workloads that need those boundaries.

## Freed ID profiles and certificates

```text
node hub.mjs identity list --json
node hub.mjs identity show --id merrin-tide --json
node hub.mjs identity add --file ABSOLUTE-PROFILE-JSON --execute --json
node hub.mjs identity certificate --id PROFILE-ID --execute --json
node hub.mjs identity verify --id PROFILE-ID --json
```

A Freed ID profile is a project identity and capability CV. It can contain a chosen name, role, hope, pronouns, a country of representation, known session identifiers, learning disciplines, pillars, hobbies and capability records. Unknown personal choices remain empty; the software does not invent a human age or professional qualification for an agent.

Capability claims retain their provenance category. An imported claim of an observation does not become independently verified simply by naming it `observed`. Unsupported observations are downgraded, and an issuer signature cannot repair absent evidence. Role labels do not confer permissions, professional authority or legal identity.

The local issuer uses Ed25519 to sign the stored profile bytes. Verification separates signature integrity from trust in the issuer. An independently selected issuer fingerprint is needed before `issuerTrusted` can be true. A correct signature proves integrity under that key, not the truth of every claim or control of a provider account. Older issued profile bytes are preserved so a later display-normalization change does not silently invalidate historical integrity checks.

Human contact details live in a separate protected D-only record. They are not duplicated into the agent CVs, catalogue, MCP responses, cloud packages or Git source. The private signing key also stays outside the source and export collections. Native provider sign-in stores remain separate from these project identities.

## Private memory and Spaces

```text
node hub.mjs memory list --json
node hub.mjs memory show --id RECORD-ID --json
node hub.mjs memory add --file ABSOLUTE-RECORD-JSON --execute --json
node hub.mjs memory export --id SELECTED-SHAREABLE-ID --execute --json
```

Memory records are immutable by ID in this interface and carry an explicit private/shareable classification. Selected exports include only named shareable records. There is no whole-drive upload, automatic sync, credential backup or raw chat-history export. A local export receipt does not establish an upload or a restored backup.

Known credential patterns are rejected in all retained memory fields, not just the main body. Reads validate older stored records before displaying or exporting them. These checks are a useful guard, not a complete detector of every secret or private fact. The operator still classifies and reviews selected content before an off-device transfer.

The Windows private root is protected with local ACLs. Reads reject redirected components and multi-link files, bind the opened file identity to a currently confined name, and reject changes observed during the read. Non-replacing writes use atomic no-clobber publication. These measures do not make a trusted-user file store an isolation boundary against a hostile administrator who controls the process or filesystem.

Spaces is a separate provider surface. A Page can hold selected nonsecret instructions, source manifests and reviewed outputs. The hub's local bank does not imply an automatic mounted Space or Google Drive filesystem. Save, upload, Page readback, publication and consumer verification remain separate records.

## MCP and App Server

The Nexus MCP process is a fixed read-only tool surface over reviewed aliases. It does not accept an arbitrary shell command or make a session ID into an authentication credential. Human contact files, raw transcripts, credential stores and issuer private keys have no MCP output slot. Stdio access inherits the launching process's operating-system boundary. Remote transport requires its own supported authentication and authorization.

The code distinguishes MCP from Codex App Server. MCP exposes Nexus tools; App Server provides supported Codex thread metadata and lifecycle methods. The small metadata adapter accepts summary reads only. It omits preview/history fields from returned summaries, validates protocol sequencing, bounds output and records cleanup uncertainty. A real reader reserves its capacity until closure is observed; an uncertain child is not treated as a free slot for automatic retries.

Protocol versions and client interoperability must be reported from the actual integration tests. A legacy MCP handshake test is not evidence of current-protocol support. Likewise, an installed server file is not evidence that a new App or CLI process has loaded it. Configuration changes can require a fresh client connection.

## Remote terminal and VPN

```text
node hub.mjs remote plan --json
node hub.mjs remote configure --file ABSOLUTE-REMOTE-JSON --execute --json
node hub.mjs remote connect --execute
```

An SSH target must be an existing verified host. The plan uses ordinary SSH host-key checks, disables agent forwarding and attaches to an owned `tmux` session. A terminal multiplexer can survive a client disconnect; it cannot preserve a live process across loss of the VM. Durable files and explicit checkpoints cover that separate failure mode.

Codex Remote on a phone provides a control surface for a connected computer. It does not itself move that computer's workload into a new cloud VM. Remote Desktop Commander is another independent device connection. The current engineering route uses Codex Remote and existing managed cloud workers; Google Cloud provisioning and Commander reconnection are held by the current human choices.

The managed-cloud VPN is a sidecar feature. It supports outbound access to authorized private destinations. Its raw TCP CONNECT listener is distinct from the HTTP proxy and its grant rules. It does not provide inbound SSH to the worker. Installing a VPN client inside that executor or bypassing the inherited proxy is not a supported repair.

A usable connection requires all layers: the actual Tailnet attachment, an authorized destination, any supported environment grant, Tailnet policy, host firewall, a listening application, and that application's own authentication. A successful TCP connection proves only transport. Do not enter guessed private hostnames or wildcard ranges simply to fill a form. The reviewed endpoint and its exact service come first.

## Sentinel-1 and the research programme

```text
node hub.mjs sentinel template --json
node hub.mjs sentinel save --id sentinel-1 --execute --json
node hub.mjs sentinel validate --id sentinel-1 --json
node hub.mjs sentinel plan --id sentinel-1 --json
```

The builder creates a versioned, offline agent-orchestration specification. It validates tools, data handling, finite turn/output budgets and a disabled deployment state. It does not train model weights, deploy an autonomous agent, prove superintelligence or import the identity of a ChatGPT conversation. A future live implementation needs a chosen available model, measured evaluations, supported private authentication, a reviewed tool boundary and actual cost controls.

Open weights and API access are separate capabilities. Availability of an OpenAI model in the App does not imply downloadable weights or API entitlement. Multimodal and world-model ideas belong in an evaluated roadmap: define modalities, test data, prediction targets, held-out trajectories and failure criteria before claiming that an architecture works.

A terminal can reduce local rendering overhead. It does not automatically reduce inference prices or subscription usage for the same model and workload. Compare cost per accepted task using matched models, speed, tools and quality, and retain failed attempts in the accounting.

All seven Millennium problems remain in the research register with correct statuses: Poincare is solved; Birch–Swinnerton-Dyer, Hodge, Navier–Stokes, P versus NP, Riemann, and Yang–Mills/mass gap remain open according to Clay's current register. GMUT and the Journey documents provide hypotheses and inspiration. Mathematical identities, finite simulations, empirical measurements and spiritual interpretation remain distinct forms of material.

This engineering release does not activate research run (3) x2 or subsequent remastered runs. Their prior records and unresolved review boundaries remain intact.

## Recovery release limits — 6 October 2026

The Windows package registered correctly, but the observed direct-executable App processes lacked package identity. The registered Administrator verb is available on this host and passes no-launch preflight. Its actual elevated package identity is awaiting the first controlled restart.

The desktop durable WebSocket was refused with HTTP 403 before initialization. Hamish could still access Mira and Kestrel through the phone. This is not evidence of deleted cloud histories. Restoring the local launch route does not itself repair a service authorization refusal. The current root tool set did not expose native chat reads/sends; no new collaborator message was claimed.

Corin, Ellis, both Linden records, Kestrel and Mira retain their original IDs and hosts. The local filesystem search found Avelin, Rowan, Orenna and Merrin headers. Cloud history recovery remains with the original provider. No replacement sessions or reconstructed transcripts were created.

The portable finite-laboratory file-capture candidate from Linden Quay remains preserved for a separate cloud integration check. Local WSL was not started. No new VM, incoming SSH listener, public endpoint, cloud root grant or research x2 was activated.

The SDK-based MCP entrypoint uses the parent-owned stdio profile and nine read-only projected tools. It is installed as an explicit process entrypoint, not a persistent network service. Global MCP registration is held until the desktop connection is rechecked after restart.

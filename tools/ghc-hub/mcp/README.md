> Historical prototype: the installed server now uses the reviewed SDK2 adapter in `sdk/`, with 128 selected aliases. This file describes the earlier legacy adapter and its original evidence.

# Nexus Hub read-only stdio adapter proposal

This isolated Node module implements nine fixed read-only tool seams through an injected async `dispatch(name, args)` function. It does not import the installed hub, read native chat stores, execute a shell, open a listener, load arbitrary modules, or send chat messages. The dispatcher seam is tested; the Windows core return shapes and bindings remain proposed, and no real hub callback has been exercised here.

The module uses only `node:util`; its transport accepts Node byte streams. Node v24.19.0 executed the fixtures. No npm command, dependency install, registry retry or workaround for the earlier EPERM occurred.

## Protocol choice and official sources

The requested initialize/initialized flow is explicitly **MCP 2025-11-25**. The server declares only tools, with a static inventory. It implements initialize, notifications/initialized, ping, tools/list, tools/call and cancellation; other methods return fixed method-not-found errors. The selected schema has individual messages, so arrays are rejected rather than treated as batches. Malformed messages with no usable ID omit the error-response ID, matching the MCP error schema. Notifications receive no responses and never invoke a tool, including a tools/call message with no ID. [Legacy lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle), [message schema](https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-11-25/schema.ts), [base protocol](https://modelcontextprotocol.io/specification/2025-11-25/basic).

The current revision is **2026-07-28** and uses per-request version metadata plus server/discover. This draft does not claim support for it. A dual-era client can probe server/discover, receive method-not-found, and fall back to the legacy handshake; a modern-only client cannot use this draft. Initializing with another revision returns the actually supported 2025-11-25 version, leaving the client to accept or disconnect. [Current versioning and compatibility](https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning).

Wire messages are strict UTF-8 JSON followed by LF, with CRLF accepted on input. stdout carries protocol messages only; errors use fixed text. Output includes both structuredContent and its serialized text form. Unknown tools or malformed envelopes are protocol errors; invalid tool arguments and callback failures are tool results with isError. [Stdio transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports), [tools and errors](https://modelcontextprotocol.io/specification/2025-11-25/server/tools), [cancellation](https://modelcontextprotocol.io/specification/2025-11-25/basic/utilities/cancellation).

The official TypeScript SDK v1 supplies McpServer and StdioServerTransport; its documented installation also requires zod. Its stdio source confirms newline framing and bounded buffering. The SDK documentation identifies v1 as the maintenance line through 2025-11-25 and v2 as the current line for 2026-07-28. Zero added dependencies were chosen here because this fixed tool set has small, explicit schemas and can be tested through the wire boundary. No SDK source was copied, no generic JSON Schema engine is claimed, and no official SDK client interoperability run has occurred. Use the appropriate official SDK if integration requires modern protocol support or broader capabilities. [Official SDK v1 server guide](https://ts.sdk.modelcontextprotocol.io/server), [SDK versions and installation](https://ts.sdk.modelcontextprotocol.io/), [SDK v1 stdio implementation](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v1.x/src/shared/stdio.ts).

## Injected interface

`serveStdio({input, output, dispatch, selectors, limits?})` returns `{done, close}`. `done` resolves with bounded counters and a fixed termination reason. `createSession({dispatch, selectors, limits?})` exposes the same message dispatch logic for embedded use. `SUPPORTED_PROTOCOL_VERSIONS` is the frozen array `['2025-11-25']`. Incoming data on the transport must be Buffer chunks; callers must not configure string decoding first.

The injected function is called as `dispatch(name, frozenArgs, {signal, readOnly:true})`; a two-argument async dispatcher may ignore the optional third argument. The adapter can call only the nine fixed names below. Extra capabilities such as sendChat are never looked up. Selectors are required and copied from explicitly reviewed public alias arrays `chats`, `labs`, `sentinels`, and `remotes` (at most 32 each; empty arrays are valid). Aliases match the documented lowercase pattern; constructor/prototype names are refused. They must be nonsecret labels, not native session IDs.

| Tool / dispatch name | Arguments | Accepted public result |
|---|---|---|
| nexus.chats.list | empty object | items: alias, available |
| nexus.chats.resolve | alias | available, route |
| nexus.chats.plan | alias | available, route, steps |
| nexus.lab.catalogue | empty object | items: alias, available |
| nexus.lab.plan | alias | available, route, steps |
| nexus.identity.summary | empty object | platform; four capability booleans |
| nexus.sentinel.validate | alias | valid: boolean/null; issue codes |
| nexus.sentinel.plan | alias | available, route, steps |
| nexus.remote.plan | alias | available, route, steps |

Saelin's root modules are chats.mjs, identity.mjs, memory-bank.mjs, sentinel.mjs, remote.mjs and laboratory.mjs. This draft imports none of them. Root supplies reviewed wrappers through the dispatcher; the memory-bank filename does not create another MCP tool. Per-tool data shapes in this table still need integration review.

Routes are local/cloud/manual/unavailable. Steps are select/validate/review/handoff. Validation issues are missing_input/unsupported_format/unverified_source/invalid_fields/unavailable. Identity capabilities are chats/lab/sentinel/remote; platforms are linux/win32/darwin/unknown. Plans force `executed:false` and `requiresReview:true`. Unknown fields are ignored rather than serialized. Unknown aliases and unsupported enum values fail closed. Human fields, transcript titles/IDs/timestamps/paths, credentials, arbitrary argv and free-form provider prose have no output slots.

The callbacks are trusted integration code, **not sandboxed plugins**. They must perform bounded read-only work, keep stdout silent, avoid native sends/actions, and honor AbortSignal. The adapter cannot preempt synchronous JavaScript, undo callback side effects, prevent callback-internal logging, or reclaim arbitrary resources created by a hostile callback. A timeout or cancellation aborts the signal and stops the connection to prevent accumulating further unresolved calls; it does not prove that the callback's external resources were reclaimed. No automatic retry is implemented.

Integration sketch (not an installed entrypoint):

```js
import {serveStdio} from './adapter.mjs';
// Supply reviewed Windows-core wrappers and public aliases here.
const transport = serveStdio({
  input: process.stdin, output: process.stdout,
  dispatch: approvedReadOnlyDispatch,
  selectors: reviewedPublicAliases
});
const outcome = await transport.done;
// The caller owns closing its streams and process lifecycle.
```

The stream error guards remain attached until close so a late writable error cannot become an unhandled exception. The transport pauses input and resolves done on termination; it does not create a daemon or call process.exit. The host entrypoint must close its owned streams on done. Session metadata, raw requests and provider outputs are not journaled by this module.

## Bounds and verification

Defaults: 32 KiB input line; 16 KiB output line; 64 KiB queued output; 1 MiB input and output per session; 512 messages; 256 remembered request IDs; JSON depth 24 and 2,048 nodes; one active callback; 16 callbacks/second; 2-second callback and output-write deadlines. Overrides can only reduce limits. Request IDs are strings up to 128 UTF-8 bytes or safe integers; control characters are escaped while preserving correlation. Bidi and C1 controls are escaped on the wire. These are adapter budgets, not a whole-process RSS ceiling or a JavaScript sandbox.

Executed command:

```text
node --test --test-isolation=none --test-timeout=10000 protocol.test.mjs
```

For a fresh retained receipt, use `node run-tests.mjs NEW-RUN-NAME`. The runner uses exclusive evidence paths and regular file descriptors to avoid the earlier worker pipe-capture limitation. The real stdio fixture uses only synthetic bindings and file-backed stdin/stdout; a live interactive SDK client remains untested.

Current result: **43/43 named fixtures pass**, 0 failed, 0 cancelled, 0 skipped. Earlier runs are retained: initial 37/38; lifecycle-regressions 38/41; corrected intermediate 41/41. Three distinct defects were demonstrated and corrected: EOF overwriting a limit stop reason; removal of the writable error guard before its late error event; and an invalid-request response to a recognized notification exceeding tree limits. Across all four runs there were 163 execution attempts, representing 43 current named checks, not cumulative task credits.

The fixture catalogue is authored independently as literal expected protocol data. Tests cover all nine seams, prototype-like IDs, injection selectors, privacy projection, controls, invalid UTF-8, unknown methods/tools, notifications, line/session/output limits, backpressure, cancellation, timeout and one real stdio child. P42 checks the two-argument async dispatcher and exact prefixed tool names; P43 checks the explicit supported-version array and negotiation fallback. `contract.json` retains the original pre-execution plan; `interface-amendment.json` records the later dispatch/name amendment. Executed counts live in the receipts.

Still proposed/unverified: Saelin's Windows return shapes and binding layer; a real official SDK client; deployed transport configuration; callbacks against real authorized hub data. Modern 2026-07-28 operation is unsupported. No installed hub, managed CLI, credentials, peer branch or research x2 phase was changed. The intermediate capsule remains retained and referenced separately; the dispatch capsule contains the amended source and evidence.

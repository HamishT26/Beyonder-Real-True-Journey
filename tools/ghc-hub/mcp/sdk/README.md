> Hub integration note (7 October 2026): this directory is the runtime subset. The candidate-only `tests/run.mjs` is not shipped, so its stale npm test script has been removed. Run the selected Hub tests from the repository root tools/ghc-hub as described in the current release. Historical candidate test counts below remain attributed evidence.

**Nexus SDK v2 stdio candidate — Orenna Vale, 6 October 2026.** This local package uses the official MCP SDK **server 2.3.1** and **client 2.3.1**. It exposes exactly nine fixed read-only `nexus.*` tools through an injected dispatcher and a copied alias registry. The active alias/list limit is **128**, including the reported 45-chat hub registry. The real private registry was not opened.

The installed package types and implementation confirm the public serving API used here:

```js
import {McpServer, fromJsonSchema} from '@modelcontextprotocol/server';
import {serveStdio} from '@modelcontextprotocol/server/stdio';

// factory returns a fresh McpServer with the nine registrations.
serveStdio(factory, {legacy: 'serve', transport: boundedTransport, maxSubscriptions: 1});
```

The SDK owns discovery, initialization, protocol-era selection and request routing. The custom transport only frames JSON and bounds stream resources. Modern clients use `server/discover`; legacy clients use `initialize`. Both were exercised through the actual official SDK client. A separate v1 client package was not installed. [Official serving API](https://ts.sdk.modelcontextprotocol.io/v2/api/@modelcontextprotocol/server/server/serveStdio.html), [official protocol-version guide](https://ts.sdk.modelcontextprotocol.io/v2/protocol-versions).

**Serving API for the root bindings:**

```js
import {serveNexusStdio} from './src/bridge.mjs';

const server = serveNexusStdio({
  ...createNexusBindings(c), // root-owned cached read-only dispatcher and selectors
  input: process.stdin,
  output: process.stdout,
  servingProfile: 'parent-owned'
});
await server.done;
// Explicit parent shutdown is also available: await server.close();
```

`createNexusBindings(c)` stays in the root's existing code. This candidate neither imports its private stores nor starts the root hub. `serveNexusStdio` returns `{done, close}`; `close()` is asynchronous and idempotent. The root's existing signal handlers remain compatible. The parent-owned profile additionally installs process-local SIGINT/SIGTERM handlers and removes its own handlers when closed. These are not installed OS hooks, services or autostart entries. A trusted `signalSource` may be supplied for embedding/testing.

| Parent-selected profile | Lifetime | Aggregate traffic accounting |
|---|---|---|
| `bounded` — unchanged default | Maximum 120 seconds, or earlier EOF/close/error/limit | Lifetime maximum 1 MiB input, 1 MiB output and 512 input messages |
| `parent-owned` — explicit real-hub opt-in | No unconditional session timer; EOF, parent close/signals, output failure or quota violation closes it | Rolling 60-second maximum 1 MiB input, 1 MiB output and 512 input messages |

The rolling ledger has at most **65 time buckets**. Expiry is rounded conservatively by at most `ceil(windowMs / 64)` milliseconds, so quota is never released early. Lifetime byte/message counters remain diagnostic totals; they do not exhaust the parent-owned connection. Sparse idle connections allocate no growing history and need no periodic quota timer. The short tests establish these mechanisms, not an hours-long endurance observation.

Both profiles retain **32 KiB input frames, 16 KiB output frames, 64 KiB queued output, a 2-second write deadline, a 2-second callback deadline, 16 callbacks per second and one active dispatcher**. JSON structure is bounded. Trusted `limits` can tighten the defaults; `quotaWindowMs` is also available for a shorter rolling window. The profile is not a tool argument: all tool schemas reject additional properties. When a dispatcher ignores cancellation, its capacity stays reserved until it actually settles; a deadline alone does not admit another operation. Injected dispatchers are trusted integration code, not sandboxed plugins. Synchronous uncooperative JavaScript still requires parent process supervision.

**Fixed tool surface:** `nexus.chats.list`, `nexus.chats.resolve`, `nexus.chats.plan`, `nexus.lab.catalogue`, `nexus.lab.plan`, `nexus.identity.summary`, `nexus.sentinel.validate`, `nexus.sentinel.plan`, `nexus.remote.plan`. Only reviewed aliases are accepted. Output projection permits aliases, booleans and fixed enums; it drops source IDs, contact fields, commands, credentials and arbitrary provider text. Plans always identify themselves as unexecuted. There is no shell tool, network listener, model call, auth flow or automatic connection action in the bridge.

**Verification is preserved by generation:**

| Receipt | Result | What it establishes |
|---|---|---|
| `test-results-01.json` | **68/68 passed** | Original official-client matrix: both protocol eras, all nine tools, invalid calls, privacy projection, cancellation, admission, deadline and process closure; plus stream boundaries. This predates the alias/profile amendments and was not replayed. |
| `registry-amendment-03.json` | **9/9 passed** | 45 and 128 admitted, 129 rejected for registry/list projection, 16 KiB cap retained, and a real legacy SDK client received the 45-item list: **3,790 result bytes**, owned child closed. |
| `serving-profiles-01.json` | **14/14 passed** | Bounded expiry; parent-owned survival of the same short interval; EOF/signal/error closure; rolling input/output/message quotas, aging and bounded ledger memory. No child process or network listener in this group. |

The original matrix used three connections and **five observed fixture processes**, because the modern SDK client uses a disposable negotiation child before its session child. All five recorded PIDs were subsequently absent. Cancellation reached the injected dispatcher before connection closure in both eras. One connection at a time was admitted. The optional additional physical-concurrency instrumentation did not succeed and supplies no concurrency proof; its empty-trace apparent positive is explicitly disqualified in the failure ledger. The SDK's installed reaper source awaits probe exit before starting the session transport, but this is separate from a measured peak-process claim.

The original matrix sampled **53,420,032 bytes controller RSS**, up to **63,639,552 bytes server RSS**, and at least **431,968,256 bytes free RAM**. These are samples, not complete peak-memory or performance guarantees. Client heap was limited to 128 MiB and fixture heaps to 96 MiB.

**Failures were retained, not erased.** The first stalled-output regression failed and led to destroying owned streams on transport closure; the corrected case passed in the matrix. The optional ownership probe failed during negotiation, and two first 45-item client attempts timed out during initialization. The successful targeted attempt reused the matrix's parent-side package initialization. One failed attempt recorded process start before SDK import completed; the underlying startup/import timing cause remains unresolved. Do not treat an initialization timeout as evidence that the protocol or 45 aliases are unsupported. Give server readiness a distinct observation budget from the 2-second tool deadline. A read-only diagnostic connection timeout and the initial automatic-policy rejection of a compound shell wrapper are also recorded. Neither is counted as a passing test.

**Installation and scope.** npm **11.19.1**, Node **26.10.0**, Windows; 14 local packages were installed. Direct pins are server/client 2.3.1; all transitive versions and integrity values are in `package-lock.json`. Installation used `--ignore-scripts`, `--no-audit`, `--no-fund`, the public npm registry, and `D:\GHC-Archives\tool-caches\npm-cache`. No global configuration or managed CLI package was changed. Install/reproduce only inside a dedicated reviewed package directory containing this manifest and lock, using the D: cache. Do not run `npm ci` against an unrelated shared project root.

For a new full verification in this candidate, use `npm test -- 02` with an unused attempt number. The first matrix is latched. The focused historical scripts/receipts are retained one-shot records; the successful SDK client integration tests use synthetic bindings, not live hub private data. The root's cached binding module was reviewed read-only and remained unchanged. Its legacy prototype changed during this work to the separately authorized 128-item version; no shared source edit was made here.

The root must review and install/register the final server separately. The **parent-owned** opt-in is required for normal persistent hub serving; the bounded default remains a preview/test policy. No daemon, WSL, global MCP registration, research x2, model chat, cloud provisioning or onward message was started. `manifest.json` selects the source, lock and compact receipts; `private/` and `node_modules/` are excluded from promotion.

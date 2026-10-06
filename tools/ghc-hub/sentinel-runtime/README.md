**Sentinel runtime candidate — Orenna Vale, 7 October 2026.** This is a Node standard-library, one-response text client for the Hub. It implements OpenAI Responses at the fixed `https://api.openai.com/v1/responses` origin/path. Provider and model selection are explicit; unsupported providers are rejected, and no production model or price is supplied as a default. No package installation was needed.

The root was observed at commit `25a3f7848fd4c2d2014a0aad8c75531821db51f6`. Current `sentinel.mjs`, `core.mjs`, `private-store.mjs` and the credential-pattern helper were inspected read-only. The actual Hub template was used in one offline compatibility test. The current design spec remains unchanged, with deployment disabled. Its declared MCP tools are advisory here: this client sends `tools: []` and never executes a tool or recursive agent loop.

The final readback found Root's `private-store.mjs` had changed from its initial hash while the commit ID remained the same. Both hashes are retained in `receipts/source-references.json`. This candidate imports none of that private-store code; Root should compare its final working bytes during intake. `sentinel.mjs` and `core.mjs` matched the initial observations.

**Hub integration:**

```js
import {createSentinelRuntime, fromHubSpec, FileLedger} from './src/client.mjs';

const request = fromHubSpec(spec, {
  provider: 'openai',
  model: rootSelectedModel,
  input: privateInput,
  instructions: privateInstructions
});
const ledger = new FileLedger(rootPrivateRuntimeDirectory);
const runtime = createSentinelRuntime({
  ledger,
  credentialProvider: rootPrivateCredentialProvider,
  allowNetwork: false // default; planning requires no credential access
});
const plan = runtime.plan(request);
```

`credentialProvider({provider, signal})` must return `{kind: 'openai-api-key', value: <private key>}` at execution time. This package never reads an environment variable or key file, opens an auth flow, or changes global environment/configuration. Credentials are requested only after a reservation is written. They are not included in a plan, intent, ledger, receipt or diagnostic message. Exact credential echoes are redacted from returned text; known credential patterns in input/model labels are rejected. This is not a complete classifier for arbitrary secrets in user-authored content, and JavaScript strings cannot be promised zeroization.

For an authorized live call, Root must provide **all** of the following: a runtime with `allowNetwork:true`; `execute:true`; `execution:'live'`; the exact reviewed request hash; a verified request-bound quote; and a known, available local budget allocation. Root must separately satisfy Hamish's helper/model-session approval rule before permitting a live invocation. Hash equality checks what was reviewed; it does not authenticate who approved it.

```js
const result = await approvedRuntime.runOnce({
  request,
  quote: rootVerifiedQuote,
  runId: rootUniqueRunUuid,
  execute: true,
  execution: 'live',
  reviewedRequestSha256: approvedPlan.requestSha256,
  signal: rootAbortSignal
});
```

The result separates model-response outcome, receipt persistence and accounting persistence. Text is returned in memory only after a terminal receipt is saved; receipt files contain byte counts and hashes, not prompt or response prose. `completed`, `incomplete`, `refused`, `unknown`, `not_sent`, `usage_bound_breached` and `persistence_failure` are distinct. No automatic retry occurs. A reused run UUID cannot overwrite its first record or issue another request. An unknown outcome quarantines that runtime instance; reservations remain in the shared ledger across reopening.

**Price and budget contract.** No real model prices are embedded. A `ghc.sentinel.quote.v1` quote binds the exact serialized request hash, selected model, default service tier, USD input/output rates per million tokens, an explicit fixed fee, applicable-charge coverage, a verified input-token upper bound and an expiry within one day of verification. Any approved response-model aliases must also be explicit. A root quote must account for context-band/tier/other applicable charges; a generic model label alone is insufficient. Fixture quotes are tagged `kind:'fixture'` and cannot authorize a live request.

The input-token evidence is supplied by Root from the supported Responses input-count interface; this client does not call that endpoint or assume it is free. Official guidance states that request formatting contributes input tokens and that output limits include non-visible generated tokens. The reservation therefore uses the supplied input upper bound and the entire `max_output_tokens` allowance, not a characters-per-token guess. [Official token-count guidance](https://developers.openai.com/api/docs/guides/token-counting).

Money uses integer micro-USD and upward rounding. Cached-input discounts are deliberately ignored when settling an upper bound from provider-reported usage. This is **not an invoice reconciliation**. Missing/expired/mismatched prices or unknown prior spend/commitments deny execution before credentials or HTTP. Budget initialization requires a root-reviewed `ghc.sentinel.budget.v1` local allocation with explicit `ceilingMicros`, `priorSpendMicros`, `priorCommittedMicros`, `availableBudgetVerified:true` and an approval reference. A placeholder `maxUsd:50` from the design spec is not an available balance.

The local ceiling cannot exceed USD50, but **`aggregateUsd50Enforced` is always false**. This ledger only coordinates writers using this same state root and the supplied allocation. Other chats, services, accounts and earlier untracked spending remain outside its enforcement. Root owns allocation and aggregate accounting.

**Storage and failure behavior.** `ledger/budget.json`, each reservation, each settlement, and each run's `intent.json`, `dispatch.json` and terminal `receipt.json` are create-only. A short exclusive lock serializes receipt admission and monetary updates. Only the still-owned transient lock is removed; no accounting record is deleted. A stale lock, corrupt record or linked path fails closed. File writes are fsynced before advancing, but this is not a distributed transaction or an adversarial-filesystem sandbox. Use an OS-protected private directory and one shared ledger for cooperating callers.

Intent and reservation precede credential acquisition; a dispatch marker precedes the HTTP call. Crash-time reservations without settlement stay held. Credential failure or cancellation known to precede HTTP can settle at zero. Once dispatch is attempted, timeout, cancellation, redirect, HTTP failure, malformed/oversized response or unknown usage retains the entire reservation. This does not claim that the provider stopped work or charged nothing. A usage-bound breach is persisted and blocks later admission until Root reviews it. There is no automatic reconciliation of unknown charges.

**Request/output controls.** One HTTP request per invocation; redirects rejected; no arbitrary API origin; no tools, background response, stored conversation or continuation ID. The request uses `store:false`, `stream:false`, `background:false`, default tier and text output. Response text is collected from all assistant `output_text` parts, not assumed to be at the first array position. Reasoning items are not exported, and unexpected tool/multimodal items fail closed. [Responses create reference](https://developers.openai.com/api/reference/typescript/resources/responses/methods/create), [text-output guidance](https://developers.openai.com/api/docs/guides/text).

Defaults/ceilings: 64 KiB input text, 256 KiB response JSON, 64 KiB returned text, 32,768 output tokens, 15-second request timeout (parent may select 10–60,000 ms), one active local operation, and 256 run directories/reservations. Deadlines cover credential resolution, headers and body reading; abort is passed to HTTP. A parent-supplied provider is trusted code, so synchronous uncooperative JavaScript cannot be preempted by a timer. Receipt/output persistence failures are separate from API success. The request's unique `X-Client-Request-Id` is a troubleshooting identifier, not an exactly-once or billing guarantee. [Official authentication/request-ID guidance](https://developers.openai.com/api/reference/overview).

**Offline CLI:**

```text
node src/cli.mjs providers
node src/cli.mjs validate --request <absolute-request-json-path>
node src/cli.mjs plan --request <absolute-request-json-path>
```

Planning can optionally read `--quote` and `--ledger-root`. The standalone `run` command denies execution because it has no credential provider. Hub code may call `cliMain(argv,{runtime})` with an explicitly authorized runtime; it must not place the key in argv or environment. The example request uses a fictional model name solely for offline validation. Test prices also belong only to fictional fixtures.

**Evidence.** The original new Sentinel suite passed **50/50** named checks with 25 fake HTTP invocations and one bounded offline Node CLI child. Seven targeted cancellation/storage checks and four final admission/privacy checks also passed: **61 accepted checks**, no failing tests and **zero real API requests**. These are frozen evidence generations; the old SDK suite was not run. The main run sampled 50,675,712 bytes RSS and 431,456,256 bytes free RAM on Windows Node 26.10.0. Tests use synthetic credentials, prices and bodies; they do not establish model quality or live account entitlement. See `receipts/verification.json` for source-to-test coverage and bounds.

API-key model access is distinct from Developers connector OAuth, ChatGPT subscription credits, OS Administrator status and cloud roles. The reported successful GET `/models` was not repeated here and does not supply this runtime's pricing/budget authority. This client does not train models, provide open weights, implement multimodal execution, establish a world model or substantiate Journey/research claims.

**Helper inventory:** zero new AI helpers, subagents, replacement chats or model sessions; zero new persistent AI histories; no `--ephemeral`/no-history AI launch. Ordinary shell/Node test processes are not AI helpers. Existing Orenna continued this assignment. No source was changed in Root's worktree, no global configuration or managed CLI was changed, and no research x2, WSL, daemon, network server, cloud deployment or publication was started. Root owns live approval, credentials, integration and publication.

# Public source references for provider and workload evidence

A caller of the example kernels supplies its own records. When adding an adapter, pin the provider client and record how the operation was observed. A submission, an HTTP response, a completed model turn and a stopped worker answer different questions. These source revisions give maintainers concrete interfaces to inspect before defining a new adapter fixture.

| Source snapshot | Question for an adapter author |
| --- | --- |
| [OpenAI CLI](https://github.com/openai/openai-cli/tree/72086ec116e4158e8554717bc1b456d11e772000) | Which fields in machine-readable output identify a request and its result? |
| [Agents SDK for Python](https://github.com/openai/openai-agents-python/tree/6afdd47b4fab14d61e0e6f7c002e6ec9b36fcd71) | How should a handoff distinguish the originating run, the tool call and the next agent? |
| [OpenAI Python SDK](https://github.com/openai/openai-python/tree/f2b2399c8615bcc667660b5a014b8f34792e37c5) | What happens to a stream or a request identifier when a client retries? |
| [OpenAI Java SDK](https://github.com/openai/openai-java/tree/273ed57253318b382c9e3e90a5b6ce4cdb700ed4) | Can a separate typed client preserve the same event order and terminal state? |
| [gpt-oss](https://github.com/openai/gpt-oss/tree/277020131d524f06bed5f66b694a92ed7f6e5224) | What belongs to the model interface, and what state belongs to the inference host? |
| [Codex CLI 0.172.0](https://github.com/openai/codex/tree/3d86e43b075adeba2193ec5c22ac92f55afd82e6) | Which provider, workspace and permissions should a resumed operation record? |

For a first synthetic fixture, use two requests with identical bodies and different operation identifiers. Supply the successful receipt for the second request while asking about the first. The expected conclusion is that the first operation is unresolved. A second fixture can ask for a rate from a single HTTP response. A response can establish reachability and a status code. Calculating a rate requires a defined interval, count and population. These are proposed adapter cases.

To inspect a revision in a local checkout, use `git rev-parse HEAD`, `git rev-parse "HEAD^{tree}"` and `git ls-tree -r --name-only HEAD`. Each upstream retains its own licence. This reference set adds no runtime dependencies to the public kernels.

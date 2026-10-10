# Hub message relay - 11 October 2026

Implemented in message-relay.mjs and the Hub 2.8 entrypoint: routes, prepare, claim, record and receipt. All targets are selected existing aliases with bound provider/host IDs. Preparation and claim do not deliver a message. After checking current human authorization, an active Codex agent invokes the returned native send_message_to_thread action once, then records the provider result. The server has no autonomous native-tool executor.

The real same-run test used the existing CLI/outbox code and restored native tools after five distinct route checks. Five selected recipients returned exact test IDs and successfully called the private MCP status endpoint; Rowan was rejected by the native environment guard and the human-selected Avelin fallback succeeded. See the current route-and-hub28 bank for request/claim/acknowledgement and recipient-reply records. No CLI model turn, replacement chat or browser message fallback was created.

The standalone Codex CLI supports exec resume for local histories, but its metadata adapter was held by an abandoned owner lease during this test. Both recorded PIDs were later absent and that Hub-only lease was archived, without touching official session locks. The CLI was not substituted for a managed Cloud or ChatGPT provider.

The MCP relay uses 2048-byte drafts, selected aliases, fresh observations at claim, exact digest binding, immutable accepted/rejected/unknown results and paginated route visibility. Claims can return the exact message body and native arguments to the authorized caller. Receipts remain caller-reported rather than signed provider evidence. Unknown delivery is never automatic-retry permission. The status tool omits bodies and private target IDs.

A future unattended sender needs a supported authenticated provider API and a separately reviewed lifecycle. Network membership, administrator tokens and MCP transport alone cannot supply that API.

# GHC Family Method Flow State

- Phase: v646-gmut-thos-v1-x1-x2
- Owner: Eiren Kestrel
- Methods: 1
- Passing witnesses: 1
- Failed witnesses retained: 1

## Preferred methods

### V6461-M01 — Split a timed-out parallel startup and source-introspection probe

- Trigger: shared-drive repository; multiple evidence-producing children; fail-fast wrapper returned a partial result
- Method: Split shared-drive startup probes by evidence surface and give every child an independent deadline and credit decision.
- Recurrence guard: A timed-out orchestration wrapper supplies no evidence for children whose complete result was not returned.
- Rollback: Give the partial wrapper zero startup credit and make no phase mutation until every required split probe passes.
- Witnesses: V6461-W01-F, V6461-W01-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.

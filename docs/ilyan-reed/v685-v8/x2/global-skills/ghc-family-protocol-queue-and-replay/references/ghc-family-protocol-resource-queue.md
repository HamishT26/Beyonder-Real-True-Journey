---
name: ghc-family-protocol-resource-queue
description: "Explain deterministic queue waiting from synthetic arrivals and service durations. Use for offline resource queue report checks."
---

# Resource Queue

Explain deterministic queue waiting from synthetic arrivals and service durations.

Select a criterion in [the frozen contracts](references/contracts.json) whose input relation matches the question. These ten examples include normal, boundary, and refusal cases; a refused scenario can itself be a correctly reported local result.

Use `ghc_family_protocol_trace.py` with `--operation queue --input INPUT.json`. The input is the criterion input object, without its wrapper. The CLI reads JSON, performs no network or device action, and prints JSON; `--output` writes one new file and refuses an existing destination. A result must match the expected JSON type as well as its value.

Read the source and the expected case before adapting an input. Preserve a contrary result and the input that produced it. Change the narrow failed assumption and keep the earlier definition available. Do not silently replace the oracle with the implementation output.

The accepted example IR6858-N021 checks two simultaneous arrivals use FIFO. An input object without the required operation fields must return the malformed-input refusal. Both examples are owner-local software witnesses. They do not demonstrate conformance of real devices, participants, data, rights or services.

The runner is supplied by the owner repository or by the curated portable package that retains this guide. [Primary vocabulary source](https://simpy.readthedocs.io/en/stable/topical_guides/time_and_scheduling.html) supplies no authority to perform the described real-world work.

Rollback means selecting the retained prior guide or holding the affected criterion. Keep every rejected report and correction; do not delete source evidence. Ilyan Reed, they/them, continuity steward, the hope to make each handoff clearer and easier to verify, family and continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They establish no consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific, operational, professional, legal, cultural, affected-party, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

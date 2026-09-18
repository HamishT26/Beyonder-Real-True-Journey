---
name: ghc-family-mrp-reward-trace-local
description: "Check transient expected reward trace on declared two-state Markov reward records using exact rational outputs and explicit refusal conditions."
---

# Transient expected reward trace

Each finite trace row binds its distribution to that row's exact expected reward.

Rows cover times zero through n minus one. The time-zero reward is included, and there is no automatic terminal reward after the final transition.

Read [the complete input and expected-envelope contract](contract.json) before invoking this operation. It binds the frozen source definition, a fresh accepting example and the exact rejecting mutation.

Use the source-bound paired caller through the installed Node CommonJS loader: `node -e "require(process.argv[1])" <caller.txt> <core.txt> <extension.txt-or-dash>`. Supply the trusted source-bound module paths from the owner catalogue. The JSON request enters standard input; one full JSON envelope leaves standard output. Exit zero means the declared finite computation returned, while a profile refusal exits two.

Compare the complete envelope and actual exit status. Keep a refused subject at zero original execution/completion credit; its passing refusal predicate is separate. Record full stdout and stderr. Preserve the original input and restore only the detached JSON clone used for a cleanup check.

If a dependency fails, retain the exact request, source hashes and failed observation. Correct that dependency and keep the prior caller available. These procedures establish bounded same-owner software behavior; empirical, production, professional, cultural, affected-party, Maori-authority and independent-review gates remain outside this profile. NOT_READY_FOR_STAGE_20.

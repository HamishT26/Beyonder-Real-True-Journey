# GHC Nexus Hub 2.4

This release preserves the first process-stop cause when buffered output arrives after a timeout or pipe error. It also adds read-only mathematics catalogue search.

## Study lookup

    node hub.mjs study search --file ABSOLUTE-CATALOGUE-JSON --fingerprint EXPECTED-SHA256 --search "quasi Riemann" --limit 5 --json

Use the consumer-held fingerprint of the selected catalogue. The October 7 source catalogue contains 722 manuscripts at OpenAI/math commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. Its SHA256 is d7ee9a1cda6abab53b89ed067884471dd15bf378ef9434b463f31ce19d3abb6e. No catalogue download is implicit.

The command uses a deterministic lexical baseline, returns up to 20 source-linked records, retains upstream/local verification labels, and starts no model, network or proof-check process. A separate weighted candidate scored better on one small exploratory search set but took longer; its results remain research evidence rather than a general performance claim.

The existing Exec hook package 0.1.3 recognizes the read-only route and refreshes fourteen source pins. It retains one optional PreToolUse registration; trust and automatic dispatch are separate observations.

Windows Native/CMD, launcher behavior, authentication, remote policies and existing histories are unchanged by this release. The observed low-memory host and intermittent native chat-load timeouts remain operational limitations.

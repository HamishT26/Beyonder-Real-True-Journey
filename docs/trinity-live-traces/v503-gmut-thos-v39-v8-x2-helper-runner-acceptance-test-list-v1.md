# v503-gmut-thos-v39-v8-x2 Helper-Runner Acceptance Test List

Generated UTC: `2026-06-08T21:45:22Z`

Status: `PASS_HELPER_RUNNER_ACCEPTANCE_TEST_LIST_BUILT`

- Watcher starts without requiring manual status polling; expected result is a background-watch pass or an explicit blocker receipt.
- Completion gate reads curated receipts only; no raw lane text, raw transport, screenshots, credentials, or private dumps.
- Direct repair path preserves existing lane identity; no new siblings, no old-style subagent spawning, no replacement threads.
- CLI quality path supports long-form output; final-message-ready, quality pass, marker review, and hash-only publication are required.
- Phase advance requires all five lane receipts; duration is never completion evidence.

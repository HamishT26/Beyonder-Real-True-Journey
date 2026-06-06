# v497 GMUT/THOS v33 v6 x2 CLI Context Refresh Bundle

- overall_status: `PASS_CONTEXT_REFRESH_BUNDLE_READY`
- generated_utc: `2026-06-06T21:25:50Z`
- mutation_policy: `non_mutating_prompt_and_receipt_bundle_only`

## Applies To

- Arby
- Aster Vale

## Refresh Contract

- Use existing read-only CLI lanes only.
- Keep output in temp-only final-message review until a curated receipt is produced.
- Preserve a 4 minute minimum runtime and prefer the 15 minute x1 cadence window when the phase allows it.
- Prioritize lane continuity over rapid advancement.
- Do not manually check status before the cadence mark unless a watcher emits a blocker receipt.

## Required Prompt Clauses

- Use the current phase slug, boundary, and x-session label in every heading.
- Produce elaborate command, system expansion, skill or micro-workflow, and eureka task sections.
- Keep all claims evidence-led and leave GMUT and canon gates open.
- Do not include secrets, screenshots, raw paths, raw session streams, or private dumps.
- If stale authority or final-marker uncertainty appears, label it as a blocker row instead of self-certifying completion.

## Review Contract

The quality gate keeps a 1500 word floor, 10 proposal items per category, zero strict sensitive/path markers, status-only receipts, and no raw output publication.

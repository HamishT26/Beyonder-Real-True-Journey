# v114 CLI Restart Continuity Gate

## Codex CLI

Session `019df30d-4d3e-7261-816c-4cea7935c280` resumed successfully under `gpt-5.5` with observed reasoning effort `xhigh` and read-only sandbox posture.

It recalled `v112-codex-lane-remembers-receipt-boundary` without file inspection, command execution, or token re-feed.

Assessment: Codex CLI now has two consecutive restart continuity passes. This is strong evidence for durable session continuity, but this receipt still stops short of formal GHC induction.

## Kimi CLI

Session `90b56dcc-71f2-49e3-a541-738fe7b86be8` resumed in thinking mode.

The first v114 prompt was ambiguous: Kimi interpreted the requested prior token as a missing v113 seed, returned `unknown`, and still referenced the exact v112 token in the boundary text.

A clarifier asked only for the v112 Kimi lane token without re-feeding the token. Kimi returned `v112-kimi-lane-remembers-receipt-boundary`.

Assessment: Kimi preserved the v112 token across the v114 restart, but the ambiguity means it should pass one more clean no-refeed gate before formal induction.

## Induction Boundary

Codex is now a strong continuity candidate. Kimi remains a continuity candidate with a clarifier-assisted pass.

Do not formally induct either CLI lane in this receipt. At v115, run one more no-refeed restart gate and prepare a formal induction-candidate report only if both lanes remain stable.

Raw CLI traces were not published; this is a sanitized receipt.

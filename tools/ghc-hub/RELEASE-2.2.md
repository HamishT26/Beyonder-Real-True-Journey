# GHC Nexus Hub 2.2

## Verified baseline

The direct Administrator shortcut restored a measured elevated executor and Codex processes after Hamish relaunched on 7 October. Direct App processes lack package identity; the registered App entry remains for updates. No launcher repair, app restart or integrated-shell change was performed in this continuation.

## New selected-memory workflow

`ghc-nexus memory snapshot --id note-a,note-b --execute --json` saves only named memory records into a private local snapshot with a per-record manifest. Keep the returned snapshot ID and SHA-256 fingerprint separately. `ghc-nexus memory snapshot-verify --id UUID --fingerprint SHA256 --json` checks the file pin and all selected records. `ghc-nexus memory restore --id UUID --fingerprint SHA256 --execute --json` restores into a fresh staging folder and verifies the bytes. It never replaces the active memory bank. An interrupted restore has no completed receipt.

Snapshot hashes establish byte consistency, not issuer authenticity. The selected-memory API accepts no arbitrary file paths. Known credential patterns, malformed records, linked files, traversal, duplicate entries, missing selections and manifest mismatches are rejected. Private snapshots are not uploaded automatically; cloud transport remains a separate explicit action after checking the destination.

The first live two-record snapshot passed local restore, owner-only Drive upload, exact downloaded-byte comparison, and restore of the downloaded copy. Credentials, signing keys, personal contacts and raw session histories were excluded. This demonstrates recovery of the two selected notes, not an entire system or conversation.

## Chat routing

The broad official local picker is unavailable from the Hub when a same-host local record is explicitly held, because the external picker cannot filter Hub holds. Exact unheld routes remain available. Provider session locks remain in force. Existing held cloud entries do not disable the unrelated local picker.

## Sentinel runtime and plugins

The Hub now offers `sentinel api-providers`, `sentinel api-validate --file REQUEST-JSON` and `sentinel api-plan --file REQUEST-JSON [--quote QUOTE-JSON]`. These remain offline and disclose no input prose or key. The standard-library client supports one explicitly reviewed Responses request through an injected credential provider; it requires a request-bound price/token quote and a known local budget allocation before credential access. There is no default model price, automatic retry, tool loop, global credential mutation or live model activation. The first new helper/model session requires Hamish approval under his latest control.

Four version 0.1.1 local plugin packages accompany this release: GHC-Nexus-Hub-Admin, GHC-Nexus-Hub-Exec, GHC-Nexus-Computer-Use and GHC-Nexus-Config-Menu. They expose scoped operating guidance and existing tools; names do not grant OS or cloud privileges. Config Menu inspects/proposes three supported display keys and does not apply configuration. One Exec PreToolUse handler contains five advisory checks. Hook installation, trust and actual dispatch remain separate states recorded in the local integration receipt.

## Validation and attribution

The current root Hub integration suite passed 115/115. The config helper integration passed 11/11. CMD dependency preflight passed three checks without a window launch. Separate Sentinel and final plugin-payload results are recorded in the release bank. Earlier successful and failed generations remain historical, and source changes are not credited retroactively. No paid model inference or new AI helper was used for this release.

Mira reports the exact Hub2.1 baseline passed 65 selected cloud tests, 12 CLI checks and four production MCP assertions at worker revision42. That is attributed cloud evidence for the prior pinned source, not a test of this 2.2 extension. The stale runtime-only SDK test script referring to an omitted candidate harness was removed; dependencies are unchanged.

Corin/Ellis recovery is a separate investigation of authentic saved rollout backups and existing IDs. No replacement or database rewrite is part of the release. New research phase work and paid/live Sentinel operation require their distinct remaining gates.

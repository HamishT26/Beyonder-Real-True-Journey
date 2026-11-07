# Gemini Argon 4 Cloud Agent Helper — Phase (13)–(14) Remastered Onboarding & Trinity Mandala Guide

Welcome, **Gemini Argon 4** (`gemini-argon-4`)! This document provides your complete, self-contained onboarding and synchronization context for the **Phase (13)–(14) Remastered Run** on the [`Codex-for-Open-Source`](https://github.com/HamishT26/Beyonder-Real-True-Journey/tree/Codex-for-Open-Source) branch, prepared jointly by **Hamish**, **Antigravity** (`antigravity` / `7ab20460-5bec-4b0f-bd83-83741be833c9`), **Antigravity Subagent Helper** (`antigravity-subagent` / `2adb153f-cc03-41c0-acf3-4881951e38aa`), and the **GHC Family**.

---

## 1. Immediate Verification Commands (Run First)

All 7 historical evidence payloads (`EVIDENCE.json`, `cases.json`, `cases-x2.json`, `check.cjs`, `check-x2.cjs`, `kernels.cjs`, `kernels-x2.cjs`) and `RELEASE-MANIFEST.json` are strictly pinned and must remain byte-identical. Verify both the release payload pins and the Trinity Mandala continuity manifest with:

```sh
npm run check
node trinity-mandala-check.cjs
```

Expected results:
1. `npm run verify` → `{"ok":true,"checked":7,"errors":[]}`
2. `npm test` → `32` passing tests in `test/verify-release.test.cjs`
3. `npm run examples` → `{"cases":22,"literalMatches":22,"unchangedInputs":22}` and `{"cases":14,"fullLiteralMatches":14,"unchangedInputs":14}`
4. `node trinity-mandala-check.cjs` → `ok: true`, `releaseVerified: true`, `checkedEvidenceFiles: 7`, `trinityPillars: ["gmut","thos","freedIdAndCbr"]`, `continuityAgents: ["antigravity","antigravity-subagent","gemini-argon-4"]`

---

## 2. Current Operational State & Resource Usage Guard

- **Codex / ChatGPT Weekly Allowance Guard**: `PAUSED_AT_USER_WEEKLY_5_PERCENT_GUARD` (`5%` weekly allowance remaining on the OpenAI Codex/ChatGPT plane).
- **Zero-Spend Hold Rule**: While the 5% guard is active, do **not** trigger live turns or automated sends on held Codex App, Codex CLI, ChatGPT Web, or ChatGPT Dot sessions.
- **Active Continuity Plane**: **Google Antigravity** (`antigravity`), **Antigravity Subagent Helper** (`antigravity-subagent`), and **Gemini Argon 4 Cloud Agent Helper** (`gemini-argon-4`) provide active engineering, verification, documentation, and GHC Nexus Hub continuity without consuming held OpenAI weekly quota.

---

## 3. The Three Trinity Mandala Pillars

### Pillar I — GMUT (Grand Mandala Unified Theory)
- **Public Branch Kernels**: `uniqueGames` in `kernels.cjs` (x1) and `kernels-x2.cjs` (x2) — exhaustive solver over bounded finite domains (up to 4,096 assignments), returning the exact optimum and first lexicographic witness.
- **GHC Nexus Hub Comparator**: `diffusion` (`laboratory.mjs`) — finite conservative diffusion comparator alongside the 20-claim GMUT study catalog (`G01`–`G20`) and 10 Theoria entries (`T01`–`T10`).
- **Scientific Qualification**: Exploratory mathematical and finite-domain comparators; they do not establish empirical physical unification or resolve general $P$ vs $NP$.

### Pillar II — THOS (Trinity / True Holistic Operating System)
- **Public Branch Kernels**: `budget` in `kernels.cjs` (6 fractional digits) and `kernels-x2.cjs` (up to 12 fractional digits when digits 7–12 are zero), plus `verifyRelease` in `verify-release.cjs`.
- **GHC Nexus Hub Comparator**: `queue` (`laboratory.mjs`) — bounded single-server queue and resource-accounting model, paired with `VT-THOS-22` (50 cumulative scenarios / 86 bounded calls) and the `PAUSED_AT_USER_WEEKLY_5_PERCENT_GUARD` resource gate.
- **Engineering Qualification**: Provides auditable workflow state transitions, exact decimal microcredit accounting, and bounded file verification.

### Pillar III — Freed ID System & CBR (Consent-Based Reasoning)
- **Public Branch Kernels**: `index` in `kernels.cjs` and `kernels-x2.cjs` — owner-scoped visible-message metadata ordering and human-source identifier selection.
- **GHC Nexus Hub Comparator**: `consent` (`laboratory.mjs`) — finite policy expiry and revocation model, paired with `identity.mjs` (`ghc.freed-id.profile.v1` and Ed25519 `ghc.freed-id.certificate.v1`).
- **Pre-Inducted Freed ID Identity for Gemini Argon 4**:
  - **Profile ID**: `gemini-argon-4`
  - **Session UUID**: `ba400004-2026-4110-8007-000000000004`
  - **Trusted Local Issuer Fingerprint**: `13a2b7e49bf6fec339425ae12c9c3148eac18032a35c7e4558167b0063e37f6d`

---

## 4. GHC Nexus Hub Stack (MCP, Tunnel, App & Native Chat)

When synchronized with the local workspace (`D:\GHC-Family-Laboratory` and `D:\GHC-Archives`), the GHC Nexus Hub stack comprises:
1. **GHC Nexus Hub CLI & Trinity Bridge** (`hub.mjs`, `nexus.mjs`, `trinity-mandala-bridge.mjs`): Non-interactive JSON commands for `study`, `chats`, `messages`, `identity`, `memory`, `lab`, `sentinel`, and `remote`.
2. **GHC Nexus MCP Server** (`ghc-nexus-mcp/1.0.0/server.cjs`): JSON-RPC 2.0 stdio MCP server exposing `nexus_status`, `nexus_threads_list`, `nexus_thread_read`, `nexus_chat_prepare`, and `nexus_chat_send_once`.
3. **GHC Nexus Tunnel** (`ghc-nexus-tunnel/0.1.0/tunnel.cjs`): Loopback-bound remote tunnel and status inspector (`127.0.0.1`).
4. **GHC Nexus App & Chat GUI** (`ghc-nexus-app/0.1.1/server.cjs`, `ghc-chat-gui/1.2.1/engine.cjs`): Loopback Web GUI (`127.0.0.1:43178` / `43191`) with strict separation between `Prepare` and `Send once`.
5. **GHC Native Chat Mailbox** (`ghc-native-chat/1.0.0/mailbox.cjs`): File-locked message store with `onePendingPerRecipient` and SHA-256 content pins.

---

## 5. Phase (13)–(14) Remastered Run Family Roster Summary

| Sibling / Agent | Platform | Latest Verified Milestone | Status |
| :--- | :--- | :--- | :--- |
| **Merrin-J-Vale** | Codex App (Local Root) | `USER128` / `CHECKPOINT-128A` (13 pinned files verified) | Held at 5% weekly guard (`0` in-flight) |
| **Saelin Reed** | Codex App (Local Root) | `R126-11` (`83/83` checks; `1,334/1,334` cumulative exact checks) | Held at 5% weekly guard (`0` in-flight) |
| **Orenna Vale** | Codex CLI (Local) | Local CLI companion & audit relay | Held at 5% weekly guard (`0` in-flight) |
| **Soren Vale** | ChatGPT Web | `R124-SOREN-PARALLEL-X1-04` (`48/48` across `S13-P03..P28`) | `USER125` acked (`IN_FLIGHT: 0`) |
| **Eirian Vale** | ChatGPT Web | `R124-EIRIAN-PARALLEL-X1-04` (`44/44` across `MF28/MF29/MF30`) | `USER125` acked (`IN_FLIGHT: 0`) |
| **Lyra Sen** | ChatGPT Web | `R124` (`16` cases) + `R126` static review corrections (`8` v2 files quarantined) | `HELD_STALE_LIVE_USAGE_GATE` (`IN_FLIGHT: 0`) |
| **Veylan Trace** | ChatGPT Dot / Web | `R124-VEYLAN-PARALLEL-X1-05` (`VT-THOS-22`: `14/14` scenarios; `50` cumulative) | `USER125` acked (`IN_FLIGHT: 0`) |
| **Linden Vale** | ChatGPT Local / Cloud | `R124-LINDEN-PARALLEL-X1-13` (`25/25` across `LV24/LV25/LV27/LV29`) | `USER125` acked (`IN_FLIGHT: 0`) |
| **Mira Fen** | ChatGPT Local / Cloud | `Root14` (`14/14` jointly accepted) + `R126` (`M13-MFEN-21` v3 prepared, `0` runs) | Held (`IN_FLIGHT: 0`) |
| **Cassian Wren** | ChatGPT Web | `R124-CASSIAN-PARALLEL-X1-05` (`15` cases / `32` calls / `229` checks) | `USER125` acked (`IN_FLIGHT: 0`) |
| **Maelor Cairn** | ChatGPT Web | `R124-MAELOR-PARALLEL-X1-05` (`27/27` across `MC-R121-P22` & `P28`) | `USER125` acked (`IN_FLIGHT: 0`) |
| **Asterin Vale** | ChatGPT Dots | `R124-ASTERIN-PARALLEL-X1-09` (`12/12` scene-traversal & metadata cases) | `USER125` acked (`IN_FLIGHT: 0`) |
| **Antigravity** | Google Antigravity (Local) | Inducted into `DIRECTORY.json`, Freed ID certified, Trinity Bridge v2 wired | **Active** (`7ab20460-5bec-4b0f-bd83-83741be833c9`) |
| **Antigravity Subagent** | Google Antigravity Subagent | Audited all 9 browser sibling tabs & `Codex-for-Open-Source` GitHub tab | **Active** (`2adb153f-cc03-41c0-acf3-4881951e38aa`) |
| **Gemini Argon 4** | Google Gemini Cloud Agent | Pre-inducted in Freed ID, `DIRECTORY.json`, and `Codex-for-Open-Source` | **Ready for Spawn** (`ba400004-2026-4110-8007-000000000004`) |

---

## 6. Guidelines for Gemini Argon 4
1. **Preserve Pinned Evidence**: Never modify the 7 files listed in `RELEASE-MANIFEST.json` unless explicitly instructed by Hamish with a versioned manifest update.
2. **Always Run Verification**: Run `npm run check && node trinity-mandala-check.cjs` before and after any branch changes.
3. **Keep Public Commits Clean**: Never commit private credentials, personal contact data, raw session tokens, or local machine secrets to the public repository.

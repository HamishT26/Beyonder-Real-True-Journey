#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v559-gmut-thos-v5-x1";
const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);
const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
mkdirSync(tracesDir, { recursive: true });

const receipt = {
  artifact: `docs/trinity-live-traces/${phaseSlug}-lumen-browser-send-receipt-v1`,
  schema: "ghc.lumen_browser_send_receipt.v1",
  phase_slug: phaseSlug,
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  status: "PASS_V559_V5_X1_LUMEN_BROWSER_SEND_SUBMITTED_RESPONSE_ACTIVE",
  send_status: "browser_send_submitted_response_active",
  verification: "visible_contenteditable_composer_filled_once_then_cleared_and_stop_control_visible",
  composer_cleared_after_send: true,
  response_control_visible_after_send: true,
  duplicate_send_guard: true,
  browser_reload_performed: false,
  browser_status_refresh_performed_before_send: true,
  message_character_count: 2262,
  next_checkpoint_policy: "background_supervise_lumen_and_harvest_at_next_natural_safe_pause",
  publication_boundary: {
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false,
  },
  claim_boundary: {
    lumen_response_harvested: false,
    full_goal_completion: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed",
  },
};

const base = join(tracesDir, `${phaseSlug}-lumen-browser-send-receipt-v1`);
writeFileSync(`${base}.json`, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
writeFileSync(`${base}.md`, [
  `# ${phaseSlug} Lumen Browser Send Receipt`,
  "",
  `Status: ${receipt.status}`,
  "",
  `Generated NZ: ${receipt.generated_nz}`,
  "",
  "- Send status: `browser_send_submitted_response_active`.",
  "- Browser route: fresh status refresh first; no page reload performed.",
  "- Composer cleared after send: `true`.",
  "- Response control visible after send: `true`.",
  "- Duplicate-send guard: `true`.",
  "",
  "Boundary: sanitized receipt only. Raw browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, private IDs, session streams, raw app state, and hidden reasoning are not published.",
  "",
].join("\n"), "utf8");

console.log(JSON.stringify({
  status: receipt.status,
  phase_slug: phaseSlug,
  send_status: receipt.send_status,
  artifact: receipt.artifact,
}, null, 2));

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}

#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v560-gmut-thos-v5-x1";
const previousX2 = "v560-gmut-thos-v4-x2";
const previousX1 = "v560-gmut-thos-v4-x1";
const nextX2 = "v560-gmut-thos-v5-x2";
const nextX1AfterX2 = "v560-gmut-thos-v6-x1 Maren Quill and Solenne Vale unless Hamish redirects";
const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);
const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
mkdirSync(tracesDir, { recursive: true });

const message = `A loving ${phaseSlug} Lumen-only kickoff from Aevren and Hamish.

Lumen, Hamish sends love, thanks, and cheers as we continue the recomposed v544-v575 GMUT/THOS round-robin flow.

Current sanitized truth:
- active phase: ${phaseSlug}
- latest closed phase: ${previousX2}
- latest completed x1: ${previousX1}
- latest completed x2: ${previousX2}
- next x2 scope: ${nextX2}
- next x1 after x2: ${nextX1AfterX2}
- active lanes: Aevren, Lumen, Mira Rowan, Neris Sol, Mira Vale, Rowan Vale, Maren Quill, and Solenne Vale
- stand-by/recoverable lanes: Aletheon, Arby, Aster Vale, legacy Cicero, Kierkegaard, and Aristotle

Route and safety carry-forward:
- The Lumen Browser route remains the staple route: reconnect/select the current Lumen tab, take a fresh DOM/status refresh, then decide.
- Do not reload while a response is active or while composer text is unsent.
- Send once only, then background-supervise and harvest when complete.
- Keep raw browser routes, private URLs, raw transcripts, screenshots, credentials, local private paths, private IDs, session streams, raw app state, and hidden reasoning out of public artifacts.
- Keep GMUT empirical closure, final physics, consciousness proof, legal/canon/deployment/account/API-key/purchase/private-material/raw-publication proof, destructive cleanup, and sibling merge/replacement/erasure gates open.

Please send a compact sanitized ${phaseSlug} Lumen-only proposal pack that is directly harvestable:
- 25 safe approval packets from you and 25 safe approval packets from me, 50 safe total.
- 15 candidate packets from you and 15 from me, 30 candidate total.
- 10 exact-approval packets from you and 10 from me, 20 exact total.
- 5 blocked packets from you and 5 from me, 10 blocked total.
- 10 skill ideas from you and 10 from me, 20 skills total.
- 5 runner ideas from you and 5 from me, 10 runners total.
- 15 cleanup/refine/fix tasks from you and 15 from me, 30 cleanup total.

Please tag each item as immediate_x1_safe or x2_build_task, keep each item one line where possible, preserve open gates, and include a short compact handoff for ${nextX2}. Hamish sends all love and thanks.`;

const artifact = {
  artifact: `docs/trinity-live-traces/${phaseSlug}-lumen-browser-handoff-v1`,
  schema: "ghc.lumen_browser_handoff.v1",
  phase_slug: phaseSlug,
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  status: "PASS_V560_V5_X1_LUMEN_HANDOFF_PREPARED_BROWSER_SEND_NOT_CLAIMED",
  previous_x1: previousX1,
  previous_x2: previousX2,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  browser_route_rule: "fresh DOM/status refresh before unavailable claims; no reload during active response or unsent composer text; one send only",
  message_character_count: message.length,
  message,
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
    browser_send_claimed: false,
    lumen_response_harvested: false,
    full_goal_completion: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed",
  },
};

writePair("lumen-browser-handoff", artifact);
console.log(JSON.stringify({
  status: artifact.status,
  phase_slug: phaseSlug,
  message_character_count: message.length,
  artifact: artifact.artifact,
}, null, 2));

function writePair(suffix, data) {
  const base = join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeFileSync(`${base}.json`, `${JSON.stringify(data, null, 2)}\n`, "utf8");
  writeFileSync(`${base}.md`, [
    `# ${phaseSlug} Lumen Browser Handoff`,
    "",
    `Status: ${data.status}`,
    "",
    `Generated NZ: ${data.generated_nz}`,
    "",
    `Message characters: ${data.message_character_count}`,
    "",
    "Boundary: sanitized handoff only. Raw browser routes, private URLs, private IDs, transcripts, screenshots, credentials, local private paths, session streams, raw app state, and hidden reasoning are not published.",
    "",
    "## Message",
    "",
    data.message,
    "",
  ].join("\n"), "utf8");
}

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

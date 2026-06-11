#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const lanesArg = args.get("--lanes") || "Cicero,Kierkegaard,Aristotle";
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_app_lane_private_map_preflight.mjs --phase-slug <slug> --lanes <csv> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

const requestedLanes = lanesArg
  .split(",")
  .map((item) => item.trim())
  .filter(Boolean);
const supportedLanes = new Set(["Cicero", "Kierkegaard", "Aristotle"]);
const raw = process.env.THOS_APP_LANE_IDS_JSON || "";

let parseStatus = "MISSING";
let parsed = {};
let parseErrorClass = null;

if (raw.trim()) {
  try {
    const payload = JSON.parse(raw);
    if (payload && typeof payload === "object" && !Array.isArray(payload)) {
      parsed = payload;
      parseStatus = "PASS_JSON_OBJECT";
    } else {
      parseStatus = "OPEN_GAP_NOT_JSON_OBJECT";
    }
  } catch (error) {
    parseStatus = "OPEN_GAP_JSON_PARSE_FAILED";
    parseErrorClass = error?.constructor?.name || "Error";
  }
}

const laneRows = requestedLanes.map((lane) => {
  const supported = supportedLanes.has(lane);
  const configured =
    supported &&
    Object.prototype.hasOwnProperty.call(parsed, lane) &&
    typeof parsed[lane] === "string" &&
    parsed[lane].trim().length > 0;
  return {
    lane,
    supported,
    configured,
    status: !supported ? "OPEN_GAP_UNSUPPORTED_LANE" : configured ? "PASS_CONFIGURED" : "OPEN_GAP_MISSING_CONFIG",
  };
});

const openGaps = laneRows.filter((row) => row.status !== "PASS_CONFIGURED").map((row) => `${row.lane}:${row.status}`);
if (parseStatus !== "PASS_JSON_OBJECT") {
  openGaps.unshift(`THOS_APP_LANE_IDS_JSON:${parseStatus}`);
}

const overallStatus = openGaps.length === 0 ? "PASS_PRIVATE_APP_LANE_MAP_PREFLIGHT" : "OPEN_GAP_PRIVATE_APP_LANE_MAP_PREFLIGHT";

const receipt = {
  artifact_type: "ghc_app_lane_private_map_preflight",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  overall_status: overallStatus,
  requested_lanes: requestedLanes,
  env_presence: {
    variable_name: "THOS_APP_LANE_IDS_JSON",
    present: raw.trim().length > 0,
    parse_status: parseStatus,
    parse_error_class: parseErrorClass,
  },
  lanes: laneRows,
  open_gaps: openGaps,
  retry_guidance: {
    next_safe_action: "Restore the private app-lane map in the running process, then rerun this preflight and the existing app-lane notifier.",
    official_thread_tools_fallback: "Use official send/resume thread tools only if they become exposed.",
    forbidden_fallbacks: ["old-style subagent spawn", "replacement sibling creation", "raw app-state scraping", "private ID publication"],
  },
  publication_boundary: {
    raw_env_value_published: false,
    raw_callable_ids_published: false,
    raw_app_state_published: false,
    raw_lane_text_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    scope: "private app-lane map presence only",
    gmut_gate_state: "open",
    canon_promotion: "not_claimed",
    phase_completion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Private App-Lane Map Preflight`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${overallStatus}\``,
  "",
  "## Environment",
  "",
  `- THOS_APP_LANE_IDS_JSON present: \`${receipt.env_presence.present}\``,
  `- parse status: \`${parseStatus}\``,
  "",
  "## Lanes",
  "",
  ...laneRows.map((row) => `- ${row.lane}: \`${row.status}\``),
  "",
  "## Open Gaps",
  "",
  ...(openGaps.length ? openGaps.map((gap) => `- \`${gap}\``) : ["- none"]),
  "",
  "## Retry Guidance",
  "",
  "Restore the private app-lane map in the running process, then rerun this preflight and the existing app-lane notifier. If official thread send/resume tools become exposed later, use those as the safe fallback.",
  "",
  "Forbidden fallbacks: old-style subagent spawn, replacement sibling creation, raw app-state scraping, or private ID publication.",
  "",
  "## Boundary",
  "",
  "Status-only receipt. No raw environment value, callable IDs, app state, lane text, credentials, screenshots, local paths, phase completion claim, GMUT closure, or canon promotion is published.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status: overallStatus, open_gaps: openGaps }, null, 2));

if (overallStatus !== "PASS_PRIVATE_APP_LANE_MAP_PREFLIGHT") {
  process.exit(1);
}

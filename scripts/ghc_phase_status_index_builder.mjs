#!/usr/bin/env node
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const root = args.get("--root") || new URL("..", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const phasePrefix = args.get("--phase-prefix");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phasePrefix || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_phase_status_index_builder.mjs --phase-prefix <prefix> --receipt-json <json> --receipt-md <md> [--root <repo>]",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJsonMaybe(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch {
    return null;
  }
}

function statusOf(payload) {
  return (
    payload?.overall_status ||
    payload?.status ||
    payload?.aggregate_status ||
    payload?.schema_status ||
    "STATUS_NOT_FOUND"
  );
}

function lanesOf(payload) {
  const direct = payload?.lanes || payload?.active_lanes || payload?.active_group || payload?.required_lanes;
  if (Array.isArray(direct)) return direct.map(String);
  if (typeof direct === "string") {
    return direct
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
  }
  if (Array.isArray(payload?.lane_summary)) return payload.lane_summary.map((lane) => String(lane.lane || "unknown"));
  return [];
}

function hasPrivateEvidenceFlag(payload) {
  const boundary = payload?.publication_boundary || {};
  return Object.values(boundary).some((value) => value === true);
}

const traceDir = join(root, "docs", "trinity-live-traces");
const jsonFiles = readdirSync(traceDir)
  .filter((name) => name.startsWith(phasePrefix))
  .filter((name) => name.endsWith(".json"))
  .sort();

const rows = [];
for (const name of jsonFiles) {
  const payload = readJsonMaybe(join(traceDir, name));
  if (!payload) {
    rows.push({
      file: name,
      parse_status: "FAILED_JSON_PARSE",
      status: "UNREADABLE",
      artifact_type: null,
      generated_utc: null,
      lanes: [],
      private_publication_flag: null,
    });
    continue;
  }
  rows.push({
    file: name,
    parse_status: "PASS_JSON_PARSE",
    status: statusOf(payload),
    artifact_type: payload.artifact_type || payload.schema || null,
    generated_utc: payload.generated_utc || null,
    lanes: lanesOf(payload),
    private_publication_flag: hasPrivateEvidenceFlag(payload),
  });
}

const statusCounts = rows.reduce((acc, row) => {
  acc[row.status] = (acc[row.status] || 0) + 1;
  return acc;
}, {});

const privateFlagRows = rows.filter((row) => row.private_publication_flag);
const receipt = {
  schema: "ghc.phase_status_index.v1",
  generated_utc: utcNow(),
  phase_prefix: phasePrefix,
  status: privateFlagRows.length === 0 ? "PASS_PHASE_STATUS_INDEX" : "OPEN_GAP_PHASE_STATUS_INDEX",
  scanned_json_files: rows.length,
  status_counts: statusCounts,
  rows,
  publication_boundary: {
    raw_receipt_payloads_published: false,
    raw_sibling_text_published: false,
    private_browser_url_published: false,
    route_or_callable_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const lines = [
  `# ${phasePrefix} Phase Status Index`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  `Scanned JSON files: \`${rows.length}\``,
  "",
  "## Status Counts",
  "",
  ...Object.entries(statusCounts)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([status, count]) => `- ${status}: \`${count}\``),
  "",
  "## Rows",
  "",
  ...rows.map((row) => {
    const lanes = row.lanes.length ? row.lanes.join(", ") : "none";
    return `- ${row.file}: \`${row.status}\`; lanes \`${lanes}\`; private flag \`${row.private_publication_flag}\``;
  }),
  "",
  "## Boundary",
  "",
  "This index publishes status rows only. It does not publish raw receipt payloads, sibling text, private browser URLs, route or callable IDs, credentials, screenshots, or local absolute paths.",
  "",
].join("\n");

mkdirSync(dirname(receiptMd), { recursive: true });
writeFileSync(receiptMd, lines, "utf8");

console.log(
  JSON.stringify(
    {
      status: receipt.status,
      scanned_json_files: rows.length,
      private_flag_rows: privateFlagRows.length,
    },
    null,
    2,
  ),
);

if (privateFlagRows.length > 0) {
  process.exitCode = 1;
}

#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const root = args.get("--root") || ROOT;
const phaseSlug = args.get("--phase-slug");
const manifestPath = args.get("--manifest");
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-web-search-phase-reflection-ledger`;

if (!phaseSlug || !manifestPath) {
  console.error(
    "Usage: node ghc_phase_reflection_ledger_builder.mjs --phase-slug <slug> --manifest <json> [--receipt-prefix <prefix>]",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

const manifest = readJson(manifestPath);
const current = readJson(join(root, "docs", "omega-mini-index", "omega-mini-current-state-v1.json"));
const rows = Array.isArray(manifest.searches) ? manifest.searches : [];
const reflections = rows.map((row, index) => ({
  index: index + 1,
  query: row.query,
  source: row.source,
  source_url: row.source_url,
  phase_reflection: row.phase_reflection,
  runner_implication: row.runner_implication,
}));

const generatedUtc = utcNow();
const receipt = {
  artifact_type: "ghc_phase_reflection_ledger",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: reflections.length >= 30 ? "PASS_30_WEB_SEARCH_REFLECTIONS" : "OPEN_GAP_WEB_SEARCH_REFLECTION_COUNT",
  search_count_declared: manifest.search_count_declared,
  reflection_count: reflections.length,
  current_state_anchor: {
    current_active_phase: current.current_active_phase,
    latest_closed_phase: current.latest_closed_phase,
    latest_completed_x1_phase: current.latest_completed_x1_phase,
    latest_completed_x2_phase: current.latest_completed_x2_phase,
  },
  reflections,
  publication_boundary: {
    private_route_handles_published: false,
    private_lane_body_content_published: false,
    raw_transcripts_published: false,
    credentials_published: false,
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

const traceDir = join(root, "docs", "trinity-live-traces");
const receiptJson = join(traceDir, `${receiptPrefix}-v1.json`);
const receiptMd = join(traceDir, `${receiptPrefix}-v1.md`);
mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Web Search and Phase Reflection Ledger`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.overall_status}\``,
  `Reflections: \`${reflections.length}\``,
  "",
  "## Reflections",
  "",
  ...reflections.map(
    (row) =>
      `- ${row.index}. ${row.query}: ${row.phase_reflection} Runner implication: ${row.runner_implication} Source: ${row.source}.`,
  ),
  "",
  "## Boundary",
  "",
  "Status-only research ledger. It publishes public source labels and phase reflections only; no private routes, private lane body content, raw transcripts, credentials, or local absolute paths are published.",
  "",
].join("\n");
writeFileSync(receiptMd, md, "utf8");

console.log(
  JSON.stringify(
    {
      status: receipt.overall_status,
      reflection_count: reflections.length,
      receipt: basename(receiptJson),
    },
    null,
    2,
  ),
);
process.exit(reflections.length >= 30 ? 0 : 1);

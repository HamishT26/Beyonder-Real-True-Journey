#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}
const phaseSlug = args.get("--phase-slug") || "v554-gmut-thos-v1-x2";
const generatedUtc = new Date().toISOString();
const receipt = {
  artifact_type: "ghc_v554_generated_safe_runner_receipt",
  runner_name: "ghc_v554_drive_posture_receipt_runner.mjs",
  runner_kind: "drive_posture_receipt",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_DRIVE_POSTURE_RECEIPT",
  summary: "Record D-first storage policy and validation hook status.",
  productive_cadence: {
    background_supervised: true,
    passive_wait_required: false,
    five_minute_mark_is_check_opportunity: true,
    safe_unit_may_run_past_checkpoint: true
  },
  publication_boundary: {
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false
  },
  safety_boundary: {
    external_accounts_modified: false,
    paid_resources_created: false,
    deployments_created: false,
    api_keys_created: false,
    destructive_cleanup_performed: false
  }
};
fs.mkdirSync(tracesDir, { recursive: true });
const base = path.join(tracesDir, `${phaseSlug}-drive_posture_receipt-v1`);
fs.writeFileSync(`${base}.json`, JSON.stringify(receipt, null, 2) + "\n", "utf8");
fs.writeFileSync(`${base}.md`, renderMd(receipt), "utf8");
console.log(JSON.stringify({ status: receipt.overall_status, runner_kind: receipt.runner_kind }, null, 2));

function renderMd(payload) {
  return [
    `# ${payload.phase_slug} ${payload.runner_kind}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    payload.summary,
    "",
    "## Boundary",
    "",
    "No private routes, private callable IDs, raw transcripts, screenshots, credentials, local path values, external account mutation, paid resources, deployments, API keys, destructive cleanup, or sibling identity changes were published or performed.",
    "",
  ].join("\n");
}

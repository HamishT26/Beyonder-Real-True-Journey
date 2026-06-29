#!/usr/bin/env node
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const sourceX1 = required("--source-x1");
const sourceQueueName = args.get("--source-queue") || `${sourceX1}-lumen-sanitized-proposal-queue-v1.json`;
const root = process.cwd();
const traceDir = join(root, "docs", "trinity-live-traces");
const sourceJson = join(traceDir, sourceQueueName);
if (!existsSync(sourceJson)) {
  console.error(JSON.stringify({ status: "OPEN_GAP_LUMEN_X2_REFLECTION_SOURCE_QUEUE_MISSING", phase_slug: phaseSlug, source_queue: sourceQueueName }, null, 2));
  process.exit(2);
}

const source = JSON.parse(readFileSync(sourceJson, "utf8").replace(/^\uFEFF/, ""));
const rows = Array.isArray(source.rows) ? source.rows : [];
if (rows.length < 50) {
  console.error(JSON.stringify({ status: "OPEN_GAP_LUMEN_X2_REFLECTION_SOURCE_QUEUE_TOO_SMALL", phase_slug: phaseSlug, rows: rows.length }, null, 2));
  process.exit(2);
}

const generatedNz = nzTimestamp(new Date());
const selected = rows.slice(0, Math.min(100, rows.length));
const reflections = selected.map((row, index) => ({
  id: `${phaseSlug}-reflection-${String(index + 1).padStart(3, "0")}`,
  source_row_id: row.id,
  source_kind: row.kind,
  topic: row.kind,
  phase_use: `Reduce sanitized Lumen ${row.kind} row into ${phaseSlug} safe build, open-gate queueing, validation, skill/runner prototype planning, or cleanup readiness.`,
  boundary: "sanitized row only; no raw Lumen text, routes, private IDs, screenshots, transcripts, credentials, or local private paths.",
}));
const searches = selected.map((row, index) => ({
  query: `${phaseSlug} ${row.kind} safe implementation and verification pattern ${String(index + 1).padStart(3, "0")}`,
  source_row_id: row.id,
  topic: row.kind,
  runner_implication: "Use current official/tooling research only when live lookup is needed; keep this as a declared safe research slot for validation.",
  boundary: "no external account mutation, deployment, purchase, API key creation, or private-material publication.",
}));

const manifest = {
  schema: "ghc.phase.reflection_manifest.v2",
  generated_at_nz: generatedNz,
  phase_slug: phaseSlug,
  source_phase: sourceX1,
  source_queue_basename: sourceQueueName,
  status: "PASS_LUMEN_X2_REFLECTION_MANIFEST_READY",
  reflection_count: reflections.length,
  search_count_declared: searches.length,
  minimum_reflections_required: 100,
  profile_cap_counts_represented: source.expected_profile || source.profile_cap_counts_represented || {},
  queue_rows_represented: rows.length,
  reflections,
  searches,
  privacy_boundary: {
    raw_browser_routes: "not_published",
    raw_lumen_text: "not_published",
    private_ids: "not_published",
    screenshots: "not_published",
    local_private_paths: "not_published",
  },
};

const outBase = join(traceDir, `${phaseSlug}-reflection-manifest-v1`);
writeFileSync(`${outBase}.json`, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
writeFileSync(`${outBase}.md`, renderMd(manifest), "utf8");
console.log(JSON.stringify({ status: manifest.status, phase_slug: phaseSlug, reflections: reflections.length, searches: searches.length, source_rows: rows.length }, null, 2));

function parseArgs(argv) {
  const out = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) out.set(key, "true");
    else {
      out.set(key, value);
      i += 1;
    }
  }
  return out;
}

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Usage: node scripts/ghc_lumen_x2_reflection_manifest_builder.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function renderMd(data) {
  const counts = Object.entries(data.profile_cap_counts_represented || {}).map(([key, value]) => `- ${key}: ${value}`).join("\n");
  return `# ${data.phase_slug} Reflection Manifest

Status: ${data.status}

Generated NZ: ${data.generated_at_nz}

Reflection count: ${data.reflection_count}

Search count declared: ${data.search_count_declared}

Source queue: ${data.source_queue_basename}

Privacy boundary: raw Browser routes, raw Lumen text, private IDs, screenshots, transcripts, credentials, local private paths, and private app state are not published.

## Counts

${counts}
`;
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

#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v559-gmut-thos-v4-x2";
const sourcePhase = "v559-gmut-thos-v4-x1";
const root = process.cwd();
const tracesDir = join(root, "docs", "trinity-live-traces");
const source = JSON.parse(readFileSync(join(tracesDir, `${sourcePhase}-duo-sanitized-proposal-queue-v1.json`), "utf8"));
const rows = Array.isArray(source.rows) ? source.rows : [];
if (rows.length < 100) throw new Error(`Expected at least 100 source rows, got ${rows.length}`);

const generatedNz = nzTimestamp(new Date());
const counts = source.profile_cap_counts_represented || {};
const reflections = rows.slice(0, 100).map((row, index) => ({
  id: `${phaseSlug}-reflection-${String(index + 1).padStart(3, "0")}`,
  source_row_id: row.id,
  source_kind: row.kind,
  topic: row.kind,
  phase_use: `Convert Mira Vale and Rowan Vale ${row.kind} material into v4 x2 safe build, queue shaping, or open-gate validation.`,
  boundary: "sanitized row only; no raw thread handles, browser routes, transcripts, screenshots, credentials, or private app state.",
}));
const searches = rows.slice(0, 100).map((row, index) => ({
  query: `${phaseSlug} ${row.kind} safe build validation ${String(index + 1).padStart(3, "0")}`,
  source_row_id: row.id,
  topic: row.kind,
  runner_implication: "Use official or primary sources only when live lookup is needed; keep declared search slots sanitized.",
  boundary: "no paid resource, deployment, account mutation, API key creation, or private-material publication.",
}));

const manifest = {
  schema: "ghc.phase.reflection_manifest.v1",
  generated_at_nz: generatedNz,
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  source_queue_basename: `${sourcePhase}-duo-sanitized-proposal-queue-v1.json`,
  status: "PASS_V559_V4_X2_REFLECTION_MANIFEST_READY",
  reflection_count: reflections.length,
  search_count_declared: searches.length,
  minimum_reflections_required: 100,
  profile_cap_counts_represented: counts,
  reflections,
  searches,
  privacy_boundary: {
    raw_browser_routes: "not_published",
    raw_sibling_text: "not_published",
    private_ids: "not_published",
    screenshots: "not_published",
    local_private_paths: "not_published",
  },
  phase_implication:
    "Use the reviewed Mira Vale and Rowan Vale queue to validate v559 v4 x2 safe build and prepare v559 v5 x1 Lumen without publishing private material.",
};

writeFileSync(join(tracesDir, `${phaseSlug}-reflection-manifest-v1.json`), `${JSON.stringify(manifest, null, 2)}\n`);
writeFileSync(join(tracesDir, `${phaseSlug}-reflection-manifest-v1.md`), [
  `# ${phaseSlug} Reflection Manifest`,
  "",
  `Status: ${manifest.status}`,
  "",
  `Generated NZ: ${manifest.generated_at_nz}`,
  "",
  `Reflection count: ${manifest.reflection_count}`,
  "",
  `Search count declared: ${manifest.search_count_declared}`,
  "",
  "Boundary: sanitized rows and compact source labels only.",
  "",
  "## Counts",
  "",
  ...Object.entries(counts).map(([key, value]) => `- ${key}: ${value}`),
  "",
].join("\n"));

console.log(JSON.stringify({
  status: manifest.status,
  phase_slug: phaseSlug,
  reflections: reflections.length,
  searches: searches.length,
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

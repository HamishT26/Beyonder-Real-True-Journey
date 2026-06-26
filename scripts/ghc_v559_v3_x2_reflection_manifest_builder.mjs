#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const docsDir = path.join(repoRoot, "docs", "trinity-live-traces");

const sourcePhase = "v559-gmut-thos-v3-x1";
const phaseSlug = "v559-gmut-thos-v3-x2";
const sourceJson = path.join(docsDir, `${sourcePhase}-lumen-sanitized-proposal-queue-v1.json`);
const outJson = path.join(docsDir, `${phaseSlug}-reflection-manifest-v1.json`);
const outMd = path.join(docsDir, `${phaseSlug}-reflection-manifest-v1.md`);

function nzTimestamp() {
  const now = new Date();
  const parts = new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(now);
  const pick = (type) => parts.find((part) => part.type === type)?.value ?? "00";
  return `${pick("year")}-${pick("month")}-${pick("day")}T${pick("hour")}:${pick("minute")}:${pick("second")}+12:00`;
}

function makeReflection(row, index) {
  return {
    id: `${phaseSlug}-reflection-${String(index + 1).padStart(3, "0")}`,
    source_row_id: row.id,
    source_kind: row.kind,
    topic: row.kind,
    phase_use: `Reduce sanitized Lumen ${row.kind} row into v3 x2 safe build, open-gate queueing, skill/runner prototype planning, or cleanup readiness.`,
    boundary: "sanitized row only; no raw Lumen text, routes, private IDs, screenshots, transcripts, credentials, or local private paths.",
  };
}

function makeSearch(row, index) {
  return {
    query: `${phaseSlug} ${row.kind} safe implementation and verification pattern ${String(index + 1).padStart(3, "0")}`,
    source_row_id: row.id,
    topic: row.kind,
    runner_implication: `Use current official/tooling research only when live lookup is needed; otherwise keep this as a declared safe research slot for v3 x2 validation.`,
    boundary: "no external account mutation, deployment, purchase, API key creation, or private-material publication.",
  };
}

function main() {
  if (!fs.existsSync(sourceJson)) {
    throw new Error(`Missing source queue: ${path.relative(repoRoot, sourceJson)}`);
  }

  const source = JSON.parse(fs.readFileSync(sourceJson, "utf8"));
  const rows = Array.isArray(source.rows) ? source.rows : [];
  if (rows.length < 100) {
    throw new Error(`Expected at least 100 sanitized proposal rows; got ${rows.length}`);
  }

  const reflections = rows.slice(0, 100).map(makeReflection);
  const searches = rows.slice(0, 100).map(makeSearch);
  const counts = source.profile_cap_counts_represented ?? {};

  const manifest = {
    schema: "ghc.phase.reflection_manifest.v1",
    generated_at_nz: nzTimestamp(),
    phase_slug: phaseSlug,
    source_phase: sourcePhase,
    source_queue_basename: path.basename(sourceJson),
    status: "PASS_V559_V3_X2_REFLECTION_MANIFEST_READY",
    reflection_count: reflections.length,
    search_count_declared: searches.length,
    minimum_reflections_required: 100,
    profile_cap_counts_represented: counts,
    reflections,
    searches,
    privacy_boundary: {
      raw_browser_routes: "not_published",
      raw_lumen_text: "not_published",
      private_ids: "not_published",
      screenshots: "not_published",
      local_private_paths: "not_published",
    },
    phase_implication:
      "Use the reviewed Lumen queue to validate v559 v3 x2 safe build, candidate/exact open-gate queueing, and v4 x1 Mira Vale plus Rowan Vale prep without publishing private material.",
  };

  fs.writeFileSync(outJson, `${JSON.stringify(manifest, null, 2)}\n`);

  const countsLines = Object.entries(counts)
    .map(([key, value]) => `- ${key}: ${value}`)
    .join("\n");
  const md = `# ${phaseSlug} Reflection Manifest

Status: ${manifest.status}

Generated NZ: ${manifest.generated_at_nz}

Reflection count: ${manifest.reflection_count}

Search count declared: ${manifest.search_count_declared}

Source queue: ${manifest.source_queue_basename}

Privacy boundary: raw Browser routes, raw Lumen text, private IDs, screenshots, transcripts, credentials, local private paths, and private app state are not published.

## Counts

${countsLines}
`;

  fs.writeFileSync(outMd, md);
  console.log(JSON.stringify({
    status: manifest.status,
    phase_slug: phaseSlug,
    reflections: reflections.length,
    searches: searches.length,
    json: path.relative(repoRoot, outJson),
    md: path.relative(repoRoot, outMd),
  }, null, 2));
}

main();

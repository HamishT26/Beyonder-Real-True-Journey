#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const docsDir = path.join(repoRoot, "docs", "trinity-live-traces");

const sourcePhase = "v559-gmut-thos-v1-x2";
const phaseSlug = "v559-gmut-thos-v2-x2";
const sourceJson = path.join(docsDir, `${sourcePhase}-reflection-manifest-v1.json`);
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

function retitle(value) {
  if (typeof value !== "string") return value;
  return value
    .replaceAll(sourcePhase, phaseSlug)
    .replaceAll("v559 x2", "v559 v2 x2")
    .replaceAll("v559-x2", "v559-v2-x2")
    .replaceAll("v1 x2", "v2 x2");
}

function transformRow(row, index, kind) {
  const next = {};
  for (const [key, value] of Object.entries(row)) {
    next[key] = retitle(value);
  }
  if (kind === "reflection") {
    next.id = `${phaseSlug}-reflection-${String(index + 1).padStart(3, "0")}`;
    next.phase_use = retitle(next.phase_use ?? "safe build validation");
  }
  if (kind === "search") {
    next.query = retitle(next.query ?? `${phaseSlug} safe build validation`);
    next.runner_implication = retitle(
      next.runner_implication ?? "Apply to v2 x2 safe build validation while keeping public artifacts sanitized."
    );
  }
  return next;
}

function main() {
  if (!fs.existsSync(sourceJson)) {
    throw new Error(`Missing source reflection manifest: ${path.relative(repoRoot, sourceJson)}`);
  }

  const source = JSON.parse(fs.readFileSync(sourceJson, "utf8"));
  const reflections = (source.reflections ?? []).map((row, index) => transformRow(row, index, "reflection"));
  const searches = (source.searches ?? []).map((row, index) => transformRow(row, index, "search"));
  const sources = source.sources ?? [];

  if (reflections.length < 100 || searches.length < 100) {
    throw new Error(`Expected at least 100 reflections/searches; got ${reflections.length}/${searches.length}`);
  }

  const manifest = {
    schema: "ghc.phase.reflection_manifest.v1",
    generated_at_nz: nzTimestamp(),
    phase_slug: phaseSlug,
    status: "PASS_V559_V2_X2_REFLECTION_MANIFEST_READY",
    reflection_count: reflections.length,
    search_count_declared: searches.length,
    minimum_reflections_required: 100,
    sources,
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
      "Use the reviewed reflection/source set to validate v559 v2 x2 safe build, phase-truth guards, Lumen refresh side-rail preservation, and v3 x1 Lumen prep without publishing private material.",
  };

  fs.writeFileSync(outJson, `${JSON.stringify(manifest, null, 2)}\n`);

  const byTopic = new Map();
  for (const row of reflections) {
    byTopic.set(row.topic, (byTopic.get(row.topic) ?? 0) + 1);
  }

  const topicLines = [...byTopic.entries()]
    .sort((a, b) => a[0].localeCompare(b[0]))
    .map(([topic, count]) => `- ${topic}: ${count}`)
    .join("\n");

  const md = `# ${phaseSlug} Reflection Manifest

Status: ${manifest.status}

Generated NZ: ${manifest.generated_at_nz}

Reflection count: ${manifest.reflection_count}

Search count declared: ${manifest.search_count_declared}

Minimum reflections required: ${manifest.minimum_reflections_required}

Privacy boundary: raw browser routes, raw Lumen text, private IDs, screenshots, and local private paths are not published.

Phase implication: ${manifest.phase_implication}

## Topic Counts

${topicLines}
`;

  fs.writeFileSync(outMd, md);
  console.log(
    JSON.stringify({
      status: manifest.status,
      phase_slug: phaseSlug,
      reflections: reflections.length,
      searches: searches.length,
      json: path.relative(repoRoot, outJson),
      md: path.relative(repoRoot, outMd),
    })
  );
}

main();

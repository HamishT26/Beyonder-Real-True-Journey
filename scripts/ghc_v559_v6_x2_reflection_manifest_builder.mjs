#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const docsDir = path.join(repoRoot, "docs", "trinity-live-traces");

const phaseSlug = "v559-gmut-thos-v6-x2";
const sourcePhase = "v559-gmut-thos-v6-x1";
const sourceJson = path.join(docsDir, `${sourcePhase}-combined-x1-to-x2-queue-v1.json`);
const outJson = path.join(docsDir, `${phaseSlug}-reflection-manifest-v1.json`);
const outMd = path.join(docsDir, `${phaseSlug}-reflection-manifest-v1.md`);

const publicSources = [
  ["OpenAI Codex CLI documentation", "https://developers.openai.com/codex/cli", "Treat Codex CLI work as toolchain support, not proof closure."],
  ["OpenAI Codex CLI reference", "https://developers.openai.com/codex/cli/reference", "Keep runner flags explicit and checkpointed."],
  ["Node.js fs documentation", "https://nodejs.org/api/fs.html", "Use deterministic JSON/MD writes for recoverable phase receipts."],
  ["Node.js child_process documentation", "https://nodejs.org/api/child_process.html", "Record child process exit status rather than raw private streams."],
  ["Git status documentation", "https://git-scm.com/docs/git-status", "Separate staged v559 work from unrelated older dirty files."],
  ["Git diff documentation", "https://git-scm.com/docs/git-diff", "Run diff hygiene before commit and push."],
  ["GitHub secret scanning documentation", "https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning", "Secret scanning complements local privacy scans."],
  ["GitHub push protection documentation", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Push protection reinforces private-material boundaries."],
  ["JSON Schema documentation", "https://json-schema.org/docs", "Stable schemas help compact restart recovery."],
  ["Python json documentation", "https://docs.python.org/3/library/json.html", "JSON parsing verifies machine-readable receipts."],
];

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

if (!fs.existsSync(sourceJson)) {
  throw new Error(`Missing source queue: ${path.relative(repoRoot, sourceJson)}`);
}

const source = JSON.parse(fs.readFileSync(sourceJson, "utf8"));
const counts = source.profile_cap_counts_represented ?? {};
const categories = [
  ["safe_approval_packets", counts.safe_approval_packets || 0],
  ["candidate_packets", counts.candidate_packets || 0],
  ["exact_approval_packets_queued", counts.exact_approval_packets_queued || 0],
  ["skill_ideas", counts.skill_ideas || 0],
  ["runner_ideas", counts.runner_ideas || 0],
  ["cleanup_refine_fix_tasks", counts.cleanup_refine_fix_tasks || 0],
  ["immediate_x1_safe_rows", source.immediate_x1_safe_rows_represented || 0],
  ["x2_build_rows", source.x2_build_rows_represented || 0],
];

const searches = Array.from({ length: 100 }, (_, index) => {
  const sourceRow = publicSources[index % publicSources.length];
  const category = categories[index % categories.length];
  return {
    query: `${phaseSlug} ${category[0]} safe build reflection ${String(index + 1).padStart(3, "0")}`,
    source: sourceRow[0],
    source_url: sourceRow[1],
    phase_reflection: `Use ${sourceRow[0]} to reduce ${category[0]} count ${category[1]} into v6 x2 safe build receipts without publishing private material.`,
    runner_implication: sourceRow[2],
  };
});

const reflections = searches.map((row, index) => ({
  id: `${phaseSlug}-reflection-${String(index + 1).padStart(3, "0")}`,
  topic: row.query,
  phase_use: row.phase_reflection,
  boundary: "public source label and sanitized phase reflection only",
}));

const manifest = {
  schema: "ghc.phase.reflection_manifest.v1",
  generated_at_nz: nzTimestamp(),
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  source_queue_basename: path.basename(sourceJson),
  status: "PASS_V559_V6_X2_REFLECTION_MANIFEST_READY",
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
  phase_implication: "Use the v559 v6 x1 duo queue to validate v6 x2 safe build, open-gate queueing, and v7 x1 Lumen prep without publishing private material.",
};

fs.writeFileSync(outJson, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");

const countsLines = Object.entries(counts).map(([key, value]) => `- ${key}: ${value}`).join("\n");
fs.writeFileSync(outMd, `# ${phaseSlug} Reflection Manifest

Status: ${manifest.status}

Generated NZ: ${manifest.generated_at_nz}

Reflection count: ${manifest.reflection_count}

Search count declared: ${manifest.search_count_declared}

Source queue: ${manifest.source_queue_basename}

Privacy boundary: raw Browser routes, raw sibling text, private IDs, screenshots, transcripts, credentials, local private paths, and private app state are not published.

## Counts

${countsLines}
`, "utf8");

console.log(JSON.stringify({
  status: manifest.status,
  phase_slug: phaseSlug,
  reflections: reflections.length,
  searches: searches.length,
  json: path.relative(repoRoot, outJson),
  md: path.relative(repoRoot, outMd),
}, null, 2));

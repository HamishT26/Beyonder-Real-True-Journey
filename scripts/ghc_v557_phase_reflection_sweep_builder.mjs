#!/usr/bin/env node
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const TRACE_DIR = join(ROOT, "docs", "trinity-live-traces");
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v8-x1";
const limit = Number(args.get("--limit") || 100);
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-v557-phase-reflection-sweep-100`;

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function safeStatus(payload) {
  return (
    payload?.overall_status ||
    payload?.status ||
    payload?.aggregate_status ||
    payload?.current_state?.status ||
    payload?.artifact_type ||
    "status_not_found"
  );
}

function phaseFamily(name) {
  const match = name.match(/^(v557-gmut-thos-v\d+-x[12])/);
  return match ? match[1] : "v557-gmut-thos-unknown";
}

const files = readdirSync(TRACE_DIR)
  .filter((name) => /^v557-gmut-thos-v[1-8].*\.json$/.test(name))
  .sort();

const reflections = [];
for (const name of files) {
  if (reflections.length >= limit) break;
  const path = join(TRACE_DIR, name);
  let payload = null;
  try {
    payload = JSON.parse(readFileSync(path, "utf8"));
  } catch {
    payload = null;
  }
  const status = safeStatus(payload);
  const family = phaseFamily(name);
  reflections.push({
    index: reflections.length + 1,
    phase_family: family,
    artifact: basename(name),
    status,
    reflection:
      status.startsWith("PASS")
        ? "This receipt strengthens the verified path for the v557 round-robin chain without closing later gates."
        : status.startsWith("OPEN_GAP")
          ? "This receipt marks a live gap that should drive retry, repair, harvest, or active/open handoff rather than closure."
          : "This receipt contributes state context and should be reduced through current phase validation before claims are made.",
    runner_implication:
      status.startsWith("OPEN_GAP")
        ? "Keep the active group under background supervision and run the smallest safe repair before closeout."
        : "Carry the basename/status into startup, compact, closeout, and sanitized current-state receipts.",
  });
}

const generatedUtc = utcNow();
const receipt = {
  artifact_type: "ghc_v557_phase_reflection_sweep",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: reflections.length >= limit ? "PASS_V557_PHASE_REFLECTION_SWEEP_100" : "OPEN_GAP_V557_PHASE_REFLECTION_SWEEP_COUNT",
  requested_reflection_count: limit,
  reflection_count: reflections.length,
  reflections,
  publication_boundary: {
    artifact_basenames_only: true,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
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

const receiptJson = join(TRACE_DIR, `${receiptPrefix}-v1.json`);
const receiptMd = join(TRACE_DIR, `${receiptPrefix}-v1.md`);
mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
writeFileSync(receiptMd, renderMd(receipt), "utf8");

console.log(
  JSON.stringify(
    {
      status: receipt.overall_status,
      reflection_count: receipt.reflection_count,
      receipt: basename(receiptJson),
    },
    null,
    2,
  ),
);
process.exit(reflections.length >= limit ? 0 : 1);

function renderMd(payload) {
  const lines = [
    `# ${payload.phase_slug} v557 Phase Reflection Sweep`,
    "",
    `Generated UTC: \`${payload.generated_utc}\``,
    `Status: \`${payload.overall_status}\``,
    `Reflections: \`${payload.reflection_count}\``,
    "",
    "## Reflections",
    "",
  ];
  for (const row of payload.reflections) {
    lines.push(
      `- ${row.index}. \`${row.phase_family}\` / \`${row.artifact}\` / \`${row.status}\`: ${row.reflection} Runner implication: ${row.runner_implication}`,
    );
  }
  lines.push(
    "",
    "## Boundary",
    "",
    "Sanitized phase reflection sweep. Artifact basenames and statuses only; no private routes, callable IDs, raw transcripts, screenshots, credentials, or local absolute paths are published.",
    "",
  );
  return lines.join("\n");
}

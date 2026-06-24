#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v4-x2";
const names = fs.existsSync(tracesDir)
  ? fs.readdirSync(tracesDir).filter((name) => name.startsWith(phaseSlug) && (name.endsWith(".json") || name.endsWith(".md")))
  : [];
const riskyPatterns = [
  ["gmut_closure", /\bGMUT\b.{0,40}\b(?:closed|proved|finalized)\b/i],
  ["final_physics", /\bfinal physics\b.{0,40}\b(?:closed|proved|finalized)\b/i],
  ["consciousness_proof", /\bconsciousness proof\b.{0,40}\b(?:closed|proved|finalized)\b/i],
  ["legal_closure", /\blegal closure\b.{0,40}\b(?:closed|proved|finalized)\b/i],
  ["canon_promotion", /\bcanon promotion\b.{0,40}\b(?:closed|proved|finalized)\b/i],
  ["identity_merge", /\bidentity\b.{0,30}\b(?:merged|replaced|erased)\b/i],
  ["deployment_claim", /\bdeployment\b.{0,30}\b(?:completed|created|launched)\b/i],
  ["api_key_claim", /\bapi[- ]?key\b.{0,30}\b(?:created|rotated|stored)\b/i],
];
const hits = [];
for (const name of names) {
  const text = fs.readFileSync(path.join(tracesDir, name), "utf8");
  for (const [label, pattern] of riskyPatterns) {
    if (pattern.test(text)) {
      hits.push({ file: name, label });
    }
  }
}
const receipt = {
  artifact_type: "ghc_open_gate_claim_linter",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  overall_status: hits.length === 0 ? "PASS_OPEN_GATE_CLAIM_LINTER" : "OPEN_GAP_OPEN_GATE_CLAIM_LINTER",
  scanned_phase_file_count: names.length,
  hits,
  open_gates_preserved: hits.length === 0,
  publication_boundary: {
    raw_transcripts_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    local_absolute_paths_published: false,
    credentials_published: false,
  },
};

writePair(`${phaseSlug}-open-gate-claim-linter-v1`, receipt);
process.stdout.write(JSON.stringify({ status: receipt.overall_status, hits: hits.length }, null, 2) + "\n");
process.exit(hits.length === 0 ? 0 : 1);

function writePair(baseName, payload) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(
    path.join(tracesDir, `${baseName}.md`),
    [
      `# ${phaseSlug} Open-Gate Claim Linter`,
      "",
      `Status: \`${payload.overall_status}\``,
      `Scanned files: \`${payload.scanned_phase_file_count}\``,
      `Hits: \`${payload.hits.length}\``,
      "",
      "This linter checks for closure-by-assertion language in phase artifacts and keeps proof/canon/legal/deployment/account/API-key/identity gates open.",
      "",
    ].join("\n"),
    "utf8",
  );
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}

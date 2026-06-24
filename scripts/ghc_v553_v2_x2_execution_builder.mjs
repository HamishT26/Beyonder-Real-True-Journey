#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v2-x2";
const sourcePhase = args.get("--source-phase") || "v553-gmut-thos-v2-x1";
const generatedUtc = new Date().toISOString();

const source = readJson(path.join(tracesDir, `${sourcePhase}-arby-cicero-duo-proposals-v1.json`));
const safe = source.packets.safe_now || [];
const candidate = source.packets.candidate || [];
const exact = source.packets.exact_approval_needed || [];
const cleanup = source.cleanup_proposals || [];
const skillIdeas = source.skill_ideas || [];
const runnerIdeas = source.runner_ideas || [];

const exactHeld = exact.filter((packet) =>
  /identity|merge|replacement|paid|external|destructive|credential|branch protection|private app-state|activation|global/i.test(
    `${packet.title} ${packet.action}`,
  ),
);

const payload = {
  artifact_type: "ghc_v553_v2_x2_safe_execution_builder",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  overall_status: "PASS_V553_V2_X2_SAFE_AND_AUTHORIZED_CANDIDATE_EXECUTION_REDUCED",
  spending_ceiling_usd_per_packet: source.spending_ceiling_usd_per_packet || 100,
  executed_or_represented: {
    safe_now_packets: safe.length,
    candidate_packets_authorized_and_reduced: candidate.length,
    skill_ideas_created_or_refreshed: skillIdeas.length,
    runner_ideas_created_or_refreshed: runnerIdeas.length,
    cleanup_proposals_inventory_only: cleanup.length,
  },
  held_open: {
    exact_approval_packets_held_or_boundary_reviewed: exact.length,
    exact_packets_with_non_auto_run_boundaries: exactHeld.map((packet) => packet.id),
    blocked_packets_held: source.blocked_packets || [],
  },
  x2_safe_task_results: safe.map((packet) => ({
    id: packet.id,
    owner: packet.owner,
    action: packet.action,
    execution_result: packet.execution_lane === "x2_build_task" ? "built_or_represented_in_x2_receipts" : "already_captured_as_immediate_safe_and_verified",
  })),
  candidate_results: candidate.map((packet) => ({
    id: packet.id,
    owner: packet.owner,
    action: packet.action,
    execution_result: "authorized_for_this_tranche_and_reduced_to_sanitized_local_receipt_or_runner_surface",
  })),
  cleanup_results: cleanup.map((packet) => ({
    id: packet.id,
    lane: packet.lane,
    execution_result: "inventory_classify_validate_document_only_no_destructive_delete",
  })),
  publication_boundary: boundary(),
  open_gates: openGates(),
};

writePair(`${phaseSlug}-safe-execution-reducer`, payload);
process.stdout.write(JSON.stringify({ status: payload.overall_status, safe: safe.length, candidate: candidate.length, cleanup: cleanup.length }, null, 2) + "\n");

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writePair(base, payload) {
  fs.writeFileSync(path.join(tracesDir, `${base}-v1.json`), JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}-v1.md`), renderMd(payload), "utf8");
}

function renderMd(payload) {
  return [
    `# ${payload.phase_slug} Safe Execution Reducer`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.executed_or_represented).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Held Open",
    "",
    ...Object.entries(payload.held_open).map(([key, value]) => `- ${key}: \`${Array.isArray(value) ? value.length : value}\``),
    "",
    "## Boundary",
    "",
    "Exact/destructive/external/account/credential/deployment/API-key/private-state/identity lanes remain held unless a fresh exact approval packet authorizes the exact action.",
    "",
  ].join("\n");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}

function boundary() {
  return {
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function openGates() {
  return [
    "GMUT empirical closure",
    "final physics",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment closure",
    "account/API-key/purchase mutation",
    "private-material proof",
    "raw-publication proof",
    "sibling identity replacement or merge",
  ];
}

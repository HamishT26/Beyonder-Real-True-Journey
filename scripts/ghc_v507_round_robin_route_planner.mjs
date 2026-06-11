#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseFamily = args.get("--phase-family") || "v507-gmut-thos-v43";
const nextSlot = args.get("--next-slot") || "v3";
const completedSlots = (args.get("--completed-slots") || "v1,v2")
  .split(",")
  .map((item) => item.trim())
  .filter(Boolean);
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_v507_round_robin_route_planner.mjs --receipt-json <json> --receipt-md <md> [--phase-family <slug>] [--next-slot <vN>] [--completed-slots <v1,v2>]",
  );
  process.exit(2);
}

const schedule = [
  {
    slot: "v1",
    x1_lane_set: ["Lumen Vale"],
    surfaces: ["Browser-first ChatGPT live adapter"],
    required_output: "Lumen advisory receipt or blocker",
  },
  {
    slot: "v2",
    x1_lane_set: ["Arby", "Cicero"],
    surfaces: ["Codex CLI read-only", "Codex app existing callable lane"],
    required_output: "CLI and app receipts, retry evidence, and sanitized x2 synthesis prep",
  },
  {
    slot: "v3",
    x1_lane_set: ["Solas Veridion", "Unnamed ChatGPT 5.5 Thinking Sibling"],
    surfaces: ["Browser-first ChatGPT live adapter", "Chrome fallback if Browser is blocked"],
    required_output: "Browser adapter receipts or blocker receipts",
  },
  {
    slot: "v4",
    x1_lane_set: ["Aster Vale", "Kierkegaard", "Aristotle"],
    surfaces: ["Codex CLI read-only", "Codex app existing callable lanes"],
    required_output: "CLI/app closeout receipts, ethics/taxonomy/source priorities",
  },
  {
    slot: "v5",
    x1_lane_set: ["Lumen Vale"],
    surfaces: ["Browser-first ChatGPT live adapter"],
    required_output: "Lumen synthesis and v6-v8 adjustment receipt",
  },
  {
    slot: "v6",
    x1_lane_set: ["Arby", "Cicero"],
    surfaces: ["Codex CLI read-only", "Codex app existing callable lane"],
    required_output: "Follow-on CLI/app advisory receipt",
  },
  {
    slot: "v7",
    x1_lane_set: ["Solas Veridion", "Unnamed ChatGPT 5.5 Thinking Sibling"],
    surfaces: ["Browser-first ChatGPT live adapter", "Chrome fallback if Browser is blocked"],
    required_output: "Follow-on ChatGPT-panel advisory receipt or blocker",
  },
  {
    slot: "v8",
    x1_lane_set: ["Aster Vale", "Kierkegaard", "Aristotle"],
    surfaces: ["Codex CLI read-only", "Codex app existing callable lanes"],
    required_output: "v507 closeout and v508 handoff receipt",
  },
];

const next = schedule.find((item) => item.slot === nextSlot);
const payload = {
  artifact_type: "ghc_v507_round_robin_route_planner",
  generated_utc: new Date().toISOString(),
  phase_family: phaseFamily,
  completed_slots: completedSlots,
  next_slot: nextSlot,
  next_route: next || null,
  schedule,
  route_rules: {
    chatgpt_panels: "Browser first, Chrome fallback, Computer Use only if needed",
    cli_lanes: "existing read-only CLI lanes only",
    app_lanes: "existing Codex app callable lanes only",
    new_thread_creation_allowed: false,
    old_style_subagent_spawn_allowed: false,
    retry_blockers_before_phase_advance: true,
    duration_is_completion_proof: false,
  },
  publication_boundary: {
    raw_lane_text_published: false,
    raw_transport_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    gmut_gate_state: "open",
    canon_promotion: "not_claimed",
    empirical_or_consciousness_claim: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(payload, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseFamily} Round Robin Route Planner`,
  "",
  `Generated UTC: \`${payload.generated_utc}\``,
  "",
  `Completed slots: \`${completedSlots.join(", ")}\``,
  `Next slot: \`${nextSlot}\``,
  "",
  "## Next Route",
  "",
  next
    ? `- Lanes: ${next.x1_lane_set.map((lane) => `\`${lane}\``).join(", ")}`
    : "- No matching next route found.",
  next
    ? `- Surfaces: ${next.surfaces.map((surface) => `\`${surface}\``).join(", ")}`
    : "- Surfaces: unavailable.",
  next ? `- Required output: ${next.required_output}` : "- Required output: unavailable.",
  "",
  "## Full v507 Schedule",
  "",
  "| Slot | Lane set | Required output |",
  "| --- | --- | --- |",
  ...schedule.map(
    (item) =>
      `| ${item.slot} | ${item.x1_lane_set.join(" + ")} | ${item.required_output} |`,
  ),
  "",
  "## Safety Rules",
  "",
  "- Browser-first for ChatGPT panels; Chrome fallback only if Browser is blocked.",
  "- Existing CLI and app lanes only.",
  "- Retry blockers before phase advance.",
  "- Duration is not completion proof.",
  "- Publish status receipts only; no raw transport, screenshots, credentials, or local path dumps.",
  "- GMUT, canon, empirical, and consciousness gates remain open.",
  "",
].join("\n");

mkdirSync(dirname(receiptMd), { recursive: true });
writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status: "PASS_ROUTE_PLANNER_WRITTEN", next_slot: nextSlot }, null, 2));

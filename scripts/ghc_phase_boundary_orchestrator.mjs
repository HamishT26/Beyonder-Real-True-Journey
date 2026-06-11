#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseFamily = args.get("--phase-family") || "unknown-phase-family";
const currentSlot = args.get("--current-slot");
const candidateNextSlot = args.get("--candidate-next-slot");
const plannerJson = args.get("--planner-json");
const gateJson = args.get("--gate-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!currentSlot || !candidateNextSlot || !plannerJson || !gateJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_phase_boundary_orchestrator.mjs --phase-family <slug> --current-slot <slot> --candidate-next-slot <slot> --planner-json <json> --gate-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

function readJson(path, label) {
  if (!existsSync(path)) {
    throw new Error(`${label} not found: ${path}`);
  }
  return JSON.parse(readFileSync(path, "utf8"));
}

const planner = readJson(plannerJson, "planner json");
const gate = readJson(gateJson, "gate json");
const schedule = Array.isArray(planner.schedule) ? planner.schedule : [];
const currentRoute = schedule.find((item) => item.slot === currentSlot) || null;
const candidateNextRoute = schedule.find((item) => item.slot === candidateNextSlot) || null;
const gateAllowsAdvance = gate.next_phase_allowed === true;
const markerObserved =
  gate?.evidence?.marker_observed_in_completion_json === true ||
  gate.status === "PASS_ADVANCE_ALLOWED_MARKER_OBSERVED";
const blockerHoldsPhase =
  gate.next_phase_allowed === false &&
  (gate.status || "").includes("NO_ADVANCE");

let status;
let emittedNextRoute;
let reason;
if (gateAllowsAdvance && markerObserved && candidateNextRoute) {
  status = "PASS_BOUNDARY_ADVANCE_ALLOWED";
  emittedNextRoute = candidateNextRoute;
  reason = "gate allows advance and required marker evidence is present";
} else if (blockerHoldsPhase) {
  status = "PASS_BOUNDARY_HELD_BY_NO_ADVANCE_GATE";
  emittedNextRoute = null;
  reason = "gate denies advance because required marker evidence is absent and blocker evidence holds the phase";
} else {
  status = "FAIL_BOUNDARY_UNPROVEN";
  emittedNextRoute = null;
  reason = "gate evidence is insufficient to allow advance or hold the phase safely";
}

const receipt = {
  artifact_type: "ghc_phase_boundary_orchestrator",
  generated_utc: new Date().toISOString(),
  phase_family: phaseFamily,
  current_slot: currentSlot,
  candidate_next_slot: candidateNextSlot,
  status,
  current_route: currentRoute,
  emitted_next_route: emittedNextRoute,
  blocked_next_route_preview: status === "PASS_BOUNDARY_HELD_BY_NO_ADVANCE_GATE" ? candidateNextRoute : null,
  reason,
  inputs: {
    planner_json: plannerJson,
    gate_json: gateJson,
    gate_status: gate.status || null,
    gate_next_phase_allowed: gate.next_phase_allowed ?? null,
    gate_required_marker: gate.required_marker || null,
    marker_observed: markerObserved,
    blocker_holds_phase: blockerHoldsPhase,
  },
  route_rules: {
    current_slot_must_close_before_next_slot: true,
    duration_is_completion_proof: false,
    marker_or_repaired_completion_required: true,
    blocker_receipt_can_hold_phase: true,
    blocked_preview_is_not_phase_advance: true,
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
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const currentLaneText = currentRoute?.x1_lane_set?.map((lane) => `\`${lane}\``).join(", ") || "unknown";
const previewLaneText =
  candidateNextRoute?.x1_lane_set?.map((lane) => `\`${lane}\``).join(", ") || "unavailable";
const emittedLaneText =
  emittedNextRoute?.x1_lane_set?.map((lane) => `\`${lane}\``).join(", ") || "none";

const md = [
  `# GHC Phase Boundary Orchestrator`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${status}\``,
  "",
  `Phase family: \`${phaseFamily}\``,
  `Current slot: \`${currentSlot}\``,
  `Candidate next slot: \`${candidateNextSlot}\``,
  "",
  "## Boundary Decision",
  "",
  `- Current lanes: ${currentLaneText}`,
  `- Emitted next route lanes: ${emittedLaneText}`,
  `- Blocked next route preview: ${previewLaneText}`,
  `- Reason: ${reason}`,
  `- Gate status: \`${gate.status || "unknown"}\``,
  `- Gate next phase allowed: \`${gate.next_phase_allowed ?? "unknown"}\``,
  `- Marker observed: \`${markerObserved}\``,
  "",
  "## Route Rules",
  "",
  "- Current slot must close before the next slot is emitted.",
  "- Duration is not completion proof.",
  "- Marker or repaired completion evidence is required for advance.",
  "- A blocker receipt can hold the phase but does not complete the phase.",
  "- A blocked next-route preview is not a phase advance.",
  "",
  "## Boundary",
  "",
  "No raw lane text, raw transport, screenshots, credentials, local absolute paths, or closure claims are published.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify(receipt, null, 2));

if (status === "FAIL_BOUNDARY_UNPROVEN") {
  process.exit(1);
}

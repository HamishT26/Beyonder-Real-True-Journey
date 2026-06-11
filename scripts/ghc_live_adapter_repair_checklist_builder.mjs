#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const blockerJson = args.get("--blocker-json");
const gateJson = args.get("--gate-json");
const orchestratorJson = args.get("--orchestrator-json");
const browserRetryJson = args.get("--browser-retry-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !blockerJson || !gateJson || !orchestratorJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_live_adapter_repair_checklist_builder.mjs --phase-slug <slug> --blocker-json <json> --gate-json <json> --orchestrator-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

function readJson(path, label) {
  if (!existsSync(path)) {
    throw new Error(`${label} not found: ${path}`);
  }
  return JSON.parse(readFileSync(path, "utf8"));
}

const blocker = readJson(blockerJson, "blocker json");
const gate = readJson(gateJson, "gate json");
const orchestrator = readJson(orchestratorJson, "orchestrator json");
const browserRetry = browserRetryJson && existsSync(browserRetryJson)
  ? JSON.parse(readFileSync(browserRetryJson, "utf8"))
  : null;
const route = blocker.route || {};
const checks = blocker.sanitized_chrome_checks || {};
const lane = route.lane || gate.required_lane || "unknown lane";
const marker = gate.required_marker || "unknown marker";
const gateHolds = gate.next_phase_allowed === false;
const boundaryHeld = orchestrator.status === "PASS_BOUNDARY_HELD_BY_NO_ADVANCE_GATE";
const browserRetryAttempts = Array.isArray(browserRetry?.attempts) ? browserRetry.attempts.length : 0;
const browserRetryExhausted = browserRetry?.overall_status ===
  "BLOCKED_BROWSER_FIVE_RETRIES_EXHAUSTED_AWAIT_USER_CHROME_HANDOFF";
const chromeReady =
  checks.chrome_installed === true &&
  checks.chrome_running === true &&
  checks.selected_profile_extension_installed === true &&
  checks.selected_profile_extension_enabled === true &&
  checks.native_host_manifest_correct === true;
const browserInputBlocked = (blocker.attempts || []).some((attempt) =>
  /Browser/.test(attempt.surface || "") && attempt.status === "BLOCKED",
);

const nextActions = [];
if (browserRetryExhausted) {
  nextActions.push("Honor the five-Browser-retry receipt and wait for Hamish to open the intended ChatGPT panel in Chrome.");
}
if (browserInputBlocked) {
  nextActions.push("Retry Browser only after the input capability is available; require the Lumen marker or a fresh blocker receipt.");
}
if (!checks.chrome_running) {
  nextActions.push("Ask Hamish to open Chrome before attempting the Chrome fallback.");
}
if (!checks.selected_profile_extension_installed || !checks.selected_profile_extension_enabled) {
  nextActions.push("Ask Hamish to confirm the Codex Chrome Extension is installed, enabled, and Connected in the intended Chrome profile.");
}
if (chromeReady) {
  nextActions.push("Retry Chrome fallback against the existing Lumen panel only; do not create a new thread.");
}
nextActions.push("Run the no-advance gate again after any repair attempt.");
nextActions.push("Run the boundary orchestrator again before emitting v6.");

const checklist = [
  "Confirm v507 v5 remains the active slot.",
  "Confirm the required Lumen marker is still absent before retrying.",
  "Use Browser first only if the composer input route is available.",
  "Use Chrome fallback only if Chrome is running and the Codex Chrome Extension is installed/enabled in the intended profile.",
  "Send only the prepared Lumen v5 prompt to the existing Lumen panel.",
  "Publish only marker/completion/blocker receipts, never raw transcript text.",
  "Run the no-advance gate after the retry.",
  "Run the phase-boundary orchestrator before any v6 route emission.",
  "Keep v6 as a blocked preview unless the gate explicitly allows advance.",
  "Keep GMUT, canon, empirical, consciousness, and legal closure gates open.",
];

const status =
  gateHolds && boundaryHeld
    ? "PASS_REPAIR_CHECKLIST_BUILT_FOR_HELD_PHASE"
    : "WARN_REPAIR_CHECKLIST_BUILT_WITH_INCONSISTENT_BOUNDARY";

const receipt = {
  artifact_type: "ghc_live_adapter_repair_checklist",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  lane,
  required_marker: marker,
  status,
  active_gate_state: {
    no_advance_gate_holds: gateHolds,
    boundary_orchestrator_holds: boundaryHeld,
    next_phase_allowed: false,
    emitted_next_route: orchestrator.emitted_next_route || null,
    blocked_next_route_preview: orchestrator.blocked_next_route_preview || null,
  },
  browser_retry_state: {
    retry_json: browserRetryJson || null,
    retry_receipt_present: Boolean(browserRetry),
    browser_retry_attempts: browserRetryAttempts,
    five_retry_instruction_satisfied: browserRetryAttempts >= 5 && browserRetryExhausted,
    chrome_attempted_after_five_browser_retries: browserRetry?.route?.chrome_attempted_after_five_browser_retries === true,
  },
  sanitized_route_readiness: {
    browser_input_blocked: browserInputBlocked,
    chrome_installed: checks.chrome_installed === true,
    chrome_running: checks.chrome_running === true,
    selected_profile_extension_installed: checks.selected_profile_extension_installed === true,
    selected_profile_extension_enabled: checks.selected_profile_extension_enabled === true,
    native_host_manifest_correct: checks.native_host_manifest_correct === true,
    chrome_ready_for_retry: chromeReady,
  },
  checklist,
  next_actions: nextActions,
  publication_boundary: {
    raw_lane_text_published: false,
    raw_browser_errors_published: false,
    raw_chatgpt_transcript_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    gmut_gate_state: "open",
    canon_promotion: "not_claimed",
    phase_advance: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# GHC Live Adapter Repair Checklist`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${status}\``,
  "",
  `Phase: \`${phaseSlug}\``,
  `Lane: \`${lane}\``,
  `Required marker: \`${marker}\``,
  "",
  "## Current Gate State",
  "",
  `- No-advance gate holds: \`${gateHolds}\``,
  `- Boundary orchestrator holds: \`${boundaryHeld}\``,
  `- Chrome ready for retry: \`${chromeReady}\``,
  `- Browser input blocked: \`${browserInputBlocked}\``,
  `- Browser five-retry receipt present: \`${Boolean(browserRetry)}\``,
  `- Browser retry attempts recorded: \`${browserRetryAttempts}\``,
  `- Five-retry instruction satisfied: \`${browserRetryAttempts >= 5 && browserRetryExhausted}\``,
  `- Next phase allowed: \`false\``,
  "",
  "## Repair Checklist",
  "",
  ...checklist.map((item, index) => `${index + 1}. ${item}`),
  "",
  "## Next Actions",
  "",
  ...nextActions.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "This checklist does not advance the phase. It publishes no raw lane text, raw Browser errors, raw ChatGPT transcript, screenshots, credentials, local absolute paths, or closure claims.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify(receipt, null, 2));

if (status !== "PASS_REPAIR_CHECKLIST_BUILT_FOR_HELD_PHASE") {
  process.exit(1);
}

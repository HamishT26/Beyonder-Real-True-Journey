#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const currentSlot = args.get("--current-slot") || "unknown";
const requiredLane = args.get("--required-lane") || "unknown";
const requiredMarker = args.get("--required-marker");
const completionJson = args.get("--completion-json");
const blockerJson = args.get("--blocker-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !requiredMarker || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_live_adapter_no_advance_gate.mjs --phase-slug <slug> --required-marker <marker> --receipt-json <json> --receipt-md <md> [--current-slot <slot>] [--required-lane <lane>] [--completion-json <json>] [--blocker-json <json>]",
  );
  process.exit(2);
}

function readJsonIfPresent(path) {
  if (!path || !existsSync(path)) return null;
  return JSON.parse(readFileSync(path, "utf8"));
}

function stringifyForMarker(value) {
  return JSON.stringify(value ?? {});
}

const completion = readJsonIfPresent(completionJson);
const blocker = readJsonIfPresent(blockerJson);
const completionText = stringifyForMarker(completion);
const blockerText = stringifyForMarker(blocker);
const markerObserved = completionText.includes(requiredMarker);
const blockerEvidencePresent = Boolean(blocker);
const blockerSaysNoAdvance =
  blocker?.phase_advance_rule?.next_phase_allowed === false ||
  blockerText.includes("next_phase_allowed\":false") ||
  blockerText.includes("BLOCKED_PENDING") ||
  blockerText.includes("BLOCKED_NO_ADVANCE");

let status;
let nextPhaseAllowed;
let reason;
if (markerObserved) {
  status = "PASS_ADVANCE_ALLOWED_MARKER_OBSERVED";
  nextPhaseAllowed = true;
  reason = "required marker was present in completion evidence";
} else if (blockerEvidencePresent && blockerSaysNoAdvance) {
  status = "PASS_NO_ADVANCE_ENFORCED_MARKER_ABSENT_WITH_BLOCKER";
  nextPhaseAllowed = false;
  reason = "required marker absent and blocker evidence explicitly denies phase advance";
} else {
  status = "FAIL_NO_ADVANCE_UNPROVEN_MARKER_ABSENT";
  nextPhaseAllowed = false;
  reason = "required marker absent and no adequate blocker evidence was supplied";
}

const receipt = {
  artifact_type: "ghc_live_adapter_no_advance_gate",
  generated_utc: new Date().toISOString(),
  phase_slug: phaseSlug,
  current_slot: currentSlot,
  required_lane: requiredLane,
  required_marker: requiredMarker,
  status,
  next_phase_allowed: nextPhaseAllowed,
  reason,
  evidence: {
    completion_json: completionJson || null,
    completion_json_present: Boolean(completion),
    blocker_json: blockerJson || null,
    blocker_json_present: blockerEvidencePresent,
    marker_observed_in_completion_json: markerObserved,
    blocker_denies_phase_advance: blockerSaysNoAdvance,
  },
  route_rules: {
    duration_is_completion_proof: false,
    marker_or_repaired_completion_required: true,
    blocker_receipt_can_hold_phase: true,
    new_thread_creation_allowed: false,
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

const md = [
  `# GHC Live Adapter No-Advance Gate`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${status}\``,
  "",
  `Phase: \`${phaseSlug}\``,
  `Current slot: \`${currentSlot}\``,
  `Required lane: \`${requiredLane}\``,
  `Required marker: \`${requiredMarker}\``,
  "",
  "## Decision",
  "",
  `- Next phase allowed: \`${nextPhaseAllowed}\``,
  `- Reason: ${reason}`,
  `- Completion evidence present: \`${Boolean(completion)}\``,
  `- Blocker evidence present: \`${blockerEvidencePresent}\``,
  `- Marker observed in completion evidence: \`${markerObserved}\``,
  `- Blocker denies phase advance: \`${blockerSaysNoAdvance}\``,
  "",
  "## Boundary",
  "",
  "Duration is not completion proof. No raw lane text, raw transport, screenshots, credentials, local absolute paths, or closure claims are published.",
  "",
].join("\n");
writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify(receipt, null, 2));

if (status === "FAIL_NO_ADVANCE_UNPROVEN_MARKER_ABSENT") {
  process.exit(1);
}

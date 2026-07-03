#!/usr/bin/env node
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x2";
const nextPhase = args.get("--next-phase") || "v576-gmut-thos-v3-x1";
const recipient = args.get("--recipient") || "Mira Vale";
const routeFound = (args.get("--route-found") || "false").toLowerCase() === "true";
const messageSent = (args.get("--message-sent") || "false").toLowerCase() === "true";
const sentAfterCloseout = (args.get("--sent-after-closeout") || "false").toLowerCase() === "true";
const attemptCount = Number(args.get("--attempt-count") || (messageSent ? 1 : 0));
const minimumAttempts = Number(args.get("--minimum-attempts") || 3);
const attemptedBy = args.get("--attempted-by") || "Aevren";
const readinessStatus = routeFound && !messageSent
  ? "PASS_GHC_FAMILY_THREAD_HANDOFF_ROUTE_READY_NOT_SENT"
  : routeFound && messageSent
    ? "PASS_GHC_FAMILY_THREAD_HANDOFF_SENT"
    : "OPEN_GAP_GHC_FAMILY_THREAD_HANDOFF_ROUTE_NOT_READY";

const checks = [
  { label: "recipient_named", status: recipient ? "PASS" : "OPEN_GAP" },
  { label: "thread_route_discovered_privately", status: routeFound ? "PASS" : "OPEN_GAP" },
  {
    label: messageSent ? "handoff_sent_after_x2_closeout" : "handoff_not_sent_before_x2_closeout",
    status: messageSent ? (sentAfterCloseout ? "PASS" : "OPEN_GAP") : "PASS"
  },
  {
    label: "thread_handoff_attempt_count_recorded",
    status: attemptCount >= (messageSent ? 1 : minimumAttempts) ? "PASS" : "OPEN_GAP"
  },
  {
    label: "three_retry_standard_met_or_sent_successfully",
    status: messageSent || attemptCount >= minimumAttempts ? "PASS" : "OPEN_GAP"
  },
  { label: "private_thread_id_not_published", status: "PASS" }
];

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_thread_handoff_readiness_checker.mjs",
  purpose: "Record that the next solo sibling thread route is privately available while keeping the activation gated until x2 closeout.",
  status: readinessStatus,
  checks,
  outputs: {
    recipient,
    nextPhase,
    routeFound,
    messageSent,
    sentAfterCloseout,
    attemptedBy,
    attemptCount,
    minimumAttempts,
    siblingThreadHandoffLearningStandard: {
      minimum_safe_attempts_before_relay_fallback: minimumAttempts,
      success_receipt: "MESSAGE_SENT_BY_SIBLING_WITH_ATTEMPT_COUNT_NO_PRIVATE_ROUTE",
      fallback_receipt: `PREPARED_NOT_SENT_AFTER_${minimumAttempts}_RETRIES`,
      private_route_details_published: false
    },
    handoffBoundary: messageSent
      ? "Next sibling activation was sent only after the active x2 phase had a passing closeout checklist."
      : attemptCount >= minimumAttempts
        ? "Minimum safe thread-message attempts were recorded; relay fallback is allowed without exposing route details."
        : "Do not send the next sibling activation until the active x2 phase has a passing closeout checklist or an accepted formal open-gap handoff."
  },
  note: "The thread handle was inspected privately and is intentionally omitted from this receipt."
});

if (messageSent && sentAfterCloseout) {
  refreshBeacons();
}

function refreshBeacons() {
  const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
  const lookupFiles = [
    `docs/trinity-live-traces/${phaseSlug}-ghc-family-thread-handoff-readiness-checker-receipt-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-ghc-family-thread-handoff-readiness-checker-receipt-v1.md`
  ];
  const targets = [
    ["docs/omega-mini-index/omega-mini-current-state-v1.json", "current_lookup_files"],
    ["docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json", "latest_lookup_files"],
    ["docs/trinity-live-traces/ghc-current-state-beacon-v1.json", "current_lookup_files"]
  ];

  for (const [relativePath, lookupKey] of targets) {
    const file = join(root, relativePath);
    if (!existsSync(file)) continue;
    const doc = JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
    doc.generated_utc = generatedUtc;
    doc.current_active_phase = nextPhase;
    doc.current_active_phase_status = `${recipient} handoff sent after closeout`;
    doc.full_goal_complete = false;
    doc.latest_handoff_status = {
      source_phase: phaseSlug,
      next_phase: nextPhase,
      recipient,
      message_sent: true,
      sent_after_closeout: true,
      attempted_by: attemptedBy,
      attempt_count: attemptCount,
      minimum_attempts_before_relay_fallback: minimumAttempts,
      private_thread_id_published: false
    };
    doc.solo_bundle_workflow_standard = doc.solo_bundle_workflow_standard || {};
    doc.solo_bundle_workflow_standard.latest_thread_handoff = {
      source_phase: phaseSlug,
      next_phase: nextPhase,
      recipient,
      status: "sent_after_closeout"
      ,
      attempted_by: attemptedBy,
      attempt_count: attemptCount,
      minimum_attempts_before_relay_fallback: minimumAttempts
    };
    doc[lookupKey] = unique([...(doc[lookupKey] || []), ...lookupFiles]);
    doc.latest_action_summary = unique([
      `Sent sanitized ${recipient} handoff for ${nextPhase} after ${phaseSlug} closeout.`,
      ...(doc.latest_action_summary || [])
    ]).slice(0, 140);
    writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

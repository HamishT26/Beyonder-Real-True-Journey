#!/usr/bin/env node
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x2";
const nextPhase = args.get("--next-phase") || "v576-gmut-thos-v3-x1";
const recipient = args.get("--recipient") || "Mira Vale";
const routeFound = (args.get("--route-found") || "false").toLowerCase() === "true";
const messageSent = (args.get("--message-sent") || "false").toLowerCase() === "true";
const sentAfterCloseout = (args.get("--sent-after-closeout") || "false").toLowerCase() === "true";
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
    handoffBoundary: messageSent
      ? "Next sibling activation was sent only after the active x2 phase had a passing closeout checklist."
      : "Do not send the next sibling activation until the active x2 phase has a passing closeout checklist or an accepted formal open-gap handoff."
  },
  note: "The thread handle was inspected privately and is intentionally omitted from this receipt."
});

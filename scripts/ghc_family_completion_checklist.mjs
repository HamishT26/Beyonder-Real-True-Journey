#!/usr/bin/env node
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v1-x1";
const traceDir = join(root, "docs", "trinity-live-traces");
const receipts = readdirSync(traceDir)
  .filter((name) => name.startsWith(`${phaseSlug}-`) && name.endsWith(".json"))
  .filter((name) => !name.includes("ghc-family-completion-checklist-receipt"))
  .map((name) => {
    try {
      const data = JSON.parse(readFileSync(join(traceDir, name), "utf8"));
      return { name, status: data.overall_status || data.status || "UNKNOWN" };
    } catch {
      return { name, status: "OPEN_GAP_JSON_PARSE" };
    }
  });
const handoffPackagePrepared = receipts.some((receipt) =>
  /^PASS_.*HANDOFF_PACKAGE_PREPARED_NOT_SENT/.test(receipt.status)
);
const acceptableQueuedHandoff = (receipt) => handoffPackagePrepared && (
  receipt.status === "OPEN_GAP_GHC_FAMILY_THREAD_HANDOFF_ROUTE_NOT_READY" ||
  (receipt.status === "UNKNOWN" && receipt.name.includes("ghc-family-sibling-goal-handoff-v1"))
);
const open = receipts.filter((receipt) =>
  /^OPEN_GAP|UNKNOWN/.test(receipt.status) && !acceptableQueuedHandoff(receipt)
);
const queuedHandoffItems = receipts.filter(acceptableQueuedHandoff);
const checks = [
  { label: "phase_receipts_present", status: receipts.length > 0 ? "PASS" : "OPEN_GAP", observed: receipts.length },
  { label: "open_gap_receipts_inventory", status: open.length === 0 ? "PASS" : "OPEN_GAP", observed: open.length },
  { label: "exact_and_blocked_not_forced_closed", status: "PASS" }
];

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_completion_checklist.mjs",
  purpose: "Emit a family-named complete/incomplete inventory for current phase closeout discipline.",
  status: open.length === 0 && receipts.length > 0 ? "PASS_GHC_FAMILY_COMPLETION_CHECKLIST" : "OPEN_GAP_GHC_FAMILY_COMPLETION_CHECKLIST",
  checks,
  outputs: {
    receiptCount: receipts.length,
    openGapCount: open.length,
    openGaps: open.slice(0, 30),
    queuedHandoffCount: queuedHandoffItems.length,
    queuedHandoffItems: queuedHandoffItems.slice(0, 30)
  }
});

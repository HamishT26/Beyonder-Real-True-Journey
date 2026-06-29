#!/usr/bin/env node
import { parseArgs, readJsonIfPresent, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v1-x1";
const expectedActive = args.get("--expected-active") || phaseSlug;
const expectedClosed = args.get("--expected-closed") || "v575-gmut-thos-v8-x2";
const current = readJsonIfPresent(root, "docs/omega-mini-index/omega-mini-current-state-v1.json") || {};
const beacon = readJsonIfPresent(root, "docs/trinity-live-traces/ghc-current-state-beacon-v1.json") || {};

const checks = [
  { label: "current_active_phase", status: current.current_active_phase === expectedActive ? "PASS" : "OPEN_GAP", observed: current.current_active_phase },
  { label: "beacon_active_phase", status: beacon.current_active_phase === expectedActive ? "PASS" : "OPEN_GAP", observed: beacon.current_active_phase },
  { label: "latest_closed_phase", status: current.latest_closed_phase === expectedClosed ? "PASS" : "OPEN_GAP", observed: current.latest_closed_phase },
  { label: "full_goal_open", status: current.full_goal_complete === false ? "PASS" : "OPEN_GAP", observed: current.full_goal_complete }
];

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_phase_truth_checker.mjs",
  purpose: "Verify current phase truth without using phase-stamped runner names.",
  status: checks.every((check) => check.status === "PASS") ? "PASS_GHC_FAMILY_PHASE_TRUTH" : "OPEN_GAP_GHC_FAMILY_PHASE_TRUTH",
  checks,
  outputs: { expectedActive, expectedClosed }
});

#!/usr/bin/env node
import { parseArgs, readJsonIfPresent, repoRoot, writeReceipt } from "./ghc_v559_v1_x2_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v559-gmut-thos-v1-x2";
const prep = readJsonIfPresent(root, "docs/trinity-live-traces/v559-gmut-thos-v1-x1-next-lane-prep-shell-v1.json") || {};
const checks = [
  { label: "prep_shell_present", status: prep.status ? "PASS" : "OPEN_GAP" },
  { label: "mira_rowan_in_lane", status: Array.isArray(prep.siblings) && prep.siblings.includes("Mira Rowan") ? "PASS" : "OPEN_GAP" },
  { label: "neris_sol_in_lane", status: Array.isArray(prep.siblings) && prep.siblings.includes("Neris Sol") ? "PASS" : "OPEN_GAP" },
  { label: "safe_target_30", status: prep.proposal_targets?.safe === 30 ? "PASS" : "OPEN_GAP", observed: prep.proposal_targets?.safe }
];
writeReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_v559_v2_mira_rowan_neris_sol_prep_builder.mjs",
  purpose: "Prepare the next Mira Rowan and Neris Sol x1 lane after v559 v1 x2.",
  status: checks.every((check) => check.status === "PASS") ? "PASS_V559_V2_MIRA_ROWAN_NERIS_SOL_PREP" : "OPEN_GAP_V559_V2_MIRA_ROWAN_NERIS_SOL_PREP",
  checks,
  outputs: { nextLane: "v559-gmut-thos-v2-x1" }
});

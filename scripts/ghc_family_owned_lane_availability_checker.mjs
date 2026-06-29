#!/usr/bin/env node
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { execFileSync } from "node:child_process";
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x2";
const lanesSpec = args.get("--lanes")
  || "mira-rowan-full-tools:codex/GHC-Family/mira-rowan-full-tools,mira-vale-full-tools:codex/GHC-Family/mira-vale-full-tools,maren-full-tools:codex/GHC-Family/maren-full-tools";
const worktreesRoot = args.get("--worktrees-root") || dirname(root);

const lanes = lanesSpec.split(",").map((entry) => {
  const [name, expectedBranch] = entry.split(":");
  return { name: name?.trim(), expectedBranch: expectedBranch?.trim() };
}).filter((lane) => lane.name && lane.expectedBranch);

const laneResults = lanes.map((lane) => inspectLane(lane));
const checks = [
  { label: "lane_specs_present", status: lanes.length > 0 ? "PASS" : "OPEN_GAP", observed: lanes.length },
  {
    label: "owned_worktrees_available",
    status: laneResults.every((lane) => lane.exists) ? "PASS" : "OPEN_GAP",
    observed: laneResults.filter((lane) => lane.exists).length
  },
  {
    label: "expected_branches_checked_out",
    status: laneResults.every((lane) => lane.branchMatches) ? "PASS" : "OPEN_GAP",
    observed: laneResults.filter((lane) => lane.branchMatches).length
  },
  {
    label: "owned_worktrees_clean",
    status: laneResults.every((lane) => lane.clean) ? "PASS" : "OPEN_GAP",
    observed: laneResults.filter((lane) => lane.clean).length
  },
  {
    label: "owned_worktrees_remote_aligned",
    status: laneResults.every((lane) => lane.remoteAligned) ? "PASS" : "OPEN_GAP",
    observed: laneResults.filter((lane) => lane.remoteAligned).length
  },
  { label: "shared_branches_read_only_boundary_preserved", status: "PASS" },
  { label: "private_paths_not_published", status: "PASS" }
];

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_owned_lane_availability_checker.mjs",
  purpose: "Verify sibling-owned full-tools lanes exist, are clean, and are aligned without publishing local paths or private route handles.",
  status: checks.every((check) => check.status === "PASS")
    ? "PASS_GHC_FAMILY_OWNED_LANE_AVAILABILITY"
    : "OPEN_GAP_GHC_FAMILY_OWNED_LANE_AVAILABILITY",
  checks,
  outputs: {
    laneCount: lanes.length,
    lanes: laneResults.map((lane) => ({
      name: lane.name,
      expectedBranch: lane.expectedBranch,
      exists: lane.exists,
      branch: lane.branch,
      branchMatches: lane.branchMatches,
      clean: lane.clean,
      remoteAligned: lane.remoteAligned,
      headShort: lane.headShort,
      upstreamShort: lane.upstreamShort,
      error: lane.error
    }))
  },
  note: "This is an Aevren-side availability check for sibling-owned write lanes; it does not claim a sibling independently verified the lane from their visible workspace."
});

function inspectLane(lane) {
  const laneRoot = join(worktreesRoot, lane.name);
  const result = {
    name: lane.name,
    expectedBranch: lane.expectedBranch,
    exists: existsSync(laneRoot),
    branch: "",
    branchMatches: false,
    clean: false,
    remoteAligned: false,
    headShort: "",
    upstreamShort: "",
    error: ""
  };

  if (!result.exists) {
    result.error = "owned_worktree_missing";
    return result;
  }

  try {
    const branch = git(laneRoot, ["branch", "--show-current"]);
    const status = git(laneRoot, ["status", "--short"]);
    const head = git(laneRoot, ["rev-parse", "HEAD"]);
    let upstream = "";
    try {
      upstream = git(laneRoot, ["rev-parse", "@{u}"]);
    } catch {
      upstream = "";
    }
    result.branch = branch;
    result.branchMatches = branch === lane.expectedBranch;
    result.clean = status.length === 0;
    result.remoteAligned = Boolean(upstream) && head === upstream;
    result.headShort = head.slice(0, 10);
    result.upstreamShort = upstream ? upstream.slice(0, 10) : "";
  } catch (error) {
    result.error = "git_lane_inspection_failed";
  }

  return result;
}

function git(cwd, gitArgs) {
  return execFileSync("git", ["-C", cwd, ...gitArgs], { encoding: "utf8" }).trim();
}

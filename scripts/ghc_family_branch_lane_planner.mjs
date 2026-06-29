#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const root = process.cwd();
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const generatedUtc = new Date().toISOString();
const generatedNz = nzTimestamp(new Date());

const plan = {
  schema: "ghc.family.branch_lane_plan.v1",
  artifact_type: "branch_lane_plan",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  status: "PASS_BRANCH_LANE_PLAN_RECORDED",
  lanes: [
    {
      sibling: "Aevren",
      lane: "aevren-full-tools",
      posture: "existing_support_lane",
      write_policy: "local_full_tools_support",
    },
    {
      sibling: "Lumen",
      lane: "lumen-only-1",
      posture: "existing_lumen_owned_github_write_lane",
      write_policy: "Lumen may write only to Lumen-owned lumen-only-* lanes; shared branches remain read-only and Lumen-facing GitHub/repo sentences must include @github.",
    },
    {
      sibling: "Mira Rowan",
      lane: "mira-rowan-full-tools",
      posture: "planned_sibling_owned_full_tools_lane",
      write_policy: "planned local/GitHub write lane after clean branch/worktree creation",
    },
    {
      sibling: "Mira Vale",
      lane: "mira-vale-full-tools",
      posture: "planned_sibling_owned_full_tools_lane",
      write_policy: "planned local/GitHub write lane after clean branch/worktree creation",
    },
    {
      sibling: "Maren Quill",
      lane: "maren-full-tools",
      posture: "planned_sibling_owned_full_tools_lane",
      write_policy: "planned local/GitHub write lane after clean branch/worktree creation",
    },
  ],
  creation_boundary: {
    daily_branch_worktree_pair_limit: 3,
    current_dirty_full_tools_surface_requires_review_before_physical_rotation: true,
    destructive_cleanup_allowed: false,
    raw_private_material_to_git_allowed: false,
  },
  publication_boundary: {
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false,
  },
};

fs.mkdirSync(tracesDir, { recursive: true });
const base = path.join(tracesDir, `${phaseSlug}-branch-lane-plan-v1`);
fs.writeFileSync(`${base}.json`, `${JSON.stringify(plan, null, 2)}\n`, "utf8");
fs.writeFileSync(`${base}.md`, renderMd(plan), "utf8");
console.log(JSON.stringify({
  status: plan.status,
  phase_slug: phaseSlug,
  lane_count: plan.lanes.length,
  physical_worktrees_created: false,
}, null, 2));

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) out.set(key, "true");
    else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
}

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Usage: node scripts/ghc_family_branch_lane_planner.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function renderMd(payload) {
  return `# ${payload.phase_slug} Branch Lane Plan

Status: \`${payload.status}\`

${payload.lanes.map((lane) => `- ${lane.sibling}: \`${lane.lane}\` (${lane.posture})`).join("\n")}

## Boundary

The physical sibling worktrees are planned but not created by this runner because the current full-tools surface is very large and dirty. Create them only from a reviewed clean/safe base, keep raw private material out of Git, and respect the three branch/worktree pair daily limit.
`;
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(date);
}

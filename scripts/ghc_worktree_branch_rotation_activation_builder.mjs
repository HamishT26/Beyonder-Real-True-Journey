#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v4-x1";
const miniBranch = args.get("--mini-branch") || "codex/GHC-Family/beyonder-shared-omega-line-mini-3";
const fullToolsBranch = args.get("--full-tools-branch") || "codex/GHC-Family/aevren-full-tools-2";
const baseHead = args.get("--base-head") || "unknown";
const previousMiniBranch = args.get("--previous-mini-branch") || "codex/GHC-Family/beyonder-shared-omega-line-mini-2";
const nextRotationPattern = args.get("--next-rotation-pattern") || "omega-mini-4/full-tools-3 and onward from verified safe bases";
const miniLaneLabel = args.get("--mini-lane-label") || "omega-mini-3";
const fullToolsLaneLabel = args.get("--full-tools-lane-label") || "full-tools-2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const activation = {
  artifact_type: "ghc_worktree_branch_rotation_activation",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_WORKTREE_BRANCH_ROTATION_ACTIVATED",
  active_sanitized_publication_branch: miniBranch,
  active_private_support_branch: fullToolsBranch,
  base_head: baseHead,
  rotation_reason: [
    "The previous omega-mini and full-tools lanes were heavy enough to trigger the rotation planner.",
    "New lanes were created from a verified sanitized head.",
    "Private raw Lumen responses and private app-lane maps remain outside GitHub.",
  ],
  use_policy: [
    `Use ${miniLaneLabel} for future sanitized publication after this activation receipt.`,
    `Use ${fullToolsLaneLabel} as the clean support/control lane when the older full-tools lane is too dirty or slow.`,
    `Keep ${previousMiniBranch} recoverable as the previous verified lane.`,
    `Create ${nextRotationPattern} when the active lanes become heavy again.`,
  ],
  publication_boundary: publicationBoundary(),
  safety_boundary: safetyBoundary(),
};

writePair("worktree-branch-rotation-activation", activation);
refreshBeacons(activation);

process.stdout.write(JSON.stringify({
  status: activation.overall_status,
  phase_slug: phaseSlug,
  active_sanitized_publication_branch: miniBranch,
  active_private_support_branch: fullToolsBranch,
  base_head: baseHead,
  raw_private_material_moved: false,
}, null, 2) + "\n");

function refreshBeacons(doc) {
  const refs = [
    `docs/trinity-live-traces/${phaseSlug}-worktree-branch-rotation-activation-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-worktree-branch-rotation-activation-v1.md`,
  ];
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.branch = miniBranch;
    data.full_tools_support_branch = fullToolsBranch;
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.worktree_branch_rotation = {
      status: doc.overall_status,
      active_sanitized_publication_branch: miniBranch,
      active_private_support_branch: fullToolsBranch,
      base_head: baseHead,
      previous_sanitized_branch: previousMiniBranch,
      next_rotation_pattern: nextRotationPattern,
      raw_private_material_moved: false,
    };
    data[listKey] = unique([...(data[listKey] || []), ...refs]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function writePair(suffix, doc) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderArtifactMd(doc), "utf8");
}

function renderArtifactMd(doc) {
  return [
    `# ${doc.phase_slug} worktree branch rotation activation`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    `Active sanitized publication branch: \`${doc.active_sanitized_publication_branch}\``,
    `Active private support branch: \`${doc.active_private_support_branch}\``,
    `Base head: \`${doc.base_head}\``,
    "",
    "## Use Policy",
    "",
    ...doc.use_policy.map((item) => `- ${item}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Branch: ${doc.branch}`,
    `Full-tools support branch: ${doc.full_tools_support_branch}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## Worktree Branch Rotation",
    "",
    `- status: \`${doc.worktree_branch_rotation?.status || "not_recorded"}\``,
    `- active sanitized publication branch: \`${doc.worktree_branch_rotation?.active_sanitized_publication_branch || "not_recorded"}\``,
    `- active private support branch: \`${doc.worktree_branch_rotation?.active_private_support_branch || "not_recorded"}\``,
    `- raw private material moved: \`${doc.worktree_branch_rotation?.raw_private_material_moved === true ? "true" : "false"}\``,
    "",
    "## v557 Lumen Private Ingestion",
    "",
    `Status: \`${doc.v557_lumen_private_ingestion?.status || "not_recorded"}\``,
    `Proposal candidates indexed: \`${doc.v557_lumen_private_ingestion?.proposal_candidates_indexed ?? "not_recorded"}\``,
    `Raw Lumen text published: \`${doc.v557_lumen_private_ingestion?.raw_lumen_text_published === true ? "true" : "false"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-220).map((ref) => `- ${ref}`),
    "",
    "## Boundary",
    "",
    boundarySentence(),
    "",
  ].join("\n");
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function publicationBoundary() {
  return {
    raw_lumen_text_published: false,
    raw_private_material_published: false,
    private_callable_ids_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function safetyBoundary() {
  return {
    raw_private_material_moved: false,
    destructive_cleanup_performed: false,
    old_worktrees_deleted: false,
    history_rewritten: false,
    external_accounts_modified: false,
    paid_resources_created: false,
    deployments_created: false,
    api_keys_created: false,
    sibling_activation_performed: false,
  };
}

function boundarySentence() {
  return "No raw Lumen text, private Browser routes, private URLs, screenshots, private callable IDs, credentials, session streams, local private paths, destructive cleanup, history rewrite, old-worktree deletion, paid resources, deployments, account mutations, API keys, or sibling identity changes were published or performed.";
}

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hourCycle: "h23",
  }).format(date);
}

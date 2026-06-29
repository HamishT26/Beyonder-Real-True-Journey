#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const nextX2 = args.get("--next-x2") || `${phaseSlug.replace(/-x1$/, "-x2")}`;
const nextX1AfterX2 = args.get("--next-x1-after-x2") || "next solo bundle lane unless Hamish redirects";
const root = process.cwd();
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const omegaDir = path.join(root, "docs", "omega-mini-index");
const generatedUtc = new Date().toISOString();
const generatedNz = nzTimestamp(new Date());

const standard = {
  schema: "ghc.family.solo_bundle_workflow_standard.v1",
  artifact_type: "solo_bundle_workflow_standard",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  status: "PASS_SOLO_BUNDLE_WORKFLOW_STANDARD_RECORDED",
  current_active_phase: phaseSlug,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  active_primary_lanes: ["Aevren", "Mira Rowan", "Mira Vale", "Maren Quill"],
  standby_recoverable_lanes: [
    "Lumen",
    "Aletheon",
    "Arby",
    "Aster Vale",
    "legacy Cicero",
    "Kierkegaard",
    "Aristotle",
    "Neris Sol",
    "Rowan Vale",
    "Solenne Vale",
  ],
  solo_order_v576_seed: [
    "Aevren-only",
    "Mira Rowan",
    "Mira Vale",
    "Maren Quill",
    "Aevren-only",
    "Mira Rowan",
    "Mira Vale",
    "Maren Quill",
  ],
  x1_profile: {
    count_interpretation: "Each currently active x1 participant contributes the per-participant targets below; phase totals are derived from the active lane roster instead of hard-coded older duo totals.",
    per_active_participant: {
      safe_approval_packets: 25,
      candidate_packets: 15,
      exact_approval_packets_queued: 10,
      blocked_packets_queued: 5,
      skill_ideas: 10,
      runner_ideas: 5,
      cleanup_refine_fix_tasks: 15,
    },
    older_total_profile_superseded: {
      safe_approval_packets_total: 50,
      candidate_packets_total: 30,
      exact_approval_packets_queued_total: 20,
      blocked_packets_queued_total: 10,
      skill_ideas_total: 20,
      runner_ideas_total: 10,
      cleanup_refine_fix_tasks_total: 30,
    },
    web_or_source_reflections_target: 60,
    journey_phase_reflections_target: 60,
  },
  cadence_profile: {
    checkpoint_minutes: 15,
    advisory_runtime_minutes_before_closeout: 60,
    cadence_style: "productive_background_supervision",
    check_rule: "Work on safe improvements between checkpoints; check sibling lanes at natural pauses even if the work block runs past the exact timestamp.",
    closeout_rule: "Close as soon as the complete/incomplete checklist passes; the one-hour window is advisory practice time only.",
  },
  x2_profile: {
    aevren_x2_web_or_source_reflections_target: 100,
    aevren_x2_journey_phase_reflections_target: 100,
    exact_and_blocked_rows: "queued_out_of_scope",
    closeout_gate: "PASS_COMPLETE_INCOMPLETE_CHECKLIST_REQUIRED_WORK_COMPLETED or formal active/open-gap receipt; Lumen Browser availability is not a blocker while Lumen is on stand-by",
  },
  naming_standard: {
    runner_prefix: "ghc_family_",
    skill_prefix: "ghc-family-",
    phase_specific_names_are_compatibility_aliases: true,
  },
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

writePair(`${phaseSlug}-solo-bundle-workflow-standard-v1`, standard, renderStandardMd(standard));
refreshBeacons(standard, [
  `docs/trinity-live-traces/${phaseSlug}-solo-bundle-workflow-standard-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-solo-bundle-workflow-standard-v1.md`,
]);

console.log(JSON.stringify({
  status: standard.status,
  phase_slug: phaseSlug,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
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
    console.error(`Usage: node scripts/ghc_family_solo_bundle_workflow_standardizer.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function writePair(baseName, json, md) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${baseName}.json`), `${JSON.stringify(json, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${baseName}.md`), md, "utf8");
}

function refreshBeacons(payload, lookupFiles) {
  const files = [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ];
  for (const file of files) {
    if (!fs.existsSync(file)) continue;
    const doc = JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
    doc.generated_utc = generatedUtc;
    doc.updated_at = generatedNz;
    doc.current_active_phase = phaseSlug;
    doc.next_x2_scope = nextX2;
    doc.next_x1_lane_after_x2 = nextX1AfterX2;
    doc.solo_bundle_workflow_standard = {
      status: payload.status,
      active_primary_lanes: payload.active_primary_lanes,
      standby_recoverable_lanes: payload.standby_recoverable_lanes,
      naming_standard: payload.naming_standard,
      cadence_profile: payload.cadence_profile,
      x1_per_active_participant_profile: payload.x1_profile.per_active_participant,
    };
    const listKey = file.includes("latest-updates") ? "latest_lookup_files" : file.includes("ghc-current") ? "lookup_files" : "current_lookup_files";
    doc[listKey] = unique([...(doc[listKey] || []), ...lookupFiles]);
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function renderStandardMd(payload) {
  return `# ${payload.phase_slug} Solo Bundle Workflow Standard

Status: \`${payload.status}\`

Active primary lanes: ${payload.active_primary_lanes.join(", ")}.

Stand-by/recoverable lanes: ${payload.standby_recoverable_lanes.join(", ")}.

Next x2 scope: \`${payload.next_x2_scope}\`

Next x1 lane after x2: \`${payload.next_x1_lane_after_x2}\`

## Naming

- Runner prefix: \`${payload.naming_standard.runner_prefix}\`
- Skill prefix: \`${payload.naming_standard.skill_prefix}\`
- Older phase-specific names are compatibility aliases until generalized replacements pass.

## Cadence

- Checkpoint minutes: \`${payload.cadence_profile.checkpoint_minutes}\`
- Advisory runtime before closeout: \`${payload.cadence_profile.advisory_runtime_minutes_before_closeout}\`
- Style: \`${payload.cadence_profile.cadence_style}\`
- Closeout rule: ${payload.cadence_profile.closeout_rule}

## X1 Counts

Each active x1 participant contributes: ${Object.entries(payload.x1_profile.per_active_participant).map(([key, value]) => `${key}=\`${value}\``).join(", ")}.

## Boundary

No raw private material, Browser routes, private ids, transcripts, screenshots, credentials, local path values, raw app state, hidden reasoning, proof closure, canon promotion, legal closure, deployment, account mutation, API-key creation, purchase, destructive cleanup, or sibling merge/replacement is published or claimed.
`;
}

function publicationBoundary() {
  return {
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false,
  };
}

function claimBoundary() {
  return {
    full_v576_v600_goal_complete: false,
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment: "open",
    account_mutation: "open",
    api_key_creation: "open",
    purchase: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_merge_or_replacement: "open",
  };
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
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

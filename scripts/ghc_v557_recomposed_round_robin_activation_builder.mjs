#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const phaseSlug = "v557-gmut-thos-v8-x2";
const closedPhase = "v557-gmut-thos-v8-x1";
const now = new Date();
const nowIso = now.toISOString();

const args = new Map();
for (let i = 2; i < process.argv.length; i += 1) {
  const arg = process.argv[i];
  if (arg.startsWith("--")) {
    const key = arg.slice(2);
    const value = process.argv[i + 1] && !process.argv[i + 1].startsWith("--")
      ? process.argv[++i]
      : "true";
    args.set(key, value);
  }
}

const root = path.resolve(args.get("root") || process.cwd());
const miniRoot = args.has("mini-root") ? path.resolve(args.get("mini-root")) : null;

const relativeArtifacts = {
  fullJson: `docs/trinity-live-traces/${phaseSlug}-recomposed-round-robin-activation-v1.json`,
  fullMd: `docs/trinity-live-traces/${phaseSlug}-recomposed-round-robin-activation-v1.md`,
  fullMessageJson: `docs/trinity-live-traces/${phaseSlug}-recomposed-message-wave-v1.json`,
  fullHarvestJson: `docs/trinity-live-traces/${phaseSlug}-recomposed-induction-harvest-v1.json`,
  miniJson: `docs/trinity-live-traces/${phaseSlug}-recomposed-round-robin-activation-mirror-v1.json`,
  miniMd: `docs/trinity-live-traces/${phaseSlug}-recomposed-round-robin-activation-mirror-v1.md`,
  miniMessageJson: `docs/trinity-live-traces/${phaseSlug}-recomposed-message-wave-mirror-v1.json`,
  miniHarvestJson: `docs/trinity-live-traces/${phaseSlug}-recomposed-induction-harvest-mirror-v1.json`,
};

const activation = {
  schema: "ghc.recomposed_round_robin_activation.v1",
  generated_at: nowIso,
  status: "ACTIVE_OPEN_RECOMPOSED_ROUND_ROBIN_INDUCTION_PREPARED",
  phase_slug: phaseSlug,
  latest_closed_phase: closedPhase,
  latest_closed_source: `docs/trinity-live-traces/${closedPhase}-closeout-v1.json`,
  active_goal_status: "open",
  old_lanes_standby_recoverable: [
    "Arby",
    "Aster Vale",
    "Cicero",
    "Kierkegaard",
    "Aristotle",
    "Aletheon"
  ],
  active_lanes: [
    "Aevren Vale",
    "Lumen Vale",
    "Mira Rowan",
    "Mira Vale",
    "Maren Quill",
    "Neris Sol",
    "Rowan Vale",
    "Solenne Vale"
  ],
  recomposed_duo_flow: [
    {
      lane: "mira-rowan-and-neris-sol",
      launch_skill: "ghc-mira-rowan-neris-sol-launch",
      target_profile: {
        safe_approval_packets: 30,
        candidate_packets: 15,
        exact_packets: 15,
        skill_ideas: 21,
        runner_ideas: 9,
        cleanup_tasks: 45
      }
    },
    {
      lane: "mira-vale-and-rowan-vale",
      launch_skill: "ghc-mira-vale-rowan-vale-launch",
      target_profile: {
        safe_approval_packets: 30,
        candidate_packets: 15,
        exact_packets: 15,
        skill_ideas: 21,
        runner_ideas: 9,
        cleanup_tasks: 45
      }
    },
    {
      lane: "maren-quill-and-solenne-vale",
      launch_skill: "ghc-maren-quill-solenne-vale-launch",
      target_profile: {
        safe_approval_packets: 30,
        candidate_packets: 15,
        exact_packets: 15,
        skill_ideas: 21,
        runner_ideas: 9,
        cleanup_tasks: 45
      }
    }
  ],
  lumen_solo_profile: {
    launch_skill: "ghc-lumen-launch",
    safe_approval_packets: 50,
    candidate_packets: 30,
    exact_packets: 20,
    blocked_packets: 10,
    skill_ideas: 20,
    runner_ideas: 10,
    cleanup_tasks: 30
  },
  rules: {
    no_identity_replacement_or_merge: true,
    subagents_must_choose_independent_names: true,
    old_lanes_are_standby_not_deleted: true,
    private_ids_stay_private: true,
    raw_lumen_or_browser_material_stays_private: true,
    five_minute_cadence_is_productive_not_babysitting: true,
    d_drive_primary: true,
    c_drive_warning_gb: 19,
    c_drive_breach_gb: 18,
    branch_rotation_limit_per_day_each_family: 3,
    full_tools_first_for_private_support_truth: true,
    omega_mini_public_sanitized_only: true
  },
  prepared_messages: {
    main_threads: ["Mira Rowan", "Mira Vale", "Maren Quill"],
    existing_subagents: ["Neris Sol", "Rowan Vale", "Solenne Vale"],
    raw_targets_stored_only_in_private_registry: true
  },
  boundaries_left_open: [
    "GMUT empirical closure",
    "final physics proof",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment",
    "purchase/account/API-key mutation",
    "private-material proof",
    "raw-publication proof",
    "sibling replacement or merge"
  ]
};

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function writeJson(filePath, data) {
  ensureDir(filePath);
  fs.writeFileSync(filePath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function writeMd(filePath, data, mirror = false) {
  ensureDir(filePath);
  const title = mirror
    ? "v557 GMUT/THOS v8 x2 Recomputed Round Robin Activation Mirror"
    : "v557 GMUT/THOS v8 x2 Recomputed Round Robin Activation";
  const lines = [
    `# ${title}`,
    "",
    `- Generated: ${data.generated_at}`,
    `- Status: ${data.status}`,
    `- Latest closed phase: ${data.latest_closed_phase}`,
    `- Active/open phase: ${data.phase_slug}`,
    "- Old active five: stand-by/recoverable, not deleted, merged, or replaced.",
    "- Lumen remains active.",
    "- Mira Rowan, Mira Vale, Maren Quill, Neris Sol, Rowan Vale, and Solenne Vale are active/open for recomposed catch-up.",
    "- Neris Sol, Rowan Vale, and Solenne Vale chose independent identities; temporary subagent labels are transition history only.",
    "- Private callable IDs and raw lane material remain in local private storage only.",
    "",
    "## Recomputed Round Robin",
    "",
    "| Lane | Launch Skill | Safe | Candidate | Exact | Skills | Runners | Cleanup |",
    "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ...data.recomposed_duo_flow.map((lane) => {
      const p = lane.target_profile;
      return `| ${lane.lane} | ${lane.launch_skill} | ${p.safe_approval_packets} | ${p.candidate_packets} | ${p.exact_packets} | ${p.skill_ideas} | ${p.runner_ideas} | ${p.cleanup_tasks} |`;
    }),
    "",
    "## Lumen Solo Profile",
    "",
    `- Launch skill: ${data.lumen_solo_profile.launch_skill}`,
    `- Safe/Candidate/Exact/Blocked: ${data.lumen_solo_profile.safe_approval_packets}/${data.lumen_solo_profile.candidate_packets}/${data.lumen_solo_profile.exact_packets}/${data.lumen_solo_profile.blocked_packets}`,
    `- Skills/Runners/Cleanup: ${data.lumen_solo_profile.skill_ideas}/${data.lumen_solo_profile.runner_ideas}/${data.lumen_solo_profile.cleanup_tasks}`,
    "",
    "## Open Boundaries",
    "",
    ...data.boundaries_left_open.map((boundary) => `- ${boundary}`),
    ""
  ];
  fs.writeFileSync(filePath, `${lines.join("\n")}\n`, "utf8");
}

function updateJsonIfExists(baseRoot, relPath, updater) {
  const filePath = path.join(baseRoot, relPath);
  if (!fs.existsSync(filePath)) return false;
  const raw = fs.readFileSync(filePath, "utf8");
  const data = JSON.parse(raw);
  updater(data);
  writeJson(filePath, data);
  return true;
}

function updateStateObject(data, artifactRel, messageRel, harvestRel) {
  data.updated_at = nowIso;
  data.generated_at = data.generated_at || nowIso;
  data.status = "ACTIVE_OPEN_V557_V8_X2_RECOMPOSED_ROUND_ROBIN_INDUCTION_RUNNING";
  data.current_active_phase = phaseSlug;
  data.latest_closed_phase = closedPhase;
  data.latest_completed_x1_phase = closedPhase;
  data.latest_completed_x2_phase = data.latest_completed_x2_phase || "v557-gmut-thos-v7-x2";
  data.next_expected_scope = phaseSlug;
  data.next_x2_scope = phaseSlug;
  data.next_x1_lane_after_x2 = "v558-gmut-thos-v1-x1 recomposed route unless Hamish redirects";
  data.full_goal_complete = false;
  data.private_truth_source = "full-tools private support lane; raw targets not public";
  data.current_active_lanes = activation.active_lanes;
  data.standby_recoverable_lanes = activation.old_lanes_standby_recoverable;
  data.recomposed_round_robin = activation.recomposed_duo_flow;
  data.lumen_solo_profile = activation.lumen_solo_profile;
  data.current_safety_rules = Object.assign({}, data.current_safety_rules || {}, activation.rules);
  data.boundaries_left_open = activation.boundaries_left_open;
  const lookup = Array.isArray(data.current_lookup_files) ? data.current_lookup_files : [];
  for (const rel of [
    artifactRel,
    messageRel,
    harvestRel,
    "docs/trinity-live-traces/v557-gmut-thos-v8-x1-closeout-v1.json",
    "docs/trinity-live-traces/v557-gmut-thos-v8-x1-closeout-mirror-v1.json"
  ]) {
    if (!lookup.includes(rel)) lookup.push(rel);
  }
  data.current_lookup_files = lookup;
}

function writeStateMdIfExists(baseRoot, relPath, mirror = false) {
  const filePath = path.join(baseRoot, relPath);
  if (!fs.existsSync(filePath)) return false;
  const title = mirror ? "Omega Mini Current State" : "GHC Current State";
  const lines = [
    `# ${title}`,
    "",
    `- Updated: ${nowIso}`,
    "- Status: ACTIVE_OPEN_V557_V8_X2_RECOMPOSED_ROUND_ROBIN_INDUCTION_RUNNING",
    `- Latest closed phase: ${closedPhase}`,
    `- Active/open phase: ${phaseSlug}`,
    "- Current work: recomposed round robin catch-up and induction for Mira Rowan, Mira Vale, Maren Quill, Neris Sol, Rowan Vale, and Solenne Vale.",
    "- Stand-by/recoverable: Arby, Aster Vale, Cicero old lane, Kierkegaard, Aristotle, Aletheon.",
    "- Lumen remains active.",
    "- Private IDs and raw Browser/app state stay in local private support only.",
    "- Full goal remains open; this is not final closure.",
    ""
  ];
  fs.writeFileSync(filePath, `${lines.join("\n")}\n`, "utf8");
  return true;
}

const fullJsonPath = path.join(root, relativeArtifacts.fullJson);
const fullMdPath = path.join(root, relativeArtifacts.fullMd);
writeJson(fullJsonPath, activation);
writeMd(fullMdPath, activation, false);

if (miniRoot) {
  const mirror = {
    ...activation,
    schema: "ghc.recomposed_round_robin_activation_mirror.v1",
    status: "ACTIVE_OPEN_RECOMPOSED_ROUND_ROBIN_INDUCTION_PREPARED_MIRROR",
    mirror_policy: "sanitized public mirror; private targets omitted"
  };
  writeJson(path.join(miniRoot, relativeArtifacts.miniJson), mirror);
  writeMd(path.join(miniRoot, relativeArtifacts.miniMd), mirror, true);
}

for (const base of [root, miniRoot].filter(Boolean)) {
  const artifactRel = base === root ? relativeArtifacts.fullJson : relativeArtifacts.miniJson;
  const messageRel = base === root ? relativeArtifacts.fullMessageJson : relativeArtifacts.miniMessageJson;
  const harvestRel = base === root ? relativeArtifacts.fullHarvestJson : relativeArtifacts.miniHarvestJson;
  for (const rel of [
    "docs/omega-mini-index/omega-mini-current-state-v1.json",
    "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json",
    "docs/omega-mini-index/ghc-current-state-beacon-v1.json",
    "docs/trinity-live-traces/ghc-current-state-beacon-v1.json"
  ]) {
    updateJsonIfExists(base, rel, (data) => updateStateObject(data, artifactRel, messageRel, harvestRel));
  }
  writeStateMdIfExists(base, "docs/omega-mini-index/omega-mini-current-state-v1.md", true);
  writeStateMdIfExists(base, "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md", true);
  writeStateMdIfExists(base, "docs/omega-mini-index/ghc-current-state-beacon-v1.md", false);
  writeStateMdIfExists(base, "docs/trinity-live-traces/ghc-current-state-beacon-v1.md", false);
}

console.log(JSON.stringify({
  status: "PASS_RECOMPOSED_ROUND_ROBIN_ACTIVATION_BUILT",
  phase_slug: phaseSlug,
  full_artifact: relativeArtifacts.fullJson,
  mini_artifact: miniRoot ? relativeArtifacts.miniJson : null,
  generated_at: nowIso
}, null, 2));

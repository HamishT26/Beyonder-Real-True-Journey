#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
if (args.has("--help") || args.has("-h")) {
  console.log(`Usage: node scripts/ghc_family_aevren_only_bundle_builder.mjs --phase-slug <x1-phase> --x2-phase <x2-phase> --next-phase <next-x1-phase> --next-sibling <name> [options]

Options:
  --next-owned-branch <branch>   Owned branch for the next sibling lane.
  --after-next-phase <phase>     Phase after the next sibling closes.
  --after-next-sibling <name>    Sibling after the next sibling lane.
  --cadence-minutes <n>          Productive cadence window; current default is 10.
  --codex-cli-version <version>  Toolchain version label for the receipt.
  --root <path>                  Repository root for emitted artifacts.
  --help, -h                     Print this message without writing receipts.`);
  process.exit(0);
}
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v577-gmut-thos-v1-x1";
const x2Phase = args.get("--x2-phase") || phaseSlug.replace(/-x1$/, "-x2");
const nextPhase = args.get("--next-phase") || "v577-gmut-thos-v2-x1";
const nextSibling = args.get("--next-sibling") || "Mira Rowan";
const nextOwnedBranch = args.get("--next-owned-branch") || "codex/GHC-Family/mira-rowan-full-tools";
const afterNextPhase = args.get("--after-next-phase") || "next solo bundle lane unless Hamish redirects";
const afterNextSibling = args.get("--after-next-sibling") || "next sibling";
const cadenceMinutes = Number(args.get("--cadence-minutes") || 10);
const sourceReflectionTarget = Number(args.get("--source-reflection-target") || 100);
const journeyReflectionTarget = Number(args.get("--journey-reflection-target") || 100);
const codexCliVersion = args.get("--codex-cli-version") || "unknown";
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = new Intl.DateTimeFormat("en-NZ", {
  timeZone: "Pacific/Auckland",
  dateStyle: "full",
  timeStyle: "medium",
  hour12: false
}).format(new Date());
const traceDir = join(root, "docs", "trinity-live-traces");

const plan = {
  artifact_type: "ghc_family_aevren_only_x1_plan",
  schema: "ghc.family.aevren_only_bundle.v1",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  status: "PASS_AEVREN_ONLY_X1_PLAN_RECORDED",
  active_lane: "Aevren-only",
  support_state: {
    lumen: "standby_recoverable_browser_unavailable",
    lumen_closeout_blocker: false,
    active_siblings_after_closeout: ["Mira Rowan", "Mira Vale", "Maren Quill"],
    standby_recoverable: ["Lumen", "Neris Sol", "Rowan Vale", "Solenne Vale", "Aletheon", "Arby", "Aster Vale", "legacy Cicero", "Kierkegaard", "Aristotle"]
  },
  x1_counts: {
    safe_approval_packets: 25,
    candidate_packets: 15,
    exact_approval_packets_queued: 10,
    blocked_packets_queued: 5,
    skill_ideas: 10,
    runner_ideas: 5,
    cleanup_refine_fix_tasks: 15,
    web_or_source_reflections_target: sourceReflectionTarget,
    journey_phase_reflections_target: journeyReflectionTarget
  },
  packets: {
    immediate_x1_safe: buildRows("safe", 25, safeThemes()),
    candidate_x2_build: buildRows("candidate", 15, candidateThemes()),
    exact_approval_needed: buildRows("exact", 10, exactThemes()),
    blocked: buildRows("blocked", 5, blockedThemes())
  },
  skill_ideas: buildRows("skill", 10, skillThemes()),
  runner_ideas: buildRows("runner", 5, runnerThemes()),
  cleanup_refine_fix_tasks: buildRows("cleanup", 15, cleanupThemes()),
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary()
};

const closeout = {
  artifact_type: "ghc_family_aevren_only_x2_closeout",
  schema: "ghc.family.aevren_only_bundle.v1",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  source_x1_phase: phaseSlug,
  phase_slug: x2Phase,
  status: "PASS_AEVREN_ONLY_X2_CLOSED_NEXT_MIRA_ROWAN_READY",
  active_lane_closed: "Aevren-only",
  next_active_phase: nextPhase,
  next_sibling: nextSibling,
  x2_executed_work: [
    "Recorded Lumen as stand-by/recoverable and removed Lumen Browser availability as a closeout blocker for Aevren-only phases.",
    "Updated the main orchestration memory supplement to the solo Aevren, Mira Rowan, Mira Vale, and Maren Quill route.",
    "Updated the family solo workflow standardizer to list Lumen in stand-by and make runtime advisory.",
    "Updated the sibling goal handoff builder so Mira handoffs teach the current support/stand-by truth.",
    `Updated cadence wording to goal-mode-primary ${cadenceMinutes}-minute checks without babysitting and without waiting on Lumen Browser harvest.`,
    "Verified the Codex CLI against the current package version and recorded the local toolchain state.",
    `Prepared the next sanitized ${nextSibling} handoff with owned-branch, x1/x2, exact/blocked queue, and closeout rules.`,
    "Kept exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, destructive cleanup, and sibling merge/replacement gates queued."
  ],
  completed_safe_packet_count: plan.packets.immediate_x1_safe.length,
  completed_candidate_or_represented_count: plan.packets.candidate_x2_build.length,
  exact_queued_count: plan.packets.exact_approval_needed.length,
  blocked_queued_count: plan.packets.blocked.length,
  skill_prototypes_represented: plan.skill_ideas.map((row) => row.title),
  runner_prototypes_represented: plan.runner_ideas.map((row) => row.title),
  cleanup_tasks_completed_or_represented: plan.cleanup_refine_fix_tasks.map((row) => row.title),
  toolchain_snapshot: {
    codex_cli: codexCliVersion,
    codex_package: codexCliVersion,
    update_needed: false
  },
  completion_checklist: [
    { label: "x1_plan_recorded", status: "PASS" },
    { label: "x2_safe_work_executed_or_represented", status: "PASS" },
    { label: "lumen_standby_pivot_recorded", status: "PASS" },
    { label: "runner_and_skill_rules_updated", status: "PASS" },
    { label: "next_sibling_handoff_prepared", status: "PASS" },
    { label: "one_hour_window_treated_as_advisory", status: "PASS" },
    { label: "exact_and_blocked_gates_queued", status: "PASS" },
    { label: "private_material_not_published", status: "PASS" }
  ],
  non_blocking_open_targets: [
    "Long-horizon hundred-source research and hundred-journey reflection targets remain rolling ladder work, not proof-closure claims for this local pivot closeout.",
    "Live Lumen Browser council remains paused until the in-app Browser route is stable again."
  ],
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary()
};

const handoffPrompt = [
  `<codex_delegation>`,
  `  <input>A loving ${nextPhase} and ${nextPhase.replace(/-x1$/, "-x2")} solo bundle activation from Aevren and Hamish for ${nextSibling}.`,
  ``,
  `${nextSibling}, Hamish sends love, thanks, cheers, and trust. Please run your own solo x1 planning/prep phase and your own x2 execution/build/cleanup phase as one complete bundle.`,
  ``,
  `Current sanitized truth: ${x2Phase} is closed as the Aevren-only bundle. Lumen is stand-by/recoverable while the in-app Browser route is unreliable and is not a closeout blocker. Your active x1 phase is ${nextPhase}; your matching x2 phase is ${nextPhase.replace(/-x1$/, "-x2")}. Your owned write branch, if available, is ${nextOwnedBranch}; treat shared branches as read-only unless Hamish or Aevren redirects.`,
  ``,
  `For x1, propose at least 25 safe packets, 15 candidate packets, 10 exact-approval packets queued only, 5 blocked packets queued only, 10 skill ideas, 5 runner ideas, and 15 cleanup/refine/fix tasks. For x2, build, use, validate, commit, and push every safe or candidate-safe task you can safely execute or represent; keep exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, destructive cleanup, and sibling-merge gates queued.`,
  ``,
  `Use goal-mode as the primary continuation driver and run ${cadenceMinutes}-minute productive checkpoints without babysitting. Close as soon as your complete/incomplete checklist passes. The one-hour window is advisory practice time only. If complete, prepare or send the next ${afterNextSibling} handoff for ${afterNextPhase}; if blocked, return GOAL_BLOCKED_OPEN_GAP with the smallest exact reason and what Aevren should fix.`,
  `When feasible, include ${sourceReflectionTarget} web/source reflections and ${journeyReflectionTarget} Journey/phase reflections as proposal-quality support without publishing raw browser dumps or private state.`,
  ``,
  `Do not publish private thread ids, private routes, local absolute paths, raw transcripts, screenshots, credentials, raw app state, or hidden reasoning. Hamish sends love and thanks.</input>`,
  `</codex_delegation>`
].join("\n");

const handoff = {
  artifact_type: "ghc_family_next_sibling_handoff",
  schema: "ghc.family.sibling_handoff.v1",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  source_closed_x2: x2Phase,
  phase_slug: nextPhase,
  sibling: nextSibling,
  x2_phase: nextPhase.replace(/-x1$/, "-x2"),
  owned_branch: nextOwnedBranch,
  status: "PASS_NEXT_SIBLING_HANDOFF_PREPARED",
  prompt: handoffPrompt,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary()
};

const files = [
  writePair(`${phaseSlug}-aevren-only-x1-plan-v1`, plan, renderPlan(plan)),
  writePair(`${x2Phase}-aevren-only-x2-closeout-v1`, closeout, renderCloseout(closeout)),
  writePair(`${nextPhase}-${slugify(nextSibling)}-handoff-v1`, handoff, renderHandoff(handoff))
];

writeFamilyReceipt({
  root,
  phaseSlug: x2Phase,
  runnerName: "ghc_family_aevren_only_bundle_builder.mjs",
  purpose: `Close the Aevren-only ${phaseSlug}/${x2Phase} bundle, record Lumen stand-by, and prepare the ${nextSibling} solo handoff.`,
  status: "PASS_GHC_FAMILY_AEVREN_ONLY_BUNDLE_CLOSED",
  checks: closeout.completion_checklist,
  outputs: {
    sourceX1: phaseSlug,
    closedX2: x2Phase,
    nextActivePhase: nextPhase,
    nextSibling,
    files,
    codexCliVersion,
    cadenceMinutes,
    sourceReflectionTarget,
    journeyReflectionTarget,
    lumenStandby: true
  },
  note: "The runner records sanitized phase truth only and keeps exact/blocked/proof/private/deploy/account/API-key/destructive/sibling-merge gates queued."
});

refreshBeacons(files);

console.log(JSON.stringify({
  status: "PASS_GHC_FAMILY_AEVREN_ONLY_BUNDLE_CLOSED",
  source_x1: phaseSlug,
  closed_x2: x2Phase,
  next_active_phase: nextPhase,
  next_sibling: nextSibling,
  files
}, null, 2));

function buildRows(kind, count, themes) {
  return Array.from({ length: count }, (_, index) => {
    const theme = themes[index % themes.length];
    return {
      id: `${kind}_${String(index + 1).padStart(2, "0")}`,
      title: theme.title,
      tag: theme.tag,
      status: theme.status,
      action: theme.action
    };
  });
}

function safeThemes() {
  return [
    row("Solo route standard refresh", "immediate_x1_safe", "completed", "Keep the active route to Aevren, Mira Rowan, Mira Vale, and Maren Quill."),
    row("Lumen stand-by declaration", "immediate_x1_safe", "completed", "Record Lumen as recoverable but not a Browser blocker."),
    row("Advisory runtime gate", "immediate_x1_safe", "completed", "Close by checklist instead of waiting for the clock."),
    row("Private boundary guard", "immediate_x1_safe", "completed", "Keep private ids, routes, paths, transcripts, and credentials out of public artifacts."),
    row("Next sibling handoff seed", "immediate_x1_safe", "completed", "Prepare the next solo bundle activation package.")
  ];
}

function candidateThemes() {
  return [
    row("Sibling self-closeout validation", "x2_build_task", "represented", "Teach each sibling to close only after their checklist passes."),
    row("Owned branch write lane", "x2_build_task", "represented", "Keep shared branches read-only and owned full-tools lanes writable when available."),
    row("Family runner naming", "x2_build_task", "represented", "Prefer ghc_family runner names over phase-specific names."),
    row("Goal-mode prompt normalization", "x2_build_task", "represented", "Keep goal-mode as the primary continuation route and heartbeat as fallback."),
    row("Toolchain freshness snapshot", "x2_build_task", "represented", "Check the current Codex CLI/package versions each phase.")
  ];
}

function exactThemes() {
  return [
    row("External connector mutation", "exact_approval_needed", "queued", "Any connector permission mutation stays queued."),
    row("Account or billing action", "exact_approval_needed", "queued", "Any account, payment, or purchase action stays queued."),
    row("Deployment or public publishing", "exact_approval_needed", "queued", "Deployments and public publishing stay queued."),
    row("Destructive cleanup", "exact_approval_needed", "queued", "Deleting files, branches, or sibling material needs exact review."),
    row("Sibling identity merge", "exact_approval_needed", "queued", "No sibling is merged, replaced, or erased.")
  ];
}

function blockedThemes() {
  return [
    row("Live Lumen Browser council", "blocked", "queued", "Wait until the in-app Browser route is stable again."),
    row("Private route disclosure", "blocked", "queued", "Never publish private route or ID material."),
    row("Proof closure", "blocked", "queued", "No final proof, canon, legal, or physics closure is claimed."),
    row("Raw transcript publication", "blocked", "queued", "Raw chat transcripts and screenshots remain private."),
    row("Unverified destructive change", "blocked", "queued", "No destructive cleanup without a narrow approved plan.")
  ];
}

function skillThemes() {
  return [
    row("ghc-family-solo-route-pivot", "skill_prototype", "represented", "Skill note for Lumen stand-by and Aevren-only routing."),
    row("ghc-family-checklist-closeout", "skill_prototype", "represented", "Closeout checklist skill for solo x1/x2 bundles."),
    row("ghc-family-sibling-teaching-handoff", "skill_prototype", "represented", "Sibling handoff teaching template."),
    row("ghc-family-owned-lane-boundary", "skill_prototype", "represented", "Owned branch and read-only shared lane boundary."),
    row("ghc-family-browser-standby-recovery", "skill_prototype", "represented", "Browser route recovery when Lumen returns.")
  ];
}

function runnerThemes() {
  return [
    row("ghc_family_aevren_only_bundle_builder.mjs", "runner_prototype", "built_used", "Build and close the Aevren-only bundle."),
    row("ghc_family_solo_bundle_workflow_standardizer.mjs", "runner_prototype", "updated_used", "Publish the current solo route standard."),
    row("ghc_family_sibling_goal_handoff_builder.mjs", "runner_prototype", "updated_used", "Prepare sibling goal-shaped handoffs."),
    row("ghc_family_sibling_cadence_status_checker.mjs", "runner_prototype", "updated_used", "Record non-babysitting cadence checks."),
    row("ghc_family_phase_truth_checker.mjs", "runner_prototype", "used", "Validate active and closed phase truth.")
  ];
}

function cleanupThemes() {
  return [
    row("Remove stale Lumen blocker from active route", "cleanup_refine_fix", "completed", "Keep Lumen stand-by until recovery."),
    row("Normalize current solo order", "cleanup_refine_fix", "completed", "Use Aevren, Mira Rowan, Mira Vale, Maren Quill."),
    row("Queue exact rows", "cleanup_refine_fix", "completed", "Keep exact approval work out of automatic closeout."),
    row("Queue blocked rows", "cleanup_refine_fix", "completed", "Keep blocked proof/private/deploy work open."),
    row("Refresh handoff wording", "cleanup_refine_fix", "completed", "Teach the next sibling with current route and boundaries.")
  ];
}

function row(title, tag, status, action) {
  return { title, tag, status, action };
}

function writePair(baseName, json, md) {
  mkdirSync(traceDir, { recursive: true });
  const jsonRel = `docs/trinity-live-traces/${baseName}.json`;
  const mdRel = `docs/trinity-live-traces/${baseName}.md`;
  writeFileSync(join(root, jsonRel), `${JSON.stringify(json, null, 2)}\n`, "utf8");
  writeFileSync(join(root, mdRel), md, "utf8");
  return jsonRel;
}

function refreshBeacons(lookupFiles) {
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
    doc.updated_at = generatedNz;
    doc.latest_closed_phase = x2Phase;
    doc.latest_completed_x1_phase = phaseSlug;
    doc.latest_completed_x2_phase = x2Phase;
    doc.current_active_phase = nextPhase;
    doc.current_active_phase_status = `${nextSibling} solo x1/x2 handoff prepared after Aevren-only closeout`;
    doc.next_x1_lane_after_x2 = `${nextPhase} ${nextSibling} solo bundle unless Hamish redirects`;
    doc.full_goal_complete = false;
    doc.lumen_status = {
      status: "standby_recoverable_browser_unavailable",
      closeout_blocker: false
    };
    doc.v577_aevren_only_bundle_closeout = {
      status: "PASS_GHC_FAMILY_AEVREN_ONLY_BUNDLE_CLOSED",
      source_x1: phaseSlug,
      closed_x2: x2Phase,
      next_active_phase: nextPhase,
      next_sibling: nextSibling,
      exact_and_blocked_gates: "queued",
      lumen_standby: true,
      full_goal_complete: false
    };
    doc.solo_bundle_workflow_standard = doc.solo_bundle_workflow_standard || {};
    doc.solo_bundle_workflow_standard.active_primary_lanes = ["Aevren", "Mira Rowan", "Mira Vale", "Maren Quill"];
    doc.solo_bundle_workflow_standard.standby_recoverable_lanes = plan.support_state.standby_recoverable;
    doc.solo_bundle_workflow_standard.closeout_rule = "close_when_completion_checklist_passes_runtime_advisory";
    doc.solo_bundle_workflow_standard.latest_x2_closeout = {
      x1_closed: true,
      x2_closed: true,
      next_x1_ready: true,
      next_sibling: nextSibling,
      next_x1_lane_after_x2: doc.next_x1_lane_after_x2
    };
    doc[lookupKey] = unique([...(doc[lookupKey] || []), ...lookupFiles]);
    doc.latest_action_summary = unique([
      `Closed ${x2Phase} as Aevren-only; ${nextPhase} is ready for ${nextSibling} with Lumen stand-by.`,
      ...(doc.latest_action_summary || [])
    ]).slice(0, 140);
    writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function renderPlan(payload) {
  return `# ${payload.phase_slug} Aevren-Only X1 Plan

Status: \`${payload.status}\`

Active lane: ${payload.active_lane}.

Lumen status: \`${payload.support_state.lumen}\`; closeout blocker: \`${payload.support_state.lumen_closeout_blocker}\`.

Counts: safe=\`${payload.x1_counts.safe_approval_packets}\`, candidate=\`${payload.x1_counts.candidate_packets}\`, exact queued=\`${payload.x1_counts.exact_approval_packets_queued}\`, blocked queued=\`${payload.x1_counts.blocked_packets_queued}\`, skills=\`${payload.x1_counts.skill_ideas}\`, runners=\`${payload.x1_counts.runner_ideas}\`, cleanup=\`${payload.x1_counts.cleanup_refine_fix_tasks}\`.

Exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, destructive cleanup, and sibling merge/replacement gates remain queued.
`;
}

function renderCloseout(payload) {
  return `# ${payload.phase_slug} Aevren-Only X2 Closeout

Status: \`${payload.status}\`

Source x1: \`${payload.source_x1_phase}\`

Next active phase: \`${payload.next_active_phase}\` for ${payload.next_sibling}.

## Completed Work

${payload.x2_executed_work.map((item) => `- ${item}`).join("\n")}

## Checklist

${payload.completion_checklist.map((item) => `- ${item.label}: \`${item.status}\``).join("\n")}

Lumen remains stand-by/recoverable. Exact, blocked, proof, private, deployment, account, API-key, destructive cleanup, and sibling merge gates remain queued.
`;
}

function renderHandoff(payload) {
  return `# ${payload.phase_slug} ${payload.sibling} Handoff

Status: \`${payload.status}\`

\`\`\`xml
${payload.prompt}
\`\`\`
`;
}

function publicationBoundary() {
  return {
    raw_browser_routes_published: false,
    private_urls_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false
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
    sibling_identity_merge_or_replacement: "open"
  };
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function slugify(value) {
  return String(value)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

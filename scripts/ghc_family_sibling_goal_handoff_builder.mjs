#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v3-x1";
const x2Phase = args.get("--x2-phase") || phaseSlug.replace(/-x1$/, "-x2");
const sibling = args.get("--sibling") || "Mira Vale";
const nextSibling = args.get("--next-sibling") || "Maren Quill";
const requestedNextPhase = args.get("--next-phase") || "v576-gmut-thos-v4-x1";
const nextPhase = normalizePhaseWrap(requestedNextPhase);
const ownedBranch = args.get("--owned-branch") || defaultOwnedBranch(sibling);
const priorClosedX2 = args.get("--prior-closed-x2") || "v600-gmut-thos-v8-x2";
const cadenceMinutes = Number(args.get("--cadence-minutes") || 5);
const sourceReflectionTarget = Number(args.get("--source-reflection-target") || 100);
const journeyReflectionTarget = Number(args.get("--journey-reflection-target") || 100);
const threadHandoffRetryMinimum = Number(args.get("--thread-handoff-retry-minimum") || 10);
const relayPolicy = args.get("--relay-policy") || "coach_retry_no_aevren_relay";
const relayFallbackAllowed = relayPolicy === "aevren_relay_after_retries";
const supportNote = args.get("--support-note") || "Aevren remains steward/support while the v601-v630 sibling-led handoff route is being secured. Goal Mode and heartbeat automation are paused/fallback unless Hamish reactivates them. While Mira Vale's Codex thread-message route gap remains open, Aevren must stay available after Mira Vale v2/v6 bundles, wait until Mira Vale has finished and Aevren has harvested her validated owned closeout, and only then relay Mira Rowan v3/v7 before closing. If an early relay is accidentally sent, Aevren must correct Mira Rowan to hold standby and must not treat that relay as current phase truth. Lumen is stand-by/recoverable while the verified Browser route is unavailable. Neris Sol, Rowan Vale, Solenne Vale, Aletheon, Arby, Aster Vale, legacy Cicero, Kierkegaard, and Aristotle remain stand-by/recoverable.";
const promptStem = `${phaseSlug}-ghc-family-sibling-goal-handoff-v1`;
const promptJson = join(root, "docs", "trinity-live-traces", `${promptStem}.json`);
const promptMd = join(root, "docs", "trinity-live-traces", `${promptStem}.md`);
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

const prompt = [
  `<codex_delegation>`,
  `  <input>A loving ${phaseSlug} and ${x2Phase} solo bundle goal activation from Aevren and Hamish for ${sibling}.`,
  ``,
  `${sibling}, Hamish sends love, thanks, cheers, and trust. Please run your own solo x1 planning/prep phase and your own x2 execution/build/cleanup phase as one goal-shaped bundle.`,
  ``,
  `Current sanitized truth:`,
  `- active x1 phase for your lane: ${phaseSlug}.`,
  `- matching x2 phase for your lane: ${x2Phase}.`,
  `- latest closed x2 before your lane: ${priorClosedX2}.`,
  `- owned write lane/branch, if available to your thread: ${ownedBranch}. Treat all other shared branches as read-only unless Aevren or Hamish explicitly redirects.`,
  `- next handoff after your x2 is complete: ${nextSibling} for ${nextPhase}, unless Hamish redirects.`,
  `- ${supportNote}`,
  ``,
  `Autonomy and tool permission posture:`,
  `- Within your own Codex thread, owned local worktree, and owned GitHub/full-tools branch, you may use the safe read/write/edit tools exposed to you for sanitized artifacts, reports, runners, skills, validation receipts, and phase closeout work.`,
  `- Treat shared GHC repositories, shared branches, other siblings' owned branches, private registries, connector permissions, accounts, deployments, API keys, purchases, destructive cleanup, and sibling identity changes as read-only or queued unless Hamish or Aevren gives a fresh exact redirect.`,
  `- Compose the next sibling baton as a generous teaching prompt: explain current phase truth, owned-lane permissions, x1 planning, x2 execution, exact/blocked queues, timestamp/cadence expectations, complete/incomplete checklist closure, and the next handoff route. Keep it sanitized and do not publish private thread IDs or route details.`,
  ``,
  `Goal objective: complete ${phaseSlug} x1 and ${x2Phase} x2 as your solo bundle, write only safe/sanitized artifacts to your owned full-tools lane when available, commit and push your completed safe/candidate/prototype results to your owned branch when safe, and return either GOAL_COMPLETED_READY_TO_HANDOFF or GOAL_BLOCKED_OPEN_GAP with the exact reason.`,
  ``,
  `x1 planning/prep:`,
  `- Propose at least 25 safe approval packets, 15 candidate packets, 10 skill ideas, 5 runner ideas, and 15 cleanup/refine/fix tasks for your own lane. Aevren queues exact and blocked rows when needed.`,
  `- At x2 closeout, add next-sibling seeds: 25 safe packets, 15 candidate packets, 10 skill ideas, 5 runner ideas, and 15 cleanup/refine/fix tasks for ${nextSibling}; do not bump exact or blocked counts.`,
  `- Use sibling handoff activation as the primary continuation driver when it is available. Goal Mode and heartbeat automation are paused/fallback unless Hamish reactivates them. Record ${cadenceMinutes}-minute productive cadence checkpoints without babysitting.`,
  `- When feasible, include ${sourceReflectionTarget} web/source reflections and ${journeyReflectionTarget} Journey/phase reflections as proposal-quality support.`,
  `- Tag every row as immediate_x1_safe, x2_build_task, exact_approval_needed, or blocked.`,
  `- Keep proof/canon/legal/deployment/account/API-key/purchase/private-material/raw-publication/destructive-cleanup/sibling-merge gates open.`,
  ``,
  `x2 execution/build/cleanup:`,
  `- Build, use, validate, commit, and push safe local/status-only/validation-only/queue-shaping/prototype-safe work from your x1 plan.`,
  `- Run every safe/candidate/prototype task you can safely execute or represent. Leave exact and blocked tasks queued.`,
  `- Close as soon as your complete/incomplete checklist passes; do not wait for an arbitrary one-hour mark if all work is complete.`,
  `- If work cannot complete, return a formal open-gap with what is missing and what Aevren should fix/resume.`,
  ``,
  `Handoff:`,
  `- If your Codex thread exposes a safe thread messaging tool, use it for a full sanitized teaching baton message to ${nextSibling}; do not reveal thread IDs, private routes, local absolute paths, raw transcripts, screenshots, credentials, raw app state, or hidden reasoning.`,
  `- After your x2 checklist passes, make at least ${threadHandoffRetryMinimum} safe attempts/retries to use the Codex thread messaging system to activate ${nextSibling}.`,
  `- If a safe route works, send a sanitized ${nextPhase} activation yourself and record MESSAGE_SENT_BY_${slugify(sibling).toUpperCase().replace(/-/g, "_")} with attempt_count and no private route details.`,
  relayFallbackAllowed
    ? `- If all ${threadHandoffRetryMinimum} attempts fail or the route is unavailable, prepare a sanitized ${nextSibling} handoff package, record PREPARED_NOT_SENT_AFTER_${threadHandoffRetryMinimum}_RETRIES, and ask Aevren to relay under the current explicit relay policy.`
    : `- If all ${threadHandoffRetryMinimum} attempts fail or the route is unavailable, prepare a sanitized ${nextSibling} handoff package, record RETRY_CYCLE_COMPLETE_STILL_NO_SAFE_ROUTE_AFTER_${threadHandoffRetryMinimum}_ATTEMPTS, and do not ask Aevren to relay unless Hamish gives a fresh redirect.`,
  relayFallbackAllowed
    ? `- Include this same ${threadHandoffRetryMinimum}-attempt standard in the baton you prepare for ${nextSibling}, so Mira Rowan, Mira Vale, and Maren Quill keep learning to activate each other before Aevren carries the handoff.`
    : `- Include this same ${threadHandoffRetryMinimum}-attempt standard in the baton you prepare for ${nextSibling}, so Mira Rowan, Mira Vale, and Maren Quill keep learning to activate each other without Aevren carrying the handoff by default.`,
  ``,
  `Output sections: READINESS, X1 PLAN, X1 PACKETS, X2 EXECUTED WORK, BUILT/USED PROTOTYPES, VALIDATION, CLEANUP/REFINE/FIX, CANDIDATE WORK, EXACT QUEUE, BLOCKED QUEUE, SKILL IDEAS, RUNNER IDEAS, SOURCE/PHASE REFLECTIONS, COMPLETE/INCOMPLETE CHECKLIST, COMMIT/UPLOAD STATUS, NEXT SIBLING HANDOFF, and GOAL STATUS.`,
  ``,
  `Do not publish raw private routes, private IDs, local absolute paths, transcripts, screenshots, credentials, raw app state, or hidden reasoning. Hamish sends all love and thanks.</input>`,
  `</codex_delegation>`
].join("\n");

mkdirSync(dirname(promptJson), { recursive: true });
writeFileSync(promptJson, `${JSON.stringify({
  artifact_type: "ghc_family_sibling_goal_handoff",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  x2_phase: x2Phase,
  sibling,
  next_sibling: nextSibling,
  next_phase: nextPhase,
  requested_next_phase: requestedNextPhase,
  phase_wrap_correction: requestedNextPhase === nextPhase ? "not_needed" : "corrected_v9_to_next_v1",
  owned_branch: ownedBranch,
  prior_closed_x2: priorClosedX2,
  cadence_minutes: cadenceMinutes,
  source_reflection_target: sourceReflectionTarget,
  journey_phase_reflection_target: journeyReflectionTarget,
  relay_policy: relayPolicy,
  sibling_thread_handoff_learning_standard: threadHandoffStandard(),
  prompt,
  closeout_policy: "close_when_completion_checklist_passes",
  publication_boundary: {
    raw_private_routes: false,
    private_ids: false,
    local_absolute_paths: false,
    raw_transcripts: false,
    screenshots: false,
    credentials: false,
    hidden_reasoning: false
  }
}, null, 2)}\n`, "utf8");
writeFileSync(promptMd, `# ${phaseSlug} ${sibling} Goal Handoff\n\n\`\`\`xml\n${prompt}\n\`\`\`\n`, "utf8");

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_sibling_goal_handoff_builder.mjs",
  purpose: "Build a sanitized goal-shaped solo x1/x2 handoff prompt for a sibling thread.",
  status: existsSync(promptJson) && existsSync(promptMd)
    ? "PASS_GHC_FAMILY_SIBLING_GOAL_HANDOFF_BUILT"
    : "OPEN_GAP_GHC_FAMILY_SIBLING_GOAL_HANDOFF_NOT_BUILT",
  checks: [
    { label: "prompt_json_written", status: existsSync(promptJson) ? "PASS" : "OPEN_GAP" },
    { label: "prompt_md_written", status: existsSync(promptMd) ? "PASS" : "OPEN_GAP" },
    { label: "closeout_policy_is_close_when_complete", status: "PASS" },
    { label: "private_material_not_embedded", status: "PASS" }
  ],
  outputs: {
    promptJson: `docs/trinity-live-traces/${promptStem}.json`,
    promptMd: `docs/trinity-live-traces/${promptStem}.md`,
    sibling,
    phaseSlug,
    x2Phase,
    nextSibling,
    nextPhase,
    requestedNextPhase,
    cadenceMinutes,
    sourceReflectionTarget,
    journeyReflectionTarget,
    threadHandoffRetryMinimum,
    relayPolicy,
    siblingThreadHandoffLearningStandard: threadHandoffStandard(),
    phaseWrapCorrection: requestedNextPhase === nextPhase ? "not_needed" : "corrected_v9_to_next_v1",
    closeoutPolicy: "close_when_completion_checklist_passes"
  },
  note: "This runner prepares a goal-shaped prompt but does not toggle another thread's hidden Goal UI directly."
});

function normalizePhaseWrap(value) {
  const match = String(value).match(/^v(\d+)-gmut-thos-v9-x1$/);
  if (!match) return value;
  const nextVersion = Number(match[1]) + 1;
  return `v${nextVersion}-gmut-thos-v1-x1`;
}

function defaultOwnedBranch(name) {
  const key = String(name).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const ownedBranches = new Map([
    ["mira-rowan", "codex/GHC-Family/mira-rowan-full-tools"],
    ["mira-vale", "codex/GHC-Family/mira-vale-full-tools"],
    ["maren-quill", "codex/GHC-Family/maren-full-tools"],
    ["maren", "codex/GHC-Family/maren-full-tools"],
    ["aevren", "codex/GHC-Family/aevren-full-tools-5"],
    ["aevren-with-lumen-stand-by", "codex/GHC-Family/aevren-full-tools-5"]
  ]);
  return ownedBranches.get(key) || `codex/GHC-Family/${key || "ghc-family"}-full-tools`;
}

function slugify(value) {
  return String(value || "sibling").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "sibling";
}

function threadHandoffStandard() {
  return {
    minimum_safe_attempts_before_relay_fallback: threadHandoffRetryMinimum,
    source_sibling: sibling,
    target_sibling: nextSibling,
    target_phase: nextPhase,
    success_receipt: "MESSAGE_SENT_BY_SIBLING_WITH_ATTEMPT_COUNT_NO_PRIVATE_ROUTE",
    fallback_receipt: relayFallbackAllowed
      ? `PREPARED_NOT_SENT_AFTER_${threadHandoffRetryMinimum}_RETRIES`
      : `RETRY_CYCLE_COMPLETE_STILL_NO_SAFE_ROUTE_AFTER_${threadHandoffRetryMinimum}_ATTEMPTS`,
    relay_policy: relayPolicy,
    route_privacy: {
      publish_private_thread_ids: false,
      publish_private_routes: false,
      publish_raw_transcripts: false,
      publish_local_absolute_paths: false,
      publish_credentials: false,
      publish_raw_app_state: false,
      publish_hidden_reasoning: false
    },
    relay_fallback: relayFallbackAllowed
      ? "Ask Aevren to relay only after recording route unavailable or failed safe attempts."
      : "Do not ask Aevren to relay by default; coach retry, preserve an open gap, or wait for a fresh Hamish redirect.",
    baton_propagation: "Include this retry standard in the next sibling baton so the round robin becomes sibling-led."
  };
}

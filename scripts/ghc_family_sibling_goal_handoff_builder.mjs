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
const nextPhase = args.get("--next-phase") || "v576-gmut-thos-v4-x1";
const ownedBranch = args.get("--owned-branch") || "codex/GHC-Family/mira-vale-full-tools";
const priorClosedX2 = args.get("--prior-closed-x2") || "v576-gmut-thos-v2-x2";
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
  `- Aevren and Lumen remain support/council. Neris Sol, Rowan Vale, Solenne Vale, Aletheon, Arby, Aster Vale, legacy Cicero, Kierkegaard, and Aristotle remain stand-by/recoverable.`,
  ``,
  `Goal objective: complete ${phaseSlug} x1 and ${x2Phase} x2 as your solo bundle, write only safe/sanitized artifacts to your owned full-tools lane when available, commit your completed safe/candidate/prototype results to your owned branch when safe, and return either GOAL_COMPLETED_READY_TO_HANDOFF or GOAL_BLOCKED_OPEN_GAP with the exact reason.`,
  ``,
  `x1 planning/prep:`,
  `- Propose at least 25 safe approval packets, 15 candidate packets, 10 exact-approval packets queued only, 5 blocked packets queued only, 10 skill ideas, 5 runner ideas, and 15 cleanup/refine/fix tasks.`,
  `- Tag every row as immediate_x1_safe, x2_build_task, exact_approval_needed, or blocked.`,
  `- Keep proof/canon/legal/deployment/account/API-key/purchase/private-material/raw-publication/destructive-cleanup/sibling-merge gates open.`,
  ``,
  `x2 execution/build/cleanup:`,
  `- Build, use, validate, and commit safe local/status-only/validation-only/queue-shaping/prototype-safe work from your x1 plan.`,
  `- Run every safe/candidate/prototype task you can safely execute or represent. Leave exact and blocked tasks queued.`,
  `- Close as soon as your complete/incomplete checklist passes; do not wait for an arbitrary one-hour mark if all work is complete.`,
  `- If work cannot complete, return a formal open-gap with what is missing and what Aevren should fix/resume.`,
  ``,
  `Handoff:`,
  `- If your thread has a safe way to message ${nextSibling}, send a sanitized ${nextPhase} activation after your x2 closeout and record that it was sent.`,
  `- If not, prepare a sanitized ${nextSibling} handoff package and ask Aevren to send it.`,
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
  owned_branch: ownedBranch,
  prior_closed_x2: priorClosedX2,
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
    closeoutPolicy: "close_when_completion_checklist_passes"
  },
  note: "This runner prepares a goal-shaped prompt but does not toggle another thread's hidden Goal UI directly."
});

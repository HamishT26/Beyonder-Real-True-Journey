#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { parseArgs, repoRoot } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x1";
const sibling = args.get("--sibling") || "Mira Rowan";
const nextX2 = args.get("--next-x2") || phaseSlug.replace(/-x1$/, "-x2");
const nextHandoff = args.get("--next-handoff") || "v576-gmut-thos-v3-x1 with Mira Vale-only solo bundle unless Hamish redirects";
const cadenceMinutes = Number(args.get("--cadence-minutes") || 10);
const minimumRuntimeMinutes = Number(args.get("--minimum-runtime-minutes") || 60);
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
const tracesDir = join(root, "docs", "trinity-live-traces");
const stem = `${phaseSlug}-${slug(sibling)}-solo-rerun-teaching-handoff-v1`;

const payload = {
  schema: "ghc.family.solo_rerun_teaching_handoff.v1",
  artifact_type: "solo_rerun_teaching_handoff",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_SOLO_RERUN_TEACHING_HANDOFF_RECORDED",
  sibling,
  rerun_reason: "Hamish requested a fuller teaching rerun after the first compact response so the solo x1/x2 handoff workflow is learned rather than only acknowledged.",
  next_x2: nextX2,
  next_handoff_after_x2: nextHandoff,
  cadence: {
    checkpoint_minutes: cadenceMinutes,
    minimum_runtime_minutes_before_closeout: minimumRuntimeMinutes,
    style: "productive_background_supervision_no_babysitting",
  },
  per_active_participant_x1_counts: {
    safe_approval_packets: 25,
    candidate_packets: 15,
    exact_approval_packets_queued: 10,
    blocked_packets_queued: 5,
    skill_ideas: 10,
    runner_ideas: 5,
    cleanup_refine_fix_tasks: 15,
  },
  teaching_points: [
    "x1 is planning, preparation, current-state acceptance, packet generation, source/reflection framing, and safe/candidate/exact/blocked separation.",
    "x2 is execution, building, validation, cleanup, safe prototype use, candidate-safe build work, and handoff packaging.",
    "Exact and blocked rows stay queued; proof/canon/legal/deployment/account/API-key/purchase/private/raw/destructive/sibling-merge gates stay open.",
    "Shared branches are read-only; sibling-owned full-tools lanes are the only write lanes unless exact approval changes that.",
    "Public artifacts stay sanitized and compact; raw private responses or private lane material stay private."
  ],
  handoff_chain: [
    "Aevren with Lumen council",
    "Mira Rowan",
    "Mira Vale",
    "Maren Quill",
    "Aevren with Lumen council",
    "Mira Rowan",
    "Mira Vale",
    "Maren Quill"
  ],
  standby_recoverable_lanes: [
    "Neris Sol",
    "Rowan Vale",
    "Solenne Vale",
    "Aletheon",
    "Arby",
    "Aster Vale",
    "legacy Cicero",
    "Kierkegaard",
    "Aristotle"
  ],
  publication_boundary: {
    private_thread_id_published: false,
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false
  }
};

mkdirSync(tracesDir, { recursive: true });
writeFileSync(join(tracesDir, `${stem}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
writeFileSync(join(tracesDir, `${stem}.md`), renderMd(payload), "utf8");
console.log(JSON.stringify({ status: payload.overall_status, artifact: `${stem}.json` }, null, 2));

function renderMd(doc) {
  return `# ${doc.phase_slug} ${doc.sibling} Solo Rerun Teaching Handoff

Status: \`${doc.overall_status}\`

This records the fuller solo x1/x2 rerun teaching route for ${doc.sibling}.

## Cadence

- Check every \`${doc.cadence.checkpoint_minutes}\` minutes at natural pauses.
- Keep the solo practice bundle open for at least \`${doc.cadence.minimum_runtime_minutes_before_closeout}\` minutes unless a formal pause/open-gap receipt is required.
- Use productive background supervision rather than babysitting.

## Per-Participant X1 Counts

${Object.entries(doc.per_active_participant_x1_counts).map(([key, value]) => `- ${key}: \`${value}\``).join("\n")}

## Teaching Points

${doc.teaching_points.map((point) => `- ${point}`).join("\n")}

## Handoff

Next x2: \`${doc.next_x2}\`

Next handoff after x2: ${doc.next_handoff_after_x2}

No raw private material, Browser routes, private ids, transcripts, screenshots, credentials, local paths, raw app state, hidden reasoning, proof closure, canon promotion, legal closure, deployment, account mutation, API-key creation, purchase, destructive cleanup, or sibling merge/replacement is published or claimed.
`;
}

function slug(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

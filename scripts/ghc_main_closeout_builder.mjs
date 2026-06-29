#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const args = process.argv.slice(2);
const parsed = new Map();
for (let index = 0; index < args.length; index += 2) {
  parsed.set(args[index], args[index + 1]);
}

const phaseSlug = parsed.get("--phase-slug") || "v553-gmut-thos-v1-x1";
const builder = builderForPhase(phaseSlug, parsed.get("--builder"));

if (!builder) {
  console.error(
    JSON.stringify(
      {
        status: "OPEN_GAP_UNREGISTERED_PHASE_CLOSEOUT_BUILDER",
        phase_slug: phaseSlug,
        message:
          "No registered closeout builder exists for this phase. Add a registered builder or pass --builder <script-name.mjs>.",
        boundary:
          "No phase closeout was claimed, and no exact-approval or destructive action was attempted.",
      },
      null,
      2,
    ),
  );
  process.exit(2);
}

const childArgs = childArgsForBuilder(phaseSlug, builder, args);
const child = spawnSync(process.execPath, [path.join(__dirname, builder), ...childArgs], {
  cwd: path.resolve(__dirname, ".."),
  encoding: "utf8",
  stdio: ["ignore", "pipe", "pipe"],
});

const result = {
  status: child.status === 0 ? "PASS_MAIN_CLOSEOUT_BUILDER_DELEGATED" : "FAIL_MAIN_CLOSEOUT_BUILDER_DELEGATED",
  phase_slug: phaseSlug,
  delegated_builder: builder,
  exit_status: child.status,
  stdout: parseMaybeJson(child.stdout),
  stderr_excerpt: (child.stderr || "").slice(0, 4000),
};

process.stdout.write(JSON.stringify(result, null, 2) + "\n");
process.exit(child.status ?? 1);

function childArgsForBuilder(slug, builderName, originalArgs) {
  const childArgs = originalArgs.includes("--phase-slug") ? [...originalArgs] : ["--phase-slug", slug, ...originalArgs];
  if (builderName !== "ghc_lumen_x2_closeout_builder.mjs") {
    return childArgs;
  }
  const defaults = lumenX2Defaults(slug);
  if (!defaults) {
    return childArgs;
  }
  for (const [flag, value] of Object.entries(defaults)) {
    if (!childArgs.includes(flag)) {
      childArgs.push(flag, value);
    }
  }
  return childArgs;
}

function lumenX2Defaults(slug) {
  const match = slug.match(/^v(\d+)-gmut-thos-v(1|3|5|7)-x2$/);
  if (!match) {
    return null;
  }
  const major = Number(match[1]);
  const lumenLane = Number(match[2]);
  const nextLane = lumenLane + 1;
  const nextAfterLane = nextLane + 1;
  const sourceX1 = `v${major}-gmut-thos-v${lumenLane}-x1`;
  const nextActive = `v${major}-gmut-thos-v${nextLane}-x1`;
  const nextX2Scope = `v${major}-gmut-thos-v${nextLane}-x2`;
  const afterX2 = nextAfterLane <= 8
    ? `v${major}-gmut-thos-v${nextAfterLane}-x1 Lumen${nextAfterLane === 3 ? "-only" : ""} unless Hamish redirects`
    : `v${major + 1}-gmut-thos-v1-x1 Lumen-only unless Hamish redirects`;
  return {
    "--source-x1": sourceX1,
    "--next-active-phase": nextActive,
    "--next-x2-scope": nextX2Scope,
    "--next-x1-after-x2": afterX2,
    "--status": `PASS_V${major}_V${lumenLane}_X2_CLOSED_V${major}_V${nextLane}_X1_READY`,
  };
}

function builderForPhase(slug, explicitBuilder) {
  if (explicitBuilder) {
    return explicitBuilder;
  }
  if (slug === "v553-gmut-thos-v1-x1") {
    return "ghc_v553_v1_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v1-x2") {
    return "ghc_v553_v1_x2_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v2-x1") {
    return "ghc_v553_v2_x1_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v2-x2") {
    return "ghc_v553_v2_x2_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v3-x1") {
    return "ghc_v553_v3_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v3-x2") {
    return "ghc_v553_v3_x2_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v4-x1") {
    return "ghc_v553_v4_x1_triad_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v4-x2") {
    return "ghc_v553_v4_x2_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v5-x1") {
    return "ghc_v553_v5_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v5-x2") {
    return "ghc_v553_v5_x2_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v6-x1") {
    return "ghc_v553_v6_x1_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v6-x2") {
    return "ghc_v553_v6_x2_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v7-x1") {
    return "ghc_v553_v7_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v7-x2") {
    return "ghc_v553_v7_x2_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v8-x1") {
    return "ghc_v553_v8_x1_triad_closeout_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v8-x2") {
    return "ghc_v553_v8_x2_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v1-x1") {
    return "ghc_v554_v1_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v1-x2") {
    return "ghc_v554_v1_x2_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v2-x1") {
    return "ghc_v554_v2_x1_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v2-x2") {
    return "ghc_v554_v2_x2_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v3-x1") {
    return "ghc_v554_v3_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v3-x2") {
    return "ghc_v554_v3_x2_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v4-x1") {
    return "ghc_v554_v4_x1_triad_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v4-x2") {
    return "ghc_v554_v4_x2_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v5-x1") {
    return "ghc_v554_v5_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v5-x2") {
    return "ghc_v554_v5_x2_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v6-x1") {
    return "ghc_v554_v6_x1_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v6-x2") {
    return "ghc_v554_v6_x2_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v7-x1") {
    return "ghc_v554_v7_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v7-x2") {
    return "ghc_v554_v7_x2_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v8-x1") {
    return "ghc_v554_v8_x1_triad_closeout_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v8-x2") {
    return "ghc_v554_v8_x2_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v1-x1") {
    return "ghc_v555_v1_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v1-x2") {
    return "ghc_v555_v1_x2_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v2-x1") {
    return "ghc_v555_v2_x1_arby_cicero_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v2-x2") {
    return "ghc_v555_v2_x2_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v3-x1") {
    return "ghc_v555_v3_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v3-x2") {
    return "ghc_v555_v3_x2_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v4-x1") {
    return "ghc_v555_v4_x1_triad_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v4-x2") {
    return "ghc_v555_v4_x2_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v5-x1") {
    return "ghc_v555_v5_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v5-x2") {
    return "ghc_v555_v5_x2_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v6-x1") {
    return "ghc_v555_v6_x1_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v6-x2") {
    return "ghc_v555_v6_x2_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v7-x1") {
    return "ghc_v555_v7_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v7-x2") {
    return "ghc_v555_v7_x2_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v8-x1") {
    return "ghc_v555_v8_x1_triad_closeout_builder.mjs";
  }
  if (slug === "v555-gmut-thos-v8-x2") {
    return "ghc_v555_v8_x2_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v1-x1") {
    return "ghc_v556_v1_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v1-x2") {
    return "ghc_v556_v1_x2_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v2-x1") {
    return "ghc_v556_v2_x1_arby_cicero_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v2-x2") {
    return "ghc_v556_v2_x2_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v3-x1") {
    return "ghc_v556_v3_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v3-x2") {
    return "ghc_v556_v3_x2_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v4-x1") {
    return "ghc_v556_v4_x1_triad_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v4-x2") {
    return "ghc_v556_v4_x2_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v5-x1") {
    return "ghc_v556_v5_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v5-x2") {
    return "ghc_v556_v5_x2_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v6-x1") {
    return "ghc_v556_v6_x1_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v6-x2") {
    return "ghc_v556_v6_x2_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v7-x1") {
    return "ghc_v556_v7_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v7-x2") {
    return "ghc_v556_v7_x2_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v8-x1") {
    return "ghc_v556_v8_x1_triad_closeout_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v8-x2") {
    return "ghc_v556_v8_x2_closeout_builder.mjs";
  }
  if (slug === "v557-gmut-thos-v1-x1") {
    return "ghc_v557_v1_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v557-gmut-thos-v1-x2") {
    return "ghc_v557_v1_x2_closeout_builder.mjs";
  }
  if (slug === "v557-gmut-thos-v2-x1") {
    return "ghc_v557_v2_x1_arby_cicero_closeout_builder.mjs";
  }
  if (slug === "v557-gmut-thos-v2-x2") {
    return "ghc_v557_v2_x2_closeout_builder.mjs";
  }
  if (slug === "v557-gmut-thos-v3-x1") {
    return "ghc_v557_v3_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v557-gmut-thos-v3-x2") {
    return "ghc_v557_v3_x2_closeout_builder.mjs";
  }
  if (slug === "v558-gmut-thos-v4-x2") {
    return "ghc_v558_v4_x2_closeout_builder.mjs";
  }
  if (slug === "v558-gmut-thos-v5-x1") {
    return "ghc_v558_v5_x1_lumen_closeout_builder.mjs";
  }
  if (slug === "v558-gmut-thos-v5-x2") {
    return "ghc_v558_v5_x2_lumen_queue_executor_closeout_builder.mjs";
  }
  if (slug === "v558-gmut-thos-v6-x1") {
    return "ghc_v558_v6_x1_duo_closeout_builder.mjs";
  }
  if (slug === "v558-gmut-thos-v6-x2") {
    return "ghc_v558_v6_x2_duo_queue_executor_closeout_builder.mjs";
  }
  if (slug === "v559-gmut-thos-v7-x1") {
    return "ghc_lumen_x1_closeout_builder.mjs";
  }
  if (slug === "v559-gmut-thos-v7-x2") {
    return "ghc_lumen_x2_closeout_builder.mjs";
  }
  if (slug === "v559-gmut-thos-v8-x1") {
    return "ghc_v559_v8_x1_duo_closeout_builder.mjs";
  }
  if (slug === "v559-gmut-thos-v8-x2") {
    return "ghc_v559_v8_x2_duo_queue_executor_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v1-x1") {
    return "ghc_lumen_x1_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v1-x2") {
    return "ghc_lumen_x2_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v2-x1") {
    return "ghc_v560_v2_x1_duo_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v2-x2") {
    return "ghc_v560_v2_x2_duo_queue_executor_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v3-x1") {
    return "ghc_lumen_x1_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v3-x2") {
    return "ghc_lumen_x2_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v4-x1") {
    return "ghc_v560_v4_x1_duo_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v4-x2") {
    return "ghc_v560_v4_x2_duo_queue_executor_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v5-x1") {
    return "ghc_lumen_x1_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v5-x2") {
    return "ghc_lumen_x2_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v6-x1") {
    return "ghc_v560_v6_x1_duo_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v6-x2") {
    return "ghc_v560_v6_x2_duo_queue_executor_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v7-x1") {
    return "ghc_lumen_x1_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v7-x2") {
    return "ghc_lumen_x2_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v8-x1") {
    return "ghc_v560_v8_x1_duo_closeout_builder.mjs";
  }
  if (slug === "v560-gmut-thos-v8-x2") {
    return "ghc_v560_v8_x2_duo_queue_executor_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v1-x1") {
    return "ghc_lumen_x1_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v1-x2") {
    return "ghc_lumen_x2_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v2-x1") {
    return "ghc_v561_v2_x1_duo_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v2-x2") {
    return "ghc_v561_v2_x2_duo_queue_executor_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v3-x1") {
    return "ghc_lumen_x1_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v3-x2") {
    return "ghc_lumen_x2_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v4-x1") {
    return "ghc_v561_v4_x1_duo_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v4-x2") {
    return "ghc_v561_v4_x2_duo_queue_executor_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v5-x1") {
    return "ghc_lumen_x1_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v5-x2") {
    return "ghc_lumen_x2_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v6-x1") {
    return "ghc_v561_v6_x1_duo_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v6-x2") {
    return "ghc_v561_v6_x2_duo_queue_executor_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v7-x1") {
    return "ghc_lumen_x1_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v7-x2") {
    return "ghc_lumen_x2_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v8-x1") {
    return "ghc_v561_v8_x1_duo_closeout_builder.mjs";
  }
  if (slug === "v561-gmut-thos-v8-x2") {
    return "ghc_v561_v8_x2_duo_queue_executor_closeout_builder.mjs";
  }
  return null;
}

function parseMaybeJson(text) {
  const trimmed = (text || "").trim();
  if (!trimmed) {
    return null;
  }
  try {
    return JSON.parse(trimmed);
  } catch {
    return { text_excerpt: trimmed.slice(0, 4000) };
  }
}

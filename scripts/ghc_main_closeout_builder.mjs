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

const childArgs = args.includes("--phase-slug") ? args : ["--phase-slug", phaseSlug, ...args];
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

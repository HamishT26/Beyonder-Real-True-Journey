#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");

const args = process.argv.slice(2);
const parsed = new Map();
for (let index = 0; index < args.length; index += 2) {
  parsed.set(args[index], args[index + 1]);
}

const phaseSlug = parsed.get("--phase-slug") || readCurrentPhase() || "unknown";
const explicitBuilder = parsed.get("--builder");
const builder = builderForPhase(phaseSlug, explicitBuilder);

if (builder) {
  const childArgs = args.includes("--phase-slug") ? args : ["--phase-slug", phaseSlug, ...args];
  runChild(builder, childArgs, "PASS_MAIN_STARTUP_BUILDER_DELEGATED");
} else {
  const receiptPrefix = parsed.get("--receipt-prefix") || `${phaseSlug}-main-startup-context`;
  runChild(
    "ghc_phase_startup_context_updater.mjs",
    [
      "--root",
      repoRoot,
      "--phase-slug",
      phaseSlug,
      "--event",
      parsed.get("--event") || "startup",
      "--agent",
      parsed.get("--agent") || "Aevren Vale",
      "--receipt-prefix",
      receiptPrefix,
    ],
    "PASS_MAIN_STARTUP_BUILDER_GENERIC_UPDATER",
  );
}

function runChild(scriptName, childArgs, passStatus) {
  const child = spawnSync(process.execPath, [path.join(__dirname, scriptName), ...childArgs], {
    cwd: repoRoot,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    windowsHide: true,
    maxBuffer: 1024 * 1024,
  });
  const result = {
    status: child.status === 0 ? passStatus : "FAIL_MAIN_STARTUP_BUILDER_DELEGATED",
    phase_slug: phaseSlug,
    delegated_builder: scriptName,
    exit_status: child.status,
    stdout: parseMaybeJson(child.stdout),
    stderr_excerpt: (child.stderr || "").slice(0, 4000),
  };
  process.stdout.write(JSON.stringify(result, null, 2) + "\n");
  process.exit(child.status ?? 1);
}

function builderForPhase(slug, explicit) {
  if (explicit) {
    return explicit;
  }
  if (slug === "v553-gmut-thos-v1-x1") {
    return "ghc_v553_v1_x1_lumen_startup_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v3-x1") {
    return "ghc_v553_v3_x1_lumen_startup_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v7-x1") {
    return "ghc_v553_v7_x1_lumen_startup_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v7-x2") {
    return "ghc_v553_v7_x2_startup_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v8-x1") {
    return "ghc_v553_v8_x1_triad_workbench_builder.mjs";
  }
  if (slug === "v553-gmut-thos-v8-x2") {
    return "ghc_v553_v8_x2_startup_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v1-x1") {
    return "ghc_v554_v1_x1_lumen_startup_builder.mjs";
  }
  if (slug === "v554-gmut-thos-v3-x1") {
    return "ghc_v554_v3_x1_lumen_startup_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v2-x1") {
    return "ghc_v556_v2_x1_arby_cicero_startup_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v3-x1") {
    return "ghc_v556_v3_x1_lumen_startup_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v5-x1") {
    return "ghc_v556_v5_x1_lumen_startup_builder.mjs";
  }
  if (slug === "v556-gmut-thos-v6-x1") {
    return "ghc_v556_v6_x1_duo_phase_builder.mjs";
  }
  return null;
}

function readCurrentPhase() {
  const file = path.join(repoRoot, "docs", "omega-mini-index", "omega-mini-current-state-v1.json");
  if (!fs.existsSync(file)) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(file, "utf8")).current_active_phase || null;
  } catch {
    return null;
  }
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

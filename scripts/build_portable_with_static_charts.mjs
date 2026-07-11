#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [inputName, outputName, pluginRootArg] = process.argv.slice(2);
const pluginRoot = pluginRootArg || process.env.CODEX_DATA_ANALYTICS_PLUGIN_ROOT;
if (!inputName || !outputName || !pluginRoot) {
  throw new Error(
    "usage: node build_portable_with_static_charts.mjs artifact.json output.html <data-analytics-plugin-root>\n" +
      "or set CODEX_DATA_ANALYTICS_PLUGIN_ROOT",
  );
}
const reportScripts = join(resolve(pluginRoot), "skills", "build-report", "scripts");
const { buildPortableArtifact } = await import(pathToFileURL(join(reportScripts, "build_portable_artifact.mjs")).href);
const { extractPortableChartSvgs } = await import(pathToFileURL(join(reportScripts, "extract_portable_chart_svgs.mjs")).href);
const inputPath = resolve(inputName);
const outputPath = resolve(outputName);
const input = JSON.parse(readFileSync(inputPath, "utf8"));
writeFileSync(outputPath, buildPortableArtifact(input), "utf8");
const staticCharts = await extractPortableChartSvgs({
  actionTimeoutMs: 15000,
  htmlPath: outputPath,
  readyTimeoutMs: 30000,
});
writeFileSync(outputPath, buildPortableArtifact(input, { staticCharts }), "utf8");
process.stdout.write(JSON.stringify({ output: outputPath, chartCount: Object.keys(staticCharts).length }) + "\n");

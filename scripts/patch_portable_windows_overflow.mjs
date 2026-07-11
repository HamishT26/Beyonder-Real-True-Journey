#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const [inputName, outputName] = process.argv.slice(2);
if (!inputName || !outputName) {
  throw new Error("usage: node patch_portable_windows_overflow.mjs input.html output.html");
}
const inputPath = resolve(inputName);
const outputPath = resolve(outputName);
const html = readFileSync(inputPath, "utf8");
const marker = "</head>";
if (!html.includes(marker)) throw new Error("portable report has no closing head element");
const style = [
  '<style data-eiren-windows-overflow-compat="true">',
  'html,body{max-width:100%;overflow-x:hidden}',
  '</style>',
].join("");
const patched = html.replace(marker, `${style}${marker}`);
writeFileSync(outputPath, patched, "utf8");
process.stdout.write(JSON.stringify({ input: inputPath, output: outputPath, patch: "windows_classic_scrollbar_overflow_guard" }) + "\n");

#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const path = require("node:path");

function count(text, pattern) {
  return [...text.matchAll(pattern)].length;
}

function diagnose(html) {
  const fixedWidths = [...html.matchAll(/(?<!max-)(?:width|min-width)\s*:\s*(\d{4,})px/gi)].map(
    (match) => Number(match[1]),
  );
  const findings = {
    viewport_meta_present: /<meta[^>]+name=["']viewport["']/i.test(html),
    horizontal_overflow_rules: count(html, /overflow-x\s*:/gi),
    responsive_media_rules: count(html, /max-width\s*:\s*100%/gi),
    wide_fixed_width_count: fixedWidths.length,
    widest_fixed_width_px: fixedWidths.length ? Math.max(...fixedWidths) : null,
    table_count: count(html, /<table\b/gi),
    pre_count: count(html, /<pre\b/gi),
    svg_count: count(html, /<svg\b/gi),
    image_count: count(html, /<img\b/gi),
  };
  const risks = [];
  if (!findings.viewport_meta_present) risks.push("missing_viewport_meta");
  if (findings.wide_fixed_width_count) risks.push("wide_fixed_css_width");
  if (findings.table_count && !findings.horizontal_overflow_rules) {
    risks.push("tables_without_explicit_horizontal_overflow_rule");
  }
  if ((findings.svg_count || findings.image_count) && !findings.responsive_media_rules) {
    risks.push("media_without_detected_max_width_rule");
  }
  return {
    schema: "ghc.family.portable-overflow-diagnostic.v1",
    findings,
    risks,
    status: risks.length ? "review_required" : "no_static_overflow_risk_detected",
    limitation: "Static pattern inspection does not replace browser viewport or PDF export review.",
  };
}

function main(argv) {
  if (argv.length < 1 || argv.length > 2) {
    throw new Error("usage: node ghc_family_diagnose_portable_overflow.cjs input.html [output.json]");
  }
  const [input, output] = argv;
  const result = diagnose(fs.readFileSync(input, "utf8"));
  result.input_basename = path.basename(input);
  const serialized = `${JSON.stringify(result, null, 2)}\n`;
  if (output) fs.writeFileSync(output, serialized, "utf8");
  process.stdout.write(serialized);
  process.exitCode = result.status === "review_required" ? 2 : 0;
}

if (require.main === module) main(process.argv.slice(2));

module.exports = { diagnose };

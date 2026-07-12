#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const { pathToFileURL } = require("node:url");
const { chromium } = require("playwright");

async function main() {
  const [input, output, screenshot] = process.argv.slice(2);
  if (!input || !output || process.argv.length > 5) {
    throw new Error("usage: node ghc_family_render_html_pdf.cjs input.html output.pdf [screenshot.png]");
  }
  if (!fs.existsSync(input)) throw new Error(`input not found: ${input}`);
  fs.mkdirSync(path.dirname(output), { recursive: true });
  if (screenshot) fs.mkdirSync(path.dirname(screenshot), { recursive: true });
  const launchOptions = { headless: true };
  if (process.env.GHC_BROWSER_EXECUTABLE) {
    launchOptions.executablePath = process.env.GHC_BROWSER_EXECUTABLE;
  }
  const browser = await chromium.launch(launchOptions);
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
    await page.goto(pathToFileURL(path.resolve(input)).href, { waitUntil: "networkidle" });
    await page.emulateMedia({ media: "print", colorScheme: "light", reducedMotion: "reduce" });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: output,
      format: "A4",
      printBackground: true,
      preferCSSPageSize: true,
      tagged: true,
      outline: true,
    });
    if (screenshot) {
      await page.emulateMedia({ media: "screen", colorScheme: "light", reducedMotion: "reduce" });
      await page.screenshot({ path: screenshot, fullPage: true });
    }
    const result = await page.evaluate(() => {
      const documentScrollWidth = Math.max(
        document.documentElement.scrollWidth,
        document.body.scrollWidth,
      );
      return {
        title: document.title,
        tables: document.querySelectorAll("table").length,
        links: document.querySelectorAll("a[href]").length,
        viewportWidth: window.innerWidth,
        documentScrollWidth,
        horizontalOverflow: documentScrollWidth > window.innerWidth + 1,
        textLength: document.body.innerText.length,
      };
    });
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    if (result.horizontalOverflow) process.exitCode = 2;
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exit(1);
});

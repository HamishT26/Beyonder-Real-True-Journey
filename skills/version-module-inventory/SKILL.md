---
name: version-module-inventory
description: Build a per-version module inventory table across Beyonder Journey artifacts, showing what was introduced, refined, and validated.
---

# Version Module Inventory

Use when the user requests a timeline table across versions (v13-v33, v29, etc.).

## Workflow
1. Collect available artifacts by version (`rg --files`).
2. Extract module/system clues from docs, code, and extracted appendices.
3. Build a table with columns:
   - Version
   - Introduced/emphasized modules
   - Refined/validated status
4. Flag uncertain rows explicitly as pending evidence.

## Quality bar
- Do not over-claim from unreadable PDFs.
- Link each non-trivial row to at least one source citation.

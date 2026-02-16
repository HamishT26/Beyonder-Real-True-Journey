---
name: qcit-ocr-validation
description: Validate QCIT/QCfT terminology and definitions from Beyonder v33 artifacts using reproducible extraction steps, with explicit handling of OCR/tooling limitations.
---

# QCIT OCR Validation

Use this skill when the user asks to confirm QCIT/QCfT language in v33 PDFs and align it with repo specs.

## Workflow
1. Extract structural text from the target PDF (`strings -n 8`) and capture heading-level evidence.
2. Cross-check the extracted structure against `quantum_to_classical_transmuter.md`.
3. Record exact commands used and store evidence in a docs appendix.
4. If OCR binaries are unavailable, mark the limitation and provide a concrete external OCR follow-up plan.

## Output requirements
- Include a short **confidence statement** (high/medium/low).
- Separate **confirmed text** from **inferred text**.
- Add file citations to synthesis output.

See `references/ocr-checklist.md` for command templates and evidence format.

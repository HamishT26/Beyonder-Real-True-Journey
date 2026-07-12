# v641 embedded visualization inventory and mini-briefs

## Layer 1 — outcome disposition bar

- **Story job:** show that all eighty units were processed while preserving incomplete and exact-gated outcomes.
- **Data shape:** four disposition counts summing to eighty.
- **Primary specialist:** visualization strategy and critique; supporting: accessibility, testing, report/PDF automation.
- **Encoding:** one horizontal stacked bar, directly labelled segments, blue completed, gold represented, rust open gap, violet exact gate; color is redundant with text and pattern/border.
- **Fallback/accessibility:** adjacent count table and long description; no hover dependency.
- **QA:** count sum equals 80; labels remain visible at 375 px and print width; grayscale distinction checked by borders/text.
- **Fresh pass:** local specialist pass; subagent delegation intentionally not used.

## Layer 2 — 10-by-8 mission matrix

- **Story job:** preserve the original ten missions and eight functions inside the compressed pilot.
- **Data shape:** categorical 10-by-8 matrix.
- **Primary specialist:** visualization strategy and critique; supporting: accessibility, testing, report/PDF automation.
- **Encoding:** compact table-graphic with direct status tokens; rows are missions, columns are functions.
- **Fallback/accessibility:** semantic HTML table and full Markdown table.
- **QA:** exactly eighty cells; every cell links to the ledger disposition.
- **Fresh pass:** local specialist pass.

## Layer 3 — Stage 20 evidence ladder

- **Story job:** distinguish specification, internal testing, external support, and independent reproduction.
- **Data shape:** twelve claims with ordinal E0-E4 grades and state.
- **Primary specialist:** visualization strategy and critique; supporting: accessibility, testing, report/PDF automation.
- **Encoding:** ranked evidence table with direct grade labels; no decorative mandala or 3D layer.
- **Fallback/accessibility:** complete text description and JSON table.
- **QA:** each claim has evidence, owner, review date, and rejection/promotion condition; no GMUT unique claim is visually promoted above its evidence.
- **Fresh pass:** local specialist pass.

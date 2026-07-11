# Validation manifest

Validated on 11 July 2026 after the Node, npm, and Git updates.

| Gate | Result | Evidence boundary |
|---|---:|---|
| GMUT deterministic tests | `15/15 PASS` | algebra, conservation identities, toy integration, and rejection gates; not empirical cosmology |
| Term registry | `PASS`, zero issues | physical terms require rank, units, action, null limit, observable, and falsifier |
| Coefficient ledger | `PASS`, zero issues | every row carries domain, units, prior/range, null condition, observable, and rejection rule |
| JSON corpus | `9/9 parsed` | syntax and structure only; the individual validators supply semantic checks |
| Python sources | `PASS` | all new Python modules compile |
| Node helper sources | `PASS` | both new MJS helpers pass `node --check` under Node 24.18.0 |
| Portable HTML report | `PASS` | 15 blocks, two charts, three metrics, three tables, source dialog, and responsive checks at 1440 px and 390 px |
| DOCX structure/layout boundaries | `19/19 PASS` | Letter geometry, exact business-brief styles, 49 body-width tables, three visuals, 61 links, OOXML integrity, and path/privacy checks |
| DOCX native open | `PASS` | final DOCX opened read-only in Microsoft Word with 1,614 rendered paragraphs and 49 tables |
| DOCX page raster | `BLOCKED` | bundled LibreOffice is unavailable; Word PDF export also timed out on an unrelated control DOCX, so no page-raster claim is made |
| LaTeX monograph | `PASS` | Tectonic 0.16.9 produced a ten-page Letter PDF; all ten pages were visually inspected |
| PDF safety metadata | `PASS` | unencrypted, no JavaScript, ten pages, Letter size |
| Journey coverage | `19/19 versions` | all available v36-v54 variants were hashed and duplicate groups recorded |
| Live round-robin coverage | `4 lanes × 40/40 versions` | clean/upstream-equal state was verified at the stated audit timestamp; counts are not novelty scores |

## Security boundary

The scoped new-artifact privacy and secret-pattern scan is part of closeout. The exhaustive Codex Security workflow was not claimed because its required delegated subagent scan conflicts with Hamish's explicit no-agent-spawning rule. Legacy corpus secrets or private registry material were not reproduced.

## Publication boundary

Exact staging, diff review, push, and upstream-head equality are closeout gates. Their final commit identifier belongs in the task handoff rather than inside a self-referential receipt.

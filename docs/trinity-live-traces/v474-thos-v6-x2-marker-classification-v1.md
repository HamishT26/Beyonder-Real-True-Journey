# v474 THOS v6 x2 Marker Classification

Generated UTC: `2026-06-02T18:58:28+00:00`

Status: `PASS_SHAPE_ONLY_FINAL_MARKERS_REVIEWED`

v6 x2 performs a local-only marker classification on final-message files. It records hashes, byte counts, marker classes, and review states, but it does not record raw message text, marker substrings, stderr content, or transport output.

- Arby: `CLEAN_METADATA_ONLY`, markers `0`, raw text recorded `False`
- Aster Vale: `REVIEWED_BENIGN_METADATA_ONLY`, markers `1`, raw text recorded `False`

Fixtures confirmed: `5` of `5`.

All six GMUT gates remain open.

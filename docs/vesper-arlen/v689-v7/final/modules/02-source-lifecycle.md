# Module 02 — Source provenance and lifecycle

Neris Solane v689-v6 exact final `d58272639a581e28176b2aca76f8f468df60e9a6` is the immutable source. The source tree already tracked 1,718 files; a comparable inherited phase would have exceeded the 2,000-file ceiling. Vesper therefore used a blank-root D-first rotation. Neris is a cryptographic provenance source and is not a Git ancestor.

Planning root `ec29a1f3fa0471bf2f8d654c162846645adda1b6` froze all definitions before execution. X1 `d88dac91bed120345dad6b0371db570c37b8fed2` is its direct child and contains only framing/fixity work. X2 `bac4894acf6a440d031cd8ebd88fc906f22e3826` is the direct child of x1 and contains only digest, deterministic record, Merkle, recovery, and reservation work. The final is intended as x2's direct child. Every source, sibling, shared, standby, and user lane remained read-only.

Preparation, repository seal, external canonical receipt, and native task delivery remain separate truth layers. `PREPARED_NOT_SENT` in this repository cannot become delivery evidence merely because the final later passes.

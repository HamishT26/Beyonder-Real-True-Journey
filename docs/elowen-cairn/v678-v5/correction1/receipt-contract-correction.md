# Elowen Cairn v678-v5 correction1 — frontmatter-aware document predicate

## Retained failure

The one attributable owner-scoped canonical aggregate at retained first final `831f948e326e3875ef0d5d7391560297ce0e2ee8` remains `INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL`, with invocation count one, success count zero, replay count zero, and zero aggregate-success credit. Its immutable receipt SHA-256 is `bfa2115b166ee9eb5f3f9aaac9a4d7f5379e574a24ac4dc60bc7b8accf758ccd` and canonical payload SHA-256 is `36f8a96bb375543e02e6095e34002dbef4bb83b78d51d25095b59b889ed66507`. The receipt proves that 34 tests, 1,412 manifest entries, 642 JSON parses, privacy adjudication, bounded changed-code review, topology, clean state, typed divergence, and fresh equality passed. None may be replayed by correction1.

The sole failed predicate was `documents_structurally_bounded`. It rejected exactly twenty official owner-local `SKILL.md` files because those files correctly begin with YAML frontmatter. Their Markdown headings follow the closing delimiter. This is a validator-shape defect, not a defect in the skill documents.

## Narrow correction

Correction1 adds a phase-local validator that accepts either ordinary Markdown beginning with a heading or an official `SKILL.md` beginning with a closed YAML frontmatter block and containing at least one Markdown heading afterward. HTML continues to require title, main, and level-one-heading structure. The failed dependency may execute exactly once at the additive corrected final. The component also checks only new-head topology, correction manifests, changed-code compilation and bounded security, changed-file privacy, clean state, typed divergence, and fresh equality. It imports every successful first-final observation by immutable receipt hash and does not rerun x1, x2, final tests, old manifest replays, all JSON parsing, old privacy scans, or old security scans.

Repository correction truth and the later external component remain separate. The repository overlay preserves two new failed witnesses and one bounded memory-path recovery. If and only if the external document component passes, its separate `EC6785-CORR-EXT-P001` passing witness raises effective methods and passing witnesses by one without changing negatives, failed witnesses, gaps, gates, outcomes, or the terminal verdict. `NOT_READY_FOR_STAGE_20` remains exact.

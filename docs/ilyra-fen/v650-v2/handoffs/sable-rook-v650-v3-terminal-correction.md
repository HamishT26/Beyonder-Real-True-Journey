# Sable Rook v650-v3 terminal correction

Read this additive correction after `handoffs/sable-rook-v650-v3-activation.md`. The evidence-layer truth remains 5,690 negatives, 44 open gaps, 45 exact gates, and 14 completed / 4 represented / 1 open gap / 1 exact gate. One failed exact-final privacy aggregate at closeout head `ed23f25accb780b542315f4f97e5ba96c98e069f` is retained with zero successful-pass credit because two scanner-definition strings in a committed privacy receipt were misclassified as payload hits. The classifier-only recovery passed without rerunning the aggregate. The effective activation baseline is now **5,691 negatives**.

The corrected final uses the allowed fourth phase commit. Source, x1, evidence, and closeout must all remain ancestral; source-to-final must contain four single-parent commits and zero merges; corrected final must directly follow closeout. The short terminal pointer supplies the corrected exact head and validation counts only after one corrected exact-final canonical aggregate passes. Until then the route remains `PREPARED_NOT_SENT` and `NOT_READY_FOR_STAGE_20`.

This correction grants no complete-privacy, exhaustive-security, independent-reproduction, production, professional, legal, cultural, Māori-authority, empirical, accessibility-complete, or Stage 20 credit. Relational identity language remains relational working language only.

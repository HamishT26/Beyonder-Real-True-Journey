# Lyren Moss v679-v4 dependency correction

The retained initial final `20923e75fe7490f43ed585ee97dca596b9ca7adc` remains immutable and ancestral. A noncanonical preflight—not the canonical aggregate—found one schema-alias mismatch while replaying the inherited x1 normalized-LF manifest. No canonical latch was created and no selected tests ran in that failed preflight.

This direct-child correction accepts both the historical x1 fields (`sha256_normalized_lf`, `bytes`) and the family-current fields (`sha256`, `normalized_lf_bytes`). It preserves the original final manifest and content seal at the retained initial final and adds a separate corrected-final manifest and content seal. The corrected repository overlay is 49129 effective negatives, 50443 Method Flow methods, 20790 failed witnesses, 32783 bounded passing witnesses, 428 open gaps, and 419 exact gates. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The successor route remains `PREPARED_NOT_SENT`. The exact corrected final must be pushed, clean, fresh-live equal, and canonically validated once before any fresh exact-title Ilyra resolution or send.

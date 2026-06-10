# v478 THOS v14 x6 Start CLI Marker Review Resolution

- generated_nz: `2026-06-05T10:32:00+12:00`
- overall_status: `PASS_FALSE_POSITIVE_TOKEN_WORD_REVIEW`
- claim boundary: CLI marker review resolution only; no lane body text; no local paths; all GMUT gates remain open.

## Review

- Arby: `3678` final-message bytes, hash `4cc56de01213009f9593b92ea898023fe855c34f73d650afd33d92d2857ce319`, two sensitive-marker hits.
- Arby marker counts: RSA `0`, OpenSSH `0`, API credential marker `0`, secret `0`, credential-phrase marker `0`, plain token word `2`.
- Arby resolution: `false_positive_plain_token_word`; completion allowed.
- Aster Vale: `3592` final-message bytes, hash `afd5f8e7522cb6a3eec4f1d08663febdd598da161dff4b475408b894b89de8a9`, no sensitive-marker review needed; completion allowed.

## Operator Reading

- The final-message files arrived after the 30-minute watcher timeout, so x6 start should record an over-window completion rather than an absent completion.
- Arby's two sensitive-marker hits are plain token-word false positives, not credential or private-material evidence.
- No final lane body text is published; only byte counts, hashes, and review status are recorded.

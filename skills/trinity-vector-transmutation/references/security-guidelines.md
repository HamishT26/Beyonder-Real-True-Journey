# Security Guidelines (Local Trinity Vector Profile)

- Treat passphrases as secrets; do not commit plaintext passphrases.
- Rotate passphrase if any profile artifact is shared in an untrusted channel.
- Validate `hmac_sha256` before trusting encrypted payload contents.
- For production-grade security, replace XOR stream with an authenticated cipher (e.g., AES-GCM) via a vetted crypto library.

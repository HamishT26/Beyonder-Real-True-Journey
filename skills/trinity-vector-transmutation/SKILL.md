---
name: trinity-vector-transmutation
description: Build a secure Trinity vector profile by transmuting energy/information/memory/identity/governance into mind-body-soul anatomy and an integrity-checked encrypted payload.
---

# Trinity Vector Transmutation

Use this skill when the user asks for encryption + transmutation of Trinity system vectors into a reusable secure profile.

## Workflow
1. Run `scripts/trinity_vector_transmuter.py` with vector values and passphrase.
2. Output file defaults to `docs/trinity-vector-profile.json`.
3. Confirm payload includes:
   - `vectors`
   - `anatomy` (mind/body/soul)
   - `nervous_system`
   - `encrypted` block with HMAC integrity
4. Reference governance constraints from `references/security-guidelines.md`.

## Command template
```bash
python3 scripts/trinity_vector_transmuter.py \
  --energy 0.82 --information 0.88 --memory 0.9 --identity 0.89 --governance 0.94 \
  --passphrase "<strong-passphrase>"
```

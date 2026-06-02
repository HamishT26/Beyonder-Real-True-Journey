# v472 THOS v4 x1 User-Skill BOM Repair Receipt

Status: `PASS_LOADER_ERRORS_CLEARED`.

Removed leading UTF-8 BOM bytes from `6` approved user-level skills. All six now start with raw `---`, retain `name` and `description`, and keep all bytes after the BOM unchanged.

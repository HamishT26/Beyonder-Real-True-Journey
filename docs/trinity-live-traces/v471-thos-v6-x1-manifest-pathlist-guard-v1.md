# v471 THOS v6 x1 Manifest Path-List Guard

Status: `PASS_SHAPE_ONLY`.

The guard validates the v5 affected manifest against the v5 affected path list as a closed-world pair: count equality, content equality, duplicate paths, case collisions, relative path safety, checksum presence, path ID presence, and mutation status.

This proves manifest/path-list consistency only. It does not repair plugin cache, authorize live writes, restore CLI sibling health, or prove Browser availability.

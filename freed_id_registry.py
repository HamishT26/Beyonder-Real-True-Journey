"""
Compatibility shim for case-sensitive imports.

Some files import `freed_id_registry` while the canonical implementation file
in this repository is `Freed_id_registry.py`. This shim re-exports the public
types to keep both import styles working on Linux/macOS.
Compatibility wrapper for the Freed ID registry module.

The repository historically stored the implementation in `Freed_id_registry.py`
with an uppercase leading letter.  Some runtime modules import the lowercase
`freed_id_registry` path.  This wrapper keeps both import styles working.
"""

from Freed_id_registry import DIDDocument, FreedIDRegistry

__all__ = ["DIDDocument", "FreedIDRegistry"]

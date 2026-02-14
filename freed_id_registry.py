"""
Compatibility wrapper for the Freed ID registry module.

The repository historically stored the implementation in `Freed_id_registry.py`
with an uppercase leading letter.  Some runtime modules import the lowercase
`freed_id_registry` path.  This wrapper keeps both import styles working.
"""

from Freed_id_registry import DIDDocument, FreedIDRegistry

__all__ = ["DIDDocument", "FreedIDRegistry"]

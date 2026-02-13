"""
Compatibility shim for case-sensitive imports.

Some files import `freed_id_registry` while the canonical implementation file
in this repository is `Freed_id_registry.py`. This shim re-exports the public
types to keep both import styles working on Linux/macOS.
"""

from Freed_id_registry import DIDDocument, FreedIDRegistry

__all__ = ["DIDDocument", "FreedIDRegistry"]

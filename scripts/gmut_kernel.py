"""Deprecated compatibility import; use scripts.ghc_family_gmut_kernel."""

try:
    from scripts.ghc_family_gmut_kernel import *  # noqa: F401,F403
except ModuleNotFoundError:
    from ghc_family_gmut_kernel import *  # type: ignore  # noqa: F401,F403

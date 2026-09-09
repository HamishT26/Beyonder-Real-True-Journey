#!/usr/bin/env python3
from ghc_family_preservation_x1 import cli_main

ALLOWED = {'fixed_chunk_ranges', 'chunk_reassemble'}

if __name__ == "__main__":
    raise SystemExit(cli_main(ALLOWED))

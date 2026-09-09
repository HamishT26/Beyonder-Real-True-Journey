#!/usr/bin/env python3
from ghc_family_preservation_x2 import cli_main

ALLOWED = {'sha256_digest', 'digest_match'}

if __name__ == "__main__":
    raise SystemExit(cli_main(ALLOWED))

#!/usr/bin/env python3
from ghc_family_preservation_x1 import cli_main

ALLOWED = {'base32_encode', 'base32_decode'}

if __name__ == "__main__":
    raise SystemExit(cli_main(ALLOWED))

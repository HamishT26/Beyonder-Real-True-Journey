#!/usr/bin/env python3
from ghc_family_preservation_x2 import cli_main

ALLOWED = {'xor_recover', 'claim_reservation'}

if __name__ == "__main__":
    raise SystemExit(cli_main(ALLOWED))

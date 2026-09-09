#!/usr/bin/env python3
from ghc_family_preservation_x1 import cli_main

ALLOWED = {'unsigned_varint_encode', 'unsigned_varint_decode'}

if __name__ == "__main__":
    raise SystemExit(cli_main(ALLOWED))

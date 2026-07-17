#!/usr/bin/env python3
import argparse
from ghc_family_v647_v7_runtime import emit_surface

parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()
emit_surface("oauth_resource", args.output)

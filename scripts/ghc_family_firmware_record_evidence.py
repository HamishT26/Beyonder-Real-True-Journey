"""Bounded ghc family firmware record evidence.py interface."""
from ghc_family_firmware_records_core import cli
ALLOWED=('word_decode', 'record_fixity', 'record_provenance', 'authority_reservation')
if __name__=="__main__":raise SystemExit(cli(ALLOWED))

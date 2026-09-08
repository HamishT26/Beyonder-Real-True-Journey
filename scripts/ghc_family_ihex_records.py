"""Bounded ghc family ihex records.py interface."""
from ghc_family_firmware_records_core import cli
ALLOWED=('ihex_record', 'ihex_checksum', 'ihex_extended', 'ihex_start', 'ihex_image', 'ihex_eof')
if __name__=="__main__":raise SystemExit(cli(ALLOWED))

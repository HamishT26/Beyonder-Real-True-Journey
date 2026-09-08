"""Bounded ghc family srec records.py interface."""
from ghc_family_firmware_records_core import cli
ALLOWED=('srec_record', 'srec_checksum', 'srec_count', 'srec_termination', 'srec_image')
if __name__=="__main__":raise SystemExit(cli(ALLOWED))

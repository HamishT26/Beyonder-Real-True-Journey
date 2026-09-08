"""Bounded ghc family firmware record suite.py interface."""
from ghc_family_firmware_records_core import cli
ALLOWED=('ihex_record', 'ihex_checksum', 'ihex_extended', 'ihex_start', 'ihex_image', 'ihex_eof', 'srec_record', 'srec_checksum', 'srec_count', 'srec_termination', 'srec_image', 'segment_runs', 'image_overlay', 'image_relocate', 'image_crop', 'image_holes', 'word_decode', 'record_fixity', 'record_provenance', 'authority_reservation')
if __name__=="__main__":raise SystemExit(cli(ALLOWED))

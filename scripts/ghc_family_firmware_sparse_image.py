"""Bounded ghc family firmware sparse image.py interface."""
from ghc_family_firmware_records_core import cli
ALLOWED=('segment_runs', 'image_overlay', 'image_relocate', 'image_crop', 'image_holes')
if __name__=="__main__":raise SystemExit(cli(ALLOWED))

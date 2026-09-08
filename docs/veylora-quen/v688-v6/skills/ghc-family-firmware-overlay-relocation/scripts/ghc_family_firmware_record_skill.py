"""Selected synthetic firmware contract interface."""
from ghc_family_firmware_records_core import cli
ALLOWED=('image_overlay', 'image_relocate')
if __name__=="__main__":raise SystemExit(cli(ALLOWED))

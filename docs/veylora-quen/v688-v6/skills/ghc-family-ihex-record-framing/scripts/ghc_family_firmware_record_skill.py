"""Selected synthetic firmware contract interface."""
from ghc_family_firmware_records_core import cli
ALLOWED=('ihex_record', 'ihex_checksum')
if __name__=="__main__":raise SystemExit(cli(ALLOWED))

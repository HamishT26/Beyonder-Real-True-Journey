"""Selected synthetic firmware contract interface."""
from ghc_family_firmware_records_core import cli
ALLOWED=('record_provenance', 'authority_reservation')
if __name__=="__main__":raise SystemExit(cli(ALLOWED))

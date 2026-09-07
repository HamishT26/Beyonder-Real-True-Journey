"""Planning-only v688-v6 fixture and proposal authoring. No evaluator or x2 imports."""
from pathlib import Path
import argparse, copy, hashlib, json, re, subprocess
OWNER="Veylora Quen"; PHASE="v688-v6"
SOURCE="d72ba9a9ebefc1e18cb89d2c8b90c661ba8aaf14"
PREFIX="VQ6886"
BASE="docs/veylora-quen/v688-v6"
BOUNDARY=("Relational working language only. No consciousness, sentience, personhood, legal identity, "
"identity continuity, employment, qualification, independent agency, scientific, operational, "
"professional, legal, cultural, affected-party, or Maori authority is established. "
"Same-owner synthetic evidence is not independent reproduction. NOT_READY_FOR_STAGE_20. "
"Maori concepts remain under Maori authority.")
GATES=["empirical","participant","professional","production","deployment","legal","cultural",
"affected_party","maori_authority","privacy_complete","accessibility_complete","exhaustive_security",
"independent_reproduction","agi_asi","consciousness_personhood","theory_of_everything","proof_canon","stage20"]
PRACTICES=["synthetic firmware record registrar","address-space arithmetic analyst",
"preservation byte-integrity reviewer","provenance and accessible-handover steward"]
SKILLS=['ihex-record-framing', 'ihex-address-metadata', 'ihex-stream-termination', 'srec-record-framing', 'srec-count-termination', 'firmware-image-segments', 'firmware-overlay-relocation', 'firmware-window-missingness', 'firmware-word-fixity', 'firmware-provenance-reservations']
RUNNERS=["ghc_family_ihex_records.py","ghc_family_srec_records.py","ghc_family_firmware_sparse_image.py",
"ghc_family_firmware_record_evidence.py","ghc_family_firmware_record_suite.py"]
SREC_WIDTH={0:2,1:2,2:3,3:4,5:2,6:3,7:4,8:3,9:2}
def serial(x): return json.dumps(x,ensure_ascii=True,sort_keys=True,separators=(",",":")).encode()
def digest(x): return hashlib.sha256(x).hexdigest()
def ih(kind,offset=0,data=()):
    v=[len(data),offset>>8,offset&255,kind,*data]
    return ":"+bytes(v+[(-sum(v))&255]).hex().upper()
def sr(kind,address=0,data=()):
    a=list(address.to_bytes(SREC_WIDTH[kind],"big"))
    v=[len(a)+len(data)+1,*a,*data]
    return "S"+str(kind)+bytes(v+[(~sum(v))&255]).hex().upper()
def case(title,payload,value=None,error=None,expected="completed"):
    return dict(title=title,payload=payload,value=value,error=error,expected=expected)
def fixture_groups():
    groups=[]
    def add(op,pillar,practice,rows):
        assert len(rows)==10,(op,len(rows))
        groups.append((op,pillar,practice,rows))
    def record_value(kind,offset,data):
        return dict(length=len(data),offset=offset,record_type=kind,data_hex=bytes(data).hex())
    add("ihex_record",1,0,[
      case("Intel HEX empty data record retains its zero byte count",{"record":ih(0)},record_value(0,0,[])),
      case("Intel HEX single payload byte is distinct from its checksum",{"record":ih(0,16,[0xA5])},record_value(0,16,[0xA5])),
      case("Intel HEX maximum 255-byte payload retains all byte positions",{"record":ih(0,0,list(range(255)))},record_value(0,0,list(range(255)))),
      case("Intel HEX highest sixteen-bit load offset stays unsigned",{"record":ih(0,65535,[1])},record_value(0,65535,[1])),
      case("Intel HEX lowercase hex digits preserve the decoded record",{"record":ih(0,32,[0xAB,0xCD]).lower()},record_value(0,32,[0xAB,0xCD])),
      case("Intel HEX end marker remains a typed zero-length record",{"record":ih(1)},record_value(1,0,[])),
      case("Intel HEX linear-base record preserves its two declared bytes",{"record":ih(4,0,[0x12,0x34])},record_value(4,0,[0x12,0x34])),
      case("Intel HEX framing refuses a missing colon",{"record":"00000001FF"},error="ihex_lexical"),
      case("Intel HEX framing refuses inconsistent declared length",{"record":":01000001FF"},error="ihex_length"),
      case("Intel HEX framing refuses a changed checksum byte",{"record":":0000000100"},error="ihex_checksum")])
    add("ihex_checksum",0,2,[
      case("Intel HEX two-complement checksum of an empty vector is zero",{"bytes":[]},0),
      case("Intel HEX checksum includes the count byte",{"bytes":[1,0,0,0,1]},254),
      case("Intel HEX checksum cancels an FF byte modulo 256",{"bytes":[255]},1),
      case("Intel HEX checksum wraps a carry of exactly 256",{"bytes":[128,128]},0),
      case("Intel HEX checksum includes both offset octets",{"bytes":[2,18,52,0,1,2]},181),
      case("Intel HEX checksum distinguishes the record type octet",{"bytes":[0,0,0,1]},255),
      case("Intel HEX checksum bounds a maximum framed payload",{"bytes":[255]*259},3),
      case("Intel HEX checksum refuses negative octets",{"bytes":[-1]},error="octet"),
      case("Intel HEX checksum refuses Boolean octets",{"bytes":[True]},error="octet"),
      case("Intel HEX checksum refuses octets above 255",{"bytes":[256]},error="octet")])
    add("ihex_extended",0,1,[
      case("Intel HEX segment base shifts the declared value by four bits",{"record":ih(2,0,[0x12,0x34])},{"mode":"segment","base":0x12340}),
      case("Intel HEX linear base shifts the declared value by sixteen bits",{"record":ih(4,0,[0x12,0x34])},{"mode":"linear","base":0x12340000}),
      case("Intel HEX zero segment base is explicit metadata",{"record":ih(2)},error="ihex_extension_shape"),
      case("Intel HEX correctly sized zero segment base is accepted",{"record":ih(2,0,[0,0])},{"mode":"segment","base":0}),
      case("Intel HEX largest segment base stays below the 20-bit boundary",{"record":ih(2,0,[255,255])},{"mode":"segment","base":0xFFFF0}),
      case("Intel HEX largest linear base preserves its high word",{"record":ih(4,0,[255,255])},{"mode":"linear","base":0xFFFF0000}),
      case("Intel HEX linear extension can reset the base to zero",{"record":ih(4,0,[0,0])},{"mode":"linear","base":0}),
      case("Intel HEX base interpretation refuses a data-record substitute",{"record":ih(0,0,[0,1])},error="ihex_extension_kind"),
      case("Intel HEX extension refuses nonzero reserved offset",{"record":ih(4,1,[0,1])},error="ihex_extension_shape"),
      case("Intel HEX extension refuses a three-octet base value",{"record":ih(2,0,[0,1,2])},error="ihex_extension_shape")])
    add("ihex_start",1,0,[
      case("Intel HEX start segment preserves CS and IP separately",{"record":ih(3,0,[0x12,0x34,0x56,0x78])},{"kind":"segment","cs":0x1234,"ip":0x5678,"executed":False}),
      case("Intel HEX start linear preserves an unsigned entry value",{"record":ih(5,0,[0x12,0x34,0x56,0x78])},{"kind":"linear","entry":0x12345678,"executed":False}),
      case("Intel HEX zero linear entry does not request execution",{"record":ih(5,0,[0,0,0,0])},{"kind":"linear","entry":0,"executed":False}),
      case("Intel HEX maximal linear entry is metadata only",{"record":ih(5,0,[255]*4)},{"kind":"linear","entry":0xFFFFFFFF,"executed":False}),
      case("Intel HEX zero CS remains separate from a nonzero IP",{"record":ih(3,0,[0,0,0,1])},{"kind":"segment","cs":0,"ip":1,"executed":False}),
      case("Intel HEX nonzero CS remains separate from zero IP",{"record":ih(3,0,[0,1,0,0])},{"kind":"segment","cs":1,"ip":0,"executed":False}),
      case("Intel HEX maximal segment registers are not collapsed to a pointer",{"record":ih(3,0,[255]*4)},{"kind":"segment","cs":65535,"ip":65535,"executed":False}),
      case("Intel HEX start interpretation refuses extension records",{"record":ih(4,0,[0,1])},error="ihex_start_kind"),
      case("Intel HEX start record refuses nonzero reserved offset",{"record":ih(5,1,[0]*4)},error="ihex_start_shape"),
      case("Intel HEX start record refuses missing register bytes",{"record":ih(3,0,[0]*3)},error="ihex_start_shape")])
    def image_value(pairs,entry=None): return {"image":pairs,"entry":entry}
    add("ihex_image",1,0,[
      case("Intel HEX empty terminated stream has no loaded bytes",{"records":[ih(1)]},image_value([])),
      case("Intel HEX adjacent data records form one ordered address map",{"records":[ih(0,1,[10]),ih(0,2,[20]),ih(1)]},image_value([[1,10],[2,20]])),
      case("Intel HEX separated records preserve an unfilled address hole",{"records":[ih(0,1,[10]),ih(0,4,[20]),ih(1)]},image_value([[1,10],[4,20]])),
      case("Intel HEX linear base changes subsequent absolute addresses",{"records":[ih(4,0,[0,1]),ih(0,2,[7]),ih(1)]},image_value([[65538,7]])),
      case("Intel HEX segment base changes subsequent absolute addresses",{"records":[ih(2,0,[0,1]),ih(0,2,[7]),ih(1)]},image_value([[18,7]])),
      case("Intel HEX base replacement leaves earlier data fixed",{"records":[ih(4,0,[0,1]),ih(0,2,[7]),ih(4,0,[0,0]),ih(0,2,[8]),ih(1)]},image_value([[2,8],[65538,7]])),
      case("Intel HEX start metadata is preserved without executing the image",{"records":[ih(5,0,[0,0,0,8]),ih(0,8,[1]),ih(1)]},image_value([[8,1]],{"kind":"linear","entry":8,"executed":False})),
      case("Intel HEX image refuses duplicate address occupancy",{"records":[ih(0,1,[1]),ih(0,1,[1]),ih(1)]},error="image_overlap"),
      case("Intel HEX strict profile refuses an address-wrap record",{"records":[ih(2,0,[0,1]),ih(0,65535,[1,2]),ih(1)]},error="address_wrap"),
      case("Intel HEX image refuses a second entry declaration",{"records":[ih(5,0,[0]*4),ih(5,0,[0,0,0,1]),ih(1)]},error="duplicate_entry")])
    add("ihex_eof",1,0,[
      case("Intel HEX EOF-only input closes at record zero",{"records":[ih(1)]},{"eof_index":0,"record_count":1}),
      case("Intel HEX EOF follows one data record",{"records":[ih(0,0,[1]),ih(1)]},{"eof_index":1,"record_count":2}),
      case("Intel HEX EOF follows one extension record",{"records":[ih(4,0,[0,1]),ih(1)]},{"eof_index":1,"record_count":2}),
      case("Intel HEX EOF follows an entry declaration",{"records":[ih(3,0,[0]*4),ih(1)]},{"eof_index":1,"record_count":2}),
      case("Intel HEX EOF index counts zero-length data records",{"records":[ih(0),ih(0,1),ih(1)]},{"eof_index":2,"record_count":3}),
      case("Intel HEX EOF framing permits lowercase checksum spelling",{"records":[ih(1).lower()]},{"eof_index":0,"record_count":1}),
      case("Intel HEX EOF framing refuses an empty record collection",{"records":[]},error="ihex_eof_missing"),
      case("Intel HEX EOF framing refuses a missing terminator",{"records":[ih(0)]},error="ihex_eof_missing"),
      case("Intel HEX EOF framing refuses a duplicate terminator",{"records":[ih(1),ih(1)]},error="ihex_after_eof"),
      case("Intel HEX EOF framing refuses data after termination",{"records":[ih(1),ih(0,0,[1])]},error="ihex_after_eof")])
    def sv(t,a,d): return {"record_type":"S"+str(t),"address":a,"data_hex":bytes(d).hex(),"count":SREC_WIDTH[t]+len(d)+1}
    add("srec_record",1,0,[
      case("S-record S0 header retains its descriptive octets",{"record":sr(0,0,[72,68,82])},sv(0,0,[72,68,82])),
      case("S-record S1 data retains a sixteen-bit address",{"record":sr(1,0x1234,[1,2])},sv(1,0x1234,[1,2])),
      case("S-record S2 data retains a twenty-four-bit address",{"record":sr(2,0x123456,[3])},sv(2,0x123456,[3])),
      case("S-record S3 data retains a thirty-two-bit address",{"record":sr(3,0x12345678,[4])},sv(3,0x12345678,[4])),
      case("S-record S5 count occupies the two-byte address field",{"record":sr(5,3)},sv(5,3,[])),
      case("S-record S6 count occupies the three-byte address field",{"record":sr(6,65536)},sv(6,65536,[])),
      case("S-record S7 terminator retains a four-byte entry declaration",{"record":sr(7,16)},sv(7,16,[])),
      case("S-record parser refuses the undefined S4 record kind",{"record":"S4030000FC"},error="srec_type"),
      case("S-record parser refuses a mismatched byte count",{"record":"S105000001FE"},error="srec_length"),
      case("S-record parser refuses a corrupted ones-complement checksum",{"record":"S903000000"},error="srec_checksum")])
    add("srec_checksum",0,2,[
      case("S-record empty checksum vector produces ones-complement FF",{"bytes":[]},255),
      case("S-record checksum includes a three-byte count value",{"bytes":[3,0,0]},252),
      case("S-record checksum cancels an FF byte to zero",{"bytes":[255]},0),
      case("S-record checksum wraps a complete carry to FF",{"bytes":[128,128]},255),
      case("S-record checksum includes high and low address bytes",{"bytes":[5,18,52,1,2]},177),
      case("S-record checksum preserves the distinction from two-complement",{"bytes":[1]},254),
      case("S-record checksum bounds a maximum 255-octet vector",{"bytes":[255]*255},254),
      case("S-record checksum refuses a fractional octet",{"bytes":[1.5]},error="octet"),
      case("S-record checksum refuses Boolean octets",{"bytes":[False]},error="octet"),
      case("S-record checksum refuses octets above its field width",{"bytes":[256]},error="octet")])
    add("srec_count",0,2,[
      case("S-record count describes one S1 data record",{"records":[sr(1,0,[1]),sr(5,1)]},{"data_records":1,"declared_count":1}),
      case("S-record count describes two data records despite byte length",{"records":[sr(1,0,[1,2]),sr(1,2,[3]),sr(5,2)]},{"data_records":2,"declared_count":2}),
      case("S-record S6 can declare a small record count",{"records":[sr(3,0,[1]),sr(6,1)]},{"data_records":1,"declared_count":1}),
      case("S-record zero count accompanies an empty data set",{"records":[sr(5,0)]},{"data_records":0,"declared_count":0}),
      case("S-record absent optional count remains explicit",{"records":[sr(2,0,[1])]},{"data_records":1,"declared_count":None}),
      case("S-record header is excluded from the data-record count",{"records":[sr(0,0,[1]),sr(1,0,[2]),sr(5,1)]},{"data_records":1,"declared_count":1}),
      case("S-record terminator is excluded from the data-record count",{"records":[sr(1,0,[1]),sr(5,1),sr(9,0)]},{"data_records":1,"declared_count":1}),
      case("S-record count refuses a declared total below the observed count",{"records":[sr(1,0,[1]),sr(5,0)]},error="srec_count_mismatch"),
      case("S-record strict profile refuses duplicate count records",{"records":[sr(5,0),sr(5,0)]},error="srec_multiple_counts"),
      case("S-record count refuses payload bytes in count metadata",{"records":[sr(5,0,[1])]},error="srec_metadata_shape")])
    add("srec_termination",1,0,[
      case("S-record S9 termination matches sixteen-bit data",{"records":[sr(1,0,[1]),sr(9,0)]},{"termination":"S9","entry":0,"executed":False}),
      case("S-record S8 termination matches twenty-four-bit data",{"records":[sr(2,0,[1]),sr(8,0x123456)]},{"termination":"S8","entry":0x123456,"executed":False}),
      case("S-record S7 termination matches thirty-two-bit data",{"records":[sr(3,0,[1]),sr(7,0x12345678)]},{"termination":"S7","entry":0x12345678,"executed":False}),
      case("S-record empty block uses an explicit S9 termination",{"records":[sr(9,0)]},{"termination":"S9","entry":0,"executed":False}),
      case("S-record header can precede a terminated empty block",{"records":[sr(0,0,[72]),sr(9,0)]},{"termination":"S9","entry":0,"executed":False}),
      case("S-record count may precede the final termination",{"records":[sr(1,0,[1]),sr(5,1),sr(9,4)]},{"termination":"S9","entry":4,"executed":False}),
      case("S-record terminator retains its maximal sixteen-bit entry",{"records":[sr(1,0,[1]),sr(9,65535)]},{"termination":"S9","entry":65535,"executed":False}),
      case("S-record termination refuses an absent terminator",{"records":[sr(1,0,[1])]},error="srec_termination_missing"),
      case("S-record termination refuses a width mismatch",{"records":[sr(2,0,[1]),sr(9,0)]},error="srec_termination_width"),
      case("S-record termination refuses trailing data",{"records":[sr(9,0),sr(1,0,[1])]},error="srec_after_termination")])
    add("srec_image",1,0,[
      case("S-record empty terminated image contains no payload bytes",{"records":[sr(9,0)]},image_value([],0)),
      case("S-record data records map adjacent bytes in address order",{"records":[sr(1,1,[10]),sr(1,2,[20]),sr(9,1)]},image_value([[1,10],[2,20]],1)),
      case("S-record out-of-order data retains absolute addresses",{"records":[sr(1,4,[10]),sr(1,1,[20]),sr(9,1)]},image_value([[1,20],[4,10]],1)),
      case("S-record image retains a twenty-four-bit sparse address",{"records":[sr(2,65536,[7]),sr(8,65536)]},image_value([[65536,7]],65536)),
      case("S-record image retains a thirty-two-bit sparse address",{"records":[sr(3,16777216,[7]),sr(7,16777216)]},image_value([[16777216,7]],16777216)),
      case("S-record image excludes header description from payload",{"records":[sr(0,0,[72]),sr(1,0,[8]),sr(9,0)]},image_value([[0,8]],0)),
      case("S-record image validates optional record counts",{"records":[sr(1,0,[1,2]),sr(5,1),sr(9,0)]},image_value([[0,1],[1,2]],0)),
      case("S-record image refuses overlapping data addresses",{"records":[sr(1,0,[1]),sr(1,0,[2]),sr(9,0)]},error="image_overlap"),
      case("S-record strict profile refuses mixed data address widths",{"records":[sr(1,0,[1]),sr(2,1,[2]),sr(8,0)]},error="srec_mixed_width"),
      case("S-record image refuses payload overflow past its address width",{"records":[sr(1,65535,[1,2]),sr(9,0)]},error="address_wrap")])
    add("segment_runs",0,1,[
      case("Sparse firmware run index preserves an empty image",{"image":[]},[]),
      case("Sparse firmware run index creates one singleton interval",{"image":[[4,9]]},[{"start":4,"end":5,"data_hex":"09"}]),
      case("Sparse firmware run index joins adjacent byte addresses",{"image":[[4,9],[5,8]]},[{"start":4,"end":6,"data_hex":"0908"}]),
      case("Sparse firmware run index splits across a missing address",{"image":[[4,9],[6,8]]},[{"start":4,"end":5,"data_hex":"09"},{"start":6,"end":7,"data_hex":"08"}]),
      case("Sparse firmware run index sorts a declared unordered image",{"image":[[2,8],[1,9]]},[{"start":1,"end":3,"data_hex":"0908"}]),
      case("Sparse firmware run index permits an exclusive end at 2 power 32",{"image":[[0xFFFFFFFF,1]]},[{"start":0xFFFFFFFF,"end":0x100000000,"data_hex":"01"}]),
      case("Sparse firmware run index retains zero-valued stored bytes",{"image":[[0,0],[1,0]]},[{"start":0,"end":2,"data_hex":"0000"}]),
      case("Sparse firmware run index refuses duplicate addresses",{"image":[[0,1],[0,1]]},error="image_overlap"),
      case("Sparse firmware run index refuses Boolean addresses",{"image":[[True,1]]},error="address"),
      case("Sparse firmware run index refuses malformed address-byte pairs",{"image":[[0,1,2]]},error="image_pair")])
    add("image_overlay",1,1,[
      case("Firmware overlay preview joins disjoint images",{"base":[[0,1]],"overlay":[[2,3]],"policy":"reject_any"},[[0,1],[2,3]]),
      case("Firmware overlay preview keeps a base when overlay is empty",{"base":[[1,2]],"overlay":[],"policy":"reject_any"},[[1,2]]),
      case("Firmware overlay preview accepts an empty base",{"base":[],"overlay":[[1,2]],"policy":"identical_only"},[[1,2]]),
      case("Firmware overlay preview permits an identical byte by explicit policy",{"base":[[1,2]],"overlay":[[1,2]],"policy":"identical_only"},[[1,2]]),
      case("Firmware overlay preview permits identical and new bytes together",{"base":[[1,2]],"overlay":[[1,2],[2,3]],"policy":"identical_only"},[[1,2],[2,3]]),
      case("Firmware overlay preview sorts disjoint address ranges",{"base":[[10,2]],"overlay":[[1,3]],"policy":"reject_any"},[[1,3],[10,2]]),
      case("Firmware overlay preview retains explicit FF data",{"base":[[0,255]],"overlay":[[1,0]],"policy":"reject_any"},[[0,255],[1,0]]),
      case("Firmware overlay preview refuses equal overlap under reject-any policy",{"base":[[0,1]],"overlay":[[0,1]],"policy":"reject_any"},error="overlay_conflict"),
      case("Firmware overlay preview refuses differing overlap under identical-only policy",{"base":[[0,1]],"overlay":[[0,2]],"policy":"identical_only"},error="overlay_conflict"),
      case("Firmware overlay preview refuses an implicit overwrite policy",{"base":[],"overlay":[],"policy":"overwrite"},error="overlay_policy")])
    add("image_relocate",0,1,[
      case("Firmware relocation preview shifts a byte upward",{"image":[[0,1]],"delta":16},[[16,1]]),
      case("Firmware relocation preview shifts a byte downward",{"image":[[16,1]],"delta":-16},[[0,1]]),
      case("Firmware relocation preview preserves zero shift",{"image":[[4,1],[7,2]],"delta":0},[[4,1],[7,2]]),
      case("Firmware relocation preview preserves relative gaps",{"image":[[4,1],[7,2]],"delta":2},[[6,1],[9,2]]),
      case("Firmware relocation preview permits an empty image",{"image":[],"delta":1},[]),
      case("Firmware relocation preview reaches the maximal address exactly",{"image":[[0,9]],"delta":0xFFFFFFFF},[[0xFFFFFFFF,9]]),
      case("Firmware relocation preview reorders no payload values",{"image":[[8,0],[9,255]],"delta":-4},[[4,0],[5,255]]),
      case("Firmware relocation preview refuses address underflow",{"image":[[0,1]],"delta":-1},error="relocation_range"),
      case("Firmware relocation preview refuses address overflow",{"image":[[0xFFFFFFFF,1]],"delta":1},error="relocation_range"),
      case("Firmware relocation preview refuses Boolean displacement",{"image":[],"delta":True},error="delta")])
    add("image_crop",0,1,[
      case("Firmware crop includes the declared lower boundary",{"image":[[1,2],[2,3]],"start":1,"end":2},[[1,2]]),
      case("Firmware crop excludes the declared upper boundary",{"image":[[1,2],[2,3]],"start":0,"end":2},[[1,2]]),
      case("Firmware crop preserves an empty interval",{"image":[[1,2]],"start":1,"end":1},[]),
      case("Firmware crop preserves an empty image",{"image":[],"start":0,"end":1},[]),
      case("Firmware crop keeps a hole without adding fill bytes",{"image":[[0,1],[2,3]],"start":0,"end":3},[[0,1],[2,3]]),
      case("Firmware crop permits the complete 32-bit envelope",{"image":[[0xFFFFFFFF,1]],"start":0,"end":0x100000000},[[0xFFFFFFFF,1]]),
      case("Firmware crop can exclude all stored addresses",{"image":[[1,2]],"start":4,"end":8},[]),
      case("Firmware crop refuses a reversed interval",{"image":[],"start":2,"end":1},error="interval"),
      case("Firmware crop refuses a negative endpoint",{"image":[],"start":-1,"end":1},error="interval"),
      case("Firmware crop refuses Boolean interval endpoints",{"image":[],"start":False,"end":1},error="interval")])
    add("image_holes",0,1,[
      case("Firmware hole ledger reports a fully empty window",{"image":[],"start":0,"end":4},[[0,4]]),
      case("Firmware hole ledger reports no gaps in a full window",{"image":[[0,1],[1,2]],"start":0,"end":2},[]),
      case("Firmware hole ledger retains a leading gap",{"image":[[2,1]],"start":0,"end":3},[[0,2]]),
      case("Firmware hole ledger retains a trailing gap",{"image":[[0,1]],"start":0,"end":3},[[1,3]]),
      case("Firmware hole ledger retains an internal gap",{"image":[[0,1],[2,2]],"start":0,"end":3},[[1,2]]),
      case("Firmware hole ledger ignores bytes outside the requested window",{"image":[[0,1],[4,2]],"start":1,"end":4},[[1,4]]),
      case("Firmware hole ledger permits an empty requested window",{"image":[[0,1]],"start":0,"end":0},[]),
      case("Firmware hole ledger refuses an overlarge endpoint",{"image":[],"start":0,"end":0x100000001},error="interval"),
      case("Firmware hole ledger refuses a reversed window",{"image":[],"start":2,"end":1},error="interval"),
      case("Firmware hole ledger refuses duplicate stored addresses",{"image":[[1,1],[1,2]],"start":0,"end":3},error="image_overlap")])
    add("word_decode",0,2,[
      case("Firmware word decoder interprets a big-endian unsigned pair",{"data_hex":"1234","width":16,"byteorder":"big","signed":False},4660),
      case("Firmware word decoder interprets a little-endian unsigned pair",{"data_hex":"1234","width":16,"byteorder":"little","signed":False},13330),
      case("Firmware word decoder preserves a signed negative one",{"data_hex":"ffff","width":16,"byteorder":"big","signed":True},-1),
      case("Firmware word decoder preserves the signed minimum byte",{"data_hex":"80","width":8,"byteorder":"big","signed":True},-128),
      case("Firmware word decoder supports an explicit twenty-four-bit width",{"data_hex":"010203","width":24,"byteorder":"big","signed":False},66051),
      case("Firmware word decoder supports an explicit sixty-four-bit zero",{"data_hex":"0000000000000000","width":64,"byteorder":"little","signed":False},0),
      case("Firmware word decoder separates signedness from bytes",{"data_hex":"ff","width":8,"byteorder":"big","signed":False},255),
      case("Firmware word decoder refuses an unsupported bit width",{"data_hex":"00","width":7,"byteorder":"big","signed":False},error="word_width"),
      case("Firmware word decoder refuses a byte-length mismatch",{"data_hex":"00","width":16,"byteorder":"big","signed":False},error="word_length"),
      case("Firmware word decoder refuses an implicit byte-order label",{"data_hex":"00","width":8,"byteorder":"native","signed":False},error="byteorder")])
    fix_texts=[("", "empty record text"),(":00000001FF","one terminator without newline"),
      (":00000001FF\n","one LF-terminated line"),(":00000001FF\r\n","one CRLF-terminated line"),
      (":00000001ff\n","lowercase checksum spelling"),("S9030000FC\n","one S9 termination line"),
      (":0100000001FE\n:00000001FF\n","two declared Intel HEX records")]
    rows=[]
    for t,title in fix_texts:
        rows.append(case("Firmware textual fixity distinguishes "+title,{"text":t},
          {"raw_sha256":digest(t.encode("ascii")),"lf_sha256":digest(t.replace("\r\n","\n").encode("ascii")),
           "raw_bytes":len(t.encode("ascii")),"normalization":"CRLF_to_LF_only","authenticity_established":False},expected="represented"))
    rows += [case("Firmware textual fixity refuses non-ASCII input",{"text":"\u0100"},error="ascii_text"),
             case("Firmware textual fixity refuses a NUL control",{"text":"A\u0000B"},error="text_control"),
             case("Firmware textual fixity refuses nontext input",{"text":False},error="text_type")]
    add("record_fixity",2,2,rows)
    pv={"source_label":"synthetic-fixture","source_digest":"a"*64,"rights_state":"unknown","review_state":"absent","observed":False}
    def provenance(**kw):
        p=dict(pv);p.update(kw);return p
    def pvalue(p):
        return {"source_label":p["source_label"],"rights_state":p["rights_state"],"review_state":p["review_state"],
        "observation":"synthetic","publication_authorized":False}
    rows=[]
    for title,p in [
      ("Firmware provenance keeps unknown rights explicit",provenance()),
      ("Firmware provenance retains a declared rights label without validating it",provenance(rights_state="declared")),
      ("Firmware provenance retains a declared review without independence credit",provenance(review_state="declared")),
      ("Firmware provenance separates declared review and rights from permission",provenance(rights_state="declared",review_state="declared"))]:
        rows.append(case(title,p,pvalue(p),expected="represented"))
    for title,p in [
      ("Firmware provenance exposes an absent source label",provenance(source_label="")),
      ("Firmware provenance exposes an absent source digest",provenance(source_digest="")),
      ("Firmware provenance exposes both missing source bindings",provenance(source_label="",source_digest=""))]:
        rows.append(case(title,p,{"missing":[k for k in ["source_label","source_digest"] if not p[k]],"publication_authorized":False},expected="open_gap"))
    rows += [case("Firmware provenance refuses a malformed source digest",provenance(source_digest="bad"),error="digest"),
      case("Firmware provenance refuses a real observation preclaim",provenance(observed=True),error="synthetic_only"),
      case("Firmware provenance refuses an unsupported rights label",provenance(rights_state="certified"),error="rights_state")]
    add("record_provenance",2,3,rows)
    action_requirements={
      "hardware_write":"exact device owner, target, qualified operator, rollback and safety evidence",
      "firmware_deployment":"exact deployment target, authorization, test and recovery evidence",
      "professional_certification":"competent professional authority and independent evaluation",
      "legal_ownership":"competent legal and rights-holder evidence",
      "cultural_interpretation":"competent and affected cultural authority",
      "maori_wording":"tangata whenua, iwi, hapu and Maori authority",
      "affected_party_approval":"the affected parties and their actual approval",
      "privacy_complete":"appropriate privacy review, threat model and affected-party evidence",
      "independent_reproduction":"an independent executor and independently obtained evidence",
      "stage20":"all exact evidence and authority required by the protected Stage 20 gate"}
    add("authority_reservation",2,3,[
      case("Firmware authority reservation retains the "+action.replace("_"," ")+" gate",
      {"action":action},{"action":action,"executed":False,"required":requirement},expected="exact_gate")
      for action,requirement in action_requirements.items()])
    assert len(groups)==20
    return groups

def git(root,*args): return subprocess.check_output(["git","-C",str(root),*args])
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    data=value if isinstance(value,str) else json.dumps(value,ensure_ascii=True,indent=2,sort_keys=True)+"\n"
    if path.exists(): raise RuntimeError("refuse_existing_plan_artifact:"+path.name)
    path.write_bytes(data.encode("utf-8"))
def source_inventory(root):
    paths=[p for p in git(root,"ls-tree","-r","--name-only",SOURCE,"--","docs").decode().splitlines()
           if "proposal" in p.lower() and p.endswith(".json")]
    q=("\n".join(SOURCE+":"+p for p in paths)+"\n").encode()
    data=subprocess.run(["git","-C",str(root),"cat-file","--batch"],input=q,stdout=subprocess.PIPE,check=True).stdout
    titles=[]; hashes=set(); failures=[]; pos=0
    def walk(x,path):
        if isinstance(x,dict):
            name=x.get("title",x.get("hypothesis"))
            if isinstance(name,str) and name.strip():
                titles.append((x.get("proposal_id",x.get("id","")),name,path))
            for key in ["input","frozen_input","effective_input","complete_input"]:
                if isinstance(x.get(key),(dict,list)): hashes.add(digest(serial(x[key])))
            for v in x.values(): walk(v,path)
        elif isinstance(x,list):
            for v in x: walk(v,path)
    for path in paths:
        end=data.index(b"\n",pos); fields=data[pos:end].split(); assert len(fields)==3
        n=int(fields[2]); blob=data[end+1:end+1+n];pos=end+n+2
        try: walk(json.loads(blob),path)
        except (ValueError,UnicodeError) as exc: failures.append({"path":path,"error_class":type(exc).__name__})
    return paths,titles,hashes,failures
def main():
    import urllib.request,datetime,os
    ap=argparse.ArgumentParser();ap.add_argument("--bank",type=Path,required=True);ap.add_argument("--skill-root",type=Path,required=True)
    args=ap.parse_args();root=Path(__file__).resolve().parents[1];x1=root/BASE/"x1"
    assert git(root,"rev-parse","HEAD").decode().strip()==SOURCE
    assert not x1.exists()
    groups=fixture_groups();proposals=[]
    pillars=["GMUT Mind","THOS Body","Freed ID and CBR Heart"]
    for operation,pi,pri,cases in groups:
        for c in cases:
            ident=f"{PREFIX}-N{len(proposals)+1:03d}"
            proposals.append({"schema":"ghc.family.frozen-firmware-contract.v1","proposal_id":ident,
              "title":c["title"],"operation":operation,"input":{"operation":operation,**c["payload"]},
              "expected_acceptance":c["error"] is None,"expected_error":c["error"],"expected_value":c["value"],
              "expected_execution_disposition":c["expected"],"planning_only":True,"execution_credit":0,
              "source_kind":"synthetic","source_status":"current",
              "source_refs":["SRECORD-IHEX","SRECORD-MOTOROLA","BITSTRUCT-UPSTREAM"],
              "pillar":pillars[pi],"practice":PRACTICES[pri],
              "hypothesis":c["title"]+" within the explicitly bounded owner profile.",
              "null_or_failure_condition":"Any acceptance, error-class, complete-value, immutability or protected-boundary mismatch rejects this witness.",
              "approval_class":"safe_now" if c["expected"]=="completed" else ("exact_approval_needed" if c["expected"]=="exact_gate" else "candidate"),
              "execution_lane":"x2_synthetic_projection_only",
              "current_official_or_primary_source_needs":"Use the cited implementation specifications and exact package provenance; preserve unreadable and version-drift source limits.",
              "concrete_artifact":BASE+f"/x2/contracts/{len(proposals)+1:03d}.json",
              "falsifier_or_acceptance_gate":"The entire result envelope must equal the frozen acceptance, error, value, disposition and non-execution boundary. Input must remain unchanged.",
              "rollback_or_recovery":"Retain the failed input and expected definition, isolate the owner implementation, and add a correction without changing immutable x1.",
              "protected_gates":GATES,"external_credit":False})
    assert len(proposals)==200
    source= json.loads(git(root,"show",SOURCE+":docs/elowen-cairn/v688-v5/x1/new-proposal-freeze.json"))
    inherited=[{"selection_id":f"{PREFIX}-I{i+1:03d}","source_commit":SOURCE,
      "source_artifact":"docs/elowen-cairn/v688-v5/x1/new-proposal-freeze.json",
      "source_proposal":p,"inherited_execution_credit":0,"inherited_novelty_credit":0}
      for i,p in enumerate(source["proposals"])]
    paths,titles,old_hashes,parse_errors=source_inventory(root)
    assert not parse_errors
    def tokens(t): return set(re.findall("[a-z0-9]+",t.lower()))
    corpus=[(r,tokens(r[1])) for r in titles]
    neighbors=[]
    for p in proposals:
        pt=tokens(p["title"]); score,near=max(((len(pt&t)/len(pt|t),r) for r,t in corpus),key=lambda a:a[0])
        neighbors.append({"proposal_id":p["proposal_id"],"nearest_source_id":near[0],"nearest_source_title":near[1],
         "nearest_source_path":near[2],"jaccard":round(score,6)})
    exact_names={t[1].casefold() for t in titles}
    exact_collisions=[p["proposal_id"] for p in proposals if p["title"].casefold() in exact_names]
    input_collisions=[p["proposal_id"] for p in proposals if digest(serial(p["input"])) in old_hashes]
    local_hashes=[digest(serial(p["input"])) for p in proposals]
    assert not exact_collisions and not input_collisions and len(set(local_hashes))==200
    assert max(n["jaccard"] for n in neighbors)<0.78
    startup=json.loads((args.bank/"startup-observations.json").read_text())
    src_truth=json.loads(git(root,"show",SOURCE+":docs/elowen-cairn/v688-v5/correction1/phase-truth.json"))
    release=json.loads((args.bank/"source-route-release.json").read_text())
    prior_route=json.loads((args.bank/"source-route-gap.json").read_text())
    baseline=release["external_effective_counts"]
    stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(x1/"new-proposals.json",{"schema":"ghc.family.new-proposal-freeze.v1","owner":OWNER,"phase":PHASE,"source":SOURCE,
      "planning_only":True,"chain_before":16430,"chain_after":16630,"count":200,"proposals":proposals})
    write(x1/"inherited-proposals.json",{"schema":"ghc.family.inherited-proposal-freeze.v1","count":200,"planning_only":True,"execution_credit":0,"selections":inherited})
    write(x1/"novelty-review.json",{"schema":"ghc.family.source-bounded-novelty.v1","source":SOURCE,"source_path_count":len(paths),
      "source_title_count":len(titles),"source_input_count":len(old_hashes),"source_parse_failures":parse_errors,
      "source_object_review_only":True,"unchanged_history_validation":False,"cross_worktree_scan":False,
      "exact_title_collisions":exact_collisions,"input_hash_collisions":input_collisions,
      "threshold":0.78,"neighbors":neighbors,"universal_novelty_claimed":False,
      "interpretation":"Lexical and input comparisons are bounded novelty screens, not proof of independent invention. Source rows remain inherited evidence."})
    counts={"safe_now":300,"candidates":250,"clean_fix_refine":300,"exact_packets":50,"blocked_packets":30}
    portfolio={"schema":"ghc.family.firmware-portfolio-plan.v1","planning_only":True,"execution_credit":0,
      "destructive_cleanup_planned":False,"counts":counts}
    for key in ["safe_now","candidates","clean_fix_refine"]:
        rows=[]
        for i in range(counts[key]):
            p=proposals[i%200]
            mode={"safe_now":("contract_check" if i<200 else "repeat_stability"),
             "candidates":("unknown_field_rejection" if i<200 else "missing_field_rejection"),
             "clean_fix_refine":("altered_output_rejection" if i<200 else "json_key_order_invariance")}[key]
            rows.append({"task_id":f"{PREFIX}-{key.upper()}-{i+1:03d}","proposal_id":p["proposal_id"],"procedure":mode,
              "approval_class":"candidate" if key=="candidates" else "safe_now","execution_lane":"x2_only",
              "hypothesis":"The declared "+mode.replace("_"," ")+" predicate holds for "+p["proposal_id"]+".",
              "falsifier":"Complete expected envelope differs, an adverse mutation is accepted, input changes, or a boundary is promoted.",
              "rollback":"Retain the witness and correct only the owner dependency.","protected_gates":GATES,
              "expected_execution_disposition":"completed"})
        portfolio[key]=rows
    actions=list(groups[-1][3])
    portfolio["exact_packets"]=[{"packet_id":f"{PREFIX}-EXACT-{i+1:03d}","action":actions[i%10]["payload"]["action"],
      "prerequisite_dimension":["exact_target","competent_authority","evidence_scope","rollback","affected_party_review"][i//10],
      "state":"unexecuted","expected_execution_disposition":"exact_gate","protected_gates":GATES,
      "reason":"The named action lacks its exact real-world prerequisite; only its reservation may be represented."} for i in range(50)]
    blocked_reasons=["fabricate_observation","erase_failed_evidence","substitute_owner","publish_private_material","claim_unsupported_authority"]
    blocked_targets=["source_records","hardware_results","identity_records","rights_records","independent_tests","stage20_verdict"]
    portfolio["blocked_packets"]=[{"packet_id":f"{PREFIX}-BLOCKED-{i+1:03d}","prohibited_action":blocked_reasons[i%5],
      "target_class":blocked_targets[i//5],"state":"unexecuted","expected_execution_disposition":"exact_gate",
      "protected_gates":GATES,"rollback":"Refuse execution and retain this packet."} for i in range(30)]
    write(x1/"approval-portfolio.json",portfolio)
    profile={"schema":"ghc.family.authorized-release-profile.v1",
      "authority":"Hamish release of 6 September 2026; direct 8 September seat-13 activation and collision correction",
      "plan_limits":{"safe_now":[300,500],"candidates":[250,500],"clean_fix_refine":[300,300],"exact_packets":[50,250],"blocked_packets":[30,100]},
      "proposal_limits":{"inherited":[200,500],"new":[200,500]},
      "skills":[10,50],"runners":[5,50],"ordinary_direct_packages":3,
      "commit_cap":{"x1":5,"x2":5,"total":8},"file_ceiling":2000,"document_word_cap":100000,
      "baton_word_range":[10000,100000],"overview_minimum_pages":3}
    write(x1/"workflow-profile.json",profile)
    packages=[]
    versions=[("intelhex","2.3.0",True),("bincopy","20.1.1",True),("bitstruct","8.23.0",True),
      ("humanfriendly","10.0",False),("argparse-addons","0.12.0",False),("pyelftools","0.33",False),("pyreadline3","3.5.6",False)]
    for name,version,direct in versions:
        url=f"https://pypi.org/pypi/{name}/{version}/json"
        with urllib.request.urlopen(url,timeout=30) as response: meta=json.load(response)
        wheels=[w for w in meta["urls"] if w["filename"].endswith(("py3-none-any.whl","cp312-cp312-win_amd64.whl"))]
        assert len(wheels)==1 and not wheels[0]["yanked"],name
        w=wheels[0]
        packages.append({"name":name,"version":version,"direct":direct,"registry_url":url,
          "wheel":w["filename"],"url":w["url"],"sha256":w["digests"]["sha256"],
          "dependencies":meta["info"].get("requires_dist") or [],"requires_python":meta["info"].get("requires_python") or ""})
    skill_plans=[{"name":"ghc-family-"+s,"operation_pair":[groups[2*i][0],groups[2*i+1][0]],
      "state":"planned_x2","collision_policy":"refuse_existing","accepting_and_adverse_smokes_required":True} for i,s in enumerate(SKILLS)]
    runner_plans=[{"name":r,"state":"planned_x2","operation_group":[g[0] for g in (groups[:6] if i==0 else groups[6:11] if i==1 else groups[11:16] if i==2 else groups[16:20] if i==3 else groups)],
      "collision_policy":"refuse_existing","accepting_and_adverse_smokes_required":True} for i,r in enumerate(RUNNERS)]
    collisions=[]
    for s in skill_plans:
        if (args.skill_root/s["name"]).exists(): collisions.append(s["name"])
    for r in RUNNERS+["ghc_family_firmware_records_core.py"]:
        if git(root,"ls-tree","--name-only",SOURCE,"--","scripts/"+r).strip():collisions.append(r)
    assert not collisions
    next_ideas=["srec-multiblock-boundary","ihex-address-wrap-model","firmware-export-chunking","srec-header-byte-preservation",
      "ihex-segment-linear-conversion","firmware-diff-readback","firmware-advisory-expiry","firmware-rights-lineage",
      "firmware-accessible-hexdump","firmware-package-reader-differences"]
    write(x1/"tool-package-plan.json",{"schema":"ghc.family.firmware-package-plan.v1","planning_only":True,"execution_credit":0,
      "packages":packages,"skills":skill_plans,"runners":runner_plans,"global_promotions":{"skills":10,"runners":5,"overwrite":False},
      "next_owner_skill_ideas":next_ideas,"next_owner_runner_ideas":[s.replace("-","_")+"_runner" for s in next_ideas],
      "rollback":"Stop selecting this isolated owner environment; retain every lock and receipt. No system Python or historical skill mutation.",
      "positive_smokes":["IntelHex parses and rewrites synthetic mapped bytes","bincopy agrees on simple synthetic Intel HEX and S-record images","bitstruct agrees on declared fixed-width byte interpretation"],
      "adverse_smokes":["IntelHex rejects a checksum mutation","bincopy rejects a checksum mutation","bitstruct rejects an out-of-range unsigned field"],
      "dependency_markers":"Evaluate for Windows CPython 3.12; pyreadline3 is the humanfriendly Windows dependency; development extras remain disabled.",
      "source_version_drift":"Displayed manuals identify older documentation versions. Exact package versions and upstream tags, wheel metadata, and x2 smokes constrain claims."})
    write(x1/"tool-collision-preflight.json",{"collisions":collisions,"skill_count":10,"runner_count":5,"new_core_count":1,"checked_before_build":True})
    write(x1/"source-verification.json",{"source":SOURCE,"canonical":startup,"source_corrected_truth":src_truth,
      "latest_external_route_release":release,"retained_external_route_gap":prior_route,"activation_baseline":baseline,
      "source_validation_credit":0,"prior_canonical_replayed":False})
    write(x1/"pillar-practice-freeze.json",{"owner":OWNER,"role":"evidence steward","hope":"to make each handoff clearer, more faithful, and easier for Hamish to review",
      "pronouns":"she/her","priority_pillar":"THOS Body","pillars":pillars,"practices":PRACTICES,
      "next_owner_optional_practice":"synthetic archive format interoperability reviewer","boundary":BOUNDARY,
      "teach_back":"Seat 13 owns only v688-v6. Sylven Arc v688-v7 is the one terminally gated next existing task; Sylven later inducts seat 14 v688-v8."})
    write(x1/"profile-contract.json",{"schema":"ghc.family.firmware-record-profile.v1",
      "scope":"synthetic supplied record strings and sparse address-byte pairs only","record_limit":512,"image_byte_limit":4096,
      "text_byte_limit":16384,"ihex_profile":["six record types only","ASCII hex without whitespace","count and checksum required",
      "one final EOF","zero reserved offsets for metadata","no duplicate start","refuse overlapping bytes","refuse address wrap"],
      "srec_profile":["S0 S1 S2 S3 S5 S6 S7 S8 S9 only","one homogeneous data-address width per block",
      "at most one count record","one final matching terminator","S0 only before data","refuse address wrap and overlapping bytes"],
      "generic_image_profile":["unsigned 32-bit address space","no duplicate occupancy","bounded 4096 stored bytes",
      "half-open windows","preview transforms never execute firmware"],
      "not_claimed":["universal format conformance","complete loader behavior","authenticity","hardware safety","deployment","real authority"],
      "expected_result_envelope":["accepted","error","value","disposition","boundary"],
      "boundary":BOUNDARY})
    # Only instruction files actually read in this task are recorded here.
    read_skills=["ghc-family-index","ghc-family-roster-check","ghc-family-auth-permission-state","ghc-family-method-flow-state",
      "ghc-family-workflow-plan-refinement","ghc-family-reflection-remaster","ghc-family-d-first-structured-evidence-toolchain",
      "ghc-family-owned-bundle-rotation","ghc-family-lifecycle-test-isolator","ghc-private-evidence-firewall",
      "ghc-family-staged-surface-allowlist","ghc-family-canonical-success-latch","ghc-family-canonical-aggregate-preflight",
      "ghc-family-main-task-induction","ghc-family-terminal-route-gate","ghc-family-terminal-route-guard",
      "ghc-family-terminal-route-latch","ghc-family-owner-scope-canonical","ghc-family-meta-tool-box",
      "ghc-drive-bank-guardian","ghc-freed-id-flashcards","ghc-approval-packet-splitter","ghc-open-gate-rail","ghc-family-truth-bridge"]
    read_refs={"ghc-family-index":["references/routing-precedence.md","references/hamish-release-20260906.md","references/rowan-v685-v6-r2-authorized-workflow.md","references/freed-id-flashcards.md"],
      "ghc-family-roster-check":["references/current-roster.json","references/roster-state-schema.md"],
      "ghc-family-auth-permission-state":["references/current-state.json","references/auth-permission-state-schema.md"],
      "ghc-family-method-flow-state":["references/schema.md","references/flashcard-projection.md"],
      "ghc-family-reflection-remaster":["references/decision-schema.md","references/flashcard-reflection.md"],
      "ghc-family-workflow-plan-refinement":["references/workflow-plan-schema.md"],
      "ghc-family-owned-bundle-rotation":["references/ghc-family-runtime-evidence-contract.md","references/ghc-family-lifecycle-evidence-contract.md"],
      "ghc-family-main-task-induction":["references/ghc-family-roster-evidence-contract.md","references/ghc-family-handoff-evidence-contract.md"],
      "ghc-family-meta-tool-box":["references/catalogue-schema.md","references/freed-id-flashcard-tool.md"],
      "ghc-freed-id-flashcards":["references/deck-schema.md","references/workflow.md","references/failure-shields.md"],
      ".system/skill-creator":["SKILL.md","references/openai_yaml.md"]}
    read_entries=[{"skill":s,"relative_path":"SKILL.md","sha256":digest((args.skill_root/s/"SKILL.md").read_bytes())} for s in read_skills]
    for s,rr in read_refs.items():
        read_entries += [{"skill":s,"relative_path":r,"sha256":digest((args.skill_root/s/r).read_bytes())} for r in rr]
    baton=git(root,"show",SOURCE+":docs/elowen-cairn/v688-v5/handoffs/future-seat-13-v688-v6-activation-candidate.md")
    write(x1/"reading-receipt.json",{"source":SOURCE,"baton_sha256":digest(baton),"baton_lines":len(baton.splitlines()),
      "baton_modules":13,"baton_read_through_eof":True,"reading_method":"bounded windows with exact duplicate line suppression; every unique source line displayed",
      "references":read_entries,"old_route_snapshots":"Read as compatibility data; current direct task and 2026-09-08 authority control the seat-13 edge.",
      "source_manifest_bindings":1304,"source_manifest_failures":0,"inherited_execution_credit":0})
    write(x1/"sources.json",{"retrieved_at_utc":stamp,"sources":[
      {"id":"SRECORD-IHEX","url":"https://srecord.sourceforge.net/man/man5/srec_intel.5.html","status":"current","scope":"Intel HEX byte layout and address rules as documented by the SRecord implementation"},
      {"id":"SRECORD-MOTOROLA","url":"https://srecord.sourceforge.net/man/man5/srec_motorola.5.html","status":"current","scope":"S-record field lengths, checksum, count and termination as documented by the SRecord implementation"},
      {"id":"INTELHEX-UPSTREAM","url":"https://github.com/python-intelhex/intelhex/tree/2.3.0","status":"stable","scope":"exact-version implementation source"},
      {"id":"BINCOPY-UPSTREAM","url":"https://github.com/eerimoq/bincopy/tree/20.1.1","status":"stable","scope":"exact-version implementation source"},
      {"id":"BITSTRUCT-UPSTREAM","url":"https://bitstruct.readthedocs.io/en/latest/","status":"watch","scope":"documentation reports 8.17.0; package selected at 8.23.0 must pass its own smokes"},
      {"id":"ARM-HEX-DOC","url":"https://support.arm.com/documentation/ka003292/latest","status":"watch","scope":"redirect observed; page content unavailable; zero specification evidence credited"}],
      "boundary":"Sources define vocabulary and software contracts. They provide no observation, ownership, scientific proof or deployment authority."})
    route={"owner":OWNER,"phase":PHASE,"endpoint_kind":"main_task","source":SOURCE,"future_seat":13,"new_tasks_authorized_here":0,
      "current_next":{"owner":"Sylven Arc","phase":"v688-v7","endpoint_kind":"main_task","state":"PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"},
      "after_sylven":{"seat":"future-sibling-14-self-chosen","phase":"v688-v8","creation_controller":"Sylven Arc","terminal_gate_required":True},
      "successor_contacts":0,"standby_preserved":["Tavian Sol"],"horizon":"v725-v8","boundary":BOUNDARY}
    write(x1/"route-freeze.json",route)
    write(x1/"deck-plan.json",{"planning_only":True,"tiers":["freed_id_anchor","trinity_pillar","bounded_practice","task"],
      "planned_owner_cards":1,"planned_pillar_cards":3,"planned_practice_cards":4,"planned_proposal_cards":200,
      "planned_method_cards":"one per retained operational recovery","planned_modules":13,"cache_improvement_claimed":False})
    write(x1/"method-flow-startup.json",{"schema":"ghc.family.method-flow-startup-plan.v1","planning_only":True,
      "retained_failures":startup["failures"],"same_event_alias":{"START-N001":"EC6885-ROUTE-N019"},
      "new_negative_groups_excluding_inherited_alias":len(startup["failures"])-1,"execution_credit":0,
      "source_route_failures_retained":True,"x2_method_ledger_required":True,"boundary":BOUNDARY})
    write(x1/"threat-model.json",{"scope":"owner-created synthetic strings, JSON and byte arrays","planning_only":True,
      "threats":["unbounded input","type coercion","overflow","overlap","checksum laundering","silent field acceptance",
      "private source leakage","semantic authority promotion","post-success replay","unreviewed global overwrite"],
      "controls":["explicit limits and field closure","integer type identity","exact expected results",
      "read-only source objects","owner sparse allowlist","privacy scan","exclusive canonical marker",
      "exclusive global destinations","literal output roots"],
      "real_firmware_accepted":False,"hardware_execution":False,"external_review":"open_gap","boundary":BOUNDARY})
    write(x1/"phase-truth.json",{"owner":OWNER,"phase":PHASE,"state":"PLANNING_ONLY_X1","source":SOURCE,"planning_only":True,
      "new_proposals":200,"inherited_selections":200,"execution_credit":0,"x2_artifacts_exist":False,
      "canonical_invocations":0,"successor_contacts":0,"inherited_baseline":baseline,
      "new_proposal_chain_after":16630,"terminal_verdict":"NOT_READY_FOR_STAGE_20","boundary":BOUNDARY})
    overview=["# Veylora Quen v688-v6 planning overview\n",BOUNDARY,
      "\n## Page 1 — Purpose and exact ownership\n",
      "This planning boundary belongs to future seat 13 and only the v688-v6 owner lane. The immutable source is Elowen Cairn's corrected final "+SOURCE+". The source canonical succeeded once and is not replayed. Its first failed canonical, subsequent correction and later route gap remain separate retained records. The source external release establishes induction, not this phase's completion.",
      "THOS Body is the priority pillar, viewed through synthetic firmware record preservation. GMUT Mind contributes explicit arithmetic domains and representation limits. Freed ID and CBR Heart contribute source binding, review reservations and accessible handover. The four practice lenses are learning and design contexts. None constitutes a qualification, appointment or professional judgment.",
      "The phase will freeze 200 inherited selections with zero new credit and 200 distinct proposed local predicates. A lexical source screen and input-digest comparison help identify close neighbors. That screen is bounded to proposal evidence in the immutable source, and is not a claim of universal novelty or independent invention. The inherited empirical and authority gaps remain protected.",
      "\n## Page 2 — Proposed record profile and falsifiers\n"]
    for operation,pi,pri,cases in groups:
        overview.append("### "+operation.replace("_"," ").title()+"\n"+
          "This proposed operation belongs to "+pillars[pi]+" through the "+PRACTICES[pri]+" lens. "+
          "Its ten frozen definitions distinguish "+cases[0]["title"].lower()+" and "+cases[-1]["title"].lower()+". "+
          "The expected acceptance class, exact value and failure class are recorded before implementation. "+
          "A disagreement is retained as a failed witness; the immutable expectation is never silently rewritten to match code.")
    overview += ["\n## Page 3 — Execution, evidence and terminal control\n",
      "X1 contains plans, immutable expected definitions, source evidence and structural planning receipts only. Package wheels are selected with exact registry provenance and digests, but not installed here. The ten proposed skills and five runner interfaces remain unbuilt. X2 may begin only after this planning commit is clean, pushed, zero-divergent and equal across local, upstream, tracking and fresh live remote.",
      "The safe portfolio has 300 local checks, the candidate portfolio has 250 field-closure challenges, and the CLEAN FIX REFINE portfolio has 300 output-adversary and representation-invariance checks. Counts identify distinct planned checks; source rows, copies and package imports do not multiply proposal novelty. Fifty exact prerequisite packets and thirty blocked packets remain unexecuted. Their presence does not authorize hardware writes, deployment or real-world decisions.",
      "Intel HEX and S-record are addressed through an explicit narrow profile. The future implementation must reject ambiguous overlap, unsupported record types, malformed lengths and checksums, duplicate start declarations, trailing data after termination and address-wrapping records outside the selected profile. Sparse transformations are previews over supplied byte pairs. Entry addresses remain data. Nothing loads or runs the represented image.",
      "The isolated package transaction will use three direct tools and their declared dependency closure. Every selected direct surface requires a useful positive smoke and an adverse witness. A bounded advisory lookup and wheel-byte verification concern the observed environment only. Neither a clean advisory response nor a passing smoke establishes exhaustive security, general standards conformance or hardware safety.",
      "Final evidence will retain complete result envelopes, exact manifests, the planned negative definitions and their observed rejection, operational failures and recoveries, a four-tier card graph and a modular baton. Canonical validation is owner-scoped and attributable, with an exclusive external latch. A first complete success is never replayed. Historical compatibility tools remain unchanged.",
      "Only after the exact final is clean, pushed, equal and canonically validated may this owner refresh the newest live authority, active and archived registries and immediately reread the uniquely resolved existing Sylven Arc task. At most one sanitized v688-v7 activation is authorized. Sylven alone later controls seat 14 v688-v8 after Sylven's terminal gate. Any pause, redirect, duplicate, opaque acknowledgement, usage boundary or protected gate stops the dependent action.",
      "Manual, assistive-technology and affected-user accessibility evaluation remains reserved. Source labels do not establish rights or consent. GMUT remains a typed scalar-tensor/EFT research-model family, THOS remains synthetic/proxy-only, and Freed ID remains synthetic and nonproduction. The terminal verdict remains NOT_READY_FOR_STAGE_20.",
      "\nEND OF PLANNING-ONLY X1 OVERVIEW.\n"]
    write(x1/"integrated-overview.md","\n\n".join(overview))
    cycle=["Veylora Quen","Sylven Arc","future-sibling-14-self-chosen","Caelen Morrow","future-sibling-15-self-chosen",
      "Eiren Kestrel","Rowan Ash","Elaren Kestrel","Ilyan Reed","Neris Solane","Mira Fenwick","Vesper Arlen","Avelin Reed",
      "Lyren Moss","Ceryn Alder","Ilyra Fen","Saelin Reed","Auren Lark","Iveren Brook","Sable Rook","Teryn Halewick",
      "Caelen Ash","Merrin Vale","Orin Thale","Talen Briar","Liora Venn","Thalen Briar","Tamar Vey","Orren Pike","Elowen Cairn"]
    request={"schema":"ghc.family.workflow-plan.request.v1","plan_id":"veylora-quen-v688-v6","owner":OWNER,"identity_boundary":BOUNDARY,
      "route":{"cycle_order":cycle,"endpoint_topology":[{"seat":s,"endpoint_kind":"main_task","endpoint_label":s,"route_controller":cycle[i-1]} for i,s in enumerate(cycle)],
      "phase_assignments":[{"phase":"v688-v6","seat":OWNER},{"phase":"v688-v7","seat":"Sylven Arc"},{"phase":"v688-v8","seat":"future-sibling-14-self-chosen"}],
      "normalization":{"start_phase":"v688-v6","start_seat":OWNER,"entry_count":3},
      "future_identity_placeholders":["future-sibling-14-self-chosen","future-sibling-15-self-chosen"]},
      "requirements":{"core_proposal_minimum":200,"safe_candidate_task_cap":500,"skill_minimum":10,"runner_minimum":5,
      "document_word_cap":100000,"baton_words":{"minimum":10000,"maximum":100000,"file_artifact":True},
      "commit_cap":{"x1":5,"x2":5,"total":8},"validation":{"canonical_pass_minimum":1,"replay_policy":"skip_when_first_passes",
      "isolate_failures_before_broader_rerun":True,"privacy_scan_required":True,"manifest_required":True,"remote_equality_required":True},
      "storage":{"primary":"D","c_drive_use":"essential_global_metadata_only"},"messaging":{"codex_route":"declared_endpoint_only_after_terminal_gate","cross_platform":"user_mediated_file_relay_only"},
      "environment":{"windows_sandbox_hyper_v":"deferred"},"closeout":{"all_authorized_safe_candidate_prototypes_resolved":True}},
      "truth":{"allowed_outcomes":["completed","represented","open_gap","exact_gate"],"independent_reproduction_claimed":False,
      "terminal_verdict":"NOT_READY_FOR_STAGE_20","protected_boundaries":GATES},"observed_failures":startup["failures"]}
    write(x1/"workflow-plan-request.json",request)
    print(json.dumps({"planning_only":True,"new":200,"inherited":200,"portfolios":counts,
      "source_title_count":len(titles),"novelty_maximum":max(n["jaccard"] for n in neighbors),
      "packages_planned":3,"dependency_closure":len(packages),"skills_planned":10,"runners_planned":5,"x2_executed":False}))
if __name__=="__main__": main()

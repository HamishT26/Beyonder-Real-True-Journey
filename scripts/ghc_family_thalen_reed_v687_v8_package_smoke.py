"""Three pinned-package positive/adverse witnesses over synthetic in-memory bytes."""
import argparse
import hashlib
import io
import json
import struct
from importlib.metadata import version
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    import soundfile as sf
    import numpy as np
    import bitstruct
    from construct import Struct, Bytes, Int32ul, StreamError
    rows=[]
    samples=np.array([-32768,-1,0,1,32767],dtype=np.int16)
    stream=io.BytesIO();sf.write(stream,samples,8000,format='WAV',subtype='PCM_16');stream.seek(0)
    recovered,rate=sf.read(stream,dtype='int16',always_2d=True)
    positive=bool(rate==8000 and recovered.shape==(5,1) and np.array_equal(recovered[:,0],samples))
    rejected=False
    try:sf.read(io.BytesIO(b'RIFF'),dtype='int16')
    except sf.LibsndfileError:rejected=True
    rows.append({'name':'soundfile','version':version('soundfile'),'positive_pass':positive,'adverse_rejected':rejected,'adverse_success_credit':0,'fixture_frames':5,'source_audio':'synthetic_in_memory','libsndfile_version':sf.__libsndfile_version__})
    parser=Struct('magic'/Bytes(4),'size'/Int32ul,'form'/Bytes(4))
    header=b'RIFF'+struct.pack('<I',4)+b'WAVE';p=parser.parse(header)
    rejected=False
    try:parser.parse(b'RIFF')
    except StreamError:rejected=True
    rows.append({'name':'construct','version':version('construct'),'positive_pass':bool(p.magic==b'RIFF' and p.size==4 and p.form==b'WAVE'),'adverse_rejected':rejected,'adverse_success_credit':0})
    packed=bitstruct.pack('s16s16',-32768,32767);unpacked=bitstruct.unpack('s16s16',packed)
    rejected=False
    try:bitstruct.pack('s16',32768)
    except bitstruct.Error:rejected=True
    rows.append({'name':'bitstruct','version':version('bitstruct'),'positive_pass':unpacked==(-32768,32767),'adverse_rejected':rejected,'adverse_success_credit':0,'packed_sha256':hashlib.sha256(packed).hexdigest()})
    report={'schema':'ghc.family.package-smokes.v1','rows':rows,'same_owner_only':True,'independent_reproduction':False,'audio_playback':False,'real_audio':False,'all_pass':all(r['positive_pass'] and r['adverse_rejected'] for r in rows)}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(report));assert report['all_pass']

if __name__=='__main__':main()

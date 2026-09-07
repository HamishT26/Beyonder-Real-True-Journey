"""Owner-only frozen contracts and cross-case invariants for synthetic PCM evidence."""
import copy
import hashlib
import io
import itertools
import json
import struct
import sys
import unittest
import wave
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_pcm_evidence_core import evaluate, strict_load, Refusal

def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(',',':'))

class PCMEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=json.loads((ROOT/'docs/thalen-reed/v687-v8/x1/new-proposals.json').read_text(encoding='utf-8'))['proposals']

    def test_all_frozen_complete_outputs(self):
        for c in self.cases:
            with self.subTest(proposal=c['proposal_id']):
                self.assertEqual(canon(evaluate(c['input'])),canon(c['expected_output']))

    def test_all_inputs_remain_unchanged(self):
        for c in self.cases:
            x=copy.deepcopy(c['input']);before=canon(x);evaluate(x);self.assertEqual(canon(x),before)

    def test_runtime_does_not_consume_proposal_ordinals(self):
        for c in self.cases[::20]:
            x=dict(c['input'],ordinal=7)
            self.assertEqual(evaluate(x)['error'],'FIELD_SET')

    def test_unknown_operation_is_held(self):
        self.assertEqual(evaluate({'operation':'unknown'})['error'],'OPERATION')

    def test_nonobject_record_is_held(self):
        for x in [None,[],1,True,'riff_chunks']:
            self.assertEqual(evaluate(x)['error'],'RECORD_TYPE')

    def test_wrapper_scope_is_enforced(self):
        self.assertEqual(evaluate(self.cases[0]['input'],['pcm_range'])['error'],'OPERATION_SCOPE')

    def test_duplicate_root_json_key_is_rejected(self):
        with self.assertRaisesRegex(Refusal,'DUPLICATE_JSON_KEY'):
            strict_load('{"x":1,"x":2}')

    def test_duplicate_nested_json_key_is_rejected(self):
        with self.assertRaisesRegex(Refusal,'DUPLICATE_JSON_KEY'):
            strict_load('{"outer":{"x":1,"x":2}}')

    def test_nonfinite_json_constants_are_rejected(self):
        for s in ['NaN','Infinity','-Infinity']:
            with self.assertRaisesRegex(Refusal,'NONFINITE_JSON_CONSTANT'):
                strict_load('{"value":'+s+'}')

    def test_boolean_and_integer_outputs_are_distinct(self):
        self.assertNotEqual(canon({'accepted':True}),canon({'accepted':1}))

    def test_riff_limits_are_applied_before_payload_interpretation(self):
        self.assertEqual(evaluate({'operation':'riff_chunks','hex':'00'*65537})['error'],'BYTE_LIMIT')

    def test_riff_chunk_count_is_bounded(self):
        body=b'WAVE'+(b'JUNK'+struct.pack('<I',0))*65
        raw=b'RIFF'+struct.pack('<I',len(body))+body
        self.assertEqual(evaluate({'operation':'riff_chunks','hex':raw.hex()})['error'],'CHUNK_LIMIT')

    def test_nonascii_fourcc_is_refused(self):
        body=b'WAVE'+b'\xffabc'+struct.pack('<I',0)
        raw=b'RIFF'+struct.pack('<I',len(body))+body
        self.assertEqual(evaluate({'operation':'riff_chunks','hex':raw.hex()})['error'],'FOURCC_ASCII')

    def test_python_wave_fixture_has_consistent_container_and_frame_arithmetic(self):
        buffer=io.BytesIO()
        with wave.open(buffer,'wb') as writer:
            writer.setnchannels(2);writer.setsampwidth(2);writer.setframerate(8000)
            writer.writeframes(struct.pack('<hhhh',-32768,32767,0,1))
        raw=buffer.getvalue()
        result=evaluate({'operation':'riff_chunks','hex':raw.hex()})
        self.assertTrue(result['accepted'])
        chunks=result['value']['chunks'];self.assertEqual([c['id'] for c in chunks],['fmt ','data'])
        fmt=next(c for c in chunks if c['id']=='fmt ');values=struct.unpack_from('<HHIIHH',raw,fmt['offset']+8)
        tag,channels,rate,byte_rate,align,bits=values
        parsed=evaluate({'operation':'pcm_format','tag':tag,'channels':channels,'rate':rate,'bits':bits,'block_align':align,'byte_rate':byte_rate})
        self.assertEqual(parsed['value']['frame_bytes'],4)
        data=next(c for c in chunks if c['id']=='data')
        frames=evaluate({'operation':'pcm_frames','data_bytes':data['size'],'block_align':align,'declared_frames':2})
        self.assertEqual(frames['value']['frames'],2)

    def test_sample_time_roundtrip_for_multiple_rates_origins_and_indices(self):
        for rate,index,origin in itertools.product([1,8000,11025,44100,48000,96000],[0,1,7,100000],['0','1/3','-7/2']):
            seconds=evaluate({'operation':'sample_time','mode':'to_seconds','index':index,'rate':rate,'origin':origin})
            self.assertTrue(seconds['accepted'])
            reverse=evaluate({'operation':'sample_time','mode':'to_index','seconds':seconds['value']['seconds'],'rate':rate,'origin':origin})
            self.assertEqual(reverse['value']['index'],index)

    def test_half_sample_is_never_rounded(self):
        for rate in [1,8000,44100,48000]:
            result=evaluate({'operation':'sample_time','mode':'to_index','seconds':str(Fraction(1,2*rate)),'rate':rate,'origin':'0'})
            self.assertEqual(result['error'],'OFF_SAMPLE_GRID')

    def test_channel_inverse_recovers_each_original_frame(self):
        for n in range(1,5):
            labels=[str(i) for i in range(n)];frames=[list(range(n)),list(range(n,2*n))]
            for order in itertools.permutations(range(n)):
                first=evaluate({'operation':'channel_permutation','channels':labels,'frames':frames,'order':list(order)})['value']
                back=evaluate({'operation':'channel_permutation','channels':first['channels'],'frames':first['frames'],'order':first['inverse']})['value']
                self.assertEqual(back['channels'],labels);self.assertEqual(back['frames'],frames)

    def test_unicode_labels_are_preserved_without_identity_inference(self):
        labels=['left-α','right-β']
        value=evaluate({'operation':'channel_permutation','channels':labels,'frames':[],'order':[1,0]})['value']
        self.assertEqual(value['channels'],labels[::-1])

    def test_edit_partition_for_all_six_frame_subsets(self):
        n=6
        for flags in itertools.product([False,True],repeat=n):
            spans=[];start=None
            for i,kept in enumerate(flags+(False,)):
                if kept and start is None:start=i
                if not kept and start is not None:spans.append([start,i]);start=None
            result=evaluate({'operation':'edit_intervals','source_frames':n,'keep':spans})['value']
            self.assertEqual(result['output_frames'],sum(flags))
            kept={i for a,b in spans for i in range(a,b)}
            removed={i for a,b in result['dropped'] for i in range(a,b)}
            self.assertFalse(kept & removed);self.assertEqual(kept | removed,set(range(n)))
            self.assertEqual(sum(b-a for a,b in result['dropped'])+result['output_frames'],n)

    def test_all_small_byte_subsegments_bind_without_text_conversion(self):
        raw=bytes([0,255,13,10,128,65,0,66]);sha=lambda b:hashlib.sha256(b).hexdigest()
        for a in range(len(raw)+1):
            for b in range(a,len(raw)+1):
                out=evaluate({'operation':'segment_binding','hex':raw.hex(),'start':a,'end':b,'source_sha256':sha(raw),'segment_sha256':sha(raw[a:b])})
                self.assertTrue(out['accepted']);self.assertEqual(out['value']['segment_bytes'],b-a)

    def test_byte_change_invalidates_source_binding(self):
        x=copy.deepcopy(self.cases[140]['input']);x['hex']='00'+x['hex'][2:]
        self.assertEqual(evaluate(x)['error'],'SOURCE_DIGEST_MISMATCH')

    def test_numeric_rail_does_not_claim_clipping(self):
        out=evaluate({'operation':'pcm_range','bits':16,'signed':True,'samples':[-32768,32767]})
        self.assertEqual(out['value']['rail_indices'],[0,1]);self.assertIs(out['value']['clipping_established'],False)

    def test_unknown_fields_are_refused_across_all_operations(self):
        for c in self.cases[::20]:
            self.assertEqual(evaluate(dict(c['input'],unexpected='value'))['error'],'FIELD_SET')

    def test_missing_fields_are_refused_across_all_operations(self):
        for c in self.cases[::20]:
            x=dict(c['input']);key=next(k for k in x if k not in ['operation','mode']);del x[key]
            self.assertEqual(evaluate(x)['error'],'FIELD_SET')

    def test_represented_metrics_never_establish_perceptual_effectiveness(self):
        for c in self.cases[160:170]:
            out=evaluate(c['input'])['value']
            self.assertIs(out['perceptual_effectiveness_established'],False)
            self.assertIs(out['independent_reproduction'],False)

    def test_claimed_permissions_do_not_authorize_external_actions(self):
        for c in self.cases[184:]:
            out=evaluate(c['input'])['value'];self.assertEqual(out['disposition'],'exact_gate')
            self.assertIs(out['executed_external_action'],False)
            empty=dict(c['input'],claimed_permissions=[])
            self.assertEqual(canon(evaluate(empty)),canon(evaluate(c['input'])))

    def test_real_source_cannot_enter_local_disclosure_contract(self):
        x=dict(self.cases[180]['input'],source_kind='real')
        self.assertEqual(evaluate(x)['error'],'REAL_AUDIO_AUTHORITY_REQUIRED')

    def test_all_operations_deny_external_credit(self):
        for c in self.cases:self.assertIs(evaluate(c['input'])['external_credit'],False)

if __name__=='__main__':unittest.main()

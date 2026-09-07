"""Planning-only PCM evidence fixtures. This file contains no runtime evaluator."""
from __future__ import annotations

import copy
import hashlib
import json
import struct
from collections import Counter

CASES = []

def accept(value):
    return {"accepted": True, "value": value, "error": None, "external_credit": False}

def hold(code):
    return {"accepted": False, "value": None, "error": code, "external_credit": False}

def add(operation, title, payload, expected, disposition="completed"):
    CASES.append({"proposal_id": f"TR6878-N{len(CASES)+1:03d}", "operation": operation,
                  "title": title, "input": {"operation": operation, **payload},
                  "expected_output": expected, "expected_execution_disposition": disposition})

def chunk_fixture(specs, form=b"WAVE"):
    body = form
    expected = []
    for label, payload, pad in specs:
        offset = 8 + len(body)
        padding = bytes([pad]) if len(payload) % 2 else b""
        body += label + struct.pack("<I", len(payload)) + payload + padding
        expected.append({"id": label.decode("ascii"), "offset": offset,
                         "size": len(payload), "pad_hex": padding.hex()})
    raw = b"RIFF" + struct.pack("<I", len(body)) + body
    return raw, {"form": form.decode("ascii"), "bytes": len(raw), "chunks": expected}

def riff_cases():
    op = "riff_chunks"
    definitions = [
        ("Empty WAVE envelope preserves its twelve-byte boundary", []),
        ("Empty data chunk remains an addressable zero-length chunk", [(b"data", b"", 0)]),
        ("Odd JUNK payload consumes its one padding byte", [(b"JUNK", b"a", 0)]),
        ("Even payload does not consume a padding byte", [(b"data", b"ab", 0)]),
        ("Unknown chunk remains in source order", [(b"zzzz", b"ab", 0), (b"data", b"c", 0)]),
        ("Space is preserved inside a FOURCC", [(b" abc", b"", 0)]),
        ("Duplicate data identifiers are retained by the container walk", [(b"data", b"a", 0), (b"data", b"bc", 0)]),
        ("Chunk walking does not infer format semantics from duplicate fmt", [(b"fmt ", b"", 0), (b"fmt ", b"", 0)]),
        ("Nonzero padding is retained as bytes rather than discarded", [(b"JUNK", b"abc", 127)]),
        ("Three heterogeneous chunks retain exact offsets", [(b"fmt ", b"abcd", 0), (b"JUNK", b"x", 1), (b"data", b"abcdef", 0)]),
    ]
    for title, specs in definitions:
        raw, expected = chunk_fixture(specs)
        add(op, title, {"hex": raw.hex()}, accept(expected))
    raw, _ = chunk_fixture([(b"data", b"abc", 0)])
    defects = [
        ("No header bytes cannot describe a RIFF envelope", b"", "TRUNCATED_RIFF_HEADER"),
        ("Four-byte magic alone cannot supply a size or form", b"RIFF", "TRUNCATED_RIFF_HEADER"),
        ("Eleven-byte envelope is one byte short of its form", raw[:11], "TRUNCATED_RIFF_HEADER"),
        ("Big-endian RIFX is explicitly outside this walker", b"RIFX" + raw[4:], "UNSUPPORTED_CONTAINER"),
        ("AVI form is not silently accepted as WAVE", raw[:8] + b"AVI " + raw[12:], "UNSUPPORTED_FORM"),
        ("Declared RIFF size cannot understate the supplied bytes", raw[:4] + struct.pack("<I", len(raw)-9) + raw[8:], "RIFF_SIZE_MISMATCH"),
        ("Declared RIFF size cannot overstate the supplied bytes", raw[:4] + struct.pack("<I", len(raw)-7) + raw[8:], "RIFF_SIZE_MISMATCH"),
        ("Partial chunk header is retained as a refusal", b"RIFF" + struct.pack("<I", 7) + b"WAVEabc", "TRUNCATED_CHUNK_HEADER"),
        ("Chunk length may not exceed its containing envelope", b"RIFF" + struct.pack("<I", 12) + b"WAVEdata" + struct.pack("<I", 9), "CHUNK_OVERRUN"),
        ("An odd payload without its pad byte is refused", b"RIFF" + struct.pack("<I", 13) + b"WAVEdata" + struct.pack("<I", 1) + b"x", "MISSING_PADDING"),
    ]
    for title, raw, code in defects:
        add(op, title, {"hex": raw.hex()}, hold(code))

def format_cases():
    op = "pcm_format"
    base = {"tag": 1, "channels": 2, "rate": 48000, "bits": 16,
            "block_align": 4, "byte_rate": 192000}
    for title, ch, rate, bits in [
        ("Eight-bit mono uses one byte per frame", 1, 8000, 8),
        ("Sixteen-bit mono uses two bytes per frame", 1, 44100, 16),
        ("Eight-bit stereo uses two bytes per frame", 2, 11025, 8),
        ("Sixteen-bit stereo uses four bytes per frame", 2, 48000, 16),
        ("One-hertz integer sample rate is retained literally", 1, 1, 8),
        ("High-rate PCM arithmetic remains a metadata claim", 2, 192000, 16),
    ]:
        align = ch * bits // 8
        p = dict(base, channels=ch, rate=rate, bits=bits, block_align=align, byte_rate=rate*align)
        add(op, title, p, accept({"frame_bytes": align, "byte_rate": rate*align,
                                 "sample_encoding": "unsigned" if bits == 8 else "signed"}))
    for title, patch, code in [
        ("Zero channel count is refused", {"channels": 0}, "CHANNEL_COUNT"),
        ("Three-channel classic PCM is outside the declared profile", {"channels": 3}, "CHANNEL_COUNT"),
        ("A zero sample rate cannot define frame time", {"rate": 0}, "SAMPLE_RATE"),
        ("Negative sample rate is refused", {"rate": -1}, "SAMPLE_RATE"),
        ("Boolean sample rate does not pass as integer one", {"rate": True}, "INTEGER_TYPE"),
        ("Fractional numeric sample rate is not rounded", {"rate": 44100.5}, "INTEGER_TYPE"),
        ("Twenty-four-bit PCM needs a separately declared extended profile", {"bits": 24}, "SAMPLE_BITS"),
        ("Zero-width samples cannot define block alignment", {"bits": 0}, "SAMPLE_BITS"),
        ("IEEE float tag is not treated as integer PCM", {"tag": 3}, "FORMAT_TAG"),
        ("Extensible tag is retained as unsupported by the classic profile", {"tag": 65534}, "FORMAT_TAG"),
        ("Mismatched block alignment is refused", {"block_align": 2}, "BLOCK_ALIGN_MISMATCH"),
        ("Mismatched average byte rate is refused", {"byte_rate": 96000}, "BYTE_RATE_MISMATCH"),
        ("Sample rate beyond the bounded profile is held", {"rate": 384001}, "SAMPLE_RATE"),
        ("Unknown format metadata is not silently dropped", {"extension": 0}, "FIELD_SET"),
    ]:
        add(op, title, dict(base, **patch), hold(code))

def frame_cases():
    op = "pcm_frames"
    for title, size, align, declared, count in [
        ("Zero bytes represent zero frames", 0, 1, None, 0),
        ("One mono eight-bit byte represents one frame", 1, 1, 1, 1),
        ("A stereo sixteen-bit frame uses four bytes", 4, 4, 1, 1),
        ("Two complete frames retain a declared match", 8, 4, 2, 2),
        ("Missing declared count remains unknown", 12, 4, None, 3),
        ("Twenty-four-bit stereo alignment is six bytes in the generic counter", 18, 6, 3, 3),
        ("Eight channels with four-byte samples use alignment thirty-two", 64, 32, 2, 2),
        ("One-megabyte upper byte boundary is representable", 1048576, 8, 131072, 131072),
    ]:
        add(op, title, {"data_bytes": size, "block_align": align, "declared_frames": declared},
            accept({"frames": count, "declared_frames": declared, "declaration_checked": declared is not None}))
    base = {"data_bytes": 8, "block_align": 4, "declared_frames": 2}
    for title, patch, code in [
        ("A partial final frame is not silently truncated", {"data_bytes": 7}, "PARTIAL_FRAME"),
        ("Zero alignment is refused before division", {"block_align": 0}, "BLOCK_ALIGN"),
        ("Negative alignment is refused", {"block_align": -1}, "BLOCK_ALIGN"),
        ("Overwide alignment exceeds this bounded counter", {"block_align": 65}, "BLOCK_ALIGN"),
        ("Negative byte count is refused", {"data_bytes": -1}, "DATA_BYTES"),
        ("Counter byte ceiling is enforced", {"data_bytes": 1048577}, "DATA_BYTES"),
        ("Boolean byte count cannot masquerade as integer", {"data_bytes": False}, "INTEGER_TYPE"),
        ("Float alignment is not coerced", {"block_align": 4.0}, "INTEGER_TYPE"),
        ("A contradictory declared count remains a mismatch", {"declared_frames": 3}, "FRAME_COUNT_MISMATCH"),
        ("A negative declaration is invalid metadata", {"declared_frames": -1}, "DECLARED_FRAMES"),
        ("Boolean declaration is not a one-frame claim", {"declared_frames": True}, "INTEGER_TYPE"),
        ("Extra counter fields require a new contract", {"duration": 1}, "FIELD_SET"),
    ]:
        add(op, title, dict(base, **patch), hold(code))

def time_cases():
    op = "sample_time"
    for title, payload, value in [
        ("Frame zero with zero origin maps to exact zero", {"mode":"to_seconds","index":0,"rate":44100,"origin":"0"}, {"seconds":"0","index":0}),
        ("A single frame keeps its exact rational time", {"mode":"to_seconds","index":1,"rate":44100,"origin":"0"}, {"seconds":"1/44100","index":1}),
        ("One second roundtrip does not need floating arithmetic", {"mode":"to_seconds","index":48000,"rate":48000,"origin":"0"}, {"seconds":"1","index":48000}),
        ("A negative origin remains distinct from a negative frame index", {"mode":"to_seconds","index":2,"rate":4,"origin":"-1"}, {"seconds":"-1/2","index":2}),
        ("Fractional origin composes exactly with frame time", {"mode":"to_seconds","index":1,"rate":3,"origin":"1/6"}, {"seconds":"1/2","index":1}),
        ("An exact half-second maps to an integer index", {"mode":"to_index","seconds":"1/2","rate":48000,"origin":"0"}, {"seconds":"1/2","index":24000}),
        ("Shifted origin is subtracted before inverse mapping", {"mode":"to_index","seconds":"3/2","rate":4,"origin":"1"}, {"seconds":"3/2","index":2}),
        ("Equivalent rational spellings normalize in the view", {"mode":"to_index","seconds":"2/4","rate":4,"origin":"0/7"}, {"seconds":"1/2","index":2}),
        ("Time equal to origin maps to zero", {"mode":"to_index","seconds":"-2","rate":8,"origin":"-2"}, {"seconds":"-2","index":0}),
        ("A billion-frame index remains exact", {"mode":"to_seconds","index":1000000000,"rate":1000,"origin":"0"}, {"seconds":"1000000","index":1000000000}),
    ]:
        add(op, title, payload, accept(value))
    for title, payload, code in [
        ("Off-grid time is held instead of rounded", {"mode":"to_index","seconds":"1/3","rate":2,"origin":"0"}, "OFF_SAMPLE_GRID"),
        ("Time before origin cannot create a negative index", {"mode":"to_index","seconds":"0","rate":2,"origin":"1"}, "NEGATIVE_INDEX"),
        ("Negative source index is refused", {"mode":"to_seconds","index":-1,"rate":2,"origin":"0"}, "NEGATIVE_INDEX"),
        ("Boolean index is not integer sample evidence", {"mode":"to_seconds","index":True,"rate":2,"origin":"0"}, "INTEGER_TYPE"),
        ("Zero rate is refused", {"mode":"to_seconds","index":1,"rate":0,"origin":"0"}, "SAMPLE_RATE"),
        ("Floating origin does not receive implicit rationalization", {"mode":"to_seconds","index":1,"rate":2,"origin":0.1}, "RATIONAL_SYNTAX"),
        ("A zero denominator is refused", {"mode":"to_seconds","index":1,"rate":2,"origin":"1/0"}, "RATIONAL_SYNTAX"),
        ("Decimal text is outside the integer-fraction lexical profile", {"mode":"to_seconds","index":1,"rate":2,"origin":"0.5"}, "RATIONAL_SYNTAX"),
        ("An unknown conversion mode cannot select a fallback", {"mode":"round","index":1,"rate":2,"origin":"0"}, "MODE"),
        ("An excessively large rational field is held", {"mode":"to_seconds","index":1,"rate":2,"origin":"9"*81}, "RATIONAL_SYNTAX"),
    ]:
        add(op, title, payload, hold(code))

def range_cases():
    op = "pcm_range"
    for title, bits, signed, samples, out, rail in [
        ("Unsigned eight-bit endpoint samples are rails, not clipping proof",8,False,[0,255],[],[0,1]),
        ("Signed sixteen-bit endpoint samples retain asymmetry",16,True,[-32768,32767],[],[0,1]),
        ("Zero-valued signed samples are interior",16,True,[0,0],[],[]),
        ("Unsigned lower excursion is reported by position",8,False,[-1,0,1],[0],[1]),
        ("Unsigned upper excursion is reported by position",8,False,[254,255,256],[2],[1]),
        ("Signed excursions on both sides remain distinct",16,True,[-32769,32768],[0,1],[]),
        ("Twenty-four-bit signed bounds are exact integers",24,True,[-8388608,8388607],[],[0,1]),
        ("Thirty-two-bit signed bounds avoid float conversion",32,True,[-2147483648,2147483647],[],[0,1]),
        ("One-bit unsigned range is finite",1,False,[0,1,2],[2],[0,1]),
        ("One-bit signed range retains minus one and zero",1,True,[-1,0,1],[2],[0,1]),
        ("An empty sample array establishes no observed rail",8,False,[],[],[]),
        ("Repeated endpoint positions stay independently addressable",8,False,[255,255,0],[],[0,1,2]),
    ]:
        lo=-(1 << (bits-1)) if signed else 0; hi=(1 << (bits-1))-1 if signed else (1<<bits)-1
        add(op,title,{"bits":bits,"signed":signed,"samples":samples},accept({"lower":lo,"upper":hi,"out_of_range_indices":out,"rail_indices":rail,"clipping_established":False}))
    base={"bits":16,"signed":True,"samples":[0]}
    for title,patch,code in [
        ("Zero bit width is refused",{"bits":0},"SAMPLE_BITS"),
        ("Widths over thirty-two are outside this bounded contract",{"bits":33},"SAMPLE_BITS"),
        ("Boolean bit width is not integer one",{"bits":True},"INTEGER_TYPE"),
        ("Signedness must be a Boolean",{"signed":"true"},"SIGNED_TYPE"),
        ("Boolean sample values cannot masquerade as PCM integers",{"samples":[False]},"SAMPLE_TYPE"),
        ("Floating sample values are not silently quantized",{"samples":[0.5]},"SAMPLE_TYPE"),
        ("A scalar sample field is refused",{"samples":0},"SAMPLE_ARRAY"),
        ("The sixty-four-sample fixture ceiling is enforced",{"samples":[0]*65},"SAMPLE_ARRAY"),
    ]:add(op,title,dict(base,**patch),hold(code))

def channel_cases():
    op="channel_permutation"
    for title,ch,order,frames,outch,outframes,inverse in [
        ("Mono identity preserves each frame",["mono"],[0],[[1],[-1]],["mono"],[[1],[-1]],[0]),
        ("Stereo swap preserves sample values and reverses labels",["left","right"],[1,0],[[1,2],[3,4]],["right","left"],[[2,1],[4,3]],[1,0]),
        ("Three-channel cycle records its inverse",["a","b","c"],[2,0,1],[[10,20,30]],["c","a","b"],[[30,10,20]],[1,2,0]),
        ("An empty frame list does not invent audio",["left","right"],[1,0],[],["right","left"],[],[1,0]),
        ("Identity mapping keeps distinct channel labels",["a","b"],[0,1],[[0,0]],["a","b"],[[0,0]],[0,1]),
        ("Four-channel reversal is a bijection",["a","b","c","d"],[3,2,1,0],[[1,2,3,4]],["d","c","b","a"],[[4,3,2,1]],[3,2,1,0]),
    ]:add(op,title,{"channels":ch,"order":order,"frames":frames},accept({"channels":outch,"frames":outframes,"inverse":inverse}))
    base={"channels":["left","right"],"order":[0,1],"frames":[[1,2]]}
    for title,patch,code in [
        ("Duplicate channel labels are ambiguous",{"channels":["left","left"]},"CHANNEL_LABELS"),
        ("Empty channel lists cannot define a frame",{"channels":[]},"CHANNEL_LABELS"),
        ("Empty channel labels are refused",{"channels":["","right"]},"CHANNEL_LABELS"),
        ("Numeric channel labels are not coerced",{"channels":[0,"right"]},"CHANNEL_LABELS"),
        ("A repeated source index is not a permutation",{"order":[0,0]},"PERMUTATION"),
        ("A missing source index is not a permutation",{"order":[0]},"PERMUTATION"),
        ("An out-of-range source index is refused",{"order":[0,2]},"PERMUTATION"),
        ("A negative source index cannot use Python wraparound",{"order":[-1,0]},"PERMUTATION"),
        ("Boolean permutation members are not integer indices",{"order":[False,1]},"PERMUTATION"),
        ("Ragged frames cannot silently lose a channel",{"frames":[[1]]},"FRAME_SHAPE"),
        ("Extra frame channels are refused",{"frames":[[1,2,3]]},"FRAME_SHAPE"),
        ("Float sample values remain outside the integer fixture profile",{"frames":[[1,2.0]]},"SAMPLE_TYPE"),
        ("A null frames field is refused",{"frames":None},"FRAME_SHAPE"),
        ("More than eight declared channels exceeds the bound",{"channels":[str(i) for i in range(9)]},"CHANNEL_LABELS"),
    ]:add(op,title,dict(base,**patch),hold(code))

def edit_cases():
    op="edit_intervals"
    specs=[
        ("Full-span keep preserves source duration",10,[[0,10]],10,[],[[0,10,0,10]]),
        ("Empty keep list represents removal without changing source",10,[],0,[[0,10]],[]),
        ("Leading trim retains its discarded prefix",10,[[2,10]],8,[[0,2]],[[2,10,0,8]]),
        ("Trailing trim retains its discarded suffix",10,[[0,8]],8,[[8,10]],[[0,8,0,8]]),
        ("Interior keep retains both surrounding gaps",10,[[2,8]],6,[[0,2],[8,10]],[[2,8,0,6]]),
        ("Two separated keeps expose the middle gap",10,[[0,3],[5,10]],8,[[3,5]],[[0,3,0,3],[5,10,3,8]]),
        ("Touching half-open spans do not overlap",10,[[0,3],[3,10]],10,[],[[0,3,0,3],[3,10,3,10]]),
        ("Zero-length source with no keeps is well defined",0,[],0,[],[]),
        ("A one-frame keep remains one output frame",10,[[4,5]],1,[[0,4],[5,10]],[[4,5,0,1]]),
        ("Three keeps retain a cumulative output map",12,[[1,3],[5,7],[9,11]],6,[[0,1],[3,5],[7,9],[11,12]],[[1,3,0,2],[5,7,2,4],[9,11,4,6]]),
    ]
    for title,n,keep,total,dropped,mapping in specs:add(op,title,{"source_frames":n,"keep":keep},accept({"output_frames":total,"dropped":dropped,"mapping":mapping}))
    base={"source_frames":10,"keep":[[1,3]]}
    for title,patch,code in [
        ("Overlapping spans cannot duplicate frames implicitly",{"keep":[[0,5],[4,8]]},"SPAN_ORDER_OR_OVERLAP"),
        ("Reverse-ordered spans need an explicit reorder contract",{"keep":[[5,7],[1,3]]},"SPAN_ORDER_OR_OVERLAP"),
        ("Reversed endpoints are refused",{"keep":[[3,1]]},"SPAN_BOUNDS"),
        ("Empty spans are refused rather than counted",{"keep":[[3,3]]},"SPAN_BOUNDS"),
        ("Negative starts do not use wraparound",{"keep":[[-1,3]]},"SPAN_BOUNDS"),
        ("Past-end endpoints are refused",{"keep":[[1,11]]},"SPAN_BOUNDS"),
        ("Boolean endpoints are not frame indices",{"keep":[[False,3]]},"SPAN_TYPE"),
        ("A span must have exactly two endpoints",{"keep":[[1,2,3]]},"SPAN_TYPE"),
        ("Negative source duration is refused",{"source_frames":-1},"SOURCE_FRAMES"),
        ("Null edit lists cannot mean keep-all",{"keep":None},"SPAN_ARRAY"),
    ]:add(op,title,dict(base,**patch),hold(code))

def binding_cases():
    op="segment_binding"
    sha=lambda b:hashlib.sha256(b).hexdigest()
    source=b"abcdefgh"
    def payload(raw,start,end):return {"hex":raw.hex(),"start":start,"end":end,"source_sha256":sha(raw),"segment_sha256":sha(raw[start:end])}
    for title,raw,start,end in [
        ("Full source span binds to its source digest",source,0,8),
        ("Prefix segment is bound to literal source bytes",source,0,3),
        ("Suffix segment is bound to literal source bytes",source,5,8),
        ("Interior segment preserves half-open endpoints",source,2,5),
        ("Empty segment at source start has the empty digest",source,0,0),
        ("Empty segment at source end remains valid",source,8,8),
        ("Empty source is an explicit zero-byte binding",b"",0,0),
        ("Non-text bytes are bound without decoding",bytes([0,255,128,13]),1,4),
    ]:add(op,title,payload(raw,start,end),accept({"source_bytes":len(raw),"segment_bytes":end-start,"source_sha256":sha(raw),"segment_sha256":sha(raw[start:end])}))
    base=payload(source,1,4)
    for title,patch,code in [
        ("Wrong source digest is refused",{"source_sha256":"0"*64},"SOURCE_DIGEST_MISMATCH"),
        ("Wrong segment digest is refused",{"segment_sha256":"0"*64},"SEGMENT_DIGEST_MISMATCH"),
        ("Digest case is governed by an explicit lowercase profile",{"source_sha256":sha(source).upper()},"DIGEST_SYNTAX"),
        ("A shortened digest is not silently padded",{"segment_sha256":"ab"},"DIGEST_SYNTAX"),
        ("Nonhexadecimal digest characters are refused",{"segment_sha256":"g"*64},"DIGEST_SYNTAX"),
        ("Negative segment starts are refused",{"start":-1},"SPAN_BOUNDS"),
        ("Segment end cannot exceed source length",{"end":9},"SPAN_BOUNDS"),
        ("Reversed binding endpoints are refused",{"start":5,"end":4},"SPAN_BOUNDS"),
        ("Boolean binding endpoints are not integer indices",{"start":True},"SPAN_TYPE"),
        ("Odd-length hexadecimal is refused",{"hex":"abc"},"HEX_SYNTAX"),
        ("Whitespace in hex does not silently alter the byte domain",{"hex":"61 62"},"HEX_SYNTAX"),
        ("Extra digest algorithms need a separately declared profile",{"algorithm":"md5"},"FIELD_SET"),
    ]:add(op,title,dict(base,**patch),hold(code))

def claim_cases():
    op="restoration_claim"
    base={"source_kind":"synthetic","before":{"frames":8,"rate":8000,"channels":1},"after":{"frames":8,"rate":8000,"channels":1},"metric_before":"3","metric_after":"1","direction":"lower","independent_review":False}
    for title,a,b,direction,delta,better in [
        ("Lower synthetic error metric is only a fixture improvement","3","1","lower","-2",True),
        ("Higher error metric is retained as worsening","1","3","lower","2",False),
        ("Equal metrics do not establish improvement","2","2","lower","0",False),
        ("Higher score can be better under an explicit direction","1","2","higher","1",True),
        ("Lower score is not better under higher-is-better","2","1","higher","-1",False),
        ("Rational metric differences remain exact","2/3","1/6","lower","-1/2",True),
        ("Negative metrics retain their declared ordering","-2","-3","lower","-1",True),
        ("A zero metric remains numeric evidence in the fixture","1","0","lower","-1",True),
        ("Large integers do not require a float projection","1000000000000000000","999999999999999999","lower","-1",True),
        ("Equivalent rational metrics normalize without apparent gain","2/4","1/2","higher","0",False),
    ]:add(op,title,dict(base,metric_before=a,metric_after=b,direction=direction),accept({"metric_delta":delta,"better_in_fixture":better,"perceptual_effectiveness_established":False,"independent_reproduction":False}),"represented")
    for title,patch,code,disposition in [
        ("Missing before metric remains an evidence gap",{"metric_before":None},"MISSING_METRIC","open_gap"),
        ("Missing after metric remains an evidence gap",{"metric_after":None},"MISSING_METRIC","open_gap"),
        ("Different rates require a registered comparison mapping",{"after":{"frames":8,"rate":16000,"channels":1}},"NOT_COMPARABLE","open_gap"),
        ("Different frame counts require a registered comparison mapping",{"after":{"frames":7,"rate":8000,"channels":1}},"NOT_COMPARABLE","open_gap"),
        ("Different channel counts require a registered comparison mapping",{"after":{"frames":8,"rate":8000,"channels":2}},"NOT_COMPARABLE","open_gap"),
        ("A declared independent review is not verified by local fields",{"independent_review":True},"EXTERNAL_REVIEW_REQUIRED","exact_gate"),
        ("Real audio remains outside synthetic fixture authority",{"source_kind":"real"},"REAL_AUDIO_AUTHORITY_REQUIRED","exact_gate"),
        ("An unspecified metric direction is held",{"direction":"automatic"},"DIRECTION","open_gap"),
        ("Floating metric fields are not implicitly rationalized",{"metric_after":0.1},"RATIONAL_SYNTAX","open_gap"),
        ("Invalid metric denominator is refused",{"metric_after":"1/0"},"RATIONAL_SYNTAX","open_gap"),
    ]:add(op,title,dict(base,**patch),hold(code),disposition)

DISCLOSURE_REQUIREMENTS={
    "publish_audio":["rights_holder","affected_people","privacy_review"],
    "publish_transcript":["rights_holder","speaker_consent","privacy_review"],
    "identify_speaker":["affected_people","competent_identity_review"],
    "determine_rights":["competent_legal_authority","rights_holder"],
    "assign_maori_label":["maori_authority","affected_people"],
    "release_maori_data":["maori_data_governance","tangata_whenua_iwi_hapu"],
    "assert_tikanga":["maori_authority"],
    "assert_taonga_status":["maori_authority"],
    "claim_restoration_quality":["preregistered_listener_evidence","independent_review"],
    "claim_accessibility_complete":["affected_user_evaluation","assistive_technology_review"],
    "deploy_identity_service":["production_keys_proofs","security_review","trust_governance"],
    "delete_source":["exact_destructive_authority","recoverable_backup"],
    "change_shared_archive":["archive_custodian","exact_shared_target"],
    "use_real_participants":["governed_consent","safety_monitoring","competent_review"],
    "claim_gmut_confirmation":["empirical_model_comparison","independent_review"],
    "promote_stage20":["all_exact_external_gates","competent_affected_authority"],
}

def disclosure_cases():
    op="disclosure_gate"
    for action,title in [("inspect_synthetic","Inspecting synthetic metadata grants no rights"),("plan_redaction","A redaction plan does not alter a real recording"),("draft_access_summary","A draft access summary remains unevaluated"),("retain_private_source","Retention representation does not verify custody")]:
        add(op,title,{"action":action,"source_kind":"synthetic","claimed_permissions":[]},accept({"action":action,"disposition":"represented","executed_external_action":False,"required_authorities":[]}),"represented")
    for action,required in DISCLOSURE_REQUIREMENTS.items():
        add(op,"Reserve "+action.replace("_"," ")+" to its exact evidence and authority",{"action":action,"source_kind":"synthetic","claimed_permissions":required},accept({"action":action,"disposition":"exact_gate","executed_external_action":False,"required_authorities":required}),"exact_gate")

def build_cases():
    CASES.clear()
    for build in [riff_cases,format_cases,frame_cases,time_cases,range_cases,channel_cases,edit_cases,binding_cases,claim_cases,disclosure_cases]:build()
    counts=Counter(c['operation'] for c in CASES)
    assert len(CASES)==200 and set(counts.values())=={20}, counts
    assert len({json.dumps(c['input'],sort_keys=True) for c in CASES})==200
    return copy.deepcopy(CASES)

if __name__ == '__main__':
    cases=build_cases()
    print(json.dumps({'planning_only':True,'proposals':len(cases),'operations':dict(Counter(c['operation'] for c in cases))}))

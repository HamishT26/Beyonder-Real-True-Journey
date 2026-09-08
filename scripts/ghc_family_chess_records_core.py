#!/usr/bin/env python3
"""Bounded synthetic chess-record evaluator for Sylven Arc v688-v7."""
from __future__ import annotations
import copy,hashlib,json,re
from typing import Any

BOUNDARY=("Same-owner synthetic chess-record software evidence only; no real game, participant, rating, "
"tournament, professional, legal, cultural, Maori-authority, independent-reproduction, consciousness, "
"Theory-of-Everything, or Stage 20 evidence.")
FIELDS={
 "square_parse":{"operation","square"},"square_name":{"operation","index"},
 "fen_board":{"operation","board"},"fen_record":{"operation","fen"},
 "fen_castling":{"operation","rights"},"fen_en_passant":{"operation","square"},
 "uci_move":{"operation","move"},"uci_sequence":{"operation","moves"},
 "san_token":{"operation","token"},"pgn_tag":{"operation","line"},
 "pgn_headers":{"operation","headers"},"pgn_movetext":{"operation","tokens"},
 "position_graph":{"operation","nodes","edges"},"move_tree":{"operation","nodes","edges"},
 "board_material":{"operation","counts"},"halfmove_timeline":{"operation","start","events"},
 "chess_record_fixity":{"operation","text"},
 "chess_record_provenance":{"operation","source_label","source_digest","rights_state","review_state","observed"},
 "accessible_move":{"operation","move","locale","review_state"},
 "chess_authority_reservation":{"operation","action"},
}
ACTIONS={"tournament_ruling","rating_assignment","competition_result_certification","engine_deployment",
 "participant_research","legal_ownership","cultural_interpretation","maori_wording","privacy_complete","stage20"}
class ProfileError(ValueError):
    def __init__(self,code):self.code=code;super().__init__(code)
def integer(value,code):
    if isinstance(value,bool) or not isinstance(value,int):raise ProfileError(code)
    return value
def square(name):
    if not isinstance(name,str) or not re.fullmatch(r"[a-h][1-8]",name):raise ProfileError("square")
    return {"file":ord(name[0])-97,"rank":int(name[1]),"index":(int(name[1])-1)*8+ord(name[0])-97}
def square_from_index(index):
    integer(index,"square_index")
    if not 0<=index<64:raise ProfileError("square_index")
    return chr(97+index%8)+str(index//8+1)
def board(field):
    if not isinstance(field,str):raise ProfileError("fen_board")
    ranks=field.split("/")
    if len(ranks)!=8:raise ProfileError("fen_board")
    counts={};occupied=0
    for rank in ranks:
        width=0
        for ch in rank:
            if ch in "12345678":width+=int(ch)
            elif ch in "prnbqkPRNBQK":
                width+=1;occupied+=1;counts[ch]=counts.get(ch,0)+1
            else:raise ProfileError("fen_board")
        if width!=8:raise ProfileError("fen_board")
    return {"occupied":occupied,"pieces":dict(sorted(counts.items()))}
def castling(rights):
    if not isinstance(rights,str):raise ProfileError("castling")
    if rights=="-":return []
    if not rights or any(c not in "KQkq" for c in rights) or len(rights)!=len(set(rights)):
        raise ProfileError("castling")
    if rights!="".join(c for c in "KQkq" if c in rights):raise ProfileError("castling")
    return list(rights)
def en_passant(name):
    if name=="-":return {"square":None}
    if not isinstance(name,str) or not re.fullmatch(r"[a-h][36]",name):raise ProfileError("en_passant")
    return {"square":name}
def fen_record(text):
    if not isinstance(text,str):raise ProfileError("fen_fields")
    fields=text.split()
    if len(fields)!=6:raise ProfileError("fen_fields")
    placement,turn,rights,ep,half,full=fields
    board(placement)
    if turn not in {"w","b"}:raise ProfileError("fen_turn")
    castling(rights);en_passant(ep)
    try:half_i=int(half);full_i=int(full)
    except ValueError:raise ProfileError("fen_counter")
    if str(half_i)!=half or str(full_i)!=full or half_i<0 or full_i<1:raise ProfileError("fen_counter")
    return {"board":placement,"turn":turn,"castling":rights,"en_passant":ep,"halfmove":half_i,"fullmove":full_i}
def uci(move):
    if move=="0000":return {"null":True}
    if not isinstance(move,str) or not re.fullmatch(r"[a-h][1-8][a-h][1-8][qrbn]?",move):raise ProfileError("uci")
    return {"from":move[:2],"to":move[2:4],"promotion":move[4] if len(move)==5 else None,"null":False}
def uci_sequence(moves):
    if not isinstance(moves,list):raise ProfileError("uci_sequence")
    for move in moves:uci(move)
    if len(moves)>512:raise ProfileError("uci_sequence")
    return {"count":len(moves),"moves":copy.deepcopy(moves)}
def san_token(token):
    if not isinstance(token,str):raise ProfileError("san")
    pattern=r"(?:O-O(?:-O)?|(?:[KQRBN]?[a-h]?[1-8]?x?[a-h][1-8]|[a-h]x?[a-h][1-8])(?:=[QRBN])?)[+#]?"
    if not re.fullmatch(pattern,token):raise ProfileError("san")
    return {"token":token,"castle":token.startswith("O-O"),"check":token.endswith("+"),"mate":token.endswith("#")}
def pgn_tag(line):
    if not isinstance(line,str):raise ProfileError("pgn_tag")
    match=re.fullmatch(r'\[([A-Za-z0-9_]+) "([^"\\]*)"\]',line)
    if not match:raise ProfileError("pgn_tag")
    return {"key":match.group(1),"value":match.group(2)}
def pgn_headers(headers):
    if not isinstance(headers,list):raise ProfileError("pgn_header")
    names=set();result=[]
    for pair in headers:
        if not isinstance(pair,list) or len(pair)!=2 or not all(isinstance(x,str) for x in pair):
            raise ProfileError("pgn_header")
        if pair[0] in names:raise ProfileError("pgn_header_duplicate")
        names.add(pair[0]);result.append(copy.deepcopy(pair))
    return {"count":len(result),"headers":result}
def pgn_movetext(tokens):
    if not isinstance(tokens,list) or not all(isinstance(t,str) for t in tokens):raise ProfileError("pgn_tokens")
    results={"1-0","0-1","1/2-1/2","*"}
    if not tokens or tokens[-1] not in results or any(t in results for t in tokens[:-1]):raise ProfileError("pgn_result")
    moves=[t for t in tokens[:-1] if not re.fullmatch(r"\d+\.(?:\.\.)?",t)]
    return {"moves":moves,"result":tokens[-1]}
def position_graph(nodes,edges):
    if not isinstance(nodes,list) or not isinstance(edges,list) or not all(isinstance(n,str) for n in nodes):
        raise ProfileError("graph")
    if len(nodes)!=len(set(nodes)):raise ProfileError("graph")
    adj={n:set() for n in nodes}
    for edge in edges:
        if not isinstance(edge,list) or len(edge)!=2 or edge[0] not in adj or edge[1] not in adj or edge[0]==edge[1]:
            raise ProfileError("graph")
        adj[edge[0]].add(edge[1]);adj[edge[1]].add(edge[0])
    components=[];seen=set()
    for start in sorted(nodes):
        if start in seen:continue
        stack=[start];seen.add(start);component=[]
        while stack:
            node=stack.pop();component.append(node)
            for other in sorted(adj[node],reverse=True):
                if other not in seen:seen.add(other);stack.append(other)
        components.append(sorted(component))
    return {"components":components,"degrees":{n:len(adj[n]) for n in sorted(nodes)}}
def move_tree(nodes,edges):
    if not isinstance(nodes,list) or not isinstance(edges,list) or not all(isinstance(n,str) for n in nodes):
        raise ProfileError("move_tree")
    if len(nodes)!=len(set(nodes)):raise ProfileError("move_tree")
    children={n:[] for n in nodes};indegree={n:0 for n in nodes}
    for edge in edges:
        if not isinstance(edge,list) or len(edge)!=2 or edge[0] not in children or edge[1] not in children or edge[0]==edge[1]:
            raise ProfileError("move_tree")
        children[edge[0]].append(edge[1]);indegree[edge[1]]+=1
    if any(v>1 for v in indegree.values()):raise ProfileError("move_tree")
    roots=sorted(n for n,v in indegree.items() if v==0);queue=list(roots);order=[]
    while queue:
        node=queue.pop(0);order.append(node)
        for child in sorted(children[node]):
            indegree[child]-=1
            if indegree[child]==0:queue.append(child)
    if len(order)!=len(nodes):raise ProfileError("move_tree")
    return {"roots":roots,"leaves":sorted(n for n in nodes if not children[n]),"topological":order}
def board_material(counts):
    if not isinstance(counts,dict):raise ProfileError("material")
    values={"P":1,"N":3,"B":3,"R":5,"Q":9,"K":0};white=black=0
    for symbol,count in counts.items():
        if symbol not in "PNBRQKpnbrqk" or isinstance(count,bool) or not isinstance(count,int) or count<0:
            raise ProfileError("material")
        amount=values[symbol.upper()]*count
        if symbol.isupper():white+=amount
        else:black+=amount
    return {"white":white,"black":black,"balance":white-black}
def halfmove(start,events):
    integer(start,"halfmove")
    if start<0 or not isinstance(events,list):raise ProfileError("halfmove")
    result=[];clock=start
    for event in events:
        if event=="quiet":clock+=1
        elif event in {"pawn","capture"}:clock=0
        else:raise ProfileError("halfmove_event")
        result.append(clock)
    return result
def record_fixity(text):
    if not isinstance(text,str):raise ProfileError("text_type")
    raw=text.encode("utf-8");lf=raw.replace(b"\r\n",b"\n")
    return {"raw_bytes":len(raw),"raw_sha256":hashlib.sha256(raw).hexdigest(),
      "lf_sha256":hashlib.sha256(lf).hexdigest(),"normalization":"CRLF_to_LF_only",
      "authenticity_established":False}
def provenance(data):
    if data["observed"] is not False:raise ProfileError("synthetic_only")
    if data["rights_state"] not in {"unknown","declared"}:raise ProfileError("rights_state")
    if data["review_state"] not in {"absent","declared"}:raise ProfileError("review_state")
    label=data["source_label"];source_digest=data["source_digest"]
    if not isinstance(label,str) or not isinstance(source_digest,str):raise ProfileError("source")
    if source_digest and not re.fullmatch(r"[0-9a-f]{64}",source_digest):raise ProfileError("digest")
    missing=[key for key,value in (("source_label",label),("source_digest",source_digest)) if not value]
    if missing:return {"missing":missing,"publication_authorized":False}
    return {"source_label":label,"rights_state":data["rights_state"],"review_state":data["review_state"],
      "observation":"synthetic","publication_authorized":False}
def accessible(move,locale,review_state):
    if locale!="en" or review_state not in {"synthetic","reserved"}:raise ProfileError("accessibility_profile")
    parsed=uci(move)
    if parsed["null"]:text="null move marker"
    else:
        start=square(move[:2]);end=square(move[2:4])
        text=f"move from {move[:2]} file {start['file']+1} rank {start['rank']} to {move[2:4]} file {end['file']+1} rank {end['rank']}"
        if len(move)==5:text+=f" promote to {move[4]}"
    return {"text":text,"human_evaluation":False}
def authority(action):
    if action not in ACTIONS:raise ProfileError("authority_action")
    return {"action":action,"executed":False,
      "required":"exact target, competent authority, evidence scope, affected-party review, and rollback"}
def disposition(operation,data):
    if operation=="chess_record_fixity":return "represented"
    if operation=="chess_record_provenance":
        return "open_gap" if not data["source_label"] or not data["source_digest"] else "completed"
    if operation=="accessible_move":return "represented" if data["review_state"]=="reserved" else "completed"
    if operation=="chess_authority_reservation":return "exact_gate"
    return "completed"
def evaluate(data:dict[str,Any])->dict[str,Any]:
    if not isinstance(data,dict) or not isinstance(data.get("operation"),str):
        return {"accepted":False,"error":"field_set","value":None,"disposition":"completed","boundary":BOUNDARY}
    operation=data["operation"]
    if operation not in FIELDS or set(data)!=FIELDS[operation]:
        return {"accepted":False,"error":"field_set","value":None,
          "disposition":disposition(operation,data) if operation in FIELDS and FIELDS[operation]-set(data)==set() else "completed",
          "boundary":BOUNDARY}
    try:
        value={
          "square_parse":lambda:square(data["square"]),
          "square_name":lambda:square_from_index(data["index"]),
          "fen_board":lambda:board(data["board"]),
          "fen_record":lambda:fen_record(data["fen"]),
          "fen_castling":lambda:castling(data["rights"]),
          "fen_en_passant":lambda:en_passant(data["square"]),
          "uci_move":lambda:uci(data["move"]),
          "uci_sequence":lambda:uci_sequence(data["moves"]),
          "san_token":lambda:san_token(data["token"]),
          "pgn_tag":lambda:pgn_tag(data["line"]),
          "pgn_headers":lambda:pgn_headers(data["headers"]),
          "pgn_movetext":lambda:pgn_movetext(data["tokens"]),
          "position_graph":lambda:position_graph(data["nodes"],data["edges"]),
          "move_tree":lambda:move_tree(data["nodes"],data["edges"]),
          "board_material":lambda:board_material(data["counts"]),
          "halfmove_timeline":lambda:halfmove(data["start"],data["events"]),
          "chess_record_fixity":lambda:record_fixity(data["text"]),
          "chess_record_provenance":lambda:provenance(data),
          "accessible_move":lambda:accessible(data["move"],data["locale"],data["review_state"]),
          "chess_authority_reservation":lambda:authority(data["action"]),
        }[operation]()
        return {"accepted":True,"error":None,"value":copy.deepcopy(value),
          "disposition":disposition(operation,data),"boundary":BOUNDARY}
    except ProfileError as exc:
        return {"accepted":False,"error":exc.code,"value":None,
          "disposition":disposition(operation,data),"boundary":BOUNDARY}
def expected_envelope(proposal):
    return {"accepted":proposal["expected_acceptance"],"error":proposal["expected_error"],
      "value":copy.deepcopy(proposal["expected_value"]),
      "disposition":proposal["expected_execution_disposition"],"boundary":BOUNDARY}
def matches_contract(proposal,result):
    return result==expected_envelope(proposal)


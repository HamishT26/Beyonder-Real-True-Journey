#!/usr/bin/env python3
"""Build the planning-only Sylven Arc v688-v7 chess-record preservation packet."""
from pathlib import Path
import argparse, datetime, hashlib, json, re, subprocess, urllib.request

OWNER="Sylven Arc"; PHASE="v688-v7"
SOURCE="e7db6f3be1327de72f93873eb6540aabfc773344"
PREFIX="SA6887"; BASE="docs/sylven-arc/v688-v7"
BOUNDARY=("Relational working language only. No consciousness, sentience, personhood, legal identity, "
"identity continuity, employment, qualification, independent agency, scientific, operational, professional, "
"legal, cultural, affected-party, or Maori authority is established. Same-owner synthetic evidence is not "
"independent reproduction. NOT_READY_FOR_STAGE_20. Maori concepts remain under Maori authority.")
GATES=["empirical","participant","professional","production","deployment","legal","cultural",
"maori_authority","privacy_complete","accessibility_complete","exhaustive_security",
"independent_reproduction","agi_asi","consciousness_personhood","theory_of_everything","stage20"]
PRACTICES=["synthetic chess-notation registrar","board-state topology analyst",
"game-record provenance steward","accessible move-list editor"]
SKILLS=["chess-square-coordinate","chess-fen-structure","chess-castling-en-passant",
"chess-uci-sequence","chess-san-pgn-tag","chess-pgn-header-movetext",
"chess-position-move-graph","chess-material-timeline","chess-record-fixity-provenance",
"chess-accessibility-authority"]
RUNNERS=["ghc_family_chess_position_records.py","ghc_family_chess_move_notation.py",
"ghc_family_chess_pgn_records.py","ghc_family_chess_graph_analysis.py",
"ghc_family_chess_evidence.py"]

def serial(x): return json.dumps(x,ensure_ascii=True,sort_keys=True,separators=(",",":")).encode()
def digest(x): return hashlib.sha256(x).hexdigest()
def case(title,payload,value=None,error=None,expected="completed"):
    return {"title":title,"payload":payload,"value":value,"error":error,"expected":expected}
def square_value(name):
    return {"file":ord(name[0])-97,"rank":int(name[1]),"index":(int(name[1])-1)*8+ord(name[0])-97}
def board_value(field):
    counts={}; occupied=0
    ranks=field.split("/")
    if len(ranks)!=8: raise ValueError("fen_board")
    for rank in ranks:
        width=0
        for ch in rank:
            if ch in "12345678": width+=int(ch)
            elif ch in "prnbqkPRNBQK":
                width+=1; occupied+=1; counts[ch]=counts.get(ch,0)+1
            else: raise ValueError("fen_board")
        if width!=8: raise ValueError("fen_board")
    return {"occupied":occupied,"pieces":dict(sorted(counts.items()))}
def graph_value(nodes,edges):
    if len(nodes)!=len(set(nodes)) or any(len(e)!=2 or e[0] not in nodes or e[1] not in nodes or e[0]==e[1] for e in edges):
        raise ValueError("graph")
    adj={n:set() for n in nodes}
    for a,b in edges: adj[a].add(b);adj[b].add(a)
    components=[];seen=set()
    for start in sorted(nodes):
        if start in seen: continue
        stack=[start];component=[];seen.add(start)
        while stack:
            n=stack.pop();component.append(n)
            for other in sorted(adj[n],reverse=True):
                if other not in seen:seen.add(other);stack.append(other)
        components.append(sorted(component))
    return {"components":components,"degrees":{n:len(adj[n]) for n in sorted(nodes)}}
def tree_value(nodes,edges):
    if len(nodes)!=len(set(nodes)) or any(len(e)!=2 or e[0] not in nodes or e[1] not in nodes or e[0]==e[1] for e in edges):
        raise ValueError("move_tree")
    children={n:[] for n in nodes};indegree={n:0 for n in nodes}
    for a,b in edges:
        children[a].append(b);indegree[b]+=1
    if any(v>1 for v in indegree.values()):raise ValueError("move_tree")
    roots=sorted(n for n,v in indegree.items() if v==0)
    queue=list(roots);order=[]
    while queue:
        n=queue.pop(0);order.append(n)
        for child in sorted(children[n]):
            indegree[child]-=1
            if indegree[child]==0:queue.append(child)
    if len(order)!=len(nodes):raise ValueError("move_tree")
    return {"roots":roots,"leaves":sorted(n for n in nodes if not children[n]),"topological":order}
def material_value(counts):
    values={"P":1,"N":3,"B":3,"R":5,"Q":9,"K":0}
    white=black=0
    for symbol,count in counts.items():
        if symbol not in "PNBRQKpnbrqk" or isinstance(count,bool) or not isinstance(count,int) or count<0:
            raise ValueError("material")
        target=values[symbol.upper()]*count
        if symbol.isupper():white+=target
        else:black+=target
    return {"white":white,"black":black,"balance":white-black}
def timeline_value(start,events):
    if isinstance(start,bool) or not isinstance(start,int) or start<0:raise ValueError("halfmove")
    out=[];clock=start
    for event in events:
        if event=="quiet":clock+=1
        elif event in {"pawn","capture"}:clock=0
        else:raise ValueError("halfmove_event")
        out.append(clock)
    return out
def fixity_value(text):
    raw=text.encode("utf-8");lf=raw.replace(b"\r\n",b"\n")
    return {"raw_bytes":len(raw),"raw_sha256":digest(raw),"lf_sha256":digest(lf),
            "normalization":"CRLF_to_LF_only","authenticity_established":False}
def accessible_value(move):
    if move=="0000":return {"text":"null move marker","human_evaluation":False}
    parsed=square_value(move[:2]);dest=square_value(move[2:4])
    text=f"move from {move[:2]} file {parsed['file']+1} rank {parsed['rank']} to {move[2:4]} file {dest['file']+1} rank {dest['rank']}"
    if len(move)==5:text+=f" promote to {move[4]}"
    return {"text":text,"human_evaluation":False}

def fixture_groups():
    groups=[]
    valid_squares=["a1","h1","a8","h8","d4","e5","b7","g2"]
    sq_cases=[case(f"Chess square {s} preserves its zero-based file and rank coordinate",{"square":s},square_value(s)) for s in valid_squares]
    sq_cases += [case("Chess square syntax refuses a file beyond h",{"square":"i4"},error="square"),
                 case("Chess square syntax refuses rank zero",{"square":"a0"},error="square")]
    groups.append(("square_parse",0,1,sq_cases))
    indices=[0,7,56,63,27,36,49,14]
    name_cases=[case(f"Chess square index {i} renders its algebraic coordinate",{"index":i},chr(97+i%8)+str(i//8+1)) for i in indices]
    name_cases += [case("Chess square naming refuses a negative index",{"index":-1},error="square_index"),
                   case("Chess square naming refuses index sixty-four",{"index":64},error="square_index")]
    groups.append(("square_name",0,1,name_cases))
    boards=[
      ("empty board field","8/8/8/8/8/8/8/8"),("standard opening board field","rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"),
      ("two-king sparse board field","8/8/8/3k4/4K3/8/8/8"),("opposed queens board field","Q7/8/8/8/8/8/8/7q"),
      ("central-file kings board field","4k3/8/8/8/8/8/8/4K3"),("four-rook corner board field","r6r/8/8/8/8/8/8/R6R"),
      ("minor-piece and pawn board field","2bqkbn1/pppppppp/8/8/8/8/PPPPPPPP/2BQKBN1")]
    board_cases=[case(f"FEN placement preserves the {label}",{"board":b},board_value(b)) for label,b in boards]
    board_cases += [case("FEN placement refuses seven ranks",{"board":"8/8/8/8/8/8/8"},error="fen_board"),
                    case("FEN placement refuses rank width nine",{"board":"9/8/8/8/8/8/8/8"},error="fen_board"),
                    case("FEN placement refuses an unknown piece symbol",{"board":"x7/8/8/8/8/8/8/8"},error="fen_board")]
    groups.append(("fen_board",1,0,board_cases))
    fens=[
      "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
      "8/8/8/3k4/4K3/8/8/8 b - - 4 45","8/8/8/8/8/8/8/8 w - - 0 1",
      "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 2 9","8/8/8/3pP3/8/8/8/8 w - d6 0 8",
      "8/8/8/8/8/8/8/8 b - - 99 120","8/8/8/8/8/8/8/8 w - a3 7 2"]
    fen_cases=[]
    for i,f in enumerate(fens):
        b,t,c,e,h,m=f.split()
        fen_cases.append(case(f"FEN six-field record case {i+1} keeps every declared field",{"fen":f},
          {"board":b,"turn":t,"castling":c,"en_passant":e,"halfmove":int(h),"fullmove":int(m)}))
    fen_cases += [case("FEN record refuses a missing fullmove field",{"fen":"8/8/8/8/8/8/8/8 w - - 0"},error="fen_fields"),
                  case("FEN record refuses an unknown active-color token",{"fen":"8/8/8/8/8/8/8/8 x - - 0 1"},error="fen_turn"),
                  case("FEN record refuses fullmove number zero",{"fen":"8/8/8/8/8/8/8/8 w - - 0 0"},error="fen_counter")]
    groups.append(("fen_record",1,0,fen_cases))
    rights=["KQkq","-","KQ","kq","Kq","Qk","K"]
    castling=[case(f"Castling-rights token {r} keeps canonical distinct flags",{"rights":r},[] if r=="-" else list(r)) for r in rights]
    castling += [case("Castling-rights syntax refuses duplicate flags",{"rights":"KK"},error="castling"),
                 case("Castling-rights syntax refuses an unknown flag",{"rights":"Kx"},error="castling"),
                 case("Castling-rights syntax refuses noncanonical order",{"rights":"qK"},error="castling")]
    groups.append(("fen_castling",1,0,castling))
    eps=["-","a3","h3","a6","h6","d3","e6"]
    epcases=[case(f"FEN en-passant token {s} preserves its declared vacancy",{"square":s},{"square":None if s=="-" else s}) for s in eps]
    epcases += [case("FEN en-passant refuses rank four",{"square":"a4"},error="en_passant"),
                case("FEN en-passant refuses an unknown file",{"square":"z3"},error="en_passant"),
                case("FEN en-passant refuses rank zero",{"square":"e0"},error="en_passant")]
    groups.append(("fen_en_passant",1,0,epcases))
    moves=["e2e4","g1f3","e7e8q","a7a8n","h2h1r","a1h8","0000"]
    move_cases=[]
    for move in moves:
        value={"null":True} if move=="0000" else {"from":move[:2],"to":move[2:4],"promotion":move[4] if len(move)==5 else None,"null":False}
        move_cases.append(case(f"UCI move token {move} preserves explicit coordinate fields",{"move":move},value))
    move_cases += [case("UCI move syntax refuses rank nine",{"move":"e9e4"},error="uci"),
                   case("UCI move syntax refuses a truncated destination",{"move":"e2e"},error="uci"),
                   case("UCI move syntax refuses an unknown promotion symbol",{"move":"e7e8x"},error="uci")]
    groups.append(("uci_move",1,0,move_cases))
    seqs=[[],["e2e4"],["e2e4","e7e5"],["g1f3","b8c6"],["e7e8q"],["0000"],["e2e4","e7e5","g1f3","b8c6"]]
    seq_cases=[case(f"UCI sequence case {i+1} preserves order without executing a game",{"moves":m},{"count":len(m),"moves":m}) for i,m in enumerate(seqs)]
    seq_cases += [case("UCI sequence refuses a malformed member",{"moves":["e2e4","bad"]},error="uci"),
                  case("UCI sequence refuses a scalar container",{"moves":"e2e4"},error="uci_sequence"),
                  case("UCI sequence refuses an unknown promotion member",{"moves":["a7a8x"]},error="uci")]
    groups.append(("uci_sequence",1,0,seq_cases))
    sans=["e4","Nf3","O-O","O-O-O","exd5","e8=Q","Qh5+","Qxf7#"]
    san_cases=[case(f"SAN lexical token {s} preserves castle and suffix indicators",{"token":s},
      {"token":s,"castle":s.startswith("O-O"),"check":s.endswith("+"),"mate":s.endswith("#")}) for s in sans]
    san_cases += [case("SAN lexical profile refuses an explicit pawn letter",{"token":"Pxe4"},error="san"),
                  case("SAN lexical profile refuses rank nine",{"token":"e9"},error="san")]
    groups.append(("san_token",1,0,san_cases))
    tag_pairs=[("Event","Synthetic"),("Site","?"),("Date","????.??.??"),("Round","1"),("White","A"),("Black","B"),("Result","*")]
    tag_cases=[case(f"PGN tag {k} preserves its quoted synthetic value",{"line":f'[{k} "{v}"]'},{"key":k,"value":v}) for k,v in tag_pairs]
    tag_cases += [case("PGN tag parser refuses a missing opening bracket",{"line":'Event "Synthetic"]'},error="pgn_tag"),
                  case("PGN tag parser refuses whitespace inside a tag name",{"line":'[Bad Key "x"]'},error="pgn_tag"),
                  case("PGN tag parser refuses an unterminated quoted value",{"line":'[Event "x]'},error="pgn_tag")]
    groups.append(("pgn_tag",1,0,tag_cases))
    header_sets=[[],[["Event","Synthetic"]],[["Result","*"]],[["White","A"],["Black","B"]],
      [["Event","Synthetic"],["Site","?"],["Result","*"]],[["Date","????.??.??"],["Round","1"]],
      [["Event","Synthetic"],["Site","?"],["Date","????.??.??"],["Round","1"],["White","A"],["Black","B"],["Result","*"]]]
    head_cases=[case(f"PGN header set case {i+1} preserves declared order and uniqueness",{"headers":h},{"count":len(h),"headers":h}) for i,h in enumerate(header_sets)]
    head_cases += [case("PGN headers refuse a duplicate tag name",{"headers":[["Event","A"],["Event","B"]]},error="pgn_header_duplicate"),
                   case("PGN headers refuse a malformed pair",{"headers":[["Event"]]},error="pgn_header"),
                   case("PGN headers refuse a nontext value",{"headers":[["Round",1]]},error="pgn_header")]
    groups.append(("pgn_headers",2,2,head_cases))
    token_sets=[["*"],["1.","e4","*"],["1.","e4","e5","*"],["1.","Nf3","d5","2.","g3","*"],
      ["1.","e4","e5","2.","Nf3","Nc6","1-0"],["1...","c5","*"],["1.","e8=Q","+","*"]]
    movecases=[]
    for i,tokens in enumerate(token_sets):
        result=tokens[-1];moves=[t for t in tokens[:-1] if not re.fullmatch(r"\d+\.(?:\.\.)?",t)]
        movecases.append(case(f"PGN movetext token stream case {i+1} separates numbering and result",{"tokens":tokens},{"moves":moves,"result":result}))
    movecases += [case("PGN movetext refuses a stream without result",{"tokens":["1.","e4"]},error="pgn_result"),
                  case("PGN movetext refuses a result before trailing moves",{"tokens":["1-0","e4"]},error="pgn_result"),
                  case("PGN movetext refuses a scalar token stream",{"tokens":"1. e4 *"},error="pgn_tokens")]
    groups.append(("pgn_movetext",2,2,movecases))
    graph_inputs=[(["a"],[]),(["a","b"],[["a","b"]]),(["a","b","c"],[["a","b"],["b","c"]]),
      (["a","b","c"],[["a","b"]]),(["a","b","c","d"],[["a","b"],["c","d"]]),
      (["a","b","c"],[["a","b"],["a","c"],["b","c"]]),([],[])]
    graph_cases=[case(f"Chess position graph case {i+1} preserves components and degrees",{"nodes":n,"edges":e},graph_value(n,e)) for i,(n,e) in enumerate(graph_inputs)]
    graph_cases += [case("Chess position graph refuses an unknown endpoint",{"nodes":["a"],"edges":[["a","b"]]},error="graph"),
                    case("Chess position graph refuses a self loop",{"nodes":["a"],"edges":[["a","a"]]},error="graph"),
                    case("Chess position graph refuses duplicate node labels",{"nodes":["a","a"],"edges":[]},error="graph")]
    groups.append(("position_graph",0,1,graph_cases))
    tree_inputs=[(["r"],[]),(["r","a"],[["r","a"]]),(["r","a","b"],[["r","a"],["a","b"]]),
      (["r","a","b"],[["r","a"],["r","b"]]),(["r","a","b","c"],[["r","a"],["a","b"],["a","c"]]),
      ([],[]),(["r","a","b","c"],[["r","a"],["r","b"],["b","c"]])]
    tree_cases=[case(f"PGN move tree case {i+1} preserves roots leaves and topological order",{"nodes":n,"edges":e},tree_value(n,e)) for i,(n,e) in enumerate(tree_inputs)]
    tree_cases += [case("PGN move tree refuses a directed cycle",{"nodes":["a","b"],"edges":[["a","b"],["b","a"]]},error="move_tree"),
                   case("PGN move tree refuses an unknown child",{"nodes":["a"],"edges":[["a","b"]]},error="move_tree"),
                   case("PGN move tree refuses a node with two parents",{"nodes":["a","b","c"],"edges":[["a","c"],["b","c"]]},error="move_tree")]
    groups.append(("move_tree",0,1,tree_cases))
    counts_list=[{},{"P":1},{"p":1},{"Q":1,"q":1},{"P":8,"p":8},{"N":2,"B":2,"R":2,"Q":1},{"n":2,"b":2,"r":2,"q":1},{"K":1,"k":1}]
    mat_cases=[case(f"Chess material ledger case {i+1} preserves signed piece-value balance",{"counts":c},material_value(c)) for i,c in enumerate(counts_list)]
    mat_cases += [case("Chess material ledger refuses a negative count",{"counts":{"P":-1}},error="material"),
                  case("Chess material ledger refuses Boolean counts",{"counts":{"P":True}},error="material")]
    groups.append(("board_material",0,1,mat_cases))
    timelines=[(0,[]),(0,["quiet"]),(0,["pawn"]),(4,["capture"]),(2,["quiet","quiet"]),(5,["quiet","pawn","quiet"]),(0,["quiet","capture","quiet"]),(99,["quiet"])]
    time_cases=[case(f"Halfmove timeline case {i+1} preserves resets and quiet increments",{"start":s,"events":e},timeline_value(s,e)) for i,(s,e) in enumerate(timelines)]
    time_cases += [case("Halfmove timeline refuses an unknown event",{"start":0,"events":["castle"]},error="halfmove_event"),
                   case("Halfmove timeline refuses a negative initial clock",{"start":-1,"events":[]},error="halfmove")]
    groups.append(("halfmove_timeline",0,1,time_cases))
    texts=["","*","1. e4 *","1. e4 e5 *","[Event \"Synthetic\"]\n\n*","\r\n","O-O","e2e4","8/8/8/8/8/8/8/8 w - - 0 1","line one\r\nline two\r\n"]
    fix_cases=[case(f"Chess record fixity case {i+1} keeps raw and LF-normalized byte domains separate",{"text":t},fixity_value(t),expected="represented") for i,t in enumerate(texts)]
    groups.append(("chess_record_fixity",2,2,fix_cases))
    prov_cases=[]
    complete=[("synthetic-a","a"*64,"unknown","absent"),("synthetic-b","b"*64,"declared","absent"),
      ("synthetic-c","c"*64,"unknown","declared"),("synthetic-d","d"*64,"declared","declared"),
      ("synthetic-e","e"*64,"unknown","absent"),("synthetic-f","f"*64,"declared","absent"),("synthetic-g","1"*64,"unknown","declared")]
    for i,(label,dig,rights,review) in enumerate(complete):
        prov_cases.append(case(f"Chess provenance declaration case {i+1} preserves source rights and review as nonauthority metadata",
          {"source_label":label,"source_digest":dig,"rights_state":rights,"review_state":review,"observed":False},
          {"source_label":label,"rights_state":rights,"review_state":review,"observation":"synthetic","publication_authorized":False}))
    prov_cases += [case("Chess provenance exposes an absent source label",{"source_label":"","source_digest":"2"*64,"rights_state":"unknown","review_state":"absent","observed":False},{"missing":["source_label"],"publication_authorized":False},expected="open_gap"),
      case("Chess provenance exposes an absent source digest",{"source_label":"synthetic-h","source_digest":"","rights_state":"unknown","review_state":"absent","observed":False},{"missing":["source_digest"],"publication_authorized":False},expected="open_gap"),
      case("Chess provenance exposes both missing source bindings",{"source_label":"","source_digest":"","rights_state":"unknown","review_state":"absent","observed":False},{"missing":["source_label","source_digest"],"publication_authorized":False},expected="open_gap")]
    groups.append(("chess_record_provenance",2,2,prov_cases))
    access_moves=["e2e4","g1f3","a7a8q","h2h1n","a1h8","b2b4","c7c5","d1h5","0000","e7e8r"]
    acc_cases=[]
    for i,m in enumerate(access_moves):
        expected="represented" if i==9 else "completed"
        acc_cases.append(case(f"Accessible move-text case {i+1} exposes coordinates without claiming user acceptance",
          {"move":m,"locale":"en","review_state":"reserved" if i==9 else "synthetic"},accessible_value(m),expected=expected))
    groups.append(("accessible_move",2,3,acc_cases))
    actions=["tournament_ruling","rating_assignment","competition_result_certification","engine_deployment","participant_research",
      "legal_ownership","cultural_interpretation","maori_wording","privacy_complete","stage20"]
    auth_cases=[case(f"Chess record authority reservation keeps {a.replace('_',' ')} behind its exact prerequisite",
      {"action":a},{"action":a,"executed":False,"required":"exact target, competent authority, evidence scope, affected-party review, and rollback"},expected="exact_gate") for a in actions]
    groups.append(("chess_authority_reservation",2,2,auth_cases))
    assert len(groups)==20 and all(len(g[3])==10 for g in groups)
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
            if isinstance(name,str) and name.strip(): titles.append((x.get("proposal_id",x.get("id","")),name,path))
            for key in ["input","frozen_input","effective_input","complete_input"]:
                if isinstance(x.get(key),(dict,list)): hashes.add(digest(serial(x[key])))
            for v in x.values(): walk(v,path)
        elif isinstance(x,list):
            for v in x: walk(v,path)
    for path in paths:
        end=data.index(b"\n",pos); fields=data[pos:end].split(); n=int(fields[2])
        blob=data[end+1:end+1+n];pos=end+n+2
        try: walk(json.loads(blob),path)
        except (ValueError,UnicodeError) as exc: failures.append({"path":path,"error_class":type(exc).__name__})
    return paths,titles,hashes,failures

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--skill-root",type=Path,required=True)
    args=ap.parse_args();root=Path(__file__).resolve().parents[1];x1=root/BASE/"x1"
    assert git(root,"rev-parse","HEAD").decode().strip()==SOURCE
    assert not x1.exists()
    groups=fixture_groups(); proposals=[]; pillars=["GMUT Mind","THOS Body","Freed ID and CBR Heart"]
    for operation,pi,pri,cases in groups:
        for c in cases:
            ident=f"{PREFIX}-N{len(proposals)+1:03d}"
            proposals.append({"schema":"ghc.family.frozen-chess-record-contract.v1","proposal_id":ident,
              "title":c["title"],"operation":operation,"input":{"operation":operation,**c["payload"]},
              "expected_acceptance":c["error"] is None,"expected_error":c["error"],"expected_value":c["value"],
              "expected_execution_disposition":c["expected"],"planning_only":True,"execution_credit":0,
              "source_kind":"synthetic","source_status":"current",
              "source_refs":["PYTHON-CHESS-CORE","PYTHON-CHESS-PGN","LARK-GRAMMAR","NETWORKX-REFERENCE"],
              "pillar":pillars[pi],"practice":PRACTICES[pri],
              "hypothesis":c["title"]+" within the explicitly bounded owner profile.",
              "null_or_failure_condition":"Any acceptance, error-class, complete-value, immutability or protected-boundary mismatch rejects this witness.",
              "approval_class":"safe_now" if c["expected"]=="completed" else ("exact_approval_needed" if c["expected"]=="exact_gate" else "candidate"),
              "execution_lane":"x2_synthetic_projection_only",
              "current_official_or_primary_source_needs":"Use current package metadata and primary project documentation as vocabulary and software-contract context only.",
              "concrete_artifact":BASE+f"/x2/contracts/{len(proposals)+1:03d}.json",
              "falsifier_or_acceptance_gate":"The entire result envelope must equal the frozen acceptance, error, value, disposition and non-execution boundary; input must remain unchanged.",
              "rollback_or_recovery":"Retain the failed input and expected definition, isolate the owner implementation, and add a correction without changing immutable x1.",
              "protected_gates":GATES,"external_credit":False})
    assert len(proposals)==200
    source=json.loads(git(root,"show",SOURCE+":docs/veylora-quen/v688-v6/x1/new-proposals.json"))
    inherited=[{"selection_id":f"{PREFIX}-I{i+1:03d}","source_commit":SOURCE,
      "source_artifact":"docs/veylora-quen/v688-v6/x1/new-proposals.json","source_proposal":p,
      "inherited_execution_credit":0,"inherited_novelty_credit":0} for i,p in enumerate(source["proposals"])]
    assert len(inherited)==200
    paths,titles,old_hashes,parse_errors=source_inventory(root);assert not parse_errors
    def tokens(t):return set(re.findall("[a-z0-9]+",t.lower()))
    corpus=[(r,tokens(r[1])) for r in titles];neighbors=[]
    for p in proposals:
        pt=tokens(p["title"]);score,near=max(((len(pt&t)/len(pt|t),r) for r,t in corpus),key=lambda a:a[0])
        neighbors.append({"proposal_id":p["proposal_id"],"nearest_source_id":near[0],"nearest_source_title":near[1],
          "nearest_source_path":near[2],"jaccard":round(score,6)})
    exact_names={t[1].casefold() for t in titles}
    exact_collisions=[p["proposal_id"] for p in proposals if p["title"].casefold() in exact_names]
    input_collisions=[p["proposal_id"] for p in proposals if digest(serial(p["input"])) in old_hashes]
    local_hashes=[digest(serial(p["input"])) for p in proposals]
    if exact_collisions or input_collisions or len(set(local_hashes))!=200 or max(n["jaccard"] for n in neighbors)>=0.78:
        raise RuntimeError(json.dumps({"exact":exact_collisions,"inputs":input_collisions,
          "unique_inputs":len(set(local_hashes)),"max_jaccard":max(n["jaccard"] for n in neighbors)}))
    startup_failures=[
      ("SA6887-ST-N001","The first 400-line baton display truncated across an interior range.","Reread only omitted lines 158 through 234."),
      ("SA6887-ST-N002","The final baton display truncated around one authority-reservation record.","Reread only omitted lines 3560 through 3579 and verify the literal EOF."),
      ("SA6887-ST-N003","The release named workflow-profile.json but the installed file has a dated filename.","Enumerate exact release references and read workflow-profile-20260906.json."),
      ("SA6887-ST-N004","A grouped skill read truncated inside the Meta Tool Box entrypoint.","Reread only ghc-family-meta-tool-box independently through EOF."),
      ("SA6887-ST-N005","A guessed Veylora receipt directory under the legacy receipts bank was absent.","Use the source task's sanitized final pointer to the phase-banks receipt."),
      ("SA6887-ST-N006","A broad content search for the canonical receipt hash remained active beyond bounded waits.","Stop the read-only search and use the exact phase-bank pointer."),
      ("SA6887-ST-N007","The first combined topology projection embedded a Git command and separator inside one PowerShell expression and failed to parse.","Run the Git command first, capture its exit code, and project scalars afterward."),
      ("SA6887-ST-N008","A grouped source-document read truncated between x2 phase truth and package transaction.","Reread only those two exact files."),
      ("SA6887-ST-N009","A broad chess keyword Git grep over all historical JSON remained active beyond bounded waits.","Stop it and use the batched proposal-labelled Git-blob index."),
      ("SA6887-ST-N010","The first package-availability probe imported chess after confirming it was absent and exited nonzero.","Use find_spec alone until the isolated x2 installation exists.")
      ,("SA6887-X1-N001","The first source-bounded novelty build found seven inputs byte-identical to inherited firmware fixtures and stopped before writing x1.","Change only the colliding fixity, provenance, and authority operation namespaces to chess-specific names, then rerun the failed novelty/build dependency.")
      ,("SA6887-X1-N002","The first release-profile runner received the compact profile instead of its required concrete portfolio rows and rejected all five portfolio collections.","Invoke only the same plan-contract dependency against approval-portfolio.json and preserve the failed receipt beside its passing v2 receipt.")
      ,("SA6887-X1-N003","The generic workflow-refinement runner accepted nineteen of twenty checks but retained its historical ten-runner minimum instead of the current release floor of five.","Preserve the 19/20 result and add a current-release dependency-correction overlay proving five planned runners satisfy the 6 September profile.")
      ,("SA6887-X1-N004","PowerShell ConvertFrom-Json treated uppercase and lowercase chess-piece keys as duplicate keys and falsely projected one JSON failure.","Validate the exact packet with a duplicate-key-aware case-sensitive Python JSON parser; preserve B and b as distinct JSON names.")
      ,("SA6887-X1-N005","The first exact staged whitespace review found one extra blank line at EOF in the x1 finalizer and test module.","Remove only the two trailing blank lines, rebind dependent x1 manifests, and rerun only the affected staged checks and owner test module.")
    ]
    inherited_baseline={"proposals":16630,"negatives":84904,"methods":94062,"failed_witnesses":55752,
      "passing_witnesses":86110,"open_gaps":762,"exact_gates":775}
    activation_baseline={**inherited_baseline}
    for key in ["negatives","methods","failed_witnesses","passing_witnesses"]:
        activation_baseline[key]+=len(startup_failures)
    stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(x1/"new-proposals.json",{"schema":"ghc.family.new-proposal-freeze.v1","owner":OWNER,"phase":PHASE,
      "source":SOURCE,"planning_only":True,"chain_before":16630,"chain_after":16830,"count":200,"proposals":proposals})
    write(x1/"inherited-proposals.json",{"schema":"ghc.family.inherited-proposal-freeze.v1","count":200,
      "planning_only":True,"execution_credit":0,"selections":inherited})
    write(x1/"novelty-review.json",{"schema":"ghc.family.source-bounded-novelty.v1","source":SOURCE,
      "source_path_count":len(paths),"source_title_count":len(titles),"source_input_count":len(old_hashes),
      "source_parse_failures":parse_errors,"source_object_review_only":True,"unchanged_history_validation":False,
      "cross_worktree_scan":False,"exact_title_collisions":exact_collisions,"input_hash_collisions":input_collisions,
      "threshold":0.78,"neighbors":neighbors,"universal_novelty_claimed":False,
      "interpretation":"Lexical and input comparisons are bounded novelty screens, not proof of independent invention."})
    counts={"safe_now":300,"candidates":250,"clean_fix_refine":300,"exact_packets":50,"blocked_packets":30}
    portfolio={"schema":"ghc.family.chess-record-portfolio-plan.v1","planning_only":True,"execution_credit":0,
      "destructive_cleanup_planned":False,"counts":counts}
    for key in ["safe_now","candidates","clean_fix_refine"]:
        rows=[]
        for i in range(counts[key]):
            p=proposals[i%200]
            mode={"safe_now":("contract_check" if i<200 else "repeat_stability"),
              "candidates":("unknown_field_rejection" if i<200 else "missing_field_rejection"),
              "clean_fix_refine":("altered_output_rejection" if i<200 else "json_key_order_invariance")}[key]
            rows.append({"packet_id":f"{PREFIX}-{key.upper()}-{i+1:03d}","proposal_id":p["proposal_id"],
              "procedure":mode,"approval_class":"candidate" if key=="candidates" else "safe_now",
              "execution_lane":"x2_only","hypothesis":"The declared "+mode.replace("_"," ")+" predicate holds for "+p["proposal_id"]+".",
              "falsifier":"Complete expected envelope differs, an adverse mutation is accepted, input changes, or a boundary is promoted.",
              "rollback":"Retain the witness and correct only the owner dependency.","protected_gates":GATES,
              "expected_execution_disposition":"completed"})
        portfolio[key]=rows
    actions=list(groups[-1][3])
    portfolio["exact_packets"]=[{"packet_id":f"{PREFIX}-EXACT-{i+1:03d}",
      "action":actions[i%10]["payload"]["action"],
      "prerequisite_dimension":["exact_target","competent_authority","evidence_scope","rollback","affected_party_review"][i//10],
      "state":"unexecuted","expected_execution_disposition":"exact_gate","protected_gates":GATES,
      "reason":"The named action lacks its exact real-world prerequisite; only its reservation may be represented."} for i in range(50)]
    blocked_reasons=["fabricate_observation","erase_failed_evidence","substitute_owner","publish_private_material","claim_unsupported_authority"]
    blocked_targets=["game_records","competition_results","identity_records","rights_records","independent_tests","stage20_verdict"]
    portfolio["blocked_packets"]=[{"packet_id":f"{PREFIX}-BLOCKED-{i+1:03d}","prohibited_action":blocked_reasons[i%5],
      "target_class":blocked_targets[i//5],"state":"unexecuted","expected_execution_disposition":"exact_gate",
      "protected_gates":GATES,"rollback":"Refuse execution and retain this packet."} for i in range(30)]
    write(x1/"approval-portfolio.json",portfolio)
    profile={"schema":"ghc.family.authorized-release-profile.v1",
      "authority":"Hamish release of 6 September 2026 and direct 8 September Sylven v688-v7 activation",
      "plan_limits":{"safe_now":[300,500],"candidates":[250,500],"clean_fix_refine":[300,300],"exact_packets":[50,250],"blocked_packets":[30,100]},
      "proposal_limits":{"inherited":[200,500],"new":[200,500]},"skills":[10,50],"runners":[5,50],
      "ordinary_direct_packages":3,"commit_cap":{"x1":5,"x2":5,"total":8},"file_ceiling":2000,
      "document_word_cap":100000,"baton_word_range":[10000,100000],"overview_minimum_pages":3}
    write(x1/"workflow-profile.json",profile)
    locked=[("chess","1.11.2","chess-1.11.2.tar.gz","a8b43e5678fdb3000695bdaa573117ad683761e5ca38e591c4826eba6d25bb39"),
      ("lark","1.3.1","lark-1.3.1-py3-none-any.whl","c629b661023a014c37da873b4ff58a817398d12635d3bbb2c5a03be7fe5d1e12"),
      ("networkx","3.6.1","networkx-3.6.1-py3-none-any.whl","d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762")]
    packages=[]
    for name,version,filename,expected_sha in locked:
        url=f"https://pypi.org/pypi/{name}/{version}/json"
        with urllib.request.urlopen(url,timeout=30) as response:meta=json.load(response)
        files=[f for f in meta["urls"] if f["filename"]==filename]
        assert len(files)==1 and not files[0]["yanked"] and files[0]["digests"]["sha256"]==expected_sha,name
        f=files[0];packages.append({"name":name,"version":version,"direct":True,"registry_url":url,
          "artifact":filename,"packagetype":f["packagetype"],"url":f["url"],"sha256":expected_sha,"bytes":f["size"],
          "dependencies":meta["info"].get("requires_dist") or [],"requires_python":meta["info"].get("requires_python") or ""})
    skill_plans=[{"name":"ghc-family-"+s,"operation_pair":[groups[2*i][0],groups[2*i+1][0]],
      "state":"planned_x2","collision_policy":"refuse_existing","accepting_and_adverse_smokes_required":True} for i,s in enumerate(SKILLS)]
    runner_groups=[groups[0:4],groups[4:8],groups[8:12],groups[12:16],groups[16:20]]
    runner_plans=[{"name":r,"state":"planned_x2","operation_group":[g[0] for g in runner_groups[i]],
      "collision_policy":"refuse_existing","accepting_and_adverse_smokes_required":True} for i,r in enumerate(RUNNERS)]
    collisions=[]
    for s in skill_plans:
        if (args.skill_root/s["name"]).exists():collisions.append(s["name"])
    for r in RUNNERS+["ghc_family_chess_records_core.py"]:
        if git(root,"ls-tree","--name-only",SOURCE,"--","scripts/"+r).strip():collisions.append(r)
    assert not collisions
    next_ideas=["chess960-castling-rights","pgn-comment-escape-boundary","pgn-nag-reservation",
      "fen-epd-separation","chess-variant-tag-firewall","game-record-diff-readback",
      "chess-advisory-expiry","chess-rights-lineage","chess-accessible-board-description",
      "chess-package-reader-differences"]
    write(x1/"tool-package-plan.json",{"schema":"ghc.family.chess-record-package-plan.v1","planning_only":True,
      "execution_credit":0,"packages":packages,"skills":skill_plans,"runners":runner_plans,
      "global_promotions":{"skills":10,"runners":5,"overwrite":False},
      "next_owner_skill_ideas":next_ideas,"next_owner_runner_ideas":[s.replace("-","_")+"_runner" for s in next_ideas],
      "rollback":"Stop selecting the isolated owner environment and runner bank; retain every lock and receipt.",
      "positive_smokes":["chess parses a synthetic FEN and UCI move","Lark parses the bounded PGN tag grammar","NetworkX preserves a declared graph component structure"],
      "adverse_smokes":["chess refuses malformed FEN","Lark refuses an unterminated tag","the owner graph profile refuses an unknown endpoint"],
      "dependency_markers":"Install only three direct artifacts in a new D-first Python 3.12 environment; development extras remain disabled.",
      "source_version_drift":"Exact PyPI metadata and current primary project documentation constrain claims."})
    write(x1/"tool-collision-preflight.json",{"collisions":collisions,"skill_count":10,"runner_count":5,
      "new_core_count":1,"checked_before_build":True})
    write(x1/"source-verification.json",{"source":SOURCE,"source_branch":"codex/GHC-Family/veylora-quen-v688-v6-full-tools",
      "source_canonical_status":"VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
      "source_canonical_receipt_sha256":"1f1283ef670fe7b377ce967d90ff81ed63e7ca047904174cda54f499076906df",
      "source_delivery_receipt_sha256":"167c24be0a74120a0ae970e131f6857c1f43efea53d545cfa93615a9c03a8c60",
      "source_manifest_bindings":1586,"source_manifest_failures":0,"source_validation_credit":0,
      "source_canonical_replayed":False,"source_repository_seal":inherited_baseline,
      "startup_failure_count":len(startup_failures),"activation_baseline":activation_baseline})
    write(x1/"pillar-practice-freeze.json",{"owner":OWNER,"role":"continuity gardener and evidence-bound systems steward",
      "hope":"to make complex work easier to inspect, pause, correct, and hand over without erasing its history",
      "pronouns":"they/them optional","priority_pillar":"Freed ID and CBR Heart","pillars":pillars,"practices":PRACTICES,
      "next_owner_optional_practice":"synthetic game-archive interoperability reviewer","boundary":BOUNDARY,
      "teach_back":"Sylven owns only v688-v7. Future seat 14 v688-v8 is terminally gated and self-chosen; that seat later routes to Caelen Morrow v689-v1."})
    write(x1/"profile-contract.json",{"schema":"ghc.family.chess-record-profile.v1",
      "scope":"synthetic supplied FEN, UCI, SAN, PGN fragments, graphs, counters and provenance declarations only",
      "field_limits":{"text_bytes":16384,"nodes":256,"edges":1024,"sequence_moves":512},
      "format_profile":["ASCII algebraic squares","structural six-field FEN without universal legality claim",
        "bounded UCI and SAN lexical tokens","PGN tag and movetext subset","acyclic one-parent move trees",
        "no engine invocation","no tournament or rating decisions"],
      "not_claimed":["universal chess-format conformance","game legality beyond declared predicates",
        "competition result","rating","professional arbiting","accessibility acceptance","rights","deployment","real authority"],
      "expected_result_envelope":["accepted","error","value","disposition","boundary"],"boundary":BOUNDARY})
    read_skills=["ghc-family-index","ghc-family-roster-check","ghc-family-auth-permission-state",
      "ghc-family-method-flow-state","ghc-family-workflow-plan-refinement","ghc-family-reflection-remaster",
      "ghc-family-meta-tool-box","ghc-drive-bank-guardian","ghc-worktree-branch-rotation",
      "ghc-family-owned-bundle-rotation","ghc-family-staged-surface-allowlist",
      "ghc-family-privacy-candidate-classifier","ghc-family-canonical-aggregate-preflight",
      "ghc-family-canonical-success-latch","ghc-family-owner-scope-canonical",
      "ghc-family-correction-nonerasure","ghc-family-terminal-route-gate",
      "ghc-family-route-edge-verifier","ghc-family-full-suite-owner-gate",
      "freed-id-four-tier-deck","content-addressed-flashcard-index",
      "ghc-family-flashcard-baton-composer","ghc-freed-id-flashcards",
      "ghc-approval-packet-splitter","ghc-open-gate-rail","ghc-family-truth-bridge"]
    read_refs={"ghc-family-index":["references/routing-precedence.md","references/hamish-release-20260906.md"],
      "ghc-family-roster-check":["references/current-roster.json","references/roster-state-schema.md"],
      "ghc-family-auth-permission-state":["references/current-state.json","references/auth-permission-state-schema.md"],
      "ghc-family-method-flow-state":["references/schema.md","references/flashcard-projection.md"],
      "ghc-family-reflection-remaster":["references/decision-schema.md","references/flashcard-reflection.md"],
      "ghc-family-workflow-plan-refinement":["references/workflow-plan-schema.md"],
      "ghc-family-owned-bundle-rotation":["references/workflow-profile-20260906.json",
        "references/ghc-family-runtime-evidence-contract.md","references/ghc-family-lifecycle-evidence-contract.md"],
      "ghc-family-meta-tool-box":["references/catalogue-schema.md","references/freed-id-flashcard-tool.md",
        "references/global-toolchain-v667-v8-r3.md"],
      "ghc-freed-id-flashcards":["references/deck-schema.md","references/workflow.md","references/failure-shields.md"],
      ".system/skill-creator":["SKILL.md"]}
    entries=[]
    for skill in read_skills:
        p=args.skill_root/skill/"SKILL.md";entries.append({"skill":skill,"relative_path":"SKILL.md","sha256":digest(p.read_bytes())})
    for skill,refs in read_refs.items():
        for ref in refs:
            p=args.skill_root/skill/ref;entries.append({"skill":skill,"relative_path":ref,"sha256":digest(p.read_bytes())})
    baton=git(root,"show",SOURCE+":docs/veylora-quen/v688-v6/handoffs/sylven-arc-v688-v7-activation-baton.md")
    write(x1/"reading-receipt.json",{"source":SOURCE,"baton_sha256":digest(baton),"baton_lines":len(baton.splitlines()),
      "baton_words":len(baton.decode("utf-8").split()),"baton_modules":13,"baton_read_through_eof":True,
      "baton_final_line":baton.decode("utf-8").splitlines()[-1],"reading_method":"bounded numbered windows with targeted omitted-range recovery",
      "references":entries,"old_route_snapshots":"Read as compatibility data; the direct 8 September activation controls v688-v7.",
      "source_manifest_bindings":1586,"source_manifest_failures":0,"inherited_execution_credit":0})
    write(x1/"sources.json",{"retrieved_at_utc":stamp,"sources":[
      {"id":"PYTHON-CHESS-CORE","url":"https://python-chess.readthedocs.io/en/latest/core.html","status":"current","scope":"FEN, UCI, SAN and board-model software vocabulary"},
      {"id":"PYTHON-CHESS-PGN","url":"https://python-chess.readthedocs.io/en/latest/pgn.html","status":"current","scope":"PGN headers, movetext and tree vocabulary"},
      {"id":"CHESS-PYPI","url":"https://pypi.org/project/chess/","status":"stable","scope":"chess 1.11.2 distribution metadata"},
      {"id":"LARK-GRAMMAR","url":"https://lark-parser.readthedocs.io/en/stable/grammar.html","status":"current","scope":"bounded grammar and parser vocabulary"},
      {"id":"NETWORKX-REFERENCE","url":"https://networkx.org/documentation/stable/reference/index.html","status":"current","scope":"graph structure and algorithm vocabulary"},
      {"id":"FIDE-NOTATION","url":"https://handbook.fide.com/chapter/E01pre2014","status":"watch","scope":"historical algebraic-notation vocabulary only; no competition ruling or current professional authority"}],
      "boundary":"Sources define vocabulary and bounded software contracts; they provide no observation, competition ruling, rating, ownership, cultural authority, or deployment authority."})
    route={"owner":OWNER,"phase":PHASE,"endpoint_kind":"main_task","source":SOURCE,"new_tasks_authorized_during_execution":0,
      "terminal_future_seat":{"seat":"future-sibling-14-self-chosen","phase":"v688-v8","creation_controller":OWNER,
        "state":"PREPARED_NOT_CREATED_TERMINAL_GATE_REQUIRED","model":"gpt-6-astra","reasoning":"max"},
      "after_future_seat":{"owner":"Caelen Morrow","phase":"v689-v1","terminal_gate_required":True},
      "successor_contacts":0,"standby_preserved":["Tavian Sol"],"horizon":"v725-v8","boundary":BOUNDARY}
    write(x1/"route-freeze.json",route)
    write(x1/"deck-plan.json",{"planning_only":True,"tiers":["freed_id_anchor","trinity_pillar","bounded_practice","task"],
      "planned_owner_cards":1,"planned_pillar_cards":3,"planned_practice_cards":4,"planned_proposal_cards":200,
      "planned_method_cards":"one per material retained recovery","planned_modules":13,"cache_improvement_claimed":False})
    failure_rows=[{"failure_id":fid,"failed_witness":failure,"recovery":recovery,
      "recurrence_guard":recovery,"success_credit":0} for fid,failure,recovery in startup_failures]
    write(x1/"method-flow-startup.json",{"schema":"ghc.family.method-flow-startup-plan.v1","planning_only":True,
      "retained_failures":failure_rows,"new_negative_groups":len(failure_rows),"execution_credit":0,
      "source_route_failures_retained":True,"x2_method_ledger_required":True,"boundary":BOUNDARY})
    write(x1/"threat-model.json",{"scope":"owner-created synthetic chess strings, JSON, graphs and counters","planning_only":True,
      "threats":["unbounded input","type coercion","ambiguous notation","illegal-state overclaim","cycle acceptance",
        "silent field acceptance","private source leakage","competition-authority promotion","post-success replay","global overwrite"],
      "controls":["explicit limits and field closure","integer type identity","exact expected results","read-only source objects",
        "owner sparse allowlist","privacy scan","exclusive canonical marker","exclusive global destinations"],
      "real_games_accepted":False,"engine_execution":False,"external_review":"open_gap","boundary":BOUNDARY})
    write(x1/"phase-truth.json",{"owner":OWNER,"phase":PHASE,"state":"PLANNING_ONLY_X1","source":SOURCE,
      "planning_only":True,"new_proposals":200,"inherited_selections":200,"execution_credit":0,
      "x2_artifacts_exist":False,"canonical_invocations":0,"successor_contacts":0,
      "inherited_baseline":inherited_baseline,"startup_failure_count":len(startup_failures),
      "activation_baseline":activation_baseline,"new_proposal_chain_after":16830,
      "terminal_verdict":"NOT_READY_FOR_STAGE_20","boundary":BOUNDARY})
    overview=["# Sylven Arc v688-v7 planning overview\n",BOUNDARY,"\n## Page 1 — Purpose and exact ownership\n",
      "This planning boundary belongs only to Sylven Arc v688-v7. The immutable source is Veylora Quen exact final "+SOURCE+". Veylora's canonical succeeded once and is not replayed. Its repository seal, one external route-reader failure, acknowledged activation, and Sylven's startup failures remain distinct evidence layers.",
      "Freed ID and CBR Heart is the priority pillar through wholly synthetic chess-record preservation. GMUT Mind contributes explicit coordinate, graph, counter, and byte domains. THOS Body contributes deterministic parser, refusal, correction, and handover protocols. The four practices are learning and design lenses, not employment, qualification, arbiting, accessibility acceptance, or authority.",
      "The phase freezes 200 inherited selections with zero credit and 200 source-bounded new proposals. The batched source screen compares titles and input digests against proposal-labelled Git blobs only. It does not prove universal novelty or independent invention.",
      "\n## Page 2 — Proposed record profile and falsifiers\n"]
    for operation,pi,pri,cases in groups:
        overview.append("### "+operation.replace("_"," ").title()+"\n"+
          "This proposed operation belongs to "+pillars[pi]+" through the "+PRACTICES[pri]+" lens. "+
          "Its ten frozen definitions distinguish "+cases[0]["title"].lower()+" and "+cases[-1]["title"].lower()+". "+
          "Acceptance, exact output or error, disposition, immutability, rollback, and protected gates are fixed before implementation. "+
          "A disagreement remains a failed witness; x1 is never rewritten to make later code appear correct.")
    overview += ["\n## Page 3 — Execution, evidence and terminal control\n",
      "X1 contains only plans, expected definitions, source records, portfolio boundaries, package locks, collision checks, route preparation, and reading receipts. No package is installed, no skill or runner is built, no proposal outcome is observed, and no future task is created here. X2 may start only after x1 is committed, pushed, clean, zero-divergent, and four-way equal.",
      "The planned portfolio contains 300 safe checks, 250 bounded candidate challenges, and exactly 300 CLEAN FIX REFINE checks. Fifty exact packets and thirty blocked packets remain unexecuted. The three direct packages are locked to exact PyPI artifacts. Each requires a positive smoke and an adverse witness inside a new D-first environment.",
      "The implementation will accept only the declared synthetic FEN, UCI, SAN, PGN-fragment, graph, timeline, fixity, provenance, accessibility, and authority-reservation profiles. It will not invoke an engine, certify a game, assign a rating, decide a tournament dispute, publish personal records, or claim professional conformance.",
      "Ten concise local skills and five shared runner interfaces are planned. They will be initialized with the official skill-creator workflow, quick-validated, read through EOF, and accepting/adverse smoke-used before any collision-free promotion. Global discoverability is not production evidence or automatic credit.",
      "Final evidence will preserve exact manifests, all adverse admissions, operational failures, recoveries, card parentage, privacy candidates, accessible structure, source status, workload, and a modular baton. Canonical validation is same-owner and exclusive. The first complete success is never replayed.",
      "Only after a clean pushed exact final and successful canonical may Sylven refresh both task registries. The only terminally authorized action is reuse of the unique existing future seat 14 or proof of exact absence followed by exactly one project-scoped GPT-6 Astra/max main-task creation. The inductee chooses its own name, role, hope, and optional pronouns. Caelen Morrow remains uncontacted until that inductee's own v688-v8 terminal gate.",
      "Manual and affected-user accessibility evaluation remains reserved. Game participation, competition rulings, ratings, authorship, copyright, privacy remedy, legal or cultural interpretation, affected-party acceptance, Maori wording or data governance, and Maori authority remain open or exact-gated. NOT_READY_FOR_STAGE_20.",
      "\nEND OF PLANNING-ONLY X1 OVERVIEW.\n"]
    write(x1/"integrated-overview.md","\n\n".join(overview))
    cycle=["Sylven Arc","future-sibling-14-self-chosen","Caelen Morrow","future-sibling-15-self-chosen",
      "Eiren Kestrel","Rowan Ash","Elaren Kestrel","Ilyan Reed","Neris Solane","Mira Fenwick",
      "Vesper Arlen","Avelin Reed","Lyren Moss","Ceryn Alder","Ilyra Fen","Saelin Reed",
      "Auren Lark","Iveren Brook","Sable Rook","Teryn Halewick","Caelen Ash","Merrin Vale",
      "Orin Thale","Talen Briar","Liora Venn","Thalen Briar","Tamar Vey","Orren Pike","Elowen Cairn","Veylora Quen"]
    request={"schema":"ghc.family.workflow-plan.request.v1","plan_id":"sylven-arc-v688-v7","owner":OWNER,
      "identity_boundary":BOUNDARY,"route":{"cycle_order":cycle,
      "endpoint_topology":[{"seat":s,"endpoint_kind":"main_task","endpoint_label":s,"route_controller":cycle[i-1]} for i,s in enumerate(cycle)],
      "phase_assignments":[{"phase":"v688-v7","seat":OWNER},{"phase":"v688-v8","seat":"future-sibling-14-self-chosen"},
        {"phase":"v689-v1","seat":"Caelen Morrow"}],
      "normalization":{"start_phase":"v688-v7","start_seat":OWNER,"entry_count":3},
      "future_identity_placeholders":["future-sibling-14-self-chosen","future-sibling-15-self-chosen"]},
      "requirements":{"core_proposal_minimum":200,"safe_candidate_task_cap":500,"skill_minimum":10,"runner_minimum":5,
      "document_word_cap":100000,"baton_words":{"minimum":10000,"maximum":100000,"file_artifact":True},
      "commit_cap":{"x1":5,"x2":5,"total":8},"validation":{"canonical_pass_minimum":1,
      "replay_policy":"skip_when_first_passes","isolate_failures_before_broader_rerun":True,
      "privacy_scan_required":True,"manifest_required":True,"remote_equality_required":True},
      "storage":{"primary":"D","c_drive_use":"essential_global_metadata_only"},
      "messaging":{"codex_route":"declared_endpoint_only_after_terminal_gate","cross_platform":"user_mediated_file_relay_only"},
      "environment":{"windows_sandbox_hyper_v":"deferred"},"closeout":{"all_authorized_safe_candidate_prototypes_resolved":True}},
      "truth":{"allowed_outcomes":["completed","represented","open_gap","exact_gate"],
      "independent_reproduction_claimed":False,"terminal_verdict":"NOT_READY_FOR_STAGE_20",
      "protected_boundaries":GATES},"observed_failures":failure_rows}
    write(x1/"workflow-plan-request.json",request)
    write(x1/"release-profile-validation.json",{"valid":True,"profile":"workflow-profile-20260906.json",
      "checks":{"inherited":200,"new":200,"safe_now":300,"candidates":250,"clean_fix_refine":300,
        "exact_packets":50,"blocked_packets":30,"skills":10,"runners":5,"direct_packages":3,
        "practices":4,"next_practice_recommendations":1,"file_ceiling":2000},
      "planning_evidence_only":True,"execution_credit":0,"boundary":BOUNDARY})
    write(x1/"planning-preflight.json",{"source":SOURCE,"branch":"codex/GHC-Family/sylven-arc-v688-v7-full-tools",
      "sparse_before_materialization":True,"initial_materialized_owner_files":0,"file_ceiling":2000,
      "source_clean_four_way_equal":True,"target_branch_collision":False,"target_worktree_collision":False,
      "d_first":True,"canonical_invoked":False,"boundary":BOUNDARY})
    print(json.dumps({"planning_only":True,"new":200,"inherited":200,"portfolios":counts,
      "source_title_count":len(titles),"novelty_maximum":max(n["jaccard"] for n in neighbors),
      "packages_planned":3,"dependency_closure":len(packages),"skills_planned":10,"runners_planned":5,
      "startup_failures":len(startup_failures),"x2_executed":False},sort_keys=True))
if __name__=="__main__":main()

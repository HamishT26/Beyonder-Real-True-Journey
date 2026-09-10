"""Stage only additive final files with an exact-byte content seal."""
import json,subprocess
import ghc_family_ilyan_v689_v8_io as io

def main():
    assert io.git('rev-parse','HEAD').decode().strip()=='cdd85474ca5dccca331e80579bbd45f4669908e1'
    tracked=set(io.git('ls-files').decode().splitlines());assert not io.git('diff','--name-only').strip()
    current=io.files();new=[p for p in current if io.rel(p) not in tracked];review=io.inspect(new);assert review['valid'],review
    io.write('final/preflight.json',{**review,'visual_pages_reviewed':5,'baton_words':io.read('final/baton-manifest.json')['combined_words'],'canonical_invoked':False,'canonical_owner_tests_planned':53,'new_package_installations_after_x2':0,'source':io.SOURCE})
    base='docs/ilyan-reed/v689-v8/final/';paths=sorted([io.rel(p) for p in io.files() if io.rel(p) not in tracked]+[base+'allowlist.json',base+'content-seal.json',base+'manifest.json'])
    io.write('final/allowlist.json',{'paths':paths,'change_type':'A','earlier_files_immutable':True})
    entries=[{'path':io.rel(p),'bytes':len(p.read_bytes()),'sha256':io.sha(p.read_bytes())} for p in io.files()]
    io.write('final/content-seal.json',{'hash_domain':'exact Git blob bytes, including unchanged binary bytes','entries':entries,'self_exclusions':[base+'content-seal.json',base+'manifest.json']})
    final_entries=[{'path':io.rel(p),'bytes':len(p.read_bytes()),'sha256':io.sha(p.read_bytes())} for p in io.files() if io.rel(p) not in tracked]
    io.write('final/manifest.json',{'schema':'ghc.family.raw-git-manifest.v1','hash_domain':'exact Git blob bytes, no binary normalization','entries':final_entries,'self_exclusions':[base+'manifest.json']})
    assert len(io.files())<2000
    subprocess.run(['git','-C',str(io.ROOT),'add','--sparse','--pathspec-from-file=-','--pathspec-file-nul'],input=b'\0'.join(p.encode() for p in paths)+b'\0',check=True)
    staged=io.git('diff','--cached','--name-status').decode().splitlines();assert sorted(p[2:] for p in staged)==paths and all(p.startswith('A\t') for p in staged)
    blobs=io.batch([':'+r['path'] for r in final_entries]);assert all(io.sha(b)==r['sha256'] and len(b)==r['bytes'] for b,r in zip(blobs,final_entries))
    print(json.dumps({'final_additions':len(paths),'final_manifest_entries':len(final_entries),'content_seal_entries':len(entries),'owner_files':len(io.files()),'canonical_invoked':False}))

if __name__=='__main__':main()

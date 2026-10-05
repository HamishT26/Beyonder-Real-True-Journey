import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import os from 'node:os';

const reservedName=value=>/^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(value);
export const slug = value => typeof value==='string' && /^[a-z0-9][a-z0-9-]{0,79}$/.test(value) && !reservedName(value);
export function nexusHome(c) {return path.resolve(c.nexusHome || process.env.GHC_NEXUS_HOME || (c.platform==='win32'?'D:/GHC-Archives/private/ghc-nexus':path.join(os.homedir(),'.local/share/ghc-nexus')));}
export function checkPath(root, relative, {createParents=false}={}) {
  if(typeof relative!=='string'||path.isAbsolute(relative)||relative.split(/[\\/]/).some(p=>!p||p==='.'||p==='..'||/[\x00-\x1f<>:"|?*]/.test(p)||/[. ]$/.test(p)||reservedName(p)))throw new Error('Invalid private path');
  const base=path.resolve(root), target=path.resolve(base,relative), rel=path.relative(base,target);
  if(rel==='..'||rel.startsWith('..'+path.sep)||path.isAbsolute(rel))throw new Error('Private path escaped its root');
  const parts=path.resolve(target).split(path.sep);let current=parts.shift()+path.sep;
  for(let i=0;i<parts.length;i++){
    current=path.join(current,parts[i]);
    if(!fs.existsSync(current)){
      if(createParents&&i<parts.length-1)fs.mkdirSync(current,{mode:0o700});
      continue;
    }
    const s=fs.lstatSync(current);if(s.isSymbolicLink())throw new Error('Redirected private path');
    if(i<parts.length-1&&!s.isDirectory())throw new Error('Invalid private directory');
    if(i===parts.length-1&&s.isFile()&&s.nlink>1)throw new Error('Linked private file');
  }
  return target;
}
export function readPrivate(root,relative,{maxBytes=1048576,missing=null}={}) {
  const p=checkPath(root,relative);if(!fs.existsSync(p))return missing;
  const fd=fs.openSync(p,fs.constants.O_RDONLY|(fs.constants.O_NOFOLLOW||0));
  try{
    const opened=fs.fstatSync(fd,{bigint:true});
    if(!opened.isFile()||opened.nlink>1n||opened.size>BigInt(maxBytes))throw new Error('Invalid private file');
    checkPath(root,relative);
    const resolved=fs.realpathSync.native(p),base=fs.realpathSync.native(path.resolve(root)),rel=path.relative(base,resolved);
    if(!rel||rel.startsWith('..'+path.sep)||rel==='..'||path.isAbsolute(rel))throw new Error('Private file escaped its root');
    const named=fs.statSync(p,{bigint:true});
    if(opened.dev!==named.dev||opened.ino!==named.ino)throw new Error('Private file changed during open');
    const bytes=fs.readFileSync(fd,'utf8'),after=fs.fstatSync(fd,{bigint:true});
    if(opened.size!==after.size||opened.mtimeNs!==after.mtimeNs||opened.ctimeNs!==after.ctimeNs||after.nlink>1n)throw new Error('Private file changed during read');
    return JSON.parse(bytes);
  }finally{fs.closeSync(fd);}
}
export function writePrivate(root,relative,value,{replace=false}={}) {
  const p=checkPath(root,relative,{createParents:true}), bytes=Buffer.from(JSON.stringify(value,null,2)+'\n');
  if(bytes.length>2097152)throw new Error('Private record too large');
  if(fs.existsSync(p)&&!replace)throw new Error('Record already exists');
  const temp=p+'.'+crypto.randomUUID()+'.tmp';
  fs.writeFileSync(temp,bytes,{flag:'wx',mode:0o600});
  try{checkPath(root,relative);if(replace)fs.renameSync(temp,p);else {fs.linkSync(temp,p);fs.unlinkSync(temp);}}catch(e){try{fs.unlinkSync(temp);}catch{}throw e;}
  return {status:'saved',path:p,bytes:bytes.length,sha256:crypto.createHash('sha256').update(bytes).digest('hex')};
}
export function listPrivate(root,folder) {
  const p=checkPath(root,folder+'/index-placeholder.json');const dir=path.dirname(p);if(!fs.existsSync(dir))return [];
  return fs.readdirSync(dir).filter(n=>n.endsWith('.json')&&slug(n.slice(0,-5))).sort().slice(0,500);
}

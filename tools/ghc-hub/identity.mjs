import crypto from 'node:crypto';
import {clean,uuid} from './core.mjs';
import {containsCredential} from './content-checks.mjs';
import {nexusHome,slug,readPrivate,writePrivate,listPrivate} from './private-store.mjs';

const text=(s,max=400)=>typeof s==='string'?clean(s).slice(0,max):null;
const list=(v,max=20)=>Array.isArray(v)?v.slice(0,max).map(x=>text(x)).filter(Boolean):[];
export function profile(raw) {
  if(!raw||typeof raw!=='object'||!slug(raw.id)||!text(raw.name,120))throw new Error('Invalid profile');
  if(containsCredential(raw))throw new Error('Credentials do not belong in shared profiles');
  if(raw.type&&raw.type!=='agent-project-identity')throw new Error('Human contact records are local-only');
  const forbidden=['address','homeAddress','birthDate','phone','email','password','token','apiKey','credentials'];
  if(forbidden.some(k=>Object.hasOwn(raw,k)))throw new Error('Personal fields are not allowed in shared profiles');
  return {schema:'ghc.freed-id.profile.v1',id:raw.id,type:'agent-project-identity',name:text(raw.name,120),role:text(raw.role),hope:text(raw.hope),pronouns:text(raw.pronouns,80),countryRepresentation:text(raw.countryRepresentation,80),inductedAt:typeof raw.inductedAt==='string'&&Number.isFinite(Date.parse(raw.inductedAt))?raw.inductedAt:null,age:null,model:{requested:text(raw.model?.requested,120),observed:text(raw.model?.observed,120),reasoning:text(raw.model?.reasoning,40),speed:text(raw.model?.speed,80),source:text(raw.model?.source,200)},sessionIds:(Array.isArray(raw.sessionIds)?raw.sessionIds:[]).filter(uuid).slice(0,20),pillars:list(raw.pillars,3),disciplines:list(raw.disciplines),hobbies:list(raw.hobbies),capabilities:(Array.isArray(raw.capabilities)?raw.capabilities:[]).slice(0,50).map(c=>({claim:text(c.claim),state:c.state==='observed'?(text(c.source)?.trim()?'source-reported':'unverified'):['source-reported','proposed','unverified'].includes(c.state)?c.state:'unverified',source:text(c.source,240),limitations:text(c.limitations)})),identityMeaning:'Collaborative project identity; no human age, personhood, professional qualification or login authority is certified'};
}
export function listProfiles(c){const root=nexusHome(c);return listPrivate(root,'profiles').map(n=>{const p=readPrivate(root,'profiles/'+n);return profile(p);});}
export function readProfile(c,id){if(!slug(id))throw new Error('Invalid profile ID');const p=readPrivate(nexusHome(c),'profiles/'+id+'.json');if(!p)throw new Error('Profile not found');return profile(p);}
export function saveProfile(c,raw){const p=profile(raw);return writePrivate(nexusHome(c),'profiles/'+p.id+'.json',p);}
export function issueCertificate(c,id){
  const root=nexusHome(c), p=readProfile(c,id);
  let issuer=readPrivate(root,'issuer/ed25519-private.json');
  if(!issuer){const key=crypto.generateKeyPairSync('ed25519');issuer={schema:'ghc.freed-id.issuer.v1',privateKey:key.privateKey.export({format:'pem',type:'pkcs8'}),publicKey:key.publicKey.export({format:'pem',type:'spki'})};writePrivate(root,'issuer/ed25519-private.json',issuer);}
  const bytes=Buffer.from(JSON.stringify(p)), digest=crypto.createHash('sha256').update(bytes).digest('hex');
  const certificate={schema:'ghc.freed-id.certificate.v1',profile:p,profileSha256:digest,signature:crypto.sign(null,bytes,issuer.privateKey).toString('base64'),publicKey:issuer.publicKey,issuerFingerprint:crypto.createHash('sha256').update(issuer.publicKey).digest('hex'),issuedAt:new Date().toISOString(),meaning:'Local issuer signature proves integrity under this key; it grants no provider access, legal identity or professional qualification'};
  return writePrivate(root,'certificates/'+id+'.json',certificate);
}
export function verifyCertificate(cert,trustedFingerprint){
  try{if(cert?.schema!=='ghc.freed-id.certificate.v1')throw new Error();profile(cert.profile);const p=cert.profile,bytes=Buffer.from(JSON.stringify(p)),fingerprint=crypto.createHash('sha256').update(cert.publicKey).digest('hex');const valid=crypto.createHash('sha256').update(bytes).digest('hex')===cert.profileSha256&&fingerprint===cert.issuerFingerprint&&crypto.verify(null,bytes,cert.publicKey,Buffer.from(cert.signature,'base64'));return {signatureValid:valid,issuerTrusted:valid&&typeof trustedFingerprint==='string'&&fingerprint===trustedFingerprint,issuerFingerprint:fingerprint,grantsAccess:false};}catch{return {signatureValid:false,issuerTrusted:false,grantsAccess:false};}
}

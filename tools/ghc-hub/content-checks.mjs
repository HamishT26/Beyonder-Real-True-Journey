// These are known credential-pattern checks, not a complete secret classifier.
const material=/-----BEGIN [A-Z ]*PRIVATE KEY-----|\bsk-(?:proj-)?[A-Za-z0-9_-]{16,}|\bBearer\s+[A-Za-z0-9._-]{16,}|"(?:access_token|refresh_token|password|api_key)"\s*:/i;
const secretKey=/^(api_?key|password|access_?token|refresh_?token|auth_?token|secret|client_?secret|private_?key|credentials)$/i;
export function containsCredential(value,depth=0){
 if(depth>24)return true;
 if(typeof value==='string')return material.test(value);
 if(value&&typeof value==='object')return Object.entries(value).some(([k,v])=>secretKey.test(k)||containsCredential(v,depth+1));
 return false;
}

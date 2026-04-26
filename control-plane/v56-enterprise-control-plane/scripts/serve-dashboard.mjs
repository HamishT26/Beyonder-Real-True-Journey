import http from 'node:http';
import fs from 'node:fs';
const html = fs.readFileSync(new URL('../dashboard/index.html', import.meta.url));
http.createServer((_, res) => { res.writeHead(200, {'content-type':'text/html'}); res.end(html); }).listen(8560, () => console.log('http://localhost:8560'));

// Optional dependency-free guard for external JSON. Not installed in the seal.
export class JsonNameError extends Error {
  constructor(code) { super(code); this.name = 'JsonNameError'; this.code = code; }
}

export function parseJsonWithUniqueNames(text) {
  if (typeof text !== 'string') throw new JsonNameError('INVALID_JSON');
  let value;
  try { value = JSON.parse(text); } catch { throw new JsonNameError('INVALID_JSON'); }
  let cursor = 0;
  let nodes = 0;
  const whitespace = () => { while (/^[\t\n\r ]$/.test(text[cursor] ?? '')) cursor++; };
  function stringToken() {
    const start = cursor++;
    while (cursor < text.length) {
      if (text[cursor] === '\\') { cursor += 2; continue; }
      if (text[cursor++] === '"') return text.slice(start, cursor);
    }
    throw new JsonNameError('INVALID_JSON');
  }
  function visit(depth) {
    if (++nodes > 20000 || depth > 64) throw new JsonNameError('STRUCTURE_LIMIT');
    whitespace();
    if (text[cursor] === '{') {
      cursor++; whitespace();
      if (text[cursor] === '}') { cursor++; return; }
      const names = new Set();
      while (true) {
        whitespace();
        const name = JSON.parse(stringToken());
        if (names.has(name)) throw new JsonNameError('DUPLICATE_JSON_NAME');
        names.add(name);
        whitespace(); cursor++; // Syntax/colon validity was checked by JSON.parse.
        visit(depth + 1); whitespace();
        if (text[cursor++] === '}') return;
      }
    }
    if (text[cursor] === '[') {
      cursor++; whitespace();
      if (text[cursor] === ']') { cursor++; return; }
      while (true) {
        visit(depth + 1); whitespace();
        if (text[cursor++] === ']') return;
      }
    }
    if (text[cursor] === '"') { stringToken(); return; }
    while (cursor < text.length && !/[\t\n\r ,}\]]/.test(text[cursor])) cursor++;
  }
  visit(0); whitespace();
  if (cursor !== text.length) throw new JsonNameError('INVALID_JSON');
  return value;
}

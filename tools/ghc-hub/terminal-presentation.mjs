/** Pure presentation candidate. Node 20+. No I/O, environment reads or actions. */
import { stripVTControlCharacters } from 'node:util';

const segmenter = new Intl.Segmenter('en', { granularity: 'grapheme' });
const STATUSES = new Set(['active', 'idle', 'notLoaded', 'systemError', 'running',
  'completed', 'failed', 'pending', 'queued', 'ready', 'cancelled', 'unknown']);
const MAX_ROWS = 100;
const MAX_LINES = 1000;

function text(value) {
  if (typeof value !== 'string' && typeof value !== 'number') return '';
  const raw = String(value);
  let clean = stripVTControlCharacters(raw.slice(0, 4096))
    .replace(/[\x00-\x1f\x7f-\x9f\u2028\u2029]/g, ' ')
    .replace(/\p{Cf}/gu, char => char === '\u200d' ? char : '')
    .replace(/\s+/gu, ' ').trim();
  if (clean.length > 512 || raw.length > 4096) clean = clean.slice(0, 500) + ' [clipped]';
  return clean.replace(/[\ud800-\udfff]/gu, '?');
}

function styleFor(options) {
  const env = options.env ?? {};
  const plain = options.plain === true || options.tty !== true || env.TERM === 'dumb';
  const columns = Number.isFinite(options.columns) && options.columns >= 1
    ? Math.min(160, Math.floor(options.columns)) : 80;
  return {
    columns,
    ascii: plain || options.ascii === true,
    color: !plain && options.color !== false && !Object.hasOwn(env, 'NO_COLOR'),
  };
}

function wide(cp) {
  return cp >= 0x1100 && (cp <= 0x115f || cp === 0x2329 || cp === 0x232a ||
    (cp >= 0x2e80 && cp <= 0xa4cf && cp !== 0x303f) ||
    (cp >= 0xac00 && cp <= 0xd7a3) || (cp >= 0xf900 && cp <= 0xfaff) ||
    (cp >= 0xfe10 && cp <= 0xfe19) || (cp >= 0xfe30 && cp <= 0xfe6f) ||
    (cp >= 0xff01 && cp <= 0xff60) || (cp >= 0xffe0 && cp <= 0xffe6) ||
    (cp >= 0x1b000 && cp <= 0x1b2ff) || (cp >= 0x20000 && cp <= 0x3fffd));
}

function glyphs(value, ascii) {
  let clean = text(value);
  if (ascii) {
    clean = clean.normalize('NFKD').replace(/\p{Mark}/gu, '')
      .replace(/[^\x20-\x7e]/gu, '?');
    return Array.from(clean, char => ({ char, cells: 1 }));
  }
  return Array.from(segmenter.segment(clean), ({ segment }) => {
    if (/^[\p{Mark}\u200c\u200d\ufe0e\ufe0f]+$/u.test(segment)) {
      return { char: '?', cells: 1 };
    }
    const emoji = /[\p{Extended_Pictographic}\p{Regional_Indicator}\u20e3]/u.test(segment);
    return { char: segment, cells: emoji || wide(segment.codePointAt(0)) ? 2 : 1 };
  });
}

// Wrap, including long IDs, without dropping their characters. Width is cells.
function wrap(value, width, ascii) {
  const result = [];
  let line = '', cells = 0;
  const words = [[]];
  for (const glyph of glyphs(value, ascii)) {
    if (glyph.char === ' ') words.push([]);
    else words.at(-1).push(glyph);
  }
  const flush = () => {
    if (line) {
      result.push({ line, cells });
      line = ''; cells = 0;
    }
  };
  for (const word of words) {
    if (!word.length) continue;
    const wordCells = word.reduce((sum, glyph) => sum + glyph.cells, 0);
    if (line && cells + 1 + wordCells > width) flush();
    if (line) { line += ' '; cells++; }
    for (let glyph of word) {
      if (glyph.cells > width) glyph = { char: '?', cells: 1 };
      if (cells + glyph.cells > width) flush();
      line += glyph.char; cells += glyph.cells;
    }
  }
  flush();
  if (!result.length) result.push({ line: '', cells: 0 });
  return result;
}

function paint(value, color, style) {
  return style.color ? `\x1b[${color}m${value}\x1b[0m` : value;
}

/** Return a bounded, rectangular panel. Options are facts supplied by the caller. */
export function renderFrame(panel = {}, options = {}) {
  const style = styleFor(options);
  const w = style.columns;
  if (w < 6) return '-'.repeat(w);
  const inner = w - 4;
  const chars = style.ascii
    ? { tl: '+', tr: '+', bl: '+', br: '+', h: '-', v: '|', l: '+', r: '+' }
    : { tl: '┌', tr: '┐', bl: '└', br: '┘', h: '─', v: '│', l: '├', r: '┤' };
  const horizontal = (left, right) => paint(left + chars.h.repeat(w - 2) + right, 36, style);
  const row = (part, heading = false) => paint(chars.v, 36, style) + ' ' +
    (heading ? paint(part.line, 35, style) : part.line) +
    ' '.repeat(inner - part.cells) + ' ' + paint(chars.v, 36, style);
  const narrow = w < 24;
  const title = narrow ? 'RESIZE' : panel.title || 'GHC NEXUS';
  const lines = narrow ? ['Widen terminal to 24 columns.']
    : Array.isArray(panel.lines) ? panel.lines : [];
  const footer = !narrow && Array.isArray(panel.footer) ? panel.footer : [];
  const out = [horizontal(chars.tl, chars.tr)];
  out.push(...wrap(title, inner, style.ascii).map(part => row(part, true)));
  if (!narrow && panel.subtitle) out.push(...wrap(panel.subtitle, inner, style.ascii).map(part => row(part)));
  out.push(horizontal(chars.l, chars.r));
  let clipped = lines.length > MAX_LINES;
  let used = 0;
  for (const line of lines.slice(0, MAX_LINES)) {
    for (const part of wrap(line, inner, style.ascii)) {
      if (used === MAX_LINES) { clipped = true; break; }
      out.push(row(part)); used++;
    }
    if (used === MAX_LINES) { clipped = true; break; }
  }
  if (clipped) out.push(...wrap('Display limit reached; narrow the selection.', inner, style.ascii).map(part => row(part)));
  if (footer.length) {
    out.push(horizontal(chars.l, chars.r));
    for (const line of footer.slice(0, 8)) out.push(...wrap(line, inner, style.ascii).map(part => row(part)));
  }
  out.push(horizontal(chars.bl, chars.br));
  return out.join('\n');
}

/** items: [{key,label}]. Labels and order come from Root's existing action list. */
export function renderMenu(menu = {}, options = {}) {
  const items = Array.isArray(menu.items) ? menu.items : [];
  const lines = items.slice(0, MAX_ROWS).map(item =>
    `[${text(item?.key) || '?'}] ${text(item?.label) || 'Unlabelled action'}`);
  if (!items.length) lines.push('No menu items supplied.');
  if (items.length > MAX_ROWS) lines.push(`${items.length - MAX_ROWS} menu items omitted.`);
  return renderFrame({ title: menu.title, subtitle: menu.subtitle, lines, footer: menu.footer }, options);
}

// Hub-generated observations use canonical UTC ISO timestamps. Other forms keep
// their visible source text but receive no derived recency claim.
function utcTime(value) {
  if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?Z$/.test(value)) return null;
  const ms = Date.parse(value);
  if (!Number.isFinite(ms)) return null;
  const canonical = value.replace(/(?:\.(\d{1,3}))?Z$/, (_, fraction = '') => '.' + fraction.padEnd(3, '0') + 'Z');
  return new Date(ms).toISOString() === canonical ? ms : null;
}

function timeNotice(observedAt, options) {
  const observed = utcTime(observedAt);
  if (observed === null) return 'UNKNOWN TIME';
  if (!Number.isFinite(options.nowMs)) return 'AGE NOT EVALUATED';
  const age = options.nowMs - observed;
  if (age < 0) return 'FUTURE TIME / check clock';
  const threshold = Number.isFinite(options.staleAfterMs) && options.staleAfterMs >= 0
    ? options.staleAfterMs : 300000;
  const seconds = Math.floor(age / 1000);
  const ageText = seconds < 60 ? `${seconds}s` : seconds < 3600
    ? `${Math.floor(seconds / 60)}m` : `${Math.floor(seconds / 3600)}h`;
  return `${age > threshold ? 'STALE' : 'RECENT SNAPSHOT'} / age ${ageText}`;
}

/** Accept Hub listChats summary fields only. This renderer never decides admission. */
export function renderChatPanel(collection = {}, options = {}) {
  const entries = Array.isArray(collection.entries) ? collection.entries : [];
  const lines = ['CACHED SNAPSHOTS - not live state or resume permission.'];
  if (!entries.length) lines.push('No saved observations to display.');
  entries.slice(0, MAX_ROWS).forEach((entry, index) => {
    const record = entry ?? {};
    const status = STATUSES.has(record.status) ? record.status : 'unknown';
    lines.push('', `${index + 1}. ${text(record.title) || 'Untitled chat'}`,
      `ID: ${text(record.id) || 'unknown'}`,
      `Host: ${text(record.hostId) || 'unknown'} | Provider: ${text(record.kind) || 'unknown'}`,
      `CACHED SNAPSHOT | Recorded: ${status}`,
      `Observed: ${text(record.observedAt) || 'unknown'}`,
      timeNotice(record.observedAt, options));
    if (record.held === true) lines.push('HOLD RECORDED - no release inferred.');
    if (record.reportedActive === true) lines.push('ACTIVITY FLAG RECORDED - not a current check.');
  });
  const suppliedTotal = Number.isSafeInteger(collection.total) && collection.total >= entries.length
    ? collection.total : entries.length;
  const shown = Math.min(MAX_ROWS, entries.length);
  if (shown < suppliedTotal || collection.truncated === true) {
    lines.push(`Showing ${shown} of ${suppliedTotal} known entries; filter for the exact ID.`);
  }
  const footer = [];
  if (collection.cache?.status === 'unavailable') footer.push('Snapshot save failed; persistence of refreshed rows is unconfirmed.');
  if (Array.isArray(collection.observations) && collection.observations.some(item => item?.status === 'unavailable')) {
    footer.push('Provider metadata unavailable; displayed rows may be older.');
  }
  return renderFrame({ title: 'CHAT OBSERVATIONS', lines, footer }, options);
}

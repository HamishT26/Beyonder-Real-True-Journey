import test from 'node:test';
import assert from 'node:assert/strict';
import { stripVTControlCharacters } from 'node:util';
import { renderFrame, renderMenu, renderChatPanel } from './terminal-presentation.mjs';

const NOW = Date.parse('2026-10-07T05:20:00.000Z');
const ID = '00000000-0000-4000-8000-000000000041';
const OPTIONS = { columns: 80, plain: true, nowMs: NOW };
const record = overrides => ({ id: ID, title: 'Example saved chat', hostId: 'local',
  kind: 'codex-local', status: 'idle', observedAt: '2026-10-07T05:19:00.000Z', ...overrides });
const menu = { title: 'NEXUS', items: [{ key: 'A', label: 'App' }, { key: 'D', label: 'CMD' }] };
const words = output => stripVTControlCharacters(output).split('\n')
  .map(line => line.replace(/^[|│] /u, '').replace(/ [|│]$/u, '').trim())
  .join(' ').replace(/\s+/gu, ' ');

test('ASCII menu has the reviewed fixed-width layout', () => {
  assert.equal(renderMenu(menu, { columns: 24, plain: true }), [
    '+----------------------+',
    '| NEXUS                |',
    '+----------------------+',
    '| [A] App              |',
    '| [D] CMD              |',
    '+----------------------+',
  ].join('\n'));
});

test('neon uses only cyan/magenta/reset and preserves plain text', () => {
  const base = { columns: 40, tty: true, ascii: true };
  const colored = renderMenu(menu, base);
  assert.match(colored, /\x1b\[36m/);
  assert.match(colored, /\x1b\[35m/);
  assert.equal(stripVTControlCharacters(colored), renderMenu(menu, { ...base, color: false }));
  assert.ok([...colored.matchAll(/\x1b\[([^m]+)m/g)].every(match => ['0', '35', '36'].includes(match[1])));
});

test('NO_COLOR presence wins over requested color and FORCE_COLOR', () => {
  for (const value of ['', '0', '1']) {
    const view = renderMenu(menu, { tty: true, color: true, env: { NO_COLOR: value, FORCE_COLOR: '1' } });
    assert.doesNotMatch(view, /\x1b/);
  }
});

test('non-TTY output is plain ASCII even if color or Unicode was requested', () => {
  const view = renderMenu({ ...menu, title: 'Café 界 🚀' }, { tty: false, color: true, ascii: false });
  assert.doesNotMatch(view, /[^\x20-\x7e\n]/u);
  assert.match(view, /Cafe/);
});

test('TERM=dumb and explicit plain mode each disable color and Unicode borders', () => {
  for (const options of [{ tty: true, env: { TERM: 'dumb' } }, { tty: true, plain: true }]) {
    const view = renderMenu(menu, options);
    assert.doesNotMatch(view, /[^\x20-\x7e\n]/u);
    assert.ok(view.startsWith('+'));
  }
});

test('ASCII rows are rectangular across tiny, narrow, normal and capped widths', () => {
  for (const columns of [1, 2, 3, 4, 5, 6, 8, 16, 23, 24, 25, 40, 79, 80, 120, 160, 200]) {
    const view = renderChatPanel({ entries: [record({ title: 'Long title '.repeat(25) })] }, { ...OPTIONS, columns });
    for (const line of view.split('\n')) assert.equal(line.length, Math.min(columns, 160), `columns=${columns}`);
  }
});

test('unusable narrow panels ask for resize instead of showing misleading partial chat state', () => {
  const view = words(renderChatPanel({ entries: [record()] }, { ...OPTIONS, columns: 20 }));
  assert.match(view, /RESIZE/);
  assert.match(view, /Widen terminal to 24 columns/);
  assert.doesNotMatch(view, /Recorded: idle/);
});

test('common CJK and emoji graphemes wrap at cell boundaries', () => {
  const cjk = renderFrame({ title: 'A', lines: ['界'.repeat(11)] }, { columns: 24, tty: true, color: false });
  assert.ok(cjk.split('\n').includes('│ ' + '界'.repeat(10) + ' │'));
  assert.ok(cjk.split('\n').includes('│ 界' + ' '.repeat(19) + '│'));
  const emoji = renderFrame({ title: 'A', lines: ['👩‍💻'.repeat(11)] }, { columns: 24, tty: true, color: false });
  assert.ok(emoji.split('\n').includes('│ ' + '👩‍💻'.repeat(10) + ' │'));
  assert.equal((emoji.match(/👩‍💻/gu) || []).length, 11);
});

test('combining clusters stay intact; isolated marks and invisible controls cannot alter borders', () => {
  const view = renderFrame({ title: 'A', lines: ['e\u0301'.repeat(21), '\u0301', 'one\u200btwo\u202ethree'] },
    { columns: 24, tty: true, color: false });
  assert.ok(view.split('\n').includes('│ ' + 'e\u0301'.repeat(20) + ' │'));
  assert.doesNotMatch(view, /[\u200b\u202e]/u);
  assert.ok(view.includes('│ ?'));
});

test('full ID and host remain recoverable through narrow wrapping', () => {
  const host = 'a-long-distinct-host-name';
  const view = words(renderChatPanel({ entries: [record({ hostId: host })] }, { ...OPTIONS, columns: 24 }));
  assert.ok(view.replaceAll(' ', '').includes(ID));
  assert.ok(view.replaceAll(' ', '').includes(host));
});

test('fresh idle, ready and notLoaded are always recorded snapshots, never live admission', () => {
  for (const status of ['idle', 'ready', 'notLoaded']) {
    const view = words(renderChatPanel({ entries: [record({ status })] }, OPTIONS));
    assert.match(view, /CACHED SNAPSHOT \| Recorded:/);
    assert.ok(view.includes(`Recorded: ${status}`));
    assert.match(view, /RECENT SNAPSHOT \/ age 1m/);
    assert.match(view, /not live state or resume permission/);
  }
});

test('stale observations retain their recorded status with an explicit stale notice', () => {
  const view = words(renderChatPanel({ entries: [record({ observedAt: '2026-10-07T04:20:00.000Z' })] }, OPTIONS));
  assert.match(view, /CACHED SNAPSHOT \| Recorded: idle/);
  assert.match(view, /STALE \/ age 1h/);
});

test('missing, malformed, calendar-invalid and non-UTC observation times make no recency claim', () => {
  for (const observedAt of [undefined, 'yesterday', '2026-02-30T00:00:00.000Z', '2026-10-07T05:19:00+00:00']) {
    const view = words(renderChatPanel({ entries: [record({ observedAt })] }, OPTIONS));
    assert.match(view, /UNKNOWN TIME/);
    assert.doesNotMatch(view, /RECENT SNAPSHOT \/ age/);
  }
});

test('future timestamps and absent caller clock are distinct from current status', () => {
  assert.match(words(renderChatPanel({ entries: [record({ observedAt: '2026-10-07T06:00:00.000Z' })] }, OPTIONS)), /FUTURE TIME/);
  assert.match(words(renderChatPanel({ entries: [record()] }, { plain: true })), /AGE NOT EVALUATED/);
});

test('stale threshold is display-only and preserves its documented boundary', () => {
  const collection = { entries: [record()] };
  assert.match(words(renderChatPanel(collection, { ...OPTIONS, staleAfterMs: 60000 })), /RECENT SNAPSHOT/);
  assert.match(words(renderChatPanel(collection, { ...OPTIONS, staleAfterMs: 59999 })), /STALE \/ age 1m/);
  assert.match(words(renderChatPanel(collection, { ...OPTIONS, staleAfterMs: 59999 })), /Recorded: idle/);
});

test('stored holds and activity flags remain visible regardless of recorded idle status', () => {
  const view = words(renderChatPanel({ entries: [record({ held: true, reportedActive: true })] }, OPTIONS));
  assert.match(view, /HOLD RECORDED - no release inferred/);
  assert.match(view, /ACTIVITY FLAG RECORDED - not a current check/);
});

test('provider or snapshot failures remain visible alongside cached rows', () => {
  const view = words(renderChatPanel({ entries: [record()], cache: { status: 'unavailable' },
    observations: [{ status: 'unavailable' }] }, OPTIONS));
  assert.match(view, /Snapshot save failed/);
  assert.match(view, /Provider metadata unavailable/);
  assert.match(view, /CACHED SNAPSHOT/);
});

test('input terminal escapes and control sequences cannot become commands or extra rows', () => {
  const malicious = '\x1b[2Jtitle\x1b]52;c;PAYLOAD\x07\r\n\x1b[31mred\x1b[0m';
  const view = renderMenu({ title: malicious, items: [{ key: '1', label: malicious }] }, { plain: true });
  assert.doesNotMatch(view, /\x1b|\r|\x07|PAYLOAD/);
  assert.equal(view.split('\n').length, 5);
  assert.match(view, /title red/);
});

test('only selected summary fields are shown; unknown statuses have no implied meaning', () => {
  const view = renderChatPanel({ entries: [record({ status: 'LIVE_AND_AUTHORIZED', history: 'HIDDEN-HISTORY',
    preview: 'HIDDEN-PREVIEW', apiKey: 'HIDDEN-KEY', source: 'LIVE VERIFIED' })] }, OPTIONS);
  assert.doesNotMatch(view, /HIDDEN-|LIVE VERIFIED|LIVE_AND_AUTHORIZED/);
  assert.match(view, /Recorded: unknown/);
});

test('oversize text, entries and rendered height are bounded with visible notices', () => {
  const entries = Array.from({ length: 101 }, () => record({ title: 'z'.repeat(10000) }));
  const view = renderChatPanel({ entries, total: 105 }, { ...OPTIONS, columns: 24 });
  assert.ok(view.split('\n').length < 1100);
  assert.match(words(view), /Display limit reached/);
  assert.match(words(view), /\[clipped\]/);
  const short = words(renderChatPanel({ entries: [record()], total: 10, truncated: true }, OPTIONS));
  assert.match(short, /Showing 1 of 10 known entries/);
});

test('renders are deterministic and do not mutate frozen records, arrays or options', () => {
  const item = Object.freeze(record());
  const collection = Object.freeze({ entries: Object.freeze([item]) });
  const options = Object.freeze({ ...OPTIONS, env: Object.freeze({ NO_COLOR: '' }) });
  const before = JSON.stringify({ collection, options });
  assert.equal(renderChatPanel(collection, options), renderChatPanel(collection, options));
  assert.equal(JSON.stringify({ collection, options }), before);
});

test('empty collections and invalid widths have explicit bounded output', () => {
  assert.match(words(renderChatPanel({}, OPTIONS)), /No saved observations/);
  assert.match(words(renderMenu({}, OPTIONS)), /No menu items/);
  for (const columns of [0, -1, NaN, Infinity, '80']) {
    assert.ok(renderMenu(menu, { columns, plain: true }).split('\n').every(line => line.length === 80));
  }
});

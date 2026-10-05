const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const code = fs.readFileSync(path.join(__dirname, '../website/docs/javascripts/comparison.js'), 'utf8');
function load(storage = new Map(), unavailable = false) {
  const context = {window: {}, document: {querySelectorAll: () => [], querySelector: () => null}, sessionStorage: {
    getItem: k => {if (unavailable) throw Error('blocked'); return storage.get(k) || null;},
    setItem: (k, v) => {if (unavailable) throw Error('blocked'); storage.set(k, v);},
  }};
  vm.runInNewContext(code, context);
  return context.window.DexTrailCompare;
}
const plain = value => JSON.parse(JSON.stringify(value));
test('selection and technical view survive a page navigation', () => {
  const storage = new Map();
  load(storage).save({ids: ['shadow-hand', 'leap-hand'], view: 'software', differences: true});
  assert.deepEqual(plain(load(storage).read()), {ids: ['shadow-hand', 'leap-hand'], view: 'software', differences: true});
});
test('adding a fourth hand never silently removes an existing selection', () => {
  const api = load(); const state = {ids: ['shadow-hand', 'leap-hand', 'allegro-v4'], view: 'mechanics'};
  const result = api.add(state, 'wuji-hand-2');
  assert.equal(result.result, 'full'); assert.deepEqual(plain(result.state.ids), state.ids);
  assert.equal(api.add(state, 'leap-hand').result, 'present');
});
test('append preserves the view, order and explicit empty selection', () => {
  const api = load(); api.save({ids: ['shadow-hand'], view: 'sensing', differences: true});
  api.save(api.add(api.read(), 'leap-hand').state);
  assert.deepEqual(plain(api.read().ids), ['shadow-hand', 'leap-hand']);
  assert.equal(api.read().view, 'sensing');
  api.save({ids: [], view: 'sensing'}); assert.deepEqual(plain(api.read().ids), []);
});
test('corrupt or blocked session storage does not break detail pages', () => {
  const storage = new Map([['dextrail-comparison:v2', '{broken']]);
  assert.deepEqual(plain(load(storage).read().ids), []);
  const blocked = load(new Map(), true);
  assert.deepEqual(plain(blocked.read().ids), []);
  assert.equal(blocked.save({ids: ['leap-hand']}).ids.length, 1);
});
test('invalid ids, duplicates and unsupported view values are sanitized', () => {
  const api = load();
  const clean = api.save({ids: ['leap-hand', 'leap-hand', '../bad', null], view: '__proto__'});
  assert.deepEqual(plain(clean.ids), ['leap-hand']); assert.equal(clean.view, 'all');
  assert.equal(api.add(clean, '../bad').result, 'invalid');
});

const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const context = {window: {}, document: {querySelector: () => null}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../website/docs/javascripts/algorithm-atlas.js'), 'utf8'), context);
const {matches} = context.window.DexTrailAlgorithms;
const catalog = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/algorithm-atlas.json'), 'utf8'));
const filter = selection => catalog.cases.filter(item => matches({problems: Object.keys(item.problems), methods: Object.keys(item.methods)}, selection)).map(item => item.id);

test('problem and method intersect across actual sourced cases', () => {
  assert.deepEqual(filter({problems: 'perception-and-state', methods: 'generative-models'}), ['pp-tac']);
  assert.deepEqual(filter({problems: 'retargeting', methods: 'imitation-learning'}), ['dexmv']);
  assert.deepEqual(filter({problems: 'identification-and-adaptation', methods: 'reinforcement-learning'}), ['hora']);
});

test('uncollected combinations stay empty and clearing restores all cases', () => {
  assert.deepEqual(filter({problems: 'retargeting', methods: 'probabilistic-inference'}), []);
  assert.deepEqual(filter({problems: 'unknown', methods: ''}), []);
  assert.equal(filter({problems: '', methods: ''}).length, catalog.cases.length);
});

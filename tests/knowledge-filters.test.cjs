const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const context = {window: {}, document: {querySelector: () => null}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../website/docs/javascripts/knowledge-filters.js'), 'utf8'), context);
const {matches} = context.window.DexTrailTopics;
const groups = {academic: 'record', industry: 'record', tactile: 'sensing', learning: 'control'};

test('topic selection allows alternatives within a group and intersects distinct groups', () => {
  const tags = ['academic', 'tactile'];
  assert.equal(matches(tags, [], groups), true);
  assert.equal(matches(tags, ['academic', 'industry'], groups), true);
  assert.equal(matches(tags, ['industry', 'tactile'], groups), false);
  assert.equal(matches(tags, ['academic', 'industry', 'tactile'], groups), true);
  assert.equal(matches(tags, ['academic', 'tactile', 'learning'], groups), false);
});

test('an unknown topic cannot silently broaden results', () => {
  assert.equal(matches(['academic'], ['academic', 'unknown'], groups), false);
  assert.equal(matches(['academic'], ['__proto__'], groups), false);
});

function historyFixture() {
  const listeners = {}, frames = [];
  const element = dataset => ({dataset, hidden: false, attributes: {},
    setAttribute(key, value) {this.attributes[key] = value;},
    removeAttribute(key) {delete this.attributes[key];},
    addEventListener(key, fn) {this[key] = fn;}});
  const items = ['academic kinematics', 'industry', 'industry teleoperation'].map(tags => element({topicTags: tags}));
  const years = ['1982', '2025', '2026'].map((year, index) => ({...element({historyYear:year}), top:[50,900,1800][index],
    getBoundingClientRect() {return {top:this.top};}, querySelectorAll:() => [items[index]]}));
  const links = years.map(row => ({...element({historyLink:row.dataset.historyYear}),
    getBoundingClientRect:() => ({top:20, bottom:50})}));
  const nav = {hidden:false, scrollTop:0, querySelectorAll:() => links, getBoundingClientRect:() => ({top:0,bottom:200})};
  const controls = [['academic','record'], ['industry','record'], ['kinematics','mechanics']].map(([topicTag,topicGroup]) => element({topicTag,topicGroup}));
  const clear = element({}), summary = {}, empty = {hidden:true}, yearEmpty = {hidden:true}, timeline = {};
  const page = {querySelectorAll:selector => selector === '[data-topic-item]' ? items : selector === '[data-topic-tag]' ? controls : years,
    querySelector:selector => ({'.history-scroll':timeline,'.knowledge-filter-empty':empty})[selector] || null};
  const rail = {dataset:{topicMode:'history',topicUnit:'个节点'}, closest:() => page,
    querySelectorAll:() => controls,
    querySelector:selector => ({'.history-year-nav':nav,'.history-year-empty':yearEmpty,
      '.dex-filter-result':summary,'[data-topic-clear]':clear})[selector] || null};
  const fixture = {window:{addEventListener:(name,fn) => {listeners[name]=fn;}}, document:{querySelector:() => rail},
    URLSearchParams, location:{search:''}, requestAnimationFrame:fn => frames.push(fn), ResizeObserver:class {observe() {}}};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../website/docs/javascripts/knowledge-filters.js'), 'utf8'), fixture);
  const flush = () => {while (frames.length) frames.shift()();};
  flush();
  return {years,links,controls,clear,nav,yearEmpty,timeline,flush,listeners};
}

test('scroll highlights the containing year, including long years and upward scroll', () => {
  const h = historyFixture();
  const active = () => h.links.filter(link => link.attributes['aria-current'] === 'location').map(link => link.dataset.historyLink);
  assert.deepEqual(active(), ['1982']);
  h.years[0].top = -900; h.years[1].top = -200; h.years[2].top = 700;
  h.listeners.scroll(); h.flush(); assert.deepEqual(active(), ['2025']);
  h.years[2].top = 80;
  h.listeners.scroll(); h.flush(); assert.deepEqual(active(), ['2026']);
  h.years[1].top = 800; h.years[2].top = 1700;
  h.listeners.scroll(); h.flush(); assert.deepEqual(active(), ['1982']);
});

test('filtering removes empty years, clears an empty current year, and restores navigation', () => {
  const h = historyFixture();
  h.controls[1].click(); h.flush();
  assert.deepEqual(h.links.map(link => link.hidden), [true,false,false]);
  assert.equal(h.links[1].attributes['aria-current'], 'location');
  h.controls[2].click(); h.flush();
  assert.equal(h.nav.hidden, true); assert.equal(h.yearEmpty.hidden, false);
  assert.equal(h.links.some(link => link.attributes['aria-current']), false);
  h.clear.click(); h.flush();
  assert.equal(h.nav.hidden, false); assert.equal(h.yearEmpty.hidden, true);
  assert.deepEqual(h.links.map(link => link.hidden), [false,false,false]);
  assert.equal(h.links[0].attributes['aria-current'], 'location');
});

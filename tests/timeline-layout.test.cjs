const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const context = {window:{}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../website/docs/javascripts/timeline-layout.js'),'utf8'),context);
const timeline = context.window.DexTrailTimeline;
const hand = (id, year, dof, actuators, fingers, transmission) => ({
  id, name:id, coordinates:{year,dof,actuators}, classification:{fingers,transmission},
});
const entries = [hand('a',2025,16,16,4,'geared-drive'),hand('b',2025,null,null,null,null),
  hand('c',2026,5,2,5,'tendon-driven'),hand('d',null,22,22,5,'tendon-driven')];

test('every dated hand appears exactly once in every view, including unknown parameters',()=>{
  for(const view of ['transmission','dof','fingers','actuators','mobility']) {
    const layout=timeline.build(entries,entries,view);
    assert.deepEqual([...layout.cells.values()].flat().map(h=>h.id).sort(),['a','b','c']);
    assert.deepEqual(Array.from(layout.missing,h=>h.id),['d']);
    assert.equal(layout.cells.get('unknown|2025')[0].id,'b');
  }
});
test('year columns retain evidence dates, while filtering removes only matching records',()=>{
  const layout=timeline.build(entries,[entries[0]],'transmission');
  assert.deepEqual(Array.from(layout.years),[2025,2026]);
  assert.equal(layout.cells.get('geared-drive|2025')[0].id,'a');
  assert.equal(layout.rows.length,1);
  assert.equal(layout.missing.length,0);
  const empty=timeline.build(entries,[],'dof');
  assert.equal(empty.cells.size,0);assert.equal(empty.rows.length,0);
});
test('active axes, actuators and fingers keep separate meanings and stable category order',()=>{
  assert.equal(timeline.groupKey(entries[0],'dof'),'4');
  assert.equal(timeline.groupKey(entries[0],'mobility'),'16');
  assert.equal(timeline.groupKey(entries[2],'actuators'),'2');
  assert.equal(timeline.groupKey(entries[2],'fingers'),'5');
  const rows=timeline.categories(entries,'mobility');
  assert.deepEqual(Array.from(rows,row=>row[0]),['5','16','22','unknown']);
  assert.equal(rows[0][1],'5 主动轴');
});

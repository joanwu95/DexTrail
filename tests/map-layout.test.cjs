const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const context={window:{}};
vm.runInNewContext(fs.readFileSync(require('node:path').join(__dirname,'../website/docs/javascripts/map-layout.js'),'utf8'),context);
const layout=context.window.DexTrailMapLayout;

test('same-date products remain individual and become separated when zoomed',()=>{
  const points=Array.from({length:30},(_,i)=>({id:`hand-${String(i).padStart(2,'0')}`,x:150,y:2.5}));
  const offsets=layout.offsets(points,{grouped:true,rowHeight:68});
  assert.equal(offsets.size,points.length);
  const sorted=[...offsets.values()].sort((a,b)=>a-b);
  assert.ok(sorted[1]-sorted[0]<layout.size(1).height);
  for(let i=1;i<sorted.length;i++)assert.ok((sorted[i]-sorted[i-1])*layout.MAX_ZOOM>layout.size(layout.MAX_ZOOM).height);
  assert.ok(sorted.every(offset=>Math.abs(offset)<68/2));
  assert.ok(points.every(point=>point.x===150 && point.y===2.5));
});

test('lanes stay stable across input order and do not depend on camera or zoom',()=>{
  const points=[{id:'a',x:10,y:1.5},{id:'b',x:10,y:1.5},{id:'c',x:100,y:1.5},{id:'d',x:10,y:3.5}];
  const a=layout.offsets(points,{grouped:true,rowHeight:68});
  const b=layout.offsets([...points].reverse(),{grouped:true,rowHeight:68});
  for(const point of points)assert.equal(a.get(point.id),b.get(point.id));
  assert.notEqual(a.get('a'),a.get('b'));
  assert.equal(a.get('a'),a.get('c'));
  assert.equal(a.get('d'),0);
});

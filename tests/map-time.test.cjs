const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const context={window:{}};
for(const file of ['map-time','name-layout'])vm.runInNewContext(fs.readFileSync(`${__dirname}/../website/docs/javascripts/${file}.js`,'utf8'),context);
const time=context.window.DexTrailMapTime, layout=context.window.DexTrailNameLayout;

test('documented months order same-year products without changing the evidence relation',()=>{
  const jan=time.point({timeline:{year:2025,month:1,relation:'by'}});
  const dec=time.point({timeline:{year:2025,month:12,relation:'event'}});
  assert.ok(jan.value<dec.value);
  assert.equal(jan.upperBound,true);
  assert.equal(dec.upperBound,false);
  assert.equal(jan.precision,'month');
});
test('unknown months do not come from verification dates or incidental prose',()=>{
  const point=time.point({timeline:{year:2026,verified_on:'2026-10-04',detail:'Earlier prototype 2025-03-31'}});
  assert.equal(point.value,2026.5);
  assert.equal(point.month,null);
  assert.equal(point.precision,'year');
  assert.equal(time.point({coordinates:{year:null}}),null);
});
test('tick detail increases from years to quarters to months, including year boundaries',()=>{
  assert.ok(time.ticks(2025,2027,40).every(t=>/^\d{4}$/.test(t.label)));
  assert.ok(time.ticks(2025,2026,350).some(t=>t.label==='04月'));
  const ticks=time.ticks(2025,2026,1200);
  assert.equal(ticks.length,13);
  assert.equal(ticks[0].label,'2025');
  assert.equal(ticks[12].label,'2026');
});
test('coincident products retain distinct names and stable lanes without moving dates',()=>{
  const points=Array.from({length:25},(_,i)=>({id:`hand-${String(i).padStart(2,'0')}`,x:450,key:'tendon',width:95}));
  const result=layout.pack(points,['tendon','unknown'],{left:100,right:500});
  const reverse=layout.pack([...points].reverse(),['tendon','unknown'],{left:100,right:500});
  assert.equal(result.positions.size,25);
  const offsets=[...result.positions.values()].map(p=>p.offset).sort((a,b)=>a-b);
  for(let i=1;i<offsets.length;i++)assert.ok(offsets[i]-offsets[i-1]>=19);
  for(const p of points){assert.equal(p.x,450);assert.equal(result.positions.get(p.id).offset,reverse.positions.get(p.id).offset);}
  assert.equal(result.positions.get('hand-00').side,'left');
});
test('numerical anchors stay exact while dense labels get readable positions',()=>{
  const points=Array.from({length:40},(_,i)=>({id:`hand-${i}`,start:500,width:120,value:16+(i%3),max:40}));
  const result=layout.numeric(points);
  assert.equal(result.positions.size,40);
  const labels=[...result.positions.values()].map(p=>p.center).sort((a,b)=>a-b);
  for(let i=1;i<labels.length;i++)assert.ok(labels[i]-labels[i-1]>=18);
  for(const p of points)assert.equal(result.positions.get(p.id).anchor,24+p.value/p.max*(result.height-48));
});
test('empty categories do not reserve space below the products',()=>{
  const point={id:'one',key:'tendon',x:150,width:80};
  const layoutResult=layout.pack([point],['direct','tendon','unknown'],{left:100,right:500});
  assert.equal(layoutResult.bands.length,1);
  assert.equal(layoutResult.height,52);
  assert.equal(layoutResult.positions.size,1);
  assert.equal(layout.pack([],['unknown'],{left:100,right:500}).height,0);
});
test('the camera cannot pan the coordinate plane away or zoom below its fitted extent',()=>{
  const small=layout.camera({k:.65,x:-400,y:-800},900,600);
  assert.equal(small.k,1);assert.equal(small.x,0);assert.equal(small.y,0);
  const large=layout.camera({k:3,x:-3000,y:-700},900,600);
  assert.equal(large.x,-1800);assert.equal(large.y,0);
  const other=layout.camera({k:3,x:900,y:4000},900,600);
  assert.equal(other.x,0);assert.equal(other.y,1200);
});

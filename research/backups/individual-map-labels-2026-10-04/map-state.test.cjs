const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const code = fs.readFileSync(path.join(__dirname, '../website/docs/javascripts/map-state.js'), 'utf8');
const allowed = {views:['dof','transmission','fingers','actuators','mobility'], tags:new Set(['five-fingers','tendon-driven']), hands:new Set(['shadow-hand','leap-hand'])};
const key = 'dextrail-map:time-x-v2:/';
const initial = () => ({view:'fingers',query:'Shadow',tags:['five-fingers'],k:1.82,x:-.16,y:.08,expanded:['shadow-hand'],pending:true,scrollY:130,listScroll:240});
const plain = value => JSON.parse(JSON.stringify(value));
function load(storage = new Map(), unavailable = false) {
  const context = {window:{},sessionStorage:{
    getItem:k=>{if(unavailable)throw Error('blocked');return storage.get(k)??null;},
    setItem:(k,v)=>{if(unavailable)throw Error('blocked');storage.set(k,v);},
  }};
  vm.runInNewContext(code,context);
  return context.window.DexTrailMapState;
}
test('returning from a detail page retains filters, view, camera and expanded records',()=>{
  const storage=new Map();load(storage).save(key,initial(),allowed);
  assert.deepEqual(plain(load(storage).read(key,allowed)),initial());
});
test('corrupt JSON and unavailable storage never prevent map initialization',()=>{
  assert.equal(load(new Map([[key,'{broken']])).read(key,allowed),null);
  const blocked=load(new Map(),true);
  assert.equal(blocked.read(key,allowed),null);
  assert.deepEqual(plain(blocked.save(key,initial(),allowed)),initial());
});
test('a stale collection removes unknown and duplicate tags or expanded records',()=>{
  const saved={...initial(),tags:['five-fingers','removed-tag','five-fingers',null],expanded:['shadow-hand','deleted-hand','shadow-hand',42]};
  const storage=new Map([[key,JSON.stringify(saved)]]);
  const result=load(storage).read(key,allowed);
  assert.deepEqual(plain(result.tags),['five-fingers']);
  assert.deepEqual(plain(result.expanded),['shadow-hand']);
  assert.equal(result.query,'Shadow');assert.equal(result.k,1.82);
});
test('malformed lists are ignored instead of throwing during tag restoration',()=>{
  const state=load().clean({...initial(),tags:{bad:true},expanded:'shadow-hand'},allowed);
  assert.deepEqual(plain(state.tags),[]);assert.deepEqual(plain(state.expanded),[]);
});
test('invalid views and nonfinite or unsupported zoom values cannot enter the renderer',()=>{
  const api=load();
  for(const bad of [{view:'__proto__'},{query:null},{k:0},{k:8},{k:NaN},{x:Infinity},{y:'12'}])
    assert.equal(api.clean({...initial(),...bad},allowed),null);
  const state=api.clean({...initial(),scrollY:-4,listScroll:Infinity,pending:'true'},allowed);
  assert.equal(state.scrollY,0);assert.equal(state.listScroll,0);assert.equal(state.pending,false);
});
test('maps deployed under different base paths keep independent exploration states',()=>{
  const storage=new Map();const api=load(storage);
  api.save(key,initial(),allowed);
  const other='dextrail-map:time-x-v2:/atlas/';
  assert.equal(api.read(other,allowed),null);
  api.save(other,{...initial(),view:'transmission',query:'LEAP'},allowed);
  assert.equal(api.read(key,allowed).query,'Shadow');
  assert.equal(api.read(other,allowed).query,'LEAP');
});

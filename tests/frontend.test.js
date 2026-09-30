const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../services/frontend/src/app.js'), 'utf8');
const tick = () => new Promise(resolve => setImmediate(resolve));
function setup(request) {
  const elements = {output:{value:''}, content:{value:'Madam and cloud'}};
  const messages = [];
  const context = vm.createContext({
    AbortController, console:{log(){}, error(){}},
    document:{getElementById:id=>elements[id]}, alert:x=>messages.push(x),
    prompt:()=> 'demo', setInterval(){},
    fetch: async (url, options) => url === 'config.json'
      ? {ok:true,json:async()=>({proxy_url:'/api/count',savepost_url:'/api/text',monitor_url:'/api/monitor'})}
      : request(url, options)
  });
  vm.runInContext(source, context);
  return {context, elements, messages};
}
test('cancels old fetch and prevents late response from overwriting latest result',async()=>{
  const pending=[];
  const {context,elements,messages}=setup((url,options)=>new Promise(resolve=>pending.push({resolve,options})));
  const first=context.fetchData('wordcount','old');
  await tick();
  const second=context.fetchData('wordcount','new');
  await tick();
  assert.equal(pending[0].options.signal.aborted,true);
  pending[1].resolve({ok:true,json:async()=>({answer:2})});
  await second;
  pending[0].resolve({ok:true,json:async()=>({answer:99})});
  await first;
  assert.equal(elements.output.value,2);
  assert.equal(messages.length,0);
});
test('offline and error status stay visible',async()=>{
  const {context,messages}=setup(async()=>({ok:true,json:async()=>({a:{status:'Offline'},b:{status:'Error'}})}));
  await context.checkServices();
  assert.match(messages[0],/a: Offline/);
  assert.match(messages[0],/b: Error/);
});
test('shows backend storage error instead of assuming duplicate ID',async()=>{
  const {context,elements}=setup(async()=>({ok:false,json:async()=>({error:'A JSON object is required'})}));
  await context.saveText();
  assert.equal(elements.output.value,'A JSON object is required');
});

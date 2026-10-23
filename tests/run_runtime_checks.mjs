// Optional integration check: node tests/run_runtime_checks.mjs /path/to/pyodide-package
import {Worker} from 'node:worker_threads';
import {execFileSync} from 'node:child_process';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';

const root=fileURLToPath(new URL('../',import.meta.url));
const runtime=process.argv[2];
if(!runtime)throw new Error('Provide the installed pyodide@314.0.7 package directory.');
const cases=JSON.parse(execFileSync(process.env.BECOMING_TEST_PYTHON||'python',[
  '-c', 'import json; from coding import CHALLENGES; from coding_runner import runner_config; print(json.dumps([{**runner_config(c,c["solution"]),"runChecks":True} for c in CHALLENGES if c["extension"] in ["py","sql"]]))'
],{cwd:root,encoding:'utf8'}));
let source=await readFile(new URL('../components/coding_runner/worker.mjs',import.meta.url),'utf8');
source=source.replace('https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs',pathToFileURL(resolve(runtime,'pyodide.mjs')).href)
  .replace("indexURL:'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/'",'indexURL:'+JSON.stringify(resolve(runtime)+'/'));
const adapter="import {parentPort} from 'node:worker_threads'; globalThis.self={postMessage:value=>parentPort.postMessage(value)}; parentPort.on('message',data=>self.onmessage({data}));\n"+source;
const worker=new Worker(new URL('data:text/javascript;charset=utf-8,'+encodeURIComponent(adapter)),{type:'module'});
function run(config) {
  return new Promise((resolve,reject)=>{
    const timeout=setTimeout(()=>{cleanup();reject(new Error('Runtime test timed out'));},60000);
    function cleanup(){clearTimeout(timeout);worker.off('message',onMessage);worker.off('error',onError);}
    function onMessage(data){if(data.type==='result'){cleanup();resolve(data);}}
    function onError(error){cleanup();reject(error);}
    worker.on('message',onMessage);worker.on('error',onError);worker.postMessage(config);
  });
}
try {
  for(const config of cases){const result=await run(config);assert.equal(result.ok,true,config.challengeId+': '+result.output);console.log('PASS',config.challengeId);}
  const broken=await run({language:'python',code:'def broken(:',runChecks:false});
  assert.equal(broken.ok,false);assert.match(broken.output,/SyntaxError/);console.log('PASS syntax error output');
  await run({language:'python',code:'private_to_this_run=42',runChecks:false});
  const isolated=await run({language:'python',code:'print(private_to_this_run)',runChecks:false});
  assert.equal(isolated.ok,false);assert.match(isolated.output,/NameError/);console.log('PASS fresh namespace');
  await new Promise((resolve,reject)=>{
    const timeout=setTimeout(()=>reject(new Error('Missing execution event')),10000);
    worker.once('message',data=>{clearTimeout(timeout);data.type==='executing'?resolve():reject(new Error('Missing execution event'));});
    worker.postMessage({language:'python',code:'while True: pass',runChecks:false});
  });
  await worker.terminate();console.log('PASS runaway execution terminates');
}finally{await worker.terminate();}

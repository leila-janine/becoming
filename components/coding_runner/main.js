'use strict';
const byId = id => document.getElementById(id);
const source=byId('source'), output=byId('output'), status=byId('status');
let config={challengeId:'playground',language:'python',code:'print("Hello, Leila!")\n',starter:'print("Hello, Leila!")\n',checks:'',setup:'',expected:null};
let mounted=false, worker=null, busy=false, deadline=null, runWithChecks=false, submittedCode='';
function message(type,body={}) {window.parent.postMessage({isStreamlitMessage:true,type,...body},'*');}
function resize() {message('streamlit:setFrameHeight',{height:Math.ceil(document.documentElement.getBoundingClientRect().height)+2});}
function value(state,code=source.value) {message('streamlit:setComponentValue',{dataType:'json',value:{code,status:state,revision:Date.now()+'-'+Math.random().toString(36).slice(2)}});}
function setBusy(state) {busy=state;byId('run').disabled=state;byId('checks').disabled=state||!(config.checks||config.expected);byId('stop').disabled=!state;}
function endWorker() {if(worker)worker.terminate();worker=null;clearTimeout(deadline);setBusy(false);}
function stop(text='Stopped. Your code is still in the editor.') {endWorker();status.textContent=text;value('stopped',submittedCode||source.value);resize();}
function arm(ms,text) {clearTimeout(deadline);deadline=setTimeout(()=>stop(text),ms);}
function run(checks=false) {
  if(busy)return;
  if(source.value.length>30000) {status.textContent='Keep this practice script under 30,000 characters.';return;}
  submittedCode=source.value;runWithChecks=checks;setBusy(true);output.textContent='';status.textContent='Loading the browser runtime…';
  arm(90000,'Runtime loading timed out. Check your connection and try again.');
  if(!worker) {
    worker=new Worker(new URL('./worker.mjs',window.location.href),{type:'module'});
    worker.onmessage=event=>{
      const data=event.data;
      if(data.type==='executing') {status.textContent='Running '+(runWithChecks?'code and checks':'code')+'…';arm(10000,'Time limit reached (10 seconds). Check for a loop, then run again.');return;}
      if(data.type==='result') {
        clearTimeout(deadline);setBusy(false);
        output.textContent=String(data.output||'Finished without printed output.').slice(0,22000);
        status.textContent=data.ok?(runWithChecks?'Checks passed for the supplied examples.':'Run complete.'):'Run failed. Read the error below and try one change.';
        value(data.ok?(runWithChecks?'passed':'ran'):'failed',submittedCode);resize();
      }
    };
    worker.onerror=()=>{endWorker();output.textContent='The runtime could not load or stopped unexpectedly. Check your connection and retry. Your draft has not been removed.';status.textContent='Runtime unavailable.';value('failed',submittedCode);resize();};
  }
  worker.postMessage({...config,code:submittedCode,runChecks:checks});
}
byId('run').onclick=()=>run(false);byId('checks').onclick=()=>run(true);byId('stop').onclick=()=>stop();
byId('draft').onclick=()=>{if(source.value.length>30000){status.textContent='Keep your draft under 30,000 characters.';return;}value('draft');status.textContent='Draft copied into your attempt below. Save coding practice to keep it with your account.';resize();};
function indent() {source.setRangeText('  ',source.selectionStart,source.selectionEnd,'end');source.focus();}
byId('indent').onclick=indent;
source.addEventListener('keydown',event=>{
  if(event.key==='Tab') {event.preventDefault();if(event.shiftKey){const pos=source.selectionStart;if(source.value.slice(Math.max(0,pos-2),pos)==='  ')source.setRangeText('',pos-2,pos,'end');}else indent();}
  if((event.ctrlKey||event.metaKey)&&event.key==='Enter') {event.preventDefault();run(false);}
});
byId('reset').onclick=()=>{if(window.confirm('Replace the current editor text with this challenge’s starter? Download your draft first if you want to keep it.')){source.value=config.starter;status.textContent='Starter restored. Your previously saved attempts are unchanged.';value('draft');resize();}};
byId('download').onclick=()=>{const blob=new Blob([source.value],{type:'text/plain;charset=utf-8'});const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=config.challengeId+(config.language==='sql'?'.sql':'.py');link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
window.addEventListener('message',event=>{
  if(event.source!==window.parent||event.data?.type!=='streamlit:render')return;
  config={...config,...event.data.args};
  const theme=event.data.theme;
  if(theme)for(const [key,field] of Object.entries({'--bg':'backgroundColor','--panel':'secondaryBackgroundColor','--text':'textColor','--accent':'primaryColor'})){if(theme[field])document.documentElement.style.setProperty(key,theme[field]);}
  if(!mounted){source.value=config.code;mounted=true;}
  byId('language').textContent=config.language==='sql'?'SQLite practice editor':'Python practice editor';
  if(!busy)setBusy(false);
  resize();
});
source.value=config.code;setBusy(false);
new ResizeObserver(resize).observe(document.body);
message('streamlit:componentReady',{apiVersion:1});resize();

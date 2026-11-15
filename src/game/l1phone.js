// L1 점검(폰 세로): 스텝마다 S.idx를 바꿔 renderStep()을 부르고 0.1초·0.8초 뒤 문제 띠(.dialog .line)를 덮는 요소를 잰다. 사용: node src/game/l1phone.js [스테이지id,…]
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
const src=fs.readFileSync(ROOT+'/index.html','utf8');const A='window.__DSG = { get S()';
const OUT=ROOT+'/local_l1phone.html';fs.writeFileSync(OUT,src.replace(A,'window.__DSG = { startRun, renderStep, get S()'));
const {chromium,devices}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();
const ctx=await b.newContext({...devices['iPhone 13'],deviceScaleFactor:1});
await ctx.route(/^https?:/,r=>r.abort());
await ctx.addInitScript(()=>{try{localStorage.setItem('dsg_onb','1');localStorage.setItem('dsg_name','검수봇');}catch(e){}});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+OUT);await p.waitForTimeout(800);
let stages=await p.evaluate(()=>window.__DSG.STAGES.map(s=>s.id)); if(process.argv[2]) stages=process.argv[2].split(',');
const hits={},pos=[];const cnt={};
const probe=()=>p.evaluate(()=>{const S=window.__DSG.S;const s=S.steps[S.idx];const line=document.querySelector('.dialog .line');if(!line||!line.offsetParent||!s)return null;
  const L=line.getBoundingClientRect();const h=[];const dlg=line.closest('.dialog');
  for(const e of document.querySelectorAll('body *')){if(dlg.contains(e)||e.contains(dlg))continue;const cs=getComputedStyle(e);if(cs.position!=='fixed'&&cs.position!=='absolute')continue;if(cs.visibility==='hidden'||+cs.opacity===0)continue;
    const R=e.getBoundingClientRect();if(R.width<2||R.height<2)continue;const ix=Math.min(R.right,L.right)-Math.max(R.left,L.left),iy=Math.min(R.bottom,L.bottom)-Math.max(R.top,L.top);if(ix<=0||iy<=0)continue;
    if(e.closest('#shot')||e.closest('.layer')||e.closest('.frame'))continue;
    h.push((e.className&&e.className.toString().split(' ')[0]||e.tagName)+'@z'+cs.zIndex+':'+Math.round(ix*iy*100/(L.width*L.height))+'%');}
  return{sid:s.id,top:Math.round(L.top),bot:Math.round(L.bottom),vh:innerHeight,h};});
for(const id of stages){
  await p.evaluate(()=>{document.getElementById('overlayHost').innerHTML='';window.__DSG.S.steps=[];});
  await p.evaluate(id=>{const D=window.__DSG;const S=D.S;S.profile={name:'검수봇',office:''};S.name='검수봇';if(!S.persona)S.persona=D.PERSONAS.no||Object.values(D.PERSONAS)[0];D.startRun('one',id);},id);
  for(let k=0;k<30;k++){const n=await p.evaluate(()=>{const b=document.getElementById('stayPortrait');if(b)b.click();const host=document.getElementById('overlayHost');const bs=[...host.querySelectorAll('button')].filter(x=>x.offsetParent&&!/맵/.test(x.textContent));if(!b&&bs.length)bs[0].click();return window.__DSG.S.steps.length;});if(n)break;await p.waitForTimeout(150);}
  const n=await p.evaluate(()=>window.__DSG.S.steps.length);cnt[id]=n;
  for(let i=0;i<n;i++){
    await p.evaluate(i=>{const D=window.__DSG;D.S.idx=i;D.S.locked=false;D.S.busy=false;document.getElementById('overlayHost').innerHTML='';D.renderStep();},i);
    for(const w of [100,700]){await p.waitForTimeout(w);const c=await probe();if(!c)continue;pos.push([id,c.sid,c.top,c.bot,c.vh]);for(const k of c.h){const key=id+'|'+c.sid+'|'+k;hits[key]=(hits[key]||0)+1;}}
  }
}
const tops=pos.map(x=>x[2]),bots=pos.map(x=>x[3]);
console.log(JSON.stringify({mode:'phone',cnt,samples:pos.length,top:[Math.min(...tops),Math.max(...tops)],bot:[Math.min(...bots),Math.max(...bots)],vh:pos[0]&&pos[0][4],offscreen:pos.filter(x=>x[2]<0||x[3]>x[4]).slice(0,10),hits,errs:errs.slice(0,3)}));
await b.close();})();

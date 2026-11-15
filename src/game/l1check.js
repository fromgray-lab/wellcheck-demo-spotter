// L1 점검: 전 스테이지를 자동 플레이하며 매 순간 문제 띠(.dialog .line)를 덮는 요소가 있는지 잰다. 사용: node src/game/l1check.js [pc|phone] [스테이지id,…]
// autoplay.js와 같은 사본(local_autoplay.html) 방식 · 외부 네트워크 차단. 결과: 덮은 요소(클래스)·스텝·덮인 비율, 띠 위치(top/bottom px).
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
const src=fs.readFileSync(ROOT+'/index.html','utf8');const A='window.__DSG = { get S()';
const OUT=ROOT+'/local_autoplay.html';fs.writeFileSync(OUT,src.replace(A,'window.__DSG = { startRun, get S()'));
const {chromium,devices}=require('/opt/npm-tools/node_modules/playwright');
const MODE=process.argv[2]||'pc';
(async()=>{const b=await chromium.launch();
const ctx=await b.newContext(MODE==='phone'?{...devices['iPhone 13'],deviceScaleFactor:1}:{viewport:{width:1280,height:800}});
await ctx.route(/^https?:/,r=>r.abort());
await ctx.addInitScript(()=>{try{localStorage.setItem('dsg_onb','1');localStorage.setItem('dsg_name','검수봇');}catch(e){}});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+OUT);await p.waitForTimeout(800);
let stages=await p.evaluate(()=>window.__DSG.STAGES.map(s=>s.id)); if(process.argv[3]) stages=process.argv[3].split(',');
const hits={},pos=[];const out=[];
for(const id of stages){
  await p.evaluate(()=>{document.getElementById('overlayHost').innerHTML='';document.querySelectorAll('.modal.on,.modal.open').forEach(m=>m.classList.remove('on','open'));window.__DSG.S.steps=[];});
  await p.evaluate(id=>{const D=window.__DSG;const S=D.S;S.profile={name:'검수봇',office:''};S.name='검수봇';if(!S.persona)S.persona=D.PERSONAS.no||Object.values(D.PERSONAS)[0];D.startRun('one',id);},id);
  let res='timeout';const t0=Date.now();
  while(Date.now()-t0<110000){
    await p.waitForTimeout(90);
    const st=await p.evaluate(id=>{const S=window.__DSG.S;const r=S.stageRes[id]||{};const host=document.getElementById('overlayHost');const btns=[...host.querySelectorAll('button')].filter(x=>x.offsetParent);
      const line=document.querySelector('.dialog .line');let cov=null;
      const s=S.steps[S.idx];
      if(line&&line.offsetParent&&s&&!btns.length){const L=line.getBoundingClientRect();const hitsL=[];const dlg=line.closest('.dialog');
  for(const e of document.querySelectorAll('body *')){if(dlg.contains(e)||e.contains(dlg))continue;const cs=getComputedStyle(e);if(cs.position!=='fixed'&&cs.position!=='absolute')continue;if(cs.visibility==='hidden'||+cs.opacity===0)continue;
    const R=e.getBoundingClientRect();if(R.width<2||R.height<2)continue;const ix=Math.min(R.right,L.right)-Math.max(R.left,L.left),iy=Math.min(R.bottom,L.bottom)-Math.max(R.top,L.top);if(ix<=0||iy<=0)continue;
    if(e.closest('#shot')||e.closest('.layer')||e.closest('.frame'))continue;
    hitsL.push((e.className&&e.className.toString().split(' ')[0]||e.tagName)+'@z'+cs.zIndex+':'+Math.round(ix*iy*100/(L.width*L.height))+'%');}
        cov={sid:s.id,top:Math.round(L.top),bot:Math.round(L.bottom),vh:innerHeight,h:hitsL};}
      if(r.cleared)return{done:'clear',cov};if(S.over)return{done:'over',cov};
      if(btns.length)return{btn:1};
      if(S.locked||S.busy||!s)return{wait:1,cov};
      const R=s.rects[0];const bb=document.getElementById('shot').getBoundingClientRect();
      return{tap:[bb.left+(R.l+R.w/2)/100*bb.width,bb.top+(R.t+R.h/2)/100*bb.height],sid:s.id,cov};},id);
    if(st.cov){const c=st.cov;pos.push([id,c.sid,c.top,c.bot,c.vh]);for(const k of c.h){const key=id+'|'+c.sid+'|'+k;hits[key]=(hits[key]||0)+1;}}
    if(st.done){res=st.done;break;}
    if(st.btn){await p.evaluate(()=>{const host=document.getElementById('overlayHost');const btns=[...host.querySelectorAll('button')].filter(x=>x.offsetParent&&!x.disabled);if(!btns.length)return;const nx=btns.find(x=>x.id==='qNext'||/계속|다음|▶/.test(x.textContent)&&!/맵/.test(x.textContent));const q=btns.find(x=>x.classList.contains('qopt')||x.dataset.i!==undefined);(nx||q||btns.find(x=>!/맵/.test(x.textContent))||btns[0]).click();});await p.waitForTimeout(150);continue;}
    if(st.tap){await p.mouse.click(st.tap[0],st.tap[1]);await p.waitForTimeout(200);}
  }
  out.push(id+': '+res);
}
const tops=pos.map(x=>x[2]),bots=pos.map(x=>x[3]);
console.log(JSON.stringify({mode:MODE,stages:out,samples:pos.length,top:[Math.min(...tops),Math.max(...tops)],bot:[Math.min(...bots),Math.max(...bots)],vh:pos[0]&&pos[0][4],offscreen:pos.filter(x=>x[2]<0||x[3]>x[4]).slice(0,10),hits,errs:errs.slice(0,3)}));
await b.close();})();

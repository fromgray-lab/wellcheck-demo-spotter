// 전 스테이지 자동 플레이(배포 전 검증, 운영서 7번). 사용: node src/game/autoplay.js [스테이지id,…]
// 루트 index.html을 복사해 startRun만 노출한 사본(루트 local_autoplay.html, .gitignore 대상)으로 실행. 외부 네트워크는 모두 차단 → 시트에 기록이 남지 않음.
// 원장님 질문·사이트 퀴즈는 첫 보기를 골라 넘기므로 '오답'에 퀴즈 오답이 섞일 수 있음. 판정은 clear 여부.
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
const src=fs.readFileSync(ROOT+'/index.html','utf8');const A='window.__DSG = { get S()';
if(!src.includes(A)){console.error('startRun 노출 지점 없음');process.exit(2);}
const OUT=ROOT+'/local_autoplay.html';fs.writeFileSync(OUT,src.replace(A,'window.__DSG = { startRun, get S()'));
const {chromium}=require('/opt/npm-tools/node_modules/playwright');
const URL='file://'+OUT;
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:800}});
await ctx.route(/^https?:/,r=>r.abort());
await ctx.addInitScript(()=>{try{localStorage.setItem('dsg_onb','1');localStorage.setItem('dsg_name','검수봇');}catch(e){}});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto(URL);await p.waitForTimeout(800);
let stages=await p.evaluate(()=>window.__DSG.STAGES.map(s=>s.id)); if(process.argv[2]) stages=process.argv[2].split(',');
const out=[];
for(const id of stages){
  await p.evaluate(()=>{document.getElementById('overlayHost').innerHTML='';document.querySelectorAll('.modal.on,.modal.open').forEach(m=>m.classList.remove('on','open'));});
  await p.evaluate(id=>{const D=window.__DSG;const S=D.S;S.profile={name:'검수봇',office:''};S.name='검수봇';if(!S.persona)S.persona=D.PERSONAS.no||Object.values(D.PERSONAS)[0];D.startRun('one',id);},id);
  let res='timeout',taps=0,ov=0;const t0=Date.now();
  while(Date.now()-t0<150000){
    await p.waitForTimeout(120);
    const st=await p.evaluate(id=>{const S=window.__DSG.S;const r=S.stageRes[id]||{};const host=document.getElementById('overlayHost');const btns=[...host.querySelectorAll('button')].filter(x=>x.offsetParent);
      if(r.cleared)return{done:'clear',w:r.wrong+' '+JSON.stringify((r.steps||[]).filter(l=>l.w||l.wrong).map(l=>l.id+':'+(l.w||l.wrong)))+' q'+JSON.stringify((S.qLog||[]).filter(x=>!x.ok).length)};if(S.over)return{done:'over',w:r.wrong};
      if(btns.length){const q=btns.find(x=>x.classList.contains('qopt')||x.dataset.i!==undefined||x.dataset.so!==undefined);return{btn:q?'q':'b'};}
      if(S.locked||S.busy)return{wait:1};const s=S.steps[S.idx];if(!s)return{wait:1};
      const R=s.rects[0];const bb=document.getElementById('shot').getBoundingClientRect();
      return{tap:[bb.left+(R.l+R.w/2)/100*bb.width,bb.top+(R.t+R.h/2)/100*bb.height],sid:s.id};},id);
    if(process.env.DBG) console.log(JSON.stringify(st));
    if(st.done){res=st.done+' 오답'+st.w;break;}
    if(st.btn){ov++;await p.evaluate(()=>{const host=document.getElementById('overlayHost');const btns=[...host.querySelectorAll('button')].filter(x=>x.offsetParent&&!x.disabled);if(!btns.length)return;const nx=btns.find(x=>x.id==='qNext'||/계속|다음|▶/.test(x.textContent)&&!/맵/.test(x.textContent));const q=btns.find(x=>x.classList.contains('qopt')||x.dataset.i!==undefined);(nx||q||btns.find(x=>!/맵/.test(x.textContent))||btns[0]).click();});await p.waitForTimeout(200);continue;}
    if(st.tap){taps++;await p.mouse.click(st.tap[0],st.tap[1]);await p.waitForTimeout(250);}
  }
  out.push(id+': '+res+' (탭'+taps+')');
}
console.log(out.join('\n'));console.log('pageerrors',errs.length,errs.slice(0,3).join(' | '));const bad=out.filter(x=>!/: clear/.test(x)).length+errs.length;console.log(bad?'실패 '+bad:'전 스테이지 클리어');process.exitCode=bad?1:0;await b.close();})();

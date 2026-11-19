// L9 점검 보조(v69~): 따라하기·복습 끝 화면(practiceEnd)의 👍/👎 원탭이 PC·폰 세로·폰 가로 첫 화면에서 보이고, 누르면 kind:'tap' 의견이 저장되는지 잰다.
// 사용: node src/game/l9practice.js [스테이지id]  (기본 m2). 외부 네트워크 차단 — 저장은 이 기기 보관함(dsg_fb, 새 것이 맨 앞)으로 확인.
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
const src=fs.readFileSync(ROOT+'/index.html','utf8');const A='window.__DSG = { get S()';
if(!src.includes(A)){console.error('노출 지점 없음');process.exit(2);}
const OUT=ROOT+'/local_l9practice.html';fs.writeFileSync(OUT,src.replace(A,'window.__DSG = { startRun, practiceEnd, get S()'));
const {chromium,devices}=require('/opt/npm-tools/node_modules/playwright');
const VIEWS=[['PC',{viewport:{width:1280,height:800}}],['폰세로',{...devices['iPhone 13'],deviceScaleFactor:1}],['폰가로',{...devices['iPhone 13 landscape'],deviceScaleFactor:1}]];
const id=process.argv[2]||'m2';
(async()=>{const b=await chromium.launch();const rows=[];const errs=[];
for(const [vn,opt] of VIEWS){
  const ctx=await b.newContext(opt);await ctx.route(/^https?:/,r=>r.abort());
  await ctx.addInitScript(()=>{try{localStorage.setItem('dsg_onb','1');localStorage.setItem('dsg_name','검수봇');}catch(e){}});
  const p=await ctx.newPage();p.on('pageerror',e=>errs.push(vn+': '+e.message));
  await p.goto('file://'+OUT);await p.waitForTimeout(800);
  for(const kind of ['guide','review']){
    await p.evaluate(id=>{document.getElementById('overlayHost').innerHTML='';const D=window.__DSG;const S=D.S;S.steps=[];S.profile={name:'검수봇',office:''};S.name='검수봇';if(!S.persona)S.persona=D.PERSONAS.no||Object.values(D.PERSONAS)[0];D.startRun('one',id);},id);
    for(let i=0;i<40;i++){await p.waitForTimeout(150);const n=await p.evaluate(()=>{const sp=document.getElementById('stayPortrait');if(sp&&sp.offsetParent)sp.click();return window.__DSG.S.steps.length;});if(n)break;}
    await p.waitForTimeout(4000); // 시작 카운트다운이 끝난 뒤 끝 화면을 연다(안 그러면 카운트다운이 끝 화면을 덮어씀)
    await p.evaluate(kind=>{const S=window.__DSG.S;S.stageRes=S.stageRes||{};S.stageRes[S.stage.id]=S.stageRes[S.stage.id]||{wrong:1};document.getElementById('overlayHost').innerHTML='';window.__DSG.practiceEnd(kind);},kind);
    await p.waitForTimeout(700);
    const btn=await p.evaluate(()=>{const vw=innerWidth,vh=innerHeight;return [...document.querySelectorAll('#overlayHost #fbCard .thumbs button')].map(x=>{const r=x.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2;const inV=cx>=0&&cx<=vw&&cy>=0&&cy<=vh;const top=inV?document.elementFromPoint(cx,cy):null;return{t:x.dataset.t,w:Math.round(r.width),h:Math.round(r.height),cy:Math.round(cy),vh,vis:!!(top&&(top===x||x.contains(top)))};});});
    const nb=await p.evaluate(()=>{const x=document.getElementById("nextStageBtn");if(!x)return null;const r=x.getBoundingClientRect();return {mid:Math.round(r.top+r.height/2),bottom:Math.round(r.bottom),vh:innerHeight};});
    const shot=path.join(process.env.L9SHOT||'/tmp','l9p_'+vn+'_'+kind+'.png');await p.screenshot({path:shot});
    let saved=null;const up=btn.find(x=>x.t==='up');
    if(up&&up.vis){const before=await p.evaluate(()=>JSON.parse(localStorage.getItem('dsg_fb')||'[]').length);
      const ok=await p.evaluate(()=>{const x=document.querySelector("#overlayHost #fbCard .thumbs button[data-t=up]");if(!x)return document.getElementById("overlayHost").innerText.slice(0,200);const r=x.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];});if(typeof ok==="string"){console.log("사라짐",vn,kind,ok);}else await p.mouse.click(ok[0],ok[1]);await p.waitForTimeout(600);
      saved=await p.evaluate(n=>{const l=JSON.parse(localStorage.getItem('dsg_fb')||'[]');const d=l.slice(0,l.length-n);return d.map(x=>({kind:x.kind,stage:x.stage,result:x.result,thumbs:x.thumbs}));},before);
      await p.screenshot({path:shot.replace('.png','_tap.png')});}
    rows.push({vn,kind,btn,nextBtnY:nb,saved,shot});
  }
  await ctx.close();
}
for(const r of rows) console.log(JSON.stringify(r));
const bad=rows.filter(r=>!r.btn.length||r.btn.some(x=>!x.vis)||!r.saved||r.saved.length!==1||r.saved[0].kind!=='tap');
console.log('pageerrors',errs.length,errs.slice(0,3).join(' | '));console.log(bad.length?'위반 '+bad.length:'따라하기·복습 끝 화면 전부 원탭 가능·저장 확인');await b.close();process.exit(bad.length?1:0);})();

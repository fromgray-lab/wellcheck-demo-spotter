// L9 점검 보조(v70~): 순서 맞추기 끝 화면(.oresult)의 👍/👎 원탭이 PC·폰 세로·폰 가로 첫 화면에서 보이고, 누르면 kind:'tap'·mode:'order' 의견이 저장되는지 잰다.
// 사용: node src/game/l9order.js [스테이지id]  (기본 m0). 외부 네트워크 차단 — 저장은 이 기기 보관함(dsg_fb, 새 것이 맨 앞)으로 확인.
// 카드를 정답 순서대로 눌러(실수 0) 끝 화면을 연다. 아래 주 버튼('다시'·'이 스테이지 실전')이 화면 안에 남는지도 잰다.
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
const src=fs.readFileSync(ROOT+'/index.html','utf8');const A='window.__DSG = { get S()';
if(!src.includes(A)){console.error('노출 지점 없음');process.exit(2);}
const OUT=ROOT+'/local_l9order.html';fs.writeFileSync(OUT,src.replace(A,'window.__DSG = { openOrder, get S()'));
const {chromium,devices}=require('/opt/npm-tools/node_modules/playwright');
const VIEWS=[['PC',{viewport:{width:1280,height:800}}],['폰세로',{...devices['iPhone 13'],deviceScaleFactor:1}],['폰가로',{...devices['iPhone 13 landscape'],deviceScaleFactor:1}]];
const ids=(process.argv[2]||'m0').split(',');
(async()=>{const b=await chromium.launch();const rows=[];const errs=[];
for(const [vn,opt] of VIEWS){
  const ctx=await b.newContext(opt);await ctx.route(/^https?:/,r=>r.abort());
  await ctx.addInitScript(()=>{try{localStorage.setItem('dsg_onb','1');localStorage.setItem('dsg_name','검수봇');}catch(e){}});
  const p=await ctx.newPage();p.on('pageerror',e=>errs.push(vn+': '+e.message));
  await p.goto('file://'+OUT);await p.waitForTimeout(800);
  for(const id of ids){
    const order=await p.evaluate(id=>{const D=window.__DSG,S=D.S;S.profile={name:'검수봇',office:''};S.name='검수봇';const st=D.STAGES.find(s=>s.id===id);if(st&&st.course&&S.course!==st.course)D.setCourse(st.course);D.openOrder(id);
      const P=S.persona||D.PERSONAS.no;return D.STEPS.filter(s=>s.st===id&&(!s.branch||s.branch===(P.branch||P.key))).map(s=>s.id);},id);
    await p.waitForTimeout(500);
    for(const sid of order){await p.evaluate(sid=>{const c=document.querySelector(`#orderModal .ocard[data-id="${sid}"]`);if(c)c.click();},sid);await p.waitForTimeout(40);}
    await p.waitForTimeout(1200); // 스크롤(smooth) 끝날 때까지
    const m=await p.evaluate(()=>{const vh=innerHeight,vw=innerWidth;const box=x=>{if(!x)return null;const r=x.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2;const inV=cx>=0&&cx<=vw&&cy>=0&&cy<=vh;const top=inV?document.elementFromPoint(cx,cy):null;return{cy:Math.round(cy),bottom:Math.round(r.bottom),vis:!!(top&&(top===x||x.contains(top)))};};
      return {vh,thumbs:[...document.querySelectorAll('#ofbCard .thumbs button')].map(x=>({t:x.dataset.t,...box(x)})),again:box(document.getElementById('oAgain')),play:box(document.getElementById('oPlay'))};});
    const shot=path.join(process.env.L9SHOT||'/tmp','l9o_'+vn+'_'+id+'.png');await p.screenshot({path:shot});
    let saved=null;const up=m.thumbs.find(x=>x.t==='up');
    if(up&&up.vis){const before=await p.evaluate(()=>JSON.parse(localStorage.getItem('dsg_fb')||'[]').length);
      const xy=await p.evaluate(()=>{const r=document.querySelector('#ofbCard .thumbs button[data-t=up]').getBoundingClientRect();return[r.left+r.width/2,r.top+r.height/2];});
      await p.mouse.click(xy[0],xy[1]);await p.waitForTimeout(500);
      saved=await p.evaluate(n=>{const l=JSON.parse(localStorage.getItem('dsg_fb')||'[]');return l.slice(0,l.length-n).map(x=>({kind:x.kind,stage:x.stage,mode:x.mode,result:x.result,thumbs:x.thumbs}));},before);
      await p.screenshot({path:shot.replace('.png','_tap.png')});}
    rows.push({vn,id,...m,saved,shot});
    await p.evaluate(()=>{const h=document.getElementById('overlayHost2');if(h)h.innerHTML='';});
  }
  await ctx.close();
}
for(const r of rows) console.log(JSON.stringify(r));
const bad=rows.filter(r=>!r.thumbs.length||r.thumbs.some(x=>!x.vis)||!r.saved||r.saved.length!==1||r.saved[0].kind!=='tap'||r.saved[0].mode!=='order'||r.saved[0].stage!==r.id);
const btnOut=rows.filter(r=>!(r.again&&r.again.vis&&r.play&&r.play.vis));
console.log('pageerrors',errs.length,errs.slice(0,3).join(' | '));
console.log('주 버튼 화면 밖',btnOut.length,btnOut.map(r=>r.vn+'/'+r.id).join(' '));
console.log(bad.length?'위반 '+bad.length:'순서 맞추기 끝 화면 전부 원탭 가능·저장 확인');await b.close();process.exit(bad.length?1:0);})();

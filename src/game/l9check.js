// L9 점검(의견 원탭): 스테이지 끝 화면(클리어·퇴장)에서 👍/👎 버튼이 스크롤 없이 첫 화면에 보이고 누를 수 있는지 잰다.
// 사용: node src/game/l9check.js [스테이지id,…]  (기본: 스텝이 가장 적은 스테이지 1개 + m2)
// PC(1280×800) · 폰 세로(iPhone 13) · 폰 가로(iPhone 13 가로) 세 화면. 외부 네트워크 차단(시트에 기록 안 남김).
// 폰 세로는 보드가 화면보다 넓어 좌표 탭으로 끝까지 못 가므로 클리어 화면은 stageClear()를 바로 불러 연다.
// 판정: 버튼 가운데 점이 화면 안이고 elementFromPoint가 그 버튼이면 '보임'. 가로·세로 크기(px)도 기록(권장 ≥ 36px).
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
const src=fs.readFileSync(ROOT+'/index.html','utf8');const A='window.__DSG = { get S()';
if(!src.includes(A)){console.error('노출 지점 없음');process.exit(2);}
const OUT=ROOT+'/local_l9check.html';fs.writeFileSync(OUT,src.replace(A,'window.__DSG = { startRun, stageClear, get S()'));
const {chromium,devices}=require('/opt/npm-tools/node_modules/playwright');
const VIEWS=[['PC',{viewport:{width:1280,height:800}}],['폰세로',{...devices['iPhone 13'],deviceScaleFactor:1}],['폰가로',{...devices['iPhone 13 landscape'],deviceScaleFactor:1}]];
(async()=>{const b=await chromium.launch();const rows=[];const errs=[];
for(const [vn,opt] of VIEWS){
  const ctx=await b.newContext(opt);await ctx.route(/^https?:/,r=>r.abort());
  await ctx.addInitScript(()=>{try{localStorage.setItem('dsg_onb','1');localStorage.setItem('dsg_name','검수봇');}catch(e){}});
  const p=await ctx.newPage();p.on('pageerror',e=>errs.push(vn+': '+e.message));
  await p.goto('file://'+OUT);await p.waitForTimeout(800);
  let stages=process.argv[2]?process.argv[2].split(','):await p.evaluate(()=>{const D=window.__DSG;const n={};D.STEPS.forEach(s=>n[s.st]=(n[s.st]||0)+1);const ids=D.STAGES.map(s=>s.id).filter(id=>n[id]);ids.sort((a,b)=>n[a]-n[b]);return [ids[0],'m2'];});
  for(const id of stages) for(const kind of ['clear','over']){
    await p.evaluate(()=>{document.getElementById('overlayHost').innerHTML='';document.querySelectorAll('.modal.on').forEach(m=>m.classList.remove('on'));const S=window.__DSG.S;S.steps=[];S.over=false;});
    await p.evaluate(id=>{const D=window.__DSG;const S=D.S;S.profile={name:'검수봇',office:''};S.name='검수봇';if(!S.persona)S.persona=D.PERSONAS.no||Object.values(D.PERSONAS)[0];D.startRun('one',id);},id);
    let got=null;const t0=Date.now();
    while(Date.now()-t0<120000){
      await p.waitForTimeout(150);
      const st=await p.evaluate(([id,kind])=>{const S=window.__DSG.S;const sp=document.getElementById('stayPortrait');if(sp&&sp.offsetParent){sp.click();return{wait:1};}
        const fb=document.querySelector('#overlayHost #fbCard');const qo=[...document.querySelectorAll('.qopt')].some(x=>x.offsetParent);if(fb&&!qo)return{fb:1};const nq=document.getElementById('qNext');if(nq&&nq.offsetParent){nq.click();return{wait:1};}if(qo){const q=[...document.querySelectorAll('.qopt')].find(x=>x.offsetParent);const r=q.getBoundingClientRect();return{tap:[r.left+r.width/2,r.top+r.height/2]};}
        const host=document.getElementById('overlayHost');const btns=[...host.querySelectorAll('button')].filter(x=>x.offsetParent&&!x.disabled);
        if(btns.length){const nx=btns.find(x=>x.id==='qNext'||/계속|다음|▶/.test(x.textContent)&&!/맵/.test(x.textContent));const q=btns.find(x=>x.classList.contains('qopt')||x.dataset.i!==undefined);(nx||q||btns.find(x=>!/맵/.test(x.textContent))||btns[0]).click();return{wait:1};}
        if(S.locked||S.busy||!S.steps.length)return{wait:1};if(kind==='clear'&&innerHeight>innerWidth){window.__DSG.stageClear();return{wait:1};}const s=S.steps[S.idx];if(!s)return{wait:1};
        const R=s.rects[0];const bb=document.getElementById('shot').getBoundingClientRect();
        if(kind==='over'){S.patience=Math.min(S.patience,1);const x=(R.l+R.w/2)>50?0.04:0.96,y=(R.t+R.h/2)>50?0.06:0.94;return{tap:[bb.left+x*bb.width,bb.top+y*bb.height]};}
        return{tap:[bb.left+(R.l+R.w/2)/100*bb.width,bb.top+(R.t+R.h/2)/100*bb.height]};},[id,kind]);
      if(st.fb){await p.waitForTimeout(900);got=await p.evaluate(()=>{const vw=innerWidth,vh=innerHeight;return [...document.querySelectorAll('#fbCard .thumbs button')].map(x=>{const r=x.getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2;const inV=cx>=0&&cx<=vw&&cy>=0&&cy<=vh;const top=inV?document.elementFromPoint(cx,cy):null;return{t:x.dataset.t,w:Math.round(r.width),h:Math.round(r.height),cy:Math.round(cy),vh,vis:!!(top&&(top===x||x.contains(top)))};});});
        const whyN=await p.evaluate(()=>document.querySelectorAll('#fbCard .fbwr').length);
        const shot=path.join(process.env.L9SHOT||'/tmp','l9_'+vn+'_'+id+'_'+kind+'.png');await p.screenshot({path:shot});
        rows.push({vn,id,kind,btn:got,why:whyN,shot});break;}
      if(st.tap){await p.mouse.click(st.tap[0],st.tap[1]);await p.waitForTimeout(250);}
    }
    if(!got) rows.push({vn,id,kind,btn:null,note:'끝 화면 못 봄'});
  }
  await ctx.close();
}
for(const r of rows) console.log(JSON.stringify(r));
const bad=rows.filter(r=>!r.btn||!r.btn.length||r.btn.some(x=>!x.vis));
console.log('pageerrors',errs.length,errs.slice(0,3).join(' | '));console.log(bad.length?'위반 '+bad.length:'전부 첫 화면에서 원탭 가능');await b.close();})();

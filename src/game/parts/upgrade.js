
/* ═══════════════════════════════════════════ 고도화 v8: 마스터키 · 따라하기 · 복습 런 · 추천 임무 · 이어하기 · 이미지 저장 · 편집 · 단축키 · BGM ═══════════════════════════════════════════ */
/* ── 마스터키 (전체 결과는 키가 있어야) ── */
const MASTER_KEY='inbliss'; /* 바꾸려면 여기 */
function masterOk(){ try{ return sessionStorage.getItem('dsg_master')==='1'; }catch(e){ return false; } }
let keyCb=null;
function askMaster(cb){ if(masterOk()){ BOARD.admin=true; cb(); return; } keyCb=cb; $('keyInput').value=''; $('keyInput').style.borderColor=''; openModal('keyModal'); setTimeout(()=>{ try{ $('keyInput').focus(); }catch(e){} },60); }
$('keyOk').addEventListener('click', ()=>{ if(($('keyInput').value||'').trim()===MASTER_KEY){ try{ sessionStorage.setItem('dsg_master','1'); }catch(e){} BOARD.admin=true; closeModal('keyModal'); SFX.go(); const cb=keyCb; keyCb=null; if(cb) cb(); } else { $('keyInput').style.borderColor='var(--red)'; $('keyInput').select(); SFX.wrong(); } });
$('keyCancel').addEventListener('click', ()=>{ keyCb=null; closeModal('keyModal'); });
$('keyInput').addEventListener('keydown', e=>{ e.stopPropagation(); if(e.key==='Enter') $('keyOk').click(); });

/* ── 추천 임무 · 이어하기 (임무판) ── */
function loadResume(){ try{ return JSON.parse(localStorage.getItem('dsg_resume')||'null'); }catch(e){ return null; } }
function saveResume(){ if(S.mode!=='all'||S.demo||S.guide) return; const last=S.qi>=S.queue.length-1; if(last){ try{ localStorage.removeItem('dsg_resume'); }catch(e){} return; } try{ localStorage.setItem('dsg_resume', JSON.stringify({ course:S.course, queue:S.queue, qi:S.qi+1, wrong:S.wrong, chance:S.chance, tips:S.tips, chances:S.chances, results:S.results, qLog:S.qLog||[], stageRes:S.stageRes, elapsed:Date.now()-S.start, persona:S.persona?S.persona.key:'no', at:Date.now() })); }catch(e){} }
function clearResume(){ try{ localStorage.removeItem('dsg_resume'); }catch(e){} }
function resumeRun(rs){ S.mode='all'; S.demo=false; S.guide=false; S.course=rs.course; S.queue=rs.queue; S.qi=rs.qi; S.wrong=rs.wrong||0; S.chance=rs.chance||0; S.tips=rs.tips||0; S.chances=rs.chances??3; S.results=rs.results||[]; S.qLog=rs.qLog||[]; S.stageRes=rs.stageRes||{}; S.over=false; S.start=Date.now()-(rs.elapsed||0); S.stepLog=[]; S.cur=null; if(rs.persona&&PERSONAS[rs.persona]) S.persona=PERSONAS[rs.persona]; clearInterval(S.timer); S.timer=setInterval(tickTimer,1000); tickTimer(); show('play'); fitArena(); tryFullscreen(); portraitGate(()=>startStage()); }
function renderTodo(){
  const sts=STAGES.filter(st=>st.course===S.course&&!st.locked);
  const recs=sts.map(st=>{ const b=S.stars[st.id]; const sc=b?b.stars:0; return { st, sc, why: !b?'미클리어':sc<3?'★'+sc+' → 무결점 도전':'' }; }).filter(r=>r.why).sort((a,b)=>a.sc-b.sc).slice(0,3);
  const el=$('todo'); if(!el) return;
  el.innerHTML = recs.length ? `<span class="tl">🎯 오늘의 추천 미션</span>${recs.map(r=>`<button type="button" class="tchip" data-st="${r.st.id}"><b>${stageCode(r.st)}</b> ${esc(r.st.title)} <small>${esc(r.why)}</small></button>`).join('')}` : `<span class="tl">🏆 전 스테이지 무결점!</span><span class="src">전체 완주 타임어택으로 기록을 줄여보세요</span>`;
  el.querySelectorAll('.tchip').forEach(b=>b.addEventListener('click', ()=>{ SFX.go(); startRun('one', b.dataset.st); }));
  const rs=loadResume(); const rb=$('resumeBtn'); if(rb){ if(rs && rs.course===S.course && rs.qi<rs.queue.length){ const st=STAGES.find(s=>s.id===rs.queue[rs.qi]); rb.hidden=false; rb.textContent='⏯ 이어하기 ('+(st?stageCode(st):'?')+'부터)'; rb.onclick=()=>{ SFX.go(); resumeRun(rs); }; } else rb.hidden=true; }
}

/* ── 틀린 것만 복습 런 ── */
function startReview(){ const ids=(S.lastBad||[]).filter(id=>STEPS.some(s=>s.id===id)); if(!ids.length) return; S.reviewIds=ids; S.mode='review'; S.demo=false; S.guide=false; S.queue=['review']; S.qi=0; S.stepLog=[]; S.cur=null; S.wrong=0; S.chance=0; S.tips=0; S.results=[]; S.stageRes={}; S.over=false; S.start=Date.now(); S.chances=3; clearInterval(S.timer); S.timer=setInterval(tickTimer,1000); tickTimer(); show('play'); fitArena(); tryFullscreen(); portraitGate(()=>startStage()); }
$('reviewBtn').addEventListener('click', ()=>{ SFX.go(); startReview(); });

/* ── 따라하기(가이드) 보조 ── */
function showRing(st){ const r=st.rects[0]; const ring=document.createElement('div'); ring.className='ring'; ring.style.left=(r.l+r.w/2)+'%'; ring.style.top=(r.t+r.h/2)+'%'; ring.style.width=(Math.max(r.w,3.5)+2.5)+'%'; ring.style.height=(Math.max(r.h,5)+4)+'%'; $('fx').appendChild(ring); const hand=document.createElement('div'); hand.className='hand'; hand.style.left=(r.l+r.w/2)+'%'; hand.style.top=(r.t+r.h/2)+'%'; hand.textContent='👆'; $('fx').appendChild(hand); }
function guideStep(st){ $('tbar').hidden=true; showRing(st); $('dHint').textContent='✋ '+st.chance+' — 직접 눌러보세요'; $('dHint').classList.add('on'); }
function guideSay(st){ const say=st.tip&&st.tip.say?st.tip.say:''; if(!say) return 0; const card=document.createElement('div'); card.className='demo-say'; card.innerHTML=`<div class="dl">🗣 이 화면에서 할 말</div><div>${esc(say)}</div>`; $('arenaUi').appendChild(card); return Math.min(4500, 1400+say.length*40); }
function practiceEnd(kind){ stopStepTimer(); SFX.clear(); const id=S.stage.id; const host=$('overlayHost'); const title = kind==='guide' ? '따라하기 완료!' : '복습 완료!'; const desc = kind==='guide' ? `${stageCode(S.stage)} · ${S.stage.title} — 손에 익었나요? 이제 실전으로.` : `틀렸던 ${S.steps.length}단계를 다시 짚었습니다 (오답 ${S.stageRes[id].wrong}).`;
  host.innerHTML=`<div class="overlay" style="pointer-events:auto"><div class="g-panel"><svg class="ovchar r" viewBox="0 0 280 330" aria-hidden="true"><use href="#chDocYes"/></svg><div class="banner blue">${title}</div><p style="margin:6px 0 0;color:var(--dim)">${desc}</p>${recapHtml()}<div class="btn-row">${kind==='guide'?`<button type="button" class="g-btn big green" id="nextStageBtn">🎯 실전 도전</button>`:`<button type="button" class="g-btn big green" id="nextStageBtn">성적표로</button>`}<button type="button" class="g-btn gray" id="toMap2">맵으로</button></div></div></div>`;
  $('nextStageBtn').addEventListener('click', ()=>{ host.innerHTML=''; if(kind==='guide'){ S.guide=false; startRun('one', id); } else { exitFullscreen(); show('result'); } });
  $('toMap2').addEventListener('click', ()=>{ host.innerHTML=''; S.guide=false; exitFullscreen(); renderMap(); show('map'); }); }
/* ── 핵심 멘트 리캡 (스테이지 끝) ── */
function recapHtml(){ const steps=S.steps.filter(s=>s.tip&&s.tip.say); if(!steps.length) return ''; const bad=new Set(S.results.filter(r=>r.runIdx===S.qi&&(r.wrong>0||r.chance)).map(r=>r.id)); const pick=[...steps.filter(s=>bad.has(s.id)), ...steps.filter(s=>!bad.has(s.id))].slice(0,3); return `<details class="recap"><summary>🗣 이 스테이지 핵심 멘트 ${pick.length}</summary><ol>${pick.map(s=>`<li>${bad.has(s.id)?'<b>[틀린 단계]</b> ':''}${esc(s.tip.say)}</li>`).join('')}</ol></details>`; }

/* ── 성적표 이미지 저장 ── */
function roundRect(c,x,y,w,h,r){ c.beginPath(); c.moveTo(x+r,y); c.arcTo(x+w,y,x+w,y+h,r); c.arcTo(x+w,y+h,x,y+h,r); c.arcTo(x,y+h,x,y,r); c.arcTo(x,y,x+w,y,r); c.closePath(); }
function saveResultImage(){ const L=S.lastResult; if(!L) return; const W=1080,H=1350; const cv=document.createElement('canvas'); cv.width=W; cv.height=H; const c=cv.getContext('2d');
  // 햇살 배경
  if(c.createConicGradient){ const g=c.createConicGradient(0,W/2,H*0.32); for(let i=0;i<=48;i++){ g.addColorStop(i/48, i%2?'#ffd23f':'#ff9a1f'); } c.fillStyle=g; } else c.fillStyle='#ffb52e';
  c.fillRect(0,0,W,H); c.fillStyle='#e0177a'; c.fillRect(0,H*0.78,W,H*0.22); c.fillStyle='#2a2f55'; c.fillRect(0,H*0.78,W,16);
  // 패널
  c.save(); c.shadowColor='rgba(0,0,0,.25)'; c.shadowBlur=30; c.shadowOffsetY=14; roundRect(c,70,120,W-140,H-300,34); c.fillStyle='#fff8e7'; c.fill(); c.restore(); roundRect(c,70,120,W-140,H-300,34); c.lineWidth=8; c.strokeStyle='#1d2140'; c.stroke();
  const F=(sz,fam)=>`${sz}px ${fam||"'Jua','Noto Sans KR',sans-serif"}`; c.textAlign='center'; c.textBaseline='middle';
  c.font=F(58,"'Black Han Sans','Jua',sans-serif"); c.lineWidth=14; c.strokeStyle='#1d2140'; c.lineJoin='round'; c.strokeText('틀린시연찾기',W/2,62); c.fillStyle='#ffd93b'; c.fillText('틀린시연찾기',W/2,62);
  c.fillStyle='#1d2140'; c.font=F(44); c.fillText(L.doc, W/2, 200); c.font=F(26); c.fillStyle='#5b6383'; c.fillText(L.courseName+' · '+L.date, W/2, 250);
  // 등급 박스
  const gc={S:['#ffe347','#ff8a1c'],A:['#7bd389','#22b573'],B:['#6fd7ff','#2b9bff'],C:['#d8a6ff','#8b5cf6'],D:['#b9c3d8','#5b6b8a'],F:['#ff7b7b','#c43e3e']}[L.g]||['#ddd','#999']; const gg=c.createLinearGradient(0,300,0,520); gg.addColorStop(0,gc[0]); gg.addColorStop(1,gc[1]); roundRect(c,W/2-110,300,220,220,44); c.fillStyle=gg; c.fill(); c.lineWidth=8; c.strokeStyle='#1d2140'; c.stroke(); c.font=F(170,"'Black Han Sans','Jua',sans-serif"); c.lineWidth=10; c.strokeText(L.g,W/2,412); c.fillStyle='#fff'; c.fillText(L.g,W/2,412);
  c.fillStyle='#1d2140'; c.font=F(40); c.fillText(L.name, W/2, 580); c.font=F(26); c.fillStyle='#5b6383'; c.fillText(L.verdict, W/2, 626);
  // 지표
  const stats=[['점수',L.total],['오답',L.wrong],['찬스',L.chance],['응대',L.q&&L.q.total?`${L.q.ok}/${L.q.total}`:'—'],['시간',L.time]]; stats.forEach(([k,v],i)=>{ const x=110+i*(W-220)/5, w=(W-220)/5-12; roundRect(c,x,670,w,96,18); c.fillStyle='#fff'; c.fill(); c.lineWidth=4; c.strokeStyle='#1d2140'; c.stroke(); c.fillStyle='#5b6383'; c.font=F(20); c.fillText(k,x+w/2,696); c.fillStyle='#1d2140'; c.font=F(String(v).length>5?30:36); c.fillText(String(v),x+w/2,736); });
  // 스테이지 별
  c.textAlign='left'; let y=820; L.rows.forEach(([code,title,stars])=>{ c.fillStyle='#1d2140'; c.font=F(24); c.fillText(code+' '+title, 130, y); c.font=F(30); c.strokeStyle='#1d2140'; c.lineWidth=3; const sw=c.measureText('★').width+6; const x0=W-130-sw*3; for(let k=0;k<3;k++){ const on=k<stars; c.fillStyle=on?'#ffd93b':'#e3e5ee'; c.strokeStyle=on?'#1d2140':'#b8bccc'; c.strokeText('★', x0+k*sw, y); c.fillText('★', x0+k*sw, y); } c.strokeStyle='#1d2140'; y+=44; });
  c.textAlign='center'; c.fillStyle='#fff'; c.font=F(28); c.lineWidth=6; c.strokeStyle='#1d2140'; c.strokeText('웰체크 자유자재 시연 MR 양성소', W/2, H-96); c.fillText('웰체크 자유자재 시연 MR 양성소', W/2, H-96);
  const fn=`틀린시연찾기_${L.name}_${L.g}.png`; const btn=$('imgBtn'); const done=(t,ms)=>{ btn.textContent=t; setTimeout(()=>{ btn.textContent='🖼 이미지 저장'; btn.disabled=false; }, ms||1800); };
  btn.disabled=true; btn.textContent='준비 중…';
  cv.toBlob(async b=>{ if(!b){ done('저장 실패'); return; }
    const dl=await getDownloads();
    if(dl){ btn.textContent='저장 확인 중…'; try{ await dl.save({ filename:fn, data:b }); SFX.star(); done('저장됨 ✓'); } catch(e){ const c=e&&e.code; done(c==='declined'?'취소됨':c==='rate_limited'?'잠시 후 다시':c==='too_large'?'용량 초과':'저장 실패'); } }
    else if(!window.claude){ const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=fn; document.body.appendChild(a); a.click(); setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); },1500); done('저장됨 ✓'); }
    else { done('이 화면에선 저장 불가', 2600); }
  }, 'image/png'); }
/* downloads 권한: claude 뷰어 안에서는 downloads capability로 저장, 로컬 미리보기에서는 blob 링크로 저장 */
let DLNS; function getDownloads(){ if(DLNS!==undefined) return Promise.resolve(DLNS); if(!(window.claude&&typeof claude.use==='function')){ DLNS=null; return Promise.resolve(null); } return claude.use('downloads').then(ns=>{ DLNS=ns||null; return DLNS; }).catch(()=>{ DLNS=null; return null; }); }
(function(){ if(!(window.claude&&typeof claude.use==='function')) return; getDownloads().then(ns=>{ if(!ns){ const b=$('imgBtn'); if(b){ b.hidden=true; } } }); })();
$('imgBtn').addEventListener('click', saveResultImage);

/* ── 관리자: 보드 위에서 드래그로 정답영역 편집 ── */
const E={ on:false, drag:false, x0:0, y0:0, rect:null };
function shotPct(cx,cy){ const b=$('shot').getBoundingClientRect(); return [ (cx-b.left)/b.width*100, (cy-b.top)/b.height*100 ]; }
function editToggle(){ E.on=!E.on; $('zedit').classList.toggle('on',E.on); arena.style.cursor=E.on?'cell':'crosshair'; if(!E.on) editClear(); }
function editClear(){ E.drag=false; const r=$('fx').querySelector('.editrect'); if(r) r.remove(); const p=$('arenaUi').querySelector('.editpanel'); if(p) p.remove(); }
function editStart(e){ editClear(); const [x,y]=shotPct(e.clientX,e.clientY); E.drag=true; E.x0=x; E.y0=y; const d=document.createElement('div'); d.className='editrect'; d.style.left=x+'%'; d.style.top=y+'%'; $('fx').appendChild(d); }
function editMove(e){ if(!E.drag) return; const [x,y]=shotPct(e.clientX,e.clientY); const l=Math.min(E.x0,x), t=Math.min(E.y0,y), w=Math.abs(x-E.x0), h=Math.abs(y-E.y0); const d=$('fx').querySelector('.editrect'); if(d){ d.style.left=l+'%'; d.style.top=t+'%'; d.style.width=w+'%'; d.style.height=h+'%'; } E.rect={ l:Math.round(l*10)/10, t:Math.round(t*10)/10, w:Math.round(w*10)/10, h:Math.round(h*10)/10 }; }
function editEnd(){ if(!E.drag) return; E.drag=false; const r=E.rect; if(!r||r.w<1||r.h<1){ editClear(); return; } const st=S.steps[S.idx]; if(!st) return; const p=document.createElement('div'); p.className='editpanel'; p.innerHTML=`<b>${st.id}</b> 정답영역 l ${r.l} · t ${r.t} · w ${r.w} · h ${r.h}<div class="btn-row" style="margin-top:6px;justify-content:flex-start"><button type="button" class="g-btn sm blue" data-ed="rect+">추가</button><button type="button" class="g-btn sm orange" data-ed="rect=">교체</button><button type="button" class="g-btn sm" data-ed="x">취소</button></div>`; $('arenaUi').appendChild(p);
  p.querySelectorAll('[data-ed]').forEach(b=>b.addEventListener('click', async()=>{ const f=b.dataset.ed; if(f==='x'){ editClear(); return; } b.textContent='저장 중…'; const o={ step:st.id, stage:st.st, field:f, value:r, reason:'관리자 드래그 편집', by:S.name||'관리자', at:new Date().toISOString(), status:'active' }; await saveOverride(o); OVERRIDES.push(o); applyOverrides(OVERRIDES); editClear(); SFX.star(); word('저장!','chance'); renderStep(); })); }
$('zedit').addEventListener('click', editToggle);

/* ── 키보드 단축키 ── */
document.addEventListener('keydown', e=>{ if(!$('play').classList.contains('on')) return; if(e.target&&/INPUT|SELECT|TEXTAREA/.test(e.target.tagName)) return; const k=e.key.toLowerCase(); if(k==='t'){ $('tipBtn').click(); } else if(k==='c'){ $('chanceBtn').click(); } else if(k==='f'){ $('zfit').click(); } else if(e.key==='+'||e.key==='='){ $('zin').click(); } else if(e.key==='-'){ $('zout').click(); } });

/* ── BGM: 8비트 느낌 루프 (타이틀·임무판·결과에서만, 기본 꺼짐) ── */
const BGM={ on:false, iv:null, step:0 };
const BGM_MEL=[0,4,7,12,7,4,0,-5, 2,5,9,14,9,5,2,-3, 0,4,7,12,16,12,7,4, -1,2,7,11,14,11,7,2];
const BGM_BASS=[0,0,7,7,-3,-3,5,5];
function bgmTick(){ if(!S.sound){ return; } const ac=ctx(); if(!ac) return; const i=BGM.step%32; const t=ac.currentTime; const n=(f,d,type,v)=>{ const o=ac.createOscillator(), g=ac.createGain(); o.type=type; o.frequency.value=f; g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(v,t+0.01); g.gain.exponentialRampToValueAtTime(0.0001,t+d); o.connect(g).connect(ac.destination); o.start(t); o.stop(t+d+0.02); }; n(523.25*Math.pow(2,BGM_MEL[i]/12),0.12,'square',0.035); if(i%4===0) n(130.81*Math.pow(2,BGM_BASS[Math.floor(i/4)%8]/12),0.22,'triangle',0.06); if(i%2===1) noise(0.02,0.025,6000); BGM.step++; }
function bgmStart(){ if(BGM.iv||!BGM.on) return; BGM.iv=setInterval(bgmTick,125); }
function bgmStop(){ clearInterval(BGM.iv); BGM.iv=null; }
function bgmSet(on){ BGM.on=on; try{ localStorage.setItem('dsg_bgm', on?'1':'0'); }catch(e){} document.querySelectorAll('.bgmBtn').forEach(b=>{ b.textContent=on?'🎵 BGM':'🔇 BGM'; b.classList.toggle('on',on); }); if(on && !$('play').classList.contains('on')) bgmStart(); else bgmStop(); }
document.querySelectorAll('.bgmBtn').forEach(b=>b.addEventListener('click', e=>{ e.stopPropagation(); bgmSet(!BGM.on); if(BGM.on) SFX.pop(); }));
try{ if(localStorage.getItem('dsg_bgm')==='1'){ BGM.on=true; document.querySelectorAll('.bgmBtn').forEach(b=>{ b.textContent='🎵 BGM'; b.classList.add('on'); }); document.addEventListener('pointerdown', ()=>bgmStart(), { once:true }); } }catch(e){}

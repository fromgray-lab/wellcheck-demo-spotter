
/* ═══════════════════════════════════════════ v11: 시범 자막 싱크 · 약점 집중 훈련 · 실수 DNA · 인증서 · 대본 인쇄본 · 내 노래 BGM · 주간 다이제스트 ═══════════════════════════════════════════ */

/* ── 1) 시범 모드: 자막 싱크(카라오케식 하이라이트) + 음성 자동 재생 + 진행 바 ── */
function demoClean(say){ return String(say||'').replace(/<[^>]+>/g,'').replace(/[“”"]/g,'').trim(); }
function capHtml(say){ const parts=String(say||'').split(/(\s+)/); let pos=0; return parts.map(p=>{ const s=pos; pos+=p.length; if(!p.trim()) return p; return `<span class="cw" data-s="${s}">${esc(p)}</span>`; }).join(''); }
function demoStop(){ S.demoTok=null; if(S.demoT){ clearTimeout(S.demoT); S.demoT=null; } if(S.demoAnim){ cancelAnimationFrame(S.demoAnim); S.demoAnim=null; } }
function demoNarrate(say, go, card){
  demoStop(); const tok={}; S.demoTok=tok; const words=[...card.querySelectorAll('.cw')]; const n=say.length;
  const mark=(ci)=>{ words.forEach(w=>w.classList.toggle('on', +w.dataset.s<=ci)); };
  const tts=TTS.on&&TTS.ok&&!!say; const est = tts ? Math.min(20000, 1500+n*220) : Math.min(6500, 2200+n*45); /* 음성은 끝나는 시점(onend)에 맞춰 당겨짐 — 추정치는 넉넉히 */
  const bar=card.querySelector('.dprog i'); if(bar){ bar.style.transition='none'; bar.style.width='0%'; requestAnimationFrame(()=>requestAnimationFrame(()=>{ bar.style.transition=`width ${est}ms linear`; bar.style.width='100%'; })); }
  const t0=Date.now(); let bound=false; mark(-1);
  const tick=()=>{ if(S.demoTok!==tok) return; if(!bound){ const f=Math.min(1,(Date.now()-t0-350)/Math.max(1,est-800)); mark(Math.floor(f*n)); } S.demoAnim=requestAnimationFrame(tick); };
  S.demoAnim=requestAnimationFrame(tick);
  const finish=(ms)=>{ if(S.demoTok!==tok) return; mark(n+1); if(S.demoT) clearTimeout(S.demoT); S.demoT=setTimeout(go, ms); };
  S.demoT=setTimeout(go, est+450);
  if(tts) speak(say,{ rate:1.0, onBoundary:(ci)=>{ if(S.demoTok!==tok) return; bound=true; mark(ci); }, onEnd:(why)=>{ if(why==='end') finish(700); } });
}

/* ── 2) 약점 집중 훈련: 숙련도 낮은 스텝 10개만 골라 반복 ── */
function focusPick(course){ computeMastery(localRuns(), localList('dsg_evals')); const pool=STEPS.filter(s=>{ const st=STAGES.find(x=>x.id===s.st); return st&&st.course===course&&!st.locked&&!s.branch; }); const bad=new Set(S.lastBad||[]);
  const scored=pool.map(s=>{ const m=MASTERY.step[s.id]; const tried=m!=null; return { s, m: tried?m:null, k:(tried?(100-m):45)+(bad.has(s.id)?30:0)+Math.random()*6 }; }).sort((a,b)=>b.k-a.k);
  const pick=scored.slice(0,10); const order=new Map(STEPS.map((s,i)=>[s.id,i])); pick.sort((a,b)=>order.get(a.s.id)-order.get(b.s.id)); return pick; }
function focusWeak(course){ computeMastery(localRuns(), localList('dsg_evals')); const ids=STEPS.filter(s=>{ const st=STAGES.find(x=>x.id===s.st); return st&&st.course===course&&!st.locked&&!s.branch; }); const tried=ids.filter(s=>MASTERY.step[s.id]!=null); return { tried:tried.length, weak:tried.filter(s=>MASTERY.step[s.id]<60).length, total:ids.length }; }
function startFocus(){ const pick=focusPick(S.course); S.focusIds=pick.map(x=>x.s.id); S.focusBefore={}; pick.forEach(x=>{ S.focusBefore[x.s.id]=x.m; });
  S.mode='focus'; S.demo=false; S.guide=false; S.prevSite=null; S.queue=['focus']; S.qi=0; S.stepLog=[]; S.qLog=[]; S.cur=null; S.wrong=0; S.chance=0; S.tips=0; S.results=[]; S.stageRes={}; S.over=false; S.start=Date.now(); applyDiff(); clearInterval(S.timer); S.timer=setInterval(tickTimer,1000); tickTimer(); show('play'); fitArena(); tryFullscreen(); portraitGate(()=>startStage()); }
function focusEnd(){ stopStepTimer(); clearInterval(S.timer); SFX.clear(); const res=S.stageRes.focus; res.secs=Math.floor((Date.now()-res.start)/1000); res.steps=S.stepLog.filter(l=>l.st); const score=Math.max(0,100-W_WRONG*res.wrong-W_CHANCE*res.chance); const g=gradeOf(score,false);
  const comp=compactSteps(res.steps); const after=masteryFromRuns(myRuns(localRuns()), comp).step;
  saveRun({ ...(S.profile||{name:S.name}), persona:S.persona?S.persona.key:'', mode:'focus', course:S.course, stage:'focus', diff:S.diff, grade:g, score, wrong:res.wrong, chance:res.chance, tips:res.tips, secs:res.secs, at:new Date().toISOString(), over:false, stars:{}, steps:comp, q:qSummary() });
  const rows=(S.focusIds||[]).map(id=>{ const st=STEPS.find(s=>s.id===id); const b=S.focusBefore[id]; const a=after[id]; return { st, b, a:a==null?0:a }; });
  const avg=l=>l.length?Math.round(l.reduce((x,y)=>x+y,0)/l.length):0; const avgB=avg(rows.map(r=>r.b==null?0:r.b)), avgA=avg(rows.map(r=>r.a));
  const host=$('overlayHost'); host.innerHTML=`<div class="overlay" style="pointer-events:auto"><div class="g-panel"><svg class="ovchar r" viewBox="0 0 280 330" aria-hidden="true"><use href="#chDocYes"/></svg><div class="banner">약점 집중 훈련 완료!</div><div style="font-family:var(--display);color:var(--dim)">${esc(COURSES[S.course].name)} · 숙련도 평균 <b style="color:var(--ink)">${avgB}% → ${avgA}%</b> ${avgA>avgB?`<span class="up">▲${avgA-avgB}</span>`:avgA<avgB?`<span class="dn2">▼${avgB-avgA}</span>`:''}</div><div class="tally"><div><small>점수</small><b>${score}</b></div><div><small>오답</small><b>${res.wrong}</b></div><div><small>찬스</small><b>${res.chance}</b></div><div><small>시간</small><b>${fmtTime(res.secs)}</b></div></div><div class="flist">${rows.map(r=>{ const stg=STAGES.find(s=>s.id===r.st.st); const d=r.a-(r.b==null?0:r.b); return `<div class="frow"><span class="fcode">${stg?stageCode(stg):''}</span><span class="ftask">${(r.st.task||'').replace(/<[^>]+>/g,'')}</span><span class="fm ${d>0?'up':d<0?'dn2':''}">${r.b==null?'미시도':r.b+'%'} → <b>${r.a}%</b></span></div>`; }).join('')}</div>${recapHtml()}${fbCardHtml()}<div class="btn-row"><button type="button" class="g-btn big green" id="nextStageBtn">맵으로</button><button type="button" class="g-btn orange" id="focusAgain">🎯 한 번 더</button></div></div></div>`;
  bindFb(host,'clear',res); $('nextStageBtn').addEventListener('click', ()=>{ host.innerHTML=''; exitFullscreen(); renderMap(); show('map'); }); $('focusAgain').addEventListener('click', ()=>{ host.innerHTML=''; SFX.go(); startFocus(); }); }
function renderFocusChip(){ const el=$('todo'); if(!el) return; const w=focusWeak(S.course); const chip=document.createElement('button'); chip.type='button'; chip.className='tchip focus'; chip.innerHTML=`<b>🎯</b> 약점 집중 훈련 <small>${w.tried?`숙련도 60% 미만 ${w.weak}스텝 · 미시도 ${w.total-w.tried}`:'기록이 쌓이면 약한 스텝 위주로'}</small>`; chip.title='숙련도가 낮은 스텝 10개만 골라 반복 — 훈련 뒤 숙련도 변화를 보여줍니다'; chip.addEventListener('click', ()=>{ SFX.go(); startFocus(); }); const d=el.querySelector('.tchip.daily'); if(d) d.after(chip); else el.prepend(chip); }

/* ── 3) 실수 DNA: 오클릭 위치·시간초과·찬스를 유형으로 분류 → 코칭 한 줄 ── */
const DNA_KINDS = {
  near:{ ic:'🎯', n:'위치 미세', tip:'정답 바로 옆을 눌렀어요 — 보드를 핀치로 확대해 정확히 탭하는 습관을' },
  mid:{ ic:'🧭', n:'메뉴 혼동', tip:'같은 화면의 비슷한 메뉴·버튼과 헷갈렸어요 — 👀 시범으로 메뉴 이름을 소리 내어 읽어 보세요' },
  far:{ ic:'🗺', n:'흐름 혼동', tip:'다음 단계가 어디인지 몰랐어요 — 🔀 순서 맞추기와 📜 시연 대본으로 흐름부터' },
  site:{ ic:'🔀', n:'사이트 이동', tip:'사이트가 바뀌는 지점에서 틀렸어요 — 브라우저 바 배지(웰체크/심평원/앱)를 먼저 확인하는 습관을' },
  to:{ ic:'⏳', n:'망설임', tip:'제한 시간 안에 못 찾았어요 — ✋ 따라하기로 각 화면의 첫 동작부터 익히세요' },
  chance:{ ic:'💡', n:'힌트 의존', tip:'찬스를 썼어요 — 🔁 틀린 것만 복습으로 힌트 없이 다시 도전해 보세요' }
};
function missKind(st, p){ const x=p[0], y=p[1]; let best=Infinity; (st.rects||[]).forEach(r=>{ const dx=Math.max(r.l-x,0,x-(r.l+r.w)); const dy=Math.max(r.t-y,0,y-(r.t+r.h))*0.55; best=Math.min(best,Math.hypot(dx,dy)); }); return best<7?'near':best<24?'mid':'far'; }
function prevStepOf(st){ const i=STEPS.indexOf(st); for(let j=i-1;j>=0;j--){ const p=STEPS[j]; if(p.st!==st.st) return null; if(!p.branch||p.branch===(S.persona&&S.persona.key)) return p; } return null; }
function errorDna(stepsObj){ const cnt={near:0,mid:0,far:0,to:0,chance:0,site:0}; let total=0;
  Object.entries(stepsObj||{}).forEach(([id,a])=>{ const st=STEPS.find(s=>s.id===id); if(!st||!Array.isArray(a)) return; const w=a[0]||0, c=a[1]||0, to=a[4]||0, miss=a[5]||[];
    miss.forEach(p=>{ cnt[missKind(st,p)]++; total++; }); if(w>miss.length){ cnt.far+=w-miss.length; total+=w-miss.length; }
    if(to){ cnt.to+=to; total+=to; } if(c){ cnt.chance++; total++; }
    if((w||to) && typeof siteOf==='function'){ const pv=prevStepOf(st); if(pv && siteOf(pv).n!==siteOf(st).n) cnt.site++; } });
  const list=Object.keys(cnt).filter(k=>cnt[k]>0).map(k=>({ k, v:cnt[k], ...DNA_KINDS[k] })).sort((a,b)=>b.v-a.v);
  return { total, cnt, list, top:list.find(x=>x.k!=='site')||list[0]||null }; }
function errorDnaRuns(runs){ const sum={near:0,mid:0,far:0,to:0,chance:0,site:0}; let total=0; (runs||[]).forEach(r=>{ const d=errorDna(r.steps); total+=d.total; Object.keys(sum).forEach(k=>sum[k]+=d.cnt[k]); }); const list=Object.keys(sum).filter(k=>sum[k]>0).map(k=>({ k, v:sum[k], ...DNA_KINDS[k] })).sort((a,b)=>b.v-a.v); return { total, cnt:sum, list, top:list.find(x=>x.k!=='site')||list[0]||null }; }
function dnaHtml(d, compact){ if(!d||!d.total) return `<p class="dnaok">실수 없음 — DNA가 깨끗합니다 ✨</p>`; const base=Math.max(1,...d.list.map(x=>x.v));
  return `<div class="dnabars">${d.list.map(x=>`<div class="dnab" title="${esc(x.tip)}"><span class="dk">${x.ic} ${esc(x.n)}</span><span class="db"><i style="width:${Math.round(x.v/base*100)}%"></i></span><b>${x.v}</b></div>`).join('')}</div>${d.top&&!compact?`<div class="dnatip">${d.top.ic} <b>${esc(d.top.n)}</b>이 가장 많아요 — ${esc(d.top.tip)}</div>`:''}`; }
function renderDna(stepsObj){ const box=$('review'); if(!box) return; const old=box.querySelector('.dna'); if(old) old.remove(); const d=errorDna(stepsObj); if(!d.total) return; const div=document.createElement('div'); div.className='dna'; div.innerHTML=`<h3>🧬 실수 DNA <small>오클릭 ${d.cnt.near+d.cnt.mid+d.cnt.far} · 시간초과 ${d.cnt.to} · 찬스 ${d.cnt.chance}</small></h3>`+dnaHtml(d); box.appendChild(div); }

/* ── 4) MR 자격 인증서 이미지 ── */
function certText(){ const p=S.profile||{}; return { name:p.name||S.name||'시연자', office:[p.div,p.office].filter(Boolean).join(' · '), rank:RANK, mBiz:MASTERY.course.biz||0, mZone:MASTERY.course.zone||0, q:RANK.q&&RANK.q.t?`${RANK.q.ok}/${RANK.q.t}`:'—', date:new Date().toLocaleDateString('ko-KR',{year:'numeric',month:'long',day:'numeric'}) }; }
function saveCertImage(btn){ const T=certText(); const W=1400,H=990; const cv=document.createElement('canvas'); cv.width=W; cv.height=H; const c=cv.getContext('2d');
  const bg=c.createLinearGradient(0,0,W,H); bg.addColorStop(0,'#fff6dc'); bg.addColorStop(1,'#ffe7b3'); c.fillStyle=bg; c.fillRect(0,0,W,H);
  c.strokeStyle='#1d2140'; c.lineWidth=14; roundRect(c,40,40,W-80,H-80,36); c.stroke(); c.strokeStyle='#e0177a'; c.lineWidth=4; roundRect(c,66,66,W-132,H-132,26); c.stroke();
  const F=(sz,fam)=>`${sz}px ${fam||"'Jua','Noto Sans KR',sans-serif"}`; c.textAlign='center'; c.textBaseline='middle';
  const gold=T.rank.id==='master'; const ribbon=gold?'#ffb300':T.rank.id==='certified'?'#2b9bff':'#5ad36b'; c.fillStyle=ribbon; roundRect(c,W/2-270,96,540,64,22); c.fill(); c.strokeStyle='#1d2140'; c.lineWidth=5; c.stroke(); c.fillStyle='#fff'; c.font=F(30); c.fillText('웰체크 자유자재 시연 MR 양성소',W/2,128);
  c.fillStyle='#1d2140'; c.font=F(72,"'Black Han Sans','Jua',sans-serif"); c.fillText('MR 자격 인증서',W/2,236);
  c.font=F(120); c.fillText(T.rank.ic,W/2,370);
  c.font=F(56); c.fillStyle='#1d2140'; c.fillText(T.rank.n,W/2,470);
  c.font=F(44); c.fillText(T.name,W/2,560); c.font=F(26); c.fillStyle='#5b6383'; if(T.office) c.fillText(T.office,W/2,604);
  c.font=F(28); c.fillStyle='#1d2140'; c.fillText(`실무 숙련도 ${T.mBiz}% · 체험존 숙련도 ${T.mZone}% · 원장님 질문 응대 ${T.q}`,W/2,668);
  c.font=F(24); c.fillStyle='#5b6383'; c.fillText(T.rank.desc,W/2,712);
  c.font=F(30); c.fillStyle='#1d2140'; c.fillText('위 사람은 틀린시연찾기 훈련을 통해',W/2,768); c.fillText(`${T.rank.n} 자격 기준을 충족하였기에 이 증서를 수여합니다.`,W/2,808);
  c.font=F(26); c.fillText(T.date,W/2,858); c.font=F(30); c.fillText('신사업전략팀',W/2,896);
  c.save(); c.translate(W-230,H-150); c.rotate(-0.22); c.strokeStyle='#e0177a'; c.lineWidth=7; roundRect(c,-112,-40,224,80,14); c.stroke(); c.fillStyle='#e0177a'; c.font=F(40,"'Black Han Sans','Jua',sans-serif"); c.fillText(gold?'마스터':T.rank.id==='certified'?'정식 인증':'견습',0,2); c.restore();
  const fn=`MR인증서_${T.name}_${T.rank.n}.png`; const done=(t,ms)=>{ if(!btn) return; btn.textContent=t; setTimeout(()=>{ btn.textContent='🏅 인증서 저장'; btn.disabled=false; }, ms||1800); }; if(btn){ btn.disabled=true; btn.textContent='준비 중…'; }
  cv.toBlob(async b=>{ if(!b){ done('저장 실패'); return; } const dl=await getDownloads(); if(dl){ try{ await dl.save({ filename:fn, data:b }); SFX.star(); done('저장됨 ✓'); }catch(e){ const code=e&&e.code; done(code==='declined'?'취소됨':code==='rate_limited'?'잠시 후 다시':'저장 실패'); } } else if(!window.claude){ const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=fn; document.body.appendChild(a); a.click(); setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); },1500); done('저장됨 ✓'); } else done('이 화면에선 저장 불가',2600); }, 'image/png'); }

/* ── 5) 시연 대본 인쇄본(HTML): A4 인쇄용 ── */
function scriptHtml(course){ const sts=STAGES.filter(s=>s.course===course&&!s.locked&&!s.bonus); const e=esc;
  const body=sts.map(st=>{ const steps=STEPS.filter(s=>s.st===st.id&&!s.branch); const qs=QCARDS.filter(q=>q.st===st.id); return `<section><h2><span class="code">${e(stageCode(st))}</span> ${e(st.title)} <small>${e(st.sub)}</small></h2><ol>${steps.map(s=>{ const site=siteOf(s); return `<li><div class="path">${e(site.n)}${s.path?' › '+e(s.path):''}</div><div class="task">${s.task}</div>${s.who&&s.say?`<div class="say">${e(s.who)} ${e(s.say)}</div>`:''}${s.tip&&s.tip.say?`<div class="tip">🗣 ${e(s.tip.say)}</div>`:''}${s.tip&&s.tip.note?`<div class="note">※ ${s.tip.note}</div>`:''}</li>`; }).join('')}</ol>${qs.length?`<div class="qa"><h3>원장님 질문 응대</h3>${qs.map(q=>`<div class="q"><b>Q.</b> ${e(q.q)}<br><b>A.</b> ${e(q.opts[q.ans])}<span class="why"> — ${e(q.why||'')}</span></div>`).join('')}</div>`:''}</section>`; }).join('');
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>웰체크 시연 대본 · ${e(COURSES[course].long)}</title><style>
  @page{size:A4;margin:16mm} body{font-family:'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif;color:#1d2140;line-height:1.5;max-width:860px;margin:24px auto;padding:0 16px}
  h1{font-size:24px;margin:0 0 4px} .meta{color:#5b6383;font-size:13px;margin-bottom:18px} section{break-inside:avoid-page;margin-bottom:22px;border:2px solid #1d2140;border-radius:12px;padding:12px 16px}
  h2{font-size:17px;margin:0 0 8px;display:flex;align-items:center;gap:8px} h2 small{color:#5b6383;font-weight:400;font-size:12px} .code{background:#1d2140;color:#ffd93b;border-radius:8px;padding:1px 8px;font-size:13px}
  ol{margin:0;padding-left:22px} li{margin:0 0 9px;break-inside:avoid} .path{font-size:11px;color:#2b9bff;font-weight:700} .task{font-weight:700} .say{color:#8b5cf6;font-size:13px} .tip{color:#1f9d55;font-size:13px} .note{color:#5b6383;font-size:12px}
  .qa{margin-top:8px;border-top:1px dashed #b8bccc;padding-top:8px} h3{font-size:13px;margin:0 0 6px;color:#e0177a} .q{font-size:13px;margin-bottom:6px} .why{color:#5b6383;font-size:12px}
  .print{position:fixed;right:16px;top:12px;padding:8px 14px;border:2px solid #1d2140;border-radius:10px;background:#ffd93b;font-weight:700;cursor:pointer} @media print{.print{display:none}}
  </sty`+`le></head><body><button class="print" onclick="window.print()">🖨 인쇄 / PDF 저장</button><h1>웰체크 시연 대본 · ${e(COURSES[course].long)}</h1><div class="meta">틀린시연찾기 · 신사업전략팀 · ${e(new Date().toLocaleDateString('ko-KR'))} · 스테이지 ${sts.length}개 · 질문 카드 ${QCARDS.filter(q=>q.course===course).length}장</div>${body}</body></html>`; }
async function saveScriptHtml(btn){ const course=S.course; const html=scriptHtml(course); const fn=`웰체크_시연대본_${COURSES[course].name.replace(/\(.*?\)|\s/g,'')}_인쇄용.html`; const dl=await getDownloads(); if(btn) btn.disabled=true; const done=(t)=>{ if(!btn) return; btn.textContent=t; setTimeout(()=>{ btn.textContent='🖨 인쇄용'; btn.disabled=false; },1800); };
  try{ if(dl){ await dl.save({ filename:fn, data:new Blob([html],{type:'text/html'}) }); done('저장됨 ✓'); } else if(!window.claude){ const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([html],{type:'text/html'})); a.download=fn; document.body.appendChild(a); a.click(); setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); },1500); done('저장됨 ✓'); } else done('저장 불가'); }catch(e){ done(e&&e.code==='declined'?'취소됨':'저장 실패'); } }

/* ── 6) BGM = 견우 노래 「라면을 먹으면」 (bgm/custom.mp3, 페이지에 동봉) — 켜기/끄기만 ── */
const BGM_CUSTOM = { src:'bgm/custom.mp3', title:'견우 노래 「라면을 먹으면」', ok:false, audio:null };
function bgmScreenOk(){ const sc=document.body.dataset.screen; return sc!=='play' && sc!=='board' && sc!=='loop'; }
(function(){ try{ const a=new Audio(); a.preload='auto'; a.loop=true; a.volume=0.45; a.addEventListener('loadedmetadata', ()=>{ BGM_CUSTOM.ok=true; BGM_CUSTOM.audio=a; bgmLabel(); if(BGM.on && bgmScreenOk()) bgmStart(); /* 켜자마자 재생 시도 — 브라우저가 막으면 첫 터치에서 */ }); a.addEventListener('error', ()=>{ BGM_CUSTOM.ok=false; BGM_CUSTOM.audio=null; document.querySelectorAll('.bgmBtn').forEach(b=>{ b.hidden=true; }); }); a.src=BGM_CUSTOM.src; }catch(e){} })();
/* 자동재생이 막힌 브라우저(iOS 등): 첫 터치/키 입력에서 바로 시작 */
['pointerdown','keydown','touchstart'].forEach(ev=>document.addEventListener(ev, ()=>{ if(BGM.on && BGM_CUSTOM.audio && BGM_CUSTOM.audio.paused && bgmScreenOk() && S.sound) bgmStart(); }, { passive:true }));
function bgmLabel(){ document.querySelectorAll('.bgmBtn').forEach(b=>{ b.textContent = BGM.on ? '🎵 BGM' : '🔇 BGM'; b.classList.toggle('on',BGM.on); b.title = BGM_CUSTOM.title+(BGM.on?' 끄기':' 켜기'); }); }
function bgmCycle(){ BGM.on=!BGM.on; try{ localStorage.setItem('dsg_bgm', BGM.on?'1':'0'); }catch(e){} bgmLabel(); if(BGM.on && bgmScreenOk()) bgmStart(); else bgmStop(); }
function bgmSync(){ if(BGM.on && bgmScreenOk()) bgmStart(); else bgmStop(); }
bgmLabel();

/* ── 7) CM 주간 다이제스트: 이번 주 팀 훈련 요약 텍스트(카톡/슬랙용) ── */
function digestText(){ const rows=BOARD.rows||[]; const wk=rows.filter(r=>weekIdx(r.at)===0), pw=rows.filter(r=>weekIdx(r.at)===1); const key=r=>(r.name||'')+'|'+(r.office||''); const people=l=>new Set(l.map(key)).size; const full=l=>l.filter(r=>r.mode==='all'&&!r.over);
  const avg=l=>l.length?Math.round(l.reduce((a,r)=>a+(r.score||0),0)/l.length):0; const modeN=(l,m)=>l.filter(r=>r.mode===m).length;
  const L=[`📰 틀린시연찾기 주간 다이제스트 · ${new Date().toLocaleDateString('ko-KR')} 기준 최근 7일`, ''];
  L.push(`👥 참여 ${people(wk)}명 (지난주 ${people(pw)}명) · 훈련 ${wk.length}건 (지난주 ${pw.length}건)`);
  L.push(`   전체 완주 ${full(wk).length}건 · 단독 ${modeN(wk,'one')} · 오늘의 10문제 ${modeN(wk,'daily')} · 순서 ${modeN(wk,'order')} · 약점 집중 ${modeN(wk,'focus')} · 복습 ${modeN(wk,'review')}`);
  const gd={}; full(wk).forEach(r=>{ gd[r.grade]=(gd[r.grade]||0)+1; }); L.push(`   완주 평균 ${avg(full(wk))}점 (지난주 ${avg(full(pw))}점) · 등급 ${['S','A','B','C','D'].filter(g=>gd[g]).map(g=>g+' '+gd[g]).join(' / ')||'—'}`);
  const best=l=>{ const m={}; l.forEach(r=>{ const k=key(r); if(!m[k]||r.score>m[k].score) m[k]=r; }); return Object.values(m).sort((a,b)=>b.score-a.score||(a.secs||0)-(b.secs||0)); };
  const top=best(full(wk)).slice(0,3); if(top.length) L.push('', `🏆 이번 주 TOP ${top.length}`, ...top.map((r,i)=>`   ${['🥇','🥈','🥉'][i]} ${r.name}${r.office?' ('+r.office+')':''} — ${r.grade} ${r.score}점 · ${fmtTime(r.secs||0)} · ${COURSES[r.course]?COURSES[r.course].name:r.course}`));
  const pb=best(full(pw)); const imp=best(full(wk)).map(r=>{ const o=pb.find(x=>key(x)===key(r)); return o?{ r, d:r.score-o.score }:null; }).filter(x=>x&&x.d>0).sort((a,b)=>b.d-a.d).slice(0,3); if(imp.length) L.push('', '📈 가장 많이 오른 사람', ...imp.map(x=>`   ${x.r.name} +${x.d}점 (${x.r.score-x.d} → ${x.r.score})`));
  const att={}; wk.forEach(r=>{ Object.entries(r.steps||{}).forEach(([id,a])=>{ if(!Array.isArray(a)) return; const o=att[id]=att[id]||{n:0,w:0}; o.n++; if(a[0]>0||a[1]||a[4]) o.w++; }); }); const weak=Object.entries(att).filter(([id,o])=>o.n>=3).map(([id,o])=>({ id, n:o.n, r:o.w/o.n })).sort((a,b)=>b.r-a.r).slice(0,5).filter(x=>x.r>=0.3);
  if(weak.length) L.push('', '🧱 팀 약점 스텝 (오답·찬스·시간초과율)', ...weak.map(x=>{ const st=STEPS.find(s=>s.id===x.id); const stg=st&&STAGES.find(s=>s.id===st.st); return `   ${stg?stageCode(stg):''} ${st?(st.task||'').replace(/<[^>]+>/g,''):x.id} — ${Math.round(x.r*100)}% (${x.n}회)`; }));
  const qw={}; wk.forEach(r=>{ (r.q&&r.q.wrong||[]).forEach(id=>{ qw[id]=(qw[id]||0)+1; }); }); const qtop=Object.entries(qw).sort((a,b)=>b[1]-a[1]).slice(0,3); if(qtop.length) L.push('', '🩺 응대 약점 (자주 틀린 원장님 질문)', ...qtop.map(([id,n])=>{ const q=QCARDS.find(c=>c.id===id); return `   “${q?q.q:id}” — ${n}회 오답`+(q?` → ${q.opts[q.ans]}`:''); }));
  const dna=errorDnaRuns(wk); if(dna.total){ L.push('', `🧬 팀 실수 DNA — ${dna.list.slice(0,3).map(x=>`${x.ic} ${x.n} ${x.v}`).join(' · ')}`); if(dna.top) L.push(`   코칭: ${dna.top.tip}`); }
  const ranks={}; (BOARD.people||[]).forEach(p=>{ const pm=typeof personMastery==='function'?personMastery(p.runs.concat(typeof evalsAsAttempts==='function'?evalsAsAttempts(evalsFor(p)):[])):null; if(pm) ranks[pm.R.n]=(ranks[pm.R.n]||0)+1; }); if(Object.keys(ranks).length) L.push('', `🎖 자격 분포 — ${Object.entries(ranks).map(([k,v])=>`${k} ${v}명`).join(' · ')}`);
  const idle=(BOARD.people||[]).filter(p=>!p.runs.some(r=>weekIdx(r.at)===0) && p.runs.some(r=>weekIdx(r.at)===1)).map(p=>p.name).slice(0,8); if(idle.length) L.push('', `😴 지난주엔 했는데 이번 주 안 한 사람 — ${idle.join(', ')}`);
  L.push('', '— 틀린시연찾기 현황표에서 자동 생성'); return L.join('\n'); }
function openDigest(){ const host=$('overlayHost2')||(()=>{ const d=document.createElement('div'); d.id='overlayHost2'; document.body.appendChild(d); return d; })(); const t=digestText();
  host.innerHTML=`<div class="modal on" id="dgModal"><div class="g-panel" style="width:min(760px,100%)"><div class="eyebrow">📰 CM 주간 다이제스트 · 카톡/슬랙에 붙여넣기</div><pre class="digest" id="dgText">${esc(t)}</pre><div class="btn-row"><button type="button" class="g-btn sm" id="dgCopy">복사</button><button type="button" class="g-btn sm gray" id="dgClose">닫기</button></div></div></div>`;
  $('dgClose').addEventListener('click', ()=>{ host.innerHTML=''; }); $('dgModal').addEventListener('click', e=>{ if(e.target.id==='dgModal') host.innerHTML=''; });
  $('dgCopy').addEventListener('click', async ()=>{ try{ await navigator.clipboard.writeText(t); $('dgCopy').textContent='복사됨 ✓'; }catch(e){ $('dgCopy').textContent='복사 실패'; } setTimeout(()=>$('dgCopy').textContent='복사',1500); }); SFX.pop(); }

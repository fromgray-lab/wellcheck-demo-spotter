
/* ═══════════════════════════════════════════ v22: 복습 카드 → 이 스텝만 연습 · 🩺 응대 오답 노트 ═══════════════════════════════════════════ */
/* ── 1) 복습 카드에서 바로 그 스텝만 다시 (복습 모드, 1스텝) ── */
function startReviewIds(ids){ ids=(ids||[]).filter(id=>STEPS.some(s=>s.id===id)); if(!ids.length) return; S.lastBad=ids; startReview(); }
function bindPractice(root){ root.querySelectorAll('[data-practice]').forEach(b=>b.addEventListener('click', ()=>{ SFX.go(); startReviewIds([b.dataset.practice]); })); }

/* ── 2) 응대 오답 노트: 내 기록에서 틀린 질문 카드를 모아 다시 풀기 ── */
function wrongQIds(){ const me=(S.profile&&S.profile.name)||S.name||''; const cnt={}; localRuns().filter(r=>(r.name||'')===me&&r.q&&Array.isArray(r.q.wrong)).forEach(r=>{ r.q.wrong.forEach(id=>{ cnt[id]=(cnt[id]||0)+1; }); });
  /* 최근 정답으로 푼 카드는 제외: 가장 최근 런에서 shown에 있고 wrong에 없으면 해결된 것으로 */
  const runs=localRuns().filter(r=>(r.name||'')===me&&r.q).sort((a,b)=>(b.at||'').localeCompare(a.at||''));
  const latest={}; runs.forEach(r=>{ (r.q.shown||[]).forEach(id=>{ if(latest[id]==null) latest[id]=(r.q.wrong||[]).includes(id)?'wrong':'ok'; }); });
  return Object.keys(cnt).filter(id=>latest[id]!=='ok' && QCARDS.some(q=>q.id===id&&q.course===S.course)).sort((a,b)=>cnt[b]-cnt[a]); }
function renderWrongQChip(){ const el=$('todo'); if(!el) return; const ids=wrongQIds(); if(!ids.length) return; const chip=document.createElement('button'); chip.type='button'; chip.className='tchip wrongq'; chip.innerHTML=`<b>📕</b> 응대 오답 노트 <small>틀린 질문 ${ids.length}장 다시 풀기</small>`; chip.title='내 기록에서 틀렸던 원장님 질문만 모아 다시 — 맞히면 노트에서 빠집니다'; chip.addEventListener('click', ()=>startQDrill(ids)); const q=el.querySelector('.tchip.qdrill'); if(q) q.after(chip); else el.prepend(chip); }

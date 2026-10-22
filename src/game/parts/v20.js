
/* ═══════════════════════════════════════════ v20: 미션 화면 훈련 칩 정리 · 정답 지도 기간 필터 ═══════════════════════════════════════════ */
/* ── 1) #todo 를 두 줄로: [🏋️ 훈련 모드] 10문제·주간·약점·특훈 / [🧭 오늘 할 것] 입문 코스 다음 단계 · 추천 미션 ── */
function layoutTodo(){ const el=$('todo'); if(!el||el.querySelector('.trow')) return; const modes=[...el.querySelectorAll('.tchip.daily,.tchip.weekly,.tchip.focus,.tchip.qdrill')]; const path=el.querySelector('.tchip.path'); const tl=el.querySelector(':scope > .tl'); const recs=[...el.querySelectorAll(':scope > .tchip')].filter(c=>!modes.includes(c)&&c!==path);
  const r1=document.createElement('div'); r1.className='trow modes'; r1.innerHTML='<span class="tl">🏋️ 훈련 모드</span>'; modes.forEach(c=>r1.appendChild(c));
  const r2=document.createElement('div'); r2.className='trow today'; r2.innerHTML='<span class="tl">🧭 오늘 할 것</span>'; if(path) r2.appendChild(path); recs.forEach(c=>r2.appendChild(c));
  if(tl) tl.remove(); [...el.childNodes].forEach(n=>{ if(n!==r1&&n!==r2&&n.nodeType===1&&!n.classList.contains('trow')) n.remove(); }); el.appendChild(r1); el.appendChild(r2); }

/* ── 2) 정답 지도 기간 필터 ── */
let BM_DAYS=0;
function bmFilterRuns(rows){ if(!BM_DAYS) return rows; const since=Date.now()-BM_DAYS*864e5; return (rows||[]).filter(r=>Date.parse(r.at)>=since); }
/* ── 3) 개인 패널 기록 행: 모드 라벨 ── */
function modeLabel(r){ const M={all:'전체',one:'',daily:'10문제',weekly:'주간',focus:'약점',qdrill:'특훈',order:'순서',review:'복습',demo:'시범',guide:'따라하기'}; const st=STAGES.find(s=>s.id===r.stage); const code=st?stageCode(st):''; const m=M[r.mode]!=null?M[r.mode]:(r.mode||''); return [m,code].filter(Boolean).join(' ')||'?'; }

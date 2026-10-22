
/* ═══════════════════════════════════════════ 숙련도 모델 + MR 자격 등급 ═══════════════════════════════════════════
   스텝 숙련도 = 시도 품질(오답0·찬스0=1.0 / 오답1=0.6 / 찬스 또는 오답2=0.3 / 그 이상=0)의 최근 가중 평균(EMA 0.5) × 시간 감쇠(60일에 걸쳐 60%까지)
   스테이지 숙련도 = 스텝 평균(미시도=0) · 코스 숙련도 = 스테이지 평균 */
const RANKS = [
  { id:'trainee', n:'견습 MR', ic:'🌱', desc:'양성소 입소. 시범·따라하기로 흐름을 익히는 단계' },
  { id:'certified', n:'정식 MR', ic:'🎖', desc:'실무 8단계 완주 B등급 이상 + 실무 숙련도 60% 이상' },
  { id:'master', n:'마스터 MR', ic:'👑', desc:'실무·체험존 모두 A등급 이상 완주 + 두 코스 숙련도 85% 이상 + 원장님 질문 응대 정답률 80% 이상(10문 이상)' }
];
function attemptQ(a){ const [w,c,,,to]=a; if(w===0&&c===0&&!to) return 1; if(w<=1&&!c&&!to) return 0.6; if(c||w===2||to) return 0.3; return 0; }
function myRuns(runs){ const p=S.profile||{}; const name=(p.name||S.name||'').trim(); if(!name) return []; return (runs||[]).filter(r=>(r.name||'').trim()===name && (!p.office || !r.office || r.office===p.office)); }
function masteryFromRuns(runs, extra){
  const per={}; // stepId -> [{at, q}]
  (runs||[]).forEach(r=>{ const at=Date.parse(r.at)||0; Object.entries(r.steps||{}).forEach(([id,a])=>{ (per[id]=per[id]||[]).push({at, q:attemptQ(a)}); }); });
  if(extra){ const at=Date.now(); Object.entries(extra).forEach(([id,a])=>{ (per[id]=per[id]||[]).push({at, q:attemptQ(a)}); }); }
  const step={}; const now=Date.now();
  Object.entries(per).forEach(([id,l])=>{ l.sort((a,b)=>a.at-b.at); let m=l[0].q; for(let i=1;i<l.length;i++) m=0.5*m+0.5*l[i].q; const days=(now-l[l.length-1].at)/864e5; const decay=Math.max(0.6, 1-days/150); step[id]=Math.round(m*decay*100); });
  const stage={}; STAGES.forEach(st=>{ let ids=STEPS.filter(s=>s.st===st.id && !s.branch).map(s=>s.id); if(!ids.length) return; if(st.bonus){ const tried=ids.filter(id=>step[id]!=null); ids = tried.length ? tried : ids; } stage[st.id]=Math.round(ids.reduce((a,id)=>a+(step[id]||0),0)/ids.length); });
  const course={}; Object.keys(COURSES).forEach(c=>{ const ids=STAGES.filter(s=>s.course===c&&!s.locked).map(s=>s.id); course[c]=ids.length?Math.round(ids.reduce((a,id)=>a+(stage[id]||0),0)/ids.length):0; });
  return { step, stage, course };
}
function masteryAfterRun(){ const extra={}; Object.values(S.stageRes||{}).forEach(r=>{ if(r&&r.steps) Object.assign(extra, compactSteps(r.steps)); }); return masteryFromRuns(myRuns(localRuns()), extra).course; }
function rankOf(runs, M){ return rankOfRuns(myRuns(runs), M); }
function rankOfRuns(mine, M){ const best=c=>mine.filter(r=>r.mode==='all'&&r.course===c&&!r.over).map(r=>r.grade).sort().join('');
  const gradeOk=(c,min)=>{ const order='SABCDF'; return mine.some(r=>r.mode==='all'&&r.course===c&&!r.over&&order.indexOf(r.grade)<=order.indexOf(min)); };
  const q=mine.reduce((a,r)=>{ if(r.q){ a.t+=r.q.total||0; a.ok+=r.q.ok||0; } return a; },{t:0,ok:0});
  const qRate=q.t?q.ok/q.t:0;
  if(gradeOk('biz','A')&&gradeOk('zone','A')&&M.course.biz>=85&&M.course.zone>=85&&q.t>=10&&qRate>=0.8) return { ...RANKS[2], q, qRate };
  if(gradeOk('biz','B')&&M.course.biz>=60) return { ...RANKS[1], q, qRate };
  return { ...RANKS[0], q, qRate, next: gradeOk('biz','B') ? `실무 숙련도 ${M.course.biz}% → 60%` : '실무 8단계 완주 B등급 이상' };
}
let MASTERY={ step:{}, stage:{}, course:{biz:0,zone:0} }, RANK=RANKS[0];
function myEvals(evals){ const p=S.profile||{}; const name=(p.name||S.name||'').trim(); if(!name) return []; return (evals||[]).filter(e=>(e.name||'').trim()===name && (!p.office || !e.office || e.office===p.office)); }
function computeMastery(runs, evals){ MASTERY=masteryFromRuns(myRuns(runs).concat(typeof evalsAsAttempts==='function'?evalsAsAttempts(myEvals(evals||[])):[])); RANK=rankOf(runs, MASTERY); return MASTERY; }
function renderMastery(){
  computeMastery(localRuns(), localList('dsg_evals'));
  let chip=$('rankChip'); if(!chip){ chip=document.createElement('span'); chip.className='player-chip rank'; chip.id='rankChip'; chip.title='자격 기준 보기'; $('mapPlayerChip').after(chip); chip.addEventListener('click', openRankInfo); }
  chip.innerHTML=`<span class="av">${RANK.ic}</span><span>${esc(RANK.n)} · 숙련도 ${MASTERY.course[S.course]||0}%</span>`; chip.dataset.rank=RANK.id;
  document.querySelectorAll('#stageGrid .stage').forEach((b,i)=>{ const st=STAGES.filter(s=>s.course===S.course)[i]; if(!st||st.locked) return; const m=MASTERY.stage[st.id]||0; const steps=STEPS.filter(s=>s.st===st.id&&!s.branch); const tried=steps.filter(s=>MASTERY.step[s.id]!=null).length; let el=b.querySelector('.mbar'); if(!el){ el=document.createElement('span'); el.className='mbar'; const anchor=b.querySelector('.stars'); if(anchor) anchor.after(el); else b.appendChild(el); } el.innerHTML=`<i style="width:${m}%"></i><em>숙련도 ${m}%${tried<steps.length?` · 미시도 ${steps.length-tried}`:''}</em>`; el.dataset.lv = m>=85?'hi':m>=60?'mid':'low'; });
  // 공유 저장소가 있으면 팀 기록까지 반영해 갱신
  Promise.all([loadRuns(), loadEvals().catch(()=>[])]).then(([{rows}, evals])=>{ if(!rows||!rows.length) return; const merged=[...rows, ...localRuns()]; const seen=new Set(); const uniq=merged.filter(r=>{ const k=(r.name||'')+'|'+(r.at||''); if(seen.has(k)) return false; seen.add(k); return true; }); computeMastery(uniq, evals||[]); const c=$('rankChip'); if(c&&document.body.dataset.screen==='map'){ c.innerHTML=`<span class="av">${RANK.ic}</span><span>${esc(RANK.n)} · 숙련도 ${MASTERY.course[S.course]||0}%</span>`; c.dataset.rank=RANK.id; document.querySelectorAll('#stageGrid .stage').forEach((b,i)=>{ const st=STAGES.filter(s=>s.course===S.course)[i]; if(!st||st.locked) return; const m=MASTERY.stage[st.id]||0; const el=b.querySelector('.mbar'); if(el){ el.querySelector('i').style.width=m+'%'; el.querySelector('em').textContent=`숙련도 ${m}%`; el.dataset.lv=m>=85?'hi':m>=60?'mid':'low'; } }); } }).catch(()=>{});
}
function openRankInfo(){ const host=$('overlayHost2')||(()=>{ const d=document.createElement('div'); d.id='overlayHost2'; document.body.appendChild(d); return d; })();
  host.innerHTML=`<div class="modal on" id="rankModal"><div class="g-panel"><h2 class="g">🎖 MR 자격 등급</h2><p class="rk-cur">현재: <b>${RANK.ic} ${esc(RANK.n)}</b> · 실무 숙련도 ${MASTERY.course.biz}% · 체험존 숙련도 ${MASTERY.course.zone}%${RANK.q&&RANK.q.t?` · 응대 ${RANK.q.ok}/${RANK.q.t}`:''}${RANK.next?`<br><span class="rk-next">다음 단계까지: ${esc(RANK.next)}</span>`:''}</p><div class="rk-list">${RANKS.map(r=>`<div class="rk ${r.id===RANK.id?'on':''}"><span class="rk-ic">${r.ic}</span><div><b>${esc(r.n)}</b><div>${esc(r.desc)}</div></div></div>`).join('')}</div><p class="rk-note">숙련도 = 스텝별 최근 시도 품질의 가중 평균(최근일수록 비중 큼, 오래 안 하면 서서히 감소). 미시도 스텝은 0%.</p><div class="btn-row"><button type="button" class="g-btn" id="rankClose">닫기</button></div></div></div>`;
  $('rankClose').addEventListener('click', ()=>{ host.innerHTML=''; }); $('rankModal').addEventListener('click', e=>{ if(e.target.id==='rankModal') host.innerHTML=''; }); SFX.pop(); }

/* 현황표용: 담당자 1명의 런 목록 → 숙련도·자격·응대 */
function personMastery(runs){ const M=masteryFromRuns(runs); const R=rankOfRuns(runs, M); return { M, R, mBiz:M.course.biz||0, mZone:M.course.zone||0, qText: R.q&&R.q.t ? `${R.q.ok}/${R.q.t} (${Math.round(R.qRate*100)}%)` : '—' }; }

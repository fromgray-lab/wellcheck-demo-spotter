
/* ═══════════════════════════════════════════ v31(v43): 목적 집중 — 🧭 자유자재 지수 (막힘 없이·망설임 없이) ═══════════════════════════════════════════ */
/* 자유자재 스텝 = 오답 0 · 찬스 0 · 시간초과 0 · FLU_SEC초 안에 정답. 지수 = 자유자재 스텝 / 전체 스텝 */
const FLU_SEC=8;
function fluStats(logs){ const l=(logs||[]).filter(x=>x&&x.id); if(!l.length) return null; const isFlu=x=>!(x.w||0)&&!(x.c||0)&&!(x.to||0)&&(x.s||0)<=FLU_SEC; const flu=l.filter(isFlu).length; const slow=l.filter(x=>!isFlu(x)).map(x=>({ x, st:STEPS.find(s=>s.id===x.id) })).filter(o=>o.st).sort((a,b)=>((b.x.s||0)+(b.x.w||0)*6+(b.x.c||0)*8+(b.x.to||0)*10)-((a.x.s||0)+(a.x.w||0)*6+(a.x.c||0)*8+(a.x.to||0)*10)); const secs=l.reduce((a,x)=>a+(x.s||0),0);
  return { n:l.length, flu, idx:Math.round(flu/l.length*100), avg:Math.round(secs/l.length*10)/10, slow:slow.slice(0,3) }; }
function fluWhy(x){ const r=[]; if(x.w) r.push(`오답 ${x.w}`); if(x.c) r.push('찬스'); if(x.to) r.push('시간 초과'); if((x.s||0)>FLU_SEC) r.push(`${x.s}초 망설임`); return r.join(' · ')||`${x.s||0}초`; }
function fluHtml(logs){ const f=fluStats(logs); if(!f) return ''; const lv=f.idx>=90?['자유자재','ok']:f.idx>=70?['거의 자유자재','mid']:['아직 더듬는 중','low'];
  return `<div class="flu ${lv[1]}"><div class="fhead"><b>🧭 자유자재 지수 ${f.idx}%</b><span>${lv[0]} · 막힘 없이 ${FLU_SEC}초 안에 ${f.flu}/${f.n}스텝 · 스텝당 평균 ${f.avg}초</span></div>${f.slow.length?`<ol class="fslow">${f.slow.map(o=>`<li><b>${esc(stageCode(STAGES.find(s=>s.id===o.st.st)||{}))}</b> ${esc((o.st.task||'').replace(/<[^>]+>/g,''))} <small>${esc(fluWhy(o.x))}</small></li>`).join('')}</ol>`:'<div class="fall">모든 스텝을 막힘 없이 — 원장님 앞에서도 그대로</div>'}</div>`; }
function fluAll(){ const box=$('review'); if(!box) return; const old=box.querySelector('.flu'); if(old) old.remove(); const h=fluHtml(S.stepLog); if(!h) return; const d=document.createElement('div'); d.innerHTML=h; box.prepend(d.firstChild); }
/* 도구 줄: 이제 📲 설치만 (웹) */
function ensureToolsRow(){ const el=$('todo'); if(!el) return null; let r=el.querySelector('.trow.tools'); if(!r){ r=document.createElement('div'); r.className='trow tools'; r.innerHTML='<span class="tl">🧰 도구</span>'; el.appendChild(r); } return r; }

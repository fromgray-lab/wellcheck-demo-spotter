
/* ═══════════════════════════════════════════ v15: 📣 팀 공지 배너 · 입문 코스 팀 추적(시범/따라하기 기록) ═══════════════════════════════════════════ */

/* ── 1) 팀 공지: 관리자가 현황표에서 쓰면 모든 팀원 미션 화면 상단에 표시 (공유 저장소 notes/'__notice__', 없으면 이 기기) ── */
const NOTICE_KEY='__notice__';
async function loadNotice(){ try{ const notes=await loadNotes(); const n=Object.values(notes||{}).find(x=>x&&x.key===NOTICE_KEY); return n||null; }catch(e){ return null; } }
function renderNotice(){ let el=$('notice'); if(!el){ el=document.createElement('div'); el.id='notice'; el.className='notice'; el.hidden=true; const cork=document.querySelector('#map .cork'); if(cork) cork.prepend(el); else return; }
  loadNotice().then(n=>{ if(!n||!(n.text||'').trim()){ el.hidden=true; return; } el.hidden=false; el.innerHTML=`<span class="nic">📣</span><div class="ntx">${esc(n.text).replace(/\n/g,'<br>')}</div><small class="nby">${esc(n.by||'')}${n.at?' · '+new Date(n.at).toLocaleDateString('ko-KR'):''}</small>`; }); }
function openNoticeEditor(){ const host=$('overlayHost2')||(()=>{ const d=document.createElement('div'); d.id='overlayHost2'; document.body.appendChild(d); return d; })();
  loadNotice().then(n=>{ host.innerHTML=`<div class="modal on" id="ntModal"><div class="g-panel" style="width:min(560px,100%)"><h2 class="g">📣 팀 공지</h2><p class="kbd" style="margin:0 0 8px">모든 팀원의 시연 미션 화면 상단에 뜹니다 (예: 이번 주 미션 — 주간 챌린지 A 이상!). 비우고 저장하면 내려갑니다.</p><textarea id="ntText" rows="4" style="width:100%;font:inherit;font-size:14px;border:2px solid var(--ink);border-radius:10px;padding:8px">${esc(n&&n.text||'')}</textarea><div class="btn-row"><button type="button" class="g-btn green" id="ntSave">저장</button><button type="button" class="g-btn gray" id="ntClose">닫기</button></div></div></div>`;
    $('ntClose').addEventListener('click', ()=>{ host.innerHTML=''; }); $('ntModal').addEventListener('click', e=>{ if(e.target.id==='ntModal') host.innerHTML=''; });
    $('ntSave').addEventListener('click', async ()=>{ $('ntSave').disabled=true; $('ntSave').textContent='저장 중…'; await saveNote(NOTICE_KEY, $('ntText').value.trim()); toast('공지 저장됨'); host.innerHTML=''; renderNotice(); }); SFX.pop(); }); }

/* ── 2) 입문 코스 팀 추적: 시범/따라하기 첫 완료를 가벼운 기록으로 남겨 현황표·다이제스트에서 n/7 계산 ── */
function pathLight(kind, stageId){ try{ saveRun({ ...(S.profile||{name:S.name}), persona:S.persona?S.persona.key:'', mode:kind, course:S.course, stage:stageId, grade:'', score:null, wrong:0, chance:0, tips:0, secs:0, at:new Date().toISOString(), over:false, stars:{}, steps:{} }); }catch(e){} }
function pathFromRuns(runs){ const r=runs||[]; const has=(mode,st)=>r.some(x=>x.mode===mode&&x.stage===st); const starOf=(st)=>Math.max(0,...r.map(x=>(x.stars&&x.stars[st])||0));
  const dailyDays=new Set(r.filter(x=>x.mode==='daily').map(x=>(x.at||'').slice(0,10))).size;
  const items=[ ['m0','m1','m2'].every(st=>has('demo',st)), ['m0','m1','m2'].every(st=>has('guide',st)), ['m0','m1','m2','m3'].every(st=>starOf(st)>=2), r.some(x=>x.mode==='qdrill'&&x.score>=70), r.some(x=>x.mode==='all'&&x.course==='biz'&&!x.over&&'SAB'.includes(x.grade)), dailyDays>=3, r.some(x=>x.mode==='all'&&x.course==='zone'&&!x.over) ];
  return { done:items.filter(Boolean).length, total:items.length, items }; }
function pathBadge(p){ const pr=pathFromRuns(p.runs); return pr.done>=pr.total ? '🎓 입문 완료' : `🧭 입문 ${pr.done}/${pr.total}`; }

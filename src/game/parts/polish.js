
/* ═══════════════════════════════════════════ 폴리시: 온보딩 코치마크 · 탭 이탈 시 타이머 정지 · 로딩 스켈레톤 · 토스트 · 모달 포커스 ═══════════════════════════════════════════ */
function toast(msg, ms){ document.querySelectorAll('.toast').forEach(t=>t.remove()); const t=document.createElement('div'); t.className='toast'; t.textContent=msg; document.body.appendChild(t); setTimeout(()=>t.remove(), ms||2400); }
function saveStatus(where){ if(where==='supabase'||where==='db') toast('☁ 팀 공유 기록에 저장됐어요'); else if(where==='local') toast('📱 이 기기에만 저장됐어요 (공유 저장소 없음)'); }

/* ── 보드 로딩 스켈레톤 ── */
(function(){ const img=$('shot'); if(!img) return; const _setBoard=setBoard; setBoard=function(key, reset){ _setBoard(key, reset); arena.classList.toggle('loading', !(img.complete && img.naturalWidth>0)); };
  img.addEventListener('load', ()=>arena.classList.remove('loading')); img.addEventListener('error', ()=>{ arena.classList.remove('loading'); toast('화면 이미지를 불러오지 못했어요 — 네트워크를 확인해 주세요', 3200); }); })();

/* ── 탭 이탈/화면 꺼짐: 스텝 타이머·전체 타이머 정지, 복귀 시 이어서 ── */
(function(){ let hiddenAt=0, left=null;
  document.addEventListener('visibilitychange', ()=>{
    if(document.body.dataset.screen!=='play') return;
    if(document.hidden){ hiddenAt=Date.now(); if(T.iv){ left=Math.max(0,T.deadline-Date.now()); stopStepTimer(); } else left=null; }
    else { const gap=Date.now()-hiddenAt; if(hiddenAt && gap>0){ S.start+=gap; if(S.cur) S.cur.t0+=gap; } hiddenAt=0;
      if(left!=null && S.timed && !S.locked && !S.over){ T.deadline=Date.now()+left; $('tbar').hidden=false; T.iv=setInterval(()=>{ const l=Math.max(0,T.deadline-Date.now()); $('tfill').style.transform=`scaleX(${l/(LIMIT*1000)})`; $('clockHand').style.transform=`rotate(${Math.round((1-l/(LIMIT*1000))*360)}deg)`; $('tbar').classList.toggle('hurry',l<10000); if(l<=0){ stopStepTimer(); onTimeout(); } },100); toast('⏸ 잠깐 멈췄다가 이어서 합니다', 1600); }
      left=null; }
  }); })();

/* ── 모달 포커스 + Esc ── */
(function(){ const _open=openModal; openModal=function(id){ _open(id); try{ const m=$(id); const f=m&&m.querySelector('input,select,textarea,button:not([disabled])'); if(f && /INPUT|TEXTAREA/.test(f.tagName) && !m.querySelector('.pgrid')) setTimeout(()=>f.focus({preventScroll:true}),60); }catch(e){} };
  document.addEventListener('keydown', e=>{ if(e.key!=='Escape') return; const c=document.querySelector('.coach'); if(c){ c.remove(); coachDone(); return; } const q=$('qNext'); if(q) return; const m=[...document.querySelectorAll('.modal.on')].pop(); if(m && m.id!=='setupModal'){ m.classList.remove('on'); if(m.id==='rankModal') m.remove(); } }); })();

/* ── 온보딩 코치마크: 첫 실전 플레이에서 한 번 ── */
function coachSeen(){ try{ return localStorage.getItem('dsg_onb')==='1'; }catch(e){ return false; } }
function coachDone(){ try{ localStorage.setItem('dsg_onb','1'); }catch(e){} if(S.timed && !T.iv && !S.locked && document.body.dataset.screen==='play') startStepTimer(); }
function maybeOnboard(st){ if(S.demo||S.guide||coachSeen()||S.mode==='review') return; if(innerWidth<340) { try{ localStorage.setItem('dsg_onb','1'); }catch(e){} return; }
  stopStepTimer();
  const steps=[
    { el:()=>$('layer'), t:'여기가 시연 화면', d:'원장님 앞에서 실제로 눌러야 할 자리를 찾아 탭하세요. 맞으면 ⭕, 틀리면 ❌와 함께 원장님 인내심이 줄어요.' },
    { el:()=>document.querySelector('.dialog'), t:'임무와 경로', d:'지금 해야 할 일과 "어느 사이트 › 어느 메뉴"인지 여기에 표시됩니다. 사이트가 바뀌면 화면 위 브라우저 바도 바뀌어요.' },
    { el:()=>$('tipBtn'), t:'💡 팁 = 이 화면에서 할 말', d:'감점 없이 언제든 열 수 있는 시연 멘트입니다. 클릭만이 아니라 말까지 익히세요.' },
    { el:()=>$('chanceBtn'), t:'🔍 찬스 = 정답 짚어주기', d:'3번까지. 쓰면 점수가 조금 깎이지만 막혔을 때 흐름을 끊지 않게 해줍니다.' },
    { el:()=>document.querySelector('.hud .mood')||document.querySelector('.hud'), t:'원장님 인내심', d:'오답·시간초과·응대 실수마다 줄어듭니다. 0이 되면 원장님이 퇴장! 중간에 원장님 질문 카드가 뜨면 가장 좋은 답을 고르세요.' }
  ];
  const root=document.createElement('div'); root.className='coach'; root.innerHTML='<div class="hole"></div><div class="bub"></div>'; document.body.appendChild(root);
  const hole=root.querySelector('.hole'), bub=root.querySelector('.bub'); let i=0;
  const place=()=>{ const s=steps[i]; const el=s.el(); const r=el?el.getBoundingClientRect():{left:innerWidth/2-100,top:innerHeight/2-60,width:200,height:120}; const pad=8; hole.style.left=(r.left-pad)+'px'; hole.style.top=(r.top-pad)+'px'; hole.style.width=(r.width+pad*2)+'px'; hole.style.height=(r.height+pad*2)+'px';
    bub.innerHTML=`<b>${esc(s.t)}</b>${esc(s.d)}<div class="row"><span class="n">${i+1} / ${steps.length}</span><button type="button" class="g-btn sm gray" id="coachSkip">건너뛰기</button><button type="button" class="g-btn sm green" id="coachNext">${i<steps.length-1?'다음 ▶':'시작!'}</button></div>`;
    const bw=Math.min(360, innerWidth-24); let bx=r.left+r.width/2-bw/2; bx=Math.max(12, Math.min(innerWidth-bw-12, bx)); const below=r.top+r.height+14; const above=r.top-14; bub.style.width=bw+'px'; bub.style.left=bx+'px';
    const need=200; const spaceBelow=innerHeight-(r.top+r.height), spaceAbove=r.top; bub.style.bottom='auto';
    if(spaceBelow>=need) bub.style.top=below+'px'; else if(spaceAbove>=need){ bub.style.top='auto'; bub.style.bottom=(innerHeight-above)+'px'; } else bub.style.top=Math.max(12, Math.min(innerHeight-need, r.top+r.height/2-100))+'px';
    $('coachNext').addEventListener('click', ()=>{ SFX.pop(); if(i<steps.length-1){ i++; place(); } else { root.remove(); coachDone(); SFX.go(); } }); $('coachSkip').addEventListener('click', ()=>{ root.remove(); coachDone(); }); };
  place();
}

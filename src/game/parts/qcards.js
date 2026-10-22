
/* ═══════════════════════════════════════════ 원장님 질문 카드: 클릭만이 아니라 '말'도 훈련 (매뉴얼 근거 3지선다) ═══════════════════════════════════════════ */
const QCARDS = /*QCARDS_JSON*/[];
const QBY = {}; QCARDS.forEach(q=>{ (QBY[q.after]=QBY[q.after]||[]).push(q); });
/* 스테이지마다 카드 풀에서 최대 2장을 무작위로 뽑아 출제(따라하기는 전부) → 매 런이 조금씩 다름 */
function pickQCards(stageId){ const pool = stageId==='daily' ? QCARDS.filter(q=>q.course===S.course && (S.dailyIds||[]).includes(q.after)) : QCARDS.filter(q=>q.st===stageId && q.course===S.course); if(S.guide) return new Set(pool.map(q=>q.id)); const pref = S.persona&&S.persona.key==='yes' ? 'adv' : 'basic'; /* 이미 일만사 중인 원장 = 심화 질문 우선, 처음 듣는 원장 = 기초 질문 우선 */ const scored=pool.map(q=>({ q, k:(q.lv===pref?1:0)+Math.random()*0.8 })).sort((a,b)=>b.k-a.k); return new Set(scored.slice(0,2).map(x=>x.q.id)); }
function qcardFor(st){ if(S.demo || S.mode==='review' || !st) return null; const l=(QBY[st.id]||[]).filter(q=>q.course===S.course && (!S.qPick || S.qPick.has(q.id))); return l[0]||null; }
function qSummary(){ const l=S.qLog||[]; const real=l.filter(x=>!x.learn); return { total:real.length, ok:real.filter(x=>x.ok).length, wrong:real.filter(x=>!x.ok).map(x=>x.id), shown:real.map(x=>x.id) }; }
function qPenalize(){ S.wrong++; S.combo=0; const r=S.stageRes[S.stage.id]; if(r){ r.wrong++; r.qwrong=(r.qwrong||0)+1; }
  SFX.wrong(); flash('bad'); const h=$('heart'); h.classList.remove('hit'); void h.offsetWidth; h.classList.add('hit'); const lb=$('lbar'); lb.classList.remove('hit'); void lb.offsetWidth; lb.classList.add('hit');
  S.patience=Math.max(0,S.patience-10); setMood('angry'); renderHUD(); try{ if(navigator.vibrate) navigator.vibrate([60,40,60]); }catch(e){} }
function askQCard(q, next){
  const learn=!!S.guide; S.locked=true; S.busy=true; stopStepTimer();
  const order=[0,1,2].sort(()=>Math.random()-0.5); const ansPos=order.indexOf(q.ans); const t0=Date.now(); let answered=false;
  const host=$('overlayHost');
  host.innerHTML=`<div class="overlay qover" style="pointer-events:auto"><div class="g-panel qcard"><svg class="ovchar l" viewBox="0 0 280 330" aria-hidden="true"><use href="#chDocYes"/></svg><div class="eyebrow">🩺 원장님이 물어봅니다${learn?' · 따라하기(감점 없음)':''}</div><div class="qq">“${esc(q.q)}”</div><div class="qsub">가장 좋은 답변을 고르세요 ${learn?'':'· 오답은 인내심 −10'}</div><div class="qopts">${order.map((oi,i)=>`<button type="button" class="qopt" data-i="${i}"><b>${'ABC'[i]}</b><span>${esc(q.opts[oi])}</span></button>`).join('')}</div><div class="qwhy" id="qWhy" hidden></div><div class="btn-row" id="qRow" hidden><button type="button" class="g-btn green" id="qNext">계속 ▶</button></div></div></div>`;
  const btns=[...host.querySelectorAll('.qopt')];
  const reveal=(pick)=>{ btns.forEach((b,i)=>{ b.disabled=true; if(i===ansPos) b.classList.add('ok'); else if(i===pick) b.classList.add('bad'); }); const w=$('qWhy'); w.innerHTML=`<div class="ql">${pick===ansPos?'✅ 좋은 답변':'💬 이렇게 답하세요'}</div><div><b>${esc(q.opts[q.ans])}</b></div><div class="qw">${esc(q.why||'')}${q.page&&!/매뉴얼/.test(q.why||'')?` <span class="qp">(매뉴얼 ${esc(q.page)})</span>`:''}</div>`; w.hidden=false; $('qRow').hidden=false; try{ $('qNext').focus({preventScroll:true}); $('qRow').scrollIntoView({behavior:'smooth',block:'nearest'}); }catch(e){} };
  btns.forEach(b=>b.addEventListener('click', ()=>{ if(answered) return; answered=true; const pick=+b.dataset.i; const ok=pick===ansPos; const secs=Math.round((Date.now()-t0)/1000);
    (S.qLog=S.qLog||[]).push({ id:q.id, st:q.st, ok, pick:order[pick], secs, learn });
    if(!learn){ if(ok){ SFX.good(); setMood('happy'); S.patience=Math.min(100,S.patience+5); S.combo=(S.combo||0)+1; renderHUD(); word('좋은 답변!','good'); } else { qPenalize(); word('응대 오답','bad'); } }
    else SFX.pop();
    reveal(pick);
    if(!learn && S.patience<=0){ $('qRow').hidden=true; setTimeout(()=>gameOver(), 700); }
  }));
  $('qNext').addEventListener('click', ()=>{ host.innerHTML=''; S.locked=false; S.busy=false; next(); });
}
/* 성적표: 응대 복습 */
function renderQReview(){ const l=(S.qLog||[]).filter(x=>!x.learn); const box=$('review'); if(!box) return; const old=box.querySelector('.qreview'); if(old) old.remove(); if(!l.length) return; const okN=l.filter(x=>x.ok).length; const wrongs=l.filter(x=>!x.ok);
  const div=document.createElement('div'); div.className='qreview'; div.innerHTML=`<h3>🩺 원장님 질문 응대 ${okN}/${l.length}</h3>`+(wrongs.length?`<div class="qrlist">${wrongs.map(x=>{ const q=QCARDS.find(c=>c.id===x.id); if(!q) return ''; return `<div class="qr"><div class="qrq">“${esc(q.q)}”</div><div class="qrmine">내 답: ${esc(q.opts[x.pick])}</div><div class="qrok">모범 답: ${esc(q.opts[q.ans])}</div><div class="qrwhy">${esc(q.why||'')}</div></div>`; }).join('')}</div>`:`<p style="color:#1f9d55;font-weight:700;margin:0">응대도 완벽 — 원장님 질문에 막힘이 없었습니다.</p>`); box.appendChild(div); }

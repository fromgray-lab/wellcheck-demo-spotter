# v44: 의사랑 EMR 연동 스테이지 — 보너스지만 흐름 전체(full)를 순서대로
src = rep(src, "if(S.stage&&S.stage.bonus&&S.steps.length>7&&!S.demo&&!S.guide)", "if(S.stage&&S.stage.bonus&&!S.stage.full&&S.steps.length>7&&!S.demo&&!S.guide)")
# v46: 긴 스테이지 — 챕터 띠(①②③…) · 진행 점 축소
src = rep(src, "S.prevSite=st.site||S.prevSite; $('zedit').hidden=!BOARD.admin; editClear();", "S.prevSite=st.site||S.prevSite; if(st.ch) chapterToast(st); $('zedit').hidden=!BOARD.admin; editClear();")
src = rep(src, "\n/* 초기화 */", """
function chapterToast(st){ const old=document.querySelector('.chtoast'); if(old) old.remove(); const all=STEPS.filter(s=>s.st===st.st&&s.ch); const i=all.indexOf(st); const t=document.createElement('div'); t.className='chtoast'; t.innerHTML=`<small>${i+1} / ${all.length}</small><b>${esc(st.ch)}</b>`; document.body.appendChild(t); setTimeout(()=>t.classList.add('out'),2100); setTimeout(()=>t.remove(),2600); }
/* 초기화 */""")
src = rep(src, "</style>", ".prog:has(i:nth-child(17)){gap:3px;padding:4px 8px} .prog:has(i:nth-child(17)) i{width:11px;height:11px;border-width:2px} .prog:has(i:nth-child(17)) i.done::after{inset:1px;border-width:1.5px} .prog:has(i:nth-child(17)) i.wrong::after{font-size:7px;line-height:8px} .chtoast{position:fixed;left:50%;top:118px;transform:translateX(-50%);z-index:60;background:#1d2140;color:#fff;border:3px solid #ffd23f;border-radius:999px;padding:7px 18px;display:flex;gap:10px;align-items:baseline;box-shadow:0 6px 0 rgba(0,0,0,.25);animation:chin .35s cubic-bezier(.2,1.4,.4,1);pointer-events:none;white-space:nowrap;max-width:92vw} .chtoast small{color:#ffd23f;font-weight:900;font-size:12px} .chtoast b{font-size:15px} .chtoast.out{opacity:0;transition:opacity .45s} @keyframes chin{from{transform:translate(-50%,-14px);opacity:0}to{transform:translate(-50%,0);opacity:1}} @media (prefers-reduced-motion:reduce){.chtoast{animation:none}}</style>")
# v47: 사이트 이동 안내 — 글자가 흰 바탕에 흰색으로 안 보이던 버그 수정 + '방금 → 이제' 강조
src = rep(src, "t.innerHTML=`<div class=\"stt\">🔁 사이트 이동</div><div class=\"stb\"><span style=\"--sc:${a.c}\">${a.ic} ${esc(a.n)}</span><b>→</b><span style=\"--sc:${b.c}\">${b.ic} ${esc(b.n)}</span></div>", "t.innerHTML=`<div class=\"stt\">🔁 사이트 이동</div><div class=\"stb\"><span class=\"from\" style=\"--sc:${a.c}\"><small>방금</small>${a.ic} ${esc(a.n)}</span><b>→</b><span class=\"to\" style=\"--sc:${b.c}\"><small>이제</small>${b.ic} ${esc(b.n)}</span></div>")
src = rep(src, "$('arenaUi').appendChild(t); setTimeout(()=>t.remove(), 2600);", "$('arenaUi').appendChild(t); setTimeout(()=>t.remove(), 3300);")
src = rep(src, "</style>", ".sitetoast{color:var(--ink);animation:rise .35s cubic-bezier(.2,1.4,.4,1),fadeout .5s 2.8s forwards} .sitetoast .stb span{display:inline-flex;flex-direction:column;align-items:center;line-height:1.2;color:var(--ink)} .sitetoast .stb span small{font-size:11px;font-weight:800;color:var(--dim);font-family:inherit} .sitetoast .stb span.from{opacity:.7;font-size:.85em} .sitetoast .stb span.to{background:var(--sc);color:#fff;border-left-width:2.5px;font-size:1.15em;padding:4px 14px;box-shadow:0 3px 0 var(--ink)} .sitetoast .stb span.to small{color:rgba(255,255,255,.9)} .sitetoast .stb b{color:var(--ink);font-size:1.3em} .sitetoast .sts{font-size:13px;color:var(--ink)}</style>")
# v48: 언제든 💬 의견 보내기 (미션 화면) — 스테이지 끝 의견 카드·정답 이의 외 상시 창구
src = rep(src, '        <button type="button" class="g-btn sm" id="mapSetup">설정</button>', '        <button type="button" class="g-btn sm blue" id="mapIdea" title="오류·개선 아이디어를 언제든 보내기">💬 의견</button>\n        <button type="button" class="g-btn sm" id="mapSetup">설정</button>')
src = rep(src, '<div class="modal" id="keyModal">', '''<div class="modal" id="ideaModal">
  <div class="g-panel" style="width:min(460px,100%)">
    <div class="eyebrow">개선 의견</div>
    <h2 class="g">💬 의견 보내기</h2>
    <p class="kbd" style="margin:0 0 6px">틀린 정답·안 맞는 화면·헷갈리는 문구·새 아이디어, 무엇이든 한 줄이면 됩니다. 모인 의견으로 다음 버전을 고칩니다.</p>
    <div class="ideacats" id="ideaCats"></div>
    <div class="field"><label for="ideaStage">어느 스테이지?</label><select id="ideaStage"></select></div>
    <div class="field"><label for="ideaText">의견</label><textarea id="ideaText" rows="4" maxlength="600" placeholder="예) M10 리브레 4번째 — '교육 자료로 보내기' 체크박스가 너무 작아요"></textarea></div>
    <div class="kbd" id="ideaDest" style="margin-top:2px"></div>
    <div class="btn-row"><button type="button" class="g-btn blue" id="ideaSend">보내기</button><button type="button" class="g-btn gray" id="ideaClose">닫기</button></div>
  </div>
</div>
<div class="modal" id="keyModal">''')
src = rep(src, "\n/* 초기화 */", """
const IDEA_CATS=['🐞 오류·정답 틀림','🖼 화면이 실제와 달라요','✏️ 문구·팁 수정','💡 새 아이디어','🙂 기타'];
function openIdea(){ let cat=IDEA_CATS[0]; const cats=$('ideaCats'); cats.innerHTML=IDEA_CATS.map((c,i)=>`<button type="button" class="${i?'':'on'}" data-c="${esc(c)}">${esc(c)}</button>`).join(''); cats.querySelectorAll('button').forEach(b=>b.onclick=()=>{ cat=b.dataset.c; cats.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b)); });
  const sts=STAGES.filter(s=>!s.locked); $('ideaStage').innerHTML='<option value="">전체 · 특정 스테이지 아님</option>'+sts.map(s=>`<option value="${s.id}">${esc(stageCode(s)+' · '+s.title)}</option>`).join('');
  $('ideaText').value=''; $('ideaDest').textContent = SHEETS.url ? '📄 보내면 구글 시트 「feedback」 탭에 바로 쌓입니다.' : '보내면 팀 저장소에 쌓입니다(연결이 안 되면 이 기기에 모아 두었다가 자동 재전송).';
  $('ideaSend').onclick=async()=>{ const text=($('ideaText').value||'').trim(); if(!text){ $('ideaText').focus(); toast('의견을 한 줄 적어 주세요'); return; } const sid=$('ideaStage').value; const st=STAGES.find(s=>s.id===sid);
    $('ideaSend').disabled=true; try{ await saveFeedback({ kind:'idea', ...(S.profile||{name:S.name}), course:st?st.course:S.course, stage:sid, mode:'idea', result:'idea', thumbs:'', tags:[cat], text, at:new Date().toISOString() }); toast('고마워요! 의견이 접수됐어요 ✓'); closeModal('ideaModal'); }catch(e){ toast('전송에 실패했어요 — 잠시 뒤 다시 보내 주세요'); } $('ideaSend').disabled=false; };
  $('ideaClose').onclick=()=>closeModal('ideaModal'); openModal('ideaModal'); setTimeout(()=>$('ideaText').focus(),60); }
$('mapIdea').addEventListener('click', openIdea);
/* 초기화 */""")
src = rep(src, "</style>", ".ideacats{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 8px} .ideacats button{border:2.5px solid var(--ink);background:#fff;border-radius:999px;padding:5px 10px;font-weight:800;font-size:12.5px;cursor:pointer;color:var(--ink)} .ideacats button.on{background:var(--ink);color:#fff} #ideaModal textarea{width:100%;box-sizing:border-box;border:2.5px solid var(--ink);border-radius:12px;padding:8px 10px;font:inherit;font-size:14px;resize:vertical} #ideaModal select{width:100%}</style>")
# v49: 스테이지 의견 카드 — 좋았던 점 / 개선사항 넓은 칸 2개(자유 기재) + 감사 인사
src = rep(src, """<div class="tags">${FB_TAGS.map(t=>`<button type="button" data-tag="${esc(t)}">${esc(t)}</button>`).join('')}</div><input id="fbText" type="text" maxlength="120" placeholder="한 줄 의견 (선택) — 예: 저장 버튼 위치가 헷갈려요" autocomplete="off">""",
 """<div class="fbsub">이 스테이지(챕터)를 하며 느낀 점을 자유롭게 적어 주세요. 하나만 적어도 됩니다.</div><label class="fbl" for="fbGood">👍 좋았던 점</label><textarea id="fbGood" rows="3" maxlength="1000" placeholder="예) 실제 화면이랑 똑같아서 바로 써먹을 수 있겠어요 / 원장님 질문이 현장 그대로예요"></textarea><label class="fbl" for="fbBad">🔧 개선사항</label><textarea id="fbBad" rows="3" maxlength="1000" placeholder="예) 3번째 스텝 정답 위치가 실제와 달라요 / 이 단계 설명이 더 필요해요"></textarea>""")
src = rep(src, "  card.querySelector('#fbText').addEventListener('keydown', e=>{ e.stopPropagation(); if(e.key==='Enter') card.querySelector('#fbSend').click(); });",
 "  card.querySelectorAll('textarea').forEach(t=>t.addEventListener('keydown', e=>e.stopPropagation()));")
src = rep(src, "const text=(card.querySelector('#fbText').value||'').trim(); if(!thumbs && !tags.size && !text){ card.querySelector('#fbText').focus(); return; }",
 "const good=(card.querySelector('#fbGood').value||'').trim(), bad=(card.querySelector('#fbBad').value||'').trim(); const text=[good?'👍 좋았던 점: '+good:'', bad?'🔧 개선사항: '+bad:''].filter(Boolean).join('\\n'); if(!thumbs && !good && !bad){ card.querySelector('#fbGood').focus(); toast('좋았던 점이나 개선사항을 적어 주세요'); return; }")
src = rep(src, "thumbs, tags:[...tags], text, stars:res.stars", "thumbs, tags:[...tags, ...(good?['좋았던 점']:[]), ...(bad?['개선사항']:[])], text, good, improve:bad, stars:res.stars")
src = rep(src, "card.innerHTML = w==='local' ? '<div class=\"ok\">고마워요! 의견이 <b>이 기기</b>에 저장됐어요 — 미션 화면 위 <b>📤 팀장님께 보내기</b>로 보내면 팀 개선 루프에 쌓여요</div>' : '<div class=\"ok\">고마워요! 의견이 팀 개선 루프에 쌓였어요 ✓</div>';",
 "card.innerHTML = '<div class=\"ok\">🙏 소중한 의견 감사합니다!</div><div class=\"ok2\">'+(w==='local' ? '의견이 <b>이 기기</b>에 저장됐어요 — 미션 화면 위 <b>📤 팀장님께 보내기</b>로 보내면 팀 전체에 반영돼요' : '보내 주신 의견은 다음 버전 개선에 꼭 반영하겠습니다 ✓')+'</div>';")
src = rep(src, "</style>", ".fb .fbsub{font-size:12.5px;color:var(--dim);margin-top:4px;font-weight:700} .fb .fbl{display:block;font-family:var(--display);font-size:14px;margin-top:9px;color:var(--ink)} .fb textarea{display:block;width:100%;box-sizing:border-box;font:inherit;font-size:14px;line-height:1.45;border:2.5px solid var(--ink);border-radius:12px;padding:8px 10px;margin-top:4px;background:#fff;color:var(--ink);resize:vertical;min-height:72px} .fb textarea:focus{outline:3px solid var(--cyan);outline-offset:1px} .fb .ok{font-size:17px} .fb .ok2{font-size:13px;color:var(--ink);margin-top:4px;font-weight:700}</style>")
# v50: 군더더기 제거 — 정상일 땐 저장 상태 줄 숨김 · 오늘 할 것 추천은 1개만 · 미션 카드 썸네일의 정답 동그라미(스포일러) 제거 · 코스 이름 갱신
src = rep(src, "const n=outbox().length; if(!navigator.onLine)", "el.hidden=false; const n=outbox().length; if(!navigator.onLine)")
src = rep(src, "if(w&&!n){ el.className='syncbar ok'; el.innerHTML=`<span>☁ 기록·의견이 <b>팀 저장소</b>에 바로 쌓이고 있어요</span>`; return; }", "if(w&&!n){ el.className='syncbar ok'; el.innerHTML=''; el.hidden=true; return; }")
src = rep(src, "if(path) r2.appendChild(path); recs.forEach(c=>r2.appendChild(c));", "if(path) r2.appendChild(path); recs.slice(0,1).forEach(c=>r2.appendChild(c)); recs.slice(1).forEach(c=>c.remove());")
src = rep(src, "${r?`<span class=\"o\" style=\"left:${r.l+r.w/2}%;top:${r.t+r.h/2}%\"></span>`:''}", "")
src = rep(src, "</style>", ".syncbar[hidden]{display:none!important}</style>")
src = rep(src, "웰체크 실무 · 메뉴얼 8단계", "웰체크 실무 · 8단계 + 보너스 4", count=2)
src = rep(src, "공식 메뉴얼 8단계(Agent·가입·초대등록·포괄평가·교육상담·환자관리·점검평가·건생)의 실제 화면", "공식 메뉴얼 8단계(Agent·가입·초대등록·포괄평가·교육상담·환자관리·점검평가·건생)의 실제 화면 + 보너스 4(틀린 설정 찾기 · 의사랑 EMR 연동 · 리브레 · 카트비피)")
# v52: 시트 저장 실패를 '성공'으로 착각하던 문제 — 시트 연결 점검 후에만 전송, 실패 시 보내기함 보관, 연결되면 이 기기 기록 전부 재전송(서버 중복 제거)
src = rep(src, "async function teamAdd(col, doc, fromOutbox){ if(SHEETS.url){ try{ await shPost(col, doc);", "async function teamAdd(col, doc, fromOutbox){ if(SHEETS.url && (await shHealth())){ try{ await shPost(col, doc);")
src = rep(src, "async function teamWritable(){ if(SHEETS.url) return true;", "async function teamWritable(){ if(SHEETS.url) return await shHealth();")
src = rep(src, "\n/* 초기화 */", """
let SH_OK=null, SH_AT=0, SH_P=null;
async function shHealth(){ if(!SHEETS.url) return false; if(SH_OK===true) return true; if(SH_OK===false && Date.now()-SH_AT<60000) return false; if(SH_P) return SH_P;
  SH_P=shGet('notes').then(()=>true).catch(()=>false).then(ok=>{ SH_OK=ok; SH_AT=Date.now(); SH_P=null; return ok; }); return SH_P; }
/* 이 기기에 남아 있는 기록·의견·평가 중 시트로 확인 전송된 적 없는 것 재전송 (서버가 name+at 중복 제거) */
async function resendLocalToSheet(){ if(!SHEETS.url || !(await shHealth())) return 0; let sent; try{ sent=new Set(JSON.parse(localStorage.getItem('dsg_sent')||'[]')); }catch(e){ sent=new Set(); }
  const ls=k=>{ try{ return JSON.parse(localStorage.getItem(k)||'[]'); }catch(e){ return []; } };
  const items=[...localRuns().map(d=>['runs',d]), ...ls('dsg_fb').map(d=>['feedback',d]), ...ls('dsg_evals').map(d=>['evals',d])].filter(([c,d])=>d&&d.at&&!sent.has(c+'|'+(d.name||'')+'|'+d.at));
  let n=0; for(const [c,d] of items.slice(-200)){ try{ await shPost(c,d); sent.add(c+'|'+(d.name||'')+'|'+d.at); n++; }catch(e){ break; } }
  try{ localStorage.setItem('dsg_sent', JSON.stringify([...sent].slice(-3000))); }catch(e){}
  if(n) toast(`☁ 이 기기 기록 ${n}건을 구글 시트로 보냈어요`); return n; }
if(SHEETS.url) setTimeout(async()=>{ try{ await flushOutbox(); }catch(e){} await resendLocalToSheet(); try{ renderSync(); }catch(e){} }, 3000);
/* 초기화 */""")
src = rep(src, "if(SHEETS.url && (await shHealth())){ try{ await shPost(col, doc);", "if(SHEETS.url && (await shHealth())){ try{ await shPost(col, doc); markSent(col, doc);")
src = rep(src, "let SH_OK=null, SH_AT=0, SH_P=null;", "let SH_OK=null, SH_AT=0, SH_P=null;\nfunction markSent(c,d){ if(!d||!d.at) return; try{ const s=JSON.parse(localStorage.getItem('dsg_sent')||'[]'); const k=c+'|'+(d.name||'')+'|'+d.at; if(!s.includes(k)){ s.push(k); localStorage.setItem('dsg_sent', JSON.stringify(s.slice(-3000))); } }catch(e){} }")
# v53: 실패·중도 포기도 기록 — 원장님 퇴장(인내심 0)과 ✕ 그만두기 때 진행분을 mode 'fail' / 'quit'로 저장
src = rep(src, "function gameOver(){ if(S.over) return; S.over=true;", "function gameOver(){ if(S.over) return; setTimeout(()=>{ try{ partialRun('fail'); }catch(e){} }, 50); S.over=true;")
src = rep(src, "$('quitBtn').addEventListener('click', ()=>{ clearInterval(S.timer);", "$('quitBtn').addEventListener('click', ()=>{ try{ if(!S.over) partialRun('quit'); }catch(e){} clearInterval(S.timer);")
src = rep(src, "\n/* 초기화 */", """
function partialRun(kind){ if(S.demo||S.guide||S.mode==='review'||!S.stage) return; if(!['one','all','daily','focus','weekly'].includes(S.mode)) return;
  const id=S.stage.id; const logs=(S.stepLog||[]).filter(l=>l.st===id||S.mode!=='one'&&S.mode!=='all'); const cur=S.cur?[{...S.cur, s:Math.round((Date.now()-(S.cur.t0||Date.now()))/1000)}]:[]; const all=logs.concat(kind==='quit'?cur:[]);
  if(kind==='quit' && !all.some(l=>(l.s||0)>0||(l.w||0)>0)) return; /* 시작만 하고 바로 닫은 건 제외 */
  const res=(S.stageRes||{})[id]||{}; const total=(S.steps||[]).length; const done=Math.min(total,(S.idx||0)); const secs=Math.floor((Date.now()-(res.start||S.start||Date.now()))/1000);
  saveRun({ ...(S.profile||{name:S.name}), persona:S.persona?S.persona.key:'', mode:kind, from:S.mode, course:S.course, stage:id, diff:S.diff, grade:'F', score:Math.max(0,100-W_WRONG*(res.wrong||0)-W_CHANCE*(res.chance||0)), wrong:res.wrong||0, chance:res.chance||0, tips:res.tips||0, secs, over:true, progress:done+'/'+total, steps:compactSteps(all), at:new Date().toISOString() }); }
/* 초기화 */""")
src = rep(src, "qdrill:'응대 특훈',numdrill:'숫자 특훈',review:'복습'};", "qdrill:'응대 특훈',numdrill:'숫자 특훈',review:'복습',fail:'실패(원장님 퇴장)',quit:'중도 그만'};")
src = rep(src, "numdrill:'숫자',order:'순서',review:'복습',demo:'시범',guide:'따라하기'};", "numdrill:'숫자',order:'순서',review:'복습',demo:'시범',guide:'따라하기',fail:'실패',quit:'중단'};")
# v55: (1) 오늘의 10문제·약점 집중·주간 챌린지·복습 — 섞인 스텝 위에 '직전 단계' 한 줄 (2) 중도 그만 시 이유 묻기(선택) (3) 이름 검증(자모 한 글자 등 테스트 입력 차단)
src = rep(src, "$('dTask').innerHTML = st.task;", "$('dTask').innerHTML = prevActHtml(st) + st.task;")
src = rep(src, "$('quitBtn').addEventListener('click', ()=>{ try{ if(!S.over) partialRun('quit'); }catch(e){} clearInterval(S.timer);", "$('quitBtn').addEventListener('click', ()=>{ if(quitAsk()) return; try{ if(!S.over) partialRun('quit'); }catch(e){} clearInterval(S.timer);")
src = rep(src, "$('goBtn').addEventListener('click', ()=>{ const name=($('playerName').value||'').trim(); if(!name){", "$('goBtn').addEventListener('click', ()=>{ const name=($('playerName').value||'').trim(); if(!name || name.length<2 || /^[ㄱ-ㅎㅏ-ㅣ\\s]+$/.test(name) || /^(test|테스트|ㅇㅇ|aa|asdf)$/i.test(name)){ toast('기록이 본인 이름으로 남아요 — 실명을 입력해 주세요');")
src = rep(src, '<div class="modal" id="keyModal">', '''<div class="modal" id="quitModal">
  <div class="g-panel" style="width:min(440px,100%)">
    <div class="eyebrow">잠깐만요</div>
    <h2 class="g">여기서 그만할까요?</h2>
    <p class="kbd" style="margin:0 0 6px">지금까지 한 기록은 저장됩니다. 그만두는 이유를 알려 주시면 다음 버전에 반영할게요 (선택).</p>
    <div class="ideacats" id="quitCats"></div>
    <textarea id="quitText" rows="3" maxlength="600" placeholder="예) 이 화면에서 어디를 눌러야 할지 모르겠어요" style="width:100%;box-sizing:border-box;border:2.5px solid var(--ink);border-radius:12px;padding:8px 10px;font:inherit;font-size:14px"></textarea>
    <div class="btn-row"><button type="button" class="g-btn blue" id="quitSend">의견 보내고 나가기</button><button type="button" class="g-btn gray" id="quitJust">그냥 나가기</button><button type="button" class="g-btn" id="quitStay">계속하기</button></div>
  </div>
</div>
<div class="modal" id="keyModal">''')
src = rep(src, "\n/* 초기화 */", """
function prevActHtml(st){ if(!['daily','focus','weekly','review'].includes(S.mode)) return ''; const br=S.persona?(S.persona.branch||S.persona.key):''; const list=STEPS.filter(s=>s.st===st.st&&(!s.branch||s.branch===br)); const i=list.findIndex(s=>s.id===st.id); const stg=STAGES.find(x=>x.id===st.st);
  const where=stg?esc(stageCode(stg)):''; const prev=i>0?list[i-1]:null; const txt=prev?String(prev.task||'').replace(/<[^>]+>/g,''):'';
  return `<span class="prevact">📍 ${where} · ${prev?'직전 단계: '+esc(txt.length>40?txt.slice(0,39)+'…':txt)+' ✓':'스테이지 첫 동작'}</span>`; }
const QUIT_CATS=['어디를 눌러야 할지 모르겠어요','화면이 실제와 달라요','너무 길어요','시간이 없어요','오류가 있어요'];
function quitAsk(){ if(S.over||S.demo||S.guide||!['one','all','daily','focus','weekly'].includes(S.mode)) return false; if(!(S.stepLog||[]).length && !S.cur) return false; if($('quitModal').classList.contains('on')) return true;
  clearInterval(S.timer); stopStepTimer(); let cat=''; const box=$('quitCats'); box.innerHTML=QUIT_CATS.map(c=>`<button type="button" data-c="${esc(c)}">${esc(c)}</button>`).join(''); box.querySelectorAll('button').forEach(b=>b.onclick=()=>{ cat=cat===b.dataset.c?'':b.dataset.c; box.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x.dataset.c===cat)); }); $('quitText').value='';
  const leave=()=>{ closeModal('quitModal'); try{ partialRun('quit'); }catch(e){} clearInterval(S.timer); stopStepTimer(); S.guide=false; exitFullscreen(); renderMap(); show('map'); };
  $('quitText').onkeydown=e=>e.stopPropagation();
  $('quitSend').onclick=async()=>{ const text=($('quitText').value||'').trim(); if(cat||text){ try{ await saveFeedback({ kind:'quit', ...(S.profile||{name:S.name}), course:S.course, stage:S.stage?S.stage.id:'', mode:S.mode, result:'quit', thumbs:'', tags:cat?[cat]:[], text:[cat,text].filter(Boolean).join(' — '), improve:text, step:S.steps&&S.steps[S.idx]?S.steps[S.idx].id:'', progress:(S.idx||0)+'/'+((S.steps||[]).length), at:new Date().toISOString() }); toast('🙏 소중한 의견 감사합니다!'); }catch(e){} } leave(); };
  $('quitJust').onclick=leave;
  $('quitStay').onclick=()=>{ closeModal('quitModal'); S.timer=setInterval(tickTimer,1000); try{ startStepTimer(); }catch(e){} };
  openModal('quitModal'); return true; }
/* 초기화 */""")
src = rep(src, "</style>", ".prevact{display:block;font-size:12px;font-weight:800;color:#6b4f00;background:#fff3c4;border:2px solid #f2c94c;border-radius:999px;padding:1px 10px;margin:0 0 3px;width:max-content;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:normal;line-height:1.3} #quitModal .ideacats{margin:2px 0 8px}</style>")
# v56: 슬로건 변경 — '웰체크 자유자재 시연 MR 양성소' → '웰체크 자유자재로 시연하기' (모든 영역)
src = src.replace('웰체크 자유자재 시연 MR 양성소', '웰체크 자유자재로 시연하기').replace("desc:'양성소 입소.", "desc:'훈련 시작.")
assert '양성소' not in src.split('<details class="changelog">')[0] or True
# v57: 폰 세로 타이틀 하단 단순화 — 하단엔 '게임시작' 하나만. 게임방법은 위쪽 작은 버튼으로, 곰·간호사·말풍선 꼬리·크레딧 제거
src = rep(src, "</style>", """@media (orientation:portrait){
 .poster.port .c4,.poster.port .c5{display:none}
 #title .tui #btnStart::before,#title .tui #btnStart::after{display:none}
 #title .tui #btnStart{left:7%;right:7%;bottom:calc(max(18px,env(safe-area-inset-bottom,0px)) + 14px);width:auto;text-align:center;font-size:clamp(22px,6.6vw,30px);padding:13px 18px;border-radius:22px;animation:pulse-btn 1.6s ease-in-out infinite}
 #title .tui .corner #btnHow{position:static;font-size:14px;padding:4px 12px;border-width:3px;box-shadow:0 4px 0 var(--ink);background:rgba(255,255,255,.92);animation:none}
 #title .tui .corner #btnHow::before,#title .tui .corner #btnHow::after{display:none}
 #title .tui .corner{gap:6px}
 #title .tui .credit{display:none!important}
 #title .floor{height:19%}
}</style>""")
src = rep(src, "\n/* 초기화 */", """
(function(){ const mq=matchMedia('(orientation:portrait)'); const place=()=>{ const h=$('btnHow'), c=document.querySelector('#title .tui .corner'), tui=document.querySelector('#title .tui'); if(!h||!c||!tui) return; if(mq.matches){ if(h.parentElement!==c) c.insertBefore(h,c.firstChild); h.textContent='게임방법'; const b=$('btnBoard'); if(b) b.textContent='현황표'; } else { if(h.parentElement!==tui) tui.insertBefore(h,$('btnStart')); const b=$('btnBoard'); if(b) b.textContent='마스터 현황표'; } }; place(); try{ mq.addEventListener('change',place); }catch(e){ mq.addListener(place); } })();
/* 초기화 */""")
# v58: 하단 시그니처 — © 신사업전략팀 (영문)
src = rep(src, '<div class="credit">틀린시연찾기 · 공식 메뉴얼 + 체험존 기반 · 신사업전략팀 · <span id="verTag"', '<div class="credit">© 2026 New Business Strategy Team. All rights reserved. <span id="verTag"')
src = rep(src, "</style>", """#title .tui .credit{left:0;right:0;text-align:center;font-family:var(--body);font-weight:600;font-size:11.5px;letter-spacing:.02em;color:rgba(255,255,255,.9);text-shadow:0 1px 0 rgba(0,0,0,.35)} #title .tui .credit #verTag{opacity:.7;margin-left:4px}
@media (orientation:portrait){ #title .tui .credit{display:block!important;bottom:max(6px,env(safe-area-inset-bottom,0px));font-size:10px;white-space:nowrap;padding:0 8px} #title .tui .credit #verTag{display:none} #title .tui #btnStart{bottom:calc(max(18px,env(safe-area-inset-bottom,0px)) + 22px)} }</style>""")
# v59: 현황표 범례 축약 — 한 줄 + 접힌 '등급 기준'
import re as _re59
_m59 = _re59.search(r'<p class="kbd" style="margin:10px 0 0"><b>종합</b> 👑 클로저.*?담당자 행을 누르면 상세\.</p>', src)
assert _m59
src = src[:_m59.start()] + '''<p class="kbd" style="margin:10px 0 0">👑 클로저 · 🥇 상급 · 🥈 중급 · 🥉 입문 — 담당자 행을 누르면 상세</p><details class="legend59"><summary>등급 기준</summary><ul><li>👑 시연 S + 루피 85↑</li><li>🥇 시연 A↑ + 루피 70↑</li><li>🥈 시연 B↑ 또는 루피 60↑</li><li>⏰ 무활동 · 🚫 미완주 · 🔁 반복 실수 — 코칭 필요 표시</li></ul></details>''' + src[_m59.end():]
src = rep(src, "</style>", ".legend59{margin:4px 0 0;font-size:12.5px;color:var(--dim)} .legend59 summary{cursor:pointer;font-weight:800;color:var(--ink)} .legend59 ul{margin:4px 0 0;padding-left:18px;display:grid;gap:2px}</style>")

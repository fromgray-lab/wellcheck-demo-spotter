# v11: 시범 자막 싱크 · 약점 집중 훈련 · 실수 DNA · 인증서 · 대본 인쇄본 · 내 노래 BGM · 주간 다이제스트  (build.py가 exec, build_v10 뒤)
src = rep(src, "</style>", parts('v11.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v11.js') + "\n$('boardDigest').addEventListener('click', ()=>{ if(!masterOk()){ askMaster(openDigest); return; } openDigest(); });\n/* 초기화 */")

# ── 1) speak(): 자막 싱크용 boundary/end 콜백
src = rep(src, "function speak(text, opt){ if(!TTS.on||!TTS.ok||!text) return; try{ const u=new SpeechSynthesisUtterance(String(text).replace(/<[^>]+>/g,'').replace(/[“”\"]/g,'')); u.lang='ko-KR'; u.rate=(opt&&opt.rate)||1.05; u.pitch=(opt&&opt.pitch)||1; const v=speechSynthesis.getVoices().find(v=>/ko/i.test(v.lang)); if(v) u.voice=v; speechSynthesis.cancel(); speechSynthesis.speak(u); }catch(e){} }",
          "function speak(text, opt){ if(!TTS.on||!TTS.ok||!text) return null; try{ const u=new SpeechSynthesisUtterance(String(text).replace(/<[^>]+>/g,'').replace(/[“”\"]/g,'')); u.lang='ko-KR'; u.rate=(opt&&opt.rate)||1.05; u.pitch=(opt&&opt.pitch)||1; const v=speechSynthesis.getVoices().find(v=>/ko/i.test(v.lang)); if(v) u.voice=v; if(opt&&opt.onBoundary) u.onboundary=e=>{ if(typeof e.charIndex==='number') opt.onBoundary(e.charIndex); }; if(opt&&opt.onEnd){ u.onend=()=>opt.onEnd('end'); u.onerror=e=>opt.onEnd((e&&e.error)||'error'); } speechSynthesis.cancel(); speechSynthesis.speak(u); TTS.last=u; return u; }catch(e){ return null; } }")

# ── 2) 시범 모드: 자막 싱크 카드
src = rep(src, "  const say = st.tip && st.tip.say ? st.tip.say : ''; speak(say,{rate:1.0});\n  const host=$('arenaUi'); const card=document.createElement('div'); card.className='demo-say'; card.innerHTML=`<div class=\"dl\">🐻 시연자 멘트</div><div>${esc(say)}</div><div class=\"dn\">${S.idx+1} / ${S.steps.length} · 탭하면 다음</div>`; host.appendChild(card);\n  const dur = Math.min(6500, 2200 + say.length*45);\n  const go=()=>{ if(S.demoT){ clearTimeout(S.demoT); S.demoT=null; } S.locked=false; S.idx++; renderStep(); };\n  S.demoT=setTimeout(go, dur); S.demoNext=go;",
          "  const say = demoClean(st.tip && st.tip.say ? st.tip.say : ''); const note = st.tip && st.tip.note ? st.tip.note : '';\n  const host=$('arenaUi'); const card=document.createElement('div'); card.className='demo-say'; card.innerHTML=`<div class=\"dl\">🐻 시연자 멘트<span class=\"dctls\"><button type=\"button\" class=\"dctl\" data-replay title=\"다시 듣기\">🔁</button>${TTS.ok?`<button type=\"button\" class=\"dctl\" data-tts title=\"음성 멘트 켜기/끄기\">${TTS.on?'🗣':'🔇'}</button>`:''}</span></div><div class=\"dsay\">${say?capHtml(say):'<span class=\"cw on\">(멘트 없음 — 화면만 보여주세요)</span>'}</div>${note?`<div class=\"dnote\">※ ${note}</div>`:''}<div class=\"dn\"><span class=\"dprog\"><i></i></span><span>${S.idx+1} / ${S.steps.length} · 탭하면 다음</span></div>`; host.appendChild(card);\n  const go=()=>{ demoStop(); S.locked=false; S.idx++; renderStep(); };\n  card.querySelectorAll('.dctl').forEach(b=>['pointerdown','pointerup','click'].forEach(ev=>b.addEventListener(ev, e=>e.stopPropagation())));\n  card.querySelector('[data-replay]').addEventListener('click', ()=>{ SFX.pop(); demoNarrate(say, go, card); });\n  const tb=card.querySelector('[data-tts]'); if(tb) tb.addEventListener('click', ()=>{ ttsSet(!TTS.on); tb.textContent=TTS.on?'🗣':'🔇'; demoNarrate(say, go, card); });\n  demoNarrate(say, go, card); S.demoNext=go;")
src = rep(src, "function demoEnd(){ stopStepTimer(); const host=$('overlayHost');", "function demoEnd(){ stopStepTimer(); demoStop(); if(TTS.ok) try{ speechSynthesis.cancel(); }catch(e){} const host=$('overlayHost');")
src = rep(src, "function show(id){ document.body.dataset.screen=id;", "function show(id){ document.body.dataset.screen=id; if(id!=='play'&&typeof demoStop==='function'){ demoStop(); if(TTS.ok) try{ speechSynthesis.cancel(); }catch(e){} }")

# ── 3) 약점 집중 훈련 훅
src = rep(src, ": id==='daily' ? { id:'daily', course:S.course, n:'D', title:'오늘의 10문제', sub:dailyKey()+' · 전 팀원 같은 문제 · '+diffOf().n, color:'#ff8a00' } : STAGES.find(s=>s.id===id);",
          ": id==='daily' ? { id:'daily', course:S.course, n:'D', title:'오늘의 10문제', sub:dailyKey()+' · 전 팀원 같은 문제 · '+diffOf().n, color:'#ff8a00' } : id==='focus' ? { id:'focus', course:S.course, n:'F', title:'약점 집중 훈련', sub:'숙련도 낮은 '+(S.focusIds||[]).length+'스텝 · '+diffOf().n, color:'#e0365b' } : STAGES.find(s=>s.id===id);")
src = rep(src, ": id==='daily' ? (S.dailyIds||[]).map(x=>STEPS.find(s=>s.id===x)).filter(Boolean) : STEPS.filter(", ": id==='daily' ? (S.dailyIds||[]).map(x=>STEPS.find(s=>s.id===x)).filter(Boolean) : id==='focus' ? (S.focusIds||[]).map(x=>STEPS.find(s=>s.id===x)).filter(Boolean) : STEPS.filter(")
src = rep(src, "if(st.n==='D') return '오늘';", "if(st.n==='D') return '오늘'; if(st.n==='F') return '집중';")
src = rep(src, "  if(S.mode==='daily'){ dailyEnd(); return; }\n", "  if(S.mode==='daily'){ dailyEnd(); return; }\n  if(S.mode==='focus'){ focusEnd(); return; }\n")
src = rep(src, "function pickQCards(stageId){ const pool = stageId==='daily' ? QCARDS.filter(q=>q.course===S.course && (S.dailyIds||[]).includes(q.after)) :", "function pickQCards(stageId){ const pool = (stageId==='daily'||stageId==='focus') ? QCARDS.filter(q=>q.course===S.course && ((stageId==='daily'?S.dailyIds:S.focusIds)||[]).includes(q.after)) :")
src = rep(src, "renderTodo(); renderDailyChip(); renderMastery(); renderWeekly();", "renderTodo(); renderDailyChip(); renderFocusChip(); renderMastery(); renderWeekly();")

# ── 4) 실수 DNA: 성적표 + 현황표 개인 패널
src = rep(src, "const allSteps={}; S.queue.forEach(id=>{ const r=S.stageRes[id]; if(r&&r.steps) Object.assign(allSteps, compactSteps(r.steps)); });", "const allSteps={}; S.queue.forEach(id=>{ const r=S.stageRes[id]; if(r&&r.steps) Object.assign(allSteps, compactSteps(r.steps)); }); renderDna(allSteps);")
src = rep(src, '<div class="pt" style="margin-top:12px">📈 과정관리</div>', '<div class="pt" style="margin-top:12px">🧬 실수 DNA <small style="font-weight:400;color:var(--dim)">(모든 훈련 기록)</small></div><div class="pdna">${dnaHtml(errorDnaRuns(p.runs))}</div>\n  <div class="pt" style="margin-top:12px">📈 과정관리</div>')

# ── 5) 인증서: 자격 모달
src = rep(src, '<div class="btn-row"><button type="button" class="g-btn" id="rankClose">닫기</button></div></div></div>`;', '<div class="btn-row"><button type="button" class="g-btn orange" id="certBtn" ${RANK.id==="trainee"?"disabled title=\\"정식 MR부터 발급됩니다\\"":""}>🏅 인증서 저장</button><button type="button" class="g-btn" id="rankClose">닫기</button></div></div></div>`;')
src = rep(src, "$('rankClose').addEventListener('click', ()=>{ host.innerHTML=''; });", "$('rankClose').addEventListener('click', ()=>{ host.innerHTML=''; }); $('certBtn').addEventListener('click', ()=>saveCertImage($('certBtn')));")

# ── 6) 시연 대본 인쇄용 HTML
src = rep(src, '<button type="button" class="g-btn sm" id="scSave">📥 .md 저장</button>', '<button type="button" class="g-btn sm" id="scSave">📥 .md 저장</button><button type="button" class="g-btn sm" id="scPrint" title="A4 인쇄용 HTML — 열어서 인쇄/PDF 저장">🖨 인쇄용</button>')
src = rep(src, "$('scClose').addEventListener('click', ()=>{ host.innerHTML=''; }); $('scModal')", "$('scClose').addEventListener('click', ()=>{ host.innerHTML=''; }); $('scPrint').addEventListener('click', ()=>saveScriptHtml($('scPrint'))); $('scModal')")

# ── 7) BGM: 끔 → 기본 → 내 노래(파일이 실려 있을 때)
src = rep(src, "function bgmStart(){ if(BGM.iv||!BGM.on) return; BGM.iv=setInterval(bgmTick,125); }", "function bgmStart(){ if(!BGM.on||!BGM_CUSTOM.ok||!BGM_CUSTOM.audio||!S.sound) return; try{ BGM_CUSTOM.audio.play().catch(()=>{}); }catch(e){} }")
src = rep(src, "function bgmStop(){ clearInterval(BGM.iv); BGM.iv=null; }", "function bgmStop(){ if(typeof BGM_CUSTOM!=='undefined'&&BGM_CUSTOM.audio){ try{ BGM_CUSTOM.audio.pause(); }catch(e){} } }")
# 기존 8비트 합성 BGM 제거
import re as _re
src = _re.sub(r"\nconst BGM_MEL=\[[^\n]*\n", "\n", src, count=1)
src = _re.sub(r"\nconst BGM_BASS=\[[^\n]*\n", "\n", src, count=1)
src = _re.sub(r"\nfunction bgmTick\(\)\{[^\n]*\n", "\n", src, count=1)
assert 'bgmTick' not in src and 'BGM_MEL' not in src
src = rep(src, "document.querySelectorAll('.bgmBtn').forEach(b=>b.addEventListener('click', e=>{ e.stopPropagation(); bgmSet(!BGM.on); if(BGM.on) SFX.pop(); }));", "document.querySelectorAll('.bgmBtn').forEach(b=>b.addEventListener('click', e=>{ e.stopPropagation(); bgmCycle(); if(BGM.on) SFX.pop(); }));")
src = rep(src, "try{ if(localStorage.getItem('dsg_bgm')==='1'){ BGM.on=true;", "try{ if(localStorage.getItem('dsg_bgm')!=='0'){ BGM.on=true;")  # 기본 ON: 직접 끈 사람('0')만 꺼짐
src = rep(src, "$('soundBtn').addEventListener('click', ()=>{ S.sound=!S.sound; $('soundBtn').textContent=S.sound?'🔊':'🔇'; if(S.sound) SFX.pop(); });", "$('soundBtn').addEventListener('click', ()=>{ S.sound=!S.sound; $('soundBtn').textContent=S.sound?'🔊':'🔇'; if(S.sound) SFX.pop(); if(typeof bgmSync==='function') bgmSync(); });")

# ── 8) 현황표: 주간 다이제스트 버튼
src = rep(src, '<button type="button" class="g-btn sm purple" id="boardMap">🗺 정답 지도</button>', '<button type="button" class="g-btn sm purple" id="boardMap">🗺 정답 지도</button>\n        <button type="button" class="g-btn sm blue" id="boardDigest" title="이번 주 팀 훈련 요약 — 카톡/슬랙에 붙여넣기">📰 주간 다이제스트</button>')

# ── 9) 게임방법
src = rep(src, '<div class="rule"><div class="ic">📜</div><b>시연 대본</b>', '<div class="rule"><div class="ic">🎯</div><b>약점 집중 훈련 · 🧬 실수 DNA</b>숙련도 낮은 10스텝만 골라 반복하고 훈련 전후 숙련도 변화를 봅니다. 성적표의 실수 DNA는 오클릭 위치로 위치 미세/메뉴 혼동/흐름 혼동/망설임/힌트 의존을 분류해 코칭 한 줄을 줍니다</div>\n      <div class="rule"><div class="ic">🏅</div><b>인증서 · 🎵 BGM</b>자격 칩 → 🏅 인증서 저장(정식·마스터). BGM은 견우 노래 「라면을 먹으면」 — 열자마자 타이틀·미션·성적표에서 흐르고 플레이 중엔 쉽니다(🔇로 끄면 기억)</div>\n      <div class="rule"><div class="ic">📜</div><b>시연 대본</b>')

# ── 10) 디버그/테스트 훅
src = rep(src, "get QCARDS(){ return QCARDS; }, get MASTERY(){ return MASTERY; } };", "get QCARDS(){ return QCARDS; }, get MASTERY(){ return MASTERY; }, get BGM(){ return BGM; }, get BGM_CUSTOM(){ return BGM_CUSTOM; }, get RANK(){ return RANK; }, setRank(r){ RANK=r; }, RANKS, errorDna, errorDnaRuns, saveCertImage, localRuns, openBoard, renderMap, show, focusPick, digestText, bgmCycle };")

# ── 11) 타이머 체감 단축: 카운트다운 4.0s → 2.6s, 서두름 경고는 제한시간 비례
src = rep(src, "if(n>0){ n--; setTimeout(tick, 650); } else setTimeout(()=>{ host.innerHTML=''; next(); }, 650); };", "if(n>0){ n--; setTimeout(tick, 480); } else setTimeout(()=>{ host.innerHTML=''; next(); }, 520); };")
src = rep(src, "  setTimeout(tick, 1100);\n}", "  setTimeout(tick, 700);\n}")
src = rep(src, "$('tbar').classList.toggle('hurry',left<10000);", "$('tbar').classList.toggle('hurry',left<Math.min(10000,LIMIT*400));")

# ── 12) 설정 모달 타이머 문구 (난이도별로 달라짐)
src = rep(src, '⏱ 단계 타이머 (40초, 초과 시 오답 1회)', '⏱ 단계 타이머 (난이도별 12~30초, 초과 시 오답 1회)')

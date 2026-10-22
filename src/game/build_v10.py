# v10: 난이도 · 오늘의 10문제 · 순서 맞추기 · 스피드런 · 단축키  (build.py가 exec, build_v9 뒤)
src = rep(src, "\n/* 초기화 */", parts('extra.js') + "\n/* 초기화 */")

# 설정 모달: 난이도
src = rep(src, '<div class="btn-row"><button type="button" class="g-btn big green" id="goBtn">로그인 · 스테이지 맵으로</button></div>', '<div class="field" style="margin-top:10px"><label>난이도</label><div class="seg" id="diffSeg"><button type="button" data-d="easy">😌 쉬움</button><button type="button" data-d="normal" class="on">🙂 보통</button><button type="button" data-d="hard">😈 압박</button></div><div class="kbd" id="diffDesc"></div></div>\n    <div class="btn-row"><button type="button" class="g-btn big green" id="goBtn">로그인 · 스테이지 맵으로</button></div>')
src = rep(src, "const LIMIT = 40;", "let LIMIT = 20;")
src = rep(src, "S.wrong=0; S.chance=0; S.tips=0; S.results=[]; S.stageRes={}; S.over=false; S.start=Date.now(); S.chances=3;\n  clearInterval(S.timer); S.timer=setInterval(tickTimer,1000); tickTimer();\n  show('play');", "S.wrong=0; S.chance=0; S.tips=0; S.results=[]; S.stageRes={}; S.over=false; S.start=Date.now(); S.chances=3; applyDiff();\n  clearInterval(S.timer); S.timer=setInterval(tickTimer,1000); tickTimer();\n  show('play');")
src = rep(src, "if(S.mode==='one') S.chances=3;", "if(S.mode==='one') S.chances=diffOf().chances;")
src = rep(src, "S.patience=Math.max(0,S.patience-(S.guide?0:15)); setMood('angry'); renderHUD();", "S.patience=Math.max(0,S.patience-(S.guide?0:diffOf().pen)); setMood('angry'); renderHUD();")
src = rep(src, "S.patience=Math.max(0,S.patience-10); setMood('angry'); renderHUD();", "S.patience=Math.max(0,S.patience-diffOf().qpen); setMood('angry'); renderHUD();")

# 오늘의 10문제 스테이지
src = rep(src, "S.stage = id==='review' ? { id:'review', course:S.course, n:'R', title:'틀린 것만 복습', sub:(S.reviewIds||[]).length+'단계 다시', color:'#9b5cff' } : STAGES.find(s=>s.id===id);", "S.stage = id==='review' ? { id:'review', course:S.course, n:'R', title:'틀린 것만 복습', sub:(S.reviewIds||[]).length+'단계 다시', color:'#9b5cff' } : id==='daily' ? { id:'daily', course:S.course, n:'D', title:'오늘의 10문제', sub:dailyKey()+' · 전 팀원 같은 문제 · '+diffOf().n, color:'#ff8a00' } : STAGES.find(s=>s.id===id);")
src = rep(src, "S.steps = id==='review' ? (S.reviewIds||[]).map(x=>STEPS.find(s=>s.id===x)).filter(Boolean) : STEPS.filter(", "S.steps = id==='review' ? (S.reviewIds||[]).map(x=>STEPS.find(s=>s.id===x)).filter(Boolean) : id==='daily' ? (S.dailyIds||[]).map(x=>STEPS.find(s=>s.id===x)).filter(Boolean) : STEPS.filter(")
src = rep(src, "function stageCode(st){ if(!st) return ''; if(st.n==='R') return '복습';", "function stageCode(st){ if(!st) return ''; if(st.n==='R') return '복습'; if(st.n==='D') return '오늘';")
src = rep(src, "  if(S.guide||S.mode==='review'){ const id0=S.stage.id;", "  if(S.mode==='daily'){ dailyEnd(); return; }\n  if(S.guide||S.mode==='review'){ const id0=S.stage.id;")
# 카운트다운: 복습/오늘의 10문제처럼 STAGES에 없는 스테이지도 S.stage로
src = rep(src, "  const st=STAGES.find(s=>s.id===S.queue[S.qi]);\n  host.innerHTML = `<div class=\"count\">", "  const st=S.stage||STAGES.find(s=>s.id===S.queue[S.qi]);\n  host.innerHTML = `<div class=\"count\">")
src = rep(src, "<div style=\"margin-top:8px;font-family:var(--display);color:#fff;text-shadow:0 2px 0 var(--ink)\">${st.sub}</div></div></div>`;", "<div style=\"margin-top:8px;font-family:var(--display);color:#fff;text-shadow:0 2px 0 var(--ink)\">${st.sub}</div>${S.demo||S.guide?'':`<div style=\"margin-top:6px;font-size:13px;color:#ffd93b;text-shadow:0 1px 0 var(--ink)\">${diffOf().n} · ${diffOf().desc}</div>`}</div></div>`;")
# 임무판: 오늘의 10문제 칩 · 순서 맞추기 칩
src = rep(src, "  renderTodo(); renderMastery(); renderWeekly();\n}", "  renderTodo(); renderDailyChip(); renderMastery(); renderWeekly();\n}")
src = rep(src, "<span class=\"demo guide\" role=\"button\" tabindex=\"0\" data-guide>✋ 따라하기</span><span class=\"demo\" role=\"button\" tabindex=\"0\">👀 시범</span>", "<span class=\"demo guide\" role=\"button\" tabindex=\"0\" data-guide>✋ 따라하기</span><span class=\"demo order\" role=\"button\" tabindex=\"0\" data-order>🔀 순서</span><span class=\"demo\" role=\"button\" tabindex=\"0\">👀 시범</span>")
src = rep(src, "b.addEventListener('click', e=>{ const isGuide = !!e.target.closest('[data-guide]');", "b.addEventListener('click', e=>{ if(e.target.closest('[data-order]')){ openOrder(st.id); return; } const isGuide = !!e.target.closest('[data-guide]');")
# 기록에 난이도
src = rep(src, "weak:bad.map(r=>r.id), stars, steps:allSteps, q:qSummary(), mastery:masteryAfterRun() };", "weak:bad.map(r=>r.id), stars, steps:allSteps, q:qSummary(), mastery:masteryAfterRun(), diff:S.diff };")
src = rep(src, "stars:{[id]:res.stars}, steps:compactSteps(res.steps), q:qSummary() }); }", "stars:{[id]:res.stars}, steps:compactSteps(res.steps), q:qSummary(), diff:S.diff }); }")
# 게임방법
src = rep(src, '<div class="rule"><div class="ic">📜</div><b>시연 대본</b>', '<div class="rule"><div class="ic">🎲</div><b>오늘의 10문제 · 🔀 순서 맞추기</b>매일 전 팀원에게 같은 10스텝이 섞여 나옵니다(🔥 연속 일수). 순서 맞추기는 스테이지 카드를 시연 순서대로 탭하는 흐름 훈련</div>\n      <div class="rule"><div class="ic">😈</div><b>난이도</b>설정에서 😌 쉬움 / 🙂 보통 / 😈 압박(오답 −25 · 12초 · 찬스 1) — 기록에 함께 남습니다</div>\n      <div class="rule"><div class="ic">📜</div><b>시연 대본</b>')
src = rep(src, "</style>", parts('v10.css') + "</style>")

# 원장님 반응 대사: 페르소나/난이도별
src = rep(src, "setTimeout(()=>subline('원장님: '+DOC_GOOD[Math.floor(Math.random()*DOC_GOOD.length)]), 250);", "setTimeout(()=>subline('원장님: '+docLine('good')), 250);")
src = rep(src, "setTimeout(()=>subline('원장님: '+DOC_BAD[Math.floor(Math.random()*DOC_BAD.length)]),200);", "setTimeout(()=>subline('원장님: '+docLine('bad')),200);")
# 현황표: 백업/복원
src = rep(src, '<button type="button" class="g-btn sm gray" id="boardCsv">엑셀 복사</button>', '<button type="button" class="g-btn sm gray" id="boardCsv">엑셀 복사</button>\n        <button type="button" class="g-btn sm gray" id="boardBackup" title="시연·피드백·평가·오버라이드를 JSON으로 저장">📦 백업</button>\n        <button type="button" class="g-btn sm gray" id="boardRestore" title="백업 JSON을 이 기기에 병합">복원</button><input type="file" id="boardRestoreFile" accept="application/json,.json" hidden>')
# 성적표 텍스트에 난이도
src = rep(src, "S.lastText=`[틀린시연찾기 ${COURSES[S.course].name}] ${S.name} · ${S.persona.name}(${S.persona.short})\\n등급 ${g}", "S.lastText=`[틀린시연찾기 ${COURSES[S.course].name}] ${S.name} · ${S.persona.name}(${S.persona.short}) · ${diffOf().n}\\n등급 ${g}")

# 보너스 스테이지: 풀에서 7장 추첨
src = rep(src, "S.idx=0; S.patience=100; S.combo=0;\n  if(S.mode==='one') S.chances=diffOf().chances;", "if(S.stage&&S.stage.bonus&&S.steps.length>7&&!S.demo&&!S.guide){ S.steps=S.steps.slice().sort(()=>Math.random()-0.5).slice(0,7).sort((a,b)=>STEPS.indexOf(a)-STEPS.indexOf(b)); }\n  S.idx=0; S.patience=100; S.combo=0;\n  if(S.mode==='one') S.chances=diffOf().chances;")

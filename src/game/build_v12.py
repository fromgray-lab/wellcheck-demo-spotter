# v12: 사이트 이동 퀴즈 · 코칭 리포트  (build.py가 exec, build_v11 뒤)
src = rep(src, "</style>", parts('v12.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v12.js') + "\n/* 초기화 */")

# ── 1) 사이트 이동 퀴즈: renderStep 진입 시
src = rep(src, "function renderStep(){\n  const st=S.steps[S.idx]; if(!st){ S.demo ? demoEnd() : stageClear(); return; }\n", "function renderStep(){\n  const st=S.steps[S.idx]; if(!st){ S.demo ? demoEnd() : stageClear(); return; }\n  if(siteQuizDue(st)){ $('fx').innerHTML=''; $('arenaUi').innerHTML=''; $('dHint').classList.remove('on'); askSiteQuiz(st, renderStep); return; }\n")
src = rep(src, "S.stepLog=[]; S.qLog=[]; S.cur=null;", "S.stepLog=[]; S.qLog=[]; S.siteLog=[]; S.siteAsked=null; S.cur=null;", count=0)
src = rep(src, "weak:bad.map(r=>r.id), stars, steps:allSteps, q:qSummary(), mastery:masteryAfterRun(), diff:S.diff };", "weak:bad.map(r=>r.id), stars, steps:allSteps, q:qSummary(), siteq:siteSummary(), mastery:masteryAfterRun(), diff:S.diff };")
src = rep(src, "stars:{[id]:res.stars}, steps:compactSteps(res.steps), q:qSummary(), diff:S.diff }); }", "stars:{[id]:res.stars}, steps:compactSteps(res.steps), q:qSummary(), siteq:siteSummary(), diff:S.diff }); }")
# 실수 DNA에 사이트 퀴즈 오답 반영
src = rep(src, "function errorDna(stepsObj){ const cnt={near:0,mid:0,far:0,to:0,chance:0,site:0}; let total=0;", "function errorDna(stepsObj, siteLog){ const cnt={near:0,mid:0,far:0,to:0,chance:0,site:0}; let total=0; (siteLog||[]).forEach(x=>{ if(!x.ok){ cnt.site++; total++; } });")
src = rep(src, "function errorDnaRuns(runs){ const sum={near:0,mid:0,far:0,to:0,chance:0,site:0}; let total=0; (runs||[]).forEach(r=>{ const d=errorDna(r.steps);", "function errorDnaRuns(runs){ const sum={near:0,mid:0,far:0,to:0,chance:0,site:0}; let total=0; (runs||[]).forEach(r=>{ const d=errorDna(r.steps, (r.siteq&&r.siteq.wrong||[]).map(id=>({id, ok:false})));")
src = rep(src, "Object.assign(allSteps, compactSteps(r.steps)); }); renderDna(allSteps);", "Object.assign(allSteps, compactSteps(r.steps)); }); renderDna(allSteps, S.siteLog);")
src = rep(src, "function renderDna(stepsObj){ const box=$('review'); if(!box) return; const old=box.querySelector('.dna'); if(old) old.remove(); const d=errorDna(stepsObj);", "function renderDna(stepsObj, siteLog){ const box=$('review'); if(!box) return; const old=box.querySelector('.dna'); if(old) old.remove(); const d=errorDna(stepsObj, siteLog);")
src = rep(src, "div.innerHTML=`<h3>🧬 실수 DNA <small>오클릭 ${d.cnt.near+d.cnt.mid+d.cnt.far} · 시간초과 ${d.cnt.to} · 찬스 ${d.cnt.chance}</small></h3>`", "div.innerHTML=`<h3>🧬 실수 DNA <small>오클릭 ${d.cnt.near+d.cnt.mid+d.cnt.far} · 시간초과 ${d.cnt.to} · 찬스 ${d.cnt.chance}${siteLog&&siteLog.length?` · 사이트 퀴즈 ${siteLog.filter(x=>x.ok).length}/${siteLog.length}`:''}</small></h3>`")
# 성적표 텍스트
src = rep(src, "+(qSummary().total?`\\n응대 ${qSummary().ok}/${qSummary().total}`:'');", "+(qSummary().total?`\\n응대 ${qSummary().ok}/${qSummary().total}`:'')+(siteSummary().total?` · 사이트 이동 ${siteSummary().ok}/${siteSummary().total}`:'');")

# ── 2) 코칭 리포트 버튼 (개인 패널)
src = rep(src, '<button type="button" class="g-btn sm purple" id="fieldBtn">📋 동행 체크리스트</button>', '<button type="button" class="g-btn sm purple" id="fieldBtn">📋 동행 체크리스트</button><button type="button" class="g-btn sm" id="reportBtn" title="숙련도·실수 DNA·평가·기록을 A4 인쇄용으로">🖨 코칭 리포트</button>')
src = rep(src, "const fbtn=$('fieldBtn'); if(fbtn) fbtn.addEventListener('click', ()=>openField(p));", "const fbtn=$('fieldBtn'); if(fbtn) fbtn.addEventListener('click', ()=>openField(p)); const rbtn=$('reportBtn'); if(rbtn) rbtn.addEventListener('click', ()=>saveCoachReport(p, rbtn));")

# ── 3) 게임방법
src = rep(src, '<div class="rule"><div class="ic">📜</div><b>시연 대본</b>', '<div class="rule"><div class="ic">🔀</div><b>사이트 이동 퀴즈</b>사이트가 바뀌는 지점에서 보드가 뜨기 전에 "다음 동작은 어디서?"를 먼저 묻습니다(실전·단독 모드, 쉬움 난이도 제외, 스테이지당 최대 2회). 오답은 인내심 −5, 실수 DNA의 🔀 사이트 이동에 기록</div>\n      <div class="rule"><div class="ic">📜</div><b>시연 대본</b>')

# ── 4) 테스트 훅
src = rep(src, "focusPick, digestText, bgmCycle };", "focusPick, digestText, bgmCycle, siteSummary, coachReportHtml };")

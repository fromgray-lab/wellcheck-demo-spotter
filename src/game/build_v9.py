# v9: 원장님 질문 카드(응대) · 숙련도/자격 · 정답 지도 · 온보딩 · 폴리시  (build.py가 exec)
import json as _json, os as _os

# ── 1) 질문 카드 데이터 + 엔진
_qp = P('parts', 'qcards.json')
_qcards = _json.load(open(_qp, encoding='utf-8')) if _os.path.exists(_qp) else []
_qjs = parts('qcards.js').replace('/*QCARDS_JSON*/[]', _json.dumps(_qcards, ensure_ascii=False))
src = rep(src, "\n/* 초기화 */", _qjs + parts('mastery.js') + parts('boardmap.js') + parts('script.js') + parts('field.js') + parts('polish.js') + "\n/* 초기화 */")

# correct() 뒤 → 질문 카드가 있으면 먼저 묻고 다음 스텝
src = rep(src, "const go=()=>{ S.idx++; renderStep(); };\n  if(S.guide){ const d=guideSay(st);", "const go0=()=>{ S.idx++; renderStep(); }; const go=()=>{ const q=qcardFor(st); if(q) askQCard(q, go0); else go0(); };\n  if(S.guide){ const d=guideSay(st);")
# 런 시작 시 로그 초기화
src = rep(src, "S.qi = 0; S.stepLog=[]; S.cur=null;", "S.qi = 0; S.stepLog=[]; S.qLog=[]; S.cur=null;")
# 성적표: 응대 복습 + 기록에 q 요약
src = rep(src, "bindDisputes($('review'));", "bindDisputes($('review')); renderQReview();")
src = rep(src, "weak:bad.map(r=>r.id), stars, steps:allSteps };", "weak:bad.map(r=>r.id), stars, steps:allSteps, q:qSummary(), mastery:masteryAfterRun() };")
src = rep(src, "stars:{[id]:res.stars}, steps:compactSteps(res.steps) }); }", "stars:{[id]:res.stars}, steps:compactSteps(res.steps), q:qSummary() }); }")
src = rep(src, ":'\\n복습 포인트 없음');\n}", ":'\\n복습 포인트 없음')+(qSummary().total?`\\n응대 ${qSummary().ok}/${qSummary().total}`:'');\n}")

# ── 2) 스타일
src = rep(src, "</style>", parts('v9.css') + "</style>")

# ── 3) 숙련도/자격: 맵 렌더 뒤
src = rep(src, "  renderTodo();\n}\n$('playAll')", "  renderTodo(); renderMastery();\n}\n$('playAll')")
# ── 4) 온보딩 코치마크: 실전 첫 스텝
src = rep(src, "  if(S.guide){ guideStep(st); return; }\n  startStepTimer();\n}", "  if(S.guide){ guideStep(st); return; }\n  startStepTimer(); maybeOnboard(st);\n}")
# ── 5) 저장 상태 토스트
src = rep(src, "saveRun(run); renderRecords($('recordsBox'));", "saveRun(run).then(w=>saveStatus(w)); renderRecords($('recordsBox'));")
# ── 6) 현황표: 정답 지도 버튼
src = rep(src, '<button type="button" class="g-btn sm orange" id="boardLoop">♻ 개선 루프</button>', '<button type="button" class="g-btn sm orange" id="boardLoop">♻ 개선 루프</button>\n        <button type="button" class="g-btn sm purple" id="boardMap">🗺 정답 지도</button>')
src = rep(src, "\n/* 초기화 */", "\n$('boardMap').addEventListener('click', openBoardMap);\n/* 초기화 */")
# ── 7) 디버그 훅에 질문 카드 노출(린트용)
src = rep(src, "setCourse, loadFeedback, loadEvals };", "setCourse, loadFeedback, loadEvals, get QCARDS(){ return QCARDS; }, get MASTERY(){ return MASTERY; } };")

# ── 8) 현황표: 자격·숙련도·응대
src = rep(src, "  list.forEach(p=>{\n    p.level=levelOf(p.best);", "  list.forEach(p=>{\n    p.level=levelOf(p.best); p.pm=personMastery(p.runs);")
src = rep(src, '<span class="lv">${p.composite}</span><span class="gr ${p.best?p.best.grade:\'\'}">', '<span class="lv" title="자격 ${esc(p.pm.R.n)} · 실무 숙련도 ${p.pm.mBiz}% · 체험존 ${p.pm.mZone}% · 응대 ${esc(p.pm.qText)}">${p.composite} <span class="rk-mini" data-rank="${p.pm.R.id}">${p.pm.R.ic}</span></span><span class="gr ${p.best?p.best.grade:\'\'}">')
src = rep(src, "<div class=\"pt\" style=\"margin-top:12px\">📈 과정관리</div>", "<div class=\"pt\" style=\"margin-top:12px\">🎖 자격 · 숙련도</div><div class=\"pm\">${p.pm.R.ic} <b>${esc(p.pm.R.n)}</b> · 실무 숙련도 ${p.pm.mBiz}% · 체험존 ${p.pm.mZone}% · 원장님 질문 응대 ${esc(p.pm.qText)}${p.pm.R.next?' · 다음 단계: '+esc(p.pm.R.next):''}</div><div class=\"pstages\">${STAGES.filter(s=>!s.locked).map(s=>`<div class=\"pstage\"><small>${stageCode(s)} ${esc(s.title)}</small><div class=\"bbar\"><i style=\"width:${p.pm.M.stage[s.id]||0}%\"></i></div><div class=\"meta\">숙련도 ${p.pm.M.stage[s.id]||0}%</div></div>`).join('')}</div>\n  <div class=\"pt\" style=\"margin-top:12px\">📈 과정관리</div>")
src = rep(src, "'제안세션','평가자평균','최근','코칭플래그','코칭메모'].join('\\t')]", "'제안세션','평가자평균','자격','실무숙련도','체험존숙련도','응대정답','최근','코칭플래그','코칭메모'].join('\\t')]")
src = rep(src, "return e.length?Math.round(e.reduce((a,x)=>a+(x.avg||0),0)/e.length*10)/10:''; })(),p.lastAt?p.lastAt.slice(0,10):''", "return e.length?Math.round(e.reduce((a,x)=>a+(x.avg||0),0)/e.length*10)/10:''; })(),p.pm.R.n,p.pm.mBiz,p.pm.mZone,p.pm.qText,p.lastAt?p.lastAt.slice(0,10):''")

# ── 9) 시연 대본 · 음성 · 주간 랭킹
src = rep(src, '<button type="button" class="g-btn bgmBtn">🔇 BGM</button>', '<button type="button" class="g-btn bgmBtn">🔇 BGM</button>\n        <button type="button" class="g-btn ttsBtn">🔇 음성</button>\n        <button type="button" class="g-btn" id="scriptBtn">📜 시연 대본</button>')
src = rep(src, '<div class="todo" id="todo"></div>', '<div class="todo" id="todo"></div>\n      <div class="todo weekly" id="weekly" hidden></div>')
src = rep(src, "  renderTodo(); renderMastery();\n}", "  renderTodo(); renderMastery(); renderWeekly();\n}")
src = rep(src, "$('dWho').textContent = st.who ? st.who+' '+(st.say||'') : ''; $('dTask').innerHTML = st.task;", "$('dWho').textContent = st.who ? st.who+' '+(st.say||'') : ''; $('dTask').innerHTML = st.task; if(st.who&&st.say&&!S.demo) speak(st.say);")
src = rep(src, "  const say = st.tip && st.tip.say ? st.tip.say : '';\n  const host=$('arenaUi'); const card=document.createElement('div'); card.className='demo-say';", "  const say = st.tip && st.tip.say ? st.tip.say : ''; speak(say,{rate:1.0});\n  const host=$('arenaUi'); const card=document.createElement('div'); card.className='demo-say';")
src = rep(src, "host.innerHTML=`<div class=\"overlay qover\"", "speak(q.q,{pitch:0.9}); host.innerHTML=`<div class=\"overlay qover\"")

# ── 10) 성적표 이미지에 응대 포함
src = rep(src, "time:fmtTime(secs), rows:S.queue.map(id=>{", "time:fmtTime(secs), q:qSummary(), rows:S.queue.map(id=>{")

# ── 11) 게임방법에 질문 카드 · 숙련도/자격 · 대본 추가
src = rep(src, '<div class="rule"><div class="ic">🖥</div><b>사이트 구분</b>보드 위 브라우저 바가 지금 어느 사이트(웰체크·심평원·앱·Agent…)인지 보여주고, 바뀌면 "사이트 이동" 안내</div>\n    </div>', '<div class="rule"><div class="ic">🖥</div><b>사이트 구분</b>보드 위 브라우저 바가 지금 어느 사이트(웰체크·심평원·앱·Agent…)인지 보여주고, 바뀌면 "사이트 이동" 안내. 📸 실제 화면 / 📄 매뉴얼 화면 배지로 출처 표시</div>\n      <div class="rule"><div class="ic">🩺</div><b>원장님 질문 카드</b>스테이지 중간에 원장님이 물어봅니다 — 3지선다. 좋은 답 = 인내심 +5, 오답 = 인내심 −10 · 오답 1회(매뉴얼 근거 해설 표시)</div>\n      <div class="rule"><div class="ic">🎖</div><b>숙련도 · MR 자격</b>스텝마다 최근 시도 품질로 숙련도(%)가 쌓이고, 🌱 견습 → 🎖 정식 → 👑 마스터 자격이 올라갑니다 (미션 화면 칩에서 기준 확인)</div>\n      <div class="rule"><div class="ic">📜</div><b>시연 대본</b>미션 화면의 📜 시연 대본에서 경로·할 일·멘트·응대를 한 번에 보고 복사/저장</div>\n    </div>')

# ── 12) 스테이지 시작 시 질문 카드 추첨
src = rep(src, "S.stageRes[id] = { wrong:0, chance:0, tips:0, start:Date.now() }; preloadStage(id);", "S.stageRes[id] = { wrong:0, chance:0, tips:0, start:Date.now() }; S.qPick = (typeof pickQCards==='function') ? pickQCards(id) : null; preloadStage(id);")

# ── 13) 현장 동행 체크리스트 (평가자)
src = rep(src, '<button type="button" class="g-btn sm blue" id="evSave">평가 저장</button>', '<button type="button" class="g-btn sm blue" id="evSave">평가 저장</button><button type="button" class="g-btn sm purple" id="fieldBtn">📋 동행 체크리스트</button>')
src = rep(src, "  const es=$('evSave');", "  const fbtn=$('fieldBtn'); if(fbtn) fbtn.addEventListener('click', ()=>openField(p));\n  const es=$('evSave');")
src = rep(src, "p.pm=personMastery(p.runs);", "p.pm=personMastery(p.runs.concat(evalsAsAttempts(evalsFor(p))));")

# ── 14) 보드 이미지 alt = 임무 (접근성) · 게임방법에 보너스 스테이지
src = rep(src, "$('dTask').innerHTML = st.task; if(st.who&&st.say&&!S.demo) speak(st.say);", "$('dTask').innerHTML = st.task; try{ $('shot').alt='시연 화면 — '+st.task.replace(/<[^>]+>/g,''); }catch(e){} if(st.who&&st.say&&!S.demo) speak(st.say);")
src = rep(src, '<div class="rule"><div class="ic">📜</div><b>시연 대본</b>', '<div class="rule"><div class="ic">🧪</div><b>M8 틀린 설정 찾기</b>실무 코스 마지막 보너스. 매뉴얼 화면에 일부러 넣은 흔한 실수(Port 오타·체크 해제·미설치·검사일 초과…)를 찾아 탭 — "🧪 변조 화면" 배지가 붙습니다</div>\n      <div class="rule"><div class="ic">📜</div><b>시연 대본</b>')

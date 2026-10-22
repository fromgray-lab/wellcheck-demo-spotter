# v31(v43): 목적 집중 — 수가계산기·숫자특훈·카드북·응대특훈·오답노트 칩 제외 + 🧭 자유자재 지수  (build.py가 exec, build_v29 뒤)
src = rep(src, "</style>", parts('v31.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v31.js') + "\n/* 초기화 */")
src = rep(src, "renderWeeklyChip(); renderQDrillChip(); renderWrongQChip(); renderNumChip(); renderPathChip(); layoutTodo(); renderTools();", "renderWeeklyChip(); renderPathChip(); layoutTodo();")
src = rep(src, "function renderInstallChip(){ if(!ON_WEB||IS_STANDALONE) return; const row=document.querySelector('#todo .trow.tools');", "function renderInstallChip(){ if(!ON_WEB||IS_STANDALONE) return; const row=ensureToolsRow();")
src = rep(src, '<button type="button" class="g-btn sm" id="scBook" title="질문 카드 전부(오답 보기까지) + 핵심 숫자 — A4 인쇄용">📖 카드북</button>', '')
src = rep(src, " $('scBook').addEventListener('click', ()=>saveCardbook($('scBook')));", "")
# 입문 코스: 응대 특훈 → 순서 맞추기(실무 흐름)
src = rep(src, "{ id:'qdrill', ic:'🩺', n:'응대 특훈 70% 이상',              test:(s)=>s.runs.some(r=>r.mode==='qdrill'&&r.score>=70), next:()=>null, go:()=>startQDrill() }",
               "{ id:'order', ic:'🔀', n:'순서 맞추기 M0~M3',               test:(s)=>['m0','m1','m2','m3'].every(id=>s.runs.some(r=>r.mode==='order'&&r.stage===id&&!r.over)), next:(s)=>['m0','m1','m2','m3'].find(id=>!s.runs.some(r=>r.mode==='order'&&r.stage===id&&!r.over)), go:(id)=>{ if(S.course!=='biz') setCourse('biz'); openOrder(id||'m0'); } }")
src = rep(src, "r.some(x=>x.mode==='qdrill'&&x.score>=70)", "['m0','m1','m2','m3'].every(st=>r.some(x=>x.mode==='order'&&x.stage===st&&!x.over))")
src = rep(src, '<div class="rule"><div class="ic">🏁</div><b>주간 챌린지 · 🩺 응대 특훈</b>매주 전 팀원에게 같은 12스텝(😈 압박 고정)이 나오고 주간 보드에 최고점이 올라갑니다. 응대 특훈은 보드 없이 질문 카드 10장 연속 — 정답률이 MR 자격(응대 80%)에 반영</div>',
               '<div class="rule"><div class="ic">🏁</div><b>주간 챌린지</b>매주 전 팀원에게 같은 12스텝(😈 압박 고정)이 나오고 주간 보드에 최고점이 올라갑니다</div><div class="rule"><div class="ic">🧭</div><b>자유자재 지수</b>오답·찬스·시간초과 없이 8초 안에 정답을 누른 스텝의 비율. 성적표 맨 위에 지수와 머뭇거린 곳 TOP3가 나옵니다 — 이 게임의 최종 목표는 지수 90% 이상</div>')
src = rep(src, '입문 7단계 코스</b>신규 MR 첫 주 추천 순서(시범 → 따라하기 → 실전 단독 → 응대 특훈 → 전체 완주', '입문 7단계 코스</b>신규 MR 첫 주 추천 순서(시범 → 따라하기 → 실전 단독 → 순서 맞추기 → 전체 완주')
_i = src.find('<div class="rule"><div class="ic">🧮</div>'); _j = src.find('</div>', src.find('</b>', _i)) + len('</div>')
assert _i > 0
src = src[:_i] + src[_j:]
# 성적표·스테이지 클리어에 자유자재 지수
src = rep(src, "setTimeout(()=>{ try{ paceResult(secs); }catch(e){} },0);", "setTimeout(()=>{ try{ paceResult(secs); fluAll(); }catch(e){} },0);")
src = rep(src, "<small>시간</small><b>${fmtTime(res.secs)}</b></div></div>${recapHtml()}${S.demo?'':fbCardHtml()}", "<small>시간</small><b>${fmtTime(res.secs)}</b></div></div>${S.demo||S.guide?'':fluHtml(S.stepLog.filter(l=>l.st===S.stage.id))}${recapHtml()}${S.demo?'':fbCardHtml()}")

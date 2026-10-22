# v26(v33): 🧮 수가 계산기 · 🔢 숫자 특훈 · ⏱ 10분 페이스 · 📖 응대 카드북  (build.py가 exec, build_v25 뒤)
src = rep(src, "</style>", parts('v26.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v26.js') + "\n/* 초기화 */")
# HUD 타이머 틱에 페이스
src = rep(src, "function tickTimer(){ $('timer').textContent = fmtTime(Math.floor((Date.now()-S.start)/1000)); }",
               "function tickTimer(){ $('timer').textContent = fmtTime(Math.floor((Date.now()-S.start)/1000)); try{ paceTick(); }catch(e){} }")
# 성적표에 10분 페이스 줄
src = rep(src, "$('sTime').textContent=fmtTime(secs);", "$('sTime').textContent=fmtTime(secs); setTimeout(()=>{ try{ paceResult(secs); }catch(e){} },0);")
# 미션 화면: 숫자 특훈 칩 + 도구 줄
src = rep(src, "renderWrongQChip(); renderPathChip(); layoutTodo();", "renderWrongQChip(); renderNumChip(); renderPathChip(); layoutTodo(); renderTools();")
src = rep(src, "const modes=[...el.querySelectorAll('.tchip.daily,.tchip.weekly,.tchip.focus,.tchip.qdrill,.tchip.wrongq')];",
               "const modes=[...el.querySelectorAll('.tchip.daily,.tchip.weekly,.tchip.focus,.tchip.qdrill,.tchip.wrongq,.tchip.numdrill')];")
# 시연 대본 모달에 📖 카드북
src = rep(src, '<button type="button" class="g-btn sm" id="scPrint" title="A4 인쇄용 HTML — 열어서 인쇄/PDF 저장">🖨 인쇄용</button>',
               '<button type="button" class="g-btn sm" id="scPrint" title="A4 인쇄용 HTML — 열어서 인쇄/PDF 저장">🖨 인쇄용</button><button type="button" class="g-btn sm" id="scBook" title="질문 카드 전부(오답 보기까지) + 핵심 숫자 — A4 인쇄용">📖 카드북</button>')
src = rep(src, "$('scPrint').addEventListener('click', ()=>saveScriptHtml($('scPrint')));",
               "$('scPrint').addEventListener('click', ()=>saveScriptHtml($('scPrint'))); $('scBook').addEventListener('click', ()=>saveCardbook($('scBook')));")
# 모드 라벨·기록실 탭·다이제스트·코칭 리포트
src = rep(src, "['qdrill','응대 특훈'],['order','순서']]", "['qdrill','응대 특훈'],['numdrill','숫자 특훈'],['order','순서']]")
src = rep(src, "const M={all:'전체',one:'',daily:'10문제',weekly:'주간',focus:'약점',qdrill:'특훈',order:'순서',review:'복습',demo:'시범',guide:'따라하기'};",
               "const M={all:'전체',one:'',daily:'10문제',weekly:'주간',focus:'약점',qdrill:'특훈',numdrill:'숫자',order:'순서',review:'복습',demo:'시범',guide:'따라하기'};")
src = rep(src, "qdrill:'응대 특훈',review:'복습'}; const diffN", "qdrill:'응대 특훈',numdrill:'숫자 특훈',review:'복습'}; const diffN")
src = rep(src, "· 응대 특훈 ${modeN(wk,'qdrill')} · 복습 ${modeN(wk,'review')}", "· 응대 특훈 ${modeN(wk,'qdrill')} · 숫자 특훈 ${modeN(wk,'numdrill')} · 복습 ${modeN(wk,'review')}")
# 게임 방법
src = rep(src, '<div class="rule"><div class="ic">📜</div><b>시연 대본</b>',
               '<div class="rule"><div class="ic">🧮</div><b>수가 계산기 · 🔢 숫자 특훈 · ⏱ 10분 페이스</b>미션 화면 🧰 도구의 계산기는 원장님 숫자(환자 수·횟수·위험군)로 연 수가를 바로 계산해 복사합니다(26년 수가표, 재진진찰료 별도). 숫자 특훈은 원장님이 현장에서 검산할 수 있는 수가·횟수·기한·포인트만 10문제. 체험존 전체 시연은 HUD에 🐇/🐢 예상 시간이 떠서 "10분 안에" 약속을 지켰는지 성적표에 남습니다</div><div class="rule"><div class="ic">📜</div><b>시연 대본</b>')

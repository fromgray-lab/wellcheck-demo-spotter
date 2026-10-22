# v16: 복습 카드 오클릭 표시 · 시연 대본 전체 듣기  (build.py가 exec, build_v15 뒤)
src = rep(src, "</style>", parts('v16.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v16.js') + "\n/* 초기화 */")
# 복습 카드: 크롭 안에 정답 박스 + 오클릭 점
src = rep(src, 'return `<div class="rcard"><div class="crop" style="--bs:${bs};--bp:${bp};background-image:url(${IMG[st.img]})"></div><div class="cap">', 'return `<div class="rcard"><div class="crop" style="--bs:${bs};--bp:${bp};background-image:url(${IMG[st.img]})">${reviewMarks(st)}</div><div class="legend"><span><b></b>정답 영역</span><span><i></i>내가 누른 곳</span></div><div class="cap">')
# 대본 모달: 전체 듣기 버튼
src = rep(src, '<button type="button" class="g-btn sm" id="scPrint" title="A4 인쇄용 HTML — 열어서 인쇄/PDF 저장">🖨 인쇄용</button>', '<button type="button" class="g-btn sm" id="scPrint" title="A4 인쇄용 HTML — 열어서 인쇄/PDF 저장">🖨 인쇄용</button><button type="button" class="g-btn sm orange" id="scListen" title="이 스테이지 경로·멘트를 음성으로 순서대로">🔊 전체 듣기</button>')
src = rep(src, "$('scClose').addEventListener('click', ()=>{ host.innerHTML=''; }); $('scPrint')", "$('scClose').addEventListener('click', ()=>{ listenStop(); host.innerHTML=''; }); $('scListen').addEventListener('click', ()=>listenStage(cur)); $('scPrint')")
src = rep(src, "$('scTabs').querySelectorAll('[data-st]').forEach(b=>b.addEventListener('click', ()=>{ cur=b.dataset.st; render(); SFX.pop(); })); };", "$('scTabs').querySelectorAll('[data-st]').forEach(b=>b.addEventListener('click', ()=>{ listenStop(); cur=b.dataset.st; render(); SFX.pop(); })); };")
src = rep(src, "$('scModal').addEventListener('click', e=>{ if(e.target.id==='scModal') host.innerHTML=''; });", "$('scModal').addEventListener('click', e=>{ if(e.target.id==='scModal'){ listenStop(); host.innerHTML=''; } });")
src = rep(src, "openNoticeEditor, renderNotice, pathFromRuns, loadNotice };", "openNoticeEditor, renderNotice, pathFromRuns, loadNotice, reviewMarks, listenStage };")
# 복습 카드 크롭을 정답 중심으로
src = rep(src, "function reviewCard(r){ const st=STEPS.find(s=>s.id===r.id); if(!st) return ''; const rc=st.rects[0]; const cx=rc.l+rc.w/2, cy=rc.t+rc.h/2; const zoom=2.5; const bs=`${zoom*100}% auto`; const px=Math.max(0,Math.min(100,cx)), py=Math.max(0,Math.min(100,cy)); const bp=`${px}% ${py}%`;", "function reviewCard(r){ const st=STEPS.find(s=>s.id===r.id); if(!st) return ''; const zoom=2.5; const bs=`${zoom*100}% auto`; const cp=cropPos(st); const bp=`${cp.px.toFixed(2)}% ${cp.py.toFixed(2)}%`;")

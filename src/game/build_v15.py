# v15: 팀 공지 배너 · 입문 코스 팀 추적  (build.py가 exec, build_v14 뒤)
src = rep(src, "</style>", parts('v15.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v15.js') + "\n$('boardNotice').addEventListener('click', ()=>{ if(!masterOk()){ askMaster(openNoticeEditor); return; } openNoticeEditor(); });\n/* 초기화 */")
# 시범/따라하기 첫 완료 → 가벼운 팀 기록
src = rep(src, "function pathMark(kind, stageId){ try{ const p=pathState(); const l=p[kind]=p[kind]||[]; if(!l.includes(stageId)) l.push(stageId); localStorage.setItem('dsg_path', JSON.stringify(p)); }catch(e){} }", "function pathMark(kind, stageId){ try{ const p=pathState(); const l=p[kind]=p[kind]||[]; if(!l.includes(stageId)){ l.push(stageId); localStorage.setItem('dsg_path', JSON.stringify(p)); pathLight(kind, stageId); } }catch(e){} }")
# 미션 화면 공지 배너
src = rep(src, "renderTodo(); renderDailyChip(); renderFocusChip(); renderWeeklyChip(); renderQDrillChip(); renderPathChip(); renderMastery(); renderWeekly();", "renderTodo(); renderDailyChip(); renderFocusChip(); renderWeeklyChip(); renderQDrillChip(); renderPathChip(); renderMastery(); renderWeekly(); renderNotice();")
# 현황표: 공지 버튼 · 개인 패널 입문 진행
src = rep(src, '<button type="button" class="g-btn sm blue" id="boardDigest" title="이번 주 팀 훈련 요약 — 카톡/슬랙에 붙여넣기">📰 주간 다이제스트</button>', '<button type="button" class="g-btn sm blue" id="boardDigest" title="이번 주 팀 훈련 요약 — 카톡/슬랙에 붙여넣기">📰 주간 다이제스트</button>\n        <button type="button" class="g-btn sm yellow" id="boardNotice" title="모든 팀원 미션 화면 상단에 뜨는 공지">📣 공지</button>')
src = rep(src, '<div class="pt">🎯 시연 (틀린시연찾기) · ${p.level}</div>', '<div class="pt">🎯 시연 (틀린시연찾기) · ${p.level} <span class="lvbadge" title="입문 7단계: 시범·따라하기·단독 별2·응대 특훈·완주 B·10문제 3일·체험존 완주">${pathBadge(p)}</span></div>')
# 다이제스트: 입문 진행
src = rep(src, "const idle=(BOARD.people||[])", "const newbies=(BOARD.people||[]).map(p=>({ p, pr:pathFromRuns(p.runs) })).filter(x=>x.pr.done<x.pr.total).slice(0,8); if(newbies.length) L.push('', `🧭 입문 코스 진행 — ${newbies.map(x=>`${x.p.name} ${x.pr.done}/${x.pr.total}`).join(' · ')}`);\n  const idle=(BOARD.people||[])")
# 게임방법
src = rep(src, '<div class="rule"><div class="ic">📜</div><b>시연 대본</b>', '<div class="rule"><div class="ic">📣</div><b>팀 공지</b>관리자가 현황표에서 쓴 공지가 미션 화면 맨 위에 뜹니다(공유 저장소가 있으면 팀 전체)</div>\n      <div class="rule"><div class="ic">📜</div><b>시연 대본</b>')
src = rep(src, "pathProgress, pathMark, saveCardImage };", "pathProgress, pathMark, saveCardImage, openNoticeEditor, renderNotice, pathFromRuns, loadNotice };")
# 현황표 나갈 때 열린 개인 패널 닫기
src = rep(src, "$('boardBack').addEventListener('click', ()=>{ show(S.profile ? 'map' : 'title'); });", "$('boardBack').addEventListener('click', ()=>{ try{ closeModal('personModal'); }catch(e){} show(S.profile ? 'map' : 'title'); });")

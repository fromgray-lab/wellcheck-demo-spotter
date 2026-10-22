# v13: 주간 챌린지 · 응대 특훈  (build.py가 exec, build_v12 뒤)
src = rep(src, "</style>", parts('v13.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v13.js') + "\n/* 초기화 */")
# 스테이지 훅
src = rep(src, ": id==='focus' ? { id:'focus', course:S.course, n:'F', title:'약점 집중 훈련', sub:'숙련도 낮은 '+(S.focusIds||[]).length+'스텝 · '+diffOf().n, color:'#e0365b' } : STAGES.find(s=>s.id===id);",
          ": id==='focus' ? { id:'focus', course:S.course, n:'F', title:'약점 집중 훈련', sub:'숙련도 낮은 '+(S.focusIds||[]).length+'스텝 · '+diffOf().n, color:'#e0365b' } : id==='weekly' ? { id:'weekly', course:S.course, n:'W', title:'주간 챌린지', sub:weekKey()+' · 전 팀원 같은 12스텝 · 😈 압박', color:'#b45309' } : STAGES.find(s=>s.id===id);")
src = rep(src, ": id==='focus' ? (S.focusIds||[]).map(x=>STEPS.find(s=>s.id===x)).filter(Boolean) : STEPS.filter(", ": id==='focus' ? (S.focusIds||[]).map(x=>STEPS.find(s=>s.id===x)).filter(Boolean) : id==='weekly' ? (S.weeklyIds||[]).map(x=>STEPS.find(s=>s.id===x)).filter(Boolean) : STEPS.filter(")
src = rep(src, "if(st.n==='F') return '집중';", "if(st.n==='F') return '집중'; if(st.n==='W') return '주간';")
src = rep(src, "  if(S.mode==='focus'){ focusEnd(); return; }\n", "  if(S.mode==='focus'){ focusEnd(); return; }\n  if(S.mode==='weekly'){ weeklyEnd(); return; }\n")
src = rep(src, "function pickQCards(stageId){ const pool = (stageId==='daily'||stageId==='focus') ? QCARDS.filter(q=>q.course===S.course && ((stageId==='daily'?S.dailyIds:S.focusIds)||[]).includes(q.after)) :", "function pickQCards(stageId){ const pool = (stageId==='daily'||stageId==='focus'||stageId==='weekly') ? QCARDS.filter(q=>q.course===S.course && ((stageId==='daily'?S.dailyIds:stageId==='focus'?S.focusIds:S.weeklyIds)||[]).includes(q.after)) :")
src = rep(src, "renderTodo(); renderDailyChip(); renderFocusChip(); renderMastery(); renderWeekly();", "renderTodo(); renderDailyChip(); renderFocusChip(); renderWeeklyChip(); renderQDrillChip(); renderMastery(); renderWeekly();")
# 게임방법
src = rep(src, '<div class="rule"><div class="ic">📜</div><b>시연 대본</b>', '<div class="rule"><div class="ic">🏁</div><b>주간 챌린지 · 🩺 응대 특훈</b>매주 전 팀원에게 같은 12스텝(😈 압박 고정)이 나오고 주간 보드에 최고점이 올라갑니다. 응대 특훈은 보드 없이 질문 카드 10장 연속 — 정답률이 MR 자격(응대 80%)에 반영</div>\n      <div class="rule"><div class="ic">📜</div><b>시연 대본</b>')
# 주간 다이제스트 모드 카운트
src = rep(src, "· 약점 집중 ${modeN(wk,'focus')} · 복습 ${modeN(wk,'review')}`);", "· 약점 집중 ${modeN(wk,'focus')} · 주간 챌린지 ${modeN(wk,'weekly')} · 응대 특훈 ${modeN(wk,'qdrill')} · 복습 ${modeN(wk,'review')}`);")
# 코칭 리포트 모드명
src = rep(src, "const modeN={all:'전체 완주',one:'단독',daily:'오늘의 10문제',order:'순서',focus:'약점 집중',review:'복습'};", "const modeN={all:'전체 완주',one:'단독',daily:'오늘의 10문제',order:'순서',focus:'약점 집중',weekly:'주간 챌린지',qdrill:'응대 특훈',review:'복습'};")
# 테스트 훅
src = rep(src, "siteSummary, coachReportHtml };", "siteSummary, coachReportHtml, startQDrill, startWeekly, weekKey };")

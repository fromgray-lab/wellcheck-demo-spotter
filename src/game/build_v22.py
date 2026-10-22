# v22: 복습 카드 → 이 스텝만 연습 · 응대 오답 노트  (build.py가 exec, build_v21 뒤)
src = rep(src, "</style>", parts('v22.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v22.js') + "\n/* 초기화 */")
# 복습 카드 버튼
src = rep(src, '<div class="dsp"><button type="button" data-dsp="${st.id}" title="판정이 이상하면 알려주세요">⚑ 판정 이의</button></div></div>`; }', '<div class="dsp"><button type="button" data-practice="${st.id}" title="이 스텝만 바로 다시 연습">🎯 이 스텝만 연습</button><button type="button" data-dsp="${st.id}" title="판정이 이상하면 알려주세요">⚑ 판정 이의</button></div></div>`; }')
src = rep(src, "bindDisputes($('review')); renderQReview();", "bindDisputes($('review')); bindPractice($('review')); renderQReview();")
# 응대 특훈: 카드 id 목록 지정 가능
src = rep(src, "function startQDrill(){ const pool=QCARDS.filter(q=>q.course===S.course); if(pool.length<3){ toast('이 코스엔 질문 카드가 부족해요'); return; }", "function startQDrill(onlyIds){ const pool=QCARDS.filter(q=>q.course===S.course&&(!onlyIds||onlyIds.includes(q.id))); if(pool.length<1){ toast('풀 카드가 없어요'); return; }")
src = rep(src, "const pref=S.persona&&(S.persona.key==='yes'||S.persona.key==='busy')?'adv':'basic'; const picked=pool.map(q=>({ q, k:(q.lv===pref?0.6:0)+Math.random() })).sort((a,b)=>b.k-a.k).slice(0,10).map(x=>x.q);", "const pref=S.persona&&(S.persona.key==='yes'||S.persona.key==='busy')?'adv':'basic'; const picked=pool.map(q=>({ q, k:(q.lv===pref?0.6:0)+Math.random() })).sort((a,b)=>b.k-a.k).slice(0,onlyIds?pool.length:10).map(x=>x.q);")
src = rep(src, "$('qdAgain').addEventListener('click', ()=>{ host.innerHTML=''; startQDrill(); });", "$('qdAgain').addEventListener('click', ()=>{ host.innerHTML=''; startQDrill(onlyIds); });")
src = rep(src, "renderTodo(); renderDailyChip(); renderFocusChip(); renderWeeklyChip(); renderQDrillChip(); renderPathChip(); layoutTodo();", "renderTodo(); renderDailyChip(); renderFocusChip(); renderWeeklyChip(); renderQDrillChip(); renderWrongQChip(); renderPathChip(); layoutTodo();")
src = rep(src, "const modes=[...el.querySelectorAll('.tchip.daily,.tchip.weekly,.tchip.focus,.tchip.qdrill')];", "const modes=[...el.querySelectorAll('.tchip.daily,.tchip.weekly,.tchip.focus,.tchip.qdrill,.tchip.wrongq')];")
src = rep(src, "renderRecords, myPerson, growthSvg, saveMyReport, layoutTodo };", "renderRecords, myPerson, growthSvg, saveMyReport, layoutTodo, wrongQIds, startReviewIds };")

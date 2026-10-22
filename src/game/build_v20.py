# v20: 미션 화면 훈련 칩 정리 · 정답 지도 기간 필터  (build.py가 exec, build_v19 뒤)
src = rep(src, "</style>", parts('v20.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v20.js') + "\n/* 초기화 */")
src = rep(src, "renderTodo(); renderDailyChip(); renderFocusChip(); renderWeeklyChip(); renderQDrillChip(); renderPathChip(); renderMastery(); renderWeekly(); renderNotice();", "renderTodo(); renderDailyChip(); renderFocusChip(); renderWeeklyChip(); renderQDrillChip(); renderPathChip(); layoutTodo(); renderMastery(); renderWeekly(); renderNotice();")
# 정답 지도: 기간 select + 집계 필터
src = rep(src, '<select id="bmStage"></select><label class="kbd"><input type="checkbox" id="bmMiss" checked> 오클릭 점(🔴)</label>', '<select id="bmStage"></select><select id="bmDays"><option value="0">전체 기간</option><option value="7">최근 7일</option><option value="30">최근 30일</option><option value="90">최근 90일</option></select><label class="kbd"><input type="checkbox" id="bmMiss" checked> 오클릭 점(🔴)</label>')
src = rep(src, "$('bmMiss').addEventListener('change', bmRender); $('bmZone').addEventListener('change', bmRender);", "$('bmMiss').addEventListener('change', bmRender); $('bmZone').addEventListener('change', bmRender); $('bmDays').value=String(BM_DAYS); $('bmDays').addEventListener('change', e=>{ BM_DAYS=Number(e.target.value)||0; bmRender(); if($('bmSrc')) $('bmSrc').textContent=`${BM.src} · ${bmFilterRuns(BM.runs).length}런`; });")
src = rep(src, "function bmAggregate(){ const agg={}; BM.runs.forEach(r=>{", "function bmAggregate(){ const agg={}; bmFilterRuns(BM.runs).forEach(r=>{")
src = rep(src, "renderRecords, myPerson, growthSvg, saveMyReport };", "renderRecords, myPerson, growthSvg, saveMyReport, layoutTodo };")

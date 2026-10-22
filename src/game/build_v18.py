# v18: 기록 공유 코드 · 기록실 모드별 보기  (build.py가 exec, build_v17 뒤)
src = rep(src, "</style>", parts('v18.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v18.js') + "\n$('boardShareIn').addEventListener('click', ()=>{ if(!masterOk()){ askMaster(openShareIn); return; } openShareIn(); });\n/* 초기화 */")
# 기록실: 모드 필터 + 공유 코드 버튼
src = rep(src, "const got=await loadRuns(); rows=got.rows.filter(r=>r.mode==='all'); src=got.src;\n  if(!rows.length){ el.innerHTML=`<h2 class=\"g\" style=\"font-size:18px\">기록실</h2><div class=\"src\">아직 기록이 없습니다. 전체 시연을 마치면 여기에 남습니다.</div>`; return; }",
          "const got=await loadRuns(); rows=got.rows.filter(r=>r.mode===REC_MODE); src=got.src;\n  if(!rows.length){ el.innerHTML=`<h2 class=\"g\" style=\"font-size:18px\">기록실</h2>${recModeBar()}<div class=\"src\">아직 이 모드의 기록이 없습니다.</div>`; bindRecModes(el); return; }")
src = rep(src, "el.innerHTML=`<h2 class=\"g\" style=\"font-size:18px\">기록실 <span class=\"src\" style=\"font-family:var(--body);font-weight:400\">· ${src}</span></h2>`+(top.length?", "el.innerHTML=`<h2 class=\"g\" style=\"font-size:18px\">기록실 <span class=\"src\" style=\"font-family:var(--body);font-weight:400\">· ${src}</span></h2>`+recModeBar()+(top.length?")
src = rep(src, "<table>${head}<tbody>${rows.slice(0,12).map(fmt).join('')}</tbody></table>`;\n}", "<table>${head}<tbody>${rows.slice(0,12).map(fmt).join('')}</tbody></table>`; bindRecModes(el);\n}")
# 현황표: 코드 붙여넣기
src = rep(src, '<button type="button" class="g-btn sm yellow" id="boardNotice" title="모든 팀원 미션 화면 상단에 뜨는 공지">📣 공지</button>', '<button type="button" class="g-btn sm yellow" id="boardNotice" title="모든 팀원 미션 화면 상단에 뜨는 공지">📣 공지</button>\n        <button type="button" class="g-btn sm gray" id="boardShareIn" title="팀원이 카톡으로 보낸 DSG 공유 코드를 이 기기에 합치기">📥 코드 합치기</button>')
# 게임방법
src = rep(src, '<div class="rule"><div class="ic">📜</div><b>시연 대본</b>', '<div class="rule"><div class="ic">📤</div><b>기록 공유 코드</b>공유 저장소가 없어도 기록실 → 📤 공유 코드를 복사해 카톡으로 보내면, 팀장님이 현황표 📥 코드 합치기로 합칩니다(지난 공유 이후 기록만, 중복 제외)</div>\n      <div class="rule"><div class="ic">📜</div><b>시연 대본</b>')
src = rep(src, "reviewMarks, listenStage, cropPos, get LIMIT(){ return LIMIT; } };", "reviewMarks, listenStage, cropPos, get LIMIT(){ return LIMIT; }, makeShareCode, parseShareCode, mergeShared, renderRecords };")

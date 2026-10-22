# v29(v39): 새 주소로 이사  (build.py가 exec, build_v28 뒤)
src = rep(src, "</style>", parts('v29.css') + "</style>")
src = rep(src, "\n/* 초기화 */", parts('v29.js') + "\n/* 초기화 */")
src = rep(src, "renderSync(); flushOutbox();", "renderSync(); flushOutbox(); renderMoveBar(); renderInstallChip();")
# 현황표: 웹 버전이면 📊 구글 시트 바로가기
src = rep(src, '<button type="button" class="g-btn sm gray" id="boardShareIn" title="팀원이 카톡으로 보낸 DSG 공유 코드를 이 기기에 합치기">📥 코드 합치기</button>',
               '<button type="button" class="g-btn sm gray" id="boardShareIn" title="팀원이 카톡으로 보낸 DSG 공유 코드를 이 기기에 합치기">📥 코드 합치기</button><a class="g-btn sm gray" id="boardSheet" href="https://docs.google.com/spreadsheets/d/1NzUdVlCRoTM7YBiP0vBRa62yLp4IRhf1DHkdrAzh-dQ/edit" target="_blank" rel="noopener" title="모든 기록·의견이 쌓이는 구글 시트 (관리자 계정만 열림)" style="text-decoration:none">📊 구글 시트</a>')

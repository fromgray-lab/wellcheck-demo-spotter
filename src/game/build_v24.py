# v24: 현황표 팀 8주 추이  (build.py가 exec, build_v23 뒤)
src = rep(src, "\n/* 초기화 */", parts('v24.js') + "\n/* 초기화 */")
src = rep(src, "<div class=\"tile\"><small>최근 ${WEEKS}주 활동</small><b>${spark(g.weeks,'big')}</b></div>`;", "<div class=\"tile\"><small>최근 ${WEEKS}주 활동</small><b>${spark(g.weeks,'big')}</b></div><div class=\"tile trend\"><small>📈 팀 ${WEEKS}주 추이</small>${teamTrendSvg(ps)||'<b class=\"sub\">기록 없음</b>'}</div>`;")
src = rep(src, "</style>", ".tile.trend{grid-column:1/-1} .tile.trend svg{max-height:170px!important}</style>")

# v60: 문제(지시문)를 화면 상단으로 — 시선이 위→아래로 흐르므로 HUD 바로 아래에 강조 표시
src = rep(src, "</style>", """#play>.hud{order:1} #play>#prog{order:2} #play>#dialog{order:3} #play>#arena{order:4}
#play>#dialog{border-top:0;border-bottom:4px solid var(--ink);background:#ffd84d;box-shadow:0 5px 0 rgba(13,16,40,.25);z-index:6}
#dialog .line{border-width:3px}
#dialog .line .task{display:block;font-size:1.2em;font-weight:900;line-height:1.3;margin-top:2px}
#dialog .line .task::before{content:"문제";display:inline-block;background:var(--ink);color:#ffd84d;font-family:var(--body);font-weight:900;font-size:.6em;border-radius:6px;padding:2px 7px;margin-right:7px;vertical-align:.18em;letter-spacing:.06em}
#dialog .line.qpop{animation:qpop60 .45s cubic-bezier(.2,1.5,.4,1)} @keyframes qpop60{0%{transform:scale(.96);box-shadow:0 0 0 0 #ff6a00}60%{box-shadow:0 0 0 6px rgba(255,106,0,.45)}100%{transform:none;box-shadow:0 3px 0 var(--ink)}}
@media (prefers-reduced-motion:reduce){#dialog .line.qpop{animation:none}}
</style>""")
src = rep(src, "$('dTask').innerHTML = prevActHtml(st) + st.task; try{", "$('dTask').innerHTML = prevActHtml(st) + st.task; (function(){ const l=$('dTask').closest('.line'); if(l){ l.classList.remove('qpop'); void l.offsetWidth; l.classList.add('qpop'); } })(); try{")

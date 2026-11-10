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

# v61: 체험존 「웰체크 시뮬레이터」 화면으로 교체 (체험존 S2~S5 · 실무 M2·M3·M4·M6)
src = rep(src, "\n/* 초기화 */", "\n" + open(P('parts/course_sim.js'), encoding='utf-8').read() + "\n/* 초기화 */")
src = rep(src, "</style>", ".chtoast{top:auto;bottom:max(22px,env(safe-area-inset-bottom,0px))}\n</style>")

# v62: 의견이 쌓이는 구조 — 👍/👎 원탭 즉시 저장 + '막혔던 곳, 왜였나요?' 원탭(스텝·이유·오클릭 좌표가 함께 시트로)
src = rep(src, "function bindFb(host, result, res){ const card=host.querySelector('#fbCard'); if(!card) return;", "function bindFb(host, result, res){ const card=host.querySelector('#fbCard'); if(!card) return; try{ fbQuick(card,result,res); }catch(e){}")
src = rep(src, "\n/* 초기화 */", r"""
/* v62 원탭 의견 */
function fbBase(result,res){ return { ...(S.profile||{name:S.name}), course:S.course, stage:S.stage?S.stage.id:'', mode:S.mode, result, stars:res.stars||0, wrong:res.wrong, persona:S.persona?S.persona.key:'' }; }
function fbQuick(card,result,res){
  let sentT='';
  card.querySelectorAll('.thumbs button').forEach(b=>b.addEventListener('click',()=>{ const t=b.dataset.t; if(t===sentT) return; sentT=t;
    Promise.resolve(saveFeedback({ kind:'tap', ...fbBase(result,res), thumbs:t, tags:['원탭'], text:'', at:new Date().toISOString() })).catch(()=>{});
    const s=card.querySelector('.fbsub'); if(s) s.innerHTML='✓ 저장됐어요. <b>한 줄만 더</b> 적어 주시면 바로 고치는 데 씁니다.'; }));
  const sc=l=>(l.w||0)+(l.to||0);
  const hard=(res.steps||[]).filter(l=>sc(l)>0).sort((a,b)=>sc(b)-sc(a)).slice(0,2);
  if(!hard.length) return;
  const box=document.createElement('div'); box.className='fbwhy';
  box.innerHTML='<div class="fbwt">🚩 막혔던 곳 — 왜였나요? <span>한 번만 눌러 주세요</span></div>'+hard.map(l=>{ const st=STEPS.find(x=>x.id===l.id); const nm=st?String(st.task).replace(/<[^>]+>/g,'').slice(0,28):l.id;
    return '<div class="fbwr" data-id="'+l.id+'"><div class="fbwn">'+nm+' <i>오답 '+(l.w||0)+'</i></div><div class="fbwb">'+['문제가 모호','정답 위치가 이상','화면이 잘 안 보임','제가 몰랐어요'].map(r=>'<button type="button">'+r+'</button>').join('')+'</div></div>'; }).join('');
  const sub=card.querySelector('.fbsub'); if(!sub) return; sub.parentNode.insertBefore(box, sub.nextSibling);
  box.querySelectorAll('.fbwr').forEach(row=>row.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{ if(row.dataset.done) return; row.dataset.done='1'; const l=hard.find(x=>x.id===row.dataset.id); b.classList.add('on'); row.classList.add('done'); try{ SFX.pop(); }catch(e){}
    Promise.resolve(saveFeedback({ kind:'why', ...fbBase(result,res), thumbs:'', tags:['막힌 이유', b.textContent], text:'🚩 ['+l.id+'] '+b.textContent, step:l.id, reason:b.textContent, miss:l.miss||[], w:l.w||0, to:l.to||0, at:new Date().toISOString() })).catch(()=>{}); })));
}

/* 초기화 */""")
src = rep(src, "</style>", """.fbwhy{margin:8px 0 10px;padding:9px 10px;border:2px dashed #ff8a3d;border-radius:12px;background:#fff7ec;text-align:left}
.fbwt{font-weight:900;font-size:13.5px;color:#b34700;margin-bottom:6px}.fbwt span{font-weight:600;font-size:11px;color:#8a6a4a;margin-left:4px}
.fbwr{margin-top:6px}.fbwn{font-size:12.5px;font-weight:700;color:#1b1f3a;margin-bottom:4px}.fbwn i{font-style:normal;font-size:11px;color:#d23b3b;margin-left:4px}
.fbwb{display:flex;flex-wrap:wrap;gap:5px}.fbwb button{font:inherit;font-size:12px;font-weight:700;padding:6px 10px;border-radius:999px;border:2px solid #1b1f3a;background:#fff;color:#1b1f3a;cursor:pointer}
.fbwb button.on{background:#1b1f3a;color:#ffd84d}.fbwr.done button:not(.on){opacity:.35;pointer-events:none}.fbwr.done .fbwn::after{content:" ✓ 접수";color:#1a9c5b;font-size:11px}
</style>""")
src = rep(src, "</style>", "body:has(#overlayHost .g-panel) #play>#dialog{visibility:hidden}\n</style>")

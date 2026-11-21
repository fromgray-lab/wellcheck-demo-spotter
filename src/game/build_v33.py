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

# v63: 예전 의견 복구 — 이 기기에 남아 있는 의견(dsg_fb)은 '전송됨' 표시와 무관하게 한 번 더 시트로 (서버가 name+at 중복 제거)
src = rep(src, "if(SHEETS.url) setTimeout(async()=>{ try{ await flushOutbox(); }catch(e){} await resendLocalToSheet();", "if(SHEETS.url) setTimeout(async()=>{ try{ await flushOutbox(); }catch(e){} try{ await recoverFb63(); }catch(e){} await resendLocalToSheet();")
src = rep(src, "\n/* 초기화 */", r"""
async function recoverFb63(){ if(localStorage.getItem('dsg_fb_rec63')) return; if(!SHEETS.url || !(await shHealth())) return; let l=[]; try{ l=JSON.parse(localStorage.getItem('dsg_fb')||'[]'); }catch(e){} l=l.filter(d=>d&&d.at);
  let n=0; for(const d of l.slice(-100)){ try{ await shPost('feedback', Object.assign({}, d, {recovered:1})); markSent('feedback', d); n++; }catch(e){ return; } }
  localStorage.setItem('dsg_fb_rec63', String(n)); if(n) try{ toast('예전에 남기신 의견 '+n+'건을 다시 보냈어요 🙏'); }catch(e){} }

/* 초기화 */""")

# 루프 런타임 덮어쓰기 — 생성물(parts/course_sim.js)·원본 스텝을 직접 고치지 않고 스텝 id로 찾아 문구만 바꾼다(운영서 「자료」).
# v66 (2026-11-14, 규칙 L4 전수 점검): 같은 글자가 왼쪽 메뉴·구역 제목에도 있는 스텝에 '버튼'을 명시
LOOP_OVR = [
  ('h2',  'task', '성명 "테스트" 환자를 찾는 <b>조회</b> 버튼'),
  ('h5',  'task', '참여자 정보를 불러오는 <b>조회</b> 버튼'),
  ('h6',  'task', '<b>차감신청</b> 버튼으로 신청 창을 여세요'),
  ('ze3', 'task', '바구니에 담긴 상태 — <b>교육자료 발송</b> 버튼'),
  ('m4b', 'task', '바구니에 담긴 상태 — <b>교육자료 발송</b> 버튼'),
  # v67 (2026-11-15): L4 미룸 m2c · L3 전수 점검(폰 세로 지시문 4줄 이상) m0e·m0h
  ('m2c', 'task', '개별 발송 — 번호 입력 후 <b>초대장 발송</b> 버튼'),
  ('m0e', 'task', '① 우클릭 메뉴 — <b>HIRA e-Form Agent 로그인</b>'),
  ('m0h', 'task', '로그인 확인 — 작업표시줄 <b>파란 심평원 아이콘</b>'),
]
import json as _json
src = rep(src, "\n/* 초기화 */", "\n/* 루프 런타임 덮어쓰기 */\n(function(){ const L=" + _json.dumps(LOOP_OVR, ensure_ascii=False) + "; L.forEach(([id,k,v])=>{ const s=STEPS.find(x=>x.id===id); if(s) s[k]=v; }); })();\n/* 초기화 */")

# v68 (2026-11-19, 규칙 L9 전수 점검): 폰 가로(게임이 권하는 방향)에서 스테이지 클리어 화면의 👍/👎가 첫 화면 아래(스크롤해야 보임)에 있었음
# → 의견 카드를 별·성적 바로 아래(자유자재 지수·핵심 멘트 위)로 올려 스크롤 없이 원탭. 되돌리기: 이 rep 한 줄 삭제.
src = rep(src, "${S.demo||S.guide?'':fluHtml(S.stepLog.filter(l=>l.st===S.stage.id))}${recapHtml()}${S.demo?'':fbCardHtml()}",
               "${S.demo?'':fbCardHtml()}${S.demo||S.guide?'':fluHtml(S.stepLog.filter(l=>l.st===S.stage.id))}${recapHtml()}")

# v69 (2026-11-20, 규칙 L9 미룸 처리): 따라하기·복습 끝 화면(practiceEnd)에 의견 남길 길이 없었음 → 👍/👎 원탭 카드(kind:'tap', 기존 fbQuick 그대로)를
# 설명 바로 아래에 한 줄로 추가(폰 가로 342px에서 '실전 도전' 버튼이 밀려나지 않게 안내 줄 없이). 입력 단계 없음(L9). 되돌리기: 아래 rep 두 줄 삭제.
src = rep(src, "<p style=\"margin:6px 0 0;color:var(--dim)\">${desc}</p>${recapHtml()}<div class=\"btn-row\">${kind==='guide'?",
               "<p style=\"margin:6px 0 0;color:var(--dim)\">${desc}</p>${S.demo?'':pfbHtml()}${recapHtml()}<div class=\"btn-row\">${kind==='guide'?")
src = rep(src, "  $('nextStageBtn').addEventListener('click', ()=>{ host.innerHTML=''; if(kind==='guide'){ S.guide=false; startRun('one', id); }",
               "  try{ pfbBind(host, kind, id); }catch(e){}\n  $('nextStageBtn').addEventListener('click', ()=>{ host.innerHTML=''; if(kind==='guide'){ S.guide=false; startRun('one', id); }")
src = rep(src, "\n/* 초기화 */", r"""
/* v69 따라하기·복습 끝 원탭 의견 */
function pfbHtml(){ return '<div class="fb" id="fbCard"><div class="fbt"><span>📝 이 연습, 어땠나요?</span><span class="thumbs"><button type="button" data-t="up" title="좋아요">👍</button><button type="button" data-t="down" title="별로예요">👎</button></span></div></div>'; }
function pfbBind(host, kind, id){ const c=host.querySelector('#fbCard'); if(!c) return; const r=(S.stageRes&&S.stageRes[id])||{}; fbQuick(c, kind==='guide'?'guide':'review', {stars:0, wrong:r.wrong||0, steps:[]});
  c.querySelectorAll('.thumbs button').forEach(b=>b.addEventListener('click',()=>{ c.querySelectorAll('.thumbs button').forEach(x=>x.classList.toggle('on',x===b)); const s=c.querySelector('.fbt>span'); if(s) s.textContent='✓ 저장됐어요. 고맙습니다!'; try{ SFX.pop(); }catch(e){} })); }

/* 초기화 */""")

# v70 (2026-11-21, 규칙 L9 미룸 처리): 순서 맞추기 끝 화면(.oresult)에 의견 남길 길이 없었음 → 👍/👎 한 줄 원탭 카드(kind:'tap', result='order')를
# 별·틀림 줄 아래에 추가하고, 끝나면 결과 상자를 화면 안으로 스크롤(카드 그리드 아래에 붙어 폰에선 첫 화면 밖이었음). 입력 단계 없음(L9).
# fbBase는 S.stage·S.mode(직전 실전 값)를 쓰므로 stage·mode를 순서 맞추기 값으로 덮어 저장. 되돌리기: 아래 rep 세 줄 삭제.
# (숫자 특훈·응대 특훈 끝 화면은 v43에서 진입 칩이 빠져 도달할 수 없어 대상 아님)
src = rep(src, ":''}<div class=\"btn-row\"><button type=\"button\" class=\"g-btn green\" id=\"oAgain\">",
               ":''}${ofbHtml()}<div class=\"btn-row\"><button type=\"button\" class=\"g-btn green\" id=\"oAgain\">")
src = rep(src, "$('oAgain').addEventListener('click', ()=>openOrder(stageId));",
               "try{ ofbBind(host, stageId, wrong, stars); }catch(e){} $('oAgain').addEventListener('click', ()=>openOrder(stageId));")
src = rep(src, "\n/* 초기화 */", r"""
/* v70 순서 맞추기 끝 원탭 의견 */
function ofbHtml(){ return '<div class="fb" id="ofbCard" style="margin:8px auto 0;max-width:420px"><div class="fbt"><span>📝 이 연습, 어땠나요?</span><span class="thumbs"><button type="button" data-t="up" title="좋아요">👍</button><button type="button" data-t="down" title="별로예요">👎</button></span></div></div>'; }
function ofbBind(host, stageId, wrong, stars){ const c=host.querySelector('#ofbCard'); let sent=''; if(c) c.querySelectorAll('.thumbs button').forEach(b=>b.addEventListener('click',()=>{ const t=b.dataset.t; if(t===sent) return; sent=t;
    Promise.resolve(saveFeedback({ kind:'tap', ...fbBase('order',{stars, wrong}), stage:stageId, mode:'order', thumbs:t, tags:['원탭'], text:'', at:new Date().toISOString() })).catch(()=>{});
    c.querySelectorAll('.thumbs button').forEach(x=>x.classList.toggle('on',x===b)); const s=c.querySelector('.fbt>span'); if(s) s.textContent='✓ 저장됐어요. 고맙습니다!'; try{ SFX.pop(); }catch(e){} }));
  const r=host.querySelector('.oresult'); if(r) setTimeout(()=>{ try{ r.scrollIntoView({block:'end',behavior:'smooth'}); }catch(e){} }, 60); }

/* 초기화 */""")

# v71 (2026-11-22, 규칙 L10 전수 점검): 시트 쓰기(shPost)는 교차 출처라 응답을 못 읽어 2.5초 뒤 '보냄'으로 간주하고 markSent로 '전송됨'에 올린다.
# 그 POST가 실제로는 유실돼도(연결 끊김·서버 오류) '전송됨'이라 resendLocalToSheet가 다시 보내지 않아 기기에만 남는 구멍이 있었음 = 도착 확인 없는 저장.
# → 시작할 때 시트를 읽어(최근 300행, 서버 중복 제거 창과 같음) '전송됨'인데 시트에 없는 기록·의견·평가를 '전송됨'에서 빼 기존 재전송이 다시 보내게 함.
# 보내는 길(shPost)은 바꾸지 않음. 10분 안의 것·읽은 창보다 오래된 것은 건드리지 않음(중복 방지). 되돌리기: 아래 rep 세 줄 삭제.
src = rep(src, "function shGet(col){", "function shGet(col, lim){")
src = rep(src, "'&limit=3000&cb='", "'&limit='+(lim||3000)+'&cb='")
src = rep(src, "try{ await recoverFb63(); }catch(e){} await resendLocalToSheet();", "try{ await recoverFb63(); }catch(e){} try{ await verifySentOnSheet(); }catch(e){} await resendLocalToSheet();")
src = rep(src, "\n/* 초기화 */", r"""
/* v71 도착 확인: '전송됨'인데 시트에 없는 것은 다시 보낼 대상으로 */
async function verifySentOnSheet(){ if(!SHEETS.url || !(await shHealth())) return 0; let sent; try{ sent=JSON.parse(localStorage.getItem('dsg_sent')||'[]'); }catch(e){ return 0; } if(!sent.length) return 0;
  const LIM=300, cut=new Date(Date.now()-10*60000).toISOString(), drop=new Set();
  for(const col of ['runs','feedback','evals']){ let rows; try{ rows=await shGet(col, LIM); }catch(e){ continue; } if(!Array.isArray(rows)) continue;
    const have=new Set(rows.map(r=>col+'|'+((r&&r.name)||'')+'|'+((r&&r.at)||''))); let oldest=''; if(rows.length>=LIM) rows.forEach(r=>{ if(r&&r.at&&(!oldest||r.at<oldest)) oldest=r.at; });
    sent.forEach(k=>{ if(k.indexOf(col+'|')!==0) return; const at=k.slice(k.lastIndexOf('|')+1); if(!at||at>=cut||(oldest&&at<oldest)) return; if(!have.has(k)) drop.add(k); }); }
  if(drop.size){ try{ localStorage.setItem('dsg_sent', JSON.stringify(sent.filter(k=>!drop.has(k)))); }catch(e){} }
  return drop.size; }

/* 초기화 */""")

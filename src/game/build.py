#!/usr/bin/env python3
"""Assemble demo-spotter.html (v6: 오마주 리디자인 + 메뉴얼 코스 + 피드백/텔레메트리) from v5 + parts."""
import re, os, sys, json
ROOT = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(ROOT, *a)
src = open(P('demo-spotter.v5.html'), encoding='utf-8').read()
parts = lambda n: open(P('parts', n), encoding='utf-8').read()

def rep(s, old, new, count=1):
    assert s.count(old) >= 1, 'MISSING: ' + old[:90]
    if count == 1:
        assert s.count(old) == 1, 'AMBIGUOUS (%d): %s' % (s.count(old), old[:90])
    return s.replace(old, new) if count != 1 else s.replace(old, new, 1)

# ── 1) CSS
css = parts('style.css')
src = re.sub(r'<style>.*?</style>', lambda m: '<style>\n' + css + '</style>', src, count=1, flags=re.S)

# ── 2) 배경 + 타이틀 + 임무판/플레이 HTML
src = rep(src, '<div class="sky" aria-hidden="true"><div class="cloud c1"></div><div class="cloud c2"></div><div class="cloud c3"></div></div>', '<div class="sunburst" aria-hidden="true"></div>')
title = parts('title.html').replace('<!--SYMBOLS-->', parts('symbols.svg.html'))
src = re.sub(r'<!-- ═════════ 타이틀 ═════════ -->.*?</section>\n', lambda m: title, src, count=1, flags=re.S)
src = re.sub(r'<!-- ═════════ 스테이지 맵 ═════════ -->.*?<!-- ═════════ 결과 ═════════ -->', lambda m: parts('map_play.html') + '\n<!-- ═════════ 결과 ═════════ -->', src, count=1, flags=re.S)

# ── 3) 결과(동의서/수료증) 마크업: 제목·행을 JS가 채움
src = rep(src, '''      <h2>웰체크 도입 동의서</h2>
      <table>
        <tr><td>의료기관</td><td id="cClinic">—</td></tr>
        <tr><td>원장님 유형</td><td id="cPersona">—</td></tr>
        <tr><td>시연자</td><td id="cPlayer">—</td></tr>
        <tr><td>시연 일시</td><td id="cDate">—</td></tr>
        <tr><td>시연 소요시간</td><td id="cTime">—</td></tr>
        <tr><td>원장님 판정</td><td id="cVerdict">—</td></tr>
      </table>
      <div class="sig"><span>원장 서명</span><span class="name" id="cSig">김 원 장</span></div>''',
'''      <h2 id="cTitle">웰체크 도입 동의서</h2>
      <table><tbody id="cRows"></tbody></table>
      <div class="sig"><span id="cSigLabel">원장 서명</span><span class="name" id="cSig">김 원 장</span></div>''')

# ── 4) 게임 방법 모달
src = re.sub(r'<h2 class="g">틀린 그림 찾기처럼, 틀리지 않게 시연하기</h2>.*?<div class="btn-row"><button type="button" class="g-btn" id="howClose">닫기</button></div>', lambda m: '''<h2 class="g">틀린 그림 찾기처럼, 틀리지 않게 시연하기</h2>
    <div class="rules">
      <div class="rule"><div class="ic">⭕</div><b>정답 클릭</b>시연 순서에 맞는 자리를 누르면 동그라미</div>
      <div class="rule"><div class="ic">❌</div><b>오답 클릭</b>엑스 + 원장님 인내심 −15%. 0이면 원장님 퇴장</div>
      <div class="rule"><div class="ic">💡</div><b>2번 틀리면</b>힌트와 따뜻한 영역이 열립니다</div>
      <div class="rule"><div class="ic"><svg viewBox="0 0 64 64"><use href="#symMag"/></svg></div><b>돋보기 = 찬스 (3회)</b>정답 자리를 짚어주지만 감점 8점</div>
      <div class="rule"><div class="ic"><svg viewBox="0 0 64 64"><use href="#symBulb"/></svg></div><b>전구 = 팁</b>이 화면에서 원장님께 할 말. 감점 없음</div>
      <div class="rule"><div class="ic">⭐</div><b>별점</b>스테이지 무결점 3★ · 실수 2회 이하 2★ · 클리어 1★</div>
      <div class="rule"><div class="ic">📘</div><b>웰체크 실무 코스</b>공식 메뉴얼 8단계(Agent·가입·초대등록·포괄평가·교육상담·환자관리·점검평가·건생)의 실제 화면</div>
      <div class="rule"><div class="ic">🏥</div><b>체험존(Patient Care Room) 시연 코스</b>원장님 앞 10분 시연 흐름(오프닝·EMR·등록·케어플랜·건생)</div>
      <div class="rule"><div class="ic">📝</div><b>스테이지 피드백</b>끝날 때마다 👍👎·태그·한 줄 의견 → 개선 루프</div>
    </div>
    <p class="kbd" style="margin:10px 0 0">전체 완주 점수 = 100 − 오답×5 − 찬스×8. S 100 · A 90↑ · B 75↑ · C 60↑ · D · F(원장님 퇴장). 시간 초과도 오답 1회. 👀 시범은 정답과 멘트를 보여주는 자동 재생.</p>
    <div class="btn-row"><button type="button" class="g-btn" id="howClose">닫기</button></div>''', src, count=1, flags=re.S)

# ── 5) JS: 데이터
src = rep(src, 'const R = (l,t,w,h) => ({l,t,w,h});', 'const IMGA = {}; /* 보드 가로세로비 (없으면 체험존 1512/795) */\nconst R = (l,t,w,h) => ({l,t,w,h});')
src = re.sub(r"/\* 스테이지 = 일만사 행위 단위 \*/\nconst STAGES = \[.*?\n\];", lambda m: '''/* 스테이지 = 일만사 행위 단위. course: zone(체험존 시연) / biz(웰체크 실무 메뉴얼) */
const STAGES = [
  { id:'open', course:'zone', n:0, title:'오프닝', sub:'체험존 입장 · 원장님과 대화 열기', color:'#ff6fb5' },
  { id:'emr',  course:'zone', n:1, title:'EMR 기초자료 세팅', sub:'오름차트에서 대상환자 선별 · 수가 · 설득 자료', color:'#2b9bff' },
  { id:'reg',  course:'zone', n:2, title:'일만사 환자등록', sub:'초대장 · 심평원 포털 대상자 등록', color:'#5ad36b' },
  { id:'plan', course:'zone', n:3, title:'케어플랜', sub:'포괄평가/계획수립 · 심평원 임시저장', color:'#ff9f1c' },
  { id:'hs',   course:'zone', n:4, title:'건생 포인트', sub:'건강생활실천지원금 대리신청 · 포인트 차감 · 체험 종료', color:'#ff5252' }
];
const COURSES = { biz:{ name:'웰체크 실무', long:'웰체크 실무 · 메뉴얼 8단계', code:'M', doc:'수료증' }, zone:{ name:'체험존(Patient Care Room) 시연', long:'체험존(Patient Care Room) 시연 · 5단계', code:'S', doc:'동의서' } };
function stageCode(st){ return (COURSES[st.course]||COURSES.zone).code + st.n; }''', src, count=1, flags=re.S)
src = rep(src, "\n];\n\n/* ═══════════════════════════════════════════ 상태", "\n];\n" + parts('course_manual.js').replace('/*YSR*/', parts('course_ysr.js')+parts('course_dh.js')) + "\n/* ═══════════════════════════════════════════ 상태")

# ── 6) 상태 · 화면 전환 · 타이틀
src = rep(src, "const S = { persona:null, name:'', timed:true, mode:'all',", "const S = { persona:null, name:'', timed:true, mode:'all', course:'biz', stepLog:[], cur:null,")
src = rep(src, "function show(id){ document.querySelectorAll('.screen').forEach(s=>s.classList.toggle('on', s.id===id));", "function show(id){ document.body.dataset.screen=id; document.querySelectorAll('.screen').forEach(s=>s.classList.toggle('on', s.id===id));")
src = rep(src, "$('title').addEventListener('click', e=>{ if(e.target.closest('.corner')) return; SFX.go(); openSetup(); });", "$('title').addEventListener('click', e=>{ if(e.target.closest('.tui button')) return; SFX.go(); openSetup(); });\n$('btnStart').addEventListener('click', e=>{ e.stopPropagation(); SFX.go(); openSetup(); });")

# ── 7) 임무판 렌더 (코스 탭 + 폴라로이드 카드)
src = re.sub(r"function renderMap\(\)\{.*?\n\}\n\$\('playAll'\)", lambda m: '''function loadCourse(){ try{ const c=localStorage.getItem('dsg_course'); if(COURSES[c]) S.course=c; }catch(e){} }
function setCourse(c){ S.course=c; try{ localStorage.setItem('dsg_course',c); }catch(e){} renderMap(); }
document.querySelectorAll('#courseTabs .ctab').forEach(b=>b.addEventListener('click', ()=>{ SFX.pop(); setCourse(b.dataset.course); }));
function preloadStage(id){ STEPS.filter(s=>s.st===id).forEach(s=>{ [s.img,s.end].filter(Boolean).forEach(k=>{ const i=new Image(); i.src=IMG[k]; }); }); }
function renderMap(){
  loadStars();
  $('mapPlayer').textContent = profileLabel(S.profile) || S.name || '시연자'; $('mapDoctor').lastElementChild.textContent = S.persona ? S.persona.name.split(' ')[0] + ' · ' + S.persona.short : '원장님';
  document.querySelectorAll('#courseTabs .ctab').forEach(b=>b.classList.toggle('on', b.dataset.course===S.course));
  const C=COURSES[S.course]; $('playAll').textContent = S.course==='biz' ? '▶ 실무 8단계 완주 · 자유자재 MR 도전' : '▶ 전체 시연 · 자유자재 MR 도전';
  $('mapNote').textContent = S.course==='biz' ? '공식 메뉴얼 「웰체크 활용 실무: 일만사 중심」의 실제 화면 70장면. 스테이지만 골라 연습해도 되고, 8단계를 완주하면 수료증이 나옵니다.' : '체험존(patientcareroom) 시연 흐름. 스테이지만 골라 연습해도 되고, 전체 시연을 완주하면 동의서 성적표가 나옵니다.';
  const g=$('stageGrid'); g.innerHTML='';
  STAGES.filter(st=>st.course===S.course).forEach(st=>{
    const steps = STEPS.filter(s=>s.st===st.id && (!s.branch || s.branch===(S.persona||PERSONAS.no).key));
    const first=steps[0]; const r=first?first.rects[0]:null;
    const b=document.createElement('button'); b.type='button'; b.className='stage'+(st.locked?' locked':''); b.disabled=!!st.locked;
    const best = S.stars[st.id];
    b.innerHTML = `<span class="pin"></span><div class="num" style="background:${st.color}">${st.locked?'🔒':st.n}</div><div class="thumb" style="--ar:${first?(IMGA[first.img]||ASPECT).toFixed(3):'1.9'};background-image:url(${first?IMG[first.img]:''})">${r?`<span class="o" style="left:${r.l+r.w/2}%;top:${r.t+r.h/2}%"></span>`:''}<svg class="mag" viewBox="0 0 64 64" aria-hidden="true"><use href="#symMag"/></svg></div><b><span class="code">${stageCode(st)}</span>${st.title}</b><small>${st.locked ? st.locked : st.sub+' · '+steps.length+'클릭'+(st.page?' · '+st.page:'')}</small>${st.locked?'':starsHtml(best ? best.stars : 0)}${best?`<span class="best ${best.wrong===0&&best.chance===0?'perfect':''}">${best.wrong===0&&best.chance===0?'PERFECT':'오답 '+best.wrong} · ${fmtTime(best.secs||0)}</span>`:''}${st.locked?'<span class="tape">COMING SOON</span>':'<span class="demo" role="button" tabindex="0">👀 시범</span>'}`;
    if(!st.locked){ b.addEventListener('click', e=>{ const isDemo = !!e.target.closest('.demo'); SFX.go(); startRun('one', st.id, isDemo); }); }
    g.appendChild(b);
  });
}
$('playAll')''', src, count=1, flags=re.S)

# ── 8) 런/스테이지
src = rep(src, "S.queue = mode==='all' ? STAGES.filter(s=>!s.locked).map(s=>s.id) : [stageId]; S.qi = 0;", "S.queue = mode==='all' ? STAGES.filter(s=>s.course===S.course && !s.locked).map(s=>s.id) : [stageId]; S.qi = 0; S.stepLog=[]; S.cur=null;\n  if(stageId){ const st0=STAGES.find(s=>s.id===stageId); if(st0&&st0.course&&st0.course!==S.course) setCourse(st0.course); }")
src = rep(src, "  S.stageRes[id] = { wrong:0, chance:0, tips:0, start:Date.now() };", "  S.stageRes[id] = { wrong:0, chance:0, tips:0, start:Date.now() }; preloadStage(id);")
src = rep(src, "$('dTask').innerHTML=`<b>STAGE ${S.stage.n}</b> ${S.stage.title} — ${S.stage.sub}`;", "$('dTask').innerHTML=`<b>${stageCode(S.stage)}</b> ${S.stage.title} — ${S.stage.sub}`;")
src = rep(src, "  host.innerHTML = `<div class=\"count\"><div style=\"text-align:center\"><div class=\"wood\" style=\"font-size:clamp(18px,3vw,30px)\">STAGE ${st.n} · ${st.title}</div>", "  host.innerHTML = `<div class=\"count\"><div style=\"text-align:center\"><div class=\"wood\" style=\"font-size:clamp(18px,3vw,30px)\">${stageCode(st)} · ${st.title}</div>")
src = rep(src, "$('stageBadge').textContent = (S.demo?'👀 시범 · ':'') + (innerWidth<700 ? `STAGE ${S.stage.n}` : `STAGE ${S.stage.n} · ${S.stage.title}`);", "$('stageBadge').textContent = (S.demo?'👀 시범 · ':'') + (innerWidth<700 ? stageCode(S.stage) : `${stageCode(S.stage)} · ${S.stage.title}`);")
src = rep(src, "$('quitBtn').addEventListener('click', ()=>{ clearInterval(S.timer); stopStepTimer(); exitFullscreen(); renderMap(); show('map'); });", "$('quitBtn').addEventListener('click', ()=>{ clearInterval(S.timer); stopStepTimer(); exitFullscreen(); renderMap(); show('map'); });\n$('clockHand').style.transformOrigin='32px 36px'; $('clockHand').style.transformBox='view-box';")

# ── 9) 아레나: 보드별 가로세로비
src = rep(src, "const ASPECT=1512/795; const Z={s:1,tx:0,ty:0,W:0,H:0,aw:0,ah:0,min:1,max:4};", "const ASPECT=1512/795; const Z={s:1,tx:0,ty:0,W:0,H:0,aw:0,ah:0,min:1,max:4,aspect:ASPECT};")
src = rep(src, "if(aw/ah>ASPECT){ Z.H=ah; Z.W=Math.round(ah*ASPECT); } else { Z.W=aw; Z.H=Math.round(aw/ASPECT); }", "if(aw/ah>Z.aspect){ Z.H=ah; Z.W=Math.round(ah*Z.aspect); } else { Z.W=aw; Z.H=Math.round(aw/Z.aspect); }")
src = rep(src, "function setBoard(key, reset){ const changed = $('shot').getAttribute('src')!==IMG[key]; $('shot').src=IMG[key]; $('ambient').style.backgroundImage=`url(${IMG[key]})`; fitArena(true);", "function setBoard(key, reset){ const changed = $('shot').getAttribute('src')!==IMG[key]; $('shot').src=IMG[key]; $('ambient').style.backgroundImage=`url(${IMG[key]})`; Z.aspect = IMGA[key]||ASPECT; fitArena(true);")
# 스텝 타이머: 시계 바늘
src = rep(src, "T.iv=setInterval(()=>{ const left=Math.max(0,T.deadline-Date.now()); $('tfill').style.transform=`scaleX(${left/(LIMIT*1000)})`;", "T.iv=setInterval(()=>{ const left=Math.max(0,T.deadline-Date.now()); $('tfill').style.transform=`scaleX(${left/(LIMIT*1000)})`; $('clockHand').style.transform=`rotate(${Math.round((1-left/(LIMIT*1000))*360)}deg)`;")

# ── 10) 스텝 렌더 · 텔레메트리 · 표정
src = rep(src, "  S.stepWrong=0; S.stepChance=false; S.locked=false; S.busy=false;\n", "  S.stepWrong=0; S.stepChance=false; S.locked=false; S.busy=false; S.cur={ id:st.id, st:st.st, t0:Date.now(), w:0, c:0, tips:0, to:0, miss:[] };\n")
src = rep(src, "  setMouth('neutral'); renderHUD();", "  setMood('neutral'); renderHUD();")
src = rep(src, "function setMouth(m){ const el=$('docMouth'); if(el) el.setAttribute('d', m==='happy'?'M24 45 Q32 55 40 45' : m==='angry'?'M26 50 Q32 44 38 50' : 'M26 47 Q32 51 38 47'); }",
'''function setMood(m){ const mouth = m==='happy'?'M24 45 Q32 55 40 45' : m==='angry'?'M26 50 Q32 44 38 50' : 'M26 47 Q32 51 38 47'; const low=S.patience<=50, crit=S.patience<=30;
  document.querySelectorAll('.docface').forEach(f=>{ f.querySelector('.docMouth').setAttribute('d', mouth); f.querySelector('.docBrowL').setAttribute('d', m==='angry'||crit ? 'M16 24 Q23 26 30 29' : m==='happy' ? 'M16 26 Q23 21 30 25' : 'M16 27 Q23 23 30 27'); f.querySelector('.docBrowR').setAttribute('d', m==='angry'||crit ? 'M34 29 Q41 26 48 24' : m==='happy' ? 'M34 25 Q41 21 48 26' : 'M34 27 Q41 23 48 27'); f.querySelector('.docSweat').style.display = low ? '' : 'none'; f.querySelector('.docAnger').style.display = crit ? '' : 'none'; }); }
const setMouth = setMood;''')
src = rep(src, "  S.locked=true; S.busy=true; stopStepTimer(); SFX.good(); setMouth('happy');", "  S.locked=true; S.busy=true; stopStepTimer(); SFX.good(); setMood('happy'); if(S.cur){ S.cur.s=Math.round((Date.now()-S.cur.t0)/1000); S.stepLog.push(S.cur); S.cur=null; }")
src = rep(src, "  SFX.wrong(); setMouth('angry'); flash('bad');", "  SFX.wrong(); flash('bad'); if(S.cur){ if(xy){ S.cur.w++; if(S.cur.miss.length<6) S.cur.miss.push([Math.round(xy[0]),Math.round(xy[1])]); } else S.cur.to++; }")
src = rep(src, "  S.patience=Math.max(0,S.patience-15); renderHUD();\n  if(S.patience<=0) gameOver();", "  S.patience=Math.max(0,S.patience-15); setMood('angry'); renderHUD();\n  if(S.patience<=0) gameOver();")
src = rep(src, "S.chances--; S.chance++; S.stepChance=true;", "S.chances--; S.chance++; S.stepChance=true; if(S.cur) S.cur.c=1;")
src = rep(src, "S.tips++; if(S.stageRes[S.stage.id]) S.stageRes[S.stage.id].tips++; SFX.tip();", "S.tips++; if(S.cur) S.cur.tips++; if(S.stageRes[S.stage.id]) S.stageRes[S.stage.id].tips++; SFX.tip();")
src = re.sub(r'<div class="bear"><svg viewBox="0 0 120 120" aria-hidden="true">.*?</svg><div class="bubble">', '<div class="bear"><svg viewBox="0 0 120 130" aria-hidden="true"><use href="#chBear"/></svg><div class="bubble">', src, count=1, flags=re.S)

# ── 11) 피드백/텔레메트리 블록 삽입 (스테이지 클리어 섹션 앞)
fb_block = r'''
/* ═══════════════════════════════════════════ 피드백(스테이지마다) · 텔레메트리 · 평가자 평가 ═══════════════════════════════════════════ */
const FB_TAGS=['힌트가 애매해요','정답 위치가 실제와 달라요','화면이 실제와 달라요','순서가 이상해요','팁 설명이 부족해요','너무 쉬움','너무 어려움','재밌어요'];
function fbCardHtml(){ return `<div class="fb" id="fbCard"><div class="fbt"><span>📝 이 스테이지, 어땠나요?</span><span class="thumbs"><button type="button" data-t="up" title="좋아요">👍</button><button type="button" data-t="down" title="별로예요">👎</button></span></div><div class="tags">${FB_TAGS.map(t=>`<button type="button" data-tag="${esc(t)}">${esc(t)}</button>`).join('')}</div><input id="fbText" type="text" maxlength="120" placeholder="한 줄 의견 (선택) — 예: 저장 버튼 위치가 헷갈려요" autocomplete="off"><div class="fbrow"><span class="kbd">의견은 개선 루프에 모여 힌트·좌표·팁을 고치는 데 씁니다</span><button type="button" class="g-btn sm blue" id="fbSend">보내기</button></div></div>`; }
function compactSteps(steps){ const o={}; (steps||[]).forEach(l=>{ o[l.id]=[l.w||0,l.c||0,l.tips||0,l.s||0,l.to||0,l.miss||[]]; }); return o; }
function bindFb(host, result, res){ const card=host.querySelector('#fbCard'); if(!card) return; let thumbs=''; const tags=new Set();
  card.querySelectorAll('.thumbs button').forEach(b=>b.addEventListener('click',()=>{ thumbs=b.dataset.t; card.querySelectorAll('.thumbs button').forEach(x=>x.classList.toggle('on',x===b)); SFX.pop(); }));
  card.querySelectorAll('.tags button').forEach(b=>b.addEventListener('click',()=>{ const t=b.dataset.tag; if(tags.has(t)) tags.delete(t); else tags.add(t); b.classList.toggle('on',tags.has(t)); SFX.pop(); }));
  card.querySelector('#fbText').addEventListener('keydown', e=>{ e.stopPropagation(); if(e.key==='Enter') card.querySelector('#fbSend').click(); });
  card.querySelector('#fbSend').addEventListener('click', async ()=>{ const text=(card.querySelector('#fbText').value||'').trim(); if(!thumbs && !tags.size && !text){ card.querySelector('#fbText').focus(); return; }
    const fb={ kind:'stage', ...(S.profile||{name:S.name}), course:S.course, stage:S.stage.id, mode:S.mode, result, thumbs, tags:[...tags], text, stars:res.stars||0, wrong:res.wrong, chance:res.chance, tips:res.tips, secs:res.secs||0, steps:compactSteps(res.steps), persona:S.persona?S.persona.key:'', at:new Date().toISOString() };
    card.innerHTML='<div class="ok">고마워요! 의견이 개선 루프에 들어갔어요 ✓</div>'; SFX.star(); await saveFeedback(fb); }); }
function localList(key){ try{ return JSON.parse(localStorage.getItem(key)||'[]'); }catch(e){ return []; } }
function localPush(key, obj, cap){ try{ const l=localList(key); l.unshift(obj); localStorage.setItem(key, JSON.stringify(l.slice(0,cap||200))); }catch(e){} }
async function saveFeedback(fb){ localPush('dsg_fb', fb, 300); if(SUPABASE.url&&SUPABASE.key){ try{ await sbFetch('dsg_feedback',{method:'POST',body:JSON.stringify(fb)}); return 'supabase'; }catch(e){} } const db=await getDB(); if(db){ try{ await db.collection('feedback').add(fb); return 'db'; }catch(e){} } return 'local'; }
async function loadFeedback(){ if(SUPABASE.url&&SUPABASE.key){ try{ const r=await sbFetch('dsg_feedback?select=*&order=at.desc&limit=3000',{headers:{Prefer:''}}); return await r.json(); }catch(e){} } const db=await getDB(); if(db){ try{ const snap=await db.collection('feedback').orderBy('at','desc').limit(2000).get(); return snap.docs.map(d=>({id:d.id,...d.data()})); }catch(e){} } return localList('dsg_fb'); }
async function saveEval(ev){ localPush('dsg_evals', ev, 300); if(SUPABASE.url&&SUPABASE.key){ try{ await sbFetch('dsg_evals',{method:'POST',body:JSON.stringify(ev)}); return 'supabase'; }catch(e){} } const db=await getDB(); if(db){ try{ await db.collection('evals').add(ev); return 'db'; }catch(e){} } return 'local'; }
async function loadEvals(){ if(SUPABASE.url&&SUPABASE.key){ try{ const r=await sbFetch('dsg_evals?select=*&order=at.desc&limit=3000',{headers:{Prefer:''}}); return await r.json(); }catch(e){} } const db=await getDB(); if(db){ try{ const snap=await db.collection('evals').orderBy('at','desc').limit(2000).get(); return snap.docs.map(d=>({id:d.id,...d.data()})); }catch(e){} } return localList('dsg_evals'); }
const EVAL_AXES=[['acc','정확성'],['flow','흐름'],['persuade','설득력'],['respond','응대']];

/* ═══════════════════════════════════════════ 스테이지 클리어 / 게임오버'''
src = rep(src, "\n/* ═══════════════════════════════════════════ 스테이지 클리어 / 게임오버", fb_block)

# 스테이지 클리어: 캐릭터 + 피드백
src = rep(src, "res.secs=Math.floor((Date.now()-res.start)/1000); res.stars=stageStars(res); res.cleared=true;", "res.secs=Math.floor((Date.now()-res.start)/1000); res.stars=stageStars(res); res.cleared=true; res.steps=S.stepLog.filter(l=>l.st===id);")
src = rep(src, "saveRun({ ...(S.profile||{name:S.name}), persona:S.persona.key, mode:'one', stage:id, grade:'', score:Math.max(0,100-W_WRONG*res.wrong-W_CHANCE*res.chance), wrong:res.wrong, chance:res.chance, tips:res.tips, secs:res.secs, at:new Date().toISOString(), over:false, stars:{[id]:res.stars} });",
                 "saveRun({ ...(S.profile||{name:S.name}), persona:S.persona.key, mode:'one', course:S.course, stage:id, grade:'', score:Math.max(0,100-W_WRONG*res.wrong-W_CHANCE*res.chance), wrong:res.wrong, chance:res.chance, tips:res.tips, secs:res.secs, at:new Date().toISOString(), over:false, stars:{[id]:res.stars}, steps:compactSteps(res.steps) });")
src = rep(src, "const host=$('overlayHost'); host.innerHTML=`<div class=\"overlay\" style=\"pointer-events:auto\"><div class=\"g-panel\"><div class=\"banner\">STAGE CLEAR!</div><div style=\"font-family:var(--display);color:var(--dim)\">STAGE ${S.stage.n} · ${S.stage.title}</div>${starsHtml(0,true)}<div class=\"tally\"><div><small>오답</small><b>${res.wrong}</b></div><div><small>찬스</small><b>${res.chance}</b></div><div><small>시간</small><b>${fmtTime(res.secs)}</b></div></div><div class=\"btn-row\">",
                 "const host=$('overlayHost'); host.innerHTML=`<div class=\"overlay\" style=\"pointer-events:auto\"><div class=\"g-panel\"><svg class=\"ovchar r\" viewBox=\"0 0 280 330\" aria-hidden=\"true\"><use href=\"#chDocYes\"/></svg><div class=\"banner\">STAGE CLEAR!</div><div style=\"font-family:var(--display);color:var(--dim)\">${stageCode(S.stage)} · ${S.stage.title}</div>${starsHtml(0,true)}<div class=\"tally\"><div><small>오답</small><b>${res.wrong}</b></div><div><small>찬스</small><b>${res.chance}</b></div><div><small>시간</small><b>${fmtTime(res.secs)}</b></div></div>${S.demo?'':fbCardHtml()}<div class=\"btn-row\">")
src = rep(src, "  const stars=host.querySelectorAll('.bigstars i'); for(let i=0;i<res.stars;i++){ setTimeout(()=>{ stars[i].classList.add('on'); SFX.star(); }, 500+i*380); }", "  const stars=host.querySelectorAll('.bigstars i'); for(let i=0;i<res.stars;i++){ setTimeout(()=>{ stars[i].classList.add('on'); SFX.star(); }, 500+i*380); }\n  bindFb(host,'clear',res);")
# 게임오버
src = rep(src, "function gameOver(){ if(S.over) return; S.over=true; S.locked=true; stopStepTimer(); SFX.over(); const id=S.stage.id; const res=S.stageRes[id]; res.cleared=false; res.stars=0;", "function gameOver(){ if(S.over) return; S.over=true; S.locked=true; stopStepTimer(); SFX.over(); const id=S.stage.id; const res=S.stageRes[id]; res.cleared=false; res.stars=0; if(S.cur){ S.cur.s=Math.round((Date.now()-S.cur.t0)/1000); S.stepLog.push(S.cur); S.cur=null; } res.steps=S.stepLog.filter(l=>l.st===id); res.secs=Math.floor((Date.now()-res.start)/1000);")
src = rep(src, "host.innerHTML=`<div class=\"overlay\" style=\"pointer-events:auto\"><div class=\"g-panel\"><div class=\"banner red\">원장님 퇴장…</div><p style=\"margin:6px 0 0;color:var(--dim)\">\"다음에 다시 봅시다.\" 인내심이 바닥났습니다.</p><div class=\"tally\"><div><small>이 스테이지 오답</small><b>${res.wrong}</b></div><div><small>찬스</small><b>${res.chance}</b></div><div><small>남은 단계</small><b>${S.steps.length-S.idx}</b></div></div><div class=\"btn-row\">",
                 "host.innerHTML=`<div class=\"overlay\" style=\"pointer-events:auto\"><div class=\"g-panel\"><svg class=\"ovchar l\" viewBox=\"0 0 280 330\" aria-hidden=\"true\"><use href=\"#chDocDizzy\"/></svg><div class=\"banner red\">원장님 퇴장…</div><p style=\"margin:6px 0 0;color:var(--dim)\">\"다음에 다시 봅시다.\" 인내심이 바닥났습니다.</p><div class=\"tally\"><div><small>이 스테이지 오답</small><b>${res.wrong}</b></div><div><small>찬스</small><b>${res.chance}</b></div><div><small>남은 단계</small><b>${S.steps.length-S.idx}</b></div></div>${fbCardHtml()}<div class=\"btn-row\">")
src = rep(src, "    $('toMap2').addEventListener('click', ()=>{ host.innerHTML=''; exitFullscreen(); renderMap(); show('map'); });\n  }, 900);", "    $('toMap2').addEventListener('click', ()=>{ host.innerHTML=''; exitFullscreen(); renderMap(); show('map'); });\n    bindFb(host,'over',res);\n  }, 900);")

# ── 12) 성적표: 코스별 문서(동의서/수료증) + 이의제기
src = rep(src, "function reviewCard(r){ const st=STEPS.find(s=>s.id===r.id); if(!st) return ''; const rc=st.rects[0]; const cx=rc.l+rc.w/2, cy=rc.t+rc.h/2; const zoom=2.5; const bs=`${zoom*100}% auto`; const px=Math.max(0,Math.min(100,cx)), py=Math.max(0,Math.min(100,cy)); const bp=`${px}% ${py}%`; return `<div class=\"rcard\"><div class=\"crop\" style=\"--bs:${bs};--bp:${bp};background-image:url(${IMG[st.img]})\"></div><div class=\"cap\"><b>${esc(r.task)}</b><span>${r.chance?'찬스 · ':''}${r.wrong?'오답 '+r.wrong+'회 · ':''}정답: ${esc(r.answer)}</span></div></div>`; }",
                 "function reviewCard(r){ const st=STEPS.find(s=>s.id===r.id); if(!st) return ''; const rc=st.rects[0]; const cx=rc.l+rc.w/2, cy=rc.t+rc.h/2; const zoom=2.5; const bs=`${zoom*100}% auto`; const px=Math.max(0,Math.min(100,cx)), py=Math.max(0,Math.min(100,cy)); const bp=`${px}% ${py}%`; return `<div class=\"rcard\"><div class=\"crop\" style=\"--bs:${bs};--bp:${bp};background-image:url(${IMG[st.img]})\"></div><div class=\"cap\"><b>${esc(r.task)}</b><span>${r.chance?'찬스 · ':''}${r.wrong?'오답 '+r.wrong+'회 · ':''}정답: ${esc(r.answer)}</span></div><div class=\"dsp\"><button type=\"button\" data-dsp=\"${st.id}\" title=\"판정이 이상하면 알려주세요\">⚑ 판정 이의</button></div></div>`; }\nfunction bindDisputes(root){ root.querySelectorAll('[data-dsp]').forEach(b=>b.addEventListener('click', ()=>{ const wrap=b.parentElement; if(wrap.querySelector('input')) return; const inp=document.createElement('input'); inp.type='text'; inp.maxLength=120; inp.placeholder='어떤 점이 이상했나요? (선택)'; const ok=document.createElement('button'); ok.type='button'; ok.textContent='보내기'; ok.className='on'; wrap.appendChild(inp); wrap.appendChild(ok); inp.focus(); inp.addEventListener('keydown',e=>{ e.stopPropagation(); if(e.key==='Enter') ok.click(); }); ok.addEventListener('click', async ()=>{ const st=STEPS.find(s=>s.id===b.dataset.dsp); await saveFeedback({ kind:'dispute', ...(S.profile||{name:S.name}), course:st?st.course||S.course:S.course, stage:st?st.st:'', step:b.dataset.dsp, text:(inp.value||'').trim(), at:new Date().toISOString() }); wrap.innerHTML='<span class=\"ok\" style=\"font-family:var(--display);color:#15803d;font-size:12px\">접수됨 ✓ 개선 루프에서 검토합니다</span>'; SFX.pop(); }); })); }")
src = rep(src, "  const c=$('consent'); c.classList.remove('signed','refused'); const stamp=$('bigStamp'); stamp.classList.toggle('gray',!!over); stamp.classList.remove('long');\n  $('cClinic').textContent=S.persona.clinic; $('cPersona').textContent=S.persona.name+' · '+S.persona.short; $('cPlayer').textContent=S.name; $('cDate').textContent=new Date().toLocaleString('ko-KR',{dateStyle:'medium',timeStyle:'short'}); $('cTime').textContent=`${Math.floor(secs/60)}분 ${secs%60}초`;\n  if(over){ c.classList.add('refused'); stamp.textContent='보류'; $('cVerdict').textContent='\"다음에 다시 봅시다.\" (인내심 소진)'; $('cSig').textContent='(서명 없음)'; }\n  else { c.classList.add('signed'); stamp.textContent = (g==='S'||g==='A') ? '동의' : '조건부 동의'; stamp.classList.toggle('long', stamp.textContent.length>3); $('cVerdict').textContent = g==='S'?'\"바로 시작하죠.\"':g==='A'?'\"좋네요, 진행합시다.\"':g==='B'?'\"일단 해보죠.\"':'\"음… 한번 써볼게요.\"'; $('cSig').textContent=S.persona.name.split(' ')[0]; }",
'''  const c=$('consent'); c.classList.remove('signed','refused'); const stamp=$('bigStamp'); stamp.classList.toggle('gray',!!over); stamp.classList.remove('long');
  const biz = S.course==='biz'; const when=new Date().toLocaleString('ko-KR',{dateStyle:'medium',timeStyle:'short'}); const dur=`${Math.floor(secs/60)}분 ${secs%60}초`;
  const verdict = over ? (biz?'미수료 — 원장님 인내심 소진':'"다음에 다시 봅시다." (인내심 소진)') : biz ? (g==='S'?'우수 수료 — 자유자재 시연 가능':g==='A'?'수료 — 현장 시연 투입 가능':g==='B'?'수료 — 약한 단계 복습 권장':'조건부 수료 — 재시연 필요') : (g==='S'?'"바로 시작하죠."':g==='A'?'"좋네요, 진행합시다."':g==='B'?'"일단 해보죠."':'"음… 한번 써볼게요."');
  $('cTitle').textContent = biz ? '웰체크 실무 시연 수료증' : '웰체크 도입 동의서';
  $('cRows').innerHTML = (biz ? [['과정','웰체크 활용 실무 · 일만사 8단계 (Agent·가입·초대등록·포괄평가·교육상담·환자관리·점검평가·건생)'],['시연자',profileLabel(S.profile)||S.name],['시연 상대',S.persona.name+' · '+S.persona.short],['시연 일시',when],['소요시간',dur],['판정',verdict]] : [['의료기관',S.persona.clinic],['원장님 유형',S.persona.name+' · '+S.persona.short],['시연자',S.name],['시연 일시',when],['시연 소요시간',dur],['원장님 판정',verdict]]).map(([k,v])=>`<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join('');
  $('cSigLabel').textContent = biz ? '교육 담당 확인' : '원장 서명';
  if(over){ c.classList.add('refused'); stamp.textContent='보류'; $('cSig').textContent='(서명 없음)'; }
  else { c.classList.add('signed'); stamp.textContent = biz ? ((g==='S'||g==='A') ? '수료' : '조건부 수료') : ((g==='S'||g==='A') ? '동의' : '조건부 동의'); stamp.classList.toggle('long', stamp.textContent.length>3); $('cSig').textContent = biz ? '신사업전략팀' : S.persona.name.split(' ')[0]; }''')
src = rep(src, "  const rows=$('stageRows'); rows.innerHTML = S.queue.map(id=>{ const st=STAGES.find(s=>s.id===id), r=S.stageRes[id]; if(!r) return ''; const sc=r.cleared?Math.max(0,100-W_WRONG*r.wrong-W_CHANCE*r.chance):0; return `<div class=\"srow\"><span>S${st.n} ${st.title}</span>", "  const rows=$('stageRows'); rows.innerHTML = S.queue.map(id=>{ const st=STAGES.find(s=>s.id===id), r=S.stageRes[id]; if(!r) return ''; const sc=r.cleared?Math.max(0,100-W_WRONG*r.wrong-W_CHANCE*r.chance):0; return `<div class=\"srow\"><span>${stageCode(st)} ${st.title}</span>")
src = rep(src, "  $('review').innerHTML=`<h3>복습 카드 ${bad.length}장</h3>`+(bad.length?`<div class=\"rcards\">${bad.map(r=>reviewCard(r)).join('')}</div>`:`<p style=\"color:#1f9d55;font-weight:700;margin:0\">틀린 곳 없음 — 자유자재 수준입니다.</p>`);", "  $('review').innerHTML=`<h3>복습 카드 ${bad.length}장</h3>`+(bad.length?`<div class=\"rcards\">${bad.map(r=>reviewCard(r)).join('')}</div>`:`<p style=\"color:#1f9d55;font-weight:700;margin:0\">틀린 곳 없음 — 자유자재 수준입니다.</p>`); bindDisputes($('review'));")
src = rep(src, "  const run={ ...(S.profile||{name:S.name}), persona:S.persona.key, personaName:S.persona.name, mode:'all', grade:g, score:total, wrong:S.wrong, chance:S.chance, tips:S.tips, secs, at:new Date().toISOString(), over:!!over, weak:bad.map(r=>r.id), stars };", "  const allSteps={}; S.queue.forEach(id=>{ const r=S.stageRes[id]; if(r&&r.steps) Object.assign(allSteps, compactSteps(r.steps)); });\n  const run={ ...(S.profile||{name:S.name}), persona:S.persona.key, personaName:S.persona.name, mode:'all', course:S.course, grade:g, score:total, wrong:S.wrong, chance:S.chance, tips:S.tips, secs, at:new Date().toISOString(), over:!!over, weak:bad.map(r=>r.id), stars, steps:allSteps };")
src = rep(src, "  S.lastText=`[틀린시연찾기 성적표] ${S.name} · ${S.persona.name}(${S.persona.short})\\n등급 ${g} · 점수 ${total} · 오답 ${S.wrong} · 찬스 ${S.chance} · 팁 ${S.tips} · ${fmtTime(secs)}\\n`+S.queue.map(id=>{ const st=STAGES.find(s=>s.id===id), r=S.stageRes[id]; return r?`S${st.n} ${st.title}", "  S.lastText=`[틀린시연찾기 ${COURSES[S.course].name}] ${S.name} · ${S.persona.name}(${S.persona.short})\\n등급 ${g} · 점수 ${total} · 오답 ${S.wrong} · 찬스 ${S.chance} · 팁 ${S.tips} · ${fmtTime(secs)}\\n`+S.queue.map(id=>{ const st=STAGES.find(s=>s.id===id), r=S.stageRes[id]; return r?`${stageCode(st)} ${st.title}")

# ── 13) 현황표: 코스별 별 합계 컬럼, 평가자 평가
src = rep(src, "function starCells(stars, cls){ return STAGES.filter(s=>!s.locked).map(s=>{ const v=stars[s.id]; const n=typeof v==='number'?v:0; return `<span class=\"st s${Math.round(n)} ${cls||''}\" title=\"S${s.n} ${s.title}\">${typeof v==='number' && !Number.isInteger(v) ? v.toFixed(1)+'★' : '★'.repeat(Math.round(n))+'☆'.repeat(3-Math.round(n))}</span>`; }).join(''); }",
                 "function courseStars(stars, course){ const sts=STAGES.filter(s=>!s.locked&&s.course===course); const sum=sts.reduce((a,s)=>a+(stars[s.id]||0),0); return [sum, sts.length*3]; }\nfunction starCells(stars, cls){ return ['biz','zone'].map(c=>{ const [sum,max]=courseStars(stars,c); const r=max?sum/max:0; return `<span class=\"st s${r>=0.99?3:r>=0.6?2:r>0?1:0} ${cls||''}\" title=\"${COURSES[c].long}: ${sum.toFixed(sum%1?1:0)} / ${max}★\">${sum.toFixed(sum%1?1:0)}/${max}★</span>`; }).join(''); }")
src = rep(src, "<span class=\"num hideM\">제안</span>${STAGES.filter(s=>!s.locked).map(s=>`<span class=\"num hideS\">S${s.n}</span>`).join('')}<span class=\"hideS\">활동</span>", "<span class=\"num hideM\">제안</span><span class=\"num hideS\">실무★</span><span class=\"num hideS\">체험존★</span><span class=\"hideS\">활동</span>")
src = rep(src, ".brow{display:grid;grid-template-columns:minmax(150px,1.4fr) 78px 44px 50px 64px repeat(5,34px) 64px minmax(120px,1.2fr) 56px;", ".brow{display:grid;grid-template-columns:minmax(150px,1.4fr) 78px 44px 50px 64px repeat(2,68px) 64px minmax(120px,1.2fr) 56px;")
src = rep(src, "const weak=openStages.filter(s=>(p.stars[s.id]||0)<3).map(s=>'S'+s.n+' '+s.title);", "const weak=openStages.filter(s=>(p.stars[s.id]||0)<3).map(s=>stageCode(s)+' '+s.title);")
src = rep(src, "if(stuck.length) flags.push('🔁 '+stuck.map(s=>'S'+s.n).join('·')+' 반복 실수');", "if(stuck.length) flags.push('🔁 '+stuck.map(s=>stageCode(s)).join('·')+' 반복 실수');")
src = rep(src, "let BOARD = { rows:[], rp:[], rpOn:false, people:[], src:'', admin:false, notes:{} };", "let BOARD = { rows:[], rp:[], rpOn:false, people:[], src:'', admin:false, notes:{}, evals:[], fb:[] };")
src = rep(src, "const [{ rows, src }, rp, notes] = await Promise.all([loadRuns(), loadRP(), loadNotes()]); BOARD.rows=rows; BOARD.src=src; BOARD.rp=rp.rows; BOARD.rpOn=rp.on; BOARD.notes=notes;", "const [{ rows, src }, rp, notes, evals, fb] = await Promise.all([loadRuns(), loadRP(), loadNotes(), loadEvals(), loadFeedback()]); BOARD.rows=rows; BOARD.src=src; BOARD.rp=rp.rows; BOARD.rpOn=rp.on; BOARD.notes=notes; BOARD.evals=evals||[]; BOARD.fb=fb||[];")
src = rep(src, "      <div class=\"pstages\">${STAGES.filter(s=>!s.locked).map(s=>`<div class=\"pstage\"><small>S${s.n} ${esc(s.title)}</small>", "      <div class=\"pstages\">${STAGES.filter(s=>!s.locked).map(s=>`<div class=\"pstage\"><small>${stageCode(s)} ${esc(s.title)}</small>")
# 평가자 평가 블록 (코칭 메모 앞)
src = rep(src, "  <div class=\"memo-box\"><div class=\"pt\">📝 코칭 메모", "  ${evalBox(p)}\n  <div class=\"memo-box\"><div class=\"pt\">📝 코칭 메모")
src = rep(src, "  openModal('personModal'); $('personClose').addEventListener('click',()=>closeModal('personModal'));", "  openModal('personModal'); $('personClose').addEventListener('click',()=>closeModal('personModal'));\n  const es=$('evSave'); if(es) es.addEventListener('click', async()=>{ const ev={ kind:'eval', key:p.key, hq:p.hq, div:p.div, office:p.office, name:p.name, by:S.name||'관리자', at:new Date().toISOString(), text:($('evText').value||'').trim() }; EVAL_AXES.forEach(([k])=>ev[k]=Number($('ev_'+k).value)); ev.avg=Math.round(EVAL_AXES.reduce((a,[k])=>a+ev[k],0)/EVAL_AXES.length*10)/10; es.textContent='저장 중…'; await saveEval(ev); BOARD.evals.unshift(ev); es.textContent='저장됨 ✓'; setTimeout(()=>openPerson(p.key),500); });")
src = rep(src, "function noteFor(key){ return Object.values(BOARD.notes).find(n=>n.key===key); }", "function noteFor(key){ return Object.values(BOARD.notes).find(n=>n.key===key); }\nfunction evalsFor(p){ return (BOARD.evals||[]).filter(e=>e.key===p.key || (e.name===p.name && (!e.office||e.office===p.office))).sort((a,b)=>(b.at||'').localeCompare(a.at||'')); }\nfunction evalBox(p){ const evs=evalsFor(p); const avg=evs.length?Math.round(evs.reduce((a,e)=>a+(e.avg||0),0)/evs.length*10)/10:null; return `<div class=\"memo-box\"><div class=\"pt\">🧑‍⚖️ 평가자 현장 평가 ${avg!==null?`<span class=\"lvbadge\">평균 ${avg} / 5 · ${evs.length}회</span>`:'<span class=\"src\">(아직 없음)</span>'}</div>${BOARD.admin?`<div class=\"evgrid\">${EVAL_AXES.map(([k,l])=>`<div><label for=\"ev_${k}\">${l}</label><select id=\"ev_${k}\">${[5,4,3,2,1].map(v=>`<option value=\"${v}\" ${v===4?'selected':''}>${v}</option>`).join('')}</select></div>`).join('')}</div><textarea id=\"evText\" rows=\"2\" style=\"width:100%;font:inherit;font-size:13px;border:2px solid var(--ink);border-radius:10px;padding:8px;margin-top:6px\" placeholder=\"현장(동행) 시연 코멘트 — 예: 수가 설명은 좋았으나 심평원 등록 화면에서 헤맴\"></textarea><div class=\"btn-row\" style=\"justify-content:flex-start;margin-top:6px\"><button type=\"button\" class=\"g-btn sm blue\" id=\"evSave\">평가 저장</button></div>`:''}<div class=\"evlist\">${evs.slice(0,5).map(e=>`<div><b>${(e.avg||0)}</b> · ${EVAL_AXES.map(([k,l])=>l.slice(0,2)+(e[k]||'-')).join(' ')} · ${esc(e.by||'')} · ${e.at?new Date(e.at).toLocaleDateString('ko-KR'):''}${e.text?' — '+esc(e.text):''}</div>`).join('')}</div></div>`; }")
# CSV: 평가자 평균 컬럼
src = rep(src, "'제안세션','최근','코칭플래그','코칭메모'].join('\\t')];", "'제안세션','평가자평균','최근','코칭플래그','코칭메모'].join('\\t')];")
src = rep(src, "...ax.map(k=>p.rpAxes?p.rpAxes[k][0]:''),p.rp.length,p.lastAt?p.lastAt.slice(0,10):'',p.flags.join(' '),", "...ax.map(k=>p.rpAxes?p.rpAxes[k][0]:''),p.rp.length,(()=>{ const e=evalsFor(p); return e.length?Math.round(e.reduce((a,x)=>a+(x.avg||0),0)/e.length*10)/10:''; })(),p.lastAt?p.lastAt.slice(0,10):'',p.flags.join(' '),")
# 기록실 구분 컬럼에 코스 표기
src = rep(src, "const fmt=r=>`<tr><td>${esc(r.name)}${r.office?' <span class=\"src\">'+esc(r.office)+'</span>':''}</td><td>${esc((r.personaName||'').split(' ')[0])}</td>", "const fmt=r=>`<tr><td>${esc(r.name)}${r.office?' <span class=\"src\">'+esc(r.office)+'</span>':''}</td><td>${esc((r.personaName||'').split(' ')[0])}<span class=\"src\"> ${r.course==='biz'?'실무':'체험존'}</span></td>")
# 담당자 상세 기록 표: 코스 표기
src = rep(src, "<td>시연 ${r.mode==='all'?'전체':'S'+((STAGES.find(s=>s.id===r.stage)||{}).n??'?')}</td>", "<td>${r.course==='biz'?'실무':'체험존'} ${r.mode==='all'?'전체':(()=>{ const st=STAGES.find(s=>s.id===r.stage); return st?stageCode(st):'?'; })()}</td>")

# ── 14) 초기화: 프리로드 제한, 코스 로드
src = rep(src, "Object.values(IMG).forEach(src=>{ const i=new Image(); i.src=src; });", "loadCourse(); ['s01','s02','s03'].forEach(k=>{ const i=new Image(); i.src=IMG[k]; });")
src = rep(src, "window.__DSG = { get S(){ return S; }, STEPS, STAGES, IMG, PERSONAS };", "window.__DSG = { get S(){ return S; }, STEPS, STAGES, IMG, IMGA, PERSONAS, COURSES, setCourse, loadFeedback, loadEvals };")

# ── 14b) 2배 해상도 보드(체험존)로 교체: img/hd/<base>.webp 가 있으면 그 키를 바꿈
hd = sorted(f[:-5] for f in os.listdir(P('img','hd')) if f.endswith('.webp'))
for base in hd:
    key = base.split('_')[0]
    src = re.sub(r"(\b%s:')img/%s\.jpg'" % (key, base), r"\1img/hd/%s.webp'" % base, src, count=1)
hdkeys = [b.split('_')[0] for b in hd if b.startswith('s')]
src = rep(src, "const IMGA = {}; /* 보드 가로세로비 (없으면 체험존 1512/795) */", "const IMGA = {}; /* 보드 가로세로비 (없으면 체험존 1512/795) */\n%s.forEach(k=>IMGA[k]=2562/1350); /* 2배 캡처 보드 */" % json.dumps(hdkeys))
print('hd boards', len(hd))

# ── 15) 개선 루프 화면 + 스크립트
src = rep(src, "<!-- ═════════ 모달: 담당자 상세 ═════════ -->", parts('loop.html') + "\n<!-- ═════════ 모달: 담당자 상세 ═════════ -->")
src = rep(src, '<button type="button" class="g-btn sm gray" id="boardAdmin">관리자</button>', '<button type="button" class="g-btn sm gray" id="boardAdmin">관리자</button>\n        <button type="button" class="g-btn sm orange" id="boardLoop">♻ 개선 루프</button>')
src = rep(src, "\n/* 초기화 */", parts('loop.js') + "\n/* 초기화 */")
# ── 16) 판정 완화: 최소 히트 영역 6%×8% + 여유, 근접 클릭(아깝다!) 1회 무감점
src = rep(src, "function hit(st,x,y){ return st.rects.some(r=>{ const padW=Math.max(0,3.2-r.w)/2+0.5, padH=Math.max(0,4.5-r.h)/2+0.6; return x>=r.l-padW && x<=r.l+r.w+padW && y>=r.t-padH && y<=r.t+r.h+padH; }); }",
          "function hitZone(r,extra){ const e=extra||0; const padW=Math.max(0,6-r.w)/2+1.0+e, padH=Math.max(0,8-r.h)/2+1.2+e*1.4; return { l:r.l-padW, t:r.t-padH, w:r.w+2*padW, h:r.h+2*padH }; }\nfunction hit(st,x,y,extra){ return st.rects.some(r=>{ const z=hitZone(r,extra); return x>=z.l && x<=z.l+z.w && y>=z.t && y<=z.t+z.h; }); }\nfunction nearMiss(st,x,y){ S.nearUsed=true; SFX.tip(); if(S.cur && S.cur.miss.length<6) S.cur.miss.push([Math.round(x),Math.round(y)]); const m=document.createElement('div'); m.className='mark near'; m.style.left=x+'%'; m.style.top=y+'%'; m.textContent='?'; $('fx').appendChild(m); setTimeout(()=>m.remove(),1400); word('아깝다!','chance'); setTimeout(()=>subline('바로 옆이에요 — 조금만 더 정확히'),150); try{ if(navigator.vibrate) navigator.vibrate(20); }catch(e){} }")
src = rep(src, "if(x<0||x>100||y<0||y>100) return; if(hit(st,x,y)) correct(st); else wrong(st,x,y); }", "if(x<0||x>100||y<0||y>100) return; if(hit(st,x,y)) correct(st); else if(!S.nearUsed && hit(st,x,y,4)) nearMiss(st,x,y); else wrong(st,x,y); }")
src = rep(src, "S.stepWrong=0; S.stepChance=false; S.locked=false; S.busy=false; S.cur=", "S.stepWrong=0; S.stepChance=false; S.locked=false; S.busy=false; S.nearUsed=false; S.cur=")
src = rep(src, ".mark.x.fade{animation:fadeout .6s 1.2s forwards}", ".mark.x.fade{animation:fadeout .6s 1.2s forwards}\n.mark.near{width:5%;aspect-ratio:1;border-radius:50%;background:#ffd93b;border:3px solid var(--ink);color:var(--ink);font-family:var(--impact);font-size:clamp(16px,2.6vw,34px);display:flex;align-items:center;justify-content:center;animation:stamp .3s cubic-bezier(.2,1.8,.4,1),fadeout .5s .9s forwards;box-shadow:0 3px 0 var(--ink)}")
exec(open(P('build_v8.py'), encoding='utf-8').read())
exec(open(P('build_v9.py'), encoding='utf-8').read())
exec(open(P('build_v10.py'), encoding='utf-8').read())
exec(open(P('build_v11.py'), encoding='utf-8').read())
exec(open(P('build_v12.py'), encoding='utf-8').read())
exec(open(P('build_v13.py'), encoding='utf-8').read())
exec(open(P('build_v14.py'), encoding='utf-8').read())
exec(open(P('build_v15.py'), encoding='utf-8').read())
exec(open(P('build_v16.py'), encoding='utf-8').read())
exec(open(P('build_v17.py'), encoding='utf-8').read())
exec(open(P('build_v18.py'), encoding='utf-8').read())
exec(open(P('build_v19.py'), encoding='utf-8').read())
exec(open(P('build_v20.py'), encoding='utf-8').read())
exec(open(P('build_v21.py'), encoding='utf-8').read())
exec(open(P('build_v22.py'), encoding='utf-8').read())
exec(open(P('build_v23.py'), encoding='utf-8').read())
exec(open(P('build_v24.py'), encoding='utf-8').read())
exec(open(P('build_v25.py'), encoding='utf-8').read())
exec(open(P('build_v26.py'), encoding='utf-8').read())
exec(open(P('build_v27.py'), encoding='utf-8').read())
exec(open(P('build_v28.py'), encoding='utf-8').read())
exec(open(P('build_v29.py'), encoding='utf-8').read())
# v30(🎙 멘트 말하기)는 루피(알피왕)와 역할 중복 → 제외 (2026-10-21 키아누)
exec(open(P('build_v31.py'), encoding='utf-8').read())
exec(open(P('build_v32.py'), encoding='utf-8').read())
open(P('demo-spotter.html'), 'w', encoding='utf-8').write(src)
print('built', len(src), 'bytes')

# ── 콘텐츠 린트: 오류가 있으면 빌드 실패
import subprocess, sys
r = subprocess.run(['node', P('lint.js')], capture_output=True, text=True)
print(r.stdout.strip())
if r.returncode != 0:
    print(r.stderr.strip()); print('✖ 린트 실패 — 빌드 산출물은 생성됐지만 오류를 고쳐야 합니다'); sys.exit(1)

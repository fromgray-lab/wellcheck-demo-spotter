
/* ═══════════════════════════════════════════ v26(v33): 🧮 수가 계산기 · 🔢 숫자 특훈 · ⏱ 10분 페이스 · 📖 응대 카드북 ═══════════════════════════════════════════ */

/* ── 1) 🧮 수가 계산기: 원장님이 "그래서 얼마냐"를 자기 숫자로 물을 때 — 26년 체험존 수가표 기준, 재진진찰료·검사료 별도 ── */
const FEES={ ax001:35810, ax002:28090, ax003:28090, ax004:15650, ax005:13920, ib023:11130, ib024:11910, ib025:13100 };
const FEE_NOTE='26년 체험존 수가표 기준. 저위험군 11,130원은 26년 환산 시 11,310원으로 추정(고시 재확인 전) — 환자관리료는 "회당 1.1만~1.3만원"으로 말하기.';
const CALC_DEF={ n:300, cycle:1, edu:10, eduBy:'ax004', mg:12, mgFee:FEES.ib024, chk:2 };
function calcState(){ try{ return Object.assign({}, CALC_DEF, JSON.parse(localStorage.getItem('dsg_calc')||'{}')); }catch(e){ return Object.assign({}, CALC_DEF); } }
function calcSave(c){ try{ localStorage.setItem('dsg_calc', JSON.stringify(c)); }catch(e){} }
function fmtWon(n){ n=Math.round(n); if(n>=1e8){ const ok=Math.floor(n/1e8), man=Math.round((n%1e8)/1e4); return man?`${ok}억 ${man.toLocaleString()}만원`:`${ok}억원`; } if(n>=1e4) return `${(n/1e4).toLocaleString(undefined,{maximumFractionDigits:n>=1e6?0:1})}만원`; return `${n.toLocaleString()}원`; }
function calcCompute(c){ const first=c.cycle==1?FEES.ax001:FEES.ax002; const rows=[ { name:'포괄평가·계획수립', code:c.cycle==1?'AX001 초회':'AX002 2주기~', fee:first, n:1 }, { name:'점검·평가', code:'AX003', fee:FEES.ax003, n:+c.chk }, { name:'교육상담', code:c.eduBy==='ax004'?'AX004 의사':'AX005 코디', fee:FEES[c.eduBy]||FEES.ax004, n:+c.edu }, { name:'환자관리료(비대면)', code:'IB023~025', fee:+c.mgFee||0, n:+c.mg } ];
  rows.forEach(r=>{ r.sum=r.fee*r.n; r.total=r.sum*c.n; }); const per=rows.reduce((a,r)=>a+r.sum,0); return { rows, per, total:per*c.n, monthly:per*c.n/12 }; }
function calcText(c, r){ const mgName=c.mgFee==FEES.ib023?'저위험군':c.mgFee==FEES.ib024?'중위험군':c.mgFee==FEES.ib025?'고위험군':'회당 '+(+c.mgFee).toLocaleString()+'원';
  return `[일만사 수가 계산 · 26년 기준] 환자 ${c.n}명 · ${c.cycle==1?'1주기':'2주기~'} · 교육상담 ${c.edu}회(${c.eduBy==='ax004'?'의사':'코디'}) · 환자관리 ${c.mg}회(${mgName}) · 점검평가 ${c.chk}회\n연 합계 약 ${fmtWon(r.total)} (환자당 ${fmtWon(r.per)} · 월 평균 ${fmtWon(r.monthly)})\n`+r.rows.map(x=>`- ${x.name} ${x.code} ${x.fee.toLocaleString()}원×${x.n}회 = ${x.sum.toLocaleString()}원/인 → ${fmtWon(x.total)}`).join('\n')+`\n※ 재진진찰료·검사료는 별도(기존 그대로). 환자 본인부담 30%→20%. 교육·관리 횟수를 다 채웠을 때 기준, 참고용.`; }
function openCalc(){ const host=$('overlayHost2')||(()=>{ const d=document.createElement('div'); d.id='overlayHost2'; document.body.appendChild(d); return d; })(); let c=calcState();
  const seg=(name, opts, cur)=>`<div class="cseg" data-k="${name}">${opts.map(([v,l])=>`<button type="button" class="${String(v)===String(cur)?'on':''}" data-v="${v}">${l}</button>`).join('')}</div>`;
  host.innerHTML=`<div class="modal on" id="calcModal"><div class="g-panel calc" style="width:min(760px,100%)"><h2 class="g">🧮 일만사 수가 계산기 <small class="src">26년 · 재진진찰료·검사료 별도</small></h2>
    <div class="cgrid"><div class="cin">
      <label>일만사 등록 환자 수 <output id="cN">${c.n}</output>명</label><input type="range" id="cNr" min="10" max="500" step="10" value="${c.n}"><div class="cpre">${[30,50,100,200,300].map(v=>`<button type="button" data-n="${v}">${v}명</button>`).join('')}</div>
      <label>주기</label>${seg('cycle',[[1,'1주기(초회)'],[2,'2주기부터']],c.cycle)}
      <label>교육상담 <output id="cEdu">${c.edu}</output>회 / 주기당 최대 10회</label><input type="range" id="cEduR" min="0" max="10" value="${c.edu}">${seg('eduBy',[['ax004','의사 15,650'],['ax005','코디 13,920']],c.eduBy)}
      <label>환자관리(비대면) <output id="cMg">${c.mg}</output>회 / 연 최대 12회</label><input type="range" id="cMgR" min="0" max="12" value="${c.mg}">${seg('mgFee',[[FEES.ib023,'저 11,130'],[FEES.ib024,'중 11,910'],[FEES.ib025,'고 13,100']],c.mgFee)}
      <label>점검·평가 <output id="cChk">${c.chk}</output>회 / 주기당 최대 2회</label><input type="range" id="cChkR" min="0" max="2" value="${c.chk}">
    </div><div class="cout"><div class="cbig"><small>연 합계(일만사 수가만)</small><b id="cTotal"></b></div><div class="ctwo"><div><small>환자당 연</small><b id="cPer"></b></div><div><small>월 평균</small><b id="cMon"></b></div></div><table class="ctable" id="cTable"></table><p class="src" id="cNote">${esc(FEE_NOTE)}</p></div></div>
    <div class="btn-row"><button type="button" class="g-btn green" id="cCopy">📋 계산 복사</button><button type="button" class="g-btn" id="cReset">체험존 기본값(300명)</button><button type="button" class="g-btn gray" id="cClose">닫기</button></div></div></div>`;
  const render=()=>{ const r=calcCompute(c); $('cTotal').textContent=fmtWon(r.total); $('cPer').textContent=fmtWon(r.per); $('cMon').textContent=fmtWon(r.monthly); $('cTable').innerHTML=`<tr><th>항목</th><th>단가×횟수</th><th>환자당</th><th>합계</th></tr>`+r.rows.map(x=>`<tr><td>${esc(x.name)}<br><small>${esc(x.code)}</small></td><td>${x.fee.toLocaleString()}×${x.n}</td><td>${x.sum.toLocaleString()}</td><td><b>${fmtWon(x.total)}</b></td></tr>`).join(''); $('cN').textContent=c.n; $('cEdu').textContent=c.edu; $('cMg').textContent=c.mg; $('cChk').textContent=c.chk; host.querySelectorAll('.cseg').forEach(sg=>{ sg.querySelectorAll('button').forEach(b=>b.classList.toggle('on', String(b.dataset.v)===String(c[sg.dataset.k]))); }); calcSave(c); };
  if(c.n>500) c.n=500; host.querySelectorAll('.cpre button').forEach(b=>b.addEventListener('click', ()=>{ c.n=+b.dataset.n; $('cNr').value=c.n; SFX.pop(); render(); })); const on=(id,k)=>$(id).addEventListener('input', e=>{ c[k]=+e.target.value; render(); }); on('cNr','n'); on('cEduR','edu'); on('cMgR','mg'); on('cChkR','chk');
  host.querySelectorAll('.cseg button').forEach(b=>b.addEventListener('click', ()=>{ const k=b.closest('.cseg').dataset.k; c[k]=k==='eduBy'?b.dataset.v:+b.dataset.v; SFX.pop(); render(); }));
  $('cReset').addEventListener('click', ()=>{ c=Object.assign({}, CALC_DEF); ['cNr','cEduR','cMgR','cChkR'].forEach((id,i)=>{ $(id).value=[c.n,c.edu,c.mg,c.chk][i]; }); SFX.pop(); render(); });
  $('cCopy').addEventListener('click', async ()=>{ const t=calcText(c, calcCompute(c)); try{ await navigator.clipboard.writeText(t); $('cCopy').textContent='복사됨 ✓'; }catch(e){ $('cCopy').textContent='복사 실패'; } setTimeout(()=>$('cCopy').textContent='📋 계산 복사',1800); });
  $('cClose').addEventListener('click', ()=>{ host.innerHTML=''; }); $('calcModal').addEventListener('click', e=>{ if(e.target.id==='calcModal') host.innerHTML=''; }); render(); SFX.pop(); }

/* ── 2) 🔢 숫자 특훈: 원장님이 현장에서 바로 검산할 수 있는 숫자만 10문제 (수가·횟수·기한·포인트·제도 날짜) ── */
const NUMS=[
  { c:'all', q:'포괄평가·계획수립(AX001) 초회 수가는?', a:'35,810원', d:['28,090원','15,650원','53,810원'], src:'체험존 수가표(26년)' },
  { c:'all', q:'2주기부터 포괄평가·계획수립(AX002) 수가는?', a:'28,090원', d:['35,810원','13,920원','20,890원'], src:'체험존 수가표(26년)' },
  { c:'all', q:'점검·평가(AX003)는 주기당 몇 회까지?', a:'2회', d:['1회','4회','12회'], src:'매뉴얼 p.64' },
  { c:'all', q:'교육상담은 주기당 최대 몇 회?', a:'10회', d:['6회','12회','24회'], src:'매뉴얼 p.47' },
  { c:'all', q:'환자관리료(비대면)는 연 몇 회까지?', a:'12회', d:['6회','10회','24회'], src:'체험존 수가표(26년)' },
  { c:'all', q:'의사 교육상담(AX004) 회당 수가는?', a:'15,650원', d:['13,920원','11,130원','28,090원'], src:'체험존 수가표(26년)' },
  { c:'all', q:'의사 교육상담은 최소 몇 분 이상?', a:'10분', d:['5분','15분','20분'], src:'매뉴얼 p.47' },
  { c:'all', q:'케어코디네이터(간호사·영양사) 교육상담은 최소 몇 분?', a:'20분', d:['10분','15분','30분'], src:'매뉴얼 p.47' },
  { c:'all', q:'일만사 참여 환자의 본인부담(재진진찰료·검사료) 경감은?', a:'30% → 20%', d:['30% → 10%','20% → 10%','30% → 0%'], src:'매뉴얼 p.81' },
  { c:'all', q:'건강생활실천지원금은 연 최대 몇 포인트?', a:'8만p', d:['5만p','10만p','12만p'], src:'체험존 건생 팝업' },
  { c:'all', q:'건생 참여 신청·케어플랜 수립 포인트는 각각?', a:'5,000p', d:['3,000p','10,000p','20,000p'], src:'체험존 건생 팝업' },
  { c:'all', q:'건생 걸음·자가측정·교육 포인트 한도는 각각 연?', a:'2만p', d:['1만p','3만p','5만p'], src:'체험존 건생 팝업' },
  { c:'all', q:'초기 적립 1만p를 받으려면 케어플랜 수립 후 몇 개월 내 신청?', a:'3개월', d:['1개월','6개월','12개월'], src:'체험존 건생 팝업' },
  { c:'all', q:'건생 포인트를 병원 수납 때 즉시 차감하는 제도는 언제부터?', a:'2025년 12월 15일', d:['2025년 10월 1일','2025년 12월 31일','2026년 1월 1일'], src:'복지부·공단 발표' },
  { c:'all', q:'첫 청구(AX001)에 필요한 임상검사는 계획수립일 기준 몇 개월 이내?', a:'6개월', d:['3개월','12개월','1개월'], src:'매뉴얼 p.38' },
  { c:'all', q:'1차 점검/평가는 케어플랜 수립 후 몇 개월?', a:'4개월', d:['2개월','3개월','6개월'], src:'매뉴얼 p.64' },
  { c:'all', q:'2차 점검/평가는 1차 점검/평가 후 몇 개월?', a:'1개월', d:['2개월','3개월','4개월'], src:'매뉴얼 p.64' },
  { c:'all', q:'환자관리 내역은 얼마나 자주 전송?', a:'월 1회', d:['주 1회','월 2회','분기 1회'], src:'매뉴얼 p.54' },
  { c:'all', q:'건생 관리 포인트는 조건 달성 후 약 며칠 뒤 지급?', a:'1~3일', d:['당일','7일','익월 15일'], src:'매뉴얼 p.81' },
  { c:'all', q:'건생 대리 신청에 병원이 보관할 필수 서류는 몇 종?', a:'3종', d:['1종','2종','5종'], src:'매뉴얼 p.81' },
  { c:'biz', q:'심평원 Agent 통신 포트 번호는?', a:'1707', d:['1701','8080','7071'], src:'매뉴얼 p.8' },
  { c:'biz', q:'초대장 엑셀 일괄 발송은 1회 최대 몇 명?', a:'500명', d:['100명','300명','1,000명'], src:'매뉴얼 p.25' },
  { c:'biz', q:'환자관리 자동 메시지는 매주 언제 발송?', a:'금요일 오전 9시경', d:['월요일 오전 9시경','금요일 오후 6시경','매일 오전 9시경'], src:'매뉴얼 p.57' },
  { c:'zone', q:'경감시작일을 넣으면 경감종료일은 며칠 뒤로 자동 계산?', a:'364일', d:['180일','365일','730일'], src:'체험존 대상자 등록 화면' },
  { c:'zone', q:'체험존 시뮬레이션: 환자 300명이면 일만사 수가 연 약?', a:'1.17억원', d:['5,600만원','1.7억원','2.3억원'], src:'체험존 수익 시뮬레이션' },
  { c:'zone', q:'환자 1명 연 12회 내원 시 일만사 X vs O(재진진찰료 포함) 금액은?', a:'18.8만원 vs 56.6만원', d:['18.8만원 vs 38.9만원','12만원 vs 56.6만원','18.8만원 vs 116만원'], src:'체험존 수익 시뮬레이션' },
  { c:'zone', q:'환자 혜택 화면의 임상 연구는 시범사업 참여 환자 몇 명 추적?', a:'901명', d:['300명','1,000명','5,000명'], src:'체험존 환자 혜택 화면(복지부)' },
  { c:'zone', q:'참여군은 비참여군보다 HbA1c가 얼마나 낮았나?', a:'0.38%p', d:['0.83%p','1.2%p','0.1%p'], src:'체험존 환자 혜택 화면(복지부)' },
  { c:'zone', q:'참여군은 비참여군보다 수축기 혈압이 얼마나 낮았나?', a:'3.4mmHg', d:['1.4mmHg','8.4mmHg','12mmHg'], src:'체험존 환자 혜택 화면(복지부)' },
  { c:'zone', q:'체험존 기준 환자부담금 연 평균 경감액은?', a:'23,500원', d:['12,500원','40,000원','56,200원'], src:'체험존 환자 혜택 화면' },
  { c:'zone', q:'건생 신청은 케어플랜 수립일부터 몇 개월 이내 가능?(체험존 팝업 기준)', a:'12개월', d:['3개월','6개월','24개월'], src:'체험존 건생 팝업' }
];
function numPool(){ return NUMS.filter(x=>x.c==='all'||x.c===S.course); }
function numBest(){ const me=(S.profile&&S.profile.name)||S.name||''; return localRuns().filter(r=>(r.name||'')===me&&r.mode==='numdrill'&&r.course===S.course).reduce((a,r)=>Math.max(a,r.score||0),-1); }
function startNumDrill(){ const pool=numPool(); if(pool.length<4){ toast('숫자 문제가 부족해요'); return; } const picked=pool.slice().sort(()=>Math.random()-0.5).slice(0,10); const log=[]; let i=0; const t0=Date.now();
  const host=$('overlayHost2')||(()=>{ const d=document.createElement('div'); d.id='overlayHost2'; document.body.appendChild(d); return d; })();
  const finish=()=>{ const ok=log.filter(x=>x.ok).length; const score=Math.round(ok/log.length*100); const g=score>=100?'S':score>=90?'A':score>=70?'B':score>=50?'C':'D'; const secs=Math.round((Date.now()-t0)/1000); const wrongs=log.filter(x=>!x.ok); delete host._ndPick;
    saveRun({ ...(S.profile||{name:S.name}), persona:S.persona?S.persona.key:'', mode:'numdrill', course:S.course, stage:'numdrill', diff:S.diff, grade:g, score, wrong:wrongs.length, chance:0, tips:0, secs, at:new Date().toISOString(), over:false, stars:{}, steps:{}, nq:{ total:log.length, ok, wrong:wrongs.map(x=>x.q) } }).then(w=>saveStatus(w)); SFX.clear();
    const card={ title:'🔢 숫자 특훈', sub:`${COURSES[S.course].name} · 수가·횟수·기한·포인트`, g, name:(S.profile&&S.profile.name)||S.name||'', line:`${ok}/${log.length} 정답 · ${fmtTime(secs)}`, stats:[['정답률',score+'%'],['맞힘',ok],['틀림',wrongs.length],['시간',fmtTime(secs)]], msg:score>=90?'원장님이 검산해도 끄떡없음':score>=70?'핵심 숫자는 잡혔어요':'수가표부터 다시 한 번', fn:'틀린시연찾기_숫자특훈.png', c1:'#bfe3ff', c2:'#2b9bff' };
    host.innerHTML=`<div class="modal on" id="ndModal"><div class="g-panel" style="width:min(640px,100%)"><div class="banner ${ok===log.length?'':'blue'}">숫자 특훈 ${ok}/${log.length}</div><div class="tally"><div><small>정답률</small><b>${score}%</b></div><div><small>등급</small><b>${g}</b></div><div><small>시간</small><b>${fmtTime(secs)}</b></div></div>${wrongs.length?`<div class="qrlist" style="max-height:40vh;overflow:auto;text-align:left">${wrongs.map(x=>`<div class="qr"><div class="qrq">${esc(x.q)}</div><div class="qrmine">내 답: ${esc(x.pick)}</div><div class="qrok">정답: ${esc(x.a)} <span class="src">(${esc(x.src)})</span></div></div>`).join('')}</div>`:`<p style="color:#1f9d55;font-weight:700">숫자가 입에 붙었습니다 — 원장님이 검산해도 끄떡없음.</p>`}<div class="btn-row"><button type="button" class="g-btn green" id="ndAgain">🔢 한 번 더</button>${cardBtnHtml()}<button type="button" class="g-btn" id="ndCalc">🧮 계산기</button><button type="button" class="g-btn gray" id="ndClose">닫기</button></div></div></div>`;
    bindCardBtn(host, card); $('ndClose').addEventListener('click', ()=>{ host.innerHTML=''; renderNumChip(true); }); $('ndAgain').addEventListener('click', ()=>{ host.innerHTML=''; startNumDrill(); }); $('ndCalc').addEventListener('click', ()=>{ host.innerHTML=''; openCalc(); }); };
  const ask=()=>{ const x=picked[i]; const opts=[x.a].concat(x.d).map((t,k)=>({ t, ok:k===0 })).sort(()=>Math.random()-0.5); const tq=Date.now(); let answered=false;
    host.innerHTML=`<div class="modal on" id="ndModal"><div class="g-panel qcard" style="position:relative"><button type="button" class="g-btn sm gray qdquit" id="ndQuit" title="그만하기">✕</button><div class="eyebrow">🔢 숫자 특훈 ${i+1}/${picked.length} · ${esc(COURSES[S.course].name)}</div><div class="qq">${esc(x.q)}</div><div class="qsub">정확한 숫자를 고르세요 (1·2·3·4)</div><div class="qopts">${opts.map((o,k)=>`<button type="button" class="qopt" data-i="${k}"><b>${k+1}</b><span>${esc(o.t)}</span></button>`).join('')}</div><div class="qwhy" id="ndWhy" hidden></div><div class="btn-row" id="ndRow" hidden><button type="button" class="g-btn green" id="ndNext">${i<picked.length-1?'다음 ▶':'결과 보기'}</button></div></div></div>`;
    const btns=[...host.querySelectorAll('.qopt')]; const okPos=opts.findIndex(o=>o.ok);
    const pick=(k)=>{ if(answered) return; answered=true; const ok=k===okPos; log.push({ q:x.q, a:x.a, src:x.src, ok, pick:opts[k].t, secs:Math.round((Date.now()-tq)/1000) }); btns.forEach((b,j)=>{ b.disabled=true; if(j===okPos) b.classList.add('ok'); else if(j===k) b.classList.add('bad'); }); if(ok) SFX.good(); else SFX.wrong(); const w=$('ndWhy'); w.innerHTML=`<div class="ql">${ok?'✅ 정확':'❌ 다시 외우기'}</div><div><b>${esc(x.a)}</b> <span class="qp">(${esc(x.src)})</span></div>`; w.hidden=false; $('ndRow').hidden=false; try{ $('ndNext').focus({preventScroll:true}); }catch(e){} };
    btns.forEach(b=>b.addEventListener('click', ()=>pick(+b.dataset.i))); host.dataset.ndkeys='1'; host._ndPick=pick;
    $('ndNext').addEventListener('click', ()=>{ i++; if(i<picked.length) ask(); else finish(); }); $('ndQuit').addEventListener('click', ()=>{ host.innerHTML=''; delete host._ndPick; }); };
  SFX.pop(); ask(); }
document.addEventListener('keydown', e=>{ const host=$('overlayHost2'); if(!host||!host._ndPick||!host.querySelector('#ndModal')) return; if(e.key>='1'&&e.key<='4'){ host._ndPick(+e.key-1); e.preventDefault(); } else if(e.key==='Enter'){ const n=$('ndNext'); if(n&&!$('ndRow').hidden){ n.click(); e.preventDefault(); } } });
function renderNumChip(replace){ const el=$('todo'); if(!el) return; const old=el.querySelector('.tchip.numdrill'); if(old){ if(!replace) return; old.remove(); } const n=numPool().length; const best=numBest(); const chip=document.createElement('button'); chip.type='button'; chip.className='tchip numdrill'+(best>=90?' done':''); chip.innerHTML=`<b>🔢</b> 숫자 특훈 <small>수가·횟수·기한 10문제 · 풀 ${n}${best>=0?` · 내 최고 ${best}%`:''}</small>`; chip.title='원장님이 현장에서 바로 검산할 수 있는 숫자만 — 수가·횟수·기한·포인트·제도 날짜'; chip.addEventListener('click', ()=>{ SFX.go(); startNumDrill(); });
  const q=el.querySelector('.tchip.wrongq')||el.querySelector('.tchip.qdrill'); if(q) q.after(chip); else el.prepend(chip); }

/* ── 3) ⏱ 10분 페이스: 체험존 전체 시연은 "10분 안에 보여드리겠습니다"(o1) — 진행 속도로 예상 완료 시간을 HUD에 ── */
const PACE_TARGET={ zone:600 };
function paceInfo(){ if(S.mode!=='all'||!PACE_TARGET[S.course]) return null; const br=S.persona?(S.persona.branch||S.persona.key):''; const total=(S.queue||[]).reduce((a,id)=>a+STEPS.filter(s=>s.st===id&&(!s.branch||s.branch===br)).length,0); const done=(S.results||[]).length; const el=(Date.now()-S.start)/1000; const target=PACE_TARGET[S.course]; const est=done>=3?el/done*total:null; return { total, done, el, target, est }; }
function paceTick(){ const p=paceInfo(); let chip=$('pace'); if(!p){ if(chip) chip.hidden=true; return; } if(!chip){ chip=document.createElement('span'); chip.className='chip pace'; chip.id='pace'; const t=$('timer'); if(t) t.after(chip); else return; } chip.hidden=false;
  if(p.est==null){ chip.textContent=`⏱ 목표 ${fmtTime(p.target)}`; chip.className='chip pace'; return; } const over=p.est>p.target; chip.textContent=`${over?'🐢':'🐇'} 예상 ${fmtTime(Math.round(p.est))} / ${fmtTime(p.target)}`; chip.className='chip pace'+(over?' slow':' ok'); chip.title=`${p.done}/${p.total} 스텝 · 지금 속도면 ${over?'목표 초과':'목표 안'}`; }
function paceResult(secs){ const p=paceInfo(); const box=$('review'); if(!p||!box) return; const old=box.querySelector('.paceline'); if(old) old.remove(); const ok=secs<=p.target; const d=document.createElement('div'); d.className='paceline '+(ok?'ok':'slow'); d.innerHTML=`<b>⏱ 시연 시간 ${fmtTime(secs)}</b> — 원장님께 약속한 "10분 안에" ${ok?'✅ 지켰습니다':`❌ ${fmtTime(secs-p.target)} 초과`}${ok?'':' · 팁은 플레이 전에 읽고, 화면 전환은 말하면서'}`; box.prepend(d); }

/* ── 4) 📖 응대 카드북: 질문 카드 전부(오답 보기까지) A4 인쇄용 — 암기용 ── */
function cardbookHtml(course){ const e=esc; const cards=QCARDS.filter(q=>q.course===course); const sts=STAGES.filter(s=>s.course===course&&!s.locked&&!s.bonus);
  const body=sts.map(st=>{ const qs=cards.filter(q=>q.st===st.id); if(!qs.length) return ''; return `<section><h2><span class="code">${e(stageCode(st))}</span> ${e(st.title)} <small>${qs.length}장</small></h2>${qs.map((q,i)=>`<div class="card"><div class="q"><b>Q${i+1}.</b> “${e(q.q)}” <span class="lv">${q.lv==='adv'?'심화':'기초'}</span></div><ol>${q.opts.map((o,k)=>`<li class="${k===q.ans?'ok':'no'}">${k===q.ans?'✅':'✗'} ${e(o)}</li>`).join('')}</ol><div class="why">${e(q.why||'')}${q.page?` <span class="pg">(매뉴얼 ${e(q.page)})</span>`:''}</div></div>`).join('')}</section>`; }).join('');
  const nums=NUMS.filter(x=>x.c==='all'||x.c===course);
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>원장님 질문 응대 카드북 · ${e(COURSES[course].long)}</title><style>
  @page{size:A4;margin:14mm} body{font-family:'Noto Sans KR','Apple SD Gothic Neo','Malgun Gothic',sans-serif;color:#1d2140;line-height:1.45;max-width:860px;margin:24px auto;padding:0 16px;font-size:13px}
  h1{font-size:22px;margin:0 0 4px} .meta{color:#5b6383;font-size:12px;margin-bottom:16px} section{margin-bottom:18px} h2{font-size:16px;margin:0 0 8px;display:flex;align-items:center;gap:8px;border-bottom:2px solid #1d2140;padding-bottom:4px} h2 small{color:#5b6383;font-weight:400;font-size:12px} .code{background:#1d2140;color:#ffd93b;border-radius:8px;padding:1px 8px;font-size:12px}
  .card{break-inside:avoid;border:1.5px solid #1d2140;border-radius:10px;padding:8px 12px;margin-bottom:8px} .q{font-weight:700;font-size:14px} .lv{font-size:10px;color:#fff;background:#8b5cf6;border-radius:6px;padding:0 6px;margin-left:6px;vertical-align:middle} ol{margin:4px 0;padding-left:0;list-style:none} li{margin:2px 0;padding-left:4px} li.ok{color:#1f9d55;font-weight:700} li.no{color:#8a8fa8} .why{color:#5b6383;font-size:12px;border-top:1px dashed #b8bccc;margin-top:4px;padding-top:4px} .pg{color:#2b9bff}
  table{border-collapse:collapse;width:100%;font-size:12px} th,td{border:1px solid #b8bccc;padding:3px 6px;text-align:left} th{background:#f1f3f9}
  .print{position:fixed;right:16px;top:12px;padding:8px 14px;border:2px solid #1d2140;border-radius:10px;background:#ffd93b;font-weight:700;cursor:pointer} @media print{.print{display:none}}
  </sty`+`le></head><body><button class="print" onclick="window.print()">🖨 인쇄 / PDF 저장</button><h1>원장님 질문 응대 카드북 · ${e(COURSES[course].long)}</h1><div class="meta">틀린시연찾기 · 신사업전략팀 · ${e(new Date().toLocaleDateString('ko-KR'))} · 질문 카드 ${cards.length}장 + 핵심 숫자 ${nums.length}개 · ✅ 모범 답, ✗ 오답(왜 오답인지는 해설)</div>${body}<section><h2><span class="code">#</span> 핵심 숫자 <small>원장님이 바로 검산하는 것들</small></h2><table><tr><th>질문</th><th>답</th><th>근거</th></tr>${nums.map(x=>`<tr><td>${e(x.q)}</td><td><b>${e(x.a)}</b></td><td>${e(x.src)}</td></tr>`).join('')}</table><p class="why">${e(FEE_NOTE)}</p></section></body></html>`; }
async function saveCardbook(btn){ const course=S.course; const html=cardbookHtml(course); const fn=`웰체크_응대카드북_${COURSES[course].name.replace(/\(.*?\)|\s/g,'')}.html`; const dl=await getDownloads(); const orig=btn?btn.innerHTML:''; if(btn) btn.disabled=true; const done=(t)=>{ if(!btn) return; btn.textContent=t; setTimeout(()=>{ btn.innerHTML=orig; btn.disabled=false; },1800); };
  try{ if(dl){ await dl.save({ filename:fn, data:new Blob([html],{type:'text/html'}) }); done('저장됨 ✓'); } else if(!window.claude){ const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([html],{type:'text/html'})); a.download=fn; document.body.appendChild(a); a.click(); setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); },1500); done('저장됨 ✓'); } else done('저장 불가'); }catch(e){ done(e&&e.code==='declined'?'취소됨':'저장 실패'); } }

/* ── 5) 미션 화면 🧰 도구 줄 ── */
function renderTools(){ const el=$('todo'); if(!el||el.querySelector('.trow.tools')) return; const r=document.createElement('div'); r.className='trow tools'; r.innerHTML=`<span class="tl">🧰 도구</span><button type="button" class="tchip calc" title="원장님 숫자로 연 수가 계산 — 복사해서 카톡으로"><b>🧮</b> 수가 계산기 <small>환자 수·횟수·위험군</small></button><button type="button" class="tchip book" title="질문 카드 전부 + 핵심 숫자 — A4 인쇄용"><b>📖</b> 응대 카드북 <small>인쇄용</small></button>`; el.appendChild(r); r.querySelector('.calc').addEventListener('click', openCalc); const b=r.querySelector('.book'); b.addEventListener('click', ()=>saveCardbook(b)); getDownloads().then(dl=>{ if(!dl&&window.claude) b.hidden=true; }); }

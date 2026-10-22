
/* ═══════════════════════════════════════════ 관리자 정답 지도 + 오클릭 히트맵 (마스터키) ═══════════════════════════════════════════ */
const BM = { course:'biz', stage:'', runs:[], src:'', fb:[] };
function bmAggregate(){ const agg={}; BM.runs.forEach(r=>{ Object.entries(r.steps||{}).forEach(([id,a])=>{ const o=agg[id]=agg[id]||{ n:0, wrong:0, chance:0, to:0, secs:0, miss:[] }; o.n++; if(a[0]>0) o.wrong++; if(a[1]) o.chance++; if(a[4]) o.to++; o.secs+=a[3]||0; (a[5]||[]).forEach(p=>{ if(o.miss.length<400) o.miss.push(p); }); }); }); return agg; }
function bmRender(){ const host=$('bmBody'); if(!host) return; const agg=bmAggregate(); const disputes={}; BM.fb.filter(f=>f.kind==='dispute').forEach(f=>{ disputes[f.step]=(disputes[f.step]||0)+1; });
  const steps=STEPS.filter(s=>s.st===BM.stage && !s.branch); const showMiss=$('bmMiss').checked; const showZone=$('bmZone').checked;
  host.innerHTML = steps.map((st,i)=>{ const a=agg[st.id]||{n:0,wrong:0,chance:0,to:0,secs:0,miss:[]}; const wr=a.n?Math.round(a.wrong/a.n*100):0; const ar=IMGA[st.img]||ASPECT;
    const rects=st.rects.map((r,ri)=>`<div class="rect ${ri?'alt':''}" style="left:${r.l}%;top:${r.t}%;width:${r.w}%;height:${r.h}%"></div>`+(showZone?(()=>{ const z=hitZone(r); return `<div class="zone" style="left:${z.l}%;top:${z.t}%;width:${z.w}%;height:${z.h}%"></div>`; })():'')).join('');
    const dots=showMiss?a.miss.map(([x,y])=>`<i class="dot" style="left:${x}%;top:${y}%"></i>`).join(''):'';
    const flags=[]; if(wr>=40&&a.n>=3) flags.push(`<span class="warn">오답률 ${wr}%</span>`); if(disputes[st.id]) flags.push(`<span class="tag">⚑ 이의 ${disputes[st.id]}건</span>`); if(a.n&&a.to) flags.push(`<span class="tag">⏰ ${a.to}</span>`);
    return `<div class="bm"><div class="bmimg" style="aspect-ratio:${ar.toFixed(3)}"><img src="${IMG[st.img]}" alt="" loading="lazy">${rects}${dots}</div><div class="bmcap"><b>${i+1}. ${st.task}</b><span class="st">${siteLabel(st)}${st.path?' › '+esc(st.path):''}</span><span class="st">시도 ${a.n} · 오답률 ${wr}% · 찬스 ${a.n?Math.round(a.chance/a.n*100):0}% · 평균 ${a.n?Math.round(a.secs/a.n):0}초 · 오클릭 ${a.miss.length}점</span>${flags.join('')}</div></div>`; }).join('') || '<p>이 스테이지에 스텝이 없습니다.</p>';
}
async function openBoardMap(){ if(!masterOk()){ askMaster(openBoardMap); return; }
  const host=$('overlayHost2')||(()=>{ const d=document.createElement('div'); d.id='overlayHost2'; document.body.appendChild(d); return d; })();
  BM.course=S.course; const stages=()=>STAGES.filter(s=>s.course===BM.course&&!s.locked); BM.stage=(stages()[0]||{}).id;
  host.innerHTML=`<div class="modal on" id="bmModal"><div class="g-panel" style="width:min(1100px,100%)"><h2 class="g">🗺 정답 지도 · 오클릭 히트맵</h2><div class="bmap"><div class="bmhead"><select id="bmCourse">${Object.entries(COURSES).map(([k,c])=>`<option value="${k}" ${k===BM.course?'selected':''}>${esc(c.long)}</option>`).join('')}</select><select id="bmStage"></select><label class="kbd"><input type="checkbox" id="bmMiss" checked> 오클릭 점(🔴)</label><label class="kbd"><input type="checkbox" id="bmZone" checked> 판정 영역(점선)</label><span class="kbd" id="bmSrc">기록 불러오는 중…</span><button type="button" class="g-btn sm gray" id="bmClose" style="margin-left:auto">닫기</button></div><p class="kbd" style="margin:0">초록 실선 = 정답 영역(점선 안까지 정답 처리) · 빨간 점 = 실제 오클릭 위치. 점이 한 곳에 몰리면 그 UI가 정답처럼 보인다는 뜻 — ♻ 개선 루프에서 영역 추가/힌트 수정으로 반영하세요.</p><div id="bmBody" class="bmap"><p>불러오는 중…</p></div></div></div></div>`;
  const fillStages=()=>{ $('bmStage').innerHTML=stages().map(s=>`<option value="${s.id}" ${s.id===BM.stage?'selected':''}>${stageCode(s)} · ${esc(s.title)}</option>`).join(''); };
  fillStages();
  $('bmCourse').addEventListener('change', e=>{ BM.course=e.target.value; BM.stage=(stages()[0]||{}).id; fillStages(); bmRender(); });
  $('bmStage').addEventListener('change', e=>{ BM.stage=e.target.value; bmRender(); });
  $('bmMiss').addEventListener('change', bmRender); $('bmZone').addEventListener('change', bmRender);
  $('bmClose').addEventListener('click', ()=>{ host.innerHTML=''; }); $('bmModal').addEventListener('click', e=>{ if(e.target.id==='bmModal') host.innerHTML=''; });
  try{ const {rows,src}=await loadRuns(); BM.runs=rows||[]; BM.src=src||''; BM.fb=await loadFeedback(); }catch(e){ BM.runs=localRuns(); BM.src='이 기기 기록'; }
  if($('bmSrc')) $('bmSrc').textContent=`${BM.src} · ${BM.runs.length}런`;
  bmRender();
}

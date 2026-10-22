
/* ═══════════════════════════════════════════ v27(v37): 다 쌓이게 — 팀 저장 보내기함(outbox) · 저장 상태 표시 · 공유 코드 합치면 팀 저장소로 ═══════════════════════════════════════════ */
/* 원리: 팀 저장소(db)에 못 쓴 기록·의견·평가는 이 기기 보내기함에 쌓아 두고, 다음에 저장 가능할 때 자동 재전송.
   팀 저장소에 쓸 수 없는 사람(조직 밖·로그인 안 함)은 📤 공유 코드로 보내고, 팀장님이 합치면 팀 저장소로 올라간다. */
const OUTBOX_KEY='dsg_outbox';
let TEAMW=null; /* true=팀 저장 가능, false=불가, null=모름 */
function outbox(){ try{ return JSON.parse(localStorage.getItem(OUTBOX_KEY)||'[]'); }catch(e){ return []; } }
function outboxSet(l){ try{ localStorage.setItem(OUTBOX_KEY, JSON.stringify(l.slice(-1500))); }catch(e){} }
function docKey(col, d){ return col+'|'+(d.name||'')+'|'+(d.at||'')+'|'+(d.mode||d.kind||'')+'|'+(d.stage||''); }
async function teamWritable(){ if(TEAMW!==null) return TEAMW; const db=await getDB(); if(!db){ TEAMW=false; return false; } try{ const u=window.claude&&window.claude.use?await window.claude.use('user'):null; const c=u&&u.can?await u.can('data.write'):null; TEAMW = c===false?false:true; }catch(e){ TEAMW=true; } return TEAMW; }
async function teamAdd(col, doc, fromOutbox){ const db=await getDB(); if(db && (await teamWritable())){ try{ await db.collection(col).add(doc); if(!fromOutbox) setTimeout(flushOutbox, 400); return 'db'; }catch(e){ TEAMW=false; } }
  if(!fromOutbox){ const l=outbox(); const k=docKey(col,doc); if(!l.some(x=>x.k===k)){ l.push({ k, col, doc }); outboxSet(l); } renderSync(); } return 'local'; }
let FLUSHING=false;
async function flushOutbox(){ if(FLUSHING) return; const l=outbox(); if(!l.length) return; if(!(await teamWritable())) { renderSync(); return; } FLUSHING=true; const left=[]; for(const x of l){ const r=await teamAdd(x.col, x.doc, true); if(r==='local') left.push(x); } outboxSet(left); FLUSHING=false; renderSync(); if(l.length>left.length) toast(`☁ 이 기기에 쌓여 있던 ${l.length-left.length}건을 팀 저장소로 보냈어요`); }
/* 미션 화면 저장 상태 줄 */
function renderSync(){ const cork=document.querySelector('#map .cork'); if(!cork) return; let el=$('syncBar'); if(!el){ el=document.createElement('div'); el.id='syncBar'; el.className='syncbar'; const n=$('notice'); if(n) n.after(el); else cork.prepend(el); }
  const n=outbox().length; if(!navigator.onLine){ el.className='syncbar warn'; el.innerHTML=`<span>📴 오프라인 — 훈련은 그대로 하세요. ${n?`기록·의견 <b>${n}건</b>이 기다리는 중, `:''}연결되면 자동으로 시트에 올라가요</span>`; return; } teamWritable().then(w=>{ if(w&&!n){ el.className='syncbar ok'; el.innerHTML=`<span>☁ 기록·의견이 <b>팀 저장소</b>에 바로 쌓이고 있어요</span>`; return; }
    el.className='syncbar warn'; el.innerHTML=`<span>📱 ${w?`팀 저장소 연결 대기 — <b>${n}건</b>이 이 기기에 쌓여 있어요(자동 재전송)`:`이 기기에서는 팀 저장소에 쓸 수 없어요 — 기록·의견 <b>${n}건</b>이 이 기기에만 있어요`}</span>${w?'':'<button type="button" class="g-btn sm" id="syncSend">📤 팀장님께 보내기</button>'}<small>${w?'':'공유 코드를 카톡으로 보내면 팀장님 현황표에서 합쳐져 팀 전체에 쌓입니다'}</small>`;
    const b=$('syncSend'); if(b) b.addEventListener('click', openShareOut); }); }
/* 공유 코드로 합친 기록 → 팀 저장소에도 올림(팀장님 기기에서) */
async function pushMergedToTeam(added){ if(!(await teamWritable())) return 0; let n=0; for(const [col, d] of added){ const r=await teamAdd(col, d, true); if(r!=='local') n++; } return n; }
/* 로드: 팀 저장소 + 이 기기(합친 코드·보내기함) 합치기, 중복 제거 */
function mergeRows(rows, local){ const seen=new Set((rows||[]).map(r=>(r.name||'')+'|'+(r.at||''))); const out=(rows||[]).slice(); (local||[]).forEach(r=>{ const k=(r.name||'')+'|'+(r.at||''); if(!seen.has(k)){ seen.add(k); out.push(r); } }); return out.sort((a,b)=>(b.at||'').localeCompare(a.at||'')); }

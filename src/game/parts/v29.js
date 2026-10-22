
/* ═══════════════════════════════════════════ v29(v39): 🚚 새 주소로 이사 — 예전(claude.ai) 기록을 한 번에 웹 사이트로 ═══════════════════════════════════════════ */
const WEB_URL='https://fromgray-lab.github.io/wellcheck-demo-spotter/';
const ON_WEB=location.hostname.endsWith('github.io');
async function makeMoveCode(){ const payload={ v:1, by:(S.profile&&S.profile.name)||S.name||'', at:new Date().toISOString(), move:true, runs:localRuns().slice(0,400).map(compactRun), evals:localList('dsg_evals').slice(0,200), fb:localList('dsg_fb').slice(0,300) };
  const bytes=new TextEncoder().encode(JSON.stringify(payload)); const z=await deflateBytes(bytes); return { code: z ? 'DSG1:'+B64U.enc(z) : 'DSG0:'+B64U.enc(bytes), n:payload.runs.length+payload.evals.length+payload.fb.length }; }
/* 예전 버전(아티팩트): 미션 화면에 이사 안내 + 한 번에 옮기기 */
function renderMoveBar(){ if(ON_WEB) return; const cork=document.querySelector('#map .cork'); if(!cork||$('moveBar')) return; const el=document.createElement('div'); el.id='moveBar'; el.className='movebar';
  const n=localRuns().length+localList('dsg_fb').length+localList('dsg_evals').length;
  el.innerHTML=`<span>🚚 <b>새 주소로 이사했어요</b> — 이제 기록·의견이 구글 시트에 자동으로 쌓이는 웹 버전을 써 주세요.${n?` 이 기기의 기록·의견 <b>${n}건</b>을 한 번에 옮길 수 있어요.`:''}</span><a class="g-btn sm green" id="moveGo" href="${WEB_URL}" target="_blank" rel="noopener">${n?'📦 내 기록 들고 새 주소로':'새 주소 열기'}</a>`;
  cork.prepend(el); const a=$('moveGo'); if(n) a.addEventListener('click', async (e)=>{ e.preventDefault(); a.textContent='준비 중…'; try{ const { code }=await makeMoveCode(); const url=WEB_URL+'#import='+code; const w=window.open(url,'_blank','noopener'); if(!w){ a.href=url; a.textContent='👉 다시 눌러 새 주소 열기'; a.replaceWith(a.cloneNode(true)); return; } a.textContent='✓ 새 주소에서 합쳐집니다'; }catch(err){ a.textContent='새 주소 열기'; window.open(WEB_URL,'_blank','noopener'); } }); }
/* 웹 버전: 주소 #import=코드 로 들어오면 자동으로 합치고 시트에 올림 */
async function importFromHash(){ const m=(location.hash||'').match(/import=([^&]+)/); if(!m) return; try{ history.replaceState(null,'',location.pathname+location.search); }catch(e){}
  try{ const d=await parseShareCode(decodeURIComponent(m[1])); const { nr, ne, nf }=mergeShared(d); toast(`📦 이사 완료 — 기록 ${nr} · 의견 ${nf||0} · 평가 ${ne}건을 가져왔어요 (시트로 올리는 중)`); }catch(err){ toast('이사 코드를 읽지 못했어요 — 예전 화면에서 다시 눌러 주세요'); } }
setTimeout(importFromHash, 600);

/* ── 📲 홈 화면 앱 · 오프라인 훈련 (웹 버전만) ── */
let INSTALL_EVT=null; const IS_STANDALONE=(window.matchMedia&&matchMedia('(display-mode: standalone)').matches)||navigator.standalone===true;
if(ON_WEB && 'serviceWorker' in navigator){ window.addEventListener('load', ()=>{ navigator.serviceWorker.register('sw.js').catch(()=>{}); }); }
window.addEventListener('beforeinstallprompt', e=>{ e.preventDefault(); INSTALL_EVT=e; renderInstallChip(); });
function renderInstallChip(){ if(!ON_WEB||IS_STANDALONE) return; const row=document.querySelector('#todo .trow.tools'); if(!row||row.querySelector('.tchip.install')) return; const b=document.createElement('button'); b.type='button'; b.className='tchip install'; b.innerHTML='<b>📲</b> 홈 화면에 앱으로 <small>인터넷 없어도 훈련</small>'; b.title='폰 홈 화면에 설치 — 지하철·대기실에서도 연습, 기록은 연결되면 자동으로 시트에'; row.appendChild(b);
  b.addEventListener('click', async ()=>{ if(INSTALL_EVT){ INSTALL_EVT.prompt(); try{ const r=await INSTALL_EVT.userChoice; if(r&&r.outcome==='accepted'){ toast('📲 설치됐어요 — 홈 화면의 「틀린시연찾기」로 여세요'); b.remove(); } }catch(e){} INSTALL_EVT=null; return; }
    const ios=/iphone|ipad|ipod/i.test(navigator.userAgent); toast(ios?'아이폰: 사파리 아래 공유 버튼(□↑) → "홈 화면에 추가"':'크롬 오른쪽 위 ⋮ → "홈 화면에 추가" 또는 "앱 설치"'); }); }
function renderNetBadge(){ if(!ON_WEB) return; let el=$('netBadge'); if(!el){ el=document.createElement('div'); el.id='netBadge'; el.className='netbadge'; document.body.appendChild(el); } el.hidden=navigator.onLine; el.textContent='📴 오프라인 — 훈련은 계속, 기록은 연결되면 자동 전송'; }
window.addEventListener('online', ()=>{ renderNetBadge(); toast('🛜 다시 연결됐어요 — 쌓인 기록을 보내는 중'); try{ flushOutbox(); renderSync(); }catch(e){} });
window.addEventListener('offline', ()=>{ renderNetBadge(); try{ renderSync(); }catch(e){} }); setTimeout(renderNetBadge, 800);

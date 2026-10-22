
/* ═══════════════════════════════════════════ v16: 복습 카드에 내 오클릭 표시 · 시연 대본 전체 듣기 ═══════════════════════════════════════════ */

/* ── 1) 복습 카드 오버레이: 정답 영역(초록 박스) + 내가 누른 곳(빨간 점) — 크롭(배경 250%, 16:9) 좌표로 변환 ── */
/* 크롭 위치: 정답 중심이 가운데 오도록 background-position 계산 (p = (f·S − 0.5)/(S − 1), 0~100% 클램프) */
function cropPos(st){ const rc=st.rects[0]; const A=IMGA[st.img]||ASPECT; const Sx=2.5, Sy=2.5*16/(9*A); const fx=(rc.l+rc.w/2)/100, fy=(rc.t+rc.h/2)/100; const px=Math.max(0,Math.min(1,(fx*Sx-0.5)/(Sx-1)))*100, py=Math.max(0,Math.min(1,(fy*Sy-0.5)/(Sy-1)))*100; return { px, py, Sx, Sy }; }
function reviewMarks(st){ const rc=st.rects[0]; const { px:P, py:Py, Sx, Sy }=cropPos(st);
  const mx=(x)=>P+(x-P)*Sx, my=(y)=>Py+(y-Py)*Sy;
  const logs=(S.stepLog||[]).filter(l=>l.id===st.id); const last=logs[logs.length-1]; const miss=(last&&last.miss)||[];
  const box=`<b class="rbox" style="left:${mx(rc.l).toFixed(1)}%;top:${my(rc.t).toFixed(1)}%;width:${(rc.w*Sx).toFixed(1)}%;height:${(rc.h*Sy).toFixed(1)}%"></b>`;
  const dots=miss.map(([x,y],i)=>{ const ex=mx(x), ey=my(y); if(ex<-3||ex>103||ey<-3||ey>103) return ''; return `<i class="rdot" style="left:${ex.toFixed(1)}%;top:${ey.toFixed(1)}%" title="내가 누른 곳 ${i+1}">${i+1}</i>`; }).join('');
  const out=miss.filter(([x,y])=>{ const ex=mx(x), ey=my(y); return ex<-3||ex>103||ey<-3||ey>103; }).length;
  return box+dots+(out?`<small class="rout">화면 밖 오클릭 ${out}</small>`:''); }

/* ── 2) 시연 대본 전체 듣기(TTS): 스테이지의 경로·멘트를 순서대로 읽어줌 — 출퇴근 귀 연습 ── */
const LISTEN={ on:false, tok:null };
function listenStop(){ LISTEN.on=false; LISTEN.tok=null; if(TTS.ok) try{ speechSynthesis.cancel(); }catch(e){} const b=$('scListen'); if(b) b.textContent='🔊 전체 듣기'; document.querySelectorAll('.sclist li.say').forEach(li=>li.classList.remove('say')); }
function listenStage(stageId){ if(!TTS.ok){ toast('이 브라우저는 음성 합성을 지원하지 않아요'); return; } if(LISTEN.on){ listenStop(); return; } if(!TTS.on) ttsSet(true);
  const steps=STEPS.filter(s=>s.st===stageId&&!s.branch); const items=[]; steps.forEach((s,i)=>{ const site=siteOf(s); items.push({ i, text:`${i+1}번. ${site.n}${s.path?', '+s.path.replace(/›/g,',')+'.':'.'} ${(s.task||'').replace(/<[^>]+>/g,'')}` }); if(s.who&&s.say) items.push({ i, text:`${s.who}. ${s.say}`, pitch:0.9 }); if(s.tip&&s.tip.say) items.push({ i, text:s.tip.say }); });
  const tok={}; LISTEN.on=true; LISTEN.tok=tok; const b=$('scListen'); if(b) b.textContent='⏹ 정지'; let k=0;
  const next=()=>{ if(LISTEN.tok!==tok) return; if(k>=items.length){ listenStop(); return; } const it=items[k++]; document.querySelectorAll('.sclist li').forEach((li,j)=>li.classList.toggle('say', j===it.i)); const u=speak(it.text,{ rate:1.0, pitch:it.pitch||1, onEnd:(why)=>{ if(LISTEN.tok!==tok) return; if(why==='end') setTimeout(next, 350); else if(why!=='interrupted'&&why!=='canceled') setTimeout(next, 350); } }); if(!u){ setTimeout(next, 10); } };
  next(); }

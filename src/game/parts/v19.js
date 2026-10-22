
/* ═══════════════════════════════════════════ v19: 🖨 내 코칭 리포트(본인용) · 성장 그래프 ═══════════════════════════════════════════ */
function myPerson(){ const rows=localRuns(); const me=(S.profile&&S.profile.name)||S.name||''; const office=(S.profile&&S.profile.office)||''; const list=aggregate(rows.filter(r=>(r.name||'')===me), []); return list.find(p=>p.name===me && (!office||p.office===office)) || list[0] || null; }
/* 성장 그래프: 전체 완주 점수(파랑) · 오늘의 10문제/주간 챌린지 점수(주황) 시간순, SVG */
function growthSvg(runs){ const pts=(runs||[]).filter(r=>['all','daily','weekly','focus'].includes(r.mode)&&typeof r.score==='number'&&!r.over).sort((a,b)=>(a.at||'').localeCompare(b.at||'')).slice(-30); if(pts.length<2) return '';
  const W=720,H=180,pl=36,pr=12,pt=14,pb=26; const n=pts.length; const x=i=>pl+(W-pl-pr)*(n===1?0.5:i/(n-1)); const y=v=>pt+(H-pt-pb)*(1-v/100);
  const col={all:'#2b9bff',daily:'#ff8a00',weekly:'#b45309',focus:'#e0365b'}; const lab={all:'전체 완주',daily:'오늘의 10문제',weekly:'주간 챌린지',focus:'약점 집중'};
  const grid=[0,25,50,75,100].map(v=>`<line x1="${pl}" y1="${y(v)}" x2="${W-pr}" y2="${y(v)}" stroke="#e3e6ee"/><text x="${pl-6}" y="${y(v)+4}" font-size="10" text-anchor="end" fill="#8a90ab">${v}</text>`).join('');
  const line=`<polyline fill="none" stroke="#b8bccc" stroke-width="1.5" points="${pts.map((r,i)=>x(i)+','+y(r.score)).join(' ')}"/>`;
  const dots=pts.map((r,i)=>`<circle cx="${x(i)}" cy="${y(r.score)}" r="4.5" fill="${col[r.mode]||'#999'}" stroke="#fff" stroke-width="1.5"><title>${lab[r.mode]||r.mode} ${r.score}점 · ${r.grade||''} · ${r.at?new Date(r.at).toLocaleDateString('ko-KR'):''}</title></circle>`).join('');
  const xl=[0,Math.floor((n-1)/2),n-1].filter((v,i,a)=>a.indexOf(v)===i).map(i=>`<text x="${x(i)}" y="${H-8}" font-size="10" text-anchor="middle" fill="#8a90ab">${pts[i].at?new Date(pts[i].at).toLocaleDateString('ko-KR',{month:'numeric',day:'numeric'}):''}</text>`).join('');
  const legend=Object.entries(lab).filter(([k])=>pts.some(r=>r.mode===k)).map(([k,l],i)=>`<circle cx="${pl+i*120}" cy="${pt-6}" r="4" fill="${col[k]}"/><text x="${pl+i*120+8}" y="${pt-2}" font-size="10" fill="#5b6383">${l}</text>`).join('');
  return `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-height:220px;display:block" role="img" aria-label="점수 추이">${grid}${line}${dots}${xl}${legend}</svg>`; }
function saveMyReport(btn){ const p=myPerson(); if(!p){ toast('아직 기록이 없어요'); return; } saveCoachReport(p, btn); }

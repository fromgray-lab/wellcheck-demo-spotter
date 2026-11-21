// 규칙 L10 점검 도구: '전송됨' 표시와 실제 시트 도착이 어긋날 때 기기 보관분이 다시 시트로 가는지 잰다.
// 사용: node src/game/l10check.js [index.html 경로(기본 루트 index.html)]
// 빌드본을 github.io 주소로 띄우고(SHEETS.url이 켜지게) script.google.com을 가짜 시트로 가로챈다 — 실제 시트에는 아무것도 쓰지 않음.
// 기기 보관분(시드): R1 시트에 있음·전송됨 / R2 전송 안 됨 / F1 전송됨인데 시트에 없음(유실) / R3 전송됨·시트에 없음·2분 전(아직 도착 중일 수 있음 → 건드리면 안 됨)
// 기대: R1 중복 없이 1행 · R2 도착 · F1 도착(도착 확인 재전송) · R3 안 보냄
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');const FILE=path.resolve(process.argv[2]||ROOT+'/index.html');
const {chromium}=require('/opt/npm-tools/node_modules/playwright');
const BASE='https://fromgray-lab.github.io/wellcheck-demo-spotter/';
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1280,height:800}});
const now=Date.now(),iso=ms=>new Date(now-ms).toISOString();
const R1={name:'검수봇',mode:'one',stage:'m0',score:90,at:iso(3600e3)},R2={name:'검수봇',mode:'one',stage:'m1',score:80,at:iso(3000e3)},R3={name:'검수봇',mode:'one',stage:'m2',score:70,at:iso(120e3)};
const F1={kind:'tap',name:'검수봇',stage:'m0',thumbs:'up',at:iso(2400e3)};
const store={runs:[R1],feedback:[],evals:[],notes:[]};const posts=[];
await ctx.route(/script\.google\.com/,async r=>{const req=r.request();
  if(req.method()==='POST'){const body=new URLSearchParams(req.postData()||'');let p={};try{p=JSON.parse(body.get('payload')||'{}');}catch(e){}
    posts.push(p.col+':'+(p.doc&&p.doc.stage)+':'+(p.doc&&p.doc.kind||''));const L=store[p.col];if(L&&p.doc&&!L.some(x=>x.at===p.doc.at&&x.name===p.doc.name))L.push(p.doc);
    return r.fulfill({status:200,contentType:'text/html',body:'<html>ok</html>'});}
  const u=new URL(req.url());const col=u.searchParams.get('col'),cb=u.searchParams.get('cb'),lim=+u.searchParams.get('limit')||3000;
  const rows=(store[col]||[]).slice(-lim).reverse();return r.fulfill({status:200,contentType:'application/javascript',body:cb+'('+JSON.stringify({ok:true,rows})+')'});});
await ctx.route(/^https:\/\/fromgray-lab\.github\.io\//,async r=>{let rel=new URL(r.request().url()).pathname.replace('/wellcheck-demo-spotter/','');
  let f=rel===''?FILE:path.join(ROOT,decodeURIComponent(rel));if(!fs.existsSync(f)||fs.statSync(f).isDirectory())return r.fulfill({status:404,body:''});
  const ext=path.extname(f).toLowerCase();const ct={'.html':'text/html','.js':'application/javascript','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.json':'application/json','.mp3':'audio/mpeg','.css':'text/css','.svg':'image/svg+xml'}[ext]||'application/octet-stream';
  return r.fulfill({status:200,contentType:ct,body:fs.readFileSync(f)});});
await ctx.route(/^https?:/,r=>{const u=r.request().url();if(/script\.google\.com|fromgray-lab\.github\.io/.test(u))return r.fallback();return r.abort();});
await ctx.addInitScript(([R1,R2,R3,F1])=>{try{if(localStorage.getItem('__seeded'))return;localStorage.setItem('__seeded','1');localStorage.setItem('dsg_onb','1');localStorage.setItem('dsg_name','검수봇');localStorage.setItem('dsg_fb_rec63','0');
  localStorage.setItem('dsg_runs',JSON.stringify([R3,R2,R1]));localStorage.setItem('dsg_fb',JSON.stringify([F1]));
  localStorage.setItem('dsg_sent',JSON.stringify(['runs|검수봇|'+R1.at,'feedback|검수봇|'+F1.at,'runs|검수봇|'+R3.at]));}catch(e){}},[R1,R2,R3,F1]);
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto(BASE);await p.waitForTimeout(14000);
const sentAfter=await p.evaluate(()=>JSON.parse(localStorage.getItem('dsg_sent')||'[]'));
const has=(col,d)=>store[col].filter(x=>x.at===d.at).length;
const res={R1:has('runs',R1),R2:has('runs',R2),F1:has('feedback',F1),R3:has('runs',R3)};
console.log('시트 행 수',JSON.stringify(res),'POST',posts.length,JSON.stringify(posts));console.log('전송됨 표시',sentAfter.length,'건 · pageerrors',errs.length,errs.slice(0,2).join(' | '));
const ok=res.R1===1&&res.R2===1&&res.F1===1&&res.R3===0&&!errs.length;console.log(ok?'L10 통과 — 유실분 재전송·중복 없음·도착 중인 것 대기':'L10 실패');process.exitCode=ok?0:1;await b.close();})();

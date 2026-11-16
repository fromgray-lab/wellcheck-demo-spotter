// 빌드된 루트 index.html에서 STEPS·STAGES·IMG를 JSON으로 뽑는다(외부 네트워크 차단). 사용: node src/game/dump_steps.js 출력.json
const fs=require('fs'),path=require('path');const ROOT=path.resolve(__dirname,'../..');
const {chromium}=require('/opt/npm-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext();await ctx.route(/^https?:/,r=>r.abort());
const p=await ctx.newPage();await p.goto('file://'+ROOT+'/index.html');await p.waitForTimeout(800);
const d=await p.evaluate(()=>({steps:window.__DSG.STEPS.map(s=>({id:s.id,st:s.st,img:s.img,task:s.task,hint:s.hint,rects:s.rects})),stages:window.__DSG.STAGES.map(s=>s.id),IMG:window.__DSG.IMG}));
fs.writeFileSync(process.argv[2]||'steps.json',JSON.stringify(d));await b.close();})();

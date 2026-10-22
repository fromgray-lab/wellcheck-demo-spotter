// 콘텐츠 린트: 빌드된 demo-spotter.html을 headless로 열어 STEPS/STAGES/IMG를 전수 검사.
// 오류(error)가 하나라도 있으면 exit 1 → build.py가 실패. 경고(warn)는 출력만.
const fs = require('fs'), path = require('path');
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const GAME = __dirname + '/';
const html = fs.readFileSync(GAME + 'demo-spotter.html', 'utf8');
const wrap = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + html + '</body></html>';
fs.writeFileSync(GAME + '.lint.html', wrap);
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 800 } });
  const errors = [], warns = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  await page.route(/fonts\.g(oogleapis|static)\.com/, r => r.abort());
  await page.goto('file://' + GAME + '.lint.html', { waitUntil: 'load' });
  await page.waitForTimeout(400);
  const data = await page.evaluate(() => {
    const D = window.__DSG;
    return {
      steps: D.STEPS.map(s => ({ id: s.id, st: s.st, img: s.img, rects: s.rects, hint: s.hint, chance: s.chance, task: s.task, tip: s.tip, site: s.site, path: s.path, branch: s.branch, who: s.who, say: s.say, real: s.real, next: s.next, q: s.q })),
      stages: D.STAGES.map(s => ({ id: s.id, course: s.course, n: s.n, title: s.title })),
      IMG: D.IMG, IMGA: D.IMGA, QCARDS: (D.QCARDS || window.QCARDS || []).map(q => ({ id: q.id, course: q.course, st: q.st, after: q.after, q: q.q, opts: q.opts, ans: q.ans, why: q.why }))
    };
  });
  await browser.close();
  const { steps, stages, IMG, IMGA, QCARDS } = data;
  const stageIds = new Set(stages.map(s => s.id));
  const seen = new Set();
  const strip = s => String(s || '').replace(/<[^>]+>/g, '');
  const hitZone = (r, e) => { e = e || 0; const padW = Math.max(0, 6 - r.w) / 2 + 1.0 + e, padH = Math.max(0, 8 - r.h) / 2 + 1.2 + e * 1.4; return { l: r.l - padW, t: r.t - padH, w: r.w + 2 * padW, h: r.h + 2 * padH }; };
  const imgDims = {};
  for (const k of Object.keys(IMG)) {
    const p = GAME + IMG[k];
    if (!fs.existsSync(p)) { errors.push(`이미지 없음 ${k} → ${IMG[k]}`); continue; }
    // webp/jpg 크기 읽기(간단 파서)
    const buf = fs.readFileSync(p); let w = 0, h = 0;
    if (buf.slice(0, 4).toString() === 'RIFF' && buf.slice(8, 12).toString() === 'WEBP') {
      const chunk = buf.slice(12, 16).toString();
      if (chunk === 'VP8X') { w = 1 + buf.readUIntLE(24, 3); h = 1 + buf.readUIntLE(27, 3); }
      else if (chunk === 'VP8 ') { w = buf.readUInt16LE(26) & 0x3fff; h = buf.readUInt16LE(28) & 0x3fff; }
      else if (chunk === 'VP8L') { const b = buf.readUInt32LE(21); w = (b & 0x3fff) + 1; h = ((b >> 14) & 0x3fff) + 1; }
    } else if (buf[0] === 0xff && buf[1] === 0xd8) {
      let i = 2; while (i < buf.length) { if (buf[i] !== 0xff) { i++; continue; } const m = buf[i + 1]; if (m >= 0xc0 && m <= 0xcf && m !== 0xc4 && m !== 0xc8 && m !== 0xcc) { h = buf.readUInt16BE(i + 5); w = buf.readUInt16BE(i + 7); break; } i += 2 + buf.readUInt16BE(i + 2); }
    }
    imgDims[k] = [w, h];
    if (w && h && IMGA[k]) { const a = w / h; if (Math.abs(a - IMGA[k]) / IMGA[k] > 0.015) errors.push(`비율 불일치 ${k}: 파일 ${w}x${h}=${a.toFixed(3)} vs IMGA ${IMGA[k].toFixed(3)}`); }
    if (!IMGA[k]) warns.push(`IMGA 없음 ${k} (기본 비율 사용)`);
    if (w && w < 1200) warns.push(`저해상도 ${k} ${w}x${h}`);
  }
  for (const s of steps) {
    const tag = `[${s.st}/${s.id}]`;
    if (seen.has(s.id)) errors.push(`${tag} 중복 id`); seen.add(s.id);
    if (!stageIds.has(s.st)) errors.push(`${tag} 없는 스테이지`);
    if (!IMG[s.img]) errors.push(`${tag} 이미지 키 없음 ${s.img}`);
    if (!s.rects || !s.rects.length) errors.push(`${tag} rects 없음`);
    (s.rects || []).forEach((r, i) => {
      if (!(r.w > 0 && r.h > 0)) errors.push(`${tag} rect${i} 크기 0`);
      if (r.l < 0 || r.t < 0 || r.l + r.w > 100.01 || r.t + r.h > 100.01) errors.push(`${tag} rect${i} 범위 밖 ${JSON.stringify(r)}`);
      const z = hitZone(r);
      if (z.l < -3 || z.t < -3 || z.l + z.w > 103 || z.t + z.h > 103) warns.push(`${tag} rect${i} 판정영역이 보드 밖으로 많이 나감`);
      if (r.w * r.h < 4) warns.push(`${tag} rect${i} 매우 작음 ${r.w}x${r.h}% (판정 최소 6x8%로 확장됨)`);
      if (r.w > 60 || r.h > 60) warns.push(`${tag} rect${i} 매우 큼 ${r.w}x${r.h}%`);
    });
    if (!strip(s.task).trim()) errors.push(`${tag} task 비어 있음`);
    const stg = stages.find(x => x.id === s.st); if (stg && stg.course === 'biz' && !/<b>/.test(s.task || '')) warns.push(`${tag} task에 강조(<b>) 없음`);
    if (strip(s.task).length > 64) warns.push(`${tag} task 길이 ${strip(s.task).length}`);
    if (!s.branch) {
      if (!s.hint || !s.hint.trim()) errors.push(`${tag} hint 없음`);
      if (!s.chance || !s.chance.trim()) errors.push(`${tag} chance 없음`);
      if (s.hint && s.hint.length > 44) warns.push(`${tag} hint 길이 ${s.hint.length}`);
      if (s.hint && strip(s.task).includes(s.hint)) warns.push(`${tag} hint가 task와 동일(힌트 가치 낮음)`);
    }
    if (s.tip && s.tip.say && s.tip.say.length > 160) warns.push(`${tag} tip.say 길이 ${s.tip.say.length}`);
    if (!s.tip || !s.tip.say) warns.push(`${tag} tip 없음`);
    if (!s.site) errors.push(`${tag} 사이트 매핑 없음(SITE_OF)`);
    if (s.site && !s.path) warns.push(`${tag} 경로(path) 없음`);
    if (s.say && !s.who) warns.push(`${tag} say 있는데 who 없음`);
    if (s.next && !steps.find(x => x.id === s.next)) errors.push(`${tag} next 스텝 없음 ${s.next}`);
  }
  // 같은 보드 안에서 서로 다른 스텝의 정답이 거의 같은 위치면(연속 스텝 제외) 혼동 경고
  const byImg = {}; steps.forEach(s => { (byImg[s.img] = byImg[s.img] || []).push(s); });
  const ov = (a, b) => { const x = Math.max(0, Math.min(a.l + a.w, b.l + b.w) - Math.max(a.l, b.l)), y = Math.max(0, Math.min(a.t + a.h, b.t + b.h) - Math.max(a.t, b.t)); const i = x * y; return i / Math.min(a.w * a.h, b.w * b.h); };
  for (const [img, list] of Object.entries(byImg)) for (let i = 0; i < list.length; i++) for (let j = i + 1; j < list.length; j++) {
    const a = list[i], b = list[j]; if (a.st !== b.st) continue;
    for (const ra of a.rects) for (const rb of b.rects) if (ov(ra, rb) > 0.6 && strip(a.task) !== strip(b.task)) warns.push(`[${a.id}↔${b.id}] 같은 보드(${img}) 정답 위치가 겹침(${Math.round(ov(ra, rb) * 100)}%)`);
  }
  // 질문 카드
  const stepIds = new Set(steps.map(s => s.id)); const qseen = new Set(); const ansDist = [0, 0, 0];
  for (const q of QCARDS) {
    const tag = `[Q ${q.id}]`;
    if (qseen.has(q.id)) errors.push(`${tag} 중복`); qseen.add(q.id);
    if (!stepIds.has(q.after)) errors.push(`${tag} after 스텝 없음 ${q.after}`);
    const st = steps.find(s => s.id === q.after); if (st && st.st !== q.st) errors.push(`${tag} st(${q.st})와 after 스텝의 스테이지(${st && st.st}) 불일치`);
    if (!q.q || q.q.length > 60) warns.push(`${tag} 질문 길이 ${q.q && q.q.length}`);
    if (!Array.isArray(q.opts) || q.opts.length !== 3) errors.push(`${tag} 보기 3개 아님`);
    if (!(q.ans >= 0 && q.ans < 3)) errors.push(`${tag} ans 범위 밖`); else ansDist[q.ans]++;
    (q.opts || []).forEach((o, i) => { if (o.length > 60) warns.push(`${tag} 보기${i} 길이 ${o.length}`); });
    if (!q.why) errors.push(`${tag} 해설 없음`);
  }
  if (QCARDS.length && Math.max(...ansDist) > QCARDS.length * 0.6) warns.push(`질문 카드 정답 위치 편중 ${ansDist.join('/')}`);
  const stepCount = {}; steps.forEach(s => { stepCount[s.st] = (stepCount[s.st] || 0) + (s.branch ? 0 : 1); });
  console.log(`린트: 스텝 ${steps.length}개 · 스테이지 ${stages.length}개 · 이미지 ${Object.keys(IMG).length}개 · 질문카드 ${QCARDS.length}개`);
  console.log('스테이지별 스텝:', JSON.stringify(stepCount));
  warns.forEach(w => console.log('  ⚠ ' + w));
  errors.forEach(e => console.log('  ✖ ' + e));
  console.log(`경고 ${warns.length} · 오류 ${errors.length}`);
  try { fs.unlinkSync(GAME + '.lint.html'); } catch (e) {}
  process.exit(errors.length ? 1 : 0);
})().catch(e => { console.error('LINT FATAL', e); process.exit(1); });

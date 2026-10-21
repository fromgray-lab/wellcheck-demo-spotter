/** 틀린시연찾기 — 구글 시트 저장소 (Apps Script 웹앱)
 *  배포: 배포 > 새 배포 > 웹 앱 / 실행: 나 / 액세스: 모든 사용자
 *  게임은 POST(text/plain JSON)로 쓰고 GET으로 읽는다. KEY가 맞아야 동작(가벼운 보호).
 */
const KEY = 'dsg-7Kq2-wellcheck';
const SHEETS = {
  runs:      ['at','name','office','mode','course','stage','grade','score','wrong','chance','tips','secs','diff','persona','week','json'],
  feedback:  ['at','name','office','course','stage','mode','result','thumbs','tags','text','stars','wrong','json'],
  evals:     ['at','name','office','evaluator','course','total','memo','json'],
  notes:     ['id','key','text','by','at','json'],
  overrides: ['id','at','status','field','stepId','value','json']
};
const UPSERT = { notes:'id', overrides:'id' };

function sheet_(col){ const ss=SpreadsheetApp.getActive(); let sh=ss.getSheetByName(col); if(!sh){ sh=ss.insertSheet(col); sh.appendRow(SHEETS[col]); sh.setFrozenRows(1); sh.getRange(1,1,1,SHEETS[col].length).setFontWeight('bold').setBackground('#e8eaf0'); } return sh; }
function out_(o){ return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function cell_(v){ if(v==null) return ''; if(Array.isArray(v)) return v.join(', '); if(typeof v==='object') return JSON.stringify(v); const s=String(v); return s.length>2000?s.slice(0,2000):s; }

function doPost(e){
  try{
    const raw=(e.parameter&&e.parameter.payload)||(e.postData&&e.postData.contents)||'{}'; const b=JSON.parse(raw);
    if(b.k!==KEY) return out_({ok:false,err:'key'});
    const col=b.col; if(!SHEETS[col]) return out_({ok:false,err:'col'});
    const d=b.doc||{}; const js=JSON.stringify(d); if(js.length>45000) return out_({ok:false,err:'size'});
    const row=SHEETS[col].map(h=>h==='json'?js:cell_(d[h]));
    const lock=LockService.getScriptLock(); lock.waitLock(20000);
    try{
      const sh=sheet_(col); const idf=UPSERT[col];
      if(idf && d[idf]){ const ids=sh.getRange(2,1,Math.max(0,sh.getLastRow()-1),1).getValues().map(r=>String(r[0])); const i=ids.indexOf(String(d[idf])); if(i>=0){ sh.getRange(i+2,1,1,row.length).setValues([row]); return out_({ok:true,upd:true}); } }
      if(!idf && d.at){ const last=sh.getLastRow(); if(last>1){ const ji=SHEETS[col].indexOf('json')+1; const from=Math.max(2,last-299); const v=sh.getRange(from,ji,last-from+1,1).getValues(); const at=String(d.at), nm=String(d.name||''); for(let i=0;i<v.length;i++){ try{ const o=JSON.parse(v[i][0]); if(String(o.at)===at && String(o.name||'')===nm) return out_({ok:true,dup:true}); }catch(_){} } } }
      sh.appendRow(row);
    } finally { lock.releaseLock(); }
    return out_({ok:true});
  }catch(err){ return out_({ok:false,err:String(err)}); }
}

function doGet(e){
  const p=e.parameter||{};
  const res=get_(p);
  if(p.cb && /^[A-Za-z_$][\w$.]*$/.test(p.cb)) return ContentService.createTextOutput(p.cb+'('+JSON.stringify(res)+')').setMimeType(ContentService.MimeType.JAVASCRIPT);
  return out_(res);
}
function get_(p){
  if(p.k!==KEY) return {ok:false,err:'key'};
  const col=p.col; if(!SHEETS[col]) return {ok:false,err:'col'};
  const sh=sheet_(col); const n=sh.getLastRow()-1; if(n<1) return {ok:true,rows:[]};
  const lim=Math.min(Number(p.limit)||3000, 5000); const start=Math.max(2, sh.getLastRow()-lim+1);
  const hdr=SHEETS[col]; const ji=hdr.indexOf('json');
  const vals=sh.getRange(start,1,sh.getLastRow()-start+1,hdr.length).getValues();
  const rows=[]; vals.forEach(v=>{ try{ rows.push(JSON.parse(v[ji])); }catch(_){} });
  rows.reverse();
  return {ok:true,rows};
}

/** 📊 요약 탭 만들기 — 편집기에서 setupSummary 한 번 실행. 이후 runs·feedback에 쌓이면 수식이 자동 갱신 */
function setupSummary(){
  const ss=SpreadsheetApp.getActive(); ['runs','feedback','evals'].forEach(c=>sheet_(c));
  let sh=ss.getSheetByName('📊 요약'); if(!sh) sh=ss.insertSheet('📊 요약',0); sh.clear();
  const EX="B<>'연결테스트' and B<>'검수봇' and B<>''";
  const blocks=[
    ['A1','■ 사람별 현황 (전체 기록, 테스트 계정 제외)', "=QUERY(runs!A:P,\"select B, C, count(A), max(H), avg(H), max(A) where "+EX+" group by B, C order by max(A) desc label B '이름', C '사무소', count(A) '훈련 수', max(H) '최고점', avg(H) '평균점', max(A) '최근 활동'\",1)"],
    ['I1','■ 모드별 훈련 수', "=QUERY(runs!A:P,\"select D, count(A), avg(H) where "+EX+" group by D order by count(A) desc label D '모드', count(A) '건수', avg(H) '평균점'\",1)"],
    ['I14','■ 최근 7일 참여', "=QUERY(runs!A:P,\"select B, count(A), max(H) where "+EX+" and A >= '\"&TEXT(TODAY()-7,\"yyyy-mm-dd\")&\"' group by B order by count(A) desc label B '이름', count(A) '건수', max(H) '최고점'\",1)"],
    ['M1','■ 최근 의견 50건 (스테이지 피드백)', "=IFERROR(QUERY(feedback!A:M,\"select A, B, E, H, I, J where "+EX+" and (J<>'' or H<>'') order by A desc limit 50 label A '시각', B '이름', E '스테이지', H '👍👎', I '태그', J '의견'\",1),\"아직 의견 없음\")"]
  ];
  blocks.forEach(([cell,title,f])=>{ const r=sh.getRange(cell); r.setValue(title).setFontWeight('bold').setFontColor('#1d2140'); r.offset(1,0).setFormula(f); });
  sh.getRange('E3:E200').setNumberFormat('0.0'); sh.getRange('K3:K12').setNumberFormat('0.0');
  sh.setColumnWidths(1,6,110); sh.setColumnWidth(6,170); sh.setColumnWidth(13,150); sh.setColumnWidth(18,360); sh.setFrozenRows(0);
  return 'ok';
}


/** 📊 요약 탭 만들기 — 편집기에서 setupSummary 한 번 실행. 이후 runs·feedback에 쌓이면 수식이 자동 갱신 */
function setupSummary(){
  const ss=SpreadsheetApp.getActive(); ['runs','feedback','evals'].forEach(c=>sheet_(c));
  let sh=ss.getSheetByName('📊 요약'); if(!sh) sh=ss.insertSheet('📊 요약',0); sh.clear();
  const EX="B<>'연결테스트' and B<>'검수봇' and B<>''";
  const blocks=[
    ['A1','■ 사람별 현황 (전체 기록, 테스트 계정 제외)', "=QUERY(runs!A:P,\"select B, C, count(A), max(H), avg(H), max(A) where "+EX+" group by B, C order by max(A) desc label B '이름', C '사무소', count(A) '훈련 수', max(H) '최고점', avg(H) '평균점', max(A) '최근 활동'\",1)"],
    ['I1','■ 모드별 훈련 수', "=QUERY(runs!A:P,\"select D, count(A), avg(H) where "+EX+" group by D order by count(A) desc label D '모드', count(A) '건수', avg(H) '평균점'\",1)"],
    ['I14','■ 최근 7일 참여', "=QUERY(runs!A:P,\"select B, count(A), max(H) where "+EX+" and A >= '\"&TEXT(TODAY()-7,\"yyyy-mm-dd\")&\"' group by B order by count(A) desc label B '이름', count(A) '건수', max(H) '최고점'\",1)"],
    ['M1','■ 최근 의견 50건 (스테이지 피드백 · 💬 상시 의견)', "=IFERROR(QUERY(feedback!A:M,\"select A, B, E, G, H, I, J where "+EX+" and (J<>'' or H<>'') order by A desc limit 50 label A '시각', B '이름', E '스테이지', G '구분', H '👍👎', I '태그', J '의견'\",1),\"아직 의견 없음\")"]
  ];
  blocks.forEach(([cell,title,f])=>{ const r=sh.getRange(cell); r.setValue(title).setFontWeight('bold').setFontColor('#1d2140'); r.offset(1,0).setFormula(f); });
  sh.getRange('E3:E200').setNumberFormat('0.0'); sh.getRange('K3:K12').setNumberFormat('0.0');
  sh.setColumnWidths(1,6,110); sh.setColumnWidth(6,170); sh.setColumnWidth(13,150); sh.setColumnWidth(19,380); sh.setFrozenRows(0);
  return 'ok';
}

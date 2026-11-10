# 체험존 「웰체크 시뮬레이터」(patientcareroom.web.app/wellcheck-simulator.html) 캡처 → 보드·스텝 생성
# 입력: /tmp/z/steps_{staff,edu,checkup}.json + /tmp/z/shots/*.png   출력: img/sim/*.webp, parts/course_sim.js
import json, os, sys
from PIL import Image
Z='/tmp/z'; HERE=os.path.dirname(os.path.abspath(__file__))
J={m:json.load(open(f'{Z}/steps_{m}.json',encoding='utf8')) for m in ('staff','edu','checkup')}
PFX={'staff':'sa','edu':'se','checkup':'sc'}
def key(m,i): return f'{PFX[m]}{i:02d}'
def pct(r,pad=3):
    x,y,w,h=r; x-=pad; y-=pad; w+=2*pad; h+=2*pad
    x=max(0,x); y=max(0,y); w=min(w,1281-x); h=min(h,675-y)
    return [round(x/1281*100,1),round(y/675*100,1),round(w/1281*100,1),round(h/675*100,1)]
used=set()
def T(m,i,what=None):
    """what: None=가이드 대상 / 'btn:텍스트' / 'x:셀렉터' / 여러 개는 리스트"""
    s=J[m][i]; used.add((m,i))
    if what is None: return [pct(s['r'])]
    out=[]
    for w in (what if isinstance(what,list) else [what]):
        if w=='hl': out.append(pct(s['r']))
        elif w.startswith('btn:'): out.append(pct(s['btns'][w[4:]]))
        elif w.startswith('x:'): out.append(pct(s['extra'][w[2:]]))
    return out
WC,HI,AP,ZN='wc','hira','app','zone'
def st(id,m,i,task,hint,chance,site,path,tip=None,tipFrom=None,who='',say=None,ch=None,rect=None):
    d=dict(id=id,img=key(m,i),task=task,hint=hint,chance=chance,site=site,path=path,rects=T(m,i,rect))
    if tip: d['tip']=dict(say=tip[0],note=tip[1] if len(tip)>1 else '')
    if tipFrom: d['tipFrom']=tipFrom
    if who: d['who']=who; d['say']=say
    if ch: d['ch']=ch
    return d
def keep(id,ch=None):
    d=dict(keep=id)
    if ch: d['ch']=ch
    return d
LIST='일차의료 만성질환 › 일만사 대상자 목록'
HREG='환자 관리 및 서비스 제공 › 대상자 등록'
def reg_core(ids,zone):
    a=[]
    a.append(st(ids[0],'staff',1,'대상자를 등록하러 — <b>심평원 바로 가기</b>','오른쪽 위 검은 버튼',"'심평원 바로 가기'",WC,LIST,tipFrom='m2g',who='원장님',say='"심평원 등록은 어디서요?"',ch=None if zone else '① 심평원 대상자 등록'))
    a.append(st(ids[1],'staff',2,'새 <b>대상자 행</b>을 여는 버튼','표 오른쪽 위 회색 버튼 둘 중 왼쪽',"'대상자등록'",HI,HREG,tipFrom='r3'))
    a.append(st(ids[2],'staff',3,'붉은 <b>필수 항목</b> 채우기 (체험존은 한 번에)','빨간 버튼 — 위·아래 어느 쪽이든',"'모두 입력'",HI,HREG,tipFrom='m2h',rect=['hl','btn:모두 입력']))
    a.append(st(ids[3],'staff',4,'대상자 등록을 끝내는 <b>저장</b>',"'대상자등록' 바로 옆","'저장'",HI,HREG,tipFrom='m2i'))
    a.append(st(ids[4],'staff',5,'심평원 창을 <b>닫고</b> 웰체크로','오른쪽 위 검은 버튼',"'✕ 닫기'",HI,HREG,tip=('저장이 끝나면 심평원 창을 닫고 웰체크로 돌아옵니다.','')))
    a.append(st(ids[5],'staff',6,'등록한 환자를 <b>불러오는</b> 버튼','표 오른쪽 위 파란 버튼',"'환자 정보 업데이트'",WC,LIST,tipFrom='m2j',who='원장님',say='"등록했는데 목록이 비어 있네요?"'))
    return a
def invite(ids,zone):
    a=[]
    a.append(st(ids[0],'staff',7,'박고당 환자에게 <b>앱 초대장</b> 보내기','환자App 열',"환자App 열의 '가입대상'",WC,LIST,tip=('대상자 목록의 환자App 열에서 바로 앱 초대장을 보냅니다.',''),who='원장님',say='"환자 앱은 어떻게 깔게 해요?"',ch='① 앱 초대' if zone else '② 환자 앱 초대'))
    a.append(st(ids[1],'staff',8,'초대장 <b>발송</b>을 확정','팝업 오른쪽 파란 버튼',"'확인'",WC,LIST+' › 가입 필요 팝업',tip=('아직 앱에 가입하지 않은 환자라 설치 초대장을 보낼지 묻습니다. 확인을 누르면 문자가 나갑니다.','')))
    a.append(st(ids[2],'staff',9,'환자 폰 — 문자의 <b>앱 설치 링크</b>',"'웰체크앱 설치 바로가기' 아래",'파란 링크 상자',AP,'환자 스마트폰 › 초대 문자',tip=('환자분 휴대폰으로 초대 문자가 갑니다. 링크 하나로 설치까지 이어져요.',''),ch='② 환자 스마트폰' if zone else None))
    a.append(st(ids[3],'staff',10,'스토어에서 웰체크 <b>설치</b>','초록 버튼',"'설치'",AP,'환자 스마트폰 › Google Play',tip=('스토어에서 설치만 누르시면 됩니다.','')))
    a.append(st(ids[4],'staff',12,'앱 첫 화면 — <b>카카오</b>로 가입','노란 버튼',"'카카오로 시작하기'",AP,'웰체크 앱 › 시작 화면',tip=('휴대폰 번호·카카오·네이버 중 편한 방법으로 가입하시면 됩니다.','')))
    return a
def survey(ids,zone):
    a=[]
    a.append(st(ids[0],'staff',13,'일만사 참여서류 — <b>지금 작성하기</b>','위쪽 파란 카드',"파란 카드의 '지금 작성하기'",AP,'웰체크 앱 › 홈',tipFrom='m3b',ch=None if zone else '① 환자 앱 — 동의·문진'))
    a.append(st(ids[1],'staff',14,'약관 — <b>필수 항목 전체 동의</b>','화면 맨 아래 파란 버튼',"'필수 항목 전체 동의하기'",AP,'웰체크 앱 › 약관 동의',tip=('개인정보·민감정보·제3자 제공과 사업 참여 신청서까지 한 번에 동의받습니다.','화면의 필수 동의 6개 항목 기준.')))
    a.append(st(ids[2],'staff',16,'문진 — <b>복용 중인 약</b>을 고르세요','보기 6개 중 아무거나','보기 상자 안 아무 항목',AP,'웰체크 앱 › 문진표 작성',tip=('해당하는 약을 모두 고르면 다음 버튼이 켜집니다.',''),rect='x:#mob-med-options'))
    a.append(st(ids[3],'staff',18,'마지막 문항 뒤 — <b>문진 제출</b>','화면 맨 아래 파란 버튼',"'문진 제출 완료'",AP,'웰체크 앱 › 문진표 작성',tip=('제출하면 문진 결과가 의사 웹으로 넘어갑니다.','')))
    return a
def careplan(ids,zone):
    a=[]
    a.append(st(ids[0],'staff',20,'앱 문진 결과를 <b>불러오기</b>','표 오른쪽 위 파란 버튼',"'환자 정보 업데이트'",WC,LIST,tip=('환자가 앱에서 낸 문진은 환자 정보 업데이트를 누르면 목록에 반영됩니다.',''),ch='③ 문진 결과·검사' if zone else '② 검사·계획수립'))
    a.append(st(ids[1],'staff',21,'포괄평가 열의 <b>검사</b> 버튼','박고당 행 · 포괄평가 열',"포괄평가 열의 '검사'",WC,LIST,tipFrom='m3a'))
    if zone:
        a.append(st(ids[2],'staff',23,'임상검사 값을 <b>한 번에</b> 채우기','임상검사 내역 제목 줄 · 또는 오른쪽 위',"주황 '검사값 자동채우기' (또는 'EMR 결과 가져오기')",WC,'환자 상세 › 포괄평가 계획수립',tipFrom='p1',who='원장님',say='"검사값을 또 일일이 쳐 넣어야 해요?"',rect=['hl','btn:EMR 결과 가져오기']))
    else:
        a.append(st(ids[2],'staff',23,'임상검사를 EMR에서 — <b>EMR 결과 가져오기</b>','오른쪽 위 버튼 줄',"'EMR 결과 가져오기 ▾'",WC,'환자 상세 › 포괄평가 계획수립',tipFrom='m3c',rect='btn:EMR 결과 가져오기'))
        a.append(st('m3d','staff',25,'문진만 먼저 — <b>문진 저장</b>','문진 내역 제목 줄 오른쪽',"'문진 저장'",WC,'환자 상세 › 포괄평가 계획수립',tipFrom='m3d',rect='btn:문진 저장'))
        a.append(st('m3e','staff',25,'<b>임상검사 저장</b>','임상검사 내역 제목 줄 오른쪽 끝',"'임상검사 저장'",WC,'환자 상세 › 포괄평가 계획수립',tipFrom='m3e',rect='btn:임상검사 저장'))
    a.append(st(ids[3],'staff',25,'<b>계획 수립 일자</b>를 오늘로','일만사 대상자 정보 상자 위쪽',"'계획 수립 일자' 달력 칸",WC,'환자 상세 › 포괄평가 계획수립',tip=('계획 수립 일자를 정하면 그날부터 1년이 관리 주기입니다.','주기는 계획수립일로부터 1년.')))
    a.append(st(ids[4],'staff',26,'심평원에 올리는 <b>임시저장</b>','오른쪽 위 파란 버튼',"'임시저장(심평원)'",WC,'환자 상세 › 포괄평가 계획수립',tipFrom='p5' if zone else 'm3f',who='원장님',say='"심평원에는 누가 올려요?"',ch='④ 심평원 작성완료' if zone else '③ 심평원 임시저장·작성완료'))
    a.append(st(ids[5],'staff',28,'작성완료하러 — <b>심평원 바로가기</b>','임시저장 옆 검은 버튼',"'심평원 바로가기'",WC,'환자 상세 › 포괄평가 계획수립',tip=('작성완료는 심평원에서만 됩니다. 오른쪽 위 심평원 바로가기로 바로 가요.','')))
    a.append(st(ids[6],'staff',29,'심평원 포괄평가 — <b>작성완료</b>','버튼 셋 중 오른쪽 끝',"'작성완료'",HI,'환자 관리 및 서비스 제공 › 포괄평가 및 계획수립',tipFrom='m3h'))
    a.append(st(ids[7],'staff',30,'심평원 창 <b>닫기</b>','오른쪽 위 검은 버튼',"'✕ 닫기'",HI,'환자 관리 및 서비스 제공 › 포괄평가 및 계획수립',tip=('작성완료가 끝났으니 창을 닫고 웰체크로 돌아갑니다.','')))
    a.append(st(ids[8],'staff',31,'환자께 드릴 <b>케어플랜 보고서</b> 출력','대상자 정보 상자 오른쪽',"검은 '케어플랜 출력하기'",WC,'환자 상세 › 포괄평가 계획수립',tipFrom='p6' if zone else 'm3g',rect='btn:케어플랜 출력하기'))
    return a
def edu(ids,zone):
    P='환자 상세 › 교육상담'; H='환자 관리 및 서비스 제공 › 교육 및 상담'
    a=[]
    a.append(st(ids[0],'edu',0,'교육상담 열의 <b>0/10</b>','박고당 행 · 교육상담 열',"교육상담 열의 '0/10'",WC,LIST,tipFrom='m4a',who='원장님',say='"교육상담은 어떻게 남겨요?"'))
    a.append(st(ids[1],'edu',1,'보낼 <b>교육자료</b>를 체크 (맨 위 영상)','목록 첫 줄 왼쪽','첫 번째 자료의 체크박스',WC,P,tip=('영상·이미지·PDF 중 환자에게 맞는 자료를 골라 담습니다.','')))
    a.append(st(ids[2],'edu',2,'바구니에 담았으면 <b>교육자료 발송</b>','오른쪽 발송바구니 아래',"파란 '교육자료 발송'",WC,P,tipFrom='m4b'))
    a.append(st(ids[3],'edu',3,'교육상담 <b>실시일자</b>를 오늘로','팝업 표 첫 칸',"'실시일자' 달력 칸",WC,P+' › 교육상담 반영내용',tip=('의사는 10분 이상, 의사 외(간호사·영양사 등)는 20분 이상 진행해야 인정됩니다.','팝업 상단 「교육상담 인정 기준」 문구.')))
    a.append(st(ids[4],'edu',4,'자료 발송 + 심평원 자료제출 — <b>발송</b>','팝업 맨 아래',"파란 '발송'",WC,P+' › 교육상담 반영내용',tip=('발송 한 번에 환자에게 교육자료가 가고, 교육상담 내역이 심평원에 임시저장됩니다.','팝업 하단 안내 문구.')))
    a.append(st(ids[5],'edu',6,'작성완료하러 <b>심평원으로</b>','팝업 오른쪽 파란 버튼',"'심평원 이동'",WC,P+' › 임시저장 완료 팝업',tipFrom='m4f'))
    a.append(st(ids[6],'edu',7,'작성완료할 교육 행을 <b>체크</b>','1차 행 맨 왼쪽','1차 행의 체크박스',HI,H,tip=('작성완료할 차수의 행을 먼저 체크합니다.','')))
    a.append(st(ids[7],'edu',8,'교육상담 <b>작성완료</b>','버튼 셋 중 오른쪽 끝',"'작성완료'",HI,H,tipFrom='m4g'))
    a.append(st(ids[8],'edu',9,'심평원 창 <b>닫기</b>','오른쪽 위 검은 버튼',"'✕ 닫기'",HI,H,tip=('작성완료가 끝났으니 창을 닫고 웰체크 대상자 목록으로 돌아갑니다.','')))
    return a
def chk(ids,zone):
    P='환자 상세 › 점검/평가'; H='환자 관리 및 서비스 제공 › 점검 및 평가'
    a=[]
    a.append(st(ids[0],'checkup',0,'점검·평가 산정 시점을 확인하고 <b>확인</b>','팝업 아래 파란 버튼',"'확인'",WC,LIST+' › 주의사항 팝업',tip=('점검·평가는 케어플랜 수립일로부터 4개월 이후, 연 2회 산정할 수 있습니다.','체험존 주의사항 팝업 문구.'),who='원장님',say='"점검평가는 언제부터 할 수 있어요?"'))
    a.append(st(ids[1],'checkup',1,'점검 평가 열의 <b>1차 대상</b>','박고당 행 맨 오른쪽 열',"점검 평가 열의 '1차 대상'",WC,LIST,tipFrom='m6a'))
    a.append(st(ids[2],'checkup',2,'환자에게 점검평가 <b>문진표 발송</b>','팝업 오른쪽 파란 버튼',"'문진표 발송'",WC,LIST+' › 1차 점검평가 대상 팝업',tipFrom='m6b'))
    a.append(st(ids[3],'checkup',3,'환자 앱 보라색 카드 — <b>지금 작성하기</b>','위쪽 보라색 카드',"보라 카드의 '지금 작성하기'",AP,'웰체크 앱 › 홈',tipFrom='m6c'))
    a.append(st(ids[4],'checkup',4,'문진 — 약 복용 여부에 <b>답하기</b>','예 / 아니오 중 하나',"'예' 또는 '아니오'",AP,'웰체크 앱 › 점검/평가 문진',tip=('환자가 예·아니오만 누르면 되는 간단한 문진입니다.',''),rect=['x:#btn-chk-med-yes','x:#btn-chk-med-no']))
    a.append(st(ids[5],'checkup',5,'답했으면 <b>다음</b>','화면 맨 아래 오른쪽',"'다음'",AP,'웰체크 앱 › 점검/평가 문진',tip=('답을 고르면 다음 버튼이 켜집니다.','')))
    a.append(st(ids[6],'checkup',6,'제출 완료 — <b>홈으로</b>','화면 맨 아래 버튼',"'홈으로'",AP,'웰체크 앱 › 문진 제출 완료',tip=('환자가 제출한 값은 웰체크 점검/평가표에 반영됩니다.','')))
    a.append(st(ids[7],'checkup',7,'1차 점검 <b>결과값</b> 채우기 (체험존은 한 번에)','세부 내역 제목 줄 오른쪽',"주황 '1차 점검 결과값 자동입력'",WC,P,tip=('고혈압은 혈압, 당뇨·복합은 당화혈색소까지 필수입니다.','약물 모니터링·중증사례·생활습관 목표·체중 필수. 자동입력은 체험존 실습용 버튼.')))
    a.append(st(ids[8],'checkup',9,'<b>1차 실시 일자</b>를 오늘로','세부 내역 표 왼쪽 위',"'1차 실시 일자' 달력 칸",WC,P,tip=('결과값을 넣었으면 1차 실시 일자를 정합니다.','')))
    a.append(st(ids[9],'checkup',10,'심평원에 올리는 <b>임시저장</b>','오른쪽 위 파란 버튼',"'임시저장'",WC,P,tipFrom='m6d'))
    a.append(st(ids[10],'checkup',13,'작성완료하러 — <b>심평원 바로가기</b>','임시저장 옆 검은 버튼',"'심평원 바로가기'",WC,P,tipFrom='m6e'))
    a.append(st(ids[11],'checkup',14,'심평원 점검/평가 — <b>작성완료</b>','버튼 셋 중 오른쪽 끝',"'작성완료'",HI,H,tipFrom='m6f'))
    a.append(st(ids[12],'checkup',15,'심평원 창 <b>닫기</b>','오른쪽 위 검은 버튼',"'✕ 닫기'",HI,H,tip=('작성완료가 끝났으니 창을 닫으면 점검·평가가 마무리됩니다.','')))
    return a
N=lambda p,n:[f'{p}{i}' for i in range(1,n+1)]
stages={}
# 체험존 코스
z0=st('zr0','staff',0,'혜택 3가지를 설명한 뒤 <b>심평원 환자 등록</b>으로','카드 아래 파란 버튼',"'심평원 환자 등록 시작 →'",ZN,'직원 › 환자 설득하기',tip=('본인부담금 30%→20%, 건강생활실천지원금 최대 8만원, 케어플랜 수립 선물 — 환자분께는 이 3가지만 말씀드리면 됩니다.','체험존 「환자 설득하기」 화면 문구 기준.'),who='원장님',say='"환자한테는 뭐라고 설명해요?"')
stages['reg']=[keep('r1'),z0]+reg_core(N('zr',6),True)
stages['plan']=invite(N('zi',5),True)+survey(N('zs',4),True)+careplan(N('zp',9),True)
stages['edu']=edu(N('ze',9),True)
stages['chk']=chk(N('zc',13),True)
# 웰체크 실무 코스
stages['m2']=reg_core(['m2g','m2g2','m2h','m2i','m2i2','m2j'],False)+invite(['m2k','m2l','m2m','m2n','m2o'],False)+[keep('m2a',ch='③ 초대문자 메뉴로 보내기'),keep('m2b'),keep('m2c'),keep('m2d'),keep('m2e'),keep('m2f')]
stages['m3']=survey(['m3b','m3b2','m3b3','m3b4'],False)+careplan(['m3a2','m3a','m3c','m3p','m3f','m3f2','m3h','m3h2','m3g'],False)+[keep('m3i')]
stages['m4']=edu(['m4a','m4a2','m4b','m4b2','m4b3','m4f','m4g1','m4g','m4g2'],False)+[keep('m4c',ch='그 밖에 — 수기 추가 · 환자 앱'),keep('m4d'),keep('m4e')]
stages['m6']=chk(['m6pre','m6a','m6b','m6c','m6c2','m6c3','m6c4','m6d0','m6d1','m6d','m6e','m6f','m6f2'],False)
for k in ('m2','m4','m6'):
    f=stages[k][0]
    if k!='m2' and 'ch' in f: pass
# ── 체험존 본 화면(experience.html) 새 레이아웃: 오프닝·EMR·건생 보드/좌표 갱신
X=json.load(open(f'{Z}/steps_exp.json',encoding='utf8'))
def XR(sc,k,pad=3,grow=None):
    r=list(X[sc][k])
    if grow: r[2]+=grow
    return pct(r,pad)
def ov(id,sc,k,pad=3,grow=None,**kw):
    d=dict(id=id,img=sc,rects=[XR(sc,k,pad,grow)]); d.update(kw); return d
ovr=[ov('o1','x01','zone'),ov('o2','x02','tour'),ov('o3y','x03','yes'),ov('o3n','x03','no'),ov('o4','x11','doc'),
 ov('e1','x13','won',hint='왼쪽 위 둥근 버튼 넷 중 첫 번째(₩)',chance='왼쪽 위 파란 ₩ 버튼'),ov('e1c','x15','close'),
 ov('e2','x13','point',hint='₩ 바로 오른쪽',chance='왼쪽 위 초록 P 버튼'),ov('e2c','x16','close'),
 ov('e3','x13','h0',pad=0),ov('e4','x13','h1',pad=0),ov('e5','x14','h2',pad=0),ov('e6','x13','h3',pad=0),
 ov('e7','x13','rev',hint='오른쪽 위 초록 버튼',chance='오른쪽 위 "수익 시뮬레이션"'),
 ov('e8','x18','slider',pad=10),ov('e9','x18','benefit',hint='오른쪽 위 파란 버튼'),ov('e10','x19','start',hint='오른쪽 위 파란 버튼'),
 ov('r1','x02','staff'),ov('h1','x02','hs'),ov('h2','x33','search'),ov('h3','x34','apply'),ov('h4','x34','menu'),ov('h5','x35','search'),
 ov('h6','x36','open'),ov('h7','x37','full'),ov('h8','x37','agree',pad=5,grow=42),ov('h9','x38','submit'),
 ov('h10','x36','end',hint='오른쪽 위 빨간 버튼',chance='오른쪽 위 "체험종료"')]
ins=[dict(after='e2c',st='emr',id='e2d',img='x13',who='원장님',say='"검사는 어떤 게 할인돼요?"',task='<b>검사 할인 목록</b>을 띄우세요',rects=[XR('x13','pct')],hint='P 바로 오른쪽',chance='왼쪽 위 보라 % 버튼',site='zone',path='체험존 › 검사 할인 목록',tip=dict(say='고혈압·당뇨 공통 검사와 질환별 검사가 할인 대상입니다. 연간 급여횟수가 정해진 검사는 그 횟수까지 적용돼요.',note='체험존 「일차의료만성질환 검사 할인 목록」 팝업 기준.')),
     dict(after='e2d',st='emr',id='e2e',img='x17',who='',task='할인 목록을 설명한 뒤 <b>닫으세요</b>',rects=[XR('x17','close')],hint='팝업 오른쪽 위',chance='보라 헤더의 ✕',site='zone',path='체험존 › 검사 할인 목록',tip=dict(say='상병별로 어떤 검사 코드가 할인되는지 표로 보여드리고 닫습니다.',note=''))]
ximgs=sorted({d['img'] for d in ovr+ins})
for k in ximgs:
    Image.open(f'{Z}/shots/{k}.png').convert('RGB').save(f'{HERE}/img/sim/{k}.webp','WEBP',quality=84,method=6)
imgs=sorted({d['img'] for l in stages.values() for d in l if 'img' in d})
os.makedirs(f'{HERE}/img/sim',exist_ok=True)
for k in imgs:
    m={'sa':'staff','se':'edu','sc':'checkup'}[k[:2]]; i=int(k[2:])
    out=f'{HERE}/img/sim/{k}.webp'
    Image.open(f'{Z}/shots/z_{m}_{i:02d}.png').convert('RGB').save(out,'WEBP',quality=84,method=6)
data=json.dumps(dict(imgs=imgs+ximgs,stages=stages,ovr=ovr,ins=ins),ensure_ascii=False,separators=(',',':'))
js='''/* ── v61 · 체험존 「웰체크 시뮬레이터」 화면으로 교체: 체험존 S2~S5 + 웰체크 실무 M2·M3·M4·M6 (gen_sim.py 생성물 — 직접 고치지 말 것) ── */
(function(){
  const D=%s;
  D.imgs.forEach(k=>{ IMG[k]='img/sim/'+k+'.webp'; IMGA[k]=2562/1350; });
  if(!STAGES.find(s=>s.id==='edu')){ const hi=STAGES.findIndex(s=>s.id==='hs');
    STAGES.splice(hi,0,{ id:'edu', course:'zone', n:4, title:'교육상담', sub:'교육자료 발송 · 실시일자 · 심평원 작성완료', color:'#b06cff' },{ id:'chk', course:'zone', n:5, title:'점검·평가', sub:'문진표 발송 · 환자 앱 문진 · 결과값 · 심평원 작성완료', color:'#7c5cff' });
    const hS=STAGES.find(s=>s.id==='hs'); if(hS) hS.n=6; }
  const pS=STAGES.find(s=>s.id==='plan'); if(pS) pS.sub='앱 초대 · 환자 앱 문진 · 검사/계획수립 · 심평원 작성완료';
  const rS=STAGES.find(s=>s.id==='reg'); if(rS) rS.sub='환자 설득 3가지 · 심평원 포털 대상자 등록 · 환자 불러오기';
  const byId=id=>STEPS.find(s=>s.id===id);
  const mk=(st,d)=>{ if(d.keep){ const o=byId(d.keep); if(d.ch) o.ch=d.ch; return o; }
    const src=d.tipFrom&&byId(d.tipFrom); const tip=d.tip||(src&&src.tip)||{say:'',note:''};
    const o={ st, id:d.id, img:d.img, who:d.who||'', task:d.task, rects:d.rects.map(r=>R(r[0],r[1],r[2],r[3])), hint:d.hint, chance:d.chance, tip:JSON.parse(JSON.stringify(tip)), site:d.site, path:d.path };
    if(d.say) o.say=d.say; if(d.ch) o.ch=d.ch; return o; };
  D.ovr.forEach(o=>{ const s=byId(o.id); if(!s) return; s.img=o.img; s.rects=o.rects.map(r=>R(r[0],r[1],r[2],r[3])); ['hint','chance','task'].forEach(k=>{ if(o[k]) s[k]=o[k]; }); });
  D.ins.forEach(d=>{ if(byId(d.id)) return; const at=STEPS.indexOf(byId(d.after)); if(at<0) return; const o=Object.assign({},d,{rects:d.rects.map(r=>R(r[0],r[1],r[2],r[3]))}); delete o.after; if(!o.say) delete o.say; STEPS.splice(at+1,0,o); });
  const order=['reg','plan','edu','chk','m2','m3','m4','m6'];
  const built={}; order.forEach(st=>{ built[st]=D.stages[st].map(d=>mk(st,d)).filter(Boolean); });
  let prev=null;
  order.forEach(st=>{ const old=STEPS.filter(s=>s.st===st); let at;
    if(old.length) at=STEPS.indexOf(old[0]); else { const p=STEPS.filter(s=>s.st===prev); at=STEPS.indexOf(p[p.length-1])+1; }
    old.forEach(o=>STEPS.splice(STEPS.indexOf(o),1)); STEPS.splice(at,0,...built[st]); prev=st; });
  try{ if(typeof QCARDS!=='undefined'&&Array.isArray(QCARDS)) QCARDS.forEach(q=>{ if(!byId(q.after)){ const l=STEPS.filter(s=>s.st===q.st); if(l.length) q.after=l[l.length-1].id; } }); }catch(e){}
})();
''' % data
open(f'{HERE}/parts/course_sim.js','w',encoding='utf8').write(js)
print('imgs',len(imgs),'steps',{k:len(v) for k,v in stages.items()},'js',len(js))

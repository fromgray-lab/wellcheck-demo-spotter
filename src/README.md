# 틀린시연찾기 — 소스

- 빌드: `python3 src/game/build.py && python3 src/make_site.py` → 저장소 루트 `index.html`·`sw.js` 갱신
- `src/game/build.py`가 `demo-spotter.v5.html` + `parts/*` + `build_v8~v32.py`를 조립하고 `lint.js`(Playwright)로 전수 검사
- 이미지·BGM은 루트 `img/`·`bgm/` (src/game/img, bgm은 심볼릭 링크). 새 이미지 폴더는 `make_site.py`의 목록 튜플에도 추가
- 스테이지 콘텐츠: `parts/course_manual.js`(실무 M0~M8) · `course_ysr.js`(M9 의사랑) · `course_dh.js`(M10 리브레·M11 카트비피) · `fix_zone4.py`(체험존) · 원장님 질문 `parts/qcards.json` · 사이트 경로 `parts/sites.js`
- 시트 저장소 Apps Script: `src/sheets/` (배포 액세스 = **모든 사용자** 필수)

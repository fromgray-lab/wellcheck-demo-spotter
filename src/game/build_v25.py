# v25: 타이틀 크레딧에 버전 표기 (업데이트 노트의 첫 항목에서 자동)  (build.py가 exec, build_v24 뒤)
import re as _re2
_m = _re2.search(r"<li><b>(v\d+)</b>", parts('changelog.html'))
_ver = _m.group(1) if _m else ''
src = rep(src, '<div class="credit">틀린시연찾기 · 공식 메뉴얼 + 체험존 기반 · 신사업전략팀</div>', '<div class="credit">틀린시연찾기 · 공식 메뉴얼 + 체험존 기반 · 신사업전략팀 · <span id="verTag" title="업데이트 노트는 게임방법 안에">%s</span></div>' % _ver)

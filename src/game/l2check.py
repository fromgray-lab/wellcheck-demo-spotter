"""L2 점검: 스텝이 실제로 쓰는 보드의 가로 픽셀과 '실제 선명도'를 잰다.
사용: node src/game/dump_steps.js 경로/steps.json && python3 src/game/l2check.py 경로/steps.json
선명도 = 원본과 '½ 축소 후 다시 확대한 사본'의 평균 밝기 차. 작을수록 원래부터 흐린(작은 원본을 키운) 보드.
체험존 시뮬레이터 2배 렌더(sa*/sc*/x*)는 0.4~0.9로 낮게 나와도 선명하다 — 숫자는 후보 추리기용, 판정은 이미지를 직접 보고 한다."""
import json, sys
from PIL import Image, ImageChops, ImageStat
d = json.load(open(sys.argv[1])); G = 'src/game/'
use = {}
for s in d['steps']: use.setdefault(s['img'], []).append(s['st'] + '/' + s['id'])
rows = []
for k, f in d['IMG'].items():
    if k not in use: continue
    im = Image.open(G + f).convert('L'); w, h = im.size
    sm = im.resize((w // 2, h // 2), Image.LANCZOS).resize((w, h), Image.LANCZOS)
    rows.append((k, w, h, round(ImageStat.Stat(ImageChops.difference(im, sm)).mean[0], 2), use[k]))
print('사용 중 보드', len(rows), '/ IMG', len(d['IMG']))
print('-- 가로 1200px 미만');  [print(' ', r[0], f'{r[1]}x{r[2]}', r[3], r[4]) for r in rows if r[1] < 1200]
print('-- 선명도 낮은 순 10'); [print(' ', r[0], f'{r[1]}x{r[2]}', r[3], r[4]) for r in sorted(rows, key=lambda r: r[3])[:10]]

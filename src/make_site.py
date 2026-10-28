#!/usr/bin/env python3
"""game/demo-spotter.html → site/index.html (+ sw.js 자산 목록·버전) — GitHub Pages 배포용"""
import os, re, hashlib, json
R=os.path.dirname(os.path.abspath(__file__)); G=os.path.join(R,'game'); S=os.path.dirname(R)
body=open(os.path.join(G,'demo-spotter.html'),encoding='utf-8').read()
head=('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
      '<meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#1d2140">'
      '<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="apple-touch-icon.png">'
      '<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
      '<meta name="apple-mobile-web-app-title" content="틀린시연찾기">'
      '<meta name="description" content="웰체크 자유자재 시연 MR 양성소 — 실제 화면에서 틀린 클릭을 찾아내는 시연 훈련 게임">'
      '<meta property="og:type" content="website"><meta property="og:title" content="틀린시연찾기 · 웰체크 시연 MR 양성소">'
      '<meta property="og:description" content="실제 화면으로 웰체크 시연을 연습하고, 원장님 질문까지 막힘 없이.">'
      '<meta property="og:url" content="https://fromgray-lab.github.io/wellcheck-demo-spotter/"><meta property="og:image" content="https://fromgray-lab.github.io/wellcheck-demo-spotter/og.jpg">'
      '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
      '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://fromgray-lab.github.io/wellcheck-demo-spotter/og.jpg">')
open(os.path.join(S,'index.html'),'w',encoding='utf-8').write('<!doctype html><html lang="ko"><head>'+head+'</head><body>'+body+'</body></html>')
assets=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png','apple-touch-icon.png']
for d in ('img','img/m','img/hd','img/ysr','img/dh','bgm'):
    for f in sorted(os.listdir(os.path.join(S,d))):
        p=os.path.join(S,d,f)
        if os.path.isfile(p): assets.append(d+'/'+f)
ver=hashlib.sha1(body.encode()).hexdigest()[:10]
sw=open(os.path.join(R,'sw.tpl.js'),encoding='utf-8').read().replace('__VER__',ver).replace('__ASSETS__',json.dumps(assets))
open(os.path.join(S,'sw.js'),'w',encoding='utf-8').write(sw)
print('site ok', ver, len(assets),'assets')

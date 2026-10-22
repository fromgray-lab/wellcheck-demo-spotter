/* 틀린시연찾기 오프라인 서비스워커 — make_site.py가 버전·자산 목록을 채움 */
const VER='dsg-__VER__'; const ASSETS=__ASSETS__;
self.addEventListener('install', e=>{ e.waitUntil(caches.open(VER).then(c=>Promise.all(ASSETS.map(a=>c.add(new Request(a,{cache:'reload'})).catch(()=>null)))).then(()=>self.skipWaiting())); });
self.addEventListener('activate', e=>{ e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith('dsg-')&&k!==VER).map(k=>caches.delete(k)))).then(()=>self.clients.claim())); });
self.addEventListener('fetch', e=>{ const u=new URL(e.request.url); if(e.request.method!=='GET'||u.origin!==location.origin) return; /* 구글 시트·폰트 등 외부는 손대지 않음 */
  const isPage=e.request.mode==='navigate'||u.pathname.endsWith('/')||u.pathname.endsWith('index.html');
  if(isPage){ /* 화면: 네트워크 우선(업데이트 반영), 끊기면 캐시 */
    e.respondWith(fetch(e.request).then(r=>{ const cp=r.clone(); caches.open(VER).then(c=>c.put('index.html',cp)); return r; }).catch(()=>caches.match('index.html').then(r=>r||caches.match('./')))); return; }
  /* 이미지·BGM: 캐시 우선 */
  e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request).then(res=>{ if(res.ok){ const cp=res.clone(); caches.open(VER).then(c=>c.put(e.request,cp)); } return res; }))); });

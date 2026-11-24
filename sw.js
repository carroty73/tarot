// 서비스 워커(web_common_gen.py가 만든 파일이라 직접 고치지 않는다).
// 크롬이 "앱 설치"를 띄우려면 fetch를 처리하는 서비스 워커가 필요하다.
// 항상 네트워크를 먼저 쓰고(옛 화면이 남는 문제를 막기 위해), 안 될 때만 저장본을 보여 준다.
// 저장하는 것은 페이지 이동과 SHELL 파일뿐이다.
const CACHE = "site-shell-v1";
const SHELL = ["./", "manifest.json", "assets/img/icon/app-icon-180.png?v=f1402621", "assets/img/icon/app-icon-192.png?v=c8f34690", "assets/img/icon/app-icon-512.png?v=816b0a0d", "assets/img/icon/app-icon-maskable-512.png?v=816b0a0d"];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  // 페이지 이동과 위의 SHELL 파일만 다룬다(이미지, 영상 같은 큰 파일은 저장하지 않는다).
  const inShell = SHELL.some((p) => new URL(p, self.registration.scope).href === url.href);
  if (req.mode !== "navigate" && !inShell) return;
  e.respondWith(
    fetch(req).then((res) => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req).then((hit) => hit || caches.match("./")))
  );
});

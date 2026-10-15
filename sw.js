/* TRB service worker: makes the game load instantly and work offline.
   Bump V whenever you deploy a new version so phones pick up the update. */
const V = 'trb-v3';
const CORE = [
  './', 'index.html', 'manifest.webmanifest',
  'vendor/three.min.js',
  'fonts/bricolage-400.woff2', 'fonts/bricolage-600.woff2',
  'icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png',
  'icons/apple-touch-icon.png', 'icons/favicon-32.png', 'icons/icon.svg'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(V).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== V).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;

  // page loads: network first (so updates arrive), cached copy when offline
  if (req.mode === 'navigate') {
    e.respondWith(
      fetch(req)
        .then(res => { const copy = res.clone(); caches.open(V).then(c => c.put('index.html', copy)); return res; })
        .catch(() => caches.match('index.html'))
    );
    return;
  }

  // everything else: serve from cache instantly, refresh it in the background
  e.respondWith(
    caches.match(req).then(hit => {
      const net = fetch(req)
        .then(res => { if (res.ok) { const copy = res.clone(); caches.open(V).then(c => c.put(req, copy)); } return res; })
        .catch(() => hit);
      return hit || net;
    })
  );
});

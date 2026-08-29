/* MEXC Position Calculator — service worker.
 *
 * Makes the app load instantly and work offline (shows last-known data).
 * Caches the app shell (same-origin GETs) cache-first; the Cloudflare Worker
 * relay calls (cross-origin, MEXC live data) are left network-only so you
 * always get live data when online.
 *
 * Register this file from index.html. GitHub Pages serves over HTTPS, which
 * is required for service workers to activate. When you update the app,
 * bump the version below (e.g. mexc-calc-v2) so phones drop the old cache.
 */
const CACHE = 'mexc-calc-v1';
const APP_SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => c.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  const isSameOrigin = url.origin === location.origin;
  const isGet = e.request.method === 'GET';
  const isApi = url.pathname.startsWith('/api/'); // (unused on mobile; safety)

  // Only handle same-origin GETs for the app shell. Worker relay + cross-origin
  // requests always go straight to the network.
  if (!isSameOrigin || !isGet || isApi) return;

  e.respondWith(
    caches.match(e.request).then((cached) => {
      if (cached) return cached;
      return fetch(e.request).then((resp) => {
        const clone = resp.clone();
        caches.open(CACHE).then((c) => c.put(e.request, clone));
        return resp;
      });
    })
  );
});

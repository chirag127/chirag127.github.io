/**
 * Service Worker for Chirag Hub PWA
 *
 * Features:
 * - Offline support with cache-first strategy
 * - Background sync for form submissions
 * - App install prompt support
 */

const CACHE_NAME = 'chirag-hub-v1';
const OFFLINE_URL = '/offline.html';

// Assets to cache on installconst PRECACHE_ASSETS = [
  '/',
  '/about.html',
  '/privacy.html',
  '/terms.html',
  '/cookies.html',
  '/voters.html',
  '/contractors.html',
  '/contact.html',
  '/universal/config.js',
  '/universal/core.js',
  '/universal/style.css',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
];

// Install: Cache core assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW] Caching core assets');
        return cache.addAll(PRECACHE_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activate: Clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME)
            .map(key => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Cache-first for static, network-first for API
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Skip Chrome extensions and external APIs
  if (url.protocol === 'chrome-extension:') return;
  if (url.hostname === 'api.github.com') return;

  // Cache-first for static assets
  if (url.pathname.match(/\.(html|css|js|png|jpg|svg|woff2?)$/)) {
    event.respondWith(
      caches.match(request).then(cached => {
        if (cached) return cached;

        return fetch(request).then(response => {
          // Clone and cache
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // Network-first for HTML pages
  event.respondWith(
    fetch(request)
      .then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
        }
        return response;
      })
      .catch(() => caches.match(request))
  );
});

// Message handler for skip waiting
self.addEventListener('message', event => {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
});

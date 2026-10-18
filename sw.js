const CACHE_NAME = 'asad-tech-v73';
const ASSETS = [
  './',
  './index.html',
  './manifest.json'
];

// Install: Save files to cache
self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

// Activate: Clean up old caches and take control immediately
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Serve from cache first, fallback to network
self.addEventListener('fetch', (e) => {
  // Only handle GET requests
  if (e.request.method !== 'GET') return;

  e.respondWith(
    caches.match(e.request).then((response) => {
      if (response) {
        return response; // Return from cache
      }
      
      // If not in cache, try network
      return fetch(e.request).then((networkResponse) => {
        // If network works, cache the new file for next time
        return caches.open(CACHE_NAME).then((cache) => {
          cache.put(e.request, networkResponse.clone());
          return networkResponse;
        });
      }).catch(() => {
        // If offline AND not in cache, fallback to index.html
        return caches.match('./index.html');
      });
    })
  );
});

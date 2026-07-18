const CACHE_NAME = 'estawredly-cache-v1';
const urlsToCache = [
  './',
  './index.html',
  './shop.html',
  './product.html',
  './checkout.html',
  './style.css',
  './enhancements.css',
  './main.js',
  './store.js',
  './products_db.js',
  './enhancements.js',
  './logo.jpg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});

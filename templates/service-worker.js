// Bump this version number each time a cached or asset changes.
// If you don't, the SW won't be reinstalled and the pages you cache initially won't be updated
// (by default at least, see next sections for more on caching).
const VERSION = '{{ version }}';

var cacheName = 'djangopwa-v2';

var filesToCache = [
    '/',                // index.html
    normalizeUrl(),
];
self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(cacheName)
            .then(function (cache) {
                console.info('[sw.js] cached all files');
                console.info(VERSION);
                return cache.addAll(filesToCache);
            })
    );
});

self.addEventListener('fetch', function (event) {
    event.respondWith(
        // Try the network

        fetch(event.request)
            .then(function (res) {

                var reqCopy = event.request.clone();
                var resCopy = res.clone();
                return caches.open(cacheName)
                    .then(function (cache) {
                        // Put in cache if succeeds
                        cache.put(reqCopy.url, resCopy);
                        return res;
                    })
            })
            .catch(function (err) {
                // Fallback to cache
                return caches.match(event.request);
            })
    );
});
// self.addEventListener('fetch', function (event) {
//     event.respondWith(
//         caches.match(event.request)
//             .then(function (response) {
//                 if (response) {
//                     return response
//                 } else {
//                     // clone request stream
//                     // as stream once consumed, can not be used again
//                     var reqCopy = event.request.clone();
//
//                     return fetch(reqCopy, {credentials: 'include'}) // reqCopy stream consumed
//                         .then(function (response) {
//                             // bad response
//                             // response.type !== 'basic' means third party origin request
//                             if (!response || response.status !== 200 || response.type !== 'basic') {
//                                 caches.open(cacheName)
//                                     .then(function (cache) {
//
//                                         var resCopy = response.clone();
//                                         console.log("Cache put");
//                                         return cache.put(reqCopy, response); // reqCopy, resCopy streams consumed
//                                     });
//                                 console.log("response stream consumed");
//                                 return response; // response stream consumed
//                             }
//                             // clone response stream
//                             // as stream once consumed, can not be used again
//
//
//                             // ================== IN BACKGROUND ===================== //
//
//                             // add response to cache and return response
//                             caches.open(cacheName)
//                                 .then(function (cache) {
//
//                                     console.log("Cache put");
//                                     return cache.put(reqCopy, resCopy); // reqCopy, resCopy streams consumed
//                                 });
//
//                             // ====================================================== //
//
//
//                             console.log("Response final");
//                             return response; // response stream consumed
//
//                         })
//                 }
//             })
//     );
// });

function normalizeUrl() {
    let reg = self.registration.scope.split("/")[4].toString();

    const regurl = `{% url 'manifest' 9999 %}`.replace(/9999/, reg);
    return regurl
}

self.addEventListener('activate', (event) => {
    var cacheKeeplist = [cacheName];

    event.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if (cacheKeeplist.indexOf(key) === -1) {
                    return caches.delete(key);
                }
            }));
        })
    );
});

//     this.addEventListener('fetch', function (event) {
//     // it can be empty if you just want to get rid of that error
// });

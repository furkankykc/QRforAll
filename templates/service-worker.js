// Bump this version number each time a cached or asset changes.
// If you don't, the SW won't be reinstalled and the pages you cache initially won't be updated
// (by default at least, see next sections for more on caching).
const VERSION = '{{ version }}';

var cacheName = 'djangopwa-v1';

var filesToCache = [
    '/',                // index.html
    normalizeUrl(),
];
self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(cacheName)
            .then(function (cache) {
                console.info('[sw.js] cached all files');
                return cache.addAll(filesToCache);
            })
    );
});


self.addEventListener('fetch', function (event) {
    event.respondWith(
        caches.match(event.request)
            .then(function (response) {
                if (response) {
                    return response
                } else {
                    // clone request stream
                    // as stream once consumed, can not be used again
                    var reqCopy = event.request.clone();

                    return fetch(reqCopy, {credentials: 'include'}) // reqCopy stream consumed
                        .then(function (response) {
                            // bad response
                            // response.type !== 'basic' means third party origin request
                            if (!response || response.status !== 200 || response.type !== 'basic') {
                                return response; // response stream consumed
                            }

                            // clone response stream
                            // as stream once consumed, can not be used again
                            var resCopy = response.clone();


                            // ================== IN BACKGROUND ===================== //

                            // add response to cache and return response
                            caches.open(cacheName)
                                .then(function (cache) {
                                    return cache.put(reqCopy, resCopy); // reqCopy, resCopy streams consumed
                                });

                            // ====================================================== //


                            return response; // response stream consumed
                        })
                }
            })
    );
});

function normalizeUrl() {
    let reg = self.registration.scope.split("/")[4].toString();

    const regurl =`{% url 'manifest' 9999 %}`.replace(/9999/, reg);
    return regurl
}


//     this.addEventListener('fetch', function (event) {
//     // it can be empty if you just want to get rid of that error
// });

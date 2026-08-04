/* AI工具箱 — Service Worker
 * 策略（v2 修正）：
 *  - 页面导航（navigation）：network-first，失败回退缓存，再回退首页
 *  - 静态资源（JS/CSS/图片/字体）：network-first，成功即更新缓存，失败回退缓存
 *    —— 这样每次修改代码后用户刷新都能拿到最新版本，避免被旧缓存锁死
 *  - PRECACHE 覆盖全部工具页与 JS，首访即缓存正确版本
 *  - CACHE 版本号已 bump（v1 → v2），旧缓存会被 activate 清除
 */
const CACHE = 'aifunnyplay-v4';
const PRECACHE = [
  'index.html',
  'tools.html',
  'about.html',
  'links.html',
  'contact.html',
  'privacy.html',
  'disclaimer.html',
  'sitemap.html',
  '404.html',
  'manifest.json',
  'favicon.svg',
  'icon-192.png',
  'icon-512.png',
  'icon-maskable-192.png',
  'icon-maskable-512.png',
  'assets/css/style.css',
  'assets/js/site.js',
  'assets/js/tools.js',
  'assets/js/qrcode.js',
  'assets/js/tools-new.js',
  'assets/js/tools-v2.js',
  'assets/js/zh-map.js',
  'tools/qrcode.html',
  'tools/image-compress.html',
  'tools/art-text.html',
  'tools/watermark.html',
  'tools/date-calc.html',
  'tools/unit-convert.html',
  'tools/color-convert.html',
  'tools/text-diff.html',
  'tools/mortgage.html',
  'tools/bmi.html',
  'tools/base-convert.html',
  'tools/word-count.html',
  'tools/json-formatter.html',
  'tools/base64-convert.html',
  'tools/url-encode.html',
  'tools/timestamp-convert.html',
  'tools/password-generator.html',
  'tools/uuid-generator.html',
  'tools/md5-hash.html',
  'tools/zh-convert.html',
  'tools/md-to-html.html',
  'tools/image-convert.html',
  'tools/age-calc.html',
  'tools/nine-grid.html',
  'tools/regex-tester.html',
  'tools/tax-calc.html',
  'tools/timezone-convert.html',
  'assets/js/tools-v3.js'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return c.addAll(PRECACHE).catch(function () { /* 个别资源缺失不阻断安装 */ });
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE) return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;

  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // 跨域直接放行

  if (req.mode === 'navigate') {
    // 页面：先网络，失败回退缓存，再回退首页
    e.respondWith(
      fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
        return res;
      }).catch(function () {
        return caches.match(req).then(function (r) { return r || caches.match('index.html'); });
      })
    );
    return;
  }

  // 静态资源：network-first（保证更新可达），成功更新缓存，失败回退缓存
  e.respondWith(
    fetch(req).then(function (res) {
      if (res && res.status === 200 && res.type === 'basic') {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
      }
      return res;
    }).catch(function () {
      return caches.match(req).then(function (r) { return r || caches.match('index.html'); });
    })
  );
});

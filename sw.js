/* AI工具箱 — Service Worker
 * 策略（v2 修正）：
 *  - 页面导航（navigation）：network-first，失败回退缓存，再回退首页
 *  - 静态资源（JS/CSS/图片/字体）：network-first，成功即更新缓存，失败回退缓存
 *    —— 这样每次修改代码后用户刷新都能拿到最新版本，避免被旧缓存锁死
 *  - PRECACHE 覆盖全部工具页与 JS，首访即缓存正确版本
 *  - CACHE 版本号已 bump（v1 → v2），旧缓存会被 activate 清除
 */
const CACHE = 'aifunnyplay-v8';
const PRECACHE = [
  'index.html',
  'tools.html',
  'changelog.html',
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
  'tools/fuel-cost.html',
  'tools/due-date.html',
  'tools/random-generator.html',
  'tools/meme-maker.html',
  'tools/image-pixelate.html',
  'tools/id-photo.html',
  'tools/relative-calc.html',
  'tools/solar-term.html',
  'assets/js/tools-v3.js',
  'assets/js/tools-v4.js',
  'assets/js/tools-v5.js',
  'ai-background-remover-api-for-developers.html',
  'ai-chatbot-for-small-business-customer-service.html',
  'ai-code-assistant-vs-github-copilot-alternative.html',
  'ai-data-analysis-tool-for-excel-beginners.html',
  'ai-email-writer-chrome-extension-gmail.html',
  'ai-image-generator-for-ecommerce-product-photos.html',
  'ai-logo-maker-for-startups-free-trial.html',
  'ai-music-generator-royalty-free-commercial-use.html',
  'ai-paraphrasing-tool-to-avoid-plagiarism.html',
  'ai-pdf-summarizer-for-research-papers.html',
  'ai-presentation-maker-templates-guide.html',
  'ai-presentation-maker-with-templates.html',
  'ai-resume-builder-with-ats-optimization.html',
  'ai-seo-tool-for-keyword-research-affiliate.html',
  'ai-transcription-software-for-podcasters-comparison.html',
  'best-ai-photo-enhancer-for-real-estate.html',
  'best-ai-voice-generator-for-youtube-videos.html',
  'best-ai-writing-tools-for-bloggers-2025.html',
  'cheap-ai-content-detector-for-teachers.html',
  'free-ai-video-editor-no-watermark.html',
  'category/ai-writing.html',
  'category/ai-image.html',
  'category/ai-video-audio.html',
  'category/ai-office.html',
  'category/ai-marketing.html',
  'category/ai-review.html',
  'tag/index.html',
  'robots.txt'
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

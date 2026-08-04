/*! AI工具箱 - 站点交互增强（返回顶部 / 跳转链接 / 导航高亮 / 阅读进度）
 *  纯原生 JS，无依赖，defer 加载，不影响首屏渲染。
 */
(function () {
  'use strict';

  // 1) 返回顶部按钮
  var topBtn = document.createElement('button');
  topBtn.className = 'back-to-top';
  topBtn.setAttribute('aria-label', '返回顶部');
  topBtn.innerHTML = '&#8593;';
  topBtn.type = 'button';
  document.body.appendChild(topBtn);

  function onScroll() {
    if (window.scrollY > 400) topBtn.classList.add('show');
    else topBtn.classList.remove('show');
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  topBtn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // 2) 导航当前项高亮
  var path = location.pathname.replace(/index\.html$/, '').replace(/\/+$/, '') || '/';
  document.querySelectorAll('nav a').forEach(function (a) {
    var href = (a.getAttribute('href') || '').replace(/index\.html$/, '').replace(/\/+$/, '');
    if (!href) return;
    if (href === '/' ? path === '/' : path.indexOf(href) === 0) {
      a.classList.add('active');
      a.setAttribute('aria-current', 'page');
    }
  });

  // 3) 阅读进度条（仅文章页）
  if (document.querySelector('.article-content')) {
    var bar = document.createElement('div');
    bar.className = 'reading-progress';
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('aria-label', '阅读进度');
    document.body.appendChild(bar);
    function progress() {
      var d = document.documentElement;
      var st = d.scrollTop || document.body.scrollTop;
      var sh = d.scrollHeight - d.clientHeight;
      bar.style.width = (sh > 0 ? (st / sh) * 100 : 0) + '%';
    }
    window.addEventListener('scroll', progress, { passive: true });
    progress();
  }

  // 4) 广告启用辅助函数（预留，暂不启用）
  //    上线广告时调用 enableAds() 可一键显示所有广告位（如需默认隐藏占位框）。
  window.enableAds = function () {
    document.body.classList.remove('no-ads');
  };
  window.disableAds = function () {
    document.body.classList.add('no-ads');
  };

  // 5) 移动端汉堡菜单（注入按钮，不改动 HTML 结构）
  var hdr = document.querySelector('.site-header .container');
  var navEl = hdr && hdr.querySelector('nav');
  if (hdr && navEl) {
    var toggle = document.createElement('button');
    toggle.className = 'nav-toggle';
    toggle.setAttribute('aria-label', '打开导航菜单');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.innerHTML = '<span></span><span></span><span></span>';
    hdr.insertBefore(toggle, navEl);
    toggle.addEventListener('click', function () {
      var open = navEl.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? '关闭导航菜单' : '打开导航菜单');
    });
    navEl.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        navEl.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // 6) 深色模式切换（记忆偏好 + 跟随系统）
  var themeBtn = document.createElement('button');
  themeBtn.className = 'theme-toggle';
  themeBtn.setAttribute('aria-label', '切换深色 / 浅色模式');
  themeBtn.type = 'button';
  if (hdr) hdr.appendChild(themeBtn);

  function applyTheme(dark) {
    if (dark) {
      document.documentElement.setAttribute('data-theme', 'dark');
      themeBtn.textContent = '☀️';
    } else {
      document.documentElement.removeAttribute('data-theme');
      themeBtn.textContent = '🌙';
    }
  }
  var saved = null;
  try { saved = localStorage.getItem('theme'); } catch (e) {}
  var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(saved ? saved === 'dark' : prefersDark);
  themeBtn.addEventListener('click', function () {
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    var next = !isDark;
    applyTheme(next);
    try { localStorage.setItem('theme', next ? 'dark' : 'light'); } catch (e) {}
  });

  // 7) PWA Service Worker 注册（仅安全上下文：https 或 localhost）
  if ('serviceWorker' in navigator) {
    var swReady = function () {
      navigator.serviceWorker.register('sw.js').catch(function (err) {
        if (window.console) console.warn('SW register skipped/failed:', err);
      });
    };
    if (document.readyState === 'complete') swReady();
    else window.addEventListener('load', swReady);
  }

  // 8) 工具收藏（首页卡片 ☆ / ★，localStorage 持久化，收藏的工具显示为星标）
  var FAV_KEY = 'aihub_favs';
  function getFavs() {
    try { return JSON.parse(localStorage.getItem(FAV_KEY)) || []; } catch (e) { return []; }
  }
  function setFavs(arr) {
    try { localStorage.setItem(FAV_KEY, JSON.stringify(arr)); } catch (e) {}
  }
  function cardSlug(card) {
    var href = card.getAttribute('href') || '';
    var m = href.match(/tools\/([a-z0-9-]+)\.html/);
    return m ? m[1] : '';
  }
  var hubCards = document.querySelectorAll('.hub-card');
  if (hubCards.length) {
    var favs = getFavs();
    var favBtn = null;
    hubCards.forEach(function (card) {
      var slug = cardSlug(card);
      if (!slug) return;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'fav-btn' + (favs.indexOf(slug) !== -1 ? ' faved' : '');
      btn.setAttribute('aria-label', '收藏此工具');
      btn.setAttribute('title', favs.indexOf(slug) !== -1 ? '取消收藏' : '收藏此工具');
      btn.innerHTML = favs.indexOf(slug) !== -1 ? '★' : '☆';
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var arr = getFavs();
        var i = arr.indexOf(slug);
        if (i !== -1) { arr.splice(i, 1); btn.classList.remove('faved'); btn.innerHTML = '☆'; btn.setAttribute('title', '收藏此工具'); }
        else { arr.push(slug); btn.classList.add('faved'); btn.innerHTML = '★'; btn.setAttribute('title', '取消收藏'); }
        setFavs(arr);
        if (window.sortFavs) window.sortFavs();
      });
      card.appendChild(btn);
    });
  }

  // 9) 工具页「复制结果」按钮（计算器/转换类工具，运行时注入，不改 HTML 结构）
  //    结果容器 id 与页面 slug 映射；容器为空时给出提示，不产生无效复制。
  var COPY_TARGETS = {
    'age-calc': ['ac-result'],
    'base-convert': ['bc-output'],
    'bmi': ['bmi-output'],
    'date-calc': ['dc-diff-out', 'dc-calc-out'],
    'due-date': ['dd-result'],
    'fuel-cost': ['fc-result'],
    'mortgage': ['mg-output'],
    'regex-tester': ['rt-output'],
    'relative-calc': ['rc-result'],
    'solar-term': ['st-list'],
    'tax-calc': ['tc-result'],
    'text-diff': ['td-output'],
    'timestamp-convert': ['ts-output'],
    'timezone-convert': ['tz-list'],
    'unit-convert': ['uc-result'],
    'word-count': ['wc-stats']
  };
  (function () {
    var slugM = (location.pathname || '').match(/tools\/([a-z0-9-]+)\.html/);
    if (!slugM) return;
    var targets = COPY_TARGETS[slugM[1]];
    if (!targets || !targets.length) return;

    function copyPlain(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        return navigator.clipboard.writeText(text).catch(function () { return legacyCopy(text); });
      }
      return legacyCopy(text);
    }
    function legacyCopy(text) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) {}
      document.body.removeChild(ta);
      return ok ? Promise.resolve() : Promise.reject(new Error('copy failed'));
    }

    targets.forEach(function (id) {
      var box = document.getElementById(id);
      if (!box || box.getAttribute('data-copy-enhanced')) return;
      box.setAttribute('data-copy-enhanced', '1');
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'tool-btn tool-btn-ghost';
      btn.textContent = '📋 复制结果';
      btn.setAttribute('aria-label', '复制结果');
      btn.style.marginTop = '.7rem';
      btn.addEventListener('click', function () {
        var text = '';
        if (id === 'wc-stats') {
          // 统计卡：逐项拼成「指标：数值」
          box.querySelectorAll('.wc-stat').forEach(function (s) {
            var num = s.querySelector('.wc-num');
            var lab = s.querySelector('.wc-label');
            if (num && lab) text += (lab.textContent || '').trim() + '：' + (num.textContent || '').trim() + '\n';
          });
        } else {
          text = (box.textContent || '').replace(/\u00a0/g, ' ').replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n').trim();
        }
        if (!text) {
          btn.textContent = '⚠️ 暂无结果';
          setTimeout(function () { btn.textContent = '📋 复制结果'; }, 1400);
          return;
        }
        copyPlain(text).then(function () {
          btn.textContent = '✓ 已复制';
          btn.classList.add('copied');
          setTimeout(function () { btn.textContent = '📋 复制结果'; btn.classList.remove('copied'); }, 1400);
        }).catch(function () {
          btn.textContent = '❌ 复制失败，请手动选择';
          setTimeout(function () { btn.textContent = '📋 复制结果'; }, 1800);
        });
      });
      box.parentNode.insertBefore(btn, box.nextSibling);
    });
  })();

  // 10) 无障碍运行时增强（不改 HTML 文件）
  //  - 隐藏文件输入补 aria-label
  ['ic-file', 'wm-file'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el && !el.getAttribute('aria-label')) el.setAttribute('aria-label', '选择图片文件');
  });
  //  - 未被 label 关联的可见 checkbox（如平铺水印开关），用相邻文本补 aria-label
  document.querySelectorAll('.tool-page input[type="checkbox"]').forEach(function (cb) {
    if (cb.closest('label')) return;
    if (cb.id && document.querySelector('label[for="' + cb.id + '"]')) return;
    if (cb.getAttribute('aria-label')) return;
    var txt = '';
    var n = cb.nextSibling;
    while (n && n.nodeType === 3) { txt += n.nodeValue; n = n.nextSibling; }
    if (!txt) txt = (cb.parentNode ? cb.parentNode.textContent : '') || '';
    txt = txt.replace(/\s+/g, ' ').trim();
    if (txt) cb.setAttribute('aria-label', txt);
  });
  //  - relative-calc 关系链 label 指向不存在的控件：移除无效 for，保留可见文本
  var rcRel = document.querySelector('label[for="rc-rel"]');
  if (rcRel) rcRel.removeAttribute('for');
})();

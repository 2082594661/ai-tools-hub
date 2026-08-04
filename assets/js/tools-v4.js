/* tools-v4.js — AI 工具箱 第四批 4 个新工具（纯前端、零 API、本地运行）
 * 油耗计算器 / 预产期计算器 / 随机数生成器 / 表情包制作
 * 每个 init 函数按页面专属元素守卫，未命中即 no-op。
 */
(function () {
  'use strict';

  function $(id) { return document.getElementById(id); }

  /* ---------- 通用：复制到剪贴板 ---------- */
  function copyText(text, btn) {
    var done = function () {
      if (!btn) return;
      var old = btn.textContent;
      btn.textContent = '✓ 已复制';
      btn.classList.add('copied');
      setTimeout(function () { btn.textContent = old; btn.classList.remove('copied'); }, 1400);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text); done(); });
    } else { fallbackCopy(text); done(); }
  }
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
  }
  function setMsg(id, text, isErr) {
    var el = $(id);
    if (!el) return;
    el.textContent = text;
    el.className = 'tool-msg' + (isErr ? ' msg-error' : ' msg-ok');
  }
  function num(id) {
    var v = parseFloat($(id).value);
    return isNaN(v) || v < 0 ? 0 : v;
  }

  /* ================= 1. 油耗计算器 ================= */
  function initFuelCost() {
    var runBtn = $('fc-run');
    if (!runBtn) return;
    runBtn.addEventListener('click', function () {
      var km = num('fc-km');
      var liters = num('fc-liters');
      var price = num('fc-price');
      if (km <= 0 || liters <= 0) { setMsg('fc-msg', '⚠️ 请填写行驶里程和耗油量（都需大于 0）', true); return; }
      var per100 = liters / km * 100;          // 百公里油耗 L/100km
      var totalCost = liters * price;          // 总油费
      var perKm = km > 0 ? totalCost / km : 0; // 每公里油费
      function set(id, v) { var el = $(id); if (el) el.textContent = v; }
      set('fc-hundred', per100.toFixed(2) + ' L/100km');
      set('fc-per-km', '¥' + perKm.toFixed(2));
      set('fc-total', '¥' + totalCost.toFixed(2));
    });
  }

  /* ================= 2. 预产期计算器 ================= */
  function initDueDate() {
    var runBtn = $('dd-run');
    if (!runBtn) return;
    function pad(n) { return (n < 10 ? '0' : '') + n; }
    function fmtDate(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
    runBtn.addEventListener('click', function () {
      var lmpVal = $('dd-lmp').value;
      if (!lmpVal) { setMsg('dd-msg', '⚠️ 请选择末次月经第一天', true); return; }
      var lmp = new Date(lmpVal + 'T00:00:00');
      if (isNaN(lmp.getTime())) { setMsg('dd-msg', '⚠️ 日期无效', true); return; }
      var due = new Date(lmp.getTime() + 280 * 86400000);  // 40 周 = 280 天
      var now = new Date();
      now.setHours(0, 0, 0, 0);
      var daysPregnant = Math.max(0, Math.round((now.getTime() - lmp.getTime()) / 86400000));
      var weeks = Math.floor(daysPregnant / 7);
      var days = daysPregnant % 7;
      var remain = Math.max(0, Math.round((due.getTime() - now.getTime()) / 86400000));
      function set(id, v) { var el = $(id); if (el) el.textContent = v; }
      set('dd-due', fmtDate(due));
      set('dd-week', weeks + ' 周 + ' + days + ' 天');
      set('dd-days', daysPregnant + ' 天');
      set('dd-remain', remain + ' 天');
    });
  }

  /* ================= 3. 随机数生成器 ================= */
  function initRandomGenerator() {
    var runBtn = $('rg-run');
    if (!runBtn) return;
    var copyBtn = $('rg-copy');
    var output = $('rg-output');
    var lastResult = '';
    function gen() {
      var min = Math.floor(num('rg-min'));
      var max = Math.floor(num('rg-max'));
      var count = Math.floor(num('rg-count'));
      if (isNaN(min) || isNaN(max) || isNaN(count) || count < 1) { setMsg('rg-msg', '⚠️ 请填写有效的范围与个数', true); return; }
      if (min > max) { var t = min; min = max; max = t; }
      var unique = $('rg-unique').value === '1';
      var maxPossible = max - min + 1;
      if (unique && count > maxPossible) { setMsg('rg-msg', '⚠️ 不重复模式下个数不能超过可选范围（' + maxPossible + ' 个）', true); return; }
      var arr = [];
      if (unique) {
        var pool = [];
        for (var i = min; i <= max; i++) pool.push(i);
        // Fisher–Yates 部分洗牌取前 count 个
        for (var j = pool.length - 1; j > 0 && arr.length < count; j--) {
          var k = Math.floor(Math.random() * (j + 1));
          var tmp = pool[j]; pool[j] = pool[k]; pool[k] = tmp;
          arr.push(pool[j]);
        }
        if (arr.length < count) arr.push(pool[0]);
      } else {
        for (var n = 0; n < count; n++) arr.push(min + Math.floor(Math.random() * (max - min + 1)));
      }
      var sort = $('rg-sort').value;
      if (sort === 'asc') arr.sort(function (a, b) { return a - b; });
      if (sort === 'desc') arr.sort(function (a, b) { return b - a; });
      lastResult = arr.join(', ');
      output.innerHTML = arr.map(function (v, idx) { return '<span class="rg-num">' + v + '</span>'; }).join('');
      setMsg('rg-msg', '✅ 已生成 ' + arr.length + ' 个随机数');
    }
    runBtn.addEventListener('click', gen);
    copyBtn.addEventListener('click', function () {
      if (!lastResult) { setMsg('rg-msg', '⚠️ 请先生成随机数', true); return; }
      copyText(lastResult, copyBtn);
    });
    gen();  // 首次自动生成示例
  }

  /* ================= 4. 表情包制作 ================= */
  function initMemeMaker() {
    var fileEl = $('mm-file');
    if (!fileEl) return;
    var canvas = $('mm-canvas');
    var ctx = canvas.getContext('2d');
    var img = null;
    var wrap = $('mm-wrap');

    fileEl.addEventListener('change', function () {
      var f = fileEl.files && fileEl.files[0];
      if (!f) return;
      var url = URL.createObjectURL(f);
      var tmp = new Image();
      tmp.onload = function () {
        img = tmp;
        URL.revokeObjectURL(url);
        // 限制最大宽 800，等比缩放
        var w = Math.min(img.width, 800);
        var h = Math.round(img.height * w / img.width);
        canvas.width = w; canvas.height = h;
        setMsg('mm-msg', '✅ 已载入 ' + f.name + '（' + img.width + '×' + img.height + '），填好文字点「生成表情包」');
        render();
      };
      tmp.onerror = function () { setMsg('mm-msg', '❌ 图片加载失败，换一张试试', true); };
      tmp.src = url;
    });

    function render() {
      if (!img) return;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      var size = Math.round(canvas.width * parseFloat($('mm-size').value || 0.1));
      ctx.font = 'bold ' + size + 'px "Microsoft YaHei", "PingFang SC", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';
      ctx.fillStyle = $('mm-color').value || '#ffffff';
      ctx.lineWidth = Math.max(3, size / 8);
      ctx.strokeStyle = 'rgba(0,0,0,.85)';
      // 顶行
      var top = $('mm-top').value || '';
      if (top) {
        var ty = size * 0.2;
        wrapText(top, canvas.width / 2, ty, canvas.width * 0.92, size, ctx, true);
      }
      // 底行
      var bottom = $('mm-bottom').value || '';
      if (bottom) {
        var lines = Math.ceil(ctx.measureText(bottom).width / (canvas.width * 0.92));
        var lineCount = Math.max(1, Math.ceil(bottom.length * size * 1.05 / (canvas.width * 0.92)));
        var by = canvas.height - size * (lineCount + 0.4);
        wrapText(bottom, canvas.width / 2, by, canvas.width * 0.92, size, ctx, false);
      }
    }
    function wrapText(text, x, y, maxWidth, size, c, topAlign) {
      var words = text.split('');
      var line = '';
      var lineH = size * 1.25;
      var yy = y;
      for (var i = 0; i < words.length; i++) {
        var test = line + words[i];
        if (c.measureText(test).width > maxWidth && line) {
          strokeFill(c, line, x, yy);
          yy += lineH;
          line = words[i];
        } else {
          line = test;
        }
      }
      if (line) strokeFill(c, line, x, yy);
    }
    function strokeFill(c, text, x, y) {
      c.strokeText(text, x, y);
      c.fillText(text, x, y);
    }

    $('mm-render').addEventListener('click', function () {
      if (!img) { setMsg('mm-msg', '⚠️ 请先选择一张图片', true); return; }
      render();
      setMsg('mm-msg', '✅ 表情包已生成，点「下载 PNG」保存');
    });
    $('mm-download').addEventListener('click', function () {
      if (!img) { setMsg('mm-msg', '⚠️ 请先生成表情包', true); return; }
      render();
      var a = document.createElement('a');
      a.href = canvas.toDataURL('image/png');
      a.download = 'meme.png';
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
      setMsg('mm-msg', '⬇️ 已开始下载 meme.png');
    });
    // 输入变化实时刷新预览（有图时）
    ['mm-top', 'mm-bottom', 'mm-size', 'mm-color'].forEach(function (id) {
      var el = $(id);
      if (el) el.addEventListener('input', function () { if (img) render(); });
    });
  }

  /* ============ 注册：DOMContentLoaded 逐个执行 ============ */
  var inits = [
    initFuelCost, initDueDate, initRandomGenerator, initMemeMaker
  ];
  function runAll() {
    inits.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error('tools-v4 init error:', e); } });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runAll);
  } else {
    runAll();
  }
})();

/* tools-new.js — AI 工具箱 8 个新工具（纯前端、零 API、本地运行）
 * 图片加水印 / 日期计算器 / 单位换算 / 颜色转换 / 文本对比 /
 * 房贷月供计算器 / BMI 计算器 / 进制转换
 * 每个 init 函数按页面专属元素守卫，未命中即 no-op（同页只跑对应一个）。
 */
(function () {
  'use strict';

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

  /* ================= 工具：图片加水印 ================= */
  function initWatermark() {
    var drop = document.getElementById('wm-drop');
    if (!drop) return;
    var fileInput = document.getElementById('wm-file');
    var controls = document.getElementById('wm-controls');
    var textEl = document.getElementById('wm-text');
    var fsEl = document.getElementById('wm-fontsize');
    var opEl = document.getElementById('wm-opacity');
    var colorEl = document.getElementById('wm-color');
    var posEl = document.getElementById('wm-position');
    var tileEl = document.getElementById('wm-tile');
    var preview = document.getElementById('wm-preview');
    var stats = document.getElementById('wm-stats');
    var download = document.getElementById('wm-download');

    var sourceImage = null, lastUrl = null;
    var MAX = 2000;

    drop.addEventListener('click', function () { fileInput.click(); });
    drop.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); } });
    drop.addEventListener('dragover', function (e) { e.preventDefault(); drop.style.borderColor = 'var(--clr-primary)'; });
    drop.addEventListener('dragleave', function () { drop.style.borderColor = ''; });
    drop.addEventListener('drop', function (e) { e.preventDefault(); drop.style.borderColor = ''; if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]); });
    fileInput.addEventListener('change', function () { if (fileInput.files[0]) handleFile(fileInput.files[0]); });

    function handleFile(file) {
      if (!file.type.match(/^image\//)) { stats.textContent = '请选择图片文件'; return; }
      var reader = new FileReader();
      reader.onload = function (e) {
        var img = new Image();
        img.onload = function () { sourceImage = img; controls.style.display = 'block'; render(); };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    [textEl, fsEl, opEl, colorEl, posEl, tileEl].forEach(function (el) {
      el.addEventListener('input', render); el.addEventListener('change', render);
    });

    function render() {
      if (!sourceImage) return;
      var scale = 1;
      var w = sourceImage.naturalWidth, h = sourceImage.naturalHeight;
      if (Math.max(w, h) > MAX) { scale = MAX / Math.max(w, h); w = Math.round(w * scale); h = Math.round(h * scale); }
      var canvas = document.createElement('canvas');
      canvas.width = w; canvas.height = h;
      var ctx = canvas.getContext('2d');
      ctx.drawImage(sourceImage, 0, 0, w, h);
      var fs = Math.max(12, Math.round(w * (parseInt(fsEl.value, 10) / 100)));
      ctx.font = 'bold ' + fs + 'px sans-serif';
      ctx.fillStyle = colorEl.value;
      ctx.globalAlpha = parseInt(opEl.value, 10) / 100;
      var pad = Math.round(fs * 0.6);
      var pos = posEl.value;
      if (tileEl.checked) {
        var stepX = fs * 9, stepY = fs * 5;
        for (var y = stepY / 2; y < h + stepY; y += stepY) {
          for (var x = 0; x < w + stepX; x += stepX) { ctx.fillText(textEl.value, x, y); }
        }
      } else {
        var align = 'left', baseline = 'top', cx = pad, cy = pad;
        if (pos.indexOf('top') === 0) { baseline = 'top'; cy = pad; }
        else if (pos.indexOf('bottom') === 0) { baseline = 'bottom'; cy = h - pad; }
        else { baseline = 'middle'; cy = h / 2; }
        if (pos.indexOf('left') >= 0) { align = 'left'; cx = pad; }
        else if (pos.indexOf('right') >= 0) { align = 'right'; cx = w - pad; }
        else { align = 'center'; cx = w / 2; }
        ctx.textAlign = align; ctx.textBaseline = baseline;
        ctx.fillText(textEl.value, cx, cy);
      }
      ctx.globalAlpha = 1;
      if (lastUrl) URL.revokeObjectURL(lastUrl);
      lastUrl = canvas.toDataURL('image/png');
      preview.innerHTML = '<figure><img src="' + lastUrl + '" alt="加水印后预览"><figcaption>预览（含水印）</figcaption></figure>';
      stats.textContent = '原图 ' + sourceImage.naturalWidth + '×' + sourceImage.naturalHeight + ' ｜ 水印已叠加，可下载 PNG';
      download.href = lastUrl; download.setAttribute('download', 'watermarked.png');
    }
  }

  /* ================= 工具：日期计算器 ================= */
  function initDateCalc() {
    var diffBtn = document.getElementById('dc-diff-btn');
    if (!diffBtn) return;
    var a = document.getElementById('dc-date-a');
    var b = document.getElementById('dc-date-b');
    var diffOut = document.getElementById('dc-diff-out');
    var from = document.getElementById('dc-from');
    var amount = document.getElementById('dc-amount');
    var unit = document.getElementById('dc-unit');
    var dir = document.getElementById('dc-dir');
    var calcBtn = document.getElementById('dc-calc-btn');
    var calcOut = document.getElementById('dc-calc-out');

    function parse(d) { var p = d.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
    function fmt(dt) {
      var w = ['日', '一', '二', '三', '四', '五', '六'][dt.getDay()];
      return dt.getFullYear() + '年' + (dt.getMonth() + 1) + '月' + dt.getDate() + '日（周' + w + '）';
    }
    function daysBetween(x, y) { return Math.round((parse(y) - parse(x)) / 86400000); }

    diffBtn.addEventListener('click', function () {
      if (!a.value || !b.value) { diffOut.innerHTML = '<div class="result-line">请选择两个日期</div>'; return; }
      var d = daysBetween(a.value, b.value);
      var abs = Math.abs(d);
      diffOut.innerHTML = '<div class="result-line">相差 <b>' + abs + '</b> 天（约 ' + (abs / 7).toFixed(1) + ' 周）</div>' +
        '<div class="result-line">' + (d >= 0 ? 'B 比 A 晚' : 'B 比 A 早') + ' <b>' + abs + '</b> 天</div>';
    });

    calcBtn.addEventListener('click', function () {
      if (!from.value) { calcOut.innerHTML = '<div class="result-line">请选择起始日期</div>'; return; }
      var base = parse(from.value);
      var n = parseInt(amount.value, 10) || 0;
      if (dir.value === 'sub') n = -n;
      var u = unit.value;
      var r = new Date(base);
      if (u === 'day') r.setDate(base.getDate() + n);
      else if (u === 'week') r.setDate(base.getDate() + n * 7);
      else if (u === 'month') r.setMonth(base.getMonth() + n);
      else if (u === 'year') r.setFullYear(base.getFullYear() + n);
      calcOut.innerHTML = '<div class="result-line">结果日期：<b>' + fmt(r) + '</b></div>';
    });
  }

  /* ================= 工具：单位换算 ================= */
  function initUnitConvert() {
    var cat = document.getElementById('uc-cat');
    if (!cat) return;
    var from = document.getElementById('uc-from');
    var to = document.getElementById('uc-to');
    var val = document.getElementById('uc-value');
    var out = document.getElementById('uc-result');

    var DATA = {
      '长度': { base: '米', units: { '毫米': 0.001, '厘米': 0.01, '米': 1, '千米': 1000, '英寸': 0.0254, '英尺': 0.3048, '码': 0.9144, '英里': 1609.344 } },
      '重量': { base: '千克', units: { '毫克': 1e-6, '克': 0.001, '千克': 1, '吨': 1000, '盎司': 0.0283495, '磅': 0.453592 } },
      '面积': { base: '平方米', units: { '平方厘米': 0.0001, '平方米': 1, '平方千米': 1e6, '公顷': 10000, '亩': 666.6667, '平方英尺': 0.092903, '英亩': 4046.856 } },
      '体积': { base: '升', units: { '毫升': 0.001, '升': 1, '立方米': 1000, '加仑(美)': 3.78541, '品脱(美)': 0.473176 } },
      '数据存储': { base: '字节', units: { 'B': 1, 'KB': 1024, 'MB': 1048576, 'GB': 1073741824, 'TB': 1099511627776 } }
    };
    var TEMP = { '摄氏度(°C)': 'C', '华氏度(°F)': 'F', '开尔文(K)': 'K' };

    function fill(sel, obj) { sel.innerHTML = ''; Object.keys(obj).forEach(function (k) { var o = document.createElement('option'); o.value = k; o.textContent = k; sel.appendChild(o); }); }
    function repopulate() {
      if (cat.value === '温度') { fill(from, TEMP); fill(to, TEMP); }
      else { fill(from, DATA[cat.value].units); fill(to, DATA[cat.value].units); }
      calc();
    }
    function toBaseC(v, unit) {
      if (unit === '摄氏度(°C)') return v;
      if (unit === '华氏度(°F)') return (v - 32) * 5 / 9;
      return v - 273.15; // K
    }
    function fromBaseC(c, unit) {
      if (unit === '摄氏度(°C)') return c;
      if (unit === '华氏度(°F)') return c * 9 / 5 + 32;
      return c + 273.15;
    }
    function calc() {
      var v = parseFloat(val.value);
      if (isNaN(v)) { out.innerHTML = '<div class="result-line">请输入数值</div>'; return; }
      var res;
      if (cat.value === '温度') res = fromBaseC(toBaseC(v, from.value), to.value);
      else {
        var factor = DATA[cat.value].units;
        res = v * factor[from.value] / factor[to.value];
      }
      var txt = (Math.abs(res) >= 1e-4 && Math.abs(res) < 1e9) ? res.toFixed(6).replace(/\.?0+$/, '') : res.toExponential(4);
      out.innerHTML = '<div class="result-line"><b>' + val.value + ' ' + from.value + '</b> = <b>' + txt + ' ' + to.value + '</b></div>';
    }
    cat.addEventListener('change', repopulate);
    [from, to, val].forEach(function (el) { el.addEventListener('input', calc); el.addEventListener('change', calc); });
    repopulate();
  }

  /* ================= 工具：颜色转换（可视化取色器 + 热门色） ================= */
  function initColorConvert() {
    var input = document.getElementById('cc-input');
    if (!input) return;
    var swatch = document.getElementById('cc-swatch');
    var out = document.getElementById('cc-output');
    var sv = document.getElementById('cc-sv');
    var svHandle = document.getElementById('cc-sv-handle');
    var hue = document.getElementById('cc-hue');
    var hueHandle = document.getElementById('cc-hue-handle');
    var popular = document.getElementById('cc-popular');

    function clamp(n, lo, hi) { return Math.max(lo, Math.min(hi, n)); }

    function parse(str) {
      str = (str || '').trim();
      var m;
      if ((m = str.match(/^#([0-9a-f]{3}|[0-9a-f]{6})$/i))) {
        var h = m[1]; if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
        return { r: parseInt(h.substr(0, 2), 16), g: parseInt(h.substr(2, 2), 16), b: parseInt(h.substr(4, 2), 16) };
      }
      if ((m = str.match(/rgba?\(([^)]+)\)/i))) {
        var p = m[1].split(',').map(function (x) { return parseFloat(x); });
        return { r: clamp(Math.round(p[0]), 0, 255), g: clamp(Math.round(p[1]), 0, 255), b: clamp(Math.round(p[2]), 0, 255) };
      }
      if ((m = str.match(/hsla?\(([^)]+)\)/i))) {
        var q = m[1].split(',').map(function (x) { return parseFloat(x); });
        return hslToRgb(q[0], (q[1] || 0) / 100, (q[2] || 0) / 100);
      }
      return null;
    }
    function hslToRgb(h, s, l) {
      h = (h % 360) / 360; var r, g, b;
      if (s === 0) { r = g = b = l; }
      else {
        var hue2rgb = function (p, q, t) { if (t < 0) t += 1; if (t > 1) t -= 1; if (t < 1 / 6) return p + (q - p) * 6 * t; if (t < 1 / 2) return q; if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6; return p; };
        var q2 = l < 0.5 ? l * (1 + s) : l + s - l * s, p2 = 2 * l - q2;
        r = hue2rgb(p2, q2, h + 1 / 3); g = hue2rgb(p2, q2, h); b = hue2rgb(p2, q2, h - 1 / 3);
      }
      return { r: clamp(Math.round(r * 255), 0, 255), g: clamp(Math.round(g * 255), 0, 255), b: clamp(Math.round(b * 255), 0, 255) };
    }
    function rgbToHsl(r, g, b) {
      r /= 255; g /= 255; b /= 255;
      var max = Math.max(r, g, b), min = Math.min(r, g, b), h, s, l = (max + min) / 2;
      if (max === min) { h = s = 0; } else {
        var d = max - min; s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        if (max === r) h = (g - b) / d + (g < b ? 6 : 0);
        else if (max === g) h = (b - r) / d + 2;
        else h = (r - g) / d + 4;
        h /= 6;
      }
      return { h: Math.round(h * 360), s: Math.round(s * 100), l: Math.round(l * 100) };
    }
    function rgbToHsv(r, g, b) {
      r /= 255; g /= 255; b /= 255;
      var max = Math.max(r, g, b), min = Math.min(r, g, b), d = max - min, h = 0, s, v = max;
      if (d === 0) { s = 0; } else {
        s = v === 0 ? 0 : d / v;
        if (max === r) h = (g - b) / d + (g < b ? 6 : 0);
        else if (max === g) h = (b - r) / d + 2;
        else h = (r - g) / d + 4;
        h /= 6;
      }
      return { h: Math.round(h * 360), s: Math.round(s * 1000) / 1000, v: Math.round(v * 1000) / 1000 };
    }
    function hsvToRgb(h, s, v) {
      h = ((h % 360) + 360) % 360 / 360; s = clamp(s, 0, 1); v = clamp(v, 0, 1);
      var i = Math.floor(h * 6), f = h * 6 - i, p = v * (1 - s), q = v * (1 - f * s), t = v * (1 - (1 - f) * s), r, g, b;
      switch (i % 6) {
        case 0: r = v; g = t; b = p; break;
        case 1: r = q; g = v; b = p; break;
        case 2: r = p; g = v; b = t; break;
        case 3: r = p; g = q; b = v; break;
        case 4: r = t; g = p; b = v; break;
        default: r = v; g = p; b = q;
      }
      return { r: clamp(Math.round(r * 255), 0, 255), g: clamp(Math.round(g * 255), 0, 255), b: clamp(Math.round(b * 255), 0, 255) };
    }
    function toHex(r, g, b) { return '#' + [r, g, b].map(function (x) { return clamp(x, 0, 255).toString(16).padStart(2, '0'); }).join(''); }

    // 取色器内部状态：HSV（与色块区/色相条一一对应）
    var state = { h: 14, s: 0.62, v: 0.77, exactHex: null };

    function render() {
      var rgb = hsvToRgb(state.h, state.s, state.v);
      var hex = state.exactHex || toHex(rgb.r, rgb.g, rgb.b);
      var hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
      sv.style.backgroundColor = 'hsl(' + Math.round(state.h) + ',100%,50%)';
      svHandle.style.left = (state.s * 100) + '%';
      svHandle.style.top = ((1 - state.v) * 100) + '%';
      hueHandle.style.left = (state.h / 360 * 100) + '%';
      swatch.style.background = hex;
      input.value = hex;
      sv.setAttribute('aria-valuetext', '饱和度 ' + Math.round(state.s * 100) + '%，明度 ' + Math.round(state.v * 100) + '%');
      hue.setAttribute('aria-valuetext', '色相 ' + Math.round(state.h) + ' 度');
      out.innerHTML =
        row('HEX', hex) + row('RGB', 'rgb(' + rgb.r + ', ' + rgb.g + ', ' + rgb.b + ')') +
        row('HSL', 'hsl(' + hsl.h + ', ' + hsl.s + '%, ' + hsl.l + '%)');
    }
    function row(label, val) {
      return '<div class="tool-result-item"><span>' + label + '：<b>' + val + '</b></span>' +
        '<button class="copy-btn" type="button" data-copy="' + val + '">复制</button></div>';
    }
    function setFromRgb(rgb, exactHex) {
      if (!rgb) return;
      var hsv = rgbToHsv(rgb.r, rgb.g, rgb.b);
      state.h = hsv.h; state.s = hsv.s; state.v = hsv.v;
      state.exactHex = exactHex || null;
      render();
    }

    // SV 方块拖拽
    var svDrag = false;
    function moveSV(e) {
      var rect = sv.getBoundingClientRect();
      var x = clamp((e.clientX - rect.left) / rect.width, 0, 1);
      var y = clamp((e.clientY - rect.top) / rect.height, 0, 1);
      state.s = x; state.v = 1 - y; state.exactHex = null; render();
    }
    sv.addEventListener('pointerdown', function (e) { svDrag = true; sv.setPointerCapture(e.pointerId); moveSV(e); });
    sv.addEventListener('pointermove', function (e) { if (svDrag) moveSV(e); });
    sv.addEventListener('pointerup', function () { svDrag = false; });
    sv.addEventListener('pointercancel', function () { svDrag = false; });
    sv.addEventListener('keydown', function (e) {
      var step = e.shiftKey ? 0.1 : 0.02;
      if (e.key === 'ArrowLeft') { state.s = clamp(state.s - step, 0, 1); state.exactHex = null; render(); e.preventDefault(); }
      else if (e.key === 'ArrowRight') { state.s = clamp(state.s + step, 0, 1); state.exactHex = null; render(); e.preventDefault(); }
      else if (e.key === 'ArrowUp') { state.v = clamp(state.v + step, 0, 1); state.exactHex = null; render(); e.preventDefault(); }
      else if (e.key === 'ArrowDown') { state.v = clamp(state.v - step, 0, 1); state.exactHex = null; render(); e.preventDefault(); }
    });

    // 色相条拖拽
    var hueDrag = false;
    function moveHue(e) {
      var rect = hue.getBoundingClientRect();
      var x = clamp((e.clientX - rect.left) / rect.width, 0, 1);
      state.h = x * 360; state.exactHex = null; render();
    }
    hue.addEventListener('pointerdown', function (e) { hueDrag = true; hue.setPointerCapture(e.pointerId); moveHue(e); });
    hue.addEventListener('pointermove', function (e) { if (hueDrag) moveHue(e); });
    hue.addEventListener('pointerup', function () { hueDrag = false; });
    hue.addEventListener('pointercancel', function () { hueDrag = false; });
    hue.addEventListener('keydown', function (e) {
      var step = e.shiftKey ? 10 : 2;
      if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') { state.h = (state.h - step + 360) % 360; state.exactHex = null; render(); e.preventDefault(); }
      else if (e.key === 'ArrowRight' || e.key === 'ArrowUp') { state.h = (state.h + step) % 360; state.exactHex = null; render(); e.preventDefault(); }
    });

    // 文本输入 -> 取色器联动
    input.addEventListener('input', function () {
      var c = parse(input.value);
      if (c) setFromRgb(c, /^#[0-9a-f]{3,6}$/i.test(input.value.trim()) ? input.value.trim() : null);
      else out.innerHTML = '<div class="result-line">无法识别，请输入如 #ff6b6b、rgb(255,107,107) 或 hsl(0,100%,71%)</div>';
    });
    out.addEventListener('click', function (e) { var b = e.target.closest('.copy-btn'); if (b) copyText(b.getAttribute('data-copy'), b); });

    // 热门颜色
    var POPULAR = [
      { n: '中国红', c: '#e60012' }, { n: '微信绿', c: '#07c160' }, { n: '抖音红', c: '#fe2c55' },
      { n: '腾讯蓝', c: '#0052d9' }, { n: '美团黄', c: '#ffc300' }, { n: '阿里橙', c: '#ff6a00' },
      { n: '薄荷绿', c: '#00b894' }, { n: '克莱因蓝', c: '#002fa7' }, { n: '蒂芙尼蓝', c: '#0abab5' },
      { n: '香槟金', c: '#d4af37' }, { n: '莫兰迪粉', c: '#d8a7b1' }, { n: '雾霾蓝', c: '#8ba3c7' },
      { n: '高级灰', c: '#8c8c8c' }, { n: '牛油果绿', c: '#7cb342' }, { n: '爱马仕橙', c: '#ff6600' },
      { n: '星空黑', c: '#1a1a1a' }
    ];
    POPULAR.forEach(function (p) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'popular-swatch';
      b.setAttribute('aria-label', p.n + ' ' + p.c);
      b.innerHTML = '<span class="pc" style="background:' + p.c + '"></span>' +
        '<span class="pn">' + p.n + '</span><span class="ph">' + p.c + '</span>';
      b.addEventListener('click', function () { setFromRgb(parse(p.c), p.c); });
      popular.appendChild(b);
    });

    // 用输入框初始值定位取色器
    setFromRgb(parse(input.value) || { r: 196, g: 93, b: 58 }, /^#[0-9a-f]{3,6}$/i.test(input.value.trim()) ? input.value.trim() : '#c45d3a');
  }

  /* ================= 工具：文本对比 ================= */
  function initTextDiff() {
    var btn = document.getElementById('td-btn');
    if (!btn) return;
    var a = document.getElementById('td-a');
    var b = document.getElementById('td-b');
    var out = document.getElementById('td-output');

    function lcs(aa, bb) {
      var m = aa.length, n = bb.length, dp = [];
      for (var i = 0; i <= m; i++) dp[i] = new Array(n + 1).fill(0);
      for (i = m - 1; i >= 0; i--) for (var j = n - 1; j >= 0; j--)
        dp[i][j] = aa[i] === bb[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
      var res = [], i = 0, j = 0;
      while (i < m && j < n) {
        if (aa[i] === bb[j]) { res.push({ t: 'same', v: aa[i] }); i++; j++; }
        else if (dp[i + 1][j] >= dp[i][j + 1]) { res.push({ t: 'del', v: aa[i] }); i++; }
        else { res.push({ t: 'add', v: bb[j] }); j++; }
      }
      while (i < m) { res.push({ t: 'del', v: aa[i++] }); }
      while (j < n) { res.push({ t: 'add', v: bb[j++] }); }
      return res;
    }
    btn.addEventListener('click', function () {
      var la = a.value.split('\n'), lb = b.value.split('\n');
      // 空输入提示
      if (!a.value.trim() && !b.value.trim()) {
        out.innerHTML = '<div class="diff-empty">📝 请在上方两个文本框中分别粘贴需要对比的文字，再点击「开始对比」</div>';
        return;
      }
      var diff = lcs(la, lb), html = '';
      var adds = 0, dels = 0;
      diff.forEach(function (d) {
        if (d.t === 'add') adds++;
        else if (d.t === 'del') dels++;
        var cls = d.t === 'add' ? 'diff-add' : d.t === 'del' ? 'diff-del' : '';
        var prefix = d.t === 'add' ? '+ ' : d.t === 'del' ? '- ' : '  ';
        html += '<div class="' + cls + '">' + prefix + escapeHtml(d.v) + '</div>';
      });
      // 统计栏
      var stat = '<div class="diff-stat">共 ' + diff.length + ' 行';
      if (dels > 0) stat += ' · <span style="color:#b23b1e">−' + dels + ' 删除</span>';
      if (adds > 0) stat += ' · <span style="color:#1f6b4f">+' + adds + ' 新增</span>';
      if (dels === 0 && adds === 0) stat += ' · <span style="color:var(--clr-secondary)">✓ 完全一致</span>';
      stat += '</div>';
      out.innerHTML = stat + html;
    });
    function escapeHtml(s) { return s.replace(/[&<>"']/g, function (c) { return ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'": '&#39;' })[c]; }); }
    // 清空按钮
    var clearBtn = document.getElementById('td-clear');
    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        a.value = '';
        b.value = '';
        out.innerHTML = '';
      });
    }
  }

  /* ================= 工具：房贷月供计算器 ================= */
  function initMortgage() {
    var btn = document.getElementById('mg-btn');
    if (!btn) return;
    var total = document.getElementById('mg-total');
    var rate = document.getElementById('mg-rate');
    var years = document.getElementById('mg-years');
    var type = document.getElementById('mg-type');
    var out = document.getElementById('mg-output');

    btn.addEventListener('click', function () {
      var P = parseFloat(total.value) * 10000;
      var annual = parseFloat(rate.value) / 100;
      var n = parseInt(years.value, 10) * 12;
      if (isNaN(P) || isNaN(annual) || isNaN(n) || P <= 0) { out.innerHTML = '<div class="result-line">请填写正确的贷款总额、年利率、年限</div>'; return; }
      var r = annual / 12;
      var html = '';
      if (type.value === 'equal') {
        var pow = Math.pow(1 + r, n);
        var monthly = P * r * pow / (pow - 1);
        var totalPay = monthly * n;
        html = '<div class="result-line">每月月供：<span class="result-big">' + monthly.toFixed(2) + ' 元</span></div>' +
          '<div class="result-line">还款总额：<b>' + totalPay.toFixed(2) + ' 元</b></div>' +
          '<div class="result-line">支付利息：<b>' + (totalPay - P).toFixed(2) + ' 元</b></div>';
      } else {
        var principal = P / n;
        var first = principal + P * r;
        var last = principal + principal * r;
        var interest = (P * r) * (n + 1) / 2;
        html = '<div class="result-line">首月月供：<span class="result-big">' + first.toFixed(2) + ' 元</span></div>' +
          '<div class="result-line">每月递减：<b>' + (principal * r).toFixed(2) + ' 元</b></div>' +
          '<div class="result-line">末月月供：<b>' + last.toFixed(2) + ' 元</b></div>' +
          '<div class="result-line">支付利息：<b>' + interest.toFixed(2) + ' 元</b></div>';
      }
      out.innerHTML = html;
    });
  }

  /* ================= 工具：BMI 计算器 ================= */
  function initBMI() {
    var btn = document.getElementById('bmi-btn');
    if (!btn) return;
    var h = document.getElementById('bmi-height');
    var w = document.getElementById('bmi-weight');
    var out = document.getElementById('bmi-output');

    btn.addEventListener('click', function () {
      var height = parseFloat(h.value) / 100;
      var weight = parseFloat(w.value);
      if (!height || !weight || height <= 0) { out.innerHTML = '<div class="result-line">请输入正确的身高(cm)和体重(kg)</div>'; return; }
      var bmi = weight / (height * height);
      var cat, color;
      if (bmi < 18.5) { cat = '偏瘦'; color = '#2d6b5a'; }
      else if (bmi < 24) { cat = '正常'; color = '#1f6b4f'; }
      else if (bmi < 28) { cat = '超重'; color = '#c45d3a'; }
      else { cat = '肥胖'; color = '#b23b1e'; }
      var min = (18.5 * height * height).toFixed(1);
      var max = (23.9 * height * height).toFixed(1);
      out.innerHTML = '<div class="result-line">你的 BMI：<span class="result-big" style="color:' + color + '">' + bmi.toFixed(1) + '</span>（' + cat + '）</div>' +
        '<div class="result-line">健康体重范围：<b>' + min + ' – ' + max + ' kg</b></div>';
    });
  }

  /* ================= 工具：进制转换 ================= */
  function initBaseConvert() {
    var btn = document.getElementById('bc-btn');
    if (!btn) return;
    var val = document.getElementById('bc-value');
    var from = document.getElementById('bc-from');
    var to = document.getElementById('bc-to');
    var out = document.getElementById('bc-output');

    btn.addEventListener('click', function () {
      var fb = parseInt(from.value, 10), tb = parseInt(to.value, 10);
      var v = val.value.trim().toUpperCase();
      if (fb < 2 || fb > 36 || tb < 2 || tb > 36) { out.innerHTML = '<div class="result-line">进制需为 2–36 之间</div>'; return; }
      var dec;
      try { dec = parseToBig(v, fb); } catch (e) { out.innerHTML = '<div class="result-line">输入内容不符合 ' + fb + ' 进制</div>'; return; }
      var res = bigToBase(dec, tb);
      out.innerHTML = '<div class="result-line"><b>' + fb + ' 进制</b> ' + v + ' = <b>' + tb + ' 进制</b> ' + res + '</div>';
    });
    function parseToBig(str, base) {
      var neg = false; if (str[0] === '-') { neg = true; str = str.slice(1); }
      var big = 0n, B = BigInt(base);
      for (var i = 0; i < str.length; i++) {
        var d = parseInt(str[i], base);
        if (isNaN(d)) throw new Error('bad');
        big = big * B + BigInt(d);
      }
      return neg ? -big : big;
    }
    function bigToBase(big, base) {
      var neg = big < 0n; if (neg) big = -big;
      if (big === 0n) return '0';
      var B = BigInt(base), s = '';
      var digits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      while (big > 0n) { s = digits[Number(big % B)] + s; big /= B; }
      return neg ? '-' + s : s;
    }
  }

  /* ---------- 初始化 ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    [initWatermark, initDateCalc, initUnitConvert, initColorConvert, initTextDiff, initMortgage, initBMI, initBaseConvert].forEach(function (fn) {
      try { fn(); } catch (err) { console.error('工具初始化失败:', fn.name, err); }
    });
  });
})();

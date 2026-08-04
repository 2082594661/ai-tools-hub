/* tools-v3.js — AI 工具箱 第三批 4 个新工具（纯前端、零 API、本地运行）
 * 九宫格切图 / 正则表达式测试 / 个税计算器 / 时区转换
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
  function triggerDownload(url, filename) {
    var a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
  }

  /* ================= 1. 九宫格切图 ================= */
  function initNineGrid() {
    var fileEl = $('ng-file');
    if (!fileEl) return;
    var grid = $('ng-grid');
    var actions = $('ng-actions');
    var cropBtn = $('ng-crop');
    var clearBtn = $('ng-clear');
    var dlAll = $('ng-download-all');
    var img = null;
    var pieces = [];

    fileEl.addEventListener('change', function () {
      var f = fileEl.files && fileEl.files[0];
      if (!f) return;
      var url = URL.createObjectURL(f);
      var tmp = new Image();
      tmp.onload = function () {
        img = tmp;
        URL.revokeObjectURL(url);
        setMsg('ng-msg', '✅ 已载入 ' + f.name + '（' + img.width + '×' + img.height + '）。建议正方形图片效果最佳，点「切成九宫格」开始。');
        grid.innerHTML = '';
        actions.style.display = 'none';
        pieces = [];
      };
      tmp.onerror = function () { setMsg('ng-msg', '❌ 图片加载失败，请换一张试试', true); };
      tmp.src = url;
    });

    cropBtn.addEventListener('click', function () {
      if (!img) { setMsg('ng-msg', '⚠️ 请先选择一张图片', true); return; }
      var size = Math.min(img.width, img.height);   // 取最短边，居中裁剪成正方形
      var sx = (img.width - size) / 2;
      var sy = (img.height - size) / 2;
      var step = size / 3;
      pieces = [];
      grid.innerHTML = '';
      for (var r = 0; r < 3; r++) {
        for (var c = 0; c < 3; c++) {
          (function (row, col) {
            var cv = document.createElement('canvas');
            cv.width = step; cv.height = step;
            var ctx = cv.getContext('2d');
            ctx.drawImage(img, sx + col * step, sy + row * step, step, step, 0, 0, step, step);
            var dataUrl = cv.toDataURL('image/png');
            pieces.push(dataUrl);
            var wrap = document.createElement('div');
            wrap.className = 'ng-cell';
            var im = document.createElement('img');
            im.src = dataUrl; im.alt = '九宫格第 ' + (row * 3 + col + 1) + ' 张';
            im.className = 'ng-img';
            wrap.appendChild(im);
            im.addEventListener('click', function () {
              triggerDownload(this.src, 'nine-grid-' + (row * 3 + col + 1) + '.png');
            });
            grid.appendChild(wrap);
          })(r, c);
        }
      }
      actions.style.display = '';
      setMsg('ng-msg', '✅ 已切成 9 张（每张 ' + Math.round(step) + '×' + Math.round(step) + 'px）。点击任意小图可单独下载。');
    });

    dlAll.addEventListener('click', function () {
      if (!pieces.length) return;
      pieces.forEach(function (url, i) {
        setTimeout(function () { triggerDownload(url, 'nine-grid-' + (i + 1) + '.png'); }, i * 300);
      });
      setMsg('ng-msg', '⬇️ 已开始下载 9 张图片（浏览器可能提示允许下载多个文件）');
    });

    clearBtn.addEventListener('click', function () {
      img = null; pieces = [];
      fileEl.value = '';
      grid.innerHTML = '';
      actions.style.display = 'none';
      setMsg('ng-msg', '');
    });
  }

  /* ================= 2. 正则表达式测试 ================= */
  function initRegexTester() {
    var patternEl = $('rt-pattern');
    if (!patternEl) return;
    var flagsEl = $('rt-flags');
    var inputEl = $('rt-input');
    var runBtn = $('rt-run');
    var clearBtn = $('rt-clear');
    var output = $('rt-output');

    function escapeHtml(s) {
      return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
    function highlight(text, regex) {
      var html = '';
      var last = 0;
      var m;
      var re = new RegExp(regex.source, regex.flags.replace('g', ''));
      // 使用带 g 的全局正则逐个匹配，自己维护 lastIndex
      var g = new RegExp(regex.source, regex.flags.indexOf('g') !== -1 ? regex.flags : regex.flags + 'g');
      while ((m = g.exec(text)) !== null) {
        if (m.index > last) html += escapeHtml(text.slice(last, m.index));
        html += '<mark>' + escapeHtml(m[0]) + '</mark>';
        last = m.index + m[0].length;
        if (m[0].length === 0) g.lastIndex++;  // 防空匹配死循环
      }
      html += escapeHtml(text.slice(last));
      return html;
    }

    runBtn.addEventListener('click', function () {
      var pattern = patternEl.value.trim();
      var flags = flagsEl.value.trim().replace(/[^gimsuy]/g, '');
      var text = inputEl.value;
      if (!pattern) { setMsg('rt-msg', '⚠️ 请输入正则表达式', true); return; }
      var re;
      try { re = new RegExp(pattern, flags); }
      catch (e) { setMsg('rt-msg', '❌ 正则表达式有误：' + e.message, true); return; }
      var count = 0;
      var g = new RegExp(re.source, re.flags.indexOf('g') !== -1 ? re.flags : re.flags + 'g');
      var m;
      while ((m = g.exec(text)) !== null) { count++; if (m[0].length === 0) g.lastIndex++; }
      output.innerHTML = '<div class="rt-count">共匹配 <strong>' + count + '</strong> 处</div>' +
        '<div class="rt-highlight">' + (text ? highlight(text, re) : '（测试文本为空）') + '</div>';
      var list = [];
      var g2 = new RegExp(re.source, re.flags.indexOf('g') !== -1 ? re.flags : re.flags + 'g');
      var m2;
      var idx = 0;
      while ((m2 = g2.exec(text)) !== null) {
        idx++;
        var snippet = m2[0].length > 40 ? m2[0].slice(0, 40) + '…' : m2[0];
        list.push('<li><span class="rt-idx">' + idx + '</span><code>' + escapeHtml(snippet) + '</code><span class="rt-pos">位置 ' + m2.index + '</span></li>');
        if (m2[0].length === 0) g2.lastIndex++;
        if (idx >= 200) { list.push('<li class="rt-more">…仅显示前 200 条</li>'); break; }
      }
      output.innerHTML += '<ol class="rt-list">' + list.join('') + '</ol>';
      setMsg('rt-msg', '✅ 匹配完成，共 ' + count + ' 处');
    });

    clearBtn.addEventListener('click', function () {
      patternEl.value = ''; flagsEl.value = 'g'; inputEl.value = '';
      output.innerHTML = ''; setMsg('rt-msg', '');
    });
  }

  /* ================= 3. 个税计算器 ================= */
  function initTaxCalc() {
    var runBtn = $('tc-run');
    if (!runBtn) return;
    // 综合所得按月换算后的税率表（月度）
    var BRACKETS = [
      { up: 3000, rate: 0.03, quick: 0 },
      { up: 12000, rate: 0.10, quick: 210 },
      { up: 25000, rate: 0.20, quick: 1410 },
      { up: 35000, rate: 0.25, quick: 2660 },
      { up: 55000, rate: 0.30, quick: 4410 },
      { up: 80000, rate: 0.35, quick: 7160 },
      { up: Infinity, rate: 0.45, quick: 15160 }
    ];
    function calcMonthlyTax(taxable) {
      if (taxable <= 0) return { tax: 0, rate: 0, quick: 0 };
      for (var i = 0; i < BRACKETS.length; i++) {
        if (taxable <= BRACKETS[i].up) {
          var tax = taxable * BRACKETS[i].rate - BRACKETS[i].quick;
          return { tax: Math.max(0, Math.round(tax * 100) / 100), rate: BRACKETS[i].rate, quick: BRACKETS[i].quick };
        }
      }
      return { tax: 0, rate: 0, quick: 0 };
    }
    function num(id) {
      var v = parseFloat($(id).value);
      return isNaN(v) || v < 0 ? 0 : v;
    }
    runBtn.addEventListener('click', function () {
      var salary = num('tc-salary');
      var insurance = num('tc-insurance');
      var deduction = num('tc-deduction');
      var bonus = num('tc-bonus');
      var taxable = salary - 5000 - insurance - deduction;  // 月度应纳税所得额
      var m = calcMonthlyTax(taxable);
      var monthlyTax = m.tax;
      // 年终奖单独计税：奖金 ÷ 12 找税率，再全额 × 税率 - 速算扣除
      var bonusTax = 0;
      if (bonus > 0) {
        var avg = bonus / 12;
        var bm = calcMonthlyTax(avg);
        bonusTax = Math.max(0, Math.round((bonus * bm.rate - bm.quick) * 100) / 100);
      }
      var net = salary - insurance - monthlyTax;
      var yearTax = Math.round((monthlyTax * 12 + bonusTax) * 100) / 100;
      function set(id, v) { var el = $(id); if (el) el.textContent = v; }
      set('tc-tax', '¥' + monthlyTax.toFixed(2));
      set('tc-net', '¥' + net.toFixed(2));
      set('tc-rate', (m.rate * 100).toFixed(0) + '%');
      set('tc-year', '¥' + yearTax.toFixed(2));
      var note = $('tc-note');
      if (!note) {
        note = document.createElement('div');
        note.id = 'tc-note';
        note.className = 'tool-usage';
        $('tc-result').parentNode.appendChild(note);
      }
      note.innerHTML = '<strong>📌 说明：</strong>按现行个税政策（起征点 5000 元/月）估算' +
        (bonus > 0 ? '，其中年终奖已按「全年一次性奖金」单独计税' : '') +
        '。实际扣缴以单位申报为准。';
    });
  }

  /* ================= 4. 时区转换 ================= */
  function initTimezoneConvert() {
    var dtEl = $('tz-datetime');
    if (!dtEl) return;
    var runBtn = $('tz-run');
    var nowBtn = $('tz-now');
    var listEl = $('tz-list');
    var CITIES = [
      { name: '北京（中国）', zone: 'Asia/Shanghai', flag: '🇨🇳' },
      { name: '东京（日本）', zone: 'Asia/Tokyo', flag: '🇯🇵' },
      { name: '首尔（韩国）', zone: 'Asia/Seoul', flag: '🇰🇷' },
      { name: '新加坡', zone: 'Asia/Singapore', flag: '🇸🇬' },
      { name: '迪拜（阿联酋）', zone: 'Asia/Dubai', flag: '🇦🇪' },
      { name: '莫斯科（俄罗斯）', zone: 'Europe/Moscow', flag: '🇷🇺' },
      { name: '柏林（德国）', zone: 'Europe/Berlin', flag: '🇩🇪' },
      { name: '巴黎（法国）', zone: 'Europe/Paris', flag: '🇫🇷' },
      { name: '伦敦（英国）', zone: 'Europe/London', flag: '🇬🇧' },
      { name: '纽约（美国）', zone: 'America/New_York', flag: '🇺🇸' },
      { name: '洛杉矶（美国）', zone: 'America/Los_Angeles', flag: '🇺🇸' },
      { name: '悉尼（澳大利亚）', zone: 'Australia/Sydney', flag: '🇦🇺' },
      { name: '奥克兰（新西兰）', zone: 'Pacific/Auckland', flag: '🇳🇿' },
      { name: '中国标准时间', zone: 'Asia/Shanghai', flag: '🕐' }
    ];
    function fmt(date, zone) {
      try {
        return new Intl.DateTimeFormat('zh-CN', {
          timeZone: zone, year: 'numeric', month: '2-digit', day: '2-digit',
          hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
        }).format(date);
      } catch (e) { return '—'; }
    }
    function render(date) {
      var rows = CITIES.map(function (c) {
        var t = fmt(date, c.zone);
        var parts = t.split(' ').filter(Boolean);
        var datePart = parts[0] || '';
        var timePart = parts[1] || '';
        var isBeijing = c.zone === 'Asia/Shanghai';
        return '<div class="tz-row' + (isBeijing ? ' tz-beijing' : '') + '">' +
          '<span class="tz-flag">' + c.flag + '</span>' +
          '<span class="tz-name">' + c.name + '</span>' +
          '<span class="tz-date">' + datePart + '</span>' +
          '<span class="tz-time"><strong>' + timePart + '</strong></span>' +
          '</div>';
      }).join('');
      listEl.innerHTML = rows;
    }
    function localNow() {
      var d = new Date();
      var pad = function (n) { return (n < 10 ? '0' : '') + n; };
      return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) +
        'T' + pad(d.getHours()) + ':' + pad(d.getMinutes());
    }
    if (!dtEl.value) dtEl.value = localNow();
    runBtn.addEventListener('click', function () {
      if (!dtEl.value) { dtEl.value = localNow(); }
      render(new Date(dtEl.value));
    });
    nowBtn.addEventListener('click', function () {
      dtEl.value = localNow();
      render(new Date());
    });
    render(new Date());
  }

  /* ============ 注册：DOMContentLoaded 逐个执行 ============ */
  var inits = [
    initNineGrid, initRegexTester, initTaxCalc, initTimezoneConvert
  ];
  function runAll() {
    inits.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error('tools-v3 init error:', e); } });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runAll);
  } else {
    runAll();
  }
})();

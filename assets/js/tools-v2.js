/* tools-v2.js — AI 工具箱 第二批 12 个新工具（纯前端、零 API、本地运行）
 * 字数统计 / JSON格式化 / Base64编解码 / URL编解码 / 时间戳转换 / 随机密码 /
 * UUID生成 / MD5哈希 / 简繁转换 / Markdown转HTML / 图片格式转换 / 年龄计算
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

  /* ================= 1. 字数统计 ================= */
  function initWordCount() {
    var input = $('wc-input');
    if (!input) return;
    function update() {
      var text = input.value;
      var cn = (text.match(/[\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef]/g) || []).length;
      var en = (text.match(/[A-Za-z0-9]+/g) || []).length;
      var words = cn + en;
      var chars = text.length;
      var charsNo = text.replace(/\s/g, '').length;
      var lines = text ? text.split('\n').length : 0;
      var paras = text ? text.split(/\n\s*\n/).filter(function (p) { return p.trim(); }).length : 0;
      var readMin = words ? Math.max(1, Math.round(words / 300)) : 0;
      function set(id, v) { var el = $(id); if (el) el.textContent = v; }
      set('wc-words', words);
      set('wc-chars', chars);
      set('wc-chars-no', charsNo);
      set('wc-lines', lines);
      set('wc-paras', paras);
      set('wc-readtime', words ? readMin + ' 分钟' : '0 分钟');
    }
    input.addEventListener('input', update);
    var clear = $('wc-clear');
    if (clear) clear.addEventListener('click', function () { input.value = ''; update(); input.focus(); });
    update();
  }

  /* ================= 2. JSON 格式化 ================= */
  function initJsonFormatter() {
    var input = $('jf-input');
    if (!input) return;
    var output = $('jf-output');
    function parse() {
      var text = input.value.trim();
      if (!text) { setMsg('jf-msg', '请先输入 JSON 内容', true); return null; }
      try { return JSON.parse(text); }
      catch (e) {
        var m = String(e.message).match(/position\s*(\d+)/i);
        var hint = m ? '（第 ' + m[1] + ' 个字符附近）' : '';
        setMsg('jf-msg', '❌ JSON 解析失败：' + e.message + hint, true);
        return null;
      }
    }
    var fmt = $('jf-format');
    if (fmt) fmt.addEventListener('click', function () {
      var obj = parse(); if (obj === null) return;
      output.value = JSON.stringify(obj, null, 2);
      setMsg('jf-msg', '✅ 格式化完成');
    });
    var min = $('jf-minify');
    if (min) min.addEventListener('click', function () {
      var obj = parse(); if (obj === null) return;
      output.value = JSON.stringify(obj);
      setMsg('jf-msg', '✅ 压缩完成');
    });
    var val = $('jf-validate');
    if (val) val.addEventListener('click', function () {
      var obj = parse(); if (obj === null) return;
      setMsg('jf-msg', '✅ 校验通过：这是一个合法 JSON（顶层类型 ' + (Array.isArray(obj) ? '数组' : typeof obj === 'object' ? '对象' : typeof obj) + '）');
    });
    var copy = $('jf-copy');
    if (copy) copy.addEventListener('click', function () {
      if (!output.value) { setMsg('jf-msg', '没有可复制的内容', true); return; }
      copyText(output.value, copy);
      setMsg('jf-msg', '✅ 已复制到剪贴板');
    });
  }

  /* ================= 3. Base64 编解码 ================= */
  function initBase64Convert() {
    var input = $('b64-input');
    if (!input) return;
    var output = $('b64-output');
    var mode = $('b64-mode');
    function run() {
      var text = input.value;
      if (!text) { setMsg('b64-msg', '请输入内容', true); return; }
      try {
        if (mode.value === 'encode') {
          var bytes = new TextEncoder().encode(text);
          var bin = '';
          for (var i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
          output.value = btoa(bin);
          setMsg('b64-msg', '✅ 编码完成');
        } else {
          var bin2 = atob(text.replace(/\s+/g, ''));
          var bytes2 = new Uint8Array(bin2.length);
          for (var j = 0; j < bin2.length; j++) bytes2[j] = bin2.charCodeAt(j);
          output.value = new TextDecoder('utf-8', { fatal: false }).decode(bytes2);
          setMsg('b64-msg', '✅ 解码完成（按 UTF-8 解码）');
        }
      } catch (e) {
        setMsg('b64-msg', '❌ 转换失败：' + e.message + '（Base64 字符串可能不合法）', true);
      }
    }
    $('b64-run').addEventListener('click', run);
    var swap = $('b64-swap');
    if (swap) swap.addEventListener('click', function () {
      mode.value = mode.value === 'encode' ? 'decode' : 'encode';
      input.value = output.value;
      output.value = '';
      setMsg('b64-msg', '已切换方向');
      run();
    });
    var copy = $('b64-copy');
    if (copy) copy.addEventListener('click', function () {
      if (!output.value) { setMsg('b64-msg', '没有可复制的内容', true); return; }
      copyText(output.value, copy);
    });
  }

  /* ================= 4. URL 编解码 ================= */
  function initUrlEncode() {
    var input = $('ue-input');
    if (!input) return;
    var output = $('ue-output');
    var mode = $('ue-mode');
    function run() {
      var text = input.value;
      if (!text) { setMsg('ue-msg', '请输入内容', true); return; }
      try {
        if (mode.value === 'encode') {
          output.value = encodeURIComponent(text);
          setMsg('ue-msg', '✅ 编码完成（encodeURIComponent 完整编码）');
        } else {
          output.value = decodeURIComponent(text);
          setMsg('ue-msg', '✅ 解码完成');
        }
      } catch (e) {
        setMsg('ue-msg', '❌ 解码失败：' + e.message + '（可能不是合法的 URL 编码串）', true);
      }
    }
    $('ue-run').addEventListener('click', run);
    var swap = $('ue-swap');
    if (swap) swap.addEventListener('click', function () {
      mode.value = mode.value === 'encode' ? 'decode' : 'encode';
      input.value = output.value;
      output.value = '';
      setMsg('ue-msg', '已切换方向');
      run();
    });
    var copy = $('ue-copy');
    if (copy) copy.addEventListener('click', function () {
      if (!output.value) { setMsg('ue-msg', '没有可复制的内容', true); return; }
      copyText(output.value, copy);
    });
  }

  /* ================= 5. 时间戳转换 ================= */
  function initTimestampConvert() {
    var input = $('ts-input');
    if (!input) return;
    var output = $('ts-output');
    var unit = $('ts-unit');
    function pad(n) { return (n < 10 ? '0' : '') + n; }
    function fmt(d) {
      return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()) +
        ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds());
    }
    function convert() {
      var val = input.value.trim();
      if (!val || isNaN(val)) { output.value = '请输入有效的时间戳数字'; return; }
      var ms = unit.value === 's' ? parseInt(val, 10) * 1000 : parseInt(val, 10);
      var d = new Date(ms);
      if (isNaN(d.getTime())) { output.value = '无效的时间戳（超出范围）'; return; }
      var weekdays = ['日', '一', '二', '三', '四', '五', '六'];
      output.value =
        '本地时间：' + fmt(d) + '（星期' + weekdays[d.getDay()] + '）\n' +
        'UTC 时间：' + d.toUTCString() + '\n' +
        'ISO 8601：' + d.toISOString() + '\n' +
        '时间戳(秒)：' + Math.floor(ms / 1000) + '\n' +
        '时间戳(毫秒)：' + ms;
    }
    $('ts-convert').addEventListener('click', convert);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') convert(); });
    var now = $('ts-now');
    if (now) now.addEventListener('click', function () {
      var t = Date.now();
      input.value = unit.value === 's' ? Math.floor(t / 1000) : t;
      convert();
    });
  }

  /* ================= 6. 随机密码生成 ================= */
  function initPasswordGenerator() {
    var lenEl = $('pg-length');
    if (!lenEl) return;
    var lenVal = $('pg-length-val');
    var out = $('pg-output');
    var strength = $('pg-strength');
    var upper = $('pg-upper'), lower = $('pg-lower'), digit = $('pg-digit'), symbol = $('pg-symbol');
    function rand(n) {
      var buf = new Uint32Array(1);
      crypto.getRandomValues(buf);
      return buf[0] % n;
    }
    function gen() {
      var len = parseInt(lenEl.value, 10);
      var pool = '';
      var sets = [];
      if (upper.checked) { pool += 'ABCDEFGHJKLMNPQRSTUVWXYZ'; sets.push('ABCDEFGHJKLMNPQRSTUVWXYZ'); }
      if (lower.checked) { pool += 'abcdefghijkmnpqrstuvwxyz'; sets.push('abcdefghijkmnpqrstuvwxyz'); }
      if (digit.checked) { pool += '23456789'; sets.push('23456789'); }
      if (symbol.checked) { pool += '!@#$%^&*()_+-=[]{}|;:,.<>?'; sets.push('!@#$%^&*()_+-=[]{}|;:,.<>?'); }
      if (!pool) { out.value = ''; strength.textContent = '请至少勾选一种字符类型'; return; }
      var chars = [];
      // 确保每个勾选的集合至少出现一次
      sets.forEach(function (s) { chars.push(s[rand(s.length)]); });
      for (var i = chars.length; i < len; i++) chars.push(pool[rand(pool.length)]);
      // Fisher-Yates 洗牌
      for (var j = chars.length - 1; j > 0; j--) {
        var k = rand(j + 1);
        var tmp = chars[j]; chars[j] = chars[k]; chars[k] = tmp;
      }
      out.value = chars.join('');
      var entropy = len * Math.log2(pool.length);
      if (entropy >= 90) strength.textContent = '🟢 密码强度：极强（推荐用于重要账户）';
      else if (entropy >= 60) strength.textContent = '🟢 密码强度：强';
      else if (entropy >= 36) strength.textContent = '🟡 密码强度：中等（建议增加长度）';
      else strength.textContent = '🔴 密码强度：弱（请增加长度或字符类型）';
    }
    lenEl.addEventListener('input', function () { lenVal.textContent = lenEl.value; gen(); });
    [upper, lower, digit, symbol].forEach(function (c) { c.addEventListener('change', gen); });
    $('pg-gen').addEventListener('click', gen);
    var copy = $('pg-copy');
    if (copy) copy.addEventListener('click', function () {
      if (!out.value) return;
      copyText(out.value, copy);
    });
    gen();
  }

  /* ================= 7. UUID 生成器 ================= */
  function initUuidGenerator() {
    var countEl = $('ug-count');
    if (!countEl) return;
    var countVal = $('ug-count-val');
    var out = $('ug-output');
    var format = $('ug-format');
    function uuid() {
      if (crypto.randomUUID) return crypto.randomUUID();
      var b = new Uint8Array(16);
      crypto.getRandomValues(b);
      b[6] = (b[6] & 0x0f) | 0x40;
      b[8] = (b[8] & 0x3f) | 0x80;
      var hex = '';
      for (var i = 0; i < 16; i++) hex += (b[i] < 16 ? '0' : '') + b[i].toString(16);
      return hex.slice(0, 8) + '-' + hex.slice(8, 12) + '-' + hex.slice(12, 16) + '-' + hex.slice(16, 20) + '-' + hex.slice(20);
    }
    function formatUuid(u) {
      if (format.value === 'plain') return u.replace(/-/g, '');
      if (format.value === 'upper') return u.toUpperCase();
      if (format.value === 'braces') return '{' + u + '}';
      return u;
    }
    function gen() {
      var n = parseInt(countEl.value, 10);
      var lines = [];
      for (var i = 0; i < n; i++) lines.push(formatUuid(uuid()));
      out.value = lines.join('\n');
    }
    countEl.addEventListener('input', function () { countVal.textContent = countEl.value; gen(); });
    format.addEventListener('change', gen);
    $('ug-gen').addEventListener('click', gen);
    var copy = $('ug-copy');
    if (copy) copy.addEventListener('click', function () {
      if (!out.value) return;
      copyText(out.value, copy);
    });
    gen();
  }

  /* ================= 8. MD5 哈希 ================= */
  function initMd5Hash() {
    var input = $('md5-input');
    if (!input) return;
    var out = $('md5-output');
    var format = $('md5-format');

    /* 标准 MD5 实现（RFC 1321），支持 UTF-8 */
    function md5(str) {
      function utf8Bytes(s) {
        var bytes = [];
        for (var i = 0; i < s.length; i++) {
          var c = s.charCodeAt(i);
          if (c < 0x80) bytes.push(c);
          else if (c < 0x800) { bytes.push(0xc0 | (c >> 6), 0x80 | (c & 0x3f)); }
          else if (c < 0xd800 || c >= 0xe000) { bytes.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 0x3f), 0x80 | (c & 0x3f)); }
          else { c = 0x10000 + (((c & 0x3ff) << 10) | (s.charCodeAt(++i) & 0x3ff)); bytes.push(0xf0 | (c >> 18), 0x80 | ((c >> 12) & 0x3f), 0x80 | ((c >> 6) & 0x3f), 0x80 | (c & 0x3f)); }
        }
        return bytes;
      }
      function toWords(bytes) {
        var words = [];
        for (var i = 0; i < bytes.length; i += 4) {
          words.push((bytes[i]) | (bytes[i + 1] << 8) | (bytes[i + 2] << 16) | (bytes[i + 3] << 24));
        }
        return words;
      }
      function add32(a, b) { return (a + b) & 0xffffffff; }
      function rol(n, s) { return (n << s) | (n >>> (32 - s)); }
      var bytes = utf8Bytes(str);
      var bitLen = bytes.length * 8;
      bytes.push(0x80);
      while (bytes.length % 64 !== 56) bytes.push(0);
      var words = toWords(bytes);
      words.push(bitLen >>> 0, Math.floor(bitLen / 0x100000000) >>> 0);
      var a0 = 0x67452301, b0 = 0xefcdab89, c0 = 0x98badcfe, d0 = 0x10325476;
      var K = [0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391];
      var S = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21];
      for (var i = 0; i < words.length; i += 16) {
        var A = a0, B = b0, C = c0, D = d0;
        var M = words.slice(i, i + 16);
        for (var j = 0; j < 64; j++) {
          var F, g;
          if (j < 16) { F = (B & C) | (~B & D); g = j; }
          else if (j < 32) { F = (D & B) | (~D & C); g = (5 * j + 1) % 16; }
          else if (j < 48) { F = B ^ C ^ D; g = (3 * j + 5) % 16; }
          else { F = C ^ (B | ~D); g = (7 * j) % 16; }
          var tmp = D;
          D = C;
          C = B;
          B = add32(B, rol(add32(add32(A, F), add32(K[j], M[g])), S[j]));
          A = tmp;
        }
        a0 = add32(a0, A); b0 = add32(b0, B); c0 = add32(c0, C); d0 = add32(d0, D);
      }
      function hex(n) {
        var s = '';
        for (var i = 0; i < 4; i++) {
          var b = (n >>> (i * 8)) & 0xff;
          s += (b < 16 ? '0' : '') + b.toString(16);
        }
        return s;
      }
      return hex(a0) + hex(b0) + hex(c0) + hex(d0);
    }

    function run() {
      var text = input.value;
      if (!text) { out.value = '请输入文本'; return; }
      var h = md5(text);
      if (format.value === '32upper') h = h.toUpperCase();
      else if (format.value === '16lower') h = h.slice(8, 24);
      else if (format.value === '16upper') h = h.slice(8, 24).toUpperCase();
      out.value = h;
    }
    $('md5-run').addEventListener('click', run);
    var copy = $('md5-copy');
    if (copy) copy.addEventListener('click', function () {
      if (!out.value) return;
      copyText(out.value, copy);
    });
  }

  /* ================= 9. 简体繁体转换 ================= */
  function initZhConvert() {
    var input = $('zh-input');
    if (!input) return;
    if (!window.ZH_MAP) return; // zh-map.js 未加载
    var output = $('zh-output');
    var mode = $('zh-mode');
    function convert() {
      var text = input.value;
      if (!text) { output.value = ''; return; }
      var words = mode.value === 's2t' ? window.ZH_MAP.s2tWord : window.ZH_MAP.t2sWord;
      var chars = mode.value === 's2t' ? window.ZH_MAP.s2tChar : window.ZH_MAP.t2sChar;
      var keys = Object.keys(words).sort(function (a, b) { return b.length - a.length; });
      var out = text;
      for (var i = 0; i < keys.length; i++) {
        var w = words[keys[i]];
        if (w !== keys[i]) out = out.split(keys[i]).join(w);
      }
      var arr = out.split('');
      for (var j = 0; j < arr.length; j++) {
        if (chars[arr[j]]) arr[j] = chars[arr[j]];
      }
      output.value = arr.join('');
    }
    $('zh-run').addEventListener('click', convert);
    var swap = $('zh-swap');
    if (swap) swap.addEventListener('click', function () {
      mode.value = mode.value === 's2t' ? 't2s' : 's2t';
      input.value = output.value;
      convert();
    });
    var copy = $('zh-copy');
    if (copy) copy.addEventListener('click', function () {
      if (!output.value) return;
      copyText(output.value, copy);
    });
  }

  /* ================= 10. Markdown 转 HTML ================= */
  function initMdToHtml() {
    var input = $('md-input');
    if (!input) return;
    var output = $('md-output');
    var preview = $('md-preview');

    function esc(s) {
      return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
    function inline(s) {
      // 行内代码
      s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
      // 图片 ![alt](url)
      s = s.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, '<img src="$2" alt="$1" loading="lazy">');
      // 链接 [text](url)
      s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
      // 粗体
      s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>').replace(/__([^_]+)__/g, '<strong>$1</strong>');
      // 斜体
      s = s.replace(/\*([^*]+)\*/g, '<em>$1</em>').replace(/_([^_]+)_/g, '<em>$1</em>');
      // 删除线
      s = s.replace(/~~([^~]+)~~/g, '<del>$1</del>');
      return s;
    }
    function render() {
      var text = input.value;
      var lines = text.split('\n');
      var html = [];
      var i = 0, inCode = false, codeBuf = [], inTable = false, tableBuf = [];
      function flushTable() {
        if (!tableBuf.length) return;
        var rows = tableBuf.map(function (r) {
          var cells = r.split('|').slice(1, -1).map(function (c) { return c.trim(); });
          return '<tr>' + cells.map(function (c) { return '<td>' + inline(c) + '</td>'; }).join('') + '</tr>';
        });
        html.push('<table><thead>' + rows[0] + '</thead><tbody>' + rows.slice(2).join('') + '</tbody></table>');
        tableBuf = [];
      }
      while (i < lines.length) {
        var line = lines[i];
        // 代码块
        if (/^```/.test(line)) {
          flushTable();
          if (inCode) { html.push('<pre><code>' + codeBuf.join('\n') + '</code></pre>'); codeBuf = []; inCode = false; }
          else inCode = true;
          i++; continue;
        }
        if (inCode) { codeBuf.push(esc(line)); i++; continue; }
        // 表格（连续两行 + 分隔行）
        if (/\|.+\|/.test(line) && i + 1 < lines.length && /^\s*\|?[\s:|-]+\|?\s*$/.test(lines[i + 1]) && lines[i + 1].indexOf('-') >= 0) {
          flushTable();
          tableBuf = [line, lines[i + 1]];
          i += 2;
          while (i < lines.length && /\|.+\|/.test(lines[i])) { tableBuf.push(lines[i]); i++; }
          flushTable();
          continue;
        }
        flushTable();
        // 标题
        var h = line.match(/^(#{1,6})\s+(.*)/);
        if (h) { html.push('<h' + h[1].length + '>' + inline(h[2]) + '</h' + h[1].length + '>'); i++; continue; }
        // 分隔线
        if (/^\s*(-{3,}|\*{3,})\s*$/.test(line)) { html.push('<hr>'); i++; continue; }
        // 引用
        if (/^\s*>\s?/.test(line)) {
          var quote = [];
          while (i < lines.length && /^\s*>\s?/.test(lines[i])) { quote.push(lines[i].replace(/^\s*>\s?/, '')); i++; }
          html.push('<blockquote>' + quote.map(function (q) { return '<p>' + inline(q) + '</p>'; }).join('') + '</blockquote>');
          continue;
        }
        // 无序列表
        if (/^\s*[-*+]\s+/.test(line)) {
          var ul = [];
          while (i < lines.length && /^\s*[-*+]\s+/.test(lines[i])) { ul.push('<li>' + inline(lines[i].replace(/^\s*[-*+]\s+/, '')) + '</li>'); i++; }
          html.push('<ul>' + ul.join('') + '</ul>');
          continue;
        }
        // 有序列表
        if (/^\s*\d+\.\s+/.test(line)) {
          var ol = [];
          while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) { ol.push('<li>' + inline(lines[i].replace(/^\s*\d+\.\s+/, '')) + '</li>'); i++; }
          html.push('<ol>' + ol.join('') + '</ol>');
          continue;
        }
        // 空行
        if (/^\s*$/.test(line)) { i++; continue; }
        // 普通段落（合并到下一个空行）
        var para = [line];
        i++;
        while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^(#{1,6}\s|```|\s*>\s?|\s*[-*+]\s+|\s*\d+\.\s+)/.test(lines[i])) { para.push(lines[i]); i++; }
        html.push('<p>' + inline(para.join(' ')) + '</p>');
      }
      if (inCode) html.push('<pre><code>' + codeBuf.join('\n') + '</code></pre>');
      flushTable();
      var out = html.join('\n');
      output.value = out;
      preview.innerHTML = out || '<p style="color:#9e9590">输入 Markdown 后这里会显示渲染效果</p>';
    }
    input.addEventListener('input', render);
    var copy = $('md-copy-html');
    if (copy) copy.addEventListener('click', function () {
      if (!output.value) return;
      copyText(output.value, copy);
    });
    var clear = $('md-copy-md');
    if (clear) clear.addEventListener('click', function () {
      input.value = '';
      render();
      input.focus();
    });
    render();
  }

  /* ================= 11. 图片格式转换 ================= */
  function initImageConvert() {
    var drop = $('ic-drop');
    if (!drop) return;
    var fileInput = $('ic-file');
    var format = $('ic-format');
    var quality = $('ic-quality');
    var qualityVal = $('ic-quality-val');
    var list = $('ic-list');
    var msg = $('ic-msg');
    var files = [];

    drop.addEventListener('click', function () { fileInput.click(); });
    drop.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); fileInput.click(); } });
    drop.addEventListener('dragover', function (e) { e.preventDefault(); drop.style.borderColor = 'var(--clr-primary)'; });
    drop.addEventListener('dragleave', function () { drop.style.borderColor = ''; });
    drop.addEventListener('drop', function (e) {
      e.preventDefault(); drop.style.borderColor = '';
      if (e.dataTransfer.files.length) handleFiles(e.dataTransfer.files);
    });
    fileInput.addEventListener('change', function () {
      if (fileInput.files.length) handleFiles(fileInput.files);
    });
    quality.addEventListener('input', function () { qualityVal.textContent = quality.value; refresh(); });

    function handleFiles(fileList) {
      files = Array.prototype.slice.call(fileList).filter(function (f) { return f.type.match(/^image\//); });
      if (!files.length) { msg.textContent = '请选择图片文件'; return; }
      msg.textContent = '已添加 ' + files.length + ' 张图片，正在转换…';
      refresh();
    }
    function refresh() {
      list.innerHTML = '';
      if (!files.length) { msg.textContent = '点击上方区域选择图片'; return; }
      msg.textContent = '共 ' + files.length + ' 张图片，点击卡片下载转换结果';
      files.forEach(function (file, idx) {
        var card = document.createElement('div');
        card.className = 'ic-card';
        var img = document.createElement('img');
        img.alt = file.name;
        img.src = URL.createObjectURL(file);
        card.appendChild(img);
        var info = document.createElement('p');
        info.className = 'ic-name';
        info.textContent = file.name + '（' + (file.size / 1024).toFixed(1) + ' KB）';
        card.appendChild(info);
        var dl = document.createElement('a');
        dl.className = 'tool-btn ic-dl';
        dl.textContent = '⬇ 下载';
        dl.href = '#';
        card.appendChild(dl);
        list.appendChild(card);
        var image = new Image();
        image.onload = function () {
          var canvas = document.createElement('canvas');
          canvas.width = image.naturalWidth;
          canvas.height = image.naturalHeight;
          var ctx = canvas.getContext('2d');
          ctx.drawImage(image, 0, 0);
          var mime = format.value;
          canvas.toBlob(function (blob) {
            if (!blob) { msg.textContent = '转换失败：' + file.name; return; }
            var ext = mime === 'image/jpeg' ? 'jpg' : mime === 'image/webp' ? 'webp' : 'png';
            var url = URL.createObjectURL(blob);
            dl.href = url;
            dl.download = file.name.replace(/\.[^.]+$/, '') + '.' + ext;
            dl.textContent = '⬇ 下载 ' + ext.toUpperCase() + '（' + (blob.size / 1024).toFixed(1) + ' KB）';
          }, mime, parseInt(quality.value, 10) / 100);
        };
        image.src = URL.createObjectURL(file);
      });
    }
  }

  /* ================= 12. 年龄计算器 ================= */
  function initAgeCalc() {
    var dateEl = $('ac-date');
    if (!dateEl) return;
    var zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪'];
    var constellations = [
      [1, 20, '水瓶座'], [2, 19, '双鱼座'], [3, 21, '白羊座'], [4, 20, '金牛座'],
      [5, 21, '双子座'], [6, 22, '巨蟹座'], [7, 23, '狮子座'], [8, 23, '处女座'],
      [9, 23, '天秤座'], [10, 24, '天蝎座'], [11, 23, '射手座'], [12, 22, '摩羯座']
    ];
    function getConstellation(m, d) {
      for (var i = 0; i < 12; i++) {
        var c = constellations[i];
        var next = constellations[(i + 1) % 12];
        if ((m === c[0] && d >= c[1]) || (m === next[0] && d < next[1])) return c[2];
      }
      return '摩羯座';
    }
    function run() {
      var val = dateEl.value;
      if (!val) return;
      var birth = new Date(val + 'T00:00:00');
      var now = new Date();
      if (isNaN(birth.getTime()) || birth > now) {
        setAge('ac-age', '—'); setAge('ac-xu', '—'); setAge('ac-days', '—'); setAge('ac-zodiac', '—'); setAge('ac-constellation', '—');
        return;
      }
      // 周岁
      var age = now.getFullYear() - birth.getFullYear();
      var mDiff = now.getMonth() - birth.getMonth();
      if (mDiff < 0 || (mDiff === 0 && now.getDate() < birth.getDate())) age--;
      // 虚岁（出生算 1 岁，每过农历年 +1；简化为公历年）
      var xu = now.getFullYear() - birth.getFullYear() + 1;
      // 已活天数
      var days = Math.floor((now.getTime() - birth.getTime()) / 86400000);
      // 生肖（按公历年近似，农历年初一前会有偏差）
      var zodiac = zodiacs[(birth.getFullYear() - 4) % 12];
      var constel = getConstellation(birth.getMonth() + 1, birth.getDate());
      setAge('ac-age', age + ' 岁');
      setAge('ac-xu', xu + ' 岁');
      setAge('ac-days', days.toLocaleString() + ' 天');
      setAge('ac-zodiac', zodiac);
      setAge('ac-constellation', constel);
    }
    function setAge(id, v) { var el = $(id); if (el) el.textContent = v; }
    $('ac-run').addEventListener('click', run);
    run();
  }

  /* ============ 注册：DOMContentLoaded 逐个执行 ============ */
  var inits = [
    initWordCount, initJsonFormatter, initBase64Convert, initUrlEncode,
    initTimestampConvert, initPasswordGenerator, initUuidGenerator, initMd5Hash,
    initZhConvert, initMdToHtml, initImageConvert, initAgeCalc
  ];
  function runAll() {
    inits.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error('tools-v2 init error:', e); } });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runAll);
  } else {
    runAll();
  }
})();

/* tools-v5.js — AI 工具箱 第五批 4 个新工具（纯前端、零 API、本地运行）
 * 图片像素化 / 证件照尺寸 / 亲戚称呼计算器 / 节气查询
 * 每个 init 函数按页面专属元素守卫，未命中即 no-op。
 */
(function () {
  'use strict';

  function $(id) { return document.getElementById(id); }

  /* ---------- 通用 ---------- */
  function setMsg(id, text, isErr) {
    var el = $(id);
    if (!el) return;
    el.textContent = text;
    el.className = 'tool-msg' + (isErr ? ' msg-error' : ' msg-ok');
  }

  /* ================= 1. 图片像素化 ================= */
  function initImagePixelate() {
    var fileEl = $('ip-file');
    if (!fileEl) return;
    var canvas = $('ip-canvas');
    var ctx = canvas.getContext('2d');
    var img = null;
    var blockEl = $('ip-block');
    var blockVal = $('ip-block-val');

    blockEl.addEventListener('input', function () {
      if (blockVal) blockVal.textContent = blockEl.value + 'px';
      if (img) render();
    });

    fileEl.addEventListener('change', function () {
      var f = fileEl.files && fileEl.files[0];
      if (!f) return;
      var url = URL.createObjectURL(f);
      var tmp = new Image();
      tmp.onload = function () {
        img = tmp;
        URL.revokeObjectURL(url);
        canvas.width = Math.min(img.width, 600);
        canvas.height = Math.round(img.height * canvas.width / img.width);
        setMsg('ip-msg', '✅ 已载入 ' + f.name + '，调节像素块大小实时预览');
        render();
      };
      tmp.onerror = function () { setMsg('ip-msg', '❌ 图片加载失败，换一张试试', true); };
      tmp.src = url;
    });

    function render() {
      if (!img) return;
      var block = parseInt(blockEl.value, 10) || 10;
      ctx.imageSmoothingEnabled = false;
      // 先缩小到像素块粒度，再放大回画布大小（经典像素化）
      var bw = Math.max(2, Math.round(canvas.width / block));
      var bh = Math.max(2, Math.round(canvas.height / block));
      var small = document.createElement('canvas');
      small.width = bw; small.height = bh;
      var sctx = small.getContext('2d');
      sctx.imageSmoothingEnabled = false;
      sctx.drawImage(img, 0, 0, bw, bh);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(small, 0, 0, canvas.width, canvas.height);
    }

    $('ip-render').addEventListener('click', function () {
      if (!img) { setMsg('ip-msg', '⚠️ 请先选择一张图片', true); return; }
      render();
      setMsg('ip-msg', '✅ 已像素化（块大小 ' + blockEl.value + 'px），点「下载 PNG」保存');
    });
    $('ip-download').addEventListener('click', function () {
      if (!img) { setMsg('ip-msg', '⚠️ 请先生成像素图', true); return; }
      render();
      var a = document.createElement('a');
      a.href = canvas.toDataURL('image/png');
      a.download = 'pixelated.png';
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
    });
  }

  /* ================= 2. 证件照尺寸 ================= */
  function initIdPhoto() {
    var fileEl = $('idp-file');
    if (!fileEl) return;
    var canvas = $('idp-canvas');
    var ctx = canvas.getContext('2d');
    var img = null;
    var SIZES = {
      '1inch': [295, 413], 'small1': [260, 378], '2inch': [413, 579],
      'small2': [390, 567], 'passport': [390, 567]
    };

    fileEl.addEventListener('change', function () {
      var f = fileEl.files && fileEl.files[0];
      if (!f) return;
      var url = URL.createObjectURL(f);
      var tmp = new Image();
      tmp.onload = function () {
        img = tmp;
        URL.revokeObjectURL(url);
        setMsg('idp-msg', '✅ 已载入 ' + f.name + '（' + img.width + '×' + img.height + '），选好类型点「生成证件照」');
        render();
      };
      tmp.onerror = function () { setMsg('idp-msg', '❌ 图片加载失败，换一张试试', true); };
      tmp.src = url;
    });

    function render() {
      if (!img) return;
      var size = SIZES[$('idp-type').value] || SIZES['1inch'];
      canvas.width = size[0]; canvas.height = size[1];
      var bg = $('idp-bg').value;
      ctx.fillStyle = bg === 'keep' ? '#fff' : bg;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      // 覆盖式裁剪（cover）：按短边比例放大居中裁切
      var scale = Math.max(canvas.width / img.width, canvas.height / img.height);
      var dw = img.width * scale, dh = img.height * scale;
      var dx = (canvas.width - dw) / 2, dy = (canvas.height - dh) / 2;
      if (bg === 'keep') {
        ctx.drawImage(img, dx, dy, dw, dh);
      } else {
        // 换底色：把非肤色区域替换。简化实现：整图绘制后做一次近肤色保留的混合
        ctx.drawImage(img, dx, dy, dw, dh);
        try {
          var idata = ctx.getImageData(0, 0, canvas.width, canvas.height);
          var d = idata.data;
          var bgRGB = hexToRgb(bg);
          for (var i = 0; i < d.length; i += 4) {
            var r = d[i], g = d[i + 1], b = d[i + 2];
            // 非肤色（简单阈值：红色通道明显高于蓝/绿，或整体很亮/很暗）→ 换背景
            var isSkin = (r > 95 && g > 40 && b > 20 && (r - g) > 15 && (r - b) > 15 && r > b * 1.2);
            if (!isSkin) {
              d[i] = bgRGB[0]; d[i + 1] = bgRGB[1]; d[i + 2] = bgRGB[2];
            }
          }
          ctx.putImageData(idata, 0, 0);
        } catch (e) { /* 跨域等异常时保持原图 */ }
      }
    }
    function hexToRgb(hex) {
      var h = hex.replace('#', '');
      return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
    }

    $('idp-render').addEventListener('click', function () {
      if (!img) { setMsg('idp-msg', '⚠️ 请先选择一张照片', true); return; }
      render();
      var size = SIZES[$('idp-type').value];
      setMsg('idp-msg', '✅ 已生成 ' + size[0] + '×' + size[1] + 'px 证件照，点「下载 PNG」保存');
    });
    $('idp-download').addEventListener('click', function () {
      if (!img) { setMsg('idp-msg', '⚠️ 请先生成证件照', true); return; }
      render();
      var a = document.createElement('a');
      a.href = canvas.toDataURL('image/png');
      a.download = 'id-photo-' + $('idp-type').value + '.png';
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
    });
    // 类型/底色切换实时刷新
    ['idp-type', 'idp-bg'].forEach(function (id) {
      $(id).addEventListener('change', function () { if (img) render(); });
    });
  }

  /* ================= 3. 亲戚称呼计算器 ================= */
  function initRelativeCalc() {
    var addBtn = $('rc-add');
    if (!addBtn) return;
    var chips = $('rc-chips');
    var steps = [];   // 关系链，如 ['father', 'father']
    // 关系键 → 展示名（站在"我"的角度）
    var REL = [
      ['father', '爸爸'], ['mother', '妈妈'], ['husband', '老公'], ['wife', '老婆'],
      ['son', '儿子'], ['daughter', '女儿'],
      ['brother', '哥哥/弟弟'], ['sister', '姐姐/妹妹'],
      ['grandfather', '爷爷（父之父）'], ['grandmother', '奶奶（父之母）'],
      ['maternal-grandfather', '外公（母之父）'], ['maternal-grandmother', '外婆（母之母）'],
      ['uncle', '叔叔/伯伯（父之兄弟）'], ['aunt', '姑姑（父之姐妹）'],
      ['maternal-uncle', '舅舅（母之兄弟）'], ['maternal-aunt', '姨妈（母之姐妹）'],
      ['nephew', '侄子/外甥'], ['niece', '侄女/外甥女']
    ];
    // 关系链 → 称呼（简化版映射表，覆盖常用组合）
    var MAP = {
      'self': { self: '我', 'self-f': '我' },
      'father': { self: '爸爸', 'self-f': '爸爸' },
      'mother': { self: '妈妈', 'self-f': '妈妈' },
      'husband': { self: '老公', 'self-f': '老公' },
      'wife': { self: '老婆', 'self-f': '老婆' },
      'father,father': { self: '爷爷', 'self-f': '爷爷' },
      'father,mother': { self: '奶奶', 'self-f': '奶奶' },
      'mother,father': { self: '外公', 'self-f': '外公' },
      'mother,mother': { self: '外婆', 'self-f': '外婆' },
      'father,brother': { self: '伯父/叔叔（按年龄分）', 'self-f': '伯父/叔叔' },
      'father,brother,wife': { self: '伯母/婶婶', 'self-f': '伯母/婶婶' },
      'father,sister': { self: '姑姑', 'self-f': '姑姑' },
      'father,sister,husband': { self: '姑父', 'self-f': '姑父' },
      'mother,brother': { self: '舅舅', 'self-f': '舅舅' },
      'mother,brother,wife': { self: '舅妈', 'self-f': '舅妈' },
      'mother,sister': { self: '姨妈', 'self-f': '姨妈' },
      'mother,sister,husband': { self: '姨父', 'self-f': '姨父' },
      'father,father,father': { self: '曾祖父/太爷爷', 'self-f': '曾祖父/太爷爷' },
      'father,mother,mother': { self: '曾祖母/太奶奶', 'self-f': '曾祖母/太奶奶' },
      'son,son': { self: '孙子', 'self-f': '孙子' },
      'son,daughter': { self: '孙女', 'self-f': '孙女' },
      'daughter,son': { self: '外孙', 'self-f': '外孙' },
      'daughter,daughter': { self: '外孙女', 'self-f': '外孙女' },
      'brother,son': { self: '侄子', 'self-f': '侄子' },
      'brother,daughter': { self: '侄女', 'self-f': '侄女' },
      'sister,son': { self: '外甥', 'self-f': '外甥' },
      'sister,daughter': { self: '外甥女', 'self-f': '外甥女' },
      'father,brother,son': { self: '堂兄弟', 'self-f': '堂兄弟' },
      'father,brother,daughter': { self: '堂姐妹', 'self-f': '堂姐妹' },
      'father,sister,son': { self: '表兄弟', 'self-f': '表兄弟' },
      'father,sister,daughter': { self: '表姐妹', 'self-f': '表姐妹' },
      'mother,brother,son': { self: '表兄弟', 'self-f': '表兄弟' },
      'mother,brother,daughter': { self: '表姐妹', 'self-f': '表姐妹' },
      'mother,sister,son': { self: '表兄弟', 'self-f': '表兄弟' },
      'mother,sister,daughter': { self: '表姐妹', 'self-f': '表姐妹' }
    };

    function renderChips() {
      chips.innerHTML = steps.map(function (k) {
        var label = '';
        for (var i = 0; i < REL.length; i++) if (REL[i][0] === k) label = REL[i][1];
        return '<span class="rc-chip">' + label + '</span>';
      }).join('');
    }

    addBtn.addEventListener('click', function () {
      // 简易选择器：直接用 prompt 式下拉太重，改为循环轮换常见关系（点一下加一个）
      // 用 select 方式更好：动态插入一个下拉供选择
      var sel = document.createElement('select');
      sel.className = 'rc-step-select';
      REL.forEach(function (r) { var o = document.createElement('option'); o.value = r[0]; o.textContent = r[1]; sel.appendChild(o); });
      var row = document.createElement('div');
      row.className = 'rc-step-row';
      var add = document.createElement('button');
      add.type = 'button'; add.className = 'tool-btn tool-btn-ghost'; add.textContent = '➕';
      add.addEventListener('click', function () {
        steps.push(sel.value);
        row.remove();
        renderChips();
      });
      var cancel = document.createElement('button');
      cancel.type = 'button'; cancel.className = 'tool-btn tool-btn-ghost'; cancel.textContent = '✖';
      cancel.addEventListener('click', function () { row.remove(); });
      row.appendChild(sel); row.appendChild(add); row.appendChild(cancel);
      chips.appendChild(row);
    });

    $('rc-clear').addEventListener('click', function () {
      steps = []; renderChips(); $('rc-result').innerHTML = '';
      setMsg('rc-msg', '');
    });

    $('rc-run').addEventListener('click', function () {
      var gender = $('rc-a').value;
      if (!steps.length) { setMsg('rc-msg', '⚠️ 请先添加关系链，如「爸爸」「爸爸」', true); return; }
      var key = steps.join(',');
      var found = MAP[key];
      var out = $('rc-result');
      if (found) {
        var name = found[gender] || found['self'];
        out.innerHTML = '<div class="rc-answer"><span class="rc-emoji">👨‍👩‍👧‍👦</span> 应该叫：<strong>' + name + '</strong></div>' +
          '<p class="rc-chain">' + steps.map(function (k) {
            for (var i = 0; i < REL.length; i++) if (REL[i][0] === k) return REL[i][1];
            return k;
          }).join(' → ') + '</p>';
        setMsg('rc-msg', '✅ 计算完成');
      } else {
        out.innerHTML = '<div class="rc-answer">暂时没收录这个组合 😅</div>';
        setMsg('rc-msg', '⚠️ 该关系链暂未收录，试试更短的组合', true);
      }
    });
    renderChips();
  }

  /* ================= 4. 节气查询 ================= */
  function initSolarTerm() {
    var yearSel = $('st-year');
    if (!yearSel) return;
    var TERMS = ['小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨',
      '立夏', '小满', '芒种', '夏至', '小暑', '大暑', '立秋', '处暑',
      '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至'];
    // 2025-2030 节气日期（月-日），每行一个节气，顺序同 TERMS
    var DATES = {
      2025: ['1-5', '1-20', '2-3', '2-18', '3-5', '3-20', '4-4', '4-20', '5-5', '5-21', '6-5', '6-21', '7-7', '7-22', '8-7', '8-23', '9-7', '9-23', '10-8', '10-23', '11-7', '11-22', '12-7', '12-21'],
      2026: ['1-5', '1-20', '2-4', '2-18', '3-5', '3-20', '4-5', '4-20', '5-5', '5-21', '6-5', '6-21', '7-7', '7-23', '8-7', '8-23', '9-7', '9-23', '10-8', '10-23', '11-7', '11-22', '12-7', '12-22'],
      2027: ['1-5', '1-20', '2-4', '2-19', '3-6', '3-21', '4-5', '4-20', '5-6', '5-21', '6-6', '6-21', '7-7', '7-23', '8-8', '8-23', '9-8', '9-23', '10-8', '10-24', '11-8', '11-22', '12-7', '12-22'],
      2028: ['1-6', '1-21', '2-4', '2-19', '3-5', '3-20', '4-4', '4-20', '5-5', '5-20', '6-5', '6-21', '7-6', '7-22', '8-7', '8-22', '9-7', '9-22', '10-8', '10-23', '11-7', '11-22', '12-6', '12-21'],
      2029: ['1-5', '1-20', '2-3', '2-18', '3-5', '3-20', '4-4', '4-20', '5-5', '5-21', '6-5', '6-21', '7-7', '7-22', '8-7', '8-23', '9-7', '9-23', '10-8', '10-23', '11-7', '11-22', '12-7', '12-21'],
      2030: ['1-5', '1-20', '2-4', '2-18', '3-5', '3-20', '4-5', '4-20', '5-5', '5-21', '6-5', '6-21', '7-7', '7-23', '8-7', '8-23', '9-7', '9-23', '10-8', '10-23', '11-7', '11-22', '12-7', '12-22']
    };

    for (var y = 2025; y <= 2030; y++) {
      var o = document.createElement('option');
      o.value = y; o.textContent = y + ' 年';
      yearSel.appendChild(o);
    }
    var termSel = $('st-term');
    TERMS.forEach(function (t) {
      var o = document.createElement('option');
      o.value = t; o.textContent = t;
      termSel.appendChild(o);
    });
    yearSel.value = String(new Date().getFullYear());

    function buildList(year, filter) {
      var list = $('st-list');
      var rows = DATES[year] || [];
      var html = '<div class="st-table">';
      for (var i = 0; i < TERMS.length; i++) {
        var name = TERMS[i];
        if (filter && name !== filter) continue;
        var md = rows[i] || '';
        var parts = md.split('-');
        var dateStr = parts[0] + ' 月 ' + parts[1] + ' 日';
        var season = ['立春', '雨水', '惊蛰', '春分', '清明', '谷雨'].indexOf(name) !== -1 ? '春' :
                     ['立夏', '小满', '芒种', '夏至', '小暑', '大暑'].indexOf(name) !== -1 ? '夏' :
                     ['立秋', '处暑', '白露', '秋分', '寒露', '霜降'].indexOf(name) !== -1 ? '秋' : '冬';
        html += '<div class="st-row' + (name === '立春' || name === '立夏' || name === '立秋' || name === '立冬' ? ' st-major' : '') + '">' +
          '<span class="st-season">' + season + '</span>' +
          '<span class="st-name">' + name + '</span>' +
          '<span class="st-date">' + dateStr + '</span>' +
          '</div>';
      }
      html += '</div>';
      list.innerHTML = html;
    }

    $('st-run').addEventListener('click', function () {
      buildList(parseInt(yearSel.value, 10), termSel.value || '');
      setMsg('st-msg', '✅ 已加载 ' + yearSel.value + ' 年节气');
    });

    $('st-next').addEventListener('click', function () {
      var now = new Date();
      var year = now.getFullYear();
      var rows = DATES[year];
      if (!rows) { setMsg('st-msg', '⚠️ 该年份数据暂未收录', true); return; }
      var best = null, bestName = '', bestDate = null;
      for (var i = 0; i < TERMS.length; i++) {
        var parts = rows[i].split('-');
        var d = new Date(year, parseInt(parts[0], 10) - 1, parseInt(parts[1], 10));
        if (d >= now && (!bestDate || d < bestDate)) { bestDate = d; bestName = TERMS[i]; }
      }
      if (!bestDate) {
        // 当年已过完 → 取明年立春
        var nextYear = year + 1;
        var nrows = DATES[nextYear];
        if (nrows) { var p = nrows[2].split('-'); bestDate = new Date(nextYear, parseInt(p[0], 10) - 1, parseInt(p[1], 10)); bestName = '立春'; }
      }
      if (bestDate) {
        var days = Math.round((bestDate - now) / 86400000);
        var list = $('st-list');
        list.innerHTML = '<div class="st-next-answer">下一个节气：<strong>' + bestName + '</strong>' +
          '（' + (bestDate.getMonth() + 1) + ' 月 ' + bestDate.getDate() + ' 日，还有 ' + days + ' 天）</div>';
        setMsg('st-msg', '✅ 查询完成');
      } else {
        setMsg('st-msg', '⚠️ 暂未找到，请检查年份', true);
      }
    });

    buildList(parseInt(yearSel.value, 10), '');
    setMsg('st-msg', '✅ 已加载 ' + yearSel.value + ' 年节气');
  }

  /* ============ 注册：DOMContentLoaded 逐个执行 ============ */
  var inits = [
    initImagePixelate, initIdPhoto, initRelativeCalc, initSolarTerm
  ];
  function runAll() {
    inits.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error('tools-v5 init error:', e); } });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runAll);
  } else {
    runAll();
  }
})();

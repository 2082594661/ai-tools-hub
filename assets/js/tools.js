/* tools.js — AI 小工具箱 纯前端逻辑（零依赖、零 API、本地运行）
 * 二维码生成器 / 图片智能压缩 / 艺术字生成器
 */
(function () {
  'use strict';

  /* ---------- 通用：复制到剪贴板（带降级方案） ---------- */
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
    } else {
      fallbackCopy(text); done();
    }
  }
  function fallbackCopy(text) {
    var ta = document.createElement('textarea');
    ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
  }

  /* ================= 工具3：图片智能压缩 ================= */
  function initCompressor() {
    var drop = document.getElementById('ic-drop');
    var fileInput = document.getElementById('ic-file');
    var controls = document.getElementById('ic-controls');
    var quality = document.getElementById('ic-quality');
    var qval = document.getElementById('ic-qval');
    var qval2 = document.getElementById('ic-qval2');
    var preview = document.getElementById('ic-preview');
    var stats = document.getElementById('ic-stats');
    var download = document.getElementById('ic-download');
    if (!drop) return;

    var sourceImage = null;     // 当前 Image 对象
    var originalSize = 0;
    var lastBlobUrl = null;

    function pickFile() { fileInput.click(); }
    drop.addEventListener('click', pickFile);
    drop.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pickFile(); } });
    drop.addEventListener('dragover', function (e) { e.preventDefault(); drop.style.borderColor = 'var(--clr-primary)'; });
    drop.addEventListener('dragleave', function () { drop.style.borderColor = ''; });
    drop.addEventListener('drop', function (e) {
      e.preventDefault(); drop.style.borderColor = '';
      if (e.dataTransfer.files && e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
    });
    fileInput.addEventListener('change', function () {
      if (fileInput.files && fileInput.files[0]) handleFile(fileInput.files[0]);
    });

    function handleFile(file) {
      if (!file.type.match(/^image\//)) {
        stats.textContent = '请选择图片文件（JPG / PNG / WebP）';
        return;
      }
      originalSize = file.size;
      var reader = new FileReader();
      reader.onload = function (e) {
        var img = new Image();
        img.onload = function () {
          sourceImage = img;
          controls.style.display = 'block';
          compress();
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    quality.addEventListener('input', function () {
      qval.textContent = quality.value;
      qval2.textContent = quality.value + '%';
      if (sourceImage) compress();
    });

    function compress() {
      var q = parseInt(quality.value, 10) / 100;
      var canvas = document.createElement('canvas');
      canvas.width = sourceImage.naturalWidth;
      canvas.height = sourceImage.naturalHeight;
      var ctx = canvas.getContext('2d');
      ctx.drawImage(sourceImage, 0, 0);
      // 优先 WebP（体积更小），不支持则退回 JPEG
      var useType = ('toBlob' in canvas) ? 'image/webp' : 'image/jpeg';
      if (sourceImage.src.indexOf('data:image/png') === 0 || sourceImage.src.indexOf('data:image/webp') === 0) {
        // PNG/WebP 透明图仍用 webp 保留透明
        useType = 'image/webp';
      }
      canvas.toBlob(function (blob) {
        if (!blob) { // 极端情况退回 jpeg
          canvas.toBlob(function (b2) {
            if (b2) renderResult(b2, 'image/jpeg');
          }, 'image/jpeg', q);
          return;
        }
        renderResult(blob, useType);
      }, useType, q);
    }

    function renderResult(blob, type) {
      if (lastBlobUrl) URL.revokeObjectURL(lastBlobUrl);
      lastBlobUrl = URL.createObjectURL(blob);
      var ratio = originalSize > 0 ? (1 - blob.size / originalSize) * 100 : 0;
      preview.innerHTML =
        '<figure><img src="' + sourceImage.src + '" alt="原图预览"><figcaption>原图 · ' + fmtSize(originalSize) + '</figcaption></figure>' +
        '<figure><img src="' + lastBlobUrl + '" alt="压缩后预览"><figcaption>压缩后 · ' + fmtSize(blob.size) + '</figcaption></figure>';
      stats.innerHTML = '格式 <b>' + (type.split('/')[1].toUpperCase()) + '</b> ｜ 节省 <b>' +
        (ratio > 0 ? ratio.toFixed(1) + '%' : '0%') + '</b> 体积（' + fmtSize(originalSize) + ' → ' + fmtSize(blob.size) + '）';
      download.href = lastBlobUrl;
      var ext = type.split('/')[1];
      download.setAttribute('download', 'compressed.' + ext);
    }

    function fmtSize(bytes) {
      if (bytes < 1024) return bytes + ' B';
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
      return (bytes / 1024 / 1024).toFixed(2) + ' MB';
    }
  }

  /* ================= 工具4：二维码生成器 ================= */
  function initQR() {
    var btn = document.getElementById('qr-btn');
    if (!btn) return;
    var textEl = document.getElementById('qr-text');
    var ecEl = document.getElementById('qr-ec');
    var sizeEl = document.getElementById('qr-size');
    var out = document.getElementById('qr-output');

    btn.addEventListener('click', function () {
      var text = textEl.value.trim();
      if (!text) {
        out.innerHTML = '<div class="tool-result-item"><span style="color:var(--clr-text-muted)">先填点内容再生成～</span></div>';
        return;
      }
      var res;
      try {
        res = window.QRCode.generate(text, { ecLevel: ecEl.value });
      } catch (e) {
        out.innerHTML = '<div class="tool-result-item"><span style="color:var(--clr-text-muted)">内容太长了，换短一点的文字或网址试试（最大约 200 字）。</span></div>';
        return;
      }
      var quiet = 4;
      var total = res.size + quiet * 2;
      var scale = Math.max(2, Math.round(parseInt(sizeEl.value, 10) / total));
      var canvas = document.createElement('canvas');
      canvas.width = total * scale;
      canvas.height = total * scale;
      var ctx = canvas.getContext('2d');
      ctx.fillStyle = '#fff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = '#000';
      for (var y = 0; y < res.size; y++) {
        for (var x = 0; x < res.size; x++) {
          if (res.modules[y][x]) ctx.fillRect((x + quiet) * scale, (y + quiet) * scale, scale, scale);
        }
      }
      canvas.className = 'qr-canvas';
      out.innerHTML = '<div class="qr-canvas-wrap"></div><div class="qr-actions"></div>';
      out.querySelector('.qr-canvas-wrap').appendChild(canvas);
      var dl = document.createElement('a');
      dl.className = 'tool-btn';
      dl.textContent = '⬇️ 下载 PNG';
      dl.href = canvas.toDataURL('image/png');
      dl.download = 'qrcode.png';
      out.querySelector('.qr-actions').appendChild(dl);
    });
  }

  /* ================= 工具7：艺术字生成器 ================= */
  function initArtText() {
    var btn = document.getElementById('art-btn');
    if (!btn) return;
    var input = document.getElementById('art-text-input');
    var presetsEl = document.getElementById('art-presets');
    var out = document.getElementById('art-output');
    var currentStyle = 'gradient';

    presetsEl.querySelectorAll('.art-preset').forEach(function (p) {
      p.addEventListener('click', function () {
        presetsEl.querySelectorAll('.art-preset').forEach(function (x) { x.classList.remove('active'); });
        p.classList.add('active');
        currentStyle = p.getAttribute('data-style');
      });
    });

    btn.addEventListener('click', function () {
      var text = (input.value.trim()) || 'AI趣味分享';
      var dpr = 2;
      var fontSize = 120;
      var measure = document.createElement('canvas').getContext('2d');
      measure.font = 'bold ' + fontSize + 'px sans-serif';
      var w = Math.ceil(measure.measureText(text).width) + 80;
      var h = fontSize + 80;
      var canvas = document.createElement('canvas');
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      var ctx = canvas.getContext('2d');
      ctx.scale(dpr, dpr);
      ctx.font = 'bold ' + fontSize + 'px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      var cx = w / 2, cy = h / 2;

      if (currentStyle === 'gradient') {
        var g = ctx.createLinearGradient(0, 0, w, h);
        g.addColorStop(0, '#ff6b6b');
        g.addColorStop(0.5, '#c45d3a');
        g.addColorStop(1, '#7b4bd1');
        ctx.fillStyle = g;
        ctx.fillText(text, cx, cy);
      } else if (currentStyle === 'outline') {
        ctx.lineWidth = 8;
        ctx.strokeStyle = '#c45d3a';
        ctx.strokeText(text, cx, cy);
        ctx.fillStyle = '#ffffff';
        ctx.fillText(text, cx, cy);
      } else if (currentStyle === 'shadow') {
        ctx.shadowColor = 'rgba(0,0,0,0.35)';
        ctx.shadowBlur = 12;
        ctx.shadowOffsetY = 6;
        ctx.fillStyle = '#333333';
        ctx.fillText(text, cx, cy);
      } else if (currentStyle === 'neon') {
        ctx.shadowColor = '#00eaff';
        ctx.shadowBlur = 22;
        ctx.fillStyle = '#ffffff';
        ctx.fillText(text, cx, cy);
        ctx.shadowBlur = 8;
        ctx.fillText(text, cx, cy);
      }

      canvas.className = 'art-canvas';
      out.innerHTML = '<div class="art-canvas-wrap"></div>';
      out.querySelector('.art-canvas-wrap').appendChild(canvas);
      var dl = document.createElement('a');
      dl.className = 'tool-btn';
      dl.textContent = '⬇️ 下载 PNG';
      dl.href = canvas.toDataURL('image/png');
      dl.download = 'art-text.png';
      dl.style.marginTop = '1rem';
      dl.style.display = 'inline-block';
      out.appendChild(dl);
    });
  }


  /* ---------- 初始化 ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    initCompressor();
    initQR();
    initArtText();
  });
})();

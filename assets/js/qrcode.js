/* qrcode.js — 纯前端、零依赖的二维码生成器（字节模式，支持版本 1-10，EC 等级 L/M/Q/H）
 * 实现遵循 ISO/IEC 18004 标准：GF(256) 里德-所罗门纠错、数据编码、模块排布、掩码、格式/版本信息。
 * 已与 Python qrcode 库逐位比对验证正确性（版本 1-10、EC 等级 L/M/Q/H、自动选掩码、中英文与 emoji 均通过）。
 * 对外暴露：window.QRCode.generate(text, {ecLevel, version, mask}) -> { size, modules: boolean[][] }
 */
(function (global) {
  'use strict';

  /* ---------- GF(256) 对数/指数表（本原多项式 0x11D） ---------- */
  var EXP = new Array(512), LOG = new Array(256);
  (function () {
    var x = 1;
    for (var i = 0; i < 255; i++) {
      EXP[i] = x;
      LOG[x] = i;
      x <<= 1;
      if (x & 0x100) x ^= 0x11d;
    }
    for (var i = 255; i < 512; i++) EXP[i] = EXP[i - 255];
  })();
  function gfMul(a, b) {
    if (a === 0 || b === 0) return 0;
    return EXP[LOG[a] + LOG[b]];
  }

  /* ---------- 里德-所罗门生成多项式 ---------- */
  function rsGenPoly(degree) {
    var g = [1];
    for (var i = 0; i < degree; i++) {
      var ng = new Array(g.length + 1);
      for (var k = 0; k < ng.length; k++) ng[k] = 0;
      for (var j = 0; j < g.length; j++) {
        ng[j] ^= gfMul(g[j], EXP[i]);
        ng[j + 1] ^= g[j];
      }
      g = ng;
    }
    return g;
  }
  function rsEncode(data, ecLen) {
    // Standard RS encoder: multiply data by x^ecLen, divide by generator poly.
    // rsGenPoly returns coefficients in ascending order (const..leading);
    // the LFSR/long-division loop expects descending order (leading..const), so reverse.
    var gen = rsGenPoly(ecLen); // ascending: gen[0] = const, gen[ecLen] = 1 (monic)
    gen.reverse();              // descending: gen[0] = 1 (leading)
    var msg = data.slice();
    for (var i = 0; i < ecLen; i++) msg.push(0);
    for (var i = 0; i < data.length; i++) {
      var coef = msg[i];
      if (coef !== 0) {
        for (var j = 1; j < gen.length; j++) {
          msg[i + j] ^= gfMul(gen[j], coef);
        }
      }
    }
    return msg.slice(data.length); // last ecLen bytes = error-correction codewords
  }

  /* ---------- 纠错块结构表 (version -> EC等级 -> 分组[count,total,data,...]) ---------- */
  var RS_TABLE = {
    1:  { L:[1,26,19], M:[1,26,16], Q:[1,26,13], H:[1,26,9] },
    2:  { L:[1,44,34], M:[1,44,28], Q:[1,44,22], H:[1,44,16] },
    3:  { L:[1,70,55], M:[1,70,44], Q:[2,35,17], H:[2,35,13] },
    4:  { L:[1,100,80], M:[2,50,32], Q:[2,50,24], H:[4,25,9] },
    5:  { L:[1,134,108], M:[2,67,43], Q:[2,33,15,2,34,16], H:[2,33,11,2,34,12] },
    6:  { L:[2,86,68], M:[4,43,27], Q:[4,43,19], H:[4,43,15] },
    7:  { L:[2,98,78], M:[4,49,31], Q:[2,32,14,4,33,15], H:[4,39,13,1,40,14] },
    8:  { L:[2,121,97], M:[2,60,38,2,61,39], Q:[4,40,18,2,41,19], H:[4,40,14,2,41,15] },
    9:  { L:[2,146,116], M:[3,58,36,2,59,37], Q:[4,36,16,4,37,17], H:[4,36,12,4,37,13] },
    10: { L:[2,86,68,2,87,69], M:[4,69,43,1,70,44], Q:[6,43,19,2,44,20], H:[6,43,15,2,44,16] }
  };
  var PATTERN_POS = {
    1:[], 2:[6,18], 3:[6,22], 4:[6,26], 5:[6,30], 6:[6,34],
    7:[6,22,38], 8:[6,24,42], 9:[6,26,46], 10:[6,28,50]
  };
  var MAX_VERSION = 10;
  var EC_BITS = { L: 0b01, M: 0b00, Q: 0b11, H: 0b10 };

  /* ---------- BCH：格式信息(15,5) 与版本信息(18,6) ---------- */
  var G15 = 0x537, G15_MASK = 0x5412, G18 = 0x1f25;
  function bchFormat(data5) {
    var d = data5 << 10;
    while (bitWidth(d) - bitWidth(G15) >= 0) d ^= G15 << (bitWidth(d) - bitWidth(G15));
    return ((data5 << 10) | d) ^ G15_MASK;
  }
  function bchVersion(data6) {
    var d = data6 << 12;
    while (bitWidth(d) - bitWidth(G18) >= 0) d ^= G18 << (bitWidth(d) - bitWidth(G18));
    return (data6 << 12) | d;
  }
  function bitWidth(x) { var w = 0; while (x) { w++; x >>>= 1; } return w; }

  /* ---------- 版本自动选择 ---------- */
  function countBitsForVersion(v) { return v <= 9 ? 8 : 16; }
  function totalDataCodewords(v, ecLevel) {
    var groups = RS_TABLE[v][ecLevel];
    var total = 0;
    for (var i = 0; i < groups.length; i += 3) total += groups[i] * groups[i + 2];
    return total;
  }
  function chooseVersion(text, ecLevel) {
    var bytes = utf8Bytes(text);
    for (var v = 1; v <= MAX_VERSION; v++) {
      var cap = totalDataCodewords(v, ecLevel) * 8;
      var needed = 4 + countBitsForVersion(v) + bytes.length * 8;
      if (needed <= cap) return v;
    }
    throw new Error('内容过长，超出二维码容量（最大版本 ' + MAX_VERSION + '）');
  }

  /* ---------- UTF-8 编码 ---------- */
  function utf8Bytes(str) {
    var out = [];
    for (var i = 0; i < str.length; i++) {
      var c = str.charCodeAt(i);
      if (c < 0x80) out.push(c);
      else if (c < 0x800) { out.push(0xc0 | (c >> 6), 0x80 | (c & 0x3f)); }
      else if (c >= 0xd800 && c <= 0xdbff) {
        var c2 = str.charCodeAt(++i);
        var cp = 0x10000 + ((c & 0x3ff) << 10) + (c2 & 0x3ff);
        out.push(0xf0 | (cp >> 18), 0x80 | ((cp >> 12) & 0x3f), 0x80 | ((cp >> 6) & 0x3f), 0x80 | (cp & 0x3f));
      } else { out.push(0xe0 | (c >> 12), 0x80 | ((c >> 6) & 0x3f), 0x80 | (c & 0x3f)); }
    }
    return out;
  }

  /* ---------- 编码数据码字（字节模式） ---------- */
  function encodeData(text, v, ecLevel) {
    var bytes = utf8Bytes(text);
    var dataCap = totalDataCodewords(v, ecLevel);
    var bits = [];
    function pushBits(val, n) { for (var i = n - 1; i >= 0; i--) bits.push((val >> i) & 1); }
    pushBits(0b0100, 4);                       // 字节模式指示符
    pushBits(bytes.length, countBitsForVersion(v)); // 字符计数
    for (var i = 0; i < bytes.length; i++) pushBits(bytes[i], 8);
    // 终止符（最多 4 个 0）
    var cap = dataCap * 8;
    var term = Math.min(4, cap - bits.length);
    for (var i = 0; i < term; i++) bits.push(0);
    while (bits.length % 8 !== 0) bits.push(0); // 补齐到字节
    var codewords = [];
    for (var i = 0; i < bits.length; i += 8) {
      var b = 0; for (var j = 0; j < 8; j++) b = (b << 1) | bits[i + j];
      codewords.push(b);
    }
    // 填充字节
    var pad = [0xec, 0x11]; var p = 0;
    while (codewords.length < dataCap) { codewords.push(pad[p % 2]); p++; }
    return codewords;
  }

  /* ---------- 构建最终码字序列（分块 + 交织 + 纠错） ---------- */
  function buildCodewords(data, v, ecLevel) {
    var groups = RS_TABLE[v][ecLevel];
    var blocks = [];
    var idx = 0;
    for (var g = 0; g < groups.length; g += 3) {
      var count = groups[g], total = groups[g + 1], dcount = groups[g + 2];
      var ecLen = total - dcount;
      for (var b = 0; b < count; b++) {
        var d = data.slice(idx, idx + dcount);
        var ec = rsEncode(d, ecLen);
        blocks.push({ data: d, ec: ec });
        idx += dcount;
      }
    }
    // 交织数据
    var result = [];
    var maxData = 0; for (var i = 0; i < blocks.length; i++) maxData = Math.max(maxData, blocks[i].data.length);
    for (var col = 0; col < maxData; col++)
      for (var i = 0; i < blocks.length; i++)
        if (col < blocks[i].data.length) result.push(blocks[i].data[col]);
    var maxEc = 0; for (var i = 0; i < blocks.length; i++) maxEc = Math.max(maxEc, blocks[i].ec.length);
    for (var col = 0; col < maxEc; col++)
      for (var i = 0; i < blocks.length; i++)
        if (col < blocks[i].ec.length) result.push(blocks[i].ec[col]);
    return result;
  }

  /* ---------- 模块矩阵构建 ---------- */
  function buildMatrix(v, ecLevel, maskId, finalCodewords) {
    var size = 17 + 4 * v;
    var mod = []; for (var y = 0; y < size; y++) { mod[y] = []; for (var x = 0; x < size; x++) mod[y][x] = null; }
    var reserved = []; for (var y = 0; y < size; y++) { reserved[y] = []; for (var x = 0; x < size; x++) reserved[y][x] = false; }

    function setF(x, y, val) { mod[y][x] = val; reserved[y][x] = true; }

    // 定位图案 + 分隔符（每个角一个 8x8 块，含 1 模块宽白边）
    function placeFinderBlock(ox, oy) {
      for (var y = -1; y <= 7; y++) for (var x = -1; x <= 7; x++) {
        var xx = ox + x, yy = oy + y;
        if (xx < 0 || yy < 0 || xx >= size || yy >= size) continue;
        var onFinder = (x >= 0 && x <= 6 && y >= 0 && y <= 6);
        var inRing = onFinder && (x === 0 || x === 6 || y === 0 || y === 6);
        var isCenter = onFinder && (x >= 2 && x <= 4 && y >= 2 && y <= 4);
        setF(xx, yy, inRing || isCenter); // 分隔符区域值为 false（白），同样保留
      }
    }
    placeFinderBlock(0, 0); placeFinderBlock(size - 7, 0); placeFinderBlock(0, size - 7);

    // 定时图案
    for (var i = 8; i < size - 8; i++) {
      var t = (i % 2 === 0);
      if (!reserved[6][i]) { mod[6][i] = t; reserved[6][i] = true; }
      if (!reserved[i][6]) { mod[i][6] = t; reserved[i][6] = true; }
    }
    // 校正图案（中心）
    var pos = PATTERN_POS[v];
    for (var a = 0; a < pos.length; a++) for (var b = 0; b < pos.length; b++) {
      var cx = pos[a], cy = pos[b];
      if (cx === 6 && cy === 6) continue;
      if (cx === 6 && cy === size - 7) continue;
      if (cx === size - 7 && cy === 6) continue;
      for (var dy = -2; dy <= 2; dy++) for (var dx = -2; dx <= 2; dx++) {
        var isCenter = (dx === 0 && dy === 0);
        var isRing = (Math.max(Math.abs(dx), Math.abs(dy)) === 2);
        setF(cx + dx, cy + dy, isCenter || isRing);
      }
    }
    // 暗模块
    setF(8, size - 8, true);
    // 预留格式信息
    for (var i = 0; i <= 8; i++) { if (i !== 6) reserved[8][i] = reserved[i][8] = true; }
    for (var i = 0; i <= 8; i++) { reserved[size - 1 - i][8] = reserved[8][size - 1 - i] = true; }
    // 预留版本信息（v>=7）
    if (v >= 7) {
      for (var i = 0; i < 6; i++) for (var j = 0; j < 3; j++) {
        reserved[size - 11 + j][i] = reserved[i][size - 11 + j] = true;
      }
    }

    // 格式信息（必须在 map_data 之前设置，使其被跳过）—— 逐行移植 Python setup_type_info
    var fmt = bchFormat((EC_BITS[ecLevel] << 3) | maskId);
    for (var i = 0; i <= 14; i++) {
      var fbit = ((fmt >> i) & 1) === 1;
      if (i < 6) mod[i][8] = fbit;
      else if (i < 8) mod[i + 1][8] = fbit;
      else mod[size - 15 + i][8] = fbit;
      if (i < 8) mod[8][size - 1 - i] = fbit;
      else if (i < 9) mod[8][15 - i] = fbit;
      else mod[8][14 - i] = fbit;
    }
    mod[size - 8][8] = true; // 固定暗模块

    // 版本信息（v>=7）—— 逐行移植 Python setup_type_number
    if (v >= 7) {
      var vbits = bchVersion(v);
      for (var i = 0; i < 18; i++) {
        var vbit = ((vbits >> i) & 1) === 1;
        mod[Math.floor(i / 3)][i % 3 + size - 8 - 3] = vbit;
      }
      for (var i = 0; i < 18; i++) {
        var vbit = ((vbits >> i) & 1) === 1;
        mod[i % 3 + size - 8 - 3][Math.floor(i / 3)] = vbit;
      }
    }

    // 数据放置（之字形 + 掩码，逐行移植 Python map_data）
    var maskFunc;
    switch (maskId) {
      case 0: maskFunc = function (i, j) { return (i + j) % 2 === 0; }; break;
      case 1: maskFunc = function (i, j) { return i % 2 === 0; }; break;
      case 2: maskFunc = function (i, j) { return j % 3 === 0; }; break;
      case 3: maskFunc = function (i, j) { return (i + j) % 3 === 0; }; break;
      case 4: maskFunc = function (i, j) { return (Math.floor(i / 2) + Math.floor(j / 3)) % 2 === 0; }; break;
      case 5: maskFunc = function (i, j) { return (i * j) % 2 + (i * j) % 3 === 0; }; break;
      case 6: maskFunc = function (i, j) { return ((i * j) % 2 + (i * j) % 3) % 2 === 0; }; break;
      case 7: maskFunc = function (i, j) { return ((i * j) % 3 + (i + j) % 2) % 2 === 0; }; break;
    }
    var inc = -1, row = size - 1, bitIndex = 7, byteIndex = 0;
    var dataLen = finalCodewords.length;
    for (var col = size - 1; col > 0; col -= 2) {
      var cc = col;
      if (cc <= 6) cc -= 1;
      var colRange = [cc, cc - 1];
      while (true) {
        for (var ci = 0; ci < 2; ci++) {
          var c = colRange[ci];
          if (mod[row][c] === null) {
            var dark = false;
            if (byteIndex < dataLen) dark = ((finalCodewords[byteIndex] >> bitIndex) & 1) === 1;
            if (maskFunc(row, c)) dark = !dark;
            mod[row][c] = dark;
            bitIndex -= 1;
            if (bitIndex === -1) { byteIndex += 1; bitIndex = 7; }
          }
        }
        row += inc;
        if (row < 0 || row >= size) { row -= inc; inc = -inc; break; }
      }
    }
    return mod;
  }

  /* ---------- 掩码惩罚评分（自动选最优） ---------- */
  function lostPoint(mod, size) {
    var score = 0;
    // 规则1：行/列连续同色 >=5
    for (var y = 0; y < size; y++) {
      var run = 1;
      for (var x = 1; x < size; x++) {
        if (mod[y][x] === mod[y][x - 1]) { run++; if (run === 5) score += 3; else if (run > 5) score++; }
        else run = 1;
      }
    }
    for (var x = 0; x < size; x++) {
      var run = 1;
      for (var y = 1; y < size; y++) {
        if (mod[y][x] === mod[y - 1][x]) { run++; if (run === 5) score += 3; else if (run > 5) score++; }
        else run = 1;
      }
    }
    // 规则2：2x2 同色块
    for (var y = 0; y < size - 1; y++) for (var x = 0; x < size - 1; x++) {
      var c = mod[y][x];
      if (c === mod[y][x + 1] && c === mod[y + 1][x] && c === mod[y + 1][x + 1]) score += 3;
    }
    // 规则3：类似定位图案的行/列
    function patternPenalty(arr) {
      var s = 0, pat = [true,false,true,true,true,false,true,false,false,false,false];
      for (var i = 0; i + 10 < arr.length; i++) {
        var match = true;
        for (var j = 0; j < 11; j++) if (arr[i + j] !== pat[j]) { match = false; break; }
        if (match) s += 40;
      }
      var pat2 = [false,false,false,false,true,false,true,true,true,false,true];
      for (var i = 0; i + 10 < arr.length; i++) {
        var match = true;
        for (var j = 0; j < 11; j++) if (arr[i + j] !== pat2[j]) { match = false; break; }
        if (match) s += 40;
      }
      return s;
    }
    for (var y = 0; y < size; y++) { var row = []; for (var x = 0; x < size; x++) row.push(mod[y][x]); score += patternPenalty(row); }
    for (var x = 0; x < size; x++) { var col = []; for (var y = 0; y < size; y++) col.push(mod[y][x]); score += patternPenalty(col); }
    // 规则4：黑模块比例偏离 50%
    var dark = 0;
    for (var y = 0; y < size; y++) for (var x = 0; x < size; x++) if (mod[y][x]) dark++;
    var ratio = Math.abs(dark * 100 / (size * size) - 50) / 5;
    score += Math.floor(ratio) * 10;
    return score;
  }

  /* ---------- 对外主函数 ---------- */
  function generate(text, opts) {
    opts = opts || {};
    var ecLevel = opts.ecLevel || 'M';
    if (!RS_TABLE[1][ecLevel]) ecLevel = 'M';
    var version = opts.version;
    if (!version) version = chooseVersion(text, ecLevel);
    if (version > MAX_VERSION) throw new Error('超出支持的最大版本');

    var data = encodeData(text, version, ecLevel);
    var final = buildCodewords(data, version, ecLevel);

    var chosenMask = opts.mask;
    if (chosenMask === null || chosenMask === undefined) {
      var best = 0, bestScore = Infinity;
      for (var m = 0; m < 8; m++) {
        var mm = buildMatrix(version, ecLevel, m, final);
        var sc = lostPoint(mm, 17 + 4 * version);
        if (sc < bestScore) { bestScore = sc; best = m; }
      }
      chosenMask = best;
    }
    var mod = buildMatrix(version, ecLevel, chosenMask, final);
    // 转为 boolean（true=黑）
    var size = mod.length;
    var modules = [];
    for (var y = 0; y < size; y++) {
      var row = [];
      for (var x = 0; x < size; x++) row.push(mod[y][x] === true);
      modules.push(row);
    }
    return { size: size, modules: modules, version: version, mask: chosenMask, ecLevel: ecLevel };
  }

  global.QRCode = { generate: generate };
})(typeof window !== 'undefined' ? window : this);

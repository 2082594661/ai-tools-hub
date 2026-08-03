# -*- coding: utf-8 -*-
"""验证 zh-map.js 转换正确性"""
import io, re, json

src = io.open(r"C:\Users\龙潜\Desktop\AI趣味分享\assets\js\zh-map.js", encoding="utf-8").read()
# 提取 JS 对象并转换为合法 JSON（给顶层键加引号）
marker = "window.ZH_MAP = "
start = src.index(marker) + len(marker)
end = src.rindex("}")
js_obj = src[start:end+1]
for key in ["s2tChar", "s2tWord", "t2sChar", "t2sWord"]:
    js_obj = js_obj.replace(key + ":", '"' + key + '":')
data = json.loads(js_obj)

def conv(text, words, chars):
    keys = sorted(words.keys(), key=len, reverse=True)
    out = text
    for k in keys:
        out = out.replace(k, words[k])
    return "".join(chars.get(c, c) for c in out)

s2t = conv("头发 发财 发展 后面 面条 干净 干活 一只 系统 台湾 计划 制作 斗争 准备 复习 复杂 软件 网络 服务器 浏览器 什么 手机 电脑 微信", data["s2tWord"], data["s2tChar"])
t2s = conv("頭髮 發財 發展 後面 麵條 乾淨 幹活 一隻 系統 臺灣 計劃 製作 鬥爭 準備 複習 複雜 軟件 網絡 服務器 瀏覽器 什麼 手機 電腦 微信", data["t2sWord"], data["t2sChar"])
print("简→繁:", s2t)
print("繁→简:", t2s)
# 断言关键词组
assert "頭髮" in s2t and "發財" in s2t and "後面" in s2t and "麵條" in s2t
assert "乾淨" in s2t and "幹活" in s2t and "臺灣" in s2t and "瀏覽器" in s2t
assert "头发" in t2s and "发财" in t2s and "后面" in t2s and "面条" in t2s
assert "干净" in t2s and "干活" in t2s and "台湾" in t2s and "浏览器" in t2s
print("✅ 简繁映射验证通过")

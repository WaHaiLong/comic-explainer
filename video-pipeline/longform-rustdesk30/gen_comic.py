#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 content_a/b 的 12 章 63 格数据渲染成 comic30.html（comic-explainer 风格单文件）"""
import sys, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from content_a import CHAPTERS_A
from content_b import CHAPTERS_B
from extend import apply_extend
from extend2 import apply_extend2

CHAPTERS = apply_extend2(apply_extend(CHAPTERS_A + CHAPTERS_B))
INK, PAPER, ACCENT, BLUE, YELLOW = "#2b2622", "#f7f1e3", "#e8542f", "#2f6fe8", "#ffd94a"
BGS = ["#f2ead6", "#efe7d2", "#f6efdd", "#ece2c8"]

CSS = """
:root{--ink:#2b2622;--paper:#f7f1e3;--panel:#fffdf6;--accent:#e8542f;--blue:#2f6fe8;--yellow:#ffd94a;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:radial-gradient(circle at 20% 10%,#efe6d0 0 40%,transparent 60%),
 radial-gradient(circle at 80% 90%,#ece2c8 0 40%,transparent 60%),var(--paper);
 font-family:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",-apple-system,sans-serif;
 color:var(--ink);line-height:1.6;}
.comic{max-width:860px;margin:0 auto;padding:28px 16px 80px;}
header.cover{text-align:center;padding:46px 18px 34px;border:4px solid var(--ink);
 background:var(--yellow);border-radius:14px;box-shadow:8px 8px 0 rgba(43,38,34,.85);
 margin-bottom:34px;position:relative;overflow:hidden;}
header.cover h1{font-size:clamp(28px,5.5vw,44px);letter-spacing:2px;}
header.cover h1 .num{color:var(--accent);font-family:ui-monospace,Menlo,monospace;}
header.cover p.sub{margin-top:10px;font-size:15px;opacity:.8;}
header.cover .stripe{position:absolute;top:-30px;right:-60px;width:220px;height:90px;opacity:.18;
 background:repeating-linear-gradient(45deg,var(--ink) 0 12px,transparent 12px 24px);transform:rotate(-24deg);}
.panel{position:relative;border:3.5px solid var(--ink);border-radius:12px;background:var(--panel);
 margin:30px 0 0;overflow:hidden;box-shadow:6px 6px 0 rgba(43,38,34,.75);}
.ptag{position:absolute;top:0;left:0;z-index:5;background:var(--ink);color:#fff;font-size:13px;
 font-weight:700;padding:5px 14px 6px;border-radius:9px 0 12px 0;letter-spacing:1px;}
.ptitle{position:absolute;z-index:5;top:34px;left:14px;font-size:clamp(18px,3.4vw,26px);font-weight:900;
 letter-spacing:1px;text-shadow:2px 2px 0 #fff,-2px -2px 0 #fff,2px -2px 0 #fff,-2px 2px 0 #fff;}
.scene{display:block;width:100%;height:auto;}
.bub{position:absolute;z-index:6;max-width:44%;background:#fff;border:2.6px solid var(--ink);
 border-radius:16px;padding:9px 13px;font-size:clamp(12px,1.9vw,15.5px);font-weight:600;
 box-shadow:3px 3px 0 rgba(43,38,34,.25);}
.bub::after{content:"";position:absolute;bottom:-14px;left:26px;border:8px solid transparent;border-top:14px solid var(--ink);}
.bub.tail-r::after{left:auto;right:26px;}
.bub .hl{color:var(--accent);} .bub .bl{color:var(--blue);}
.narr{position:absolute;z-index:6;left:14px;right:14px;bottom:12px;background:var(--ink);color:#fdf7e8;
 font-size:clamp(12px,2vw,15px);padding:8px 14px;border-radius:6px;font-weight:600;}
.narr b{color:var(--yellow);}
.factbox{margin:34px 4px 0;border:3px dashed var(--ink);border-radius:12px;background:#eaf2ff;padding:16px 18px;}
.factbox h3{font-size:16px;margin-bottom:6px;color:var(--blue);} .factbox li{margin-left:1.2em;font-size:14px;}
footer{text-align:center;margin-top:48px;font-size:13px;opacity:.65;}
/* HTML 卡片类面板 */
.cardwrap{height:430px;display:flex;flex-direction:column;justify-content:center;padding:64px 40px 66px;gap:10px;}
.ct{font-size:22px;font-weight:900;letter-spacing:1px;border-bottom:3px solid var(--ink);
 padding-bottom:8px;margin-bottom:6px;display:flex;align-items:center;gap:10px;}
.ct .dot{width:16px;height:16px;border-radius:50%;background:var(--accent);border:3px solid var(--ink);flex:0 0 auto;}
table.cmp{width:100%;border-collapse:collapse;font-size:15.5px;background:#fff;border:3px solid var(--ink);border-radius:10px;overflow:hidden;}
table.cmp th{background:var(--yellow);border:2.5px solid var(--ink);padding:8px 12px;font-size:15.5px;}
table.cmp td{border:2px solid var(--ink);padding:8px 12px;font-weight:600;}
table.cmp tr:nth-child(even) td{background:#faf5e6;}
ul.biglist{list-style:none;display:flex;flex-direction:column;gap:9px;}
ul.biglist li{display:flex;align-items:center;gap:12px;font-size:16.5px;font-weight:700;background:#fff;
 border:2.5px solid var(--ink);border-radius:10px;padding:8px 14px;box-shadow:3px 3px 0 rgba(43,38,34,.2);}
ul.biglist li .n{flex:0 0 auto;width:26px;height:26px;border-radius:50%;background:var(--blue);color:#fff;
 display:flex;align-items:center;justify-content:center;font-size:14px;border:2.5px solid var(--ink);}
.terminal{background:#20242b;color:#d5e2d0;border:3.5px solid var(--ink);border-radius:12px;
 padding:16px 20px;font-family:ui-monospace,Menlo,monospace;font-size:14.5px;line-height:1.9;box-shadow:4px 4px 0 rgba(43,38,34,.4);}
.terminal .c{color:#7f8c98;}
.flowrow{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:nowrap;}
.flowbox{background:#fff;border:3px solid var(--ink);border-radius:10px;padding:12px 10px;font-size:14.5px;
 font-weight:800;text-align:center;box-shadow:4px 4px 0 rgba(43,38,34,.3);flex:1;}
.flowarrow{color:var(--accent);font-size:22px;font-weight:900;flex:0 0 auto;}
.tl{display:flex;gap:8px;}
.tlitem{flex:1;text-align:center;position:relative;padding-top:26px;}
.tlitem::before{content:"";position:absolute;top:8px;left:50%;transform:translateX(-50%);width:16px;height:16px;
 border-radius:50%;background:var(--accent);border:3px solid var(--ink);}
.tl::before{content:"";position:absolute;top:15px;left:6%;right:6%;height:4px;background:var(--ink);border-radius:2px;}
.tlwrap{position:relative;}
.tlyear{font-weight:900;font-size:15px;color:var(--accent);}
.tltext{font-size:12.8px;font-weight:700;line-height:1.45;margin-top:2px;}
.bigcard{text-align:center;}
.bigcard .huge{font-size:72px;font-weight:900;color:var(--accent);letter-spacing:2px;
 text-shadow:3px 3px 0 var(--yellow);}
.bigcard .lab{font-size:22px;font-weight:900;margin-top:6px;}
.bigcard .sub2{font-size:14.5px;opacity:.75;margin-top:8px;}
"""

def mascot_svg(pose, prop, bg):
    # 表情部件
    if pose == "happy":
        eyes = '<path d="M46 52 Q54 45 62 52" stroke="#2b2622" stroke-width="4" fill="none"/><path d="M74 52 Q82 45 90 52" stroke="#2b2622" stroke-width="4" fill="none"/>'
        mouth = '<path d="M52 68 Q68 78 84 68" stroke="#2b2622" stroke-width="4" fill="none"/>'
    elif pose == "think":
        eyes = '<circle cx="54" cy="48" r="5.5" fill="#2b2622"/><circle cx="82" cy="48" r="5.5" fill="#2b2622"/><circle cx="56" cy="46" r="1.8" fill="#fff"/><circle cx="84" cy="46" r="1.8" fill="#fff"/>'
        mouth = '<path d="M58 70 Q68 66 78 70" stroke="#2b2622" stroke-width="4" fill="none"/>'
    elif pose == "warn":
        eyes = '<circle cx="54" cy="50" r="6" fill="#2b2622"/><circle cx="82" cy="50" r="6" fill="#2b2622"/><line x1="44" y1="38" x2="62" y2="44" stroke="#e8542f" stroke-width="4" stroke-linecap="round"/><line x1="92" y1="38" x2="74" y2="44" stroke="#e8542f" stroke-width="4" stroke-linecap="round"/>'
        mouth = '<ellipse cx="68" cy="70" rx="9" ry="11" fill="#2b2622"/>'
    elif pose == "money":
        eyes = '<text x="47" y="56" font-size="17" font-weight="900" fill="#2b7a34">$</text><text x="76" y="56" font-size="17" font-weight="900" fill="#2b7a34">$</text>'
        mouth = '<path d="M54 68 Q68 80 82 68" stroke="#2b2622" stroke-width="4" fill="none"/>'
    else:  # ok
        eyes = '<circle cx="54" cy="50" r="5.5" fill="#2b2622"/><circle cx="82" cy="50" r="5.5" fill="#2b2622"/>'
        mouth = '<path d="M54 68 Q68 77 82 68" stroke="#2b2622" stroke-width="4" fill="none"/>'
    # 道具（右侧小图）
    props = {
        "laptop": '<g transform="translate(560,120)"><rect width="150" height="96" rx="12" fill="#cdeccf" stroke="#2b2622" stroke-width="3.5"/><circle cx="56" cy="42" r="6" fill="#2b2622"/><circle cx="96" cy="42" r="6" fill="#2b2622"/><path d="M62 64 Q76 74 90 64" stroke="#2b2622" stroke-width="3.5" fill="none"/><rect x="44" y="96" width="62" height="12" fill="#2b2622"/><rect x="20" y="108" width="110" height="12" rx="5" fill="#2b2622"/></g>',
        "server": '<g transform="translate(575,110)"><rect width="110" height="150" rx="10" fill="#cfd8dc" stroke="#2b2622" stroke-width="3.5"/><circle cx="24" cy="34" r="6" fill="#43a047"/><circle cx="24" cy="70" r="6" fill="#e53935"/><circle cx="24" cy="106" r="6" fill="#43a047"/><line x1="44" y1="34" x2="92" y2="34" stroke="#2b2622" stroke-width="3"/><line x1="44" y1="70" x2="92" y2="70" stroke="#2b2622" stroke-width="3"/><line x1="44" y1="106" x2="92" y2="106" stroke="#2b2622" stroke-width="3"/></g>',
        "net": '<g transform="translate(560,110)"><circle cx="100" cy="70" r="62" fill="#dbe9ff" stroke="#2b2622" stroke-width="3.5"/><ellipse cx="100" cy="70" rx="28" ry="62" fill="none" stroke="#2f6fe8" stroke-width="3"/><line x1="38" y1="70" x2="162" y2="70" stroke="#2f6fe8" stroke-width="3"/><path d="M50 38 Q100 58 150 38" fill="none" stroke="#2f6fe8" stroke-width="3"/><path d="M50 102 Q100 82 150 102" fill="none" stroke="#2f6fe8" stroke-width="3"/></g>',
        "coin": '<g transform="translate(575,105)"><circle cx="65" cy="75" r="62" fill="#ffd94a" stroke="#2b2622" stroke-width="4"/><text x="65" y="100" text-anchor="middle" font-size="64" font-weight="900" fill="#c23a15">¥</text></g>',
        "shield": '<g transform="translate(570,95)"><path d="M70 0 L140 26 V86 Q140 138 70 160 V0 Z" fill="#e1f0ff" stroke="#2b2622" stroke-width="4"/><path d="M46 84 L64 102 L98 60" stroke="#43a047" stroke-width="9" fill="none" stroke-linecap="round"/></g>',
    }
    prop_svg = props.get(prop, "")
    dashed = '<line x1="330" y1="180" x2="545" y2="175" stroke="#2f6fe8" stroke-width="4" stroke-dasharray="10 8"/>' if prop == "net" else ""
    return f'''<svg class="scene" viewBox="0 0 860 430" xmlns="http://www.w3.org/2000/svg">
      <rect width="860" height="430" fill="{bg}"/>
      {prop_svg}{dashed}
      <g transform="translate(300,110)">
        <rect x="0" y="40" width="136" height="66" rx="13" fill="#ffe082" stroke="#2b2622" stroke-width="3.5"/>
        <line x1="26" y1="40" x2="17" y2="6" stroke="#2b2622" stroke-width="4" stroke-linecap="round"/>
        <line x1="110" y1="40" x2="119" y2="6" stroke="#2b2622" stroke-width="4" stroke-linecap="round"/>
        <circle cx="17" cy="2" r="4.5" fill="#e8542f"/><circle cx="119" cy="2" r="4.5" fill="#e8542f"/>
        {eyes}{mouth}
        <line x1="0" y1="58" x2="-20" y2="70" stroke="#2b2622" stroke-width="4" stroke-linecap="round"/>
        <line x1="136" y1="58" x2="156" y2="70" stroke="#2b2622" stroke-width="4" stroke-linecap="round"/>
        <rect x="28" y="110" width="80" height="20" rx="4" fill="#fff" stroke="#2b2622" stroke-width="2"/>
        <text x="68" y="125" text-anchor="middle" font-size="13" font-weight="900" fill="#2b2622">RustDesk</text>
      </g>
    </svg>'''

def chapter_svg(num, title, sub, bg):
    return f'''<svg class="scene" viewBox="0 0 860 430" xmlns="http://www.w3.org/2000/svg">
      <rect width="860" height="430" fill="{YELLOW}"/>
      <rect x="60" y="60" width="740" height="310" rx="18" fill="#fffdf6" stroke="#2b2622" stroke-width="4"/>
      <rect x="60" y="60" width="740" height="310" rx="18" fill="none" stroke="#2b2622" stroke-width="4"/>
      <text x="430" y="150" text-anchor="middle" font-size="64" font-weight="900" fill="{ACCENT}" font-family="ui-monospace,Menlo,monospace">第 {num} 章</text>
      <text x="430" y="235" text-anchor="middle" font-size="42" font-weight="900" fill="#2b2622">{title}</text>
      <text x="430" y="300" text-anchor="middle" font-size="20" font-weight="700" fill="#2b2622" opacity=".75">{sub}</text>
    </svg>'''

def panel_html(idx, ch, p):
    bg = BGS[idx % len(BGS)]
    t = p["type"]
    inner_parts = []
    if t == "chapter_card":
        scene = chapter_svg(ch["num"], ch["title"], ch["sub"], bg)
        title = f"第 {ch['num']} 章"
    elif t == "mascot":
        scene = mascot_svg(p["pose"], p["prop"], bg)
        title = p["label"]
        tail = "tail-r" if p.get("tail") == "r" else ""
        bstyle = "top:96px; left:56px;" if p.get("tail") == "r" else "top:96px; right:400px; left:auto;"
        inner_parts.append(f'<div class="bub {tail}" style="{bstyle}">{html.escape(p["bubble"])}</div>')
    else:
        title = p.get("title", "")
        if t == "table_card":
            rows = "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>" for r in p["rows"])
            heads = "".join(f"<th>{html.escape(h)}</th>" for h in p["headers"])
            body = f'<table class="cmp"><tr>{heads}</tr>{rows}</table>'
        elif t == "list_card":
            lis = "".join(f'<li><span class="n">{i+1}</span>{html.escape(it)}</li>' for i, it in enumerate(p["items"]))
            body = f'<ul class="biglist">{lis}</ul>'
        elif t == "terminal_card":
            body = '<div class="terminal">' + "".join(
                f'<div>{html.escape(l)}</div>' for l in p["lines"]) + "</div>"
        elif t == "flow_card":
            items = "".join(
                f'<div class="flowbox">{html.escape(s)}</div>' + ('<div class="flowarrow">➜</div>' if i < len(p["steps"])-1 else "")
                for i, s in enumerate(p["steps"]))
            body = f'<div class="flowrow">{items}</div>'
        elif t == "timeline_card":
            items = "".join(f'<div class="tlitem"><div class="tlyear">{y}</div><div class="tltext">{html.escape(x)}</div></div>'
                            for y, x in p["items"])
            body = f'<div class="tlwrap"><div class="tl">{items}</div></div>'
        elif t == "big_card":
            body = (f'<div class="bigcard"><div class="huge">{html.escape(p["big"])}</div>'
                    f'<div class="lab">{html.escape(p["label"])}</div>'
                    f'<div class="sub2">{html.escape(p.get("sub",""))}</div></div>')
        else:
            body = ""
        scene = f'<div class="cardwrap"><div class="ct"><span class="dot"></span>{html.escape(title)}</div>{body}</div>'
    narr = p.get("narr", "")
    narr_html = f'<div class="narr">{html.escape(narr)}</div>' if narr else ""
    ptitle = f'<span class="ptitle">{html.escape(title)}</span>' if title and t != "chapter_card" else ""
    return f'''  <section class="panel">
    <span class="ptag">P.{idx}</span>
    {ptitle}
    {scene}
    {"".join(inner_parts)}
    {narr_html}
  </section>'''

def main():
    pages = []   # (title, lines) 给 TTS 用
    sections = []
    idx = 0
    for ch in CHAPTERS:
        # 章头卡（自动生成，含口播两句）
        sub_spoken = ch["sub"].replace("·", "，")
        card = {"type": "chapter_card",
                "lines": [f"第{ch['num']}章，{ch['title']}。", f"{sub_spoken}。这一站，我们把它讲透。"]}
        for p in [card] + ch["panels"]:
            idx += 1
            sections.append(panel_html(idx, ch, p))
            pages.append({"page": idx, "chapter": ch["num"],
                          "lines": p.get("spoken", p["lines"])})
    doc = f'''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RustDesk 深度 30 分钟 · 动态漫画</title>
<style>{CSS}</style></head>
<body><div class="comic">

  <header class="cover">
    <div class="stripe"></div>
    <p style="font-size:14px;letter-spacing:3px;opacity:.7;">开源软件底细系列 · 第 1 话 · 完整版</p>
    <h1>RustDesk <span class="num">底细大揭秘</span></h1>
    <p class="sub">30 分钟深度版：原理 · 架构 · 自建 · 安全 · 商业 · 横评 · 实战</p>
  </header>

{chr(10).join(sections)}

  <div class="factbox">
    <h3>📌 本页知识清单</h3>
    <ul>
      <li>远控四步舞：报 ID → 问路 → 打洞 → 中继兜底；能直连绝不中继。</li>
      <li>端口速记：21116 信令(TCP+UDP)、21117 中继、21118 IP 直连。</li>
      <li>技术栈：客户端 Rust+Flutter 六端同源；服务端 hbbs/hbbr 两个轻量程序。</li>
      <li>自建：Docker 两条命令；三大坑=端口不全、key 不配对、漏 UDP 21116。</li>
      <li>商业：open-core——免费区大方，付费四档，利润奶牛是定制客户端授权。</li>
      <li>结论均标注"推测/未证实"者为公开信息合理推断，非官方口径。</li>
    </ul>
  </div>

  <footer>—— 开源软件底细系列 · 30 分钟完整版 · 2026-08-30 ——</footer>
</div></body></html>'''
    out = pathlib.Path(__file__).parent / "comic30.html"
    out.write_text(doc, encoding="utf-8")
    import json
    (pathlib.Path(__file__).parent / "pages.json").write_text(
        json.dumps(pages, ensure_ascii=False, indent=0), encoding="utf-8")
    total = sum(len(l) for pg in pages for l in pg["lines"])
    est = total / 5.05 + len(pages) * (0.5 + 0.8 + 0.45 * 3)
    print(f"panels: {idx}, total chars: {total}, est duration: {est/60:.1f} min")

if __name__ == "__main__":
    main()

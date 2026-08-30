# 漫画素材配方库（SVG 片段，复制即用）

所有片段可直接贴进 `.panel` 的 `<svg class="scene">` 里，用 `transform="translate(x,y)"` 摆位。配色沿用 SKILL.md 的 token。

## 角色

### 路由器 / 机器人主角（三种表情状态）

```svg
<!-- 站立开心 -->
<g transform="translate(300,150)">
  <rect x="0" y="30" width="124" height="60" rx="12" fill="#ffe082" stroke="#2b2622" stroke-width="3.5"/>
  <line x1="24" y1="30" x2="16" y2="2" stroke="#2b2622" stroke-width="4" stroke-linecap="round"/>
  <line x1="100" y1="30" x2="108" y2="2" stroke="#2b2622" stroke-width="4" stroke-linecap="round"/>
  <circle cx="16" cy="0" r="4" fill="#e8542f"/><circle cx="108" cy="0" r="4" fill="#e8542f"/>
  <circle cx="46" cy="52" r="5.5" fill="#2b2622"/><circle cx="78" cy="52" r="5.5" fill="#2b2622"/>
  <path d="M50 68 Q62 76 74 68" stroke="#2b2622" stroke-width="3.5" fill="none"/>
</g>
```

- 晕倒/死机：给机身 rect 加 `transform="rotate(84 0 30)"`，眼睛换成 ✕✕：
  `<circle cx="30" cy="72" r="6" fill="none" stroke="#2b2622" stroke-width="3"/><path d="M24 66 L36 78 M36 66 L24 78" stroke="#2b2622" stroke-width="3"/>`
- 睡觉打 Z：头顶加 `<text font-size="15" font-weight="900" fill="#e8542f">zzZ……</text>`
- 开心眯眼：眼睛换成弧线 `<path d="M38 52 Q46 46 54 52" .../>`
- 名牌：机身下方加白底小 rect + 等宽字体文字。

### 笔记本电脑

```svg
<g transform="translate(80,200)">
  <rect width="110" height="64" rx="9" fill="#e1f5d3" stroke="#2b2622" stroke-width="3"/>
  <circle cx="38" cy="30" r="5" fill="#2b2622"/><circle cx="72" cy="30" r="5" fill="#2b2622"/>
  <path d="M46 46 Q55 52 64 46" stroke="#2b2622" stroke-width="3" fill="none"/>
</g>
```

### 手机

```svg
<g transform="translate(680,230)">
  <rect width="56" height="94" rx="10" fill="#e3f2fd" stroke="#2b2622" stroke-width="3"/>
  <circle cx="20" cy="36" r="5" fill="#2b2622"/><circle cx="40" cy="36" r="5" fill="#2b2622"/>
  <path d="M20 56 Q30 64 40 56" stroke="#2b2622" stroke-width="3" fill="none"/>
</g>
```

### 光猫 / 机顶盒类（灰盒子+指示灯）

```svg
<g transform="translate(60,270)">
  <rect width="105" height="56" rx="10" fill="#cfd8dc" stroke="#2b2622" stroke-width="3"/>
  <circle cx="24" cy="24" r="5" fill="#43a047"/><circle cx="42" cy="24" r="5" fill="#e53935"/>
</g>
```

## 道具与图示

### 信封（数据包）

```svg
<g transform="translate(80,150)">
  <rect width="92" height="58" rx="8" fill="#fff" stroke="#2b2622" stroke-width="3"/>
  <path d="M0 0 L46 32 L92 0" fill="none" stroke="#2b2622" stroke-width="3"/>
  <text x="46" y="76" text-anchor="middle" font-size="12">寄件人标签</text>
</g>
```

### 大箭头（流向）

```svg
<path d="M0 16 H100 M86 2 L100 16 L86 30" stroke="#e8542f" stroke-width="6" fill="none" stroke-linecap="round"/>
```
方向：左箭头把 H 与折线镜像；绿色 `#43a047`=回程/成功，蓝 `#2f6fe8`=请求，红=强调。

### 盖章动作

```svg
<rect x="42" y="16" width="70" height="26" rx="5" fill="#ffd94a" stroke="#e8542f" stroke-width="2.5" transform="rotate(-6 42 16)"/>
<text x="76" y="34" text-anchor="middle" fill="#e8542f" font-size="11" font-weight="900" transform="rotate(-6 76 34)">STAMP!</text>
```

### 断掉的公路（故障示意）

```svg
<line x1="150" y1="32" x2="230" y2="32" stroke="#2b2622" stroke-width="7" stroke-dasharray="16 10"/>
<path d="M178 12 L204 52 M204 12 L178 52" stroke="#e53935" stroke-width="6" stroke-linecap="round"/>
```

### 决策二分框（排查方法论格）

```svg
<rect x="300" y="28" width="260" height="52" rx="10" fill="#fff" stroke="#2b2622" stroke-width="3.5"/>
<text x="430" y="60" text-anchor="middle" font-size="13.5" font-weight="800">第一步：{{检查动作}}</text>
<!-- 左右分支：通→绿底 #e2f2dc 框；不通→红底 #ffe4d1 框，stroke 同色系 -->
```

### 浏览器窗口（讲后台/网页时用）

```svg
<g transform="translate(70,56)">
  <rect width="430" height="290" rx="12" fill="#fff" stroke="#2b2622" stroke-width="3.5"/>
  <rect width="430" height="40" fill="#e0d6bd" stroke="#2b2622" stroke-width="3.5" rx="12"/>
  <circle cx="24" cy="20" r="6" fill="#e53935" stroke="#2b2622" stroke-width="2"/>
  <rect x="86" y="8" width="330" height="24" rx="12" fill="#fff" stroke="#2b2622" stroke-width="2.5"/>
  <text x="104" y="25" font-size="14" font-weight="800" font-family="ui-monospace,Menlo,monospace" fill="#2f6fe8">http://{{地址}}</text>
</g>
```

### 柜台（办事/服务类隐喻）

```svg
<rect x="20" y="60" width="150" height="14" fill="#b08968" stroke="#2b2622" stroke-width="3"/>
<rect x="30" y="74" width="130" height="70" fill="#e6ccb2" stroke="#2b2622" stroke-width="3"/>
```

## 文字元素

- 拟声词（HTML，绝对定位在 .panel 内）：`<span class="sfx" style="top:...;left:...;font-size:34px;">ズバッ!</span>`；日系可用「ドン!」「ガタガタ」「安睡中…zzZ」。
- 网格纸场景底纹：
  `<defs><pattern id="grid" width="43" height="43" patternUnits="userSpaceOnUse"><path d="M43 0H0V43" fill="none" stroke="#d9cba8" stroke-width="1"/></pattern></defs><rect width="860" height="460" fill="url(#grid)"/>`
- 场景底色可选：`#f2ead6 / #efe7d2 / #f6efdd / #ece2c8`（米色系轮着用，避免每格雷同）。

## 对话框位置约定

- `.bub` 默认尾巴朝下偏左；说话人在右时用 `tail-r`；旁白在上方说话人下方时用 `tail-b`。
- 对白放 SVG 外层（HTML），不要塞 `<text>` 长句——SVG 文字不会自动换行。

## 交付前验证（必跑）

```bash
python3 - <<'EOF'
from html.parser import HTMLParser
import sys
class P(HTMLParser):
    VOID={'meta','br','img','input','hr','link','path','circle','rect','line','ellipse'}
    def __init__(self):
        super().__init__(); self.stack=[]; self.errs=[]
    def handle_starttag(self,t,a):
        if t not in self.VOID: self.stack.append(t)
    def handle_endtag(self,t):
        if t in self.VOID: return
        if self.stack and self.stack[-1]==t: self.stack.pop()
        else: self.errs.append(f"mismatch </{t}> line {self.getpos()[0]}")
p=P()
src=open(sys.argv[1],encoding='utf-8').read()
p.feed(src)
print("errors:", p.errs or "none"); print("unclosed:", p.stack or "none")
EOF
```

用法：`python3 check.py <文件路径>`（heredoc 版把 open 的路径换成实际文件）。必须 `errors: none` 且 `unclosed: none`。

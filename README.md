# 漫画讲解工坊 Comic Explainer

> 零依赖、单文件、手绘风的 HTML 漫画模板 —— 用 SVG 分镜 + 清晰中文对话框，把任何知识讲成一个故事。
>
> English: a zero-dependency, single-file, hand-drawn-style HTML comic template. Explain any topic as a story with SVG panels and crisp CJK speech bubbles. [README (English) →](README-EN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![单文件](https://img.shields.io/badge/%E5%8D%95%E6%96%87%E4%BB%B6-one%20HTML-2f6fe8)
![零依赖](https://img.shields.io/badge/%E9%9B%B6%E4%BE%9D%E8%B5%96-no%20dependencies-43a047)

## 为什么不用 AI 生图？

生图模型画**中文文字**几乎必糊，风格跨格漂移，而且画出来的字没法改。本项目反其道而行：

| 层 | 技术 | 负责 |
|---|---|---|
| 画面 | 内联 SVG（圆/矩形/线条/路径） | 角色、道具、场景 |
| 文字 | HTML + CSS 气泡/旁白 | 对白、旁白、拟声词 |
| 漫画感 | 30 行 CSS | 粗边框 + 纯色偏移阴影 + 纸纹底色 |

结果：**中文永远清晰、任何一句话改一行代码、矢量缩放不糊、整个漫画一个 .html 文件（约 30KB）**。

## 在线预览 / Live demos

- 🏠 [门房大叔 192.168.10.1](https://wahailong.github.io/comic-explainer/examples/network-gatekeeper.html) —— 把「路由器是什么」画成小镇故事
- 🧑 [画人能力小样](https://wahailong.github.io/comic-explainer/examples/human-drawing-demo.html) —— Q 版人物图鉴与画风边界自检

（也可直接下载 `examples/*.html` 本地用浏览器打开，完全离线可用。）

## 快速上手（3 步）

1. 复制 [`skill/template.html`](skill/template.html) —— 这是完整页面骨架：封面、分镜格、对话框（3 种尾巴方向）、黑底旁白、拟声词、干货框的 CSS 全部就位。
2. 替换所有 `{{占位符}}`：标题、每格 `.ptitle`、气泡 `.bub`、旁白 `.narr`。
3. 用 [`skill/reference.md`](skill/reference.md) 的 SVG 配方画场景，每格一个 `<svg class="scene" viewBox="0 0 860 4xx">`。

### 分镜幕序模板（直接套）

```
① 全景格    建立世界观（把主题域拟人化：网络=小镇、内存=仓库……）
② ~ ⑤ 概念格 一个核心知识点一幕，剧情=概念隐喻
⑥ 特别篇    若有真实经历/故障现场，改编进来（共鸣感来源）
⑦ 收束格    方法论/口诀 + .factbox 知识清单
```

## 设计系统

- 配色 token：墨线 `#2b2622`、纸底 `#f7f1e3`、强调红 `#e8542f`、蓝 `#2f6fe8`、漫画黄 `#ffd94a`
- 漫画感三件套：`border: 3.5px solid` + `box-shadow: 6px 6px 0`（纯色偏移）+ 米色径向渐变纸纹
- 文字量红线：每格对白 ≤ 3 行、旁白 ≤ 2 行，讲不清就拆格
- SVG 里只放短标签（人名/按钮/门牌号），**整句对白一律放 HTML `.bub`**（SVG `<text>` 不换行）

## 给 AI Agent 用（Agent Skills）

`skill/` 目录同时是一个标准的 Agent Skill（SKILL.md + 模板 + 素材库），已适配 [QwenWork](https://qwenwork.cn)；对 Claude Code / 其他支持 SKILL.md 的 agent，把目录拷进各自的 skills 路径即可。装好后对 agent 说：

> 「用漫画讲讲 Docker」→ 自动出第 N 话，风格与前作统一，还能喊旧角色客串

内置 4 种玩法：讲概念 / 真实事件改编 / 软件教程 / 同风格续集。

## 目录结构

```
comic-explainer/
├── README.md / README-EN.md
├── LICENSE                     # MIT
├── skill/
│   ├── SKILL.md                # 工作流：分镜→绘制→校验→交付
│   ├── template.html           # 页面骨架（起手就拷它）
│   └── reference.md            # SVG 素材配方库 + 标签闭合校验脚本
└── examples/
    ├── network-gatekeeper.html # 第 1 话：路由器 192.168.10.1
    └── human-drawing-demo.html # 画人能力小样
```

## 能力边界（诚实版）

- ✅ 放心画：Q 版人物、动物、机器人、载具、建筑、流程图、漫画分镜
- ❌ 画不了：写实人脸、复杂透视、细腻光影 —— 这类交给 AI 生图，然后**字仍然用代码排**（混合法：AI 画无字插画 + 本模板排气泡）

## 校验

发布前跑 `reference.md` 里的 Python 标签闭合检查，要求 `errors: none` 且 `unclosed: none`。

## License

[MIT](LICENSE) — 随便用，标注出处会更开心，但不强制。

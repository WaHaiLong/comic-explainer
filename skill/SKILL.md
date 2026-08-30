---
name: comic-explainer
name_en: Comic Explainer
name_zh: 漫画讲解工坊
description: Turns any topic, concept, or real event into a scrollable hand-drawn-style single-file HTML comic (SVG panels + crisp Chinese speech bubbles). Use when the user asks for 漫画讲解, 做成漫画故事, 科普漫画, comic-style explanation, or wants to turn an explanation or incident into a visual story.
description_en: Turns any topic, concept, or real event into a scrollable hand-drawn-style single-file HTML comic (SVG panels + crisp Chinese speech bubbles). Use when the user asks for a comic-style explanation.
description_zh: 把任意知识点、工具或真实事件改编成可滚动手绘风单文件 HTML 漫画（SVG 分镜 + 清晰中文对话框）。用户说"用漫画讲/做成漫画故事/科普漫画"时使用。
argument-hint: 给出想漫画化的主题、概念或真实事件
argument-hint-en: Give a topic, concept, or real event to turn into a comic story
argument-hint-zh: 给出想漫画化的主题、概念或真实事件
user-invocable: true
---

# 漫画讲解工坊

把讲解内容变成一篇 6~8 格的手绘风 HTML 漫画。**永远不用 AI 生图画分镜**（中文文字必糊、风格漂移、不可改字），一律 SVG 画形 + HTML 排字。

## 工作流

1. **设计分镜脚本**（先列给用户看，可跳过直接做）
   - 把主题的每个知识点映射成一幕剧情；抽象概念必须拟人化/场景化（例：路由器=门房大叔、IP=门牌号、数据包=信封、NAT=盖章、故障=门房晕倒）。
   - 标准幕序：①全景建立世界观 → ②~⑤每个核心概念一幕 → ⑥"今日特别篇"（若对话中有真实事件/排障经历，改编进来）→ ⑦方法论/口诀收束。
   - 结尾必须有一个 `.factbox`「本页知识清单」做干货回收。
2. **复制 [template.html](template.html) 起手**，逐格替换占位内容。铁律：单文件、全部内联（无外链字体/图片/JS）、viewBox 宽固定 860、格高 400~460。
3. **画场景**：角色与道具的 SVG 配方在 [reference.md](reference.md)（路由器人、笔记本、手机、信封+箭头、决策框、对话框变体、拟声词）。同一角色跨格保持同配色（CSS 变量已定义）。
4. **验证**：跑 reference.md 里的 Python 标签闭合检查，`errors: none` 且 `unclosed: none` 才算过；不过就修，别交付坏页。
5. **交付**：存到 `outputs/<主角名>-漫画讲解.html`，用 `qwenwork_file_present_files` 呈现，再用 3~5 行概述每格剧情（不要长篇复述知识本身）。

## 设计规则

- 配色 token（template 已内置）：墨线 `--ink #2b2622`、纸 `--paper #f7f1e3`、强调红 `--accent #e8542f`、蓝 `--blue #2f6fe8`、漫画黄 `--yellow #ffd94a`。
- 漫画感三件套：粗边框 + `box-shadow: 6px 6px 0` 纯色偏移阴影 + 网点纸背景；旁白用黑底 `.narr` 条，对话用白底 `.bub`（尾巴方向 `tail-r`/`tail-b` 可变）。
- 文字量控制：每格对白 ≤ 3 行、旁白 ≤ 2 行；讲不清的概念宁可拆成两格。
- SVG 里的文字只用短标签（角色名、门牌号、按钮），整句对话一律放 HTML `.bub`，方便换主题时改。
- 语言跟随用户对话语言。

## 换主题复用要点

复用时只换三样：分镜脚本（幕序不变）、角色阵容（从 reference.md 配方改配色/配件）、每格文案。CSS 与页面骨架一个字都不用动。

# Comic Explainer 漫画讲解工坊

> A zero-dependency, single-file, hand-drawn-style HTML comic template. Explain any topic as a story with SVG panels and crisp CJK speech bubbles. 中文版见 [README.md](README.md)。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Why not AI image generation?

Text-to-image models garble CJK text, drift in style across panels, and the baked-in words can never be edited. This project inverts the stack:

| Layer | Tech | Handles |
|---|---|---|
| Art | Inline SVG (circles / rects / lines / paths) | Characters, props, scenes |
| Text | HTML + CSS bubbles / captions | Dialogue, narration, SFX |
| Manga feel | ~30 lines of CSS | Thick borders + solid offset shadows + paper grain |

Result: **perfectly sharp CJK text, every sentence editable in one line of code, infinitely scalable, the whole comic is one ~30 KB .html file.**

## Live demos

- 🏠 [The Gatekeeper 192.168.10.1](https://wahailong.github.io/comic-explainer/examples/network-gatekeeper.html) — "what is a router" as a little-town story (zh)
- 🤖 [Bit Learns to Cook · Self-Improving Agents](https://wahailong.github.io/comic-explainer/examples/cs329a-self-improving-agents.html) — Stanford CS329A told as a cooking-and-food-critic story (zh)
- 🧑 [Character drawing sampler](https://wahailong.github.io/comic-explainer/examples/human-drawing-demo.html) — chibi cast & style limits (zh)

Download `examples/*.html` and open in any browser — fully offline.

## Quick start (3 steps)

1. Copy [`skill/template.html`](skill/template.html) — the full page skeleton (cover, panels, 3 bubble tail directions, narration bar, SFX, fact box) is ready.
2. Replace every `{{placeholder}}`: titles, `.ptitle`, `.bub`, `.narr`.
3. Draw scenes with the SVG recipes in [`skill/reference.md`](skill/reference.md), one `<svg class="scene" viewBox="0 0 860 4xx">` per panel.

### Storyboard formula

```
① Wide shot     Build the world (anthropomorphize the domain: network = town, RAM = warehouse...)
② – ⑤ Concept    One panel per core idea; the plot IS the metaphor
⑥ Special       Adapt a real incident you lived through (this is where the charm comes from)
⑦ Wrap-up       A mnemonic + the .factbox knowledge checklist
```

## Design system

- Tokens: ink `#2b2622`, paper `#f7f1e3`, accent red `#e8542f`, blue `#2f6fe8`, manga yellow `#ffd94a`
- Manga feel: `border: 3.5px solid` + `box-shadow: 6px 6px 0` (flat offset) + radial-gradient paper grain
- Text budget: ≤ 3 dialogue lines and ≤ 2 narration lines per panel — split the panel instead
- Keep SVG text to short labels; **all full sentences live in HTML `.bub`** (SVG `<text>` never wraps)

## For AI agents

`skill/` is also a standard Agent Skill (SKILL.md + template + recipe book). Drop the folder into your agent's skills directory (QwenWork, Claude Code, etc.) and just say *"explain Docker as a comic"* — consistent style, recurring characters, sequels supported.

## Honest limits

- ✅ Great at: chibi characters, animals, robots, vehicles, buildings, flowcharts, manga panels
- ❌ Bad at: photorealistic faces, complex perspective, fine lighting — use image generation for those, then keep the text in code (hybrid: AI art without text + this template for bubbles)

## Validation

Run the Python tag-balance checker in `reference.md` before shipping; require `errors: none` and `unclosed: none`.

## License

[MIT](LICENSE)

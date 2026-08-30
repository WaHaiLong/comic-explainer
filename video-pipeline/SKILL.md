---
name: comic-to-video
name_en: Comic to Video
name_zh: 漫画转动态漫视频
description: Turn a comic-explainer HTML comic into a narrated motion-comic MP4 (panel screenshots + camera moves + Chinese TTS + burned-in subtitles + BGM), plus platform release pack (covers, chapters, bilingual copy). Use when the user asks 做成视频, 动态漫, 给漫画配音, 漫画转视频, or wants a comic published to Bilibili/YouTube.
description_en: Turn a comic-explainer HTML comic into a narrated motion-comic MP4 with Chinese TTS, burned-in subtitles and BGM, plus platform release packs.
description_zh: 把 comic-explainer 漫画 HTML 变成带配音、大字幕、运镜与 BGM 的动态漫 MP4，并产出 B站/YouTube 发布包。用户说"做成视频/配音/动态漫/发平台"时使用。
argument-hint: 漫画 HTML 路径 + 配音风格（标准/评书腔/分角色）
argument-hint-en: Comic HTML path + narration style (standard / storyteller / per-character)
argument-hint-zh: 漫画 HTML 路径 + 配音风格（标准/评书腔/分角色）
user-invocable: true
---

# 漫画转动态漫视频（comic-explainer 下游管线）

产物：1080p/30fps MP4（分镜逐格运镜 + 中文配音 + 黄字大字幕 + BGM）+ 发布包（封面/章节轴/双平台文案）。工作目录建议 `video_<主题>/{slides,pngs,aud,seg,subs}`。

## 流水线（顺序执行）

1. **配音剧本** `script.json`：`{"<页码>": [["角色","台词"],…]}`。每页 1~3 条、单条 ≤90 字（约 20s 内）。风格三选一：标准播报 / 评书腔（结论先行+自问自答+职场隐喻+口头禅）/ 分角色。**时长硬规则**（搬自火宝短剧提示词资产）：单段音轨 ≥ 台词字数÷4.5 字/秒 + 2s 余量；全片总时长 ≈ 剧本总字数÷500 字/分钟（±20%），超了砍台词不砍画面；分格必须落在【开场】【触发】【高潮】【收尾】节拍边界，同一因果链不许切散；口播稿禁抽象形容词（"很伤心""紧张"），一律转可见描写（"低下头、攥紧杯沿"）——评书腔同理。
2. **拆页截图**：从漫画 HTML 正则提取 `<header class="cover">` 与各 `<section class="panel">`，逐页包进 1920×1080 舞台（`.stage{width:860px;transform:translate(-50%,-50%) scale(2.02)}`，px 定位的气泡会随 SVG 等比缩放，勿改布局）。Chrome 无头截图：`--headless --window-size=1920,1080 --hide-scrollbars --screenshot`。
3. **TTS**：首选 **edge-tts**（微软神经音色，比 macOS `say` 自然一个次元）：`python -m edge_tts --voice zh-CN-YunjianNeural --rate=+12% --proxy socks5h://127.0.0.1:7890 --text ... --write-media x.mp3`，国内直连报 `NoAudioReceived` 必须走代理；mp3→`ffmpeg -ar 44100 -ac 2` 转 wav。**定版音色：云健 zh-CN-YunjianNeural rate+12%（评书腔，用户拍板）**，edge-tts 音量偏轻，成片混音时人声轨加 `volume=2.2` 再限幅。备选 `say -v <音色> -r 235~255`。**say 音色必须用完整显示名**（见坑①）。每句生成后断言时长 >1s，防整段静音。可仿口吻，**不克隆真人声音**（声纹授权红线，平台判违规）。
4. **每页音轨**：0.5s 前置 + 句间 0.45s + 尾 0.8s 静音拼接；评书腔/大嗓门加 `volume=1.75,alimiter=limit=0.92`。
5. **字幕**：按 `[，。！？；：]` 切 ≤20 字条，句内按字数比例分摊实测时长。渲染成**透明底 PNG**（HTML + Chrome `--default-background-color=00000000`），样式：PingFang 52px 900 `#ffd94a` + 四向 text-shadow 描边，**bottom:168px**（避开漫画自带旁白条）。
6. **分段渲染**：每段 = PNG + 音轨，zoompan 缓推缓拉交替（输入先 `scale=3840:2160` 减抖，`d=时长×30`）。可选黑底大字开场/收场卡（同 Chrome 截图，配静默音轨）。
7. **合成一条命令**：N 段 + M 张字幕 PNG + BGM 全部作输入 → `concat=n=N:v=1:a=1`（滤镜！见坑③）→ 逐条 `overlay=enable='between(t,a,b)'` → `amix` BGM（volume≈0.32）→ `alimiter` + 尾部 `afade`。
8. **BGM**：先试 `qwenwork_music_generate`（见坑④，常失败）；兜底本地合成：Python wave 写五声音阶八分拨弦（指数衰减正弦+泛音）+ 每拍贝斯 + 反拍噪声沙锤，73s 循环，峰值归一 ~0.22。
9. **验收（必做）**：`ffprobe` 视频流与音频流时长差 <0.5s（坑③同类漂移）；抽 2 帧看字幕对齐与遮挡；`volumedetect` mean ≈ -19~-22dB。
10. **发布包**：封面 = 大字 HTML → Chrome 截图 1920×1080 PNG + `sips -Z 1280` 出 YouTube jpg；章节轴 = 逐段实测时长累加；文案包 = B站（分区/标题/简介/标签）+ YouTube（双语 description/章节/Category），**必含 AI 语音申报提醒**；仿写口吻注明"与任何创作者无关"。

## 竖屏 9:16 版（抖音/快手/视频号必做）

不是加黑边，是重排版式：1080×1920 舞台，顶部常驻系列徽章+大标题（70~330px 区），中段漫画格 `.stage{left:40px;top:640px;width:860px;transform-origin:top left}` 缩放 **1.1628**（左右各留 40px 安全边距），底部字幕区。运镜改**纵向**缓推缓拉：输入 `scale=2160:3840`，`zoompan z=1.06`（>1.1 会裁掉格内边缘文字！实测 1.16 切掉"第二站"标题），y 在 `0..(ih-ih/zoom)` 逐帧线性移动、奇偶页换方向；字幕 PNG 重出 1080×1920 版，`bottom:420px`。音轨与横屏共用，事件时间轴不变。

## 重配音（换嗓子不动画）

面板 PNG、字幕 PNG 全部复用：①新音色重跑逐句 TTS；②重拼每页音轨；③重算字幕事件时间轴（**断言切条数不变**，变了才需重截字幕 PNG）；④分段重渲染（时长变了）；⑤若只是响度不够，跳过 ①-④，仅在最终混音给 `[ca]volume=2.2` 重跑合成。视频号**已发布视频换不了视频文件**，只能重发新帖+引导用户手机长按删旧。

## 坑录（全部实测踩过）

- ① `say` 新音色裸名（Eddy/Grandpa/Shelley/Rocko）读中文 = **纯静音 0.016s**，必须 `"Eddy (中文（中国大陆）)"`；Tingting 例外。
- ② zsh 下未加引号的变量不做分词，ffmpeg 参数串会被当成单个文件名——多参数拼接一律走 Python subprocess 列表。
- ③ zoompan + `-loop 1` 的段用 `concat demuxer -c copy` 拼接，**视频流会比音频长出一截**（帧溢出，实测 134s 变 155s）；必须用 `concat` **滤镜**重编码收尾。
- ④ `qwenwork_music_generate` 纯 BGM 会报 `lyrics_prompt` 校验错（`auto_lyrics=false` 也救不了），失败标记 resumable=false 时直接转本地合成，别死磕。
- ⑤ Homebrew ffmpeg 8 可能没编 libass/drawtext（`subtitles` 滤镜不存在）→ 透明 PNG + overlay 是通用替代；`subtitles=` 语法也要写成 `subtitles=filename=`。
- ⑥ 所有 ffmpeg 重跑命令带 `-y`，否则静默跳过覆盖，产出的还是旧文件。
- ⑦ `loudnorm` 的 TP 取值范围 [-9,0]，传 2 直接报错；简单场景 volume+alimiter 足够。
- ⑧ filter_complex 里 bgm 输入索引 = 段数 + 字幕张数（从 0 数），差一位报 Invalid file index。
- ⑨ 字幕 bottom 太大会压住漫画格底部黑旁白条（两者都是白/黄字，糊成一团）。
- ⑩ zsh 通配符**无匹配会在执行前中止整条命令行**（`&&` 链后半静默不跑，表现为"文件不存在"假象）——多 glob 清理逐条执行或 `setopt null_glob`。
- ⑪ 两阶段发布脚本的 GO 旗标文件用完**必须立刻移走**（`mv 到 ~/.Trash/`），否则下次脚本秒发；`rm` 会被 Bash 安全层拦截且连带中断 `&&` 链。

## 交付

成片与封面、文案包复制到 outputs 并 `present_files`；若仓库化发布，视频放 `videos/`（<100MB 免 LFS），push 前先 `git pull --rebase`（多会话并发仓库）。

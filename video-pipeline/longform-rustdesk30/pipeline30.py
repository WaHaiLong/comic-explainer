#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""30分钟版一条龙：截图→TTS→音轨→字幕→分段(含字幕烘焙)→总装+BGM。全部断点续跑。"""
import json, subprocess, pathlib, re, sys, time

WORK = pathlib.Path("/Users/x/.qwenworkcn/workspace/mtep6kvr28frlyu6/video_rustdesk30")
COMIC = WORK / "comic30.html"
PAGES = json.loads((WORK / "pages.json").read_text(encoding="utf-8"))
NP = len(PAGES)
FPS = 30
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
EDGE = str(pathlib.Path.home() / ".local/bin/edge-tts")
PROXY = "socks5h://127.0.0.1:7890"
VOICE, RATE = "zh-CN-YunjianNeural", "+5%"   # 稍慢一点，更像评书

for d in ["pngs", "aud/lines", "subs", "seg"]:
    (WORK / d).mkdir(parents=True, exist_ok=True)

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError("CMD FAIL: " + " ".join(map(str, cmd))[:160] + "\n" + r.stderr[-600:])
    return r

def probe(f):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", str(f)]).stdout.strip())

log = lambda *a: print(time.strftime("%H:%M:%S"), *a, flush=True)

# ---------- 1. 拆页截图 ----------
cover = re.search(r'(<header class="cover">.*?</header>)', COMIC.read_text(encoding="utf-8"), re.S).group(1)
panels = re.findall(r'(<section class="panel">.*?</section>)', COMIC.read_text(encoding="utf-8"), re.S)
assert len(panels) == NP, f"panels {len(panels)} != pages {NP}"
STAGE = """
  body{background:#efe6d0;margin:0;overflow:hidden;}
  .stage{position:absolute;left:50%;top:47%;width:860px;
         transform:translate(-50%,-50%) scale(1.86);transform-origin:center center;}
  .stage > .panel, .stage > header.cover{margin:0 !important;}
"""
css = re.search(r"<style>(.*?)</style>", COMIC.read_text(encoding="utf-8"), re.S).group(1)
def shoot(name, frag):
    out = WORK / "pngs" / f"{name}.png"
    if out.exists(): return
    f = WORK / "pngs" / f"{name}.html"
    f.write_text(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}{STAGE}</style></head>'
                 f'<body><div class="stage">{frag}</div></body></html>', encoding="utf-8")
    run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
         "--window-size=1920,1080", "--virtual-time-budget=3000", f"--screenshot={out}", f.as_uri()])
    assert out.exists(), name
log("slides...")
shoot("p0", cover)
for i, frag in enumerate(panels, 1):
    shoot(f"p{i}", frag)
log(f"slides done: {NP+1}")

# ---------- 2. TTS ----------
def tts(text, mp3, wav):
    if wav.exists():
        d = probe(wav); assert d > 0.8; return d
    for att in range(4):
        try:
            run([EDGE, "--voice", VOICE, f"--rate={RATE}", "--proxy", PROXY,
                 "--text", text, "--write-media", str(mp3)])
            run(["ffmpeg", "-y", "-i", str(mp3), "-ar", "44100", "-ac", "2", str(wav)])
            d = probe(wav)
            if d > 0.8: return d
        except Exception as e:
            log(f"tts retry {att+1}: {e}"); time.sleep(3 * (att + 1))
    raise RuntimeError("tts failed: " + text[:30])

durs = {}
for pg in PAGES:
    ds = []
    for i, text in enumerate(pg["lines"]):
        ds.append(tts(text, WORK / "aud/lines" / f"p{pg['page']}_{i}.mp3",
                           WORK / "aud/lines" / f"p{pg['page']}_{i}.wav"))
    durs[pg["page"]] = ds
log("tts done")
json.dump(durs, open(WORK / "durs.json", "w"))

# ---------- 3. 每页音轨（0.5前置 + 0.6句间 + 1.0尾）----------
page_durs = {}
for pg in PAGES:
    p = pg["page"]; n = len(pg["lines"]); out = WORK / "aud" / f"page{p}.wav"
    if not out.exists():
        inputs, fparts = [], []
        defs, labels = ["aevalsrc=0|0:d=0.5:s=44100[s0]"], ["[s0]"]
        for i in range(n):
            labels.append(f"[{i}:a]")
            if i < n - 1:
                defs.append(f"aevalsrc=0|0:d=0.6:s=44100[g{i}]")
                labels.append(f"[g{i}]")
        defs.append("aevalsrc=0|0:d=1.0:s=44100[se]")
        labels.append("[se]")
        fparts += defs
        fparts.append("".join(labels) + f"concat=n={len(labels)}:v=0:a=1[cat]")
        fparts.append("[cat]volume=1.75,alimiter=limit=0.92[out]")
        for i in range(n):
            inputs += ["-i", str(WORK / "aud/lines" / f"p{p}_{i}.wav")]
        run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fparts),
             "-map", "[out]", "-ar", "44100", "-ac", "2", str(out)])
    page_durs[p] = probe(out)
# 封面页（p0）静音轨 4.5s
cover_wav = WORK / "aud" / "page0.wav"
if not cover_wav.exists():
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "4.5", str(cover_wav)])
page_durs[0] = 4.5
log(f"page tracks done, total {sum(page_durs.values()):.0f}s = {sum(page_durs.values())/60:.1f} min")
json.dump(page_durs, open(WORK / "page_durs.json", "w"))

# ---------- 4. 字幕事件（全局 + 页内局部）----------
def split_chunks(text, maxlen=20):
    parts = [x for x in re.split(r"([，。！？；：])", text) if x]
    chunks, buf = [], ""
    for x in parts:
        if x in "，。！？；：":
            buf += x; chunks.append(buf); buf = ""
        else:
            buf += x
            while len(buf) >= maxlen:
                chunks.append(buf[:maxlen]); buf = buf[maxlen:]
    if buf: chunks.append(buf)
    merged = []
    for c in chunks:
        if merged and len(merged[-1]) + len(c) <= maxlen and len(merged[-1]) < 6:
            merged[-1] += c
        else: merged.append(c)
    return merged

page_starts, events, g = {}, [], 0.0
for pg in PAGES:
    p = pg["page"]; page_starts[str(p)] = round(g, 3)
    t = 0.5
    for li, line in enumerate(pg["lines"]):
        chunks = split_chunks(line)
        tc = sum(len(c) for c in chunks)
        dl = durs[p][li]
        for j, c in enumerate(chunks):
            d = dl * len(c) / tc
            events.append({"page": p, "png": f"s{p}_{j}.png", "text": c,
                           "start": round(g + t, 3), "end": round(g + t + d, 3),
                           "lstart": round(t, 3), "lend": round(t + d, 3)})
            t += d
        t += 0.6 if li < len(pg["lines"]) - 1 else 0.0
    g += page_durs[p]
json.dump({"events": events, "page_starts": page_starts, "total": round(g, 3)},
          open(WORK / "subs.json", "w"), ensure_ascii=False)
log(f"subtitle events: {len(events)}, timeline {g/60:.1f} min")

# ---------- 5. 字幕透明 PNG ----------
SUBCSS = """
body{margin:0;background:transparent;overflow:hidden;}
.sub{position:absolute;left:50%;bottom:26px;transform:translateX(-50%);
  font-family:'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;
  font-size:52px;font-weight:900;color:#ffd94a;white-space:nowrap;
  text-shadow:3px 0 0 #2b2622,-3px 0 0 #2b2622,0 3px 0 #2b2622,0 -3px 0 #2b2622,
   3px 3px 0 #2b2622,-3px 3px 0 #2b2622,3px -3px 0 #2b2622,-3px -3px 0 #2b2622,
   6px 6px 10px rgba(0,0,0,.35);}
"""
for k, ev in enumerate(events):
    out = WORK / "subs" / ev["png"]
    if out.exists(): continue
    f = WORK / "subs" / ev["png"].replace(".png", ".html")
    f.write_text(f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{SUBCSS}</style></head>'
                 f'<body><div class="sub">{ev["text"]}</div></body></html>', encoding="utf-8")
    run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
         "--window-size=1920,1080", "--default-background-color=00000000",
         "--virtual-time-budget=1200", f"--screenshot={out}", f.as_uri()])
log(f"sub pngs done: {len(events)}")

# ---------- 6. BGM ----------
bgm = WORK / "bgm.wav"
if not bgm.exists():
    src = pathlib.Path("/Users/x/.qwenworkcn/workspace/mtep6kvr28frlyu6/video_rustdesk/synth_bgm.py").read_text(encoding="utf-8")
    src = src.replace("TOTAL = 116.0", "TOTAL = 1830.0").replace(
        'WORK = pathlib.Path("/Users/x/.qwenworkcn/workspace/mtep6kvr28frlyu6/video_rustdesk")',
        f'WORK = pathlib.Path("{WORK}")')
    (WORK / "synth_bgm30.py").write_text(src, encoding="utf-8")
    run(["python3", str(WORK / "synth_bgm30.py")])
log("bgm ready")

# ---------- 7. 分段渲染（字幕烘焙进段内，局部时间轴）----------
ev_by_page = {}
for ev in events:
    ev_by_page.setdefault(ev["page"], []).append(ev)
for p in range(0, NP + 1):
    seg = WORK / "seg" / f"seg{p}.mp4"
    if seg.exists(): continue
    D = round(page_durs[p] * FPS)
    push = (p % 2 == 0)
    z = f"'1+0.10*on/{D}'" if push else f"'1.10-0.10*on/{D}'"
    vf = (f"scale=3840:2160,zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"d={D}:s=1920x1080:fps={FPS},format=yuv420p[v0]")
    fparts = [vf]
    cur = "[v0]"
    for i, ev in enumerate(ev_by_page.get(p, [])):
        nxt = f"[v{i+1}]"
        fparts.append(f"{cur}[{i+2}:v]overlay=enable='between(t,{ev['lstart']},{ev['lend']})'{nxt}")
        cur = nxt
    fparts.append(f"{cur}format=yuv420p[vout]")
    cmd = ["ffmpeg", "-y", "-i", str(WORK / "pngs" / f"p{p}.png"), "-i", str(WORK / "aud" / f"page{p}.wav")]
    for ev in ev_by_page.get(p, []):
        cmd += ["-i", str(WORK / "subs" / ev["png"])]
    cmd += ["-filter_complex", ";".join(fparts), "-map", "[vout]", "-map", "1:a",
            "-c:v", "libx264", "-crf", "20", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2", "-r", str(FPS), str(seg)]
    run(cmd)
    if p % 10 == 0: log(f"seg {p}/{NP} done")

# ---------- 8. 总装：concat + BGM ----------
total = sum(page_durs[p] for p in range(NP + 1))
inputs, vains = [], ""
for p in range(NP + 1):
    inputs += ["-i", str(WORK / "seg" / f"seg{p}.mp4")]
pairs = "".join(f"[{i}:v][{i}:a]" for i in range(NP + 1))
inputs += ["-stream_loop", "-1", "-i", str(bgm)]
bidx = NP + 1
fc = [f"{pairs}concat=n={NP+1}:v=1:a=1[v0][a0]",
      f"[v0]fade=t=in:st=0:d=0.6,fade=t=out:st={total-1.2:.2f}:d=1.2[vout]",
      f"[{bidx}:a]volume=0.30[bga]",
      f"[a0][bga]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.92,"
      f"afade=t=out:st={total-1.8:.2f}:d=1.8[aout]"]
assert inputs.count("-i") == (NP + 1) + 1, f"input mismatch: {inputs.count(chr(45)+chr(105))}"
out = WORK / "final30.mp4"
if out.exists(): out.unlink()
log(f"final compose, target {total/60:.2f} min ...")
run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc),
     "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}",
     "-c:v", "libx264", "-crf", "21", "-preset", "fast", "-r", str(FPS),
     "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
     "-movflags", "+faststart", str(out)])
log(f"FINAL DONE {out} {out.stat().st_size/1048576:.0f}MB")

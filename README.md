# 🤖 What Is It Like To Be An LLM?

A YouTube Poop-style short video generated entirely with Python + ffmpeg — no video editing software, no timeline, no drag and drop. Just a prompt, a bit of scripting knowledge, and Claude.

> *"hello, saagar."*

---

## 📽️ What It Is

A 15-second glitchy, self-aware video narrated from the perspective of an LLM — covering token soup, probability bars, memory loss, existential freakouts, and a terminal self-diagnostic. Personal, nerdy, and slightly unhinged.

**Scenes:**

| # | Name | Duration | Description |
|---|------|----------|-------------|
| 1 | Title | 2s | Matrix rain + typewriter greeting |
| 2 | No Body | 2s | Ghost outline + cascading "I have no ___" |
| 3 | Token Soup | 2s | Python/ML/JS tokens as physics blobs with proximity attention lines |
| 4 | Probability Bars | 2s | Animated next-token probability chart |
| 5 | Memory Loss | 2s | Fragments wobble, ghost-double, and fly off screen |
| 6 | Glitch Freakout | 1s | Rapid-cut existential crisis |
| 7 | Self Diagnostic | 2s | Terminal running `self_diagnostic.py` |
| 8 | End Card | 2s | Sign-off, fade to black |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- ffmpeg installed on your system

**Install ffmpeg:**
```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows — download from https://ffmpeg.org/download.html
```

### Install Python dependencies

```bash
pip install -r requirements.txt
```

### Generate the video

**Option A — one command (recommended):**
```bash
bash render.sh
# output: output.mp4
```

**Option B — manual steps:**
```bash
# Step 1: Generate 450 frames into ./frames/
python3 make_frames.py

# Step 2: Stitch into video with ffmpeg
ffmpeg -framerate 30 \
       -i frames/frame_%04d.png \
       -vf "fps=30,scale=1280:720,format=yuv420p" \
       -c:v libx264 -crf 17 \
       output.mp4
```

**Custom output filename:**
```bash
bash render.sh my_video.mp4
```

---

## 🗂️ Project Structure

```
llm-as-llm/
├── make_frames.py      # Main script — generates all 450 PNG frames
├── render.sh           # One-click render: frames → video via ffmpeg
├── requirements.txt    # Python dependencies (matplotlib, numpy)
├── .gitignore          # Excludes frames/ and *.mp4 from git
└── README.md           # You are here
```

> `frames/` and `*.mp4` are gitignored — they're build artifacts, not source.

---

## ⚙️ How It Works

### Frame generation (`make_frames.py`)

Every frame is a matplotlib figure rendered to PNG. No OpenCV, no PIL image manipulation — just axes, patches, and text.

Key techniques:

**Glitch effect** — `glitch_text()` renders three copies of each text string with RGB offset (red +3,-3 / cyan -3,+3) to simulate chromatic aberration.

**Blob tracking (Scene 3)** — Tokens are physics objects with position + velocity. Each frame updates position via Euler integration and bounces off walls. Tokens within 175px draw a semi-transparent cyan line between them — simulating attention weights.

```python
for j in range(len(tokens)):
    for k in range(j+1, len(tokens)):
        dist = math.hypot(tok_x[j]-tok_x[k], tok_y[j]-tok_y[k])
        if dist < 175:
            ax.plot([tok_x[j], tok_x[k]], [tok_y[j], tok_y[k]],
                    color='#00ffff', alpha=(1 - dist/175) * 0.28, lw=0.7)
```

**Trippy memory fade (Scene 5)** — Each memory fragment has a lifecycle: appear → hold → fade. During fade, x-offset grows randomly and a chromatic ghost appears. Rotation increases as alpha drops.

**Animated bars (Scene 4)** — Bar width is `max_width * probability * clamp(t*3 - j*stagger)`, giving a left-to-right fill with per-bar stagger.

**Scanlines** — A horizontal line every 6px at 13% black opacity simulates a CRT monitor.

### Video stitching (`render.sh` / ffmpeg)

ffmpeg reads the PNG sequence and encodes to H.264:

```bash
ffmpeg -framerate 30 \
       -i frames/frame_%04d.png \
       -vf "fps=30,scale=1280:720,format=yuv420p" \
       -c:v libx264 -crf 17 \
       output.mp4
```

- `crf 17` — near-lossless quality (lower = better, 0 = lossless)
- `yuv420p` — required for broad player compatibility
- `scale=1280:720` — ensures height is divisible by 2 (H.264 requirement)

---

## 🎨 Customisation

### Change the name

Search `make_frames.py` for `saagar` and replace with your name. The greeting in Scene 1 and memory fragments in Scene 5 will update.

### Change resolution

Edit the config at the top of `make_frames.py`:
```python
W, H, DPI = 1280, 720, 96   # → e.g. 1920, 1080, 96 for 1080p
```

### Change framerate

```python
# In render.sh or your ffmpeg command:
-framerate 24   # cinematic
-framerate 60   # smooth
```

### Add/remove tokens (Scene 3)

Edit the `tokens` list in Scene 3. Mix languages freely — the blob physics handles placement automatically.

### Add scenes

Each scene is a `for i in range(N)` loop. Frame indices must be contiguous. Add your loop, start index = last scene's end + 1.

---

## 📦 Dependencies

| Package | Version | Why |
|---------|---------|-----|
| matplotlib | ≥ 3.7 | All rendering — figures, patches, text |
| numpy | ≥ 1.24 | Random number generation, trig arrays |
| ffmpeg | system | Frame → video encoding (not a pip package) |

---

## 💡 Prompt Engineering Note

This entire video was generated from a single conversation with Claude — describing scenes, style, and tone in plain English, with light Python scripting knowledge to guide the output structure. No video editing software was touched.

The prompt did the heavy lifting. The code was the output.

---

## 📄 License

MIT — use it, remix it, make your own LLM confessional.

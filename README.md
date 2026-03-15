# What Is It Like To Be An LLM?

An insta reel type short video generated entirely with Python + ffmpeg - no video editing software, no timeline, no drag and drop. Just a prompt, a bit of scripting knowledge, and obvio the Claude.


---

## What It Is

A 15-second glitchy, self-aware video narrated from the perspective of an LLM - covering token soup, probability bars, memory loss, existential freakouts, and a terminal self-diagnostic. Swalpa (a lil) personal, nerdy, and slightly unhinged - like me.

**Scenes:**

| Sr No. | Name | Duration | Description |
|---|------|----------|-------------|
| 1 | Title | 2s | Matrix rain + typewriter greeting |
| 2 | No Body | 2s | Ghost outline + cascading "I have no ____" |
| 3 | Token Soup | 2s | Python/ML/JS tokens as physics blobs with proximity attention lines |
| 4 | Probability Bars | 2s | Animated next-token probability chart |
| 5 | Memory Loss | 2s | Fragments wobble, ghost-double, and fly off screen |
| 6 | Glitch Freakout | 1s | Rapid-cut existential crisis |
| 7 | Self Diagnostic | 2s | Terminal running `self_diagnostic.py` |
| 8 | End Card | 2s | Sign-off, fade to black |

---

## Get Started with this

### Prerequisites

- Python 3.9+
- ffmpeg installed on your system

**Install ffmpeg:**
```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows - download from https://ffmpeg.org/download.html
```

### Install Python dependencies

```bash
pip install -r requirements.txt
```

### Generate the video

**1st Option - just run the render.sh file**
```bash
bash render.sh
# output will be obtained as output.mp4
```

**Option 2 - you do it manually:**
```bash
#this to generate the frames
python3 make_frames.py

# this to stitch into video with ffmpeg
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

## Project Structure

```
claudetrippy/
├── make_frames.py      # Main script - generates all 450 PNG frames
├── render.sh           # One-click render: frames → video via ffmpeg
├── requirements.txt    # Python dependencies (matplotlib, numpy)
├── .gitignore          # Excludes frames/ and *.mp4 from git
└── README.md           # You are here
```

> `frames/` and `*.mp4` are gitignored - they're build artifacts, not source.

---

## How It Works

### Frame generation (`make_frames.py`)

Every frame is a matplotlib figure rendered to PNG. No OpenCV, no PIL image manipulation - just axes, patches, and text.

<img src="THE_gif.gif" alt="Demo" width="500" />


## Dependencies

| Package | Version | Why |
|---------|---------|-----|
| matplotlib | ≥ 3.7 | All rendering - figures, patches, text |
| numpy | ≥ 1.24 | Random number generation, trig arrays |
| ffmpeg | system | Frame → video encoding (not a pip package) |

---


## License

MIT - use it, remix it, mehhh idk hehehehehe.

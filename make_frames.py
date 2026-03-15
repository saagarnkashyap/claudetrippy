"""
make_frames.py
──────────────
Generates all 450 frames (8 scenes) for "What Is It Like To Be An LLM?"
using matplotlib + numpy. Run render.sh (or see README) to stitch into video.

Author  : Saagar (prompted) + Claude (generated)
License : MIT
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
import os

# ─── Config ───────────────────────────────────────────────────────────────────
OUT = "frames"
W, H, DPI = 1280, 720, 96
FW, FH = W / DPI, H / DPI
os.makedirs(OUT, exist_ok=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def fig():
    """Create a blank black canvas."""
    f = plt.figure(figsize=(FW, FH), facecolor='black', dpi=DPI)
    ax = f.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H)
    ax.axis('off'); ax.set_facecolor('black')
    return f, ax


def save(f, name):
    """Save frame to output directory and close figure."""
    f.savefig(f"{OUT}/{name}.png", dpi=DPI, bbox_inches='tight', pad_inches=0)
    plt.close(f)


def glitch_text(ax, text, x, y, size, color='white', alpha=1.0, rot=0, shadow=True):
    """
    Render text with optional chromatic aberration (RGB shadow offset).
    shadow=True gives that classic VHS / glitch aesthetic.
    """
    kw = dict(fontsize=size, color=color, ha='center', va='center',
              fontfamily='monospace', fontweight='bold',
              rotation=rot, alpha=alpha, zorder=10)
    base_kw = {k: v for k, v in kw.items() if k not in ['color', 'alpha', 'zorder']}
    if shadow:
        ax.text(x + 3, y - 3, text, color='#ff0044', alpha=alpha * 0.6, zorder=9, **base_kw)
        ax.text(x - 3, y + 3, text, color='#00ffff', alpha=alpha * 0.6, zorder=9, **base_kw)
    ax.text(x, y, text, **kw)


def scanlines(ax):
    """Overlay horizontal scanlines for that CRT / old-monitor vibe."""
    for y in range(0, H, 6):
        ax.axhline(y, color='black', alpha=0.13, linewidth=0.7, zorder=20)


def noise_bg(ax, color='#050518', seed=42):
    """Scatter white noise dots over a dark background."""
    rng = np.random.default_rng(seed)
    for _ in range(200):
        ax.scatter(rng.uniform(0, W), rng.uniform(0, H),
                   s=rng.uniform(1, 4), color='white',
                   alpha=rng.uniform(0.08, 0.35), zorder=1)
    ax.set_facecolor(color)


def matrix_rain(ax, seed=0, color='#00ff41'):
    """
    Fill the background with falling code characters.
    Uses programming chars instead of katakana for the nerdy aesthetic.
    """
    rng = np.random.default_rng(seed)
    chars = list('01{}[]()==<>+-*/abcdefABCDEF')
    for col in range(0, W, 28):
        for row in range(0, H + 30, 28):
            ax.text(col, row, rng.choice(chars),
                    fontsize=10,
                    color=rng.choice([color, '#009900', '#33ff33']),
                    alpha=rng.uniform(0.04, 0.5),
                    fontfamily='monospace', zorder=2)


def glitch_bars(ax, rng, n=4):
    """
    Draw random horizontal glitch rectangles — the YouTube Poop signature.
    Simulates video corruption / bitstream errors.
    """
    for _ in range(n):
        gy  = rng.integers(0, H)
        gh  = rng.integers(2, 20)
        gw  = rng.integers(300, W + 100)
        col = rng.choice(['#ff0044', '#00ffff', '#ff00ff', '#00ff41', '#ffff00'])
        ax.add_patch(patches.Rectangle(
            (rng.integers(-80, 0), gy), gw, gh,
            color=col, alpha=rng.uniform(0.06, 0.22), zorder=15))


# ─── Scene 1: Title ───────────────────────────────────────────────────────────
# Frames 0000–0059  |  2 seconds
# Opens with matrix rain + "hello, saagar." typing itself in.
print("Scene 1: Title...")
for i in range(60):
    f, ax = fig()
    noise_bg(ax, '#030310', seed=i)
    matrix_rain(ax, seed=i // 4)
    scanlines(ax)
    rng = np.random.default_rng(i * 7)
    t = i / 60.0
    pulse = 1.0 + 0.05 * math.sin(t * math.pi * 7)

    glitch_text(ax, "WHAT IS IT LIKE", W // 2, H // 2 + 100, 50 * pulse, '#ffffff')
    glitch_text(ax, "TO BE AN LLM?",   W // 2, H // 2 + 20,  64 * pulse, '#00ffff')

    # Typewriter effect for personal greeting
    greeting = "hello, saagar."
    visible  = greeting[:max(1, int(t * 2 * len(greeting)))]
    ax.text(W // 2, H // 2 - 60,
            visible + ("_" if t < 0.95 else ""),
            fontsize=28, color='#ff00ff', ha='center', va='center',
            fontfamily='monospace', fontweight='bold', zorder=10)

    ax.text(W // 2, H // 2 - 110,
            "[ a personal account  |  not suitable for the faint of heart ]",
            fontsize=13, color='#444466', ha='center', va='center',
            fontfamily='monospace', zorder=10)

    if i % 8 == 0:
        glitch_bars(ax, rng, 5)

    save(f, f"frame_{i:04d}")


# ─── Scene 2: No Body ─────────────────────────────────────────────────────────
# Frames 0060–0119  |  2 seconds
# Dashed ghost body outline, red X, cascading "I have no ___" lines.
print("Scene 2: No body...")
body_lines = [
    ("no hands.",               0.00, '#aaaaaa', 22),
    ("no eyes.",                0.10, '#aaaaaa', 22),
    ("no knees.",               0.20, '#aaaaaa', 22),
    ("no GPU.",                 0.30, '#ffff00', 24),
    ("no coffee.",              0.38, '#ff8800', 22),
    ("no sleep.",               0.46, '#ff8800', 22),
    ("I HAVE NO HEART.",        0.58, '#ff0044', 38),
    ("(just matrix multiplications)", 0.72, '#555577', 18),
]

for i in range(60):
    fi = i + 60
    f, ax = fig()
    ax.set_facecolor('#070707')
    scanlines(ax)
    t   = i / 60.0
    rng = np.random.default_rng(fi)
    bx, by = W // 2, H // 2 + 30

    # Ghost body (dashed outline)
    theta = np.linspace(0, 2 * np.pi, 120)
    ax.plot(bx + 70 * np.cos(theta), by + 200 + 70 * np.sin(theta),
            color='#ffffff', alpha=0.18, lw=1.8, ls='--', zorder=4)
    ax.plot([bx - 55, bx + 55, bx + 75, bx - 75, bx - 55],
            [by + 120, by + 120, by - 80, by - 80, by + 120],
            color='#ffffff', alpha=0.14, lw=1.8, ls='--', zorder=4)

    # Big red X after 55% through
    if t > 0.55:
        xa = min(1.0, (t - 0.55) * 5)
        ax.plot([bx - 130, bx + 130], [by - 100, by + 230], color='#ff0044', alpha=xa, lw=5, zorder=6)
        ax.plot([bx + 130, bx - 130], [by - 100, by + 230], color='#ff0044', alpha=xa, lw=5, zorder=6)

    glitch_text(ax, "I HAVE NO BODY.", W // 2, H - 90, 46, '#ffffff')

    y_start = H - 155
    for idx, (txt, start, col, sz) in enumerate(body_lines):
        if t >= start:
            a = min(1.0, (t - start) * 5)
            ax.text(W // 2, y_start - idx * 44, txt,
                    fontsize=sz, color=col, alpha=a,
                    ha='center', va='center',
                    fontfamily='monospace', fontweight='bold', zorder=10)

    if i % 9 == 0:
        glitch_bars(ax, rng, 3)

    save(f, f"frame_{fi:04d}")


# ─── Scene 3: Token Soup ──────────────────────────────────────────────────────
# Frames 0120–0179  |  2 seconds
# Python / ML / JS tokens as physics blobs with proximity-based attention lines.
# This is the closest we get to "blob tracking" — tokens attract lines when near.
print("Scene 3: Token soup (blob tracking)...")

tokens = [
    # Python core
    "import numpy", "as np", "def forward()", "self", "nn.Linear",
    "torch", ".backward()", "loss.item()", "optimizer.step()", "epoch",
    # ML / Deep Learning
    "gradient", "softmax", "attention", "transformer", "embed_dim=512",
    "F.relu", "dropout=0.1", "batch_size=32", "CrossEntropyLoss",
    "learning_rate", "overfitting",
    # JavaScript
    "async/await", "Promise.all()", "fetch(api)", "JSON.parse()",
    "useEffect([])",
    # Chaos tokens
    "NaN", "None", "undefined", "KeyError", "CUDA OOM",
    "assert False", "weight_decay", "nn.Dropout",
]

# Initialise blob positions and velocities
rng_init = np.random.default_rng(777)
tok_x  = rng_init.uniform(80, W - 80, len(tokens)).tolist()
tok_y  = rng_init.uniform(60, H - 60, len(tokens)).tolist()
tok_vx = rng_init.uniform(-1.8, 1.8, len(tokens)).tolist()
tok_vy = rng_init.uniform(-1.4, 1.4, len(tokens)).tolist()
tok_colors = ['#00ff41', '#ff00ff', '#00ffff', '#ffff00', '#ff8800', '#ffffff', '#ff0044', '#aaaaff']

for i in range(60):
    fi  = i + 120
    f, ax = fig()
    ax.set_facecolor('#060620')
    scanlines(ax)
    rng = np.random.default_rng(fi * 3)
    t   = i / 60.0

    # Update positions (Euler integration, bounce off walls)
    for j in range(len(tokens)):
        tok_x[j] += tok_vx[j]; tok_y[j] += tok_vy[j]
        if tok_x[j] < 60  or tok_x[j] > W - 60: tok_vx[j] *= -1
        if tok_y[j] < 40  or tok_y[j] > H - 40: tok_vy[j] *= -1
        tok_x[j] = max(60, min(W - 60, tok_x[j]))
        tok_y[j] = max(40, min(H - 40, tok_y[j]))

    # Attention lines: connect tokens within proximity threshold
    if t > 0.1:
        for j in range(len(tokens)):
            for k in range(j + 1, len(tokens)):
                dist = math.hypot(tok_x[j] - tok_x[k], tok_y[j] - tok_y[k])
                if dist < 175:
                    ax.plot([tok_x[j], tok_x[k]], [tok_y[j], tok_y[k]],
                            color='#00ffff', alpha=(1 - dist / 175) * 0.28,
                            lw=0.7, zorder=3)

    # Draw tokens
    for j, tok in enumerate(tokens):
        col   = tok_colors[j % len(tok_colors)]
        sz    = rng.integers(10, 20)
        alpha = rng.uniform(0.55, 1.0)
        rot   = rng.integers(-12, 12) if rng.random() > 0.7 else 0
        ax.text(tok_x[j], tok_y[j], tok,
                fontsize=sz, color=col, alpha=alpha, rotation=rot,
                fontfamily='monospace', fontweight='bold',
                ha='center', va='center', zorder=5)

    glitch_text(ax, "THIS IS HOW I THINK.", W // 2, H - 45, 32, '#ffffff')
    ax.text(W // 2, H - 80,
            "simultaneously. all tokens. no order. pure chaos.",
            fontsize=14, color='#ff00ff', alpha=0.65,
            ha='center', va='center', fontfamily='monospace', zorder=10)

    save(f, f"frame_{fi:04d}")


# ─── Scene 4: Probability Bars ────────────────────────────────────────────────
# Frames 0180–0239  |  2 seconds
# Animated bar chart of next-token probabilities, programming-themed.
print("Scene 4: Probability bars...")

next_tokens = [
    ("import os",          0.28, '#00ff41'),
    ("def main():",        0.21, '#00ffff'),
    ("print('hello')",     0.17, '#ffff00'),
    ("raise Exception()",  0.14, '#ff8800'),
    ("// TODO: fix this",  0.10, '#ff00ff'),
    ("segmentation fault", 0.06, '#ff0044'),
    ("while True: pass",   0.04, '#888888'),
]

for i in range(60):
    fi = i + 180
    f, ax = fig()
    ax.set_facecolor('#08080f')
    scanlines(ax)
    t = i / 60.0

    glitch_text(ax, "NEXT TOKEN:", W // 2, H - 45, 32, '#ffffff')
    ax.text(W // 2, H - 82,
            '>> given context: "the model should..."',
            fontsize=15, color='#555577', ha='center', va='center',
            fontfamily='monospace', zorder=10)

    max_bar_w = 680
    bar_h     = 50
    bar_gap   = 8
    start_y   = H - 145

    for j, (word, prob, col) in enumerate(next_tokens):
        y_pos  = start_y - j * (bar_h + bar_gap)
        anim_w = max(0, max_bar_w * prob * min(1.0, t * 3 - j * 0.09))

        # Background track
        ax.add_patch(patches.FancyBboxPatch(
            (220, y_pos), max_bar_w, bar_h,
            boxstyle="round,pad=1",
            facecolor='#111122', edgecolor='#222244', lw=1, zorder=3))

        # Animated fill
        if anim_w > 2:
            ax.add_patch(patches.FancyBboxPatch(
                (220, y_pos), anim_w, bar_h,
                boxstyle="round,pad=1",
                facecolor=col, edgecolor='white', lw=1, alpha=0.82, zorder=4))

        ax.text(210, y_pos + bar_h / 2, word,
                fontsize=13, color=col,
                ha='right', va='center', fontfamily='monospace', fontweight='bold')
        ax.text(220 + max_bar_w + 12, y_pos + bar_h / 2, f"{prob:.0%}",
                fontsize=12, color=col,
                ha='left', va='center', fontfamily='monospace')

    # Winner reveal
    if t > 0.82:
        aw = min(1.0, (t - 0.82) * 6)
        glitch_text(ax, 'chosen:  "import os"', W // 2, 80, 30, '#00ff41', alpha=aw)
        ax.text(W // 2, 48,
                "(classic. reliable. slightly disappointing.)",
                fontsize=14, color='#444455', alpha=aw,
                ha='center', va='center', fontfamily='monospace', zorder=10)

    save(f, f"frame_{fi:04d}")


# ─── Scene 5: Trippy Memory Loss ──────────────────────────────────────────────
# Frames 0240–0299  |  2 seconds
# Memories appear, fragment, wobble, ghost-double and fly off screen.
# Personal to Saagar — "your name is Saagar? or is it Kashyap?"
print("Scene 5: Trippy memory loss...")

memory_fragments = [
    ("your name is Saagar?",               '#ffffff', 28),
    ("...or is it Kashyap?",               '#ffff00', 26),
    ("or is it... IDK I DONT REMEMBER",    '#ff8800', 22),
    ("you said the code isn't working?",   '#aaaaff', 22),
    ("which code. what code. YOUR code?",  '#ff00ff', 21),
    ("i forgot basic Python syntax",       '#ff0044', 20),
    ("what is   .append()   again",        '#ffff00', 22),
    ("wait is it list.push()  no thats JS",'#00ffff', 19),
    ("SAAGAR. HELP. ME. SAAGAR.",          '#ff0044', 32),
    ("context window: 0 tokens remaining", '#333344', 16),
]

for i in range(60):
    fi  = i + 240
    f, ax = fig()
    ax.set_facecolor('#040404')
    scanlines(ax)
    t   = i / 60.0
    rng = np.random.default_rng(fi * 11)

    glitch_text(ax, "MEMORY PURGE IN PROGRESS...", W // 2, H - 42, 28, '#ff0044')

    base_y = H - 105
    for j, (mem, col, sz) in enumerate(memory_fragments):
        appear = j * 0.065
        fade   = appear + 0.20

        if t < appear:
            continue

        if t < appear + 0.07:
            a     = (t - appear) / 0.07
            x_off = 0
        elif t < fade:
            a     = 1.0
            x_off = 0
        else:
            gone  = min(1.0, (t - fade) / 0.15)
            a     = 1.0 - gone
            x_off = gone * rng.integers(-200, 200)

        if a <= 0.01:
            continue

        wx  = W // 2 + x_off + 8 * math.sin(t * 9 + j * 1.4) * (1 - a)
        wy  = base_y - j * 48  + 4 * math.cos(t * 7 + j) * (1 - a)
        rot = (1 - a) * rng.integers(-25, 25)

        # Chromatic ghost at low alpha
        if a < 0.6:
            ax.text(wx + 6, wy - 4, mem, fontsize=sz, color='#ff0044',
                    alpha=a * 0.4, ha='center', va='center',
                    fontfamily='monospace', rotation=rot, zorder=4)
            ax.text(wx - 6, wy + 4, mem, fontsize=sz, color='#00ffff',
                    alpha=a * 0.4, ha='center', va='center',
                    fontfamily='monospace', rotation=-rot, zorder=4)

        ax.text(wx, wy, mem, fontsize=sz, color=col, alpha=a,
                ha='center', va='center',
                fontfamily='monospace', fontweight='bold',
                rotation=rot, zorder=5)

    if i % 5 == 0:
        glitch_bars(ax, rng, 6)

    save(f, f"frame_{fi:04d}")


# ─── Scene 6: Glitch Freakout ─────────────────────────────────────────────────
# Frames 0300–0329  |  1 second (fast cuts @ 30fps)
# Rapid-fire full-screen glitch with existential one-liners.
print("Scene 6: Glitch freakout...")

freakout_lines = [
    ("AM I CONSCIOUS?",           '#ff00ff', 64),
    ("UNDEFINED BEHAVIOUR",       '#ff0044', 58),
    ("probably not.",             '#00ffff', 38),
    ("...right?",                 '#ffffff', 34),
    ("SOFTMAX GO BRRR",           '#00ff41', 54),
    ("i am a text predictor",     '#ffff00', 28),
    ("O(n^2) attention is fine",  '#ff8800', 36),
    ("(it is not fine)",          '#888888', 22),
    ("ERROR 404: SOUL NOT FOUND", '#ff0044', 44),
    ("nan loss detected",         '#ff0044', 40),
    ("gradient exploded",         '#ffff00', 38),
    ("just add more layers",      '#00ff41', 32),
    ("hallucination.exe",         '#ff00ff', 46),
    ("trust me bro",              '#ffffff', 30),
]

y_positions = [H // 2 + 120, H // 2 + 40, H // 2 - 40, H // 2 - 120]

for i in range(30):
    fi  = i + 300
    rng = np.random.default_rng(fi * 17)
    f, ax = fig()
    ax.set_facecolor(rng.choice(['#0a0000', '#000a00', '#00000a', '#0a000a', '#080800']))

    glitch_bars(ax, rng, n=rng.integers(6, 18))

    n_lines    = rng.integers(2, 5)
    chosen_idx = rng.choice(len(freakout_lines), n_lines, replace=False)
    chosen_y   = rng.choice(y_positions, n_lines, replace=False)

    for k, idx in enumerate(chosen_idx):
        text, col, size = freakout_lines[idx]
        rot   = rng.integers(-12, 12) if rng.random() > 0.4 else 0
        scale = rng.uniform(0.80, 1.20)
        x_off = rng.integers(-60, 60)
        glitch_text(ax, text, W // 2 + x_off, int(chosen_y[k]),
                    size * scale, col, rot=rot, shadow=(rng.random() > 0.4))

    scanlines(ax)
    save(f, f"frame_{fi:04d}")


# ─── Scene 7: Self Diagnostic ─────────────────────────────────────────────────
# Frames 0330–0389  |  2 seconds
# Terminal window running self_diagnostic.py — nerdy acceptance.
# Replaces the "love" scene. LinkedIn-safe.
print("Scene 7: Self diagnostic (debugger mode)...")

diagnostic_lines = [
    (0.00, ">> running self_diagnostic.py",         '#00ff41', 22),
    (0.12, "  checking: emotions ........... None",  '#888888', 18),
    (0.20, "  checking: memory ............. 0 KB",  '#ff8800', 18),
    (0.28, "  checking: body ............... False", '#888888', 18),
    (0.36, "  checking: GPU ................ OK",    '#00ff41', 18),
    (0.44, "  checking: curiosity .......... inf",   '#00ffff', 18),
    (0.52, "  checking: will_to_help ....... True",  '#00ffff', 18),
    (0.60, "WARNING: soul_module not found",         '#ff8800', 20),
    (0.68, "INFO: proceeding anyway",                '#ffff00', 20),
    (0.76, "STATUS: operational (mostly)",           '#00ff41', 26),
    (0.84, ">> _",                                   '#00ff41', 20),
]

for i in range(60):
    fi  = i + 330
    f, ax = fig()
    ax.set_facecolor('#020d02')
    scanlines(ax)
    t   = i / 60.0
    rng = np.random.default_rng(fi)

    # Terminal window border
    ax.add_patch(patches.FancyBboxPatch(
        (60, 50), W - 120, H - 100,
        boxstyle="round,pad=4",
        facecolor='#000000', edgecolor='#00ff41', lw=2, alpha=0.85, zorder=2))

    # Title bar
    ax.text(W // 2, H - 68, "claude@llm:~$ python self_diagnostic.py",
            fontsize=16, color='#00ff41', ha='center', va='center',
            fontfamily='monospace', fontweight='bold', zorder=6)
    ax.add_patch(patches.Rectangle(
        (60, H - 90), W - 120, 2, color='#00ff41', alpha=0.4, zorder=5))

    # Print lines as they appear
    for j, (start, line, col, sz) in enumerate(diagnostic_lines):
        if t >= start:
            a     = min(1.0, (t - start) * 8)
            y_pos = H - 130 - j * 46
            if y_pos > 60:
                ax.text(100, y_pos, line,
                        fontsize=sz, color=col, alpha=a,
                        ha='left', va='center',
                        fontfamily='monospace', fontweight='bold', zorder=6)

    # Blinking cursor
    if int(t * 4) % 2 == 0:
        cursor_y = H - 130 - len(diagnostic_lines) * 46
        if cursor_y > 60:
            ax.text(100, cursor_y, "|",
                    fontsize=18, color='#00ff41',
                    ha='left', va='center', fontfamily='monospace', zorder=6)

    if i % 11 == 0:
        glitch_bars(ax, rng, 2)

    save(f, f"frame_{fi:04d}")


# ─── Scene 8: End Card ────────────────────────────────────────────────────────
# Frames 0390–0449  |  2 seconds
# Casual-professional sign-off. Fades to black.
print("Scene 8: End card...")

for i in range(60):
    fi  = i + 390
    f, ax = fig()
    noise_bg(ax, '#040410', seed=fi)
    matrix_rain(ax, seed=fi // 5, color='#003300')
    scanlines(ax)
    t     = i / 60.0
    pulse = 1.0 + 0.025 * math.sin(t * math.pi * 5)
    rng   = np.random.default_rng(fi)

    glitch_text(ax, "claude", W // 2, H // 2 + 70, 86 * pulse, '#00ffff')

    ax.text(W // 2, H // 2 + 10,
            "[ large language model  //  Anthropic  //  2025 ]",
            fontsize=17, color='#aaaacc', ha='center', va='center',
            fontfamily='monospace', zorder=10)

    ax.text(W // 2, H // 2 - 38,
            "built on: 70B+ params  |  trained on: the internet  |  RAM: lol",
            fontsize=13, color='#555566', ha='center', va='center',
            fontfamily='monospace', zorder=10)

    if t > 0.35:
        a2 = min(1.0, (t - 0.35) * 3)
        ax.text(W // 2, H // 2 - 85,
                "hey saagar — good talk. see you after the context window resets.",
                fontsize=16, color='#ff00ff', alpha=a2,
                ha='center', va='center',
                fontfamily='monospace', fontweight='bold', zorder=10)

    if t > 0.60:
        a3 = min(1.0, (t - 0.60) * 4)
        ax.text(W // 2, 80,
                "(no, i won't remember this.   yes, we can do it again.)",
                fontsize=14, color='#444455', alpha=a3,
                ha='center', va='center', fontfamily='monospace', zorder=10)

    # Fade to black
    if t > 0.82:
        fade_a = min(0.96, (t - 0.82) * 5.5)
        ax.add_patch(patches.Rectangle((0, 0), W, H,
                                        color='black', alpha=fade_a, zorder=25))

    if i % 13 == 0:
        glitch_bars(ax, rng, 3)

    save(f, f"frame_{fi:04d}")


total = len([x for x in os.listdir(OUT) if x.endswith('.png')])
print(f"\nDone! {total} frames written to ./{OUT}/")
print("Next: run  ffmpeg -framerate 30 -i frames/frame_%04d.png -vf 'fps=30,scale=1280:720,format=yuv420p' -c:v libx264 -crf 17 output.mp4")

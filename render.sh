#!/bin/bash
# render.sh — Generate frames + stitch video in one go.
# Usage: bash render.sh [output_name]

set -e

OUTPUT="${1:-output.mp4}"
FRAMES_DIR="frames"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " LLM Life Video Renderer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Step 1: Generate frames
echo ""
echo "▶  Step 1/2 — Generating frames..."
mkdir -p "$FRAMES_DIR"
python3 make_frames.py

FRAME_COUNT=$(ls "$FRAMES_DIR"/*.png 2>/dev/null | wc -l)
echo "   ✓ $FRAME_COUNT frames generated"

# Step 2: Stitch with ffmpeg
echo ""
echo "▶  Step 2/2 — Stitching video with ffmpeg..."
ffmpeg -y \
  -framerate 30 \
  -i "$FRAMES_DIR/frame_%04d.png" \
  -vf "fps=30,scale=1280:720,format=yuv420p" \
  -c:v libx264 \
  -crf 17 \
  -preset fast \
  "$OUTPUT" 2>&1 | grep -E "(frame=|kb/s|error|Error)" || true

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " ✓ Done! Output: $OUTPUT"
echo " Size: $(du -sh "$OUTPUT" | cut -f1)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

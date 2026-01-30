---
name: video-to-gif
description: Convert video files to GIF. Use when the user wants to convert a video to GIF format, especially for marketing emails or web use.
---

## Prerequisites

Requires ffmpeg. Install with Homebrew if not available:

```bash
which ffmpeg || brew install ffmpeg
```

## Converting Video to GIF

Use a two-pass approach with palette generation for optimal quality and file size:

```bash
ffmpeg -i input.mov -vf "fps=12,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif -y
```

### Parameters Explained

- `fps=12` - Frame rate (10-15 is good for email, reduces file size)
- `scale=600:-1` - Width in pixels, -1 maintains aspect ratio
- `flags=lanczos` - High-quality scaling algorithm
- `palettegen` / `paletteuse` - Generates optimized 256-color palette for better quality
- `-loop 0` - Loop forever (use `-loop 1` for single play)
- `-y` - Overwrite output file without asking

## Recommended Settings by Use Case

### Marketing Emails (Recommended defaults)
- Width: 600px (best email client compatibility)
- FPS: 10-12
- Target size: Under 1-2MB

```bash
ffmpeg -i input.mov -vf "fps=12,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif -y
```

### Social Media / Web
- Width: 800px
- FPS: 15

```bash
ffmpeg -i input.mov -vf "fps=15,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif -y
```

### High Quality (larger file)
- Original width or custom
- FPS: 20-24

```bash
ffmpeg -i input.mov -vf "fps=20,scale=1200:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif -y
```

## Checking Video Properties

Before conversion, check the source video dimensions and duration:

```bash
mdls -name kMDItemDurationSeconds -name kMDItemPixelWidth -name kMDItemPixelHeight input.mov
```

## Tips for Reducing File Size

1. Lower the frame rate (fps=10 instead of fps=15)
2. Reduce dimensions (scale=480:-1 instead of scale=600:-1)
3. Trim the video duration using `-ss` (start) and `-t` (duration):
   ```bash
   ffmpeg -i input.mov -ss 0 -t 3 -vf "fps=12,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 output.gif -y
   ```

## Video in Email Limitations

Native video in email has poor support:
- Gmail, Outlook, Yahoo strip `<video>` tags entirely
- Only Apple Mail and iOS mail support HTML5 video
- For broad compatibility, use GIF or a static thumbnail linking to hosted video

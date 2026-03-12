---
name: image-gen
description: Generate images using Nano Banana 2. Use when the user wants to generate illustrations or images in specific styles.
---

## Overview

Generate images using Nano Banana 2 (Gemini 3.1 Flash Image) via the Gemini API. The skill maintains a library of reference styles for consistent imagery.

## Environment

```bash
export $(cat ~/.claude/skills/image-gen/.env | xargs)
```

## Available Styles

| Style ID | Name | Description |
|----------|------|-------------|
| `playful-colorful` | Playful Colorful | Bright cartoon style with clean black outlines, saturated colors, friendly characters, flat coloring |
| `balsamiq` | Balsamiq Mockup | Hand-drawn wireframe style resembling Balsamiq — sketchy lines, simple shapes, Comic Sans-like font, grayscale with occasional blue highlights. **No reference image** — describe the style in the prompt instead. |

Reference images: `~/.claude/skills/image-gen/style-{style-id}.jpg` (not all styles have reference images)

**Important:** Only use a predefined style when the user explicitly asks for it. By default, generate images without a style reference — just use the prompt directly.

**Styles without reference images** (e.g. `balsamiq`): Use the "no style" API call but incorporate the style description directly into the prompt. For example: *"Hand-drawn wireframe mockup in Balsamiq style with sketchy lines, simple shapes, Comic Sans-like font, grayscale with occasional blue highlights. The mockup shows: {user's prompt}"*

## Generate Image (no style)

```bash
export $(cat ~/.claude/skills/image-gen/.env | xargs)

PROMPT="A person working on a laptop in a cozy coffee shop"
RATIO="16:9"  # Options: 1:1, 16:9, 9:16, 4:3, 3:2, 21:9, 1:4, 4:1, 1:8, 8:1
SIZE="2K"     # Options: 512, 1K, 2K, 4K

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"text": "'"$PROMPT"'"}
      ]
    }],
    "generationConfig": {
      "responseModalities": ["IMAGE", "TEXT"],
      "imageConfig": {
        "aspectRatio": "'"$RATIO"'",
        "imageSize": "'"$SIZE"'"
      },
      "thinkingConfig": {
        "thinkingLevel": "minimal",
        "includeThoughts": false
      }
    }
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > output.png
```

## Generate Image (with style)

Only use this when the user explicitly requests a specific style.

```bash
export $(cat ~/.claude/skills/image-gen/.env | xargs)

STYLE="playful-colorful"
PROMPT="A person working on a laptop in a cozy coffee shop"
RATIO="16:9"
SIZE="2K"

STYLE_IMAGE=$(base64 -i ~/.claude/skills/image-gen/style-$STYLE.jpg)

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"inlineData": {"mimeType": "image/jpeg", "data": "'"$STYLE_IMAGE"'"}},
        {"text": "Generate a new image in this exact visual style. '"$RATIO"' aspect ratio. The image should depict: '"$PROMPT"'"}
      ]
    }],
    "generationConfig": {
      "responseModalities": ["IMAGE", "TEXT"],
      "imageConfig": {
        "aspectRatio": "'"$RATIO"'",
        "imageSize": "'"$SIZE"'"
      },
      "thinkingConfig": {
        "thinkingLevel": "minimal",
        "includeThoughts": false
      }
    }
  }' | jq -r '.candidates[0].content.parts[] | select(.inlineData) | .inlineData.data' | base64 -d > output.png
```

## Aspect Ratios

- **1:1** - Square (social media, avatars)
- **16:9** - Widescreen (blog headers, presentations)
- **21:9** - Ultrawide (cinematic, banners)
- **9:16** - Portrait (stories, mobile)
- **4:3** - Standard (articles, thumbnails)
- **3:2** - Photo standard (marketing)
- **1:4** / **4:1** - Extreme vertical/horizontal
- **1:8** / **8:1** - Ultra-extreme vertical/horizontal

## Image Sizes

- **512** - Low res (thumbnails, previews)
- **1K** - Standard (web use)
- **2K** - High quality (default recommendation)
- **4K** - Maximum quality (print, large displays)

## Usage Tips

- Be specific about composition and elements
- Use `2K` as the default size for a good balance of quality and speed
- When using a style reference, keep prompts focused on subject matter — the reference image handles the style

## Adding New Styles

1. Save reference image: `~/.claude/skills/image-gen/style-{id}.jpg`
2. Resize: `sips -Z 800 style-{id}.jpg`
3. Add to the styles table above

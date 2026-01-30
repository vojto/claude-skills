---
name: ahrefs
description: Fetch keyword data from Ahrefs using Chrome browser automation. Use when the user needs keyword difficulty, search volume, or CPC data and API credits are exhausted.
---

## Overview

This skill uses Chrome browser automation to fetch keyword metrics from Ahrefs Keywords Explorer. It's a fallback for when API credits are exhausted.

**Requires:** User must be logged into Ahrefs in Chrome.

## Direct URL Access (Fastest Method)

Construct the URL directly to skip form navigation:

```
https://app.ahrefs.com/keywords-explorer/google/us/overview?keyword={URL_ENCODED_KEYWORD}
```

Examples:
- `meditation app` → `https://app.ahrefs.com/keywords-explorer/google/us/overview?keyword=meditation%20app`
- `best running shoes` → `https://app.ahrefs.com/keywords-explorer/google/us/overview?keyword=best%20running%20shoes`

URL encode spaces as `%20` and special characters appropriately.

## Extracting Metrics

After navigating to the keyword URL, use this JavaScript to extract metrics:

```javascript
const extractAhrefsMetrics = () => {
  const pageText = document.body.innerText;

  // Keyword Difficulty (0-100 score)
  const kdPattern = pageText.match(/Keyword Difficulty[\s\S]*?(\d{1,3})\s*(Super hard|Hard|Medium|Easy)/);
  const keywordDifficulty = kdPattern ? parseInt(kdPattern[1]) : null;
  const difficultyLabel = kdPattern ? kdPattern[2] : null;

  // Search Volume (US monthly)
  const svSection = pageText.match(/Search volume[^\d]*(\d+\.?\d*[KMB]?)/);
  const searchVolume = svSection ? svSection[1] : null;

  // CPC (Cost Per Click in USD)
  const cpcSection = pageText.match(/CPC\s*\$?([\d.]+)/);
  const cpc = cpcSection ? cpcSection[1] : null;

  // Traffic Potential
  const tpSection = pageText.match(/Traffic Potential[^\d]*(\d+\.?\d*[KMB]?)/);
  const trafficPotential = tpSection ? tpSection[1] : null;

  return {
    keywordDifficulty,
    difficultyLabel,
    searchVolume,
    cpc,
    trafficPotential
  };
};

extractAhrefsMetrics();
```

## Metrics Explained

| Metric | Description | Range/Format |
|--------|-------------|--------------|
| **Keyword Difficulty (KD)** | How hard it is to rank in top 10 | 0-100 (higher = harder) |
| **Difficulty Label** | Human-readable difficulty | Easy, Medium, Hard, Super hard |
| **Search Volume** | Monthly US searches | Number with K/M suffix |
| **CPC** | Cost per click for ads | USD amount |
| **Traffic Potential** | Estimated traffic if ranking #1 | Number with K/M suffix |

## Step-by-Step Manual Flow (Fallback)

If direct URL doesn't work:

1. Navigate to `https://app.ahrefs.com/keywords-explorer`
2. Click on the text input area (center of page)
3. Type the keyword(s)
4. Ensure "United States" is selected in the country dropdown
5. Click the orange "Search" button
6. Wait for results to load (2-3 seconds)
7. Extract metrics from the overview page

## Country Setting

This skill always uses **United States** (`us` in the URL path). The URL structure for other countries would be:
- `/google/us/` - United States
- `/google/gb/` - United Kingdom
- `/google/de/` - Germany

## Troubleshooting

- **Login required**: If redirected to login, user must authenticate in Chrome first
- **No data**: Some keywords may have insufficient data
- **Rate limiting**: Wait between requests if encountering issues

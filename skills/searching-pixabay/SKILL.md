---
name: searching-pixabay
description: Searches Pixabay for high-quality images and videos. Enforces strict resolution and file size limits for web performance.
---

# Searching Pixabay

This skill helps you find and process visual assets from Pixabay.

## Core Mandates

### 1. Resolution Discipline
- **Images**: Download `Large` (approx 1920px wide). Avoid original 4K/8K uploads.
- **Videos**: 
    - **Target**: `HD (1280x720)` or `FHD (1920x1080)`. 
    - **FORBIDDEN**: `4K`, `UHD`, `QHD`. These destroy git repo limits.

### 2. Processing Requirement (Videos)
Raw video files are **NEVER** allowed in the `inputs/` folder. You must process them immediately.
- **Trim**: Max **7 seconds**.
- **Audio**: Remove (mute).
- **Format**: `mp4` (H.264).
- **Script**: Run `python skills/searching-pixabay/scripts/process_video.py [input] [output]`.

### 3. File Size Limits
- **Background Video**: < 5 MB (Strict).
- **Images**: < 500 KB.

## Workflow

### Step 1: Search
Use `google_web_search` to find Pixabay assets if API is not available, or browse manually.
> "site:pixabay.com video beach waves"

### Step 2: Selection
Identify the download URL for the **1280x720 (720p)** version. 

### Step 3: Download & Process
1.  Download the raw file to a temporary location (e.g., `temp/raw_video.mp4`).
2.  **IMMEDIATELY** run the processor:
    ```bash
    python skills/searching-pixabay/scripts/process_video.py temp/raw_video.mp4 inputs/[Lesson]/images/final_video.mp4
    ```
3.  Delete the raw file.

### Step 4: Attribution
Create a `[filename]_attribution.txt` file next to the asset containing the Pixabay user and URL.
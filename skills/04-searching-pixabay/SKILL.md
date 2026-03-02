---
name: 04-searching-pixabay
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
- **Script**: Run `python skills/04-searching-pixabay/scripts/process_video.py [input] [output]`.

### 3. File Size Limits
- **Background Video**: < 5 MB (Strict).
- **Images**: < 500 KB.

## Workflow

### Step 1: Automated Download (Video)
Use the python script to search and download videos by query or ID.
```bash
python skills/04-searching-pixabay/scripts/download_video.py --query "search terms" --output "images/raw_video.mp4"
```

### Step 2: Mandatory Processing
**IMMEDIATELY** process the raw video to enforce size/duration limits (7s, Mute, 720p).
```bash
python skills/04-searching-pixabay/scripts/process_video.py "images/raw_video.mp4" "images/final_video_7s.mp4"
```
*Note: The script automatically deletes the raw file upon success.*

### Step 3: Deployment
- Move the final processed video to `inputs/[Lesson]/images/` (if < 1MB) or root `images/` (if > 1MB).
- Update `presentation.json` with the correct path.
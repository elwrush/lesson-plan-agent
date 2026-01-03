---
name: pushing-to-gdocs
description: >
  Uploads HTML content to Google Drive and converts it to a Google Doc. Use when
  the user wants to push materials to Google Docs or upload to Drive.
---

# Pushing to Google Docs

This skill details how to upload HTML content and convert it into a Google Doc in a specific Drive folder.

---

## Prerequisites

- `.credentials/GDocs-credentials.json` (Google API credentials)
- `.credentials/gdocs-token.json` (OAuth token with Drive + Docs scopes)
- Target Folder ID: `1_n11w9BRN6sd0uaXlqEXjqZuZ74zFiOl`

---

## Critical Constraints

Google Docs is a **paginated word processor**, not a browser. See [GDocs-HTML-Constraints.md](file:///c:/PROJECTS/LESSONS%20AND%20SLIDESHOWS%202/knowledge_base/GDocs-HTML-Constraints.md) for full details.

**What Google Docs IGNORES:**
- `float`, `box-shadow`, `border-radius`, `max-width`
- Class-based styles (`.class {}`)
- Local image paths (`../images/`)

**Design Philosophy — Avoid Excessive Tables:**
- Tables should be reserved for **truly tabular data** (lesson plans, behavior grids, comparison charts)
- For styling (colored boxes, emphasis), prefer **formatted text with inline styles**
- Headers can use single-cell tables for emphasis, but content should flow as paragraphs
- Use **tabs and lines** for spacing rather than table-based layouts

**Preferred Approach — Avoid Tables:**
- Use **formatted paragraphs** with inline styles for all content
- Use **circle icons (⭘)** with tabbed numbers for rating scales
- Use **borders only** (not background shading) for emphasis
- Place **images above text** and manually wrap in Google Docs
- Let content flow as natural paragraphs — easier to edit

**Legacy Workarounds (if needed):**
- 1-cell tables for colored boxes (use sparingly)
- 2-column tables for image insets (avoid if possible)

---

## Workflow

### Step 1: Prepare the HTML
Ensure the HTML follows [Converting to GDocs HTML](file:///c:/PROJECTS/LESSONS%20AND%20SLIDESHOWS%202/skills/converting-to-gdocs-html/SKILL.md) and the constraints above.

### Step 2: Run the Push Script
```powershell
python scripts/push_to_gdocs.py --file "inputs/folder/file.html" --name "DD-MM-YY-Topic-Skill-Program"
```

The script will:
1. Embed local images as base64 data URIs
2. Upload HTML to Drive with MIME type conversion
3. **Set page format: A4 with 2cm margins** (via Docs API)
4. Return the Google Doc URL (visible in task artifacts)

### Step 3: Manual Adjustments (if needed)
When reviewing the uploaded Google Doc, you may need to:
- **Image wrapping**: Click image → Wrap text
- **Paragraph spacing**: Format → Line & paragraph spacing → Remove spacing after paragraph

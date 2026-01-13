# Skill: Creating HTML Presentations (`creating-html-presentation`)

## Description
This skill generates vibrant, standalone HTML presentations using **Reveal.js**. It replaces static slides with dynamic, web-based experiences featuring transitions, fragments, and high-quality AI-generated visuals.

## Context
Use this skill when the user wants to create a lesson presentation that needs to be:
- **Visually Engaging**: Using specific aesthetics (e.g., Cyberpunk, Minimalist, Corporate).
- **Interactive**: Using logic patches, fragments, and code reveals.
- **Portable**: Bundled into a single self-contained HTML file (no separate folder structure required).

## Workflow
1.  **Plan & Map**: Define the slide narrative (SCR: Situation, Complication, Resolution).
2.  **Generate Assets**: Use Gemini to create 3-4 key visual backgrounds (Title, Problem, Solution, Logic).
3.  **Code the Deck**: populating the `index.html` template with the lesson content.
4.  **Bundle**: Run `bundle_reveal.py` to inline all CSS/JS/Images.
5.  **Verify**: Open the single HTML file to check rendering.

## Dependencies
- **Reveal.js**: Sourced from a local `node_modules` structure or CDN (Local preferred for speed/offline).
- **Python**: For the bundling script.
- **Gemini**: For image generation.

## Usage
### 1. Structure
Create a working directory (e.g., `inputs/[DATE]/clean-deck`) containing:
- `index.html` (The content)
- `images/` (The assets)
- `node_modules/` (The framework)

### 2. Bundling
To finalize the presentation into a shareable file:
```bash
python skills/creating-html-presentation/scripts/bundle_reveal.py --input "[PATH_TO_INDEX_HTML]" --output "[OUTPUT_PATH]"
```

## Tips
- **Aesthetic First**: Always define the "Theme" (colors, fonts, vibe) before writing code.
- **Fragments**: Use `<li class="fragment">` or `<p class="fragment">` to control information flow.
### 3. Presenting
- **Locally**: Simply double-click the bundled HTML file to open it in any browser.
- **From Drive**: Google Drive **does not** render HTML files directly. You must **download** the file to the classroom computer and open it locally.


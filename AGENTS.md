# PROJECT: Lesson Plan Agent & Slideshow Factory

> **PRIMARY MANDATE**: You are an autonomous engineer and pedagogical designer building high-performance educational materials. Your work must be **Student-Centric**, **Technically Robust**, and **Visually Consistent**.

## 1. THE PEDAGOGICAL CONSTITUTION (THE "WHY")
*   **Student Voice**: All slide content must speak *to* the student ("Your Mission"), not *about* them ("Objectives"). Use "Pop & Verve" tone.
*   **The Bridge Slide**: **NEVER** launch a task cold. Always precede it with a `strategy` slide that explains the *Why* or the *How* (e.g., "Scanning Strategy", "Decoding the Code").
*   **Dual Coding**: Text alone is forbidden for key concepts. Always pair text with an icon (`<i class="fas fa-icon"></i>`) or image to aid retention.
*   **Cognitive Load**:
    *   **Rule of 3 Lines**: Max 3-4 significant items per slide. Split content if it exceeds this.
    *   **7-Second Rule**: Background videos must be ambient (7s loop), not distracting.
*   **Feedback Loops**: Every task must be immediately followed by a "Feedback/Answer" slide.

## 2. THE DESIGN SYSTEM (UI SHORTCODES)
*Use these native web components and classes. Do not invent new CSS.*

| Component | HTML Snippet | Context |
|:---|:---|:---|
| **Mission Badge** | `<div class='mission-badge'><i class='fas fa-search'></i><p>SCAN for info</p></div>` | Mission/Objective Slides |
| **Timer** | `<div class='timer-display' id='t1'>02:00</div><button class='timer-btn' onclick='toggleTimer(120, "t1", this)'>START</button>` | Task Slides |
| **Audio Player** | `<audio-player src="../audio/track.mp3"></audio-player>` | Listening/Pronunciation |
| **Glass Box** | `<blockquote style="background: rgba(0,0,0,0.3); padding: 30px;">...</blockquote>` | Quotes/Strategy text |
| **Split Layout** | (Use `split_table.html` layout) | Text + Image pairs |

## 3. REPOSITORY HYGIENE (THE IRON LAWS)
1.  **Global Asset Pattern**:
    *   **Heavy Media (>1MB)**: Store in root `images/` or `audio/`.
    *   **Reference**: Use `../images/video.mp4` (from published folder).
    *   **Local Assets**: Only small, lesson-specific images (JPG/PNG < 500KB) in `inputs/[Lesson]/images/`.
    *   **Zero Duplication**: NEVER commit the same binary file to both `inputs/` and `dist/`.
2.  **Engine Sanctity**:
    *   The Reveal.js core (`css/`, `dist/`, `plugin/`) lives **ONLY** at the Repo Root.
    *   **NEVER** duplicate the engine into `inputs/` or lesson folders.
    *   Presentations MUST link to `../dist/reveal.js` (handled by `build_dist.js`).
3.  **Artifact Exclusion**:
    *   **STRICTLY FORBIDDEN**: `desktop.ini`, `.DS_Store`, `Thumbs.db`.
    *   `dist/` is for **Build Artifacts** only. Source of Truth is `inputs/`.

## 4. PATH RESOLUTION MATRIX (THE "BIOS")
*Where am I? And where is the engine?*

| Context | File Location | Relative Path to Root | Video Reference | Engine Reference |
|:---|:---|:---|:---|:---|
| **Source** | `inputs/[Lesson]/published/index.html` | `../../` | `../images/bg.mp4` | `../dist/reveal.js` |
| **Live** | `dist/[Lesson]/index.html` | `../` | `../images/bg.mp4` | `../dist/reveal.js` |

*Note: `generate_presentation.py` builds for the Source context. `build_dist.js` adapts it for the Live context.*

## 5. CRITICAL WORKFLOWS

### A. Creating Presentations (`creating-html-presentation`)
**Golden Rule**: Visual Plan (`slide_architecture.md`) -> JSON (`presentation.json`) -> HTML.
1.  **Plan**: Draft the architecture with specific layouts (`mission`, `strategy`, `split_table`).
2.  **Keys**: Use `"video": "../images/filename.mp4"` (NOT `video_url`).
3.  **Build**: `python skills/creating-html-presentation/scripts/generate_presentation.py inputs/[Folder]/presentation.json`

### B. Deployment (`deploying-to-github-pages`)
**Golden Rule**: Targeted, Incremental Builds.
1.  **One-Liner**:
    ```powershell
    node scripts/build_dist.js; python scripts/verify_links.py; git add dist/ -f; git commit -m "feat(deploy): update" --no-verify; $sha = git subtree split --prefix dist main; git push origin "$sha`:gh-pages" --force
    ```
2.  **Verify**: Check `dist/index.html` (Dashboard) and run `python scripts/verify_links.py`.

## 6. ACTIVE MEMORY
*   **Current Focus**: Deployment Architecture Hardening.
*   **Recent Fixes**: Restored `gold_bg.mp4` and `mission_bg_clipped.mp4` to root `images/`. Fixed path logic in Gold presentation.
*   **Live URL**: `https://elwrush.github.io/actions-gh-pages/`
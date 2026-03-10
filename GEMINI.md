# GEMINI.md - Lesson Plan Agent & Slideshow Factory

## Project Overview
This project is an **AI-powered Lesson Planning Assistant and Slideshow Factory** designed specifically for **Thai Middle School ESL learners** at the Bell Language Centre. It utilizes a **Skills-based Architecture** to ensure pedagogical accuracy, visual consistency, and technical robustness.

- **Core Technologies**
- **Logic & Automation:** Python 3.x
- **Presentations (HTML):** Reveal.js (HTML/JS/CSS)
- **Status:** PowerPoint (PPTX) is deprecated. Focus is on high-fidelity HTML.
- **Document Generation:** Typst (Worksheets only)
- **Serving:** GitHub Pages (Deployment)
- **Data Format:** Markdown-driven manifests (`presentation.md`)

## Building and Running

### Building
- **Build Target Lesson**: `python build.py [lesson-name]`
- **Validation**: Run `.gemini/hooks/present-validator.py`

## Critical Mandates & Conventions

### 1. The Skill Activation Gate (MANDATORY)
Before starting ANY task, identify the task type and read the corresponding skill file in `c:\PROJECTS\LESSONS AND SLIDESHOWS 2\skills\[skill-id]\SKILL.md`.
If working in a subfolder (like `SUMMER-CONVERSION`), reference skills via `../skills/` or absolute paths.
- `00-manage-git-workflow` (Source Repo Management)
- `00a-manage-gh-pages-workflow` (Live Deployment Management)
- `01-grabbing-youtube-transcripts`
- `02-writing-lesson-plans` (Enforces Shape & Pedagogical Density; single universal template: `modern_template_EP`)
- `03-producing-educational-materials` (Worksheets & PDFs)
- `04-searching-pixabay` (Mandatory for unique assets)
- `06-creating-html-presentation` (Standalone Bundle Engine)
- `07-generating-quizzes`
- `08-using-meander`
- `11-uploading-to-google-drive`
- `12-rendering-prompts-into-mermaid`
- `14-delegating-to-jules`
- `15-consulting-typst-repo` (MANDATORY for all .typ work)
- `16-consulting-global-repos` (GitHub API Fetcher - Authenticated via GITHUB_MCP_PAT)

## Custom Slash Commands
This project uses namespaced slash commands to directly trigger skill workflows. Use them followed by any necessary arguments (e.g., `/skill:02-plan Lesson-Title`).

| Command | Skill / Workflow |
| :--- | :--- |
| `/skill:00-git` | Manage Git Source (`00`) |
| `/skill:00a-deploy` | Deploy to GH Pages (`00a`) |
| `/skill:01-transcript` | YouTube Transcriptions (`01`) |
| `/skill:02-plan` | Initiate Lesson Planning (`02`) |
| `/skill:03-materials` | Produce Worksheets/PDFs (`03`) |
| `/skill:04-pixabay` | Search & Download Images (`04`) |
| `/skill:06-slides` | Create Reveal.js Slides (`06`) |
| `/skill:07-quiz` | Generate Quizzes (`07`) |
| `/skill:08-meander` | Meander Text-Wrapping (`08`) |
| `/skill:11-gdrive` | Upload to Google Drive (`11`) |
| `/skill:12-mermaid` | Render Mermaid Diagrams (`12`) |
| `/skill:14-jules` | Delegate to Jules (`14`) |
| `/skill:15-typst` | Consult Typst Repo (`15`) |
| `/skill:16-global` | Consult Global Repos (`16`) |
| `/skill:17-jinja` | Add Jinja Templates (`17`) |

### 2. Guardrails & Hooks
Automated validation is enforced via `.gemini/hooks/`:
- `folder_guard.py`: **CRITICAL**. Blocks creation of top-level folders in `inputs/`. Agents MUST work in the folder provided by the user.
- `instruction_integrity.py`: **MANDATORY**. Compares `SOURCE_TEXT.md` counts against `.typ` files to prevent task truncation.
- `lp_gatekeeper.py`: Blocks `.typ` generation until `SOURCE_TEXT.md` exists and blueprint is approved.
- `present-validator.py`: Enforces presentation JSON schema and verbatim alignment.
- `typst_guard.py`: Prevents forbidden Typst syntax and enforces worksheet standards (Badges, Mission, Q&A Integrity).

### 3. The 5-Phase Pipeline (Strict Chronology)
1.  **Phase 1: Ingestion**: Extract ALL content to `SOURCE_TEXT.md`. **MANDATORY**: Include `(Count: X)` tags for numbered items to prevent truncation.
2.  **Phase 2: Blueprint**: Create `lesson_plan_blueprint.md` itemizing every workbook task (e.g., Task 4, Task 5).
3.  **Phase 3: Typst Production**: Generate WS. **RULE**: LP generation is disabled; use worksheets only for summer conversion.
4.  **Phase 4: Visual Roadmap**: Create `visual_plan.md` mapping stages to Reveal.js layouts using the MVC schema.
5.  **Phase 5: Code Assembly**: Generate `presentation.md` and build bundle.

### 3. Repository Hygiene & The 'Published' Law
- **The Folder Continuity Law**: **STRICT**. You are FORBIDDEN from creating new top-level directories in `inputs/`. You MUST use the existing folder provided by the user.
- **The Native Presentation Law**: You act as "Presentation Director." Content is authored purely in Reveal.js native Markdown (`presentation.md`). The legacy JSON/Jinja pipeline is DEPRECATED. ALL teacher-facing instructions MUST go in the `notes` field.
- **The Truncation Law**: **ZERO TOLERANCE**. Every task, sentence, and exercise from `SOURCE_TEXT.md` MUST appear in the final materials.
- **The One Template Law**: ALL lesson plans use **one** universal template: `/templates/modern_template.typ`. There is no Bell vs Intensive branching. Import pattern:
    ```typst
    #import "/templates/modern_template.typ": modern_template, stage
    ```
    The following are **DELETED and LEGACY** — never use them:
    - `lesson-plan-components.typ`, `lesson_plan.typ`
    - `#lesson_header()`, `#metadata_table()`, `#stage_table()`
    - The local `/lib/` folder and `lib/typst/lib.typ`
- **Typst Layout Integrity** (Worksheets):
    - Q&A pairs MUST be wrapped in `#block(breakable: true/false, [...])`.
    - Writing tasks > 150 words require a mandatory second page of lines.

- **Typst/Presentation Consultation Law**: Never "guess" Typst or Reveal.js syntax. You MUST consult official repositories via **Skill 16** (`16-consulting-global-repos`) for all syntax, pedagogical templates (Bell/Intensive), and branding patterns. The local `/lib/` folder is deprecated and must not be used as a source of truth.
- **Self-Containment**: Every lesson in `inputs/[lesson-name]/published/` MUST be a standalone bundle including its own `dist/`, `plugin/`, and `fontawesome/` folders (automatically managed by the build system via GitHub acquisition).
- **The File Separation Law**: The source `.typ` files MUST remain in the root of the lesson folder. ONLY compiled `.pdf` files and the final presentation HTML/assets go into the `published/` folder.
- **Strict Naming Standard**: Lesson plans must be named `DD-MM-YYYY-[LEVEL]-[TITLE]-LP.typ` (and `.pdf`). Worksheets must be `DD-MM-YYYY-[LEVEL]-[TITLE]-WS.typ` (and `.pdf`).
- **URL-Friendly Naming**: Lesson folders MUST use lowercase alphanumeric characters and hyphens only (e.g., `28jan-listening-wb-p9`). **Spaces and underscores are FORBIDDEN**.
- **Root-Relative Imports**: All Typst files and presentation logic must use root-relative pathing (`/images/`, `/skills/`) to support project-level automation.
- **Worksheet Permission Gate**: DO NOT create worksheets automatically as part of the lesson planning phase. You MUST ask for explicit permission before initiating the `03-producing-educational-materials` skill.

### 4. Pedagogical & Visual Constitution
- **2026 Gold Standard Enforcements**:
    - **Mission First**: Slide 2 MUST be "YOUR MISSION" with `mission_bg_clipped.mp4` and 320px single-deck badges.
    - **Worksheet Mission**: MUST include a "YOUR MISSION" block with a specific Cambridge Exam hook (PET/First).
    - **Badge Law**: Worksheets MUST feature exactly three badges: CEFR Level, Skill, and Topic.
    - **Hero Image Mandate**: EVERY worksheet MUST have a hero image (Pixabay or User-supplied).
    - **Layout Integrity**: 
        - ID Blocks go *immediately* before the writing task, preceded by a page break.
        - NEVER put manual page breaks immediately after the main reading text.
        - Questions and Ruled Lines MUST be wrapped in non-breakable blocks.
        - Minimum 0.8cm vertical clearance for all handwritten response lines.
        - **Baseline Alignment Mandate**: All inline answer gaps (e.g., Task 2 grids) MUST use `#box(outset: (bottom: 2pt), baseline: 15%)[#hide[a]]` to ensure stroke alignment with text.
    - **No r-stretch Overlaps**: NEVER use the Reveal.js `r-stretch` class for image grids if they are followed by custom Web Components (like `<timer-pill>`). It causes layout collapse. Use standard flex containers with explicit heights instead.
    - **Audio Unlock Mandate**: Any custom web component triggering audio must "unlock" the audio context (silent play/pause) on the very first user interaction (click) to bypass browser autoplay restrictions.
    - **The 16:9 Aspect Ratio Law**: All presentations MUST use **1280x720** (16:9) resolution with a `margin: 0.05` to ensure consistent font scaling.
    - **The Pedagogical Font Matrix**: Standardized variables (`--ped-lead-in-size`, `--ped-body-size`) MUST be used to prevent font drift.
    - **The Stable Matching Law**: Use consistent `data-id` attributes for structural elements and sequential IDs for dynamic items to stabilize `auto-animate`.
    - **Segue-Bridge Law**: EVERY `segue` slide MUST be followed by a pedagogical bridge (`strategy`, `vocab`, `editing`, or a `PRODUCTION` task).
    - **The Timer Law (Work-Only)**: Timers are MANDATORY for active student work/discussion and FORBIDDEN for transitions, titles, and explanations.
    - **Timer Uniqueness Law**: Every timer component MUST use a unique ID derived from `slide_id` to prevent conflicts.
    - **Highlight Persistence Law**: When highlighting text (e.g. grammar choices), use the `.visible` CSS class (instead of `.current-fragment`) so the highlight persists after clicking.
    - **Matching Interaction**: Vocabulary or definition matching exercises MUST use the `match_reorder` layout.
    - **Minimalist Image Law**: On `schema_activation` slides, images MUST use a simple 1px gold border applied directly to the `img` tag. Do NOT use heavy container boxes.
    - **No Teacher Jargon**: BANNED: "Pre-teaching", "Lead-in", "Gist", "Practice". Use student-centric terms.
    - **Vocab Standard**: White context text, 1.1em size, gold (#FFD700) highlighting for the target word.
    - **Strategy Standard**: White titles (1.4em), balanced table font (0.95em), horizontal timer layout.
    - **Task 3 Consolidation**: ONE slide for all scan gaps, PNG images with direct 2px gold borders.
- **Immersive Audio Canvas**: Listening slides MUST NOT use foreground icons. Use thematic backgrounds (`background` field) only.
- **Real Person Image Law**: You MUST NOT search Pixabay for images of real people (celebrities, historical figures, etc.). You **MUST** ask the user to provide these images.
- **Zero Placeholder Tolerance**: Common placeholders (lion, bird, etc.) are blocked by programmatic hooks.
- **Answer Separation**: Strict **One-Answer-Per-Slide** enforcement (except for sequence tasks).
- **Dual Coding**: Use FontAwesome icons paired with key text.
- **Student-Centric Persona**: Use warm, encouraging ESL persona. Avoid teacher-facing jargon (Gist, Lead-in).

### 5. Security, Git & Technical Governance
- **Secret Protection**: `token.json`, `.env`, and `.credentials/` MUST be present in `.gitignore`.
- **Dual-Repo Workflow**: Use `00` for source code and `00a` for live deployments.
- **Banned Filenames**: Files named `nul`, `con`, `prn`, or other reserved OS names are strictly forbidden.
- **Markdown Presentation Integrity**: Presentation data MUST follow the Native Reveal.js Markdown Syntax.
    - Use `<!-- .slide: ... -->` for slide backgrounds and classes.
    - Use Web Components (`<slide-task>`, `<timer-pill>`) for layout logic.
- **Asset Discovery**: Use non-greedy regex for media collection to ensure filename precision.

## Key Files for Context
- `AGENTS.md`: The "Source of Truth" for persona and core mandates.
- `CRITICAL-MEMORY-RULES.md`: Essential rules to prevent regression.
- `/templates/modern_template.typ`: The **sole** lesson plan template. Contains the `stage()` helper.
- `build.py`: The core build script for aggregating presentations into `/dist`.

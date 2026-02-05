---
name: creating-html-presentation
description: Generates vibrant Reveal.js HTML presentations from materials and instructions. Handles design, animation, and strict content validation. Use when the user wants to generate a Reveal.js slideshow from lesson content or educational materials.
---

# Skill: Creating HTML Presentations (`creating-html-presentation`)

**Version**: 6.0 (Pedagogical Architecture + Layout Gap Analysis)

## Description
This skill generates high-energy Reveal.js presentations. It mandates a **Pedagogical Architecture** (Schema Activation -> Task) and operates on a **Local-First Architecture**. It strictly enforces content alignment and layout suitability.

## Core Mandates
1.  **Pedagogical Scaffolding**: **NEVER** present a task without a preceding "Bridge Slide" (Strategy/Context). Use the `strategy` layout to explain the "Why" before the "What".
2.  **Layout Gap Analysis**: If the content does not fit an existing layout (`REFERENCE.md`), you **MUST** ask the user to authorize designing a new template. Do not shoehorn complex content into simple lists.
3.  **Local-First Architecture**: **ABSOLUTELY NO CDNs** (except FontAwesome). All code comes from `temp_reveal_repo`.
4.  **Verbatim Fidelity**: Content in the slide JSON must match the `.typ` source 100%. No summarization.
5.  **Pedagogical UI**: Use **Dual Coding** (Icons + Text) and **Negative Feedback** animations (Red Strikethrough).
6.  **Phonemic Casing**: Phonemic script (text within slashes, e.g., /tɒm/) MUST NEVER use upper-case Latin letters (A-Z). Phonemes are always lower-case or specific IPA symbols.
7.  **Student-Centric Voice**: All visible slide content (titles, instructions, rationales) **MUST** be addressed directly to the student using an engaging, high-energy "Pop & Verve" tone (e.g., "YOUR MISSION", "THE CHALLENGE", "FINAL CHALLENGE"). **NEVER** use teacher-facing procedural language (e.g., "Objective", "Rationale", "Monitor") in student-visible areas. These belong exclusively in `<aside class="notes">`.
8.  **Repo Hygiene (Global Asset Pattern)**: To prevent repository bloat, **Heavy Media** (Videos > 1MB, Audio) **MUST** be stored in the project root `images/` folder and referenced via relative paths (e.g., `../../images/video.mp4`). **NEVER** duplicate heavy assets into the lesson's `dist/` folder. Small images (JPG/PNG) may remain local.

## Workflow

### Phase 0: 🧠 Discovery & Architecture
**Goal**: Define the "Master Blueprint" and validate Layout Fit.
1.  **Ingest Materials**: Read `.typ` files (Source of Truth).
2.  **Map Tasks**: Consult `REFERENCE.md` -> **Pedagogical Mapping Matrix**.
3.  **Layout Gap Check**:
    *   *Check*: Does every task map cleanly to a layout?
    *   *Action*: If NO, ask user: *"Task X requires a new layout. Shall I design one?"*
4.  **Draft Architecture**: Create `slide_architecture.md`. Define the layout for *every* slide, including mandatory **Bridge Slides**.

## Workflow

### Phase 0: 🧠 Visual & Pedagogical Architecture (MANDATORY)
**Goal**: Create a detailed blueprint and secure user approval.
1.  **Skeleton Mapping**: Map worksheet/book materials as the core skeleton.
2.  **Pedagogical Augmentation**: Overlay the Lesson Plan stages.
3.  **Human-Readable Detailing**: Create a Markdown file (`slide_architecture.md`) thatspecifies for every slide:
    - **Visual Vibe**: A clear, non-technical description of the image/video and layout.
    - **The Voice**: The exact student-centric headline and instructions.
    - **The Logic**: specify `auto-animate` transitions and `fragment` triggers.
    - **The Bridge**: specify how this slide links to the next pedagogical step.
4.  **Formatting**: Use bold headers, tables for lists, and clear bullet points. **NO BLOCK CODE** for the plan itself—it must be rendered Markdown.
5.  **STOP AND WAIT**: Present this Markdown plan to the user. **DO NOT** take any further action until it is explicitly approved.

### Phase 1: 📊 Pedagogical Mapping (Visualization)
**Goal**: Verify the Learning Journey.
1.  **Execute**: `skills/rendering-prompts-into-mermaid`.
2.  **Constraint**: Nodes must be labeled with `[Layout ID]`.
3.  **Verify Flow**: Check for **Bridge Node** -> **Task Node** -> **Feedback Node** pattern. If Bridge is missing, add it.

### Phase 2: 📦 Asset Strategy
**Goal**: Source and process high-quality visual assets.
1.  **Search & Selection**: Use the **[searching-pixabay](cci:7://file:///c:/PROJECTS/LESSONS%20AND%20SLIDESHOWS%202/skills/searching-pixabay/SKILL.md:0:0-0:0)** skill to find high-resolution images and videos.
2.  **Video Processing**: **MANDATORY**. All Pixabay videos MUST be processed using `python skills/searching-pixabay/scripts/process_video.py` to ensure they are trimmed (max 7s), muted, and scaled (720p).
3.  **Looping Mandate**: Ensure opening/background videos are set to `video_loop: true` in the slide configuration.
4.  **Local Storage**: Store all processed assets in the lesson's `images/` folder.

### Phase 3: 🎨 Config Generation (The Plan)
**Goal**: Create the JSON driver.
1.  **Constraint**: Use the **Approved Markdown Architecture** as the ONLY source for the JSON.
2.  **Gatekeeper Validation**:
    *   **CRITICAL STEP**: Run `scripts/validate_architecture_sync.py [json_path]`.
    *   **Action**: If fails, **STOP** and fix JSON.

### Phase 4: 🛠️ Build & Render
**Goal**: Generate the HTML using the Local Repo.
1.  **Execute**: `python skills/creating-html-presentation/scripts/generate_presentation.py [json_path]`.
2.  **Architecture**: The script generates a "clean" `index.html` and copies lesson-specific images/audio ONLY. 
3.  **Engine**: The Reveal.js engine is shared at the root of the library. Subfolder `index.html` files must use `../dist/` etc. (Handled automatically by `build_dist.js`).
4.  **Output**: `index.html` in the lesson's `published/` folder.

### Phase 5: 🧪 Final Validation
**Goal**: Ensure technical stability.
1.  **Run Suite**:
    *   `python skills/creating-html-presentation/scripts/validate_presentation.py` (Checks assets, CSS).
    *   `python skills/creating-html-presentation/scripts/validate_pedagogical.py` (Checks timer/answer logic).

## Scripts
*   `validate_content_alignment.py`: **[Critical]** Checks JSON against `.typ` source.
*   `generate_presentation.py`: Builds the HTML from JSON using **Local Repo**.
*   `validate_presentation.py`: Checks HTML structure and assets.

> **Tip**: See `REFERENCE.md` for the **Pedagogical Mapping Matrix**, code snippets, and layout documentation.

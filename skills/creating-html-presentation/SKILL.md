---
name: creating-html-presentation
description: Generates vibrant Reveal.js HTML presentations from materials and instructions. Handles design, animation, and strict content validation. Use when the user wants to generate a Reveal.js slideshow from lesson content or educational materials.
---

# Skill: Creating HTML Presentations (`creating-html-presentation`)

**Version**: 6.0 (Pedagogical Architecture + Layout Gap Analysis)

## Description
This skill generates high-energy Reveal.js presentations. It mandates a **Pedagogical Architecture** (Schema Activation -> Task) and operates on a **Local-First Architecture**. It strictly enforces content alignment and layout suitability.

## Core Mandates
1.  **Task Separation Mandate**: **NEVER** conflate multiple distinct tasks (e.g., Task B, C, and D) onto a single slide. Each task **MUST** have its own **Strategy Slide** (Bridge), its own **Task Slide**, and its own **Answer Detail Slide**. This ensures students have clear focus and proper feedback for every activity.
2.  **Title Slide Mandate**: The opening `title` slide **MUST** always include a `subtitle` field that displays the CEFR level and the core skill (e.g., "B1 Reading", "A2 Grammar"). This subtitle appears in yellow H2 styling under the main title.
3.  **Pedagogical Scaffolding**: **NEVER** present a task without a preceding "Bridge Slide" (Strategy/Context). Use the `strategy` layout to explain the **"What"** (Task) and the **"How"** (Pro Tips) before the "What". 
4.  **Strategy Table Mandate**: Content in `strategy` slides **MUST** be reformatted as a native HTML `<table>`. Use icons in the first column for every row (Task, Tips, Goals). This fixes vertical stacking issues and ensures a clean, professional look.
3.  **Phase-Based Segues**: Every phase of the lesson **MUST** be introduced with a `segue` slide that uses a **Phase Marker** (e.g., "PHASE 1") and a clear **Action Title** (e.g., "WORDS YOU'LL NEED" instead of "THE TOOLS").
    - **Segue Video Ban**: **NEVER** use video backgrounds on `segue` slides. Use plain, high-contrast backgrounds.
4.  **Vocab Pre-Teaching Mandate**: **NEVER** launch a reading or listening task without first pre-teaching the necessary vocabulary. Dedicated vocabulary slides (using `vocab` layout with images, phonemes, and context) **MUST** appear BEFORE the tasks they support.
5.  **External Image Prompts**: For historical figures or specific characters (e.g., Mary Shelley) unlikely to be found on stock sites, the agent **MUST** provide the user with high-quality image prompts for external generation.
6.  **Layout Gap Analysis**: If the content does not fit an existing layout (`REFERENCE.md`), you **MUST** ask the user to authorize designing a new template. Do not shoehorn complex content into simple lists.
5.  **Local-First Architecture**: **ABSOLUTELY NO CDNs** (except FontAwesome). All code comes from `temp_reveal_repo`.
6.  **Verbatim Fidelity**: Content in the slide JSON must match the `.typ` source 100%. No summarization.
7.  **Answer Detail Protocol**: Feedback slides **MUST** use the `answer_detail` layout. You **MUST** populate the specific fields: `answer`, `evidence`, and `explanation`. **NEVER** use a generic `content` table for these slides as it breaks the intended UI/UX pattern. Verbatim snippets from the text are mandatory for the `evidence` field.
15. **Mandatory Answer Population Hook**: Before finishing a presentation build, you MUST verify that every slide using the `answer_detail` layout contains non-placeholder values for `answer`, `evidence`, and `explanation`. Failure to populate these is a protocol violation.
8.  **ESL Pedagogical Voice**: Abandon "Mission" language (except on the specific Helicopter Mission Slide). Adopt a **Warm, Encouraging ESL Teacher Persona** suitable for **Thai Middle Schoolers**. Instructions must be simple, direct, and high-energy. **NEVER** use teacher-facing procedural language (e.g., "Lead-in", "Gist", "Objective", "Rationale", "The Tools", "The Crime") in student-visible areas.
9.  **Visual Sourcing**: **ALWAYS** use the `searching-pixabay` skill to source high-quality, relevant background images for vocabulary and key reading stages. Do not rely on generic placeholders.
10. **Table Styling**: All tables **MUST** be left-aligned (`text-align: left`) and use a font size of `1.2em`. 
11. **Vocab Transparency**: The background opacity for `vocab` card boxes **MUST** be set to `0.65` to balance image visibility and text legibility.
8.  **Repo Hygiene (Global Asset Pattern)**: To prevent repository bloat, **Heavy Media** (Videos > 1MB, Audio) **MUST** be stored in the project root `images/` folder and referenced via relative paths (e.g., `../../images/video.mp4`). **NEVER** duplicate heavy assets into the lesson's `dist/` folder. Small images (JPG/PNG) may remain local.
9.  **Header Integrity (No-Wrap Mandate)**: Vocabulary headers (Word + Phoneme) **MUST** remain on a single row. Use `white-space: nowrap` and `flex-wrap: nowrap` to prevent ugly line breaks on long words like "RADIATION".
10. **High-Impact Vocab Examples**: Vocabulary examples **MUST** be simple, easy to understand, and ideally non-topic-specific to aid general understanding. The target word in the example **MUST** be highlighted in gold using `<span style='color: #FFD700;'>`.

11. **Timer Table Mandate**: **NEVER** place timer boxes or their controls outside of a table. Every task slide requiring a timer MUST use a `<table>` layout, and the timer controls MUST be embedded as a row within that table (usually using `colspan`). The timer and its control buttons (START and RESET) **MUST** be horizontally stacked using the `.timer-container` wrapper. A "RESET" button is mandatory for every timer instance.
12. **Icon-Only Mandate**: **NEVER** use plain bullets (`<ul>`/`<li>`), carats (`>`), or generic chevron icons (e.g., `fa-chevron-right`) for lists or task items. You **MUST** use context-specific, descriptive FontAwesome icons (e.g., `fa-globe-americas`, `fa-star`, `fa-microchip`) to support the learning content via Dual Coding.
13. **Mandatory Mission Video**: Every slide with the `mission` layout **MUST** include the background video `../images/mission_bg_clipped.mp4` to maintain brand consistency.
14. **Table Styling Mandate**: All HTML tables `<table>` **MUST** explicitly set `font-size: 1.2em` and `text-align: left`. All text within table cells (`<td>`) **MUST** be left-aligned. **NEVER** use `text-align: center` for task text, numbers, or headers within a table. Every row/item **MUST** utilize a context-aware icon (Dual Coding).
16. **Answer Detail Typography**: To ensure clarity and prevent overflow, all text within the `answer_detail` layout (specifically the `answer` and `explanation` fields) **MUST** be set to a font size of `1.1em`. This is enforced at the template level but must be respected in any manual overrides.
17. **ESL Pedagogical Voice**: Abandon "Mission" language (except on the specific Helicopter Mission Slide). Adopt a **Warm, Encouraging ESL Teacher Persona** suitable for **Thai Middle Schoolers**. Instructions must be simple, direct, and high-energy.
18. **Smart Scripting Mandate**: Consult `knowledge_base/reveal_activity_matrix.md` to determine if **Auto-Animate** is required instead of single slides. Strict **One-Answer-Per-Slide** enforcement applies unless the matrix specifies otherwise (e.g., matching/choice tasks).
19. **Targeted Build Mandate**: **ALWAYS** use the targeted build argument (e.g., `python build.py [lesson-name]`) when editing a single lesson. This prevents unnecessary full-project rebuilds and maintains development velocity.
20. **Server Verification**: Before providing a preview link, you **MUST** verify the Caddy server is listening on port 8000 (e.g., via `netstat` or a silent check). If the connection is refused, restart the server immediately via `run_server.bat`.

## Workflow

### Phase 1: Ingestion (The Source Gate)
**Goal**: strict verbatim extraction of source content.
1.  **Content Checklist**: Create `inputs/[Lesson]/content_checklist.md` using the template.
2.  **Verbatim Check**: Extract ALL text verbatim from the source (PDF/Typst).
3.  **Gate**: User must verify checklist matches source 100%.

### Phase 2: Lesson Planning (The Lesson Plan Gate)
**Goal**: Define the pedagogical structure before visuals.
1.  **Typst Lesson Plan**: Write `lesson_plan.typ`.
2.  **Structure**: Define Strategy -> Task -> Answer sequences.
3.  **Gate**: User must approve the lesson flow.

### Phase 3: Visual Mapping (The Visual Gate)
**Goal**: Map content to slides and assets.
1.  **Visual Plan**: Create `inputs/[Lesson]/visual_plan.md`.
    *   Map each stage to a layout (consult `knowledge_base/reveal_activity_matrix.md`).
    *   Write Image Prompts for every visual.
2.  **Asset Acquisition**:
    *   **User Provided**: Place in `inputs/[Lesson]/images/`.
    *   **Stock Fallback**: Use `searching-pixabay` skill.
    *   **Video Processing**: Process all videos to 7s loops.
3.  **Gate**: User must approve visuals and layouts.

### Phase 4: Code Assembly (The Build Gate)
**Goal**: Generate the presentation.
1.  **JSON Creation**: Write `inputs/[Lesson]/presentation.json` based *strictly* on the Visual Plan.
2.  **Asset Hygiene**: Ensure all heavy media is in root `images/`.
3.  **Generation**: Run `python skills/creating-html-presentation/scripts/generate_presentation.py ...`
4.  **Validation**: Run `.gemini/hooks/present-validator.py`.
    *   Checks: Content Alignment, Sequence, Pedagogical Rules.
5.  **Gate**: Zero validation errors.

## 🛡️ Troubleshooting & Prevention

### 🌐 The "Connection Refused" Bug
If the user reports "Site can't be reached" or "127.0.0.1 refused to connect":
1. **Verification**: Run `netstat -ano | findstr :8000`. If empty, the server is down.
2. **FIX**: Run `Start-Process "run_server.bat"` immediately to launch the visible Caddy window.
3. **Log Check**: Check the Caddy terminal window for port conflicts or syntax errors.

### 🏷️ The "Missing Subtitle" Violation
If the title slide lacks the yellow CEFR/Skill text:
**FIX**: Ensure `presentation.json` has a `"subtitle": "B2 Reading"` (or similar) field in the first slide.

## Scripts
*   `validate_content_alignment.py`: **[Critical]** Checks JSON against `.typ` source.
*   `generate_presentation.py`: Builds the HTML from JSON using **Local Repo**.
*   `validate_presentation.py`: Checks HTML structure and assets.

> **Tip**: See `REFERENCE.md` for the **Pedagogical Mapping Matrix**, code snippets, and layout documentation.

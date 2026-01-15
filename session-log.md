
---

## 2026-01-14 | Presentation Physics Overhaul & Visual Workflow

### Key Technical Achievement: "Fixed Canvas Logic"
- **Problem**: Fluid/Responsive layouts (`height: 100%`) caused content to overflow or disappear on large screens ("Webpage Logic").
- **Solution**: Adopted **Fixed Artboard Logic** (960x700px).
  - Explicit pixel heights for rows (`500px`).
  - Strict `max-height: 400px` for all media.
  - Floating "Cyber Pill" header (`absolute`, `z-index: 10`) to remove layout impact.
  - **Result**: Perfect deployment on Cloudflare (Desktop & Mobile).

### Workflow Pivot: The "Visual First" Standard
- **Change**: Moved from "Code-First" (writing HTML directly) to a **5-Step Gated Workflow**.
  1.  **Theme Selection**: Dynamic choice (Cyber, Noir, Minimal).
  2.  **Visual Plan (Markdown)**: Descriptive planning of visuals with pedagogical intent.
  3.  **User Approval**: Explicit "Stop & Check."
  4.  **Wireframe**: Canvas logic mapping (Mermaid).
  5.  **Implementation**: Copying the Gold Standard `REFERENCE_TEMPLATE.html`.

### Pedagogical Upgrades
- **Source Sync**: Slides must strictly match Worksheet task names (e.g., "TASK 2").
- **Answer Keys**: Enforced "Single Answer Interleaving" (One answer per slide, immediately following question, with 'Why' explanation).
- **Voice**: "Pop & Verve" tone mandated (e.g., "YOUR MISSION" instead of "Task").
- **Infographics**: Prioritized **Generative AI** for "Pop" visuals; restricted Mermaid to technical data.

### Feature Addition: TTS Vocabulary Audio
- **Requirement**: "Direct Vocabulary" slides must include audio pronunciation context.
- **Engine**: **Gemini 2.5 Pro Preview TTS**.
- **Implementation**:
  - Script: `skills/creating-html-presentation/scripts/generate_vocab_audio.py`
  - Output: `.wav` files in `images/audio/`
  - UI: Stylized "Cyber" audio player with "Listen!" label.

### Skill Upgrade
- **`creating-html-presentation`**: Fully rewritten to version 2.3.
- **Reference**: `REFERENCE_TEMPLATE.html` created and updated with new CSS (`.audio-player`).

---

## 2026-01-15 | Worksheet Graphics & Layout Refinement

### Visual Upgrade: "Transparent Layouts" & "Defined Motifs"
- **Goal**: Move away from blocky, whitespace-heavy images to integrated layouts.
- **Action**:
  -   **Trimming**: Implemented `trim_image.py` to auto-crop whitespace from generated assets.
  -   **Transparency**: Enforced transparent PNGs for all non-rectangular motifs.
  -   **Separators**: Standardized on "Wide Trimmed" motifs (e.g., EKG line) for section breaks.

### Usability: "The Handwriting Standard"
- **Problem**: Previous templates ignored physical space needed for handwriting.
- **Solution**:
  -   **Writing Tasks**: Dedicated page, Grouped Prompts, 10 Double-Spaced Lines (Dark Gray).
  -   **Definitions**: `Word: ____________` layout (Auto + 1fr Line) with 1.5cm spacing.
  -   **Matching**: Minimum 1cm gap between items.

### Layout: "Booklet Safety"
- **Constraint**: Printing on A3 folded (Booklet).
- **Rule**: Content must never split across the "Page 4 -> 5" boundary (Sheet transition).
- **Implementation**: Strict manual page breaks enforced at these boundaries to keep Tasks self-contained on a physical sheet.

### Skill Update
-   **`developing-bespoke-materials`**: Updated with strict rules for Pagination, Image Quality, and Handwriting Spacing.
-   **`processing-images`**: Created new skill for image hygiene.

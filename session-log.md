
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

# Error Fix Log - March 2026

## Core Presentation Architecture (v16.0)
- **The "Local Lib" Delusion**: Assuming the `/lib/` folder contains current truth leads to using broken/obsolete templates (e.g., legacy `lesson_header()`).
  - **Fix**: **MANDATORY SKILL 16**. Consult the official repositories (`reveal/revealjs.com`, `typst/typst`) for ALL syntax and pedagogical patterns. The local `/lib/` is deprecated.
- **"Director" Parser Sensitivity**: My initial `manifest_parser.py` was too strict with colons, breaking on directives like `[HIGHLIGHT: text]`.
  - **Fix**: Implemented a **RegEx Identifier Validation** in the parser. A line is only treated as a slide key if it's a valid variable name (e.g., `layout:`, `timer:`). If it has brackets or spaces, it's treated as content.
- **Pandoc Slide Break Failure**: Pandoc crashed because it didn't recognize `# SLIDE X` as a break.
  - **Fix**: The `presentation_fixer.py` now acts as a **Technical Normalizer**. it generates a temporary `pptx_source.md` where `# SLIDE` headers are converted to standard `---` separators. This preserves the "Director" readability while satisfying the Pandoc compiler.
- **Unicode Resilience Mandate**: On Windows, all build/validation scripts MUST use plain ASCII for console output (OR ensure stdout is wrapped in `io.TextIOWrapper` with `encoding='utf-8'`). Prefer `[OK]`, `[FAIL]`, `[WARN]` over emojis to prevent `UnicodeEncodeError`.
- **Centralized Pathing (V2)**: The `PresentationConfig` class in `skills/06-creating-html-presentation/scripts/presentation_config.py` is now the SOLE source of truth for build paths. Scripts must NOT manually concatenate `inputs/` or `published/` strings.
- **Manifest Normalization**: The `presentation_fixer.py` hook handles the `presentation.md` -> internal JSON conversion. Validators and Generators should rely on the internal JSON produced by the fixer.
- **Cloud Purge**: Wrangler, Cloudflare, and Google Docs references are officially legacy and have been removed from the pipeline.

### FIXED (10-03-2026 SESSION)
- [x] **Phase 17.0 Breakthrough (Pure Reveal.js)**: The legacy Python/Jinja/JSON "baking" pipeline was completely decommissioned. The architecture now uses **Native Reveal.js Markdown Loading** with inlined content.
- [x] **Pure Markdown Law**: Discovered that wrapping text in HTML block tags (e.g., `<p>`, `<div>`) disables the Reveal.js Markdown parser for those lines, breaking bold (`**`) and italics (`*`).
  - **Fix**: **MANDATE**: Use pure Markdown for all text content and apply styling via Reveal.js **Element Attributes**: `<!-- .element: class="..." -->`.
- [x] **CORS Security Bypass**: Fixed the "Black Screen" issue when opening files locally by inlining `presentation.md` directly into the `index.html` shell during the build process.
- [x] **Automatic Cinematic Overlays**: Replaced manual `<div>` overlays with a CSS pseudo-element class (`.cinematic`). This ensures background videos play correctly without being blocked by foreground HTML elements.
- [x] **Standardized Separators**: Standardized on `---` for slide breaks and `Note:` for speaker notes, ensuring the Markdown plugin correctly identifies slide boundaries and hides teacher-facing instructions.
- [x] **PPTX Deprecation**: Officially decommissioned PowerPoint generation. Removed Pandoc calls from `generate_presentation.py` and excised `.pptx` logic from the Fixer and Config.
- [x] **Skill 16 Repository Purge**: Successfully purged the redundant `hakimel/reveal.js` mapping. All Reveal.js consultations and clones MUST use `reveal/revealjs.com`.
- [x] **Validator Refactor (V17)**: Updated `.gemini/hooks/present-validator.py` to validate Native Markdown syntax and call the new `build_native.py` bundler.
- [x] **r-stretch Overlap Bug**: The Reveal.js `r-stretch` helper class caused layout collapsing and overlap when followed by custom Web Components (like `<timer-pill>`).
  - **Fix**: Replaced `r-stretch` with standard flex layouts and explicit heights (e.g., `height: 350px`) for image grids in `presentation.md`.
- [x] **Timer Audio Blocked (Autoplay Policy)**: Audio on `<timer-pill>` failed to play at milestones because the browser blocked async audio playback triggered by a `setInterval` detached from a user click.
  - **Fix**: Implemented an "audio unlock" mechanism in `slide-components.js`. On the very first click of the Start button, the `AudioFX` initializes and forces a silent `.play()` and immediate `.pause()` for ALL available sound effects, satisfying the browser's interaction requirement.
- [x] **Stage Badge Stretching**: In the native flex layout, `.stage-badge` elements were stretching to 100% width, creating an unwanted yellow bar across the slide.
  - **Fix**: Updated `pedagogy.css` to set `.stage-badge` to `display: inline-block` and `width: fit-content`.
- [x] **Legacy Wrapper Interference**: Legacy `impact-content` and `impact-layout` `div` wrappers were causing height calculation errors and violating the "Pure Markdown Law".
  - **Fix**: Purged all manual `div` wrappers from `presentation.md`, allowing Reveal.js to manage the layout flow natively.
- [x] **Video Loop Stalling**: Background videos occasionally stalled on the final frame instead of looping.
  - **Fix**: Standardized on explicit boolean attributes (`data-background-video-loop="true"`) instead of standalone flags.


## Media & Asset Management
- **The 4K Video Trap**: Downloading "Original" videos from Pixabay destroys Git limits.
  - **Fix**: Auto-trim to **7 seconds** and scale to **720p** before adding to the project.
- **The Windows Console Trap**: Emojis in `print()` statements cause `UnicodeEncodeError` on Windows (cp1252). **MANDATE**: Use ASCII-only tags for logging (e.g., `[OK]`, `[FAIL]`, `[WARN]`). No emoji icons in scripts.
- **Path Centralization**: Hardcoded relative paths lead to "File Drift." **MANDATE**: All scripts (Fixer, Generator, Validators) MUST import and use `PresentationConfig` for all path resolutions.
- **Director Format (MD-First)**: Moving from JSON to Markdown created parsing friction. **MANDATE**: Use `presentation_fixer.py` as the normalization gate. Do not manually edit `presentation.json`.

## Typst Production
- **The Lobotomy Trap (Dynamic Lines)**: Manual line counting in Typst is fragile.
  - **Fix**: Use `#v(1fr)` followed by a `#stack()` of lines. This is the **breakthrough pattern** for filling space. Never use manual math for page filling.

---
*Note: This log is now maintained for current Architectural Truths (v16.0). Legacy entries from Jan/Feb 2026 have been purged to prevent knowledge drift.*

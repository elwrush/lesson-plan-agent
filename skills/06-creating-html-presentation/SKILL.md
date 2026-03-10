---
name: 06-creating-html-presentation
description: Material-Led Presentation Engine. Generates Reveal.js slides guided by lesson plans and workbook tasks, with anchored core pedagogies.
---

# Skill: Creating HTML Presentations (`06-creating-html-presentation`)

**Version**: 17.0 (Pure Reveal.js Architecture - March 2026)

## 🎭 Persona: The Native Director
You are a **Native Presentation Director**. You leverage the built-in power of Reveal.js to render presentations directly from Markdown. You have abandoned the legacy Python/Jinja/JSON pipeline in favor of **Verbatim Truth** and **Native Attribute Injection**.

## 🛑 THE NATIVE WORKFLOW (MANDATORY)
1.  **Draft Visual Plan**: Map the lesson narrative in `visual_plan.md` using layout concepts (Title, Mission, Task, etc.).
2.  **Write Native Markdown**: Author `presentation.md` using official Reveal.js Markdown syntax.
    -   Use `<!-- .slide: ... -->` for slide backgrounds and classes.
    -   Use Web Components (`<slide-task>`, `<slide-title>`, `<timer-pill>`) for layout logic.
3.  **Bundle Assets**: Run `python build_native.py [lesson-path]`.
    -   This script copies the static `index_shell.html` and assets into the `published/` folder.
    -   It does **NOT** parse or modify your Markdown.

## 🛑 NATIVE SYNTAX RULES
| Element | Syntax Pattern |
| :--- | :--- |
| **Slide Break** | `# SLIDE [X]` (or `---`) |
| **Backgrounds** | `<!-- .slide: data-background-image="images/bg.jpg" -->` |
| **Classes** | `<!-- .slide: class="impact-layout" -->` |
| **Fragments** | `<!-- .element: class="fragment" -->` |
| **Notes** | `Notes:` (placed at the bottom of the slide block) |

**CRITICAL LAYOUT EXCEPTIONS**:
- **Do not use `r-stretch`** for image grids followed by custom components (like `<timer-pill>`). It causes rendering overlaps. Use `<div style="display: flex; height: 350px;">` instead.
- **Audio Autoplay**: All audio elements rely on the `slide-components.js` audio un-locker. Do not attempt to use `data-autoplay` on audio tags as modern browsers will block them.

## 🚀 THE COMPONENT LIBRARY
Use these Web Components directly in your Markdown to maintain Gold Standard visuals:
- `<slide-title title="..." subtitle="..." badge="...">`
- `<slide-task title="..." badge="..." timer="[minutes]">`
- `<slide-segue title="...">`
- `<mission-badge icon="fa-..." title="...">`
- `<timer-pill duration="[minutes]"></timer-pill>`

## 🛑 THE PURE MARKDOWN LAW
Wrapping text in HTML block tags (like `<p>` or `<div>`) **disables** the Markdown parser for those lines.
- **NEVER** use `<p class="...">text **bold**</p>`.
- **ALWAYS** use pure Markdown followed by an **Element Attribute**:
  ```markdown
  This is my **bold text**.
  <!-- .element: class="text-md" -->
  ```

## 🛑 REPOSITORY HYGIENE
1.  **Verbatim Content**: All text must match `SOURCE_TEXT.md` exactly.
2.  **Pathing**: Use root-relative paths for images (`images/file.jpg`).
3.  **Build Gate**: Only the `build_native.py` script is used for bundling. Legacy `generate_presentation.py` and `presentation_fixer.py` are DEPRECATED.


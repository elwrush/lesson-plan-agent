---
name: 06-creating-html-presentation
description: Generates vibrant Reveal.js HTML presentations from materials and instructions. Handles design, animation, and strict content validation. Use when the user wants to generate a Reveal.js slideshow from lesson content or educational materials.
---

# Skill: Creating HTML Presentations (`06-creating-html-presentation`)

**Version**: 10.0 (Production Gold Standard - March 2026)

## Description
This skill generates high-energy Reveal.js presentations using a **Legacy Manual HTML/CSS Template System** (Jinja2). It mandates a strict **Pedagogical Architecture** and operates on a **Local-First Asset Architecture**.

## Core Mandates

### 1. The Production Standard
-   **Legacy Templates Only**: Use the manual HTML/CSS templates in `/templates/`. **BANNED**: Do not use experimental Web Components (e.g., `<slide-title>`).
-   **Local Assets**: ALL lesson images and videos MUST be stored in the lesson's local `images/` directory. Root images are for shared branding only.
-   **Reveal.js Consultation**: Consult the official Reveal.js repository via Skill 16 (alias `revealjs`) for all syntax and configuration.

### 2. Pedagogical Flow & Language
-   **Mission First**: Slide 2 MUST be the "YOUR MISSION" slide.
-   **The Segue-Bridge Law**: EVERY `segue` slide MUST be followed by a pedagogical bridge (`strategy` or `vocab`). Never jump from a segue straight into a task.
-   **Student-Centric Voice**: BANNED teacher jargon: "Pre-teaching", "Lead-in", "Gist", "Controlled Practice", "Stage". Use: "Word Power", "Quick Scan", "The Challenge".

### 3. Slide Architecture
-   **Mission Slide**: 
    -   Title: Exactly "YOUR MISSION".
    -   Video: Exactly `images/mission_bg_clipped.mp4`.
    -   Badges: Single deck of text (merged title/desc). Width: **320px**.
-   **Task 3 (Summary Scan)**:
    -   Consolidate all scan items into ONE slide.
    -   Images: Use PNGs with a direct **2px gold border** (`#FFD700`). No extra boxed containers.
-   **Answer Detail**:
    -   Numerals: Use numbers (1., 2.) instead of question mark icons in the left column.
    -   Width: Containers MUST be **1200px** wide to prevent text wrapping.
    -   One-Answer-Per-Slide: Every question gets its own slide.
-   **Timer UI**: Controls (START/RESET) MUST be **horizontally next to** the timer display.

### 4. Visual Styling & Typography
-   **Vocabulary**: 
    -   Text: White context sentences (`color: white`) at **1.1em**.
    -   Highlighting: Target word MUST use Gold (`<span style='color: #FFD700;'>word</span>`).
-   **Strategies**: 
    -   Titles: White (`color: white !important`) at **1.4em**.
    -   Tables: Balanced text at **0.95em** with fixed **60px** icon columns.

## Workflow
1. Ingestion (`SOURCE_TEXT.md`).
2. Blueprint (`lesson_plan_blueprint.md`).
3. Visual Map (`visual_plan.md`).
4. Asset Sourcing (`04-searching-pixabay`). Move assets to local `images/`.
5. Assembly (`presentation.json`).
6. Validation (`.gemini/hooks/present-validator.py`).
7. Build (`python scripts/fast_edit.py`).

## Validation Scripts
* `validate_gold_standard.py`: Enforces visual/architectural rules.
* `validate_pedagogical.py`: Enforces interleaving and source alignment.

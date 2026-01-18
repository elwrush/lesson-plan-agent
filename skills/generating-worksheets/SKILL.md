---
name: generating-worksheets
description: >
  Generates professional, branded PDF worksheets using Typst.
  Use when the user requests worksheet creation, especially for grammar or skill-based activities.
---

# Generating Worksheets Skill

## Description
Generates high-quality, print-ready PDF worksheets using **Typst**, offering superior layout control, precise pagination, and "printer-safe" margins.

## Prerequisites
- **Typst CLI** must be installed and accessible in the terminal.
- **Branding Assets** must be present in `/images/`:
  - Bell: `ACT_transparent.png`, `Bell.svg`
  - Intensive: `intensive-header.jpg`

- **If Intensive**: Use `images/intensive-header.jpg` as the header image. 
  - **CRITICAL**: **NEVER** use the maroon strap or the `integrated_header()` function.
  - **PRINTER SAFETY**: The header image MUST be **center-aligned** and have at least **0.5cm of top padding** from the edge of the sheet (do not use `dy: -1.5cm`).
  - **Action**: Use the `intensive_header()` function and ensure it uses `align(center)` and reasonable vertical spacing.

## Reference Material
- **Bell Template**: `knowledge_base/templates/grammar_repair_worksheet_gold.typ`
- **Intensive Template**: `skills/generating-worksheets/templates/intensive_worksheet_template.typ`

## Workflow

1. **Source the Template**:
   - Copy the gold standard template from `knowledge_base/templates/grammar_repair_worksheet_gold.typ`.
   - Save it to `skills/generating-worksheets/templates/[new_worksheet_name].typ`.

2. **Select Header**:
   - **Bell**: Use `#integrated_header()` with maroon strap and logos.
   - **Intensive**: Use `#intensive_header()` which displays `intensive-header.jpg`.
   - **Diagnostic Section (Page 1)**: Customize the "Repair Targets" or introductory activity.
   - **Tasks (Pages 2-4)**: 
     - Update the `task_card` function calls with specific prompts, contexts, and constraints.
     - **Constraint**: Maintain the **15-line limit** for writing areas to ensure zero spillover.
     - **Pagination**: Keep strict `#pagebreak()` calls between levels (A2/B1/B2).
     - **Orphan Prevention**: **CRITICAL**. Wrap every Task header and its instructions in a block with `breakable: false` (e.g., `#block(breakable: false)[ #text(...) [...] ]`). Never let a header sit alone at the bottom of a page.

3. **Compile PDF**:
   - Compiling follows a strict naming convention: `DD-MM-YYYY-[CEFR LEVEL]-[DESCRIPTION].pdf`.
   - Run the Typst initialization command from the project root:
   ```powershell
   typst compile "skills/generating-worksheets/templates/[template].typ" "inputs/[Folder]/DD-MM-YYYY-[CEFR_LEVEL]-[DESCRIPTION].pdf" --root "."
   ```
   - *Example: `11-01-2026-A2-B2-Grammar-Repair-Shop.pdf`*

4. **🧪 Validate (MANDATORY)**:
   Run the validator before finalizing:
   ```powershell
   python skills/generating-worksheets/scripts/validate_worksheet.py "path/to/worksheet.typ" --mode [bell|intensive]
   ```
   - **Rule**: If the script fails, fix the issues and re-run until it passes.
   - **Checks**: Branding, writing line limits (max 15), image paths, pagebreaks.

5. **🚦 Visual Verify**:
   - Check for **printer safety**: Are headers inside the margins?
   - Check for **logo visibility**: Are the SVG/PNG logos rendering correctly?
   - Check for **line contrast**: Are ruled lines **dark gray** (#4D4D4D)? NEVER use light gray.
   - Check for **spillover**: Does every page fit perfectly without content bleeding to the next?
   - Check for **warnings**: Did the Typst compiler throw any "no text within stars" warnings? 
     - **Fix**: Use `#strong[]` instead of `**` and `#emph[]` instead of `*` for nested or punctuation-adjacent text.

6. **🏁 THE LINK GATE (MANDATORY)**:
   > [!CRITICAL]
   > **YOU MUST PROVIDE A CLICKABLE LINK TO THE PDF.**
   > 
   > **Action**: Post the link using the `file:///` protocol so the user can open it in the IDE.
   > 
   > **Example**: [My Worksheet](file:///path/to/worksheet.pdf)
   > 
   > **DO NOT** proceed to any follow-up tasks (like lesson planning or pushing to Drive) until this link is provided and the user has seen it.

## Template Structure
The Typst template uses a functional component approach:
- `#integrated_header()`: **BELL ONLY**. The maroon strap with logos and title.
- `#intensive_header()`: **INTENSIVE ONLY**. Full-width branding image (`intensive-header.jpg`). Do NOT add text or straps over this.
- `#task_card()`: Boxed prompt with level and context.
- `#radar_box()`: Self-correction checklist.
- `#writing_lines(count: 15)`: Fixed-height writing area.

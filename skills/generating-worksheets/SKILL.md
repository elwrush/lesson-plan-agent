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

## Step 0: Context Check (MANDATORY)
**Ask**: "Is this a **Bell** or **Intensive** worksheet?"
- **If Bell**: Use the maroon strap header with ACT/Bell logos.
- **If Intensive**: Use `images/intensive-header.jpg` as the full-width header image.

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
   - Check for **spillover**: Does every page fit perfectly without content bleeding to the next?

## Template Structure
The Typst template uses a functional component approach:
- `#integrated_header()`: The maroon strap with logos and title.
- `#task_card()`: Boxed prompt with level and context.
- `#radar_box()`: Self-correction checklist.
- `#writing_lines(count: 15)`: Fixed-height writing area.

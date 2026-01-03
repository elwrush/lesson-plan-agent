---
name: generating-worksheets
description: >
  Generates branded, print-ready PDF worksheets (Intensive or Bell styles) from a master HTML template.
  Use when the user requests worksheet creation, PDF generation for lesson materials, or mentions printable worksheets.
---

# Generating Worksheets Skill

## Description
Generates branded, print-ready PDF worksheets ("Intensive" or "Bell" styles) from a master HTML template. Use when the user requests worksheet creation or PDF generation for lesson materials.

## Setup
Ensure dependencies are installed:
```bash
pip install jinja2 playwright
npx playwright install chromium
```

## Usage
Use the builder script to render the template and generate a PDF. PDFs will automatically appear as artifacts for the user to review.

**IMPORTANT: Always provide the file link to the generated PDF after completion.**

### Command Line
```bash
python skills/generating-worksheets/scripts/build_worksheet.py --brand <brand> --content <content-file> --output <path>
```

### Arguments
- `--brand`: `intensive` (default) or `bell`. Determines the header style.
- `--content`: Path to HTML content fragment file to inject into the template.
- `--output`: Path to save the final PDF.
- `--header-title`: (Bell brand only) Main header text - appears BELOW the "Bell Language Centre" strap line. **Do NOT include "Bell Language Centre" in this parameter.**
- `--quote`: (Optional) Subheader quote with compass icon. If omitted, quote section will not appear and padding will be added automatically.

### Bell Brand Header Structure
The Bell header has two lines:
1. **Top strap (hardcoded)**: "Bell Language Centre" (small, uppercase)
2. **Main header (--header-title)**: Your custom text (large, uppercase)

**Example:**
```bash
# ✅ CORRECT - only specify the topic/title
--header-title "Useful Language for Presentations"

# ❌ WRONG - don't include "Bell Language Centre" 
--header-title "Bell Language Centre|Useful Language for Presentations"
```

### Complete Example
```bash
python skills/generating-worksheets/scripts/build_worksheet.py \
  --brand bell \
  --content "inputs/02-Useful Language/useful-language-content.html" \
  --output "inputs/02-Useful Language/worksheet.pdf" \
  --header-title "Useful Language for Presentations"
```

## Workflow
1. Create content HTML file with your material sections
2. Run build script with appropriate parameters
3. **Provide the PDF file link to the user for review**
4. Make any necessary adjustments based on feedback

## Architecture
- **Template:** `templates/worksheet-master.html` (Jinja2 with logical switches).
- **Builder:** `scripts/build_worksheet.py` (Orchestrates rendering + PDF conversion).
- **PDF Engine:** `scripts/pdf_converter.js` (Playwright wrapper).

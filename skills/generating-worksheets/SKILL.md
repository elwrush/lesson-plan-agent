---
name: generating-worksheets
description: >
  Generates branded, print-ready PDF worksheets (Intensive or Bell styles) from a master HTML template.
  Use when the user requests worksheet creation, PDF generation for lesson materials, or mentions printable worksheets.
---

# Generating Worksheets Skill

## Description
Generates branded, print-ready PDF worksheets ("Intensive" or "Bell" styles) from a master HTML template using **WeasyPrint** for reliable paged-media CSS support.

## Setup
```bash
pip install jinja2 weasyprint
```

## Usage

### Command Line
```bash
python skills/generating-worksheets/scripts/build_worksheet.py --brand <brand> --content <content-file> --output <path>
```

### Arguments
- `--brand`: `intensive` (default) or `bell`. Determines the header style.
- `--content`: Path to HTML content fragment file to inject into the template.
- `--output`: Path to save the final PDF.
- `--header-title`: (Bell brand only) Main header text - appears BELOW the "Bell Language Centre" strap line. **Do NOT include "Bell Language Centre" in this parameter.**
- `--quote`: (Optional) Subheader quote with compass icon. If omitted, quote section will not appear.
- `--debug`: Keep temporary HTML file for inspection.

### Example
```bash
python skills/generating-worksheets/scripts/build_worksheet.py \
  --brand bell \
  --content "inputs/02-Useful Language/useful-language-content.html" \
  --output "inputs/02-Useful Language/worksheet.pdf" \
  --header-title "Useful Language for Presentations"
```

---

## Workflow (GATED)

> [!IMPORTANT]
> **Step 2 validates, Step 4 is a USER GATE.** You MUST validate AND get user approval before publishing.

1. **Create Content HTML**: Write your material sections using the content fragment format.

2. **🔍 RUN VALIDATOR**: Check content HTML for compliance
   ```bash
   python skills/generating-worksheets/scripts/validate_worksheet.py <content.html>
   ```
   - **Checks performed**:
     - ❌ Single-column text (no 2-column CSS)
     - ❌ Page break before Answer Key
     - ⚠️ Orphan prevention CSS present
     - ❌ No duplicate headers in fragment
   - **Fix ALL errors** before proceeding

3. **Generate PDF**: Run `build_worksheet.py` with appropriate parameters.

4. **🚦 USER REVIEW GATE**: Open the generated PDF locally and **wait for user feedback**.
   - Use `Start-Process <path-to-pdf>` to open the file.
   - If user requests changes, edit HTML and go back to step 2.
   - **DO NOT proceed to Step 5 until user explicitly approves.**

5. **Publish to Google Drive**: Only after approval, run the publishing script.


---

## Layout Best Practices (Orphan/Whitespace Prevention)

Include these CSS rules in content fragments to prevent layout issues:

```css
/* Prevent orphaned table headers */
table { break-inside: auto; }
tr { break-inside: avoid; break-after: auto; }
thead { display: table-header-group; }

/* Keep titles with their content */
h1, h2, h3 { break-after: avoid; }
p { orphans: 2; widows: 2; }

/* Explicit page breaks */
.page-break { page-break-before: always; break-before: page; display: block; }
```

### When to Use Manual Page Breaks
- **ALWAYS**: Before the Answer Key.
- **RECOMMENDED**: Before major activity shifts (e.g., "Task: Use your Hero Tool").
- **AVOID**: Mid-paragraph or mid-table (rely on CSS `break-inside: avoid` instead).

---

## Architecture
- **Template:** `templates/worksheet-master.html` (Jinja2 with logical switches).
- **Builder:** `scripts/build_worksheet.py` (Orchestrates rendering + WeasyPrint PDF conversion).

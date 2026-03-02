---
name: 15-consulting-typst-repo
description: >
  Hybrid Typst Reference System for consulting the official public Typst GitHub repository
  to understand syntax and formatting, avoiding hallucinations.
---

# Skill: Consulting Typst Repo (`15-consulting-typst-repo`)

## Description
This skill implements the "Public Reference + Local Branding" hybrid model for Typst report generation. It ensures that AI agents always use the most current Typst syntax directly from the official repository while adhering to local branding standards.

## Core Mandates
1. **No Guessing**: You MUST consult the Typst public repository for syntax rather than guessing or using web searches.
2. **Local Branding**: All project-specific components reside in `lib/typst/lib.typ`. You MUST use local definitions for branding (e.g., headers, badges) rather than redefining them.
3. **Avoid Deprecated Patterns**: Do not use legacy strings like `bell_header` or `#h(1fr)` if there are modern alternatives. 

## The Workflow

### Step 1: Consult Local Branding
First, read the local component library to ensure you understand the local branding.
```powershell
# Use your read_file tool to check:
lib/typst/lib.typ
```
After doing this, update `.gemini/tmp/typst_last_consulted.json` with the current Unix timestamp:
```json
{ "timestamp": 1718000000.0 }
```

### Step 2: Consult Public Typst Syntax
Never use Google search for Typst documentation. Use the `web_fetch` tool to fetch the relevant source from the official repo.

*   **Browse Structure**: `https://api.github.com/repos/typst/typst/contents/crates/typst-library/src`
*   **Read Source (e.g. lists/enums)**: `https://raw.githubusercontent.com/typst/typst/main/crates/typst-library/src/layout/list.rs` or `enum.rs`.

After doing this, update `.gemini/tmp/typst_github_last_consulted.json` with the current Unix timestamp.

### Step 3: Implement & Validate
When modifying a `.typ` file:
1. Ensure the mandatory import `#import "/lib/typst/lib.typ": *` (or the specific local library in use) is present.
2. Apply changes utilizing your newly acquired, up-to-date syntax.
3. Run the Typst compiler to ensure no regressions occur.

**Note**: There is a pre-tool hook (`.gemini/hooks/typst_guard.py`) that enforces these rules. If you haven't consulted the repo recently, your edits to `.typ` files will be blocked.
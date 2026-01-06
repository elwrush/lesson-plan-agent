---
name: developing-bespoke-materials
description: >
  Creates custom educational materials tailored to CEFR levels and skill types. Use when
  the user wants to design worksheets, transform textbook content, or develop new teaching materials.
---

# Developing Bespoke Materials

## Purpose
Guide the creation of custom educational materials tailored to specific CEFR levels, skills, and program types. Supports both transforming existing materials and developing brand new content.

---

## Workflow

### Step 1: Initial Consultation
Gather requirements BEFORE generating any content:
- **CEFR Level**: A1, A2, B1, B2, C1, or C2
- **Skill/System**: Reading, Listening, Writing, Speaking, Grammar, Vocabulary, or Pronunciation
- **Duration**: Ask "How long is this lesson?" (e.g., 46 minutes, 50 minutes, 90 minutes)

### Step 2: Material Source
Ask the user:
> Are you mainly wishing to **transform existing materials** or **write brand new materials**?

### Step 3: Program Type
Ask the user:
> Are you creating these materials for **regular classes** (Bell) or the **Intensive program**?

### Step 4: Development Phase

#### General Principles
1.  **Header Images**:
    -   **Regular/Bell**: ALWAYS use `../images/bell-header.jpg`.
    -   **Intensive**: ALWAYS use `../images/intensive-header.jpg`.
    -   *Do not* attempt to generate custom headers unless explicitly requested AND the standard headers are unsuitable.
2.  **Image Generation**:
    -   Use `generate_image` sparingly.
    -   **Fallback**: If generation fails (e.g., 429 errors), immediately pivot to high-quality CSS design (colors, emojis, clear typography) or use existing assets. Do not loop retries.
3.  **Lesson Planning**:
    -   **NEVER** create the lesson plan before the worksheet/material is finalized and approved by the user.
    -   **Sequence**: Design Material → User Review → User Approval → Create Lesson Plan.

#### If Transforming Existing Materials:
1. Suggest using **Gemini 3 Flash's multimodal image capabilities** to read source materials
2. Ask user to provide images/scans of the source materials
3. Extract and analyze the content
4. Work in dialog with the user to adapt and transform the materials

#### If Writing Brand New Materials:
1. Discuss the topic, context, and learning objectives with the user
2. Determine required content types:
   - 📖 Reading texts
   - 🎧 Audio scripts (for listening)
   - 🖼️ Images (use `generate_image` tool ONLY for content illustrations, not layout elements)
3. Collaborate iteratively to develop the content

### Step 5: Draft & Approval
1. Develop all materials in **Markdown format** first for content clarity, OR directly in HTML if the design is complex.
2. **Do NOT use the browser tool to automatically review the file.**
3. Instead, run a command to open the file in the user's default browser window:
   ```python
   # Windows
   import os
   os.startfile("path/to/file.html")
   ```
4. **Wait for explicit approval** before proceeding to any next steps (like Lesson Plans).

### Step 6: Export & Format

> ⚠️ **MANDATORY FORMAT RULE**
> - **Materials (worksheets, handouts)** → Export as **PDF** using the `generating-worksheets` skill.
> - **Lesson Plans** → Export as **HTML** and push to **Google Docs** using the `pushing-to-gdocs` skill.

#### For Materials (PDF Output)
1. Create content HTML in `inputs/[Topic]/` as a content fragment.
2. Use the `generating-worksheets` skill to render the final PDF with Bell/Intensive branding.
3. Open the PDF locally for user validation before publishing.

#### For Lesson Plans (GDocs Output)
- **File Location**: Save the final HTML in `inputs/[Topic]/`.
- **Styling**:
    -   **Colored Boxes**: ALWAYS use **single-cell tables** (`<table><tr><td style="background: ..."> ... </td></tr></table>`) for rule boxes, examples, or exercise containers. `<div>` background colors are often stripped by Google Docs.
    -   **No Horizontal Rules**: Do not use `<hr>` tags. Use spacing or border-bottom on headers if separation is needed.
    -   **GDocs Compatibility**:
        -   **ZERO MARGINS**: Always set `p, h1, h2, ul { margin: 0; padding: 0; }` in CSS to override Google Docs defaults. Add controlled bottom margin (e.g., `margin-bottom: 8pt`) only where needed.
        -   **Compact Headers**: Set `margin-bottom: 0` and `padding-bottom: 0` for H1 and H2 to avoid large white gaps.
        -   Use `pt` units (e.g., `11pt`) instead of `px`.
        -   Use inline styles for everything important.
        -   Avoid `flexbox` and `grid`.
    -   **Colors**: Use high-contrast colors (e.g., Bell Maroon `#A62D26`, Deep Blue `#2196F3`).

---

## Conversation Starters

Use one of these to begin the workflow:

```
Hello! I'm here to help you create bespoke educational materials.

To get started, please tell me:
1. What **CEFR level** are you targeting? (A1, A2, B1, B2, C1, C2)
2. What **skill or system** do you want to focus on? (Reading, Listening, Writing, Speaking, Grammar, Vocabulary, Pronunciation)
```

---

## Quality Standards

### Content Requirements
- Age-appropriate and culturally sensitive
- Aligned with CEFR descriptors for the target level
- Clear instructions and rubrics where applicable
- Consistent formatting throughout
- **Mandatory Answer Key**: Every worksheet MUST have a complete answer key appended at the end.
- **Mandatory Transcript**: If the materials involve a listening task, the full transcript MUST be included at the end (after the answer key).

### Format Standards
- **Headers**: Start with the correct branded image (`bell-header.jpg` or `intensive-header.jpg`).
- **Typography**: Use Arial or Roboto; `11pt` body text is standard.
- **Layout**:
    - **NEVER use multiple columns for main text**. Text should always flow in a single column for readability.
    - **Tables**: Use tables for boxing content (rules, examples), not for page layout columns.
- **Self-Checks**: Include "Before You Present" or "Self-Check" checklists for student autonomy.
- **Mandatory Page Breaks**:
    - Always insert a hard page break before the **Answer Key**.
    - Use `<div class="page-break"></div>` followed by a spacer (e.g., `&nbsp;`).

### File Naming Convention

```
DD-MM-YY-[Topic]-[Skill/System]-[Program]
```

| Component | Options |
|-----------|---------|
| `DD-MM-YY` | Date (e.g., `27-12-25`) |
| `Topic` | Subject matter (e.g., `Politeness`, `Presentation-Structure`) |
| `Skill/System` | `Reading`, `Listening`, `Writing`, `Speaking` |
| `Program` | `Bell` or `Intensive` |

**Examples:**
- `27-12-25-Politeness-Reading-Intensive.html`
- `29-12-25-Presentation-Structure-Speaking-Bell.html`

---

## Dependencies

| Dependency | Status | Notes |
|------------|--------|-------|
| Multimodal image reading | ✅ Available | Gemini 3 Flash |
| Image generation | ⚠️ Restricted | Use `generate_image` cautiously; prefer CSS/Assets. |
| Audio generation | 🔜 Planned | Future skill |

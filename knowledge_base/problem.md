# Technical Problem Report: Bespoke Typst Lesson Plan Template

## 1. Objective
We are attempting to create a professional, bespoke lesson plan template in Typst named `modern_template_EP`. This template must approximate a specific visual design (provided via image) while adhering to strict pedagogical and stylistic mandates for the Bell Language Centre.

## 2. File Locations (Absolute Paths)
- **Template Source**: `C:\PROJECTS\LESSONS AND SLIDESHOWS 2\templates\modern_template_EP.typ`
- **Test Harness**: `C:\PROJECTS\LESSONS AND SLIDESHOWS 2\test_template_EP.typ`
- **Compiled Output**: `C:\PROJECTS\LESSONS AND SLIDESHOWS 2\test_template_EP.pdf`
- **Reference Image**: `C:\PROJECTS\LESSONS AND SLIDESHOWS 2\templates\2027-lesson-plan-template.png`
- **Logo Asset**: `C:\PROJECTS\LESSONS AND SLIDESHOWS 2\images\ACT.png`

## 3. Core Requirements
- **Typography**: Base font must be **Calibri 11 point**.
- **Branding**:
    - Header must contain "UNIT LESSON PLAN" (centered and underlined).
    - The ACT logo must appear only on the **right ear** (right-aligned).
- **Metadata**: A bar containing Teacher (hardcoded to "Ed"), Date, Week No, Classes, and Course Level.
- **Main Table Structure**:
    - **Lesson Topic**: Full width row.
    - **Lesson Aim**: Full width row.
    - **Lesson Shape & Page Numbers**: Split row.
    - **Lesson Stages**: A header row spanning all columns.
    - **Stages Columns**: Exactly three columns: **Aim**, **Procedure**, and **Interaction**.
    - **Cell Alignment**: All material in all cells must be **top-aligned**.
    - **Stage Separation**: Each lesson stage must be visually separated (ruled horizontal lines).
    - **Footer Row**: Resources and Slides URL in a separate row at the bottom.

## 4. The Problem: The "Content Distribution" Block
The primary technical hurdle is how to pass lesson stage material from the user's `.typ` file into the template's table such that it correctly populates the three columns (Aim, Procedure, Interaction).

### Failed Approaches:
1. **The `doc` Sequence Logic**:
   - **Method**: User provides a continuous stream of content blocks. The template attempts to detect a `sequence`, filter out paragraph breaks/spaces, and spread the remaining "children" as positional arguments to the table (`..doc.children`).
   - **Symptom**: This resulted in literal array brackets `[` and `]` appearing in the rendered PDF, and content often "left-shifting" where all material (Aim, Proc, Interaction) ended up merged in the "Aim" column.

2. **The Helper Function (`stage`)**:
   - **Method**: Providing a `stage(aim, proc, interaction)` helper that returns an array of content.
   - **Symptom**: Typst's scoping and sequence handling produced errors like `unexpected argument` or `unknown variable` during the `#show: ... .with(...)` call.

3. **Scoping and Syntax Errors**:
   - Frequent compiler rejections of function signatures (e.g., `#let` vs `let`) and issues with named vs. positional arguments when attempting to pass the stages list.

## 5. Current Status
The template is currently in a "broken" state regarding stage distribution. The goal is to find a robust Typst pattern that allows a teacher to write their lesson stages naturally while ensuring the template places them into the 3-column grid without layout corruption or literal syntax appearing in the output.

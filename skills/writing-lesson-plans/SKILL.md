---
name: writing-lesson-plans
description: >
  Interactive lesson planning workflow. Use when the user wants to create
  a lesson plan, design a lesson, or prepare teaching materials. Guides
  through shape selection, metadata collection, and lesson generation.
---

# Writing Lesson Plans

This skill guides you through an 8-step interactive workflow to create a lesson plan.

## Prerequisites

- Access to `knowledge_base/shapes/` directory for modular shape definitions
- Materials in `/inputs` subfolder (or user will design new materials)

## Workflow

### Step 1: Present Lesson Shape Menu

Load shapes from `knowledge_base/shapes/` directory and present:

```
Which lesson shape would you like to use?

A. Text-based presentation of language
B. Language Practice
C. Test-Teach-Test (TTT)
D. Situational Presentation (PPP)
E. Receptive Skills (Reading/Listening - Traditional)
F. Productive Skills (Speaking/Writing - Traditional)
G. Task-Based Learning (TBL)
H. SCR Receptive Skills (Reading/Listening - Storytelling Framework)
I. SCR Systems (Grammar/Vocabulary - Storytelling Framework)
J. SCR Productive Skills (Speaking/Writing - Message Structure)
```

### Step 2: Collect Lesson Metadata

Ask for:
- **CEFR Level**: A1, A2, B1, B2, C1, C2
- **Focus**: Systems (Grammar/Vocabulary/Pronunciation) or Skills (Reading/Writing/Listening/Speaking)
- **Teacher Name**: Defaults to **Ed Rush** (Always use this unless specified otherwise)
- **Duration**: Total lesson time in minutes
- **Textbook/Unit**: If using coursebook
- **Page Numbers**: Relevant pages
- **Assessment Type**: CA (Continuous Assessment), formal test, or n/a

### Step 3: Lesson Type

Ask:
> "Is this an **Intensive** or **Regular Bell** lesson?"

This determines which header image to use:
- **Intensive**: `intensive-header.jpg`
- **Regular Bell**: `bell-header.jpg` (or appropriate regular header)

### Step 4: Materials Source

Ask:
> "Will you be designing new materials (separate skill) or using pre-existing materials?"

If pre-existing:
1. List subfolders in `/inputs`
2. Ask user to select one
3. Note: Actual file scanning uses a separate multimodal skill

### Step 5: Clarify Materials

If materials are unclear, ask specific questions:
- What is the main topic/context?
- What target language items are covered?
- Are there audio/video components?
- Are there exercises with answer keys?

### Step 6: Special Requests and Notes

Before generating the lesson plan, ask:
> "Do you have any special requests or notes for this lesson? (e.g., include a YouTube video, emphasize particular exercises, specific activities, time constraints, student needs)"

Wait for user response and incorporate their requests into the lesson plan.

### Step 7: Suggest Objective + Marker Sentences

Based on collected information:

1. **Propose lesson objective** using format:
   > "By the end of the lesson, learners will be better able to [skill/language point] in the context of [topic]."

2. **Suggest marker sentences** (for shapes A, B, C, D):
   > Example sentences containing target language for clarification stages.

Wait for user approval before proceeding.

> [!CRITICAL]
> ## Model Compliance Requirement
> 
> Before generating the lesson plan, **consult the model lesson plan** for the selected shape in `knowledge_base/shapes/shape-[letter].yaml`.
> 
> The generated lesson plan must:
> 1. **Match the stage structure** of the model (not be a slavish rendering of materials)
> 2. **Follow the pedagogical intent** - e.g., Shape E focuses on skills, not language
> 3. **Use similar stage headers** - e.g., "Lead-in", "Reading for detail", "Post-reading"
> 4. **Maintain similar timing proportions** - the model shows where to invest time
> 5. **Consolidate activities** into logical stages rather than listing each exercise separately
6. **Explicit Task Referencing**: Always reference specific task/exercise numbers (e.g., "Task 2: Global Reading") within the Procedure column. This ensures the lesson plan is directly anchored to the materials.
> 
> **Example: Shape E (Receptive Skills) model has only 3 stages:**
> - Stage 1: Lead-in (6 min) - Multi-part warmup with prediction/discussion
> - Stage 2: Reading for detail and specific information (22 min) - Main reading tasks
> - Stage 3: Post-reading task (2 min) - Brief personalization or 70-word response
> 
> **Do NOT** create 6+ granular stages for each worksheet section. Combine related activities into coherent stages that match the model.

> [!IMPORTANT]
> ## McKinsey Storylining & Strategic Pedagogy
> 
> Do NOT slavishly and mechanistically reproduce the structure of worksheets. Also, **AVOID labored, hokey, or intrusive metaphors** (e.g., Turning everything into "Coding", "Heroes", or "Mechanics").
> 
> Instead:
> - **McKinsey Logic**: Use the **SCR Framework** (Situation, Complication, Resolution) to structure the lesson flow.
> - **Dot-Dash Strategy**: Organize key points as **Dots** (Headlines) and evidence as **Dashes** (Details).
> - **Similes over Metaphors**: When explaining pedagogy, use **professional similes** rather than deep metaphors. 
>   - *Example (Simile)*: "Like an architect sketching a plan, we must outline our ideas before writing."
>   - *Avoid (Labored Metaphor)*: "You are the Programmer, and Paragraph 2 is your System Architecture."
> - **Strategic Clarity**: Frame material as an expert consultant would—focused on *influence* and *clarity*.
- **No Rewards/Dojos**: NEVER include mentions of "Dojo rewards", "stickers", or any other artificial reward systems. The focus is on intrinsic motivation and professional task engagement.
- **No Hallucinations**: Do NOT invent visual materials (e.g., "Show photo of Thai student with EKG") unless they definitively exist in the `images/` or materials folder. Use generic references to the title/topic if unsure.

### Step 8: Write Lesson Plan (Typst Format)

Generate the lesson plan **in Typst format** for professional PDF output. Use the standardized component library.

> [!IMPORTANT]
> **Output Format**: Typst (`.typ`) files compiled to PDF using the `compiling-typst-docs` skill.
> - Typst provides version control, reusability, and consistent branding.
> - **Template Import**: Always import the components at the top:
>   `#import "../../skills/writing-lesson-plans/templates/lesson-plan-components.typ": *`

#### File Naming Convention
Store in the **source folder** (same as materials) with this format:
```
DD-MM-YYYY-LP-[CEFR]-[topic]-[Shape].typ
```
*(Note: Use 4-digit year)*

#### Typst Structure

**Template Boilerplate:**

```typst
#import "../../skills/writing-lesson-plans/templates/lesson-plan-components.typ": *

#set page(paper: "a4", margin: (top: 1.5cm, bottom: 2cm, x: 2cm))
#set text(font: "Arial", size: 10pt, fill: rgb("#333333"))
#set par(leading: 0.65em, justify: false)

#lesson_header("[bell or intensive]")

#metadata_table((
  teacher: "Ed Rush",
  date: "[DD-MM-YYYY]",
  cefr: "[Level]",
  duration: "[XX Minutes]",
  shape: "[X (Name)]",
  assessment: "[N/A or CA]",
  focus: "[Focus]",
  materials: "[filename]",
))

#v(0.5cm)

#main_aim_box[
  By the end of the lesson, learners will have practiced...
]

#v(0.5cm)

#differentiation_box[
  This lesson employs a "Tiered Text" strategy, allowing students to self-select between B1, B1+, and B2 versions of the core material. This approach is grounded in *Krashen's Input Hypothesis (1982)*, which posits that language acquisition occurs when learners receive "comprehensible input" (i+1). 
]

#v(0.5cm)

#stage_table((
  stage("ONE", "Lead-in", "8", "To activate schema...", [
    - Procedure point 1...
    - Procedure point 2...
  ], "T-Ss / Ss-Ss"),
))
```

#### 🔍 MANDATORY: Review & Polish

Before finalizing the plan, you **MUST** conduct a self-evaluation:

1.  **Consult the Model**: Open `knowledge_base/shapes/shape-[letter].yaml`.
2.  **Evaluate Detail**: Does your procedure have the same level of granular detail as the `example_lesson_plan` in the model?
3.  **Correct Truncation**: Expand procedures with specific pedagogical steps if they look too brief.
4.  **🔍 CHECK FOR ORPHANS**: Ensure no "Stage Header" (maroon row) is left alone at the bottom of a page. 
    - **To Fix**: If a Stage Header is orphaned, split the `stage_table` into two separate calls and insert `#pagebreak()` between them in the `.typ` file.
5.  **Verification**: You will be judged on whether the lesson plan feels as "thick" and professional as the model.

#### 🧪 Step 9: Validate (MANDATORY)
Run the validator before finalizing:
```powershell
python skills/writing-lesson-plans/scripts/validate_lesson_plan.py "path/to/lesson-plan.typ" --mode [bell|intensive]
```
- **Rule**: If the script fails, fix the issues and re-run until it passes.

#### Pre-teach Vocabulary Format (Shape E)

Select **5 words** from the source text.

```
### 1. word /phonetic/: English context sentence (implies meaning).
Thai translation: Thai context sentence (implies meaning).
```

---

## Reference Files

- [REFERENCE.md](REFERENCE.md) - Shape summaries
- [knowledge_base/shapes/](file:///c:/PROJECTS/LESSONS%20AND%20SLIDESHOWS%202/knowledge_base/shapes/) - Complete shape definitions

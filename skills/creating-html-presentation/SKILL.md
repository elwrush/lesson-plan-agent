# Skill: Creating HTML Presentations (`creating-html-presentation`)

## Description
This skill generates vibrant, high-energy HTML presentations using **Reveal.js**. It transforms lesson plans into dynamic, web-based experiences with "pop and verve."

## Context
Use this skill to create the visual backbone of a lesson. Slides must:
- **Mirror the Lesson Plan**: Alignment with stages and materials is mandatory.
- **High-Energy Stage Segues**: Use clear, high-energy transitions (Phases).
- **Visual Impact**: Use high-contrast themes and cinematic visuals.

## 🛑 VISUAL-FIRST WORKFLOW (MANDATORY)

> [!CRITICAL]
> **DO NOT WRITE CODE UNTIL STEP 4**
> You must strictly follow this linear process. Do not skip steps.

### Step 0: ❓ Context Check
**Goal**: Determine the target audience and file routing.
- **Ask**: "Is this a **Bell** or **Intensive** presentation?"
- **Why**: This determines where the final 'link text file' (for Google Docs) is saved and how the tone is calibrated.

### Step 1: 🎨 Theme Selection
**Goal**: Define the visual identity before planning content.
- **Action**: Propose 2-3 distinct visual themes based on the lesson topic.
- **Examples**:
  - **Cyber-Gamer**: (Default) Neon, Dark Navy, Glitch effects. High Energy.
  - **Noir / Detective**: Black & White, Red Accents, Typewriter fonts. (Good for: Analysis/Investigation).
  - **Minimal / Corporate**: Clean White/Grey, Bold Sans-Serif, Deep Blue accents. (Good for: Exam Prep).
- **Gate**: **STOP** and wait for user to choose a theme.

### Step 2: 📝 The Visual Plan (Markdown)
Once the theme is picked, describe the *visual experience*.
- **Goal**: Map the lesson stages to slides using the **Approved Theme**.
- **Instruction**: "Describe visuals/colors that match the [Theme Choice]."
- **Format**:
  ```markdown
  ## Slide 1: Title
  - **Visual**: Hero image of [Subject]...
  - **Text**: "The 20/20 Tech Writer" (Big, Bold)
  
  ## Slide 2: Segue (Phase 1)
  - **Color Palette**: [Matches Approved Theme]
  - **Visual**: [Specific Icon/Image]
  - **Text**: "PHASE 1: THE HOOK"
  ```

### Step 3: 🚦 User Approval Gate
**STOP**. Present the Visual Plan (Markdown) to the user.
- **Ask**: "Does this visual structure match the [Theme Name] vision?"
- **Do not proceed** to wireframing until the user says "Yes."

### Step 4: 📐 The Wireframe (Mermaid Canvas Logic)
Map the layout of every slide using a Mermaid diagram. 
- **Philosophy**: "Canvas, Not Webpage."
- **Constraint**: The slide is a **Fixed 960x700 Artboard**.
- **Logic**: Use `row-container` (Rows) and `col-XX` (Columns).

```mermaid
graph TD
    subgraph "Slide Canvas (960x700)"
        Row[Row Container (Height: 500px)]
        Left[Col-40: Image (Max-Height: 400px)]
        Right[Col-60: Text Content]
    end
```

### Step 5: 🛠️ Implementation (The Gold Standard)
Now, write the `index.html`.
- **Golden Rule**: **COPY `REFERENCE_TEMPLATE.html`**.
- **Adapt the Theme**:
  - Modify the `:root` CSS variables (`--maroon`, `--cyan`, `--navy`, `--glass`) to match the **Approved Theme**.
  - **DO NOT** break the layout classes (`.row-container`). Only change colors/fonts.
- **Branding Rules**:
  - **Front Page**: MUST use the logo `@[images/ACT_transparent.png]`.
  - **Title Text**: NO "Bell Language Centre" or identifying text.
- **Safety Rules**:
  - **Images/Iframes**: MUST be `max-height: 400px` (or 350px). NEVER `height: 100%`.
  - **Text**: Use `r-fit-text` ONLY for titles.

### Step 6: 🚀 Deployment & Link File
- Push to the repository.
- Verify on the deployed URL (Cloudflare).
- **Generate Link File**: Create the `.html` link file (for Google Docs).
- **Cache Bust**: If updating, add `?v=X.X` to CSS links.

## Pedagogical & Thematic Standards (STRICT)

### 1. The Expert ESL Teacher Voice
Slides are a teaching tool, not just a display.
- **Rule**: Every slide must have a clear *student action* or *takeaway*.
- **Tone**: **Warm & Authoritative**. High standards, high energy.
- **Scaffolding**: You MUST use the `<div class="teacher-tip">` box for hints, warnings, or "Pro Tips."

| ❌ Weak / Boring (Forbidden) | ✅ "Pop & Verve" (Mandatory) |
| :--- | :--- |
| "Writing Task 1" | "YOUR MISSION: CODE THE ARTICLE" |
| "Here is a model answer." | "THE PERFECT 20/20 BLUEPRINT" |
| "Vocabulary List" | "VOCABULARY WEAPONS" |
| "Conclusion" | "MISSION COMPLETE / DEBRIEF" |

### 2. Theming: Flexible Identity
- **Rule**: The visuals must strictly follow the **Approved Theme** (Step 1).
- **Adaptability**: Changing the theme means changing the **CSS Variables** in `index.html`.
  - *Example*: If "Noir" is chosen, change `--cyan` to `--red` and `--navy` to `black`.
- **Consistency**: Once a theme is chosen, apply it to **every slide** (Segues, Headers, Boxes).
- **Forbidden**: 
  - 🚫 White backgrounds (unless "Minimal" theme is explicitly chosen).
  - 🚫 Mismatched aesthetics (e.g., Neon font on a Sepia background).
  - 🚫 "Corporate" stock photos.

### 3. Language & Formatting
- **Headings**: ALWAYS Uppercase. ALWAYS `r-fit-text` (for Slide Titles).
- **Body Text**: Large, readable (min 24px).
- **Bolding**: Bold **key phrases** in every paragraph to guide the eye.


### 3. Source Material Sync
- **Rule**: Slides cannot be divorced from source materials.
- **Naming**: If the Worksheet says "Task 2", the Slide must say "TASK 2". Do not invent new names like "Activity B".
- **References**: Always cite the specific worksheet section or page number.

### 4. The Answer Key Golden Rule
- **Interleaving**: Answer slides must appear **immediately after** the relevant Question slide.
- **Density**: **ONE Answer Per Slide**. Never list 5 answers on one screen.
- **Content**:
  - **The Answer**: Big and Bold.
  - **The Proof**: A snippet of the text/transcript where the answer was found.
  - **The Why**: A brief explanation of *why* it is correct.

### 5. Direct Vocabulary Instruction (The Legacy Standard)
For **Bell** or **Vocabulary-Focused** lessons, you must use this strict format:
- **One Word Per Slide**.
- **Header**: Word + /phonemics/ + **Thai Definition** (No English transliteration).
- **Body**: 
  - English Context Sentence (Target word **bolded**).
  - Thai Context Sentence (Target word **bolded**).
- **Audio Enhancement (Mandatory)**:
  - **Action**: Run `skills/creating-html-presentation/scripts/generate_vocab_audio.py`.
    - `python generate_vocab_audio.py --word "Hikikomori" --context "Toshi had such extreme..." --output "images/audio/hikikomori.wav"`
  - **HTML**: Insert a "Listen" button above the context sentence:
    ```html
    <div class="audio-player">
        <p class="listen-label">🔊 Listen to the word!</p>
        <audio controls src="images/audio/word.wav"></audio>
    </div>
    ```

- **Constraint**: The context sentence must *illustrate the meaning*, not just use the word.

### 6. Visualizing Processes (Infographics)
- **Primary Method**: Use the `generate_image` tool.
  - **Prompting**: "Create a high-contrast [Theme] style infographic showing [Process]. Use neon colors on a dark background."
  - **Why**: Custom art matches the "Pop & Verve" aesthetic better than code-generated charts.
- **Fallback**: Only use Mermaid/Charts if the data is *highly technical* and requires exact precision (e.g., specific stats).
- **Rule**: If it looks "corporate" or "default," **kill it and regenerate**.

## Technical Standards (The Fixed Canvas)

### 📐 Resolution
- **960x700**. Do not change this.
- **Margin**: 0.1.

### 🧱 Layout Classes (Use These EXACTLY)
- `.slide-canvas`: The main wrapper.
- `.row-container`: `width: 900px`, `gap: 40px`.
- `.col-40`, `.col-50`, `.col-60`: Fixed width columns.
- `.glass-box`: The standard container for text.
- `.header-strap`: The "Cyber Pill" branding (Top-Left).

### 🎬 Media
- **Local Assets**: Use `images/`.
- **YouTube**: Always use the `padding-bottom: 56.25%` wrapper hack for aspect ratio, constrained by a parent `col` width.

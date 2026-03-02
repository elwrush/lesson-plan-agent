# Code Reference & Layout Catalog

> **Purpose**: Detailed reference for layouts, themes, and code patterns.
> **Use**: Consult this file during Step 3 (Config Generation).

---

## 🧠 Pedagogical Mapping Matrix (The "Brain")

**CRITICAL**: Use this table to select the correct layout for the content type. Do not guess.

| Worksheet Content Type | **MANDATORY Layout** | **Required Content Structure** |
| :--- | :--- | :--- |
| **New Concept / Strategy** | `strategy` | **Bridge Slide**: Background Color + Big Icon + Rationale. |
| **List of Vocabulary** | `split_table` | Native HTML `<table>` with icons in col 1. |
| **Matching (Word + Def)** | `match_reorder` | JSON lists (`left_items`, `right_items`). |
| **Gap Fill / Sentence Completion** | `split_table` | Native HTML `<table>` with descriptive icons in col 1. **No bullets/carats**. |
| **Listening/Reading Text** | `audio_experience` | Immersive listening: Title + Instruction + Player + Background. |
| **Editing / Error Correction** | `editing` | Text with sequential replacements using `auto-animate`. |
| **Individual New Word** | `vocab` | **High-Impact Intro**: Left-aligned card, Header Word + Icon. Table Rows: Phoneme, Thai, Example. |
| **List of Vocabulary** | `split_table` | Native HTML `<table>` with icons in col 1. |
| **Lead-in / Warmer** | `video` or `title` | Video/Image background. |

> **⚠️ Layout Gap Analysis**: If the content does NOT fit these patterns (e.g., complex game, timeline), you **MUST** ask the user: *"This content requires a new layout. Shall I design a new template for it?"*

---

## 🏗️ Layout Catalog (The "Menu")

| Layout ID | Description | Best For |
| :--- | :--- | :--- |
| **`title`** | Gold Standard Split: Deck 1 (ALL CAPS) & Deck 2 (Title Case). | Opening slide. |
| **`segue`** | Heavy Radial Gradient with Skewed Phase markers. | Transition between phases. |
| **`strategy`** | Solid Color Background + Title + Text. | **Bridge Slides**, Context, Rules. |
| **`split_table`** | Split layout with embedded HTML table. | List-based tasks (Vocab/Matching). |
| **`match_reorder`** | Interactive Vocabulary Match. Right column morphs. | Matching tasks. |
| **`video`** | Embeds YouTube/Shorts + Floating Task Box. | Lead-ins, Warmers. |
| **`checklist`** | Grid of items for "Skim" tasks. | Simple checking tasks. |
| **`vocab`** | High-impact word intro. Rows: Phoneme, Thai, Example with highlighting. | High-frequency word introduction. |
| **`answer`** | Validation slide with "Why?" explanation box. | Answer keys. |
| **`cross_out`** | Legacy red-strikethrough fragments. | Finding mistakes (Deprecated). |
| **`editing`** | Auto-animating word replacement (Green). | Premium Error Correction. |
| **`audio_experience`** | Immersive listening deck with integrated player. | Audio-led reading/listening. |
| **`schema_activation`** | Discussable Lead-in with icon and question. | Warmers/Lead-ins. |

---

## 🎨 CSS Themes

Themes are located in `css/themes/`.

| Theme | Vibe | Usage |
| :--- | :--- | :--- |
| **`thai-heritage.css`** | **Gold Standard**. Deep Royal Blue + Gold. | Default for all academic lessons. |
| **`indonesia.css`** | Batik patterns, warm earth tones. | Cultural topics. |
| **`noir.css`** | High contrast, monochrome + red accent. | Serious/Crime topics. |
| **`cyber.css`** | Neon, dark mode, futuristic. | Tech/Sci-Fi topics. |

---

## ⚠️ Technical Pitfalls (Learned Lessons)

1.  **Pedagogical Scaffolding**:
    -   ❌ **NEVER** dump a task without context.
    -   ✅ **ALWAYS** insert a **Bridge Slide** (`strategy` layout) before every major task block (Vocab, Grammar, Speaking) to explain the *Why* and *How*.

2.  **Table Alignment**:
    -   ❌ **NEVER** use center-alignment for any text or numbers in tables.
    -   ✅ **ALWAYS** ensure `text-align: left` is applied to the table or individual cells to maintain readability and flow.

3.  **Generative Hallucinations**:
    -   ❌ **NEVER** summarize or truncate source sentences in grammar/vocab tasks.
    -   ✅ **ALWAYS** verify strict verbatim alignment with the `.typ` source.

4.  **Student-Centric Voice**:
    -   ❌ **NEVER** use teacher-procedural words in student-visible areas (e.g., "Objective: Students will...", "Rationale: Focus on...").
    -   ✅ **ALWAYS** address the student directly with high energy (e.g., "YOUR MISSION", "THE CHALLENGE", "PRO TIP").

### 🎭 Tone Comparison Table

| Teacher-Facing (BANNED) | Student-Facing (REQUIRED: "Pop & Verve") |
| :--- | :--- |
| Objective: Master IPA Symbols | YOUR MISSION: Decode the Secret Code! |
| Rationale: Focus on phoneme contrasts | THE CHALLENGE: Spot the Difference! |
| Instructions: Listen and tick | LISTEN & TICK: Can you catch them all? |
| Procedural: Monitor student pairs | *[Place in <aside class="notes"> only]* |
| Note: /ɪ/ is a short vowel | PRO TIP: Keep it short and snappy! |

5.  **Timer Placement**:
    -   ❌ **NEVER** place `<div class='timer-display'>` or `<button class='timer-btn'>` outside of a table structure.
    -   ✅ **ALWAYS** wrap timers in a `<tr><td colspan='2'>` row at the bottom of the relevant task table.
    -   ✅ **ALWAYS** use the `.timer-container` wrapper to ensure the timer and buttons are **horizontally stacked**.
6.  **Icon-Only Discipline**:
    -   ❌ **NEVER** use `<ul>` bullets, `>` carats, or generic `fa-chevron-right` icons.
    -   ✅ **ALWAYS** use content-aware icons (e.g., `fa-pen-fancy` for writing, `fa-comments` for discussion).

---

## 📖 Human-Readable Blueprint Template

Use this format for `slide_architecture.md`. It must be clear, bold, and easy to skim.

### SLIDE 1: TITLE — [Purpose: Hook & Branding]
*   **Headline**: PRONUNCIATION: SOUNDS & SYMBOLS
*   **Visual**: Cinematic video of a glowing digital code background.
*   **Voice**: High-energy greeting.
*   **Logic**: No animation. Fade-in transition.

### SLIDE 2: THE CHALLENGE — [Purpose: Bridge to Phonemes]
*   **Headline**: ENGLISH IS A LIE!
*   **Visual**: A large, amber Warning icon on a dark maroon background.
*   **Logic**: `auto-animate` the word "LIE" to pulse.
*   **Bridge**: Links the frustration of spelling to the solution (the Chart).

### SLIDE 3: TASK 1 (PART A) — [Purpose: Core Practice]
*   **Headline**: LISTEN & TRANSCRIBE
*   **Layout**: `split_table`
*   **Visual**: Character lineup image on the left; Transcription table on the right.
*   **Logic**: Sequential `fragments` for the audio controls.
*   **Bridge**: Moves from global listening to specific vowel focus.

11. **Timer Table Mandate**: **NEVER** place timer boxes or their controls outside of a table. Every task slide requiring a timer MUST use a `<table>` layout, and the timer controls MUST be embedded as a row within that table (usually using `colspan`). The timer and its control buttons **MUST** be horizontally stacked using the `.timer-container` wrapper.

---

## 🧩 Copy-Paste Snippets

### Bridge Slide (Pedagogical Scaffolding)
```json
{
    "layout": "strategy",
    "title": "BUILDING BLOCKS",
    "background_color": "#C2B280",
    "icon": "fas fa-map-marked-alt",
    "content": "<p>Contextual explanation...</p>",
    "notes": "Explain why we are learning this."
}
```

### Individual Vocab Slide (High-Impact)
```json
{
    "layout": "vocab",
    "word": "PRECIOUS",
    "icon": "fas fa-gem",
    "phoneme": "/ˈpreʃəs/",
    "thai": "ล้ำค่า",
    "context_sentence": "Don't drop that vase! It's very <span style='color: var(--accent);'>precious</span> to my grandmother.",
    "image": "images/gold_bar.jpg"
}
```

### Native Table Pattern (Task + Timer)
```html
<table style='width: 100%; border-collapse: separate; border-spacing: 0 20px; font-size: 1.2em; text-align: left;'>
    <tbody>
        <tr>
            <!-- MANDATORY: Always use an ICON for the list item. Must be LEFT aligned. -->
            <td style='width: 60px; text-align: left; vertical-align: middle; font-weight: bold; color: #FFD700;'><i class='fas fa-question-circle'></i></td>
            <td style='vertical-align: middle;'>Question text here...</td>
        </tr>
        <!-- Timers should also follow the left-alignment rule for the container cell -->
        <tr>
            <td colspan='2' style='text-align: left;'>
                <div class='timer-container' style='justify-content: flex-start;'>
                    <div class='timer-display' id='t1'>02:00</div>
                    <button class='timer-btn' onclick='toggleTimer(120, "t1", this)'>START</button>
                    <button class='timer-btn' onclick='resetTimer(120, "t1", this)'>RESET</button>
                </div>
            </td>
        </tr>
    </tbody>
</table>
```
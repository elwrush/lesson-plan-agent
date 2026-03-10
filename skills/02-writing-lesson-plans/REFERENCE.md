# Lesson Shapes Reference

Quick reference for the 7 lesson shapes. Full details in [lesson_shapes.yaml](file:///c:/PROJECTS/LESSONS%20AND%20SLIDESHOWS%202/knowledge_base/lesson_shapes.yaml).

## Shape Summaries

| Shape | Name | When to Use | Typical Stages |
|-------|------|-------------|----------------|
| **A** | Text-based Presentation | Introducing language via reading/listening text | Lead-in → Clarify TL → Controlled Practice → Freer Practice |
| **B** | Language Practice | Follow-up to A or C; more practice needed | Lead-in → Semi-controlled → Freer Practice |
| **C** | Test-Teach-Test (TTT) | Testing prior knowledge before teaching | Lead-in → Test 1 → Test 2 → Teach → Practice |
| **D** | Situational Presentation (PPP) | Teaching new language in context | Lead-in → Present (MPF) → Produce |
| **E** | Receptive Skills | Reading/Listening focus | Lead-in → Pre-teach Vocab → Gist / Scanning → Main Task (Detail) → Post-task |
| **F** | Productive Skills | Speaking/Writing focus | Lead-in → Preparation → Task → Feedback |
| **G** | Task-Based Learning (TBL) | Communication-first approach | Pre-task → Task Cycle → Planning → Report → Analysis |
| **H** | SCR Receptive Skills | Narrative-driven Reading/Listening | Situation → Complication (Conflict) → Resolution (Insight) |
| **I** | SCR Systems | Narrative-driven Grammar/Vocab | Situation (Awareness) → Complication (Challenge) → Resolution (Mastery) |
| **J** | SCR Productive Skills | Narrative-driven Speaking/Writing | Situation (Position) → Complication (Counter-view) → Resolution (Synthesis) |

## Generic / Combined Stages (Preferred for Modern Designs)
| Stage Name | When to Use |
|------------|-------------|
| **Context & Genre** | Opening stage for reading/listening lessons. |
| **Vocab & Prediction** | Replacing or combining Pre-teach Vocab with schema activation. |
| **The Story (Gist)** | For narrative-based gist tasks. |
| **Deep Analysis** | For complex comprehension or thematic analysis tasks. |
| **Vocab & Prediction** | Combining barrier removal with content guessing. |

## Interaction Patterns

| Code | Meaning |
|------|---------|
| T-Ss | Teacher to Students (whole class) |
| Ss-Ss | Student to Student (pairs/groups) |
| S | Solo work |

## Objective Templates

**Systems (Grammar/Vocabulary):**
> By the end of the lesson, learners will be better able to use [target language] in the context of [topic].

**Skills (Reading/Listening):**
> By the end of the lesson, learners will have practiced the sub-skills of [gist/detail/inference] in the context of [text type about topic].

**Skills (Speaking/Writing):**
> By the end of the lesson, learners will be better able to [communicate/write] about [topic] using [language features].

---

## Example Lesson Plan Output

**Life Elementary – Unit 10B – How well can you remember**

**Aim**: By the end of the lesson, learners will have had practice using the present perfect and past simple in the context of life experiences.
**Systems**: Grammar
**Page Numbers**: SB: 167
**Assessment**: n/a

### Lead-in

| Stage | Aim | Procedure | Time | Interaction |
|-------|-----|-----------|------|-------------|
| 1 | To engage Ss and activate schemata | Mini WB quiz about Nelson Dellis. 1 mini WB per student. Ss negotiate answers in teams. Award points. | 3 | T-Ss |

### Clarifying Target Language

| Stage | Aim | Procedure | Time | Interaction |
|-------|-----|-----------|------|-------------|
| 2 | To clarify meaning, form, pronunciation of TL | **Meaning**: Guided discovery with marker sentences on PP. Pairs answer CCQs. 1 min. Feedback. **Form**: New pairs discuss form. 1 min. Feedback. **Pron**: Model and drill chorally/individually. Pairs work on stress and connected speech. | 5 | Ss-Ss |

### Controlled Practice

| Stage | Aim | Procedure | Time | Interaction |
|-------|-----|-----------|------|-------------|
| 3 | To provide controlled practice | Page 167, Exercise 2. Ss choose correct option. 5 min. Swap and check scores. | 8 | T-Ss |

### Freer Practice

| Stage | Aim | Procedure | Time | Interaction |
|-------|-----|-----------|------|-------------|
| 4 | To provide freer practice | Liar! Liar! game. A makes present perfect questions. B answers "yes, I have". A asks follow-up past simple questions to detect lies. 5 questions each, then swap. 8 min. Content feedback → error correction. | 10 | Ss-Ss |

---

### Answer Key (Footer)

**Exercise 2 (p.167)**: 1. have visited, 2. went, 3. has lived, 4. moved, 5. have never been

---

## Typst Template <a name="typst-template"></a>

All lesson plans MUST use the single universal template. **No other template exists.**

```typst
#import "/templates/modern_template.typ": modern_template, stage

#show: modern_template.with(
  topic:      "[Lesson Topic]",
  teachers:   "Ed",
  date:       "DD-MM-YYYY",
  week:       "Week N",
  classes:    "[Class List]",
  level:      "[CEFR Level]",
  lesson_aim: "By the end of the lesson, learners will...",
  shape:      "[Letter] ([Shape Name])",
  sb:         "Page XX",
  wb:         "Page XX",
  resources:  "[Materials list]",
  slides_url: "https://elwrush.github.io/actions-gh-pages/[lesson-folder]/",
  stages: (

    stage(
      [Stage aim sentence.],
      [
        - *Part 1*: Procedure detail.
        - *Part 2*: Procedure detail.
      ],
      [T-Ss],
    ),

    stage(
      [Stage aim sentence.],
      [
        Workbook Page XX, Ex Y. Students do Z. T monitors.
      ],
      [Ss-Ss],
    ),

    // Add one stage() call per lesson stage.
  ),
)
```

### Rules
- `stage(aim, procedure, interaction)` — all three arguments are **content blocks** (`[...]`).
- `stages:` receives an **array of `stage()` calls** — one per lesson stage.
- **Never** pass raw content blocks directly into `stages:` — always wrap in `stage()`.
- The `#show:` line requires no body content after it; leave the file blank after the closing `)`.

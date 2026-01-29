---
name: generating-quizzes
description: Generates high-quality multiple-choice and Boolean quizzes using a multi-stage NLP approach (Anchors -> Bloom's Alignment -> Distractor Refinement).
---

# Generating Quizzes

This skill automates the creation of high-quality, pedagogically sound assessments from reading and listening texts. It uses a structured multi-stage approach inspired by the `Questgen.ai` framework to ensure cognitive depth and plausible distractors.

## Workflow

```mermaid
graph TD
    A[Discovery: Ingest Text/Transcript] --> B[Stage 1: Identify Assessment Anchors]
    B --> C[Linguistic Alignment: CEFR Profiling]
    C --> D[Stage 2: Balanced Randomized Answer Key]
    D --> E[Generate Pre-determined Options Order]
    E --> F[Stage 3: Bloom's Alignment & Generation]
    F --> G[Map Concepts to Keyed Options]
    G --> H[Stage 4: Validation Script]
    H --> I{Valid JSON?}
    I -- No --> F
    I -- Yes --> J[Stage 5: Agent Self-Critique]
    J --> K{Metrics Pass?}
    K -- No: Easy/Obvious --> F
    K -- Yes --> L[Human Subjective Validation]
    L --> M[Final Quiz JSON in published/]
```

1.  **Define Parameters**:
    -   **Source Content**: Reading text or Listening transcript.
    -   **CEFR Level**: Target difficulty (A1-C2).
    -   **Question Types**: Choose from the 12 types in [REFERENCE.md](file:///c:/PROJECTS/LESSONS%20AND%20SLIDESHOWS%202/skills/generating-quizzes/REFERENCE.md).
    -   **Bloom's Levels**: Specify target cognitive levels (e.g., "Understanding", "Analyzing").
    -   **CRITICAL INTERACTION**: The agent MUST present these options as an **enumerated menu** to the user to confirm the "Assessment Blueprint" before proceeding.

2.  **Generate Answer Key**:
    -   **CRITICAL**: Generate a randomized sequence of correct answer positions (e.g., [1, 0, 3, 2...]) *before* generating the questions. 
    -   **Randomization Rule**: You MUST ensure a balanced distribution of answers (A, B, C, D) across the quiz. For a 6-item quiz, each option (0-3) should ideally appear at least once. Do NOT allow more than 2 consecutive identical answers.

3.  **Generate Content**:
    -   Apply the multi-stage prompt series in [REFERENCE.md](file:///c:/PROJECTS/LESSONS%20AND%20SLIDESHOWS%202/skills/generating-quizzes/REFERENCE.md).
    -   Match the correct answer for each question to the pre-generated Answer Key position.
    -   **Constraint**: Every question must be grounded in an "Assessment Anchor" from the text.

4.  **Validate Structure**:
    -   Run `python skills/generating-quizzes/scripts/validate_quiz.py [path_to_json]`.
    -   **Published Storage**: The final, validated quiz JSON MUST be saved to the `inputs/[folder]/published/` subfolder.
    -   **Requirements**: Exactly 4 choices for MCQs, 0-indexed answers, and pedagogical explanations.

5.  **Human Subjective Validation & Agent Self-Critique**:
    -   Perform a final quality check as a "human validator." 
    -   **MANDATORY Agent Critique**: You MUST specifically answer the following three questions for the generated quiz:
        1.  **Is the quiz too easy or difficult?** (Does it match the CEFR level?)
        2.  **Are the answers obvious?** (Can they be guessed without reading the text?)
        3.  **Do the distractors need to be improved?** (Are they plausible but clearly wrong?)
    -   **Rewrite Rule**: If the answer to any of the above is "Yes" (meaning the quiz fails the metric), you MUST rewrite the affected questions and repeat the validation until it passes.

## Design Standards

-   **Plausible Distractors**: Distractors must be semantically related to the correct answer but factually incorrect based on the text.
-   **No Ordinals**: Choices must not contain "A)", "1.", etc.
-   **Bloom's Taxonomy**: Questions should range from "Remembering" to "Evaluating" based on task requirements.

## Troubleshooting

-   **Hallucination**: If questions reference information not in the text, reinforce the "Assessment Anchor" constraint in the prompt.
-   **Predictable Answers**: Ensure "Answer Mention Order" is varied (don't always make 'C' the correct answer).

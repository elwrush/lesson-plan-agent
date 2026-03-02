# This file contains the single source of truth for approved stage names
# It is imported by the programmatic validator hook to enforce consistency.

APPROVED_STAGES = {
    # Shape A: Text-based Presentation
    "Lead-in",
    "Clarify TL",
    "Controlled Practice",
    "Freer Practice",

    # Shape B: Language Practice
    # "Lead-in", (duplicate)
    # "Controlled", (too generic, prefer Controlled Practice)
    "Semi-controlled",
    # "Freer Practice", (duplicate)

    # Shape C: Test-Teach-Test (TTT)
    # "Lead-in", (duplicate)
    "Test 1",
    "Test 2",
    "Teach",
    "Practice",

    # Shape D: Situational Presentation (PPP)
    # "Lead-in", (duplicate)
    "Present (MPF)",
    # "Practice", (duplicate)
    "Produce",

    # Shape E: Receptive Skills
    # "Lead-in", (duplicate)
    "Pre-teach Vocab",
    "Gist / Scanning",
    "Main Task (Detail)",
    "Vocabulary Focus",
    "Post-task",

    # Shape F: Productive Skills
    # "Lead-in", (duplicate)
    "Preparation",
    "Task",
    "Feedback",

    # Shape G: Task-Based Learning (TBL)
    "Pre-task",
    "Task Cycle",
    "Planning",
    "Report",
    "Analysis",

    # Shape H: SCR Receptive Skills
    "Situation",
    "Complication (Conflict)",
    "Resolution (Insight)",

    # Shape I: SCR Systems
    "Situation (Awareness)",
    "Complication (Challenge)",
    "Resolution (Mastery)",

    # Shape J: SCR Productive Skills
    "Situation (Position)",
    "Complication (Counter-view)",
    "Resolution (Synthesis)",
    
    # Generic / Combined Stages
    "Context & Genre",
    "Vocab & Prediction",
    "The Story (Gist)",
    "Deep Analysis"
}

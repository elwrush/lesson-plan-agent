# Skill: Creating HTML Presentations (`creating-html-presentation`)

## Description
This skill generates vibrant, high-energy HTML presentations using **Reveal.js**. It transforms lesson plans into dynamic, web-based experiences with "pop and verve" tailored for middle and high school students.

## Context
Use this skill to create the visual backbone of a lesson. Slides must:
- **Mirror the Lesson Plan**: Alignment with the stages and materials (Worksheets/Course Packets) is mandatory.
- **High-Energy Stage Segues**: Use clear, high-energy transitions that signal exactly which stage of the lesson is occurring.
- **Visual Impact**: Use high-contrast themes, dynamic fragments, and cinematic AI-generated visuals to maintain teenage engagement.

## Gated Workflow (MANDATORY)

> [!CRITICAL]
> **Markdown Preview Gate**
> 
> You MUST present a structural outline to the user before generating the Reveal.js code.
> 
> 1. **Create a Markdown Outline**: Map the slides to the Lesson Shape stages.
>    ```markdown
>    # [Title] - Presentation Structure
>    ## Slide 1: [Engagement Title] (Lead-in)
>    - Stage: [Name]
>    - Content: [Key points]
>    ```
> 2. **🚦 USER REVIEW GATE**: Present the outline to the user.
>    - **DO NOT proceed** to coding the `index.html` until the user explicitly approves the structure.
> 3. **Drafting the Verve**: Once approved, write the code in `index.html` using the approved narrative.
> 4. **Generate Assets**: Create cinematic backgrounds for the key transition moments.
> 5. **Bundle & Verify**: Run `bundle_reveal.py` to create the final standalone HTML.

## Pedagogical Standards

### 1. The Expert ESL Teacher Voice
Slides are not just information—they are a teaching tool. Every slide must sound as if it were designed by an expert teacher.
- **Warm & Authoritative**: Use encouraging phrases ("Let's dive in," "Your time to shine") while maintaining high standards.
- **Scaffolding**: Include "Teacher's Tips" or "Examiner Notes" to add extra value and guidance beyond the basic task.
- **Engagement**: Use rhetorical questions and dramatic framing to keep energy levels high.

### 2. The Energy Rule ("Pop & Verve")
Every slide should feel like a moment in a show, not a corporate briefing. This is critical for middle and high school learners.
- **Punchy Language**: Use "YOUR MISSION" instead of "Writing Task." Use "LOCK IN" instead of "Conclusion."
- **Visual Storytelling**: Use single large words, punchy quotes, or high-impact images to drive a point.
- **Hook & Hold**: Every 3-4 slides should have a dramatic visual shift (color change, full-screen image) to reset student attention.

### 3. Mandatory Stage Segues
Never move between lesson stages without a dedicated **Transition Slide**. These provide the mental map for students to follow the lesson flow.
- **Form**: A high-impact title + a guiding phrase that builds excitement for the next task.
- **Vibe**: 
  - *Anti-pattern*: "Next: Task 2."
  - *Verve Style*: "BLUEPRINT LOCKED. Now, let's build the masterpiece..."

### 4. Vertical & Horizontal Alignment
- **Horizontal**: If a student reads ONLY the slide titles, they should understand the entire story of the lesson.
- **Vertical**: Every slide must directly support the objective of its current Lesson Stage.
- **Materials Sync**: If a slide says "Look at Task 2," then Task 2 must be prominently labeled and identical in the Worksheet.

## Technical Standards

### 📐 Sizing & Scaling (16:9 Standard)
```javascript
Reveal.initialize({
  width: 1920,
  height: 1080,
  margin: 0.1,
  minScale: 0.2,
  maxScale: 2.0,
  autoPlayMedia: true,
  transition: 'slide', 
  hash: true
});
```

### 🎬 Multimedia Rule
Classroom connectivity can be inconsistent.
- **Local Assets**: Use local images inside the `images/` folder where possible.
- **YouTube Embeds**: Use `r-stretch` to ensure the video dominates the room.
- **Lazy Loading**: Always use `data-src` for images/videos.

## Usage
### 1. Setup
Create a directory `inputs/[DATE]/clean-deck` containing `index.html`. 

### 2. Bundling
```bash
python skills/creating-html-presentation/scripts/bundle_reveal.py --input "[PATH_TO_INDEX_HTML]" --output "[OUTPUT_PATH]"
```

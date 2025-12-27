---
name: reading-visual-content
description: >
  Extracts text from images and PDFs using Gemini's multimodal vision. Use when the
  user mentions scans, screenshots, photos of documents, or "read this image".
---

# Reading Visual Content

Extract text and structure from images (JPG, PNG) and PDFs using Gemini's multimodal vision capabilities.

---

## Triggers
Use this skill when:
- User provides image files (JPG, PNG, JPEG) containing text
- User provides PDF files that need text extraction
- User mentions "scan", "screenshot", "photo of document", or "read this image"

---

> [!CAUTION]
> ## MANDATORY: Model Confirmation Required
> 
> **This skill ONLY works with Gemini 3 Flash or later models with multimodal vision.**
> 
> Before attempting to read ANY image or PDF file, you MUST:
> 
> 1. **Stop and ask the user:**
>    > "To read visual content, I need to use Gemini 3 Flash which has multimodal vision capabilities. Please confirm you have selected **Gemini 3 Flash** in your model settings before I proceed."
> 
> 2. **Wait for explicit confirmation** from the user that they have switched models.
> 
> 3. **If you cannot see/read image content**, be HONEST and say:
>    > "I cannot read this image with the current model. Please switch to Gemini 3 Flash and try again."
> 
> **NEVER hallucinate or invent content that you cannot actually see in the image.**

---

## Workflow

### Step 1: Confirm Model
Before processing ANY image, ask:
```
To accurately read this image, I need Gemini 3 Flash's multimodal capabilities. 
Have you selected Gemini 3 Flash in your model settings? 
Please confirm before I proceed.
```

**Do NOT proceed until the user confirms.**

### Step 2: Identify Source Files
List the files to be processed. Supported formats:
- `.jpg`, `.jpeg`, `.png` (images)
- `.pdf` (documents)

### Step 3: View Files with Multimodal
Use the `view_file` tool to read image/PDF content:

```
view_file AbsolutePath="/path/to/image.jpg"
```

### Step 4: Verify You Can See the Content
After viewing, you MUST be able to describe:
- The actual text visible in the image
- The layout and structure
- Any images or diagrams present

> [!WARNING]
> If the `view_file` output does not show readable text content from the image, STOP and inform the user:
> "I received the file but cannot see its contents. This usually means the current model doesn't support image reading. Please switch to Gemini 3 Flash."

### Step 5: Extract & Structure
Only proceed if you can genuinely see the content. Follow these guidelines:

#### Text Extraction
- Preserve the original structure (headings, paragraphs, lists)
- Mark unclear/illegible text with `[illegible]`
- Preserve formatting cues (bold, italic, numbered lists)

#### Quality Checks
- Quote specific text from the image to prove you can see it
- Compare extracted text against visible content
- Flag any uncertain interpretations with `[?]`

### Step 6: Output Format
Structure extracted content in Markdown:

```markdown
# [Document Title - from the actual image]

## [Section 1 - actual heading from image]
[Extracted text exactly as it appears...]

[IMAGE: Description of any figures you can actually see]
```

---

## Honesty Protocol

| Situation | Required Response |
|-----------|-------------------|
| Cannot see image content | "I cannot read this image. Please switch to Gemini 3 Flash." |
| Partially legible | "Some text is unclear. Here's what I can read: [actual text]" |
| User hasn't confirmed model | "Please confirm you're using Gemini 3 Flash before I proceed." |
| Content fully visible | Proceed with extraction, quoting specific text to verify |

---

## Anti-Hallucination Checklist

Before providing extracted content, verify:
- [ ] User confirmed Gemini 3 Flash is active
- [ ] I can quote specific text from the image
- [ ] I can describe the visual layout accurately
- [ ] I have NOT invented any content

**If any checkbox fails, DO NOT provide extracted content.**

---

## Example: Correct Behavior

**User provides**: `document.jpg`

**WRONG (hallucinating)**:
> "The document discusses strategies for effective communication..."

**CORRECT (honest)**:
> "To read this image accurately, I need Gemini 3 Flash. Please confirm you've switched to that model, then I'll extract the content."

*After confirmation and successful reading:*
> "I can see the document. The title reads 'Chapter 5: Communication Skills' and the first paragraph states: '[exact quote from image]'..."

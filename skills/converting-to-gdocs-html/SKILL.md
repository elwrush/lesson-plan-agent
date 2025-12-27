---
name: converting-to-gdocs-html
description: >
  Converts content to HTML that imports cleanly into Google Docs. Use when preparing
  materials for Google Docs upload or when the user mentions GDocs formatting.
---

# Converting to GDocs HTML

Guidelines for converting content to HTML that imports cleanly and professionally into Google Docs.

---

## Typography Standards
Follow the rules in [GDocs-Typography.md](file:///c:/PROJECTS/LESSONS%20AND%20SLIDESHOWS%202/knowledge_base/GDocs-Typography.md).

## Shading & Design Features

### 1. Element Shading
Use `background-color` and `padding` on `div` or `table` elements. This imports as paragraph shading or cell background in GDocs.
- **Good**: `<div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px;">Content</div>`
- **Avoid**: Complex CSS filters, gradients, or shadows (they usually fail).
- **Vocabulary Boxes**: For word lists in boxes, use pipe separators (`|`) with non-breaking spaces (`&nbsp;`) for clear, import-friendly formatting.
  - Example: `word1 &nbsp;|&nbsp; word2 &nbsp;|&nbsp; word3`

### 2. Borders
Specify all four borders for boxes. `border-radius` is sometimes ignored but worth including for web preview.
- **Recommended**: `border: 1px solid #ccc;`

### 3. Layout: The Inset Image Problem
While `float: right` works for web browsing, Google Docs HTML import often converts floated images into standard block elements.
- **Robust Workaround**: Use a **2-column table** with `border: 0`.
  - Column 1: Text
  - Column 2: Image
  - Setting column widths (e.g., `width="60%"` and `width="40%"`) ensures the layout survives.

### 4. Spacing
Google Docs handles `margin` inconsistently in HTML import. Use `padding` inside shaded boxes and `<br>` or empty paragraphs for vertical spacing between sections.

---

## CSS Best Practices for Import
- **Inline Styles**: For the highest success rate, use inline `style="..."` attributes on elements.
- **Simplified CSS**: Avoid pseudo-elements (`::before`), flexbox, or grid for layout (use tables).
- **Colors**: Use hex codes (#ffffff).

---

## Implementation Template

```html
<!-- Robust Shaded Box -->
<div style="background-color: #f0f7ff; padding: 15px; border: 1px solid #cce0ff; border-radius: 8px; margin-bottom: 20px;">
  <p style="margin: 0;"><strong>Exercise 1:</strong> Instruction text...</p>
</div>

<!-- Robust Inset Image (using table) -->
<table width="100%" border="0" cellspacing="0" cellpadding="10" style="border-collapse: collapse;">
  <tr>
    <td valign="top" style="text-align: justify;">
      Text passage goes here...
    </td>
    <td width="40%" valign="top">
      <img src="image.png" width="100%" style="display: block;">
    </td>
  </tr>
</table>
```

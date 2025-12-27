# Google Docs Typography Standards

These are the mandatory font and spacing rules for all Google Docs output.

---

## Typography Rules

| Element | Font | Size | Weight | Spacing |
|---------|------|------|--------|---------|
| Body text | Roboto | 11pt | Normal | 1.5pt line spacing |
| H1 | Arial | 14pt | **Bold** | - |
| H2 | Arial | 13pt | **Bold** | - |
| H3 | Arial | 12pt | **Bold** | - |

---

## CSS Implementation

When generating HTML for Google Docs, use these inline styles:

```css
/* Body text */
font-family: 'Roboto', sans-serif;
font-size: 11pt;
line-height: 1.5;

/* H1 */
font-family: Arial, sans-serif;
font-size: 14pt;
font-weight: bold;

/* H2 */
font-family: Arial, sans-serif;
font-size: 13pt;
font-weight: bold;

/* H3 */
font-family: Arial, sans-serif;
font-size: 12pt;
font-weight: bold;
```

---

## HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>[Document Title]</title>
  <style>
    body {
      font-family: 'Roboto', sans-serif;
      font-size: 11pt;
      line-height: 1.5;
      color: #333;
    }
    h1 {
      font-family: Arial, sans-serif;
      font-size: 14pt;
      font-weight: bold;
    }
    h2 {
      font-family: Arial, sans-serif;
      font-size: 13pt;
      font-weight: bold;
    }
    h3 {
      font-family: Arial, sans-serif;
      font-size: 12pt;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <!-- Content here -->
</body>
</html>
```

---

## Google Docs Import Notes

When importing HTML to Google Docs:
- Google Fonts (like Roboto) must be available in Google Docs
- Inline styles may be required for consistent rendering
- Complex CSS may not be preserved

---

## Related Files
- [Google-Style.md](file:///c:/PROJECTS/LESSONS%20AND%20SLIDESHOWS%202/knowledge_base/Google-Style.md) - Code formatting conventions for HTML/CSS

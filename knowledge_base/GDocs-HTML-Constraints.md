# Google Docs HTML Import Constraints

When pushing HTML to Google Docs via API, many CSS properties are ignored or behave differently. Google Docs translates HTML into its internal schema, not browser rendering.

---

## The "Big Three" Issues

| Issue | Problem | Solution |
|-------|---------|----------|
| **Floats** | `float: right/left` is ignored | Use 2-column tables with `border: none` |
| **CSS Classes** | `.class` selectors unreliable | Use inline `style=""` attributes |
| **Unsupported CSS** | `box-shadow`, `border-radius`, `max-width` | Remove or accept they'll be ignored |

---

## Supported vs Unsupported CSS

| Feature | ✅ Supported | ❌ Not Supported |
|---------|-------------|-----------------|
| **Typography** | `font-family`, `font-size`, `color`, `font-weight`, `text-align` | Custom web fonts, `letter-spacing`, `text-shadow` |
| **Spacing** | `margin-top/bottom`, `line-height` | `margin-left/right` (on blocks), `z-index`, `position: absolute/fixed` |
| **Lists** | Standard `<ul>` and `<ol>` | Custom `list-style-type` images |
| **Colors** | Hex codes, RGB | RGBA (transparency flattened) |
| **Layout** | Tables | Flexbox, Grid |

---

## Structural Translation

| Web Concept | Google Docs API Equivalent |
|-------------|---------------------------|
| Floating Image | 2-column table: text cell (70%), image cell (30%) |
| Colored Box | 1-cell table with `background-color` |
| Gaps (`<span>`) | Underscores `_______` or fixed-width text |
| Page Breaks | API `insertPageBreak` request (HTML ignored) |

---

## Best Practices

1. **Inline Your CSS** — Use `style=""` attributes, not `<style>` blocks or classes
2. **Use Points (pt)** — Font sizes and widths in `pt`, not `px`
3. **Sanitize HTML** — Remove `<script>`, `<iframe>`, `<form>` tags
4. **Images Must Be URLs** — Local paths don't work. Either:
   - Host images publicly (https://...)
   - Embed as base64 data URIs
   - Use API's `insertInlineImage` request
5. **Width in Percentages or Points** — Avoid `max-width`

---

## Design Philosophy — When to Use Tables

**Avoid tables for styling.** Tables should be reserved for **truly tabular data**:
- ✅ Lesson plans (Stage/Aim/Procedure/Time)
- ✅ Behavior rating grids
- ✅ Comparison charts
- ✅ Data with rows and columns

**For other content, prefer formatted text:**
- Use **paragraph styles** with inline CSS for emphasis
- Use **tabs and horizontal rules** for spacing
- Use **single-cell tables sparingly** for colored headers only
- Let content flow as natural paragraphs

**Rationale:** Tables in Google Docs are harder to edit, have spacing issues, and create unnecessary complexity.

**Additional Note:** Background shading (`background-color`) is also optional — plain text with good formatting is easier to edit.

---

## Table-Based Box Template

```html
<!-- Colored box using 1-cell table -->
<table style="width: 100%; background-color: #f0f7ff; border: 1px solid #cce0ff; border-collapse: collapse;">
  <tr>
    <td style="padding: 15pt;">
      <p><strong>Exercise 1:</strong> Instructions here...</p>
    </td>
  </tr>
</table>
```

---

## Table-Based Image Inset Template

```html
<!-- Text with inset image using 2-column table -->
<table style="width: 100%; border: none; border-collapse: collapse;">
  <tr>
    <td style="vertical-align: top; padding-right: 15pt;">
      <p>Text content goes here...</p>
    </td>
    <td style="width: 200pt; vertical-align: top;">
      <img src="https://hosted-url.com/image.png" width="200">
    </td>
  </tr>
</table>
```

---

## Related Files
- [GDocs-Typography.md](GDocs-Typography.md) — Font and spacing standards
- [converting-to-gdocs-html/SKILL.md](file:///c:/PROJECTS/LESSONS%20AND%20SLIDESHOWS%202/skills/converting-to-gdocs-html/SKILL.md) — Conversion skill

---
name: using-meander
description: Guides text wrapping around images in Typst worksheets using the Meander package. Use when creating inset images with flowing text in two-column layouts.
---

# Using Meander for Text Wrapping

## Purpose
This skill documents how to use the **Meander 0.3.1** Typst package to wrap text around images in worksheet layouts. It covers single and multi-column flows with centered or aligned image obstacles.

## Prerequisites
- Typst installed and accessible via `typst compile`
- Meander package available from Typst Universe (`@preview/meander:0.3.1`)

## Core Concepts

### Import
```typst
#import "@preview/meander:0.3.1"
```

### Basic Structure
```typst
#meander.reflow({
  import meander: *

  // 1. Define obstacles (images, boxes)
  placed(alignment, content)

  // 2. Define containers for text flow
  container(width: Xcm)

  // 3. Provide content to flow
  content[ ... ]
})
```

## Common Patterns

### Single Column with Right-Aligned Image
```typst
#meander.reflow({
  import meander: *

  placed(
    top + right,
    block(
      width: 6cm,
      stroke: 2pt + maroon,
      inset: 12pt,
      image("/images/example.png", width: 100%)
    )
  )

  container()

  content[
    Your text flows here, wrapping around the image.
  ]
})
```

### Two-Column Layout with Centered Image
```typst
#meander.reflow({
  import meander: *

  // Centered image pushed down
  placed(
    center + top,
    dy: 4cm,
    block(
      width: 5cm,
      stroke: 2pt + maroon,
      inset: 16pt,
      fill: white,
      image("/images/example.png", width: 100%)
    )
  )

  // Two columns side-by-side
  container(width: 8cm)              // Left column
  container(width: 8cm, dx: 8.5cm)   // Right column

  content[
    Text flows from left column to right column,
    wrapping around the centered image.
  ]
})
```

### Multi-Page Flow
Add additional `container()` calls for each column on subsequent pages:
```typst
  container(width: 8cm)              // Left column, page 1
  container(width: 8cm, dx: 8.5cm)   // Right column, page 1
  container(width: 8cm)              // Left column, page 2
  container(width: 8cm, dx: 8.5cm)   // Right column, page 2
```

## Key Parameters

| Parameter | Used In | Purpose |
|-----------|---------|---------|
| `width` | `container()`, `block()` | Sets the width of the element |
| `dx` | `container()`, `placed()` | Horizontal offset from default position |
| `dy` | `placed()` | Vertical offset (push image down) |
| `inset` | `block()` | Internal padding inside the block |
| `stroke` | `block()` | Border style (e.g., `2pt + maroon`) |
| `fill` | `block()` | Background color |

## Limitations

1. **Contour Wrapping via Mathematical Equations**: Meander **DOES support contour wrapping**, but NOT via PNG alpha channels. Instead, it uses the `boundary: contour.grid()` feature with mathematical equations to define custom shapes (circles, ellipses, polygons, etc.). See "Advanced: Contour Wrapping" section below.
2. **Page Breaks**: Meander does not automatically create new containers for page overflow. You must pre-define enough containers.

## Best Practices

- Use `dy` to push images down so text flows above them before wrapping.
- Set `inset: 12pt` or higher for visual padding inside bordered image blocks.
- For two-column layouts, calculate `dx` as `column_width + gutter` (e.g., 8cm + 0.5cm = 8.5cm).
- Always test with `typst compile` after changes—meander errors can be cryptic.

## Advanced: Contour Wrapping

Meander supports **custom boundary shapes** using mathematical equations via `boundary: contour.grid()`. This allows text to wrap around circles, ellipses, or any shape definable by a function.

### Circle Example
```typst
#meander.reflow({
  import meander: *

  placed(
    center + horizon,
    boundary:
      // Override the default margin
      contour.margin(1cm) +
      // Then redraw the shape as a grid
      contour.grid(
        // 25 vertical and horizontal subdivisions.
        // Just pick a number that looks good.
        // A good rule of thumb is to start with obstacles
        // about as high as one line of text.
        div: 25,
        // Equation for a circle of center (0.5, 0.5) and radius 0.5
        (x, y) => calc.pow(2 * x - 1, 2) + calc.pow(2 * y - 1, 2) <= 1
      ),
    // Underlying object
    circle(radius: 3cm, fill: yellow),
  )

  container(width: 48%)
  container(align: right, width: 48%)
  content[
    #set par(justify: true)
    #lorem(570)
  ]
})
```

### How It Works
- `contour.margin(1cm)`: Adds spacing around the obstacle
- `contour.grid(div: 25, ...)`: Subdivides the bounding box into a grid
- `(x, y) => ...`: Mathematical function defining the shape (returns `true` if point is inside)
- Coordinates are normalized (0 to 1)

### Common Shapes
| Shape | Equation |
|:---|:---|
| **Circle** | `calc.pow(2 * x - 1, 2) + calc.pow(2 * y - 1, 2) <= 1` |
| **Ellipse** | `calc.pow((x - 0.5) / 0.4, 2) + calc.pow((y - 0.5) / 0.6, 2) <= 1` |
| **Diamond** | `calc.abs(x - 0.5) + calc.abs(y - 0.5) <= 0.5` |

### Limitations
- **NOT based on PNG alpha channels**: You cannot automatically trace a PNG's transparency
- **Manual equations required**: You must write the mathematical function for your shape
- **Grid resolution**: Higher `div` values = smoother contours but slower compilation

## Troubleshooting

### Common Errors

| Error | Cause | Fix |
|:---|:---|:---|
| `failed to decode image` | Image path is wrong or image is corrupted | Verify path starts with `/` (project root) and image opens correctly |
| `unexpected token` | Special characters inside `content[]` | Remove `**double asterisks**`, use `*single*` for emphasis |
| `expected identifier` | Placeholder syntax inside content | Do not use `#h(2cm)` inside `content[]`; use it outside |
| Content disappears | Not enough `container()` calls | Add more containers for page overflow |
| Text doesn't wrap | Image not `placed()` correctly | Ensure `placed()` comes before `container()` |

### Debug Workflow
1. **Compile without Meander first**: Ensure base document works.
2. **Add `placed()` only**: Verify image appears.
3. **Add `container()`**: Check containers are positioned.
4. **Add `content[]` last**: Verify text flows.

## Fallback Strategy

> **If Meander fails after 2 attempts, abandon it.**

Use a simple side-by-side layout instead:

```typst
#grid(
  columns: (1fr, 6cm),
  gutter: 1cm,
  [
    Your text content goes here without wrapping.
    It will appear in the left column.
  ],
  image("/images/example.png", width: 100%)
)
```

**Why**: Meander is powerful but fragile. A working simple layout is better than a broken complex one.

## Example Reference

See the "Fight or Flight" worksheet template:
`skills/generating-worksheets/templates/15-01-2026-B1-B2-Fight-or-Flight.typ`

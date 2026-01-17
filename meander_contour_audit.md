# Meander Contour Wrapping Audit - 2026-01-16

## Context7 Query Results

**Query**: Text wrapping around image contours and alpha channels in Typst Meander package

**Findings**: Context7 does not have the Typst Meander package (`@preview/meander`) indexed separately. Search results for "meander" returned the Clojure library `/noprompt/meander` instead.

## GitHub Repository Analysis

**Repository**: https://github.com/Vanille-N/meander.typ  
**Current Version**: 0.3.1  
**Last Updated**: Active development

### Key Discovery: Contour Wrapping IS Supported

Meander **DOES support contour wrapping**, but NOT via PNG alpha channel detection.

### How It Works

Meander uses `boundary: contour.grid()` with **mathematical equations** to define custom shapes:

```typst
placed(
  center + horizon,
  boundary:
    contour.margin(1cm) +
    contour.grid(
      div: 25,
      (x, y) => calc.pow(2 * x - 1, 2) + calc.pow(2 * y - 1, 2) <= 1
    ),
  circle(radius: 3cm, fill: yellow),
)
```

### Capabilities

✅ **Supported**:
- Circle contours
- Ellipse contours
- Diamond/polygon contours
- Any shape definable by a mathematical function `(x, y) => boolean`
- Adjustable grid resolution (`div` parameter)
- Margin control around obstacles

❌ **NOT Supported**:
- Automatic PNG alpha channel tracing
- Image-based contour detection
- Automatic shape recognition

### Parameters

| Parameter | Purpose |
|:---|:---|
| `contour.margin(1cm)` | Adds spacing around the obstacle |
| `contour.grid(div: 25, ...)` | Subdivides bounding box into grid (higher = smoother) |
| `(x, y) => ...` | Mathematical function (coordinates normalized 0-1) |

### Common Shape Equations

**Circle** (center 0.5, 0.5, radius 0.5):
```typst
(x, y) => calc.pow(2 * x - 1, 2) + calc.pow(2 * y - 1, 2) <= 1
```

**Ellipse** (horizontal 0.4, vertical 0.6):
```typst
(x, y) => calc.pow((x - 0.5) / 0.4, 2) + calc.pow((y - 0.5) / 0.6, 2) <= 1
```

**Diamond**:
```typst
(x, y) => calc.abs(x - 0.5) + calc.abs(y - 0.5) <= 0.5
```

## Skill Compliance Status

### Previous State (OUTDATED)
Our `using-meander` skill incorrectly stated:
> "**No Contour Wrapping**: Meander treats all images as rectangular bounding boxes. It cannot read PNG alpha channels to wrap text around irregular shapes."

### Current State (UPDATED ✅)
Skill now correctly documents:
1. Contour wrapping **IS supported** via `boundary: contour.grid()`
2. Uses mathematical equations, NOT PNG alpha channels
3. Includes working circle example from official docs
4. Documents common shape equations (circle, ellipse, diamond)
5. Clarifies limitations (manual equations required, no automatic tracing)

## Recommendations

1. **Use contour wrapping for geometric shapes**: Circles, ellipses, and simple polygons work well
2. **Avoid for complex organic shapes**: Requires manual mathematical approximation
3. **Start with `div: 25`**: Good balance between smoothness and compilation speed
4. **Test compilation time**: Higher `div` values can slow down rendering significantly

## References

- Official README: https://github.com/Vanille-N/meander.typ/blob/master/README.md
- Documentation PDF: https://github.com/Vanille-N/meander.typ/blob/master/docs/docs.pdf
- Package: `@preview/meander:0.3.1`

#import "@preview/meander:0.3.1"

#set page(paper: "a4", margin: 2cm)
#set text(font: "Arial", size: 11pt)
#set par(justify: true, leading: 0.65em)

// Use existing transparent image from your library
#let test_image = "/images/hook_icon_transparent.png"

// ========================================
// DEMONSTRATION: Meander Contour Limitations
// ========================================

#align(center)[
  #text(size: 16pt, weight: "bold")[Meander Contour Wrapping Test]
  #v(0.5em)
  #text(size: 10pt, style: "italic", fill: rgb("#A62D26"))[
    Testing whether Meander can wrap text around PNG alpha channel
  ]
]

#v(2em)

// ========================================
// TEST 1: Default (No Contour)
// ========================================
#text(size: 13pt, weight: "bold")[Test 1: Default Rectangular Boundary]
#v(0.5em)
#text(size: 9pt, fill: gray)[
  Meander treats the transparent PNG as a rectangular bounding box.
  The transparency is IGNORED.
]

#v(1em)

#meander.reflow({
  import meander: *

  placed(
    top + right,
    image(test_image, width: 6cm),
  )

  container()

  content[
    #lorem(120)
  ]
})

#pagebreak()

// ========================================
// TEST 2: Circular Contour Approximation
// ========================================
#text(size: 13pt, weight: "bold")[Test 2: Circular Contour (Mathematical Equation)]
#v(0.5em)
#text(size: 9pt, fill: gray)[
  Using `boundary: contour.grid()` with a circle equation.
  This does NOT read the PNG alpha channel - it's a manual mathematical approximation.
]

#v(1em)

#meander.reflow({
  import meander: *

  placed(
    top + right,
    boundary: contour.margin(0.5cm)
      + contour.grid(
        div: 30,
        (x, y) => calc.pow(2 * x - 1, 2) + calc.pow(2 * y - 1, 2) <= 1,
      ),
    image(test_image, width: 6cm),
  )

  container()

  content[
    #lorem(120)
  ]
})

#pagebreak()

// ========================================
// TEST 3: Ellipse Contour
// ========================================
#text(size: 13pt, weight: "bold")[Test 3: Ellipse Contour (Manual Approximation)]
#v(0.5em)
#text(size: 9pt, fill: gray)[
  Using an ellipse equation to approximate the shape.
  Still NOT based on the actual PNG transparency.
]

#v(1em)

#meander.reflow({
  import meander: *

  placed(
    top + right,
    boundary: contour.margin(0.5cm)
      + contour.grid(
        div: 30,
        // Ellipse: wider horizontally
        (x, y) => calc.pow((x - 0.5) / 0.5, 2) + calc.pow((y - 0.5) / 0.4, 2) <= 1,
      ),
    image(test_image, width: 6cm),
  )

  container()

  content[
    #lorem(120)
  ]
})

#pagebreak()

// ========================================
// CONCLUSION
// ========================================
#align(center)[
  #text(size: 14pt, weight: "bold", fill: rgb("#A62D26"))[
    Conclusion: Meander Cannot Read PNG Alpha Channels
  ]
]

#v(2em)

#block(
  fill: rgb("#F5F5F5"),
  inset: 16pt,
  radius: 4pt,
  width: 100%,
)[
  #text(size: 11pt)[
    *Key Findings:*

    1. *Meander does NOT automatically detect PNG transparency*
      - The transparent background is completely ignored
      - Text wraps around the full rectangular bounding box
      - You can see this clearly in Test 1

    2. *Manual contour equations are required*
      - You must write mathematical functions (circle, ellipse, etc.)
      - These are crude approximations, not based on the actual image shape
      - Compare Test 1 vs Test 2/3 to see the difference

    3. *Limitation for complex organic shapes*
      - Irregular shapes cannot be automatically traced
      - Mathematical approximations (circle/ellipse) don't follow the actual contour
      - The hook icon's irregular shape is NOT being traced

    4. *Best use case: Simple geometric shapes*
      - Circles, ellipses, diamonds work well
      - Complex organic shapes require manual "staircase" approximation (tedious)
  ]
]

#v(2em)

#align(center)[
  #text(size: 10pt, style: "italic", fill: gray)[
    For automatic contour wrapping around PNG alpha channels,
    you would need a different tool that can trace transparency.
    Meander's strength is in mathematical precision for geometric shapes.
  ]
]

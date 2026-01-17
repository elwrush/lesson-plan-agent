#import "@preview/meander:0.3.1"

#set page(paper: "a4", margin: 2cm)
#set text(font: "Arial", size: 11pt)
#set par(justify: true, leading: 0.65em)

// ========================================
// TEST 1: Default Rectangular Wrapping
// ========================================
#align(center)[
  #text(size: 14pt, weight: "bold")[Test 1: Default Rectangular Wrapping]
]

#v(1em)

#meander.reflow({
  import meander: *

  // Place the stressed student image (rectangular boundary)
  placed(
    top + right,
    block(
      width: 6cm,
      inset: 8pt,
      stroke: 2pt + rgb("#A62D26"),
      fill: white,
      image("/images/thai_student_fight_flight_transparent.png", width: 100%),
    ),
  )

  container()

  content[
    #lorem(150)
  ]
})

#pagebreak()

// ========================================
// TEST 2: Circular Contour Approximation
// ========================================
#align(center)[
  #text(size: 14pt, weight: "bold")[Test 2: Circular Contour Approximation]
  #v(0.5em)
  #text(size: 9pt, style: "italic", fill: gray)[
    (Using boundary: contour.grid() with circle equation)
  ]
]

#v(1em)

#meander.reflow({
  import meander: *

  // Place the stressed student image with circular contour
  placed(
    top + right,
    boundary: // Add margin around the obstacle
    contour.margin(0.8cm)
      +
      // Define circular boundary
      contour.grid(
        div: 30,
        // 30 subdivisions for smooth contour
        // Circle equation: center (0.5, 0.5), radius 0.5
        (x, y) => calc.pow(2 * x - 1, 2) + calc.pow(2 * y - 1, 2) <= 1,
      ),
    // The actual image
    block(
      width: 6cm,
      inset: 8pt,
      stroke: 2pt + rgb("#A62D26"),
      fill: white,
      image("/images/thai_student_fight_flight_transparent.png", width: 100%),
    ),
  )

  container()

  content[
    #lorem(150)
  ]
})

#pagebreak()

// ========================================
// TEST 3: Ellipse Contour (Taller)
// ========================================
#align(center)[
  #text(size: 14pt, weight: "bold")[Test 3: Ellipse Contour (Vertical)]
  #v(0.5em)
  #text(size: 9pt, style: "italic", fill: gray)[
    (Using boundary: contour.grid() with ellipse equation)
  ]
]

#v(1em)

#meander.reflow({
  import meander: *

  // Place the stressed student image with elliptical contour
  placed(
    top + right,
    boundary: contour.margin(0.8cm)
      + contour.grid(
        div: 30,
        // Ellipse equation: narrower horizontally, taller vertically
        (x, y) => calc.pow((x - 0.5) / 0.35, 2) + calc.pow((y - 0.5) / 0.55, 2) <= 1,
      ),
    block(
      width: 6cm,
      inset: 8pt,
      stroke: 2pt + rgb("#A62D26"),
      fill: white,
      image("/images/thai_student_fight_flight_transparent.png", width: 100%),
    ),
  )

  container()

  content[
    #lorem(150)
  ]
})

#pagebreak()

// ========================================
// TEST 4: Two-Column Layout with Contour
// ========================================
#align(center)[
  #text(size: 14pt, weight: "bold")[Test 4: Two-Column Layout with Circular Contour]
]

#v(1em)

#meander.reflow({
  import meander: *

  // Centered image with circular contour
  placed(
    center + horizon,
    dy: 3cm, // Push down 3cm
    boundary: contour.margin(1cm)
      + contour.grid(
        div: 25,
        (x, y) => calc.pow(2 * x - 1, 2) + calc.pow(2 * y - 1, 2) <= 1,
      ),
    block(
      width: 5cm,
      inset: 8pt,
      stroke: 2pt + rgb("#A62D26"),
      fill: white,
      image("/images/thai_student_fight_flight_transparent.png", width: 100%),
    ),
  )

  // Two columns
  container(width: 8cm)
  container(width: 8cm, dx: 8.5cm)

  content[
    #lorem(200)
  ]
})

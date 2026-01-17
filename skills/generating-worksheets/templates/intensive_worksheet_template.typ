
// ============================================================
// INTENSIVE WORKSHEET TEMPLATE
// ============================================================
// Use this template for Intensive Program worksheets.
// Key Difference: Full-width header image instead of maroon strap.
// ============================================================

#set page(
  paper: "a4",
  margin: (top: 1.5cm, bottom: 2cm, x: 2cm),
)
#set text(font: "Arial", size: 11pt, fill: rgb("#333333"))
#set par(leading: 0.8em, justify: true)

// BRAND COLORS
#let maroon = rgb("#8B1538")
#let slate-dark = rgb("#334155")
#let gray-line = rgb("#E0E0E0")

// ==========================================
// 1. INTENSIVE HEADER (MANDATORY)
// ==========================================
// Uses the pre-designed header image instead of building a strap.

#let intensive_header() = {
  block(
    width: 100%,
    [
      #image("/images/intensive-header.jpg", width: 100%)
    ],
  )
  v(0.3cm)
}

// ==========================================
// 2. STUDENT IDENTITY
// ==========================================

#let identity_block() = {
  block(width: 100%, inset: (bottom: 1em), [
    #grid(
      columns: (auto, 1fr, auto, 4cm),
      gutter: 1em,
      text(weight: "bold", fill: maroon)[Name:],
      line(start: (0pt, 0.8em), length: 100%, stroke: 0.5pt + black),
      text(weight: "bold", fill: maroon)[Student ID:],
      grid(
        columns: (1fr, 1fr, 1fr, 1fr, 1fr),
        gutter: 4pt,
        ..range(5).map(_ => box(width: 100%, height: 1.2em, stroke: (bottom: 1pt + black)))
      ),
    )
  ])
}

// ==========================================
// 3. TASK HEADER
// ==========================================

#let task_header(number, title) = {
  v(0.8cm)
  block(width: 100%, [
    #text(weight: "bold", fill: maroon, size: 14pt)[TASK #number: #title]
    #v(0.2cm)
    #line(length: 100%, stroke: 1.5pt + maroon)
    #v(0.4cm)
  ])
}

// ==========================================
// 4. WRITING LINES
// ==========================================

#let writing_lines(count: 15) = {
  for i in range(count) {
    v(0.75cm)
    line(length: 100%, stroke: 0.5pt + gray-line)
  }
}

// ==========================================
// 5. ANSWER KEY HEADER
// ==========================================

#let answer_key_header() = {
  v(1cm)
  block(width: 100%, fill: slate-dark, inset: 12pt, [
    #text(fill: white, weight: "bold", size: 12pt)[ANSWER KEY (For Teacher Reference)]
  ])
  v(0.5cm)
// ==========================================
// 6. GAPFILL COMPONENT (Modular)
// ==========================================
// Requires a placeholder string in items (e.g. "__") which is replaced by a writing line.

#let gapfill_exercise(items, placeholder: "__", line_length: 2.5cm) = {
  stack(
    dir: ttb,
    spacing: 0.4cm,
    ..items.enumerate().map(((i, item)) => {
      // Split the string by placeholder and rejoin with the visual line box
      let parts = item.split(placeholder)
      let content = parts.intersperse(
        box(width: line_length, height: 1em, stroke: (bottom: 0.5pt + black), baseline: 0.2em)
      ).join()
      
      grid(
        columns: (auto, 1fr),
        gutter: 1em,
        text(weight: "bold")[#(i + 1).],
        content
      )
    })
  )
}

// ==========================================
// 7. SINGLE SENTENCE WRITING (Modular)
// ==========================================
// Standard layout for rewrites: Question -> Vertical Space -> Full Width Line

#let single_sentence_writing(items, vertical_space: 1.2cm) = {
  stack(
    dir: ttb,
    spacing: 1cm,
    ..items.enumerate().map(((i, item)) => block(width: 100%, [
      #text(weight: "bold")[#(i + 1). #item] \
      #v(vertical_space)
      #line(length: 100%, stroke: 0.5pt + rgb("#E0E0E0")) // gray-line
    ]))
  )
}

// ==========================================
// USAGE EXAMPLE
// ==========================================
// Uncomment below to see a sample layout:
/*
#intensive_header()
#identity_block()

#task_header(1, "Sample Task")
Your task content goes here.

#writing_lines(count: 10)

#pagebreak()
#answer_key_header()
Answers go here.
*/

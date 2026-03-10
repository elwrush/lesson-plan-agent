// ============================================================
// modern_template.typ  —  ACT Unit Lesson Plan Template
// Usage:  #import "templates/modern_template.typ": modern_template, stage
//         #show: modern_template.with( ... stages: (stage(...), ...) ... )
// ============================================================

// Helper: wrap one stage's three columns into a typed tuple.
// Always call this from the user file — never pass raw content directly.
#let stage(aim, proc, interaction) = (aim, proc, interaction)

// Main template function.
// NOTE: `body` MUST be the final parameter so that #show: works correctly.
#let modern_template(
  topic:      "",
  teachers:   "Ed",
  date:       "",
  week:       "",
  classes:    "",
  level:      "",
  lesson_aim: "",
  shape:      "",
  sb:         "",
  wb:         "",
  resources:  "",
  slides_url: "",
  stages:     (),   // array of stage() tuples
  body,             // receives the doc body from #show: — do not remove
) = {

  // ── Page & Text Defaults ──────────────────────────────────
  set page(
    paper:  "a4",
    margin: (x: 1.5cm, top: 1.5cm, bottom: 1.5cm),
  )
  set text(font: "Calibri", size: 11pt, fill: rgb("#333333"))
  set par(leading: 0.55em)
  set table(align: top + left, stroke: 0.5pt + rgb("#bbbbbb"))

  // ── Colour Palette ────────────────────────────────────────
  let clr-header    = rgb("#4a0000")   // deep maroon — stage header bar
  let clr-col-head  = rgb("#f2f2f2")   // light grey  — column headings row
  let clr-meta-rule = rgb("#999999")

  // ── HEADER: centred title + right-ear logo ────────────────
  grid(
    columns: (2cm, 1fr, 2cm),
    align:   horizon,
    gutter:  0pt,
    [],
    align(center)[
      #text(weight: "bold", size: 14pt)[
        #underline(offset: 2pt)[UNIT LESSON PLAN]
      ]
    ],
    align(right)[
      #image("/images/ACT.png", width: 1.8cm)
    ],
  )

  v(0.25cm)

  // ── METADATA BAR ──────────────────────────────────────────
  block(
    width:  100%,
    stroke: (top: 0.5pt + clr-meta-rule, bottom: 0.5pt + clr-meta-rule),
    inset:  (y: 7pt, x: 5pt),
  )[
    #grid(
      columns: (auto, 1fr, auto, 1fr, auto, 1fr, auto, 1fr, auto, 1fr),
      column-gutter: 10pt,
      align: horizon,
      [*Teacher:*], [#teachers],
      [*Date:*],    [#date],
      [*Week No:*], [#week],
      [*Classes:*], [#classes],
      [*Course Level:*], [#level],
    )
  ]

  v(0.3cm)

  // ── PRE-BUILD STAGE CELLS ─────────────────────────────────
  // Each stage() call returns a 3-tuple.  stages is an array of those.
  // .flatten() collapses one level: [(a1,p1,i1),(a2,p2,i2)] → [a1,p1,i1,a2,p2,i2]
  let stage_cells = stages.flatten()

  // ── MAIN TABLE ────────────────────────────────────────────
  table(
    columns: (1fr, 2.8fr, 0.9fr),
    inset:   (x: 8pt, y: 8pt),

    // ── Row 1: Lesson Topic ───────────────────────────────
    table.cell(colspan: 3, align: left)[*Lesson Topic:* #topic],

    // ── Row 2: Lesson Aim ─────────────────────────────────
    table.cell(colspan: 3, align: left)[*Lesson Aim:* #lesson_aim],

    // ── Row 3: Shape | Page Numbers (split) ───────────────
    table.cell(colspan: 1, align: left)[*Lesson Shape:* \ #shape],
    table.cell(colspan: 2, align: left)[
      #grid(
        columns: (auto, 1fr, auto, 1fr),
        column-gutter: 12pt,
        align: horizon,
        [*SB:*], [#sb],
        [*WB:*], [#wb],
      )
    ],

    // ── Row 4: LESSON STAGES header bar ───────────────────
    table.cell(
      colspan: 3,
      fill:    clr-header,
      align:   center,
    )[
      #text(fill: white, weight: "bold", size: 10.5pt)[LESSON STAGES]
    ],

    // ── Row 5: Column headings ────────────────────────────
    table.cell(fill: clr-col-head, align: center)[*Aim*],
    table.cell(fill: clr-col-head, align: center)[*Procedure*],
    table.cell(fill: clr-col-head, align: center)[*Interaction*],

    // ── Stage rows (all three columns per stage) ──────────
    ..stage_cells,

    // ── Footer rows ───────────────────────────────────────
    table.cell(colspan: 3, align: left)[*Resources:* #resources],
    table.cell(colspan: 3, align: left)[
      *Slides URL:* #link(slides_url)[#slides_url]
    ],
  )

  // Render any body content placed after #show: (usually empty)
  body
}

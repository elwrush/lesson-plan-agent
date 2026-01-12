
// ============================================================
// PRONUNCIATION REPAIR WORKSHEET - V1 (TYPST NATIVE)
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
// 1. COMPONENTS
// ==========================================

// PAGE 1 HEADER (GAP STYLE - INTEGRATED STRAP)
#let integrated_header(title: "THE PRONUNCIATION SOUNDCHECK") = {
  block(
    width: 100%,
    height: 1.5cm,
    fill: maroon,
    inset: (left: 0.8cm, right: 1cm),
    radius: 0pt,
    align(horizon + left)[
      #stack(
        dir: ltr,
        spacing: 1.25em,
        image("/images/ACT_transparent.png", height: 0.75cm),
        image("/images/Bell.svg", height: 0.75cm),
        h(0.2cm),
        text(fill: white, size: 10.5pt, weight: "bold", tracking: 0.05em)[
          BELL LANGUAGE CENTRE #h(0.5em) | #h(0.5em) #title
        ],
      )
    ],
  )

  v(0.2cm)
  line(length: 100%, stroke: 1.5pt + maroon)
  v(0.6cm)
}

// STUDENT IDENTITY
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

// TASK CARD
#let task_card(level, title, bg_context, prompt, constraints) = {
  block(
    width: 100%,
    stroke: 1pt + maroon,
    radius: 4pt,
    clip: true,
    below: 0.8cm,
    [
      #block(fill: maroon, width: 100%, inset: 10pt, [
        #grid(
          columns: (auto, 1fr),
          text(fill: white, weight: "bold")[#level], align(right)[#text(fill: white, weight: "bold")[#title]],
        )
      ])
      #block(fill: white, inset: 12pt, width: 100%, [
        #text(size: 10pt, style: "italic", weight: "bold", fill: slate-dark)[#bg_context]
        #v(0.4em)
        #text(size: 11pt)[#prompt]
        #v(0.6em)
        #line(length: 100%, stroke: 0.5pt + gray-line)
        #v(0.4em)
        #text(size: 9pt, fill: slate-dark)[#constraints]
      ])
    ],
  )
}

// WRITING LINES
#let writing_lines(count: 15) = {
  v(0.4cm)
  for _ in range(count) {
    line(length: 100%, stroke: 0.5pt + slate-dark)
    v(0.55cm)
  }
}

// PEER REVIEW CHECKLIST
#let peer_checklist() = {
  block(
    width: 100%,
    stroke: 1pt + maroon,
    radius: 4pt,
    inset: 10pt,
    fill: rgb("#fff1f2"),
    [
      #text(weight: "bold", fill: maroon, size: 12pt)[Partner Review: Soundcheck Checklist]
      #v(0.5em)
      #table(
        columns: (1fr, auto, auto, auto),
        stroke: (x, y) => if y == 0 { (bottom: 1.5pt + maroon) } else { (bottom: 0.5pt + gray-line) },
        inset: 8pt,
        align: (horizon + left, center, center, center),
        fill: (x, y) => if y == 0 { maroon },
        text(fill: white, weight: "bold", size: 9pt)[Criteria],
        text(fill: white, weight: "bold", size: 9pt)[☺ Great],
        text(fill: white, weight: "bold", size: 9pt)[😐 OK],
        text(fill: white, weight: "bold", size: 9pt)[🔧 Remix],

        [Crossfader (Smooth linking)], [⭘], [⭘], [⭘],
        [Anchors (Final consonants)], [⭘], [⭘], [⭘],
        [Tapered Endings (No shouting)], [⭘], [⭘], [⭘],
        [Bass Kick (Sentence stress)], [⭘], [⭘], [⭘],
        [Performance (No long pauses)], [⭘], [⭘], [⭘],
      )
    ],
  )
}

// ==========================================
// 2. DOCUMENT LAYOUT
// ==========================================

// --- PAGE 1: DIAGNOSTIC & MIXING ---
#integrated_header()

#text(size: 18pt, weight: "bold", fill: maroon)[Step 1: The Mic Check]
#v(0.4em)
#text[Review your Speaking Feedback Sheet. What are the three most important 'distortions' you need to fix in your overall performance?]

#v(0.8cm)

#grid(
  columns: (1fr, 1fr, 1fr),
  gutter: 1cm,
  ..range(1, 4).map(i => block(
    width: 100%,
    height: 3cm,
    fill: rgb("#F8FAFC"),
    radius: 6pt,
    inset: 12pt,
    stroke: 1pt + gray-line,
    [
      #text(weight: "bold", fill: maroon, size: 12pt)[Target #i]
      #v(1fr)
      #line(length: 100%, stroke: 1pt + maroon)
    ],
  ))
)

#v(1.2cm)

#text(size: 18pt, weight: "bold", fill: maroon)[Step 2: The Studio Remix]
#v(0.4em)
#text[Now read the **Pronunciation** section of your report. Note three specific 'Mix Fixes' you will use to make your English sound smoother and more professional.]

#v(0.8cm)

#stack(
  dir: ttb,
  spacing: 0.8cm,
  ..range(1, 4).map(i => grid(
    columns: (auto, 1fr),
    gutter: 1em,
    text(weight: "bold", fill: maroon)[Action #i:], line(start: (0pt, 0.8em), length: 100%, stroke: 0.5pt + black),
  )),
)

#v(1fr)
#align(center)[#text(style: "italic", fill: slate-dark)[Write your script on the next page.]]

// --- PAGE 2: LEVEL A2 TASK ---
#pagebreak()
#identity_block()

#task_card(
  "Level A2 / A2+",
  "My Hope for the Future",
  "Speaking Challenge: One-Minute Preview",
  "Tell your partner about your future hopes. 'In the future, I want to... because... I think it will be...'",
  "Target: 1 Minute | Focus: Clear word endings (final /s/, /t/, /d/)",
)

#text(
  size: 10pt,
  weight: "bold",
  fill: slate-dark,
)[✍️ Write your one-minute script below. Then, underline your stressed words.]

#writing_lines(count: 10)

#v(0.2cm)
#peer_checklist()

// --- PAGE 3: LEVEL B1 TASK ---
#pagebreak()
#identity_block()

#task_card(
  "Level B1 / B1+",
  "A Vision for Later",
  "Speaking Challenge: One-Minute Narrative",
  "Explain your future plans. 'Looking ahead, my main ambition is... If I achieve this, then...'",
  "Target: 1 Minute | Focus: Sentence stress and natural rhythm",
)

#text(
  size: 10pt,
  weight: "bold",
  fill: slate-dark,
)[✍️ Write your one-minute script below. Then, underline stressed words and draw links (e.g. an‿apple).]

#writing_lines(count: 10)

#v(0.2cm)
#peer_checklist()

// --- PAGE 4: LEVEL B2 TASK ---
#pagebreak()
#identity_block()

#task_card(
  "Level B2",
  "Projecting Mastery",
  "Speaking Challenge: One-Minute Presentation",
  "Present your long-term goals. 'Ultimately, what I'm aiming for is... Not only would this help me..., but it would also...'",
  "Target: 1 Minute | Focus: Smooth linking and connected speech",
)

#text(
  size: 10pt,
  weight: "bold",
  fill: slate-dark,
)[✍️ Write your one-minute script below. Then, underline stressed words and draw linkages.]

#writing_lines(count: 10)

#v(0.2cm)
#peer_checklist()

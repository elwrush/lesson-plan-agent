
// ============================================================
// B1 REVERSE ENGINEERING: THE 20/20 TECH ARTICLE
// ============================================================

#set page(
  paper: "a4",
  margin: (top: 1cm, bottom: 2cm, x: 2cm),
)
#set text(font: "Arial", size: 12pt, fill: rgb("#333333"))
#set par(leading: 0.8em, justify: true)

// BRAND COLORS
#let maroon = rgb("#8B1538")
#let slate-dark = rgb("#334155")
#let gray-line = rgb("#E0E0E0")
#let code-bg = rgb("#F8FAFC")

// ==========================================
// 1. COMPONENTS
// ==========================================

// INTENSIVE HEADER STRAP
#let intensive_strap() = {
  align(center)[
    #image("/images/intensive-header.jpg", width: 100%)
  ]
  v(0.6cm)
}

// IDENTITY BLOCK
#let identity_block() = {
  block(width: 100%, inset: (bottom: 1em), [
    #grid(
      columns: (auto, 1fr, auto, 4cm),
      gutter: 1em,
      text(weight: "bold", fill: maroon)[Nickname:],
      line(start: (0pt, 0.8em), length: 100%, stroke: 0.5pt + black),
      text(weight: "bold", fill: maroon)[ID:],
      grid(
        columns: (1fr, 1fr, 1fr, 1fr, 1fr),
        gutter: 4pt,
        ..range(5).map(_ => box(width: 100%, height: 1.2em, stroke: (bottom: 1pt + black)))
      ),
    )
  ])
}

// SOURCE CODE BOX
#let source_code_box(content) = {
  block(
    width: 100%,
    fill: code-bg,
    stroke: 1pt + maroon,
    radius: 4pt,
    inset: 12pt,
    [
      #text(weight: "bold", fill: maroon)[MODEL CODE: Candidate C (Score 20/20)]
      #v(0.5em)
      #text(style: "italic")[#content]
    ],
  )
}

// ANALYSIS BOX
#let analysis_box(title, explanation, example) = {
  block(
    width: 100%,
    stroke: 0.5pt + slate-dark,
    radius: 4pt,
    inset: 10pt,
    below: 0.8cm,
    [
      #text(weight: "bold", fill: maroon)[#title]
      #v(0.2em)
      #text(size: 11pt)[#explanation]
      #v(0.5em)
      #line(length: 100%, stroke: 0.5pt + gray-line)
      #v(0.5em)
      #text(weight: "bold", size: 11pt)[Code Snippet:]
      #h(0.5em)
      #box(fill: rgb("#FFF1F2"), inset: 4pt, radius: 2pt)[#text(font: "Courier New", size: 10pt)[#example]]
    ],
  )
}

// TASK TASK BOX
#let task_card(title, prompt) = {
  block(
    width: 100%,
    stroke: 1.5pt + maroon,
    radius: 4pt,
    clip: true,
    below: 0.8cm,
    [
      #block(fill: maroon, width: 100%, inset: 10pt, [
        #text(fill: white, weight: "bold")[#title]
      ])
      #block(fill: white, inset: 12pt, width: 100%, [
        #text(size: 12pt)[#prompt]
      ])
    ],
  )
}

// WRITING LINES
#let writing_lines(count: 15) = {
  v(0.2cm)
  for _ in range(count) {
    line(length: 100%, stroke: 0.5pt + slate-dark)
    v(0.65cm)
  }
}

// ==========================================
// 2. DOCUMENT CONTENT
// ==========================================

// --- PAGE 1: THE SOURCE CODE ---
#intensive_strap()

#text(size: 18pt, weight: "bold", fill: maroon)[System Analysis: The 20/20 Article]
#v(0.4em)
#text[To build a high-performance Technology article, we first "Reverse Engineer" the model text below. Identify the snippets that make the examiner give it 20/20.]

#v(0.5cm)

#task_card(
  "THE ORIGINAL TASK: SOMETHING THAT MAKES YOU LAUGH",
  [
    Write an article for your school magazine about something that makes you laugh. Tell us what it is and why it makes you laugh. Is it important for people to laugh?
  ],
)

#v(0.2cm)

#source_code_box[
  "I love to watch comedies a lot because it makes me laugh. The comedy I love the most is the Chinese Running Man. I enjoy watching and laughing it with my family. In the show, famous actors and actresses must overcome some challenging quests, such as trading a coffee bean with someone else for something more expensive... The storylines are very interesting and they always tickle my funny bone. Laughing out loud is great! Laughing can help us to release stress and make us feel better. It may also make us more attractive too!"
]

// --- PAGE 2: THE CODE PATCHES (ANALYSIS) ---
#pagebreak()

#text(size: 18pt, weight: "bold", fill: maroon)[Code Snippet Analysis]
#v(0.8cm)

#analysis_box(
  "Logic Patch 1: The Specific Intro",
  "Upgrade your opening by using superlative focus. Don't just list what you like—identify the 'main' choice.",
  "The [Topic] I love/use the most is...",
)

#analysis_box(
  "Logic Patch 2: Functional Complexity",
  "Use 'must overcome + such as' to link a requirement with a specific, detailed example.",
  "Users must overcome complex issues, such as [Specific Detail].",
)

#analysis_box(
  "Logic Patch 3: The Balanced Output",
  "End with a 'Resolution' that shows a wider view of technology, balancing positive and negative impacts.",
  "It allows us to [positive], but it may also make us [negative] too!",
)

// --- PAGE 3: THE TECH CHALLENGE ---
#pagebreak()

#task_card(
  "MISSION: TECHNOLOGY AND YOU",
  [
    *Articles wanted!* \ \
    Write an article telling us which website or app you like the most and how often you use it. \ \
    Do you think it is important for teenagers to have a computer? Why?
  ],
)

// --- PAGE 4: PRODUCTION ---
#pagebreak()

#identity_block()

#text(weight: "bold", fill: maroon)[Your Output (Clean Architecture):]
#v(0.2cm)
#text(size: 10pt, style: "italic")[Apply your Code Snippets to Paragraph 2 & 3.]

#writing_lines(count: 18) // Reduced count to guarantee no overflow to P5

#v(1fr)
#align(center)[#text(size: 9pt, fill: slate-dark)[Bell Language Centre | Intensive Program | 2026]]

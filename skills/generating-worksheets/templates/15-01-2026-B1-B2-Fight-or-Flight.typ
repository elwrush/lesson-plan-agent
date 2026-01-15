
// ============================================================
// WORKSHEET: FIGHT OR FLIGHT (B1/B2 Reading)
// ============================================================

#set page(
  paper: "a4",
  margin: (top: 1.5cm, bottom: 2cm, x: 2cm),
)
#set text(font: "Arial", size: 12pt, fill: rgb("#333333"))
#set par(leading: 0.65em, justify: true)

// BRAND COLORS
#let maroon = rgb("#8B1538")
#let slate-dark = rgb("#334155")
#let gray-line = rgb("#E0E0E0")

// ==========================================
// 1. COMPONENTS
// ==========================================

#let integrated_header(title) = {
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
  v(0.4cm)
}

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

#let task_card(number, title, prompt) = {
  v(0.5cm)
  block(width: 100%, [
    #text(weight: "bold", fill: maroon, size: 12pt)[TASK #number: #title]
    #v(0.2em)
    #text(style: "italic", fill: slate-dark)[#prompt]
    #v(0.4em)
  ])
}

// ==========================================
// 2. DOCUMENT LAYOUT
// ==========================================

#integrated_header("FIGHT OR FLIGHT")

#task_card(1, "Before you read", "Discuss these questions with a partner.")
1. What fears do your friends and family have?
2. What reactions do they have to their fears?

#v(0.5cm)

#align(center)[#image("/images/title_graphic_final.png", width: 8cm)]

#v(0.5cm)

#import "@preview/meander:0.3.1"

#meander.reflow({
  import meander: *

  // Centered image block inset between columns
  // Pushed down to allow text flow above
  placed(
    center + top,
    dy: 4.5cm,
    block(
      width: 5cm,
      stroke: 2pt + maroon,
      inset: 24pt,
      fill: white,
      image("/images/thai_student_fight_flight_transparent.png", width: 100%),
    ),
  )

  // Thread text through two columns side-by-side
  container(width: 8cm) // Left column, page 1
  container(width: 8cm, dx: 8.5cm) // Right column, page 1
  container(width: 8cm) // Left column, page 2
  container(width: 8cm, dx: 8.5cm) // Right column, page 2

  content[
    #text(weight: "bold")[1] Most people connect fear with negative feelings, but it can actually be very positive as well. Fear is natural and something we are born with. We have always needed it to keep us safe from danger. If we face a dangerous situation, we can find abilities that we often do not know we have.

    #v(0.4em)

    #text(weight: "bold")[2] In the past, humans faced danger every day so they learned to respond to it straight away to stay alive. This natural reaction can also be seen in many animals. Take cuttlefish, an animal in the same family as a squid and octopus. These creatures have an amazing ability to change color and shape. They use this to both fight and escape. With the help of their bright colors, they make other fish slower and easier to catch. Their color also helps them to hide in their environment. Another fish, the electric eel, uses its electric shock to catch food and for self-defense, as an action to protect itself from others. Humans might not have such unusual responses but they do still have a fight or flight instinct, which is the body's natural way of keeping us safe by either facing the danger or getting away from it as quickly as possible.

    #v(0.4em)

    #text(weight: "bold")[3] Our bodies react in a number of different ways when we are in a dangerous situation. For example, our reactions often become faster, we become stronger and have more energy. Under pressure we become nervous and some simple skills such as putting a key in a door often become worse. However, physical abilities such as running and jumping tend to improve. If an angry dog chases you, you will probably run away from it faster. In a normal situation we often only use 65% of our strength, but studies have shown that this can increase to as much as 85% in more dangerous situations.

    #v(0.4em)

    #text(weight: "bold")[4] So how does our body create such a reaction? Fear is a natural reaction in the brain to an external stressful or dangerous situation and is the body's internal way of trying to stay calm. Hormones are released that cause our heart to beat faster and our breathing to become quicker. This response is known as the fight or flight response and it makes it difficult to remain calm. Instead, you might run away or fight the situation that scared you.

    #v(0.4em)

    #text(weight: "bold")[5] In biology, the brain causes the body to release over 30 different hormones, such as adrenaline, a chemical that gives you more energy when frightened, excited, or angry, to help keep us safe. These hormones cause a range of reactions. Some senses such as our eyes change to let more light in. Some of our body relaxes to let more air in. Other parts of the body become tense because of the adrenaline and glucose, a sugar produced in the body. More blood is sent to our muscles and organs, for example, the heart and other parts of the body that do specific jobs to keep us alive. We often feel cold and connect fear with being cold because our bodies are keeping us and our organs safe, instead of keeping us warm. It is also why we feel tired when we recover from a shock. Fear is designed to protect us.

    #v(0.4em)

    #text(weight: "bold")[6] Although we might not face as many physical dangers today as we did in the past, fear still helps to keep us safe. It stops us from doing stupid things, like walking out into a busy road or not being careful on a high building. It limits the risks that we are willing to take. However, these limits may also take away some opportunities in our lives. One common fear is a fear of failure. Many people are not willing to take risks because they are too scared of failing. This fear can lead to people not taking good chances. The risk of making a mistake is minimized, but it also means people are less likely to try new things and may achieve less. This desire to avoid failure can make people act differently to when they feel more confident.

    #v(0.4em)

    #text(weight: "bold")[7] While fear may make people work slowly, and even limit opportunities in life, it can also make us better at certain things. People who experience fear often are usually better at making decisions as they understand the risk more quickly. If people always only see the positives in things, they may not pay attention to negative information they receive. As a result, this can make them poor decision makers.

    #v(0.4em)

    #text(weight: "bold")[8] When we combine anxiety and fear with training, the results can be even more positive. If we are well-trained and prepared, we can react to stressful situations in a normal and calm way. Fear and adrenaline from the fight or flight instinct make you quick to respond to things while training means you know what to do. This is why emergency professionals train for a wide range of situations and can remain calm when most of us would panic. Fear can be used to your advantage as long as you plan ahead and do your research.
  ]
})

#v(0.5cm)
#image("/images/ekg_ultrawide_trimmed.png", width: 100%)
#v(0.5cm)

#task_card(
  2,
  "Global Reading",
  "Skim each paragraph in the text and identify in which paragraph you could find the information to answer these questions.",
)
#grid(
  columns: (1fr, auto),
  // Ensure no forced itemization
  gutter: 1cm,
  // Column gutter
  row-gutter: 1cm,
  // Row gutter for writing space

  [1. What is the body naturally trying to do when we feel fear?],
  [Para: #box(width: 2cm, height: 1em, stroke: (bottom: 0.5pt))],

  [2. What things can fear stop us doing today?], [Para: #box(width: 2cm, height: 1em, stroke: (bottom: 0.5pt))],

  [3. Which animal changes color to keep it safe?], [Para: #box(width: 2cm, height: 1em, stroke: (bottom: 0.5pt))],

  [4. What can fear make us better at?], [Para: #box(width: 2cm, height: 1em, stroke: (bottom: 0.5pt))],

  [5. What happens to our reactions when we are in danger?],
  [Para: #box(width: 2cm, height: 1em, stroke: (bottom: 0.5pt))],

  [6. How can training help us deal with situations many fear?],
  [Para: #box(width: 2cm, height: 1em, stroke: (bottom: 0.5pt))],

  [7. How do biology and hormones affect our eyes when we are in danger?],
  [Para: #box(width: 2cm, height: 1em, stroke: (bottom: 0.5pt))],
)

#v(0.5cm)
#align(center)[#image("/images/ekg_ultrawide_trimmed.png", width: 4cm)]
#v(0.5cm)

#pagebreak()
#v(0.4cm)
#stack(
  dir: ltr,
  spacing: 1em,
  text(weight: "bold", fill: maroon, size: 14pt)[FIGHT OR FLIGHT],
  align(horizon)[#image("/images/ekg_ultrawide_trimmed.png", height: 0.8cm)],
)
#v(0.2cm)

#task_card(3, "Close Reading & Vocabulary", "Read the text again and complete the following activities.")

#block(
  width: 100%,
  inset: 12pt,
  fill: rgb("#FFFBEB"),
  stroke: 1pt + rgb("#FBBF24"),
  radius: 4pt,
  [
    #text(weight: "bold")[Reading Tip: Finding Meaning] \
    While it is often possible to use the context of a paragraph to find the meaning of new words, sometimes unusual words are defined in the text. This is often true if the words are very specific and unlikely to be known, for example with scientific vocabulary. There might be full definitions where the meaning of the word is explained, e.g. \
    _When an animal is scared, it will try to escape, *get away from something*._ \
    Or the new words can be defined using examples: \
    _In an emergency it is important to have a calm reaction, like *speaking softly to someone who is hurt*._
  ],
)

#v(0.6cm)

*Find the definitions for the following words in the text:*

#grid(
  columns: (auto, 1fr),
  row-gutter: 1.5cm,
  gutter: 1em,
  // Space between word and line

  [1. self-defense:], [#align(horizon)[#line(length: 100%, stroke: 0.5pt + gray.lighten(40%))]],
  [2. fight or flight instinct:], [#align(horizon)[#line(length: 100%, stroke: 0.5pt + gray.lighten(40%))]],
  [3. physical abilities:], [#align(horizon)[#line(length: 100%, stroke: 0.5pt + gray.lighten(40%))]],
  [4. adrenaline:], [#align(horizon)[#line(length: 100%, stroke: 0.5pt + gray.lighten(40%))]],
  [5. glucose:], [#align(horizon)[#line(length: 100%, stroke: 0.5pt + gray.lighten(40%))]],
  [6. organs:], [#align(horizon)[#line(length: 100%, stroke: 0.5pt + gray.lighten(40%))]],
)

#v(0.4cm)
#text(style: "italic", fill: slate-dark)[Discuss the meaning of these words with your partner.]

#v(1cm)

#pagebreak()
#task_card(4, "Critical Thinking", "Discuss or write your answers to the following questions.")
#v(0.5cm)
#identity_block()
#v(0.5cm)

1. "Fight or flight" claims that fear can stop us from taking risks. Do you think avoiding risk is a good or bad thing?

2. Do you agree that fear stops people from achieving what they want to? What examples can you think of?
#v(1.5cm)
#grid(
  rows: 10,
  row-gutter: 1.5cm,
  ..range(10).map(_ => line(length: 100%, stroke: 0.5pt + gray))
)


#pagebreak()
#v(0.4cm)
#stack(
  dir: ltr,
  spacing: 1em,
  text(weight: "bold", fill: maroon, size: 14pt)[ANSWER KEY],
  align(horizon)[#image("/images/ekg_ultrawide_trimmed.png", height: 0.8cm)],
)
#v(0.2cm)

#text(weight: "bold", size: 14pt, fill: maroon)[Answer Key]

#v(0.5cm)

*Task 2: Global Reading*
1. Para 4 (trying to stay calm)
2. Para 6 (stops us from doing stupid things / taking risks)
3. Para 2 (cuttlefish)
4. Para 7 (making decisions / understanding risk)
5. Para 3 (become faster, stronger, more energy)
6. Para 8 (react in a normal and calm way)
7. Para 5 (change to let more light in)

#v(0.5cm)

*Task 3: Close Reading & Vocabulary*
1. self-defense: an action to protect itself from others (Para 2)
2. fight or flight instinct: the body's natural way of keeping us safe by either facing the danger or getting away from it as quickly as possible (Para 2)
3. physical abilities: such as running and jumping (Para 3)
4. adrenaline: a chemical that gives you more energy when frightened, excited, or angry (Para 5)
5. glucose: a sugar produced in the body (Para 5)
6. organs: parts of the body that do specific jobs to keep us alive (Para 5)

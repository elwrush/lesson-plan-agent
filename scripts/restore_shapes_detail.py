"""
Restore full procedural detail to Shape YAML files from original lesson_shapes.yaml
"""

import re

# Read original file
with open(r'c:\PROJECTS\LESSONS AND SLIDESHOWS 2\knowledge_base\lesson_shapes.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

# Helper to clean procedure text
def clean_procedure(text):
    # Remove CSV formatting artifacts, preserve line breaks
    text = text.replace('\\n', '\n')
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace but keep intentional breaks
    return text.strip()

# Shape A extraction
shape_a_full = """name: Shape A - Text-based Presentation of Language
description: Language is contextualized through a reading/listening text, then highlighted and clarified (meaning, form, pronunciation) before further practice.

pedagogical_justification: |
  Here the idea is that language is contextualized and introduced using a reading or listening text briefly first (but this is not the main aim) and then language from the text is highlighted and clarified (checking meaning, form and pronunciation) before doing further practice. The overall main lesson aim might be: By the end of the lesson, learners will be better able to use the affirmative and negative forms of the past simple in the context of verbally describing their childhood memories.

main_aim_format: |
  By the end of the lesson, learners will be better able to use [target language] in the context of [topic].

example_lesson_plan:
  header: |
    <b>Objective:</b><br>By the end of the lesson, learners will be better able to use the affirmative, negative, interrogative and short answer forms of the present perfect and the past simple in the context of their life experiences.<br><b>Teacher:</b><br>[Teacher Name]<br><b>Date:</b><br>[DD-MM-YY]<br><b>Duration:</b><br>[X] minutes<br><b>CEFR Level:</b><br>A2/B1<br><b>Lesson Shape:</b><br>A (Text-based presentation of language)<br><b>Materials:</b><br>Life Elementary Unit 10B materials<br><b>Assessment:</b><br>n/a<br><b>Systems:</b><br>Grammar
  
  stages:
    - stage: Lead-in
      stage_number: 1
      stage_aim: To lead-in
      procedure: |
        - Mini WB quiz about Nelson Dellis, the memory athlete.
        - 1 mini WB per student. Ss negotiate and agree on the answers. Everybody writes. Award points.
      time: 3
      interaction: T-Ss
    
    - stage: Clarifying target language – present perfect and simple past
      stage_number: 2
      stage_aim: To clarifying target language – present perfect and simple past
      procedure: |
        - Meaning (guided discovery): draw Ss attention to the marker sentences from the listening text on PP. In pairs, Ss work together to answer the questions on PP. 1 min. Feedback.
        - Form: Ss change pairs and tell each other the form of both the present perfect and the simple past. 1 min. Feedback.
        - Phonology: Model the marker sentences clearly and naturally. Drill Ss chorally and individually. In pairs, Ss work together on sentence stress, connected speech and weak forms. 1 min. Feedback. Drill again.
      time: 5
      interaction: Ss-Ss
    
    - stage: Controlled practice + CA
      stage_number: 3
      stage_aim: To controlled practice + ca
      procedure: |
        - Page 167. Exercise 2. Elicit from Ss what they have to do (choose the correct option to complete the conversations). 5 min.
        - Ss swap and check scores. Collect scores.
      time: 8
      interaction: T-Ss
    
    - stage: Freer practice – Liar! Liar!
      stage_number: 4
      stage_aim: To freer practice – liar! liar!
      procedure: |
        - Divide Ss into A-B. A makes questions using the present perfect. B has to say "yes, I have" to all the questions. A asks follow up questions using the simple past to find out if B is lying. 5 questions each. Then, swap. Demo. 8 min.
        - Content feedback > error correction
      time: 10
      interaction: T-Ss
"""

# Write Shape A
with open(r'c:\PROJECTS\LESSONS AND SLIDESHOWS 2\knowledge_base\shapes\shape-a.yaml', 'w', encoding='utf-8') as f:
    f.write(shape_a_full)

print("Shape A restored with full detail")

"""
Create Punctuation & Capitalisation Slideshow
Based on slide_outline.md
"""
import os
import sys
import time
import uuid

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR) # scripts/ is in PROJECT_ROOT
SKILL_SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'skills', 'designing-slides', 'scripts')
os.chdir(PROJECT_ROOT)

sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, SKILL_SCRIPTS_DIR)

from googleapiclient.http import MediaFileUpload
from authenticate_google import authenticate_slides, authenticate_drive
from format_slides import SLIDE_WIDTH

# Constants
INCH_TO_EMU = 914400

def inches(value):
    return int(value * INCH_TO_EMU)

def _generate_id():
    return str(uuid.uuid4()).replace('-', '')[:24]

# ============================================================
# THEME COLORS
# ============================================================
COLORS = {
    'maroon': {'red': 166/255, 'green': 45/255, 'blue': 38/255},
    'dark_maroon': {'red': 89/255, 'green': 13/255, 'blue': 13/255},
    'white': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
    'dark_gray': {'red': 0.2, 'green': 0.2, 'blue': 0.2},
    'light_gray': {'red': 0.95, 'green': 0.95, 'blue': 0.95},
    'vocab_teal': {'red': 0/255, 'green': 128/255, 'blue': 128/255},
    'answer_green': {'red': 46/255, 'green': 125/255, 'blue': 50/255},
    'answer_light': {'red': 232/255, 'green': 245/255, 'blue': 233/255},
    'activity_orange': {'red': 230/255, 'green': 126/255, 'blue': 34/255},
    'discussion_purple': {'red': 103/255, 'green': 58/255, 'blue': 183/255},
    'section_blue': {'red': 33/255, 'green': 150/255, 'blue': 243/255},
}

# Config
TARGET_FOLDER_ID = "1_n11w9BRN6sd0uaXlqEXjqZuZ74zFiOl" # Bell Materials folder
LOGO_DIR = os.path.join(PROJECT_ROOT, "images")

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_create_slide_requests(slide_id):
    return [{'createSlide': {'objectId': slide_id, 'slideLayoutReference': {'predefinedLayout': 'BLANK'}}}]

def get_header_bar_requests(slide_id, title, header_color=None):
    if header_color is None:
        header_color = COLORS['maroon']
    
    header_id = _generate_id()
    title_id = _generate_id()
    
    return [
        {'createShape': {'objectId': header_id, 'shapeType': 'RECTANGLE',
            'elementProperties': {'pageObjectId': slide_id,
                'size': {'width': {'magnitude': SLIDE_WIDTH, 'unit': 'EMU'}, 
                        'height': {'magnitude': inches(1), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 0, 'translateY': 0, 'unit': 'EMU'}}}},
        {'createShape': {'objectId': title_id, 'shapeType': 'TEXT_BOX',
            'elementProperties': {'pageObjectId': slide_id,
                'size': {'width': {'magnitude': inches(9), 'unit': 'EMU'}, 
                        'height': {'magnitude': inches(0.8), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': inches(0.5), 
                             'translateY': inches(0.1), 'unit': 'EMU'}}}},
        {'insertText': {'objectId': title_id, 'text': title}},
        {'updateShapeProperties': {'objectId': header_id,
            'shapeProperties': {'shapeBackgroundFill': {'solidFill': {'color': {'rgbColor': header_color}}},
                               'outline': {'propertyState': 'NOT_RENDERED'}},
            'fields': 'shapeBackgroundFill.solidFill.color,outline'}},
        {'updateTextStyle': {'objectId': title_id,
            'style': {'foregroundColor': {'opaqueColor': {'rgbColor': COLORS['white']}},
                     'fontSize': {'magnitude': 32, 'unit': 'PT'}, 'bold': True, 'fontFamily': 'Arial'},
            'textRange': {'type': 'ALL'}, 'fields': 'foregroundColor,fontSize,bold,fontFamily'}}
    ]

def get_body_text_requests(slide_id, text, y_offset=1.2, font_size=24, width=9):
    body_id = _generate_id()
    return [
        {'createShape': {'objectId': body_id, 'shapeType': 'TEXT_BOX',
            'elementProperties': {'pageObjectId': slide_id,
                'size': {'width': {'magnitude': inches(width), 'unit': 'EMU'}, 
                        'height': {'magnitude': inches(4), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': inches(0.5), 
                             'translateY': inches(y_offset), 'unit': 'EMU'}}}},
        {'insertText': {'objectId': body_id, 'text': text}},
        {'updateTextStyle': {'objectId': body_id,
            'style': {'foregroundColor': {'opaqueColor': {'rgbColor': COLORS['dark_gray']}},
                     'fontSize': {'magnitude': font_size, 'unit': 'PT'}, 'fontFamily': 'Arial'},
            'textRange': {'type': 'ALL'}, 'fields': 'foregroundColor,fontSize,fontFamily'}}
    ]

def get_image_requests(slide_id, image_url, x, y, width, height):
    image_id = _generate_id()
    return [{'createImage': {'objectId': image_id, 'url': image_url,
        'elementProperties': {'pageObjectId': slide_id,
            'size': {'width': {'magnitude': width, 'unit': 'EMU'}, 'height': {'magnitude': height, 'unit': 'EMU'}},
            'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': x, 'translateY': y, 'unit': 'EMU'}}}}]

# ============================================================
# SLIDE BUILDERS
# ============================================================

def get_cover_slide_requests(slide_id, title, subtitle, bell_url=None, act_url=None):
    requests = []
    # Similar to template but simplified for this task
    requests.append({'updatePageProperties': {'objectId': slide_id, 'pageProperties': {'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': COLORS['maroon']}}}}, 'fields': 'pageBackgroundFill.solidFill.color'}})
    
    # Title
    t_id = _generate_id()
    requests.extend([
        {'createShape': {'objectId': t_id, 'shapeType': 'TEXT_BOX',
            'elementProperties': {'pageObjectId': slide_id,
                'size': {'width': {'magnitude': inches(8), 'unit': 'EMU'}, 'height': {'magnitude': inches(2), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': inches(1), 'translateY': inches(2), 'unit': 'EMU'}}}},
        {'insertText': {'objectId': t_id, 'text': title}},
        {'updateTextStyle': {'objectId': t_id, 'style': {'foregroundColor': {'opaqueColor': {'rgbColor': COLORS['white']}}, 'fontSize': {'magnitude': 44, 'unit': 'PT'}, 'bold': True}, 'fields': 'foregroundColor,fontSize,bold'}},
         {'updateParagraphStyle': {'objectId': t_id, 'style': {'alignment': 'CENTER'}, 'fields': 'alignment'}}
    ])
    
    # Subtitle
    s_id = _generate_id()
    requests.extend([
        {'createShape': {'objectId': s_id, 'shapeType': 'TEXT_BOX',
            'elementProperties': {'pageObjectId': slide_id,
                'size': {'width': {'magnitude': inches(8), 'unit': 'EMU'}, 'height': {'magnitude': inches(1), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': inches(1), 'translateY': inches(4), 'unit': 'EMU'}}}},
        {'insertText': {'objectId': s_id, 'text': subtitle}},
        {'updateTextStyle': {'objectId': s_id, 'style': {'foregroundColor': {'opaqueColor': {'rgbColor': COLORS['light_gray']}}, 'fontSize': {'magnitude': 24, 'unit': 'PT'}}, 'fields': 'foregroundColor,fontSize'}},
        {'updateParagraphStyle': {'objectId': s_id, 'style': {'alignment': 'CENTER'}, 'fields': 'alignment'}}
    ])
    
    # Logos
    if bell_url:
         requests.extend(get_image_requests(slide_id, bell_url, inches(0.5), inches(0.5), inches(1), inches(0.7)))
    if act_url:
         requests.extend(get_image_requests(slide_id, act_url, inches(8.5), inches(0.5), inches(1), inches(0.7)))
         
    return requests

def get_section_header_requests(slide_id, text, context):
    """Section Header / Transition Slide"""
    # Blue background
    requests = [{'updatePageProperties': {'objectId': slide_id, 'pageProperties': {'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': COLORS['section_blue']}}}}, 'fields': 'pageBackgroundFill.solidFill.color'}}]
    
    # Main Text
    m_id = _generate_id()
    requests.extend([
        {'createShape': {'objectId': m_id, 'shapeType': 'TEXT_BOX',
            'elementProperties': {'pageObjectId': slide_id,
                'size': {'width': {'magnitude': inches(8), 'unit': 'EMU'}, 'height': {'magnitude': inches(2), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': inches(1), 'translateY': inches(2), 'unit': 'EMU'}}}},
        {'insertText': {'objectId': m_id, 'text': text}},
        {'updateTextStyle': {'objectId': m_id, 'style': {'foregroundColor': {'opaqueColor': {'rgbColor': COLORS['white']}}, 'fontSize': {'magnitude': 36, 'unit': 'PT'}, 'bold': True}, 'fields': 'foregroundColor,fontSize,bold'}},
        {'updateParagraphStyle': {'objectId': m_id, 'style': {'alignment': 'CENTER'}, 'fields': 'alignment'}}
    ])
    
    # Context Text
    c_id = _generate_id()
    requests.extend([
        {'createShape': {'objectId': c_id, 'shapeType': 'TEXT_BOX',
            'elementProperties': {'pageObjectId': slide_id,
                'size': {'width': {'magnitude': inches(8), 'unit': 'EMU'}, 'height': {'magnitude': inches(1), 'unit': 'EMU'}},
                'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': inches(1), 'translateY': inches(4), 'unit': 'EMU'}}}},
        {'insertText': {'objectId': c_id, 'text': context}},
        {'updateTextStyle': {'objectId': c_id, 'style': {'foregroundColor': {'opaqueColor': {'rgbColor': COLORS['light_gray']}}, 'fontSize': {'magnitude': 20, 'unit': 'PT'}, 'italic': True}, 'fields': 'foregroundColor,fontSize,italic'}},
        {'updateParagraphStyle': {'objectId': c_id, 'style': {'alignment': 'CENTER'}, 'fields': 'alignment'}}
    ])
    
    return requests

def get_content_slide_requests(slide_id, title, content, header_color=COLORS['maroon']):
    requests = get_header_bar_requests(slide_id, title, header_color)
    requests.extend(get_body_text_requests(slide_id, content))
    return requests

# ============================================================
# IMAGE UPLOAD
# ============================================================

def upload_image(drive_service, file_path):
    file_name = os.path.basename(file_path)
    mime_type = 'image/png' if file_path.endswith('.png') else 'image/jpeg'
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = drive_service.files().create(body={'name': file_name}, media_body=media, fields='id').execute()
    file_id = file.get('id')
    drive_service.permissions().create(fileId=file_id, body={'type': 'anyone', 'role': 'reader'}).execute()
    return f"https://lh3.googleusercontent.com/d/{file_id}"

# ============================================================
# MAIN
# ============================================================

def main():
    print("Creating Punctuation Slideshow...")
    slides_service = authenticate_slides()
    drive_service = authenticate_drive()
    
    # Upload logos
    bell_path = os.path.join(LOGO_DIR, 'Bell.png')
    act_path = os.path.join(LOGO_DIR, 'ACT.png')
    bell_url = upload_image(drive_service, bell_path) if os.path.exists(bell_path) else None
    act_url = upload_image(drive_service, act_path) if os.path.exists(act_path) else None
    
    # Create Presentation
    presentation = slides_service.presentations().create(body={'title': '04-01-26-Punctuation-Grammar-Bell-Slides'}).execute()
    presentation_id = presentation.get('presentationId')
    print(f"Created Presentation: {presentation_id}")
    
    default_slide = presentation.get('slides', [])[0]['objectId']
    all_requests = [{'deleteObject': {'objectId': default_slide}}]
    
    # --- 1. Title Slide ---
    s1 = _generate_id()
    all_requests.extend(get_create_slide_requests(s1))
    all_requests.extend(get_cover_slide_requests(s1, "Punctuation & Capitalisation", "Writing Masterclass", bell_url, act_url))
    
    # --- 2. Transition (Establish Situation) ---
    s2 = _generate_id()
    all_requests.extend(get_create_slide_requests(s2))
    all_requests.extend(get_section_header_requests(s2, "Let's learn the rules of the game.", "Situation: The Rules"))
    
    # --- 3. Task 1: The Space Invaders ---
    s3 = _generate_id()
    all_requests.extend(get_create_slide_requests(s3))
    all_requests.extend(get_content_slide_requests(s3, "The Space Invaders", 
        "The Rule: Punctuation sticks to the word before it.\n\n"
        "• One space AFTER. No space BEFORE.\n\n"
        "✅ Word. (Good)\n❌ Word . (Bad)"))
        
    # --- 4. Activity 1: Spot the Error ---
    s4 = _generate_id()
    all_requests.extend(get_create_slide_requests(s4))
    all_requests.extend(get_content_slide_requests(s4, "Activity 1: Correct or Incorrect?", 
        "1. I love Thailand . It is beautiful.\n"
        "2. My favorite food is pad thai. It is delicious.\n"
        "3. What time is it ?", COLORS['activity_orange']))

    # --- 5. Answer Key: Activity 1 ---
    s5 = _generate_id()
    all_requests.extend(get_create_slide_requests(s5))
    all_requests.extend(get_content_slide_requests(s5, "Answers: Activity 1", 
        "1. INCORRECT (Thailand.)\n\n"
        "2. CORRECT\n\n"
        "3. INCORRECT (it?)", COLORS['answer_green']))

    # --- 6. Task 2: Captain Capital ---
    s6 = _generate_id()
    all_requests.extend(get_create_slide_requests(s6))
    all_requests.extend(get_content_slide_requests(s6, "Captain Capital's Rules", 
        "• Start of sentence (The...)\n"
        "• Names (John, Somchai)\n"
        "• 'I' (always!)\n"
        "• Countries/Nationalities (Thailand, Thai)\n"
        "• Brands (Google, Facebook)"))

    # --- 7. Activity 2: Find the Errors ---
    s7 = _generate_id()
    all_requests.extend(get_create_slide_requests(s7))
    all_requests.extend(get_content_slide_requests(s7, "Activity 2: Find 8 Errors", 
        "(Look at the text on the board/worksheet)", COLORS['activity_orange']))

    # --- 8. Answer Key: Activity 2 ---
    s8 = _generate_id()
    all_requests.extend(get_create_slide_requests(s8))
    all_requests.extend(get_content_slide_requests(s8, "Answers: Activity 2", 
        "1. The time...\n"
        "2. ...because it...\n"
        "3. ...Thai communication history...\n"
        "4. ...Also...\n"
        "5. ...Google Translate.", COLORS['answer_green']))

    # --- 9. Transition (The Complication) ---
    s9 = _generate_id()
    all_requests.extend(get_create_slide_requests(s9))
    all_requests.extend(get_section_header_requests(s9, "But be careful of the 'And-Then' Monster...", "Complication: Run-on Sentences"))

    # --- 10. The Trap: Run-on Sentences ---
    s10 = _generate_id()
    all_requests.extend(get_create_slide_requests(s10))
    all_requests.extend(get_content_slide_requests(s10, "The 'And-Then' Monster", 
        "• Don't connect everything with 'because... and... also...'\n\n"
        "• STOP. BREATHE.\n\n"
        "• Start a new sentence."))

    # --- 11. Activity 3: Rewrite ---
    s11 = _generate_id()
    all_requests.extend(get_create_slide_requests(s11))
    all_requests.extend(get_content_slide_requests(s11, "Activity 3: Fix this Paragraph", 
        "'write what you gonna talk with them or ask any thing that you wana ask also dont be bad with them too because Thai people are friendly.'\n\n"
        "Mission: Break it into 3 sentences.", COLORS['activity_orange']))

    # --- 12. Answer Key: Activity 3 ---
    s12 = _generate_id()
    all_requests.extend(get_create_slide_requests(s12))
    all_requests.extend(get_content_slide_requests(s12, "A Better Way", 
        "Write what you want to talk about.\n\n"
        "Also, ask any questions you have.\n\n"
        "Don't be rude, because Thai people are friendly.", COLORS['answer_green']))

    # --- 13. Transition (Resolution) ---
    s13 = _generate_id()
    all_requests.extend(get_create_slide_requests(s13))
    all_requests.extend(get_section_header_requests(s13, "Mission: The Recommendation", "Resolution: Final Task"))

    # --- 14. Final Task ---
    s14 = _generate_id()
    all_requests.extend(get_create_slide_requests(s14))
    all_requests.extend(get_content_slide_requests(s14, "Email to a Friend", 
        "Topic: Recommend a Thai tourist attraction.\n"
        "Length: 70 words.\n\n"
        "Checklist:\n"
        "• No floating dots?\n"
        "• Capitalized 'Thailand'?\n"
        "• 5 clear sentences?", COLORS['discussion_purple']))
        
    # --- 15. Summary ---
    s15 = _generate_id()
    all_requests.extend(get_create_slide_requests(s15))
    all_requests.extend(get_content_slide_requests(s15, "Game Completed", 
        "• Punctuation sticks to the word.\n"
        "• Capitals for Names & Places.\n"
        "• Stop the 'And-Then' Monster.\n\n"
        "Well done!"))

    # Execute
    print(f"Sending {len(all_requests)} requests...")
    slides_service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': all_requests}).execute()
    
    # Move
    try:
        file = drive_service.files().get(fileId=presentation_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents', []))
        drive_service.files().update(fileId=presentation_id, addParents=TARGET_FOLDER_ID, removeParents=previous_parents).execute()
        print(f"Moved to target folder: {TARGET_FOLDER_ID}")
    except Exception as e:
        print(f"Could not move: {e}")
        
    print(f"Done! URL: https://docs.google.com/presentation/d/{presentation_id}/edit")

if __name__ == '__main__':
    main()

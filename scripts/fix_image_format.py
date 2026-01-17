
import os
from PIL import Image

image_path = "C:/PROJECTS/LESSONS AND SLIDESHOWS 2/images/thai_student_fight_flight.png"

try:
    with Image.open(image_path) as img:
        print(f"Format: {img.format}")
        if img.format != "PNG":
            print(f"Converting {img.format} to PNG...")
            img.save(image_path, "PNG")
            print("Conversion complete.")
        else:
            print("File is already a valid PNG.")
except Exception as e:
    print(f"Error: {e}")

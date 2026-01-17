
from PIL import Image
import os

def set_transparency(path, out_path, tolerance=30):
    img = Image.open(path).convert("RGBA")
    width, height = img.size
    
    # Sample top-left corner for background color
    bg_color = img.getpixel((0, 0))
    tr, tg, tb, ta = bg_color
    
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            # Euclidean distance to bg color
            dist = ((r - tr)**2 + (g - tg)**2 + (b - tb)**2)**0.5
            if dist < tolerance:
                pixels[x, y] = (tr, tg, tb, 0)
    
    img.save(out_path)
    print(f"Saved transparent image to {out_path}")

set_transparency("images/thai_student_fight_flight.png", "images/thai_student_fight_flight_transparent.png")

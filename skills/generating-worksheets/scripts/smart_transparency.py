from PIL import Image
import os

def analyze_and_clear(path, tolerance=50):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    
    img = Image.open(path).convert("RGBA")
    width, height = img.size
    
    # Get corner pixel (typically background)
    corner_pixel = img.getpixel((0, 0))
    print(f"Analyzing {path}: Corner Pixel = {corner_pixel}")
    
    # Target color
    tr, tg, tb, ta = corner_pixel
    
    pixels = img.load()
    new_img = Image.new("RGBA", img.size)
    new_pixels = new_img.load()
    
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            # distance check
            dist = ((r - tr)**2 + (g - tg)**2 + (b - tb)**2)**0.5
            if dist < tolerance:
                new_pixels[x, y] = (tr, tg, tb, 0) # Transparent
            else:
                new_pixels[x, y] = (r, g, b, a)
                
    out_path = path.replace(".png", "_fixed.png")
    new_img.save(out_path)
    print(f"Saved to {out_path}")

images = [
    "images/ACT.png",
    "images/hook_icon.png",
    "images/story_arc_icon.png",
    "images/microphone_icon.png",
    "images/Bell.png"
]

for img_path in images:
    analyze_and_clear(img_path)

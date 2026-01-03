from PIL import Image
import sys
import os

def remove_white_background(input_path, output_path, tolerance=30):
    try:
        from PIL import Image, ImageChops
        img = Image.open(input_path).convert("RGBA")
        
        # Create a mask for anything that is white-ish
        # We can use the brightness or just check R,G,B
        # A more robust way in PIL:
        r, g, b, a = img.split()
        
        # Binary mask: 255 (white) if pixel is white-ish, else 0 (black)
        # We'll consider white as anything where R, G, B are all > (255 - tolerance)
        mask = Image.new("L", img.size, 0)
        pixels = img.load()
        mask_pixels = mask.load()
        
        width, height = img.size
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                if pixel[0] > (255 - tolerance) and pixel[1] > (255 - tolerance) and pixel[2] > (255 - tolerance):
                    mask_pixels[x, y] = 255 # Mark as background
        
        # Invert mask: Background becomes black (0), foreground white (255)
        mask = ImageChops.invert(mask)
        
        # Put mask into alpha channel
        img.putalpha(mask)
        
        img.save(output_path, "PNG")
        print(f"Created transparent image: {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python make_transparent.py <input> <output>")
        sys.exit(1)
    
    remove_white_background(sys.argv[1], sys.argv[2])

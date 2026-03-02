import argparse
from PIL import Image
import os
import sys

def resize_image(input_path, output_path=None, max_width=1920, max_height=1080, quality=85):
    """
    Resizes an image to fit within max_width and max_height while maintaining aspect ratio.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return False

    try:
        img = Image.open(input_path)
        
        # Calculate new dimensions
        width, height = img.size
        aspect_ratio = width / height
        
        if width > max_width or height > max_height:
            if width / max_width > height / max_height:
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
                
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            print(f"Resized {input_path} from {width}x{height} to {new_width}x{new_height}")
        else:
            print(f"Image {input_path} is within limits ({width}x{height}). Optimizing only.")

        if output_path is None:
            output_path = input_path

        # Save with optimization
        img.save(output_path, quality=quality, optimize=True)
        print(f"Saved to {output_path}")
        return True

    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize and optimize images.")
    parser.add_argument("input_path", help="Path to the input image")
    parser.add_argument("--output", help="Path to the output image (optional, defaults to overwrite)")
    parser.add_argument("--width", type=int, default=1280, help="Max width (default 1280 for 720p)")
    parser.add_argument("--height", type=int, default=720, help="Max height (default 720 for 720p)")
    
    args = parser.parse_args()
    
    resize_image(args.input_path, args.output, args.width, args.height)

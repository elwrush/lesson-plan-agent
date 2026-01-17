import argparse
import base64
import os
import time
import json
from google import genai
from google.genai import types

def generate_image_batch(assets_file, output_dir):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return

    client = genai.Client(api_key=api_key)
    
    with open(assets_file, 'r') as f:
        assets = json.load(f)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for item in assets:
        prompt = item['prompt']
        filename = item['filename']
        output_path = os.path.join(output_dir, filename)

        if os.path.exists(output_path):
            print(f"Skipping {filename}, already exists.")
            continue

        print(f"Generating image for: {filename}...")
        print(f"Prompt: {prompt}")

        try:
            # Using imagen-4.0-generate-001 as requested by user.
            model = "imagen-4.0-generate-001" 
            
            result = client.models.generate_images(
                model=model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    include_rai_reason=True,
                    output_mime_type="image/png"
                )
            )

            if result.generated_images:
                image = result.generated_images[0]
                with open(output_path, "wb") as f:
                    f.write(image.image.image_bytes)
                print(f"Saved to {output_path}")
            else:
                print(f"No image generated for {filename}")

        except Exception as e:
            print(f"Failed to generate {filename}: {e}")
        
        # Rate limit pause
        print("Waiting 10 seconds to respect quota...")
        time.sleep(10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch generate images using Gemini/Imagen")
    parser.add_argument("--assets", required=True, help="JSON file containing list of prompts and filenames")
    parser.add_argument("--output_dir", required=True, help="Directory to save images")
    args = parser.parse_args()

    generate_image_batch(args.assets, args.output_dir)

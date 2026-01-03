
import os
import google.generativeai as genai
from PIL import Image
import sys

def generate_image(prompt, output_file):
    api_key = os.environ.get('GEMINI-API-KEY')
    if not api_key:
        print("Error: GEMINI-API-KEY environment variable not set.")
        return False

    genai.configure(api_key=api_key)

    # Using the Imagen 3 model
    # Note: The model name might vary. 'imagen-3.0-generate-001' is a common identifier for API access if available to the key.
    # If not, we might need to use a different model or the user's specific endpoint.
    # For this script we will try the 'gemini-pro-vision' or similar if available for generation, 
    # but strictly speaking Imagen is a separate model. 
    # Let's try to access the image generation capability if exposed via this SDK version.
    # As of v0.8.3+, typical access is via `genai.ImageGenerationModel`.

    try:
        # User requested model
        print("Using model: gemini-2.5-flash-image")
        # Note: The SDK might access this differently depending on exact version, 
        # but we will try passing it to the ImageGenerationModel constructor or via genai.GenerativeModel if it was a multimodal generation, 
        # but for pure image generation, we usually use ImageGenerationModel.
        # However, 'gemini-2.5-flash-image' sounds like a specific new endpoint.
        # Let's try to load it.
        imagen = genai.ImageGenerationModel("gemini-2.5-flash-image") 
        
        print(f"Generating image for: '{prompt}'...")
        images = imagen.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="1:1",
            safety_filter_level="block_some",
            person_generation="allow_adult"
        )
        
        if images:
            images[0].save(output_file)
            print(f"✅ Image saved to: {output_file}")
            return True
        else:
            print("❌ No image returned.")
            return False

    except Exception as e:
        print(f"❌ Error generating image: {e}")
        # Fallback for some users who might have access via "imagen-2"
        try:
             print("Retrying with 'imagen-2'...")
             imagen = genai.ImageGenerationModel("imagen-2")
             images = imagen.generate_images(prompt=prompt, number_of_images=1)
             if images:
                images[0].save(output_file)
                print(f"✅ Image saved to: {output_file}")
                return True
        except Exception as e2:
             print(f"❌ Retry failed: {e2}")
             return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_images_gemini.py <prompt> <output_path>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    output_path = sys.argv[2]
    
    generate_image(prompt, output_path)

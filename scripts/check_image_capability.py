import os
import google.generativeai as genai
import sys

def generate_image(prompt, output_file):
    """Generate image using Gemini Flash multimodal model"""
    api_key = os.environ.get('GEMINI-API-KEY')
    if not api_key:
        print("Error: GEMINI-API-KEY environment variable not set.")
        return False

    genai.configure(api_key=api_key)
    
    try:
        # Try using Gemini Pro for image generation
        # Some Gemini models can generate images when prompted correctly
        model = genai.GenerativeModel('gemini-pro')
        
        print(f"Generating image for: '{prompt}'...")
        print("Note: Standard Gemini models do not support image generation output.")
        print("You may need to use a dedicated image generation service like DALL-E, Stable Diffusion, or Midjourney.")
        print("Alternatively, check if your API key has access to Imagen 3 via Google Cloud Vertex AI.")
        
        return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python check_image_capability.py <prompt> <output_path>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    output_path = sys.argv[2]
    
    generate_image(prompt, output_path)

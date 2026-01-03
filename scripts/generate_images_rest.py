import os
import google.generativeai as genai
import requests
import sys

def generate_image_via_api(prompt, output_file):
    """Generate image using direct REST API call to Gemini/Imagen"""
    api_key = os.environ.get('GEMINI-API-KEY')
    if not api_key:
        print("Error: GEMINI-API-KEY environment variable not set.")
        return False

    # Try using the Imagen REST API directly
    # This is the standard endpoint for image generation
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash-image:generateImage"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "prompt": prompt,
        "numberofImages": 1
    }
    
    try:
        print(f"Generating image with prompt: '{prompt}'...")
        print(f"Using API endpoint: {url}")
        
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'images' in result and len(result['images']) > 0:
                # The image is base64 encoded
                import base64
                image_data = base64.b64decode(result['images'][0])
                with open(output_file, 'wb') as f:
                    f.write(image_data)
                print(f"✅ Image saved to: {output_file}")
                return True
            else:
                print(f"❌ No images in response: {result}")
                return False
        else:
            print(f"❌ API error ({response.status_code}): {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_images_rest.py <prompt> <output_path>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    output_path = sys.argv[2]
    
    generate_image_via_api(prompt, output_path)

import os
import requests
import base64
import sys
import json

def generate_image(prompt, output_file):
    """Generate image using Gemini 3 Pro Image Preview via REST API"""
    api_key = os.environ.get('GEMINI-API-KEY')
    if not api_key:
        print("Error: GEMINI-API-KEY environment variable not set.")
        return False

    # Use the specific model endpoint
    model = "models/gemini-3-pro-image-preview"
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    # Request body for image generation
    data = {
        "contents": [{
            "parts": [{
                "text": f"Generate an image: {prompt}"
            }]
        }],
        "generationConfig": {
            "temperature": 1.0,
            "candidateCount": 1,
        }
    }
    
    try:
        print(f"Generating image for: '{prompt}'...")
        print(f"Using model: {model}")
        
        response = requests.post(
            f"{url}?key={api_key}",
            headers=headers,
            json=data,
            timeout=60
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response received: {json.dumps(result, indent=2)[:500]}...")
            
            # Check if there's image data in the response
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    for part in candidate['content']['parts']:
                        if 'inlineData' in part:
                            # Found image data
                            image_data = base64.b64decode(part['inlineData']['data'])
                            with open(output_file, 'wb') as f:
                                f.write(image_data)
                            print(f"✅ Image saved to: {output_file}")
                            return True
            
            print(f"❌ No image data found in response")
            return False
        else:
            print(f"❌ API error ({response.status_code}): {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_image_gemini3.py <prompt> <output_path>")
        sys.exit(1)
    
    prompt = sys.argv[1]
    output_path = sys.argv[2]
    
    generate_image(prompt, output_path)

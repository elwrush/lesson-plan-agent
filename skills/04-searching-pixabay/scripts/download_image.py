import argparse
import os
import sys
import requests
import shutil

# Pixabay API Endpoints
API_URL_IMAGE = "https://pixabay.com/api/"
API_URL_VIDEO = "https://pixabay.com/api/videos/"

def download_image(query, output_path, image_type="photo", orientation="horizontal"):
    api_key = os.environ.get("PIXABAY_API_KEY")
    if not api_key:
        print("[ERROR] PIXABAY_API_KEY environment variable is not set.")
        sys.exit(1)

    # Determine endpoint and type
    if image_type == "video":
        url = API_URL_VIDEO
        req_type = "film" # Pixabay parameter for videos might be different, but usually just 'video_type' or implicit
        # For video endpoint, 'q' is same. 'video_type' can be 'all', 'film', 'animation'
    else:
        url = API_URL_IMAGE
        req_type = image_type

    params = {
        "key": api_key,
        "q": query,
        "orientation": orientation,
        "per_page": 3,
        "safesearch": "true"
    }
    
    if image_type != "video":
        params["image_type"] = req_type
    else:
        params["video_type"] = "all"


    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if int(data["totalHits"]) > 0:
            # Pick the first result
            if image_type == "video":
                # Video object has 'videos' -> 'large' -> 'url' usually, or variations
                # Format: hits[0]['videos']['large']['url'] or 'medium'
                # Let's try to get the largest available connection (large or medium)
                hit = data["hits"][0]
                if 'videos' in hit and 'large' in hit['videos']:
                    download_url = hit['videos']['large']['url']
                elif 'videos' in hit and 'medium' in hit['videos']:
                    download_url = hit['videos']['medium']['url']
                else:
                    # Fallback if structure differs (unlikely for Pixabay API)
                    print("[ERROR] Could not find video URL in response.")
                    return False
            else:
                download_url = data["hits"][0]["largeImageURL"]
            
            print(f"[INFO] Found asset: {download_url}")
            
            # Download
            img_response = requests.get(download_url, stream=True)
            img_response.raise_for_status()

            # Create directory if missing
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, 'wb') as f:
                img_response.raw.decode_content = True
                shutil.copyfileobj(img_response.raw, f)
            
            print(f"[SUCCESS] Saved to: {output_path}")
            return True
        else:
            print(f"[WARN] No assets found for query: '{query}'")
            return False

    except Exception as e:
        print(f"[ERROR] Failed to download image: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download images from Pixabay.")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--type", default="photo", choices=["all", "photo", "illustration", "vector", "video"], help="Image type")
    parser.add_argument("--orientation", default="horizontal", choices=["all", "horizontal", "vertical"], help="Orientation")

    args = parser.parse_args()

    success = download_image(args.query, args.output, args.type, args.orientation)
    if not success:
        sys.exit(1)

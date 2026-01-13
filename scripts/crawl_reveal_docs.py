import os
import requests
import json
import time

def crawl_site(url, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    # Using the crawl endpoint to get all subpages
    # We limit depth and maxPages to keep it focused on the core docs
    data = {
        "url": url,
        "limit": 30,
        "scrapeOptions": {
            "formats": ["markdown"]
        }
    }
    
    print(f"Starting crawl of {url}...")
    response = requests.post("https://api.firecrawl.dev/v1/crawl", headers=headers, json=data)
    
    if response.status_code == 200:
        job_id = response.json().get("id")
        print(f"Crawl started with ID: {job_id}")
        return job_id
    else:
        print(f"Error starting crawl: {response.status_code} - {response.text}")
        return None

def check_crawl_status(job_id, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    while True:
        response = requests.get(f"https://api.firecrawl.dev/v1/crawl/{job_id}", headers=headers)
        if response.status_code == 200:
            status_data = response.json()
            status = status_data.get("status")
            print(f"Crawl status: {status} ({status_data.get('completed', 0)}/{status_data.get('total', '?')} pages)")
            
            if status == "completed":
                return status_data.get("data", [])
            elif status == "failed":
                print(f"Crawl failed: {status_data.get('error')}")
                return []
        else:
            print(f"Error checking status: {response.status_code}")
            return []
        time.sleep(10)

def main():
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("FIRECRAWL_API_KEY not found in environment")
        return

    # Root of the docs
    root_url = "https://revealjs.com/"
    
    job_id = crawl_site(root_url, api_key)
    if job_id:
        results = check_crawl_status(job_id, api_key)
        
        combined_markdown = "# Reveal.js Complete Reference Guide\n\n"
        combined_markdown += "> Generated via Firecrawl from official documentation.\n\n"
        
        # Sort results by URL for consistency
        results.sort(key=lambda x: x.get('metadata', {}).get('sourceURL', ''))
        
        for page in results:
            url = page.get('metadata', {}).get('sourceURL')
            title = page.get('metadata', {}).get('title', url)
            content = page.get('markdown', 'No content')
            
            combined_markdown += f"\n\n---\n# {title}\n**Source: {url}**\n\n" + content

        # Save to the final destination
        output_path = "knowledge-base/reveal-reference-guide.md"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(combined_markdown)
        print(f"Crawl complete. Saved to {output_path}")

if __name__ == "__main__":
    main()

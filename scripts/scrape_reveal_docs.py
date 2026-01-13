import os
import requests
import json

def scrape_page(url, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "url": url,
        "formats": ["markdown"]
    }
    response = requests.post("https://api.firecrawl.dev/v1/scrape", headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("data", {}).get("markdown", "")
    else:
        print(f"Error scraping {url}: {response.status_code} - {response.text}")
        return ""

def main():
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("FIRECRAWL_API_KEY not found in environment")
        return

    pages = [
        "https://revealjs.com/config/",
        "https://revealjs.com/media/",
        "https://revealjs.com/layout/"
    ]

    combined_markdown = ""
    for page in pages:
        print(f"Scraping {page}...")
        content = scrape_page(page, api_key)
        combined_markdown += f"\n\n# Source: {page}\n\n" + content

    with open("reveal_docs_scraped.md", "w", encoding="utf-8") as f:
        f.write(combined_markdown)
    print("Scraping complete. Saved to reveal_docs_scraped.md")

if __name__ == "__main__":
    main()

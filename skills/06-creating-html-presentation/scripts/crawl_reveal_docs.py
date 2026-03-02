"""Crawl Reveal.js documentation pages using Firecrawl."""
import os
import sys
from firecrawl import FirecrawlApp

DOCS_TO_CRAWL = {
    "reveal-markup.md": "https://revealjs.com/markup/",
    "reveal-backgrounds.md": "https://revealjs.com/backgrounds/",
    "reveal-layout.md": "https://revealjs.com/layout/",
    "reveal-fragments.md": "https://revealjs.com/fragments/",
    "reveal-auto-animate.md": "https://revealjs.com/auto-animate/",
}

def main():
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("❌ FIRECRAWL_API_KEY environment variable is missing.")
        sys.exit(1)

    app = FirecrawlApp(api_key=api_key)
    output_dir = "skills/creating-html-presentation/docs"
    os.makedirs(output_dir, exist_ok=True)

    for filename, url in DOCS_TO_CRAWL.items():
        print(f"🔥 Crawling: {url}")
        try:
            result = app.scrape(url, formats=['markdown'])
            if 'markdown' in result:
                output_path = os.path.join(output_dir, filename)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result['markdown'])
                print(f"✅ Saved to {output_path} ({len(result['markdown'])} chars)")
            else:
                print(f"❌ No markdown returned for {url}")
        except Exception as e:
            print(f"❌ Error crawling {url}: {e}")

    print("\n✅ Documentation crawl complete!")

if __name__ == "__main__":
    main()

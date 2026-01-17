import os
import requests
import json

def test_context7():
    api_key = os.getenv("CONTEXT7-API-KEY") or os.getenv("CONTEXT7_API_KEY")
    if not api_key:
        print("No API key found.")
        return

    # Try multiple library name variations
    searches = [
        ("typst", "meander text wrapping"),
        ("meander.typ", "contour wrapping alpha"),
        ("typst-meander", "wrap text around image"),
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    for lib_name, query in searches:
        url = f"https://context7.com/api/v2/libs/search?libraryName={lib_name}&query={query.replace(' ', '+')}"
        print(f"\n🔍 Searching: {lib_name} | Query: {query}")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("results"):
                    print(f"✅ Found {len(data['results'])} result(s)")
                    for r in data["results"]:
                        print(f"   - {r['id']}: {r['title']}")
                    
                    filename = f"context7_{lib_name.replace('.', '_')}.json"
                    with open(filename, "w") as f:
                        json.dump(data, f, indent=2)
                    print(f"   Saved to {filename}")
                else:
                    print("   No results found")
            else:
                print(f"❌ Status {response.status_code}: {response.text[:100]}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_context7()

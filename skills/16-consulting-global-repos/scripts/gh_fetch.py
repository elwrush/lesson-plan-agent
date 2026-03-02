import os
import requests
import sys
import base64
import json

# Configuration for Global Reference Repositories
REPOS = {
    "typst": "typst/typst",
    "typst-packages": "typst/packages",
    "revealjs": "hakimel/reveal.js",
    "fontawesome": "FortAwesome/Font-Awesome",
    "reference": "elwrush/lesson-plan-references",
}

# The PAT provided by the user in the environment
TOKEN = os.getenv("GITHUB_MCP_PAT")

def get_gh_content(alias_path):
    """
    Fetches file content or directory listings from GitHub.
    Usage: <alias>:<path>
    """
    if ":" not in alias_path:
        return f"Error: Usage must be <alias>:<path>. Available aliases: {', '.join(REPOS.keys())}"

    alias, path = alias_path.split(":", 1)
    repo = REPOS.get(alias)
    
    if not repo:
        return f"Error: Alias '{alias}' not found in REPOS mapping."
    
    # Construct API URL
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Gemini-CLI-Repo-Reader"
    }
    
    # Try with token first if available
    if TOKEN:
        auth_prefix = "Bearer" if TOKEN.startswith("github_pat_") else "token"
        headers["Authorization"] = f"{auth_prefix} {TOKEN}"
    
    try:
        response = requests.get(url, headers=headers)
        
        # If 401, try one last time without auth (for public repos)
        if response.status_code == 401 and TOKEN:
            del headers["Authorization"]
            response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            # Handle Directory listing
            if isinstance(data, list):
                output = []
                for item in data:
                    item_type = "DIR " if item['type'] == 'dir' else "FILE"
                    output.append(f"{item_type} {item['path']}")
                return "\n".join(output)
            
            # Handle Single File
            if data.get("encoding") == "base64":
                # Decode base64 content
                content = base64.b64decode(data['content']).decode('utf-8')
                return content
            
            return f"Error: Unexpected response format from GitHub API."
            
        elif response.status_code == 404:
            return f"Error: 404 Not Found ({repo}/{path})"
        elif response.status_code == 401:
            return f"Error: 401 Unauthorized. Check your GITHUB_MCP_PAT."
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.RequestException as e:
        return f"Error during request: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gh_fetch.py <alias>:<path>")
        print(f"Available Aliases: {', '.join(REPOS.keys())}")
        sys.exit(1)
        
    result = get_gh_content(sys.argv[1])
    print(result)

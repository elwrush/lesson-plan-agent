import subprocess
import sys

def verify_repo():
    try:
        # Get git remote origin URL
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        url = result.stdout.strip()
        
        target_repo = "elwrush/actions-gh-pages"
        
        if target_repo not in url:
            print(f"❌ Error: Wrong repository!")
            print(f"   Expected to contain: '{target_repo}'")
            print(f"   Current remote: '{url}'")
            print("   Deployment MUST run from the 'actions-gh-pages' repository.")
            sys.exit(1)
            
        print(f"✅ Repository verified: {url}")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ Error: Not a git repository or no remote origin found.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error verifying repo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_repo()

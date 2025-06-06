import os
import requests

# GitHub repository details
USER = 'vsaikiran234'
REPO = 'FR_TEST'
BRANCH = 'main'
GITHUB_API_COMMITS_URL = f'https://api.github.com/repos/{USER}/{REPO}/commits/{BRANCH}'
GITHUB_RAW_URL = f'https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/bin/main.py'
LOCAL_MAIN_PY_PATH = os.path.join('bin', 'main.py')
LOCAL_COMMIT_HASH_PATH = os.path.join('bin', '.latest_commit')

def get_latest_commit_hash():
    """Fetch the latest commit hash from GitHub."""
    response = requests.get(GITHUB_API_COMMITS_URL)
    if response.status_code == 200:
        return response.json()["sha"]
    else:
        print(f"❌ Failed to fetch commit hash. HTTP Status: {response.status_code}")
        return None

def download_main_py():
    """Download main.py only if the latest commit hash is different."""
    latest_commit_hash = get_latest_commit_hash()
    if not latest_commit_hash:
        return

    # Check local commit hash
    if os.path.exists(LOCAL_COMMIT_HASH_PATH):
        with open(LOCAL_COMMIT_HASH_PATH, 'r') as file:
            local_commit_hash = file.read().strip()

        if local_commit_hash == latest_commit_hash:
            print("✅ No changes detected in main.py. Already up to date.")
            return

    print(f"🔄 Updating bin/main.py from {GITHUB_RAW_URL}...")
    response = requests.get(GITHUB_RAW_URL)
    if response.status_code == 200:
        new_content = response.text

        if not os.path.exists('bin'):
            os.makedirs('bin')

        with open(LOCAL_MAIN_PY_PATH, 'w') as file:
            file.write(new_content)
        
        # Save the new commit hash
        with open(LOCAL_COMMIT_HASH_PATH, 'w') as file:
            file.write(latest_commit_hash)

        print("✅ Updated local bin/main.py with latest version from GitHub.")
    else:
        print(f"❌ Failed to download file. HTTP Status: {response.status_code}")

if __name__ == '__main__':
    download_main_py()

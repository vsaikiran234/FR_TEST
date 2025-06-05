import os
import requests

# GitHub repository details
USER = 'vsaikiran234'
REPO = 'FR_TEST'
BRANCH = 'main'
GITHUB_RAW_URL = f'https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/bin/main.py'
LOCAL_MAIN_PY_PATH = os.path.join('bin', 'main.py')

def download_main_py():
    print(f"🔄 Checking for updates to bin/main.py from {GITHUB_RAW_URL}...")
    response = requests.get(GITHUB_RAW_URL)
    if response.status_code == 200:
        new_content = response.text

        if not os.path.exists('bin'):
            os.makedirs('bin')

        if os.path.exists(LOCAL_MAIN_PY_PATH):
            with open(LOCAL_MAIN_PY_PATH, 'r') as file:
                existing_content = file.read()
            if existing_content == new_content:
                print("✅ No changes detected in main.py. Already up to date.")
                return

        with open(LOCAL_MAIN_PY_PATH, 'w') as file:
            file.write(new_content)
        print("✅ Updated local bin/main.py with latest version from GitHub.")
    else:
        print(f"❌ Failed to download file. HTTP Status: {response.status_code}")

if __name__ == '__main__':
    download_main_py()

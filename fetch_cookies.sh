# fetch_cookies.py
import urllib.request

url = "https://drive.google.com/uc?export=download&id=1lv2qcVGMC7jLT3cX7LXPWB9Qne8RHAC4"
output_path = "cookies.txt"

try:
    print("🔁 Downloading cookies.txt...")
    urllib.request.urlretrieve(url, output_path)
    print("✅ cookies.txt downloaded successfully.")
except Exception as e:
    print("❌ Failed to download cookies.txt:", e)

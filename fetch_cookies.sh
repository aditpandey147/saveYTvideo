# fetch_cookies.py
import urllib.request

url = "https://drive.google.com/uc?export=download&id=1k064giVco56MSo6eYn7Ol58kw1muISCf"
output_path = "cookies.txt"

try:
    print("🔁 Downloading cookies.txt...")
    urllib.request.urlretrieve(url, output_path)
    print("✅ cookies.txt downloaded successfully.")
except Exception as e:
    print("❌ Failed to download cookies.txt:", e)

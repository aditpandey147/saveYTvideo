# fetch_cookies.py
import urllib.request

URL = "https://drive.google.com/uc?export=download&id=1Y-Vst2pQZGEA_SUWbFVDkUn0N_ZGltxF"
OUTPUT = "cookies.txt"

try:
    print("⬇️ Downloading cookies.txt from Google Drive...")
    urllib.request.urlretrieve(URL, OUTPUT)
    print("✅ cookies.txt downloaded and saved!")
except Exception as e:
    print("❌ Error downloading cookies.txt:", e)

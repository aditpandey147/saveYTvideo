# fetch_cookies.py
import urllib.request
import os

FILE_ID = "1Y-Vst2pQZGEA_SUWbFVDkUn0N_ZGltxF"  # 🔁 Replace with YOUR file ID
URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"
OUTPUT = os.path.join(os.path.dirname(__file__), "cookies.txt")

try:
    print("⬇️ Downloading cookies.txt from Google Drive...")
    urllib.request.urlretrieve(URL, OUTPUT)
    print("✅ cookies.txt downloaded and saved!")
except Exception as e:
    print("❌ Error downloading cookies.txt:", e)

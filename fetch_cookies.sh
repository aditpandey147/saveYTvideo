#!/bin/bash

echo "🔁 Fetching cookies.txt from Google Drive..."

# ✅ REPLACE ONLY THIS FILE ID with your real one
FILE_ID="YOUR_FILE_ID_HERE"

curl -L -o cookies.txt "https://drive.google.com/uc?export=download&id=1Y-Vst2pQZGEA_SUWbFVDkUn0N_ZGltxF"

if [ -f cookies.txt ]; then
    echo "✅ cookies.txt downloaded!"
else
    echo "❌ Failed to download cookies.txt"
    ls -l
fi

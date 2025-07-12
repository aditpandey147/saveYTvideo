#!/bin/bash

echo "🔁 Downloading cookies.txt..."

curl -L -o cookies.txt "https://drive.google.com/file/d/1Y-Vst2pQZGEA_SUWbFVDkUn0N_ZGltxF/view?usp=sharing"

if [ -f cookies.txt ]; then
    echo "✅ cookies.txt downloaded!"
else
    echo "❌ Failed to download cookies.txt"
fi

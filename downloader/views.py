import os
import subprocess
import random
import requests
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.shortcuts import render

# Your Google Drive file ID
GOOGLE_DRIVE_FILE_ID = '1k064giVco56MSo6eYn7Ol58kw1muISCf'
COOKIES_FILE_NAME = 'cookies.txt'
COOKIES_URL = f'https://drive.google.com/uc?export=download&id={GOOGLE_DRIVE_FILE_ID}'

def download_cookies():
    """Auto-download cookies.txt from Google Drive."""
    cookies_path = os.path.join(settings.BASE_DIR, COOKIES_FILE_NAME)
    if not os.path.exists(cookies_path):
        try:
            print("📥 Downloading cookies.txt...")
            response = requests.get(COOKIES_URL)
            if response.status_code == 200:
                with open(cookies_path, 'wb') as f:
                    f.write(response.content)
                print("✅ cookies.txt downloaded.")
            else:
                print("❌ Failed to download cookies:", response.status_code)
        except Exception as e:
            print("❌ Error fetching cookies:", e)
    return cookies_path

def index(request):
    return render(request, 'downloader/index.html')

def download_video(request):
    if request.method == 'POST':
        url = request.POST.get('link')
        selected_format = request.POST.get('format')

        if not url or not selected_format:
            return HttpResponse("❌ Missing link or format.")

        cookies_path = download_cookies()
        print("✅ COOKIES EXISTS:", os.path.exists(cookies_path))
        print("📁 BASE_DIR files:", os.listdir(settings.BASE_DIR))

        output_dir = os.path.join(settings.BASE_DIR, 'downloads')
        os.makedirs(output_dir, exist_ok=True)
        output_template = os.path.join(output_dir, '%(title)s.%(ext)s')

        proxies = [
            "http://103.139.242.178:8080",
            "http://49.207.251.89:61033",
            "http://103.86.155.78:3128",
        ]
        proxy = random.choice(proxies)
        command = []
        ext = ''

        if selected_format == 'mp3':
            command = [
                'yt-dlp',
                '--cookies', cookies_path,
                '--proxy', proxy,
                '-x', '--audio-format', 'mp3',
                '--ffmpeg-location', '/usr/bin/ffmpeg',
                '-o', output_template,
                url
            ]
            ext = '.mp3'
        elif selected_format == 'mp4_720':
            command = [
                'yt-dlp',
                '--cookies', cookies_path,
                '--proxy', proxy,
                '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                '--merge-output-format', 'mp4',
                '-o', output_template,
                url
            ]
            ext = '.mp4'
        elif selected_format == 'mp4_360':
            command = [
                'yt-dlp',
                '--cookies', cookies_path,
                '--proxy', proxy,
                '-f', 'bestvideo[height<=360]+bestaudio/best[height<=360]',
                '--merge-output-format', 'mp4',
                '-o', output_template,
                url
            ]
            ext = '.mp4'
        else:
            return HttpResponse("❌ Invalid format selected.")

        try:
            print("▶️ Running yt-dlp...")
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=240)
            if result.returncode != 0:
                return HttpResponse("❌ yt-dlp failed.<br><pre>" + result.stderr + "</pre>")

            # Check output file
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    if file.endswith(ext):
                        file_path = os.path.join(root, file)
                        return FileResponse(open(file_path, 'rb'), as_attachment=True)

            return HttpResponse("❌ Could not find downloaded file.")

        except subprocess.TimeoutExpired:
            return HttpResponse("❌ yt-dlp took too long and was killed. Try again.")
        except Exception as e:
            import traceback
            error_log = traceback.format_exc()
            print("🔥 Full error:\n", error_log)
            return HttpResponse(f"❌ Internal Error:<br><pre>{error_log}</pre>")


    return HttpResponse("❌ Invalid request.")

def blog(request):
   return render(request, "blog.html",)
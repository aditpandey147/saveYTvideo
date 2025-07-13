import os
import subprocess
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
import random

def index(request):
    return render(request, 'downloader/index.html')

def download_video(request):
    if request.method == 'POST':
        url = request.POST.get('link')
        selected_format = request.POST.get('format')

        cookies_path = os.path.join(settings.BASE_DIR, 'cookies.txt')
        print("✅ COOKIES EXISTS:", os.path.exists(cookies_path))
        print("📁 BASE_DIR files:", os.listdir(settings.BASE_DIR))

        if not url or not selected_format:
            return HttpResponse("❌ Missing link or format.")

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
                '-x',
                '--audio-format', 'mp3',
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
            print("▶️ Running yt-dlp command...")
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)

            if result.returncode != 0:
                print("❌ yt-dlp failed:", result.stderr)
                return HttpResponse("❌ yt-dlp failed.<br><pre>" + result.stderr + "</pre>")

            for line in result.stdout.splitlines():
                if 'Destination' in line:
                    filename = line.split('Destination')[-1].strip()
                    if os.path.exists(filename):
                        print("✅ File ready:", filename)
                        return FileResponse(open(filename, 'rb'), as_attachment=True)

            return HttpResponse("❌ Could not find the downloaded file.")

        except subprocess.TimeoutExpired:
            return HttpResponse("❌ yt-dlp took too long and was killed. Try again.")
        except Exception as e:
            print("❌ Unexpected error:", str(e))
            return HttpResponse("❌ Unexpected error:<br><pre>" + str(e) + "</pre>")

    return HttpResponse("❌ Invalid request method.")

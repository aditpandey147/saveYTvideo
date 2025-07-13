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

        file_ext = ''
        command = []

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
            file_ext = '.mp3'

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
            file_ext = '.mp4'

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
            file_ext = '.mp4'
        else:
            return HttpResponse("❌ Invalid format selected.")

        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print("✅ yt-dlp output:\n", result.stdout)

            for filename in os.listdir(output_dir):
                if filename.endswith(file_ext):
                    file_path = os.path.join(output_dir, filename)
                    if os.path.exists(file_path):
                        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)

            return HttpResponse("❌ File not found after download.")

        except subprocess.CalledProcessError as e:
            print("❌ yt-dlp failed:\n", e.stderr)
            return HttpResponse("❌ Download failed. Error below:<br><pre>" + e.stderr + "</pre>", status=500)

        except SystemExit as e:
            print("❌ yt-dlp caused SystemExit:", e)
            return HttpResponse("❌ SystemExit error occurred. yt-dlp exited with code 1. Likely due to proxy, cookie, or region issue.", status=500)

        except Exception as e:
            print("❌ Unexpected error:", str(e))
            return HttpResponse(f"❌ Unexpected error: {str(e)}", status=500)

    return HttpResponse("❌ Invalid request method.")
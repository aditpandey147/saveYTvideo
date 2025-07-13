import os
import subprocess
import random
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse, HttpResponse


def index(request):
    return render(request, 'downloader/index.html')


def download_video(request):
    if request.method != 'POST':
        return HttpResponse("❌ Invalid request method.")

    url = request.POST.get('link')
    selected_format = request.POST.get('format')
    cookies_path = os.path.join(settings.BASE_DIR, 'cookies.txt')
    cookies_exist = os.path.exists(cookies_path)

    print("✅ COOKIES EXISTS:", cookies_exist)
    print("📁 BASE_DIR files:", os.listdir(settings.BASE_DIR))

    if not url or not selected_format:
        return HttpResponse("❌ Missing video link or format selection.")

    output_dir = os.path.join(settings.BASE_DIR, 'downloads')
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, '%(title)s.%(ext)s')

    proxies = [
        "http://103.139.242.178:8080",
        "http://49.207.251.89:61033",
        "http://103.86.155.78:3128",
    ]
    proxy = random.choice(proxies)

    # Build yt-dlp command based on selected format
    command = [
        "yt-dlp",
        "--proxy", proxy,
        "-o", output_template,
        url
    ]

    if cookies_exist:
        command = ["yt-dlp", "--cookies", cookies_path, "--proxy", proxy, "-o", output_template, url]

    if selected_format == 'mp3':
        command += [
            "-x",
            "--audio-format", "mp3",
            "--ffmpeg-location", "/usr/bin/ffmpeg"
        ]
        file_ext = ".mp3"
    elif selected_format == 'mp4_720':
        command += [
            "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "--merge-output-format", "mp4"
        ]
        file_ext = ".mp4"
    elif selected_format == 'mp4_360':
        command += [
            "-f", "bestvideo[height<=360]+bestaudio/best[height<=360]",
            "--merge-output-format", "mp4"
        ]
        file_ext = ".mp4"
    else:
        return HttpResponse("❌ Invalid format selected.")

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print("✅ yt-dlp output:\n", result.stdout)

        # Find the downloaded file
        for filename in os.listdir(output_dir):
            if filename.endswith(file_ext):
                file_path = os.path.join(output_dir, filename)
                if os.path.exists(file_path):
                    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)

        return HttpResponse("❌ File not found after download.")
    except subprocess.CalledProcessError as e:
        print("❌ yt-dlp error:\n", e.stderr)
        return HttpResponse("❌ Download failed. Error below:<br><pre>" + e.stderr + "</pre>")
    except Exception as e:
        print("❌ Unexpected error:\n", str(e))
        return HttpResponse(f"❌ Unexpected error: {str(e)}")

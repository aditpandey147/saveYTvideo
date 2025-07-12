import os
import subprocess
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from django.conf import settings

DOWNLOAD_DIR = os.path.join(settings.BASE_DIR, 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def index(request):
    return render(request, 'downloader/index.html')

def download_video(request):
    if request.method == 'POST':
        url = request.POST.get('link')
        selected_format = request.POST.get('format')

        output_template = os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')

        if selected_format == 'mp3':
            command = [
                'yt-dlp',
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
                '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                '-o', output_template,
                url
            ]
            ext = '.mp4'
        elif selected_format == 'mp4_360':
            command = [
                'yt-dlp',
                '-f', 'bestvideo[height<=360]+bestaudio/best[height<=360]',
                '-o', output_template,
                url
            ]
            ext = '.mp4'
        else:
            return HttpResponse("❌ Invalid format selected.")

        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("✅ Download Success:\n", result.stdout)

            # Get downloaded file path
            lines = result.stdout.splitlines()
            downloaded_file = None
            for line in lines:
                if '[ExtractAudio]' in line or 'Destination' in line:
                    downloaded_file = line.split('Destination: ')[-1].strip()
                    break

            if not downloaded_file or not os.path.exists(downloaded_file):
                return HttpResponse("❌ File not found after download.")

            # Stream file to user
            response = FileResponse(open(downloaded_file, 'rb'), as_attachment=True)
            return response

        except subprocess.CalledProcessError as e:
            print("❌ Download Failed:\n", e.stderr)
            return HttpResponse(f"❌ Download failed:\n{e.stderr}")

    return HttpResponse("❌ Invalid request.")

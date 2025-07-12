import os
import subprocess
from django.shortcuts import render
from django.http import FileResponse, HttpResponse

def index(request):
    return render(request, 'downloader/index.html')

def download_video(request):
    if request.method == 'POST':
        url = request.POST.get('link')
        selected_format = request.POST.get('format')

        output_template = 'downloads/%(title)s.%(ext)s'

        if selected_format == 'mp3':
            command = [
                'yt-dlp',
                '-x', '--audio-format', 'mp3',
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
        except subprocess.CalledProcessError as e:
            print("❌ Download Failed:\n", e.stderr)
    return HttpResponse("❌ Invalid request.")

import os
import subprocess
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from pathlib import Path

def index(request):
    return render(request, 'downloader/index.html')

def download_video(request):
    if request.method == 'POST':
        url = request.POST.get('link')
        selected_format = request.POST.get('format')

        download_dir = 'downloads'
        os.makedirs(download_dir, exist_ok=True)

        output_template = os.path.join(download_dir, '%(title)s.%(ext)s')

        # Choose yt-dlp command
        if selected_format == 'mp3':
            command = [
                'yt-dlp', '-x',
                '--audio-format', 'mp3',
                '--ffmpeg-location', '/usr/bin/ffmpeg',
                '-o', output_template,
                url
            ]
            file_ext = '.mp3'
        elif selected_format == 'mp4_720':
            command = [
                'yt-dlp',
                '-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                '--ffmpeg-location', '/usr/bin/ffmpeg',
                '-o', output_template,
                url
            ]
            file_ext = '.mp4'
        elif selected_format == 'mp4_360':
            command = [
                'yt-dlp',
                '-f', 'bestvideo[height<=360]+bestaudio/best[height<=360]',
                '--ffmpeg-location', '/usr/bin/ffmpeg',
                '-o', output_template,
                url
            ]
            file_ext = '.mp4'
        else:
            return HttpResponse("❌ Invalid format selected.")

        try:
            # Run yt-dlp
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Find downloaded file
            for line in result.stdout.splitlines():
                if "[ExtractAudio]" in line or "[download]" in line:
                    continue
                if "[Merger]" in line or "Merging formats into" in line:
                    file_path = line.split("‘")[-1].split("’")[0]
                    break

            # Fallback method if stdout doesn't help
            downloaded_files = list(Path(download_dir).glob(f'*.{file_ext.strip(".")}'))
            if not downloaded_files:
                return HttpResponse("❌ Downloaded file not found.")
            file_path = str(downloaded_files[-1])

            # Return file
            return FileResponse(open(file_path, 'rb'), as_attachment=True)

        except subprocess.CalledProcessError as e:
            return HttpResponse("❌ Download failed:<br><pre>" + e.stderr + "</pre>")

    return HttpResponse("❌ Invalid request.")

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

        if not url or not selected_format:
            return HttpResponse("❌ Missing link or format.")

        output_dir = 'downloads'
        os.makedirs(output_dir, exist_ok=True)
        output_template = os.path.join(output_dir, '%(title)s.%(ext)s')

        command = []
        ext = ""

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
                '--merge-output-format', 'mp4',
                '-o', output_template,
                url
            ]
            ext = '.mp4'
        elif selected_format == 'mp4_360':
            command = [
                'yt-dlp',
                '-f', 'bestvideo[height<=360]+bestaudio/best[height<=360]',
                '--merge-output-format', 'mp4',
                '-o', output_template,
                url
            ]
            ext = '.mp4'
        else:
            return HttpResponse("❌ Invalid format selected.")

        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("✅ Download Output:", result.stdout)

            # Search for downloaded file
            for line in result.stdout.splitlines():
                if 'Destination' in line:
                    filename = line.split('Destination')[-1].strip()
                    if os.path.exists(filename):
                        return FileResponse(open(filename, 'rb'), as_attachment=True)
        except subprocess.CalledProcessError as e:
            print("❌ yt-dlp failed with this stderr:\n", e.stderr)
            return HttpResponse("❌ Download failed. Error below:<br><pre>" + e.stderr + "</pre>")
    return HttpResponse("❌ Invalid request.")

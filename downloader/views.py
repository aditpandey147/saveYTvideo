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
                '--ffmpeg-location', r'C:\ffmpeg\bin',  # 👈 point to your folder!
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
            subprocess.run(command, check=True)

            # Find the latest file
            files = [f for f in os.listdir('downloads') if f.endswith(ext)]
            if not files:
                return HttpResponse("❌ File not downloaded.")
            latest_file = max(files, key=lambda f: os.path.getctime(os.path.join('downloads', f)))
            return FileResponse(open(os.path.join('downloads', latest_file), 'rb'), as_attachment=True)

        except Exception as e:
            return HttpResponse(f"❌ Error: {str(e)}")

    return HttpResponse("❌ Invalid request.")

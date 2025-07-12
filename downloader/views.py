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

        if not url:
            return HttpResponse("❌ Please enter a YouTube link.")

        # Check if video is available before download
        check_command = ['yt-dlp', '--skip-download', '--print', 'title', url]
        try:
            subprocess.run(check_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            return HttpResponse("❌ This video is not available or is restricted. Try another link.")

        # Prepare download command
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
            print("✅ Download successful:", result.stdout)

            # Find downloaded file path from yt-dlp output
            for line in result.stdout.splitlines():
                if '[ExtractAudio]' in line or '[download] Destination:' in line:
                    filepath = line.split(':', 1)[-1].strip()
                    if os.path.exists(filepath):
                        return FileResponse(open(filepath, 'rb'), as_attachment=True)

            return HttpResponse("✅ Download completed. Check downloads folder.")
        except subprocess.CalledProcessError as e:
            print("❌ Download error:", e.stderr)
            return HttpResponse("❌ Download failed. Please check the link or try a different video.")

    return HttpResponse("❌ Invalid request.")

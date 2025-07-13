import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# ✅ Define BASE_DIR
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yt_downloader.settings')

application = get_wsgi_application()

# ✅ Enable WhiteNoise for static files
application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))

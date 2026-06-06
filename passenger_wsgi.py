import os
import sys

# 🔴 این آدرس رو به مسیر واقعی هاستت تغییر بده
# (از File Manager ببین دقیقاً کجایی)
PROJECT_PATH = '/home/mostafazarei/public_html'

if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'titan_config.settings')
os.environ['PYTHON_EGG_CACHE'] = '/tmp/python_egg_cache'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import os
import sys

# مسیر ریشه پروژه
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'titan_config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

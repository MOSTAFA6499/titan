import os
import sys

print("=== App is starting ===")
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'titan_config.settings')
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("=== Django loaded successfully ===")
    
except Exception as e:
    print(f"=== ERROR: {e} ===")
    raise

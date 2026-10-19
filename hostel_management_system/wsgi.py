"""WSGI config for hostel_management_system."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hostel_management_system.settings")

application = get_wsgi_application()
app = application  # Vercel looks for `app`
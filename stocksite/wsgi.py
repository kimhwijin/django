"""
WSGI config for stocksite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_FILES = os.path.join(BASE_DIR, 'staticfiles')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocksite.settings')

application = get_wsgi_application()
application = WhiteNoise(application,root=STATIC_FILES)

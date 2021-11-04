"""
ASGI config for IPC2_Proyecto3_201801295 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IPC2_Proyecto3_201801295.settings')

application = get_asgi_application()

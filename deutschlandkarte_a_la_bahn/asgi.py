"""
ASGI config for deutschlandkarte_a_la_bahn project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deutschlandkarte_a_la_bahn.settings')

application = get_asgi_application()

"""
ASGI config for meuprojeto02 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto02.settings')

application = get_asgi_application()
# ASGI, que significa Asynchronous Server Gateway Interface, é uma interface de comunicação assíncrona entre servidores web e aplicativos Python. No contexto do Django, o ASGI se tornou essencial para o desenvolvimento web moderno, proporcionando diversos benefícios em comparação com a interface anterior, WSGI (Web Server Gateway Interface).
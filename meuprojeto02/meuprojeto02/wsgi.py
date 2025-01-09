"""
WSGI config for meuprojeto02 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto02.settings')

application = get_wsgi_application()
# O wsgi.py é um arquivo Python que define como a aplicação Django será executada pelo servidor web. Ele define a interface WSGI (Web Server Gateway Interface) que o servidor utiliza para se comunicar com a aplicação Django.

# O wsgi.py geralmente importa o módulo django.wsgi e utiliza a função get_wsgi_application para criar a aplicação WSGI. Essa aplicação é então passada para o servidor web, que a utiliza para processar as solicitações HTTP e gerar as respostas adequadas.
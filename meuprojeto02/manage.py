#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto02.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
# O manage.py é um utilitário de linha de comando poderoso que oferece diversas funcionalidades para gerenciar e executar tarefas relacionadas ao seu projeto Django. Através dele, você pode realizar ações como:

# Criar projetos e aplicativos Django
# Executar migrações de banco de dados
# Iniciar o servidor de desenvolvimento
# Criar usuários de administração
# Gerenciar arquivos estáticos
# Testar seu código
# O manage.py é uma ferramenta essencial para o desenvolvimento de qualquer projeto Django, pois simplifica diversas tarefas administrativas e facilita o gerenciamento do seu código.
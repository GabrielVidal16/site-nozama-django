#Instalar o venv:
#pip install virtualenv
#Criando um Ambiente Virtual:
#python -m venv .venv
#Ative o ambiente virtual criado:
#.\.venv\Scripts\activate
#Atualize o pip:
#python.exe -m pip install --upgrade pip
# Abra o terminal e execute o seguinte comando para instalar o Django globalmente:
# pip install django
#Verifique se o Django foi instalado corretamente executando o comando:
#django-admin --version
#instalando banco de dados
#pip install mysql-connector
# Dentro do ambiente virtual ativado, navegue até o diretório onde deseja criar seu projeto.
# Utilize o comando django-admin para criar um novo projeto chamado "meuprojeto":
#django-admin startproject meuprojeto
#abra o diretorio que esta seu projeto:
#cd meuprojeto
#Explorando a Estrutura do Projeto:
# Acesse o diretório "meuprojeto" criado.
# Observe os arquivos e pastas presentes:
# manage.py: Script para gerenciar tarefas do Django, como criar migrações e executar testes.
# meuprojeto: Diretório principal do seu projeto, contendo o arquivo settings.py com as configurações globais da aplicação.
# meuprojeto/urls.py: Define as URLs que serão mapeadas para as funções do seu projeto.
# meuprojeto/wsgi.py: Ponto de entrada para o servidor web do Django.
#No terminal, dentro do diretório do projeto, utilize o comando:
#python manage.py startapp main nome do seu projeto
#Para criar seu app no_seu_app

#no seu gerenciador de projeto no arquivo settings.py;
# import os
# from pathlib import Path
# from main.bd_config import conecta_no_banco_de_dados
#abaixo de DEBUG no settings insira:
# if DEBUG:
#     bd = conecta_no_banco_de_dados()

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'no_seu_app',
# ]
#pip install mysqlclient   
#Instale o mysqlclient, necessário para que seja realizada a migração do sqlite para o mysql.connector.
#python manage.py migrate  
#Realiza a migração do sqlite para o mysql.connector.
#python manage.py createsuperuser
#Cria um super usuário para gestão do django.

#Dentro de settings, para usar o mysql.connector, substitua o que vem por padrão:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'aula06', 
#         'USER': 'root',  
#         'PASSWORD': '',  
#         'HOST': '127.0.0.1', 
#         'PORT': '3306', 
#         'OPTIONS': {
#             'autocommit': True,
#         }
#     }
# }


#no seu gerenciador de projeto no arquivo urls.py
#import o seu projeto
# from main import views
# e passe a rota de acesso
# urlpatterns = [
#    #rota, view responsavel nome de referencia
#     path('', views.index, name='index'),
    
# ]
# no seu projeto no arquivo views.py
# crie o render para acessar sua rota com a função
# from django.shortcuts import render

# def index(request):
#     return render(request, 'index.html')


#python manage.py runserver
# O comando iniciará o servidor de desenvolvimento do Django em uma porta específica (geralmente a 8000).
# Acesse o endereço http://http://127.0.0.1:8000/ em seu navegador para visualizar a página inicial padrão do Django.





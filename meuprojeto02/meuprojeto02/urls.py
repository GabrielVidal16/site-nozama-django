"""
URL configuration for meuprojeto02 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   #rota, view responsavel nome de referencia
    path('guia', views.index, name='index'),
    path('sobre',views.sobre,name='sobre'),
     path('contato/', views.contato, name='contato'),
    
     
     path('cadastro/', views.cadastro, name='cadastro'),
     path('editarusuario/<int:id>', views.editarusuario, name='editarusuario'),
     path('excluirususario/<int:id>/', views.excluirususario, name='excluirususario'),
      
      
      path('contatos/', views.contatos, name='contatos'),
      path('usuarios/', views.usuarios, name='usuarios'),
      path('', views.login, name='login'),
      path('admin/', admin.site.urls),
      path('paginainicial', views.paginainicial, name='paginainicial'),
        path('accounts/', include('django.contrib.auth.urls')),
      path('atendimento/<int:id>/',views.atenderchamado, name='atendimento_detail'),
      
 ]
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()


#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Este arquivo define o mapeamento entre URLs e as views (visualizações) do seu projeto Django. Ele funciona como um roteador, direcionando cada solicitação HTTP para a view correta. O urls.py é organizado em padrões de URL que definem a estrutura das URLs da sua aplicação.

# Ao definir um padrão de URL, você especifica a URL que acionará a view correspondente. A view é a função Python que processa a solicitação e gera a resposta HTML que será enviada ao usuário.
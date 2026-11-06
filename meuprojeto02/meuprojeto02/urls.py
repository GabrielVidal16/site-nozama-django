from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path("", views.home, name="home"),
    path("carrinho/", views.carrinho, name="carrinho"),
    path("adicionar-ao-carrinho/<int:produto_id>/", views.adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
    path("finalizar-compra/", views.finalizar_compra, name="finalizar_compra"),
    path("compras/", views.compras, name="compras"),
    path("registro/", views.registro, name="registro"),
    path("editarproduto/<int:produto_id>/", views.editarproduto, name="editarproduto"),
    path("excluirproduto/<int:produto_id>/", views.excluirproduto, name="excluirproduto"),
    path("produtos/", views.produtos, name="produtos"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout_view"),
    path("admin/", admin.site.urls),
]

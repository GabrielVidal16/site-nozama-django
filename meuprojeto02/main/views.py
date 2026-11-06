from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CadastroForm, LoginForm
from .models import Product, Purchase, UserProfile


def _cart_items(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart.keys())
    return [
        {
            "product": product,
            "quantity": int(cart.get(str(product.id), 0)),
            "total": product.price * int(cart.get(str(product.id), 0)),
        }
        for product in products
    ]


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        auth_login(request, form.get_user())
        return redirect("home")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    return redirect("login")


def registro(request):
    form = CadastroForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        UserProfile.objects.create(user=user)
        return redirect("login")
    return render(request, "cadastro_usuario.html", {"form": form})


def home(request):
    profile = (
        UserProfile.objects.filter(user=request.user).first()
        if request.user.is_authenticated
        else None
    )
    return render(request, "home.html", {
        "produtos": Product.objects.all(),
        "nome_usuario": request.user.first_name if request.user.is_authenticated else "",
        "perfil": profile.role if profile else "",
    })


def carrinho(request):
    items = _cart_items(request)
    total = sum((item["total"] for item in items), Decimal("0.00"))
    return render(request, "carrinho_de_compras.html", {
        "itens": [
            {"nome": item["product"].name, "preco": item["product"].price,
             "quantidade": item["quantity"], "total": item["total"]}
            for item in items
        ],
        "total_carrinho": total,
    })


@login_required
def finalizar_compra(request):
    items = _cart_items(request)
    return render(request, "compra_finalizada.html", {
        "itens": [
            {"nome": item["product"].name, "preco": item["product"].price,
             "quantidade": item["quantity"], "total": item["total"]}
            for item in items
        ],
        "total_carrinho": sum((item["total"] for item in items), Decimal("0.00")),
    })


@login_required
def compras(request):
    items = _cart_items(request)
    if not items:
        return redirect("carrinho")
    for item in items:
        Purchase.objects.create(
            user=request.user, product=item["product"]
        )
    request.session["cart"] = {}
    return redirect("home")


@require_POST
def adicionar_ao_carrinho(request, produto_id):
    product = get_object_or_404(Product, id=produto_id)
    cart = request.session.get("cart", {})
    key = str(product.id)
    cart[key] = int(cart.get(key, 0)) + 1
    request.session["cart"] = cart
    return redirect("home")


def _is_admin(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    return request.user.is_staff or (profile and profile.role == UserProfile.Role.ADMIN)


@login_required
def produtos(request):
    if not _is_admin(request):
        return redirect("home")
    return render(request, "produtos.html", {"produtos": Product.objects.all()})


@login_required
def editarproduto(request, produto_id):
    if not _is_admin(request):
        return redirect("home")
    product = get_object_or_404(Product, id=produto_id)
    if request.method == "POST":
        name = request.POST.get("nome", "").strip()
        price = request.POST.get("preco", "").strip()
        try:
            product.name = name
            product.price = Decimal(price)
            if not name or product.price < 0:
                raise ValueError
            product.save(update_fields=["name", "price"])
            return redirect("produtos")
        except (ValueError, ArithmeticError):
            messages.error(request, "Informe um nome e um preço válidos.")
    return render(request, "editarproduto.html", {"produto": product})


@login_required
def excluirproduto(request, produto_id):
    if not _is_admin(request):
        return redirect("home")
    product = get_object_or_404(Product, id=produto_id)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Produto excluído com sucesso.")
    return redirect("produtos")

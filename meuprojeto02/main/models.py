from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def produto_id(self):
        return self.id

    @property
    def nome(self):
        return self.name

    @property
    def preco(self):
        return self.price

    @property
    def imagem(self):
        return self.image


class UserProfile(models.Model):
    class Role(models.TextChoices):
        USER = "usuario", "Usuário"
        ADMIN = "administrador", "Administrador"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)


class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
